from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_impactexile4_return245_received"
ARCHIVE = RECEIVED / "DD_Rank9_ImpactExile1_Director_Return245_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile1_Director_Return245_DELIVERY.json"
SOURCE_PACKET = BASE / "rank9_impactexile4_current_source_245_prepared/DD_Rank9_ImpactExile4_CurrentSource_245.zip"
SOURCE_DELIVERY = BASE / "rank9_impactexile4_current_source_245_prepared/DD_Rank9_ImpactExile4_CurrentSource_245_DELIVERY.json"
PACKET_AUDIT = BASE / "RANK9IMPACTEXILE4_PACKET_245_INDEPENDENT_AUDIT.json"
PACKET_RECEIPT = BASE / "RANK9IMPACTEXILE4_PACKET_245_RECEIPT.json"
RETURN228 = BASE / "rank9_impactexile4_return228_received/DD_Rank9_ImpactExile1_Director_Return228.zip"
RETURN228_AUDIT = BASE / "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_245.json"
REPORT = BASE / "RANK9IMPACTEXILE4_RETURN245_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9IMPACTEXILE4_RETURN245_RECEIPT.json"

TARGET = "reverse-gravity-field"
AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
NEXT = {"group": "rank9-illusion-reality5", "pendingIds": ["soul-reflection"]}
CASE_MEMBERS = [
    "cases/RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-A.json",
    "cases/RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B.json",
    "cases/RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B__anchored.json",
    "cases/RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B__feather.json",
    "cases/RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B__overlap.json",
    "cases/RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B__ready-ray-concentration.json",
]
EXPECTED_SUMMON_HOLDS = {
    "summon-elemental-avatar": ["SH202-B01"],
    "summon-herald-of-the-planes": ["SH202-B02"],
    "summon-avatar-of-decay": ["SH202-B03"],
}


def digest(path: Path) -> tuple[int, str, str]:
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def archive_json(archive: zipfile.ZipFile, name: str) -> dict:
    return json.loads(archive.read(name).decode("utf-8-sig"))


def add(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery = read_json(DELIVERY)
    size, sha, crc = digest(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = digest(DELIVERY)
    expected_archive = delivery["archive"]
    add(
        checks,
        "Downloaded Return245 ZIP matches its external size, SHA-256, CRC32 and filename",
        (size, sha, crc)
        == (expected_archive["bytes"], expected_archive["sha256"], expected_archive["crc32"].lower())
        and delivery["filename"] == ARCHIVE.name == expected_archive["filename"],
        {"bytes": size, "sha256": sha, "crc32": crc, "filename": ARCHIVE.name},
    )

    source_size, source_sha, source_crc = digest(SOURCE_PACKET)
    source_manifest = read_json(SOURCE_DELIVERY)
    source_binding = delivery["externalSourceArchive"]
    add(
        checks,
        "Return245 binds the exact locally prepared and independently audited Packet245 source archive",
        source_binding["filename"] == SOURCE_PACKET.name
        and (source_binding["bytes"], source_binding["sha256"], source_binding["crc32"].lower())
        == (source_size, source_sha, source_crc)
        and source_manifest["archive"]["sha256"] == source_sha,
        {"sourceBytes": source_size, "sourceSha256": source_sha, "sourceCrc32": source_crc},
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
            "Archive has 58 unique safe members exactly matching the delivery allowlist",
            len(names) == len(set(names)) == len(external_rows) == delivery["memberCount"] == 58
            and set(names) == set(delivery["exactAllowlist"]) == set(external_rows)
            and not unsafe
            and z.testzip() is None,
            {"members": len(names), "unsafe": unsafe[:8]},
        )

        member_failures = [
            name
            for name, row in external_rows.items()
            if member_digest(z, name)
            != (row["bytes"], row["sha256"], row["crc32"].lower())
        ]
        add(
            checks,
            "Every returned member independently matches the external delivery size/hash/CRC",
            not member_failures,
            {"checked": len(external_rows), "failures": member_failures[:12]},
        )

        internal = archive_json(z, "MEMBER_MANIFEST.json")
        internal_rows = {row["path"]: row for row in internal["members"]}
        payload_names = set(names) - {"MEMBER_MANIFEST.json"}
        self_binding = external_rows["MEMBER_MANIFEST.json"]
        add(
            checks,
            "Internal exact-member manifest and its external self-binding reconcile",
            internal["id"] == "RETURN245-EXACT-PAYLOAD-MANIFEST"
            and internal["memberCountExcludingSelf"] == 57
            and set(internal_rows) == payload_names
            and len(internal_rows) == 57
            and internal["authority"] == AUTHORITY
            and internal["heldIds"] == [TARGET]
            and (self_binding["bytes"], self_binding["sha256"], self_binding["crc32"].lower())
            == member_digest(z, "MEMBER_MANIFEST.json")
            and internal["sourcePacketExternalBinding"] == source_binding,
            {"payloadMembers": len(internal_rows), "manifestSelfBinding": self_binding},
        )
        internal_failures = [
            name
            for name, row in internal_rows.items()
            if member_digest(z, name) != (row["bytes"], row["sha256"], row["crc32"].lower())
        ]
        add(
            checks,
            "Every payload member independently matches the internal manifest",
            not internal_failures,
            {"checked": len(internal_rows), "failures": internal_failures[:12]},
        )

        decision = archive_json(z, "DIRECTOR_DECISION.json")
        counts = archive_json(z, "COUNTS.json")
        replay = archive_json(z, "CASE_REPLAY.json")
        data_check = archive_json(z, "DATA_INTEGRITY_CHECK.json")
        semantic = archive_json(z, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        holds = archive_json(z, "HOLD_REGISTER.json")
        next_group = archive_json(z, "NEXT_PENDING_GROUP.json")
        validation = archive_json(z, "VALIDATION.json")

        add(
            checks,
            "External and internal rulings are held only on reverse-gravity-field at unchanged authority",
            delivery["id"] == "RETURN245-DELIVERY"
            and delivery["authority"] == AUTHORITY
            and delivery["accepted"] is False
            and delivery["applied"] is False
            and delivery["acceptedIds"] == []
            and delivery["appliedIds"] == []
            and delivery["heldIds"] == [TARGET]
            and delivery["blockerIds"] == ["IE204-B02"]
            and decision["scope"] == [TARGET]
            and decision["acceptedIds"] == []
            and decision["appliedIds"] == []
            and decision["heldIds"] == [TARGET]
            and decision["authority"] == AUTHORITY
            and decision["perIdentity"][0]["spellId"] == TARGET
            and decision["perIdentity"][0]["blockerIds"] == ["IE204-B02"],
            {"heldIds": delivery["heldIds"], "blockers": delivery["blockerIds"], "authority": delivery["authority"]},
        )
        witness_text = " ".join(decision["perIdentity"][0]["minimumMissingWitnesses"]).lower()
        add(
            checks,
            "IE204-B02 retains both minimum physical witnesses without inventing object or tether rules",
            len(decision["perIdentity"][0]["minimumMissingWitnesses"]) == 2
            and "20lb" in witness_text
            and "60ft/120ft" in witness_text
            and "tether/anchor" in witness_text
            and semantic["acceptanceResult"] == "HELD"
            and semantic["blockers"][0]["id"] == "IE204-B02"
            and semantic["blockers"][0]["noInventedObjectHPOrSalvage"] is True,
            decision["perIdentity"][0]["minimumMissingWitnesses"],
        )

        case_rows = replay["cases"]
        case_ok = (
            replay["scope"] == [TARGET]
            and replay["freshReplay"] is True
            and replay["runtimeExecuted"] is False
            and len(case_rows) == 6
            and all(row["replayPassed"] if "replayPassed" in row else row.get("fullStateReplay") == "PASS" for row in case_rows)
            and sum(row["events"] for row in case_rows) == 224
            and sum(row["forwardOperations"] for row in case_rows) == 448
            and sum(row["inverseOperations"] for row in case_rows) == 448
            and sum(row.get("wholeCaseComplete", row.get("completePositiveSpellWitness", False)) is True for row in case_rows) == 1
            and sum(row.get("wholeCaseComplete", row.get("completePositiveSpellWitness", False)) is False for row in case_rows) == 5
        )
        add(
            checks,
            "Six preserved cases replay with 224 events, 448 forward and 448 inverse operations; one complete and five incomplete",
            case_ok
            and counts["targetCasesReplayed"] == 6
            and counts["incompleteTargetCases"] == 5
            and counts["completeCreatureOnlyConditionalCases"] == 1
            and counts["eventOperations"] == 896,
            {"cases": len(case_rows), "events": 224, "forward": 448, "inverse": 448},
        )

        with zipfile.ZipFile(RETURN228) as prior:
            exact_case_mirrors = all(z.read(name) == prior.read(name) for name in CASE_MEMBERS)
        add(
            checks,
            "All six case files are byte-exact to the previously audited Return228 set",
            exact_case_mirrors and read_json(RETURN228_AUDIT)["status"] == "PASS",
            {"cases": CASE_MEMBERS, "priorAudit": "PASS"},
        )

    # The prior check is asserted outside ZIP parsing to keep counts independently reconciled.
    with zipfile.ZipFile(ARCHIVE) as z:
        data_check = archive_json(z, "DATA_INTEGRITY_CHECK.json")
        add(
            checks,
            "All 14,610 fresh source/data checks pass and all 240 sealed package checks pass",
            data_check["status"] == "PASS"
            and data_check["checkCount"] == 14610
            and len(data_check["failures"]) == 0
            and all(row["passed"] is True for row in data_check["checks"])
            and delivery["counts"]["freshAuditChecks"] == delivery["counts"]["freshAuditPassed"] == 14610
            and delivery["counts"]["freshAuditFailures"] == 0
            and delivery["packageChecks"]["status"] == "PASS"
            and delivery["packageChecks"]["checkCount"] == delivery["packageChecks"]["passed"] == 240
            and delivery["packageChecks"]["failed"] == 0
            and all(row["passed"] is True for row in delivery["packageChecks"]["checks"]),
            {"freshAuditChecks": data_check["checkCount"], "packageChecks": delivery["packageChecks"]["checkCount"]},
        )

    queue = read_json(QUEUE)
    groups = queue["currentPendingGroups"]
    pos = next(i for i, row in enumerate(groups) if row["group"] == "rank9-impact-exile4")
    queue_next = groups[pos + 1]
    delivered_next = {
        "group": delivery["nextPendingGroup"]["group"],
        "pendingIds": delivery["nextPendingGroup"]["pendingIds"],
    }
    artifact_next = {"group": next_group["group"], "pendingIds": next_group["pendingIds"]}
    add(
        checks,
        "Return245 next group matches the next group in current queue245",
        delivered_next == artifact_next == NEXT
        and queue_next["group"] == NEXT["group"]
        and queue_next["pendingIds"] == NEXT["pendingIds"],
        {"return": delivered_next, "queue": {"group": queue_next["group"], "pendingIds": queue_next["pendingIds"]},
         "returnQueuePath": delivery["nextPendingGroup"].get("queuePath")},
    )

    summons = next(row for row in holds["unrelatedCurrentHolds"] if row["group"] == "rank9-summon-hosts5")
    add(
        checks,
        "Return244 Summon/Hosts holds stay outside scope and unchanged",
        summons["pendingIds"] == list(EXPECTED_SUMMON_HOLDS)
        and summons["blockingReturn"]["blockers"] == EXPECTED_SUMMON_HOLDS,
        summons["blockingReturn"]["blockers"],
    )
    add(
        checks,
        "Downstream review, implementation, runtime, play, balance and release gates remain closed",
        delivery["accepted"] is False
        and delivery["applied"] is False
        and delivery["canonicalChanges"] is False
        and delivery["githubChanges"] is False
        and delivery["sourceArchiveNotRepackaged"] is True
        and validation["runtimeExecuted"] is False
        and validation["suppliedProgramsExecuted"] is False
        and "HELD" in validation["status"],
        {"qualification": delivery["qualification"], "validation": validation["status"]},
    )

    # Reconcile the returned archived manifest's source binding to the exact source packet record.
    required_source_context = {
        "source_context/RANK9IMPACTEXILE4_PACKET_245_INDEPENDENT_AUDIT.json",
        "source_context/RANK9IMPACTEXILE4_PACKET_245_RECEIPT.json",
        "source_context/DD_Rank9_ImpactExile4_CurrentSource_245_DELIVERY.json",
    }
    with zipfile.ZipFile(ARCHIVE) as returned_archive:
        returned_members = set(returned_archive.namelist())
        source_context_bytes_match = (
            returned_archive.read("source_context/RANK9IMPACTEXILE4_PACKET_245_INDEPENDENT_AUDIT.json")
            == PACKET_AUDIT.read_bytes()
            and returned_archive.read("source_context/RANK9IMPACTEXILE4_PACKET_245_RECEIPT.json")
            == PACKET_RECEIPT.read_bytes()
            and returned_archive.read("source_context/DD_Rank9_ImpactExile4_CurrentSource_245_DELIVERY.json")
            == SOURCE_DELIVERY.read_bytes()
        )
    add(
        checks,
        "Return archive contains the Packet245 audit, receipt and delivery context",
        required_source_context <= returned_members
        and source_context_bytes_match
        and delivery["externalSourceArchive"]["sha256"] == digest(SOURCE_PACKET)[1],
        sorted(required_source_context),
    )

    passed = sum(row["passed"] for row in checks)
    report = {
        "id": "RANK9IMPACTEXILE4-RETURN245-INDEPENDENT-AUDIT",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": size, "sha256": sha, "crc32": crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size,
                     "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": delivery["authority"],
        "targetIds": [TARGET],
        "acceptedIds": delivery["acceptedIds"],
        "appliedIds": delivery["appliedIds"],
        "heldIds": delivery["heldIds"],
        "blockerIds": delivery["blockerIds"],
        "counts": delivery["counts"],
        "nextPendingGroup": NEXT,
        "filenameLabelAnomaly": "Archive label says ImpactExile1 while target/current source group is ImpactExile4; bytes, manifest, source binding and all member content are self-consistent.",
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(checks) - passed,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_size, report_sha, report_crc = digest(REPORT)
    receipt = {
        "id": "RANK9IMPACTEXILE4-RETURN245-RECEIPT",
        "status": report["status"],
        "archive": report["archive"],
        "delivery": report["delivery"],
        "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), "bytes": report_size,
                             "sha256": report_sha, "crc32": report_crc},
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(checks) - passed,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(checks) - passed,
        "archiveSha256": sha,
        "deliverySha256": delivery_sha,
        "report": str(REPORT),
        "receipt": str(RECEIPT),
        "failures": [row for row in checks if not row["passed"]],
    }, indent=2))
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
