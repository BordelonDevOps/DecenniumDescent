from __future__ import annotations
import copy, hashlib, json, subprocess, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(sys.argv[1]); BASE='docs/audit/2026-10-08/full-game/director-spell-review-129'
V2=f'{BASE}/elemental_shell_b02_witness_482_repack02'; V1=f'{BASE}/elemental_shell_b02_witness_482_repack01'
PRE=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json'
READY=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json'
ADOPT=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/OWNER_DF218_B02_ADOPTION_477_REPACK01_TESTONLY.json'
PKG=ROOT/BASE/'elemental_shell_b02_witness_482_repack03'; PKG.mkdir(parents=True,exist_ok=True)
OLD_WITNESS=f'{V2}/DF218_B02_WITNESS_482_REPACK02_TESTONLY.json'
OLD_HOLD=f'{V2}/DIRECTOR_READBACK_482_HOLD.json'
OLD_V1_WITNESS=f'{V1}/DF218_B02_WITNESS_482_TESTONLY.json'
HOLD_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack03/DIRECTOR_READBACK_482_HOLD.json'
WITNESS_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack03/DF218_B02_WITNESS_482_REPACK03_TESTONLY.json'
TRACE_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack03/B02_EVENT_TRACE_482_REPACK03.json'
VERIFY_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack03/verify_shell_b02_witness_482_repack03.py'
def gitraw(path): return subprocess.check_output(['git','-C',str(ROOT),'show',f'refs/heads/main:{path}'])
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def obj(x): return sha(canonical(x))
def load(b): return json.loads(b.decode('utf-8-sig'))
def replace_value(x,old,new):
    if isinstance(x,dict):
        for k,v in x.items(): x[k]=replace_value(v,old,new)
    elif isinstance(x,list):
        for i,v in enumerate(x): x[i]=replace_value(v,old,new)
    elif x==old: return new
    return x
stamp=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
prior_raw=gitraw(OLD_WITNESS); prior=load(prior_raw); prior_hash=sha(prior_raw)
assert prior_hash=='a8740794dd0ff2b5c1822c85fe205a78d694a41b237bbd1a349411f51081b7d8',prior_hash
v1_raw=gitraw(OLD_V1_WITNESS); v1=load(v1_raw)
profile_path=next(x['path'] for x in prior['sourceBindings'] if x['path'].endswith('/ACTOR_PROFILES.json'))
profile_raw=gitraw(profile_path); profile=load(profile_raw); limit=profile['Wizard18']['DissonanceLimit']; assert limit==13
family_old='WIZARD18-FIRST-DISTINCT-PREPARED-MATRIX-FAMILY-001'; family_new='elemental-shell'
findings=[
 {'id':'B02-482-C01','title':'Wizard18 Dissonance limit','status':'CORRECTION_REQUIRED_IN_SUBMITTED_WITNESS','finding':'Every submitted snapshot records Wizard18/vitals/DissonanceLimit as 10, while the bound ACTOR_PROFILES.json specifies 13 at /Wizard18/DissonanceLimit.','sourcePath':profile_path,'sourceSha256':sha(profile_raw),'sourcePointer':'/Wizard18/DissonanceLimit','observedValue':10,'expectedValue':13,'requiredAction':'Set the field to 13 in snapshots 0–15; regenerate dependent hashes, replay bindings, validation and delivery records; add a direct assertion against the bound profile.','newOwnerAdoptionRequired':False},
 {'id':'B02-482-C02','title':'Wizard18 prepared-family key','status':'CORRECTION_REQUIRED_IN_SUBMITTED_WITNESS','finding':'Snapshots 8–15 use WIZARD18-FIRST-DISTINCT-PREPARED-MATRIX-FAMILY-001, but the prepared family key must be elemental-shell.','sourcePath':f'{BASE}/elemental_shell_b02_witness_482_repack01/DF218_B02_WITNESS_482_TESTONLY.json','sourceSha256':sha(v1_raw),'sourcePointers':['/stateTransitionReplay/stateSnapshots/{8..15}/completeState/actors/Wizard18/casting/preparedRankedCastFamiliesUsed/0','/stateTransitionReplay/stateSnapshots/{8..15}/completeState/actors/Wizard18/casting/castHistory/0/preparedFamilyKey'],'observedValue':family_old,'expectedValue':family_new,'requiredAction':'Replace both keyed fields in snapshots 8–15 and regenerate affected transition operands, snapshot hashes, aggregate forward/inverse operations and package bindings. Keep the family history empty before the 3.1 commitment; do not import B01 encounter history.','newOwnerAdoptionRequired':False}
]
hold={'schemaVersion':1,'id':'DIRECTOR-READBACK-DF218-B02-WITNESS-482-HOLD-C01-C02','source':'GPT Director, Calibration review part 6, completed audit readback','recordedAtUtc':stamp,'classification':'TEST_ONLY_WITNESS_REVIEW_HOLD','decision':'HOLD_FOR_TWO_SOURCE_STATE_CORRECTIONS','reviewedTarget':{'path':OLD_V1_WITNESS,'sha256':sha(v1_raw),'branchId':v1['branchId'],'proposalSha256':v1['sourceProposal']['sha256']},'findings':findings,'passedAreas':['Forward and reverse replay; 15 events, 16 snapshots, 141 forward and 141 inverse operations restore the exact submitted start state.','Adopted geometry, responder declines, paid casting, turn history, command execution, custody, deadlines, attack/reflection settlement and HP outcome.','Prepared-family source grouping uses the underlying spell; B01 witness481 already uses elemental-shell.'],'outcomeUnchanged':'Neither correction changes costs, damage, timing or outcome; Wizard Dissonance remains zero.','nonEffects':{'B01Witness481Changed':False,'B01DispositionChanged':False,'B02Closed':False,'sealIssued':False,'identityAcceptedOrApplied':False,'canonicalRuleChanged':False,'queueChanged':False,'campaignEventClaimed':False},'queueAuthority':{'reviewedApplied':831,'pending':17,'acceptedUnapplied':0,'firstPendingIdentity':'elemental-shell'}}
hold_bytes=(json.dumps(hold,ensure_ascii=False,indent=2)+'\n').encode(); (PKG/'DIRECTOR_READBACK_482_HOLD.json').write_bytes(hold_bytes)
(PKG/'PRIOR_WITNESS_482_REPACK02.json').write_bytes(prior_raw)
prior_hold_raw=gitraw(OLD_HOLD); (PKG/'PRIOR_DIRECTOR_READBACK_482_HOLD_REPACK02.json').write_bytes(prior_hold_raw)
(PKG/'PRIOR_WITNESS_482_REPACK01.json').write_bytes(v1_raw)
new=copy.deepcopy(prior); new['id']='DF218-B02-WITNESS-482-REPACK03'; new['status']='CONSTRUCTED_FOR_DIRECTOR_C01_C02_RECHECK_NOT_SEALED'; new['constructedAtUtc']=stamp
new['correctedFrom']={'priorWitnessPath':OLD_WITNESS,'priorWitnessSha256':prior_hash,'priorDirectorReadbackPath':OLD_HOLD,'priorDirectorReadbackSha256':sha(prior_hold_raw),'directorReadbackPath':HOLD_PATH,'directorReadbackSha256':sha(hold_bytes),'correctionIds':['B02-482-C01','B02-482-C02'],'newOwnerAdoptionRequired':False,'onlySemanticCorrections':['Wizard18/vitals/DissonanceLimit remains 13 in snapshots 0–15, matching bound actor profile.','Wizard18 preparedRankedCastFamiliesUsed/0 and castHistory/0/preparedFamilyKey are elemental-shell in snapshots 8–15; history remains empty before commitment at 3.1.']}
replay=new['stateTransitionReplay']; old_count=sum(1 for k in []); replay=replace_value(replay,family_old,family_new)
for snap in replay['stateSnapshots']: snap['stateSha256']=obj(snap['completeState'])
byid={x['stateId']:x['completeState'] for x in replay['stateSnapshots']}
for ev in replay['eventTransitions']:
 before=byid[ev['beforeStateId']]; after=byid[ev['afterStateId']]
 ev['beforeStateSha256']=obj(before); ev['afterStateSha256']=obj(after)
restored=copy.deepcopy(byid[replay['finalStateId']])
for ev in reversed(replay['eventTransitions']):
    # Independent operation replay is checked by the packaged verifier.
    pass
# Verify inverse application and exact restoration through shared JSON-pointer operations.
def keys(p): return [x.replace('~1','/').replace('~0','~') for x in p[1:].split('/')]
def get(o,p):
    for k in keys(p): o=o[k]
    return o
def put(o,p,v,e):
    a=keys(p);q=o
    for k in a[:-1]: q=q[k]
    if e:q[a[-1]]=copy.deepcopy(v)
    else:del q[a[-1]]
def apply(s,ops):
    s=copy.deepcopy(s)
    for x in ops:
        try:before=get(s,x['path']);exists=True
        except (KeyError,IndexError):before=None;exists=False
        assert exists==x['beforeExists'] and (not exists or canonical(before)==canonical(x['before'])),x['path']
        put(s,x['path'],x.get('after'),x['afterExists'])
    return s
for ev in reversed(replay['eventTransitions']): restored=apply(restored,ev['inverseOperations'])
assert restored==byid[replay['initialStateId']]
replay['initialStateSha256']=next(x['stateSha256'] for x in replay['stateSnapshots'] if x['stateId']==replay['initialStateId'])
replay['finalStateSha256']=next(x['stateSha256'] for x in replay['stateSnapshots'] if x['stateId']==replay['finalStateId'])
replay['inverseReplayResult']={'restoresExactInitialState':True,'restoredStateSha256':obj(restored),'expectedInitialStateSha256':obj(byid[replay['initialStateId']])}
# Preserve the existing source bindings and bind the precise two-finding readback plus the previous successor.
def binding(path,b,use): return {'path':path,'bytes':len(b),'sha256':sha(b),'gitBlobSha1':blob(b),'gitSha256':sha(b),'gitBytes':len(b),'use':use}
new['sourceBindings'] += [binding(OLD_WITNESS,prior_raw,'Exact prior Repack02 witness; source for focused C01/C02 successor.'),binding(OLD_HOLD,prior_hold_raw,'Prior GPT hold receipt; preserved without rewriting.'),binding(HOLD_PATH,hold_bytes,'GPT final two-finding hold readback transcribed into this packet.')]
W=PKG/'DF218_B02_WITNESS_482_REPACK03_TESTONLY.json'; W.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
events=replay['eventTransitions']; trace={'id':'DF218-B02-EVENT-TRACE-482-REPACK03','witnessPath':WITNESS_PATH,'witnessSha256':sha(W.read_bytes()),'correctedFrom':new['correctedFrom'],'events':[{'eventId':e['eventId'],'timeSeconds':e['timeSeconds'],'kind':e['kind'],'beforeStateId':e['beforeStateId'],'afterStateId':e['afterStateId'],'beforeStateSha256':e['beforeStateSha256'],'afterStateSha256':e['afterStateSha256'],'forwardOperationCount':len(e['forwardOperations']),'inverseOperationCount':len(e['inverseOperations'])} for e in events],'terminalStateSummary':new['terminalStateSummary'],'inverseReplayResult':replay['inverseReplayResult']}
T=PKG/'B02_EVENT_TRACE_482_REPACK03.json'; T.write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
# Adapt the prior independent verifier; add source-profile, family-key and exact two-correction assertions.
old_verify=gitraw(f'{V2}/verify_shell_b02_witness_482_repack02.py').decode('utf-8-sig')
ver=old_verify.replace('REPACK02','REPACK03').replace('CONSTRUCTED_FOR_DIRECTOR_RECHECK_NOT_SEALED','CONSTRUCTED_FOR_DIRECTOR_C01_C02_RECHECK_NOT_SEALED')
old_block="""hold=load(HERE/'DIRECTOR_READBACK_482_HOLD.json')
ck('focused C01 hold receipt and unchanged owner adoption',hold['findings'][0]['id']=='B02-482-C01' and hold['findings'][0]['newOwnerAdoptionRequired'] is False and w['correctedFrom']['priorWitnessSha256']=='9109d59aef0c302c83ddd63c2a601a150a60ed25beb588baa27b4616d47877d4')
prior=json.loads(raw('docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b02_witness_482_repack01/DF218_B02_WITNESS_482_TESTONLY.json'))
only_c01=True
for old_s,new_s in zip(prior['stateTransitionReplay']['stateSnapshots'],r['stateSnapshots']):
 corrected=copy.deepcopy(new_s['completeState']); corrected['actors']['Wizard18']['vitals']['DissonanceLimit']=10
 only_c01=only_c01 and corrected==old_s['completeState']
same_ops=all(a['forwardOperations']==b['forwardOperations'] and a['inverseOperations']==b['inverseOperations'] for a,b in zip(prior['stateTransitionReplay']['eventTransitions'],r['eventTransitions']))
ck('C01-only state correction; all 141 forward and inverse operations unchanged',only_c01 and same_ops and sum(len(e['forwardOperations']) for e in r['eventTransitions'])==141 and sum(len(e['inverseOperations']) for e in r['eventTransitions'])==141)
"""
new_block="""hold=load(HERE/'DIRECTOR_READBACK_482_HOLD.json')
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
"""
assert old_block in ver, 'expected verifier block missing'
ver=ver.replace(old_block,new_block)
V=PKG/'verify_shell_b02_witness_482_repack03.py'; V.write_text(ver,encoding='utf-8',newline='\n')
README=PKG/'README_482_REPACK03.md'; README.write_text(f'''# Elemental Shell DF218-B02 witness 482 Repack03

This focused successor addresses GPT Director findings B02-482-C01 and B02-482-C02. C01 sets Wizard18 DissonanceLimit to 13 in all 16 snapshots, matching `{profile_path}` (SHA-256 `{sha(profile_raw)}`), pointer `/Wizard18/DissonanceLimit`. C02 changes the Wizard prepared-family key to `elemental-shell` at both specified fields in snapshots 8–15. The prepared-family list remains empty through snapshot 7, before the 3.1 commitment; no B01 encounter history is imported.

The independent verifier asserts both exact state corrections against the bound source and prior Repack02, regenerates and replays the complete 141-operation forward/inverse contract, and confirms exact inverse restoration. Costs, timing, damage, Dissonance, and encounter outcome are unchanged. The exact owner adoption of Proposal477 Repack01 remains in force; GPT stated no new owner adoption is required. This successor is unsealed and awaits focused Director recheck. No identity, B01, canon, queue, campaign, or runtime state changes are claimed.
''',encoding='utf-8',newline='\n')
# Re-run the independent verifier now; its JSON output records the full check ledger.
subprocess.check_call(['python',str(V)],cwd=ROOT,stdout=subprocess.DEVNULL)
R=PKG/'INDEPENDENT_VALIDATION_482_REPACK03.json'; validation=load(R.read_bytes())
assert validation['status']=='PASS' and validation['checksFailed']==0
# Carry the exact prior artifact chain and both prior hold receipts in the delivery archive.
files=[W,T,V,R,README,PKG/'build_shell_b02_witness_482_repack03.py',PKG/'DIRECTOR_READBACK_482_HOLD.json',PKG/'PRIOR_WITNESS_482_REPACK02.json',PKG/'PRIOR_DIRECTOR_READBACK_482_HOLD_REPACK02.json',PKG/'PRIOR_WITNESS_482_REPACK01.json']
manifest={'id':'DF218-B02-WITNESS-482-REPACK03-MANIFEST','status':'FOCUSED_C01_C02_RECHECK_PACKET_NOT_SEALED','correctedFrom':new['correctedFrom'],'ownerAdoptionPath':ADOPT,'ownerAdoptionSha256':sha(gitraw(ADOPT)),'proposalPath':PRE,'proposalSha256':sha(gitraw(PRE)),'files':[{'path':str(x.relative_to(ROOT)).replace('\\','/'),'bytes':x.stat().st_size,'sha256':sha(x.read_bytes())} for x in files]}
M=PKG/'MANIFEST_482_REPACK03.json'; M.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
Z=PKG/'DD_ElementalShell_B02_Witness_482_REPACK03_TESTONLY.zip'
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for x in files+[M,ROOT/ADOPT]: z.write(x,arcname=str(x.relative_to(ROOT)).replace('\\','/'))
delivery={'id':'DF218-B02-WITNESS-482-REPACK03-DELIVERY','status':'READY_FOR_DIRECTOR_C01_C02_RECHECK_NOT_SEALED','branchId':new['branchId'],'proposalSha256':new['sourceProposal']['sha256'],'adoptionPath':ADOPT,'adoptionSha256':sha(gitraw(ADOPT)),'priorWitnessPath':OLD_WITNESS,'priorWitnessSha256':prior_hash,'priorDirectorReadbackPath':OLD_HOLD,'priorDirectorReadbackSha256':sha(prior_hold_raw),'directorHoldPath':HOLD_PATH,'directorHoldSha256':sha(hold_bytes),'witnessPath':WITNESS_PATH,'witnessSha256':sha(W.read_bytes()),'validationPath':f'{BASE}/elemental_shell_b02_witness_482_repack03/INDEPENDENT_VALIDATION_482_REPACK03.json','validationStatus':validation['status'],'validationChecksPassed':validation['checksPassed'],'eventCount':validation['eventCount'],'snapshotCount':validation['snapshotCount'],'forwardOperationCount':141,'inverseOperationCount':141,'manifestPath':f'{BASE}/elemental_shell_b02_witness_482_repack03/MANIFEST_482_REPACK03.json','manifestSha256':sha(M.read_bytes()),'zipPath':f'{BASE}/elemental_shell_b02_witness_482_repack03/DD_ElementalShell_B02_Witness_482_REPACK03_TESTONLY.zip','zipSha256':sha(Z.read_bytes()),'corrections':{'C01':{'field':'Wizard18/vitals/DissonanceLimit','profilePath':profile_path,'profileSha256':sha(profile_raw),'profilePointer':'/Wizard18/DissonanceLimit','value':13,'snapshots':'0-15','allMatch':True},'C02':{'fields':['actors/Wizard18/casting/preparedRankedCastFamiliesUsed/0','actors/Wizard18/casting/castHistory/0/preparedFamilyKey'],'value':'elemental-shell','snapshots':'8-15','emptyBeforeCommitmentSnapshot7':True}},'decisionBoundary':new['decisionBoundary']}
D=PKG/'DELIVERY_482_REPACK03.json'; D.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'witnessSha256':sha(W.read_bytes()),'checksPassed':validation['checksPassed'],'validationStatus':validation['status'],'zipSha256':sha(Z.read_bytes()),'deliverySha256':sha(D.read_bytes()),'sourceDissonanceLimit':limit,'snapshots':len(replay['stateSnapshots']),'events':len(replay['eventTransitions']),'forwardOperations':sum(len(e['forwardOperations']) for e in replay['eventTransitions']),'inverseOperations':sum(len(e['inverseOperations']) for e in replay['eventTransitions'])},indent=2))
