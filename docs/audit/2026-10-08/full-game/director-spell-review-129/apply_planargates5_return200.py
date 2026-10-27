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
RECEIVED = AUDIT / "rank9_planargates5_return200_received"
ZIP = RECEIVED / "DD_Rank9_PlanarGates5_Director_Return200.zip"
DELIVERY = RECEIVED / "DD_Rank9_PlanarGates5_Director_Return200_DELIVERY.json"
AUDIT_JSON = AUDIT / "RANK9_PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
Q0 = AUDIT / "CURRENT_SPELL_QUEUE_198.json"
H0 = AUDIT / "CURRENT_HANDOFF_198.json"
P0 = AUDIT / "CURRENT58_PENDING_IDENTITY_AUDIT_198.json"
BACKUP = AUDIT / "authored_review_index.before_planargates5_200.json"
PKG_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200")
PKG = ROOT / PKG_REL
STAGE = PKG.with_name(PKG.name + ".staging")
MAN = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_PLANAR_GATES5_REVIEWED_200.md"
ACCEPTED = ["gate", "absolute-gate", "planar-sanctuary"]
UNACCEPTED = ["banishment-gate", "conjure-demiplane-fortress"]
GROUP = ACCEPTED + UNACCEPTED
NEXT = "rank9-summon-hosts5"
BEFORE = {"reviewed": 790, "pending": 58}
AFTER = {"reviewed": 793, "pending": 55}
COMPLETE0, COMPLETE1 = 514, 517
REVIEW = "RANK9-PLANARGATES5-EXACT-AUTHORED-ACCEPTANCE-200"
APP = "RANK9-PLANARGATES5-APPLICATION-200"
DEC = AUDIT / "RANK9_PLANARGATES5_DIRECTOR_DECISION_200.json"
ACC = AUDIT / "RANK9_PLANARGATES5_EXACT_ACCEPTANCE_200.json"
RCPT = AUDIT / "RANK9_PLANARGATES5_RETURN200_RECEIPT.json"
APPFILE = AUDIT / "RANK9_PLANARGATES5_APPLICATION_200.json"
OPS = AUDIT / "RANK9_PLANARGATES5_INDEX_OPERATIONS_200.json"
P1 = AUDIT / "CURRENT55_PENDING_IDENTITY_AUDIT_200.json"
Q1 = AUDIT / "CURRENT_SPELL_QUEUE_200.json"
H1 = AUDIT / "CURRENT_HANDOFF_200.json"
VALID = AUDIT / "RANK9_PLANARGATES5_APPLICATION_VALIDATION_200.json"
SNAP = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_200.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(jb(value))


def bind(path: Path, raw: bytes | None = None):
    value = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(value), "sha256": sha(value)}


def copy_member(archive: zipfile.ZipFile, name: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with archive.open(name, "r") as source, target.open("wb") as dest:
        shutil.copyfileobj(source, dest, 1024 * 1024)


def main() -> None:
    outputs = [BACKUP, MAN, DEC, ACC, RCPT, APPFILE, OPS, P1, Q1, H1, VALID, SNAP]
    assert read(AUDIT_JSON)["status"] == "PASS" and read(AUDIT_JSON)["checksPassed"] == 21
    assert all(not path.exists() for path in outputs)
    assert not PKG.exists() and not STAGE.exists()

    delivery = read(DELIVERY)
    baseline = {
        "reviewedApplied": 790, "pending": 58, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 514, "scopedInterfaces": 173,
    }
    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read(INDEX), read(CATALOG)
    q0, h0, p0 = map(read, (Q0, H0, P0))
    rows = {entry["id"]: entry for entry in before["entries"]}
    cats = {entry["id"] for entry in catalog["spells"]}
    live = {entry["id"] for entry in before["entries"]
            if entry["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == BEFORE
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE0
    assert len(live) == 58 and set(GROUP) <= live and set(p0["pendingIds"]) == live
    assert p0["indexBinding"]["sha256"] == sha(before_raw)
    assert q0["currentAuthority"] == baseline and q0["pendingCount"] == 58
    assert h0["currentAuthority"] == baseline
    assert delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED
    assert delivery["applied"] is False and delivery["authorityUnchanged"] == baseline
    timestamp = datetime.now(timezone.utc).isoformat()

    with zipfile.ZipFile(ZIP) as archive:
        director = json.loads(archive.read("DIRECTOR_DECISION.json"))
        spell_records = json.loads(archive.read("PROCEDURES.json"))["spells"]
        spell_map = {entry["id"]: entry for entry in spell_records}
        decisions = {entry["spellId"]: entry for entry in director["perIdentity"]}
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        delivery_rows = {item["path"]: item for item in delivery["members"]}
        next_handoff = json.loads(archive.read("NEXT_QUEUE_HANDOFF.json"))
        next_group = next_handoff["nextCurrentQueueGroupUnchanged"]

        assert director["acceptedIds"] == ACCEPTED and director["unacceptedIds"] == UNACCEPTED
        assert director["authorityUnchanged"] == baseline and director["applied"] is False
        assert next_handoff["canonicalAuthorityUnchanged"] == baseline
        assert next_handoff["acceptedThisReturnUnapplied"] == ACCEPTED
        assert next_group["group"] == NEXT and next_group["pendingCount"] == 5
        assert next_group["pendingIds"] == [
            "summon-elemental-avatar", "conjure-magmatic-wyrm", "planar-army",
            "summon-herald-of-the-planes", "summon-avatar-of-decay",
        ]
        assert all(decisions[s]["accepted"] and not decisions[s]["applied"]
                   and not decisions[s]["blockerIds"] for s in ACCEPTED)
        assert all(not decisions[s]["accepted"] and not decisions[s]["applied"]
                   and decisions[s]["blockerIds"] for s in UNACCEPTED)
        assert set(spell_map) == set(decisions) == set(GROUP)
        assert all(spell_map[s]["accepted"] and not spell_map[s]["applied"] for s in ACCEPTED)
        assert all(not spell_map[s]["accepted"] and not spell_map[s]["applied"] for s in UNACCEPTED)
        for sid in GROUP:
            old = rows[sid]
            projection = spell_map[sid]["sourceIndexEntryUnchanged"]
            assert old["sourceStatus"] == "blocked-pending-operational-review"
            assert old["authoredStatus"] == "pending-authored-procedure"
            assert projection["id"] == sid and projection["name"] == old["name"]
            assert projection["wholeCardPointer"] == old["wholeCardPointer"]
            assert projection["sourceStatus"] == old["sourceStatus"]
            assert spell_map[sid]["nativeCardUnchanged"]["id"] == sid

        stage_allow = {"CASEBOOK.json"}
        STAGE.mkdir(parents=True)
        for name in archive.namelist():
            if name.endswith("/") or name in stage_allow or name.startswith(("cases/", "supplemental_sources/", "source_packet/")):
                continue
            copy_member(archive, name, STAGE / name)

        source_map = []
        supplemental = json.loads(archive.read("SUPPLEMENTAL_SOURCE_VERIFICATION.json"))["bindings"]
        for pos, source in enumerate(supplemental):
            member = "supplemental_sources/" + source["path"]
            short = f"{pos:02d}_{source['sha256'][:12]}_{source['path'].rsplit('/', 1)[-1]}"
            target = STAGE / "supplemental_sources" / short
            copy_member(archive, member, target)
            raw = target.read_bytes()
            assert len(raw) == source["bytes"] and sha(raw) == source["sha256"]
            source_map.append({
                "sourcePath": source["path"],
                "packagePath": (PKG_REL / "supplemental_sources" / short).as_posix(),
                "bytes": len(raw), "sha256": sha(raw),
            })
        write(STAGE / "SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json", {
            "sourceCommit": director["sourceCommit"], "count": len(source_map), "sources": source_map,
        })
        source_map_bind = bind(STAGE / "SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json")
        with archive.open("CASEBOOK.json", "r") as source, (STAGE / "CASEBOOK.json.gz").open("wb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0, compresslevel=6) as compressed:
                shutil.copyfileobj(source, compressed, 1024 * 1024)
        (STAGE / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGE / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(AUDIT_JSON.read_bytes())

        archive_binding, delivery_binding, audit_binding = bind(ZIP), bind(DELIVERY), bind(AUDIT_JSON)
        source_packet = delivery["sourcePacket"]
        packet_binding = {
            "path": source_packet["path"], "bytes": source_packet["bytes"], "sha256": source_packet["sha256"]
        }
        dispositions = json.loads(archive.read("CASE_DISPOSITIONS.json"))["cases"]
        disposition_map = {item["id"]: item for item in dispositions}
        case_ids = {sid: list(spell_map[sid]["caseIds"]) for sid in GROUP}
        accepted_case_ids = {case for sid in ACCEPTED for case in case_ids[sid]}
        accepted_events = sum(disposition_map[case]["eventCount"] for case in accepted_case_ids)

        spells = []
        for pos, sid in enumerate(ACCEPTED):
            spell = spell_map[sid]
            native = copy.deepcopy(spell["nativeCardUnchanged"])
            assert native["id"] == sid and native["status"] == "blocked-pending-operational-review"
            question_ids = copy.deepcopy(spell["questionIds"])
            spells.append({
                "id": sid,
                "name": rows[sid]["name"],
                "position": pos,
                "procedure": {
                    "id": "PG200-STATIC-" + sid.upper().replace("-", "_"),
                    "spellId": sid,
                    "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                    "accepted": True,
                    "applied": False,
                    "nativeCardUnchanged": native,
                    "procedureContent": copy.deepcopy(spell["procedure"]),
                    "sharedRequirements": copy.deepcopy(spell["sharedContract"]),
                    "questionIds": question_ids,
                    "qualifications": {
                        "directorDecision": decisions[sid]["decision"],
                        "retainedHoldIds": copy.deepcopy(spell["holdIds"]),
                        "caseCount": len(case_ids[sid]),
                    },
                    "caseIds": case_ids[sid],
                    "directorDecisionId": director["id"],
                },
                "directorProcedureRecord": copy.deepcopy(spell),
                "nativeCardUnchanged": native,
                "caseIds": case_ids[sid],
                "questionIds": question_ids,
                "holdIds": copy.deepcopy(spell["holdIds"]),
                "runtimeSelectionEnabled": False,
            })

        blocker_map = {}
        for sid in UNACCEPTED:
            blocker_ids = decisions[sid]["blockerIds"]
            records = [copy.deepcopy(row) for row in director["blockers"]
                       if row["id"] in blocker_ids and sid in row.get("spellIds", [])]
            assert records and [row["id"] for row in records] == blocker_ids
            blocker_map[sid] = {"blockerIds": blocker_ids, "blockerRecords": records}

        model = {
            "schemaVersion": 1,
            "moduleId": "rank9planargates5-reviewed-200",
            "status": "THREE_EXACT_STATIC_AUTHORED_PROCEDURES_APPLIED_WITH_TWO_BLOCKED",
            "scope": "Only the three individually accepted static procedures are applied. Banishment Gate and Conjure Demiplane Fortress remain pending under PG200-B03/B04 and PG200-B06. Native cards, source/access status and class routes remain unchanged; runtime and downstream approval gates stay disabled.",
            "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED,
            "excludedPendingIds": sorted(live - set(ACCEPTED)),
            "unacceptedHolds": blocker_map,
            "sharedRequirements": {"scope": "No global/shared rule changes; native cards and class routes unchanged.",
                                   "runtimeSelectionEnabled": False},
            "spells": spells,
            "caseCoverage": {
                "caseCount": sum(len(value) for value in case_ids.values()),
                "acceptedCaseCount": len(accepted_case_ids),
                "acceptedEventCount": accepted_events,
                "caseDispositionsBinding": delivery_rows["CASE_DISPOSITIONS.json"],
            },
            "returnCounts": delivery["counts"],
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "submittedSourcePacket": packet_binding,
            "casebookFile": "CASEBOOK.json.gz",
            "casebookSourceArchiveMemberBinding": delivery_rows["CASEBOOK.json"],
            "casebookBinding": bind(STAGE / "CASEBOOK.json.gz"),
            "supplementalSourcePackageMap": source_map_bind,
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
        write(STAGE / "MODEL.json", model)
        package_manifest = {
            "id": "RANK9-PLANARGATES5-PACKAGE-MANIFEST-200",
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "sourceAnchorCommit": director["sourceCommit"],
            "files": [],
        }
        for file in sorted(path for path in STAGE.rglob("*") if path.is_file()):
            raw = file.read_bytes()
            package_manifest["files"].append({
                "path": (PKG_REL / file.relative_to(STAGE)).as_posix(),
                "bytes": len(raw), "sha256": sha(raw),
            })
        write(STAGE / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
        shutil.move(str(STAGE), str(PKG))
        model_binding = bind(PKG / "MODEL.json")
        package_manifest_binding = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
        casebook_binding = bind(PKG / "CASEBOOK.json.gz")
        MAN.parent.mkdir(parents=True, exist_ok=True)
        MAN.write_bytes((PKG / "STANDALONE_PROCEDURES.md").read_bytes())
        shutil.copyfile(INDEX, BACKUP)
        assert BACKUP.read_bytes() == before_raw

        write(DEC, {
            "id": director["id"], "recordedAtUtc": timestamp,
            "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE",
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "blockers": blocker_map, "directorReturn": archive_binding,
            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
            "authorityAtDecision": baseline, "exactDirectorDecisions": director["perIdentity"],
            "scope": "Static authorship only; no runtime, implementation, human-play, balance, cosmology, domain closure, completion or release approval.",
            "canonicalFilesChangedByDirector": False,
        })
        acceptance = {
            "id": REVIEW, "recordedAtUtc": timestamp,
            "status": "THREE_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_TWO_RETAINED_BLOCKERS",
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "directorDecision": bind(DEC), "directorReturn": archive_binding,
            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
            "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
            "countsBefore": BEFORE, "countsAfter": AFTER,
            "completeReviewedStandaloneProceduresBefore": COMPLETE0,
            "completeReviewedStandaloneProceduresAfter": COMPLETE1,
            "blockers": blocker_map, "runtimeSelectionEnabled": False,
            "canonicalApplicationPerformedByOwner": False,
        }
        write(ACC, acceptance)
        write(RCPT, {
            "id": "RANK9-PLANARGATES5-RETURN200-RECEIPT",
            "recordedAtUtc": timestamp,
            "status": "THREE_ACCEPTED_TWO_BLOCKED_INDEPENDENT_AUDIT_PASSED",
            "reviewedIds": GROUP, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "blockers": blocker_map, "directorReturn": archive_binding,
            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
            "sourceAuthority": baseline, "counts": delivery["counts"],
            "decisionId": director["id"],
        })
        write(APPFILE, {
            "id": APP, "recordedAtUtc": timestamp,
            "status": "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS",
            "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.",
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "directorAcceptance": bind(ACC), "directorDecision": bind(DEC),
            "directorReturnReceipt": bind(RCPT), "directorReturn": archive_binding,
            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
            "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
            "manuscript": bind(MAN), "indexBefore": bind(BACKUP, before_raw),
            "countsBefore": BEFORE, "countsAfter": AFTER,
            "completeReviewedStandaloneProcedures": {"before": COMPLETE0, "after": COMPLETE1},
            "sourceStatusPreservedAsBlocked": True, "catalogChanged": False,
            "runtimeSelectionEnabled": False,
        })
        application_binding = bind(APPFILE)

        after = copy.deepcopy(before)
        operations = []
        for pos, sid in enumerate(ACCEPTED):
            index = next(i for i, entry in enumerate(before["entries"]) if entry["id"] == sid)
            old = before["entries"][index]
            new = copy.deepcopy(old)
            new.update({
                "authoredStatus": "reviewed-authored-operational-playtest",
                "procedureFile": "../spell_candidates/rank9planargates5_reviewed_200/MODEL.json",
                "procedurePointer": f"/spells/{pos}/procedure",
                "wholeCardPointer": f"/spells/{pos}",
                "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
                "wholeCardIdField": "id",
                "procedureTextPointer": f"/spells/{pos}/procedure/procedureContent",
                "directorProcedureRecordPointer": f"/spells/{pos}/directorProcedureRecord",
                "sharedRulesPointer": f"/spells/{pos}/procedure/sharedRequirements",
                "manuscript": "../../../docs/spells/candidates/RANK9_PLANAR_GATES5_REVIEWED_200.md",
                "reviewId": APP,
                "runtimeSelectionEnabled": False,
                "historicalCandidateLabelsPreserved": True,
                "completeEvidenceRoot": PKG_REL.as_posix(),
                "completeEnvelopeBinding": model_binding,
                "casebookBinding": casebook_binding,
                "supplementalSourcePackageMap": source_map_bind,
                "casebookEncoding": "Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the director return archive.",
                "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
                "sourceArchiveBinding": archive_binding,
                "deliveryManifestBinding": delivery_binding,
                "candidatePackageManifestBinding": package_manifest_binding,
                "procedureSourceBinding": bind(DEC),
                "authoredAcceptanceReceipt": bind(ACC),
                "authoredApplicationReceipt": application_binding,
            })
            assert old["sourceStatus"] == new["sourceStatus"] == "blocked-pending-operational-review"
            operations.append({"op": "replace-entry", "identity": sid, "index": index,
                              "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
            after["entries"][index] = new
        after["additionalStandaloneEnvelopes"].append({
            "file": "../spell_candidates/rank9planargates5_reviewed_200/MODEL.json",
            "binding": model_binding, "reviewId": REVIEW, "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED, "excludedPendingIds": sorted(live - set(ACCEPTED)),
            "authority": bind(ACC), "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
            "sourceArchive": archive_binding, "deliveryManifest": delivery_binding,
            "casebookBinding": casebook_binding, "candidatePackageManifestBinding": package_manifest_binding,
            "scope": acceptance["status"], "runtimeSelectionEnabled": False,
        })
        after["authoredCounts"] = AFTER
        after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE1
        pending = {entry["id"] for entry in after["entries"]
                   if entry["authoredStatus"] == "pending-authored-procedure"}
        assert pending == live - set(ACCEPTED) and len(pending) == 55
        inverse = copy.deepcopy(after)
        for operation in operations:
            inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
        inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
        inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
        inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
        assert inverse == before
        after_raw = jb(after)
        temporary = INDEX.with_suffix(".json.planargates200.tmp")
        temporary.write_bytes(after_raw)
        temporary.replace(INDEX)
        assert CATALOG.read_bytes() == catalog_raw
        write(OPS, {
            "id": "RANK9-PLANARGATES5-INDEX-OPERATIONS-200",
            "before": bind(BACKUP, before_raw), "after": bind(INDEX, after_raw),
            "operations": operations, "inverseSemanticExact": True, "onlyIdentityIds": ACCEPTED,
        })

        groups = []
        for old_group in q0["currentPendingGroups"]:
            remaining = [sid for sid in old_group["pendingIds"] if sid in pending]
            if not remaining:
                continue
            group = copy.deepcopy(old_group)
            group["pendingIds"] = remaining
            group["pendingCount"] = len(remaining)
            if group["group"] == "rank9-planar-gates5":
                group.update({
                    "status": "PARTIAL_RETURN200_THREE_ACCEPTED_APPLIED_TWO_BLOCKED",
                    "freshPacketRequiredForCurrentAuthority": True,
                    "blockingReturn": {
                        "ids": UNACCEPTED,
                        "blockers": {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED},
                        "receipt": RCPT.relative_to(ROOT).as_posix(),
                    },
                })
            if group["group"] == NEXT:
                group.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
                              "freshPacketRequiredForCurrentAuthority": True})
            groups.append(group)
        next_record = next(group for group in groups if group["group"] == NEXT)
        authority = {
            "reviewedApplied": 793, "pending": 55, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 517, "scopedInterfaces": 173,
        }
        pending_doc = {key: copy.deepcopy(value) for key, value in p0.items()
                       if key.startswith("retainedReturn")}
        pending_doc.update({
            "id": "CURRENT55-PENDING-IDENTITY-AUDIT-200",
            "recordedAtUtc": timestamp,
            "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
            "indexBinding": bind(INDEX, after_raw), "catalogBinding": bind(CATALOG, catalog_raw),
            "authoredCounts": AFTER, "pendingCount": 55, "pendingIds": sorted(pending),
            "allPendingExistInSourceCatalog": pending <= cats, "acceptedUnapplied": 0,
            "retainedReturn200Blockers": {
                sid: {"blockerIds": decisions[sid]["blockerIds"],
                      "reasons": [record["missing"] for record in director["blockers"]
                                  if record["id"] in decisions[sid]["blockerIds"]]}
                for sid in UNACCEPTED
            },
            "closed335AndCompletedCohortsReopened": False,
        })
        assert pending_doc["allPendingExistInSourceCatalog"] is True
        write(P1, pending_doc)
        next_request = {
            "group": NEXT, "pendingIds": next_group["pendingIds"], "pendingCount": 5,
            "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
            "freshPacketRequiredForCurrentAuthority": True,
            "candidate": next_group["candidate"], "archive": next_group["archive"],
        }
        q1 = copy.deepcopy(q0)
        q1.update({
            "id": "SPELL-REVIEW-QUEUE-200", "recordedAtUtc": timestamp,
            "currentAuthority": authority, "pendingCount": 55, "currentPendingGroups": groups,
            "justAppliedBatch": {
                "reviewId": REVIEW, "ids": ACCEPTED, "count": len(ACCEPTED),
                "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
                "directorAcceptance": ACC.relative_to(ROOT).as_posix(),
                "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix(),
            },
            "pendingIdentityAudit": {"path": P1.relative_to(ROOT).as_posix(), "pending": 55,
                                     "sha256": sha(P1.read_bytes())},
            "nextGroup": NEXT, "next": next_request, "nextPreparedRequest": next_request,
            "packetStatus": "RANK9_PLANARGATES5_RETURN200_THREE_APPLIED_TWO_HELD_793_55_NEXT_RANK9_SUMMON_HOSTS5",
            "currentReturnBinding": archive_binding, "currentReturnAudit": audit_binding,
        })
        for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
            q1.pop(key, None)
        q1["currentSubmission"] = bind(RCPT)
        q1["currentSubmissionBinding"] = bind(RCPT)
        write(Q1, q1)
        h1 = copy.deepcopy(h0)
        h1.update({
            "id": "CURRENT-HANDOFF-200", "recordedAtUtc": timestamp,
            "status": "RANK9_PLANARGATES5_THREE_APPLIED_TWO_HELD_NEXT_RANK9_SUMMON_HOSTS5_55_PENDING",
            "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw),
            "currentCatalogBinding": bind(CATALOG, catalog_raw),
            "pendingIdentityAudit": {"id": pending_doc["id"], "path": P1.relative_to(ROOT).as_posix(),
                                     "pendingCount": 55, "sha256": sha(P1.read_bytes())},
            "appliedThisStep": {
                "reviewId": REVIEW, "ids": ACCEPTED, "count": len(ACCEPTED),
                "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
                "directorAcceptance": ACC.relative_to(ROOT).as_posix(),
                "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix(),
                "applicationValidation": {"path": VALID.relative_to(ROOT).as_posix()},
            },
            "unacceptedThisStep": {
                "ids": UNACCEPTED,
                "blockers": {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED},
                "retainedInPendingSet": True,
            },
            "nextGroup": NEXT, "nextPendingCount": 5, "nextPreparedRequest": next_request,
            "currentQueueBinding": bind(Q1), "currentReturnBinding": archive_binding,
            "independentAuditBinding": audit_binding, "parentHandoff": H0.relative_to(ROOT).as_posix(),
            "currentSubmissionBinding": bind(RCPT), "currentReturnAudit": audit_binding,
            "resumePriority": "Prepare a fresh Rank9 Summon Hosts5 packet at 793/55 for GPT; submit, independently audit, apply and push only exact accepted IDs, and continue until pending is zero. Retain the two Planar Gates blockers under PG200-B03/B04 and PG200-B06.",
        })
        for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
            h1.pop(key, None)
        write(H1, h1)
        shutil.copyfile(MAN, AUDIT / "RANK9_PLANARGATES5_REVIEWED_200.md")
        SNAP.write_text(
            "# Current ordinary spell-review checkpoint 200\n\n"
            f"Return200 passed {read(AUDIT_JSON)['checksPassed']} independent checks, including all 125 archive members and all 72 case traces / 4,159 events. Applied exactly {', '.join(ACCEPTED)} as static authored procedures. Banishment Gate remains pending under PG200-B03/B04; Conjure Demiplane Fortress remains pending under PG200-B06. Authority: **793 reviewed / 55 pending / 0 accepted-unapplied**, 517 complete procedures. Next: Rank9 Summon Hosts5. Runtime and downstream approval gates remain disabled.\n",
            encoding="utf-8", newline="\n",
        )
        start = ROOT / "START_HERE.md"
        prior_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
        start.write_text(
            f"**Current ordinary spell-review handoff [200](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_200.json):** Applied exactly {', '.join(ACCEPTED)}. Authority is **793 reviewed / 55 pending / 0 accepted-unapplied**. Banishment Gate remains pending under PG200-B03/B04; Conjure Demiplane Fortress remains pending under PG200-B06. Next group: Rank9 Summon Hosts5.\n\n" + prior_start,
            encoding="utf-8", newline="\n",
        )

        validations = [
            ("Return archive and delivery match the independent audit bindings",
             sha_file(ZIP) == archive_binding["sha256"] and sha_file(DELIVERY) == delivery_binding["sha256"]),
            ("Exactly three director-accepted IDs were applied and both held IDs remain pending",
             [op["identity"] for op in operations] == ACCEPTED and set(UNACCEPTED) <= pending),
            ("Authority advanced from 790/58/514 to 793/55/517",
             after["authoredCounts"] == AFTER
             and after["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE1),
            ("Pending identity set is exactly the previous set minus three acceptances",
             pending == live - set(ACCEPTED)),
            ("Index inverse is exact and catalog bytes are unchanged",
             inverse == before and CATALOG.read_bytes() == catalog_raw),
            ("All staged candidate package files match their manifest",
             all((ROOT / item["path"]).is_file()
                 and (ROOT / item["path"]).stat().st_size == item["bytes"]
                 and sha_file(ROOT / item["path"]) == item["sha256"]
                 for item in package_manifest["files"])),
            ("Next group and all five identities match Return200 handoff",
             q1["nextGroup"] == NEXT and next_record["pendingIds"] == next_group["pendingIds"]
             and next_record["pendingCount"] == 5),
            ("Runtime and downstream approval gates remain disabled",
             all(model[key] is False for key in ("runtimeSelectionEnabled", "runtimeTestsExecuted",
                 "sourceProgramsExecuted", "implementationApproved", "humanPlaytested",
                 "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))),
            ("No closed feat or completed cohort was reopened",
             pending_doc["closed335AndCompletedCohortsReopened"] is False
             and set(ACCEPTED) <= set(p0["pendingIds"])),
        ]
        validation = {
            "id": "RANK9-PLANARGATES5-APPLICATION-VALIDATION-200",
            "recordedAtUtc": timestamp,
            "status": "PASS" if all(item[1] for item in validations) else "FAIL",
            "checksPassed": sum(item[1] for item in validations),
            "checksFailed": sum(not item[1] for item in validations),
            "checks": [{"check": name, "passed": passed} for name, passed in validations],
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "countsBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE0},
            "countsAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE1},
            "indexBefore": bind(BACKUP, before_raw), "indexAfter": bind(INDEX),
            "catalogUnchanged": bind(CATALOG, catalog_raw), "applicationReceipt": bind(APPFILE),
            "independentAudit": bind(AUDIT_JSON), "nextGroup": NEXT,
        }
        write(VALID, validation)
        if validation["status"] != "PASS":
            raise SystemExit("Application validation failed; inspect the validation report.")
        print(json.dumps({
            "status": validation["status"], "checksPassed": validation["checksPassed"],
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "authority": authority, "nextGroup": NEXT, "pendingAudit": P1.relative_to(ROOT).as_posix(),
            "independentAudit": read(AUDIT_JSON)["status"], "candidateManifest": package_manifest_binding,
            "candidateFiles": len(package_manifest["files"]),
        }, indent=2))


if __name__ == "__main__":
    main()
