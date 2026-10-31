from __future__ import annotations
import copy, hashlib, json, pathlib, zlib
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parents[5]
AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_fate_rewrite_current_source_320_prepared'

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def crc(b:bytes)->str:return f'{zlib.crc32(b)&0xffffffff:08x}'
def pretty(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p:pathlib.Path):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def read(p):return json.loads(p.read_text(encoding='utf-8'))

base=AUDIT
qprev=read(base/'CURRENT_SPELL_QUEUE_319.json')
hprev=read(base/'CURRENT_HANDOFF_319.json')
pprev=read(base/'CURRENT25_PENDING_IDENTITY_AUDIT_319.json')
packet=OUT/'DD_Rank9_FateRewrite_CurrentSource_320.zip'
delivery=read(OUT/'DD_Rank9_FateRewrite_CurrentSource_320_DELIVERY.json')
audit=read(base/'FATE_REWRITE_PACKET_320_INDEPENDENT_AUDIT.json')
request=(OUT/'FATE_REWRITE_DIRECTOR_REQUEST_320.md').read_text(encoding='utf-8')
message='Director: Packet320 is attached. Please adjudicate only Fate Rewrite / TF192-B04. The packet includes the 17 preserved cases, current authority and source comparison, linked Eternal Prophecy evidence, and FR-EP-WITNESS-CONSTRUCTION-01. The existing prophecy-conflict case starts with no obligation, records zero payment, and rejects before payment; Eternal Prophecy TF192-GUARANTEE-01 still lacks closure for all-routes-prevented and unavailable item/destination branches. I found no source-complete paid/fulfilled guarantee. Confirm whether any authorized source closes TF192-B02; otherwise seal Fate Rewrite held at B04, retain H-HISTORY/DEATH, and tell me whether to proceed to Collapse Timeline while the dependency remains. No acceptance or application is requested.'
now=datetime.now(timezone.utc).isoformat(timespec='seconds')
receipt={'id':'FATE-REWRITE-PACKET-320-SUBMISSION-RECEIPT','recordedAtUtc':now,'destination':'ChatGPT Director conversation: Calibration review part 6','submissionMethod':'User-authorized browser upload and message','status':'SENT_DIRECTOR_RESPONSE_PENDING',
 'scopeIds':['fate-rewrite'],'linkedContextIds':['eternal-prophecy'],'blockerIds':['TF192-B04','TF192-B02'],'attachment':bind(packet),'delivery':bind(OUT/'DD_Rank9_FateRewrite_CurrentSource_320_DELIVERY.json'),
 'independentAudit':bind(base/'FATE_REWRITE_PACKET_320_INDEPENDENT_AUDIT.json'),'auditStatus':audit['status'],'auditChecks':{'passed':audit['passedChecks'],'failed':audit['failedChecks']},'message':message,'messageSha256':sha(message.encode()),
 'authority':qprev['currentAuthority'],'acceptedIds':[],'appliedIds':[],'heldIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
receipt_path=base/'FATE_REWRITE_PACKET_320_SUBMISSION_RECEIPT.json';receipt_path.write_bytes(pretty(receipt))

q=copy.deepcopy(qprev); q['id']='SPELL-REVIEW-QUEUE-320';q['recordedAtUtc']=now;q['supersedesQueue']='SPELL-REVIEW-QUEUE-319'
q['activeReview']={'spellId':'fate-rewrite','blockerIds':['TF192-B04','TF192-B02'],'packet':delivery['archive'],'status':'PACKET320_SUBMITTED_TO_DIRECTOR_RESPONSE_PENDING'}
q['currentSourcePacket']=delivery['archive'];q['currentPreparation']={'path':(OUT/'DD_Rank9_FateRewrite_CurrentSource_320_DELIVERY.json').relative_to(ROOT).as_posix(),**bind(OUT/'DD_Rank9_FateRewrite_CurrentSource_320_DELIVERY.json')}
q['currentPacket']={'archive':delivery['archive'],'delivery':delivery['archive'],'independentAudit':delivery['independentAudit'],'sourceComparison':delivery['sourceComparison']}
q['currentSubmission']=bind(receipt_path);q['submissionReceipt']=bind(receipt_path);q['directorConnectionStatus']='Packet320 for Fate Rewrite / TF192-B04 sent to Director; response pending. FR-EP-WITNESS-CONSTRUCTION-01 is limited to evidence preparation and does not supply TF192-B02 guarantee mechanism.'
q['currentPacketStatus']='PACKET320_SUBMITTED_DIRECTOR_RESPONSE_PENDING';q['canonicalFilesChanged']=False;q['applicationPerformed']=False;q['githubChanges']=False
q['acceptedThisStep']=[];q['appliedThisStep']=[];q['closureTasksRemaining']=25;q['firstReviewTasksRemaining']=0
q['currentDirectorInstruction']={'path':(base/'FATE_REWRITE_DIRECTOR_STATUS_320.json').relative_to(ROOT).as_posix(),'authorizationId':'FR-EP-WITNESS-CONSTRUCTION-01','mechanismSupplied':False}
q_path=base/'CURRENT_SPELL_QUEUE_320.json';q_path.write_bytes(pretty(q))

p=copy.deepcopy(pprev);p['id']='SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-320';p['recordedAtUtc']=now;p['supersedes']='CURRENT25_PENDING_IDENTITY_AUDIT_319.json'
p['status']='PASS_CURRENT_823_25_FATE_REWRITE_PACKET320_SUBMITTED';p['sourceQueue']=q_path.relative_to(ROOT).as_posix();p['currentQueueBinding']=bind(q_path)
p['closureTasksRemaining']=25;p['firstReviewTasksRemaining']=0;p['nextGroup']='rank9-time-fate6';p['nextPendingIds']=q['nextPendingIds'];p['nextPendingCount']=q['nextPendingCount'];p['nextStep']='Await Director disposition on Fate Rewrite / TF192-B04; preserve TF192-B02, then proceed per sealed next-identity instruction.'
p['currentPacketSubmission']=bind(receipt_path);p['acceptedIds']=[];p['appliedIds']=[];p['canonicalFilesChanged']=False;p['heldThisStep']=['time-stop'];p['fateRewriteSubmissionStatus']='DIRECTOR_RESPONSE_PENDING'
p_path=base/'CURRENT25_PENDING_IDENTITY_AUDIT_320.json';p_path.write_bytes(pretty(p))

h=copy.deepcopy(hprev);h['id']='SPELL-REVIEW-HANDOFF-320';h['recordedAtUtc']=now;h['supersedes']='CURRENT-HANDOFF-319';h['status']='PACKET320_FATE_REWRITE_SUBMITTED_AWAITING_DIRECTOR'
h['scopeIds']=['fate-rewrite'];h['blockerIds']=['TF192-B04','TF192-B02'];h['queue']=q_path.relative_to(ROOT).as_posix();h['queueBinding']=bind(q_path);h['pendingIdentityAudit']=p_path.relative_to(ROOT).as_posix();h['pendingIdentityAuditBinding']=bind(p_path)
h['acceptedThisStep']=[];h['appliedThisStep']=[];h['heldThisStep']=['time-stop'];h['currentBlocker']='TF192-B04';h['nextPendingGroup']=['fate-rewrite','collapse-timeline','eternal-prophecy']
h['nextStep']='Check Director reply to Packet320. If held, retain TF192-B04/TF192-B02 and follow the sealed direction on proceeding to Collapse Timeline.'
h['currentSubmission']=bind(receipt_path);h['currentPacketStatus']='PACKET320_SUBMITTED_DIRECTOR_RESPONSE_PENDING';h['closureTasksRemaining']=25;h['firstReviewTasksRemaining']=0;h['canonicalFilesChanged']=False;h['runtimeExecuted']=False
h_path=base/'CURRENT_HANDOFF_320.json';h_path.write_bytes(pretty(h))

snapshot=f'''# Current spell review snapshot — queue 320\n\n- Authority: **823 applied / 25 pending / 0 accepted-unapplied**; 547 complete standalone procedures and 173 scoped interfaces.\n- Fate Rewrite / TF192-B04 is the active review. Packet320 was uploaded to GPT Director for adjudication; response pending.\n- Linked dependency: Eternal Prophecy / TF192-B02 remains open. Director authorized FR-EP-WITNESS-CONSTRUCTION-01 for interface evidence preparation only; no guarantee mechanism or source qualification was authorized.\n- Key evidence gap: the existing prophecy-creation-conflict case has no initial obligation, pays 0 RP, and refuses pre-payment. It is not a completed guarantee witness.\n- Packet320 contains 17 preserved Fate Rewrite cases, 14 linked Eternal Prophecy cases, current rows, 140-source comparison (139 unchanged, only authored index changed), both blocker records, relevant questions/obligations, and Director status. Independent audit: **12/12 PASS**.\n- No spell accepted/applied; no canonical changes or runtime execution. 25 closure tasks remain; 0 first-review tasks. Time Stop remains held at TF192-B01.\n- Next action: read Director’s response and follow sealed guidance on Fate Rewrite and whether to proceed to Collapse Timeline.\n'''
snapshot_path=base/'CURRENT_SPELL_REVIEW_SNAPSHOT_320.md';snapshot_path.write_text(snapshot,encoding='utf-8',newline='\n')
print(json.dumps({'status':'PASS','receipt':bind(receipt_path),'queue':bind(q_path),'handoff':bind(h_path),'pendingAudit':bind(p_path),'snapshot':bind(snapshot_path),'authority':q['currentAuthority'],'next':q['next'],'closureTasks':q['closureTasksRemaining']},ensure_ascii=False))
