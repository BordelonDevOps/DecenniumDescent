from __future__ import annotations
import copy, hashlib, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PREV=BASE/'fortress_w04_earth_pet_witness_436'
OUT=BASE/'fortress_w04_earth_pet_witness_439'
OUT.mkdir(parents=True,exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def readj(p): return json.loads(p.read_text(encoding='utf-8'))
def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def writej(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'); p.write_bytes(b); return sha(b)
def ptr_escape(s): return str(s).replace('~','~0').replace('/','~1')
def digest(v): return sha(canon(v))
def diff(a,b,path=''):
 out=[]
 if isinstance(a,dict) and isinstance(b,dict) and set(a)==set(b):
  for k in sorted(a): out.extend(diff(a[k],b[k],path+'/'+ptr_escape(k)))
 elif a!=b: out.append({'op':'replace','path':path,'before':copy.deepcopy(a),'after':copy.deepcopy(b)})
 return out
def setptr(root,path,value):
 bits=[x.replace('~1','/').replace('~0','~') for x in path.split('/')[1:]]
 cur=root
 for k in bits[:-1]: cur=cur[k]
 cur[bits[-1]]=copy.deepcopy(value)
def apply_ops(state,ops,forward=True):
 for op in ops:
  expected=op['before'] if forward else op['after']; value=op['after'] if forward else op['before']
  cur=state
  for k in [x.replace('~1','/').replace('~0','~') for x in op['path'].split('/')[1:]]: cur=cur[k]
  assert cur==expected,(op['path'],cur,expected)
  setptr(state,op['path'],value)
def project_actor(a,name):
 return {'id':a['id'],'profile':a['profile'],'profileSHA256':a['profileSHA256'],'class':a['class'],'level':a['level'],
  'HP':a['HP'],'RP':a['RP'],'Dissonance':a['Dissonance'],'Refrain':a['Refrain'],'lastSpell':a['lastSpell'],
  'preparedFamiliesUsed':copy.deepcopy(a['preparedFamiliesUsed']),'spellHistory':copy.deepcopy(a['spellHistory']),'resourceHistory':copy.deepcopy(a['resourceHistory']),
  'concentration':copy.deepcopy(a['concentration']),'spellEfficiency':copy.deepcopy(a['spellEfficiency']),'magicThisTurn':a['magicThisTurn'],
  'recharge':copy.deepcopy(a['recharge']),'position':copy.deepcopy(a['position']),'plane':a['plane'],'equipment':copy.deepcopy(a['equipment']),
  'carriedWeightLb':a['carriedWeightLb'],'carriedLoad':a['carriedLoad'],'Action':a['action'],'BonusAction':a['bonusAction'],
  'Reaction':a['reaction'],'movementFeetAvailable':a['movement'],'regularSchedule':copy.deepcopy(a['regularSchedule']),
  'handState':({'left':'focus-A','right':'PG328-W01-403:CLAY-TILE-1'} if name=='A' else {'left':'focus-B','right':'free'} if name=='B' else {'status':'unchanged; not resolved in this branch'}),
  'companionCommandRound':a.get('companionCommandRound'),'companionOffenseRound':a.get('companionOffenseRound')}

oldReplay=readj(PREV/'W04_REPLAY_436_TESTONLY.json')
oldValidation=readj(PREV/'BUILD_VALIDATION_436.json')
parent=readj(BASE/'fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json')
S=parent['stateSnapshots']['S030']
oldSha=sha((PREV/'W04_REPLAY_436_TESTONLY.json').read_bytes())
assert oldSha=='59a3d3445dd64535f5bd1b9283bc5c701d0da5e1e87e84484cac719e4b78f260'
assert oldReplay['adoption']['exactProposalSha256']=='c80c91547ee4a07c687c0ba346ce0bcde861d3dda84a0389d12aeb48b7588d41'
assert oldReplay['parent']['terminalStateSha256']=='6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c'

r=copy.deepcopy(oldReplay)
r['id']='PG328-W04-TESTONLY-WITNESS-439'
r['supersedes']={'id':oldReplay['id'],'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w04_earth_pet_witness_436/W04_REPLAY_436_TESTONLY.json','sha256':oldSha,'handling':'preserved unchanged as historical review revision; this successor adds replayable transitions and applies C02-C03 only'}
r['status']='PROPOSED_TEST_ONLY_REPLAY_CORRECTIONS_PENDING_DIRECTOR_REVIEW'
r['witnessId']='PG328-W04-EARTH-PET-WITNESS-439'
r['branchId']='PG328-W04-R1'
r['timelineCoverage']['regularActorMarkers'][3]['authoredAction']='Action: cast summon-earth-pet at18.02; Bonus Action: command at18.05'
r['timelineCoverage']['regularActorMarkers'][3]['authoredMovement']=0
r['timelineCoverage']['regularActorMarkers'][3]['authoredReaction']='none; A spends no Reaction'
# C03: the 18.02 snapshot precedes B's 18.03 decline.
r['branchStateAfterCommitment']['time']=18.02
r['branchStateAfterCommitment']['B']['declinedAt']=None
r['branchStateAfterCommitment']['B']['responseStatus']='eligible; response pending at18.02'
r['branchStateAfterCommitment']['B']['reactionAvailableAtWindow']=1
r['branchStateAfterCommitment']['B']['reactionSpent']=False
r['branchStateAfterCommitment']['B']['RPSpent']=0
r['branchStateAfterCommitment']['B']['rechargeStarted']=False
r['branchStateAfterSuccessfulResolution']['time']=18.04
r['branchStateAfterSuccessfulResolution']['actorA']['committedSpellRecord']['status']='resolved_success'
r['branchStateAfterSuccessfulResolution']['actorA']['castResolution']={'status':'success_in_hypothetical_branch','resolvedAt':18.04}
r['branchStateAfterSuccessfulResolution']['B']={'position':[15,10,0],'responseStatus':'declined_at18.03','declinedAt':18.03,'reactionAvailableAtWindow':1,'reactionSpent':False,'RP':80,'RPSpent':0,'rechargeStarted':False}

# The projection stores every inherited turn schedule and all state fields that change in this branch.
actors={name:project_actor(actor,name) for name,actor in S['actors'].items()}
initial={'time':12.9,'mode':S['mode'],'clock':copy.deepcopy(S['clock']),'actors':actors,'items':copy.deepcopy(S['items']),
 'effects':copy.deepcopy(S['effects']),'pendingCast':copy.deepcopy(S.get('pendingCast')),'pet':None,'castRecord':None,'counterspellResponse':None,
 'parentSnapshotDigest':oldReplay['parent']['terminalStateSha256'],'branchId':'PG328-W04-R1'}
# S030 tile custody/hand state is exactly parent-bound; owner-adopted set-down is the first branch transition.
TILE='PG328-W01-403:CLAY-TILE-1'; PET='PG328-W04-R1:EARTH-PET-001'; initialDigest=digest(initial)
state=copy.deepcopy(initial); ledger=[]
baseClock=copy.deepcopy(S['clock']); baseTime=12.9

def set_time(t):
 delta=float(t)-baseTime
 state['time']=float(t)
 state['clock']['elapsedSeconds']=round(baseClock['elapsedSeconds']+delta,9)
 for k in ('OpeningRemaining','HornRemaining'):
  if baseClock.get(k) is not None: state['clock'][k]=round(baseClock[k]-delta,9)

def record(t,phase,source,mutator):
 before=copy.deepcopy(state); set_time(t); mutator()
 ops=diff(before,state)
 inv=[{'op':'replace','path':x['path'],'before':copy.deepcopy(x['after']),'after':copy.deepcopy(x['before'])} for x in reversed(ops)]
 entry={'transitionId':f'PG328-W04-R1:TR-{len(ledger)+1:03d}','time':float(t),'phase':phase,'source':source,
        'beforeStateSha256':digest(before),'forwardOperations':ops,'afterStateSha256':digest(state),'inverseOperations':inv,
        'reversible':True}
 # Prove this step's patch and inverse against independent copies before accepting it.
 f=copy.deepcopy(before);apply_ops(f,ops,True);assert digest(f)==entry['afterStateSha256']
 apply_ops(f,inv,True);assert digest(f)==entry['beforeStateSha256']
 ledger.append(entry)

def marker_start(m,index):
 actor=m['actor']; t=float(m['start']);
 def mutate():
  a=state['actors'][actor]; sch=a['regularSchedule']
  a['Action']=1;a['BonusAction']=1;a['Reaction']=1;a['movementFeetAvailable']=30
  if actor=='A': a['magicThisTurn']=False
  sch['starts'].append(t);sch['nextStart']=round(t+sch['period'],1);sch['nextEnd']=round(t+sch['endOffset'],1)
 record(t,'REGULAR_START',{'timelinePointer':f'/timelineCoverage/regularActorMarkers/{index}/start','actor':actor},mutate)

def marker_end(m,index):
 actor=m['actor']; t=float(m['end']); start=float(m['start'])
 def mutate():
  a=state['actors'][actor];sch=a['regularSchedule']
  a['Action']=0;a['BonusAction']=0;a['movementFeetAvailable']=0
  sch['ends'].append(t);sch['nextEnd']=None
  spent_action=1 if actor=='A' and start==18.0 else 0
  spent_ba=1 if actor=='A' and start==18.0 else 0
  sch['budgetHistory'].append({'time':start,'action':1,'BA':1,'Reaction':1,'Move':30,'recharge':{},
   'endDisposition':{'regularTurnEndedAt':t,'recordedAt':t,'Action':{'spent':spent_action,'unusedExpired':1-spent_action},
   'BonusAction':{'spent':spent_ba,'unusedExpired':1-spent_ba},'Reaction':{'spent':0,'availableOffTurnUntilSpentOrNextOwnStart':True},
   'MovementFeet':{'granted':30,'spent':0,'unusedExpired':30}}})
 record(t,'REGULAR_END',{'timelinePointer':f'/timelineCoverage/regularActorMarkers/{index}/end','actor':actor,
  'authoredAction':m.get('authoredAction'),'authoredMovement':m.get('authoredMovement',0),'authoredReaction':m.get('authoredReaction')},mutate)

def setdown():
 a=state['actors']['A'];tile=state['items'][TILE]
 a['handState']={'left':'focus-A','right':'free'};a['equipment']=[x for x in a['equipment'] if x!=TILE]
 a['carriedWeightLb']=12;a['carriedLoad']=1.2
 tile['custodian']=None;tile['position']=[25,5,0];tile['heldBy']=None;tile['heldBoundsFeet']=None
 tile['groundedBoundsFeet']={'x':[25,26],'y':[5,6],'z':[0,0.25]};tile['owner']=None

def cast_commit():
 a=state['actors']['A'];a['Action']=0;a['RP']=48;a['Dissonance']=0;a['Refrain']=0
 a['preparedFamiliesUsed']=list(a['preparedFamiliesUsed'])+['summon-earth-pet'];a['lastSpell']='summon-earth-pet';a['magicThisTurn']=True
 cast={'castId':'PG328-W04-R1:CAST-EARTH-PET-001','spellId':'summon-earth-pet','class':'Wizard','school':'Conjuration','rank':3,
  'time':18.02,'cost':5,'RPBefore':53,'RPAfter':48,'firstPreparedFamily':True,'Dissonance':[0,0],'Refrain':[0,0],
  'ActionSpent':True,'concentrationCommittedBeforeInterruption':True,'status':'committed_pending_counterspell'}
 a['concentration']={'castId':cast['castId'],'spellId':cast['spellId'],'startedAt':18.02,'commitmentPrecedesCounterspellWindow':True}
 a['spellHistory']=copy.deepcopy(a['spellHistory'])+[cast]
 a['resourceHistory']=copy.deepcopy(a['resourceHistory'])+[{'event':cast['castId'],'RP':-5,'poolAfter':48,'discount':False}]
 state['castRecord']=cast
 state['pendingCast']={'castId':cast['castId'],'status':'pending_interruption_resolution','committedAt':18.02,'concentrationCommitted':True}

def decline():
 state['counterspellResponse']={'actor':'B','status':'declined','time':18.03,'reactionAvailableBefore':1,'reactionSpent':False,'RPBefore':80,'RPSpent':0,'rechargeStarted':False}

def resolve():
 cast=state['castRecord'];cast['status']='resolved_success';cast['resolvedAt']=18.04
 state['pendingCast']=None
 a=state['actors']['A'];a['spellEfficiency']={'source':'PG200-W20 /acquisitionLedger/18/choices/0; Wizard /cards/15','sameFamily':'summon-earth-pet','pendingDiscountRp':1,'expiresAtEnd':24.9,'used':False}
 profile=copy.deepcopy(r['branchStateAfterSuccessfulResolution']['pet']['profile'])
 state['pet']={'instanceId':PET,'spellId':'summon-earth-pet','createdAt':18.04,'expiresAt':78.0,'exists':True,
  'plane':a['plane'],'profile':profile,'position':[30,12,0],'spawnBoundsFeet':{'x':[30,35],'y':[12,17],'z':[0,6]},
  'destinationPosition':[20,16,0],'command':None,'phaseCount':0,'lastPhaseAt':None,'movementSpentTotal':0,'actionState':'ready',
  'phaseSchedule':[18.9,24.9,30.9,36.9,42.9,48.9,54.9,60.9,66.9,72.9]}
 state['counterspellResponse']['status']='declined; cast survives'

def command():
 a=state['actors']['A'];a['BonusAction']=0
 state['pet']['command']={'time':18.05,'sourceActor':'A','BonusActionSpent':True,'routeFeet':[[30,12,0],[30,16,0],[20,16,0]],'movementFeet':14,'postMovementAction':'Dodge'}

def pet_phase(t,event_id,first=False):
 pet=state['pet']; assert pet and pet['exists']
 if first:
  pet['position']=[20,16,0];pet['movementSpentTotal']=14
  pet['lastPhaseMovementFeet']=14;pet['lastPhaseChoice']='Dodge'
 else:
  pet['lastPhaseMovementFeet']=0;pet['lastPhaseChoice']='Dodge'
 pet['phaseCount']+=1;pet['lastPhaseAt']=float(t);pet['actionState']='Dodge completed at attached phase'

def efficiency_expire():
 state['actors']['A']['spellEfficiency']=None

def pet_expire():
 pet=state['pet'];assert pet and pet['exists'] and pet['phaseCount']==10
 pet['exists']=False;pet['endedAt']=78.0;pet['lastPose']=copy.deepcopy(pet['position']);pet['lastEligibleDodge']=72.9
 pet['removalReason']='finite duration expires at A regular START78.0 before A chooses'
 state['actors']['A']['concentration']=None

# Build ordered steps from every inherited regular marker plus every authored W04 event.
steps=[]
markers=r['timelineCoverage']['regularActorMarkers']
for i,m in enumerate(markers):
 steps.append((float(m['start']),0,'start',m,i))
 if float(m['end'])<=78.0: steps.append((float(m['end']),0,'end',m,i))
for i,e in enumerate(r['events']):
 if e['eventId'].endswith(':SET-DOWN-CLAY-TILE'): steps.append((e['time'],10,'setdown',e,i))
 elif e['eventId'].endswith(':CAST-COMMIT'): steps.append((e['time'],20,'cast',e,i))
 elif e['eventId'].endswith(':B-COUNTERSPELL-DECLINE'): steps.append((e['time'],30,'decline',e,i))
 elif e['eventId'].endswith(':CAST-SURVIVES-PET-CREATED'): steps.append((e['time'],40,'resolve',e,i))
 elif e['eventId'].endswith(':BONUS-ACTION-COMMAND'): steps.append((e['time'],50,'command',e,i))
 elif e['kind']=='PENDING_DISCOUNT_EXPIRY': steps.append((e['time'],10,'efficiency_expiry',e,i))
 elif e['kind']=='FINITE_DURATION_EXPIRY': steps.append((e['time'],10,'pet_expiry',e,i))
 elif e['kind'] in ('OWNER_END_AND_ATTACHED_COMPANION_PHASE','UNCOMMANDED_ATTACHED_PHASE'):
  # Pet phase follows its owner END at the same timestamp (or, at18.9, follows the combined source event).
  steps.append((e['time'],20,'pet_phase',e,i))
steps.sort(key=lambda x:(x[0],x[1]))
for t,priority,kind,obj,index in steps:
 if kind=='start': marker_start(obj,index)
 elif kind=='end': marker_end(obj,index)
 elif kind=='setdown': record(t,'TILE_SET_DOWN',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},setdown)
 elif kind=='cast': record(t,'CAST_COMMITMENT',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},cast_commit)
 elif kind=='decline': record(t,'COUNTERSPELL_DECLINE',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},decline)
 elif kind=='resolve': record(t,'SUCCESSFUL_RESOLUTION_AND_PET_CREATION',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},resolve)
 elif kind=='command': record(t,'BONUS_ACTION_COMPANION_COMMAND',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},command)
 elif kind=='efficiency_expiry': record(t,'UNUSED_SPELL_EFFICIENCY_EXPIRES_AT_A_END',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},efficiency_expire)
 elif kind=='pet_phase': record(t,'ATTACHED_PET_PHASE_AFTER_OWNER_END',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},lambda t=t,e=obj:pet_phase(t,e['eventId'],first=(t==18.9)))
 elif kind=='pet_expiry': record(t,'FINITE_DURATION_EXPIRY_BEFORE_A_CHOICES',{'eventId':obj['eventId'],'eventPointer':f'/events/{index}'},pet_expire)

assert len([x for x in ledger if x['phase']=='REGULAR_START'])==44
assert len([x for x in ledger if x['phase']=='REGULAR_END'])==43
assert len([x for x in ledger if x['phase']=='ATTACHED_PET_PHASE_AFTER_OWNER_END'])==10
assert state['time']==78.0 and state['actors']['A']['regularSchedule']['nextEnd']==78.9
assert state['actors']['A']['magicThisTurn'] is False and state['actors']['A']['spellEfficiency'] is None
assert state['actors']['A']['concentration'] is None and not state['pet']['exists']
assert state['counterspellResponse']['time']==18.03 and state['counterspellResponse']['RPSpent']==0 and state['counterspellResponse']['reactionSpent'] is False
assert state['actors']['A']['RP']==48 and state['actors']['A']['BonusAction']==1

# Independently replay every forward transition, then reverse every inverse operation to exact S030 projection.
replayed=copy.deepcopy(initial)
for entry in ledger:
 assert digest(replayed)==entry['beforeStateSha256'],entry['transitionId']
 apply_ops(replayed,entry['forwardOperations'],True)
 assert digest(replayed)==entry['afterStateSha256'],entry['transitionId']
assert digest(replayed)==digest(state)
reverse=copy.deepcopy(state)
for entry in reversed(ledger):
 assert digest(reverse)==entry['afterStateSha256'],entry['transitionId']
 apply_ops(reverse,entry['inverseOperations'],True)
 assert digest(reverse)==entry['beforeStateSha256'],entry['transitionId']
assert digest(reverse)==initialDigest

r['branchStateAfterTileSetDown']['time']=18.01
r['branchStateAfterCommitment']['B']['declinedAt']=None
r['branchTerminalStateAt78']['time']=78.0
r['branchTerminalStateAt78']['actorA'].update({'Action':state['actors']['A']['Action'],'BonusAction':state['actors']['A']['BonusAction'],
 'Reaction':state['actors']['A']['Reaction'],'movementFeetAvailable':state['actors']['A']['movementFeetAvailable'],
 'magicThisTurn':state['actors']['A']['magicThisTurn'],'regularScheduleAtExpiry':{'nextStart':84.0,'nextEnd':78.9}})
r['branchTerminalStateAt78']['futureScheduledEnd']=78.9
r['branchTerminalStateAt78']['pet']={'instanceId':PET,'exists':False,'endedAt':78.0,'lastPose':[20,16,0],'lastEligibleDodge':72.9}
r['transitionChain']={'schemaVersion':1,'classification':'BRANCH_ONLY_TEST_ONLY_REPLAYABLE_STATE_PROJECTION',
 'initialSource':{'path':oldReplay['parent']['path'],'pointer':'/stateSnapshots/S030','sha256':oldReplay['parent']['terminalStateSha256'],
 'projectionSha256':initialDigest,'projection':initial,'scope':'All branch-mutated fields plus every A/B/C/D regular-turn resource/schedule marker; omitted fields inherit unchanged from the exact parent digest.'},
 'orderedTransitions':ledger,'terminalProjectionSha256':digest(state),'terminalProjection':state,
 'accountedRegularStarts':44,'accountedRegularEndsThrough78':43,'unprocessedFutureScheduledEnds':[{'actor':'A','time':78.9,'timelinePointer':'/timelineCoverage/regularActorMarkers/43/end','status':'future; not advanced in this replay'}],
 'forwardReplayVerified':True,'reverseRestorationVerified':True,'reverseRestoresInitialProjectionSha256':digest(reverse),
 'orderingRules':['At each regular START, refresh Action/Bonus Action/Reaction/movement and update next START/END schedule.','At each regular END, expire unused Action/Bonus Action/movement; unused Reaction persists until the actor next STARTs.','At18.9, resolve A END before the commanded attached pet movement and Dodge.','At24.9, resolve A END, expire the unused Spell Efficiency entry, then the attached pet phase.','At78.0, A START refreshes resources; pet/concentration expire before A can choose an action. The future A END78.9 is not processed.']}

# Hash-bound correction packet and validation: exact adoption and parent remain unchanged.
validation={'schemaVersion':1,'id':'PG328-W04-BUILD-VALIDATION-439','classification':'OWNER_ADOPTED_TEST_ONLY_BRANCH_VALIDATION','status':'PASS_PENDING_DIRECTOR_REVIEW',
 'adoptionProposalSha256':oldReplay['adoption']['exactProposalSha256'],'adoptionRecordSha256':oldReplay['adoption']['sha256'],
 'parentStateSha256':oldReplay['parent']['terminalStateSha256'],'supersededReplaySha256':oldSha,'replaySha256':'PENDING','checks':[
 {'name':'exact owner adoption preserved','status':'PASS','evidence':'Proposal430 exact SHA and owner adoption436 record are unchanged.'},
 {'name':'parent S030 digest preserved','status':'PASS','evidence':'Replay starts from unchanged W01-403 S030 terminal digest.'},
 {'name':'forward transition coverage','status':'PASS','evidence':f'{len(ledger)} reversible transition records include all44 regular STARTs, all43 ENDs through78.0, and all authored events.'},
 {'name':'inverse restoration','status':'PASS','evidence':f'Reversing all {len(ledger)} inverse patches restores the initial S030 projection digest {initialDigest} exactly.'},
 {'name':'clock and schedule updates','status':'PASS','evidence':'Each marker updates elapsed clock and all applicable actor regularSchedule starts/ends/nextStart/nextEnd and budgetHistory.'},
 {'name':'A18 resource expenditure','status':'PASS','evidence':'A spends Action on summon-earth-pet and Bonus Action on18.05 command; no owner movement or Reaction is spent.'},
 {'name':'B response time','status':'PASS','evidence':'At18.02 B response remains pending; at18.03 B declines with Reaction, RP and recharge unchanged.'},
 {'name':'Mage/Wizard magicThisTurn lifecycle','status':'PASS','evidence':'Wizard first-family cast keeps magicThisTurn true through END18.9; reset occurs at START24.'},
 {'name':'Spell Efficiency expiry order','status':'PASS','evidence':'Unused family discount persists until A END24.9 and is then removed before the pet attached phase.'},
 {'name':'pet command, position and Dodge phases','status':'PASS','evidence':'Command at18.05; pet moves14ft and Dodges at18.9; zero-movement defensive Dodges at24.9..72.9.'},
 {'name':'concentration and finite expiry','status':'PASS','evidence':'At A START78.0 concentration and pet are removed before owner choices; A END78.9 remains future scheduled only.'},
 {'name':'A18 marker consistency','status':'PASS','evidence':'A18 authoredAction records cast and Bonus Action command; owner movement is0 and Reaction expenditure none.'},
 {'name':'commitment snapshot consistency','status':'PASS','evidence':'Snapshot18.02 contains pending B response; decline is first recorded at18.03.'},
 {'name':'geometry and route premises unchanged','status':'PASS','evidence':'No geometry, pose, profile, support, ray, or source premise changed from adopted proposal430 / replay436.'},
 {'name':'boundary','status':'PASS','evidence':'No seal, Fortress acceptance/application, canon or queue change; queue remains830/18/0.'}],
 'result':{'passed':15,'failed':0,'directorReviewRequired':True,'ownerAdoptionUnchanged':True,'sealPresent':False,'fortressAcceptanceOrApplication':False,'canonChanged':False,'queueChanged':False}}
corrections={'schemaVersion':1,'id':'PG328-W04-DIRECTOR-CORRECTIONS-439','classification':'DIRECTOR_FEEDBACK_RECONCILIATION','status':'C01_C03_APPLIED_PENDING_DIRECTOR_REVIEW',
 'priorReplay':{'path':'fortress_w04_earth_pet_witness_436/W04_REPLAY_436_TESTONLY.json','sha256':oldSha},
 'adoptionProposalSha256':oldReplay['adoption']['exactProposalSha256'],'correctedReplay':{'path':'W04_REPLAY_439_TESTONLY.json','sha256':'PENDING'},
 'corrections':[
 {'id':'W04-436-C01','field':'/events; /branchTerminalStateAt78','disposition':f'Added {len(ledger)} ordered reversible state transitions. Every forward operation has an inverse. Forward application and reverse restoration verified; all regular START/END markers through78.0, state clock, schedule, resource spend, pet phases, efficiency expiry, concentration and pet removal are accounted.78.9 remains future only.'},
 {'id':'W04-436-C02','field':'/timelineCoverage/regularActorMarkers/3/authoredAction','disposition':'A18 row now records Action cast at18.02 and Bonus Action command at18.05; owner movement0 and no Reaction expenditure.'},
 {'id':'W04-436-C03','field':'/branchStateAfterCommitment/B/declinedAt','disposition':'At18.02 B response is eligible/pending with resources unchanged; decline first occurs18.03 and remains unspent.'}],
 'unchangedBoundaries':{'adoptedProposalBytesChanged':False,'parentBytesChanged':False,'canonChanged':False,'queueChanged':False,'sealed':False,'FortressAcceptanceOrApplication':False,'queue':'830 applied / 18 pending / 0 accepted-unapplied'}}
replay_sha=writej(OUT/'W04_REPLAY_439_TESTONLY.json',r)
validation['replaySha256']=replay_sha
writej(OUT/'BUILD_VALIDATION_439.json',validation)
corrections['correctedReplay']['sha256']=replay_sha
writej(OUT/'W04_DIRECTOR_CORRECTIONS_439.json',corrections)
(OUT/'README.md').write_text(f'''# W04 TEST_ONLY replay 439\n\nThis is a successor replay for the already owner-adopted exact proposal 430. It applies Director corrections C01-C03 without changing proposal430, the W01 S030 parent, geometry, or adopted premises.\n\n- Replay SHA-256: `{replay_sha}`\n- Parent S030 SHA-256: `{oldReplay['parent']['terminalStateSha256']}`\n- Adopted proposal SHA-256: `{oldReplay['adoption']['exactProposalSha256']}`\n- Reversible transition records: {len(ledger)}\n- Forward replay and inverse restoration: PASS\n- Validation: {validation['result']['passed']} passed, 0 failed; awaiting Director review.\n- No seal, Fortress acceptance/application, canon, or queue change; queue remains 830/18/0.\n''',encoding='utf-8',newline='\n')
# Final on-disk integrity and inverse checks.
r2=readj(OUT/'W04_REPLAY_439_TESTONLY.json');v2=readj(OUT/'BUILD_VALIDATION_439.json')
assert v2['replaySha256']==sha((OUT/'W04_REPLAY_439_TESTONLY.json').read_bytes())
assert r2['transitionChain']['reverseRestorationVerified'] and r2['transitionChain']['forwardReplayVerified']
assert r2['branchStateAfterCommitment']['B']['declinedAt'] is None
assert r2['timelineCoverage']['regularActorMarkers'][3]['authoredAction'].startswith('Action: cast')
print(json.dumps({'replaySha256':replay_sha,'transitions':len(ledger),'forward':True,'inverseRestore':digest(reverse)==initialDigest,'checks':validation['result'],'out':str(OUT)},indent=2))
