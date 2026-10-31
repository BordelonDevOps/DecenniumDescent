from __future__ import annotations
import hashlib, json, zlib, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/"docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT=AUDIT/"rank9_impactexile4_current_source_286_prepared"
ARCHIVE=OUT/"DD_Rank9_ImpactExile4_CurrentSource_286.zip"
DELIVERY=OUT/"DD_Rank9_ImpactExile4_CurrentSource_286_DELIVERY.json"
CANDIDATE=OUT/"CURRENT_SOURCE_CONFERENCE_CANDIDATE_286.json"
PREP=AUDIT/"RANK9IMPACTEXILE4_SOURCE_PREPARATION_286.json"
REPORT=AUDIT/"RANK9IMPACTEXILE4_PACKET_286_INDEPENDENT_AUDIT.json"
RECEIPT=AUDIT/"RANK9IMPACTEXILE4_PACKET_286_RECEIPT.json"
AUTH={"reviewedApplied":816,"pending":32,"acceptedUnapplied":0,"completeStandaloneProcedures":540,"scopedInterfaces":173}
TARGETS=["reverse-gravity-field"]
CLOSED=["eternal-anvil","transmute-flesh-to-energy","planar-collapse"]

def digest_bytes(b): return (len(b),hashlib.sha256(b).hexdigest(),f"{zlib.crc32(b)&0xffffffff:08x}")
def digest_file(p):
    h,crc,size=hashlib.sha256(),0,0
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b);crc=zlib.crc32(b,crc);size+=len(b)
    return size,h.hexdigest(),f"{crc&0xffffffff:08x}"
def digest_member(z,n):
    h,crc,size=hashlib.sha256(),0,0
    with z.open(n) as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b);crc=zlib.crc32(b,crc);size+=len(b)
    return size,h.hexdigest(),f"{crc&0xffffffff:08x}"
def record(checks,name,passed,detail=None): checks.append({"check":name,"passed":bool(passed),"detail":detail})

def main():
    delivery=json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    prep=json.loads(PREP.read_text(encoding="utf-8-sig"))
    c=json.loads(CANDIDATE.read_text(encoding="utf-8-sig"))
    checks=[]
    actual=digest_file(ARCHIVE)
    record(checks,"Packet ZIP exact byte/SHA/CRC match delivery",(actual[0],actual[1],actual[2])==(delivery["archive"]["bytes"],delivery["archive"]["sha256"],delivery["archive"]["crc32"].lower()),{"archive":actual})
    record(checks,"Preparation record is PASS with all preparation checks passing",prep["status"]=="PASS" and all(x["passed"] for x in prep["checks"]),{"checks":len(prep["checks"])})
    with zipfile.ZipFile(ARCHIVE) as z:
        names=z.namelist();unsafe=[n for n in names if n.startswith(("/","\\")) or "\\" in n or PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts]
        manifest=json.loads(z.read("MANIFEST.json"));rows={x["path"]:x for x in manifest["members"]}
        # Delivery carries the archived member count and top-level source hashes; MANIFEST binds all individual members.
        record(checks,"Archive has unique safe paths, valid CRC, and exact internal manifest allowlist",
            len(names)==len(set(names))==len(rows)+1==manifest["memberCountExcludingSelf"]+1==delivery["members"]
            and set(names)-{"MANIFEST.json"}==set(rows) and not unsafe and z.testzip() is None,
            {"members":len(names),"manifestRows":len(rows),"unsafe":unsafe[:5]})
        failures=[]
        for n,row in rows.items():
            if digest_member(z,n)!=(row["bytes"],row["sha256"],row["crc32"].lower()): failures.append(n)
        record(checks,"Every internal manifest member independently matches bytes/SHA/CRC",not failures,{"checked":len(rows),"failures":failures[:8]})
        record(checks,"Packet scope, authority, closed IDs and commit match delivery",
            manifest["group"]=="rank9-impact-exile4" and manifest["pendingIds"]==TARGETS and manifest["closedAcceptedIds"]==CLOSED
            and manifest["sourceAuthority"]==AUTH and manifest["sourceCommit"]==delivery["sourceCommit"]
            and delivery["sourceAuthority"]==AUTH and delivery["pendingIds"]==TARGETS and delivery["closedAcceptedIds"]==CLOSED,
            {"scope":manifest["pendingIds"],"authority":manifest["sourceAuthority"]})
        archived_candidate=json.loads(z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_286.json"))
        context=json.loads(z.read("CURRENT_CONTEXT_286.json"))
        notes=json.loads(z.read("HISTORICAL_NOTES/RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json"))
        request=z.read("REQUEST_286.txt").decode("utf-8")
        record(checks,"Candidate/context/request in ZIP match submitted sidecars and exact target scope",
            archived_candidate==c and [x["spellId"] for x in c["records"]]==TARGETS
            and context["sourceAuthority"]==AUTH and context["targetGroup"]["pendingIds"]==TARGETS
            and "review exactly reverse-gravity-field" in request.lower()
            and "Apply no changes in this review" in request,
            {"scope":[x["spellId"] for x in c["records"]],"targetQuestions":len(c["questions"]),"futureRequirements":len(c["futureCaseRequirements"])})
        record(checks,"Original 26 questions, two focused addenda, eight cases and seven future requirements are retained",
            len(c["questions"])==26 and len(notes["focusedAdditionalQuestions"])==2 and len(notes["requiredNewCases"])==8
            and len(c["futureCaseRequirements"])==len(notes["originalFutureCaseRequirementsUnchanged"])==7
            and context["preservation"]=={"originalQuestions":26,"focusedAddenda":2,"requiredMainCases":8,"futureCaseRequirements":7},
            {"questions":len(c["questions"]),"addenda":len(notes["focusedAdditionalQuestions"]),"futureRequirements":len(c["futureCaseRequirements"])})
        rows=c["sourceBindings"];local_fail=[];zip_fail=[]
        for row in rows:
            p=ROOT/row["path"]
            if not p.is_file():
                local_fail.append(row["path"]+":missing")
                continue
            if digest_file(p)[:2]!=(row["bytes"],row["sha256"]): local_fail.append(row["path"]+":local-hash")
            m="current/"+row["path"]
            if m not in names or digest_member(z,m)[:2]!=(row["bytes"],row["sha256"]): zip_fail.append(row["path"])
        record(checks,"All refreshed source bindings independently match current files and packet copies",
            len(rows)==delivery["sourceBindings"] and not local_fail and not zip_fail,
            {"bindings":len(rows),"localFailures":local_fail[:8],"zipFailures":zip_fail[:8]})
        source=json.loads(z.read("CURRENT_CONTEXT_286.json"))
        record(checks,"Return205 accepted IDs are closed and current target blocker remains IE204-B02",
            source["priorAcceptedAppliedBatch205"]["acceptedIds"]==CLOSED and source["priorAcceptedAppliedBatch205"]["doNotReopen"] is True
            and source["priorHold"]["blockers"]==["IE204-B02"],
            {"closed":source["priorAcceptedAppliedBatch205"]["acceptedIds"],"blocker":source["priorHold"]["blockers"]})
        record(checks,"Return244 holds remain outside scope and are independently audited",
            source["return244OutsideScope"]["heldIds"]==["summon-elemental-avatar","summon-herald-of-the-planes","summon-avatar-of-decay"]
            and source["return244OutsideScope"]["audit"]["path"].endswith("RANK9SUMMONHOSTS5_RETURN244_INDEPENDENT_AUDIT.json"),
            source["return244OutsideScope"])
        record(checks,"Latest Return285 three-identity hold is audited at current authority and outside scope",
            source["return285OutsideScope"]["heldIds"]==["summon-elemental-avatar","summon-herald-of-the-planes","summon-avatar-of-decay"]
            and source["return285OutsideScope"]["authorityUnchanged"]==AUTH
            and source["return285OutsideScope"]["audit"]["path"].endswith("RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json"),
            source["return285OutsideScope"])
        prior228=source["priorReturn228SameIdentityHold"]
        record(checks,"Prior Return228 same-identity hold and IE204-B02 are explicit and outside the new adjudication",
            prior228["heldIds"]==TARGETS and prior228["blockers"]=={"reverse-gravity-field":["IE204-B02"]}
            and prior228["decision"]["path"].endswith("extracted/DIRECTOR_DECISION.json")
            and c["previousImpactReturn228Binding"]["sameIdentityPriorHold"] is True,
            {"heldIds":prior228["heldIds"],"blockers":prior228["blockers"]})
        required_recent=[]
        for n in range(238,244):
            required_recent.extend([f"evidence/RETURN{n}.zip",f"evidence/RETURN{n}_DELIVERY.json",
                f"evidence/RETURN{n}_INDEPENDENT_AUDIT.json",f"evidence/RETURN{n}_RECEIPT.json"])
        recent_missing=[n for n in required_recent if n not in names]
        record(checks,"All six active sealed hold packages Returns238–243 and their audits/receipts are carried forward",
            not recent_missing and len(required_recent)==24,
            {"requiredFiles":len(required_recent),"missing":recent_missing})
        record(checks,"Return228 and Return244 sealed archives, manifests, audits and receipts are package-bound",
            all(n in names for n in ["evidence/RETURN228.zip","evidence/RETURN228_DELIVERY.json",
                "evidence/RETURN228_DECISION.json","evidence/RETURN228_INDEPENDENT_AUDIT.json","evidence/RETURN228_RECEIPT.json",
                "evidence/RETURN244.zip","evidence/RETURN244_DELIVERY.json","evidence/RETURN244_INDEPENDENT_AUDIT.json",
                "evidence/RETURN244_RECEIPT.json"])
            and c["previousReturn244Binding"]["heldIds"]==["summon-elemental-avatar","summon-herald-of-the-planes","summon-avatar-of-decay"],
            {"Return228":prior228["heldIds"],"Return244":c["previousReturn244Binding"]["heldIds"]})
        record(checks,"Return285 archive, delivery, independent audit, receipt, and Packet285 audit are package-bound",
            all(n in names for n in ["evidence/RETURN285.zip","evidence/RETURN285_DELIVERY.json",
                "evidence/RETURN285_INDEPENDENT_AUDIT.json","evidence/RETURN285_RECEIPT.json",
                "evidence/RETURN285_PACKET_INDEPENDENT_AUDIT.json","evidence/RETURN285_PACKET_RECEIPT.json",
                "evidence/RETURN285_PACKET_RECORD.json","evidence/RETURN285_PACKET_RECONCILIATION.json"])
            and c["currentReturn285Binding"]["outsideScope"] is True
            and c["currentReturn285Binding"]["authorityUnchanged"]==AUTH,
            c["currentReturn285Binding"])
        record(checks,"The current-source candidate names only the pending target at 816/32/0 on main",
            c["currentBranch"]=="main" and c["currentAuthority"]==AUTH
            and c["currentPendingGroup"]=={"group":"rank9-impact-exile4","spellIds":TARGETS,"count":1}
            and delivery["sourceBranch"]=="main" and delivery["pendingIds"]==TARGETS,
            {"branch":c["currentBranch"],"pendingGroup":c["currentPendingGroup"],"authority":c["currentAuthority"]})
    passed=sum(x["passed"] for x in checks)
    report={"id":"RANK9IMPACTEXILE4-PACKET-286-INDEPENDENT-AUDIT","status":"PASS" if passed==len(checks) else "FAIL",
        "checkedAtUtc":datetime.now(timezone.utc).isoformat(),"archive":{"path":ARCHIVE.relative_to(ROOT).as_posix(),"bytes":actual[0],"sha256":actual[1],"crc32":actual[2]},
        "delivery":{"path":DELIVERY.relative_to(ROOT).as_posix(),"bytes":DELIVERY.stat().st_size,"sha256":digest_file(DELIVERY)[1]},
        "authority":AUTH,"acceptedIds":[],"targetIds":TARGETS,"checkCount":len(checks),"passedChecks":passed,
        "failedChecks":[x for x in checks if not x["passed"]],"checks":checks}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"id":"RANK9IMPACTEXILE4-PACKET-286-INDEPENDENT-AUDIT-RECEIPT","status":report["status"],
        "archiveSHA256":actual[1],"deliverySHA256":digest_file(DELIVERY)[1],"auditPath":REPORT.relative_to(ROOT).as_posix(),
        "checkCount":len(checks),"passedChecks":passed,"failedChecks":len(report["failedChecks"]),"acceptedIds":[],"pendingIds":TARGETS,
        "authority":AUTH}
    RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    if report["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__": main()

