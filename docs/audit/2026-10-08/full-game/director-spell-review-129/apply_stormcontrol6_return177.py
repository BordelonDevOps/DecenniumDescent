from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
RECV = AUDIT / "rank9_stormcontrol6_return177_received"
RETURN = RECV / "DD_Rank9_StormControl6_Director_Return177.zip"
DELIVERY = RECV / "DD_Rank9_StormControl6_Director_Return177_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_STORMCONTROL6_RETURN177_INDEPENDENT_AUDIT.json"
SOURCE_ARCHIVE = FULL / "DD_Rank9_Storm_Control_6_Source_Conference_02_175.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_storm_control_6_source_conference_02_175.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_178.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_178.json"
PENDING_BEFORE = AUDIT / "CURRENT99_PENDING_IDENTITY_AUDIT_177.json"
IDS = ["cosmic-implosion", "frozen-eternity", "hellstorm", "storm-of-vengeance", "thunder-wrath", "storm-cage"]
ID_SET = set(IDS)
BEFORE = {"reviewed": 749, "pending": 99, "acceptedUnapplied": 0}
AFTER = {"reviewed": 755, "pending": 93, "acceptedUnapplied": 0}
COMPLETE_BEFORE = 473
COMPLETE_AFTER = 479
REVIEW_ID = "RANK9-STORMCONTROL6-EXACT-AUTHORED-ACCEPTANCE-177"
APP_ID = "RANK9-STORMCONTROL6-APPLICATION-179"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9stormcontrol6_reviewed_177"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_STORMCONTROL6_REVIEWED_177.md"
BACKUP = AUDIT / "authored_review_index.before_stormcontrol6_179.json"
DECISION = AUDIT / "RANK9_STORMCONTROL6_GPT_DECISION_177.json"
ACCEPTANCE = AUDIT / "RANK9_STORMCONTROL6_EXACT_ACCEPTANCE_177.json"
RECEIPT = AUDIT / "RANK9_STORMCONTROL6_GPT_RETURN_177.json"
APPLICATION = AUDIT / "RANK9_STORMCONTROL6_APPLICATION_179.json"
OPERATIONS = AUDIT / "RANK9_STORMCONTROL6_INDEX_OPERATIONS_179.json"
PENDING_AFTER = AUDIT / "CURRENT93_PENDING_IDENTITY_AUDIT_179.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_179.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_179.json"
VALIDATION = AUDIT / "RANK9_STORMCONTROL6_APPLICATION_VALIDATION_179.json"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-26_SPELL_REVIEW_179.md"
START = ROOT / "START_HERE.md"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
DIRECTOR_FILES = [
    "DIRECTOR_DECISION.json",
    "SEMANTIC_FAILURE_CHECK.json",
    "PROCEDURES.json",
    "QUESTION_DISPOSITIONS.json",
    "CASE_DISPOSITIONS.json",
    "CASE_INDEX.json",
    "HOLD_REGISTER.json",
    "ORIGINAL_OBLIGATIONS.json",
    "PROCEDURE_PROPOSALS.json",
    "STANDALONE_PROCEDURES.md",
    "SOURCE_VERIFICATION.json",
    "DATA_VALIDATION.json",
    "REGULAR_CLOCK_FAILURE_CHECK.json",
    "PROFILE_REPAIR_EVIDENCE.json",
    "QUALIFIED_EXTRA_TURN_OBLIGATION.json",
    "EVIDENCE_MANIFEST.json",
    "FINAL_METADATA_VALIDATION.json",
    "ACCEPTED_COMPARISON_VERIFICATION.json",
    "AUXILIARY_SOURCE_VERIFICATION.json",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def bind(path: Path, rel: str | None = None, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def bind_stream(path: Path, rel: str | None = None) -> dict:
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha_file(path)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def preflight() -> dict:
    audit = read_json(INDEPENDENT_AUDIT)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["acceptedIds"] == IDS
    delivery = read_json(DELIVERY)
    archive_bytes = RETURN.stat().st_size
    assert archive_bytes == delivery["archive"]["bytes"] == 105824642
    assert sha_file(RETURN) == delivery["archive"]["sha256"] == "ae787f7f830262075483f7de1a6391da2d7bdb4a144cb611d9f53d7bf8750674"
    assert delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS
    with zipfile.ZipFile(RETURN, "r") as archive:
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        model_source = json.loads(archive.read("MODEL.json"))
        procedures = json.loads(archive.read("PROCEDURES.json"))["procedures"]
        procedures_by_id = {row["spellId"]: row for row in procedures}
        assert archive.testzip() is None
        assert all(PurePosixPath(name).as_posix() == name for name in archive.namelist())

    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = read_json(INDEX)
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    entries = {row["id"]: row for row in before["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 749, "pending": 99}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    assert len(live_pending) == 99 and ID_SET <= live_pending
    assert decision["accepted"] is True and decision["applied"] is False and decision["acceptedIds"] == IDS and decision["blockers"] == []
    assert decision["sourceAuthority"] == {"appliedReviewed": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173}
    assert queue["currentAuthority"]["reviewedApplied"] == handoff["currentAuthority"]["reviewedApplied"] == 749
    assert queue["currentAuthority"]["pending"] == handoff["currentAuthority"]["pending"] == 99
    assert queue["currentPendingGroups"][0]["group"] == "rank9-storm-control6" and queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    catalog_git_blob = subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{CATALOG.relative_to(ROOT).as_posix()}"], cwd=ROOT)
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_git_blob) and json.loads(catalog_git_blob) == catalog
    assert pending_before["pendingCount"] == 99 and ID_SET <= set(pending_before["pendingIds"])
    assert all(entries[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS)
    assert all(procedures_by_id[sid]["nativeCardUnchanged"] == catalog_rows[sid] for sid in IDS)
    assert all(entries[sid]["sourceStatus"] == "blocked-pending-operational-review" for sid in IDS)
    assert model_source["accepted"] is True and model_source["applied"] is False and model_source["authority"]["reviewedApplied"] == 749 and model_source["authority"]["pending"] == 99

    outputs = [STAGING, CANDIDATE, MANUSCRIPT, BACKUP, DECISION, ACCEPTANCE, RECEIPT, APPLICATION, OPERATIONS, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, VALIDATION, SNAPSHOT]
    existing = [str(path) for path in outputs if path.exists()]
    assert not existing, f"Application outputs already exist; inspect before retrying: {existing}"
    assert CATALOG.read_bytes() == catalog_bytes
    return locals()


def apply() -> None:
    data = preflight()
    ts = now()
    audit = data["audit"]
    before = data["before"]
    before_bytes = data["before_bytes"]
    catalog = data["catalog"]
    catalog_bytes = data["catalog_bytes"]
    queue_before = data["queue"]
    handoff_before = data["handoff"]
    live_pending = data["live_pending"]
    delivery = data["delivery"]
    procedures = data["procedures_by_id"]
    excluded_pending = sorted(live_pending - ID_SET)
    assert len(excluded_pending) == 93

    with zipfile.ZipFile(RETURN, "r") as archive:
        source_members = {name: archive.read(name) for name in DIRECTOR_FILES}
        procedures_doc = json.loads(source_members["PROCEDURES.json"])
        questions_doc = json.loads(source_members["QUESTION_DISPOSITIONS.json"])
        obligations_doc = json.loads(archive.read("ORIGINAL_OBLIGATIONS.json"))
        case_dispositions = json.loads(source_members["CASE_DISPOSITIONS.json"])
        hold_register = json.loads(source_members["HOLD_REGISTER.json"])
        source_decision = json.loads(source_members["DIRECTOR_DECISION.json"])
        model_source = json.loads(archive.read("MODEL.json"))
        casebook_binding_source = next(row for row in delivery["members"] if row["path"] == "CASEBOOK.json")
        archive_members = [row["path"] for row in delivery["members"]]
        original_obligations_binding = {"path": "ORIGINAL_OBLIGATIONS.json", "bytes": len(archive.read("ORIGINAL_OBLIGATIONS.json")), "sha256": sha(archive.read("ORIGINAL_OBLIGATIONS.json"))}
        SOURCE_CANDIDATE_BYTES = archive.read("SOURCE_CONFERENCE_CANDIDATE.json")

    procedures = {row["spellId"]: row for row in procedures_doc["procedures"]}
    assert [procedures[sid]["spellId"] for sid in IDS] == IDS
    assert all(procedures[sid]["accepted"] is True and procedures[sid]["applied"] is False for sid in IDS)
    assert all(procedures[sid]["nativeCardUnchanged"] == data["catalog_rows"][sid] for sid in IDS)

    # Stage a compact but complete local envelope: the exact full ZIP remains bound,
    # while selected control records and a deterministic gzip casebook stay convenient to inspect.
    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    for name, raw in source_members.items():
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "DIRECTOR_DELIVERY.json").write_bytes(DELIVERY.read_bytes())
    (STAGING / "RETURN_INDEPENDENT_AUDIT.json").write_bytes(INDEPENDENT_AUDIT.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(SOURCE_CANDIDATE_BYTES)
    casebook_path = STAGING / "CASEBOOK.json.gz"
    casebook_hash = hashlib.sha256()
    casebook_total = 0
    with zipfile.ZipFile(RETURN, "r") as archive, casebook_path.open("wb") as raw_out:
        with archive.open("CASEBOOK.json", "r") as casebook_in, gzip.GzipFile(fileobj=raw_out, mode="wb", mtime=0) as compressed:
            for block in iter(lambda: casebook_in.read(1024 * 1024), b""):
                casebook_hash.update(block)
                casebook_total += len(block)
                compressed.write(block)
    assert casebook_total == casebook_binding_source["bytes"]
    assert casebook_hash.hexdigest() == casebook_binding_source["sha256"]

    spell_rows = []
    catalog_rows = data["catalog_rows"]
    for pos, sid in enumerate(IDS):
        procedure = procedures[sid]
        native = catalog_rows[sid]
        spell_rows.append({
            "id": sid,
            "name": native["name"],
            "procedure": copy.deepcopy(procedure),
            "directorProcedureRecord": copy.deepcopy(procedure),
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "questionDispositions": copy.deepcopy(procedure["questions"]),
            "runtimeSelectionEnabled": False,
        })

    returned_counts = copy.deepcopy(delivery["counts"])
    all_hold_records = hold_register["localHolds"] + hold_register["inheritedExactScopeRecords"]
    hold_ids = [row["id"] for row in hold_register["localHolds"]] + [row["scopedRecordId"] for row in hold_register["inheritedExactScopeRecords"]]
    return_binding = bind(RETURN)
    delivery_binding = bind(DELIVERY)
    independent_audit_binding = bind(INDEPENDENT_AUDIT)
    packet_binding = bind(SOURCE_ARCHIVE)
    source_candidate_binding = bind(SOURCE_CANDIDATE)
    archive_only_members = sorted(set(archive_members) - set(DIRECTOR_FILES) - {"CASEBOOK.json", "ORIGINAL_OBLIGATIONS.json", "SOURCE_CONFERENCE_CANDIDATE.json"})
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9-stormcontrol6-reviewed-177",
        "status": "EXACT_SIX_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly the six GPT-accepted Rank9 Storm Control6 static authored procedures. Native cards, catalog rows, class access, source status, accepted interfaces, and global rules remain unchanged. All 95 scoped hold records remain, including the qualified genuine-extra-turn obligation and unresolved observed-die input. Runtime selection stays disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Common timing and resource language remains local to these six exact records; no global rule or accepted interface is changed.", "perSpellCommon": {sid: copy.deepcopy(procedures[sid]["commonRules"]) for sid in IDS}},
        "spells": spell_rows,
        "questionDispositions": questions_doc,
        "originalObligations": obligations_doc,
        "futureCaseDispositions": case_dispositions,
        "returnCounts": returned_counts,
        "applicationCountSummary": {"procedures": 6, "questions": 27, "mainCases": 12, "branches": 49, "caseRecords": 61, "events": 2592, "reversibleEventOperations": 10368, "proposalOperations": 24, "conditionalOutcomeBranches": 7, "totalScopedHolds": 95, "dataAndScopedSemanticChecks": 57066, "failedChecks": 0},
        "holdIds": hold_ids,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLD_REGISTER.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROCEDURE_PROPOSALS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip with mtime=0; exact decompression reproduces the CASEBOOK.json member of the bound director ZIP",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_total, "sha256": casebook_hash.hexdigest()},
        "directorReturnArchive": return_binding,
        "directorReturnArchiveBinding": return_binding,
        "directorDeliveryBinding": delivery_binding,
        "independentReturnAudit": independent_audit_binding,
        "archiveOnlyMembers": archive_only_members,
        "archiveOnlyRationale": "All 140 bytes-exact members remain in the bound director ZIP. Large event-case and evidence members are not duplicated as loose repository files; standalone case files and all event hashes were independently replayed before application.",
        "sourceConferenceArchive": packet_binding,
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "sourceConferenceCandidateBinding": source_candidate_binding,
        "standaloneProcedures": "DIRECTOR_RETURN/STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
        "directorDecisionId": source_decision["id"],
        "directorReturnDeliveryObservation": {"archiveBytes": return_binding["bytes"], "archiveSha256": return_binding["sha256"], "accepted": True, "applied": False, "memberCount": 140, "passedDataChecks": 57066, "failedDataChecks": 0, "passedPackageChecks": 423, "failedPackageChecks": 0, "savedArtifactChecks": 225, "independentAuditChecks": 25, "independentAuditFailures": 0},
        "sourceAuthorityAtDecision": copy.deepcopy(source_decision["sourceAuthority"]),
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
        "domainClosure": False,
    }

    package_files = []
    for path in sorted(STAGING.rglob("*")):
        relative = path.relative_to(STAGING).as_posix()
        if path.is_file() and relative not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            package_files.append(bind_stream(path, f"{CANDIDATE.relative_to(ROOT).as_posix()}/{relative}"))
    package_manifest = {
        "id": "RANK9-STORMCONTROL6-CANDIDATE-PACKAGE-MANIFEST-179",
        "sourceArchive": return_binding,
        "sourceDelivery": delivery_binding,
        "independentAudit": independent_audit_binding,
        "sourceConferenceArchive": packet_binding,
        "sourceConferenceCandidate": source_candidate_binding,
        "files": package_files,
        "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
        "archiveOnlyMembers": archive_only_members,
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    model["candidatePackageManifestBinding"] = bind(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")
    write_json(STAGING / "MODEL.json", model)
    model_binding = bind(STAGING / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json")
    casebook_binding = bind(STAGING / "CASEBOOK.json.gz", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    hold_binding = bind(STAGING / "DIRECTOR_RETURN/HOLD_REGISTER.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLD_REGISTER.json")
    proposal_binding = bind(STAGING / "DIRECTOR_RETURN/PROCEDURE_PROPOSALS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROCEDURE_PROPOSALS.json")
    procedure_source_binding = bind(STAGING / "DIRECTOR_RETURN/DIRECTOR_DECISION.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json")
    os.replace(STAGING, CANDIDATE)

    # Save the verbatim director return and exact acceptance receipt before changing the canonical index.
    receipt = {
        "id": "RANK9-STORMCONTROL6-GPT-RETURN-177",
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_SIX_UNAPPLIED; INDEPENDENT_AUDIT_PASSED",
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT},
        "decisionId": source_decision["id"],
        "accepted": True,
        "appliedAtDecision": False,
        "reviewedIds": IDS,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "blockingDefects": [],
        "directorReturn": return_binding,
        "deliveryManifest": delivery_binding,
        "independentAudit": independent_audit_binding,
        "sourceAuthority": copy.deepcopy(source_decision["sourceAuthority"]),
        "counts": returned_counts,
        "priorFindingDispositions": copy.deepcopy(source_decision["priorFindingDispositions"]),
        "qualifications": copy.deepcopy(source_decision["qualifications"]),
    }
    write_json(RECEIPT, receipt)

    director_decision = {
        "id": "GPT-DIRECTOR-DECISION-STORMCONTROL6-177",
        "recordedAtUtc": ts,
        "source": receipt["source"],
        "decisionId": source_decision["id"],
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "remainingBlockingDefects": [],
        "verification": {"sourceChecksPassed": 311, "sourceChecksFailed": 0, "acceptedComparisonChecksPassed": 106, "auxiliarySourceChecksPassed": 10, "dataAndScopedSemanticChecksPassed": 57066, "dataAndScopedSemanticChecksFailed": 0, "packageChecksPassed": 423, "savedArtifactChecksPassed": 225, "independentReturnAudit": audit, "returnMembers": 140, "caseRecords": 61, "events": 2592, "eventOperations": 10368, "proposalOperations": 24, "retainedScopedHolds": 95},
        "acceptedArchive": return_binding,
        "deliveryManifest": delivery_binding,
        "scope": source_decision["decision"],
        "retainedBoundary": "The six records remain static authored procedures only. Source/access, content, physical, lifecycle, missing-extra-turn-source, and unobserved-die holds remain. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "directorMadeNoCanonicalChanges": True,
    }
    write_json(DECISION, director_decision)
    acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": bind(DECISION),
        "directorReturnReceipt": bind(RECEIPT),
        "directorReturn": return_binding,
        "independentAudit": independent_audit_binding,
        "acceptedIds": IDS,
        "countsBefore": {**BEFORE, "scopedInterfaces": 173},
        "countsAfter": {**AFTER, "scopedInterfaces": 173},
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "acceptedProcedures": 6,
        "acceptedMainCases": 12,
        "acceptedBranches": 49,
        "acceptedCaseRecords": 61,
        "acceptedEvents": 2592,
        "eventOperations": 10368,
        "proposalOperations": 24,
        "retainedHolds": 95,
        "sourceStatusPreserved": "blocked-pending-operational-review for all six identities; static authored procedure review only.",
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
        "canonicalApplicationPerformed": False,
    }
    write_json(ACCEPTANCE, acceptance)
    shutil.copyfile(INDEX, BACKUP)
    assert BACKUP.read_bytes() == before_bytes

    app = {
        "id": APP_ID,
        "recordedAtUtc": ts,
        "status": "APPLIED_SIX_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact GPT-accepted ordinary-spell batch, push it to GitHub, and continue until all pending identities are applied.",
        "acceptedIds": IDS,
        "directorAcceptance": bind(ACCEPTANCE),
        "directorDecision": bind(DECISION),
        "directorReturnReceipt": bind(RECEIPT),
        "directorReturn": return_binding,
        "directorDelivery": delivery_binding,
        "independentAudit": independent_audit_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "indexBefore": bind(BACKUP, raw=before_bytes),
        "counts": {"before": {**BEFORE, "scopedInterfaces": 173}, "after": {**AFTER, "scopedInterfaces": 173}},
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "caseRecords": 61,
        "mainCases": 12,
        "branches": 49,
        "events": 2592,
        "eventOperations": 10368,
        "retainedScopedHolds": 95,
        "sourceStatusPreservedAsBlocked": True,
        "sourceCatalogChanged": False,
        "nativeSpellCardsChanged": False,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(APPLICATION, app)
    application_binding = bind(APPLICATION)

    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(IDS):
        index_position = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_position]
        updated = copy.deepcopy(old)
        updated.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9stormcontrol6_reviewed_177/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/sharedRules/perSpellCommon/{sid}",
            "manuscript": "../../../docs/spells/candidates/RANK9_STORMCONTROL6_REVIEWED_177.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": model["casebookEncoding"],
            "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": return_binding,
            "sourceConferenceArchiveBinding": packet_binding,
            "sourceCandidateBinding": source_candidate_binding,
            "candidatePackageManifestBinding": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
            "retainedHoldsBinding": hold_binding,
            "procedureSourceBinding": procedure_source_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": acceptance["decision"],
            "authoredAcceptanceReceipt": bind(ACCEPTANCE),
            "authoredApplicationReceipt": application_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": index_position, "before": copy.deepcopy(old), "after": copy.deepcopy(updated)})
        after["entries"][index_position] = updated
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9stormcontrol6_reviewed_177/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "authority": bind(ACCEPTANCE),
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "sourceArchive": return_binding,
        "sourceConferenceArchive": packet_binding,
        "casebookBinding": casebook_binding,
        "holdsBinding": hold_binding,
        "candidatePackageManifestBinding": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "scope": acceptance["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 755, "pending": 93}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after_set = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 6 and len(pending_after_set) == 93 and pending_after_set == live_pending - ID_SET
    assert sum(row["authoredStatus"] == "reviewed-authored-operational-playtest" for row in after["entries"]) == 755
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    write_json(OPERATIONS, {"id": "RANK9-STORMCONTROL6-INDEX-OPERATIONS-179", "before": bind(BACKUP, raw=before_bytes), "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)}, "operations": operations, "inverse": {"semanticExact": True, "restores": "six identity rows, aggregate authored counts, standalone-envelope array and representation count"}, "onlyIdentityIds": IDS})
    temp_index = INDEX.with_suffix(".json.stormcontrol6-179.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = {"reviewedApplied": 755, "pending": 93, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 479, "scopedInterfaces": 173}
    remaining_groups = []
    for group in queue_before["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in pending_after_set]
        if left:
            row = copy.deepcopy(group)
            row["pendingIds"] = left
            row["pendingCount"] = len(left)
            row["freshPacketRequiredForCurrentAuthority"] = True
            for key in ["submissionReceipt", "submission", "directorReturn", "currentSubmission"]:
                row.pop(key, None)
            row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            remaining_groups.append(row)
    assert remaining_groups[0]["group"] == "rank9-psychic-fear7" and sum(group["pendingCount"] for group in remaining_groups) == 93
    catalog_ids = {row["id"] for row in catalog["spells"]}
    pending_doc = {"id": "CURRENT93-PENDING-IDENTITY-AUDIT-179", "recordedAtUtc": now(), "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": after["authoredCounts"], "pendingCount": 93, "pendingIds": sorted(pending_after_set), "allPendingExistInSourceCatalog": pending_after_set <= catalog_ids, "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0}
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)

    queue_after = copy.deepcopy(queue_before)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-179",
        "recordedAtUtc": now(),
        "currentAuthority": authority,
        "currentPendingGroups": remaining_groups,
        "nextSuggestedGroups": remaining_groups[:5],
        "nextGroup": remaining_groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": len(IDS), "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 93, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": remaining_groups[0]["group"], "pendingCount": remaining_groups[0]["pendingCount"], "historicalCandidate": remaining_groups[0].get("candidate"), "historicalArchive": remaining_groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"},
        "packetStatus": "RANK9_STORMCONTROL6_RETURN177_APPLIED_755_93",
        "currentSubmission": {"path": RECEIPT.name, "bytes": RECEIPT.stat().st_size, "sha256": sha(RECEIPT.read_bytes())},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT, "receipt": {"path": RECEIPT.name, "bytes": RECEIPT.stat().st_size, "sha256": sha(RECEIPT.read_bytes())}, "reviewIds": IDS, "acceptedIds": IDS, "appliedIds": IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
    })
    write_json(QUEUE_AFTER, queue_after)

    handoff = copy.deepcopy(handoff_before)
    previous_correction = handoff.pop("directorCorrectionRequest", None)
    handoff.update({
        "id": "CURRENT-HANDOFF-179",
        "recordedAtUtc": now(),
        "status": "RANK9_STORMCONTROL6_ACCEPTED_AND_APPLIED_NEXT_93_PENDING",
        "currentAuthority": authority,
        "currentIndexBinding": bind(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": bind(CATALOG, "authority/catalog.json"),
        "currentQueueBinding": bind(QUEUE_AFTER),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 93, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 6, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()},
        "nextGroup": remaining_groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed spell cohorts, or previously accepted/applied spell batches. Runtime, source, access, content, physical, lifecycle, extra-turn-source, unobserved-die, balance, cosmology, and release holds remain separate and active.",
        "resumePriority": f"Prepare a fresh {remaining_groups[0]['group']} packet bound to current 755/93 authority for the same GPT director, independently audit its exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": remaining_groups[0]["group"], "candidate": remaining_groups[0].get("candidate"), "historicalArchive": remaining_groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "request": "Prepare a fresh packet/archive against current 755/93 authority before the director review."},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT, "receipt": bind(RECEIPT), "archive": return_binding, "reviewIds": IDS, "acceptedIds": IDS, "appliedIds": IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
        "currentSubmissionBinding": bind(RECEIPT),
        "appliedDirectorReturn": {"decisionId": source_decision["id"], "archive": return_binding, "delivery": delivery_binding, "independentAudit": bind(INDEPENDENT_AUDIT), "accepted": True, "applied": True, "acceptedIds": IDS},
        "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(),
    })
    if previous_correction is not None:
        handoff["supersededDirectorCorrectionRequest"] = previous_correction
    write_json(HANDOFF_AFTER, handoff)

    validation_checks = [
        {"check": "Return177 independent audit passed with 25 checks and no failures", "passed": audit["status"] == "PASS" and audit["checksPassed"] == 25 and audit["checksFailed"] == 0},
        {"check": "Exactly six director-accepted identities changed from pending to reviewed", "passed": [op["identity"] for op in operations] == IDS and all(op["before"]["authoredStatus"] == "pending-authored-procedure" and op["after"]["authoredStatus"] == "reviewed-authored-operational-playtest" for op in operations)},
        {"check": "All unaccepted index entries are semantically unchanged", "passed": [row for row in after["entries"] if row["id"] not in ID_SET] == [row for row in before["entries"] if row["id"] not in ID_SET]},
        {"check": "Index operations reverse semantically to the exact prior index", "passed": inverse == before and BACKUP.read_bytes() == before_bytes},
        {"check": "Authored counts update to 755/93 and 479 complete procedures", "passed": after["authoredCounts"] == {"reviewed": 755, "pending": 93} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_AFTER},
        {"check": "All six native source cards, access, source status, and catalog bytes remain unchanged", "passed": CATALOG.read_bytes() == catalog_bytes and all(indexed["sourceStatus"] == "blocked-pending-operational-review" for indexed in [row for row in after["entries"] if row["id"] in ID_SET]) and all(procedures[sid]["nativeCardUnchanged"] == catalog_rows[sid] for sid in IDS)},
        {"check": "All 93 current pending identities still exist in the native source catalog", "passed": pending_doc["allPendingExistInSourceCatalog"] and len(pending_after_set) == 93},
        {"check": "Next queue group is a fresh Rank9 Psychic Fear7 packet", "passed": remaining_groups[0]["group"] == "rank9-psychic-fear7" and remaining_groups[0]["pendingCount"] == 7 and remaining_groups[0]["freshPacketRequiredForCurrentAuthority"] is True},
        {"check": "Runtime selection remains disabled and no closed cohort was reopened", "passed": all(row["after"]["runtimeSelectionEnabled"] is False for row in operations) and pending_doc["closed335AndCompletedCohortsReopened"] is False},
        {"check": "Retained source/access, extra-turn, physical/lifecycle, and unobserved-die holds remain", "passed": model["applicationCountSummary"]["totalScopedHolds"] == 95 and source_decision["qualifications"] and source_decision["priorFindingDispositions"][0]["blocking"] is False},
        {"check": "Candidate package binds the exact full return and accepted delivery", "passed": model["directorReturnArchiveBinding"] == return_binding and model["directorDeliveryBinding"] == delivery_binding and model["candidatePackageManifestBinding"]["sha256"] == sha((CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json").read_bytes())},
        {"check": "Deterministic casebook gzip is bound to the exact returned casebook member", "passed": casebook_binding["bytes"] == (CANDIDATE / "CASEBOOK.json.gz").stat().st_size and model["casebookSourceArchiveMemberBinding"] == {"path": "CASEBOOK.json", "bytes": casebook_total, "sha256": casebook_hash.hexdigest()}},
    ]
    assert all(item["passed"] for item in validation_checks), [item for item in validation_checks if not item["passed"]]
    validation = {
        "id": "RANK9-STORMCONTROL6-APPLICATION-VALIDATION-179",
        "recordedAtUtc": now(),
        "status": "PASS",
        "checksPassed": len(validation_checks),
        "checksFailed": 0,
        "checks": validation_checks,
        "beforeIndex": bind(BACKUP, raw=before_bytes),
        "afterIndex": bind(INDEX),
        "catalog": bind(CATALOG),
        "changedIdentityIds": IDS,
        "acceptedIds": IDS,
        "appliedIds": IDS,
        "authoredCounts": after["authoredCounts"],
        "completeReviewedStandaloneProcedures": COMPLETE_AFTER,
        "sourceStatusStillBlocked": True,
        "sourceCatalogUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "runtimeSelectionEnabled": False,
        "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before,
        "pendingIdentityAudit": bind(PENDING_AFTER),
        "nextGroup": remaining_groups[0]["group"],
        "nextPendingCount": remaining_groups[0]["pendingCount"],
    }
    write_json(VALIDATION, validation)

    old_start = START.read_text(encoding="utf-8-sig") if START.exists() else "# Decennium Descent — start here\n"
    marker = "**Prior checkpoint: ["
    marker_at = old_start.find(marker)
    historical = old_start[marker_at:] if marker_at >= 0 else old_start
    START.write_text(
        "**Current ordinary spell-review checkpoint [179](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_179.json):** GPT accepted and Codex independently audited and applied exactly cosmic-implosion, frozen-eternity, hellstorm, storm-of-vengeance, thunder-wrath, and storm-cage. Authority is **755 reviewed / 93 pending / 0 accepted-unapplied**, with 479 complete reviewed standalone procedures. All 140 return members, source bindings, repaired Monk profile, clock repairs, case calendars, and 2,592 events / 10,368 reversible operations pass independent checks. All 95 scoped holds remain, including the qualified extra-turn obligation and unobserved dice; runtime selection stays disabled. Next: prepare a fresh Rank9 Psychic Fear7 packet bound to 755/93 authority and continue until pending reaches zero.\n\n"
        f"See [handoff 179](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [queue 179](docs/audit/2026-10-08/full-game/director-spell-review-129/{QUEUE_AFTER.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [independent audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{INDEPENDENT_AUDIT.name}), [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), and [Return177 archive](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECV.name}/{RETURN.name}).\n\n"
        + historical,
        encoding="utf-8",
        newline="\n",
    )
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Storm Control6 Return177 applied\n\n"
        f"As of {ts}, authored ordinary-spell authority is **755 reviewed / 93 pending / 0 accepted-unapplied**, including 479 complete reviewed standalone procedures. GPT accepted and the application records exactly {', '.join(IDS)}.\n\n"
        f"Return177 is {return_binding['bytes']:,} bytes with SHA-256 `{return_binding['sha256']}`. The independent audit passed 25 checks, streamed all 140 member bindings, and replayed all 2,592 events with 10,368 reversible operations. Application validation passed {len(validation_checks)} checks.\n\n"
        "All 95 scoped holds remain, including the qualified extra-turn obligation, unobserved dice, and source/access/content/physical/lifecycle conditions. Native catalog cards, class access, and source status are unchanged; runtime selection remains disabled. This static authored review does not grant runtime, human-play, balance, cosmology, domain-closure, or release approval.\n\n"
        f"The next pending group is {remaining_groups[0]['group']} with {remaining_groups[0]['pendingCount']} identities and requires a fresh packet bound to 755/93 authority. Continue until pending reaches zero. See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8",
        newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "authority": authority, "nextGroup": remaining_groups[0]["group"], "nextPendingCount": remaining_groups[0]["pendingCount"], "independentAudit": audit["status"], "applicationValidation": validation["status"], "indexSha256": sha(INDEX.read_bytes()), "catalogUnchanged": True}, indent=2))


if __name__ == "__main__":
    apply()
