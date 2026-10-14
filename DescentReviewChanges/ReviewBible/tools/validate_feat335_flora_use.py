"""Actual paid Flora/Trapcasting source history plus named conditional use traces."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json
from feat335_flora_use import FloraUse
from feat_exact_01_flora_acquisition import FloraAcquisition
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read,info,serial

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'


def main():
    out=A/'FEAT335_FLORA_USE_CHECK.json';assert not out.exists()
    paths=[R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R/'data/director/magic_core_feat_operating_proposal_internal.json',R/'data/public/feat_candidates/exact_01/shared_rules.json',
        R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
        Path(__file__),*[R/'tools'/n for n in ['feat335_flora_use.py','feat_exact_01_flora_acquisition.py',
            'feat_exact_01_remaining_owned_chains.py','feat_exact_01_casting_selections.py','feat_exact_01_composite_casting_model.py',
            'feat_exact_01_initiate_acquisition_model.py','feat_exact_01_casting_credential_model.py',
            'feat_exact_01_training_prerequisite_model.py','feat_exact_01_acquisition_models.py','core_playtest_rules.py','spell_playtest_rules.py']]]
    bindings=[info(p) for p in paths]
    foundation,ancestry,equipment,sm,dependencies,wizard,contracts,prior,core=[read(p) for p in paths[:9]]
    classes={x['class']:x for x in foundation['classes']};skills={s:a for a,ss in foundation['skillAbilities'].items() for s in ss}
    equipment={x['id']:x for x in equipment['records']};backgrounds={x['id']:x for x in ancestry['backgrounds']}
    supplements={x['id']:x['value'] for x in sm['groups']};contracts={x['id']:x for x in contracts['records']}
    sources=CastingSources(G,dependencies['spells'],supplements,wizard)
    checks=[];histories=[]
    def check(label,ok,detail=None):
        checks.append({'id':label,'passed':bool(ok),'detail':deepcopy(detail)});assert ok,label
    def reject(label,m,call):
        before=m.snapshot()
        try:call()
        except ValueError as e:check(label,True,str(e))
        else:check(label,False)
        check(label+'/no-partial-commit',m.snapshot()==before)
    def world():
        return {'evidenceMode':'conditional_fixture','actors':{
            'owner':{'position':0,'canAct':True,'spokenCommand':True,'silenced':False,'visibleCommand':False,'perceivesPlants':True,'saves':{'DEX':0,'CON':0,'STR':0},'conditionImmunities':[]},
            'enemy':{'position':15,'saves':{'DEX':0,'CON':0,'STR':0},'conditionImmunities':[]},
            'ally':{'position':20,'saves':{'DEX':0,'CON':0,'STR':0},'conditionImmunities':[]},
            'distant':{'position':100,'saves':{'DEX':0,'CON':0,'STR':0},'conditionImmunities':[]}},
            'supportedVisibleGround':[5,10,20,25,30,35,75], 'walls':[],
            'areas':{'square-A':{'origin':15,'supported':True,'creatures':['enemy','ally']}}}
    def make(curriculum='Wizard',level=12,trap=True):
        actor=deepcopy(prior['actorSourceProjection']);actor.update(firstClass='Warrior',classLevels={'Warrior':1},selectedClassSkills=['Nature','Athletics'])
        h=FloraAcquisition(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources);h.configure_choice_sources(core)
        paid=InitiateAcquisitions(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements['SUP-04'],dependencies['spells'])
        paid.advance(4);paid.earn(4);ability,cantrips,rank1=prior['authoredCurriculumChoices'][curriculum]
        paid.acquire('magicInitiate',4,{'curriculum':curriculum,'cantrips':cantrips,'rank1':rank1})
        h.advance(4);h.pay=paid.pay;h.casting.import_initiate(paid,4)
        h.advance(8);h.earn(8);h.acquire_named('conjure_flora',8,h.actual_casting_routes()[0])
        if level>8:h.advance(level)
        if trap:
            assert level>=12;h.earn(12);h.acquire_named('trapcasting',12)
        m=FloraUse(h,world());m.begin_turn('owner-regular-1','round-1',0)
        return m
    def record(label,m,**extra):histories.append({'id':label,'state':m.snapshot(),'extra':deepcopy(extra),'worldStatus':'conditional_source_qualified_fixture_not_campaign_fact'})

    check('three-current-modes',set(x['id'] for x in supplements['SUP-07']['floraBody']['modes'])=={'lash','spore','entangle'})
    check('current-command-phase-and-one-outcome-source','A coordinated command chooses only one permitted outcome' in supplements['SUP-07']['floraBody']['commandChoice'])
    check('current-Trapcasting-narrow-exception','first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase' in contracts['trapcasting']['completeOperativeProcedure'])
    for curriculum in ['Dragoon','Monk','Thief','Wizard','Cleric','Bard']:
        m=make(curriculum);before=m.acquired.snapshot();p=m.create('create','p','lash',10,60)
        check(curriculum+'/paid-distinct-ancestry-provider-history',m.acquired.pay.current_classes=={'Warrior':12} and m.acquired.pay.has('trapcasting'))
        check(curriculum+'/initial-body-snapshot',p['maximumHP']==9 and p['hp']==9 and p['saveBonus']==4 and p['ac']==12)
        check(curriculum+'/no-cast-RP-repertoire-or-score-grant',m.acquired.casting.snapshot()==before['casting'] and m.acquired.pay.scores==before['payment']['scores'])
        result=m.command('command',['p'],'lash',['enemy'],{'enemy':1},die=5)
        check(curriculum+'/source-DC-and-one-native-result',result[0]['dc']==m.acquired.flora_dc_projection()['dc'] and result[0]['nativeDamage']==5 and len(result)==1)
        record('retained-provider-to-actual-Lash/'+curriculum,m)

    for mode in ['lash','spore','entangle']:
        for success in [False,True]:
            m=make();m.create('create','p',mode,10,60)
            targets=['enemy','ally'] if mode=='entangle' else ['enemy'];roll=20 if success else 1
            result=m.command('command',['p'],mode,targets,{t:roll for t in targets},die=5 if mode=='lash' else None,
                deadlines={t:12 for t in targets},area='square-A' if mode=='entangle' else None)
            check(mode+str(success)+'/binary-save-not-attack',all(r['save']['success']==success for r in result))
            if mode=='lash':check(mode+str(success)+'/half-floors',result[0]['nativeDamage']==(2 if success else 5))
            else:check(mode+str(success)+'/native-condition-only',all(r['nativeDamage']==0 and (r['condition'] is None)==success for r in result))
            check(mode+str(success)+'/one-BA-one-owner-offense',m.bonus_actions==0 and m.offense=={'round-1'} and m.phases=={'owner-regular-1'})
            record('command/'+mode+'/'+str(success),m,outcomes=result)

    m=make();m.create('first','p1','spore',10,60)
    reject('second-still-costs-an-Action',m,lambda:m.create('second','p2','entangle',20,66,additional=True))
    m.begin_turn('owner-regular-2','round-2',6);m.create('second','p2','entangle',20,66,additional=True)
    check('two-bodies-one-rest-charge-no-remaining-second',m.initial['creationUses']['current']==0 and len(m.initial['activePlants'])==2 and not m.initial['additionalCreationPending'])
    result=m.command('combined-Lash',['p1','p2'],'lash',['enemy'],{'enemy':1},die=6)
    check('coordinated-group-one-die-not-per-plant',len(result)==1 and result[0]['nativeDamage']==6)
    m.begin_turn('owner-extra','round-2',7,regular=False)
    reject('extra-turn-no-second-attached-phase',m,lambda:m.command('extra-command',['p1'],'lash',['enemy'],{'enemy':1},die=6))
    reject('third-body-no-entitlement',m,lambda:m.create('third','p3','lash',25,67,additional=True))
    m.advance(60);check('first-expires-on-original-deadline-second-survives',not m.plants['p1']['active'] and m.plants['p2']['active'])
    m.advance(66);check('second-own-deadline-not-parent-extension',not m.plants['p2']['active'])
    record('two-paid-Actions-one-charge-independent-clocks',m)

    m=make(level=8,trap=False);m.create('first','p','lash',10,60)
    m.acquired.advance(10);m.begin_turn('owner-regular-2','round-2',6)
    check('level-growth-no-charge-or-retroactive-second',m.initial['plantCapacity']==2 and m.initial['creationUses']['current']==0 and m.second is None)
    reject('growth-cannot-replay-old-use-as-level10',m,lambda:m.create('second','p2','lash',20,66,additional=True))
    check('creation-PB-snapshot-not-live-growth',m.plants['p']['maximumHP']==8 and m.plants['p']['saveBonus']==3)
    record('level8-creation-then-level10-capacity',m)

    m=make();m.create('first','p','spore',10,60,armed=True)
    m.world['actors']['enemy']['position']=10
    result=m.enter('forced-entry','p','enemy',1,from_outside=True,meaningful_hostile=True,deadline=12)
    check('off-phase-spore-trap-DEX-not-CON',result[0]['saveAbility']=='DEX' and result[0]['condition']['kind']=='Poisoned')
    reject('entry-spends-same-command-offense',m,lambda:m.command('after-trap',['p'],'lash',['enemy'],{'enemy':1},die=6))
    m.begin_turn('extra-same-round','round-1',1,regular=False)
    check('same-hostile-entry-not-repeated',m.enter('reenter','p','enemy',1,from_outside=True,meaningful_hostile=True,deadline=12)==[])
    m.begin_turn('owner-regular-2','round-2',6)
    check('real-later-round-trap-may-qualify',len(m.enter('next-entry','p','enemy',20,from_outside=True,meaningful_hostile=True,deadline=18))==1 and 'round-2'in m.offense)
    check('successful-trap-save-still-spends-offense',len(m.conditions)==1)
    m.damage('p',9);check('destroying-generator-ends-condition-no-dying-body',not m.conditions and not m.plants['p']['active'] and m.plants['p']['endReason']=='destroyed-at-zero-no-corpse')
    reject('dead-plant-no-healing-recreation',m,lambda:m.heal('p',9))
    record('trap-entry-shared-budget-generator-ending',m)

    for mode in ['lash','entangle']:
        m=make();m.create('first','p',mode,10,60,armed=True);m.world['actors']['enemy']['position']=10
        check(mode+'/placement-not-entry',m.enter('placement','p','enemy',1,from_outside=False,meaningful_hostile=True,die=5 if mode=='lash' else None,deadline=12)==[] and not m.offense)
        check(mode+'/nonhostile-not-trigger',m.enter('friendly','p','enemy',1,from_outside=True,meaningful_hostile=False,die=5 if mode=='lash' else None,deadline=12)==[] and not m.offense)
        result=m.enter('real-entry','p','enemy',1,from_outside=True,meaningful_hostile=True,die=5 if mode=='lash' else None,deadline=12)
        check(mode+'/DEX-trap-payload',result[0]['saveAbility']=='DEX' and (result[0]['nativeDamage']==5 if mode=='lash' else result[0]['condition']['kind']=='Restrained'))
        if mode=='entangle':
            escape=m.escape('actual-escape','p','enemy',20,0,ability='DEX(Acrobatics)',can_act=True)
            check('entangle/real-task-escape',escape['success'] and not m.conditions)
        record('trap/'+mode,m)

    for mode in ['lash','spore','entangle']:
        m=make();m.create('create','p',mode,10,60,armed=True)
        # The area contains owner0/enemy15/ally20: owner is not excluded.
        targets=['owner','enemy','ally'];result=m.burst('burst','p',targets,{'owner':1,'enemy':20,'ally':1},[3,4])
        check(mode+'/all-area-targets-and-half',[(r['target'],r['nativeDamage']) for r in result]==[('owner',7),('enemy',3),('ally',7)])
        check(mode+'/fixed-burst-type',all(r['damageType']==('poison' if mode=='spore' else 'piercing') for r in result))
        check(mode+'/body-ends-before-payload-no-refund',m.history[-1]['plantEndedBeforePayload'] and m.initial['creationUses']['current']==0)
        reject(mode+'/no-same-dead-body-command',m,lambda:m.command('later',['p'],'lash',['enemy'],{'enemy':1},die=6))
        record('burst/'+mode,m)

    m=make();m.create('create','p','spore',10,60,armed=True)
    m.world['actors']['owner']['silenced']=True
    reject('spoken-command-silenced',m,lambda:m.command('silenced',['p'],'spore',['enemy'],{'enemy':1},deadlines={'enemy':12}))
    m.world['actors']['owner']['visibleCommand']=True;m.world['actors']['enemy']['conditionImmunities']=['Poisoned']
    result=m.command('visible-command',['p'],'spore',['enemy'],{'enemy':1},deadlines={'enemy':12})
    check('actual-visible-channel-and-immunity',result[0]['condition'] is None and not m.conditions)
    m.begin_turn('owner-regular-2','round-2',6);m.damage('p',4);old=deepcopy(m.plants['p']);m.acquired.advance(16)
    check('healing-only-existing-deficit',m.heal('p',30)==4 and m.plants['p']['maximumHP']==old['maximumHP'] and m.plants['p']['deadline']==old['deadline'])
    failed=m.disarm('failed-disarm','p',1,0,tools=True,reach=True)
    check('failed-disarm-no-explosion',not failed['success'] and m.plants['p']['active'] and m.plants['p']['armed'] and not m.offense-{'round-1'})
    success=m.disarm('safe-disarm','p',20,0,tools=True,reach=True)
    check('disarm-body-retained',success['success'] and m.plants['p']['active'] and not m.plants['p']['armed'])
    m.uproot('p');check('uproot-ends-no-cargo-plant',not m.plants['p']['active'] and m.plants['p']['noLootOrResourceOutputs'])
    record('channels-immunity-current-body-healing-disarm-uproot',m)

    m=make();before=m.snapshot()
    reject('no-unsupported-ground',m,lambda:m.create('x','p','lash',15,60))
    reject('no-out-of-range-ground',m,lambda:m.create('x','p','lash',35,60))
    m.world['walls']=[5];reject('no-blocked-line',m,lambda:m.create('x','p','lash',10,60));m.world['walls']=[]
    m.create('create','p','entangle',10,60)
    reject('entangle-cannot-exclude-real-ally',m,lambda:m.command('exclude',['p'],'entangle',['enemy'],{'enemy':1},deadlines={'enemy':12},area='square-A'))
    reject('burst-cannot-exclude-owner',m,lambda:m.burst('exclude-owner','p',['enemy','ally'],{'enemy':1,'ally':1},[3,4]))
    m.offense.add('round-1')  # Explicit earlier actual OTHER companion offense premise.
    reject('other-companion-spent-budget-blocks-Flora',m,lambda:m.command('after-other',['p'],'lash',['enemy'],{'enemy':1},die=4))
    record('physical-and-shared-budget-rejections',m)

    m=make();m.create('first','p','lash',10,60);m.advance(60)
    check('missed-second-not-banked',m.second is None and not m.initial['additionalCreationPending'])
    m.advance(3600)
    check('debt-only-rest-no-refill',not m.rest('debt',beneficial=False,kind='SR') and m.initial['creationUses']['current']==0)
    check('actual-beneficial-rest-refills-only-creation-use',m.rest('sr-1',beneficial=True,kind='SR') and m.initial['creationUses']['current']==1 and not m.initial['activePlants'] and not m.second)
    m.begin_turn('later-regular','round-later',3600);m.create('new-use','p2','lash',10,3660)
    check('rest-replay-no-refill',not m.rest('sr-1',beneficial=True,kind='LR') and m.initial['creationUses']['current']==0)
    record('expired-entitlement-and-real-rest-receipt',m)
    check('all-source-bindings-stable',bindings==[info(p) for p in paths])
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'results':checks,'histories':histories,'completeFloraSupplement':supplements['SUP-07']['floraBody'],
        'completeContracts':{k:contracts[k] for k in ['conjure_flora','trapcasting','verdant_bond']},
        'counts':{'profiles':3,'retainedActualCastingProviders':6,'recordedHistories':len(histories)},
        'scope':'Paid-source-to-body creation, conditional command/trap/burst state, one shared offense, source DC, binary saves and selected lifecycle conservation. Native damage outputs are before ordinary defenses; condition records do not execute every action restriction.',
        'limits':['Actual world, sound/sight, meaningful opposition, target/body positions, supported squares, completed action/escape/disarm facts and canonical clock/rest identities are explicit conditional premises, not authenticated campaigns.',
            'All positions lie on one axis. Arbitrary geometry, movement, attacks against plant AC, passive damage defenses, owner/target whole HP/Wound engines and actual inventory/cargo are outside this bounded slice.',
            'Command commitment and its one immediately following attached phase are a single bounded operation. Interruption between command and phase, suppressed source resumption and owner death need governing interfaces; no generic alternate rule is implied.',
            'Lost casting-provider use and creating the second plant after the first is destroyed/uprooted before its original minute endpoint remain explicit source-adjudication questions. The model declines those unimplemented cases without declaring them illegal game actions.',
            'Verdant Bond actual message and Nature-route effects, enemy identification of armed mode, full virtual-marker scheduler and no-resource integration remain separate finite work. No complete FXC04/09 closure or exact feat approval is claimed.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'counts':result['counts'],'report':info(out)}))

if __name__=='__main__':main()
