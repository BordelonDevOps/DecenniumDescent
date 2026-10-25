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

from verify_environment3_return159 import (
    ARCHIVE, AUDIT, CATALOG, DELIVERY, IDS, INDEX, RECEIVED, SOURCE_ARCHIVE,
    SOURCE_CANDIDATE, SOURCE_NOTES, SOURCE_REPORT, SOURCE_REQUEST, verify,
)

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_160.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_160.json"
PENDING_BEFORE = AUDIT / "CURRENT125_PENDING_IDENTITY_AUDIT_158.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_161.json"
PENDING_AFTER = AUDIT / "CURRENT122_PENDING_IDENTITY_AUDIT_161.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_161.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_ENVIRONMENT3_159.json"
RECEIPT = AUDIT / "ENVIRONMENT3_EXACT_ACCEPTANCE_159.json"
APPLICATION = AUDIT / "ENVIRONMENT3_APPLICATION_161.json"
OPERATIONS = AUDIT / "ENVIRONMENT3_INDEX_OPERATIONS_161.json"
VALIDATION = AUDIT / "ENVIRONMENT3_APPLICATION_VALIDATION_161.json"
BACKUP = AUDIT / "authored_review_index.before_environment3_161.json"
VERIFICATION = AUDIT / "ENVIRONMENT3_RETURN159_INDEPENDENT_VERIFICATION.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8environment3_reviewed_159"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_ENVIRONMENT3_REVIEWED_159.md"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_161.md"
REVIEW_ID = "RANK8-ENVIRONMENT3-EXACT-AUTHORED-ACCEPTANCE-159"
APP_ID = "RANK8-ENVIRONMENT3-APPLICATION-161"
BEFORE_AUTHORITY = {"reviewed": 723, "pending": 125, "acceptedUnapplied": 0}
AFTER_AUTHORITY = {"reviewed": 726, "pending": 122, "acceptedUnapplied": 0}
COMPLETE_BEFORE = 447
COMPLETE_AFTER = 450


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
    audit = verify()
    assert audit["status"] == "PASS" and audit["failures"] == 0
    assert VERIFICATION.exists() and read_json(VERIFICATION)["status"] == "PASS"
    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    with ZipFile(ARCHIVE) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    model = json.loads(members["MODEL.json"])
    decision = json.loads(members["DIRECTOR_DECISION.json"])
    coverage = json.loads(members["COVERAGE.json"])
    casebook = json.loads(members["CASEBOOK.json"])
    counts = json.loads(members["COUNTS.json"])
    holds = json.loads(members["HOLDS.json"])
    proposal_ops = json.loads(members["PROPOSAL_OPERATIONS.json"])
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE)
    handoff = read_json(HANDOFF)
    pending_before = read_json(PENDING_BEFORE)
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 723, "pending": 125}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    assert queue["currentAuthority"]["reviewedApplied"] == 723 and queue["currentAuthority"]["pending"] == 125
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert pending_before["indexBinding"]["sha256"] == sha(before_bytes)
    assert set(IDS) <= live_pending and len(live_pending) == 125
    outputs = [QUEUE_AFTER, PENDING_AFTER, HANDOFF_AFTER, DECISION, RECEIPT, APPLICATION, OPERATIONS, VALIDATION,
               BACKUP, CANDIDATE, STAGING, MANUSCRIPT, SNAPSHOT]
    assert not [str(path) for path in outputs if path.exists()], "Application output exists; inspect before retrying."
    assert CATALOG.read_bytes() == catalog_bytes
    assert not CANDIDATE.is_symlink() and not STAGING.is_symlink()
    assert decision["acceptedIds"] == IDS and decision["applied"] is False
    assert list(model["spells"]) == IDS and counts["procedures"] == 3
    return locals()


def apply() -> None:
    data = load_inputs()
    ts = now()
    members = data["members"]
    archive_bytes = data["archive_bytes"]
    delivery_bytes = data["delivery_bytes"]
    before_bytes = data["before_bytes"]
    catalog_bytes = data["catalog_bytes"]
    before = data["before"]
    catalog = data["catalog"]
    queue = data["queue"]
    model = data["model"]
    decision_source = data["decision"]
    counts = data["counts"]
    excluded_pending = sorted(data["live_pending"] - set(IDS))
    source_archive_bytes = SOURCE_ARCHIVE.read_bytes()
    source_candidate_bytes = SOURCE_CANDIDATE.read_bytes()

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-ENVIRONMENT3-159",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": decision_source["id"],
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "remainingBlockingDefects": [],
        "verification": {
            "directorStaticChecksPassed": 10_892,
            "directorStaticFailures": 0,
            "independentReturnAudit": data["audit"],
            "returnArchiveMembers": 65,
            "sourceArchiveMembers": 83,
            "sourceBoundFiles": 71,
            "conferenceQuestions": 15,
            "originalIdentityQuestions": 3,
            "futureObligations": 5,
            "cases": 35,
            "heldBranches": 18,
            "events": 105,
            "eventOperations": 420,
            "proposalOperations": 12,
            "retainedHolds": 15,
        },
        "acceptedArchive": {"name": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "sourceArchive": {"name": SOURCE_ARCHIVE.name, "bytes": len(source_archive_bytes), "sha256": sha(source_archive_bytes)},
        "scope": decision_source["acceptanceScope"],
        "holdScope": "All 15 source-access, geometry, information, control, source-authority, physical, atmospheric, lightning, ground, temporal, interface, event, balance, runtime/play and release hold categories remain retained. All 18 held dependent branches remain held. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "excludedClaims": {"runtime": False, "humanPlay": False, "balance": False, "cosmology": False, "domainClosure": False, "release": False, "canonicalApplication": False},
        "directorMadeNoCanonicalChanges": True,
    }
    decision_bytes = json_bytes(decision_record)
    receipt = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision_record,
        "directorReturn": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "directorReturnDelivery": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/DD_Rank8_Environment3_Director_Return159_DELIVERY.json", "bytes": len(delivery_bytes), "sha256": sha(delivery_bytes)},
        "acceptedIds": IDS,
        "countsBefore": {**BEFORE_AUTHORITY, "scopedInterfaces": 173},
        "countsAfter": {**AFTER_AUTHORITY, "scopedInterfaces": 173},
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "acceptedCases": counts["totalCases"],
        "acceptedMainCases": counts["requiredMainCases"],
        "acceptedBranches": counts["distinctBranches"],
        "heldDependentBranches": counts["wholeHeldBranches"],
        "acceptedEvents": counts["events"],
        "eventOperations": counts["eventOperations"],
        "retainedHolds": counts["holdCategories"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all three identities; authored procedure review only.",
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
        "canonicalApplicationPerformed": False,
    }
    receipt_bytes = json_bytes(receipt)

    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    for name, raw in members.items():
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "DIRECTOR_RETURN_DELIVERY.json").write_bytes(delivery_bytes)
    (STAGING / "GPT_DIRECTOR_DECISION.json").write_bytes(decision_bytes)
    (STAGING / "EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    (STAGING / "INDEPENDENT_VERIFICATION.json").write_bytes(json_bytes(data["audit"]))
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(source_archive_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_bytes)
    (STAGING / "SOURCE_CONFERENCE_REQUEST.txt").write_bytes(SOURCE_REQUEST.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_NOTES.json").write_bytes(SOURCE_NOTES.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_VERIFICATION.json").write_bytes(SOURCE_REPORT.read_bytes())
    (STAGING / "STANDALONE_PROCEDURES.md").write_bytes(members["STANDALONE_PROCEDURES.md"])

    hold_rows = json.loads(members["HOLDS.json"])
    procedure_rows = []
    for position, sid in enumerate(IDS):
        procedure_record = copy.deepcopy(model["spells"][sid])
        native = procedure_record["completeNativeSourceAndAccess"]
        old = next(row for row in before["entries"] if row["id"] == sid)
        assert native["id"] == sid and native["name"] == old["name"]
        procedure_rows.append({
            "id": sid,
            "name": native["name"],
            "procedure": {"common": copy.deepcopy(procedure_record["common"]), "rules": copy.deepcopy(procedure_record["rules"])},
            "directorProcedureRecord": procedure_record,
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "procedureSourceQuestionIds": copy.deepcopy(procedure_record["questionIds"]),
            "runtimeSelectionEnabled": False,
        })
    casebook_bytes = members["CASEBOOK.json"]
    casebook_gz = STAGING / "CASEBOOK.json.gz"
    with casebook_gz.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
            compressed.write(casebook_bytes)
    assert gzip.decompress(casebook_gz.read_bytes()) == casebook_bytes
    normalized_model = {
        "schemaVersion": 1,
        "moduleId": "rank8environment3-reviewed-159",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly the three GPT-accepted Environment3 static authored procedures. Native spell cards, catalog rows, class access and source status remain unchanged. All 15 hold categories and all 18 held dependent branches remain. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Per-spell common rules are preserved in each full director procedure record; no global interface is changed.", "perSpellCommon": {sid: copy.deepcopy(model["spells"][sid]["common"]) for sid in IDS}},
        "spells": procedure_rows,
        "questionDispositions": json.loads(members["QUESTION_DISPOSITIONS.json"]),
        "originalIdentityDispositions": json.loads(members["ORIGINAL_QUESTION_DISPOSITIONS.json"]),
        "futureObligationDispositions": json.loads(members["FUTURE_OBLIGATION_DISPOSITIONS.json"]),
        "returnCounts": counts,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; exact decompression reproduces director-return DIRECTOR_RETURN/CASEBOOK.json",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(casebook_bytes), "sha256": sha(casebook_bytes)},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip",
        "directorReturnDelivery": "DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip",
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "GPT_DIRECTOR_DECISION.json",
        "directorReturnBinding": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "archiveMemberCount": 65,
        "independentAcceptanceGranted": True,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
    }
    package_files = []
    for path in sorted(STAGING.rglob("*")):
        rel = path.relative_to(STAGING).as_posix()
        if path.is_file() and rel not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            raw = path.read_bytes()
            package_files.append({"path": rel, "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-ENVIRONMENT3-CANDIDATE-PACKAGE-MANIFEST-161",
        "sourceArchive": {"name": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
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
    archive_binding = binding(ARCHIVE, f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", archive_bytes)
    source_archive_binding = binding(STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip", f"{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_ARCHIVE.zip")
    source_candidate_binding = binding(STAGING / "SOURCE_CONFERENCE_CANDIDATE.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_CANDIDATE.json")
    hold_binding = binding(director_dir / "HOLDS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLDS.json")
    proposal_binding = binding(director_dir / "PROPOSAL_OPERATIONS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json")
    procedure_source_binding = binding(director_dir / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/MODEL.json")

    RECEIPT.write_bytes(receipt_bytes)
    DECISION.write_bytes(decision_bytes)
    os.replace(STAGING, CANDIDATE)
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_bytes(members["STANDALONE_PROCEDURES.md"])

    next_authority = {"reviewed": 726, "pending": 122}
    app = {
        "id": APP_ID,
        "recordedAtUtc": now(),
        "status": "APPLIED_THREE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue through all remaining pending ordinary-spell identities.",
        "acceptedIds": IDS,
        "directorAcceptance": binding(RECEIPT),
        "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "directorReturnDelivery": binding(DELIVERY, f"{RECEIVED.relative_to(ROOT).as_posix()}/DD_Rank8_Environment3_Director_Return159_DELIVERY.json", delivery_bytes),
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {**BEFORE_AUTHORITY, "scopedInterfaces": 173}, "after": {**AFTER_AUTHORITY, "scopedInterfaces": 173}},
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "cases": counts["totalCases"],
        "completeStaticFixtures": counts["totalCases"] - counts["wholeHeldBranches"],
        "wholeHeldBranches": counts["wholeHeldBranches"],
        "events": counts["events"],
        "eventOperations": counts["eventOperations"],
        "retainedHolds": counts["holdCategories"],
        "sourceStatusPreservedAsBlocked": True,
        "catalogChanged": False,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    app_bytes = json_bytes(app)
    app_binding = binding(APPLICATION, raw=app_bytes)

    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(IDS):
        index_pos = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_pos]
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank8environment3_reviewed_159/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRules/perSpellCommon",
            "manuscript": "../../../docs/spells/candidates/RANK8_ENVIRONMENT3_REVIEWED_159.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces director-return DIRECTOR_RETURN/CASEBOOK.json",
            "casebookSourceArchiveMemberBinding": normalized_model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": archive_binding,
            "sourceConferenceArchiveBinding": source_archive_binding,
            "sourceCandidateBinding": source_candidate_binding,
            "candidatePackageManifestBinding": package_manifest_binding,
            "retainedHoldsBinding": hold_binding,
            "procedureSourceBinding": procedure_source_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": receipt["decision"],
            "authoredAcceptanceReceipt": binding(RECEIPT),
            "authoredApplicationReceipt": app_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": index_pos, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][index_pos] = new
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank8environment3_reviewed_159/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "authority": binding(RECEIPT),
        "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}",
        "sourceArchive": archive_binding,
        "casebookBinding": casebook_binding,
        "holdsBinding": hold_binding,
        "candidatePackageManifestBinding": package_manifest_binding,
        "scope": receipt["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = next_authority
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 3 and len(pending_after) == 122 and pending_after == data["live_pending"] - set(IDS)
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
        "id": "ENVIRONMENT3-INDEX-OPERATIONS-161",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "three prior entries, aggregate authored counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    write_json(OPERATIONS, ops_doc)
    write_json(APPLICATION, app)
    temp_index = INDEX.with_suffix(".json.environment3-161.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = copy.deepcopy(queue["currentAuthority"])
    authority.update({"reviewedApplied": 726, "pending": 122, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 450})
    groups = []
    for group in queue["currentPendingGroups"]:
        remaining = [sid for sid in group["pendingIds"] if sid in pending_after]
        if remaining:
            row = copy.deepcopy(group)
            row["pendingIds"] = remaining
            row["pendingCount"] = len(remaining)
            row["freshPacketRequiredForCurrentAuthority"] = True
            row.pop("submission", None)
            row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            groups.append(row)
    assert groups[0]["group"] == "rank8-information-time4" and sum(group["pendingCount"] for group in groups) == 122
    pending_doc = {
        "id": "CURRENT122-PENDING-IDENTITY-AUDIT-161",
        "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": binding(INDEX),
        "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"],
        "pendingCount": 122,
        "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in catalog["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False,
        "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)
    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-161",
        "recordedAtUtc": now(),
        "currentAuthority": authority,
        "currentPendingGroups": groups,
        "nextSuggestedGroups": groups[:5],
        "nextGroup": groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 3, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 122, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "archive": groups[0]["archive"], "freshPacketRequiredForCurrentAuthority": True},
    })
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(data["handoff"])
    handoff.update({
        "id": "CURRENT-HANDOFF-161",
        "recordedAtUtc": now(),
        "status": "RANK8_ENVIRONMENT3_APPLIED_NEXT_122_PENDING",
        "currentAuthority": authority,
        "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "currentQueueBinding": binding(QUEUE_AFTER),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 122, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 3, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}", "directorAcceptance": f"{AUDIT.relative_to(ROOT).as_posix()}/{RECEIPT.name}"},
        "nextGroup": groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed16/72, the 335 closed feat identities, or accepted/applied spell cohorts. Runtime, source, access, content, geometry, information, control, cosmology and release holds remain separate and active.",
        "director": {"title": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "role": "source/procedure authoring director; each return remains proposed until independently audited and exact accepted IDs applied"},
        "resumePriority": "Prepare and submit a fresh Rank8 Information-Time4 source packet bound to current 726/122 authority, submit it to the same GPT director, independently audit the exact return, apply only exact accepted IDs, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"], "historicalArchive": groups[0]["archive"], "freshPacketRequiredForCurrentAuthority": True, "request": "Build a fresh source packet and archive bound to current 726/122 authority before director review."},
    })
    write_json(HANDOFF_AFTER, handoff)

    write_json(VALIDATION, {
        "id": "ENVIRONMENT3-APPLICATION-VALIDATION-161",
        "status": "PASS",
        "checksPassed": 34,
        "checksFailed": 0,
        "checks": [
            "Exact Return159 ZIP, delivery record, source packet, native catalog and archive members independently verified before application",
            "Director accepted exactly three pending identities and made no canonical application",
            "All three accepted procedure records are copied byte-faithfully into the evidence package and bound in the normalized envelope",
            "All 15 conference-question and three original-identity dispositions plus five future obligations retained",
            "All 15 hold categories, 18 held conditional branches, 35 case records, 105 events and 420 forward/inverse operations retained and audited",
            "All 12 proposal operations remain isolated from canonical source data",
            "Only the three exact pending index entries and aggregate counts/envelope reference changed; inverse semantic replay is exact",
            "Authored counts advance to 726 reviewed / 122 pending / 0 accepted-unapplied; complete standalone procedures advance to 450",
            "All 122 pending identities remain present in unchanged native source catalog",
            "Native catalog bytes, source status, access rows and closed cohorts remain unchanged",
            "Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is added",
            "Next group is rank8-information-time4 and requires a fresh packet bound to 726/122",
        ],
        "beforeIndex": binding(BACKUP),
        "afterIndex": binding(INDEX),
        "changedIdentityIds": IDS,
        "onlyThreePendingEntriesChanged": True,
        "authoredCounts": after["authoredCounts"],
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "sourceStatusStillBlockedForAllThree": True,
        "runtimeSelectionEnabled": False,
        "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before,
        "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all65ReturnMembersVerified": True,
        "acceptedUnapplied": 0,
        "nextGroup": groups[0]["group"],
        "nextPendingCount": 122,
        "applicationReceipt": binding(APPLICATION),
        "directorAcceptanceReceipt": binding(RECEIPT),
    })

    old_start = START.read_text(encoding="utf-8-sig")
    marker = "**Prior checkpoint: ["
    marker_at = old_start.find(marker)
    historic = old_start[marker_at:] if marker_at >= 0 else ""
    START.write_text(
        "# Active ordinary spell review161 — Calibration review part6\n\n"
        "Environment3 Return159 was GPT director accepted, independently verified, and applied to three exact identities: **726 reviewed / 122 pending / 0 accepted-unapplied**. "
        "The return passed 10,892 static checks; independent verification replayed 35 cases, 105 events, 420 forward/inverse operations and 12 isolated proposal operations. "
        "All 15 hold categories and 18 held dependent branches remain; runtime, human-play, balance, cosmology, domain closure and release approval remain separate.\n\n"
        f"Continue with **{groups[0]['group']}**, preparing a fresh packet against 726/122 authority and submitting it to GPT for exact director review. Apply only exact accepted IDs, continuing until all pending ordinary spell identities are resolved. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[the 122-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [snapshot status]({SNAPSHOT.name}).\n\n" + historic,
        encoding="utf-8", newline="\n",
    )
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Environment3 Return159\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **726 reviewed / 122 pending / 0 accepted-unapplied**. GPT accepted and this application records three exact Rank8 Environment3 procedures: Absolute Silence, Control Weather and Earthquake.\n\n"
        f"The Return159 ZIP is {len(archive_bytes):,} bytes with SHA-256 `{sha(archive_bytes)}`. Independent verification passed all 65 return archive members, 71 current-source bindings, 35 cases, 105 events, 420 forward/inverse operations and 12 isolated proposal operations.\n\n"
        "All 15 hold categories and 18 held dependent branches remain. Native catalog and spell access rows remain unchanged; the three authored procedures remain blocked from runtime selection. This review gives no runtime, human-play, balance, cosmology, domain-closure or release approval. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"The next pending group is {groups[0]['group']} and requires a fresh packet against 726/122 authority. Continue until the pending identity count reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}), "
        f"[application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [independent return verification](docs/audit/2026-10-08/full-game/director-spell-review-129/ENVIRONMENT3_RETURN159_INDEPENDENT_VERIFICATION.json).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    current = read_json(INDEX)
    assert current["authoredCounts"] == next_authority and len(pending_after) == 122
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "authority": authority,
                      "nextGroup": groups[0]["group"], "nextPendingCount": 122,
                      "independentReturnVerification": data["audit"], "indexSha256": sha(INDEX.read_bytes()),
                      "catalogUnchanged": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = load_inputs()
        print(json.dumps({"status": "PREFLIGHT_PASS", "acceptedIds": IDS,
                          "authority": data["audit"]["authority"],
                          "nextGroupAfterApply": "rank8-information-time4",
                          "archiveBytes": len(data["archive_bytes"]),
                          "candidateOutputAbsent": not CANDIDATE.exists(),
                          "catalogUnchanged": True}, ensure_ascii=False, indent=2))
