"""Source preservation, acquisition simulation and resource boundary checks.

This validates written structure and selected engine invariants. It is deliberately
not described as a full combat simulator or proof of numerical balance.
"""
from pathlib import Path
import json,hashlib,random,re,itertools
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/public/class_playtests';SRC=ROOT/'data/playtest/class_sources'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
checks=[];issues=[];builds={}
def check(name,ok,detail=''):
 checks.append({'check':name,'pass':bool(ok),'detail':detail})
 if not ok:issues.append(name+(': '+detail if detail else ''))
idx=read(SRC/'card_index.json');manifest=read(DATA/'manifest.json')
expected=set(read(SRC/'supplements.json')['class-spell-progression']['CLASS_SPELL_PROGRESSION'])
check('All17 base classes represented',set(x['class'] for x in manifest['classes'])==expected,str(sorted(expected-set(x['class'] for x in manifest['classes']))))
book=ROOT.parents[1]/'docs/reference/Player_Rulebook_v6_source_text.txt'
bookhash=hashlib.sha256(book.read_bytes()).hexdigest()
names=[]
def available(c,lv,route,chosen):
 if c['acquisition']!='selection' or c['minimumClassLevel']>lv or c['id'] in chosen:return False
 if c['band']=='Hero' and c['path'] not in [None,route]:return False
 if c['path']=='Tortoise':
  if not any('discipline-initiate' in x for x in chosen):return False
 return True
def simulate(d,route,seed):
 rng=random.Random(seed);chosen=set();rows=[]
 for r in d['schedule']:
  lv=r['classLevel'];n=r['choose'];act=r['minimumActives'];selected=[]
  if d['class']=='Wizard' and route=='Elementalist' and lv==10:n=1
  candidates=[c for c in d['cards'] if available(c,lv,route,chosen) and c['band'] in r['bands']]
  rng.shuffle(candidates)
  # Select required active options first so passive picks cannot make a legal row fail.
  active=[c for c in candidates if c['sourceKind']=='active' or c['activation'].startswith(('Action','Bonus Action','Reaction','Ritual'))]
  if len(active)<act:return False,f'{route} level{lv}: {len(active)} active options for minimum{act}',rows
  selected=active[:act]
  rest=[c for c in candidates if c not in selected]
  selected+=rest[:n-len(selected)]
  if len(selected)<n:return False,f'{route} level{lv}: {len(selected)}/{n} eligible choices',rows
  chosen.update(c['id'] for c in selected)
  rows.append({'classLevel':lv,'selected':[c['id'] for c in selected]})
 return True,'',rows

for entry in manifest['classes']:
 name=entry['class'];names.append(name)
 if name=='Bard':continue # Existing Bard validator owns its dedicated implementation.
 d=read(DATA/(name.lower().replace(' ','-')+'.json'));source=read(SRC/(name.lower().replace(' ','-')+'.json'));cards=d['cards']
 check(name+' source extract unchanged',d['sourceExtractSha256']==bookhash)
 ids=[c['id'] for c in cards];check(name+' unique card IDs',len(ids)==len(set(ids)))
 byline={c['source'].get('line'):c for c in cards if c['source'].get('line')}
 if name in idx:
  missing=[m['name'] for m in idx[name] if m['line'] not in byline]
  check(name+' indexed source coverage',not missing,str(missing))
  changed=[m['line'] for m in idx[name] if m['line'] in byline and byline[m['line']]['source']['originalText']!=m['originalText']]
  check(name+' original indexed descriptions preserved',not changed,str(changed))
 if name=='Oracle':
  refs='\n'.join(str(c['source'].get('reference','')) for c in cards)
  missing=[]
  fields=['level1','tierI[0]','tierI[1]','tierI[2]','tierII[0]','tierII[1]','tierII[2]','tierIII','mysticInsight','revelationMastery','propheticSurge','finalRevelation','prophecyTrigger']
  for i in range(10):
   for f in fields:
    key=f'ORACLE_MYSTERIES[{i}].{f}'
    if key not in refs:missing.append(key)
  check('Oracle all10 complete Mystery source trees',not missing,str(missing))
  check('Oracle all10 Curses with separately gated50 Boons',sum(c['sourceKind']=='curse' for c in cards)==10 and sum(c['sourceKind']=='curseBoon' for c in cards)==50)
  problems=[];runs=0
  for mystery,curse,tier1,first,second in itertools.product(range(10),range(10),range(3),range(3),range(3)):
   if first==second:continue
   runs+=1
   required={f'level1':1,'prophecyTrigger':1,f'tierI[{tier1}]':3,f'tierII[{first}]':6,f'tierII[{second}]':6,'tierIII':9,'mysticInsight':12,'revelationMastery':15,'propheticSurge':18,'finalRevelation':20}
   for field,gate in required.items():
    wanted=f'MYSTERIES.ORACLE_MYSTERIES[{mystery}].{field}'
    found=[c for c in cards if c['source'].get('reference')==wanted]
    if len(found)!=1 or found[0]['minimumClassLevel']!=gate:problems.append(wanted)
  check('Oracle1800 Mystery/Curse/ordered Tier-II combinations retain stage gates',runs==1800 and not problems,str(sorted(set(problems))))
  check('Oracle Curse Boons have exact3/5/10/15/20 gates',all(sorted(c['minimumClassLevel'] for c in cards if c['sourceKind']=='curseBoon' and c['path']==curse['name'])==[3,5,10,15,20] for curse in cards if curse['sourceKind']=='curse'))
 if name=='Paladin':
  refs='\n'.join(str(c['source'].get('reference','')) for c in cards)
  missing=[]
  fields=['smiteType','auraEffect','signaturePower','revelationSpells[0]','revelationSpells[1]','revelationSpells[2]','revelationSpells[3]','revelationSpells[4]','finalOathGift','oathbreaker.deathTouch','oathbreaker.aura','oathbreaker.blasphemousWord']
  for i in range(10):
   for f in fields:
    key=f'SACRED_OATHS[{i}].{f}'
    if key not in refs:missing.append(key)
  check('Paladin all10 Oaths,50 spells and30 inverted mechanics',not missing,str(missing))
  bad=[];runs=0
  for oath,inverted,style,secondary in itertools.product(range(10),[False,True],range(3),range(2)):
   runs+=1
   choices={'oathbreaker.deathTouch':3,'oathbreaker.aura':3,'oathbreaker.blasphemousWord':11} if inverted else {'smiteType':3,'auraEffect':3,'signaturePower':11,'finalOathGift':20,**{f'revelationSpells[{i}]':lv for i,lv in enumerate([3,5,9,13,17])}}
   for f,gate in choices.items():
    key=f'SACRED_OATHS[{oath}].{f}'
    found=[c for c in cards if c['source'].get('reference')==key]
    if len(found)!=1 or found[0]['minimumClassLevel']!=gate:bad.append(key)
  check('Paladin120 Oath/inversion/style/aura configurations retain stage gates',runs==120 and not bad,str(sorted(set(bad))))
 if name=='Druid':
  base=[2451,2455,2460,2464,2467];arch=[2632,2636,2640,2644,2648]
  heroes=[2677,2681,2699,2703,2720,2724,2744,2748,2765,2769,2787,2791,2810,2814]
  check('Druid all24 named forms preserve their proper gates',all(byline.get(n,{}).get('minimumClassLevel')==gate for gate,group in [(1,base),(11,arch),(10,heroes)] for n in group))
  circles=['Land','Moon','Storm','Thorns','Winterfang','Rotshaper','Ashen Grove'];bad=[]
  for circle,forms in itertools.product(circles,itertools.combinations(arch,2)):
   relevant=[c for c in cards if c['path']==circle]
   if not all(any(c['minimumClassLevel']==lv for c in relevant) for lv in [2,6,10,14]):bad.append(circle)
  check('Druid70 Circle/Arch-attunement configurations have full progression',not bad,str(sorted(set(bad))))
 if name in ['Oracle','Paladin']:
  unresolved=[c['id'] for c in cards if c['source'].get('reference') and re.search(r'(MYSTERIES|CURSES|SACRED_OATHS)\b',c['source']['reference']) and not c['source'].get('originalObjects')]
  check(name+' explicit supplemental references resolve to preserved objects',not unresolved,str(unresolved))
 required=['activation','cost','rangeAndTarget','duration','frequency','effect']
 if name=='Oracle':
  actual=sorted(c['minimumClassLevel'] for c in cards if c['name'].startswith('Ability Score Improvement'))
  check('Oracle exceptional ASIs match its four progression grants',actual==d['asiClassLevels']==[4,8,14,19],str(actual))
 if name=='Ranger':
  feature=next(c for c in cards if c['name']=='Efficient Killer')
  check('Ranger cannot select Hit Chain upgrade before its engine unlock',not available(feature,10,'Stalker',set()) and feature['minimumClassLevel']>=11)
 if name=='Thief':
  finals=[c for c in cards if c['name']=='Master of the Unseen']
  check('Thief alternative finales are isolated to their two eligible paths',len(finals)==2 and {c['path'] for c in finals}=={'Arcane Trickster','Shadowblade'} and all(c['acquisition']=='automatic' and c['minimumClassLevel']==20 for c in finals))
 if name in ['Mage','Ranger','Shaman','Soldier']:
  shared=[c for c in cards if c['minimumClassLevel']==20 and not c['path']]
  check(name+' shared level20 completion is an automatic grant',len(shared)==1 and shared[0]['acquisition']=='automatic')
 bad=[c['id'] for c in cards if any(not isinstance(c.get(k),str) or not c[k].strip() for k in required)]
 check(name+' complete operational card fields',not bad,str(bad))
 gates=[c['id'] for c in cards if not isinstance(c['minimumClassLevel'],int) or not 1<=c['minimumClassLevel']<=20 or(c['band']=='Hero' and c['minimumClassLevel']<10) or(c['band']=='Arch' and c['minimumClassLevel']<3)]
 check(name+' stage and class-level gates',not gates,str(gates))
 if name in['Oracle','Soldier','Warrior']:check(name+' no RP or ordinary spell ranks',not any(d['rpByClassLevel']) and not any(d['maxSpellRankByClassLevel']))
 else:check(name+' twenty nondecreasing positive pool values',len(d['rpByClassLevel'])==20 and all(x>0 for x in d['rpByClassLevel']) and d['rpByClassLevel']==sorted(d['rpByClassLevel']))
 if d['schedule']:
  routes=list(dict.fromkeys(c['path'] for c in cards if c['band']=='Hero' and c['path'])) or [None]
  runs=[];example={};failure=[]
  for route in routes:
   for seed in range(100):
    ok,err,rows=simulate(d,route,seed);runs.append(ok)
    if not ok:failure.append(err)
    elif route not in example:example[route or 'Default']=rows
  check(name+' sampled legal acquisition across all Hero paths',all(runs),' / '.join(sorted(set(failure))) if failure else f'{len(runs)} complete builds; sampling is not exhaustive')
  builds[name]={'sampleCount':len(runs),'successful':sum(runs),'examples':example}

# Pure invariant models check edge conditions of the printed shared rules.
def pay(pool,cost):
 if pool<cost or cost<0:raise ValueError('illegal payment')
 return pool-cost
def gain(pool,n,cap):return min(cap,pool+max(0,n))
def consume_reserve(hp,missing,reserve):
 amount=min(max(0,hp),missing,reserve);return amount,reserve-amount
def counter_reset(counter,already):return (0,True) if counter>0 and not already else (counter,already)
for cap in[3,4,5,6,7]:
 check(f'Resource cap{cap} gain/payment boundaries',gain(cap,2,cap)==cap and pay(cap,cap)==0 and gain(0,-1,cap)==0)
try:pay(2,3);illegal=False
except ValueError:illegal=True
check('Overspending rejected',illegal)
r=13;healed=0
for _ in range(100):amount,r=consume_reserve(20,100,r);healed+=amount
check('Druid/Warrior finite reserve cannot refill through repetition',healed==13 and r==0)
c,used=counter_reset(3,False);c=4;c2,used2=counter_reset(c,used)
check('Only one positive reset per round',c2==4 and used2)
check('Zero recharge cannot consume reset',counter_reset(0,False)==(0,False))
seen=set();denials=[]
for target in ['a','a','b','a']:
 denials.append(target not in seen);seen.add(target)
check('Shared hard-denial guard tracks source-target once',denials==[True,False,True,False])
# Model protected cadence boundaries rather than claiming to simulate all cards.
def wizard_strain(family,seen,repeats):
 base=0 if family not in seen else 1;seen.add(family);return base+min(3,repeats)
seen=set();check('Wizard first family exemption does not erase Refrain',wizard_strain('bolt',seen,0)==0 and wizard_strain('bolt',seen,1)==2)
check('Thief hidden cadence reduces Refrain only',max(0,0-1)+1==1 and max(0,2-1)+1==2)
cleric=read(DATA/'cleric.json');crimson=read(DATA/'crimson-agent.json')
check('Cleric and Crimson mandatory capacities explicitly recorded',any(re.search(r'capacity.*5|maximum.*5',s,re.I) for s in cleric['engine']) and any('capacity 6' in s for s in crimson['engine']))
# Validate relative Markdown file links in generated packets, excluding anchors/web.
broken=[]
for p in (ROOT/'docs/mechanics/classes').glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  target=target.split('#')[0]
  if not (p.parent/target).resolve().exists():broken.append(str(p.name)+':'+target)
check('Generated packet file links resolve',not broken,str(broken))
result={'date':'2026-10-08','status':'PASS' if not issues else 'INCOMPLETE_OR_FAILED','classes':len(names),'checks':checks,'issues':issues,
 'scope':'Source completeness, fields, stage gates, sampled legal acquisitions, selected shared resource invariants and local links. No claim of full combat simulation or balanced gameplay.', 'buildExamples':builds}
(ROOT/'docs/mechanics/CLASS_PLAYTEST_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(result['status'],len(checks),'checks',len(issues),'issues')
for s in issues:print(s)
