"""Register a verified reference slice while the existing GPT audit is pending.

This deliberately preserves historical evidence and all unrelated ledger rows.
The caller supplies exact source-bound report expectations and scope wording.
"""
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


def register(config, caller):
    now = datetime.now(timezone.utc).isoformat()
    previous = A / config['previousCheckpoint']; target = A / config['checkpoint']
    delta = A / config['delta']; preservation = A / config['preservationDirectory']
    assert all(not p.exists() for p in [target, delta, preservation])
    report_path = A / config['report']; report = read(report_path); notes_path = A / config['notes']
    observation_path = A / config['observation']; observation = read(observation_path)
    assert report['checks'] == config['checks'] and not report['failures'] and all(x['passed'] for x in report['results'])
    assert len(report[config['historyKey']]) == config['histories']
    for key, value in config['expectedCounts'].items(): assert report['counts'][key] == value
    for bound in report['sourceBindings']: assert info(G / bound['path']) == bound
    assert observation['stopVisible'] is True and observation['turnState'] == 'in_progress'
    state = read(previous); ledger_path = R / 'data/playtest/game_development_coverage.json'
    assert info(ledger_path) == state['coverageLedger']
    assert state['activeGptReview']['pendingResponse'] and not state['activeGptReview']['replyReceived']
    scope = config['scope']; before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        addendum = {'id': config['id'], 'recordedAtUtc': now, 'checks': report['checks'],
            'histories': config['histories'], 'identities': report['cohort'], 'counts': report['counts'],
            'limits': report['limits'], 'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False}
        if 'localGapCorrection' in report: addendum['localGapCorrection'] = deepcopy(report['localGapCorrection'])
        row.setdefault('currentEvidenceAddenda', []).append(addendum)
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'status': row['status'], 'reason': 'Preserve open work before '+config['id']+'.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'].append(config['openIssue'])
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        '+json.dumps(config['previousDelta'])+','; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor+'\n        '+json.dumps(config['delta'])+',')
    anchor = config['navigationAnchor']; assert text.count(anchor) == 1
    addition = anchor
    for label, file in config['navigationLinks']:
        assert (A / file).is_file()
        addition += '\n        ('+json.dumps(label, ensure_ascii=False)+', '+json.dumps(file)+'),'
    text = text.replace(anchor, addition)
    anchor = state['status']; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor+' '+scope); compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        bound = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        saved.append({**bound, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    write_new(delta, {'recordedAtUtc': now, 'status': config['id']+'-verified-scoped-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / config['previousDelta']),
        'recorders': [info(Path(__file__)), info(Path(caller))],
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0,
        'sourceInformationDeleted': False, 'newRuleAdoptions': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': config['previousClassification'],
        'previousCheckpoint': info(previous), 'status': scope,
        config['stateKey']: {'report': info(report_path), 'notes': info(notes_path),
            'checks': report['checks'], 'histories': config['histories'], 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': config['ruleScope'],
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    if 'localGapCorrection' in report: state[config['stateKey']]['localGapCorrection'] = deepcopy(report['localGapCorrection'])
    state['activeGptReview'].update({'lastRunningObservation': observation['capturedAtUtc'], 'latestObservation': info(observation_path)})
    state['safeNextActions'].insert(3, config['nextAction'])
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
        'checks': report['checks'], 'histories': config['histories']}, indent=2))
