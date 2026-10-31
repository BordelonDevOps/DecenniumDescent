from __future__ import annotations
import copy, hashlib, json, zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"

def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def enc(x): return json.dumps(x, ensure_ascii=False, indent=2) + "\n"
def info(p):
    b=p.read_bytes()
    return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"crc32":f"{zlib.crc32(b)&0xffffffff:08x}"}

now=datetime.now(timezone.utc).isoformat()
prep=read(BASE/"RANK9DEATHRECOVERY7_SOURCE_PREPARATION_235.json")
audit=read(BASE/"RANK9DEATHRECOVERY7_PACKET235_INDEPENDENT_AUDIT.json")
receipt=read(BASE/"RANK9DEATHRECOVERY7_PACKET235_RECEIPT.json")
assert prep["status"]=="PREPARED_NOT_SENT" and audit["status"]==receipt["status"]=="PASS" and audit["failedChecks"]==receipt["failedChecks"]==0
archive=BASE/"rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235.zip"
delivery=BASE/"rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235_DELIVERY.json"
assert info(archive)["sha256"]==prep["archive"]["sha256"] and info(delivery)["sha256"]==prep["deliveryManifest"]["sha256"]
packet=info(archive); delivery_info=info(delivery); audit_info=info(BASE/"RANK9DEATHRECOVERY7_PACKET235_INDEPENDENT_AUDIT.json"); receipt_info=info(BASE/"RANK9DEATHRECOVERY7_PACKET235_RECEIPT.json")
submission={"id":"RANK9DEATHRECOVERY7-PACKET235-SUBMISSION","recordedAtUtc":now,"status":"PACKET235_SUBMITTED_GPT_PENDING_811_37_0","group":"rank9-death-recovery7","targetIds":["final-word"],"authority":prep["authority"],"archive":packet,"deliveryManifest":delivery_info,"independentAudit":audit_info,"auditReceipt":receipt_info,"auditStatus":"PASS","auditChecks":audit["checkCount"],"auditFailures":0,"acceptedIds":[],"appliedIds":[],"heldIds":[],"destination":"Calibration review part 6","browserVerified":True,"submittedAtUtc":now,"githubChanges":False}
submission_path=BASE/"RANK9DEATHRECOVERY7_PACKET_235_SUBMISSION.json"
submission_path.write_text(enc(submission),encoding="utf-8")

p_path=BASE/"CURRENT37_PENDING_IDENTITY_AUDIT_235.json"
p=read(p_path)
p["status"]="PACKET235_SUBMITTED_GPT_PENDING_811_37_0"
p["preparedNextGroup"].update({"status":"PACKET235_SUBMITTED_GPT_PENDING_811_37_0","packet":packet,"deliveryManifest":delivery_info,"independentAudit":audit_info,"auditReceipt":receipt_info,"submittedAtUtc":now})
p["lastSubmittedPacket"]={"group":"rank9-death-recovery7","targetIds":["final-word"],"archive":packet,"deliveryManifest":delivery_info,"independentAudit":audit_info,"receipt":receipt_info,"acceptedIds":[],"appliedIds":[]}
p_path.write_text(enc(p),encoding="utf-8")

q_path=BASE/"CURRENT_SPELL_QUEUE_235.json"
q=read(q_path)
q["recordedAtUtc"]=now
q["status"]=q["packetStatus"]="PACKET235_SUBMITTED_GPT_PENDING_811_37_0"
q["pendingIdentityAudit"]={"path":p_path.relative_to(ROOT).as_posix(),**info(p_path)}
q["currentPreparation"]=prep["candidate"]
q["currentPacket"]=packet
q["currentDeliveryManifest"]=delivery_info
q["currentPacketDelivery"]=delivery_info
q["currentPacketAudit"]=audit_info
q["currentPacketAuditReceipt"]=receipt_info
q["currentPacketAuditStatus"]="PASS"
q["currentPacketAuditChecks"]=audit["checkCount"]
q["currentPacketAuditFailures"]=0
q["sourcePreparation"]=info(BASE/"RANK9DEATHRECOVERY7_SOURCE_PREPARATION_235.json")
q["currentSubmission"]={"path":submission_path.relative_to(ROOT).as_posix(),**info(submission_path)}
q["submittedAtUtc"]=now
q["githubChanges"]=False
row=next(x for x in q["currentPendingGroups"] if x["group"]=="rank9-death-recovery7")
row["status"]="PACKET235_SUBMITTED_GPT_PENDING_811_37_0"
row["freshPacketRequiredForCurrentAuthority"]=True
q_path.write_text(enc(q),encoding="utf-8")

h_path=BASE/"CURRENT_HANDOFF_235.json"
h=read(h_path)
h["recordedAtUtc"]=now
h["status"]="PACKET235_SUBMITTED_GPT_PENDING_811_37_0"
h["pendingIdentityAudit"]={"path":p_path.relative_to(ROOT).as_posix(),**info(p_path)}
h["queue"]={"path":q_path.relative_to(ROOT).as_posix(),**info(q_path)}
h["currentQueueBinding"]={"path":q_path.relative_to(ROOT).as_posix(),**info(q_path)}
h["currentPacket"]=packet
h["currentPacketDelivery"]=delivery_info
h["currentPacketAudit"]=audit_info
h["currentPacketAuditReceipt"]=receipt_info
h["packetAuditStatus"]="PASS"
h["packetAuditChecks"]=audit["checkCount"]
h["packetAuditFailures"]=0
h["sourcePreparation"]=info(BASE/"RANK9DEATHRECOVERY7_SOURCE_PREPARATION_235.json")
h["currentSubmission"]={"path":submission_path.relative_to(ROOT).as_posix(),**info(submission_path)}
h["submittedAtUtc"]=now
h["nextStep"]="GPT review of final-word is in progress. Keep monitoring the browser and ping if needed, then independently audit the sealed return before applying only exact accepted identities."
h["resumePriority"]="Packet235 for final-word only is submitted to GPT and independently passed 19 checks. Monitor Calibration review part 6, ping if needed, and audit any sealed decision before applying exact accepted identities."
h_path.write_text(enc(h),encoding="utf-8")
print(json.dumps({"status":submission["status"],"submission":info(submission_path),"queue":info(q_path),"handoff":info(h_path),"pendingAudit":info(p_path)},ensure_ascii=False,indent=2))
