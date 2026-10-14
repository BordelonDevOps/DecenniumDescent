from pathlib import Path
import json
from healing_source_extensions import *
from healing_playtest_rules import LifeState,survival_damage_event,healing_packet,HealingReduction
ROOT=Path(__file__).resolve().parents[1]

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    check('Immunity0 cannot remove explicit minimum backlash damage',zealot_backlash(0),1)
    check('An actual suppression source cancels the whole backlash',zealot_backlash(4,explicitly_suppressed=True),0)
    out,event=survival_damage_event(LifeState(20,1),zealot_backlash(0),wound_natural=20)
    check('Backlash is not survival floor and can drop ally to0',(out.hp,out.dead,event['woundSaves']),(0,False,1))
    out,event=survival_damage_event(LifeState(20,1,temp_hp=1),zealot_backlash(0))
    check('TemporaryHP still absorbs resolved minimum backlash',(out.hp,out.temp_hp,event['actualDamageDealt']),(1,0,1))
    healed=healing_packet(LifeState(20,1),8,hp_gain_prohibited=True)['state']
    out,event=survival_damage_event(healed,zealot_backlash(2),wound_natural=20)
    check('Blocked healing does not cancel later backlash',(out.hp,event['resolvedDamage']),(0,2))
    kw=dict(shared_cap_total=7,scale=2,roll_instance_id='cap-roll')
    check('No recipients skips division and healing',crown_burn_healing(20,[],**kw),[])
    check('Positive packet numeric0 generates no Crown healing',crown_burn_healing(0,['a'],**kw),[])
    rows=crown_burn_healing(23,['a','b','c'],**kw)
    check('Shared cap applies equally against floored share',[r['sourceBase'] for r in rows],[7,7,7])
    check('One shared roll with real S dice survives provenance',[(r['rollInstanceId'],r['diceCount']) for r in rows],[('cap-roll',2)]*3)
    rows=crown_burn_healing(5,['a','b'],**kw)
    check('Damage share is floored once before recipient pipeline',[r['sourceBase'] for r in rows],[2,2])
    rows=crown_burn_healing(1,['a','b','c'],**kw)
    check('Positive numeric pool invokes printed source minimum1',[r['sourceBase'] for r in rows],[1,1,1])
    check('Source minimum cannot bypass recipient healing prohibition',healing_packet(LifeState(20,1),rows[0]['sourceBase'],hp_gain_prohibited=True)['actualHpGained'],0)
    rejects('Recipients cannot be duplicated to change division',lambda:crown_burn_healing(10,['a','a'],**kw))
    rejects('More than3 recipients remains illegal',lambda:crown_burn_healing(10,list('abcd'),**kw))
    declared=crown_burn_healing(12,['a','b','c'],**kw)
    living={'a','c'}
    check('Later-ineligible recipient does not change locked denominator',
          [(r['targetId'],r['sourceBase']) for r in declared if r['targetId'] in living],[('a',4),('c',4)])
    records=[MendRecord('one','creature-A','ally',9,'roll-one'),MendRecord('two','creature-B','ally',7,'roll-two')]
    components=dual_mend_components(records)
    check('Two paid eligible Mend profiles survive Dual Echo classification',[r['sourceBase'] for r in components],[4,3])
    check('Same ally may receive both supplied components',[r['targetId'] for r in components],['ally','ally'])
    check('Copied half amounts carry zero new dice',[r['diceCount'] for r in components],[0,0])
    target=LifeState(20,1)
    penalty=HealingReduction('desecrated','desecrated','per-die',1)
    for c in components:target=healing_packet(target,c['sourceBase'],dice_count=c['diceCount'],reductions=[penalty])['state']
    check('Per-die penalty cannot invent dice on flat half copies',target.hp,8)
    rejects('Same source creature cannot supply both captures',lambda:dual_mend_components([records[0],MendRecord('two','creature-A','ally',7,'two-roll')]))
    rejects('Same record cannot be consumed twice',lambda:dual_mend_components([records[0],records[0]]))
    report={'status':'PASS','reviewStatus':'REVIEWED / reference-VALIDATED; three selected primitives only',
            'scope':'Three corrected source interfaces only: Zealot backlash, Crown Burn pooled/shared healing and Dual Echo two-Mend numeric components. Caller ownership/cost/action, scheduler and broader copy lifecycle are not implemented here.',
            'checkCount':len(checks),'checks':checks}
    (ROOT/'docs/mechanics/HEALING_EXTENSION_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS{len(checks)} selected healing-extension checks; bounded GPT closure recorded.')
if __name__=='__main__':main()
