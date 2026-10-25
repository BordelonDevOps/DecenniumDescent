from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
OLD_ARCHIVE = FULL / "DD_Rank8_Planar_5_Source_Conference_01.zip"
OLD_PREPARATION = FULL / "RANK8_PLANAR_5_SOURCE_CONFERENCE_01_PREPARATION.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_164.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_164.json"
PENDING = AUDIT / "CURRENT118_PENDING_IDENTITY_AUDIT_164.json"
LAST_APP = AUDIT / "INFORMATION_TIME4_APPLICATION_164.json"
LAST_DECISION = AUDIT / "GPT_DIRECTOR_DECISION_INFORMATION_TIME4_162.json"
LAST_ACCEPTANCE = AUDIT / "INFORMATION_TIME4_EXACT_ACCEPTANCE_162.json"
LAST_VALIDATION = AUDIT / "INFORMATION_TIME4_APPLICATION_VALIDATION_164.json"
IDS = ["demiplane", "maze", "planar-seal", "seal-of-banishment", "gloom-bind"]
EXPECTED_AUTHORITY = {
    "reviewedApplied": 730,
    "pending": 118,
    "acceptedUnapplied": 0,
    "completeReviewedStandaloneProcedures": 454,
    "scopedInterfaces": 173,
}
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_planar_5_source_conference_02.json"
OUTPUT = FULL / "rank8-planar5-source-conference-02-165"
ARCHIVE = FULL / "DD_Rank8_Planar_5_Source_Conference_02.zip"
CHECK = FULL / "RANK8_PLANAR_5_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_PLANAR_5_SOURCE_CONFERENCE_02_PREPARATION.json"
REQUEST = FULL / "RANK8_PLANAR_5_SOURCE_CONFERENCE_02_REQUEST.txt"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_165.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_165.json"


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def write_bytes(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def main() -> None:
    final_outputs = [ARCHIVE, CHECK, PREPARATION, QUEUE_AFTER, HANDOFF_AFTER]
    existing = [str(path) for path in final_outputs if path.exists()]
    assert not existing, f"Conference02 final outputs already exist; inspect before retry: {existing}"
    if REQUEST.exists():
        assert "730 applied-reviewed / 118 pending" in REQUEST.read_text(encoding="utf-8-sig"), "Refusing to overwrite an unrelated request"
    if CANDIDATE.exists():
        assert read(CANDIDATE).get("id") == "RANK8-PLANAR5-SOURCE-CONFERENCE02-165", "Refusing to overwrite an unrelated candidate"
    if OUTPUT.exists() and (OUTPUT / "CANDIDATE.json").exists():
        assert read(OUTPUT / "CANDIDATE.json").get("id") == "RANK8-PLANAR5-SOURCE-CONFERENCE02-165", "Refusing to overwrite an unrelated packet directory"

    with zipfile.ZipFile(OLD_ARCHIVE) as old_zip:
        assert old_zip.testzip() is None
        old_candidate_raw = old_zip.read("CANDIDATE.json")
        old_candidate = json.loads(old_candidate_raw.decode("utf-8-sig"))
        old_manifest = json.loads(old_zip.read("MANIFEST.json"))
        old_check = json.loads(old_zip.read("SOURCE_CHECK.json"))
        old_readme = old_zip.read("README.md")
        old_source_members = [n for n in old_zip.namelist() if n.startswith("sources/")]
    old_prep = read(OLD_PREPARATION)
    old_archive_raw = OLD_ARCHIVE.read_bytes()
    assert len(old_archive_raw) == old_prep["archive"]["bytes"]
    assert sha(old_archive_raw) == old_prep["archive"]["sha256"]

    index = read(INDEX)
    catalog = read(CATALOG)
    queue_before = read(QUEUE)
    handoff_before = read(HANDOFF)
    pending_before = read(PENDING)
    assert queue_before["currentAuthority"] == handoff_before["currentAuthority"] == EXPECTED_AUTHORITY
    assert pending_before["pendingCount"] == EXPECTED_AUTHORITY["pending"]
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 118 and set(pending_before["pendingIds"]) == live_pending
    first = queue_before["currentPendingGroups"][0]
    assert first["group"] == "rank8-planar5" and first["pendingIds"] == IDS
    assert set(IDS) <= live_pending
    catalog_by_id = {row["id"]: row for row in catalog["spells"]}
    index_by_id = {row["id"]: row for row in index["entries"]}
    assert all(sid in catalog_by_id for sid in IDS)
    assert all(index_by_id[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS)

    source_files: dict[str, Path] = {}
    for row in old_candidate["sourceBindings"]:
        rel = Path(row["path"])
        path = ROOT / rel
        assert path.is_file(), f"historical conference source is missing from current checkout: {rel}"
        source_files[rel.as_posix()] = path
    for path in [INDEX, CATALOG, QUEUE, HANDOFF, PENDING, LAST_APP, LAST_DECISION, LAST_ACCEPTANCE, LAST_VALIDATION]:
        assert path.is_file(), f"required current authority source missing: {path}"
        source_files[path.relative_to(ROOT).as_posix()] = path
    current_sources = [
        {"path": rel, "bytes": len(path.read_bytes()), "sha256": sha(path.read_bytes())}
        for rel, path in sorted(source_files.items())
    ]
    source_map = {row["path"]: row for row in current_sources}

    candidate = copy.deepcopy(old_candidate)
    now = datetime.now(timezone.utc).isoformat()
    candidate.update({
        "id": "RANK8-PLANAR5-SOURCE-CONFERENCE02-165",
        "recordedAtUtc": now,
        "status": "SOURCE_CONFERENCE_PREPARED_UNSENT",
        "priorConferenceSupersededBy": "Conference02 is freshly bound to current 730 applied-reviewed / 118 pending / 0 accepted-unapplied authority. Conference01 remains historical 525/323 evidence only and cannot authorize current acceptance or application.",
        "currentAuthority": {
            **EXPECTED_AUTHORITY,
            "index": binding(INDEX),
            "catalog": binding(CATALOG),
            "currentQueue": binding(QUEUE),
            "pendingIdentityAudit": binding(PENDING),
            "priorHandoff": binding(HANDOFF),
            "latestAppliedBatch": binding(LAST_APP),
            "latestDirectorDecision": binding(LAST_DECISION),
            "latestExactAcceptance": binding(LAST_ACCEPTANCE),
            "latestApplicationValidation": binding(LAST_VALIDATION),
        },
        "countsUnchanged": {"reviewed": EXPECTED_AUTHORITY["reviewedApplied"], "pending": EXPECTED_AUTHORITY["pending"], "acceptedUnapplied": 0},
        "historicalConference01": {
            "authority": old_candidate["countsUnchanged"],
            "archive": {"path": "docs/audit/2026-10-08/full-game/DD_Rank8_Planar_5_Source_Conference_01.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
            "qualification": "Full source context only; all question decisions remain unselected and all 525/323 authority claims are superseded.",
        },
        "historicalSourceBindingsConference01": copy.deepcopy(old_candidate["sourceBindings"]),
        "sourceBindings": current_sources,
        "currentPendingIds": IDS,
        "currentQueueGroup": copy.deepcopy(first),
        "currentPendingIdentityAudit": {"id": pending_before["id"], **binding(PENDING), "pendingCount": 118, "pendingIds": pending_before["pendingIds"]},
        "priorConferenceQuestionSetPreserved": {"questionCount": len(old_candidate["questions"]), "allStillUnselected": True},
        "gptCommunication": "Fresh Rank8 Planar5 source conference for current 730 applied-reviewed / 118 pending / 0 accepted-unapplied authority. Review only demiplane, maze, planar-seal, seal-of-banishment, and gloom-bind. Resolve the 24 preserved source questions. Preserve every source, access, content, lifecycle, information, structure, runtime, balance, cosmology, and release hold. Do not reopen any completed or applied cohort.",
        "nonAcceptanceOfLaterSourceChanges": "This packet supplies current source context only. No canonical rules, realm identities, realm ontology, owner decisions, gameplay procedures, or release state are adopted. Preserve exact acceptance/application boundaries; later source text does not reopen completed spells.",
        "newRuleAdoptions": 0,
        "runtimeTestsExecuted": 0,
        "humanPlaytests": 0,
        "sourceInformationDeleted": 0,
        "wholeGameComplete": False,
    })
    assert len(candidate["questions"]) == 24
    assert all(row["decisionSelected"] is False for row in candidate["questions"])
    assert set().union(*(set(row["spellIds"]) for row in candidate["questions"])) == set(IDS)
    assert len(candidate["records"]) == 5
    for record in candidate["records"]:
        sid = record["spellId"]
        assert sid in IDS
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(catalog_by_id[sid])
        record["currentIndexEntry"] = copy.deepcopy(index_by_id[sid])
        record["currentQueueStatus"] = {"identity": sid, "group": "rank8-planar5", "pending": True, "reviewedApplied": 730, "pendingCount": 118}
        record["status"] = "Fresh source conference prepared; no choices adopted."
    candidate_raw = encode(candidate)
    write_bytes(CANDIDATE, candidate_raw)

    request_text = f"""GPT — please review the exact fresh Rank8 Planar5 Conference02 packet attached and published on the current branch.\n\nPacket: DD_Rank8_Planar_5_Source_Conference_02.zip\nAuthority: 730 applied-reviewed / 118 pending / 0 accepted-unapplied.\nScope: demiplane, maze, planar-seal, seal-of-banishment, gloom-bind only.\n\nResolve all 24 source questions and return source-faithful complete operational procedures, complete question and case dispositions, exact accepted IDs, a complete hold register, and an independent semantic failure check. Retain all original source/access distinctions and unresolved cosmology. Do not infer plane equivalences, objective realm ontology, natural origins, afterlife, or release status. Keep runtime, human-play, balance, cosmology, and release qualifications explicit. Do not edit canonical files or revisit any completed/applied cohort. If the exact packet passes, state accepted=true and applied=false only for the exact IDs accepted; otherwise keep every identity unaccepted and unapplied and list exact blockers.\n"""
    write_bytes(REQUEST, request_text.encode("utf-8"))
    write(OUTPUT / "CANDIDATE.json", candidate)
    write(OUTPUT / "CURRENT_AUTHORITY_UPDATE.json", {"id": "PLANAR5-CURRENT-AUTHORITY-UPDATE-165", "recordedAtUtc": now, "authority": EXPECTED_AUTHORITY, "pendingIds": pending_before["pendingIds"], "group": "rank8-planar5", "scopeIds": IDS, "index": binding(INDEX), "catalog": binding(CATALOG), "queue": binding(QUEUE), "handoff": binding(HANDOFF), "pendingAudit": binding(PENDING), "exactAppliedBatch": binding(LAST_APP), "qualification": "Source review only; no rule adoption, runtime, human-play, balance, cosmology, or release approval."})
    write_bytes(OUTPUT / "REQUEST.txt", request_text.encode("utf-8"))
    write_bytes(OUTPUT / "historical/Conference01_ARCHIVE.zip", old_archive_raw)
    write_bytes(OUTPUT / "historical/Conference01_README.md", old_readme)
    write_bytes(OUTPUT / "historical/Conference01_SOURCE_CHECK.json", encode(old_check))
    for rel, path in source_files.items():
        write_bytes(OUTPUT / "sources" / Path(*rel.split("/")), path.read_bytes())
    readme = """# Rank8 Planar5 Source Conference02\n\nFresh source context bound to 730 applied-reviewed / 118 pending / 0 accepted-unapplied authority. Scope is exactly demiplane, maze, planar-seal, seal-of-banishment, and gloom-bind. The 24 historical source questions remain unselected. Conference01 and its 525/323 authority are retained as historical context only. No rules, cosmology, runtime behavior, balance, human play, or release are approved.\n"""
    write_bytes(OUTPUT / "README.md", readme.encode("utf-8"))

    checks: list[dict[str, Any]] = []
    def ck(name: str, passed: bool) -> None:
        checks.append({"check": name, "passed": bool(passed)})
        assert passed, name
    ck("Current authority equals 730/118/0 plus 454 procedures and 173 scoped interfaces", queue_before["currentAuthority"] == EXPECTED_AUTHORITY)
    ck("Current pending audit exactly matches live index", set(pending_before["pendingIds"]) == live_pending and pending_before["pendingCount"] == len(live_pending))
    ck("Only exact Planar5 identities are selected for this review", candidate["currentPendingIds"] == IDS and set(IDS) <= set(pending_before["pendingIds"]))
    ck("All 24 historical source questions remain unselected", len(candidate["questions"]) == 24 and all(q["decisionSelected"] is False for q in candidate["questions"]))
    ck("All five records bind current catalog cards and index entries", all(r["completeCurrentCatalogSourceAndAccess"] == catalog_by_id[r["spellId"]] and r["currentIndexEntry"] == index_by_id[r["spellId"]] for r in candidate["records"]))
    ck("No accepted-unapplied identities exist", EXPECTED_AUTHORITY["acceptedUnapplied"] == 0 and pending_before["acceptedUnapplied"] == 0)
    ck("No choices, rules, runtime, playtests or release states adopted", candidate["newRuleAdoptions"] == candidate["runtimeTestsExecuted"] == candidate["humanPlaytests"] == 0 and candidate["wholeGameComplete"] is False)
    ck("All historical source bindings have current exact source copies", len(current_sources) >= 82 and all((OUTPUT / "sources" / Path(*row["path"].split("/"))).read_bytes() == (ROOT / row["path"]).read_bytes() for row in current_sources))
    ck("Conference01 source archive retained byte-exact", (OUTPUT / "historical/Conference01_ARCHIVE.zip").read_bytes() == old_archive_raw)
    ck("Candidate has fresh current authority and retains source questions", candidate["currentAuthority"]["reviewedApplied"] == 730 and candidate["currentAuthority"]["pending"] == 118 and candidate["historicalConference01"]["authority"] == {"reviewed": 525, "pending": 323})
    check_doc = {"id": "RANK8-PLANAR5-SOURCE-CONFERENCE02-CHECK-165", "recordedAtUtc": now, "failures": 0, "candidate": {"path": CANDIDATE.relative_to(ROOT).as_posix(), "bytes": len(candidate_raw), "sha256": sha(candidate_raw)}, "checks": checks, "questionCount": len(candidate["questions"]), "reviewIds": IDS, "currentAuthority": EXPECTED_AUTHORITY}
    write(CHECK, check_doc)
    write(OUTPUT / "SOURCE_CHECK.json", check_doc)
    manifest = {
        "id": "RANK8-PLANAR5-SOURCE-CONFERENCE02-MANIFEST-165",
        "candidate": {"path": "CANDIDATE.json", "bytes": len(candidate_raw), "sha256": sha(candidate_raw)},
        "check": {"path": "SOURCE_CHECK.json", "bytes": len(encode(check_doc)), "sha256": sha(encode(check_doc))},
        "request": {"path": "REQUEST.txt", "bytes": len(request_text.encode("utf-8")), "sha256": sha(request_text.encode("utf-8"))},
        "historicalConference01Archive": {"path": "historical/Conference01_ARCHIVE.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
        "currentAuthority": EXPECTED_AUTHORITY,
        "currentSourceBindings": current_sources,
    }
    write(OUTPUT / "MANIFEST.json", manifest)
    # Include all evidence members byte-exactly; the manifest separately enumerates source bindings.
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(OUTPUT.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(OUTPUT).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names))
        assert z.read("CANDIDATE.json") == candidate_raw
        assert json.loads(z.read("SOURCE_CHECK.json"))["failures"] == 0
        assert z.read("historical/Conference01_ARCHIVE.zip") == old_archive_raw
        for row in current_sources:
            assert z.read("sources/" + row["path"]) == (ROOT / row["path"]).read_bytes(), row["path"]
    archive_binding = {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": ARCHIVE.stat().st_size, "sha256": sha(ARCHIVE.read_bytes())}
    prep_doc = {"id": "RANK8-PLANAR5-SOURCE-CONFERENCE02-PREPARATION-165", "recordedAtUtc": now, "status": "PREPARED_UNSENT", "candidate": check_doc["candidate"], "archive": archive_binding, "check": binding(CHECK), "questionCount": len(candidate["questions"]), "sourceBindingCount": len(current_sources), "archiveMemberCount": len(names), "currentAuthority": EXPECTED_AUTHORITY, "reviewIds": IDS}
    write(PREPARATION, prep_doc)
    write(OUTPUT / "PREPARATION.json", prep_doc)
    write(OUTPUT / "MANIFEST.json", manifest)
    # Queue/handoff note that the fresh packet is ready but has not yet been sent.
    queue_after = copy.deepcopy(queue_before)
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-165", "recordedAtUtc": now, "packetStatus": "FRESH_PLANAR5_PACKET_PREPARED_UNSENT"})
    queue_after["currentPendingGroups"][0].update({"candidate": check_doc["candidate"], "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "FRESH_PACKET_PREPARED_UNSENT"})
    queue_after["next"] = {"group": "rank8-planar5", "pendingCount": 5, "candidate": check_doc["candidate"], "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "FRESH_PACKET_PREPARED_UNSENT"}
    queue_after["sourceConferencePrepared"] = {"candidate": check_doc["candidate"], "archive": archive_binding, "check": binding(CHECK), "preparation": binding(PREPARATION), "request": binding(REQUEST), "status": "prepared-unsent"}
    queue_after["nextPreparedRequest"] = queue_after["sourceConferencePrepared"]
    write(QUEUE_AFTER, queue_after)
    handoff_after = copy.deepcopy(handoff_before)
    handoff_after.update({"id": "CURRENT-HANDOFF-165", "recordedAtUtc": now, "status": "PLANAR5_FRESH_PACKET_PREPARED_UNSENT", "currentQueueBinding": binding(QUEUE_AFTER)})
    handoff_after["nextPreparedRequest"] = queue_after["sourceConferencePrepared"]
    handoff_after["directorSubmission"] = {"status": "prepared-unsent", "group": "rank8-planar5", "reviewIds": IDS, "candidate": check_doc["candidate"], "archive": archive_binding, "request": binding(REQUEST)}
    write(HANDOFF_AFTER, handoff_after)
    print(json.dumps({"status": "PASS_PREPARED_UNSENT", "candidate": check_doc["candidate"], "archive": archive_binding, "checkCount": len(checks), "archiveMemberCount": len(names), "sourceBindingCount": len(current_sources), "currentAuthority": EXPECTED_AUTHORITY, "reviewIds": IDS}, indent=2))


if __name__ == "__main__":
    main()
