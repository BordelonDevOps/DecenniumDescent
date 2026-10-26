from __future__ import annotations

import copy
import gzip
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_defenseform8_return186_received"
RETURN = RECEIVED / "DD_Rank9_DefenseForm8_Director_Return186.zip"
DELIVERY = RECEIVED / "DD_Rank9_DefenseForm8_Director_Return186_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json"
INPUT_PACKET = AUDIT / "rank9_defenseform8_return185_prepared/DD_Rank9_DefenseForm8_CurrentSource_185.zip"
SOURCE_CANDIDATE_MEMBER = "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
BEFORE_BACKUP = AUDIT / "RANK9_DEFENSEFORM8_INDEX_BEFORE_186.json"
OPERATIONS = AUDIT / "RANK9_DEFENSEFORM8_INDEX_OPERATIONS_186.json"
REVIEW_ID = "RANK9-DEFENSEFORM8-APPLICATION-186"
APP_ID = "RANK9-DEFENSEFORM8-APPLICATION-186"
GROUP = ["absolute-immunity", "astral-shell", "divine-shield", "eternal-protection", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]
ACCEPTED = ["astral-shell", "divine-shield", "eternal-protection"]
UNACCEPTED = ["absolute-immunity", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]
BLOCKERS = {
    "absolute-immunity": ["DF186-H-TRACKS"],
    "elemental-shell": ["DF186-H-NULL", "DF186-H-ENV", "DF186-H-COMPANION"],
    "body-to-void": ["DF186-H-OCCUPIED"],
    "timeless-form": ["DF186-H-AGING", "DF186-H-TIMESTOP"],
    "invulnerable-sphere": ["DF186-H-PLANAR", "DF186-H-CONTROL"],
}
PRIOR_HELD = ["psychic-scream", "mass-phantom-killer", "weird", "doom", "final-word", "eternal-pact"]
NEXT_GROUP = "rank9-ward-control6"
NEXT_IDS = ["greater-spell-turning", "nullification-wave", "eternal-ward", "ultimate-ward", "reality-anchor", "prismatic-sphere"]
CANDIDATE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186")
CANDIDATE = ROOT / CANDIDATE_REL
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
PENDING_AFTER = AUDIT / "CURRENT82_PENDING_IDENTITY_AUDIT_186.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_186.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_186.json"
DECISION = AUDIT / "RANK9_DEFENSEFORM8_DIRECTOR_DECISION_186.json"
ACCEPTANCE = AUDIT / "RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_186.json"
RECEIPT = AUDIT / "RANK9_DEFENSEFORM8_RETURN186_RECEIPT.json"
APPLICATION = AUDIT / "RANK9_DEFENSEFORM8_APPLICATION_186.json"
VALIDATION = AUDIT / "RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_186.json"
PENDING_BEFORE = AUDIT / "CURRENT85_PENDING_IDENTITY_AUDIT_184.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_185.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_185.json"
START = ROOT / "START_HERE.md"


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


def bind(path: str | Path, raw: bytes | None = None) -> dict:
    path_text = Path(path).as_posix() if isinstance(path, Path) else path
    if raw is None:
        raw = (ROOT / path_text).read_bytes()
    return {"path": path_text, "bytes": len(raw), "sha256": sha(raw)}


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def main() -> None:
    if CANDIDATE.exists() or STAGING.exists():
        raise FileExistsError("Candidate package already exists; inspect before retrying")
    audit = read_json(INDEPENDENT_AUDIT)
    delivery = read_json(DELIVERY)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0
    assert audit["acceptedIds"] == ACCEPTED and audit["unacceptedIds"] == UNACCEPTED and audit["appliedIds"] == []
    assert delivery["applied"] is False and delivery["canonicalFilesEdited"] is False
    assert sha_file(RETURN) == delivery["archive"]["sha256"] and RETURN.stat().st_size == delivery["archive"]["bytes"]

    before_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    before = json.loads(before_raw.decode("utf-8-sig"))
    catalog = json.loads(catalog_raw.decode("utf-8-sig"))
    assert before["authoredCounts"] == {"reviewed": 763, "pending": 85}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 487
    index_rows = {row["id"]: row for row in before["entries"]}
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert set(ACCEPTED) | set(UNACCEPTED) <= live_pending
    assert all(index_rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in GROUP)
    catalog_rows = {row["id"]: row for row in catalog["spells"]}

    with zipfile.ZipFile(RETURN) as archive:
        decision = json.loads(archive.read("DIRECTOR_DECISION_186.json"))
        procedures_doc = json.loads(archive.read("PROCEDURES.json"))
        procedures = {row["spellId"]: row for row in procedures_doc["spells"]}
        decision_rows = {row["spellId"]: row for row in decision["perIdentityDecisions"]}
        question_doc = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        question_map = {row["id"]: row for row in question_doc["questions"]}
        case_index_doc = json.loads(archive.read("CASE_INDEX.json"))
        case_index = {row["id"]: row for row in case_index_doc["cases"]}
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        obligations = json.loads(archive.read("ORIGINAL_OBLIGATIONS.json"))
        delivery_counts = delivery["counts"]
        assert decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == UNACCEPTED
        assert set(procedures) == set(decision_rows) == set(GROUP)
        assert all(decision_rows[s]["accepted"] is True and decision_rows[s]["applied"] is False for s in ACCEPTED)
        assert all(decision_rows[s]["accepted"] is False and decision_rows[s]["applied"] is False for s in UNACCEPTED)

        STAGING.mkdir(parents=True)
        with (STAGING / "CASEBOOK.json.gz").open("wb") as raw_gzip:
            with gzip.GzipFile(fileobj=raw_gzip, mode="wb", filename="", mtime=0, compresslevel=6) as gz:
                with archive.open("CASEBOOK.json") as source:
                    shutil.copyfileobj(source, gz, length=1024 * 1024)
        casebook_member = next(row for row in delivery["members"] if row["path"] == "CASEBOOK.json")
        casebook_compressed_binding = bind(CANDIDATE_REL / "CASEBOOK.json.gz", (STAGING / "CASEBOOK.json.gz").read_bytes())

        retained_files = [
            "ACTOR_PROFILES.json", "CASE_INDEX.json", "DATA_INTEGRITY_AND_SCOPED_SEMANTIC_CHECK.json",
            "DIRECTOR_DECISION_186.json", "DOCUMENT_AND_COVERAGE_CHECK.json", "FUTURE_OBLIGATION_DISPOSITIONS.json",
            "HISTORICAL_QUESTION_BRIDGE.json", "HOLD_REGISTER.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
            "MAIN_CASE_DISPOSITIONS.json", "ORIGINAL_OBLIGATIONS.json", "PROCEDURES.json", "QUESTION_DISPOSITIONS.json",
            "SOURCE_INTEGRITY_CHECK.json", "SOURCE_LINE_ENDING_RECONCILIATION.json", "SOURCE_SCOPE_RECHECK.json",
            "STANDALONE_PROCEDURES.md", "VALIDATION_SUMMARY.json", "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json",
        ]
        for member in retained_files:
            destination = STAGING / member
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(member))
        for sid in GROUP:
            (STAGING / "procedures").mkdir(exist_ok=True)
            (STAGING / "procedures" / f"{sid}.json").write_bytes(archive.read(f"procedures/{sid}.json"))
        (STAGING / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        proposal_operations = {"id": "DF186-NO-PROPOSAL-OPERATIONS", "status": "NO_PROPOSAL_OPERATIONS", "proposalOperations": 0, "operations": [], "scope": "Only three exact director-accepted authored procedures are recorded; no shared or canonical rules are proposed."}
        write_json(STAGING / "PROPOSAL_OPERATIONS.json", proposal_operations)

        archive_binding = bind(RETURN.relative_to(ROOT).as_posix())
        delivery_binding = bind(DELIVERY.relative_to(ROOT).as_posix())
        audit_binding = bind(INDEPENDENT_AUDIT.relative_to(ROOT).as_posix())
        packet_binding = bind(INPUT_PACKET.relative_to(ROOT).as_posix())
        candidate_raw = archive.read(SOURCE_CANDIDATE_MEMBER)
        candidate_binding = bind((CANDIDATE_REL / "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json"), candidate_raw)
        decision_binding = bind(CANDIDATE_REL / "DIRECTOR_DECISION_186.json", (STAGING / "DIRECTOR_DECISION_186.json").read_bytes())
        hold_binding = bind(CANDIDATE_REL / "HOLD_REGISTER.json", (STAGING / "HOLD_REGISTER.json").read_bytes())
        proposal_binding = bind(CANDIDATE_REL / "PROPOSAL_OPERATIONS.json", (STAGING / "PROPOSAL_OPERATIONS.json").read_bytes())
        casebook_source_binding = {"path": "CASEBOOK.json", "bytes": casebook_member["bytes"], "sha256": casebook_member["sha256"]}

        unaccepted_decisions = [copy.deepcopy(decision_rows[s]) for s in UNACCEPTED]
        model_spells = []
        for position, sid in enumerate(ACCEPTED):
            source = procedures[sid]
            card = source["nativeCardAndAccessUnchanged"]
            qids = source["questionIds"]
            procedure = {
                "id": f"DF186-STATIC-PROCEDURE-186-{sid.upper().replace('-', '_')}",
                "spellId": sid,
                "status": "director-accepted static authored procedure; applied to the authored review index; runtime remains disabled",
                "accepted": True,
                "applied": False,
                "nativeCardAndAccessUnchanged": copy.deepcopy(card),
                "sourceRecordPointer": source["sourceRecordPointer"],
                "procedureText": source["procedureText"],
                "sharedRules": copy.deepcopy(source["sharedRules"]),
                "questionIds": copy.deepcopy(qids),
                "directorDecisionId": "RANK9-DEFENSEFORM8-DIRECTOR-RETURN186",
            }
            model_spells.append({
                "id": sid,
                "name": card["name"],
                "procedure": procedure,
                "directorProcedureRecord": copy.deepcopy(source),
                "nativeCardAndAccessUnchanged": copy.deepcopy(card),
                "questionDispositions": {qid: copy.deepcopy(question_map[qid]) for qid in qids if qid in question_map},
                "runtimeSelectionEnabled": False,
            })

        accepted_case_ids = [cid for sid in ACCEPTED for cid in decision_rows[sid]["caseIds"]]
        excluded_pending = sorted(live_pending - set(ACCEPTED))
        next_manifest_base = {
            "id": "RANK9-DEFENSEFORM8-CANDIDATE-PACKAGE-MANIFEST-186",
            "sourceArchive": archive_binding,
            "sourceDeliveryObservation": delivery_binding,
            "independentAudit": audit_binding,
            "sourceConferenceArchive": packet_binding,
            "sourceConferenceCandidate": candidate_binding,
            "files": [],
        }
        model = {
            "schemaVersion": 1,
            "moduleId": "rank9-defenseform8-reviewed-186",
            "status": "EXACT_THREE_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_FIVE_RETAINED_PENDING_BLOCKERS",
            "scope": "Exactly astral-shell, divine-shield and eternal-protection are individually director-accepted for static authored procedures and applied to the authored review index. The eight-identity batch remains unaccepted; the other five identities stay pending under nine exact positive-evidence blockers. Runtime and all downstream gates remain disabled.",
            "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED,
            "excludedPendingIds": excluded_pending,
            "unacceptedDecisions": unaccepted_decisions,
            "sharedRules": {"scope": "No global or shared rule changes; each full native card and class route is retained.", "runtimeSelectionEnabled": False},
            "spells": model_spells,
            "questionDispositions": question_doc,
            "originalQuestionsAndObligations": obligations,
            "caseCoverage": {"returnedCases": delivery_counts["caseCount"], "acceptedCaseIds": accepted_case_ids, "acceptedCaseCount": len(accepted_case_ids), "acceptedCaseEventsIndependentlyReplayed": audit["caseReplay"]["events"], "allCurrentQuestions": delivery_counts["currentSourceQuestions"], "focusedAdditionalQuestions": delivery_counts["focusedAdditionalQuestions"]},
            "returnCounts": delivery_counts,
            "independentAcceptedCaseReplay": {"status": "PASS", **audit["caseReplay"], "audit": audit_binding},
            "applicationCountSummary": {"before": {"reviewed": 763, "pending": 85, "completeReviewedStandaloneProcedures": 487}, "after": {"reviewed": 766, "pending": 82, "completeReviewedStandaloneProcedures": 490}},
            "holdIds": [row["id"] for row in hold_register["holds"]],
            "holdRegisterFile": "HOLD_REGISTER.json",
            "proposalOperationsFile": "PROPOSAL_OPERATIONS.json",
            "casebookFile": "CASEBOOK.json.gz",
            "casebookEncoding": "gzip with mtime=0; decompression reproduces the exact CASEBOOK.json member of Return186",
            "casebookSourceArchiveMemberBinding": casebook_source_binding,
            "directorReturnArchive": archive_binding,
            "directorDeliveryObservation": delivery_binding,
            "independentReturnAudit": audit_binding,
            "archiveOnlyMembers": [name for name in archive.namelist() if name not in {"CASEBOOK.json", "DIRECTOR_DECISION_186.json", "PROCEDURES.json", "HOLD_REGISTER.json", "STANDALONE_PROCEDURES.md", "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json"}],
            "archiveOnlyRationale": "All 255 members remain bound in the exact Return186 ZIP. The candidate package carries the deterministic casebook, exact accepted procedures, source-context candidate, decision, holds, and coverage artifacts; duplicated source trees remain in the bound return archive.",
            "sourceConferenceArchive": packet_binding,
            "sourceConferenceCandidate": "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json",
            "sourceConferenceCandidateBinding": candidate_binding,
            "standaloneProcedures": "STANDALONE_PROCEDURES.md",
            "directorDecisionFile": "DIRECTOR_DECISION_186.json",
            "directorDecisionId": "RANK9-DEFENSEFORM8-DIRECTOR-RETURN186",
            "sourceAuthorityAtDecision": delivery["baselineAuthority"],
            "runtimeSelectionEnabled": False,
            "runtimeTestsExecuted": False,
            "sourceProgramsExecuted": False,
            "humanPlaytested": False,
            "balanceApproved": False,
            "cosmologyModified": False,
            "releaseApproved": False,
            "domainClosure": False,
        }
        # The package manifest excludes MODEL.json to avoid a recursive self-hash.
        for path in sorted(p for p in STAGING.rglob("*") if p.is_file() and p.name != "MODEL.json"):
            raw = path.read_bytes()
            next_manifest_base["files"].append({"path": (CANDIDATE_REL / path.relative_to(STAGING)).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
        manifest_path = STAGING / "CANDIDATE_PACKAGE_MANIFEST.json"
        write_json(manifest_path, next_manifest_base)
        model["candidatePackageManifestBinding"] = bind(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json", manifest_path.read_bytes())
        write_json(STAGING / "MODEL.json", model)
        shutil.move(str(STAGING), str(CANDIDATE))
        model_binding = bind(CANDIDATE_REL / "MODEL.json")
        package_manifest_binding = bind(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json")
        casebook_binding = bind(CANDIDATE_REL / "CASEBOOK.json.gz")

    timestamp = datetime.now(timezone.utc).isoformat()
    decision_record = {
        "id": "RANK9-DEFENSEFORM8-GPT-DIRECTOR-DECISION-186",
        "recordedAtUtc": timestamp,
        "source": {"product": "ChatGPT", "project": "Dungeon Crawler", "conversation": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decisionId": "RANK9-DEFENSEFORM8-DIRECTOR-RETURN186",
        "batchAccepted": False,
        "accepted": False,
        "appliedAtDecision": False,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "remainingBlockingDefects": [{"spellId": sid, "holdIds": BLOCKERS[sid]} for sid in UNACCEPTED],
        "perIdentityAccepted": {sid: True for sid in ACCEPTED},
        "exactVisibleResponse": "Return186 independently accepts astral-shell, divine-shield, and eternal-protection for static authored procedure review, all unapplied. It holds absolute-immunity (condition-track traces), elemental-shell (positive Null/environment/companion evidence), body-to-void (lawful occupied reversion), timeless-form (aging state and pending Time Stop), and invulnerable-sphere (actual planar/cross-boundary control attempts).",
        "verification": {"independentAudit": audit_binding, "independentAuditChecks": audit["checksPassed"], "independentAuditFailures": audit["checksFailed"], "returnMembers": delivery["archive"]["memberCount"], "caseRecords": delivery["counts"]["caseCount"], "events": delivery["counts"]["eventCount"], "reversibleOperations": delivery["counts"]["eventOperationCount"], "dataIntegrityChecks": delivery["counts"]["dataIntegrityAndScopedSemanticChecks"], "documentCoverageChecks": delivery["counts"]["documentAndCoverageChecks"], "acceptedCaseReplay": audit["caseReplay"]},
        "acceptedArchive": archive_binding,
        "deliveryManifest": delivery_binding,
        "scope": "Three exact individual static authored procedure decisions; no runtime, operational, source-access, play, balance, cosmology, closure, or release approval.",
        "retainedBoundary": "The five unaccepted identities and their nine source-evidence blockers remain pending. The six carried-forward Psychic Fear7 and Death/Recovery7 identities remain unchanged.",
        "directorMadeNoCanonicalChanges": True,
    }
    write_json(DECISION, decision_record)
    acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": timestamp,
        "status": "DIRECTOR_ACCEPTED_THREE_EXACT_STATIC_AUTHORED_PROCEDURES_WITH_FIVE_RETAINED_HOLDS",
        "decision": "EXACT_THREE_IDENTITIES_ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "directorDecision": bind(DECISION.relative_to(ROOT).as_posix()),
        "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "batchAccepted": False,
        "countsBefore": {"reviewed": 763, "pending": 85, "acceptedUnapplied": 0},
        "countsAfter": {"reviewed": 766, "pending": 82, "acceptedUnapplied": 0},
        "completeReviewedStandaloneProceduresBefore": 487,
        "completeReviewedStandaloneProceduresAfter": 490,
        "acceptedProcedures": len(ACCEPTED),
        "returnedCaseRecords": delivery["counts"]["caseCount"],
        "acceptedCaseRecordsIndependentlyReplayed": audit["caseReplay"]["acceptedCases"],
        "acceptedEventsIndependentlyReplayed": audit["caseReplay"]["events"],
        "acceptedForwardOperationsIndependentlyReplayed": audit["caseReplay"]["forwardOperations"],
        "acceptedInverseOperationsIndependentlyReplayed": audit["caseReplay"]["inverseOperations"],
        "remainingBlockingDefects": decision_record["remainingBlockingDefects"],
        "sourceStatusPreserved": "blocked-pending-operational-review for all eight; only authoredStatus advances for the exact three accepted identities.",
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
    receipt = {
        "id": "RANK9-DEFENSEFORM8-GPT-RETURN-186-RECEIPT",
        "recordedAtUtc": timestamp,
        "status": "DIRECTOR_PARTIALLY_ACCEPTED_THREE_EXACT_IDENTITIES; FIVE_REMAIN_BLOCKED; INDEPENDENT_AUDIT_PASSED",
        "source": decision_record["source"],
        "decisionId": decision_record["decisionId"],
        "batchAccepted": False,
        "accepted": False,
        "appliedAtDecision": False,
        "reviewedIds": GROUP,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "blockingDefects": decision_record["remainingBlockingDefects"],
        "exactVisibleResponse": decision_record["exactVisibleResponse"],
        "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "sourceAuthority": delivery["baselineAuthority"],
        "counts": delivery["counts"],
        "qualifications": delivery["qualifications"],
        "perIdentityAccepted": {sid: True for sid in ACCEPTED},
    }
    write_json(RECEIPT, receipt)
    application_receipt = {
        "id": APP_ID,
        "recordedAtUtc": timestamp,
        "status": "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_FIVE_RETAINED_PENDING_BLOCKERS",
        "ownerInstruction": "Apply only the exact director-accepted spell identities, push the batch to GitHub, and continue through the queue until pending reaches zero.",
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "batchAccepted": False,
        "directorAcceptance": bind(ACCEPTANCE.relative_to(ROOT).as_posix()),
        "directorDecision": bind(DECISION.relative_to(ROOT).as_posix()),
        "directorReturnReceipt": bind(RECEIPT.relative_to(ROOT).as_posix()),
        "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "indexBefore": bind(BEFORE_BACKUP.relative_to(ROOT).as_posix(), before_raw),
        "counts": {"before": {"reviewed": 763, "pending": 85}, "after": {"reviewed": 766, "pending": 82}},
        "completeReviewedStandaloneProcedures": {"before": 487, "after": 490},
        "acceptedCasesIndependentlyReplayed": audit["caseReplay"],
        "retainedBlockingHoldIds": BLOCKERS,
        "priorHeldIdentitiesUnchanged": PRIOR_HELD,
        "sourceStatusPreservedAsBlocked": True,
        "catalogChanged": False,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(APPLICATION, application_receipt)
    application_binding = bind(APPLICATION.relative_to(ROOT).as_posix())

    shutil.copyfile(INDEX, BEFORE_BACKUP)
    assert BEFORE_BACKUP.read_bytes() == before_raw
    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(ACCEPTED):
        index_position = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_position]
        updated = copy.deepcopy(old)
        updated.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9defenseform8_reviewed_186/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure/procedureText",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/spells/{position}/procedure/sharedRules",
            "manuscript": "../../../docs/spells/candidates/RANK9_DEFENSEFORM8_REVIEWED_186.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE_REL.as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "gzip with mtime=0; decompression reproduces the exact CASEBOOK.json member of the bound director ZIP",
            "casebookSourceArchiveMemberBinding": casebook_source_binding,
            "sourceArchiveBinding": archive_binding,
            "sourceConferenceArchiveBinding": packet_binding,
            "sourceCandidateBinding": candidate_binding,
            "candidatePackageManifestBinding": package_manifest_binding,
            "retainedHoldsBinding": hold_binding,
            "procedureSourceBinding": decision_binding,
            "proposalOperationsBinding": proposal_binding,
            "acceptedSharedRuleScope": acceptance["decision"],
            "authoredAcceptanceReceipt": bind(ACCEPTANCE.relative_to(ROOT).as_posix()),
            "authoredApplicationReceipt": application_binding,
        })
        assert updated["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review"
        operations.append({"op": "replace-entry", "identity": sid, "index": index_position, "before": copy.deepcopy(old), "after": copy.deepcopy(updated)})
        after["entries"][index_position] = updated

    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9defenseform8_reviewed_186/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "excludedPendingIds": excluded_pending,
        "authority": bind(ACCEPTANCE.relative_to(ROOT).as_posix()),
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "sourceArchive": archive_binding,
        "sourceConferenceArchive": packet_binding,
        "casebookBinding": casebook_binding,
        "retainedHoldsBinding": hold_binding,
        "candidatePackageManifestBinding": package_manifest_binding,
        "scope": acceptance["decision"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": 766, "pending": 82}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 490
    pending_after_set = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(operations) == 3 and pending_after_set == live_pending - set(ACCEPTED) and len(pending_after_set) == 82
    assert sum(row["authoredStatus"] == "reviewed-authored-operational-playtest" for row in after["entries"]) == 766
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_raw = json_bytes(after)
    write_json(OPERATIONS, {
        "id": "RANK9-DEFENSEFORM8-INDEX-OPERATIONS-186",
        "before": bind(BEFORE_BACKUP.relative_to(ROOT).as_posix(), before_raw),
        "after": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": len(after_raw), "sha256": sha(after_raw)},
        "operations": operations,
        "inverse": {"semanticExact": True, "restores": "three identity rows, authored counts, standalone-envelope list, and complete-reviewed-procedure count"},
        "onlyIdentityIds": ACCEPTED,
    })
    temp_index = INDEX.with_suffix(".json.defenseform8-186.tmp")
    temp_index.write_bytes(after_raw)
    temp_index.replace(INDEX)
    assert CATALOG.read_bytes() == catalog_raw

    authority_after = {"reviewedApplied": 766, "pending": 82, "acceptedUnapplied": 0, "completeStandaloneProcedures": 490, "scopedInterfaces": 173}
    queue_before = read_json(QUEUE_BEFORE)
    handoff_before = read_json(HANDOFF_BEFORE)
    current_groups = []
    for old_group in queue_before["currentPendingGroups"]:
        left = [sid for sid in old_group["pendingIds"] if sid in pending_after_set]
        if not left:
            continue
        group_row = copy.deepcopy(old_group)
        group_row["pendingIds"] = left
        group_row["pendingCount"] = len(left)
        if group_row["group"] == "rank9-defense-form8":
            group_row.update({
                "status": "PARTIAL_RETURN186_THREE_ACCEPTED_APPLIED_FIVE_SOURCE_EVIDENCE_BLOCKED",
                "freshPacketRequiredForCurrentAuthority": True,
                "blockingReturn": {"receipt": RECEIPT.relative_to(ROOT).as_posix(), "ids": UNACCEPTED, "blockerHoldIds": BLOCKERS},
            })
        if group_row["group"] == NEXT_GROUP:
            group_row["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            group_row["freshPacketRequiredForCurrentAuthority"] = True
        current_groups.append(group_row)
    next_group_row = next(row for row in current_groups if row["group"] == NEXT_GROUP)
    next_request = {
        "group": NEXT_GROUP,
        "pendingIds": NEXT_IDS,
        "pendingCount": 6,
        "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
        "freshPacketRequiredForCurrentAuthority": True,
        "candidate": next_group_row["candidate"],
        "archive": next_group_row["archive"],
    }
    pending_doc = {
        "id": "CURRENT82-PENDING-IDENTITY-AUDIT-186",
        "recordedAtUtc": timestamp,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": bind(INDEX.relative_to(ROOT).as_posix(), after_raw),
        "catalogBinding": bind(CATALOG.relative_to(ROOT).as_posix(), catalog_raw),
        "authoredCounts": after["authoredCounts"],
        "pendingCount": 82,
        "pendingIds": sorted(pending_after_set),
        "allPendingExistInSourceCatalog": pending_after_set <= set(catalog_rows),
        "closed335AndCompletedCohortsReopened": False,
        "acceptedUnapplied": 0,
        "retainedReturn186Blockers": {sid: BLOCKERS[sid] for sid in UNACCEPTED},
        "priorHeldIdentitiesUnchanged": PRIOR_HELD,
    }
    assert pending_doc["allPendingExistInSourceCatalog"] and set(PRIOR_HELD) <= pending_after_set and set(UNACCEPTED) <= pending_after_set
    write_json(PENDING_AFTER, pending_doc)

    queue_after = copy.deepcopy(queue_before)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-186",
        "recordedAtUtc": timestamp,
        "currentAuthority": authority_after,
        "pendingCount": 82,
        "currentPendingGroups": current_groups,
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": 3, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": PENDING_AFTER.relative_to(ROOT).as_posix(), "pending": 82, "sha256": sha(PENDING_AFTER.read_bytes())},
        "nextGroup": NEXT_GROUP,
        "next": next_request,
        "nextPreparedRequest": next_request,
        "packetStatus": "RANK9_DEFENSEFORM8_RETURN186_THREE_APPLIED_FIVE_HELD_766_82_NEXT_WARD_CONTROL6",
        "currentSubmission": {"path": RECEIPT.relative_to(ROOT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": sha_file(RECEIPT)},
        "currentSubmissionBinding": bind(RECEIPT.relative_to(ROOT).as_posix()),
        "currentReturnBinding": archive_binding,
        "currentPreparation": bind(INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()),
        "currentPacket": archive_binding,
    })
    write_json(QUEUE_AFTER, queue_after)

    handoff_after = copy.deepcopy(handoff_before)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-186",
        "recordedAtUtc": timestamp,
        "status": "RANK9_DEFENSEFORM8_THREE_APPLIED_FIVE_HELD_NEXT_WARD_CONTROL6_82_PENDING",
        "currentAuthority": authority_after,
        "currentIndexBinding": bind(INDEX.relative_to(ROOT).as_posix(), after_raw),
        "currentCatalogBinding": bind(CATALOG.relative_to(ROOT).as_posix(), catalog_raw),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.relative_to(ROOT).as_posix(), "pendingCount": 82, "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": 3, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(), "applicationValidation": {"path": VALIDATION.relative_to(ROOT).as_posix()}},
        "unacceptedThisStep": {"ids": UNACCEPTED, "blockerHoldIds": BLOCKERS, "retainedInPendingSet": True},
        "nextGroup": NEXT_GROUP,
        "nextPendingCount": 6,
        "retainedBoundary": "Astral Shell, Divine Shield, and Eternal Protection are applied as static authored procedures only. Absolute Immunity, Elemental Shell, Body to Void, Timeless Form, and Invulnerable Sphere remain pending under DF186 evidence holds. Preserve all six carried-forward Psychic Fear7 and Death/Recovery7 held identities. Runtime, source/access, human-play, balance, cosmology, domain closure, and release remain unapproved.",
        "resumePriority": "Prepare and send a fresh Rank9 Ward/Control6 packet against current 766/82 authority to the same GPT director. Apply only audited exact acceptances and continue in queue order until pending reaches zero; retain all eleven current and carried-forward evidence holds.",
        "nextPreparedRequest": next_request,
        "currentQueueBinding": bind(QUEUE_AFTER.relative_to(ROOT).as_posix()),
        "currentSubmissionBinding": bind(RECEIPT.relative_to(ROOT).as_posix()),
        "currentReturnBinding": archive_binding,
        "independentAuditBinding": audit_binding,
        "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(),
    })
    write_json(HANDOFF_AFTER, handoff_after)

    validation_checks = [
        {"check": "Return186 exact archive binding and 33-check independent audit passed before application", "passed": audit["status"] == "PASS" and audit["checksFailed"] == 0 and sha_file(RETURN) == archive_binding["sha256"]},
        {"check": "Exactly three per-identity director acceptances are applied", "passed": [op["identity"] for op in operations] == ACCEPTED and all(op["after"]["authoredStatus"] == "reviewed-authored-operational-playtest" for op in operations)},
        {"check": "Five unaccepted identities remain pending under all nine exact blockers", "passed": all(index_rows[s]["authoredStatus"] == "pending-authored-procedure" for s in UNACCEPTED) and set(h for hs in BLOCKERS.values() for h in hs) == set(h for sid in UNACCEPTED for h in BLOCKERS[sid])},
        {"check": "Authority updates exactly from 763/85 to 766/82 and complete procedures 487 to 490", "passed": after["authoredCounts"] == {"reviewed": 766, "pending": 82} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 490},
        {"check": "All 82 pending IDs equal the prior set minus the exact three acceptances", "passed": pending_after_set == live_pending - set(ACCEPTED) and len(pending_after_set) == pending_doc["pendingCount"] == 82},
        {"check": "All six earlier held identities remain pending and unchanged", "passed": set(PRIOR_HELD) <= pending_after_set and all(index_rows[s]["authoredStatus"] == "pending-authored-procedure" for s in PRIOR_HELD)},
        {"check": "Catalog and native class/access/source rows remain unchanged", "passed": CATALOG.read_bytes() == catalog_raw and all(after["entries"][next(i for i,row in enumerate(after["entries"]) if row["id"] == sid)]["sourceStatus"] == "blocked-pending-operational-review" for sid in GROUP)},
        {"check": "Three-row inverse operation restores exact pre-application index", "passed": inverse == before and sha(BEFORE_BACKUP.read_bytes()) == sha(before_raw)},
        {"check": "Next group is exactly the six-identity Ward/Control6 queue group", "passed": queue_after["nextGroup"] == NEXT_GROUP and next_group_row["pendingIds"] == NEXT_IDS and next_group_row["pendingCount"] == 6},
        {"check": "Candidate package files match the package manifest and deterministic casebook gzip", "passed": all((ROOT / row["path"]).is_file() and (ROOT / row["path"]).stat().st_size == row["bytes"] and sha_file(ROOT / row["path"]) == row["sha256"] for row in next_manifest_base["files"]) and CANDIDATE.joinpath("MODEL.json").is_file() and casebook_binding["bytes"] > 0},
        {"check": "Accepted status remains authored-static-only with no downstream approval", "passed": model["runtimeSelectionEnabled"] is False and all(model[k] is False for k in ("runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))},
    ]
    validation = {
        "id": "RANK9-DEFENSEFORM8-APPLICATION-VALIDATION-186",
        "recordedAtUtc": timestamp,
        "status": "PASS" if all(row["passed"] for row in validation_checks) else "FAIL",
        "checksPassed": sum(row["passed"] for row in validation_checks),
        "checksFailed": sum(not row["passed"] for row in validation_checks),
        "checks": validation_checks,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "countsBefore": {"reviewed": 763, "pending": 85, "completeReviewedStandaloneProcedures": 487},
        "countsAfter": {"reviewed": 766, "pending": 82, "completeReviewedStandaloneProcedures": 490},
        "indexBefore": bind(BEFORE_BACKUP.relative_to(ROOT).as_posix(), before_raw),
        "indexAfter": bind(INDEX.relative_to(ROOT).as_posix(), INDEX.read_bytes()),
        "catalog": bind(CATALOG.relative_to(ROOT).as_posix(), CATALOG.read_bytes()),
        "application": bind(APPLICATION.relative_to(ROOT).as_posix()),
        "independentAudit": audit_binding,
        "pendingIdentityAudit": bind(PENDING_AFTER.relative_to(ROOT).as_posix()),
        "queueAfter": bind(QUEUE_AFTER.relative_to(ROOT).as_posix()),
        "handoffAfter": bind(HANDOFF_AFTER.relative_to(ROOT).as_posix()),
        "nextGroup": NEXT_GROUP,
        "nextPendingCount": 6,
        "runtimeSelectionEnabled": False,
        "closedCohortsReopened": False,
    }
    write_json(VALIDATION, validation)
    assert validation["status"] == "PASS", validation_checks

    snapshot_text = (
        "# Current ordinary spell-review checkpoint 186\n\n"
        "Authority is **766 reviewed / 82 pending / 0 accepted-unapplied**, with 490 complete reviewed standalone procedures. Return186 passed a 33-check independent audit, including 255 exact archive bindings, all 87 refreshed current-source bindings, and forward/inverse replay of 38 accepted cases (814 events). Exactly `astral-shell`, `divine-shield`, and `eternal-protection` were applied as static authored procedures. Five Defense/Form8 identities remain held under nine DF186 evidence blockers; the six Psychic Fear7 and Death/Recovery7 holds remain pending.\n\n"
        f"See [handoff 186](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [queue 186](docs/audit/2026-10-08/full-game/director-spell-review-129/{QUEUE_AFTER.name}), [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [independent audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{INDEPENDENT_AUDIT.name}), [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}), and [Return186 ZIP](docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIVED.name}/{RETURN.name}).\n"
    )
    (AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_186.md").write_text(snapshot_text, encoding="utf-8")
    old_start = START.read_text(encoding="utf-8-sig") if START.exists() else ""
    start_update = (
        "**Current ordinary spell-review checkpoint [186](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_186.json):** Return186 was independently audited and applied for exactly `astral-shell`, `divine-shield`, and `eternal-protection`. Authority is **766 reviewed / 82 pending / 0 accepted-unapplied**. Five Defense/Form8 identities remain held on nine exact source-evidence gaps. The next queue group is Rank9 Ward/Control6; the six carried-forward Psychic Fear7 and Death/Recovery7 holds remain pending. See [handoff 186](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_186.json) and [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT82_PENDING_IDENTITY_AUDIT_186.json).\n\n"
    )
    START.write_text(start_update + old_start, encoding="utf-8")
    assert CATALOG.read_bytes() == catalog_raw
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "authority": authority_after, "nextGroup": NEXT_GROUP, "nextPendingCount": 6, "independentAudit": audit["status"], "applicationValidation": validation["status"], "indexSha256": sha_file(INDEX), "catalogUnchanged": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
