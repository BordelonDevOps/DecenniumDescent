"""One-use source-bound Nature transaction evidence. World facts are conditional."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from feat335_nature_transactions import NativeNatureActor, NatureBorrowedTransactions, NatureTransactions, NATURE
from feat335_nature_acquisition import NatureAcquisitions as CompositeCastingHistory
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_lineage_prerequisite_model import current_lineage
from validate_feat_exact_01_composite_casting import read, info, serial

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def main():
    output=A/'FEAT335_NATURE_TRANSACTIONS_CHECK.json';assert not output.exists()
    foundation=read(R/'data/playtest/character_foundation.json');classes={x['class']:x for x in foundation['classes']}
    skills={s:a for a,names in foundation['skillAbilities'].items() for s in names}
    ancestry=read(R/'data/playtest/ancestry_background_candidate.json');backgrounds={x['id']:x for x in ancestry['backgrounds']}
    equipment={x['id']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records']}
    supplements={x['id']:x['value'] for x in read(R/'data/public/feat_candidates/exact_01/supplements.json')['groups']}
    contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
    class_sources={n:read(G/classes[n]['classCandidatePath']) for n in ['Ranger','Bard','Warrior']}
    wizard=read(R/'data/public/class_playtests/wizard.json')
    sources=CastingSources(G,read(R/'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells'],supplements,wizard)
    template=read(A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json')['actorSourceProjection']
    allowance=next(x for x in read(A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json')['entries'] if x['id']=='versatile_mastery')['finiteAllowances'][0]
    controlling=read(A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json')
    card=next(c for c in class_sources['Ranger']['cards'] if c['id']==NATURE)
    ranger_path=G/classes['Ranger']['classCandidatePath'];binding=info(ranger_path)
    assert any(x['path']==binding['path'] and x['sha256']==binding['sha256'] and x['bytes']==binding['bytes'] for x in controlling['descendants'])
    authority={'reviewId':controlling['reviewId'],'effect':card['effect'],'currentSource':binding,'record':info(A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json')}
    eligible=[c for c in class_sources['Ranger']['cards'] if c['band']=='Base' and c['minimumClassLevel']<=1 and c['acquisition']=='selection']
    selection=[NATURE]+[c['id'] for c in sorted(eligible,key=lambda c:c['sourceKind']!='active') if c['id']!=NATURE][:3]
    paths=[Path(__file__),R/'tools/feat335_nature_transactions.py',R/'tools/feat335_nature_acquisition.py',R/'tools/feat335_borrowed_skill_transactions.py',R/'tools/feat335_borrowed_transactions.py',R/'tools/feat335_borrowed_stunts.py',
        R/'tools/feat335_allowance_bindings.py',R/'tools/feat_exact_01_composite_casting_model.py',R/'tools/feat_exact_01_training_prerequisite_model.py',
        R/'tools/feat_exact_01_lineage_prerequisite_model.py',R/'tools/feat_exact_01_acquisition_models.py',R/'tools/feat_exact_01_casting_credential_model.py',R/'tools/core_playtest_rules.py',
        R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',R/'data/playtest/equipment_source_catalog.json',
        R/'data/public/feat_candidates/exact_01/supplements.json',R/'data/public/feat_candidates/exact_01/shared_rules.json',R/'data/public/feat_candidates/exact_01/spell_dependencies.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json',
        A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json',A/'FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json',A/'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json',
        A/'feat335-nature-source-check-01-verdict/FINITE_NATURE_EXPECTATIONS.json',A/'feat335-nature-source-check-01-verdict/NATURE_FOLLOWTHROUGH_CONTRACT.json',
        A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json',A/'FEAT335_FLORA_PHYSICAL_INTERFACES_CHECK.json',
        R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',
        *[G/classes[n]['classCandidatePath'] for n in [*class_sources,'Wizard']]]
    bindings=[info(p) for p in paths];checks=[];histories=[];coverage={g['id']:[] for g in read(A/'feat335-nature-source-check-01-verdict/FINITE_NATURE_EXPECTATIONS.json')['groups']}
    group='NWT-01'
    def check(label,value):
        label=group+'/'+label;checks.append({'id':label,'pass':bool(value)});coverage[group].append(label)
        if not value:raise AssertionError(label)
    def reject(label,m,operation):
        before=m.snapshot()
        try:operation()
        except ValueError as e:check(label,True);checks[-1]['reason']=str(e)
        else:check(label,False)
        check(label+'/atomic-no-change',before==m.snapshot())
    def record(label,m):histories.append({'id':group+'/'+label,'final':m.snapshot()})
    def make(*,borrowed=False,first=None,level=None,prepare=True):
        first=first or ('Bard' if borrowed else 'Ranger');level=level or (4 if borrowed else 1)
        actor=deepcopy(template);actor.update(firstClass=first,classLevels={first:1})
        actor['abilityRolls']['WIS']=[1,3,4,4];actor['permanentScores']['WIS']=12
        actor['selectedClassSkills']=['Perception']+[s for s in classes[first]['skillOptions'] if s not in {'Perception','Survival','Reputation','Persuasion','History','Performance'}][:classes[first]['skillChoices']-1]
        actor['classToolChoices']=([k for k,v in equipment.items() if v.get('group')=='Musical Instruments'][:3] if first=='Bard' else [])
        acquired=CompositeCastingHistory(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources)
        if level>1:acquired.advance(level)
        if borrowed:
            lineage=current_lineage({**actor,'ancestryId':actor['ancestry'],'variantId':actor['variant']},ancestry)
            acquired.earn(4);acquired.pay.commit('versatile_mastery',first+':4',prerequisites_met=lineage['lineage']=='Human')
        terrain={key:{'position':pos,'natural':True,'activationPerceived':True,'activationLine':True,'taskPerceived':True,'taskLine':True,'taskAccessible':True,'totalCover':False}
            for key,pos in [('track',5),('far-track',30),('second',10)]}
        base_task={'actualLawfulCheck':True,'skill':'Perception','cell':'track','minimumSeconds':0,'requiresHands':False,'requiresTools':False,'dc':15,
            'advantageSources':[],'disadvantageSources':[],'evidenceState':'established','supportedEvidence':['Observer can identify the recorded bootprint at position5.']}
        signals={k:{'donor':'donor','actorCanProduce':True,'donorCanPerceive':True,'sharedMeaningRecord':'agreed-trail-signal','kind':k,'needsFreeHand':k=='visible'} for k in ['audible','visible']}
        world={'scope':'Explicit synthetic conditional geometry, consent, paid task, source incapacity and perception premises; not authenticated world evidence.',
            'owner':{'position':0,'canAct':True,'conscious':True,'personalRP':class_sources[first]['rpByClassLevel'][level-1],'poolKind':'personal-RP','poolOwner':'owner',
                'silenced':False,'freeHands':2,'hasFocus':False,'magicalTechniqueProhibited':False,'suppressedCards':[],'reactionLegal':True,'usableTaskTools':True},
            'terrain':terrain,'areas':{'site':{'cells':['track']},'other-site':{'cells':['second']}},'tasks':{'look':base_task,'survive':{**deepcopy(base_task),'skill':'Survival'}},
            'signals':signals,'agreedSignals':{'agreed-trail-signal':{'agreedBy':['owner','donor'],'meaning':'Use the taught Nature technique at this natural site.'}},
            'triggerDefinitions':{'footstep':{'perceivable':'Audible actual footstep crossing marked stone.'}},
            'triggerEvents':{'step':{'perceived':True,'actualEvent':True,'kind':'audible-physical-event','matches':'footstep'}},
            'interruptions':{k:{'actualSource':'Conditional actual '+k,'actualTrigger':True,'coversPendingOperation':True,'kind':k} for k in
                ['ordinary-counterspell','rank-limited-spell-dispel','ordinary-damage-only','announced-private-name','incapacitating-condition']}}
        donor={'class':'Ranger','classLevel':1,'selectedCards':selection,'selectedSkills':['Perception','Survival','Nature'],'skillOptions':classes['Ranger']['skillOptions'],
            'position':0,'party':True,'willing':True,'conscious':True,'sharedChannel':True,'perceivesSignal':True,'canHear':True,'canSee':True,
            'suppressed':[],'copiedOrBorrowed':[],'RP':100,'resourcesSpent':0,'ownRechargeHistory':{'sentinel':2}}
        controller=NatureBorrowedTransactions(acquired,supplements['SUP-09'],class_sources,equipment,{'donor':donor},world,allowance) if borrowed else NativeNatureActor(acquired,world)
        m=NatureTransactions(controller,class_sources,authority,native_selection={'selectedAtClassLevel1':selection} if first=='Ranger' else None,
            spell_history={'dissonance':4,'previousSpell':'prior-actual-spell-fixture','refrain':2,'classRecords':{}})
        if borrowed and prepare:
            controller.start_prepare('prepare','donor',NATURE);controller.complete_prepare(60,uninterrupted=True)
        m.begin_turn('turn1','round1',controller.now)
        return m
    def declare(m,event='use',route=None,area='site',signal='audible',**kw):
        return m.declare(event,area,route=route or ('borrowed' if isinstance(m.actor,NatureBorrowedTransactions) else 'native'),signal=signal,expected_version=m.version,**kw)
    def activate(m,event='use',**kw):declare(m,event,**kw);return m.resolve(event)
    def next_turn(m,now=None,identity='turn2',regular=True):
        if m.actor.turn is not None:m.end_turn(m.actor.turn,actual_end=True)
        m.begin_turn(identity,identity+'-round',m.actor.now+6 if now is None else now,regular=regular)
    def task(m,event='look',task_id='look',faces=None):
        m.start_task(event,task_id);p=m.declare_check(event,expected_version=m.version)
        return p,m.resolve_check(event,[2,12] if faces is None else faces)

    m=make();p=declare(m);check('native-level1-nonspell',p['spellRank'] is None and p['components']==[] and m.owner['personalRP']==0 and m.actor.actions==0 and m.actor.cooldowns[NATURE]==3)
    check('native-no-credential-created',not m.acquired.casting.snapshot()['grants']);m.resolve('use');record('native-selected-Ranger1',m)
    m=make(borrowed=True);before=m.acquired.snapshot();activate(m)
    check('borrowed-identity-keeps-acquisition',m.acquired.snapshot()==before and m.acquired.pay.current_classes=={'Bard':4});record('paid-Human-Bard4',m)
    for rank in [0,1]:
        changed=deepcopy(class_sources);next(c for c in changed['Ranger']['cards'] if c['id']==NATURE)['spellRank']=rank
        reject('null-not-rank'+str(rank),m,lambda:NatureTransactions(m.actor,changed,authority))

    group='NWT-02'
    for field,value in [('silenced',True),('freeHands',0),('hasFocus',False)]:
        m=make();m.owner[field]=value;check(field+'-alone-allowed',activate(m)['resolved']);record(field,m)
    for field,value in [('conscious',False),('canAct',False),('magicalTechniqueProhibited',True),('personalRP',0)]:
        m=make();m.owner[field]=value;reject(field,m,lambda:declare(m));record(field,m)
    m=make();m.actor.actions=0;reject('no-required-Action',m,lambda:declare(m))
    m=make();m.actor.world['terrain']['track']['activationPerceived']=False;reject('no-invented-sense',m,lambda:declare(m));record('actual-terrain-perception',m)
    for field in ['requiresHands','requiresTools']:
        m=make();activate(m);next_turn(m);m.actor.world['tasks']['look'][field]=True;m.owner['freeHands']=0;m.owner['usableTaskTools']=False
        reject('later-task-'+field,m,lambda:m.start_task('look','look'));check('rider-retained-'+field,m.rider is not None);record(field,m)

    group='NWT-03'
    m=make(borrowed=True);m.owner['silenced']=True;reject('audible-blocked',m,lambda:declare(m));m.actor.donors['donor']['position']=30
    check('real-visible-signal-at30',declare(m,signal='visible')['provenance']['preparation']['elapsedSeconds']==60);m.resolve('use');record('signal-not-component',m)
    for field,value in [('willing',False),('conscious',False),('party',False),('perceivesSignal',False),('position',31),('suppressed',[NATURE]),('copiedOrBorrowed',[NATURE]),('selectedCards',selection[1:])]:
        m=make(borrowed=True);m.actor.donors['donor'][field]=value;reject('donor-'+field,m,lambda:declare(m));record('donor-'+field,m)
    for label,mutate in [('no-agreed-meaning',lambda m:m.actor.world['agreedSignals'].clear()),('impossible-visible',lambda m:m.owner.update(freeHands=0)),('invented-telepathy',lambda m:m.actor.world['signals']['visible'].update(kind='telepathy'))]:
        m=make(borrowed=True);mutate(m);reject(label,m,lambda:declare(m,signal='visible'));record(label,m)
    m=make(borrowed=True,prepare=False);m.actor.start_prepare('prepare','donor',NATURE)
    reject('full-minute-not59',m,lambda:m.actor.complete_prepare(59,uninterrupted=True));m.actor.donors['donor']['position']=6
    reject('preparation-within5',m,lambda:m.actor.complete_prepare(60,uninterrupted=True));record('full-preparation',m)

    group='NWT-04'
    m=make(borrowed=True);donor=deepcopy(m.actor.donors);declare(m)
    check('Bard4-7-to6-use1-to0-R3',m.owner['personalRP']==6 and m.actor.allowance.use.current==0 and m.actor.cooldowns[NATURE]==3 and m.actor.donors==donor)
    m.resolve('use')
    for i in range(2,5):next_turn(m,identity='turn'+str(i))
    check('readiness-no-RP-or-use-refill',m.actor.cooldowns[NATURE]==0 and m.owner['personalRP']==6 and m.actor.allowance.use.current==0)
    reject('spent-borrowed-use-even-ready',m,lambda:declare(m,'second'));record('own-payment-no-refill',m)
    for field,value in [('poolKind','borrowed-RP'),('poolOwner','donor'),('personalRP',0),('personalRP',8)]:
        m=make(borrowed=True);m.owner[field]=value;reject(field+'-'+str(value),m,lambda:declare(m));record(field+'-'+str(value),m)
    m=make(borrowed=True,first='Warrior');reject('no-class-RP-pool',m,lambda:declare(m));record('Warrior-no-invented-pool',m)
    m=make(borrowed=True);m.actor.cooldowns[NATURE]=2;reject('own-prior-card-recharge',m,lambda:declare(m));record('same-card-ledger',m)

    group='NWT-05'
    m=make(borrowed=True);m.spell_history['dissonance']=20;before=deepcopy(m.spell_history);acq=m.acquired.snapshot();p=declare(m);m.resolve('use')
    check('fractured-history-unchanged',m.spell_history==before and p['paidRP']==1 and m.acquired.snapshot()==acq)
    check('no-invented-spell-fields',all(k not in p for k in ['castingAbility','limit','trauma','rankPrice','performance','crescendo','echoGrant']));record('Bard-no-spell-hook',m)
    m=make(level=4);ranger_engine=next(x for x in class_sources['Ranger']['engine'] if 'single-use/nonstacking' in x and '1 less Dissonance' in x)
    m.spell_history['classRecords']['ranger-stabilization']={'active':True,'deadline':12,'consumed':False,'sourceText':ranger_engine,'premise':'Conditional real direct successful weapon hit before this activation; hit is not simulated.'}
    before=deepcopy(m.spell_history);activate(m);check('source-stabilization-not-consumed-refreshed',m.spell_history==before)
    m.advance(12);check('independent-real-deadline',not m.spell_history['classRecords']['ranger-stabilization']['active'] and not m.spell_history['classRecords']['ranger-stabilization']['consumed']);record('Ranger-existing-stabilization',m)

    group='NWT-06'
    m=make();declare(m);m.owner['canAct']=False;m.interrupt('use','incapacitating-condition')
    check('committed-interrupted-blocks-idle',m.end_turn('turn1',actual_end=True)['after']==4);record('legal-commit-idle',m)
    m=make();m.owner['magicalTechniqueProhibited']=True;reject('illegal-precommit',m,lambda:declare(m))
    check('illegal-does-not-block-idle',m.end_turn('turn1',actual_end=True)['after']==3);reject('no-tick-replay',m,lambda:m.end_turn('turn1',actual_end=True));record('illegal-idle',m)
    m=make();activate(m);next_turn(m);m.owner['magicalTechniqueProhibited']=True;task(m)
    check('ordinary-check-is-not-new-activation',m.end_turn('turn2',actual_end=True)['after']==3)
    m.begin_turn('extra','round2',7,regular=False);check('extra-no-idle-tick',m.end_turn('extra',actual_end=True)['after']==3);record('later-task-and-extra-turn',m)

    group='NWT-07'
    m=make(borrowed=True);p=declare(m);check('paid-before-result',m.actor.pending==p and m.rider is None and 'result' not in m.actor.events['use'] and 'faces' not in p)
    reject('cannot-bank-pending',m,lambda:m.begin_turn('next','round2',66));reject('damage-no-concentration',m,lambda:m.interrupt('use','ordinary-damage-only'))
    check('capable-damaged-actor-resolves',m.resolve('use')['resolved']);record('split-paid-pending',m)
    m=make();declare(m);m.owner['canAct']=False;m.interrupt('use','incapacitating-condition')
    check('actual-incapacity-no-refund',m.rider is None and m.owner['personalRP']==0 and m.actor.cooldowns[NATURE]==3);reject('interrupted-no-replay',m,lambda:m.resolve('use'));record('source-incapacity',m)
    for label,mutate in [('actor-moved',lambda m:m.owner.update(position=21)),('terrain-moved',lambda m:m.actor.world['terrain']['track'].update(position=6))]:
        m=make();declare(m);mutate(m);check(label+'-fails-paid',not m.resolve('use')['resolved'] and m.owner['personalRP']==0 and m.rider is None);record(label,m)
    m=make(borrowed=True);declare(m);m.actor.donors['donor'].update(position=100,willing=False)
    check('donor-no-postcommit-tether',m.resolve('use')['resolved']);record('donor-leaves-after-commit',m)

    group='NWT-08'
    m=make();before=deepcopy(m.spell_history);m.ready_setup('ready','native','footstep')
    check('setup-Action-only',m.actor.actions==0 and m.owner['personalRP']==1 and not m.actor.cooldowns and m.rider is None and m.spell_history==before)
    m.end_turn('turn1',actual_end=True);check('setup-quiet-turn',m.spell_history['dissonance']==3);m.advance(5);p=declare(m,ready_trigger='step')
    check('Reaction-release-no-second-Action',p['actionCost']=='reaction' and m.reactions==0 and m.actor.actions==0 and m.owner['personalRP']==0)
    check('resolution-deadline65',m.resolve('use')['deadline']==65 and m.spell_history['dissonance']==3);record('nonspell-ready-offturn',m)
    m=make(borrowed=True);m.ready_setup('ready','borrowed','footstep');m.end_turn('turn1',actual_end=True);m.advance(65)
    m.owner['reactionLegal']=False;reject('prohibited-release',m,lambda:declare(m,ready_trigger='step'));m.owner['reactionLegal']=True
    m.actor.world['triggerEvents']['step']['kind']='private-ability-name';reject('private-name-not-trigger',m,lambda:declare(m,ready_trigger='step'))
    m.actor.world['triggerEvents']['step']['kind']='audible-physical-event';declare(m,ready_trigger='step');m.owner['canAct']=False;m.interrupt('use','incapacitating-condition')
    check('borrowed-released-interrupt-retains-costs',m.actor.allowance.use.current==0 and m.owner['personalRP']==6 and m.rider is None);record('Ready-borrowed-interrupted',m)
    m=make();m.ready_setup('ready','native','footstep');m.advance(5)
    check('declined-trigger-no-release',m.ready is not None and m.owner['personalRP']==1 and not m.actor.cooldowns)
    next_turn(m,6);check('next-regular-expires-setup-only',m.ready is None and m.owner['personalRP']==1 and not m.actor.cooldowns);record('Ready-declined-expiry',m)
    m=make();m.ready_setup('ready','native','footstep');next_turn(m,1,'extra',False);m.ready_setup('replacement','native','footstep')
    check('replacement-costs-setup-only',m.actor.events['ready']['status']=='ready-replaced' and m.actor.actions==0 and m.owner['personalRP']==1 and not m.actor.cooldowns);record('Ready-replacement',m)

    group='NWT-09'
    m=make();declare(m)
    for kind in ['ordinary-counterspell','rank-limited-spell-dispel','announced-private-name']:reject(kind,m,lambda kind=kind:m.interrupt('use',kind))
    m.owner['canAct']=False;m.interrupt('use','incapacitating-condition');check('actual-covering-incapacity',m.actor.events['use']['status']=='interrupted-no-refund');record('real-interrupt-only',m)

    group='NWT-10'
    m=make();activate(m);next_turn(m);m.owner['position']=20;p,result=task(m)
    check('fixed-evidence5-owner20-distance15',result['total']==15 and result['success']);record('edge15-valid',m)
    for label,mutate in [('distance16',lambda m:m.owner.update(position=21)),('new-terrain-not-fixed',lambda m:(m.owner.update(position=20),m.actor.world['tasks']['look'].update(cell='far-track'))),
        ('lost-task-sense',lambda m:m.actor.world['terrain']['track'].update(taskPerceived=False)),('lost-task-line',lambda m:m.actor.world['terrain']['track'].update(taskLine=False)),
        ('lost-access',lambda m:m.actor.world['terrain']['track'].update(taskAccessible=False)),('not-natural-anymore',lambda m:m.actor.world['terrain']['track'].update(natural=False))]:
        m=make();activate(m);next_turn(m);m.start_task('look','look');mutate(m);reject(label,m,lambda:m.declare_check('look',expected_version=m.version));check(label+'-keeps-rider',m.rider is not None);record(label,m)
    m=make();m.actor.world['terrain']['track']['natural']=False;reject('no-natural-terrain',m,lambda:declare(m));record('actual-terrain',m)
    m=make();m.actor.world['tasks']['look'].update(evidenceState='unknown',supportedEvidence=[]);p=declare(m)
    check('activation-no-clue-presence-oracle','evidence' not in p and m.resolve('use')['resolved']);record('legitimate-site-unknown',m)

    group='NWT-11'
    m=make(borrowed=True);declare(m);m.advance(61);check('resolution61-deadline121',m.resolve('use')['deadline']==121)
    next_turn(m,110);m.start_task('long','look');m.advance(120);m.declare_check('long',expected_version=m.version);m.resolve_check('long',[2,12]);check('120-valid',m.rider is None);record('strict-before-deadline',m)
    for now in [121,130]:
        m=make(borrowed=True);declare(m);m.advance(61);m.resolve('use');next_turn(m,110);m.start_task('long','look');m.advance(now)
        reject('adjudicate-'+str(now),m,lambda:m.declare_check('long',expected_version=m.version));check('absolute-expiry-'+str(now),m.rider is None and m.rider_history[-1]['deadline']==121);record('deadline-'+str(now),m)
    m=make(borrowed=True);activate(m);next_turn(m,66);deadline=m.rider['deadline'];m.actor.rest('nonbeneficial',kind='SR',beneficial=False);m.actor.donors['donor']['position']=100
    check('ending-preparation-no-new-clock',m.actor.prepared is None and m.rider['deadline']==deadline);m.advance(70,outside_initiative=True);task(m);record('rest-label-and-donor-departure',m)

    group='NWT-12'
    m=make();activate(m);reject('no-free-Search',m,lambda:m.start_task('look','look'));next_turn(m);m.start_task('look','look');p=m.declare_check('look',expected_version=m.version)
    check('rider-spent-before-faces',m.rider is None and p['consumedBeforeFaces'] and 'faces' not in p and 'result' not in m.actor.events['look'])
    result=m.resolve_check('look',[1,2]);check('failure-still-consumed',not result['success'] and m.rider is None)
    next_turn(m,12,'turn3');m.start_task('retry','look');reject('ordinary-retry-not-second-rider',m,lambda:m.declare_check('retry',expected_version=m.version));record('task-cost-and-failure',m)
    m=make();activate(m);next_turn(m);m.start_task('look','look');m.declare_check('look',expected_version=m.version);m.owner['canAct']=False;m.interrupt('look','incapacitating-condition')
    check('check-interruption-stays-consumed',m.rider is None and m.tasks['look']['state']=='interrupted-no-refund');record('interrupt-after-check-commit',m)

    group='NWT-13'
    for skill,expected,success in [('look',15,True),('survive',13,False)]:
        m=make(borrowed=True);activate(m);next_turn(m);p,result=task(m,task_id=skill)
        check('own-modifier-'+skill,p['modifier']==(3 if skill=='look' else 1) and result['total']==expected and result['success']==success);record('trained-v-untrained-'+skill,m)
    m=make();activate(m);next_turn(m);m.actor.world['tasks']['look']['disadvantageSources']=['conditional actual obscured-detail task'];m.start_task('look','look');p=m.declare_check('look',expected_version=m.version)
    check('real-disadvantage-cancels',p['mode']=='normal' and m.rider is None);reject('not-always-max-two',m,lambda:m.resolve_check('look',[2,12]));result=m.resolve_check('look',[2])
    check('single-face-cancelled-result',result['total']==5 and not result['success']);record('ordinary-cancellation',m)
    m=make();activate(m);next_turn(m);m.actor.world['tasks']['look']['advantageSources']=['conditional separate actual advantage'];p,result=task(m)
    check('redundant-advantage-consumes',m.rider is None and p['mode']=='advantage' and result['total']==15 and result['passiveBonus']==0)
    reject('resolved-check-cannot-get-new-Nature-roll',m,lambda:m.resolve_check('look',[20,20]));record('no-stack-or-repeat',m)

    group='NWT-14'
    for state,evidence,expected in [('established',['Recorded location, without sight of the hidden creature.'],['Recorded location, without sight of the hidden creature.']),
        ('established',['Source-supported search found no identifiable tracks in this cell.'],['Source-supported search found no identifiable tracks in this cell.']),('unknown',[],[])]:
        m=make();activate(m);next_turn(m);m.actor.world['tasks']['look'].update(evidenceState=state,supportedEvidence=evidence);p,result=task(m)
        check(state+'-supported-evidence',result['revealedEvidence']==expected and result['unknownDataDoesNotProveAbsence'] and not result['grantsSight']);record(state+'-'+str(len(evidence)),m)
    m=make();activate(m);next_turn(m);m.start_task('look','look');m.actor.world['terrain']['track']['totalCover']=True
    reject('total-cover-not-new-sense',m,lambda:m.declare_check('look',expected_version=m.version));record('no-through-cover',m)

    group='NWT-15'
    m=make(borrowed=True,first='Ranger');activate(m,route='native');first_rider=deepcopy(m.rider)
    next_turn(m,61,'extra',False);check('extra-no-recharge',m.actor.cooldowns[NATURE]==3)
    for i,remaining in [(2,2),(3,1),(4,0)]:
        next_turn(m,60+6*(i-1),'turn'+str(i));check('regular-start-'+str(i),m.actor.cooldowns[NATURE]==remaining)
    declare(m,'borrowed-new',route='borrowed',area='other-site');m.resolve('borrowed-new')
    check('native-borrowed-one-rider-new-area',m.rider['activation']=='borrowed-new' and m.rider['area']=='other-site' and m.rider_history[-1]['activation']==first_rider['activation'] and m.rider_history[-1]['state']=='replaced')
    check('same-ledger-reset-on-borrowed',m.actor.cooldowns[NATURE]==3 and m.owner['personalRP']==2 and m.actor.allowance.use.current==0);record('shared-native-borrowed-clock-and-rider',m)
    m=make(level=4);activate(m);m.end_turn('turn1',actual_end=True);m.advance(6,outside_initiative=True);check('outside-first6sec',m.actor.cooldowns[NATURE]==2)
    m.begin_turn('entry','round2',6);check('no-double-tick-on-entry',m.actor.cooldowns[NATURE]==2);m.end_turn('entry',actual_end=True);m.advance(18,outside_initiative=True)
    check('outside-total18-ready',m.actor.cooldowns[NATURE]==0);record('elapsed-initiative-boundary',m)
    for outcome in ['failed','interrupted']:
        m=make(level=4);activate(m);old=deepcopy(m.rider)
        for i in range(2,5):next_turn(m,identity='turn'+str(i))
        declare(m,'later');m.owner['canAct']=False
        if outcome=='failed':m.resolve('later')
        else:m.interrupt('later','incapacitating-condition')
        check(outcome+'-new-preserves-old',m.rider==old and m.owner['personalRP']==2 and m.actor.cooldowns[NATURE]==3);record('preserved-old-'+outcome,m)

    group='NWT-16'
    check('source-propagation-evidence-separate',read(A/'FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json')['checks']==137 and read(A/'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json')['checks']==124)
    m=make(borrowed=True);reject('historical-clearance-entry-disabled',m,lambda:m.actor.nature_whisper('legacy'))
    check('old-clearance-not-admission', 'actualMinorWeaveClearance' not in m.owner);record('new-descendant-only',m)
    prior=read(A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json');check('362-and38-historical',prior['checks']==362 and len(prior['histories'])==38)
    check('all-input-bytes-unchanged',bindings==[info(p) for p in paths])
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],'sourceBindings':bindings,'results':checks,'histories':histories,
        'counts':{'conditionalHistories':len(histories),'expectationGroupsTouched':len([v for v in coverage.values() if v]),'authoredGroups':16,'authoredVariants':47},'groupEvidence':coverage,
        'scope':'Current exact Nature source, real paid class/feat selection slices, native Ranger1 and borrowed Bard4 payment, physical signals, split activation/check transactions, fixed terrain, absolute minute, actual own skill math, nonspell Ready, idle/recharge chronology and replacement-rider rules in conditional world histories.',
        'unfulfilledAcceptanceDetails':[
            {'group':'NWT-05','variant':1,'remaining':'History preservation executes, but the next actual same-named paid ordinary spell and its complete class-cadence integration are not executed by this Nature-only service.'},
            {'group':'NWT-13','variant':3,'remaining':'No duplicate Nature reroll is allowed; passive bonus stays0. A genuinely permitted external replacement roll before consequences, bound to an actual acquired source and the original check lineage, still needs integration.'}],
        'limits':['World geometry, consent, timing, lawful-task DC, source interruption and existing-class-record premises are explicitly conditional and are not authenticated campaign facts.',
            'Only actual first-class native Ranger and acquired Human Versatile Mastery slices are supported; multiclass RP ownership, complete native card trees and all other actor providers remain outside this service.',
            'Interrupt positives use actual conditional source incapacity, not a general reaction/counter/suppression engine. Native component absence is no permission to ignore an actual covering prohibition.',
            'Own trained/untrained WIS cases execute; other independently acquired Expertise and ability-substitution providers have not been independently earned and exercised here.',
            'Recharge executes finite regular/extra/outside6second boundaries including duplicate entry at one timestamp; full absent/dead/resumed/virtual scheduler authority is not simulated.',
            'Rest labels exercise existing borrower preparation ending and no minute reset; full labor/safety/rest engine is not executed. No free spell casting or source roll is inferred.',
            'Source propagation124/137 and historical borrowed362/38 evidence are separate preserved receipts. No full335, class balance, human playtest, runtime or whole-game approval follows.'],
        'newRules':0,'natureAll47VariantsFulfilled':False,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output),'openAcceptanceDetails':len(report['unfulfilledAcceptanceDetails'])}))


if __name__=='__main__':main()
