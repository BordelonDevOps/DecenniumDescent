"""Apply the exact received KEEP clarification to current DI7 expectations only."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, V, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    received = A / 'DI7_ACQ19_RECEIVED.json'
    delta = A / 'DI7_ACQ19_DERIVED_OPERATIONS.json'
    current_path = R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    preservation = A / 'source-before-di7-acq19-clarification'
    assert all(not p.exists() for p in [received, delta, current_path, preservation])
    dom_path = A / 'DI7_ACQ19_RECEIVED_DOM.txt'; screenshot = A / 'DI7_ACQ19_RECEIVED.png'
    text_path = A / 'DI7_ACQ19_EXPECTATION_REPLACEMENT.txt'; replacement = text_path.read_text(encoding='utf-8')
    dom = dom_path.read_text(encoding='utf-8')
    assert 'DI7-ACQ19 — KEEP: rank access is not spell acquisition' in dom and 'Response complete' in dom and 'button "Stop"' not in dom and screenshot.exists()
    assert replacement.startswith('All seven retain their exact original objects, source class placements') and replacement in dom
    source_path = V / 'FINITE_DI7_EXPECTATIONS.json'; source = read(source_path); current = deepcopy(source)
    assert current['groups'][0]['id'] == 'D7T-01' and current['groups'][0]['variants'][0]['id'] == 'D7T-01-01'
    old = current['groups'][0]['variants'][0]['expected']; assert old != replacement
    current['groups'][0]['variants'][0]['expected'] = replacement
    inverse = deepcopy(current); inverse['groups'][0]['variants'][0]['expected'] = old; assert inverse == source
    internal_path = R / 'data/director/spell_candidates/divination_rank7_exact_01.json'
    before_bytes = internal_path.read_bytes(); before = read(internal_path); after = deepcopy(before)
    assert before['finiteExpectations'] == source
    after['finiteExpectations'] = current
    inverse_internal = deepcopy(after); inverse_internal['finiteExpectations'] = source
    assert inverse_internal == before and encoded(inverse_internal) == before_bytes
    saved = preservation / internal_path.relative_to(G); saved.parent.mkdir(parents=True, exist_ok=True); saved.write_bytes(before_bytes)
    assert saved.read_bytes() == before_bytes
    preserved = {**info(internal_path), 'preservedCopy': saved.relative_to(G).as_posix()}
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded([preserved]))
    current_path.parent.mkdir(parents=True, exist_ok=True); current_path.write_bytes(encoded(current)); internal_path.write_bytes(encoded(after))
    now = datetime.now(timezone.utc).isoformat()
    operation = {'pointer': '/finiteExpectations/groups/0/variants/0/expected', 'groupIdGuard': 'D7T-01', 'variantIdGuard': 'D7T-01-01', 'old': old, 'replacement': replacement}
    delta.write_bytes(encoded({'recordedAtUtc': now, 'id': 'DI7-ACQ19-KEEP', 'classification': 'KEEP interpretation; no new learning grant',
        'changes': [{'before': preserved, 'after': info(internal_path), 'operations': [operation], 'exactInverseBytesVerified': True}],
        'newCurrentExpectations': info(current_path), 'originalExpectationsPreserved': info(source_path),
        'allOtherInternalFieldsUnchanged': True, 'allClassRankPlacementCostSelectionFieldsUnchanged': True, 'sourceInformationDeleted': 0}))
    received.write_bytes(encoded({'recordedAtUtc': now, 'reviewId': 'DI7-ACQ19', 'status': 'terminal-KEEP-clarification-received-applied',
        'submission': info(A / 'DI7_ACQ19_SUBMISSION.json'), 'responseDom': info(dom_path), 'visibleProof': info(screenshot),
        'exactReplacement': info(text_path), 'appliedOperation': info(delta), 'currentExpectations': info(current_path),
        'interpretation': 'Rank7 access remains19; ordinary hybrid fallback grants no new ranked learning addition at19 and same-or-lower rest replacement cannot upgrade rank6. Level20 may select one rank7 through its actual addition. No supplied independent19 acquisition route exists; Bloodcaller loss remains.',
        'finiteRequirement': 'For all seven IDs preserve placement; execute18 gate failure,19 unacquired rejection and prohibited rank6-to7 rest replacement, one actual20 selection, and retained-provider/Bloodcaller outcomes. No negative case spends or invents repertoire.',
        'reviewerDidNotRerunLocal185Checks': True, 'sourceConferenceReopened': False, 'replyReceived': True, 'pendingResponse': False,
        'exactCardsApproved': False, 'full49VariantsFulfilled': False, 'newRuleAdoptions': 0, 'cosmologyReviewed': False, 'pushed': False}))
    print(json.dumps({'received': info(received), 'delta': info(delta), 'currentExpectations': info(current_path)}))


if __name__ == '__main__':
    main()
