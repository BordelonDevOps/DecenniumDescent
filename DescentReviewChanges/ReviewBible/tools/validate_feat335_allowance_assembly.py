"""FW08/AA18 finite descriptor/identity assembly, preserving honest scope."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from build_feat335_allowance_descriptors import assemble, R, G, A, V
from feat335_allowance_bindings import BoundAllowance, EpochClaims
from validate_feat_exact_01_composite_casting import read, info


def main():
    report_path=A/'FEAT335_ALLOWANCE_ASSEMBLY_CHECK.json'
    join_path=A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY.json'
    assert not report_path.exists() and not join_path.exists()
    descriptor_path=A/'FEAT335_ALLOWANCE_DESCRIPTORS.json'
    descriptor=read(descriptor_path); reconstructed=assemble()
    descriptor_compare=deepcopy(descriptor); descriptor_compare.pop('recordedAtUtc')
    reconstructed.pop('recordedAtUtc'); assert descriptor_compare==reconstructed
    register_path=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CONDITIONAL_PRESERVATION.json'
    register=read(register_path); hist_path=A/'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_FAA04_CHECK.json'
    hist=read(hist_path); entries={x['id']:x for x in descriptor['entries']}
    checks=[]; traces=[]
    def check(label, truth, detail=None):
        checks.append({'id':label,'passed':bool(truth),'detail':deepcopy(detail)})
        assert truth,label
    def reject(label, call):
        try:call()
        except ValueError as e:check(label,True,str(e));return
        check(label,False)
    def snapshot(a):
        return {'owner':a.owner,'identity':a.identity,'recovery':a.reset,'maximum':a.use.maximum,
            'current':a.use.current,'completedRests':sorted(a.use.completed_rests),
            'lastSpentSecond':a.last_spent_second,'encounters':sorted(a.seen_encounters)}
    bindings=descriptor['sourceBindings']+[info(descriptor_path),info(register_path),info(hist_path),
        info(R/'tools/feat_exact_01_acquisition_models.py'),info(Path(__file__))]
    for b in bindings:check('current-binding/'+b['path'],info(G/b['path'])==b)
    for b in register['sourceBindings']:check('current-register-source/'+b['path'],info(G/b['path'])==b)
    # Reuse the freshly immutable FS06 algebra exactly; no historical suite rerun.
    check('shared897-result-retained',hist['checks']==897 and not hist['failures'])
    reused=[]
    for n in range(881,890):
        row=hist['results'][n]
        check('existing-shared/'+row['name'],row['pass'] and row['actual']==row['expected'])
        reused.append({'report':info(hist_path),'pointer':'/results/'+str(n),'name':row['name']})
    common_binding=next(b for b in hist['sourceBindings'] if b['path'].endswith('/feat_exact_01_acquisition_models.py'))
    check('shared-mechanism-byte-unchanged',info(G/common_binding['path'])==common_binding)

    fw=next(x for x in read(V/'FINITE_REMAINING_WORK.json')['groups'] if x['id']=='FW-08')
    check('all177-exact-members',list(entries)==fw['exactMembers'] and len(entries)==177)
    check('111-inside177',sum(e['auditedBranch']=='noNewConsumableOrActiveEffect' for e in entries.values())==111)
    finite=[]
    for sid,e in entries.items():
        a=e['finiteAllowances'];initial=e['exactInitialStateDescriptor']['exactObligation']
        check(sid+'/complete-source-retained',bool(e['currentCompleteContract']['completeOperativeProcedure']))
        if e['auditedBranch']=='noNewConsumableOrActiveEffect':
            check(sid+'/no-invented-consumable',not a)
        for d in a:
            finite.append(d)
            if d['maximum']=='currentPB': source_count='PB' in initial
            elif d['maximum']==3: source_count='three' in initial.lower()
            else:source_count=any(s in initial.lower() for s in ['one','three distinct'])
            check(d['identity']+'/audited-exact-count',source_count)
            recovery=d['recovery']
            compact=initial.lower().replace('-','').replace(' ','')
            full=e['currentCompleteContract']['completeOperativeProcedure'].lower().replace('-','').replace(' ','')
            marker={'LR':('lr','longrest'),'SR_OR_LR':('sr','shortrest'),
                'elapsed24h':('24elapsedhours',),'realEncounter':('encounter',)}[recovery]
            check(d['identity']+'/source-recovery-marker',any(m in compact or m in full for m in marker))
            state=BoundAllowance.initial('owner-A',d,3)
            check(d['identity']+'/initial-count-bound',state.use.maximum==state.use.current==(3 if d['maximum']=='currentPB' else d['maximum']))
        for cadence in e['laterEventCadences']:
            check(sid+'/'+cadence['family']+'/explicit-identity',cadence['maximum']==1 and bool(cadence['scope']) and bool(cadence['epoch']))
    check('60-feats62-allowances',sum(bool(e['finiteAllowances']) for e in entries.values())==60 and len(finite)==62)
    check('62-unique-owned-allowances',len({d['identity'] for d in finite})==62)

    # Only exceptions to the reused FS06 mechanism get new boundary traces.
    def make(sid,owner='owner-A',index=0,pb=3):return BoundAllowance.initial(owner,entries[sid]['finiteAllowances'][index],pb)
    for sid,kind in [('lucky','LR'),('slayer_s_resolve','SR')]:
        a=make(sid);a.spend();before=snapshot(a)
        check(sid+'/other-owner-rest-does-not-refill',not a.rest('owner-B','rest-1',kind,True) and snapshot(a)==before)
        check(sid+'/debt-only-does-not-refill',not a.rest('owner-A','rest-debt',kind,False) and snapshot(a)==before)
        if kind=='LR':check(sid+'/SR-not-LR',not a.rest('owner-A','sr-1','SR',True) and snapshot(a)==before)
        check(sid+'/governed-rest-restores',a.rest('owner-A','rest-1',kind,True))
        a.spend();spent=snapshot(a)
        check(sid+'/same-receipt-relabel-not-recovery',not a.rest('owner-A','rest-1','LR',True) and snapshot(a)==spent)
        if kind=='SR':check(sid+'/actual-LR-recovers-SR',a.rest('owner-A','lr-2','LR',True))
        traces.append({'id':sid+'.restOwnerScope','conditionalMechanismTrace':True,'before':before,'after':snapshot(a)})

    a=make('slayer_s_resolve');a.spend()
    reject('slayer/shared-attack-then-save-branch-is-spent',a.spend)
    traces.append({'id':'slayer_s_resolve.sharedModes','conditionalMechanismTrace':True,'state':snapshot(a)})
    traps=[make('trapsetter',index=i) for i in range(3)];traps[0].spend()
    check('trapsetter/types-separate',[x.use.current for x in traps]==[0,1,1])
    other=make('trapsetter','owner-B');check('trapsetter/other-owner-separate',other.use.current==1)
    traces.append({'id':'trapsetter.separateTypeAndOwner','conditionalMechanismTrace':True,'states':[snapshot(x) for x in traps]})

    gadget=make('contraption_crafter');gadget.spend(100);before=snapshot(gadget)
    check('gadget/rest-not-elapsed-time',not gadget.rest('owner-A','lr','LR',True) and snapshot(gadget)==before)
    reject('gadget/one-second-before24h',lambda:gadget.spend(86499))
    check('gadget/rejection-atomic',snapshot(gadget)==before)
    gadget.use.operative=False;reject('gadget/suppressed-cannot-spend-at24h',lambda:gadget.spend(86500))
    check('gadget/suppression-no-refill',snapshot(gadget)==before)
    gadget.use.operative=True;gadget.spend(86500)
    check('gadget/exact24h-one-new-start',gadget.last_spent_second==86500 and gadget.use.current==0)
    reject('gadget/no-second-start-same-instant',lambda:gadget.spend(86500))
    traces.append({'id':'contraption_crafter.elapsedBoundary','conditionalMechanismTrace':True,'before':before,'after':snapshot(gadget)})

    grace=make('elven_grace');check('grace/genuine-first-entry',grace.enter_encounter('owner-A','encounter-1'))
    grace.spend();before=snapshot(grace)
    check('grace/reentry-same-encounter-no-reset',not grace.enter_encounter('owner-A','encounter-1') and snapshot(grace)==before)
    check('grace/rest-not-encounter',not grace.rest('owner-A','lr','LR',True) and snapshot(grace)==before)
    check('grace/other-owner-entry-no-reset',not grace.enter_encounter('owner-B','encounter-2') and snapshot(grace)==before)
    check('grace/genuine-new-encounter',grace.enter_encounter('owner-A','encounter-2') and grace.use.current==1)
    traces.append({'id':'elven_grace.encounterIdentity','conditionalMechanismTrace':True,'before':before,'after':snapshot(grace)})

    claims=EpochClaims()
    check('mana/first-caster-claims-recipient',claims.claim('mana_burn',['target-A'],'round-1'))
    check('mana/second-caster-same-recipient-denied',not claims.claim('mana_burn',['target-A'],'round-1'))
    check('mana/different-recipient-available',claims.claim('mana_burn',['target-B'],'round-1'))
    check('mana/next-round-available',claims.claim('mana_burn',['target-A'],'round-2'))
    check('mana/old-round-replay-denied',not claims.claim('mana_burn',['target-A'],'round-1'))
    check('curse/first-owner-target',claims.claim('curse_weaving',['owner-A','target-A'],'round-1'))
    check('curse/separate-owner-target',claims.claim('curse_weaving',['owner-B','target-A'],'round-1'))
    check('curse/same-owner-target-rejected',not claims.claim('curse_weaving',['owner-A','target-A'],'round-1'))
    check('chef/recipient-first-cook',claims.claim('wilderness_chef.recipient',['eater'],'eater-lr-1'))
    check('chef/second-cook-same-recipient-rest-denied',not claims.claim('wilderness_chef.recipient',['eater'],'eater-lr-1'))
    check('chef/actual-recipient-new-rest',claims.claim('wilderness_chef.recipient',['eater'],'eater-lr-2'))
    for family in ['copyRelease','freeStoredRelease','hardDenial','combat_reflexes.extraReaction']:
        scope=['owner-A','target-A'] if family=='hardDenial' else ['owner-A']
        epoch='actual-encounter-1' if family=='hardDenial' else 'actual-round-1'
        check(family+'/first',claims.claim(family,scope,epoch))
        check(family+'/different-feature-extra-turn-reentry-same-epoch-denied',not claims.claim(family,scope,epoch))
    # Capacity growth and a rest never clear the independent round/cast roots.
    efficient=make('efficient_caster',pb=2);efficient.spend()
    check('efficient/round-claim',claims.claim('efficient_caster',['owner-A'],'round-1'))
    efficient.use.capacity(3)
    check('efficient/growth-keeps-current-and-round',efficient.use.current==1 and not claims.claim('efficient_caster',['owner-A'],'round-1'))
    efficient.rest('owner-A','lr1','LR',True)
    check('efficient/rest-recovers-charge-only',efficient.use.current==3 and not claims.claim('efficient_caster',['owner-A'],'round-1'))
    sink=make('energy_sink');sink.spend();check('sink/first-cast-root',claims.claim('energy_sink.hostileCast',['owner-A','cast-root'],'cast-lifetime'))
    sink.rest('owner-A','lr1','LR',True)
    check('sink/rest-no-repeat-old-cast',not claims.claim('energy_sink.hostileCast',['owner-A','cast-root'],'cast-lifetime'))
    traces.append({'id':'recipient.owner.sharedEpochAlgebra','conditionalMechanismTrace':True,'claims':sorted(claims.claims),'efficient':snapshot(efficient),'sink':snapshot(sink)})

    # Evidence closure joins current source records to the already fulfilled
    # finite groups; it does NOT re-label all335 rows as new played characters.
    evidence={
        'FW-01':[register['findingEvidence']['FAA-01']],
        'FW-02':[register['findingEvidence']['FAA-02']],
        'FW-03':[register['findingEvidence']['FAA-03']],
        'FW-04':[register['findingEvidence']['FAA-04'],info(A/'FEAT_EXACT_01_NUMERIC_PREREQUISITE_AFTER_FAA04_V2_CHECK.json')],
        'FW-05':list(register['sharedStateEvidence'].values()),
        'FW-06':[register['deferredStateEvidence']['descriptorFile'],register['deferredStateEvidence']['paidHistoryReport']],
        'FW-07':list(register['fixedSnapshotEvidence'].values()),
        'FW-08':[info(descriptor_path)],
        'FW-09':[register['conditionalPreservationEvidence']]}
    for group,refs in evidence.items():
        for b in refs:check(group+'/preserved-evidence/'+Path(b['path']).name,info(G/b['path'])==b)
    pub=read(R/'data/public/feat_candidates/exact_01/candidate.json')
    internal=read(R/'data/director/feat_candidates/exact_01/candidate.json')
    public={x['id']:x for x in pub['feats']}; private={x['id']:x for x in internal['records']}
    contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
    audit={x['id']:x for x in read(V/'ACQUISITION_ROWS.json')['rows']}
    check('335-source-identity-parity',set(public)==set(contracts)==set(audit)=={r['id'] for r in register['rows']} and len(public)==335)
    joined=[]
    for n,row in enumerate(register['rows']):
        sid=row['id'];p=public[sid];c=contracts[sid];r=audit[sid];operative=p.get('unchangedReviewedRecord',p)['operationalRules']
        check(sid+'/current-full-procedure-parity',operative==c['completeOperativeProcedure'])
        check(sid+'/original-object-parity',p['sourceObject']==c['originalObject']==r['a_acquisition']['completeOriginalObject'])
        check(sid+'/raw-prerequisite-presence',('prerequisite' in p['sourceObject'])==c['printedPrerequisitePresent'] and p['sourceObject'].get('prerequisite')==c['printedPrerequisite'])
        for source_key,current_key in [('b_mandatorySelectionsAndSnapshots','exactMandatorySelectionAndSnapshotDescriptor'),('c_initialState','exactInitialStateDescriptor'),('d_externalOrDeferred','exactConditionalOrDeferredDescriptor')]:
            check(sid+'/'+current_key,row[current_key]==r[source_key])
        if sid in private:
            check(sid+'/internal-parity',private[sid]['operationalRules']==operative and private[sid]['sourceObject']==p['sourceObject'])
            check(sid+'/unapproved-flags',all(p[k] is False and private[sid][k] is False for k in ['selectionEnabled','exactApproved','runtimeApproved']))
        else:check(sid+'/reviewed-record-whole-retained','unchangedReviewedRecord' in p)
        if sid in {'astral_projection','planar_binding'}:
            check(sid+'/explicit-null-not-absence','payloadOperational'in p and p['payloadOperational'] is None)
        # Current register's byte-level full wrapper digest includes menus,
        # original absence/null and all reviewed-record nesting without adapters.
        digest=sha256(json.dumps(p,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        check(sid+'/whole-wrapper-menu-digest',digest==row['currentPublicRecordSha256'])
        check(sid+'/all-finite-groups-bound',all(g in evidence for g in row['finiteWorkGroups']))
        if sid!='conjure_flora':check(sid+'/audited-procedure-unchanged',operative==r['a_acquisition']['completeControllingOperativeProcedure'])
        else:check(sid+'/accepted-provider-correction-bound','FAA-01'in register['findingEvidence'])
        joined.append({'id':sid,'currentPublic':deepcopy(p),'currentCompleteContract':deepcopy(c),
            'reviewedAcquisitionDescriptor':deepcopy(r['a_acquisition']),
            'mandatorySelectionsAndSnapshots':deepcopy(row['exactMandatorySelectionAndSnapshotDescriptor']),
            'initialState':deepcopy(row['exactInitialStateDescriptor']),
            'conditionalOrDeferred':deepcopy(row['exactConditionalOrDeferredDescriptor']),
            'finiteGroupEvidence':{g:evidence[g] for g in row['finiteWorkGroups']},
            'specializedCurrentEvidence':{k:v for k,v in row.items() if k.endswith('Evidence')},
            'commonPaymentAndInitializationEvidence':info(hist_path),
            'ordinaryAllowanceDescriptorPointer':('/entries/'+str(fw['exactMembers'].index(sid))) if sid in entries else None,
            'all335FullAcquisitionsExecuted':False,'fullUseRuntimeApproved':False})
    check('public-and-internal-selection-remains-disabled',pub['selectionEnabled'] is False and internal['selectionEnabled'] is False)
    for b in bindings:check('stable-input/'+b['path'],info(G/b['path'])==b)
    assembly={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'finite audit assembly complete; full exact review pending',
        'sourceBindings':bindings,'finiteGroupEvidence':evidence,'entries':joined,
        'fulfills':['AA-18','FW-08'],'allFiniteGroupsBound':True,
        'scope':'All335 current full source wrappers, menus, raw fields and exact acquisition/initial-state descriptors joined to finite evidence. New execution is only bounded allowance/identity algebra, not new paid acquisitions or full use simulation.',
        'historicalEvidenceRerun':False,'all335FullAcquisitionsExecuted':False,'fullFeatExactApproved':False,
        'runtimeApproved':False,'humanBalanceApproved':False,'wholeGameFlowConfirmed':False,'pushed':False,'cosmologyReviewed':False,'sourceInformationDeleted':0}
    join_path.write_text(json.dumps(assembly,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'counts':{**descriptor['counts'],'finiteFeatRows':60,'finiteAllowances':62,
            'cadenceRows':sum(bool(e['laterEventCadences']) for e in entries.values()),'joinedSourceRecords':335},
        'assembly':info(join_path),'reusedFS06Results':reused,'newBoundaryTraces':traces,'results':checks,
        'finiteWorkGroup':'FW-08','acceptanceGroup':'AA-18','fullFeatExactApproved':False,
        'newPaidAcquisitionsExecuted':0,'newFullUseProceduresExecuted':0,'newGameRules':0,'cosmologyReviewed':False}
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'counts':report['counts'],'report':info(report_path),'assembly':info(join_path)}))


if __name__=='__main__':main()
