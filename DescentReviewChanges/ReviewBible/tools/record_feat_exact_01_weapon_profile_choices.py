"""Preserve and register the two weapon-selection evidence slices once."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_CASTING_SELECTIONS.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_WEAPON_PROFILE_CHOICES.json'
    delta = A / 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-weapon-profile-choices'
    assert all(not p.exists() for p in [target, delta, preservation])
    report_path = A / 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_CHECK.json'; report = read(report_path)
    notes_path = A / 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_NOTES.md'
    assert report['checks'] == 591 and not report['failures'] and all(x['passed'] for x in report['results'])
    assert len(report['traces']) == 47 and report['counts']['currentReviewedEquipmentProfiles'] == 40
    assert report['counts']['sourceQualifiedUnarmedFocusHistories'] == 1
    assert report['counts']['conditionalNaturalProfileHistories'] == 2
    for bound in report['sourceBindings']: assert info(G / bound['path']) == bound
    state = read(previous)
    assert info(G / state['coverageLedger']['path']) == state['coverageLedger']
    scope = ('Weapon Focus and Weapon Mastery now have 591 passing checks across 47 recorded histories. '
        'All 40 current reviewed equipment profiles have actual paid selections: 24 use Warrior first-class Martial proficiency and 16 first purchase Weapon Master training. '
        'The pass records exact permanent choices, proficiency receipts, distinct-profile Focus repetition, nonrepeatable Mastery and actual earned opportunity/level gates. '
        'One Monk unarmed Focus witness uses actual Simple training; two Troll Claws histories are explicitly conditional on an external eligible body and independently authorized exact proficiency, neither authenticated nor created here. '
        'Bounded modifier checks retain native melee/thrown profiles, reject generic improvised inheritance, suppress Focus on proficiency loss without erasing purchases, and preserve Mastery own use predicates. '
        'A paid Precision Throw combination and Core kept-die/critical-range comparisons add no damage execution. '
        'Specific unarmed Mastery, full physical attack legality, damage/resource interactions, remaining initialization, all 335 complete acquisitions and assembled GPT review remain open.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'WEAPON-PROFILE-CHOICES', 'recordedAtUtc': now, 'checks': 591, 'histories': 47,
            'identities': report['cohort'], 'counts': report['counts'], 'partialPrerequisiteIdentities': 335,
            'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({
                'recordedAtUtc': now, 'status': row['status'], 'reason': 'Preserve prior open work before weapon-profile selection pass.',
                'openIssues': deepcopy(row['openIssues'])})
            old = 'Continue exact weapon-profile choices, remaining initialization and the full335 acquisition audit; keyword scans and partial counts do not establish completion.'
            assert row['openIssues'][1].count(old) == 1
            row['openIssues'][1] = row['openIssues'][1].replace(old,
                'Weapon Focus/Mastery have 591 checks across 47 histories covering all 40 reviewed equipment profiles, '
                'one source-qualified Monk unarmed Focus and two explicitly conditional natural-profile histories. '
                'Specific unarmed Mastery and authenticated natural-body/proficiency sources remain outside that slice. '
                'Audit remaining initialization and every full acquisition contract; keyword scans and partial counts do not establish completion.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_CASTING_SELECTIONS_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_COVERAGE_DELTA.json",')
    anchor = '        ("Casting selections — scope and spell placement limits", "FEAT_EXACT_01_CASTING_SELECTIONS_NOTES.md"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Weapon Focus/Mastery — profile evidence', report_path.name),
                        ('Weapon profile choices — source and conditional limits', notes_path.name)]:
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
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-scoped-weapon-profile-selection-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_CASTING_SELECTIONS_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: eleven casting-selection slices',
        'previousCheckpoint': info(previous), 'status': scope,
        'featWeaponProfileChoicesPass': {'report': info(report_path), 'notes': info(notes_path),
            'checks': 591, 'histories': 47, 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'No new source rule; existing exact Focus/Mastery, FS02/ACQ01 and Core attack procedures apply.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    state['safeNextActions'] = [
        'Audit each of the 335 full acquisition contracts for all remaining fixed choices, snapshot branches and initial fields. Partial prerequisite and selection cohorts do not prove full acquisition completion.',
        'Carry the 40-profile Focus/Mastery and specific Monk unarmed Focus evidence. Conditional Troll Claws histories do not authenticate a body or proficiency. Resolve any needed specific-unarmed Mastery classification or actual natural proficiency source from exact existing rules, conferring with actual GPT for a real source gap; do not invent umbrella permissions.',
        'Carry the eleven casting selections and their exact source/conditional boundaries. Full casts, ritual learning, Cantrip Mastery damage, provider use, reserve/death/resource behavior and all other feat execution remain distinct work.',
        'Complete remaining FXC04–10 supplements, initial resources, clocks/recovery, damage/resource causality, command/custody/mount and casting/copy interactions, all660 original cases plus28 additions, then actual assembled full-feat GPT review.',
        'Continue ordinary/higher SPELL catalogs and bestiary/Director content. Preserve owner CRPG/12-character/parallel-activity/host-permission direction and completed crafting/language/onboarding/EX58 scopes.',
        'Actual final joint whole-game flow agreement precedes authorized GitHub push, verified remote and careful cosmology review. Preserve all sources; software implementation and human balance remain separate.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'checks': 591, 'histories': 47}, indent=2))


if __name__ == '__main__':
    main()
