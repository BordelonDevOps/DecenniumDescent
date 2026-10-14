"""Adversarial candidate contract scenarios, not balance or complete runtime tests."""
from dataclasses import replace
from pathlib import Path
from itertools import product
from copy import deepcopy
import json, hashlib
from transformation_spell_playtest_rules import *
from spell_playtest_rules import quote_cast, access_for
from core_playtest_rules import LifeState
from form_temphp_playtest_rules import DruidState, DruidStats

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
sources=json.loads((AUDIT/'TRANSFORMATION_SPELL_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
fixtures={s['id']:deepcopy(s['wholeOverlaySnapshot']) for s in sources['spells']}
for f in fixtures.values():f['status']='operational-playtest-draft'  # in-memory candidate fixture only
checks=0

def check(value,label):
    global checks
    assert value,label
    checks+=1

def rejects(fn,label):
    try:fn()
    except SpellRuleError:check(True,label)
    else:raise AssertionError(label)

def stats(owner='a',attack=10,dc=18,pb=6,modifier=4):return CastStats(owner,'Wizard',attack,dc,pb,modifier)

def price(spell,*,paid=None,surcharge=False):
    q=quote_cast(fixtures[spell],'Wizard',20,available_spell_ids={spell},rp=100,max_rp=100,
                 dissonance=12 if surcharge else 0,proficiency=6,casting_modifier=4)
    return CastPrice.from_quote(q,actual_base_paid=paid,exact_reduction_authorized=paid is not None)

def world(ids=('a','b','c'),objects=()):
    w=TransformationWorld(BufferLedger(),ConcentrationLedger())
    for ident in ids+tuple(objects):
        obj=ident in objects
        origin=PhysicalOrigin(ident,'object' if obj else 'creature','Medium',frozenset() if obj else frozenset({'humanoid'}),100,20 if obj else None)
        life={'hp':20,'maximum_hp':20} if obj else LifeState(40,31,wounds=(None,))
        w.add_body(Body(origin,life,'Medium',100,equipment=set() if obj else {ident+':coat'}))
    return w

def select(target='b',profile='spellform.predator',willing=True,cell=None,**kwargs):
    return Selection(target,profile,willing,frozenset({cell or target}),frozenset({cell or target}),True,**kwargs)

def cast(w,spell='polymorph',target='b',profile='spellform.predator',*,ident='cast',owner='a',now=0,index=1,willing=True,selections=None,save=False,countered=False,wallet=None,**selection_options):
    return w.cast(ident,spell,stats(owner),price(spell),wallet or Wallet(rp=100),
                  selections or [select(target,profile,willing,**selection_options)],now,index,
                  legal=True,resolve_save=lambda target,dc:save,countered=countered)

def main():
    global checks
    # Actual class gates/price rows, tested through the ordinary cast pricer.
    for spell,f in fixtures.items():
        for cls,a in f['classAccess'].items():
            check(access_for(f,cls,a['minimumClassLevel'])==a,spell+' actual class gate')
            if a['minimumClassLevel']>1:rejects(lambda:access_for(f,cls,a['minimumClassLevel']-1),'Underlevel rejected')
            q=quote_cast(f,cls,20,available_spell_ids={spell},rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=4)
            check(q['baseRpCost']==a['baseRpCost'] and q['rank']==a['rank'],'Preserved class-specific price/rank')
        rejects(lambda:quote_cast(f,'Wizard',20,available_spell_ids=set(),rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=4),'Known/prepared gate remains')
    b=BufferLedger();w=Wallet(rp=100)
    result=harmonic_bulwark(b,stats(),price('harmonic-bulwark',paid=3,surcharge=True),w,'h1','b',2,0,legal=True)
    check(result['creditedRP']==5 and b.amount('b')==25 and result['paidRP']==6,'Base discount+X+surcharge credit separation')
    check(w.rp==94 and w.actions==0,'All actual RP and Action committed')
    w=Wallet(rp=100);harmonic_bulwark(b,stats(),price('harmonic-bulwark'),w,'h2','b',0,0,legal=True)
    check(b.current('b').grant_id=='h1' and w.rp==95,'Equal shield retains original after payment')
    w=Wallet(rp=6);rejects(lambda:harmonic_bulwark(b,stats(),price('harmonic-bulwark'),w,'bad','b',2,0,legal=True),'Cannot pay full transaction')
    check(w.rp==6 and w.actions==1,'Invalid transaction spends nothing')
    rejects(lambda:harmonic_bulwark(b,stats(),price('harmonic-bulwark',paid=0),Wallet(rp=10),'free','b',0,0,legal=True),'Zero credit blocked')
    r=harmonic_bulwark(b,stats(),price('harmonic-bulwark',paid=0),Wallet(rp=10),'convert','c',2,0,legal=True)
    check(r['paidRP']==2 and b.amount('c')==10,'Free base plus paid X valid')
    w=Wallet(rp=100);r=harmonic_bulwark(b,stats(),price('harmonic-bulwark'),w,'counter','c',3,0,legal=True,countered=True)
    check(w.rp==92 and r['offer'] is None and b.amount('c')==10,'Counter spends base and X but offers no shield')
    rejects(lambda:harmonic_bulwark(b,stats(),price('harmonic-bulwark'),Wallet(rp=100),'counter','c',3,0,legal=True),'Countered ID cannot replay')
    b.completed_long_rest('c',1);check(b.amount('c')==0,'Recipient long-rest clock')

    # Same-source concentration ends at commit; another source ends on success.
    w=world();cast(w,'mass-polymorph',selections=[select('b'),select('c')],ident='mass')
    order=[];wallet=Wallet(rp=100)
    def saves(target,dc):
        order.append((target,w.current('b'),w.current('c'),wallet.rp,wallet.actions));return True
    w.cast('next','polymorph',stats(),price('polymorph'),wallet,[select('b',willing=False)],1,2,legal=True,resolve_save=saves)
    check(order[0][1:]==(None,None,93,0),'Old Mass ends and full payment precedes save')
    check(w.current('b') is None and 'a' not in w.concentration.current,'Save never restores old concentration')
    w=world();cast(w,ident='old');cast(w,ident='failed-other',owner='c',willing=False,save=True)
    check(w.current('b').cast_id=='old','Other caster failed replacement leaves anatomy')
    cast(w,ident='new-other',owner='c');check(w.current('b').cast_id=='new-other' and w.links['old:b'].state=='replaced','Success replaces exactly one record')
    w.concentration.end('c','actual-failed-check');check(w.current('b') is None,'Old form does not reappear')
    w=world();cast(w,ident='old');cast(w,ident='countered',countered=True)
    check(w.current('b') is None,'Countered new own concentration still ends old')
    w=world();cast(w,'shapechange',target='a',ident='high')
    rejects(lambda:cast(w,target='a',owner='c',ident='low'),'Other lower rank cannot overwrite')
    cast(w,target='a',owner='a',ident='ownlower');check(w.current('a').cast_id=='ownlower','Own old concentration ends before lower-rank application')

    # Profiles and ownership of actual attack events.
    w=world();life=w.bodies['b'].life;cast(w)
    attack=w.attack('b',stats(attack=12,modifier=5),1,Wallet(),legal=True)
    check((attack['attacker'],attack['statProvider'],attack['attack'],attack['modifier'])==('b','a',12,5),'Current caster stats, subject event ownership')
    check(not attack['spellcast'] and not attack['directCasterSpellDamage'] and not attack['weaponOnlyFeaturesAuthorized'],'No spellcast/caster/weapon trigger laundering')
    check(w.bodies['b'].life is life and life.hp==31 and life.wounds==(None,),'Same HP/Wounds object retained')
    p=w.profile('b',stats(),1,12,ac_components_certified=True)
    check(p['typeTags']==['humanoid'] and p['ac']==13 and not p['grantsMultiattack'],'Original type; selected AC; no Multiattack')
    rejects(lambda:w.profile('b',stats(),1,20,ac_components_certified=False),'Melded AC cannot silently apply')
    for profile,p in PROFILES.items():
        t=world();cast(t,'true-polymorph',profile=profile)
        row=t.profile('b',stats(attack=20,modifier=10),1,12,ac_components_certified=True)
        check(row['attack']['attack']==10 and row['attack']['modifier']==4 and row['attack']['reachFeet']==5,profile+' True snapshots and reach')
    w=world();cast(w,'true-polymorph');w.checkpoint(60,started_packets_and_due_saves_finished=True)
    check(w.current('b').state=='permanent' and not w.concentration.current,'True stable, concentration released')
    rejects(lambda:cast(w,owner='c',ident='ordinary'),'Ordinary spell cannot overwrite permanence')
    cast(w,'true-polymorph',owner='c',ident='newtrue');w.concentration.end('c','release')
    check(w.current('b') is None,'New True has no hidden old permanent record')

    # Hostile saves, damage rounds and final timestamp ordering.
    w=world();cast(w,willing=False)
    rejects(lambda:w.repeat_save('b',stats(),1,trigger='damage',event_or_turn='hp0',round_number=1,normal_hp_damage=0,success=False),'Temporary-HP-only loss gives no repeat')
    r=w.repeat_save('b',stats(dc=20),1,trigger='damage',event_or_turn='hit',round_number=1,normal_hp_damage=2,success=False)
    check(r['dc']==20,'Polymorph repeat uses current DC')
    rejects(lambda:w.repeat_save('b',stats(),2,trigger='damage',event_or_turn='hit2',round_number=1,normal_hp_damage=2,success=False),'One positive damage repeat per numbered round')
    rejects(lambda:w.repeat_save('b',stats(),2,trigger='damage',event_or_turn='hit',round_number=2,normal_hp_damage=2,success=False),'No cross-round event replay')
    w.repeat_save('b',stats(),6,trigger='regular-end',event_or_turn='turn1',success=False)
    rejects(lambda:w.repeat_save('b',stats(),6,trigger='regular-end',event_or_turn='turn1',success=False),'No extra-turn/repeated regular endpoint')
    w=world();cast(w,'true-polymorph',willing=False)
    r=w.repeat_save('b',stats(dc=25),60,trigger='regular-end',event_or_turn='last',success=True)
    w.checkpoint(60,started_packets_and_due_saves_finished=True)
    check(r['dc']==18 and w.current('b') is None,'True snapshot final save prevents stabilization')
    w=world();cast(w);rejects(lambda:w.checkpoint(60,started_packets_and_due_saves_finished=False),'Cannot stabilize/expire before pending packet/saves')
    rejects(lambda:w.attack('b',stats(),60,Wallet(),legal=True),'No actions past unresolved deadline')
    w.checkpoint(60,started_packets_and_due_saves_finished=True);check(w.current('b') is None,'Exact60-second temporary expiry')
    w=world();cast(w);rejects(lambda:w.repeat_save('b',stats(),1,trigger='regular-end',event_or_turn='willing',success=True),'Willing waiver does not become hostile repeat')
    wallet=Wallet();w.reject('b',1,wallet,actual_regular_turn=True,legal=True)
    check(wallet.actions==0 and w.current('b') is None,'Willing temporary rejection pays Action')

    # True object anatomy, immutable origins, sponsor and commands.
    objargs=dict(object_template='open-container',object_size='Medium',object_mass=80,object_value=0,mundane_output_certified=True)
    w=world();cast(w,'true-polymorph',target='a',profile=None,**objargs)
    p=w.profile('a',stats(),1,12,ac_components_certified=True)
    check(p['actionlessObjectAnatomy'] and not p['appliesIncapacitated'] and 'a' in w.concentration.current,'Self object can concentrate while actionless')
    check(not w.healing_target_eligible('a',native_eligible=True),'Creature-origin object cannot be newly healed as creature')
    rejects(lambda:w.reject('a',1,Wallet(),actual_regular_turn=True,legal=True),'Object anatomy cannot pay rejection Action')
    w.bodies['a'].life=replace(w.bodies['a'].life,hp=0)
    w.finalize_damage_state('a',actual_hp=0,incapacitated=False,dead=False)
    check(w.current('a') is None,'Actual0 ends object shaping even if not incapacitated')
    w=world();cast(w,'true-polymorph',profile=None,**objargs);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    w.bodies['b'].life=replace(w.bodies['b'].life,hp=0,dead=True)
    w.finalize_damage_state('b',actual_hp=0,incapacitated=True,dead=True)
    check(w.current('b').state=='permanent','Permanent creature-origin object does not auto-revert at death')
    w.dispel('b',legal=True);check(w.bodies['b'].life.hp==0 and w.bodies['b'].life.dead,'Dispel retains actual dead HP state without healing')
    # Input lives below are structural dictionaries, never creature death ledgers.
    w=world(objects=('o','p'));cast(w,'true-polymorph',target='o',object_input_eligible=True)
    check(w.slots=={'a':'o'} and not w.healing_target_eligible('o',native_eligible=True),'Slot reserved during shaping; no ordinary healing')
    p=w.profile('o',stats(),1,10,ac_components_certified=True)
    check(p['typeTags']==['transformed-object'] and p['saves']==6 and not p['deathSaves'] and not p['soul'],'Object origin baseline and saves')
    rejects(lambda:cast(w,'true-polymorph',target='o',profile='spellform.humanoid',owner='c',ident='launder'),'Origin survives cross-caster humanoid laundering')
    cast(w,'true-polymorph',target='p',object_input_eligible=True,ident='second-shaping')
    check(w.slots=={'a':'p'} and w.current('o') is None,'Own concentration replacement releases shaping slot before new creation')
    w.checkpoint(60,started_packets_and_due_saves_finished=True)
    wallet=Wallet(rp=100)
    rejects(lambda:cast(w,'true-polymorph',target='o',object_input_eligible=True,ident='army',wallet=wallet),'Permanent slot blocks second distinct creature')
    check(wallet.rp==100 and wallet.actions==1,'Occupied permanent slot rejected before payment')
    cast(w,'true-polymorph',target='p',owner='c',ident='other')
    check(w.slots=={'a':'p'} and w.bodies['p'].controller=='a','Other caster recast preserves sponsor and controller')
    ledger=CommandLedger('a');wallet=Wallet()
    rejects(lambda:w.attack('p',stats('c'),1,Wallet(),legal=True),'Object creature cannot take independent attack turn')
    w.command('p','order',1,1,ledger,wallet,mode='attack',legal=True,distance=60,owner_perceives=True)
    r=w.resolve_command('order',stats('c'),1,attached_phase=True,still_legal=True)
    check(not wallet.bonus_action and r['attack']['attacker']=='p' and r['attack']['statProvider']=='c','Owner BA, attached subject attack, new caster stat snapshot')
    rejects(lambda:ledger.activate(1,'attack',Wallet()),'No second companion offensive/command allowance')
    rejects(lambda:w.resolve_command('order',stats('c'),1,attached_phase=True,still_legal=True),'No command replay')
    check(w.uncommanded('p',1)['options']==['move','Dodge'],'Uncommanded defense only')
    w.bodies['p'].life['hp']=0
    w.finalize_damage_state('p',actual_hp=0,incapacitated=False,dead=False)
    check(w.bodies['p'].destroyed and not w.slots and w.current('p') is None,'Structural0 destroys manifestation and frees slot')
    rejects(lambda:cast(w,'true-polymorph',target='p',object_input_eligible=True,ident='resurrect'),'Destroyed object cannot be reconstructed by casting')

    # Invalid objects and economic outputs fail before any payment.
    for options in [dict(object_mass=101),dict(object_size='Huge'),dict(object_template='key'),dict(mundane_output_certified=False),dict(object_value=5)]:
        w=world();params=dict(objargs);params.update(options);wallet=Wallet(rp=100)
        rejects(lambda:cast(w,'true-polymorph',profile=None,wallet=wallet,**params),'Bounded creature-object input/output')
        check(wallet.rp==100 and wallet.actions==1,'Object preflight atomic')
    w=world(objects=('o',));rejects(lambda:cast(w,'true-polymorph',target='o'),'Object eligibility must certify no corpse/magic/carried/structural input')
    missing=PhysicalOrigin('unknown','object','Medium');w.add_body(Body(missing,{'hp':2,'maximum_hp':2},'Medium'))
    rejects(lambda:cast(w,'true-polymorph',target='unknown',profile=None,object_input_eligible=True,**objargs),'Missing mass/value prevents fabricated object')

    # Suppression preserves clocks/slots and True may stabilize while suppressed.
    for spell in ('polymorph','mass-polymorph','shapechange','true-polymorph'):
        w=world();target='a' if spell=='shapechange' else 'b';cast(w,spell,target=target)
        w.set_suppressed(target,10,suppressed=True,legal=True)
        check(w.current(target).suppressed and w.current(target).deadline==60 and 'a' in w.concentration.current,spell+' keeps concentration/clock under suppression')
        w.checkpoint(60,started_packets_and_due_saves_finished=True)
        if spell=='true-polymorph':
            check(w.current(target).state=='permanent' and w.current(target).suppressed,'True stabilizes while suppressed')
            w.set_suppressed(target,61,suppressed=False,legal=True)
            w.check_reversion_placement(target,fits_at_current_anchor=True)
            check(w.profile(target,stats(),61,12,ac_components_certified=True)['attack']['attack']==10,'Same stable record resumes')
        else:check(w.current(target) is None,spell+' expires while suppressed')
    w=world(objects=('o','p'));cast(w,'true-polymorph',target='o',object_input_eligible=True);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    w.set_suppressed('o',61,suppressed=True,legal=True)
    rejects(lambda:cast(w,'true-polymorph',target='p',object_input_eligible=True,ident='suppression-army',now=61),'Suppression cannot free permanent slot')
    check(w.slots=={'a':'o'},'Sponsor survives suppression')

    # Independent-review blocker1: active True object replacement and retained agency.
    w=world();original_life=w.bodies['b'].life
    cast(w,'true-polymorph',profile=None,**objargs);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    wallet=Wallet(rp=100)
    r=cast(w,'true-polymorph',ident='unwilling-saved',owner='c',now=61,willing=False,save=True,wallet=wallet)
    check(not r['links'] and wallet.rp==74 and wallet.actions==0,'Unwilling original person retains paid CON save while object-shaped')
    check(w.current('b').cast_id=='cast' and w.current('b').state=='permanent','Successful recast save retains old True object')
    r=cast(w,'true-polymorph',ident='unwilling-failed',owner='c',now=62,willing=False,save=False)
    check(len(r['links'])==1 and w.current('b').profile=='spellform.predator','Failed save permits creature-origin object-to-creature recast without fresh-object certification')
    check(w.bodies['b'].life is original_life and w.bodies['b'].origin.kind=='creature' and not w.slots,'Same creature HP and origin; no companion slot')
    check(w.healing_target_eligible('b',native_eligible=True),'Creature healing eligibility returns with creature anatomy')
    w=world();cast(w,'true-polymorph',profile=None,**objargs);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    wallet=Wallet(rp=100)
    rejects(lambda:cast(w,'true-polymorph',profile=None,ident='hostile-object',owner='c',now=61,willing=False,wallet=wallet,**objargs),'Original person cannot be forced into another object profile')
    check(wallet.rp==100 and wallet.actions==1 and w.current('b').cast_id=='cast','Object consent failure is unpaid and leaves old record')
    cast(w,'true-polymorph',profile=None,ident='willing-object',owner='c',now=61,**objargs)
    check(w.current('b').cast_id=='willing-object' and w.current('b').profile is None,'Willing active True object-to-object recast needs no fresh admission')
    w=world(objects=('o',));cast(w,'true-polymorph',target='o',profile=None,object_input_eligible=True,**objargs)
    w.checkpoint(60,started_packets_and_due_saves_finished=True)
    cast(w,'true-polymorph',target='o',ident='object-recast',owner='c',now=61,willing=False,save=True)
    check(w.current('o').profile=='spellform.predator' and w.bodies['o'].origin.kind=='object','Object-origin registered object recast needs no fresh outside-object certificate or creature-origin save')
    check(w.slots=={'c':'o'} and not w.healing_target_eligible('o',native_eligible=True),'Fresh creature manifestation uses new caster slot; origin restrictions persist')
    # A genuinely fresh outside object still cannot bypass the original gate.
    w=world(objects=('o',));wallet=Wallet(rp=100)
    rejects(lambda:cast(w,'true-polymorph',target='o',ident='fresh-bypass',wallet=wallet),'Registered body alone does not waive fresh outside-object admission')
    check(wallet.rp==100,'Fresh object admission failure pays nothing')

    # Independent-review blocker2: agency belongs to expressed anatomy while suppressed.
    for spell,profile in [('polymorph','spellform.predator'),('mass-polymorph','spellform.predator'),
                          ('true-polymorph','spellform.predator'),('true-polymorph',None)]:
        w=world();cast(w,spell,profile=profile,**(objargs if profile is None else {}))
        w.set_suppressed('b',1,suppressed=True,legal=True)
        wallet=Wallet();w.reject('b',2,wallet,actual_regular_turn=True,legal=True)
        check(wallet.actions==0 and w.current('b') is None,spell+str(profile)+' suppressed willing regular Action rejection')
        check('b' not in w.buffers.spell_anatomies,'Rejection actually frees Druid admission registry')
    w=world();cast(w,'true-polymorph',profile=None,**objargs)
    rejects(lambda:w.reject('b',1,Wallet(),actual_regular_turn=True,legal=True),'Unsuppressed creature-object remains actionless')
    w=world(objects=('o',));cast(w,'true-polymorph',target='o',object_input_eligible=True)
    rejects(lambda:w.reject('o',1,Wallet(),actual_regular_turn=True,legal=True),'Object-origin creature has no player-style rejection entitlement')
    w.set_suppressed('o',1,suppressed=True,legal=True)
    rejects(lambda:w.reject('o',2,Wallet(),actual_regular_turn=True,legal=True),'Object-origin root stays actionless under suppression')
    w=world();cast(w,'shapechange',target='a');w.set_suppressed('a',1,suppressed=True,legal=True)
    rejects(lambda:w.switch_shapechange('a','spellform.brute',6,2,Wallet(),original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True),'Suppression blocks internal Shapechange switch')
    check(w.bodies['a'].melded=={'a:coat'} and not w.bodies['a'].equipment,'Original meld set stays inaccessible while suppressed')

    # Real gear identities across switching, replacement, loss and reversion.
    w=world();cast(w,'shapechange',target='a',profile='spellform.humanoid')
    w.acquire_external_gear('a','external-shield',1,compatible_and_equipped=True)
    wallet=Wallet()
    rejects(lambda:w.switch_shapechange('a','spellform.predator',1,1,wallet,original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True),'No casting-turn switch')
    rejects(lambda:w.switch_shapechange('a','spellform.predator',1,2,wallet,original_regular_turn=False,legal=True,retained_gear=set(),drop_placement_legal=True),'No extra-turn switch')
    r=w.switch_shapechange('a','spellform.predator',6,2,wallet,original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True)
    check(r['droppedItemIds']==['external-shield'] and not wallet.bonus_action and not r['spellcast'],'Incompatible external gear drops; BA only')
    rejects(lambda:w.switch_shapechange('a','spellform.brute',6,2,Wallet(),original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True),'One switch per original regular turn')
    w.mark_item_lost('a','a:coat',actual_loss=True);w.concentration.end('a','release')
    check(not w.bodies['a'].equipment,'No lost melded coat or dropped shield reappears')
    w=world();cast(w,profile='spellform.humanoid');w.acquire_external_gear('b','new-sword',1,compatible_and_equipped=True)
    cast(w,owner='c',ident='replacement')
    check(w.bodies['b'].melded=={'b:coat','new-sword'},'Close-and-recapture includes still-existing original and external gear exactly once')
    w.dispel('b',legal=True)
    check(w.bodies['b'].equipment=={'b:coat','new-sword'} and not w.bodies['b'].melded,'Real identities return once')
    conflict=w.check_reversion_placement('b',fits_at_current_anchor=False)
    check(conflict['placementConflict'] and not conflict['automaticRelocation'] and conflict['automaticDamage']==0,'Blocked mandatory reversion handed to geometry')

    # Druid bridge uses existing finite resource/dependency engine.
    w=world(ids=('a','d'));ds=DruidStats('d',20,6,4,4,4)
    druid=DruidState(ds,'Moon',w.buffers,{'refrain':0,'rememberedSpell':None,'dissonance':0})
    w.druids['d']=druid
    formid='druid.base.bear-form-tank'
    druid.shift(ds,formid,'druid-bear',0,Wallet(),legal=True)
    reserve=druid.reserve;surges=druid.surges
    cast(w,target='d')
    check(druid.current is None and druid.reserve==reserve and druid.surges==surges,'Spell ends Druid form without resource refund')
    check(w.buffers.amount('d')==0,'Druid form-dependent entry buffer actually ends')
    rejects(lambda:druid.shift(ds,formid,'escape',1,Wallet(),legal=True),'Druid cannot escape spell with shift')
    w.set_suppressed('d',1,suppressed=True,legal=True)
    rejects(lambda:druid.shift(ds,formid,'suppressed-escape',1,Wallet(),legal=True),'Suppressed spell still occupies anatomy slot')

    # Pairwise Mass preflight agrees with full independent-outcome enumeration.
    scenarios=0
    for cells in product(range(3),repeat=6):
        selections=[select(str(i),cell='x') for i in range(3)]
        selections=[replace(s,original_cells=frozenset({cells[2*i]}),transformed_cells=frozenset({cells[2*i+1]})) for i,s in enumerate(selections)]
        brute=all(len({cells[2*i+choice[i]] for i in range(3)})==3 for choice in product(range(2),repeat=3))
        try:validate_mass_space(selections);pairwise=True
        except SpellRuleError:pairwise=False
        assert pairwise==brute,'Mass spatial independent-outcome mismatch'
        scenarios+=1
    check(scenarios==729,'729 occupancy cases compare against exhaustive outcomes')
    ids=tuple('t'+str(i) for i in range(10));w=world(ids=('a',)+ids)
    r=w.cast('ten','mass-polymorph',stats(),price('mass-polymorph'),Wallet(rp=100),[select(t,willing=False) for t in ids],0,1,
             legal=True,resolve_save=lambda target,dc:int(target[1:])%2==0)
    check(len(r['links'])==5 and len([i for i in ids if w.current(i)])==5,'Ten Mass targets with independent mixed saves')
    w.concentration.end('a','release');check(all(w.current(i) is None for i in ids),'One concentration ends all surviving links')

    frozen=ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md'
    check(hashlib.sha256(frozen.read_bytes()).hexdigest()=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81','Frozen class packet unchanged')
    report={'status':'PASS','checks':checks,'massOccupancyScenarios':scenarios,'profiles':len(PROFILES),'spellCandidates':len(fixtures),
            'reviewStatus':'Candidate implementation; independent GPT review pending','scope':'Bounded reference contracts; not full runtime, geometry engine or balance certification'}
    batch=ROOT/'data/playtest/spell_drafts/batch_transformations.json'
    if batch.exists():
        approved=json.loads(batch.read_text(encoding='utf-8'))
        reviewed=json.loads((AUDIT/'TRANSFORMATION_CORRECTION_MANIFEST.json').read_text(encoding='utf-8'))
        helper=next(r for r in reviewed if r['path']=='tools/transformation_spell_playtest_rules.py')
        if hashlib.sha256((ROOT/helper['path']).read_bytes()).hexdigest()==helper['sha256']:
            report['reviewStatus']='REVIEWED / reference-VALIDATED: five spell interfaces and12 profiles'
            report['reviewClosure']=approved['reviewEvidence'][0]
    (ROOT/'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
