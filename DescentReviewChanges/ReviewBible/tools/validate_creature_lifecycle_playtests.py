"""Adversarial state transitions for bounded creature lifecycle interfaces."""
from pathlib import Path
from dataclasses import replace
from copy import deepcopy
import json
from creature_lifecycle_playtest_rules import *
from maximum_hp_playtest_rules import MaxHpRecord
ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append({'name':name,'result':'PASS'})
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append({'name':name,'result':'PASS'})
        else:raise AssertionError(name)
    def stats(cls='wizard',owner='owner',level=10):
        return SourceStats(owner,cls,level,4,3,2,7,15,wisdom=3)
    def summon(world,profile='mirror',ident='pet',cls='mirrorsage',**kw):
        sources={'mirror':'mirrorsage.base.mirror-beast-summon','familiar':'mage.arch.conjure-elemental-familiar',
                 'radiant':'mirrorsage.hero.light-weaver.radiant-mirror-beast','swarm':'druid.base.rotshaper.swarm-summoning'}
        args=dict(use_key='summon:'+ident,legal=True,ledger=CommandLedger('owner'))
        if profile=='familiar':args['focus']='fire'
        if profile in ('swarm','radiant'):args['concentration']='conc:'+ident
        args.update(kw)
        return world.summon(sources[profile],(ident,),stats(cls),0,ClockMarker(18),Wallet(20),**args)[0]
    def corpse(world,ident,kind='humanoid',**kw):
        c=Corpse(ident,'original:'+ident,kind,**kw);world.register_corpse(c);return c
    def harvest(world,ident='s',body='body',profile='skeleton',**kw):
        corpse(world,body)
        return world.harvest(ident,body,profile,stats(),Wallet(10),use_key='harvest:'+ident,legal=True,**kw)
    def ranger(world,ident='animal',**kw):
        args=dict(use_key='bond:'+ident,old_hp=7,old_maximum=20,movement_mode='fly',speed=40,keen_sense='smell',
                  legal=True,effects={'disease':'original','injury':'old-scar'})
        args.update(kw)
        return world.bond_ranger(ident,stats('ranger'),Wallet(10),**args)
    def lich(world):return world.unlock_lich(stats('mage'),{p:p for p in ELITES},successful_transformation=True)

    b=CreatureWorld();c=summon(b,mirrorcall=True)
    check('Mirrorcall adjusts creation HP/speed',(c.hp,c.maximum_hp,c.ac,c.speed),(23,23,14,35))
    c.hp=9;c.effects['marked']='persists';c.spent_uses.add('old');c.recharges['x']=6
    b.shift_appearance('pet',1,Wallet(1),method='mirror-shift',appearance='stored bat',movement='climb',use_key='shift1',legal=True)
    check('Appearance never imports anatomy or heals',(c.hp,c.effects,c.spent_uses,c.recharges,c.movement_overrides),(9,{'marked':'persists'},{'old'},{'x':6},{'shift':{'climb':30}}))
    rejects('Mirror Shift cannot grant flight',lambda:b.shift_appearance('pet',1,Wallet(1),method='mirror-shift',appearance='bat',movement='fly',use_key='shift2',legal=True))
    old=deepcopy(c);w=Wallet(1)
    rejects('Insufficient RP cannot dismiss prior Beast',lambda:b.summon('mirrorsage.base.mirror-beast-summon',('new',),stats('mirrorsage'),1,ClockMarker(60),w,use_key='new',legal=True,ledger=CommandLedger('owner')))
    check('Rejected replacement preserves old creature/payment',(c,w.rp),(old,1))
    b.damage('pet',99,2)
    check('Finite zero ends without organic states/corpse',(c.state,len(b.corpses)),('ended',0))
    rejects('Finite corpse cannot be relabeled real',lambda:b.register_corpse(Corpse('fake','pet','humanoid')))
    rejects('Healing cannot resummon ended creature',lambda:b.heal('pet',8,3,legal=True))
    b=CreatureWorld();f=summon(b,'familiar',cls='mage')
    check('Familiar finite profile',(f.hp,f.ac,f.focus,f.effects),(18,16,'fire',{'resistance':'fire'}))
    f.hp=4;f.refresh_maximum(stats('mage',level=20))
    check('Finite base stats remain creation snapshot',(f.hp,f.maximum_hp,f.ac),(4,18,16))
    check('Familiar attacks use current source-owner stats',f.attack_profile(replace(stats('mage'),attack=11))['attack'],11)
    rejects('Temporary controller cannot overwrite stat owner',lambda:f.attack_profile(stats('mage',owner='dominator')))
    f2=summon(b,'familiar','f2','mage',focus='lightning')
    check('New familiar replaces old and uses chosen Focus',(f.state,f2.focus,f2.movement_overrides),('ended','lightning',{'fly':30}))
    b.expire(18,{})
    check('Duration ending produces no corpse',(f2.state,b.corpses),('ended',{}))

    b=CreatureWorld();sw=summon(b,'swarm',cls='druid')
    pair=b.summon('druid.hero.rotshaper.insect-broodmother',('a','b'),stats('druid'),0,ClockMarker(50),Wallet(),
                  use_key='brood/form1',legal=True,parent_form='form1',form_surge_paid=True)
    check('Brood two bodies share one command identity',(len(pair),pair[0].command_group==pair[1].command_group),(2,True))
    ledger=CommandLedger('owner');o=b.command('pair',('a','b'),'attack',1,0,Wallet(),ledger,regular=True,legal=True,capable=True)
    check('Brood pair gets one combined attack',b.resolve_command('pair',1,attached_phase=True,legal=True,capable=True)['attackRolls'],1)
    b.end_dependency(form='form1')
    check('Form end preserves independent Base Swarm',(pair[0].state,pair[1].state,sw.state),('ended','ended','active'))
    b.end_dependency(concentration='conc:pet')
    check('Actual concentration ends independent Swarm',sw.state,'ended')
    sub=paid_swarm_substitution(paid_count=1,duration=ClockMarker(90),concentration='paidspell',form_id='vermin')
    check('Master of Vermin preserves paid spell dependency',(sub['count'],sub['expiry'],sub['parentForm'],sub['additionalCasts']),(1,ClockMarker(90),None,0))
    rejects('Form swarm cannot exceed one minute',lambda:b.summon('druid.hero.rotshaper.carrion-rat-king',('rat',),stats('druid'),0,ClockMarker(61),Wallet(),use_key='rat',legal=True,parent_form='rat-form',form_surge_paid=True))
    rejects('No unpaid Form Surge',lambda:b.summon('druid.hero.rotshaper.insect-broodmother',('x','y'),stats('druid'),0,ClockMarker(60),Wallet(),use_key='brood',legal=True,parent_form='form',form_surge_paid=False))

    b=CreatureWorld();r=ranger(b)
    check('Wounded initial bond is proportional and preserves state',(r.hp,r.maximum_hp,r.effects),(8,23,{'disease':'original','injury':'old-scar'}))
    check('Retained movement is one legal capped mode',(r.movement_mode,r.speed,r.keen_sense),('fly',40,'smell'))
    rejects('Wounded Beast cannot rebond for healing',lambda:ranger(b,'new'))
    r.refresh_maximum(replace(stats('ranger'),level=20,wisdom=4,pb=6))
    check('Ranger growth adds capacity only',(r.hp,r.maximum_hp,r.ac),(8,44,15))
    r.refresh_maximum(replace(stats('ranger'),level=1,wisdom=-5,pb=2))
    check('Actual negative WIS not minimum M',(r.hp,r.maximum_hp,r.ac),(1,1,13))
    outcome=b.damage('animal',1,1)
    check('Ranger zero is actual death without Wound/save',(outcome['state'],outcome['woundRoll'],outcome['deathSave'],len(b.corpses)),('dead',False,False,1))
    rejects('No rebond before completed long rest',lambda:ranger(b,'next'))
    b.completed_long_rest('owner',stats('ranger'),100)
    check('Long rest alone does not resurrect Beast',r.state,'dead')
    rejects('Same animal requires independently legal resurrection',lambda:ranger(b,'animal'))
    body=b.corpses['body:animal'];body_identity=id(body)
    b.record_ranger_resurrection('animal',legal=True,restored_hp=2,restored_maximum=20)
    check('Accepted resurrection immediately removes corpse eligibility before rebond',(r.state,body.available,body.body_state),('unbonded',False,'living'))
    rejects('Living resurrected body cannot be consumed as a corpse',lambda:b.consume_body('body:animal','corpse spell'))
    rejects('Rebond cannot invent healthier post-resurrection ratio',lambda:ranger(b,'animal',resurrected=True,old_hp=20,old_maximum=20,use_key='bond/lr2'))
    r2=ranger(b,'animal',resurrected=True,old_hp=2,old_maximum=20,use_key='bond/lr2')
    check('Resurrected real identity requires full wounded ritual',(r2.instance_id,r2.hp),('animal',2))
    check('Rebond keeps one living body record',(id(body)==body_identity,body.available,len(b.corpses)),(True,False,1))
    b.damage('animal',99,101)
    check('Second genuine death reactivates SAME physical corpse',(id(b.corpses['body:animal'])==body_identity,body.available,body.body_state,len(b.corpses),r2.death_count),(True,True,'corpse',1,2))
    rejects('No duplicated corpse fragments',lambda:b.register_corpse(Corpse('fragment','animal','beast')))
    b.consume_body('body:animal','actual future legal consumer')
    before=deepcopy((body,r2))
    rejects('Ordinary resurrection cannot recreate a consumed body',lambda:b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20))
    check('Rejected missing-body return is atomic',(body,r2),before)
    b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20,body_reconstructed=True)
    check('Explicit independent source reconstruction retains physical identity/provenance',(id(body)==body_identity,body.available,body.consumed_by),(True,False,'actual future legal consumer'))
    rejects('Actual resurrection alone does not bypass after-death rest requirement',lambda:ranger(b,'animal',resurrected=True,old_hp=1,old_maximum=20,use_key='bond/lr3'))
    b=CreatureWorld();r=ranger(b);b.damage('animal',99,1,body_survives=False)
    check('Body-destroying death retains unavailable original body identity',(b.corpses['body:animal'].body_state,b.corpses['body:animal'].available),('removed',False))
    rejects('Removed body cannot spontaneously return',lambda:b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20))
    rejects('Notification cannot itself grant resurrection permission',lambda:b.record_ranger_resurrection('animal',legal=False,restored_hp=1,restored_maximum=20,body_reconstructed=True))
    b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20,body_reconstructed=True)
    check('Explicit source reconstruction of removed body makes it living not corpse',(r.state,b.corpses['body:animal'].available),('unbonded',False))
    rejects('Duplicate resurrection event cannot refill living animal',lambda:b.record_ranger_resurrection('animal',legal=True,restored_hp=20,restored_maximum=20,body_reconstructed=True))
    rejects('Canonical S cannot exceed4',lambda:replace(stats(),scale=5))
    rejects('Canonical M cannot be0',lambda:replace(stats(),modifier=0))

    b=CreatureWorld();els=lich(b);e=b.creatures['boneflayer']
    e.hp=1;e.spent_uses.add('fear/enc');e.recharges['fear']=12;e.effects['curse']='still applies'
    e.refresh_maximum(stats('mage',level=20))
    check('Elite dynamic capacity does not heal',(e.hp,e.maximum_hp),(1,52))
    b.damage('boneflayer',5,1)
    check('Destroyed elite remains same asset without corpse',(e.state,e.asset_id,len(b.corpses)),('destroyed','boneflayer',0))
    rejects('Destroyed elites still block duplicate unlock',lambda:lich(b))
    oldid=id(e);w=Wallet(5)
    b.soulbound('boneflayer',stats('mage',level=20),w,2,use_key='ritual/lr1',legal=True)
    check('Soulbound restores same identity at half current max',(id(e)==oldid,e.hp,e.temp_hp,e.temp_expiry),(True,26,5,ClockMarker(62)))
    check('Soulbound preserves independent history',(e.spent_uses,e.recharges,e.effects),({'fear/enc'},{'fear':12},{'curse':'still applies'}))
    check('Soulbound pays Action/RP/use',(w.actions,w.rp,w.used),(0,0,{'ritual/lr1'}))
    e.hp=1;b.damage('boneflayer',5,3)
    b.completed_long_rest('owner',stats('mage',level=20),100)
    check('Completed LR returns same elite full without independent reset',(id(e)==oldid,e.hp,e.spent_uses,e.recharges),(True,52,{'fear/enc'},{'fear':12}))
    rejects('Wizard elite cannot use Mage constructor',lambda:CreatureWorld().unlock_lich(stats('wizard'),{p:p for p in ELITES},successful_transformation=True))
    check('Wizard supplied profile remains inspectable',elite_profile('dreadblade',stats())['maximumHP'],46)
    rejects('Cross-class duplicate elite identities invalid',lambda:validate_elite_assets([('owner','boneflayer','mage-bone'),('owner','boneflayer','wizard-bone')]))
    e=b.creatures['wraithbound'];e.offense_event(1)
    check('Wraith attack/control immediately ends invisibility',e.invisible,False)
    e.regular_end(1);check('Wraith remains visible at current marker end',e.invisible,False)
    e.regular_end(2);check('Wraith returns at next proper marker',e.invisible,True)
    rejects('Extra turn cannot supply companion marker',lambda:e.regular_end(3,regular=False))
    rejects('Initiative reordering cannot replay old marker',lambda:e.regular_end(1))

    b=CreatureWorld();s=harvest(b)
    check('Harvest consumes body and uses snapshot stats',(b.corpses['body'].available,s.hp,s.ac),(False,26,14))
    s.hp=3;s.refresh_maximum(stats(level=20))
    check('Standard undead base does not grow with level',(s.hp,s.maximum_hp),(3,26))
    corpse(b,'kill1');b.auto_raise_trigger('s','kill1',1,'attached1','raise1')
    check('Auto-Raise immediately reserves one capacity',b.standard_count('owner'),2)
    harvest(b,'s2','body2')
    corpse(b,'body3');w=Wallet(4)
    rejects('Reserved third slot prevents fourth manual raise',lambda:b.harvest('s3','body3','skeleton',stats(),w,use_key='h3',legal=True))
    check('Over-cap failure preserves payment/body',(w.rp,b.corpses['body3'].available),(4,True))
    b.damage('s',999,2)
    raised=b.auto_raise_checkpoint('attached1',{'owner':stats()},{'raise1':('raised',True,())},2)[0]
    check('Killer destruction does not cancel reserved raise',(raised.profile,raised.blocked_round,raised.state),('skeleton',1,'active'))
    check('New minion cannot even defensive-move/Dodge',b.uncommanded('raised',2,1,capable=True),())
    rejects('Creation-round attack forbidden',lambda:b.command('newattack',('raised',),'attack',1,2,Wallet(),CommandLedger('owner'),regular=True,legal=True,capable=True))
    check('Next numbered round permits defensive behavior',b.uncommanded('raised',2,2,capable=True),('defensive-move','dodge'))
    corpse(b,'later');check('After-checkpoint kill creates no orphan reservation',b.auto_raise_trigger('raised','later',2,'attached1','late'),None)
    check('After-checkpoint rejected trigger leaves later round unused',('owner',2) in b.auto_used,False)
    rejects('Closed checkpoint cannot reopen',lambda:b.auto_raise_checkpoint('attached1',{},{}))
    b.completed_long_rest('owner',stats(),100)
    check('Auto-Raised and harvested standard minions end at LR',(raised.state,b.creatures['s2'].state),('ended','ended'))
    check('No consumed body returns on ending',b.corpses['kill1'].available,False)

    b=CreatureWorld();s=harvest(b);corpse(b,'kill');b.auto_raise_trigger('s','kill',1,'end','r')
    b.consume_body('kill','another legal corpse consumer')
    check('Reservation does not freeze corpse',b.auto_raise_checkpoint('end',{'owner':stats()},{'r':('new',True,())}),())
    check('Failed raise consumes round opportunity and releases slot',(b.auto_used,b.standard_count('owner')),({('owner',1)},1))
    corpse(b,'later');check('Later kill cannot replace failed opportunity',b.auto_raise_trigger('s','later',1,'end2','r2'),None)
    b=CreatureWorld();s=harvest(b)
    corpse(b,'fiend','fiend');check('No Pact means Fiend ineligible',b.auto_raise_trigger('s','fiend',1,'end','r'),None)
    check('Pact enables Fiend Skeleton raise',b.auto_raise_trigger('s','fiend',1,'end','r',pact=True).profile,'skeleton')
    conj=MaxHpRecord('conj','wizard.engine[10]','owner','raised',10)
    rejects('Auto-Raise cannot gain new Conjuration snapshot',lambda:b.auto_raise_checkpoint('end',{'owner':stats()},{'r':('raised',True,(conj,))}))
    check('Invalid modifier preflight preserves reservation/checkpoint',('r' in b.reservations,'end' in b.closed_checkpoints),(True,False))
    b.auto_raise_checkpoint('end',{'owner':stats()},{'r':('raised',True,())})
    b=CreatureWorld();corpse(b,'gob',goblinoid=True)
    g=b.harvest('g','gob','goblin-thrall',stats(),Wallet(4),use_key='h',legal=True)
    corpse(b,'human');check('Goblin Thrall cannot convert ordinary Humanoid',b.auto_raise_trigger('g','human',1,'end','r'),None)
    corpse(b,'devil','fiend');check('Pact does not bypass goblinoid predicate',b.auto_raise_trigger('g','devil',1,'end','r',pact=True),None)
    corpse(b,'gob2',goblinoid=True);check('First qualifying goblinoid kill auto-reserves',b.auto_raise_trigger('g','gob2',1,'end','r').profile,'goblin-thrall')

    b=CreatureWorld();s=harvest(b);ledger=CommandLedger('owner');w=Wallet(2)
    b.command('lash',('s',),'attack',1,0,w,ledger,regular=True,legal=True,capable=True,ghoul_lash=True,adjacent_controlled_undead=True)
    check('Ghoul Lash pays one command plus2RP',(w.rp,w.bonus_action,ledger.rounds[1]),(0,False,{'command':True,'damage':True}))
    check('Ghoul Lash resolves two actual rolls',b.resolve_command('lash',1,attached_phase=True,legal=True,capable=True)['attackRolls'],2)
    rejects('Command cannot resolve twice',lambda:b.resolve_command('lash',1,attached_phase=True,legal=True,capable=True))
    rejects('No Gadget Sync after paid companion offense',lambda:ledger.activate(1,'gadget-sync',Wallet(1),rp=1))
    b=CreatureWorld();lich(b);ledger=CommandLedger('owner');w=Wallet()
    b.command('fear',('boneflayer',),'control',1,0,w,ledger,regular=True,legal=True,capable=True)
    rejects('Non-damaging Mage fear also blocks Gadget Sync',lambda:ledger.activate(1,'gadget-sync',Wallet(1),rp=1))
    check('Invalid resolution loses committed command',b.resolve_command('fear',1,attached_phase=True,legal=False,capable=True)['resolved'],False)
    check('Invalid later target gives no BA refund',w.bonus_action,False)
    rejects('Ordinary command cannot issue on extra turn',lambda:b.command('extra',('boneflayer',),'attack',2,2,Wallet(),CommandLedger('owner'),regular=False,legal=True,capable=True))
    check('Uncommanded living elite has no independent offense',b.uncommanded('boneflayer',1,1,capable=True),('defensive-move','dodge'))

    b=CreatureWorld();c=summon(b,'radiant');ledger=CommandLedger('owner');echoes=EchoLedger('owner',{'rec'});w=Wallet(5)
    before=deepcopy((w,ledger,echoes,c))
    rejects('Echo needs own legal perception/origin before all payment',lambda:b.echo_from_beast('pet',stats('mirrorsage'),1,1,'rec',2,w,ledger,echoes,own_turn=True,legal=False))
    check('Invalid Echo is atomic',(w,ledger,echoes,c),before)
    out=b.echo_from_beast('pet',stats('mirrorsage'),1,1,'rec',2,w,ledger,echoes,own_turn=True,legal=True)
    check('Beast Echo is immediate owner Action with no free movement',(out['resolves'],out['extraBeastMovement'],out['caster']),('immediate owner Action',False,'owner'))
    check('Echo consumes Action BA record and release cap',(w.actions,w.bonus_action,w.rp,echoes.records,echoes.released_rounds),(0,False,3,set(),{1}))
    check('Echo leaves offensive allowance unused',ledger.rounds[1]['damage'],False)
    ledger.activate(1,'gadget-sync',w,rp=1)
    check('Legal later Gadget Sync uses remaining offense',(w.rp,ledger.rounds[1]['damage']),(2,True))
    rejects('Radiant cannot heal after same-round Echo',lambda:b.command('heal',('pet',),'radiant-heal',1,1,Wallet(1),CommandLedger('owner'),regular=True,legal=True,capable=True))
    echoes.records.add('rec2');w=Wallet(2,actions=1,bonus_action=False)
    rejects('Extra Action alone cannot pay Echo BA',lambda:b.echo_from_beast('pet',stats('mirrorsage'),2,2,'rec2',2,w,ledger,echoes,own_turn=True,legal=True))
    check('Missing BA preserves record/RP',(echoes.records,w.rp),({'rec2'},2))
    b.echo_from_beast('pet',stats('mirrorsage'),2,2,'rec2',2,Wallet(2),ledger,echoes,own_turn=True,legal=True)
    check('Actual extra own turn with real BA may Echo',2 in echoes.released_rounds,True)

    b=CreatureWorld();c=summon(b);ledger=CommandLedger('owner');hard=HardDenialLedger();w=Wallet(3)
    bond=b.apply_reflective('owner','original-enemy','charm',ClockMarker(18),'conc',w,ledger,use_key='charm/lr',legal=True,failed_save=True)
    check('Reflective replaces Beast without damaging original target',(c.state,bond.target_id,hard.used),('ended','original-enemy',set()))
    resolution=bond.queue(1,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=False,capable=True,legal=True)
    check('After target already acted queues next round',resolution,2)
    check('BA issue round and offense next round are distinct',(ledger.rounds[1],ledger.reservations),({'command':True,'damage':False},{2:'force'}))
    rejects('Future reservation blocks device offense',lambda:ledger.activate(2,'gadget-sync',Wallet(1),rp=1))
    w=Wallet();before=deepcopy(w)
    rejects('Second pending order fails before payment',lambda:bond.queue(2,2,'force2',w,ledger,hard,'enc',target_turn_upcoming=True,capable=True,legal=True))
    check('Second-order rejection keeps new BA',w,before)
    hard.spend('enc','owner','original-enemy')
    check('Other feature spending hard guard cancels reservation',bond.revalidate_pending(2,ledger,hard,capable=True,legal=True),False)
    check('Canceled order releases offense but not original BA',(ledger.reservations,ledger.rounds[1]['command'],bond.pending),({},True,None))
    rejects('Spent hard guard grants no fallback command',lambda:bond.queue(2,2,'force2',Wallet(),ledger,hard,'enc',target_turn_upcoming=True,capable=True,legal=True))
    check('Charm relation can remain after hard denial spent',bond.operative(2),True)
    b=CreatureWorld();ledger=CommandLedger('owner');hard=HardDenialLedger()
    bond=b.apply_reflective('owner','enemy','charm',ClockMarker(18),'conc',Wallet(3),ledger,use_key='charm/lr',legal=True,failed_save=True)
    bond.queue(0,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=True,capable=True,legal=True)
    rejects('Forced action cannot use a duplicate/extra turn',lambda:bond.resolve(1,1,ledger,hard,actual_regular_action_slot=False,capable=True,legal=True))
    out=bond.resolve(1,1,ledger,hard,actual_regular_action_slot=True,capable=True,legal=True)
    check('One forced normal Action commits hard guard',(out['replacesNormalAction'],out['extraTurn'],hard.used),(True,False,{('enc','owner','enemy')}))
    rejects('Same Charm never grants second forced Action',lambda:bond.queue(2,2,'again',Wallet(),ledger,hard,'enc2',target_turn_upcoming=True,capable=True,legal=True))
    b=CreatureWorld();ledger=CommandLedger('owner');hard=HardDenialLedger()
    bond=b.apply_reflective('owner','enemy','charm',ClockMarker(18),'conc',Wallet(3),ledger,use_key='charm/lr',legal=True,failed_save=True)
    bond.queue(0,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=False,capable=True,legal=True)
    b.end_dependency(concentration='conc',ledger=ledger)
    check('Concentration ending cancels future reservation without hard spend',(bond.active,ledger.reservations,hard.used),(False,{},set()))
    b=CreatureWorld();ledger=CommandLedger('owner');hard=HardDenialLedger()
    bond=b.apply_reflective('owner','enemy','charm',ClockMarker(18),'conc',Wallet(3),ledger,use_key='charm/lr',legal=True,failed_save=True)
    bond.queue(0,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=False,capable=True,legal=True)
    summon(b,ledger=ledger)
    check('Mirror replacement cancels Charm order without killing target',(bond.active,ledger.reservations,hard.used),(False,{},set()))

    states=0
    for level in range(1,21):
        for wisdom in (-5,-1,0,3,5):
            for old_max in (1,7,20):
                for hp in range(1,old_max+1):
                    b=CreatureWorld();st=replace(stats('ranger',level=level),wisdom=wisdom)
                    c=b.bond_ranger('animal',st,Wallet(4),use_key='bond',old_hp=hp,old_maximum=old_max,
                                    movement_mode='walk',speed=30,keen_sense='smell',legal=True)
                    mx=max(1,2*level+wisdom)
                    assert c.hp==max(1,mx*hp//old_max) and 1<=c.hp<=mx
                    before=c.hp;c.refresh_maximum(replace(st,level=20,wisdom=5))
                    assert c.hp==before
                    states+=1
    disposition=json.loads((ROOT/'data/playtest/creature_lifecycle_bindings.json').read_text(encoding='utf-8'))
    result={'result':'PASS','status':disposition['status'],'reviewClosure':disposition.get('reviewClosure'),
            'scope':'100 source roles plus5 frozen supports; selected lifecycle boundaries only, not complete cards/runtime',
            'checkCount':len(checks),'rangerConversionStates':states,'checks':checks}
    (ROOT/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} creature lifecycle checks and {states} Ranger conversion states.')


if __name__=='__main__':main()
