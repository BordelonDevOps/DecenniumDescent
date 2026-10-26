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
RECEIVED = AUDIT / "rank9_wardcontrol6_return188_received"
RETURN = RECEIVED / "DD_Rank9_WardControl6_Director_Return188.zip"
DELIVERY = RECEIVED / "DD_Rank9_WardControl6_Director_Return188_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_WARDCONTROL6_RETURN188_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_187.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_187.json"
PENDING_BEFORE = AUDIT / "CURRENT82_PENDING_IDENTITY_AUDIT_187.json"
BEFORE_BACKUP = AUDIT / "authored_review_index.before_wardcontrol6_188.json"
CANDIDATE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9wardcontrol6_reviewed_188")
CANDIDATE = ROOT / CANDIDATE_REL
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging_retry3")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_WARDCONTROL6_REVIEWED_188.md"
ACCEPTED = ["greater-spell-turning", "eternal-ward", "ultimate-ward", "prismatic-sphere"]
UNACCEPTED = ["nullification-wave", "reality-anchor"]
GROUP = ACCEPTED[:1] + ["nullification-wave", "eternal-ward", "ultimate-ward", "reality-anchor", "prismatic-sphere"]
NEXT_GROUP = "rank9-agency-control9"
NEXT_IDS = ["absolute-domination", "command-reality", "dominate-legion", "erase-soul", "overwhelming-presence", "perfect-mesmerize", "prophecy-fulfilled", "puppetmaster-s-realm", "rewrite-loyalty"]
BEFORE = {"reviewed": 766, "pending": 82, "acceptedUnapplied": 0}
AFTER = {"reviewed": 770, "pending": 78, "acceptedUnapplied": 0}
COMPLETE_BEFORE, COMPLETE_AFTER = 490, 494
REVIEW_ID = "RANK9-WARDCONTROL6-EXACT-AUTHORED-ACCEPTANCE-188"
APP_ID = "RANK9-WARDCONTROL6-APPLICATION-188"
DECISION_PATH = AUDIT / "RANK9_WARDCONTROL6_DIRECTOR_DECISION_188.json"
ACCEPTANCE_PATH = AUDIT / "RANK9_WARDCONTROL6_EXACT_ACCEPTANCE_188.json"
RECEIPT_PATH = AUDIT / "RANK9_WARDCONTROL6_RETURN188_RECEIPT.json"
APPLICATION_PATH = AUDIT / "RANK9_WARDCONTROL6_APPLICATION_188.json"
OPERATIONS_PATH = AUDIT / "RANK9_WARDCONTROL6_INDEX_OPERATIONS_188.json"
PENDING_AFTER = AUDIT / "CURRENT78_PENDING_IDENTITY_AUDIT_188.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_188.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_188.json"
VALIDATION_PATH = AUDIT / "RANK9_WARDCONTROL6_APPLICATION_VALIDATION_188.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
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
    assert not CANDIDATE.exists() and not STAGING.exists(), "Candidate output exists; inspect before retrying"
    audit, delivery = read_json(INDEPENDENT_AUDIT), read_json(DELIVERY)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["acceptedIds"] == ACCEPTED
    assert audit["unacceptedIds"] == UNACCEPTED and audit["applied"] is False
    assert RETURN.stat().st_size == delivery["bytes"] and sha_file(RETURN) == delivery["sha256"]
    assert delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED
    assert delivery["batchAcceptedInFull"] is False and delivery["applied"] is False
    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read_json(INDEX), read_json(CATALOG)
    assert before["authoredCounts"] == {"reviewed": 766, "pending": 82}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    rows = {r["id"]: r for r in before["entries"]}
    live_pending = {r["id"] for r in before["entries"] if r["authoredStatus"] == "pending-authored-procedure"}
    assert set(ACCEPTED + UNACCEPTED) <= live_pending
    assert all(rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in ACCEPTED + UNACCEPTED)
    assert all(not p.exists() for p in (BEFORE_BACKUP, CANDIDATE, MANUSCRIPT, DECISION_PATH, ACCEPTANCE_PATH, RECEIPT_PATH, APPLICATION_PATH, OPERATIONS_PATH, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER, VALIDATION_PATH))
    queue_before, handoff_before, pending_before = map(read_json, (QUEUE_BEFORE, HANDOFF_BEFORE, PENDING_BEFORE))
    assert queue_before["currentAuthority"]["reviewedApplied"] == 766 and queue_before["currentAuthority"]["pending"] == 82
    assert pending_before["pendingCount"] == 82 and set(pending_before["pendingIds"]) == live_pending

    timestamp = datetime.now(timezone.utc).isoformat()
    with zipfile.ZipFile(RETURN) as archive:
        assert archive.testzip() is None
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        procedures_doc = json.loads(archive.read("PROCEDURES.json"))
        procedures = {r["id"]: r for r in procedures_doc["procedures"]}
        decisions = {r["spellId"]: r for r in decision["decisions"]}
        blockers = {sid: {"blockerIds": row["blockerIds"], "holdIds": next(b["holdIds"] for b in decision["blockers"] if sid in b["spellIds"])} for sid, row in decisions.items() if sid in UNACCEPTED}
        questions = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        qmap = {q["questionId"]: q for q in questions["dispositions"]}
        assert set(procedures) == set(decisions) == set(ACCEPTED + UNACCEPTED)
        assert decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == UNACCEPTED
        assert decision["authorityBeforeAndStillCanonical"] == {"acceptedUnapplied": 0, "pending": 82, "reviewedApplied": 766, "scopedInterfaces": 173, "standaloneProcedures": 490}
        assert all(decisions[s]["accepted"] and not decisions[s]["applied"] for s in ACCEPTED)
        assert all(not decisions[s]["accepted"] and not decisions[s]["applied"] for s in UNACCEPTED)
        STAGING.mkdir(parents=True)
        for name in archive.namelist():
            if name.endswith("/") or name == "CASEBOOK.json" or name.startswith(("inputs/", "packet187/", "supplement/")):
                continue
            dest = STAGING / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(archive.read(name))
        with (STAGING / "CASEBOOK.json.gz").open("wb") as gzraw:
            with gzip.GzipFile(fileobj=gzraw, mode="wb", filename="", mtime=0, compresslevel=6) as gz:
                shutil.copyfileobj(archive.open("CASEBOOK.json"), gz, length=1024 * 1024)
        packet_candidate_raw = archive.read("packet187/CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json")
        (STAGING / "INPUT_PACKET").mkdir()
        (STAGING / "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json").write_bytes(packet_candidate_raw)
        (STAGING / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGING / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(INDEPENDENT_AUDIT.read_bytes())

        archive_binding, delivery_binding, audit_binding = bind(RETURN), bind(DELIVERY), bind(INDEPENDENT_AUDIT)
        source_candidate_binding = {"path": (CANDIDATE_REL / "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json").as_posix(), "bytes": len(packet_candidate_raw), "sha256": sha(packet_candidate_raw)}
        casebook_member = next(m for m in delivery["completeArchiveMemberBindings"] if m["path"] == "CASEBOOK.json")
        casebook_source_binding = {"path": "CASEBOOK.json", "bytes": casebook_member["bytes"], "sha256": casebook_member["sha256"]}
        casebook_binding = {"path": (CANDIDATE_REL / "CASEBOOK.json.gz").as_posix(), "bytes": (STAGING / "CASEBOOK.json.gz").stat().st_size, "sha256": sha_file(STAGING / "CASEBOOK.json.gz")}
        package_manifest = {"id": "RANK9-WARDCONTROL6-CANDIDATE-PACKAGE-MANIFEST-188", "sourceArchive": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding, "files": []}
        spells = []
        for pos, sid in enumerate(ACCEPTED):
            src = procedures[sid]
            card = src["nativeCardUnchanged"]
            qids = src["questionIds"]
            proc = {"id": f"WC188-STATIC-PROCEDURE-{sid.upper().replace('-', '_')}", "spellId": sid, "status": "director-accepted static authored procedure; applied to authored review index; runtime remains disabled", "accepted": True, "applied": False, "nativeCardUnchanged": copy.deepcopy(card), "sourceEnvelopePointer": src["sourceEnvelopePointer"], "procedureText": src["procedure"], "procedureSections": copy.deepcopy(src["procedureSections"]), "sharedRules": copy.deepcopy(src["sharedRules"]), "questionIds": copy.deepcopy(qids), "directorDecisionId": decision["id"]}
            spells.append({"id": sid, "name": src["name"], "procedure": proc, "directorProcedureRecord": copy.deepcopy(src), "nativeCardUnchanged": copy.deepcopy(card), "questionDispositions": {q: copy.deepcopy(qmap[q]) for q in qids if q in qmap}, "runtimeSelectionEnabled": False})
        excluded_pending = sorted(live_pending - set(ACCEPTED))
        model = {"schemaVersion": 1, "moduleId": "rank9-wardcontrol6-reviewed-188", "status": "FOUR_EXACT_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_TWO_RETAINED_BLOCKERS", "scope": "Exactly the four director-accepted identities are applied as static authored procedures. Nullification Wave and Reality Anchor remain pending under WC188-B01 and WC188-B02. Native catalog cards and source status remain unchanged; runtime and downstream approval gates remain disabled.", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "excludedPendingIds": excluded_pending, "unacceptedDecisions": [copy.deepcopy(decisions[s]) for s in UNACCEPTED], "sharedRules": {"scope": "No global or shared rule changes; native cards and class routes remain unchanged.", "runtimeSelectionEnabled": False}, "spells": spells, "questionDispositions": questions, "caseCoverage": {"caseCount": delivery["counts"]["cases"], "eventCount": delivery["counts"]["events"], "independentReplay": audit["replay"]}, "returnCounts": delivery["counts"], "blockers": blockers, "sourceArchive": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding, "casebookFile": "CASEBOOK.json.gz", "casebookSourceArchiveMemberBinding": casebook_source_binding, "sourceConferenceCandidate": source_candidate_binding, "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False, "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False, "releaseApproved": False, "domainClosure": False}
        for p in sorted(x for x in STAGING.rglob("*") if x.is_file() and x.name != "MODEL.json"):
            raw = p.read_bytes()
            package_manifest["files"].append({"path": (CANDIDATE_REL / p.relative_to(STAGING)).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
        write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
        model["candidatePackageManifestBinding"] = {"path": (CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json").as_posix(), "bytes": (STAGING / "CANDIDATE_PACKAGE_MANIFEST.json").stat().st_size, "sha256": sha_file(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json")}
        write_json(STAGING / "MODEL.json", model)
        shutil.move(str(STAGING), str(CANDIDATE))

    model_binding = bind(CANDIDATE_REL / "MODEL.json")
    manifest_binding = bind(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json")
    casebook_binding = bind(CANDIDATE_REL / "CASEBOOK.json.gz")
    manuscript_raw = (CANDIDATE / "STANDALONE_PROCEDURES.md").read_bytes()
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_bytes(manuscript_raw)
    manuscript_binding = bind(MANUSCRIPT)
    shutil.copyfile(INDEX, BEFORE_BACKUP)
    assert BEFORE_BACKUP.read_bytes() == before_raw
    decision_record = {"id": decision["id"], "recordedAtUtc": timestamp, "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "blockers": blockers, "directorReturn": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding, "authorityAtDecision": decision["authorityBeforeAndStillCanonical"], "exactDirectorDecisions": decision["decisions"], "scope": "Static authored procedure acceptance only. No runtime, source-access, human-play, balance, cosmology, closure, or release approval.", "canonicalFilesChangedByDirector": False}
    write_json(DECISION_PATH, decision_record)
    acceptance = {"id": REVIEW_ID, "recordedAtUtc": timestamp, "status": "FOUR_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_TWO_RETAINED_BLOCKERS", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "directorDecision": bind(DECISION_PATH), "directorReturn": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding, "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding, "countsBefore": BEFORE, "countsAfter": AFTER, "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE, "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER, "blockers": blockers, "runtimeSelectionEnabled": False, "canonicalApplicationPerformedByDirector": False}
    write_json(ACCEPTANCE_PATH, acceptance)
    receipt = {"id": "RANK9-WARDCONTROL6-DIRECTOR-RETURN-188-RECEIPT", "recordedAtUtc": timestamp, "status": "DIRECTOR_PARTIALLY_ACCEPTED_FOUR_EXACT_IDENTITIES; TWO_REMAIN_BLOCKED; INDEPENDENT_AUDIT_PASSED", "reviewedIds": GROUP, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "blockers": blockers, "directorReturn": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding, "sourceAuthority": decision["authorityBeforeAndStillCanonical"], "counts": delivery["counts"], "decisionId": decision["id"]}
    write_json(RECEIPT_PATH, receipt)
    application = {"id": APP_ID, "recordedAtUtc": timestamp, "status": "APPLIED_FOUR_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS", "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "directorAcceptance": bind(ACCEPTANCE_PATH), "directorDecision": bind(DECISION_PATH), "directorReturnReceipt": bind(RECEIPT_PATH), "directorReturn": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding, "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding, "manuscript": manuscript_binding, "indexBefore": bind(BEFORE_BACKUP, before_raw), "countsBefore": BEFORE, "countsAfter": AFTER, "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER}, "sourceStatusPreservedAsBlocked": True, "catalogChanged": False, "runtimeSelectionEnabled": False}
    write_json(APPLICATION_PATH, application)
    application_binding = bind(APPLICATION_PATH)

    after = copy.deepcopy(before)
    operations = []
    for pos, sid in enumerate(ACCEPTED):
        i = next(i for i, r in enumerate(before["entries"]) if r["id"] == sid)
        old = before["entries"][i]
        new = copy.deepcopy(old)
        new.update({"authoredStatus": "reviewed-authored-operational-playtest", "procedureFile": "../spell_candidates/rank9wardcontrol6_reviewed_188/MODEL.json", "procedurePointer": f"/spells/{pos}/procedure", "wholeCardPointer": f"/spells/{pos}", "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"], "wholeCardIdField": "id", "procedureTextPointer": f"/spells/{pos}/procedure/procedureText", "directorProcedureRecordPointer": f"/spells/{pos}/directorProcedureRecord", "sharedRulesPointer": f"/spells/{pos}/procedure/sharedRules", "manuscript": "../../../docs/spells/candidates/RANK9_WARDCONTROL6_REVIEWED_188.md", "reviewId": APP_ID, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True, "completeEvidenceRoot": CANDIDATE_REL.as_posix(), "completeEnvelopeBinding": model_binding, "casebookBinding": casebook_binding, "casebookEncoding": "Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the bound director archive.", "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"], "sourceArchiveBinding": archive_binding, "candidatePackageManifestBinding": manifest_binding, "procedureSourceBinding": bind(DECISION_PATH), "authoredAcceptanceReceipt": bind(ACCEPTANCE_PATH), "authoredApplicationReceipt": application_binding})
        assert new["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review"
        operations.append({"op": "replace-entry", "identity": sid, "index": i, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][i] = new
    after["additionalStandaloneEnvelopes"].append({"file": "../spell_candidates/rank9wardcontrol6_reviewed_188/MODEL.json", "binding": model_binding, "reviewId": REVIEW_ID, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "excludedPendingIds": excluded_pending, "authority": bind(ACCEPTANCE_PATH), "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(), "sourceArchive": archive_binding, "casebookBinding": casebook_binding, "candidatePackageManifestBinding": manifest_binding, "scope": acceptance["status"], "runtimeSelectionEnabled": False})
    after["authoredCounts"] = {"reviewed": 770, "pending": 78}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 494
    pending_after = {r["id"] for r in after["entries"] if r["authoredStatus"] == "pending-authored-procedure"}
    assert pending_after == live_pending - set(ACCEPTED) and len(pending_after) == 78
    inv = copy.deepcopy(after)
    for op in operations:
        inv["entries"][op["index"]] = copy.deepcopy(op["before"])
    inv["additionalStandaloneEnvelopes"] = inv["additionalStandaloneEnvelopes"][:-1]
    inv["authoredCounts"], inv["representationCounts"] = copy.deepcopy(before["authoredCounts"]), copy.deepcopy(before["representationCounts"])
    assert inv == before
    after_raw = json_bytes(after)
    temp = INDEX.with_suffix(".json.wardcontrol6-188.tmp")
    temp.write_bytes(after_raw)
    temp.replace(INDEX)
    assert CATALOG.read_bytes() == catalog_raw
    write_json(OPERATIONS_PATH, {"id": "RANK9-WARDCONTROL6-INDEX-OPERATIONS-188", "before": bind(BEFORE_BACKUP, before_raw), "after": bind(INDEX, after_raw), "operations": operations, "inverseSemanticExact": True, "onlyIdentityIds": ACCEPTED})

    groups = []
    for old in queue_before["currentPendingGroups"]:
        left = [s for s in old["pendingIds"] if s in pending_after]
        if not left:
            continue
        row = copy.deepcopy(old)
        row["pendingIds"], row["pendingCount"] = left, len(left)
        if row["group"] == "rank9-ward-control6":
            row.update({"status": "PARTIAL_RETURN188_FOUR_ACCEPTED_APPLIED_TWO_SOURCE_EVIDENCE_BLOCKED", "freshPacketRequiredForCurrentAuthority": True, "blockingReturn": {"receipt": RECEIPT_PATH.relative_to(ROOT).as_posix(), "ids": UNACCEPTED, "blockerIds": blockers}})
        if row["group"] == NEXT_GROUP:
            row.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True})
        groups.append(row)
    next_row = next(r for r in groups if r["group"] == NEXT_GROUP)
    pending_doc = {"id": "CURRENT78-PENDING-IDENTITY-AUDIT-188", "recordedAtUtc": timestamp, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX, after_raw), "catalogBinding": bind(CATALOG, catalog_raw), "authoredCounts": after["authoredCounts"], "pendingCount": 78, "pendingIds": sorted(pending_after), "allPendingExistInSourceCatalog": pending_after <= {s["id"] for s in catalog["spells"]}, "acceptedUnapplied": 0, "retainedReturn188Blockers": blockers, "closed335AndCompletedCohortsReopened": False}
    write_json(PENDING_AFTER, pending_doc)
    authority = {"reviewedApplied": 770, "pending": 78, "acceptedUnapplied": 0, "completeStandaloneProcedures": 494, "scopedInterfaces": 173}
    next_request = {"group": NEXT_GROUP, "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS), "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True, "candidate": next_row.get("candidate"), "archive": next_row.get("archive")}
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-188", "recordedAtUtc": timestamp, "currentAuthority": authority, "pendingCount": 78, "currentPendingGroups": groups, "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": 4, "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE_PATH.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()}, "pendingIdentityAudit": {"path": PENDING_AFTER.relative_to(ROOT).as_posix(), "pending": 78, "sha256": sha(PENDING_AFTER.read_bytes())}, "nextGroup": NEXT_GROUP, "next": next_request, "nextPreparedRequest": next_request, "packetStatus": "RANK9_WARDCONTROL6_RETURN188_FOUR_APPLIED_TWO_HELD_770_78_NEXT_AGENCY_CONTROL9", "currentSubmissionBinding": bind(RECEIPT_PATH), "currentReturnBinding": archive_binding, "currentPreparation": audit_binding})
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(handoff_before)
    handoff.update({"id": "CURRENT-HANDOFF-188", "recordedAtUtc": timestamp, "status": "RANK9_WARDCONTROL6_FOUR_APPLIED_TWO_HELD_NEXT_AGENCY_CONTROL9_78_PENDING", "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw), "currentCatalogBinding": bind(CATALOG, catalog_raw), "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.relative_to(ROOT).as_posix(), "pendingCount": 78, "sha256": sha(PENDING_AFTER.read_bytes())}, "appliedThisStep": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": 4, "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(), "directorAcceptance": ACCEPTANCE_PATH.relative_to(ROOT).as_posix(), "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(), "applicationValidation": {"path": VALIDATION_PATH.relative_to(ROOT).as_posix()}}, "unacceptedThisStep": {"ids": UNACCEPTED, "blockers": blockers, "retainedInPendingSet": True}, "nextGroup": NEXT_GROUP, "nextPendingCount": len(NEXT_IDS), "nextPreparedRequest": next_request, "currentQueueBinding": bind(QUEUE_AFTER), "currentReturnBinding": archive_binding, "independentAuditBinding": audit_binding, "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(), "resumePriority": "Prepare a fresh Agency/Control9 packet against current 770/78 authority for the same GPT director, audit the return independently, apply only exact accepted IDs, push, and continue in queue order until pending reaches zero."})
    write_json(HANDOFF_AFTER, handoff)
    checks = [
        {"check": "Independent Return188 audit passed and archive binding matches", "passed": audit["status"] == "PASS" and sha_file(RETURN) == archive_binding["sha256"]},
        {"check": "Exactly four accepted IDs applied and two blockers retained", "passed": [o["identity"] for o in operations] == ACCEPTED and set(UNACCEPTED) <= pending_after},
        {"check": "Authority changed exactly from 766/82/490 to 770/78/494", "passed": after["authoredCounts"] == {"reviewed": 770, "pending": 78} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 494},
        {"check": "Pending set equals prior set minus four accepted identities", "passed": pending_after == live_pending - set(ACCEPTED)},
        {"check": "Index inverse restores exact prior value and catalog is byte-identical", "passed": inv == before and CATALOG.read_bytes() == catalog_raw},
        {"check": "Candidate package manifest binds every staged member", "passed": all((ROOT / x["path"]).is_file() and (ROOT / x["path"]).stat().st_size == x["bytes"] and sha_file(ROOT / x["path"]) == x["sha256"] for x in package_manifest["files"])},
        {"check": "Next queue group is Agency/Control9 with nine exact IDs", "passed": queue_after["nextGroup"] == NEXT_GROUP and next_row["pendingIds"] == NEXT_IDS},
        {"check": "Runtime and downstream approvals remain disabled", "passed": model["runtimeSelectionEnabled"] is False and all(model[k] is False for k in ("runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))},
    ]
    validation = {"id": "RANK9-WARDCONTROL6-APPLICATION-VALIDATION-188", "recordedAtUtc": timestamp, "status": "PASS" if all(c["passed"] for c in checks) else "FAIL", "checksPassed": sum(c["passed"] for c in checks), "checksFailed": sum(not c["passed"] for c in checks), "checks": checks, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "countsBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE_BEFORE}, "countsAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE_AFTER}, "indexBefore": bind(BEFORE_BACKUP, before_raw), "indexAfter": bind(INDEX), "catalog": bind(CATALOG), "application": bind(APPLICATION_PATH), "independentAudit": audit_binding, "pendingIdentityAudit": bind(PENDING_AFTER), "queueAfter": bind(QUEUE_AFTER), "handoffAfter": bind(HANDOFF_AFTER), "nextGroup": NEXT_GROUP, "runtimeSelectionEnabled": False}
    write_json(VALIDATION_PATH, validation)
    assert validation["status"] == "PASS", checks
    snapshot = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_188.md"
    snapshot.write_text(f"# Current ordinary spell-review checkpoint 188\n\nReturn188 passed all {audit['checksPassed']} independent checks, including exact source and archive bindings, 60 bidirectionally replayed cases, and 5,182 reversible events. Exactly {', '.join(f'`{x}`' for x in ACCEPTED)} were applied as static authored procedures. `{UNACCEPTED[0]}` and `{UNACCEPTED[1]}` remain pending under WC188-B01 and WC188-B02. Authority: **770 reviewed / 78 pending / 0 accepted-unapplied**, with 494 complete standalone procedures. The next group is Agency/Control9.\n\nSee [handoff](CURRENT_HANDOFF_188.json), [queue](CURRENT_SPELL_QUEUE_188.json), [pending audit](CURRENT78_PENDING_IDENTITY_AUDIT_188.json), [independent audit](RANK9_WARDCONTROL6_RETURN188_INDEPENDENT_AUDIT.json), and [application validation](RANK9_WARDCONTROL6_APPLICATION_VALIDATION_188.json).\n", encoding="utf-8")
    start = ROOT / "START_HERE.md"
    old = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(f"**Current ordinary spell-review checkpoint [188](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_188.json):** Return188 was independently audited and applied for exactly {', '.join(f'`{x}`' for x in ACCEPTED)}. Authority is **770 reviewed / 78 pending / 0 accepted-unapplied**. Nullification Wave and Reality Anchor remain pending under their two source-evidence blockers. The next group is Rank9 Agency/Control9. See [handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_188.json) and [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT78_PENDING_IDENTITY_AUDIT_188.json).\n\n" + old, encoding="utf-8")
    assert CATALOG.read_bytes() == catalog_raw
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "authority": authority, "nextGroup": NEXT_GROUP, "nextPendingCount": len(NEXT_IDS), "audit": audit["status"], "validation": validation["status"], "indexSha256": sha_file(INDEX)}, indent=2))


if __name__ == "__main__":
    main()
