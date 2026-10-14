"""Record finite choice progress and received/applied ACQ-05 source directions.

One-use checkpoint update. Preserve predecessors and immutable test reports.
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


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PRODIGY_AND_ACQ05_SUBMISSION.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHOICES_AND_ACQ05_SOURCE.json'
    delta = A / 'FEAT_EXACT_01_CHOICES_AND_ACQ05_SOURCE_COVERAGE_DELTA.json'
    correction_path = A / 'FEAT_EXACT_01_CHOICES_AND_ACQ05_VALIDATOR_CORRECTIONS.json'
    preservation = A / 'navigation-and-coverage-before-choices-and-acq05-source'
    assert all(not p.exists() for p in [target, delta, correction_path, preservation])
    trade_path = A / 'FEAT_EXACT_01_TRADE_SELECTIONS_CHECK.json'
    half_path = A / 'FEAT_EXACT_01_HALF_FEAT_CHOICES_CHECK.json'
    source_path = A / 'FEAT327_ACQ_05_INDEPENDENT_DESCENDANT_CHECK.json'
    trade, half, source = [read(p) for p in [trade_path, half_path, source_path]]
    operation_path = A / 'FEAT327_ACQ_05_DERIVED_OPERATIONS.json'
    operations = read(operation_path)
    altered = {c['after']['path']: c for c in operations['changes']}
    for report, count in [(trade, 404), (half, 569), (source, 272)]:
        assert report['checks'] == count and not report['failures'] and all(c['passed'] for c in report['results'])
        for bound in report.get('sourceBindings', []):
            actual = info(G / bound['path'])
            if actual != bound:
                change = altered[bound['path']]
                assert {k: change['before'][k] for k in bound} == bound and actual == change['after']
                assert info(G / change['before']['preservedCopy'])['sha256'] == bound['sha256']
    assert trade['counts']['recordedHistories'] == 147 and trade['counts']['allMenuPositiveCases'] == 54
    assert half['counts']['recordedTraces'] == 181 and half['counts']['currentReviewedWeaponProfiles'] == 40
    drafts = A / 'half-feat-check-before-catalog-correction'
    correction = {'recordedAtUtc': now,
        'scope': 'Local validator/model draft corrections before immutable passing reports; no game source changed to fit a test.',
        'corrections': [
            {'id': 'reviewed-weapon-menu',
             'preservedDrafts': [info(drafts / 'feat_exact_01_half_feat_choices.py'), info(drafts / 'validate_feat_exact_01_half_feat_choices.py')],
             'failure': 'Initial assumed38 count used an old source catalog including Unarmed Strike; the first filter also omitted three completed profiles with singular Weapon categories.',
             'sourceResolution': 'The current reviewed equipment candidate has37 other complete weapon profiles plus Kama, Nunchaku and Repeating Heavy Crossbow:40. Unarmed Strike is not a selectable weapon profile here. The corrected model includes the three current profiles and their applicable first-class training.',
             'finalEvidence': info(half_path)},
            {'id': 'monk-resource-growth-expectation',
             'preservedDraft': info(drafts / 'validate_after_catalog_before_monk_expectation_fix.py'),
             'failure': 'The local expected Monk12 maximum RP was incorrectly9.',
             'sourceResolution': 'The actual source progression gives maximum12 at level12. The corrected expectation retains current RP1 without refill.',
             'finalEvidence': info(half_path)},
            {'id': 'internal-candidate-record-count',
             'preservedDraft': info(A / 'ACQ05_DESCENDANT_VALIDATOR_BEFORE_INTERNAL_COUNT_CORRECTION.py'),
             'failure': 'The independent preservation validator incorrectly expected335 entries in the internal records array.',
             'sourceResolution': 'The unchanged internal structure has327 candidate records,8 separately retained reviewed feats and335 original-registry entries. Public candidate and contracts each have335 entries. The corrected check verifies these actual structures.',
             'finalEvidence': info(source_path)}],
        'oldReportsOverwritten': False, 'sourceInformationDeleted': False, 'newRulesAdoptedByCorrections': False}
    write_new(correction_path, correction)
    choices_scope = ('Trade-selection acquisition evidence has404 passing checks across147 histories, all19 artisan-tool and16 primary-discipline options. '
        'Eight half-feats have569 passing checks across181 traces,18 ability menu entries, score boundaries16/19/20, '
        'all40 complete reviewed weapon profiles, source-earned armor chains and nonhealing HP/resource growth. '
        'These are finite acquisition/initialization slices with stated conditional limits; full effects, all335 acquisitions and software are not established. '
        'No new prerequisite identities are added to the existing335 partial index.')
    source_scope = ('Actual GPT ACQ-05 reply bda5be25-7b23-4bd0-8afb-8adbb01a18f7 resolves Animal Companion paid ownership before bonding, '
        'attempt expenditure at a valid start, interruption, post-ending beneficial-rest gates and engine-specific replacement/transfer costs. '
        'Its96 source checks reproduce locally. Seven guarded replacements affect only five existing files;272 independent preservation/parity checks pass. '
        'All originals, historical sourceDirection, old model/report, other procedures and approval flags are preserved. '
        'The new twenty-group lifecycle behavior pass remains outstanding; source adoption is not full feat approval.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before)
    changed = {'DD-06', 'DD-14', 'DD-69'}
    decision_path = A / 'FEAT327_ACQ_05_RECEIVED_DECISION.json'
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('completedScopes', []).extend([choices_scope, source_scope])
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [trade_path, half_path, source_path, correction_path])
        row.setdefault('reviewEvidence', []).append(decision_path.relative_to(G).as_posix())
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'CHOICES-AND-ACQ05-SOURCE', 'recordedAtUtc': now,
            'tradeChecks': 404, 'halfFeatChecks': 569, 'sourcePreservationChecks': 272,
            'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0,
            'acq05SourceApplied': True, 'acq05BehavioralAcceptanceComplete': False,
            'all335AcquisitionsComplete': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now, 'status': row['status'],
                'reason': 'Preserve pre-reply ACQ05 pending status and earlier mandatory-choice scope.',
                'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = ('All335 identities retain disjoint partial prerequisite evidence. Prodigy ordered choices, '
                'three trade-training feat selections and eight half-feat ability/equipment choices now have the bounded evidence recorded here. '
                'Continue remaining mandatory choices and full initialization/use. ACQ-05 is received and its seven exact changes are applied; '
                'do not resend the settled source question. Execute the20 named lifecycle acceptance groups using distinct paid purchase, spent start, '
                'completion/interruption and real rest facts. The old110-check companion model/report remains historical, not the new timing rule. '
                'ACQ-04 is fulfilled. Full335 acquisition/use, the660 original examples and complete assembled GPT review remain open.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav = R / 'tools/build_review_map.py'; nav_text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_PRODIGY_AND_ACQ05_COVERAGE_DELTA.json",'
    assert nav_text.count(anchor) == 1
    nav_text = nav_text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_CHOICES_AND_ACQ05_SOURCE_COVERAGE_DELTA.json",')
    anchor = '    chain = list(entries.values()) + acq03["changes"] + acq04["changes"] + coverage_deltas'
    assert nav_text.count(anchor) == 1
    nav_text = nav_text.replace(anchor, '    acq05 = read(A / "FEAT327_ACQ_05_DERIVED_OPERATIONS.json")\n    chain = list(entries.values()) + acq03["changes"] + acq04["changes"] + acq05["changes"] + coverage_deltas')
    anchor = '        ("Prodigy — scope and limits", "FEAT_EXACT_01_PRODIGY_CHOICES_NOTES.md"),'
    assert nav_text.count(anchor) == 1
    links = [
        ('Trade-training selections — evidence', trade_path.name),
        ('Trade-training selections — scope', 'FEAT_EXACT_01_TRADE_SELECTIONS_NOTES.md'),
        ('Eight half-feats — ability and training choices', half_path.name),
        ('Eight half-feats — scope', 'FEAT_EXACT_01_HALF_FEAT_CHOICES_NOTES.md'),
        ('Companion lifecycle — actual GPT reply', 'FEAT327_ACQ_05_GPT_RESPONSE.json'),
        ('Companion lifecycle — controlling addendum', 'feat327-acq05-source/FEAT327_ACQ05_CONTROLLING_ADDENDUM.md'),
        ('Companion lifecycle — preserved exact source changes', operation_path.name),
        ('Companion lifecycle — independent preservation checks', source_path.name),
        ('Companion lifecycle — twenty outstanding acceptance groups', 'feat327-acq05-source/ACQ05_ACCEPTANCE_EXPECTATIONS.json'),
        ('Local validator corrections — retained draft evidence', correction_path.name)]
    nav_text = nav_text.replace(anchor, anchor + ''.join('\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(file) + '),' for label, file in links))
    # Replace only the immediately prior current-status paragraph; its complete
    # predecessor remains preserved in the checkpoint and map snapshots.
    previous_scope = read(previous)['status']
    assert nav_text.count(previous_scope) == 1
    nav_text = nav_text.replace(previous_scope, choices_scope + ' ' + source_scope)
    compile(nav_text, str(nav), 'exec')
    saved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        binding = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert path.read_bytes() == dest.read_bytes()
        saved.append({**binding, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta, {'recordedAtUtc': now, 'status': 'verified-scoped-choices-and-source-adoption',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'validation': [info(p) for p in [trade_path, half_path, source_path]],
        'sourceOperations': info(operation_path),
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_PRODIGY_AND_ACQ05_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 335, 'newPartialPrerequisiteIdentities': 0, 'fullFeatCandidateApproved': False})
    nav.write_text(nav_text, encoding='utf-8', newline='\n')
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state = read(previous); decision = read(decision_path)
    prior_review = deepcopy(state['activeGptReview'])
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'progress: Prodigy choices and actual ACQ05 submission',
        'previousCheckpoint': info(previous), 'status': choices_scope + ' ' + source_scope,
        'featTradeSelectionPass': {'report': info(trade_path), 'checks': 404, 'histories': 147, 'counts': trade['counts'], 'limits': trade['limits']},
        'featHalfFeatChoicePass': {'report': info(half_path), 'checks': 569, 'traces': 181, 'counts': half['counts'], 'limits': half['limits']},
        'featACQ05SourceApplication': {'operations': info(operation_path), 'independentVerification': info(source_path),
            'reviewerChecksReproduced': 96, 'independentChecks': 272, 'behavioralAcceptanceComplete': False,
            'acceptanceGroupsRemaining': 20, 'sourceInformationDeleted': False},
        'activeGptReview': {'id': 'FEAT327-ACQ-05', 'status': 'reply-received-source-applied-twenty-behavioral-groups-outstanding',
            'replyReceived': True, 'replyMessageId': decision['replyMessageId'], 'chatUrl': decision['chatUrl'],
            'browserId': decision['browserId'], 'tabId': decision['tabId'], 'decision': info(decision_path),
            'pendingResponse': False, 'noUnchangedResubmissionRequired': True, 'wholeExactCandidateApproved': False},
        'newRuleAdoptions': 1, 'newRuleAdoptionCountScope': 'This checkpoint only; not a cumulative count of all prior addenda.',
        'newRuleAdoptionScope': 'One actual GPT ACQ05 narrow lifecycle addendum: purchase/bond distinction, start expenditure, interruption/rest chronology and corrected replacement/transfer costs. No full feat/class promotion.',
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta),
        'validatorDraftCorrections': info(correction_path),
        'navigationBindingPolicy': 'Explicit preserved coverage deltas and measured ACQ01/02/03/04/05 source changes; no blanket hash exceptions.'})
    state['featCompanionAcquisition']['historicalScopeAfterACQ05'] = ('Preserved110-check/30-history completed-hour slice predates ACQ05. '
        'Its four HP endpoints remain compatible; completion-first payment does not govern the current lifecycle. Use a new derived model, not an in-place rewrite of this evidence.')
    state.setdefault('priorCompletedGptObservations', []).append({'recordedAtUtc': now, 'supersededObservation': prior_review,
        'reason': 'Terminal actual reply captured, downloaded, verified and applied; response is no longer pending.'})
    state['safeNextActions'] = [
        'ACQ05 source work is applied and independently verified. Do not resend the settled question. Build a new lifecycle model/history adapter preserving the old model/report, execute all20 named groups against the exact source addendum, and then record finite fulfillment.',
        'Prove separately paid ownership without an animal, valid-start attempt expenditure, interruption/no refund, rest epochs, release/replacement, same-body rebond, receiving-owner history, distinct Ranger gates, physical/control conservation and child ownership. Conditional fixtures must never authenticate actual campaign events.',
        'The three trade-training and eight half-feat selection passes are complete within their stated scopes. Preserve their original pre-ACQ05 input hashes and follow the measured operations to current descendants. Continue other mandatory choices and full initialization/use for all335 identities.',
        'Complete FXC04–10 supplements, clocks/recovery, damage/resource causality, custody/commands, casting/copy and all660 original case premises plus28 authored additions. Then obtain actual assembled exact-candidate GPT review.',
        'Ordinary spells remain412 reviewed/436 pending. Higher SPELLS have435 identities, including180 unadopted drafts and208 still requiring pre-push proposal work; these counts do not describe Arch/Hero classes.',
        'Carry forward reviewed crafting/language/onboarding/EX58 and owner CRPG/12-character/parallel-activity/host-permission direction. Complete remaining creatures/Director content and joint whole-game flow; then authorized commit/push, verify remote, carefully review cosmology and perform preservation-based cleanup. CRPG implementation and human balance testing remain separate later work.'
    ]
    state.setdefault('preservationManifests', []).extend([info(manifest), operations['preservationManifest']])
    write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
        'tradeChecks': 404, 'halfFeatChecks': 569, 'independentSourceChecks': 272,
        'acq05BehavioralGroupsRemaining': 20, 'pushed': False, 'cosmologyReviewed': False}, indent=2))


if __name__ == '__main__':
    main()
