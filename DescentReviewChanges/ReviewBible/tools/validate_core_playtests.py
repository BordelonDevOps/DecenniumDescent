"""Source checks and regression scenarios for the bounded core integration."""
from pathlib import Path
from dataclasses import asdict
import hashlib
import json
import re
from core_playtest_rules import (LifeState, task_check, attack_roll, saving_throw,
    opposed_check, damage_event, death_save, heal, stabilize, stable_recovery,
    remove_wounds, active_injuries, hit_dice_recovered, healing_ceiling)
from spell_playtest_rules import SpellRuleError

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
checks=[]


def check(name, success):
    checks.append({'name':name,'pass':bool(success)})


def rejects(fn):
    try:fn()
    except SpellRuleError:return True
    return False


def hit(state, damage, **kwargs):
    args=dict(wound_natural=20, constitution_save_modifier=5, injury_d6=1)
    args.update(kwargs)
    return damage_event(state,damage,**args)


def main():
    evidence=json.loads((ROOT/'data/playtest/core_condition_sources.json').read_text(encoding='utf-8'))
    check('Approved Core source unchanged',hashlib.sha256((PROJECT/evidence['source']).read_bytes()).hexdigest()==evidence['sha256'])
    conditions=evidence['conditions']
    check('All28 Core book conditions preserved uniquely',len(conditions)==len({c['name'] for c in conditions})==28)
    check('Unconscious already includes Prone in Core',any(c['name']=='Unconscious' and 'Prone' in c['sourceText'] for c in conditions))
    check('Attack nat1 misses despite huge modifier',not attack_roll(1,100,10)['hit'])
    check('Attack nat20 hits and crits despite impossibleAC',attack_roll(20,-5,99)['critical'])
    check('BeatingACby10 does not itself crit',attack_roll(10,15,15)['hit'] and not attack_roll(10,15,15)['critical'])
    check('Broader critical range still requires a hit below20',not attack_roll(19,0,25,19)['critical'] and attack_roll(19,0,18,19)['critical'])
    check('Save nat20 can fail and nat1 can succeed',not saving_throw(20,0,25)['success'] and saving_throw(1,20,15)['success'])
    check('Save failure margin uses final numeric total',saving_throw(1,4,10)['failureMargin']==5)
    check('Task threshold exact margins',task_check(10,10,10)['degree']=='critical-success' and task_check(10,-10,10)['degree']=='critical-failure')
    check('Task nat20 shifts once and may still fail',task_check(20,-15,20)['degree']=='failure')
    check('Task nat1 shifts once and may still succeed',task_check(1,30,10)['degree']=='success')
    check('Opposed tie preserves state even with different naturals',not opposed_check(20,0,10,10)['changesState'])
    check('StaticDC tie succeeds',saving_throw(10,2,12)['success'] and task_check(10,2,12)['success'])
    s,e=hit(LifeState(40,40,temp_hp=10),25)
    check('Post-temp half-max threshold',s.hp==25 and s.temp_hp==0 and e['woundSaves']==0)
    s,e=hit(LifeState(40,40,temp_hp=30),20)
    check('Fully buffered hit gives no ordinaryWound',s.hp==40 and e['woundSaves']==0)
    s,e=hit(LifeState(40,40,temp_hp=30),20,maiming=True)
    check('Maiming independently triggers atzero post-temp damage',s.hp==40 and e['woundSaves']==1 and e['woundDC']==10)
    s,e=hit(LifeState(40,15),25,maiming=True)
    check('Drop+halfMax+Maiming give exactlyone save',s.hp==0 and e['woundSaves']==1 and e['deathFailuresAdded']==0)
    s,e=hit(LifeState(40,40,wounds=(None,None)),20,wound_natural=11,constitution_save_modifier=0)
    check('ThirdWound uses oldpenalty and doesnotkill',len(s.wounds)==3 and not s.dead and e['woundTotal']==9)
    s,e=hit(LifeState(40,40,wounds=(None,None)),20,wound_natural=5,constitution_save_modifier=0,injury_d6=4)
    check('Severe thirdWound links exactlyone Injury',s.wounds==(None,None,4) and not s.dead and e['injuryRolls']==1)
    s,e=hit(LifeState(40,40,wounds=(None,None,None)),20,wound_natural=1,constitution_save_modifier=0)
    check('Later failedWound save kills withoutfourthWoundorInjury',s.dead and s.hp==0 and len(s.wounds)==3 and e['injuryRolls']==0)
    s,e=hit(LifeState(40,20),60,knockout=True,melee=True)
    check('Excess equalsmaxHP InstantDeath precedesknockoutandWound',s.dead and e['instantDeath'] and e['woundSaves']==0)
    s,e=hit(LifeState(40,0),40)
    check('Atzero maxHPdamage InstantDeath skipsfailures',s.dead and e['instantDeath'] and e['deathFailuresAdded']==0)
    s,e=hit(LifeState(40,0),1)
    check('Damageatzerogivesonefailure',s.death_failures==1 and not s.dead)
    s,e=hit(LifeState(40,0,death_failures=1),1,critical=True)
    check('Criticaldamageatzerocanreachthreefailures',s.dead and s.death_failures==3)
    s,e=hit(LifeState(40,0,stable=True,temp_hp=5,stable_until_seconds=7200),5)
    check('Buffered Stable target preservesdeadline',s.stable and s.stable_until_seconds==7200 and s.death_failures==0)
    s,e=hit(s,1)
    check('UnbuffereddamagebreaksStableandcancelsdeadline',not s.stable and s.stable_until_seconds is None and s.death_failures==1)
    s,e=hit(LifeState(40,5),5,knockout=True,melee=True,stable_d4=2,now_seconds=100)
    check('Survivingknockout stabilizesafterWoundcheck',s.stable and s.death_failures==0 and e['woundSaves']==1 and s.stable_until_seconds==7300)
    s,e=hit(LifeState(40,5,wounds=(None,None,None)),5,knockout=True,melee=True,wound_natural=1,constitution_save_modifier=0)
    check('KnockoutcannotpreventfatalWoundfailure',s.dead and not s.stable)
    s=heal(LifeState(1,0,wounds=(None,None,None)),1)
    check('CriticalmaxHPonecanrecover',s.hp==1 and len(s.wounds)==3)
    check('HealingcriticalatmaximumdoesnotremoveHP',heal(LifeState(40,40,wounds=(None,None,None)),5).hp==40)
    check('Criticalhealingcapswithoutchangingmaximum',heal(LifeState(40,20,wounds=(None,None,None)),40).hp==39)
    s=LifeState(40,0,stable=True,stable_until_seconds=4*3600)
    check('Stabledeadlineuseselapsedtimeonce',stable_recovery(s,3*3600).hp==0 and stable_recovery(stable_recovery(s,8*3600),8*3600).hp==1)
    s=death_save(LifeState(40,0,death_successes=2,death_failures=2),20,regular_turn_id=1)
    check('Deathnat20healsandresetsbothcounters',s.hp==1 and s.death_successes==s.death_failures==0)
    s=death_save(LifeState(40,0,death_successes=2),10,regular_turn_id=1,stable_d4=1)
    check('Thirdsuccessstabilizesandresetscounters',s.stable and s.death_successes==s.death_failures==0)
    s=death_save(LifeState(40,0),10,regular_turn_id=1)
    check('Noextraorrepeatedturndeathsaves',rejects(lambda:death_save(s,10,regular_turn_id=1)) and rejects(lambda:death_save(s,10,regular_turn_id=2,regular=False)))
    check('StableandDeadcannotrolldeathsaves',rejects(lambda:death_save(LifeState(40,0,stable=True),10,regular_turn_id=1)) and rejects(lambda:death_save(LifeState(40,0,dead=True),10,regular_turn_id=1)))
    check('Already Stable cannot reroll its recovery deadline',rejects(lambda:stabilize(LifeState(40,0,stable=True,stable_until_seconds=7200),1,0)))
    check('Deadcannotreceiveordinaryhealing',rejects(lambda:heal(LifeState(40,0,dead=True),10)))
    s,e=hit(LifeState(40,0,stable=True,uses_death_saves=False),1)
    check('Ordinary knocked-out creature dies when unbuffered damage breaks Stable',s.dead and e['deathFailuresAdded']==0)
    s,e=hit(LifeState(40,5,uses_death_saves=False),5,knockout=True,melee=True,stable_d4=2)
    check('Ordinary creature can survive a legal knockout',s.stable and not s.dead)
    check('Invalid death-counter states are rejected',rejects(lambda:LifeState(10,5,death_failures=1)) and rejects(lambda:LifeState(10,0,stable=True,death_successes=1)) and rejects(lambda:LifeState(10,0,death_failures=3)))
    s=LifeState(40,20,wounds=(3,3,6))
    first=remove_wounds(s,[0]); second=remove_wounds(first,[0])
    check('DuplicateInjuriesretainseparatelinkswithoutstacking',active_injuries(s)=={3,6} and active_injuries(first)=={3,6} and active_injuries(second)=={6})
    check('RemovingWoundliftsCriticalceilingbutdoesnotheal',healing_ceiling(first)==40 and first.hp==20)
    check('WoundsreduceHDrecoverynotbelowzero',hit_dice_recovered(1,3)==0 and hit_dice_recovered(5,2)==3)
    check('Illegalrawrollsandnegativevaluesrejected',rejects(lambda:task_check(0,0,10)) and rejects(lambda:attack_roll(True,0,10)) and rejects(lambda:damage_event(LifeState(10,10),-1)))
    check('MissingrequiredWoundrollleavesinputintact',rejects(lambda:damage_event(LifeState(10,10),5)))
    cases=0; valid=True
    for maximum in (1,10,21,40):
        for hp in range(maximum+1):
            for temp in (0,10):
                for wounds in (0,2,3):
                    for damage in (0,1,5,10,20,30,40,80):
                        for die in (1,10,20):
                            initial=LifeState(maximum,hp,temp_hp=temp,wounds=(None,)*wounds)
                            snapshot=asdict(initial)
                            result,event=hit(initial,damage,wound_natural=die,constitution_save_modifier=2)
                            valid &= asdict(initial)==snapshot and 0<=result.hp<=maximum and result.temp_hp>=0 and len(result.wounds)<=3
                            valid &= event['woundSaves']<=1 and event['injuryRolls']<=1 and (not result.dead or result.hp==0)
                            valid &= not (hp>0 and event['deathFailuresAdded']>0)
                            cases+=1
    check(f'{cases} damage-state boundary scenarios preserveinvariants',valid)
    broken=[]
    for name in ['CORE_RESOLUTION_PLAYTEST.md','GAME_DEVELOPMENT_COVERAGE.md','DEVELOPMENT_ROADMAP.md']:
        path=ROOT/'docs/mechanics'/name
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if '://' not in link and not link.startswith('#') and not (path.parent/link.split('#')[0]).resolve().exists():broken.append(link)
    check('Coreandcoveragedocumentlinksresolve',not broken)
    errors=[c['name'] for c in checks if not c['pass']]
    report={'status':'PASS' if not errors else 'FAILED','checks':checks,'boundaryScenarios':cases,'errors':errors,
            'scope':'Core roll and HP/Wound/death reference invariants; source preservation and document links. Not full combat effects, defense evaluation, all conditions, treatment inventory, human balance or game completion.'}
    (ROOT/'docs/mechanics/CORE_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['status'],len(checks),'checks;',cases,'damage-state scenarios;',len(errors),'issues')
    for error in errors:print(error)
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
