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
RECEIVED = AUDIT / "rank9_deathrecovery7_return184_received"
RETURN = RECEIVED / "DD_Rank9_DeathRecovery7_Director_Return184.zip"
DELIVERY = RECEIVED / "DD_Rank9_DeathRecovery7_Director_Return184_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_DEATHRECOVERY7_RETURN184_INDEPENDENT_AUDIT.json"
VERIFY = AUDIT / "verify_death_recovery7_return184.py"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_182.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_182.json"
PENDING_BEFORE = AUDIT / "CURRENT89_PENDING_IDENTITY_AUDIT_182.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Death_Recovery_7_Source_Conference_01.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_death_recovery_7_source_conference_01.json"
IDS = ["soul-harvest", "power-word-kill", "thread-severance", "wail-of-the-banshee"]
UNACCEPTED = ["doom", "final-word", "eternal-pact"]
GROUP_IDS = ["doom", "soul-harvest", "final-word", "eternal-pact", "power-word-kill", "thread-severance", "wail-of-the-banshee"]
BLOCKERS = {"doom": "DR184-B03", "final-word": "DR184-B01", "eternal-pact": "DR184-B02"}
BEFORE = {"reviewedApplied": 759, "pending": 89, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 483, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 763, "pending": 85, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 487, "scopedInterfaces": 173}
REVIEW_ID = "RANK9-DEATHRECOVERY7-EXACT-AUTHORED-ACCEPTANCE-184"
APP_ID = "RANK9-DEATHRECOVERY7-APPLICATION-184"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9deathrecovery7_reviewed_184"
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_DEATHRECOVERY7_REVIEWED_184.md"
BACKUP = AUDIT / "authored_review_index.before_deathrecovery7_184.json"
DECISION = AUDIT / "RANK9_DEATHRECOVERY7_DIRECTOR_DECISION_184.json"
ACCEPTANCE = AUDIT / "RANK9_DEATHRECOVERY7_EXACT_ACCEPTANCE_184.json"
RECEIPT = AUDIT / "RANK9_DEATHRECOVERY7_GPT_RETURN_184.json"
OBSERVATION = RECEIVED / "RETURN184_DELIVERY_OBSERVATION.json"
APPLICATION = AUDIT / "RANK9_DEATHRECOVERY7_APPLICATION_184.json"
OPERATIONS = AUDIT / "RANK9_DEATHRECOVERY7_INDEX_OPERATIONS_184.json"
PENDING_AFTER = AUDIT / "CURRENT85_PENDING_IDENTITY_AUDIT_184.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_184.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_184.json"
VALIDATION = AUDIT / "RANK9_DEATHRECOVERY7_APPLICATION_VALIDATION_184.json"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-26_SPELL_REVIEW_184.md"
START = ROOT / "START_HERE.md"
DIRECTOR_FILES = [
    "ACTOR_PROFILES.json",
    "BLOCKERS.json",
    "CASE_INDEX.json",
    "CLOCK_LEDGER.json",
    "COMPARISON_BOUNDARIES.json",
    "COUNTS.json",
    "COVERAGE.json",
    "CURRENT_CONTEXT_184.json",
    "DATA_INTEGRITY_CHECK.json",
    "DIRECTOR_DECISION.json",
    "EXTRA_TURN_EVIDENCE_SCOPE.json",
    "HOLD_REGISTER.json",
    "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
    "MEMBER_MANIFEST.json",
    "NEXT_QUEUE_HANDOFF.json",
    "ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json",
    "PACKAGING_POLICY.json",
    "PROCEDURES.json",
    "PROCEDURE_SOURCE_MAP.json",
    "PROPOSAL_OPERATIONS.json",
    "QUESTION_DISPOSITIONS.json",
    "README.md",
    "SEMANTIC_CHECK_DETAILS.json",
    "SOURCE_BINDINGS.json",
    "SOURCE_CHECK.json",
    "STANDALONE_PROCEDURES.md",
    "VALIDATION_INPUT_BINDINGS.json",
]
GPT_TEXT = (
    "Accepted=true, applied=false: soul-harvest, power-word-kill, thread-severance, wail-of-the-banshee.\n\n"
    "Unaccepted:\n"
    "doom — DR184-B03: genuine full-extra-turn evidence remains unavailable.\n"
    "final-word — DR184-B01: lawful soul capture and dependent reserve-payment traces remain held.\n"
    "eternal-pact — DR184-B02: eligible successful return and dependent recurrence traces remain held.\n\n"
    "The package contains 7 procedures, 22 answered questions, 103 cases, 2,074 events, 8,324 reversible operations and 13 holds. All 39,177 static checks and 767 packaging checks passed. Saved ZIP read-back matches 82,015,677 bytes, including all 190 member hashes and CRCs.\n\n"
    "DD_Rank9_DeathRecovery7_Director_Return184.zip\n"
    "DD_Rank9_DeathRecovery7_Director_Return184_DELIVERY.json\n\n"
    "Canonical authority remains 759 applied / 89 pending. Nothing was applied. All source/access, physical, runtime, human-play, balance, cosmology, domain-closure and release qualifications remain.\n\n"
    "Next group: rank9-defense-form8, following your audited application and authority refresh."
)


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


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{path}"], cwd=ROOT)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def bind(path: Path, rel: str | None = None, raw: bytes | None = None) -> dict:
    data = raw if raw is not None else path.read_bytes()
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def bind_stream(path: Path, rel: str) -> dict:
    return {"path": rel, "bytes": path.stat().st_size, "sha256": sha_file(path)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def preflight() -> dict:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert head == "25273775f16cf9877c758b3b923f672e60d6a44b", head
    audit = read_json(INDEPENDENT_AUDIT)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["acceptedIds"] == IDS
    before_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    before = read_json(INDEX)
    catalog_rel = CATALOG.relative_to(ROOT).as_posix()
    catalog = json.loads(subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{catalog_rel}"], cwd=ROOT).decode("utf-8"))
    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)
    entries = {row["id"]: row for row in before["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == {"reviewed": 759, "pending": 89}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 483
    assert len(live_pending) == 89 and set(IDS) <= live_pending
    assert pending_before["pendingCount"] == 89 and set(GROUP_IDS) <= set(pending_before["pendingIds"])
    assert handoff["currentAuthority"] == queue["currentAuthority"] == BEFORE
    target_group = next(row for row in queue["currentPendingGroups"] if row["group"] == "rank9-death-recovery7")
    assert target_group["pendingIds"] == GROUP_IDS and target_group["pendingCount"] == 7
    assert all(entries[s]["authoredStatus"] == "pending-authored-procedure" and entries[s]["sourceStatus"] == "blocked-pending-operational-review" for s in GROUP_IDS)
    assert all(catalog_rows[s]["operational"] is None for s in GROUP_IDS)
    assert CANDIDATE.exists() is False and STAGING.exists() is False
    outputs = [OBSERVATION, BACKUP, DECISION, ACCEPTANCE, RECEIPT, APPLICATION, OPERATIONS, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, VALIDATION, MANUSCRIPT, SNAPSHOT]
    existing = [str(path) for path in outputs if path.exists()]
    assert not existing, f"Application outputs already exist; inspect before retrying: {existing}"
    assert sha_file(RETURN) == audit["archive"]["sha256"] and RETURN.stat().st_size == audit["archive"]["bytes"]
    assert CATALOG.read_bytes() == catalog_bytes
    return locals()


def apply() -> None:
    data = preflight()
    ts = now()
    before = data["before"]
    before_bytes = data["before_bytes"]
    catalog_bytes = data["catalog_bytes"]
    catalog_rows = data["catalog_rows"]
    queue_before = data["queue"]
    handoff_before = data["handoff"]
    live_pending = data["live_pending"]
    entries = data["entries"]
    audit = data["audit"]
    delivery_counts = read_json(DELIVERY)["counts"]
    excluded_pending = sorted(live_pending - set(IDS))
    assert len(excluded_pending) == 85

    with zipfile.ZipFile(RETURN, "r") as archive:
        member_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        archive_members = archive.namelist()
        procedures_doc = json.loads(archive.read("PROCEDURES.json"))
        questions_doc = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        obligations_doc = json.loads(archive.read("ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json"))
        case_index = json.loads(archive.read("CASE_INDEX.json"))
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        coverage = json.loads(archive.read("COVERAGE.json"))
        source_candidate_bytes = archive.read("SOURCE_CONFERENCE_CANDIDATE_01.json")
        casebook_info = next(row for row in member_manifest["members"] if row["path"] == "CASEBOOK.json")
        source_members = {name: archive.read(name) for name in DIRECTOR_FILES}
        procedures_by_id = {row["id"]: row for row in procedures_doc["spells"]}
        decisions = {row["id"]: row for row in decision["decisions"]}
        assert decision["acceptedIds"] == IDS and decision["unacceptedIds"] == UNACCEPTED
        assert set(procedures_by_id) == set(GROUP_IDS)
        assert all(decisions[s]["accepted"] and not decisions[s]["applied"] for s in IDS)
        assert all(not decisions[s]["accepted"] and not decisions[s]["applied"] for s in UNACCEPTED)
        assert all(procedures_by_id[s]["accepted"] and not procedures_by_id[s]["applied"] for s in IDS)
        assert all(procedures_by_id[s]["nativeCardUnchanged"] == catalog_rows[s] for s in IDS)
        assert all(not decisions[s]["blockerIds"] for s in IDS)
        assert {s: decisions[s]["blockerIds"][0] for s in UNACCEPTED} == BLOCKERS

    source_candidate_bytes_git = git_blob("DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_death_recovery_7_source_conference_01.json")
    source_archive_bytes_git = git_blob("docs/audit/2026-10-08/full-game/DD_Rank9_Death_Recovery_7_Source_Conference_01.zip")
    assert source_candidate_bytes == source_candidate_bytes_git
    assert SOURCE_ARCHIVE.read_bytes() == source_archive_bytes_git

    return_binding = bind(RETURN)
    delivery_binding = bind(DELIVERY)
    audit_binding = bind(INDEPENDENT_AUDIT)
    packet_binding = bind(SOURCE_ARCHIVE)
    candidate_binding = bind(SOURCE_CANDIDATE, raw=source_candidate_bytes)
    source_authority = copy.deepcopy(decision["sourceAuthority"])
    assert source_authority == BEFORE

    observation = {
        "id": "RANK9-DEATHRECOVERY7-RETURN184-DELIVERY-OBSERVATION",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT},
        "libraryArtifacts": {
            "returnArchive": {"fileId": "libfile_f58ab47381c08191830a6a07989aee79", "fileName": RETURN.name},
            "deliveryManifest": {"fileId": "libfile_c48a040bd478819183f05205e219abea", "fileName": DELIVERY.name},
        },
        "archive": {"path": return_binding["path"], "bytes": return_binding["bytes"], "sha256": return_binding["sha256"], "memberCount": len(archive_members)},
        "decisionObservation": {"batchAccepted": False, "acceptedIds": IDS, "unacceptedIds": UNACCEPTED, "appliedAtDecision": False, "authority": BEFORE, "exactVisibleResponse": GPT_TEXT},
        "verificationCounts": {"staticDataChecks": counts["authoredStaticValidationChecks"], "dataIntegrityChecks": counts["dataIntegrityChecks"], "packageIntegrityChecks": delivery_counts["packageIntegrityChecks"], "caseRecords": counts["cases"], "events": counts["events"], "eventOperations": counts["eventOperations"], "proposalOperations": counts["proposalOperations"], "totalReversibleOperations": counts["totalReversibleOperations"], "members": len(archive_members), "acceptedCaseReplay": audit["independentReplay"]},
        "note": "The aggregate seven-identity batch remains unaccepted because three identities retain explicit evidence blockers. The four exact per-identity decisions below are accepted for static authored review only; no source/access, runtime, playtest, balance, cosmology, domain-closure or release approval is inferred.",
    }
    write_json(OBSERVATION, observation)
    delivery_binding = bind(OBSERVATION)

    STAGING.mkdir(parents=True, exist_ok=False)
    director_dir = STAGING / "DIRECTOR_RETURN"
    for name, raw in source_members.items():
        target = director_dir / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(source_candidate_bytes)
    (STAGING / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(json_bytes(observation))
    (STAGING / "RETURN_INDEPENDENT_AUDIT.json").write_bytes(INDEPENDENT_AUDIT.read_bytes())

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
    casebook_source_binding = {"path": "CASEBOOK.json", "bytes": casebook_bytes, "sha256": casebook_hash.hexdigest()}

    hold_binding = bind(director_dir / "HOLD_REGISTER.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLD_REGISTER.json")
    proposal_binding = bind(director_dir / "PROPOSAL_OPERATIONS.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json")
    decision_binding = bind(director_dir / "DIRECTOR_DECISION.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json")
    casebook_binding = bind_stream(casebook_path, f"{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz")
    spell_rows = []
    for position, sid in enumerate(IDS):
        source_row = procedures_by_id[sid]
        native = catalog_rows[sid]
        spell_rows.append({
            "id": sid,
            "name": native["name"],
            "procedure": {
                "id": f"RANK9-DEATHRECOVERY7-STATIC-PROCEDURE-184-{sid.upper()}",
                "spellId": sid,
                "status": "director-accepted static authored procedure; applied to the authored review index; runtime remains disabled",
                "accepted": True,
                "applied": False,
                "nativeCardAndAccessUnchanged": copy.deepcopy(native),
                "sourceRecordPointer": f"DIRECTOR_RETURN/PROCEDURES.json#/spells/{GROUP_IDS.index(sid)}",
                "procedureText": source_row["procedure"],
                "sharedRules": copy.deepcopy(source_row["sharedRules"]),
                "questionIds": copy.deepcopy(source_row["questionIds"]),
                "directorDecisionId": "DD-RANK9-DEATHRECOVERY7-DIRECTOR-RETURN184",
            },
            "directorProcedureRecord": copy.deepcopy(source_row),
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "questionDispositions": {q["id"]: copy.deepcopy(q) for q in questions_doc["questions"] if q["id"] in source_row["questionIds"]},
            "runtimeSelectionEnabled": False,
        })
    unaccepted_summary = [{"id": sid, "accepted": False, "applied": False, "blockerIds": decisions[sid]["blockerIds"], "caseIds": decisions[sid]["caseIds"], "holdIds": decisions[sid]["holdIds"]} for sid in UNACCEPTED]
    all_hold_ids = [row["id"] for row in hold_register["holds"]]
    archive_only_members = sorted(set(archive_members) - set(DIRECTOR_FILES) - {"CASEBOOK.json", "SOURCE_CONFERENCE_CANDIDATE_01.json"})
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9-deathrecovery7-reviewed-184",
        "status": "EXACT_FOUR_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_THREE_RETAINED_PENDING_BLOCKERS",
        "scope": "Exactly soul-harvest, power-word-kill, thread-severance and wail-of-the-banshee are accepted as static authored procedures and applied to the authored review index. The seven-identity batch remains unaccepted. Doom, final-word and eternal-pact remain pending on DR184-B03, DR184-B01 and DR184-B02. Native cards, catalog rows, class access, source status, accepted interfaces and global rules remain unchanged. Runtime selection stays disabled; no runtime, source/access, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
        "excludedPendingIds": excluded_pending,
        "unacceptedDecisions": unaccepted_summary,
        "sharedRules": {"scope": "The exact authored shared mechanics remain local to the four accepted identity rows; no global rule or accepted interface is changed.", "perSpellCommon": {sid: copy.deepcopy(procedures_by_id[sid]["sharedRules"]) for sid in IDS}},
        "spells": spell_rows,
        "questionDispositions": copy.deepcopy(questions_doc),
        "originalQuestionsAndObligations": obligations_doc,
        "caseCoverage": {"file": "DIRECTOR_RETURN/CASE_INDEX.json", "binding": bind(director_dir / "CASE_INDEX.json", f"{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/CASE_INDEX.json"), "questions": len(coverage["questions"]), "futureObligations": len(coverage["originalFutureObligations"])},
        "returnCounts": counts,
        "independentAcceptedCaseReplay": audit["independentReplay"],
        "applicationCountSummary": {"procedures": len(IDS), "unacceptedProcedures": len(UNACCEPTED), "answeredQuestionDispositions": counts["answeredQuestionDispositions"], "caseRecords": counts["cases"], "events": counts["events"], "eventOperations": counts["eventOperations"], "proposalOperations": counts["proposalOperations"], "totalReversibleOperations": counts["totalReversibleOperations"], "staticChecks": counts["authoredStaticValidationChecks"], "packageChecks": delivery_counts["packageIntegrityChecks"], "holds": counts["holds"]},
        "holdIds": all_hold_ids,
        "holdRegisterFile": "DIRECTOR_RETURN/HOLD_REGISTER.json",
        "proposalOperationsFile": "DIRECTOR_RETURN/PROPOSAL_OPERATIONS.json",
        "casebookFile": "CASEBOOK.json.gz",
        "casebookEncoding": "gzip with mtime=0; exact decompression reproduces the CASEBOOK.json member of the bound director ZIP",
        "casebookSourceArchiveMemberBinding": casebook_source_binding,
        "directorReturnArchive": return_binding,
        "directorDeliveryObservation": delivery_binding,
        "independentReturnAudit": audit_binding,
        "archiveOnlyMembers": archive_only_members,
        "archiveOnlyRationale": "All 190 byte-exact members remain in the bound Return184 ZIP. The aggregate casebook is additionally retained as deterministic gzip; the four accepted identities' 58 source-bound cases were independently replayed through 1,031 events and 4,124 forward/inverse operations before application.",
        "sourceConferenceArchive": packet_binding,
        "sourceConferenceCandidate": "SOURCE_CONFERENCE_CANDIDATE.json",
        "sourceConferenceCandidateBinding": candidate_binding,
        "standaloneProcedures": "DIRECTOR_RETURN/STANDALONE_PROCEDURES.md",
        "directorDecisionFile": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
        "directorDecisionId": "DD-RANK9-DEATHRECOVERY7-DIRECTOR-RETURN184",
        "sourceAuthorityAtDecision": source_authority,
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
        "id": "RANK9-DEATHRECOVERY7-CANDIDATE-PACKAGE-MANIFEST-184",
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
    os.replace(STAGING, CANDIDATE)

    director_decision_record = {
        "id": "GPT-DIRECTOR-DECISION-DEATHRECOVERY7-184",
        "recordedAtUtc": ts,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": CHAT},
        "decisionId": "DD-RANK9-DEATHRECOVERY7-DIRECTOR-RETURN184",
        "batchAccepted": False,
        "accepted": False,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
        "remainingBlockingDefects": [{"id": BLOCKERS[sid], "spellId": sid} for sid in UNACCEPTED],
        "perIdentityAccepted": {sid: True for sid in IDS},
        "exactVisibleResponse": GPT_TEXT,
        "verification": {"independentAudit": audit_binding, "independentAuditChecks": audit["checksPassed"], "independentAuditFailures": audit["checksFailed"], "returnMembers": len(archive_members), "caseRecords": counts["cases"], "events": counts["events"], "eventOperations": counts["eventOperations"], "dataIntegrityChecks": counts["dataIntegrityChecks"], "packageIntegrityChecks": delivery_counts["packageIntegrityChecks"], "acceptedCaseReplay": audit["independentReplay"]},
        "acceptedArchive": return_binding,
        "deliveryObservation": delivery_binding,
        "scope": "Exact static authored procedure acceptance, individually for four named spells; no application had occurred when GPT decided.",
        "retainedBoundary": "The three unaccepted identities remain pending: Doom lacks authorized genuine full-extra-turn evidence; Final Word lacks lawful soul capture and dependent reserve-payment traces; Eternal Pact lacks eligible successful-return and dependent recurrence traces. No source/access, runtime, human-play, balance, cosmology, domain-closure or release approval is granted.",
        "directorMadeNoCanonicalChanges": True,
    }
    write_json(DECISION, director_decision_record)
    exact_acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": ts,
        "status": "DIRECTOR_ACCEPTED_FOUR_EXACT_STATIC_AUTHORED_PROCEDURES_WITH_THREE_RETAINED_HOLDS",
        "decision": "EXACT_FOUR_IDENTITIES_ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": bind(DECISION),
        "directorReturn": return_binding,
        "deliveryManifest": bind(DELIVERY),
        "deliveryObservation": delivery_binding,
        "independentAudit": audit_binding,
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
        "batchAccepted": False,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProceduresBefore": 483,
        "completeReviewedStandaloneProceduresAfter": 487,
        "acceptedProcedures": len(IDS),
        "returnedCaseRecords": counts["cases"],
        "returnedEvents": counts["events"],
        "returnedEventOperations": counts["eventOperations"],
        "totalReversibleOperations": counts["totalReversibleOperations"],
        "retainedHolds": counts["holds"],
        "remainingBlockers": director_decision_record["remainingBlockingDefects"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all seven; only authoredStatus advances for the four exact accepted identities.",
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "sourceProgramsExecuted": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "releaseApproved": False,
        "canonicalApplicationPerformed": False,
    }
    write_json(ACCEPTANCE, exact_acceptance)
    return_receipt = {
        "id": "RANK9-DEATHRECOVERY7-GPT-RETURN-184",
        "recordedAtUtc": ts,
        "status": "DIRECTOR_PARTIALLY_ACCEPTED_FOUR_EXACT_IDENTITIES; THREE_REMAIN_BLOCKED; INDEPENDENT_AUDIT_PASSED",
        "source": director_decision_record["source"],
        "decisionId": director_decision_record["decisionId"],
        "batchAccepted": False,
        "accepted": False,
        "appliedAtDecision": False,
        "reviewedIds": GROUP_IDS,
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
        "blockingDefects": director_decision_record["remainingBlockingDefects"],
        "exactVisibleResponse": GPT_TEXT,
        "directorReturn": return_binding,
        "deliveryManifest": bind(DELIVERY),
        "deliveryObservation": delivery_binding,
        "independentAudit": audit_binding,
        "sourceAuthority": source_authority,
        "counts": counts,
        "qualifications": copy.deepcopy(decision["qualifications"]),
        "perIdentityAccepted": {sid: True for sid in IDS},
    }
    write_json(RECEIPT, return_receipt)

    app = {
        "id": APP_ID,
        "recordedAtUtc": ts,
        "status": "APPLIED_FOUR_EXACT_AUTHORED_PROCEDURES_WITH_THREE_RETAINED_PENDING_BLOCKERS",
        "reviewId": REVIEW_ID,
        "ownerInstruction": "Apply each exact GPT-accepted ordinary-spell identity, push the batch to GitHub, and continue until pending reaches zero.",
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
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
        "counts": {"before": BEFORE, "after": AFTER},
        "completeReviewedStandaloneProcedures": {"before": 483, "after": 487},
        "returnedCaseRecords": counts["cases"],
        "acceptedCaseRecordsIndependentlyReplayed": audit["independentReplay"]["acceptedCases"],
        "acceptedEventsIndependentlyReplayed": audit["independentReplay"]["acceptedEvents"],
        "acceptedForwardOperationsIndependentlyReplayed": audit["independentReplay"]["forwardOperations"],
        "acceptedInverseOperationsIndependentlyReplayed": audit["independentReplay"]["inverseOperations"],
        "retainedIndexedHolds": counts["holds"],
        "sourceStatusPreservedAsBlocked": True,
        "sourceCatalogChanged": False,
        "nativeSpellCardsChanged": False,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(APPLICATION, app)
    application_binding = bind(APPLICATION)

    shutil.copyfile(INDEX, BACKUP)
    assert BACKUP.read_bytes() == before_bytes
    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(IDS):
        index_position = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_position]
        updated = copy.deepcopy(old)
        updated.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9deathrecovery7_reviewed_184/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure/procedureText",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/sharedRules/perSpellCommon/{sid}",
            "manuscript": "../../../docs/spells/candidates/RANK9_DEATHRECOVERY7_REVIEWED_184.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE.relative_to(ROOT).as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip with mtime=0; exact decompression reproduces the CASEBOOK.json member of the bound director ZIP",
            "casebookSourceArchiveMemberBinding": casebook_source_binding,
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
        "file": "../spell_candidates/rank9deathrecovery7_reviewed_184/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
        "excludedPendingIds": excluded_pending,
        "authority": bind(ACCEPTANCE),
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "sourceArchive": return_binding,
        "sourceConferenceArchive": packet_binding,
        "casebookBinding": casebook_binding,
        "retainedHoldsBinding": hold_binding,
        "candidatePackageManifestBinding": bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "scope": exact_acceptance["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 763, "pending": 85}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 487
    pending_after_set = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 4 and pending_after_set == live_pending - set(IDS) and len(pending_after_set) == 85
    assert sum(row["authoredStatus"] == "reviewed-authored-operational-playtest" for row in after["entries"]) == 763
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_bytes = json_bytes(after)
    write_json(OPERATIONS, {"id": "RANK9-DEATHRECOVERY7-INDEX-OPERATIONS-184", "before": bind(BACKUP, raw=before_bytes), "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_bytes), "sha256": sha(after_bytes)}, "operations": operations, "inverse": {"semanticExact": True, "restores": "four identity rows, aggregate authored counts, standalone-envelope array and complete-procedure representation count"}, "onlyIdentityIds": IDS})
    temp_index = INDEX.with_suffix(".json.deathrecovery7-184.tmp")
    temp_index.write_bytes(after_bytes)
    os.replace(temp_index, INDEX)
    assert CATALOG.read_bytes() == catalog_bytes

    authority_after = AFTER
    remaining_groups = []
    for group in queue_before["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in pending_after_set]
        if left:
            row = copy.deepcopy(group)
            row["pendingIds"] = left
            row["pendingCount"] = len(left)
            if set(group["pendingIds"]) & set(GROUP_IDS):
                row["freshPacketRequiredForCurrentAuthority"] = True
                row["status"] = "PENDING_THREE_EXPLICIT_SOURCE_EVIDENCE_BLOCKERS_CARRIED_FORWARD"
                row["blockingReturn"] = {"decision": RECEIPT.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(), "blockers": [BLOCKERS[s] for s in UNACCEPTED], "ids": UNACCEPTED}
            if row["group"] == "rank9-defense-form8":
                row["freshPacketRequiredForCurrentAuthority"] = True
                row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            remaining_groups.append(row)
    assert sum(row["pendingCount"] for row in remaining_groups) == 85
    defense = next(row for row in remaining_groups if row["group"] == "rank9-defense-form8")
    assert defense["pendingCount"] == 8

    pending_doc = {"id": "CURRENT85-PENDING-IDENTITY-AUDIT-184", "recordedAtUtc": ts, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": after["authoredCounts"], "pendingCount": 85, "pendingIds": sorted(pending_after_set), "allPendingExistInSourceCatalog": pending_after_set <= set(data["catalog_rows"]), "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0}
    assert pending_doc["allPendingExistInSourceCatalog"]
    write_json(PENDING_AFTER, pending_doc)
    defense_next = {"group": defense["group"], "pendingIds": defense["pendingIds"], "pendingCount": defense["pendingCount"], "candidate": defense["candidate"], "archive": defense["archive"], "freshPacketRequiredForCurrentAuthority": True, "status": defense["status"]}
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-184",
        "recordedAtUtc": ts,
        "currentAuthority": authority_after,
        "pendingCount": 85,
        "currentPendingGroups": remaining_groups,
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": PENDING_AFTER.relative_to(AUDIT).as_posix(), "pending": 85, "sha256": sha(PENDING_AFTER.read_bytes())},
        "nextGroup": "rank9-defense-form8",
        "next": defense_next,
        "nextPreparedRequest": defense_next,
        "packetStatus": "RANK9_DEATHRECOVERY7_RETURN184_FOUR_APPLIED_THREE_HELD_763_85",
        "currentSubmission": {"path": RECEIPT.relative_to(AUDIT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": sha_file(RECEIPT)},
        "currentSubmissionBinding": bind(RECEIPT),
        "currentReturnBinding": return_binding,
    })
    write_json(QUEUE_AFTER, queue_after)

    handoff_after = copy.deepcopy(handoff_before)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-184",
        "recordedAtUtc": ts,
        "status": "RANK9_DEATHRECOVERY7_PARTIALLY_APPLIED_FOUR_ACCEPTED_THREE_HELD_NEXT_DEFENSE_FORM8_85_PENDING",
        "currentAuthority": authority_after,
        "currentIndexBinding": bind(INDEX),
        "currentCatalogBinding": bind(CATALOG),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.name, "pendingCount": 85, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": IDS, "count": 4, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(), "applicationValidation": {"path": VALIDATION.relative_to(ROOT).as_posix()}},
        "nextGroup": "rank9-defense-form8",
        "nextPendingCount": 8,
        "retainedBoundary": "Four exact Death/Recovery7 identities are now applied as static authored reviews. Doom, Final Word and Eternal Pact remain pending on DR184-B03/B01/B02; the three Psychic Fear7 identities remain pending on PF182-B01/B02. Preserve all six holds and do not reopen completed or applied cohorts.",
        "resumePriority": "Prepare and send a fresh Rank9 Defense Form8 packet against current 763/85 authority to the same GPT director. Continue in queue order, apply each exact accepted identity after independent audit, and carry all six source-evidence blockers forward without dropping them until pending reaches zero.",
        "nextPreparedRequest": defense_next,
        "currentQueueBinding": bind(QUEUE_AFTER),
        "directorSubmission": {"status": "partial-acceptance-four-applied-three-held", "conversation": CHAT, "receipt": bind(RECEIPT), "archive": return_binding, "acceptedIds": IDS, "appliedIds": IDS, "unacceptedIds": UNACCEPTED, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix()},
        "currentSubmissionBinding": bind(RECEIPT),
        "appliedDirectorReturn": {"decisionId": director_decision_record["decisionId"], "archive": return_binding, "deliveryObservation": delivery_binding, "independentAudit": audit_binding, "batchAccepted": False, "accepted": False, "applied": True, "acceptedIds": IDS, "unacceptedIds": UNACCEPTED},
        "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(),
    })
    write_json(HANDOFF_AFTER, handoff_after)

    manuscript = [
        "# Rank 9 Death/Recovery7 accepted static procedures (Return184)",
        "",
        "Authority: 763 reviewed / 85 pending / 0 accepted-unapplied; 487 complete reviewed standalone procedures. The aggregate seven-identity batch remains unaccepted. Four exact per-identity director acceptances were independently audited and applied.",
        "",
        "| Identity | Status | Native source/access |",
        "|---|---|---|",
    ]
    for sid in IDS:
        native = catalog_rows[sid]
        routes = ", ".join(f"{cls} {row.get('school')}" for cls, row in native.get("classAccess", {}).items())
        manuscript.append(f"| `{sid}` | accepted static authored procedure; applied via `{APP_ID}` | {routes} |")
    manuscript += [
        "",
        "## Remaining source-evidence blockers",
        "",
        "- `doom`: DR184-B03, a genuine authorized full-extra-turn source and legal schedule remain unavailable.",
        "- `final-word`: DR184-B01, lawful soul capture and dependent reserve-payment traces remain held.",
        "- `eternal-pact`: DR184-B02, eligible successful return and dependent recurrence traces remain held.",
        "",
        "The full Return184 ZIP, procedures, cases, source bindings, holds and qualifications remain bound under the candidate package. Runtime selection, source/access authorization, physical/runtime execution, human play, balance, cosmology, domain closure and release remain unapproved.",
        "",
    ]
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text("\n".join(manuscript), encoding="utf-8")

    candidate_package_manifest = read_json(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")
    candidate_package_failures = []
    for member in candidate_package_manifest["files"]:
        member_path = ROOT / member["path"]
        if not member_path.is_file() or member_path.stat().st_size != member["bytes"] or sha_file(member_path) != member["sha256"]:
            candidate_package_failures.append(member["path"])
    casebook_check_hash = hashlib.sha256()
    casebook_check_bytes = 0
    with gzip.open(CANDIDATE / "CASEBOOK.json.gz", "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            casebook_check_hash.update(block)
            casebook_check_bytes += len(block)
    model_file_binding = bind(CANDIDATE / "MODEL.json")
    accepted_index_rows = {row["id"]: row for row in after["entries"] if row["id"] in IDS}
    blocked_index_rows = {row["id"]: row for row in after["entries"] if row["id"] in UNACCEPTED}

    validation_checks = [
        {"check": "Return184 package and independent audit passed before application", "passed": audit["status"] == "PASS" and audit["checksFailed"] == 0 and sha_file(RETURN) == return_binding["sha256"]},
        {"check": "Exactly four per-identity director acceptances were applied", "passed": [op["identity"] for op in operations] == IDS and all(op["after"]["authoredStatus"] == "reviewed-authored-operational-playtest" for op in operations)},
        {"check": "Doom, Final Word and Eternal Pact remain pending under exact blockers", "passed": all(after["entries"][next(i for i, row in enumerate(after["entries"]) if row["id"] == sid)]["authoredStatus"] == "pending-authored-procedure" for sid in UNACCEPTED) and all(decisions[s]["blockerIds"] == [BLOCKERS[s]] for s in UNACCEPTED)},
        {"check": "Authority updates exactly from 759/89 to 763/85 with 487 complete procedures", "passed": after["authoredCounts"] == {"reviewed": 763, "pending": 85} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 487},
        {"check": "All 85 pending IDs equal the prior set minus the four accepted identities", "passed": pending_after_set == live_pending - set(IDS) and pending_doc["pendingCount"] == 85 and pending_doc["allPendingExistInSourceCatalog"]},
        {"check": "Psychic Fear7 holds and the three Death/Recovery7 blockers are retained", "passed": {"psychic-scream", "mass-phantom-killer", "weird"} <= pending_after_set and set(UNACCEPTED) <= pending_after_set},
        {"check": "Catalog and native class/access/source rows remain unchanged", "passed": CATALOG.read_bytes() == catalog_bytes and all(after["entries"][next(i for i, row in enumerate(after["entries"]) if row["id"] == sid)]["sourceStatus"] == "blocked-pending-operational-review" for sid in GROUP_IDS)},
        {"check": "Index operation inverse restores the exact pre-application index", "passed": inverse == before and sha(INDEX.read_bytes()) == sha(after_bytes)},
        {"check": "Return184 aggregate remains unaccepted while only exact identity acceptances are authoritative", "passed": decision["accepted"] is False and decision["applied"] is False and decision["acceptedIds"] == IDS and all(decisions[s]["accepted"] for s in IDS)},
        {"check": "All source, runtime, play, balance, cosmology, closure and release qualifications remain", "passed": model["runtimeSelectionEnabled"] is False and not model["runtimeTestsExecuted"] and not model["sourceProgramsExecuted"] and not model["humanPlaytested"] and not model["balanceApproved"] and not model["cosmologyModified"] and not model["releaseApproved"] and not model["domainClosure"]},
        {"check": "Next director group is the exact eight-identity Rank9 Defense Form8 queue group", "passed": queue_after["nextGroup"] == "rank9-defense-form8" and defense["pendingCount"] == 8 and sum(row["pendingCount"] for row in remaining_groups) == 85},
        {"check": "All candidate package files match manifest size and SHA-256 bindings", "passed": not candidate_package_failures and len(candidate_package_manifest["files"]) == 31, "detail": {"files": len(candidate_package_manifest["files"]), "mismatches": candidate_package_failures}},
        {"check": "CASEBOOK gzip reconstructs the exact Return184 archive member", "passed": casebook_check_bytes == casebook_source_binding["bytes"] and casebook_check_hash.hexdigest() == casebook_source_binding["sha256"], "detail": {"bytes": casebook_check_bytes, "sha256": casebook_check_hash.hexdigest()}},
        {"check": "Four index rows bind the exact static model and preserve native source status; three blockers remain pending", "passed": all(accepted_index_rows[s]["completeEnvelopeBinding"] == model_file_binding and accepted_index_rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in IDS) and all(blocked_index_rows[s]["authoredStatus"] == "pending-authored-procedure" for s in UNACCEPTED)},
    ]
    validation = {
        "id": "RANK9-DEATHRECOVERY7-APPLICATION-VALIDATION-184",
        "recordedAtUtc": ts,
        "status": "PASS" if all(row["passed"] for row in validation_checks) else "FAIL",
        "checksPassed": sum(row["passed"] for row in validation_checks),
        "checksFailed": sum(not row["passed"] for row in validation_checks),
        "checks": validation_checks,
        "acceptedIds": IDS,
        "unacceptedIds": UNACCEPTED,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProceduresBefore": 483,
        "completeReviewedStandaloneProceduresAfter": 487,
        "indexBefore": bind(BACKUP, raw=before_bytes),
        "indexAfter": bind(INDEX),
        "catalog": bind(CATALOG),
        "application": bind(APPLICATION),
        "independentAudit": bind(INDEPENDENT_AUDIT),
        "pendingIdentityAudit": bind(PENDING_AFTER),
        "queueAfter": bind(QUEUE_AFTER),
        "handoffAfter": bind(HANDOFF_AFTER),
        "nextPendingCount": 8,
        "nextGroup": "rank9-defense-form8",
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(VALIDATION, validation)
    assert validation["status"] == "PASS", validation_checks

    operations_record = read_json(OPERATIONS)
    operations_record["after"].update(bind(INDEX))
    write_json(OPERATIONS, operations_record)

    snapshot_text = (
        "# Current ordinary spell-review checkpoint 184\n\n"
        "Authority is **763 reviewed / 85 pending / 0 accepted-unapplied**, with 487 complete reviewed standalone procedures. Return184's independent package audit passed 42 checks, including exact 190-member ZIP bindings and forward/inverse replay of 58 accepted cases (1,031 events; 4,124 operations). Exactly `soul-harvest`, `power-word-kill`, `thread-severance`, and `wail-of-the-banshee` were applied. `doom`, `final-word`, and `eternal-pact` remain pending under DR184-B03/B01/B02. The three Psychic Fear7 holds also remain pending.\n\n"
        f"See [handoff 184](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [queue 184](docs/audit/2026-10-08/full-game/director-spell-review-129/{QUEUE_AFTER.name}), [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [independent audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{INDEPENDENT_AUDIT.name}), [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), and [Return184 ZIP](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIVED.name}/{RETURN.name}).\n"
    )
    SNAPSHOT.write_text(snapshot_text, encoding="utf-8")
    old_start = START.read_text(encoding="utf-8-sig") if START.exists() else ""
    start_update = (
        "**Current ordinary spell-review checkpoint [184](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_184.json):** GPT's Return184 accepted four exact identities, independently audited and applied: `soul-harvest`, `power-word-kill`, `thread-severance`, and `wail-of-the-banshee`. Authority is **763 reviewed / 85 pending / 0 accepted-unapplied**. Doom, Final Word, and Eternal Pact remain held on DR184-B03/B01/B02; the three Psychic Fear7 identities remain pending under PF182-B01/B02. The next current-authority queue group is Rank9 Defense Form8. See [handoff 184](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_184.json) and [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT85_PENDING_IDENTITY_AUDIT_184.json).\n\n"
    )
    START.write_text(start_update + old_start, encoding="utf-8")
    assert CATALOG.read_bytes() == catalog_bytes
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": IDS, "unacceptedIds": UNACCEPTED, "authority": authority_after, "nextGroup": queue_after["nextGroup"], "nextPendingCount": defense["pendingCount"], "independentAudit": audit["status"], "applicationValidation": validation["status"], "indexSha256": sha(INDEX.read_bytes()), "catalogUnchanged": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    apply()
