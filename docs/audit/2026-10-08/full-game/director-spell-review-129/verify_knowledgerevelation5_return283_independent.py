from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_knowledgerevelation5_return283_received"
ARCHIVE = RECEIVED / "DD_Rank9_KnowledgeRevelation5_Director_Return283_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_KnowledgeRevelation5_Director_Return283_HELD_DELIVERY.json"
PACKET_DIR = BASE / "rank9_knowledgerevelation5_current_source_283_prepared"
PACKET = PACKET_DIR / "DD_Rank9_KnowledgeRevelation5_CurrentSource_283.zip"
PACKET_DELIVERY = PACKET_DIR / "DD_Rank9_KnowledgeRevelation5_CurrentSource_283_DELIVERY.json"
SUPPLEMENT_DIR = BASE / "rank9_knowledgerevelation5_return198_witness_supplement_283"
SUPPLEMENT = SUPPLEMENT_DIR / "DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_283.zip"
SUPPLEMENT_DELIVERY = SUPPLEMENT_DIR / "DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_283_DELIVERY.json"
PRIOR = BASE / "rank9_knowledgerevelation5_return198_received/DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
REPORT = BASE / "RANK9_KNOWLEDGEREVELATION5_RETURN283_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_KNOWLEDGEREVELATION5_RETURN283_RECEIPT.json"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
SPELL = "faction-omniscience-supreme"
HELD = [SPELL]
BLOCKERS = ["KR198-B01"]
QUALS = ["KR198-H01", "KR198-H02", "KR198-H03", "KR198-H04", "KR198-H05", "KR198-H06"]
NEXT = {"groupId": "rank9-planar-gates5", "pendingIds": ["banishment-gate", "conjure-demiplane-fortress"],
        "requiresFreshAuthorityPacket": True}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def file_binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def member_binding(archive: zipfile.ZipFile, name: str) -> dict:
    raw = archive.read(name)
    return {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(x not in ("", ".", "..") for x in path.parts)


def state_sha(value: object) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))


def replay(case: dict) -> tuple[bool, int, int, int]:
    if state_sha(case["initialState"]) != case["initialSHA256"] or state_sha(case["finalState"]) != case["finalSHA256"]:
        return False, 0, 0, 0
    state = case["initialState"]
    prev_time = float("-inf")
    forward = inverse = 0
    for event in case["events"]:
        before, after = event["beforeState"], event["afterState"]
        fops, iops = event["forward"], event["inverse"]
        forward += len(fops); inverse += len(iops)
        t = after.get("time")
        if (before != state or state_sha(before) != event["beforeSHA256"] or state_sha(after) != event["afterSHA256"]
                or len(fops) != 2 or len(iops) != 2 or (isinstance(t, (int, float)) and t < prev_time)):
            return False, forward, inverse, len(case["events"])
        if isinstance(t, (int, float)):
            prev_time = t
        if not (fops[0] == {"op": "test", "path": "", "value": before}
                and fops[1] == {"op": "replace", "path": "", "value": after}
                and iops[0] == {"op": "test", "path": "", "value": after}
                and iops[1] == {"op": "replace", "path": "", "value": before}):
            return False, forward, inverse, len(case["events"])
        state = after
    return state == case["finalState"], forward, inverse, len(case["events"])


def main() -> None:
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    packet_delivery = json.loads(PACKET_DELIVERY.read_text(encoding="utf-8-sig"))
    supplement_delivery = json.loads(SUPPLEMENT_DELIVERY.read_text(encoding="utf-8-sig"))
    checks: list[dict] = []

    def ck(name: str, passed: bool, detail=None) -> None:
        checks.append({"id": name, "passed": bool(passed), "details": detail})

    archive_info, packet_info, supplement_info = file_binding(ARCHIVE), file_binding(PACKET), file_binding(SUPPLEMENT)
    ck("Downloaded Return283 archive matches exact delivery bytes, SHA-256 and CRC32",
       archive_info == {k: delivery["archive"][k] for k in ("bytes", "sha256", "crc32")}, archive_info)
    ck("Packet283 and Return198 witness supplement bind to their exact local delivery manifests and Return283 references",
       all(packet_info[k] == packet_delivery["archive"][k] == delivery["sourcePacket"][k] for k in ("bytes", "sha256", "crc32")) and
       all(supplement_info[k] == delivery["targetWitnessSupplement"][k] for k in ("bytes", "sha256", "crc32")) and
       all(supplement_info[k] == supplement_delivery["archive"][k] for k in ("bytes", "sha256")),
       {"packet": packet_info, "supplement": supplement_info})
    ck("Return283 delivery is the exact one-spell hold at authority 816/32/0",
       delivery.get("id") == "RANK9-KNOWLEDGEREVELATION5-DIRECTOR-RETURN283-DELIVERY" and
       delivery.get("sourceAuthority") == AUTH and delivery.get("accepted") is False and delivery.get("applied") is False and
       delivery.get("acceptedIds") == delivery.get("appliedIds") == [] and delivery.get("heldIds") == HELD and
       delivery.get("blockerIds") == BLOCKERS and delivery.get("qualificationIds") == QUALS and delivery.get("nextPendingGroup") == NEXT,
       {"authority": delivery.get("sourceAuthority"), "heldIds": delivery.get("heldIds"), "blockers": delivery.get("blockerIds"), "next": delivery.get("nextPendingGroup")})

    with zipfile.ZipFile(ARCHIVE) as returned, zipfile.ZipFile(PACKET) as packet, zipfile.ZipFile(SUPPLEMENT) as supplement, zipfile.ZipFile(PRIOR) as prior:
        names = returned.namelist()
        outer_rows = {row["path"]: row for row in delivery["members"]}
        manifest = json.loads(returned.read("MEMBER_MANIFEST.json"))
        inner_rows = {row["path"]: row for row in manifest["members"]}
        row_errors = []
        for name in names:
            actual = member_binding(returned, name)
            if name not in outer_rows or actual != {k: outer_rows[name][k] for k in ("bytes", "sha256", "crc32")}:
                row_errors.append("outer:" + name)
            if name != "MEMBER_MANIFEST.json" and (name not in inner_rows or actual != {k: inner_rows[name][k] for k in ("bytes", "sha256", "crc32")}):
                row_errors.append("inner:" + name)
        ck("Return283 ZIP has 63 unique safe members and all inner/outer size-SHA-CRC rows pass",
           returned.testzip() is None and len(names) == len(set(names)) == delivery.get("memberCount") == 63 and
           delivery.get("payloadMemberCount") == manifest.get("payloadMemberCount") == len(inner_rows) == 62 and
           set(names) == set(outer_rows) and set(names) - {"MEMBER_MANIFEST.json"} == set(inner_rows) and
           all(safe(name) for name in names) and not row_errors,
           {"members": len(names), "payload": len(inner_rows), "errors": row_errors[:10]})
    
        package = delivery.get("packageChecks", {})
        ck("All sealed packaging checks pass",
           package.get("checkCount") == package.get("passed") == 256 and package.get("failed") == 0 and
           all(row.get("pass") is True for row in package.get("checks", [])) and
           delivery.get("totalChecksIncludingPackage") == 4653,
           {"checks": package.get("checkCount"), "failed": package.get("failed"), "total": delivery.get("totalChecksIncludingPackage")})

        decision = json.loads(returned.read("DIRECTOR_DECISION.json"))
        row = decision["perIdentity"][0]
        ck("Sealed decision holds only faction-omniscience-supreme under KR198-B01/H01-H06",
           decision.get("group") == "rank9-knowledge-revelation5" and decision.get("scope") == HELD and
           decision.get("sourceAuthority") == decision.get("postDecisionAuthority") == AUTH and
           decision.get("accepted") is False and decision.get("applied") is False and decision.get("held") is True and
           decision.get("acceptedIds") == decision.get("appliedIds") == [] and decision.get("heldIds") == HELD and
           decision.get("blockerIds") == BLOCKERS and decision.get("qualificationIds") == QUALS and
           row.get("id") == SPELL and row.get("decision") == "HOLD" and row.get("accepted") is False and row.get("applied") is False and
           row.get("blockerIds") == BLOCKERS and row.get("qualificationIds") == QUALS and
           isinstance(row.get("minimumMissingWitness"), list) and len(row["minimumMissingWitness"]) == 4,
           {"decision": row, "qualifications": decision.get("qualificationIds")})
        ck("Minimum missing witness lists the complete faction ledger, forecast, privacy/continuity and positive lifecycle inputs",
           [x.get("id") for x in row["minimumMissingWitness"]] == ["KR198-B01-W1", "KR198-B01-W2", "KR198-B01-W3", "KR198-B01-W4"] and
           json.loads(returned.read("MINIMUM_WITNESS.json"))["blockerId"] == BLOCKERS[0], row["minimumMissingWitness"])
        ck("Return283 preserves all downstream gates and makes no canonical/GitHub/application/runtime changes",
           decision.get("canonicalFilesModified") is False and decision.get("applicationPerformed") is False and
           decision.get("GitHubModified") is False and decision.get("sourceProgramsExecuted") is False and
           decision.get("runtimeExecuted") is False and all(decision.get(k) is False for k in
           ("implementationApproved", "humanPlayApproved", "balanceApproved", "cosmologyApproved", "completionApproved", "releaseApproved")) and
           decision.get("allUnrelatedHoldsUnchanged") is True,
           {k: decision.get(k) for k in ("canonicalFilesModified", "applicationPerformed", "GitHubModified", "runtimeExecuted", "allUnrelatedHoldsUnchanged")})
        ck("Next group is exactly Planar Gates5 with two pending identities",
           decision.get("nextPendingGroup") == delivery.get("nextPendingGroup") == json.loads(returned.read("REMAINING_QUEUE.json")).get("nextPendingGroup") == NEXT,
           decision.get("nextPendingGroup"))

        counts = json.loads(returned.read("COUNTS.json"))
        expected_counts = {"procedures": 1, "sourceBindings": 126, "cases": 8, "events": 140,
                           "forwardOperations": 280, "inverseOperations": 280, "sourceChecks": 1295,
                           "dataChecks": 877, "clockChecks": 2048, "semanticInvariantChecks": 166,
                           "semanticManualChecks": 11, "preSealChecks": 4397, "acceptedIds": 0, "appliedIds": 0, "heldIds": 1}
        ck("Decision counts reconcile 126 sources, eight cases, reversible traces and all review checks",
           all(counts.get(k) == v for k, v in expected_counts.items()) and delivery.get("counts") == counts,
           {k: counts.get(k) for k in expected_counts})

        source_doc = json.loads(returned.read("SOURCE_BINDING.json"))
        source_rows = source_doc.get("currentSourceBindings", [])
        source_candidate = json.loads(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_283.json"))
        candidate_rows = {row["path"]: row for row in source_candidate.get("currentSourceBindings", [])}
        return_rows = {row["path"]: row for row in source_rows}
        source_errors = []
        packet_manifest = json.loads(packet.read("MANIFEST.json"))
        packet_manifest_rows = {row["path"]: row for row in packet_manifest.get("members", [])}
        for row in source_rows:
            member = row["packetMember"]
            if member not in packet.namelist():
                source_errors.append(member + ":missing")
                continue
            raw = packet.read(member)
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or blob != row["gitBlobSHA1"]:
                source_errors.append(member + ":source-binding")
            manifest_row = packet_manifest_rows.get(member)
            if not manifest_row or {k: manifest_row[k] for k in ("bytes", "sha256", "crc32")} != member_binding(packet, member):
                source_errors.append(member + ":manifest")
        ck("All 126 current source bindings match Packet283 bytes, Git blob IDs and exact candidate rows",
           source_doc.get("sourceAuthority") == AUTH and source_doc.get("sourceBranch") == "main" and
           source_doc.get("inputArchive", {}).get("sha256") == packet_info["sha256"] and
           len(source_rows) == len(candidate_rows) == 126 and set(return_rows) == set(candidate_rows) and
           all(return_rows[k] == candidate_rows[k] for k in return_rows) and not source_errors,
           {"sources": len(source_rows), "candidateRows": len(candidate_rows), "errors": source_errors[:10]})

        reports = [("SOURCE_VERIFICATION.json", 1295), ("DATA_INTEGRITY_CHECK.json", 877), ("CLOCK_CHECK.json", 2048),
                   ("SEMANTIC_INVARIANT_CHECKS.json", 166)]
        report_summary = {}
        report_good = True
        for name, expected_count in reports:
            report = json.loads(returned.read(name))
            report_summary[name] = {"count": report.get("checkCount"), "failures": report.get("failureCount")}
            report_good = report_good and report.get("checkCount") == expected_count and report.get("failureCount") == 0 and all(x.get("pass") is True for x in report.get("checks", []))
        sem = json.loads(returned.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        validation = json.loads(returned.read("VALIDATION.json"))
        witness_failures = sem.get("requiredWitnessFailures", [])
        report_good = report_good and sem.get("semanticAcceptancePass") is False and sem.get("decision") == "HOLD" and sem.get("unexpectedFailures") == [] and len(witness_failures) == 1 and witness_failures[0].get("id") == "KR198-B01" and validation.get("sourceIntegrity") == "PASS" and validation.get("dataReplay") == "PASS" and validation.get("clockChecks") == "PASS_SCOPED_STATIC_INVARIANTS" and validation.get("semanticInvariantChecks") == "PASS" and validation.get("requiredWholePositiveWitness") == "INCOMPLETE_KR198-B01"
        ck("Source, data, clock and semantic reports pass while the required whole-positive witness stays incomplete", report_good,
           {"reports": report_summary, "semanticDecision": sem.get("decision"), "requiredWitnessFailures": sem.get("requiredWitnessFailures"), "validation": validation.get("requiredWholePositiveWitness")})

        case_paths = sorted(name for name in returned.namelist() if name.startswith("cases/") and name.endswith(".json"))
        case_errors = []
        event_count = forward = inverse = 0
        for path in case_paths:
            raw = returned.read(path)
            if path not in prior.namelist() or prior.read(path) != raw:
                case_errors.append(path + ":not-exact-prior-case")
                continue
            ok, fcount, icount, events = replay(json.loads(raw))
            event_count += events; forward += fcount; inverse += icount
            if not ok:
                case_errors.append(path + ":replay")
        procedure = "procedures/faction-omniscience-supreme.json"
        procedure_exact = procedure in returned.namelist() and procedure in prior.namelist() and returned.read(procedure) == prior.read(procedure)
        ck("Original procedure and eight Return198 cases remain byte-exact and replay reversibly", procedure_exact and
           len(case_paths) == 8 and not case_errors and event_count == 140 and forward == inverse == 280,
           {"procedureExact": procedure_exact, "cases": len(case_paths), "events": event_count, "forward": forward, "inverse": inverse, "errors": case_errors[:10]})

        embedded_checks = [
            ("evidence/DD_Rank9_KnowledgeRevelation5_CurrentSource_283_DELIVERY.json", PACKET_DELIVERY),
            ("evidence/DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_283_DELIVERY.json", SUPPLEMENT_DELIVERY),
            ("evidence/RANK9_KNOWLEDGEREVELATION5_PACKET_283_INDEPENDENT_AUDIT.json", BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_283_INDEPENDENT_AUDIT.json"),
            ("evidence/RANK9_KNOWLEDGEREVELATION5_PACKET_283_RECEIPT.json", BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_283_RECEIPT.json"),
        ]
        embed_errors = [name for name, path in embedded_checks if name not in returned.namelist() or returned.read(name) != path.read_bytes()]
        ck("Return283 embeds exact local Packet283 delivery, supplement delivery and independent packet audit records", not embed_errors, embed_errors)

    now = datetime.now(timezone.utc).isoformat()
    failures = [row for row in checks if not row["passed"]]
    report = {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN283-INDEPENDENT-AUDIT", "recordedAtUtc": now,
              "status": "PASS" if not failures else "FAIL",
              "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_info},
              "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **file_binding(DELIVERY)},
              "sourcePacket": {"path": PACKET.relative_to(ROOT).as_posix(), **packet_info},
              "authority": AUTH, "group": "rank9-knowledge-revelation5", "targetIds": HELD,
              "acceptedIds": [], "appliedIds": [], "heldIds": HELD, "blockers": BLOCKERS,
              "qualifications": QUALS, "nextGroup": NEXT,
              "sourceBindingsVerified": 126, "cases": 8, "events": 140,
              "forwardOperations": 280, "inverseOperations": 280,
              "checksPassed": sum(row["passed"] for row in checks), "checksFailed": len(failures),
              "checkCount": len(checks), "checks": checks,
              "scopeLimitation": "Verifies package integrity, current source and prior-case byte bindings, decision metadata, replay and review ledgers; it does not independently adjudicate game-rule semantics."}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    receipt = {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN283-RECEIPT", "status": report["status"],
               "auditReport": REPORT.relative_to(ROOT).as_posix(), "auditReportSHA256": sha(REPORT.read_bytes()),
               "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
               "authority": AUTH, "acceptedIds": [], "appliedIds": [], "heldIds": HELD,
               "blockers": BLOCKERS, "qualifications": QUALS, "nextGroup": NEXT,
               "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"]}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
