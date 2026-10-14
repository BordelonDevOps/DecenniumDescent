from pathlib import Path
import json
from maximum_hp_playtest_rules import *
from core_playtest_rules import LifeState,healing_ceiling
from healing_playtest_rules import survival_damage_event
ROOT=Path(__file__).resolve().parents[1]
RIB='monk.hero.iron-fist-master.ribcrusher-strike'
BONE='monk.hero.iron-fist-master.bone-breaking-strike'
SILENCE='monk.hero.way-of-shadow.deathless-silence'
FLESH='warrior.supplement.flesh-warden'

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected);checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    def rec(name,source,amount,owner='owner',target='target',**kw):
        return MaxHpRecord(name,source,owner,target,amount,ends_on_completed_rest=source in MONK,**kw)
    rows=[rec('flesh',FLESH,20),rec('trauma',RIB,9)]
    out=effective_maximum(101,rows,target='target',expedition=4,exhaustion=4)
    check('Flat bonus and global trauma precede systemic product',out['effectiveMaximum'],42)
    check('Otherwise applicable maximum includes both flat operations',out['preSystemicMaximum'],112)
    suppressed=[rows[0],replace(rows[1],suppressed=True)]
    check('Suppressing trauma recomputes from base without drift',
          effective_maximum(101,suppressed,target='target',expedition=4,exhaustion=4)['effectiveMaximum'],45)
    monks=[rec('small',RIB,5,owner='Monk-A'),rec('large',BONE,9,owner='Monk-B')]
    check('Different Monk owners share one global strongest reduction',
          effective_maximum(30,monks,target='target')['effectiveMaximum'],21)
    check('Suppressed strongest reveals smaller owner record',
          effective_maximum(30,[monks[0],replace(monks[1],suppressed=True)],target='target')['effectiveMaximum'],25)
    duplicate=rec('another-cast',RIB,7,owner='Monk-A',starts=ClockMarker(2),expires=ClockMarker(8))
    rows=monks+[duplicate]
    check('Repeated card keeps separate record but never stacks',
          effective_maximum(30,rows,target='target',now=3)['monkTraumaReduction'],9)
    check('Future application not active yet',
          effective_maximum(30,[duplicate],target='target',now=1)['effectiveMaximum'],30)
    check('Expiry wins at exact endpoint',
          effective_maximum(30,[duplicate],target='target',now=8)['effectiveMaximum'],30)
    check('Suppressed clock still expires',
          effective_maximum(30,[replace(duplicate,suppressed=True)],target='target',now=9)['effectiveMaximum'],30)
    stopped=complete_target_rest(rows,'target',completed=True,rest_type='short')
    check('Completed target rest ends all default Monk records including other owners',
          [r.present for r in stopped],[False]*3)
    check('Interrupted rest ends none',complete_target_rest(rows,'target',completed=False,rest_type='short'),tuple(rows))
    check('Another target rest cannot end records',
          complete_target_rest(rows,'someone-else',completed=True,rest_type='long'),tuple(rows))
    bonus=rec('permanent','feat:tenacity',8)
    check('Rest does not remove unrelated bonus',complete_target_rest([bonus],'target',completed=True,rest_type='long')[0].present,True)
    different=replace(duplicate,ends_on_completed_rest=False)
    check('Explicit endpoint-only record not replaced by default rest rule',
          complete_target_rest([different],'target',completed=True,rest_type='short')[0].present,True)
    check('Same feat duplicate does not stack',effective_maximum(20,[bonus,rec('duplicate-feat','feat:tenacity',8)],target='target')['effectiveMaximum'],28)
    all_feats=[rec('tenacity','feat:tenacity',10),rec('tough','feat:tough',6),
               rec('nails','feat:tough_as_nails',20),rec('dark','feat:dark_fortitude',20)]
    check('Distinct permanent feats add under explicit integration',effective_maximum(20,all_feats,target='target')['effectiveMaximum'],76)
    check('Tough snapshots acquisition level',source_amount('feat:tough',character_level=12,acquisition_level=3),6)
    check('Tough as Nails grows by explicit source',source_amount('feat:tough_as_nails',character_level=12),24)
    check('Tenacity grows dynamically',source_amount('feat:tenacity',character_level=12),12)
    check('Dark Fortitude grows dynamically',source_amount('feat:dark_fortitude',character_level=12),24)
    check('Familiar bonus current owner level',source_amount('feat:familiar_bond',character_level=12),12)
    check('Flesh Warden uses Warrior rather than character level',source_amount(FLESH,character_level=12,warrior_level=5),10)
    check('Conjuration uses creating Wizard snapshot',source_amount('wizard.engine[10]',wizard_level=12,conjuration_creation_level=5),5)
    check('Flesh Ascendant uses current controller Wizard level',source_amount('wizard.engine[24]',wizard_level=12),24)
    wizard=[rec('school','wizard.engine[10]',10),rec('flesh-engine','wizard.engine[24]',20),
            rec('flesh-card','wizard.hero.necromancer.flesh-ascendant',20)]
    check('Conjuration stacks with Flesh but duplicate engine/card do not',
          effective_maximum(20,wizard,target='target')['effectiveMaximum'],50)
    current=LifeState(30,26,temp_hp=35)
    after,event=update_maximum(current,30,[rec('trauma',BONE,15)],target='target')
    check('Clamp lowers currentHP but does not consume temporaryHP',(after.maximum_hp,after.hp,after.temp_hp),(15,15,35))
    check('Clamp produces no damage healing Wound or failure metrics',
          tuple(event[k] for k in ('capacityClamp','actualHpDamage','actualHpGained','woundSaves','deathFailuresAdded')),(11,0,0,0,0))
    healed_capacity,event=update_maximum(after,30,[],target='target')
    check('Removing reduction restores capacity without HP',(healed_capacity.maximum_hp,healed_capacity.hp),(30,15))
    critical=LifeState(30,15,wounds=(None,None,None))
    critical,_=update_maximum(critical,30,[rec('trauma',BONE,15)],target='target')
    check('Critical ceiling recalculates after max change',(critical.maximum_hp,healing_ceiling(critical)),(15,14))
    dying=LifeState(30,0,death_failures=2)
    dying,_=update_maximum(dying,30,[rec('severe',SILENCE,100)],target='target',expedition=6,exhaustion=6)
    check('Minimum max1 and lethal-track math do not alter zero life state',
          (dying.maximum_hp,dying.hp,dying.dead,dying.death_failures),(1,0,False,2))
    dead=LifeState(30,0,dead=True,death_failures=3)
    dead,_=update_maximum(dead,30,[rec('flesh',FLESH,20)],target='target')
    check('Capacity increase does not resurrect corpse',(dead.maximum_hp,dead.hp,dead.dead,dead.death_failures),(50,0,True,3))
    stable=LifeState(30,0,stable=True,stable_until_seconds=3600)
    stable,_=update_maximum(stable,30,[rec('flesh',FLESH,20)],target='target')
    check('Capacity update preserves Stable deadline',(stable.stable,stable.stable_until_seconds),(True,3600))
    check('Exact quarter comparison uses cross multiplication',threshold(25,100,fraction=Fraction(1,4),relation='at-or-below'),True)
    check('26of101 not quarter eligible',threshold(26,101,fraction=Fraction(1,4),relation='at-or-below'),False)
    check('Odd maximum half not rounded first',threshold(50,101),True)
    check('Exact half not strictly below',threshold(50,100),False)
    check('Pain uses exact full ten-percent bands',pain_empowerment(91,101),0)
    check('Pain reaches first full ten-percent band',pain_empowerment(90,101),1)
    check('Pain caps bonus at5',pain_empowerment(1,101),5)
    loss=HpEventSnapshot('loss',26,25,100,'damage')
    check('Genuine damage crosses inclusive quarter',loss.falls_across(),True)
    check('Direct HP loss can cross quarter',replace(loss,kind='direct-hp-loss').falls_across(),True)
    check('Capacity clamp never fires fall trigger',replace(loss,kind='capacity-change').falls_across(),False)
    check('Already below quarter losingHP does not cross again',HpEventSnapshot('already-low',20,19,100,'damage').falls_across(),False)
    check('Strict half crossing excludes landing on half',HpEventSnapshot('half',51,50,100,'damage').falls_across(fraction=Fraction(1,2),inclusive=False),False)
    check('Strict half crossing includes crossing from exact half',HpEventSnapshot('half-cross',50,49,100,'damage').falls_across(fraction=Fraction(1,2),inclusive=False),True)
    check('Healed-above-half requires actual healing gain',HpEventSnapshot('heal',50,51,100,'healing').healed_above_half(),True)
    check('NoHPgain despite already above half does not end healed gate',HpEventSnapshot('none',60,60,100,'healing').healed_above_half(),False)
    check('Max-only change cannot satisfy healed exit',HpEventSnapshot('max',60,60,100,'capacity-change').healed_above_half(),False)
    history=HpEventSnapshot('old-damage',60,49,100,'damage')
    check('Historical damage uses original event maximum',history.damage_left_below_half(),True)
    check('Later max60 would differ but does not rewrite stored predicate',threshold(49,60),False)
    check('WoundEaterIII no invented minimum at tiny maximum',percentage_amount(3,4),0)
    check('Explicit Spiral/FalseLife minimum1 remains',percentage_amount(3,4,source_minimum=1),1)
    check('Viable resurrection bridge minimum1 remains',percentage_amount(1,2,source_minimum=1),1)
    damage_state,damage_event=survival_damage_event(LifeState(30,30),4)
    trauma_state,stat_event=update_maximum(damage_state,30,[rec('bone',BONE,15)],target='target')
    check('Damage precedes separate maximumHP clamp',(damage_state.hp,trauma_state.hp,damage_event['actualDamageDealt'],stat_event['capacityClamp']),(26,15,4,11))
    rejects('Duplicate application identity rejected',lambda:effective_maximum(20,[bonus,bonus],target='target'))
    rejects('Unknown modifier source rejected',lambda:rec('unknown','spell:invented',5))
    rejects('Tough requires explicit acquisition snapshot',lambda:source_amount('feat:tough',character_level=12))
    rejects('Conjuration requires explicit creation snapshot',lambda:source_amount('wizard.engine[10]',wizard_level=12))
    rejects('Trauma cannot lose all endpoints',lambda:MaxHpRecord('endless',RIB,'monk','target',3))
    rejects('Approximate floating threshold disallowed',lambda:threshold(1,10,fraction=0.25))
    states=0
    for base in range(1,102):
      for expedition in (0,4,6):
       for exhaustion in (0,4,6):
        actual=effective_maximum(base,[],target='target',expedition=expedition,exhaustion=exhaustion)['effectiveMaximum']
        expected=max(1,(Fraction(base)* (Fraction(3,4) if expedition>=4 else 1) * (Fraction(1,2) if exhaustion>=4 else 1)).__floor__())
        assert actual==expected
        states+=1
    report={'status':'PASS','reviewStatus':'REVIEWED / reference-VALIDATED; bounded 58-source interface',
            'scope':'Selected modifier formulas/groups, capacity recomputation/clamp, rest endpoints, exact percentage thresholds and recorded HP transitions. Not full feat/class acquisition, companion creation/lifecycle or combat scheduler.',
            'checkCount':len(checks),'systemicParityStates':states,'checks':checks}
    (ROOT/'docs/mechanics/MAXIMUM_HP_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} maximumHP checks and {states} systemic parity states; bounded interface reviewed.')
if __name__=='__main__':main()
