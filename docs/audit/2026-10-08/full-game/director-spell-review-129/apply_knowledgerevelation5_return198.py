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
RECEIVED = AUDIT / "rank9_knowledgerevelation5_return198_received"
ZIP = RECEIVED / "DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
DELIVERY = RECEIVED / "DD_Rank9_KnowledgeRevelation5_Director_Return198_DELIVERY.json"
AUDIT_JSON = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN198_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
Q0 = AUDIT / "CURRENT_SPELL_QUEUE_197.json"
H0 = AUDIT / "CURRENT_HANDOFF_197.json"
P0 = AUDIT / "CURRENT62_PENDING_IDENTITY_AUDIT_197.json"
BACKUP = AUDIT / "authored_review_index.before_knowledgerevelation5_198.json"
PKG_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198")
PKG = ROOT / PKG_REL
STAGE = PKG.with_name(PKG.name + ".staging")
MAN = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_KNOWLEDGEREVELATION5_REVIEWED_198.md"
ACCEPTED = ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"]
UNACCEPTED = ["faction-omniscience-supreme"]
GROUP = ACCEPTED + UNACCEPTED
NEXT = "rank9-planar-gates5"
NEXT_IDS = ["gate", "absolute-gate", "banishment-gate", "planar-sanctuary", "conjure-demiplane-fortress"]
BEFORE = {"reviewed": 786, "pending": 62}
AFTER = {"reviewed": 790, "pending": 58}
COMPLETE0, COMPLETE1 = 510, 514
REVIEW = "RANK9-KNOWLEDGEREVELATION5-EXACT-AUTHORED-ACCEPTANCE-198"
APP = "RANK9-KNOWLEDGEREVELATION5-APPLICATION-198"
DEC = AUDIT / "RANK9_KNOWLEDGEREVELATION5_DIRECTOR_DECISION_198.json"
ACC = AUDIT / "RANK9_KNOWLEDGEREVELATION5_EXACT_ACCEPTANCE_198.json"
RCPT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN198_RECEIPT.json"
APPFILE = AUDIT / "RANK9_KNOWLEDGEREVELATION5_APPLICATION_198.json"
OPS = AUDIT / "RANK9_KNOWLEDGEREVELATION5_INDEX_OPERATIONS_198.json"
P1 = AUDIT / "CURRENT58_PENDING_IDENTITY_AUDIT_198.json"
Q1 = AUDIT / "CURRENT_SPELL_QUEUE_198.json"
H1 = AUDIT / "CURRENT_HANDOFF_198.json"
VALID = AUDIT / "RANK9_KNOWLEDGEREVELATION5_APPLICATION_VALIDATION_198.json"
SNAP = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_198.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
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
    with archive.open(name, "r") as src, target.open("wb") as dst:
        shutil.copyfileobj(src, dst, 1024 * 1024)


def main() -> None:
    outputs = [BACKUP, MAN, DEC, ACC, RCPT, APPFILE, OPS, P1, Q1, H1, VALID, SNAP]
    assert not PKG.exists() and not STAGE.exists() and all(not p.exists() for p in outputs)
    audit, delivery = read(AUDIT_JSON), read(DELIVERY)
    assert audit["status"] == "PASS" and audit["checksPassed"] == 18 and audit["checksFailed"] == 0
    assert audit["applied"] is False and audit["acceptedIds"] == ACCEPTED and audit["unacceptedIds"] == UNACCEPTED
    assert sha_file(ZIP) == delivery["archive"]["sha256"] == audit["returnArchive"]["sha256"] == "2da202eaab4542d7b3bef90e03e75b5276f8396b8a8e3e535a1245d20d87afca"
    assert ZIP.stat().st_size == delivery["archive"]["bytes"] == 113662026
    assert delivery["applied"] is False and delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED
    baseline = {"reviewedApplied": 786, "pending": 62, "acceptedUnapplied": 0, "completeStandaloneProcedures": 510, "scopedInterfaces": 173}
    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read(INDEX), read(CATALOG)
    q0, h0, p0 = map(read, (Q0, H0, P0))
    rows = {entry["id"]: entry for entry in before["entries"]}
    cats = {entry["id"]: entry for entry in catalog["spells"]}
    live = {entry["id"] for entry in before["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == BEFORE and before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE0
    assert len(live) == 62 and set(GROUP) <= live and set(p0["pendingIds"]) == live
    assert p0["indexBinding"]["sha256"] == sha(before_raw)
    assert q0["currentAuthority"] == baseline and q0["pendingCount"] == 62
    assert h0["currentAuthority"] == baseline and h0["status"] == "RANK9_KNOWLEDGE_REVELATION5_PACKET_197_SUBMITTED_AWAITING_GPT_RETURN_786_62"
    assert all(rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in GROUP)
    timestamp = datetime.now(timezone.utc).isoformat()

    with zipfile.ZipFile(ZIP) as archive:
        director = json.loads(archive.read("DIRECTOR_DECISION.json"))
        model_src = json.loads(archive.read("MODEL.json"))
        next_queue = json.loads(archive.read("NEXT_QUEUE_GROUP.json"))["nextExactGroupUnchanged"]
        decisions = {entry["id"]: entry for entry in director["perIdentity"]}
        model_spells = {entry["id"]: entry for entry in model_src["spells"]}
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        new_holds = hold_register["newHolds"]
        assert director["acceptedIds"] == ACCEPTED and director["unacceptedIds"] == UNACCEPTED
        assert director["authorityBaselineUnchanged"] == baseline
        assert director["nextGroup"] == NEXT and next_queue["group"] == NEXT and next_queue["pendingIds"] == NEXT_IDS
        assert set(decisions) == set(model_spells) == set(GROUP)
        assert all(decisions[s]["accepted"] and not decisions[s]["applied"] and not decisions[s]["blockerIds"] for s in ACCEPTED)
        assert all(not decisions[s]["accepted"] and not decisions[s]["applied"] and decisions[s]["blockerIds"] for s in UNACCEPTED)
        assert all(model_spells[s]["accepted"] and not model_spells[s]["applied"] for s in ACCEPTED)
        assert all(not model_spells[s]["accepted"] and not model_spells[s]["applied"] for s in UNACCEPTED)
        assert model_src["applied"] is False and model_src["acceptedIds"] == ACCEPTED and model_src["unacceptedIds"] == UNACCEPTED
        for spell_id in GROUP:
            assert model_spells[spell_id]["sourceEnvelopeUnchanged"]["currentIndexEntry"] == {
                "id": spell_id,
                "name": rows[spell_id]["name"],
                "authoredStatus": "pending-authored-procedure",
                "procedureFile": "catalog.json",
                "procedurePointer": None,
                "wholeCardPointer": rows[spell_id]["wholeCardPointer"],
                "sourceStatus": "blocked-pending-operational-review",
                "priorCatalogSelectionStatusUnchanged": True,
            }
        prior_packet = q0["nextPreparedRequest"]["packet"]
        assert prior_packet["sha256"] == "a55e76efc14e2dc43f4e2b16ff3d176ac65ee33b0d5aee53fdf624cd4b674c04"

        stage_allow = {"CASEBOOK.json"}
        STAGE.mkdir(parents=True)
        for name in archive.namelist():
            if name.endswith("/") or name in stage_allow or name.startswith(("cases/", "additional_sources/", "source_packet/")):
                continue
            copy_member(archive, name, STAGE / name)

        source_map = []
        for pos, binding in enumerate(json.loads(archive.read("ADDITIONAL_SOURCE_BINDINGS.json"))["bindings"]):
            member = "additional_sources/" + binding["path"]
            short = f"{pos:02d}_{binding['sha256'][:12]}_{binding['path'].rsplit('/', 1)[-1]}"
            target = STAGE / "supplemental_sources" / short
            copy_member(archive, member, target)
            raw = target.read_bytes()
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
            source_map.append({"sourcePath": binding["path"], "packagePath": (PKG_REL / "supplemental_sources" / short).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
        write(STAGE / "SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json", {"sourceCommit": audit["sourceCommit"], "count": len(source_map), "sources": source_map})
        source_map_bind = bind(STAGE / "SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json")
        with archive.open("CASEBOOK.json", "r") as src, (STAGE / "CASEBOOK.json.gz").open("wb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0, compresslevel=6) as gz:
                shutil.copyfileobj(src, gz, 1024 * 1024)
        (STAGE / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGE / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(AUDIT_JSON.read_bytes())
        arc_bind, del_bind, audit_bind = bind(ZIP), bind(DELIVERY), bind(AUDIT_JSON)
        packet_bind = {"path": prior_packet["path"], "bytes": prior_packet["bytes"], "sha256": prior_packet["sha256"]}
        case_dispositions = json.loads(archive.read("CASE_DISPOSITIONS.json"))
        case_ids = {sid: list(model_spells[sid]["caseIds"]) for sid in GROUP}
        accepted_case_ids = {case for sid in ACCEPTED for case in case_ids[sid]}
        accepted_events = 0
        for sid in ACCEPTED:
            for case_id in case_ids[sid]:
                member = "cases/" + case_id.replace("/", "__") + ".json"
                case = json.loads(archive.read(member))
                accepted_events += len(case.get("events", []))

        spells = []
        for pos, sid in enumerate(ACCEPTED):
            spell = model_spells[sid]
            native = copy.deepcopy(spell["nativeCardUnchanged"])
            assert native["id"] == sid and native["status"] == "blocked-pending-operational-review"
            spells.append({
                "id": sid,
                "name": rows[sid]["name"],
                "position": pos,
                "procedure": {
                    "id": "KR198-STATIC-" + sid.upper().replace("-", "_"),
                    "spellId": sid,
                    "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                    "accepted": True,
                    "applied": False,
                    "nativeCardUnchanged": native,
                    "procedureContent": copy.deepcopy(spell["procedureContent"]),
                    "sharedRequirements": copy.deepcopy(spell["commonProcedure"]),
                    "newChoices": copy.deepcopy(spell["procedureContent"].get("selection")),
                    "qualifications": {
                        "source": spell["sourceQualification"],
                        "decision": spell["decisionQualification"],
                        "futureObligations": copy.deepcopy(spell["futureObligations"]),
                        "futureDispositions": copy.deepcopy(spell["futureDispositions"]),
                        "retainedHolds": copy.deepcopy(spell["holds"]),
                    },
                    "caseIds": case_ids[sid],
                    "questionIds": sorted({q["id"] for q in spell["questionDispositions"]}),
                    "holdIds": copy.deepcopy(spell["holds"]),
                    "directorDecisionId": director["id"],
                },
                "directorProcedureRecord": copy.deepcopy(spell),
                "nativeCardUnchanged": native,
                "caseIds": case_ids[sid],
                "questionIds": sorted({q["id"] for q in spell["questionDispositions"]}),
                "holdIds": copy.deepcopy(spell["holds"]),
                "runtimeSelectionEnabled": False,
            })
        blocker_map = {}
        for sid in UNACCEPTED:
            records = [copy.deepcopy(h) for h in new_holds if sid in h.get("spellIds", []) and h.get("blocking")]
            blocker_map[sid] = {"blockerIds": decisions[sid]["blockerIds"], "holdIds": copy.deepcopy(model_spells[sid]["holds"]), "blockerRecords": records}
            assert records and blocker_map[sid]["blockerIds"] == [record["id"] for record in records]

        model = {
            "schemaVersion": 1,
            "moduleId": "rank9knowledgerevelation5-reviewed-198",
            "status": "FOUR_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_ONE_BLOCKER",
            "scope": "Only the four individually accepted static procedures are applied. Faction Omniscience Supreme remains pending under KR198-B01. Native cards, source/access status and class routes remain unchanged; runtime and downstream approval gates stay disabled.",
            "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED,
            "excludedPendingIds": sorted(live - set(ACCEPTED)),
            "unacceptedHolds": blocker_map,
            "inheritedNamedBlockers": director["carriedNamedBlockersUnchanged"],
            "sharedRequirements": {"scope": "No global/shared rule changes; native cards and class routes unchanged.", "runtimeSelectionEnabled": False},
            "spells": spells,
            "caseCoverage": {"caseCount": sum(len(v) for v in case_ids.values()), "acceptedCaseCount": len(accepted_case_ids), "acceptedEventCount": accepted_events, "caseDispositionsBinding": next(x for x in delivery["allOuterMembersIncludingManifest"] if x["path"] == "CASE_DISPOSITIONS.json")},
            "returnCounts": delivery["counts"],
            "sourceArchive": arc_bind,
            "deliveryManifest": del_bind,
            "independentAudit": audit_bind,
            "submittedSourcePacket": packet_bind,
            "casebookFile": "CASEBOOK.json.gz",
            "casebookSourceArchiveMemberBinding": next(x for x in delivery["allOuterMembersIncludingManifest"] if x["path"] == "CASEBOOK.json"),
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
        pkg_manifest = {"id": "RANK9-KNOWLEDGEREVELATION5-PACKAGE-MANIFEST-198", "sourceArchive": arc_bind, "deliveryManifest": del_bind, "independentAudit": audit_bind, "sourceAnchorCommit": audit["sourceCommit"], "files": []}
        for file in sorted(path for path in STAGE.rglob("*") if path.is_file()):
            raw = file.read_bytes()
            pkg_manifest["files"].append({"path": (PKG_REL / file.relative_to(STAGE)).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
        write(STAGE / "CANDIDATE_PACKAGE_MANIFEST.json", pkg_manifest)
        shutil.move(str(STAGE), str(PKG))
        model_bind = bind(PKG / "MODEL.json")
        manifest_bind = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
        casebook_bind = bind(PKG / "CASEBOOK.json.gz")
        MAN.parent.mkdir(parents=True, exist_ok=True)
        MAN.write_bytes((PKG / "STANDALONE_PROCEDURES.md").read_bytes())
        shutil.copyfile(INDEX, BACKUP)
        assert BACKUP.read_bytes() == before_raw

        write(DEC, {"id": director["id"], "recordedAtUtc": timestamp, "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "blockers": blocker_map, "directorReturn": arc_bind, "deliveryManifest": del_bind, "independentAudit": audit_bind, "authorityAtDecision": baseline, "exactDirectorDecisions": director["perIdentity"], "inheritedNamedBlockersCarriedForward": director["carriedNamedBlockersUnchanged"], "scope": "Static authorship only; no runtime, implementation, human-play, balance, cosmology, domain closure, completion or release approval.", "canonicalFilesChangedByDirector": False})
        acceptance = {"id": REVIEW, "recordedAtUtc": timestamp, "status": "FOUR_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_ONE_RETAINED_BLOCKER", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "directorDecision": bind(DEC), "directorReturn": arc_bind, "deliveryManifest": del_bind, "independentAudit": audit_bind, "candidateEnvelope": model_bind, "candidatePackageManifest": manifest_bind, "countsBefore": BEFORE, "countsAfter": AFTER, "completeReviewedStandaloneProceduresBefore": COMPLETE0, "completeReviewedStandaloneProceduresAfter": COMPLETE1, "blockers": blocker_map, "runtimeSelectionEnabled": False, "canonicalApplicationPerformedByOwner": False}
        write(ACC, acceptance)
        write(RCPT, {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN198-RECEIPT", "recordedAtUtc": timestamp, "status": "FOUR_ACCEPTED_ONE_BLOCKED_INDEPENDENT_AUDIT_PASSED", "reviewedIds": GROUP, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "blockers": blocker_map, "inheritedNamedBlockers": director["carriedNamedBlockersUnchanged"], "directorReturn": arc_bind, "deliveryManifest": del_bind, "independentAudit": audit_bind, "sourceAuthority": baseline, "counts": delivery["counts"], "decisionId": director["id"]})
        write(APPFILE, {"id": APP, "recordedAtUtc": timestamp, "status": "APPLIED_FOUR_EXACT_AUTHORED_PROCEDURES_WITH_ONE_RETAINED_BLOCKER", "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "directorAcceptance": bind(ACC), "directorDecision": bind(DEC), "directorReturnReceipt": bind(RCPT), "directorReturn": arc_bind, "deliveryManifest": del_bind, "independentAudit": audit_bind, "candidateEnvelope": model_bind, "candidatePackageManifest": manifest_bind, "manuscript": bind(MAN), "indexBefore": bind(BACKUP, before_raw), "countsBefore": BEFORE, "countsAfter": AFTER, "completeReviewedStandaloneProcedures": {"before": COMPLETE0, "after": COMPLETE1}, "sourceStatusPreservedAsBlocked": True, "catalogChanged": False, "runtimeSelectionEnabled": False})
        app_bind = bind(APPFILE)

        after = copy.deepcopy(before)
        operations = []
        for pos, sid in enumerate(ACCEPTED):
            index = next(i for i, entry in enumerate(before["entries"]) if entry["id"] == sid)
            old = before["entries"][index]
            new = copy.deepcopy(old)
            new.update({
                "authoredStatus": "reviewed-authored-operational-playtest",
                "procedureFile": "../spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json",
                "procedurePointer": f"/spells/{pos}/procedure",
                "wholeCardPointer": f"/spells/{pos}",
                "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
                "wholeCardIdField": "id",
                "procedureTextPointer": f"/spells/{pos}/procedure/procedureContent",
                "directorProcedureRecordPointer": f"/spells/{pos}/directorProcedureRecord",
                "sharedRulesPointer": f"/spells/{pos}/procedure/sharedRequirements",
                "manuscript": "../../../docs/spells/candidates/RANK9_KNOWLEDGEREVELATION5_REVIEWED_198.md",
                "reviewId": APP,
                "runtimeSelectionEnabled": False,
                "historicalCandidateLabelsPreserved": True,
                "completeEvidenceRoot": PKG_REL.as_posix(),
                "completeEnvelopeBinding": model_bind,
                "casebookBinding": casebook_bind,
                "supplementalSourcePackageMap": source_map_bind,
                "casebookEncoding": "Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the director return archive.",
                "casebookSourceArchiveMemberBinding": model["casebookSourceArchiveMemberBinding"],
                "sourceArchiveBinding": arc_bind,
                "deliveryManifestBinding": del_bind,
                "candidatePackageManifestBinding": manifest_bind,
                "procedureSourceBinding": bind(DEC),
                "authoredAcceptanceReceipt": bind(ACC),
                "authoredApplicationReceipt": app_bind,
            })
            assert old["sourceStatus"] == new["sourceStatus"] == "blocked-pending-operational-review"
            operations.append({"op": "replace-entry", "identity": sid, "index": index, "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
            after["entries"][index] = new
        after["additionalStandaloneEnvelopes"].append({"file": "../spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json", "binding": model_bind, "reviewId": REVIEW, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "excludedPendingIds": sorted(live - set(ACCEPTED)), "authority": bind(ACC), "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(), "sourceArchive": arc_bind, "deliveryManifest": del_bind, "casebookBinding": casebook_bind, "candidatePackageManifestBinding": manifest_bind, "scope": acceptance["status"], "runtimeSelectionEnabled": False})
        after["authoredCounts"] = AFTER
        after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE1
        pending = {entry["id"] for entry in after["entries"] if entry["authoredStatus"] == "pending-authored-procedure"}
        assert pending == live - set(ACCEPTED) and len(pending) == 58
        inverse = copy.deepcopy(after)
        for op in operations:
            inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
        inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
        inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
        inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
        assert inverse == before
        after_raw = jb(after)
        tmp = INDEX.with_suffix(".json.knowledgerevelation198.tmp")
        tmp.write_bytes(after_raw)
        tmp.replace(INDEX)
        assert CATALOG.read_bytes() == catalog_raw
        write(OPS, {"id": "RANK9-KNOWLEDGEREVELATION5-INDEX-OPERATIONS-198", "before": bind(BACKUP, before_raw), "after": bind(INDEX, after_raw), "operations": operations, "inverseSemanticExact": True, "onlyIdentityIds": ACCEPTED})

        groups = []
        for old_group in q0["currentPendingGroups"]:
            left = [sid for sid in old_group["pendingIds"] if sid in pending]
            if not left:
                continue
            group = copy.deepcopy(old_group)
            group["pendingIds"] = left
            group["pendingCount"] = len(left)
            if group["group"] == "rank9-knowledge-revelation5":
                group.update({"status": "PARTIAL_RETURN198_FOUR_ACCEPTED_APPLIED_ONE_BLOCKED", "freshPacketRequiredForCurrentAuthority": True, "blockingReturn": {"ids": UNACCEPTED, "blockers": {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED}, "receipt": RCPT.relative_to(ROOT).as_posix()}})
            if group["group"] == NEXT:
                group.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True})
            groups.append(group)
        next_group = next(group for group in groups if group["group"] == NEXT)
        authority = {"reviewedApplied": 790, "pending": 58, "acceptedUnapplied": 0, "completeStandaloneProcedures": 514, "scopedInterfaces": 173}
        pending_doc = {key: copy.deepcopy(value) for key, value in p0.items() if key.startswith("retainedReturn")}
        pending_doc.update({"id": "CURRENT58-PENDING-IDENTITY-AUDIT-198", "recordedAtUtc": timestamp, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX, after_raw), "catalogBinding": bind(CATALOG, catalog_raw), "authoredCounts": AFTER, "pendingCount": 58, "pendingIds": sorted(pending), "allPendingExistInSourceCatalog": pending <= set(cats), "acceptedUnapplied": 0, "retainedReturn198Blockers": {sid: {"blockerIds": decisions[sid]["blockerIds"], "holdIds": model_spells[sid]["holds"], "reason": next(h["missing"] for h in new_holds if sid in h.get("spellIds", []))} for sid in UNACCEPTED}, "closed335AndCompletedCohortsReopened": False})
        write(P1, pending_doc)
        next_req = {"group": NEXT, "pendingIds": NEXT_IDS, "pendingCount": 5, "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY", "freshPacketRequiredForCurrentAuthority": True, "candidate": next_group.get("candidate"), "archive": next_group.get("archive")}
        q1 = copy.deepcopy(q0)
        q1.update({"id": "SPELL-REVIEW-QUEUE-198", "recordedAtUtc": timestamp, "currentAuthority": authority, "pendingCount": 58, "currentPendingGroups": groups, "justAppliedBatch": {"reviewId": REVIEW, "ids": ACCEPTED, "count": 4, "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(), "directorAcceptance": ACC.relative_to(ROOT).as_posix(), "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix()}, "pendingIdentityAudit": {"path": P1.relative_to(ROOT).as_posix(), "pending": 58, "sha256": sha(P1.read_bytes())}, "nextGroup": NEXT, "next": next_req, "nextPreparedRequest": next_req, "packetStatus": "RANK9_KNOWLEDGEREVELATION5_RETURN198_FOUR_APPLIED_ONE_HELD_790_58_NEXT_RANK9_PLANAR_GATES5", "currentReturnBinding": arc_bind, "currentReturnAudit": audit_bind})
        for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
            q1.pop(key, None)
        q1["currentSubmission"] = bind(RCPT)
        q1["currentSubmissionBinding"] = bind(RCPT)
        write(Q1, q1)
        h1 = copy.deepcopy(h0)
        h1.update({"id": "CURRENT-HANDOFF-198", "recordedAtUtc": timestamp, "status": "RANK9_KNOWLEDGEREVELATION5_FOUR_APPLIED_ONE_HELD_NEXT_RANK9_PLANAR_GATES5_58_PENDING", "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw), "currentCatalogBinding": bind(CATALOG, catalog_raw), "pendingIdentityAudit": {"id": pending_doc["id"], "path": P1.relative_to(ROOT).as_posix(), "pendingCount": 58, "sha256": sha(P1.read_bytes())}, "appliedThisStep": {"reviewId": REVIEW, "ids": ACCEPTED, "count": 4, "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(), "directorAcceptance": ACC.relative_to(ROOT).as_posix(), "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix(), "applicationValidation": {"path": VALID.relative_to(ROOT).as_posix()}}, "unacceptedThisStep": {"ids": UNACCEPTED, "blockers": {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED}, "retainedInPendingSet": True}, "nextGroup": NEXT, "nextPendingCount": 5, "nextPreparedRequest": next_req, "currentQueueBinding": bind(Q1), "currentReturnBinding": arc_bind, "independentAuditBinding": audit_bind, "parentHandoff": H0.relative_to(ROOT).as_posix(), "currentSubmissionBinding": bind(RCPT), "currentReturnAudit": audit_bind, "resumePriority": "Prepare a fresh Rank9 Planar Gates5 packet at 790/58 for GPT; submit, independently audit, apply and push only exact accepted IDs, and continue until pending is zero."})
        for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
            h1.pop(key, None)
        write(H1, h1)
        shutil.copyfile(MAN, AUDIT / "RANK9_KNOWLEDGEREVELATION5_REVIEWED_198.md")
        SNAP.write_text("# Current ordinary spell-review checkpoint 198\n\n" f"Return198 passed {audit['checksPassed']} independent checks, including all 77 cases, {delivery['counts']['events']} events, and exact reversible event/state verification. Applied exactly {', '.join(ACCEPTED)} as static authored procedures. Faction Omniscience Supreme remains pending under KR198-B01. Authority: **790 reviewed / 58 pending / 0 accepted-unapplied**, 514 complete procedures. Next: Rank9 Planar Gates5. Runtime and downstream approval gates remain disabled.\n", encoding="utf-8", newline="\n")
        start = ROOT / "START_HERE.md"
        old_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
        start.write_text(f"**Current ordinary spell-review handoff [198](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_198.json):** Applied exactly {', '.join(ACCEPTED)}. Authority is **790 reviewed / 58 pending / 0 accepted-unapplied**. Faction Omniscience Supreme remains pending under KR198-B01. Next group: Rank9 Planar Gates5.\n\n" + old_start, encoding="utf-8", newline="\n")

        checks = [
            {"check": "Return archive, delivery manifest, and independent audit bindings match", "passed": audit["status"] == "PASS" and sha_file(ZIP) == arc_bind["sha256"] and sha_file(DELIVERY) == del_bind["sha256"]},
            {"check": "Exactly four accepted IDs applied; faction omniscience remains pending", "passed": [op["identity"] for op in operations] == ACCEPTED and set(UNACCEPTED) <= pending},
            {"check": "Authority advanced 786/62/510 to 790/58/514", "passed": after["authoredCounts"] == AFTER and after["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE1},
            {"check": "Pending set is exact prior set minus four acceptances", "passed": pending == live - set(ACCEPTED)},
            {"check": "Index inverse restores original index and canonical catalog is byte-identical", "passed": inverse == before and CATALOG.read_bytes() == catalog_raw},
            {"check": "Every candidate package file matches its manifest binding", "passed": all((ROOT / entry["path"]).is_file() and (ROOT / entry["path"]).stat().st_size == entry["bytes"] and sha_file(ROOT / entry["path"]) == entry["sha256"] for entry in pkg_manifest["files"])},
            {"check": "Next group and all five IDs match GPT director instructions", "passed": q1["nextGroup"] == NEXT and next_group["pendingIds"] == NEXT_IDS},
            {"check": "Runtime and downstream gates remain disabled", "passed": all(model[key] is False for key in ("runtimeSelectionEnabled", "runtimeTestsExecuted", "sourceProgramsExecuted", "implementationApproved", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))},
            {"check": "No closed feat or completed cohort was reopened", "passed": pending_doc["closed335AndCompletedCohortsReopened"] is False and set(ACCEPTED) <= set(p0["pendingIds"])},
        ]
        validation = {"id": "RANK9-KNOWLEDGEREVELATION5-APPLICATION-VALIDATION-198", "recordedAtUtc": timestamp, "status": "PASS" if all(check["passed"] for check in checks) else "FAIL", "checksPassed": sum(check["passed"] for check in checks), "checksFailed": sum(not check["passed"] for check in checks), "checks": checks, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "countsBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE0}, "countsAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE1}, "indexBefore": bind(BACKUP, before_raw), "indexAfter": bind(INDEX), "catalog": bind(CATALOG), "application": bind(APPFILE), "independentAudit": audit_bind, "pendingIdentityAudit": bind(P1), "queueAfter": bind(Q1), "handoffAfter": bind(H1), "nextGroup": NEXT, "runtimeSelectionEnabled": False}
        write(VALID, validation)
        assert validation["status"] == "PASS", checks
        print(json.dumps({"status": "APPLIED_AND_VALIDATED", "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED, "authority": authority, "nextGroup": NEXT, "independentAudit": audit["status"], "validation": validation["status"], "indexSha256": sha_file(INDEX), "candidateManifest": manifest_bind, "candidateFiles": len(pkg_manifest["files"])}, indent=2))


if __name__ == "__main__":
    main()
