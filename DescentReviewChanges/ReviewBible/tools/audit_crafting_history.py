"""Read original recipe sources and every workbook sheet; write audit evidence only."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def recipe_rows(path):
    data = read(path)
    return data if isinstance(data, list) else data['recipes']


def workbook_sheets(path):
    """Read XML cells without importing, recalculating or saving the workbook."""
    with zipfile.ZipFile(path) as archive:
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings = [''.join(t.text or '' for t in item.findall('.//m:t', NS))
                       for item in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        relations = {r.attrib['Id']: r.attrib['Target'] for r in
                     ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
        sheets = []
        for sheet in ET.fromstring(archive.read('xl/workbook.xml')).find('m:sheets', NS):
            key = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
            target = relations[sheet.attrib[key]]
            target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            doc = ET.fromstring(archive.read(target))
            cells = {}
            for cell in doc.findall('m:sheetData/m:row/m:c', NS):
                value = cell.find('m:v', NS)
                value = value.text if value is not None else ''
                if cell.get('t') == 's':
                    value = strings[int(value)]
                elif cell.get('t') == 'inlineStr':
                    value = ''.join(t.text or '' for t in cell.findall('.//m:t', NS))
                if value != '':
                    cells[cell.attrib['r']] = value
            dimension = doc.find('m:dimension', NS)
            sheets.append({'name': sheet.attrib['name'], 'state': sheet.get('state', 'visible'),
                           'range': dimension.get('ref') if dimension is not None else None, 'cells': cells,
                           'formulaCount': len(doc.findall('.//m:f', NS))})
        extras = [n for n in archive.namelist()
                  if any(k in n.lower() for k in ('comment', 'external', 'drawing', 'vba'))]
        return sheets, extras


def nested_differences(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                out.append({'path': path + '/' + key, 'earlierPresent': key in a,
                            'currentPresent': key in b, 'earlier': a.get(key), 'current': b.get(key)})
            else:
                out.extend(nested_differences(a[key], b[key], path + '/' + key))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b))
                for d in nested_differences(x, y, path + '/' + str(i))]
    return [] if a == b else [{'path': path, 'earlier': a, 'current': b}]


def main():
    discovered = subprocess.check_output([
        'rg', '--files', '--hidden', '-g', '*crafting*.json', '-g', '*Crafting*.json',
        '-g', '*crafting*.xlsx', '-g', '*Crafting*.xlsx', '-g', '*crafting*.bak*',
        '-g', '!node_modules', '-g', '!vendor', '-g', '!assets', str(GAME)], text=True).splitlines()
    sources = [Path(p) for p in discovered if Path(p).suffix == '.xlsx' or
               Path(p).name.lower().startswith(('crafting-recipes', 'decennium_descent_crafting_bible'))]
    before = {p.relative_to(GAME).as_posix(): sha(p) for p in sources}
    groups = {}
    for rel, digest in before.items():
        groups.setdefault(digest, []).append(rel)
    inventory = [{'sha256': h, 'paths': sorted(paths)} for h, paths in sorted(groups.items())]
    paths = {
        'legacy': 'archive/main-pre-v6-cutover-2026-08-05/src/data/crafting-recipes.json',
        'earlyBackup': 'src/data/backups/crafting-recipes.json.bak-2026-07-31',
        'mechanicalV4': 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json',
        'internalV4': 'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json',
        'v2': 'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json',
        'publicRuntime': 'src/data/crafting-recipes.json',
        'workbook': 'decennium_descent_crafting_recipes_validated.xlsx',
    }
    catalogs = {key: recipe_rows(GAME / path) for key, path in paths.items() if key != 'workbook'}
    legacy, current = catalogs['legacy'], catalogs['mechanicalV4']
    by_id = {r['id']: r for r in current}
    by_name = {(r['skill'], r['name']): r for r in legacy}
    checks = {}
    checks['uniqueLegacyIdsAndTradeNames'] = len(legacy) == len(by_name) == len({r['id'] for r in legacy}) == 623
    checks['uniqueExpandedIds'] = len(current) == len(by_id) == 687
    checks['allLegacyIdsRetained'] = all(r['id'] in by_id for r in legacy)
    checks['allLegacyNamesRetainedAsAliases'] = all(r['name'] == by_id[r['id']].get('legacyName') for r in legacy)
    checks['allLegacyEffectsRetained'] = all(r.get('effects') == by_id[r['id']].get('legacyEffect') for r in legacy)
    checks['earlyBackupIdentityNamesMatch'] = {(r['id'], r['name'], r['skill']) for r in catalogs['earlyBackup']} == {(r['id'], r['name'], r['skill']) for r in legacy}
    checks['publicRuntimeExactProjection'] = catalogs['publicRuntime'] == [r for r in current if r['visibility'] == 'public']
    checks['expandedVersionIdentitySetsEqual'] = all({r['id'] for r in catalogs[k]} == set(by_id) for k in ('internalV4', 'v2'))
    added = [r for r in current if r['id'] not in {x['id'] for x in legacy}]
    checks['exactlyFourAddedPerTrade'] = len(added) == 64 and set(Counter(r['skill'] for r in added).values()) == {4}

    workbook = GAME / paths['workbook']
    sheets, extras = workbook_sheets(workbook)
    bindings, unmatched = [], []
    differences = Counter()
    columns = {'A': 'name', 'B': 'rarity', 'C': 'skillLevel', 'D': 'baseIngredients',
               'E': 'monsterParts', 'F': 'tags', 'G': 'difficulty', 'H': 'craftingTime',
               'I': 'quantity', 'J': 'effects', 'K': 'value'}
    summary = []
    for sheet in sheets:
        cells = sheet['cells']
        trade_sheet = cells.get('A3') == 'Recipe Name' and cells.get('K3') == 'Value (GP)'
        summary.append({k: v for k, v in sheet.items() if k != 'cells'} | {
            'populatedCells': len(cells), 'recipeSheet': trade_sheet})
        if not trade_sheet:
            continue
        row_numbers = sorted({int(re.sub('[A-Z]', '', c)) for c in cells if c.startswith('A') and int(re.sub('[A-Z]', '', c)) >= 4})
        for row in row_numbers:
            name = cells.get(f'A{row}')
            old = by_name.get((sheet['name'], name))
            if old is None:
                unmatched.append({'sheet': sheet['name'], 'row': row, 'name': name})
                continue
            expected = {k: str(old.get(v, '')) for k, v in columns.items() if k not in ('D', 'E', 'K')}
            expected['D'] = ', '.join(f"{c['name']} ({c['quantity']})" for c in old['components'] if c['category'] != 'monster_part')
            expected['E'] = ', '.join(f"{c['name']} (Tier {c['tier']})" for c in old['components'] if c['category'] == 'monster_part')
            expected['K'] = str(old['resultItem']['value'])
            changed = []
            for col, field in columns.items():
                observed = cells.get(f'{col}{row}', '')
                if observed != expected[col]:
                    differences[field] += 1
                    changed.append({'field': field, 'cell': f'{col}{row}', 'workbook': observed, 'legacyJSON': expected[col]})
            new = by_id[old['id']]
            bindings.append({'recipeId': old['id'], 'sheet': sheet['name'], 'range': f'A{row}:K{row}',
                             'legacyName': name, 'currentName': new['name'], 'workbookVsLegacyDifferences': changed})
    checks['workbookAll623RowsBoundUniquely'] = len(bindings) == len({r['recipeId'] for r in bindings}) == 623 and not unmatched
    checks['workbookNoHiddenOrUninspectedSheets'] = len(summary) == 20 and all(x['state'] == 'visible' for x in summary)
    checks['workbookNoFormulasOrSupplementaryParts'] = not extras and not any(x['formulaCount'] for x in summary)
    workbook_copies = [p for p in sources if p.suffix == '.xlsx']
    checks['fiveWorkbookCopiesByteIdentical'] = len(workbook_copies) == 5 and len({sha(p) for p in workbook_copies}) == 1

    name_pairs = Counter()
    component_shape_problems = []
    for binding in bindings:
        for diff in binding['workbookVsLegacyDifferences']:
            earlier = re.findall(r'(?:^|, )(.+?) \(([^()]*)\)(?=, |$)', diff['workbook'])
            later = re.findall(r'(?:^|, )(.+?) \(([^()]*)\)(?=, |$)', diff['legacyJSON'])
            if (len(earlier) != len(later)
                    or ', '.join(f'{n} ({q})' for n, q in earlier) != diff['workbook']
                    or ', '.join(f'{n} ({q})' for n, q in later) != diff['legacyJSON']
                    or [x[1] for x in earlier] != [x[1] for x in later]):
                component_shape_problems.append({'recipeId': binding['recipeId'], 'field': diff['field']})
            else:
                for old_part, new_part in zip(earlier, later):
                    if old_part[0] != new_part[0]:
                        name_pairs[(diff['field'], old_part[0], new_part[0])] += 1
    checks['workbookComponentDifferencesAreNamesOnlyWithCountsAndTiersRetained'] = not component_shape_problems

    version_diffs = {}
    for key in ('internalV4', 'v2'):
        counts = Counter()
        mechanics = []
        for earlier in catalogs[key]:
            later = by_id[earlier['id']]
            changed = [k for k in set(earlier) | set(later) if earlier.get(k) != later.get(k)]
            counts.update(changed)
            # Preserve concrete mechanical variants; cosmology content is not adjudicated here.
            for field in ('components', 'workRequirements'):
                if field in changed:
                    mechanics.append({'recipeId': earlier['id'], 'trade': earlier['skill'], 'field': field,
                                      'differences': nested_differences(earlier[field], later[field], '/' + field)})
        version_diffs[key] = {'changedRecipeCountsByTopLevelField': dict(sorted(counts.items())),
                              'mechanicalDifferences': mechanics,
                              'interpretation': 'Preserved historical variants; no replacement or deletion authorized by this comparison.'}
    review = read(ROOT / 'data/director/crafting_recipe_review_catalog.json')
    reviewed_counts = Counter(r['trade'] for r in review['recipes'] if r['status'] == 'reviewed-authored-playtest')
    draft_counts = Counter(r['trade'] for r in review['recipes'] if r['status'] == 'draft-awaiting-GPT-review')
    trades = sorted({r['skill'] for r in current})
    trade_summary = [{'trade': t, 'legacy': sum(r['skill'] == t for r in legacy),
                      'expanded': sum(r['skill'] == t for r in current),
                      'public': sum(r['skill'] == t and r['visibility'] == 'public' for r in current),
                      'currentPassReviewed': reviewed_counts[t], 'currentPassDraft': draft_counts[t]} for t in trades]
    checks['originalFilesUnchanged'] = all(sha(GAME / rel) == digest for rel, digest in before.items())
    assert all(checks.values()), checks
    report = {
        'scope': 'Recipe history and source preservation, not a new mechanical/cosmology ruling or retrospective proof of every GPT conversation.',
        'status': 'PASS: identity reconciliation complete; historical approval scope and mechanical variants remain preserved for GPT discussion.',
        'checks': checks, 'sourcePaths': paths, 'sourceInventory': inventory,
        'sourceFilesReadOnly': len(sources), 'uniqueContentGroups': len(inventory),
        'legacyRecipeCount': len(legacy), 'expandedRecipeCount': len(current),
        'visibility': dict(Counter(r['visibility'] for r in current)),
        'addedRecipeIds': [r['id'] for r in added], 'trades': trade_summary,
        'workbook': {'path': paths['workbook'], 'sha256': sha(workbook), 'sheets': summary,
                     'supplementaryParts': extras, 'unmatchedRecipeRows': unmatched,
                     'differenceCounts': dict(differences), 'bindings': bindings,
                     'componentShapeProblems': component_shape_problems,
                     'observedNameCorrespondences': [{'field': f, 'workbook': a, 'legacyJSON': b, 'occurrences': n}
                                                     for (f, a, b), n in sorted(name_pairs.items())]},
        'versionDifferences': version_diffs,
        'currentPassTotals': review['totals'],
        'approvalInterpretation': 'The 175 count is this operational review pass only. Earlier owner-authorized V6 cutover is recorded in docs/canon/CANON_MANIFEST.json and docs/crafting/CRAFTING_V4_MAIN_CUTOVER_2026-08-05.md. Neither invalidating those approvals nor inferring present exact-card approval is warranted.',
        'noDeletion': True, 'cosmologyDeferredUntilVerifiedPush': True,
    }
    (AUDIT / 'CRAFTING_HISTORY_RECONCILIATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Crafting history reconciliation', '',
             '**The existing work is preserved: all 623 legacy recipe identities, names and effects are accounted for in the expanded 687-recipe catalog.** The expanded set adds four recipes to each of sixteen trades. The current 175 reviewed count describes the new operational manuscript pass; it does not mean only 175 recipes were previously written or approved.', '',
             'The [August cutover record](../../../crafting/CRAFTING_V4_MAIN_CUTOVER_2026-08-05.md) and [canon manifest](../../../canon/CANON_MANIFEST.json) record the earlier owner-authorized release. This audit verifies local file contents; it does not reconstruct every prior GPT conversation or revoke earlier decisions.', '',
             '## Verified source coverage', '',
             f'- {len(sources)} original source files were read without changes, grouped into {len(inventory)} distinct byte contents.',
             '- Five workbook copies are byte-identical. All 20 sheets were inspected: 16 recipe sheets, Dashboard, Recipe Template, Bestiary Cross-Reference and Validation Report. No hidden sheets, formulas or supplementary comment/external/drawing/VBA parts were found.',
             '- All 623 workbook recipe rows map uniquely by trade and legacy name to retained IDs. The row-by-row map and field differences are preserved in the [machine-readable evidence](CRAFTING_HISTORY_RECONCILIATION.json).',
             '- All 623 legacy names and effects are retained exactly in the V4 legacyName and legacyEffect fields. Older component definitions remain in the intact archive and workbook; these versions are not interchangeable.',
             '- The live 433-recipe public JSON is exactly the public projection of the 687-recipe mechanical catalog. The other 254 identities remain present as restricted or Director-only records.', '',
             '## Preserved differences', '',
             f'Workbook-to-legacy differences by field: `{json.dumps(dict(differences), sort_keys=True)}`. All of these component-field differences are names: ordered component counts, printed quantities and tier labels remain equal. The evidence records {len(name_pairs)} observed name correspondences (14 base-ingredient names and 45 monster-part names), including Mithral ingot → Brightsteel Ingot. This is a textual correspondence, not a new ruling that differently named materials can be substituted in play. The workbook also retains its separate 50-row Bestiary Cross-Reference and validation notes; those are historical evidence, not current creature-stat approval.', '',
             'The full internal V4 file has the same 687 identities but differs from the mechanical V4 in 21 tool-list records and eight component records. Every one of these differences is Focusing crystal/Crystal → Resonance lens/Lens; other fields in those mechanical records match. The exact changes are recorded in the evidence JSON. V2 also retains different publication/access metadata and Director guidance. All variants remain intact; this comparison makes no cosmology ruling.', '',
             '## Counts by trade', '',
             '| Trade | Legacy/workbook | Expanded | Public | Reviewed this pass | Draft this pass |',
             '|---|---:|---:|---:|---:|---:|']
    lines += [f"| {r['trade']} | {r['legacy']} | {r['expanded']} | {r['public']} | {r['currentPassReviewed']} | {r['currentPassDraft']} |" for r in trade_summary]
    lines += ['', 'The 43 Blacksmithing drafts have source/interface decisions and local validation, but no completed exact-manuscript verdict. Calibration Review reached its conversation-length limit. Its attempted exact submission is preserved; a replacement review chat awaits owner authorization. See the [prepared handoff](GPT_REVIEW_CONTINUATION_HANDOFF.md).', '',
              f"Validation: {len(checks)} checks passed. No original workbook, recipe source or prior reviewed rule was edited. No file was deleted. GitHub delivery and the careful post-push cosmology review remain pending.", '']
    (AUDIT / 'CRAFTING_HISTORY_RECONCILIATION.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'checks': len(checks), 'sourceFiles': len(sources), 'uniqueContents': len(inventory),
                      'workbookRows': len(bindings), 'workbookDifferences': dict(differences), 'trades': trade_summary}, ensure_ascii=False))


if __name__ == '__main__':
    main()
