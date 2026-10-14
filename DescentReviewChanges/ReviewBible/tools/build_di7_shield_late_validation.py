"""Derive a fresh regression runner without overwriting the successful original."""
from apply_di7_ap_as_01 import R


def main():
    original = R / 'tools/validate_di7_shield_transactions.py'
    target = R / 'tools/validate_di7_shield_late_transactions.py'; assert not target.exists()
    text = original.read_text(encoding='utf-8')
    replacements = [
        ('from di7_shield_transactions import ShieldTransactions', 'from di7_shield_late_transactions import ShieldLateTransactions as ShieldTransactions'),
        ("output = A / 'DI7_SHIELD_TRANSACTIONS_CHECK.json'", "output = A / 'DI7_SHIELD_LATE_TRANSACTIONS_CHECK.json'"),
        ("'di7_shield_transactions.py', 'validate_di7_shield_transactions.py',", "'di7_shield_transactions.py', 'validate_di7_shield_transactions.py', 'di7_shield_late_transactions.py', 'validate_di7_shield_late_transactions.py',"),
        ("'First component while suppressed/unavailable, later first ward admission during the same occurrence: explicitly rejected pending GPT clarification.',", "'First-admission timing is now settled by DI7-SHIELD-LATE-01; the original68/27 report remains pre-ruling evidence.',"),
        ("extra += [R / 'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md',", "extra += [A / 'DI7_SHIELD_LATE_ADMISSION_RECEIVED.json', A / 'DI7_SHIELD_LATE_DERIVED_OPERATIONS.json', R / 'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md',"),
        ("'candidateApproved': False, 'full49Fulfilled': False,", "'sourceTimingRulingApplied': 'DI7-SHIELD-LATE-01', 'focusedSourceCases': ['A', 'B1', 'B2', 'C'], 'candidateApproved': False, 'full49Fulfilled': False,"),
        ("'Legal suppression/dispel events and independent recipient death are supplied campaign events.'", "'Legal suppression/dispel events and independent recipient death are supplied campaign events.', 'B1/B2 assume a separately legal upstream interleaving window for the actual paid Shield; this ward evaluator grants no such window and is not its source scheduler.'")]
    for old, new in replacements:
        assert text.count(old) == 1, old; text = text.replace(old, new, 1)
    old = """    m = make(); m.suppress_ward('ward', True); schedule(m, 'ambiguous'); packet(m, 'ambiguous', 0); m.suppress_ward('ward', False)
    reject('open-seam-late-first-admission-fails-closed', m, lambda: m.admit('ambiguous', 'part1', 'target'))
    record('explicit-unresolved-late-first-admission', m)
"""
    new = """    # Actual source ruling A: once a recipient's first component passes,
    # restored availability does not reopen admission for that occurrence.
    m = make(); m.suppress_ward('ward', True); m.advance(3610); schedule(m, 'case-A'); packet(m, 'case-A', 0)
    m.advance(3610.5); m.suppress_ward('ward', False)
    for i, at in [(1, 3611), (2, 3612)]: m.advance(at); packet(m, 'case-A', i)
    m.finish_occurrence('case-A')
    check('late-A-none-of-three-protected', [x['prevented'] for x in m.packet_results] == [0, 0, 0])
    check('late-A-no-use-original-deadline', m.wards['ward']['remaining'] == 2 and m.wards['ward']['deadline'] == 3660)
    schedule(m, 'A-later-tick', components=1, origin='case-A', occasion='actual-tick1', kind='spell-scheduled')
    packet(m, 'A-later-tick', 0); m.finish_occurrence('A-later-tick')
    check('late-A-distinct-tick-can-admit', m.wards['ward']['remaining'] == 1 and m.packet_results[-1]['prevented'] == 12)
    record('source-case-A-closed-admission', m)

    # The incoming schedule and separately legal interleaving permission are
    # explicit external premises. These calls execute the Shield's own source
    # learning, Action, RP, components, counter and attachment, not that grant.
    for mode in ['no-old', 'replace', 'failed', 'countered']:
        m = make(establish=mode != 'no-old'); m.advance(3610); schedule(m, 'case-B'); packet(m, 'case-B', 0)
        m.advance(3610.5); m.begin_turn('donor', 'conditional-legal-intervening-Shield-turn')
        m.declare('donor', 'premonition-shield', 'new', {'target': 'target'})
        if mode == 'countered':
            m.declare('counter', 'counterspell', 'counter-new', {'pendingCast': 'new'}); m.resolve_counter('counter-new', 20)
        else:
            if mode == 'failed': m.world['entities']['target']['willing'] = False
            m.resolve_shield('new')
        for i, at in [(1, 3611), (2, 3612)]: m.advance(at); packet(m, 'case-B', i)
        m.finish_occurrence('case-B')
        expected = [0, 0, 0] if mode == 'no-old' else [12, 0, 0] if mode == 'replace' else [12, 12, 12]
        check('late-B-' + mode + '/coverage', [x['prevented'] for x in m.packet_results] == expected)
        check('late-B-' + mode + '/paid-no-refund', m.actors['donor']['rp'] == 31 and m.casts['new']['refund'] == 0)
        if mode in {'no-old', 'replace'}:
            check('late-B-' + mode + '/new-uses-and-own-deadline', m.wards['new']['remaining'] == 2 and m.wards['new']['deadline'] == 3670.5)
            if mode == 'replace': check('late-B-old-admission-not-inherited', m.wards['ward']['ended'] and m.occurrences['case-B']['claims']['target'] == 'ward')
            schedule(m, 'B-later-tick', components=1, origin='case-B', occasion='actual-tick1', kind='spell-scheduled')
            packet(m, 'B-later-tick', 0); m.finish_occurrence('B-later-tick')
            check('late-B-' + mode + '/new-ward-admits-distinct-tick', m.packet_results[-1]['prevented'] == 12 and m.wards['new']['remaining'] == 1)
        else: check('late-B-' + mode + '/old-live-one-use', not m.wards['ward']['ended'] and m.wards['ward']['remaining'] == 1 and 'new' not in m.wards)
        record('source-case-B-' + mode, m)

    for prior_use in [False, True]:
        m = make()
        if prior_use: attack(m, 'prior-use')
        m.advance(3610); schedule(m, 'case-C'); packet(m, 'case-C', 0)
        m.advance(3611); m.suppress_ward('ward', True); packet(m, 'case-C', 1)
        m.advance(3612); m.suppress_ward('ward', False); packet(m, 'case-C', 2)
        check('late-C-resume-same-record-' + str(prior_use), [x['prevented'] for x in m.packet_results if x['occurrence'] == 'case-C'] == [12, 0, 12])
        check('late-C-only-one-use-' + str(prior_use), m.wards['ward']['remaining'] == (0 if prior_use else 1) and not m.wards['ward']['ended'])
        m.finish_occurrence('case-C')
        check('late-C-end-only-if-second-' + str(prior_use), m.wards['ward']['ended'] == prior_use)
        record('source-case-C-prior-use-' + str(prior_use), m)

    # Another recipient's first component is its own admission point, even
    # after the spell has already affected somebody else.
    m = make(target='other')
    receipt = {'id': 'per-recipient', 'kind': 'spell-immediate', 'originId': 'per-recipient', 'occasionId': 'immediate',
        'actualResolution': True, 'sourceFact': {'kind': 'conditional-source-qualified-recipient-schedule'},
        'components': [{'id': 'part0', 'rootId': 'per-recipient/root0', 'directTargets': ['target'], 'preShareTargets': []},
            {'id': 'part1', 'rootId': 'per-recipient/root1', 'directTargets': ['other'], 'preShareTargets': []}]}
    m.register_occurrence(receipt); packet(m, 'per-recipient', 0); packet(m, 'per-recipient', 1, target='other'); m.finish_occurrence('per-recipient')
    check('late-per-recipient-not-global-spell-checkpoint', [x['prevented'] for x in m.packet_results] == [0, 12] and m.wards['ward']['remaining'] == 1)
    record('independent-recipient-checkpoint', m)

    # A prior direct zero-damage component closes the same recipient's point;
    # later positive pre-mitigation sharing cannot reopen it. A prior zero
    # share alone supplies no point, so the first positive share can admit.
    for prior_direct in [False, True]:
        m = make(target='other'); m.suppress_ward('ward', True)
        receipt = {'id': 'share-timing', 'kind': 'spell-immediate', 'originId': 'share-timing', 'occasionId': 'immediate',
            'actualResolution': True, 'sourceFact': {'kind': 'conditional-source-qualified-share-schedule'},
            'components': [{'id': 'part0', 'rootId': 'share-timing/root0', 'directTargets': ['other' if prior_direct else 'target'], 'preShareTargets': []},
                {'id': 'part1', 'rootId': 'share-timing/root1', 'directTargets': ['target'], 'preShareTargets': ['other']}]}
        m.register_occurrence(receipt)
        packet(m, 'share-timing', 0, target='other' if prior_direct else 'target', amount=0 if prior_direct else 3)
        m.suppress_ward('ward', False); m.admit('share-timing', 'part1', 'target')
        root = DamageRoot('share-timing/root1', 'target', 20, 'physical', attack_hit=True)
        root.transfer(bloodbond, 'conditional-qualified-bloodweaver', {'other': 5})
        m.resolve_packet('share-timing', 'part1', root, root.original_id, LifeState(100, 100))
        _, event = m.resolve_packet('share-timing', 'part1', root, 'share-timing/root1/transfer/1', LifeState(100, 100))
        m.complete_component('share-timing', 'part1'); m.finish_occurrence('share-timing')
        check('late-share-checkpoint-' + str(prior_direct), event['actualDamageDealt'] == (5 if prior_direct else 0) and m.wards['ward']['remaining'] == (2 if prior_direct else 1))
        check('late-share-no-hit-or-save-' + str(prior_direct), not event['attackHit'] and not event['failedOriginalSave'])
        record('share-timing-prior-direct-' + str(prior_direct), m)
"""
    assert text.count(old) == 1; text = text.replace(old, new, 1)
    compile(text, str(target), 'exec'); target.write_text(text, encoding='utf-8', newline='\n')
    print(str(target))


if __name__ == '__main__': main()
