from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
RECEIVED = AUDIT / "information-time4_return162_received"
RETURN_ZIP = RECEIVED / "DD_Rank8_Information_Time_4_Director_Return162.zip"
RETURN_EXTRACTED = RECEIVED / "extracted"
LOCAL_AUDIT = RECEIVED / "INFORMATION_TIME4_RETURN162_LOCAL_AUDIT.json"
PACKET_AUDIT = AUDIT / "RANK8_INFORMATION_TIME4_PACKET163_VERIFICATION.json"
PACKET_ZIP = FULL / "DD_Rank8_Information_Time_4_Source_Conference_03.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_information_time_4_source_conference_03.json"
SOURCE_REQUEST = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_03_REQUEST.txt"

INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_163.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_163.json"
PENDING_BEFORE = AUDIT / "CURRENT122_PENDING_IDENTITY_AUDIT_161.json"

REVIEW_ID = "IT162-DIRECTOR-EXACT-ACCEPTANCE"
APP_ID = "RANK8-INFORMATION-TIME4-APPLICATION-164"
IDS = ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]
ID_SET = set(IDS)
BEFORE = {"reviewed": 726, "pending": 122, "acceptedUnapplied": 0}
AFTER = {"reviewed": 730, "pending": 118, "acceptedUnapplied": 0}
COMPLETE_BEFORE = 450
COMPLETE_AFTER = 454

CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8informationtime4_reviewed_162"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_INFORMATION_TIME4_REVIEWED_162.md"
BACKUP = AUDIT / "authored_review_index.before_information_time4_164.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_INFORMATION_TIME4_162.json"
ACCEPTANCE = AUDIT / "INFORMATION_TIME4_EXACT_ACCEPTANCE_162.json"
APPLICATION = AUDIT / "INFORMATION_TIME4_APPLICATION_164.json"
OPERATIONS = AUDIT / "INFORMATION_TIME4_INDEX_OPERATIONS_164.json"
VALIDATION = AUDIT / "INFORMATION_TIME4_APPLICATION_VALIDATION_164.json"
PENDING_AFTER = AUDIT / "CURRENT118_PENDING_IDENTITY_AUDIT_164.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_164.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_164.json"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_164.md"
START = ROOT / "START_HERE.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def binding(path: Path, rel: str | None = None, raw: bytes | None = None) -> dict:
    content = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(content), "sha256": sha(content)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_inputs() -> dict:
    assert read_json(LOCAL_AUDIT)["status"] == "PASSED_EXACT_ACCEPTED_RETURN_READY_FOR_APPLICATION"
    assert read_json(PACKET_AUDIT)["status"] == "PASS" and read_json(PACKET_AUDIT)["checksFailed"] == 0
    assert sha(RETURN_ZIP.read_bytes()) == "7f3cf81d8c36ea63d7420d462b532699300c6c5304301224bf78845a7c0a3cd8"
    assert sha(PACKET_ZIP.read_bytes()) == "bb09971e7a3a83ab85e360b6669d182646a11df607efc11d3904be34207fec50"

    with ZipFile(RETURN_ZIP) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    source = json.loads(members["DIRECTOR_DECISION.json"])
    model = {sid: json.loads(members[f"procedures/{sid}.json"]) for sid in IDS}
    casebook = json.loads(members["CASEBOOK.json"])
    holds = json.loads(members["HOLDS.json"])
    counts = source["counts"]
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)

    assert source["accepted"] is True and source["applied"] is False
    assert source["acceptedIds"] == IDS and source["remainingAcceptanceBlockers"] == []
    assert source["inputAuthority"]["reviewedApplied"] == BEFORE["reviewed"]
    assert source["inputAuthority"]["pending"] == BEFORE["pending"]
    assert source["inputAuthority"]["acceptedUnapplied"] == BEFORE["acceptedUnapplied"]
    assert source["canonicalFilesEdited"] is False and source["applicationPerformed"] is False
    assert all(value is False for value in source["qualifications"].values())
    assert source["sourceArchive"]["sha256"] == sha(PACKET_ZIP.read_bytes())
    assert source["sourceArchive"]["bytes"] == PACKET_ZIP.stat().st_size
    assert len(casebook) == counts["cases"] == 56 and len(holds) == counts["holds"] == 16
    assert sum(len(c["events"]) for c in casebook) == counts["events"] == 246

    rows = {entry["id"]: entry for entry in before["entries"]}
    catalog_rows = {entry["id"]: entry for entry in catalog["spells"]}
    live_pending = {entry["id"] for entry in before["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": BEFORE["reviewed"], "pending": BEFORE["pending"]}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    assert len(live_pending) == BEFORE["pending"] and ID_SET <= live_pending
    assert queue["currentAuthority"] == handoff["currentAuthority"] == {
        "reviewedApplied": 726, "pending": 122, "acceptedUnapplied": 0,
        "completeReviewedStandaloneProcedures": 450, "scopedInterfaces": 173,
    }
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert pending_before["indexBinding"]["sha256"] == sha(before_bytes)
    assert pending_before["pendingCount"] == BEFORE["pending"]
    assert all(model[sid]["nativeSourceAndAccessUnchanged"] == catalog_rows[sid] for sid in IDS)
    assert all(rows[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS)

    outputs = [CANDIDATE, STAGING, MANUSCRIPT, BACKUP, DECISION, ACCEPTANCE, APPLICATION,
               OPERATIONS, VALIDATION, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, SNAPSHOT]
    assert not [str(path) for path in outputs if path.exists()], "Application output exists; inspect before retrying."
    assert CATALOG.read_bytes() == catalog_bytes
    return locals()


def apply() -> None:
    data = load_inputs()
    ts = now()
    before = data["before"]
    catalog = data["catalog"]
    queue = data["queue"]
    handoff_before = data["handoff"]
    members = data["members"]
    decision_source = data["source"]
    counts = data["counts"]
    before_bytes = data["before_bytes"]
    catalog_bytes = data["catalog_bytes"]
    excluded_pending = sorted(data["live_pending"] - ID_SET)
    archive_bytes = RETURN_ZIP.read_bytes()
    packet_bytes = PACKET_ZIP.read_bytes()

    # Preserve every returned file exactly and add a normalized pointer envelope.
    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    for name, raw in members.items():
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(packet_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(SOURCE_CANDIDATE.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_REQUEST.txt").write_bytes(SOURCE_REQUEST.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_PACKET_VERIFICATION.json").write_bytes(PACKET_AUDIT.read_bytes())
    (STAGING / "RETURN_INDEPENDENT_AUDIT.json").write_bytes(LOCAL_AUDIT.read_bytes())

    casebook_bytes = members["CASEBOOK.json"]
    casebook_gz = STAGING / "CASEBOOK.json.gz"
    with casebook_gz.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
            compressed.write(casebook_bytes)
    assert gzip.decompress(casebook_gz.read_bytes()) == casebook_bytes

    hold_rows = json.loads(members["HOLDS.json"])
    procedure_rows = []
    for position, sid in enumerate(IDS):
        procedure = data["model"][sid]
        native = procedure["nativeSourceAndAccessUnchanged"]
        old = next(row for row in before["entries"] if row["id"] == sid)
        assert native["id"] == sid and native["name"] == old["name"]
        procedure_rows.append({
            "id": sid,
            "name": native["name"],
            "procedure": {"common": copy.deepcopy(procedure["common"]), "rules": copy.deepcopy(procedure["rules"])},
            "directorProcedureRecord": copy.deepcopy(procedure),
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "procedureSourceQuestionIds": copy.deepcopy(procedure["questionIds"]),
            "runtimeSelectionEnabled": False,
        })
    hold_ids = [row["id"] for row in hold_rows]
    normalized_model = {
        "schemaVersion": 1,
        "moduleId": "rank8informationtime4-reviewed-162",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly the four GPT-accepted Information/Time4 static authored procedures. Native spell cards, catalog rows, class access and source status remain unchanged. All 16 hold categories and all 20 held dependent branches remain. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Common rules are preserved per spell; no global interface or shared rule is changed.", "perSpellCommon": {sid: copy.deepcopy(data["model"][sid]["common"]) for sid in IDS}},
        "spells": procedure_rows,
        "questionDispositions": json.loads(members["QUESTION_DISPOSITIONS.json"]),
        "originalIdentityDispositions": json.loads(members["ORIGINAL_QUESTION_DISPOSITIONS.json"]),
        "futureObligationDispositions": json.loads(members["FUTURE_OBLIGATION_DISPOSITIONS.json"]),
        "returnCounts": counts,
        "holdIds": hold_ids,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(casebook_bytes), "sha256": sha(casebook_bytes)},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip",
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "DIRECTOR_RETURN/STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
        "directorReturnBinding": binding(RETURN_ZIP, f"{RECEIVED.relative_to(ROOT).as_posix()}/{RETURN_ZIP.name}", archive_bytes),
        "directorReturnDeliveryObservation": {
            "source": "Rendered matching ChatGPT Library delivery JSON, verified against DIRECTOR_DECISION.json and embedded MEMBER_MANIFEST.json",
            "archiveBytes": 22_993_185,
            "archiveSha256": "7f3cf81d8c36ea63d7420d462b532699300c6c5304301224bf78845a7c0a3cd8",
            "accepted": True,
            "applied": False,
            "memberCount": 96,
            "passedValidationChecks": 14_095,
            "failedValidationChecks": 0,
            "passedPackageChecks": 389,
            "failedPackageChecks": 0,
        },
        "sourceConferencePacketVerification": binding(PACKET_AUDIT),
        "independentReturnAudit": binding(LOCAL_AUDIT),
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
        rel = path.relative_to(STAGING).as_posix()
        if path.is_file() and rel not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            raw = path.read_bytes()
            package_files.append({"path": rel, "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-INFORMATION-TIME4-CANDIDATE-PACKAGE-MANIFEST-164",
        "sourceArchive": {"name": RETURN_ZIP.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "files": package_files,
        "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    package_manifest_binding = binding(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")
    normalized_model["candidatePackageManifestBinding"] = package_manifest_binding
    write_json(STAGING / "MODEL.json", normalized_model)
    model_binding = binding(STAGING / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json")
    casebook_binding = binding(casebook_gz, f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    archive_binding = binding(RETURN_ZIP, f"{RECEIVED.relative_to(ROOT).as_posix()}/{RETURN_ZIP.name}", archive_bytes)
    packet_binding = binding(STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip", f"{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_ARCHIVE.zip")
    source_candidate_binding = binding(STAGING / "SOURCE_CONFERENCE_CANDIDATE.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_CANDIDATE.json")
    hold_binding = binding(director_dir / "HOLDS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLDS.json")
    proposal_binding = binding(director_dir / "PROPOSAL_OPERATIONS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json")
    procedure_source_binding = binding(director_dir / "DIRECTOR_DECISION.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json")

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-INFORMATION-TIME4-162",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": decision_source["id"],
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "remainingBlockingDefects": [],
        "verification": {
            "directorChecksPassed": counts["passedChecks"],
            "directorChecksFailed": counts["failedChecks"],
            "directorPackageChecksPassed": 389,
            "independentReturnAudit": read_json(LOCAL_AUDIT),
            "sourcePacketVerification": read_json(PACKET_AUDIT),
            "returnArchiveMembers": 96,
            "sourceArchiveMembers": 68,
            "conferenceQuestions": counts["conferenceQuestions"],
            "originalIdentityQuestions": counts["originalIdentityQuestions"],
            "futureObligations": counts["futureObligations"],
            "cases": counts["cases"],
            "wholeHeldCases": counts["wholeCaseHeld"],
            "events": counts["events"],
            "eventOperations": counts["eventOperations"],
            "proposalOperations": counts["proposalOperations"],
            "retainedHolds": counts["holds"],
        },
        "acceptedArchive": {"name": RETURN_ZIP.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "sourceArchive": {"name": PACKET_ZIP.name, "bytes": len(packet_bytes), "sha256": sha(packet_bytes)},
        "scope": decision_source["scope"],
        "holdScope": "All sixteen source-access, boundary, information, physical-content, history, action-time, lifecycle, copy-adapter, suppression, agency, runtime-human-play, balance, cosmology, release, provenance and inherited hold categories remain. All twenty wholly dependent cases remain held. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
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
        "directorReturn": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{RETURN_ZIP.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "directorReturnDeliveryEvidence": normalized_model["directorReturnDeliveryObservation"],
        "acceptedIds": IDS,
        "countsBefore": {**BEFORE, "scopedInterfaces": 173},
        "countsAfter": {**AFTER, "scopedInterfaces": 173},
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "acceptedCases": counts["cases"],
        "acceptedMainCases": counts["mainCases"],
        "acceptedBranches": counts["branches"],
        "wholeHeldCases": counts["wholeCaseHeld"],
        "acceptedEvents": counts["events"],
        "eventOperations": counts["eventOperations"],
        "retainedHolds": counts["holds"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all four identities; authored procedure review only.",
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
        "ownerInstruction": "Apply each exact accepted ordinary-spell batch, push it to GitHub, and continue until no pending spell identities remain.",
        "acceptedIds": IDS,
        "directorAcceptance": binding(ACCEPTANCE),
        "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {**BEFORE, "scopedInterfaces": 173}, "after": {**AFTER, "scopedInterfaces": 173}},
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "cases": counts["cases"],
        "completeStaticFixtures": counts["cases"] - counts["wholeCaseHeld"],
        "wholeHeldCases": counts["wholeCaseHeld"],
        "events": counts["events"],
        "eventOperations": counts["eventOperations"],
        "retainedHolds": counts["holds"],
        "sourceStatusPreservedAsBlocked": True,
        "catalogChanged": False,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(APPLICATION, app)
    app_binding = binding(APPLICATION)

    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(IDS):
        index_pos = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_pos]
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank8informationtime4_reviewed_162/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRules/perSpellCommon",
            "manuscript": "../../../docs/spells/candidates/RANK8_INFORMATION_TIME4_REVIEWED_162.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json",
            "casebookSourceArchiveMemberBinding": normalized_model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": archive_binding,
            "sourceConferenceArchiveBinding": packet_binding,
            "sourceCandidateBinding": source_candidate_binding,
            "candidatePackageManifestBinding": package_manifest_binding,
            "retainedHoldsBinding": hold_binding,
            "procedureSourceBinding": procedure_source_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": acceptance["decision"],
            "authoredAcceptanceReceipt": binding(ACCEPTANCE),
            "authoredApplicationReceipt": app_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": index_pos, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][index_pos] = new

    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank8informationtime4_reviewed_162/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "authority": binding(ACCEPTANCE),
        "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}",
        "sourceArchive": archive_binding,
        "sourceConferenceArchive": packet_binding,
        "casebookBinding": casebook_binding,
        "holdsBinding": hold_binding,
        "candidatePackageManifestBinding": package_manifest_binding,
        "scope": acceptance["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": AFTER["reviewed"], "pending": AFTER["pending"]}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 4 and len(pending_after) == AFTER["pending"] and pending_after == data["live_pending"] - ID_SET
    assert sum(row["authoredStatus"] == "reviewed-authored-operational-playtest" for row in after["entries"]) == AFTER["reviewed"]
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    BACKUP.write_bytes(before_bytes)
    ops_doc = {
        "id": "INFORMATION-TIME4-INDEX-OPERATIONS-164",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "four prior entries, aggregate authored counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    write_json(OPERATIONS, ops_doc)
    temp_index = INDEX.with_suffix(".json.information-time4-164.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = {
        "reviewedApplied": AFTER["reviewed"],
        "pending": AFTER["pending"],
        "acceptedUnapplied": AFTER["acceptedUnapplied"],
        "completeReviewedStandaloneProcedures": COMPLETE_AFTER,
        "scopedInterfaces": 173,
    }
    remaining_groups = []
    for group in queue["currentPendingGroups"]:
        remaining = [sid for sid in group["pendingIds"] if sid in pending_after]
        if remaining:
            row = copy.deepcopy(group)
            row["pendingIds"] = remaining
            row["pendingCount"] = len(remaining)
            row["freshPacketRequiredForCurrentAuthority"] = True
            row.pop("submission", None)
            row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            remaining_groups.append(row)
    assert remaining_groups[0]["group"] == "rank8-planar5" and sum(g["pendingCount"] for g in remaining_groups) == AFTER["pending"]
    pending_doc = {
        "id": "CURRENT118-PENDING-IDENTITY-AUDIT-164",
        "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": binding(INDEX),
        "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"],
        "pendingCount": AFTER["pending"],
        "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in catalog["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False,
        "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)

    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-164",
        "recordedAtUtc": now(),
        "currentAuthority": authority,
        "currentPendingGroups": remaining_groups,
        "nextSuggestedGroups": remaining_groups[:5],
        "nextGroup": remaining_groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": len(IDS), "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": AFTER["pending"], "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": remaining_groups[0]["group"], "pendingCount": remaining_groups[0]["pendingCount"], "archive": remaining_groups[0]["archive"], "freshPacketRequiredForCurrentAuthority": True, "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"},
        "packetStatus": "INFORMATION_TIME4_RETURN162_APPLIED_730_118",
    })
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(handoff_before)
    handoff.update({
        "id": "CURRENT-HANDOFF-164",
        "recordedAtUtc": now(),
        "status": "INFORMATION_TIME4_APPLIED_NEXT_118_PENDING",
        "currentAuthority": authority,
        "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "currentQueueBinding": binding(QUEUE_AFTER),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": AFTER["pending"], "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": len(IDS), "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}", "directorAcceptance": f"{AUDIT.relative_to(ROOT).as_posix()}/{ACCEPTANCE.name}"},
        "nextGroup": remaining_groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed16/72, the 335 closed feat identities, or accepted/applied spell cohorts. Runtime, source, access, content, geometry, information, control, cosmology and release holds remain separate and active.",
        "resumePriority": "Prepare and submit a fresh Rank8 Planar5 source packet bound to current 730/118 authority, submit it to the same GPT director, independently audit the exact return, apply only exact accepted IDs, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": remaining_groups[0]["group"], "candidate": remaining_groups[0]["candidate"], "historicalArchive": remaining_groups[0]["archive"], "freshPacketRequiredForCurrentAuthority": True, "request": "Build a fresh source packet and archive bound to current 730/118 authority before director review."},
    })
    write_json(HANDOFF_AFTER, handoff)

    validation = {
        "id": "INFORMATION-TIME4-APPLICATION-VALIDATION-164",
        "status": "PASS",
        "checksPassed": 39,
        "checksFailed": 0,
        "checks": [
            "Exact Return162 ZIP and all 96 unique members, CRCs and per-member hashes verified",
            "Conference03 controlling archive hash, corrected provenance and prior Packet163 13-check verification match",
            "Director accepted exactly four pending identities; applied=false and canonicalFilesEdited=false at decision",
            "All four returned native cards and class-access rows equal the unchanged live catalog",
            "All 17 conference questions, four original identity questions, seven future obligations, 56 cases and sixteen retained holds are present",
            "All 246 events have 984 forward/inverse operations; twenty dependent cases remain wholly held",
            "Only four accepted index entries and aggregate counts/envelope reference changed; inverse replay restores exact previous index object",
            "Authored counts advance to 730 reviewed / 118 pending / 0 accepted-unapplied; complete standalone procedures advance to 454",
            "All 118 pending identities remain present in unchanged native source catalog",
            "Native catalog bytes, original source status, class access rows and closed cohorts remain unchanged",
            "All sixteen hold categories remain; runtime selection is disabled and no runtime, human-play, balance, cosmology, domain-closure or release approval is added",
            "Fresh next group is Rank8 Planar5 and requires a new packet against 730/118 authority",
        ],
        "beforeIndex": binding(BACKUP),
        "afterIndex": binding(INDEX),
        "changedIdentityIds": IDS,
        "onlyFourPendingEntriesChanged": True,
        "authoredCounts": after["authoredCounts"],
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "sourceStatusStillBlockedForAllFour": True,
        "runtimeSelectionEnabled": False,
        "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before,
        "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all96ReturnMembersVerified": True,
        "acceptedUnapplied": 0,
        "nextGroup": remaining_groups[0]["group"],
        "nextPendingCount": AFTER["pending"],
        "applicationReceipt": binding(APPLICATION),
        "directorAcceptanceReceipt": binding(ACCEPTANCE),
    }
    write_json(VALIDATION, validation)

    old_start = START.read_text(encoding="utf-8-sig") if START.exists() else ""
    marker = "**Prior checkpoint: ["
    marker_at = old_start.find(marker)
    historic = old_start[marker_at:] if marker_at >= 0 else ""
    START.write_text(
        "# Active ordinary spell review164 — Calibration review part6\n\n"
        "Information/Time4 Return162 was GPT director accepted, independently audited, and applied to exactly four identities: **730 reviewed / 118 pending / 0 accepted-unapplied**. "
        "The return passed 14,095 director checks and a local exact archive/source audit. Its 16 hold categories and 20 whole-dependent-case holds remain; runtime, human-play, balance, cosmology, domain closure and release approval remain separate.\n\n"
        f"Continue with **{remaining_groups[0]['group']}**, preparing a fresh packet against 730/118 authority. Apply only exact accepted IDs, continuing until all pending ordinary spell identities are resolved. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[the 118-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n\n" + historic,
        encoding="utf-8", newline="\n",
    )
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Information/Time4 Return162\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **730 reviewed / 118 pending / 0 accepted-unapplied**. GPT accepted and this application records four exact Rank8 Information/Time4 procedures: Alignment Revelation (Mass), Moment of Prescience, Telepathy and Time Echo.\n\n"
        f"The Return162 ZIP is {len(archive_bytes):,} bytes with SHA-256 `{sha(archive_bytes)}`. The director reports 14,095 static checks and no acceptance blockers; independent local verification checked all 96 return members and the byte-exact corrected Conference03 source archive.\n\n"
        "All 16 hold categories and 20 wholly dependent cases remain. Native catalog and class access rows are unchanged; the four authored procedures remain blocked from runtime selection. This review gives no runtime, human-play, balance, cosmology, domain-closure or release approval. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"The next pending group is {remaining_groups[0]['group']} and requires a fresh packet against 730/118 authority. Continue until the pending identity count reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{ACCEPTANCE.name}), "
        f"[application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8", newline="\n",
    )

    assert CATALOG.read_bytes() == catalog_bytes
    current = read_json(INDEX)
    assert current["authoredCounts"] == {"reviewed": 730, "pending": 118}
    assert len(pending_after) == 118
    print(json.dumps({
        "status": "APPLIED_AND_VALIDATED",
        "acceptedIds": IDS,
        "authority": authority,
        "nextGroup": remaining_groups[0]["group"],
        "nextPendingCount": 118,
        "returnArchive": binding(RETURN_ZIP),
        "sourceCatalogUnchanged": True,
        "indexSha256": sha(INDEX.read_bytes()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = load_inputs()
        print(json.dumps({
            "status": "PREFLIGHT_PASS",
            "acceptedIds": IDS,
            "authorityBefore": {**BEFORE, "scopedInterfaces": 173, "completeReviewedStandaloneProcedures": COMPLETE_BEFORE},
            "authorityAfter": {**AFTER, "scopedInterfaces": 173, "completeReviewedStandaloneProcedures": COMPLETE_AFTER},
            "nextGroupAfterApply": "rank8-planar5",
            "returnBytes": RETURN_ZIP.stat().st_size,
            "candidateOutputAbsent": not CANDIDATE.exists(),
            "catalogUnchanged": True,
        }, ensure_ascii=False, indent=2))
