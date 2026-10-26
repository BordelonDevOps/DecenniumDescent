from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
RECV = AUDIT / "rank9_psychicfear7_return182_received"
RETURN = RECV / "DD_Rank9_PsychicFear7_Director_Return182.zip"
DELIVERY_OBSERVATION = RECV / "RETURN182_DELIVERY_OBSERVATION.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_PSYCHICFEAR7_RETURN182_INDEPENDENT_AUDIT.json"
VERIFY = AUDIT / "verify_psychicfear7_return182.py"
SOURCE_ARCHIVE = FULL / "DD_Rank9_Psychic_Fear_7_Source_Conference_02_180.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_02_180.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_179.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_179.json"
PENDING_BEFORE = AUDIT / "CURRENT93_PENDING_IDENTITY_AUDIT_179.json"
ALL_IDS = [
    "phantom-armageddon",
    "phantom-cataclysm",
    "psychic-scream",
    "frightful-sovereignty",
    "mass-phantom-killer",
    "weird",
    "reality-break",
]
IDS = ["phantom-armageddon", "phantom-cataclysm", "frightful-sovereignty", "reality-break"]
ID_SET = set(IDS)
BLOCKED_IDS = ["psychic-scream", "mass-phantom-killer", "weird"]
BEFORE = {"reviewed": 755, "pending": 93, "acceptedUnapplied": 0}
AFTER = {"reviewed": 759, "pending": 89, "acceptedUnapplied": 0}
COMPLETE_BEFORE = 479
COMPLETE_AFTER = 483
REVIEW_ID = "RANK9-PSYCHICFEAR7-EXACT-AUTHORED-ACCEPTANCE-182"
APP_ID = "RANK9-PSYCHICFEAR7-APPLICATION-182"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9psychicfear7_reviewed_182"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_PSYCHICFEAR7_REVIEWED_182.md"
BACKUP = AUDIT / "authored_review_index.before_psychicfear7_182.json"
DECISION = AUDIT / "RANK9_PSYCHICFEAR7_GPT_DECISION_182.json"
ACCEPTANCE = AUDIT / "RANK9_PSYCHICFEAR7_EXACT_ACCEPTANCE_182.json"
RECEIPT = AUDIT / "RANK9_PSYCHICFEAR7_GPT_RETURN_182.json"
APPLICATION = AUDIT / "RANK9_PSYCHICFEAR7_APPLICATION_182.json"
OPERATIONS = AUDIT / "RANK9_PSYCHICFEAR7_INDEX_OPERATIONS_182.json"
PENDING_AFTER = AUDIT / "CURRENT89_PENDING_IDENTITY_AUDIT_182.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_182.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_182.json"
VALIDATION = AUDIT / "RANK9_PSYCHICFEAR7_APPLICATION_VALIDATION_182.json"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-26_SPELL_REVIEW_182.md"
START = ROOT / "START_HERE.md"
DIRECTOR_FILES = [
    "DIRECTOR_DECISION.json",
    "SEMANTIC_FAILURE_CHECK.json",
    "PROCEDURES.json",
    "PROCEDURE_PROPOSALS.json",
    "QUESTION_DISPOSITIONS.json",
    "CASE_DISPOSITIONS.json",
    "CASE_INDEX.json",
    "HOLD_REGISTER.json",
    "ORIGINAL_OBLIGATIONS.json",
    "STANDALONE_PROCEDURES.md",
    "SOURCE_VERIFICATION.json",
    "DATA_VALIDATION.json",
    "METADATA_VALIDATION.json",
    "EVIDENCE_MANIFEST.json",
    "MEMBER_MANIFEST.json",
    "RETURN181_REPAIR_LEDGER.json",
    "GIT_PUBLICATION_EVIDENCE.json",
    "COUNTS.json",
    "CURRENT_AUTHORITY.json",
    "COVERAGE_MATRIX.json",
    "ACTOR_PROFILES.json",
    "COMPARISON_BOUNDARIES.json",
    "INHERITED_APPLIED_HOLDS.json",
    "INHERITED_CATASTROPHE_HOLDS.json",
    "ACCEPTED_COMPARISON_MEMBER_PROOF.json",
    "evidence_ACCEPTED_PROFILE_COMPARISON.json",
    "README.md",
    "ORIGINAL_REQUEST.txt",
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
    subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=True)
    audit = read_json(INDEPENDENT_AUDIT)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["acceptedIds"] == IDS
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = read_json(INDEX)
    catalog = json.loads(subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{CATALOG.relative_to(ROOT).as_posix()}"], cwd=ROOT).decode("utf-8"))
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    entries = {row["id"]: row for row in before["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 755, "pending": 93}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    assert len(live_pending) == 93 and ID_SET <= live_pending
    assert pending_before["pendingCount"] == 93 and set(ALL_IDS) <= set(pending_before["pendingIds"])
    assert queue["currentAuthority"]["reviewedApplied"] == handoff["currentAuthority"]["reviewedApplied"] == 755
    assert queue["currentAuthority"]["pending"] == handoff["currentAuthority"]["pending"] == 93
    assert queue["currentPendingGroups"][0]["group"] == "rank9-psychic-fear7" and queue["currentPendingGroups"][0]["pendingIds"] == ALL_IDS
    assert all(entries[sid]["authoredStatus"] == "pending-authored-procedure" and entries[sid]["sourceStatus"] == "blocked-pending-operational-review" for sid in ALL_IDS)

    with zipfile.ZipFile(RETURN, "r") as archive:
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        procedures = json.loads(archive.read("PROCEDURES.json"))
        procedures_by_id = {row["spellId"]: row for row in procedures}
        assert archive.testzip() is None
        assert all(PurePosixPath(name).as_posix() == name for name in archive.namelist())
    decisions = {row["id"]: row for row in decision["perIdentity"]}
    assert decision["acceptedIds"] == IDS and decision["unacceptedIds"] == BLOCKED_IDS
    assert decision["accepted"] is False and decision["batchAccepted"] is False and decision["applied"] is False
    assert all(decisions[sid]["accepted"] is True and decisions[sid]["applied"] is False and decisions[sid]["blockerIds"] == [] for sid in IDS)
    assert all(decisions[sid]["accepted"] is False and decisions[sid]["applied"] is False for sid in BLOCKED_IDS)
    assert all(procedures_by_id[sid]["accepted"] is False and procedures_by_id[sid]["applied"] is False for sid in ALL_IDS)
    assert all(procedures_by_id[sid]["nativeCardAndAccessUnchanged"] == catalog_rows[sid] for sid in IDS)
    source_candidate_bytes = SOURCE_CANDIDATE.read_bytes()
    source_archive_bytes = SOURCE_ARCHIVE.read_bytes()
    assert sha_file(RETURN) == audit["archive"]["sha256"] and RETURN.stat().st_size == audit["archive"]["bytes"]
    assert source_candidate_bytes == zipfile.ZipFile(RETURN).read("SOURCE_CONFERENCE_CANDIDATE.json")
    assert source_archive_bytes == zipfile.ZipFile(RETURN).read("SOURCE_CONFERENCE_ARCHIVE.zip")

    outputs = [STAGING, CANDIDATE, RECV / "RETURN182_DELIVERY_OBSERVATION.json", MANUSCRIPT, BACKUP, DECISION, ACCEPTANCE, RECEIPT, APPLICATION, OPERATIONS, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, VALIDATION, SNAPSHOT]
    existing = [str(path) for path in outputs if path.exists()]
    assert not existing, f"Application outputs already exist; inspect before retrying: {existing}"
    assert CATALOG.read_bytes() == catalog_bytes
    return locals()


def apply() -> None:
    data = preflight()
    ts = now()
    before = data["before"]
    before_bytes = data["before_bytes"]
    catalog = data["catalog"]
    catalog_bytes = data["catalog_bytes"]
    queue_before = data["queue"]
    handoff_before = data["handoff"]
    live_pending = data["live_pending"]
    entries = data["entries"]
    catalog_rows = data["catalog_rows"]
    audit = data["audit"]
    excluded_pending = sorted(live_pending - ID_SET)
    assert len(excluded_pending) == 89

    with zipfile.ZipFile(RETURN, "r") as archive:
        member_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        archive_members = [row["path"] for row in member_manifest["members"]] + ["MEMBER_MANIFEST.json"]
        source_members = {name: archive.read(name) for name in DIRECTOR_FILES}
        procedures_doc = json.loads(archive.read("PROCEDURES.json"))
        questions_doc = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        obligations_doc = json.loads(archive.read("ORIGINAL_OBLIGATIONS.json"))
        case_dispositions = json.loads(archive.read("CASE_DISPOSITIONS.json"))
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        source_verification = json.loads(archive.read("SOURCE_VERIFICATION.json"))
        casebook_info = next(row for row in member_manifest["members"] if row["path"] == "CASEBOOK.json")
        source_candidate_bytes = archive.read("SOURCE_CONFERENCE_CANDIDATE.json")
    procedures_by_id = {row["spellId"]: row for row in procedures_doc}
    decisions = {row["id"]: row for row in decision["perIdentity"]}
    decision_id = f"GPT-DIRECTOR-DECISION-PSYCHICFEAR7-{decision['return']}"
    assert [row["spellId"] for row in procedures_doc] == ALL_IDS
    assert all(decision["perIdentity"][i]["id"] in ALL_IDS for i in range(len(ALL_IDS)))
    assert all(procedures_by_id[sid]["nativeCardAndAccessUnchanged"] == catalog_rows[sid] for sid in IDS)

    # Preserve the exact large return archive as the immutable source; keep a deterministic
    # gzip copy of its aggregate casebook for convenient local reads, verified byte-for-byte.
    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    for name, raw in source_members.items():
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    observation = {
        "id": "RANK9-PSYCHICFEAR7-RETURN182-DELIVERY-OBSERVATION",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT},
        "libraryArtifacts": {
            "returnArchive": {"fileId": "libfile_fd90bdfd6c148191aef5226926ecfff3", "fileName": RETURN.name},
            "deliveryManifest": {"fileId": "libfile_2632573b5ce48191903a32c8b831eaf8", "fileName": "DD_Rank9_PsychicFear7_Director_Return182_DELIVERY.json"},
        },
        "archive": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": RETURN.stat().st_size, "sha256": sha_file(RETURN), "memberCount": len(archive_members)},
        "decisionObservation": {"batchAccepted": False, "acceptedIds": IDS, "unacceptedIds": BLOCKED_IDS, "applied": False, "authority": BEFORE},
        "verificationCounts": {"dataAndClock": 48_108, "source": 307, "metadata": 600, "package": 765, "savedArtifactRoundTrip": 534, "caseFiles": 100, "events": 3_851, "eventOperations": 15_404, "members": 175},
        "note": "The delivery JSON reports batchAccepted=false because three of seven identities remain held. DIRECTOR_DECISION.json is authoritative per identity and records exact static authored acceptance for the four listed IDs. The external JSON is identified by its ChatGPT Library artifact ID; the return ZIP and its internal exact member manifest are independently preserved and audited.",
    }
    write_json(RECV / "RETURN182_DELIVERY_OBSERVATION.json", observation)
    (STAGING / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(json_bytes(observation))
    (STAGING / "RETURN_INDEPENDENT_AUDIT.json").write_bytes(INDEPENDENT_AUDIT.read_bytes())
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_bytes)

    casebook_path = STAGING / "CASEBOOK.json.gz"
    casebook_hash = hashlib.sha256()
    casebook_bytes = 0
    with zipfile.ZipFile(RETURN, "r") as archive, casebook_path.open("wb") as raw_out:
        with archive.open("CASEBOOK.json", "r") as casebook_in, gzip.GzipFile(fileobj=raw_out, mode="wb", mtime=0, compresslevel=9) as compressed:
            for block in iter(lambda: casebook_in.read(1024 * 1024), b""):
                casebook_hash.update(block)
                casebook_bytes += len(block)
                compressed.write(block)
    assert casebook_bytes == casebook_info["bytes"] and casebook_hash.hexdigest() == casebook_info["sha256"]

    all_hold_records = hold_register.get("localHolds", []) + hold_register.get("inheritedExactScopeRecords", [])
    hold_ids = [row.get("id", row.get("scopedRecordId")) for row in all_hold_records]
    spell_rows = []
    for pos, sid in enumerate(IDS):
        source_record = procedures_by_id[sid]
        native = catalog_rows[sid]
        local_procedure = copy.deepcopy(source_record["localProcedure"])
        shared_procedure = copy.deepcopy(source_record["sharedProcedure"])
        accepted_procedure = {
            "id": source_record["id"],
            "spellId": sid,
            "status": "director-accepted static authored procedure; qualifications retained; unapplied",
            "accepted": True,
            "applied": False,
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "sourceRecordPointer": f"DIRECTOR_RETURN/PROCEDURES.json#/{pos}",
            "localProcedure": local_procedure,
            "sharedProcedure": shared_procedure,
            "qualifications": copy.deepcopy(source_record["qualifications"]),
            "repair182Clarifications": copy.deepcopy(source_record["repair182Clarifications"]),
            "directorDecisionId": decision_id,
        }
        spell_rows.append({
            "id": sid,
            "name": native["name"],
            "procedure": accepted_procedure,
            "directorProcedureRecord": copy.deepcopy(source_record),
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "questionDispositions": copy.deepcopy(source_record["originalQuestionsUnchanged"]),
            "runtimeSelectionEnabled": False,
        })

    return_binding = bind(RETURN)
    delivery_binding = bind(RECV / "RETURN182_DELIVERY_OBSERVATION.json")
    audit_binding = bind(INDEPENDENT_AUDIT)
    packet_binding = bind(SOURCE_ARCHIVE)
    candidate_binding = bind(SOURCE_CANDIDATE)
    archive_only_members = sorted(set(archive_members) - set(DIRECTOR_FILES) - {"CASEBOOK.json", "SOURCE_CONFERENCE_CANDIDATE.json"})
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9-psychicfear7-reviewed-182",
        "status": "EXACT_FOUR_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope": "Exactly the four per-identity GPT-accepted Rank9 Psychic Fear7 static authored procedures. The aggregate seven-identity batch remains unaccepted. Native cards, catalog rows, class access, source status, accepted interfaces and global rules remain unchanged. Three exact identities remain pending on PF182-B01/B02; runtime selection stays disabled and no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "excludedPendingIds": excluded_pending,
        "sharedRules": {"scope": "Shared authored rules remain local to these four exact identities; no global rule or accepted interface is changed.", "perSpellCommon": {sid: copy.deepcopy(procedures_by_id[sid]["sharedProcedure"]) for sid in IDS}},
        "spells": spell_rows,
        "questionDispositions": copy.deepcopy(questions_doc),
        "originalObligations": obligations_doc,
        "futureCaseDispositions": case_dispositions,
        "returnCounts": counts,
        "applicationCountSummary": {"procedures": 4, "questions": 25, "mainCases": 14, "branches": 86, "caseRecords": 100, "events": 3_851, "eventOperations": 15_404, "proposalOperations": 28, "totalIndexedHoldRecords": counts["totalIndexedHoldRecords"], "dataAndScopedSemanticChecks": 48_108, "failedChecks": 0},
        "holdIds": hold_ids,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLD_REGISTER.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROCEDURE_PROPOSALS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip with mtime=0; exact decompression reproduces the CASEBOOK.json member of the bound director ZIP",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_bytes, "sha256": casebook_hash.hexdigest()},
        "directorReturnArchive": return_binding,
        "directorReturnArchiveBinding": return_binding,
        "directorDeliveryObservation": delivery_binding,
        "independentReturnAudit": audit_binding,
        "archiveOnlyMembers": archive_only_members,
        "archiveOnlyRationale": "All 175 byte-exact members remain in the bound director ZIP. The 100-case aggregate is additionally preserved as a deterministic gzip. The accepted four identities' 53 standalone cases were independently replayed through 1,387 events and 5,548 forward/inverse operations before application.",
        "sourceConferenceArchive": packet_binding,
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "sourceConferenceCandidateBinding": candidate_binding,
        "standaloneProcedures": "DIRECTOR_RETURN/STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
        "directorDecisionId": decision_id,
        "directorReturnDeliveryObservation": {"archiveBytes": return_binding["bytes"], "archiveSha256": return_binding["sha256"], "batchAccepted": False, "acceptedIds": IDS, "unacceptedIds": BLOCKED_IDS, "appliedAtDecision": False, "memberCount": len(archive_members), "passedDataChecks": 48_108, "passedSourceChecks": 307, "passedMetadataChecks": 600, "passedPackageChecks": 765, "savedArtifactChecks": 534, "independentAuditChecks": audit["checksPassed"], "independentAuditFailures": audit["checksFailed"]},
        "sourceAuthorityAtDecision": copy.deepcopy(decision["authorityUnchanged"]),
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
        "id": "RANK9-PSYCHICFEAR7-CANDIDATE-PACKAGE-MANIFEST-182",
        "sourceArchive": return_binding,
        "sourceDeliveryObservation": delivery_binding,
        "independentAudit": audit_binding,
        "sourceConferenceArchive": packet_binding,
        "sourceConferenceCandidate": candidate_binding,
        "files": package_files,
        "excludedFromBindings": ["CANDIDATE_PACKAGE_MANIFEST.json", "MODEL.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
        "archiveOnlyMembers": archive_only_members,
    }
    write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    model["candidatePackageManifestBinding"] = bind(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json")
    write_json(STAGING / "MODEL.json", model)
    model_binding = bind(STAGING / "MODEL.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json")
    casebook_binding = bind_stream(STAGING / "CASEBOOK.json.gz", f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    hold_binding = bind(STAGING / "DIRECTOR_RETURN/HOLD_REGISTER.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLD_REGISTER.json")
    proposal_binding = bind(STAGING / "DIRECTOR_RETURN/PROCEDURE_PROPOSALS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROCEDURE_PROPOSALS.json")
    decision_binding = bind(STAGING / "DIRECTOR_RETURN/DIRECTOR_DECISION.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json")
    os.replace(STAGING, CANDIDATE)

    exact_acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_EXACT_FOUR_STATIC_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision": "EXACT_FOUR_IDENTITIES_ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": decision_binding,
        "directorReturn": return_binding,
        "deliveryObservation": delivery_binding,
        "independentAudit": audit_binding,
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "batchAccepted": False,
        "countsBefore": {**BEFORE, "scopedInterfaces": 173},
        "countsAfter": {**AFTER, "scopedInterfaces": 173},
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "acceptedProcedures": 4,
        "returnedCaseRecords": 100,
        "returnedEvents": 3_851,
        "returnedEventOperations": 15_404,
        "retainedHolds": counts["totalIndexedHoldRecords"],
        "remainingBlockers": decision["blockers"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all seven identities; only authoredStatus is advanced for the four exact accepted identities.",
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
        "canonicalApplicationPerformed": False,
    }
    director_decision_record = {
        "id": "GPT-DIRECTOR-DECISION-PSYCHICFEAR7-182",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT},
        "decisionId": decision_id,
        "batchAccepted": False,
        "accepted": False,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "remainingBlockingDefects": decision["blockers"],
        "perIdentityAccepted": {sid: True for sid in IDS},
        "verification": {"independentAudit": audit, "returnMembers": 175, "caseRecords": 100, "events": 3_851, "eventOperations": 15_404, "dataChecks": 48_108, "sourceChecks": 307, "metadataChecks": 600, "packageChecks": 765, "savedArtifactChecks": 534, "acceptedCaseReplay": audit["independentAcceptedCaseReplay"]},
        "acceptedArchive": return_binding,
        "deliveryObservation": delivery_binding,
        "scope": decision["qualification"],
        "retainedBoundary": "The four exact records are accepted for static authored review only. Psychic Scream remains blocked on authoritative anatomy/head consequences; Mass Phantom Killer and Weird remain blocked on an acquired genuine full-extra-turn source and actor schedule. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "directorMadeNoCanonicalChanges": True,
    }
    write_json(DECISION, director_decision_record)
    exact_acceptance["directorDecision"] = bind(DECISION)
    write_json(ACCEPTANCE, exact_acceptance)

    receipt = {
        "id": "RANK9-PSYCHICFEAR7-GPT-RETURN-182",
        "recordedAtUtc": ts,
        "status": "DIRECTOR_PARTIALLY_ACCEPTED_FOUR_EXACT_IDENTITIES; THREE_REMAIN_BLOCKED; INDEPENDENT_AUDIT_PASSED",
        "source": director_decision_record["source"],
        "decisionId": decision_id,
        "batchAccepted": False,
        "accepted": False,
        "appliedAtDecision": False,
        "reviewedIds": ALL_IDS,
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "blockingDefects": decision["blockers"],
        "directorReturn": return_binding,
        "deliveryObservation": delivery_binding,
        "independentAudit": audit_binding,
        "sourceAuthority": copy.deepcopy(decision["authorityUnchanged"]),
        "counts": counts,
        "qualifications": copy.deepcopy(decision["qualification"]),
        "perIdentityAccepted": {sid: True for sid in IDS},
    }
    write_json(RECEIPT, receipt)
    exact_acceptance["directorReturnReceipt"] = bind(RECEIPT)
    write_json(ACCEPTANCE, exact_acceptance)

    shutil.copyfile(INDEX, BACKUP)
    assert BACKUP.read_bytes() == before_bytes
    app = {
        "id": APP_ID,
        "recordedAtUtc": ts,
        "status": "APPLIED_FOUR_EXACT_AUTHORED_PROCEDURES_WITH_THREE_RETAINED_PENDING_BLOCKERS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact GPT-accepted ordinary-spell identity, push the batch to GitHub, and continue until all pending identities are applied.",
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "batchAccepted": False,
        "directorAcceptance": bind(ACCEPTANCE),
        "directorDecision": bind(DECISION),
        "directorReturnReceipt": bind(RECEIPT),
        "directorReturn": return_binding,
        "deliveryObservation": delivery_binding,
        "independentAudit": audit_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "indexBefore": bind(BACKUP, raw=before_bytes),
        "counts": {"before": {**BEFORE, "scopedInterfaces": 173}, "after": {**AFTER, "scopedInterfaces": 173}},
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "returnedCaseRecords": 100,
        "acceptedCaseRecordsIndependentlyReplayed": audit["independentAcceptedCaseReplay"]["cases"],
        "acceptedEventsIndependentlyReplayed": audit["independentAcceptedCaseReplay"]["events"],
        "acceptedEventOperationsIndependentlyReplayed": audit["independentAcceptedCaseReplay"]["forwardAndInverseOperations"],
        "retainedIndexedHolds": counts["totalIndexedHoldRecords"],
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
            "procedureFile": "../spell_candidates/rank9psychicfear7_reviewed_182/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/sharedRules/perSpellCommon/{sid}",
            "manuscript": "../../../docs/spells/candidates/RANK9_PSYCHICFEAR7_REVIEWED_182.md",
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
            "sourceCandidateBinding": candidate_binding,
            "candidatePackageManifestBinding": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
            "retainedHoldsBinding": hold_binding,
            "procedureSourceBinding": decision_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": exact_acceptance["decision"],
            "authoredAcceptanceReceipt": bind(ACCEPTANCE),
            "authoredApplicationReceipt": application_binding,
        })
        assert updated["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review"
        operations.append({"op": "replace-entry", "identity": sid, "index": index_position, "before": copy.deepcopy(old), "after": copy.deepcopy(updated)})
        after["entries"][index_position] = updated
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9psychicfear7_reviewed_182/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "excludedPendingIds": excluded_pending,
        "authority": bind(ACCEPTANCE),
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "sourceArchive": return_binding,
        "sourceConferenceArchive": packet_binding,
        "casebookBinding": casebook_binding,
        "holdsBinding": hold_binding,
        "candidatePackageManifestBinding": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "scope": exact_acceptance["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 759, "pending": 89}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after_set = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 4 and pending_after_set == live_pending - ID_SET and len(pending_after_set) == 89
    assert sum(row["authoredStatus"] == "reviewed-authored-operational-playtest" for row in after["entries"]) == 759
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    write_json(OPERATIONS, {"id": "RANK9-PSYCHICFEAR7-INDEX-OPERATIONS-182", "before": bind(BACKUP, raw=before_bytes), "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)}, "operations": operations, "inverse": {"semanticExact": True, "restores": "four identity rows, aggregate authored counts, standalone-envelope array and representation count"}, "onlyIdentityIds": IDS})
    temp_index = INDEX.with_suffix(".json.psychicfear7-182.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority_after = {"reviewedApplied": 759, "pending": 89, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 483, "scopedInterfaces": 173}
    remaining_groups = []
    for group in queue_before["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in pending_after_set]
        if left:
            row = copy.deepcopy(group)
            row["pendingIds"] = left
            row["pendingCount"] = len(left)
            if set(group["pendingIds"]) & ID_SET:
                row["freshPacketRequiredForCurrentAuthority"] = True
                row["status"] = "PENDING_FRESH_DIRECTOR_CONTINUATION_FOR_CURRENT_AUTHORITY"
                row["blockingReturn"] = {"decision": RECEIPT.relative_to(ROOT).as_posix(), "blockers": ["PF182-B01", "PF182-B02"], "ids": BLOCKED_IDS}
                for key in ["submissionReceipt", "submission", "directorReturn", "currentSubmission"]:
                    row.pop(key, None)
            remaining_groups.append(row)
    assert remaining_groups[0]["group"] == "rank9-psychic-fear7" and remaining_groups[0]["pendingIds"] == BLOCKED_IDS and sum(row["pendingCount"] for row in remaining_groups) == 89
    pending_doc = {"id": "CURRENT89-PENDING-IDENTITY-AUDIT-182", "recordedAtUtc": ts, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": after["authoredCounts"], "pendingCount": 89, "pendingIds": sorted(pending_after_set), "allPendingExistInSourceCatalog": pending_after_set <= set(catalog_rows), "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0}
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-182", "recordedAtUtc": ts, "currentAuthority": authority_after, "pendingCount": 89, "currentPendingGroups": remaining_groups, "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": len(IDS), "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()}})
    write_json(QUEUE_AFTER, queue_after)

    handoff_after = copy.deepcopy(handoff_before)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-182",
        "recordedAtUtc": ts,
        "status": "RANK9_PSYCHIC_FEAR7_PARTIALLY_APPLIED_FOUR_ACCEPTED_THREE_BLOCKED_NEXT_89_PENDING",
        "currentAuthority": authority_after,
        "currentIndexBinding": bind(INDEX),
        "currentCatalogBinding": bind(CATALOG),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 89, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(), "applicationValidation": {"path": VALIDATION.relative_to(ROOT).as_posix()}},
        "nextGroup": "rank9-psychic-fear7",
        "nextPendingCount": 3,
        "retainedBoundary": "Do not redo the four accepted/applied Psychic Fear7 identities, feats, or completed cohorts. Psychic Scream remains pending on authoritative current-form head anatomy and positive head consequence. Mass Phantom Killer and Weird remain pending on a currently authorized acquired genuine full-extra-turn grant and legal actor schedule. Continue only on these three exact pending identities and other open queue groups.",
        "resumePriority": "Prepare a fresh, narrowly scoped continuation for the three remaining rank9-psychic-fear7 identities against current 759/89 authority for the same GPT director. Seek source-qualified resolution of PF182-B01/B02 only from already authorized bindings or newly available exact sources; preserve explicit holds where facts remain unavailable. Independently audit each return, apply only exact per-identity accepted IDs, push each batch, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": "rank9-psychic-fear7", "ids": BLOCKED_IDS, "freshPacketRequiredForCurrentAuthority": True, "blockers": ["PF182-B01", "PF182-B02"], "request": "Continue only the three unaccepted identities; do not reopen the four accepted/applied identities or other completed cohorts."},
        "currentQueueBinding": bind(QUEUE_AFTER),
        "directorSubmission": {"status": "partial-acceptance-four-applied-three-blocked", "conversation": CHAT, "receipt": bind(RECEIPT), "archive": return_binding, "acceptedIds": IDS, "appliedIds": IDS, "unacceptedIds": BLOCKED_IDS, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
        "currentSubmissionBinding": bind(RECEIPT),
        "appliedDirectorReturn": {"decisionId": decision_id, "archive": return_binding, "deliveryObservation": delivery_binding, "independentAudit": audit_binding, "batchAccepted": False, "accepted": False, "applied": True, "acceptedIds": IDS, "unacceptedIds": BLOCKED_IDS},
        "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(),
    })
    write_json(HANDOFF_AFTER, handoff_after)

    manuscript = [
        "# Rank 9 Psychic Fear7 — accepted static procedures (Return182)",
        "",
        "Authority: 759 authored-reviewed / 89 pending / 0 accepted-unapplied. The aggregate seven-identity batch was not accepted; the director's per-identity overlay accepts only the four IDs below. The three held identities remain pending.",
        "",
        "| Identity | Status | Native class/school access |",
        "|---|---|---|",
    ]
    for sid in IDS:
        card = catalog_rows[sid]
        routes = ", ".join(f"{cls} {row.get('school')}" for cls, row in card.get("classAccess", {}).items())
        manuscript.append(f"| `{sid}` | accepted; applied via RANK9-PSYCHICFEAR7-APPLICATION-182 | {routes} |")
    manuscript += ["", "## Remaining blockers", "", "- `psychic-scream`: PF182-B01, source-qualified current-form head anatomy and a positive head consequence remain unavailable.", "- `mass-phantom-killer`, `weird`: PF182-B02, no acquired genuine full-extra-turn grant and legal actor schedule is evidenced.", "", "The exact authored language, traces, dispositions, qualifications, and case evidence remain in the bound candidate package and Return182 ZIP. This acceptance is static authored review only. Runtime selection, source/access unblocking, human play, balance, cosmology, domain closure, and release remain unapproved.", ""]
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text("\n".join(manuscript), encoding="utf-8")

    validation_checks = [
        {"check": "Exactly four per-identity director acceptances were applied", "passed": [op["identity"] for op in operations] == IDS and all(op["after"]["authoredStatus"] == "reviewed-authored-operational-playtest" for op in operations)},
        {"check": "The three unaccepted identities remain pending", "passed": all(after["entries"][next(i for i, row in enumerate(after["entries"]) if row["id"] == sid)]["authoredStatus"] == "pending-authored-procedure" for sid in BLOCKED_IDS)},
        {"check": "Authority updates exactly from 755/93 to 759/89 with 483 complete procedures", "passed": after["authoredCounts"] == {"reviewed": 759, "pending": 89} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 483},
        {"check": "All 89 pending IDs equal the prior set minus the four accepted identities", "passed": pending_after_set == live_pending - ID_SET and pending_doc["pendingCount"] == 89 and pending_doc["allPendingExistInSourceCatalog"]},
        {"check": "Catalog and every native card/access/source row remain unchanged", "passed": CATALOG.read_bytes() == catalog_bytes and all(after["entries"][next(i for i, row in enumerate(after["entries"]) if row["id"] == sid)]["sourceStatus"] == "blocked-pending-operational-review" for sid in IDS)},
        {"check": "Index operation inverse restores the exact pre-application index", "passed": inverse == before and sha(INDEX.read_bytes()) == sha(after_bytes)},
        {"check": "The GPT aggregate remains unaccepted while the four exact identity overlay remains authoritative", "passed": decision["batchAccepted"] is False and decision["accepted"] is False and decision["acceptedIds"] == IDS and all(decisions[sid]["accepted"] is True for sid in IDS)},
        {"check": "Return archive, audit, source conference, casebook and candidate package bindings are present", "passed": model["directorReturnArchive"]["sha256"] == audit["archive"]["sha256"] and model["casebookSourceArchiveMemberBinding"]["bytes"] == casebook_bytes and sha_file(CANDIDATE / "CASEBOOK.json.gz") == casebook_binding["sha256"] and model["candidatePackageManifestBinding"]["sha256"] == sha_file(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")},
        {"check": "Runtime remains disabled and closed cohorts remain closed", "passed": model["runtimeSelectionEnabled"] is False and pending_doc["closed335AndCompletedCohortsReopened"] is False and app["closedCohortsReopened"] is False},
    ]
    validation = {
        "id": "RANK9-PSYCHICFEAR7-APPLICATION-VALIDATION-182",
        "recordedAtUtc": ts,
        "status": "PASS" if all(row["passed"] for row in validation_checks) else "FAIL",
        "checksPassed": sum(row["passed"] for row in validation_checks),
        "checksFailed": sum(not row["passed"] for row in validation_checks),
        "checks": validation_checks,
        "acceptedIds": IDS,
        "unacceptedIds": BLOCKED_IDS,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "indexBefore": bind(BACKUP, raw=before_bytes),
        "indexAfter": bind(INDEX),
        "catalog": bind(CATALOG),
        "application": bind(APPLICATION),
        "independentAudit": bind(INDEPENDENT_AUDIT),
        "pendingIdentityAudit": bind(PENDING_AFTER),
        "queueAfter": bind(QUEUE_AFTER),
        "handoffAfter": bind(HANDOFF_AFTER),
        "nextPendingCount": 89,
        "nextGroup": "rank9-psychic-fear7",
        "nextUnacceptedIds": BLOCKED_IDS,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(VALIDATION, validation)
    assert validation["status"] == "PASS", validation_checks

    snapshot_text = (
        "# Current ordinary spell-review checkpoint 182\n\n"
        "Authority is **759 reviewed / 89 pending / 0 accepted-unapplied**, with 483 complete reviewed standalone procedures. Return182 independently passed its package/source/metadata checks and Codex independently replayed 53 accepted-identity cases (1,387 events; 5,548 reversible event operations). Exactly `phantom-armageddon`, `phantom-cataclysm`, `frightful-sovereignty`, and `reality-break` were applied. `psychic-scream`, `mass-phantom-killer`, and `weird` remain pending under PF182-B01/B02.\n\n"
        f"See [handoff 182](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [queue 182](docs/audit/2026-10-08/full-game/director-spell-review-129/{QUEUE_AFTER.name}), [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [independent audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{INDEPENDENT_AUDIT.name}), [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), and [Return182 ZIP](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECV.name}/{RETURN.name}).\n"
    )
    SNAPSHOT.write_text(snapshot_text, encoding="utf-8")
    old_start = START.read_text(encoding="utf-8-sig") if START.exists() else ""
    start_update = (
        "**Current ordinary spell-review checkpoint [182](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_182.json):** GPT's Return182 accepted four exact identities, independently audited and applied: `phantom-armageddon`, `phantom-cataclysm`, `frightful-sovereignty`, and `reality-break`. Authority is **759 reviewed / 89 pending / 0 accepted-unapplied**. Three Rank9 Psychic Fear7 identities remain blocked by PF182-B01/B02. Continue with a fresh, narrowly scoped director continuation; preserve all completed cohorts and apply only exact per-identity acceptances. See [handoff 182](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_182.json) and [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT89_PENDING_IDENTITY_AUDIT_182.json).\n\n"
    )
    START.write_text(start_update + old_start, encoding="utf-8")
    assert CATALOG.read_bytes() == catalog_bytes
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "unacceptedIds": BLOCKED_IDS, "authority": authority_after, "nextGroup": remaining_groups[0]["group"], "nextPendingCount": remaining_groups[0]["pendingCount"], "independentAudit": audit["status"], "applicationValidation": validation["status"], "indexSha256": sha(INDEX.read_bytes()), "catalogUnchanged": True}, indent=2))


if __name__ == "__main__":
    apply()
