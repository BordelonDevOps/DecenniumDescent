"""Preserve and verify the complete gathering sources; prepare a staged GPT conference.

Never sends messages, changes source rules, or promotes cards. Original preparation
packets remain immutable. Each trade gets a bounded source verdict before integration.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as E
from prepare_combat_feat_source_audit import section
from prepare_cooking_exact_review import merge

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
THREAD = '6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def compact(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':'))


def create(p, text):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(text)


def main():
    dest = AUDIT / 'GATHERING_TOOL_PART2_SUBMISSION.json'
    assert not dest.exists(), 'Preserve the prepared conference; use a new revision.'
    original = read(AUDIT / 'GATHERING_TOOL_SOURCE_PACKET_STATUS.json')
    prep = read(AUDIT / 'GATHERING_TOOL_SOURCE_PREPARATION.json')
    source = ROOT / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    source_rows = read(source)['recipes']
    rows = [r for r in source_rows if r['skill'] in prep['trades']]
    assert len(rows) == 128 and rows == prep['recipes']
    assert sha(source) == prep['sourceSha256']
    assert all(c['pass'] for c in prep['checks']) and len(prep['checks']) == 18
    protected = dict(read(AUDIT / 'FISHING_PART2_SUBMISSION.json')['protectedFiles'])

    def protect(p):
        key = p.relative_to(GAME).as_posix()
        value = sha(p)
        assert key not in protected or protected[key] == value, key
        protected[key] = value

    for name in ('GATHERING_TOOL_SOURCE_PACKET_STATUS.json',
                 'GATHERING_TOOL_SOURCE_PREPARATION.json',
                 'GATHERING_TOOL_SOURCE_AUDIT.md',
                 'GATHERING_TOOL_REVIEW_SCENARIOS.md'):
        protect(AUDIT / name)
    protect(source)
    original_texts = {}
    for label, entry in original['parts'].items():
        p = AUDIT / entry['file']
        assert sha(p) == entry['sha256'] and entry['sent'] is False
        original_texts[label] = p.read_text(encoding='utf-8')
        assert len(original_texts[label]) == entry['characters']
        protect(p)
    for trade in prep['trades']:
        text = original_texts[trade.upper()]
        block = text.split('ALL ORIGINAL RECORDS LOSSLESSLY FACTORED\n', 1)[1].split('\n\nEXACT PUBLIC BOOK BINDINGS', 1)[0]
        factored = json.loads(block)
        expected = [r for r in rows if r['skill'] == trade]
        reconstructed = [merge(factored['COMMON'], factored['recipeOverrides'][r['id']]) for r in expected]
        assert reconstructed == expected
        assert all(source_rows[index]['id'] == rid for rid, index in factored['sourceIndices'].items())
    book = GAME / 'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    assert sha(book) == prep['bookSha256']
    protect(book)
    with zipfile.ZipFile(book) as z:
        tree = E.fromstring(z.read('word/document.xml'))
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    paragraphs = [''.join(t.text or '' for t in p.iter(w + 't')) for p in tree.iter(w + 'p')]
    assert len(prep['publicBookBindings']) == 82
    assert all(paragraphs[p['index']] == p['text'] for b in prep['publicBookBindings'] for p in b['paragraphs'])
    for b in prep['reviewedBoundaryEvidence']:
        p = GAME / b['file']
        assert sha(p) == b['sha256'] and b['exactParagraph'] in p.read_text(encoding='utf-8')
        protect(p)
    version = prep['versionAudit']
    for key, expected_hash in version['sourceHashes'].items():
        p = GAME / version['sourcePaths'][key]
        assert sha(p) == expected_hash
        protect(p)
    scenarios = (AUDIT / 'GATHERING_TOOL_REVIEW_SCENARIOS.md').read_text(encoding='utf-8')
    assert len(set(re.findall(r'GT-\d\d', scenarios))) == 32

    manifests = []
    for name in ('ALCHEMY', 'HERBALISM', 'COOKING', 'POISONCRAFTING',
                 'BLACKSMITHING', 'LEATHERWORKING', 'TAILORING',
                 'JEWELCRAFTING', 'FISHING'):
        p = ROOT / f'docs/mechanics/{name}_REVIEW_STATUS.json'
        m = read(p)
        assert m['status'].startswith('REVIEWED')
        protect(p)
        for relative, expected_hash in m['artifactHashes'].items():
            assert sha(GAME / relative) == expected_hash
            protect(GAME / relative)
        manifests.append(m)
    fishing = manifests[-1]
    assert fishing['aggregateReviewedRecipes'] == 392 and fishing['publicReviewedRecipes'] == 251
    assert fishing['remainingRecipeEffects'] == 295 and fishing['validationChecks'] == 717
    refs = {
        'CRAFTING_HARVEST_PLAYTEST.md': None,
        'CRAFTING_TRADE_REFERENCE.md': None,
        'EQUIPMENT_ACQUISITION_PLAYTEST.md': None,
        'BODY_EQUIPMENT_PLAYTEST.md': None,
        'FISHING_RECIPE_PLAYTEST.md': None,
        'CORE_RESOLUTION_PLAYTEST.md': ['Which rule applies', 'Rolls'],
        'BLACKSMITHING_RECIPE_PLAYTEST.md': [
            'Complete bodies and exact ingredients',
            'Base custody, transformation and mass',
            'Structural state and suppression',
            'Craft quality and preexisting damage',
            'Repair and reconstruction',
            'Work phases, stations and source access',
            'Reference value and access'],
        'CREATURE_LIFECYCLE_PLAYTEST.md': ['At the table', 'Different kinds of creature life', 'Stats and ownership'],
        'GAMEPLAY_LOOP_CANON.md': ['5. Opening clock and Watches', '6. Route procedure',
                                  'Resource Team', 'Team check procedure', 'Supply Units',
                                  '15. Harvesting and salvage'],
    }
    excerpts = []
    for name, heads in refs.items():
        p = ROOT / 'docs/mechanics' / name
        text = p.read_text(encoding='utf-8')
        protect(p)
        for heading in heads or [None]:
            excerpts.append({
                'file': p.relative_to(GAME).as_posix(), 'heading': heading,
                'sha256': sha(p), 'exactText': section(text, heading) if heading else text,
                'scope': ('Source travel/Supply procedure; whole expedition/Haven audit remains open. Later reviewed Core/crafting/equipment/Fishing rules control their stated interfaces.'
                          if name == 'GAMEPLAY_LOOP_CANON.md' else
                          'Existing operational text within its own scope; trade-specific values are comparative evidence, not automatic new gathering-tool values.')})
    current = '''Codex to Calibration Review Part 2: begin the Mining, Skinning and Salvaging SOURCE/INTERFACE conference. This is staged so you can resolve each complete trade without waiting for an oversized combined verdict.

PART A supplies current governing rules. Acknowledge receipt only. Next PART B supplies shared source evidence, all32 GT scenarios and every Mining original; then give a finite Mining/shared-interface authoring verdict. PART C will supply every Skinning original for its own finite verdict. PART D will supply every Salvaging original. Finally we will reconcile the three source verdicts together before authoring exact operational cards. A source verdict alone approves zero cards.

Current verified status: nine recipe trades reviewed,392/687 recipes;295 remaining. Public251/433 reviewed,182 remaining. Fishing44 has completed FI-E01..11 and717 local checks; you acknowledged its receipt in reply7274a2b3-0c08-49e7-916a-1e09ce3b7f7b. That acknowledgement is not an independent retest. Mining43/Skinning43/Salvaging42 are wholly pending:82public/6restricted/40Director-only. The old preparation's262 totals, pending Tailoring and active Leatherworking references are historical logistics only. All nine reviewed manifests have freshly verified artifact hashes.

The complete original prepared files are preserved byte-for-byte. No source was deleted. The original developed/needsReview flags do not approve operational effects. Recipe and resultItem extraYield1 values omitted from prose require explicit dispositions, not a silent reinterpretation. Mining/Skinning/Salvaging are NON-ARTISAN credentials. Existing dismantling is binary DC10 and25% physical mundane recovery; a printed critical Salvaging clause needs an explicit new bridge. Finite material identity, selected pools, prior damage, loss/forfeiture, suppression, containment, source visibility and real body custody remain consequential. Fishing's actual finite-stock and material chronology rules are included in full for interface review; its fishing-specific times and values do not automatically govern mining or carcass work.

Use our supplied game sources, not outside RPG assumptions. Clearly label each NEW authoring completion, with exact affected IDs/families, bounds, concrete values, failure behavior and interaction with existing rules. Names/tags, donors and Soul-Circuit/Unholy/Arcane language cannot establish ecology, availability, cosmology or magical salvage authority. List true unresolved dependencies rather than inventing source facts. Full game integration, human playtesting/balance, market/ingredient availability and companion runtime remain open. The owner requires final whole-game joint flow confirmation before authorized GitHub push; verify the remote commit before careful cosmology review. No push or cosmology review yet.

Please preserve full source verdicts in your response, and also offer a verbatim UTF-8 Markdown download if long. Later exact operational cards will return for separate review. For this PART A only, acknowledge receipt and await PART B.
'''
    part_a = current + '\nEXACT CURRENT GOVERNING RULES\n' + compact(excerpts)
    part_a += '\nVERIFIED FISHING REVIEW MANIFEST\n' + compact(fishing)
    part_a += '\nEND PART A. Acknowledge receipt only; wait for PART B.'
    part_b = '''Codex PART B: shared gathering-tool evidence and ALL43 Mining originals. PART A already supplied current governing rules. After reading this part, issue finite GT-M authoring decisions for Mining and shared interfaces: resolve GT-01..18 and GT-29..32 as far as these actual Mining sources permit; identify constraints needed by later Skinning/Salvaging, but do not pretend their original records are supplied yet. Address every printed Mining effect and every one of its13 extraYield1 omissions, all six physical families, roles/attempts/deposits/retries, quality steps, creation/repair/value, suppression and public projection. Provide complete NEW body values and procedures where sources leave gaps, with concrete worked cases including GT-04's recipe322 and GT-15's finite deposit. Preserve existing sources. Do not promote cards.

All following prepared source text is VERBATIM historical evidence. Its unsent/pending/active logistics and old counts are superseded by PART A. The preserved formulas, fields, book paragraphs and source questions remain authoritative evidence of what the files say. Current392reviewed,295remaining; all128 gathering-tool cards still pending.
\n''' + original_texts['SHARED_INTERFACES'] + '\n\nALL43 MINING SOURCES\n' + original_texts['MINING']
    part_b += '\n\nEND PART B. Give the complete Mining/shared source-authoring verdict now. Defer Skinning- and Salvaging-specific final decisions until their complete originals arrive.'
    parts = {'A_CURRENT_RULES': part_a, 'B_SHARED_AND_MINING': part_b}
    for label, trade, count, focus in [
        ('C_SKINNING', 'SKINNING', 43, 'GT-14 and GT-19..22 plus GT-01..12 andGT-29..32; all12 omitted extraYield1 fields and all five physical families; actual selected finite anatomy and prior damaged-unit critical preservation, clocks and quality steps'),
        ('D_SALVAGING', 'SALVAGING', 42, 'GT-23..28 plus GT-01..12 andGT-29..32; all six physical families, six exact recovery percentages and the new critical bridge, indivisible-unit arithmetic, irreversible source-component accounting and no magic/unique salvage by name'),
    ]:
        parts[label] = f'''Codex PART {label[0]}: all{count} complete {trade} source records and their exact public book bindings. Review against PART A's current rules, PART B's complete shared evidence/all32 cases and the prior trade source verdict(s). Current392/687 reviewed; all128 gathering-tool cards remain pending. Focus: {focus}. Give finite GT-{trade[0]} authoring decisions, clearly NEW where required, complete body values and operational procedures, exact affected recipe IDs and worked edge cases. Reconcile shared-interface choices explicitly; identify any changed earlier decision instead of silently contradicting it. This is source authoring, zero exact card promotions. Original prepared logistics are historical, as explained in PART A; all original source fields remain preserved. No deletion, push or cosmology review.
\n''' + original_texts[trade] + f'\n\nEND COMPLETE {trade} SOURCE PART. Give the complete source-authoring verdict now; a final joint integration pass across all three verdicts follows.'
    assert all(sha(GAME / p) == h for p, h in protected.items())
    status = {
        'status': 'Prepared current staged gathering-tool source conference; not sent',
        'threadId': THREAD, 'parts': {}, 'sourceRecipes': 128, 'sourceReconstructions': 128,
        'publicBookBindings': 82, 'sourceScenarios': 32, 'currentGuideExcerpts': len(excerpts),
        'currentReviewedTotal': 392, 'remaining': 295, 'publicReviewed': 251,
        'recipesApproved': 0, 'protectedFiles': protected, 'sourceInformationDeleted': 0,
        'githubPushed': False, 'cosmology': 'post-verified-push only',
        'next': 'Send A; capture actual acknowledgement; send B for Mining verdict; then C, D and a three-verdict integration pass.'}
    for label, text in parts.items():
        p = AUDIT / f'CODEX_GATHERING_TOOL_PART2_{label}.txt'
        create(p, text)
        status['parts'][label] = {'file': p.name, 'characters': len(text), 'sha256': sha(p), 'sent': False}
    create(dest, json.dumps(status, ensure_ascii=False, indent=2) + '\n')
    print(compact({k: v for k, v in status.items() if k != 'protectedFiles'} | {'protectedFiles': len(protected)}))


if __name__ == '__main__':
    main()
