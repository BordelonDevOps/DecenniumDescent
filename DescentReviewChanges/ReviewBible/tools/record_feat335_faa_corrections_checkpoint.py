"""One-use current-source register and preserved navigation checkpoint for FAA01-04."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

G = Path('C:/Github/DecenniumDescent')
R = G/'DescentReviewChanges/ReviewBible'
A = G/'docs/audit/2026-10-08/full-game'
V = A/'feat335-acquisition-audit-01-verdict'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    now = datetime.now(timezone.utc).isoformat()
    old_checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_AND_FEAT335_AUDIT.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FAA_CORRECTIONS.json'
    register = A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH.json'
    verification = A/'FEAT335_FAA_CORRECTIONS_CURRENT_BINDING_CHECK.json'
    preservation = A/'navigation-before-feat335-faa-corrections'
    delta = A/'FEAT335_FAA_CORRECTIONS_PROGRESS_DELTA.json'
    assert all(not p.exists() for p in [checkpoint, register, verification, preservation, delta])
    state = read(old_checkpoint)
    receipt_names = ['FEAT335_ACQUISITION_AUDIT_01_DERIVED_OPERATIONS.json',
        'FEAT335_FAA_FOLLOWTHROUGH_DERIVED_OPERATIONS.json',
        'FEAT335_FAA04_NUMERIC_BINDING_ADAPTATION.json',
        'FEAT335_FAA03_PROFILE_BRIDGE_DERIVED_OPERATIONS.json']
    receipts = [read(A/n) for n in receipt_names]
    chain = [x for receipt in receipts for x in receipt['changes']]
    checks = []

    def check(label, truth):
        checks.append({'id': label, 'passed': bool(truth)})
        assert truth, label

    def bound(binding, label):
        # Traverse only recorded preserved before->after descendants of this turn.
        path = G/binding['path']
        actual = info(path)
        expected = {k: binding[k] for k in ['path', 'bytes', 'sha256']}
        visited = set()
        while expected != actual:
            key = (expected['path'], expected['sha256'])
            check(label+'/no-cycle/'+str(len(visited)), key not in visited)
            visited.add(key)
            matches = [x for x in chain if all(x['before'][k] == expected[k] for k in expected)]
            check(label+'/one-exact-descendant/'+str(len(visited)), len(matches) == 1)
            entry = matches[0]
            preserved = info(G/entry['before']['preservedCopy'])
            check(label+'/preserved-before/'+str(len(visited)), all(preserved[k] == expected[k] for k in ['bytes', 'sha256']))
            check(label+'/same-path/'+str(len(visited)), entry['after']['path'] == expected['path'])
            expected = entry['after']
        check(label+'/current-file-exact', actual == expected)

    for i, entry in enumerate(chain):
        old = info(G/entry['before']['preservedCopy'])
        check('operation/'+str(i)+'/before-byte-preserved', all(old[k] == entry['before'][k] for k in ['bytes', 'sha256']))
        bound(entry['after'], 'operation/'+str(i)+'/after')
    check('fourteen-GPT-guarded-edits-ten-files', receipts[0]['operationCount'] == 14 and receipts[0]['changedFiles'] == 10)
    for i, b in enumerate(receipts[0]['unchangedHistoricalAndSourceFiles']):
        bound(b, 'retained-history-or-source/'+str(i))

    report_names = [
        'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_FAA04_CHECK.json',
        'FEAT_EXACT_01_NUMERIC_PREREQUISITE_AFTER_FAA04_V2_CHECK.json',
        'FEAT335_FAA04_IMMUTABLE_EVIDENCE_CHECK.json',
        'FEAT335_FAA01_FAA02_PROVIDER_CHECK.json',
        'FEAT335_FAA03_UNARMED_PROFILE_CHECK.json']
    expected_checks = [897, 11851, 593, 278, 324]
    reports = []
    for name, total in zip(report_names, expected_checks):
        report = read(A/name); reports.append(report)
        check(name+'/check-count', report['checks'] == total)
        check(name+'/no-failures', not report.get('failures') and not report.get('failed') and not report.get('failureCount'))
        for i, binding in enumerate(report['sourceBindings']):
            bound(binding, name+'/input/'+str(i))
    check('all559-immutable-comparisons-retained', reports[2]['historicalMismatchRowsPreserved'] == 559)
    check('provider27-histories', reports[3]['counts']['recordedHistories'] == 27)
    check('profile12-histories-and40-prior-profiles', reports[4]['historyCount'] == 12 and reports[4]['inventoryRegressionCount'] == 40)

    public_path = R/'data/public/feat_candidates/exact_01/candidate.json'
    internal_path = R/'data/director/feat_candidates/exact_01/candidate.json'
    contract_path = A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    public = read(public_path); internal = read(internal_path); contract = read(contract_path)
    current = {x['id']: (i, x) for i, x in enumerate(public['feats'])}
    original_public_binding = next(x['before'] for x in receipts[0]['changes'] if x['before']['path'] == public_path.relative_to(G).as_posix())
    original_public = {x['id']: x for x in read(G/original_public_binding['preservedCopy'])['feats']}
    authored = {x['id']: (i, x) for i, x in enumerate(internal['records'])}
    obligations = read(V/'ACQUISITION_ROWS.json')['rows']
    groups = read(V/'FINITE_REMAINING_WORK.json')['groups']
    acceptance = read(V/'ACCEPTANCE_EXPECTATIONS.json')['groups']
    rows = []
    check('335-public-contract-audit-join', len(current) == len(contract['records']) == len(obligations) == 335 and
          set(current) == {x['id'] for x in contract['records']} == {x['id'] for x in obligations})
    check('327-authored-records-retained', len(authored) == 327)
    for i, c in enumerate(contract['records']):
        sid = c['id']; pi, p = current[sid]
        ai, audited = next((j, x) for j, x in enumerate(obligations) if x['id'] == sid)
        check(sid+'/printed-source-preserved', p['sourceObject'] == c['originalObject'] == audited['a_acquisition']['completeOriginalObject'])
        operative = p.get('unchangedReviewedRecord', p)
        check(sid+'/complete-operative-parity', c['completeOperativeProcedure'] == operative['operationalRules'])
        check(sid+'/selection-approval-fields-preserved', public['selectionEnabled'] is False and all(
            (k in p, p.get(k)) == (k in original_public[sid], original_public[sid].get(k))
            for k in ['selectionEnabled', 'exactApproved', 'runtimeApproved', 'reviewStatus']))
        if 'unchangedReviewedRecord' in p:
            check(sid+'/entire-reviewed-record-preserved', p == original_public[sid])
        if sid in authored:
            _, ip = authored[sid]
            check(sid+'/internal-parity', ip['sourceObject'] == p['sourceObject'] and ip['operationalRules'] == p['operationalRules'] and ip['payloadOperational'] == p['payloadOperational'])
        assigned = [g['id'] for g in groups if sid in g['exactMembers']]
        aa = [g['id'] for g in acceptance if sid in g['affectedIds']]
        rows.append({'id': sid, 'name': p['name'],
            'currentPublicPointer': '/feats/'+str(pi), 'currentContractPointer': '/records/'+str(i),
            'retainedAuditPointer': '/rows/'+str(ai),
            'currentPublicRecordSha256': sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
            'exactMandatorySelectionAndSnapshotDescriptor': deepcopy(audited['b_mandatorySelectionsAndSnapshots']),
            'exactInitialStateDescriptor': deepcopy(audited['c_initialState']),
            'exactConditionalOrDeferredDescriptor': deepcopy(audited['d_externalOrDeferred']),
            'finiteWorkGroups': assigned, 'acceptanceGroups': aa,
            'fulfilledTargetedAcceptanceGroups': [g for g in aa if int(g.split('-')[1]) <= 11],
            'remainingAssemblyGroups': [g for g in assigned if int(g.split('-')[1]) >= 5],
            'fullAcquisitionApproved': False, 'completeUseRuntimeApproved': False,
            'descriptorBindingScope': 'Current procedure/original-object parity and retained GPT descriptors only; remaining assembly groups still need their bounded paid-state/common-contract joins.'})
    for sid in ['astral_projection', 'planar_binding']:
        check(sid+'/null-remains-unavailable', current[sid][1]['payloadOperational'] is None and
              current[sid][1]['selectionEnabled'] is False and current[sid][1] == original_public[sid])

    fulfillment = {'recordedAtUtc': now, 'auditId': 'FEAT335-ACQUISITION-AUDIT-01',
        'status': 'All four findings corrected with bounded evidence. AA01-11 fulfilled in stated scopes; AA12-18 and full assembled feat review remain pending.',
        'sourceBindings': [info(p) for p in [public_path, internal_path, contract_path,
            R/'data/public/feat_candidates/exact_01/shared_rules.json',
            V/'ACQUISITION_ROWS.json', V/'FINITE_REMAINING_WORK.json', V/'ACCEPTANCE_EXPECTATIONS.json']],
        'guardedOperations': 14, 'derivedOperationReceipts': [info(A/n) for n in receipt_names],
        'findingEvidence': {'FAA-01': info(A/report_names[3]), 'FAA-02': info(A/report_names[3]),
                            'FAA-03': info(A/report_names[4]), 'FAA-04': info(A/report_names[2])},
        'fulfilledAcceptanceGroups': ['AA-'+str(i).zfill(2) for i in range(1, 12)],
        'remainingAcceptanceGroups': ['AA-'+str(i).zfill(2) for i in range(12, 19)],
        'fulfilledFiniteGroups': ['FW-01', 'FW-02', 'FW-03', 'FW-04'],
        'remainingFiniteGroups': [deepcopy(x) for x in groups if int(x['id'].split('-')[1]) >= 5],
        'rows': rows, 'sourceInformationDeleted': 0, 'fullFeatCandidateApproved': False,
        'wholeGameFlowConfirmed': False, 'pushed': False, 'cosmologyReviewed': False}

    ledger_path = R/'data/playtest/game_development_coverage.json'
    nav = R/'tools/build_review_map.py'
    old_ledger = read(ledger_path); ledger = deepcopy(old_ledger)
    check('previous-ledger-current', info(ledger_path) == state['coverageLedger'])
    scope = ('The four FEAT335 acquisition-audit findings now have fourteen applied guarded edits and bounded current-source verification. '
        'FAA01/02 pass278 checks across27 paid-provider histories, including actual STR/DEX routes and separately paid Trapcasting parents. '
        'FAA03 passes324 checks across12 unarmed/Claws histories plus all40 prior inventory-profile selections. '
        'FAA04 fresh descendant reports pass897 history and11851 numeric checks;593 integrity checks rejoin all559 historical snapshot discrepancies without overwriting them. '
        'All335 current source/contract/original-object rows are joined in a new follow-through register. '
        'AA01–11 and FW01–04 are fulfilled only within these finite scopes; shared pools, delayed/empty states, fixed snapshots and177 common finite descriptors remain assembly work. '
        'The full assembled feat exact review, final whole-game flow agreement and human balance gates remain open. '
        'Higher spells remain187 unadopted procedures/374 examples,201 pre-push questions and47 post-push receipts; ordinary reviewed/pending totals remain412/436.')
    stale_issue = 'Fulfill FAA-01–04 and the finite remaining-work groups from the completed335-row audit. Recent Flora override overlaps FAA-01 but must be reconciled with STR/DEX routes and parent Trapcasting histories. Preserve historical559 snapshot discrepancies; rerun corrected capture checkpoints into new descendant evidence.'
    for row in ledger['aspects']:
        if row['id'] in {'DD-14', 'DD-69'}:
            check(row['id']+'/specific-old-open-item', row['openIssues'].count(stale_issue) == 1)
            row['openIssues'][row['openIssues'].index(stale_issue)] = ('FAA01–04 targeted corrections are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH.json. '
                'Complete FW05–09/AA12–18 bounded assembly joins, including reverse shared-pool/cantrip ownership, delayed or empty state, fixed snapshots,177 ordinary finite descriptors and conditional/null preservation; then submit the full assembled feat candidate for actual GPT exact review.')
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [register, verification, *[A/n for n in report_names]])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'FEAT335-FAA01-04-corrections', 'recordedAtUtc': now,
                'findingsCorrected': ['FAA-01', 'FAA-02', 'FAA-03', 'FAA-04'], 'guardedOperationsApplied': 14,
                'fulfilledAcceptanceGroups': fulfillment['fulfilledAcceptanceGroups'], 'remainingAcceptanceGroups': fulfillment['remainingAcceptanceGroups'],
                'targetedCorrectionsFulfilled': True, 'fullAcquisitionAssemblyComplete': False, 'fullFeatCandidateApproved': False})
    for before, after in zip(old_ledger['aspects'], ledger['aspects']):
        check(before['id']+'/closure-human-owner-unchanged', all(before.get(k) == after.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence']))
        if before['id'] not in {'DD-14', 'DD-69'}: check(before['id']+'/unrelated-unchanged', before == after)
    check('ledger-metadata-unchanged', {k:v for k,v in old_ledger.items() if k != 'aspects'} == {k:v for k,v in ledger.items() if k != 'aspects'})
    nav_text = nav.read_text(encoding='utf-8')
    old_chain = ' + read(A / "DI7_AND_FEAT335_AUDIT_PROGRESS_DELTA.json")["changes"]\n'
    assert nav_text.count(old_chain) == 1
    nav_text = nav_text.replace(old_chain, old_chain.rstrip('\n') + ''.join(' + read(A / '+json.dumps(n)+')["changes"]' for n in receipt_names+[delta.name])+'\n')
    assert nav_text.count(state['status']) == 1
    nav_text = nav_text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'
    assert nav_text.count(marker) == 1
    links = [('Current335-row acquisition follow-through and remaining scopes', register.name),
             ('Current correction bindings and preservation checks', verification.name),
             ('Corrected actual casting-provider histories', report_names[3]),
             ('Actual unarmed and Troll Claws profile histories', report_names[4]),
             ('Immutable historical snapshot comparison verification', report_names[2]),
             ('Fresh897-check acquisition history report', report_names[0]),
             ('Fresh11851-check numeric prerequisite report', report_names[1])]
    nav_text = nav_text.replace(marker, marker+''.join('        ('+json.dumps(label)+', '+json.dumps(name)+'),\n' for label, name in links))
    compile(nav_text, str(nav), 'exec')

    # All preflight checks precede current-file mutation. Original reports remain untouched.
    save(register, fulfillment)
    save(verification, {'recordedAtUtc': now, 'status': 'pass', 'checks': len(checks), 'failures': 0,
        'results': checks, 'scope': 'Exact current/preserved descendant bindings, all335 source-object and complete-procedure joins, and unchanged owner/human/closure gates. Not all335 complete acquisitions or runtime.',
        'checkedReports': [info(A/n) for n in report_names], 'register': info(register),
        'operationReceipts': [info(A/n) for n in receipt_names], 'sourceInformationDeleted': 0})
    preserved = []
    for path in [ledger_path, nav, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        copy = preservation/path.relative_to(G)
        copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, copy)
        assert path.read_bytes() == copy.read_bytes()
        preserved.append({**info(path), 'preservedCopy': copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json', preserved)
    save(ledger_path, ledger)
    nav.write_text(nav_text, encoding='utf-8', newline='\n')
    save(delta, {'recordedAtUtc': now, 'changes': [
        {'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [ledger_path, nav]],
        'aspectsChanged': ['DD-14', 'DD-69'], 'allOtherAspectsUnchanged': True,
        'allClosuresAndHumanEvidenceUnchanged': True, 'ownerDirectionUnchanged': True,
        'sourceInformationDeleted': 0, 'fullFeatCandidateApproved': False})
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    map_report = read(A/'REVIEW_MAP_BUILD.json')
    assert not map_report['missingLinks']
    assert info(G/'REVIEW_MAP.html')['sha256'] == map_report['sha256']
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress', 'previousCheckpoint': info(old_checkpoint),
        'status': scope, 'coverageLedger': info(ledger_path), 'coverageDelta': info(delta),
        'feat335CorrectionFulfillment': {'currentRegister': info(register), 'bindingCheck': info(verification),
            'appliedGuardedOperations': 14, 'targetedFindingsCorrected': ['FAA-01', 'FAA-02', 'FAA-03', 'FAA-04'],
            'fulfilledAcceptanceGroups': fulfillment['fulfilledAcceptanceGroups'], 'remainingAcceptanceGroups': fulfillment['remainingAcceptanceGroups'],
            'sourceOperationReceipts': [info(A/n) for n in receipt_names], 'targetedEvidence': [info(A/n) for n in report_names],
            'providerHistories': 27, 'unarmedHistories': 12, 'priorInventoryProfiles': 40,
            'historicalSnapshotDiscrepanciesPreserved': 559, 'fullAcquisitionAssemblyComplete': False, 'fullFeatCandidateApproved': False},
        'navigation': {'map': info(G/'REVIEW_MAP.html'), 'receipt': info(A/'REVIEW_MAP_BUILD.json'), 'links': map_report['existingDistinctLinks'], 'missingLinks': []},
        'newRuleAdoptions': 1, 'newRuleAdoptionCountScope': 'One explicit new FAA03/FS02 narrow unarmed-profile source-composition bridge; other findings retain existing source mechanics. No final exact/runtime approval.',
        'sourceInformationDeleted': 0, 'pushed': False, 'cosmologyReviewed': False})
    state['featAcquisitionAudit'].update({'correctionsFulfilled': True, 'correctionScope': 'Four named findings and AA01-11 only; FW05-09/AA12-18 remain open',
        'currentFollowthrough': info(register), 'fullFeatCandidateApproved': False})
    state['activeGptReview'].update({'finalVerdictScope': '335-row source/acquisition audit completed. Four named findings now corrected with targeted local evidence; bounded assembly and full feat exact review remain.',
        'pendingResponse': False, 'awaitingGptResponse': False, 'replyReceived': True})
    state['safeNextActions'] = [
        state['safeNextActions'][0],
        'Current authoritative checkpoint is AFTER_FEAT335_FAA_CORRECTIONS. All14 guarded edits are applied. AA01-11/FW01-04 pass scoped fresh evidence: provider278, unarmed324, history897, numeric11851, immutable593. Do not rerun one-use appliers or replace preserved historical reports.',
        'Actual GPT audit is terminal, no pending reply. Follow FW05-09 and AA12-18 from current follow-through register. No generic resubmission is needed for the already scoped finite correction work; eventual full assembled feat exact review remains required.',
        'FW05: reuse Hemo-empty/Life-Drinker-full and old-spent-plus-new-die cases. Add the missing Lifeleech-after-Soul-Cage history preserving pool/body/death records, and paid Forbidden Pact/Eldritch Echo in both orders preserving one exact cantrip without reset.',
        'FW06/07: bind delayed/empty/capacity states and fixed-versus-live vision/HP/variant/training descriptors to their actual named paid grants. Reuse existing bound evidence. Conditional probes are not campaign events.',
        'FW08:177 ordinary finite descriptors need exact count/owner/recipient/shared-pool/rest/round-epoch joins to the common initial-use mechanism.111 no-new-state rows need no invented bespoke scenarios. All335 current source parity exists but is not the completed descriptor/mechanism join.',
        'FW09: keep two null payloads unavailable and ACQ04 external-source branches conditional. No pre-push cosmology proof or newly invented positive grant is required.',
        'FAA03 new SourceUnarmedChoices models authentic source lineage/training/payments only. Actual unarmed/Claws qualifies with actual covering training. Weapon Master four-inventory-profile menu unchanged; no combined Monk/Claws damage formula or world event created.',
        'Higher spells remain187 complete unadopted procedures/374 examples,201 pre-push mechanical questions,47 deferred receipts.116 drafts unsent;71 comparison-only. Ordinary authored totals412/436. DI7 and other unadopted draft issues require actual dedicated GPT review.',
        'Continue bestiary, Director and cross-system/packaging work. Final actual joint whole-game flow agreement precedes authorized GitHub push; verify remote commit before careful cosmology review. No deletion or full approval occurred.']
    save(checkpoint, state)
    print(json.dumps({'checkpoint': info(checkpoint), 'bindingChecks': len(checks),
                      'navigationLinks': map_report['existingDistinctLinks'], 'missingLinks': map_report['missingLinks']}))


if __name__ == '__main__':
    main()
