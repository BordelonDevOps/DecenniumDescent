"""Preserve and record Prodigy choice evidence and the actual ACQ05 submission."""
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
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ04_FULFILLMENT.json'
    target = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PRODIGY_AND_ACQ05_SUBMISSION.json'
    submission = A/'FEAT327_ACQ_05_SUBMISSION.json'
    delta = A/'FEAT_EXACT_01_PRODIGY_AND_ACQ05_COVERAGE_DELTA.json'
    preservation = A/'navigation-and-coverage-before-prodigy-and-acq05'
    assert all(not p.exists() for p in [target, submission, delta, preservation])
    preparation = read(A/'FEAT327_ACQ_05_PREPARATION.json')
    capture_path = A/'FEAT327_ACQ_05_SUBMISSION_VISIBLE_CAPTURE.json'; capture = read(capture_path)
    message_id = 'b76f5068-2d0c-4662-bb8e-87129ad8f4e0'
    assert capture['status'] == 'submitted-response-running'
    assert len(capture['nodes']) == 1 and capture['nodes'][0]['messageIds'] == message_id
    assert 'FEAT327-ACQ-05' in capture['nodes'][0]['text'] and 'DD_FEAT327_ACQ05_Companion_Timing_Source.zip' in capture['nodes'][0]['text']
    for key in ['request', 'archive']:
        assert info(G/preparation[key]['path']) == preparation[key]
    report_path = A/'FEAT_EXACT_01_PRODIGY_CHOICES_CHECK.json'; report = read(report_path)
    assert report['checks'] == 245 and report['failures'] == [] and all(x['passed'] for x in report['results'])
    assert len(report['traces']) == 104 and report['counts']['sourceToolProfiles'] == 42 and report['counts']['primaryTrades'] == 16
    for binding in report['sourceBindings']:
        assert info(G/binding['path']) == binding
    write_new(submission, {'recordedAtUtc': now, 'id': 'FEAT327-ACQ-05', 'status': 'submitted-to-actual-GPT-response-observed-running',
        'savedUserMessageId': message_id, 'chatUrl': capture['url'], 'browserId': '3', 'tabId': '125745532',
        'preparation': info(A/'FEAT327_ACQ_05_PREPARATION.json'), 'request': preparation['request'], 'archive': preparation['archive'],
        'payloads': preparation['payloads'], 'visibleCapture': info(capture_path), 'screenshot': info(A/'FEAT327_ACQ_05_SUBMITTED.png'),
        'responseObservationAtUtc': capture['capturedAtUtc'], 'submitTimeoutResolution': 'The Send observation timed out, then the same tab showed the saved message, attached ZIP and Stop control. No second send was performed.',
        'questionScope': ['First purchase/payment versus first bond', 'Attempt spend, interruption, retry and actual rest', 'Transfer/replacement versus nonrepeatable feat ownership'],
        'noRuleAdoptedBySubmission': True, 'candidateExactApproved': False, 'sourceInformationDeleted': False})
    scope = ('Prodigy ordered-choice evidence now has245 passing checks and104 recorded traces. '
             'The actual Human/Imperial/Warrior training and payment slice covers all42 profiled tools and16 primary trades, '
             'new/existing skill Expertise, actual source language-slot counts, conditional language contact/modes, '
             'separately paid Skill Expert ordering, rejection and exhaustion. It changes no rule or source flag. '
             'Conditional contact/saturation states are not authenticated campaign histories or complete class builds. '
             'The335 partial prerequisite count is unchanged. ACQ-05 was actually submitted to GPT for Animal Companion purchase/attempt/transfer timing; no answer or approval is inferred from submission.')
    ledger_path = R/'data/playtest/game_development_coverage.json'; before = read(ledger_path); ledger = deepcopy(before)
    changed = {'DD-06', 'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, A/'FEAT_EXACT_01_PRODIGY_CHOICES_NOTES.md'])
        row.setdefault('reviewEvidence', []).append(submission.relative_to(G).as_posix())
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'PRODIGY-CHOICES-AND-ACQ05-SUBMISSION', 'recordedAtUtc': now,
            'prodigyChecks': 245, 'recordedTraces': 104, 'partialPrerequisiteIdentities': 335,
            'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve pending Prodigy choice work and unsent companion question before local fulfillment and actual submission.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = ('All335 original identities have disjoint finite partial prerequisite evidence. '
                'Prodigy now has245 checks/104 traces for ordered skill/tool/language/Expertise choices and their stated conditional limits. '
                'Continue every other mandatory choice and initialization; complete acquisition coverage remains unfinished. '
                'Animal Companion successful completed-hour evidence does not settle live purchase/attempt timing, interruption or transfer/rebond. '
                'ACQ-05 is submitted to actual GPT under message ' + message_id + '; inspect that same live response before any resend. '
                'ACQ-04 is fulfilled; no unchanged preliminary re-review. Full335 selections, resources/use, original660 examples and exact assembled review remain open.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R/'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT327_ACQ_04_FULFILLMENT_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_PRODIGY_AND_ACQ05_COVERAGE_DELTA.json",')
    anchor = '        ("All335 feats — partial prerequisite evidence index", "FEAT_EXACT_01_PARTIAL_PREREQUISITE_COVERAGE_INDEX.json"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Prodigy — ordered choice evidence', report_path.name), ('Prodigy — scope and limits', 'FEAT_EXACT_01_PRODIGY_CHOICES_NOTES.md'),
                        ('Animal Companion — actual ACQ05 submission', submission.name), ('Animal Companion — submitted lifecycle question', 'FEAT327_ACQ_05_COMPANION_TIMING_QUESTION.txt')]:
        addition += '\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(file) + '),'
    text = text.replace(anchor, addition)
    anchor = 'The old numeric/history/Warrior reports retain their original input bindings;'
    assert text.count(anchor) == 1
    text = text.replace(anchor, scope + ' ' + anchor); compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        binding = info(path); dest = preservation/path.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest); assert path.read_bytes() == dest.read_bytes()
        saved.append({**binding, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation/'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-scoped-coverage-update',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(submission)],
        'previousCoverageDelta': info(A/'FEAT327_ACQ_04_FULFILLMENT_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state = read(previous)
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'no progress: status-only roadmap response; current sources and actual browser revalidated before this work',
        'previousCheckpoint': info(previous), 'status': scope,
        'featProdigyChoicePass': {'report': info(report_path), 'notes': info(A/'FEAT_EXACT_01_PRODIGY_CHOICES_NOTES.md'),
            'checks': 245, 'traces': 104, 'toolProfiles': 42, 'primaryTrades': 16, 'noNewRuleAdopted': True,
            'limits': report['limits'], 'all335AcquisitionsComplete': False},
        'activeGptReview': {'id': 'FEAT327-ACQ-05', 'status': 'submitted-response-observed-running',
            'savedUserMessageId': message_id, 'submission': info(submission), 'chatUrl': capture['url'], 'browserId': '3', 'tabId': '125745532',
            'pendingResponse': True, 'replyReceived': False, 'lastRunningObservation': capture['capturedAtUtc'], 'wholeExactCandidateApproved': False},
        'navigation': {'map': info(G/'REVIEW_MAP.html'), 'receipt': info(A/'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    state['safeNextActions'] = [
        'Inspect the existing actual GPT ACQ-05 response in Calibration Review Part 2. Submission is confirmed; never resubmit solely because a browser observation times out. Capture/download the terminal decision, inspect its evidence, then implement only the exact resolved lifecycle changes with preserved predecessors.',
        'Prodigy ordered choices now have finite evidence; preserve its stated conditional scope and historical lineage-only reports. Continue remaining mandatory choices/initialization for all335 acquisitions.',
        'Continue FXC-04–10 resource/recovery, clocks, damage/resource causality, command/custody, casting/copy and all660 original case premises. Then obtain actual assembled exact-candidate review.',
        'All335 identities have partial prerequisite evidence, not full acquisition/use acceptance. ACQ-04 is fulfilled; do not reopen unchanged reviewed scopes.',
        'Carry owner CRPG/12-character/parallel-activity/host-permission direction forward. Finish systems and joint whole-game flow before authorized commit/push, remote verification, careful cosmology and preservation-based cleanup. Software conversion remains later.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'submission': info(submission), 'coverage': info(ledger_path),
                      'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'prodigyChecks': 245}, indent=2))


if __name__ == '__main__':
    main()
