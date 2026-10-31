from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_projectionconfinement2_current_source_288_prepared"
ARCHIVE = OUT / "DD_Rank9_ProjectionConfinement2_CurrentSource_288.zip"
DELIVERY = OUT / "DD_Rank9_ProjectionConfinement2_CurrentSource_288_DELIVERY.json"
CANDIDATE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_288.json"
CONTEXT = OUT / "CURRENT_CONTEXT_288.json"
REQUEST = OUT / "REQUEST_288.txt"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Projection_Confinement_2_Source_Conference_01.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_projection_confinement_2_source_conference_01.json"
SOURCE_NOTES = AUDIT / "RANK9PROJECTIONCONFINEMENT2_NEXT_CONFERENCE_NOTES_129.json"
SOURCE_PACKET_RECORD = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_129.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_288.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_288.json"
PENDING = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_288.json"
PACKET_RECORD = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_288.json"
REPORT = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_RECEIPT.json"
TARGETS = ["astral-projection", "imprisonment"]
HELD287 = ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"]
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
RECENT = {
    284: ("rank9_planargates5_return284_received", "DD_Rank9_PlanarGates5_Director_Return284_HELD.zip", "DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json", "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json", "RANK9_PLANARGATES5_RETURN284_RECEIPT.json"),
    285: ("rank9_summonhosts5_return285_received", "DD_Rank9_SummonHosts5_Director_Return285_HELD.zip", "DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json", "RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json", "RANK9SUMMONHOSTS5_RETURN285_RECEIPT.json"),
    286: ("rank9_impactexile4_return286_received", "DD_Rank9_ImpactExile4_Director_Return286_HELD.zip", "DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN286_RECEIPT.json"),
    287: ("rank9_alignmentfactionpurification5_return287_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN287_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN287_RECEIPT.json"),
}


def file_digest(path: Path) -> tuple[int, str, str]:
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


def add(checks: list[dict], name: str, passed: bool, detail=None):
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main():
    checks = []
    delivery = read_json(DELIVERY)
    candidate = read_json(CANDIDATE)
    context = read_json(CONTEXT)
    notes = read_json(SOURCE_NOTES)
    old_candidate = read_json(SOURCE_CANDIDATE)
    old_packet_record = read_json(SOURCE_PACKET_RECORD)
    packet_record = read_json(PACKET_RECORD)
    archive_size, archive_sha, archive_crc = file_digest(ARCHIVE)
    delivery_size, delivery_sha, delivery_crc = file_digest(DELIVERY)
    source_archive_size, source_archive_sha, source_archive_crc = file_digest(SOURCE_ARCHIVE)

    add(checks, "Packet288 archive size/SHA/CRC and filename match its DELIVERY manifest", (archive_size, archive_sha, archive_crc) == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower()) and delivery["archive"]["path"].endswith(ARCHIVE.name), {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc})
    add(checks, "Packet is bound to current main authority 816/32/0 and exact two still-pending IDs", delivery["sourceBranch"] == "main" and delivery["sourceAuthority"] == AUTHORITY and delivery["group"] == "rank9-projection-confinement2" and delivery["pendingIds"] == TARGETS and delivery["accepted"] is False and delivery["applied"] is False and context["sourceAuthority"] == AUTHORITY and context["targetGroup"]["pendingIds"] == TARGETS, {"authority": delivery["sourceAuthority"], "targets": delivery["pendingIds"]})
    add(checks, "Current index and catalog contain both targets as pending with exact current counts", read_json(INDEX)["authoredCounts"] == {"reviewed": 816, "pending": 32} and all(row["currentIndexEntry"]["authoredStatus"] == "pending-authored-procedure" and row["currentIndexEntry"]["sourceStatus"] == "blocked-pending-operational-review" for row in candidate["currentReviewTargets"]) and [row["spellId"] for row in candidate["currentReviewTargets"]] == TARGETS and all(row["completeCurrentCatalogSourceAndAccess"]["id"] == row["spellId"] for row in candidate["currentReviewTargets"]), {"targetStatuses": [(row["spellId"], row["currentIndexEntry"]["authoredStatus"]) for row in candidate["currentReviewTargets"]]})
    add(checks, "Historical conference and source-conference packet are explicitly prepared-only, not prior decisions", old_packet_record["status"] == "PREPARED_NOT_SENT" and read_json(ROOT / "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_PREPARATION.json")["status"] == "PREPARED_UNSENT" and delivery["historicalWorkflow"]["priorDirectorRuling"] is None and candidate["historicalWorkflow"]["priorDirectorDecision"] is None and candidate["historicalWorkflow"]["priorDirectorReturn"] is None, {"conference129": old_packet_record["status"], "sourceConference01": delivery["historicalWorkflow"]["sourceConference01"]})
    add(checks, "Preserved question, main-case and future-requirement counts reconcile", len(old_candidate["questions"]) == len(notes["completeOriginalQuestionsUnchanged"]) == 24 and len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["allQuestions"]) == 26 and len(notes["requiredNewCases"]) == 4 and len(old_candidate["futureCaseRequirements"]) == len(notes["originalFutureCaseRequirementsUnchanged"]) == 8 and (delivery["originalQuestions"], delivery["focusedAdditionalQuestions"], delivery["requiredMainCases"], delivery["futureRequirements"]) == (24, 2, 4, 8), {"originalQuestions": 24, "focusedAdditions": 2, "totalQuestions": 26, "mainCases": 4, "futureRequirements": 8})
    add(checks, "Prepared candidate adopts no new rules and retains the exact two source records", candidate["newRuleAdoptions"] == 0 and [row["spellId"] for row in candidate["records"]] == TARGETS and candidate["currentAuthority"] == AUTHORITY and candidate["sourceBindingRefresh"]["sourceFiles"] == 135, {"newRuleAdoptions": candidate["newRuleAdoptions"], "recordIds": [row["spellId"] for row in candidate["records"]]})

    with zipfile.ZipFile(ARCHIVE) as packet, zipfile.ZipFile(SOURCE_ARCHIVE) as historical:
        names = packet.namelist()
        manifest = read_member(packet, "MANIFEST.json")
        rows = {row["path"]: row for row in manifest["members"]}
        payload = set(names) - {"MANIFEST.json"}
        unsafe = [name for name in names if name.startswith(("/", "\\")) or "\\" in name or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts]
        manifest_digest = member_digest(packet, "MANIFEST.json")
        add(checks, "ZIP contains exactly 183 unique safe members matching the internal manifest", len(names) == len(set(names)) == delivery["members"] == 183 and len(rows) == len(payload) == manifest["memberCountExcludingSelf"] == 182 and set(rows) == payload and not unsafe and packet.testzip() is None, {"members": len(names), "payloadMembers": len(payload), "manifestBytes": manifest_digest[0], "manifestSha256": manifest_digest[1], "unsafe": unsafe[:5]})
        failures = [name for name, row in rows.items() if member_digest(packet, name) != (row["bytes"], row["sha256"], row["crc32"].lower())]
        add(checks, "Every payload member independently matches the internal manifest", not failures, {"checked": len(rows), "failures": failures[:8]})

        source_member = "historical/DD_Rank9_Projection_Confinement_2_Source_Conference_01.zip"
        add(checks, "Historical source-conference archive is embedded byte-exactly", historical.testzip() is None and member_digest(packet, source_member) == (source_archive_size, source_archive_sha, source_archive_crc) and packet.read(source_member) == SOURCE_ARCHIVE.read_bytes(), {"bytes": source_archive_size, "sha256": source_archive_sha, "members": len(historical.namelist())})
        changed_paths = []
        source_failures = []
        with zipfile.ZipFile(SOURCE_ARCHIVE) as original_source:
            for old in old_candidate["sourceBindings"]:
                path = old["path"]
                hist_name = "sources/" + path
                current_name = "sources_current/" + path
                current_bytes = (ROOT / path).read_bytes()
                refreshed = next(row for row in candidate["sourceBindings"] if row["path"] == path)
                if member_digest(original_source, hist_name)[:2] != (old["bytes"], old["sha256"]):
                    source_failures.append(path + " historical binding")
                if current_name not in names or packet.read(current_name) != current_bytes or member_digest(packet, current_name)[:2] != (refreshed["bytes"], refreshed["sha256"]) or (len(current_bytes), hashlib.sha256(current_bytes).hexdigest()) != (refreshed["bytes"], refreshed["sha256"]):
                    source_failures.append(path + " current binding")
                if (old["bytes"], old["sha256"]) != (refreshed["bytes"], refreshed["sha256"]):
                    changed_paths.append(path)
        add(checks, "All 135 historical bindings and refreshed current source bytes reconcile", len(old_candidate["sourceBindings"]) == len(candidate["sourceBindings"]) == delivery["sourceBindings"] == 135 and not source_failures and set(changed_paths) == {row["path"] for row in candidate["sourceBindingRefresh"]["changedSinceHistoricalCandidate"]}, {"bindings": 135, "changedBindings": len(changed_paths), "failures": source_failures[:8]})
        add(checks, "Historical notes, packet record, preparation, check and request are included byte-exactly", packet.read("historical/NEXT_CONFERENCE_NOTES_129.json") == SOURCE_NOTES.read_bytes() and packet.read("historical/PACKET_129_SUBMISSION_RECORD.json") == SOURCE_PACKET_RECORD.read_bytes() and packet.read("historical/SOURCE_CONFERENCE_PREPARATION_01.json") == (ROOT / "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_PREPARATION.json").read_bytes() and packet.read("historical/SOURCE_CONFERENCE_CHECK_01.json") == (ROOT / "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_CHECK.json").read_bytes() and packet.read("historical/SOURCE_CONFERENCE_REQUEST_01.txt") == (ROOT / "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_REQUEST.txt").read_bytes(), {"questions": len(notes["allQuestions"]), "priorStatus": old_packet_record["status"]})

        return_failures = []
        for number, (folder, archive_name, delivery_name, audit_name, receipt_name) in RECENT.items():
            base = AUDIT / folder
            for relative, local in ((f"evidence/RETURN{number}.zip", base / archive_name), (f"evidence/RETURN{number}_DELIVERY.json", base / delivery_name)):
                if relative not in names or packet.read(relative) != local.read_bytes():
                    return_failures.append(relative)
            for name, relative in ((audit_name, f"current/evidence/RETURN{number}_INDEPENDENT_AUDIT.json"), (receipt_name, f"current/evidence/RETURN{number}_RECEIPT.json")):
                local = AUDIT / name
                if relative not in names or packet.read(relative) != local.read_bytes():
                    return_failures.append(relative)
        add(checks, "Return284–287 archives, matching deliveries, independent audits and receipts are embedded byte-exactly", not return_failures, {"returns": sorted(RECENT), "failures": return_failures[:8]})

        queue = read_member(packet, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_288.json")
        handoff = read_member(packet, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_288.json")
        pending = read_member(packet, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_288.json")
        submission287 = read_member(packet, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_SUBMISSION.json")
        target_row = next(row for row in queue["currentPendingGroups"] if row["group"] == "rank9-projection-confinement2")
        add(checks, "Queue, handoff and pending audit retain authority and identify only the next two IDs", queue["currentAuthority"] == handoff["currentAuthority"] == pending["authority"] == AUTHORITY and target_row["pendingIds"] == TARGETS and target_row["pendingCount"] == 2 and handoff["nextGroup"] == "rank9-projection-confinement2" and handoff["nextPendingCount"] == 2 and pending["pendingCount"] == 32, {"authority": queue["currentAuthority"], "targetIds": target_row["pendingIds"]})
        add(checks, "Return287 submission record and queue preserve the five held decisions", submission287["status"] == "RETURN287_AUDITED_HELD_816_32_0" and submission287["directorReturn"]["acceptedIds"] == [] and submission287["directorReturn"]["appliedIds"] == [] and submission287["directorReturn"]["heldIds"] == HELD287 and queue["lastReviewedBatch"]["heldIds"] == HELD287, {"submissionStatus": submission287["status"], "heldIds": submission287["directorReturn"]["heldIds"]})
        # Queue snapshot predates attachment of packet288; verify its unresolved next request and prior return explicitly.
        add(checks, "Packet requests only target 288 and carries all prior holds without canonical/application changes", "Review ONLY astral-projection and imprisonment" in packet.read("REQUEST_288.txt").decode("utf-8") and context["preservedRecentHolds"] == delivery["preservedRecentHolds"] and delivery["canonicalChanges"] is False and delivery["applicationChanges"] is False and candidate["newRuleAdoptions"] == 0, {"preservedHolds": [(row["returnNumber"], row["heldIds"]) for row in delivery["preservedRecentHolds"]]})

    failures = [row for row in checks if not row["passed"]]
    report = {
        "id": "RANK9PROJECTIONCONFINEMENT2-PACKET288-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL",
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_size, "sha256": delivery_sha, "crc32": delivery_crc},
        "authority": delivery["sourceAuthority"], "targetIds": TARGETS,
        "questions": 26, "requiredMainCases": 4, "futureRequirements": 8,
        "sourceBindings": 135, "changedHistoricalBindings": len(candidate["sourceBindingRefresh"]["changedSinceHistoricalCandidate"]),
        "preservedReturns": sorted(RECENT),
        "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_size, report_sha, report_crc = file_digest(REPORT)
    receipt = {"id": "RANK9PROJECTIONCONFINEMENT2-PACKET288-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"], "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), "bytes": report_size, "sha256": report_sha, "crc32": report_crc}, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures)}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    packet_record.update({"status": "PACKET288_INDEPENDENT_AUDIT_PASS_PENDING_GPT_SUBMISSION" if not failures else "PACKET288_INDEPENDENT_AUDIT_FAILED", "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), "bytes": report_size, "sha256": report_sha}, "auditReceipt": {"path": RECEIPT.relative_to(ROOT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": hashlib.sha256(RECEIPT.read_bytes()).hexdigest()}, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures)})
    PACKET_RECORD.write_text(json.dumps(packet_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "archiveSha256": archive_sha, "deliverySha256": delivery_sha, "report": str(REPORT), "receipt": str(RECEIPT), "failed": failures}, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
