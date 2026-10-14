"""Apply the actual ACQ-03 wording/annotations; retain originals and prior bindings.

This one-use source operation does not claim the separate finite behavioral
acceptance checks or the complete feat candidate are finished.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'
I = R / 'data/director/feat_candidates/exact_01'; U = R / 'data/public/feat_candidates/exact_01'
D = R / 'docs/feats/exact-candidate-01'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def encoded(v):
    return (json.dumps(v, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def at(value, pointer):
    for key in pointer.strip('/').split('/'):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def main():
    receipt = A / 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json'
    preservation = A / 'feat-exact-01-before-acq03'
    assert not receipt.exists() and not preservation.exists(), 'One-use operation already started'
    decision = read(A / 'FEAT327_ACQ_03_RECEIVED_DECISION.json')
    assert decision['replyMessageId'] == '67894042-55c3-44d4-bf3a-a2f31dd1140b'
    for key in ['reply', 'visibleReply', 'nodeBindings', 'sourceBindings']:
        assert info(G / decision[key]['path']) == decision[key]
    nodes = read(G / decision['nodeBindings']['path'])
    contracts_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    assert info(contracts_path)['sha256'] == nodes['sourcePathSha256']
    directive = decision['operations']; bridge = '\n\n'.join(directive['FS02']['paragraphs'])
    old_sentence = directive['FS09']['oldSentence']; new_sentence = directive['FS09']['newSentence']
    anchor = directive['FS02']['insertionBefore']
    planned = {}; changes = []; operations = []
    for p in [I / 'shared_rules.json', U / 'shared_rules.json']:
        value = read(p)
        for sid in ['FS-02', 'FS-09']:
            index = next(i for i, x in enumerate(value['rules']) if x['id'] == sid)
            old = value['rules'][index]['wording']
            if sid == 'FS-02':
                assert old.count(anchor) == 1 and 'FEAT327-ACQ-03' not in old
                new = old.replace(anchor, bridge + '\n\n' + anchor)
            else:
                assert old.count(old_sentence) == 1
                new = old.replace(old_sentence, new_sentence)
            value['rules'][index]['wording'] = new
            operations.append({'path': p.relative_to(G).as_posix(), 'pointer': f'/rules/{index}/wording', 'old': old, 'new': new})
        planned[p] = encoded(value)
    assert planned[I / 'shared_rules.json'] == planned[U / 'shared_rules.json']
    p = D / 'SHARED_RULES.md'; old = p.read_text(encoding='utf-8')
    assert old.count(anchor) == 1 and old.count(old_sentence) == 1
    planned[p] = old.replace(anchor, bridge + '\n\n' + anchor).replace(old_sentence, new_sentence).encode('utf-8')
    old_sup = read(U / 'supplements.json')
    for p in [I / 'supplements.json', U / 'supplements.json']:
        value = read(p); index = next(i for i, x in enumerate(value['groups']) if x['id'] == 'SUP-05')
        value_key = 'completeAuthoringValue' if p == I / 'supplements.json' else 'value'
        focus = value['groups'][index][value_key]['newSpellFocus']
        assert focus['id'] == 'proposal_spell_focus' and 'castingPrerequisitePolicyRef' not in focus
        focus.update(directive['annotation'])
        operations.append({'path': p.relative_to(G).as_posix(), 'pointer': f'/groups/{index}/{value_key}/newSpellFocus',
                           'addedFields': directive['annotation']})
        planned[p] = encoded(value)
    internal_focus = next(x['completeAuthoringValue']['newSpellFocus'] for x in json.loads(planned[I / 'supplements.json'])['groups'] if x['id'] == 'SUP-05')
    public_focus = next(x['value']['newSpellFocus'] for x in json.loads(planned[U / 'supplements.json'])['groups'] if x['id'] == 'SUP-05')
    assert all(internal_focus[key] == value for key, value in public_focus.items())
    old_group = next(x['value'] for x in old_sup['groups'] if x['id'] == 'SUP-05')
    new_group = deepcopy(old_group); new_group['newSpellFocus'].update(directive['annotation'])
    p = D / 'SUPPLEMENTS.md'; text = p.read_text(encoding='utf-8')
    old_block = json.dumps(old_group, ensure_ascii=False, indent=2)
    assert text.count(old_block) == 1
    planned[p] = text.replace(old_block, json.dumps(new_group, ensure_ascii=False, indent=2)).encode('utf-8')
    contracts = read(contracts_path); by_id = {row['id']: row for row in contracts['records']}
    assert len(nodes['operations']) == 33 and nodes['counts'] == {'actualSpellcastingRoute': 25, 'actualCastAccess': 8}
    for op in nodes['operations']:
        row = by_id[op['featId']]
        assert row['printedPrerequisite'] == op['sourcePrintedPrerequisite']
        node = at(row, op['relativePointer'])
        assert node == op['observedNode'] and op['derivedAnnotationToAdd'] == directive['annotation']
        node.update(op['derivedAnnotationToAdd'])
        operations.append({'path': contracts_path.relative_to(G).as_posix(), 'featId': row['id'],
                           'relativePointer': op['relativePointer'], 'addedFields': op['derivedAnnotationToAdd']})
    contracts['controllingAddenda'].append(info(A / 'FEAT327_ACQ_03_RECEIVED_DECISION.json'))
    # Original sourceBindings remain immutable history; this receipt binds current descendants.
    planned[contracts_path] = encoded(contracts)
    p = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'; text = p.read_text(encoding='utf-8')
    old_contracts = read(contracts_path)
    for old_row, new_row in zip(old_contracts['records'], contracts['records']):
        if old_row['requirements'] != new_row['requirements']:
            old_line = f"| `{old_row['id']}` | {old_row['printedPrerequisite']} | `{json.dumps(old_row['requirements'], ensure_ascii=False, separators=(',', ':'))}` |"
            new_line = f"| `{new_row['id']}` | {new_row['printedPrerequisite']} | `{json.dumps(new_row['requirements'], ensure_ascii=False, separators=(',', ':'))}` |"
            assert text.count(old_line) == 1
            text = text.replace(old_line, new_line)
    link_anchor = '[Controlling GPT addendum](FEAT327_ACQ_01_GPT_ADDENDUM.md).'
    assert text.count(link_anchor) == 1
    text = text.replace(link_anchor, link_anchor + '\n\n[FEAT327-ACQ-03 casting snapshot addendum](FEAT327_ACQ_03_GPT_ADDENDUM.md) controls the annotated casting nodes and the supplementary Spell Focus school choice. Other Boolean alternatives and prerequisites remain unchanged.')
    planned[p] = text.encode('utf-8')
    assert len(planned) == 8
    # Build every complete output before any overwrite; preserve each original byte.
    for p, data in planned.items():
        before = info(p); saved = preservation / p.relative_to(G); saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, saved); assert saved.read_bytes() == p.read_bytes()
        changes.append({'before': {**before, 'preservedCopy': saved.relative_to(G).as_posix()},
                        'after': {'path': p.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'
    manifest.write_bytes(encoded([x['before'] for x in changes]))
    for p, data in planned.items():
        p.write_bytes(data)
    for change in changes:
        assert info(G / change['after']['path']) == change['after']
    record = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'addendumId': 'FEAT327-ACQ-03',
        'status': 'exact-derived-operations-applied-finite-behavioral-acceptance-still-required',
        'actualGptDecision': info(A / 'FEAT327_ACQ_03_RECEIVED_DECISION.json'),
        'preservationManifest': info(manifest), 'operations': operations, 'changes': changes,
        'measuredCurrentDescendants': {x['after']['path']: x['after'] for x in changes},
        'castingNodesAnnotated': 33, 'supplementarySpellFocusAnnotatedInBothViews': True,
        'historicalContractSourceBindingsPreserved': True,
        'onlyThisNamedIssueClosed': False, 'finiteBehavioralAcceptanceComplete': False,
        'candidateExactApproved': False, 'candidateReadyForSubmission': False,
        'sourceInformationDeleted': False, 'cosmologyReviewed': False,
        'scope': 'Two exact shared-wording amendments and policy annotations only. No original feat/card/effect, Wizard engine, Eldritch Blast school/payload, source archive, deferred payload, live selection or approval field is promoted or replaced. Historical proposal/source echoes remain historical; use the current shared contract and derived supplement.'}
    receipt.write_bytes(encoded(record))
    print(json.dumps({'receipt': info(receipt), 'descendants': len(changes), 'annotatedNodes': 33,
                      'behavioralAcceptanceComplete': False}, indent=2))


if __name__ == '__main__':
    main()
