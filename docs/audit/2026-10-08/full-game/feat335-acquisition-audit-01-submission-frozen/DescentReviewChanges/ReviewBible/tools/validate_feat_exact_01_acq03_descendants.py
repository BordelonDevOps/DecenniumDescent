"""Independently reconstruct the eight ACQ-03 source-derived changes.

No implementation module is imported. This checks exact source operations and
preservation, not the outstanding casting-credential behavioral expectations.
"""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'
I = R / 'data/director/feat_candidates/exact_01'; U = R / 'data/public/feat_candidates/exact_01'
D = R / 'docs/feats/exact-candidate-01'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def main():
    output = A / 'FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json'
    assert not output.exists(), 'Preserve the existing report; do not rerun this one-use check over it'
    receipt_path = A / 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json'; receipt = read(receipt_path)
    source_path = A / 'FEAT327_ACQ_03_GPT_RESPONSE.json'; source = read(source_path)
    manifest = read(G / receipt['preservationManifest']['path'])
    preserved = {x['path']: x for x in manifest}
    results = []

    def check(label, truth, kind='whole-file-source'):
        results.append({'id': label, 'kind': kind, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def old_path(p):
        bound = preserved[p.relative_to(G).as_posix()]
        saved = G / bound['preservedCopy']
        check('preserved/' + bound['path'], info(saved)['sha256'] == bound['sha256'], 'source-integrity')
        return saved

    check('actual-source-message', source['messageId'] == '67894042-55c3-44d4-bf3a-a2f31dd1140b', 'source-data')
    check('eight-exact-descendants', len(receipt['changes']) == len(preserved) == 8, 'coverage')
    quoted = source['quotations']; check('three-quotations', len(quoted) == 3 and len(quoted[0]['paragraphs']) == 8, 'source-data')
    bridge = '\n\n'.join(quoted[0]['paragraphs']); anchor = 'For the six exploration training entries,'
    old_sentence, new_sentence = quoted[1]['text'], quoted[2]['text']
    for p in [I / 'shared_rules.json', U / 'shared_rules.json']:
        expected = read(old_path(p)); before = deepcopy(expected)
        fs02 = next(x for x in expected['rules'] if x['id'] == 'FS-02')
        fs09 = next(x for x in expected['rules'] if x['id'] == 'FS-09')
        check(str(p) + '/unique-insertion', fs02['wording'].count(anchor) == 1 and fs09['wording'].count(old_sentence) == 1, 'source-data')
        fs02['wording'] = fs02['wording'].replace(anchor, bridge + '\n\n' + anchor)
        fs09['wording'] = fs09['wording'].replace(old_sentence, new_sentence)
        check(str(p) + '/whole-exact-two-wording-changes', read(p) == expected)
        check(str(p) + '/FS01-retained', next(x for x in read(p)['rules'] if x['id'] == 'FS-01') == next(x for x in before['rules'] if x['id'] == 'FS-01'))
    check('internal-public-shared-parity', read(I / 'shared_rules.json') == read(U / 'shared_rules.json'))
    p = D / 'SHARED_RULES.md'; expected = old_path(p).read_text(encoding='utf-8')
    expected = expected.replace(anchor, bridge + '\n\n' + anchor).replace(old_sentence, new_sentence)
    check('shared-reader-exact', p.read_text(encoding='utf-8') == expected)
    old_public_supplement = None
    for p, key in [(I / 'supplements.json', 'completeAuthoringValue'), (U / 'supplements.json', 'value')]:
        expected = read(old_path(p))
        if p == U / 'supplements.json':
            old_public_supplement = deepcopy(expected)
        focus = next(x[key]['newSpellFocus'] for x in expected['groups'] if x['id'] == 'SUP-05')
        check(str(p) + '/no-previous-annotation', 'castingPrerequisitePolicyRef' not in focus, 'source-data')
        focus['castingPrerequisitePolicyRef'] = 'FEAT327-ACQ-03'
        check(str(p) + '/only-focus-annotation', read(p) == expected)
    p = D / 'SUPPLEMENTS.md'; expected = old_path(p).read_text(encoding='utf-8')
    old_group = next(x['value'] for x in old_public_supplement['groups'] if x['id'] == 'SUP-05')
    new_group = deepcopy(old_group); new_group['newSpellFocus']['castingPrerequisitePolicyRef'] = 'FEAT327-ACQ-03'
    expected = expected.replace(json.dumps(old_group, ensure_ascii=False, indent=2), json.dumps(new_group, ensure_ascii=False, indent=2))
    check('supplement-reader-exact', p.read_text(encoding='utf-8') == expected)
    p = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'; before = read(old_path(p)); expected = deepcopy(before)
    inventory = []

    def annotate(node, sid, path):
        if node['kind'] in {'actualSpellcastingRoute', 'actualCastAccess'}:
            inventory.append({'featId': sid, 'relativePointer': path, 'observedNode': deepcopy(node)})
            node['castingPrerequisitePolicyRef'] = 'FEAT327-ACQ-03'
        for index, child in enumerate(node.get('requirements', [])):
            annotate(child, sid, path + '/requirements/' + str(index))

    for row in expected['records']:
        annotate(row['requirements'], row['id'], '/requirements')
    node_source = read(A / 'FEAT327_ACQ_03_NODE_BINDINGS.json')
    check('independent-complete-node-inventory', inventory == [{k: x[k] for k in ['featId', 'relativePointer', 'observedNode']} for x in node_source['operations']], 'source-data')
    check('25-generic-eight-specific', Counter(x['observedNode']['kind'] for x in inventory) == {'actualSpellcastingRoute': 25, 'actualCastAccess': 8}, 'coverage')
    expected['controllingAddenda'].append(info(A / 'FEAT327_ACQ_03_RECEIVED_DECISION.json'))
    current = read(p); check('whole-contract-only-annotations-and-provenance', current == expected)
    check('historical-source-bindings-retained', before['sourceBindings'] == current['sourceBindings'])
    check('all335-originals-and-procedures-retained', all(x['originalObject'] == y['originalObject'] and x['completeOperativeProcedure'] == y['completeOperativeProcedure'] for x, y in zip(before['records'], current['records'])) and len(current['records']) == 335)
    unannotated = deepcopy(current)
    def strip(node):
        node.pop('castingPrerequisitePolicyRef', None)
        for child in node.get('requirements', []):
            strip(child)
    for row in unannotated['records']:
        strip(row['requirements'])
    check('all-original-boolean-filters-and-noncasting-predicates-retained', [x['requirements'] for x in unannotated['records']] == [x['requirements'] for x in before['records']])
    p = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'; expected_text = old_path(p).read_text(encoding='utf-8')
    for x, y in zip(before['records'], current['records']):
        if x['requirements'] != y['requirements']:
            old_line = f"| `{x['id']}` | {x['printedPrerequisite']} | `{json.dumps(x['requirements'], ensure_ascii=False, separators=(',', ':'))}` |"
            new_line = f"| `{y['id']}` | {y['printedPrerequisite']} | `{json.dumps(y['requirements'], ensure_ascii=False, separators=(',', ':'))}` |"
            check('reader-row-unique/' + x['id'], expected_text.count(old_line) == 1, 'source-data')
            expected_text = expected_text.replace(old_line, new_line)
    link = '[Controlling GPT addendum](FEAT327_ACQ_01_GPT_ADDENDUM.md).'
    expected_text = expected_text.replace(link, link + '\n\n[FEAT327-ACQ-03 casting snapshot addendum](FEAT327_ACQ_03_GPT_ADDENDUM.md) controls the annotated casting nodes and the supplementary Spell Focus school choice. Other Boolean alternatives and prerequisites remain unchanged.')
    check('all335-reader-rows-only-authorized-changes', p.read_text(encoding='utf-8') == expected_text)
    build = read(A / 'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    for rel, bound in build['originalSourceBindings'].items():
        actual = info(G / rel)
        check('unchanged-original/' + rel, all(actual[k] == bound[k] for k in ['bytes', 'sha256']), 'source-integrity')
    overrides = {}
    for name in ['FEAT327_ACQ_01_DERIVED_FULFILLMENT.json', 'FEAT327_ACQ_02_DERIVED_OPERATIONS.json', 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json']:
        descendants = read(A / name)['measuredCurrentDescendants']
        overrides.update({x['path']: x for x in descendants} if isinstance(descendants, list) else descendants)
    for rel, historical in build['artifacts'].items():
        bound = overrides.get(rel, historical); actual = info(G / rel)
        check('current-candidate/' + rel, all(actual[k] == bound[k] for k in ['bytes', 'sha256']), 'source-integrity')
    check('all47-candidate-artifacts-accounted-for', len(build['artifacts']) == 47, 'coverage')
    for change in receipt['changes']:
        check('measured-current/' + change['after']['path'], info(G / change['after']['path']) == change['after'], 'source-integrity')
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-exact-source-descendants-behavioral-acceptance-pending',
        'sourceReply': info(source_path), 'derivedOperations': info(receipt_path), 'validator': info(Path(__file__)),
        'descendants': 8, 'annotatedCastingNodes': 33, 'checks': len(results), 'checkKinds': dict(Counter(x['kind'] for x in results)),
        'failures': [], 'results': results, 'onlyThisNamedIssueClosed': False, 'finiteBehavioralAcceptanceComplete': False,
        'remainingAcceptance': 'Execute source-qualified A-H and additional acquisition snapshot controls from the actual GPT reply. Strings/annotations alone do not establish actual qualifying personal grants. Do not count33 casting identities as covered by this source operation.',
        'priorReportsRemainHistorical': 'Magic Initiate/lineage/training/ownership reports retain their pre-ACQ-03 bindings. Current eight-file differences are bound separately; do not rewrite old reports or blindly rerun obsolete hash expectations.',
        'candidateExactApproved': False, 'candidateReadyForSubmission': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False}
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2); stream.write('\n')
    print(json.dumps({'report': info(output), 'checks': len(results), 'failures': 0, 'behavioralAcceptanceComplete': False}, indent=2))


if __name__ == '__main__':
    main()
