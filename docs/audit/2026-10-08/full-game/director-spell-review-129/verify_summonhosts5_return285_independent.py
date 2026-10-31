from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_summonhosts5_return285_received"
ARCHIVE = RECEIVED / "DD_Rank9_SummonHosts5_Director_Return285_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_summonhosts5_current_source_285_prepared"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_SummonHosts5_CurrentSource_285.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_SummonHosts5_CurrentSource_285_DELIVERY.json"
SOURCE_CANDIDATE = SOURCE_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json"
SOURCE_CONTEXT = SOURCE_DIR / "CURRENT_CONTEXT_285.json"
REQUEST = SOURCE_DIR / "REQUEST_285.txt"
SOURCE_AUDIT = BASE / "RANK9SUMMONHOSTS5_PACKET_285_INDEPENDENT_AUDIT.json"
SOURCE_RECEIPT = BASE / "RANK9SUMMONHOSTS5_PACKET_285_RECEIPT.json"
SOURCE_RECONCILIATION = BASE / "RANK9SUMMONHOSTS5_PACKET_285_AUDIT_RECONCILIATION.json"
REPORT = BASE / "RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9SUMMONHOSTS5_RETURN285_RECEIPT.json"

TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
BLOCKERS = {
    "summon-elemental-avatar": ["SH202-B01"],
    "summon-herald-of-the-planes": ["SH202-B02"],
    "summon-avatar-of-decay": ["SH202-B03"],
}
QUALIFICATIONS = [f"SH202-H{i:02d}" for i in range(1, 13)]
AUTHORITY = {
    "reviewedApplied": 816,
    "pending": 32,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 540,
    "scopedInterfaces": 173,
}
NEXT = {"group": "rank9-impact-exile4", "ids": ["reverse-gravity-field"], "blockerIds": ["IE204-B02"]}
INCOMPLETE = {
    "RANK9SUMMONHOSTS5129-SUMMON-AVATAR-OF-DECAY-A",
    "RANK9SUMMONHOSTS5129-SUMMON-AVATAR-OF-DECAY-B",
    "RANK9SUMMONHOSTS5129-SUMMON-ELEMENTAL-AVATAR-B",
    "RANK9SUMMONHOSTS5129-SUMMON-HERALD-OF-THE-PLANES-A",
    "RANK9SUMMONHOSTS5129-SUMMON-HERALD-OF-THE-PLANES-B",
}


def digest_bytes(data: bytes) -> tuple[int, str, str]:
    return len(data), hashlib.sha256(data).hexdigest(), f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def digest_file(path: Path) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return size, h.hexdigest(), f"{crc & 0xFFFFFFFF:08x}"


def digest_member(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
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
    archive_size, archive_sha, archive_crc = digest_file(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = digest_file(DELIVERY)
    record(checks, "Return285 archive matches the external byte, SHA-256 and CRC32 seal",
        (archive_size, archive_sha, archive_crc) == (
            delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower())
        and delivery["archive"]["path"] == ARCHIVE.name,
        {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc})
    record(checks, "External manifest binds current Packet285 and exact authority",
        delivery["id"] == "RANK9-SUMMONHOSTS5-DIRECTOR-RETURN285-DELIVERY"
        and delivery["authority"] == AUTHORITY
        and delivery["sourcePacket"]["path"] == SOURCE_ARCHIVE.name,
        {"id": delivery["id"], "authority": delivery["authority"], "sourcePacket": delivery["sourcePacket"]})

    source_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
    source_audit = json.loads(SOURCE_AUDIT.read_text(encoding="utf-8-sig"))
    source_receipt = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8-sig"))
    source_reconciliation = json.loads(SOURCE_RECONCILIATION.read_text(encoding="utf-8-sig"))
    source_size, source_sha, source_crc = digest_file(SOURCE_ARCHIVE)
    record(checks, "Packet285 source archive is independently audited and matches both seals",
        (source_size, source_sha, source_crc) == (
            delivery["sourcePacket"]["bytes"], delivery["sourcePacket"]["sha256"],
            delivery["sourcePacket"]["crc32"].lower())
        and (source_size, source_sha, source_crc) == (
            source_delivery["archive"]["bytes"], source_delivery["archive"]["sha256"],
            source_delivery["archive"]["crc32"].lower())
        and source_audit["status"] == "PASS"
        and source_receipt.get("status") == "PASS"
        and source_reconciliation["status"] == "PASS",
        {"sourceBytes": source_size, "sourceSHA256": source_sha, "audit": source_audit["status"],
         "receipt": source_receipt.get("status"), "reconciliation": source_reconciliation["status"]})
    sidecar_failures = []
    for local_path, member_name in [
        (SOURCE_DELIVERY, "source_context/DD_Rank9_SummonHosts5_CurrentSource_285_DELIVERY.json"),
        (SOURCE_CANDIDATE, "source_context/CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json"),
        (SOURCE_CONTEXT, "source_context/CURRENT_CONTEXT_285.json"),
        (REQUEST, "source_context/REQUEST_285.txt"),
    ]:
        if digest_file(local_path)[:2] != digest_bytes(zipfile.ZipFile(ARCHIVE).read(member_name))[:2]:
            sidecar_failures.append(local_path.name)
    record(checks, "Return285 preserves the exact submitted Packet285 sidecars",
        not sidecar_failures, {"mismatches": sidecar_failures})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        unsafe = [n for n in names if n.startswith(("/", "\\")) or "\\" in n
                  or PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts]
        external_rows = {row["path"]: row for row in delivery["members"]}
        record(checks, "107 archive members are unique, safe, and exactly allowlisted",
            len(names) == len(set(names)) == len(external_rows) == delivery["archiveMemberCount"] == 107
            and delivery["payloadMemberCount"] == 106 and set(names) == set(external_rows)
            and not unsafe and z.testzip() is None,
            {"members": len(names), "allowlist": len(external_rows), "unsafe": unsafe[:5]})
        external_failures = []
        for name in names:
            if digest_member(z, name) != (external_rows[name]["bytes"], external_rows[name]["sha256"],
                                           external_rows[name]["crc32"].lower()):
                external_failures.append(name)
        record(checks, "Every archive member matches the Director external manifest",
            not external_failures, {"checked": len(names), "failures": external_failures[:8]})

        internal = read_json(z, "MEMBER_MANIFEST.json")
        internal_rows = {row["path"]: row for row in internal["members"]}
        internal_failures = []
        for name, row in internal_rows.items():
            if digest_member(z, name) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                internal_failures.append(name)
        record(checks, "Internal manifest independently binds all 106 payload members",
            internal["id"] == "RANK9-SUMMONHOSTS5-DIRECTOR-RETURN285-MEMBER-MANIFEST"
            and internal["payloadMemberCount"] == 106 and len(internal_rows) == 106
            and set(internal_rows) == set(names) - {"MEMBER_MANIFEST.json"}
            and internal["excludedSelfOnly"] == "MEMBER_MANIFEST.json"
            and not internal_failures
            and internal["sourcePacket"]["sha256"] == source_sha
            and internal["authority"] == AUTHORITY
            and internal["acceptedIds"] == [] and internal["appliedIds"] == []
            and set(internal["heldIds"]) == set(TARGETS),
            {"payloadMembers": len(internal_rows), "failures": internal_failures[:8]})

        package = delivery["packageChecks"]
        record(checks, "All 646 sealed package checks passed",
            package["status"] == "PASS" and package["checks"] == 646 and package["failures"] == []
            and len(package["results"]) == 646 and all(r.get("pass") is True for r in package["results"]),
            {"status": package["status"], "checks": package["checks"], "failures": package["failures"]})

        decision = read_json(z, "DIRECTOR_DECISION.json")
        decision_rows = {row["id"]: row for row in decision["decisions"]}
        exact_scope = (decision["id"] == "RANK9-SUMMONHOSTS5-DIRECTOR-RETURN285"
            and decision["scope"] == TARGETS and set(decision_rows) == set(TARGETS)
            and decision["authority"] == AUTHORITY and decision["accepted"] is False
            and decision["applied"] is False and decision["acceptedIds"] == []
            and decision["appliedIds"] == [] and set(decision["heldIds"]) == set(TARGETS)
            and delivery["accepted"] is False and delivery["applied"] is False
            and delivery["acceptedIds"] == [] and delivery["appliedIds"] == []
            and set(delivery["heldIds"]) == set(TARGETS))
        record(checks, "Director decision holds only the three scoped identities and accepts/applies none",
            exact_scope, {"scope": decision["scope"], "heldIds": decision["heldIds"]})
        exact_holds = all(decision_rows[s]["accepted"] is False and decision_rows[s]["applied"] is False
            and decision_rows[s]["held"] is True and decision_rows[s]["status"] == "HELD_REQUIRED_WITNESSES"
            and decision_rows[s]["blockerIds"] == BLOCKERS[s]
            and bool(decision_rows[s]["minimumMissingWitness"])
            and bool(decision_rows[s].get("reassessment")) for s in TARGETS)
        record(checks, "Three exact blockers and their minimum missing witnesses are explicit",
            exact_holds and delivery["blockerIds"] == BLOCKERS,
            {s: {"blockers": decision_rows[s]["blockerIds"],
                 "minimumMissingWitness": decision_rows[s]["minimumMissingWitness"]} for s in TARGETS})
        blocker_rows = {row["id"]: row for row in decision["blockers"]}
        record(checks, "All blockers remain open and all twelve qualifications are retained",
            set(blocker_rows) == {b[0] for b in BLOCKERS.values()}
            and all(blocker_rows[b[0]]["blocking"] is True for b in BLOCKERS.values())
            and set(decision["conditionalQualificationIds"]) == set(QUALIFICATIONS)
            and set(delivery["conditionalQualificationIds"]) == set(QUALIFICATIONS),
            {"blockers": sorted(blocker_rows), "qualifications": decision["conditionalQualificationIds"]})

        counts = read_json(z, "COUNTS.json")
        validation = read_json(z, "VALIDATION.json")
        expected = {"procedures": 3, "sourceBindings": 280, "sourcePacketMembers": 428,
            "cases": 28, "mainCases": 6, "branches": 22, "events": 3665,
            "forwardOperations": 7330, "inverseOperations": 7330, "proposalOperations": 12,
            "actorEventRecords": 14556, "newCases": 0, "modifiedCases": 0,
            "incompleteMainCases": 5, "demonstratedComponentsRetained": 23,
            "blockers": 3, "conditionalQualifications": 12, "acceptedIds": 0,
            "appliedIds": 0, "heldIds": 3, "freshChecksBeforeSeal": 249474,
            "failedChecksBeforeSeal": 0}
        count_failures = {k: {"got": counts.get(k), "want": v} for k, v in expected.items()
                          if counts.get(k) != v}
        record(checks, "Counts and validation summary reconcile to the sealed 816/32 authority",
            not count_failures and validation["status"] == "PASS_STATIC_DATA_AND_REPLAY_WITH_SEMANTIC_HOLDS"
            and validation["counts"] == counts and validation["sourceVerificationPass"] is True
            and validation["allComponentReplaysPass"] is True
            and validation["completeWholeSpellWitnesses"] is False,
            {"countFailures": count_failures, "validation": validation["status"]})

        replay = read_json(z, "validation/CASE_REPLAY.json")
        replay_cases = replay["cases"]
        event_total = sum(c["events"] for c in replay_cases)
        forward_total = sum(c["forwardOperations"] for c in replay_cases)
        inverse_total = sum(c["inverseOperations"] for c in replay_cases)
        replay_incomplete = {c["id"] for c in replay_cases if c["statusPreserved"] == "HELD_INCOMPLETE"}
        record(checks, "All 28 case replays pass while the five incomplete main cases remain held",
            {c["spellId"] for c in replay_cases} == set(TARGETS) and len(replay_cases) == 28
            and all(c["replayPass"] is True for c in replay_cases)
            and event_total == replay["events"] == counts["events"] == 3665
            and forward_total == replay["forwardOperations"] == counts["forwardOperations"] == 7330
            and inverse_total == replay["inverseOperations"] == counts["inverseOperations"] == 7330
            and replay["fullReverseTraversals"] == 28
            and replay_incomplete == INCOMPLETE,
            {"cases": len(replay_cases), "events": event_total, "forward": forward_total,
             "inverse": inverse_total, "heldIncomplete": sorted(replay_incomplete)})
        dispositions = read_json(z, "CASE_DISPOSITIONS.json")
        disposition_rows = {row["id"]: row for row in dispositions["cases"]}
        replay_rows = {row["id"]: row for row in replay_cases}
        case_paths = {row["casePath"] for row in dispositions["cases"]}
        record(checks, "Every replay case has a matching held/demonstrated disposition and packaged case file",
            len(disposition_rows) == len(replay_rows) == 28
            and set(disposition_rows) == set(replay_rows)
            and case_paths <= set(names)
            and all(disposition_rows[i]["numericReplay"] == "PASS"
                and disposition_rows[i]["status"] == replay_rows[i]["statusPreserved"]
                for i in replay_rows),
            {"caseDispositions": len(disposition_rows), "caseFiles": len(case_paths)})

        source_bindings = read_json(z, "SOURCE_BINDINGS.json")
        candidate = read_json(z, "source_context/CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json")
        candidate_rows = {row["path"]: row for row in candidate["sourceBindings"]}
        return_rows = {row["path"]: row for row in source_bindings["rows"]}
        source_binding_matches = len(candidate_rows) == len(return_rows) == 280 and all(
            {k: candidate_rows[path].get(k) for k in ("path", "bytes", "sha256", "gitBlobSHA1")}
            == {k: return_rows[path].get(k) for k in ("path", "bytes", "sha256", "gitBlobSHA1")}
            and return_rows[path].get("archiveMember") == "sources_current/" + path
            and bool(return_rows[path].get("crc32"))
            for path in candidate_rows)
        record(checks, "All 280 source binding rows reconcile to the current candidate and Packet285",
            source_binding_matches
            and source_bindings["sourcePacket"]["sha256"] == source_sha
            and source_bindings["authority"] == AUTHORITY
            and source_bindings["scope"] == "Exact working-tree bytes; no substitution by HEAD-only checkout.",
            {"candidateRows": len(candidate_rows), "returnRows": len(return_rows)})
        prior_source_audit = read_json(z, "source_context/RANK9SUMMONHOSTS5_PACKET_285_INDEPENDENT_AUDIT.json")
        prior_source_receipt = read_json(z, "source_context/RANK9SUMMONHOSTS5_PACKET_285_RECEIPT.json")
        record(checks, "Embedded Packet285 audit and receipt retain their PASS state",
            prior_source_audit["status"] == "PASS" and prior_source_receipt.get("status") == "PASS"
            and digest_member(z, "source_context/RANK9SUMMONHOSTS5_PACKET_285_INDEPENDENT_AUDIT.json")[:2]
                == digest_file(SOURCE_AUDIT)[:2]
            and digest_member(z, "source_context/RANK9SUMMONHOSTS5_PACKET_285_RECEIPT.json")[:2]
                == digest_file(SOURCE_RECEIPT)[:2],
            {"audit": prior_source_audit["status"], "receipt": prior_source_receipt.get("status")})

        original = read_json(z, "ORIGINAL_OBLIGATIONS.json")
        questions = read_json(z, "QUESTION_DISPOSITIONS.json")
        future = read_json(z, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        qualifications = read_json(z, "QUALIFICATIONS.json")
        qualification_ids = {row["id"] for row in qualifications["qualifications"]}
        record(checks, "Original questions, addenda, future requirements, and all qualifications are preserved",
            len(original["sourceQuestions"]) == 32 and len(original["focusedAddenda"]) == 2
            and len(original["futureObligations"]) == 8
            and len(questions["dispositions"]) == 23
            and len(future["targetDispositions"]) == 6
            and qualification_ids == set(QUALIFICATIONS)
            and qualifications["noApplication"] is True
            and qualifications["noCanonicalEdits"] is True
            and qualifications["allDownstreamGatesClosed"] is True,
            {"sourceQuestions": len(original["sourceQuestions"]), "addenda": len(original["focusedAddenda"]),
             "requirements": len(original["futureObligations"]), "qualifications": sorted(qualification_ids)})
        holds = read_json(z, "HOLD_REGISTER.json")
        record(checks, "No prior accepted identities or unrelated holds are reopened",
            holds["closedReturn202Ids"] == ["conjure-magmatic-wyrm", "planar-army"]
            and len(holds["blockingRecords"]) == 3
            and len(holds["conditionalQualificationRecords"]) == 12,
            {"closedReturn202Ids": holds["closedReturn202Ids"],
             "blockingRecords": len(holds["blockingRecords"])})

        remaining = read_json(z, "REMAINING_QUEUE.json")
        context_queue = read_json(z, "context/CURRENT_SPELL_QUEUE_285.json")
        context_pending = read_json(z, "context/CURRENT32_PENDING_IDENTITY_AUDIT_285.json")
        norm_next = lambda value: {"group": value.get("group"), "ids": value.get("ids"),
                                   "blockerIds": value.get("blockerIds")}
        context_next = next((row for row in context_queue.get("currentPendingGroups", [])
            if row.get("group") == NEXT["group"] and row.get("pendingIds") == NEXT["ids"]), None)
        next_matches = (norm_next(decision["nextPendingGroup"]) == NEXT
            and norm_next(delivery["nextPendingGroup"]) == NEXT
            and norm_next(remaining["nextPendingGroup"]) == NEXT
            and context_next is not None
            and context_pending["authority"] == AUTHORITY
            and NEXT["ids"][0] in context_pending["pendingIds"]
            and NEXT["ids"][0] in remaining["pendingIds"])
        record(checks, "Director-selected next pending group matches the current queue",
            next_matches, {"next": remaining["nextPendingGroup"]})

    passed = sum(c["passed"] for c in checks)
    report = {
        "id": "RANK9SUMMONHOSTS5-RETURN285-INDEPENDENT-AUDIT",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size,
                    "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size,
                     "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": AUTHORITY,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockers": BLOCKERS,
        "nextPendingGroup": NEXT,
        "checksPassed": passed,
        "checksFailed": len(checks) - passed,
        "checks": checks,
        "semantics": "All director decisions are held; numerical replay and archive integrity do not close missing semantic witnesses. No canonical changes or application.",
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    receipt = {
        "id": "RANK9SUMMONHOSTS5-RETURN285-INDEPENDENT-AUDIT-RECEIPT",
        "audit": REPORT.name,
        "status": report["status"],
        "archiveSHA256": archive_sha,
        "deliverySHA256": delivery_sha,
        "checksPassed": passed,
        "checksFailed": len(checks) - passed,
        "authorityUnchanged": AUTHORITY,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "nextPendingGroup": NEXT,
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checksPassed": passed,
        "checksFailed": len(checks) - passed, "archiveSHA256": archive_sha,
        "deliverySHA256": delivery_sha, "report": str(REPORT), "receipt": str(RECEIPT)}, indent=2))
    if report["status"] != "PASS":
        for check in checks:
            if not check["passed"]:
                print("FAIL:", check["check"], json.dumps(check["detail"], ensure_ascii=False))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
