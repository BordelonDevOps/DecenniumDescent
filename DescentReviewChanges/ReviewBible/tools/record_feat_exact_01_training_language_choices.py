"""Preserve and record five bounded skill/tool/language acquisition passes."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_FIXED_MENUS.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_TRAINING_LANGUAGE_CHOICES.json'
    delta = A / 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-training-language-choices'
    assert all(not p.exists() for p in [target, delta, preservation])
    report_path = A / 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_CHECK.json'; report = read(report_path)
    notes_path = A / 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_NOTES.md'
    assert report['checks'] == 623 and not report['failures'] and all(r['passed'] for r in report['results'])
    assert len(report['traces']) == 228 and report['counts']['jackPairs'] == 91
    assert report['counts']['languageTriples'] == 40 and report['counts']['newPartialPrerequisiteIdentities'] == 0
    for bound in report['sourceBindings']:
        assert info(G / bound['path']) == bound
    state = read(previous)
    assert info(G / state['coverageLedger']['path']) == state['coverageLedger']
    scope = ('Skilled, Jack of All Trades, Cultural Expert, Linguist and Polyglot now have623 passing checks across228 recorded histories. '
        'The finite source slice covers8 ordered skill/tool patterns,14 initially untrained skills, all42 profiled tools/16 primary trades, '
        'all91 pairs of those untrained skills and40 language triples over the explicit admitted-contact list. '
        'It distinguishes true proficiency from half-PB, fixed contextual Expertise and bounded History; records actual language modes, '
        'partial knowledge, duplicates, exhaustion and Polyglot family anchors; and preserves permanent INT gates and separate payments. '
        'Culture/Lore/contact/saturation and later training changes are explicit conditional premises, not authenticated canon or campaign facts. '
        'No source rule changes or broader335-acquisition, recognition-use, whole-game, software or cosmology approval are claimed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'TRAINING-LANGUAGE-CHOICE-PASS', 'recordedAtUtc': now,
            'checks': 623, 'histories': 228, 'identities': report['cohort'], 'counts': report['counts'],
            'partialPrerequisiteIdentities': 335, 'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve prior mandatory-choice status before skill/tool/language selection evidence.',
                'openIssues': deepcopy(row['openIssues'])})
            old = ('Continue skill/tool/language selections, remaining fixed casting abilities/routes/sigils/cantrip choices, weapon profiles '
                'and all relevant initialization; do not infer complete acquisition coverage from keyword scans or partial prerequisite counts.')
            assert row['openIssues'][1].count(old) == 1
            row['openIssues'][1] = row['openIssues'][1].replace(old,
                'Skilled, Jack of All Trades, Cultural Expert, Linguist and Polyglot now have bounded623-check/228-history selection evidence; '
                'their full task/recognition/use scope remains separate. Continue remaining fixed casting abilities/routes/sigils/cantrip choices, '
                'exact weapon profiles, relevant initialization and the full335 acquisition audit; keyword scans and partial prerequisite counts do not establish completion.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_FIXED_MENUS_COVERAGE_DELTA.json",'; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_COVERAGE_DELTA.json",')
    anchor = '        ("Martial, metamagic and elemental menus — scope", "FEAT_EXACT_01_FIXED_MENUS_NOTES.md"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Skill, tool and language choices — evidence', report_path.name),
        ('Skill, tool and language choices — scope', notes_path.name)]:
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
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-scoped-training-language-choice-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_FIXED_MENUS_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: five martial/metamagic/elemental fixed acquisition menus',
        'previousCheckpoint': info(previous), 'status': scope,
        'featTrainingLanguageChoicePass': {'report': info(report_path), 'notes': info(notes_path),
            'checks': 623, 'histories': 228, 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'No new rule; bounded skill/tool/language selection and training contribution evidence.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    state['safeNextActions'] = [
        'The five skill/tool/language choice slices now have623 checks/228 histories. Preserve the existing reviewed language/crafting rules and conditional evidence limits; no knowledge or cosmology was authored. Full skill/language use scenarios remain separate.',
        'Continue permanent casting-ability/route/spell choices from full current contracts: Arcane Pulse, Cantrip Mastery, Fey/Shadow Touched, Ritual Caster, Telekinetic/Telepathic, full Forbidden Pact sigils, Hemocraft ability and Soul Cage provider. Inspect exact source spell availability and prior evidence before claiming complete acquisitions.',
        'Complete Elemental Affinity and remaining exact weapon-profile selections/initialization. The surfaced menu list is not an exhaustive335-feat acquisition audit. Review complete procedures and preserve specific source-qualified natural/unarmed choices without inventing general proficiency.',
        'ACQ05 is fulfilled within its20 bounded conditional groups; no unchanged source resubmission. Five martial/metamagic/elemental menus have1282 checks, but their use/resource/damage interactions remain distinct work.',
        'Complete all remaining FXC04–10 supplements/choices/initialization, clocks/recovery, damage/resources, actual command/custody/mount and casting/copy behavior, all660 original cases plus28 additions, then actual full assembled feat review.',
        'Continue ordinary/higher SPELL catalogs and remaining bestiary/Director content. Carry owner CRPG/12-character/parallel-activity/host-permission direction and completed crafting/language/onboarding/EX58. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology; implementation and human balance remain separate.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'checks': 623, 'histories': 228}, indent=2))


if __name__ == '__main__':
    main()
