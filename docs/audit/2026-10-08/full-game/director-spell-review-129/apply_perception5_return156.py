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

from verify_perception5_return156 import (
    ARCHIVE, AUDIT, CATALOG, DELIVERY, HANDOFF, IDS, INDEX, PENDING, QUEUE, RECEIVED,
    SOURCE_ARCHIVE, SOURCE_CANDIDATE, EXPECTED_AUTHORITY, read_json, verify,
)

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_158.json"
PENDING_AFTER = AUDIT / "CURRENT125_PENDING_IDENTITY_AUDIT_158.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_158.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_PERCEPTION5_156.json"
RECEIPT = AUDIT / "PERCEPTION5_EXACT_ACCEPTANCE_156.json"
APPLICATION = AUDIT / "PERCEPTION5_APPLICATION_158.json"
OPERATIONS = AUDIT / "PERCEPTION5_INDEX_OPERATIONS_158.json"
VALIDATION = AUDIT / "PERCEPTION5_APPLICATION_VALIDATION_158.json"
BACKUP = AUDIT / "authored_review_index.before_perception5_158.json"
VERIFICATION = AUDIT / "PERCEPTION5_RETURN156_INDEPENDENT_VERIFICATION.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8perception5_reviewed_156"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_PERCEPTION5_REVIEWED_156.md"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_158.md"
REVIEW_ID = "RANK8-PERCEPTION5-EXACT-AUTHORED-ACCEPTANCE-156"
APP_ID = "RANK8-PERCEPTION5-APPLICATION-158"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def binding(path: Path, rel: str | None = None, raw: bytes | None = None) -> dict:
    content = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(content), "sha256": sha(content)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_return() -> dict:
    audit = verify()
    assert audit["status"] == "PASS" and audit["failures"] == 0
    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    with ZipFile(ARCHIVE) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    model = json.loads(members["MODEL.json"])
    decision = json.loads(members["DIRECTOR_DECISION.json"])
    coverage = json.loads(members["COVERAGE.json"])
    casebook = json.loads(members["CASEBOOK.json"])
    manifest = json.loads(members["MANIFEST.json"])
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE)
    handoff = read_json(HANDOFF)
    pending_before = read_json(PENDING)
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 718, "pending": 130}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 442
    assert queue["currentAuthority"]["reviewedApplied"] == 718 and queue["currentAuthority"]["pending"] == 130
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert pending_before["indexBinding"]["sha256"] == sha(before_bytes)
    assert set(IDS) <= live_pending and len(live_pending) == 130
    outputs = [QUEUE_AFTER, PENDING_AFTER, HANDOFF_AFTER, DECISION, RECEIPT, APPLICATION, OPERATIONS, VALIDATION, BACKUP, CANDIDATE, STAGING, MANUSCRIPT, SNAPSHOT]
    assert not [str(path) for path in outputs if path.exists()], "An application output exists already; inspect before retrying."
    assert VERIFICATION.exists() and read_json(VERIFICATION)["status"] == "PASS"
    assert CATALOG.read_bytes() == catalog_bytes
    assert not CANDIDATE.is_symlink() and not STAGING.is_symlink()
    return {
        "audit": audit, "archiveBytes": archive_bytes, "deliveryBytes": delivery_bytes, "members": members,
        "model": model, "decision": decision, "coverage": coverage, "casebook": casebook,
        "archiveManifest": manifest, "beforeBytes": before_bytes, "catalogBytes": catalog_bytes,
        "before": before, "catalog": catalog, "queue": queue, "handoff": handoff,
        "pendingBefore": pending_before, "pendingIds": live_pending,
    }


def apply() -> None:
    data = load_return()
    ts = now()
    archive_bytes = data["archiveBytes"]
    delivery_bytes = data["deliveryBytes"]
    before_bytes = data["beforeBytes"]
    catalog_bytes = data["catalogBytes"]
    before = data["before"]
    queue = data["queue"]
    model = data["model"]
    counts = data["coverage"]["counts"]
    verification = data["audit"]
    members = data["members"]
    excluded_pending = sorted(data["pendingIds"] - set(IDS))
    source_archive_bytes = SOURCE_ARCHIVE.read_bytes()
    source_candidate_bytes = SOURCE_CANDIDATE.read_bytes()
    source_candidate = json.loads(source_candidate_bytes.decode("utf-8-sig"))
    next_authority = {"reviewed": 723, "pending": 125}

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-PERCEPTION5-156",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": "Perception5-Director-Return156",
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "rejectedIds": [],
        "remainingBlockingDefects": [],
        "verification": {
            "directorStaticChecksPassed": 18_889,
            "directorStaticFailures": 0,
            "independentReturnAudit": verification,
            "archiveMembers": 98,
            "sourceBindings": 96,
            "acceptedInterfaceBoundaries": 31,
            "exactComparisonSnapshots": 19,
            "cases": 68,
            "events": 186,
            "eventOperations": 744,
            "proposalOperations": 20,
            "retainedHolds": 14,
            "wholeCaseHolds": 31,
        },
        "acceptedArchive": {"name": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "sourceArchive": {"name": SOURCE_ARCHIVE.name, "bytes": len(source_archive_bytes), "sha256": sha(source_archive_bytes)},
        "scope": data["decision"]["scope"],
        "holdScope": "All 14 source, access, accepted-scope, physical-geometry, hostility-identity-content, equipment-weapon, information-private, control-life, suppression, agency, cosmology, runtime-human-play, balance, release-closure and inherited hold categories remain active. All 31 held dependent cases remain held. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
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
        "directorReturnDelivery": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN_DELIVERY.json", "bytes": len(delivery_bytes), "sha256": sha(delivery_bytes)},
        "acceptedIds": IDS,
        "countsBefore": {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0},
        "countsAfter": {"reviewed": 723, "pending": 125, "acceptedUnapplied": 0},
        "completeReviewedStandaloneProceduresBefore": 442,
        "completeReviewedStandaloneProceduresAfter": 447,
        "acceptedCases": counts["totalCases"],
        "acceptedMainCases": counts["requiredMainCases"],
        "acceptedBranches": counts["additionalBranches"],
        "heldDependentCases": counts["wholeCaseHeld"],
        "acceptedEvents": counts["events"],
        "eventOperations": counts["eventOperations"],
        "retainedHolds": counts["retainedHoldCategories"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all five identities; authored procedure review only.",
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
    director_dir.mkdir()
    with ZipFile(ARCHIVE) as archive:
        for name in archive.namelist():
            if "/" not in name and name != "CASEBOOK.json":
                (director_dir / name).write_bytes(archive.read(name))
            elif name.startswith("procedures/") and name.endswith(".json"):
                target = director_dir / "PROCEDURES" / PurePosixPath(name).name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
    casebook_bytes = members["CASEBOOK.json"]
    casebook_gz = STAGING / "CASEBOOK.json.gz"
    with casebook_gz.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
            compressed.write(casebook_bytes)
    assert gzip.decompress(casebook_gz.read_bytes()) == casebook_bytes
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "DIRECTOR_RETURN_DELIVERY.json").write_bytes(delivery_bytes)
    (STAGING / "GPT_DIRECTOR_DECISION.json").write_bytes(decision_bytes)
    (STAGING / "EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    (STAGING / "INDEPENDENT_VERIFICATION.json").write_bytes(json_bytes(verification))
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(source_archive_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_bytes)
    (STAGING / "SOURCE_CONFERENCE_REQUEST.txt").write_bytes((FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_REQUEST.txt").read_bytes())
    (STAGING / "SOURCE_CONFERENCE_CHECK.json").write_bytes((FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_CHECK.json").read_bytes())
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
    normalized_model = {
        "schemaVersion": 1,
        "moduleId": "rank8perception5-reviewed-156",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly the five GPT-accepted Perception5 static authored procedures. Native spell cards, catalog rows, class access and source status remain unchanged. All 14 hold categories and all 31 held dependent cases remain. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Per-spell common rules are preserved in each full director procedure record; no global interface is changed.", "perSpellCommon": {sid: copy.deepcopy(model["spells"][sid]["common"]) for sid in IDS}},
        "spells": procedure_rows,
        "questionDispositions": json.loads(members["QUESTION_DISPOSITIONS.json"]),
        "originalIdentityDispositions": model["originalIdentityDispositions"],
        "futureObligationDispositions": model["futureObligationDispositions"],
        "returnCounts": counts,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; exact decompression reproduces the director-return CASEBOOK.json member",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(casebook_bytes), "sha256": sha(casebook_bytes)},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip",
        "directorReturnDelivery": "DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip",
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "GPT_DIRECTOR_DECISION.json",
        "directorReturnBinding": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "archiveMemberCount": 98,
        "independentAcceptanceGranted": True,
        "canonicalApplicationPerformed": False,
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
        "id": "RANK8-PERCEPTION5-CANDIDATE-PACKAGE-MANIFEST-158",
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

    app = {
        "id": APP_ID,
        "recordedAtUtc": now(),
        "status": "APPLIED_FIVE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue through all remaining pending ordinary-spell identities.",
        "acceptedIds": IDS,
        "directorAcceptance": binding(RECEIPT),
        "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "directorReturnDelivery": binding(DELIVERY, f"{RECEIVED.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN_DELIVERY.json", delivery_bytes),
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0}, "after": {"reviewed": 723, "pending": 125, "acceptedUnapplied": 0}},
        "completeReviewedStandaloneProcedures": {"before": 442, "after": 447},
        "cases": counts["totalCases"],
        "completeStaticFixtures": counts["totalCases"] - counts["wholeCaseHeld"],
        "wholeCaseHeld": counts["wholeCaseHeld"],
        "events": counts["events"],
        "eventOperations": counts["eventOperations"],
        "retainedHolds": counts["retainedHoldCategories"],
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
        index = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index]
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank8perception5_reviewed_156/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRules/perSpellCommon",
            "manuscript": "../../../docs/spells/candidates/RANK8_PERCEPTION5_REVIEWED_156.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces the director-return CASEBOOK.json member",
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
        operations.append({"op": "replace-entry", "identity": sid, "index": index, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][index] = new
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank8perception5_reviewed_156/MODEL.json",
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
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 447
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 5 and len(pending_after) == 125 and pending_after == data["pendingIds"] - set(IDS)
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    write_json(BACKUP, json.loads(before_bytes.decode("utf-8-sig")))
    # Preserve the exact pre-application bytes in the backup, including any BOM/formatting.
    BACKUP.write_bytes(before_bytes)
    ops_doc = {
        "id": "PERCEPTION5-INDEX-OPERATIONS-158",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "five prior entries, aggregate authored counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    write_json(OPERATIONS, ops_doc)
    write_json(APPLICATION, app)
    temp_index = INDEX.with_suffix(".json.application158.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = copy.deepcopy(queue["currentAuthority"])
    authority.update({"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 447})
    groups = []
    for group in queue["currentPendingGroups"]:
        remaining = [sid for sid in group["pendingIds"] if sid in pending_after]
        if remaining:
            row = copy.deepcopy(group)
            row["pendingIds"] = remaining
            row["pendingCount"] = len(remaining)
            row["freshPacketRequiredForCurrentAuthority"] = True
            groups.append(row)
    assert groups[0]["group"] == "rank8-environment3" and sum(group["pendingCount"] for group in groups) == 125
    pending_doc = {
        "id": "CURRENT125-PENDING-IDENTITY-AUDIT-158",
        "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": binding(INDEX),
        "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"],
        "pendingCount": 125,
        "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in data["catalog"]["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False,
        "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)
    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-158",
        "recordedAtUtc": now(),
        "currentAuthority": authority,
        "currentPendingGroups": groups,
        "nextSuggestedGroups": groups[:5],
        "nextGroup": groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 5, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 125, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "archive": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True},
    })
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(data["handoff"])
    handoff.update({
        "id": "CURRENT-HANDOFF-158",
        "recordedAtUtc": now(),
        "status": "RANK8_PERCEPTION5_APPLIED_NEXT_125_PENDING",
        "currentAuthority": authority,
        "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "currentQueueBinding": binding(QUEUE_AFTER),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 125, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 5, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}", "directorAcceptance": f"{AUDIT.relative_to(ROOT).as_posix()}/{RECEIPT.name}"},
        "nextGroup": groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed16/72, feat335 or any accepted/applied spell cohort. Runtime, source, access, content, geometry, information, control, cosmology and release holds remain separate and active.",
        "director": {"title": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "role": "source/procedure authoring director; each return remains proposed until independently audited and exact accepted IDs applied"},
        "resumePriority": "Prepare a fresh Rank8 Environment3 source packet against 723/125 authority, submit to the same GPT director, audit its exact return and apply only accepted IDs; continue until pending reaches zero.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True, "request": "Prepare and submit a fresh request bound to current 723/125 authority before director review."},
    })
    handoff["currentAuthority"] = authority
    write_json(HANDOFF_AFTER, handoff)

    write_json(VALIDATION, {
        "id": "PERCEPTION5-APPLICATION-VALIDATION-158",
        "status": "PASS",
        "checksPassed": 37,
        "checksFailed": 0,
        "checks": [
            "Exact Return156 and delivery hashes matched the accepted manifest; all 98 members and 97 listed member SHA256/CRC bindings verified",
            "Independent Return156 audit passed all 18,889 director checks with no blockers",
            "Current source conference was independently reverified against 96 live source files at 718/130",
            "All five exact accepted IDs were first pending identities and no rejected or nonaccepted identity changed",
            "All five director procedures are byte-bound, source-faithful to the current native catalog cards, and exact to the bound procedure members",
            "All 23 conference dispositions, five original identity dispositions, seven future obligations, and 14 retained hold definitions were preserved",
            "31 dependent cases remain held; no held case is marked actual campaign success",
            "All 68 case records, 186 full-state events, 744 forward/inverse operations, and 20 isolated proposal operations replayed exactly",
            "Only five pending-authored index entries and the three aggregate review counters changed; inverse semantic replay restores the exact prior index",
            "Authored counts advance to 723 reviewed / 125 pending / 0 accepted-unapplied and standalone procedures to 447",
            "All 125 pending identities remain present in the native source catalog",
            "Catalog bytes, native spell rows, current source access and spell source status remain unchanged",
            "All 14 hold categories, historical acceptance boundaries and exact closed cohorts remain unchanged",
            "Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is added",
            "Next pending group is Rank8 Environment3 and requires a fresh packet bound to 723/125",
        ],
        "beforeIndex": binding(BACKUP),
        "afterIndex": binding(INDEX),
        "changedIdentityIds": IDS,
        "onlyFivePendingEntriesChanged": True,
        "authoredCounts": after["authoredCounts"],
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "sourceStatusStillBlockedForAllFive": True,
        "runtimeSelectionEnabled": False,
        "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before,
        "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all98ReturnMembersVerified": True,
        "acceptedUnapplied": 0,
        "nextGroup": groups[0]["group"],
        "nextPendingCount": 125,
        "applicationReceipt": binding(APPLICATION),
        "directorAcceptanceReceipt": binding(RECEIPT),
    })

    old_start = START.read_text(encoding="utf-8-sig")
    marker = "**Prior checkpoint: ["
    marker_at = old_start.find(marker)
    historic = old_start[marker_at:] if marker_at >= 0 else ""
    START.write_text(
        "# Active ordinary spell review158 — Calibration review part6\n\n"
        "Perception5 Return156 was GPT director accepted, independently verified, and applied to five exact identities: **723 reviewed / 125 pending / 0 accepted-unapplied**. "
        "The return passed 18,889 static checks; independent verification replayed 68 cases, 186 events, 744 forward/inverse operations and 20 isolated proposal operations. "
        "All 14 hold categories and 31 held dependent cases remain. Runtime, human-play, balance, cosmology, domain closure and release approval remain separate.\n\n"
        f"Continue with **{groups[0]['group']}**, preparing a fresh packet against 723/125 authority and submitting it to GPT for exact director review. Apply only exact accepted IDs, continuing until all pending ordinary spell identities are resolved. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[the 125-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [snapshot status]({SNAPSHOT.name}).\n\n" + historic,
        encoding="utf-8", newline="\n",
    )
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Perception5 Return156\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **723 reviewed / 125 pending / 0 accepted-unapplied**. GPT accepted and this application records five exact Rank8 Perception5 procedures: Mass Hallucination, Illusory Dragon, Phantom Execution, Antipathy/Sympathy, and Glibness.\n\n"
        "The Return156 ZIP is 15,465,602 bytes with SHA-256 `1726d1b99a17643e358e459104162965260949aa1f032cb71a7c9c15accf3d68`. Independent verification passed all 98 archive members, 96 live source bindings, 31 accepted-interface boundaries, 19 exact comparison snapshots, 23 conference questions, 68 cases, 186 events, 744 forward/inverse operations, and 20 isolated proposal operations.\n\n"
        "All 14 hold categories and 31 held dependent cases remain. Native catalog and spell access rows remain unchanged; the five authored procedures remain blocked from runtime selection. This review gives no runtime, human-play, balance, cosmology, domain-closure, or release approval. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"The next pending group is {groups[0]['group']} and requires a fresh packet against 723/125 authority. Continue until the pending identity count reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}), "
        f"[application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [independent return verification](docs/audit/2026-10-08/full-game/director-spell-review-129/{VERIFICATION.name}).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    current = read_json(INDEX)
    assert current["authoredCounts"] == next_authority
    assert len({row["id"] for row in current["entries"] if row["authoredStatus"] == "pending-authored-procedure"}) == 125
    print(json.dumps({
        "status": "APPLIED_AND_VALIDATED",
        "acceptedIds": IDS,
        "authority": authority,
        "nextGroup": groups[0]["group"],
        "nextPendingCount": 125,
        "independentReturnVerification": verification,
        "indexSha256": sha(INDEX.read_bytes()),
        "catalogUnchanged": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = load_return()
        print(json.dumps({
            "status": "PREFLIGHT_PASS",
            "acceptedIds": IDS,
            "authority": data["audit"]["inputAuthority"],
            "nextGroupAfterApply": data["queue"]["currentPendingGroups"][1]["group"],
            "archiveBytes": len(data["archiveBytes"]),
            "candidateOutputAbsent": not CANDIDATE.exists(),
            "catalogUnchanged": True,
        }, ensure_ascii=False, indent=2))
