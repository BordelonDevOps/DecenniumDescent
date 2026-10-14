"""Preserve navigation and record 34 additional partial prerequisite identities."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
from record_feat_exact_01_acq03_fulfillment import read, info, write_new

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ03_FULFILLMENT.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_COMPOSITE_CASTING.json'
    delta_path = A / 'FEAT_EXACT_01_COMPOSITE_CASTING_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-exact-01-composite-casting'
    assert all(not p.exists() for p in [target, delta_path, preservation]), 'One-use checkpoint already started'
    report_path = A / 'FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_CHECK.json'
    notes_path = A / 'FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_NOTES.md'
    report = read(report_path)
    assert report['checks'] == 336 and not report['failures'] and all(x['passed'] for x in report['results'])
    assert len(report['cohort']) == 34 and len(report['remaining']) == 9
    assert report['counts']['cumulativePartialPrerequisiteIdentities'] == 326
    assert report['counts']['recordedCases'] == 73 and report['counts']['prerequisiteComparisons'] == 114
    for binding in report['sourceBindings']:
        assert info(G / binding['path']) == binding, binding['path']
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    scope = (
        'A combined casting/owned-supplement pass adds34 disjoint partial prerequisite identities: all33 casting-bearing trees and Greater Spell Focus. '
        '336 checks pass across73 source-qualified conditional snapshots and114 prerequisite comparisons, with actual paid parent histories and earned/unspent opportunities. '
        'Independent scores, levels, martial training, smith tools and Boolean alternatives remain operative. '
        'The minimum-rank5 positive uses reviewed rank8 Stitch Fate, not an exact-rank5 boundary; Planar Binding remains null and unavailable. '
        'The partial ledger now covers326 identities with9 remaining. No full target acquisition, new rule, exact candidate approval, runtime or human balance finding is claimed.')
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('validationEvidence', []).append(report_path.relative_to(G).as_posix())
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'FEAT-EXACT-01-COMPOSITE-CASTING-PREREQUISITES', 'recordedAtUtc': now,
            'status': report['status'], 'validation': report_path.relative_to(G).as_posix(),
            'newPartialIdentities': 34, 'cumulativePartialIdentities': 326, 'remainingIdentities': 9,
            'fullFeatCandidateApproved': False, 'allTargetAcquisitionsValidated': False,
        })
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'reason': 'Preserve the292/43 partial-prerequisite checkpoint before34 additional mixed casting/ownership identities.',
                'status': row['status'], 'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = (
                'FXC-05 partial predicate bookkeeping:209 numeric/level/None,12 Warrior,48 training,10 owned-feat,13 current-lineage and34 combined casting/owned-supplement identities;9 remain. '
                'The new pass has336 checks across73 explicit conditional snapshots and114 comparisons. Actual GPT KEEP still applies only to the earlier48+10 reports; no new broad approval is implied. '
                'Magic Initiate has466 local selection checks; current lineages have3130 local checks. No complete326-acquisition claim is made. '
                'Remaining identities: ' + ', '.join(x['id'] for x in report['remaining']) + '. '
                'Dragon Blood needs actual qualifying legacy/bloodline and damage-type evidence; no Drakari alias. Prodigy still needs ordered skill/tool/language/Expertise selections. '
                'Acquired class-feature credentials, actual source trade levels, genuine context and remaining ownership branches still need completion. '
                'ACQ-03 remains fulfilled with175 source checks and113 snapshot/source controls. Full selection, resource, use and exact-candidate review remain open.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT327_ACQ_03_FULFILLMENT_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_COMPOSITE_CASTING_COVERAGE_DELTA.json",')
    anchor = '        ("Casting prerequisites — finite fulfillment", "FEAT327_ACQ_03_FINITE_FULFILLMENT.json"),'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n'
        '        ("Combined feat prerequisites — source-qualified cases", "FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_CHECK.json"),\n'
        '        ("Combined feat prerequisites — scope and remaining work", "FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_NOTES.md"),')
    anchor = 'The old numeric/history/Warrior reports retain their original input bindings;'
    assert text.count(anchor) == 1
    text = text.replace(anchor,
        'A later combined pass adds34 disjoint partial identities across all33 casting-bearing trees and Greater Spell Focus:336 checks,73 conditional snapshots and114 prerequisite comparisons pass. '
        'The resulting326 partial identities leave9; they are not326 complete acquisitions. Actual paid parents, independent scores/levels/training and earned opportunities remain mandatory. '
        'Reviewed rank8 Stitch Fate supports a minimum-rank5 predicate without completing or activating Planar Binding. No exact-rank5 positive boundary, runtime or broad approval is claimed. ' + anchor)
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
        'previousFeatOpenIssuesPreservedVerbatim': True, 'validation': [info(report_path)],
        'previousCoverageDelta': info(A / 'FEAT327_ACQ_03_FULFILLMENT_COVERAGE_DELTA.json'),
        'newSourceRuleAdopted': False, 'newPartialPrerequisiteIdentities': 34, 'remainingCredentialDependentIdentities': 9,
        'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    result = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        print(result.stderr); raise SystemExit(result.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state = read(previous)
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: ACQ-03 finite source and behavioral fulfillment',
        'previousCheckpoint': info(previous), 'status': scope,
        'featCompositeCastingPrerequisitePass': {'report': info(report_path), 'notes': info(notes_path),
            'checks': 336, 'cases': 73, 'prerequisiteComparisons': 114, 'failures': 0,
            'newPartialIdentities': 34, 'cumulativePartialIdentities': 326, 'remainingIdentities': 9,
            'allTargetAcquisitionsValidated': False, 'candidateReadyForSubmission': False},
        'remainingCredentialIdentitiesCurrent': report['remaining'],
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path),
        'navigationBindingPolicy': 'Explicit preserved coverage chain through the combined casting predicate pass; candidate source changes remain bounded by measured ACQ-01/02/03 operations.'})
    state['safeNextActions'][0] = (
        'ACQ-03 is fulfilled; do not resend. The latest combined prerequisite report has336 checks for34 additional identities, leaving9: '
        + ', '.join(x['id'] for x in report['remaining']) + '. '
        'Complete actual parent choices/qualifications, source trade-level histories and acquired class-rage credentials; retain unavailable legacy/context sources without inventing them. '
        'Then continue complete feat acquisition choices and use procedures, not merely this partial predicate tally.')
    state.setdefault('preservationManifests', []).append(info(manifest))
    write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path), 'navigationLinks': navigation['existingDistinctLinks'],
        'missingLinks': 0, 'partialIdentities': 326, 'remaining': 9, 'sourceInformationDeleted': False, 'pushed': False}, indent=2))


if __name__ == '__main__':
    main()
