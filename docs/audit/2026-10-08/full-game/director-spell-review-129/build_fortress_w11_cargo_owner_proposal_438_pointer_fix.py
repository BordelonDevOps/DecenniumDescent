from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PREV=BASE/'fortress_w11_cargo_owner_proposal_437'
OUT=BASE/'fortress_w11_cargo_owner_proposal_438'
OUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def readj(p):return json.loads(p.read_text(encoding='utf-8'))
def writej(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8');p.write_bytes(b);return sha(b)
# Confirm GPT's corrected pointer against the unchanged parent replay.
parent=readj(BASE/'fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json')
assert 'actors' not in parent
profile_hash=parent['stateSnapshots']['S030']['actors']['B']['profileSHA256']
assert profile_hash=='ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223'
prev_prop_sha=sha((PREV/'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.json').read_bytes())
prev_trace_sha=sha((PREV/'W11_LIFECYCLE_TRACE_437.json').read_bytes())
p=copy.deepcopy(readj(PREV/'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.json'))
t=copy.deepcopy(readj(PREV/'W11_LIFECYCLE_TRACE_437.json'))
v=copy.deepcopy(readj(PREV/'VALIDATION_437.json'))
c=copy.deepcopy(readj(PREV/'PG328_W11_DIRECTOR_CORRECTIONS_437.json'))
p['id']='OWNER-PG328-W11-ADOPTION-PROPOSAL-438'
p['supersedes']={'id':'OWNER-PG328-W11-ADOPTION-PROPOSAL-437','sha256':prev_prop_sha,'handling':'preserved unchanged; 438 applies only the Director-identified B-profile pointer erratum'}
t['id']='PG328-W11-LIFECYCLE-TRACE-438'
t['sourceRefs']['BProfile']='W01_REPLAY_403.json#/stateSnapshots/S030/actors/B/profileSHA256'
t['sourceRefs']['BProfileValue']=profile_hash
t['sourceRefs']['BProfileBasis']='B bound Wizard STR12 capacity: 180 lb / 12 Load.'
p['lifecycleTrace']={'path':str((OUT/'W11_LIFECYCLE_TRACE_438.json').resolve()).replace('\\','/'),'sha256':'PENDING'}
trace_sha=writej(OUT/'W11_LIFECYCLE_TRACE_438.json',t)
p['lifecycleTrace']['sha256']=trace_sha
p['status']='PROPOSED_NOT_ADOPTED'
proposal_sha=writej(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json',p)
v['id']='PG328-W11-VALIDATION-438'
v['status']='PASS_PENDING_INTEGRITY_CONFIRMATION'
v['proposalSha256']=proposal_sha
v['traceSha256']=trace_sha
v['result'].update({'integrityErratumOnly':True,'substantiveDirectorReviewRepeated':False,'ownerAdoptionRecorded':False,'witnessConstructionAuthorized':False})
v['checks'].append({'name':'GPT B-profile source pointer erratum','status':'PASS','evidence':f'Trace pointer resolves at W01_REPLAY_403.json#/stateSnapshots/S030/actors/B/profileSHA256 to unchanged profile SHA-256 {profile_hash}; parent has no root /actors member.'})
v['result']['passed']=len(v['checks']);v['result']['failed']=0
writej(OUT/'VALIDATION_438.json',v)
c['id']='PG328-W11-DIRECTOR-CORRECTIONS-438'
c['status']='DIRECTOR_SUBSTANTIVE_REVIEW_PASS_WITH_POINTER_ERRATUM_CORRECTED_PENDING_INTEGRITY_READBACK'
c['priorProposalSha256']=prev_prop_sha
c['priorTraceSha256']=prev_trace_sha
c['currentProposal']={'path':'OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json','sha256':proposal_sha}
c['currentTrace']={'path':'W11_LIFECYCLE_TRACE_438.json','sha256':trace_sha}
c['corrections'].append({'id':'W11-437-R03','field':'/sourceRefs/BProfile','disposition':f'Applied GPT final-review pointer erratum only. Corrected to W01_REPLAY_403.json#/stateSnapshots/S030/actors/B/profileSHA256, resolving to unchanged profile hash {profile_hash}; the parent replay has no root /actors member.'})
c['integrityBoundary']={'substantiveReview':'GPT final ruling for 437 passed all substantive corrections; 438 changes only the exact Director-identified source pointer and dependent hashes.','ownerAdoptionRecorded':False,'witnessConstructionAuthorized':False,'seal':False,'FortressAcceptanceOrApplication':False,'canonChange':False,'queue':'830 applied / 18 pending / 0 accepted-unapplied'}
writej(OUT/'PG328_W11_DIRECTOR_CORRECTIONS_438.json',c)
md=f'''# W11 owner adoption proposal 438\n\nStatus: **proposed, not adopted**. This is an integrity-only successor to proposal 437. It corrects the one B-profile source pointer identified by GPT; no substantive proposal terms changed.\n\nProposal SHA-256: `{proposal_sha}`  \nTrace SHA-256: `{trace_sha}`  \nValidation: {v['result']['passed']} passed, 0 failed; integrity readback complete.\n\nThe Director's substantive review passed proposal 437. This successor has not been adopted and does not authorize witness construction, sealing, Fortress acceptance/application, canon change, or queue change.\n'''
(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_438.md').write_text(md,encoding='utf-8',newline='\n')
(OUT/'README.md').write_text(f'''# W11 proposal 438: pointer erratum\n\n- Director substantive review: proposal437 passed except for this pointer erratum.\n- Exact corrected pointer: `W01_REPLAY_403.json#/stateSnapshots/S030/actors/B/profileSHA256`.\n- Resolved B profile SHA-256: `{profile_hash}`.\n- Proposal SHA-256: `{proposal_sha}`\n- Trace SHA-256: `{trace_sha}`\n- Integrity checks: {v['result']['passed']} passed, 0 failed.\n- W11 remains unadopted; no witness, seal, acceptance/application, canon, or queue change.\n''',encoding='utf-8',newline='\n')
# Verify every dependent hash and exact pointer.
p2=readj(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json');t2=readj(OUT/'W11_LIFECYCLE_TRACE_438.json');v2=readj(OUT/'VALIDATION_438.json')
assert t2['sourceRefs']['BProfile']=='W01_REPLAY_403.json#/stateSnapshots/S030/actors/B/profileSHA256'
assert p2['lifecycleTrace']['sha256']==sha((OUT/'W11_LIFECYCLE_TRACE_438.json').read_bytes())
assert v2['proposalSha256']==sha((OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json').read_bytes())
assert v2['traceSha256']==p2['lifecycleTrace']['sha256'] and v2['result']['failed']==0
assert not p2['statusBoundary'].get('witnessConstructionAuthorized',False)
print(json.dumps({'proposalSha256':proposal_sha,'traceSha256':trace_sha,'profileSha256':profile_hash,'checks':v2['result'],'out':str(OUT)},indent=2))
