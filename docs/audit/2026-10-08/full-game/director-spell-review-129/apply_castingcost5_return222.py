from __future__ import annotations

import copy
import gzip
import hashlib
import json
import shutil
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN = BASE / "rank9_castingcost5_return222_received"
ARCHIVE = RETURN / "DD_Rank9_CastingCost2_Director_Return222.zip"
DELIVERY = RETURN / "DD_Rank9_CastingCost2_Director_Return222_DELIVERY.json"
SOURCE_DELIVERY = BASE / "rank9_castingcost5_current_source_222_prepared_retry1/DD_Rank9_CastingCost5_CurrentSource_222_DELIVERY.json"
AUDIT = BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json"
INDEPENDENT_RECEIPT = BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_RECEIPT.json"
RECEIPT = BASE / "RANK9_CASTINGCOST5_RETURN222_RECEIPT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE0 = BASE / "CURRENT_SPELL_QUEUE_222.json"
HANDOFF0 = BASE / "CURRENT_HANDOFF_222.json"
PENDING0 = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_222.json"
BACKUP = BASE / "authored_review_index.before_castingcost5_222.json"
PKG_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_222_final")
PKG = ROOT / PKG_REL
STAGE = PKG.with_name(PKG.name + ".staging")
MAN = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_CASTINGCOST5_REVIEWED_222.md"
DECISION = BASE / "RANK9_CASTINGCOST5_DIRECTOR_DECISION_222.json"
ACCEPTANCE = BASE / "RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_222.json"
APPLICATION = BASE / "RANK9_CASTINGCOST5_APPLICATION_222.json"
OPS = BASE / "RANK9_CASTINGCOST5_INDEX_OPERATIONS_222.json"
VALIDATION = BASE / "RANK9_CASTINGCOST5_APPLICATION_VALIDATION_222.json"
PENDING1 = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_223.json"
QUEUE1 = BASE / "CURRENT_SPELL_QUEUE_223.json"
HANDOFF1 = BASE / "CURRENT_HANDOFF_223.json"
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_223.md"
NEXT = "rank9-memory-denial6"
NEXT_IDS = ["mind-collapse", "unravel-identity"]
AUTH0 = {"reviewedApplied": 810, "pending": 38, "acceptedUnapplied": 0,
         "completeStandaloneProcedures": 534, "scopedInterfaces": 173}
AUTH1 = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
         "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
ACCEPTED = ["perfect-spell"]
HELD = ["unholy-ascendance"]
SCOPE = ACCEPTED + HELD
REVIEW = "RANK9-CASTINGCOST5-EXACT-AUTHORED-ACCEPTANCE-222"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: Path, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def writej(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(jb(value))


def main():
    output_files = [BACKUP, MAN, DECISION, ACCEPTANCE, APPLICATION, OPS, VALIDATION, PENDING1, QUEUE1, HANDOFF1, SNAPSHOT]
    assert all(path.exists() is False for path in output_files), "Refusing to overwrite an application artifact."
    assert PKG.exists() is False and STAGE.exists() is False, "Refusing to overwrite a candidate package."
    for path in [ARCHIVE, DELIVERY, AUDIT, INDEPENDENT_RECEIPT, INDEX, CATALOG, QUEUE0, HANDOFF0, PENDING0]:
        assert path.is_file(), f"Required application input missing: {path}"

    audit, receipt, delivery = readj(AUDIT), readj(INDEPENDENT_RECEIPT), readj(DELIVERY)
    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = readj(INDEX), readj(CATALOG)
    q0, h0, p0 = readj(QUEUE0), readj(HANDOFF0), readj(PENDING0)
    archive_raw = ARCHIVE.read_bytes()
    assert audit["status"] == "PASS" and audit["checksFailed"] == 0 and audit["applied"] is False
    assert receipt["acceptedIds"] == ACCEPTED and receipt["appliedIds"] == [] and receipt["heldIds"] == HELD
    assert delivery["acceptedIds"] == ACCEPTED and delivery["heldIds"] == HELD and delivery["applied"] is False
    assert delivery["archive"]["bytes"] == len(archive_raw) and delivery["archive"]["sha256"] == sha(archive_raw)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTH0
    assert before["authoredCounts"] == {"reviewed": 810, "pending": 38}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 534
    assert p0["pendingCount"] == 38 and set(SCOPE) <= set(p0["pendingIds"])

    rows = {x["id"]: x for x in before["entries"]}
    catalog_rows = {x["id"]: x for x in catalog["spells"]}
    pending_before = {x["id"] for x in before["entries"] if x["authoredStatus"] == "pending-authored-procedure"}
    assert len(pending_before) == 38 and pending_before == set(p0["pendingIds"])
    assert rows["perfect-spell"]["authoredStatus"] == "pending-authored-procedure"
    assert rows["perfect-spell"]["sourceStatus"] == "blocked-pending-operational-review"
    assert catalog_rows["perfect-spell"].get("operational") is None
    assert set(NEXT_IDS) <= pending_before

    with zipfile.ZipFile(ARCHIVE) as zf:
        assert zf.testzip() is None
        director = json.loads(zf.read("DIRECTOR_DECISION.json"))
        hold_register = json.loads(zf.read("HOLD_REGISTER.json"))
        focused = json.loads(zf.read("FOCUSED_CASES.json"))
        trace = json.loads(zf.read("TRACE_INDEX.json"))
        procedures = {sid: json.loads(zf.read(f"procedures/{sid}.json")) for sid in SCOPE}
        decs = {d["id"]: d for d in director["decisions"]}
        assert director["scope"] == SCOPE and director["acceptedIds"] == ACCEPTED and director["heldIds"] == HELD
        assert director["applied"] is False and decs["perfect-spell"]["accepted"] is True and decs["perfect-spell"]["applied"] is False
        assert decs["perfect-spell"]["resolvedBlockerIds"] == ["CC194-B01"]
        assert decs["unholy-ascendance"]["blockerIds"] == ["CC194-B04"]
        proc = procedures["perfect-spell"]
        assert proc["accepted"] is True and proc["applied"] is False and proc["resolvedBlockerIds"] == ["CC194-B01"]
        assert proc["completeSourceAndAccess"] == catalog_rows["perfect-spell"]
        assert audit["replay"]["cases"] == 34 and audit["replay"]["events"] == 522
        trace_rows = [x for x in trace["cases"] if x["spellId"] == "perfect-spell"]
        case_ids = [x["caseId"] for x in trace_rows]
        case_events = sum(x["events"] for x in trace_rows)
        assert set(case_ids) == set(proc["caseIds"])
        accepted_cases = len(case_ids)
        focused_ids = {x["id"] for x in focused["cases"]}
        assert {"CC222-PS-funded-X2", "CC222-PS-funded-PB6", "CC222-PS-zero-credit-rejected",
                "CC222-PS-over-cap-rejected", "CC222-PS-insufficient-RP-rejected", "CC222-PS-equal-offer-retained",
                "CC222-PS-weaker-offer-retained", "CC222-PS-stronger-offer-replaces", "CC222-PS-countered-paid-X"} <= focused_ids
        blocker_records = hold_register["currentBlockers"]
        held_record = next(x for x in blocker_records if x["id"] == "CC194-B04")
        assert held_record["blockingForIds"] == HELD
        assert all(v is False for v in (director["applied"], proc["applied"], procedures["unholy-ascendance"]["applied"]))

        # Preserve the exact return evidence and procedures in the candidate envelope.
        STAGE.mkdir(parents=True)
        keep = ["DIRECTOR_DECISION.json", "HOLD_REGISTER.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
                "COUNTS.json", "SOURCE_BINDING.json", "SOURCE_VERIFICATION.json", "TRACE_INDEX.json", "VALIDATION.json"]
        for name in keep:
            (STAGE / name).write_bytes(zf.read(name))
        (STAGE / "procedures/perfect-spell.json").parent.mkdir(parents=True, exist_ok=True)
        for sid in SCOPE:
            (STAGE / f"procedures/{sid}.json").write_bytes(zf.read(f"procedures/{sid}.json"))
        (STAGE / "PRESERVED_CASEBOOK.json.gz").write_bytes(zf.read("PRESERVED_CASEBOOK.json.gz"))
        focused_raw = zf.read("FOCUSED_CASES.json")
        with (STAGE / "FOCUSED_CASES.json.gz").open("wb") as out:
            with gzip.GzipFile(fileobj=out, mode="wb", filename="", mtime=0, compresslevel=6) as gz:
                gz.write(focused_raw)
        standalone = zf.read("STANDALONE_PROCEDURES.md").decode("utf-8-sig")
        # The director's archive filename/title says Cost2, while its source binding,
        # request, and identity scope all say Casting/Cost5. Correct only this title typo.
        standalone = standalone.replace("# Director Return222 � Casting/Cost2", "# Director Return222 — Casting/Cost5", 1)
        (STAGE / "STANDALONE_PROCEDURES.md").write_text(standalone, encoding="utf-8", newline="\n")

    timestamp = datetime.now(timezone.utc).isoformat()
    archive_binding, delivery_binding = bind(ARCHIVE, archive_raw), bind(DELIVERY)
    audit_binding, receipt_binding = bind(AUDIT), bind(INDEPENDENT_RECEIPT)
    source_packet_binding = {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_castingcost5_current_source_222_prepared_retry1/DD_Rank9_CastingCost5_CurrentSource_222.zip",
                             "bytes": delivery["sourcePacket"]["bytes"], "sha256": delivery["sourcePacket"]["sha256"]}
    procedure_record = procedures["perfect-spell"]
    director_row = next(d for d in director["decisions"] if d["id"] == "perfect-spell")
    spells = [{"id": "perfect-spell", "name": rows["perfect-spell"]["name"], "position": 0,
               "procedure": {"id": "CC222-STATIC-PERFECT-SPELL", "spellId": "perfect-spell",
                             "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                             "accepted": True, "applied": False,
                             "nativeCardUnchanged": copy.deepcopy(procedure_record["completeSourceAndAccess"]),
                             "procedureContent": copy.deepcopy(procedure_record["procedure"]),
                             "sharedRequirements": procedure_record["commonProcedure"],
                             "newChoices": copy.deepcopy(procedure_record["newChoices"]),
                             "qualifications": copy.deepcopy(procedure_record["qualifications"]),
                             "caseIds": copy.deepcopy(procedure_record["caseIds"]),
                             "questionIds": copy.deepcopy(procedure_record["questionIds"]),
                             "holdIds": copy.deepcopy(director_row["conditionalQualificationIds"]),
                             "resolvedBlockerIds": copy.deepcopy(director_row["resolvedBlockerIds"]),
                             "directorDecisionId": director["id"]},
               "directorProcedureRecord": copy.deepcopy(procedure_record),
               "nativeCardUnchanged": copy.deepcopy(procedure_record["completeSourceAndAccess"]),
               "caseIds": copy.deepcopy(procedure_record["caseIds"]),
               "questionIds": copy.deepcopy(procedure_record["questionIds"]),
               "holdIds": copy.deepcopy(director_row["conditionalQualificationIds"]),
               "runtimeSelectionEnabled": False}]
    unaccepted = {"unholy-ascendance": {"blockerIds": ["CC194-B04"],
                 "holdIds": copy.deepcopy(decs["unholy-ascendance"]["conditionalQualificationIds"]),
                 "blockerRecords": [copy.deepcopy(held_record)]}}
    model = {"schemaVersion": 1, "moduleId": "rank9-castingcost5-reviewed-222",
             "status": "ONE_EXACT_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_WITH_ONE_BLOCKER",
             "scope": "Only Perfect Spell's exact static authored procedure is accepted and applied to the review index. Unholy Ascendance remains pending under CC194-B04. Native cards, class routes and source catalog remain unchanged; runtime and downstream approvals remain disabled.",
             "acceptedIds": ACCEPTED, "unacceptedIds": HELD,
             "excludedPendingIds": sorted(pending_before - set(ACCEPTED)), "unacceptedHolds": unaccepted,
             "inheritedNamedBlockerIds": ["AG190-B01", "AG190-B02", "TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"],
             "sharedRequirements": {"scope": "No global/shared rule changes; native cards and class routes unchanged.", "runtimeSelectionEnabled": False},
             "spells": spells,
             "caseCoverage": {"caseCount": len(case_ids), "caseIds": case_ids, "eventCount": case_events,
                              "allCaseReplay": audit["replay"], "newFocusedCaseIds": sorted(focused_ids)},
             "returnCounts": delivery["counts"], "sourceArchive": archive_binding,
             "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
             "directorReceipt": receipt_binding, "sourceConferencePacket": source_packet_binding,
             "casebookFile": "PRESERVED_CASEBOOK.json.gz",
             "casebookSourceArchiveMemberBinding": next(r for r in delivery["members"] if r["path"] == "PRESERVED_CASEBOOK.json.gz"),
             "casebookBinding": bind(STAGE / "PRESERVED_CASEBOOK.json.gz"),
             "focusedCaseFile": "FOCUSED_CASES.json.gz",
             "focusedCasesBinding": bind(STAGE / "FOCUSED_CASES.json.gz"),
             "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "sourceProgramsExecuted": False,
             "implementationApproved": False, "humanPlaytested": False, "balanceApproved": False,
             "cosmologyModified": False, "releaseApproved": False, "domainClosure": False}
    model_path = STAGE / "MODEL.json"
    model_path.write_bytes(jb(model))
    model_binding_staged = bind(model_path)
    package_manifest = {"id": "RANK9-CASTINGCOST5-PACKAGE-MANIFEST-222", "sourceArchive": archive_binding,
                        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
                        "sourceAnchorCommit": "197366eae0c786415de55a0e4739e83f49f1a65f", "files": []}
    for path in sorted(p for p in STAGE.rglob("*") if p.is_file() and p.name != "CANDIDATE_PACKAGE_MANIFEST.json"):
        raw = path.read_bytes()
        package_manifest["files"].append({"path": (PKG_REL / path.relative_to(STAGE)).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    package_manifest_path = STAGE / "CANDIDATE_PACKAGE_MANIFEST.json"
    package_manifest_path.write_bytes(jb(package_manifest))
    package_manifest_binding_staged = bind(package_manifest_path)
    shutil.move(str(STAGE), str(PKG))
    model_binding = bind(PKG / "MODEL.json")
    package_manifest_binding = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
    casebook_binding = bind(PKG / "PRESERVED_CASEBOOK.json.gz")
    focused_binding = bind(PKG / "FOCUSED_CASES.json.gz")
    assert model_binding["bytes"] == model_binding_staged["bytes"] and model_binding["sha256"] == model_binding_staged["sha256"]
    assert package_manifest_binding["bytes"] == package_manifest_binding_staged["bytes"] and package_manifest_binding["sha256"] == package_manifest_binding_staged["sha256"]
    assert all((ROOT / item["path"]).is_file() and (ROOT / item["path"]).stat().st_size == item["bytes"] and sha((ROOT / item["path"]).read_bytes()) == item["sha256"] for item in package_manifest["files"])

    # Publish the written decision, exact acceptance, receipt and application provenance.
    MAN.parent.mkdir(parents=True, exist_ok=True)
    MAN.write_text((PKG / "STANDALONE_PROCEDURES.md").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    manuscript_binding = bind(MAN)
    shutil.copyfile(INDEX, BACKUP)
    assert BACKUP.read_bytes() == index_raw
    writej(DECISION, {"id": director["id"], "recordedAtUtc": timestamp, "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE",
                      "acceptedIds": ACCEPTED, "heldIds": HELD, "blockers": unaccepted,
                      "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
                      "independentAudit": audit_binding, "directorReceipt": receipt_binding,
                      "authorityAtDecision": AUTH0, "exactDirectorDecisions": director["decisions"],
                      "scope": model["scope"], "canonicalFilesChangedByDirector": False})
    decision_binding = bind(DECISION)
    writej(ACCEPTANCE, {"id": REVIEW, "recordedAtUtc": timestamp,
                        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_WITH_ONE_RETAINED_BLOCKER",
                        "acceptedIds": ACCEPTED, "heldIds": HELD, "directorDecision": decision_binding,
                        "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
                        "independentAudit": audit_binding, "directorReceipt": receipt_binding,
                        "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
                        "countsBefore": {"reviewed": 810, "pending": 38}, "countsAfter": {"reviewed": 811, "pending": 37},
                        "completeReviewedStandaloneProceduresBefore": 534, "completeReviewedStandaloneProceduresAfter": 535,
                        "blockers": unaccepted, "runtimeSelectionEnabled": False,
                        "canonicalApplicationPerformedByOwner": False})
    acceptance_binding = bind(ACCEPTANCE)
    writej(RECEIPT, {"id": "RANK9-CASTINGCOST5-RETURN222-RECEIPT", "recordedAtUtc": timestamp,
                     "status": "ONE_ACCEPTED_ONE_BLOCKED_INDEPENDENT_AUDIT_PASSED",
                     "reviewedIds": SCOPE, "acceptedIds": ACCEPTED, "appliedIds": [], "heldIds": HELD,
                     "blockers": {"unholy-ascendance": ["CC194-B04"]}, "sourceAuthority": AUTH0,
                     "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
                     "independentAudit": audit_binding, "counts": delivery["counts"], "decisionId": director["id"]})
    receipt_binding = bind(RECEIPT)
    writej(APPLICATION, {"id": "RANK9-CASTINGCOST5-APPLICATION-222", "recordedAtUtc": timestamp,
                        "status": "APPLIED_ONE_EXACT_AUTHORED_PROCEDURE_WITH_ONE_RETAINED_BLOCKER",
                        "ownerInstruction": "Apply exact director-accepted ordinary-spell batches; keep unresolved identities pending.",
                        "acceptedIds": ACCEPTED, "unacceptedIds": HELD,
                        "directorAcceptance": acceptance_binding, "directorDecision": decision_binding,
                        "directorReturnReceipt": receipt_binding, "directorReturn": archive_binding,
                        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
                        "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
                        "manuscript": manuscript_binding, "indexBefore": bind(BACKUP, index_raw),
                        "countsBefore": {"reviewed": 810, "pending": 38}, "countsAfter": {"reviewed": 811, "pending": 37},
                        "completeReviewedStandaloneProcedures": {"before": 534, "after": 535},
                        "sourceStatusPreservedAsBlocked": True, "catalogChanged": False, "runtimeSelectionEnabled": False})
    application_binding = bind(APPLICATION)

    after = copy.deepcopy(before)
    index_pos = next(i for i, row in enumerate(before["entries"]) if row["id"] == "perfect-spell")
    old = before["entries"][index_pos]
    new = copy.deepcopy(old)
    new.update({"authoredStatus": "reviewed-authored-operational-playtest",
                "procedureFile": "../spell_candidates/rank9castingcost5_reviewed_222/MODEL.json",
                "procedurePointer": "/spells/0/procedure", "wholeCardPointer": "/spells/0",
                "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
                "wholeCardIdField": "id", "procedureTextPointer": "/spells/0/procedure/procedureContent",
                "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
                "sharedRulesPointer": "/spells/0/procedure/sharedRequirements",
                "manuscript": "../../../docs/spells/candidates/RANK9_CASTINGCOST5_REVIEWED_222.md",
                "reviewId": REVIEW, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
                "completeEvidenceRoot": PKG_REL.as_posix(), "completeEnvelopeBinding": model_binding,
                "casebookBinding": casebook_binding, "casebookEncoding": "Deterministic gzip; decompression reproduces the preserved casebook member in the exact director return archive.",
                "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
                "focusedCasesBinding": focused_binding, "sourceArchiveBinding": archive_binding,
                "deliveryManifestBinding": delivery_binding, "candidatePackageManifestBinding": package_manifest_binding,
                "procedureSourceBinding": decision_binding, "authoredAcceptanceReceipt": acceptance_binding,
                "authoredApplicationReceipt": application_binding})
    assert old["sourceStatus"] == new["sourceStatus"] == "blocked-pending-operational-review"
    after["entries"][index_pos] = new
    envelope = {"file": "../spell_candidates/rank9castingcost5_reviewed_222/MODEL.json", "binding": model_binding,
                "reviewId": REVIEW, "acceptedIds": ACCEPTED, "heldIds": HELD,
                "excludedPendingIds": sorted(pending_before - set(ACCEPTED)),
                "authority": acceptance_binding, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
                "sourceArchive": archive_binding, "deliveryManifest": delivery_binding,
                "casebookBinding": casebook_binding, "focusedCasesBinding": focused_binding,
                "candidatePackageManifestBinding": package_manifest_binding,
                "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_WITH_ONE_RETAINED_BLOCKER",
                "runtimeSelectionEnabled": False}
    after.setdefault("additionalStandaloneEnvelopes", []).append(envelope)
    after["authoredCounts"] = {"reviewed": 811, "pending": 37}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = 535
    pending_after = {x["id"] for x in after["entries"] if x["authoredStatus"] == "pending-authored-procedure"}
    assert pending_after == pending_before - set(ACCEPTED) and len(pending_after) == 37
    inverse = copy.deepcopy(after)
    inverse["entries"][index_pos] = copy.deepcopy(old)
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before

    after_raw = jb(after)
    index_temp = INDEX.with_suffix(".json.perfect222.tmp")
    index_temp.write_bytes(after_raw)
    index_temp.replace(INDEX)
    assert CATALOG.read_bytes() == catalog_raw
    writej(OPS, {"id": "RANK9-CASTINGCOST5-INDEX-OPERATIONS-222", "before": bind(BACKUP, index_raw),
                 "after": bind(INDEX, after_raw), "operations": [{"op": "replace-entry", "identity": "perfect-spell", "index": index_pos,
                 "before": copy.deepcopy(old), "after": copy.deepcopy(new)}], "inverseSemanticExact": True,
                 "onlyIdentityIds": ACCEPTED, "catalogChanged": False})

    # Advance the current pending audit, queue and handoff, carrying every unrelated hold.
    pending_doc = copy.deepcopy(p0)
    pending_doc.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-223", "recordedAtUtc": timestamp,
                        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN222",
                        "authority": AUTH1, "indexBinding": bind(INDEX, after_raw), "catalogBinding": bind(CATALOG, catalog_raw),
                        "pendingCount": 37, "pendingIds": sorted(pending_after), "allPendingIdsExistInNativeCatalog": pending_after <= set(catalog_rows),
                        "noPendingTargetWasSilentlyAccepted": True,
                        "lastDirectorReturn": receipt_binding,
                        "lastInlineDirectorReturn": receipt_binding,
                        "appliedReturn222": {"acceptedIds": ACCEPTED, "application": bind(APPLICATION), "independentAudit": audit_binding},
                        "retainedReturn222Blockers": {"unholy-ascendance": {"blockerIds": ["CC194-B04"], "holdIds": decs["unholy-ascendance"]["conditionalQualificationIds"], "reason": held_record["missing"]}},
                        "closed335AndCompletedCohortsReopened": False})
    pending_groups = []
    for group in pending_doc.get("groups", []):
        left = [sid for sid in group["pendingIds"] if sid in pending_after]
        if not left:
            continue
        g = copy.deepcopy(group)
        g["pendingIds"], g["pendingCount"] = left, len(left)
        if g["group"] == "rank9-casting-cost5":
            g.update({"status": "RETURN222_PERFECT_SPELL_APPLIED_UNHOLY_ASCENDANCE_HELD_CC194-B04",
                      "freshPacketRequiredForCurrentAuthority": True,
                      "blockingReturn": {"ids": HELD, "blockers": {"unholy-ascendance": ["CC194-B04"]}, "receipt": RECEIPT.relative_to(ROOT).as_posix()}})
        if g["group"] == NEXT:
            g.update({"status": "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_811_37", "freshPacketRequiredForCurrentAuthority": True})
        pending_groups.append(g)
    pending_doc["groups"] = pending_groups
    writej(PENDING1, pending_doc)
    pending_binding = bind(PENDING1)

    queue = copy.deepcopy(q0)
    groups = []
    for group in queue["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in pending_after]
        if not left:
            continue
        g = copy.deepcopy(group)
        g["pendingIds"], g["pendingCount"] = left, len(left)
        if g["group"] == "rank9-casting-cost5":
            g.update({"status": "RETURN222_PERFECT_SPELL_APPLIED_UNHOLY_ASCENDANCE_HELD_CC194-B04",
                      "freshPacketRequiredForCurrentAuthority": True,
                      "blockingReturn": {"ids": HELD, "blockers": {"unholy-ascendance": ["CC194-B04"]},
                                         "receipt": RECEIPT.relative_to(ROOT).as_posix(),
                                         "archive": archive_binding, "independentAudit": audit_binding}})
        if g["group"] == NEXT:
            g.update({"status": "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_811_37", "freshPacketRequiredForCurrentAuthority": True})
        groups.append(g)
    next_group = next(g for g in groups if g["group"] == NEXT)
    next_step = {"group": NEXT, "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS),
                 "status": "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_811_37", "freshPacketRequiredForCurrentAuthority": True,
                 "candidate": next_group.get("candidate"), "archive": next_group.get("archive")}
    batch = {"return": 222, "group": "rank9-casting-cost5", "ids": SCOPE,
             "acceptedIds": ACCEPTED, "appliedIds": ACCEPTED, "heldIds": HELD,
             "blockers": {"unholy-ascendance": ["CC194-B04"]}, "sourceAuthorityBefore": AUTH0,
             "sourceAuthorityAfter": AUTH1, "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
             "independentAudit": audit_binding, "application": bind(APPLICATION),
             "currentDecision": decision_binding, "exactAcceptance": acceptance_binding}
    queue.update({"id": "SPELL-REVIEW-QUEUE-223", "recordedAtUtc": timestamp, "supersedesQueue": bind(QUEUE0),
                  "currentAuthority": AUTH1, "currentIndexBinding": bind(INDEX, after_raw), "currentCatalogBinding": bind(CATALOG, catalog_raw),
                  "currentPendingGroups": groups, "pendingCount": 37, "nextGroup": NEXT, "next": next_step,
                  "nextPreparedRequest": next_step, "justAppliedBatch": batch, "lastReviewedBatch": batch,
                  "pendingIdentityAudit": pending_binding, "currentReturnArchive": archive_binding,
                  "currentReturnDelivery": delivery_binding, "currentReturnDecision": decision_binding,
                  "currentReturnAudit": audit_binding,
                  "packetStatus": "RETURN222_PERFECT_SPELL_APPLIED_UNHOLY_ASCENDANCE_HELD_811_37_NEXT_MEMORY_DENIAL6",
                  "githubChanges": False})
    queue["currentReturnSourceArchive"] = source_packet_binding
    queue["currentReturnSourceDelivery"] = bind(SOURCE_DELIVERY)
    writej(QUEUE1, queue)
    queue_binding = bind(QUEUE1)

    handoff = copy.deepcopy(h0)
    handoff.update({"id": "CURRENT-HANDOFF-223", "recordedAtUtc": timestamp,
                    "status": "RANK9_CASTINGCOST5_PERFECT_SPELL_APPLIED_UNHOLY_ASCENDANCE_HELD_NEXT_MEMORY_DENIAL6_811_37",
                    "currentAuthority": AUTH1, "currentIndexBinding": bind(INDEX, after_raw), "currentCatalogBinding": bind(CATALOG, catalog_raw),
                    "latestBatch": batch, "nextGroup": NEXT, "nextPendingCount": len(NEXT_IDS), "nextStep": next_step,
                    "pendingIdentityAudit": pending_binding, "queue": queue_binding, "appliedThisStep": batch,
                    "unacceptedThisStep": {"ids": HELD, "blockers": {"unholy-ascendance": ["CC194-B04"]}, "retainedInPendingSet": True},
                    "githubChanges": False, "runtimeSelectionEnabled": False, "canonicalRuntimeApplicationPerformed": False,
                    "currentReturnBinding": archive_binding, "currentReturnDelivery": delivery_binding,
                    "currentReturnAudit": audit_binding, "currentPreparation": bind(BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_222.json"),
                    "currentPacket": source_packet_binding,
                    "currentPacketDelivery": bind(SOURCE_DELIVERY)})
    writej(HANDOFF1, handoff)
    handoff_binding = bind(HANDOFF1)

    checks = [
        {"check": "Return222 ZIP and manifest independently pass 29 checks with no failures", "passed": audit["status"] == "PASS" and audit["checksFailed"] == 0},
        {"check": "Only director-accepted Perfect Spell is applied; Unholy Ascendance remains held", "passed": ACCEPTED == ["perfect-spell"] and HELD == ["unholy-ascendance"] and "CC194-B04" in unaccepted["unholy-ascendance"]["blockerIds"]},
        {"check": "Authority advances by one to 811 reviewed / 37 pending / 535 complete procedures", "passed": after["authoredCounts"] == {"reviewed": 811, "pending": 37} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 535},
        {"check": "Pending IDs equal the exact prior set minus Perfect Spell", "passed": pending_after == pending_before - set(ACCEPTED) and len(pending_after) == 37},
        {"check": "Inverse operation restores original index exactly and catalog remains byte-identical", "passed": inverse == before and CATALOG.read_bytes() == catalog_raw},
        {"check": "Candidate package files all reconcile to the package manifest", "passed": all((ROOT / x["path"]).is_file() and (ROOT / x["path"]).stat().st_size == x["bytes"] and sha((ROOT / x["path"]).read_bytes()) == x["sha256"] for x in package_manifest["files"])},
        {"check": "Next queue group is the exact two-identity Memory/Denial6 group", "passed": queue["nextGroup"] == NEXT and next_step["pendingIds"] == NEXT_IDS},
        {"check": "Runtime and downstream approval gates remain off", "passed": all(model[k] is False for k in ("runtimeSelectionEnabled", "runtimeTestsExecuted", "sourceProgramsExecuted", "implementationApproved", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))},
    ]
    validation = {"id": "RANK9-CASTINGCOST5-APPLICATION-VALIDATION-222", "recordedAtUtc": timestamp,
                  "status": "PASS" if all(x["passed"] for x in checks) else "FAIL",
                  "checksPassed": sum(x["passed"] for x in checks), "checksFailed": sum(not x["passed"] for x in checks),
                  "checks": checks, "acceptedIds": ACCEPTED, "heldIds": HELD,
                  "countsBefore": {"reviewed": 810, "pending": 38, "completeReviewedStandaloneProcedures": 534},
                  "countsAfter": {"reviewed": 811, "pending": 37, "completeReviewedStandaloneProcedures": 535},
                  "indexBefore": bind(BACKUP, index_raw), "indexAfter": bind(INDEX), "catalog": bind(CATALOG),
                  "application": bind(APPLICATION), "independentAudit": audit_binding,
                  "pendingIdentityAudit": pending_binding, "queueAfter": queue_binding, "handoffAfter": handoff_binding,
                  "nextGroup": NEXT, "runtimeSelectionEnabled": False}
    writej(VALIDATION, validation)
    assert validation["status"] == "PASS", checks
    SNAPSHOT.write_text("# Current ordinary spell-review checkpoint 223\n\n"
                        "Return222 independently passed 29 checks: 34 cases, 522 events, 1,044 forward and 1,044 inverse operations. "
                        "Applied exactly Perfect Spell as a static authored procedure. Unholy Ascendance remains pending under CC194-B04. "
                        "Authority: **811 reviewed/applied / 37 pending / 0 accepted-unapplied**, 535 complete standalone procedures and 173 scoped interfaces. "
                        "Next group: Rank9 Memory/Denial6 (mind-collapse, unravel-identity).\n\n"
                        "See [handoff](CURRENT_HANDOFF_223.json), [queue](CURRENT_SPELL_QUEUE_223.json), "
                        "[pending audit](CURRENT37_PENDING_IDENTITY_AUDIT_223.json), [Return222 audit](RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json), "
                        "[application validation](RANK9_CASTINGCOST5_APPLICATION_VALIDATION_222.json), and [candidate package](../spell_candidates/rank9castingcost5_reviewed_222/MODEL.json).\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "heldIds": HELD,
                      "authority": AUTH1, "nextGroup": NEXT, "independentAudit": audit["status"],
                      "validation": validation["status"], "validationChecks": validation["checksPassed"],
                      "indexSha256": sha(INDEX.read_bytes()), "candidateModel": model_binding,
                      "candidateManifest": package_manifest_binding}, indent=2))


if __name__ == "__main__":
    main()
