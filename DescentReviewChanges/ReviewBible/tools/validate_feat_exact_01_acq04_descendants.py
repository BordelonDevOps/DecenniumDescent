"""Independently verify the minimal ACQ-04 changes and untouched source content."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def main():
    target = A / 'FEAT327_ACQ_04_INDEPENDENT_DESCENDANT_CHECK.json'
    assert not target.exists()
    receipt_path = A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json'
    receipt = read(receipt_path); decision = read(A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json')
    policy_path = A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json'; policy = read(policy_path)
    changes = {x['after']['path']: x for x in receipt['changes']}; results = []

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def before(path):
        binding = changes[path.relative_to(G).as_posix()]['before']
        saved = G / binding['preservedCopy']
        check('saved/' + binding['path'], info(saved)['sha256'] == binding['sha256'] and info(saved)['bytes'] == binding['bytes'])
        return saved

    check('actual-reply', decision['replyMessageId'] == 'a469c764-37b9-4beb-9a8c-f485a071eb8d')
    check('five-existing-files-only', len(changes) == 5)
    check('policy-verbatim-reviewer-file', policy_path.read_bytes() == (A / 'feat327-acq04-source' / policy_path.name).read_bytes())
    for side in ['public', 'director']:
        path = R / f'data/{side}/feat_candidates/exact_01/shared_rules.json'
        expected = read(before(path)); old = deepcopy(expected)
        row = next(x for x in expected['rules'] if x['id'] == 'FS-02')
        row['wording'] += '\n\n' + policy['sharedAppend']
        check(side + '/only-shared-append', read(path) == expected)
        check(side + '/old-FS02-retained-prefix', read(path)['rules'][1]['wording'].startswith(old['rules'][1]['wording'] + '\n\n'))
    check('public-internal-parity', read(R / 'data/public/feat_candidates/exact_01/shared_rules.json') == read(R / 'data/director/feat_candidates/exact_01/shared_rules.json'))
    path = R / 'docs/feats/exact-candidate-01/SHARED_RULES.md'
    original = before(path).read_text(encoding='utf-8')
    public_path = R / 'data/public/feat_candidates/exact_01/shared_rules.json'
    old_wording = read(G / changes[public_path.relative_to(G).as_posix()]['before']['preservedCopy'])['rules'][1]['wording']
    check('shared-manuscript-only-append', path.read_text(encoding='utf-8') == original.replace(old_wording, old_wording + '\n\n' + policy['sharedAppend']))
    path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    expected = read(before(path)); original = deepcopy(expected)
    annotated = []
    for row in expected['records']:
        if row['id'] in policy['dispositions']:
            check('policy-ref-previously-absent/' + row['id'], 'externalCredentialPolicyRef' not in row)
            row['externalCredentialPolicyRef'] = policy_path.relative_to(G).as_posix() + '#/dispositions/' + row['id']
            annotated.append(row['id'])
    check('exact-four-policy-references-only', read(path) == expected and len(annotated) == 4)
    check('335-originals-trees-procedures-flags-retained', all(
        {k: v for k, v in new.items() if k != 'externalCredentialPolicyRef'} == old
        for old, new in zip(original['records'], read(path)['records'])) and len(expected['records']) == 335)
    path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'
    old = before(path).read_text(encoding='utf-8'); current = path.read_text(encoding='utf-8')
    check('acquisition-manuscript-original-prefix', current.startswith(old))
    append = current[len(old):]
    check('four-only-rendered-references', append.count('ACQ04-EC1 disposition') == 4)
    for sid in annotated:
        check('rendered-policy/' + sid, f'`{sid}`' in append and f'#/dispositions/{sid}' in append)
    build = read(A / 'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    for rel, binding in build['originalSourceBindings'].items():
        actual = info(G / rel)
        check('original-source/' + rel, all(actual[k] == binding[k] for k in ['bytes', 'sha256']))
    overrides = {}
    for name in ['FEAT327_ACQ_01_DERIVED_FULFILLMENT.json', 'FEAT327_ACQ_02_DERIVED_OPERATIONS.json', 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json']:
        value = read(A / name)['measuredCurrentDescendants']
        overrides.update({x['path']: x for x in value} if isinstance(value, list) else value)
    overrides.update({rel: item['after'] for rel, item in changes.items()})
    for rel, bound in build['artifacts'].items():
        current_bound = overrides.get(rel, bound); actual = info(G / rel)
        check('current-candidate/' + rel, all(actual[k] == current_bound[k] for k in ['bytes', 'sha256']))
    check('47-artifacts-accounted-for', len(build['artifacts']) == 47)
    submitted = read(A / 'feat327-acq04-source/SUBMITTED_PACKAGE_MANIFEST.json')
    for rel, bound in submitted.items():
        actual = info(G / rel); current_bound = overrides.get(rel, bound)
        check('submitted-source-current/' + rel, all(actual[k] == current_bound[k] for k in ['bytes', 'sha256']))
    for rel, change in changes.items():
        check('measured-current/' + rel, info(G / rel) == change['after'])
    record = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-exact-five-descendants-plus-policy',
        'validator': info(Path(__file__)), 'decision': info(A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json'),
        'derivedOperations': info(receipt_path), 'policy': info(policy_path), 'checks': len(results), 'failures': [], 'results': results,
        'finiteBehavioralAcceptanceComplete': False, 'candidateReadyForSubmission': False,
        'onlyThisNamedIssueClosed': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False,
        'remaining': 'Execute all sixteen authored ACQ-04 acceptance groups before recording finite fulfillment.'}
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(record, f, ensure_ascii=False, indent=2); f.write('\n')
    print(json.dumps({'report': info(target), 'checks': len(results), 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
