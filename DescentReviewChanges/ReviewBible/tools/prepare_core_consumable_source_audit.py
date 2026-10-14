"""Preserve all12 Core brews and12 substances for their own source conference.

No operational rules are supplied or changed. Cosmic perception/setting clauses
remain explicit receipts for the owner-directed post-push review.
"""
from pathlib import Path
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib, json, re

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'CORE_CONSUMABLE_24_SOURCE_PREPARATION.json'
DOC = A / 'CORE_CONSUMABLE_24_SOURCE_AUDIT.md'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
protected = {}


def rel(p): return p.relative_to(G).as_posix()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(p): protected[rel(p)] = sha(p); return p.read_text(encoding='utf-8-sig')
def read(p): return json.loads(raw(p))
def dump(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


BREW_QUESTIONS = [
    "Define one real serving's volume/mass and drinking time using current ingestion rules. Preserve one-serving no-Intoxication and hydration-safe language; decide repeated servings and actual water/nutrition credit without creating Supply or unlimited exemptions.",
    "Define the eligible spoiled-food save, when the one advantage entitlement is spent, eight-hour expiry and repeat-serving behavior. It does not by its wording cure an existing illness, remove a consumed poison or guarantee safe food.",
    "The source says first level of cold-weather exposure but supplies no scale in this record. Reconcile HZ-03 and actual exposure sources before choosing that effect. Preserve four hours and price; do not silently convert it to cold resistance or Exhaustion removal.",
    "Locate or author the actual seasickness procedure, eligible checks and frequency; preserve eight-hour advantage. Distinguish seasickness from drowning, poison and general balance checks, and specify repeat servings without stacking advantage.",
    "Resolve the literal phrase fire resistance 1 against environmental heat: flat reduction, resistance magnitude or another source-specific rule. Preserve one hour and distinguish environmental exposure from combat fire; do not silently replace the numeral with universal halving.",
    "Define during the meal, one eligible Nature or Performance check, expenditure/expiry and repeated servings. A meal does not create a roll, proficiency, a complete research task or a stack of unspent bonuses.",
    "Define when dreams occur and finish, whose knowledge/agency bounds an emotional truth, the Wisdom-save DC and exact nightmare consequence/duration. Do not determine protected cosmological truth or dictate a player's chosen identity and emotions.",
    "Specify flat-speed ordering with current movement, ten-minute expiry, one post-effect Intoxication point and repeated/overlapping servings. Dispel, suppression or early ending cannot silently erase a printed consequence; decide each actual ending route.",
    "Define the one fear-save advantage entitlement, its expiry and what consumed too quickly means under the actual drinking procedure. Preserve one fire damage and its legitimate mitigation; no extra attacks or undefined forced drinking.",
    "Separate hunger sensation from actual food/water/Supply need. Define healing-received reduction per actual healing packet, minimum, order, duration, suppression and repeated servings using the reviewed healing pipeline; avoid duplicate subtraction on derived/redirected healing.",
    "Use the reviewed language/communication predicates to define whispers, receiving/sending telepathy and the exact cannot-benefit-from-Bard-Chants clause for one hour. Preserve other hearing and non-Chant features unless the source actually covers them. Do not interpret deferred voices or cosmological origins.",
    "Preserve the unique vintage, State-controlled price field and final-spoken-sentence wording. The meaning of final, where a record persists and what could reveal it is not established here. Carry this as a receipt for the deferred soul/death/information review; do not invent terminal-state recording rules before that review.",
]
SUBSTANCE_QUESTIONS = [
    "Preserve +10 feet and initiative advantage for ten minutes, then the already-reviewed +1 expedition Strain and independent one-hour DEX-check disadvantage. Define dose/recast/crash scheduling and initiative eligibility; no reroll of established initiative or merging with Warrior serum Strain.",
    "Define sleep and a directed symbolic vision without granting unsourced protected knowledge; map Divination checks to actual eligible checks. Resolve the causal ambiguity first failed Wisdom save ... made with disadvantage into a finite procedure, with exact next-rest anchors, waking crash and repeated-dose behavior.",
    "Preserve temporary HP equal to twice the user's actual PB and ten-minute suppression of one Wound penalty. Define exactly which penalty is ignored, current Wound count/HD consequences, 1d6 crash damage type/timing and the cannot-benefit-until-long-rest lock; do not erase a Wound or turn temporary HP into healing.",
    "Preserve 120-foot darkvision and detection of invisible movement within10 feet for one hour. Specify what movement detection actually reveals, barriers and stationary targets using reviewed vision rules. Define the later one-hour bright-light sight-check disadvantage and ongoing dose clocks.",
    "Preserve ten-minute ethereal-creature/spiritual-residue perception and the end-effect fear clause, dependence DC and price as exact source. Its perception taxonomy depends on the owner's deferred planes/souls review. Do not operationalize that taxonomy or invent spirit/corpse identity, visibility, Wisdom DC or targeting scope in this pre-push preparation.",
    "Define advantage against spells, incoming spell-damage reduction by PB and their order for one minute. Preserve the later ten-minute prohibition on spending RP with exact actual-resource scope; do not silently extend it to Oracle RC or turn it into immunity to spells, free casting or waived material costs.",
    "Bind the actual Charisma-check advantage, psychic resistance and ten-minute duration; preserve +1 Unity Exposure on crash using only the already-reviewed public track if later authorized for the candidate. Keep repeated-use false-resonance/identity-loss language as an uninterpreted post-push receipt, with no added setting claims or invented penalties.",
    "Specify one chosen Arcana/History/Religion/Nature/Engineering research project, the +2 modifier and eight-hour window using actual work/check rules. Define the crash's concentration penalty trigger and finite ending while preserving player agency; do not grant free research progress or an indefinite compulsory action.",
    "Preserve water breathing and swim speed equal to current walking speed for one hour, with source-specific anatomy and component limits. Define the later eight-hour doubled actual water requirement through the expedition Supply conference, including overlap, consumption accounting and expiry; no automatic food or pressure conversion.",
    "Preserve fire resistance and +1 damage with melee attacks for ten minutes, with exact eligible attacks/packets and normal resistance/stacking. Define the later one-hour de-escalation-check disadvantage narrowly, without dictating behavior or applying it to every social check.",
    "Specify an actual available Hit Die spent and maximized immediately, applicable modifiers, healing caps/triggers, and one-hour suppression of Poisoned source records without pausing their timers. Preserve the dependence DC16 and vague develops quickly clause beside a proposed finite decision; do not remove dependence or create a die when none remains.",
    "Define ingestion versus the breath activation, one legal15-foot cone, chosen elemental-type vocabulary, save DC, half-damage rounding, entitlement expiry and1d6 same-type recoil. Locate the actual Mutation complication table for overdose; do not substitute Warrior mutations or invent its cosmological meaning from the shared word.",
]


def main():
    if OUT.exists():
        previous = json.loads(OUT.read_text(encoding='utf-8'))
        assert previous['submitted'] is False and previous['newRules'] == 0
    active = read(A / 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    assert all(sha(G / p) == h for p, h in active.items())
    core_path = R / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
    core = read(core_path)
    original_packet = read(A / 'CODEX_CONDITION_SOURCE_PACKET.json')
    assert core['brews'] == original_packet['brews']
    assert core['magical_substances'] == original_packet['magicalSubstances']
    assert len(core['brews']) == len(core['magical_substances']) == 12
    p = R / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx'
    protected[rel(p)] = sha(p)
    with ZipFile(p) as z: xml = z.read('word/document.xml'); root = ET.fromstring(xml)
    paragraphs = [''.join(t.text or '' for t in e.findall('.//w:t', NS)) for e in root.findall('.//w:p', NS)]
    start = paragraphs.index('37. Magical Substances and Dependence')
    end = next(i for i in range(start + 1, len(paragraphs)) if paragraphs[i].startswith('39. '))
    body = root.find('w:body', NS)
    tables = []
    for i, e in enumerate(body):
        if e.tag != f"{{{NS['w']}}}tbl": continue
        rows = [[[''.join(t.text or '' for t in p.findall('.//w:t', NS)) for p in c.findall('.//w:p', NS)]
                 for c in row.findall('w:tc', NS)] for row in e.findall('w:tr', NS)]
        flat = ['\n'.join(c) for row in rows for c in row]
        if any(name in flat for name in ['Quickglass', 'Gatehouse Small Beer', 'Repeated dose before long rest',
                'Medical emergency; gain a Wound or die without treatment at Director discretion.']):
            tables.append({'bodyElementIndex': i, 'rows': rows,
                           'xmlSha256': hashlib.sha256(ET.tostring(e)).hexdigest()})
    assert len(tables) == 4
    recipe_index = read(R / 'data/director/crafting_recipe_review_catalog.json')
    equipment = read(R / 'data/playtest/equipment_source_catalog.json')
    recipe_names = {x['name'].casefold(): x for x in recipe_index['recipes']}
    equipment_names = {x['name'].casefold(): x for x in equipment['records']}
    records = []
    for family, prefix, questions in [('brews', 'CB', BREW_QUESTIONS), ('magical_substances', 'CS', SUBSTANCE_QUESTIONS)]:
        for idx, (source, question) in enumerate(zip(core[family], questions)):
            found = [(t['bodyElementIndex'], j, row) for t in tables for j, row in enumerate(t['rows']) if row[0] == [source['name']]]
            assert len(found) == 1, source['name']
            table_id, row_id, row = found[0]
            value = ['\n'.join(c) for c in row]
            if family == 'brews':
                assert value == [source['name'], str(source['tier']), source['price'], source['effect']]
            else:
                assert value == [source['name'], source['effect'], source['crash'], str(source['dependence_dc']), source['legality'], f"{source['price_gp']} gp"]
            same_recipe = recipe_names.get(source['name'].casefold())
            same_equipment = equipment_names.get(source['name'].casefold())
            deferred = source['name'] in ['Ghostwine', 'Sovereign Reserve']
            partial_receipt = source['name'] in ['Choir Dust', 'Choirless Absinthe']
            records.append({'questionId': f'{prefix}-{idx+1:02}', 'family': family, 'sourceArrayIndex': idx,
                'name': source['name'], 'completeCoreJsonRecord': source,
                'currentBookBinding': {'bodyElementIndex': table_id, 'rowIndex': row_id, 'completeCellParagraphs': row,
                    'jsonSharedFieldsExactlyMatchBookRow': True},
                'question': question, 'status': 'source-only-post-push-receipt' if deferred else 'pre-push-source-question; no operational approval',
                'deferredMeaningReceipt': deferred or partial_receipt,
                'exactNameRecipeMatch': same_recipe, 'exactNameEquipmentMatch': same_equipment,
                'matchLimit': 'Exact case-insensitive display-name comparison only, not semantic equivalence or proof of independent identity.',
                'operational': None})
    guide_paths = [R / 'docs/mechanics' / n for n in ['CONDITION_RECOVERY_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
        'CORE_RESOLUTION_PLAYTEST.md', 'STRAIN_PLAYTEST.md', 'HEALING_DEATH_PLAYTEST.md', 'HEALING_PULSE_PLAYTEST.md',
        'EQUIPMENT_ITEM_PROCEDURES.md', 'EQUIPMENT_ACQUISITION_PLAYTEST.md', 'LANGUAGE_COMMUNICATION_PLAYTEST.md',
        'SPELL_INTEGRATION_RULES.md', 'BODY_EQUIPMENT_PLAYTEST.md']]
    guides = [{'file': rel(p), 'sha256': sha(p), 'exactText': raw(p)} for p in guide_paths]
    authorities = [A / 'GPT_CONDITIONS_FINAL_CLOSURE.md', A / 'GPT_CONDITIONS_EXACT_FINDINGS.md',
        A / 'GPT_CONDITIONS_SECOND_REVIEW.md', A / 'STRAIN_SOURCE_BINDINGS.json',
        A / 'LANGUAGE_EXACT_FULFILLMENT.json', R / 'docs/mechanics/LANGUAGE_REVIEW_STATUS.json',
        A / 'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json', A / 'POST_GITHUB_COSMOLOGY_REVIEW.md',
        A / 'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json', A / 'ENVIRONMENT_HAZARD_SOURCE_RECONNAISSANCE.json']
    for p in authorities: raw(p)
    result = {'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'Full24 source records prepared; UNSENT; no operational approval',
        'audience': 'internal source reconciliation; keep every source audience and scope',
        'sourceJsonFile': rel(core_path), 'sourceJsonSha256': sha(core_path),
        'bookFile': rel(R / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx'),
        'bookSha256': protected[rel(R / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx')],
        'bookXmlSha256': hashlib.sha256(xml).hexdigest(),
        'bookIndexConvention': 'zero-based all w:p including table cells; table bodyElementIndex uses direct body children; rowIndex includes header',
        'completeBookSections37And38': [{'paragraphIndex': i, 'exactText': paragraphs[i]} for i in range(start, end)],
        'selectedCompleteTables': tables, 'records': records, 'governingGuides': guides,
        'commonQuestion': 'For each pre-push record, settle actual serving/dose physical identity, lawful acquisition and source-price scope, use/target/ingestion, start/expiry, exact effect and all original clauses, stacking/reapplication/suppression/ending, crash, dependence/tolerance/overdose where applicable, save/check/DC, recovery and persistent record. Preserve source values and label each new finite choice NEW. Missing item-specific severe consequences cannot be filled by pretending generic recovery already approved the item. Keep two whole-record post-push receipts and other deferred meaning clauses unaltered.',
        'existingAuthority': ['Conditions final closure approves28 condition identities and generic recovery, explicitly excluding individual substances/items and hazards.',
            'Quickglass crash namespace already resolves to expedition Strain; do not reopen that binding.',
            'Completed687 recipe review covers the indexed recipes only; it is not approval of similarly functioning Core consumables.',
            'Reviewed ingestion, container, healing, temporaryHP, language and source-specific protection rules continue to govern their actual scopes.',
            'Ghostwine and Sovereign Reserve remain source-only post-push receipts. Deferred meaning in Choir Dust/Choirless Absinthe is not interpreted.'],
        'counts': {'brews': 12, 'substances': 12, 'identities': len(records), 'prePushQuestions': sum(r['status'].startswith('pre-push') for r in records),
            'wholeRecordPostPushReceipts': sum(r['status']=='source-only-post-push-receipt' for r in records),
            'bookParagraphs': end-start, 'completeTables': len(tables), 'bookBindings': len(records),
            'exactNameRecipeMatches': sum(r['exactNameRecipeMatch'] is not None for r in records),
            'exactNameEquipmentMatches': sum(r['exactNameEquipmentMatch'] is not None for r in records)},
        'originalConditionPacket24RecordsUnchanged': True, 'protectedFiles': protected,
        'scopeLimits': ['No cosmology, spirit taxonomy or protected-information interpretation.',
            'Record preparation does not settle any substantive question or adopt external-game defaults.',
            'This is the complete named24 Core set, not proof that every consumable elsewhere in the game is covered.',
            'No effect is promoted into the public playable catalog by source accounting.'],
        'newRules': 0, 'newApprovals': 0, 'runtimeImplemented': False, 'humanBalanceApproved': False,
        'submitted': False, 'cosmologyReviewed': False, 'sourceInformationDeleted': 0}
    assert len({x['questionId'] for x in records}) == len({x['name'] for x in records}) == 24
    assert all(sha(G / p) == h for p, h in protected.items())
    assert all(sha(G / p) == h for p, h in active.items())
    result['all342ActiveSpellInputsUnchanged'] = True
    dump(OUT, result)
    lines = ['# Core brews and magical substances —24 source records', '',
        '**Prepared and unsent. No new rules or operational approval.** [Full source records, book bindings and governing guides](CORE_CONSUMABLE_24_SOURCE_PREPARATION.json).', '',
        'Core contains12 named brews and12 magical substances. All24 exactly match their printed book rows for every shared field; '
        'the JSON descriptions and original strings are also preserved. The full two book sections and all four tables are retained. '
        'All24 source objects still equal the original condition-conference packet.', '',
        f"Exact name comparison with all687 crafting recipes and273 equipment rows finds {result['counts']['exactNameRecipeMatches']} recipe matches and "
        f"{result['counts']['exactNameEquipmentMatches']} equipment matches. This is name evidence, not proof of semantic independence.", '',
        'The reviewed generic condition/recovery chapter explicitly does not complete individual consumables. '
        'Quickglass already has a resolved expedition-Strain crash binding; retain it. '
        'The later language, healing and equipment rules provide relevant interfaces without filling every item-specific gap.', '',
        '**22 pre-push source questions and two whole-record post-push receipts.** Ghostwine and Sovereign Reserve retain their exact sources '
        'until the careful post-push review resolves their perception/terminal-record dependencies. '
        'Choir Dust and Choirless Absinthe retain their deferred-meaning clauses without new setting interpretation. '
        'Neither catalog selection nor price means the effects are playable or stock is available.', '',
        '| Case | Source name | Scope | Individual question |', '|---|---|---|---|']
    lines += [f"| {r['questionId']} | {r['name']} | {r['status']} | {r['question']} |" for r in records]
    lines += ['', '**Shared conference requirements:** actual dose/serving, source/price/procurement, ingestion and target legality, '
        'timing/expiry, all original effect clauses, stacking and repeated uses, crash and recovery, actual dependence/tolerance/overdose '
        'where applicable, exact checks/saves and persistent records. Label every new choice NEW. '
        'A generic severe complication placeholder is not an operational item.', '',
        'The full137-spell conference continues independently; all342 inputs remain unchanged. '
        'Confer on this complete source set before authoring, then submit actual complete candidates for exact review. '
        'Cosmology stays deferred until the authorized GitHub push and remote verification.', '']
    DOC.write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'counts': result['counts'], 'protectedInputs': len(protected), 'newRules': 0}, indent=2))


if __name__ == '__main__': main()
