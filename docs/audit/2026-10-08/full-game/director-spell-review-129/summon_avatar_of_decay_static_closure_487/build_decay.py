"""Deterministic, branch-scoped authored-review witnesses. No runtime/campaign execution."""
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
BASE='c6d6a3a0e084008fc260dc6096c2b01fd77e67d6'
PROPDIR=AUDIT/'summon_avatar_of_decay_r01_control_integration_proposal_2026-11-02'
PROP=PROPDIR/'OWNER_SH333_R01_CONTROL_INTEGRATION_PROPOSAL_REPACK03_TESTONLY.json'
PAY=AUDIT/'rank9_summon_avatar_of_decay_return333_received/payload'
PARENT=PAY/'components/SH333-RIDER-CANCEL.json'
PROC=PAY/'input/05_RETURN285_AVATAR_PROCEDURE.json'
R2DIR=AUDIT/'summon_avatar_of_decay_r02_obligation_revision_request_2026-11-02'
REQ=R2DIR/'OWNER_SH333_R02_ELIGIBILITY_LOSS_REVISION_DECISION_REQUEST_TESTONLY.json'
RULING=R2DIR/'DIRECTOR_READBACK_SH333_R02_OBLIGATION_REVISION_01.json'

def read(p): return json.loads((ROOT/p).read_bytes())
def canon(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def h(v): return hashlib.sha256(canon(v)).hexdigest()
def binding(p):
 b=(ROOT/p).read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'hashDomain':'raw Git UTF-8 bytes','baseCommit':BASE}
def save(name,obj):
 p=ROOT/OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');return binding(OUT/name)
def esc(k):return str(k).replace('~','~0').replace('/','~1')
def diff(a,b,p=''):
 if type(a) is dict and type(b) is dict:
  ops=[]
  for k in sorted(a.keys()-b.keys()):ops.append({'op':'remove','path':p+'/'+esc(k)})
  for k in sorted(b.keys()-a.keys()):ops.append({'op':'add','path':p+'/'+esc(k),'value':copy.deepcopy(b[k])})
  for k in sorted(a.keys()&b.keys()):ops+=diff(a[k],b[k],p+'/'+esc(k))
  return ops
 return [] if a==b else [{'op':'replace','path':p,'value':copy.deepcopy(b)}]

class Trace:
 def __init__(self,initial):self.initial=copy.deepcopy(initial);self.s=copy.deepcopy(initial);self.events=[]
 def emit(self,tick,kind,mutate,evidence=None):
  before=copy.deepcopy(self.s);self.s['tick']=tick;self.s['phase']=kind;mutate(self.s)
  self.events.append({'id':f'E{len(self.events)+1:03d}','tick':tick,'kind':kind,'sequence':len(self.events)+1,'evidence':evidence or {},'beforeSHA256':h(before),'afterSHA256':h(self.s),'forward':diff(before,self.s),'inverse':diff(self.s,before)})
 def document(self,id,bindings,scope):return {'schemaVersion':1,'id':id,'classification':'HYPOTHETICAL_TEST_ONLY_UNSEALED','scope':scope,'campaignOccurrence':False,'runtimeExecuted':False,'hashDomain':'state SHA-256: UTF-8 JSON sorted keys, compact separators, ensure_ascii=false; file bindings: raw bytes','sourceBindings':bindings,'initialState':self.initial,'initialSHA256':h(self.initial),'events':self.events,'terminalState':self.s,'terminalSHA256':h(self.s),'eventCount':len(self.events),'forwardOperationCount':sum(len(e['forward']) for e in self.events),'inverseOperationCount':sum(len(e['inverse']) for e in self.events),'inversePurpose':'Audit restoration only; no in-game undo, resource refund, resurrection or history erasure.'}

proposal=read(PROP)
authorization=save('DELEGATED_TESTONLY_AUTHORIZATION_487.json',{
 'id':'DECAY-DELEGATED-TESTONLY-AUTHORIZATION-487','status':'AUTHORIZED_BY_CURRENT_OWNER_INSTRUCTION','instructionEvidence':[
 {'quote':'then work on them until all 15 are complete, what are we doing here?','role':'user'},
 {'quote':'No. work on 1 until its complete, then go to 2','role':'user','firstIdentity':'summon-avatar-of-decay'}],
 'interpretation':'Delegated execution of the already Director-reviewed R01 proposal and expressly authorized R02 static-test route, followed by evidence-based Director disposition and static application. No claim that the owner pasted prior proposed adoption wording verbatim.',
 'adoptedForConstruction':[binding(PROP),binding(REQ)],'R02Authority':binding(RULING),
 'scope':['SH333-R01-R1 only under exact Repack03 inputs','SH333-R02-R1 only: explicit synthetic baseline, abstract type eligibility loss and return, no type-changing provider asserted'],
 'nonEffects':['No campaign fact or actual-source qualification','No native/source rule or runtime promotion','R03/R04 seals preserved','No automatic identity acceptance: construction must pass independent replay and semantic checks'],
 'authorityBefore':{'applied':833,'pending':15,'acceptedUnapplied':0},'queue':binding(AUDIT/'CURRENT_SPELL_QUEUE_478.json')})

tr=Trace(read(PARENT)['initialState']['world']);MB='wizard.hero.necromancer.mental-binding';MID='N1:mental-binding-1';AV='A:cast1:body1'
def init(s):
 s['actors']['C']['pos']=[45,-5,0]
 s['branchContext']={'id':'SH333-R01-R1','geometryConvention':'center-XY / feet-Z; AABB z=[z,z+height]','campaignOccurrence':False,'parentHistoryReplayed':False,'regularEndReceipts':[],'auraEligibilityChecks':[],'responseWindows':[],'pendingCast':None,'dissonanceLimit':13}
tr.emit(300,'adoptedBranchProjection',init,{'proposalPointer':'/premises/parentProjection/branchOnlyOverride','onlyWorldOverride':'C position [40,-5,0] -> [45,-5,0]; hypothetical branch placement, not movement'})

def box(o):
 x,y,z=o['pos'];w,d,ht=o['box'];return [(x-w/2,x+w/2),(y-d/2,y+d/2),(z,z+ht)]
def gap(a,b):return math.sqrt(sum(max(0,x[0]-y[1],y[0]-x[1])**2 for x,y in zip(box(a),box(b))))
def roll(s,what,dice,modifier=0):s['RNG'].append({'tick':s['tick'],'operand':what,'dice':dice,'modifier':modifier,'provenance':'explicit adopted TEST_ONLY operand; no RNG sampling'})
def damage(s,id,dealer,target,raw,typ,save=None,stats=None):
 t=s['actors'].get(target) or s['bodies'][target];amount=raw
 if save and save['success']:amount//=2
 if typ in t.get('immunities',[]):amount=0
 elif typ in t.get('resistances',[]):amount//=2
 temp=min(t['tempHP'],amount);t['tempHP']-=temp;before=t['HP'];t['HP']=max(0,before-(amount-temp))
 s['rootLedger'][id]={'id':id,'dealer':dealer,'sourceOwner':'A' if dealer==AV else s['bodies'].get(dealer,s['actors'].get(dealer,{})).get('sourceOwner'),'controller':s['bodies'].get(dealer,s['actors'].get(dealer,{})).get('controller'),'creationTick':s['tick'],'nullNonlethal':False,'packets':[{'target':target,'raw':raw,'type':typ,'save':save,'resolved':amount,'tempAbsorbed':temp,'HPBefore':before,'HPAfter':t['HP'],'HPLoss':before-t['HP'],'stats':stats}],'noResourceRecursion':True}
def recompute(s,owner):
 group=[b for b in s['bodies'].values() if b['controller']==owner and b['type']=='Undead' and b['active']]
 for b in group:
  b['dynamicFlesh']=34;b['maxHP']=b['nativeHP']+b.get('creationModifiers',{}).get('conjuration',0)+34;b['HP']=min(b['HP'],b['maxHP']);b['AC']=b['baseAC']+(len(group)>=2);b['saves']={k:6+(len(group)>=2) for k in b['saves']}
def retire(s,rid):
 r=s['relations'][rid];target=r['target'];b=s['actors'].get(target) or s['bodies'][target]
 s['hardGuards'][r['hardGuardKey']]={'spent':True,'tick':s['tick'],'relationId':rid}
 r.update(status='executed-ended',executedTick=s['tick'],endedTick=s['tick'],endedReason='one designated execution completed')
 if r['budgetKey']:
  budget=s['ownerRoundBudgets'][r['budgetKey']];budget['reservations'].remove(rid);budget['offense']=True;budget.setdefault('executions',[]).append({'relationId':rid,'tick':s['tick']})
 b['controller']=r['originalController']
 if target in s['bodies']:b['pendingOrder']=None;recompute(s,r['originalController'])

def commit(s):
 a=s['actors']['N1'];a['RP']-=4;a['actions']['Action']=0;a['refrain']=0;a['lastCast']=MB;a['preparedSeen'].append(MB);a['magicThisTurn']=True;a['concentration']=MID
 a['resourceHistory'].append({'sourceId':MID,'spell':MB,'rank':7,'baseCost':4,'actualPaid':4,'preDissonance':2,'baseDissonance':0,'refrainAdded':0,'refrainBefore':1,'refrainAfter':0,'surcharge':0,'tick':310,'firstPreparedFamily':True})
 a['activeSourceIds'].append(MID)
 s['sources'][MID]={'id':MID,'spellId':MB,'owner':'N1','rank':7,'castTick':310,'formationTick':None,'expires':2110,'concentration':True,'active':False,'status':'committed-pending','target':'F','history':[]}
 s['branchContext']['pendingCast']={'sourceId':MID,'target':'F','committedTick':310,'window':'pending','costPaid':4}
def responses(s):
 rs=[]
 for who in ['A','B','C','N2']:
  a=s['actors'][who];dist=math.dist(a['pos'],s['actors']['N1']['pos']);rs.append({'actor':who,'source':'wizard.arch.counterspell','rangeFeet':60,'distanceFeet':dist,'samePlane':True,'perceived':True,'lineOfEffect':True,'RP':a['RP'],'minimumBaseCost':3,'Reaction':a['actions']['Reaction'],'recharge':a['recharge'].get('wizard.arch.counterspell',0),'eligible':True,'choice':'DECLINE','spentRP':0,'spentReaction':0})
 s['branchContext']['responseWindows'].append({'tick':310,'sourceId':MID,'responders':rs,'hypotheticalCheckDC':24,'selfResponder':{'actor':'N1','attempt':False,'eligibility':'UNADJUDICATED'}});s['branchContext']['pendingCast']['window']='closed-all-declined'
def resolve(s):
 roll(s,'F initial Mental Binding WIS save',[3],0);s['actors']['F']['conditions'].append({'id':'Charmed','sourceId':MID,'caster':'N1','expires':2110,'repeatSave':'own regular END and on damage','DC':21});s['sources'][MID].update(active=True,status='established',formationTick=310);s['actors']['N1']['recharge'][MB]=3;s['branchContext']['pendingCast']=None
def approach(s):
 s['orders']['N1:approach:1']={'id':'N1:approach:1','controller':'N1','sourceId':MID,'target':'F','issued':310,'expires':510,'designatedOpportunity':510,'status':'pending','mode':'Approach','route':[[45,0,0],[45,10,0]],'distanceFeet':10,'maximumFeet':20,'hardGuardKey':'N1:F:encounter','executed':False}

def aura(s,who):
 body=s['bodies'][AV];targets=[s['actors'][who]]+[b for b in s['bodies'].values() if b['sourceOwner']==who and b['id']!=AV]
 for target in targets:
  d=gap(body,target);key=f"{target['id']}:{body['lastSourceMarker']}";due=d<=10 and s['tick']>body['lastSourceMarker'] and key not in body['auraConsumed']
  s['branchContext']['auraEligibilityChecks'].append({'tick':s['tick'],'recipient':target['id'],'sourceMarker':body['lastSourceMarker'],'nearestBoundsFeet':d,'lineOfEffect':True,'inside':d<=10,'due':due,'key':key})
  if not due:continue
  inputs={(700,'B'):([3,3],17,2),(1000,'N2:cast1:minion'):([2,4],11,7),(1600,'N2:cast1:minion'):([3,5],12,7)}
  dice,d20,mod=inputs[(s['tick'],target['id'])];roll(s,key+' pool',dice);roll(s,key+' CON',[d20],mod)
  damage(s,'R01:aura:'+key,AV,target['id'],sum(dice),'necrotic',{'d20':d20,'modifier':mod,'DC':19,'success':d20+mod>=19}, {'dice':dice,'sourceMarker':body['lastSourceMarker']});body['auraConsumed'].append(key)
def start(s,who):
 a=s['actors'][who];a['actions']={'Action':1,'BA':1,'Reaction':1,'moveSpent':0,'objectInteraction':1};a['turnActive']=True;a['lastRegularStart']=s['tick'];a['nextRegularStart']=s['tick']+600;a['magicThisTurn']=False
 if a['stance']=='Dodge':a['stance']='Neutral'
 for k in a['recharge']:a['recharge'][k]=max(0,a['recharge'][k]-1)
 s['round']=s['tick']//600+1;s['ownerRoundBudgets'].setdefault(f"{who}:{s['round']}",{'command':False,'offense':False,'reservations':[]})
 for b in s['bodies'].values():
  if b['sourceOwner']==who:
   b['lastSourceMarker']=s['tick'];b['nextSourceMarker']=s['tick']+600;b['Dodge']=False;b['DodgeUntil']=None;b['breathRecharge']=max(0,b['breathRecharge']-1)
 aura(s,who)
def end(s,who):
 a=s['actors'][who];before=a['dissonance'];a['turnActive']=False;a['lastRegularEnd']=s['tick']
 if a['class'] and not a.get('magicThisTurn',False):a['dissonance']=max(0,a['dissonance']-1)
 s['branchContext']['regularEndReceipts'].append({'actor':who,'tick':s['tick'],'magicThisTurn':a.get('magicThisTurn',False),'DissonanceBefore':before,'DissonanceAfter':a['dissonance'],'Refrain':a['refrain'],'unusedActions':copy.deepcopy(a['actions']),'opportunityClosed':True})
def attached(s,owner,except_id=None):
 for b in s['bodies'].values():
  if b['sourceOwner']!=owner or b['id']==except_id:continue
  b['Dodge']=True;b['DodgeUntil']=b['nextSourceMarker'];b['pendingOrder']=None;b['phaseHistory'].append({'phase':s['tick'],'order':None,'valid':True,'default':'Dodge','movementSpent':0})
def attack(s,rid,die,damage_die,flat,target,typ):
 r=s['relations'][rid];dealer=r['target'];b=s['actors'].get(dealer) or s['bodies'][dealer]
 if rid=='relay:2':b['pos']=[35,-20,0]
 roll(s,rid+' attack',[die],3 if dealer=='F' else 11);roll(s,rid+' damage',[damage_die],flat)
 damage(s,'R01:'+rid,dealer,target,damage_die+flat,typ,stats={'d20':die,'attackModifier':3 if dealer=='F' else 11,'targetAC':s['actors'][target]['AC'],'damageDie':damage_die,'damageFlat':flat,'critical':False})
 b['offenseHistory'].append({'tick':s['tick'],'relationId':rid,'root':'R01:'+rid,'target':target})
 if dealer=='F':b['actions']['Action']=0
 else:
  b['strikeSlotsByRound'][str(s['tick']//600+1)]=1;b['phaseHistory'].append({'phase':s['tick'],'order':rid,'valid':True,'movementSpent':20 if rid=='relay:2' else 0,'Action':'ordinary attack'});b['Dodge']=False;b['DodgeUntil']=None
 retire(s,rid)
 if rid in ('relay:1','relay:2'):attached(s,r['originalOwner'],dealer)
def arbitration(s):
 s['branchContext']['arbitration']={'tick':510,'validReservations':['relay:3','N1:approach:1'],'issuedTicks':[90,310],'winner':'relay:3','precedence':'earlier valid reservation; execute before unexecuted expiry','sameOpportunity':True}
 attack(s,'relay:3',12,2,0,'C','fire');s['orders']['N1:approach:1'].update(status='expired-unexecuted',endedTick=510,reason='earlier valid reservation consumed the designated opportunity',executed=False)
def repeat(s,d20):
 roll(s,'Mental Binding repeat WIS',[d20],0);s['sources'][MID]['history'].append({'tick':s['tick'],'event':'repeat-save','d20':d20,'modifier':0,'DC':21,'success':False})
def move_b(s):s['actors']['B']['pos']=[40,-10,0];s['actors']['B']['actions']['moveSpent']=20
def dodge_f(s):s['actors']['F']['actions']['Action']=0;s['actors']['F']['stance']='Dodge'
def finish(s):
 s['sources'][MID].update(active=False,status='ended',endedTick=2110,endedReason='original concentration deadline');s['actors']['N1']['concentration']=None;s['actors']['N1']['activeSourceIds'].remove(MID);s['actors']['F']['conditions']=[c for c in s['actors']['F']['conditions'] if c.get('sourceId')!=MID]

tasks=[]
def add(t,n,k,f,e=None):tasks.append((t,n,k,f,e))
add(310,1,'castCommit',commit);add(310,2,'counterspellDeclines',responses);add(310,3,'castResolution',resolve);add(310,4,'queueApproach',approach)
for who,offset in [('A',0),('B',100),('C',200),('N1',300),('N2',400),('F',500)]:
 for t in range(offset,2111,600):
  if t>300:add(t,0,'regularStart:'+who,lambda s,w=who:start(s,w))
  if 300<t+80<=2110:add(t+80,0,'regularEnd:'+who,lambda s,w=who:end(s,w))
for t,owner in [(390,'N1'),(490,'N2'),(690,'A'),(990,'N1'),(1090,'N2'),(1290,'A'),(1590,'N1'),(1690,'N2'),(1890,'A')]:
 if t==390:add(t,1,'relay1Execution',lambda s:attack(s,'relay:1',12,2,4,'B','necrotic'))
 elif t==490:add(t,1,'relay2Execution',lambda s:attack(s,'relay:2',8,3,4,'B','necrotic'))
 else:add(t,1,'attachedDodge:'+owner,lambda s,w=owner:attached(s,w))
add(510,0,'competingControlArbitration',arbitration)
for t,d20 in [(580,4),(1180,10),(1780,19)]:add(t,1,'repeatSave',lambda s,d=d20:repeat(s,d))
add(700,1,'BMovement',move_b,{'route':[[30,-20,0],[30,-10,0],[40,-10,0]],'distanceFeet':20,'noAdditionalAction':True})
for t in [1100,1700]:add(t,1,'FDodge',dodge_f)
add(2110,0,'MentalBindingDeadline',finish)
for t,n,k,f,e in sorted(tasks,key=lambda x:(x[0],x[1])):tr.emit(t,k,f,e)
r1bindings=[binding(PROP),authorization,binding(PARENT),binding(PROC)]+proposal['bindings']
r1=tr.document('SH333-R01-R1-487',r1bindings,'Adopted Repack03 competing-control integration only; R02 and existing R03/R04 not executed.')
r1['proposalSequence']=proposal['sequence'];r1['noSpellEfficiency']='W17N has no acquired Spell Efficiency; no discount/benefit is created.'
save('SH333_R01_R1_WITNESS_487_TESTONLY.json',r1)

# Independent R02 abstract contract. No acquired type-changing source is asserted.
r2start={'tick':300,'phase':'syntheticBaseline','classification':'TEST_ONLY_ABSTRACT_ELIGIBILITY_INPUT','parentSource':{'id':'R02:decay','active':True,'expires':6020,'owner':'R02:W17N','concentration':True},'avatar':{'id':'R02:avatar','sourceId':'R02:decay','active':True,'HP':284,'maxHP':284,'nativeHP':250,'dynamicFlesh':34,'type':'Undead','controller':'R02:W17N','AC':16,'baseAC':15,'saves':7,'baseSaves':6,'pos':[0,0,0],'auraActive':True},'recipient':{'id':'R02-TEST-RECIPIENT','type':'Undead','kind':'conditional independent recipient','originalController':'R02-TEST-RECIPIENT','controller':'R02:W17N','nativeHP':40,'HP':60,'maxHP':74,'dynamicFlesh':34,'baseAC':14,'AC':15,'baseSaves':6,'saves':7,'pos':[20,0,0],'box':[5,5,5],'physicalSupport':'R02:test-floor','equipment':['R02:item:1'],'pendingOrder':'R02:order','nextRegularStart':500,'Action':1,'agency':'one designated action reserved'},'relay':{'id':'R02:relay','sourceId':'R02:decay','target':'R02-TEST-RECIPIENT','issued':90,'expires':510,'status':'pending','guardKey':'R02:W17N:R02-TEST-RECIPIENT:encounter','reservation':'R02:reservation'},'order':{'id':'R02:order','status':'pending','designatedOpportunity':510,'executed':False},'reservation':{'id':'R02:reservation','active':True,'relationId':'R02:relay'},'budgets':{'casterCommandSpent':True,'casterOffenseSpent':True,'recipientActionSpent':False},'guardHistory':{'R02:W17N:other:encounter':{'spent':True,'tick':80}},'resources':{'casterRP':38,'casterDissonance':0,'casterRefrain':0,'paidHistory':[{'sourceId':'R02:decay','amount':26,'tick':10,'provenance':'synthetic baseline only; not a newly executed cast'}]},'property':{'R02:item:1':{'owner':'R02-TEST-RECIPIENT','custodian':'R02-TEST-RECIPIENT','placement':'carried','massLb':1}},'unrelatedRelation':{'id':'R02:other-relay','target':'R02:other','status':'pending','expires':900},'settlements':[],'providerQualification':{'typeChangingProvider':None,'acquisition':None,'activation':None,'actualSourceQualified':False},'schedules':{'sourceDeadline':6020,'relayOpportunity':510,'providerClock':None}}
r2=Trace(r2start)
def loss(s):
 q=s['recipient'];q.update(type='NonUndead_TEST_ONLY',controller=q['originalController'],pendingOrder=None,agency='prospective original agency',dynamicFlesh=0,maxHP=40,HP=40,AC=14,saves=6)
 s['avatar'].update(AC=15,saves=6)
 s['relay'].update(status='cancelled',endedTick=310,endedReason='loss of Undead eligibility');s['order'].update(status='cancelled',endedTick=310,executed=False);s['reservation']['active']=False
 s['settlements'].append({'tick':310,'cause':'TEST_ONLY abstract eligibility input','HPBefore':60,'HPAfter':40,'maximumBefore':74,'maximumAfter':40,'damage':0,'healing':0,'newGuardSpend':False,'refund':0,'relatedAvatarPairBonusRemoved':True})
def back(s):
 s['recipient']['type']='Undead';s['settlements'].append({'tick':320,'cause':'TEST_ONLY return to Undead','controllerRemains':'R02-TEST-RECIPIENT','noNewControl':True,'noReinstatement':True,'HPRemains':40,'maximumRemains':40,'parentAvatarPairBonusRemainsAbsent':True})
r2.emit(310,'abstractEligibilityLoss',loss)
r2.emit(320,'abstractReturnToUndead',back)
r2.emit(510,'cancelledOpportunityObservation',lambda s:s['settlements'].append({'tick':510,'cause':'original deadline reached; order already cancelled','execution':False,'newGuardSpend':False,'noSecondTermination':True,'noBudgetRefresh':True}))
r2doc=r2.document('SH333-R02-R1-487',[binding(REQ),binding(RULING),authorization,binding(PROC),binding(PAY/'evidence/EXISTING_W17N_PROFILE.json'),binding(Path('DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json'))],'SH333-R02-OBLIGATION-REVISION-01 abstract static test only. Numeric baseline explicitly synthetic; no operational type-changing provider, paid activation, acquisition or campaign history.')
r2doc['baselineDerivation']={'FleshAscendant':'Wizard17 acquired passive: +34 maximumHP; two initially controlled Undead (Avatar and recipient) +1 AC/save. Eligibility loss restores independent recipient agency and leaves one controlled Undead, removing only related pair bonuses. Return of Undead type alone restores neither control nor bonuses.','unrelatedRelations':'Other relation is metadata for an unrelated source; it does not add another Undead controlled by this caster.','noExternalProvider':'The change is a test operand under the explicit review-obligation revision, not a spell or in-game ability.','time':'Subturn observations only. Recipient START500 is intentionally out of the abstract operator harness, not a claimed complete encounter; no regular turn or actor action is executed.'}
save('SH333_R02_R1_WITNESS_487_TESTONLY.json',r2doc)
print(json.dumps({'R01_events':len(tr.events),'R01_operations':r1['forwardOperationCount'],'R02_events':len(r2.events),'output':str(ROOT/OUT)},indent=2))
