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


ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
IDS = ["erase-mind", "feeblemind", "mass-dominate", "mind-ravel"]
REVIEW_ID = "RANK8-MEMORY-CONTROL4-EXACT-AUTHORED-ACCEPTANCE-150"
APP_ID = "RANK8-MEMORY-CONTROL4-APPLICATION-150"
ARCHIVE_NAME = "DD_Rank8_MemoryControl4_Director_Return150.zip"
DELIVERY_NAME = "DD_Rank8_MemoryControl4_Director_Return150_DELIVERY.json"
RECEIVED = AUDIT / "rank8memorycontrol4_return150_received"
ARCHIVE = RECEIVED / ARCHIVE_NAME
DELIVERY = RECEIVED / "DIRECTOR_RETURN_DELIVERY.json"
DOWNLOADS = Path.home() / "Downloads"
INPUT_ARCHIVE = DOWNLOADS / ARCHIVE_NAME
INPUT_DELIVERY = DOWNLOADS / DELIVERY_NAME
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_149 = AUDIT / "CURRENT_SPELL_QUEUE_149.json"
PENDING_149 = AUDIT / "CURRENT143_PENDING_IDENTITY_AUDIT_149.json"
HANDOFF_149 = AUDIT / "CURRENT_HANDOFF_149.json"
QUEUE_150 = AUDIT / "CURRENT_SPELL_QUEUE_150.json"
PENDING_150 = AUDIT / "CURRENT139_PENDING_IDENTITY_AUDIT_150.json"
HANDOFF_150 = AUDIT / "CURRENT_HANDOFF_150.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_MEMORY_CONTROL4_150.json"
RECEIPT = AUDIT / "MEMORY_CONTROL4_EXACT_ACCEPTANCE_150.json"
APPLICATION = AUDIT / "MEMORY_CONTROL4_APPLICATION_150.json"
OPERATIONS = AUDIT / "MEMORY_CONTROL4_INDEX_OPERATIONS_150.json"
VALIDATION = AUDIT / "MEMORY_CONTROL4_APPLICATION_VALIDATION_150.json"
BACKUP = AUDIT / "authored_review_index.before_memory_control4_150.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8memorycontrol4_reviewed_150"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_MEMORY_CONTROL4_REVIEWED_150.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_150.md"
START = ROOT / "START_HERE.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


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


def safe_archive_members(archive: ZipFile, expected_count: int) -> list[str]:
    names = archive.namelist()
    assert len(names) == len(set(names)) == expected_count
    for name in names:
        path = PurePosixPath(name)
        assert not path.is_absolute() and ".." not in path.parts and "\\" not in name
        assert name and not name.startswith("/")
    return names


def validate_input():
    input_archive = ARCHIVE if ARCHIVE.exists() else INPUT_ARCHIVE
    input_delivery = DELIVERY if DELIVERY.exists() else INPUT_DELIVERY
    assert input_archive.is_file() and input_delivery.is_file(), "Accepted Return150 archive or delivery file is missing."
    archive_bytes = input_archive.read_bytes()
    delivery_bytes = input_delivery.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    assert len(archive_bytes) == 15_485_461
    assert sha(archive_bytes) == "2b5e9d2621b682116ce0064e659e5ff1c96d1041a8bd7174db1debe71ccab17d"
    assert delivery["id"] == "MEMORY4-DIRECTOR-RETURN150-DELIVERY"
    assert delivery["archive"]["fileName"] == ARCHIVE_NAME
    assert delivery["archive"]["bytes"] == len(archive_bytes) and delivery["archive"]["sha256"] == sha(archive_bytes)
    assert delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS
    assert delivery["inputAuthority"] == {"reviewedApplied": 705, "pending": 143, "acceptedUnapplied": 0}
    assert delivery["canonicalIndexCatalogModified"] is False
    assert delivery["archive"]["memberCount"] == 186
    assert delivery["staticDataChecksPassed"] == 29_730 and delivery["failedChecks"] == 0
    assert delivery["localPackageMemberRoundTripChecksPassed"] == 748
    assert delivery["blockingDefects"] == [] and delivery["all13HoldsRetained"] is True
    assert delivery["counts"] == {
        "procedures": 4, "conferenceQuestions": 21, "originalIdentityQuestions": 4,
        "futureObligations": 6, "mainCases": 8, "branches": 65, "cases": 73,
        "events": 420, "eventOperations": 1680, "proposalOperations": 16,
        "holds": 13, "wholeCaseHeld": 59,
    }
    assert delivery["sourceArchive"]["sha256"] == "a78b83530c160679f890ed49a827ce8c66fbc96a45add8f59d8df9c3da0ad2f8"
    output_paths = [
        RECEIVED, CANDIDATE, STAGING, MANUSCRIPT, DECISION, RECEIPT, APPLICATION,
        OPERATIONS, VALIDATION, BACKUP, QUEUE_150, PENDING_150, HANDOFF_150, SNAPSHOT,
    ]
    existing_outputs = [str(path) for path in output_paths if path.exists()]
    assert not existing_outputs, f"Return150 output paths already exist; inspect before retrying: {existing_outputs}"

    with ZipFile(input_archive) as archive:
        names = safe_archive_members(archive, 186)
        assert "STANDALONE_PROCEDURES.md" in names
        assert archive.testzip() is None
        member_manifest_raw = archive.read("MEMBER_MANIFEST.json")
        member_manifest = json.loads(member_manifest_raw)
        manifest_binding = delivery["memberManifest"]
        assert len(member_manifest_raw) == manifest_binding["bytes"] == 58_722
        assert sha(member_manifest_raw) == manifest_binding["sha256"] == "a1a4e512e137c79fcec4635eac7e8c927164116a85fa64b197256a9d03a27feb"
        assert f"{__import__('zlib').crc32(member_manifest_raw):08x}" == manifest_binding["CRC32"]
        assert member_manifest["archiveMemberCount"] == 186
        assert set(names) == set(member_manifest["allowlist"])
        assert member_manifest["hiddenOrTemporaryMembers"] is False
        payload_rows = {row["path"]: row for row in member_manifest["payloadMembers"]}
        assert set(payload_rows) == set(names) - {"MEMBER_MANIFEST.json"}
        for name, row in payload_rows.items():
            raw = archive.read(name)
            info = archive.getinfo(name)
            assert len(raw) == info.file_size == row["bytes"]
            assert sha(raw) == row["sha256"]
            assert f"{info.CRC:08x}" == row["CRC32"].lower()

        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        model = json.loads(archive.read("MODEL.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        validation = json.loads(archive.read("VALIDATION.json"))
        failure = json.loads(archive.read("INDEPENDENT_FAILURE_CHECK.json"))
        dispositions = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        holds = json.loads(archive.read("HOLDS.json"))
        proposal_ops = json.loads(archive.read("PROPOSAL_OPERATIONS.json"))
        source_verification = json.loads(archive.read("SOURCE_VERIFICATION.json"))
        assert decision["accepted"] is True and decision["applied"] is False
        assert decision["acceptedIds"] == IDS and decision["rejectedIds"] == []
        assert decision["blockingDefects"] == [] and decision["canonicalFilesModified"] is False
        assert decision["closedCohortsReopened"] is False
        assert decision["dataChecksPassed"] == 29_730
        assert decision["inputAuthority"] == {
            "reviewedApplied": 705, "pending": 143, "acceptedUnapplied": 0,
            "completeReviewedStandaloneProcedures": 429, "canonicalFilesModified": False,
        }
        assert model["accepted"] is True and model["applied"] is False and model["noCanonicalMutation"] is True
        assert model["authority"] == decision["inputAuthority"]
        assert [spell["id"] for spell in model["spells"]] == IDS
        assert all(spell["runtimeSelectionEnabled"] is False for spell in model["spells"])
        assert counts == delivery["counts"]
        assert validation["passed"] is True and validation["checkCount"] == 29_730 and validation["failedCount"] == 0
        assert len(validation["checks"]) == 29_730 and all(check["passed"] for check in validation["checks"])
        assert failure["passed"] is True and failure["blockingDefects"] == []
        assert len(dispositions["conferenceQuestions"]) == 21
        assert len(dispositions["originalIdentityQuestions"]) == 4
        assert len(dispositions["futureObligations"]) == 6
        assert holds["allRetained"] is True and len(holds["holds"]) == 13
        assert isinstance(proposal_ops, list) and len(proposal_ops) == 4
        assert sum(len(op["forward"]) + len(op["inverse"]) for op in proposal_ops) == 16
        assert all(op["before"]["applied"] is False and op["after"]["applied"] is False for op in proposal_ops)
        assert all(op.get("canonicalIndexMutation") is not True for op in proposal_ops)
        assert source_verification["boundSourceCount"] == 79 and source_verification["all79BoundSourceFilesVerify"] is True
        assert source_verification["liveAuthorityUnchanged"]["reviewedApplied"] == 705
        assert source_verification["liveAuthorityUnchanged"]["pending"] == 143
        assert source_verification["liveAuthorityUnchanged"]["acceptedUnapplied"] == 0
        assert source_verification["liveAuthorityUnchanged"]["index"]["sha256"] == sha(INDEX.read_bytes())
        assert source_verification["liveAuthorityUnchanged"]["catalog"]["sha256"] == sha(CATALOG.read_bytes())

    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = json.loads(catalog_bytes.decode("utf-8-sig"))
    queue = read_json(QUEUE_149)
    pending = read_json(PENDING_149)
    handoff = read_json(HANDOFF_149)
    assert sha(before_bytes) == "8fd9f6c7708a38d3cb2885b415e5d470935d7aa2d89221aa5c4f65964c884a18"
    assert before["authoredCounts"] == {"reviewed": 705, "pending": 143}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 429
    assert pending["pendingCount"] == 143 and pending["indexBinding"]["sha256"] == sha(before_bytes)
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert queue["currentAuthority"]["reviewedApplied"] == 705 and queue["currentAuthority"]["pending"] == 143
    assert queue["currentPendingGroups"][0]["group"] == "rank8-memory-control4"
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS

    with ZipFile(input_archive) as archive:
        source_index_paths = [name for name in archive.namelist() if name.startswith("evidence/source02/sources/") and name.endswith("/spell_playtests/authored_review_index.json")]
        source_catalog_paths = [name for name in archive.namelist() if name.startswith("evidence/source02/sources/") and name.endswith("/spell_playtests/catalog.json")]
        assert len(source_index_paths) == len(source_catalog_paths) == 1
        assert archive.read(source_index_paths[0]) == before_bytes
        assert json.loads(archive.read(source_catalog_paths[0]).decode("utf-8-sig")) == catalog

    rows = {row["id"]: row for row in before["entries"]}
    current_pending = {entry["id"] for entry in before["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert len(rows) == 848 and len(current_pending) == 143 and set(pending["pendingIds"]) == current_pending
    assert set(IDS) <= current_pending
    return {
        "inputArchive": input_archive, "inputDelivery": input_delivery,
        "archiveBytes": archive_bytes, "deliveryBytes": delivery_bytes,
        "directorDecision": decision, "directorModel": model, "counts": counts,
        "dispositions": dispositions, "holds": holds, "proposalOperations": proposal_ops,
        "beforeBytes": before_bytes, "catalogBytes": catalog_bytes, "before": before,
        "catalog": catalog, "queue": queue, "pendingIds": current_pending,
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
    catalog = data["catalog"]
    model = data["directorModel"]
    decision = data["directorDecision"]
    counts = data["counts"]
    dispositions = data["dispositions"]
    excluded_pending = sorted(data["pendingIds"] - set(IDS))

    decision_record = {
        "id": "GPT-DIRECTOR-DECISION-MEMORY-CONTROL4-150",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": decision["id"], "accepted": True, "appliedAtDecision": False,
        "acceptedIds": IDS, "rejectedIds": [], "remainingBlockingDefects": [],
        "verification": {
            "independentStaticChecksPassed": 29_730, "independentStaticFailures": 0,
            "packageMemberChecksPassed": 748, "packageMemberFailures": 0,
            "archiveMembers": 186, "cases": 73, "events": 420,
            "eventOperations": 1680, "holds": 13, "wholeCaseHeld": 59,
        },
        "acceptedArchive": {"name": ARCHIVE_NAME, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "scope": decision["decision"], "holdScope": "All 13 indexed holds and each source/access/content/event/roster/companion/physical/defense/restore/device/runtime/cosmology/release qualification remain. No missing event ledger or unreviewed CR profile is supplied by this authored acceptance.",
        "excludedClaims": {
            "runtime": False, "humanPlay": False, "balance": False, "cosmology": False,
            "domainClosure": False, "release": False, "canonicalApplication": False,
            "reopenedAppliedCohort": False,
        },
        "directorMadeNoLocalChanges": True,
    }
    decision_record_bytes = json_bytes(decision_record)
    receipt = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision_record,
        "directorReturn": {"path": f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/{ARCHIVE_NAME}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "directorReturnDelivery": {"path": f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/DIRECTOR_RETURN_DELIVERY.json", "bytes": len(delivery_bytes), "sha256": sha(delivery_bytes)},
        "acceptedIds": IDS,
        "countsBefore": {"reviewed": 705, "pending": 143, "acceptedUnapplied": 0},
        "countsAfter": {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0},
        "completeReviewedStandaloneProceduresBefore": 429,
        "completeReviewedStandaloneProceduresAfter": 433,
        "acceptedCases": counts["cases"], "acceptedEvents": counts["events"],
        "eventOperations": counts["eventOperations"], "retainedHolds": 13,
        "wholeCaseHeld": counts["wholeCaseHeld"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all four identities; authored procedure review only.",
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "releaseApproved": False, "canonicalApplicationPerformed": False,
    }
    receipt_bytes = json_bytes(receipt)
    receipt_binding = binding(RECEIPT, raw=receipt_bytes)

    STAGING.mkdir(parents=True)
    (STAGING / "DIRECTOR_RETURN/PROCEDURES").mkdir(parents=True)
    with ZipFile(data["inputArchive"]) as archive:
        member_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        for name in archive.namelist():
            if name == "CASEBOOK.json" or name.startswith("procedures/") or "/" in name:
                continue
            path = PurePosixPath(name)
            dest = STAGING / "DIRECTOR_RETURN" / Path(*path.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name, "r") as src, dest.open("wb") as out:
                shutil.copyfileobj(src, out)
        for name in archive.namelist():
            if not name.startswith("procedures/") or not name.endswith(".json"):
                continue
            path = PurePosixPath(name)
            dest = STAGING / "DIRECTOR_RETURN/PROCEDURES" / Path(*path.parts[1:])
            dest.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name, "r") as src, dest.open("wb") as out:
                shutil.copyfileobj(src, out)
        casebook_info = archive.getinfo("CASEBOOK.json")
        casebook_row = next(row for row in member_manifest["payloadMembers"] if row["path"] == "CASEBOOK.json")
        casebook_path = STAGING / "CASEBOOK.json.gz"
        with archive.open("CASEBOOK.json", "r") as source, casebook_path.open("wb") as output:
            with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
                shutil.copyfileobj(source, compressed)
    with gzip.open(casebook_path, "rb") as compressed:
        casebook_hash = hashlib.sha256()
        casebook_size = 0
        for chunk in iter(lambda: compressed.read(1024 * 1024), b""):
            casebook_hash.update(chunk)
            casebook_size += len(chunk)
    assert casebook_size == casebook_row["bytes"] == casebook_info.file_size
    assert casebook_hash.hexdigest() == casebook_row["sha256"]

    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "DIRECTOR_RETURN_DELIVERY.json").write_bytes(delivery_bytes)
    (STAGING / "GPT_DIRECTOR_DECISION.json").write_bytes(decision_record_bytes)
    (STAGING / "EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    with ZipFile(data["inputArchive"]) as archive:
        source_archive_bytes = archive.read("history/DD_Rank8_Memory_Control_4_Source_Conference_02.zip")
        source_candidate_bytes = archive.read("evidence/source02/CANDIDATE.json")
        standalone_bytes = archive.read("STANDALONE_PROCEDURES.md")
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(source_archive_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_bytes)
    (STAGING / "STANDALONE_PROCEDURES.md").write_bytes(standalone_bytes)

    spells = []
    for i, proc in enumerate(model["spells"]):
        old = next(row for row in before["entries"] if row["id"] == proc["id"])
        native = proc["nativeCardAndAccessUnchanged"]
        assert native["id"] == proc["id"] and native["name"] == old["name"]
        spells.append({
            "id": proc["id"], "name": native["name"],
            "procedure": copy.deepcopy(proc["procedure"]),
            "directorProcedureRecord": copy.deepcopy(proc),
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "sourceRecordPointer": proc.get("sourceRecordPointer"),
            "runtimeSelectionEnabled": False,
        })
    normalized_model = {
        "schemaVersion": 3, "moduleId": "rank8memorycontrol4-reviewed-150",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Only the four director-accepted Memory/Control4 authored procedures, exact dispositions and bound static evidence are recorded. Native spell cards, class access, source status and catalog bytes remain unchanged. All 13 qualifications remain, including 59 whole-case holds. Proposal operations remain unapplied. Runtime selection stays disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "sharedRules": {"id": "MEMORY-CONTROL4-COMMON-150", "rules": copy.deepcopy(model["sharedRules"]), "scope": "These four identities only."},
        "spells": spells,
        "sourceLinkedCounterpartsUnchanged": model["sourceLinkedCounterpartsUnchanged"],
        "currentAcceptedInterfacesUnchanged": model["currentAcceptedInterfacesUnchanged"],
        "closedComparisonGroupsUnchanged": model["closedComparisonGroupsUnchanged"],
        "questionDispositions": dispositions, "returnCounts": counts,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; decompression is byte-identical to the CASEBOOK.json member of DIRECTOR_RETURN_ARCHIVE.zip",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_row["bytes"], "sha256": casebook_row["sha256"]},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip", "directorReturnDelivery": "DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip", "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "STANDALONE_PROCEDURES.md", "directorDecisionFile": "GPT_DIRECTOR_DECISION.json",
        "directorReturnBinding": {"path": f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/{ARCHIVE_NAME}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "sourceArchiveMemberCount": 186, "independentAcceptanceGranted": True,
        "canonicalApplicationPerformed": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False, "releaseApproved": False,
    }

    package_files = []
    for path in sorted(STAGING.rglob("*")):
        if path.is_file() and path.relative_to(STAGING).as_posix() not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}:
            raw = path.read_bytes()
            package_files.append({"path": path.relative_to(STAGING).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-MEMORY-CONTROL4-CANDIDATE-PACKAGE-MANIFEST-150",
        "sourceArchive": {"name": ARCHIVE_NAME, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "files": package_files, "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    package_binding = binding(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")
    normalized_model["candidatePackageManifestBinding"] = package_binding
    write_json(STAGING / "MODEL.json", normalized_model)
    model_binding = binding(STAGING / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json")
    casebook_binding = binding(STAGING / "CASEBOOK.json.gz", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    archive_binding = binding(ARCHIVE, f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/{ARCHIVE_NAME}", archive_bytes)
    source_archive_binding = binding(STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip", f"{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_ARCHIVE.zip")
    source_candidate_binding = binding(STAGING / "SOURCE_CONFERENCE_CANDIDATE.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_CANDIDATE.json")
    holds_binding = binding(STAGING / "DIRECTOR_RETURN/HOLDS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLDS.json")
    proposal_binding = binding(STAGING / "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json")
    procedure_source_binding = binding(STAGING / "DIRECTOR_RETURN/MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/MODEL.json")

    RECEIVED.mkdir(parents=True)
    shutil.copyfile(data["inputArchive"], ARCHIVE)
    shutil.copyfile(data["inputDelivery"], DELIVERY)
    assert ARCHIVE.read_bytes() == archive_bytes and DELIVERY.read_bytes() == delivery_bytes
    write_json(DECISION, decision_record)
    write_json(RECEIPT, receipt)
    os.replace(STAGING, CANDIDATE)
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_bytes(standalone_bytes)

    app = {
        "id": APP_ID, "recordedAtUtc": now(), "status": "APPLIED_FOUR_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue through the remaining pending ordinary spell identities.",
        "acceptedIds": IDS, "directorAcceptance": binding(RECEIPT), "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "directorReturnDelivery": binding(DELIVERY, f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/DIRECTOR_RETURN_DELIVERY.json", delivery_bytes),
        "candidateEnvelope": model_binding, "candidatePackageManifest": package_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {"reviewed": 705, "pending": 143, "acceptedUnapplied": 0}, "after": {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0}},
        "completeReviewedStandaloneProcedures": {"before": 429, "after": 433},
        "cases": 73, "events": 420, "eventOperations": 1680,
        "retainedHolds": 13, "wholeCaseHeld": 59,
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
            "procedureFile": "../spell_candidates/rank8memorycontrol4_reviewed_150/MODEL.json",
            "procedurePointer": f"/spells/{n}/procedure", "wholeCardPointer": f"/spells/{n}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id", "procedureTextPointer": f"/spells/{n}/procedure",
            "directorProcedureRecordPointer": f"/spells/{n}/directorProcedureRecord", "sharedRulesPointer": "/sharedRules",
            "manuscript": "../../../docs/spells/candidates/RANK8_MEMORY_CONTROL4_REVIEWED_150.md",
            "reviewId": APP_ID, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(), "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces the director return CASEBOOK.json member",
            "casebookSourceArchiveMemberBinding": normalized_model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": archive_binding, "sourceConferenceArchiveBinding": source_archive_binding,
            "sourceCandidateBinding": source_candidate_binding, "candidatePackageManifestBinding": package_binding,
            "retainedHoldsBinding": holds_binding, "procedureSourceBinding": procedure_source_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": receipt["decision"],
            "authoredAcceptanceReceipt": binding(RECEIPT), "authoredApplicationReceipt": app_binding,
        })
        operations.append({"op": "replace-entry", "identity": sid, "index": i, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][i] = new
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank8memorycontrol4_reviewed_150/MODEL.json", "binding": model_binding,
        "reviewId": REVIEW_ID, "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "authority": binding(RECEIPT), "applicationReceipt": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APPLICATION.name}",
        "sourceArchive": archive_binding, "casebookBinding": casebook_binding, "holdsBinding": holds_binding,
        "candidatePackageManifestBinding": package_binding, "scope": receipt["decision"], "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 709, "pending": 139}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 433
    pending_after = {entry["id"] for entry in after["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 4 and len(pending_after) == 139
    assert pending_after == data["pendingIds"] - set(IDS)

    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    ops_doc = {
        "id": "MEMORY-CONTROL4-INDEX-OPERATIONS-150",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "four prior entries, aggregate counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    BACKUP.write_bytes(before_bytes)
    write_json(APPLICATION, app)
    write_json(OPERATIONS, ops_doc)
    tmp_index = INDEX.with_suffix(".json.application150.tmp")
    tmp_index.write_bytes(after_bytes)
    os.replace(tmp_index, INDEX)
    assert INDEX.read_bytes() == after_bytes and CATALOG.read_bytes() == catalog_bytes

    authority = copy.deepcopy(queue["currentAuthority"])
    authority.update({"reviewedApplied": 709, "pending": 139, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 433})
    groups = []
    for group in queue["currentPendingGroups"]:
        remaining = [sid for sid in group["pendingIds"] if sid in pending_after]
        if remaining:
            item = copy.deepcopy(group)
            item["pendingIds"] = remaining
            item["pendingCount"] = len(remaining)
            item["freshPacketRequiredForCurrentAuthority"] = True
            groups.append(item)
    assert groups[0]["group"] == "rank8-life-form4" and sum(g["pendingCount"] for g in groups) == 139
    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-150", "recordedAtUtc": now(), "currentAuthority": authority,
        "currentPendingGroups": groups, "nextSuggestedGroups": groups[:5], "nextGroup": groups[0]["group"],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_150.name, "pending": 139, "sha256": sha(json_bytes({"pendingIds": sorted(pending_after)}))},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "archive": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True},
    })
    pending_doc = {
        "id": "CURRENT139-PENDING-IDENTITY-AUDIT-150", "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": binding(INDEX),
        "catalogBinding": binding(CATALOG), "authoredCounts": after["authoredCounts"], "pendingCount": 139,
        "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(row.get("id") == sid for row in catalog["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(QUEUE_150, queue_after)
    write_json(PENDING_150, pending_doc)
    queue_after["pendingIdentityAudit"]["sha256"] = sha(PENDING_150.read_bytes())
    queue_after["pendingIdentityAudit"]["path"] = PENDING_150.name
    write_json(QUEUE_150, queue_after)
    handoff = copy.deepcopy(read_json(HANDOFF_149))
    handoff.update({
        "id": "CURRENT-HANDOFF-150", "recordedAtUtc": now(), "status": "RANK8_MEMORY_CONTROL4_APPLIED_NEXT_139_PENDING",
        "currentAuthority": authority, "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_150.name, "pendingCount": 139, "sha256": sha(PENDING_150.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4,
            "applicationReceipt": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APPLICATION.name}",
            "directorAcceptance": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}"},
        "nextGroup": groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed16/72, feat335, or any accepted/applied spell cohort. Runtime, source/content/access and domain holds remain separately tracked.",
        "resumePriority": "Prepare a fresh Rank8 Life/Form4 packet against 709/139 and submit it to Calibration review part 6. Apply only after exact GPT director acceptance.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True, "request": "Prepare and submit a fresh request bound to current 709/139 authority before director review."},
    })
    write_json(HANDOFF_150, handoff)

    validation_record = {
        "id": "MEMORY-CONTROL4-APPLICATION-VALIDATION-150", "status": "PASS", "checksPassed": 24, "checksFailed": 0,
        "checks": [
            "Return150 archive and delivery hashes match sealed bindings",
            "all 186 members pass size, SHA-256, CRC, allowlist and extracted-byte checks",
            "exact director acceptance for four indexed pending IDs; no director application",
            "29,730 independent static checks and 748 package round-trip checks pass with zero failures",
            "all 13 qualifications retained, including 59 whole-case holds",
            "four proposal envelopes and all 16 forward/inverse proposal operations remain unapplied",
            "source index is byte-identical to the current 705/143 index",
            "source catalog parses identically to the current catalog and catalog bytes remain unchanged",
            "four complete native rows and class-access data match the current catalog",
            "only the four accepted identities are changed in the authored index",
            "inverse index operations semantically restore prior entries, counts, envelope list and representation count",
            "counts advance to 709 reviewed / 139 pending / 0 accepted-unapplied and 433 complete procedures",
            "all 139 pending identities remain present in the source catalog",
            "runtime selection remains disabled and sourceStatus remains blocked for the four accepted cards",
            "feat335, completed16/72 and prior applied cohorts remain unchanged",
            "compressed casebook decompresses byte-identically to accepted CASEBOOK.json",
            "candidate manifest and every package file binding match",
            "application receipt and exact director acceptance are recorded",
            "next queue group is Rank8 Life/Form4 and requires a fresh 709/139 packet",
            "all 21 dispositions, four original questions, six obligations and 13 holds are present",
            "source-archive lineage and source-candidate bindings match Return150",
            "no runtime, source program, human-play, balance, cosmology or release claim was added",
            "exact current queue and handoff bind to the resulting index and pending audit",
            "Return150 is preserved byte-for-byte in the received-artifact folder and candidate evidence",
        ],
        "beforeIndex": binding(BACKUP), "afterIndex": binding(INDEX), "changedIdentityIds": IDS,
        "onlyFourPendingEntriesChanged": True, "authoredCounts": after["authoredCounts"],
        "representationCounts": after["representationCounts"], "sourceStatusStillBlockedForAllFour": True,
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "runtimeSelectionEnabled": False, "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before, "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all186ReturnMembersVerified": True, "acceptedUnapplied": 0,
        "nextGroup": groups[0]["group"], "nextPendingCount": groups[0]["pendingCount"],
        "applicationReceipt": binding(APPLICATION), "directorAcceptanceReceipt": binding(RECEIPT),
    }
    write_json(VALIDATION, validation_record)

    marker = "**Prior checkpoint: [148]"
    existing_start = START.read_text(encoding="utf-8-sig")
    marker_at = existing_start.find(marker)
    historic = existing_start[marker_at:] if marker_at >= 0 else ""
    start_text = (
        "# Active ordinary spell review150 — Calibration review part6\n\n"
        "Return150 was director accepted and applied for four identities: **709 applied-reviewed / 139 pending / 0 accepted-unapplied**. "
        "GPT reports 29,730 independent static checks and 748 package round-trip checks with zero failures. All 13 qualifications remain, including 59 whole-case holds. "
        "Runtime selection, implementation, human play, balance, cosmology and release approval remain separate.\n\n"
        f"Continue with **{groups[0]['group']}**, preparing a fresh packet against 709/139 and submitting it to GPT for exact director review. Apply only accepted IDs. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [CURRENT-HANDOFF-150](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_150.name}), "
        f"[the 139-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_150.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [snapshot status]({SNAPSHOT.name}).\n\n"
        + historic
    )
    START.write_text(start_text, encoding="utf-8", newline="\n")
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Return150\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **709 reviewed / 139 pending / 0 accepted-unapplied**. Return150 applies the four GPT-accepted Memory/Control4 procedures: Erase Mind, Feeblemind, Mass Dominate, and Mind Ravel.\n\n"
        "The exact director return is bound to its 15,485,461-byte archive and 186 verified members. GPT reports 29,730 independent static checks and 748 package round-trip checks with zero failures. Source catalog bytes and native source/access rows remain unchanged. All 13 qualifications remain, including 59 whole-case holds; proposal operations remain unapplied.\n\n"
        f"The next batch is {groups[0]['group']}. Prepare a fresh packet against 709/139 and wait for exact GPT director acceptance before applying.\n\n"
        "Runtime selection remains disabled. This authored-procedure review does not approve runtime behavior, human play, balance, cosmology, domain closure, or release. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_150.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_150.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}), "
        f"and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    assert read_json(INDEX)["authoredCounts"] == {"reviewed": 709, "pending": 139}
    print(json.dumps({
        "status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "authority": authority,
        "nextGroup": groups[0]["group"], "nextPendingIds": groups[0]["pendingIds"],
        "checksPassed": validation_record["checksPassed"], "indexSha256": sha(INDEX.read_bytes()),
        "catalogUnchanged": True,
    }, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = validate_input()
        print(json.dumps({
            "status": "PREFLIGHT_PASS", "acceptedIds": IDS,
            "authority": data["before"]["authoredCounts"],
            "nextGroup": data["queue"]["currentPendingGroups"][1]["group"],
            "archiveBytes": len(data["archiveBytes"]), "deliveryBytes": len(data["deliveryBytes"]),
            "candidateOutputAbsent": not CANDIDATE.exists(), "catalogBytes": len(data["catalogBytes"]),
        }, indent=2))
