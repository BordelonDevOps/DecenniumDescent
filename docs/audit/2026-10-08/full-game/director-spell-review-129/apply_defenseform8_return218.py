from __future__ import annotations

import copy
import hashlib
import json
import shutil
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECV = BASE / "rank9_defenseform8_return218_received"
ARCHIVE = RECV / "DD_Rank9_DefenseForm5_Director_Return218.zip"
DELIVERY = RECV / "DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json"
AUDIT = BASE / "RANK9_DEFENSEFORM8_RETURN218_INDEPENDENT_AUDIT.json"
SOURCE = BASE / "rank9_defenseform8_source_packet_218_refreshed/DD_Rank9_DefenseForm8_CurrentSource_218.zip"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = BASE / "CURRENT_SPELL_QUEUE_218.json"
HANDOFF_BEFORE = BASE / "CURRENT_HANDOFF_218.json"
PENDING_BEFORE = BASE / "CURRENT40_PENDING_IDENTITY_AUDIT_217.json"
ACCEPTED = ["absolute-immunity", "body-to-void"]
HELD = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
BLOCKERS = {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}
BEFORE = {"reviewedApplied": 808, "pending": 40, "acceptedUnapplied": 0, "completeStandaloneProcedures": 532, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 810, "pending": 38, "acceptedUnapplied": 0, "completeStandaloneProcedures": 534, "scopedInterfaces": 173}
REVIEW_ID = "RANK9-DEFENSEFORM8-EXACT-AUTHORED-ACCEPTANCE-218"
APP_ID = "RANK9-DEFENSEFORM8-APPLICATION-218"
CANDIDATE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218")
CANDIDATE = ROOT / CANDIDATE_REL


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def bind(path: Path, raw: bytes | None = None, rel: str | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise RuntimeError(msg)


def main() -> None:
    audit, delivery = read(AUDIT), read(DELIVERY)
    queue_before, handoff_before, pending_before = read(QUEUE_BEFORE), read(HANDOFF_BEFORE), read(PENDING_BEFORE)
    require(audit["status"] == "PASS" and audit["checksFailed"] == 0 and all(x["passed"] for x in audit["checks"]), "Return218 independent audit failed")
    require(delivery["acceptedIds"] == ACCEPTED and delivery["heldIds"] == HELD and delivery["applied"] is False, "Delivery disposition differs from exact acceptances")
    require(delivery["authority"] == BEFORE and queue_before["currentAuthority"] == BEFORE and handoff_before["currentAuthority"] == BEFORE, "Return218 authority does not match the current index")
    require(pending_before["exactPendingCount"] == 40 and set(pending_before["pendingIds"]) >= set(ACCEPTED + HELD), "Prior pending audit differs")
    require(bind(INDEX)["sha256"] == queue_before["currentIndexBinding"]["sha256"] and bind(CATALOG)["sha256"] == queue_before["currentCatalogBinding"]["sha256"], "Live index or catalog changed after packet 218")
    require(not CANDIDATE.exists(), f"Candidate already exists: {CANDIDATE}")

    idx_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    idx, catalog = json.loads(idx_raw.decode("utf-8-sig")), json.loads(catalog_raw.decode("utf-8-sig"))
    require(idx["authoredCounts"] == {"reviewed": 808, "pending": 40}, "Index is not at authority 808/40")
    require(idx["representationCounts"]["completeReviewedStandaloneProcedures"] == 532, "Stored standalone count is not 532")
    rows = {x["id"]: x for x in idx["entries"]}
    cards = {x["id"]: x for x in catalog["spells"]}
    live_pending = {x["id"] for x in idx["entries"] if x["authoredStatus"] == "pending-authored-procedure"}
    require(len(live_pending) == 40 and set(ACCEPTED + HELD) <= live_pending, "Live pending set differs")

    with zipfile.ZipFile(ARCHIVE) as z:
        decision = json.loads(z.read("DIRECTOR_DECISION.json"))
        procedure_doc = json.loads(z.read("PROCEDURES.json"))
        question_doc = json.loads(z.read("QUESTION_DISPOSITIONS.json"))
        hold_register = json.loads(z.read("HOLD_REGISTER.json"))
        proc_rows = {x["spellId"]: x for x in procedure_doc["spells"]}
        decision_rows = {x["spellId"]: x for x in decision["perIdentity"]}
        require(decision["sourceAuthority"] == BEFORE and decision["acceptedIds"] == ACCEPTED and decision["heldIds"] == HELD and decision["applied"] is False, "Director decision scope differs")
        require(set(proc_rows) == set(decision_rows) == set(ACCEPTED + HELD), "Returned identity set differs")
        for sid in ACCEPTED + HELD:
            require(proc_rows[sid]["nativeCardAndAccessUnchanged"] == cards[sid], f"Native card/access differs for {sid}")
            require(rows[sid]["authoredStatus"] == "pending-authored-procedure" and rows[sid]["sourceStatus"] == "blocked-pending-operational-review", f"Current index row is not pending for {sid}")
            require(decision_rows[sid]["applied"] is False and proc_rows[sid]["applied"] is False, f"Return already applied {sid}")
        for sid in ACCEPTED:
            require(decision_rows[sid]["accepted"] is True and not decision_rows[sid]["blockerIds"], f"Acceptance mismatch for {sid}")
            require(proc_rows[sid]["accepted"] is True and bool(proc_rows[sid]["procedureText"].strip()), f"Accepted procedure absent for {sid}")
        for sid in HELD:
            require(decision_rows[sid]["accepted"] is False and decision_rows[sid]["blockerIds"] == BLOCKERS[sid], f"Hold mismatch for {sid}")
            require(proc_rows[sid]["accepted"] is False, f"Held procedure marked accepted: {sid}")
        member_rows = {x["path"]: x for x in delivery["members"]}
        package_members = [
            "AUTHORITY.json", "DIRECTOR_DECISION.json", "COUNTS.json", "PROCEDURES.json", "QUESTION_DISPOSITIONS.json",
            "HOLD_REGISTER.json", "BLOCKER_REASSESSMENT.json", "CASE_INDEX.json", "CASE_DISPOSITIONS.json",
            "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "BASELINE_DATA_CHECK.json", "ADDED_DATA_INTEGRITY_CHECK.json",
            "PRESERVED_CASE_INDEX.json", "SOURCE_CHECK.json", "SOURCE_EVIDENCE_MAP.json",
            "source/CURRENT_SOURCE_CONFERENCE_CANDIDATE_218.json", "source/CANDIDATE_BINDING_RECONCILIATION_218.json",
        ]
        for name in package_members:
            require(name in member_rows and sha(z.read(name)) == member_rows[name]["sha256"], f"Missing or unbound evidence file {name}")
        archive_raw = ARCHIVE.read_bytes()
        source_packet = z.read("source/DD_Rank9_DefenseForm8_CurrentSource_218.zip")
        require(source_packet == SOURCE.read_bytes(), "Embedded source packet differs from the prepared source packet")

        timestamp = now()
        candidate_stage = CANDIDATE.with_name(CANDIDATE.name + ".staging")
        require(not candidate_stage.exists(), f"Staging candidate already exists: {candidate_stage}")
        candidate_stage.mkdir(parents=True)
        (candidate_stage / "DIRECTOR_RETURN").mkdir()
        for name in package_members:
            dest = candidate_stage / "DIRECTOR_RETURN" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(z.read(name))
        (candidate_stage / "DIRECTOR_RETURN" / "procedures").mkdir()
        for sid in ACCEPTED + HELD:
            (candidate_stage / "DIRECTOR_RETURN" / "procedures" / f"{sid}.json").write_bytes(z.read(f"procedures/{sid}.json"))

        qrows = question_doc.get("questions", [])
        spells = []
        for position, sid in enumerate(ACCEPTED):
            row = proc_rows[sid]
            native = cards[sid]
            qualification_ids = decision_rows[sid].get("conditionalQualificationIds", [])
            spells.append({
                "id": sid, "name": native["name"], "accepted": True, "applied": False,
                "nativeCardAndAccessUnchanged": copy.deepcopy(native),
                "procedure": {
                    "id": f"RANK9-DEFENSEFORM8-STATIC-PROCEDURE-218-{sid.upper()}",
                    "spellId": sid, "reviewId": REVIEW_ID,
                    "status": "static-authored-director-accepted-unapplied",
                    "procedureText": row["procedureText"], "sharedRules": copy.deepcopy(row["sharedRules"]),
                    "sourceQuestionIds": copy.deepcopy(row["questionIds"]), "qualificationIds": qualification_ids,
                    "directorDecisionPointer": "DIRECTOR_RETURN/DIRECTOR_DECISION.json",
                },
                "directorProcedureRecord": copy.deepcopy(row),
                "questionDispositions": {q["id"]: copy.deepcopy(q) for q in qrows if q.get("id") in row["questionIds"]},
                "runtimeSelectionEnabled": False,
                "directorProcedureRecordPointer": f"DIRECTOR_RETURN/PROCEDURES.json#/spells/{[x['spellId'] for x in procedure_doc['spells']].index(sid)}",
            })

        return_binding = bind(ARCHIVE)
        delivery_binding = bind(DELIVERY)
        audit_binding = bind(AUDIT)
        source_binding = bind(SOURCE)
        candidate = {
            "schemaVersion": 1, "id": "DD-RANK9-DEFENSEFORM8-DIRECTOR-RETURN218", "reviewId": REVIEW_ID,
            "status": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_THREE_HELD",
            "scope": "Only Absolute Immunity and Body to Void are accepted and applied as static authored procedures. Elemental Shell, Timeless Form, and Invulnerable Sphere remain pending under DF218 blockers. Native cards/access and runtime status are unchanged.",
            "acceptedIds": ACCEPTED, "heldIds": HELD,
            "heldDecisions": [{"id": sid, "accepted": False, "applied": False, "blockerIds": BLOCKERS[sid], "directorProcedureRecord": copy.deepcopy(proc_rows[sid])} for sid in HELD],
            "sourceAuthorityBeforeApplication": BEFORE, "sourceAuthorityAfterApplication": AFTER,
            "sharedRules": copy.deepcopy(procedure_doc.get("sharedRules", {})), "spells": spells,
            "directorQualifications": copy.deepcopy(decision.get("qualifications", [])), "holdRegister": "DIRECTOR_RETURN/HOLD_REGISTER.json",
            "directorReturnArchive": return_binding, "directorDeliveryManifest": delivery_binding,
            "independentAudit": audit_binding, "sourceConferenceArchive": source_binding,
            "currentQueueAtDecision": bind(QUEUE_BEFORE), "currentPendingAuditAtDecision": bind(PENDING_BEFORE),
            "runtimeSelectionEnabled": False, "implementationApproved": False, "humanPlaytested": False,
            "balanceApproved": False, "cosmologyModified": False, "domainClosure": False, "releaseApproved": False,
            "candidatePackageManifestBinding": None,
        }
        def candidate_files():
            return [p for p in sorted(candidate_stage.rglob("*")) if p.is_file() and p.name not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}]
        manifest = {"id": "RANK9-DEFENSEFORM8-CANDIDATE-PACKAGE-MANIFEST-218", "files": [bind(p, rel=p.relative_to(candidate_stage).as_posix()) for p in candidate_files()], "selfExcluded": "CANDIDATE_PACKAGE_MANIFEST.json", "modelExcluded": "MODEL.json"}
        dump(candidate_stage / "CANDIDATE_PACKAGE_MANIFEST.json", manifest)
        manifest_binding = bind(candidate_stage / "CANDIDATE_PACKAGE_MANIFEST.json", rel=(CANDIDATE_REL / "CANDIDATE_PACKAGE_MANIFEST.json").as_posix())
        candidate["candidatePackageManifestBinding"] = manifest_binding
        dump(candidate_stage / "MODEL.json", candidate)
        model_binding = bind(candidate_stage / "MODEL.json", rel=(CANDIDATE_REL / "MODEL.json").as_posix())
        shutil.move(str(candidate_stage), str(CANDIDATE))

    # All external inputs are verified; plan the index edit and its exact inverse.
    raw_before = INDEX.read_bytes()
    before_binding = bind(INDEX, raw_before)
    catalog_binding = bind(CATALOG, catalog_raw)
    acceptance_path = BASE / "RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_218.json"
    application_path = BASE / "RANK9_DEFENSEFORM8_APPLICATION_218.json"
    operations_path = BASE / "RANK9_DEFENSEFORM8_INDEX_OPERATIONS_218.json"
    validation_path = BASE / "RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_218.json"
    backup_path = BASE / "authored_review_index.before_defenseform8_218.json"
    generated = [acceptance_path, application_path, operations_path, validation_path, backup_path]
    require(not any(p.exists() for p in generated), "Return218 application outputs already exist")

    model_binding = bind(CANDIDATE / "MODEL.json")
    manifest_binding = bind(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")
    acceptance = {
        "id": REVIEW_ID, "recordedAtUtc": now(), "status": "TWO_EXACT_STATIC_AUTHORED_IDENTITIES_ACCEPTED_WITH_THREE_RETAINED_HELD",
        "acceptedIds": ACCEPTED, "heldIds": HELD, "blockers": BLOCKERS,
        "directorDecision": {"path": f"{CANDIDATE_REL.as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json", "sha256": sha((CANDIDATE / "DIRECTOR_RETURN/DIRECTOR_DECISION.json").read_bytes())},
        "directorReturn": bind(ARCHIVE), "deliveryManifest": bind(DELIVERY), "independentAudit": bind(AUDIT),
        "candidateEnvelope": model_binding, "candidatePackageManifest": manifest_binding,
        "countsBefore": BEFORE, "countsAfter": AFTER, "runtimeSelectionEnabled": False,
        "implementationApproved": False, "canonicalRuntimeApplicationPerformed": False,
    }
    dump(acceptance_path, acceptance)
    acceptance_binding = bind(acceptance_path)

    after = copy.deepcopy(idx)
    operations = []
    accepted_proc_rows = {x["spellId"]: x for x in procedure_doc["spells"]}
    for position, sid in enumerate(ACCEPTED):
        index_position = next(i for i, row in enumerate(idx["entries"]) if row["id"] == sid)
        old = copy.deepcopy(idx["entries"][index_position])
        updated = copy.deepcopy(old)
        updated.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": f"../spell_candidates/{CANDIDATE_REL.name}/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure", "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id", "reviewId": APP_ID, "runtimeSelectionEnabled": False,
            "priorCatalogSelectionStatusUnchanged": True, "completeEnvelopeBinding": model_binding,
            "candidatePackageManifestBinding": manifest_binding,
            "directorReturnBinding": bind(ARCHIVE), "directorDeliveryManifestBinding": bind(DELIVERY),
            "independentAuditBinding": bind(AUDIT), "sourceConferenceArchiveBinding": bind(SOURCE),
            "authoredAcceptanceReceipt": acceptance_binding,
            "authoredApplicationReceipt": application_path.relative_to(ROOT).as_posix(),
        })
        require(updated["sourceStatus"] == old["sourceStatus"] == "blocked-pending-operational-review", f"Source status changed for {sid}")
        after["entries"][index_position] = updated
        operations.append({"op": "replace-entry", "identity": sid, "index": index_position, "before": old, "after": copy.deepcopy(updated)})

    pending_after = live_pending - set(ACCEPTED)
    after["authoredCounts"] = {"reviewed": AFTER["reviewedApplied"], "pending": AFTER["pending"]}
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = AFTER["completeStandaloneProcedures"]
    excluded = sorted(pending_after)
    after["additionalStandaloneEnvelopes"].append({
        "file": f"../spell_candidates/{CANDIDATE_REL.name}/MODEL.json", "binding": model_binding,
        "reviewId": REVIEW_ID, "acceptedIds": ACCEPTED, "heldIds": HELD, "excludedPendingIds": excluded,
        "authority": acceptance_binding, "applicationReceipt": application_path.relative_to(ROOT).as_posix(),
        "sourceArchive": bind(ARCHIVE), "sourceConferenceArchive": bind(SOURCE),
        "candidatePackageManifestBinding": manifest_binding,
        "scope": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_THREE_HELD", "runtimeSelectionEnabled": False,
    })
    require({x["id"] for x in after["entries"] if x["authoredStatus"] == "pending-authored-procedure"} == pending_after and len(pending_after) == 38, "Planned pending set is wrong")
    inverse = copy.deepcopy(after)
    for op in operations:
        inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(idx["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(idx["representationCounts"])
    require(inverse == idx, "Index inverse does not restore exact current object")
    after_raw = (json.dumps(after, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    after_binding = bind(INDEX, after_raw)

    app = {
        "id": APP_ID, "recordedAtUtc": now(), "status": "APPLIED_TWO_EXACT_ACCEPTED_STATIC_AUTHORED_PROCEDURES_TO_REVIEW_INDEX",
        "acceptedIds": ACCEPTED, "heldIds": HELD, "blockerIds": BLOCKERS,
        "directorReturn": bind(ARCHIVE), "deliveryManifest": bind(DELIVERY), "independentAudit": bind(AUDIT),
        "candidateEnvelope": model_binding, "directorAcceptance": acceptance_binding,
        "indexBefore": before_binding, "indexAfter": after_binding,
        "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 532, "after": 534},
        "sourceStatusPreservedAsBlocked": True, "catalogBindingUnchanged": catalog_binding,
        "catalogChanged": False, "runtimeSelectionEnabled": False, "githubChanges": False,
    }
    dump(application_path, app)
    app_binding = bind(application_path)
    shutil.copyfile(INDEX, backup_path)
    tmp = INDEX.with_suffix(".json.return218.tmp")
    require(not tmp.exists(), "Temporary index output exists")
    tmp.write_bytes(after_raw)
    tmp.replace(INDEX)
    require(bind(INDEX)["sha256"] == after_binding["sha256"] and CATALOG.read_bytes() == catalog_raw, "Persisted index or catalog verification failed")
    dump(operations_path, {"id": "RANK9-DEFENSEFORM8-INDEX-OPERATIONS-218", "before": before_binding, "after": after_binding, "authorityBefore": BEFORE, "authorityAfter": AFTER, "operations": operations, "inverseSemanticExact": True, "inverseRestores": before_binding, "onlyIdentityIds": ACCEPTED, "catalogChanged": False})

    # Refresh every queue group from the exact post-application pending set.
    groups = copy.deepcopy(queue_before["currentPendingGroups"])
    for group in groups:
        group["pendingIds"] = [sid for sid in group["pendingIds"] if sid in pending_after]
        if not group["pendingIds"]:
            continue
        group["pendingCount"] = len(group["pendingIds"])
        if group["group"] == "rank9-defense-form8":
            group.update({"status": "HELD_RETURN218_THREE_IDENTITIES_REMAIN_ON_DF218_EVIDENCE_BLOCKERS", "freshPacketRequiredForCurrentAuthority": True,
                          "blockingReturn": {"return": 218, "ids": HELD, "blockerIds": BLOCKERS, "acceptedIds": ACCEPTED, "appliedIds": ACCEPTED, "independentAudit": str(AUDIT.relative_to(ROOT))}})
        elif not str(group.get("status", "")).startswith("HELD_"):
            group.update({"status": "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_810_38_0", "freshPacketRequiredForCurrentAuthority": True})
    groups = [g for g in groups if g["pendingIds"]]
    all_queued = [sid for g in groups for sid in g["pendingIds"]]
    require(len(all_queued) == len(set(all_queued)) == 38 and set(all_queued) == pending_after, "Refreshed queue does not match exact pending set")
    next_group = next(g for g in groups if not str(g.get("status", "")).startswith("HELD_"))
    pending_path = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_218.json"
    queue_path = BASE / "CURRENT_SPELL_QUEUE_218_APPLIED.json"
    handoff_path = BASE / "CURRENT_HANDOFF_218_APPLIED.json"
    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_218_APPLIED.md"
    request_path = BASE / "NEXT_DIRECTOR_REQUEST_AFTER_218.txt"
    pending_doc = {"id": "CURRENT38-PENDING-IDENTITY-AUDIT-218", "recordedAtUtc": now(), "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "authority": AFTER,
                   "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "pendingCount": 38, "pendingIds": all_queued, "groups": groups,
                   "allPendingIdsExistInNativeCatalog": all(s in cards for s in all_queued), "noPendingTargetWasSilentlyAccepted": True,
                   "preservedHolds": [{"ids": HELD, "blockerIds": BLOCKERS}, *pending_before.get("preservedHolds", [])]}
    dump(pending_path, pending_doc)
    pending_bind = bind(pending_path)
    queue = copy.deepcopy(queue_before)
    queue.update({"id": "SPELL-REVIEW-QUEUE-218-APPLIED", "recordedAtUtc": now(), "supersedesQueue": bind(QUEUE_BEFORE), "currentAuthority": AFTER,
                  "currentIndexBinding": bind(INDEX), "currentCatalogBinding": bind(CATALOG), "currentPendingGroups": groups,
                  "nextSuggestedGroups": [g for g in groups if not str(g.get("status", "")).startswith("HELD_")][:5],
                  "nextGroup": next_group["group"], "next": {"group": next_group["group"], "pendingIds": next_group["pendingIds"], "pendingCount": len(next_group["pendingIds"]), "freshPacketRequiredForCurrentAuthority": True},
                  "pendingIdentityAudit": pending_bind, "justAppliedBatch": {"return": 218, "reviewId": REVIEW_ID, "group": "rank9-defense-form8", "reviewedIds": ACCEPTED + HELD,
                      "acceptedIds": ACCEPTED, "appliedIds": ACCEPTED, "heldIds": HELD, "blockers": BLOCKERS, "application": str(application_path.relative_to(ROOT)), "independentAudit": str(AUDIT.relative_to(ROOT))},
                  "githubChanges": False})
    dump(queue_path, queue)
    handoff = {"id": "CURRENT-HANDOFF-218-APPLIED", "recordedAtUtc": now(), "status": "RETURN218_TWO_EXACT_ACCEPTANCES_APPLIED_810_38_NEXT_DIRECTOR_GROUP_READY",
               "currentAuthority": AFTER, "currentIndexBinding": bind(INDEX), "currentCatalogBinding": bind(CATALOG),
               "latestBatch": {"return": 218, "group": "rank9-defense-form8", "ids": ACCEPTED + HELD, "acceptedIds": ACCEPTED, "appliedIds": ACCEPTED, "heldIds": HELD,
                   "blockers": BLOCKERS, "directorReturn": bind(ARCHIVE), "deliveryManifest": bind(DELIVERY), "independentAudit": bind(AUDIT), "application": app_binding},
               "preservedOtherHolds": pending_doc["preservedHolds"], "nextStep": {"group": next_group["group"], "pendingIds": next_group["pendingIds"], "pendingCount": len(next_group["pendingIds"]), "status": "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_810_38_0"},
               "pendingIdentityAudit": pending_bind, "queue": bind(queue_path), "appliedThisStep": True, "githubChanges": False,
               "runtimeSelectionEnabled": False, "canonicalRuntimeApplicationPerformed": False}
    dump(handoff_path, handoff)
    request = (f"Continue ordinary spell review under GPT as director. Current authority is 810 reviewed/applied / 38 pending / 0 accepted-unapplied; index SHA-256 {bind(INDEX)['sha256']}; catalog SHA-256 {bind(CATALOG)['sha256']}.\n\n"
               f"Review only {next_group['group']} and its exact current pending identities: {', '.join(next_group['pendingIds'])}. Use a freshly refreshed source packet bound to authority 810/38/0. Preserve the three Defense/Form8 holds ({', '.join(HELD)}) under {', '.join(h for ids in BLOCKERS.values() for h in ids)} and all unrelated holds. Return explicit per-identity accepted/held decisions, exact blockers/conditional qualifications, and a verifiable archive plus delivery manifest. Do not apply changes; Codex will independently audit and apply only exact acceptances.\n")
    request_path.write_text(request, encoding="utf-8")
    snapshot_path.write_text(f"# Current Spell Review Snapshot — Return 218\n\nAuthority: **810 reviewed/applied / 38 pending / 0 accepted-unapplied**, with 534 complete standalone procedures. Return218 passed 22 independent checks, including 115 exact archive bindings, 69 unchanged preserved cases, and 72 forward/inverse event replays for the 3 added cases. Exactly `{', '.join(ACCEPTED)}` were applied as static authored procedures. The three remaining Defense/Form8 identities remain pending on four exact blockers.\n\nNext queue group: **{next_group['group']}** — {', '.join(next_group['pendingIds'])}. Runtime selection remains disabled; no GitHub changes were made.\n", encoding="utf-8")

    checks = [
        {"check": "Return218 independent audit passed before application", "passed": audit["status"] == "PASS" and audit["checksFailed"] == 0},
        {"check": "Only the two explicit director acceptances changed authored status", "passed": len(operations) == 2 and [x["identity"] for x in operations] == ACCEPTED},
        {"check": "Three unaccepted identities remain pending under exact blockers", "passed": all(s in pending_after for s in HELD) and BLOCKERS == {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}},
        {"check": "Authority advanced exactly from 808/40/532 to 810/38/534", "passed": after["authoredCounts"] == {"reviewed": 810, "pending": 38} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 534},
        {"check": "Exact inverse restores the pre-application index", "passed": inverse == idx},
        {"check": "All native catalog bytes and all class/source statuses remain unchanged", "passed": CATALOG.read_bytes() == catalog_raw and all(next(x for x in after["entries"] if x["id"] == sid)["sourceStatus"] == "blocked-pending-operational-review" for sid in ACCEPTED + HELD)},
        {"check": "Queue and pending audit exactly match all 38 remaining pending IDs", "passed": set(all_queued) == pending_after and len(all_queued) == 38},
        {"check": "Next group is the first non-held group in queue order", "passed": next_group["group"] == "rank9-ward-control6" and next_group["pendingIds"] == ["nullification-wave", "reality-anchor"]},
        {"check": "Candidate package file bindings pass", "passed": all((CANDIDATE / row["path"]).is_file() and bind(CANDIDATE / row["path"], rel=row["path"])["sha256"] == row["sha256"] for row in manifest["files"])},
    ]
    validation = {"id": "RANK9-DEFENSEFORM8-APPLICATION-VALIDATION-218", "recordedAtUtc": now(), "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
                  "checksPassed": sum(c["passed"] for c in checks), "checksFailed": sum(not c["passed"] for c in checks), "checks": checks,
                  "acceptedIds": ACCEPTED, "heldIds": HELD, "countsBefore": BEFORE, "countsAfter": AFTER,
                  "indexBefore": before_binding, "indexAfter": bind(INDEX), "catalog": bind(CATALOG), "application": bind(application_path),
                  "independentAudit": bind(AUDIT), "pendingIdentityAudit": bind(pending_path), "queueAfter": bind(queue_path), "handoffAfter": bind(handoff_path),
                  "nextGroup": next_group["group"], "runtimeSelectionEnabled": False, "githubChanges": False}
    dump(validation_path, validation)
    require(validation["status"] == "PASS", f"Application validation failed: {checks}")
    print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "heldIds": HELD, "authority": AFTER, "nextGroup": next_group["group"], "nextIds": next_group["pendingIds"], "audit": audit["status"], "validation": validation["status"], "indexSha256": bind(INDEX)["sha256"]}, indent=2))


if __name__ == "__main__":
    main()
