"""Index exact finite evidence and expose gaps; do not promote or recertify."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, V, info, encoded, digest


def read(path):
    return json.loads(path.read_bytes())


def main():
    output = A/'DI7_FINITE_93_EVIDENCE_INVENTORY.json'
    assert not output.exists()
    paths = {
        'cast': 'DI7_CAST_TRANSACTIONS_CHECK.json', 'fate': 'DI7_FATE_TRANSACTIONS_CHECK.json',
        'acquisition': 'DI7_ALL_SEVEN_ACQUISITION_CHECK.json', 'shield': 'DI7_SHIELD_LATE_TRANSACTIONS_CHECK.json',
        'vision': 'DI7_VISION_TRANSACTIONS_V2_CHECK.json', 'faction': 'DI7_FACTION_TRANSACTIONS_V2_CHECK.json',
        'geometry': 'DI7_AREA_GEOMETRY_CHECK.json', 'mass': 'DI7_MASS_TRANSACTIONS_CHECK.json',
        'alignment': 'DI7_ALIGNMENT_TRANSACTIONS_CHECK.json', 'clock': 'DI7_ALIGNMENT_CLOCK_CHECK.json',
        'supreme': 'DI7_SUPREME_TRANSACTIONS_CHECK.json', 'shaman': 'DI7_SHAMAN_TRANSACTIONS_CHECK.json',
        'assembly': 'DI7_EXACT_01_ASSEMBLY_CHECK.json'}
    reports = {key: read(A/value) for key, value in paths.items()}
    for key, report in reports.items():
        assert report['status'] == 'pass' and not report['failures'], key
    history_indices = {k: {h['id']: i for i,h in enumerate(r.get('histories', []))} for k,r in reports.items()}
    expectations_path = R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    expectations = read(expectations_path)
    expected = {v['id']: v for g in expectations['groups']+expectations['supplementalSourceExpectations'] for v in g['variants']}
    assert len(expected) == 93
    rows = {}

    def add(eid, alias, histories=(), *, status='conditional-execution-evidence', note='', source_refs=()):
        assert eid in expected
        row = rows.setdefault(eid, {'id': eid, 'expectation': deepcopy(expected[eid]), 'status': status, 'evidence': [], 'qualifications': []})
        assert row['status'] == status
        if note: row['qualifications'].append(note)
        for hid in histories:
            assert hid in history_indices[alias], (alias, hid)
            row['evidence'].append({'report': info(A/paths[alias]), 'historyId': hid, 'pointer': '/histories/'+str(history_indices[alias][hid])})
        for path in source_refs:
            row['evidence'].append({'source': info(path), 'kind': 'source-or-preservation-proof-not-behavior'})
        if not histories and not source_refs:
            row['evidence'].append({'report': info(A/paths[alias]), 'kind': 'complete-report-structural-checks'})

    def h(eid, alias, *ids, **kwargs):
        add(eid, alias, ids, **kwargs)

    h('D7T-01-01', 'acquisition', *history_indices['acquisition'], note='Hybrid class19 grants eligibility only; actual class20 one-spell additions and source-bounded lower-rank replacement proofs remain distinct from authenticated progression.')
    h('D7T-01-01', 'cast', 'source-qualified-Wizard-mass-revelation', 'source-qualified-Cleric-mass-revelation')
    h('D7T-01-02', 'cast', 'not-acquired', 'book-only', 'Bloodcaller-retains-pool-not-spells', 'gate-lost-provider', note='Actual route/repertoire gates are executed. Unimplemented Oracle/item/feat routes are not invented or granted by these adapters.')
    add('D7T-01-03', 'assembly', status='structural-preservation-evidence', source_refs=[R/'data/public/spell_playtests/catalog.json', V/'DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json'])
    h('D7T-02-01', 'cast', 'gate-silence', 'gate-speech', 'gate-somatic', 'gate-wrong-focus-owner', 'gate-wrong-focus-class', 'gate-focus-inaccessible', 'gate-incapacity')
    h('D7T-02-02', 'cast', 'price-band-0', 'price-band-11', 'price-band-14', 'counter-face-15', 'counter-face-14', 'nested-LIFO-parent-history', 'postcommit-incapacity')
    h('D7T-02-02', 'alignment', 'paid-binary/17/0', 'paid-immunity/alignment-alteration')
    h('D7T-03-01', 'geometry', 'DI7-GEO-M1', 'DI7-GEO-M4', 'DI7-GEO-M5', 'mass-revelation/clipping-and-empty-history-location', note='Exact requested30.1/60.1 boundary operands are not yet separately recorded here;35/65 grid exclusions and rational formula checks are recorded.', status='bounded-evidence-gap')
    h('D7T-03-02', 'mass', 'condition-helper-observer-specific-results', 'actual-limited-communication', 'snapshot-and-stale-communication')
    h('D7T-03-03', 'mass', 'paid-four-categories/Wizard', 'actual-hostility/peaceful', 'actual-hostility/disagreement', 'actual-hostility/foreign-target', 'actual-hostility/enemy-flag-only', 'trap-field-protection')
    h('D7T-04-01', 'mass', 'paid-four-categories/Wizard', 'lie-admission/speaker-left', note='Times translated to the same inclusive six-second interval in the paid fixture; all four provider histories exercise the boundary.')
    h('D7T-04-02', 'mass', 'paid-four-categories/Wizard', 'belief-protection', 'lie-admission/unheard', 'lie-admission/not-understood', 'lie-admission/recorded-sound')
    h('D7T-05-01', 'shield', 'miss-hit-Maiming-third-Multiattack-conditional-schedule', 'save-and-actual-beneficial-FateCoin', 'zero-hit')
    h('D7T-05-02', 'shield', 'miss-hit-Maiming-third-Multiattack-conditional-schedule', 'one-cast-three-roots-then-actual-scheduled-tick')
    h('D7T-05-03', 'shield', 'second-group-interleaved-third', 'second-component-expiry', 'second-component-dispel')
    h('D7T-06-01', 'shield', 'retarget-to-target', 'retarget-to-other', 'nonoccurrences')
    h('D7T-06-02', 'shield', 'actual20-to15and5-target-protected-conditional-transfer-eligibility', 'actual20-to15and5-other-protected-conditional-transfer-eligibility', 'zero-share')
    h('D7T-06-03', 'shield', 'post-defense6-conditional-paid-source-eligibility', 'identity-and-non-damage-boundaries')
    h('D7T-06-04', 'shield', 'miss-hit-Maiming-third-Multiattack-conditional-schedule', 'save-and-actual-beneficial-FateCoin')
    h('D7T-07-01', 'shield', 'replacement-success', 'replacement-countered', 'replacement-invalidated', 'caster-and-recipient-death')
    h('D7T-07-02', 'shield', 'suppressed-whole-and-exact-deadline', 'source-case-A-closed-admission', 'source-case-C-prior-use-True')
    h('D7T-08-01', 'fate', 'inclusive18-actual-cast-and-new-coin', 'rejected-original-too-old', 'rejected-original-no-observation', 'rejected-original-unresolved', 'rejected-original-copy-descendant', 'rejected-original-future-original-record')
    h('D7T-08-02', 'fate', 'rejected-original-null-rank', 'rejected-original-wrong-source-version', status='bounded-evidence-gap', note='Exact active original adapters implement only Fate Coin and Alignment Suggestion. No actual paid Reaction-only/damaging/indirect-damage/other-rank or Bonus Action original rejection histories are supplied by this report. Do not call the full finite admission variant executed.')
    h('D7T-08-03', 'fate', 'readied-original-age-rejection')
    h('D7T-08-03', 'supreme', 'history-not-copy-access-and-limited-communication')
    h('D7T-09-01', 'fate', 'inclusive18-actual-cast-and-new-coin', 'child-is-not-prepared-matrix-even-if-known')
    h('D7T-09-02', 'fate', 'spent-matrix-initialD9', 'known-child-block', 'known-child-unaffordable')
    h('D7T-09-03', 'fate', 'exclusive-reservation-and-outer-counter', 'child-counter-no-result-no-refund')
    h('D7T-09-04', 'fate', 'repriced-after-actual-counter-counter', 'repriced-unaffordable-after-actual-counter-counter', 'now-Fractured-after-actual-counter-counter', 'lost-child-components-conditional-intervening-world-event', 'moved-child-target-conditional-intervening-world-event', 'occupied-child-hand-conditional-intervening-world-event')
    h('D7T-10-01', 'fate', 'copy-provider-Cleric', 'copy-provider-Mirrorsage', 'copy-provider-Shaman', 'paid-child-actual-alignment-result', status='bounded-evidence-gap', note='Own provider statistics, focus, fresh save and exact two selected ordinary modes are executed. These two sources require no independent consumed material/charge. A source-qualified nonempty independent-entitlement child is not implemented and no waiver is granted.')
    h('D7T-10-02', 'fate', 'child-is-not-prepared-matrix-even-if-known', 'child-counter-no-result-no-refund', 'copy-coin-physical-hand-and-expiry')
    h('D7T-10-02', 'shaman', 'Fate-child/fate-coin', 'Fate-child/alignment-suggestion')
    h('D7T-10-03', 'fate', 'concentration-child-commit-and-counter')
    h('D7T-10-03', 'shaman', 'Fate-child/alignment-suggestion')
    h('D7T-10-04', 'fate', 'Ready-invalid-declined-then-valid-release-after18', 'Ready-expiry', 'Ready-concentration-loss', 'Ready-incapacity', 'Ready-prohibited-Reaction')
    h('D7T-10-04', 'shaman', 'Ready-hold-and-release', 'chronological-Fate-forecast-with-real-vent')
    h('D7T-11-01', 'vision', 'paid-complete-Wizard', 'actual-related-self-anchor', 'unrelated', 'outside120', 'blocked-line', 'trance-interruption-forced-movement', 'trance-interruption-incapacitated', 'trance-interruption-suppression', 'trance-interruption-lose-concentration')
    h('D7T-11-02', 'vision', 'later-Silence', 'damage-concentration-(24, 10, 2)', 'damage-concentration-(24, 9, 2)', 'voluntary-end-before-real-Counterspell', 'same-time-application-order-3500', 'same-time-application-order-3601', 'completed-answer-stays')
    h('D7T-11-03', 'vision', 'future-finite-guidance', 'outside-future-horizon', 'word-bound-selects-complete-supported-step')
    h('D7T-12-01', 'faction', 'paid-institutional-register-Wizard', 'false-member', 'undefined-member', 'protected-member')
    h('D7T-12-02', 'faction', 'paid-institutional-register-Wizard', '129-actual-activities-no-arbitrary-cap', 'actual-updates-and-reference-death')
    h('D7T-12-03', 'faction', 'actual-updates-and-reference-death', 'pause-and-current-only-resume-suppression', 'pause-and-current-only-resume-incapacity', 'exact-deadline-no-notice', 'feed-ending-caster-death', 'feed-ending-institution-ceased')
    h('D7T-12-04', 'faction', 'personal-field-protection', 'existence-and-update-side-channel', 'undefined-field')
    for eid, ids in reports['alignment']['sourceExpectationCoverage'].items():
        add(eid, 'alignment', ids)
    h('D7T-13-03', 'clock', 'Wizard/3601/0', 'outside-to-inside', 'actual-Fate-copied-Suggestion-clock', note='Suggestion keeps its original virtual-source-start clock; Purge uses its separate60 elapsed seconds. Full initiative scheduling remains a premise.')
    h('D7T-14-01', 'geometry', 'DI7-GEO-S1', 'DI7-GEO-S2', 'DI7-GEO-R1', 'DI7-GEO-I2', 'resonance-sight-supreme/clipping-and-empty-history-location')
    h('D7T-14-01', 'supreme', 'actual-paid-historical-query/Wizard', 'uncapped-established-history', 'current-wall-clipping')
    h('D7T-14-02', 'supreme', 'actual-paid-historical-query/Wizard', 'B-partial-history', 'B-different-protected-interior')
    h('D7T-14-03', 'supreme', 'ordinary-empty-history', 'protected-empty-history', 'unresolved-empty-history', 'C-current-only', 'scope/different-subject', 'scope/different-school', 'scope/different-rank', 'history-not-copy-access-and-limited-communication')
    h('D7T-15-01', 'vision', 'same-world-distinct-caster-paid-equivalent-query', 'same-caster-second-paid-query', 'new-world-event')
    h('D7T-15-01', 'mass', 'repeated-paid-query-with-Refrain', 'actual-change-during-counter-window')
    h('D7T-15-01', 'supreme', 'unchanged-paid-repeat', 'two-casters-same-world')
    h('D7T-15-02', 'vision', 'communication-preserves-private-content-boundary')
    h('D7T-15-02', 'mass', 'actual-limited-communication', 'snapshot-and-stale-communication')
    h('D7T-15-02', 'supreme', 'history-not-copy-access-and-limited-communication', note='Public/internal rendering and source-object parity are checked below; the public card fields retain procedures and original source records, not the conditional world fixture dossiers.')
    add('D7T-16-01', 'assembly', status='structural-preservation-evidence', source_refs=[V/'EXACT_DI7_CORRECTIONS.json', A/'DI7_AP_AS_01_DERIVED_OPERATIONS.json', A/'DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json'])
    add('D7T-16-02', 'assembly', status='package-preparation-pending', source_refs=[V/'DI7_ORIGINAL_EXAMPLE_DISPOSITIONS.json', V/'DI7_SOURCE_DECISION_REGISTER.json'], note='Current envelopes preserve all14 corrected originals and13 mechanical/one receipt issue. The next assembled upload package is not yet made/sent; Nature is separately qualified.')
    add('D7T-16-03', 'assembly', status='external-submission-pending', note='No promotion/selection/count/runtime change is made. Actual separate complete-seven submission and GPT exact verdict are still pending.')
    for alias in ['geometry', 'supreme', 'shaman']:
        for eid, values in reports[alias]['sourceExpectationCoverage'].items():
            add(eid, alias, [values] if isinstance(values, str) else values)
    for eid, ids in {
        'DI7-SHIELD-LATE-A': ['source-case-A-closed-admission'], 'DI7-SHIELD-LATE-B1': ['source-case-B-no-old'],
        'DI7-SHIELD-LATE-B2': ['source-case-B-replace'], 'DI7-SHIELD-LATE-C': ['source-case-C-prior-use-False', 'source-case-C-prior-use-True']}.items():
        add(eid, 'shield', ids)
    for eid, ids in {
        'DI7-FACTION-REF-A': ['DI7-FACTION-REF-A/'+provider for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']],
        'DI7-FACTION-REF-B': ['DI7-FACTION-REF-B'], 'DI7-FACTION-REF-C-FALSE': ['DI7-FACTION-REF-C/false'],
        'DI7-FACTION-REF-C-SCOPE': ['DI7-FACTION-REF-C/protected', 'DI7-FACTION-REF-C/unrelated-scope']}.items():
        add(eid, 'faction', ids)
    assert set(rows) == set(expected)

    # A historical report is evidence for its bound input. Follow only exact
    # same-path preserved transitions; never silently relabel it as a new run.
    delta_names = ['DI7_AP_AS_01_DERIVED_OPERATIONS.json', 'DI7_ACQ19_DERIVED_OPERATIONS.json',
        'DI7_SHIELD_LATE_DERIVED_OPERATIONS.json', 'DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json',
        'DI7_GEOMETRY_DERIVED_OPERATIONS.json', 'DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json',
        'DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json', 'DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json']
    transitions = [c for name in delta_names for c in read(A/name)['changes']]
    validated, historical = {}, []
    def verify(binding):
        key = (binding['path'], binding['sha256'])
        if key in validated: return
        current = info(G/binding['path'])
        if current['sha256'] == binding['sha256']:
            assert current['bytes'] == binding['bytes']
            validated[key] = current
            return
        old = binding
        links = []
        while old['sha256'] != current['sha256']:
            matches = [c for c in transitions if c['before']['path'] == old['path'] and c['before']['sha256'] == old['sha256']]
            assert len(matches) == 1, key
            c = matches[0]
            preserved = (G/c['before']['preservedCopy']).read_bytes()
            assert len(preserved) == old['bytes'] and digest(preserved) == old['sha256']
            links.append(deepcopy(c))
            old = c['after']
            assert len(links) <= len(transitions)
        historical.append({'original': binding, 'current': current, 'transitions': links, 'qualification': 'Historical execution retained at original bytes; current source changes are separate bound clarifications, not an implicit rerun.'})
        validated[key] = current
    for report in reports.values():
        for binding in report.get('sourceBindings', [])+report.get('authorityBindings', []): verify(binding)
    assembly = reports['assembly']
    for proof in assembly['sourceDescendantProofs']:
        for field in ['source', 'reviewerReference', 'newDescendant']: verify(proof[field])

    public_path = R/'data/public/spell_candidates/divination_rank7_exact_01.json'
    internal_path = R/'data/director/spell_candidates/divination_rank7_exact_01.json'
    manuscript_path = R/'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    public, internal = read(public_path), read(internal_path)
    assert internal['completePublicEnvelope'] == public
    assert internal['publicEnvelopeBinding'] == info(public_path)
    assert internal['finiteExpectations'] == expectations
    assert not any(public[k] for k in ['exactReviewReceived', 'selectionEnabled', 'runtimeImplemented', 'cosmologyReviewed', 'sourceInformationDeleted', 'pushed'])
    text = manuscript_path.read_text(encoding='utf-8')
    catalog_path = R/'data/public/spell_playtests/catalog.json'
    catalog = read(catalog_path)
    by_id = {x['id']: x for x in catalog['spells']}
    dispositions = read(V/'DI7_ORIGINAL_EXAMPLE_DISPOSITIONS.json')
    assert internal['originalExampleDispositions'] == dispositions and len(dispositions) == 14
    source_envelope = internal['preservedSourceDirectionEnvelope']
    assert len(public['cards']) == 7 and len(public['issueMap']) == 14
    for card in public['cards']:
        sid = card['id']
        assert not card['approved'] and not card['selectable']
        assert card['preservedSourceAndProposalFields']['fullSourceAndCurrentAccessRecord'] == by_id[sid]
        assert by_id[sid]['operational'] is None and by_id[sid]['status'] == 'blocked-pending-operational-review'
        op = card['operationalCandidate']
        assert op['baseRpCost'] == 17 and op['rank'] == 7 and op['school'] == 'Divination'
        assert text.count(op['completeProcedure']) == 1
        assert op['workedCases'] == [d['replacement'] for d in dispositions if d['spellId'] == sid]
        assert all(text.count(example) == 1 for example in op['workedCases'])
    for value in public['sharedOperatingRules'].values():
        assert text.count(value) >= 1
    for c in read(A/'DI7_AP_AS_01_DERIVED_OPERATIONS.json')['changes']:
        verify(c['after'])
        assert digest((G/c['before']['preservedCopy']).read_bytes()) == c['before']['sha256']
    assert info(catalog_path)['sha256'] == 'c5de86abf689495abea5aa6cecb4a1cea441dcafea3805941bdbb6873e072b30'
    counts = {}
    for row in rows.values(): counts[row['status']] = counts.get(row['status'], 0)+1
    gaps = [row['id'] for row in rows.values() if row['status'] == 'bounded-evidence-gap']
    report = {'id': 'DI7-FINITE-93-EVIDENCE-INVENTORY', 'status': 'inventory-verified-not-full-fulfillment',
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'expectations': info(expectations_path),
        'originalVariants': 49, 'supplementalVariants': 44, 'totalVariants': 93, 'statusCounts': counts,
        'reports': {k: info(A/v) for k,v in paths.items()}, 'rows': list(rows.values()),
        'historicalBindingTransitions': historical, 'sourceBindingsValidated': len(validated),
        'currentCandidates': [info(p) for p in [public_path, internal_path, manuscript_path]],
        'guardedSourceOperations': 18, 'correctedOriginalExamples': 14, 'mechanicalIssues': 13, 'receiptOnlyIssues': 1,
        'sourceOriginalsAndAPASPreservationVerified': True, 'renderingAndEnvelopeParityVerified': True,
        'ordinaryCatalogUnchanged': info(catalog_path), 'ordinaryReviewed': 412, 'ordinaryPending': 436,
        'boundedEvidenceGaps': gaps, 'packagePending': ['D7T-16-02'], 'externalSubmissionPending': ['D7T-16-03'],
        'qualification': 'An index of specific conditional executions and structural evidence, not a fresh rerun, full runtime, campaign authentication, human playtest or exact-card approval. Read each report scope and source/version chain. Unsupported copied modes and independent costs remain explicit gaps rather than synthetic passes.',
        'nextActions': ['Exercise the exact fractional cone boundaries.', 'Supply genuine source-bound Fate admission cases and resolve the nonempty independent-entitlement test boundary without inventing a source.', 'Build the complete exact-seven package with all original examples/issues and preserved/current envelopes, then send it once to actual GPT.'],
        'full49Fulfilled': False, 'full93Fulfilled': False, 'exactApproved': False, 'selectionEnabled': False,
        'sourceInformationDeleted': 0, 'spellPromotions': 0, 'pushed': False, 'cosmologyReviewed': False}
    output.write_bytes(encoded(report))
    print(json.dumps({'report': info(output), 'statuses': counts, 'gaps': gaps, 'sourceBindingsValidated': len(validated)}))


if __name__ == '__main__':
    main()
