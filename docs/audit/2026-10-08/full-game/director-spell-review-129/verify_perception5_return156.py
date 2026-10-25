from __future__ import annotations

import copy
import hashlib
import json
import sys
import zlib
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from verify_perception5_sourceconference02_156 import verify as verify_source_packet

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "perception5_return156_received"
ARCHIVE = RECEIVED / "DD_Rank8_Perception5_Director_Return156.zip"
DELIVERY = RECEIVED / "DIRECTOR_RETURN_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank8_Perception_5_Source_Conference_02.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_perception_5_source_conference_02.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_156.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_157.json"
PENDING = AUDIT / "CURRENT130_PENDING_IDENTITY_AUDIT_155.json"
IDS = ["mass-hallucination", "illusory-dragon", "phantom-execution", "antipathy-sympathy", "glibness"]
EXPECTED_COUNTS = {
    "procedures": 5,
    "conferenceQuestionDispositions": 23,
    "originalIdentityQuestionDispositions": 5,
    "futureObligations": 7,
    "requiredMainCases": 10,
    "additionalBranches": 58,
    "totalCases": 68,
    "wholeCaseHeld": 31,
    "events": 186,
    "eventOperations": 744,
    "proposalOperations": 20,
    "retainedHoldCategories": 14,
}
EXPECTED_AUTHORITY = {
    "reviewedApplied": 718,
    "pending": 130,
    "acceptedUnapplied": 0,
    "completeReviewedStandaloneProcedures": 442,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def apply_root_patch(state, operations):
    result = copy.deepcopy(state)
    for operation in operations:
        assert operation["path"] == "", f"Unexpected nested mutation: {operation['path']}"
        if operation["op"] == "test":
            assert result == operation["value"], "RFC6902 test does not match the complete state"
        elif operation["op"] == "replace":
            result = copy.deepcopy(operation["value"])
        else:
            raise AssertionError(f"Unexpected operation: {operation['op']}")
    return result


def verify() -> dict:
    source_report = verify_source_packet()
    assert source_report["status"] == "PASS" and source_report["failures"] == 0
    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    archive_hash = sha(archive_bytes)
    assert len(archive_bytes) == delivery["archive"]["bytes"] == 15_465_602
    assert archive_hash == delivery["archive"]["sha256"] == "1726d1b99a17643e358e459104162965260949aa1f032cb71a7c9c15accf3d68"
    assert delivery["archive"]["fileName"] == ARCHIVE.name
    assert delivery["accepted"] is True and delivery["applied"] is False
    assert delivery["acceptedIds"] == IDS and delivery["inputAuthorityUnchanged"] == EXPECTED_AUTHORITY
    assert delivery["canonicalAppliedCountStill"] == 718 and delivery["canonicalPendingCountStill"] == 130
    assert delivery["newAcceptedUnappliedIdentities"] == 5 and delivery["canonicalIndexCatalogEdited"] is False
    assert delivery["counts"] == EXPECTED_COUNTS and delivery["archiveMembers"] == 98
    assert delivery["validation"]["independentStaticChecksPassed"] == 18_889
    assert delivery["validation"]["staticFailures"] == 0 and delivery["validation"]["packageFailures"] == 0
    assert delivery["validation"]["exactAcceptedSnapshotComparisons"] == 19
    assert delivery["validation"]["currentSourceFilesVerified"] == 96
    assert delivery["validation"]["acceptedInterfaceTextHashesVerified"] == 31
    assert delivery["validation"]["packageMemberRoundTripChecksPassed"] == 493
    assert delivery["validation"]["sourceArchiveCandidateByteExact"] is True
    assert delivery["qualifications"]["staticAuthoredReviewOnly"] is True
    for key in ("runtimeApproval", "humanPlayApproval", "balanceApproval", "cosmologyApproval", "releaseApproval", "domainClosure", "canonicalApplication", "closedCohortsReopened", "suppliedOrHistoricalProgramsExecuted"):
        assert delivery["qualifications"][key] is False, key
    assert delivery["holds"]["retainedCategories"] == 14
    assert delivery["holds"]["wholeCaseHeld"] == 31
    assert delivery["holds"]["allInheritedHoldsRetained"] is True
    assert delivery["holds"]["heldCasesPromotedToCampaignSuccess"] is False

    index_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    index = json.loads(index_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE)
    handoff = read_json(HANDOFF)
    pending = read_json(PENDING)
    assert index["authoredCounts"] == {"reviewed": 718, "pending": 130}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 442
    assert handoff["currentAuthority"]["reviewedApplied"] == 718
    assert handoff["currentAuthority"]["pending"] == 130
    assert handoff["currentAuthority"]["acceptedUnapplied"] == 0
    assert handoff["currentIndexBinding"]["sha256"] == sha(index_bytes)
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_bytes)
    assert handoff["currentQueueBinding"]["sha256"] == sha(QUEUE.read_bytes())
    assert pending["pendingCount"] == 130 and pending["indexBinding"]["sha256"] == sha(index_bytes)
    assert pending["catalogBinding"]["sha256"] == sha(catalog_bytes)
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 130 and set(pending["pendingIds"]) == live_pending
    first_group = queue["currentPendingGroups"][0]
    assert first_group["group"] == "rank8-perception5" and first_group["pendingIds"] == IDS
    assert queue["currentAuthority"]["reviewedApplied"] == 718 and queue["currentAuthority"]["pending"] == 130
    assert handoff["nextGroup"] == "rank8-perception5"

    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == 98 and archive.testzip() is None
        for name in names:
            path = PurePosixPath(name)
            assert name and not path.is_absolute() and ".." not in path.parts and "\\" not in name
            assert not any(part.startswith(".") for part in path.parts)
        raw_members = {name: archive.read(name) for name in names}
        member_manifest_bytes = raw_members["MANIFEST.json"]
        member_manifest = json.loads(member_manifest_bytes.decode("utf-8-sig"))
        external_binding = delivery["memberManifest"]
        assert external_binding["path"] == "MANIFEST.json"
        assert len(member_manifest_bytes) == external_binding["bytes"]
        assert sha(member_manifest_bytes) == external_binding["sha256"]
        assert f"{zlib.crc32(member_manifest_bytes) & 0xffffffff:08x}" == external_binding["crc32"].lower()
        assert member_manifest["accepted"] is True and member_manifest["applied"] is False
        assert member_manifest["inputAuthority"] == EXPECTED_AUTHORITY
        assert member_manifest["archiveMemberCount"] == 98
        assert member_manifest["memberCountExcludingManifest"] == 97
        assert member_manifest["selfBinding"] == "MANIFEST.json is bound by the separate delivery JSON and the archive SHA256; every other archive member is exactly listed here."
        rows = {row["path"]: row for row in member_manifest["members"]}
        assert len(rows) == 97 and set(rows) == set(names) - {"MANIFEST.json"}
        for name, row in rows.items():
            raw = raw_members[name]
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"], name
            assert f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"].lower(), name

        model = json.loads(raw_members["MODEL.json"])
        decision = json.loads(raw_members["DIRECTOR_DECISION.json"])
        counts = json.loads(raw_members["COVERAGE.json"])["counts"]
        casebook_doc = json.loads(raw_members["CASEBOOK.json"])
        cases = casebook_doc["cases"]
        holds = json.loads(raw_members["HOLDS.json"])
        dispositions = json.loads(raw_members["QUESTION_DISPOSITIONS.json"])
        original = json.loads(raw_members["ORIGINAL_SOURCE_RECORDS.json"])
        proposal_ops = json.loads(raw_members["PROPOSAL_OPERATIONS.json"])
        independent = json.loads(raw_members["validation/INDEPENDENT_FAILURE_CHECK.json"])
        source_verification = json.loads(raw_members["evidence/SOURCE_VERIFICATION.json"])
        comparison_checks = json.loads(raw_members["evidence/EXACT_COMPARISON_SNAPSHOT_CHECKS.json"])
        interface_boundaries = json.loads(raw_members["evidence/ACCEPTED_INTERFACE_BOUNDARIES.json"])
        assert model["id"] == decision["id"] == "Perception5-Director-Return156"
        assert delivery["id"] == "Perception5-Director-Return156-DELIVERY"
        assert model["accepted"] is True and model["applied"] is False and model["canonicalMutation"] is False
        assert decision["accepted"] is True and decision["applied"] is False and decision["acceptedIds"] == IDS
        assert decision["rejectedIds"] == [] and decision["blockers"] == []
        assert decision["inputAuthorityUnchanged"] == EXPECTED_AUTHORITY
        assert decision["canonicalIndexCatalogEdited"] is False
        assert model["inputAuthority"] == EXPECTED_AUTHORITY
        assert model["counts"] == decision["counts"] == counts == EXPECTED_COUNTS
        assert delivery["counts"] == counts
        assert model["approvalQualifications"] == delivery["qualifications"]

        source_archive_bytes = SOURCE_ARCHIVE.read_bytes()
        candidate_bytes = SOURCE_CANDIDATE.read_bytes()
        assert raw_members["source/DD_Rank8_Perception_5_Source_Conference_02.zip"] == source_archive_bytes
        assert len(source_archive_bytes) == source_verification["archive"]["bytes"]
        assert sha(source_archive_bytes) == source_verification["archive"]["sha256"]
        assert source_verification["currentFilesVerified"] == 96
        source_authority = source_verification["currentAuthorityUnchanged"]
        assert {key: source_authority[key] for key in EXPECTED_AUTHORITY} == EXPECTED_AUTHORITY
        for key in ("index", "catalog", "currentQueue", "pendingIdentityAudit", "priorHandoff"):
            binding = source_authority[key]
            bound_path = ROOT / PurePosixPath(binding["path"])
            bound_bytes = bound_path.read_bytes()
            assert len(bound_bytes) == binding["bytes"] and sha(bound_bytes) == binding["sha256"]
        current_files = source_verification["currentFiles"]
        assert len(current_files) == 96 and all(row["verified"] is True for row in current_files)
        with ZipFile(SOURCE_ARCHIVE) as source_archive:
            source_names = source_archive.namelist()
            assert source_archive.testzip() is None and len(source_names) == 107
            assert source_archive.read("CANDIDATE.json") == candidate_bytes
            for row in current_files:
                live = (ROOT / PurePosixPath(row["path"])).read_bytes()
                frozen = source_archive.read("sources/" + row["path"])
                assert len(live) == len(frozen) == row["bytes"]
                assert sha(live) == sha(frozen) == row["sha256"], row["path"]
        assert source_verification["historicalConference01Authority"] is False
        assert source_verification["programsExecuted"] is False

        candidate = json.loads(raw_members["source/CANDIDATE.json"])
        assert raw_members["source/CANDIDATE.json"] == candidate_bytes
        assert candidate["currentAuthority"]["reviewedApplied"] == 718
        assert candidate["currentAuthority"]["pending"] == 130
        candidate_rows = {row["spellId"]: row for row in candidate["records"]}
        catalog_rows = {row["id"]: row for row in catalog["spells"]}
        index_rows = {row["id"]: row for row in index["entries"]}
        assert list(model["spells"]) == IDS and set(model["spells"]) == set(IDS)
        binding_rows = {row["id"]: row for row in decision["exactProcedureBindings"]}
        for sid in IDS:
            proc = model["spells"][sid]
            assert proc["id"] == sid
            native = proc["completeNativeSourceAndAccess"]
            assert native == catalog_rows[sid]
            assert native == candidate_rows[sid]["completeCurrentCatalogSourceAndAccess"]
            assert candidate_rows[sid]["currentIndexEntry"] == index_rows[sid]
            assert index_rows[sid]["authoredStatus"] == "pending-authored-procedure"
            assert index_rows[sid]["procedureFile"] == "catalog.json"
            assert proc["authorship"] == "NEW spell-local director proposal"
            assert set(proc["qualificationHoldIds"]) == {hold["id"] for hold in holds}
            proc_path = f"procedures/{sid}.json"
            proc_bytes = raw_members[proc_path]
            assert json.loads(proc_bytes) == proc
            bound_proc = binding_rows[sid]
            assert bound_proc["path"] == proc_path and bound_proc["bytes"] == len(proc_bytes)
            assert bound_proc["sha256"] == sha(proc_bytes)
            assert proc["caseIds"] and set(proc["caseIds"]) <= {case["id"] for case in cases}
            assert proc["questionIds"]

        assert len(dispositions) == 23 and len({row["id"] for row in dispositions}) == 23
        assert all(row["decisionSelected"] is True and row.get("originalQuestionUnchanged") for row in dispositions)
        assert len(original["originalIdentityQuestions"]) == 5
        assert len(original["requiredCasesUnchanged"]) == 10
        assert len(original["futureObligationsUnchanged"]) == 7
        assert len(model["originalIdentityDispositions"]) == 5
        assert len(model["futureObligationDispositions"]) == 7

        assert len(holds) == 14 and len({row["id"] for row in holds}) == 14
        assert len({row["category"] for row in holds}) == 14
        assert all(row["retained"] is True for row in holds)
        hold_ids = {row["id"] for row in holds}
        assert {row["id"] for row in holds} == {f"P156-H{i:02d}" for i in range(1, 15)}
        assert all(set(case["qualificationHoldIds"]) <= hold_ids for case in cases)
        assert all(set(case.get("wholeCaseHolds", [])) <= hold_ids for case in cases)
        assert sum(bool(case.get("wholeCaseHolds")) for case in cases) == 31
        assert sum(case["status"] == "held-dependent-branch" for case in cases) == 31
        assert sum(case["kind"] == "required-main" for case in cases) == 10
        assert sum(case["kind"] == "adverse-or-distinct-branch" for case in cases) == 58
        assert all(case["isActualCampaignSuccess"] is False for case in cases)
        case_by_id = {case["id"]: case for case in cases}
        assert len(case_by_id) == 68
        case_files = {name.removeprefix("cases/").removesuffix(".json") for name in names if name.startswith("cases/") and name.endswith(".json")}
        assert case_files == set(case_by_id)
        for case_id, case in case_by_id.items():
            assert json.loads(raw_members[f"cases/{case_id}.json"]) == case

        replayed_events = 0
        replayed_operations = 0
        event_ids = set()
        for case in cases:
            previous = case["initial"]
            for event in case["events"]:
                assert event["id"] not in event_ids
                event_ids.add(event["id"])
                assert previous == event["before"], f"Discontinuous state chain: {event['id']}"
                assert sha(canonical(event["before"])) == event["beforeSHA256"]
                assert sha(canonical(event["after"])) == event["afterSHA256"]
                assert apply_root_patch(event["before"], event["forward"]) == event["after"]
                assert apply_root_patch(event["after"], event["inverse"]) == event["before"]
                replayed_operations += len(event["forward"]) + len(event["inverse"])
                previous = event["after"]
                replayed_events += 1
            assert previous == case["final"]
        assert replayed_events == 186 and replayed_operations == 744

        assert len(proposal_ops) == 5 and [row["id"] for row in proposal_ops] == IDS
        proposal_operations = 0
        comparison_archive_path_relocations = []
        for row in proposal_ops:
            assert row["target"] == "isolated proposal only, not canonical index/catalog"
            assert row["before"]["native"] == row["after"]["native"]
            assert row["after"]["proposedProcedure"] == model["spells"][row["id"]]
            assert sha(canonical(row["before"])) == row["beforeSHA256"]
            assert sha(canonical(row["after"])) == row["afterSHA256"]
            assert apply_root_patch(row["before"], row["forward"]) == row["after"]
            assert apply_root_patch(row["after"], row["inverse"]) == row["before"]
            proposal_operations += len(row["forward"]) + len(row["inverse"])
        assert proposal_operations == 20

        assert independent["status"] == "PASS" and independent["checksExecuted"] == 18_889
        assert independent["failures"] == 0 and independent["blockers"] == []
        assert independent["counts"] == EXPECTED_COUNTS
        assert comparison_checks["status"] == "PASS"
        assert comparison_checks["noClosedCasesRepeated"] is True
        assert comparison_checks["sourceProgramsExecuted"] is False
        assert comparison_checks["laterEditsPromoted"] is False
        assert len(comparison_checks["checks"]) == 19
        for row in comparison_checks["checks"]:
            if "byteBindingVerified" in row:
                assert row["byteBindingVerified"] is True
                assert row["exactAcceptedCardEqualsComparisonEnvelope"] is True
                assert row["historicalCountsAdopted"] is False
            elif "currentOperationalCardEqualsRecordedAcceptedCatalogCard" in row:
                assert row["currentOperationalCardEqualsRecordedAcceptedCatalogCard"] is True
            else:
                archive_binding = row["exactAcceptedArchiveBinding"]
                accepted_archive_path = ROOT / PurePosixPath(archive_binding["path"])
                if not accepted_archive_path.exists():
                    relative_to_full = PurePosixPath(archive_binding["path"]).relative_to("docs/audit/2026-10-08/full-game")
                    accepted_archive_path = AUDIT / Path(*relative_to_full.parts)
                    comparison_archive_path_relocations.append({"recordedPath": archive_binding["path"], "presentAt": accepted_archive_path.relative_to(ROOT).as_posix()})
                accepted_archive_bytes = accepted_archive_path.read_bytes()
                assert len(accepted_archive_bytes) == archive_binding["bytes"]
                assert sha(accepted_archive_bytes) == archive_binding["sha256"]
                assert row["acceptedArchiveByteBindingVerified"] is True
                assert row["archiveCRCVerified"] is True
                assert row["currentDirectorProcedureRecordEqualsExactAcceptedMember"] is True
                with ZipFile(accepted_archive_path) as accepted_archive:
                    assert accepted_archive.testzip() is None
                    accepted_member = accepted_archive.read(row["member"])
                    assert len(accepted_member) == row["memberBytes"]
                    assert sha(accepted_member) == row["memberSHA256"]
                    preserved = json.loads(raw_members[row["preservedMember"]])
                    assert preserved == json.loads(accepted_member)
        assert len(interface_boundaries["interfaces"]) == 31
        assert all(row["exactTextHashMatches"] and row["exactCurrentEqualsHistoricalAcceptedEntry"] for row in interface_boundaries["interfaces"])
        assert len(interface_boundaries["comparisonGroupsUnchanged"]) == 5
        assert len(interface_boundaries["closedIllusionComparisonsUnchanged"]) == 6
        assert len(interface_boundaries["completeAcceptedCounterpartsUnchanged"]) == 9
        assert interface_boundaries["nonAcceptanceOfLaterSourceChangesUnchanged"]
        assert casebook_doc["status"] == "data-only-proposed-cases"
        assert casebook_doc["canonicalApplication"] is False

    return {
        "id": "PERCEPTION5-RETURN156-INDEPENDENT-VERIFICATION",
        "status": "PASS",
        "acceptedIds": IDS,
        "inputAuthority": EXPECTED_AUTHORITY,
        "archiveBytes": len(archive_bytes),
        "archiveSha256": archive_hash,
        "deliveryBytes": len(delivery_bytes),
        "deliverySha256": sha(delivery_bytes),
        "archiveMembersVerified": 98,
        "listedMemberHashesAndCRCsVerified": 97,
        "sourceFilesVerified": 96,
        "acceptedInterfaceBoundariesVerified": 31,
        "exactComparisonSnapshotsVerified": 19,
        "questionDispositionsVerified": 23,
        "holdsRetained": 14,
        "wholeCasesHeld": 31,
        "casesVerified": 68,
        "eventsReplayed": replayed_events,
        "forwardAndInverseOperationsReplayed": replayed_operations,
        "proposalOperationsReplayed": proposal_operations,
        "comparisonArchivePathRelocationsVerified": comparison_archive_path_relocations,
        "catalogUnchangedAtInput": True,
        "canonicalIndexUnchangedAtInput": True,
        "runtimeTests": 0,
        "failures": 0,
    }


if __name__ == "__main__":
    report = verify()
    output = AUDIT / "PERCEPTION5_RETURN156_INDEPENDENT_VERIFICATION.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
