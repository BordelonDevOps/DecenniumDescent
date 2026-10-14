"""Check real source bindings and selected advancement boundary examples."""
from pathlib import Path
import hashlib
import json
import re
from character_foundation import (ability_modifier, base_maximum_hp,
    clamp_after_capacity_change, merged_rp, new_class_prerequisite_failures,
    point_buy_cost, proficiency_bonus, validate_class_levels)

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
data=json.loads((ROOT/'data/playtest/character_foundation.json').read_text(encoding='utf-8'))
profiles={x['class']:x for x in data['classes']}
results=[]

def check(name,condition):
    results.append({'name':name,'pass':bool(condition)})

def rejects(name,fn):
    try: fn()
    except ValueError: check(name,True)
    else: check(name,False)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

check('Exactly the 17 protected Base classes; no orphan class',len(profiles)==17 and not {'Fighter','Swashbuckler'}&set(profiles))
check('Twenty basic skills include both omitted UI skills',sum(map(len,data['skillAbilities'].values()))==20 and 'Engineering' in data['skillAbilities']['INT'] and 'Reputation' in data['skillAbilities']['CHA'])
check('Reviewed HD exceptions retained',[profiles[n]['hitDie'] for n in ['Mirrorsage','Oracle','Ranger']]==[8,6,8])
check('Monk wealth has no times-ten; Oracle uses 3d4 times-ten',profiles['Monk']['startingWealth']=={'diceCount':5,'dieSides':4,'multiplierGp':1} and profiles['Oracle']['startingWealth']=={'diceCount':3,'dieSides':4,'multiplierGp':10})
check('Oracle ASI exception and ordinary Bard ASIs',profiles['Oracle']['asiClassLevels']==[4,8,14,19] and profiles['Bard']['asiClassLevels']==[4,8,12,16,19])
skills={x for group in data['skillAbilities'].values() for x in group}
check('Every concrete class skill list is legal and large enough',all(len(set(p['skillOptions']))==len(p['skillOptions']) and set(p['skillOptions'])<=skills and 0<p['skillChoices']<=len(p['skillOptions']) for p in profiles.values()))
check('Oracle Spellcraft substitution is only a starting choice', 'Arcana' in profiles['Oracle']['skillOptions'] and 'Spellcraft' not in profiles['Oracle']['skillOptions'])
check('Tinker Engineering is an option, not a third grant','Engineering' in profiles['Tinker']['skillOptions'] and profiles['Tinker']['skillChoices']==2)
check('Agent and Soldier multiclass gates retain CON',profiles['Crimson Agent']['multiclassPrerequisites']=={'DEX':13,'CON':13} and profiles['Soldier']['multiclassPrerequisites']=={'STR':13,'CON':13})
check('Paladin multiclass row has no heavy armor or saves','heavy' not in profiles['Paladin']['multiclassProficiencies'].lower() and 'sav' not in profiles['Paladin']['multiclassProficiencies'].lower())
check('Separate Dragoon multiclass row preserved','shields' in profiles['Dragoon']['multiclassProficiencies'] and 'Shields' not in profiles['Dragoon']['armor'])

bindings=0
for name,p in profiles.items():
    path=GAME/p['classCandidatePath']
    active=json.loads(path.read_text(encoding='utf-8'))
    same=sha(path)==p['classCandidateSha256'] and p['rpByClassLevel']==active['rpByClassLevel'] and len(p['rpByClassLevel'])==20
    check(name+' exact reviewed class pool and source hash',same)
    for level in range(1,21):
        found=merged_rp(profiles,{name:level},[name])['maximum']
        expected=0 if p['weaveTier']=='none' else active['rpByClassLevel'][level-1]
        if found!=expected: check(f'{name} level {level} source pool',False)
        bindings+=1
check('340 class-level pool bindings checked',bindings==340)

check('Negative ability modifiers floor correctly',[ability_modifier(x) for x in [3,8,9,10,13,16]]==[-4,-1,-1,0,1,3])
check('All PB transition boundaries',[proficiency_bonus(x) for x in [1,4,5,8,9,12,13,16,17,20]]==[2,2,3,3,4,4,5,5,6,6])
check('Point buy handles nonlinear 14/15 costs',point_buy_cost([15,15,15,8,8,8])==27 and point_buy_cost([15,14,13,12,10,8])==27)
rejects('Point buy rejects overspend',lambda:point_buy_cost([15,15,15,9,8,8]))
rejects('Point buy rejects out-of-range score',lambda:point_buy_cost([16,8,8,8,8,8]))
rejects('Point buy rejects wrong score count',lambda:point_buy_cost([8]*5))
rejects('Point buy rejects booleans',lambda:point_buy_cost([True,8,8,8,8,8]))
rejects('Combined level 21 is illegal',lambda:merged_rp(profiles,{'Bard':11,'Mage':10},['Bard','Mage']))
rejects('Acquisition order cannot duplicate class',lambda:merged_rp(profiles,{'Cleric':6,'Druid':6},['Cleric','Cleric','Druid']))
rejects('Unlisted Base class cannot acquire levels',lambda:merged_rp(profiles,{'Swashbuckler':1},['Swashbuckler']))

hp=base_maximum_hp(profiles,[{'class':'Bard','base':8}],14)
check('Bard initial HP and d8 record',hp=={'baseMaximum':10,'contributions':[10],'hitDiceBySize':{'8':1}})
hp2=base_maximum_hp(profiles,[{'class':'Bard','base':8},{'class':'Mage','base':4}],14)
check('New Mage class1 uses later-level base and separate HD',hp2=={'baseMaximum':16,'contributions':[10,6],'hitDiceBySize':{'8':1,'6':1}})
rejects('First character level cannot use lower fixed base',lambda:base_maximum_hp(profiles,[{'class':'Bard','base':5}],14))
rejects('HP roll cannot exceed gained class HD',lambda:base_maximum_hp(profiles,[{'class':'Bard','base':8},{'class':'Mage','base':8}],14))
floor_records=[{'class':'Mage','base':6},{'class':'Mage','base':1}]
check('Retroactive CON recomputes individual floors',base_maximum_hp(profiles,floor_records,6)['baseMaximum']==5 and base_maximum_hp(profiles,floor_records,8)['baseMaximum']==6)
check('Capacity change cannot heal or revive',clamp_after_capacity_change(6,17)==6 and clamp_after_capacity_change(0,17)==0 and clamp_after_capacity_change(19,17)==17)

mixed=merged_rp(profiles,{'Cleric':6,'Druid':6,'Wizard':1},['Druid','Cleric','Wizard'])
check('Three-class example:19RP, acquisition tie, no tertiary bonus',mixed['maximum']==19 and mixed['primary']['class']=='Druid' and mixed['secondary']['class']=='Cleric' and mixed['noncontributingWeaveClasses'][0]['class']=='Wizard')
mix=merged_rp(profiles,{'Bard':10,'Wizard':1},['Bard','Wizard'])
check('Higher tier beats larger lower-tier class/pool',mix['primary']['class']=='Wizard' and mix['secondary']['class']=='Bard' and mix['maximum']==profiles['Wizard']['rpByClassLevel'][0]+6)
mix=merged_rp(profiles,{'Cleric':1,'Wizard':1},['Cleric','Wizard'])
check('Larger equal-tier/equal-level pool beats earlier acquisition',mix['primary']['class']=='Wizard')
mix=merged_rp(profiles,{'Oracle':10,'Soldier':5,'Warrior':5},['Oracle','Soldier','Warrior'])
check('Oracle plus martials creates no RP',mix['maximum']==0 and mix['primary'] is None)
mix=merged_rp(profiles,{'Bard':5,'Oracle':5},['Bard','Oracle'])
check('Oracle does not reduce or increase single Weave constituent',mix['maximum']==profiles['Bard']['rpByClassLevel'][4] and mix['secondary'] is None)
scores={x:13 for x in ['STR','DEX','CON','INT','WIS','CHA']}
check('All held and new prerequisites pass at 13',not new_class_prerequisite_failures(profiles,['Bard','Cleric'],'Crimson Agent',scores))
scores['CON']=12
failed=new_class_prerequisite_failures(profiles,['Bard'],'Crimson Agent',scores)
check('Agent CON gate not replaced by INT',failed==[{'class':'Crimson Agent','ability':'CON','required':13,'actual':12}])
scores['CHA']=12
failed=new_class_prerequisite_failures(profiles,['Bard','Cleric'],'Mage',scores)
check('Earlier held class gate still applies on third-class entry',failed==[{'class':'Bard','ability':'CHA','required':13,'actual':12}])
check('Existing class advancement is not new-class gate',not new_class_prerequisite_failures(profiles,['Bard'],'Bard',scores))
check('First Base class needs no multiclass score gate',not new_class_prerequisite_failures(profiles,[],'Bard',scores))

sub=json.loads((AUDIT/'CHARACTER_FOUNDATION_SUBMISSION.json').read_text(encoding='utf-8'))
changed=[p['path'] for p in sub['protectedFiles'] if not Path(p['path']).exists() or sha(Path(p['path']))!=p['sha256']]
check('All protected books/classes/companion/spell files unchanged',not changed)
check('Evidence snapshot still matches its source hash',sha(AUDIT/'CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json')==data['sourceEvidenceSha256'])

out={'status':'PASS' if all(r['pass'] for r in results) else 'FAIL','checks':len(results),
     'classLevelPoolBindings':bindings,'protectedFiles':len(sub['protectedFiles']),
     'changedProtectedFiles':changed,'scope':'Source preservation and selected reference calculations only; no live UI, full character legality, balance or whole-game certification.',
     'results':results}
path=ROOT/'docs/mechanics/CHARACTER_FOUNDATION_VALIDATION.json'
path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
if out['status']!='PASS':
    print(json.dumps([x for x in results if not x['pass']],indent=2))
    raise SystemExit(1)
