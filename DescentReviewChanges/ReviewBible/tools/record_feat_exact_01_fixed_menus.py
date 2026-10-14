"""Record five finite acquisition-menu passes with preserved ledger history."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ05_FULFILLMENT.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_FIXED_MENUS.json'
    delta_path = A / 'FEAT_EXACT_01_FIXED_MENUS_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-fixed-menus'
    assert all(not p.exists() for p in [target, delta_path, preservation])
    report_path = A / 'FEAT_EXACT_01_FIXED_MENUS_CHECK.json'; report = read(report_path)
    notes_path = A / 'FEAT_EXACT_01_FIXED_MENUS_NOTES.md'
    assert report['checks'] == 1282 and not report['failures'] and all(x['passed'] for x in report['results'])
    assert len(report['traces']) == 203 and report['counts']['advancedPairCombinations'] == 90
    assert report['counts']['newPartialPrerequisiteIdentities'] == 0
    for bound in report['sourceBindings']:
        assert info(G / bound['path']) == bound
    state = read(previous)
    assert info(G / state['coverageLedger']['path']) == state['coverageLedger']
    assert read(G / state['featACQ05FiniteFulfillment']['path'])['onlyThisNamedIssueClosed']
    scope = ('Five fixed feat acquisition menus now have1282 passing checks across203 recorded histories. '
        'All15 Martial Adept pairs and90 distinct Advanced extensions are covered with both available and spent parent dice; '
        'the Advanced acquisition adds only its new available d6. All3 Metamagic pairs and10 elemental selections are covered '
        'with actual source-qualified payment/casting predicates, nonrepeatability and no invented RP/class/spell grants. '
        'These are selection/initialization slices, not attacks, spell effects, recovery or complete builds. '
        'The335 partial prerequisite count is unchanged; remaining mandatory selections and full use validation remain open.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'FIVE-FIXED-ACQUISITION-MENUS', 'recordedAtUtc': now,
            'checks': 1282, 'recordedHistories': 203, 'identities': report['cohort'], 'counts': report['counts'],
            'partialPrerequisiteIdentities': 335, 'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve earlier mandatory-choice scope before five fixed-menu acquisition passes.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] += (' Five additional acquisition-menu slices are now recorded: Martial Adept, Advanced Martial Adept, '
                'Metamagic Adept, Elemental Adept and Elemental Mastery. Their maneuver/cast/damage/recovery effects remain distinct use work. '
                'Continue skill/tool/language selections, remaining fixed casting abilities/routes/sigils/cantrip choices, weapon profiles '
                'and all relevant initialization; do not infer complete acquisition coverage from keyword scans or partial prerequisite counts.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT327_ACQ_05_FULFILLMENT_COVERAGE_DELTA.json",'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_FIXED_MENUS_COVERAGE_DELTA.json",')
    anchor = '        ("Eight half-feats — scope", "FEAT_EXACT_01_HALF_FEAT_CHOICES_NOTES.md"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Martial, metamagic and elemental menus — evidence', report_path.name),
        ('Martial, metamagic and elemental menus — scope', notes_path.name)]:
        addition += '\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(file) + '),'
    text = text.replace(anchor, addition)
    anchor = state['status']; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + ' ' + scope)
    compile(text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        bound = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert path.read_bytes() == dest.read_bytes()
        saved.append({**bound, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta_path, {'recordedAtUtc': now, 'status': 'verified-scoped-fixed-menu-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / 'FEAT327_ACQ_05_FULFILLMENT_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: ACQ05 source and20 bounded lifecycle acceptance groups fulfilled',
        'previousCheckpoint': info(previous), 'status': scope,
        'featFixedMenusPass': {'report': info(report_path), 'notes': info(notes_path), 'checks': 1282,
            'histories': 203, 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'No new rule; finite acquisition choices and initialization under existing complete procedures.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path)})
    state['safeNextActions'] = [
        'Continue the remaining permanent acquisition menus from current complete contracts. Prioritize Skilled/Jack of All Trades/Cultural Expert and Linguist/Polyglot, reusing actual source training/language records with explicit conditional access. Do not confuse a later use-time choice with an acquisition menu.',
        'Other surfaced fixed-choice work includes Arcane Pulse, Cantrip Mastery, Elemental Affinity, Fey/Shadow Touched, Ritual Caster, Telekinetic/Telepathic, full Forbidden Pact sigils, Hemocraft ability and Soul Cage casting provider. This surfaced list is not an exhaustive335-choice audit; inspect each full procedure and existing evidence before declaring its coverage.',
        'Verify Weapon Focus/Mastery exact-profile choices against the current40 completed equipment weapon profiles and actual proficiency; preserve specific source-qualified unarmed/natural possibilities without inventing an umbrella or excluding them solely from equipment menus.',
        'The five fixed-menu acquisition passes now have1282 checks/203 histories. Full maneuver, metamagic, elemental damage and resource/recovery effects remain use work. ACQ05 is fulfilled within20 bounded groups; do not resubmit its unchanged question.',
        'Complete all remaining FXC04–10 supplements/choices/initialization, clocks, damage/resources, command/custody/mount and casting/copy behavior, then all660 original cases plus28 additions and actual full assembled GPT review.',
        'Continue ordinary/higher SPELL catalogs and remaining bestiary/Director content. Carry reviewed crafting/language/onboarding/EX58 and owner CRPG/12-character/parallel-activity/host-permission direction. Final joint whole-game flow precedes authorized push, remote verification and careful cosmology review; implementation and human balance remain separate.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
        'checks': 1282, 'histories': 203, 'fullAcquisitionsComplete': False}, indent=2))


if __name__ == '__main__':
    main()
