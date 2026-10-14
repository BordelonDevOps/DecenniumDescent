"""FW09/AA17 exact current null/conditional preservation, no cosmology review."""
from datetime import datetime,timezone
from copy import deepcopy
import json
from pathlib import Path
from validate_feat_exact_01_composite_casting import read,info

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game';V=A/'feat335-acquisition-audit-01-verdict'


def main():
    out=A/'FEAT335_CONDITIONAL_PRESERVATION_CHECK.json'
    assert not out.exists()
    paths=[R/'data/public/feat_candidates/exact_01/candidate.json',
        R/'data/director/feat_candidates/exact_01/candidate.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A/'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_CHECK.json',
        V/'ACQUISITION_ROWS.json',V/'FINITE_REMAINING_WORK.json',V/'EVIDENCE_REPORT_INDEX.json',
        R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',
        A/'FEAT335_ACQUISITION_AUDIT_01_DERIVED_OPERATIONS.json',Path(__file__)]
    bindings=[info(p) for p in paths];checks=[];entries=[]

    def check(label,truth,details=None):
        checks.append({'id':label,'passed':bool(truth),'details':deepcopy(details)})
        assert truth,label

    pub=read(paths[0]);internal=read(paths[1]);contracts=read(paths[2]);external=read(paths[3])
    p={x['id']:x for x in pub['feats']};i={x['id']:x for x in internal['records']};c={x['id']:x for x in contracts['records']}
    rows={x['id']:x for x in read(paths[4])['rows']};fw=next(x for x in read(paths[5])['groups'] if x['id']=='FW-09')
    er=next(x for x in read(paths[6])['reports'] if x['reportId']=='ER-01')
    check('original-ACQ04-report-byte-identical-to-GPT-audit',info(paths[3])['sha256']==er['binding']['sha256'])
    check('original524-check-scope-remains-historical',external['checks']==524 and not external['failures'] and
          external['campaignRecordsAuthenticated']==0 and external['cosmologyReviewed'] is False and external['all335CompleteAcquisitionsValidated'] is False)
    old_public=next(x['before'] for x in read(paths[10])['changes'] if x['before']['path']==paths[0].relative_to(G).as_posix())
    raw=info(G/old_public['preservedCopy'])
    check('preserved-before-public-exact',all(raw[k]==old_public[k] for k in ['bytes','sha256']))
    before={x['id']:x for x in read(G/old_public['preservedCopy'])['feats']}
    check('exact-six-preservation-identities',set(fw['exactMembers'])=={'astral_projection','planar_binding','divine_favor','elemental_body','dragon_blood','frenzied_rage'})
    for sid in fw['exactMembers']:
        check(sid+'/entire-current-wrapper-unchanged',p[sid]==before[sid])
        check(sid+'/all-current-envelopes-complete-procedure-parity',p[sid]['operationalRules']==i[sid]['operationalRules']==c[sid]['completeOperativeProcedure']==rows[sid]['a_acquisition']['completeControllingOperativeProcedure'])
        check(sid+'/original-source-preserved',p[sid]['sourceObject']==i[sid]['sourceObject']==c[sid]['originalObject']==rows[sid]['a_acquisition']['completeOriginalObject'])
        check(sid+'/selection-and-approval-disabled',all(p[sid][k] is False and i[sid][k] is False for k in ['selectionEnabled','exactApproved','runtimeApproved']))
        if sid in {'astral_projection','planar_binding'}:
            check(sid+'/present-explicit-null-retained',all('payloadOperational' in x and x['payloadOperational'] is None for x in [p[sid],i[sid]]))
            check(sid+'/source-wrapper-does-not-unlock-payload',rows[sid]['d_externalOrDeferred']['disposition']=='KEEP_NULL_UNAVAILABLE')
        else:
            check(sid+'/conditional-branch-preserved',rows[sid]['d_externalOrDeferred']['disposition']=='KEEP_ACQ04_SOURCE_QUALIFIED_CONDITIONAL_BRANCHES')
            check(sid+'/real-printed-alternatives-unchanged',c[sid]['requirements']==rows[sid]['a_acquisition']['normalizedPredicateNavigationOnly'])
        entries.append({'id':sid,'currentCompleteContract':deepcopy(c[sid]),
            'preservedDisposition':deepcopy(rows[sid]['d_externalOrDeferred']),
            'payloadFieldPresence':True,'payloadOperational':p[sid]['payloadOperational'],
            'campaignAcquisitionEstablished':False,'fullUsePayloadPromoted':False})
    check('all263-immutable-fixture-files-retained',len(external['fixtureBindings'])==263)
    for b in external['fixtureBindings']:check('fixture/'+Path(b['path']).name,info(G/b['path'])==b)
    outcomes={};case_refs=[]
    for n,case in enumerate(external['cases']):
        if 'result' not in case:
            # These are bound complete paid-history references, not external world approvals.
            ref=case['completeHistoryRef'];check('paid-history-ref/'+str(n),info(G/ref['path'])['sha256']==ref['sha256'])
            continue
        outcome=case['result']['outcome'];outcomes[outcome]=outcomes.get(outcome,0)+1
        check('case/'+str(n)+'/no-campaign-positive',outcome in {'CONDITIONAL_ONLY','UNESTABLISHED','CONTRADICTED'} and
              case['result']['campaignAcquisitionEstablished'] is False and case['acquisitionGate']['campaignAcquisitionEstablished'] is False)
        if outcome=='CONDITIONAL_ONLY':
            check('case/'+str(n)+'/conditional-root-labelled',case['evidence']['evidenceMode']=='conditional_fixture' and
                  all(w['evidenceMode']=='conditional_fixture' for w in case['admittedWorlds']))
        else:check('case/'+str(n)+'/missing-or-contradicted-branch-does-not-pass',case['acquisitionGate']['decision']=='DENIED' and case['acquisitionGate']['paymentCommitted'] is False)
        case_refs.append({'pointer':'/cases/'+str(n),'id':case['id'],'outcome':outcome,'campaignAcquisitionEstablished':False})
    check('finite-outcome-counts-preserved',outcomes=={'CONTRADICTED':13,'UNESTABLISHED':104,'CONDITIONAL_ONLY':21},outcomes)
    check('no-test-Sorcerer-class-added','Sorcerer' not in {x['class'] for x in read(paths[7])['classes']})
    check('no-test-Dragonborn-ancestry-added','Dragonborn' not in {x['name'] for x in read(paths[8])['ancestries']})
    check('candidate-global-selection-still-disabled',pub['selectionEnabled'] is False and internal['selectionEnabled'] is False)
    check('all-source-bindings-current-and-stable',[info(p) for p in paths]==bindings)
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'acceptanceGroups':['AA-17'],'finiteWorkGroup':'FW-09','exactDescriptorCount':6,
        'sourceBindings':bindings,'entries':entries,'retainedFixtureBindings':external['fixtureBindings'],
        'retainedCaseReferences':case_refs,'retainedOutcomeCounts':outcomes,'results':checks,
        'scope':'Current six-wrapper/source-field preservation and unchanged historical conditional evidence. No new positive external credential, game option, spell activation, cosmology meaning or whole-game approval.',
        'historicalSuiteRerun':False,'campaignRecordsAuthenticated':0,'cosmologyReviewed':False,
        'sourceInformationDeleted':0,'newGameRules':0,'fullFeatCandidateApproved':False}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'report':info(out)}))


if __name__=='__main__':main()
