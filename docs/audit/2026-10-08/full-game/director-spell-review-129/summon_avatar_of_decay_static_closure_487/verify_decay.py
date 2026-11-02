"""Separate read-only verifier: no builder import, no mutation of source/witness files."""
import copy, hashlib, json, math
from pathlib import Path
def locate_repository():
 for base in [Path.cwd(), *Path(__file__).resolve().parents]:
  for candidate in [base, base/'decay_repo']:
   if (candidate/'DescentReviewChanges').is_dir(): return candidate
 raise RuntimeError('Run within the repository or beside the decay_repo staging checkout')
ROOT=locate_repository()
AUDIT=Path('docs/audit/2026-10-08/full-game/director-spell-review-129')
OUT=AUDIT/'summon_avatar_of_decay_static_closure_487'
checks=[]
def check(name,condition):
 checks.append({'check':name,'pass':bool(condition)})
 if not condition:raise AssertionError(name)
def read(p):return json.loads((ROOT/p).read_bytes())
def h(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def apply(state,ops):
 s=copy.deepcopy(state)
 for op in ops:
  tokens=[x.replace('~1','/').replace('~0','~') for x in op['path'].split('/')[1:]]
  if not tokens:s=copy.deepcopy(op['value']);continue
  p=s
  for t in tokens[:-1]:p=p[int(t)] if isinstance(p,list) else p[t]
  k=int(tokens[-1]) if isinstance(p,list) else tokens[-1]
  if op['op']=='remove':del p[k]
  else:p[k]=copy.deepcopy(op['value'])
 return s
def verify_chain(w):
 s=copy.deepcopy(w['initialState']);states=[copy.deepcopy(s)];check(w['id']+' initial hash',h(s)==w['initialSHA256'])
 last=(-1,0)
 for i,e in enumerate(w['events']):
  check(e['id']+' ordered '+w['id'],(e['tick'],e['sequence'])>last);last=(e['tick'],e['sequence'])
  check(e['id']+' prehash '+w['id'],h(s)==e['beforeSHA256']);after=apply(s,e['forward'])
  check(e['id']+' posthash '+w['id'],h(after)==e['afterSHA256']);check(e['id']+' inverse '+w['id'],apply(after,e['inverse'])==s)
  states.append(after);s=after
 check(w['id']+' terminal exact',s==w['terminalState'] and h(s)==w['terminalSHA256'])
 for e in reversed(w['events']):s=apply(s,e['inverse'])
 check(w['id']+' full reverse exact',s==w['initialState'])
 check(w['id']+' operation counts',sum(len(e['forward']) for e in w['events'])==w['forwardOperationCount'] and sum(len(e['inverse']) for e in w['events'])==w['inverseOperationCount'])
 return states
def bind(b):
 p=b.get('path');digest=b.get('sha256');size=b.get('bytes')
 if not p or not digest:return
 raw=(ROOT/p).read_bytes();check('raw source '+p,hashlib.sha256(raw).hexdigest()==digest and (size is None or len(raw)==size))
def aabb(x):
 p=x['pos'];b=x['box'];return [(p[0]-b[0]/2,p[0]+b[0]/2),(p[1]-b[1]/2,p[1]+b[1]/2),(p[2],p[2]+b[2])]
def dist(a,b):return math.sqrt(sum(max(0,x[0]-y[1],y[0]-x[1])**2 for x,y in zip(aabb(a),aabb(b))))
def overlap(a,b):return all(min(x[1],y[1])>max(x[0],y[0])+1e-10 for x,y in zip(a,b))

r1=read(OUT/'SH333_R01_R1_WITNESS_487_TESTONLY.json');r2=read(OUT/'SH333_R02_R1_WITNESS_487_TESTONLY.json')
for w in [r1,r2]:
 for b in w['sourceBindings']:bind(b)
s1=verify_chain(r1);s2=verify_chain(r2)
parent=read(AUDIT/'rank9_summon_avatar_of_decay_return333_received/payload/components/SH333-RIDER-CANCEL.json')['initialState']['world']
check('R01 exact inherited parent',r1['initialState']==parent)
q=copy.deepcopy(s1[1]);q['actors']['C']['pos']=[40,-5,0];del q['branchContext'];q['phase']=parent['phase']
check('R01 projection only adopted C position and metadata',q==parent)
mb='wizard.hero.necromancer.mental-binding';mid='N1:mental-binding-1';av='A:cast1:body1'
bykind={e['kind']:(s1[i],s1[i+1]) for i,e in enumerate(r1['events'])}
at=lambda kind:bykind[kind][1]
commit=at('castCommit');resolve=at('castResolution');end=r1['terminalState']
check('R01 legal cost/strain/family commitment',commit['actors']['N1']['RP']==52 and commit['actors']['N1']['dissonance']==2 and commit['actors']['N1']['refrain']==0 and commit['actors']['N1']['lastCast']==mb and commit['actors']['N1']['preparedSeen']==parent['actors']['N1']['preparedSeen']+[mb] and commit['actors']['N1']['actions']['Action']==0)
check('R01 concentration before response; pending before resolution',commit['actors']['N1']['concentration']==mid and commit['sources'][mid]['expires']==2110 and commit['branchContext']['pendingCast'] is not None and resolve['branchContext']['pendingCast'] is None)
before,after=bykind['counterspellDeclines'];check('R01 response non-use leaves all actor state unchanged',before['actors']==after['actors'])
for r in after['branchContext']['responseWindows'][0]['responders']:
 check('R01 responder '+r['actor'],r['distanceFeet']<=60 and abs(r['distanceFeet']-math.dist(before['actors'][r['actor']]['pos'],before['actors']['N1']['pos']))<1e-9 and r['Reaction']==1 and r['RP']>=3 and r['recharge']==0 and r['choice']=='DECLINE')
check('R01 no self-counter assertion',after['branchContext']['responseWindows'][0]['selfResponder']['eligibility']=='UNADJUDICATED')
expected_starts={w:list(range(o if o>300 else o+600,2111,600)) for w,o in [('A',0),('B',100),('C',200),('N1',300),('N2',400),('F',500)]}
for actor,expected in expected_starts.items():
 actual=[e['tick'] for e in r1['events'] if e['kind']=='regularStart:'+actor];check('R01 all STARTs '+actor,actual==expected)
 ends=[t+80 for t in ([300] if actor=='N1' else [])+expected if t+80<=2110]
 check('R01 all ENDs '+actor,[e['tick'] for e in r1['events'] if e['kind']=='regularEnd:'+actor]==ends)
for i,e in enumerate(r1['events']):
 b,a=s1[i],s1[i+1]
 if e['kind'].startswith('regularStart:'):
  who=e['kind'].split(':')[1];check(e['id']+' regular budget refresh',a['actors'][who]['actions']=={'Action':1,'BA':1,'Reaction':1,'moveSpent':0,'objectInteraction':1} and not a['actors'][who]['magicThisTurn'])
 if e['kind'].startswith('regularEnd:'):
  who=e['kind'].split(':')[1];old=b['actors'][who];new=a['actors'][who]
  check(e['id']+' END flag preserved',old.get('magicThisTurn',False)==new.get('magicThisTurn',False))
  check(e['id']+' END Dissonance',new['dissonance']==(max(0,old['dissonance']-1) if old['class'] and not old.get('magicThisTurn',False) else old['dissonance']))
  check(e['id']+' idle Refrain unchanged',old['refrain']==new['refrain'])
 if e['kind'].startswith('attached') or e['kind'] in ['relay1Execution','relay2Execution']:
  for who in b['actors']:check(e['id']+' no attached refresh '+who,b['actors'][who]['actions']==a['actors'][who]['actions'])
 # Full positions are checked against one another and floor/ceiling at each transition.
 entities=list(a['actors'].values())+list(a['bodies'].values())
 check(e['id']+' body fit/support',all(o['pos'][2]==0 and o['physicalSupport']=='floor' and 0<=aabb(o)[2][0]<=aabb(o)[2][1]<=100 and all(-500<=v<=500 for interval in aabb(o)[:2] for v in interval) for o in entities))
 check(e['id']+' body nonintersection',all(not overlap(aabb(x),aabb(y)) for n,x in enumerate(entities) for y in entities[n+1:]))
 check(e['id']+' floor static load',all(o['massLb']/(o['box'][0]*o['box'][1])<=1000 for o in entities))
 check(e['id']+' inherited property exact',a['objects']==parent['objects'])
 check(e['id']+' Decay parent/deadline preserved',a['sources']['A:cast1']==parent['sources']['A:cast1'])
 check(e['id']+' Avatar HP unchanged',a['bodies'][av]['HP']==267)
 check(e['id']+' original root retained',a['rootLedger']['root:1']==parent['rootLedger']['root:1'])

for kind,who,route in [('relay2Execution','N2:cast1:minion',[[35,0,0],[35,-20,0]]),('BMovement','B',[[30,-20,0],[30,-10,0],[40,-10,0]])]:
 b,a=bykind[kind];moving=b['actors'].get(who) or b['bodies'][who];others=[v for k,v in {**b['actors'],**b['bodies']}.items() if k!=who]
 for start,finish in zip(route,route[1:]):
  o=copy.deepcopy(moving);o['pos']=start;l=aabb(o);o['pos']=finish;r=aabb(o);sweep=[(min(x[0],y[0]),max(x[1],y[1])) for x,y in zip(l,r)]
  check(kind+' continuous sweep '+str(start),all(not overlap(sweep,aabb(o)) for o in others))
 check(kind+' 20ft budget',sum(math.dist(x,y) for x,y in zip(route,route[1:]))==20 and moving['walk']>=20)
check('B final outside aura',abs(dist(end['actors']['B'],end['bodies'][av])-12.747548783981962)<1e-9)
check('Zombie distance 7.5',dist(end['bodies']['N2:cast1:minion'],end['bodies'][av])==7.5)
arb=at('competingControlArbitration');check('R01 same-slot earlier reservation wins',arb['branchContext']['arbitration']['winner']=='relay:3' and arb['relations']['relay:3']['executedTick']==510 and arb['orders']['N1:approach:1']['status']=='expired-unexecuted' and not arb['orders']['N1:approach:1']['executed'])
check('R01 shared guards precisely three',set(end['hardGuards'])=={'A:N1:cast1:minion:encounter','A:N2:cast1:minion:encounter','A:F:encounter'})
check('R01 Ferry native attack/force defense',arb['rootLedger']['R01:relay:3']['packets'][0]['stats']['attackModifier']==3 and arb['rootLedger']['R01:relay:3']['packets'][0]['resolved']==2 and arb['actors']['C']['HP']==102 and arb['objects']['F-contract-seal']==parent['objects']['F-contract-seal'])
check('R01 final HP',end['actors']['B']['HP']==83 and end['actors']['C']['HP']==102 and end['actors']['F']['HP']==9 and end['bodies']['N2:cast1:minion']['HP']==51)
check('R01 no healing on Flesh restoration',at('relay1Execution')['bodies']['N1:cast1:minion']['HP']==40 and at('relay1Execution')['bodies']['N1:cast1:minion']['maxHP']==74 and at('relay2Execution')['bodies']['N2:cast1:minion']['HP']==61 and at('relay2Execution')['bodies']['N2:cast1:minion']['maxHP']==95)
check('R01 pair bonuses',all(end['bodies'][id]['AC']==ac and set(end['bodies'][id]['saves'].values())=={7} for id,ac in [('N1:cast1:minion',15),('N1:cast2:minion',13),('N2:cast1:minion',13),('N2:cast2:minion',15)]))
check('R01 aura exactly three new pulses',end['bodies'][av]['auraConsumed']==['B:100','B:600','N2:cast1:minion:600','N2:cast1:minion:1200'])
check('R01 failed repeat saves retained',[(x['tick'],x['d20']) for x in end['sources'][mid]['history']]==[(580,4),(1180,10),(1780,19)])
check('R01 deadline/agency/Recharge',not end['sources'][mid]['active'] and end['sources'][mid]['endedTick']==2110 and end['actors']['N1']['concentration'] is None and end['actors']['N1']['recharge'][mb]==0 and end['actors']['F']['controller']=='F' and not end['actors']['F']['conditions'])
check('R01 final cost and idle ledgers',end['actors']['N1']['RP']==52 and end['actors']['N1']['dissonance']==0 and end['actors']['N1']['refrain']==0 and end['actors']['N2']['RP']==56 and end['actors']['N2']['dissonance']==0 and end['actors']['N2']['refrain']==1)
check('R01 all reservations retired no refund',all(not b['reservations'] for b in end['ownerRoundBudgets'].values()) and all(end['ownerRoundBudgets'][k]['offense'] for k in ['A:1','N1:1','N2:1']))
check('R01 no pending cast/order resurrection',end['branchContext']['pendingCast'] is None and all(r['status']=='executed-ended' for r in end['relations'].values()) and end['orders']['N1:approach:1']['status']=='expired-unexecuted')
for i,s in enumerate(s2[1:],1):
 check('R02 preserved parent/resources/property '+str(i),all(s[k]==r2['initialState'][k] for k in ['parentSource','resources','property','unrelatedRelation','budgets','guardHistory','providerQualification','schedules']))
 check('R02 no order/reservation/control revival '+str(i),s['order']['status']=='cancelled' and not s['order']['executed'] and not s['reservation']['active'] and s['recipient']['controller']=='R02-TEST-RECIPIENT' and s['recipient']['HP']==40 and s['recipient']['maxHP']==40)
check('R02 downward clamp not damage/heal',s2[1]['settlements'][0]['damage']==0 and s2[1]['settlements'][0]['healing']==0 and s2[1]['recipient']['HP']==40 and r2['initialState']['recipient']['HP']==60)
check('R02 source-bound pair recalculation',r2['initialState']['avatar']['AC']==16 and s2[1]['avatar']['AC']==15 and s2[1]['avatar']['HP']==284 and s2[1]['avatar']['saves']==6)
check('R02 type restored not powers',s2[-1]['recipient']['type']=='Undead' and s2[-1]['recipient']['dynamicFlesh']==0 and s2[-1]['recipient']['AC']==14 and s2[-1]['recipient']['saves']==6)
report={'id':'DECAY-487-INDEPENDENT-REPLAY-SEMANTIC-VALIDATION','status':'PASS','independence':'Separate read-only verifier; does not import builder or trust its assertions. Authored and run by the same assistant; not an independent human audit.','checksPassed':len(checks),'failures':0,'checks':checks,'witnesses':[{'id':w['id'],'rawSHA256':hashlib.sha256((ROOT/OUT/name).read_bytes()).hexdigest(),'events':len(w['events']),'forwardOperations':w['forwardOperationCount'],'inverseOperations':w['inverseOperationCount']} for w,name in [(r1,'SH333_R01_R1_WITNESS_487_TESTONLY.json'),(r2,'SH333_R02_R1_WITNESS_487_TESTONLY.json')]],'noHistoricalCaseReplay':True,'noCampaignOrRuntimeExecution':True}
(ROOT/OUT/'VALIDATION_487.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
