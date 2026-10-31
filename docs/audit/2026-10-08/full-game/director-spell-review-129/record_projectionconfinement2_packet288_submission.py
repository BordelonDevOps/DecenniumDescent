from __future__ import annotations
import hashlib,json,zlib
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/"docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP="rank9-projection-confinement2"
TARGETS=["astral-projection","imprisonment"]
CHAT="https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
def read(name): return json.loads((AUDIT/name).read_text(encoding="utf-8-sig"))
def write(name,x): (AUDIT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def info(path):
 p=Path(path); raw=p.read_bytes(); return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"crc32":f"{zlib.crc32(raw)&0xffffffff:08x}"}
def main():
 now=datetime.now(timezone.utc).isoformat()
 packet=read("RANK9PROJECTIONCONFINEMENT2_PACKET_288.json")
 audit=read("RANK9PROJECTIONCONFINEMENT2_PACKET_288_INDEPENDENT_AUDIT.json")
 receipt=read("RANK9PROJECTIONCONFINEMENT2_PACKET_288_RECEIPT.json")
 prep=read("RANK9PROJECTIONCONFINEMENT2_SOURCE_PREPARATION_288.json")
 assert audit["status"]==receipt["status"]=="PASS" and audit["checkCount"]==15 and audit["failedChecks"]==0
 base=AUDIT/"rank9_projectionconfinement2_current_source_288_prepared"
 names=["DD_Rank9_ProjectionConfinement2_CurrentSource_288.zip","DD_Rank9_ProjectionConfinement2_CurrentSource_288_DELIVERY.json","CURRENT_SOURCE_CONFERENCE_CANDIDATE_288.json","CURRENT_CONTEXT_288.json","REQUEST_288.txt"]
 attached=[info(base/n) for n in names]
 attached += [info(AUDIT/n) for n in ["CURRENT_SPELL_QUEUE_288.json","CURRENT_HANDOFF_288.json","CURRENT32_PENDING_IDENTITY_AUDIT_288.json","CURRENT_SPELL_REVIEW_SNAPSHOT_288.md","RANK9PROJECTIONCONFINEMENT2_SOURCE_PREPARATION_288.json","RANK9PROJECTIONCONFINEMENT2_PACKET_288.json","RANK9PROJECTIONCONFINEMENT2_PACKET_288_INDEPENDENT_AUDIT.json","RANK9PROJECTIONCONFINEMENT2_PACKET_288_RECEIPT.json"]]
 assert len(attached)==13 and attached[0]==packet["archive"]
 submission={"id":"RANK9PROJECTIONCONFINEMENT2-PACKET-288-SUBMISSION","recordedAtUtc":now,"status":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","group":GROUP,"targetIds":TARGETS,"authority":packet["sourceAuthority"],"archive":packet["archive"],"deliveryManifest":packet["deliveryManifest"],"independentAudit":info(AUDIT/"RANK9PROJECTIONCONFINEMENT2_PACKET_288_INDEPENDENT_AUDIT.json"),"auditReceipt":info(AUDIT/"RANK9PROJECTIONCONFINEMENT2_PACKET_288_RECEIPT.json"),"attachments":attached,"attachmentCount":len(attached),"conversation":CHAT,"submittedThrough":"Chrome ChatGPT conversation UI","directorRequest":"Review only astral-projection and imprisonment; confirm access, provide progress updates, seal Return288 and identify exact next group.","acceptedIds":[],"appliedIds":[],"canonicalChanges":False,"githubChanges":False}
 submission_path=AUDIT/"RANK9PROJECTIONCONFINEMENT2_PACKET_288_SUBMISSION.json"
 submission_path.write_text(json.dumps(submission,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 record=read("RANK9PROJECTIONCONFINEMENT2_PACKET_288.json"); record.update({"status":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","submittedAtUtc":now,"submission":info(submission_path),"acceptedIds":[],"appliedIds":[],"canonicalChanges":False}); write("RANK9PROJECTIONCONFINEMENT2_PACKET_288.json",record)
 queue=read("CURRENT_SPELL_QUEUE_288.json"); request=queue["nextPreparedRequest"]; request.update({"status":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","submission":info(submission_path),"submittedAtUtc":now}); queue.update({"status":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","packetStatus":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","currentSubmission":info(submission_path),"submittedAtUtc":now,"githubChanges":False,"nextPreparedRequest":request}); write("CURRENT_SPELL_QUEUE_288.json",queue)
 handoff=read("CURRENT_HANDOFF_288.json"); handoff.update({"status":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","currentSubmission":info(submission_path),"submittedAtUtc":now,"nextPreparedRequest":request,"resumePriority":"Packet288 sent to GPT; keep reading the browser and ping for concrete progress and remaining witnesses, then independently audit Return288 before any application."}); handoff["queue"]=info(AUDIT/"CURRENT_SPELL_QUEUE_288.json"); handoff["queueBinding"]=handoff["queue"]; handoff["currentQueueBinding"]=handoff["queue"]; write("CURRENT_HANDOFF_288.json",handoff)
 pending=read("CURRENT32_PENDING_IDENTITY_AUDIT_288.json"); pending.update({"status":"PACKET288_SUBMITTED_GPT_PENDING_816_32_0","currentSubmission":info(submission_path)}); write("CURRENT32_PENDING_IDENTITY_AUDIT_288.json",pending)
 snapshot=AUDIT/"CURRENT_SPELL_REVIEW_SNAPSHOT_288.md"; text=snapshot.read_text(encoding="utf-8"); text=text.replace("passed its independent 15/15 audit and is ready to send","passed its independent 15/15 audit and was sent to GPT for review"); snapshot.write_text(text,encoding="utf-8")
 start=ROOT/"START_HERE.md"; lines=start.read_text(encoding="utf-8-sig").splitlines(); lines[0]="**Current ordinary spell-review handoff [288](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_288.json):** Packet288 passed independent audit (15/15) and was sent to GPT for only astral-projection and imprisonment. Authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied**; waiting for the Director’s progress and sealed Return288."
 start.write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(json.dumps({"status":submission["status"],"attachmentCount":len(attached),"zipSha256":attached[0]["sha256"],"submissionRecord":info(submission_path)},indent=2))
if __name__=="__main__": main()
