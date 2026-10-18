"""Trace bestiary identities and selected fields without executing build scripts."""
from collections import Counter
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess

from audit_crafting_history import workbook_sheets

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def literal(p, name):
    for node in ast.parse(p.read_text(encoding='utf-8-sig')).body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                return ast.literal_eval(node.value)
    raise ValueError((p, name))


def name_rules(base):
    rename_path = base / 'scripts/scrub_bestiary_ip.py'
    ingest_path = base / 'scripts/ingest_bestiary_from_excel.py'
    return {'renameMap': literal(rename_path, 'RENAME_MAP'),
            'aliases': literal(ingest_path, 'NAME_ALIASES'),
            'repeatedPrefixes': literal(ingest_path, 'REPEATED_NAME_PREFIXES'),
            'hiddenNames': sorted(literal(ingest_path, 'HIDDEN_NAMES'))}


def canonicalize(raw, rules):
    # Reproduce only the inspected pure string operations; do not import/run
    # source ingestion, workbook writers, generators or historical build entrypoints.
    name = raw.strip()
    if name in rules['renameMap']:
        name = rules['renameMap'][name]
    else:
        for old, new in sorted(rules['renameMap'].items(), key=lambda item: -len(item[0])):
            name = name.replace(old, new)
    for prefix in rules['repeatedPrefixes']:
        token = prefix + ' '
        while name.startswith(token + prefix):
            name = name[len(token):]
    return rules['aliases'].get(name, name)


def hidden(name, rules):
    return name in rules['hiddenNames'] or 'Hollow Dream' in name


def monsters(path):
    sheets, extra = workbook_sheets(path)
    sheet = next(s for s in sheets if s['name'] == 'Monsters')
    cells = sheet['cells']
    headers = {re.match(r'[A-Z]+', key)[0]: val for key, val in cells.items()
               if re.search(r'\d+$', key)[0] == '1'}
    numbers = sorted({int(re.search(r'\d+$', key)[0]) for key in cells
                      if int(re.search(r'\d+$', key)[0]) > 1})
    rows = [{'worksheetRow': n, 'cellsByHeader': {label: cells.get(col + str(n)) for col, label in headers.items()}}
            for n in numbers if cells.get('A' + str(n))]
    summary = [{'name': s['name'], 'state': s['state'], 'declaredRange': s['range'],
                'populatedCells': len(s['cells']), 'formulaCount': s['formulaCount']} for s in sheets]
    return rows, summary, extra, headers


def script_excerpt(path, start, stop):
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    return {'path': path.relative_to(GAME).as_posix(), 'sha256': sha(path),
            'startLine': start, 'endLine': stop,
            'text': '\n'.join(f'{i + 1}: {lines[i]}' for i in range(start - 1, min(stop, len(lines))))}


def main():
    paths = [Path(p) for p in subprocess.check_output([
        'rg', '--files', '--hidden', '-g', '*bestiary*.xlsx', '-g', '*Bestiary*.xlsx',
        '-g', '*bestiary_data_full*.json', str(GAME)], text=True).splitlines()]
    source_scripts = [base / 'scripts' / name for base in (GAME, ROOT) for name in (
        'ingest_bestiary_from_excel.py', 'scrub_bestiary_ip.py', 't1_5_bestiary_combat_trust.py',
        't6_10_bestiary_combat_trust.py', 'generate_bestiary_combat_sandbox.py')]
    older_builder = GAME / 'DecenniumDescentv6/scripts/build_known_descent_bestiary.py'
    source_scripts.append(older_builder)
    baseline = {p.relative_to(GAME).as_posix(): sha(p) for p in paths + source_scripts}
    groups = {}
    for p in paths:
        groups.setdefault(sha(p), []).append(p.relative_to(GAME).as_posix())
    inventory = []
    for digest, group in groups.items():
        entry = {'sha256': digest, 'paths': sorted(group), 'kind': 'xlsx' if group[0].endswith('.xlsx') else 'json'}
        if entry['kind'] == 'json':
            try:
                data = read(GAME / group[0])
                entry |= {'parseable': True, 'records': len(data), 'uniqueNames': len({r['name'] for r in data})}
            except json.JSONDecodeError as error:
                entry |= {'parseable': False, 'error': str(error), 'disposition': 'preserve all original bytes; no repair or deletion'}
        inventory.append(entry)

    runtime = read(ROOT / 'src/bestiary_data_full.json')
    runtime_by_name = {r['name']: r for r in runtime}
    main_rules, review_rules = name_rules(GAME), name_rules(ROOT)
    main_rows, main_sheets, main_extras, main_headers = monsters(GAME / 'Bestiary.xlsx')
    review_rows, review_sheets, review_extras, review_headers = monsters(ROOT / 'Bestiary.xlsx')
    main_by_row = {r['worksheetRow']: r['cellsByHeader'] for r in main_rows}
    review_by_row = {r['worksheetRow']: r['cellsByHeader'] for r in review_rows}
    row_diffs = [{'worksheetRow': n, 'field': key, 'main': main_by_row[n].get(key), 'review': review_by_row[n].get(key)}
                 for n in main_by_row for key in sorted(set(main_by_row[n]) | set(review_by_row[n]))
                 if main_by_row[n].get(key) != review_by_row[n].get(key)]
    mappings, failures, excluded = [], [], []
    scalar_fields = {'Size': 'size', 'Type': 'type', 'Alignment': 'alignment', 'Challenge': 'challengeRating',
                     'XP': 'xp', 'Zone Found': 'zoneFound', 'AC': 'armorClass', 'HP': 'hitPoints',
                     'Speed': 'speed', 'Save DC': 'saveDc'}
    for entry in review_rows:
        cells, number = entry['cellsByHeader'], entry['worksheetRow']
        name = canonicalize(cells['Name'], review_rules)
        if hidden(name, review_rules):
            excluded.append({'worksheetRow': number, 'nameCell': cells['Name'], 'normalizedName': name,
                             'reason': 'Existing ingestion hidden-name predicate; source row remains preserved.'})
            continue
        actual = runtime_by_name.get(name)
        assert actual is not None, (number, name)
        comparisons = []
        for column, key in scalar_fields.items():
            source = cells.get(column)
            if source is not None and key in ('xp', 'armorClass', 'hitPoints', 'saveDc'):
                source = int(float(source))
            stored = actual.get(key)
            comparisons.append({'column': column, 'runtimeField': key, 'source': source, 'runtime': stored, 'same': source == stored})
        provenance = (cells.get('Combat Provenance') or '').lower()
        expected_source = 'excel-sandbox' if 'excel-sandbox' in provenance else 'Bestiary.xlsx:Monsters'
        if 'companion-authored' in provenance:
            expected_source = 'companion-authored draft'
        for token in ('gate-guardian-trusted', 't6-10-trusted', 't1-5-trusted', 'band-trusted'):
            if token in provenance:
                expected_source = token
                break
        expected_draft = 'trusted' not in provenance
        label_match = actual['combat']['source'] == expected_source and actual['combat']['draft'] == expected_draft
        primary = actual['combat']['attacks'][0]
        attack1_match = primary['name'] == cells['Attack1 Name']
        row = {'worksheetRow': number, 'nameCell': cells['Name'], 'runtimeName': name,
               'runtimeIndex': next(i for i, r in enumerate(runtime) if r['name'] == name),
               'sourceCellsByHeader': cells, 'scalarComparisons': comparisons,
               'combatLabelDerivation': {'sourceColumn': cells['Combat Provenance'], 'expectedSource': expected_source,
                                        'expectedDraft': expected_draft, 'actualSource': actual['combat']['source'],
                                        'actualDraft': actual['combat']['draft'], 'same': label_match},
               'primaryAttackNameMatchesWorkbook': attack1_match,
               'needsReviewNoteAbsentFromRuntime': bool(cells.get('NeedsReview')) and 'NeedsReview' not in actual and 'needsReview' not in actual,
               'traitsColumnAbsentFromRuntime': bool(cells.get('Traits')) and 'traits' not in actual}
        mappings.append(row)
        failures.extend({'name': name, **c} for c in comparisons if not c['same'])
    projections = {}
    for label, rows, rules in (('main', main_rows, main_rules), ('review', review_rows, review_rules)):
        excel_names = {canonicalize(r['cellsByHeader']['Name'], rules) for r in rows}
        excel_names = {n for n in excel_names if not hidden(n, rules)}
        # Every current runtime row has a combat object, satisfying the inspected
        # override loader. This simulation covers names only, not full output data.
        overrides = {canonicalize(r['name'], rules) for r in runtime if r.get('combat')}
        retained_orphans = {n for n in overrides if n not in excel_names and canonicalize(n, rules) not in excel_names}
        projections[label] = {'scope': 'Names-only simulation of the inspected ingestion/override algorithm; no build executed',
                              'workbookNamesAfterExistingExclusion': len(excel_names),
                              'retainedCurrentOverrideOrphans': sorted(retained_orphans),
                              'projectedNames': sorted(excel_names | retained_orphans),
                              'projectedCount': len(excel_names | retained_orphans),
                              'workbookNamesAbsentFromCurrentRuntime': sorted(excel_names - set(runtime_by_name))}

    old_path = GAME / 'DecenniumDescentv6/src/bestiary_data_full.json'
    old = read(old_path)
    canonical = read(AUDIT / 'BESTIARY_SOURCE_RUNTIME_AUDIT.json')
    current_source_by_name = {r['name']: r for r in canonical['knownDossiers']}
    older_rows = []
    for r in old:
        source = current_source_by_name[r['name']]
        comparisons = [{'field': key, 'source': value, 'retainedV6': r.get(key), 'same': value == r.get(key)}
                       for key, value in (source['sourceFields'] or {}).items() if key != 'saveDc']
        older_rows.append({'id': r.get('id'), 'name': r['name'], 'sourceSlug': source['slug'],
                           'hasStatBlock': source['sourceFields'] is not None,
                           'compatibilityAliases': r.get('compatibilityAliases', []),
                           'publicationClassification': r.get('publicationClassification'),
                           'coreComparisonsExcludingSaveDC': comparisons,
                           'savedIngestSource': r.get('ingestSource'),
                           'hasStructuredCombat': 'combat' in r, 'hasSaveDc': 'saveDc' in r,
                           'lootKeys': list(r['loot']), 'actions': r['actions']})
    evidence = [script_excerpt(ROOT / 'scripts/ingest_bestiary_from_excel.py', 428, 452),
                script_excerpt(ROOT / 'scripts/ingest_bestiary_from_excel.py', 648, 680),
                script_excerpt(ROOT / 'scripts/ingest_bestiary_from_excel.py', 718, 752),
                script_excerpt(ROOT / 'scripts/t1_5_bestiary_combat_trust.py', 523, 525),
                script_excerpt(ROOT / 'scripts/t1_5_bestiary_combat_trust.py', 579, 620),
                script_excerpt(ROOT / 'scripts/t6_10_bestiary_combat_trust.py', 866, 923),
                script_excerpt(older_builder, 139, 184)]
    controls = {
        'all707RuntimeNamesBindUniquelyToReviewWorkbook': len(mappings) == len({r['runtimeName'] for r in mappings}) == len(runtime) == 707,
        'oneExistingHiddenSourceRowPreservedAndExcluded': len(excluded) == 1 and len(review_rows) == 708,
        'selectedScalarValuesMatchWorkbook': not failures,
        'all707CombatLabelsReproduceFromWorkbookProvenance': all(r['combatLabelDerivation']['same'] for r in mappings),
        'all707PrimaryAttackNamesMatchWorkbook': all(r['primaryAttackNameMatchesWorkbook'] for r in mappings),
        'mainAndReviewWorkbookCorrespondingRowsPreserved': set(main_by_row) == set(review_by_row) and len(main_by_row) == 708,
        'mainAndReviewNamesOnlyRebuildDifferenceQuantified': projections['main']['projectedCount'] == 727 and projections['review']['projectedCount'] == 707,
        'retainedV6All65NamesBindToCurrentKnownSource': len(older_rows) == 65 and all(r['name'] in current_source_by_name for r in old),
        'retainedV6All64SelectedCoreStatSetsMatchCurrentSource': sum(r['hasStatBlock'] for r in older_rows) == 64 and all(c['same'] for r in older_rows for c in r['coreComparisonsExcludingSaveDC']),
        'allInventoriedOriginalFilesUnchanged': all(sha(GAME / p) == h for p, h in baseline.items()),
    }
    report = {'status': 'PROVENANCE AUDIT ONLY; no ingestion, regeneration, source deletion or rule promotion',
              'sourceHashes': baseline, 'inventory': inventory, 'controls': controls,
              'workbookStructure': {'main': main_sheets, 'review': review_sheets,
                                    'mainExtraParts': main_extras, 'reviewExtraParts': review_extras,
                                    'mainHeaders': main_headers, 'reviewHeaders': review_headers},
              'mainAndReviewWorkbookDifferences': row_diffs, 'nameRules': {'main': main_rules, 'review': review_rules},
              'runtimeWorkbookBindings': mappings, 'existingExcludedRows': excluded,
              'selectedScalarFailures': failures, 'namesOnlyRebuildProjections': projections,
              'retainedV6Projection': {'path': old_path.relative_to(GAME).as_posix(), 'sha256': sha(old_path), 'rows': older_rows,
                                      'missingCurrentKnownNames': sorted(set(current_source_by_name) - {r['name'] for r in old}),
                                      'scope': 'Existing preserved projection, not a replacement approval. Missing fields and changed loot schema need integration.'},
              'scriptEvidence': evidence, 'noBuildScriptsExecuted': True, 'noOriginalFilesEdited': True,
              'cosmologyReviewDeferred': True}
    out = AUDIT / 'BESTIARY_HISTORY_PROVENANCE.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'controls': controls, 'inventoryFiles': len(paths), 'byteDistinctContents': len(groups),
                      'protectedFiles': len(baseline), 'scalarFailures': failures[:12],
                      'workbookDifferences': dict(Counter(r['field'] for r in row_diffs)),
                      'needsReviewNotesPreservedInWorkbook': sum(bool(r['sourceCellsByHeader'].get('NeedsReview')) for r in mappings),
                      'flaggedRowsWithRuntimeDraftFalse': sum(bool(r['sourceCellsByHeader'].get('NeedsReview')) and r['combatLabelDerivation']['actualDraft'] is False for r in mappings),
                      'traitsColumnsNotProjected': sum(r['traitsColumnAbsentFromRuntime'] for r in mappings),
                      'defenseCollectionsAllEmpty': all(not any(r['combat']['defenses'].values()) for r in runtime)}))
    assert all(controls.values()), controls


if __name__ == '__main__':
    main()
