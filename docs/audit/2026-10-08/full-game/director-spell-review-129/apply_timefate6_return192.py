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
RECEIVED = AUDIT / "rank9_timefate6_return192_received"
ARCHIVE = RECEIVED / "DD_Rank9_TimeFate6_Director_Return192.zip"
DELIVERY = RECEIVED / "DD_Rank9_TimeFate6_Director_Return192_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_TIMEFATE6_RETURN192_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_191.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_191.json"
PENDING_BEFORE = AUDIT / "CURRENT71_PENDING_IDENTITY_AUDIT_191.json"
BEFORE_BACKUP = AUDIT / "authored_review_index.before_timefate6_192.json"
CANDIDATE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192")
CANDIDATE = ROOT / CANDIDATE_REL
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_TIMEFATE6_REVIEWED_192.md"
GROUP = ["time-stop", "time-fracture", "foresight-perfect", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
ACCEPTED = ["time-fracture", "foresight-perfect"]
UNACCEPTED = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
BLOCKERS = {"time-stop": ["TF192-B01"], "eternal-prophecy": ["TF192-B02"], "fate-rewrite": ["TF192-B04"], "collapse-timeline": ["TF192-B05"]}
NEXT_GROUP = "rank9-casting-cost5"
NEXT_IDS = ["perfect-spell", "ritual-mastery", "world-rewrite", "resonance-perfection", "unholy-ascendance"]
BEFORE = {"reviewed": 777, "pending": 71}
AFTER = {"reviewed": 779, "pending": 69}
COMPLETE_BEFORE, COMPLETE_AFTER = 501, 503
REVIEW_ID = "RANK9-TIMEFATE6-EXACT-AUTHORED-ACCEPTANCE-192"
APP_ID = "RANK9-TIMEFATE6-APPLICATION-192"
DECISION_PATH = AUDIT / "RANK9_TIMEFATE6_DIRECTOR_DECISION_192.json"
ACCEPTANCE_PATH = AUDIT / "RANK9_TIMEFATE6_EXACT_ACCEPTANCE_192.json"
RECEIPT_PATH = AUDIT / "RANK9_TIMEFATE6_RETURN192_RECEIPT.json"
APPLICATION_PATH = AUDIT / "RANK9_TIMEFATE6_APPLICATION_192.json"
OPERATIONS_PATH = AUDIT / "RANK9_TIMEFATE6_INDEX_OPERATIONS_192.json"
PENDING_AFTER = AUDIT / "CURRENT69_PENDING_IDENTITY_AUDIT_192.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_192.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_192.json"
VALIDATION_PATH = AUDIT / "RANK9_TIMEFATE6_APPLICATION_VALIDATION_192.json"
SNAPSHOT_PATH = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_192.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def bind(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    rel = path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
    return {"path": rel, "bytes": len(data), "sha256": sha(data)}


def main() -> None:
    outputs = [BEFORE_BACKUP, MANUSCRIPT, DECISION_PATH, ACCEPTANCE_PATH, RECEIPT_PATH, APPLICATION_PATH,
               OPERATIONS_PATH, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, VALIDATION_PATH, SNAPSHOT_PATH]
    assert not CANDIDATE.exists() and not STAGING.exists(), "Candidate package already exists; inspect before retrying"
    assert all(not path.exists() for path in outputs), "An application output already exists; inspect before retrying"
    audit = read_json(INDEPENDENT_AUDIT)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["checksPassed"] == 18
    assert audit["acceptedIds"] == ACCEPTED and audit["unacceptedIds"] == UNACCEPTED and audit["applied"] is False
    delivery = read_json(DELIVERY)
    assert ARCHIVE.stat().st_size == delivery["archive"]["bytes"] == 90_939_303
    assert sha_file(ARCHIVE) == delivery["archive"]["sha256"] == audit["returnArchive"]["sha256"]
    assert delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED
    assert delivery["applied"] is False and delivery["appliedIds"] == [] and delivery["canonicalFilesModified"] is False
    assert delivery["sourceAuthority"] == {"reviewedApplied": 777, "pending": 71, "acceptedUnapplied": 0,
                                           "completeStandaloneProcedures": 501, "scopedInterfaces": 173}

    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read_json(INDEX), read_json(CATALOG)
    queue_before, handoff_before, pending_before = map(read_json, (QUEUE_BEFORE, HANDOFF_BEFORE, PENDING_BEFORE))
    assert before["authoredCounts"] == BEFORE
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    rows = {row["id"]: row for row in before["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    live_pending = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == BEFORE["pending"] and set(GROUP) <= live_pending
    assert pending_before["pendingCount"] == BEFORE["pending"] and set(pending_before["pendingIds"]) == live_pending
    assert pending_before["indexBinding"]["sha256"] == sha(before_raw)
    assert queue_before["currentAuthority"]["reviewedApplied"] == BEFORE["reviewed"]
    assert queue_before["currentAuthority"]["pending"] == BEFORE["pending"]
    assert all(rows[sid]["sourceStatus"] == "blocked-pending-operational-review" for sid in GROUP)

    timestamp = datetime.now(timezone.utc).isoformat()
    with zipfile.ZipFile(ARCHIVE) as archive:
        director = json.loads(archive.read("DIRECTOR_DECISION.json"))
        procedures_doc = json.loads(archive.read("PROCEDURES.json"))
        procedures = {row["spellId"]: row for row in procedures_doc["spells"]}
        decisions = {row["spellId"]: row for row in director["perIdentity"]}
        assert set(procedures) == set(decisions) == set(GROUP)
        assert director["acceptedIds"] == ACCEPTED and director["unacceptedIds"] == UNACCEPTED
        assert director["applied"] is False and director["canonicalFilesModified"] is False
        assert director["authorityAtReview"] == delivery["sourceAuthority"]
        assert all(decisions[sid]["accepted"] and not decisions[sid]["applied"] and not decisions[sid]["blockerIds"] for sid in ACCEPTED)
        assert all(not decisions[sid]["accepted"] and decisions[sid]["blockerIds"] == BLOCKERS[sid] for sid in UNACCEPTED)
        assert all(not procedures[sid]["applied"] for sid in GROUP)
        assert all(procedures[sid]["currentCatalogSourceAndAccessUnchanged"] == catalog_rows[sid] for sid in GROUP)
        assert all(procedures[sid]["currentIndexEntryUnchanged"] == rows[sid] for sid in GROUP)

        # Copy authored evidence only; the archive's supplied and historical programs are never executed.
        STAGING.mkdir(parents=True)
        keep = ["ACTOR_PROFILES.json", "CASE_DISPOSITIONS.json", "CASE_HASH_BINDINGS.json", "COUNTS.json",
                "CURRENT_CONTEXT_191.json", "DIRECTOR_DECISION.json", "EVIDENCE_MANIFEST.json",
                "FUTURE_OBLIGATIONS.json", "HOLD_REGISTER.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
                "LEGACY_QUESTION_DISPOSITIONS.json", "ORIGINAL_QUESTIONS.json", "PROCEDURES.json",
                "PROPOSAL_OPERATIONS.json", "QUALIFICATIONS.json", "QUESTION_COUNT_RECONCILIATION.json",
                "QUESTION_DISPOSITIONS.json", "SOURCE_BINDINGS.json", "SOURCE_VERIFICATION.json",
                "STANDALONE_PROCEDURES.md", "VALIDATION.json"]
        for name in keep:
            (STAGING / name).write_bytes(archive.read(name))
        for sid in GROUP:
            out = STAGING / "procedures" / f"{sid}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(archive.read(f"procedures/{sid}.json"))
        casebook_raw = archive.read("CASEBOOK.json")
        with (STAGING / "CASEBOOK.json.gz").open("wb") as compressed:
            with gzip.GzipFile(fileobj=compressed, mode="wb", filename="", mtime=0, compresslevel=6) as gz:
                gz.write(casebook_raw)
        (STAGING / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGING / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(INDEPENDENT_AUDIT.read_bytes())

        archive_binding, delivery_binding, audit_binding = bind(ARCHIVE), bind(DELIVERY), bind(INDEPENDENT_AUDIT)
        casebook_member = next(row for row in delivery["members"] if row["path"] == "CASEBOOK.json")
        casebook_source_binding = {"path": "CASEBOOK.json", "bytes": casebook_member["bytes"], "sha256": casebook_member["sha256"]}
        casebook_binding = bind(CANDIDATE_REL / "CASEBOOK.json.gz", (STAGING / "CASEBOOK.json.gz").read_bytes())
        spells = []
        for pos, sid in enumerate(ACCEPTED):
            source = procedures[sid]
            spells.append({"id": sid, "name": rows[sid]["name"], "position": pos,
                           "procedure": {"id": f"TF192-STATIC-PROCEDURE-{sid.upper().replace('-', '_')}", "spellId": sid,
                                         "status": "director-accepted static authored procedure; applied to authored review index; runtime remains disabled",
                                         "accepted": True, "applied": False,
                                         "nativeCardUnchanged": copy.deepcopy(source["currentCatalogSourceAndAccessUnchanged"]),
                                         "procedureContent": copy.deepcopy(source["procedure"]),
                                         "sharedRequirements": copy.deepcopy(source["sharedRequirements"]),
                                         "orderedExecution": copy.deepcopy(source["orderedExecution"]),
                                         "holdIds": copy.deepcopy(source["holdIds"]), "caseIds": copy.deepcopy(source["caseIds"]),
                                         "directorDecisionId": director["id"]},
                           "directorProcedureRecord": copy.deepcopy(source),
                           "nativeCardUnchanged": copy.deepcopy(source["currentCatalogSourceAndAccessUnchanged"]),
                           "caseIds": copy.deepcopy(source["caseIds"]), "questionIds": copy.deepcopy(source["questionIds"]),
                           "holdIds": copy.deepcopy(source["holdIds"]), "runtimeSelectionEnabled": False})
        unaccepted_decisions = [copy.deepcopy(decisions[sid]) for sid in UNACCEPTED]
        unaccepted_holds = {sid: {"blockerIds": copy.deepcopy(decisions[sid]["blockerIds"]),
                                  "holdIds": copy.deepcopy(procedures[sid]["holdIds"]),
                                  "reason": "Retained director blocker; see exact blocker record in DIRECTOR_DECISION.json."}
                            for sid in UNACCEPTED}
        excluded_pending = sorted(live_pending - set(ACCEPTED))
        package_manifest = {"id": "RANK9-TIMEFATE6-CANDIDATE-PACKAGE-MANIFEST-192", "sourceArchive": archive_binding,
                            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
                            "sourceAnchorCommit": audit["sourceCommit"], "files": []}
        for file in sorted(path for path in STAGING.rglob("*") if path.is_file()):
            raw = file.read_bytes()
            package_manifest["files"].append({"path": (CANDIDATE_REL / file.relative_to(STAGING)).as_posix(),
                                              "bytes": len(raw), "sha256": sha(raw)})
        write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
        manifest_binding = bind(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json",
                                (STAGING / "CANDIDATE_PACKAGE_MANIFEST.json").read_bytes())
        model = {"schemaVersion": 1, "moduleId": "rank9-timefate6-reviewed-192",
                 "status": "TWO_EXACT_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_FOUR_RETAINED_BLOCKERS",
                 "scope": "Exactly the two director-accepted identities are applied as static authored procedures. Four identities remain pending under their named blockers. Native catalog cards and class routes remain unchanged; runtime and downstream approval gates stay disabled.",
                 "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "excludedPendingIds": excluded_pending,
                 "unacceptedDecisions": unaccepted_decisions, "unacceptedHolds": unaccepted_holds,
                 "inheritedBlockers": copy.deepcopy(director["carryForwardExact"]),
                 "sharedRequirements": {"scope": "No global or shared rule changes; native cards and class routes remain unchanged.",
                                        "runtimeSelectionEnabled": False},
                 "spells": spells,
                 "caseCoverage": {"caseCount": delivery["counts"]["cases"],
                                  "acceptedCaseCount": sum(len(procedures[sid]["caseIds"]) for sid in ACCEPTED),
                                  "eventCount": sum(delivery["counts"]["perIdentity"][sid]["events"] for sid in ACCEPTED),
                                  "independentReplay": audit["replay"]},
                 "returnCounts": delivery["counts"], "blockers": unaccepted_holds,
                 "sourceArchive": archive_binding, "deliveryManifest": delivery_binding,
                 "independentAudit": audit_binding, "casebookFile": "CASEBOOK.json.gz",
                 "casebookSourceArchiveMemberBinding": casebook_source_binding, "casebookBinding": casebook_binding,
                 "candidatePackageManifestBinding": manifest_binding, "runtimeSelectionEnabled": False,
                 "runtimeTestsExecuted": False, "sourceProgramsExecuted": False, "implementationApproved": False,
                 "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
                 "releaseApproved": False, "domainClosure": False}
        write_json(STAGING / "MODEL.json", model)
        shutil.move(str(STAGING), str(CANDIDATE))

    model_binding = bind(CANDIDATE_REL / "MODEL.json")
    manifest_binding = bind(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json")
    casebook_binding = bind(CANDIDATE_REL / "CASEBOOK.json.gz")
    manuscript_raw = (CANDIDATE / "STANDALONE_PROCEDURES.md").read_bytes()
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_bytes(manuscript_raw)
    shutil.copyfile(INDEX, BEFORE_BACKUP)
    assert BEFORE_BACKUP.read_bytes() == before_raw

    blockers = unaccepted_holds
    write_json(DECISION_PATH, {"id": director["id"], "recordedAtUtc": timestamp, "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE",
                               "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "blockers": blockers,
                               "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
                               "independentAudit": audit_binding, "authorityAtDecision": delivery["sourceAuthority"],
                               "exactDirectorDecisions": director["perIdentity"], "inheritedBlockersCarriedForward": director["carryForwardExact"],
                               "scope": "Static authored procedure acceptance only. No runtime, implementation, human-play, balance, cosmology, closure, completion, or release approval.",
                               "canonicalFilesChangedByDirector": False})
    acceptance = {"id": REVIEW_ID, "recordedAtUtc": timestamp,
                  "status": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_FOUR_RETAINED_BLOCKERS",
                  "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "directorDecision": bind(DECISION_PATH),
                  "directorReturn": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
                  "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding,
                  "countsBefore": BEFORE, "countsAfter": AFTER,
                  "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
                  "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER, "blockers": blockers,
                  "runtimeSelectionEnabled": False, "canonicalApplicationPerformedByOwner": False}
    write_json(ACCEPTANCE_PATH, acceptance)
    write_json(RECEIPT_PATH, {"id": "RANK9-TIMEFATE6-DIRECTOR-RETURN-192-RECEIPT", "recordedAtUtc": timestamp,
                              "status": "DIRECTOR_PARTIALLY_ACCEPTED_TWO_EXACT_IDENTITIES; FOUR_REMAIN_BLOCKED; INDEPENDENT_AUDIT_PASSED",
                              "reviewedIds": GROUP, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
                              "blockers": blockers, "inheritedBlockers": director["carryForwardExact"],
                              "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
                              "independentAudit": audit_binding, "sourceAuthority": delivery["sourceAuthority"],
                              "counts": delivery["counts"], "decisionId": director["id"]})
    application = {"id": APP_ID, "recordedAtUtc": timestamp,
                   "status": "APPLIED_TWO_EXACT_AUTHORED_PROCEDURES_WITH_FOUR_RETAINED_BLOCKERS",
                   "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.",
                   "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
                   "directorAcceptance": bind(ACCEPTANCE_PATH), "directorDecision": bind(DECISION_PATH),
                   "directorReturnReceipt": bind(RECEIPT_PATH), "directorReturn": archive_binding,
                   "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
                   "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding,
                   "manuscript": bind(MANUSCRIPT), "indexBefore": bind(BEFORE_BACKUP, before_raw),
                   "countsBefore": BEFORE, "countsAfter": AFTER,
                   "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
                   "sourceStatusPreservedAsBlocked": True, "catalogChanged": False, "runtimeSelectionEnabled": False}
    write_json(APPLICATION_PATH, application)
    application_binding = bind(APPLICATION_PATH)

    after = copy.deepcopy(before)
    operations = []
    for pos, sid in enumerate(ACCEPTED):
        index_pos = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index_pos]
        new = copy.deepcopy(old)
        new.update({"authoredStatus": "reviewed-authored-operational-playtest",
                    "procedureFile": "../spell_candidates/rank9timefate6_reviewed_192/MODEL.json",
                    "procedurePointer": f"/spells/{pos}/procedure", "wholeCardPointer": f"/spells/{pos}",
                    "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
                    "wholeCardIdField": "id", "procedureTextPointer": f"/spells/{pos}/procedure/procedureContent",
                    "directorProcedureRecordPointer": f"/spells/{pos}/directorProcedureRecord",
                    "sharedRulesPointer": f"/spells/{pos}/procedure/sharedRequirements",
                    "manuscript": "../../../docs/spells/candidates/RANK9_TIMEFATE6_REVIEWED_192.md",
                    "reviewId": APP_ID, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
                    "completeEvidenceRoot": CANDIDATE_REL.as_posix(), "completeEnvelopeBinding": model_binding,
                    "casebookBinding": casebook_binding,
                    "casebookEncoding": "Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the director return archive.",
                    "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
                    "sourceArchiveBinding": archive_binding, "candidatePackageManifestBinding": manifest_binding,
                    "procedureSourceBinding": bind(DECISION_PATH), "authoredAcceptanceReceipt": bind(ACCEPTANCE_PATH),
                    "authoredApplicationReceipt": application_binding})
        assert new["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review"
        operations.append({"op": "replace-entry", "identity": sid, "index": index_pos,
                           "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][index_pos] = new
    excluded_pending = sorted(live_pending - set(ACCEPTED))
    after["additionalStandaloneEnvelopes"].append({"file": "../spell_candidates/rank9timefate6_reviewed_192/MODEL.json",
                                                   "binding": model_binding, "reviewId": REVIEW_ID,
                                                   "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
                                                   "excludedPendingIds": excluded_pending, "authority": bind(ACCEPTANCE_PATH),
                                                   "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(),
                                                   "sourceArchive": archive_binding, "casebookBinding": casebook_binding,
                                                   "candidatePackageManifestBinding": manifest_binding,
                                                   "scope": acceptance["status"], "runtimeSelectionEnabled": False})
    after["authoredCounts"] = AFTER
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert pending_after == live_pending - set(ACCEPTED) and len(pending_after) == AFTER["pending"]
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_raw = json_bytes(after)
    temp = INDEX.with_suffix(".json.timefate6-192.tmp")
    temp.write_bytes(after_raw)
    temp.replace(INDEX)
    assert CATALOG.read_bytes() == catalog_raw
    write_json(OPERATIONS_PATH, {"id": "RANK9-TIMEFATE6-INDEX-OPERATIONS-192",
                                 "before": bind(BEFORE_BACKUP, before_raw), "after": bind(INDEX, after_raw),
                                 "operations": operations, "inverseSemanticExact": True, "onlyIdentityIds": ACCEPTED})

    new_groups = []
    for old_group in queue_before["currentPendingGroups"]:
        left = [sid for sid in old_group["pendingIds"] if sid in pending_after]
        if not left:
            continue
        row = copy.deepcopy(old_group)
        row["pendingIds"], row["pendingCount"] = left, len(left)
        if row["group"] == "rank9-time-fate6":
            row.update({"status": "PARTIAL_RETURN192_TWO_ACCEPTED_APPLIED_FOUR_SOURCE_EVIDENCE_BLOCKED",
                        "freshPacketRequiredForCurrentAuthority": True,
                        "blockingReturn": {"receipt": RECEIPT_PATH.relative_to(ROOT).as_posix(),
                                           "ids": UNACCEPTED, "blockers": blockers}})
        if row["group"] == NEXT_GROUP:
            row.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True})
        new_groups.append(row)
    next_group = next(row for row in new_groups if row["group"] == NEXT_GROUP)
    authority = {"reviewedApplied": 779, "pending": 69, "acceptedUnapplied": 0,
                 "completeStandaloneProcedures": 503, "scopedInterfaces": 173}
    pending_doc = {"id": "CURRENT69-PENDING-IDENTITY-AUDIT-192", "recordedAtUtc": timestamp,
                   "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX, after_raw),
                   "catalogBinding": bind(CATALOG, catalog_raw), "authoredCounts": AFTER,
                   "pendingCount": AFTER["pending"], "pendingIds": sorted(pending_after),
                   "allPendingExistInSourceCatalog": pending_after <= set(catalog_rows), "acceptedUnapplied": 0,
                   "retainedReturn188Blockers": pending_before["retainedReturn188Blockers"],
                   "retainedReturn190Blockers": pending_before["retainedReturn190Blockers"],
                   "retainedReturn192Blockers": blockers, "closed335AndCompletedCohortsReopened": False}
    write_json(PENDING_AFTER, pending_doc)
    next_request = {"group": NEXT_GROUP, "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS),
                    "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
                    "freshPacketRequiredForCurrentAuthority": True,
                    "candidate": next_group.get("candidate"), "archive": next_group.get("archive")}
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-192", "recordedAtUtc": timestamp,
                        "currentAuthority": authority, "pendingCount": AFTER["pending"],
                        "currentPendingGroups": new_groups,
                        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": len(ACCEPTED),
                                             "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(),
                                             "directorAcceptance": ACCEPTANCE_PATH.relative_to(ROOT).as_posix(),
                                             "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()},
                        "pendingIdentityAudit": {"path": PENDING_AFTER.relative_to(ROOT).as_posix(),
                                                 "pending": AFTER["pending"], "sha256": sha(PENDING_AFTER.read_bytes())},
                        "nextGroup": NEXT_GROUP, "next": next_request, "nextPreparedRequest": next_request,
                        "packetStatus": "RANK9_TIMEFATE6_RETURN192_TWO_APPLIED_FOUR_HELD_779_69_NEXT_RANK9_CASTING_COST5",
                        "currentReturnBinding": archive_binding, "currentPreparation": audit_binding,
                        "currentReturnAudit": audit_binding})
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery"):
        queue_after.pop(key, None)
    queue_after["currentSubmission"] = bind(RECEIPT_PATH)
    queue_after["currentSubmissionBinding"] = bind(RECEIPT_PATH)
    queue_after["currentReturnBinding"] = archive_binding
    queue_after["currentReturnAudit"] = audit_binding
    write_json(QUEUE_AFTER, queue_after)

    handoff = copy.deepcopy(handoff_before)
    handoff.update({"id": "CURRENT-HANDOFF-192", "recordedAtUtc": timestamp,
                    "status": "RANK9_TIMEFATE6_TWO_APPLIED_FOUR_HELD_NEXT_RANK9_CASTING_COST5_69_PENDING",
                    "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw),
                    "currentCatalogBinding": bind(CATALOG, catalog_raw),
                    "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.relative_to(ROOT).as_posix(),
                                             "pendingCount": AFTER["pending"], "sha256": sha(PENDING_AFTER.read_bytes())},
                    "appliedThisStep": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": len(ACCEPTED),
                                        "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(),
                                        "directorAcceptance": ACCEPTANCE_PATH.relative_to(ROOT).as_posix(),
                                        "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(),
                                        "applicationValidation": {"path": VALIDATION_PATH.relative_to(ROOT).as_posix()}},
                    "unacceptedThisStep": {"ids": UNACCEPTED, "blockers": blockers, "retainedInPendingSet": True},
                    "nextGroup": NEXT_GROUP, "nextPendingCount": len(NEXT_IDS), "nextPreparedRequest": next_request,
                    "currentQueueBinding": bind(QUEUE_AFTER), "currentReturnBinding": archive_binding,
                    "independentAuditBinding": audit_binding, "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(),
                    "currentSubmissionBinding": bind(RECEIPT_PATH), "currentReturnAudit": audit_binding,
                    "resumePriority": "Prepare a fresh current-source packet for Rank9 Casting Cost5 against 779/69 authority for the same GPT director; independently audit the return, apply only exact accepted IDs, push, and continue in queue order until pending reaches zero."})
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        handoff.pop(key, None)
    write_json(HANDOFF_AFTER, handoff)

    checks = [
        {"check": "Independent Return192 audit passed and archive binding matches", "passed": audit["status"] == "PASS" and sha_file(ARCHIVE) == archive_binding["sha256"]},
        {"check": "Exactly two accepted identities applied; four blockers remain pending", "passed": [op["identity"] for op in operations] == ACCEPTED and set(UNACCEPTED) <= pending_after},
        {"check": "Authority changed exactly from 777/71/501 to 779/69/503", "passed": after["authoredCounts"] == AFTER and after["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_AFTER},
        {"check": "Pending set equals prior set minus exact accepted IDs", "passed": pending_after == live_pending - set(ACCEPTED)},
        {"check": "Index inverse restores exact prior value and catalog remains byte-identical", "passed": inverse == before and CATALOG.read_bytes() == catalog_raw},
        {"check": "Candidate package binds every staged evidence member", "passed": all((ROOT / row["path"]).is_file() and (ROOT / row["path"]).stat().st_size == row["bytes"] and sha_file(ROOT / row["path"]) == row["sha256"] for row in package_manifest["files"])},
        {"check": "Next group is Casting Cost5 with the five exact pending IDs", "passed": queue_after["nextGroup"] == NEXT_GROUP and next_group["pendingIds"] == NEXT_IDS},
        {"check": "Runtime and downstream approval gates remain disabled", "passed": model["runtimeSelectionEnabled"] is False and all(model[key] is False for key in ("runtimeTestsExecuted", "sourceProgramsExecuted", "implementationApproved", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))},
    ]
    validation = {"id": "RANK9-TIMEFATE6-APPLICATION-VALIDATION-192", "recordedAtUtc": timestamp,
                  "status": "PASS" if all(row["passed"] for row in checks) else "FAIL",
                  "checksPassed": sum(row["passed"] for row in checks),
                  "checksFailed": sum(not row["passed"] for row in checks), "checks": checks,
                  "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
                  "countsBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE_BEFORE},
                  "countsAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE_AFTER},
                  "indexBefore": bind(BEFORE_BACKUP, before_raw), "indexAfter": bind(INDEX),
                  "catalog": bind(CATALOG), "application": bind(APPLICATION_PATH),
                  "independentAudit": audit_binding, "pendingIdentityAudit": bind(PENDING_AFTER),
                  "queueAfter": bind(QUEUE_AFTER), "handoffAfter": bind(HANDOFF_AFTER),
                  "nextGroup": NEXT_GROUP, "runtimeSelectionEnabled": False}
    write_json(VALIDATION_PATH, validation)
    assert validation["status"] == "PASS", checks
    SNAPSHOT_PATH.write_text(
        f"# Current ordinary spell-review checkpoint 192\n\nReturn192 passed all {audit['checksPassed']} independent checks, including replay of {audit['replay']['acceptedCases']} accepted cases and {audit['replay']['events']} reversible events. Exactly {ACCEPTED[0]} and {ACCEPTED[1]} were applied as static authored procedures. Four other Time/Fate identities stay pending under TF192-B01, TF192-B02, TF192-B04 and TF192-B05. Authority: **779 reviewed / 69 pending / 0 accepted-unapplied**, with 503 complete standalone procedures. The next group is Rank9 Casting Cost5.\n\nSee [handoff](CURRENT_HANDOFF_192.json), [queue](CURRENT_SPELL_QUEUE_192.json), [pending audit](CURRENT69_PENDING_IDENTITY_AUDIT_192.json), [independent audit](RANK9_TIMEFATE6_RETURN192_INDEPENDENT_AUDIT.json), and [application validation](RANK9_TIMEFATE6_APPLICATION_VALIDATION_192.json).\n",
        encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(
        f"**Current ordinary spell-review handoff [192](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_192.json):** Return192 was independently audited and applied for exactly {ACCEPTED[0]} and {ACCEPTED[1]}. Authority is **779 reviewed / 69 pending / 0 accepted-unapplied**. The four other Time/Fate identities remain pending under TF192-B01, TF192-B02, TF192-B04 and TF192-B05. The next group is Rank9 Casting Cost5. See [handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_192.json) and [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT69_PENDING_IDENTITY_AUDIT_192.json).\n\n" + old_start,
        encoding="utf-8", newline="\n")
    assert CATALOG.read_bytes() == catalog_raw
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
                      "authority": authority, "nextGroup": NEXT_GROUP, "nextPendingCount": len(NEXT_IDS),
                      "independentAudit": audit["status"], "validation": validation["status"],
                      "indexSha256": sha_file(INDEX), "candidatePackageManifest": manifest_binding},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
