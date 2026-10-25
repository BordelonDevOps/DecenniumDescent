"""Fresh navigation and complete applied-context packaging after validated four-ID application."""
from pathlib import Path
import json,hashlib,datetime,zipfile,copy
G=Path(r'C:\Github\DecenniumDescent');D=Path(__file__).parent;A=D.parent;R=G/'DescentReviewChanges/ReviewBible';O=A/'spell-review-resume-116'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
enc=lambda x:(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
def write(p,x):p.write_bytes(enc(x))
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat();ids=['awaken','bone-cage','contagion','telekinesis'];validation=read(D/'LIFEMATTER4_APPLICATION_VALIDATION_129.json');assert validation['passed']
idx=read(R/'data/public/spell_playtests/authored_review_index.json');assert idx['authoredCounts']=={'reviewed':627,'pending':221}
ap=D/'LIFEMATTER4_EXACT_ACCEPTANCE_129.json';rp=D/'LIFEMATTER4_APPLICATION_129.json'
q=read(O/'CURRENT_SPELL_QUEUE_129.json');assert q['currentCounts']['indexPending']==225
q['currentCounts'].update({'appliedReviewed':627,'indexPending':221,'acceptedUnapplied':0,'needsAcceptance':221,'submittedAwaitingReturn':1,'otherUnaccepted':220})
q['appliedAcceptedIdentities']=sorted(set(q['appliedAcceptedIdentities'])|set(ids));q['acceptedIdentities']=ids;q['latestAcceptanceReceipts'].append(str(ap));q['latestApplicationReceipts'].append(str(rp));q['lastUpdatedAtUtc']=now
q['nextSuggestedGroups']=['life-matter5','information8','eye-judgement1','planar-travel6','rank7-perception5']
for g in q['groups']:
 if g['group']=='life-matter5':g.update({'currentPhase':'four-applied-disintegrate-focused-correction-pending-129','appliedIdentities':ids,'pendingIdentities':['disintegrate'],'applicationReceipt':str(rp),'exactAcceptanceReceipt':str(ap),'correctionRequest':str(D/'LIFEMATTER5_RETURN02_SEND_RECEIPT_129.json')})
q['director']=read(D/'CURRENT_HANDOFF_129.json')['director'];q['director']['scope']='Four LifeMatter identities applied; only Disintegrate remains pending in this conference.'
q['resumePriority']='Finish exact Disintegrate correction and apply on acceptance, then Information8/EyeJudgement1 and all221 remaining.';q['directorConnectionStatus']='ChatGPT view rate-limited; same existing Part6 backing task received correction request; no response yet visible.'
inventory=read(D/'CURRENT225_PACKET_INVENTORY_129.json');inventory['id']='CURRENT221-PACKET-INVENTORY-129';inventory['recordedAtUtc']=now;inventory['counts']=idx['authoredCounts'];inventory['priorInventory']='CURRENT225_PACKET_INVENTORY_129.json';inventory['indexSha256Unchanged']=False;inventory['currentIndexSha256']=validation['index']['sha256']
for g in inventory['groups']:
 if g['group']=='life-matter5':g['originalIdentities']=g['identities'];g['identities']=['disintegrate'];g['phase']='four-applied-disintegrate-focused-correction-pending-129'
pending={e['id'] for e in idx['entries'] if e['authoredStatus']!='reviewed-authored-operational-playtest'};listed=[sid for g in inventory['groups'] for sid in g['identities']];assert len(listed)==len(set(listed))==221 and set(listed)==pending
inventory['pendingExactlyOnce']=True;inventory['scope']='Current221 pending identities mapped once to existing verified source packets; archival bindings inherited from exact225 inventory; four now-applied LifeMatter IDs removed. Disintegrate remains pending.'
ip=D/'CURRENT221_PACKET_INVENTORY_129.json';assert not ip.exists();write(ip,inventory);q['currentPacketInventory']=str(ip);write(O/'CURRENT_SPELL_QUEUE_129.json',q)
for p in [D/'CURRENT_HANDOFF_129.json',A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_129.json']:
 v=read(p);v['currentCounts']={'reviewedApplied':627,'pending':221,'standalone':351,'scopedInterfaces':173,'acceptedUnapplied':0};v['status']='PART6_LIFEMATTER4_APPLIED_DISINTEGRATE_CORRECTION_PENDING_ALL221_REQUIRED';v['lastUpdatedAtUtc']=now;v['lifeMatter4Application129']=validation;v['next']=q['resumePriority'];v['director']=q['director'];v['currentPacketInventory']=str(ip);v['nextPacketLibraryUploads']=str(D/'INFORMATION8_EYE1_LIBRARY_UPLOAD_129.json')
 if 'resumePriority' in v:v['resumePriority']=q['resumePriority']
 if 'appliedThisTurn' in v:v['appliedThisTurn']['LifeMatter4']=ids
 if 'applicationReceipts' in v:v['applicationReceipts'].append(str(rp))
 if 'newApplied' in v:v['newApplied']=11
 write(p,v)
start=G/'START_HERE.md';old=start.read_text(encoding='utf-8-sig');marker='The checkpoint entries below preserve earlier states; checkpoint129 and the Part6 direction above control current work.';assert marker in old
prefix='# Active ordinary spell review129 — Calibration review part6\n\nAwaken, Bone Cage, Contagion and Telekinesis are independently accepted and applied from exact LifeMatter5 Return01. Current authored coverage: **627 applied /221 pending /351 standalone /173 scoped interfaces /0 accepted-unapplied**. Their8 main cases,18 branches,253 events and23 actual casts passed independent review; all121 original evidence files remain exact. Disintegrate alone remains pending focused corrections in the same Part6 task. No Disintegrate-specific shared dust rule is selected by the four-ID acceptance.\n\nContinue until all221 remaining identities are independently accepted and applied. Use Calibration review part6 (6adc506d-8770-83ea-b64c-0345d9b9b682); its confirmed backing task is01a16c9a-4007-70c7-84b3-95bedbad20e5 on durable. Correction request01a16d36-fa68-70e0-869a-515a248b4f31 is received and in progress, but no response is yet visible; do not claim returned corrections. ChatGPT view remains rate-limited. Information8 and EyeJudgement1 source packets have been uploaded to the personal Library; their next review request is still unsent. Read director-spell-review-129/CURRENT_HANDOFF_129.json, CURRENT221_PACKET_INVENTORY_129.json and spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json under docs/audit/2026-10-08/full-game. Do not reopen feats or completed spell cohorts. All content/runtime/human/balance/cosmology/release holds remain.\n\n'
start.write_text(prefix+old[old.index(marker):],encoding='utf-8')
packet=D/'DD_LifeMatter4_Applied_Context_129.zip';assert not packet.exists();payload={}
for p in [ap,rp,D/'LIFEMATTER4_APPLICATION_VALIDATION_129.json',D/'LIFEMATTER4_INDEX_OPERATIONS_129.json',D/'LIFEMATTER5_RETURN01_SEMANTIC_REVIEW_129.json',D/'LIFEMATTER5_RETURN01_CAST_SOURCE_AUDIT_129.json',D/'LIFEMATTER5_RETURN02_REQUEST_129.txt',D/'LIFEMATTER5_RETURN02_SEND_RECEIPT_129.json',R/'data/public/spell_playtests/authored_review_index.json',O/'CURRENT_SPELL_QUEUE_129.json',ip,D/'INFORMATION8_EYE1_LIBRARY_UPLOAD_129.json',R/'docs/spells/candidates/LIFEMATTER4_REVIEWED_129.md',D/'DD_LifeMatter5_Director_Return01_130.zip']:payload[p.name]=p.read_bytes()
payload['README.md']=('Current627applied/221pending/351standalone/173scoped/0accepted-unapplied. Four named LifeMatter identities applied; Disintegrate remains pending. The included exact Return01 ZIP preserves all121 evidence files; its five-ID proposal is narrowed by the independent four-ID acceptance/application scope. Current index and queue control counts; old623/225 in original return remains historical. Do not reopen the four or any closed cohorts. Finish focused Disintegrate correction, then Information8/EyeJudgement1 and all221.\n').encode()
manifest={'id':'LIFEMATTER4-APPLIED-CONTEXT-129','recordedAtUtc':now,'currentCounts':idx['authoredCounts'],'appliedIds':ids,'pendingDisintegrate':True,'files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}for n,b in payload.items()]};payload['MANIFEST.json']=enc(manifest)
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in payload.items():z.writestr(n,b)
with zipfile.ZipFile(packet) as z:
 assert z.testzip() is None
 for n,b in payload.items():assert z.read(n)==b
receipt={'id':'LIFEMATTER4-APPLIED-CONTEXT-PACKET-129','archive':bind(packet),'members':len(payload),'currentCounts':idx['authoredCounts'],'appliedIds':ids,'sent':False,'completeReturn01Preserved':True};write(D/'LIFEMATTER4_APPLIED_CONTEXT_PACKET_129.json',receipt);print(json.dumps(receipt,indent=2))
