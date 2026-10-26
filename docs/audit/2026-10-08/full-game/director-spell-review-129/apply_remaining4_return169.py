from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
RECV = AUDIT / "remaining4_return169_received"
RETURN = RECV / "DD_Rank8_Remaining4_Director_Return169.zip"
DELIVERY = RECV / "DD_Rank8_Remaining4_Director_Return169_DELIVERY.json"
LOCAL_AUDIT = AUDIT / "REMAINING4_RETURN169_INDEPENDENT_AUDIT.json"
PACKET = FULL / "DD_Rank8_Remaining_4_Source_Conference_02.zip"
PACKET_VERIFY = AUDIT / "RANK8_REMAINING_4_SOURCE_CONFERENCE_02_VERIFICATION_168.json"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_remaining_4_source_conference_02.json"
SOURCE_REQUEST = FULL / "RANK8_REMAINING_4_SOURCE_CONFERENCE_02_REQUEST.txt"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_169.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_169.json"
PENDING_BEFORE = AUDIT / "CURRENT113_PENDING_IDENTITY_AUDIT_167.json"
IDS = ["prismatic-wall", "faction-convergence", "divine-intervention-lesser", "reality-patch"]
ID_SET = set(IDS)
BEFORE = {"reviewed": 735, "pending": 113, "acceptedUnapplied": 0}
AFTER = {"reviewed": 739, "pending": 109, "acceptedUnapplied": 0}
COMPLETE_BEFORE = 459
COMPLETE_AFTER = 463
REVIEW_ID = "REMAINING4-GPT-EXACT-ACCEPTANCE-169"
APP_ID = "REMAINING4-APPLICATION-170"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8remaining4_reviewed_169"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_REMAINING4_REVIEWED_169.md"
BACKUP = AUDIT / "authored_review_index.before_remaining4_170.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_REMAINING4_169.json"
ACCEPTANCE = AUDIT / "REMAINING4_EXACT_ACCEPTANCE_169.json"
APPLICATION = AUDIT / "REMAINING4_APPLICATION_170.json"
OPERATIONS = AUDIT / "REMAINING4_INDEX_OPERATIONS_170.json"
PENDING_AFTER = AUDIT / "CURRENT109_PENDING_IDENTITY_AUDIT_170.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_170.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_170.json"
VALIDATION = AUDIT / "REMAINING4_APPLICATION_VALIDATION_170.json"
RETURN_RECEIPT = AUDIT / "REMAINING4_GPT_RETURN_169.json"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_170.md"
CHAT_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def bind(path: Path, rel: str | None = None, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def preflight():
    local_audit = read_json(LOCAL_AUDIT)
    assert local_audit["status"] == "PASS" and local_audit["checksFailed"] == 0 and local_audit["checkCount"] == 29
    packet_verify = read_json(PACKET_VERIFY)
    assert packet_verify["status"] == "PASS" and packet_verify["failures"] == 0
    delivery = read_json(DELIVERY)
    return_bytes = RETURN.read_bytes()
    packet_bytes = PACKET.read_bytes()
    assert len(return_bytes) == delivery["archive"]["bytes"] == 29362298
    assert sha(return_bytes) == delivery["archive"]["sha256"] == "081aa49e33c7df0965428db6a63bbcbf656f226e3f496976a68750fb90330b0e"
    assert delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS
    with zipfile.ZipFile(RETURN) as archive:
        names = archive.namelist()
        assert len(names) == 85 and len(set(names)) == 85 and archive.testzip() is None
        members = {name: archive.read(name) for name in names}
    source_decision = json.loads(members["DIRECTOR_ACCEPTANCE.json"])
    procedures_list = json.loads(members["PROCEDURES.json"])["procedures"]
    procedures = {row["id"]: row for row in procedures_list}
    casebook = json.loads(members["CASEBOOK.json"])
    holds = json.loads(members["HOLD_REGISTER.json"])["holds"]
    counts = json.loads(members["COUNTS.json"])
    questions = json.loads(members["QUESTION_DISPOSITIONS.json"])
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE_BEFORE)
    handoff_before = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    source_candidate = read_json(SOURCE_CANDIDATE)
    assert source_decision["accepted"] is True and source_decision["applied"] is False
    assert source_decision["acceptedIds"] == IDS and source_decision["unacceptedIds"] == [] and source_decision["blockingFindings"] == []
    assert source_decision["authoritySnapshotBeforeDecision"] == {"reviewedApplied": 735, "pending": 113, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 459}
    assert source_decision["expectedCountsOnlyAfterSeparateApplication"] == {"reviewedApplied": 739, "pending": 109, "completeReviewedStandaloneProcedures": 463}
    assert source_decision["counts"] == counts and counts["procedures"] == 4 and counts["sourceQuestions"] == 22 and counts["selectedDispositions"] == 22 and counts["totalCases"] == 47 and counts["events"] == 539 and counts["reversibleEventOperations"] == 2156 and counts["holds"] == 29 and counts["independentFinalDataFailures"] == 0
    assert all(item["selectedOptionIndex"] is not None for item in questions["questions"])
    rows = {entry["id"]: entry for entry in before["entries"]}
    catalog_rows = {entry["id"]: entry for entry in catalog["spells"]}
    live_pending = {entry["id"] for entry in before["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 735, "pending": 113} and before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    assert len(live_pending) == 113 and ID_SET <= live_pending
    assert all(procedures[sid]["nativeSource"] == catalog_rows[sid] for sid in IDS)
    assert all(rows[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS)
    assert queue["currentAuthority"] == handoff_before["currentAuthority"] == {"reviewedApplied": 735, "pending": 113, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 459, "scopedInterfaces": 173}
    assert queue["packetStatus"] == "REMAINING4_SUBMITTED_AWAITING_DIRECTOR_RETURN" and queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert handoff_before["status"] == "REMAINING4_SUBMITTED_AWAITING_DIRECTOR_RETURN"
    assert handoff_before["currentIndexBinding"]["sha256"] == sha(before_bytes) and pending_before["indexBinding"]["sha256"] == sha(before_bytes)
    assert pending_before["pendingCount"] == 113 and ID_SET <= set(pending_before["pendingIds"])
    assert members["source/CANDIDATE.json"] == SOURCE_CANDIDATE.read_bytes()
    assert members["source/DD_Rank8_Remaining_4_Source_Conference_02.zip"] == packet_bytes
    assert source_candidate["currentPendingIds"] == IDS
    outputs = [CANDIDATE, STAGING, MANUSCRIPT, BACKUP, DECISION, ACCEPTANCE, APPLICATION, OPERATIONS, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, VALIDATION, RETURN_RECEIPT, SNAPSHOT]
    assert not [str(path) for path in outputs if path.exists()], "Application output already exists; inspect before retrying."
    assert CATALOG.read_bytes() == catalog_bytes
    return locals()


def apply() -> None:
    data = preflight()
    ts = now()
    before = data["before"]
    queue = data["queue"]
    handoff_before = data["handoff_before"]
    members = data["members"]
    source_decision = data["source_decision"]
    counts = data["counts"]
    before_bytes = data["before_bytes"]
    catalog_bytes = data["catalog_bytes"]
    live_pending = data["live_pending"]
    return_bytes = data["return_bytes"]
    packet_bytes = data["packet_bytes"]
    holds = data["holds"]
    procedures = data["procedures"]
    excluded_pending = sorted(live_pending - ID_SET)

    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    archive_omitted = sorted(name for name in members if name.startswith("accepted-comparisons/"))
    for name, raw in members.items():
        if name in archive_omitted:
            continue
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(return_bytes)
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(packet_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(SOURCE_CANDIDATE.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_REQUEST.txt").write_bytes(SOURCE_REQUEST.read_bytes())
    (STAGING / "SOURCE_PACKET_VERIFICATION.json").write_bytes(PACKET_VERIFY.read_bytes())
    (STAGING / "RETURN_INDEPENDENT_AUDIT.json").write_bytes(LOCAL_AUDIT.read_bytes())
    (STAGING / "DIRECTOR_DELIVERY.json").write_bytes(DELIVERY.read_bytes())
    (STAGING / "GPT_SUBMISSION_RECEIPT.json").write_bytes((AUDIT / "REMAINING4_GPT_SUBMISSION_169.json").read_bytes())
    casebook_bytes = members["CASEBOOK.json"]
    with (STAGING / "CASEBOOK.json.gz").open("wb") as out:
        with gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as compressed:
            compressed.write(casebook_bytes)
    assert gzip.decompress((STAGING / "CASEBOOK.json.gz").read_bytes()) == casebook_bytes

    spell_rows = []
    catalog_rows = {entry["id"]: entry for entry in data["catalog"]["spells"]}
    for pos, sid in enumerate(IDS):
        procedure = procedures[sid]
        native = procedure["nativeSource"]
        assert native == catalog_rows[sid]
        spell_rows.append({
            "id": sid,
            "name": native["name"],
            "procedure": copy.deepcopy(procedure),
            "directorProcedureRecord": copy.deepcopy(procedure),
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "questionDispositions": copy.deepcopy(procedure["questionRules"]),
            "runtimeSelectionEnabled": False,
        })
    hold_ids = [hold["id"] for hold in holds]
    returned_count_info = {
        "procedures": 4,
        "sourceQuestions": 22,
        "selectedDispositions": 22,
        "originalFutureCaseObligations": 6,
        "mainCases": 9,
        "branches": 38,
        "totalCases": 47,
        "events": 539,
        "reversibleEventOperations": 2156,
        "proposalOperations": 16,
        "holds": 29,
        "wholeCaseHeldBranches": 4,
        "independentFinalDataChecks": 16261,
        "independentFinalDataFailures": 0,
    }
    model = {
        "schemaVersion": 1,
        "moduleId": "rank8-remaining4-reviewed-169",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly the four GPT-accepted Rank8 Remaining4 static authored procedures. Native cards, catalog rows, class access, source status, accepted interfaces, and global rules remain unchanged. All 29 hold records and four whole-case holds remain. Runtime selection stays disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "The common timing and resource fields remain local to each exact spell record; no global rule or accepted interface is changed.", "perSpellCommon": {sid: copy.deepcopy(procedures[sid]["commonRules"]) for sid in IDS}},
        "spells": spell_rows,
        "questionDispositions": json.loads(members["QUESTION_DISPOSITIONS.json"]),
        "originalObligations": json.loads(members["ORIGINAL_OBLIGATIONS.json"]),
        "futureCaseDispositions": json.loads(members["OBLIGATION_COVERAGE.json"]),
        "returnCounts": counts,
        "applicationCountSummary": returned_count_info,
        "holdIds": hold_ids,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLD_REGISTER.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSALS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(casebook_bytes), "sha256": sha(casebook_bytes)},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip",
        "returnArchiveOnlyMembers": archive_omitted,
        "returnArchiveOnlyRationale": "Accepted-comparison filenames may exceed Windows extraction path limits. These members remain byte-exact in DIRECTOR_RETURN_ARCHIVE.zip and were independently verified against MEMBER_MANIFEST.json.",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip",
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "DIRECTOR_RETURN/STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "DIRECTOR_RETURN/DIRECTOR_ACCEPTANCE.json",
        "directorReturnDeliveryObservation": {"source": "GPT Library delivery JSON cross-checked with DIRECTOR_ACCEPTANCE.json and MEMBER_MANIFEST.json", "archiveBytes": len(return_bytes), "archiveSha256": sha(return_bytes), "accepted": True, "applied": False, "memberCount": 85, "passedDataChecks": 16261, "failedDataChecks": 0, "passedPackageChecks": 260, "failedPackageChecks": 0, "independentLocalAuditChecks": 29, "independentLocalAuditFailures": 0},
        "directorReturnBinding": bind(RETURN, RETURN.relative_to(ROOT).as_posix(), return_bytes),
        "directorDeliveryBinding": bind(DELIVERY),
        "sourceConferencePacketVerification": bind(PACKET_VERIFY),
        "independentReturnAudit": bind(LOCAL_AUDIT),
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
            raw = path.read_bytes()
            package_files.append({"path": relative, "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-REMAINING4-CANDIDATE-PACKAGE-MANIFEST-170",
        "sourceArchive": {"name": RETURN.name, "bytes": len(return_bytes), "sha256": sha(return_bytes)},
        "files": package_files,
        "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
        "returnArchiveOnlyMembers": archive_omitted,
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    model["candidatePackageManifestBinding"] = bind(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")
    write_json(STAGING / "MODEL.json", model)
    model_binding = bind(STAGING / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json")
    casebook_binding = bind(STAGING / "CASEBOOK.json.gz", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    return_binding = bind(RETURN, RETURN.relative_to(ROOT).as_posix(), return_bytes)
    packet_binding = bind(PACKET, PACKET.relative_to(ROOT).as_posix(), packet_bytes)
    candidate_binding = bind(SOURCE_CANDIDATE)
    hold_binding = bind(director_dir / "HOLD_REGISTER.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLD_REGISTER.json")
    proposal_binding = bind(director_dir / "PROPOSALS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSALS.json")
    procedure_source_binding = bind(director_dir / "DIRECTOR_ACCEPTANCE.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_ACCEPTANCE.json")

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-REMAINING4-169",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT_URL},
        "decisionId": source_decision["id"],
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "remainingBlockingDefects": [],
        "verification": {"directorSourceChecksPassed": 223, "directorSourceChecksFailed": 0, "directorPackageChecksPassed": 260, "independentFinalDataChecksPassed": 16261, "independentFinalDataChecksFailed": 0, "independentReturnAudit": read_json(LOCAL_AUDIT), "sourcePacketVerification": read_json(PACKET_VERIFY), "returnArchiveMembers": 85, "sourceArchiveMembers": 124, "sourceQuestions": 22, "futureCaseObligations": 6, "cases": 47, "wholeHeldCases": 4, "events": 539, "reversibleEventOperations": 2156, "proposalOperations": 16, "retainedHolds": 29},
        "acceptedArchive": {"name": RETURN.name, "bytes": len(return_bytes), "sha256": sha(return_bytes)},
        "sourceArchive": {"name": PACKET.name, "bytes": len(packet_bytes), "sha256": sha(packet_bytes)},
        "scope": source_decision["scope"],
        "holdScope": "All 29 source, campaign, runtime, human-play, balance, cosmology, release, transport, faction, invocation, physical and inherited source holds remain. Four whole-case branches remain held. No runtime, human-play, balance, cosmology, or release approval is granted.",
        "excludedClaims": {"runtime": False, "humanPlay": False, "balance": False, "cosmology": False, "release": False, "canonicalApplication": False},
        "directorMadeNoCanonicalChanges": True,
    }
    write_json(DECISION, decision_record)
    acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision_record,
        "directorReturn": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": len(return_bytes), "sha256": sha(return_bytes)},
        "acceptedIds": IDS,
        "countsBefore": {**BEFORE, "scopedInterfaces": 173},
        "countsAfter": {**AFTER, "scopedInterfaces": 173},
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "acceptedCases": 47,
        "acceptedMainCases": 9,
        "acceptedBranches": 38,
        "wholeHeldCases": 4,
        "acceptedEvents": 539,
        "eventOperations": 2156,
        "retainedHolds": 29,
        "sourceStatusPreserved": "blocked-pending-operational-review for all four identities; static authored procedure review only.",
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
    os.replace(STAGING, CANDIDATE)
    manuscript_text = (CANDIDATE / "DIRECTOR_RETURN" / "STANDALONE_PROCEDURES.md").read_text(encoding="utf-8-sig")
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript_text, encoding="utf-8", newline="\n")
    app = {
        "id": APP_ID,
        "recordedAtUtc": ts,
        "status": "APPLIED_FOUR_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply exact accepted ordinary-spell batches, push each batch to GitHub, and continue until no pending spell identities remain.",
        "acceptedIds": IDS,
        "directorAcceptance": bind(ACCEPTANCE),
        "directorDecision": bind(DECISION),
        "directorReturn": return_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "indexBefore": bind(BACKUP, raw=before_bytes),
        "counts": {"before": {**BEFORE, "scopedInterfaces": 173}, "after": {**AFTER, "scopedInterfaces": 173}},
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "cases": 47,
        "mainCases": 9,
        "branches": 38,
        "wholeHeldCases": 4,
        "events": 539,
        "eventOperations": 2156,
        "retainedHolds": 29,
        "sourceStatusPreservedAsBlocked": True,
        "catalogChanged": False,
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
            "procedureFile": "../spell_candidates/rank8remaining4_reviewed_169/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/sharedRules/perSpellCommon/{sid}",
            "manuscript": "../../../docs/spells/candidates/RANK8_REMAINING4_REVIEWED_169.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json",
            "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": return_binding,
            "sourceConferenceArchiveBinding": packet_binding,
            "sourceCandidateBinding": candidate_binding,
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
        "file": "../spell_candidates/rank8remaining4_reviewed_169/MODEL.json",
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
    after["authoredCounts"] = {"reviewed": 739, "pending": 109}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after = {entry["id"] for entry in after["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 4 and len(pending_after) == 109 and pending_after == live_pending - ID_SET
    assert sum(entry["authoredStatus"] == "reviewed-authored-operational-playtest" for entry in after["entries"]) == 739
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    BACKUP.write_bytes(before_bytes)
    write_json(OPERATIONS, {"id": "REMAINING4-INDEX-OPERATIONS-170", "before": bind(BACKUP, raw=before_bytes), "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)}, "operations": operations, "inverse": {"semanticExact": True, "restores": "four prior identity rows, aggregate authored counts, standalone-envelope array and representation count"}, "onlyIdentityIds": IDS})
    temp_index = INDEX.with_suffix(".json.remaining4-170.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = {"reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173}
    remaining_groups = []
    for group in queue["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in pending_after]
        if left:
            row = copy.deepcopy(group)
            row["pendingIds"] = left
            row["pendingCount"] = len(left)
            row["freshPacketRequiredForCurrentAuthority"] = True
            for key in ["submissionReceipt", "submission"]:
                row.pop(key, None)
            row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            remaining_groups.append(row)
    assert remaining_groups[0]["group"] == "rank9-catastrophe10" and sum(group["pendingCount"] for group in remaining_groups) == 109
    pending_doc = {"id": "CURRENT109-PENDING-IDENTITY-AUDIT-170", "recordedAtUtc": now(), "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": after["authoredCounts"], "pendingCount": 109, "pendingIds": sorted(pending_after), "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in data["catalog"]["spells"]) for sid in pending_after), "closed335AndCompletedCohortsReopened": False}
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)

    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-170",
        "recordedAtUtc": now(),
        "currentAuthority": authority,
        "currentPendingGroups": remaining_groups,
        "nextSuggestedGroups": remaining_groups[:5],
        "nextGroup": remaining_groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": len(IDS), "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 109, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": remaining_groups[0]["group"], "pendingCount": remaining_groups[0]["pendingCount"], "historicalCandidate": remaining_groups[0].get("candidate"), "historicalArchive": remaining_groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"},
        "packetStatus": "REMAINING4_RETURN169_APPLIED_739_109",
        "currentSubmission": {"path": RETURN_RECEIPT.name, "bytes": RETURN_RECEIPT.stat().st_size, "sha256": sha(RETURN_RECEIPT.read_bytes())},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT_URL, "receipt": {"path": RETURN_RECEIPT.name, "bytes": RETURN_RECEIPT.stat().st_size, "sha256": sha(RETURN_RECEIPT.read_bytes())}, "reviewIds": IDS, "appliedIds": IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
    })
    write_json(QUEUE_AFTER, queue_after)

    handoff = copy.deepcopy(handoff_before)
    handoff.update({
        "id": "CURRENT-HANDOFF-170",
        "recordedAtUtc": now(),
        "status": "REMAINING4_ACCEPTED_AND_APPLIED_NEXT_109_PENDING",
        "currentAuthority": authority,
        "currentIndexBinding": bind(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": bind(CATALOG, "authority/catalog.json"),
        "currentQueueBinding": bind(QUEUE_AFTER),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 109, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": LOCAL_AUDIT.relative_to(ROOT).as_posix()},
        "nextGroup": remaining_groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed spell cohorts, or previously accepted/applied spell batches. Runtime, source, access, cosmology, content, lifecycle and release holds remain separate and active.",
        "resumePriority": f"Prepare a fresh {remaining_groups[0]['group']} packet against current 739/109 authority, submit it to the same GPT director, independently audit the exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": remaining_groups[0]["group"], "candidate": remaining_groups[0].get("candidate"), "historicalArchive": remaining_groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "request": "Build a fresh source packet and archive bound to current 739/109 authority before director review."},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT_URL, "receipt": {"path": RETURN_RECEIPT.relative_to(ROOT).as_posix(), "bytes": RETURN_RECEIPT.stat().st_size, "sha256": sha(RETURN_RECEIPT.read_bytes())}, "archive": return_binding, "reviewIds": IDS, "acceptedIds": IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
        "currentSubmissionBinding": bind(RETURN_RECEIPT),
    })
    write_json(HANDOFF_AFTER, handoff)

    old_start = START.read_text(encoding="utf-8-sig") if START.exists() else "# Decennium Descent — start here\n"
    marker = "**Prior checkpoint: ["
    marker_at = old_start.find(marker)
    historical = old_start[marker_at:] if marker_at >= 0 else old_start.split("\n", 2)[-1]
    START.write_text(
        "# Decennium Descent — start here\n\n"
        f"**Current ordinary spell-review checkpoint [170](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_170.json):** the GPT director accepted and Codex independently audited and applied exactly prismatic-wall, faction-convergence, divine-intervention-lesser, and reality-patch. Authority is **739 reviewed / 109 pending / 0 accepted-unapplied**, with 463 complete reviewed standalone procedures. The exact director ZIP SHA-256 is `{sha(return_bytes)}`; local independent verification passed 29 checks, while the director reports 16,261 data, 260 package, and 266 saved-copy checks.\n\n"
        f"All 29 holds remain, including four whole-case held branches. Native catalog/access and source status remain unchanged; procedures stay disabled for runtime selection. Runtime, human-play, balance, cosmology, and release approval remain separate. The next group is **{remaining_groups[0]['group']}** and needs a fresh 739/109 packet. Continue until pending reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{ACCEPTANCE.name}), [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), and [director return ZIP](docs/audit/2026-10-08/full-game/director-spell-review-129/remaining4_return169_received/{RETURN.name}).\n\n"
        + historical,
        encoding="utf-8",
        newline="\n",
    )
    SNAPSHOT.write_text(
        f"# Ordinary spell review snapshot — Remaining4 Return169\n\nAs of 2026-10-25, authored ordinary-spell authority is **739 reviewed / 109 pending / 0 accepted-unapplied**, including 463 complete reviewed standalone procedures. The GPT director accepted and this application records exactly {', '.join(IDS)}.\n\n"
        f"The return ZIP is {len(return_bytes):,} bytes with SHA-256 `{sha(return_bytes)}`. GPT reports 16,261 final data checks, 260 package checks, and 266 saved-copy checks passing. The independent local audit passed 29 checks, including all 113 current source bindings, the exact accepted decision, ZIP/member hashes, 47-case replay with 2,156 forward/inverse operations, and retained holds.\n\n"
        "All 29 hold records remain, including four whole-case held branches. Native catalog data, class access, and source status are unchanged; runtime selection remains disabled. This static authored review does not grant runtime, human-play, balance, cosmology, or release approval.\n\n"
        f"The next pending group is {remaining_groups[0]['group']} with {remaining_groups[0]['pendingCount']} spells and requires a fresh packet against 739/109 authority. Continue until pending reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{ACCEPTANCE.name}), and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8",
        newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    print(json.dumps({"status": "APPLIED_READY_FOR_INDEPENDENT_VERIFICATION", "acceptedIds": IDS, "authority": authority, "nextGroup": remaining_groups[0]["group"], "nextPendingCount": remaining_groups[0]["pendingCount"], "returnArchive": bind(RETURN), "indexSha256": sha(INDEX.read_bytes())}, indent=2))


if __name__ == "__main__":
    apply()
