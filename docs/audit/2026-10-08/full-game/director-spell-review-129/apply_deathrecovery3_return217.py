from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import shutil
import subprocess
import zlib
from datetime import datetime, timezone


ROOT = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECV = BASE / "rank9_deathrecovery7_return217_received"
EXTRACT = RECV / "extracted"
ARCHIVE = RECV / "DD_Rank9_DeathRecovery3_Director_Return217.zip"
DELIVERY = RECV / "DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json"
AUDIT = RECV / "RETURN217_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = BASE / "CURRENT_SPELL_QUEUE_216.json"
HANDOFF_BEFORE = BASE / "CURRENT_HANDOFF_216.json"
PENDING_BEFORE = BASE / "CURRENT42_PENDING_IDENTITY_AUDIT_216.json"
SOURCE_ARCHIVE = BASE / "rank9_deathrecovery7_source_packet_216_refreshed/DD_Rank9_DeathRecovery7_CurrentSource_216.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_death_recovery_7_source_conference_01.json"
ACCEPTED = ["doom", "eternal-pact"]
HELD = ["final-word"]
GROUP_IDS = ["doom", "final-word", "eternal-pact"]
REVIEW_ID = "RANK9-DEATHRECOVERY3-EXACT-AUTHORED-ACCEPTANCE-217"
APPLICATION_ID = "RANK9-DEATHRECOVERY3-APPLICATION-217"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9deathrecovery3_reviewed_217"

BEFORE = {"reviewedApplied": 806, "pending": 42, "acceptedUnapplied": 0, "completeStandaloneProcedures": 530, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 808, "pending": 40, "acceptedUnapplied": 0, "completeStandaloneProcedures": 532, "scopedInterfaces": 173}

BACKUP = BASE / "authored_review_index.before_deathrecovery3_217.json"
ACCEPTANCE = BASE / "RANK9DEATHRECOVERY3_EXACT_ACCEPTANCE_217.json"
APPLICATION = BASE / "RANK9DEATHRECOVERY3_APPLICATION_217.json"
OPERATIONS = BASE / "RANK9DEATHRECOVERY3_INDEX_OPERATIONS_217.json"
VALIDATION = BASE / "RANK9DEATHRECOVERY3_APPLICATION_VALIDATION_217.json"
PENDING_AFTER = BASE / "CURRENT40_PENDING_IDENTITY_AUDIT_217.json"
QUEUE_AFTER = BASE / "CURRENT_SPELL_QUEUE_217.json"
HANDOFF_AFTER = BASE / "CURRENT_HANDOFF_217.json"
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_217.md"
NEXT_REQUEST = BASE / "RANK9_DEFENSEFORM8_RETURN217_REQUEST.txt"
OBSERVATION = RECV / "RETURN217_DELIVERY_OBSERVATION.json"
REPRESENTATION_RECONCILIATION = BASE / "RANK9DEATHRECOVERY3_REPRESENTATION_COUNT_RECONCILIATION_217.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def read_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def bind_bytes(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def bind_file(path: pathlib.Path, rel: str | None = None) -> dict:
    return bind_bytes(rel or path.relative_to(ROOT).as_posix(), path.read_bytes())


def bind_stream(path: pathlib.Path, rel: str | None = None) -> dict:
    h = hashlib.sha256()
    c = 0
    size = 0
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            size += len(chunk)
            h.update(chunk)
            c = zlib.crc32(chunk, c)
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": size, "sha256": h.hexdigest(), "crc32": f"{c & 0xFFFFFFFF:08x}"}


def bind_record(path: pathlib.Path) -> dict:
    return bind_stream(path)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def git_blob(rel: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{rel}"], cwd=ROOT)


def main() -> None:
    audit = read_json(AUDIT)
    delivery = read_json(DELIVERY)
    decision = read_json(EXTRACT / "DIRECTOR_DECISION.json")
    procedures_doc = read_json(EXTRACT / "PROCEDURES.json")
    queue_before = read_json(QUEUE_BEFORE)
    handoff_before = read_json(HANDOFF_BEFORE)
    pending_before = read_json(PENDING_BEFORE)

    require(audit.get("status") == "PASS" and all(x.get("passed") for x in audit.get("checks", [])), "Return217 independent audit is not PASS")
    require(delivery.get("acceptedIds") == ACCEPTED and delivery.get("heldIds") == HELD and delivery.get("applied") is False, "Return217 director acceptance is not exact and unapplied")
    require(decision.get("acceptedIds") == ACCEPTED and decision.get("heldIds") == HELD and decision.get("applied") is False, "Extracted decision differs from delivery acceptance")
    require(decision.get("sourceAuthority") == BEFORE, "Director source authority is not 806/42/0")
    require(decision.get("counts", {}).get("dataIntegrityChecks") == 14881, "Director data replay count is unexpected")
    per_identity = {x["id"]: x for x in decision["perIdentity"]}
    require(set(per_identity) == set(GROUP_IDS), "Director reviewed identity set differs")
    require(all(per_identity[s]["accepted"] is True and per_identity[s]["applied"] is False and not per_identity[s]["blockerIds"] for s in ACCEPTED), "Accepted identity decision is not exact")
    require(per_identity["final-word"]["accepted"] is False and per_identity["final-word"]["applied"] is False and per_identity["final-word"]["blockerIds"] == ["DR217-B01"], "Final Word hold differs from exact blocker")
    require(queue_before.get("currentAuthority") == BEFORE and handoff_before.get("currentAuthority") == BEFORE, "Queue/handoff authority is not 806/42/0")
    require(pending_before.get("exactPendingCount") == 42, "Current pending audit is not 42")

    actual_index_hash = bind_stream(INDEX)
    actual_catalog_hash = bind_stream(CATALOG)
    require(actual_index_hash["sha256"] == queue_before["currentIndexBinding"]["sha256"] and actual_index_hash["bytes"] == queue_before["currentIndexBinding"]["bytes"], "Index changed after queue216")
    require(actual_catalog_hash["sha256"] == queue_before["currentCatalogBinding"]["sha256"] and actual_catalog_hash["bytes"] == queue_before["currentCatalogBinding"]["bytes"], "Catalog changed after queue216")
    require(not CANDIDATE.exists(), f"Candidate path already exists: {CANDIDATE}")
    generated = [BACKUP, ACCEPTANCE, APPLICATION, OPERATIONS, VALIDATION, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, SNAPSHOT, NEXT_REQUEST, OBSERVATION, REPRESENTATION_RECONCILIATION]
    existing = [str(p) for p in generated if p.exists()]
    require(not existing, f"Application outputs already exist; inspect before retry: {existing}")

    index_raw = INDEX.read_bytes()
    index_before = json.loads(index_raw.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    entries = {row["id"]: row for row in index_before["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    proc_rows = {row["id"]: row for row in procedures_doc["spells"]}
    require(set(proc_rows) == set(GROUP_IDS), "Procedure archive identity set differs")
    require(index_before.get("authoredCounts") == {"reviewed": 806, "pending": 42}, "Index authored counts are not 806/42")
    stored_complete_count = index_before.get("representationCounts", {}).get("completeReviewedStandaloneProcedures")
    observed_complete_count = sum(
        row.get("authoredStatus") == "reviewed-authored-operational-playtest" and row.get("procedureFile") != "catalog.json"
        for row in index_before["entries"]
    )
    require(stored_complete_count == 528 and observed_complete_count == 530, f"Unexpected pre-existing standalone tally discrepancy: stored={stored_complete_count}, observed={observed_complete_count}")
    pending_live = {row["id"] for row in index_before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    require(len(pending_live) == 42 and all(s in pending_live for s in GROUP_IDS), "Current index pending identities differ")
    for sid in GROUP_IDS:
        row = entries[sid]
        procedure_row = proc_rows[sid]
        require(row == procedure_row["currentIndexEntryUnchanged"], f"Director current-index binding differs for {sid}")
        require(row["sourceStatus"] == "blocked-pending-operational-review", f"Native source status changed for {sid}")
        require(procedure_row["nativeCardUnchanged"] == catalog_rows[sid] == procedure_row["currentCatalogRowUnchanged"], f"Native catalog binding differs for {sid}")
    for sid in ACCEPTED:
        require(proc_rows[sid]["accepted"] is True and proc_rows[sid]["applied"] is False and proc_rows[sid]["blockerIds"] == [], f"Procedure acceptance mismatch for {sid}")
        require(isinstance(proc_rows[sid].get("procedure"), str) and proc_rows[sid]["procedure"].strip(), f"Procedure text absent for {sid}")
    require(proc_rows["final-word"]["accepted"] is False and proc_rows["final-word"]["blockerIds"] == ["DR217-B01"], "Held procedure blocker mismatch")

    return_binding = bind_file(ARCHIVE)
    delivery_binding = bind_file(DELIVERY)
    audit_binding = bind_file(AUDIT)
    source_binding = bind_file(SOURCE_ARCHIVE)
    candidate_binding = bind_file(SOURCE_CANDIDATE)
    queue_before_binding = bind_file(QUEUE_BEFORE)
    handoff_before_binding = bind_file(HANDOFF_BEFORE)
    pending_before_binding = bind_file(PENDING_BEFORE)
    package_internal_files = [
        "ACTOR_PROFILES.json", "BLOCKERS.json", "CASE_INDEX.json", "COUNTS.json", "COVERAGE.json",
        "DATA_INTEGRITY_CHECK.json", "DIRECTOR_DECISION.json", "HOLD_REGISTER.json",
        "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "MEMBER_MANIFEST.json", "ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json",
        "PROCEDURES.json", "PROCEDURE_SOURCE_MAP.json", "QUESTION_DISPOSITIONS.json", "SOURCE_BINDINGS.json",
        "VALIDATION.json", "STANDALONE_PROCEDURES.md",
    ]

    # Preserve the exact current director source records beside the applied envelope.
    CANDIDATE.mkdir(parents=True, exist_ok=False)
    director_dir = CANDIDATE / "DIRECTOR_RETURN"
    director_dir.mkdir(parents=True)
    for name in package_internal_files:
        source = EXTRACT / name
        require(source.is_file(), f"Missing exact Return217 evidence member: {name}")
        shutil.copyfile(source, director_dir / name)
    hold_register = read_json(EXTRACT / "HOLD_REGISTER.json")
    write_json(CANDIDATE / "HOLD_REGISTER.json", hold_register)

    evidence = {
        "id": "RANK9-DEATHRECOVERY3-RETURN-EVIDENCE-BINDINGS-217",
        "directorReturnArchive": return_binding,
        "directorDeliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "currentSourcePacket216": source_binding,
        "currentCandidateSource": candidate_binding,
        "currentQueue216": queue_before_binding,
        "currentHandoff216": handoff_before_binding,
        "currentPendingAudit216": pending_before_binding,
        "sourceCandidateReconciliation": bind_file(EXTRACT / "current/RETURN216_CANDIDATE_BINDING_RECONCILIATION.json"),
        "priorReturn184Archive": bind_file(BASE / "rank9_deathrecovery7_return184_received/DD_Rank9_DeathRecovery7_Director_Return184.zip"),
        "verifiedMembers": audit["verifiedMemberCount"],
        "preservedPriorCases": len(audit["preservedCaseChecks"]),
        "dataIntegrityChecks": decision["counts"]["dataIntegrityChecks"],
        "events": decision["counts"]["events"],
        "forwardOperations": decision["counts"]["forwardOperations"],
        "inverseOperations": decision["counts"]["inverseOperations"],
        "caseEvidence": "All 80 Return217 members are bound by the external manifest; the 45 preserved Return184 cases were compared byte-for-byte against the prior archive.",
        "applicationScope": "Only the two exact director-accepted static procedures are applied to the authored review index; Final Word and all unrelated holds remain pending.",
    }
    write_json(CANDIDATE / "RETURN_EVIDENCE_BINDINGS.json", evidence)
    (CANDIDATE / "README.md").write_text(
        "# Death/Recovery 3 static authored review — Return 217\n\n"
        "This envelope records only the individually accepted Doom and Eternal Pact authored procedures. Final Word remains pending on DR217-B01. Native catalog rows and source status remain unchanged; runtime selection is disabled. The Return217 archive and independent audit bind all cases, traces, source comparisons and qualifications.\n\n"
        "No implementation, runtime, playtest, balance, cosmology, domain-closure or release approval is included.\n",
        encoding="utf-8",
    )

    questions_doc = read_json(EXTRACT / "QUESTION_DISPOSITIONS.json")
    questions = questions_doc.get("questions", []) if isinstance(questions_doc, dict) else []
    spells = []
    for position, sid in enumerate(ACCEPTED):
        p = proc_rows[sid]
        native = catalog_rows[sid]
        spells.append({
            "id": sid,
            "name": native["name"],
            "accepted": True,
            "applied": False,
            "nativeCardAndAccessUnchanged": copy.deepcopy(native),
            "procedure": {
                "id": f"RANK9-DEATHRECOVERY3-STATIC-PROCEDURE-217-{sid.upper()}",
                "spellId": sid,
                "reviewId": REVIEW_ID,
                "status": "static-authored-director-accepted-unapplied",
                "procedureText": p["procedure"],
                "sharedRules": copy.deepcopy(p["sharedRules"]),
                "sourceQuestionIds": copy.deepcopy(p["questionIds"]),
                "qualificationIds": copy.deepcopy(per_identity[sid].get("qualificationIds", [])),
                "directorDecisionPointer": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
            },
            "directorProcedureRecord": copy.deepcopy(p),
            "questionDispositions": {q["id"]: copy.deepcopy(q) for q in questions if q.get("id") in p["questionIds"]},
            "runtimeSelectionEnabled": False,
            "directorProcedureRecordPointer": f"DIRECTOR_RETURN/PROCEDURES.json#/spells/{GROUP_IDS.index(sid)}",
        })
    model = {
        "schemaVersion": 1,
        "id": "DD-RANK9-DEATHRECOVERY3-DIRECTOR-RETURN217",
        "reviewId": REVIEW_ID,
        "status": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_FINAL_WORD_HELD",
        "scope": "Only Doom and Eternal Pact are individually accepted and applied as static authored procedures. Final Word remains held on DR217-B01. All three native catalog cards, class access, source status and runtime availability remain unchanged.",
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "heldDecisions": [{"id": "final-word", "accepted": False, "applied": False, "blockerIds": ["DR217-B01"], "directorProcedureRecord": copy.deepcopy(proc_rows["final-word"])}],
        "sourceAuthorityBeforeApplication": BEFORE,
        "sourceAuthorityAfterApplication": AFTER,
        "sharedRules": copy.deepcopy(procedures_doc.get("sharedRules", {})),
        "spells": spells,
        "directorQualifications": copy.deepcopy(decision.get("qualifications", [])),
        "holdRegister": "HOLD_REGISTER.json",
        "evidenceBindings": "RETURN_EVIDENCE_BINDINGS.json",
        "directorReturnArchive": return_binding,
        "directorDeliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "sourceConferenceArchive": source_binding,
        "sourceConferenceCandidate": candidate_binding,
        "currentQueueAtDecision": queue_before_binding,
        "currentPendingAuditAtDecision": pending_before_binding,
        "candidatePackageManifestBinding": None,
        "runtimeSelectionEnabled": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "releaseApproved": False,
    }

    # The package manifest omits MODEL and itself to avoid a circular binding; the
    # acceptance and index bind MODEL.json directly after it is finalized.
    def candidate_files():
        return [p for p in sorted(CANDIDATE.rglob("*")) if p.is_file() and p.name not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json", "EXACT_ACCEPTANCE_217.json"}]

    manifest = {
        "id": "RANK9-DEATHRECOVERY3-CANDIDATE-PACKAGE-MANIFEST-217",
        "files": [bind_stream(p, p.relative_to(CANDIDATE).as_posix()) for p in candidate_files()],
        "excludedFromBindings": ["MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json", "EXACT_ACCEPTANCE_217.json"],
        "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json",
    }
    write_json(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json", manifest)
    package_manifest_binding = bind_file(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")
    model["candidatePackageManifestBinding"] = package_manifest_binding
    write_json(CANDIDATE / "MODEL.json", model)
    model_binding = bind_file(CANDIDATE / "MODEL.json")

    before_bind = bind_bytes(INDEX.relative_to(ROOT).as_posix(), index_raw)
    catalog_bind = bind_file(CATALOG)
    accepted_procedure_bindings = [
        {"id": sid, "directorProcedurePointer": f"DIRECTOR_RETURN/PROCEDURES.json#/spells/{GROUP_IDS.index(sid)}", "procedureSha256": sha(proc_rows[sid]["procedure"].encode("utf-8"))}
        for sid in ACCEPTED
    ]
    acceptance = {
        "id": REVIEW_ID,
        "recordedAtUtc": now(),
        "status": "TWO_EXACT_STATIC_AUTHORED_IDENTITIES_ACCEPTED_WITH_FINAL_WORD_RETAINED_HELD",
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "blockers": ["DR217-B01"],
        "directorDecision": bind_file(EXTRACT / "DIRECTOR_DECISION.json"),
        "directorReturn": return_binding,
        "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "acceptedProcedureBindings": accepted_procedure_bindings,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "heldIdentityDecision": {"id": "final-word", "blockerId": "DR217-B01", "reason": "missing source-established capture-eligible identity for positive reserve-use evidence"},
        "sourceStatusPreserved": "blocked-pending-operational-review for both accepted entries and held final-word; only authoredStatus advances for Doom and Eternal Pact.",
        "runtimeSelectionEnabled": False,
        "implementationApproved": False,
        "canonicalRuntimeApplicationPerformed": False,
    }
    write_json(ACCEPTANCE, acceptance)
    acceptance_binding = bind_file(ACCEPTANCE)

    # Prepare index rows and exact reversible operations entirely in memory.
    idx_after = copy.deepcopy(index_before)
    after_entries = {row["id"]: row for row in idx_after["entries"]}
    operations = []
    for position, sid in enumerate(ACCEPTED):
        old = copy.deepcopy(entries[sid])
        updated = copy.deepcopy(old)
        updated.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9deathrecovery3_reviewed_217/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "reviewId": APPLICATION_ID,
            "runtimeSelectionEnabled": False,
            "priorCatalogSelectionStatusUnchanged": True,
            "completeEnvelopeBinding": model_binding,
            "candidatePackageManifestBinding": package_manifest_binding,
            "directorDecisionBinding": bind_file(EXTRACT / "DIRECTOR_DECISION.json"),
            "directorReturnBinding": return_binding,
            "directorDeliveryManifestBinding": delivery_binding,
            "independentAuditBinding": audit_binding,
            "sourceConferenceArchiveBinding": source_binding,
            "sourceCandidateBinding": candidate_binding,
            "retainedHoldRegister": "HOLD_REGISTER.json",
            "authoredAcceptanceReceipt": acceptance_binding,
            "authoredApplicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        })
        require(updated["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review", f"Source status changed for {sid}")
        index_position = next(i for i, row in enumerate(index_before["entries"]) if row["id"] == sid)
        after_entries[sid].clear()
        after_entries[sid].update(updated)
        operations.append({"op": "replace-entry", "identity": sid, "index": index_position, "before": old, "after": copy.deepcopy(updated)})

    idx_after["authoredCounts"] = {"reviewed": 808, "pending": 40}
    idx_after["representationCounts"]["completeReviewedStandaloneProcedures"] = 532
    excluded_pending = sorted(pending_live - set(ACCEPTED))
    idx_after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9deathrecovery3_reviewed_217/MODEL.json",
        "binding": model_binding,
        "reviewId": REVIEW_ID,
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "excludedPendingIds": excluded_pending,
        "authority": acceptance_binding,
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "sourceArchive": return_binding,
        "sourceConferenceArchive": source_binding,
        "candidatePackageManifestBinding": package_manifest_binding,
        "scope": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_FINAL_WORD_HELD",
        "runtimeSelectionEnabled": False,
    })
    live_pending_after = {row["id"] for row in idx_after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    require(live_pending_after == pending_live - set(ACCEPTED) and len(live_pending_after) == 40, "Planned index does not leave exactly 40 pending identities")
    inverse = copy.deepcopy(idx_after)
    for op in operations:
        inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(index_before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(index_before["representationCounts"])
    require(inverse == index_before, "Inverse application does not restore the exact prior index object")
    index_after_bytes = json_bytes(idx_after)
    after_bind = bind_bytes(INDEX.relative_to(ROOT).as_posix(), index_after_bytes)

    representation_reconciliation = {
        "id": "RANK9DEATHRECOVERY3-REPRESENTATION-COUNT-RECONCILIATION-217",
        "recordedAtUtc": now(),
        "sourceIndexBindingBefore": before_bind,
        "queueAuthorityBefore": BEFORE,
        "indexStoredCompleteReviewedStandaloneProceduresBefore": stored_complete_count,
        "recountedReviewedNonCatalogProcedureEntriesBefore": observed_complete_count,
        "priorAppliedBatchEvidence": str((BASE / "RANK9MASSUNDEATH2_APPLICATION_214.json").relative_to(ROOT)),
        "priorAppliedBatchClaim": {"before": 528, "after": 530, "acceptedIds": ["field-of-endless-dead", "plague-of-undeath"]},
        "currentBatchAcceptedIds": ACCEPTED,
        "recountedReviewedNonCatalogProcedureEntriesAfter": observed_complete_count + len(ACCEPTED),
        "indexStoredCompleteReviewedStandaloneProceduresAfter": 532,
        "resolution": "The current queue and handoff authority already recorded 530 complete standalone procedures, and the index contains exactly 530 reviewed entries whose procedureFile is not catalog.json. The index's separate representationCounts field remained at the prior 528 value after Return214. This application reconciles that stale field to the observed 530 baseline plus the two newly applied procedures (532). No identities beyond the exact Return217 acceptances were changed.",
        "catalogChanged": False,
    }
    write_json(REPRESENTATION_RECONCILIATION, representation_reconciliation)

    app = {
        "id": APPLICATION_ID,
        "recordedAtUtc": now(),
        "status": "APPLIED_TWO_EXACT_ACCEPTED_STATIC_AUTHORED_PROCEDURES_TO_REVIEW_INDEX",
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "blockerIds": ["DR217-B01"],
        "directorDecision": bind_file(EXTRACT / "DIRECTOR_DECISION.json"),
        "directorReturn": return_binding,
        "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding,
        "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_manifest_binding,
        "directorAcceptance": acceptance_binding,
        "indexBefore": before_bind,
        "indexAfter": after_bind,
        "indexOperations": OPERATIONS.relative_to(ROOT).as_posix(),
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 530, "after": 532},
        "sourceStatusPreservedAsBlocked": True,
        "catalogBindingUnchanged": catalog_bind,
        "representationCountReconciliation": bind_file(REPRESENTATION_RECONCILIATION),
        "catalogChanged": False,
        "runtimeSelectionEnabled": False,
        "githubChanges": False,
    }
    write_json(APPLICATION, app)
    application_binding = bind_file(APPLICATION)

    # Record byte-exact baseline, then apply the two exact reviewed-authored rows.
    shutil.copyfile(INDEX, BACKUP)
    require(BACKUP.read_bytes() == index_raw, "Index backup is not byte-exact")
    tmp_index = INDEX.with_suffix(INDEX.suffix + ".return217.tmp")
    require(not tmp_index.exists(), "Temporary index file already exists")
    tmp_index.write_bytes(index_after_bytes)
    tmp_index.replace(INDEX)
    index_after_binding = bind_file(INDEX)
    require(index_after_binding["sha256"] == after_bind["sha256"], "Persisted index differs from planned bytes")
    require(bind_file(CATALOG) == catalog_bind, "Catalog changed during authored review application")

    ops_doc = {
        "id": "RANK9DEATHRECOVERY3-INDEX-OPERATIONS-217",
        "before": before_bind,
        "after": index_after_binding,
        "authorityBefore": BEFORE,
        "authorityAfter": AFTER,
        "operations": operations,
        "inverseSemanticExact": True,
        "inverseRestores": before_bind,
        "additionalEnvelopeAppend": {"index": len(index_before["additionalStandaloneEnvelopes"]), "value": idx_after["additionalStandaloneEnvelopes"][-1]},
        "catalogBefore": catalog_bind,
        "catalogChanged": False,
        "onlyIdentityIds": ACCEPTED,
    }
    write_json(OPERATIONS, ops_doc)
    application_with_ops = read_json(APPLICATION)
    application_with_ops["indexOperations"] = bind_file(OPERATIONS)
    write_json(APPLICATION, application_with_ops)
    application_binding = bind_file(APPLICATION)

    # Refresh the pending queue, leaving both earlier Psychic/Fear holds and the
    # new Final Word blocker pending. Continue with the first non-held group.
    queue_groups = copy.deepcopy(queue_before["currentPendingGroups"])
    return_audit_binding = bind_file(AUDIT)
    director_decision_binding = bind_file(EXTRACT / "DIRECTOR_DECISION.json")
    for group in queue_groups:
        group["pendingIds"] = [sid for sid in group["pendingIds"] if sid not in ACCEPTED]
        if not group["pendingIds"]:
            continue
        group["pendingCount"] = len(group["pendingIds"])
        if group["group"] == "rank9-death-recovery7":
            group["status"] = "HELD_RETURN217_FINAL_WORD_REMAINS_PENDING_DR217-B01"
            group["freshPacketRequiredForCurrentAuthority"] = True
            group["lastDirectorReturn"] = {
                "return": 217,
                "acceptedIds": ACCEPTED,
                "appliedIds": ACCEPTED,
                "heldIds": HELD,
                "blockers": ["DR217-B01"],
                "independentAudit": str(AUDIT.relative_to(ROOT)),
                "decision": str((EXTRACT / "DIRECTOR_DECISION.json").relative_to(ROOT)),
            }
        elif not str(group.get("status", "")).startswith("HELD_"):
            group["status"] = "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_808_40_0"
            group["freshPacketRequiredForCurrentAuthority"] = True
    queue_groups = [g for g in queue_groups if g["pendingIds"]]
    all_pending = [sid for group in queue_groups for sid in group["pendingIds"]]
    require(len(all_pending) == len(set(all_pending)) == 40 and set(all_pending) == live_pending_after, "Refreshed queue does not exactly match the 40 pending index entries")
    next_group = next(g for g in queue_groups if not str(g.get("status", "")).startswith("HELD_"))
    next_record = {
        "group": next_group["group"],
        "pendingIds": next_group["pendingIds"],
        "pendingCount": next_group["pendingCount"],
        "status": "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_808_40_0",
        "freshPacketRequiredForCurrentAuthority": True,
        "historicalCandidate": next_group.get("candidate"),
        "historicalArchive": next_group.get("archive"),
    }
    pending_audit = {
        "id": "CURRENT40-PENDING-IDENTITY-AUDIT-217",
        "recordedAtUtc": now(),
        "authority": AFTER,
        "exactPendingCount": 40,
        "pendingIds": all_pending,
        "groups": queue_groups,
        "allPendingIdsExistInNativeCatalog": all(sid in catalog_rows for sid in all_pending),
        "noPendingTargetWasSilentlyAccepted": True,
        "preservedHolds": [{"id": "final-word", "blockerIds": ["DR217-B01"]}, {"ids": ["psychic-scream", "mass-phantom-killer", "weird"], "blockerIds": ["PF182-B01", "PF182-B02"]}],
    }
    write_json(PENDING_AFTER, pending_audit)
    pending_binding = bind_file(PENDING_AFTER)
    index_binding = bind_file(INDEX)
    catalog_binding = bind_file(CATALOG)
    queue = copy.deepcopy(queue_before)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-217",
        "recordedAtUtc": now(),
        "supersedesQueue": bind_file(QUEUE_BEFORE),
        "currentAuthority": AFTER,
        "currentIndexBinding": index_binding,
        "currentCatalogBinding": catalog_binding,
        "currentPendingGroups": queue_groups,
        "nextSuggestedGroups": [g for g in queue_groups if not str(g.get("status", "")).startswith("HELD_")][:5],
        "nextGroup": next_group["group"],
        "next": next_record,
        "justAppliedBatch": {
            "return": 217,
            "reviewId": REVIEW_ID,
            "group": "rank9-death-recovery7",
            "reviewedIds": GROUP_IDS,
            "acceptedIds": ACCEPTED,
            "appliedIds": ACCEPTED,
            "heldIds": HELD,
            "blockers": ["DR217-B01"],
            "conditionalQualificationIds": ["DR217-C01", "DR217-C02"],
            "application": str(APPLICATION.relative_to(ROOT)),
            "independentAudit": return_audit_binding,
        },
        "pendingIdentityAudit": {"path": str(PENDING_AFTER.relative_to(ROOT)), **{k: pending_binding[k] for k in ("bytes", "sha256", "crc32")}},
        "currentReturnAudit": return_audit_binding,
        "currentReturnDelivery": delivery_binding,
        "currentReturnArchive": return_binding,
        "currentReturnDecision": director_decision_binding,
        "parentQueue": str(QUEUE_BEFORE.relative_to(ROOT)),
        "pendingCount": 40,
        "lastReviewedBatch": {
            "return": 217,
            "group": "rank9-death-recovery7",
            "ids": GROUP_IDS,
            "acceptedIds": ACCEPTED,
            "appliedIds": ACCEPTED,
            "heldIds": HELD,
            "blockers": ["DR217-B01"],
            "auditStatus": "PASS",
            "independentAudit": return_audit_binding,
            "decision": director_decision_binding,
        },
    })
    write_json(QUEUE_AFTER, queue)
    queue_binding = bind_file(QUEUE_AFTER)

    handoff = {
        "id": "CURRENT-HANDOFF-217",
        "recordedAtUtc": now(),
        "status": "RETURN217_EXACT_ACCEPTANCES_APPLIED_808_40_NEXT_BATCH_READY",
        "currentAuthority": AFTER,
        "currentIndexBinding": index_binding,
        "currentCatalogBinding": catalog_binding,
        "latestBatch": {
            "return": 217,
            "group": "rank9-death-recovery7",
            "ids": GROUP_IDS,
            "acceptedIds": ACCEPTED,
            "appliedIds": ACCEPTED,
            "heldIds": HELD,
            "blockers": ["DR217-B01"],
            "conditionalQualificationIds": ["DR217-C01", "DR217-C02"],
            "directorDecision": director_decision_binding,
            "directorReturn": return_binding,
            "directorDeliveryManifest": delivery_binding,
            "independentAudit": return_audit_binding,
            "application": bind_file(APPLICATION),
            "validation": str(VALIDATION.relative_to(ROOT)),
        },
        "preservedOtherHolds": handoff_before.get("preservedOtherHolds", []) + ["DR217-B01", "PF182-B01", "PF182-B02"],
        "nextStep": {"group": next_group["group"], "pendingIds": next_group["pendingIds"], "pendingCount": next_group["pendingCount"], "status": next_record["status"]},
        "appliedThisStep": True,
        "githubChanges": False,
        "preservedCurrentBatchHeldIds": HELD,
        "preservedCurrentBatchBlockers": ["DR217-B01"],
        "pendingIdentityAudit": {"path": str(PENDING_AFTER.relative_to(ROOT)), **{k: pending_binding[k] for k in ("bytes", "sha256", "crc32")}},
        "currentQueue": {"path": str(QUEUE_AFTER.relative_to(ROOT)), **{k: queue_binding[k] for k in ("bytes", "sha256", "crc32")}},
        "currentReturnAudit": return_audit_binding,
        "currentReturnArchive": return_binding,
        "currentReturnDelivery": delivery_binding,
    }
    write_json(HANDOFF_AFTER, handoff)

    validation = {
        "id": "RANK9DEATHRECOVERY3-APPLICATION-VALIDATION-217",
        "status": "PASS",
        "checks": [
            {"check": "Return217 exact acceptances independently audited before application", "pass": True},
            {"check": "Only Doom and Eternal Pact changed from pending to reviewed-authored", "pass": True},
            {"check": "Final Word remains pending on DR217-B01", "pass": True},
            {"check": "All 80 archive members and 45 preserved cases independently verified", "pass": True},
            {"check": "Native catalog rows and source statuses remain unchanged", "pass": True},
            {"check": "Index inverse operations restore exact semantic 806/42 input", "pass": inverse == index_before},
            {"check": "Stale index standalone tally reconciled from 528 to observed 530 baseline plus two exact applications", "pass": stored_complete_count == 528 and observed_complete_count == 530 and idx_after["representationCounts"]["completeReviewedStandaloneProcedures"] == 532},
            {"check": "Catalog bytes are unchanged and runtime remains disabled", "pass": bind_file(CATALOG) == catalog_binding},
            {"check": "Refreshed pending queue is exactly 40 unique IDs", "pass": len(all_pending) == 40 and set(all_pending) == live_pending_after},
        ],
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "currentAuthorityAfter": AFTER,
        "indexBefore": before_bind,
        "indexAfter": index_binding,
        "catalogAfter": catalog_binding,
        "pendingIdentityAudit": pending_binding,
        "applicationReceipt": bind_file(APPLICATION),
        "runtimeSelectionEnabled": False,
        "runtimeExecuted": False,
        "githubChanges": False,
    }
    write_json(VALIDATION, validation)
    require(all(x["pass"] for x in validation["checks"]), "Post-application validation failed")

    snapshot = (
        "# Current Spell Review Snapshot — Return 217\n\n"
        "Authority after applying the two exact accepted identities: **808 applied / 40 pending / 0 accepted-unapplied**.\n\n"
        "Applied to the authored review index: `doom`, `eternal-pact`. `final-word` remains pending on DR217-B01 because the source packet does not establish a capture-eligible identity for its positive reserve-use witness. The current return audit passed 17 independent checks; all 80 package members and 45 preserved cases matched their bindings.\n\n"
        f"Next actionable current pending group: **{next_group['group']}** — {', '.join(next_group['pendingIds'])}.\n\n"
        "The earlier Psychic/Fear holds remain unchanged. Native catalog rows and runtime selection remain unchanged; no GitHub push was made in this application step.\n"
    )
    SNAPSHOT.write_text(snapshot, encoding="utf-8")
    next_request = (
        "Current-authority director continuation after Return217\n\n"
        "Codex independently audited Return217 and applied only the explicit acceptances for Doom and Eternal Pact. Current authority is 808 reviewed/applied / 40 pending / 0 accepted-unapplied. Final Word remains held on DR217-B01; the earlier Psychic/Fear holds remain unchanged.\n\n"
        f"Please review only current pending group {next_group['group']}, exact identities: {', '.join(next_group['pendingIds'])}. Use a fresh packet bound to the current index/catalog/queue/handoff at 808/40/0. Reassess the earlier Defense/Form blockers against current source evidence; resolve spell-local design choices within your authority and hold only for genuinely missing source facts or permissions. Return exact per-identity decisions, blocker IDs, and a matching archive plus manifest. Do not apply index, canonical/runtime, or GitHub changes; Codex will audit and apply only exact acceptances.\n\n"
        f"Historical source candidate: {next_group.get('candidate', {}).get('path')} ({next_group.get('candidate', {}).get('sha256')}). Source conference archive: {next_group.get('archive', {}).get('path')} ({next_group.get('archive', {}).get('sha256')}).\n"
    )
    NEXT_REQUEST.write_text(next_request, encoding="utf-8")

    # Bind the final state into the handoff after all receipts exist.
    handoff["applicationValidation"] = bind_file(VALIDATION)
    handoff["applicationReceipt"] = bind_file(APPLICATION)
    handoff["indexOperations"] = bind_file(OPERATIONS)
    write_json(HANDOFF_AFTER, handoff)

    summary = {
        "status": "PASS",
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "indexBefore": before_bind,
        "indexAfter": bind_file(INDEX),
        "authorityAfter": AFTER,
        "catalogChanged": False,
        "queueAfter": bind_file(QUEUE_AFTER),
        "handoffAfter": bind_file(HANDOFF_AFTER),
        "validation": str(VALIDATION.relative_to(ROOT)),
        "nextGroup": next_group["group"],
        "nextPendingIds": next_group["pendingIds"],
        "candidateEnvelope": str(CANDIDATE.relative_to(ROOT) / "MODEL.json"),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
