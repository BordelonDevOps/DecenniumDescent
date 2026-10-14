"""Independent preservation/parity check of ACQ-05's current source descendants."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'; V = A / 'feat327-acq05-source'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def main():
    target = A / 'FEAT327_ACQ_05_INDEPENDENT_DESCENDANT_CHECK.json'
    assert not target.exists()
    receipt_path = A / 'FEAT327_ACQ_05_DERIVED_OPERATIONS.json'
    receipt = read(receipt_path)
    changes = {c['after']['path']: c for c in receipt['changes']}
    directions = read(V / 'ACQ05_EXACT_OPERATIONS.json')
    results = []

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def before(path):
        bound = changes[path.relative_to(G).as_posix()]['before']
        saved = G / bound['preservedCopy']
        actual = info(saved)
        check('preserved/' + bound['path'], all(actual[k] == bound[k] for k in ('bytes', 'sha256')))
        return saved

    check('actual-terminal-reply', read(A / 'FEAT327_ACQ_05_RECEIVED_DECISION.json')['replyMessageId'] == 'bda5be25-7b23-4bd0-8afb-8adbb01a18f7')
    check('five-existing-files', len(changes) == 5)
    # Independently assemble from the four narrow clauses, not whole-record edits.
    pub_path = R / 'data/public/feat_candidates/exact_01/candidate.json'
    old_pub = read(before(pub_path))
    old_row = next(r for r in old_pub['feats'] if r['id'] == 'animal_companion')
    procedure = old_row['operationalRules']
    for fragment in directions['verdictTextFragments']:
        check('single-old-fragment/' + fragment['id'], procedure.count(fragment['old']) == 1)
        procedure = procedure.replace(fragment['old'], fragment['replacement'])
    check('independently-assembled-full-procedure', procedure == (V / 'ACQ05_ANIMAL_COMPANION_OPERATIVE.txt').read_text(encoding='utf-8').rstrip('\n'))
    for path, collection, keys in [
        (pub_path, 'feats', ['operationalRules', 'payloadOperational']),
        (R / 'data/director/feat_candidates/exact_01/candidate.json', 'records', ['operationalRules', 'payloadOperational']),
        (A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', 'records', ['completeOperativeProcedure'])]:
        original = read(before(path)); current = read(path); reconstructed = deepcopy(current)
        prior = next(r for r in original[collection] if r['id'] == 'animal_companion')
        row = next(r for r in reconstructed[collection] if r['id'] == 'animal_companion')
        for key in keys:
            check(path.parent.name + '/' + key + '/current-parity', row[key] == procedure)
            row[key] = prior[key]
        check(path.relative_to(G).as_posix() + '/whole-envelope-otherwise-unchanged', reconstructed == original)
        expected_count = 327 if 'original335Registry' in current else 335
        check(path.relative_to(G).as_posix() + '/identity-count-retained', len(current[collection]) == len(original[collection]) == expected_count)
        if expected_count == 327:
            check('internal-eight-reviewed-plus-327-candidates', len(current['unchangedReviewedFeats']) == 8 and len(current['original335Registry']) == 335)
    for op in directions['operations']:
        if op['op'] != 'replace_text':
            continue
        path = G / op['path']; original = before(path).read_text(encoding='utf-8')
        current = path.read_text(encoding='utf-8')
        check(op['path'] + '/exact-named-section-only', current == original.replace(op['old'], op['replacement']))
        check(op['path'] + '/full-current-procedure', current.count(procedure) == 1)
    # Original input bindings are immutable. Candidate descendants follow only
    # measured source operations, never a blanket permission to ignore hashes.
    build = read(A / 'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    for rel, bound in build['originalSourceBindings'].items():
        actual = info(G / rel)
        check('original-source/' + rel, all(actual[k] == bound[k] for k in ['bytes', 'sha256']))
    descendants = {}
    for name in ['FEAT327_ACQ_01_DERIVED_FULFILLMENT.json', 'FEAT327_ACQ_02_DERIVED_OPERATIONS.json', 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json']:
        bindings = read(A / name)['measuredCurrentDescendants']
        descendants.update({b['path']: b for b in bindings} if isinstance(bindings, list) else bindings)
    for name in ['FEAT327_ACQ_04_DERIVED_OPERATIONS.json', receipt_path.name]:
        for change in read(A / name)['changes']:
            descendants[change['after']['path']] = change['after']
    for rel, bound in build['artifacts'].items():
        expected = descendants.get(rel, bound); actual = info(G / rel)
        check('current-candidate/' + rel, all(actual[k] == expected[k] for k in ['bytes', 'sha256']))
    check('47-current-artifacts-accounted', len(build['artifacts']) == 47)
    with zipfile.ZipFile(A / 'DD_FEAT327_ACQ05_Companion_Timing_Source.zip') as z:
        submitted = json.loads(z.read('PACKAGE_MANIFEST.json'))
        for rel, bound in submitted.items():
            expected = changes[rel]['after'] if rel in changes else {'path': rel, **bound}
            check('submitted-current-or-exact-descendant/' + rel, info(G / rel) == expected)
    for rel, bound in receipt['beforeProtectedBindings'].items():
        expected = changes[rel]['after'] if rel in changes else bound
        check('protected-file/' + rel, info(G / rel) == expected)
    check('twenty-expectations-not-yet-executed', not receipt['finiteBehavioralAcceptanceComplete'])
    record = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'passed-exact-five-file-descendants-and-protected-sources',
        'validator': info(Path(__file__)), 'derivedOperations': info(receipt_path),
        'checks': len(results), 'failures': [], 'results': results,
        'behavioralAcceptanceGroupsExecuted': 0, 'behavioralAcceptanceGroupsRemaining': 20,
        'candidateReadyForSubmission': False, 'candidateApproved': False,
        'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False,
        'remaining': 'Use a new lifecycle model/history adapter for the20 authored groups; retain the old completed-history model/report as historical evidence.'}
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(record, f, ensure_ascii=False, indent=2); f.write('\n')
    print(json.dumps({'report': info(target), 'checks': len(results), 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
