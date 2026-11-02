import copy,hashlib,json,math,subprocess,zipfile,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REVIEW=ROOT.parent; REPO=REVIEW.parents[4]
P=ROOT/'PG328_W12_REVERSION_OWNER_PROPOSAL_445_TESTONLY.json'; O=ROOT/'OWNER_PG328_W12_ADOPTION_445_TESTONLY.json'
S=REVIEW/'fortress_w01_structural_damage_witness_403_repack02'/'W01_REPLAY_403.json'; OLD=ROOT/'W12_WITNESS_450_TESTONLY.json'; RB=REVIEW/'DIRECTOR_READBACK_455.json'
FORM=REPO/'DescentReviewChanges/ReviewBible/data/playtest/spell_form_profiles.json'
W=ROOT/'W12_WITNESS_451_TESTONLY.json'; T=ROOT/'W12_LIFECYCLE_TRACE_451.json'; V=ROOT/'BUILD_VALIDATION_451.json'; R=ROOT/'README_WITNESS_451.md'; M=ROOT/'MANIFEST_451.json'; Z=ROOT/'DD_Fortress_W12_Reversible_Witness_451_TESTONLY.zip'; D=ROOT/'DELIVERY_451.json'; BUILD=ROOT/'BUILD_W12_WITNESS_451.py'; Q=ROOT/'VERIFY_W12_WITNESS_451.py'
PH='93d31941e6a6d4d059cb3a108d0e247d07cc8e6cce395712f1c0ad45523df14c'; OH='83d25ca677ea8d910575a3bcc87be6a29837553112d3445e1c50cc954a8f4c60'; SH='6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c'; RH='2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb'; ROOTID='RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1'; SPACE=ROOTID+'/space'; TILE='PG328-W01-403:CLAY-TILE-1'
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def hf(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ho(x): return hashlib.sha256(canon(x)).hexdigest()
def rel(p): return Path(p).resolve().relative_to(REVIEW.resolve()).as_posix()
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def bind(p):
 b=Path(p).read_bytes(); return {'path':Path(p).resolve().relative_to(REPO.resolve()).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def ptr(a): return '/'+ '/'.join(str(x).replace('~','~0').replace('/','~1') for x in a)
def diff(a,b,p=None):
 p=[] if p is None else p
 if isinstance(a,dict) and isinstance(b,dict):
  r=[]
  for k in sorted(a.keys()-b.keys()): r.append({'op':'remove','path':ptr(p+[k]),'oldValue':copy.deepcopy(a[k])})
  for k in sorted(b.keys()-a.keys()): r.append({'op':'add','path':ptr(p+[k]),'value':copy.deepcopy(b[k])})
  for k in sorted(a.keys()&b.keys()): r.extend(diff(a[k],b[k],p+[k]))
  return r
 if isinstance(a,list) and isinstance(b,list):
  if len(a)<=len(b) and a==b[:len(a)]: return [{'op':'add','path':ptr(p+[i]),'value':copy.deepcopy(b[i])} for i in range(len(a),len(b))]
  if len(b)<=len(a) and b==a[:len(b)]: return [{'op':'remove','path':ptr(p+[i]),'oldValue':copy.deepcopy(a[i])} for i in range(len(a)-1,len(b)-1,-1)]
  return [] if a==b else [{'op':'replace','path':ptr(p),'oldValue':copy.deepcopy(a),'value':copy.deepcopy(b)}]
 return [] if a==b else [{'op':'replace','path':ptr(p),'oldValue':copy.deepcopy(a),'value':copy.deepcopy(b)}]
def inverse(ops):
 r=[]
 for x in reversed(ops):
  if x['op']=='add': r.append({'op':'remove','path':x['path'],'oldValue':copy.deepcopy(x['value'])})
  elif x['op']=='remove': r.append({'op':'add','path':x['path'],'value':copy.deepcopy(x['oldValue'])})
  else: r.append({'op':'replace','path':x['path'],'oldValue':copy.deepcopy(x['value']),'value':copy.deepcopy(x['oldValue'])})
 return r
def apply(s,ops):
 s=copy.deepcopy(s)
 for x in ops:
  q=[z.replace('~1','/').replace('~0','~') for z in x['path'].lstrip('/').split('/')]; p=s
  for z in q[:-1]: p=p[int(z)] if isinstance(p,list) else p[z]
  k=q[-1]
  if isinstance(p,list):
   i=int(k)
   if x['op']=='add': p.insert(i,copy.deepcopy(x['value']))
   elif x['op']=='remove': p.pop(i)
   else: p[i]=copy.deepcopy(x['value'])
  elif x['op']=='add': p[k]=copy.deepcopy(x['value'])
  elif x['op']=='remove': del p[k]
  else: p[k]=copy.deepcopy(x['value'])
 return s
def add(out,t,o,k,d): out.append({'timeSeconds':float(t),'orderAtTime':o,'kind':k,'details':copy.deepcopy(d)})
def overlap(a,b): return all(min(a[k][1],b[k][1])-max(a[k][0],b[k][0])>1e-9 for k in ('x','y','z'))
def main():
 p=json.loads(P.read_text(encoding='utf-8')); adoption=json.loads(O.read_text(encoding='utf-8')); parent=json.loads(S.read_text(encoding='utf-8')); inputs=p['ownerProposedInputs']
 if hf(P)!=PH or hf(O)!=OH or hf(S)!=RH or ho(parent['stateSnapshots']['S030'])!=SH: raise ValueError('Exact source hash mismatch')
 if json.loads(RB.read_text(encoding='utf-8')).get('W12')!='HOLD_FOR_COMPONENT_SUFFICIENCY': raise ValueError('Missing W450-C01 readback')
 bindings=[]
 for x in p['sourceBindings']:
  raw=subprocess.check_output(['git','show',p['readAtCommit']+':'+x['path']],cwd=REPO); actual=hashlib.sha256(raw).hexdigest()
  bindings.append({**x,'actualSha256':actual,'matches':actual==x['sha256'],'resolvedAtCommit':p['readAtCommit']})
 if len(bindings)!=18 or not all(x['matches'] for x in bindings): raise ValueError('Source binding failed')
 initial=copy.deepcopy(parent['stateSnapshots']['S030']); state=copy.deepcopy(initial); baseclock=copy.deepcopy(state['clock']); baseT=state['time']
 predator=next(x for x in json.loads(FORM.read_text(encoding='utf-8'))['profiles'] if x['id']=='spellform.predator')
 sc=inputs['scheduledTimeAdvance']; c=inputs['terminalClosure']; specs=[]
 for aid,m in sc['markersByActor'].items():
  for t in m['starts']: add(specs,t,10,'START',{'actorId':aid})
  for t in m['ends']: add(specs,t,90,'END',{'actorId':aid})
 for t,o,k,key in [(13.1,20,'SIGHT_COMMIT',None),(13.2,30,'COUNTER_SIGHT',0),(13.3,40,'SIGHT_RESOLVE',None),(18.05,20,'TILE_DROP',None),(18.1,20,'POLY_COMMIT',None),(18.2,30,'COUNTER_POLY',1),(18.3,40,'POLY_RESOLVE',None),(78.1,20,'POLY_REVERT',None),(79.1,20,'DISPEL_COMMIT',None),(79.2,30,'COUNTER_DISPEL',2),(79.3,40,'DISPEL_RESOLVE',None)]:
  source=inputs['counterspellDecisions'][key] if key is not None else (inputs['perceptionAndDispel']['sight'] if 'SIGHT' in k else inputs['perceptionAndDispel']['dispel'] if 'DISPEL' in k else inputs['spellAndTransformation'] if 'POLY' in k else inputs['preCastInteractions'][0])
  add(specs,t,o,k,source)
 for sid,cast,expiry in [('wizard.arch.arcane-sight',13.1,19.9),('polymorph',18.1,24.9),('wizard.arch.dispel-magic',79.1,85.9)]:
  if expiry<=79.31: add(specs,expiry,70,'EFF_EXPIRY',{'spell':sid,'cast':cast,'expiry':expiry})
 add(specs,79.31,10,'ROOT_END',{'root':ROOTID})
 add(specs,79.31,20,'BODY',{'actor':'A','placement':c['A']}); add(specs,79.31,30,'BODY',{'actor':'B','placement':c['B']})
 for n,iid in enumerate(c['looseItemOrderByStableId'],40): add(specs,79.31,n,'LOOSE',next(x for x in c['looseItems'] if x['id']==iid))
 specs.sort(key=lambda x:(x['timeSeconds'],x['orderAtTime'],x['kind']))
 turns={}; events=[]; casts={}
 sinfo={'SIGHT_COMMIT':('B','wizard.arch.arcane-sight','Divination',2,2,2,'self',600),'POLY_COMMIT':('A','polymorph','Transmutation',4,7,None,'A',60),'DISPEL_COMMIT':('B','wizard.arch.dispel-magic','Abjuration',3,3,2,ROOTID,None)}
 def advance(t):
  d=t-baseT; state['time']=t; state['clock']['elapsedSeconds']=baseclock['elapsedSeconds']+d
  for k in ('OpeningRemaining','HornRemaining'):
   if k in baseclock and baseclock[k] is not None: state['clock'][k]=baseclock[k]-d
 def cast(k,e):
  aid,sid,school,rank,cost,recharge,target,dur=sinfo[k]; a=state['actors'][aid]; d=e['details']; t=e['timeSeconds']
  if aid not in turns or a['action']!=1: raise ValueError('No action for '+sid)
  ctx=turns[aid]; a['action']=0; ctx['spent']=1; ctx['kind']='CAST'; a['magicThisTurn']=True
  first=sid not in a['preparedFamiliesUsed']; strain=0 if first else (1 if rank<=5 else 2 if rank<=9 else 0); ref=min(3,a['Refrain']+1) if a['lastSpell']==sid else 0
  lim=max(4,2+a['PB']+max(0,a['M'])); ds=a['Dissonance']; surcharge=1 if ds>=lim else 2 if ds>=lim+3 else 3 if ds>=lim+6 else 0
  deadline=ctx['turnStart']+a['regularSchedule']['period']+a['regularSchedule']['endOffset']
  discount=any(x['family']==sid and x['status']=='PENDING' and t<=x['expiresAt'] for x in a.get('testOnlySpellEfficiencyHistory',[])); paid=max(1,cost-(1 if discount else 0))+surcharge
  rp=a['RP']; a['RP']-=paid; a['Dissonance']+=strain+ref; a['Refrain']=ref; a['lastSpell']=sid
  if first: a['preparedFamiliesUsed'].append(sid)
  cid=f'PG328-W12-R1:{sid}:{t:.2f}'; casts[sid]=cid
  h={'castId':cid,'spellId':sid,'class':'Wizard','school':school,'rank':rank,'time':t,'cost':paid,'firstPreparedFamily':first,'baseDissonance':strain,'Refrain':ref,'originPlane':a['plane'],'target':target,'spellEfficiencyDiscountApplied':discount,'spellEfficiencyWindowExpiresAt':deadline,'resolutionStatus':'PENDING'}
  if dur:
   h['concentration']={'activeFromCommit':True,'startedAt':t,'maximumDurationSeconds':dur,'deadline':t+dur}
   a['concentration']={'spellId':sid,'active':True,'startedAt':t,'maximumDurationSeconds':dur,'deadline':t+dur,'classification':'TEST_ONLY_HYPOTHETICAL_BRANCH'}
  a['spellHistory'].append(h); a['resourceHistory'].append({'event':cid,'RP':-paid,'poolAfter':a['RP'],'discount':discount,'spellId':sid,'DissonanceBefore':ds,'DissonanceAfter':a['Dissonance'],'Refrain':ref,'surchargeRP':surcharge})
  a.setdefault('testOnlySpellEfficiencyHistory',[]).append({'family':sid,'castId':cid,'createdAt':t,'expiresAt':float(deadline),'discountRP':1,'minimumCostRP':1,'status':'PENDING','consumedAt':None})
  if recharge is not None: a['recharge'][sid]=recharge
  state['pendingCast']={'castId':cid,'spellId':sid,'caster':aid,'target':target,'commitTime':t,'costCommitted':paid,'status':'PENDING_RESOLUTION','classification':'TEST_ONLY_HYPOTHETICAL_BRANCH'}
  if sid=='polymorph': a.setdefault('testOnlyTransformationRecords',[]).append({'spellId':sid,'castId':cid,'status':'PAID_PENDING_RESOLUTION','committedAt':t,'deadline':t+60,'profileId':predator['id'],'meldedItemIds':['focus-A','pack-A','cargo-A']})
  d.update({'actorId':aid,'castId':cid,'spellId':sid,'school':school,'rank':rank,'baseCostRP':cost,'costRP':paid,'RPBefore':rp,'RPAfter':a['RP'],'firstPreparedFamily':first,'DissonanceAfter':a['Dissonance'],'RefrainAfter':ref,'spellEfficiencyDiscountApplied':discount,'spellEfficiencyWindowExpiresAt':deadline,'ActionSpent':1,'rechargeAfterCommit':a['recharge'].get(sid),'concentrationAfterCommit':copy.deepcopy(a['concentration'])})
 for n,spec in enumerate(specs,1):
  e=copy.deepcopy(spec); t=e['timeSeconds']; k=e['kind']; d=e['details']; before=copy.deepcopy(state); advance(t)
  if k=='START':
   aid=d['actorId']; a=state['actors'][aid]; sched=a['regularSchedule']; r0=copy.deepcopy(a['recharge'])
   for key,v in list(a['recharge'].items()): a['recharge'][key]=max(0,int(v)-1)
   sched['starts'].append(t); sched['nextStart']=t+sched['period']; sched['nextEnd']=t+sched['endOffset']; a.update({'action':1,'bonusAction':1,'reaction':1,'movement':30,'magicThisTurn':False})
   turns[aid]={'turnStart':t,'spent':0,'kind':None,'BA':0,'reaction':0,'move':0}
   d.update({'budgetsAfterStart':{'Action':1,'BonusAction':1,'Reaction':1,'MovementFeet':30},'rechargeBefore':r0,'rechargeAfter':copy.deepcopy(a['recharge']),'nextStart':sched['nextStart'],'nextEnd':sched['nextEnd'],'magicThisTurn':False,'HP':a['HP'],'RP':a['RP'],'Dissonance':a['Dissonance'],'Refrain':a['Refrain']})
  elif k=='END':
   aid=d['actorId']; a=state['actors'][aid]; ctx=turns.pop(aid); ds=a['Dissonance']; decay=ctx['kind'] not in ('CAST','GROUNDING')
   if decay: a['Dissonance']=max(0,ds-1)
   sched=a['regularSchedule']; sched['ends'].append(t)
   disp={'regularTurnEndedAt':t,'recordedAt':t,'Action':{'spent':ctx['spent'],'unusedExpired':1-ctx['spent']},'BonusAction':{'spent':ctx['BA'],'unusedExpired':1-ctx['BA']},'Reaction':{'spent':ctx['reaction'],'availableOffTurnUntilSpentOrNextOwnStart':a['reaction']==1},'MovementFeet':{'granted':30,'spent':ctx['move'],'unusedExpired':30-ctx['move']}}
   sched['budgetHistory'].append({'time':ctx['turnStart'],'action':1,'BA':1,'Reaction':1,'Move':30,'recharge':copy.deepcopy(a['recharge']),'endDisposition':disp})
   a.update({'action':0,'bonusAction':0,'movement':0,'magicThisTurn':False}); sched['nextEnd']=None
   d.update({'turnStart':ctx['turnStart'],'actionSpent':ctx['spent'],'actionKind':ctx['kind'],'DissonanceBeforeEnd':ds,'DissonanceAfterEnd':a['Dissonance'],'idleDissonanceDecayApplied':decay,'unusedBudgetDisposition':disp,'nextStartPreserved':sched['nextStart'],'nextEndAfter':None})
  elif k in sinfo: cast(k,e)
  elif k=='COUNTER_SIGHT':
   a=state['actors']['A']; d.update({'attempted':False,'disposition':'NO_ATTEMPT_INELIGIBLE','hands':copy.deepcopy(a['w01HandState']),'reason':'Both hands hold focus-A and the original clay tile.','pendingCast':copy.deepcopy(state['pendingCast']),'resourcesSpent':False})
  elif k=='SIGHT_RESOLVE':
   a=state['actors']['B']; p=state['pendingCast']; sight=inputs['perceptionAndDispel']['sight']
   if not p or p['spellId']!=sight['spellId']: raise ValueError('Sight pending mismatch')
   state['pendingCast']=None; next(x for x in reversed(a['spellHistory']) if x['castId']==p['castId']).update({'resolutionStatus':'SUCCESSFUL','resolvedAt':t})
   effect={'id':'TEST_ONLY:PG328-W12-R1:ARCANE-SIGHT:B','spellId':sight['spellId'],'owner':'B','active':True,'concentration':True,'createdAt':t,'deadline':613.1,'classification':'TEST_ONLY_HYPOTHETICAL_BRANCH'}
   state['effects'][effect['id']]=effect
   obs={'time':t,'observer':'B','spellId':sight['spellId'],'subject':ROOTID,'auraPoint':sight['toAuraPoint'],'distanceFeet':sight['distanceFeet'],'samePlane':True,'totalCover':False,'lineClear':True,'knownCategory':'Conjuration','laterTurnAuraExaminationClaimed':False}
   state['observations'].append(obs); d.update({'resolutionStatus':'SUCCESSFUL','pendingCastAfter':None,'concentrationAfter':copy.deepcopy(a['concentration']),'auraPerceptionBeginsAt':t,'observation':obs,'RPAfter':a['RP']})
  elif k=='TILE_DROP':
   a=state['actors']['A']; item=state['items'][TILE]; x=inputs['preCastInteractions'][0]
   if a['w01HandState']!={'left':'focus-A','right':TILE}: raise ValueError('Initial hands mismatch')
   a['equipment'].remove(TILE); a['carriedWeightLb']=12; a['carriedLoad']=1.2; a['w01HandState']['right']='free'; item.update({'custodian':None,'plane':x['plane'],'position':x['toPosition'],'heldBy':None,'heldBoundsFeet':None}); item.setdefault('testOnlyGeometry',{})['currentBoundsFeet']=x['boundsFeet']; turns['A']['kind']='FREE_INTERACTION'
   d.update({'handsAfter':a['w01HandState'],'ownerAfter':item['owner'],'custodianAfter':None,'positionAfter':item['position'],'boundsFeet':x['boundsFeet'],'expiryPreserved':item['expiresAtEventTime'],'weightAfterLb':12,'loadAfter':1.2,'ActionSpent':0,'supportPatchId':x['supportPatchId']})
  elif k=='COUNTER_POLY':
   b=state['actors']['B']; d.update({'actorId':'B','eligible':True,'attempted':False,'disposition':'DECLINES','reactionAvailable':b['reaction']==1,'rightHandFree':b['w01HandState']['right']=='free','RPAvailable':b['RP'],'samePlane':True,'within60Feet':True,'resourceOrReactionSpent':False})
  elif k=='POLY_RESOLVE':
   a=state['actors']['A']; p=state['pendingCast']; x=inputs['spellAndTransformation']; meld=x['carriedAfterSetDown']['melds']
   if not p or p['spellId']!='polymorph': raise ValueError('Polymorph pending mismatch')
   state['pendingCast']=None; next(y for y in reversed(a['spellHistory']) if y['castId']==p['castId']).update({'resolutionStatus':'SUCCESSFUL','resolvedAt':t})
   a['form']={'spellId':'polymorph','profileId':predator['id'],'profile':predator,'appliedAt':t,'expiresAt':78.1,'sameAnchor':a['position'],'meldedItemIds':meld,'rootIdentityPreserved':True}
   a.update({'size':'Medium','bodyBox':[5,5,6],'bodyMassLb':150,'AC':13,'speed':40,'hands':0,'voice':False,'focusAccessible':False,'testOnlyMeldedItemIds':meld})
   a['testOnlyTransformationRecords'][-1].update({'status':'ACTIVE','appliedAt':t,'sameAnchor':a['position']})
   for iid in meld: state['items'][iid]['testOnlyMeldedInto']='A'
   eid='TEST_ONLY:PG328-W12-R1:POLYMORPH:A'; state['effects'][eid]={'id':eid,'spellId':'polymorph','owner':'A','target':'A','active':True,'concentration':True,'createdAt':18.1,'resolvedAt':t,'deadline':78.1,'profileId':predator['id'],'meldedItemIds':meld,'classification':'TEST_ONLY_HYPOTHETICAL_BRANCH'}
   d.update({'resolutionStatus':'SUCCESSFUL','pendingCastAfter':None,'identity':'A','HP':a['HP'],'form':a['form'],'meldedItems':meld,'tileRemainsLoose':state['items'][TILE]['custodian'] is None,'concentrationDeadline':a['concentration']['deadline']})
  elif k=='POLY_REVERT':
   a=state['actors']['A']; rec=a['testOnlyTransformationRecords'][-1]; a.update({'form':None,'size':'Medium','bodyBox':[5,5,6],'bodyMassLb':150,'AC':12,'speed':30,'hands':2,'voice':True,'focusAccessible':True,'concentration':None}); a.pop('testOnlyMeldedItemIds',None)
   rec.update({'status':'REVERTED','revertedAt':t,'sameAnchor':a['position'],'rootIdentityPreserved':True})
   for iid in rec['meldedItemIds']: state['items'][iid].pop('testOnlyMeldedInto',None)
   state['effects']['TEST_ONLY:PG328-W12-R1:POLYMORPH:A'].update({'active':False,'endedAt':t,'terminalReason':'MANDATORY_SAME_ANCHOR_REVERSION'})
   d.update({'reversionAt':t,'sameAnchor':a['position'],'formAfter':None,'HP':a['HP'],'concentrationAfter':None,'restoredEquipment':rec['meldedItemIds'],'carriedWeightLb':a['carriedWeightLb'],'carriedLoad':a['carriedLoad'],'tileRemainsLoose':state['items'][TILE]['custodian'] is None,'noHealingOrRelocation':True})
  elif k=='EFF_EXPIRY':
   aid='A' if d['spell']=='polymorph' else 'B'; a=state['actors'][aid]; q=[x for x in a['testOnlySpellEfficiencyHistory'] if x['family']==d['spell'] and x['createdAt']==d['cast'] and x['status']=='PENDING']
   for x in q: x['status']='EXPIRED_UNUSED'
   d.update({'actorId':aid,'expiredCount':len(q),'discountConsumed':False})
  elif k=='COUNTER_DISPEL':
   a=state['actors']['A']; b=state['actors']['B']; d.update({'A':{'eligible':True,'attempted':False,'disposition':'DECLINES','reactionAvailable':a['reaction']==1,'freeHand':a['w01HandState']['right']=='free','RPAvailable':a['RP'],'samePlane':a['plane']==b['plane'],'distanceFeet':inputs['spellAndTransformation']['counterspellRayToB']['distanceFeet'],'within60Feet':True,'resourcesSpent':False},'B':{'attempted':False,'selfCounterEligibility':'NOT_ADJUDICATED'},'C_D':'different plane','pendingCast':copy.deepcopy(state['pendingCast'])})
  elif k=='DISPEL_RESOLVE':
   b=state['actors']['B']; p=state['pendingCast']; x=inputs['perceptionAndDispel']['dispel']
   if not p or p['spellId']!=x['spellId']: raise ValueError('Dispel pending mismatch')
   state['pendingCast']=None; next(y for y in reversed(b['spellHistory']) if y['castId']==p['castId']).update({'resolutionStatus':'SUCCESSFUL','resolvedAt':t})
   q=x['testOnlyIntelligenceCheck']; d.update({'resolutionStatus':'SUCCESSFUL','pendingCastAfter':None,'check':{'d20':q['face'],'INT':q['intelligenceModifier'],'PB':q['proficiencyBonus'],'total':q['total'],'DC':q['dc'],'success':q['success']},'RPAfter':b['RP'],'BConcentrationPreserved':b['concentration'],'rootActiveBeforeClosure':state['effects'][ROOTID]['active']})
  elif k=='ROOT_END':
   if not any(x['kind']=='DISPEL_RESOLVE' for x in events): raise ValueError('Closure before Dispel result')
   ef=state['effects'][ROOTID]; ef.update({'active':False,'open':False,'terminalReceipt':{'time':t,'status':'ENDED_BY_SUCCESSFUL_DISPEL','spellId':'wizard.arch.dispel-magic','castId':casts['wizard.arch.dispel-magic'],'scope':'TEST_ONLY PG328-W12-R1'}})
   sp=state['spaces'][SPACE]; sp['exists']=False
   for x in sp.get('doors',[]): x['open']=False
   d.update({'activeAfter':False,'spaceExistsAfter':False,'terminalReceipt':ef['terminalReceipt'],'campaignEventAsserted':False})
  elif k=='BODY':
   aid=d['actor']; pl=d['placement']; a=state['actors'][aid]
   if (aid=='A' and a['form'] is not None) or a['death']['status']!='alive' or a['HP']!=pl['HP']: raise ValueError('Body closure mismatch')
   a['plane']='fixture:origin'; a['position']=pl['reference']; a['testOnlyQ27ClosurePose']={'bodyBounds':pl['bodyBounds'],'supportPatchId':pl['supportPatchId'],'attachedItems':pl['attachedItems']}
   for iid,ii in pl['attachedItems'].items():
    it=state['items'][iid]; it['plane']='fixture:origin'; it.setdefault('testOnlyGeometry',{})['currentBoundsFeet']=ii['closureBounds']; it['testOnlyGeometry']['containedInActorEnvelope']=True
   d.update({'planeAfter':a['plane'],'positionAfter':a['position'],'bodyBoundsAfter':pl['bodyBounds'],'supportPatchId':pl['supportPatchId'],'livingIdentityPreserved':True})
  elif k=='LOOSE':
   iid=d['id']; it=state['items'][iid]; it.update({'plane':'fixture:origin','position':d['outsidePosition'],'owner':d['owner'],'custodian':d['custodian']}); it.setdefault('testOnlyGeometry',{})['currentBoundsFeet']=d['bounds']; it['testOnlyGeometry']['supportPatchId']=d['supportPatchId']
   if iid==TILE: it['expiresAtEventTime']=d['expiry']
   d.update({'planeAfter':it['plane'],'positionAfter':it['position'],'boundsAfter':d['bounds'],'ownerAfter':it['owner'],'custodianAfter':it['custodian'],'expiryAfter':it.get('expiresAtEventTime'),'settledExactlyOnce':True})
  else: raise ValueError('Unhandled kind '+k)
  e['eventId']=f'PG328-W12-R1-E{n:03d}'; state['processedEventIds'].append(e['eventId']); ops=diff(before,state); back=inverse(ops)
  if apply(before,ops)!=state or apply(state,back)!=before: raise ValueError('Local patch failed '+e['eventId'])
  e['stateTransition']={'beforeStateSha256':ho(before),'afterStateSha256':ho(state),'forwardOperations':ops,'inverseOperations':back}; events.append(e)
 starts=sum(x['kind']=='START' for x in events); ends=sum(x['kind']=='END' for x in events)
 if (starts,ends,state['time'])!=(45,44,79.31): raise ValueError('Marker totals or endpoint')
 f=copy.deepcopy(initial); ok=True
 for e in events:
  tr=e['stateTransition']
  if ho(f)!=tr['beforeStateSha256']: ok=False; break
  f=apply(f,tr['forwardOperations'])
  if ho(f)!=tr['afterStateSha256']: ok=False; break
 r=copy.deepcopy(f); invok=True
 for e in reversed(events):
  tr=e['stateTransition']
  if ho(r)!=tr['afterStateSha256']: invok=False; break
  r=apply(r,tr['inverseOperations'])
  if ho(r)!=tr['beforeStateSha256']: invok=False; break
 if not ok or f!=state or not invok or r!=initial or ho(r)!=SH: raise ValueError('Full reversible replay failed')
 bounds={'A':c['A']['bodyBounds'],'B':c['B']['bodyBounds']}
 bounds.update({x['id']:x['bounds'] for x in c['unchangedOutsideActors']}); bounds.update({x['id']:x['bounds'] for x in c['looseItems']})
 names=list(bounds); pairs=[{'pair':[a,b],'positiveVolumeOverlap':overlap(bounds[a],bounds[b])} for i,a in enumerate(names) for b in names[i+1:]]
 A=state['actors']['A']; B=state['actors']['B']; tile=state['items'][TILE]
 if len(pairs)!=15 or any(x['positiveVolumeOverlap'] for x in pairs): raise ValueError('Q27 geometry')
 if (A['RP'],B['RP'],B['concentration']['deadline'],tile['expiresAtEventTime'])!=(46,75,613.1,3606.13): raise ValueError('Terminal ledger')
 if state['pendingCast'] is not None or state['effects'][ROOTID]['active'] or state['spaces'][SPACE]['exists']: raise ValueError('Terminal closure')
 if B['recharge'].get('wizard.arch.arcane-sight')!=0 or B['recharge'].get('wizard.arch.dispel-magic')!=2: raise ValueError('Recharge')
 trace={'classification':'TEST_ONLY_REVERSIBLE_BRANCH_STATE_RECONSTRUCTION','initialStateSha256':SH,'terminalStateSha256':ho(state),'terminalTime':79.31,'starts':starts,'ends':ends,'eventCount':len(events),'events':events,'terminalState':state,'q27CollisionPairs':pairs,'closureOrder':['root termination','A body','B body',*c['looseItemOrderByStableId']],'authority':{'applied':830,'pending':18,'acceptedUnapplied':0,'mutation':False}}
 dump(T,trace)
 replay={'classification':'TEST_ONLY_REVERSIBLE_BRANCH_STATE_RECONSTRUCTION','initialStatePath':rel(S)+'#/stateSnapshots/S030','initialState':initial,'initialStateSha256':SH,'terminalState':state,'terminalStateSha256':ho(state),'eventsAreAppliedInOrder':True,'eventCount':len(events),'forwardOperationsTotal':sum(len(x['stateTransition']['forwardOperations']) for x in events),'inverseOperationsTotal':sum(len(x['stateTransition']['inverseOperations']) for x in events),'reverseRestorationExpectedSha256':SH,'forwardReplayPass':ok,'inverseReplayPass':invok}
 w={'schemaVersion':2,'id':'PG328-W12-REVERSIBLE-WITNESS-451','supersedesWitness':{'path':rel(OLD),'sha256':hf(OLD),'finding':'W450-C01 HOLD'},'classification':'OWNER_ADOPTED_TEST_ONLY_BRANCH_WITNESS','status':'TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW','branchId':'PG328-W12-R1','component':'PG328-W12','hypotheticalOnly':True,'noCampaignEventClaim':True,'adoption':{'path':rel(O),'sha256':hf(O),'proposalPath':rel(P),'exactProposalSha256':hf(P),'ownerAdopted':True,'scope':'W12-R1 only'},'parent':{'path':rel(S),'pointer':'#/stateSnapshots/S030','replaySha256':hf(S),'snapshotSha256':SH,'timeSeconds':12.9,'parentMutated':False},'sourceBindings':bindings,'priorDirectorDisposition':{'path':rel(RB),'sha256':hf(RB),'finding':'W450-C01','status':'HOLD'},'adoptedScenario':inputs,'eventTrace':{'semantics':'Ordered reversible hypothetical state reconstruction from exact S030 through79.31.','eventCount':len(events),'regularTurnStartCount':starts,'regularTurnEndCount':ends,'events':events,'terminalProjection':c,'q27CollisionPairs':pairs},'stateTransitionReplay':replay,'terminalStateSummary':{'A':{'RP':A['RP'],'position':A['position'],'HP':A['HP'],'form':A['form'],'concentration':A['concentration']},'B':{'RP':B['RP'],'position':B['position'],'concentration':B['concentration'],'recharge':B['recharge']},'tileExpiry':tile['expiresAtEventTime'],'rootActive':state['effects'][ROOTID]['active'],'pendingCast':state['pendingCast']},'queue':{'applied':830,'pending':18,'acceptedUnapplied':0,'mutated':False},'scopeBoundary':{'testOnly':True,'sealPresent':False,'FortressAcceptedOrApplied':False,'canonicalRuleChanged':False,'campaignEventsAsserted':False,'queueChanged':False,'PG200_B06Closed':False}}
 dump(W,w)
 checks={'exact proposal/adoption/parent and S030 hashes':hf(P)==PH and hf(O)==OH and hf(S)==RH and ho(initial)==SH,'18 adopted source bindings':len(bindings)==18 and all(x['matches'] for x in bindings),'adopted scenario copied exactly':w['adoptedScenario']==inputs,'45/44 START/END processing':starts==45 and ends==44,'budgets/recharge processed':all('budgetsAfterStart' in x['details'] for x in events if x['kind']=='START') and all('unusedBudgetDisposition' in x['details'] for x in events if x['kind']=='END'),'three paid spell casts':[(x['details']['spellId'],x['details']['costRP']) for x in events if x['kind'] in sinfo]==[('wizard.arch.arcane-sight',2),('polymorph',7),('wizard.arch.dispel-magic',3)],'Sight commit concentration and resolution perception':next(x for x in events if x['kind']=='SIGHT_COMMIT')['details']['concentrationAfterCommit']['deadline']==613.1 and next(x for x in events if x['kind']=='SIGHT_RESOLVE')['details']['auraPerceptionBeginsAt']==13.3,'tile setdown and expiry':next(x for x in events if x['kind']=='TILE_DROP')['details']['expiryPreserved']==3606.13 and next(x for x in events if x['kind']=='TILE_DROP')['details']['weightAfterLb']==12,'gear meld and same-anchor reversion':next(x for x in events if x['kind']=='POLY_RESOLVE')['details']['meldedItems']==['focus-A','pack-A','cargo-A'] and next(x for x in events if x['kind']=='POLY_REVERT')['details']['sameAnchor']==[25,6,0],'Dispel23/DC19 and ordered Q27':[next(x for x in events if x['kind']=='DISPEL_RESOLVE')['details']['check']['total'],[x['kind'] for x in events if x['timeSeconds']==79.31]]==[23,['ROOT_END','BODY','BODY','LOOSE','LOOSE']],'15 collision pairs clear':len(pairs)==15 and not any(x['positiveVolumeOverlap'] for x in pairs),'terminal ledgers retained':(A['RP'],B['RP'],B['concentration']['deadline'],tile['expiresAtEventTime'])==(46,75,613.1,3606.13),'full inverse restoration':ok and invok and r==initial and ho(r)==SH,'no pending spell and fortress ended':state['pendingCast'] is None and not state['effects'][ROOTID]['active'] and not state['spaces'][SPACE]['exists'],'queue/hold scope unchanged':w['queue']=={'applied':830,'pending':18,'acceptedUnapplied':0,'mutated':False} and w['scopeBoundary']['PG200_B06Closed'] is False}
 if not all(checks.values()): raise ValueError(str([x for x,v in checks.items() if not v]))
 dump(V,{'id':'BUILD-VALIDATION-W12-451','status':'PASS','passed':len(checks),'failed':0,'checks':[{'name':x,'passed':v} for x,v in checks.items()],'witnessSha256':hf(W),'traceSha256':hf(T),'events':len(events),'starts':starts,'ends':ends,'forwardOperations':replay['forwardOperationsTotal'],'inverseOperations':replay['inverseOperationsTotal'],'terminalStateSha256':ho(state),'queue':{'applied':830,'pending':18,'acceptedUnapplied':0},'Fortress':'HELD_UNDER_PG200-B06'})
 R.write_text(f'# W12 reversible witness451 - TEST_ONLY / unsealed\n\nThis successor implements W450-C01 as a reversible hypothetical branch from exact S030 through79.31. It processes {starts} START and {ends} END markers, paid spell and resource transitions, concentration and recharge clocks, the original tile set-down, Polymorph gear melding and same-anchor reversion, Dispel23 vs DC19, and ordered Q27 closure.\n\nForward and inverse replay pass; inverse restores {SH}. Source bindings:18/18. Witness {hf(W)}; trace {hf(T)}. This branch claims no campaign event, seal, Fortress acceptance/application, canon change or queue mutation. Fortress remains HELD under PG200-B06; queue remains830/18/0.\n',encoding='utf-8',newline='\n')
 parts=[W,T,V,R,BUILD,Q,P,O,RB]
 manifest={'id':'MANIFEST-W12-451','classification':'TEST_ONLY_REVERSIBLE_WITNESS','branchId':'PG328-W12-R1','artifacts':[bind(x) for x in parts],'sourceBindings':bindings,'authority':{'applied':830,'pending':18,'acceptedUnapplied':0},'Fortress':'HELD_UNDER_PG200-B06','sealed':False}
 dump(M,manifest)
 with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for x in parts+[M]:
   zi=zipfile.ZipInfo('payload/'+x.name,(2026,11,1,0,0,0)); zi.compress_type=zipfile.ZIP_DEFLATED; z.writestr(zi,x.read_bytes())
 dump(D,{'id':'DELIVERY-W12-451','status':'READY_FOR_DIRECTOR_REVIEW','classification':'TEST_ONLY_UNSEALED','witness':bind(W),'trace':bind(T),'validation':bind(V),'manifest':bind(M),'archive':bind(Z),'sourceBindingCount':18,'eventCount':len(events),'starts':starts,'ends':ends,'forwardReplayPass':ok,'inverseReplayPass':invok,'authority':{'applied':830,'pending':18,'acceptedUnapplied':0},'Fortress':'HELD_UNDER_PG200-B06','sealed':False,'campaignEventAsserted':False,'canonChanged':False})
 print(json.dumps({'status':'PASS','checks':len(checks),'events':len(events),'starts':starts,'ends':ends,'forwardOperations':replay['forwardOperationsTotal'],'inverseOperations':replay['inverseOperationsTotal'],'witnessSha256':hf(W),'traceSha256':hf(T),'archiveSha256':hf(Z),'terminalSha256':ho(state)},indent=2))
if __name__=='__main__': main()
