"""Independent, finite reading checks for the submitted training/ownership evidence.

Uses Python's standard library and the extracted frozen input tree. It does not
import the submitted models, execute feat effects, authenticate campaign facts,
or certify complete acquisitions. Each training/history check is composite and
its components are exposed rather than multiplied into a headline test count.
"""
import argparse, hashlib, json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('root',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
r=a.root; R=r/'DescentReviewChanges/ReviewBible'; A=r/'docs/audit/2026-10-08/full-game'
def load(path): return json.loads(path.read_text(encoding='utf-8'))
f=load(R/'data/playtest/character_foundation.json'); classes={x['class']:x for x in f['classes']}
skills={s:k for k,v in f['skillAbilities'].items() for s in v}
anc=load(R/'data/playtest/ancestry_background_candidate.json');bg={x['id']:x for x in anc['backgrounds']}
human=next(x for x in anc['ancestries'] if x['id']=='human')
imp=next(x for x in human['variants'] if x['id']=='imperial-human')
equipment={x['id']:x for x in load(R/'data/playtest/equipment_source_catalog.json')['records']}
contracts={x['id']:x for x in load(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
fix=load(A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json')
t=load(A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json')
o=load(A/'FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json')
cases={x['id']:x for x in fix['cases']}
checks=[]
def check(sid,parts,observed=None):
 checks.append({'id':sid,'passed':all(parts.values()),'componentChecks':parts,'observed':observed})
def pb(n):return 2+(n-1)//4
# These finite source grant interpretations were read against the included
# first-class rows. Unprofiled Soldier grants and improvised instrument/natural
# profiles are deliberately not inferred, and an empty finite set is not a
# general assertion that no other authorized proficiency exists.
category_grants={'Bard':{'Simple'},'Monk':{'Simple'},'Paladin':{'Simple','Martial'},'Warrior':{'Martial'},'Thief':set(),'Shaman':set(),'Soldier':set()}
named_grants={'Monk':{'kama','nunchaku','quarterstaff'},'Thief':{'dagger','shortsword','crossbow, hand'},'Shaman':{'club','spear','quarterstaff'},'Soldier':{'repeating heavy crossbow'}}
def norm(s):return s.casefold().replace('’',"'").strip()
def known_training(actor, include_prior=True):
 first=actor['firstClass'];cl=classes[first]
 result={'scores':{k:sum(sorted(ds)[1:])+imp['combinedAbilityBonuses'][k] for k,ds in actor['abilityRolls'].items()},
         'skills':{actor['ancestrySkillChoice']:1,'Persuasion':1},'tools':set(),
         'armor':{s.strip().lower() for s in cl['armor'].split(';')},'weapons':set(),'totalLevel':sum(actor['classLevels'].values())}
 for skill in bg[actor['background']]['skillsSource'].split(', '):
  if skill in result['skills']:skill=actor['backgroundDuplicateSkillChoice']
  result['skills'][skill]=1
 for skill in actor['selectedClassSkills']:result['skills'][skill]=1
 result['tools'].update(actor['classToolChoices'])
 if actor['backgroundToolChoice'] is not None:result['tools'].add(actor['backgroundToolChoice'])
 fixed={'Shaman':["Alchemist's supplies",'Herbalism kit'], 'Thief':["Thieves' tools","Poisoner's kit"], 'Soldier':["Carpenter's tools"]}
 for name in fixed.get(first,[]):
  result['tools'].update(sid for sid,x in equipment.items() if x['category']=='Tools' and norm(x['name'])==norm(name))
 for sid,x in equipment.items():
  if not x['category'].casefold().endswith('weapons'):continue
  if (x['category'].split()[0] in category_grants[first] or norm(x['name']) in named_grants.get(first,set())
      or (first=='Thief' and 'Thrown' in x['sourceFields'].get('Properties',''))
      or (first=='Soldier' and x.get('sidearm') is True)):
   result['weapons'].add(sid)
 if include_prior:
  for g in actor['priorFeatChoices']:
   if g['featId']=='skill_expert':
    assert g['newSkill'] in skills and g['newSkill'] not in result['skills']
    result['skills'][g['newSkill']]=1
    assert result['skills'].get(g['expertiseSkill'])==1
    result['skills'][g['expertiseSkill']]=2
   elif g['featId']=='naturalist':
    assert result['scores']['WIS']>=13
    for sk in ['Nature','Survival']:result['skills'][sk]=2 if result['skills'].get(sk,0) else 1
   else:assert g['featId'] in {'alert','alertness','lucky'}
 return result

def evaluate(node,actor,tr,owned=()):
 k=node['kind']
 if k=='all':return bool(node['requirements']) and all(evaluate(n,actor,tr,owned) for n in node['requirements'])
 if k=='any':return bool(node['requirements']) and any(evaluate(n,actor,tr,owned) for n in node['requirements'])
 if k=='noPrintedPrerequisite':return True
 if k=='permanentAbility':return tr['scores'][node['ability']]>=node['minimum']
 if k=='totalCharacterLevel':return tr['totalLevel']>=node['minimum']
 if k=='classLevel':return actor['classLevels'].get(node['className'],0)>=node['minimum']
 if k=='ownedFeat':return node['id'] in owned
 if k=='actualProficiency':
  c=node['credential']
  if c in skills:return tr['skills'].get(c,0)>0
  if c in {'light armor','medium armor','shields'}:return c.removesuffix(' armor') in tr['armor']
  if c=='at least one actual tool':return bool(tr['tools'])
  if c=='Smith tools / Blacksmithing':return 'tools.smith-s-tools' in tr['tools']
  if c=='thieves tools mechanical disarm interface':return 'tools.thieves-tools' in tr['tools']
  if c=='bounded INT(Nature) anatomy bridge':return tr['skills'].get('Nature',0)>0
  if c=='legacy Knowledge (Monstrous Humanoids)':return False # no positive receipt in these witnesses
  raise ValueError(c)
 if k=='actualWeaponProficiency':
  c=node['category']
  if c=='permanently chosen actual profile':return actor.get('weaponChoice') in tr['weapons']
  for sid in tr['weapons']:
   w=equipment[sid];cat=w['category'].casefold();prop=w['sourceFields'].get('Properties','').casefold()
   if (c=='any actual profile' or c=='melee' and cat.endswith('melee weapons')
       or c=='ranged' and cat.endswith('ranged weapons') or c=='martial' and cat.startswith('martial ')
       or c=='Two-Handed-property' and 'two-handed' in prop
       or c in {'longbow','shortbow','whip'} and norm(w['name'])==c):return True
  return False
 if k=='permanentSkillModifier':
  if node['skill']=='thieves tools': ability='DEX'; factor=int('tools.thieves-tools' in tr['tools'])
  else:ability=skills[node['skill']];factor=tr['skills'].get(node['skill'],0)
  assert ability==node['ability']
  return factor>0 and (tr['scores'][ability]-10)//2+factor*pb(tr['totalLevel'])>=node['minimum']
 raise ValueError(k)

for trace in t['caseTraces']:
 sid=trace['featId'];actor=trace['actor'];derived=known_training(actor)
 observed=trace['derivedTraining'];op=actor['targetClassOpportunity'];cl=classes[actor['firstClass']]
 old=set();prior_valid=True
 for i,g in enumerate(actor['priorFeatChoices']):
  before=dict(actor,classLevels={actor['firstClass']:g['classLevel']},priorFeatChoices=actor['priorFeatChoices'][:i])
  prior_valid &= (g['classLevel'] in cl['asiClassLevels'] and g['classLevel']<op and g['featId'] not in old
                  and evaluate(contracts[g['featId']]['requirements'],before,known_training(before),old))
  old.add(g['featId'])
 q=evaluate(contracts[sid]['requirements'],actor,derived)
 grants=trace['paymentHistory']['grants'];expected_names=[g['featId'] for g in actor['priorFeatChoices']]+([sid] if q else [])
 components={
  'sourceAbilitiesOnce':derived['scores']==actor['permanentScores']==observed['scores'],
  'derivedSkills':derived['skills']==observed['skills'],
  'actualToolSet':derived['tools']==set(observed['tools']),
  'actualArmorSet':derived['armor']==set(observed['armor']),
  'actualProfileWeaponSet':derived['weapons']==set(observed['weapons']),
  'totalLevel':derived['totalLevel']==observed['totalLevel'],
  'orderedPriorPrerequisites':bool(prior_valid),
  'actualTargetOpportunity':op in cl['asiClassLevels'] and op<=actor['classLevels'][actor['firstClass']],
  'prerequisiteResult':q==trace['prerequisiteMet']==cases[trace['case']]['expectedPrerequisite'],
  'paidNamesAndCount':[g['identity'] for g in grants]==expected_names,
  'distinctPaidOpportunities':len({g['opportunity'] for g in grants})==len(grants),
  'partialScopeRetained':trace['completeFeatAcquisitionValidated'] is False,
 }
 check('training/'+trace['case'],components)

for trace in o['historyTraces']:
 parts={}
 for ix,event in enumerate(trace['history']):
  before=event['before'];actor=before['actor'];tr=known_training(actor);tr['scores']=before['payment']['scores']
  req=event['request'];sid=req['featId']
  if sid=='weaponFocus':actor=dict(actor,weaponChoice=req['choice'])
  q=evaluate(contracts[sid]['requirements'],actor,tr,{g['identity'] for g in before['payment']['grants']})
  op=actor['firstClass']+':'+str(req['classLevel'])
  parts[f'{ix}/prerequisite']=q==event['prerequisiteMet']
  parts[f'{ix}/earnedUnspent']=op in before['payment']['opportunities'] and not before['payment']['opportunities'][op]['spent']
  parts[f'{ix}/actualSchedule']=req['classLevel'] in classes[actor['firstClass']]['asiClassLevels'] and actor['classLevels'][actor['firstClass']]==req['classLevel']
  if event['outcome']=='acquired':
   parts[f'{ix}/grant']=q and event['after']['payment']['grants'][-1]['identity']==sid and event['after']['payment']['opportunities'][op]['spent']
  else:parts[f'{ix}/atomicRejection']=event['after']==before and not q
 final=trace['final'];actual=any(g['identity']==trace['case']['targetFeat'] for g in final['payment']['grants'])
 parts['expectedFinal']=actual==trace['case']['expectedTargetAcquired']
 check('ownership/'+trace['case']['id'],parts)

for name,rep in [('training',t),('ownership',o)]:
 check(name+'/reportedChecks',{'count':rep['checks']==len(rep['results']),'allPass':all(x['passed'] is True for x in rep['results']),'noFailures':rep['failures']==[]})
 check(name+'/allSourceBindings',{'bindingsMatch':all((r/x['path']).stat().st_size==x['bytes'] and hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in rep['sourceBindings'])})

training=set(fix['cohortIds']);ownership=set(o['cohortIds']);remaining={x['id'] for x in o['remaining']}
check('coverage/current',{'training48':len(training)==48,'ownership10':len(ownership)==10,'remaining56':len(remaining)==56,'disjoint':not(training&ownership or remaining&training or remaining&ownership),'identitiesInContracts':training|ownership|remaining<=contracts.keys(),'fullApprovalFalse':not t['candidateReadyForSubmission'] and not o['candidateReadyForSubmission']})
bycase={x['case']:x for x in t['caseTraces']};byhistory={x['case']['id']:x for x in o['historyTraces']}
check('boundary/lock-dex15',{'level4Reject':not bycase['lock_savant/modifier-4']['prerequisiteMet'],'level8Qualify':bycase['lock_savant/dex-fifteen-pb-three']['prerequisiteMet'],'arithmetic':(15-10)//2+pb(4)==4 and (15-10)//2+pb(8)==5})
check('boundary/TwoHanded-not-possession',{'versatileReject':not bycase['cleaving_momentum/shaman-versatile-thrown']['prerequisiteMet'],'proficientBowAcquisition':bycase['cleaving_momentum/simple-two-handed-shortbow']['prerequisiteMet'],'greatswordTrainingWithoutHolding':bycase['cleaving_momentum/longsword-held-full-martial-training']['prerequisiteMet']})
check('boundary/separate-old-new-dice',{'oneNewAvailable':byhistory['advanced-does-not-refill-old-die']['final']['initializations']['martialAdept']['superiorityPool']=={'die':'d6','maximum':2,'current':1}})
check('boundary/separate-reserves',{'hemocraft0of16':byhistory['life-hemocraft']['final']['initializations']['hemocraft']['recoveryReserve']=={'maximum':16,'current':0},'lifeDrinker16of16':byhistory['life-hemocraft']['final']['initializations']['life_drinker']['recoveryReserve']=={'maximum':16,'current':16}})
check('boundary/hemocraftGateDifferentFromChoice',{'INT12':byhistory['hemocraft-other-qualifying-ability']['final']['payment']['scores']['INT']==12,'CHA13':byhistory['hemocraft-other-qualifying-ability']['final']['payment']['scores']['CHA']==13,'selectedINT':byhistory['hemocraft-other-qualifying-ability']['final']['initializations']['hemocraft']['governingAbility']=='INT'})
check('boundary/masked-level-alternatives-disclosed',{'giantDisclosure':'not isolation' in byhistory['giant-owned-precision']['case']['branchNote'],'slayerDisclosure':'No earlier bonus grant' in byhistory['slayer-owned-favored-enemy']['case']['branchNote']})
result={'scope':'Independent finite source/projection consistency checks, not full acquisition or runtime execution; conditionally supplied histories are not campaign authentication.','checks':len(checks),'passed':sum(x['passed'] for x in checks),'failures':[x for x in checks if not x['passed']],'results':checks}
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'results','failures'}},indent=2))
raise SystemExit(bool(result['failures']))
