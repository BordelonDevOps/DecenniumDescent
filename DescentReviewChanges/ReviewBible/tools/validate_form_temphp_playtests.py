"""Adversarial contract checks, not full card/rider or human balance tests."""
from pathlib import Path
import json
from copy import deepcopy
from dataclasses import replace
from form_temphp_playtest_rules import *
from core_playtest_rules import LifeState
from creature_lifecycle_playtest_rules import CreatureWorld, Creature

checks=0
def check(value,label):
    global checks
    assert value,label
    checks+=1
def rejects(fn,label):
    try:fn()
    except SpellRuleError:check(True,label)
    else:raise AssertionError(label)

def grant(ident,amount,*,source='test',target='d',expiry=None,rest=0,deps=(),riders=()):
    return BufferGrant(ident,source,'d',target,amount,expiry,rest,deps,set(riders))

def state(level=20,circle='Moon',*,attuned=(),creatures=None):
    stats=DruidStats('d',level,6,4,4,4)
    ledger=BufferLedger(); cadence={'refrain':3,'rememberedSpell':'test-spell','dissonance':9}
    return stats,DruidState(stats,circle,ledger,cadence,attuned=attuned,creatures=creatures)

def main():
    global checks
    b=BufferLedger()
    b.offer(grant('old',8,expiry=ClockMarker(30),rest=None))
    b.offer(grant('small',7,expiry=ClockMarker(100),rest=None))
    check(b.current('d').grant_id=='old','Smaller grant cannot refresh')
    b.offer(grant('tie',8,expiry=ClockMarker(100),rest=None))
    check(b.current('d').expiry==ClockMarker(30),'Tie retains original deadline')
    rejects(lambda:b.offer(grant('tie',50)),'Rejected ID cannot later refill')
    b.offer(grant('bigger',9))
    check(b.grants['old'].state=='replaced' and b.amount('d')==9,'Only one active grant')
    b.end('d','depleted');check(b.amount('d')==0,'Old grant never reappears')
    b.offer(grant('zero',0));check('zero' not in b.grants,'Zero creates no grant identity')
    b.offer(grant('default',4));b.completed_long_rest('d',1)
    check(b.amount('d')==0,'Default ends at actual recipient LR')
    rejects(lambda:b.completed_long_rest('d',1),'No repeated rest reset')
    rejects(lambda:b.offer(grant('stale',5,rest=0)),'Stale recipient epoch rejected')
    b.offer(grant('fixed',5,expiry=ClockMarker(100),rest=None),50)
    b.completed_long_rest('d',2);check(b.amount('d')==5,'Explicit lifetime may outlast LR')
    b.expire(100);check(b.amount('d')==0,'Exact fixed endpoint')

    blood='crimson-agent.arch.veinweave-bloodshield'
    b=BufferLedger();b.offer(grant('unrelated',10))
    b.offer(grant('rejected-blood',10,source=blood,riders=('bloodshield-reaction',)))
    w=Wallet();rejects(lambda:b.consume_linked_reaction('d','rejected-blood',w,legal=True),'Rejected shield has no permission')
    check(w.reaction,'Invalid permission does not pay Reaction')
    b.offer(grant('blood',12,source=blood,riders=('bloodshield-reaction',)))
    b.consume_linked_reaction('d','blood',w,legal=True)
    check(not w.reaction and not b.current('d').riders,'One current linked Reaction')
    rejects(lambda:b.consume_linked_reaction('d','blood',Wallet(),legal=True),'No repeated linked use')
    b.offer(grant('blood2',13,source=blood,riders=('bloodshield-reaction',)))
    b.offer(grant('other',14));rejects(lambda:b.consume_linked_reaction('d','blood2',Wallet(),legal=True),'Replacement removes linked use')

    overflow='oracle.supplement.life.overflowing-light'
    for reason in ('replaced','depleted','dependency-ended','body-ended','long-rest'):
        b=BufferLedger();b.offer(grant('ol',3,source=overflow,expiry=ClockMarker(12),rest=None,riders=('overflowing-cleanse',)))
        check(not b.end('d',reason),'No false natural-expiry cleanse: '+reason)
        check(not b.expire(12),'No delayed cleanse after '+reason)
    b=BufferLedger();b.offer(grant('ol',3,source=overflow,expiry=ClockMarker(12),rest=None,riders=('overflowing-cleanse',)))
    rejects(lambda:b.end('d','natural-expiry',now=11),'Cannot fabricate early natural expiry')
    rejects(lambda:b.core_damage('d','late',LifeState(20,20,3),1,now=12),'Expired buffer cannot protect late event')
    check(not b.expire(11),'No early cleanse');events=b.expire(12)
    check(len(events)==1 and events[0]['chooseUpTo']==1,'One optional actual eligible cleanse')
    check(not b.expire(13),'No repeat cleanse')

    b=BufferLedger();b.offer(grant('program',10,source='tinker.hero.artificer.protective-programming',rest=None,deps=('hit1',)))
    life,events=b.core_damage('d','hit1',LifeState(20,20,10),3)
    check(life.hp==20 and life.temp_hp==7 and events['tempAbsorbed']==3,'Shield before one hit')
    b.end_dependency('hit1');check(b.amount('d')==0,'Programming remainder ends after that hit')
    b=BufferLedger();b.offer(grant('larger',20));b.offer(grant('program',10,rest=None,deps=('hit1',)))
    b.end_dependency('hit1');check(b.amount('d')==20,'Rejected one-hit shield cannot end winner')

    b=BufferLedger();b.offer(grant('shield',6))
    original=LifeState(30,8,6,wounds=(None,),stable=False,death_successes=0)
    out,e=b.core_damage('d','damage',original,4)
    check(out.hp==8 and out.wounds==(None,) and b.amount('d')==2,'THP mitigates without healing/Wound removal')
    check(original.temp_hp==6,'Core input immutable')
    rejects(lambda:b.core_damage('d','damage',out,4),'No duplicate canonical damage')
    rejects(lambda:b.core_damage('d','other',replace(out,temp_hp=100),4),'Divergent scalar HP projection rejected')
    b=BufferLedger();b.offer(grant('dying',10))
    out,e=b.core_damage('d','dmg',LifeState(20,0,10,death_failures=1),5)
    check(out.hp==0 and not out.stable and out.death_failures==1,'Buffer cannot stabilize/reset dying')

    b=BufferLedger();b.offer(grant('old',3));w=Wallet()
    q=b.necrotic_affinity('d','necro',9,w,ClockMarker(12),legal=True)
    check(q['prevented']==4 and q['remainingDamage']==5 and not w.reaction,'After-resistance half prevention')
    out,e=b.core_damage('d','necro',LifeState(20,20,3),q['remainingDamage'])
    check(out.hp==18 and e['tempAbsorbed']==3,'Old shield protects remainder only')
    b.finish_necrotic_affinity('d','necro','new',0,living_holder=True)
    check(b.amount('d')==4 and out.hp==18,'New shield only after damage')
    rejects(lambda:b.necrotic_affinity('d','necro',9,Wallet(),ClockMarker(12),legal=True),'No repeat absorption')
    rejects(lambda:b.finish_necrotic_affinity('d','necro','new2',0,living_holder=True),'No repeat post-packet grant')
    b=BufferLedger();b.necrotic_affinity('d','one',1,Wallet(),ClockMarker(12),legal=True)
    b.core_damage('d','one',LifeState(20,20),1)
    check(b.finish_necrotic_affinity('d','one','no-grant',0,living_holder=True) is None and not b.grants,'One damage can pay without zero grant')
    b=BufferLedger();q=b.necrotic_affinity('d','fatal',100,Wallet(),ClockMarker(12),legal=True)
    out,e=b.core_damage('d','fatal',LifeState(20,1),q['remainingDamage'])
    check(out.dead,'Test actual instant death')
    b.finish_necrotic_affinity('d','fatal','corpse',0,living_holder=False)
    check(not b.grants,'No post-event corpse shield')

    check(blood_ritual_offers(7)=={'self':14,'eachEligibleAlly':7,'allyLifetimeSeconds':3600},'Blood Ritual uses own offer not winner')
    check(post_event_buffer_amount('paladin.supplement.oath-of-the-martyr-king.king-s-smite',99,eligible=True,scale=2,modifier=3)==5,'Smite actual half and cap')
    rejects(lambda:post_event_buffer_amount('v6-trait:soul-drain',8,eligible=False),'Actual ancestry anti-farm gate')
    check(one_character_area_targets([('d','body'),('d','spirit'),('ally','body2')])==['d','ally'],'One area deduplicates same body identity')
    check(not spirit_walk_position_eligible(is_spirit=True,is_attack=True,physical_target_required=False,native_eligible=True),'Spirit never attack target')
    check(not spirit_walk_position_eligible(is_spirit=True,is_attack=False,physical_target_required=True,native_eligible=True),'Physical-required effect excluded')
    check(spirit_walk_position_eligible(is_spirit=True,is_attack=False,physical_target_required=False,native_eligible=True),'Legal nonphysical area exposure')

    bear='druid.base.bear-form-tank';wolf='druid.base.wolf-form-striker';hawk='druid.base.hawk-form-scout'
    stats,d=state(10);d.buffers.offer(grant('large-shield',50));w=Wallet()
    entered=d.shift(stats,bear,'bear1',0,w,legal=True)
    check(d.shifts==4 and d.reserve==4 and not w.bonus_action,'Entry pays full20 reserve and shift/BA')
    check(d.buffers.current('d').grant_id=='large-shield','Failed comparison still consumes reserve')
    check(d.cadence=={'refrain':0,'rememberedSpell':None,'dissonance':9},'Only Refrain clears')
    before=(d.reserve,d.shifts);w=Wallet()
    rejects(lambda:d.shift(stats,bear,'repeat',1,w,legal=True),'Early identical form rejected')
    check(before==(d.reserve,d.shifts) and w.bonus_action,'Illegal identical shift costs nothing')
    d.cadence['refrain']=2;d.cadence['rememberedSpell']='again'
    d.natural_endpoint(stats,600,renew=True)
    check(d.current.instance_id=='bear1' and d.reserve==4 and d.shifts==3,'Renew same instance without refill')
    check(d.cadence['refrain']==2 and d.current.expiry==ClockMarker(1200),'Renew does not clear Refrain')
    rejects(lambda:d.natural_endpoint(stats,700,renew=True),'No early renew')
    d.revert(601,Wallet(),legal=True)
    check(d.cadence['refrain']==2 and d.shifts==3 and d.buffers.amount('d')==50,'Revert preserves unrelated shield and cadence')
    d.shift(stats,bear,'bear2',602,Wallet(),legal=True)
    check(d.reserve==0,'New entry only remaining reserve offered')
    d.revert(603,Wallet(),legal=True);d.shift(stats,bear,'bear3',604,Wallet(),legal=True)
    check(d.reserve==0 and 'bear3:entry' not in d.buffers.grants,'Zero-reserve form still legal, no grant')
    rejects(lambda:d.shift(stats,wolf,'illegal',605,Wallet(),legal=False),'Illegal geometry does not mutate')

    stats,d=state(20);d.shift(stats,bear,'f',0,Wallet(),legal=True)
    check(d.shifts==8 and d.reserve==24,'Level20 free shifts do not refill finite benefits')
    d.natural_endpoint(stats,600,renew=True)
    check(d.reserve==24 and d.current.instance_id=='f','Level20 renewal preserves exact grant')
    check(d.finalize_damage_state(actual_hp=1,incapacitated=False,dead=False,unsupported=False) is None,'Actual instead1 retains form')
    result=d.finalize_damage_state(actual_hp=0,incapacitated=False,dead=False,unsupported=True)
    check(result['beginOrdinaryFall'] and not result['secondDamageResolution'] and not d.buffers.amount('d'),'Forced end/fall no second HP pool')
    stats,d=state();d.shift(stats,hawk,'h',0,Wallet(),legal=True)
    p=d.profile(stats,1,12,ac_components_certified=True)
    check(p['size']=='Tiny' and p['movement']=={'walk':10,'fly':60} and not p['canSpeak'],'Exact Hawk profile')
    check(p['mayCastDruidSpells'],'Beast Spells uses actual18 gate')
    rejects(lambda:d.profile(stats,1,20,ac_components_certified=False),'No unclassified melded AC')

    # Exact-source profile gates and an ordinary Action for all26 bodies.
    for index,(ident,p) in enumerate(PROFILES.items()):
        stats,d=state(20,p['circle'] or 'Moon',attuned=(ident,) if p['archAttunement'] else ())
        variant='air' if ident.endswith('elemental-shapeshifting') else 'ground' if ident.endswith('master-of-vermin') else None
        d.shift(stats,ident,'form'+str(index),0,Wallet(),legal=True,variant=variant)
        profile=d.profile(stats,0,12,ac_components_certified=True)
        check(profile['sourceId']==ident and profile['attack']['attack']==10,'Actual source profile '+ident)
        w=Wallet();attack=d.attack(stats,0,w,legal=True)
        check(w.actions==0 and not attack['unrelatedWeaponProcAuthorized'],'One natural Action '+ident)
    stats,d=state(10,'Moon')
    rejects(lambda:d.shift(stats,'druid.arch.dire-wolf','x',0,Wallet(),legal=True),'Arch level11 gate')
    stats,d=state(20,'Moon')
    rejects(lambda:d.shift(stats,'druid.arch.dire-wolf','x',0,Wallet(),legal=True),'Attunement required')
    rejects(lambda:d.shift(stats,'druid.hero.storm.tempest-raptor','x',0,Wallet(),legal=True),'No cross-Circle Hero form')

    moon='druid.hero.moon.mooncursed';stats,d=state();d.shift(stats,moon,'moon',0,Wallet(),legal=True)
    d.reserve=9;d.buffers.offer(grant('ally-big',20,target='a'))
    out=d.mooncursed_howl(stats,1,Wallet(),['a','b','c'],12,['a1','b1','c1'],legal=True)
    check(d.reserve==0 and out[0]['amount']==9 and not out[0]['accepted'] and out[1:]==[None,None],'Sequential9/0/0, rejected offer still pays')
    check(d.surges==5 and 'howl' in d.current.spent,'One shared mode opportunity')
    rejects(lambda:d.special(stats,1,Wallet(),'howl',legal=True),'Enemy mode cannot reuse same Howl')
    d.shift(stats,wolf,'w',2,Wallet(),legal=True);d.shift(stats,moon,'moon2',3,Wallet(),legal=True)
    d.mooncursed_howl(stats,3,Wallet(),['b'],5,['empty'],legal=True)
    check(d.surges==4 and 'empty' not in d.buffers.grants,'Exhausted legal Howl pays but creates no zero grant')
    stats,d=state();d.shift(stats,moon,'moon',0,Wallet(),legal=True)
    d.mooncursed_howl(stats,1,Wallet(),['a'],8,['ally'],legal=True)
    d.revert(2,Wallet(),legal=True);check(d.buffers.amount('a')==8,'Mooncursed ally shield survives reversion')
    d.buffers.completed_long_rest('a',1);check(d.buffers.amount('a')==0,'Mooncursed uses recipient default lifetime')

    earth='druid.arch.earth-warden-dire-bear';stats,d=state(attuned=(earth,));d.regular_start(1,0,actual_regular_marker=True)
    d.shift(stats,earth,'earth',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'slam',legal=True)
    d.shift(stats,wolf,'wolf',1,Wallet(),legal=True);d.shift(stats,earth,'earth2',2,Wallet(),legal=True)
    rejects(lambda:d.special(stats,2,Wallet(),'slam',legal=True),'Slam recharge survives shifts')
    rejects(lambda:d.regular_start(2,6,actual_regular_marker=False),'Extra turn cannot tick recharge')
    d.regular_start(2,6,actual_regular_marker=True);rejects(lambda:d.special(stats,6,Wallet(),'slam',legal=True),'Recharge2 not ready next start')
    d.regular_start(3,12,actual_regular_marker=True);d.special(stats,12,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==4,'Slam ready at second later regular start')

    frost='druid.hero.winterfang.frost-wyrmling';stats,d=state(circle='Winterfang')
    d.shift(stats,frost,'frost',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'breath',legal=True)
    d.shift(stats,wolf,'wolf',1,Wallet(),legal=True);d.shift(stats,frost,'frost2',2,Wallet(),legal=True)
    rejects(lambda:d.special(stats,2,Wallet(),'breath',legal=True),'Breath remains spent across new instances')
    d.revert(3,Wallet(),legal=True);d.recharge_clock.leave_initiative(3)
    d.completed_short_rest(1,actual_completed=True,now=3603)
    d.shift(stats,frost,'frost3',3603,Wallet(),legal=True);d.special(stats,3603,Wallet(),'breath',legal=True)
    check(d.rest_uses['short:'+frost]==1,'Actual SR restores source use only')
    rejects(lambda:d.completed_short_rest(1,actual_completed=True,now=3603),'No fabricated repeated SR')

    elemental='druid.hero.moon.elemental-shapeshifting';stats,d=state()
    d.shift(stats,elemental,'air',0,Wallet(),legal=True,variant='air')
    d.natural_endpoint(stats,600,renew=True)
    check(d.rest_uses['long:elemental']==1,'Same Elemental renew does not pay entry use')
    d.shift(stats,elemental,'water',601,Wallet(),legal=True,variant='water')
    check(d.attack(stats,601,Wallet(),legal=True)['profile']['damageType']=='cold','Subtype identity sets actual damage')
    rejects(lambda:d.shift(stats,elemental,'fire',602,Wallet(),legal=True,variant='fire'),'Two Elemental entries remain finite at20')
    d.revert(603,Wallet(),legal=True);d.recharge_clock.leave_initiative(603)
    d.completed_long_rest(stats,1,attuned=(),actual_completed=True,now=29403)
    check(d.reserve==44 and d.surges==6 and d.instances['water'].state=='voluntary-reversion','Actual LR refills reserve without recreating ended form')

    brood='druid.hero.rotshaper.insect-broodmother';world=CreatureWorld();stats,d=state(circle='Rotshaper',creatures=world)
    out=d.shift(stats,brood,'brood',0,Wallet(),legal=True,spawn=True,spawn_legal=False)
    check(out['spawnPayment'] is None and d.surges==6,'Invalid optional spawn does not undo form or pay')
    rejects(lambda:d.special(stats,1,Wallet(),'spawn',legal=True),'No later spawn window')
    d.special(stats,1,Wallet(),'negate-critical',legal=True)
    check(d.surges==5,'Separate crit-negation still available')
    d.shift(stats,wolf,'wolf',2,Wallet(),legal=True)
    out=d.shift(stats,brood,'brood2',3,Wallet(),legal=True,spawn=True,spawn_legal=True)
    check(out['spawnPayment']['formSurgePaid'] and d.surges==4,'Valid entry spawn pays exactly one Surge')
    c=Creature('swarm','d','d','druid',brood,'swarm','finite',20,20,20,15,30,expiry=ClockMarker(63),parent_form='brood2')
    independent=replace(c,instance_id='independent',parent_form=None)
    world.creatures['swarm']=c;world.creatures['independent']=independent
    d.natural_endpoint(stats,603,renew=True)
    check(c.expiry==ClockMarker(63),'Renewal never extends independent creature deadline')
    d.revert(604,Wallet(),legal=True)
    check(c.state=='ended' and independent.state=='active','Parent ending only removes its own dependent swarm')

    # The same owner recharge clock continues outside combat and through rest.
    stats,d=state(attuned=(earth,));d.regular_start(1,0,actual_regular_marker=True)
    d.shift(stats,earth,'clock-earth',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'slam',legal=True)
    d.recharge_clock.leave_initiative(0);d.recharge_clock.advance_outside(6)
    rejects(lambda:d.special(stats,6,Wallet(),'slam',legal=True),'Only one downtime tick after6 seconds')
    d.recharge_clock.advance_outside(12);d.special(stats,12,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==4,'Twelve actual downtime seconds mature Recharge2')
    d.recharge_clock.enter_initiative(18);ticks=d.recharge_clock.ticks
    d.regular_start(2,18,actual_regular_marker=True)
    check(d.recharge_clock.ticks==ticks,'Initiative entry cannot double-count same due tick')
    d.regular_start(3,19,actual_regular_marker=True)
    check(d.recharge_clock.ticks==ticks,'Reordered start before canonical interval cannot fabricate tick')
    rejects(lambda:d.recharge_clock.advance_outside(24),'No parallel elapsed clock inside initiative')
    rejects(lambda:d.recharge_clock.leave_initiative(17),'No recharge time reversal')
    d.regular_start(4,24,actual_regular_marker=True);d.special(stats,24,Wallet(),'slam',legal=True)
    d.revert(25,Wallet(),legal=True);d.recharge_clock.leave_initiative(25)
    d.completed_short_rest(1,actual_completed=True,now=3625)
    d.shift(stats,earth,'after-sr',3625,Wallet(),legal=True);d.special(stats,3625,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==d.recharge_clock.ticks+2,'Real SR elapsed time matured previous recharge')
    d.revert(3626,Wallet(),legal=True)
    d.completed_long_rest(stats,1,attuned=(earth,),actual_completed=True,now=32426)
    d.shift(stats,earth,'after-lr',32426,Wallet(),legal=True);d.special(stats,32426,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==d.recharge_clock.ticks+2,'Real LR elapsed time matured previous recharge')
    stats,phased=state(attuned=(earth,));phased.regular_start(1,5,actual_regular_marker=True)
    phased.shift(stats,earth,'phase-earth',5,Wallet(),legal=True);phased.special(stats,5,Wallet(),'slam',legal=True)
    phased.recharge_clock.leave_initiative(5);phased.recharge_clock.advance_outside(11)
    rejects(lambda:phased.special(stats,11,Wallet(),'slam',legal=True),'Nonzero owner phase: one tick at11 after use5')
    phased.recharge_clock.advance_outside(17);phased.special(stats,17,Wallet(),'slam',legal=True)
    check(phased.recharges[earth]==4,'Nonzero owner phase reaches second tick at17, not hardcoded12')

    # Global instance IDs prevent another owner's form cleanup touching summons.
    stats,d=state();d.shift(stats,wolf,'shared-name',0,Wallet(),legal=True)
    other_stats=DruidStats('other',20,6,4,4,4)
    other=DruidState(other_stats,'Moon',d.buffers,{'refrain':0,'rememberedSpell':None,'dissonance':0})
    w=Wallet();rejects(lambda:other.shift(other_stats,wolf,'shared-name',0,w,legal=True),'Cross-owner form ID collision rejected')
    check(w.bonus_action and other.current is None,'Collision preflight is unpaid and atomic')
    other.shift(other_stats,wolf,'other-unique',0,w,legal=True)
    check(other.current.instance_id=='other-unique' and d.current.instance_id=='shared-name','Two actual owners retain distinct form identities')

    # Enumerate competing values and damage: winner never stacks and conservation.
    scenarios=0
    for old in range(9):
        for new in range(9):
            for damage in range(13):
                b=BufferLedger()
                if old:b.offer(grant('old',old))
                b.offer(grant('new',new))
                winner=max(old,new)
                out,e=b.core_damage('d','packet',LifeState(100,100,winner),damage)
                assert b.amount('d')==max(0,winner-damage)
                assert out.hp==100-max(0,damage-winner)
                if old and old>=new and damage<old:assert b.current('d').grant_id=='old'
                scenarios+=1
    check(scenarios==1053,'Arbitration/damage conservation scenarios')
    report={'status':'PASS','checks':checks,'arbitrationDamageScenarios':scenarios,
            'formProfiles':len(PROFILES),'reviewStatus':'IMPLEMENTED; GPT implementation review pending',
            'scope':'Selected grant/form interface only; not full source cards, item/weapon taxonomy, full runtime or human balance.'}
    out=Path(__file__).resolve().parents[1]/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json'
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
if __name__=='__main__':main()
