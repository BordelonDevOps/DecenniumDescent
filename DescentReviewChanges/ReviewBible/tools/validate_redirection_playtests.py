from pathlib import Path
import json
from copy import deepcopy
from redirection_playtest_rules import *
from core_playtest_rules import LifeState
from healing_playtest_rules import healing_packet
from control_playtest_rules import absolute_deadline,turn_end_deadline
ROOT=Path(__file__).resolve().parents[1]
BB='crimson-agent.hero.bloodweaver.bloodbond'
VT='crimson-agent.hero.bloodweaver.veinlock-tether'
BREATH='monk.hero.enlightened-master.shared-breath'
TISSUE='warrior.hero.wardborn.guardian-tissue'
AEGIS='warrior.hero.wardborn.aegis-incarnate'
STANCE='paladin.base.protective-stance'
EMERGENCY='tinker.arch.emergency-protocols'

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected);checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    def raw(name,amount=20,**kw):return DamageRoot(name,'ally',amount,'fire',**kw)
    def defended(name,amount=20,**kw):
        r=raw(name,amount,**kw);r.defend(r.original_id);return r
    def living_all(r,states=None,**kw):
        states=states or {}
        for bid,b in r.branches.items():
            if b.stage=='raw':r.defend(bid)
            r.resolve_living(bid,states.get(b.target,LifeState(100,100)),**kw)
    r=raw('pre',40,attack_hit=True,critical=True)
    r.transfer(BB,'agent',{'agent':10})
    ids=list(r.branches);r.defend(ids[0],resistant=True);r.defend(ids[1],resistant=True)
    check('Quarter sharing precedes both recipients resistance',[b.amount for b in r.branches.values()],[15,5])
    check('Transferred portion loses attack-critical identity',(r.branch(ids[1]).attack_hit,r.branch(ids[1]).critical),(False,False))
    check('Original portion preserves hit and critical identity',(r.branch(ids[0]).attack_hit,r.branch(ids[0]).critical),(True,True))
    rejects('Pretransfer locks retained original against later transfer',lambda:r.transfer(BREATH,'monk',{'monk':1}))
    rejects('Quarter reaction cannot arbitrarily choose smaller share',lambda:raw('bad-quarter',40).transfer(BB,'agent',{'agent':5}))
    a=raw('pre-dr',40);a.transfer(BB,'agent',{'agent':10})
    a.defend(a.original_id,flat_reductions=(12,5),resistant=True)
    check('Strongest original flat reduction applies to retained share only',a.branch(a.original_id).amount,9)
    a.defend('pre-dr/transfer/1',flat_reductions=(2,),resistant=True)
    a.prevent('pre-dr/transfer/1',3,'guardian')
    check('Premitigation transfer accepts recipient defenses and pure prevention',a.branch('pre-dr/transfer/1').amount,1)
    r=raw('post',30);r.defend(r.original_id,flat_reductions=(5,3),resistant=True)
    check('Flat strongest then resistance floor',r.branch(r.original_id).amount,12)
    r.transfer(BREATH,'monk',{'monk':5},scale=2,modifier=3)
    check('Postdefense split conserves remaining amount',[b.amount for b in r.branches.values()],[7,5])
    child='post/transfer/1'
    rejects('Postdefense child cannot defend again',lambda:r.defend(child,immune=True))
    rejects('Postdefense child cannot use further pure prevention',lambda:r.prevent(child,5,'bloom'))
    rejects('Postsplit original cannot use late pure prevention',lambda:r.prevent(r.original_id,1,'late'))
    after,event=r.resolve_living(child,LifeState(20,20,temp_hp=5))
    check('Unmitigated transfer still consumes temporary HP',(after.hp,after.temp_hp,event['actualDamageDealt']),(20,0,5))
    check('TemporaryHP absorption does not erase concentration packet',event['concentrationDamage'],5)
    rejects('Root totals await every terminal branch',lambda:r.total())
    r.resolve_living(r.original_id,LifeState(20,20))
    check('Physical total counts final recipients only',r.total(),12)
    rejects('Final branch cannot resolve twice',lambda:r.resolve_living(child,after))
    r=defended('critical',6,attack_hit=True,critical=True)
    r.transfer(BREATH,'monk',{'monk':6},scale=3,modifier=3)
    after,event=r.resolve_living('critical/transfer/1',LifeState(20,0))
    check('Transferred critical damage causes one death failure',(after.death_failures,event['criticalHit']),(1,False))
    after,event=r.resolve_living(r.original_id,LifeState(20,20))
    check('Full transfer retains original hit without positive damage',(event['attackHit'],event['positiveDamageEvent']),(True,False))
    r=defended('aegis',50)
    r.transfer(AEGIS,'warrior',{'warrior':25})
    after,event=r.resolve_living('aegis/transfer/1',LifeState(10,2),ritual_ward=True)
    check('Aegis still transfers lethal packet but Ward can prevent death',(after.dead,after.hp,event['instantDeath'],event['wardUsed']),(False,1,True,True))
    check('Survival replacement does not overcount actualHP damage',event['actualDamageDealt'],1)
    r=defended('wounds',12);r.transfer(BREATH,'monk',{'monk':7},scale=3,modifier=4)
    after,event=r.resolve_living('wounds/transfer/1',LifeState(20,5),wound_natural=20)
    check('Ordinary transfer dropping positiveHP to0 invokes Wound save',(after.hp,event['woundSaves']),(0,1))
    rejects('Caller cannot replace the branch critical identity',
            lambda:r.resolve_living(r.original_id,LifeState(20,20),critical=True))
    r=defended('no-riders',10);r.transfer(BREATH,'monk',{'monk':3},modifier=2)
    rejects('Transferred branch rejects attack maiming rider',lambda:r.resolve_living('no-riders/transfer/1',LifeState(20,20),maiming=True))
    ledger=PaladinRoundLedger('paladin',1)
    r=defended('stance-small',3,attack_hit=True)
    r.transfer(STANCE,'paladin',{'paladin':3},scale=4,modifier=4,paladin_ledger=ledger)
    check('Protective Stance cannot create nonexistent excess damage',r.operation['amount'],3)
    check('Shared Paladin ledger records one operation',len(ledger.events),1)
    r2=defended('second',5);snapshot=deepcopy(r2.branches)
    rejects('Second ordinary Paladin event rejected',lambda:r2.transfer(STANCE,'paladin',{'paladin':2},paladin_ledger=ledger))
    check('Failed shared allowance leaves root unchanged',r2.branches,snapshot)
    check('Failed shared allowance does not add ledger event',len(ledger.events),1)
    r3=defended('other-owner',5)
    r3.transfer(STANCE,'other-paladin',{'other-paladin':2},paladin_ledger=PaladinRoundLedger('other-paladin',1))
    check('Different Paladin keeps independent round allowance',r3.operation['owner'],'other-paladin')
    rejects('Different owner cannot transfer already split root',lambda:r3.transfer(BREATH,'monk',{'monk':1}))
    r=defended('zero-auto',1)
    check('Automatic rounded0 share creates no operation',r.transfer(AEGIS,'warrior',{}),None)
    check('Automatic0 leaves root unclaimed',r.operation,None)
    rejects('Optional0 transfer cannot activate',lambda:defended('zero-opt',5).transfer(BREATH,'monk',{}))
    r=defended('multi',12);ledger=PaladinRoundLedger('paladin',2)
    r.transfer(BURDEN,'paladin',{'friend-A':3,'friend-B':5},level=10,modifier=2,paladin_ledger=ledger)
    check('Burden is one multi-recipient operation',[b.amount for b in r.branches.values()],[4,3,5])
    living_all(r)
    check('Burden physical total includes all branches',r.total(),12)
    check('Burden healing consumer excludes prohibited branches',r.total('healing'),4)
    check('Burden resource consumer excludes prohibited branches',r.total('resource',resource='RP'),4)
    check('Source target predicate still filters final recipients',r.total(qualified_targets={'ally'}),4)
    rejects('Native self-absorption rider cannot use damage sent to another ally',
            lambda:native_transfer_temp_hp(r,'multi/transfer/1',source=P+'oath-of-the-chain.unbroken-covenant',scale=2,modifier=2,level=10))
    rejects('Paladin ledger cannot accept unrelated transfer source',
            lambda:PaladinRoundLedger('paladin',3).record('not-paladin',BREATH,2,'ally',crown_active=False,level=10,modifier=2))
    r=defended('flags',9);r.transfer(TISSUE,'warrior',{'warrior':3})
    living_all(r)
    check('Warrior transfer bans BT only',r.total('resource',resource='BT'),6)
    check('Warrior transfer does not invent universal resource ban',r.total('resource',resource='Ki'),9)
    r=defended('pal-flags',8);ledger=PaladinRoundLedger('paladin',3)
    r.transfer(P+'oath-of-the-martyr-king.king-s-smite','paladin',{'paladin':5},paladin_ledger=ledger)
    living_all(r)
    check('Paladin reflection ban does not suppress all retaliation',(r.total('reflection'),r.total('retaliation')),(3,8))
    check('Paladin generic engine does not forbid healing generation',r.total('healing'),8)
    r=defended('native',8);ledger=PaladinRoundLedger('paladin',4)
    r.transfer(STANCE,'paladin',{'paladin':6},scale=2,modifier=4,paladin_ledger=ledger)
    living_all(r)
    check('Protective Stance suppresses generic damage-generated healing',r.total('healing'),2)
    check('Unbroken Covenant triggers on redirection despite noDamageTriggers',
          native_transfer_temp_hp(r,'native/transfer/1',source=P+'oath-of-the-chain.unbroken-covenant',scale=2,modifier=4,level=10),3)
    check('Unrelated later healing of recipient remains legal',healing_packet(LifeState(20,10),5)['actualHpGained'],5)
    ledger=PaladinRoundLedger('paladin',5)
    opts=dict(crown_active=True,level=10,modifier=2)
    ledger.record('c1',CROWN,6,'same-ally',**opts)
    ledger.record('c2',CROWN,6,'same-ally',**opts)
    check('Crown permits two different events for same selected ally',len(ledger.events),2)
    check('Crown healing floors per event then uses cumulative cap',
          (ledger.crown_heal('c1',5,scale=2,modifier=2),ledger.crown_heal('c2',6,scale=2,modifier=2)),(2,2))
    rejects('Crown third event rejected',lambda:ledger.record('c3',CROWN,1,'ally',**opts))
    rejects('Crown heal cannot be settled twice',lambda:ledger.crown_heal('c1',5,scale=2,modifier=2))
    ledger=PaladinRoundLedger('paladin',6)
    ledger.record('earlier',STANCE,2,'ally',crown_active=False,level=10,modifier=2)
    ledger.record('later',CROWN,8,'ally',**opts)
    check('Midround Crown activation preserves previous ordinary use',len(ledger.events),2)
    rejects('Crown activation cannot reset shared event history',lambda:ledger.record('extra',CROWN,1,'ally',**opts))
    ledger=PaladinRoundLedger('paladin',7)
    ledger.record('c-first',CROWN,2,'ally',**opts)
    ledger.record('o-second',STANCE,2,'ally',**opts)
    check('One Crown plus one ordinary allowed with Crown active in either order',len(ledger.events),2)
    ledger=PaladinRoundLedger('paladin',8)
    ledger.record('amount',CROWN,11,'ally',**opts)
    rejects('Crown amount cap independent of remaining event slot',lambda:ledger.record('too-much',CROWN,2,'ally',**opts))
    check('Failed amount cap leaves one event',len(ledger.events),1)
    ledger=PaladinRoundLedger('paladin',9)
    ledger.record('blocked',CROWN,8,'ally',**opts)
    nominal=ledger.crown_heal('blocked',8,scale=2,modifier=2)
    check('Blocked Crown heal yields0actual',healing_packet(LifeState(20,1),nominal,hp_gain_prohibited=True)['actualHpGained'],0)
    check('Blocked Crown healing consumes nominal cap',ledger.crown_heal_used['ally'],4)
    ledger=PaladinRoundLedger('paladin',10)
    r=defended('final-first',5);r.transfer(FINAL,'paladin',{'paladin':5},paladin_ledger=ledger)
    rejects('Final Stand constrained to one shared event that round',lambda:defended('final-second',4).transfer(FINAL,'paladin',{'paladin':4},paladin_ledger=ledger))
    check('Final Stand is an automatic profile',PROFILES[FINAL].automatic,True)
    r=defended('bloom-first',6);pool=BloomPool('bloom','ally',15,absolute_deadline(60))
    pool.absorb(r,r.original_id,0,target_next_end=turn_end_deadline(6))
    check('Bloom pool persists across small packet',(pool.remaining,pool.ended),(9,False))
    r=defended('bloom-second',12);pool.absorb(r,r.original_id,1,target_next_end=turn_end_deadline(6))
    check('Bloom depletion leaves remainder and starts rider',(r.branch(r.original_id).amount,pool.remaining,pool.ended,pool.rider_deadline),(3,0,True,turn_end_deadline(6)))
    pool=BloomPool('suppressed','ally',5,absolute_deadline(60));r=defended('suppressed',5)
    check('Suppression neither consumes nor ends Bloom',pool.absorb(r,r.original_id,2,target_next_end=turn_end_deadline(6),suppressed=True),0)
    check('Suppressed Bloom retains full capacity',(pool.remaining,pool.ended),(5,False))
    pool.absorb(r,r.original_id,70,target_next_end=turn_end_deadline(66),suppressed=True)
    check('Late observation preserves expiry-based rider deadline',(pool.ended,pool.rider_deadline),(True,turn_end_deadline(66)))
    pool=BloomPool('skip','monk',8,absolute_deadline(60));r=defended('skip-bloom',10)
    r.transfer(BREATH,'monk',{'monk':4},modifier=3)
    rejects('Unmitigated transfer cannot spend recipient Bloom',lambda:pool.absorb(r,'skip-bloom/transfer/1',1,target_next_end=turn_end_deadline(6)))
    check('Rejected Bloom attempt preserves finite pool',pool.remaining,8)
    attack=AttackRetarget('attack','ally');attack.retarget('guardian')
    check('Guardian uses original roll against own AC',attack.resolve(12,4,19)['hit'],False)
    rejects('Attack cannot bounce to another Guardian',lambda:attack.retarget('second-guardian'))
    rejects('Original attack cannot reroll on retarget',lambda:attack.resolve(20,4,19))
    rejects('Counter must wait for full original attack resolution',lambda:attack.guardian_counter(triggering_attack_fully_resolved=False,in_reach=True,actor_can_attack=True))
    flags=attack.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True)
    check('Missed incoming attack still permits single legal counter','noFreeAttackGeneration' in flags,True)
    rejects('Counter opportunity cannot replay',lambda:attack.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True))
    attack2=AttackRetarget('counter-parent','ally');attack2.retarget('guardian');attack2.resolve(10,5,12)
    check('A free counter cannot manufacture another free counter',
          attack2.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True,parent_flags=flags),None)
    attack3=AttackRetarget('unrelated-flags','ally');attack3.retarget('guardian');attack3.resolve(12,4,18)
    counter_flags=attack3.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True,
                                         parent_flags=frozenset({'noResourceGeneration','noHealingGeneration','noReflection'}))
    check('New Guardian attack drops unrelated incoming restrictions',
          counter_flags,frozenset({'noFreeAttackGeneration','noActionGeneration'}))
    attack=AttackRetarget('retarget-then-transfer','ally');attack.retarget('guardian')
    result=attack.resolve(20,3,20)
    r=DamageRoot('after-retarget',result['targetId'],10,'slashing',attack_hit=result['hit'],critical=result['critical'])
    r.defend(r.original_id);r.transfer(BREATH,'monk',{'monk':4},modifier=3)
    check('Attack retarget leaves later transfer opportunity intact',r.operation['amount'],4)
    r=defended('palm',9,attack_hit=True,melee_attack=True)
    counter=redirecting_palm(r,r.original_id,3,'attacker',second_enemy_id='second',new_root_id='palm-counter')
    check('Palm prevents floorhalf and caps separate force packet',(r.branch(r.original_id).amount,counter.rolled_packet),(5,3))
    counter.defend(counter.original_id,resistant=True)
    check('Palm force counter accepts new recipient defenses',counter.branch(counter.original_id).amount,1)
    check('Palm counter is not an attack hit',counter.branch(counter.original_id).attack_hit,False)
    check('Palm new force root has no invented consumer bans',
          [permits_consumer(counter.branch(counter.original_id),c) for c in ('free-attack','copy','action','healing')],[True]*4)
    rejects('Palm force packet cannot recursively qualify as a melee attack',
            lambda:redirecting_palm(counter,counter.original_id,3,'second'))
    r=defended('palm-no-second',9,attack_hit=True,melee_attack=True)
    check('Palm reduction remains without a second enemy',redirecting_palm(r,r.original_id,3,'attacker'),None)
    check('Palm still reduced original damage',r.branch(r.original_id).amount,5)
    r=defended('palm-bad',9,attack_hit=True,melee_attack=True)
    rejects('Palm cannot send force back to original attacker',lambda:redirecting_palm(r,r.original_id,3,'attacker',second_enemy_id='attacker',new_root_id='bad-counter'))
    check('Invalid counter target does not consume prevention',r.branch(r.original_id).amount,9)
    rejects('Ranged attack cannot activate Palm',lambda:redirecting_palm(defended('palm-ranged',9,attack_hit=True),'palm-ranged/original',3,'attacker'))
    r=defended('drone',10,attack_hit=True);r.transfer(EMERGENCY,'tinker',{'drone':6},scale=2,modifier=4)
    after,event=r.resolve_device('drone/transfer/1',DeviceState(10,3,temp_hp=1))
    check('Emergency drone destruction uses device consequences',(after.hp,after.destroyed,event['actualDamageDealt'],event['woundSaves'],event['deathFailuresAdded']),(0,True,4,0,0))
    check('Device transfer does not manufacture an enemy attack hit',event['attackHit'],False)
    check('Emergency drone transfer suppresses retaliation consumer',permits_consumer(r.branch('drone/transfer/1'),'retaliation'),False)
    rejects('Destroyed drone cannot receive another functional packet',lambda:device_damage(after,1))
    rejects('False positiveHP destroyed device rejected',lambda:DeviceState(10,1,destroyed=True))
    r=raw('stage-precedence',20)
    r.transfer(BB,'agent',{'agent':5})
    r.defend(r.original_id)
    rejects('Earlier raw transfer preempts later mandatory Aegis',lambda:r.transfer(AEGIS,'warrior',{'warrior':7}))
    check('Stage arbitration never consumes hypothetical defender prevention',r.branch(r.original_id).amount,15)
    # Independent conservation/oracle formula coverage, including floor boundaries.
    states=0
    for amount in range(0,65):
      for source,denom in ((BB,4),(TISSUE,3),(AEGIS,2)):
       chosen=amount//denom
       check_amount=transfer_limit(source,amount)
       assert check_amount==chosen
       if not chosen:continue
       r=raw('matrix',amount) if source==BB else defended('matrix',amount)
       r.transfer(source,'protector',{'protector':chosen})
       assert sum(b.amount for b in r.branches.values())==amount
       living_all(r)
       assert r.total()==amount
       states+=1
    report={'status':'PASS','reviewStatus':'REVIEWED / reference-VALIDATED; bounded39-source interface plus2Tinker engine passages',
            'scope':'Bounded39-source stage, branch flags, transfer arithmetic, per-owner Paladin/Crown budget, retarget, finite Bloom/Palm and Tinker damage interface. Not full feature execution, all-source defense order, device repair lifecycle or balance.',
            'checkCount':len(checks),'conservationStates':states,'checks':checks}
    (ROOT/'docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} redirection checks and {states} transfer conservation states; bounded GPT closure recorded.')
if __name__=='__main__':main()
