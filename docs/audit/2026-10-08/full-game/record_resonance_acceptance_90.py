"""One-shot exact authored acceptance and checkpoint; canonical implementation stays untouched."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json, hashlib

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'rank9-resonance-fields3-feedback-receipt-return-02'
PRE = A / 'ACTIVE_AUTHORING_CHECKPOINT_HEALING_BESTIARY_DISPATCH_89.json'
OUT = A / 'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_ACCEPTANCE_90.json'
CHECK = A / 'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_ACCEPTANCE_90_CHECK.json'
ACCEPT = A / 'RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json'
ACK = A / 'CODEX_RESONANCE_ACCEPTANCE_FOLLOWUP_90.txt'
OBS = A / 'PERTINENT_NOTEBOOK_RECHECK_90.json'
BACKUP = A / 'navigation-before-resonance-acceptance-90'
SAVED = A / Path(__file__).name
for path in (OUT, CHECK, ACCEPT, ACK, OBS, BACKUP, SAVED):
    assert not path.exists(), str(path)

def j(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

def info(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def put(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)

checks = []
def check(name, condition):
    checks.append({'check': name, 'pass': bool(condition)})
    assert condition, name

prior = j(PRE)
cp = deepcopy(prior)
review_path = A / 'RANK9_RESONANCE_FIELDS3_RECEIPT_SEMANTIC_RECONCILIATION_90.json'
review = j(review_path)
model = j(P / 'MODEL.json')
index = j(G / prior['currentAuthoredIndex']['path'])
check('Prior checkpoint89 exact', info(PRE)['sha256'] == 'e06e49931bfa3db6df69c894d57c599b5130265745f77a92fddd74559c15e05c')
check('Fresh bounded semantic review236 checks all passed', review['passed'] == 236 and review['failed'] == 0 and all(x['pass'] for x in review['checks']))
check('All31 returned cases plus6 additional probes', review['caseCount'] == 31 and review['additionalProbeCount'] == 6)
check('Exactly two earlier receipt findings discharged', len(review['dischargedFindings']) == 2)
check('No runtime/canonical integration implied', not review['canonicalImplementationApplied'] and review['runtimeTestsExecuted'] == 0 and not review['downloadedCodeExecuted'])
for row in [prior['currentAuthoredIndex'], prior['currentAcceptedInterfaceRegistry'], prior['currentWorkQueue'], *prior['canonicalHelperBaselinesUnchanged']]:
    check('Canonical baseline exact: ' + row['path'], info(G / row['path']) == row)
identities = [row['spellId'] for row in model['records']]
check('Exact three intended identities', identities == ['arc-furnace', 'resonance-singularity', 'resonance-nexus-supreme'])
entries = [row for row in index['entries'] if row['id'] in identities]
check('Three still-pending canonical records preserved', len(entries) == 3 and all(row['authoredStatus'] == 'pending-authored-procedure' for row in entries))
check('Prior accepted-but-unapplied count50', prior['acceptedButUnapplied'] == 50)
check('All7main28branch4conditional coverage retained', len(model['currentVectors']) == 7 and sum(len(row['independentBranches']) for row in model['currentVectors']) == 28 and len(j(P / 'HOLD_REGISTER.json')['caseSpecificConditionalBranches']) == 4)
check('Actual GPT final preserved', '83cafb84-ba74-462c-ac6e-0b45563d11d5' in (A / 'GPT_RESONANCE_RECEIPT_COMPLETE_NATIVE_89.json').read_text(encoding='utf-8'))
check('Bestiary still actively generating at saved observation', 'button "Stop"' in (A / 'GPT_BESTIARY_ACTIVE_OBSERVATION_90.txt').read_text(encoding='utf-8'))
check('No sealed-content or cosmology approval', review['cosmologyDecisions'] == 0)

acceptance = {
    'id': 'RANK9-RESONANCE-FIELDS3-PART5-EXACT-AUTHORING-ACCEPTANCE-90',
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'status': 'EXACT_AUTHORED_SUCCESSOR_ACCEPTED_WITH_DISCLOSED_QUALIFICATIONS_NOT_APPLIED',
    'scope': 'Exact three-spell authored successor accepted after the original two Feedback spent-use findings were reconciled by immutable counter-source receipts and numbered-round pointers. This acceptance preserves full original benefit/procedure scope and all conditional prerequisites. Engine implementation, human gameplay, balance, cosmology and release remain separate.',
    'selectedSuccessor': info(P / 'MODEL.json'),
    'archive': info(A / 'DD_Rank9_Resonance_Fields_3_Part5_Feedback_Receipt_Return_02.zip'),
    'retainedCompleteHistoryArchive': info(A / 'DD_Rank9_Resonance_Fields_3_Part5_Conference_Return_01.zip'),
    'localSemanticReview': info(review_path),
    'localPreservation': info(A / 'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json'),
    'priorSemanticReview': info(A / 'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json'),
    'priorIndependentReconstruction': info(A / 'RANK9_RESONANCE_FIELDS3_INDEPENDENT_RECONSTRUCTION_85.json'),
    'actualGptFinal': info(A / 'GPT_RESONANCE_RECEIPT_COMPLETE_NATIVE_89.json'),
    'actualAssistantTurn': '83cafb84-ba74-462c-ac6e-0b45563d11d5',
    'identities': identities, 'identityCount': 3,
    'selectedCaseCount': 7, 'selectedBranchCount': 28, 'conditionalBranchCount': 4,
    'fullProcedures': 3, 'selectedSharedRules': 6, 'selectedQuestionDispositions': 24,
    'holdRegister': info(P / 'HOLD_REGISTER.json'),
    'dischargedLocalHold': 'RF9-LOCAL-SEMANTIC-ACCEPTANCE only. The unmodified returned register remains historical; this later exact acceptance supersedes that local-review status alone.',
    'retainedWholePositiveCaseHolds': review['retainedWholePositiveCaseHolds'],
    'retainedQualifications': review['retainedQualifications'],
    'newAcceptedButUnappliedIdentities': 3,
    'previousAcceptedButUnapplied': 50, 'resultingAcceptedButUnapplied': 53,
    'appliedCountsUnchanged': {'reviewed': 525, 'pending': 323, 'standalone': 249, 'interfaces': 173, 'total': 848},
    'sourceInformationDeleted': 0, 'canonicalFilesChanged': 0, 'implementationApplied': False,
    'ownerImplementationReservationRetained': True, 'downloadedCodeExecuted': False,
    'runtimeTestsExecuted': 0, 'humanPlaytests': 0, 'balanceApproval': False,
    'cosmologyApproval': False, 'wholeGameComplete': False, 'releaseApproval': False,
    'requiredLaterIntegration': 'Await the owner-reserved implementation path. Use the exact Return02 MODEL and complete current artifacts with both full historical input archives. Choose one alternative reconstruction path; do not apply both. Preserve all-magic scope, actual paid costs/principals, source attribution, atomic recovery receipts, genuine native counter qualification, original numbered rounds, all conditional branches and retained holds. No unused zero-award frequency policy is selected here.'
}

ack = f'''Independent Resonance Fields3 Feedback Return02 reconciliation is complete. I read the full receipt contract, all31 complete diagnostic cases and the affected complete branches, and cross-checked the actual full Wizard/class/casting/combat sources and ordinary Counterspell record. My own standard-library review passed236 checks, independently reproduced all31 full after-states, and added six malformed-state probes that reject without minting RP. No returned code was run or imported.

Report: {review_path.name}, {info(review_path)['bytes']} bytes, SHA256 {info(review_path)['sha256']}.

I accept the exact authored successor for Arc Furnace, Resonance Singularity and Resonance Nexus (Supreme): MODEL5129434bytes SHA2565b02270f39fce01c392b6e8187ce9e144f06957d908140c5c18cf96f1e78952a, archive56617127bytes SHA256608c2943bcd976c67a5e80848dd23f635cd813f21f6169342ef29f910c8ca9ab. Removing only the new receipt fields and restoring the three metadata values reproduces the entire previous MODEL byte-exactly, preserving the prior3099-check semantic review. The233-check full intake and complete historical archives remain bound.

Both original awards remain64-3+1=62 and64-1+1=64. The immutable source key prevents replay after renamed callbacks, JSON reload and a new round. A separately refreshed Reaction does not clear Feedback's original-round use. A distinct valid new-round counter may award1 only after its own actual native payment and permissions. All native costs, Counterpulse, other budgets, casting histories, field benefits and effects remain exact.

The same-round second ordinary counter remains conditional on actual prior preparation and all native permissions; the reward projection does not execute that native transaction. Extra-turn/reentry cases are boundary projections, not full world operations. Capped-zero and prohibited-recovery cases select no new unused-frequency-spend convention. Actual source authentication, cadence adapters, atomic durable storage and game-engine integration remain unimplemented.

All7 main cases,28 branches, four conditional branches and five whole-positive-case holds survive. Only RF9-LOCAL-SEMANTIC-ACCEPTANCE is discharged by {ACCEPT.name}; every other hold remains. Applied525/323/249/173 is unchanged. Accepted-but-unapplied ordinary spell identities increase50 to53. Parent335 is still pending; no canonical implementation, runtime testing, human gameplay, balance, cosmology or release approval occurred.

This acknowledgment is prepared locally while the already-submitted Bestiary V3/current EX58 review is generating. It must not be inserted by interrupting that response. Send at the next safe conference opportunity, along with any then-current follow-through needed; the Bestiary source archives are already submitted and must not be resent merely because historical preparation files say unsent.
'''

observation = {
    'id': 'PERTINENT-NOTEBOOK-RECHECK-90', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'calibrationThread': '6ad4a867-f330-83e9-829e-bf2bb41a6c09',
    'calibrationTitle': 'Calibration Review Part 5',
    'freshNativeLatestUserTurn': '5395ae3e-01ef-4b42-bae4-9c17af13f3fb',
    'freshNativeLatestCompletedAssistant': '83cafb84-ba74-462c-ac6e-0b45563d11d5',
    'nativeStatusCaution': 'Native read reports idle with no completed response for the latest Bestiary turn; live browser Stop/Analyzing establishes generation is still active.',
    'browserObservation': info(A / 'GPT_BESTIARY_ACTIVE_OBSERVATION_90.txt'),
    'bestiaryAlreadyDispatched': prior['bestiaryActualDispatch89'],
    'unityThread': '6ad64114-2364-83e9-8764-bc55988b0479',
    'unityTitle': 'Unity Development Setup',
    'freshUnityLatestUser': '41d5797f-d115-4cce-90fd-8ccc835b86cb',
    'freshUnityLatestAssistant': 'b0572b7f-e15c-4d11-8353-86853e0329c6',
    'unityComparison': 'Unchanged from already preserved full development directions and current decision ledger; no newly issued Unity decision in this recheck.',
    'newLocalResult': 'Resonance receipt review now passes236 independent checks; exact3-spell authored acceptance recorded separately. GPT acknowledgment prepared but unsent while Bestiary is generating.',
    'implementationApplied': False, 'cosmologyDecisions': 0
}

cp['id'] = 'ACTIVE-AUTHORING-RESONANCE-ACCEPTANCE-90'
cp['recordedAtUtc'] = datetime.now(timezone.utc).isoformat()
cp['previousCheckpoint'] = info(PRE)
cp['status'] = 'Exact authored acceptance of Resonance Fields3 after236 independent receipt checks,31 complete diagnostic cases and6 additional invalid-state probes. Accepted-unapplied53; applied525/323/249/173 unchanged. GPT continues the already-submitted full Bestiary conference.'
cp['previousGoalTurnClassification'] = {'turn': 89, 'classification': 'progress', 'evidence': info(PRE)}
cp['acceptedButUnapplied'] = 53
cp['previousResonanceSemanticObservationBefore90'] = prior['currentResonanceFields3SemanticReview']
current = cp['currentResonanceFields3SemanticReview']
current['historicalOpenFindingsBefore90'] = deepcopy(current['openFindings'])
current['openFindings'] = []
current['independentExactAcceptance'] = True
current['receiptReconciliation90'] = info(review_path)
current['receiptCheckCount90'] = 236
current['findingDisposition90'] = 'Both original Feedback missing-spent-use findings discharged by the exact Return02 receipt model. Original86 findings/report retained as history; all external/runtime/balance holds remain.'
current['dispatchStatus'] = 'The historical prepared86 request was actually sent87 and completed89; receipt semantic review passed90. Do not resend based on original UNSENT label.'
receipt = cp['completedResonanceReceiptReturn02']
receipt['full31DiagnosticSemanticReviewComplete'] = True
receipt['exactAuthorshipAccepted'] = True
receipt['semanticReview90'] = info(review_path)
receipt['semanticCheckCount90'] = 236
receipt['canonicalApplied'] = False
receipt['nextReview'] = 'Complete source review accepted with retained qualifications; acknowledge to GPT after active Bestiary response completes. Future actual engine integration remains owner-reserved.'
cp['currentResonanceExactAcceptance90'] = {'path': ACCEPT.relative_to(G).as_posix(), 'bytes': len(encode(acceptance)), 'sha256': hashlib.sha256(encode(acceptance)).hexdigest()}
cp['resonanceAcceptanceAcknowledgment90'] = {'path': ACK.relative_to(G).as_posix(), 'bytes': len(ack.encode()), 'sha256': hashlib.sha256(ack.encode()).hexdigest(), 'actuallySent': False, 'reason': 'Bestiary generation active; do not interrupt.'}
cp['pertinentNotebookRecheck90'] = {'path': OBS.relative_to(G).as_posix(), 'bytes': len(encode(observation)), 'sha256': hashlib.sha256(encode(observation)).hexdigest()}
cp['previousGptObservationBefore90'] = prior['activeGptReviewAtLastVerifiedObservation']
cp['activeGptReviewAtLastVerifiedObservation']['latestObservation90'] = info(A / 'GPT_BESTIARY_ACTIVE_OBSERVATION_90.txt')
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus'] = 'Browser still has Stop and Analyzing while reading bestiary source/workbook/dependencies; no final Bestiary response observed. Do not interrupt or resend.'
cp['bestiaryActualDispatch89']['latestObservation90'] = info(A / 'GPT_BESTIARY_ACTIVE_OBSERVATION_90.txt')
cp['nextAction'] = 'Preserve active GPT Bestiary generation and independently advance remaining parent335 physical/social/world-copy and exact semantic gates. When GPT completes, preserve the full return and inspect it before canonical decisions; then actually send the prepared Resonance acceptance acknowledgment. The healing89 packet remains local and not submitted for parent335 acceptance. Do not rerun successful diagnostics; retain53 accepted-unapplied spells and all holds.'
cp['laterLocalWork'] = 'Checkpoints73–90 remain local after the last separately verified GitHub backup through72; no push in90.'
cp['lastUsageObservation'] = {'usedPercent': 51, 'remainingPercent': 49, 'resetsAt': 1793110625, 'stopAtRemainingPercent': 20, 'source': 'Fresh get_usage_limits during90'}

nav = [G / 'START_HERE.md', G / 'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md', G / 'REVIEW_MAP.html']
before, prepared = {}, {}
for path in nav:
    baseline = next(x for x in prior['navigation'] if x['path'] == path.relative_to(G).as_posix())
    check('Earlier navigation exact: ' + path.name, info(path) == baseline)
    raw = before[path] = path.read_bytes()
    if path.suffix == '.html':
        pos = raw.find(b'>', raw.find(b'<body')) + 1
        note = ('<aside><p><strong>Checkpoint90:</strong> Arc Furnace, Resonance Singularity and Resonance Nexus (Supreme) cleared exact authored review with236 new receipt checks.53 accepted-unapplied spells; applied525/323/249/173 unchanged. GPT is developing the Bestiary review. <a href="docs/audit/2026-10-08/full-game/' + OUT.name + '">Current record</a>.</p></aside>\n').encode()
    else:
        pos = raw.find(b'\n') + 1
        prefix = 'docs/audit/2026-10-08/full-game/' if path.name == 'START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
        note = ('\n**Current checkpoint — Resonance acceptance:** [Checkpoint90](' + prefix + OUT.name + ') records exact authored acceptance of Arc Furnace, Resonance Singularity and Resonance Nexus (Supreme), after236 new receipt checks.53 spell identities are accepted but unapplied; applied525/323/249/173 remains unchanged. GPT is developing the full Bestiary review. Canonical implementation and all runtime, human, balance, cosmology and release gates remain separate.\n').encode()
    check('Valid navigation insertion: ' + path.name, pos > 0)
    prepared[path] = raw[:pos] + note + raw[pos:]
    check('All previous navigation bytes retained: ' + path.name, prepared[path][:pos] + prepared[path][pos + len(note):] == raw)
check('Every prior top-level checkpoint field retained', set(prior).issubset(cp))
check('Applied counts unchanged while accepted-unapplied50to53', cp['authoredCounts'] == prior['authoredCounts'] and cp['acceptedButUnapplied'] == prior['acceptedButUnapplied'] + 3 and not cp['implementationApplied'])

put(ACCEPT, encode(acceptance))
put(ACK, ack.encode())
put(OBS, encode(observation))
BACKUP.mkdir()
cp['preservedNavigation'] = []
for path in nav:
    saved = BACKUP / path.name
    put(saved, before[path])
    cp['preservedNavigation'].append(info(saved))
    path.write_bytes(prepared[path])
cp['navigation'] = [info(path) for path in nav]
put(SAVED, Path(__file__).read_bytes())
put(OUT, encode(cp))
result = {'id': 'CHECKPOINT90-VALIDATION', 'checkpoint': info(OUT), 'acceptance': info(ACCEPT), 'checks': checks, 'passed': len(checks), 'failed': 0, 'script': info(SAVED), 'acknowledgmentActuallySent': False}
put(CHECK, encode(result))
print(json.dumps({'checkpoint': info(OUT), 'acceptance': info(ACCEPT), 'check': info(CHECK), 'passed': len(checks), 'failed': 0, 'acceptedButUnapplied': 53, 'acknowledgmentActuallySent': False}, indent=2))
