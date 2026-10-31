from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_planargates5_return226_received"
ARCHIVE = RECEIVED / "DD_Rank9_PlanarGates2_Director_Return226.zip"
DELIVERY = RECEIVED / "DD_Rank9_PlanarGates2_Director_Return226_DELIVERY.json"
SOURCE_DIR = AUDIT / "rank9_planargates5_current_source_226_prepared"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_226.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_226_DELIVERY.json"
PRIOR_ARCHIVE = AUDIT / "rank9_planargates5_return200_received/DD_Rank9_PlanarGates5_Director_Return200.zip"
REPORT = AUDIT / "RANK9_PLANARGATES5_RETURN226_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9_PLANARGATES5_RETURN226_RECEIPT.json"

TARGETS = {"banishment-gate", "conjure-demiplane-fortress"}
NEXT_IDS = [
    "summon-elemental-avatar",
    "summon-herald-of-the-planes",
    "summon-avatar-of-decay",
]
AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
EXPECTED_BLOCKERS = {
    "banishment-gate": ["PG200-B03", "PG200-B04"],
    "conjure-demiplane-fortress": ["PG200-B06"],
}
EXPECTED_HOLDS = [f"PG200-H{i:02d}" for i in range(1, 11)]


def digest(path: Path) -> tuple[int, str, str]:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            h.update(block)
            crc = zlib.crc32(block, crc)
    return size, h.hexdigest(), f"{crc & 0xFFFFFFFF:08x}"


def member_digest(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with archive.open(name, "r") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            h.update(block)
            crc = zlib.crc32(block, crc)
    return size, h.hexdigest(), f"{crc & 0xFFFFFFFF:08x}"


def record(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def read_json(archive: zipfile.ZipFile, name: str) -> dict:
    return json.loads(archive.read(name).decode("utf-8-sig"))


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    size, sha, crc = digest(ARCHIVE)
    record(
        checks,
        "Sealed Return226 archive bytes, SHA-256 and CRC32 match its delivery manifest",
        (size, sha, crc)
        == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower())
        and (size, sha, crc)
        == (1_097_803, "413fe37608fec5a675872a0aad4078a55d8e73d6fc7712752327fca2dc1d6c24", "4418595c"),
        {"bytes": size, "sha256": sha, "crc32": crc},
    )

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        infos = {item.filename: item for item in z.infolist()}
        rows = {item["path"]: item for item in delivery["members"]}
        safe = all(
            not n.startswith(("/", "\\"))
            and "\\" not in n
            and not PurePosixPath(n).is_absolute()
            and ".." not in PurePosixPath(n).parts
            for n in names
        )
        record(
            checks,
            "Return226 has 76 unique safe ZIP members and an exact manifest allowlist",
            len(names) == len(infos) == len(rows) == delivery["archiveMemberCount"] == 76
            and set(names) == set(rows)
            and safe,
            {"archiveMembers": len(names), "manifestMembers": len(rows), "safeNames": safe},
        )
        bad_member_rows = []
        for name in names:
            got = member_digest(z, name)
            expected = rows[name]
            if got != (expected["bytes"], expected["sha256"], expected["crc32"].lower()):
                bad_member_rows.append({"path": name, "actual": got, "expected": expected})
        record(
            checks,
            "All 76 ZIP members independently match delivery byte, SHA-256 and CRC32 bindings",
            not bad_member_rows,
            {"checked": len(names), "failures": bad_member_rows[:8]},
        )
        record(
            checks,
            "ZIP decompression and CRC test reports no corrupt member",
            z.testzip() is None,
            {"testzip": z.testzip()},
        )

        internal = read_json(z, "MEMBER_MANIFEST.json")
        inner = {item["path"]: item for item in internal["members"]}
        record(
            checks,
            "Internal manifest binds every outer member other than itself",
            internal["memberCountExcludingSelf"] == 75
            and internal["archiveMemberCountIncludingSelf"] == 76
            and set(inner) == set(names) - {"MEMBER_MANIFEST.json"}
            and all(
                inner[n]["bytes"] == rows[n]["bytes"]
                and inner[n]["sha256"] == rows[n]["sha256"]
                and inner[n]["crc32"].lower() == rows[n]["crc32"].lower()
                for n in inner
            ),
            {"innerRows": len(inner), "selfExclusion": internal.get("selfExclusion")},
        )

        package = delivery["packageChecks"]
        record(
            checks,
            "Director package self-report contains 386 passing package checks and no failures",
            package["status"] == "PASS"
            and package["checkCount"] == 386
            and not package["failures"]
            and len(package["checks"]) == 386
            and all(item.get("passed") is True for item in package["checks"]),
            {"checkCount": package["checkCount"], "failures": package["failures"]},
        )

        decision = read_json(z, "DIRECTOR_DECISION.json")
        record(
            checks,
            "Director disposition is exactly the two scoped holds with no acceptance or application",
            decision["scope"] == ["banishment-gate", "conjure-demiplane-fortress"]
            and set(decision["decisions"]) == TARGETS
            and decision["accepted"] is False
            and decision["applied"] is False
            and decision["acceptedIds"] == []
            and set(decision["heldIds"]) == TARGETS
            and decision["authority"] == AUTHORITY
            and delivery["authority"] == AUTHORITY
            and delivery["accepted"] is False
            and delivery["applied"] is False
            and delivery["acceptedIds"] == []
            and set(delivery["heldIds"]) == TARGETS,
            {"scope": decision["scope"], "heldIds": decision["heldIds"], "authority": decision["authority"]},
        )
        identity_rows = delivery["decisions"]
        exact_identity_holds = (
            set(identity_rows) == TARGETS
            and set(decision["decisions"]) == TARGETS
            and all(
                identity_rows[s]["accepted"] is False
                and identity_rows[s]["applied"] is False
                and identity_rows[s]["held"] is True
                and identity_rows[s]["blockerIds"] == EXPECTED_BLOCKERS[s]
                and decision["decisions"][s]["accepted"] is False
                and decision["decisions"][s]["applied"] is False
                and decision["decisions"][s]["held"] is True
                and decision["decisions"][s]["blockerIds"] == EXPECTED_BLOCKERS[s]
                and decision["decisions"][s]["conditionalQualificationIds"] == EXPECTED_HOLDS
                and decision["decisions"][s]["priorProcedureBytesUnchanged"] is True
                for s in TARGETS
            )
        )
        record(
            checks,
            "Both per-identity hold/blocker decisions and PG200-H01 through H10 qualifications match",
            exact_identity_holds,
            {s: identity_rows[s]["blockerIds"] for s in sorted(identity_rows)},
        )

        blocker_map = {item["id"]: item for item in decision["blockers"]}
        expected_blocker_ids = {"PG200-B03", "PG200-B04", "PG200-B06"}
        reassessments = {k: v.get("reassessment226", {}) for k, v in blocker_map.items()}
        witness_text = " ".join(
            str(blocker.get("scope", "")) + " " + str(blocker.get("missing", "")) + " "
            + str(blocker.get("minimalCorrection", "")) + " "
            + str(blocker.get("reassessment226", {}).get("minimumMissingWitness", "")) + " "
            + str(blocker.get("reassessment226", {}).get("sourceFinding", ""))
            for blocker in blocker_map.values()
        ).lower()
        record(
            checks,
            "Three open blockers include the required source-qualified positive-witness gaps",
            set(blocker_map) == expected_blocker_ids
            and all(blocker_map[i]["blocking"] is True and blocker_map[i]["status"] == "OPEN" for i in expected_blocker_ids)
            and all(reassessments[i].get("status") == "OPEN_REQUIRED_WITNESS" for i in expected_blocker_ids)
            and all(blocker_map[i]["accepted"] is False and blocker_map[i]["applied"] is False for i in expected_blocker_ids)
            and all(k in witness_text for k in ["nonmatching", "crossing", "guard", "escape", "summon", "structural", "work/rest", "companion", "occupied", "nested"]),
            {"blockerIds": sorted(blocker_map), "reassessmentStatus": {k: v.get("status") for k, v in reassessments.items()}},
        )

        replay = read_json(z, "CASE_REPLAY.json")
        clock = read_json(z, "CLOCK_AND_INVERSE_RESULTS.json")
        counts = read_json(z, "COUNTS.json")
        validation_checks = read_json(z, "VALIDATION_CHECKS.json")
        replay_counts_ok = (
            replay["caseCount"] == counts["cases"] == len(replay["cases"]) == 23
            and replay["eventCount"] == counts["events"] == clock["events"] == 267
            and replay["forwardOperations"] == counts["forwardEventOperations"] == clock["forwardOperations"] == 534
            and replay["inverseOperations"] == counts["inverseEventOperations"] == clock["inverseOperations"] == 534
            and replay["proposalOperations"] == counts["proposalOperations"] == clock["proposalOperations"] == 8
            and not replay["integrityFailures"]
            and clock["failures"] == 0
            and clock["status"] == "PASS_FOR_REPRESENTED_HISTORIES"
            and clock["wholeCaseReverseChains"] == 23
            and clock["noHiddenTurnClaim"] is True
            and validation_checks["checkCount"] == counts["dataAndScopedChecks"] == 14_462
            and not validation_checks["failures"]
            and counts["freshCheckFailures"] == 0
        )
        record(
            checks,
            "Case replay, clock/inverse replay, and 14,462 data/scoped checks reconcile with zero failures",
            replay_counts_ok,
            {"cases": replay["caseCount"], "events": replay["eventCount"], "forward": replay["forwardOperations"],
             "inverse": replay["inverseOperations"], "proposals": replay["proposalOperations"],
             "checks": validation_checks["checkCount"], "failures": validation_checks["failures"]},
        )

        timeline_failures = []
        case_names = set()
        for case in replay["cases"]:
            case_names.add(case["sourceFile"])
            timeline = case["timeline"]
            links = (
                bool(timeline)
                and len(timeline) == case["events"]
                and timeline[0]["beforeSHA256"] == case["initialSHA256"]
                and timeline[-1]["afterSHA256"] == case["finalSHA256"]
                and all(a["afterSHA256"] == b["beforeSHA256"] for a, b in zip(timeline, timeline[1:]))
                and all(len(e["beforeSHA256"]) == len(e["afterSHA256"]) == 64 for e in timeline)
                and case["failures"] == 0
                and case["replayPassed"] is True
                and case["accepted"] is False
                and case["applied"] is False
            )
            got = member_digest(z, case["sourceFile"])
            binding = case["binding"]
            exact_source = got == (binding["bytes"], binding["sha256"], binding["crc32"].lower())
            if not links or not exact_source:
                timeline_failures.append(case["id"])
        record(
            checks,
            "All 23 case files match their bindings and each represented state-hash timeline joins exactly",
            len(case_names) == 23 and not timeline_failures,
            {"caseFiles": len(case_names), "failures": timeline_failures[:8]},
        )

        case_dispositions = read_json(z, "CASE_DISPOSITIONS.json")
        record(
            checks,
            "All 23 case dispositions remain explicitly scoped and none converts a hold into acceptance",
            len(case_dispositions["cases"]) == 23
            and {item["id"] for item in case_dispositions["cases"]} == {item["id"] for item in replay["cases"]}
            and all(item.get("result") == "REPLAY_PASS_WHOLE_REQUIRED_WITNESS_HELD"
                    and item.get("replayPassed") is True
                    and set(item.get("blockerIds", [])) <= set(EXPECTED_BLOCKERS[item["spellId"]])
                    for item in case_dispositions["cases"])
            and {blocker for item in case_dispositions["cases"] for blocker in item.get("blockerIds", [])}
                == {b for ids in EXPECTED_BLOCKERS.values() for b in ids},
            {"dispositions": len(case_dispositions["cases"])},
        )

        proposals = read_json(z, "PROPOSAL_OPERATIONS.json")
        record(
            checks,
            "Eight proposal operations are retained but unapplied",
            len(proposals["operations"]) == 2
            and sum(len(op["forward"]) + len(op["inverse"]) for op in proposals["operations"]) == 8
            and proposals["applied"] is False
            and counts["proposalOperations"] == 8,
            {"proposalRecords": len(proposals["operations"]),
             "reversibleOperations": sum(len(op["forward"]) + len(op["inverse"]) for op in proposals["operations"]),
             "applied": proposals["applied"]},
        )

        future = read_json(z, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        questions = read_json(z, "QUESTION_DISPOSITIONS.json")
        original = read_json(z, "source_context/ORIGINAL_30_QUESTIONS_2_ADDENDA_9_FUTURE_REQUIREMENTS.json")
        record(
            checks,
            "All 30 original questions, two focused addenda, and nine future requirements remain preserved",
            counts["originalQuestionsPreserved"] == 30
            and counts["focusedAddendaPreserved"] == 2
            and counts["futureRequirementsPreserved"] == future["preservedCount"] == 9
            and questions["originalQuestionsPreserved"] == 30
            and questions["focusedAddendaPreserved"] == 2
            and len(original["completeOriginalQuestionsUnchanged"]) == 30
            and len(original["focusedAdditionalQuestions"]) == 2
            and len(original["originalFutureCaseRequirementsUnchanged"]) == 9
            and len(future["obligations"]) == 9,
            {"questions": questions["originalQuestionsPreserved"], "addenda": questions["focusedAddendaPreserved"],
             "futureRequirements": future["preservedCount"]},
        )

        validation = read_json(z, "VALIDATION.json")
        reconciliation = read_json(z, "SOURCE_RECONCILIATION.json")
        source_verification = read_json(z, "SOURCE_VERIFICATION.json")
        record(
            checks,
            "Return reports data pass with semantic holds, and explicitly closes runtime/canonical execution",
            validation["status"] == "DATA_PASS_SEMANTIC_HOLD"
            and not validation["failures"]
            and validation["suppliedProgramsExecuted"] is False
            and validation["canonicalFilesChanged"] is False
            and validation["runtimeExecuted"] is False
            and reconciliation["canonicalChanges"] is False,
            {"status": validation["status"], "failures": validation["failures"],
             "canonicalChanges": reconciliation["canonicalChanges"]},
        )

    source_size, source_sha, source_crc = digest(SOURCE_ARCHIVE)
    source_delivery_raw = SOURCE_DELIVERY.read_bytes()
    source_delivery_size, source_delivery_sha, source_delivery_crc = digest(SOURCE_DELIVERY)
    source_delivery = json.loads(source_delivery_raw.decode("utf-8-sig"))
    source_ok = (
        (source_size, source_sha, source_crc)
        == (delivery["sourcePacket"]["bytes"], delivery["sourcePacket"]["sha256"], delivery["sourcePacket"]["crc32"].lower())
        == (117_174_189, "db0c43f77222075d37c049581974828955f7d256e30ca22e7e1a7fe9333402e4", "37d64889")
        and (source_delivery_size, source_delivery_sha, source_delivery_crc)
        == (delivery["sourceDelivery"]["bytes"], delivery["sourceDelivery"]["sha256"], delivery["sourceDelivery"]["crc32"].lower())
        and source_delivery["archive"]["sha256"] == source_sha
        and source_delivery["archive"]["bytes"] == source_size
    )
    record(checks, "Current-source packet and manifest exactly match the files actually submitted", source_ok,
           {"sourceBytes": source_size, "sourceSHA256": source_sha, "sourceDeliverySHA256": source_delivery_sha})

    prior_size, prior_sha, prior_crc = digest(PRIOR_ARCHIVE)
    record(
        checks,
        "Prior Return200 archive hash is unchanged and matches Return226's recorded context binding",
        (prior_size, prior_sha, prior_crc)
        == (delivery["priorReturn200Archive"]["bytes"], delivery["priorReturn200Archive"]["sha256"], delivery["priorReturn200Archive"]["crc32"].lower()),
        {"priorBytes": prior_size, "priorSHA256": prior_sha, "priorCRC32": prior_crc},
    )

    queue = json.loads((AUDIT / "CURRENT_SPELL_QUEUE_226.json").read_text(encoding="utf-8-sig"))
    handoff = json.loads((AUDIT / "CURRENT_HANDOFF_226.json").read_text(encoding="utf-8-sig"))
    next_group = decision["nextPendingGroup"]
    record(
        checks,
        "Next group is exactly the three still-pending Rank9 Summon Hosts identities",
        next_group == {"group": "rank9-summon-hosts5", "pendingIds": NEXT_IDS}
        and delivery["nextPendingGroup"] == next_group
        and any(g["group"] == "rank9-summon-hosts5" and g["pendingIds"] == NEXT_IDS for g in queue["currentPendingGroups"])
        and handoff["nextStep"]["group"] == "rank9-planar-gates5"
        and handoff["nextStep"]["pendingIds"] == ["banishment-gate", "conjure-demiplane-fortress"],
        next_group,
    )

    passed = sum(c["passed"] for c in checks)
    report = {
        "id": "RANK9PLANARGATES5-RETURN226-INDEPENDENT-AUDIT",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checkedAtUtc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": size, "sha256": sha, "crc32": crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size,
                     "sha256": digest(DELIVERY)[1], "crc32": digest(DELIVERY)[2]},
        "authority": AUTHORITY,
        "acceptedIds": [],
        "heldIds": sorted(TARGETS),
        "nextPendingGroup": next_group,
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": [c for c in checks if not c["passed"]],
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "id": "RANK9PLANARGATES5-RETURN226-INDEPENDENT-AUDIT-RECEIPT",
        "status": report["status"],
        "archiveSHA256": sha,
        "deliverySHA256": digest(DELIVERY)[1],
        "auditPath": REPORT.relative_to(ROOT).as_posix(),
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": len(report["failedChecks"]),
        "acceptedIds": [],
        "heldIds": sorted(TARGETS),
        "authorityUnchanged": AUTHORITY,
        "nextPendingGroup": next_group,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
