import copy,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REVIEW=ROOT.parent; REPO=REVIEW.parents[4]
W=ROOT/'W12_WITNESS_451_TESTONLY.json'; T=ROOT/'W12_LIFECYCLE_TRACE_451.json'; V=ROOT/'BUILD_VALIDATION_451.json'; M=ROOT/'MANIFEST_451.json'; Z=ROOT/'DD_Fortress_W12_Reversible_Witness_451_TESTONLY.zip'; D=ROOT/'DELIVERY_451.json'
P=ROOT/'PG328_W12_REVERSION_OWNER_PROPOSAL_445_TESTONLY.json'; O=ROOT/'OWNER_PG328_W12_ADOPTION_445_TESTONLY.json'; S=REVIEW/'fortress_w01_structural_damage_witness_403_repack02'/'W01_REPLAY_403.json'; TILE='PG328-W01-403:CLAY-TILE-1'; ROOTID='RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1'; SPACE=ROOTID+'/space'
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def hf(p): return sha(Path(p).read_bytes())
def ho(x): return sha(canon(x))
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
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
w=read(W); tr=w['stateTransitionReplay']; ev=w['eventTrace']['events']; parent=read(S); initial=parent['stateSnapshots']['S030']; state=copy.deepcopy(initial); checks={}
checks['exact proposal/adoption/parent/S030 hashes']=hf(P)=='93d31941e6a6d4d059cb3a108d0e247d07cc8e6cce395712f1c0ad45523df14c' and hf(O)=='83d25ca677ea8d910575a3bcc87be6a29837553112d3445e1c50cc954a8f4c60' and hf(S)=='2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb' and ho(initial)=='6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c'
checks['all adopted source bindings verify at proposal commit']=len(w['sourceBindings'])==18 and all(hashlib.sha256(__import__('subprocess').check_output(['git','show',read(P)['readAtCommit']+':'+x['path']],cwd=REPO)).hexdigest()==x['sha256']==x['actualSha256'] and x['matches'] and x['resolvedAtCommit']==read(P)['readAtCommit'] for x in w['sourceBindings'])
checks['event ordering and IDs are unique']=ev==sorted(ev,key=lambda x:(x['timeSeconds'],x['orderAtTime'],x['kind'])) and len({x['eventId'] for x in ev})==len(ev)
forward=True
for e in ev:
 q=e['stateTransition']
 if ho(state)!=q['beforeStateSha256']: forward=False; break
 state=apply(state,q['forwardOperations'])
 if ho(state)!=q['afterStateSha256']: forward=False; break
checks['event-level forward replay reaches terminal state']=forward and state==tr['terminalState'] and ho(state)==tr['terminalStateSha256']
reverse=copy.deepcopy(state); inverse=True
for e in reversed(ev):
 q=e['stateTransition']
 if ho(reverse)!=q['afterStateSha256']: inverse=False; break
 reverse=apply(reverse,q['inverseOperations'])
 if ho(reverse)!=q['beforeStateSha256']: inverse=False; break
checks['inverse replay restores byte-bound S030']=inverse and reverse==initial and ho(reverse)=='6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c'
checks['45 START / 44 END markers']=sum(x['kind']=='START' for x in ev)==45 and sum(x['kind']=='END' for x in ev)==44 and tr['eventCount']==len(ev)
checks['actual start budgets/end expirations and recharge']=all('budgetsAfterStart' in x['details'] for x in ev if x['kind']=='START') and all('unusedBudgetDisposition' in x['details'] for x in ev if x['kind']=='END') and next(x for x in ev if x['kind']=='START' and x['details']['actorId']=='B' and x['timeSeconds']==19)['details']['rechargeAfter']['wizard.arch.arcane-sight']==1 and next(x for x in ev if x['kind']=='START' and x['details']['actorId']=='B' and x['timeSeconds']==25)['details']['rechargeAfter']['wizard.arch.arcane-sight']==0
def event(kind,actor,time): return next(x for x in ev if x['kind']==kind and x['timeSeconds']==time and (actor is None or x['details'].get('actorId')==actor))
b_end=event('END','B',13.9); b_start=event('START','B',19.0); a_end=event('END','A',18.9); a_start=event('START','A',24.0)
checks['cast flag persists through END and resets at next START']=b_end['details']['magicThisTurnAfterEnd'] is True and a_end['details']['magicThisTurnAfterEnd'] is True and not any(x['path']=='/actors/B/magicThisTurn' for x in b_end['stateTransition']['forwardOperations']) and not any(x['path']=='/actors/A/magicThisTurn' for x in a_end['stateTransition']['forwardOperations']) and b_start['details']['magicThisTurn'] is False and a_start['details']['magicThisTurn'] is False and any(x['path']=='/actors/B/magicThisTurn' and x.get('value') is False for x in b_start['stateTransition']['forwardOperations']) and any(x['path']=='/actors/A/magicThisTurn' and x.get('value') is False for x in a_start['stateTransition']['forwardOperations'])
poly=next(x for x in ev if x['kind']=='POLY_RESOLVE'); revert=next(x for x in ev if x['kind']=='POLY_REVERT')
a_form_starts=[x for x in ev if x['kind']=='START' and x['details']['actorId']=='A' and x['timeSeconds'] in [24.0,30.0,36.0,42.0,48.0,54.0,60.0,66.0,72.0,78.0]]
a_form_ends=[x for x in ev if x['kind']=='END' and x['details']['actorId']=='A' and x['timeSeconds'] in [18.9,24.9,30.9,36.9,42.9,48.9,54.9,60.9,66.9,72.9]]
a_reversion_end=event('END','A',78.9)
poly_move=poly['details'].get('movementRecalculation',{}); revert_move=revert['details'].get('movementRecalculation',{})
checks['Polymorph movement follows operative Speed and preserves spent movement']=poly_move=={'reason':'operative Polymorph form Speed becomes 40 ft','speedBeforeFeet':30,'speedAfterFeet':40,'movementSpentFeet':0,'remainingBeforeFeet':30,'remainingAfterFeet':40,'turnGrantAfterRecalculationFeet':40} and revert_move=={'reason':'mandatory reversion restores ordinary form Speed to 30 ft','speedBeforeFeet':40,'speedAfterFeet':30,'movementSpentFeet':0,'remainingBeforeFeet':40,'remainingAfterFeet':30,'turnGrantAtStartFeet':40,'recalculatedAwayFeet':10} and len(a_form_starts)==10 and all(x['details']['budgetsAfterStart']['MovementFeet']==40 and x['details']['operativeSpeedFeet']==40 and any(o['path']=='/actors/A/movement' and o.get('value')==40 for o in x['stateTransition']['forwardOperations']) for x in a_form_starts) and len(a_form_ends)==10 and all(x['details']['unusedBudgetDisposition']['MovementFeet']['granted']==40 and x['details']['unusedBudgetDisposition']['MovementFeet']['spent']==0 for x in a_form_ends) and a_reversion_end['details']['unusedBudgetDisposition']['MovementFeet']=={'granted':40,'spent':0,'unusedExpired':30,'recalculatedAway':10} and next(x for x in state['actors']['A']['regularSchedule']['budgetHistory'] if x['time']==78.0)['Move']==40 and state['actors']['A']['speed']==30 and state['actors']['A']['movement']==0
commits=[x for x in ev if x['kind'] in ['SIGHT_COMMIT','POLY_COMMIT','DISPEL_COMMIT']]
checks['three spells are paid with exact adopted costs']=[(x['details']['spellId'],x['details']['costRP']) for x in commits]==[('wizard.arch.arcane-sight',2),('polymorph',7),('wizard.arch.dispel-magic',3)]
checks['Sight concentration starts at commit; perception waits for success']=next(x for x in ev if x['kind']=='SIGHT_COMMIT')['details']['concentrationAfterCommit']['deadline']==613.1 and next(x for x in ev if x['kind']=='SIGHT_RESOLVE')['details']['auraPerceptionBeginsAt']==13.3
checks['tile setdown clears right hand, reduces load, preserves expiry']=next(x for x in ev if x['kind']=='TILE_DROP')['details']['handsAfter']['right']=='free' and next(x for x in ev if x['kind']=='TILE_DROP')['details']['weightAfterLb']==12 and next(x for x in ev if x['kind']=='TILE_DROP')['details']['expiryPreserved']==3606.13
checks['Polymorph melds exact existing gear and reverts at same anchor']=next(x for x in ev if x['kind']=='POLY_RESOLVE')['details']['meldedItems']==['focus-A','pack-A','cargo-A'] and next(x for x in ev if x['kind']=='POLY_REVERT')['details']['sameAnchor']==[25,6,0] and state['actors']['A']['form'] is None
checks['successful 23 vs DC19 Dispel precedes Q27 order']=next(x for x in ev if x['kind']=='DISPEL_RESOLVE')['details']['check']['total']==23 and [x['kind'] for x in ev if x['timeSeconds']==79.31]==['ROOT_END','BODY','BODY','LOOSE','LOOSE']
checks['Q27 15 collision pairs clear']=len(w['eventTrace']['q27CollisionPairs'])==15 and not any(x['positiveVolumeOverlap'] for x in w['eventTrace']['q27CollisionPairs'])
checks['terminal RP, concentration, recharge and tile clock']=state['actors']['A']['RP']==46 and state['actors']['B']['RP']==75 and state['actors']['B']['concentration']['deadline']==613.1 and state['actors']['B']['recharge']['wizard.arch.arcane-sight']==0 and state['actors']['B']['recharge']['wizard.arch.dispel-magic']==2 and state['items'][TILE]['expiresAtEventTime']==3606.13
checks['unused Sight/Polymorph efficiency expires; Dispel window remains pending']=all(x['status']=='EXPIRED_UNUSED' for aid in ['A','B'] for x in state['actors'][aid]['testOnlySpellEfficiencyHistory'] if x['family'] in ['polymorph','wizard.arch.arcane-sight']) and next(x for x in state['actors']['B']['testOnlySpellEfficiencyHistory'] if x['family']=='wizard.arch.dispel-magic')['status']=='PENDING'
checks['root and pending cast terminal state']=not state['effects'][ROOTID]['active'] and state['spaces'][ROOTID+'/space']['exists'] is False and state['pendingCast'] is None
checks['authority and test-only boundary unchanged']=w['queue']=={'applied':830,'pending':18,'acceptedUnapplied':0,'mutated':False} and w['scopeBoundary']['queueChanged'] is False and w['scopeBoundary']['PG200_B06Closed'] is False and w['scopeBoundary']['sealPresent'] is False and w['scopeBoundary']['campaignEventsAsserted'] is False
v=read(V); m=read(M); d=read(D); t=read(T)
checks['build validation binds current witness and trace']=v['status']=='PASS' and v['witnessSha256']==hf(W) and v['traceSha256']==hf(T) and v['passed']==len(v['checks']) and all(x['passed'] for x in v['checks'])
checks['trace equals witness event ledger']=t['events']==ev and t['terminalState']==state and t['terminalStateSha256']==ho(state)
checks['manifest and delivery bind all principal files']=any(x['path'].endswith('W12_WITNESS_451_TESTONLY.json') and x['sha256']==hf(W) for x in m['artifacts']) and d['witness']['sha256']==hf(W) and d['trace']['sha256']==hf(T) and d['archive']['sha256']==hf(Z)
with zipfile.ZipFile(Z) as z:
 bad=z.testzip(); names=set(z.namelist()); expected=[W,T,V,ROOT/'README_WITNESS_451.md',ROOT/'BUILD_W12_WITNESS_451.py',ROOT/'VERIFY_W12_WITNESS_451.py',P,O,REVIEW/'DIRECTOR_READBACK_455.json',M]
 archive_ok=bad is None and all('payload/'+x.name in names and z.read('payload/'+x.name)==x.read_bytes() for x in expected)
checks['archive CRC and exact payload bytes']=archive_ok
for k,vv in checks.items(): print(('PASS: ' if vv else 'FAIL: ')+k)
if not all(checks.values()): raise SystemExit(1)
print(f'PASS: {sum(checks.values())}/{len(checks)} independent checks; W12 remains TEST_ONLY and unsealed.')
