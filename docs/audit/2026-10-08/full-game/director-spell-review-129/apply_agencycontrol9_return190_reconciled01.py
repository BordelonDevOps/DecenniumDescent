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
RECEIVED = AUDIT / "rank9_agencycontrol9_return190_reconciled01_received"
RETURN = RECEIVED / "DD_Rank9_AgencyControl9_Director_Return190_Reconciled01.zip"
DELIVERY = RECEIVED / "DD_Rank9_AgencyControl9_Director_Return190_Reconciled01_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_INDEPENDENT_AUDIT.json"
ORIGINAL_AUDIT = AUDIT / "RANK9_AGENCYCONTROL9_RETURN190_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_189.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_189.json"
PENDING_BEFORE = AUDIT / "CURRENT78_PENDING_IDENTITY_AUDIT_189.json"
BEFORE_BACKUP = AUDIT / "authored_review_index.before_agencycontrol9_190.json"
CANDIDATE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01")
CANDIDATE = ROOT / CANDIDATE_REL
STAGING = CANDIDATE.with_name(CANDIDATE.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_AGENCYCONTROL9_REVIEWED_190_RECONCILED01.md"

GROUP = [
    "absolute-domination", "command-reality", "dominate-legion", "erase-soul",
    "overwhelming-presence", "perfect-mesmerize", "prophecy-fulfilled",
    "puppetmaster-s-realm", "rewrite-loyalty",
]
ACCEPTED = [
    "command-reality", "dominate-legion", "erase-soul", "overwhelming-presence",
    "perfect-mesmerize", "prophecy-fulfilled", "rewrite-loyalty",
]
UNACCEPTED = ["absolute-domination", "puppetmaster-s-realm"]
BLOCKERS = {
    "absolute-domination": {"blockerIds": ["AG190-B01"], "holdIds": ["AG190-B01"]},
    "puppetmaster-s-realm": {"blockerIds": ["AG190-B02"], "holdIds": ["AG190-B02"]},
}
NEXT_GROUP = "rank9-time-fate6"
NEXT_IDS = ["time-stop", "time-fracture", "foresight-perfect", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
BEFORE = {"reviewed": 770, "pending": 78, "acceptedUnapplied": 0}
AFTER = {"reviewed": 777, "pending": 71, "acceptedUnapplied": 0}
COMPLETE_BEFORE, COMPLETE_AFTER = 494, 501
REVIEW_ID = "RANK9-AGENCYCONTROL9-EXACT-AUTHORED-ACCEPTANCE-190-RECONCILED01"
APP_ID = "RANK9-AGENCYCONTROL9-APPLICATION-190-RECONCILED01"
DECISION_PATH = AUDIT / "RANK9_AGENCYCONTROL9_DIRECTOR_DECISION_190_RECONCILED01.json"
ACCEPTANCE_PATH = AUDIT / "RANK9_AGENCYCONTROL9_EXACT_ACCEPTANCE_190_RECONCILED01.json"
RECEIPT_PATH = AUDIT / "RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_RECEIPT.json"
APPLICATION_PATH = AUDIT / "RANK9_AGENCYCONTROL9_APPLICATION_190_RECONCILED01.json"
OPERATIONS_PATH = AUDIT / "RANK9_AGENCYCONTROL9_INDEX_OPERATIONS_190_RECONCILED01.json"
PENDING_AFTER = AUDIT / "CURRENT71_PENDING_IDENTITY_AUDIT_190.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_190.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_190.json"
VALIDATION_PATH = AUDIT / "RANK9_AGENCYCONTROL9_APPLICATION_VALIDATION_190_RECONCILED01.json"
SNAPSHOT_PATH = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_190.md"


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
    assert not CANDIDATE.exists() and not STAGING.exists(), "Candidate output already exists; inspect before retrying"
    assert all(not path.exists() for path in (
        BEFORE_BACKUP, MANUSCRIPT, DECISION_PATH, ACCEPTANCE_PATH, RECEIPT_PATH,
        APPLICATION_PATH, OPERATIONS_PATH, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER,
        VALIDATION_PATH, SNAPSHOT_PATH,
    )), "An application output already exists; inspect before retrying"
    audit = read_json(INDEPENDENT_AUDIT)
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0
    assert audit["acceptedIds"] == ACCEPTED and audit["unacceptedIds"] == UNACCEPTED and audit["applied"] is False
    assert sha_file(RETURN) == audit["returnArchive"]["sha256"] == "ff33cba4ead2f8dfa1db4b27edb9a8883f757a3af7380ff6d4663c6fa5eb1af6"
    delivery = read_json(DELIVERY)
    assert RETURN.stat().st_size == delivery["archive"]["bytes"] == 79_729_523
    assert sha_file(RETURN) == delivery["archive"]["sha256"]
    assert delivery["counts"]["dataIntegrityChecks"] == 126_337
    assert delivery["decisions"]["acceptedIds"] == ACCEPTED
    assert delivery["decisions"]["unacceptedIds"] == UNACCEPTED
    assert delivery["decisions"]["applied"] is False

    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read_json(INDEX), read_json(CATALOG)
    assert before["authoredCounts"] == {"reviewed": BEFORE["reviewed"], "pending": BEFORE["pending"]}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE_BEFORE
    rows = {r["id"]: r for r in before["entries"]}
    catalog_rows = {r["id"]: r for r in read_json(CATALOG)["spells"]}
    live_pending = {r["id"] for r in before["entries"] if r["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == BEFORE["pending"] and set(GROUP) <= live_pending
    assert all(rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in GROUP)
    assert all(not p.exists() for p in (CANDIDATE, MANUSCRIPT))
    queue_before, handoff_before, pending_before = map(read_json, (QUEUE_BEFORE, HANDOFF_BEFORE, PENDING_BEFORE))
    assert queue_before["currentAuthority"] == handoff_before["currentAuthority"] == {
        "reviewedApplied": 770, "pending": 78, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 494, "scopedInterfaces": 173,
    }
    assert pending_before["pendingCount"] == len(pending_before["pendingIds"]) == 78
    assert set(pending_before["pendingIds"]) == live_pending
    queue_next_ids = next(row["pendingIds"] for row in queue_before["currentPendingGroups"] if row["group"] == NEXT_GROUP)
    assert queue_next_ids == NEXT_IDS

    timestamp = datetime.now(timezone.utc).isoformat()
    with zipfile.ZipFile(RETURN) as archive:
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        procedure_doc = json.loads(archive.read("PROCEDURES.json"))
        procedures = {row["id"]: row for row in procedure_doc["procedures"]}
        decisions = {row["id"]: row for row in decision["perIdentity"]}
        assert set(procedures) == set(decisions) == set(GROUP)
        assert decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == UNACCEPTED
        assert decision["applied"] is False and decision["canonicalFilesEdited"] is False
        assert decision["canonicalAuthorityUnchanged"] == {
            "reviewedApplied": 770, "pending": 78, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 494, "scopedInterfaces": 173,
        }
        assert all(decisions[s]["accepted"] and not decisions[s]["applied"] and not decisions[s]["blockerIds"] for s in ACCEPTED)
        assert all(not decisions[s]["accepted"] and not decisions[s]["applied"] and decisions[s]["blockerIds"] == BLOCKERS[s]["blockerIds"] for s in UNACCEPTED)
        assert all(
            not procedures[s]["applied"]
            and procedures[s]["nativeCardUnchanged"] == catalog_rows[s]
            and procedures[s]["currentIndexEntryUnchanged"] == rows[s]
            for s in GROUP
        )
        assert set(decision["retainedInheritedBlockers"]) == {"WC188-B01", "WC188-B02"}

        source_candidate_raw = archive.read("evidence/packet189/CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json")
        source_candidate = json.loads(source_candidate_raw)
        questions_doc = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        qrows = {q["id"]: q for q in questions_doc["questions"]}
        assert len(qrows) == 34
        STAGING.mkdir(parents=True)
        for name in archive.namelist():
            if name.endswith("/") or name == "CASEBOOK.json" or name.startswith(("evidence/", "MEMBER_MANIFEST.json")):
                continue
            destination = STAGING / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(name))
        with (STAGING / "CASEBOOK.json.gz").open("wb") as gzraw:
            with gzip.GzipFile(fileobj=gzraw, mode="wb", filename="", mtime=0, compresslevel=6) as gz:
                shutil.copyfileobj(archive.open("CASEBOOK.json"), gz, length=1024 * 1024)
        input_packet = archive.read("evidence/input/DD_Rank9_AgencyControl9_CurrentSource_189.zip")
        input_delivery = archive.read("evidence/input/DD_Rank9_AgencyControl9_CurrentSource_189_DELIVERY.json")
        (STAGING / "INPUT_PACKET").mkdir()
        (STAGING / "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json").write_bytes(source_candidate_raw)
        (STAGING / "INPUT_PACKET/DD_Rank9_AgencyControl9_CurrentSource_189_DELIVERY.json").write_bytes(input_delivery)
        (STAGING / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGING / "ORIGINAL_DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes((AUDIT / "rank9_agencycontrol9_return190_received/DD_Rank9_AgencyControl9_Director_Return190_DELIVERY.json").read_bytes())
        (STAGING / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(INDEPENDENT_AUDIT.read_bytes())
        (STAGING / "ORIGINAL_RETURN_AUDIT.json").write_bytes(ORIGINAL_AUDIT.read_bytes())

        archive_binding, delivery_binding, audit_binding = bind(RETURN), bind(DELIVERY), bind(INDEPENDENT_AUDIT)
        source_candidate_binding = {
            "path": (CANDIDATE_REL / "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json").as_posix(),
            "bytes": len(source_candidate_raw), "sha256": sha(source_candidate_raw),
        }
        casebook_member = next(row for row in delivery["completeMemberAllowlist"] if row["path"] == "CASEBOOK.json")
        casebook_source_binding = {"path": "CASEBOOK.json", "bytes": casebook_member["bytes"], "sha256": casebook_member["sha256"]}
        casebook_binding = {
            "path": (CANDIDATE_REL / "CASEBOOK.json.gz").as_posix(),
            "bytes": (STAGING / "CASEBOOK.json.gz").stat().st_size,
            "sha256": sha_file(STAGING / "CASEBOOK.json.gz"),
        }
        package_manifest = {
            "id": "RANK9-AGENCYCONTROL9-CANDIDATE-PACKAGE-MANIFEST-190-RECONCILED01",
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "originalReturnAudit": bind(ORIGINAL_AUDIT),
            "files": [],
        }
        spells = []
        for pos, sid in enumerate(ACCEPTED):
            source = procedures[sid]
            record = {
                "id": f"AG190-STATIC-PROCEDURE-{sid.upper().replace('-', '_')}",
                "spellId": sid,
                "status": "director-accepted static authored procedure; applied to authored review index; runtime remains disabled",
                "accepted": True,
                "applied": False,
                "nativeCardUnchanged": copy.deepcopy(source["nativeCardUnchanged"]),
                "procedureContent": copy.deepcopy(source["procedure"]),
                "sharedRules": copy.deepcopy(source["sharedRulesFull"]),
                "questionDispositions": copy.deepcopy(source["questionDispositions"]),
                "holdIds": copy.deepcopy(source["holdIds"]),
                "caseIds": copy.deepcopy(source["caseIds"]),
                "directorDecisionId": decision["id"],
            }
            spells.append({
                "id": sid,
                "name": rows[sid]["name"],
                "procedure": record,
                "directorProcedureRecord": copy.deepcopy(source),
                "nativeCardUnchanged": copy.deepcopy(source["nativeCardUnchanged"]),
                "questionDispositions": {q["id"]: copy.deepcopy(q) for q in source["questionDispositions"] if q["id"] in qrows},
                "runtimeSelectionEnabled": False,
            })
        unaccepted_decisions = [copy.deepcopy(decisions[s]) for s in UNACCEPTED]
        unaccepted_holds = {
            sid: {
                "blockerIds": copy.deepcopy(decisions[sid]["blockerIds"]),
                "holdIds": copy.deepcopy(procedures[sid]["holdIds"]),
                "reason": decisions[sid]["reason"],
            }
            for sid in UNACCEPTED
        }
        excluded_pending = sorted(live_pending - set(ACCEPTED))
        casebook = json.loads(archive.read("CASEBOOK.json"))
        model = {
            "schemaVersion": 1,
            "moduleId": "rank9-agencycontrol9-reviewed-190-reconciled01",
            "status": "SEVEN_EXACT_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_TWO_RETAINED_BLOCKERS",
            "scope": "Exactly the seven director-accepted identities are applied as static authored procedures. Absolute Domination and Puppetmaster's Realm remain pending under AG190-B01 and AG190-B02. Native catalog cards and class routes remain unchanged; runtime and downstream approval gates stay disabled.",
            "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED,
            "excludedPendingIds": excluded_pending,
            "unacceptedDecisions": unaccepted_decisions,
            "unacceptedHolds": unaccepted_holds,
            "sharedRules": {"scope": "No global or shared rule changes; native cards and class routes remain unchanged.", "runtimeSelectionEnabled": False},
            "spells": spells,
            "questionDispositions": questions_doc,
            "caseCoverage": {
                "caseCount": delivery["counts"]["cases"],
                "acceptedCaseCount": sum(len(procedures[s]["caseIds"]) for s in ACCEPTED),
                "eventCount": delivery["counts"]["events"],
                "independentReplay": audit["replay"],
            },
            "returnCounts": delivery["counts"],
            "blockers": unaccepted_holds,
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "originalAudit": bind(ORIGINAL_AUDIT),
            "casebookFile": "CASEBOOK.json.gz",
            "casebookSourceArchiveMemberBinding": casebook_source_binding,
            "sourceConferenceCandidate": source_candidate_binding,
            "sourcePacketSHA256": sha(input_packet),
            "runtimeSelectionEnabled": False,
            "runtimeTestsExecuted": False,
            "sourceProgramsExecuted": False,
            "implementationApproved": False,
            "humanPlaytested": False,
            "balanceApproved": False,
            "cosmologyModified": False,
            "releaseApproved": False,
            "domainClosure": False,
        }
        for file in sorted(path for path in STAGING.rglob("*") if path.is_file() and path.name != "MODEL.json"):
            raw = file.read_bytes()
            package_manifest["files"].append({
                "path": (CANDIDATE_REL / file.relative_to(STAGING)).as_posix(),
                "bytes": len(raw), "sha256": sha(raw),
            })
        write_json(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
        model["candidatePackageManifestBinding"] = bind(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json", (STAGING / "CANDIDATE_PACKAGE_MANIFEST.json").read_bytes())
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

    blockers = copy.deepcopy(unaccepted_holds)
    decision_record = {
        "id": decision["id"], "recordedAtUtc": timestamp,
        "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE",
        "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "blockers": blockers,
        "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding, "authorityAtDecision": decision["canonicalAuthorityUnchanged"],
        "exactDirectorDecisions": decision["perIdentity"],
        "scope": "Static authored procedure acceptance only. No runtime, implementation, source-access, human-play, balance, cosmology, closure, or release approval.",
        "canonicalFilesChangedByDirector": False,
    }
    write_json(DECISION_PATH, decision_record)
    acceptance = {
        "id": REVIEW_ID, "recordedAtUtc": timestamp,
        "status": "SEVEN_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_TWO_RETAINED_BLOCKERS",
        "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
        "directorDecision": bind(DECISION_PATH), "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding,
        "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProceduresBefore": COMPLETE_BEFORE,
        "completeReviewedStandaloneProceduresAfter": COMPLETE_AFTER,
        "blockers": blockers, "runtimeSelectionEnabled": False,
        "canonicalApplicationPerformedByDirector": False,
    }
    write_json(ACCEPTANCE_PATH, acceptance)
    receipt = {
        "id": "RANK9-AGENCYCONTROL9-DIRECTOR-RETURN-190-RECONCILED01-RECEIPT",
        "recordedAtUtc": timestamp,
        "status": "DIRECTOR_PARTIALLY_ACCEPTED_SEVEN_EXACT_IDENTITIES; TWO_REMAIN_BLOCKED; INDEPENDENT_AUDIT_PASSED",
        "reviewedIds": GROUP, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
        "blockers": blockers, "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "sourceAuthority": decision["canonicalAuthorityUnchanged"],
        "counts": delivery["counts"], "decisionId": decision["id"],
    }
    write_json(RECEIPT_PATH, receipt)
    application = {
        "id": APP_ID, "recordedAtUtc": timestamp,
        "status": "APPLIED_SEVEN_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS",
        "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.",
        "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
        "directorAcceptance": bind(ACCEPTANCE_PATH), "directorDecision": bind(DECISION_PATH),
        "directorReturnReceipt": bind(RECEIPT_PATH), "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding,
        "manuscript": manuscript_binding, "indexBefore": bind(BEFORE_BACKUP, before_raw),
        "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": COMPLETE_BEFORE, "after": COMPLETE_AFTER},
        "sourceStatusPreservedAsBlocked": True, "catalogChanged": False,
        "runtimeSelectionEnabled": False,
    }
    write_json(APPLICATION_PATH, application)
    application_binding = bind(APPLICATION_PATH)

    after = copy.deepcopy(before)
    operations = []
    for pos, sid in enumerate(ACCEPTED):
        index = next(i for i, row in enumerate(before["entries"]) if row["id"] == sid)
        old = before["entries"][index]
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01/MODEL.json",
            "procedurePointer": f"/spells/{pos}/procedure",
            "wholeCardPointer": f"/spells/{pos}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{pos}/procedure/procedureContent",
            "directorProcedureRecordPointer": f"/spells/{pos}/directorProcedureRecord",
            "sharedRulesPointer": f"/spells/{pos}/procedure/sharedRules",
            "manuscript": "../../../docs/spells/candidates/RANK9_AGENCYCONTROL9_REVIEWED_190_RECONCILED01.md",
            "reviewId": APP_ID,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": CANDIDATE_REL.as_posix(),
            "completeEnvelopeBinding": model_binding,
            "casebookBinding": casebook_binding,
            "casebookEncoding": "Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the bound reconciled director archive.",
            "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
            "sourceArchiveBinding": archive_binding,
            "candidatePackageManifestBinding": manifest_binding,
            "procedureSourceBinding": bind(DECISION_PATH),
            "authoredAcceptanceReceipt": bind(ACCEPTANCE_PATH),
            "authoredApplicationReceipt": application_binding,
        })
        assert new["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review"
        operations.append({"op": "replace-entry", "identity": sid, "index": index, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][index] = new
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01/MODEL.json",
        "binding": model_binding, "reviewId": REVIEW_ID, "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED, "excludedPendingIds": excluded_pending,
        "authority": bind(ACCEPTANCE_PATH), "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(),
        "sourceArchive": archive_binding, "casebookBinding": casebook_binding,
        "candidatePackageManifestBinding": manifest_binding, "scope": acceptance["status"],
        "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = {"reviewed": AFTER["reviewed"], "pending": AFTER["pending"]}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE_AFTER
    pending_after = {r["id"] for r in after["entries"] if r["authoredStatus"] == "pending-authored-procedure"}
    assert pending_after == live_pending - set(ACCEPTED) and len(pending_after) == AFTER["pending"]
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_raw = json_bytes(after)
    temp = INDEX.with_suffix(".json.agencycontrol9-190.tmp")
    temp.write_bytes(after_raw)
    temp.replace(INDEX)
    assert CATALOG.read_bytes() == catalog_raw
    write_json(OPERATIONS_PATH, {
        "id": "RANK9-AGENCYCONTROL9-INDEX-OPERATIONS-190-RECONCILED01",
        "before": bind(BEFORE_BACKUP, before_raw), "after": bind(INDEX, after_raw),
        "operations": operations, "inverseSemanticExact": True, "onlyIdentityIds": ACCEPTED,
    })

    groups = []
    for old_group in queue_before["currentPendingGroups"]:
        left = [sid for sid in old_group["pendingIds"] if sid in pending_after]
        if not left:
            continue
        row = copy.deepcopy(old_group)
        row["pendingIds"], row["pendingCount"] = left, len(left)
        if row["group"] == "rank9-agency-control9":
            row.update({
                "status": "PARTIAL_RETURN190_SEVEN_ACCEPTED_APPLIED_TWO_SOURCE_EVIDENCE_BLOCKED",
                "freshPacketRequiredForCurrentAuthority": True,
                "blockingReturn": {"receipt": RECEIPT_PATH.relative_to(ROOT).as_posix(), "ids": UNACCEPTED, "blockers": blockers},
            })
        if row["group"] == NEXT_GROUP:
            row.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True})
        groups.append(row)
    next_row = next(row for row in groups if row["group"] == NEXT_GROUP)
    pending_doc = {
        "id": "CURRENT71-PENDING-IDENTITY-AUDIT-190", "recordedAtUtc": timestamp,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX, after_raw),
        "catalogBinding": bind(CATALOG, catalog_raw), "authoredCounts": after["authoredCounts"],
        "pendingCount": AFTER["pending"], "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": pending_after <= {s["id"] for s in catalog["spells"]},
        "acceptedUnapplied": 0, "retainedReturn188Blockers": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]},
        "retainedReturn190Blockers": blockers, "closed335AndCompletedCohortsReopened": False,
    }
    write_json(PENDING_AFTER, pending_doc)
    authority = {
        "reviewedApplied": AFTER["reviewed"], "pending": AFTER["pending"], "acceptedUnapplied": 0,
        "completeStandaloneProcedures": COMPLETE_AFTER, "scopedInterfaces": 173,
    }
    next_request = {
        "group": NEXT_GROUP, "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS),
        "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True,
        "candidate": next_row.get("candidate"), "archive": next_row.get("archive"),
    }
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-190", "recordedAtUtc": timestamp, "currentAuthority": authority,
        "pendingCount": AFTER["pending"], "currentPendingGroups": groups,
        "justAppliedBatch": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": len(ACCEPTED),
            "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(),
            "directorAcceptance": ACCEPTANCE_PATH.relative_to(ROOT).as_posix(),
            "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": PENDING_AFTER.relative_to(ROOT).as_posix(), "pending": AFTER["pending"], "sha256": sha(PENDING_AFTER.read_bytes())},
        "nextGroup": NEXT_GROUP, "next": next_request, "nextPreparedRequest": next_request,
        "packetStatus": "RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_SEVEN_APPLIED_TWO_HELD_777_71_NEXT_TIME_FATE6",
        "currentSubmissionBinding": bind(RECEIPT_PATH), "currentReturnBinding": archive_binding,
        "currentPreparation": audit_binding,
    })
    write_json(QUEUE_AFTER, queue_after)
    handoff = copy.deepcopy(handoff_before)
    handoff.update({
        "id": "CURRENT-HANDOFF-190", "recordedAtUtc": timestamp,
        "status": "RANK9_AGENCYCONTROL9_SEVEN_APPLIED_TWO_HELD_NEXT_TIME_FATE6_71_PENDING",
        "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw),
        "currentCatalogBinding": bind(CATALOG, catalog_raw),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": PENDING_AFTER.relative_to(ROOT).as_posix(), "pendingCount": AFTER["pending"], "sha256": sha(PENDING_AFTER.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW_ID, "ids": ACCEPTED, "count": len(ACCEPTED),
            "applicationReceipt": APPLICATION_PATH.relative_to(ROOT).as_posix(),
            "directorAcceptance": ACCEPTANCE_PATH.relative_to(ROOT).as_posix(),
            "independentAudit": INDEPENDENT_AUDIT.relative_to(ROOT).as_posix(),
            "applicationValidation": {"path": VALIDATION_PATH.relative_to(ROOT).as_posix()}},
        "unacceptedThisStep": {"ids": UNACCEPTED, "blockers": blockers, "retainedInPendingSet": True},
        "nextGroup": NEXT_GROUP, "nextPendingCount": len(NEXT_IDS), "nextPreparedRequest": next_request,
        "currentQueueBinding": bind(QUEUE_AFTER), "currentReturnBinding": archive_binding,
        "independentAuditBinding": audit_binding, "parentHandoff": HANDOFF_BEFORE.relative_to(ROOT).as_posix(),
        "resumePriority": "Prepare a fresh Time/Fate6 packet against current 777/71 authority for the same GPT director, independently audit the return, apply only exact accepted IDs, push, and continue in queue order until pending reaches zero.",
    })
    write_json(HANDOFF_AFTER, handoff)
    checks = [
        {"check": "Reconciled Return190 independent audit passed with matching archive binding", "passed": audit["status"] == "PASS" and sha_file(RETURN) == archive_binding["sha256"]},
        {"check": "Exactly seven accepted IDs applied and two blockers retained", "passed": [op["identity"] for op in operations] == ACCEPTED and set(UNACCEPTED) <= pending_after},
        {"check": "Authority changed exactly from 770/78/494 to 777/71/501", "passed": after["authoredCounts"] == {"reviewed": 777, "pending": 71} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 501},
        {"check": "Pending set equals prior set minus the seven accepted identities", "passed": pending_after == live_pending - set(ACCEPTED)},
        {"check": "Index inverse restores exact prior value and catalog remains byte-identical", "passed": inverse == before and CATALOG.read_bytes() == catalog_raw},
        {"check": "Candidate package manifest binds every staged member", "passed": all((ROOT / row["path"]).is_file() and (ROOT / row["path"]).stat().st_size == row["bytes"] and sha_file(ROOT / row["path"]) == row["sha256"] for row in package_manifest["files"])},
        {"check": "Next queue group is Time/Fate6 with six exact IDs", "passed": queue_after["nextGroup"] == NEXT_GROUP and next_row["pendingIds"] == NEXT_IDS},
        {"check": "Runtime and downstream approvals remain disabled", "passed": model["runtimeSelectionEnabled"] is False and all(model[key] is False for key in ("runtimeTestsExecuted", "sourceProgramsExecuted", "implementationApproved", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))},
    ]
    validation = {
        "id": "RANK9-AGENCYCONTROL9-APPLICATION-VALIDATION-190-RECONCILED01",
        "recordedAtUtc": timestamp, "status": "PASS" if all(row["passed"] for row in checks) else "FAIL",
        "checksPassed": sum(row["passed"] for row in checks), "checksFailed": sum(not row["passed"] for row in checks),
        "checks": checks, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
        "countsBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE_BEFORE},
        "countsAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE_AFTER},
        "indexBefore": bind(BEFORE_BACKUP, before_raw), "indexAfter": bind(INDEX),
        "catalog": bind(CATALOG), "application": bind(APPLICATION_PATH),
        "independentAudit": audit_binding, "pendingIdentityAudit": bind(PENDING_AFTER),
        "queueAfter": bind(QUEUE_AFTER), "handoffAfter": bind(HANDOFF_AFTER),
        "nextGroup": NEXT_GROUP, "runtimeSelectionEnabled": False,
    }
    write_json(VALIDATION_PATH, validation)
    assert validation["status"] == "PASS", checks
    SNAPSHOT_PATH.write_text(
        f"# Current ordinary spell-review checkpoint 190\n\nReturn190 Reconciled01 passed all {audit['checksPassed']} independent checks, including 72 replayed cases and 1,919 reversible events. Exactly {', '.join(f'`{sid}`' for sid in ACCEPTED)} were applied as static authored procedures. `absolute-domination` and `puppetmaster-s-realm` remain pending under AG190-B01 and AG190-B02. Authority: **777 reviewed / 71 pending / 0 accepted-unapplied**, with 501 complete standalone procedures. The next group is Time/Fate6.\n\nSee [handoff](CURRENT_HANDOFF_190.json), [queue](CURRENT_SPELL_QUEUE_190.json), [pending audit](CURRENT71_PENDING_IDENTITY_AUDIT_190.json), [independent audit](RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_INDEPENDENT_AUDIT.json), and [application validation](RANK9_AGENCYCONTROL9_APPLICATION_VALIDATION_190_RECONCILED01.json).\n",
        encoding="utf-8", newline="\n",
    )
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(
        f"**Current ordinary spell-review checkpoint [190](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_190.json):** Return190 Reconciled01 was independently audited and applied for exactly {', '.join(f'`{sid}`' for sid in ACCEPTED)}. Authority is **777 reviewed / 71 pending / 0 accepted-unapplied**. Absolute Domination and Puppetmaster's Realm remain pending under AG190-B01 and AG190-B02. The next group is Rank9 Time/Fate6. See [handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_190.json) and [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT71_PENDING_IDENTITY_AUDIT_190.json).\n\n" + old_start,
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_raw
    print(json.dumps({
        "status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
        "authority": authority, "nextGroup": NEXT_GROUP, "nextPendingCount": len(NEXT_IDS),
        "audit": audit["status"], "validation": validation["status"], "indexSha256": sha_file(INDEX),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
