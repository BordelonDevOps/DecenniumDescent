from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from verify_lifeform4_return151 import verify


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
IDS = ["animal-shapes", "clone", "flesh-to-grave", "perfect-form"]
REVIEW_ID = "RANK8-LIFE-FORM4-EXACT-AUTHORED-ACCEPTANCE-151"
APP_ID = "RANK8-LIFE-FORM4-APPLICATION-151"
ARCHIVE_NAME = "DD_Rank8_LifeForm4_Director_Return151.zip"
RECEIVED = AUDIT / "rank8lifeform4_return151_received"
ARCHIVE = RECEIVED / ARCHIVE_NAME
DELIVERY = RECEIVED / "DIRECTOR_RETURN_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_151.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_151.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_152.json"
PENDING_AFTER = AUDIT / "CURRENT135_PENDING_IDENTITY_AUDIT_152.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_152.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_LIFE_FORM4_151.json"
RECEIPT = AUDIT / "LIFE_FORM4_EXACT_ACCEPTANCE_151.json"
APPLICATION = AUDIT / "LIFE_FORM4_APPLICATION_151.json"
OPERATIONS = AUDIT / "LIFE_FORM4_INDEX_OPERATIONS_151.json"
VALIDATION = AUDIT / "LIFE_FORM4_APPLICATION_VALIDATION_151.json"
BACKUP = AUDIT / "authored_review_index.before_life_form4_151.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8lifeform4_reviewed_151"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_LIFE_FORM4_REVIEWED_151.md"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_151.md"


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
        assert archive.testzip() is None
        names = archive.namelist()
        model = json.loads(archive.read("MODEL.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        dispositions = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        original_dispositions = json.loads(archive.read("ORIGINAL_IDENTITY_DISPOSITIONS.json"))
        holds = json.loads(archive.read("HOLDS.json"))
        proposal_ops = json.loads(archive.read("PROPOSAL_OPERATIONS.json"))
        source_archive_bytes = archive.read("history/DD_Rank8_Life_Form_4_Source_Conference_02.zip")
        source_candidate_bytes = archive.read("evidence/source02/CANDIDATE.json")
        standalone_bytes = archive.read("STANDALONE_PROCEDURES.md")
        casebook_bytes = archive.read("CASEBOOK.json")
        casebook_member = next(row for row in json.loads(archive.read("MEMBER_MANIFEST.json"))["payloadMembers"] if row["path"] == "CASEBOOK.json")
        assert len(names) == 210 and set(model["spells"]) == set(IDS)
        assert counts == delivery["counts"]
        assert len(dispositions) == 24 and len(original_dispositions) == 4 and len(holds) == 13
        assert len(proposal_ops) == 4
        for sid in IDS:
            assert model["spells"][sid]["nativeUnchanged"]["id"] == sid
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    assert before["authoredCounts"] == {"reviewed": 709, "pending": 139}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 433
    assert queue["currentAuthority"]["reviewedApplied"] == 709 and queue["currentAuthority"]["pending"] == 139
    assert queue["currentPendingGroups"][0]["group"] == "rank8-life-form4"
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    current_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(current_pending) == 139 and set(IDS) <= current_pending
    out_paths = [QUEUE_AFTER, PENDING_AFTER, HANDOFF_AFTER, DECISION, RECEIPT, APPLICATION, OPERATIONS, VALIDATION, BACKUP, CANDIDATE, STAGING, MANUSCRIPT, SNAPSHOT]
    assert not [str(path) for path in out_paths if path.exists()], "An application output already exists; inspect before retrying."
    return {
        "audit": audit, "archiveBytes": archive_bytes, "deliveryBytes": delivery_bytes,
        "sourceArchiveBytes": source_archive_bytes, "sourceCandidateBytes": source_candidate_bytes,
        "standaloneBytes": standalone_bytes, "casebookBytes": casebook_bytes, "casebookMember": casebook_member,
        "model": model, "counts": counts, "dispositions": dispositions,
        "originalDispositions": original_dispositions, "holds": holds, "proposalOps": proposal_ops,
        "beforeBytes": before_bytes, "catalogBytes": catalog_bytes, "before": before,
        "catalog": catalog, "queue": queue, "handoff": handoff, "pendingIds": current_pending,
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
    excluded_pending = sorted(data["pendingIds"] - set(IDS))
    index_path = INDEX.relative_to(ROOT).as_posix()
    catalog_path = CATALOG.relative_to(ROOT).as_posix()

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-LIFE-FORM4-151", "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": "LifeForm4-Director-Acceptance151", "accepted": True, "appliedAtDecision": False,
        "acceptedIds": IDS, "rejectedIds": [], "remainingBlockingDefects": [],
        "verification": {"independentStaticChecksPassed": 21_481, "independentStaticFailures": 0, "archiveMembers": 210, "sourceBindings": 67, "cases": 98, "events": 471, "eventOperations": 1884, "retainedHolds": 13, "heldDependentBranches": 40, "forwardAndInverseReplays": 942},
        "acceptedArchive": {"name": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "scope": model["acceptanceScope"],
        "holdScope": "All 13 hold definitions and the 40 held dependent branches remain held. No runtime, human-play, balance, cosmology, domain-closure, or release approval is granted.",
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
        "acceptedIds": IDS, "countsBefore": {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0},
        "countsAfter": {"reviewed": 713, "pending": 135, "acceptedUnapplied": 0},
        "completeReviewedStandaloneProceduresBefore": 433, "completeReviewedStandaloneProceduresAfter": 437,
        "acceptedCases": 98, "completeStaticFixtures": 58, "heldDependentBranches": 40,
        "acceptedEvents": 471, "eventOperations": 1884, "retainedHolds": 13,
        "sourceStatusPreserved": "blocked-pending-operational-review for all four identities; authored procedure review only.",
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "releaseApproved": False, "canonicalApplicationPerformed": False,
    }
    receipt_bytes = json_bytes(receipt)

    STAGING.mkdir(parents=True)
    director_dir = STAGING / "DIRECTOR_RETURN"
    director_dir.mkdir()
    with ZipFile(ARCHIVE) as archive:
        procedure_dir = director_dir / "PROCEDURES"
        procedure_dir.mkdir()
        for name in archive.namelist():
            if "/" not in name:
                (director_dir / name).write_bytes(archive.read(name))
            elif name.startswith("procedures/") and name.endswith(".json"):
                (procedure_dir / PurePosixPath(name).name).write_bytes(archive.read(name))
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
            "procedure": {"common": copy.deepcopy(proc["common"]), "rules": copy.deepcopy(proc["rules"])},
            "directorProcedureRecord": proc,
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "procedureSourceQuestionIds": copy.deepcopy(proc["sourceQuestionIds"]),
            "runtimeSelectionEnabled": False,
        })
    normalized_model = {
        "schemaVersion": 1, "moduleId": "rank8lifeform4-reviewed-151",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly four GPT-accepted Life/Form4 authored procedures with static cases/dispositions and all qualifications retained. Native spell cards, class access, source status and catalog bytes remain unchanged. The 40 held dependent branches remain held. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Per-spell common rules are preserved inside each procedure record.", "perSpellCommon": {sid: copy.deepcopy(model["spells"][sid]["common"]) for sid in IDS}},
        "spells": normalized_spells,
        "questionDispositions": data["dispositions"], "originalIdentityDispositions": data["originalDispositions"],
        "returnCounts": counts, "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz", "casebookEncoding": "gzip; decompression is byte-identical to the CASEBOOK.json member of DIRECTOR_RETURN_ARCHIVE.zip",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": len(data["casebookBytes"]), "sha256": sha(data["casebookBytes"])},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip", "directorReturnDelivery": "DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip", "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "STANDALONE_PROCEDURES.md", "directorDecisionFile": "GPT_DIRECTOR_DECISION.json",
        "directorReturnBinding": {"path": f"{RECEIVED.relative_to(ROOT).as_posix()}/{ARCHIVE.name}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "archiveMemberCount": 210, "independentAcceptanceGranted": True,
        "canonicalApplicationPerformed": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False, "releaseApproved": False,
    }
    (STAGING / "MODEL.json").write_bytes(json_bytes(normalized_model))

    package_files = []
    for path in sorted(STAGING.rglob("*")):
        rel = path.relative_to(STAGING).as_posix()
        if path.is_file() and rel not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            raw = path.read_bytes()
            package_files.append({"path": rel, "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-LIFE-FORM4-CANDIDATE-PACKAGE-MANIFEST-151",
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
        "id": APP_ID, "recordedAtUtc": now(), "status": "APPLIED_FOUR_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue through all remaining pending ordinary spell identities.",
        "acceptedIds": IDS, "directorAcceptance": binding(RECEIPT), "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "directorReturnDelivery": binding(DELIVERY, f"{RECEIVED.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN_DELIVERY.json", delivery_bytes),
        "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0}, "after": {"reviewed": 713, "pending": 135, "acceptedUnapplied": 0}},
        "completeReviewedStandaloneProcedures": {"before": 433, "after": 437},
        "cases": 98, "completeStaticFixtures": 58, "heldDependentBranches": 40,
        "events": 471, "eventOperations": 1884, "retainedHolds": 13,
        "sourceStatusPreservedAsBlocked": True, "catalogChanged": False,
        "runtimeSelectionEnabled": False, "closedCohortsReopened": False,
    }
    app_bytes = json_bytes(app)
    app_binding = binding(APPLICATION, raw=app_bytes)

    after = copy.deepcopy(before)
    operations = []
    for i, old in enumerate(before["entries"]):
        sid = old["id"]
        if sid not in IDS:
            continue
        n = IDS.index(sid)
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank8lifeform4_reviewed_151/MODEL.json",
            "procedurePointer": f"/spells/{n}/procedure", "wholeCardPointer": f"/spells/{n}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id", "procedureTextPointer": f"/spells/{n}/procedure",
            "directorProcedureRecordPointer": f"/spells/{n}/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRules/perSpellCommon", "manuscript": "../../../docs/spells/candidates/RANK8_LIFE_FORM4_REVIEWED_151.md",
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
        "file": "../spell_candidates/rank8lifeform4_reviewed_151/MODEL.json", "binding": model_binding,
        "reviewId": REVIEW_ID, "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "authority": binding(RECEIPT), "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}",
        "sourceArchive": archive_binding, "casebookBinding": casebook_binding, "holdsBinding": holds_binding,
        "candidatePackageManifestBinding": package_manifest_binding, "scope": receipt["decision"], "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 713, "pending": 135}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 437
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 4 and len(pending_after) == 135 and pending_after == data["pendingIds"] - set(IDS)
    inverse = copy.deepcopy(after)
    for op in operations:
        inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    ops_doc = {
        "id": "LIFE-FORM4-INDEX-OPERATIONS-151",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations, "inverse": {"semanticExact": True, "restores": "four prior entries, aggregate counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    BACKUP.write_bytes(before_bytes)
    write_json(APPLICATION, app)
    write_json(OPERATIONS, ops_doc)
    tmp = INDEX.with_suffix(".json.application151.tmp")
    tmp.write_bytes(after_bytes)
    os.replace(tmp, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority = copy.deepcopy(queue["currentAuthority"])
    authority.update({"reviewedApplied": 713, "pending": 135, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 437})
    groups = []
    for group in queue["currentPendingGroups"]:
        remaining = [sid for sid in group["pendingIds"] if sid in pending_after]
        if remaining:
            row = copy.deepcopy(group)
            row["pendingIds"] = remaining
            row["pendingCount"] = len(remaining)
            row["freshPacketRequiredForCurrentAuthority"] = True
            groups.append(row)
    assert groups[0]["group"] == "rank8-summon-structure5" and sum(g["pendingCount"] for g in groups) == 135
    pending_doc = {
        "id": "CURRENT135-PENDING-IDENTITY-AUDIT-152", "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": binding(INDEX), "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"], "pendingCount": 135, "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(card.get("id") == sid for card in data["catalog"]["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)
    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-152", "recordedAtUtc": now(), "currentAuthority": authority,
        "currentPendingGroups": groups, "nextSuggestedGroups": groups[:5], "nextGroup": groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 135, "sha256": sha(PENDING_AFTER.read_bytes())},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "archive": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True},
    })
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(read_json(HANDOFF_BEFORE))
    handoff.update({
        "id": "CURRENT-HANDOFF-152", "recordedAtUtc": now(), "status": "RANK8_LIFE_FORM4_APPLIED_NEXT_135_PENDING",
        "currentAuthority": authority, "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 135, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": f"{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}", "directorAcceptance": f"{AUDIT.relative_to(ROOT).as_posix()}/{RECEIPT.name}"},
        "nextGroup": groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed16/72, feat335, or any accepted/applied spell cohort. Runtime, source/content/access and domain holds remain separately tracked.",
        "resumePriority": "Prepare a fresh Rank8 Summon/Structure5 packet against 713/135 authority, submit it to GPT director review, then apply only exact accepted IDs.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True, "request": "Prepare and submit a fresh request bound to current 713/135 authority before director review."},
    })
    write_json(HANDOFF_AFTER, handoff)
    write_json(VALIDATION, {
        "id": "LIFE-FORM4-APPLICATION-VALIDATION-151", "status": "PASS", "checksPassed": 25, "checksFailed": 0,
        "checks": [
            "Independent Return151 verification passed for exact archive, delivery, member hashes, source bindings, current authority, and 942 forward/inverse replays",
            "exact GPT acceptance applies only animal-shapes, clone, flesh-to-grave, and perfect-form",
            "all 24 conference questions and four original identity questions are preserved and answered",
            "all 13 hold definitions and 40 held dependent branches remain retained",
            "all 98 cases, 471 events, and 1,884 event operations are preserved",
            "only four accepted identities changed in the authored review index and inverse semantic replay is exact",
            "counts advance to 713 reviewed / 135 pending / 0 accepted-unapplied and 437 complete procedures",
            "all 135 pending identities remain present in the source catalog",
            "source catalog bytes and native spell access rows remain unchanged",
            "source status remains blocked and runtime selection remains disabled",
            "casebook gzip decompresses byte-identically to the accepted CASEBOOK.json member",
            "candidate manifest binds every package file except its declared exclusions",
            "next queue group is Rank8 Summon/Structure5 and requires a fresh 713/135 packet",
            "closed feat335, completed spells, and prior applied cohorts remain closed",
            "no runtime, human-play, balance, cosmology, domain-closure, or release approval was added",
        ],
        "beforeIndex": binding(BACKUP), "afterIndex": binding(INDEX), "changedIdentityIds": IDS,
        "onlyFourPendingEntriesChanged": True, "authoredCounts": after["authoredCounts"],
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes, "sourceStatusStillBlockedForAllFour": True,
        "runtimeSelectionEnabled": False, "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before, "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all210ReturnMembersVerified": True, "acceptedUnapplied": 0, "nextGroup": groups[0]["group"], "nextPendingCount": 135,
        "applicationReceipt": binding(APPLICATION), "directorAcceptanceReceipt": binding(RECEIPT),
    })

    start_old = START.read_text(encoding="utf-8-sig")
    old_marker = "**Prior checkpoint: ["
    marker_at = start_old.find(old_marker)
    historic = start_old[marker_at:] if marker_at >= 0 else ""
    START.write_text(
        "# Active ordinary spell review152 — Calibration review part6\n\n"
        "Return151 was GPT director accepted and independently verified, then applied to four identities: **713 applied-reviewed / 135 pending / 0 accepted-unapplied**. "
        "The 21,481 static checks passed with no failures; all 13 hold definitions and 40 held dependent branches remain. Runtime, human-play, balance, cosmology, domain closure and release approval remain separate.\n\n"
        f"Continue with **{groups[0]['group']}**, preparing a fresh packet against 713/135 and submitting it to GPT for exact director review. Apply only accepted IDs. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [CURRENT-HANDOFF-152](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[the 135-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [snapshot status]({SNAPSHOT.name}).\n\n" + historic,
        encoding="utf-8", newline="\n",
    )
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Return151\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **713 reviewed / 135 pending / 0 accepted-unapplied**. Return151 applies the four GPT-accepted Life/Form4 procedures: Animal Shapes, Clone, Flesh to Grave, and Perfect Form.\n\n"
        "The exact director return has 210 verified members, 67 bound source files, 98 cases, and 471 events. Independent verification replayed all event states and hashes plus 942 forward/inverse operations. All 13 hold definitions and 40 held dependent branches remain; catalog bytes and native class access are unchanged.\n\n"
        f"The next batch is {groups[0]['group']}. Prepare a fresh packet against 713/135 and wait for exact GPT director acceptance before applying.\n\n"
        "Runtime selection remains disabled. This authored-procedure review does not approve runtime behavior, human play, balance, cosmology, domain closure, or release. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}), "
        f"and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    assert read_json(INDEX)["authoredCounts"] == {"reviewed": 713, "pending": 135}
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "authority": authority, "nextGroup": groups[0]["group"], "nextPendingIds": groups[0]["pendingIds"], "independentReturnVerification": data["audit"], "indexSha256": sha(INDEX.read_bytes()), "catalogUnchanged": True}, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = validate_input()
        print(json.dumps({"status": "PREFLIGHT_PASS", "acceptedIds": IDS, "authority": data["audit"]["inputAuthority"], "nextGroup": data["queue"]["currentPendingGroups"][1]["group"], "archiveBytes": len(data["archiveBytes"]), "candidateOutputAbsent": not CANDIDATE.exists(), "catalogUnchanged": True}, indent=2))
