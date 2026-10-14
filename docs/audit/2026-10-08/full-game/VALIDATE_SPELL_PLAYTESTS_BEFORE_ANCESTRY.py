"""Source/coverage checks plus boundary tests for the common spell access/pricing step."""
from pathlib import Path
import hashlib
import json
import re
from build_spell_playtests import ROOT, OUT, SOURCE, DRAFT, FIELDS, source_catalog, read
from spell_playtest_rules import access_for, quote_cast, retune_amount, SpellRuleError
from fall_playtest_rules import Fall


checks = []


def check(name, condition):
    checks.append({'name':name, 'pass':bool(condition)})


def rejected(fn):
    try:
        fn()
    except SpellRuleError:
        return True
    return False


def main():
    packet = read(OUT/'catalog.json')
    source = source_catalog()
    core = read(ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    spells = {s['id']:s for s in packet['spells']}
    selected = [key for ids in read(DRAFT/'selected_sources.json').values() for key in ids]
    operational = [s for s in spells.values() if s['operational']]
    check('848 original IDs preserved exactly once',len(packet['spells'])==len(spells)==848 and set(source)==set(spells))
    check('936 source placements preserved exactly',sum(len(s['source']['original']['placements']) for s in spells.values())==936)
    check('All catalog objects preserved without alteration',all(source[k]==s['source']['original'] for k,s in spells.items()))
    check('Core936 full entries retained',read(SOURCE/'core_v2_spells.json')==core['spells'] and len(core['spells'])==936)
    check('Sources match pre-build hashes',all(hashlib.sha256((ROOT/h['path']).read_bytes()).hexdigest()==h['sha256'] for h in read(SOURCE/'source_hashes.json')))
    check('All269 individually reviewed selected IDs have operational drafts',len(selected)==len(set(selected))==269 and set(selected)=={s['id'] for s in operational})
    check('Remaining579 explicitly blocked',sum(s['status']=='blocked-pending-operational-review' and s['operational'] is None for s in spells.values())==579)
    check('No unreviewed spell selectable',all(rejected(lambda s=s:access_for(s,'Wizard',20)) for s in spells.values() if not s['operational']))
    check('Complete typed operational fields',all(all(k in s['operational'] for k in FIELDS)
          and isinstance(s['operational']['rangeFeet'],int) and not isinstance(s['operational']['rangeFeet'],bool)
          and s['operational']['rangeFeet']>=0 and isinstance(s['operational']['concentration'],bool)
          and isinstance(s['operational']['components'],list)
          and all(isinstance(s['operational'][k],str) and s['operational'][k].strip() for k in FIELDS if k not in ['rangeFeet','concentration','components']) for s in operational))
    check('Components have explicit vocabulary',all(set(s['operational']['components'])<={'V','S','F','M'} for s in operational))
    check('Core prices preserved for every class-specific rank',all(a['baseRpCost']==core['resonance_costs'][str(a['rank'])] for s in spells.values() for a in s['classAccess'].values()))
    check('Class access ranks and levels preserved exactly',all({c:a['rank'] for c,a in s['classAccess'].items()}==source[k]['classRanks'] and {c:a['minimumClassLevel'] for c,a in s['classAccess'].items()}==source[k]['classLearnLevels'] for k,s in spells.items()))
    check('Oracle Soldier Warrior never gain ordinary access',all(not {'Oracle','Soldier','Warrior'}.intersection(s['classAccess']) for s in spells.values()))
    trials = 0
    valid_gates = True
    for s in spells.values():
        for cls, a in s['classAccess'].items():
            for level in range(1,21):
                trials += 1
                allowed = not rejected(lambda:access_for(s,cls,level,require_operational=False))
                valid_gates &= allowed == (level >= a['minimumClassLevel'])
    check(f'All {trials} class/level access boundaries',valid_gates)
    covered = {}
    for cls, prog in packet['classProgression'].items():
        if not prog['learnLevels']:
            continue
        cantrip = [s for s in operational if cls in s['classAccess'] and s['classAccess'][cls]['rank']==0]
        rank1 = [s for s in operational if cls in s['classAccess'] and s['classAccess'][cls]['rank']==1]
        covered[cls]={'cantripOptions':len(cantrip),'rank1Options':len(rank1)}
    check('Starter choice coverage for all14 Weave classes',len(covered)==14 and all(x['cantripOptions']>=3 and x['rank1Options']>=6 for x in covered.values()))
    def quote(key='arcane-ray', **overrides):
        args=dict(class_name='Mage',class_level=1,available_spell_ids={key},rp=30,max_rp=30,
                  dissonance=0,proficiency=2,casting_modifier=3)
        args.update(overrides)
        return quote_cast(spells[key],**args)
    check('First cantrip zero common cost/strain',quote()['cost']==0 and quote()['dissonanceAddedBeforeClassInterface']==0)
    check('Repeated cantrip adds Refrain despite rank0',quote(previous_spell_id='arcane-ray',previous_refrain=0)['dissonanceAddedBeforeClassInterface']==1)
    check('Refrain caps at3',quote(previous_spell_id='arcane-ray',previous_refrain=3)['refrain']==3)
    check('Different named spell clears Refrain, not accumulatedD',quote(previous_spell_id='sparkbolt',previous_refrain=3,dissonance=5)['dissonanceBeforeClassInterface']==5)
    check('Rank1 baseline costs2RP',quote('elemental-bolt')['cost']==2)
    check('Strain surcharge evaluated before cast',quote('elemental-bolt',dissonance=7)['cost']==3 and quote('elemental-bolt',dissonance=10)['cost']==4)
    check('Ordinary fractured ranked cast rejected',rejected(lambda:quote('elemental-bolt',dissonance=13)))
    check('Fractured cantrip remains legal without ranked surcharge',quote(dissonance=13)['cost']==0)
    check('Explicit traumatic exception pays cost and trauma',quote('elemental-bolt',dissonance=13,traumatic_casting=True)['cost']==5 and quote('elemental-bolt',dissonance=13,traumatic_casting=True)['trauma']==3)
    check('Insufficient RP rejected',rejected(lambda:quote('elemental-bolt',rp=1)))
    check('Unknown or unprepared spell rejected',rejected(lambda:quote(available_spell_ids=set())))
    check('Invalid negative and over-cap pools rejected',rejected(lambda:quote(rp=-1)) and rejected(lambda:quote(rp=31)))
    check('Rank/access not gained by abundantRP',rejected(lambda:quote('elemental-bolt',class_name='Dragoon',class_level=2)))
    check('Paladin cantrip gate2 retained',rejected(lambda:quote('arcane-ward',class_name='Paladin',class_level=1)) and quote('arcane-ward',class_name='Paladin',class_level=2)['rank']==0)
    check('Resonance Shield mandatory extraRP',quote('resonance-shield')['cost']==spells['resonance-shield']['classAccess']['Mage']['baseRpCost']+1)
    check('Resonance Shield source1d4 retained','1d4' in spells['resonance-shield']['operational']['effect'] and 'Gain 5 temporary' not in spells['resonance-shield']['operational']['effect'])
    check('Core numeric Retune rounding bounded',retune_amount(6,3)==5 and retune_amount(1,-5)==0)
    # Same shared name can have different ranks; match each quote to its own class entry.
    multi = [s for s in operational if len({a['rank'] for a in s['classAccess'].values()})>1]
    check('Multi-rank spells priced perclass',bool(multi) and all(quote_cast(s,c,20,available_spell_ids={s['id']},rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=3)['cost']==a['baseRpCost']+s['additionalRpCost'] for s in multi for c,a in s['classAccess'].items()))
    # Regression cases from the two-agent notebook conference: cumulative distance
    # must avoid a harmless final remainder, and fixed markers prevent extra steps.
    def land(height, slowed=False):
        fall = Fall(height, 1, 2)
        fall.set_feather_fall(slowed)
        steps = 0
        while fall.height_remaining:
            result = fall.step(fall.next_round, 2)
            steps += 1
        return steps, result['damageD6']
    check('Ordinary fall thresholds and cumulative remainders',all(land(h)==expected for h,expected in [(10,(1,0)),(20,(1,1)),(300,(1,10)),(310,(2,10)),(610,(3,10))]))
    check('Slowed landing keeps cumulative distance and3d6cap',land(310,True)==(6,3) and land(10,True)==(1,0))
    fall = Fall(310,1,2)
    fall.set_feather_fall(True)
    fall.step(2,2)
    fall.step(3,2)
    fall.set_feather_fall(False)
    check('Expiry after120ft leaves190uncontrolled for9d6',fall.next_round==4 and fall.step(4,2)['damageD6']==9)
    fall = Fall(610,1,2)
    fall.step(2,2)
    fall.set_feather_fall(True)
    check('Late slowing dissipates uncontrolled momentum, retains distance',fall.uncontrolled_distance==0 and fall.total_distance==300)
    check('Premature repeated or moved marker rejected',rejected(lambda:fall.step(2,2)) and rejected(lambda:fall.step(3,1)) and rejected(lambda:fall.step(4,2)))
    while fall.height_remaining:result=fall.step(fall.next_round,2)
    check('Late slowing still caps eventual impact',result['damageD6']==3)
    check('Resolved impact cannot be undone',rejected(lambda:fall.set_feather_fall(True)) and rejected(lambda:fall.step(fall.next_round,2)))
    # In unchanged regular order, each participant has a turn between the initiating
    # turn and the end-of-slot marker in the next round, for every relative order.
    check('All initiative orders have a normal rescue opportunity',all(
        any((r,s) > (1,origin) and (r,s) <= (2,origin) and s==actor
            for r in (1,2) for s in range(6))
        for origin in range(6) for actor in range(6)))
    root_docs=[ROOT/'docs/mechanics'/x for x in ['SPELL_PLAYTEST_STARTER.md','SPELL_INTEGRATION_RULES.md','DEVELOPMENT_ROADMAP.md']]
    broken=[]
    for p in root_docs:
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' not in link and not link.startswith('#') and not (p.parent/link.split('#')[0]).resolve().exists():broken.append(link)
    check('Development document links resolve',not broken)
    failures=[x['name'] for x in checks if not x['pass']]
    result={'status':'PASS' if not failures else 'FAILED','sourceSpells':848,'operationalDrafts':len(operational),
            'unfinishedSpells':len(spells)-len(operational),'accessBoundaryCases':trials,'classStarterCoverage':covered,
            'checks':checks,'errors':failures,'limits':'Source/schema/access/common-cost checks and provisional falling regressions only. Not all spell effects, class cadence hooks, human balance, full baseline completion or live-app integration.'}
    (ROOT/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'],len(checks),'checks;',trials,'access boundaries;',len(failures),'issues')
    for error in failures:print(error)
    if failures:raise SystemExit(1)


if __name__ == '__main__':main()
