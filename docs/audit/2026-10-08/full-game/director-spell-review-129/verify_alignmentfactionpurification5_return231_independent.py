from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_alignment_faction_purification5_return231_received"
ARCHIVE = RECEIVED / "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD_DELIVERY.json"
SOURCE_DIR = AUDIT / "rank9_alignmentfactionpurification5_current_source_231_prepared"
SOURCE_PACKET = SOURCE_DIR / "DD_Rank9_AlignmentFactionPurification5_CurrentSource_231.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_AlignmentFactionPurification5_CurrentSource_231_DELIVERY.json"
PACKET_SUBMISSION = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_231_SUBMISSION.json"
PACKET_AUDIT = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_231_INDEPENDENT_AUDIT.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_231.json"
PRIOR_DIR = AUDIT / "rank9_alignment_faction_purification5_return211_received"
PRIOR_ARCHIVE = PRIOR_DIR / "DD_Rank9_AlignmentFactionPurification5_Director_Return211_HELD.zip"
SUPPLEMENT_ARCHIVE = AUDIT / "rank9_alignment_faction_purification5_comparator_supplement_211" / "DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211.zip"
REPORT = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_RECEIPT.json"

AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
TARGETS = [
    "alignment-ascension",
    "alignment-perfection",
    "faction-incarnate",
    "faction-perfection",
    "corruption-purification",
]
BLOCKERS = [f"AFP211-B0{i}" for i in range(1, 6)]
COMPARATORS = [
    "alignment-avatar",
    "alignment-immunity",
    "corruption-immunity",
    "faction-aegis",
    "faction-citadel",
    "faction-paragon",
]
NEXT = {"group": "rank9-projection-confinement2", "pendingIds": ["astral-projection", "imprisonment"]}


def digest(path: Path) -> tuple[int, str, str]:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return size, h.hexdigest(), f"{crc & 0xffffffff:08x}"


def member_digest(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h = hashlib.sha256()
    crc = 0
    size = 0
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
    delivery = read_json(DELIVERY)
    submission = read_json(PACKET_SUBMISSION)
    packet_audit = read_json(PACKET_AUDIT)
    source_delivery = read_json(SOURCE_DELIVERY)
    queue = read_json(QUEUE)
    archive_size, archive_sha, archive_crc = digest(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = digest(DELIVERY)
    source_size, source_sha, source_crc = digest(SOURCE_PACKET)
    source_delivery_size, source_delivery_sha, source_delivery_crc = digest(SOURCE_DELIVERY)
    prior_size, prior_sha, prior_crc = digest(PRIOR_ARCHIVE)
    supplement_size, supplement_sha, supplement_crc = digest(SUPPLEMENT_ARCHIVE)
    queue_size, queue_sha, queue_crc = digest(QUEUE)

    add(checks, "Return231 downloaded ZIP size/SHA/CRC and filename match DELIVERY", (archive_size, archive_sha, archive_crc) == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower()) and delivery["archive"]["fileName"] == ARCHIVE.name, {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc})
    add(checks, "Return231 authority and delivery decision preserve all five holds", delivery["authority"] == AUTHORITY and delivery["accepted"] is False and delivery["applied"] is False and delivery["acceptedIds"] == [] and delivery["appliedIds"] == [] and delivery["heldIds"] == TARGETS and [x["id"] for x in delivery["perIdentityDecisions"]] == TARGETS and all(x["accepted"] is False and x["applied"] is False and x["decision"] == "held" for x in delivery["perIdentityDecisions"]), {"authority": delivery["authority"], "heldIds": delivery["heldIds"]})
    add(checks, "Downloaded source packet and delivery still match the submitted, independently audited Packet231", (source_size, source_sha, source_crc) == (submission["packet"]["bytes"], submission["packet"]["sha256"], submission["packet"]["crc32"].lower()) and (source_size, source_sha, source_crc) == (packet_audit["archive"]["bytes"], packet_audit["archive"]["sha256"], packet_audit["archive"]["crc32"].lower()) and (source_delivery_size, source_delivery_sha) == (submission["deliveryManifest"]["bytes"], submission["deliveryManifest"]["sha256"]) and source_delivery["archive"]["sha256"] == source_sha and source_delivery["archive"]["bytes"] == source_size, {"sourcePacketSha256": source_sha, "sourceDeliverySha256": source_delivery_sha, "packetAuditStatus": packet_audit["status"]})

    with zipfile.ZipFile(ARCHIVE) as returned, zipfile.ZipFile(SOURCE_PACKET) as packet, zipfile.ZipFile(PRIOR_ARCHIVE) as prior, zipfile.ZipFile(SUPPLEMENT_ARCHIVE) as supplement:
        names = returned.namelist()
        external_rows = {row["path"]: row for row in delivery["members"]}
        unsafe = [name for name in names if name.startswith(("/", "\\")) or "\\" in name or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts]
        add(checks, "Return ZIP has exactly 257 unique safe members matching the exact allowlist", len(names) == len(set(names)) == len(external_rows) == delivery["memberCount"] == len(delivery["exactAllowlist"]) == 257 and set(names) == set(external_rows) == set(delivery["exactAllowlist"]) and not unsafe and returned.testzip() is None, {"members": len(names), "unsafe": unsafe[:5]})
        bad = [name for name, row in external_rows.items() if member_digest(returned, name) != (row["bytes"], row["sha256"], row["crc32"].lower())]
        add(checks, "Every Return231 member independently matches DELIVERY size/SHA/CRC", not bad, {"checked": len(external_rows), "failures": bad[:10]})
        manifest = read_member(returned, "MEMBER_MANIFEST.json")
        internal_rows = {row["path"]: row for row in manifest["members"]}
        payload = set(names) - {"MEMBER_MANIFEST.json"}
        manifest_digest = member_digest(returned, "MEMBER_MANIFEST.json")
        add(checks, "Internal member manifest binds the external manifest row and exact 256-member payload", len(internal_rows) == len(payload) == manifest["payloadCount"] == delivery["payloadMemberCount"] == 256 and set(internal_rows) == payload and delivery["memberManifest"]["path"] == "MEMBER_MANIFEST.json" and manifest_digest == (delivery["memberManifest"]["bytes"], delivery["memberManifest"]["sha256"], delivery["memberManifest"]["crc32"].lower()), {"payloadMembers": len(payload), "manifestSha256": manifest_digest[1]})
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
        casebook = returned.read("CASEBOOK.json")
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

        add(checks, "Director decision independently matches delivery, authority, target IDs and closed AFP211-E01", decision["id"] == "RANK9-ALIGNMENT-FACTION-PURIFICATION5-DIRECTOR-RETURN231" and decision["authority"] == AUTHORITY and decision["accepted"] is False and decision["applied"] is False and decision["acceptedIds"] == [] and decision["appliedIds"] == [] and decision["heldIds"] == TARGETS and decision["closedEvidenceFinding"] == {"id": "AFP211-E01", "status": "CLOSED", "missingComparatorClausesRemoved": True} and delivery["closedEvidenceFinding"] == decision["closedEvidenceFinding"], {"closedEvidenceFinding": decision["closedEvidenceFinding"]})
        blocker_rows = {row["id"]: row for row in holds["identityBlockers"]}
        per_identity = {row["id"]: row for row in delivery["perIdentityDecisions"]}
        decision_rows = {row["id"]: row for row in decision["decisions"]}
        add(checks, "Five spell-local blockers retain exact IDs and explicitly mark comparator evidence closed", set(blocker_rows) == set(BLOCKERS) and [per_identity[target]["blockerIds"] for target in TARGETS] == [[blocker] for blocker in BLOCKERS] and [decision_rows[target]["blockerIds"] for target in TARGETS] == [[blocker] for blocker in BLOCKERS] and all(blocker_rows[b]["status"] == "OPEN" and blocker_rows[b]["comparatorEvidenceGap"] == "closed-not-a-blocker" and blocker_rows[b]["accepted"] is False and blocker_rows[b]["applied"] is False for b in BLOCKERS) and len(delivery["perIdentityDecisions"]) == len(decision["decisions"]) == 5, {"blockers": list(blocker_rows), "closedEvidence": comparators["status"]})
        add(checks, "Minimum missing-witness and required-content records match between delivery and director decision", all(per_identity[target]["minimumMissingWitness"] == decision_rows[target]["minimumMissingWitness"] and per_identity[target]["requiredContent"] == decision_rows[target]["requiredContent"] and len(per_identity[target]["minimumMissingWitness"]) > 80 for target in TARGETS), {target: per_identity[target]["minimumMissingWitness"] for target in TARGETS})
        add(checks, "All five procedures remain explicitly incomplete proposals, with zero complete operational procedures", len(procedures) == 5 and [row["id"] for row in procedures] == TARGETS and all(row["status"] == "source-conditioned-proposal-INCOMPLETE-NOT-OPERATIONAL" and row["completeOperationalProcedure"] is False for row in procedures) and counts["completeOperationalProcedures"] == 0 and counts["completePositiveSpellCases"] == 0, {"procedureStatuses": [row["status"] for row in procedures]})
        add(checks, "All 28 original questions have preserved dispositions and seven future requirements remain incomplete", len(questions) == len(question_dispositions) == counts["originalQuestions"] == counts["questionDispositions"] == 28 and [x["id"] for x in questions] == [x["originalQuestionUnchanged"]["id"] for x in question_dispositions] and len(future) == len(future_dispositions) == counts["futureRequirements"] == 7 and all(x["completePositiveWitness"] is False for x in future_dispositions), {"questions": len(questions), "futureRequirements": len(future)})
        add(checks, "Current source data audit reports 1,584 passing checks and no failures", source_data["checkCount"] == source_data["passed"] == len(source_data["checks"]) == counts["freshSourceDataReplayChecks"] == 1584 and source_data["failed"] == counts["freshSourceDataReplayFailures"] == 0 and all(row["passed"] is True for row in source_data["checks"]), {"checks": source_data["checkCount"], "failed": source_data["failed"]})
        add(checks, "All ten preserved component cases replay and reversible-operation totals reconcile", replay["caseCount"] == replay["passedCases"] == len(replay["cases"]) == len(case_dispositions) == counts["preservedCases"] == 10 and replay["eventCount"] == counts["events"] == 10 and replay["forwardOperations"] == counts["forwardOperations"] == 20 and replay["inverseOperations"] == counts["inverseOperations"] == 20 and all(x["passed"] is True and x["completeSpellWitness"] is False for x in replay["cases"]) and all(x["preservedByteExact"] is True and x["dataReplay"] == "PASS" for x in case_dispositions), {"cases": len(replay["cases"]), "events": replay["eventCount"], "forward": replay["forwardOperations"], "inverse": replay["inverseOperations"]})
        add(checks, "Six accepted comparator envelopes close AFP211-E01 without widening scope", comparators["id"] == "AFP211-E01" and comparators["status"] == "CLOSED" and comparators["reopened"] is False and comparators["newMissingComparatorBlockers"] == 0 and {x["id"] for x in comparators["comparators"]} == set(COMPARATORS) and all(x["status"] == "exact-current-index-bindings-verified-comparison-only" and x["scopeNotExtended"] is True for x in comparators["comparators"]), {"comparators": sorted(x["id"] for x in comparators["comparators"])})
        add(checks, "Semantic and clock checks distinguish data replay from missing full positive histories", semantic["acceptedIds"] == [] and semantic["heldIds"] == TARGETS and semantic["dataIntegrityFailures"] == 0 and semantic["missingComparatorBlockers"] == 0 and semantic["clockCompletion"] is False and clock["passed"] is False and clock["failedDataReplayCases"] == 0 and clock["componentReplayCases"] == 10 and clock["fullActorTimelineCases"] == 0, {"clock": clock, "semanticBlockedCriteria": semantic["blockedCriteria"], "missingComparatorBlockers": semantic["missingComparatorBlockers"]})
        add(checks, "Pre-seal and package audit summaries report complete passes", preseal["checkCount"] == preseal["passed"] == delivery["presealChecks"]["count"] == 213 and preseal["failed"] == delivery["presealChecks"]["failed"] == 0 and delivery["packageChecks"]["count"] == delivery["packageChecks"]["passed"] == len(delivery["packageChecks"]["checks"]) == 1545 and delivery["packageChecks"]["failed"] == 0 and all(x["passed"] is True for x in delivery["packageChecks"]["checks"]), {"presealChecks": preseal["checkCount"], "packageChecks": delivery["packageChecks"]["count"]})
        add(checks, "No application, canonical/GitHub changes, supplied-program execution or runtime execution", delivery["canonicalChanges"] is False and delivery["githubChanges"] is False and delivery["sourceProgramsExecuted"] is False and delivery["runtimeExecuted"] is False and decision["canonicalChanges"] is False and decision["sourceProgramsExecuted"] is False and decision["runtimeExecuted"] is False and authority["authorityChange"] == 0 and authority["acceptedIds"] == [] and authority["appliedIds"] == [], {"canonicalChanges": delivery["canonicalChanges"], "githubChanges": delivery["githubChanges"], "runtimeExecuted": delivery["runtimeExecuted"], "authorityChange": authority["authorityChange"]})

        # Independently bind all three input archives and their embedded copies.
        archives = {row["role"]: row for row in external["archives"]}
        expected_inputs = {
            "sourceArchive": (source_size, source_sha, source_crc, "DD_Rank9_AlignmentFactionPurification5_CurrentSource_231.zip"),
            "priorArchive": (prior_size, prior_sha, prior_crc, "DD_Rank9_AlignmentFactionPurification5_Director_Return211_HELD.zip"),
            "comparatorSupplement": (supplement_size, supplement_sha, supplement_crc, "DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211.zip"),
        }
        add(checks, "Return binds exact current-source, Return211 and comparator-supplement archives", all((archives[role]["bytes"], archives[role]["sha256"], archives[role]["crc32"].lower(), archives[role]["path"]) == expected for role, expected in expected_inputs.items()) and all((row["bytes"], row["sha256"], row["crc32"].lower()) == expected_inputs[row["role"]][:3] for row in delivery["inputArchives"]), {role: archives[role]["sha256"] for role in expected_inputs})
        prior_failures = []
        prior_direct = 0
        prior_bound_to_packet = []
        for name in prior.namelist():
            candidates = ["prior211/" + name, name]
            embedded = next((candidate for candidate in candidates if candidate in names and returned.read(candidate) == prior.read(name)), None)
            if embedded is not None:
                prior_direct += 1
                continue
            historical_name = "historical/" + name.removeprefix("evidence/")
            if historical_name in packet.namelist() and packet.read(historical_name) == prior.read(name):
                prior_bound_to_packet.append({"priorMember": name, "packetMember": historical_name})
            else:
                prior_failures.append(name)
        add(checks, "All 40 Return211 members are byte-exactly preserved directly or through Packet231 historical binding", len(prior.namelist()) == 40 and prior_direct == 39 and len(prior_bound_to_packet) == 1 and not prior_failures, {"members": len(prior.namelist()), "directCopies": prior_direct, "packetHistoricalBindings": prior_bound_to_packet, "failures": prior_failures[:8]})
        supplement_rows = {row["archiveMember"]: row for row in external["comparatorMembers"]}
        supplement_failures = []
        for name in supplement.namelist():
            row = supplement_rows.get(name)
            if row is None or member_digest(supplement, name) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                supplement_failures.append(name)
            elif row["embedded"] and (row["returnMember"] not in names or returned.read(row["returnMember"]) != supplement.read(name)):
                supplement_failures.append(name)
            elif not row["embedded"] and row.get("externalArchive", {}).get("sha256") != supplement_sha:
                supplement_failures.append(name)
        add(checks, "All 17 comparator-supplement members are embedded byte-exactly and match their bindings", len(supplement.namelist()) == len(supplement_rows) == 17 and not supplement_failures, {"members": len(supplement.namelist()), "failures": supplement_failures[:8]})

        source_rows = source_bindings["sourceBindings"]
        external_source_rows = {row["path"]: row for row in external["sourceFiles"]}
        source_failures = []
        for row in source_rows:
            manifest_row = external_source_rows.get(row["path"])
            packet_name = row.get("archiveMember", "sources_current/" + row["path"])
            if manifest_row is None or (manifest_row["bytes"], manifest_row["sha256"]) != (row["bytes"], row["sha256"]) or packet_name not in packet.namelist() or member_digest(packet, packet_name)[:2] != (row["bytes"], row["sha256"]):
                source_failures.append(row["path"])
            elif row["embedded"] and (row["returnMember"] not in names or returned.read(row["returnMember"]) != packet.read(packet_name)):
                source_failures.append(row["path"])
            elif not row["embedded"] and (manifest_row.get("embedded") is not False or manifest_row.get("externalArchive", {}).get("sha256") != source_sha):
                source_failures.append(row["path"])
        add(checks, "All 130 current-source bindings match both the submitted Packet231 and embedded Return bytes", len(source_rows) == len(external["sourceFiles"]) == counts["freshSourceBindings"] == 130 and not source_failures, {"bindings": len(source_rows), "failures": source_failures[:8]})
        add(checks, "Original questions, future requirements, casebook and all ten case files remain byte-exact to Return211", returned.read("ORIGINAL_QUESTIONS.json") == prior.read("ORIGINAL_QUESTIONS.json") and returned.read("ORIGINAL_FUTURE_REQUIREMENTS.json") == prior.read("ORIGINAL_FUTURE_REQUIREMENTS.json") and casebook == prior.read("CASEBOOK.json") and all(returned.read(name) == prior.read(name) and returned.read("prior211/" + name) == prior.read(name) for name in prior.namelist() if name.startswith("cases/")) and sum(name.startswith("cases/") for name in prior.namelist()) == 10, {"questions": len(questions), "futureRequirements": len(future), "cases": sum(name.startswith("cases/") for name in prior.namelist())})

        queue_binding = next_group["queueBinding"]
        queue_member = "current/" + queue_binding["path"]
        queue_member_digest = member_digest(packet, queue_member)
        packet_queue = read_member(packet, queue_member)
        queue_pos = next(i for i, row in enumerate(queue["currentPendingGroups"]) if row["group"] == "rank9-alignment-faction-purification5")
        queue_next = queue["currentPendingGroups"][queue_pos + 1]
        packet_queue_pos = next(i for i, row in enumerate(packet_queue["currentPendingGroups"]) if row["group"] == "rank9-alignment-faction-purification5")
        packet_queue_next = packet_queue["currentPendingGroups"][packet_queue_pos + 1]
        add(checks, "Return names the actual next group in current queue order", next_group["group"] == NEXT["group"] and next_group["pendingIds"] == NEXT["pendingIds"] and delivery["nextPendingGroup"] == NEXT["group"] and delivery["nextPendingIds"] == NEXT["pendingIds"] and queue_next["group"] == NEXT["group"] and queue_next["pendingIds"] == NEXT["pendingIds"], {"nextGroup": next_group["group"], "pendingIds": next_group["pendingIds"]})
        add(checks, "Packet231 queue-member SHA/CRC matches NEXT_GROUP and local pending order is unchanged", queue_member_digest == (queue_binding["bytes"], queue_binding["sha256"], queue_binding["crc32"].lower()) and queue["currentPendingGroups"] == packet_queue["currentPendingGroups"] and packet_queue_next["group"] == NEXT["group"] and packet_queue_next["pendingIds"] == NEXT["pendingIds"], {"packetQueueSha256": queue_member_digest[1], "localMatchesPacketOrder": queue["currentPendingGroups"] == packet_queue["currentPendingGroups"], "actualNext": packet_queue_next})
        add(checks, "Return explicitly leaves the next group unreviewed and requires a fresh packet", next_group["reviewStarted"] is False and next_group["freshPacketRequired"] is True and queue_next["freshPacketRequiredForCurrentAuthority"] is True, {"reviewStarted": next_group["reviewStarted"], "freshPacketRequired": next_group["freshPacketRequired"]})

    failed = [row for row in checks if not row["passed"]]
    report = {
        "id": "RANK9ALIGNFACTIONPURIFICATION5-RETURN231-INDEPENDENT-AUDIT",
        "status": "PASS" if not failed else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size, "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": delivery["authority"],
        "targetIds": TARGETS,
        "acceptedIds": delivery["acceptedIds"],
        "appliedIds": delivery["appliedIds"],
        "heldIds": delivery["heldIds"],
        "blockerIds": BLOCKERS,
        "closedEvidenceFinding": delivery["closedEvidenceFinding"],
        "counts": delivery["counts"],
        "nextPendingGroup": NEXT,
        "checkCount": len(checks),
        "passedChecks": len(checks) - len(failed),
        "failedChecks": len(failed),
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_size, report_sha, report_crc = digest(REPORT)
    receipt = {
        "id": "RANK9ALIGNFACTIONPURIFICATION5-RETURN231-RECEIPT",
        "status": report["status"],
        "archive": report["archive"],
        "delivery": report["delivery"],
        "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), "bytes": report_size, "sha256": report_sha, "crc32": report_crc},
        "checkCount": len(checks),
        "passedChecks": len(checks) - len(failed),
        "failedChecks": len(failed),
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failed), "failedChecks": len(failed), "archiveSha256": archive_sha, "deliverySha256": delivery_sha, "report": str(REPORT), "receipt": str(RECEIPT), "failed": failed}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
