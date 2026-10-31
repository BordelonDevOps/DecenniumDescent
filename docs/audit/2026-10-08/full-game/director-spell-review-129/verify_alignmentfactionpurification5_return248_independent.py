from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_alignmentfactionpurification5_return248_received"
ARCHIVE = RECEIVED / "DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD_DELIVERY.json"
SOURCE_DIR = AUDIT / "rank9_alignmentfactionpurification5_current_source_248_prepared"
SOURCE_PACKET = SOURCE_DIR / "DD_Rank9_AlignmentFactionPurification5_CurrentSource_248.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_AlignmentFactionPurification5_CurrentSource_248_DELIVERY.json"
PACKET_SUBMISSION = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_248_SUBMISSION.json"
PACKET_AUDIT = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_248_INDEPENDENT_AUDIT.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_248.json"
PRIOR211 = AUDIT / "rank9_alignment_faction_purification5_return211_received" / "DD_Rank9_AlignmentFactionPurification5_Director_Return211_HELD.zip"
PRIOR231 = AUDIT / "rank9_alignment_faction_purification5_return231_received" / "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD.zip"
SUPPLEMENT = AUDIT / "rank9_alignment_faction_purification5_comparator_supplement_211" / "DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211.zip"
REPORT = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_RETURN248_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_RETURN248_RECEIPT.json"

AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"]
BLOCKERS = [f"AFP211-B0{i}" for i in range(1, 6)]
COMPARATORS = {"alignment-avatar", "alignment-immunity", "corruption-immunity", "faction-aegis", "faction-citadel", "faction-paragon"}
NEXT = {"group": "rank9-projection-confinement2", "pendingIds": ["astral-projection", "imprisonment"]}


def digest(path: Path) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return size, h.hexdigest(), f"{crc & 0xffffffff:08x}"


def member_digest(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with archive.open(name) as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return size, h.hexdigest(), f"{crc & 0xffffffff:08x}"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_member(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8-sig"))


def add(checks: list[dict], name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery, submission = read_json(DELIVERY), read_json(PACKET_SUBMISSION)
    packet_audit, source_delivery, queue = read_json(PACKET_AUDIT), read_json(SOURCE_DELIVERY), read_json(QUEUE)
    archive_size, archive_sha, archive_crc = digest(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = digest(DELIVERY)
    source_size, source_sha, source_crc = digest(SOURCE_PACKET)
    source_delivery_size, source_delivery_sha, _ = digest(SOURCE_DELIVERY)
    prior211_size, prior211_sha, prior211_crc = digest(PRIOR211)
    prior231_size, prior231_sha, prior231_crc = digest(PRIOR231)
    supplement_size, supplement_sha, supplement_crc = digest(SUPPLEMENT)

    add(checks, "Return248 ZIP size/SHA/CRC and path match DELIVERY", (archive_size, archive_sha, archive_crc) == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower()) and delivery["archive"]["path"] == ARCHIVE.name, {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc})
    add(checks, "Return248 authority is unchanged and all five identities are held", delivery["authority"] == AUTHORITY and delivery["group"] == "rank9-alignment-faction-purification5" and delivery["accepted"] is False and delivery["applied"] is False and delivery["acceptedIds"] == [] and delivery["appliedIds"] == [] and delivery["heldIds"] == TARGETS and delivery["blockerIds"] == BLOCKERS, {"authority": delivery["authority"], "heldIds": delivery["heldIds"], "blockers": delivery["blockerIds"]})
    add(checks, "Submitted Packet248 and independent packet audit bind local source archive and delivery", (source_size, source_sha, source_crc) == (submission["archive"]["bytes"], submission["archive"]["sha256"], submission["archive"]["crc32"].lower()) == (packet_audit["archive"]["bytes"], packet_audit["archive"]["sha256"], packet_audit["archive"]["crc32"].lower()) and packet_audit["status"] == "PASS" and (source_delivery_size, source_delivery_sha) == (submission["deliveryManifest"]["bytes"], submission["deliveryManifest"]["sha256"]) and source_delivery["archive"]["sha256"] == source_sha and source_delivery["archive"]["bytes"] == source_size, {"packetSha256": source_sha, "packetAudit": packet_audit["status"]})

    with zipfile.ZipFile(ARCHIVE) as returned, zipfile.ZipFile(SOURCE_PACKET) as packet, zipfile.ZipFile(PRIOR211) as prior211, zipfile.ZipFile(PRIOR231) as prior231, zipfile.ZipFile(SUPPLEMENT) as supplement:
        names = returned.namelist()
        external_rows = {row["path"]: row for row in delivery["members"]}
        unsafe = [name for name in names if name.startswith(("/", "\\")) or "\\" in name or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts]
        add(checks, "Return ZIP has exactly 105 unique safe members matching DELIVERY", len(names) == len(set(names)) == len(external_rows) == delivery["archiveMemberCount"] == 105 and set(names) == set(external_rows) and not unsafe and returned.testzip() is None, {"members": len(names), "unsafe": unsafe[:5]})
        bad = [name for name, row in external_rows.items() if member_digest(returned, name) != (row["bytes"], row["sha256"], row["crc32"].lower())]
        add(checks, "Every Return248 member independently matches DELIVERY size/SHA/CRC", not bad, {"checked": len(external_rows), "failures": bad[:10]})
        manifest = read_member(returned, "MEMBER_MANIFEST.json")
        internal_rows = {row["path"]: row for row in manifest["members"]}
        payload = set(names) - {"MEMBER_MANIFEST.json"}
        manifest_digest = member_digest(returned, "MEMBER_MANIFEST.json")
        add(checks, "Internal manifest binds DELIVERY and all 104 payload members", len(internal_rows) == len(payload) == manifest["payloadCount"] == delivery["payloadMemberCount"] == 104 and set(internal_rows) == payload and delivery["memberManifest"]["path"] == "MEMBER_MANIFEST.json" and manifest_digest == (delivery["memberManifest"]["bytes"], delivery["memberManifest"]["sha256"], delivery["memberManifest"]["crc32"].lower()), {"payload": len(payload), "manifestSha256": manifest_digest[1]})
        bad_internal = [name for name, row in internal_rows.items() if member_digest(returned, name) != (row["bytes"], row["sha256"], row["crc32"].lower())]
        add(checks, "Every payload member independently matches MEMBER_MANIFEST", not bad_internal, {"checked": len(internal_rows), "failures": bad_internal[:10]})

        decision = read_member(returned, "DIRECTOR_DECISION.json")
        counts = read_member(returned, "COUNTS.json")
        holds = read_member(returned, "HOLD_REGISTER.json")
        procedures = read_member(returned, "PROCEDURES.json")
        questions = read_member(returned, "ORIGINAL_QUESTIONS.json")
        question_dispositions = read_member(returned, "QUESTION_DISPOSITIONS.json")
        future = read_member(returned, "ORIGINAL_FUTURE_REQUIREMENTS.json")
        future_dispositions = read_member(returned, "FUTURE_CASE_DISPOSITIONS.json")
        replay = read_member(returned, "REPLAY_RESULTS.json")
        case_dispositions = read_member(returned, "CASE_DISPOSITIONS.json")
        source_bindings = read_member(returned, "SOURCE_BINDINGS.json")
        source_data = read_member(returned, "SOURCE_DATA_CHECK.json")
        comparators = read_member(returned, "COMPARATOR_VERIFICATION.json")
        semantic = read_member(returned, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        clock = read_member(returned, "CLOCK_CHECK.json")
        next_group = read_member(returned, "NEXT_GROUP.json")
        external = read_member(returned, "EXTERNAL_ARCHIVE_BINDINGS.json")
        authority = read_member(returned, "CURRENT_AUTHORITY.json")
        preseal = read_member(returned, "PRESEAL_CHECK.json")

        add(checks, "Director decision preserves five holds, unchanged authority and closed AFP211-E01", decision["id"] == "RANK9-ALIGNMENT-FACTION-PURIFICATION5-DIRECTOR-RETURN248" and decision["authority"] == AUTHORITY and decision["accepted"] is False and decision["applied"] is False and decision["acceptedIds"] == [] and decision["appliedIds"] == [] and decision["heldIds"] == TARGETS and decision["closedEvidenceFinding"]["id"] == "AFP211-E01" and decision["closedEvidenceFinding"]["status"] == "CLOSED" and delivery["closedEvidenceFinding"] == {"id": "AFP211-E01", "status": "CLOSED"}, {"closedEvidenceFinding": decision["closedEvidenceFinding"]})
        blocker_rows = {row["id"]: row for row in holds["identityBlockers"]}
        decision_rows = {row["id"]: row for row in decision["decisions"]}
        add(checks, "Five spell-local blockers retain exact target mapping and closed comparator gap", set(blocker_rows) == set(BLOCKERS) and len(decision_rows) == 5 and [decision_rows[target]["blockerIds"] for target in TARGETS] == [[b] for b in BLOCKERS] and all(blocker_rows[b]["status"] == "OPEN" and blocker_rows[b]["comparatorEvidenceGap"] == "closed-not-a-blocker" and blocker_rows[b]["accepted"] is False and blocker_rows[b]["applied"] is False for b in BLOCKERS), {"blockers": sorted(blocker_rows)})
        add(checks, "Each held spell has a concrete minimum missing witness and required-content list", all(len(decision_rows[target]["minimumMissingWitness"]) > 50 and len(decision_rows[target]["requiredContent"]) > 0 for target in TARGETS), {target: decision_rows[target]["minimumMissingWitness"] for target in TARGETS})
        add(checks, "All five proposals remain incomplete with zero complete positive witnesses", len(procedures) == 5 and [row["id"] for row in procedures] == TARGETS and all(row["status"] == "source-conditioned-proposal-INCOMPLETE-NOT-OPERATIONAL" and row["completeOperationalProcedure"] is False for row in procedures) and counts["completeOperationalProcedures"] == 0 and counts["completePositiveSpellCases"] == 0 and delivery["completePositiveSpellWitnesses"] == 0, {"procedures": len(procedures), "completePositiveSpellCases": counts["completePositiveSpellCases"]})
        add(checks, "All 28 question dispositions and seven future-case requirements are retained", len(questions) == len(question_dispositions) == counts["originalQuestions"] == counts["questionDispositions"] == 28 and [q["id"] for q in questions] == [q["originalQuestionUnchanged"]["id"] for q in question_dispositions] and len(future) == len(future_dispositions) == counts["futureRequirements"] == 7 and all(row["completePositiveWitness"] is False for row in future_dispositions), {"questions": len(questions), "futureRequirements": len(future)})
        add(checks, "All 2,817 fresh source-data checks pass with zero failures", source_data["status"] == "PASS" and source_data["checkCount"] == len(source_data["checks"]) == counts["freshSourceDataReplayChecks"] == 2817 and source_data["failureCount"] == counts["freshSourceDataReplayFailures"] == 0 and all(row["passed"] is True for row in source_data["checks"]), {"checks": source_data["checkCount"], "failures": source_data["failureCount"]})
        replay_events = sum(row["events"] for row in replay["cases"])
        replay_forward = sum(row["forwardOperations"] for row in replay["cases"])
        replay_inverse = sum(row["inverseOperations"] for row in replay["cases"])
        add(checks, "Ten component cases reconcile to 10 events and 20 forward/20 inverse operations", replay["status"] == "PASS" and len(replay["cases"]) == len(case_dispositions) == counts["preservedCases"] == 10 and replay_events == counts["events"] == 10 and replay_forward == counts["forwardOperations"] == 20 and replay_inverse == counts["inverseOperations"] == 20 and all(row["observed"].startswith("PASS") and row["completeSpellWitness"] is False for row in replay["cases"]) and all(row["preservedByteExact"] is True and row["dataReplay"] == "PASS" for row in case_dispositions), {"cases": len(replay["cases"]), "events": replay_events, "forward": replay_forward, "inverse": replay_inverse})
        add(checks, "AFP211-E01 closes all six comparator checks without reopening spell scope", comparators["id"] == "AFP211-E01" and comparators["status"] == "CLOSED" and comparators["reopened"] is False and {row["id"] for row in comparators["comparators"]} == COMPARATORS and all(row["status"] == "exact-current-index-bindings-verified-comparison-only" and row["scopeNotExtended"] is True for row in comparators["comparators"]), {"comparators": sorted(row["id"] for row in comparators["comparators"])})
        add(checks, "Semantic and clock audits distinguish reversible components from incomplete histories", semantic["status"] == "HOLD_ALL_FIVE" and semantic["dataIntegrity"] == "PASS" and semantic["counts"]["acceptedIdentities"] == 0 and semantic["counts"]["heldIdentities"] == 5 and semantic["counts"]["semanticBlockedCriteria"] == 10 and clock["status"] == "NOT_DEMONSTRATED_FOR_COMPLETE_SPELLS" and clock["componentCasesChecked"] == 10 and clock["completeActorClockCases"] == 0 and clock["paidCastHistories"] == 0 and clock["nativeDeadlinesPreserved"] is True and counts["clockCertifiedCases"] == 0, {"clock": clock, "semanticBlockedCriteria": semantic["counts"]["semanticBlockedCriteria"]})
        add(checks, "Preseal and all 424 package checks pass", preseal["status"] == "PASS" and preseal["checkCount"] == counts["presealConsistencyChecks"] == 183 and preseal["failures"] == counts["presealConsistencyFailures"] == 0 and delivery["packageCheckCount"] == len(delivery["packageChecks"]) == 424 and delivery["packageCheckFailures"] == 0 and all(row["passed"] is True for row in delivery["packageChecks"]), {"preseal": preseal["checkCount"], "packageChecks": delivery["packageCheckCount"]})
        add(checks, "Return explicitly records no canonical changes, runtime execution or authority shift", delivery["canonicalChanges"] is False and delivery["sourceProgramsExecuted"] is False and delivery["runtimeExecuted"] is False and authority["authority"] == AUTHORITY and authority["acceptedUnappliedDelta"] == 0 and authority["canonicalChanges"] is False and authority["applied"] is False and delivery["acceptedIds"] == [] and delivery["appliedIds"] == [], {"acceptedUnappliedDelta": authority["acceptedUnappliedDelta"], "runtimeExecuted": delivery["runtimeExecuted"]})

        expected_archives = {
            "sourcePacket": (source_size, source_sha, source_crc, SOURCE_PACKET.name),
            "priorTargetReturn": (prior211_size, prior211_sha, prior211_crc, PRIOR211.name),
            "correctedPriorReturn": (prior231_size, prior231_sha, prior231_crc, PRIOR231.name),
            "comparatorSupplement": (supplement_size, supplement_sha, supplement_crc, SUPPLEMENT.name),
        }
        add(checks, "All four external input archives match exact local bytes", all((external[role]["bytes"], external[role]["sha256"], external[role]["crc32"].lower(), external[role]["path"]) == expected for role, expected in expected_archives.items()), {role: external[role]["sha256"] for role in expected_archives})
        add(checks, "130 source bindings resolve to byte-exact Packet248 members", len(source_bindings) == counts["freshSourceBindings"] == 130 and all(row["packetMember"] in packet.namelist() and member_digest(packet, row["packetMember"])[:2] == (row["bytes"], row["sha256"]) for row in source_bindings), {"bindings": len(source_bindings)})

        case_paths = [name for name in names if name.startswith("cases/") and name in prior231.namelist()]
        case_failures = [name for name in case_paths if returned.read(name) != prior231.read(name)]
        add(checks, "All ten component case files are byte-exact to corrected Return231", len(case_paths) == 10 and not case_failures, {"cases": len(case_paths), "failures": case_failures})
        preserved = ["ORIGINAL_QUESTIONS.json", "ORIGINAL_FUTURE_REQUIREMENTS.json", "CASEBOOK.json"]
        preserved_ok = {name: name in names and name in prior231.namelist() and returned.read(name) == prior231.read(name) for name in preserved}
        add(checks, "Original questions, future requirements and casebook remain byte-exact to Return231", all(preserved_ok.values()), {"preserved": preserved_ok})

        queue_rows = queue["currentPendingGroups"]
        pos = next(i for i, row in enumerate(queue_rows) if row["group"] == "rank9-alignment-faction-purification5")
        queue_next = queue_rows[pos + 1]
        add(checks, "Return names the exact next current pending group and identities", next_group["group"] == NEXT["group"] and next_group["pendingIds"] == NEXT["pendingIds"] and delivery["nextPendingGroup"]["group"] == NEXT["group"] and delivery["nextPendingGroup"]["pendingIds"] == NEXT["pendingIds"] and queue_next["group"] == NEXT["group"] and queue_next["pendingIds"] == NEXT["pendingIds"] and next_group["reviewedInThisReturn"] is False, {"nextGroup": next_group["group"], "pendingIds": next_group["pendingIds"]})
        add(checks, "Packet248 queue member remains the source of the next pointer", next_group["source"].endswith("CURRENT_SPELL_QUEUE_248.json") and next_group["pointer"] == f"/currentPendingGroups/{pos + 1}" and len(queue_rows) > pos + 1, {"pointer": next_group["pointer"], "queueIndex": pos + 1})

    failed = [row for row in checks if not row["passed"]]
    report = {"id": "RANK9ALIGNFACTIONPURIFICATION5-RETURN248-INDEPENDENT-AUDIT", "status": "PASS" if not failed else "FAIL", "checkedAtUtc": datetime.now(timezone.utc).isoformat(), "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc}, "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size, "sha256": delivery_sha, "crc32": delivery_crc}, "authority": delivery["authority"], "targetIds": TARGETS, "acceptedIds": delivery["acceptedIds"], "appliedIds": delivery["appliedIds"], "heldIds": delivery["heldIds"], "blockerIds": BLOCKERS, "closedEvidenceFinding": delivery["closedEvidenceFinding"], "counts": delivery["counts"], "nextPendingGroup": NEXT, "checkCount": len(checks), "passedChecks": len(checks) - len(failed), "failedChecks": len(failed), "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_size, report_sha, report_crc = digest(REPORT)
    receipt = {"id": "RANK9ALIGNFACTIONPURIFICATION5-RETURN248-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"], "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), "bytes": report_size, "sha256": report_sha, "crc32": report_crc}, "checkCount": len(checks), "passedChecks": len(checks) - len(failed), "failedChecks": len(failed)}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failed), "failedChecks": len(failed), "archiveSha256": archive_sha, "deliverySha256": delivery_sha, "report": str(REPORT), "receipt": str(RECEIPT), "failed": failed}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
