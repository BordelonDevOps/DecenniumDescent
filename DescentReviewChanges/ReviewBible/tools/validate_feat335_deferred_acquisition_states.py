"""FW06/AA15 exact20 source-to-initial-state and paid opportunity histories."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from pathlib import Path
from feat335_deferred_acquisition_states import DeferredAcquisitionStates,IDS
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read,info,serial

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'


def main():
    out=A/'FEAT335_DEFERRED_ACQUISITION_STATE_CHECK.json'
    descriptors=A/'FEAT335_DEFERRED_ACQUISITION_DESCRIPTORS.json'
    assert not out.exists() and not descriptors.exists()
    paths=[R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/public/feat_candidates/exact_01/shared_rules.json',
        A/'feat335-acquisition-audit-01-verdict/ACQUISITION_ROWS.json',
        A/'feat335-acquisition-audit-01-verdict/FINITE_REMAINING_WORK.json',
        R/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',Path(__file__),
        *[R/'tools'/n for n in ['feat335_deferred_acquisition_states.py','feat_exact_01_remaining_owned_chains.py',
            'feat_exact_01_composite_casting_model.py','feat_exact_01_trade_selections.py',
            'feat_exact_01_prodigy_choices.py','feat_exact_01_casting_credential_model.py',
            'feat_exact_01_acquisition_models.py','feat_exact_01_initiate_acquisition_model.py',
            'feat_exact_01_training_prerequisite_model.py']],A/'FEAT335_CURSE_CAPACITY_DERIVED_OPERATIONS.json']
    bindings=[info(p) for p in paths]
    foundation,ancestry,equip_doc,supp_doc,dep_doc,wizard,contract_doc,prior=[read(p) for p in paths[:8]]
    classes={x['class']:x for x in foundation['classes']};skills={s:a for a,g in foundation['skillAbilities'].items() for s in g}
    equipment={x['id']:x for x in equip_doc['records']};backgrounds={x['id']:x for x in ancestry['backgrounds']}
    contracts={x['id']:x for x in contract_doc['records']};supplements={x['id']:x['value'] for x in supp_doc['groups']}
    sources=CastingSources(G,dep_doc['spells'],supplements,wizard)
    public={x['id']:x for x in read(paths[8])['feats']};rows={x['id']:x for x in read(paths[10])['rows']}
    fw=next(x for x in read(paths[11])['groups'] if x['id']=='FW-06')
    checks=[];histories=[];entries=[]

    def check(label,truth,details=None):
        checks.append({'id':label,'passed':bool(truth),'details':deepcopy(details)})
        assert truth,label

    def reject(label,h,action,reason):
        before=h.snapshot()
        try:action()
        except ValueError as error:check(label+'/reason',reason in str(error),str(error))
        else:check(label+'/reject',False)
        check(label+'/atomic',h.snapshot()==before)

    def op(h,level):h.advance(level);h.earn(level)

    def make(sid,model=DeferredAcquisitionStates):
        actor=deepcopy(prior['actorSourceProjection'])
        actor.update(firstClass='Warrior',classLevels={'Warrior':1},selectedClassSkills=['Nature','Athletics'])
        if sid in {'temporal_theory','curse_channeling'}:
            actor.update(background='arcane-academy-dropout',backgroundToolChoice=None,backgroundDuplicateSkillChoice=None)
        h=model(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources)
        level=8
        if sid in {'familiar_bond','core_infusion','arcane_momentum'}:
            op(h,4);h.initiate()
        if sid=='core_infusion':
            op(h,8);h.acquire_artisan_training(8,paths[12].read_text(encoding='utf-8'));level=12
        elif sid=='master_smithing':
            op(h,4);h.acquire_artisan_training(4,paths[12].read_text(encoding='utf-8'))
        elif sid=='arcane_momentum':
            op(h,8);h.acquire_parent('power_attack',8);level=12
        elif sid=='frenzied_rage':
            op(h,4);h.acquire_named('berserker',4)
        h.advance(level)
        return h,level

    check('exact20-GPT-group-members',set(fw['exactMembers'])==IDS and len(IDS)==20)
    expected={
      'runic_shield':lambda s:s=={'armed':True,'ward':None},
      'spell_reservoir':lambda s:s['uses']=={'maximum':1,'current':1,'recovery':'beneficial-owner-LR'} and not s['claimedRestEvents'],
      'mental_buffer':lambda s:s['uses']=={'maximum':1,'current':1,'recovery':'beneficial-owner-LR'} and not s['suppressedApplications'],
      'ritual_channeler':lambda s:s=={'permissionOnly':True},
      'quick_learner':lambda s:not s['languageCategoryUsed'] and not s['toolCategoryUsed'] and not s['projects'],
      'core_infusion':lambda s:s['rerollUses']=={'maximum':1,'current':1,'recovery':'beneficial-owner-SR-or-LR'} and s['activeInfusion'] is None,
      'master_smithing':lambda s:s['lastSuccessfulTemperCompletion'] is None and not s['ownedOutputProperties'] and not s['storedSpells'],
      'dark_binding':lambda s:s['boundWeapon'] is None and not s['bindingRitualCompleted'],
      'temporal_theory':lambda s:s['tokenCapacity']==2 and not s['tokens'] and s['activeEncounter'] is None and s['spentTokenCount']==0 and not s['deferredFatigue'],
      'arcane_momentum':lambda s:s['maximum']==3 and s['current']==0 and not s['qualifiedAttackIds'] and s['activeEncounter'] is None and s['declaredEnhancement'] is None,
      'lightning_affinity':lambda s:s=={'stormChargeCapacity':2,'stormCharges':[],'primedRider':None},
      'curse_channeling':lambda s:s['markCapacity']==1 and not s['marks'] and not s['dropEntitlementHistory'],
      'combat_reflexes':lambda s:not s['extraReactionAvailable'] and s['extraReactionEpoch'] is None and not s['spentTriggerIds'],
      'frenzied_rage':lambda s:s=={'rageInstances':{}},
      'energy_sink':lambda s:s['uses']=={'maximum':3,'current':3,'recovery':'beneficial-owner-LR'} and not s['claimedCastRoots'],
      'endurance':lambda s:s=={'foodWaterPending':0,'sleepPending':0},
      'spellweave':lambda s:s=={'heldCapacity':1,'heldBuff':None},
      'leadership':lambda s:s=={'designationCapacity':3,'designatedContracts':[]},
      'familiar_bond':lambda s:s=={'maximumHpContribution':8,'bodyCreated':False},
      'empowered_summoning':lambda s:s=={'creationLineages':{},'bodyCreated':False}}
    for sid in sorted(IDS):
        p=public[sid].get('unchangedReviewedRecord',public[sid])
        check(sid+'/exact-complete-source-parity',contracts[sid]['completeOperativeProcedure']==p['operationalRules']==rows[sid]['a_acquisition']['completeControllingOperativeProcedure'])
        h,level=make(sid);before=h.snapshot()
        check(sid+'/actual-acquisition-prerequisite',h.prerequisite(sid))
        reject(sid+'/no-free-acquisition',h,lambda:h.acquire_deferred(sid,level),'No unspent earned opportunity')
        h.earn(level)
        reject(sid+'/later-menu-is-not-purchase-choice',h,lambda:h.acquire_deferred(sid,level,{'inventedLaterChoice':True}),'no permanent purchase menu')
        environment=deepcopy(h.environment);casting=h.casting.snapshot();prior_init=deepcopy(h.initializations)
        grant=h.acquire_deferred(sid,level)
        state=deepcopy(h.initializations[sid])
        check(sid+'/source-defined-initial-state',expected[sid](state),state)
        check(sid+'/separate-real-paid-opportunity',grant['opportunity']=='Warrior:'+str(level) and h.pay.opportunities[grant['opportunity']]['spent'])
        check(sid+'/no-world-HP-RP-debt-condition-body-or-inventory-change',h.environment==environment)
        check(sid+'/no-cast-repertoire-or-use-recovery',h.casting.snapshot()==casting)
        check(sid+'/prior-feat-state-retained',{k:h.initializations[k] for k in prior_init}==prior_init)
        # Given legitimate old spending/journals, a later level must not reset them.
        if sid=='energy_sink':
            h.initializations[sid]['uses']['current']=0
            h.initializations[sid]['claimedCastRoots']=['conditional-spent-root']
        elif sid in {'mental_buffer','spell_reservoir'}:h.initializations[sid]['uses']['current']=0
        elif sid=='core_infusion':h.initializations[sid]['rerollUses']['current']=0
        h.advance(16);h.earn(16)
        reject(sid+'/nonrepeatability-preserves-state',h,lambda:h.acquire_deferred(sid,16),'Nonrepeatable identity already acquired')
        if sid=='energy_sink':
            check(sid+'/PB-growth-capacity-only',h.initializations[sid]['uses']=={'maximum':5,'current':0,'recovery':'beneficial-owner-LR'} and h.initializations[sid]['claimedCastRoots']==['conditional-spent-root'])
        elif sid in {'mental_buffer','spell_reservoir'}:check(sid+'/no-level-recharge',h.initializations[sid]['uses']['current']==0)
        elif sid=='core_infusion':check(sid+'/no-level-recharge',h.initializations[sid]['rerollUses']['current']==0 and h.initializations[sid]['activeInfusion'] is None)
        elif sid=='curse_channeling':check(sid+'/live-capacity-no-marks',h.initializations[sid]['markCapacity']==2 and not h.initializations[sid]['marks'])
        elif sid=='leadership':check(sid+'/live-capacity-no-followers',h.initializations[sid]['designationCapacity']==5 and not h.initializations[sid]['designatedContracts'])
        elif sid=='familiar_bond':check(sid+'/live-capacity-no-body',h.initializations[sid]['maximumHpContribution']==16 and h.environment['familiar'] is None)
        else:check(sid+'/later-level-no-event-backfill',h.initializations[sid]==state)
        index=len(histories)
        histories.append({'id':sid,'before':before,'paidGrant':grant,'atAcquisition':state,'after':h.snapshot(),
            'scope':'Paid source-qualified partial character; environmental history and post-acquisition spending inputs are conditional fixtures.'})
        entries.append({'id':sid,'completeContract':deepcopy(contracts[sid]),
            'gptMandatorySelectionDescriptor':deepcopy(rows[sid]['b_mandatorySelectionsAndSnapshots']),
            'gptInitialStateDescriptor':deepcopy(rows[sid]['c_initialState']),
            'initialStateAtPaidAcquisition':state,'earnedGrant':grant,'historyPointer':'/histories/'+str(index),
            'doesNotImplementFullUse':True})

    h,level=make('runic_shield');h.earn(level);h.acquire_deferred('runic_shield',level)
    before=h.snapshot()
    check('Runic/no-past-encounter-backfill',not h.conditional_next_encounter('conditional-old-encounter') and h.initializations['runic_shield']['ward'] is None)
    check('Runic/actual-next-encounter-shape',h.conditional_next_encounter('conditional-next-encounter') and h.initializations['runic_shield']=={'armed':False,'ward':{'points':15,'encounter':'conditional-next-encounter'}})
    h.initializations['runic_shield']['ward']['points']=2
    check('Runic/repeated-initiative-no-refill',not h.conditional_next_encounter('conditional-next-encounter') and not h.conditional_next_encounter('conditional-second-encounter') and h.initializations['runic_shield']['ward']['points']==2)
    check('Runic/debt-only-rest-no-rearm',not h.conditional_runic_rest('conditional-debt-only',False) and h.initializations['runic_shield']['ward']['points']==2)
    check('Runic/beneficial-rest-ends-ward-and-arms',h.conditional_runic_rest('conditional-rest-1',True) and h.initializations['runic_shield']=={'armed':True,'ward':None})
    check('Runic/new-encounter-consumes-armed-grant',h.conditional_next_encounter('conditional-third-encounter'))
    check('Runic/duplicate-rest-not-second-rearm',not h.conditional_runic_rest('conditional-rest-1',True) and not h.initializations['runic_shield']['armed'])
    histories.append({'id':'Runic-deferred-first-encounter-and-rest','before':before,'after':h.snapshot(),'scope':'Conditional event shape only; no encounter/rest eligibility engine or damage interception executed.'})

    body={'spellId':'find-familiar','bodyId':'conditional-real-source-familiar','nativeMaximumHP':10,'maximumHP':10,'currentHP':4,'featMaximumContributions':{}}
    h,level=make('familiar_bond');h.environment['familiar']=deepcopy(body);h.earn(level);before=h.snapshot()
    h.acquire_deferred('familiar_bond',level)
    check('Familiar/existing-body-capacity-not-healing',h.environment['familiar']['maximumHP']==18 and h.environment['familiar']['currentHP']==4)
    h.advance(9)
    check('Familiar/later-level-capacity-not-healing',h.environment['familiar']['maximumHP']==19 and h.environment['familiar']['currentHP']==4)
    h.conditional_familiar_arrival(body,False)
    check('Familiar/returned-existing-body-no-refill',h.environment['familiar']['maximumHP']==19 and h.environment['familiar']['currentHP']==4)
    h.conditional_familiar_arrival({**body,'bodyId':'conditional-genuinely-new-body','currentHP':10},True)
    check('Familiar/genuine-new-creation-starts-at-lawful-new-maximum',h.environment['familiar']['maximumHP']==h.environment['familiar']['currentHP']==19)
    unrelated={**body,'spellId':'summon-familiar','bodyId':'conditional-different-spell-body'}
    h.conditional_familiar_arrival(unrelated,False)
    check('Familiar/no-name-alias-or-foreign-body-grant',h.environment['familiar']==unrelated)
    histories.append({'id':'Familiar-existing-versus-new-and-returned-body','before':before,'after':h.snapshot(),'scope':'Body identities/new-creation predicates are conditional source-qualified premises, not executed summon activations.'})

    h,level=make('empowered_summoning');h.earn(level)
    h.environment['summons']=[{'body':'conditional-existing-summon','currentHP':2,'tempHP':0,'creationRoot':'conditional-old-root','roundRider':None}]
    old=deepcopy(h.environment);h.acquire_deferred('empowered_summoning',level)
    check('Empowered/purchase-does-not-backfill-existing-body',h.environment==old and not h.initializations['empowered_summoning']['creationLineages'])
    histories.append({'id':'Empowered-existing-summon-not-retroactive','after':h.snapshot(),'scope':'Acquisition only. Later creation and rolled-damage use retain unchanged reviewed full procedure.'})

    for model in [DeferredAcquisitionStates,RemainingOwnedChains]:
        for attained in [9,10,12]:
            h,level=make('curse_channeling',model);h.earn(8);h.advance(attained)
            if model is DeferredAcquisitionStates:h.acquire_deferred('curse_channeling',8)
            else:h.acquire_named('curse_channeling',8)
            check(model.__name__+'/saved-opportunity-current-level/'+str(attained),h.initializations['curse_channeling']['markCapacity']==(2 if attained>=10 else 1) and not h.initializations['curse_channeling']['marks'])
            histories.append({'id':model.__name__+'/saved-opportunity/'+str(attained),'after':h.snapshot()})
    check('all-source-bindings-stable',[info(p) for p in paths]==bindings)
    descriptor_doc={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Exact20 FW06 initial-state descriptors joined to complete unchanged procedures and genuine paid prerequisite/opportunity histories; later use remains separately governed.',
        'sourceBindings':bindings,'entries':entries,'newGameRules':0,'fullFeatCandidateApproved':False}
    descriptors.write_text(json.dumps(descriptor_doc,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8')
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'acceptanceGroups':['AA-15'],'finiteWorkGroup':'FW-06','exactDescriptorCount':20,'historyCount':len(histories),
        'sourceBindings':bindings,'descriptors':info(descriptors),'results':checks,'histories':histories,
        'scope':'Finite paid initialization/capacity preservation. Conditional later event shapes only; no full event/runtime/actor implementation or campaign proof.',
        'limitations':['No crafting, courses, command, combat or rest eligibility engine implemented.',
            'Endurance acquisition preserves existing Strain/debt/deadlines/events; its already-reviewed later EX58 penalty rules are not reexecuted here.',
            'Existing/redeployed summon bodies receive no retroactive purchase grant; full later summon activation retains its unchanged reviewed procedure.',
            'Core Infusion uses actual paid Artisan Smith-tools plus actual paid Wizard Initiate; the independent Engineering alternative is unchanged and outside this history.',
            'Frenzied Rage uses actual paid Berserker; external class-rage branches remain conditional under ACQ04.'],
        'newGameRules':0,'sourceInformationDeleted':0,'fullFeatCandidateApproved':False}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(out),'descriptors':info(descriptors)}))


if __name__=='__main__':main()
