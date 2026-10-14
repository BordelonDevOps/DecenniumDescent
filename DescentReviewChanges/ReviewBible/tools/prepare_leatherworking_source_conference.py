"""Prepare complete Leatherworking evidence while GPT continuation is pending."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from prepare_cooking_exact_review import common, delta, merge

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def write_new(path, text):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(text)


def dump_new(path, data):
    write_new(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    outputs = ['LEATHERWORKING_INTERFACE_EVIDENCE.json', 'CODEX_LEATHERWORKING_SOURCE_CONFERENCE.txt',
               'LEATHERWORKING_SOURCE_CONFERENCE_STATUS.json', 'LEATHERWORKING_REVIEW_BASELINE.json']
    assert not any((AUDIT / f).exists() for f in outputs), 'Existing preparation must be inspected, not overwritten.'
    source_path = ROOT / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    book_path = GAME / 'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    evidence = read(AUDIT / 'LEATHERWORKING_SOURCE_PREPARATION.json')
    actual = read(source_path)
    recipes = [r for r in actual['recipes'] if r['skill'] == 'Leatherworking']
    checks = {}
    checks['all44FullOriginalsEqualPreparedEvidence'] = recipes == evidence['recipes'] and len(recipes) == 44
    checks['sourceAndBookHashesUnchanged'] = sha(source_path) == evidence['sourceSha256'] and sha(book_path) == evidence['bookSha256']
    base = common(recipes)
    overrides = {r['id']: delta(r, base) for r in recipes}
    checks['all44FactoredSourceRecordsReconstructExactly'] = all(merge(base, overrides[r['id']]) == r for r in recipes)
    checks['all44SourceIndicesExact'] = all(actual['recipes'][evidence['sourceIndices'][r['id']]] == r for r in recipes)
    with zipfile.ZipFile(book_path) as archive:
        doc = ET.fromstring(archive.read('word/document.xml'))
    word = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    paragraphs = [''.join(t.text or '' for t in p.iter(word + 't')) for p in doc.iter(word + 'p')]
    bindings = evidence['publicBookBindings']
    checks['all30PublicBookBindingsMatchActualParagraphs'] = len(bindings) == 30 and all(
        paragraphs[p['index']] == p['text'] for b in bindings for p in b['paragraphs'])
    checks['exactPublicRecipeSetInBook'] = {b['recipeId'] for b in bindings} == {r['id'] for r in recipes if r['visibility'] == 'public'}
    checks['noRestrictedOrDirectorFormulaInPublicBook'] = all(
        not any(p.startswith('Formula ID: ' + r['id'] + ' ') for p in paragraphs)
        for r in recipes if r['visibility'] != 'public')
    checks['visibility30_1_13'] = Counter(r['visibility'] for r in recipes) == {'public': 30, 'restricted': 1, 'director-only': 13}

    variants = {
        'mechanicalV4': source_path,
        'internalV4': GAME / 'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json',
        'v2': GAME / 'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json',
        'publicRuntime': GAME / 'src/data/crafting-recipes.json',
    }
    variant_rows = {}
    for name, path in variants.items():
        data = read(path)
        variant_rows[name] = {r['id']: r for r in (data if isinstance(data, list) else data['recipes'])}
    armor_conflicts = []
    for recipe in recipes:
        if recipe['mechanics'].get('armorBonus', 0) == 0:
            continue
        supplied = {}
        for name, rows in variant_rows.items():
            if recipe['id'] in rows:
                r = rows[recipe['id']]
                supplied[name] = {'armorBonus': r['mechanics']['armorBonus'], 'effect': r['effects']}
        book = next((b for b in bindings if b['recipeId'] == recipe['id']), None)
        armor_conflicts.append({'recipeId': recipe['id'], 'name': recipe['name'], 'visibility': recipe['visibility'],
                               'sourceVariants': supplied, 'publicBookEffect': None if book is None else book['paragraphs'][1],
                               'decision': 'unresolved; original fields retained'})
    checks['elevenUnprintedArmorFieldsConfirmedAcrossVersions'] = len(armor_conflicts) == 11 and all(
        len({(v['armorBonus'], v['effect']) for v in r['sourceVariants'].values()}) == 1
        and not re.search(r'\bAC\b|armor class', next(iter(r['sourceVariants'].values()))['effect'], re.I)
        for r in armor_conflicts)
    checks['twoPublicArmorConflictsBoundToBookAndRuntime'] = {
        r['recipeId'] for r in armor_conflicts if r['visibility'] == 'public'} == {'recipe-308', 'recipe-653'} and all(
        'publicRuntime' in r['sourceVariants'] and r['publicBookEffect'] is not None
        for r in armor_conflicts if r['visibility'] == 'public')
    components = [c for r in recipes for c in r['components']]
    checks['all201ComponentsConsumedWithNoCatalystOrToolRole'] = len(components) == 201 and all(
        c['consumed'] and c['role'] not in ('tool', 'catalyst') for c in components)
    checks['allFieldFlagsFalse'] = all(r['workRequirements']['fieldCraftable'] is False for r in recipes)
    checks['only319HasNullSourceWorkHours'] = [r['id'] for r in recipes if r['workRequirements']['activeWorkHours'] is None] == ['recipe-319']
    checks['sevenPrintedWearableResistances'] = sum(bool(r['mechanics'].get('resistance')) for r in recipes) == 7
    checks['recipe653HasNoSourceResistance'] = next(r for r in recipes if r['id'] == 'recipe-653')['mechanics']['resistance'] is None

    equipment_path = ROOT / 'data/playtest/equipment_acquisition_candidate.json'
    equipment = read(equipment_path)
    selected = [r for r in equipment['items'] if re.search(
        r'leather|hide|padded|backpack|pouch|quiver|belt|glove|boot|coat|harness|clothes|sack|chest|barrel|basket|blanket|waterskin|rope|climber|arrows|bolts|case, crossbow bolt|glass vial|crystal vial|potion case|block and tackle|^lock$', r['name'], re.I)]
    present_names = {r['name'].casefold() for r in equipment['items']}
    missing = [n for n in ['Boots', 'Gloves', 'Leather Gear', 'Belt', 'Harness', 'Coat'] if n.casefold() not in present_names]
    checks['sixNamedStandaloneBodiesAbsentFrom220ItemCatalog'] = len(equipment['items']) == 220 and len(missing) == 6

    guide_paths = ['docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md', 'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',
                   'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md', 'docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md',
                   'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md', 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md']
    guide_texts = {p: (ROOT / p).read_text(encoding='utf-8') for p in guide_paths}
    protected = dict(read(AUDIT / 'BLACKSMITHING_REVIEW_BASELINE.json')['files'])
    checks['existing32FileBaselineUnchangedBeforeExtension'] = all(sha(GAME / p) == h for p, h in protected.items())
    assert checks['existing32FileBaselineUnchangedBeforeExtension']
    for path in [*variants.values(), book_path, equipment_path, *(ROOT / p for p in guide_paths), AUDIT / 'LEATHERWORKING_SOURCE_PREPARATION.json']:
        protected[path.relative_to(GAME).as_posix()] = sha(path)
    black = read(AUDIT / 'BLACKSMITHING_EXACT_SUBMISSION.json')
    checks['protectedFilesMatchExistingBaseline'] = all(sha(GAME / p) == h for p, h in protected.items())
    checks['pendingBlacksmithArtifactsStillMatchSubmission'] = all(sha(GAME / p) == h for p, h in black['artifactHashes'].items())
    pending_guide = ROOT / 'docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md'
    current = read(ROOT / 'data/director/crafting_recipe_review_catalog.json')['totals']
    interface = {'status': 'source evidence only; no Leatherworking decisions approved',
                 'sourceHashes': {str(p.relative_to(GAME)).replace('\\', '/'): sha(p) for p in variants.values()},
                 'equipmentSource': equipment_path.relative_to(GAME).as_posix(), 'equipmentSha256': sha(equipment_path),
                 'completeEquipmentRecords': selected, 'missingStandaloneProfiles': missing,
                 'armorFieldConflicts': armor_conflicts, 'recipeFamilyCounts': dict(Counter(r['recipeFamily'] for r in recipes)),
                 'componentRoleCounts': dict(Counter(c['role'] for c in components)),
                 'fieldModeWithFalseFlag': [r['id'] for r in recipes if r['workRequirements']['timeMode'] == 'field'],
                 'resistanceRecipes': [r['id'] for r in recipes if r['mechanics'].get('resistance')],
                 'reviewedGuideHashes': {p: sha(ROOT / p) for p in guide_paths},
                 'pendingBlacksmithGuide': {'path': pending_guide.relative_to(GAME).as_posix(), 'sha256': sha(pending_guide),
                                          'exactVerdict': 'not yet retrieved; do not treat as reviewed'},
                 'checks': checks}
    assert all(checks.values()), checks
    blocks = [(AUDIT / 'LEATHERWORKING_SOURCE_QUESTIONS.md').read_text(encoding='utf-8'),
              '\nCOMPLETE SOURCE RECORDS — COMMON plus recursive per-recipe overrides, arrays replace whole arrays\n',
              compact({'sourceSha256': evidence['sourceSha256'], 'bookSha256': evidence['bookSha256'],
                       'sourceIndices': evidence['sourceIndices'], 'COMMON': base, 'recipeOverrides': overrides}),
              '\nEXACT PUBLIC V5 PARAGRAPHS AND STRUCTURAL SOURCE AUDIT\n',
              compact({k: evidence[k] for k in ['counts', 'effectTypes', 'publicBookBindings', 'structuralAudit']}),
              '\nCOMPLETE SELECTED EQUIPMENT RECORDS AND EXPLICIT SOURCE CONFLICTS\n', compact(interface)]
    for path, text in guide_texts.items():
        blocks.extend(['\nEXISTING REVIEWED GUIDE: ' + path + '\n', text])
    blocks += ['\nPENDING BLACKSMITHING GUIDE — DRAFT, NO COMPLETED EXACT VERDICT\n', pending_guide.read_text(encoding='utf-8'),
               '\nUNRESOLVED CONCRETE REVIEW SCENARIOS\n', (AUDIT / 'LEATHERWORKING_REVIEW_SCENARIOS.md').read_text(encoding='utf-8')]
    packet = '\n'.join(blocks)
    assert all(sha(GAME / p) == h for p, h in protected.items()), 'An input changed during preparation.'
    dump_new(AUDIT / outputs[0], interface)
    write_new(AUDIT / outputs[1], packet)
    dump_new(AUDIT / outputs[3], {'scope': 'Original sources and reviewed interfaces; pending Blacksmithing artifacts separately identified.',
                                'files': protected, 'pendingBlacksmithDependencyFiles': black['artifactHashes']})
    status = {'status': 'prepared-not-sent; GPT continuation authorization and Blacksmithing exact verdict pending',
              'recipes': 44, 'publicBookMatches': 30, 'sourceReconstructions': 44, 'equipmentRecords': len(selected),
              'sourceArmorConflicts': 11, 'reviewScenarios': 20, 'checks': checks,
              'packetCharacters': len(packet), 'packetSha256': sha(AUDIT / outputs[1]),
              'protectedFiles': len(protected), 'pendingBlacksmithFiles': len(black['artifactHashes']),
              'recipesApproved': 0, 'currentRecipePassTotals': current, 'sourceOriginalsUnchanged': True,
              'cosmology': 'post-push only',
              'resume': 'Obtain owner authorization for the new GPT review chat and actual Blacksmithing verdict; supply updated cover/status before sending this preserved preparation. No send performed.'}
    dump_new(AUDIT / outputs[2], status)
    print(compact({k: status[k] for k in ['status', 'recipes', 'publicBookMatches', 'sourceReconstructions',
                                        'equipmentRecords', 'sourceArmorConflicts', 'reviewScenarios', 'packetCharacters', 'protectedFiles']}))
    print('Validation checks:', len(checks))


if __name__ == '__main__':
    main()
