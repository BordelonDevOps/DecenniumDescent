"""Register the six-maneuver evidence without promoting the full candidate."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_ACQUISITION_AUDIT_SUBMISSION.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_MANEUVER_USE.json'
    delta = A / 'FEAT_EXACT_01_MANEUVERS_USE_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-maneuver-use'
    assert all(not p.exists() for p in [target, delta, preservation])
    report_path = A / 'FEAT_EXACT_01_MANEUVERS_USE_CHECK.json'; report = read(report_path)
    notes_path = A / 'FEAT_EXACT_01_MANEUVERS_USE_NOTES.md'
    observation_path = A / 'FEAT_EXACT_01_MANEUVERS_GPT_STATUS.json'; observation = read(observation_path)
    assert report['checks'] == 243 and not report['failures'] and all(x['passed'] for x in report['results'])
    assert len(report['traces']) == 70 and report['counts']['maneuvers'] == 6 and report['counts']['d6FacesEach'] == 6
    for bound in report['sourceBindings']: assert info(G / bound['path']) == bound
    assert observation['stopVisible'] is True and observation['turnState'] == 'in_progress'
    state = read(previous)
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    assert info(ledger_path) == state['coverageLedger']
    scope = ('All six Martial Adept maneuver identities now have 243 passing checks across 70 recorded histories, including every d6 face. '
        'The bounded encounter uses actual paid Warrior Martial Adept/Advanced selections, real ability and proficiency projections, and explicit conditional body, custody, fear, obstacle and incoming damage records. '
        'It commits costs before rolls, retains costs on failed or interrupted attempts, and exercises ordinary attack faces, opposed ties, Shove outcomes, distinct Disarm methods and drop custody, '
        'typed Guarding reduction before one Core tempHP continuation, Reaction epochs, single-record Rally task degrees and separate terrain-paying movement with opportunity timing before exit. '
        'The interrupting opportunity consequence is supplied conditionally; full opportunity attacks, multiple-foe reaction ordering, other weapon profiles, full map legality, Ready/class interactions and genuine rest recovery are outside this slice. '
        'Advanced adds only its new available die to a genuinely spent parent pool. No source rule changed. '
        'The separate all335 acquisition audit remains visibly running in the same GPT chat; neither full feat execution nor whole-game approval is claimed.')
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'SIX-MANEUVER-USE', 'recordedAtUtc': now, 'checks': 243, 'histories': 70,
            'identities': report['cohort'], 'counts': report['counts'], 'limits': report['limits'],
            'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'status': row['status'], 'reason': 'Preserve open work before the bounded six-maneuver use pass.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'].append('Carry the six-maneuver use report within its actual paid-acquisition and conditional encounter scope. '
                'All six menu identities and d6 faces are exercised; full maps, other attack profiles, full opportunity/Ready/class interactions, '
                'rest recovery and complete feat execution remain distinct. Do not repeat the same bounded histories as new coverage.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT335_ACQUISITION_AUDIT_01_SUBMISSION_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_MANEUVERS_USE_COVERAGE_DELTA.json",')
    anchor = '        ("Complete feat acquisition audit — actual submission receipt", "FEAT335_ACQUISITION_AUDIT_01_SUBMISSION.json"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Six maneuvers — paid acquisition and use evidence', report_path.name),
                        ('Six maneuvers — encounter scope and remaining integration', notes_path.name)]:
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
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-bounded-six-maneuver-use-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / 'FEAT335_ACQUISITION_AUDIT_01_SUBMISSION_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0,
        'sourceInformationDeleted': False, 'newRuleAdoptions': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: complete acquisition audit submitted to actual GPT',
        'previousCheckpoint': info(previous), 'status': scope,
        'featSixManeuverUsePass': {'report': info(report_path), 'notes': info(notes_path),
            'checks': 243, 'histories': 70, 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'Existing SUP03 maneuver and Core/Combat procedures only; no candidate source changes.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    assert state['activeGptReview']['pendingResponse'] and not state['activeGptReview']['replyReceived']
    state['activeGptReview'].update({'lastRunningObservation': observation['capturedAtUtc'], 'latestObservation': info(observation_path)})
    state['safeNextActions'].insert(3,
        'Carry the 243-check/70-history six-maneuver report without rerunning or expanding its claim. All six identities and d6 faces use actual paid feat histories; encounter body/custody/fear/incoming damage and the interrupting opportunity outcome are explicitly conditional. '
        'This closes the bounded SUP03 use slice, not full maps, other attack profiles, multiple-reaction ordering, Ready/class interactions, rest recovery or all FXC04–10.')
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'checks': 243, 'histories': 70}, indent=2))


if __name__ == '__main__':
    main()
