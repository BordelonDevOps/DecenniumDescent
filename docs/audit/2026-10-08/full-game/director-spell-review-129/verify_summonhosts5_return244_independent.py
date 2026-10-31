from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_summonhosts5_return244_received"
ARCHIVE = RECEIVED / "DD_Rank9_SummonHosts3_Director_Return244_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_SummonHosts3_Director_Return244_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_summonhosts5_current_source_244_prepared"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_SummonHosts5_CurrentSource_244.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_SummonHosts5_CurrentSource_244_DELIVERY.json"
SOURCE_CANDIDATE = SOURCE_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json"
SOURCE_CONTEXT = SOURCE_DIR / "CURRENT_CONTEXT_244.json"
REQUEST = SOURCE_DIR / "REQUEST_244.txt"
SOURCE_PREPARATION = BASE / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_244.json"
OLD_DIR = BASE / "rank9_summonhosts5_return227_received"
OLD_ARCHIVE = OLD_DIR / "DD_Rank9_SummonHosts3_Director_Return227.zip"
OLD_DELIVERY = OLD_DIR / "DD_Rank9_SummonHosts3_Director_Return227_DELIVERY.json"
OLD_AUDIT = BASE / "RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json"
REPORT = BASE / "RANK9SUMMONHOSTS5_RETURN244_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9SUMMONHOSTS5_RETURN244_RECEIPT.json"

TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
BLOCKERS = {
    "summon-elemental-avatar": ["SH202-B01"],
    "summon-herald-of-the-planes": ["SH202-B02"],
    "summon-avatar-of-decay": ["SH202-B03"],
}
QUALIFICATIONS = [f"SH202-H{i:02d}" for i in range(1, 13)]
AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
NEXT = {"group": "rank9-impact-exile4", "pendingIds": ["reverse-gravity-field"]}
EXPECTED_COUNTS = {
    "procedures": 3,
    "nativePlacements": 3,
    "nativeClassAccessRows": 8,
    "sourceBindings": 260,
    "originalQuestionsPreserved": 32,
    "focusedAddendaPreserved": 2,
    "targetQuestionDispositions": 23,
    "futureRequirementsPreserved": 8,
    "requiredMainCases": 6,
    "branches": 22,
    "demonstratedComponents": 23,
    "incompleteMainCases": 5,
    "cases": 28,
    "events": 3665,
    "forwardEventOperations": 7330,
    "inverseEventOperations": 7330,
    "eventOperations": 14660,
    "proposalOperations": 12,
    "totalOperations": 14672,
    "actorStateRecordsChecked": 14556,
    "blockers": 3,
    "conditionalQualifications": 12,
    "acceptedIds": 0,
    "appliedIds": 0,
    "heldIds": 3,
    "auditChecks": 140418,
    "focusedSemanticChecks": 25,
    "totalFreshChecksBeforePackaging": 140443,
    "targetFutureDispositions": 6,
}

def file_digest(path: Path) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return size, h.hexdigest(), f"{crc & 0xFFFFFFFF:08x}"

def member_digest(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with archive.open(name, "r") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return size, h.hexdigest(), f"{crc & 0xFFFFFFFF:08x}"

def read_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8-sig"))

def record(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})

def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    archive_size, archive_sha, archive_crc = file_digest(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = file_digest(DELIVERY)
    record(checks, "Return244 archive bytes, SHA-256 and CRC32 match its delivery manifest",
        (archive_size, archive_sha, archive_crc) == (
            delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower())
        and delivery["archive"]["path"] == ARCHIVE.name,
        {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc})
    record(checks, "Return244 external delivery is SH244-DELIVERY and records current source packet/authority",
        delivery["id"] == "SH244-DELIVERY" and delivery["authority"] == AUTHORITY
        and delivery["sourcePacket"]["path"] == SOURCE_ARCHIVE.name,
        {"id": delivery["id"], "sourcePacket": delivery["sourcePacket"], "authority": delivery["authority"]})

    source_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
    source_size, source_sha, source_crc = file_digest(SOURCE_ARCHIVE)
    source_preparation = json.loads(SOURCE_PREPARATION.read_text(encoding="utf-8-sig"))
    source_delivery_size, source_delivery_sha, _ = file_digest(SOURCE_DELIVERY)
    record(checks, "Submitted Packet244 archive and manifest match Return244 source binding",
        (source_size, source_sha, source_crc) == (
            delivery["sourcePacket"]["bytes"], delivery["sourcePacket"]["sha256"],
            delivery["sourcePacket"]["crc32"].lower())
        and (source_size, source_sha, source_crc) == (
            source_delivery["archive"]["bytes"], source_delivery["archive"]["sha256"],
            source_delivery["archive"]["crc32"].lower()),
        {"bytes": source_size, "sha256": source_sha, "crc32": source_crc})
    record(checks, "Submitted Packet244 sidecars retain their recorded byte/SHA bindings",
        source_delivery_size == source_preparation["deliveryManifest"]["bytes"]
        and source_delivery_sha == source_preparation["deliveryManifest"]["sha256"]
        and file_digest(SOURCE_CANDIDATE)[:2] == (
            source_delivery["candidate"]["bytes"], source_delivery["candidate"]["sha256"])
        and file_digest(SOURCE_CONTEXT)[:2] == (
            source_delivery["context"]["bytes"], source_delivery["context"]["sha256"])
        and file_digest(REQUEST)[:2] == (
            source_delivery["request"]["bytes"], source_delivery["request"]["sha256"]),
        {"candidate": source_delivery["candidate"], "context": source_delivery["context"],
         "request": source_delivery["request"]})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        unsafe = [n for n in names if n.startswith(("/", "\\"))
            or "\\" in n or PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts]
        rows = {row["path"]: row for row in delivery["members"]}
        record(checks, "Return244 has 104 unique safe members; external allowlist and ZIP CRCs are exact",
            len(names) == len(set(names)) == len(rows) == delivery["memberCount"] == 104
            and delivery["payloadMemberCount"] == 103 and set(names) == set(rows)
            and not unsafe and z.testzip() is None,
            {"archiveMembers": len(names), "deliveryMembers": len(rows), "unsafe": unsafe[:8]})
        member_failures = []
        for name in names:
            got = member_digest(z, name)
            row = rows[name]
            if got != (row["bytes"], row["sha256"], row["crc32"].lower()):
                member_failures.append({"path": name, "actual": got, "expected": row})
        record(checks, "All 104 archive members match external byte/SHA/CRC bindings",
            not member_failures, {"checked": len(names), "failures": member_failures[:8]})

        internal = read_json(z, "MEMBER_MANIFEST.json")
        inner_rows = {row["path"]: row for row in internal["members"]}
        inner_failures = []
        for name, row in inner_rows.items():
            if member_digest(z, name) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                inner_failures.append(name)
        record(checks, "Internal manifest binds every non-self member and exact scope/authority",
            internal["id"] == "SH244-EXACT-MEMBER-MANIFEST"
            and internal["memberCountExcludingSelf"] == 103 and len(inner_rows) == 103
            and internal["onlySelfExclusion"] == "MEMBER_MANIFEST.json is bound by external DELIVERY.json. No other unlisted member."
            and set(inner_rows) == set(names) - {"MEMBER_MANIFEST.json"} and not inner_failures
            and internal["sourcePacket"]["sha256"] == source_sha
            and internal["authority"] == AUTHORITY and internal["acceptedIds"] == []
            and internal["appliedIds"] == [] and set(internal["heldIds"]) == set(TARGETS),
            {"manifestMembers": len(inner_rows), "failures": inner_failures[:8]})

        package = delivery["packageValidation"]
        record(checks, "All 316 sealed package checks pass",
            package["status"] == "PASS" and package["checkCount"] == 316
            and len(package["checks"]) == 316 and all(x.get("passed") is True for x in package["checks"]),
            {"status": package["status"], "checks": package["checkCount"],
             "failed": sum(x.get("passed") is not True for x in package["checks"])})

        decision = read_json(z, "DIRECTOR_DECISION.json")
        decision_rows = {row["id"]: row for row in decision["decisions"]}
        record(checks, "Director decision exactly scopes three pending identities and accepts/applies none",
            decision["id"] == "SH244-DIRECTOR-DECISION" and decision["scope"] == TARGETS
            and set(decision_rows) == set(TARGETS) and decision["authority"] == AUTHORITY
            and delivery["accepted"] is False and delivery["applied"] is False
            and delivery["acceptedIds"] == [] and delivery["appliedIds"] == []
            and set(delivery["heldIds"]) == set(TARGETS)
            and decision["accepted"] is False and decision["applied"] is False
            and decision["acceptedIds"] == [] and decision["appliedIds"] == []
            and set(decision["heldIds"]) == set(TARGETS),
            {"scope": decision["scope"], "heldIds": decision["heldIds"]})
        exact_holds = all(
            decision_rows[spell]["accepted"] is False and decision_rows[spell]["applied"] is False
            and decision_rows[spell]["held"] is True
            and decision_rows[spell]["blockerIds"] == BLOCKERS[spell]
            and bool(decision_rows[spell]["minimumMissingWitness"])
            and decision_rows[spell]["reassessment"]["status"] == "OPEN"
            for spell in TARGETS)
        record(checks, "Each identity retains its exact blocker and explicit missing witness",
            exact_holds and delivery["blockerIds"] == BLOCKERS,
            {"blockers": delivery["blockerIds"],
             "minimumWitnesses": {s: decision_rows[s]["minimumMissingWitness"] for s in TARGETS}})
        blocker_rows = {row["id"]: row for row in decision["blockers"]}
        record(checks, "All three blockers remain open with source-grounded reassessments",
            set(blocker_rows) == {b[0] for b in BLOCKERS.values()}
            and all(blocker_rows[b[0]]["blocking"] is True for b in BLOCKERS.values())
            and set(decision["conditionalQualificationIds"]) == set(QUALIFICATIONS)
            and set(delivery["conditionalQualificationIds"]) == set(QUALIFICATIONS),
            {"blockerIds": sorted(blocker_rows), "qualifications": decision["conditionalQualificationIds"]})

        counts = read_json(z, "COUNTS.json")
        count_failures = {k: (counts.get(k), v) for k, v in EXPECTED_COUNTS.items() if counts.get(k) != v}
        record(checks, "All reported scope, case, event, authority and audit counts reconcile",
            not count_failures and counts["checksByCategory"] == read_json(z, "validation/AUDIT_SUMMARY.json")["checksByCategory"],
            {"countFailures": count_failures, "totalFreshChecks": counts.get("totalFreshChecksBeforePackaging")})

        replay = read_json(z, "validation/CASE_REPLAY.json")
        replay_cases = replay["cases"]
        event_total = sum(c["events"] for c in replay_cases)
        forward_total = sum(c["forwardOperations"] for c in replay_cases)
        inverse_total = sum(c["inverseOperations"] for c in replay_cases)
        case_binding_failures = []
        for case in replay_cases:
            f = case["caseFile"]
            if f["path"] not in names or member_digest(z, f["path"]) != (
                f["bytes"], f["sha256"], f["crc32"].lower()):
                case_binding_failures.append(case["id"])
        incomplete_ids = set(counts["incompleteMainCaseIds"])
        incomplete_actual = {c["id"] for c in replay_cases if c["statusPreserved"] == "HELD_INCOMPLETE"}
        record(checks, "All 28 preserved cases and 3,665 events pass with hash-bound case files",
            replay["scope"] == TARGETS and len(replay_cases) == 28
            and all(c["status"] == "PASS" and c["failures"] == [] for c in replay_cases)
            and event_total == counts["events"] == 3665
            and forward_total == counts["forwardEventOperations"] == 7330
            and inverse_total == counts["inverseEventOperations"] == 7330
            and incomplete_actual == incomplete_ids and len(incomplete_ids) == 5
            and not case_binding_failures,
            {"cases": len(replay_cases), "events": event_total, "forward": forward_total,
             "inverse": inverse_total, "incompleteMainCases": sorted(incomplete_actual),
             "caseBindingFailures": case_binding_failures[:8]})

        dispositions = read_json(z, "CASE_DISPOSITIONS.json")["cases"]
        replay_by_id = {c["id"]: c for c in replay_cases}
        disposition_by_id = {c["id"]: c for c in dispositions}
        record(checks, "All case dispositions preserve exact held or demonstrated status and blocker",
            len(dispositions) == 28 and set(disposition_by_id) == set(replay_by_id)
            and all(disposition_by_id[i]["numericReplay"] == "PASS"
                and disposition_by_id[i]["status"] == replay_by_id[i]["statusPreserved"]
                for i in replay_by_id)
            and all(disposition_by_id[i]["missingEvidence"] == replay_by_id[i]["missingEvidencePreserved"]
                for i in replay_by_id),
            {"caseDispositions": len(dispositions), "heldIncomplete": len(incomplete_actual)})

        old_delivery = json.loads(OLD_DELIVERY.read_text(encoding="utf-8-sig"))
        old_size, old_sha, old_crc = file_digest(OLD_ARCHIVE)
        old_audit = json.loads(OLD_AUDIT.read_text(encoding="utf-8-sig"))
        with zipfile.ZipFile(OLD_ARCHIVE) as old:
            old_names = set(old.namelist())
            current_paths = {n for n in names if n.startswith("cases/") or n.startswith("procedures/")}
            previous_paths = {n for n in old_names if n.startswith("cases/") or n.startswith("procedures/")}
            changed = []
            for name in sorted(current_paths | previous_paths):
                if name not in current_paths or name not in previous_paths or member_digest(z, name) != member_digest(old, name):
                    changed.append(name)
        record(checks, "All three procedures and all 28 cases remain byte-exact to independently audited Return227",
            old_audit["status"] == "PASS"
            and (old_size, old_sha, old_crc) == (
                old_delivery["archive"]["bytes"], old_delivery["archive"]["sha256"], old_delivery["archive"]["crc32"].lower())
            and len(current_paths) == len(previous_paths) == 31
            and current_paths == previous_paths and not changed,
            {"priorAudit": old_audit["status"], "priorCaseProcedureMembers": len(previous_paths),
             "changed": changed[:8]})

        summary = read_json(z, "validation/AUDIT_SUMMARY.json")
        validation = read_json(z, "VALIDATION.json")
        semantic = read_json(z, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        record(checks, "Data replay and focused semantic reassessment pass while acceptance stays held",
            summary["status"] == "PASS" and summary["checkCount"] == 140418
            and summary["failures"] == [] and summary["failedChecks"] == 0
            and validation["dataAudit"]["status"] == "PASS"
            and validation["focusedReassessmentCheckCount"] == 25
            and validation["focusedReassessmentFailures"] == []
            and validation["totalFreshChecksBeforePackaging"] == 140443
            and semantic["status"] == "FAIL_ACCEPTANCE_RETAINED_THREE_BLOCKERS"
            and semantic["freshReassessmentCheckCount"] == 25
            and semantic["auditCheckFailures"] == 0
            and semantic["wholeSpellCompletion"] is False,
            {"dataAuditChecks": summary["checkCount"], "focusedChecks": validation["focusedReassessmentCheckCount"],
             "totalFreshChecks": validation["totalFreshChecksBeforePackaging"],
             "semanticStatus": semantic["status"]})

        source_bindings = read_json(z, "validation/SOURCE_BINDINGS.json")
        candidate = read_json(z, "source_context/CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json")
        candidate_rows = {r["path"]: r for r in candidate["sourceBindings"]}
        return_rows = {r["path"]: r for r in source_bindings["refreshedSourceBindings"]}
        binding_failures = []
        expected_local_overlay = {
            "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_244.json",
            "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_244.json",
            "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_244.json",
        }
        for path in sorted(set(candidate_rows) | set(return_rows)):
            if candidate_rows.get(path) != return_rows.get(path):
                binding_failures.append(path + ":candidate-vs-return")
        local_mismatches = []
        archived_failures = []
        with zipfile.ZipFile(SOURCE_ARCHIVE) as src:
            for path, row in candidate_rows.items():
                local = ROOT / Path(path)
                try:
                    got = file_digest(local)
                    if got[:2] != (row["bytes"], row["sha256"]):
                        local_mismatches.append(path)
                        archived_name = "sources_current/" + path
                        if archived_name not in src.namelist() or member_digest(src, archived_name)[:2] != (
                            row["bytes"], row["sha256"]):
                            archived_failures.append(path)
                except FileNotFoundError:
                    local_mismatches.append(path)
                    archived_name = "sources_current/" + path
                    if archived_name not in src.namelist() or member_digest(src, archived_name)[:2] != (
                        row["bytes"], row["sha256"]):
                        archived_failures.append(path)
        record(checks, "260 source-binding rows match the exact submitted candidate and Packet244 archive",
            len(candidate_rows) == len(return_rows) == 260 and not binding_failures
            and set(local_mismatches) == expected_local_overlay and not archived_failures,
            {"sourceBindings": len(return_rows), "submissionOverlayRows": sorted(local_mismatches),
             "unexpectedArchivedFailures": archived_failures[:8]})

        packet_delivery_in_return = read_json(z, "source_context/DD_Rank9_SummonHosts5_CurrentSource_244_DELIVERY.json")
        candidate_sidecar_hash = file_digest(SOURCE_CANDIDATE)[:2]
        record(checks, "Return carries the exact submitted candidate, context, request and packet delivery",
            z.read("source_context/CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json") == SOURCE_CANDIDATE.read_bytes()
            and z.read("source_context/CURRENT_CONTEXT_244.json") == SOURCE_CONTEXT.read_bytes()
            and z.read("source_context/REQUEST_244.txt") == REQUEST.read_bytes()
            and z.read("source_context/DD_Rank9_SummonHosts5_CurrentSource_244_DELIVERY.json") == SOURCE_DELIVERY.read_bytes()
            and packet_delivery_in_return["archive"]["sha256"] == source_sha
            and candidate_sidecar_hash == (
                source_delivery["candidate"]["bytes"], source_delivery["candidate"]["sha256"]),
            {"candidateBytes": candidate_sidecar_hash[0], "candidateSHA256": candidate_sidecar_hash[1]})

        original = read_json(z, "ORIGINAL_OBLIGATIONS.json")
        questions = read_json(z, "QUESTION_DISPOSITIONS.json")
        future = read_json(z, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        original_question_rows = {q["id"]: q for q in original["sourceQuestions"] + original["focusedAddenda"]}
        record(checks, "All 32 original questions, two addenda, eight requirements and target dispositions are retained",
            len(original["sourceQuestions"]) == 32 and len(original["focusedAddenda"]) == 2
            and len(original["futureObligations"]) == 8
            and questions["historicalOriginalRecordFieldsUnchanged"] is True
            and len(questions["dispositions"]) == 23
            and all(q["originalQuestionUnchanged"] == original_question_rows[q["id"]]
                and q["selectionDoesNotGrantAcceptance"] is True for q in questions["dispositions"])
            and future["allEightOriginalRequirements"] == "ORIGINAL_OBLIGATIONS.json"
            and len(future["targetDispositions"]) == 6,
            {"sourceQuestions": original["sourceQuestions"], "addenda": len(original["focusedAddenda"]),
             "futureRequirements": original["futureObligations"], "targetQuestionDispositions": len(questions["dispositions"]),
             "targetFutureDispositions": len(future["targetDispositions"])})

        hold_register = read_json(z, "HOLD_REGISTER.json")
        inherited = read_json(z, "INHERITED_HOLDS_UNCHANGED.json")
        record(checks, "All 12 qualifications and six recent hold contexts remain carried outside this scope",
            len(hold_register["blockingRecords"]) == 3 and len(hold_register["conditionalQualificationRecords"]) == 12
            and len(hold_register["perIdentityHoldIds"]) == 3
            and all(hold_register["perIdentityHoldIds"][spell][0] == BLOCKERS[spell][0]
                and hold_register["perIdentityHoldIds"][spell][1:] == QUALIFICATIONS for spell in TARGETS)
            and len(inherited["sealedCurrentContext"]) == 6
            and all(row["heldIds"] and row["acceptedIds"] == [] and row["appliedIds"] == []
                for row in inherited["sealedCurrentContext"])
            and len(inherited["explicitNamedBlockers"]) == 6,
            {"blockingRecords": len(hold_register["blockingRecords"]),
             "qualificationRecords": len(hold_register["conditionalQualificationRecords"]),
             "recentContexts": len(inherited["sealedCurrentContext"]),
             "explicitNamedBlockerContexts": len(inherited["explicitNamedBlockers"])})

        next_group = read_json(z, "NEXT_QUEUE_GROUP.json")
        queue = read_json(z, "source_context/CURRENT_SPELL_QUEUE_244.json")
        pending = read_json(z, "source_context/CURRENT37_PENDING_IDENTITY_AUDIT_244.json")
        queue_match = any(r.get("group") == NEXT["group"] and r.get("pendingIds") == NEXT["pendingIds"]
            for r in queue.get("currentPendingGroups", []))
        record(checks, "Director-selected next group is exactly the still-pending queue identity",
            decision["nextPendingGroup"] == delivery["nextPendingGroup"] == next_group == NEXT
            and queue_match and NEXT["pendingIds"][0] in pending["pendingIds"]
            and pending["authority"] == AUTHORITY,
            {"nextPendingGroup": next_group, "queueMatch": queue_match})

    passed = sum(c["passed"] for c in checks)
    report = {
        "id": "RANK9SUMMONHOSTS5-RETURN244-INDEPENDENT-AUDIT",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size,
            "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size,
            "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": AUTHORITY,
        "acceptedIds": [],
        "heldIds": TARGETS,
        "blockers": BLOCKERS,
        "nextPendingGroup": NEXT,
        "checkCount": len(checks),
        "checksPassed": passed,
        "checksFailed": len(checks) - passed,
        "failedChecks": [c for c in checks if not c["passed"]],
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "id": "RANK9SUMMONHOSTS5-RETURN244-INDEPENDENT-AUDIT-RECEIPT",
        "status": report["status"],
        "archiveSHA256": archive_sha,
        "deliverySHA256": delivery_sha,
        "auditPath": REPORT.relative_to(ROOT).as_posix(),
        "checkCount": len(checks),
        "checksPassed": passed,
        "checksFailed": len(report["failedChecks"]),
        "acceptedIds": [],
        "heldIds": TARGETS,
        "authorityUnchanged": AUTHORITY,
        "nextPendingGroup": NEXT,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
