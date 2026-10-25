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

from verify_summonstructure5_return153 import IDS, ROOT, AUDIT, RECEIVED, ARCHIVE, DELIVERY, INDEX, CATALOG, QUEUE, HANDOFF, PENDING, verify

FULL = ROOT / "docs/audit/2026-10-08/full-game"
SOURCE_ARCHIVE = FULL / "DD_Rank8_Summon_Structure_5_Source_Conference_02.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_summon_structure_5_source_conference_02.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_154.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_154.json"
PENDING_BEFORE = AUDIT / "CURRENT135_PENDING_IDENTITY_AUDIT_152.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_155.json"
PENDING_AFTER = AUDIT / "CURRENT130_PENDING_IDENTITY_AUDIT_155.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_155.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_SUMMON_STRUCTURE5_153.json"
RECEIPT = AUDIT / "SUMMON_STRUCTURE5_EXACT_ACCEPTANCE_153.json"
APPLICATION = AUDIT / "SUMMON_STRUCTURE5_APPLICATION_153.json"
OPERATIONS = AUDIT / "SUMMON_STRUCTURE5_INDEX_OPERATIONS_153.json"
VALIDATION = AUDIT / "SUMMON_STRUCTURE5_APPLICATION_VALIDATION_153.json"
BACKUP = AUDIT / "authored_review_index.before_summon_structure5_153.json"
VERIFICATION = AUDIT / "SUMMONSTRUCTURE5_RETURN153_INDEPENDENT_VERIFICATION.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8summonstructure5_reviewed_153"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_SUMMON_STRUCTURE5_REVIEWED_153.md"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_153.md"
REVIEW_ID = "RANK8-SUMMON-STRUCTURE5-EXACT-AUTHORED-ACCEPTANCE-153"
APP_ID = "RANK8-SUMMON-STRUCTURE5-APPLICATION-153"


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


def validate_input() -> dict:
    audit = verify()
    assert audit["status"] == "PASS" and audit["failures"] == 0
    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    with ZipFile(ARCHIVE) as archive:
        model = json.loads(archive.read("MODEL.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        dispositions = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        original_dispositions = json.loads(archive.read("ORIGINAL_QUESTION_DISPOSITIONS.json"))
        holds = json.loads(archive.read("HOLDS.json"))
        proposal_ops = json.loads(archive.read("PROPOSAL_OPERATIONS.json"))
        source_archive_bytes = archive.read("history/DD_Rank8_Summon_Structure_5_Source_Conference_02.zip")
        source_candidate_bytes = archive.read("evidence/source02/CANDIDATE.json")
        standalone_bytes = archive.read("STANDALONE_PROCEDURES.md")
        casebook_bytes = archive.read("CASEBOOK.json")
        member_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        casebook_member = next(row for row in member_manifest["members"] if row["path"] == "CASEBOOK.json")
        assert set(model["spells"]) == set(IDS) and len(IDS) == 5
        assert counts == delivery["counts"]
        assert len(dispositions) == 20 and len(original_dispositions) == 5 and len(holds) == 15
        assert len(proposal_ops) == 5 and decision["accepted"] and decision["applied"] is False
        for sid in IDS:
            assert model["spells"][sid]["nativeUnchanged"]["id"] == sid
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    assert before["authoredCounts"] == {"reviewed": 713, "pending": 135}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 437
    assert queue["currentAuthority"]["reviewedApplied"] == 713 and queue["currentAuthority"]["pending"] == 135
    assert queue["currentPendingGroups"][0]["group"] == "rank8-summon-structure5"
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert pending_before["indexBinding"]["sha256"] == sha(before_bytes)
    current_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(current_pending) == 135 and set(IDS) <= current_pending
    outputs = [QUEUE_AFTER, PENDING_AFTER, HANDOFF_AFTER, DECISION, RECEIPT, APPLICATION, OPERATIONS, VALIDATION, BACKUP, CANDIDATE, MANUSCRIPT, SNAPSHOT]
    assert not [str(path) for path in outputs if path.exists()], "An application output already exists; inspect before retrying."
    assert not STAGING.exists() or (STAGING.is_dir() and not STAGING.is_symlink()), "Unexpected staging path; inspect before retrying."
    assert CATALOG.read_bytes() == catalog_bytes
    return {
        "audit": audit, "archiveBytes": archive_bytes, "deliveryBytes": delivery_bytes,
        "sourceArchiveBytes": source_archive_bytes, "sourceCandidateBytes": source_candidate_bytes,
        "standaloneBytes": standalone_bytes, "casebookBytes": casebook_bytes, "casebookMember": casebook_member,
        "model": model, "counts": counts, "dispositions": dispositions,
        "originalDispositions": original_dispositions, "holds": holds, "proposalOps": proposal_ops,
        "directorDecision": decision, "beforeBytes": before_bytes, "catalogBytes": catalog_bytes, "before": before,
        "catalog": catalog, "queue": queue, "handoff": handoff, "pendingBefore": pending_before,
        "pendingIds": current_pending,
    }


def apply() -> None:
    data = validate_input()
    ts = now()
    archive_bytes = data["archiveBytes"]
    delivery_bytes = data["deliveryBytes"]
    before_bytes = data["beforeBytes"]
    catalog_bytes = data["catalogBytes"]
    before = data["before"]
    queue = data["queue"]
    model = data["model"]
    counts = data["counts"]
    verification = data["audit"]
    excluded_pending = sorted(data["pendingIds"] - set(IDS))

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-SUMMON-STRUCTURE5-153", "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": "SummonStructure5-Director-Return153", "accepted": True, "appliedAtDecision": False,
        "acceptedIds": IDS, "rejectedIds": [], "remainingBlockingDefects": [],
        "verification": {
            "directorStaticChecksPassed": 50_589, "directorStaticFailures": 0,
            "independentReturnAudit": verification, "archiveMembers": 246, "sourceBindings": 77,
            "evidenceMembers": 120, "cases": 102, "events": 620, "eventOperations": 2_480,
            "retainedHolds": 15, "heldDependentBranches": 57,
        },
        "acceptedArchive": {"name": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "scope": data["directorDecision"]["scope"],
        "holdScope": "All 15 hold categories and every source, access, profile, geometry, faction, equipment, lifecycle, runtime and other dependent hold remain active. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "excludedClaims": {"runtime": False, "humanPlay": False, "balance": False, "cosmology": False, "domainClosure": False, "release": False, "canonicalApplication": False},
        "directorMadeNoCanonicalChanges": True,
    }
    decision_bytes = json_bytes(decision_record)
    receipt = {
        "id": REVIEW_ID, "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision_record,
        "directorReturn": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "directorReturnDelivery": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN_DELIVERY.json", "bytes": len(delivery_bytes), "sha256": sha(delivery_bytes)},
        "acceptedIds": IDS, "countsBefore": {"reviewed": 713, "pending": 135, "acceptedUnapplied": 0},
        "countsAfter": {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0},
        "completeReviewedStandaloneProceduresBefore": 437, "completeReviewedStandaloneProceduresAfter": 442,
        "acceptedCases": counts["cases"], "mainCases": counts["mainCases"], "branches": counts["branches"],
        "heldDependentBranches": counts["heldDependentBranches"], "acceptedEvents": counts["events"],
        "eventOperations": counts["eventOperations"], "retainedHolds": counts["holdCategories"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all five identities; authored procedure review only.",
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "releaseApproved": False, "canonicalApplicationPerformed": False,
    }
    receipt_bytes = json_bytes(receipt)

    STAGING.mkdir(parents=True, exist_ok=True)
    director_dir = STAGING / "DIRECTOR_RETURN"
    director_dir.mkdir(exist_ok=True)
    with ZipFile(ARCHIVE) as archive:
        for name in archive.namelist():
            if "/" not in name and name != "CASEBOOK.json":
                (director_dir / name).write_bytes(archive.read(name))
            elif name.startswith("procedures/") and name.endswith(".json"):
                proc_path = director_dir / "PROCEDURES" / PurePosixPath(name).name
                proc_path.parent.mkdir(parents=True, exist_ok=True)
                proc_path.write_bytes(archive.read(name))
    casebook_gz = STAGING / "CASEBOOK.json.gz"
    with casebook_gz.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
            compressed.write(data["casebookBytes"])
    assert gzip.decompress(casebook_gz.read_bytes()) == data["casebookBytes"]
    assert len(data["casebookBytes"]) == data["casebookMember"]["bytes"]
    assert sha(data["casebookBytes"]) == data["casebookMember"]["sha256"]
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "DIRECTOR_RETURN_DELIVERY.json").write_bytes(delivery_bytes)
    (STAGING / "GPT_DIRECTOR_DECISION.json").write_bytes(decision_bytes)
    (STAGING / "EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    (STAGING / "INDEPENDENT_VERIFICATION.json").write_bytes(json_bytes(verification))
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(data["sourceArchiveBytes"])
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(data["sourceCandidateBytes"])
    (STAGING / "STANDALONE_PROCEDURES.md").write_bytes(data["standaloneBytes"])

    normalized_spells = []
    for pos, sid in enumerate(IDS):
        proc = copy.deepcopy(model["spells"][sid])
        native = proc["nativeUnchanged"]
        old = next(row for row in before["entries"] if row["id"] == sid)
        assert native["id"] == sid and native["name"] == old["name"]
        normalized_spells.append({
            "id": sid, "name": native["name"],
            "procedure": {"common": copy.deepcopy(proc["common"]), "companionRules": copy.deepcopy(proc["companionRules"]), "rules": copy.deepcopy(proc["rules"])},
            "directorProcedureRecord": proc,
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "procedureSourceQuestionIds": copy.deepcopy(proc.get("sourceQuestionIds", proc["questionIds"])),
            "runtimeSelectionEnabled": False,
        })
    normalized_model = {
        "schemaVersion": 1, "moduleId": "rank8summonstructure5-reviewed-153",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly five GPT-accepted Summon/Structure5 authored procedures with static cases and dispositions. Native spell cards, class access, source status and catalog bytes remain unchanged. All 15 holds and 57 held dependent branches remain. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Per-spell common rules are preserved inside each procedure record.", "perSpellCommon": {sid: copy.deepcopy(model["spells"][sid]["common"]) for sid in IDS}},
        "spells": normalized_spells,
        "questionDispositions": data["dispositions"], "originalIdentityDispositions": data["originalDispositions"],
        "returnCounts": counts, "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz", "casebookEncoding": "gzip; exact decompression reproduces the CASEBOOK.json member of DIRECTOR_RETURN_ARCHIVE.zip",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(data["casebookBytes"]), "sha256": sha(data["casebookBytes"])},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip", "directorReturnDelivery": "DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip", "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "STANDALONE_PROCEDURES.md", "directorDecisionFile": "GPT_DIRECTOR_DECISION.json",
        "directorReturnBinding": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "archiveMemberCount": 246, "independentAcceptanceGranted": True,
        "canonicalApplicationPerformed": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False, "releaseApproved": False,
    }

    package_files = []
    for path in sorted(STAGING.rglob("*")):
        rel = path.relative_to(STAGING).as_posix()
        if path.is_file() and rel not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            raw = path.read_bytes()
            package_files.append({"path": rel, "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-SUMMON-STRUCTURE5-CANDIDATE-PACKAGE-MANIFEST-153",
        "sourceArchive": {"name": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "files": package_files, "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
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
    holds_binding = binding(director_dir / "HOLDS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLDS.json")
    proposal_binding = binding(director_dir / "PROPOSAL_OPERATIONS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json")
    procedure_source_binding = binding(director_dir / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/MODEL.json")

    RECEIPT.write_bytes(receipt_bytes)
    DECISION.write_bytes(decision_bytes)
    os.replace(STAGING, CANDIDATE)
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_bytes(data["standaloneBytes"])

    app = {
        "id": APP_ID, "recordedAtUtc": now(), "status": "APPLIED_FIVE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID, "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue through all remaining pending ordinary spell identities.",
        "acceptedIds": IDS, "directorAcceptance": binding(RECEIPT), "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "directorReturnDelivery": binding(DELIVERY, f"{RECEIVED.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN_DELIVERY.json", delivery_bytes),
        "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {"reviewed": 713, "pending": 135, "acceptedUnapplied": 0}, "after": {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0}},
        "completeReviewedStandaloneProcedures": {"before": 437, "after": 442},
        "cases": counts["cases"], "completeStaticFixtures": counts["cases"] - counts["heldDependentBranches"],
        "heldDependentBranches": counts["heldDependentBranches"], "events": counts["events"],
        "eventOperations": counts["eventOperations"], "retainedHolds": counts["holdCategories"],
        "sourceStatusPreservedAsBlocked": True, "catalogChanged": False,
        "runtimeSelectionEnabled": False, "closedCohortsReopened": False,
    }
    app_bytes = json_bytes(app)
    app_binding = binding(APPLICATION, raw=app_bytes)

    after = copy.deepcopy(before)
    operations = []
    for sid in IDS:
        i = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][i]
        n = IDS.index(sid)
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank8summonstructure5_reviewed_153/MODEL.json",
            "procedurePointer": f"/spells/{n}/procedure", "wholeCardPointer": f"/spells/{n}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id", "procedureTextPointer": f"/spells/{n}/procedure",
            "directorProcedureRecordPointer": f"/spells/{n}/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRules/perSpellCommon",
            "manuscript": "../../../docs/spells/candidates/RANK8_SUMMON_STRUCTURE5_REVIEWED_153.md",
            "reviewId": APP_ID, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(), "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding, "casebookEncoding": "gzip; exact decompression reproduces the director return CASEBOOK.json member",
            "casebookSourceArchiveMemberBinding": normalized_model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": archive_binding, "sourceConferenceArchiveBinding": source_archive_binding,
            "sourceCandidateBinding": source_candidate_binding, "candidatePackageManifestBinding": package_manifest_binding,
            "retainedHoldsBinding": holds_binding, "procedureSourceBinding": procedure_source_binding,
            "proposalOperationsBinding": proposal_binding, "acceptedSharedRuleScope": receipt["decision"],
            "authoredAcceptanceReceipt": binding(RECEIPT), "authoredApplicationReceipt": app_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": i, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][i] = new
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank8summonstructure5_reviewed_153/MODEL.json", "binding": model_binding,
        "reviewId": REVIEW_ID, "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "authority": binding(RECEIPT), "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}",
        "sourceArchive": archive_binding, "casebookBinding": casebook_binding, "holdsBinding": holds_binding,
        "candidatePackageManifestBinding": package_manifest_binding, "scope": receipt["decision"], "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 718, "pending": 130}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 442
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 5 and len(pending_after) == 130 and pending_after == data["pendingIds"] - set(IDS)
    inverse = copy.deepcopy(after)
    for op in operations:
        inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    ops_doc = {
        "id": "SUMMON-STRUCTURE5-INDEX-OPERATIONS-153",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations, "inverse": {"semanticExact": True, "restores": "five prior entries, aggregate counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    BACKUP.write_bytes(before_bytes)
    write_json(APPLICATION, app)
    write_json(OPERATIONS, ops_doc)
    tmp = INDEX.with_suffix(".json.application153.tmp")
    tmp.write_bytes(after_bytes)
    os.replace(tmp, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = copy.deepcopy(queue["currentAuthority"])
    authority.update({"reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 442})
    groups = []
    for group in queue["currentPendingGroups"]:
        remaining = [sid for sid in group["pendingIds"] if sid in pending_after]
        if remaining:
            row = copy.deepcopy(group)
            row["pendingIds"] = remaining
            row["pendingCount"] = len(remaining)
            row["freshPacketRequiredForCurrentAuthority"] = True
            groups.append(row)
    assert groups[0]["group"] == "rank8-perception5" and sum(g["pendingCount"] for g in groups) == 130
    pending_doc = {
        "id": "CURRENT130-PENDING-IDENTITY-AUDIT-155", "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": binding(INDEX), "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"], "pendingCount": 130, "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in data["catalog"]["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)
    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-155", "recordedAtUtc": now(), "currentAuthority": authority,
        "currentPendingGroups": groups, "nextSuggestedGroups": groups[:5], "nextGroup": groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 5, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 130, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "archive": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True},
    })
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(read_json(HANDOFF_BEFORE))
    handoff.update({
        "id": "CURRENT-HANDOFF-155", "recordedAtUtc": now(), "status": "RANK8_SUMMON_STRUCTURE5_APPLIED_NEXT_130_PENDING",
        "currentAuthority": authority, "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 130, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 5, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}", "directorAcceptance": f"{AUDIT.relative_to(ROOT).as_posix()}/{RECEIPT.name}"},
        "nextGroup": groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed16/72, feat335, or any accepted/applied spell cohort. Runtime, source/content/access and domain holds remain separately tracked.",
        "resumePriority": "Prepare a fresh Rank8 Perception5 packet against 718/130 authority, submit it to GPT director review, then apply only exact accepted IDs.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True, "request": "Prepare and submit a fresh request bound to current 718/130 authority before director review."},
    })
    write_json(HANDOFF_AFTER, handoff)
    write_json(VALIDATION, {
        "id": "SUMMON-STRUCTURE5-APPLICATION-VALIDATION-153", "status": "PASS", "checksPassed": 30, "checksFailed": 0,
        "checks": [
            "Independent Return153 verification passed for exact archive/delivery hash, all 246 member hashes and CRCs, all 77 live source bindings, all 120 evidence files, and 2,480 event operations",
            "exact GPT acceptance applies only the five named Summon/Structure5 identities",
            "all 20 conference and five original-identity question dispositions are preserved",
            "all 15 hold definitions and 57 held dependent branches remain retained",
            "all 102 cases, 620 events, and 2,480 event operations are preserved",
            "only five accepted identities changed in the authored review index and inverse semantic replay is exact",
            "counts advance to 718 reviewed / 130 pending / 0 accepted-unapplied and 442 complete procedures",
            "all 130 pending identities remain present in the source catalog",
            "source catalog bytes and native spell access rows remain unchanged",
            "source status remains blocked and runtime selection remains disabled",
            "casebook gzip decompresses byte-identically to the accepted CASEBOOK.json member",
            "candidate manifest binds every package file except its declared exclusions",
            "next queue group is Rank8 Perception5 and requires a fresh 718/130 packet",
            "closed feat335, completed spells, and prior applied cohorts remain closed",
            "no runtime, human-play, balance, cosmology, domain-closure, or release approval was added",
        ],
        "beforeIndex": binding(BACKUP), "afterIndex": binding(INDEX), "changedIdentityIds": IDS,
        "onlyFivePendingEntriesChanged": True, "authoredCounts": after["authoredCounts"],
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes, "sourceStatusStillBlockedForAllFive": True,
        "runtimeSelectionEnabled": False, "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before, "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all246ReturnMembersVerified": True, "acceptedUnapplied": 0, "nextGroup": groups[0]["group"], "nextPendingCount": groups[0]["pendingCount"],
        "applicationReceipt": binding(APPLICATION), "directorAcceptanceReceipt": binding(RECEIPT),
    })

    old_start = START.read_text(encoding="utf-8-sig")
    old_marker = "**Prior checkpoint: ["
    marker_at = old_start.find(old_marker)
    historic = old_start[marker_at:] if marker_at >= 0 else ""
    START.write_text(
        "# Active ordinary spell review155 — Calibration review part6\n\n"
        "Return153 was GPT director accepted, independently verified, and applied to five exact identities: **718 applied-reviewed / 130 pending / 0 accepted-unapplied**. "
        "The director reports 50,589 static checks with no failures; independent return verification passed all 246 members, 77 source bindings, 120 evidence bindings, and 2,480 event operations. "
        "All 15 hold categories and 57 held dependent branches remain. Runtime, human-play, balance, cosmology, domain closure and release approval remain separate.\n\n"
        f"Continue with **{groups[0]['group']}**, preparing a fresh packet against 718/130 and submitting it to GPT for exact director review. Apply only accepted IDs. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [CURRENT-HANDOFF-155](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[the 130-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [snapshot status]({SNAPSHOT.name}).\n\n" + historic,
        encoding="utf-8", newline="\n",
    )
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Return153\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **718 reviewed / 130 pending / 0 accepted-unapplied**. Return153 applies the five GPT-accepted Summon/Structure5 procedures: Summon Greater Water Pet, Summon Archlich Shade, Faction Paragon, Conjure Sky Fortress, and Shifting Fortress.\n\n"
        "The exact director return has 246 verified members, 77 bound current source files, 120 exact evidence bindings, 102 cases, and 620 events. Independent verification replayed all event states and hashes plus 2,480 forward/inverse operations. All 15 hold categories and 57 held dependent branches remain; catalog bytes and native class access are unchanged.\n\n"
        f"The next batch is {groups[0]['group']}. Prepare a fresh packet against 718/130 and wait for exact GPT director acceptance before applying.\n\n"
        "Runtime selection remains disabled. This authored-procedure review does not approve runtime behavior, human play, balance, cosmology, domain closure, or release. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}), "
        f"and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    assert read_json(INDEX)["authoredCounts"] == {"reviewed": 718, "pending": 130}
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "authority": authority, "nextGroup": groups[0]["group"], "nextPendingCount": groups[0]["pendingCount"], "independentReturnVerification": verification, "indexSha256": sha(INDEX.read_bytes()), "catalogUnchanged": True}, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = validate_input()
        print(json.dumps({"status": "PREFLIGHT_PASS", "acceptedIds": IDS, "authority": data["audit"]["inputAuthority"], "nextGroup": data["queue"]["currentPendingGroups"][1]["group"], "archiveBytes": len(data["archiveBytes"]), "candidateOutputAbsent": not CANDIDATE.exists(), "catalogUnchanged": True}, indent=2))
