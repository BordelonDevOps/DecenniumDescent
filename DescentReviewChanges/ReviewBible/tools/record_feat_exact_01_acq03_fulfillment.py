"""Preserve and record the finite ACQ-03 source and behavioral fulfillment."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def write_new(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ03_SOURCE_APPLICATION.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ03_FULFILLMENT.json'
    receipt_path = A / 'FEAT327_ACQ_03_FINITE_FULFILLMENT.json'
    delta_path = A / 'FEAT327_ACQ_03_FULFILLMENT_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat327-acq03-fulfillment'
    assert all(not p.exists() for p in [target, receipt_path, delta_path, preservation]), 'One-use record already started'
    decision_path = A / 'FEAT327_ACQ_03_RECEIVED_DECISION.json'
    operations_path = A / 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json'
    source_path = A / 'FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json'
    behavior_path = A / 'FEAT327_ACQ_03_CASTING_CREDENTIAL_CHECK.json'
    notes_path = A / 'FEAT327_ACQ_03_CASTING_CREDENTIAL_NOTES.md'
    decision, operations, source, behavior = map(read, [decision_path, operations_path, source_path, behavior_path])
    assert decision['replyMessageId'] == '67894042-55c3-44d4-bf3a-a2f31dd1140b'
    assert source['checks'] == 175 and not source['failures']
    assert behavior['checks'] == 113 and not behavior['failures']
    assert behavior['finiteBehavioralAcceptanceComplete'] and behavior['onlyThisNamedIssueClosed']
    assert behavior['counts']['namedAcceptanceGroups'] == 8
    assert behavior['counts']['remainingCredentialDependentIdentities'] == 43
    assert len(behavior['traces']) == 18 and all(row['passed'] for row in behavior['results'])
    assert info(operations_path) == source['derivedOperations']
    for binding in behavior['sourceBindings']:
        assert info(G / binding['path']) == binding, binding['path']
    for change in operations['changes']:
        assert info(G / change['after']['path']) == change['after']
        assert info(G / change['before']['preservedCopy'])['sha256'] == change['before']['sha256']
    receipt = {
        'recordedAtUtc': now, 'id': 'FEAT327-ACQ-03',
        'status': 'fulfilled-finite-source-amendment-and-acquisition-snapshot-acceptance',
        'actualGptDecision': info(decision_path), 'replyMessageId': decision['replyMessageId'],
        'derivedOperations': info(operations_path), 'independentSourceVerification': info(source_path),
        'behavioralAcceptance': info(behavior_path), 'readerNotes': info(notes_path),
        'checks': {'independentSource': 175, 'behavioralAndSourceControls': 113, 'failures': 0,
                   'namedAcceptanceGroups': 8, 'recordedSnapshotTraces': 18},
        'currentDescendants': [change['after'] for change in operations['changes']],
        'historicalPendingRecordsPreserved': [info(previous), info(operations_path), info(source_path)],
        'scope': 'Exact two shared-wording amendments,33 existing casting-node annotations and supplementary Spell Focus binding, followed by the actual GPT A-H acquisition-snapshot expectations and finite additional controls.',
        'limits': behavior['limits'],
        'onlyThisNamedIssueClosed': True, 'finiteBehavioralAcceptanceComplete': True,
        'cumulativePartialPrerequisiteIdentities': 292, 'remainingCredentialDependentIdentities': 43,
        'newlyClosedFullFeatAcquisitions': 0, 'all335ActualAcquisitionBoundaryCasesExecuted': False,
        'candidateReadyForSubmission': False, 'candidateExactApproved': False,
        'runtimeImplemented': False, 'humanPlaytestApproved': False, 'wholeGameFlowApproved': False,
        'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False,
        'deliveryOrder': ['actual final joint whole-game flow agreement', 'authorized GitHub push', 'verified remote commit', 'careful cosmology review'],
    }
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path)
    ledger = deepcopy(before)
    changed = {'DD-06', 'DD-14', 'DD-69'}
    scope = (
        'ACQ-03 finite fulfillment is complete:175 independent source checks and113 acquisition-snapshot/source controls pass. '
        'Eighteen recorded traces execute all eight named A-H groups plus finite controls, with real paid Initiate/Pact/Spell Focus histories and explicit lawful Wizard repertoire subsets. '
        'Credential evaluation preserves resources, temporary casting prohibitions and exact school fields. No cast or complete Wizard build is claimed. '
        'Only this named acquisition-policy issue is closed. The existing292 partial prerequisite identities/43 remaining identities are unchanged; '
        'complete feat acquisitions, exact candidate approval and whole-game review remain open.')
    old_issue = (
        'ACQ-03 is received and its exact eight-file source application passes175 independent checks. '
        'Its source-qualified A-H and extra casting-snapshot behavioral acceptance cases still need execution; the named issue is not yet marked fulfilled.')
    new_issue = (
        'ACQ-03 finite fulfillment is recorded:175 source checks and113 snapshot/source controls pass across A-H and additional controls. '
        'Only that named policy issue is closed;43 credential-dependent identities and full acquisition/selection/use coverage remain outstanding.')
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('validationEvidence', []).extend([behavior_path.relative_to(G).as_posix(), receipt_path.relative_to(G).as_posix()])
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'FEAT327-ACQ-03-FINITE-FULFILLMENT', 'recordedAtUtc': now,
            'status': receipt['status'], 'fulfillment': receipt_path.relative_to(G).as_posix(),
            'behavioralAcceptance': behavior_path.relative_to(G).as_posix(),
            'supersedesPendingStatusOf': 'FEAT327-ACQ-03-SOURCE-APPLICATION',
            'onlyThisNamedIssueClosed': True, 'fullFeatCandidateApproved': False,
        })
        if row['id'] == 'DD-14':
            assert row['openIssues'][1].count(old_issue) == 1
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'reason': 'Preserve source-applied/behavior-pending wording before finite fulfillment.',
                'status': row['status'], 'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = row['openIssues'][1].replace(old_issue, new_issue)
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    nav = R / 'tools/build_review_map.py'
    text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT327_ACQ_03_SOURCE_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT327_ACQ_03_FULFILLMENT_COVERAGE_DELTA.json",')
    anchor = '        ("Casting prerequisites — independent source verification", "FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json"),'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n'
        '        ("Casting prerequisites — finite acceptance notes", "FEAT327_ACQ_03_CASTING_CREDENTIAL_NOTES.md"),\n'
        '        ("Casting prerequisites — all recorded snapshot evidence", "FEAT327_ACQ_03_CASTING_CREDENTIAL_CHECK.json"),\n'
        '        ("Casting prerequisites — finite fulfillment", "FEAT327_ACQ_03_FINITE_FULFILLMENT.json"),')
    old = '175 independent source/whole-file checks pass; A-H and additional behavioral acceptance still remain, so the named issue is not yet marked fulfilled.'
    assert text.count(old) == 1
    text = text.replace(old, '175 independent source/whole-file checks and113 snapshot/source controls pass. Eighteen traces cover A-H and the finite additional controls; only ACQ-03 is fulfilled. These conditional histories and lawful repertoire subsets are not actual casts or complete Wizard builds.')
    compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        binding = info(path)
        dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        saved.append({**binding, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'
    write_new(manifest, saved)
    write_new(receipt_path, receipt)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta_path, {
        'recordedAtUtc': now, 'status': 'verified-scoped-coverage-update',
        'before': next(row for row in saved if row['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True,
        'allClosuresAndHumanEvidenceUnchanged': True, 'previousFeatOpenIssuesPreservedVerbatim': True,
        'validation': [info(source_path), info(behavior_path)],
        'previousCoverageDelta': info(A / 'FEAT327_ACQ_03_SOURCE_COVERAGE_DELTA.json'),
        'fulfillment': info(receipt_path), 'onlyThisNamedIssueClosed': True, 'fullFeatCandidateApproved': False,
    })
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stderr)
        raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state = read(previous)
    state.update({
        'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: exact ACQ-03 source amendment applied with175 independent source checks',
        'previousCheckpoint': info(previous), 'status': scope, 'featACQ03FiniteFulfillment': info(receipt_path),
        'activeGptReview': {'id': 'FEAT327-ACQ-03', 'status': 'completed-source-decision-and-finite-local-fulfillment',
            'replyReceived': True, 'replyMessageId': decision['replyMessageId'], 'decision': info(decision_path),
            'fulfillment': info(receipt_path), 'chatUrl': decision['chatUrl'], 'browserId': '3', 'tabId': '125745639',
            'wholeExactCandidateApprovalRequested': False, 'note': 'No pending response or resubmission is needed for this fulfilled narrow question.'},
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path),
        'navigationBindingPolicy': 'Explicit preserved coverage chain through ACQ-03 finite fulfillment; exact source descendants continue through ACQ-01/02/03 measured operations. No blanket hash exemptions.',
    })
    state['safeNextActions'][0] = (
        'ACQ-03 is fulfilled by its actual GPT source decision,175 independent source checks and113 finite acquisition-snapshot controls. '
        'Do not resend or rerun immutable prior reports. The33 node annotations are not33 full acquisitions. '
        'Continue the43 remaining credential-dependent identities using actual source-bound routes and unchanged Boolean alternatives, earned payment and required choices.')
    state.setdefault('preservationManifests', []).append(info(manifest))
    write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'fulfillment': info(receipt_path), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
        'onlyThisNamedIssueClosed': True, 'remainingCredentialDependentIdentities': 43,
        'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False}, indent=2))


if __name__ == '__main__':
    main()
