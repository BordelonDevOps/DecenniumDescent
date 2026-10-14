"""Adversarial reference checks for eight full feat candidates; no promotion."""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import hashlib
import json
from buffer_feat_playtest_rules import FeatWorld, FeatStats, FEATS, Kit, Rations
from device_lifecycle_playtest_rules import Wallet
from core_playtest_rules import LifeState, heal, stabilize
from form_temphp_playtest_rules import BufferGrant
from healing_playtest_rules import HealingReduction, healing_packet, HealingChain, ExcessLedger
from spell_playtest_rules import SpellRuleError
from control_playtest_rules import ClockMarker, turn_end_deadline

ROOT = Path(__file__).resolve().parents[1]
checks = []
matrix = 0


def check(name, value):
    if not value: raise AssertionError(name)
    checks.append(name)


def rejects(name, function):
    try: function()
    except SpellRuleError: checks.append(name); return
    raise AssertionError('Expected rejection: '+name)


def world(feats=FEATS, owners=('a',), stats=None):
    w = FeatWorld()
    s = stats or FeatStats(8, 3, 14, 2, 14, True, True, {'mage:INT':15})
    for owner in owners:
        w.register(owner, s)
        for feat in sorted(feats):
            w.acquire(owner, feat, owner+':acquire:'+feat, legal_selection=True,
                      dc_source='mage:INT' if feat == 'soul_cage' else None)
    return w


def strong(w, target, amount=99, ident='strong'):
    w.buffers.offer(BufferGrant(ident, 'external', target, target, amount, rest_epoch=w.epoch(target)))


def cooking(w, owner='a', attempt='r1', count=3, now=0):
    inv = Rations('inventory:'+owner, count)
    w.start_cooking(owner, attempt, count, now, legal_rest_activity=True, utensils=True)
    ids = tuple(owner+':'+attempt+':food:'+str(i) for i in range(count))
    w.finish_cooking(owner, attempt, inv, ids, now+3600, uninterrupted=True)
    return inv, ids


def drain(w, event='h1', root='s1', window='round:1', life=None, damage=12, **options):
    w.select_drain('a', root, window, 'foe', eligible_before_damage=True)
    return w.drain(event, 'a', root, window, 'foe', life or LifeState(20,5), damage,
                   own_spell_damage=True, hostile_not_farmed=True, **options)


def death(w, event, body=None, owner='a', **options):
    return w.death_checkpoint(owner, event, body or event, actual_new_death_checkpoint=True,
             qualifying_hostile_soul=options.pop('qualifying_hostile_soul',True),
             legal_range_perception_line=options.pop('legal_range_perception_line',True), **options)


def lance(w, event, target='foe', now=0, success=False, owner='a'):
    w.owners[owner].soul_charges = 2  # Fixture imports an already validated resource balance.
    wallet = Wallet()
    p = w.begin_soul_ability(event, owner, target, 'agony', wallet, legal=True, crystal_available=True)
    return p, w.finish_agony(event,(3,4,6),now,con_save_success=success), wallet


def main():
    global matrix
    w=world()
    check('all eight acquired once', w.owners['a'].feats == FEATS)
    rejects('no repeated feat', lambda:w.acquire('a','chef','again',legal_selection=True))
    poor=world(feats=(),stats=FeatStats(3,2))
    for feat in FEATS-{'chef'}:
        rejects('prerequisite '+feat,lambda f=feat:poor.acquire('a',f,f,legal_selection=True))
    rejects('actual selection required',lambda:poor.acquire('a','chef','fake',legal_selection=False))
    check('acquisition does not grant reserve',w.owners['a'].recovery==0)
    w.completed_rest('a',1)
    check('completed rest fills finite reserve',w.owners['a'].recovery==16)
    rejects('same rest cannot repeat',lambda:w.completed_rest('a',1))
    w.owners['a'].stats=replace(w.owners['a'].stats,level=12,pb=4)
    check('level change is not refill',w.owners['a'].recovery==16 and w.owners['a'].recovery_capacity==16)

    w=world(owners=('a','b'))
    inv,ids=cooking(w)
    check('actual ingredients spent',inv.servings==0)
    check('cooked food has no pre-rest potency',not w.serving_potent(ids[0],4000))
    rejects('unfinished rest cannot empower',lambda:w.finalize_chef('a','r1',4000,actual_successful_rest=False))
    w.owners['a'].stats=replace(w.owners['a'].stats,pb=4)
    w.completed_rest('a',1)
    empowered=w.finalize_chef('a','r1',28800,actual_successful_rest=True)
    check('PB increase never manufactures fourth food',len(empowered)==3)
    check('current PB determines finalized shield',w.servings[ids[0]]['amount']==8)
    rejects('cannot finalize batch twice',lambda:w.finalize_chef('a','r1',28800,actual_successful_rest=True))
    strong(w,'recipient')
    offer=w.consume_chef('eat1',ids[0],'recipient',28800,28860,legal_uninterrupted_consumption=True)
    check('rejected Chef shield still consumes food and entitlement',not offer['accepted'] and w.servings[ids[0]]['state']=='consumed')
    rejects('same recipient second Chef serving',lambda:w.consume_chef('eat2',ids[1],'recipient',28860,28920,legal_uninterrupted_consumption=True))
    rejects('serving identity replay',lambda:w.consume_chef('replay',ids[0],'other',28860,28920,legal_uninterrupted_consumption=True))
    w.completed_rest('recipient',1)
    check('recipient own rest resets family entitlement',w.consume_chef('eat3',ids[1],'recipient',28920,28980,legal_uninterrupted_consumption=True)['accepted'])
    w.completed_rest('a',2)
    check('chef next rest ends unused potency',not w.serving_potent(ids[2],29000))
    check('chef rest does not erase already granted shield',w.buffers.amount('recipient')==8)
    w=world(); inv,ids=cooking(w); w.abort_cooking_rest('a','r1')
    check('failed rest retains ordinary paid food',inv.servings==0 and w.servings[ids[0]]['state']=='ordinary')
    rejects('aborted batch never finalizes',lambda:w.finalize_chef('a','r1',28800,actual_successful_rest=True))
    w=world(); inv,ids=cooking(w); w.owners['a'].stats=replace(w.owners['a'].stats,pb=2)
    w.completed_rest('a',1); chosen=w.finalize_chef('a','r1',28800,actual_successful_rest=True)
    check('PB decrease leaves ordinary remainder',len(chosen)==2 and w.servings[ids[2]]['state']=='ordinary')
    check('exact 24h potency endpoint',w.serving_potent(ids[0],115199) and not w.serving_potent(ids[0],115200))
    rejects('one minute eating required',lambda:w.consume_chef('fast',ids[0],'b',28800,28859,legal_uninterrupted_consumption=True))
    w.retire_serving(ids[1],actually_consumed_or_discarded=True)
    check('discarded item stays unavailable',not w.serving_potent(ids[1],28900))

    w=world(owners=('a','b')); strong(w,'listener')
    w.start_activity('speech','a','inspiring_leader',('listener','left'),0,legal=True)
    w.owners['a'].stats=replace(w.owners['a'].stats,charisma_score=8,charisma_modifier=-1,level=12)
    rejects('speech not completed early',lambda:w.finish_activity('speech',599,continuously_eligible=('listener',)))
    result=w.finish_activity('speech',600,continuously_eligible=('listener',))
    check('speech start snapshot and rejected offer consumption',result[0]['amount']==10 and not result[0]['accepted'])
    check('departing listener alone loses benefit',w.buffers.amount('left')==0)
    rejects('different speaker same recipient cap',lambda:w.start_activity('s2','b','inspiring_leader',('listener',),700,legal=True))
    rejects('speaker cannot target self',lambda:w.start_activity('self','a','inspiring_leader',('a',),700,legal=True))
    w.start_activity('fail','a','inspiring_leader',('new',),700,legal=True); w.interrupt_activity('fail')
    rejects('interrupted speech cannot complete',lambda:w.finish_activity('fail',1300,continuously_eligible=('new',)))
    w.start_activity('restart','a','inspiring_leader',('new',),1300,legal=True)
    check('owned feat survives later CHA loss',w.finish_activity('restart',1900,continuously_eligible=('new',))[0]['amount']==11)
    rejects('completed speech replay',lambda:w.finish_activity('restart',1901,continuously_eligible=('new',)))

    w=world(); strong(w,'a')
    w.start_activity('blood','a','blood_ritual',('ally','left'),0,legal=True)
    rejects('blood use commits at start',lambda:w.start_activity('blood2','a','blood_ritual',(),0,legal=True))
    w.owners['a'].stats=replace(w.owners['a'].stats,level=10)
    result=w.finish_activity('blood',600,continuously_eligible=('ally',))
    check('blood level snapshotted at start',result[0]['amount']==16 and result[1]['amount']==8)
    check('blood ally exact one-hour deadline',w.buffers.current('ally').expiry==ClockMarker(4200))
    check('blood advantage exists despite rejected self shield',w.blood_save('a',actual_save_rolled=False,curse_or_disease=True)==False and 'a' in w.blood_advantage)
    check('unrelated save preserves advantage',not w.blood_save('a',actual_save_rolled=True,curse_or_disease=False) and 'a' in w.blood_advantage)
    check('qualifying actual roll consumes independent rider',w.blood_save('a',actual_save_rolled=True,curse_or_disease=True) and not w.blood_save('a',actual_save_rolled=True,curse_or_disease=True))
    w.completed_rest('a',1);w.start_activity('tie','a','blood_ritual',(),1000,legal=True)
    w.completed_rest('a',2);w.finish_activity('tie',1600,continuously_eligible=())
    check('post-rest tie grant belongs to new epoch',w.buffers.current('a').rest_epoch==2 and w.blood_advantage['a']==2)
    w.completed_rest('a',3);w.start_activity('interrupted','a','blood_ritual',(),2000,legal=True);w.interrupt_activity('interrupted')
    rejects('interrupted ritual still spends use',lambda:w.start_activity('retry','a','blood_ritual',(),3000,legal=True))

    w=world()
    for slot in ('first','second'):
        w.summon_created(slot,'a','root',slot,slot,0,qualifying_creation=True,actual_paid_source_activation=True)
    check('two genuine bodies receive independent creation shields',w.buffers.amount('first')==6 and w.buffers.amount('second')==6)
    w.buffers.end_dependency('first')
    check('ended creature loses grant',w.buffers.amount('first')==0)
    check('same lineage recreation grants nothing',w.summon_created('reissue','a','root','first','new-body',1,qualifying_creation=True,actual_paid_source_activation=True) is None)
    check('fixed damage does not use rider',w.summon_damage_bonus('a','root','first','round:1',actual_damage_roll=False)==0)
    w.owners['a'].stats=replace(w.owners['a'].stats,pb=4)
    check('rolled damage uses current PB',w.summon_damage_bonus('a','root','first','round:1',actual_damage_roll=True)==4)
    check('shared roll/reissue same round cannot duplicate',w.summon_damage_bonus('a','root','first','round:1',actual_damage_roll=True)==0)
    check('other creature own roll entitlement',w.summon_damage_bonus('a','root','second','round:1',actual_damage_roll=True)==4)
    check('next true round qualifies',w.summon_damage_bonus('a','root','first','round:2',actual_damage_roll=True)==4)
    rejects('unpaid root cannot be invented',lambda:w.summon_created('bad','a','fake','slot','body',0,qualifying_creation=True,actual_paid_source_activation=False))
    rejects('device/rebuild ineligible',lambda:w.summon_created('device','a','real','slot','device',0,qualifying_creation=False,actual_paid_source_activation=True))

    w=world(); kit=Kit('kit',1); wallet=Wallet(); dying=LifeState(20,0,death_failures=2)
    stable=w.kit_stabilize('st','a','patient','episode1',dying,kit,wallet,0,2,legal=True)
    check('kit pays one actual use and BA',kit.uses==0 and not wallet.bonus_action)
    check('canonical stabilization no HP and clears failures',stable.stable and stable.hp==0 and stable.death_failures==0 and stable.stable_until_seconds==7200)
    recovered=heal(stable,1)
    check('separate background recovery preserves recorded trigger',recovered.hp==1 and w.finish_stabilization('st',0,living_target=True)['amount']==3)
    rejects('no duplicate stabilization grant',lambda:w.finish_stabilization('st',0,living_target=True))
    rejects('already Stable cannot trigger',lambda:w.record_stabilization('bad','a','patient','episode1',stable,stable,owner_caused=True))
    new_stable=replace(dying);stabilize(new_stable,1,1)
    w.record_stabilization('spell','a','patient','episode2',dying,new_stable,owner_caused=True)
    check('new actual episode / other method qualifies',w.finish_stabilization('spell',1,living_target=True)['amount']==3)
    rejects('empty real kit rejected before action',lambda:w.kit_stabilize('empty','a','p','e',dying,kit,Wallet(),2,1,legal=True))
    check('input LifeState not mutated',not dying.stable and dying.death_failures==2)

    w=world(owners=('a','b'))
    check('optional declined melee rider retains turn',w.melee_necrotic('a','turn1',(),melee_hit=True,opted_in=False)==0)
    check('melee critical doubles feat die',w.melee_necrotic('a','turn1',(3,5),melee_hit=True,opted_in=True,critical=True)==8)
    check('extra Action does not refresh',w.melee_necrotic('a','turn1',(6,),melee_hit=True,opted_in=True)==0)
    check('off-turn hit can qualify',w.melee_necrotic('a','enemy-turn',(4,),melee_hit=True,opted_in=True)==4)
    check('genuine extra turn qualifies',w.melee_necrotic('a','extra-turn',(2,),melee_hit=True,opted_in=True)==2)
    rejects('no seal for nonfatal/THP-only harm',lambda:w.seal_death('a','death',0,actual_dead=False,owned_necrotic_fatal_root=True))
    w.seal_death('a','death',0,actual_dead=True,owned_necrotic_fatal_root=True)
    check('same owner death redundant',not w.seal_death('a','death',1,actual_dead=True,owned_necrotic_fatal_root=True))
    check('rank5 blocked; higher and unknown not inferred',w.resurrection_sealed('death',1,5) and not w.resurrection_sealed('death',1,6) and not w.resurrection_sealed('death',1,None))
    check('24h exact expiry',w.resurrection_sealed('death',86399,0) and not w.resurrection_sealed('death',86400,5))
    w.seal_death('b','death',10,actual_dead=True,owned_necrotic_fatal_root=True)
    w.remove_seal('a','death',explicit_removal=True)
    check('separate owner seal remains',w.resurrection_sealed('death',20,5))
    rejects('generic cure cannot erase seal',lambda:w.remove_seal('b','death',explicit_removal=False))
    w.returned_to_life('death',actual_legal_return=True)
    check('legal return closes exact old death',not w.resurrection_sealed('death',30,5))
    w.seal_death('a','death2',40,actual_dead=True,owned_necrotic_fatal_root=True)
    check('new later death separately sealable',w.resurrection_sealed('death2',40,5))
    w=world(); wallet=Wallet(); life=LifeState(20,20)
    reaction=w.buffers.necrotic_affinity('a','necro',6,wallet,turn_end_deadline(12),legal=True)
    after,ev=w.buffers.core_damage('a','necro',life,reaction['remainingDamage'])
    offer=w.buffers.finish_necrotic_affinity('a','necro','absorbed',0,living_holder=True)
    check('reviewed reaction pipeline preserved',not wallet.reaction and after.hp==17 and reaction['prevented']==3 and offer['amount']==3)

    w=world(); p=drain(w)
    check('uncharged acquisition cannot heal or create excess',p['fundedAmount']==0 and p['actualHpGained']==0 and p['genuineExcess']==0)
    w.completed_rest('a',1)
    check('same root round entitlement remains spent after rest',w.drain('again','a','s1','round:1','foe',LifeState(20,5),12,own_spell_damage=True,hostile_not_farmed=True) is None)
    p=drain(w,event='h2',window='round:2')
    check('actual drain funds finite HP',p['actualHpGained']==6 and p['reserveSpent']==6 and w.owners['a'].recovery==10)
    rejects('no after-the-fact retarget',lambda:w.select_drain('a','s1','round:2','other',eligible_before_damage=True))
    p=drain(w,event='h3',root='s3',life=LifeState(20,20),damage=30,conditional_flat_bonuses=(99,))
    check('full HP finite excess spends remaining budget',p['genuineExcess']==10 and p['reserveSpent']==10 and p['actualHpGained']==0 and not p['conditionalAddonsQualify'])
    check('zero remaining cannot farm extra conversions',drain(w,event='h4',root='s4',life=LifeState(20,20),damage=200)['genuineExcess']==0)
    chain=HealingChain('root')
    check('child healing cannot copy or trigger resource gain',chain.child('copy',kind='copy',parent_flags=p['flags']) is None and chain.child('resource',kind='resource',parent_flags=p['flags']) is None)
    excess=ExcessLedger(p['genuineExcess'],internal_resolved=True)
    check('authorized external conversion gets finite excess',excess.convert(10,kind='temp-hp',source_eligible=True)==10)
    rejects('excess cannot spend twice',lambda:excess.convert(1,kind='damage',source_eligible=True))
    w=world();w.completed_rest('a',1)
    p=drain(w,hp_gain_prohibited=True,damage=100)
    check('prohibition spends no reserve or excess',p['fundedAmount']==0 and p['genuineExcess']==0 and w.owners['a'].recovery==16)
    p=drain(w,event='crit',root='crit',life=LifeState(20,18,wounds=(None,None,None)),damage=4)
    check('Critical ceiling loss is not automatically excess',p['fundedAmount']==2 and p['actualHpGained']==1 and p['genuineExcess']==0)
    w.select_drain('a','zero','round:1','foe',eligible_before_damage=True)
    check('zero actual damage does not commit entitlement',w.drain('zero','a','zero','round:1','foe',LifeState(20,5),0,own_spell_damage=True,hostile_not_farmed=True) is None and ('a','zero','round:1') not in w.drain_used)
    p=w.drain('one','a','zero','round:1','foe',LifeState(20,5),1,own_spell_damage=True,hostile_not_farmed=True)
    check('one damage commits even zero formula',p['fundedAmount']==0 and ('a','zero','round:1') in w.drain_used)
    w.select_drain('a','fake','round:1','foe',eligible_before_damage=True)
    rejects('Agony/natural damage not spell',lambda:w.drain('fake','a','fake','round:1','foe',LifeState(20,5),10,own_spell_damage=False,hostile_not_farmed=True))
    p=drain(w,event='deadheal',root='dead',life=LifeState(20,0,dead=True),damage=20)
    check('dead owner never resurrects from drain',p['state'].dead and p['fundedAmount']==0)

    # Independent conservation oracle, exercising funding AFTER reductions and
    # ordinary versus Critical missing HP. No need to mirror helper internals.
    for reserve in (0,1,2,7,16):
        for hp in range(21):
            for critical in (False,True):
                for damage in (0,1,2,9,40,101):
                    for factor in (Fraction(1),Fraction(1,2)):
                        w=world(feats={'lifeleech'});w.owners['a'].recovery=reserve
                        life=LifeState(20,hp,wounds=(None,None,None) if critical else ())
                        p=drain(w,life=life,damage=damage,systemic_factors=(factor,))
                        if damage==0:
                            assert p is None;matrix+=1;continue
                        funded=min(reserve,(damage//2*factor).__floor__())
                        ceiling=19 if critical else 20
                        assert p['reserveSpent']==funded
                        assert p['actualHpGained']==min(funded,max(0,ceiling-hp))
                        assert p['genuineExcess']==max(0,funded-(20-hp))
                        assert p['reserveRemaining']+p['reserveSpent']==reserve
                        matrix+=1

    w=world(owners=('a','b'))
    for i in range(3):check('soul accumulation '+str(i),death(w,'death'+str(i))==1)
    check('both feats use one capped pool',w.owners['a'].soul_charges==3)
    check('full capacity has no latent fourth',death(w,'full','body')==0)
    w.owners['a'].soul_charges=0
    check('same body later death this rest spent',death(w,'redeath','body')==0)
    rejects('old death cannot be rescanned',lambda:death(w,'full','body'))
    w.completed_rest('a',1)
    check('new rest permits future new death of body',death(w,'future','body')==1)
    check('second owner independent',death(w,'future','body',owner='b')==1)
    check('ineligible soul/object origin no charge',death(w,'object',qualifying_hostile_soul=False)==0)
    check('out of range death recorded ineligible',death(w,'far',legal_range_perception_line=False)==0)
    rejects('moving closer cannot rescan',lambda:death(w,'far'))
    w=world(feats={'soul_cage'})
    check('Soul Cage capture requires physical crystal',death(w,'no-crystal')==0)
    check('decline consumes eligible opportunity',death(w,'decline','body',crystal_available=True,accept=False)==0)
    check('declined body cannot retry this rest',death(w,'decline-redeath','body',crystal_available=True)==0)
    check('another body may capture',death(w,'other',crystal_available=True)==1)
    w.release_souls('a',1,actual_quiet_minute=True,crystal_available=True)
    check('quiet release dissipates owner charges',w.owners['a'].soul_charges==0)
    w=world(feats={'lifeleech'});death(w,'spark')
    rejects('Lifeleech alone cannot spend through unowned feat',lambda:w.begin_soul_ability('spend','a','a','shield',Wallet(),legal=True,crystal_available=True))

    w=world();w.owners['a'].soul_charges=3;strong(w,'a'); wallet=Wallet()
    w.begin_soul_ability('shield','a','a','shield',wallet,legal=True,crystal_available=True)
    offer=w.finish_soul_shield('shield',(8,8),0)
    check('self shield pays before failed arbitration',not offer['accepted'] and w.owners['a'].soul_charges==2 and not wallet.bonus_action)
    rejects('shield replay rejected',lambda:w.finish_soul_shield('shield',(8,8),0))
    rejects('lost crystal prevents ability',lambda:w.begin_soul_ability('lost','a','foe','agony',Wallet(),legal=True,crystal_available=False))
    check('lost crystal did not erase owner charges',w.owners['a'].soul_charges==2)
    p,result,wallet=lance(w,'lance',success=True)
    check('Agony pays Action/2 charges and half on save',result['damage']==6 and w.owners['a'].soul_charges==0 and wallet.actions==0 and p['dc']==15)
    check('Agony remains feat-owned damage',result['sourceKind']=='feat' and result['spellRoot'] is None and result['damageOwner']=='a')
    r=w.agony_reduction('foe',0)
    check('successful save still applies separate healing rider',r is not None and r.value==Fraction(1,2))
    lance(w,'lance2',now=30)
    check('same-family reapplication refreshes not multiplies',len(w.agony)==1 and w.agony['foe']['expires']==90 and len(w.agony['foe']['contributors'])==2)
    hp=healing_packet(LifeState(20,0),12,reductions=(w.agony_reduction('foe',30),))
    check('repeated lances still exactly half heal',hp['actualHpGained']==6)
    w.commit_healing('heal',hp)
    check('commit consumes single family record',w.agony_reduction('foe',31) is None)
    rejects('healing commitment replay rejected',lambda:w.commit_healing('heal',hp))
    lance(w,'lance3',now=100)
    hp=healing_packet(LifeState(20,20),4,hp_gain_prohibited=True,reductions=(w.agony_reduction('foe',100),))
    w.commit_healing('blockedheal',hp)
    check('positive potential consumes despite later prohibition/cap',not w.agony)
    lance(w,'lance4',now=200)
    hp=healing_packet(LifeState(20,5),0,reductions=(w.agony_reduction('foe',200),))
    w.commit_healing('zeroheal',hp)
    check('zero potential does not consume next-heal record',w.agony_reduction('foe',201) is not None)
    hp=healing_packet(LifeState(20,5),4,reductions=(w.agony_reduction('foe',201,suppressed=True),))
    w.commit_healing('suppressedheal',hp)
    check('suppression defers effect and consumption',hp['actualHpGained']==4 and w.agony_reduction('foe',202) is not None)
    check('Agony exact elapsed expiry while suppressed',w.agony_reduction('foe',260) is None)
    lance(w,'lance5',target='a',now=300)
    w.completed_rest('a',1)
    hp=drain(w,event='drain-with-agony',reductions=(w.agony_reduction('a',300),))
    check('Lifeleech integrates same canonical reducer commit',hp['fundedAmount']==3 and w.agony_reduction('a',300) is None)
    lance(w,'lance6',now=400)
    rejects('generic cure cannot remove Agony',lambda:w.remove_agony('foe',explicit_removal=False))
    w.remove_agony('foe',explicit_removal=True)
    check('explicit source removal works',w.agony_reduction('foe',401) is None)

    report={'status':'PASS — candidate reference; independent implementation review pending',
            'feats':8,'checks':len(checks),'fundingBoundaryCases':matrix,'failures':[],
            'helperSha256':hashlib.sha256((ROOT/'tools/buffer_feat_playtest_rules.py').read_bytes()).hexdigest(),
            'checksPassed':checks}
    evidence=ROOT.parents[1]/'docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FINAL_CLOSURE.md'
    submitted=ROOT.parents[1]/'docs/audit/2026-10-08/full-game/BUFFER_FEAT_IMPLEMENTATION_MANIFEST.json'
    if evidence.exists() and submitted.exists():
        reviewed=json.loads(submitted.read_text(encoding='utf-8'))['files']
        helper=next(r for r in reviewed if r['path'].endswith('/tools/buffer_feat_playtest_rules.py'))
        if helper['sha256']==report['helperSha256']:
            report['status']='PASS — REVIEWED / reference-VALIDATED bounded eight-feat scope'
            report['reviewEvidence']=str(evidence.relative_to(ROOT.parents[1])).replace('\\','/')
    (ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checksPassed'},indent=2))


if __name__=='__main__':main()
