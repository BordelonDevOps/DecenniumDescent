from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
RECV = AUDIT / "rank9_catastrophe10_return172_received"
RETURN = RECV / "DD_Rank9_Catastrophe10_Director_Return172.zip"
DELIVERY = RECV / "DD_Rank9_Catastrophe10_Director_Return172_DELIVERY.json"
RETURN_AUDIT = AUDIT / "RANK9_CATASTROPHE10_RETURN172_INDEPENDENT_AUDIT.json"
PACKET = FULL / "DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
PACKET_AUDIT = FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_VERIFICATION_171.json"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_02.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_172.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_172.json"
PENDING_BEFORE = AUDIT / "CURRENT109_PENDING_IDENTITY_AUDIT_171.json"
IDS = [
    "cataclysmic-conjuration",
    "elemental-apocalypse",
    "planar-overload",
    "armageddon",
    "cataclysm",
    "arcane-apocalypse",
    "meteor-swarm",
    "starfire-core",
    "ragnarok",
    "final-spark",
]
ID_SET = set(IDS)
BEFORE = {"reviewed": 739, "pending": 109, "acceptedUnapplied": 0}
AFTER = {"reviewed": 749, "pending": 99, "acceptedUnapplied": 0}
COMPLETE_BEFORE = 463
COMPLETE_AFTER = 473
REVIEW_ID = "RANK9-CATASTROPHE10-EXACT-AUTHORED-ACCEPTANCE-172"
APP_ID = "RANK9-CATASTROPHE10-APPLICATION-173"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9catastrophe10_reviewed_172"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_CATASTROPHE10_REVIEWED_172.md"
BACKUP = AUDIT / "authored_review_index.before_catastrophe10_173.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_CATASTROPHE10_172.json"
ACCEPTANCE = AUDIT / "CATASTROPHE10_EXACT_ACCEPTANCE_172.json"
APPLICATION = AUDIT / "CATASTROPHE10_APPLICATION_173.json"
OPERATIONS = AUDIT / "CATASTROPHE10_INDEX_OPERATIONS_173.json"
PENDING_AFTER = AUDIT / "CURRENT99_PENDING_IDENTITY_AUDIT_173.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_173.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_173.json"
RECEIPT = AUDIT / "RANK9_CATASTROPHE10_GPT_RETURN_172.json"
VALIDATION = AUDIT / "CATASTROPHE10_APPLICATION_VALIDATION_173.json"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_173.md"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def binding(path: Path, rel: str | None = None, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_inputs() -> dict:
    audit = read_json(RETURN_AUDIT)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["acceptedIds"] == IDS
    assert read_json(PACKET_AUDIT)["status"] == "PASS"
    delivery = read_json(DELIVERY)
    archive_bytes = RETURN.read_bytes()
    packet_bytes = PACKET.read_bytes()
    assert len(archive_bytes) == delivery["bytes"] == 17790499
    assert sha(archive_bytes) == delivery["sha256"] == "eda99c21a4936a5fd277fcf50fdf5f4eb35a12a79f8efa262bf97f795e152bcb"
    assert delivery["accepted"] is True and delivery["applied"] is False and delivery["exactAcceptedIds"] == IDS
    with zipfile.ZipFile(RETURN) as archive:
        archive_names = archive.namelist()
        members = {name: archive.read(name) for name in archive_names}
    assert len(archive_names) == 98 and len(set(archive_names)) == 98
    assert not [name for name in archive_names if name.startswith(("/", "\\")) or "\\" in name or ".." in PurePosixPath(name).parts]
    decision_source = json.loads(members["DIRECTOR_DECISION.json"])
    model_source = json.loads(members["MODEL.json"])
    procedures = json.loads(members["PROCEDURES.json"])
    holds = json.loads(members["HOLD_REGISTER.json"])
    cases = json.loads(members["CASEBOOK.json"])
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    pending_set = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 739, "pending": 109}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 463
    assert len(pending_set) == 109 and ID_SET <= pending_set
    assert decision_source["accepted"] is True and decision_source["applied"] is False
    assert decision_source["exactAcceptedIds"] == IDS and decision_source["unacceptedIds"] == []
    assert decision_source["staticAuthoredReviewBlockers"] == []
    assert decision_source["canonicalApplicationPerformed"] is False
    assert decision_source["baselineCanonicalAuthority"]["reviewedApplied"] == 739
    assert decision_source["baselineCanonicalAuthority"]["pending"] == 109
    assert decision_source["baselineCanonicalAuthority"]["acceptedUnapplied"] == 0
    assert queue["currentAuthority"] == handoff["currentAuthority"] == {
        "reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0,
        "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173,
    }
    assert queue["currentPendingGroups"][0]["group"] == "rank9-catastrophe10"
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert queue["packetStatus"] == "RANK9_CATASTROPHE10_SUBMITTED_AWAITING_DIRECTOR_RETURN"
    assert handoff["status"] == "RANK9_CATASTROPHE10_SUBMITTED_AWAITING_DIRECTOR_RETURN"
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_bytes)
    assert pending_before["pendingCount"] == 109 and set(IDS) <= set(pending_before["pendingIds"])
    assert len(procedures) == 10 and [row["id"] for row in procedures] == IDS
    assert all(row["accepted"] is True and row["applied"] is False for row in procedures)
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    assert all(row["completeNativeSourceAndAccess"] == catalog_rows[row["id"]] for row in procedures)
    assert all(next(row for row in before["entries"] if row["id"] == sid)["authoredStatus"] == "pending-authored-procedure" for sid in IDS)
    assert len(cases) == 59 and sum(row["wholeCaseHeld"] for row in cases) == 13
    assert len(holds) == 45 and all(row["retained"] is True for row in holds)
    output_paths = [CANDIDATE, STAGING, MANUSCRIPT, BACKUP, DECISION, ACCEPTANCE, APPLICATION, OPERATIONS, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, RECEIPT, VALIDATION, SNAPSHOT]
    assert not [str(path) for path in output_paths if path.exists()], "Application output already exists; inspect before retrying."
    assert not STAGING.is_symlink()
    assert CATALOG.read_bytes() == catalog_bytes
    return locals()


def build_and_apply() -> None:
    data = load_inputs()
    ts = now()
    before = data["before"]
    before_bytes = data["before_bytes"]
    catalog = data["catalog"]
    catalog_bytes = data["catalog_bytes"]
    queue_before = data["queue"]
    handoff_before = data["handoff"]
    procedures = data["procedures"]
    decision_source = data["decision_source"]
    model_source = data["model_source"]
    archive_bytes = data["archive_bytes"]
    packet_bytes = data["packet_bytes"]
    members = data["members"]
    pending_before = data["pending_set"]
    excluded_pending = sorted(pending_before - ID_SET)
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    source_by_id = {row["spellId"]: row for row in json.loads(members["SOURCE_RECORDS.json"])}

    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    for name, raw in members.items():
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(packet_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(SOURCE_CANDIDATE.read_bytes())
    (STAGING / "SOURCE_PACKET_VERIFICATION.json").write_bytes(PACKET_AUDIT.read_bytes())
    (STAGING / "RETURN_INDEPENDENT_AUDIT.json").write_bytes(RETURN_AUDIT.read_bytes())
    (STAGING / "DIRECTOR_DELIVERY.json").write_bytes(DELIVERY.read_bytes())
    casebook_bytes = members["CASEBOOK.json"]
    with (STAGING / "CASEBOOK.json.gz").open("wb") as raw_out:
        with gzip.GzipFile(fileobj=raw_out, mode="wb", mtime=0) as gz:
            gz.write(casebook_bytes)
    assert gzip.decompress((STAGING / "CASEBOOK.json.gz").read_bytes()) == casebook_bytes
    standalone_bytes = members["STANDALONE_PROCEDURES.md"]
    (STAGING / "STANDALONE_PROCEDURES.md").write_bytes(standalone_bytes)

    procedure_rows = []
    for position, sid in enumerate(IDS):
        record = procedures[position]
        native = record["completeNativeSourceAndAccess"]
        assert native == catalog_rows[sid] == source_by_id[sid]["completeCurrentCatalogSourceAndAccess"]
        assert record["currentIndexEntryUnchanged"] == source_by_id[sid]["currentIndexEntry"]
        procedure_rows.append({
            "id": sid,
            "name": record["name"],
            "procedure": {
                "common": copy.deepcopy(record["commonProcedure"]),
                "selected": copy.deepcopy(record["selectedProcedure"]),
            },
            "directorProcedureRecord": copy.deepcopy(record),
            "nativeSourceAndAccessUnchanged": copy.deepcopy(native),
            "questionIds": list(record["questionIds"]),
            "holdIds": list(record["holdIds"]),
            "runtimeSelectionEnabled": False,
        })
    hold_ids = [row["id"] for row in data["holds"]]
    model = {
        "schemaVersion": "RC9-authored-static-172",
        "moduleId": "rank9-catastrophe10-reviewed-172",
        "status": "director-accepted-unapplied-with-retained-holds",
        "accepted": True,
        "applied": False,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "authorityAtSubmission": {"appliedReviewed": 739, "pending": 109, "acceptedUnapplied": 0, "standaloneProcedures": 463},
        "spells": procedure_rows,
        "questionDispositions": json.loads(members["QUESTION_DISPOSITIONS.json"]),
        "originalQuestions": json.loads(members["ORIGINAL_QUESTIONS.json"]),
        "originalObligations": json.loads(members["ORIGINAL_OBLIGATIONS.json"]),
        "obligationDispositions": json.loads(members["OBLIGATION_DISPOSITIONS.json"]),
        "coverage": json.loads(members["COVERAGE.json"]),
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(casebook_bytes), "sha256": sha(casebook_bytes)},
        "standaloneProcedures": "STANDALONE_PROCEDURES.md",
        "holdRegisterFile": "DIRECTOR_RETURN/HOLD_REGISTER.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "directorDecisionFile": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip",
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "returnCounts": copy.deepcopy(model_source["returnCounts"]),
        "holdIds": hold_ids,
        "holdCountQualification": copy.deepcopy(model_source["holdCountQualification"]),
        "directorReturnDeliveryObservation": {
            "source": "GPT Library delivery JSON cross-checked with DIRECTOR_DECISION.json and MEMBER_MANIFEST.json",
            "archiveBytes": len(archive_bytes), "archiveSha256": sha(archive_bytes), "accepted": True, "applied": False,
            "memberCount": 98, "sourceBindings": 86, "directorDataChecksPassed": 12798,
            "semanticFailureChecksPassed": 36, "packageChecksPassed": 297, "failedChecks": 0,
        },
        "sourceQualification": "All source, class access, source/card status, physical, lifecycle, information and hold qualifications remain separate; canonical catalog bytes and source status are unchanged.",
        "candidatePackageManifestBinding": None,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyApproved": False,
        "domainClosure": False,
        "releaseApproved": False,
        "canonicalApplicationPerformed": False,
    }
    package_files = []
    for path in sorted(STAGING.rglob("*")):
        relative = path.relative_to(STAGING).as_posix()
        if path.is_file() and relative not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            raw = path.read_bytes()
            package_files.append({"path": relative, "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK9-CATASTROPHE10-CANDIDATE-PACKAGE-MANIFEST-173",
        "sourceArchive": {"name": RETURN.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "files": package_files,
        "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    model["candidatePackageManifestBinding"] = binding(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")
    write_json(STAGING / "MODEL.json", model)
    model_binding = binding(STAGING / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json")
    casebook_binding = binding(STAGING / "CASEBOOK.json.gz", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    return_binding = binding(RETURN, RETURN.relative_to(ROOT).as_posix(), archive_bytes)
    packet_binding = binding(PACKET, PACKET.relative_to(ROOT).as_posix(), packet_bytes)
    source_candidate_binding = binding(SOURCE_CANDIDATE)
    hold_binding = binding(director_dir / "HOLD_REGISTER.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLD_REGISTER.json")
    proposal_binding = binding(director_dir / "PROPOSAL_OPERATIONS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json")
    procedure_source_binding = binding(director_dir / "DIRECTOR_DECISION.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json")
    candidate_manifest_binding = binding(CANDIDATE_PACKAGE := STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-CATASTROPHE10-172",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT},
        "decisionId": decision_source["id"],
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "remainingBlockingDefects": [],
        "verification": {
            "directorSourceChecksPassed": 265, "directorDataChecksPassed": 12798,
            "directorSemanticChecksPassed": 36, "directorMixedArithmeticChecksPassed": 20,
            "directorPackageChecksPassed": 297, "independentReturnAudit": read_json(RETURN_AUDIT),
            "sourcePacketVerification": read_json(PACKET_AUDIT), "returnArchiveMembers": 98,
            "sourceBindings": 86, "questions": 25, "procedures": 10, "mainCases": 20,
            "branches": 39, "cases": 59, "wholeHeldCases": 13, "events": 574,
            "eventOperations": 2296, "proposalOperations": 40, "registeredHolds": 45,
            "batchSpecificHolds": 16, "inheritedClosedScopeHolds": 29,
        },
        "acceptedArchive": {"name": RETURN.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "sourceArchive": {"name": PACKET.name, "bytes": len(packet_bytes), "sha256": sha(packet_bytes)},
        "scope": decision_source["acceptanceScope"],
        "holdScope": "All 16 batch-specific hold records and 29 inherited closed-scope hold records remain. Thirteen whole-case-held traces remain held. Source, access, content, physical, lifecycle, information, structure, runtime, human-play, balance, cosmology, domain-closure and release qualifications remain explicit.",
        "excludedClaims": {"runtime": False, "humanPlay": False, "balance": False, "cosmology": False, "domainClosure": False, "release": False, "canonicalApplication": False},
        "directorMadeNoCanonicalChanges": True,
    }
    write_json(DECISION, decision_record)
    acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision_record,
        "directorReturn": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "acceptedIds": IDS,
        "countsBefore": {**BEFORE, "scopedInterfaces": 173},
        "countsAfter": {**AFTER, "scopedInterfaces": 173},
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "acceptedProcedures": 10, "acceptedQuestions": 25, "acceptedMainCases": 20,
        "acceptedBranches": 39, "acceptedCases": 59, "wholeHeldCases": 13,
        "acceptedEvents": 574, "eventOperations": 2296, "retainedHolds": 45,
        "localBatchHolds": 16, "inheritedClosedScopeHoldRecords": 29,
        "sourceStatusPreserved": "blocked-pending-operational-review for all ten identities; static authored procedure review only.",
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyApproved": False,
        "domainClosure": False, "releaseApproved": False, "canonicalApplicationPerformed": False,
    }
    write_json(ACCEPTANCE, acceptance)
    os.replace(STAGING, CANDIDATE)
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(standalone_bytes.decode("utf-8-sig"), encoding="utf-8", newline="\n")

    model_binding = binding(CANDIDATE / "MODEL.json")
    casebook_binding = binding(CANDIDATE / "CASEBOOK.json.gz")
    candidate_manifest_binding = binding(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")
    application = {
        "id": APP_ID, "recordedAtUtc": ts,
        "status": "APPLIED_TEN_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply accepted ordinary-spell identities exactly, push every batch to GitHub, and continue until pending reaches zero.",
        "acceptedIds": IDS,
        "directorAcceptance": binding(ACCEPTANCE), "directorDecision": binding(DECISION),
        "directorReturn": return_binding, "candidateEnvelope": model_binding,
        "candidatePackageManifest": candidate_manifest_binding, "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {**BEFORE, "scopedInterfaces": 173}, "after": {**AFTER, "scopedInterfaces": 173}},
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "procedures": 10, "questions": 25, "mainCases": 20, "branches": 39, "cases": 59,
        "wholeHeldCases": 13, "events": 574, "eventOperations": 2296, "retainedHolds": 45,
        "sourceStatusPreservedAsBlocked": True, "catalogChanged": False,
        "runtimeSelectionEnabled": False, "closed335AndCompletedCohortsReopened": False,
    }
    write_json(APPLICATION, application)
    application_binding = binding(APPLICATION)

    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(IDS):
        index_position = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_position]
        updated = copy.deepcopy(old)
        updated.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9catastrophe10_reviewed_172/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/spells/{position}/procedure/common",
            "manuscript": "../../../docs/spells/candidates/RANK9_CATASTROPHE10_REVIEWED_172.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json",
            "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": return_binding,
            "sourceConferenceArchiveBinding": binding(PACKET),
            "sourceCandidateBinding": binding(SOURCE_CANDIDATE),
            "candidatePackageManifestBinding": candidate_manifest_binding,
            "retainedHoldsBinding": hold_binding,
            "procedureSourceBinding": procedure_source_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": acceptance["decision"],
            "authoredAcceptanceReceipt": binding(ACCEPTANCE),
            "authoredApplicationReceipt": application_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": index_position, "before": copy.deepcopy(old), "after": copy.deepcopy(updated)})
        after["entries"][index_position] = updated
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9catastrophe10_reviewed_172/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "authority": binding(ACCEPTANCE),
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "sourceArchive": return_binding,
        "sourceConferenceArchive": binding(PACKET),
        "casebookBinding": casebook_binding,
        "holdsBinding": hold_binding,
        "candidatePackageManifestBinding": candidate_manifest_binding,
        "scope": acceptance["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 749, "pending": 99}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 473
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 10 and len(pending_after) == 99 and pending_after == pending_before - ID_SET
    assert sum(row["authoredStatus"] == "reviewed-authored-operational-playtest" for row in after["entries"]) == 749
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    BACKUP.write_bytes(before_bytes)
    write_json(OPERATIONS, {
        "id": "RANK9-CATASTROPHE10-INDEX-OPERATIONS-173",
        "before": binding(BACKUP, raw=before_bytes),
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "ten prior identity rows, aggregate authored counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    })
    temp_index = INDEX.with_suffix(".json.catastrophe10-173.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority_after = {"reviewedApplied": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173}
    remaining_groups = []
    for group in queue_before["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in pending_after]
        if left:
            row = copy.deepcopy(group)
            row["pendingIds"] = left
            row["pendingCount"] = len(left)
            row["freshPacketRequiredForCurrentAuthority"] = True
            row.pop("submissionReceipt", None)
            row.pop("submission", None)
            row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            remaining_groups.append(row)
    assert remaining_groups and sum(group["pendingCount"] for group in remaining_groups) == 99
    pending_doc = {
        "id": "CURRENT99-PENDING-IDENTITY-AUDIT-173",
        "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": binding(INDEX), "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"], "pendingCount": 99,
        "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in catalog["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False,
        "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)

    receipt = {
        "id": "RANK9-CATASTROPHE10-GPT-RETURN-172-RECEIPT",
        "recordedAtUtc": now(),
        "status": "EXACT_RETURN_RECEIVED_ACCEPTED_INDEPENDENTLY_VERIFIED_AND_APPLIED",
        "source": {"product": "ChatGPT", "conversationTitle": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "url": CHAT},
        "receivedArchive": return_binding,
        "deliveryBinding": binding(DELIVERY),
        "directorDecisionBinding": binding(DECISION),
        "accepted": True,
        "appliedAtDecision": False,
        "appliedSeparately": True,
        "acceptedIds": IDS,
        "independentAudit": {"path": RETURN_AUDIT.relative_to(ROOT).as_posix(), "status": data["audit"]["status"], "checksPassed": data["audit"]["checksPassed"], "checksFailed": data["audit"]["checksFailed"]},
        "directorReportedChecks": {"source": 265, "data": 12798, "semantic": 36, "mixedArithmetic": 20, "package": 297, "failed": 0},
        "applicationBinding": binding(APPLICATION),
        "applicationState": "Applied exactly ten accepted IDs to the authored review index; canonical catalog and native source/access rows remain byte-exact and runtime selection remains disabled.",
    }
    write_json(RECEIPT, receipt)
    receipt_binding = binding(RECEIPT)

    queue_after = copy.deepcopy(queue_before)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-173", "recordedAtUtc": now(),
        "currentAuthority": authority_after,
        "currentPendingGroups": remaining_groups,
        "nextSuggestedGroups": remaining_groups[:5],
        "nextGroup": remaining_groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 10, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 99, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": remaining_groups[0]["group"], "pendingCount": remaining_groups[0]["pendingCount"], "candidate": remaining_groups[0].get("candidate"), "archive": remaining_groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"},
        "packetStatus": "RANK9_CATASTROPHE10_RETURN172_APPLIED_749_99",
        "currentSubmission": {"path": RECEIPT.name, "bytes": RECEIPT.stat().st_size, "sha256": sha(RECEIPT.read_bytes())},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT, "receipt": receipt_binding, "reviewIds": IDS, "acceptedIds": IDS, "appliedIds": IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
    })
    write_json(QUEUE_AFTER, queue_after)

    handoff = copy.deepcopy(handoff_before)
    handoff.update({
        "id": "CURRENT-HANDOFF-173", "recordedAtUtc": now(),
        "status": "RANK9_CATASTROPHE10_ACCEPTED_AND_APPLIED_NEXT_99_PENDING",
        "currentAuthority": authority_after,
        "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "currentQueueBinding": binding(QUEUE_AFTER),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 99, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 10, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": RETURN_AUDIT.relative_to(ROOT).as_posix()},
        "nextGroup": remaining_groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed spell cohorts, or previously accepted/applied spell batches. Runtime, source, access, physical, lifecycle, information, structure, cosmology, content and release holds remain separate and active.",
        "resumePriority": f"Prepare a fresh {remaining_groups[0]['group']} packet against current 749/99 authority, submit it to the same GPT director, independently audit the exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": remaining_groups[0]["group"], "candidate": remaining_groups[0].get("candidate"), "historicalArchive": remaining_groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "request": "Build a fresh source packet and archive bound to current 749/99 authority before director review."},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT, "receipt": receipt_binding, "archive": return_binding, "reviewIds": IDS, "acceptedIds": IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
        "currentSubmissionBinding": receipt_binding,
    })
    write_json(HANDOFF_AFTER, handoff)

    validation = {
        "id": "RANK9-CATASTROPHE10-APPLICATION-VALIDATION-173",
        "status": "PENDING_INDEPENDENT_POST_APPLICATION_VERIFICATION",
        "acceptedIds": IDS,
        "before": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE_BEFORE},
        "after": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE_AFTER},
        "pendingIdentityCount": len(pending_after),
        "onlyAcceptedEntriesChanged": True,
        "catalogByteExactUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "sourceStatusPreservedBlocked": all(next(row for row in after["entries"] if row["id"] == sid)["sourceStatus"] == "blocked-pending-operational-review" for sid in IDS),
        "runtimeSelectionEnabled": False,
        "inverseSemanticExact": inverse == before,
        "independentReturnAudit": {"status": data["audit"]["status"], "checksPassed": data["audit"]["checksPassed"], "checksFailed": data["audit"]["checksFailed"]},
        "nextGroup": remaining_groups[0]["group"],
        "acceptedUnapplied": 0,
        "closed335AndCompletedCohortsReopened": False,
    }
    write_json(VALIDATION, validation)
    old_start = START.read_text(encoding="utf-8-sig")
    marker = "**Prior checkpoint: ["
    at = old_start.find(marker)
    history = old_start[at:] if at >= 0 else ""
    START.write_text(
        "# Decennium Descent — start here\n\n"
        f"**Current ordinary spell-review checkpoint [173]({HANDOFF_AFTER.relative_to(ROOT).as_posix()}):** the GPT director accepted and Codex independently audited and applied exactly {', '.join(IDS)}. Authority is **749 reviewed / 99 pending / 0 accepted-unapplied**, with 473 complete reviewed standalone procedures. The director return passed 40 independent checks across 86 source bindings, 59 cases, 574 events and 2,296 reversible operations.\n\n"
        f"All 45 registered holds remain: 16 batch-specific and 29 inherited closed-scope records; 13 whole-case traces remain held. The native catalog and source/access rows are unchanged, and runtime selection remains disabled. Runtime, human-play, balance, cosmology, domain closure and release approval remain separate. The next group is **{remaining_groups[0]['group']}** and requires a fresh packet at 749/99. Continue until pending reaches zero.\n\n"
        f"See [current handoff]({HANDOFF_AFTER.relative_to(ROOT).as_posix()}), [pending identity audit]({PENDING_AFTER.relative_to(ROOT).as_posix()}), [exact acceptance]({ACCEPTANCE.relative_to(ROOT).as_posix()}), [application]({APPLICATION.relative_to(ROOT).as_posix()}), [independent return audit]({RETURN_AUDIT.relative_to(ROOT).as_posix()}), and [director return ZIP]({RETURN.relative_to(ROOT).as_posix()}).\n\n"
        + history,
        encoding="utf-8", newline="\n",
    )
    SNAPSHOT.write_text(
        f"# Ordinary spell review snapshot — Rank9 Catastrophe10 Return172\n\nAs of 2026-10-25, authored ordinary-spell authority is **749 reviewed / 99 pending / 0 accepted-unapplied**, with 473 complete reviewed standalone procedures. The GPT director accepted and this application records exactly {', '.join(IDS)}.\n\n"
        f"The return ZIP is {len(archive_bytes):,} bytes with SHA-256 `{sha(archive_bytes)}`. The director reports 265 source checks, 12,798 data checks, 36 semantic checks, 20 mixed-arithmetic checks, and 297 package checks passing. Independent local return verification passed 40 checks, including all 86 current source bindings and independent replay of all 59 cases and 2,296 reversible event operations.\n\n"
        "All 45 hold records remain, including 13 whole-case-held traces. The catalog and native source/access rows remain unchanged; runtime selection is disabled. This static authored review gives no runtime, human-play, balance, cosmology, domain-closure or release approval.\n\n"
        f"The next pending group is {remaining_groups[0]['group']} with {remaining_groups[0]['pendingCount']} identities and requires a fresh packet at 749/99 authority. Continue until pending reaches zero.\n\n"
        f"See [current handoff]({HANDOFF_AFTER.relative_to(ROOT).as_posix()}), [pending identity audit]({PENDING_AFTER.relative_to(ROOT).as_posix()}), [exact acceptance]({ACCEPTANCE.relative_to(ROOT).as_posix()}), and [application validation]({VALIDATION.relative_to(ROOT).as_posix()}).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    print(json.dumps({
        "status": "APPLIED_READY_FOR_INDEPENDENT_POST_APPLICATION_VERIFICATION",
        "acceptedIds": IDS,
        "authority": authority_after,
        "nextGroup": remaining_groups[0]["group"],
        "nextPendingCount": remaining_groups[0]["pendingCount"],
        "returnArchive": return_binding,
        "index": binding(INDEX),
        "catalogByteExactUnchanged": True,
    }, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        build_and_apply()
    else:
        inputs = load_inputs()
        print(json.dumps({
            "status": "PREFLIGHT_PASS",
            "independentReturnChecks": inputs["audit"]["checksPassed"],
            "acceptedIds": IDS,
            "authorityBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE_BEFORE, "scopedInterfaces": 173},
            "authorityAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE_AFTER, "scopedInterfaces": 173},
            "nextGroupAfterApply": "derived-from-current-queue",
            "returnBytes": RETURN.stat().st_size,
            "outputAbsent": not CANDIDATE.exists(),
            "catalogUnchanged": True,
        }, indent=2))
