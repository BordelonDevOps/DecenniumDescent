"""Collect bounded environment interfaces without inventing or approving rules.

Read-only for all source material. Output is an unsent source reconnaissance,
not a complete operational hazard chapter or a cosmology interpretation.
"""
from pathlib import Path
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib, json, re

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'ENVIRONMENT_HAZARD_SOURCE_RECONNAISSANCE.json'
DOC = A / 'ENVIRONMENT_HAZARD_SOURCE_RECONNAISSANCE.md'
PATTERN = re.compile(
    r'suffocat|drown|extreme (?:heat|cold)|environmental (?:hazard|fatigue|penalt|adapt)'
    r'|\bweather\b|quicksand|low oxygen|poisonous atmosphere|high altitude'
    r'|respirat|breath(?:e|ing) (?:air|water)|hold (?:its|your|their) breath'
    r'|cold-weather exposure', re.I)
BOOK_PATTERN = re.compile(r'suffocat|drown|extreme (?:heat|cold)|environmental hazard|\bweather\b|quicksand', re.I)
protected = {}


def rel(p): return p.relative_to(G).as_posix()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def remember(p): protected[rel(p)] = sha(p); return p
def read(p): return json.loads(remember(p).read_text(encoding='utf-8-sig'))
def dump(p, data): p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


CASES = [
    ('HZ-01', 'Exposure clocks and authority', 'Define one actual timeline for short exposure, combat rounds, exploration turns and Watches. Reuse current rest and expedition clocks; do not create free resets or double-charge the same exposure. Separate ordinary environmental hazards from each source-specific supernatural effect.'),
    ('HZ-02', 'Breathing and suffocation', 'Locate or author the baseline for holding breath, loss of breathable air, interrupted rescue and suffocation, with finite timing, checks, damage/state changes and recovery. Preserve actual anatomy and water-breathing permissions; neither damage resistance nor generic immunity to a condition supplies breathable air.'),
    ('HZ-03', 'Heat and cold exposure', 'Define the referenced extreme-heat/cold thresholds, exposure interval, exact saves and outcomes, shelter/equipment eligibility and recovery. Core brew Stoneback Stout says to ignore the first level of cold-weather exposure for four hours. Preserve that complete consumable source; do not assume that a completed recipe review approved this separate brew or defined an exposure scale.'),
    ('HZ-04', 'Open flames and ongoing fire', 'Separate entering/remaining in an actual fire from an effect that explicitly applies Burning. Bind ignition, damage frequency, extinguishing, full immersion, immunity, suppression and multiple records to the reviewed ongoing-fire family; do not apply a second generic tick for one event.'),
    ('HZ-05', 'Smoke, gases and visibility', 'Specify actual visibility, inhalation and breathable-air consequences separately. Define geometry, ventilation, dissipating and moving volumes where needed; obey actual sight/targeting rules and source-specific gas counters. A dispersed ordinary smoke cube does not create continuing air or end a magical cloud.'),
    ('HZ-06', 'Water, currents and rescue', 'Connect movement, swimming, carrying, currents, submersion and rescue to the breathing baseline. Keep water breathing distinct from swim speed, depth/temperature protection and freedom of movement. Ending a form or spell restores actual anatomy at the current location without free relocation.'),
    ('HZ-07', 'Weather and forecasts', 'Give Directors a usable record of actual temperature, precipitation, wind and visibility. Preserve Detect Weather accuracy and its actual later-cause exception; class weather moderation and winter invocations retain their bounded scope. Do not add planar, seasonal or decennial setting interpretation.'),
    ('HZ-08', 'Environmental poison', 'Define exposure routes, dose identity, timing, save/outcome, persistence and countermeasures for each actual hazard. Keep poison damage, Poisoned and suffocation independent; route reviewed poisoncrafting delivery and cure rules without reopening completed recipe effects or granting blanket immunity.'),
    ('HZ-09', 'Disease and contagion', 'Identify actual supported disease sources and give each transmission route, onset, checks, progression, treatment and ending. Bind creature disease features to the pending bestiary source conference; do not infer a universal disease from a flavor label or turn one cure into future immunity.'),
    ('HZ-10', 'Corrosive and unstable terrain', 'Define finite procedures for actual acids, unstable ground, entrapment and similar supported hazards. Preserve object versus creature targeting, damage-type scope, structural HP and existing gear identity. Director severity advice alone does not specify complete damage or a permanent equipment-loss rule.'),
    ('HZ-11', 'Traps and finite failure', 'Use the Director manual clue/disarm guidance and reviewed device/recipe procedures. Supply concrete detection, interaction, trigger, target geometry, outcome, reset and disarm records; settle failure costs before the roll and preserve alternate routes. Do not convert suggested setbacks into automatic permanent losses.'),
    ('HZ-12', 'Falls and forced movement', 'Use the already-reviewed falling/geometry/movement procedure for actual height, rescue opportunities, flight loss and landing. Establish only missing environmental trigger interfaces; do not recreate or contradict the existing fall calculation or invent collision damage from forced movement alone.'),
    ('HZ-13', 'Actual protection and scope', 'Map each actual ancestry/class/spell/item protection to the precise hazard predicate it changes. Distinguish advantage, resistance, ignored ordinary penalties, immunity and shelter; preserve forms, worn/functional/melded equipment and shared modifier families. Pending ordinary spells remain pending.'),
    ('HZ-14', 'Recovery and worked expedition cases', 'Create complete cases for ongoing exposure interrupted by rest, shelter, rescue, transformation, treatment and a Watch boundary. Carry actual consumed supplies, doses, conditions and damage forward once; defer Supply conversion and expedition scheduling choices to their existing conference rather than choosing conflicting defaults.'),
]


def main():
    if OUT.exists():
        previous = json.loads(OUT.read_text(encoding='utf-8'))
        assert previous['submitted'] is False and previous['newRules'] == 0
    active = read(A / 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    assert all(sha(G / p) == h for p, h in active.items())
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    books = []
    for name in ['Decennium_Descent_Player_Rulebook_v6.docx', 'Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx']:
        p = remember(R / 'books/player' / name)
        with ZipFile(p) as z: root = ET.fromstring(z.read('word/document.xml'))
        paragraphs = [''.join(t.text or '' for t in e.findall('.//w:t', ns)) for e in root.findall('.//w:p', ns)]
        matches = [{'paragraphIndex': i, 'text': s} for i, s in enumerate(paragraphs) if BOOK_PATTERN.search(s)]
        # A catalogue tier-summary mention is not an environmental procedure;
        # keep its location as an uninterpreted receipt, not an authoring source.
        receipts = [x for x in matches if 'planar travel' in x['text']]
        matches = [x for x in matches if x not in receipts]
        if name.endswith('Known_Descent.docx'):
            matches += [{'paragraphIndex': i, 'text': s} for i, s in enumerate(paragraphs)
                        if 'cold-weather exposure' in s and not BOOK_PATTERN.search(s)]
        books.append({'file': rel(p), 'sha256': sha(p), 'indexConvention': 'zero-based all w:p including table cells',
                      'paragraphCount': len(paragraphs), 'literalMatches': matches,
                      'uninterpretedReceiptLocations': [x['paragraphIndex'] for x in receipts],
                      'negativeSearch': {term: not any(re.search(term, s, re.I) for s in paragraphs) for term in ['suffocat', 'drown']},
                      'scope': 'Literal reconnaissance only. Absence of these strings is not proof that no equivalent rule exists elsewhere.'})

    director = read(A / 'DIRECTOR_TABLECRAFT_SOURCE_PREPARATION.json')
    dr10 = next(x for x in director['cases'] if x['id'] == 'DR-10')
    block_ids = set(dr10['sourceBodyElements'])
    director_blocks = [x for x in director['sourceBlocks'] if x['bodyElementIndex'] in block_ids]
    assert len(director_blocks) == len(block_ids)
    classes = []
    for p in sorted((R / 'data/public/class_playtests').glob('*.json')):
        if p.name == 'manifest.json': continue
        d = read(p)
        for card in d['cards']:
            # Only the operational name/effect select a record. Full selected
            # records are preserved, including their historical source fields.
            if PATTERN.search(str(card.get('name', '')) + '\n' + str(card.get('effect', ''))):
                classes.append({'file': rel(p), 'class': d['class'], 'record': card})
    catalog = read(R / 'data/public/spell_playtests/catalog.json')
    spells = [s for s in catalog['spells'] if PATTERN.search(json.dumps({k: s[k] for k in ['name', 'operational', 'source']}, ensure_ascii=False))]
    ancestry_spells = read(R / 'data/playtest/ancestry_spell_supplement_candidate.json')
    ancestry_spell_records = [s for s in ancestry_spells['spells'] if PATTERN.search(json.dumps(s, ensure_ascii=False))]
    ancestry = read(R / 'data/playtest/ancestry_background_candidate.json')
    ancestry_records = [s for s in ancestry['ancestries'] if PATTERN.search(json.dumps(s, ensure_ascii=False))]
    core_path = R / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
    core = read(core_path)
    brews = [{'file': rel(core_path), 'record': b, 'sourceOnly': True} for b in core['brews']
             if PATTERN.search(json.dumps(b, ensure_ascii=False))]
    recipe_paths = sorted((R / 'data/playtest').glob('*_recipe_candidate.json')) + sorted((R / 'data/crafting').glob('*_recipe_candidate_public.json'))
    recipes = []
    for p in recipe_paths:
        d = read(p)
        for card in d['cards']:
            if PATTERN.search(json.dumps(card, ensure_ascii=False)):
                recipes.append({'file': rel(p), 'record': card, 'envelopeStatus': d.get('status'),
                                'exactRecipeApproval': d.get('exactRecipeApproval'),
                                'sourceSelectionOnly': True})
    guide_names = ['CORE_RESOLUTION_PLAYTEST.md', 'COMBAT_ACTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                   'CUSTOM_CONDITION_BINDINGS.md', 'HEALING_DEATH_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md',
                   'CREATURE_LIFECYCLE_PLAYTEST.md', 'EQUIPMENT_ITEM_PROCEDURES.md', 'ANCESTRY_BACKGROUND_PLAYTEST.md',
                   'SPELL_INTEGRATION_RULES.md', 'POISONCRAFTING_RECIPE_PLAYTEST.md']
    guides = []
    guide_pattern = re.compile(PATTERN.pattern + r'|ongoing.fire|extinguish|\bBurning\b|\bPoisoned\b|\bdisease\b', re.I)
    for name in guide_names:
        p = remember(R / 'docs/mechanics' / name)
        lines = p.read_text(encoding='utf-8-sig').splitlines()
        matches = [{'line': i + 1, 'exactText': s} for i, s in enumerate(lines) if guide_pattern.search(s)]
        guides.append({'file': rel(p), 'sha256': sha(p), 'matchedLines': matches,
                       'scope': 'Discovery references. Read each whole governing section before interpreting or changing an interface.'})
    counts = {'bookMatches': sum(len(x['literalMatches']) for x in books), 'directorBlocks': len(director_blocks),
              'completeClassCards': len(classes), 'completeOrdinarySpellRecords': len(spells),
              'completeAncestrySpellRecords': len(ancestry_spell_records), 'completeAncestryRecords': len(ancestry_records),
              'completePublicRecipeCards': len(recipes), 'completeCoreBrewSources': len(brews), 'governingGuides': len(guides), 'questions': len(CASES)}
    result = {'status': 'Bounded source reconnaissance; UNSENT; no new rules or approval',
              'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'coverageArea': 'DD-22',
              'selectionPatterns': {'books': BOOK_PATTERN.pattern, 'interfaces': PATTERN.pattern},
              'books': books, 'directorExistingCase': dr10, 'directorBlocks': director_blocks,
              'directorOriginalPath': director['sourceFile'], 'directorOriginalSha256': director['sourceSha256'],
              'classCards': classes, 'ordinarySpellRecords': spells, 'ancestrySpellRecords': ancestry_spell_records,
              'ancestryRecords': ancestry_records, 'publicRecipeCards': recipes, 'coreBrewSources': brews, 'governingGuideReferences': guides,
              'questions': [{'id': i, 'title': title, 'question': q, 'status': 'open; no choice made'} for i, title, q in CASES],
              'existingConferences': {'Director': 'DIRECTOR_TABLECRAFT_SOURCE_PREPARATION.json#DR-10',
                  'expedition': 'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json', 'bestiary': 'BESTIARY_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json',
                  'activeSpells': 'LOW_RANK_SPELLS_V3_SUBMISSION.json'},
              'scopeLimits': ['Not an exhaustive search of every original, historical snapshot or equivalent terminology.',
                  'Complete selected records are discovery evidence; exact statuses and permissions are retained, not newly promoted.',
                  'No claims that numbered thresholds absent from literal searches have no source anywhere.',
                  'Director timing and place references are preserved as existing procedural text; no cosmology interpretation.',
                  'Before dispatch, reconcile final spell decisions, whole governing sections and actual environmental source records.'],
              'revisionNotes': ['The cold-exposure wording was traced to Core brew Stoneback Stout, not assumed to be an approved crafting recipe. Full brew record added; no operational effect chosen.'],
              'counts': counts, 'protectedFiles': protected, 'newRules': 0, 'newApprovals': 0,
              'sourceInformationDeleted': 0, 'submitted': False, 'runtimeChanged': False, 'cosmologyReviewed': False}
    assert all(sha(G / p) == h for p, h in protected.items())
    assert all(sha(G / p) == h for p, h in active.items())
    result['all342ActiveSpellInputsUnchanged'] = True
    dump(OUT, result)
    lines = ['# Environmental hazards — source reconnaissance', '',
        '**Prepared, unsent; no new rules or approval.** This fills a source-discovery gap for DD-22. '
        'It links existing protections and procedures to the underlying hazard decisions they need.', '',
        '[Full selected records, exact excerpts and source hashes](ENVIRONMENT_HAZARD_SOURCE_RECONNAISSANCE.json)', '',
        f"The bounded inventory retains {counts['bookMatches']} literal book paragraphs, {counts['directorBlocks']} already-selected Director blocks, "
        f"{counts['completeClassCards']} complete class cards, {counts['completeOrdinarySpellRecords']} ordinary spell records, "
        f"{counts['completeAncestrySpellRecords']} ancestry spell records, {counts['completeAncestryRecords']} ancestry records and "
        f"{counts['completePublicRecipeCards']} public recipe cards and {counts['completeCoreBrewSources']} Core brew source. Their source statuses remain unchanged. Eleven governing guides are linked with exact matching lines.", '',
        'The two selected Player/Core books have no literal matches for `suffocat` or `drown`. '
        'That is a bounded search result, not proof that an equivalent rule is absent everywhere. '
        'Core brew **Stoneback Stout** (Tier2,1sp) references ignoring the first level of cold-weather exposure for four hours. '
        'Its complete source record is retained separately. The completed crafting-recipe review does not automatically approve this brew or define an exposure scale.', '',
        'Director case DR-10 already covers hazard clues, difficulty and finite failure but was not linked to DD-22. '
        'This inventory reuses that preserved source; it does not reopen or replace the Director, expedition or bestiary conferences. '
        'Use existing reviewed fire/condition/fall/body rules in their actual scopes. Pending ordinary spells remain pending.', '',
        '| Case | Topic | Decision still needed |', '|---|---|---|']
    lines += [f'| {i} | {title} | {q} |' for i, title, q in CASES]
    lines += ['', 'Before a full source conference, read whole governing sections and reconcile the final spell decisions with actual hazard sources. '
              'These literal selectors do not claim complete semantic coverage. No original was changed, and all342 active spell-packet inputs remain unchanged. '
              'Cosmology remains deferred until after the authorized GitHub push and remote verification.', '']
    DOC.write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'counts': counts, 'protectedFiles': len(protected), 'activeSpellInputsUnchanged': len(active), 'newRules': 0}, indent=2))


if __name__ == '__main__': main()
