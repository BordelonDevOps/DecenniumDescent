"""One-use paid-source and conditional transaction checks for all12 borrowed cards."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json
from feat335_borrowed_skill_transactions import BorrowedSkillTransactions as BorrowedStunts
from feat_exact_01_composite_casting_model import CompositeCastingHistory
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_lineage_prerequisite_model import current_lineage
from validate_feat_exact_01_composite_casting import read,info,serial

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def main():
    output=A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json';assert not output.exists()
    foundation=read(R/'data/playtest/character_foundation.json');classes={x['class']:x for x in foundation['classes']}
    skills={s:a for a,names in foundation['skillAbilities'].items() for s in names}
    ancestry=read(R/'data/playtest/ancestry_background_candidate.json');backgrounds={x['id']:x for x in ancestry['backgrounds']}
    equipment={x['id']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records']}
    supplements={x['id']:x['value'] for x in read(R/'data/public/feat_candidates/exact_01/supplements.json')['groups']}
    contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
    class_sources={n:read(G/classes[n]['classCandidatePath']) for n in ['Soldier','Warrior','Ranger','Thief','Monk','Bard']}
    wizard=read(R/'data/public/class_playtests/wizard.json')
    sources=CastingSources(G,read(R/'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells'],supplements,wizard)
    template=read(A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json')['actorSourceProjection']
    menu=supplements['SUP-09'];descriptors=read(A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json')
    allowance=next(x for x in descriptors['entries'] if x['id']=='versatile_mastery')['finiteAllowances'][0]
    source_paths=[Path(__file__),R/'tools/feat335_borrowed_skill_transactions.py',R/'tools/feat335_borrowed_transactions.py',R/'tools/feat335_borrowed_stunts.py',R/'tools/feat335_allowance_bindings.py',
        R/'tools/feat_exact_01_composite_casting_model.py',R/'tools/feat_exact_01_lineage_prerequisite_model.py',R/'tools/feat_exact_01_acquisition_models.py',
        R/'tools/feat_exact_01_training_prerequisite_model.py',R/'tools/feat_exact_01_casting_credential_model.py',
        R/'tools/core_playtest_rules.py',R/'tools/combat_playtest_rules.py',R/'data/playtest/character_foundation.json',
        R/'data/playtest/ancestry_background_candidate.json',R/'data/playtest/equipment_source_catalog.json',
        R/'data/public/feat_candidates/exact_01/supplements.json',R/'data/public/feat_candidates/exact_01/shared_rules.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json',A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json',
        R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
        *[G/classes[n]['classCandidatePath'] for n in [*class_sources,'Wizard']]]
    bindings=[info(p) for p in source_paths];checks=[];histories=[]
    def check(label,value):
        checks.append({'id':label,'pass':bool(value)})
        if not value:raise AssertionError(label)
    def reject(label,m,operation):
        before=m.snapshot()
        try:operation()
        except ValueError as e:checks.append({'id':label,'pass':True,'reason':str(e)})
        else:check(label,False)
        check(label+'/no-spend-or-mutation',before==m.snapshot())
    def record(label,m):histories.append({'id':label,'final':m.snapshot()})
    def make(row,first='Warrior'):
        actor=deepcopy(template);actor.update(firstClass=first,classLevels={first:1})
        if first=='Bard':
            actor['selectedClassSkills']=[s for s in classes[first]['skillOptions'] if s not in {'Reputation','Persuasion','History','Performance'}][:classes[first]['skillChoices']]
            actor['classToolChoices']=[k for k,v in equipment.items() if v.get('group')=='Musical Instruments'][:3]
        acquired=CompositeCastingHistory(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources)
        lineage_actor={**actor,'ancestryId':actor['ancestry'],'variantId':actor['variant']};lineage=current_lineage(lineage_actor,ancestry)
        check('human-printed-predicate/'+row['sourceId']+'/'+first,contracts['versatile_mastery']['requirements']=={'kind':'actualLineageReceipt','lineage':'Human','noSilentAlias':True} and lineage['lineage']=='Human')
        acquired.advance(4);acquired.earn(4);acquired.pay.commit('versatile_mastery',first+':4',prerequisites_met=lineage['lineage']=='Human')
        klass=row['actualSourceClass'];cs=class_sources[klass];cards=[c for c in cs['cards'] if c['band']=='Base' and c['minimumClassLevel']<=1 and c['acquisition']=='selection']
        selected=[row['sourceId']]+[c['id'] for c in sorted(cards,key=lambda c:c['sourceKind']!='active') if c['id']!=row['sourceId']][:3]
        donor={'class':klass,'classLevel':1,'selectedCards':selected,'selectedSkills':classes[klass]['skillOptions'][:classes[klass]['skillChoices']],
            'skillOptions':classes[klass]['skillOptions'],'position':0,'party':True,'willing':True,'conscious':True,'sharedChannel':True,'perceivesSignal':True,
            'suppressed':[],'copiedOrBorrowed':[],'RP':100,'resourcesSpent':0,'ownRechargeHistory':{'sentinel':2}}
        check('actual-source-class-selection/'+row['sourceId'],len(selected)==4 and len(donor['selectedSkills'])==classes[klass]['skillChoices'])
        world={'owner':{'position':0,'usableSpeed':30,'restrained':False,'coverOrConcealment':True,'canAct':True,'ordinaryMovementSpent':10,
            'usableThievesTools':True,'actualTurnEnd':66,'personalRP':class_sources[first]['rpByClassLevel'][3],
            'sourceQualifiedPersonalRPPool':class_sources[first]['rpByClassLevel'][3]>0,'actualMinorWeaveClearance':True},
            'targets':{'enemy':{'position':5,'ac':15,'conSave':0,'passiveInsight':15,'enemy':True,'perceivedBothWays':True},
                'enemy2':{'position':5,'ac':15,'conSave':2,'passiveInsight':12,'enemy':True,'perceivedBothWays':True}},
            'items':{name:{'profile':profile,'heldBy':'owner','ammunition':3} for name,profile in [('sword','martial-melee-weapons.longsword'),
                ('left','martial-melee-weapons.shortsword'),('right','martial-melee-weapons.shortsword'),('bow','martial-ranged-weapons.longbow'),('body','simple-melee-weapons.unarmed-strike')]},
            'mechanisms':{'trap':{'magical':False,'accessibleInReach':True,'dc':None,'complex':False,'disarmed':False,'triggered':False}}}
        return BorrowedStunts(acquired,menu,class_sources,equipment,{'donor':donor},world,allowance)
    def prepare(m,row):
        m.start_prepare('prep','donor',row['sourceId']);m.complete_prepare(60,uninterrupted=True);m.begin_turn('owner:regular:1','round1',60)
    def attack(item,target='enemy',face=12,damage=None,ability='STR'):
        return {'item':item,'target':target,'natural':face,'damageFaces':damage if damage is not None else [4],
            'ability':ability,'legalBodyRangeLineTarget':True}
    def route(**changes):
        base={'from':0,'to':10,'terrain':'normal','routeLegal':True,'hostileOccupied':False,'occupiedEndpoint':False,'canConceal':True};base.update(changes);return [base]
    check('complete-twelve-distinct-cards',len(menu)==len({r['sourceId'] for r in menu})==12)
    for row in menu:
        sid=row['sourceId'];kind=sid.rsplit('.',1)[-1];m=make(row,'Bard' if kind=='nature-s-whisper' else 'Warrior')
        before=m.snapshot();prepare(m,row)
        check(sid+'/preparation-no-use-or-resource-spend',m.allowance.use.current==1 and m.world['owner']['personalRP']==before['world']['owner']['personalRP'])
        donor_before=deepcopy(m.donors)
        if kind in {'tactical-reposition','skirmisher-s-step','cunning-movement','shadow-step'}:
            result=m.move('use',route(hostileOccupied=kind=='cunning-movement'))
            check(sid+'/separate-movement-budget',m.world['owner']['position']==10 and result['ordinaryMovementSpent']==10 and result['movementCost']==10)
            check(sid+'/exact-OA-and-visibility',result['opportunityAttacksApply']==(kind=='shadow-step') and not result['teleport'] and not result['invisibility'])
            if kind=='shadow-step':
                result=m.hide_after_shadow('hide','use',15,15);check(sid+'/actual-Hide',result['success'])
                reject(sid+'/no-second-Hide',m,lambda:m.hide_after_shadow('again','use',15,15))
        elif kind in {'covering-fire','quick-shot','brutal-strike','twin-strike','flurry-of-blows'}:
            args={}
            if kind in {'covering-fire','quick-shot'}:attacks=[attack('bow',ability='DEX')];args={'cover_deadline':72}
            elif kind=='brutal-strike':attacks=[attack('sword',face=20,damage=[2,7])];args={'extra_die':[2,5],'con_save':1,'stagger_deadline':78}
            elif kind=='twin-strike':attacks=[attack('left',face=1),attack('right','enemy2',damage=[5])]
            else:attacks=[attack('body',damage=[]),attack('body','enemy2',damage=[])]
            result=m.attacks('use',attacks,**args);out=result['attacks']
            check(sid+'/exact-count-and-no-borrowed-engine',len(out)==len(attacks) and result['extraAttacksGranted']==result['borrowedEngineResourcesGenerated']==0)
            if kind=='quick-shot':check(sid+'/no-ability-damage',out[0]['nativeDamage']==4 and m.world['items']['bow']['ammunition']==2)
            if kind=='covering-fire':check(sid+'/normal-attack-and-rider',out[0]['nativeDamage']==7 and m.riders[0]['nextAttackAgainstOtherAlly']==-2)
            if kind=='brutal-strike':check(sid+'/critical-own-dice-fixedS1',out[0]['nativeDamage']==19 and len(m.riders)==1 and m.riders[0]['deadline']==78)
            if kind=='twin-strike':check(sid+'/modifier-on-first-success',out[0]['nativeDamage']==0 and out[1]['nativeDamage']==8)
            if kind=='flurry-of-blows':check(sid+'/own-untrained-unarmed',all(x['nativeDamage']==4 and x['total']==15 for x in out))
        elif kind=='disable-device':
            result=m.task('use',12,mechanism='trap');check(sid+'/actual-source-tool-check',result['success'] and result['disarmed'] and not result['triggered'])
        elif kind=='feint':
            result=m.task('use',12,target='enemy',ability='CHA');check(sid+'/actual-task-and-own-turn-rider',result['success'] and m.riders[0]['turn']=='owner:regular:1' and m.riders[0]['deadline']==66)
        else:
            rp=m.world['owner']['personalRP'];result=m.nature_whisper('use');check(sid+'/actual-personal-RP',m.world['owner']['personalRP']==rp-1 and not result['checkGranted'])
            reject(sid+'/no-second-free-Action',m,lambda:m.use_nature_advantage('look','Survival',[2,18],15,distance=10,natural_terrain=True,total_cover=False,evidence=['actual footprint'],actual_check_action=True))
            m.begin_turn('owner:regular:2','round2',66)
            result=m.use_nature_advantage('look','Survival',[2,18],15,distance=10,natural_terrain=True,total_cover=False,evidence=['actual footprint'],actual_check_action=True)
            check(sid+'/real-check-real-evidence',result['success'] and result['revealedEvidence']==['actual footprint'])
            reject(sid+'/one-check-only',m,lambda:m.use_nature_advantage('twice','Survival',[2,18],15,distance=10,natural_terrain=True,total_cover=False,evidence=['invented'],actual_check_action=True))
        check(sid+'/own-use-donor-unchanged',m.allowance.use.current==0 and m.donors==donor_before)
        reject(sid+'/failed-or-successful-use-no-repeat',m,lambda:m.preflight('second','card'))
        record(sid,m)
    bykind={r['sourceId'].rsplit('.',1)[-1]:r for r in menu}
    row=bykind['tactical-reposition'];m=make(row);m.start_prepare('prep','donor',row['sourceId'])
    reject('less-than-minute',m,lambda:m.complete_prepare(59,uninterrupted=True))
    check('interrupted-work-no-preparation',not m.complete_prepare(30,uninterrupted=False) and m.prepared is None and m.allowance.use.current==1)
    m.start_prepare('fresh','donor',row['sourceId']);m.complete_prepare(90,uninterrupted=True);m.begin_turn('turn','r',90)
    for field,value in [('willing',False),('conscious',False),('perceivesSignal',False),('position',31),('suppressed',[row['sourceId']]),('copiedOrBorrowed',[row['sourceId']])]:
        old=deepcopy(m.donors['donor'][field]);m.donors['donor'][field]=value
        reject('donor/'+field,m,lambda:m.move('use',route()));m.donors['donor'][field]=old
    for label,changes in [('terrain-overbudget',{'terrain':'difficult'}),('blocked-route',{'routeLegal':False}),('hostile-path',{'hostileOccupied':True}),('occupied-end',{'occupiedEndpoint':True})]:
        reject(label,m,lambda changes=changes:m.move('use',route(**changes)))
    m.world['owner']['restrained']=True;reject('no-restraint-escape',m,lambda:m.move('use',route()));m.world['owner']['restrained']=False
    m.cooldowns[row['sourceId']]=2;reject('actual-same-card-cooldown-not-bypassed',m,lambda:m.move('use',route()))
    m.begin_turn('extra','r',91,regular=False);check('extra-turn-no-recharge-tick',m.cooldowns[row['sourceId']]==2)
    m.begin_turn('next-regular','r2',96);check('real-regular-ticks-once',m.cooldowns[row['sourceId']]==1)
    m.begin_turn('next-regular2','r3',102);m.move('use',route());check('eventual-legal-use',m.allowance.use.current==0)
    check('debt-rest-does-not-refill',not m.rest('debt',kind='SR',beneficial=False) and m.prepared is None and m.allowance.use.current==0)
    check('beneficial-owner-rest-refills-once',m.rest('realSR',kind='SR',beneficial=True) and m.allowance.use.current==1)
    check('same-rest-relabel-not-second-reset',not m.rest('realSR',kind='LR',beneficial=True))
    record('preparation-donor-physics-shared-clock',m)
    row=bykind['nature-s-whisper'];m=make(row);prepare(m,row);reject('Warrior-has-no-RP-to-borrow',m,lambda:m.nature_whisper('use'));record('no-invented-RP',m)
    row=bykind['disable-device']
    for face,dc,trigger in [(1,15,True),(9,15,False),(20,50,True)]:
        m=make(row);prepare(m,row);m.world['mechanisms']['trap']['dc']=dc;result=m.task('use',face,mechanism='trap')
        check('disarm-numeric-failure-margin/'+str(face),result['triggered']==trigger and m.allowance.use.current==0)
        record('disarm/'+str(face),m)
    row=bykind['quick-shot'];m=make(row);prepare(m,row);m.card_rest_spent.add(row['sourceId']);reject('known-QuickShot-spent-natural-rest-use',m,lambda:m.attacks('use',[attack('bow',ability='DEX')]));record('shared-natural-per-rest-entitlement',m)
    row=bykind['tactical-reposition'];m=make(row);skill=m.donors['donor']['selectedSkills'][0]
    m.start_prepare('skill-prep','donor',skill);m.complete_prepare(60,uninterrupted=True);m.begin_turn('skill-turn','round1',60)
    result=m.borrowed_skill('skill',skill,10,skills[skill],15,actual_check_action=True)
    check('borrowed-class-skill-own-ability-normalPB',result['total']==15 and m.allowance.use.current==0 and m.donors['donor']['resourcesSpent']==0);record('skill-alternative',m)
    for kind in ['covering-fire','quick-shot','brutal-strike','twin-strike','flurry-of-blows']:
        row=bykind[kind];m=make(row);prepare(m,row)
        item='bow' if kind in {'covering-fire','quick-shot'} else 'body' if kind=='flurry-of-blows' else 'left' if kind=='twin-strike' else 'sword'
        ds=[{'item':item,'target':'enemy','ability':'DEX' if item=='bow' else 'STR','legalBodyRangeLineTarget':True}]
        if kind in {'twin-strike','flurry-of-blows'}:ds.append({**ds[0],'item':'right' if kind=='twin-strike' else 'body','target':'enemy2'})
        paid=m.declare_attacks('pending',ds,cover_deadline=72,stagger_deadline=78)
        check(kind+'/declaration-has-no-rolls-or-outcome',m.allowance.use.current==0 and 'result' not in m.events['pending'] and all('natural' not in x and 'damageFaces' not in x for x in paid['declarations']))
        check(kind+'/ordinary-action-paid-before-resolution',(m.bonus_actions==0 if kind=='quick-shot' else m.actions==0))
        if item=='bow':check(kind+'/ammo-paid-before-resolution',m.world['items'][item]['ammunition']==2)
        reject(kind+'/cannot-bank-pending-action',m,lambda:m.begin_turn('extra','round1',61,regular=False))
        reject(kind+'/invalid-result-keeps-committed-state',m,lambda:m.resolve_attacks('pending',[]))
        m.interrupt('pending',actual_authorized_interrupt=True)
        check(kind+'/interrupt-no-resource-refund',m.pending is None and m.allowance.use.current==0 and m.events['pending']['status']=='interrupted-no-refund')
        reject(kind+'/interrupted-use-cannot-resolve',m,lambda:m.resolve_attacks('pending',[]))
        record('declared-and-interrupted/'+kind,m)
    for kind in ['feint','disable-device']:
        row=bykind[kind];m=make(row);prepare(m,row)
        m.declare_task('paid-task',target='enemy' if kind=='feint' else None,mechanism='trap' if kind=='disable-device' else None)
        check(kind+'/task-paid-before-natural-known',m.allowance.use.current==0 and 'natural' not in m.pending and 'result' not in m.events['paid-task'])
        result=m.resolve_task('paid-task',1)
        check(kind+'/failed-roll-does-not-refund',not result['success'] and m.allowance.use.current==0)
        record('explicit-task/'+kind,m)
    row=bykind['feint'];m=make(row);prepare(m,row);m.task('feint',12,target='enemy')
    check('feint-no-consumption-other-target',not m.claim_next_attack_riders('other',attacker='owner',target='enemy2',weapon_attack=True,actual_legal_attack=True)['advantage'] and len(m.riders)==1)
    check('feint-no-consumption-nonweapon',not m.claim_next_attack_riders('spell',attacker='owner',target='enemy',weapon_attack=False,actual_legal_attack=True)['advantage'] and len(m.riders)==1)
    claimed=m.claim_next_attack_riders('real-weapon',attacker='owner',target='enemy',weapon_attack=True,actual_legal_attack=True)
    check('feint-consumed-before-hit-or-miss',claimed['advantage'] and claimed['consumedBeforeHitResult'] and not m.riders and not claimed['newAttackGranted'])
    reject('same-attack-no-second-claim',m,lambda:m.claim_next_attack_riders('real-weapon',attacker='owner',target='enemy',weapon_attack=True,actual_legal_attack=True))
    check('next-distinct-attack-no-feint',not m.claim_next_attack_riders('after-miss',attacker='owner',target='enemy',weapon_attack=True,actual_legal_attack=True)['advantage']);record('Feint-later-attack-consumption',m)
    row=bykind['covering-fire'];m=make(row);prepare(m,row);m.attacks('cover',[attack('bow',ability='DEX')],cover_deadline=72)
    check('cover-does-not-penalize-attack-on-owner',m.claim_next_attack_riders('at-owner',attacker='enemy',target='owner',weapon_attack=True,actual_legal_attack=True)['attackModifier']==0 and len(m.riders)==1)
    m.riders.append({**deepcopy(m.riders[0]),'source':'conditional-second-owner-covering-source'})
    claimed=m.claim_next_attack_riders('at-other-ally',attacker='enemy',target='ally',weapon_attack=False,actual_legal_attack=True,target_is_other_ally=True)
    check('cover-one-penalty-consumes-all-applicable-sources',claimed['attackModifier']==-2 and len(claimed['consumedSources'])==2 and not m.riders)
    record('Covering-Fire-nonstacking-and-consumption',m)
    row=bykind['shadow-step'];m=make(row);prepare(m,row);m.move('shadow',route());m.begin_turn('later','round2',66)
    reject('Shadow-Hide-cannot-be-banked-across-turn',m,lambda:m.hide_after_shadow('late-hide','shadow',20,15));record('Shadow-immediate-window',m)
    def skill_setup(which='Athletics'):
        row=bykind['tactical-reposition'];m=make(row)
        assert which in m.donors['donor']['selectedSkills']
        m.start_prepare('skill-prep','donor',which);m.complete_prepare(60,uninterrupted=True);m.begin_turn('skill-turn','skill-round',60)
        return m,{'skill':which,'ability':skills[which],'dc':15,'actualCheckAction':True}
    for skill in ['Athletics','Intimidation']:
        for natural in [1,9,10,20]:
            m,declaration=skill_setup(skill);donor_before=deepcopy(m.donors);training_before=deepcopy(m.acquired.training_projection)
            paid=m.declare_skill('declared-skill',declaration)
            check(skill+str(natural)+'/payment-with-no-known-die',m.allowance.use.current==0 and m.actions==0 and 'natural' not in paid and 'result' not in m.events['declared-skill'])
            check(skill+str(natural)+'/own-stat-and-normalPB',paid['modifier']==m.mod(skills[skill])+m.proficiency() and paid['borrowedTrainingFactor']==1 and paid['ownTrainingFactor']==(1 if skill=='Athletics' else 0))
            reject(skill+str(natural)+'/bad-result-no-refund',m,lambda:m.resolve_skill('declared-skill',21))
            result=m.resolve_skill('declared-skill',natural)
            check(skill+str(natural)+'/actual-Core-total-and-success',result['total']==natural+paid['modifier'] and result['success']==(natural>=10))
            check(skill+str(natural)+'/donor-and-permanent-training-unchanged',m.donors==donor_before and m.acquired.training_projection==training_before and m.allowance.use.current==0)
            reject(skill+str(natural)+'/cannot-repeat-paid-outcome',m,lambda:m.resolve_skill('declared-skill',20))
            record('explicit-class-skill/'+skill+'/'+str(natural),m)
    m,declaration=skill_setup('Intimidation')
    for label,change in [('known-die',{'natural':20}),('known-outcome',{'success':True}),('wrong-skill',{'skill':'Athletics'}),('unsupported-ability',{'ability':'STR'}),('not-actual-task',{'actualCheckAction':False}),('bad-DC',{'dc':-1})]:
        reject('skill-precommit/'+label,m,lambda change=change:m.declare_skill('attempt',{**declaration,**change}))
    for field,value in [('conscious',False),('willing',False),('perceivesSignal',False),('position',31),('suppressed',['Intimidation']),('copiedOrBorrowed',['Intimidation'])]:
        old=deepcopy(m.donors['donor'][field]);m.donors['donor'][field]=value
        reject('skill-precommit/donor-'+field,m,lambda:m.declare_skill('attempt',declaration));m.donors['donor'][field]=old
    m.actions=0;reject('skill-precommit/no-actual-Action',m,lambda:m.declare_skill('attempt',declaration));m.actions=1
    check('all-invalid-declarations-leave-feat-unspent',m.allowance.use.current==1 and not m.pending)
    m.declare_skill('paid-interrupted',declaration)
    reject('skill-pending-cannot-bank-into-next-turn',m,lambda:m.begin_turn('next','round2',66))
    reject('skill-pending-cannot-bank-into-rest',m,lambda:m.rest('sr',kind='SR',beneficial=True))
    reject('skill-pending-no-unauthorized-refund-interruption',m,lambda:m.interrupt('paid-interrupted',actual_authorized_interrupt=False))
    m.interrupt('paid-interrupted',actual_authorized_interrupt=True)
    check('skill-interruption-retains-costs',m.pending is None and m.actions==0 and m.allowance.use.current==0 and m.events['paid-interrupted']['status']=='interrupted-no-refund')
    reject('skill-interrupted-no-later-outcome',m,lambda:m.resolve_skill('paid-interrupted',20))
    m.begin_turn('later','round2',66)
    reject('skill-extra-Action-no-second-feat-use',m,lambda:m.declare_skill('attempt',declaration))
    check('skill-genuine-rest-only-restores-use-not-preparation',m.rest('realSR',kind='SR',beneficial=True) and m.allowance.use.current==1 and m.prepared is None)
    reject('skill-rest-requires-new-preparation',m,lambda:m.declare_skill('attempt',declaration))
    record('skill-input-boundaries-interruption-recovery',m)
    check('all-sources-unchanged',bindings==[info(p) for p in source_paths])
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'pass','checks':len(checks),'failures':[],
        'sourceBindings':bindings,'completeMenu':menu,'completeSourceCards':[next(c for c in class_sources[r['actualSourceClass']]['cards'] if c['id']==r['sourceId']) for r in menu],
        'completeFeatContract':contracts['versatile_mastery'],'results':checks,'histories':histories,
        'counts':{'permittedCards':12,'conditionalHistories':len(histories),'sourceClasses':5,'borrowerClasses':['Warrior','Bard']},
        'scope':'Paid Human feat, real first-class training and earned opportunity, source-valid donor selections; bounded preparation/consent/range/payment, all12 native borrowed effects and skill alternative under explicitly conditional encounter facts.',
        'transactionExtension':'Five attack cards and two task cards now declare/pay without accepting any dice, then resolve separately; actual-authorized interrupt retains all costs. Feint/Covering Fire consumption and immediate Shadow Hide boundaries are exercised. The skill alternative now separately declares/pays and resolves one actual Action task through its normal sourced ability, without granting permanent training; full Nature Whisper casting remains separate.',
        'limitations':['Donor selections follow actual level1 schedules; party/consent, physical bodies/items/ammunition/tools, geometry, completed uninterrupted work and clock identities remain stated test-world facts, not authenticated campaign records.',
            'Conditional personal same-card prior-use histories exercise shared counters; this is not a full natural class-card activation or rest/time engine. No multiclass, class-selection advancement or respec procedure is inferred.',
            'Damage is native before passive defenses, damage packet/Wounds/healing and independent actually-owned riders. Borrowing itself creates no class resources; existing separate feature triggers remain outside this slice.',
            'Movement is one-dimensional with declared actual route segments. Shadow Hide is a bounded immediate paired operation; arbitrary interleaving, global stealth observations and opportunity-attack resolution are not implemented.',
            'Nature Whisper positive use assumes independently valid minor-Weave clearance and a sourced personal Bard RP pool; full Weave/Dissonance, casting interruption and component integration are still separate obligations.',
            'Feint and Covering Fire later attack claims consume before outcome, with conditional actual attack/alliance facts supplied by the caller. No full combat scheduler/attack authorization is invented. Full FXC04/07/08/09 closure and complete feat approval are not claimed.'],
        'earlierReport':info(A/'FEAT335_BORROWED_TRANSACTIONS_CHECK.json'),'skillTransactionScope':'Two genuinely class-selected Soldier skills, borrower trained Athletics and untrained Intimidation, separately paid before four actual Core task faces; exact precommit validation, interruption and recovery. Other authorized ability/task timing variants and real task context are not invented.','newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output)}))
if __name__=='__main__':main()
