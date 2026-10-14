"""Package all nine pending feat source cohorts and full current dependencies.

No dispatch, rule edit or approval. Preserve source preparation and rebase the
archive after intervening crafting/spell decisions before a dedicated review.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, zipfile

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
PREFIXES = ['CRAFTING_FEAT_INTERFACE', 'COMBAT_FEAT_SOURCE', 'SKILL_FEAT_SOURCE',
            'MAGIC_CORE_FEAT_SOURCE', 'MAGIC_EXTENDED_FEAT_SOURCE',
            'HERITAGE_MUTATION_FEAT_SOURCE', 'GENERAL_DEFENSE_FEAT_SOURCE',
            'GENERAL_EXPLORATION_FEAT_SOURCE', 'GENERAL_COMBAT_FEAT_SOURCE']

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def digest(v, compact=False):
    # Early feat packets use default JSON spacing; later cohorts use compact
    # spacing. Preserve each recorded convention rather than rewriting hashes.
    opts = {'separators': (',', ':')} if compact else {}
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, **opts).encode()).hexdigest()

def rel(p):
    return p.resolve().relative_to(G).as_posix()

def dump(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    receipt = A / 'FEAT_COMPLETE_FILE_HANDOFF_PREPARATION.json'
    archive = A / 'DD_Pending_Feats_327_Source_Prepared_v1.zip'
    assert not receipt.exists() and not archive.exists(), 'Preserve existing snapshot; create a new revision'
    source_path = R / 'src/data/feats.js'
    source = json.JSONDecoder().raw_decode(source_path.read_text(encoding='utf-8').split('export const feats = ', 1)[1])[0]
    by = {x['id']: x for x in source}
    manifest = read(R / 'data/public/feat_playtests/manifest.json')
    catalog = read(R / 'data/public/feat_playtests/catalog.json')
    reviewed = set(manifest['operationalIds'])
    assert len(source) == len(by) == len(catalog['feats']) == 335
    assert len(reviewed) == manifest['operationalFeats'] == 8
    assert manifest['sourceFileSha256'] == sha(source_path)
    for f in catalog['feats']:
        assert f['sourceObject'] == by[f['id']] and f['sourceObjectSha256'] == digest(by[f['id']])
    pending = set(by) - reviewed
    files, protected, cohorts, membership = set(), {}, [], []
    counterpart_count = 0
    for prefix in PREFIXES:
        prep_path = A / (prefix + '_PREPARATION.json')
        prep = read(prep_path)
        status_path = A / (prefix + '_STATUS.json')
        status = read(status_path)
        packet = A / status['packetFile']
        assert sha(packet) == status.get('packetSha256', status.get('sha256'))
        assert prep['sourceFileSha256'] == sha(source_path)
        files.update([prep_path, status_path, A / (prefix + '_AUDIT.md'), packet])
        for name, h in prep['protectedFiles'].items():
            assert sha(G / name) == h, ('Dependency changed; rebase before packaging', name)
            if name in protected:
                assert protected[name] == h
            protected[name] = h
            files.add(G / name)
        for item in prep['selectedFeats']:
            f = item['sourceObject']
            assert item['featId'] in pending and f == by[item['featId']]
            compact = prefix not in PREFIXES[:3]
            assert item['sourceObjectSha256'] == digest(f, compact)
            question = item.get('fullClauseQuestion', item.get('issue', {}).get('question'))
            assert question
            membership.append({'featId': item['featId'], 'sourceObjectSha256': item['sourceObjectSha256'],
                               'sourceHashJsonSpacing': 'compact' if compact else 'default',
                               'preparationFile': rel(prep_path), 'questionId': item.get('questionId'),
                               'questionField': 'fullClauseQuestion' if 'fullClauseQuestion' in item else 'issue.question'})
        for c in prep.get('counterpartSources', []):
            assert c['sourceObject'] == by[c['sourceObject']['id']]
            counterpart_count += 1
        for c in prep.get('relatedUnapprovedFeatSources', []):
            assert c == by[c['id']]
            counterpart_count += 1
        cohorts.append({'prefix': prefix, 'identities': len(prep['selectedFeats']),
                        'packetFile': packet.name, 'packetSha256': sha(packet),
                        'preparationSha256': sha(prep_path)})
    ids = [x['featId'] for x in membership]
    assert len(ids) == len(set(ids)) == 327 and set(ids) == pending
    assert len(protected) == 109
    old_remaining = read(A / 'REMAINING_FEAT_CATALOG_PREPARATION.json')
    assert {x['id'] for x in old_remaining['records']} == pending
    assert all(x['sourceObject'] == by[x['id']] for x in old_remaining['records'])
    supplement = read(A / 'COMBAT_FEAT_SKILL_DEPENDENCY_SUPPLEMENT.json')
    assert supplement['fullAnatomyLoreSource'] == by[supplement['fullAnatomyLoreSource']['id']]
    cr = supplement['coreRolls']
    assert sha(G / cr['file']) == cr['fileSha256'] and cr['exactText'] in (G / cr['file']).read_text(encoding='utf-8')
    files.update([A / 'COMBAT_FEAT_SKILL_DEPENDENCY_SUPPLEMENT.json',
                  A / 'REMAINING_FEAT_CATALOG_PREPARATION.json', A / 'FEAT_IDENTITY_CANDIDATES.json',
                  A / 'FEAT_REVIEW_QUEUE_VALIDATION.json', R / 'docs/director-only/FEAT_REVIEW_QUEUE.md',
                  R / 'tools/build_feat_review_queue.py', Path(__file__),
                  R / 'books/player/Decennium_Descent_Feat_Compendium_v1.docx',
                  R / 'books/player/Decennium_Descent_Player_Rulebook_v6.docx',
                  R / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',
                  G / 'docs/reference/Player_Rulebook_v6_source_text.txt'])
    classes = read(R / 'data/public/class_playtests/manifest.json')['classes']
    assert len(classes) == 17
    for c in classes:
        files.update([(R / 'docs/mechanics' / c['guide']).resolve(), (R / 'docs/mechanics' / c['data']).resolve()])
    files.update((R / 'data/playtest/class_sources').glob('*.json'))
    files.update((R / 'data/playtest/spell_drafts').glob('batch_*.json'))
    for name in ['NEWCOMER_PLAYER_GUIDE.md', 'NEWCOMER_DIRECTOR_GUIDE.md', 'RESONANCE_CHEATSHEET.md']:
        files.add(R / 'docs/playtest' / name)
    files.add(A / 'ONBOARDING_RULE_SUMMARY_RECONCILIATION.json')
    gather = read(R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json')
    assert all(sha(G / p) == h for p, h in gather['artifactHashes'].items())
    files.update(G / p for p in gather['artifactHashes'])
    files.update([R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json',
                  A / 'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md', A / 'GATHERING_128_EXACT_PROMOTION_RECEIPT.json',
                  A / 'ADVANCED_CRAFT_SOURCE_PREPARATION.json', A / 'ADVANCED_CRAFT_REVIEW_SCENARIOS.md',
                  A / 'ADVANCED_CRAFT_JOINT_SUBMISSION.json'])
    assert all(p.is_file() for p in files)
    report = {'status': 'complete pending-feat files prepared; UNSENT; refresh after intervening decisions',
              'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'cohorts': cohorts,
              'sourceIdentities': 335, 'reviewedUnchanged': 8, 'pendingIdentities': 327,
              'allPendingIncludedExactlyOnce': True, 'all335OriginalsMatchCurrentSource': True,
              'fullSourceObjectHashesVerified': True, 'counterpartOccurrencesVerified': counterpart_count,
              'historicalProtectedUnion': len(protected), 'historicalHashChanges': [],
              'sourceCategoryCounts': dict(Counter(by[x]['type'] for x in pending)),
              'membership': membership, 'sourceSha256': sha(source_path),
              'priorDedicatedFeatConferencesSubmitted': False,
              'earlierComparisonOnlySharing': {'requestTurn': '6b7737b0-b71b-4bfc-8627-4705e81fc26c',
                                              'craftingFeats': 24, 'skillFeats': 25, 'newFeatApprovals': 0},
              'sourceInformationDeleted': 0, 'newApprovals': 0, 'sent': False,
              'dispatchPrerequisite': 'Preserve this snapshot; capture and integrate intervening crafting/spell decisions, then make a current revision for the dedicated feat source review',
              'cosmology': 'literal sources preserved; cosmology interpretation remains after verified GitHub push'}
    rp = A / 'FEAT_COMPLETE_FILE_HANDOFF_SOURCE_CHECK.json'
    assert not rp.exists()
    dump(rp, report)
    files.add(rp)
    prompt = '''PREPARED DEDICATED FEAT SOURCE REQUEST — NOT SENT. Refresh the archive after intervening decisions before use.

Read the complete originals and nine source preparations for all327 pending feats, the full current feat catalog and eight reviewed counterparts, Combat Skill dependency supplement, complete class guides/cards/originals and current governing rules. The335 source identities and all existing status flags remain preserved; source flags and same names are not operational approvals. Crafting24 and Skill25 appeared earlier as unapproved comparisons only.

Resolve every full-clause question with finite authoring directions: actual acquisition/prerequisites and repeatability; activation/trigger/cost/cadence; targets/range/geometry; duration/ending; attacks/saves/checks and every success/failure outcome; all printed benefits, drawbacks and percentages; stacking, resource/repair/recovery boundaries and genuine class/spell/item dependencies. Map each ruling to its exact feat ID and question. Preserve current, legacy and description variants, and label NEW completions explicitly. State which actual existing rule is kept or changed. Do not silently merge similarly named feats, Warrior mutations, ordinary spells or class features.

Give usable bounded defaults where operating details were omitted rather than creating serial preliminary conferences. Keep genuinely missing effects, world permissions and acquisition data explicit. No exact-card approval is requested before the complete authored cards exist. The source Compendium and books are included in full; discrepancies with the preserved registry must be identified, not silently erased. No cosmology interpretation, source deletion or push in this conference. Final joint whole-game flow precedes authorized GitHub delivery; verified remote delivery precedes cosmology review.
'''
    pp = A / 'CODEX_FEAT_COMPLETE_FILE_HANDOFF_PROMPT_PREPARED.txt'
    assert not pp.exists()
    pp.write_text(prompt, encoding='utf-8')
    files.add(pp)
    readme = '''# All327 pending feat sources — complete files, UNSENT

This frozen handoff joins nine existing source cohorts. FEAT_COMPLETE_FILE_HANDOFF_SOURCE_CHECK.json maps every pending feat exactly once to its complete source and individual question. All335 source objects match the current registry and catalog; eight operational feats remain unchanged. All109 historical protected dependency hashes still match. The Combat Skill supplement and complete counterpart records are included. Original packets and their historical scheduling/count text are preserved.

Every FILE_MANIFEST.json entry is included in full at its actual repository-relative path. The feat Compendium, Player Rulebook and Core book are supplied as original references; no new book/registry equivalence is asserted by packaging. All17 class catalogs/guides and preserved class extracts, complete current spell records and draft batches, reviewed gathering files and reconciled onboarding summaries accompany the cohorts. Comparison material is not a new rule grant.

Crafting24 and Skill25 were previously supplied as unapproved comparisons in advanced-crafting request6b7737b0-b71b-4bfc-8627-4705e81fc26c. No dedicated feat source conference or new feat approval is recorded here. The included advanced crafting preparation remains pending source material, not approved mechanics. Before dispatch, integrate actual intervening decisions and produce a refreshed archive; do not overwrite this snapshot or repeat an active request.

Literal cosmology references are preserved without interpretation. Cosmology review stays after final flow, authorized GitHub push and verified remote commit. Runtime, human balance and publication approvals remain separate.
'''
    fm = {rel(p): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files, key=rel)}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW.md', readme.encode('utf-8'))
        z.writestr('FILE_MANIFEST.json', (json.dumps(fm, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        for p in sorted(files, key=rel):
            z.write(p, rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(fm) + 2
        assert all(len(z.read(p)) == m['bytes'] and hashlib.sha256(z.read(p)).hexdigest() == m['sha256'] for p, m in fm.items())
    assert all(sha(G / p) == m['sha256'] for p, m in fm.items())
    report.update({'bundleFile': archive.name, 'bundleSha256': sha(archive), 'bundleBytes': archive.stat().st_size,
                   'payloadFiles': len(fm), 'zipRoundtripVerified': True,
                   'promptFile': pp.name, 'promptSha256': sha(pp),
                   'currentFileHashes': {p: m['sha256'] for p, m in fm.items()}})
    dump(receipt, report)
    print(json.dumps({k: report[k] for k in ['status', 'sourceIdentities', 'reviewedUnchanged', 'pendingIdentities',
                       'historicalProtectedUnion', 'payloadFiles', 'bundleBytes', 'bundleSha256', 'sent']}))

if __name__ == '__main__':
    main()
