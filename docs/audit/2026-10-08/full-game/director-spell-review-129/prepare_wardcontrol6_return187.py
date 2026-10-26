from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP = "rank9-ward-control6"
IDS = [
    "greater-spell-turning", "nullification-wave", "eternal-ward",
    "ultimate-ward", "reality-anchor", "prismatic-sphere",
]
AUTHORITY = {
    "reviewedApplied": 766, "pending": 82, "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 490, "scopedInterfaces": 173,
}
SOURCE_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_ward_control_6_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Ward_Control_6_Source_Conference_01.zip"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_wardcontrol6_return187_prepared"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def bind(path: str | Path, raw: bytes) -> dict:
    path_text = Path(path).as_posix() if isinstance(path, Path) else path
    return {"path": path_text, "bytes": len(raw), "sha256": sha(raw)}


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "codex/ordinary-spell-review-complete"
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    assert all(line.endswith("prepare_wardcontrol6_return187.py") for line in dirty)
    assert not OUT.exists(), f"Output folder already exists: {OUT}"

    queue_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_186.json"
    pending_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT82_PENDING_IDENTITY_AUDIT_186.json"
    handoff_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_186.json"
    queue = read_json(git_blob(commit, queue_path))
    pending = read_json(git_blob(commit, pending_path))
    handoff = read_json(git_blob(commit, handoff_path))
    index = read_json(git_blob(commit, INDEX))
    catalog = read_json(git_blob(commit, CATALOG))
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 766, "pending": 82}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 490
    assert pending["pendingCount"] == 82 and len(pending["pendingIds"]) == 82

    source_candidate_raw = git_blob(commit, SOURCE_CANDIDATE)
    source_archive_raw = git_blob(commit, SOURCE_ARCHIVE)
    old_candidate = read_json(source_candidate_raw)
    candidate_path = Path(SOURCE_CANDIDATE)
    archive_path = Path(SOURCE_ARCHIVE)
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    # Read source bytes from the exact Git commit; working-tree line-ending conversion is irrelevant.
    queue_candidate_binding = target["candidate"]
    actual_candidate_binding = bind(SOURCE_CANDIDATE, source_candidate_raw)
    assert queue_candidate_binding["path"] == SOURCE_CANDIDATE
    assert queue_candidate_binding == actual_candidate_binding
    assert target["archive"]["path"] == SOURCE_ARCHIVE
    assert target["archive"]["bytes"] == len(source_archive_raw) and target["archive"]["sha256"] == sha(source_archive_raw)
    assert [row["spellId"] for row in old_candidate["records"]] == IDS
    assert len(old_candidate["sourceBindings"]) == 91

    entries = {row["id"]: row for row in index["entries"]}
    pending_ids = set(pending["pendingIds"])
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    assert set(IDS) <= pending_ids
    for spell_id in IDS:
        assert entries[spell_id]["authoredStatus"] == "pending-authored-procedure"
        assert entries[spell_id]["sourceStatus"] == "blocked-pending-operational-review"
        assert catalog_rows[spell_id]["operational"] is None

    historical_members: dict[str, bytes] = {}
    with zipfile.ZipFile(ROOT / SOURCE_ARCHIVE) as archive:
        names = archive.namelist()
        assert archive.testzip() is None and len(names) == len(set(names))
        assert all(safe_member(name) for name in names)
        for source in old_candidate["sourceBindings"]:
            raw = archive.read("sources/" + source["path"])
            assert len(raw) == source["bytes"] and sha(raw) == source["sha256"]
            historical_members[source["path"]] = raw

    refreshed_bindings = []
    current_sources: dict[str, bytes] = {}
    changed_since_candidate = []
    for old_binding in old_candidate["sourceBindings"]:
        source_path = old_binding["path"]
        assert safe_member(source_path) and not Path(source_path).is_absolute()
        raw = git_blob(commit, source_path)
        binding = {
            "path": source_path, "bytes": len(raw), "sha256": sha(raw),
            "gitBlobSHA1": git_blob_id(commit, source_path),
        }
        refreshed_bindings.append(binding)
        current_sources["sources_current/" + source_path] = raw
        if raw != historical_members[source_path]:
            changed_since_candidate.append({
                "path": source_path,
                "historicalBytes": len(historical_members[source_path]),
                "historicalSha256": sha(historical_members[source_path]),
                "currentBytes": len(raw), "currentSha256": sha(raw),
            })
    assert len(refreshed_bindings) == 91
    assert [row["path"] for row in changed_since_candidate] == [INDEX]

    timestamp = datetime.now(timezone.utc).isoformat()
    current_candidate = copy.deepcopy(old_candidate)
    current_candidate["historicalSourceBindings"] = copy.deepcopy(old_candidate["sourceBindings"])
    current_candidate["sourceBindings"] = refreshed_bindings
    current_candidate["currentSourceCommit"] = commit
    current_candidate["currentBranch"] = branch
    current_candidate["currentAuthority"] = AUTHORITY
    current_candidate["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current_candidate["historicalCandidateBinding"] = actual_candidate_binding
    current_candidate["queueCandidateBinding"] = copy.deepcopy(queue_candidate_binding)
    current_candidate["historicalSourceArchiveBinding"] = bind(SOURCE_ARCHIVE, source_archive_raw)
    current_candidate["sourceBindingRefresh"] = {
        "sourceFiles": len(refreshed_bindings),
        "changedSinceHistoricalCandidate": changed_since_candidate,
        "sourceContentsFromGitCommit": commit,
        "allSourceBindingsRefreshed": True,
    }
    current_candidate["countsUnchanged"] = {"reviewed": 766, "pending": 82}
    current_candidate["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_766_REVIEWED_82_PENDING_AUTHORITY"
    current_candidate["id"] = "RANK9-WARD-CONTROL6-CURRENT-SOURCE-CONTEXT-187"
    current_candidate["recordedAtUtc"] = timestamp
    for record in current_candidate["records"]:
        spell_id = record["spellId"]
        record["currentIndexEntry"] = copy.deepcopy(entries[spell_id])
        assert record["completeCurrentCatalogSourceAndAccess"] == catalog_rows[spell_id]
    candidate_raw = json_bytes(current_candidate)

    notes_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9WARDCONTROL6_NEXT_CONFERENCE_NOTES_129.json"
    historical_notes_raw = git_blob(commit, notes_path)
    historical_notes = read_json(historical_notes_raw)
    assert historical_notes["identities"] == IDS
    assert len(current_candidate["questions"]) == 24
    assert len(historical_notes["requiredNewCases"]) == 12

    latest = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186"
    current_paths = [
        INDEX, CATALOG, queue_path, pending_path, handoff_path,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_186.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_APPLICATION_186.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_186.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_RETURN186_RECEIPT.json",
        f"{latest}/MODEL.json", f"{latest}/CASEBOOK.json.gz", f"{latest}/HOLD_REGISTER.json",
        f"{latest}/PROCEDURES.json", f"{latest}/CANDIDATE_PACKAGE_MANIFEST.json",
    ]
    current_files = {"current/" + path: git_blob(commit, path) for path in current_paths}
    source_candidate_name = "CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json"
    context = {
        "id": "RANK9-WARD-CONTROL6-CURRENT-DIRECTOR-CONTEXT-187",
        "recordedAtUtc": timestamp,
        "sourceCommit": commit,
        "sourceBranch": branch,
        "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"],
        "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": queue_candidate_binding,
        "currentHistoricalCandidateBinding": actual_candidate_binding,
        "sourceRefresh": {"sourceFileCount": 91, "changedSinceCandidate": changed_since_candidate},
        "previousAppliedBatch": {
            "reviewId": "RANK9-DEFENSEFORM8-APPLICATION-186",
            "ids": ["astral-shell", "divine-shield", "eternal-protection"],
            "countsAfter": AUTHORITY,
            "acceptedUnapplied": 0,
        },
        "retainedHolds": {
            "defenseForm8": ["absolute-immunity", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"],
            "psychicFear7": ["psychic-scream", "mass-phantom-killer", "weird"],
            "deathRecovery7": ["doom", "final-word", "eternal-pact"],
        },
        "historicalNotesQualification": "The 129-era question supplement and branch list are included as requested coverage only. Revalidate each against current source snapshots; they do not select mechanics or supersede current files.",
        "qualification": "Preparation only. Static authored-procedure review; do not edit canonical files, do not execute supplied programs, and do not claim source/access, runtime, human playtest, balance, cosmology, domain-closure or release approval.",
    }

    request = (
        "GPT director — review exactly the six current pending Rank9 Ward/Control6 identities in this packet.\n\n"
        f"Source branch/commit: {branch} / {commit}. Current authority: 766 reviewed-applied / 82 pending / 0 accepted-unapplied; 490 complete reviewed standalone procedures; 173 scoped interfaces.\n\n"
        "Scope only: greater-spell-turning, nullification-wave, eternal-ward, ultimate-ward, reality-anchor, prismatic-sphere. Use the attached current handoff, queue, pending audit, index and catalog as authority. The queue candidate binding matches the current committed candidate exactly. The packet refreshes all 91 source files from the exact current Git commit; only the authored review index differs from the historical candidate's source binding set. Use sources_current/ and current/ for present authority; preserve the original conference ZIP and candidate as provenance.\n\n"
        "Recheck all 24 original unselected questions against the current sources. The two additional questions and twelve case requirements from the 129-era notes are targeted historical coverage proposals, not selected rules; include them only where still source-relevant. Preserve each native card and access route, both Reality Anchor placements, all-spell reflection, no-save Nullification Wave, full Eternal Ward site suite, the full 24-hour Ultimate Ward scope, and all seven Prismatic Sphere functions. Resolve source-pair conflicts explicitly and keep each unresolved identity held on exact evidence gaps. Do not weaken benefits silently, import external mechanics, or infer a global rank rule.\n\n"
        "Return one complete source-faithful procedure and complete reversible cases for each identity. Mark only individually passing IDs accepted=true/applied=false; keep every other ID unaccepted with exact blocker/qualification IDs. Preserve original question dispositions, all source and future obligations, full event/state/cost/provenance histories, and deterministic cleanup. Report procedures, questions, cases, events, forward/inverse operations, holds and validation counts. Include a member manifest with exact hashes and a separate delivery JSON bound to the returned ZIP. Keep runtime, implementation, playtest, balance, cosmology, completion and release gates separate. Do not edit canonical files or execute supplied/historical programs. After I independently audit the return, apply only exact accepted IDs and continue in queue order until pending reaches zero."
    )

    current_context_raw = json_bytes(context)
    request_raw = request.encode("utf-8")
    files: dict[str, bytes] = {
        "CURRENT_CONTEXT_187.json": current_context_raw,
        source_candidate_name: candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": source_candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": source_archive_raw,
        "HISTORICAL_NOTES/RANK9WARDCONTROL6_NEXT_CONFERENCE_NOTES_129.json": historical_notes_raw,
        "REQUEST_187.txt": request_raw,
        **current_files,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)

    OUT.mkdir(parents=True, exist_ok=False)
    candidate_out = OUT / source_candidate_name
    candidate_out.write_bytes(candidate_raw)
    packet_path = OUT / "DD_Rank9_WardControl6_CurrentSource_187.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        rows = []
        for name in sorted(files):
            raw = files[name]
            archive.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {
            "id": "RANK9-WARD-CONTROL6-CURRENT-SOURCE-PACKET-MANIFEST-187",
            "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
            "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows,
        }
        archive.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet_path) as archive:
        names = archive.namelist()
        assert archive.testzip() is None and len(names) == len(set(names)) == len(rows) + 1
        assert all(safe_member(name) for name in names)
        for row in rows:
            raw = archive.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]
        assert read_json(archive.read("MANIFEST.json"))["members"] == rows

    packet_binding = bind(packet_path.relative_to(ROOT).as_posix(), packet_path.read_bytes())
    candidate_binding = bind(candidate_out.relative_to(ROOT).as_posix(), candidate_raw)
    prep_path = AUDIT / "RANK9_WARDCONTROL6_SOURCE_PREPARATION_187.json"
    prep = {
        "id": "RANK9-WARD-CONTROL6-SOURCE-PREPARATION-187",
        "recordedAtUtc": timestamp, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "group": GROUP, "pendingIds": IDS,
        "historicalCandidate": actual_candidate_binding,
        "queueCandidateBinding": queue_candidate_binding,
        "historicalSourceArchive": bind(SOURCE_ARCHIVE, source_archive_raw),
        "currentDerivedCandidate": candidate_binding,
        "sourceFileCount": len(refreshed_bindings), "changedSinceHistoricalCandidate": changed_since_candidate,
        "packet": packet_binding, "deliveryManifest": {"path": (OUT / "DD_Rank9_WardControl6_CurrentSource_187_DELIVERY.json").relative_to(ROOT).as_posix()},
        "memberCount": len(rows) + 1, "checksPassed": 9, "checksFailed": 0,
        "checks": [
            {"check": "Current handoff, queue, pending audit, authored index and catalog agree on 766/82/0", "passed": True},
            {"check": "Exactly the six queue-selected Ward/Control6 IDs remain pending", "passed": True},
            {"check": "Historical archive matches the current queue archive binding and passes CRC/safety checks", "passed": True},
            {"check": "All 91 historical source bindings match their exact archive members", "passed": True},
            {"check": "All 91 source files are refreshed from the exact current Git commit", "passed": True},
            {"check": "Only the authored review index differs from the historical candidate bindings", "passed": True},
            {"check": "All six live catalog cards and pending index entries are preserved exactly", "passed": True},
            {"check": "Current accepted context, latest model, casebook, holds and receipts are included", "passed": True},
            {"check": "Packet ZIP is CRC-clean; all unique safe members match its SHA-256/CRC manifest", "passed": True, "detail": {"memberCount": len(rows) + 1, "bytes": packet_path.stat().st_size, "sha256": sha(packet_path.read_bytes())}},
        ],
        "canonicalChangesBeforePreparation": False,
        "request": request,
    }
    prep_raw = json_bytes(prep)
    prep_path.write_bytes(prep_raw)
    delivery = {
        "id": "RANK9-WARD-CONTROL6-DIRECTOR-CONTEXT-DELIVERY-187",
        "status": "PREPARED_UNSENT", "archive": packet_binding,
        "members": len(rows) + 1, "manifestBindings": len(rows),
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "group": GROUP, "pendingIds": IDS,
        "candidate": candidate_binding,
        "historicalArchive": bind(SOURCE_ARCHIVE, source_archive_raw),
        "sourceFilesRefreshed": len(refreshed_bindings),
        "sourceFilesChangedSinceHistoricalCandidate": changed_since_candidate,
        "accepted": False, "applied": False, "conversation": CHAT,
    }
    delivery_path = OUT / "DD_Rank9_WardControl6_CurrentSource_187_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)
    prep["deliveryManifest"] = delivery_binding
    prep_raw = json_bytes(prep)
    prep_path.write_bytes(prep_raw)
    prep_binding = bind(prep_path.relative_to(ROOT).as_posix(), prep_raw)

    packet_record_path = AUDIT / "RANK9_WARDCONTROL6_PACKET_187.json"
    packet_record = {
        "id": "RANK9-WARD-CONTROL6-PACKET-187", "status": "PREPARED_UNSENT",
        "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
        "packet": packet_binding, "deliveryManifest": delivery_binding,
        "preparation": prep_binding,
        "conversation": CHAT, "checksPassed": 9, "checksFailed": 0,
    }
    packet_record_raw = json_bytes(packet_record)
    packet_record_path.write_bytes(packet_record_raw)
    packet_record_binding = bind(packet_record_path.relative_to(ROOT).as_posix(), packet_record_raw)

    pending_after = copy.deepcopy(pending)
    pending_after.update({"id": "CURRENT82-PENDING-IDENTITY-AUDIT-187", "recordedAtUtc": timestamp})
    pending_after["preparedNextGroup"] = {"group": GROUP, "pendingIds": IDS, "packet": packet_binding}
    pending_path_after = AUDIT / "CURRENT82_PENDING_IDENTITY_AUDIT_187.json"
    pending_after_raw = json_bytes(pending_after)
    pending_path_after.write_bytes(pending_after_raw)
    pending_binding = bind(pending_path_after.relative_to(ROOT).as_posix(), pending_after_raw)

    next_request = {
        "group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS),
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority": False,
        "packet": packet_binding, "deliveryManifest": delivery_binding,
        "packetRecord": packet_record_binding, "preparation": prep_binding,
        "candidate": candidate_binding,
        "historicalCandidate": actual_candidate_binding,
        "archive": bind(SOURCE_ARCHIVE, source_archive_raw),
    }
    queue_after = copy.deepcopy(queue)
    target_after = next(row for row in queue_after["currentPendingGroups"] if row["group"] == GROUP)
    target_after.update({
        "candidate": candidate_binding, "historicalCandidate": actual_candidate_binding,
        "historicalCandidateBinding": queue_candidate_binding,
        "archive": bind(SOURCE_ARCHIVE, source_archive_raw),
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "preparedPacket": packet_binding, "deliveryManifest": delivery_binding,
        "packetRecord": packet_record_binding, "preparation": prep_binding,
        "freshPacketRequiredForCurrentAuthority": False,
    })
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-187", "recordedAtUtc": timestamp,
        "next": next_request, "nextPreparedRequest": next_request,
        "nextGroup": GROUP, "pendingIdentityAudit": pending_binding,
        "packetStatus": "RANK9_WARD_CONTROL6_CURRENT_SOURCE_PACKET_187_PREPARED_UNSENT_766_82",
        "currentPreparation": prep_binding, "currentPacket": packet_binding,
        "currentPacketDelivery": delivery_binding,
    })
    queue_path_after = AUDIT / "CURRENT_SPELL_QUEUE_187.json"
    queue_after_raw = json_bytes(queue_after)
    queue_path_after.write_bytes(queue_after_raw)
    queue_binding = bind(queue_path_after.relative_to(ROOT).as_posix(), queue_after_raw)

    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-187", "recordedAtUtc": timestamp,
        "status": "RANK9_WARD_CONTROL6_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_766_82",
        "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": len(IDS),
        "pendingIdentityAudit": pending_binding,
        "nextPreparedRequest": next_request,
        "currentQueueBinding": queue_binding,
        "currentPreparation": prep_binding, "currentPacket": packet_binding,
        "currentPacketDelivery": delivery_binding,
        "resumePriority": "Send the fresh 91-source Ward/Control6 packet to the same GPT director; independently audit exact per-identity returns, apply only accepted IDs, push the batch, and continue in queue order until pending reaches zero.",
    })
    handoff_path_after = AUDIT / "CURRENT_HANDOFF_187.json"
    handoff_after_raw = json_bytes(handoff_after)
    handoff_path_after.write_bytes(handoff_after_raw)

    snapshot = (
        "# Current ordinary spell-review checkpoint 187\n\n"
        "Authority is **766 reviewed / 82 pending / 0 accepted-unapplied**, with 490 complete reviewed standalone procedures. The next six-identity group is Rank9 Ward/Control6. Its fresh current-source packet refreshes all 91 bindings from the pushed source commit; only the authored review index differs from the historical candidate.\n\n"
        f"See [handoff 187](docs/audit/2026-10-08/full-game/director-spell-review-129/{handoff_path_after.name}), [queue 187](docs/audit/2026-10-08/full-game/director-spell-review-129/{queue_path_after.name}), [pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{pending_path_after.name}), [packet record](docs/audit/2026-10-08/full-game/director-spell-review-129/{packet_record_path.name}), and [source packet](docs/audit/2026-10-08/full-game/director-spell-review-129/{OUT.name}/{packet_path.name}).\n"
    )
    (AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_187.md").write_text(snapshot, encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(
        f"**Current ordinary spell-review handoff [187](docs/audit/2026-10-08/full-game/director-spell-review-129/{handoff_path_after.name}):** authority is 766 reviewed / 82 pending / 0 accepted-unapplied. A fresh 91-source packet for Rank9 Ward/Control6 is prepared for the GPT director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/{packet_record_path.name}).\n\n" + old_start,
        encoding="utf-8", newline="\n",
    )

    print(json.dumps({
        "status": "PREPARED_UNSENT", "sourceCommit": commit,
        "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
        "sourceFiles": len(refreshed_bindings), "changedSinceHistoricalCandidate": changed_since_candidate,
        "packet": packet_binding, "deliveryManifest": delivery_binding,
        "packetRecord": packet_record_binding, "queue": queue_binding,
        "handoff": bind(handoff_path_after.relative_to(ROOT).as_posix(), handoff_path_after.read_bytes()),
        "checksPassed": 9, "checksFailed": 0,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
