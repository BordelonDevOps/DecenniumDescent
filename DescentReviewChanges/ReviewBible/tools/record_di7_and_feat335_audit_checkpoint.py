"""Register seven drafts and the completed scoped GPT audit, preserving predecessors."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def info(path):
    b = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def save(path, value, new=False):
    if new:
        assert not path.exists(), str(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def once(text, old, replacement):
    assert text.count(old) == 1, old[:100]
    return text.replace(old, replacement)


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_FLORA_ACQUISITION.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_AND_FEAT335_AUDIT.json'
    preservation = A / 'navigation-and-index-before-di7-and-feat335-audit'
    delta_path = A / 'DI7_AND_FEAT335_AUDIT_PROGRESS_DELTA.json'
    index_check_path = A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_AFTER_DI7_CHECK.json'
    reproduction_receipt = A / 'FEAT335_ACQUISITION_AUDIT_01_LOCAL_REPRODUCTION.json'
    assert all(not p.exists() for p in [checkpoint, preservation, delta_path, index_check_path])
    state = read(previous)
    report_path = A / 'DIVINATION_RANK7_OPERATING_PROPOSAL_CHECK.json'
    report = read(report_path)
    proposal_path = R / 'data/director/spell_proposals/divination_rank7.json'
    proposal = read(proposal_path)
    proposal_doc = R / 'docs/spells/proposals/DIVINATION_RANK7.md'
    assert report['failures'] == 0 and report['completeMechanicalProposals'] == 7 and report['authoredExamples'] == 14
    for rel, bound in report['artifacts'].items():
        assert {k: info(G / rel)[k] for k in ['bytes', 'sha256']} == bound
    observation_path = A / 'DI7_AUTHORING_GPT_STATUS.json'
    observation = read(observation_path)
    assert observation['stopVisible'] is False and observation['turnState'] == 'complete'
    downloaded_path = A / 'FEAT335_ACQUISITION_AUDIT_01_DOWNLOAD_CHECK.json'
    downloaded = read(downloaded_path)
    for bound in downloaded['returnedFiles'] + downloaded['frozenSubmittedFiles']:
        assert info(G / bound['path']) == bound
    reproduction_path = A / 'feat335-acquisition-audit-01-local-reproduction/REPRODUCTION_RESULTS.json'
    qa_path = A / 'feat335-acquisition-audit-01-local-qa/DELIVERABLE_QA.json'
    reproduced, qa = read(reproduction_path), read(qa_path)
    assert reproduced['counts']['checks'] == reproduced['counts']['passed'] == 4194 and reproduced['counts']['failed'] == 0
    assert qa['checks'] == qa['passed'] == 4917 and qa['failed'] == 0
    assert len(qa['operations']) == 14 and reproduced['counts']['reportedSnapshotMismatches'] == 559
    audit_root = A / 'feat335-acquisition-audit-01-verdict'
    audit_rows = read(audit_root / 'ACQUISITION_ROWS.json')['rows']
    assert len(audit_rows) == len({r['id'] for r in audit_rows}) == 335
    findings = read(audit_root / 'FINDINGS_AND_REPLACEMENTS.json')['findings']
    assert {f['id'] for f in findings} == {'FAA-01', 'FAA-02', 'FAA-03', 'FAA-04'}
    reproduction_record = {'recordedAtUtc': now, 'download': info(downloaded_path),
         'sourceAndModelCounterexamples': info(reproduction_path), 'deliverableGuardAndPreservationChecks': info(qa_path),
         'sourceChecks': 4194, 'deliverableChecks': 4917, 'failures': 0, 'all335RowParity': True,
         'correctedLiveFiles': 0, 'fullRuntimeCases': 0, 'originalReportSuitesRerun': False,
         'scope': 'Independent local execution against the exact frozen 198-payload submission. Original returned evidence and submitted files reverified byte-for-byte. This reproduces baseline defects and in-memory corrections; it does not fulfill the live correction/evidence work.'}
    if reproduction_receipt.exists():
        previous_record = read(reproduction_receipt)
        assert {k: v for k, v in previous_record.items() if k != 'recordedAtUtc'} == {k: v for k, v in reproduction_record.items() if k != 'recordedAtUtc'}
    else:
        save(reproduction_receipt, reproduction_record, new=True)

    index_path = R / 'data/director/higher_spell_operating_proposal_index.json'
    index_doc = R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md'
    nav = R / 'tools/build_review_map.py'
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    assert info(index_path) == state['higherSpellIndex'] and info(ledger_path) == state['coverageLedger']
    old_index, old_ledger = read(index_path), read(ledger_path)
    index, ledger = deepcopy(old_index), deepcopy(old_ledger)
    check_details = []

    def check(name, ok):
        check_details.append({'name': name, 'pass': bool(ok)})
        assert ok, name

    ids = {r['spellId'] for r in proposal['records']}
    for before, entry in zip(old_index['entries'], index['entries']):
        sid = entry['spellId']
        if sid in ids:
            check(sid + ' was a pre-push source question only', entry['scope'] == 'pre-push mechanics' and entry['proposalState'] == 'source-question-prepared-procedure-not-yet-proposed')
            entry.update({'proposalState': 'complete-unadopted-proposal', 'proposalFile': proposal_path.relative_to(G).as_posix(),
                          'proposalDocument': proposal_doc.relative_to(G).as_posix(), 'authoredExamples': 2})
            check(sid + ' no shared/review/approval promotion', not entry['jointReviewCompleted'] and not entry['sharedAsFeatComparison'] and not entry['dedicatedSpellReviewSubmitted'])
        else:
            check(sid + ' complete index entry unchanged', entry == before)
    counts = deepcopy(index['counts'])
    counts.update({'completeUnadoptedProcedures': 187, 'completeUnadoptedUnsentProcedures': 116,
                   'mechanicalProceduresStillToPropose': 201, 'authoredExamples': 374})
    check('187 complete drafts,201 remaining pre-push,47 post-push receipts',
          sum(e['proposalState'] == 'complete-unadopted-proposal' for e in index['entries']) == 187 and
          sum(e['proposalState'] == 'source-question-prepared-procedure-not-yet-proposed' for e in index['entries']) == 201 and
          sum(e['proposalState'] == 'post-push-literal-receipt-only' for e in index['entries']) == 47)
    check('71 comparison-only drafts and374 examples', sum(e['sharedAsFeatComparison'] for e in index['entries']) == 71 and sum(e['authoredExamples'] for e in index['entries']) == 374)
    ordinary_index = read(R / 'data/public/spell_playtests/authored_review_index.json')
    check('Ordinary authored statuses stay412/436', ordinary_index['authoredCounts'] == {'reviewed': 412, 'pending': 436})
    index.update({'status': 'Navigation only:187 complete unadopted procedures.71 shared only as feat comparisons;116 unsent. Dedicated higher-spell review remains pending.', 'createdAtUtc': now, 'counts': counts})
    for p in [proposal_path, proposal_doc, report_path, Path(__file__)]:
        index['inputs'][p.relative_to(G).as_posix()] = {k: info(p)[k] for k in ['bytes', 'sha256']}

    spell_scope = ('Seven rank-seven Divination procedures and fourteen authored examples are complete drafts, unadopted and unsent. '
        'All eight source records including Greater Planar Summons remain preserved. The142 source/context/rendering checks include four plain arithmetic checks, '
        'not runtime tests. Fourteen current counterparts include eight reviewed records, four earlier full drafts and two source-only unresolved counterparts '
        '(Cast Echo and Supreme Faction Omniscience). All17 class envelopes are retained. Fourteen issues await actual joint review. '
        'The higher index now records187 unadopted procedures/374 examples,201 remaining pre-push questions and47 literal post-push receipts; ordinary authored totals remain412/436.')
    feat_scope = ('Actual GPT completed FEAT335-ACQUISITION-AUDIT-01 with all335 individual source/initial-state dispositions and four findings. '
        'All21 returned payloads and198 submitted payloads are byte-verified; local reproduction passes4194 source/model-counterexample checks and4917 deliverable/guard checks. '
        'FAA-01 confirms the Flora provider omission already found locally; FAA-02 identifies excluded actual STR/DEX providers; FAA-03 supplies an explicit new narrow unarmed/Claws training bridge; '
        'FAA-04 identifies559 mutable saved comparison rows, not559 rule failures. Fourteen guarded edits and finite integration evidence remain unfulfilled. '
        'The recent Flora override/maneuver/gadget reports were not in the audited packet. No full acquisition, exact-feat, runtime or whole-game approval is inferred.')
    for row in ledger['aspects']:
        if row['id'] == 'DD-11':
            row.setdefault('completedScopes', []).append(spell_scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, proposal_doc])
        elif row['id'] in {'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(feat_scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [downloaded_path, reproduction_receipt, audit_root / 'FEAT335_ACQUISITION_AUDIT_VERDICT.md'])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'FEAT335-ACQUISITION-AUDIT-01-terminal', 'recordedAtUtc': now,
                'rows': 335, 'findings': [f['id'] for f in findings], 'guardedOperations': 14,
                'sourceChecks': 4194, 'deliverableChecks': 4917, 'correctionsFulfilled': False, 'fullFeatCandidateApproved': False})
            row['openIssues'].append('Fulfill FAA-01–04 and the finite remaining-work groups from the completed335-row audit. Recent Flora override overlaps FAA-01 but must be reconciled with STR/DEX routes and parent Trapcasting histories. Preserve historical559 snapshot discrepancies; rerun corrected capture checkpoints into new descendant evidence.')
    for old, new in zip(old_ledger['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in {'DD-11', 'DD-14', 'DD-69'}:
            assert old == new
    assert {k: v for k, v in old_ledger.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    nav_text = nav.read_text('utf-8')
    nav_text = once(nav_text, ' + coverage_deltas\n', ' + coverage_deltas + read(A / "DI7_AND_FEAT335_AUDIT_PROGRESS_DELTA.json")["changes"]\n')
    nav_text = once(nav_text, 'Higher-spell index has180 unadopted procedures/360 examples,208 remaining mechanical questions and47 post-push receipts.',
        'Higher-spell index has187 unadopted procedures/374 examples,201 remaining mechanical questions and47 post-push receipts.')
    nav_text = once(nav_text, state['status'], state['status'] + ' Later checkpoint: ' + spell_scope + ' ' + feat_scope)
    nav_text = once(nav_text, '    featured = [\n', '    featured = [\n        ("Seven rank-seven Divination drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/DIVINATION_RANK7.md"),\n')
    nav_text = once(nav_text, '    pending = [\n', '    pending = [\n' + '\n'.join('        (' + json.dumps(label) + ', ' + json.dumps(name) + '),' for label, name in [
        ('Completed335-row acquisition audit — actual GPT verdict', 'feat335-acquisition-audit-01-verdict/FEAT335_ACQUISITION_AUDIT_VERDICT.md'),
        ('335 individual acquisition and initial-state obligations', 'feat335-acquisition-audit-01-verdict/ACQUISITION_ROWS.md'),
        ('Four findings and guarded corrections', 'feat335-acquisition-audit-01-verdict/GUARDED_CORRECTIONS.json'),
        ('Finite acquisition evidence remaining', 'feat335-acquisition-audit-01-verdict/FINITE_REMAINING_WORK.json'),
        ('Independent local reproduction of the scoped audit', 'FEAT335_ACQUISITION_AUDIT_01_LOCAL_REPRODUCTION.json'),
        ('Divination rank7 source/rendering check', 'DIVINATION_RANK7_OPERATING_PROPOSAL_CHECK.json'),
        ('Owner stop condition:50 percent weekly usage', 'OWNER_USAGE_STOP_50_PERCENT_2026-10-13.json')]) + '\n')
    compile(nav_text, str(nav), 'exec')

    preserved = []
    for path in [index_path, index_doc, ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        target = preservation / path.relative_to(G)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        assert target.read_bytes() == path.read_bytes()
        preserved.append({**info(path), 'preservedCopy': target.relative_to(G).as_posix()})
    manifest_path = preservation / 'PRESERVATION_MANIFEST.json'
    save(manifest_path, preserved, new=True)
    index['previousIndex'] = next(x for x in preserved if x['path'] == index_path.relative_to(G).as_posix())
    save(index_path, index)
    def link(path):
        return Path(os.path.relpath(path, index_doc.parent)).as_posix()
    lines = ['# Higher spell operating proposal index', '', '**187 complete drafts; dedicated joint spell review pending.**', '',
        'Of435 higher-rank identities,388 have pre-push mechanical questions:187 now have procedures and374 authored examples;201 still need procedures. '
        'The47 remaining identities stay literal post-push receipts.71 drafts have been shared only as feat comparisons;116 remain unsent.', '',
        'Ordinary authored coverage remains412 reviewed/436 pending, including the separate deferred Blink. These drafts are not spell approvals or runtime/balance evidence.', '',
        '[Structured index](' + link(index_path) + ') · [Current preservation checks](' + link(index_check_path) + ')', '', '## Proposed groups', '']
    groups = {}
    for entry in index['entries']:
        if entry['proposalDocument']:
            groups.setdefault(entry['proposalDocument'], []).append(entry['spellId'])
    for path, members in groups.items():
        lines.append('- [' + Path(path).stem.replace('_', ' ').title() + '](' + link(G / path) + '):' + str(len(members)) + ' proposed procedures.')
    lines += ['', spell_scope, '', '## All higher-rank identities', '', '| Source question | Spell | Treatment | Evidence |', '| --- | --- | --- | --- |']
    labels = {'complete-unadopted-proposal': 'Procedure proposed; joint review pending', 'post-push-literal-receipt-only': 'Literal receipt; post-push',
              'source-question-prepared-procedure-not-yet-proposed': 'Source question prepared; procedure needed'}
    for entry in index['entries']:
        target = G / (entry['proposalDocument'] or entry['preparationFile'])
        lines.append('| ' + entry['questionId'] + ' | ' + entry['name'].replace('|', '\\|') + ' | ' + labels[entry['proposalState']] + ' | [Read](' + link(target) + ') |')
    lines += ['', 'Historical group descriptions and counts are preserved in the previous index copy; no original sources or prior audit artifacts were deleted.', '']
    index_doc.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    for target in set(re.findall(r'\[[^\]]*\]\(([^)]+)\)', index_doc.read_text('utf-8'))):
        check('Index link: ' + target, (index_doc.parent / target).resolve().is_file() or (index_doc.parent / target).resolve() == index_check_path)
    save(index_check_path, {'recordedAtUtc': now, 'scope': 'Only seven complete proposal entries added; all428 unrelated entries and all approval/shared states preserved.',
        'counts': counts, 'checks': len(check_details), 'failures': 0, 'details': check_details,
        'previousPreservation': info(manifest_path), 'artifacts': {p.relative_to(G).as_posix(): {k: info(p)[k] for k in ['bytes', 'sha256']} for p in [index_path, index_doc]}}, new=True)
    save(ledger_path, ledger)
    nav.write_text(nav_text, encoding='utf-8', newline='\n')
    changed = [index_path, index_doc, ledger_path, nav]
    save(delta_path, {'recordedAtUtc': now, 'status': 'Seven unadopted spell drafts and scoped terminal acquisition audit registered; corrections pending.',
        'changes': [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in changed],
        'aspectsChanged': ['DD-11', 'DD-14', 'DD-69'], 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'ownerDirectionUnchanged': True, 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0, 'fullFeatCandidateApproved': False}, new=True)
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr)
        raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress', 'previousCheckpoint': info(previous),
        'status': spell_scope + ' ' + feat_scope,
        'newSpellCohort': {'reviewStatus': 'unadopted and unsent', 'sourceIds': sorted(ids), 'completeProcedures': 7, 'authoredExamples': 14,
            'untouchedPostPushReceipts': ['planar-summons-greater'], 'currentWholeCounterparts': 14, 'reviewedCurrentCounterparts': 8,
            'earlierFullUnadoptedCounterparts': 4, 'counterpartsWithoutCompleteProposal': ['cast-echo', 'faction-omniscience-supreme'],
            'completeClassEnvelopes': 17, 'newJointIssues': 14, 'checks': 142, 'plainArithmeticChecks': 4, 'fullSpellRuntimeCases': 0,
            'receipt': info(report_path), 'artifacts': report['artifacts']},
        'higherSpellCounts': counts, 'higherSpellIndex': info(index_path), 'higherSpellIndexCheck': info(index_check_path), 'indexChecks': len(check_details),
        'featAcquisitionAudit': {'id': 'FEAT335-ACQUISITION-AUDIT-01', 'download': info(downloaded_path), 'localReproduction': info(reproduction_receipt),
            'rows': 335, 'returnedPayloads': 21, 'findings': [f['id'] for f in findings], 'guardedOperations': 14, 'correctionsFulfilled': False,
            'reportSnapshotDiscrepancies': 559, 'correctionPlan': info(audit_root / 'GUARDED_CORRECTIONS.json'),
            'remainingWork': info(audit_root / 'FINITE_REMAINING_WORK.json'), 'fullFeatCandidateApproved': False},
        'ownerUsageStopCondition': info(A / 'OWNER_USAGE_STOP_50_PERCENT_2026-10-13.json'),
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path), 'newRuleAdoptions': 0,
        'newRuleAdoptionCountScope': 'This checkpoint only; review findings have not been applied yet.'})
    state['activeGptReview'].update({'status': 'completed-scoped-acquisition-audit', 'pendingResponse': False, 'replyReceived': True,
        'awaitingGptResponse': False, 'finalVerdictReceived': True, 'finalVerdictScope': '335-row source/acquisition audit only; fourteen edits and finite evidence pending.',
        'latestObservation': info(observation_path), 'response': info(A / 'FEAT335_ACQUISITION_AUDIT_01_RESPONSE.txt'), 'replyId': None,
        'currentAuthoritativeObservation': 'Actual Chrome terminal response and full downloaded archive verified;4194+4917 scoped checks independently reproduced.'})
    state['safeNextActions'] = [
        'Check fresh account usage before substantial work and periodically. Owner requires stopping at50 percent used in the weekly allowance. At or above50 save progress, mark active goal paused under this explicit instruction, report usage and stop. Do not redeem a reset or purchase credits.',
        'Actual FEAT335-ACQUISITION-AUDIT-01 has completed. Do not resend or wait on the old request. Read all fourteen guarded operations and eighteen acceptance groups, then preserve current before-bytes and apply the necessary current descendants. The entire returned21-payload archive and198-payload submission are preserved;4194+4917 checks reproduced against frozen input.',
        'Reconcile FAA-01 with the newer FloraAcquisition override and its current-level capacity correction. FAA-02 requires actual STR/DEX source routes; the earlier mental-only Flora and provider evidence is incomplete for those routes. Update paid Conjure Flora-to-Trapcasting parent histories without weakening the separate Verdant Bond route.',
        'Apply the explicit FAA-03 unarmed/Claws source-composition rule to both shared envelopes and manuscript, then validate the finite source-bound profile cases. Do not expand the separate Weapon Master four-proficiency menu or add ongoing proficiency to Mastery.',
        'FAA-04 requires immutable deep-copy capture and new version-bound evidence. Preserve all old reports and559 discrepancies; never replace historical actual values with expected values. Old complete report totals remain historical scope, not proof of corrected snapshots.',
        'Use FINITE_REMAINING_WORK and ACCEPTANCE_EXPECTATIONS to finish shared-owner pools, delayed/empty/capacity states, fixed snapshots/training and common finite descriptors.177 ordinary descriptors and111 no-new-state entries are not hundreds of bespoke fixture requests. Preserve conditional/null scopes; later full assembled feat exact review remains mandatory.',
        'Carry the post-submission maneuver243/gadget269/Flora165 reports into final integration with their exact limits. Reconcile the confirmed Flora gap rather than treating the newer override as proof of all FAA01/02 scopes.',
        'Higher spells now187 complete unadopted procedures/374 examples with201 pre-push questions still to author;116 drafts unsent and71 only shared as feat comparisons. DI7 seven procedures are source-preserved drafts, not approved spells. Review the explicit alignment-layer proposal and other fourteen DI7 issues with actual GPT.',
        'Continue remaining bestiary, Director, cross-system integration and source-preserving packaging. Final actual joint whole-game flow agreement precedes authorized GitHub push; verify remote commit before careful cosmology review. No deletion or full approval occurred.'
    ]
    state.setdefault('preservationManifests', []).append(info(manifest_path))
    save(checkpoint, state, new=True)
    print(json.dumps({'checkpoint': info(checkpoint), 'higherSpellCounts': counts, 'sourceChecks': 4194, 'deliverableChecks': 4917,
                      'indexChecks': len(check_details), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0}, indent=2))


if __name__ == '__main__':
    main()
