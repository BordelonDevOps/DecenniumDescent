"""Preserve and register the four-gadget reference evidence once."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_MANEUVER_USE.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_GADGET_USE.json'
    delta = A / 'FEAT_EXACT_01_GADGET_USE_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-gadget-use'
    assert all(not p.exists() for p in [target, delta, preservation])
    report_path = A / 'FEAT_EXACT_01_GADGET_USE_CHECK.json'; report = read(report_path)
    notes_path = A / 'FEAT_EXACT_01_GADGET_USE_NOTES.md'
    observation_path = A / 'FEAT_EXACT_01_GADGET_GPT_STATUS.json'; observation = read(observation_path)
    assert report['checks'] == 269 and not report['failures'] and all(x['passed'] for x in report['results'])
    assert len(report['traces']) == 38 and report['counts']['gadgetProfiles'] == 4 and report['counts']['currentGnomeVariants'] == 3
    for bound in report['sourceBindings']: assert info(G / bound['path']) == bound
    assert observation['stopVisible'] is True and observation['turnState'] == 'in_progress'
    state = read(previous); ledger_path = R / 'data/playtest/game_development_coverage.json'
    assert info(ledger_path) == state['coverageLedger']
    scope = ('Contraption Crafter now has 269 passing checks across 38 recorded histories, with paid feat acquisition by all three current Gnome variants and construction/expiry histories for all four d4 results. '
        'The procedure commits five gp of suitable owned parts and the 24-elapsed-hour allowance at construction start; ten uninterrupted minutes precede the d4 result. '
        'Interruption loses parts/use, midnight and rest do not reset the allowance, and same-object handoffs preserve the one-hour deadline. '
        'The lamp, physical-contact line bell, bounded light clamp and held hand fan use their own Action costs and utility restrictions. '
        'One resolved damage destroys the HP1 object; expiry/destruction/dismantling yield no credited reclaim, ancestral clockwork, class device, fuel or purchased supply recharge. '
        'Tools, supply/access, work, turn, contact and hearing facts are conditional fixtures. Ordinary object damage is supplied, clamp release retains a required ordinary-fall event, and full physical/virtual-clock integration remains outside this slice. '
        'No source rule changed. The all335 acquisition audit is still visibly running in the same GPT chat; no full feat or whole-game approval is claimed.')
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'FOUR-GADGET-USE', 'recordedAtUtc': now, 'checks': 269, 'histories': 38,
            'identities': report['cohort'], 'counts': report['counts'], 'limits': report['limits'],
            'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'status': row['status'], 'reason': 'Preserve open work before the bounded four-gadget construction/use pass.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'].append('Carry the Contraption Crafter four-profile construction/use evidence within its source-qualified paid Gnome history and conditional object scene. '
                'Do not repeat the same 269 checks as new coverage. Ordinary object falling/attacks, complete custody/geometry, activity authentication and virtual/outside-initiative clocks remain distinct integrations.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_MANEUVERS_USE_COVERAGE_DELTA.json",'; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_GADGET_USE_COVERAGE_DELTA.json",')
    anchor = '        ("Six maneuvers — encounter scope and remaining integration", "FEAT_EXACT_01_MANEUVERS_USE_NOTES.md"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Four heritage gadgets — construction and use evidence', report_path.name),
                        ('Four heritage gadgets — source and physical-scope limits', notes_path.name)]:
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
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-bounded-four-gadget-use-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_MANEUVERS_USE_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0,
        'sourceInformationDeleted': False, 'newRuleAdoptions': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: six maneuver transaction evidence registered',
        'previousCheckpoint': info(previous), 'status': scope,
        'featFourGadgetUsePass': {'report': info(report_path), 'notes': info(notes_path),
            'checks': 269, 'histories': 38, 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'Existing Contraption Crafter/SUP08 and ordinary object/action procedures only; no source changes.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    assert state['activeGptReview']['pendingResponse'] and not state['activeGptReview']['replyReceived']
    state['activeGptReview'].update({'lastRunningObservation': observation['capturedAtUtc'], 'latestObservation': info(observation_path)})
    state['safeNextActions'].insert(4,
        'Carry the 269-check/38-history Contraption Crafter/SUP08 gadget report. All three Gnome variants paid actual feat opportunities and all four d4 outcomes have construction/expiry witnesses. '
        'Supplies/access/activity/contact/turn facts and resolved damage are conditional; clamp releases require separate ordinary falling resolution. Full clocks/physics/custody and all FXC04–10 remain open.')
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'checks': 269, 'histories': 38}, indent=2))


if __name__ == '__main__':
    main()
