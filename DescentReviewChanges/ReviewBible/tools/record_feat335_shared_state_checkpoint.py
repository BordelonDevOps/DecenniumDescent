"""Reuse exact AA13 evidence and register FW05 completion without rerunning history."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

G = Path('C:/Github/DecenniumDescent'); R = G/'DescentReviewChanges/ReviewBible'
A = G/'docs/audit/2026-10-08/full-game'


def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))


def info(p):
    b = p.read_bytes()
    return {'path':p.relative_to(G).as_posix(), 'bytes':len(b), 'sha256':sha256(b).hexdigest()}


def save(p, data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FAA_CORRECTIONS.json'
    target = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_SHARED_STATES.json'
    register = A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_SHARED_STATES.json'
    aa13 = A/'FEAT335_AA13_EXISTING_EVIDENCE_BINDING_CHECK.json'
    delta = A/'FEAT335_SHARED_STATES_PROGRESS_DELTA.json'
    preservation = A/'navigation-before-feat335-shared-states'
    assert all(not p.exists() for p in [target,register,aa13,delta,preservation])
    state = read(previous)
    shared_path = A/'FEAT335_SHARED_ACQUISITION_STATE_CHECK.json'
    shared = read(shared_path)
    assert shared['checks'] == 203 and not shared['failures'] and shared['historyCount'] == 17
    for binding in shared['sourceBindings']: assert info(G/binding['path']) == binding
    checks = []

    def check(label, truth):
        checks.append({'id':label,'passed':bool(truth)})
        assert truth,label

    evidence_index = read(A/'feat335-acquisition-audit-01-verdict/EVIDENCE_REPORT_INDEX.json')
    reports = {x['reportId']:x for x in evidence_index['reports']}
    reused = {}
    for er in ['ER-07','ER-12']:
        b = reports[er]['binding']; p = G/b['path']
        check(er+'/exact-GPT-audited-report',info(p)['sha256'] == b['sha256'])
        reused[er] = read(p)
        check(er+'/original-report-no-failures',not reused[er]['failures'])
    owned,fixed = reused['ER-12'],reused['ER-07']
    contracts = {x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
    for sid in ['hemocraft','life_drinker']:
        check(sid+'/current-complete-procedure-unchanged',owned['completeSourceContracts'][sid]['completeOperativeProcedure'] == contracts[sid]['completeOperativeProcedure'])
        check(sid+'/printed-original-unchanged',owned['completeSourceContracts'][sid]['originalObject'] == contracts[sid]['originalObject'])
    for sid in ['martialAdept','martial_adept_advanced']:
        check(sid+'/current-complete-procedure-unchanged',fixed['completeProcedures'][sid] == contracts[sid]['completeOperativeProcedure'])
    required_helpers = {'feat_exact_01_owned_feat_model.py','feat_exact_01_fixed_menus.py',
                        'feat_exact_01_acquisition_models.py','feat_exact_01_training_prerequisite_model.py'}
    retained_bindings = []
    for er,report in reused.items():
        for b in report['sourceBindings']:
            if Path(b['path']).name in required_helpers:
                check(er+'/unchanged-relevant-helper/'+b['path'],info(G/b['path']) == b)
                retained_bindings.append(b)
    evidence = []
    for i,trace in enumerate(owned['historyTraces']):
        if trace['case']['id'] not in {'life-hemocraft','hemocraft-other-qualifying-ability'}: continue
        name = trace['case']['id']; final = trace['final']; init = final['initializations']
        check(name+'/separate-empty-and-full-reserves', init['hemocraft']['recoveryReserve'] == {'maximum':16,'current':0}
              and init['life_drinker']['recoveryReserve'] == {'maximum':16,'current':16})
        grants = final['payment']['grants']
        check(name+'/real-parent-and-child-payments',[(x['identity'],x['opportunity']) for x in grants] == [('hemocraft','Warrior:4'),('life_drinker','Warrior:8')])
        first = trace['history'][0]['after']['initializations']['hemocraft']['recoveryReserve']
        check(name+'/parent-start-zero-capacity-growth-only', first == {'maximum':8,'current':0})
        evidence.append({'report':info(G/reports['ER-12']['binding']['path']), 'pointer':'/historyTraces/'+str(i),
                         'case':deepcopy(trace['case']), 'parentReserveAfterPurchase':first,
                         'finalInitializations':deepcopy(init), 'paidGrants':deepcopy(grants)})
    check('two-existing-Hemocraft-source-choice-histories',len(evidence) == 2)
    maneuver_rows = []
    for i,trace in enumerate(fixed['traces']):
        if not trace['id'].startswith('martial/'):continue
        spent = bool(trace['conditionalPremises'])
        pool = trace['state']['initializations']['feat_superiority']
        check(trace['id']+'/only-new-die-not-old-refill',pool['maximum'] == 2 and pool['current'] == (1 if spent else 2) and pool['dieSides'] == 6)
        grants = trace['state']['payment']['grants']
        check(trace['id']+'/two-actual-paid-source-grants',[(x['identity'],x['opportunity']) for x in grants] == [('martialAdept','Warrior:4'),('martial_adept_advanced','Warrior:8')])
        maneuver_rows.append({'pointer':'/traces/'+str(i), 'id':trace['id'], 'pool':deepcopy(pool),
                             'conditionalPremises':deepcopy(trace['conditionalPremises']), 'paidGrants':deepcopy(grants)})
    check('all90-spent-and90-unspent-source-menu-compositions',len(maneuver_rows) == 180 and sum(bool(x['conditionalPremises']) for x in maneuver_rows) == 90)
    for er, labels in [('ER-12',['hemocraft-zero-and-capacity-only','life-drinker-separate-initial-full'])]:
        for label in labels:
            found = [(i,x) for i,x in enumerate(reused[er]['results']) if x['id'] == label]
            check(er+'/'+label+'/existing-test-result',len(found) == 1 and found[0][1]['passed'])
    aa13_result = {'recordedAtUtc':now,'status':'pass','acceptanceGroup':'AA-13', 'checks':len(checks),'failures':[],
        'scope':'Current complete named procedures and relevant unchanged helper bindings joined to exact GPT-audited paid histories. Old suites are reused, not asserted rerun against newer candidate files.',
        'sourceBindings':[info(Path(__file__)),info(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'),
                          info(A/'feat335-acquisition-audit-01-verdict/EVIDENCE_REPORT_INDEX.json'),
                          *[info(G/reports[x]['binding']['path']) for x in ['ER-07','ER-12']]],
        'retainedRelevantHelperBindings':retained_bindings,'results':checks,
        'HemocraftLifeDrinkerEvidence':evidence,'superiorityEvidence':maneuver_rows,
        'oldReportTotalsNotNewExecutions':True,'newGameRules':0,'sourceInformationDeleted':0,'fullFeatCandidateApproved':False}

    previous_register = G/state['feat335CorrectionFulfillment']['currentRegister']['path']
    assert info(previous_register) == state['feat335CorrectionFulfillment']['currentRegister']
    current = read(previous_register)
    current.update(recordedAtUtc=now, previousRegister=info(previous_register),
        status='Four findings and FW05 shared-owner/resource assembly complete in finite scopes. AA01-14 fulfilled; AA15-18/FW06-09 and full feat exact review pending.')
    current['fulfilledAcceptanceGroups'] = ['AA-'+str(i).zfill(2) for i in range(1,15)]
    current['remainingAcceptanceGroups'] = ['AA-'+str(i).zfill(2) for i in range(15,19)]
    current['fulfilledFiniteGroups'] = ['FW-'+str(i).zfill(2) for i in range(1,6)]
    current['remainingFiniteGroups'] = [x for x in current['remainingFiniteGroups'] if x['id'] != 'FW-05']
    for row in current['rows']:
        row['fulfilledTargetedAcceptanceGroups'] = [g for g in row['acceptanceGroups'] if int(g.split('-')[1]) <= 14]
        row['remainingAssemblyGroups'] = [g for g in row['remainingAssemblyGroups'] if g != 'FW-05']
    scope = ('FW05 shared-owner acquisition assembly is fulfilled in finite scopes. Fresh203 checks across17 source-qualified paid histories cover both Lifeleech/Soul Cage orders, '
        'all0–3 retained Soul Charge counts, and both Forbidden Pact/Eldritch Echo orders with all three actual sigils. '
        'The second source preserves charge/death/body journals and one exact CHA Eldritch Blast route/identity without replaying RP, casting history or first-source state. '
        'Prior journals are conditional fixtures, not actual campaign events. AA13 reuses two exact Hemo-empty/Life-Drinker-full histories and180 existing superiority compositions '
        'with unchanged relevant procedures/helpers; old suites were not rerun. AA01–14 are fulfilled within stated scopes; AA15–18/FW06–09 and full assembled feat exact review remain pending.')
    ledger_path = R/'data/playtest/game_development_coverage.json'; nav = R/'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    old_ledger = read(ledger_path); ledger = deepcopy(old_ledger)
    old_issue = ('FAA01–04 targeted corrections are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH.json. '
        'Complete FW05–09/AA12–18 bounded assembly joins, including reverse shared-pool/cantrip ownership, delayed or empty state, fixed snapshots,177 ordinary finite descriptors and conditional/null preservation; then submit the full assembled feat candidate for actual GPT exact review.')
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            assert row['openIssues'].count(old_issue) == 1
            row['openIssues'][row['openIssues'].index(old_issue)] = ('AA01–14/FW01–05 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_SHARED_STATES.json. '
                'Complete FW06–09/AA15–18: delayed/empty/capacity state, fixed snapshots and recipients,177 ordinary finite descriptors, conditional/null preservation and final335 descriptor/mechanism parity. Then submit the full assembled feat candidate for actual GPT exact review.')
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [shared_path,aa13,register])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-FW05-shared-state-assembly','recordedAtUtc':now,
                'fulfilledAcceptanceGroups':['AA-12','AA-13','AA-14'],'freshChecks':203,'freshHistories':17,
                'AA13HistoricalEvidenceReused':True,'fullFeatCandidateApproved':False})
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k) == after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before == after
    assert {k:v for k,v in ledger.items() if k!='aspects'} == {k:v for k,v in old_ledger.items() if k!='aspects'}
    nav_text = nav.read_text(encoding='utf-8')
    old_chain = ' + read(A / "FEAT335_FAA_CORRECTIONS_PROGRESS_DELTA.json")["changes"]\n'
    assert nav_text.count(old_chain) == 1
    nav_text = nav_text.replace(old_chain,old_chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert nav_text.count(state['status']) == 1
    nav_text = nav_text.replace(state['status'],state['status']+' Later assembly checkpoint: '+scope,1)
    marker = '    pending = [\n'; assert nav_text.count(marker) == 1
    nav_text = nav_text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Current335-row follow-through after shared-state assembly',register),('Both shared acquisition orders —203 checks',shared_path),('AA13 exact retained paid resource-state evidence',aa13)]))
    compile(nav_text,str(nav),'exec')
    save(aa13,aa13_result)
    current['sharedStateEvidence'] = {'AA12AndAA14':info(shared_path),'AA13ExistingEvidenceBinding':info(aa13)}
    save(register,current)
    preserved = []
    for path in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy = preservation/path.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,copy)
        assert path.read_bytes() == copy.read_bytes()
        preserved.append({**info(path),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved)
    save(ledger_path,ledger);nav.write_text(nav_text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    map_report = read(A/'REVIEW_MAP_BUILD.json');assert not map_report['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',
        status=state['status']+' Later assembly checkpoint: '+scope,coverageLedger=info(ledger_path),coverageDelta=info(delta),
        featSharedStateAssembly={'fulfilledFiniteGroup':'FW-05','fulfilledAcceptanceGroups':['AA-12','AA-13','AA-14'],
            'freshEvidence':info(shared_path),'reusedAA13Evidence':info(aa13),'fullFeatCandidateApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':map_report['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint: existing source shared-state initialization only. Prior FAA03 integration retained unchanged.')
    state['feat335CorrectionFulfillment'].update(currentRegister=info(register),fulfilledAcceptanceGroups=current['fulfilledAcceptanceGroups'],remainingAcceptanceGroups=current['remainingAcceptanceGroups'])
    state['featAcquisitionAudit']['currentFollowthrough'] = info(register)
    state['featAcquisitionAudit']['correctionScope'] = 'Four findings plus FW05 assembly fulfilled; AA15-18/FW06-09 remain'
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Previous turn made verified progress. Current checkpoint is AFTER_FEAT335_SHARED_STATES. AA01-14/FW01-05 are fulfilled within their named scopes. Do not rerun immutable one-use report/record builders.',
        'Next FW06/AA15: bind later-event-only, empty-container and capacity-only descriptors to actual paid grants. Use the20 exact IDs from GPT finite remaining work. Reuse existing source-bound cases; test missing state shapes only.',
        'Then FW07/AA16: bind fixed versus live vision/HP/variant snapshots and exact training recipients/duplicate branches; preserve HP and no free reselection.',
        'FW08/AA18: bind177 exact ordinary finite count/owner/recipient/shared-vs-separate/rest/round descriptors to the common initial-use mechanism.111 no-new-state entries require no invented state. Current335 parity alone is not the full descriptor/mechanism join.',
        'FW09/AA17: preserve two null unavailable payloads and ACQ04 conditional branches with exact absent/null distinctions; no positive pre-push cosmology proof.',
        'SharedAcquisitionStates supplies finite retained-source acquisition witnesses.17 histories/203 checks cover Soul pool both orders at0–3 and both blast orders/all3sigils. Conditional journal imports are not campaign events; individual blast-source removal/reacquisition and actual cast/death/rest use are outside this evidence.',
        'AA13 explicitly reused historical source-bound evidence: two Hemo-empty/Life-Drinker-full histories and180 paid superiority compositions, including90 with old die spent. No old suite rerun or changed-source execution claim.',
        'Actual GPT335 audit remains terminal; no pending response or generic resubmission. Finish bounded acquisition assembly then submit the full assembled feat candidate for actual GPT exact review.',
        *state['safeNextActions'][-2:]]
    save(target,state)
    print(json.dumps({'checkpoint':info(target),'AA13BindingChecks':len(checks),'navigationLinks':map_report['existingDistinctLinks'],'missingLinks':map_report['missingLinks']}))


if __name__ == '__main__':main()
