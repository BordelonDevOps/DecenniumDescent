from __future__ import annotations

import copy
import hashlib
import json
import zlib
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
RECEIVED = AUDIT / "summonstructure5_return153_received"
ARCHIVE = RECEIVED / "DD_Rank8_SummonStructure5_Director_Return153.zip"
DELIVERY = RECEIVED / "DIRECTOR_RETURN_DELIVERY.json"
IDS = [
    "summon-greater-water-pet",
    "summon-archlich-shade",
    "faction-paragon",
    "conjure-sky-fortress",
    "shifting-fortress",
]
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_ARCHIVE = FULL / "DD_Rank8_Summon_Structure_5_Source_Conference_02.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_summon_structure_5_source_conference_02.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_154.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_154.json"
PENDING = AUDIT / "CURRENT135_PENDING_IDENTITY_AUDIT_152.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def apply_root_patch(state, ops):
    result = copy.deepcopy(state)
    for op in ops:
        assert op["path"] == "", f"Unexpected non-root operation path: {op['path']}"
        if op["op"] == "test":
            assert result == op["value"], "Root test operation does not match state"
        elif op["op"] == "replace":
            result = copy.deepcopy(op["value"])
        else:
            raise AssertionError(f"Unexpected operation type: {op['op']}")
    return result


def verify() -> dict:
    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    assert len(archive_bytes) == delivery["bytes"] == 41_702_103
    assert sha(archive_bytes) == delivery["sha256"] == "91c026b2fde479c949bdedb6c2cfca6055437447cd5232078307b40da191b977"
    assert delivery["filename"] == ARCHIVE.name
    assert delivery["accepted"] is True and delivery["applied"] is False
    assert delivery["canonicalMutation"] is False
    assert delivery["acceptedIds"] == IDS
    expected_authority = {
        "reviewedApplied": 713,
        "pending": 135,
        "acceptedUnapplied": 0,
        "completeReviewedStandaloneProcedures": 437,
    }
    assert delivery["inputAuthority"] == expected_authority
    assert delivery["newAcceptedUnappliedProceduresInThisDecision"] == 5

    current_bindings = {
        "index": INDEX,
        "catalog": CATALOG,
        "sourceArchive": SOURCE_ARCHIVE,
        "sourceCandidate": SOURCE_CANDIDATE,
        "queue": QUEUE,
        "handoff": HANDOFF,
        "pendingIdentityAudit": PENDING,
    }
    current = {key: path.read_bytes() for key, path in current_bindings.items()}
    handoff = json.loads(current["handoff"])
    queue = json.loads(current["queue"])
    pending_doc = json.loads(current["pendingIdentityAudit"])
    index = json.loads(current["index"])
    catalog = json.loads(current["catalog"])
    candidate = json.loads(current["sourceCandidate"])
    assert handoff["currentAuthority"]["reviewedApplied"] == 713
    assert handoff["currentAuthority"]["pending"] == 135
    assert handoff["currentAuthority"]["acceptedUnapplied"] == 0
    assert handoff["currentIndexBinding"]["bytes"] == len(current["index"])
    assert handoff["currentIndexBinding"]["sha256"] == sha(current["index"])
    assert handoff["currentCatalogBinding"]["bytes"] == len(current["catalog"])
    assert handoff["currentCatalogBinding"]["sha256"] == sha(current["catalog"])
    assert handoff["currentQueueBinding"]["sha256"] == sha(current["queue"])
    assert pending_doc["pendingCount"] == 135
    assert pending_doc["indexBinding"]["sha256"] == sha(current["index"])
    assert pending_doc["catalogBinding"]["sha256"] == sha(current["catalog"])
    assert index["authoredCounts"] == {"reviewed": 713, "pending": 135}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 437
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 135 and set(IDS) <= live_pending
    assert set(pending_doc["pendingIds"]) == live_pending
    first_group = queue["currentPendingGroups"][0]
    assert first_group["group"] == "rank8-summon-structure5" and first_group["pendingIds"] == IDS
    assert candidate["currentAuthority"]["reviewedApplied"] == 713
    assert candidate["currentAuthority"]["pending"] == 135
    candidate_rows = {row["spellId"]: row for row in candidate["records"]}
    assert all(sid in candidate_rows for sid in IDS)

    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == 246 and archive.testzip() is None
        for name in names:
            path = PurePosixPath(name)
            assert name and not path.is_absolute() and ".." not in path.parts and "\\" not in name
            assert not any(part.startswith(".") for part in path.parts)
        delivery_manifest = delivery["memberManifest"]
        manifest_bytes = archive.read("MEMBER_MANIFEST.json")
        assert len(manifest_bytes) == delivery_manifest["bytes"]
        assert sha(manifest_bytes) == delivery_manifest["sha256"]
        assert f"{zlib.crc32(manifest_bytes) & 0xffffffff:08x}" == delivery_manifest["crc32"].lower()
        member_manifest = json.loads(manifest_bytes)
        assert member_manifest["memberCount"] == len(names)
        assert member_manifest["payloadMemberCount"] == len(names) - 1
        assert member_manifest["noHiddenOrTemporaryMembers"] is True
        assert member_manifest["accepted"] is True and member_manifest["applied"] is False
        assert set(member_manifest["archiveMemberAllowlist"]) == set(names)
        member_rows = {row["path"]: row for row in member_manifest["members"]}
        assert len(member_rows) == len(names) - 1
        assert set(member_rows) == set(names) - {"MEMBER_MANIFEST.json"}
        raw_members = {name: archive.read(name) for name in names}
        for name, row in member_rows.items():
            raw = raw_members[name]
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"], name
            assert f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"].lower(), name

        model = json.loads(raw_members["MODEL.json"])
        counts = json.loads(raw_members["COUNTS.json"])
        decision = json.loads(raw_members["DIRECTOR_DECISION.json"])
        validation = json.loads(raw_members["VALIDATION.json"])
        dispositions = json.loads(raw_members["QUESTION_DISPOSITIONS.json"])
        original_dispositions = json.loads(raw_members["ORIGINAL_QUESTION_DISPOSITIONS.json"])
        original_sources = json.loads(raw_members["ORIGINAL_SOURCE_RECORDS.json"])
        holds = json.loads(raw_members["HOLDS.json"])
        proposal_ops = json.loads(raw_members["PROPOSAL_OPERATIONS.json"])
        source_verification = json.loads(raw_members["SOURCE_VERIFICATION.json"])
        evidence_manifest = json.loads(raw_members["EVIDENCE_MANIFEST.json"])
        coverage = json.loads(raw_members["COVERAGE.json"])

        assert model["accepted"] is True and model["applied"] is False and model["canonicalMutation"] is False
        assert model["inputAuthority"] == expected_authority
        assert list(model["spells"]) == IDS and set(model["spells"]) == set(IDS)
        assert decision["accepted"] is True and decision["applied"] is False
        assert decision["canonicalFilesChanged"] is False and decision["acceptedIds"] == IDS
        assert decision["inputAuthority"] == expected_authority
        assert decision["remainingStaticBlockers"] == []
        assert decision["validation"]["checks"] == 50_589 and decision["validation"]["passed"] is True
        assert validation["passed"] is True and validation["checks"] == 50_589
        assert counts == delivery["counts"]
        assert counts["procedures"] == 5 and counts["conferenceQuestions"] == 20
        assert counts["originalIdentityQuestions"] == 5 and counts["futureObligations"] == 7
        assert counts["mainCases"] == 10 and counts["branches"] == 92 and counts["cases"] == 102
        assert counts["heldDependentBranches"] == 57 and counts["events"] == 620
        assert counts["eventOperations"] == 2_480 and counts["proposalOperations"] == 20
        assert counts["holdCategories"] == 15 and counts["staticChecks"] == 50_589
        assert len(holds) == 15 and all(row["retained"] is True for row in holds)
        assert len(dispositions) == 20 and all(row["decisionSelected"] is True for row in dispositions)
        source2_candidate = json.loads(raw_members["evidence/source02/CANDIDATE.json"])
        assert {row["id"] for row in dispositions} == {row["id"] for row in source2_candidate["questions"]}
        assert len(original_dispositions) == 5
        assert len(original_sources["originalIdentityQuestions"]) == 5
        assert len(original_sources["futureObligationsUnchanged"]) == 7
        assert len(proposal_ops) == 5 and [row["id"] for row in proposal_ops] == IDS
        assert all(row["target"] == "isolated-proposal-only" for row in proposal_ops)
        for row in proposal_ops:
            assert row["before"]["native"] == row["after"]["native"]

        # Exact identity, source-card, original-question, and procedure bindings.
        catalog_rows = {row["id"]: row for row in catalog["spells"]}
        index_rows = {row["id"]: row for row in index["entries"]}
        for sid in IDS:
            proc = model["spells"][sid]
            native = proc["nativeUnchanged"]
            assert native == catalog_rows[sid]
            assert native == candidate_rows[sid]["completeCurrentCatalogSourceAndAccess"]
            assert native["id"] == sid
            assert index_rows[sid]["authoredStatus"] == "pending-authored-procedure"
            proc_name = f"procedures/{sid}.json"
            assert proc_name in raw_members
            assert json.loads(raw_members[proc_name]) == proc
            decrow = next(row for row in decision["procedures"] if row["id"] == sid)
            assert len(raw_members[proc_name]) == decrow["bytes"]
            assert sha(raw_members[proc_name]) == decrow["sha256"]

        # Every source binding and every inert exact-accepted evidence member must match.
        assert source_verification["archive"]["bytes"] == len(current["sourceArchive"])
        assert source_verification["archive"]["sha256"] == sha(current["sourceArchive"])
        assert source_verification["archive"]["publicDownloadIdentical"] is True
        bound = source_verification["boundSourceFiles"]
        assert len(bound) == 77 and all(row["verified"] is True for row in bound)
        for row in bound:
            live = (ROOT / PurePosixPath(row["path"])).read_bytes()
            packaged = raw_members[row["packaged"]]
            assert len(live) == len(packaged) == row["bytes"]
            assert sha(live) == sha(packaged) == row["sha256"]
        source_archive_member = "history/DD_Rank8_Summon_Structure_5_Source_Conference_02.zip"
        assert raw_members[source_archive_member] == current["sourceArchive"]
        assert evidence_manifest["count"] == 120 and len(evidence_manifest["members"]) == 120
        for row in evidence_manifest["members"]:
            raw = raw_members[row["path"]]
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]

        # All fixture event chains are contiguous and their full-state forward/inverse operations replay.
        casebook = json.loads(raw_members["CASEBOOK.json"])
        assert len(casebook) == 102
        assert sum(case["kind"] == "main" for case in casebook) == 10
        assert sum(case["kind"] == "branch" for case in casebook) == 92
        assert sum(case["status"] == "held-dependent-branch" for case in casebook) == 57
        replayed_events = 0
        total_ops = 0
        for case in casebook:
            previous = case["initialState"]
            for event in case["events"]:
                assert previous == event["before"], f"State discontinuity at {event['id']}"
                assert sha(canonical(event["before"])) == event["beforeSHA256"]
                assert sha(canonical(event["after"])) == event["afterSHA256"]
                assert apply_root_patch(event["before"], event["forward"]) == event["after"]
                assert apply_root_patch(event["after"], event["inverse"]) == event["before"]
                total_ops += len(event["forward"]) + len(event["inverse"])
                previous = event["after"]
                replayed_events += 1
            if case["events"]:
                assert case["finalState"] == case["events"][-1]["after"]
            else:
                assert case["finalState"] == case["initialState"]
        assert replayed_events == counts["events"] and total_ops == counts["eventOperations"]

    return {
        "id": "SUMMON-STRUCTURE5-RETURN153-INDEPENDENT-VERIFICATION",
        "status": "PASS",
        "acceptedIds": IDS,
        "inputAuthority": expected_authority,
        "archiveBytes": len(archive_bytes),
        "archiveSha256": sha(archive_bytes),
        "deliverySha256": sha(delivery_bytes),
        "sourceBindingsVerified": 77,
        "evidenceBindingsVerified": 120,
        "archiveMembersVerified": 246,
        "questionDispositionsVerified": 20,
        "holdDefinitionsRetained": 15,
        "heldDependentBranches": 57,
        "casesVerified": 102,
        "eventsReplayed": 620,
        "forwardAndInverseOperationsReplayed": 2_480,
        "catalogUnchangedAtInput": True,
        "canonicalIndexUnchangedAtInput": True,
        "runtimeTests": 0,
        "failures": 0,
    }


if __name__ == "__main__":
    report = verify()
    output = AUDIT / "SUMMONSTRUCTURE5_RETURN153_INDEPENDENT_VERIFICATION.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
