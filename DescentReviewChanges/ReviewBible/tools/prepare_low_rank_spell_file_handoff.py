"""Consolidate existing unsent low-rank spell sources without changing rules.

This is a frozen preparation snapshot. Refresh after the active advanced-craft
review and integration before dispatch; no external message is sent here.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, zipfile, xml.etree.ElementTree as ET
from prepare_low_illusion_spell_source_audit import current_book_rows, digest

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
PREFIXES = ['LOW_ILLUSION_SPELL', 'LOW_UNIVERSAL_SPELL',
            'LOW_TRANSMUTATION_SPELL', 'LOW_NECROMANCY_SPELL',
            'EVOCATION_RANK3', 'REMAINING_RANK3_SPELL']

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.resolve().relative_to(G).as_posix()

def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    out = A / 'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json'
    archive = A / 'DD_Low_Rank_Spells_137_Source_Prepared_v1.zip'
    assert not out.exists() and not archive.exists(), 'Preserve existing preparation; create a new revision'
    cat = read(R / 'data/public/spell_playtests/catalog.json')
    cm = read(R / 'data/public/class_playtests/manifest.json')
    class_paths = {c['class']: (R / 'docs/mechanics' / c['data']).resolve() for c in cm['classes']}
    by = {x['id']: x for x in cat['spells']}
    source = read(R / 'data/playtest/spell_sources/catalog.json')
    core = read(R / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    actual = json.JSONDecoder().raw_decode((R / 'src/data/spells.js').read_text(encoding='utf-8').split('export const SPELLS = ', 1)[1])[0]
    assert actual == source and len(by) == 848
    for row in by.values():
        assert row['source']['original'] == source[row['id']]
        for entry in row['source']['coreEntries'] + row['source']['possibleHistoricalAliases']:
            assert entry['original'] == core['spells'][entry['index']]
    book_rows = current_book_rows()
    book_by_line = {x['line']: x for x in book_rows}
    book = R / 'books/player/Decennium_Descent_Player_Rulebook_v6.docx'
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(book) as z:
        xml = ET.fromstring(z.read('word/document.xml'))
    paras = [''.join(t.text or '' for t in p.findall('.//w:t', ns))
             for p in xml.findall('.//w:body/w:p', ns)]
    para_indices = {}
    for i, p in enumerate(paras):
        para_indices.setdefault(p, []).append(i)
    assert len(book_rows) == 936 and all(x['exactText'] in para_indices for x in book_rows)

    files, historical_hashes, cohorts, selected, bindings = set(), {}, [], [], []
    comparison_count = counterpart_count = 0
    for prefix in PREFIXES:
        pp = A / (prefix + '_SOURCE_PREPARATION.json')
        prep = read(pp)
        status = read(A / (prefix + '_SOURCE_STATUS.json'))
        packet = A / status['packetFile']
        assert sha(packet) == status['packetSha256']
        files.update([pp, A / (prefix + '_SOURCE_AUDIT.md'), A / (prefix + '_SOURCE_STATUS.json'), packet])
        for name, h in prep['protectedFiles'].items():
            historical_hashes.setdefault(name, set()).add(h)
            assert sha(G / name) == h, ('Dependency changed; record a rebase first', name)
            files.add(G / name)
        assert prep['currentRankCosts'] == cat['costByRank']
        assert prep['currentClassProgression'] == cat['classProgression']
        for item in prep['selectedSpells']:
            row = item['fullSourceAndCurrentAccessRecord']
            assert row == by[item['spellId']] and item['recordSha256'] == digest(row)
            assert row['operational'] is None and item['individualQuestion']
            selected.append({'spellId': item['spellId'], 'questionId': item['questionId'],
                             'preparationFile': rel(pp), 'recordSha256': item['recordSha256'],
                             'scope': 'post-push receipt only' if item['spellId'] == 'blink' else 'pre-push mechanics'})
        for binding in prep['currentBookBindings']:
            b = binding['currentBookRow']
            assert b == book_by_line[b['line']]
            assert binding['catalogPlacement'] in by[binding['spellId']]['source']['original']['placements']
            bindings.append({**binding, 'actualDocxFile': rel(book),
                             'actualDocxZeroBasedParagraphIndices': para_indices[b['exactText']]})
        for other in prep['completeCounterparts']:
            assert other == by[other['id']]
            counterpart_count += 1
        for c in prep['classComparisonRecords']:
            data = read(G / c['path'] if 'path' in c else class_paths[c['mention']['class']])
            if 'card' in c:
                assert c['card'] in data['cards']
            elif 'engine' in c:
                assert c['engine'] == data['engine']
            else:
                assert c['paragraph'] == data['engine'][c['engineIndex']]
            comparison_count += 1
        for e in prep['currentGoverningExcerpts']:
            assert sha(G / e['file']) == e['sha256']
            assert e['exactText'] in (G / e['file']).read_text(encoding='utf-8')
        cohorts.append({'prefix': prefix, 'identities': len(prep['selectedSpells']),
                        'bookBindings': len(prep['currentBookBindings']), 'originalPacketSha256': sha(packet)})
    selected_ids = [x['spellId'] for x in selected]
    pending_low = {x['id'] for x in by.values() if x['operational'] is None
                   and min(v['rank'] for v in x['classAccess'].values()) <= 3}
    assert len(selected_ids) == len(set(selected_ids)) == 137 and set(selected_ids) == pending_low
    assert len(bindings) == 141
    assert sum(x['operational'] is not None for x in by.values()) == 276
    assert len([x for x in selected if x['scope'] == 'post-push receipt only']) == 1
    cm = read(R / 'data/public/class_playtests/manifest.json')
    assert len(cm['classes']) == 17
    for c in cm['classes']:
        files.add((R / 'docs/mechanics' / c['guide']).resolve())
    files.update((R / 'data/playtest/class_sources').glob('*.json'))
    files.update([book, R / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',
                  G / 'docs/reference/Player_Rulebook_v6_source_text.txt',
                  R / 'docs/mechanics/CLASS_PLAYTEST_RULES.md',
                  R / 'tools/prepare_low_illusion_spell_source_audit.py',
                  R / 'tools/prepare_combat_feat_source_audit.py', Path(__file__)])
    gathering = read(R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json')
    assert all(sha(G / p) == h for p, h in gathering['artifactHashes'].items())
    files.update(G / p for p in gathering['artifactHashes'])
    files.update([R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json',
                  A / 'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md',
                  A / 'GATHERING_128_EXACT_PROMOTION_RECEIPT.json'])
    assert all(p.is_file() for p in files)

    report = {'status': 'complete files prepared; UNSENT; refresh after advanced-craft integration',
              'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'cohorts': cohorts,
              'selectedIdentities': 137, 'prePushMechanicalQuestions': 136,
              'postPushReceiptOnlyIds': ['blink'], 'currentBookBindings': 141,
              'actualDocxParagraphCount': len(paras), 'all936BookRowsPresentInActualDocx': True,
              'originalsMatchCatalogAndCore': True, 'selectedRecordsMatchCurrentCatalog': True,
              'completeCounterpartComparisons': counterpart_count, 'classComparisons': comparison_count,
              'historicalProtectedUnion': len(historical_hashes), 'historicalHashChanges': [],
              'allPendingMinimumRankZeroToThreeIncludedExactlyOnce': True,
              'ordinarySpellsOperational': 276, 'ordinarySpellsPending': 572,
              'selectedMembership': selected, 'bookBindingsWithActualDocx': bindings,
              'newApprovals': 0, 'sent': False, 'sourceInformationDeleted': 0,
              'dispatchPrerequisite': 'Capture and integrate active advanced167 verdict; create a refreshed revision with changed-interface evidence before dispatch',
              'activeAdvancedRequestTurn': '6b7737b0-b71b-4bfc-8627-4705e81fc26c',
              'cosmology': 'post-push only; Blink unchanged receipt, no mechanical decision or interpretation'}
    rp = A / 'LOW_RANK_SPELL_FILE_HANDOFF_SOURCE_CHECK.json'
    assert not rp.exists()
    dump(rp, report)
    files.add(rp)
    prompt = '''PREPARED REQUEST; NOT SENT. Rebase the attached files after the active advanced-crafting review before use.

Read the complete-file handoff for all137 remaining ordinary spell identities with minimum current class-access rank0–3. Six source preparations retain every original, Core variant, class-access route, individual source question, comparison and141 book bindings. All936 spell rows were also found in the supplied actual Player Rulebook V6. Resolve136 mechanical questions; Blink is an unchanged post-push receipt only.

Give finite authoring directions that settle each real source conflict and all operational fields: casting action/components, target/range/geometry, duration/concentration, saves/attacks and outcomes, every effect clause, scaling, source identity/recast, suppression/ending, and class-specific rank/cost access. Label new completions NEW and identify exactly which prior rule each completion keeps or changes. Map directions to every affected spell and original question ID. Supply worked boundary examples for contested procedures. Shared names never merge ordinary spells, class features or crafted outputs.

Use current complete governing files; original preparation scheduling labels are historical. Do not reopen already settled sources without an actual conflict or turn routine missing operating details into serial preliminary conferences. Keep genuine acquisition or world permissions bounded. Preserve all originals, aliases and placement differences; do not import another game's named-spell implementation. No exact-card approval is requested until authored cards exist. No cosmology decisions, deletion or push. Final joint whole-game flow must precede the authorized GitHub push, and remote verification precedes cosmology review.
'''
    pp = A / 'CODEX_LOW_RANK_SPELL_FILE_HANDOFF_PROMPT_PREPARED.txt'
    assert not pp.exists()
    pp.write_text(prompt, encoding='utf-8')
    files.add(pp)
    readme = '''# Low-rank spell complete-file preparation — UNSENT

This is a frozen preparation, not a dispatched review. The active advanced167 crafting conference must finish and relevant decisions must be integrated before a refreshed revision is sent. All originals remain intact.

The six SOURCE_PREPARATION.json files are the question and source authorities for137 distinct pending identities and141 book bindings.136 are mechanical questions; Blink is receipt-only for after the verified GitHub push. All six historical text packets, audits and status records are retained. Their old conference scheduling labels are historical. LOW_RANK_SPELL_FILE_HANDOFF_SOURCE_CHECK.json proves current membership, source/Core identity, full comparisons, unchanged78 historical dependencies and actual DOCX spell paragraph bindings.

FILE_MANIFEST.json supplies full-file hashes and sizes. Current sources, all23 prior ordinary spell batches plus the ancestry-dependency batch, all17 class catalogs and guides, original class extracts, current governing mechanics and newly completed gathering files are supplied in full at repository-relative paths. Comparison text does not grant access or approve any pending spell, feat or recipe. Current totals remain276 operational ordinary spells and572 pending of848;936 source placements are preserved. The actual rulebooks are included as original reference material; incidental cosmology text stays uninterpreted.
'''
    manifest = {rel(p): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files, key=rel)}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW.md', readme.encode('utf-8'))
        z.writestr('FILE_MANIFEST.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        for p in sorted(files, key=rel):
            z.write(p, rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(manifest) + 2
        assert all(len(z.read(p)) == m['bytes'] and hashlib.sha256(z.read(p)).hexdigest() == m['sha256']
                   for p, m in manifest.items())
    assert all(sha(G / p) == m['sha256'] for p, m in manifest.items())
    report.update({'bundleFile': archive.name, 'bundleSha256': sha(archive),
                   'bundleBytes': archive.stat().st_size, 'payloadFiles': len(manifest),
                   'zipRoundtripVerified': True, 'promptFile': pp.name, 'promptSha256': sha(pp),
                   'currentFileHashes': {p: m['sha256'] for p, m in manifest.items()}})
    dump(out, report)
    print(json.dumps({k: report[k] for k in ['status', 'selectedIdentities', 'prePushMechanicalQuestions',
                       'currentBookBindings', 'historicalProtectedUnion', 'payloadFiles', 'bundleBytes', 'bundleSha256', 'sent']}))

if __name__ == '__main__':
    main()
