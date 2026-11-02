from __future__ import annotations
import copy, hashlib, json, subprocess, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(sys.argv[1]); BASE='docs/audit/2026-10-08/full-game/director-spell-review-129'
OLD_DIR=f'{BASE}/elemental_shell_b02_witness_482_repack01'
PRE=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json'
READY=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json'
ADOPT=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/OWNER_DF218_B02_ADOPTION_477_REPACK01_TESTONLY.json'
PKG=ROOT/BASE/'elemental_shell_b02_witness_482_repack02'; PKG.mkdir(parents=True,exist_ok=True)
OLD_WITNESS=f'{OLD_DIR}/DF218_B02_WITNESS_482_TESTONLY.json'
OLD_VERIFY=f'{OLD_DIR}/verify_shell_b02_witness_482.py'
HOLD_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack02/DIRECTOR_READBACK_482_HOLD.json'
WITNESS_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack02/DF218_B02_WITNESS_482_REPACK02_TESTONLY.json'
TRACE_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack02/B02_EVENT_TRACE_482_REPACK02.json'
VERIFY_PATH=f'{BASE}/elemental_shell_b02_witness_482_repack02/verify_shell_b02_witness_482_repack02.py'

def gitraw(path): return subprocess.check_output(['git','-C',str(ROOT),'show',f'refs/heads/main:{path}'])
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def obj(x): return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load(b): return json.loads(b.decode('utf-8-sig'))
def pointer(p): return [x.replace('~1','/').replace('~0','~') for x in p[1:].split('/')]
def get(o,p):
    for k in pointer(p): o=o[k]
    return o
def put(o,p,v,exists):
    ks=pointer(p); q=o
    for k in ks[:-1]: q=q[k]
    if exists:q[ks[-1]]=copy.deepcopy(v)
    else:del q[ks[-1]]
def apply(s,ops):
    s=copy.deepcopy(s)
    for x in ops:
        try:old=get(s,x['path']); exists=True
        except (KeyError,IndexError):old=None;exists=False
        assert exists==x['beforeExists'] and (not exists or json.dumps(old,sort_keys=True)==json.dumps(x['before'],sort_keys=True)),x['path']
        put(s,x['path'],x.get('after'),x['afterExists'])
    return s

old_raw=gitraw(OLD_WITNESS); old=load(old_raw); old_hash=sha(old_raw)
assert old_hash=='9109d59aef0c302c83ddd63c2a601a150a60ed25beb588baa27b4616d47877d4'
profile_path=next(x['path'] for x in old['sourceBindings'] if x['path'].endswith('/ACTOR_PROFILES.json'))
profile_raw=gitraw(profile_path); profile=load(profile_raw)
limit=profile['Wizard18']['DissonanceLimit']; assert limit==13
stamp=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
hold={'schemaVersion':1,'id':'DIRECTOR-READBACK-DF218-B02-WITNESS-482-HOLD','source':'GPT Director, Calibration review part 6, completed audit readback','recordedAtUtc':stamp,'classification':'TEST_ONLY_WITNESS_REVIEW_HOLD','decision':'HOLD_FOR_ONE_SOURCE_STATE_CORRECTION','reviewedTarget':{'path':OLD_WITNESS,'sha256':old_hash,'branchId':old['branchId'],'proposalSha256':old['sourceProposal']['sha256']},'findings':[{'id':'B02-482-C01','title':'Wizard18 Dissonance limit','status':'CORRECTION_REQUIRED','finding':'Every snapshot records Wizard18/vitals/DissonanceLimit as 10, while the bound ACTOR_PROFILES.json specifies 13 at /Wizard18/DissonanceLimit.','sourcePath':profile_path,'sourceSha256':sha(profile_raw),'sourcePointer':'/Wizard18/DissonanceLimit','observedValue':10,'expectedValue':13,'requiredAction':'Set the field to 13 in snapshots 0–15; regenerate dependent hashes, replay bindings, validation and delivery records; add a direct assertion against the bound profile.','newOwnerAdoptionRequired':False}],'passedAreas':['Forward and reverse replay; 15 events, 16 snapshots, 141 forward and 141 inverse operations restore the exact submitted start state.','Adopted geometry, responder declines, paid casting, turn history, command execution, custody, deadlines, attack/reflection settlement and HP outcome.'],'outcomeUnchanged':'Costs and outcomes do not change; Wizard Dissonance remains zero.','nonEffects':{'B01Witness481Changed':False,'B02Closed':False,'sealIssued':False,'identityAcceptedOrApplied':False,'canonicalRuleChanged':False,'queueChanged':False,'campaignEventClaimed':False},'queueAuthority':{'reviewedApplied':831,'pending':17,'acceptedUnapplied':0,'firstPendingIdentity':'elemental-shell'}}
hold_bytes=(json.dumps(hold,ensure_ascii=False,indent=2)+'\n').encode()
(PKG/'DIRECTOR_READBACK_482_HOLD.json').write_bytes(hold_bytes)
(PKG/'PRIOR_WITNESS_482_REPACK01.json').write_bytes(old_raw)
new=copy.deepcopy(old); new['id']='DF218-B02-WITNESS-482-REPACK02'; new['status']='CONSTRUCTED_FOR_DIRECTOR_RECHECK_NOT_SEALED'; new['constructedAtUtc']=stamp
new['correctedFrom']={'priorWitnessPath':OLD_WITNESS,'priorWitnessSha256':old_hash,'directorReadbackPath':HOLD_PATH,'directorReadbackSha256':sha(hold_bytes),'correctionId':'B02-482-C01','newOwnerAdoptionRequired':False,'onlySemanticCorrection':'Wizard18/vitals/DissonanceLimit: 10 -> 13 in all 16 snapshots; no cast cost, Dissonance value or encounter outcome changed.'}
replay=new['stateTransitionReplay']; snapshots=replay['stateSnapshots']; assert len(snapshots)==16
for snap in snapshots:
    snap['completeState']['actors']['Wizard18']['vitals']['DissonanceLimit']=limit
    snap['stateSha256']=obj(snap['completeState'])
byid={x['stateId']:x['completeState'] for x in snapshots}
for ev in replay['eventTransitions']:
    before=byid[ev['beforeStateId']]; after=byid[ev['afterStateId']]
    assert apply(before,ev['forwardOperations'])==after and apply(after,ev['inverseOperations'])==before
    ev['beforeStateSha256']=obj(before); ev['afterStateSha256']=obj(after)
replay['initialStateSha256']=snapshots[0]['stateSha256']; replay['finalStateSha256']=snapshots[-1]['stateSha256']
restored=copy.deepcopy(byid[replay['finalStateId']])
for ev in reversed(replay['eventTransitions']): restored=apply(restored,ev['inverseOperations'])
assert restored==byid[replay['initialStateId']]
replay['inverseReplayResult']={'restoresExactInitialState':True,'restoredStateSha256':obj(restored),'expectedInitialStateSha256':obj(byid[replay['initialStateId']])}
new['terminalStateSummary']['wizard']['DissonanceLimit']=limit
new['sourceBindings'].append({'path':OLD_WITNESS,'bytes':len(old_raw),'sha256':old_hash,'gitBlobSha1':blob(old_raw),'gitSha256':old_hash,'gitBytes':len(old_raw),'use':'Exact prior witness reviewed under B02-482-C01; preserved unchanged.'})
new['sourceBindings'].append({'path':HOLD_PATH,'bytes':len(hold_bytes),'sha256':sha(hold_bytes),'gitBlobSha1':blob(hold_bytes),'gitSha256':sha(hold_bytes),'gitBytes':len(hold_bytes),'use':'GPT Director hold receipt identifying the single correction.'})
W=PKG/'DF218_B02_WITNESS_482_REPACK02_TESTONLY.json'; W.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
events=replay['eventTransitions']; trace={'id':'DF218-B02-EVENT-TRACE-482-REPACK02','witnessPath':WITNESS_PATH,'witnessSha256':sha(W.read_bytes()),'correctedFrom':new['correctedFrom'],'events':[{'eventId':e['eventId'],'timeSeconds':e['timeSeconds'],'kind':e['kind'],'beforeStateId':e['beforeStateId'],'afterStateId':e['afterStateId'],'beforeStateSha256':e['beforeStateSha256'],'afterStateSha256':e['afterStateSha256'],'forwardOperationCount':len(e['forwardOperations']),'inverseOperationCount':len(e['inverseOperations'])} for e in events],'terminalStateSummary':new['terminalStateSummary'],'inverseReplayResult':replay['inverseReplayResult']}
T=PKG/'B02_EVENT_TRACE_482_REPACK02.json'; T.write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

# Start from the independently reviewed verifier, retarget its files, and add the required source assertion.
ver=gitraw(OLD_VERIFY).decode('utf-8-sig')
ver=ver.replace("DF218_B02_WITNESS_482_TESTONLY.json","DF218_B02_WITNESS_482_REPACK02_TESTONLY.json")
ver=ver.replace("B02_EVENT_TRACE_482.json","B02_EVENT_TRACE_482_REPACK02.json")
ver=ver.replace("INDEPENDENT_VALIDATION_482.json","INDEPENDENT_VALIDATION_482_REPACK02.json")
ver=ver.replace("DF218-B02-WITNESS-482-INDEPENDENT-VALIDATION","DF218-B02-WITNESS-482-REPACK02-INDEPENDENT-VALIDATION")
ver=ver.replace("CONSTRUCTED_FOR_DIRECTOR_REVIEW_NOT_SEALED","CONSTRUCTED_FOR_DIRECTOR_RECHECK_NOT_SEALED")
needle="ck('15 events and 16 snapshots',len(r['eventTransitions'])==15 and len(r['stateSnapshots'])==16)"
insert="""profile_path=next(p for p in decl if p.endswith('/ACTOR_PROFILES.json'))\nprofile=json.loads(raw(profile_path))\nck('Wizard18 Dissonance limit equals bound actor profile in all snapshots',profile['Wizard18']['DissonanceLimit']==13 and all(x['completeState']['actors']['Wizard18']['vitals']['DissonanceLimit']==profile['Wizard18']['DissonanceLimit'] for x in r['stateSnapshots']))\nhold=load(HERE/'DIRECTOR_READBACK_482_HOLD.json')\nck('focused C01 hold receipt and unchanged owner adoption',hold['findings'][0]['id']=='B02-482-C01' and hold['findings'][0]['newOwnerAdoptionRequired'] is False and w['correctedFrom']['priorWitnessSha256']=='9109d59aef0c302c83ddd63c2a601a150a60ed25beb588baa27b4616d47877d4')\nprior=json.loads(raw('docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b02_witness_482_repack01/DF218_B02_WITNESS_482_TESTONLY.json'))\nonly_c01=True\nfor old_s,new_s in zip(prior['stateTransitionReplay']['stateSnapshots'],r['stateSnapshots']):\n corrected=copy.deepcopy(new_s['completeState']); corrected['actors']['Wizard18']['vitals']['DissonanceLimit']=10\n only_c01=only_c01 and corrected==old_s['completeState']\nsame_ops=all(a['forwardOperations']==b['forwardOperations'] and a['inverseOperations']==b['inverseOperations'] for a,b in zip(prior['stateTransitionReplay']['eventTransitions'],r['eventTransitions']))\nck('C01-only state correction; all 141 forward and inverse operations unchanged',only_c01 and same_ops and sum(len(e['forwardOperations']) for e in r['eventTransitions'])==141 and sum(len(e['inverseOperations']) for e in r['eventTransitions'])==141)\n"""+needle
assert needle in ver; ver=ver.replace(needle,insert)
V=PKG/'verify_shell_b02_witness_482_repack02.py'; V.write_text(ver,encoding='utf-8',newline='\n')
README=PKG/'README_482_REPACK02.md'; README.write_text(f'''# Elemental Shell DF218-B02 witness 482 Repack02\n\nThis focused successor corrects GPT Director finding B02-482-C01 in the held Repack01 witness. Wizard18's DissonanceLimit is 13, matching the exact bound actor profile `{profile_path}` (SHA-256 `{sha(profile_raw)}`), at `/Wizard18/DissonanceLimit`, in all 16 state snapshots. The independent verifier asserts this direct source match.\n\nThe 15-event forward/inverse replay, costs, Dissonance outcome, command ledger, attack, Shell prevention, reflected damage, deadlines and all other adopted branch premises remain unchanged. The exact owner adoption of Proposal477 Repack01 remains in force; no new owner adoption is required. This successor is unsealed and awaits focused Director C01 recheck. No identity, B01, canon, queue, campaign or runtime state changes are claimed.\n''',encoding='utf-8',newline='\n')
BUILDER=PKG/'build_shell_b02_witness_482_repack02.py'; BUILDER.write_bytes(Path(__file__).read_bytes())
subprocess.check_call(['python',str(V)],cwd=ROOT)
R=PKG/'INDEPENDENT_VALIDATION_482_REPACK02.json'
prior=PKG/'PRIOR_WITNESS_482_REPACK01.json'
files=[W,T,V,R,README,BUILDER,PKG/'DIRECTOR_READBACK_482_HOLD.json',prior]
manifest={'id':'DF218-B02-WITNESS-482-REPACK02-MANIFEST','status':'FOCUSED_C01_RECHECK_PACKET_NOT_SEALED','correctedFrom':new['correctedFrom'],'ownerAdoptionPath':ADOPT,'ownerAdoptionSha256':sha(gitraw(ADOPT)),'proposalPath':PRE,'proposalSha256':sha(gitraw(PRE)),'files':[{'path':str(x.relative_to(ROOT)).replace('\\','/'),'bytes':x.stat().st_size,'sha256':sha(x.read_bytes())} for x in files]}
M=PKG/'MANIFEST_482_REPACK02.json'; M.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
Z=PKG/'DD_ElementalShell_B02_Witness_482_REPACK02_TESTONLY.zip'
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for x in files+[M,ROOT/ADOPT]: z.write(x,arcname=str(x.relative_to(ROOT)).replace('\\','/'))
delivery={'id':'DF218-B02-WITNESS-482-REPACK02-DELIVERY','status':'READY_FOR_DIRECTOR_C01_RECHECK_NOT_SEALED','branchId':new['branchId'],'proposalSha256':new['sourceProposal']['sha256'],'adoptionPath':ADOPT,'adoptionSha256':sha(gitraw(ADOPT)),'priorHeldWitnessPath':OLD_WITNESS,'priorHeldWitnessSha256':old_hash,'directorHoldPath':HOLD_PATH,'directorHoldSha256':sha(hold_bytes),'witnessPath':WITNESS_PATH,'witnessSha256':sha(W.read_bytes()),'validationPath':f'{BASE}/elemental_shell_b02_witness_482_repack02/INDEPENDENT_VALIDATION_482_REPACK02.json','validationStatus':load(R.read_bytes())['status'],'validationChecksPassed':load(R.read_bytes())['checksPassed'],'manifestPath':f'{BASE}/elemental_shell_b02_witness_482_repack02/MANIFEST_482_REPACK02.json','manifestSha256':sha(M.read_bytes()),'zipPath':f'{BASE}/elemental_shell_b02_witness_482_repack02/DD_ElementalShell_B02_Witness_482_REPACK02_TESTONLY.zip','zipSha256':sha(Z.read_bytes()),'DissonanceLimit':{'actor':'Wizard18','profilePath':profile_path,'profileSha256':sha(profile_raw),'profilePointer':'/Wizard18/DissonanceLimit','value':13,'allSnapshotsMatch':True},'decisionBoundary':new['decisionBoundary']}
D=PKG/'DELIVERY_482_REPACK02.json'; D.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'witnessSha256':sha(W.read_bytes()),'checksPassed':load(R.read_bytes())['checksPassed'],'validationStatus':load(R.read_bytes())['status'],'zipSha256':sha(Z.read_bytes()),'deliverySha256':sha(D.read_bytes()),'profileDissonanceLimit':limit},indent=2))
