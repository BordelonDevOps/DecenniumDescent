import copy,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; REVIEW=HERE.parent; ROOT=REVIEW.parents[4]; BASE='docs/audit/2026-10-08/full-game/director-spell-review-129'
PRE=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json'; READY=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json'; ADOPT=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/OWNER_DF218_B02_ADOPTION_477_REPACK01_TESTONLY.json'; W=HERE/'DF218_B02_WITNESS_482_REPACK03_TESTONLY.json'; T=HERE/'B02_EVENT_TRACE_482_REPACK03.json'
def raw(p): return subprocess.check_output(['git','-C',str(ROOT),'show',f'refs/heads/main:{p}'])
def sha(b): return hashlib.sha256(b).hexdigest()
def can(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def h(x): return sha(can(x))
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def keys(p): return [x.replace('~1','/').replace('~0','~') for x in p[1:].split('/')]
def get(o,p):
 for k in keys(p): o=o[k]
 return o
def put(o,p,v,e):
 a=keys(p); q=o
 for k in a[:-1]: q=q[k]
 if e:q[a[-1]]=copy.deepcopy(v)
 else:del q[a[-1]]
def apply(s,ops):
 s=copy.deepcopy(s)
 for x in ops:
  try:o=get(s,x['path']); e=True
  except (KeyError,IndexError):o=None;e=False
  assert e==x['beforeExists'] and (not e or can(o)==can(x['before'])),x['path'];put(s,x['path'],x.get('after'),x['afterExists'])
 return s
w=load(W); t=load(T); a=load(ROOT/ADOPT); ready=json.loads(raw(READY)); pre=json.loads(raw(PRE)); r=w['stateTransitionReplay']; checks=[]
def ck(n,b):checks.append({'check':n,'passed':bool(b)});assert b,n
ck('proposal hash and readiness',sha(raw(PRE))==w['adoption']['proposalSha256']==ready['reviewedPreflight']['sha256'] and w['status']=='CONSTRUCTED_FOR_DIRECTOR_C01_C02_RECHECK_NOT_SEALED')
ck('exact owner adoption and seven premises',a['ownerAuthorization']['verbatim']=='Yes—adopt exact 477 Repack01' and len(a['scope']['adoptedPremises'])==7 and a['scope']['branchId']==w['branchId'])
decl={x['path']:x for x in pre['sourceBindings']}; corr={x['path']:x for x in json.loads(raw(READY))['sourceByteCorrespondence']}; bound={x['path']:x for x in w['sourceBindings']}
ck('17 exact source bindings',set(decl).issubset(bound) and len(decl)==17)
for p,b in decl.items():
 g=raw(p);ck('source '+p,sha(g)==corr[p]['gitSha256'] and len(g)==corr[p]['gitBytes'] and bound[p]['gitBlobSha1']==hashlib.sha1(b'blob '+str(len(g)).encode()+b'\0'+g).hexdigest())
profile_path=next(p for p in decl if p.endswith('/ACTOR_PROFILES.json'))
profile=json.loads(raw(profile_path))
ck('Wizard18 Dissonance limit equals bound actor profile in all snapshots',profile['Wizard18']['DissonanceLimit']==13 and all(x['completeState']['actors']['Wizard18']['vitals']['DissonanceLimit']==profile['Wizard18']['DissonanceLimit'] for x in r['stateSnapshots']))
hold=load(HERE/'DIRECTOR_READBACK_482_HOLD.json')
findings={x['id']:x for x in hold['findings']}
ck('GPT C01/C02 hold receipt; exact corrections need no new adoption',set(findings)=={'B02-482-C01','B02-482-C02'} and all(x['newOwnerAdoptionRequired'] is False for x in findings.values()) and w['correctedFrom']['priorWitnessSha256']=='a8740794dd0ff2b5c1822c85fe205a78d694a41b237bbd1a349411f51081b7d8')
prior=json.loads(raw('docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b02_witness_482_repack02/DF218_B02_WITNESS_482_REPACK02_TESTONLY.json'))
expected=copy.deepcopy(prior['stateTransitionReplay'])
def replace_family(x):
 if isinstance(x,dict):
  for k,v in x.items(): x[k]=replace_family(v)
 elif isinstance(x,list):
  for i,v in enumerate(x): x[i]=replace_family(v)
 elif x=='WIZARD18-FIRST-DISTINCT-PREPARED-MATRIX-FAMILY-001': return 'elemental-shell'
 return x
expected=replace_family(expected)
for snap in expected['stateSnapshots']: snap['stateSha256']=h(snap['completeState'])
expected_states={x['stateId']:x['completeState'] for x in expected['stateSnapshots']}
for ev in expected['eventTransitions']:
 ev['beforeStateSha256']=h(expected_states[ev['beforeStateId']]); ev['afterStateSha256']=h(expected_states[ev['afterStateId']])
expected['initialStateSha256']=next(x['stateSha256'] for x in expected['stateSnapshots'] if x['stateId']==expected['initialStateId'])
expected['finalStateSha256']=next(x['stateSha256'] for x in expected['stateSnapshots'] if x['stateId']==expected['finalStateId'])
rev=copy.deepcopy(expected_states[expected['finalStateId']])
for ev in reversed(expected['eventTransitions']): rev=apply(rev,ev['inverseOperations'])
expected['inverseReplayResult']={'restoresExactInitialState':True,'restoredStateSha256':h(rev),'expectedInitialStateSha256':h(expected_states[expected['initialStateId']])}
family_ok=all(s['completeState']['actors']['Wizard18']['casting']['preparedRankedCastFamiliesUsed']==([] if i<8 else ['elemental-shell']) and (i<8 or s['completeState']['actors']['Wizard18']['casting']['castHistory'][0]['preparedFamilyKey']=='elemental-shell') for i,s in enumerate(r['stateSnapshots']))
ck('C02 exact family key, empty before 3.1 and elemental-shell after commitment',family_ok)
ck('C01/C02-only correction; regenerated replay/aggregate ops and 141 forward/inverse operations',r==expected and sum(len(e['forwardOperations']) for e in r['eventTransitions'])==141 and sum(len(e['inverseOperations']) for e in r['eventTransitions'])==141)
ck('15 events and 16 snapshots',len(r['eventTransitions'])==15 and len(r['stateSnapshots'])==16)
sn={x['stateId']:x['completeState'] for x in r['stateSnapshots']};ck('snapshot hashes',all(x['stateSha256']==h(x['completeState']) for x in r['stateSnapshots']))
cur=copy.deepcopy(sn[r['initialStateId']])
for e in r['eventTransitions']:
 ck('forward '+e['eventId'],h(cur)==e['beforeStateSha256']);cur=apply(cur,e['forwardOperations']);ck('after '+e['eventId'],cur==sn[e['afterStateId']] and h(cur)==e['afterStateSha256']);ck('inverse '+e['eventId'],apply(cur,e['inverseOperations'])==sn[e['beforeStateId']]);cur=copy.deepcopy(sn[e['afterStateId']])
rev=copy.deepcopy(sn[r['finalStateId']])
for e in reversed(r['eventTransitions']):rev=apply(rev,e['inverseOperations'])
ck('complete inverse exact restoration',rev==sn[r['initialStateId']] and r['inverseReplayResult']['restoresExactInitialState'])
f=sn[r['finalStateId']];a=f['actors'];m=a['Mage9-PROPOSED'];wz=a['Wizard18'];p=a['GreaterFirePet-R2-PROPOSED']
ck('paid costs and declined Counterspells',m['vitals']['RP']==16 and wz['vitals']['RP']==42 and all(not x['activated'] and x['rpSpent']==0 and not x['reactionSpent'] for x in wz['casting']['counterspell']['responseHistory']+m['casting']['counterspell']['responseHistory']))
ck('Mage Dissonance remains at first END then vents at later END',next(x for x in r['stateSnapshots'] if x['timeSeconds']==0.9)['completeState']['actors']['Mage9-PROPOSED']['vitals']['Dissonance']==1 and m['vitals']['Dissonance']==0)
ck('original source deadlines live at terminal tick',f['timeSeconds']==7.0 and f['shellSource']['deadlineSeconds']==63.3 and p['sourceClock']['deadlineSeconds']==60.3)
ck('complete Pet profile and no aura tick',set(p['abilities'])=={'STR','DEX','CON','INT','WIS','CHA'} and p['RP'] is None and p['conditions']==[] and p['HP']==57 and not any(x.get('hostileAuraAttempt',False) for x in p['defensivePhaseReceipts']))
ck('attack, Shell settlement, one reflected root',f['lastSettlement']['attack']['total']==20 and f['lastSettlement']['damage']['preDefenseTotal']==7 and p['HP']==57 and len(f['consumedOnceOnlyKeys'])==1 and f['damageRoots'][1]['parentRootId']==f['damageRoots'][0]['rootId'] and not f['damageRoots'][1]['recursiveReflection'])
ck('no seal, identity, canon, queue, runtime or campaign change',not any(w['decisionBoundary'][k] for k in ('B02DirectorPass','B02Closed','identityAcceptedOrApplied','canonicalRuleChanged','queueChanged','runtimeOrGameplayUse','campaignEventClaimed','sealIssued')))
out={'id':'DF218-B02-WITNESS-482-REPACK03-INDEPENDENT-VALIDATION','status':'PASS','checksPassed':len(checks),'checksFailed':0,'proposalSha256':sha(raw(PRE)),'adoptionSha256':sha((ROOT/ADOPT).read_bytes()),'witnessSha256':sha(W.read_bytes()),'traceSha256':sha(T.read_bytes()),'eventCount':len(r['eventTransitions']),'snapshotCount':len(r['stateSnapshots']),'forwardInverseReplay':r['inverseReplayResult'],'queueAndIdentityUnchanged':True,'checks':checks}
(HERE/'INDEPENDENT_VALIDATION_482_REPACK03.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2))
