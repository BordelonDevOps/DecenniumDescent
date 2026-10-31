from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_impactexile4_return228_received"
ARCHIVE = RECEIVED / "DD_Rank9_ImpactExile1_Director_Return228.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json"
SOURCE_PACKET = AUDIT / "rank9_impactexile4_current_source_228_prepared/DD_Rank9_ImpactExile4_CurrentSource_228.zip"
PACKET_RECORD = AUDIT / "RANK9IMPACTEXILE4_PACKET_228.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_228.json"
REPORT = AUDIT / "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9IMPACTEXILE4_RETURN228_RECEIPT.json"

AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
TARGET = "reverse-gravity-field"
NEXT = {"group": "rank9-illusion-reality5", "pendingIds": ["soul-reflection"]}
CLOSED = ["eternal-anvil", "transmute-flesh-to-energy", "planar-collapse"]
OUTSIDE_HOLDS = {
    "summon-elemental-avatar": ["SH202-B01"],
    "summon-herald-of-the-planes": ["SH202-B02"],
    "summon-avatar-of-decay": ["SH202-B03"],
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


def add(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    archive_bytes, archive_sha, archive_crc = file_digest(ARCHIVE)
    delivery_bytes, delivery_sha, delivery_crc = file_digest(DELIVERY)
    add(
        checks,
        "Return228 ZIP bytes, SHA-256 and CRC32 match the external delivery manifest",
        (archive_bytes, archive_sha, archive_crc)
        == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower())
        and delivery["archive"]["path"] == ARCHIVE.name,
        {"bytes": archive_bytes, "sha256": archive_sha, "crc32": archive_crc},
    )

    packet_record = json.loads(PACKET_RECORD.read_text(encoding="utf-8-sig"))
    source_packet_bytes, source_packet_sha, source_packet_crc = file_digest(SOURCE_PACKET)
    add(
        checks,
        "Return228 binds the exact independently audited current-source packet",
        delivery["sourcePacket"]["bytes"] == source_packet_bytes
        and delivery["sourcePacket"]["sha256"] == source_packet_sha
        and delivery["sourcePacket"]["crc32"].lower() == source_packet_crc
        and packet_record["archive"]["sha256"] == source_packet_sha,
        {"sourcePacketBytes": source_packet_bytes, "sourcePacketSha256": source_packet_sha},
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
        external_rows = {row["path"]: row for row in delivery["members"]}
        add(
            checks,
            "Archive has unique safe members and exactly matches the delivery allowlist",
            len(names) == len(set(names)) == len(external_rows) == delivery["exactArchiveMemberCount"]
            and set(names) == set(external_rows)
            and not unsafe
            and z.testzip() is None,
            {"archiveMembers": len(names), "deliveryMembers": len(external_rows), "unsafe": unsafe[:8]},
        )

        member_failures = []
        for name, row in external_rows.items():
            if (member_digest(z, name)) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                member_failures.append(name)
        add(
            checks,
            "Every archive member independently matches external delivery bytes/SHA/CRC",
            not member_failures,
            {"checked": len(external_rows), "failures": member_failures[:12]},
        )

        internal_manifest = read_json(z, "MANIFEST.json")
        internal_rows = {row["path"]: row for row in internal_manifest["members"]}
        manifest_names = set(names) - {"MANIFEST.json"}
        add(
            checks,
            "Internal exact-member manifest matches all non-self members and its external self-binding",
            set(internal_rows) == manifest_names
            and len(internal_rows) == delivery["payloadMemberCountExcludingManifest"]
            and internal_manifest["memberCountExcludingSelf"] == len(internal_rows)
            and external_rows["MANIFEST.json"]["sha256"] == delivery["memberManifest"]["sha256"]
            and member_digest(z, "MANIFEST.json")
            == (
                delivery["memberManifest"]["bytes"],
                delivery["memberManifest"]["sha256"],
                delivery["memberManifest"]["crc32"].lower(),
            ),
            {"internalRows": len(internal_rows), "payloadCount": delivery["payloadMemberCountExcludingManifest"]},
        )
        inner_failures = []
        for name, row in internal_rows.items():
            if member_digest(z, name) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                inner_failures.append(name)
        add(
            checks,
            "Every non-self member independently matches the internal exact-member manifest",
            not inner_failures,
            {"checked": len(internal_rows), "failures": inner_failures[:12]},
        )

        decision = read_json(z, "DIRECTOR_DECISION.json")
        counts = read_json(z, "COUNTS.json")
        replay = read_json(z, "CASE_REPLAY.json")
        dispositions = read_json(z, "CASE_DISPOSITIONS.json")
        semantic = read_json(z, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        hold_register = read_json(z, "HOLD_REGISTER.json")
        next_group = read_json(z, "NEXT_PENDING_GROUP.json")
        reassessment = read_json(z, "SOURCE_REASSESSMENT.json")

    add(
        checks,
        "External and internal decisions are scoped only to reverse-gravity-field and preserve authority",
        delivery["id"] == "RANK9-IMPACT-EXILE1-RETURN228-DELIVERY"
        and delivery["authority"] == AUTHORITY
        and delivery["accepted"] is False
        and delivery["applied"] is False
        and delivery["acceptedIds"] == []
        and delivery["appliedIds"] == []
        and delivery["heldIds"] == [TARGET]
        and delivery["blockerIds"] == ["IE204-B02"]
        and decision["scope"] == [TARGET]
        and decision["authorityBefore"] == AUTHORITY
        and decision["authorityAfter"] == AUTHORITY,
        {"authority": delivery["authority"], "heldIds": delivery["heldIds"], "blockers": delivery["blockerIds"]},
    )
    identity = decision["perIdentity"][0]
    add(
        checks,
        "Per-identity ruling retains IE204-B02 with both minimum missing witnesses",
        identity["spellId"] == TARGET
        and identity["accepted"] is False
        and identity["applied"] is False
        and identity["held"] is True
        and identity["blockerIds"] == ["IE204-B02"]
        and len(identity["minimumMissingWitnesses"]) == 2
        and semantic["acceptanceGateFailures"][0]["id"] == "IE204-B02"
        and reassessment["blocker"]["id"] == "IE204-B02",
        {"minimumMissingWitnesses": identity["minimumMissingWitnesses"]},
    )

    add(
        checks,
        "Case replay contains six successful replays, one complete case and five retained incomplete cases",
        replay["summary"]["cases"] == 6
        and replay["summary"]["completeCases"] == 1
        and replay["summary"]["incompleteCases"] == 5
        and replay["summary"]["failures"] == []
        and sum(row["wholeCaseComplete"] is True for row in replay["cases"]) == 1
        and sum(row["wholeCaseComplete"] is False for row in replay["cases"]) == 5
        and all(row["replayPassed"] is True for row in replay["cases"])
        and counts["cases"] == 6
        and dispositions["incompleteCaseCount"] == 5,
        {"summary": replay["summary"], "caseStatuses": [(row["id"], row["wholeCaseComplete"]) for row in replay["cases"]]},
    )
    add(
        checks,
        "Case replay events and forward/inverse operation totals reconcile independently",
        sum(row["events"] for row in replay["cases"]) == 224
        and sum(row["forwardOperations"] for row in replay["cases"]) == 448
        and sum(row["inverseOperations"] for row in replay["cases"]) == 448
        and replay["summary"]["events"] == 224
        and replay["summary"]["forwardOperations"] == 448
        and replay["summary"]["inverseOperations"] == 448
        and counts["events"] == 224
        and counts["forwardOperations"] == 448
        and counts["inverseOperations"] == 448,
        {"events": 224, "forward": 448, "inverse": 448},
    )
    add(
        checks,
        "Data/source/clock replay and semantic/package checks report no failures",
        replay["summary"]["checkCount"] == 10477
        and replay["summary"]["failures"] == []
        and delivery["counts"]["dataSourceClockIntegrityChecks"] == 10477
        and delivery["packageChecks"]["count"] == delivery["packageChecks"]["passed"] == 270
        and delivery["packageChecks"]["failed"] == 0
        and all(row["passed"] is True for row in delivery["packageChecks"]["checks"]),
        {"dataSourceClockIntegrityChecks": 10477, "packageChecks": delivery["packageChecks"]["count"]},
    )

    closed = semantic["closedAcceptedIdsNotReassessed"]
    retained_holds = hold_register.get("Return227Unchanged", {})
    add(
        checks,
        "Previously accepted identities stay closed and all Return227 holds remain unchanged",
        all(spell_id in closed for spell_id in CLOSED) and retained_holds == OUTSIDE_HOLDS,
        {"closedAcceptedIds": closed, "Return227Unchanged": retained_holds},
    )
    qualifications = decision["qualifications"]
    add(
        checks,
        "Application, canonical, GitHub and downstream approval gates remain closed",
        all(
            qualifications.get(key) is False
            for key in (
                "applied", "canonicalFilesEdited", "githubChanged", "runtimeApproved", "gameExecuted",
                "sourceProgramsExecuted", "historicalProgramsExecuted", "implementationApproved",
                "humanPlaytested", "balanceApproved", "cosmologyApproved", "domainClosure",
                "completionClaim", "releaseApproved",
            )
        ),
        qualifications,
    )

    next_info = {"group": next_group["nextGroup"], "pendingIds": next_group["pendingIds"]}
    queue = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
    current_groups = queue["currentPendingGroups"]
    target_position = next(i for i, row in enumerate(current_groups) if row["group"] == "rank9-impact-exile4")
    queue_next = current_groups[target_position + 1]
    add(
        checks,
        "Return's next pending group agrees with the exact current queue order",
        next_info == NEXT
        and delivery["nextPendingGroup"] == NEXT["group"]
        and delivery["nextPendingIds"] == NEXT["pendingIds"]
        and queue_next["group"] == NEXT["group"]
        and queue_next["pendingIds"] == NEXT["pendingIds"],
        {"return": next_info, "queueNext": {"group": queue_next["group"], "pendingIds": queue_next["pendingIds"]}},
    )

    passed = sum(item["passed"] for item in checks)
    report = {
        "id": "RANK9IMPACTEXILE4-RETURN228-INDEPENDENT-AUDIT",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": str(ARCHIVE.relative_to(ROOT)).replace("\\", "/"), "bytes": archive_bytes, "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": str(DELIVERY.relative_to(ROOT)).replace("\\", "/"), "bytes": delivery_bytes, "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": delivery["authority"],
        "targetIds": [TARGET],
        "acceptedIds": delivery["acceptedIds"],
        "appliedIds": delivery["appliedIds"],
        "heldIds": delivery["heldIds"],
        "blockerIds": delivery["blockerIds"],
        "counts": delivery["counts"],
        "nextPendingGroup": NEXT,
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(checks) - passed,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_bytes, report_sha, report_crc = file_digest(REPORT)
    receipt = {
        "id": "RANK9IMPACTEXILE4-RETURN228-RECEIPT",
        "status": report["status"],
        "archive": {"path": report["archive"]["path"], "bytes": archive_bytes, "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": report["delivery"]["path"], "bytes": delivery_bytes, "sha256": delivery_sha, "crc32": delivery_crc},
        "independentAudit": {"path": str(REPORT.relative_to(ROOT)).replace("\\", "/"), "bytes": report_bytes, "sha256": report_sha, "crc32": report_crc},
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(checks) - passed,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": passed, "failedChecks": len(checks) - passed, "report": str(REPORT), "receipt": str(RECEIPT)}, indent=2))
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
