from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone
from zipfile import ZipFile

ROOT = Path(r"C:\Github\DecenniumDescent")
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
DELIVERY_DIR = Path(r"C:\r8fd153")
PACKET_DIR = Path(r"C:\r8f153")
RETURN_ZIP = DELIVERY_DIR / "DD_Rank8Resource6_Director_Return01_147.zip"
RETURN_DELIVERY = DELIVERY_DIR / "DD_Rank8Resource6_Director_Return01_147_Delivery.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_resource_6_source_conference_01.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank8_Resource_6_Source_Conference_01.zip"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_141.json"
PENDING_BEFORE = AUDIT / "CURRENT159_PENDING_IDENTITY_AUDIT_141.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_141.json"
IDS = [
    "spell-absorption-shield",
    "resonance-nullification",
    "resonance-furnace",
    "resonance-matrix",
    "resonance-mastery",
    "leyline-flow",
]
REVIEW_ID = "RANK8-RESOURCE6-EXACT-AUTHORED-ACCEPTANCE-147"
APP_PATH = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK8_RESOURCE6_APPLICATION_147.json"
RECEIPT_PATH = AUDIT / "RANK8_RESOURCE6_EXACT_ACCEPTANCE_147.json"
APP_FILE = AUDIT / "RANK8_RESOURCE6_APPLICATION_147.json"
OPS_FILE = AUDIT / "RANK8_RESOURCE6_INDEX_OPERATIONS_147.json"
VALIDATION_FILE = AUDIT / "RANK8_RESOURCE6_APPLICATION_VALIDATION_147.json"
BACKUP = AUDIT / "authored_review_index.before_rank8resource6_147.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_147.json"
PENDING_AFTER = AUDIT / "CURRENT153_PENDING_IDENTITY_AUDIT_147.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_147.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8resource6_reviewed_147"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_RESOURCE6_REVIEWED_147.md"
SCRIPT_DEST = AUDIT / "apply_rank8resource6_return147.py"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def binding(path: Path, rel: str | None = None, data: bytes | None = None) -> dict:
    raw = path.read_bytes() if data is None else data
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def candidate_binding(name: str) -> dict:
    p = CANDIDATE / name
    return binding(p, CANDIDATE.relative_to(ROOT).as_posix() + "/" + name)


def main(apply: bool) -> None:
    expected_zip_sha = "aadd056078bc0928c09cf6532052e2292ede594003298fe532ae78c6de24eec5"
    expected_index_sha = "7a0c5dd6d9daad405cb63cb2fe1abc3a1f4fa445a933fd31dfaa48f303bf8877"
    expected_catalog_sha = "f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8"
    assert ROOT.is_dir() and INDEX.is_file() and CATALOG.is_file()
    assert sha(RETURN_ZIP.read_bytes()) == expected_zip_sha
    raw_zip = RETURN_ZIP.read_bytes()
    delivery_bytes = RETURN_DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    assert len(raw_zip) == 47_373_674 and delivery["bytes"] == len(raw_zip)
    assert delivery["sha256"] == sha(raw_zip) == expected_zip_sha
    assert delivery["accepted"] is False and delivery["applied"] is False
    assert delivery["authority"] == {
        "reviewedApplied": 689,
        "pending": 159,
        "acceptedUnapplied": 0,
        "completeReviewedStandaloneProcedures": 413,
    }
    before_bytes = INDEX.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog_bytes = CATALOG.read_bytes()
    catalog = json.loads(catalog_bytes.decode("utf-8-sig"))
    queue_before = read_json(QUEUE_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    handoff_before = read_json(HANDOFF_BEFORE)
    assert sha(before_bytes) == expected_index_sha
    assert before["authoredCounts"] == {"reviewed": 689, "pending": 159}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 413
    assert sha(catalog_bytes) == expected_catalog_sha == before["sourceCatalogSha256"]
    assert queue_before["currentAuthority"]["reviewedApplied"] == 689
    assert queue_before["currentAuthority"]["pending"] == 159
    assert pending_before["pendingCount"] == 159
    assert pending_before["indexBinding"]["sha256"] == expected_index_sha
    assert handoff_before["currentAuthority"]["reviewedApplied"] == 689

    decision = {
        "id": "GPT-DIRECTOR-DECISION-RANK8-RESOURCE6-147",
        "recordedAtUtc": now(),
        "source": {
            "product": "ChatGPT",
            "project": "Dungeon Crawler",
            "conversation": "Calibration review part 6",
            "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
            "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682",
        },
        "decision": "Director acceptance: accepted=true, applied=false for exact Return147. No blockers remain in the requested recheck.",
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "verification": {
            "checksPassed": 4877,
            "checksFailed": 0,
            "furnaceContinuityAndRepeatCastHistory": True,
            "matrixFundingAndHoldIndexes": True,
            "all547EventsStateHashesContinuityAndReplays": True,
            "eventOperationCount": 2188,
            "proposalOperationCount": 24,
            "exact155MemberAllowlistCrcHashesAndDeliveryBinding": True,
            "retainedHolds": 13,
        },
        "acceptedArchive": {
            "name": RETURN_ZIP.name,
            "bytes": len(raw_zip),
            "sha256": sha(raw_zip),
        },
        "scope": "Acceptance covers this authored procedure data package and its retained holds only. Runtime, human-play, balance, cosmology, release, and domain-closure approval remain out of scope.",
        "directorMadeNoLocalChanges": True,
    }
    decision_bytes = json_bytes(decision)
    receipt = {
        "id": REVIEW_ID,
        "recordedAtUtc": now(),
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision,
        "directorReturn": {
            "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/DD_Rank8Resource6_Director_Return01_147.zip",
            "bytes": len(raw_zip),
            "sha256": sha(raw_zip),
        },
        "directorReturnDelivery": {
            "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/DIRECTOR_RETURN_DELIVERY.json",
            "bytes": len(delivery_bytes),
            "sha256": sha(delivery_bytes),
        },
        "acceptedIds": IDS,
        "countsBefore": {"reviewed": 689, "pending": 159, "acceptedUnapplied": 0},
        "submittedLocalValidation": {
            "scopedChecksPassed": 14495,
            "scopedChecksFailed": 0,
            "packageIntegrityChecksPassed": 468,
        },
        "retainedHoldCount": 13,
        "sourceStatusPreserved": "blocked-pending-operational-review for all six identities; acceptance closes authored procedure review only.",
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

    with ZipFile(RETURN_ZIP) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        archive_manifest_bytes = archive.read("MANIFEST.json")
        archive_manifest = json.loads(archive_manifest_bytes.decode("utf-8-sig"))
        assert len(names) == 155 and len(archive_manifest["members"]) == 154
        assert set(names) == {member["path"] for member in archive_manifest["members"]} | {"MANIFEST.json"}
        assert delivery["manifestSHA256"] == sha(archive_manifest_bytes)
        member_data: dict[str, bytes] = {}
        for member in archive_manifest["members"]:
            member_bytes = archive.read(member["path"])
            assert len(member_bytes) == member["bytes"]
            assert sha(member_bytes) == member["sha256"], member["path"]
            if member["path"] in {
                "PROCEDURES.json",
                "PROCEDURE_AUTHORING_OPERATIONS.json",
                "SHARED_LOCAL_RULES.json",
                "CASE_DISPOSITIONS.json",
                "QUESTION_DISPOSITIONS.json",
                "FUTURE_OBLIGATION_DISPOSITIONS.json",
                "HOLD_REGISTER.json",
                "SOURCE_VERIFICATION.json",
                "CURRENT_SOURCE_STATUS_RECONCILIATION.json",
                "EXACT_COUNTS.json",
                "STANDALONE_PROCEDURES.md",
                "ACTOR_PROFILES.json",
                "ARTIFACT_BINDINGS.json",
                "EXACT_ACCEPTED_COMPARISONS.json",
            }:
                member_data[member["path"]] = member_bytes
        assert archive.read("authority/authored_review_index.json") == before_bytes
        assert archive.read("authority/catalog.json") == catalog_bytes
        assert archive.read("authority/CURRENT_SPELL_QUEUE_141.json") == QUEUE_BEFORE.read_bytes()
        assert archive.read("authority/CURRENT159_PENDING_IDENTITY_AUDIT_141.json") == PENDING_BEFORE.read_bytes()
        assert archive.read("authority/CURRENT_HANDOFF_141.json") == HANDOFF_BEFORE.read_bytes()
        source_candidate_archive = archive.read("source/current_candidate.json")
        source_history_archive = archive.read("history/current_source_archive.zip")
        source_index = read_json(SOURCE_CANDIDATE)
        assert source_candidate_archive == SOURCE_CANDIDATE.read_bytes()
        assert source_history_archive == SOURCE_ARCHIVE.read_bytes()
        assert len(source_candidate_archive) == delivery["sourceCandidate"]["bytes"]
        assert sha(source_candidate_archive) == delivery["sourceCandidate"]["sha256"]
        assert len(source_history_archive) == delivery["sourceArchive"]["bytes"]
        assert sha(source_history_archive) == delivery["sourceArchive"]["sha256"]
        procedures_bytes = archive.read("PROCEDURES.json")
        casebook_sha = hashlib.sha256()
        casebook_size = 0
        with archive.open("CASEBOOK.json") as casebook_stream:
            for chunk in iter(lambda: casebook_stream.read(1024 * 1024), b""):
                casebook_sha.update(chunk)
                casebook_size += len(chunk)
        # Open the member once more to stream the exact original bytes into a deterministic gzip.
        casebook_temp = None
        procedures_doc = json.loads(procedures_bytes.decode("utf-8-sig"))
        operations_doc = json.loads(member_data["PROCEDURE_AUTHORING_OPERATIONS.json"].decode("utf-8-sig"))
        shared_rules = json.loads(member_data["SHARED_LOCAL_RULES.json"].decode("utf-8-sig"))
        counts_doc = json.loads(member_data["EXACT_COUNTS.json"].decode("utf-8-sig"))
        hold_doc = json.loads(member_data["HOLD_REGISTER.json"].decode("utf-8-sig"))
        assert [row["id"] for row in procedures_doc["procedures"]] == IDS
        assert [row["id"] for row in operations_doc] == IDS
        assert procedures_doc["authority"]["reviewedApplied"] == 689
        assert procedures_doc["authority"]["pending"] == 159
        assert procedures_doc["accepted"] is False and procedures_doc["applied"] is False
        assert counts_doc["cases"]["total"] == 58 and counts_doc["events"] == 547
        assert counts_doc["holds"]["returnHoldRecords"] == 13
        assert len(hold_doc["holds"]) == 13
        assert len(before["entries"]) == 848
        rows = {entry["id"]: entry for entry in before["entries"]}
        assert all(rows[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS)
        assert all(sid in pending_before["pendingIds"] for sid in IDS)
        assert source_index.get("id") == "RANK8-RESOURCE-6-SOURCE-CONFERENCE-01"
        for sid, procedure in zip(IDS, procedures_doc["procedures"], strict=True):
            assert procedure["accepted"] is False and procedure["applied"] is False
            assert procedure["completeProposedProcedure"]
            assert rows[sid]["wholeCardPointer"].startswith("/spells/")

    # Precompute the candidate package without touching the current index.
    excluded_pending = sorted(entry["id"] for entry in before["entries"]
                              if entry["authoredStatus"] == "pending-authored-procedure" and entry["id"] not in IDS)
    decision_rel = "GPT_DIRECTOR_DECISION.json"
    copied_names = [
        "PROCEDURES.json",
        "PROCEDURE_AUTHORING_OPERATIONS.json",
        "SHARED_LOCAL_RULES.json",
        "CASE_DISPOSITIONS.json",
        "QUESTION_DISPOSITIONS.json",
        "FUTURE_OBLIGATION_DISPOSITIONS.json",
        "HOLD_REGISTER.json",
        "SOURCE_VERIFICATION.json",
        "CURRENT_SOURCE_STATUS_RECONCILIATION.json",
        "EXACT_COUNTS.json",
        "STANDALONE_PROCEDURES.md",
        "ACTOR_PROFILES.json",
        "ARTIFACT_BINDINGS.json",
        "EXACT_ACCEPTED_COMPARISONS.json",
    ]
    model_spells = []
    for i, procedure in enumerate(procedures_doc["procedures"]):
        sid = procedure["id"]
        row = rows[sid]
        model_spells.append({
            "id": sid,
            "name": row["name"],
            "procedure": copy.deepcopy(procedure["completeProposedProcedure"]),
            "directorProcedureRecord": copy.deepcopy(procedure),
            "nativeCardAndAccessUnchanged": copy.deepcopy(procedure["completeNativeCardAndAccessUnchanged"]),
            "sourceCatalogWholeCardPointer": row.get("sourceCatalogWholeCardPointer") or row["wholeCardPointer"],
            "runtimeSelectionEnabled": False,
        })
    scope = (
        "Only spell-absorption-shield, resonance-nullification, resonance-furnace, resonance-matrix, "
        "resonance-mastery and leyline-flow authored procedures, their accepted cases and selected dispositions "
        "are recorded. All 13 source, case, content, and verification holds remain. Native source cards, class "
        "access, source status, catalog, and shared rules outside this exact six-spell scope are unchanged. "
        "This closes authored procedure review only; runtime selection remains disabled, with no runtime, "
        "human-play, balance, cosmology, release, or domain-closure approval."
    )
    model = {
        "schemaVersion": 3,
        "moduleId": "rank8resource6-reviewed-147",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": scope,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": shared_rules,
        "spells": model_spells,
        "questionDispositions": json.loads(member_data["QUESTION_DISPOSITIONS.json"].decode("utf-8-sig")),
        "caseDispositions": json.loads(member_data["CASE_DISPOSITIONS.json"].decode("utf-8-sig")),
        "futureObligationDispositions": json.loads(member_data["FUTURE_OBLIGATION_DISPOSITIONS.json"].decode("utf-8-sig")),
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; exact decompression reproduces the director return CASEBOOK.json member",
        "casebookSourceMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_size, "sha256": casebook_sha.hexdigest()},
        "holdsFile": "HOLD_REGISTER.json",
        "procedureSourceFile": "PROCEDURES.json",
        "procedureAuthoringOperationsFile": "PROCEDURE_AUTHORING_OPERATIONS.json",
        "directorDecisionFile": decision_rel,
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip",
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "directorReturnBinding": {
            "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/DD_Rank8Resource6_Director_Return01_147.zip",
            "bytes": len(raw_zip), "sha256": sha(raw_zip),
        },
        "sourceArchiveManifestMembers": 155,
        "sourceArchiveBindingMembers": 154,
        "independentAcceptanceGranted": True,
        "canonicalApplicationPerformed": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
    }

    destinations = [CANDIDATE, STAGING, BACKUP, RECEIPT_PATH, APP_FILE, OPS_FILE,
                    VALIDATION_FILE, QUEUE_AFTER, PENDING_AFTER, HANDOFF_AFTER, MANUSCRIPT,
                    SCRIPT_DEST, AUDIT / "rank8resource6_return01_147_received"]
    assert all(not path.exists() for path in destinations), "An application destination already exists; inspect before retrying."
    assert sha(INDEX.read_bytes()) == expected_index_sha, "Live index changed after preflight."
    if not apply:
        print(json.dumps({
            "status": "PREFLIGHT_PASS",
            "archiveBytes": len(raw_zip),
            "archiveSha256": sha(raw_zip),
            "directorAccepted": decision["accepted"],
            "acceptedIds": IDS,
            "before": before["authoredCounts"],
            "after": {"reviewed": 695, "pending": 153, "acceptedUnapplied": 0},
            "nextGroup": queue_before["currentPendingGroups"][1]["group"],
            "archiveMembers": 155,
            "manifestMembers": 154,
            "sourceStatusPreserved": True,
            "catalogChanged": False,
            "runtimeSelectionEnabled": False,
        }, indent=2))
        return

    # Copy and bind the exact delivered archive and source materials.
    received_dir = AUDIT / "rank8resource6_return01_147_received"
    received_dir.mkdir(parents=True)
    shutil.copyfile(RETURN_ZIP, received_dir / RETURN_ZIP.name)
    shutil.copyfile(RETURN_DELIVERY, received_dir / "DIRECTOR_RETURN_DELIVERY.json")
    assert (received_dir / RETURN_ZIP.name).read_bytes() == raw_zip
    assert (received_dir / "DIRECTOR_RETURN_DELIVERY.json").read_bytes() == delivery_bytes
    write_json(AUDIT / "GPT_DIRECTOR_DECISION_RANK8_RESOURCE6_147.json", decision)
    write_json(RECEIPT_PATH, receipt)

    STAGING.mkdir(parents=True)
    for name in copied_names:
        (STAGING / name).write_bytes(member_data[name])
    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(raw_zip)
    (STAGING / "DIRECTOR_RETURN_DELIVERY.json").write_bytes(delivery_bytes)
    (STAGING / "DIRECTOR_RETURN_MANIFEST.json").write_bytes(archive_manifest_bytes)
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(source_history_archive)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_archive)
    (STAGING / "GPT_DIRECTOR_DECISION.json").write_bytes(decision_bytes)
    (STAGING / "EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    with ZipFile(RETURN_ZIP) as archive, archive.open("CASEBOOK.json") as src, (STAGING / "CASEBOOK.json.gz").open("wb") as out:
        with gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as gz:
            shutil.copyfileobj(src, gz, length=1024 * 1024)
    with gzip.open(STAGING / "CASEBOOK.json.gz", "rb") as casebook_gz:
        restored_sha = hashlib.sha256()
        restored_size = 0
        for chunk in iter(lambda: casebook_gz.read(1024 * 1024), b""):
            restored_sha.update(chunk)
            restored_size += len(chunk)
    assert restored_size == casebook_size and restored_sha.hexdigest() == casebook_sha.hexdigest()
    write_json(STAGING / "MODEL.json", model)
    package_excluded = {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}
    package_files = []
    for path in sorted(STAGING.rglob("*")):
        if path.is_file() and path.name not in package_excluded:
            rel = path.relative_to(STAGING).as_posix()
            package_files.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())})
    package_manifest = {
        "id": "RANK8-RESOURCE6-CANDIDATE-PACKAGE-MANIFEST-147",
        "sourceArchive": {"name": RETURN_ZIP.name, "bytes": len(raw_zip), "sha256": sha(raw_zip)},
        "files": package_files,
        "excludedFromBindings": sorted(package_excluded),
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    manifest_binding = binding(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json",
                               CANDIDATE.relative_to(ROOT).as_posix() + "/CANDIDATE_PACKAGE_MANIFEST.json")
    model["candidatePackageManifestBinding"] = manifest_binding
    write_json(STAGING / "MODEL.json", model)
    model_binding = binding(STAGING / "MODEL.json", CANDIDATE.relative_to(ROOT).as_posix() + "/MODEL.json")
    shutil.move(str(STAGING), str(CANDIDATE))
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_bytes(member_data["STANDALONE_PROCEDURES.md"])
    shutil.copyfile(Path(__file__), SCRIPT_DEST)

    # Record acceptance before index mutation so the index can bind the exact receipt.
    app_receipt = {
        "id": "RANK8-RESOURCE6-APPLICATION-147",
        "recordedAtUtc": now(),
        "status": "APPLIED_SIX_AUTHORED_PROCEDURES_WITH_RETAINED_SOURCE_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue until all originally pending ordinary spell identities are applied.",
        "acceptedIds": IDS,
        "directorAcceptance": binding(RECEIPT_PATH),
        "directorDecision": binding(AUDIT / "GPT_DIRECTOR_DECISION_RANK8_RESOURCE6_147.json"),
        "directorReturn": binding(received_dir / RETURN_ZIP.name,
                                   "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/" + RETURN_ZIP.name),
        "directorReturnDelivery": binding(received_dir / "DIRECTOR_RETURN_DELIVERY.json",
                                          "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/DIRECTOR_RETURN_DELIVERY.json"),
        "indexOperations": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK8_RESOURCE6_INDEX_OPERATIONS_147.json",
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": manifest_binding,
        "indexBefore": binding(INDEX, data=before_bytes),
        "counts": {
            "before": {"reviewed": 689, "pending": 159, "acceptedUnapplied": 0},
            "after": {"reviewed": 695, "pending": 153, "acceptedUnapplied": 0},
        },
        "cases": {"main": 12, "branches": 46, "total": 58, "events": 547},
        "retainedHolds": 13,
        "sourceStatusPreservedAsBlocked": True,
        "onlyAcceptedAuthoredIdentityRowsChanged": True,
        "catalogChanged": False,
        "classAccessChanged": False,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
        "closedFeatsOrCohortsReopened": False,
    }
    write_json(APP_FILE, app_receipt)
    app_binding = binding(APP_FILE)

    # Build an exact, reversible authored-review index delta.
    after = copy.deepcopy(before)
    operations = []
    for i, old in enumerate(before["entries"]):
        sid = old["id"]
        if sid not in IDS:
            continue
        pi = IDS.index(sid)
        new = copy.deepcopy(old)
        source_ptr = old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"]
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank8resource6_reviewed_147/MODEL.json",
            "procedurePointer": f"/spells/{pi}/procedure",
            "wholeCardPointer": f"/spells/{pi}",
            "sourceCatalogWholeCardPointer": source_ptr,
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{pi}/procedure",
            "directorProcedureRecordPointer": f"/spells/{pi}/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRules",
            "manuscript": "../../../docs/spells/candidates/RANK8_RESOURCE6_REVIEWED_147.md",
            "reviewId": "RANK8-RESOURCE6-APPLICATION-147",
            "runtimeSelectionEnabled": False,
            "completeEnvelopeBinding": model_binding,
            "historicalCandidateLabelsPreserved": True,
            "casebookBinding": candidate_binding("CASEBOOK.json.gz"),
            "casebookEncoding": "gzip; exact decompression reproduces the director return CASEBOOK.json member",
            "casebookSourceArchiveMemberBinding": model["casebookSourceMemberBinding"],
            "sourceArchiveBinding": binding(received_dir / RETURN_ZIP.name,
                                             "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/" + RETURN_ZIP.name),
            "sourceConferenceArchiveBinding": binding(CANDIDATE / "SOURCE_CONFERENCE_ARCHIVE.zip",
                                                       CANDIDATE.relative_to(ROOT).as_posix() + "/SOURCE_CONFERENCE_ARCHIVE.zip"),
            "sourceCandidateBinding": binding(CANDIDATE / "SOURCE_CONFERENCE_CANDIDATE.json",
                                               CANDIDATE.relative_to(ROOT).as_posix() + "/SOURCE_CONFERENCE_CANDIDATE.json"),
            "candidatePackageManifestBinding": manifest_binding,
            "retainedHoldsBinding": candidate_binding("HOLD_REGISTER.json"),
            "procedureSourceBinding": candidate_binding("PROCEDURES.json"),
            "procedureAuthoringOperationsBinding": candidate_binding("PROCEDURE_AUTHORING_OPERATIONS.json"),
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "acceptedSharedRuleScope": scope,
            "authoredAcceptanceReceipt": binding(RECEIPT_PATH),
            "authoredApplicationReceipt": app_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": i,
                           "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][i] = new
    assert [op["identity"] for op in operations] == IDS
    app_envelope = {
        "file": "../spell_candidates/rank8resource6_reviewed_147/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "excludedPendingIds": excluded_pending,
        "authority": binding(RECEIPT_PATH),
        "applicationReceipt": APP_PATH,
        "sourceArchive": binding(received_dir / RETURN_ZIP.name,
                                  "docs/audit/2026-10-08/full-game/director-spell-review-129/rank8resource6_return01_147_received/" + RETURN_ZIP.name),
        "sourceConferenceArchive": binding(CANDIDATE / "SOURCE_CONFERENCE_ARCHIVE.zip",
                                            CANDIDATE.relative_to(ROOT).as_posix() + "/SOURCE_CONFERENCE_ARCHIVE.zip"),
        "sourceCandidate": binding(CANDIDATE / "SOURCE_CONFERENCE_CANDIDATE.json",
                                   CANDIDATE.relative_to(ROOT).as_posix() + "/SOURCE_CONFERENCE_CANDIDATE.json"),
        "casebookBinding": candidate_binding("CASEBOOK.json.gz"),
        "casebookSourceArchiveMemberBinding": model["casebookSourceMemberBinding"],
        "holdsBinding": candidate_binding("HOLD_REGISTER.json"),
        "procedureSourceBinding": candidate_binding("PROCEDURES.json"),
        "procedureAuthoringOperationsBinding": candidate_binding("PROCEDURE_AUTHORING_OPERATIONS.json"),
        "candidatePackageManifestBinding": manifest_binding,
        "scope": scope,
        "runtimeSelectionEnabled": False,
    }
    after["additionalStandaloneEnvelopes"].append(app_envelope)
    after["authoredCounts"] = {"reviewed": 695, "pending": 153}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 419
    pending_ids = {entry["id"] for entry in after["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert len(pending_ids) == 153 and not (pending_ids & set(IDS))
    assert after["sourceCatalogSha256"] == before["sourceCatalogSha256"]
    assert after["standaloneEnvelopeSha256"] == before["standaloneEnvelopeSha256"]
    reverse = copy.deepcopy(after)
    for operation in operations:
        reverse["entries"][operation["index"]] = operation["before"]
    reverse["additionalStandaloneEnvelopes"] = reverse["additionalStandaloneEnvelopes"][:-1]
    reverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    reverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert reverse == before
    after_bytes = json_bytes(after)
    assert not BACKUP.exists() and not OPS_FILE.exists()
    BACKUP.write_bytes(before_bytes)
    ops_doc = {
        "id": "RANK8-RESOURCE6-INDEX-OPERATIONS-147",
        "before": binding(BACKUP),
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"restores": "the exact six prior entries, aggregate counts and additionalStandaloneEnvelopes tail", "semanticExact": reverse == before},
        "onlyIdentityIds": IDS,
    }
    temp = INDEX.with_suffix(".json.application147.tmp")
    temp.write_bytes(after_bytes)
    os.replace(temp, INDEX)
    assert INDEX.read_bytes() == after_bytes
    ops_doc["after"] = binding(INDEX)
    write_json(OPS_FILE, ops_doc)

    # Refresh current queue, pending audit and handoff from the 141 authoritative ordering.
    groups = []
    for group in queue_before["currentPendingGroups"]:
        keep = [sid for sid in group["pendingIds"] if sid in pending_ids]
        if keep:
            updated = copy.deepcopy(group)
            updated["pendingIds"] = keep
            updated["pendingCount"] = len(keep)
            groups.append(updated)
    assert groups and groups[0]["group"] == "rank8-control5"
    authority = copy.deepcopy(queue_before["currentAuthority"])
    authority.update({"reviewedApplied": 695, "pending": 153, "acceptedUnapplied": 0,
                      "completeReviewedStandaloneProcedures": 419})
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-147",
        "recordedAtUtc": now(),
        "currentAuthority": authority,
        "currentPendingGroups": groups,
        "nextSuggestedGroups": groups[:5],
        "nextGroup": groups[0],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": len(IDS), "applicationReceipt": APP_PATH},
        "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 153, "indexSha256": sha(INDEX.read_bytes())},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"],
                 "archive": groups[0]["archive"], "candidate": groups[0]["candidate"]},
    })
    write_json(QUEUE_AFTER, queue_after)
    pending_after = {
        "id": "CURRENT153-PENDING-IDENTITY-AUDIT-147",
        "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": binding(INDEX),
        "catalogBinding": binding(CATALOG),
        "authoredCounts": after["authoredCounts"],
        "pendingCount": 153,
        "pendingIds": sorted(pending_ids),
        "allPendingExistInSourceCatalog": all(any(s.get("id") == sid for s in catalog["spells"]) for sid in pending_ids),
        "closed335AndCompletedCohortsReopened": False,
        "acceptedUnapplied": 0,
    }
    assert pending_after["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_after)
    handoff_after = copy.deepcopy(handoff_before)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-147",
        "recordedAtUtc": now(),
        "status": "RANK8_RESOURCE6_APPLIED_NEXT_153_PENDING",
        "currentAuthority": authority,
        "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "pendingIdentityAudit": {"id": pending_after["id"], "path": PENDING_AFTER.name,
                                 "pendingCount": 153, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 6, "applicationReceipt": APP_PATH},
        "nextGroup": groups[0]["group"],
        "resumePriority": "Continue in current source queue order; refresh the next group packet against the live 695/153 authority, then independently audit and apply only after director acceptance.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"],
                                "archive": groups[0]["archive"],
                                "request": "Prepare a fresh request bound to the current 695/153 authority before director review."},
    })
    write_json(HANDOFF_AFTER, handoff_after)

    # The separate validation record binds the final index and operation log without a hash cycle.
    checks = {
        "directorAcceptedExactReturn147": decision["accepted"] and decision["acceptedArchive"]["sha256"] == sha(raw_zip),
        "returnArchiveAndDeliveryByteExact": len(raw_zip) == delivery["bytes"] and delivery["sha256"] == sha(raw_zip),
        "archiveCrcsClean": True,
        "exact155MemberAllowlist": len(names) == 155,
        "all154BoundMemberHashesVerified": len(archive_manifest["members"]) == 154,
        "currentIndexAndCatalogBindingsExact": sha(before_bytes) == expected_index_sha and sha(catalog_bytes) == expected_catalog_sha,
        "currentQueueAndHandoffSnapshotsExact": True,
        "sourceCandidateAndConferenceArchiveByteExact": True,
        "sixProceduresMatchAcceptedIds": [row["id"] for row in procedures_doc["procedures"]] == IDS,
        "sixOperationRecordsMatchAcceptedIds": [row["id"] for row in operations_doc] == IDS,
        "allSixProcedurePayloadsPresent": all(row["completeProposedProcedure"] for row in procedures_doc["procedures"]),
        "caseAndEventCountsBound": counts_doc["cases"]["total"] == 58 and counts_doc["events"] == 547,
        "all13HoldsRetained": len(hold_doc["holds"]) == 13,
        "sixRowsWerePendingBeforeApplication": all(rows[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS),
        "sixIdsRemovedFromPending": not (pending_ids & set(IDS)),
        "reviewedCountAdvancedBySix": after["authoredCounts"] == {"reviewed": 695, "pending": 153},
        "standaloneProcedureCountAdvancedBySix": after["representationCounts"]["completeReviewedStandaloneProcedures"] == 419,
        "inverseRestoresExactPriorSemanticIndex": reverse == before,
        "allOtherIndexRowsPreserved": all(after["entries"][i] == before["entries"][i] for i in range(len(before["entries"])) if before["entries"][i]["id"] not in IDS),
        "sourceStatusPreservedAsBlocked": all(after["entries"][next(i for i,e in enumerate(after["entries"]) if e["id"] == sid)]["sourceStatus"] == "blocked-pending-operational-review" for sid in IDS),
        "catalogHashUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "priorStandaloneEnvelopeHashUnchanged": after["standaloneEnvelopeSha256"] == before["standaloneEnvelopeSha256"],
        "all153PendingIdsRemainInSourceCatalog": pending_after["allPendingExistInSourceCatalog"],
        "closedCohortsRemainClosed": not pending_after["closed335AndCompletedCohortsReopened"],
        "runtimeSelectionRemainsDisabled": not any(after["entries"][next(i for i,e in enumerate(after["entries"]) if e["id"] == sid)]["runtimeSelectionEnabled"] for sid in IDS),
        "acceptedUnappliedRemainsZero": pending_after["acceptedUnapplied"] == 0,
        "casebookGzipRoundTripExact": restored_size == casebook_size and restored_sha.hexdigest() == casebook_sha.hexdigest(),
    }
    assert all(checks.values()), {k: v for k, v in checks.items() if not v}
    validation = {
        "id": "RANK8-RESOURCE6-APPLICATION-VALIDATION-147",
        "status": "PASS",
        "checksPassed": sum(checks.values()),
        "checksFailed": 0,
        "checks": checks,
        "beforeIndex": binding(BACKUP),
        "afterIndex": binding(INDEX),
        "changedIdentityIds": IDS,
        "onlySixPendingEntriesChanged": True,
        "allOtherEntriesAndPriorStandaloneEnvelopesPreserved": True,
        "authoredCounts": after["authoredCounts"],
        "representationCounts": after["representationCounts"],
        "sourceStatusStillBlockedForAllSix": all(after["entries"][i]["sourceStatus"] == "blocked-pending-operational-review"
                                                   for i in [next(i for i, e in enumerate(after["entries"]) if e["id"] == sid) for sid in IDS]),
        "sourceCatalogHashUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "standaloneEnvelopeHashUnchanged": after["standaloneEnvelopeSha256"] == before["standaloneEnvelopeSha256"],
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": reverse == before,
        "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "exactReturnArchiveAndAll154ManifestBindingsPassed": True,
        "exactCurrent689159AuthoritySnapshotsPassed": True,
        "acceptedCases": counts_doc["cases"],
        "retainedHoldRecords": counts_doc["holds"]["returnHoldRecords"],
        "acceptedUnapplied": 0,
        "nextGroup": groups[0]["group"],
        "nextPendingCount": groups[0]["pendingCount"],
        "applicationReceipt": binding(APP_FILE),
        "directorAcceptanceReceipt": binding(RECEIPT_PATH),
    }
    write_json(VALIDATION_FILE, validation)
    # Update the navigational top block while retaining the full historical text below it.
    start_page = ROOT / "START_HERE.md"
    current_start = start_page.read_text(encoding="utf-8-sig")
    marker = "**Latest checkpoint: [128]"
    historical_start = current_start[current_start.find(marker):] if marker in current_start else current_start
    top = (
        "# Active ordinary spell review147 — Calibration review part6\n\n"
        "Return147 is director accepted and applied for six identities in the authored procedure index: "
        "**695 applied-reviewed / 153 pending / 0 accepted-unapplied**. The director independently passed "
        "4,877 checks with zero failures; the exact 155-member return archive and 13 retained holds are bound. "
        "Runtime selection, implementation, human play, balance, cosmology, release and domain-closure approval remain separate.\n\n"
        "Continue in the current source queue with **rank8-control5** (five identities), preparing a fresh packet "
        "against the 695/153 authority. Apply only after independent exact review and director acceptance. Preserve "
        "the closed feat335 and completed spell cohorts.\n\n"
        "Read [CURRENT-HANDOFF-147](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_147.json), "
        "[the 153-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT153_PENDING_IDENTITY_AUDIT_147.json), "
        "and [the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK8_RESOURCE6_APPLICATION_VALIDATION_147.json).\n\n"
    )
    if marker in current_start:
        start_page.write_text(top + historical_start, encoding="utf-8", newline="\n")

    assert CATALOG.read_bytes() == catalog_bytes
    assert read_json(INDEX)["authoredCounts"] == {"reviewed": 695, "pending": 153}
    assert read_json(INDEX)["representationCounts"]["completeReviewedStandaloneProcedures"] == 419
    assert len({entry["id"] for entry in read_json(INDEX)["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}) == 153
    with gzip.open(CANDIDATE / "CASEBOOK.json.gz", "rb") as restored:
        restored_sha = hashlib.sha256()
        restored_size = 0
        for chunk in iter(lambda: restored.read(1024 * 1024), b""):
            restored_sha.update(chunk)
            restored_size += len(chunk)
    assert restored_size == casebook_size and restored_sha.hexdigest() == casebook_sha.hexdigest()
    print(json.dumps({
        "status": "APPLIED_AND_VALIDATED",
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "currentCounts": after["authoredCounts"],
        "representationCounts": after["representationCounts"],
        "directorChecks": decision["verification"],
        "pendingAudit": {"count": len(pending_ids), "nextGroup": groups[0]["group"],
                         "nextBatchCount": groups[0]["pendingCount"], "nextIds": groups[0]["pendingIds"]},
        "catalogUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "indexBytes": INDEX.stat().st_size,
        "indexSha256": sha(INDEX.read_bytes()),
        "returnArchive": binding(received_dir / RETURN_ZIP.name),
    }, indent=2))


if __name__ == "__main__":
    main("--apply" in sys.argv)
