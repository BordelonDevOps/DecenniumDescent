"""Preserve and record eleven finite casting acquisition selection passes."""
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
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_TRAINING_LANGUAGE_CHOICES.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_CASTING_SELECTIONS.json'
    delta = A / 'FEAT_EXACT_01_CASTING_SELECTIONS_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat-casting-selections'
    assert all(not p.exists() for p in [target, delta, preservation])
    report_path = A / 'FEAT_EXACT_01_CASTING_SELECTIONS_CHECK.json'; report = read(report_path)
    notes_path = A / 'FEAT_EXACT_01_CASTING_SELECTIONS_NOTES.md'
    assert report['checks'] == 1999 and not report['failures'] and all(r['passed'] for r in report['results'])
    assert len(report['traces']) == 232 and report['counts']['touchedAbilityHistories'] == 192
    assert report['counts']['touchedSourcePlacements'] == 374 and report['counts']['newPartialPrerequisiteIdentities'] == 0
    for bound in report['sourceBindings']: assert info(G / bound['path']) == bound
    state = read(previous)
    assert info(G / state['coverageLedger']['path']) == state['coverageLedger']
    scope = ('Eleven permanent casting/route selection slices now have1999 passing checks across232 recorded histories. '
        'All64 Fey/Shadow Touched identity/school entries have three ability histories each, with374 exact source-class placements independently resolved. '
        'The evidence also covers all7 Forbidden Pact nested sigil branches, fixed mental abilities, no free ritual book/formula, '
        'empty Hemocraft reserve, Elemental Affinity types, exact known cantrip witnesses and Soul Cage actual-provider/shared-pool preservation. '
        'Existing ACQ03 already requires a legitimate mandatory casting-source choice even where a retained Lifeleech parent satisfies the printed OR predicate; no default DC or new source rule is invented. '
        'The passes preserve classless feat access, original spell identities and separate initial charges without enabling runtime selection. '
        'Full casting, damage, costs, recovery, all335 acquisitions, exact assembled review and whole-game approval remain open.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] not in changed: continue
        row.setdefault('completedScopes', []).append(scope)
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, notes_path])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'ELEVEN-CASTING-SELECTIONS', 'recordedAtUtc': now,
            'checks': 1999, 'histories': 232, 'identities': report['cohort'], 'counts': report['counts'],
            'partialPrerequisiteIdentities': 335, 'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve prior casting-selection open work before eleven bounded acquisition passes.',
                'openIssues': deepcopy(row['openIssues'])})
            old = ('Continue remaining fixed casting abilities/routes/sigils/cantrip choices, '
                'exact weapon profiles, relevant initialization and the full335 acquisition audit; keyword scans and partial prerequisite counts do not establish completion.')
            assert row['openIssues'][1].count(old) == 1
            row['openIssues'][1] = row['openIssues'][1].replace(old,
                'Eleven casting-selection slices now cover the fixed abilities, Touched pools, all Pact sigils, Ritual Caster empty grant, '
                'Elemental Affinity, named known-cantrip witnesses and actual Soul Cage providers with1999 checks/232 histories. '
                'They do not execute full casts, every casting engine, spell learning or resource effects. '
                'Continue exact weapon-profile choices, remaining initialization and the full335 acquisition audit; keyword scans and partial counts do not establish completion.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_COVERAGE_DELTA.json",'; assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_CASTING_SELECTIONS_COVERAGE_DELTA.json",')
    anchor = '        ("Skill, tool and language choices — scope", "FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_NOTES.md"),'
    assert text.count(anchor) == 1
    addition = anchor
    for label, file in [('Casting selections — eleven-feat evidence', report_path.name),
        ('Casting selections — scope and spell placement limits', notes_path.name)]:
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
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-scoped-casting-selection-progress',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(report_path), info(notes_path)],
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: five skill/tool/language selection passes',
        'previousCheckpoint': info(previous), 'status': scope,
        'featCastingSelectionsPass': {'report': info(report_path), 'notes': info(notes_path),
            'checks': 1999, 'histories': 232, 'counts': report['counts'], 'limits': report['limits']},
        'newRuleAdoptions': 0, 'newRuleAdoptionCountScope': 'This checkpoint only; not cumulative.',
        'newRuleAdoptionScope': 'No new source rule; existing ACQ03 and complete source-authoring procedures govern required permanent selections.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta)})
    state['safeNextActions'] = [
        'Continue Weapon Focus/Weapon Mastery exact-profile choices against current40 completed equipment weapon profiles and actual proficiency. Preserve legitimate specifically sourced natural/unarmed options without inventing an umbrella or suppressing them simply because they are outside the equipment menu.',
        'Audit every current335 full acquisition contract for remaining fixed choices and initial fields; the many partial prerequisite/selection passes do not collectively prove full335 acquisition completion. Carry forward their exact source and conditional limits.',
        'Eleven casting selections now have1999 checks/232 histories, including64 Touched entries,192 ability histories and374 source placements. The full source pools are retained under magic_core_feat_operating_proposal_internal.json/currentChoicePools. No pool was silently reduced to one class or school.',
        'Ritual Caster learning/casting, full Cantrip Mastery effects, actual Soul Cage/DC-provider use and all Pact/Telepathic/Telekinetic/Touched casts remain separate execution work. Hemocraft and Lifeleech reserve/death/resource behavior retain their existing source limits. ACQ03 controls the mandatory-provider edge case; no new default ability or cosmology interpretation was adopted.',
        'Complete remaining FXC04–10 finite supplements, initial resources, clocks/recovery, damage/resource causality, command/custody/mount and casting/copy interactions, all660 original cases plus28 additions, then actual assembled full-feat GPT review.',
        'Continue ordinary/higher SPELL catalogs and bestiary/Director content. Preserve owner CRPG/12-character/parallel-activity/host-permission direction and completed crafting/language/onboarding/EX58. Actual final joint whole-game flow precedes authorized push, verified remote and careful cosmology; software and human balance remain separate.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest)); write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'checks': 1999, 'histories': 232}, indent=2))


if __name__ == '__main__':
    main()
