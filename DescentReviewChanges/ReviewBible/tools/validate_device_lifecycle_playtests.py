"""Adversarial tests for reviewed boundaries, not full-card execution."""
from pathlib import Path
from copy import deepcopy
import json
from device_lifecycle_playtest_rules import *
from redirection_playtest_rules import DamageRoot
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
    def board(slots=2,totems=2):
        return Lifecycle({('owner','deployable'):slots,('owner','totem'):totems})
    def entity(ident='e',kind='device',maximum=20,**kw):
        slots={'device':('deployable',1),'salvage':('deployable',1),
               'totem':('totem',1),'echo':('totem',1),'field':('deployable',1)}
        sk,sc=slots.get(kind,(None,0))
        args=dict(instance_id=ident,owner='owner',source_id='tinker.engine[6]',
                  kind=kind,maximum_hp=maximum,hp=maximum,ac=14,
                  expiry=ClockMarker(18),slot_kind=sk,slot_count=sc,paid_deployment_rp=2)
        if kind=='drone':args.update(asset_id='asset-'+ident,expiry=None,source_id='tinker.engine[1]',paid_deployment_rp=0)
        if kind=='field':args.update(maximum_hp=None,hp=None,ac=None,source_id='tinker.hero.artificer.restoration-field')
        if kind in ('totem','echo'):args.update(concentration='all-totems',source_id='shaman.engine[0]')
        args.update(kw)
        return Entity(**args)
    def put(b,e):
        b.place((e,),ClockMarker(0),Wallet(100),rp=0,action=None)
        return e
    def kill(b,e,event='death',**kw):
        return b.damage(e.instance_id,ClockMarker(1),999,event_id=event,**kw)[1]

    b=board();e=put(b,entity(kind='drone'));w=Wallet(5)
    remaining=b.disable('e',0,w,dissonance=3,amount=2,use_key='route/sr1')
    check('Routing consumes BA and Dissonance but not RP',(remaining,w.rp,w.bonus_action),(1,5,False))
    b.retract('e');b.redeploy('e',0)
    check('Retraction/redeployment preserves protected disablement',(e.state,e.disabled),('deployed',True))
    d=kill(b,e,enemy_caused=True);b.reconstruct('e',2,Wallet(5),method='snap',use_key='snap/enc1')
    check('Snap returns positive HP but preserves disable',(e.hp,e.disabled,e.state),(10,True,'deployed'))
    check('Snap consumes first-event debris',(d.material_available,d.material_consumer),(False,'snap'))
    b.field_repair('e',2,Wallet(1),20)
    check('Field Repair clears disable and heals up to maximum',(e.disabled,e.hp),(False,20))
    b.set_disabled(e,True);w=Wallet(1)
    check('Full-HP disabled Field Repair is legal',b.field_repair('e',2,w,12),0)
    check('Full-HP clear still costs Action and RP',(w.actions,w.rp),(0,0))
    rejects('Full-HP enabled Field Repair invalid',lambda:b.field_repair('e',2,Wallet(1),10))
    b.retract('e');e.hp=5;w=Wallet(1)
    check('Touched retracted Drone accepts Field Repair',b.field_repair('e',2,w,8),8)
    check('Retracted repair neither redeploys nor resets payment',(e.hp,e.state,w.rp,w.actions),(13,'retracted',0,0))
    e.hp=e.maximum_hp;b.set_disabled(e,True)
    check('Full-HP retracted Drone may clear disable by touch',b.field_repair('e',2,Wallet(1),5),0)
    check('Touch clearing preserves retraction',(e.state,e.disabled),('retracted',False))
    rejects('Retracted Drone still cannot route Dissonance',lambda:b.disable('e',2,Wallet(),dissonance=2,amount=1,use_key='route/sr2'))
    e.unavailable=True;e.hp=5
    rejects('Withdrawn unavailable Drone not eligible in current configuration',lambda:b.field_repair('e',2,Wallet(1),5))

    b=board();e=put(b,entity(kind='drone',disabled=True))
    kill(b,e);b.completed_short_rest('owner')
    check('Short rest clears flag only',(e.hp,e.state,e.disabled),(0,'destroyed',False))
    rejects('Field Repair cannot revive destroyed Drone',lambda:b.field_repair('e',2,Wallet(2),20))
    b.set_disabled(e,True);b.tools_clear_disable('e',Wallet(1))
    check('Separate tools procedure clears flag without reconstruction',(e.disabled,e.hp),(False,0))
    b.set_disabled(e,True);b.reconstruct('e',2,Wallet(1),method='drone-ten-minute',use_key='drone/sr1')
    check('Drone ten-minute reconstruction does not merge disable-clear',(e.hp,e.disabled),(10,True))

    b=board(1);e=put(b,entity());kill(b,e,enemy_caused=True)
    check('Destruction releases active slot',b.free('owner','deployable',2),1)
    blocker=put(b,entity('block'));w=Wallet(4)
    rejects('Snap cannot evict occupied slot',lambda:b.reconstruct('e',2,w,method='snap',use_key='snap/enc1'))
    check('Failed Snap leaves wallet and debris intact',(w.rp,w.bonus_action,b.material('e')[1].material_available),(4,True,True))
    b.end('block');b.reconstruct('e',2,w,method='snap',use_key='snap/enc1')
    check('Snap reacquires same slot footprint',b.free('owner','deployable',2),0)
    e.ammunition={'rocket':1};e.spent_uses={'used'};e.modules=('offense',)
    d2=kill(b,e,'death2',enemy_caused=True)
    check('Second physical death creates no second material',(d2.first_for_instance,d2.material_available),(False,False))
    check('Second physical death cannot cause Volatile',b.settle_volatile('death2',2,chosen=True,enemy_in_range=True,scale=2),0)
    rejects('Second death has no Snap material',lambda:b.reconstruct('e',3,Wallet(4),method='snap',use_key='snap/enc2'))

    b=board();e=put(b,entity());kill(b,e,friendly_damage=True)
    w=Wallet(0);check('Friendly/accidental destruction can recycle',b.recycling('e',w,use_key='recycle/sr1'),1)
    check('Recycling refunds no more than deployment RP',w.rp,1)
    rejects('Consumed Recycling debris cannot Snap',lambda:b.reconstruct('e',2,Wallet(4),method='snap',use_key='snap/enc1'))
    rejects('Consumed debris cannot recycle twice',lambda:b.recycling('e',Wallet(),use_key='recycle/sr2'))
    b=board();e=put(b,entity(paid_deployment_rp=0));kill(b,e)
    check('Free deployment gets zero refund',b.recycling('e',Wallet(),use_key='recycle/sr1'),0)
    b=board();e=put(b,entity());kill(b,e,flags={'noResourceGeneration'})
    rejects('Inherited noResourceGeneration blocks Recycling',lambda:b.recycling('e',Wallet(),use_key='recycle/sr1'))
    check('Rejected refund does not consume debris',b.material('e')[1].material_available,True)
    b=board();e=put(b,entity());d=kill(b,e,enemy_caused=True,incoming_damage_was_copy=True)
    check('Real object and copied incoming damage stay distinct',(d.copied_object,d.incoming_damage_was_copy),(False,True))
    check('Copied incoming damage retains ordinary target-side destruction',b.settle_volatile('death',1,chosen=True,enemy_in_range=True,scale=2),2)
    check('Copy damage alone does not prohibit later Recycling',b.recycling('e',Wallet(),use_key='recycle/sr1'),1)
    b=board();e=put(b,entity(is_copy=True));d=kill(b,e,enemy_caused=True)
    check('Copied object exclusion comes from entity record',(d.copied_object,d.incoming_damage_was_copy),(True,False))
    check('Copied object does not qualify Volatile',b.settle_volatile('death',1,chosen=True,enemy_in_range=True,scale=2),0)
    rejects('Copied object cannot recycle',lambda:b.recycling('e',Wallet(),use_key='recycle/sr1'))

    b=board();e=put(b,entity());kill(b,e,enemy_caused=True,enemy_hit=True);b.advance(30)
    rejects('Snap illegal exactly at expiry',lambda:b.reconstruct('e',18,Wallet(3),method='snap',use_key='snap/enc1'))
    check('Earlier destroyed debris remains after expiry',b.material('e')[1].material_available,True)
    check('Recycling can use expired-deployment debris',b.recycling('e',Wallet(),use_key='recycle/sr1'),1)
    b=board();e=put(b,entity());b.advance(18)
    check('Ordinary expiry no destruction/debris',(e.state,len(b.destructions),e.material_event),('expired',0,None))

    b=board();e=put(b,entity(kind='drone',disabled=True))
    e.modules=('support',);e.spent_uses={'existing'};kill(b,e)
    b.recycling('e',Wallet(),use_key='recycle/sr1')
    new=b.long_rest_drone('e','new')
    check('LR after consumed Drone debris is fresh instance',(new.asset_id,new.instance_id,new.hp,new.destruction_history),(e.asset_id,'new',20,[]))
    check('LR rebuild preserves asset disable and module',(new.disabled,new.modules,new.spent_uses),(True,('support',),{'existing'}))
    check('Old incarnation superseded without reuse',(e.superseded,e.unavailable),(True,True))
    b.field_repair('new',2,Wallet(1),3)
    check('Asset flag clear follows historical and current instances',(e.disabled,new.disabled),(False,False))
    d=kill(b,new,'newdeath',enemy_caused=True)
    check('Fresh LR incarnation receives own first death',d.first_for_instance,True)

    b=board();e=put(b,entity(maximum=1));kill(b,e)
    check('Max1 Snap reconstruction has viability minimum',b.reconstruct('e',2,Wallet(2),method='snap',use_key='snap/enc1'),1)
    result=b.repair_pulse(('e',),2,Wallet(3),use_key='repair/sr1',ac_deadline=ClockMarker(6))
    check('Functional max1 Repair Pulse rounds half to zero',result,{'e':0})
    b.set_disabled(e,True)
    rejects('Repair Pulse has no protected-disable clearance',lambda:b.repair_pulse(('e',),2,Wallet(3),use_key='repair/sr2',ac_deadline=ClockMarker(6)))

    b=board();e=put(b,entity());e.hp=1;e.temp_hp=4;e.ammunition={'rocket':1};e.spent_uses={'trap'}
    e.effects['overcharge']={'deadline':ClockMarker(6),'requires':'damaging-activation'}
    b.reconfigure('e',2,Wallet(1),source_id='tinker.arch.deploy-net-trap',new_maximum=2,new_ac=15,known=True,nonhealing=True,slot_count=1,damaging_profile=False)
    check('Reconfiguration fractional minimum does not destroy',(e.hp,e.maximum_hp,len(e.destruction_history)),(1,2,0))
    check('Reconfiguration preserves clocks/temp/ammo/uses',(e.expiry,e.temp_hp,e.ammunition,e.spent_uses,e.effects['overcharge']['deadline']),(ClockMarker(18),4,{'rocket':1},{'trap'},ClockMarker(6)))
    rejects('Reconfiguration cannot gain slot footprint',lambda:b.reconfigure('e',2,Wallet(1),source_id='profile',new_maximum=10,new_ac=14,known=True,nonhealing=True,slot_count=2,damaging_profile=True))
    rejects('Reconfiguration cannot become healing profile',lambda:b.reconfigure('e',2,Wallet(1),source_id='profile',new_maximum=10,new_ac=14,known=True,nonhealing=False,slot_count=1,damaging_profile=False))
    b.set_disabled(e,True)
    rejects('Disabled device cannot reconfigure to escape flag',lambda:b.reconfigure('e',2,Wallet(1),source_id='profile',new_maximum=10,new_ac=14,known=True,nonhealing=True,slot_count=1,damaging_profile=False))

    b=board();e=put(b,entity(kind='drone',maximum=10));e.hp=7
    b.recompute_drone('e',level=3,pb=2,intelligence=4)
    check('Temporary actual INT updates Drone capacity/AC/attack without heal',(e.maximum_hp,e.hp,e.ac,e.attack_bonus),(12,7,17,6))
    b.recompute_drone('e',level=3,pb=2,intelligence=-3)
    check('INT decrease clamps HP without destruction',(e.maximum_hp,e.hp,e.ac,e.attack_bonus,len(e.destruction_history)),(5,5,10,-1,0))
    check('Ordinary deployable Expertise snapshot',profile_stats('device',10,4,modifier=3,expertise=True),{'hp':23,'ac':17})
    check('Harmony named elemental 3L',profile_stats('elemental',10,4,harmony=True)['hp'],30)
    check('Standard elementals use frozen half-PB AC',[profile_stats('elemental',10,pb)['ac'] for pb in range(2,7)],[13,13,14,14,15])
    check('Harmony Chorus one package 5L',profile_stats('chorus',10,4,harmony=True)['hp'],50)
    check('Echo keeps ordinary Totem object stats',profile_stats('echo',10,4),{'hp':20,'ac':16})
    check('Deployable capacity gates',[deployable_capacity(v) for v in (5,6,12,13,16,17)], [0,1,1,2,2,3])
    check('Turret Bay slot/cost fallback',(turret_bay_offer(1),turret_bay_offer(3)),((1,2),(2,4)))
    rejects('Turret Bay no free slot is illegal',lambda:turret_bay_offer(0))

    b=board();p=entity('parent','totem');echo=entity('echo','echo',parent_id='parent')
    b.place((p,echo),0,Wallet(6),rp=6)
    w=Wallet(1);np=entity('np','totem');ne=entity('ne','echo',parent_id='np')
    rejects('Unaffordable replacement leaves parent+Echo',lambda:b.place((np,ne),1,w,rp=6,replace_id='parent'))
    check('Failed placement atomically preserves old board/wallet',(p.state,echo.state,w.rp),('deployed','deployed',1))
    b.place((np,ne),1,Wallet(6),rp=6,replace_id='parent')
    check('Parent replacement frees both for paid parent+Echo',(p.state,echo.state,np.state,ne.state,len(b.destructions)),('replaced','replaced','deployed','deployed',0))
    ep=entity('ep','totem')
    b.place((ep,),1,Wallet(2),rp=2,replace_id='ne')
    check('Replacing Echo alone leaves parent',(np.state,ne.state),('deployed','replaced'))
    rejects('Echo cannot itself replace another Totem',lambda:b.place((entity('bad','echo',parent_id='np'),),1,Wallet(2),rp=2,replace_id='ep'))
    b.end_concentration('owner','all-totems')
    check('Concentration ends all active Totems, no debris',(b.occupied('owner','totem',2),len(b.destructions)),(0,0))
    b=board();p=entity('p','totem');ch=entity('ch','echo',parent_id='p')
    b.place((p,ch),0,Wallet(6),rp=6);kill(b,p)
    check('Parent destruction ends Echo administratively',(p.state,ch.state,len(b.destructions)),('destroyed','ended',1))
    b=board(totems=1);old=put(b,entity('old','totem'))
    b.place((entity('new','totem'),),0,Wallet(2),rp=2,replace_id='old')
    check('Capacity1 replaces prior ordinary Totem',old.state,'replaced')

    ledger=CommandLedger('owner');w=Wallet(4)
    ledger.activate(1,'support',w)
    ledger.activate(1,'gadget-sync',w,rp=1)
    check('Support then Sync uses BA and one damage',(w.rp,w.bonus_action,ledger.rounds[1]),(3,False,{'command':True,'damage':True}))
    rejects('Extra turn does not reset owner round command',lambda:ledger.activate(1,'attack',Wallet(4)))
    ledger=CommandLedger('owner');w=Wallet(4)
    ledger.activate(1,'gadget-sync',w,rp=1);ledger.activate(1,'support',w)
    check('Sync first leaves later legal support BA',ledger.rounds[1],{'command':True,'damage':True})
    ledger=CommandLedger('owner');w=Wallet(4)
    ledger.activate(1,'decoy',w,tinker=True,regular=False)
    check('Off-turn Decoy uses damage allowance, no BA',ledger.rounds[1],{'command':False,'damage':True})
    rejects('Decoy first blocks turret damage later',lambda:ledger.activate(1,'attack',w,tinker=True))
    ledger.activate(1,'support',w,tinker=True)
    rejects('Tinker BA cannot use extra-turn permission',lambda:CommandLedger('owner').activate(2,'attack',Wallet(),tinker=True,regular=False))
    ledger=CommandLedger('owner');w=Wallet(0)
    rejects('Unfunded Sync does not claim allowance',lambda:ledger.activate(1,'gadget-sync',w,rp=1))
    check('Failed command leaves ledger untouched',ledger.rounds,{})

    b=board(1);e=put(b,entity());d=kill(b,e,enemy_caused=True,enemy_hit=True);put(b,entity('occupant'))
    reaper=entity('reaper','reaper',expiry=ClockMarker(6,20))
    b.salvage('e',reaper,2,Wallet(2),reaper=True,use_key='reaper/sr1')
    check('Reaper succeeds with no deployable capacity',(reaper.slot_count,b.free('owner','deployable',2)),(0,0))
    check('Reaper consumes source material',d.material_consumer,'reaper')
    b=board(1);e=put(b,entity());d=kill(b,e,enemy_caused=True);put(b,entity('occupant'));w=Wallet(1)
    rejects('Salvage requires free slot before payment/debris',lambda:b.salvage('e',entity('scrap','salvage'),2,w,use_key='salvage/enc1'))
    check('Failed Salvage preserves material and RP',(d.material_available,w.rp),(True,1))
    b.end('occupant');b.salvage('e',entity('scrap','salvage'),2,w,use_key='salvage/enc1')
    s=b.entity('scrap');kill(b,s,'scrapdeath',enemy_caused=True,enemy_hit=True)
    rejects('Scrapling cannot spawn own replacement',lambda:b.salvage('scrap',entity('chain','reaper'),3,Wallet(2),reaper=True,use_key='reaper/sr2'))
    check('Scrapling destruction grants no generic device material',b.destructions['scrapdeath'].material_available,False)
    check('Scrapling is not a Volatile device',b.settle_volatile('scrapdeath',1,chosen=True,enemy_in_range=True,scale=2),0)
    rejects('Scrapling is not a Recycling device',lambda:b.recycling('scrap',Wallet(),use_key='recycle/sr1'))
    rejects('Scrapling is not a Snap device',lambda:b.reconstruct('scrap',3,Wallet(2),method='snap',use_key='snap/enc1'))
    b=board();s=put(b,entity('s','salvage'));s.hp=5
    rejects('Slot-using Scrapling is not a Field Repair machine',lambda:b.field_repair('s',1,Wallet(1),5))
    rejects('Scrapling is not a Repair Pulse device',lambda:b.repair_pulse(('s',),1,Wallet(3),use_key='repair/sr1',ac_deadline=ClockMarker(6)))
    rejects('Scrapling cannot route protected Dissonance',lambda:b.disable('s',1,Wallet(),dissonance=2,amount=1,use_key='route/sr1'))
    b=board();e=put(b,entity());d=kill(b,e,enemy_caused=True,enemy_hit=True,flags={'noDeathTriggers','noResourceGeneration'})
    w=Wallet(2)
    rejects('noDeathTriggers rejects Reaction Reaper',lambda:b.salvage('e',entity('r','reaper'),2,w,reaper=True,use_key='reaper/sr1'))
    check('Blocked Reaper preserves Reaction RP and material',(w.rp,w.reaction,d.material_available),(2,True,True))
    b.salvage('e',entity('s','salvage'),2,w,use_key='salvage/enc1')
    check('Later Action Salvage not blocked by noDeath/noResource flags',(w.rp,d.material_consumer),(1,'salvage'))
    b=board();r=put(b,entity('r','reaper'))
    result,d=b.damage('r',1,999,event_id='rdeath',enemy_caused=True,enemy_hit=True)
    check('Reaper disappears retaining hard no-own-death-chain',(result['disappeared'],d.no_own_destruction_chain,d.material_available),(True,True,False))

    b=board();e=put(b,entity());kill(b,e,enemy_caused=True,flags={'noRetaliation'})
    check('Emergency provenance blocks Volatile despite enemy cause',b.settle_volatile('death',1,chosen=True,enemy_in_range=True,scale=2),0)
    check('NoRetaliation alone does not block debris',b.material('e')[1].material_available,True)
    b=board();e=put(b,entity());kill(b,e,enemy_caused=True)
    check('Declining own opportunity gives no damage',b.settle_volatile('death',1,chosen=False,enemy_in_range=True,scale=2),0)
    check('Decline does not spend owner round allowance',b.volatile_rounds,set())
    other=put(b,entity('other'));kill(b,other,'otherdeath',enemy_caused=True)
    check('Other device may use owner Volatile after decline',b.settle_volatile('otherdeath',1,chosen=True,enemy_in_range=True,scale=2),2)
    rejects('Settled opportunity cannot replay',lambda:b.settle_volatile('otherdeath',2,chosen=True,enemy_in_range=True,scale=2))
    b=board();e=put(b,entity());e.hp=3;e.temp_hp=10
    check('Injection spends direct normal HP',b.injection_cost('e',1,2),1)
    check('Injection leaves tempHP and death history unchanged',(e.temp_hp,len(e.destruction_history)),(10,0))
    rejects('Injection must leave positive HP',lambda:b.injection_cost('e',1,1))

    b=board();f=put(b,entity('f','field'))
    rejects('Objectless Field cannot take machine damage',lambda:b.damage('f',1,2,event_id='x'))
    rejects('Objectless Field cannot receive Field Repair',lambda:b.field_repair('f',1,Wallet(1),2))
    rejects('Objectless Field cannot route Dissonance',lambda:b.disable('f',1,Wallet(),dissonance=2,amount=1,use_key='route/sr1'))
    check('Objectless Field still occupies a slot',b.occupied('owner','deployable',1),1)
    b.end('f');check('Field ending releases slot with no debris',(b.occupied('owner','deployable',1),len(b.destructions)),(0,0))
    b=board();c=put(b,entity('c','elemental',source_id='shaman.hero.theurgist.summon-cinderflame'))
    result,d=b.damage('c',1,999,event_id='cdeath')
    check('Cinder disappears but records destruction',result['disappeared'],True)
    check('Cinder death burst independent of command ledger',b.cinder_destruction('cdeath')['maximumEnemyTargets'],3)
    rejects('Cinder burst resolves once',lambda:b.cinder_destruction('cdeath'))
    b=board();c=put(b,entity('c','elemental',source_id='shaman.hero.theurgist.summon-cinderflame'));b.end('c')
    check('Cinder dismissal no death burst event',len(b.destructions),0)

    b=board();wall=put(b,entity('wall',maximum=3,source_id='tinker.hero.artificer.magnetic-wall',temp_hp=1))
    r=DamageRoot('shot','ally',12,'piercing',attack_hit=True,critical=True);r.defend(r.original_id,flat_reductions=(2,))
    w=Wallet()
    bid=magnetic_wall_intercept(b,'wall',r,1,w,scale=2,modifier=2,ranged_weapon_hit=True,ally_within_five=True,wall_in_line=True)
    check('Magnetic Wall fixed post-defense transfer',(r.branch(r.original_id).amount,r.branch(bid).amount,w.reaction),(6,4,False))
    check('Wall branch exact flags/no attack riders',(r.branch(bid).flags,r.branch(bid).attack_hit,r.branch(bid).critical),(frozenset({'noSecondMitigation','noRetransfer'}),False,False))
    rejects('Wall branch cannot get second mitigation',lambda:r.prevent(bid,1,'extra'))
    event,d=resolve_entity_branch(b,r,bid,1,enemy_caused=True,hostile_source='enemy')
    check('Wall temp then HP destruction, hostile not sacrifice',(wall.hp,wall.temp_hp,d.enemy_caused,d.deliberate_sacrifice),(0,0,True,False))
    check('Transferred damage not an enemy attack hit on wall',d.enemy_hit,False)
    check('Magnetic destruction can trigger Volatile',b.settle_volatile(d.event_id,1,chosen=True,enemy_in_range=True,scale=2),2)
    check('Magnetic destruction keeps useful debris',d.material_available,True)
    b=board();wall=put(b,entity('wall',source_id='tinker.hero.artificer.magnetic-wall'))
    r=DamageRoot('wrong','ally',10,'fire');r.defend(r.original_id);w=Wallet()
    rejects('Magnetic Wall rejects non-hit without spending Reaction',lambda:magnetic_wall_intercept(b,'wall',r,1,w,scale=1,modifier=2,ranged_weapon_hit=False,ally_within_five=True,wall_in_line=True))
    check('Invalid wall reaction preserves root and Reaction',(r.operation,w.reaction),(None,True))

    b=board();d1=put(b,entity('d1','drone'));d2=put(b,entity('d2','drone'))
    b.configure_drones('owner',level=13,mode='single',modules_by_asset={d1.asset_id:('a','b')})
    check('Single two-module configuration withdraws second without death',(d2.state,d2.unavailable,len(b.destructions)),('retracted',True,0))
    b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:('a',),d2.asset_id:('b',)})
    b.redeploy('d2',1)
    check('Returning owned second Drone keeps identity',(d2.instance_id,d2.state,d2.unavailable),('d2','deployed',False))
    rejects('Dual cannot have two modules per Drone',lambda:b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:('a','b'),d2.asset_id:('a',)}))
    rejects('Single two modules must be distinct',lambda:b.configure_drones('owner',level=13,mode='single',modules_by_asset={d1.asset_id:('a','a')}))
    rejects('Dual Protocol rejects both empty modules',lambda:b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:(),d2.asset_id:()}))
    rejects('Dual Protocol rejects one empty Drone',lambda:b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:(),d2.asset_id:('a',)}))
    rejects('Single level13 Protocol requires exactly two modules',lambda:b.configure_drones('owner',level=13,mode='single',modules_by_asset={d1.asset_id:('a',)}))
    check('Rejected module cardinalities preserve prior valid dual modules',(d1.modules,d2.modules),(('a',),('b',)))

    states=0
    for old_max in range(1,25):
        for old_hp in range(1,old_max+1):
            for new_max in (1,2,7,24):
                b=board();e=put(b,entity(maximum=old_max));e.hp=old_hp
                b.reconfigure('e',1,Wallet(1),source_id='tinker.engine[6]',new_maximum=new_max,new_ac=14,known=True,nonhealing=True,slot_count=1,damaging_profile=True)
                assert 1<=e.hp<=new_max and e.state=='deployed' and not e.destruction_history
                assert e.hp==max(1,old_hp*new_max//old_max)
                states+=1
    disposition=json.loads((ROOT/'data/playtest/device_lifecycle_bindings.json').read_text(encoding='utf-8'))
    result={'result':'PASS','status':disposition['status'],
            'reviewClosure':disposition.get('reviewClosure'),
            'scope':'74 class-source lifecycle roles plus3 frozen shared paragraphs; no full-card/game completeness claim',
            'checkCount':len(checks),'reconfigurationStates':states,'checks':checks}
    (ROOT/'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} device lifecycle checks and {states} reconfiguration states.')


if __name__=='__main__':main()
