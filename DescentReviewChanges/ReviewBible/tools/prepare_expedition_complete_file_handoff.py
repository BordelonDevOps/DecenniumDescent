"""Package the26 prepared expedition/Haven cases; no rules or dispatch."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile, xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.resolve().relative_to(G).as_posix()

def dump(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    receipt = A / 'EXPEDITION_COMPLETE_FILE_HANDOFF_PREPARATION.json'
    archive = A / 'DD_Expedition_Haven_26_Source_Prepared_v1.zip'
    assert not receipt.exists() and not archive.exists(), 'Keep prior snapshot'
    pp = A / 'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json'
    prep = read(pp)
    sp = A / 'EXPEDITION_HAVEN_FLOW_SOURCE_STATUS.json'
    status = read(sp)
    packet = A / status['packetFile']
    assert sha(packet) == status['packetSha256']
    assert len(prep['protectedFiles']) == 84
    assert all(sha(G / p) == h for p, h in prep['protectedFiles'].items())
    assert len(prep['decisionCases']) == len({x['id'] for x in prep['decisionCases']}) == 26
    assert all(x['question'] for x in prep['decisionCases'])
    files = {G / p for p in prep['protectedFiles']}
    files.update([pp, sp, packet, A / 'EXPEDITION_HAVEN_FLOW_SOURCE_AUDIT.md', Path(__file__)])
    for ex in prep['loopSections'] + prep['currentGoverningExcerpts']:
        assert sha(G / ex['file']) == ex['sha256']
        assert ex['exactText'] in (G / ex['file']).read_text(encoding='utf-8')
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    book_matches = {}
    for name, file_key, hash_key, records_key in [
        ('playerExpeditionSource', 'sourceFile', 'sourceSha256', 'paragraphs'),
        ('coreEconomySource', 'file', 'sha256', 'passages')]:
        block = prep[name]
        p = G / block[file_key]
        assert sha(p) == block[hash_key]
        with zipfile.ZipFile(p) as z:
            tree = ET.fromstring(z.read('word/document.xml'))
        paragraphs = [''.join(t.text or '' for t in para.findall('.//w:t', ns)) for para in tree.findall('.//w:p', ns)]
        assert all(paragraphs[x['paragraph']] == x['text'] for x in block[records_key])
        book_matches[name] = len(block[records_key])
    assert book_matches == {'playerExpeditionSource': 126, 'coreEconomySource': 260}
    catalog = {x['id']: x for x in read(R / 'data/public/spell_playtests/catalog.json')['spells']}
    for row in prep['reviewedSpellCounterparts']:
        assert row == catalog[row['id']]
    reputation = prep['runtimeReputationEvidence']
    assert sha(G / reputation['file']) == reputation['sha256']
    assert all(x['exactText'] in (G / reputation['file']).read_text(encoding='utf-8') for x in reputation['excerpts'])
    # Current full references supplement the old packet, without changing it.
    for name in ['NEWCOMER_PLAYER_GUIDE.md', 'NEWCOMER_DIRECTOR_GUIDE.md', 'RESONANCE_CHEATSHEET.md']:
        files.add(R / 'docs/playtest' / name)
    files.add(A / 'ONBOARDING_RULE_SUMMARY_RECONCILIATION.json')
    for name in ['CLASS_PLAYTEST_RULES.md', 'EQUIPMENT_STARTING_PACKAGES.md', 'EQUIPMENT_ITEM_PROCEDURES.md',
                 'CRAFTING_TRADE_REFERENCE.md', 'CRAFTING_RECIPE_REVIEW_INDEX.md', 'CONDITION_RECOVERY_PLAYTEST.md']:
        files.add(R / 'docs/mechanics' / name)
    cm = read(R / 'data/public/class_playtests/manifest.json')
    assert len(cm['classes']) == 17
    for c in cm['classes']:
        files.add((R / 'docs/mechanics' / c['guide']).resolve())
    files.update((R / 'data/playtest/class_sources').glob('*.json'))
    gather = read(R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json')
    assert all(sha(G / p) == h for p, h in gather['artifactHashes'].items())
    files.update(G / p for p in gather['artifactHashes'])
    files.update([R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json',
                  A / 'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md', A / 'GATHERING_128_EXACT_PROMOTION_RECEIPT.json',
                  A / 'ADVANCED_CRAFT_SOURCE_PREPARATION.json', A / 'ADVANCED_CRAFT_REVIEW_SCENARIOS.md',
                  A / 'ADVANCED_CRAFT_JOINT_SUBMISSION.json'])
    assert all(p.is_file() for p in files)
    report = {'status': 'complete expedition/Haven source files prepared; UNSENT; refresh interfaces before dispatch',
              'preparedAtUtc': datetime.now(timezone.utc).isoformat(),
              'sourceCases': 26, 'caseIds': [x['id'] for x in prep['decisionCases']],
              'historicalProtectedFiles': 84, 'historicalHashChanges': [],
              'actualBookParagraphMatches': book_matches, 'loopSections': 21, 'governingExcerpts': 22,
              'reviewedSpellCounterpartsVerified': len(prep['reviewedSpellCounterparts']),
              'historicalPacketSha256': sha(packet), 'originalPreparationSha256': sha(pp),
              'sourceCountsPreserved': prep['counts'], 'sent': False, 'newApprovals': 0,
              'sourceInformationDeleted': 0, 'runtimeChanged': False, 'cosmologyReviewed': False,
              'dispatchPrerequisite': 'Integrate actual intervening crafting/spell/feat decisions and create a refreshed handoff; preserve this snapshot',
              'scope': 'Preparation-to-Haven operating procedures and source conflicts; not whole-game final approval or cosmology review'}
    rp = A / 'EXPEDITION_COMPLETE_FILE_HANDOFF_SOURCE_CHECK.json'
    assert not rp.exists()
    dump(rp, report)
    files.add(rp)
    prompt = '''PREPARED EXPEDITION/HAVEN SOURCE REQUEST — NOT SENT. Refresh current interfaces after intervening reviews before use.

Read all26 FL cases and their complete sources in EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json, the actual books, full Gameplay Loop, governing rules and current comparison material. The original packet is preserved, including its historical scheduling labels. The84 historical dependency files are unchanged;126 player-expedition and260 Core-economy paragraphs match the actual Word documents.

Settle the finite operating decisions for preparation, funding, roster/team assignments, Supply, Watches, routes, Pressure, retreat, cargo, extraction, transport, appraisal, claims, reputation and Haven settlement. Preserve printed quantities, classifications, distinct body/item/value identities and all conflicting source versions. Map each decision to its FL case and actual governing authority. Use already reviewed Core/combat/injury/rest/carrying/class rules without reopening settled conflicts or silently applying legacy alternatives. Label NEW completions, state prerequisites and costs, give success/failure/interruption outcomes and worked boundary examples sufficient to author the complete procedure.

Treat real availability, prices, world permissions and disputed ownership as bounded scene inputs rather than infinite preliminary reviews or automatic grants. Ordinary operational defaults can be authored explicitly. Do not make an unresolved source-only spell, feat or advanced recipe executable by naming it. Reconcile artifact valuation, recipe/unit references and actual transactions without guaranteed arbitrage or free resource recovery. Finish with one traceable journey from objective and loadout through encounters, extraction, settlement and advancement, identifying only genuine remaining authoring dependencies.

Do not interpret source cosmic terms, review the excluded seasonal/cosmology chapter, or broaden this into a setting rewrite. No new world origins, soul/afterlife/plane rules, deletion, runtime installation or GitHub push. This is a source-authoring conference; full candidate procedures and examples follow for exact review. Final joint whole-game flow precedes authorized GitHub delivery, and verified remote delivery precedes cosmology review.
'''
    prompt_path = A / 'CODEX_EXPEDITION_COMPLETE_FILE_HANDOFF_PROMPT_PREPARED.txt'
    assert not prompt_path.exists()
    prompt_path.write_text(prompt, encoding='utf-8')
    files.add(prompt_path)
    readme = '''# Expedition to Haven —26 complete source cases, UNSENT

The original preparation, audit, text packet and status remain unchanged. Read the prepared complete-file prompt and EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json. All84 historical protected files and all386 actual bound Word-book paragraphs match. Full current class guides, original class evidence, operational interfaces, gathering receipts and reconciled newcomer references supplement the old packet.

FILE_MANIFEST.json inventories complete files at repository-relative paths. Historical embedded scheduling and review-count text does not control current status. The advanced-crafting material is still pending source evidence, not approved recipe mechanics. The current startup guides summarize existing authorities but do not close the expedition questions or final starter-session flow.

Refresh this package after actual intervening decisions, retaining this snapshot. Preparation grants no source decision, operational approval, balance result or software parity. Source cosmic terms remain literal and uninterpreted; excluded cosmology/seasonal content stays outside the pre-push review. Final whole-game flow, authorized GitHub delivery and remote verification precede the careful cosmology review.
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
                   'promptFile': prompt_path.name, 'promptSha256': sha(prompt_path),
                   'currentFileHashes': {p: m['sha256'] for p, m in fm.items()}})
    dump(receipt, report)
    print(json.dumps({k: report[k] for k in ['status', 'sourceCases', 'historicalProtectedFiles',
                       'actualBookParagraphMatches', 'payloadFiles', 'bundleBytes', 'bundleSha256', 'sent']}))

if __name__ == '__main__':
    main()
