"""Apply GPT's exact narrow Shield amendment, preserving every previous byte."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, node


def read(p): return json.loads(p.read_bytes())


def main():
    received_path = A / 'DI7_SHIELD_LATE_ADMISSION_RECEIVED.json'
    delta_path = A / 'DI7_SHIELD_LATE_DERIVED_OPERATIONS.json'
    preservation = A / 'source-before-di7-shield-late'
    assert all(not p.exists() for p in [received_path, delta_path, preservation])
    dom_path = A / 'DI7_SHIELD_LATE_ADMISSION_RECEIVED_DOM.txt'
    insertion_path = A / 'DI7_SHIELD_LATE_ADMISSION_INSERTION.txt'
    replacement_path = A / 'DI7_SHIELD_SUPPRESSION_RETURN_REPLACEMENT.txt'
    insertion = insertion_path.read_text(encoding='utf-8'); replacement = replacement_path.read_text(encoding='utf-8')
    dom = dom_path.read_text(encoding='utf-8')
    assert 'DI7-SHIELD-LATE-01 — first admission closes at the recipient’s first component' in dom
    assert 'Response complete' in dom and 'button "Stop"' not in dom and insertion in dom and replacement in dom
    assert insertion.startswith('NEW — first-admission closure and replacement.')
    assert replacement.startswith('After suppression ends, only the same still-live ward application')
    now = datetime.now(timezone.utc).isoformat()
    received = {'id': 'DI7-SHIELD-LATE-01', 'recordedAtUtc': now, 'status': 'terminal-source-ruling-received',
        'submission': info(A / 'DI7_SHIELD_LATE_ADMISSION_SUBMISSION.json'), 'responseDom': info(dom_path),
        'visibleProof': info(A / 'DI7_SHIELD_LATE_ADMISSION_RECEIVED.png'),
        'exactInsertion': info(insertion_path), 'exactSuppressionReturnReplacement': info(replacement_path),
        'authoredExpectationTable': info(A / 'DI7_SHIELD_LATE_ADMISSION_EXPECTED_TABLE.txt'),
        'interpretation': 'First admission closes once per actual occurrence and recipient across Shield applications. No late admission after suppression/new establishment/replacement. Replacement inherits no prior admission. Same admitted live ward can resume after suppression before expiry, including its second occurrence.',
        'classification': 'KEEP existing first-component and same-live-record principles; NEW minimal completion closes negative admission and replacement across the ward family.',
        'newRuleAdoptions': 1, 'newRuleScope': 'Family-wide first-admission closure for one occurrence and recipient.',
        'reviewerDidNotRerunTests': True, 'exactCardsApproved': False, 'full49Fulfilled': False,
        'replyReceived': True, 'pendingResponse': False, 'pushed': False, 'cosmologyReviewed': False}
    received_path.write_bytes(encoded(received))
    public_path = R / 'data/public/spell_candidates/divination_rank7_exact_01.json'
    internal_path = R / 'data/director/spell_candidates/divination_rank7_exact_01.json'
    manuscript_path = R / 'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    expectations_path = R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    paths = [public_path, internal_path, manuscript_path, expectations_path]
    before_bytes = {p: p.read_bytes() for p in paths}
    public = read(public_path); internal = read(internal_path); expectations = read(expectations_path)
    assert internal['completePublicEnvelope'] == public and internal['publicEnvelopeBinding'] == info(public_path)
    assert internal['finiteExpectations'] == expectations
    card_index = next(i for i, c in enumerate(public['cards']) if c['id'] == 'premonition-shield')
    assert card_index == 1 and not public['selectionEnabled'] and not public['exactReviewReceived']
    old = public['cards'][card_index]['operationalCandidate']['completeProcedure']
    anchor = 'Do not charge the abandoned intended target after a genuine retarget.'
    old_return = 'On return only the same still-live record and its actual remaining/committed occurrence may continue.'
    assert old.count(anchor) == old.count(old_return) == 1
    new = old.replace(anchor, anchor + '\n\n' + insertion, 1).replace(old_return, replacement, 1)
    assert new.replace(anchor + '\n\n' + insertion, anchor, 1).replace(replacement, old_return, 1) == old
    addendum = {'id': 'DI7-SHIELD-LATE-01', 'affectedSpellId': 'premonition-shield', 'authority': info(received_path),
        'scope': received['classification'], 'exactApproval': False}
    variants = [
        {'id': 'DI7-SHIELD-LATE-A', 'expected': 'Ward suppressed at the recipient first beam: zero uses spent, no prevention on any immediate beam after suppression ends, two uses and original deadline retained for distinct subsequent occurrences.'},
        {'id': 'DI7-SHIELD-LATE-B1', 'expected': 'No ward at recipient first beam; a later separately legally established paid ward cannot admit remaining beams. New ward retains two uses and its own60-second deadline; no cast refund.'},
        {'id': 'DI7-SHIELD-LATE-B2', 'expected': 'Old ward admitted first beam, then legally replaced: prior prevention remains, old application ends and discards unused remainder. Neither old nor new application protects subsequent beams. New ward spends no use on that occurrence and retains its own two uses/deadline.'},
        {'id': 'DI7-SHIELD-LATE-C', 'expected': 'Same live ward admitted first beam, suppressed only at second, then returns before third and before expiry: first/third protected, second unprotected, only one use spent. The same holds when initial commitment spent its second use, until occurrence completion; an unrelated interleaved event gains none.'}]
    supplement = {'id': 'DI7-SHIELD-LATE-01', 'authority': info(received_path),
        'evidenceKind': 'Authored expected outcomes; execution evidence is separate.', 'original49Unchanged': True,
        'variants': variants, 'interfaceNotes': [
            'Each recipient has its own checkpoint; another recipient first affected later may commit then.',
            'For share-only recipients only first positive pre-mitigation share creates the checkpoint; zero/post-defense skipPrevention branches create none.',
            'Prior qualifying direct component closes admission before any later share for the same recipient and occurrence.',
            'Failed/countered replacement retains old admitted coverage; exact deadline excludes even previously admitted later components.']}
    changes = []
    def change_json(path, original, operations):
        after = deepcopy(original)
        for op in operations:
            obj, key = node(after, op['pointer'])
            if op.get('add'):
                assert key not in obj; obj[key] = deepcopy(op['replacement'])
            else:
                assert obj[key] == op['old']; obj[key] = deepcopy(op['replacement'])
        inverse = deepcopy(after)
        for op in reversed(operations):
            obj, key = node(inverse, op['pointer']); assert obj[key] == op['replacement']
            if op.get('add'): del obj[key]
            else: obj[key] = deepcopy(op['old'])
        assert inverse == original and encoded(inverse) == before_bytes[path]
        changes.append((path, encoded(after), operations)); return after
    public = change_json(public_path, public, [
        {'pointer': '/cards/1/operationalCandidate/completeProcedure', 'spellIdGuard': 'premonition-shield', 'old': old, 'replacement': new},
        {'pointer': '/sourceDirectionAddenda', 'add': True, 'replacement': [addendum]}])
    expectations = change_json(expectations_path, expectations, [
        {'pointer': '/supplementalSourceExpectations', 'add': True, 'replacement': [supplement]}])
    old_internal = internal
    internal = change_json(internal_path, internal, [
        {'pointer': '/completePublicEnvelope/cards/1/operationalCandidate/completeProcedure', 'spellIdGuard': 'premonition-shield', 'old': old, 'replacement': new},
        {'pointer': '/completePublicEnvelope/sourceDirectionAddenda', 'add': True, 'replacement': [addendum]},
        {'pointer': '/publicEnvelopeBinding', 'old': old_internal['publicEnvelopeBinding'], 'replacement': info(public_path, encoded(public))},
        {'pointer': '/finiteExpectations/supplementalSourceExpectations', 'add': True, 'replacement': [supplement]}])
    assert internal['completePublicEnvelope'] == public and internal['finiteExpectations'] == expectations
    assert len(expectations['groups']) == 16 and sum(len(g['variants']) for g in expectations['groups']) == 49
    manuscript = manuscript_path.read_text(encoding='utf-8'); assert manuscript.count(old) == 1
    new_manuscript = manuscript.replace(old, new, 1)
    assert new_manuscript.replace(new, old, 1).encode() == before_bytes[manuscript_path]
    changes.append((manuscript_path, new_manuscript.encode(), [{'textReplace': True, 'old': old, 'replacement': new}]))
    preserved = []
    for path in paths:
        dest = preservation / path.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(before_bytes[path])
        assert dest.read_bytes() == before_bytes[path]
        preserved.append({**info(path), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    operations = []
    for path, data, ops in changes:
        path.write_bytes(data); assert path.read_bytes() == data
        operations.append({'before': next(x for x in preserved if x['path'] == path.relative_to(G).as_posix()),
            'after': info(path), 'operations': ops, 'exactInverseBytesVerified': True})
    delta_path.write_bytes(encoded({'id': 'DI7-SHIELD-LATE-01', 'recordedAtUtc': now, 'authority': info(received_path), 'changes': operations,
        'newRuleAdoptions': 1, 'original49ExpectationsUnchanged': True, 'focusedSupplementalExpectations': 4,
        'allOtherCandidateContentUnchanged': True, 'originalSourcesAndHistoricalDirectionsUnchanged': True,
        'allCostAccessApprovalSelectionFieldsUnchanged': True, 'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    print(json.dumps({'received': info(received_path), 'delta': info(delta_path), 'changedActiveFiles': len(operations), 'focusedSupplementalExpectations': 4}))


if __name__ == '__main__': main()
