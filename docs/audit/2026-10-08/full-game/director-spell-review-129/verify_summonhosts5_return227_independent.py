from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_summonhosts5_return227_received"
ARCHIVE = RECEIVED / "DD_Rank9_SummonHosts3_Director_Return227.zip"
DELIVERY = RECEIVED / "DD_Rank9_SummonHosts3_Director_Return227_DELIVERY.json"
PACKET_DIR = AUDIT / "rank9_summonhosts5_current_source_227_prepared"
SOURCE_ARCHIVE = PACKET_DIR / "DD_Rank9_SummonHosts5_CurrentSource_227.zip"
SOURCE_DELIVERY = PACKET_DIR / "DD_Rank9_SummonHosts5_CurrentSource_227_DELIVERY.json"
SOURCE_CANDIDATE = PACKET_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_227.json"
REPORT = AUDIT / "RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9SUMMONHOSTS5_RETURN227_RECEIPT.json"
TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
BLOCKERS = {
    "summon-elemental-avatar": ["SH202-B01"],
    "summon-herald-of-the-planes": ["SH202-B02"],
    "summon-avatar-of-decay": ["SH202-B03"],
}
AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
NEXT = {"group": "rank9-impact-exile4", "pendingIds": ["reverse-gravity-field"]}
EXPECTED_COUNTS = {
    "cases": 28,
    "events": 3665,
    "forwardEventOperations": 7330,
    "inverseEventOperations": 7330,
    "proposalOperations": 12,
    "freshChecks": 107315,
    "freshCheckFailures": 0,
    "priorDemonstratedCases": 23,
    "wholeMainCasesHeld": 5,
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


def read_json(archive: zipfile.ZipFile, name: str) -> dict:
    return json.loads(archive.read(name).decode("utf-8-sig"))


def record(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    archive_size, archive_sha, archive_crc = file_digest(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = file_digest(DELIVERY)
    record(
        checks,
        "Return227 archive bytes, SHA-256 and CRC32 match the external delivery manifest",
        (archive_size, archive_sha, archive_crc)
        == (
            delivery["archive"]["bytes"],
            delivery["archive"]["sha256"],
            delivery["archive"]["crc32"].lower(),
        )
        and delivery["archive"]["path"] == ARCHIVE.name,
        {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc},
    )
    record(
        checks,
        "GPT delivery archive label discrepancy is nonsemantic and explicitly recorded",
        ARCHIVE.name == delivery["archive"]["path"]
        and "SummonHosts3" in ARCHIVE.name
        and delivery["id"] == "SH227-DELIVERY",
        {"returnedArchiveName": ARCHIVE.name, "deliveryId": delivery["id"], "scopeIds": delivery.get("heldIds")},
    )

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        unsafe = [
            name
            for name in names
            if name.startswith(("/", "\\"))
            or "\\" in name
            or PurePosixPath(name).is_absolute()
            or ".." in PurePosixPath(name).parts
        ]
        delivery_rows = {row["path"]: row for row in delivery["members"]}
        record(
            checks,
            "Return227 has 88 unique safe members and the delivery allowlist is exact",
            len(names) == len(set(names)) == len(delivery_rows) == delivery["memberCount"] == 88
            and set(names) == set(delivery_rows)
            and not unsafe
            and z.testzip() is None,
            {"archiveMembers": len(names), "deliveryMembers": len(delivery_rows), "unsafe": unsafe[:8]},
        )
        member_failures = []
        for name in names:
            got = member_digest(z, name)
            expected = delivery_rows[name]
            if got != (expected["bytes"], expected["sha256"], expected["crc32"].lower()):
                member_failures.append({"path": name, "actual": got, "expected": expected})
        record(
            checks,
            "Every archive member independently matches the external byte/SHA/CRC binding",
            not member_failures,
            {"checked": len(names), "failures": member_failures[:8]},
        )

        internal = read_json(z, "MEMBER_MANIFEST.json")
        inner_rows = {row["path"]: row for row in internal["members"]}
        inner_failures = []
        for name, row in inner_rows.items():
            got = member_digest(z, name)
            if got != (row["bytes"], row["sha256"], row["crc32"].lower()):
                inner_failures.append(name)
        record(
            checks,
            "Internal manifest binds every non-self member and its stated count",
            internal["memberCountExcludingSelf"] == 87
            and internal["archiveMemberCountIncludingSelf"] == 88
            and len(inner_rows) == 87
            and set(inner_rows) == set(names) - {"MEMBER_MANIFEST.json"}
            and not inner_failures,
            {"memberCount": len(inner_rows), "failures": inner_failures[:8]},
        )

        package = delivery["packageChecks"]
        record(
            checks,
            "Director-reported package checks are all passing",
            package["status"] == "PASS"
            and package["checkCount"] == 445
            and not package["failedChecks"]
            and len(package["checks"]) == 445
            and all(item.get("passed") is True for item in package["checks"]),
            {"checks": package["checkCount"], "failed": package["failedChecks"]},
        )

        decision = read_json(z, "DIRECTOR_DECISION.json")
        record(
            checks,
            "Director decision is scoped to exactly the three pending Summon Hosts identities and accepts/applies none",
            decision["id"] == "SH227-DIRECTOR-DECISION"
            and decision["scope"] == TARGETS
            and set(decision["decisions"]) == set(TARGETS)
            and decision["accepted"] is False
            and decision["applied"] is False
            and decision["acceptedIds"] == []
            and set(decision["heldIds"]) == set(TARGETS)
            and decision["authority"] == AUTHORITY
            and delivery["authority"] == AUTHORITY
            and delivery["accepted"] is False
            and delivery["applied"] is False
            and delivery["acceptedIds"] == []
            and set(delivery["heldIds"]) == set(TARGETS),
            {"scope": decision["scope"], "acceptedIds": decision["acceptedIds"], "heldIds": decision["heldIds"]},
        )
        exact_holds = (
            set(decision["decisions"]) == set(TARGETS)
            and set(delivery["decisions"]) == set(TARGETS)
            and all(
                decision["decisions"][spell]["accepted"] is False
                and decision["decisions"][spell]["applied"] is False
                and decision["decisions"][spell]["held"] is True
                and decision["decisions"][spell]["blockerIds"] == BLOCKERS[spell]
                and delivery["decisions"][spell]["accepted"] is False
                and delivery["decisions"][spell]["applied"] is False
                and delivery["decisions"][spell]["held"] is True
                and delivery["decisions"][spell]["blockerIds"] == BLOCKERS[spell]
                and decision["decisions"][spell]["procedureBytesUnchanged"] is True
                for spell in TARGETS
            )
        )
        record(
            checks,
            "Per-identity holds retain the exact Return202 blocker and unchanged procedure bytes",
            exact_holds,
            {spell: decision["decisions"][spell]["blockerIds"] for spell in TARGETS},
        )
        blocker_rows = {item["id"]: item for item in decision["blockers"]}
        record(
            checks,
            "Each carried blocker has an open source reassessment and explicit minimum missing witness",
            set(blocker_rows) == {value[0] for value in BLOCKERS.values()}
            and all(
                blocker_rows[blocker_id]["blocking"] is True
                and blocker_rows[blocker_id]["reassessment227"]["status"] == "OPEN"
                and bool(blocker_rows[blocker_id]["reassessment227"]["minimumMissingWitness"])
                for blocker_id in {value[0] for value in BLOCKERS.values()}
            ),
            {
                blocker_id: blocker_rows[blocker_id]["reassessment227"]["minimumMissingWitness"]
                for blocker_id in sorted(blocker_rows)
            },
        )

        counts = read_json(z, "COUNTS.json")
        replay = read_json(z, "CASE_REPLAY.json")
        clock = read_json(z, "CLOCK_AND_INVERSE_RESULTS.json")
        expected_counts_ok = all(counts[key] == value for key, value in EXPECTED_COUNTS.items())
        replay_counts_ok = (
            replay["counts"]["cases"] == len(replay["cases"]) == 28
            and replay["counts"]["events"] == clock["events"] == 3665
            and replay["counts"]["forwardOperations"] == clock["forwardOperations"] == 7330
            and replay["counts"]["inverseOperations"] == clock["inverseOperations"] == 7330
            and replay["counts"]["proposalOperations"] == clock["proposalOperations"] == 12
            and replay["counts"]["checks"] == counts["freshChecks"] == 107315
            and replay["counts"]["failures"] == []
            and clock["status"] == "PASS_REPRESENTED_HISTORIES"
            and clock["cases"] == clock["wholeCaseReverseChains"] == 28
            and clock["failures"] == []
            and replay["counts"]["caseStatuses"] == {"HELD_INCOMPLETE": 5, "DEMONSTRATED": 23}
            and replay["counts"]["sourceBindings"] == 238
            and replay["counts"]["sourceMembers"] == 323
        )
        record(
            checks,
            "Replay totals, clock/inverse operation totals, all 28 case reverse chains, and check failures reconcile",
            expected_counts_ok and replay_counts_ok,
            {
                "counts": {k: counts.get(k) for k in EXPECTED_COUNTS},
                "replay": replay["counts"],
                "clock": {k: clock.get(k) for k in ["status", "cases", "wholeCaseReverseChains", "events", "forwardOperations", "inverseOperations", "proposalOperations", "failures"]},
            },
        )

        case_failures = []
        case_files = set()
        for case in replay["cases"]:
            name = case["file"]
            case_files.add(name)
            timeline = case["timeline"]
            timeline_ok = (
                len(timeline) == case["events"]
                and case["events"] == case["forwardOperations"] // 2 == case["inverseOperations"] // 2
                and timeline[0]["beforeSHA256"] == case["initialSHA256"]
                and timeline[-1]["afterSHA256"] == case["finalSHA256"]
                and all(a["afterSHA256"] == b["beforeSHA256"] for a, b in zip(timeline, timeline[1:]))
                and all(len(event["beforeSHA256"]) == len(event["afterSHA256"]) == 64 for event in timeline)
                and case["replayPassed"] is True
                and case["checks"]["failures"] == []
            )
            if name not in names or member_digest(z, name) != (
                case["binding"]["bytes"],
                case["binding"]["sha256"],
                case["binding"]["crc32"].lower(),
            ) or not timeline_ok:
                case_failures.append(case["id"])
        record(
            checks,
            "All 28 case files match their bindings and every event hash timeline joins exactly",
            len(case_files) == 28 and not case_failures,
            {"uniqueCaseFiles": len(case_files), "failures": case_failures[:12]},
        )

        dispositions = read_json(z, "CASE_DISPOSITIONS.json")
        replay_by_id = {case["id"]: case for case in replay["cases"]}
        dispositions_ok = (
            len(dispositions["cases"]) == 28
            and {row["id"] for row in dispositions["cases"]} == set(replay_by_id)
            and all(
                row["replayPassed"] is True
                and row["identityAccepted"] is False
                and row["identityApplied"] is False
                and row["blockerIds"] == BLOCKERS[row["spellId"]]
                and row["priorStatusUnchanged"] == replay_by_id[row["id"]]["statusUnchanged"]
                for row in dispositions["cases"]
            )
        )
        record(
            checks,
            "All case dispositions preserve held identity status, exact blocker assignment, and prior case status",
            dispositions_ok,
            {"cases": len(dispositions["cases"]), "statusCounts": replay["counts"]["caseStatuses"]},
        )

        questions = read_json(z, "QUESTION_DISPOSITIONS.json")
        future = read_json(z, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        original = read_json(z, "source_context/ORIGINAL_32_QUESTIONS_2_ADDENDA_8_REQUIREMENTS.json")
        record(
            checks,
            "All 32 original questions, two focused addenda, and eight future requirements are preserved",
            counts["originalQuestionsPreserved"] == questions["originalQuestionsPreserved"] == 32
            and counts["focusedAddendaPreserved"] == questions["focusedAddendaPreserved"] == 2
            and counts["futureRequirementsPreserved"] == future["preservedCount"] == len(future["obligations"]) == 8
            and len(original["completeOriginalQuestionsUnchanged"]) == 32
            and len(original["focusedAdditionalQuestions"]) == 2
            and len(original["originalFutureCaseRequirementsUnchanged"]) == 8,
            {"questions": questions["originalQuestionsPreserved"], "addenda": questions["focusedAddendaPreserved"], "futureRequirements": future["preservedCount"]},
        )
        validation = read_json(z, "VALIDATION.json")
        summary = read_json(z, "AUDIT_SUMMARY.json")
        record(
            checks,
            "Data audit passes with zero failures while identities and all downstream gates remain closed",
            validation["status"] == "DATA_PASS_IDENTITIES_HELD"
            and validation["authority"] == AUTHORITY
            and validation["failedChecks"] == []
            and validation["suppliedProgramsExecuted"] is False
            and validation["runtimeExecuted"] is False
            and validation["canonicalChanges"] is False
            and summary["failures"] == []
            and summary["checks"] == 107315
            and summary["cases"] == 28
            and summary["events"] == 3665
            and summary["caseStatuses"] == {"HELD_INCOMPLETE": 5, "DEMONSTRATED": 23},
            {"status": validation["status"], "failedChecks": validation["failedChecks"], "runtimeExecuted": validation["runtimeExecuted"], "canonicalChanges": validation["canonicalChanges"]},
        )

        source_context = read_json(z, "SOURCE_BINDINGS.json")
        archived_candidate = read_json(z, "source_context/CURRENT_SOURCE_CONFERENCE_CANDIDATE_227.json")
        record(
            checks,
            "Return227 binds the exact submitted source packet and the prior Return202 archive",
            source_context["sourcePacket"]["bytes"] == 59700261
            and source_context["sourcePacket"]["sha256"] == "bbd2b1b3ac0bac990f6cb79847d79e8b50fe8e63938a2eb2919e04bca8107731"
            and source_context["priorReturn202Archive"]["sha256"] == "d341589888f7614165ebee21d5bbcd3e6f2ea6b194a09c1b19301300e0a7918b"
            and len(source_context["sourceBindings"]) == 238
            and archived_candidate["currentAuthority"] == AUTHORITY,
            {"sourcePacket": source_context["sourcePacket"], "priorReturn202Archive": source_context["priorReturn202Archive"], "sourceBindings": len(source_context["sourceBindings"])},
        )
        source_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
        source_size, source_sha, source_crc = file_digest(SOURCE_ARCHIVE)
        record(
            checks,
            "Submitted current-source ZIP/manifest remain byte-bound to the return",
            (source_size, source_sha, source_crc)
            == (
                delivery["sourcePacket"]["bytes"],
                delivery["sourcePacket"]["sha256"],
                delivery["sourcePacket"]["crc32"].lower(),
            )
            == (
                source_delivery["archive"]["bytes"],
                source_delivery["archive"]["sha256"],
                source_delivery["archive"]["crc32"].lower(),
            )
            and source_delivery["archive"]["sha256"] == source_sha,
            {"sourceBytes": source_size, "sourceSHA256": source_sha, "sourceCRC32": source_crc},
        )
        candidate = json.loads(SOURCE_CANDIDATE.read_text(encoding="utf-8-sig"))
        candidate_bindings = {row["path"]: row for row in candidate["sourceBindings"]}
        return_bindings = {row["path"]: row for row in source_context["sourceBindings"]}
        changed_bindings = sorted(
            path for path in set(candidate_bindings) | set(return_bindings)
            if candidate_bindings.get(path) != return_bindings.get(path)
        )
        local_binding_failures = []
        for path, row in candidate_bindings.items():
            file_path = ROOT / Path(path)
            if not file_path.is_file():
                local_binding_failures.append(path + ":missing")
                continue
            size, sha, _ = file_digest(file_path)
            if (size, sha) != (row["bytes"], row["sha256"]):
                local_binding_failures.append(path + ":hash")
        record(
            checks,
            "Return source binding rows equal the submitted candidate and current local bytes",
            len(candidate_bindings) == len(return_bindings) == 238
            and not changed_bindings
            and not local_binding_failures,
            {"sourceBindings": len(candidate_bindings), "changedRows": changed_bindings[:8], "localFailures": local_binding_failures[:8]},
        )

        queue = read_json(z, "source_context/CURRENT_SPELL_QUEUE_227.json")
        pending = read_json(z, "source_context/CURRENT37_PENDING_IDENTITY_AUDIT_227.json")
        next_in_queue = any(
            row.get("group") == NEXT["group"] and row.get("pendingIds") == NEXT["pendingIds"]
            for row in queue.get("currentPendingGroups", [])
        )
        next_is_pending = "reverse-gravity-field" in pending.get("pendingIds", [])
        record(
            checks,
            "Director next group exactly matches the next current-queue pending identity",
            decision["nextPendingGroup"] == delivery["nextPendingGroup"] == NEXT
            and next_in_queue
            and next_is_pending,
            {"nextPendingGroup": decision["nextPendingGroup"], "queueMatch": next_in_queue, "pending": next_is_pending},
        )

    passed = sum(check["passed"] for check in checks)
    report = {
        "id": "RANK9SUMMONHOSTS5-RETURN227-INDEPENDENT-AUDIT",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size, "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": AUTHORITY,
        "acceptedIds": [],
        "heldIds": TARGETS,
        "nextPendingGroup": NEXT,
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": [check for check in checks if not check["passed"]],
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "id": "RANK9SUMMONHOSTS5-RETURN227-INDEPENDENT-AUDIT-RECEIPT",
        "status": report["status"],
        "archiveSHA256": archive_sha,
        "deliverySHA256": delivery_sha,
        "auditPath": REPORT.relative_to(ROOT).as_posix(),
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(report["failedChecks"]),
        "acceptedIds": [],
        "heldIds": TARGETS,
        "authorityUnchanged": AUTHORITY,
        "nextPendingGroup": NEXT,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
