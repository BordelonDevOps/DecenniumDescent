from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
D=Path(__file__).parent;A=D.parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=D/'DD_Magic7_Corrected_Return02_129.zip';proof=D/'PART6_RETURN02_CORRECTIONS_SENT_129.png';assert p.is_file() and proof.is_file()
r={'id':'MAGIC7-RETURN02-INDEPENDENT-REVIEW-129','status':'FOCUSED_CORRECTIONS_SENT_UI_AND_THREAD_VERIFIED','receivedArchive':{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'receivedDirectory':str(D/'magic7_return02_received'),'independentDataChecks':read(D/'MAGIC7_INDEPENDENT_DATA_AUDIT_129.json'),'findings':['One normal Action off-turn: TU4-09-B:13','Known-false Clone branch starts after actual image expiry','Protective Mutations allowance stored on aura owner instead of per ally; genuine second-hit branch missing; Guardian Tissue round use not recorded'],'request':str(D/'MAGIC7_RETURN02_FOCUSED_CORRECTIONS_129.txt'),'requestId':'fc20fe27-8995-4d43-b158-35c52b299cc9','directorThreadId':'6adc506d-8770-83ea-b64c-0345d9b9b682','proof':str(proof),'newAccepted':0,'newApplied':0,'recordedAtUtc':datetime.now(timezone.utc).isoformat()}
write(D/'MAGIC7_RETURN02_REVIEW_RECEIPT_129.json',r)
h=read(D/'CURRENT_HANDOFF_129.json');h['director']['activeRequest']=r['requestId'];h['director']['activeRequestStatus']=r['status'];h['director']['scope']='Magic7 Return03 focused corrections to three case issues after actual Return02 received and independently audited.';h['directorConnectionStatus']='Actual Return02 downloaded and inspected; 7482 data checks pass. Await exact Return03 correcting off-turn Dispel, expired-image branch, and per-ally Wardborn allowance/Guardian history. No Magic7 acceptance or application yet.';h['magic7Return02Review']=r;h['lastUpdatedAtUtc']=r['recordedAtUtc'];write(D/'CURRENT_HANDOFF_129.json',h)
cp=A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_129.json';c=read(cp);c['magic7Return02Review']=r;c['lastUpdatedAtUtc']=r['recordedAtUtc'];write(cp,c)
print(r['status'])
