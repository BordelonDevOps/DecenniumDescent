"""Register terminal GPT Flora ruling, guarded propagation and finite fulfillment."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json, shutil, subprocess, sys, zipfile
from validate_feat_exact_01_composite_casting import read, info

G = Path('C:/Github/DecenniumDescent'); R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'; V = A / 'feat335-flora-source-check-01-verdict'


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_BORROWED_TRANSACTIONS.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FLORA_FULFILLMENT.json'
    fulfillment = A / 'FEAT335_FLORA_SOURCE_CHECK_01_FINITE_FULFILLMENT.json'
    current = A / 'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA_FULFILLMENT.json'
    delta = A / 'FEAT335_FLORA_FULFILLMENT_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-feat335-flora-fulfillment'
    scope_path = A / 'FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint, fulfillment, current, delta, preservation, scope_path])
    now = datetime.now(timezone.utc).isoformat()
    archive = A / 'FEAT335_Flora_Source_Check_01_Addendum_and_Evidence.zip'
    assert archive.stat().st_size == 61058 and info(archive)['sha256'] == '3ff3d568c4008d227aef78baf33bcb3d1fc54e9abd104cd6e2a40673e01d9924'
    manifest = read(V / 'FILE_MANIFEST.json'); assert manifest['payloadCount'] == len(manifest['files']) == 12
    with zipfile.ZipFile(archive) as z:
        for name, b in manifest['files'].items():
            data = (V / name).read_bytes()
            assert len(data) == b['bytes'] and sha256(data).hexdigest() == b['sha256']
            assert data == z.read(name)
    reproduction = read(A / 'FEAT335_FLORA_SOURCE_CHECK_01_REPRODUCED.json')
    assert reproduction == read(V / 'EXECUTED_SOURCE_CHECKS.json') and reproduction['checks'] == reproduction['passed'] == 101 and reproduction['failed'] == 0
    propagation_path = A / 'FEAT335_FLORA_SOURCE_PROPAGATION_CHECK.json'
    propagation = read(propagation_path); assert propagation['checks'] == 738 and not propagation['failures']
    report_path = A / 'FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_V2_CHECK.json'
    report = read(report_path); assert report['checks'] == 189 and not report['failures'] and len(report['histories']) == 54
    assert report['counts']['receivedAcceptanceGroups'] == 18
    for binding in report['sourceBindings']: assert info(G / binding['path']) == binding
    source_delta = A / 'FEAT335_FLORA_DERIVED_OPERATIONS.json'
    for change in read(source_delta)['changes']:
        assert info(G / change['after']['path']) == change['after']
        original = G / change['before']['preservedCopy']
        assert original.stat().st_size == change['before']['bytes'] and info(original)['sha256'] == change['before']['sha256']
    response = A / 'FEAT335_FLORA_SOURCE_CHECK_01_RESPONSE_DOM.txt'
    response_text = response.read_text(encoding='utf-8')
    assert 'Response complete' in response_text and 'without another generic conference or unchanged335 resubmission' in response_text
    save(scope_path, {
        'currentModel': info(R / 'tools/feat335_flora_source_followthrough_v2.py'), 'currentReport': info(report_path),
        'historical114Report': info(A / 'FEAT335_FLORA_USE_CHECK.json'),
        'historicalQualification': info(A / 'FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json'),
        'historical186Report': info(A / 'FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_CHECK.json'),
        'supersededEarlierConclusions': [
            'Fixed-at-first-creation level10 eligibility in the original114 report is superseded by the actual GPT live-level10 completion. Its below10 original-use window now remains open until spent, first-body ending or original deadline.',
            'Provider-loss use, early first-plant ending, split command/phase and owner continuity are now governed by FLQ01–04 and exercised by the finite18 acceptance groups.',
            'Original114 extra-turn/third-body/post-Burst-body negatives were compound negatives. New cases leave unrelated resource, capacity and channel predicates valid and verify the intended rejection reason.',
            'The preserved186-check descendant covered capable Verdant-supporting plants only. Its overly narrow canAct gate is corrected in V2 with three additional positive incapacitated-but-active body cases; no game rule changes from that local correction.'],
        'resolvedScope': report['scope'], 'remainingLimits': report['limits'],
        'fourInterfacesFulfilled': ['FLQ-01', 'FLQ-02', 'FLQ-03', 'FLQ-04'],
        'fullFeatExactApproved': False, 'runtimeApproved': False, 'humanBalanceApproved': False,
        'sourceInformationDeleted': 0, 'cosmologyReviewed': False})
    save(fulfillment, {
        'recordedAtUtc': now, 'reviewId': 'FEAT335-FLORA-SOURCE-CHECK-01',
        'status': 'terminal-actual-GPT-ruling-guarded-propagation-and-finite-followthrough-fulfilled',
        'receivedArchive': info(archive), 'manifest': info(V / 'FILE_MANIFEST.json'), 'verifiedPayloads': 12,
        'actualGptResponse': info(response), 'reproduction': info(A / 'FEAT335_FLORA_SOURCE_CHECK_01_REPRODUCED.json'),
        'reproducedSourceChecks': 101, 'reproducedJsonEqualToReviewer': True,
        'lineEndingQualification': 'Local Windows stdout CRLF differs from reviewer LF bytes; decoded JSON and LF-normalized output agree. Original114 suite was not rerun by GPT.',
        'propagation': info(propagation_path), 'propagationChecks': 738, 'guardedSourceChanges': info(source_delta),
        'behavioralFollowThrough': info(report_path), 'behavioralChecks': 189, 'conditionalHistories': 54,
        'fulfilledSourceQuestions': ['FLQ-01', 'FLQ-02', 'FLQ-03', 'FLQ-04'],
        'fulfilledFiniteGroups': [g['id'] for g in read(V / 'FINITE_FLORA_EXPECTATIONS.json')['groups']],
        'scopeQualification': info(scope_path), 'noUnchangedSourceResubmissionRequired': True,
        'wholeFeatApproval': False, 'wholeGameFlowConfirmed': False, 'pushed': False, 'cosmologyReviewed': False})
    register = read(A / 'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA.json')
    register.update(recordedAtUtc=now, previousRegister=info(A / 'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA.json'),
                    floraFiniteModelFollowThroughComplete=True, floraFiniteFulfillment=info(fulfillment))
    assert register['fullFeatCandidateApproved'] is False
    save(current, register)
    state = read(previous)
    scope = ('Actual GPT FEAT335-FLORA-SOURCE-CHECK-01 is terminal and fulfilled within four named interfaces. '
        'The61058-byte archive and12 payloads are verified;101 reviewer source checks reproduce. Ten guarded direct operations and exact mirror propagation changed seven current files, preserving every prior byte and335 original records. '
        'The738 propagation checks pass. The current finite model passes189 checks across54 conditional histories covering all18 received groups: lost-provider operand retention, live level10 second-creation window, immediate first-body closure, split command/phase, owner death/incapacity continuity, same-owner trap budget and coupled Burst/Verdant predicates. '
        'Original114 and earlier186 evidence remain preserved and qualified. All four source interfaces close under GPT\'s explicit finite fulfillment path; full335 use and exact approval remain open. '
        'Current acquisition register/assembly/descriptors carry the Flora descendants. No GPT request is pending. Borrowed skill hidden-roll, full Nature casting and broader FXC04/06–10 work remain. '
        'The final joint whole-game agreement, GitHub push then careful cosmology sequence, source preservation and50-percent weekly-usage stop remain unchanged.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    old = read(ledger_path); ledger = deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] not in {'DD-14', 'DD-69'}: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [fulfillment, scope_path, report_path, propagation_path, current])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'FEAT335-Flora-FLQ01-04-fulfilled', 'recordedAtUtc': now,
            'sourceChecks': 101, 'propagationChecks': 738, 'behavioralChecks': 189, 'conditionalHistories': 54, 'fullUseRuntimeApproved': False})
        issues = []
        for issue in row['openIssues']:
            if 'FEAT335-ACQUISITION-AUDIT-01 is submitted and visibly running' in issue:
                issue = 'FEAT335-ACQUISITION-AUDIT-01, cadence and Flora source reviews are terminal and their finite follow-through is fulfilled. No request is currently pending. The final assembled feat review remains separate.'
            elif 'Receive the already sent FEAT335-FLORA-SOURCE-CHECK-01' in issue:
                issue = 'Flora FLQ01–04 and all18 received finite groups are fulfilled in FEAT335_FLORA_SOURCE_CHECK_01_FINITE_FULFILLMENT.json. Remaining Flora scope includes full ordinary damage/conditions, genuine scheduler, armed-mode identification and Verdant message/casting interfaces. Finish remaining FXC04/06–10 work before full335 exact submission.'
            elif 'all335 acquisition closure remain separate' in issue:
                issue = 'Use the current mandatory-provider acquisition model and FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_V2_CHECK.json for Flora. The old incomplete initialization and fixed-level use inference remain historical. Acquisition finite groups and Flora FLQ01–04 are fulfilled; broader full-use/assembled feat review remains open.'
            elif 'All AA01' in issue and 'acquisition-audit groups are fulfilled' in issue:
                issue = 'All AA01–18/FW01–09 finite acquisition-audit groups remain fulfilled; current register is FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA_FULFILLMENT.json. Complete remaining full-use cases/interfaces before submitting the full335 exact candidate to actual GPT. No complete runtime or full feat approval.'
            issues.append(issue)
        row['openIssues'] = issues
    for before, after in zip(old['aspects'], ledger['aspects']):
        assert all(before.get(k) == after.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if before['id'] not in {'DD-14', 'DD-69'}: assert before == after
    assert {k:v for k,v in old.items() if k != 'aspects'} == {k:v for k,v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "FEAT335_BORROWED_TRANSACTIONS_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "FEAT335_FLORA_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_FLORA_FULFILLMENT_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1; text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    new_links = [('Flora — actual GPT ruling and finite fulfillment', fulfillment),
        ('Flora —189 checks across all18 acceptance groups', report_path), ('Flora — historical qualifications and remaining scope', scope_path),
        ('Flora —738 guarded source propagation checks', propagation_path), ('Feats — current acquisition register after Flora fulfillment', current),
        ('Flora — received complete source addendum', V / 'FEAT335_FLORA_SOURCE_CHECK_01_ADDENDUM.md')]
    text = text.replace(marker, marker + ''.join('        (' + json.dumps(label) + ', ' + json.dumps(p.relative_to(A).as_posix()) + '),\n' for label,p in new_links))
    compile(text, str(nav), 'exec')
    preserved = []
    for p in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        copy = preservation / p.relative_to(G); copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, copy); assert copy.read_bytes() == p.read_bytes()
        preserved.append({**info(p), 'preservedCopy': copy.relative_to(G).as_posix()})
    save(preservation / 'PRESERVATION_MANIFEST.json', preserved)
    save(ledger_path, ledger); nav.write_text(text, encoding='utf-8', newline='\n')
    save(delta, {'recordedAtUtc': now, 'changes': [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [ledger_path, nav]],
                'sourcePropagation': info(source_delta), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0})
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations', []).append({'recordedAtUtc': now, 'supersededObservation': deepcopy(state['activeGptReview']), 'reason': 'Actual terminal Flora reply received and finite follow-through completed; no longer pending.'})
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress', status=scope,
        coverageLedger=info(ledger_path), coverageDelta=info(delta), floraSourceFulfillment=info(fulfillment),
        activeGptReview={'id': 'FEAT335-FLORA-SOURCE-CHECK-01', 'status': 'terminal-source-and-finite-followthrough-fulfilled',
            'pendingResponse': False, 'replyReceived': True, 'lastObservedStopVisible': False, 'fulfillment': info(fulfillment),
            'conversationUrl': state['activeGptReview']['conversationUrl'], 'browserId': '3', 'tabId': '125745933',
            'instruction': 'No current pending request. Flora four interfaces are fulfilled; do not resend the unchanged packet. Full feat exact review remains separate.'},
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        newRuleAdoptions=4, newRuleAdoptionCountScope='Four actual GPT Flora interface completions, implemented by10 guarded direct operations plus exact mirrors; not four whole-system approvals.')
    state['feat335CorrectionFulfillment']['currentRegister'] = info(current)
    state['featAllowanceAssembly'].update(assembly=info(A / 'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json'),
        descriptors=info(A / 'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json'), floraFiniteFulfillment=info(fulfillment))
    state['boundedFloraUse'].update(historicalScope=True, unapprovedGrowthInference=True, supersededBy=info(fulfillment),
        currentModel=info(R / 'tools/feat335_flora_source_followthrough_v2.py'), currentReport=info(report_path), currentScope=info(scope_path),
        currentChecks=189, currentHistories=54, currentSourceInterfacesFulfilled=True)
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_FLORA_FULFILLMENT. FLQ01–04 and18 groups fulfilled;189 checks/54 histories. Preserve all older reports. Use the V2 current Flora model and current register AFTER_FLORA_FULFILLMENT.',
        'No actual GPT request is pending. The Flora terminal reply explicitly permits this finite fulfillment without an unchanged repeat conference. Full assembled feat approval remains separate.',
        'Next finite work: borrowed class-skill separate declare/pay/resolve interface; then full Nature Whisper/casting and other remaining FXC04/06–10 use, physical/social, timing and authored-example cases. Do not relabel existing narrow evidence as full execution.',
        *state['safeNextActions'][-2:]]
    state.setdefault('preservationManifests', []).append(info(preservation / 'PRESERVATION_MANIFEST.json'))
    save(checkpoint, state)
    print(json.dumps({'checkpoint': info(checkpoint), 'fulfillment': info(fulfillment), 'currentRegister': info(current),
                      'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': []}))


if __name__ == '__main__': main()
