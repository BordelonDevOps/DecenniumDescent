"""Record the visibly running GPT audit without claiming an audit verdict."""
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
PREFIX = 'FEAT335_ACQUISITION_AUDIT_01'


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_WEAPON_PROFILE_CHOICES.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_ACQUISITION_AUDIT_SUBMISSION.json'
    submission_path = A / (PREFIX + '_SUBMISSION.json')
    delta = A / (PREFIX + '_SUBMISSION_COVERAGE_DELTA.json')
    preservation = A / 'navigation-and-coverage-before-feat335-acquisition-audit'
    assert all(not p.exists() for p in [target, submission_path, delta, preservation])
    prep_path = A / (PREFIX + '_PREPARATION.json'); prep = read(prep_path)
    capture_path = A / (PREFIX + '_SUBMISSION_VISIBLE_CAPTURE_V2.json'); capture = read(capture_path)
    for key in ['request', 'startHere', 'sourceIndex', 'archive']: assert info(G / prep[key]['path']) == prep[key]
    request = (G / prep['request']['path']).read_text(encoding='utf-8').strip()
    assert request in capture['savedPromptVisibleText']
    assert 'DD_FEAT335_Acquisition_Audit_01.zip' in capture['savedPromptVisibleText']
    assert capture['turnState'] == 'in_progress' and capture['stopVisible'] is True
    chat_url = 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b'
    submission = {'recordedAtUtc': now, 'id': 'FEAT335-ACQUISITION-AUDIT-01',
        'status': 'submitted-to-actual-GPT-response-observed-running',
        'chatUrl': chat_url, 'chatTitle': 'Calibration Review Part 2', 'browserId': '3', 'tabId': '125745532',
        'savedUserMessageId': None, 'visibleTurnKey': capture['visibleTurnKey'],
        'identifierScope': 'The current visible DOM exposes fallback-turn-24 and in_progress, not a persistent message UUID.',
        'preparation': info(prep_path), 'request': prep['request'], 'archive': prep['archive'],
        'payloads': prep['payloads'], 'completeReportsIncluded': prep['completeReportsIncluded'],
        'visibleCapture': info(capture_path), 'screenshot': info(A / (PREFIX + '_SUBMITTED.png')),
        'lastRunningObservation': capture['capturedAtUtc'], 'pendingResponse': True,
        'observationRecovery': 'Send observation and one subsequent DOM observation timed out. The same tab then showed the full saved prompt, attached ZIP, in_progress and Stop. No second send was performed.',
        'supersededObservation': {'file': info(A / (PREFIX + '_SUBMISSION_VISIBLE_CAPTURE.json')),
            'reason': 'The old data-message-id selector returned no message nodes in this UI revision. The actual heading parent and exposed turn-state attributes ground V2.'},
        'requestedScope': 'All335 complete acquisition/initial-state obligations, source-linked evidence gaps and exact unarmed/natural profile classification; not final whole-feat approval.',
        'newRuleAdoptedBySubmission': False, 'candidateExactApproved': False, 'sourceInformationDeleted': False}
    write_new(submission_path, submission)
    state = read(previous); ledger_path = R / 'data/playtest/game_development_coverage.json'
    assert info(ledger_path) == state['coverageLedger']
    scope = ('Submitted the complete 335-feat acquisition/initial-state audit to actual GPT in Calibration Review Part 2. '
        'The byte-verified archive contains 198 payloads and 20 complete local evidence reports; all 335 current contract/public full procedures match, including the eight nested unchanged reviewed records. '
        'Thirty-seven historical report source bindings differ from newer current files and are explicitly recorded, not relabeled as reruns. '
        'The request asks for every permanent choice, snapshot, starting allowance/empty reserve/shared pool, source-qualified exception and actual evidence gap, plus the specific unarmed/natural Weapon Mastery classification. '
        'The same saved prompt and in_progress/Stop controls confirmed the running response after an observation timeout; there was no duplicate send. '
        'No audit verdict, new rule, complete acquisition, runtime promotion or whole-game approval has been claimed.')
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'FEAT335-ACQUISITION-AUDIT-01-SUBMITTED', 'recordedAtUtc': now,
            'status': 'actual-review-running-no-verdict', 'submission': info(submission_path),
            'request': prep['request'], 'archive': prep['archive'],
            'currentProcedurePairsCompared': 335, 'payloads': 198, 'completeLocalReports': 20,
            'all335AcquisitionsComplete': False, 'newRuleAdoptions': 0, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'status': row['status'], 'reason': 'Preserve open work before targeted complete acquisition audit submission.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'].append('FEAT335-ACQUISITION-AUDIT-01 is submitted and visibly running in Calibration Review Part 2. '
                'Inspect that same live response and preserve the returned complete audit before applying any findings. '
                'This is the targeted full acquisition/initial-state audit, not the final assembled feat verdict.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT335_ACQUISITION_AUDIT_01_SUBMISSION_COVERAGE_DELTA.json",')
    anchor = '        ("Weapon profile choices — source and conditional limits", "FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_NOTES.md"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [
        ('Complete feat acquisition audit — submitted request', 'feat335-acquisition-audit-01-input/REQUEST.txt'),
        ('Complete feat acquisition audit — scope and evidence index', 'feat335-acquisition-audit-01-input/START_HERE.json'),
        ('Complete feat acquisition audit — literal 335-row source index', 'feat335-acquisition-audit-01-input/ALL335_SOURCE_INDEX.json'),
        ('Complete feat acquisition audit — exact submitted archive', 'DD_FEAT335_Acquisition_Audit_01.zip'),
        ('Complete feat acquisition audit — actual submission receipt', submission_path.name)]:
        addition += '\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(file) + '),'
    text = text.replace(anchor, addition)
    anchor = state['status']; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + ' ' + scope); compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        bound = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        saved.append({**bound, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta, {'recordedAtUtc': now, 'status': 'actual-targeted-acquisition-audit-submission-only',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'submission': info(submission_path), 'preparation': info(prep_path),
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_COVERAGE_DELTA.json'),
        'newRuleAdoptions': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.setdefault('priorCompletedGptObservations', []).append(deepcopy(state['activeGptReview']))
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: two weapon-profile acquisition/modifier slices',
        'previousCheckpoint': info(previous), 'status': scope,
        'activeGptReview': {k: deepcopy(submission[k]) for k in ['id', 'status', 'chatUrl', 'chatTitle',
            'browserId', 'tabId', 'savedUserMessageId', 'visibleTurnKey', 'lastRunningObservation', 'pendingResponse']},
        'feat335AcquisitionAuditSubmission': info(submission_path), 'newRuleAdoptions': 0,
        'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'Targeted audit submitted; no new source verdict received or adopted.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    state['activeGptReview'].update({'submission': info(submission_path), 'replyReceived': False, 'wholeExactCandidateApproved': False})
    state['safeNextActions'] = [
        'Inspect the SAME Chrome3 tab125745532, Calibration Review Part2, last submitted FEAT335-ACQUISITION-AUDIT-01. It was visibly in_progress with Stop; fallback-turn-24 is only a DOM turn key, not a persistent UUID. Do not resubmit or restart merely because an observation times out.',
        'On actual terminal response, capture complete visible text, download its exact offered package, preserve raw bytes, verify manifest and inspect every acquisition-audit row/remaining-work finding. Adopt only justified exact corrections within the existing user authority; no automatic whole-candidate promotion.',
        'The 198-payload/20-report archive and literal335 source index are preserved. All335 current procedure pairs match; 37 older report bindings differ explicitly. Reuse prior evidence only within its recorded source scope, following the named ACQ fulfillment chains.',
        'Independent resource work may continue, but the existing FA01/FA02 boundary report already exercises the two Endurance cause counters, canonical deadlines, genuine rest and shortage interactions. Read its actual scope before duplicating it; full physical premises and all335 acquisition initialization remain separate.',
        'Continue FXC04–10 complete supplements, initial state, clocks, damage/resource causality, custody/commands/mounts, spell/copy interactions and660+28 cases, followed by the separate full assembled feat review.',
        'Continue ordinary/higher spells and bestiary/Director content, preserving completed scopes and the owner CRPG/12-character/parallel-activity/host-permission direction. Actual final joint whole-game flow -> authorized push -> verified remote -> careful cosmology. No source deletion or human-balance/runtime claim.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'submission': info(submission_path),
        'coverage': info(ledger_path), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0}, indent=2))


if __name__ == '__main__':
    main()
