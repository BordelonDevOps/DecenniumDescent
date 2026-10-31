from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_impactexile4_return286_received"
ARCHIVE = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return286_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json"
SOURCE_PACKET = BASE / "rank9_impactexile4_current_source_286_prepared/DD_Rank9_ImpactExile4_CurrentSource_286.zip"
SOURCE_DELIVERY = BASE / "rank9_impactexile4_current_source_286_prepared/DD_Rank9_ImpactExile4_CurrentSource_286_DELIVERY.json"
PACKET_AUDIT = BASE / "RANK9IMPACTEXILE4_PACKET_286_INDEPENDENT_AUDIT.json"
PACKET_RECEIPT = BASE / "RANK9IMPACTEXILE4_PACKET_286_RECEIPT.json"
RETURN228 = BASE / "rank9_impactexile4_return228_received/DD_Rank9_ImpactExile1_Director_Return228.zip"
RETURN228_AUDIT = BASE / "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json"
RETURN285 = BASE / "rank9_summonhosts5_return285_received/DD_Rank9_SummonHosts5_Director_Return285_HELD.zip"
RETURN285_AUDIT = BASE / "RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json"
RETURN285_DELIVERY = BASE / "rank9_summonhosts5_return285_received/DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_286.json"
REPORT = BASE / "RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9IMPACTEXILE4_RETURN286_RECEIPT.json"

TARGET = "reverse-gravity-field"
AUTHORITY = {
    "reviewedApplied": 816,
    "pending": 32,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 540,
    "scopedInterfaces": 173,
}
NEXT = {
    "group": "rank9-alignment-faction-purification5",
    "pendingIds": [
        "alignment-ascension",
        "alignment-perfection",
        "faction-incarnate",
        "faction-perfection",
        "corruption-purification",
    ],
}
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
        "Downloaded Return286 ZIP matches external size, SHA-256, CRC32 and filename",
        (size, sha, crc)
        == (expected_archive["bytes"], expected_archive["sha256"], expected_archive["crc32"].lower())
        and expected_archive["filename"] == ARCHIVE.name,
        {"bytes": size, "sha256": sha, "crc32": crc, "filename": ARCHIVE.name},
    )

    source_size, source_sha, source_crc = digest(SOURCE_PACKET)
    source_manifest = read_json(SOURCE_DELIVERY)
    source_audit = read_json(PACKET_AUDIT)
    source_receipt = read_json(PACKET_RECEIPT)
    source_binding = delivery["sourcePacket"]
    add(
        checks,
        "Return286 binds the exact locally prepared, independently audited Packet286 archive",
        source_binding["filename"] == SOURCE_PACKET.name
        and (source_binding["bytes"], source_binding["sha256"], source_binding["crc32"].lower())
        == (source_size, source_sha, source_crc)
        and source_manifest["archive"]["sha256"] == source_sha
        and source_audit["status"] == source_receipt["status"] == "PASS"
        and source_audit["checkCount"] == source_audit["passedChecks"] == 16
        and source_audit["failedChecks"] == []
        and source_receipt["status"] == "PASS"
        and source_receipt["failedChecks"] == 0,
        {"sourceBytes": source_size, "sourceSha256": source_sha, "sourceCrc32": source_crc,
         "packetAudit": source_audit["status"], "packetChecks": source_audit["checkCount"]},
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
            "Archive has 80 unique safe members matching the delivery member allowlist",
            len(names) == len(set(names)) == len(external_rows) == delivery["memberCount"] == 80
            and set(names) == set(external_rows)
            and not unsafe
            and z.testzip() is None,
            {"members": len(names), "unsafe": unsafe[:8]},
        )
        external_failures = [
            name
            for name, row in external_rows.items()
            if member_digest(z, name)
            != (row["bytes"], row["sha256"], row["crc32"].lower())
        ]
        add(
            checks,
            "Every archive member independently matches the external size/hash/CRC manifest",
            not external_failures,
            {"checked": len(external_rows), "failures": external_failures[:12]},
        )

        internal = archive_json(z, "MEMBER_MANIFEST.json")
        internal_rows = {row["path"]: row for row in internal["members"]}
        payload_names = set(names) - {"MEMBER_MANIFEST.json"}
        self_binding = external_rows["MEMBER_MANIFEST.json"]
        add(
            checks,
            "Internal exact-member manifest and external self-binding reconcile",
            internal["id"] == "RANK9-IMPACTEXILE4-RETURN286-MEMBER-MANIFEST"
            and internal["memberCountExcludingSelf"] == 79
            and set(internal_rows) == payload_names
            and len(internal_rows) == 79
            and internal["authority"] == AUTHORITY
            and internal["acceptedIds"] == []
            and internal["appliedIds"] == []
            and internal["heldIds"] == [TARGET]
            and (self_binding["bytes"], self_binding["sha256"], self_binding["crc32"].lower())
            == member_digest(z, "MEMBER_MANIFEST.json"),
            {"payloadMembers": len(internal_rows), "manifestSelfBinding": self_binding},
        )
        internal_failures = [
            name
            for name, row in internal_rows.items()
            if member_digest(z, name)
            != (row["bytes"], row["sha256"], row["crc32"].lower())
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
        semantic = archive_json(z, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        holds = archive_json(z, "HOLD_REGISTER.json")
        next_group = archive_json(z, "NEXT_PENDING_GROUP.json")
        qualifications = archive_json(z, "QUALIFICATIONS.json")
        validation = archive_json(z, "VALIDATION.json")
        case_dispositions = archive_json(z, "CASE_DISPOSITIONS.json")
        source_bindings = archive_json(z, "SOURCE_BINDINGS.json")

        per_identity = decision["perIdentity"][0]
        add(
            checks,
            "External and internal rulings hold only reverse-gravity-field at unchanged authority",
            delivery["id"] == "RANK9-IMPACTEXILE4-DIRECTOR-RETURN286-DELIVERY"
            and delivery["authority"] == AUTHORITY
            and delivery["accepted"] is False
            and delivery["applied"] is False
            and delivery["acceptedIds"] == []
            and delivery["appliedIds"] == []
            and delivery["heldIds"] == [TARGET]
            and delivery["blockerIds"] == {TARGET: ["IE204-B02"]}
            and decision["scope"] == [TARGET]
            and decision["acceptedIds"] == []
            and decision["appliedIds"] == []
            and decision["heldIds"] == [TARGET]
            and decision["authority"] == AUTHORITY
            and per_identity["spellId"] == TARGET
            and per_identity["blockerIds"] == ["IE204-B02"],
            {"heldIds": delivery["heldIds"], "blockers": delivery["blockerIds"], "authority": delivery["authority"]},
        )
        witness_text = json.dumps(per_identity["minimumMissingWitnesses"], ensure_ascii=False).lower()
        add(
            checks,
            "IE204-B02 names both concrete missing physical witnesses without inventing object/tether rules",
            len(per_identity["minimumMissingWitnesses"]) == 2
            and "20" in witness_text
            and ("60" in witness_text or "120" in witness_text)
            and "tether" in witness_text
            and "anchor" in witness_text
            and semantic["status"] == "HOLD"
            and semantic["wholeSpellComplete"] is False
            and semantic["blockerIds"] == ["IE204-B02"]
            and len(semantic["minimumMissingWitnesses"]) == 2,
            per_identity["minimumMissingWitnesses"],
        )

        case_rows = replay["cases"]
        case_ok = (
            len(case_rows) == 6
            and all(row.get("replayPassed", row.get("fullStateReplay") == "PASS") for row in case_rows)
            and sum(row["events"] for row in case_rows) == 224
            and sum(row["forwardOperations"] for row in case_rows) == 448
            and sum(row["inverseOperations"] for row in case_rows) == 448
            and replay["fullReverseTraversals"] == 6
            and replay["newEvents"] == 0
            and sum(row.get("wholeCaseComplete", row.get("completePositiveSpellWitness", False)) is True for row in case_rows) == 1
            and sum(row.get("wholeCaseComplete", row.get("completePositiveSpellWitness", False)) is False for row in case_rows) == 5
        )
        add(
            checks,
            "All six preserved cases replay with 224 events and 448 forward plus 448 inverse operations",
            case_ok
            and counts["cases"] == 6
            and counts["incompleteCases"] == 5
            and counts["componentCompleteCases"] == 1
            and counts["events"] == 224
            and counts["forwardOperations"] == 448
            and counts["inverseOperations"] == 448
            and counts["fullReverseTraversals"] == 6,
            {"cases": len(case_rows), "events": 224, "forward": 448, "inverse": 448},
        )

        with zipfile.ZipFile(RETURN228) as prior:
            exact_case_mirrors = all(z.read(name) == prior.read(name) for name in CASE_MEMBERS)
        add(
            checks,
            "All six reviewed case files are byte-exact to the independently audited Return228 cases",
            exact_case_mirrors and read_json(RETURN228_AUDIT)["status"] == "PASS",
            {"cases": CASE_MEMBERS, "priorAudit": "PASS"},
        )

        add(
            checks,
            "Return286 retains the narrow source/semantic hold and all 13 release qualifications",
            len(delivery["qualificationIds"]) == 13
            and len(decision["qualifications"]) == 15
            and decision["qualifications"]["applied"] is False
            and decision["qualifications"]["canonicalFilesEdited"] is False
            and qualifications["applied"] is False
            and qualifications["canonicalFilesEdited"] is False
            and qualifications["runtimeApproved"] is False
            and qualifications["implementationApproved"] is False
            and qualifications["humanPlaytested"] is False
            and qualifications["releaseApproved"] is False
            and delivery["allDownstreamGatesClosed"] is True,
            delivery["qualificationIds"],
        )

    # Reconcile the complete current source binding list to Packet286's authenticated context.
    source_zip = zipfile.ZipFile(SOURCE_PACKET)
    with source_zip:
        source_names = set(source_zip.namelist())
        source_member_manifest = json.loads(source_zip.read("MANIFEST.json").decode("utf-8-sig"))
        returned_source_names = source_member_manifest["members"]
        source_archive_rows = {row["path"]: row for row in returned_source_names}
        current_rows = source_bindings["currentSources"]
        current_paths = [row["path"] for row in current_rows]
        current_match_failures = []
        for row in current_rows:
            archive_name = "current/" + row["path"]
            if archive_name not in source_names:
                current_match_failures.append(row["path"])
                continue
            observed = member_digest(source_zip, archive_name)
            if observed[:2] != (row["bytes"], row["sha256"]):
                current_match_failures.append(row["path"])
    add(
        checks,
        "All 386 current source bindings in Return286 match exact members of Packet286",
        len(current_rows) == 386
        and len(set(current_paths)) == 386
        and len(source_names) == 451
        and source_member_manifest["sourceAuthority"] == AUTHORITY
        and source_member_manifest["pendingIds"] == [TARGET]
        and not current_match_failures,
        {"bindings": len(current_rows), "sourceArchiveMembers": len(source_names), "failures": current_match_failures[:12]},
    )

    queue = read_json(QUEUE)
    groups = queue["currentPendingGroups"]
    pos = next(i for i, row in enumerate(groups) if row["group"] == "rank9-impact-exile4")
    queue_next = next(row for row in groups[pos + 1 :] if row["pendingCount"] > 0)
    delivered_next = {"group": delivery["nextPendingGroup"]["group"], "pendingIds": delivery["nextPendingGroup"]["pendingIds"]}
    artifact_next = {"group": next_group["group"], "pendingIds": next_group["pendingIds"]}
    add(
        checks,
        "Return286 next group matches the next nonempty current queue group",
        delivered_next == artifact_next == NEXT
        and queue_next["group"] == NEXT["group"]
        and queue_next["pendingIds"] == NEXT["pendingIds"]
        and delivery["nextPendingGroup"]["reviewNotStarted"] is True,
        {"return": delivered_next, "queue": {"group": queue_next["group"], "pendingIds": queue_next["pendingIds"]}},
    )

    with zipfile.ZipFile(ARCHIVE) as z:
        embedded_queue = archive_json(z, "context/CURRENT_SPELL_QUEUE_286.json")
        embedded_return285_audit = archive_json(z, "context/RETURN285_INDEPENDENT_AUDIT.json")
        embedded_return285_receipt = archive_json(z, "context/RETURN285_RECEIPT.json")
        embedded_source_audit = archive_json(z, "packet/RANK9IMPACTEXILE4_PACKET_286_INDEPENDENT_AUDIT.json")
        embedded_source_receipt = archive_json(z, "packet/RANK9IMPACTEXILE4_PACKET_286_RECEIPT.json")
        external_evidence = archive_json(z, "EXTERNAL_EVIDENCE_BINDINGS.json")
        evidence_rows = {row["path"]: row for row in external_evidence["nestedPriorArchives"]}
        evidence_failures = []
        with zipfile.ZipFile(SOURCE_PACKET) as source_evidence_zip:
            source_evidence_names = set(source_evidence_zip.namelist())
            for name, row in evidence_rows.items():
                if name not in source_evidence_names:
                    evidence_failures.append(name)
                    continue
                if member_digest(source_evidence_zip, name) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                    evidence_failures.append(name)
        add(
            checks,
            "Return286 embeds the current Packet286 audit and preserves Return285 holds without editing them",
            embedded_queue == queue
            and embedded_return285_audit == read_json(RETURN285_AUDIT)
            and embedded_return285_receipt["status"] == "PASS"
            and embedded_source_audit["status"] == embedded_source_receipt["status"] == "PASS"
            and embedded_source_audit["checkCount"] == 16
            and not evidence_failures,
            {"nestedEvidence": len(evidence_rows), "failures": evidence_failures,
             "return285Audit": embedded_return285_audit["status"]},
        )
        return285_delivery = read_json(RETURN285_DELIVERY)
        add(
            checks,
            "Return285 Summon/Hosts holds remain unchanged and outside the Return286 scope",
            return285_delivery["heldIds"] == list(EXPECTED_SUMMON_HOLDS)
            and return285_delivery["blockerIds"] == EXPECTED_SUMMON_HOLDS
            and read_json(RETURN285_AUDIT)["status"] == "PASS",
            return285_delivery["blockerIds"],
        )
        add(
            checks,
            "Package checks report complete success and no canonical/runtime/application side effects",
            delivery["packageChecks"]["failedChecks"] == []
            and delivery["packageChecks"]["presealCount"] == 173
            and delivery["packageChecks"]["roundTripCount"] == 405
            and delivery["packageChecks"]["totalCount"] == 578
            and delivery["allCheckCountIncludingPackage"] == 18485
            and delivery["canonicalFilesEdited"] is False
            and delivery["runtimeExecuted"] is False
            and delivery["suppliedOrHistoricalProgramsExecuted"] is False
            and validation["runtimeExecuted"] is False
            and validation["sourceProgramsExecuted"] is False,
            {"packageChecks": delivery["packageChecks"]["totalCount"],
             "allChecks": delivery["allCheckCountIncludingPackage"]},
        )

    passed = sum(row["passed"] for row in checks)
    report = {
        "id": "RANK9IMPACTEXILE4-RETURN286-INDEPENDENT-AUDIT",
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
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(checks) - passed,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_size, report_sha, report_crc = digest(REPORT)
    receipt = {
        "id": "RANK9IMPACTEXILE4-RETURN286-RECEIPT",
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
