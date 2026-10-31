from __future__ import annotations
import hashlib,json,zlib,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/"docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT=AUDIT/"rank9_projectionconfinement2_packet288_history_correction"
RET=AUDIT/"rank9_projectionconfinement2_return232_received"
TARGETS=["astral-projection","imprisonment"]
AUTH={"reviewedApplied":816,"pending":32,"acceptedUnapplied":0,"completeStandaloneProcedures":540,"scopedInterfaces":173}
BLOCKERS={"astral-projection":["PC232-B01"],"imprisonment":["PC232-B02"]}
def digest(b):return (len(b),hashlib.sha256(b).hexdigest(),f"{zlib.crc32(b)&0xffffffff:08x}")
def read(p):return json.loads(p.read_text(encoding="utf-8-sig"))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode()
def relinfo(p):
 b=p.read_bytes();return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"crc32":f"{zlib.crc32(b)&0xffffffff:08x}"}
def main():
 now=datetime.now(timezone.utc).isoformat()
 archive=RET/"DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip"; delivery=RET/"DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json"
 prior_audit=AUDIT/"RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json"; prior_receipt=AUDIT/"RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json"; prior_submission=AUDIT/"RANK9PROJECTIONCONFINEMENT2_PACKET_232_SUBMISSION.json"
 packet_delivery=read(AUDIT/"rank9_projectionconfinement2_current_source_288_prepared/DD_Rank9_ProjectionConfinement2_CurrentSource_288_DELIVERY.json")
 current_index=read(ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json")
 queue=read(AUDIT/"CURRENT_SPELL_QUEUE_288.json"); handoff=read(AUDIT/"CURRENT_HANDOFF_288.json"); pending=read(AUDIT/"CURRENT32_PENDING_IDENTITY_AUDIT_288.json")
 old_delivery=read(delivery); old_report=read(prior_audit); old_receipt=read(prior_receipt)
 assert old_report["status"]==old_receipt["status"]=="PASS" and old_report["checkCount"]==35 and old_report["failedChecks"]==0
 assert old_delivery["heldIds"]==TARGETS and old_delivery["acceptedIds"]==old_delivery["appliedIds"]==[] and old_delivery["authority"]["reviewedApplied"]==811 and old_delivery["authority"]["pending"]==37
 decisions={x["id"]:x for x in old_delivery["decisions"]}
 assert set(decisions)==set(TARGETS) and {k:v["blockerIds"] for k,v in decisions.items()}==BLOCKERS
 assert queue["currentAuthority"]==handoff["currentAuthority"]==pending["authority"]==AUTH and set(TARGETS)<=set(pending["pendingIds"])
 entries={x["id"]:x for x in current_index["entries"]}
 assert current_index["authoredCounts"]=={"reviewed":816,"pending":32} and all(entries[x]["authoredStatus"]=="pending-authored-procedure" for x in TARGETS)
 original_request=(OUT.parent/"rank9_projectionconfinement2_current_source_288_prepared/REQUEST_288.txt").read_text(encoding="utf-8")
 assert "there is no prior director ruling" in original_request
 correction={"id":"RANK9PROJECTIONCONFINEMENT2-PACKET288-HISTORY-CORRECTION","recordedAtUtc":now,"corrects":"Packet288 source request/context statement that no prior Director ruling existed for astral-projection and imprisonment.","supersedesOnlyThatStatement":True,"historicalDecision":{"return":232,"group":"rank9-projection-confinement2","authority":old_delivery["authority"],"acceptedIds":[],"appliedIds":[],"heldIds":TARGETS,"blockerIds":BLOCKERS,"qualificationIds":old_delivery["qualifications"],"archive":relinfo(archive),"delivery":relinfo(delivery),"independentAudit":relinfo(prior_audit),"auditReceipt":relinfo(prior_receipt),"auditStatus":"PASS","auditChecks":35,"failedChecks":0,"nextPendingGroup":old_delivery["nextPendingGroup"]},"currentStatus":{"authority":AUTH,"pendingIds":pending["pendingIds"],"bothTargetsRemainPending":True,"currentPacket288SHA256":packet_delivery["archive"]["sha256"]},"correctedDirectorInstruction":"Treat Return232 as the prior explicit HOLD (astral-projection/PC232-B01; imprisonment/PC232-B02) and reassess only against Packet288 current source at 816/32/0. Do not describe the identities as never reviewed. Preserve Return232's seven qualifications and all Return284–287 decisions. This correction does not change scope, current authority, source bytes, or authorize any application.","originalPacket288RequestSHA256":hashlib.sha256((OUT.parent/"rank9_projectionconfinement2_current_source_288_prepared/REQUEST_288.txt").read_bytes()).hexdigest(),"canonicalChanges":False,"applicationChanges":False}
 corrected_request=("Correction to Packet288 history: Return232 previously reviewed these same two spells at 811/37/0 and held astral-projection under PC232-B01 and imprisonment under PC232-B02 (seven qualifications; Return232 independent audit PASS 35/35). They remain pending at current 816/32/0. Reassess current source only, preserve the prior hold as history, and do not call these identities never reviewed. All other Packet288 scope and instructions remain unchanged.\n")
 files={"HISTORY_CORRECTION.json":enc(correction),"REQUEST_288_HISTORY_CORRECTED.txt":corrected_request.encode(),"evidence/RETURN232.zip":archive.read_bytes(),"evidence/RETURN232_DELIVERY.json":delivery.read_bytes(),"evidence/RETURN232_INDEPENDENT_AUDIT.json":prior_audit.read_bytes(),"evidence/RETURN232_RECEIPT.json":prior_receipt.read_bytes(),"evidence/PACKET232_SUBMISSION.json":prior_submission.read_bytes(),"current/CURRENT_SPELL_QUEUE_288.json":(AUDIT/"CURRENT_SPELL_QUEUE_288.json").read_bytes(),"current/CURRENT_HANDOFF_288.json":(AUDIT/"CURRENT_HANDOFF_288.json").read_bytes(),"current/CURRENT32_PENDING_IDENTITY_AUDIT_288.json":(AUDIT/"CURRENT32_PENDING_IDENTITY_AUDIT_288.json").read_bytes()}
 OUT.mkdir(parents=True,exist_ok=True); arc=OUT/"DD_Rank9_ProjectionConfinement2_Packet288_HistoryCorrection.zip"; manifest=[]
 with zipfile.ZipFile(arc,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,b in sorted(files.items()):
   z.writestr(name,b); size,sha,crc=digest(b); manifest.append({"path":name,"bytes":size,"sha256":sha,"crc32":crc})
  z.writestr("MANIFEST.json",enc({"id":"PACKET288-HISTORY-CORRECTION-MANIFEST","members":manifest,"memberCountExcludingSelf":len(manifest)}))
 with zipfile.ZipFile(arc) as z: assert z.testzip() is None and len(z.namelist())==len(manifest)+1
 arcinfo=relinfo(arc); menifestinfo=relinfo(OUT/"MANIFEST.json") if (OUT/"MANIFEST.json").exists() else None
 deldoc={"id":"RANK9PROJECTIONCONFINEMENT2-PACKET288-HISTORY-CORRECTION-DELIVERY","status":"PREPARED_UNAUDITED","archive":arcinfo,"memberCount":len(manifest)+1,"payloadCount":len(manifest),"members":manifest,"correctsReturnHistory":232,"currentAuthority":AUTH,"canonicalChanges":False,"applicationChanges":False}
 dp=OUT/"DD_Rank9_ProjectionConfinement2_Packet288_HistoryCorrection_DELIVERY.json"; dp.write_bytes(enc(deldoc))
 (OUT/"HISTORY_CORRECTION.json").write_bytes(files["HISTORY_CORRECTION.json"]); (OUT/"REQUEST_288_HISTORY_CORRECTED.txt").write_bytes(files["REQUEST_288_HISTORY_CORRECTED.txt"])
 print(json.dumps({"archive":arcinfo,"delivery":relinfo(dp),"members":len(manifest)+1,"return232":relinfo(archive),"return232Audit":relinfo(prior_audit),"blockers":BLOCKERS},indent=2))
if __name__=="__main__":main()
