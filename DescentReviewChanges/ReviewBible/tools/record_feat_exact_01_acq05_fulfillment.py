"""Record ACQ05 finite lifecycle fulfillment without upgrading broader gates."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHOICES_AND_ACQ05_SOURCE.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ05_FULFILLMENT.json'
    receipt_path = A / 'FEAT327_ACQ_05_FINITE_FULFILLMENT.json'
    delta_path = A / 'FEAT327_ACQ_05_FULFILLMENT_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat327-acq05-fulfillment'
    assert all(not p.exists() for p in [target, receipt_path, delta_path, preservation])
    behavior_path = A / 'FEAT327_ACQ_05_LIFECYCLE_CHECK.json'
    source_path = A / 'FEAT327_ACQ_05_INDEPENDENT_DESCENDANT_CHECK.json'
    operations_path = A / 'FEAT327_ACQ_05_DERIVED_OPERATIONS.json'
    decision_path = A / 'FEAT327_ACQ_05_RECEIVED_DECISION.json'
    behavior, source, operations, decision = map(read, [behavior_path, source_path, operations_path, decision_path])
    for report, count in [(behavior, 206), (source, 272)]:
        assert report['checks'] == count and not report['failures'] and all(x['passed'] for x in report['results'])
        for bound in report.get('sourceBindings', []):
            assert info(G / bound['path']) == bound
    assert len(behavior['groupCoverage']) == 20 and all(r['checks'] and r['traces'] for r in behavior['groupCoverage'])
    assert {r['id'] for r in behavior['groupCoverage']} == {f'ACQ05-T{i:02}' for i in range(1, 21)}
    assert len(behavior['traces']) == 71 and behavior['counts']['campaignRecordsAuthenticated'] == 0
    for c in operations['changes']:
        assert info(G / c['after']['path']) == c['after']
        assert info(G / c['before']['preservedCopy'])['sha256'] == c['before']['sha256']
    write_new(receipt_path, {'recordedAtUtc': now, 'id': 'FEAT327-ACQ-05',
        'status': 'fulfilled-named-source-and-twenty-bounded-conditional-acceptance-groups',
        'actualGptDecision': info(decision_path), 'replyMessageId': decision['replyMessageId'],
        'derivedOperations': info(operations_path), 'independentSourceVerification': info(source_path),
        'behavioralAcceptance': info(behavior_path), 'readerNotes': info(A / 'FEAT327_ACQ_05_LIFECYCLE_NOTES.md'),
        'checks': {'reviewerSourceReproduced': 96, 'independentSource': 272, 'lifecycleAndSourceControls': 206,
            'failures': 0, 'namedAcceptanceGroups': 20, 'recordedConditionalTraces': 71},
        'currentDescendants': [c['after'] for c in operations['changes']], 'limits': behavior['limits'],
        'onlyThisNamedIssueClosed': True, 'finiteBehavioralAcceptanceComplete': True,
        'finiteAcceptanceMeaning': 'All20 named groups accounted for by bounded conditional model execution and explicit preserved-source checks. No wider engine, real campaign or human-playtest acceptance.',
        'candidateReadyForSubmission': False, 'candidateExactApproved': False, 'wholeGameFlowApproved': False,
        'runtimeImplemented': False, 'humanPlaytestApproved': False, 'campaignRecordsAuthenticated': 0,
        'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False,
        'historicalPendingRecordsPreserved': [info(previous), info(operations_path), info(source_path)]})
    scope = ('ACQ-05 finite fulfillment now accounts for all20 named lifecycle groups with206 passing controls and71 conditional traces, '
        'alongside the preserved272 independent source checks and96 reproduced reviewer checks. '
        'The new reference model separates actual paid ownership, spent valid start and completion/interruption; '
        'covers rest gates, release, death, replacement, rebond and receiving-owner histories; and preserves physical identity, HP ratios and spent budgets. '
        'Ranger feature/native payment and work/rest support are explicit conditional premises; no Ranger chassis or full mounted-command engine is claimed. '
        'The historical110-check companion model/report remains unchanged. Only the named ACQ05 source/lifecycle issue is fulfilled; '
        'full335 acquisition/use, all660 original cases, exact assembled GPT review, software and whole-game approval remain open.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [behavior_path, receipt_path])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'FEAT327-ACQ05-FINITE-FULFILLMENT', 'recordedAtUtc': now,
            'lifecycleChecks': 206, 'namedGroups': 20, 'conditionalTraces': 71,
            'acq05FiniteAcceptanceComplete': True, 'partialPrerequisiteIdentities': 335,
            'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve pending ACQ05 behavior scope before finite fulfillment.', 'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = ('All335 identities retain partial prerequisite evidence. Prodigy, three trade-training feats and eight half-feat '
                'choice slices are recorded. ACQ-05 is now fulfilled within its20 named bounded conditional groups; no unchanged source resubmission is needed. '
                'Keep the old110-check completion-first companion evidence historical. Audit remaining mandatory selections and initialization, '
                'then complete resource/use, actual command/mount/casting interactions, all660 original examples and complete assembled GPT review. '
                'Neither335 partial identities nor fulfilled ACQ05 means335 complete acquisitions or gameplay approval.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_CHOICES_AND_ACQ05_SOURCE_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT327_ACQ_05_FULFILLMENT_COVERAGE_DELTA.json",')
    anchor = '        ("Companion lifecycle — twenty outstanding acceptance groups", "feat327-acq05-source/ACQ05_ACCEPTANCE_EXPECTATIONS.json"),'
    assert text.count(anchor) == 1
    replacement = anchor.replace('twenty outstanding acceptance groups', 'twenty authored acceptance expectations')
    for label, file in [('Companion lifecycle — finite fulfillment', receipt_path.name),
        ('Companion lifecycle — executed conditional traces', behavior_path.name),
        ('Companion lifecycle — scope and limits', 'FEAT327_ACQ_05_LIFECYCLE_NOTES.md')]:
        replacement += '\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(file) + '),'
    text = text.replace(anchor, replacement)
    old_scope = read(previous)['status']
    assert text.count(old_scope) == 1
    # Retain the trade/half-feat progress in the current summary while replacing
    # only the superseded ACQ05 pending-lifecycle paragraph.
    choices, old_source = old_scope.split('Actual GPT ACQ-05 reply ', 1)
    text = text.replace(old_scope, choices + scope)
    compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        binding = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert path.read_bytes() == dest.read_bytes()
        saved.append({**binding, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta_path, {'recordedAtUtc': now, 'status': 'verified-scoped-ACQ05-finite-fulfillment',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(behavior_path), info(receipt_path)],
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_CHOICES_AND_ACQ05_SOURCE_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state = read(previous)
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: trade/half-feat choices and actual ACQ05 source adoption',
        'previousCheckpoint': info(previous), 'status': scope,
        'featACQ05FiniteFulfillment': info(receipt_path),
        'featCompanionLifecyclePass': {'report': info(behavior_path), 'checks': 206, 'groups': 20, 'traces': 71,
            'limits': behavior['limits'], 'actualCampaignEventsAuthenticated': 0},
        'activeGptReview': {'id': 'FEAT327-ACQ-05', 'status': 'completed-source-and-finite-acceptance-fulfillment',
            'replyReceived': True, 'replyMessageId': decision['replyMessageId'], 'chatUrl': decision['chatUrl'],
            'browserId': decision['browserId'], 'tabId': decision['tabId'], 'fulfillment': info(receipt_path),
            'pendingResponse': False, 'noUnchangedResubmissionRequired': True, 'wholeExactCandidateApproved': False},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'No new rule; finite evidence for the already applied actual GPT ACQ05 addendum.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path)})
    state['safeNextActions'] = [
        'ACQ05 is fulfilled within its20 bounded conditional groups. Preserve the old model/report and all source versions. Do not resubmit the settled source issue; the eventual actual assembled exact-candidate review remains required.',
        'Audit all remaining mandatory feat acquisition selections and initialization against current335 complete contracts; map already executed Prodigy, Initiate, trade, half-feat and named-chain evidence without claiming those slices cover full use.',
        'Complete FXC04–10 supplements, clocks/recovery, damage/resource causality, actual custody/commands/mount use, casting/copy and all660 original cases plus28 additions. Then obtain actual assembled feat review.',
        'Continue the ordinary/higher SPELL catalogs and remaining bestiary/Director content. Higher-spell435/180draft/208proposal counts are not Arch/Hero class counts.',
        'Carry reviewed crafting/language/onboarding/EX58 and owner CRPG/12-character/parallel-activity/host-permission direction. Final joint whole-game flow precedes authorized commit/push, verified remote and careful cosmology review; implementation and human balance remain separate.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'fulfillment': info(receipt_path),
        'coverage': info(ledger_path), 'navigationLinks': navigation['existingDistinctLinks'],
        'missingLinks': 0, 'checks': 206, 'groups': 20, 'pushed': False, 'cosmologyReviewed': False}, indent=2))


if __name__ == '__main__':
    main()
