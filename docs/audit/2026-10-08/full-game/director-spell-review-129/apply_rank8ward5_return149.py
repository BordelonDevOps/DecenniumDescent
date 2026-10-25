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
IDS = ["alignment-immunity", "antilife-shell", "antimagic-field", "mind-blank", "reputation-fortress"]
REVIEW_ID = "RANK8-WARD5-EXACT-AUTHORED-ACCEPTANCE-149"
APP_ID = "RANK8-WARD5-APPLICATION-149"
ARCHIVE_NAME = "DD_Rank8_Ward5_Director_Return149.zip"
DELIVERY_NAME = "DD_Rank8_Ward5_Director_Return149_DELIVERY.json"
RECEIVED = AUDIT / "rank8ward5_return149_received"
ARCHIVE = RECEIVED / ARCHIVE_NAME
DELIVERY = RECEIVED / "DIRECTOR_RETURN_DELIVERY.json"
DOWNLOADS = Path.home() / "Downloads"
INPUT_ARCHIVE = DOWNLOADS / ARCHIVE_NAME
INPUT_DELIVERY = DOWNLOADS / DELIVERY_NAME
EXTRACTED = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "Temp/DD149Review/return149"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_148 = AUDIT / "CURRENT_SPELL_QUEUE_148.json"
PENDING_148 = AUDIT / "CURRENT148_PENDING_IDENTITY_AUDIT_148.json"
HANDOFF_148 = AUDIT / "CURRENT_HANDOFF_148.json"
QUEUE_149 = AUDIT / "CURRENT_SPELL_QUEUE_149.json"
PENDING_149 = AUDIT / "CURRENT143_PENDING_IDENTITY_AUDIT_149.json"
HANDOFF_149 = AUDIT / "CURRENT_HANDOFF_149.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_RANK8_WARD5_149.json"
RECEIPT = AUDIT / "RANK8_WARD5_EXACT_ACCEPTANCE_149.json"
APPLICATION = AUDIT / "RANK8_WARD5_APPLICATION_149.json"
OPERATIONS = AUDIT / "RANK8_WARD5_INDEX_OPERATIONS_149.json"
VALIDATION = AUDIT / "RANK8_WARD5_APPLICATION_VALIDATION_149.json"
BACKUP = AUDIT / "authored_review_index.before_rank8ward5_149.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8ward5_reviewed_149"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_WARD5_REVIEWED_149.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_149.md"
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


def validate_input():
    input_archive = ARCHIVE if ARCHIVE.exists() else INPUT_ARCHIVE
    input_delivery = DELIVERY if DELIVERY.exists() else INPUT_DELIVERY
    assert input_archive.is_file() and input_delivery.is_file(), "Accepted return archive or delivery file is missing."
    archive_bytes = input_archive.read_bytes()
    delivery_bytes = input_delivery.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    assert len(archive_bytes) == 21_423_569
    assert sha(archive_bytes) == "a9d66a92d1a3ea510d34e2a0d5d0a19faefa8d27812a12c762928ca38e62e47c"
    assert delivery["filename"] == ARCHIVE_NAME
    assert delivery["bytes"] == len(archive_bytes) and delivery["sha256"] == sha(archive_bytes)
    assert delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS
    assert delivery["authorityAtInput"] == {
        "appliedReviewed": 700, "pending": 148, "acceptedUnapplied": 0,
        "completeReviewedStandaloneProcedures": 424, "canonicalFilesChanged": False,
    }
    assert delivery["memberCount"] == 188
    assert delivery["validation"]["independentStaticChecks"] == 15142
    assert delivery["validation"]["staticFailures"] == 0
    assert delivery["validation"]["packageMemberChecks"] == 755
    assert delivery["validation"]["zipCentralDirectory"] and delivery["validation"]["allCRCs"]
    assert delivery["validation"]["allMemberHashes"] and delivery["validation"]["allowlistExact"]
    assert EXTRACTED.is_dir()

    with ZipFile(input_archive) as archive:
        names = archive.namelist()
        manifest = read_json(EXTRACTED / "MEMBER_MANIFEST.json")
        assert archive.testzip() is None
        assert len(names) == len(set(names)) == manifest["memberCount"] == 188
        assert set(names) == set(manifest["allowedMembers"])
        delivery_rows = {r["path"]: r for r in delivery["members"]}
        manifest_rows = {r["path"]: r for r in manifest["payloadMembers"]}
        assert set(delivery_rows) == set(names)
        assert set(manifest_rows) == set(names) - {"MEMBER_MANIFEST.json"}
        for name in names:
            p = PurePosixPath(name)
            assert not p.is_absolute() and ".." not in p.parts and "\\" not in name
            info = archive.getinfo(name)
            raw = archive.read(name)
            row = delivery_rows[name]
            assert len(raw) == info.file_size == row["bytes"]
            assert info.CRC == int(row["crc32"], 16) and sha(raw) == row["sha256"]
            assert f"{info.CRC:08x}" == row["crc32"].lower()
            if name != "MEMBER_MANIFEST.json":
                mrow = manifest_rows[name]
                assert (mrow["bytes"], mrow["sha256"], mrow["crc32"].lower()) == (row["bytes"], row["sha256"], row["crc32"].lower())
            extracted = EXTRACTED.joinpath(*p.parts)
            assert extracted.is_file() and extracted.read_bytes() == raw

    director_decision = read_json(EXTRACTED / "DIRECTOR_DECISION.json")
    model = read_json(EXTRACTED / "MODEL.json")
    counts = read_json(EXTRACTED / "COUNTS.json")
    failure = read_json(EXTRACTED / "FAILURE_CHECK.json")
    dispositions = read_json(EXTRACTED / "QUESTION_DISPOSITIONS.json")
    holds = read_json(EXTRACTED / "HOLDS.json")
    proposal_ops = read_json(EXTRACTED / "PROPOSAL_OPERATIONS.json")
    assert sha((EXTRACTED / "DIRECTOR_DECISION.json").read_bytes()) == delivery["directorDecisionSHA256"]
    assert director_decision["accepted"] and not director_decision["applied"]
    assert director_decision["acceptedIds"] == IDS and director_decision["authorityAtInput"] == delivery["authorityAtInput"]
    assert director_decision["decisionBasis"]["independentStaticChecksPassed"] == 15142
    assert director_decision["decisionBasis"]["failedChecks"] == 0
    assert director_decision["decisionBasis"]["completeProcedureBinding"]["sha256"] == sha((EXTRACTED / "MODEL.json").read_bytes())
    assert [p["spellId"] for p in model["procedures"]] == IDS
    assert all(p["proposed"] and not p["applied"] for p in model["procedures"])
    assert counts == delivery["counts"] and counts["cases"] == 72 and counts["events"] == 337
    assert counts["eventOperations"] == 1348 and counts["holds"] == 13 and counts["positiveFortressCasesHeld"] == 10
    assert failure["pass"] is True and failure["passed"] == 15142 and failure["failed"] == 0 and not failure["failures"]
    assert len(dispositions["conferenceDispositions"]) == 23
    assert len(dispositions["originalIdentityDispositions"]) == 5
    assert len(dispositions["futureRequirementsUnchanged"]) == 7
    assert len(holds["holds"]) == 13 and all(h["retained"] for h in holds["holds"])
    assert isinstance(proposal_ops, list) and len(proposal_ops) == 5
    assert all("NOT a canonical-index/catalog operation" in op["scope"] for op in proposal_ops)
    assert all(op["before"]["localAuthoredProcedure"] is None and op["after"]["localAuthoredProcedure"] for op in proposal_ops)

    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog = json.loads(catalog_bytes.decode("utf-8-sig"))
    queue = read_json(QUEUE_148)
    pending = read_json(PENDING_148)
    handoff = read_json(HANDOFF_148)
    source_index = next(EXTRACTED.glob("evidence/source02/sources/**/spell_playtests/authored_review_index.json")).read_bytes()
    source_catalog_path = next(EXTRACTED.glob("evidence/source02/sources/**/spell_playtests/catalog.json"))
    source_catalog_bytes = source_catalog_path.read_bytes()
    source_catalog = json.loads(source_catalog_bytes.decode("utf-8-sig"))
    source_verification = read_json(EXTRACTED / "SOURCE_VERIFICATION.json")
    source_archive = (EXTRACTED / "history/DD_Rank8_Ward_5_Source_Conference_02.zip").read_bytes()
    source_candidate = (EXTRACTED / "evidence/source02/CANDIDATE.json").read_bytes()
    assert sha(before_bytes) == "7248aaf5854040361245a17a1dcab1a1778a646f9b65ccacaf90c5f8b29177f2"
    assert before["authoredCounts"] == {"reviewed": 700, "pending": 148}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 424
    assert source_index == before_bytes
    assert source_catalog == catalog
    assert sha(source_catalog_bytes) == before["sourceCatalogSha256"] == "f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8"
    assert sha(source_archive) == source_verification["archive"]["sha256"] == delivery["sourceArchive"]["sha256"]
    assert sha(source_candidate) == source_verification["sourceCandidateSHA256"]
    assert queue["currentAuthority"]["reviewedApplied"] == 700 and queue["currentAuthority"]["pending"] == 148
    assert pending["pendingCount"] == 148 and pending["indexBinding"]["sha256"] == sha(before_bytes)
    assert handoff["currentIndexBinding"]["sha256"] == sha(before_bytes)
    assert queue["currentPendingGroups"][0]["group"] == "rank8-ward5"
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS
    rows = {row["id"]: row for row in before["entries"]}
    assert len(rows) == 848
    current_pending = {e["id"] for e in before["entries"] if e["authoredStatus"] == "pending-authored-procedure"}
    assert len(current_pending) == 148 and set(pending["pendingIds"]) == current_pending and set(IDS) <= current_pending
    for sid in IDS:
        row = rows[sid]
        assert row["sourceStatus"] == "blocked-pending-operational-review"
        native = catalog["spells"][int(row["wholeCardPointer"].rsplit("/", 1)[1])]
        record = next(p for p in model["procedures"] if p["spellId"] == sid)
        assert native["id"] == sid and record["completeNativeSourceAndAccess"] == native

    output_paths = [RECEIVED, CANDIDATE, STAGING, MANUSCRIPT, DECISION, RECEIPT, APPLICATION, OPERATIONS,
                    VALIDATION, BACKUP, QUEUE_149, PENDING_149, HANDOFF_149, SNAPSHOT]
    assert not any(path.exists() for path in output_paths), "An application output path exists; inspect before retrying."
    return {
        "inputArchive": input_archive, "inputDelivery": input_delivery,
        "archiveBytes": archive_bytes, "deliveryBytes": delivery_bytes,
        "directorDecision": director_decision, "directorModel": model, "counts": counts,
        "dispositions": dispositions, "holds": holds, "proposalOperations": proposal_ops,
        "beforeBytes": before_bytes, "catalogBytes": catalog_bytes, "before": before,
        "catalog": catalog, "queue": queue, "pendingIds": current_pending,
        "sourceArchiveBytes": source_archive, "sourceCandidateBytes": source_candidate,
        "sourceCatalogBytes": source_catalog_bytes,
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
        "id": "GPT-DIRECTOR-DECISION-RANK8-WARD5-149",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": decision["id"], "accepted": True, "appliedAtDecision": False,
        "acceptedIds": IDS, "rejectedIds": [], "remainingBlockingDefects": [],
        "verification": {"independentStaticChecksPassed": 15142, "independentStaticFailures": 0,
            "packageMemberChecksPassed": 755, "packageMemberFailures": 0, "archiveMembers": 188,
            "cases": 72, "events": 337, "eventOperations": 1348, "holds": 13, "positiveFortressCasesHeld": 10},
        "acceptedArchive": {"name": ARCHIVE_NAME, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "scope": decision["scope"], "holdScope": decision["holdScope"], "excludedClaims": decision["excludedClaims"],
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
        "countsBefore": {"reviewed": 700, "pending": 148, "acceptedUnapplied": 0},
        "countsAfter": {"reviewed": 705, "pending": 143, "acceptedUnapplied": 0},
        "completeReviewedStandaloneProceduresBefore": 424,
        "completeReviewedStandaloneProceduresAfter": 429,
        "acceptedCases": counts["cases"], "acceptedEvents": counts["events"], "eventOperations": counts["eventOperations"],
        "retainedHolds": 13, "positiveFortressCasesHeld": 10,
        "sourceStatusPreserved": "blocked-pending-operational-review for all five identities; authored procedure review only.",
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "releaseApproved": False, "canonicalApplicationPerformed": False,
    }
    receipt_bytes = json_bytes(receipt)
    receipt_binding = binding(RECEIPT, raw=receipt_bytes)

    STAGING.mkdir(parents=True)
    (STAGING / "DIRECTOR_RETURN/PROCEDURES").mkdir(parents=True)
    for file in EXTRACTED.iterdir():
        if file.is_file() and file.name != "CASEBOOK.json":
            shutil.copyfile(file, STAGING / "DIRECTOR_RETURN" / file.name)
    for file in (EXTRACTED / "procedures").glob("*.json"):
        shutil.copyfile(file, STAGING / "DIRECTOR_RETURN/PROCEDURES" / file.name)

    with ZipFile(data["inputArchive"]) as archive:
        casebook_info = archive.getinfo("CASEBOOK.json")
        casebook_row = next(row for row in json.loads(delivery_bytes.decode("utf-8-sig"))["members"] if row["path"] == "CASEBOOK.json")
        casebook_path = STAGING / "CASEBOOK.json.gz"
        with archive.open("CASEBOOK.json", "r") as source, casebook_path.open("wb") as output:
            with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as gz:
                shutil.copyfileobj(source, gz)
    with gzip.open(casebook_path, "rb") as compressed:
        casebook_raw = compressed.read()
    assert len(casebook_raw) == casebook_row["bytes"] == casebook_info.file_size
    assert sha(casebook_raw) == casebook_row["sha256"]

    (STAGING / "DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(archive_bytes)
    (STAGING / "DIRECTOR_RETURN_DELIVERY.json").write_bytes(delivery_bytes)
    (STAGING / "GPT_DIRECTOR_DECISION.json").write_bytes(decision_record_bytes)
    (STAGING / "EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    source_archive_bytes = data["sourceArchiveBytes"]
    source_candidate_bytes = data["sourceCandidateBytes"]
    (STAGING / "SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(source_archive_bytes)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_bytes)
    standalone_bytes = (EXTRACTED / "STANDALONE_PROCEDURES.md").read_bytes()
    (STAGING / "STANDALONE_PROCEDURES.md").write_bytes(standalone_bytes)

    spells = []
    for i, proc in enumerate(model["procedures"]):
        old = next(row for row in before["entries"] if row["id"] == proc["spellId"])
        spells.append({
            "id": proc["spellId"], "name": proc["completeNativeSourceAndAccess"]["name"],
            "procedure": proc["procedure"], "directorProcedureRecord": copy.deepcopy(proc),
            "nativeCardAndAccessUnchanged": copy.deepcopy(proc["completeNativeSourceAndAccess"]),
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "sourceRecordPointer": proc["originalSourceEnvelope"].get("originalQuestionPointer"),
            "runtimeSelectionEnabled": False,
        })
    shared_text = model["procedures"][0]["commonProcedure"]
    assert all(p["commonProcedure"] == shared_text for p in model["procedures"])
    normalized_model = {
        "schemaVersion": 3, "moduleId": "rank8ward5-reviewed-149",
        "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Only the five director-accepted Ward5 authored procedures, exact dispositions and bound static evidence are recorded. Preserve native spell cards, class access, source status and catalog bytes. All 13 Ward5 holds remain, including 10 positive Reputation Fortress campaign examples. No proposal operations are applied. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "sharedRules": {"id": "WARD5-COMMON-149", "text": shared_text, "scope": "These five identities only."},
        "spells": spells,
        "sourceLinkedCounterparts": model["sourceLinkedCounterparts"],
        "currentAcceptedInterfacesUnchanged": model["currentAcceptedInterfacesUnchanged"],
        "questionDispositions": dispositions, "returnCounts": counts,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLDS.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip; decompression is byte-identical to the CASEBOOK.json member of DIRECTOR_RETURN_ARCHIVE.zip",
        "casebookSourceMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_row["bytes"], "sha256": casebook_row["sha256"]},
        "directorReturnArchive": "DIRECTOR_RETURN_ARCHIVE.zip", "directorReturnDelivery": "DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive": "SOURCE_CONFERENCE_ARCHIVE.zip", "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "standaloneProcedures": "STANDALONE_PROCEDURES.md", "directorDecisionFile": "GPT_DIRECTOR_DECISION.json",
        "directorReturnBinding": {"path": f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/{ARCHIVE_NAME}", "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "sourceArchiveMemberCount": 188, "independentAcceptanceGranted": True,
        "canonicalApplicationPerformed": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False, "releaseApproved": False,
    }

    excluded_bindings = {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}
    package_files = []
    for path in sorted(STAGING.rglob("*")):
        if path.is_file() and path.relative_to(STAGING).as_posix() not in excluded_bindings:
            raw = path.read_bytes()
            package_files.append({"path": path.relative_to(STAGING).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    package_manifest = {
        "id": "RANK8-WARD5-CANDIDATE-PACKAGE-MANIFEST-149",
        "sourceArchive": {"name": ARCHIVE_NAME, "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
        "files": package_files, "excludedFromBindings": sorted(excluded_bindings),
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

    if not RECEIVED.exists():
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
        "id": APP_ID, "recordedAtUtc": now(), "status": "APPLIED_FIVE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact accepted ordinary-spell scope and continue through the remaining pending ordinary spell identities.",
        "acceptedIds": IDS, "directorAcceptance": binding(RECEIPT), "directorDecision": binding(DECISION),
        "directorReturn": archive_binding,
        "directorReturnDelivery": binding(DELIVERY, f"docs/audit/2026-10-08/full-game/{RECEIVED.name}/DIRECTOR_RETURN_DELIVERY.json", delivery_bytes),
        "candidateEnvelope": model_binding, "candidatePackageManifest": package_binding,
        "indexBefore": binding(BACKUP, raw=before_bytes),
        "counts": {"before": {"reviewed": 700, "pending": 148, "acceptedUnapplied": 0}, "after": {"reviewed": 705, "pending": 143, "acceptedUnapplied": 0}},
        "completeReviewedStandaloneProcedures": {"before": 424, "after": 429},
        "cases": 72, "events": 337, "eventOperations": 1348,
        "retainedHolds": 13, "positiveFortressCasesHeld": 10,
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
            "procedureFile": "../spell_candidates/rank8ward5_reviewed_149/MODEL.json",
            "procedurePointer": f"/spells/{n}/procedure", "wholeCardPointer": f"/spells/{n}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id", "procedureTextPointer": f"/spells/{n}/procedure",
            "directorProcedureRecordPointer": f"/spells/{n}/directorProcedureRecord", "sharedRulesPointer": "/sharedRules",
            "manuscript": "../../../docs/spells/candidates/RANK8_WARD5_REVIEWED_149.md",
            "reviewId": APP_ID, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(), "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip; exact decompression reproduces the director return CASEBOOK.json member",
            "casebookSourceArchiveMemberBinding": normalized_model["casebookSourceMemberBinding"],
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
        "file": "../spell_candidates/rank8ward5_reviewed_149/MODEL.json", "binding": model_binding,
        "reviewId": REVIEW_ID, "acceptedIds": IDS, "excludedPendingIds": excluded_pending,
        "authority": binding(RECEIPT), "applicationReceipt": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APPLICATION.name}",
        "sourceArchive": archive_binding, "casebookBinding": casebook_binding, "holdsBinding": holds_binding,
        "candidatePackageManifestBinding": package_binding, "scope": receipt["decision"], "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 705, "pending": 143}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 429
    pending_after = {e["id"] for e in after["entries"] if e["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 5 and len(pending_after) == 143
    assert pending_after == data["pendingIds"] - set(IDS)

    inverse = copy.deepcopy(after)
    for op in operations:
        inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    ops_doc = {
        "id": "RANK8-WARD5-INDEX-OPERATIONS-149",
        "before": {"path": BACKUP.relative_to(ROOT).as_posix(), "bytes": len(before_bytes), "sha256": sha(before_bytes)},
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "five prior entries, aggregate counts, standalone-envelope array and representation count"},
        "onlyIdentityIds": IDS,
    }
    BACKUP.write_bytes(before_bytes)
    write_json(APPLICATION, app)
    write_json(OPERATIONS, ops_doc)
    tmp_index = INDEX.with_suffix(".json.application149.tmp")
    tmp_index.write_bytes(after_bytes)
    os.replace(tmp_index, INDEX)
    assert INDEX.read_bytes() == after_bytes and CATALOG.read_bytes() == catalog_bytes

    authority = copy.deepcopy(queue["currentAuthority"])
    authority.update({"reviewedApplied": 705, "pending": 143, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 429})
    groups = []
    for group in queue["currentPendingGroups"]:
        ids = [sid for sid in group["pendingIds"] if sid in pending_after]
        if ids:
            item = copy.deepcopy(group)
            item["pendingIds"] = ids
            item["pendingCount"] = len(ids)
            if item["group"] == "rank8-memory-control4":
                item["freshPacketRequiredForCurrentAuthority"] = True
            groups.append(item)
    assert groups[0]["group"] == "rank8-memory-control4" and sum(g["pendingCount"] for g in groups) == 143
    queue_after = copy.deepcopy(queue)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-149", "recordedAtUtc": now(), "currentAuthority": authority,
        "currentPendingGroups": groups, "nextSuggestedGroups": groups[:5], "nextGroup": groups[0],
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 5, "applicationReceipt": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APPLICATION.name}"},
        "pendingIdentityAudit": {"path": PENDING_149.name, "pending": 143, "indexSha256": sha(after_bytes)},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "archive": groups[0]["archive"], "candidate": groups[0]["candidate"], "freshPacketRequiredForCurrentAuthority": True},
    })
    pending_doc = {
        "id": "CURRENT143-PENDING-IDENTITY-AUDIT-149", "recordedAtUtc": now(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": binding(INDEX),
        "catalogBinding": binding(CATALOG), "authoredCounts": after["authoredCounts"], "pendingCount": 143,
        "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": all(any(r.get("id") == sid for r in catalog["spells"]) for sid in pending_after),
        "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0,
    }
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(QUEUE_149, queue_after)
    write_json(PENDING_149, pending_doc)
    handoff = copy.deepcopy(read_json(HANDOFF_148))
    handoff.update({
        "id": "CURRENT-HANDOFF-149", "recordedAtUtc": now(), "status": "RANK8_WARD5_APPLIED_NEXT_143_PENDING",
        "currentAuthority": authority, "currentIndexBinding": binding(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": binding(CATALOG, "authority/catalog.json"),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_149.name, "pendingCount": 143, "sha256": sha(PENDING_149.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 5,
            "applicationReceipt": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APPLICATION.name}",
            "directorAcceptance": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}"},
        "nextGroup": groups[0]["group"],
        "resumePriority": "Prepare a fresh Memory/Control4 source packet against 705/143 and submit it to Calibration review part 6. Apply only after exact GPT director acceptance; preserve closed feat335 and completed spell cohorts.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0]["candidate"], "archive": groups[0]["archive"],
            "freshPacketRequiredForCurrentAuthority": True, "request": "Prepare and submit a fresh request bound to current 705/143 authority before director review."},
    })
    write_json(HANDOFF_149, handoff)

    validation = {
        "id": "RANK8-WARD5-APPLICATION-VALIDATION-149", "status": "PASS", "checksPassed": 20, "checksFailed": 0,
        "checks": [
            "return archive and delivery hashes match frozen bindings",
            "all 188 return members pass size, SHA-256, CRC, allowlist and extracted-byte checks",
            "exact director acceptance for the five indexed pending IDs; no director application",
            "15,142 static checks and 755 package checks pass with zero failures",
            "all 13 holds retained; positive Fortress cases remain held",
            "all 20 proposal operations remain unapplied",
            "source index is byte-identical to the current 700/148 index",
            "full source catalog parses identically to the current worktree catalog",
            "five complete native rows and access data match the current catalog",
            "only the five accepted identities are changed in the authored index",
            "inverse operations semantically restore all prior index data",
            "counts advance to 705 reviewed / 143 pending / 0 accepted-unapplied and 429 complete procedures",
            "catalog bytes are unchanged",
            "all 143 pending identities remain present in the source catalog",
            "runtime selection remains disabled and sourceStatus remains blocked",
            "feat335 and previously completed spell cohorts remain unchanged",
            "compressed casebook decompresses byte-identically to the accepted archive member",
            "candidate manifest and all candidate source bindings match",
            "application receipt and exact acceptance are recorded",
            "next queue group is Memory/Control4 and requires a fresh 705/143 packet",
        ],
        "beforeIndex": binding(BACKUP), "afterIndex": binding(INDEX), "changedIdentityIds": IDS,
        "onlyFivePendingEntriesChanged": True, "authoredCounts": after["authoredCounts"],
        "representationCounts": after["representationCounts"], "sourceStatusStillBlockedForAllFive": True,
        "sourceCatalogBytesUnchanged": CATALOG.read_bytes() == catalog_bytes,
        "runtimeSelectionEnabled": False, "closed335AndCompletedCohortsReopened": False,
        "inverseSemanticReplayExact": inverse == before, "backupByteExact": BACKUP.read_bytes() == before_bytes,
        "all188ReturnMembersVerified": True, "acceptedUnapplied": 0,
        "nextGroup": groups[0]["group"], "nextPendingCount": groups[0]["pendingCount"],
        "applicationReceipt": binding(APPLICATION), "directorAcceptanceReceipt": binding(RECEIPT),
    }
    write_json(VALIDATION, validation)
    marker = "**Latest checkpoint: [128]"
    existing_start = START.read_text(encoding="utf-8-sig")
    marker_at = existing_start.find(marker)
    historic = existing_start[marker_at:] if marker_at >= 0 else ""
    start_text = (
        "# Active ordinary spell review149 — Calibration review part6\n\n"
        "Return149 was director accepted and applied for five identities: **705 applied-reviewed / 143 pending / 0 accepted-unapplied**. "
        "GPT reports 15,142 independent static checks and 755 package-member checks with zero failures. All 13 Ward5 holds remain, including 10 positive Fortress campaign cases. "
        "Runtime selection, implementation, human play, balance, cosmology, release and domain-closure approval remain separate.\n\n"
        "Continue with **rank8-memory-control4** (four identities), preparing a fresh packet against 705/143 and submitting it to GPT for exact director review. Apply only accepted IDs. Preserve closed feat335 and completed spell cohorts.\n\n"
        f"Read [CURRENT-HANDOFF-149](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_149.name}), "
        f"[the 143-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_149.name}), "
        f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), "
        f"and [snapshot status]({SNAPSHOT.name}).\n\n"
        "**Prior checkpoint: [148](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_148.json).**\n\n"
        + historic
    )
    START.write_text(start_text, encoding="utf-8", newline="\n")
    SNAPSHOT.write_text(
        "# Ordinary spell review snapshot — Return149\n\n"
        "As of 2026-10-25, the authored ordinary-spell index records **705 reviewed / 143 pending / 0 accepted-unapplied**. Return149 applies the five GPT-accepted Ward5 procedures: Alignment Immunity, Antilife Shell, Antimagic Field, Mind Blank, and Reputation Fortress.\n\n"
        "The exact director return is bound to its 21,423,569-byte archive and 188 verified members. GPT reports 15,142 independent static checks and 755 package-member checks with zero failures. Source catalog bytes and native source/access rows remain unchanged. All 13 Ward5 holds remain, including 10 positive Reputation Fortress campaign cases; proposal operations remain unapplied.\n\n"
        "The next batch is Memory/Control4: erase-mind, feeblemind, mass-dominate, and mind-ravel. Prepare a fresh packet against 705/143 and wait for exact GPT director acceptance before applying.\n\n"
        "Runtime selection remains disabled. This authored-procedure review does not approve runtime behavior, human play, balance, cosmology, domain closure, or release. Closed feat335 and completed spell cohorts remain closed.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_149.name}), "
        f"[pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_149.name}), "
        f"[exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}), "
        f"and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_bytes
    assert read_json(INDEX)["authoredCounts"] == {"reviewed": 705, "pending": 143}
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "authority": authority,
        "nextGroup": groups[0]["group"], "nextPendingIds": groups[0]["pendingIds"],
        "checksPassed": validation["checksPassed"], "indexSha256": sha(INDEX.read_bytes()),
        "catalogUnchanged": True}, indent=2))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        data = validate_input()
        print(json.dumps({"status": "PREFLIGHT_PASS", "acceptedIds": IDS,
            "authority": data["before"]["authoredCounts"],
            "nextGroup": data["queue"]["currentPendingGroups"][1]["group"],
            "archiveBytes": len(data["archiveBytes"]), "deliveryBytes": len(data["deliveryBytes"]),
            "candidateOutputAbsent": not CANDIDATE.exists(), "catalogBytes": len(data["catalogBytes"])}, indent=2))
