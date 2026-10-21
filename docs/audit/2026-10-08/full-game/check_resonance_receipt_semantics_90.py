"""Independent bounded authored-fixture review; never imports or executes returned code."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json, hashlib

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'rank9-resonance-fields3-feedback-receipt-return-02'
OLD = A / 'rank9-resonance-fields3-part5-return-01'
R = G / 'DescentReviewChanges/ReviewBible'
OUT = A / 'RANK9_RESONANCE_FIELDS3_RECEIPT_SEMANTIC_RECONCILIATION_90.json'
SAVED = A / Path(__file__).name
for target in (OUT, SAVED):
    assert not target.exists(), str(target)

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

def info(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

checks = []
def check(name, condition, evidence=None):
    row = {'check': name, 'pass': bool(condition)}
    if evidence is not None:
        row['evidence'] = evidence
    checks.append(row)
    assert condition, name

def at(value, pointer):
    for key in pointer.strip('/').split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

FEATURE = 'wizard.supplement.arcane-feedback'
SOURCE = 'wizard#/cards/60'
IMMUTABLE = ('scopeId', 'ownerId', 'roundId', 'roundOrdinal', 'counterCastId',
             'negatedCastId', 'nativeCounterSourceRef', 'originalResolutionEventId',
             'settledAt', 'qualification')
def source_key(outcome):
    return json.dumps([outcome['scopeId'], outcome['ownerId'], FEATURE, outcome['counterCastId']], separators=(',', ':'))

def qualified(q):
    return all(q[k] is True for k in ('featureActuallyAcquired', 'ownActualCounterspell', 'successfullyNegated')) and all(q[k] is False for k in ('companionCounter', 'reflectedCounter', 'copiedCounter'))

def validate_ledger(state):
    ledger = state['limitedUses'][FEATURE]
    assert ledger['sourceRef'] == SOURCE and ledger['ownerId'] == state['ownerId']
    rounds, receipts = ledger['roundUses'], ledger['sourceSettlements']
    for round_id, use in rounds.items():
        assert use['state'] == 'spent'
        receipt = receipts[use['settlementId']]
        assert receipt['status'] == 'awarded' and receipt['roundId'] == round_id
    for key, receipt in receipts.items():
        assert source_key(receipt) == key == receipt['id']
        assert receipt['sourceRef'] == SOURCE and receipt['featureId'] == FEATURE
        assert receipt['ownerId'] == state['ownerId']
        assert receipt['scopeId'] == state['numberedRoundContext']['scopeId']
        assert receipt['requestedRP'] == 1 and qualified(receipt['qualification'])
        assert receipt['qualification']['recoveryPermitted'] is True
        assert 0 <= receipt['rpBeforeRecovery'] <= receipt['normalMaxRP']
        assert receipt['rpAfterRecovery'] == receipt['rpBeforeRecovery'] + receipt['creditedRP']
        assert receipt['rpAfterRecovery'] <= receipt['normalMaxRP']
        if receipt['status'] == 'awarded':
            assert receipt['creditedRP'] == 1
            assert rounds[receipt['roundId']] == {'state': 'spent', 'settlementId': key}
        else:
            assert receipt['status'] == 'no-award-round-already-spent'
            assert receipt['creditedRP'] == 0
            winner = receipt['roundWinnerSettlementId']
            assert winner != key and rounds[receipt['roundId']]['settlementId'] == winner
            assert receipts[winner]['status'] == 'awarded'

def settle(before, event):
    """Fixture-only reward projection. Native transaction and world qualification are supplied inputs."""
    state = deepcopy(before)
    try:
        validate_ledger(state)
        assert event['ownerId'] == state['ownerId']
        assert event['scopeId'] == state['numberedRoundContext']['scopeId']
        ledger = state['limitedUses'][FEATURE]
        key = source_key(event)
        previous = ledger['sourceSettlements'].get(key)
        if previous is not None:
            assert all(previous[k] == event[k] for k in IMMUTABLE)
            return state, {'status': 'duplicate-source-no-mutation', 'creditedRP': 0, 'originalSettlementId': key}
        q = event['qualification']
        if not qualified(q) or event['nativeCounterTransactionComplete'] is not True:
            return state, {'status': 'native-source-not-qualified', 'creditedRP': 0}
        if not q['recoveryPermitted']:
            return state, {'status': 'external-recovery-prohibition-no-award-projection', 'creditedRP': 0, 'zeroAwardFrequencyPolicySelected': False}
        if state['rp'] >= state['maxRP']:
            return state, {'status': 'normal-maximum-no-award-projection', 'creditedRP': 0, 'zeroAwardFrequencyPolicySelected': False}
        winner = ledger['roundUses'].get(event['roundId'])
        credit = 0 if winner else min(1, state['maxRP'] - state['rp'])
        receipt = {'id': key, 'featureId': FEATURE, 'sourceRef': SOURCE,
                   'status': 'no-award-round-already-spent' if winner else 'awarded',
                   **{k: deepcopy(event[k]) for k in IMMUTABLE},
                   'requestedRP': 1, 'rpBeforeRecovery': state['rp'], 'normalMaxRP': state['maxRP'],
                   'creditedRP': credit, 'rpAfterRecovery': state['rp'] + credit,
                   'frequencyDisposition': 'existing round use retained; this distinct source receives no recovery' if winner else 'spent; terminal source settlement and round pointer atomically committed with RP',
                   'otherBudgetMutation': 'none; native counter payment/Reaction/recharge/history already belongs to the counter transaction'}
        if winner:
            receipt['roundWinnerSettlementId'] = winner['settlementId']
        else:
            ledger['roundUses'][event['roundId']] = {'state': 'spent', 'settlementId': key}
        ledger['sourceSettlements'][key] = receipt
        state['rp'] += credit
        validate_ledger(state)
        result = {'status': receipt['status'], 'creditedRP': credit}
        if not winner:
            result['settlementId'] = key
        return state, result
    except (AssertionError, KeyError, TypeError, ValueError):
        return deepcopy(before), {'status': 'rejected-invalid-receipt-input', 'creditedRP': 0}

model, original = read(P / 'MODEL.json'), read(OLD / 'MODEL.json')
cp = read(A / 'ACTIVE_AUTHORING_CHECKPOINT_HEALING_BESTIARY_DISPATCH_89.json')
for binding in [cp['currentAuthoredIndex'], cp['currentAcceptedInterfaceRegistry'], cp['currentWorkQueue'], *cp['canonicalHelperBaselinesUnchanged']]:
    check('Unchanged canonical baseline: ' + binding['path'], info(G / binding['path']) == binding)
prior = read(A / 'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json')
intake = read(A / 'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json')
check('Prior full semantic review remains successful except the two explicit Feedback findings', prior['checkCount'] == 3099 and not prior['failures'] and len(prior['openFindings']) == 2)
check('Completed independent intake remains233 successful checks', intake['passed'] == 233 and intake['failed'] == 0)
check('Original MODEL binding matches inherited semantic review', info(OLD / 'MODEL.json')['sha256'] == '79d8411b7d0880ac8cb6682de895bbfc7ff75219575d68608de43f778e6525d9')
check('Successor MODEL binding exact', info(P / 'MODEL.json')['sha256'] == '5b02270f39fce01c392b6e8187ce9e144f06957d908140c5c18cf96f1e78952a')

sources = read(P / 'SOURCE_EVIDENCE.json')
for row in sources['sources']:
    raw = (P / row['completeFile']).read_bytes()
    live = G / row['originalArchiveReference']['member'].removeprefix('sources/')
    check('Complete retained source bytes/hash: ' + row['alias'], len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'])
    check('Complete source unchanged against live authority: ' + row['alias'], live.read_bytes() == raw)
wizard = read(P / 'sources/wizard.json')
for pointer, card in sources['completeCards'].items():
    check('Full class card comparison: ' + pointer, wizard['cards'][int(pointer.rsplit('/', 1)[1])] == card)
feedback = wizard['cards'][60]
check('Source level15 automatic Feedback one per round', feedback['minimumClassLevel'] == 15 and feedback['acquisition'] == 'automatic' and feedback['frequency'] == 'At most once per round')
check('Native class Counterspell Reaction3RP recharge2', wizard['cards'][17]['cost'] == '3 RP' and wizard['cards'][17]['activation'] == 'Reaction' and 'recharge 2 rounds' in wizard['cards'][17]['frequency'])
catalog = read(R / 'data/public/spell_playtests/catalog.json')
check('Full ordinary Counterspell source record exact', read(P / 'sources/ordinary_counterspell_complete_record.json') == catalog['spells'][38])

contract = read(P / 'FEEDBACK_RECEIPT_CONTRACT.json')
check('Full receipt contract agrees with MODEL', model['arcaneFeedbackReceiptFollowthrough'] == contract)
cases = read(P / 'FEEDBACK_DIAGNOSTICS.json')['cases']
check('All31 distinct diagnostic cases present', len(cases) == len({c['id'] for c in cases}) == 31)
computed = []
for i, case in enumerate(cases):
    after, result = settle(case['before'], case['sourceOutcome'])
    check(case['id'] + ': complete after-state independently reproduced', after == case['after'])
    expected_result = {k: v for k, v in case['result'].items() if k != 'message'}
    check(case['id'] + ': outcome independently reproduced', result == expected_result)
    check(case['id'] + ': Action/Reaction/recharge untouched by reward', all(after[k] == case['before'][k] for k in ('action', 'reaction', 'recharge')))
    before_other = {k: v for k, v in case['before']['limitedUses'].items() if k != FEATURE}
    after_other = {k: v for k, v in after['limitedUses'].items() if k != FEATURE}
    check(case['id'] + ': other feature budgets unchanged', before_other == after_other)
    check(case['id'] + ': RP credit arithmetic', after['rp'] - case['before']['rp'] == result['creditedRP'])
    computed.append({'id': case['id'], 'before': case['before'], 'sourceOutcome': case['sourceOutcome'], 'computedAfter': after, 'computedResult': result, 'scope': case['scope'], 'premise': case['premise']})

# Additional author-written malformed-state probes; these are not game/runtime tests.
probe_names = ['awarded receipt without round pointer', 'round pointer names nonexistent winner', 'historical receipt awards2RP', 'denied receipt names wrong winner', 'same original counter relabelled into next round', 'same original counter changes qualification']
probes = []
for i, name in enumerate(probe_names):
    seed = cases[11] if i == 3 else cases[0]
    state, event = deepcopy(seed['after']), deepcopy(seed['sourceOutcome'])
    ledger = state['limitedUses'][FEATURE]
    key = source_key(event)
    if i == 0:
        ledger['roundUses'].clear()
    elif i == 1:
        ledger['roundUses'][event['roundId']]['settlementId'] = 'nonexistent'
    elif i == 2:
        ledger['sourceSettlements'][key]['creditedRP'] = 2
        ledger['sourceSettlements'][key]['rpAfterRecovery'] += 1
    elif i == 3:
        ledger['sourceSettlements'][key]['roundWinnerSettlementId'] = key
    elif i == 4:
        event['roundId'] = 'RF9-NS-A:round:2'
        event['roundOrdinal'] = 2
    else:
        event['qualification']['copiedCounter'] = True
    after, result = settle(state, event)
    check('Independent malformed-input probe: ' + name, after == state and result['status'] == 'rejected-invalid-receipt-input' and result['creditedRP'] == 0)
    probes.append({'name': name, 'before': state, 'sourceOutcome': event, 'computedAfter': after, 'computedResult': result})

affected = read(P / 'AFFECTED_CASES.json')['cases']
reduced = deepcopy(model)
for k in ('id', 'recordedAtUtc', 'status'):
    reduced[k] = original[k]
del reduced['arcaneFeedbackReceiptFollowthrough']

def states(branch):
    yield 'initialState', branch['initialState']
    for i, step in enumerate(branch['timeline']):
        yield 'timeline/' + str(i) + '/before', step['before']
        yield 'timeline/' + str(i) + '/after', step['after']
    yield 'finalState', branch['finalState']

for index, case in enumerate(affected):
    branch = case['completeAfter']
    check(case['caseId'] + ': full before matches original MODEL', case['completeBefore'] == at(original, case['modelPointer']))
    check(case['caseId'] + ': full after matches successor MODEL', branch == at(model, case['modelPointer']))
    binding = branch['feedbackReceiptBinding']
    owner = binding['owner']
    diag = cases[0 if index == 0 else 5]
    timeline_index = binding['awardedTimelineIndex']
    event_state = branch['timeline'][timeline_index]['after']
    actor = event_state['actors'][owner]
    projection = {'ownerId': owner, 'numberedRoundContext': event_state['numberedRoundContext'], **{k: deepcopy(actor[k]) for k in ('rp', 'maxRP', 'action', 'reaction', 'recharge', 'limitedUses')}}
    check(case['caseId'] + ': complete positive diagnostic projection matches actual branch', projection == diag['after'])
    counter = event_state['castRecords'][binding['originalCounterCastId']]
    negated = event_state['castRecords'][binding['originalNegatedCastId']]
    check(case['caseId'] + ': actual counter belongs to owner and resolved using Reaction', counter['owner'] == owner and counter['state'] == 'resolved' and counter['actualBudgetSpent'] == 'reaction')
    check(case['caseId'] + ': target actual native counter outcome', negated['state'] == 'countered')
    check(case['caseId'] + ': native source/time binding', counter['nativeSourceRef'] == diag['sourceOutcome']['nativeCounterSourceRef'] and counter['paidAt'] == diag['sourceOutcome']['settledAt'])
    payment = diag['premise']['nativePayment']
    check(case['caseId'] + ': payment64 minus actual fee plus1', counter['quote']['total'] == payment['cost'] and payment['beforeRP'] == 64 and 64 - counter['quote']['total'] == payment['afterPaymentRP'] == diag['before']['rp'] and actor['rp'] == payment['afterPaymentRP'] + 1)
    stripped = deepcopy(branch)
    del stripped['feedbackReceiptBinding']
    for name, state in states(stripped):
        check(case['caseId'] + '/' + name + ': explicit same numbered-round marker', state['numberedRoundContext'] == diag['before']['numberedRoundContext'])
        current_ledger = state['actors'][owner]['limitedUses'][FEATURE]
        completed = name == 'finalState' or (name.startswith('timeline/') and (int(name.split('/')[1]) > timeline_index or (int(name.split('/')[1]) == timeline_index and name.endswith('/after'))))
        expected_ledger = diag['after' if completed else 'before']['limitedUses'][FEATURE]
        check(case['caseId'] + '/' + name + ': full pre/post ledger correctly propagated', current_ledger == expected_ledger)
        del state['numberedRoundContext']
        del state['actors'][owner]['limitedUses'][FEATURE]
    check(case['caseId'] + ': stripping only explicit new fields reproduces whole old branch', stripped == case['completeBefore'])
    parent_pointer, leaf = case['modelPointer'].rsplit('/', 1)
    at(reduced, parent_pointer)[int(leaf)] = stripped
check('Entire original MODEL reproduced after stripping only2 receipt annotations and3 metadata replacements', reduced == original and encode(reduced) == (OLD / 'MODEL.json').read_bytes())
check('All7 main cases and28 branches retained', len(model['currentVectors']) == 7 and sum(len(x['independentBranches']) for x in model['currentVectors']) == 28)
check('All3 full records unchanged', model['records'] == original['records'] and len(model['records']) == 3)
holds = read(P / 'HOLD_REGISTER.json')
check('Full hold register retained byte-exact', (P / 'HOLD_REGISTER.json').read_bytes() == (OLD / 'HOLD_REGISTER.json').read_bytes())
check('Four conditional branches remain qualified', len(holds['caseSpecificConditionalBranches']) == 4 and all(x['disposition'] == 'CONDITIONAL_EXTERNAL_PREMISE' for x in holds['caseSpecificConditionalBranches']))
whole_holds = ['IN6-09-A', 'IN6-09-B', 'EN5-01-A', 'EN5-01-B', 'EN6-03-B']
check('Five whole-positive-case holds retain source prerequisites', [x['id'] for x in holds['holds'] if x['status'] == 'RETAIN_WHOLE_POSITIVE_CASE_HOLD'] == whole_holds)
check('Second-counter ordinary5RP fixture disclosed conditional', cases[11]['premise']['status'] == 'CONDITIONAL_NATIVE_TRANSACTION_INPUT' and cases[11]['sourceOutcome']['nativeCounterSourceRef'] == 'catalog#/spells/38/operational' and cases[11]['before']['rp'] == cases[0]['after']['rp'] - 5)
check('Own START refreshes Reaction without clearing Feedback', cases[10]['before']['reaction'] is True and cases[10]['after']['limitedUses'][FEATURE] == cases[0]['after']['limitedUses'][FEATURE])
check('Round boundary alone gives no Reaction', cases[4]['after']['reaction'] is False and cases[9]['after']['reaction'] is False)
check('Old awarded and denied receipts survive later round', cases[4]['after']['limitedUses'] == cases[0]['after']['limitedUses'] and cases[13]['after']['limitedUses'] == cases[11]['after']['limitedUses'])
check('New round requires genuine new native counter and payment', cases[14]['sourceOutcome']['counterCastId'] != cases[0]['sourceOutcome']['counterCastId'] and cases[14]['before']['rp'] == cases[11]['after']['rp'] - 3 and cases[14]['after']['rp'] == 55 and len(cases[14]['after']['limitedUses'][FEATURE]['roundUses']) == 2)
check('Zero-credit cases select no new frequency-spend policy', all(cases[i]['result']['zeroAwardFrequencyPolicySelected'] is False and cases[i]['before'] == cases[i]['after'] for i in (24, 26)))

report = {
    'id': 'RANK9-RESONANCE-FIELDS3-RECEIPT-SEMANTIC-RECONCILIATION-90',
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS_BOUNDED_AUTHORED_SEMANTIC_RECONCILIATION',
    'sourceBindings': [info(P / 'MODEL.json'), info(OLD / 'MODEL.json'), info(P / 'FEEDBACK_RECEIPT_CONTRACT.json'), info(P / 'FEEDBACK_DIAGNOSTICS.json'), info(P / 'AFFECTED_CASES.json'), info(P / 'SOURCE_EVIDENCE.json'), *[info(P / s['completeFile']) for s in sources['sources']], info(P / 'sources/ordinary_counterspell_complete_record.json')],
    'priorSemanticReview': info(A / 'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json'),
    'priorIndependentReconstruction': info(A / 'RANK9_RESONANCE_FIELDS3_INDEPENDENT_RECONSTRUCTION_85.json'),
    'completedIntake': info(A / 'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json'),
    'checks': checks, 'passed': len(checks), 'failed': 0,
    'completeDiagnosticComparisons': computed, 'caseCount': len(computed),
    'additionalMalformedStateProbes': probes, 'additionalProbeCount': len(probes),
    'dischargedFindings': prior['openFindings'],
    'conclusion': 'Both previously missing spent-use derivations now have explicit immutable source receipts and authoritative original-round pointers. Native outcomes and both1RP awards are unchanged. All31 full diagnostic after-states independently reproduced. Six additional malformed-state probes reject without new RP. Full source and whole-model comparisons preserve the earlier3099-check review with no other gameplay delta.',
    'retainedQualifications': [
        'The two real positive cases retain64-3+1=62 and64-1+1=64. Native Counterspell, Counterpulse, other budgets, history, effects and geometry remain exact.',
        'Second same-round ordinary counter requires actual earlier preparation and complete native eligibility; it is a conditional reward-only projection. Own START refresh and later native cooldown/payment are supplied fixture facts, not a new scheduler.',
        'Zero-credit at full maximum or under a prohibition makes no new unused-frequency-consumption selection. These are nonaward projections, not a global recovery decision.',
        'Extra-turn and field-reentry examples test unchanged reward/source state only; no complete extra-turn or geometry operation executes.',
        'Actual native provenance authentication, authoritative cadence mapping, durable atomic storage, crash recovery and engine integration remain unimplemented.',
        'Only RF9-LOCAL-SEMANTIC-ACCEPTANCE is eligible to be discharged by the separate exact acceptance record. All other holds and all four conditional branches remain.'
    ],
    'retainedWholePositiveCaseHolds': whole_holds,
    'canonicalImplementationApplied': False, 'ownerImplementationReservationRetained': True,
    'downloadedCodeExecuted': False, 'runtimeTestsExecuted': 0, 'humanPlaytests': 0,
    'balanceApproval': False, 'cosmologyDecisions': 0, 'wholeGameComplete': False,
    'sourceInformationDeleted': 0, 'appliedCountsUnchanged': [525, 323, 249, 173],
    'exactAuthoredAcceptanceRecordedSeparately': True,
}
with SAVED.open('xb') as stream:
    stream.write(Path(__file__).read_bytes())
report['independentDiagnosticScript'] = info(SAVED)
with OUT.open('xb') as stream:
    stream.write(encode(report))
print(json.dumps({'report': info(OUT), 'passed': len(checks), 'failed': 0, 'cases': len(computed), 'additionalProbes': len(probes)}, indent=2))
