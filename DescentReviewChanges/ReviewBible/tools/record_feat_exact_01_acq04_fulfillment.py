"""Record ACQ-04 fulfillment and the complete partial-prerequisite identity map."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
from record_feat_exact_01_acq03_fulfillment import read, info, write_new

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ04_SOURCE_AND_CHAINS.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ04_FULFILLMENT.json'
    receipt_path = A / 'FEAT327_ACQ_04_FINITE_FULFILLMENT.json'
    index_path = A / 'FEAT_EXACT_01_PARTIAL_PREREQUISITE_COVERAGE_INDEX.json'
    delta_path = A / 'FEAT327_ACQ_04_FULFILLMENT_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat327-acq04-fulfillment'
    assert all(not p.exists() for p in [target, receipt_path, index_path, delta_path, preservation])
    behavior_path = A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_CHECK.json'
    companion_path = A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_CHECK.json'
    source_path = A / 'FEAT327_ACQ_04_INDEPENDENT_DESCENDANT_CHECK.json'
    behavior, companion, source = map(read, [behavior_path, companion_path, source_path])
    operations = read(A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json')
    for report, count in [(behavior, 524), (companion, 110), (source, 161)]:
        assert report['checks'] == count and not report['failures'] and all(x['passed'] for x in report['results'])
        for binding in report.get('sourceBindings', []) + report.get('fixtureBindings', []):
            assert info(G / binding['path']) == binding
    assert behavior['counts']['acceptanceGroups'] == 16 and len(behavior['groups']) == 16 and all(behavior['groups'].values())
    assert len(behavior['cases']) == 140 and len(behavior['fixtureBindings']) == 263
    for change in operations['changes']:
        assert info(G / change['after']['path']) == change['after']
        assert info(G / change['before']['preservedCopy'])['sha256'] == change['before']['sha256']
    # Reconcile actual IDs from every disjoint evidence cohort, not just totals.
    cohorts = []
    def cohort(name, count, field=None, selector=None, fixed=None):
        path = A / name; report = read(path)
        assert not report['failures']
        ids = set(fixed) if fixed is not None else set(report[field]) if selector is None else {x[selector] for x in report[field]}
        assert len(ids) == count, (name, len(ids))
        cohorts.append({'report': info(path), 'ids': sorted(ids), 'count': count})
    cohort('FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json', 209, 'coverage', 'id')
    cohort('FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json', 12, 'acquisitions', 'featId')
    cohort('FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json', 48, 'caseTraces', 'featId')
    cohort('FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json', 10, 'cohortIds')
    cohort('FEAT_EXACT_01_LINEAGE_PREREQUISITE_CHECK.json', 13, 'cohort')
    cohort('FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_CHECK.json', 34, 'cohort')
    cohort('FEAT_EXACT_01_TINKERING_PROGRESSION_CHECK.json', 1, fixed=['tinker_adept'])
    cohort('FEAT_EXACT_01_REMAINING_OWNED_CHAINS_CHECK.json', 3, 'cohort')
    cohort(behavior_path.name, 4, fixed=read(A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json')['dispositions'])
    cohort(companion_path.name, 1, fixed=['companion_training'])
    canonical = {x['id'] for x in read(A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
    covered = set(); index = []
    for group in cohorts:
        assert not covered.intersection(group['ids'])
        covered.update(group['ids'])
        index.extend({'id': sid, 'partialPrerequisiteEvidence': group['report'], 'completeAcquisitionClaimed': False} for sid in group['ids'])
    assert covered == canonical and len(covered) == 335
    write_new(index_path, {'recordedAtUtc': now, 'status': 'all335-identities-accounted-for-in-disjoint-partial-prerequisite-evidence',
        'cohorts': cohorts, 'identities': sorted(index, key=lambda x: x['id']), 'uncoveredIdentities': [],
        'counts': {'partialPrerequisiteIdentities': 335, 'disjointCohorts': 10, 'completeAcquisitionsEstablishedByThisIndex': 0},
        'scope': 'Identity accounting only. Each bound report retains its explicit positive/negative/conditional/source-history limits. No old report is rerun or silently upgraded to complete-acquisition evidence.',
        'remaining': ['All mandatory acquisition selections and relevant field initialization', 'All FXC resource/use/casting/command/clock requirements',
            'All original660-case premises and broader scenario coverage', 'Actual assembled exact-candidate review'],
        'fullFeatCandidateApproved': False})
    decision = read(A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json')
    write_new(receipt_path, {'recordedAtUtc': now, 'id': 'FEAT327-ACQ-04',
        'status': 'fulfilled-named-source-and-sixteen-finite-acceptance-groups',
        'actualGptDecision': info(A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json'), 'replyMessageId': decision['replyMessageId'],
        'derivedOperations': info(A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json'), 'independentSourceVerification': info(source_path),
        'behavioralAcceptance': info(behavior_path), 'readerNotes': info(A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_NOTES.md'),
        'checks': {'independentSource': 161, 'behavioralAndSourceControls': 524, 'failures': 0, 'namedAcceptanceGroups': 16, 'recordedCases': 140},
        'currentDescendants': [x['after'] for x in operations['changes']], 'newPolicyFile': operations['newFiles'][0],
        'limits': behavior['limits'], 'onlyThisNamedIssueClosed': True, 'finiteBehavioralAcceptanceComplete': True,
        'candidateReadyForSubmission': False, 'candidateExactApproved': False, 'wholeGameFlowApproved': False,
        'runtimeImplemented': False, 'humanPlaytestApproved': False, 'campaignRecordsAuthenticated': 0,
        'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False,
        'historicalPendingRecordsPreserved': [info(previous), info(A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json'), info(source_path)]})
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    scope = ('ACQ-04 finite fulfillment is complete:161 independent source checks and524 source/behavioral controls across all16 named groups and140 recorded cases. '
        'All263 immutable world records are explicitly conditional; no campaign-positive credential or new class/lineage/deity/plane is claimed. '
        'A separate companion pass has110 checks and30 histories, including four successful initial-body/bond/payment histories. '
        'All335 canonical identities now have disjoint finite partial prerequisite evidence, with no missing identity. '
        'This does not complete335 acquisitions, mandatory choices, original660 cases, use procedures or exact-candidate review.')
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [behavior_path, companion_path, receipt_path, index_path])
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'FEAT327-ACQ04-FULFILLMENT-AND-335-PARTIAL-IDENTITIES',
            'recordedAtUtc': now, 'partialPrerequisiteIdentities': 335, 'missingPrerequisiteIdentities': 0,
            'acq04FiniteAcceptanceComplete': True, 'full335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve330/5 and pending ACQ04 acceptance before finite fulfillment and last companion predicate pass.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = ('All335 original identities are mapped to disjoint finite partial prerequisite evidence. '
                'No remaining identity is omitted, but complete acquisition coverage is unfinished. '
                'Prodigy still needs ordered skill/tool/language/Expertise selections; audit every other mandatory choice and initial field. '
                'Animal Companion evidence covers successful completed initial bonds only: settle live attempt/payment timing, interruption and transfer/rebond meaning before claiming its full operational acquisition/use. '
                'ACQ-04 itself is fulfilled with161 source and524 behavioral/source checks; do not request an unchanged preliminary re-review. '
                'Full335 selections, resources, use procedures, original660 examples and assembled exact review remain open.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT327_ACQ_04_SOURCE_AND_CHAINS_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT327_ACQ_04_FULFILLMENT_COVERAGE_DELTA.json",')
    anchor = '        ("External credentials — sixteen acceptance groups to execute", "feat327-acq04-source/ACQ04_ACCEPTANCE_CASES.json"),'
    assert text.count(anchor) == 1
    replacement = anchor.replace('sixteen acceptance groups to execute', 'sixteen authored acceptance expectations')
    for label, filename in [('External credentials — finite fulfillment', receipt_path.name),
        ('External credentials — recorded acceptance cases', behavior_path.name),
        ('External credentials — scope and limits', 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_NOTES.md'),
        ('Animal Companion — acquisition histories', companion_path.name),
        ('Animal Companion — scope and remaining use work', 'FEAT_EXACT_01_COMPANION_ACQUISITION_NOTES.md'),
        ('All335 feats — partial prerequisite evidence index', index_path.name)]:
        replacement += '\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(filename) + '),'
    text = text.replace(anchor, replacement)
    anchor = 'The old numeric/history/Warrior reports retain their original input bindings;'
    assert text.count(anchor) == 1
    text = text.replace(anchor, scope + ' ' + anchor)
    compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        binding = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        saved.append({**binding, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta_path, {'recordedAtUtc': now, 'status': 'verified-scoped-coverage-update',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(p) for p in [behavior_path, companion_path, receipt_path, index_path]],
        'previousCoverageDelta': info(A / 'FEAT327_ACQ_04_SOURCE_AND_CHAINS_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'missingPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    result = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        print(result.stderr); raise SystemExit(result.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks']
    state = read(previous)
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress', 'previousGoalTurnClassification': 'progress: actual ACQ04 source adoption, three paid chains and owner-direction reconciliation',
        'previousCheckpoint': info(previous), 'status': scope,
        'featACQ04FiniteFulfillment': info(receipt_path), 'featCompanionAcquisition': {'report': info(companion_path), 'checks': 110, 'histories': 30},
        'partialPrerequisiteIdentityIndex': info(index_path), 'partialPrerequisiteIdentitiesCurrent': 335, 'remainingCredentialIdentitiesCurrent': [],
        'activeGptReview': {'id': 'FEAT327-ACQ-04', 'status': 'completed-source-and-finite-acceptance-fulfillment',
            'replyReceived': True, 'replyMessageId': decision['replyMessageId'], 'chatUrl': decision['chatUrl'], 'browserId': decision['browserId'], 'tabId': decision['tabId'],
            'fulfillment': info(receipt_path), 'pendingResponse': False, 'noUnchangedResubmissionRequired': True, 'wholeExactCandidateApproved': False},
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path)})
    state['safeNextActions'] = [
        'ACQ-04 is fulfilled locally; do not resend that unchanged question. All335 IDs have disjoint partial prerequisite evidence. Full acquisition choices and use validation remain unfinished.',
        'Confer narrowly on Animal Companion live purchase/initial bond attempt timing, interrupted attempts, and the source phrase new paid acquisition on transfer versus nonrepeatability. The completed-hour evidence does not settle those operating boundaries; preserve it without claiming refund semantics.',
        'Complete Prodigy ordered new skill, profiled tool, eligible language/mode and skill Expertise choices, then systematically finish other mandatory choices/initialization before full335 acquisition acceptance.',
        'Continue FXC-04–10 resource/recovery, real clocks, actual damage/resource causality, command/custody, casting/copy and all660 original case premises. Then obtain the actual assembled exact candidate review.',
        'Carry forward owner CRPG/expedition invariants and all reviewed scopes. Final actual joint whole-game flow precedes authorized GitHub push, remote verification, careful cosmology and preservation-based cleanup; software implementation remains later.',
    ]
    state.setdefault('preservationManifests', []).append(info(manifest))
    write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'fulfillment': info(receipt_path), 'identityIndex': info(index_path),
        'coverage': info(ledger_path), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
        'partialIdentities': 335, 'fullAcquisitionsComplete': False}, indent=2))


if __name__ == '__main__':
    main()
