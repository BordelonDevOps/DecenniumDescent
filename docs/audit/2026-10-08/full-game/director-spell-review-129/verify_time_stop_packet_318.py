from __future__ import annotations

import hashlib
import json
import pathlib
import zipfile
import zlib
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
PACKET_DIR = AUDIT / "rank9_time_stop_current_source_318_prepared"
PACKET = PACKET_DIR / "DD_Rank9_TimeStop_CurrentSource_318.zip"
DELIVERY = PACKET_DIR / "DD_Rank9_TimeStop_CurrentSource_318_DELIVERY.json"
BASELINE = AUDIT / "rank9_timefate6_current_source_282_prepared" / "DD_Rank9_TimeFate6_CurrentSource_282.zip"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_json(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8"))


def safe(path: str) -> bool:
    p = pathlib.PurePosixPath(path)
    return bool(path) and not p.is_absolute() and ".." not in p.parts and "\\" not in path


def main() -> None:
    raw_packet = PACKET.read_bytes()
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8"))
    checks: list[dict[str, Any]] = []
    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "passed": bool(condition), "detail": detail})

    check("delivery binds exact Packet318 archive size and SHA-256", len(raw_packet) == delivery["archive"]["bytes"] and digest(raw_packet) == delivery["archive"]["sha256"], {"bytes": len(raw_packet), "sha256": digest(raw_packet)})
    baseline_raw = BASELINE.read_bytes()
    baseline_digest = {"path": BASELINE.relative_to(ROOT).as_posix(), "bytes": len(baseline_raw), "sha256": digest(baseline_raw), "crc32": f"{zlib.crc32(baseline_raw) & 0xffffffff:08x}"}
    baseline_context = load_json(zipfile.ZipFile(PACKET).read("CONTEXT.json"))["sourceBaseline"]
    check("Packet282 archive binding matches current historical source archive", all(baseline_digest[k] == baseline_context[k] for k in baseline_digest), baseline_digest)

    with zipfile.ZipFile(PACKET) as zf:
        names = zf.namelist()
        check("ZIP central directory is valid and every member name is unique/safe", zf.testzip() is None and len(names) == len(set(names)) and all(safe(x) for x in names), {"members": len(names)})
        all_members_hashed = True
        manifest_items = load_json(zf.read("evidence/time_stop/preserved_case_manifest.json"))["cases"]
        case_errors = []
        for entry in manifest_items:
            case_raw = zf.read(entry["member"])
            if len(case_raw) != entry["bytes"] or digest(case_raw) != entry["sha256"]:
                case_errors.append(entry["id"])
        check("all 14 preserved case records match their canonical byte/hash manifest", len(manifest_items) == 14 and not case_errors, {"caseCount": len(manifest_items), "errors": case_errors})

        context = load_json(zf.read("CONTEXT.json"))
        check("authority and single target are 823/25/0 and time-stop only", context["authority"] == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173} and context["scopeIds"] == ["time-stop"] and context["pendingClosureTasks"] == 25, context["authority"])
        current_index = load_json(zf.read("authority/current/authored_review_index.json"))
        current_catalog = load_json(zf.read("authority/current/catalog.json"))
        entry_by_id = {x["id"]: x for x in current_index["entries"]}
        row_by_id = {x["id"]: x for x in current_catalog["spells"]}
        check("current Time Stop remains pending with no procedure pointer or operational card", entry_by_id["time-stop"]["authoredStatus"] == "pending-authored-procedure" and entry_by_id["time-stop"]["procedurePointer"] is None and row_by_id["time-stop"]["operational"] is None, entry_by_id["time-stop"])
        check("Timeless Form remains pending under separate DF218-B03 dependency", entry_by_id["timeless-form"]["authoredStatus"] == "pending-authored-procedure" and entry_by_id["timeless-form"]["procedurePointer"] is None and row_by_id["timeless-form"]["operational"] is None and load_json(zf.read("evidence/timeless_form/blocker_dependency.json"))["timelessFormBlockerId"] == "DF218-B03", entry_by_id["timeless-form"])

        queue = load_json(zf.read("authority/current/CURRENT_SPELL_QUEUE_317.json"))
        handoff = load_json(zf.read("authority/current/CURRENT_HANDOFF_317.json"))
        pending = load_json(zf.read("authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_317.json"))
        check("queue317, handoff317 and pending audit317 agree on current 25-pending authority", queue["currentAuthority"] == context["authority"] and handoff["authority"] == context["authority"] and pending["authority"] == context["authority"] and pending["pendingCount"] == 25, {"queue": queue["currentAuthority"], "pending": pending["pendingCount"]})
        check("historical sourceQueue316 provenance is retained while queue317 is current", pending["sourceQueue"]["path"].endswith("CURRENT_SPELL_QUEUE_316.json") and context["currentQueueBinding"]["path"].endswith("CURRENT_SPELL_QUEUE_317.json"), {"historical": pending["sourceQueue"]["path"], "current": context["currentQueueBinding"]["path"]})

        comparison = load_json(zf.read("evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json"))
        old_current = [x for x in comparison["rows"] if x["status"] == "UNCHANGED"]
        changed_current = [x for x in comparison["rows"] if x["status"] == "CHANGED"]
        missing = [x for x in comparison["rows"] if x["status"] == "MISSING"]
        check("Packet282 inventory has 140 rows, 139 unchanged, one changed and no missing files", len(comparison["rows"]) == 140 and len(old_current) == 139 and len(changed_current) == 1 and not missing and changed_current[0]["path"] == "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json", {"unchanged": len(old_current), "changed": [x["path"] for x in changed_current], "missing": len(missing)})
        unchanged_verified = 0
        delta_verified = 0
        with zipfile.ZipFile(BASELINE) as oldzip:
            for row in old_current:
                member = "sources_current/" + row["path"]
                oldbytes = oldzip.read(member)
                if len(oldbytes) == row["oldBytes"] and digest(oldbytes) == row["oldSha256"]:
                    unchanged_verified += 1
            for row in changed_current:
                raw_changed = zf.read("evidence/source_comparison/current_changed/authored_review_index.json")
                local = (ROOT / pathlib.Path(row["path"])).read_bytes()
                if raw_changed == local and len(raw_changed) == row["currentBytes"] and digest(raw_changed) == row["currentSha256"]:
                    delta_verified += 1
        check("139 unchanged source rows still match exact Packet282 archive members; changed index is current and supplied", unchanged_verified == 139 and delta_verified == 1, {"unchangedVerified": unchanged_verified, "changedVerified": delta_verified})

        procedure_raw = zf.read("evidence/time_stop/procedure.json")
        procedure = load_json(procedure_raw)
        b01 = load_json(zf.read("evidence/time_stop/TF192-B01.json"))
        check("exact procedure and hold record bind TF192-B01 only", procedure["blockerIds"] == ["TF192-B01"] and b01["id"] == "TF192-B01" and b01["status"] == "OPEN", {"blocker": b01["id"], "caseIds": len(procedure["caseIds"])})
        check("all three native Time Stop placements/modes are preserved", [x["school"] for x in row_by_id["time-stop"]["source"]["original"]["placements"]] == ["Illusion", "Transmutation", "Universal"] and "modes" in procedure["procedure"], row_by_id["time-stop"]["source"]["original"]["placements"])
        pq = load_json(zf.read("evidence/time_stop/questions_and_obligations.json"))
        qids = {q["id"] for q in pq["questions"]}
        qids |= {x["originalQuestionUnchanged"]["id"] for x in pq["focusedAddenda"]}
        expected_questions = {*(f"TF9-Q{i:02}" for i in range(1, 8)), "TF9-Q32", "TIME129-ADD01"}
        obligation_ids = {x["id"] for x in pq["obligations"]}
        check("Time Stop question and obligation scope is complete", qids == expected_questions and obligation_ids == {"TF9-CAST", "TF9-STOP-MODES", "TF9-STOP-WORLD", "TF9-PERSISTENCE"}, {"questionIds": sorted(qids), "obligations": sorted(obligation_ids)})

        ra_acceptance = load_json(zf.read("authority/reality_anchor/REALITY_ANCHOR_ACCEPTANCE_316.json"))
        ra_application = load_json(zf.read("authority/reality_anchor/REALITY_ANCHOR_APPLICATION_316.json"))
        check("Return316 acceptance and application receipts record Reality Anchor only", ra_acceptance["acceptedIds"] == ["reality-anchor"] and ra_application["appliedIds"] == ["reality-anchor"], {"accepted": ra_acceptance["acceptedIds"], "applied": ra_application["appliedIds"]})
        check("no Time Stop acceptance, application, runtime execution, or broader scope is asserted", context["acceptedIds"] == [] and context["appliedIds"] == [] and context["runtimeExecuted"] is False and context["scopeIds"] == ["time-stop"], None)

    audit = {
        "id": "TIME-STOP-PACKET-318-READBACK-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS" if all(x["passed"] for x in checks) else "FAIL",
        "packet": {"path": PACKET.relative_to(ROOT).as_posix(), "bytes": len(raw_packet), "sha256": digest(raw_packet), "crc32": f"{zlib.crc32(raw_packet) & 0xffffffff:08x}"},
        "deliveryBindingMatches": len(raw_packet) == delivery["archive"]["bytes"] and digest(raw_packet) == delivery["archive"]["sha256"],
        "checkCount": len(checks), "passedChecks": sum(1 for x in checks if x["passed"]), "failedChecks": sum(1 for x in checks if not x["passed"]),
        "checks": checks,
    }
    out = AUDIT / "TIME_STOP_PACKET_318_READBACK_AUDIT.json"
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": audit["status"], "packetBytes": len(raw_packet), "packetSha256": digest(raw_packet), "memberCount": len(zipfile.ZipFile(PACKET).namelist()), "checkCount": len(checks), "passed": audit["passedChecks"], "failed": audit["failedChecks"], "audit": out.as_posix()}, ensure_ascii=False))
    if not all(x["passed"] for x in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
