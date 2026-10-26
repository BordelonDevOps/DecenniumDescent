from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
OUT = AUDIT / "rank9_defenseform8_return185_prepared"
SOURCE_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_defense_form_8_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Defense_Form_8_Source_Conference_01.zip"
GROUP = "rank9-defense-form8"
IDS = ["absolute-immunity", "astral-shell", "divine-shield", "eternal-protection", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]
AUTHORITY = {"reviewedApplied": 763, "pending": 85, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 487, "scopedInterfaces": 173}
COMMIT = "a88d9cd4177cab3d4f6dbaa2fef55876699b626c"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{COMMIT}:{path}"], cwd=ROOT)


def git_blob_id(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{COMMIT}:{path}"], cwd=ROOT, text=True).strip()


def read_json_bytes(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: str | Path, raw: bytes | None = None) -> dict:
    if raw is None:
        raw = Path(path).read_bytes()
    return {"path": Path(path).as_posix() if isinstance(path, Path) else path, "bytes": len(raw), "sha256": sha(raw)}


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def main() -> None:
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == COMMIT
    assert not OUT.exists()
    queue = read_json_bytes(git_blob("docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_184.json"))
    handoff = read_json_bytes(git_blob("docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_184.json"))
    pending = read_json_bytes(git_blob("docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT85_PENDING_IDENTITY_AUDIT_184.json"))
    index_raw = git_blob("DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json")
    catalog_raw = git_blob("DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json")
    index = read_json_bytes(index_raw)
    catalog = read_json_bytes(catalog_raw)
    current_group = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert handoff["currentAuthority"] == queue["currentAuthority"] == AUTHORITY
    assert handoff["nextGroup"] == queue["nextGroup"] == GROUP
    assert current_group["pendingIds"] == IDS and current_group["pendingCount"] == 8
    assert pending["pendingCount"] == 85 and len(pending["pendingIds"]) == 85
    entry_map = {row["id"]: row for row in index["entries"]}
    catalog_map = {row["id"]: row for row in catalog["spells"]}
    assert index["authoredCounts"] == {"reviewed": 763, "pending": 85}
    assert set(IDS) <= set(pending["pendingIds"])
    assert all(entry_map[s]["authoredStatus"] == "pending-authored-procedure" and entry_map[s]["sourceStatus"] == "blocked-pending-operational-review" and catalog_map[s]["operational"] is None for s in IDS)

    old_candidate_raw = git_blob(SOURCE_CANDIDATE)
    old_archive_raw = git_blob(SOURCE_ARCHIVE)
    old_candidate = read_json_bytes(old_candidate_raw)
    assert sha(old_candidate_raw) == current_group["candidate"]["sha256"] and len(old_candidate_raw) == current_group["candidate"]["bytes"]
    assert sha(old_archive_raw) == current_group["archive"]["sha256"] and len(old_archive_raw) == current_group["archive"]["bytes"]
    assert [row["spellId"] for row in old_candidate["records"]] == IDS
    assert len(old_candidate["sourceBindings"]) == 87

    original_members = {}
    with zipfile.ZipFile(ROOT / SOURCE_ARCHIVE) as old_zip:
        assert old_zip.testzip() is None and len(old_zip.namelist()) == len(set(old_zip.namelist()))
        for source in old_candidate["sourceBindings"]:
            original = old_zip.read("sources/" + source["path"])
            assert len(original) == source["bytes"] and sha(original) == source["sha256"]
            original_members[source["path"]] = original

    refreshed_bindings = []
    fresh_sources = {}
    changed_since_preparation = []
    for source in old_candidate["sourceBindings"]:
        path = source["path"]
        raw = git_blob(path)
        observed = {"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": git_blob_id(path)}
        refreshed_bindings.append(observed)
        fresh_sources["sources_current/" + path] = raw
        if raw != original_members[path]:
            changed_since_preparation.append({"path": path, "originalBytes": len(original_members[path]), "originalSHA256": sha(original_members[path]), "currentBytes": len(raw), "currentSHA256": sha(raw)})
    assert [row["path"] for row in refreshed_bindings] == [row["path"] for row in old_candidate["sourceBindings"]]
    assert [row["path"] for row in changed_since_preparation] == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]

    ts = datetime.now(timezone.utc).isoformat()
    derived_candidate = copy.deepcopy(old_candidate)
    original_source_bindings = copy.deepcopy(derived_candidate["sourceBindings"])
    derived_candidate.update({
        "id": "RANK9-DEFENSE-FORM8-CURRENT-SOURCE-CONTEXT-185",
        "recordedAtUtc": ts,
        "status": "FRESH_CURRENT_SOURCE_BINDINGS_FOR_763_REVIEWED_85_PENDING_AUTHORITY",
        "historicalCandidateBinding": bind(SOURCE_CANDIDATE, old_candidate_raw),
        "historicalSourceArchiveBinding": bind(SOURCE_ARCHIVE, old_archive_raw),
        "historicalSourceBindings": original_source_bindings,
        "sourceBindings": refreshed_bindings,
        "currentSourceCommit": COMMIT,
        "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": IDS, "count": 8},
        "sourceBindingRefresh": {"sourceFiles": len(refreshed_bindings), "changedSinceOriginalPreparation": changed_since_preparation, "currentIndexRefreshedTo763Reviewed85Pending": True},
        "priorHeldIdentitiesNotReopened": ["psychic-scream", "mass-phantom-killer", "weird", "doom", "final-word", "eternal-pact"],
        "newRuleAdoptions": 0,
        "canonicalFilesEdited": False,
    })
    derived_candidate_raw = json_bytes(derived_candidate)

    current_paths = [
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_184.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_184.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT85_PENDING_IDENTITY_AUDIT_184.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEATHRECOVERY7_EXACT_ACCEPTANCE_184.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEATHRECOVERY7_APPLICATION_VALIDATION_184.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEATHRECOVERY7_RETURN184_INDEPENDENT_AUDIT.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEFENSEFORM8_NEXT_CONFERENCE_NOTES_129.json",
    ]
    current_files = {"current/" + path: git_blob(path) for path in current_paths}
    current_context = {
        "id": "RANK9-DEFENSE-FORM8-CURRENT-DIRECTOR-CONTEXT-185",
        "recordedAtUtc": ts,
        "sourceCommit": COMMIT,
        "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": 8},
        "previousDirectorReturnApplied": {"ids": ["soul-harvest", "power-word-kill", "thread-severance", "wail-of-the-banshee"], "commitBeforeThisPacket": "25273775f16cf9877c758b3b923f672e60d6a44b", "applicationCommit": COMMIT, "pendingAfter": 85},
        "carriedForwardHolds": {"psychicFear7": ["psychic-scream", "mass-phantom-killer", "weird"], "deathRecovery7": ["doom", "final-word", "eternal-pact"]},
        "sourceArchiveHistoricalSnapshotNote": "The 2026-10-20 source-conference archive is preserved byte-exact for provenance. All 87 bound source files are refreshed from the exact current Git commit under sources_current/; the only file changed since preparation is authored_review_index.json, now bound at 763 reviewed / 85 pending. Use sources_current and current/ as current authority.",
        "historicalNotesQualification": "RANK9DEFENSEFORM8_NEXT_CONFERENCE_NOTES_129.json retains useful requested branch coverage but was prepared under 616/232 authority. Treat its source interpretations as proposals to recheck against the current source snapshots, never as current authority.",
        "qualification": "Static authored-procedure review only. Do not change canonical index/catalog/queue/handoff. Do not claim application. Keep runtime selection, source/access, playtest, balance, cosmology, domain closure, and release approval separate.",
    }
    current_context_raw = json_bytes(current_context)
    request = (
        "GPT director — review the exact eight Rank9 Defense/Form8 identities in the attached current-source packet.\n\n"
        f"Current GitHub branch: codex/ordinary-spell-review-complete at {COMMIT}. Authority: 763 reviewed-applied / 85 pending / 0 accepted-unapplied; 487 complete reviewed standalone procedures; 173 scoped interfaces.\n\n"
        "Review only these eight pending IDs: absolute-immunity, astral-shell, divine-shield, eternal-protection, elemental-shell, body-to-void, timeless-form, invulnerable-sphere. The exact current queue and handoff, pending audit, authored index, and catalog are in the attached packet. The earlier 2026-10-20 source-conference archive and notes are preserved as historical inputs; the packet refreshes all 87 source bindings from the current commit. One source file changed since preparation: authored_review_index.json, now 763/85. Use the sources_current/ and current/ packet members as authority.\n\n"
        "Return exact source-faithful standalone procedures, complete cases for all eight IDs, per-identity accepted=true/applied=false only when every required branch and integrity check passes, and exact narrow blockers/holds otherwise. Do not claim application or edit canonical files. Preserve the full stated immunity, resistance, positive reflection, energy-form, temporal, and closed-boundary benefits. Recheck the historical notes against current source; do not turn their requested cases into unsupported mechanics. Do not reopen the six carried-forward held identities, feats, or completed cohorts. Preserve source/access and runtime, human-play, balance, cosmology, domain-closure, and release gates.\n\n"
        "Include an independent semantic failure check, source and data bindings, clock/inverse results, exact ZIP/member manifest and matching delivery manifest, all qualifications, and the next queue group. After my audit/application, continue in queue order until pending reaches zero."
    )

    request_raw = request.encode("utf-8")
    source_candidate_refreshed_raw = derived_candidate_raw
    files = {
        "CURRENT_CONTEXT_185.json": current_context_raw,
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json": source_candidate_refreshed_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": old_candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": old_archive_raw,
        "REQUEST_185.txt": request_raw,
        **current_files,
        **fresh_sources,
    }
    OUT.mkdir(parents=True, exist_ok=False)
    zip_path = OUT / "DD_Rank9_DefenseForm8_CurrentSource_185.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        rows = []
        for name in sorted(files):
            raw = files[name]
            archive.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {"id": "RANK9-DEFENSE-FORM8-CURRENT-SOURCE-PACKET-MANIFEST-185", "sourceCommit": COMMIT, "sourceAuthority": AUTHORITY, "memberCountExcludingSelf": len(rows), "members": rows}
        archive.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(zip_path) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(set(archive.namelist())) == len(rows) + 1
        for row in rows:
            raw = archive.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]
        assert json.loads(archive.read("MANIFEST.json"))["members"] == rows

    archive_binding = bind(zip_path.relative_to(ROOT).as_posix(), zip_path.read_bytes())
    candidate_binding = bind("CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json", derived_candidate_raw)
    checks = [
        {"check": "Current 763/85 authority matches handoff, queue, pending audit and index", "passed": handoff["currentAuthority"] == queue["currentAuthority"] == AUTHORITY and pending["pendingCount"] == 85 and index["authoredCounts"] == {"reviewed": 763, "pending": 85}},
        {"check": "Exact eight next-group IDs remain pending and native catalog rows remain unreviewed", "passed": current_group["pendingIds"] == IDS and all(entry_map[s]["authoredStatus"] == "pending-authored-procedure" and catalog_map[s]["operational"] is None for s in IDS)},
        {"check": "All 87 prepared source members are byte-exact to the historical source archive", "passed": len(original_members) == 87 and all(len(original_members[b["path"]]) == b["bytes"] and sha(original_members[b["path"]]) == b["sha256"] for b in old_candidate["sourceBindings"])},
        {"check": "All 87 source inputs are refreshed from the exact current Git commit", "passed": len(refreshed_bindings) == 87 and all(sha(git_blob(b["path"])) == b["sha256"] and git_blob_id(b["path"]) == b["gitBlobSHA1"] for b in refreshed_bindings)},
        {"check": "Only the authored review index changed since the original source conference; it is refreshed", "passed": [row["path"] for row in changed_since_preparation] == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"] and next(row for row in derived_candidate["sourceBindings"] if row["path"] == "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json")["sha256"] == sha(index_raw)},
        {"check": "New packet ZIP CRC, member allowlist, hashes and internal manifest pass", "passed": True, "detail": {"memberCount": len(rows) + 1, "bytes": zip_path.stat().st_size, "sha256": sha(zip_path.read_bytes())}},
    ]
    assert all(row["passed"] for row in checks)
    prep = {
        "id": "RANK9-DEFENSEFORM8-SOURCE-PREPARATION-185",
        "recordedAtUtc": ts,
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "sourceCommit": COMMIT,
        "sourceAuthority": AUTHORITY,
        "group": GROUP,
        "pendingIds": IDS,
        "historicalCandidate": bind(SOURCE_CANDIDATE, old_candidate_raw),
        "historicalSourceArchive": bind(SOURCE_ARCHIVE, old_archive_raw),
        "currentDerivedCandidate": candidate_binding,
        "currentSourceFileCount": len(refreshed_bindings),
        "changedSinceOriginalPreparation": changed_since_preparation,
        "currentFiles": [bind(p, raw) for p, raw in current_files.items()],
        "packet": archive_binding,
        "members": len(rows) + 1,
        "checksPassed": len(checks),
        "checksFailed": 0,
        "checks": checks,
        "canonicalChangesBeforePreparation": False,
        "request": request,
    }
    prep_path = AUDIT / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_185.json"
    write_json(prep_path, prep)
    packet_record = {"id": "RANK9-DEFENSEFORM8-PACKET-185", "status": "PREPARED_UNSENT", "group": GROUP, "pendingIds": IDS, "sourceAuthority": AUTHORITY, "packet": archive_binding, "preparation": bind(prep_path), "conversation": CHAT, "checksPassed": len(checks), "checksFailed": 0}
    packet_path = AUDIT / "RANK9_DEFENSEFORM8_PACKET_185.json"
    write_json(packet_path, packet_record)

    next_req = {"group": GROUP, "pendingIds": IDS, "pendingCount": 8, "status": "PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True, "packet": archive_binding, "packetRecord": bind(packet_path), "preparation": bind(prep_path), "candidate": current_group["candidate"], "archive": current_group["archive"]}
    queue_after = copy.deepcopy(queue)
    group_after = next(row for row in queue_after["currentPendingGroups"] if row["group"] == GROUP)
    group_after.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "preparedPacket": archive_binding, "packetRecord": bind(packet_path), "preparation": bind(prep_path), "freshPacketRequiredForCurrentAuthority": True})
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-185", "recordedAtUtc": ts, "next": next_req, "nextPreparedRequest": next_req, "nextGroup": GROUP, "packetStatus": "RANK9_DEFENSE_FORM8_SOURCE_PACKET_185_PREPARED_UNSENT_763_85", "currentPreparation": bind(prep_path), "currentPacket": bind(packet_path)})
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_185.json"
    write_json(queue_path, queue_after)

    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-185", "recordedAtUtc": ts, "status": "RANK9_DEFENSEFORM8_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_763_85", "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": 8, "nextPreparedRequest": next_req, "currentQueueBinding": bind(queue_path), "currentPreparation": bind(prep_path), "currentPacket": archive_binding, "resumePriority": "Send the current-source Defense/Form8 packet to the same GPT director; independently audit exact per-identity decisions, apply every accepted identity, push the batch, retain the six earlier source-evidence blockers, and continue until pending reaches zero."})
    handoff_path = AUDIT / "CURRENT_HANDOFF_185.json"
    write_json(handoff_path, handoff_after)

    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text("**Current ordinary spell-review handoff [185](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_185.json):** authority is 763 reviewed / 85 pending / 0 accepted-unapplied. A current-source packet for the eight Rank9 Defense/Form8 identities is prepared and awaits the GPT director. Six earlier identities remain held and carried forward. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_PACKET_185.json).\n\n" + old_start, encoding="utf-8")
    print(json.dumps({"status": "PREPARED_UNSENT", "commit": COMMIT, "authority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "sourceFiles": len(refreshed_bindings), "changedSinceOriginalPreparation": changed_since_preparation, "packet": archive_binding, "checksPassed": len(checks), "checksFailed": 0}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
