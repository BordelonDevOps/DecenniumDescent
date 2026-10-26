from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUD = FULL / "director-spell-review-129"
IDS = ["cataclysmic-conjuration", "elemental-apocalypse", "planar-overload", "armageddon", "cataclysm", "arcane-apocalypse", "meteor-swarm", "starfire-core", "ragnarok", "final-spark"]
OLD_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_01.json"
OLD_ARCHIVE = FULL / "DD_Rank9_Catastrophe_10_Source_Conference_01.zip"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUD / "CURRENT_SPELL_QUEUE_170.json"
HANDOFF = AUD / "CURRENT_HANDOFF_170.json"
PENDING = AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_170.json"
LATEST = [
    AUD / "REMAINING4_APPLICATION_170.json",
    AUD / "REMAINING4_EXACT_ACCEPTANCE_169.json",
    AUD / "REMAINING4_APPLICATION_VALIDATION_170.json",
    AUD / "REMAINING4_GPT_RETURN_169.json",
    AUD / "GPT_DIRECTOR_DECISION_REMAINING4_169.json",
    ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8remaining4_reviewed_169/MODEL.json",
]
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_02.json"
OUTPUT = FULL / "rank9-catastrophe10-source-conference-02-171"
ARCHIVE = FULL / "DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
CHECK = FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_CHECK_171.json"
PREP = FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_PREPARATION_171.json"
REQUEST = FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_REQUEST_171.txt"
PENDING_AFTER = AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_171.json"
QUEUE_AFTER = AUD / "CURRENT_SPELL_QUEUE_171.json"
HANDOFF_AFTER = AUD / "CURRENT_HANDOFF_171.json"
AUTH = {"reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173}


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bind(path: Path, rel: str | None = None):
    raw = path.read_bytes()
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def resolve_pointer(obj, pointer: str):
    current = obj
    for part in pointer.strip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def main():
    assert not any(p.exists() for p in [CANDIDATE, OUTPUT, ARCHIVE, CHECK, PREP, REQUEST, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER])
    index_bytes, catalog_bytes = INDEX.read_bytes(), CATALOG.read_bytes()
    index, catalog, queue, handoff, pending = map(read, [INDEX, CATALOG, QUEUE, HANDOFF, PENDING])
    old_archive_raw = OLD_ARCHIVE.read_bytes()
    assert sha(old_archive_raw) == "c638dd2a85617789d73864346c2a55820e84edb342a2cb7d7c90537dc5f954c4"
    with zipfile.ZipFile(OLD_ARCHIVE) as old_zip:
        assert old_zip.testzip() is None
        old_raw = old_zip.read("CANDIDATE.json")
        old_manifest_raw = old_zip.read("MANIFEST.json")
        old_check_raw = old_zip.read("SOURCE_CHECK.json")
        old_readme_raw = old_zip.read("README.md")
    assert sha(old_raw) == "6b4e527001845b7d336363cb25e728c494247ae8bc10c982068f9fbf717ce771"
    old = json.loads(old_raw.decode("utf-8-sig"))
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTH
    assert pending["authoredCounts"] == {"reviewed": 739, "pending": 109}
    assert queue["nextGroup"] == "rank9-catastrophe10" and queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert pending["pendingCount"] == 109
    live_pending = {r["id"] for r in index["entries"] if r["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 109 and set(pending["pendingIds"]) == live_pending and set(IDS) <= live_pending
    assert index["authoredCounts"] == {"reviewed": 739, "pending": 109}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 463
    assert len(old["records"]) == 10 and [r["spellId"] for r in old["records"]] == IDS
    assert len(old["questions"]) == 25 and all(not q["decisionSelected"] for q in old["questions"])
    assert sum(len(r["completeCurrentBookBindings"]) for r in old["records"]) == 12

    index_by = {r["id"]: r for r in index["entries"]}
    catalog_by = {r["id"]: r for r in catalog["spells"]}
    group = copy.deepcopy(queue["currentPendingGroups"][0])
    assert group["pendingCount"] == 10

    # Refresh every source named by the historical source conference to current repository bytes.
    source_paths = {row["path"] for row in old["sourceBindings"]}
    current_authority_paths = {
        INDEX.relative_to(ROOT).as_posix(), CATALOG.relative_to(ROOT).as_posix(),
        QUEUE.relative_to(ROOT).as_posix(), HANDOFF.relative_to(ROOT).as_posix(),
        PENDING.relative_to(ROOT).as_posix(),
        *[p.relative_to(ROOT).as_posix() for p in LATEST],
    }
    source_paths |= current_authority_paths
    for rel in source_paths:
        assert (ROOT / rel).is_file(), f"Missing live packet source: {rel}"
    source_bindings = [bind(ROOT / rel, rel) for rel in sorted(source_paths)]
    old_source_bindings = copy.deepcopy(old["sourceBindings"])

    candidate = copy.deepcopy(old)
    now = datetime.now(timezone.utc).isoformat()
    candidate.update({
        "id": "RANK9-CATASTROPHE10-SOURCE-CONFERENCE02-171",
        "recordedAtUtc": now,
        "status": "FRESH_SOURCE_CONFERENCE_PREPARED_UNSENT",
        "developmentDirection": "Fresh source context bound to the current 739 applied-reviewed / 109 pending / 0 accepted-unapplied authority. Conference01 and its 525/323 baselines are preserved as historical evidence only.",
        "supersedes": "This Conference02 packet is the current authority for the exact ten Catastrophe identities. All current index, catalog, current queue, current handoff and pending-audit bindings are refreshed to 739/109. The prior Conference01 packet remains byte-exact historical context only.",
        "currentAuthority": {**AUTH, "index": bind(INDEX), "catalog": bind(CATALOG), "currentQueue": bind(QUEUE), "currentHandoff": bind(HANDOFF), "pendingIdentityAudit": bind(PENDING), "latestApplication": bind(LATEST[0]), "latestExactAcceptance": bind(LATEST[1]), "latestApplicationValidation": bind(LATEST[2]), "latestDirectorReturnReceipt": bind(LATEST[3])},
        "countsUnchanged": {"reviewed": 739, "pending": 109, "acceptedUnapplied": 0},
        "historicalConference01": {"authority": old["countsUnchanged"], "candidate": {"path": OLD_CANDIDATE.relative_to(ROOT).as_posix(), "bytes": len(old_raw), "sha256": sha(old_raw)}, "archive": bind(OLD_ARCHIVE), "qualification": "Exact 525/323 source-conference history only. It is superseded by current Conference02 authority and does not determine present acceptance counts."},
        "historicalSourceBindingsConference01": old_source_bindings,
        "sourceBindings": source_bindings,
        "currentPendingIds": IDS,
        "currentQueueGroup": group,
        "currentPendingIdentityAudit": {"id": pending["id"], **bind(PENDING), "pendingCount": 109, "pendingIds": pending["pendingIds"]},
        "currentAcceptedBatchSinceConference01": {"ids": read(LATEST[1])["acceptedIds"], "application": bind(LATEST[0]), "acceptance": bind(LATEST[1]), "validation": bind(LATEST[2]), "decisionReceipt": bind(LATEST[3]), "scope": "Four exact Rank8 procedures applied; all stated runtime/source/content/lifecycle/hold boundaries remain in effect."},
        "priorConferenceQuestionSetPreserved": {"questionCount": 25, "allStillUnselected": True},
        "gptCommunication": "Fresh rank9-catastrophe10 packet for current 739 applied-reviewed / 109 pending / 0 accepted-unapplied authority. Review exactly cataclysmic-conjuration, elemental-apocalypse, planar-overload, armageddon, cataclysm, arcane-apocalypse, meteor-swarm, starfire-core, ragnarok, and final-spark. Preserve and resolve all 25 original source questions. Return full source-faithful procedures, questions, cases, branches, explicit accepted IDs, exact blockers, retained holds, and semantic failure checks. Do not change canonical data. Do not reopen any applied spell cohort or the closed feat review.",
        "newRuleAdoptions": 0, "runtimeTestsExecuted": 0, "humanPlaytests": 0, "sourceInformationDeleted": 0, "cosmologyDecisions": 0, "wholeGameComplete": False,
    })
    for record in candidate["records"]:
        sid = record["spellId"]
        assert record["completeCurrentCatalogSourceAndAccess"] == catalog_by[sid], f"Native card/access changed for {sid}; resolve source drift before sending."
        assert index_by[sid]["authoredStatus"] == "pending-authored-procedure"
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(catalog_by[sid])
        record["currentIndexEntry"] = copy.deepcopy(index_by[sid])
        record["currentQueueStatus"] = {"identity": sid, "group": "rank9-catastrophe10", "pending": True, "reviewedApplied": 739, "pendingCount": 109}
        record["status"] = "Fresh Conference02 source context; all decisions remain unselected."

    # Refresh embedded current accepted counterparts and interface registry records.
    for counterpart in candidate["completeAppliedCounterparts"]:
        sid = counterpart["spellId"]
        entry = index_by[sid]
        env_path = (INDEX.parent / entry["procedureFile"]).resolve()
        envelope = read(env_path)
        pointer = entry.get("wholeCardPointer") or entry["procedurePointer"]
        counterpart["source"] = bind(env_path)
        counterpart["pointer"] = pointer
        counterpart["completeCurrentCard"] = copy.deepcopy(resolve_pointer(envelope, pointer))
        shared = entry.get("sharedRulesPointer")
        counterpart["completeSharedRules"] = copy.deepcopy(resolve_pointer(envelope, shared) if shared else envelope.get("sharedRules", {}))
        counterpart["indexEntry"] = copy.deepcopy(entry)
    registry_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
    registry = read(registry_path)
    for interface in candidate["currentAcceptedInterfaceComparisons"]:
        pointer = interface["registryPointer"]
        number = int(pointer.split("/")[-1])
        interface["completeEntryUnchanged"] = copy.deepcopy(registry["entries"][number])

    # Refresh embedded current cosmology document bindings by their repository paths.
    for row in candidate["completeCosmologySourcesAndAuthority"]:
        old_bind = row.get("source") or row.get("binding")
        if isinstance(old_bind, dict) and old_bind.get("path"):
            live_path = ROOT / old_bind["path"]
            if live_path.is_file():
                row["source"] = bind(live_path)

    assert set().union(*(set(q["spellIds"]) for q in candidate["questions"])) == set(IDS)
    assert len(candidate["questions"]) == 25 and all(not q["decisionSelected"] for q in candidate["questions"])
    assert candidate["currentPendingIds"] == IDS and candidate["countsUnchanged"] == {"reviewed": 739, "pending": 109, "acceptedUnapplied": 0}
    candidate_raw = enc(candidate)
    write(CANDIDATE, candidate_raw)

    request_text = f"""GPT — review the attached fresh Rank9 Catastrophe10 Conference02 packet against the current GitHub branch.\n\nAuthority: 739 applied-reviewed / 109 pending / 0 accepted-unapplied; 463 complete standalone procedures; 173 scoped interfaces.\nExact scope: {', '.join(IDS)} only.\n\nResolve every one of the 25 preserved source questions. Return complete source-faithful procedures, selected question dispositions, full cases and branches with reversible event/state evidence, explicit accepted IDs, exact unresolved blockers, retained holds, and an independent semantic-failure check. Preserve current native source/access and all relevant accepted-interface boundaries. Keep runtime, human-play, balance, cosmology, domain-closure, and release approval separate. Do not edit canonical files, alter the index, reopen applied spell cohorts, or reopen the closed feat review. Mark accepted=true and applied=false only for the exact IDs that pass.\n"""
    write(REQUEST, request_text.encode("utf-8"))
    output_files: list[Path] = []
    write(OUTPUT / "CANDIDATE.json", candidate_raw); output_files.append(OUTPUT / "CANDIDATE.json")
    write(OUTPUT / "REQUEST.txt", request_text.encode("utf-8")); output_files.append(OUTPUT / "REQUEST.txt")
    write(OUTPUT / "historical/Conference01_ARCHIVE.zip", old_archive_raw); output_files.append(OUTPUT / "historical/Conference01_ARCHIVE.zip")
    write(OUTPUT / "historical/Conference01_CANDIDATE.json", old_raw); output_files.append(OUTPUT / "historical/Conference01_CANDIDATE.json")
    write(OUTPUT / "historical/Conference01_MANIFEST.json", old_manifest_raw); output_files.append(OUTPUT / "historical/Conference01_MANIFEST.json")
    write(OUTPUT / "historical/Conference01_SOURCE_CHECK.json", old_check_raw); output_files.append(OUTPUT / "historical/Conference01_SOURCE_CHECK.json")
    write(OUTPUT / "historical/Conference01_README.md", old_readme_raw); output_files.append(OUTPUT / "historical/Conference01_README.md")
    authority_update = {"id": "RANK9-CATASTROPHE10-CURRENT-AUTHORITY-UPDATE-171", "recordedAtUtc": now, "authority": AUTH, "scopeIds": IDS, "index": bind(INDEX), "catalog": bind(CATALOG), "queue": bind(QUEUE), "handoff": bind(HANDOFF), "pendingIdentityAudit": bind(PENDING), "latestAppliedBatch": {"application": bind(LATEST[0]), "acceptance": bind(LATEST[1]), "validation": bind(LATEST[2]), "returnReceipt": bind(LATEST[3])}, "qualification": "Fresh static source context only; no new procedure, runtime, cosmology, playtest, balance, or release approval."}
    write(OUTPUT / "CURRENT_AUTHORITY_UPDATE.json", enc(authority_update)); output_files.append(OUTPUT / "CURRENT_AUTHORITY_UPDATE.json")
    live_sources = []
    for row in source_bindings:
        src = ROOT / row["path"]
        dst = OUTPUT / "sources" / PurePosixPath(row["path"])
        write(dst, src.read_bytes())
        live_sources.append(dst)
    readme = f"# Rank9 Catastrophe10 Source Conference02\n\nFreshly bound to 739/109/0 authority. Scope is exactly ten pending rank9 identities and 25 original unselected questions. Conference01 is retained as historical context only. No authored choices or canonical changes are made by this packet.\n"
    write(OUTPUT / "README.md", readme.encode("utf-8")); output_files.append(OUTPUT / "README.md")

    checks = []
    def ck(label, ok):
        checks.append({"check": label, "passed": bool(ok)})
        assert ok, label
    ck("Current authority and standalone count match the live index", AUTH == {"reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173})
    ck("Live pending identity set matches the current pending audit", set(pending["pendingIds"]) == live_pending and pending["pendingCount"] == 109)
    ck("Exact ten Catastrophe IDs are pending in the first current group", group["group"] == "rank9-catastrophe10" and group["pendingIds"] == IDS and set(IDS) <= live_pending)
    ck("All 25 original questions and ten source records are preserved", len(candidate["questions"]) == 25 and all(not q["decisionSelected"] for q in candidate["questions"]) and len(candidate["records"]) == 10)
    ck("All ten current catalog cards and index entries bind live data", all(r["completeCurrentCatalogSourceAndAccess"] == catalog_by[r["spellId"]] and r["currentIndexEntry"] == index_by[r["spellId"]] for r in candidate["records"]))
    ck("All refreshed source bindings are exact byte-for-byte current repository files", all(bind(ROOT / r["path"]) == {"path": r["path"], "bytes": r["bytes"], "sha256": r["sha256"]} and (OUTPUT / "sources" / PurePosixPath(r["path"])).read_bytes() == (ROOT / r["path"]).read_bytes() for r in source_bindings))
    ck("Current application/acceptance/validation/return receipt all bind after prior batch", all(p.is_file() for p in LATEST) and read(LATEST[2])["status"] == "PASS")
    ck("Prior Conference01 archive and source candidate remain exact historical bytes", (OUTPUT / "historical/Conference01_ARCHIVE.zip").read_bytes() == old_archive_raw and (OUTPUT / "historical/Conference01_CANDIDATE.json").read_bytes() == old_raw)
    ck("No new rules, runtime, human-play, or cosmology choices are adopted", candidate["newRuleAdoptions"] == candidate["runtimeTestsExecuted"] == candidate["humanPlaytests"] == candidate["cosmologyDecisions"] == 0 and not candidate["wholeGameComplete"])
    check_doc = {"id": "RANK9-CATASTROPHE10-CONFERENCE02-CHECK-171", "recordedAtUtc": now, "status": "PASS", "checkCount": len(checks), "checksFailed": 0, "checks": checks, "currentAuthority": AUTH, "scopeIds": IDS, "questionCount": 25, "sourceBindingCount": len(source_bindings)}
    write(CHECK, enc(check_doc)); write(OUTPUT / "SOURCE_CHECK.json", enc(check_doc))
    members = []
    for path in sorted(OUTPUT.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.json":
            raw = path.read_bytes()
            members.append({"path": path.relative_to(OUTPUT).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    manifest = {"id": "RANK9-CATASTROPHE10-CONFERENCE02-MANIFEST-171", "candidate": {"path": "CANDIDATE.json", "bytes": len(candidate_raw), "sha256": sha(candidate_raw)}, "currentAuthority": AUTH, "scopeIds": IDS, "memberCount": len(members), "members": members, "historicalConference01Archive": {"path": "historical/Conference01_ARCHIVE.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)}, "liveCurrentSourceBindings": source_bindings}
    write(OUTPUT / "MANIFEST.json", enc(manifest)); write(OUTPUT / "MANIFEST.json", enc(manifest))
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(OUTPUT.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(OUTPUT).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        archive_names = z.namelist()
        assert len(archive_names) == len(set(archive_names))
        assert z.read("CANDIDATE.json") == candidate_raw
        assert z.read("historical/Conference01_ARCHIVE.zip") == old_archive_raw
        assert json.loads(z.read("SOURCE_CHECK.json"))["checksFailed"] == 0
        for row in source_bindings:
            assert z.read("sources/" + row["path"]) == (ROOT / row["path"]).read_bytes()
    archive_binding = bind(ARCHIVE)
    prep = {"id": "RANK9-CATASTROPHE10-CONFERENCE02-PREPARATION-171", "recordedAtUtc": now, "status": "PREPARED_UNSENT", "candidate": bind(CANDIDATE), "archive": archive_binding, "check": bind(CHECK), "request": bind(REQUEST), "manifest": bind(OUTPUT / "MANIFEST.json"), "memberCount": len(archive_names), "sourceBindingCount": len(source_bindings), "questionCount": 25, "currentAuthority": AUTH, "reviewIds": IDS}
    write(PREP, enc(prep)); write(OUTPUT / "PREPARATION.json", enc(prep))
    pending_after = {"id": "CURRENT109-PENDING-IDENTITY-AUDIT-171", "recordedAtUtc": now, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": index["authoredCounts"], "pendingCount": 109, "pendingIds": sorted(live_pending), "allPendingExistInSourceCatalog": all(sid in catalog_by for sid in live_pending), "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0}
    write(PENDING_AFTER, enc(pending_after))
    q = copy.deepcopy(queue)
    q.update({"id": "SPELL-REVIEW-QUEUE-171", "recordedAtUtc": now, "packetStatus": "RANK9_CATASTROPHE10_FRESH_PACKET_PREPARED_UNSENT", "currentAuthority": AUTH, "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 109, "sha256": sha(PENDING_AFTER.read_bytes())}})
    q["currentPendingGroups"][0].update({"candidate": prep["candidate"], "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "FRESH_PACKET_PREPARED_UNSENT"})
    q["nextGroup"] = "rank9-catastrophe10"
    q["next"] = {"group": "rank9-catastrophe10", "pendingCount": 10, "candidate": prep["candidate"], "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "FRESH_PACKET_PREPARED_UNSENT"}
    q["sourceConferencePrepared"] = {"candidate": prep["candidate"], "archive": archive_binding, "check": prep["check"], "preparation": bind(PREP), "request": bind(REQUEST), "status": "prepared-unsent"}
    write(QUEUE_AFTER, enc(q))
    h = copy.deepcopy(handoff)
    h.update({"id": "CURRENT-HANDOFF-171", "recordedAtUtc": now, "status": "RANK9_CATASTROPHE10_FRESH_PACKET_PREPARED_UNSENT", "currentQueueBinding": bind(QUEUE_AFTER), "pendingIdentityAudit": {"id": pending_after["id"], "path": PENDING_AFTER.name, "pendingCount": 109, "sha256": sha(PENDING_AFTER.read_bytes())}, "nextGroup": "rank9-catastrophe10", "resumePriority": "Submit this exact fresh 739/109 packet to the GPT director; independently audit and apply only the exact accepted IDs; push each batch; continue until pending reaches zero.", "nextPreparedRequest": {"group": "rank9-catastrophe10", "candidate": prep["candidate"], "archive": archive_binding, "request": bind(REQUEST), "freshPacketRequiredForCurrentAuthority": False}})
    h["directorSubmission"] = {"status": "prepared-unsent", "group": "rank9-catastrophe10", "reviewIds": IDS, "candidate": prep["candidate"], "archive": archive_binding, "request": bind(REQUEST)}
    write(HANDOFF_AFTER, enc(h))
    print(json.dumps({"status": "PASS_PREPARED_UNSENT", "candidate": prep["candidate"], "archive": archive_binding, "checks": len(checks), "sourceBindingCount": len(source_bindings), "archiveMemberCount": len(archive_names), "authority": AUTH, "reviewIds": IDS}, indent=2))


if __name__ == "__main__":
    main()
