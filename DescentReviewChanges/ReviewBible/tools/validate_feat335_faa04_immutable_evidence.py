"""Verify fresh captured values at every affected historical checkpoint."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
from hashlib import sha256
import ast
import json

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def info(path):
    b = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def main():
    output = A / 'FEAT335_FAA04_IMMUTABLE_EVIDENCE_CHECK.json'
    assert not output.exists()
    inventory_path = A / 'feat335-acquisition-audit-01-verdict/REPORT_SNAPSHOT_MISMATCHES.json'
    pairs = {
        'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json': 'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_FAA04_CHECK.json',
        'FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json': 'FEAT_EXACT_01_NUMERIC_PREREQUISITE_AFTER_FAA04_V2_CHECK.json'}
    reports = {name: read(A / name) for name in [*pairs, *pairs.values()]}
    inventory = read(inventory_path)
    results, comparisons = [], []

    def check(label, passed):
        results.append({'id': label, 'passed': bool(passed)})
        assert passed, label

    check('Exactly559 previously observed saved mismatches', inventory['count'] == len(inventory['rows']) == 559)
    for item in inventory['rows']:
        old_name = Path(item['path']).name
        position = int(item['pointer'].split('/')[-1])
        old = reports[old_name]['results'][position]
        fresh = reports[pairs[old_name]]['results'][position]
        check(old_name + item['pointer'], old == item['capturedRow'] and old['actual'] != old['expected'] and
              fresh.get('id', fresh.get('name')) == old.get('id', old.get('name')) and fresh['kind'] == old['kind'] and
              fresh['expected'] == old['expected'] and fresh['actual'] == fresh['expected'] and fresh.get('pass', fresh.get('passed')) is True)
        comparisons.append({'historicalReport': old_name, 'currentReport': pairs[old_name], 'pointer': item['pointer'],
                            'historicalSavedComparison': old, 'freshCapturedComparison': fresh})
    for name in pairs.values():
        data = reports[name]
        check(name + '/every-saved-pass-matches-captured-values', all(
            row['actual'] == row['expected'] and row.get('pass', row.get('passed')) is True for row in data['results']))
        check(name + '/no-failures', not data['failures'])
        for bound in data['sourceBindings']:
            check(name + '/source/' + bound['path'], info(G / bound['path']) == bound)
    helper_observations = []
    for stem in ['acquisition_history', 'numeric_prerequisites']:
        path = R / ('tools/validate_feat_exact_01_' + stem + '.py')
        tree = ast.parse(path.read_text('utf-8'))
        normalizers = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'normalized']
        main_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        check_node = next(n for n in main_node.body if isinstance(n, ast.FunctionDef) and n.name == 'check')
        namespace = {'checks': [], 'deepcopy': deepcopy}
        exec(compile(ast.Module(body=normalizers + [check_node], type_ignores=[]), str(path), 'exec'), namespace)
        actual = {'saves': {'CON'}, 'opportunities': {'earned4': {'spent': False}}}
        expected = deepcopy(actual)
        args = ['capture-before-later-events', actual, expected] if stem == 'acquisition_history' else ['capture-before-later-events', 'snapshot', actual, expected]
        namespace['check'](*args)
        captured = deepcopy(namespace['checks'][0])
        actual['saves'].add('WIS'); actual['opportunities']['earned4']['spent'] = True
        expected['saves'].add('STR'); expected['opportunities']['earned4']['spent'] = True
        check(stem + '/later-mutations-of-both-inputs-cannot-change-capture', namespace['checks'][0] == captured)
        helper_observations.append({'helper': path.relative_to(G).as_posix(), 'captured': captured,
                                    'laterActual': actual, 'laterExpected': expected})
    paths = [inventory_path, Path(__file__), *[A / name for name in [*pairs, *pairs.values()]],
             R / 'tools/validate_feat_exact_01_acquisition_history.py', R / 'tools/validate_feat_exact_01_numeric_prerequisites.py',
             A / 'FEAT335_ACQUISITION_AUDIT_01_DERIVED_OPERATIONS.json', A / 'FEAT335_FAA_FOLLOWTHROUGH_DERIVED_OPERATIONS.json',
             A / 'FEAT335_FAA04_NUMERIC_BINDING_ADAPTATION.json']
    data = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'finding': 'FAA-04', 'fulfilledGroups': ['AA-10', 'AA-11'],
            'status': 'Immutable capture correction verified at all559 affected original checkpoints with preserved historical rows.',
            'checks': len(results), 'failures': [], 'results': results, 'snapshotComparisons': comparisons,
            'correctedHelperMutationExperiments': helper_observations, 'sourceBindings': [info(p) for p in paths],
            'freshHistoryChecks': 897, 'freshNumericChecks': 11851, 'historicalMismatchRowsPreserved': 559,
            'failedIntermediateRunPreserved': info(A / 'FEAT_EXACT_01_NUMERIC_PREREQUISITE_AFTER_FAA04_CHECK.json'),
            'limits': 'Snapshot evidence integrity only. Does not prove335 complete acquisitions, other FAA findings, feat-use execution or human balance.',
            'sourceInformationDeleted': 0, 'fullFeatCandidateApproved': False}
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=lambda v: sorted(v) if isinstance(v, set) else v) + '\n', encoding='utf-8')
    print(json.dumps({'report': info(output), 'checks': len(results), 'mismatchCheckpointsCorrected': 559, 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
