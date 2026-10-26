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
FULL = ROOT / "docs/audit/2026-10-08/full-game"
GROUP = "rank9-time-fate6"
IDS = ["time-stop", "time-fracture", "foresight-perfect", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
AUTHORITY = {"reviewedApplied": 777, "pending": 71, "acceptedUnapplied": 0, "completeStandaloneProcedures": 501, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_190.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT71_PENDING_IDENTITY_AUDIT_190.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_190.json"
SOURCE_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_time_fate_6_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Time_Fate_6_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9TIMEFATE6_NEXT_CONFERENCE_NOTES_129.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_timefate6_current_source_191_prepared"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def bind(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") and not x.startswith(".") for x in p.parts)


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "codex/ordinary-spell-review-complete"
    assert subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=ROOT, text=True).split()[0] == commit
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    assert all(line.endswith("prepare_time_fate6_current_191.py") for line in dirty), dirty
    assert not OUT.exists()

    queue, pending, handoff, index, catalog = [read(blob(commit, p)) for p in (QUEUE, PENDING, HANDOFF, INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 777, "pending": 71}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 501
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 71
    target = next(r for r in queue["currentPendingGroups"] if r["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    candidate_raw, archive_raw = blob(commit, SOURCE_CANDIDATE), blob(commit, SOURCE_ARCHIVE)
    old_candidate = read(candidate_raw)
    assert [r["spellId"] for r in old_candidate["records"]] == IDS
    assert len(old_candidate["sourceBindings"]) == 140
    assert target["candidate"] == bind(SOURCE_CANDIDATE, candidate_raw)
    assert target["archive"]["path"] == SOURCE_ARCHIVE and target["archive"]["bytes"] == len(archive_raw) and target["archive"]["sha256"] == sha(archive_raw)
    entries = {r["id"]: r for r in index["entries"]}
    pending_ids = set(pending["pendingIds"])
    catalog_rows = {r["id"]: r for r in catalog["spells"]}
    assert set(IDS) <= pending_ids
    for record in old_candidate["records"]:
        sid = record["spellId"]
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert entries[sid] == record["currentIndexEntry"]
        assert catalog_rows[sid]["id"] == sid
        pointer = entries[sid]["wholeCardPointer"]
        assert pointer == record["currentIndexEntry"]["wholeCardPointer"]
        catalog_i = int(pointer.rsplit("/", 1)[1])
        assert catalog["spells"][catalog_i]["id"] == sid

    historical_members = {}
    with zipfile.ZipFile(FULL / Path(SOURCE_ARCHIVE).name) as archive:
        names = archive.namelist()
        assert archive.testzip() is None and len(names) == len(set(names)) and all(safe_member(n) for n in names)
        for source in old_candidate["sourceBindings"]:
            raw = archive.read("sources/" + source["path"])
            assert len(raw) == source["bytes"] and sha(raw) == source["sha256"]
            historical_members[source["path"]] = raw

    refreshed, current_sources, changed = [], {}, []
    for old in old_candidate["sourceBindings"]:
        path = old["path"]
        assert safe_member(path) and not Path(path).is_absolute()
        raw = blob(commit, path)
        refreshed.append({"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": blob_id(commit, path)})
        current_sources["sources_current/" + path] = raw
        if raw != historical_members[path]:
            changed.append({"path": path, "historicalBytes": len(historical_members[path]), "historicalSha256": sha(historical_members[path]), "currentBytes": len(raw), "currentSha256": sha(raw)})
    assert len(refreshed) == 140

    now = datetime.now(timezone.utc).isoformat()
    current = copy.deepcopy(old_candidate)
    current["historicalSourceBindings"] = copy.deepcopy(old_candidate["sourceBindings"])
    current["sourceBindings"] = refreshed
    current["currentSourceCommit"] = commit
    current["currentBranch"] = branch
    current["currentAuthority"] = AUTHORITY
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current["historicalCandidateBinding"] = bind(SOURCE_CANDIDATE, candidate_raw)
    current["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    current["historicalSourceArchiveBinding"] = bind(SOURCE_ARCHIVE, archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed, "sourceContentsFromGitCommit": commit, "allSourceBindingsRefreshed": True}
    current["countsUnchanged"] = {"reviewed": 777, "pending": 71}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_777_REVIEWED_71_PENDING_AUTHORITY"
    current["id"] = "RANK9-TIME-FATE6-CURRENT-SOURCE-CONTEXT-191"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[record["spellId"]])
    current_raw = json_bytes(current)

    notes_raw = blob(commit, NOTES)
    notes = read(notes_raw)
    assert notes["identities"] == IDS and len(notes["allQuestions"]) == 34 and len(notes["requiredNewCases"]) == 12
    assert len(notes["focusedAdditionalQuestions"]) == 2

    previous = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01"
    current_paths = [
        INDEX, CATALOG, QUEUE, PENDING, HANDOFF,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_EXACT_ACCEPTANCE_190_RECONCILED01.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_APPLICATION_190_RECONCILED01.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_APPLICATION_VALIDATION_190_RECONCILED01.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_RECEIPT.json",
        f"{previous}/MODEL.json", f"{previous}/CASEBOOK.json.gz", f"{previous}/HOLD_REGISTER.json",
        f"{previous}/PROCEDURES.json", f"{previous}/CANDIDATE_PACKAGE_MANIFEST.json",
        *[f"{previous}/procedures/{sid}.json" for sid in ["command-reality", "dominate-legion", "erase-soul", "overwhelming-presence", "perfect-mesmerize", "prophecy-fulfilled", "rewrite-loyalty"]],
    ]
    current_files = {"current/" + p: blob(commit, p) for p in current_paths}

    blockers = {
        "absolute-domination": "AG190-B01 remains held: genuine acquired extra-turn source is still not evidenced.",
        "puppetmaster-s-realm": "AG190-B02 remains held: native Multiattack profile and reach evidence are still incomplete.",
    }
    context = {
        "id": "RANK9-TIME-FATE6-CURRENT-DIRECTOR-CONTEXT-191",
        "recordedAtUtc": now,
        "sourceCommit": commit,
        "sourceBranch": branch,
        "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"],
        "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": target["candidate"],
        "historicalCandidateBinding": bind(SOURCE_CANDIDATE, candidate_raw),
        "historicalSourceArchiveBinding": bind(SOURCE_ARCHIVE, archive_raw),
        "sourceRefresh": {"sourceFileCount": 140, "changedSinceCandidate": changed},
        "previousAppliedBatch": {"reviewId": "RANK9-AGENCYCONTROL9-APPLICATION-190-RECONCILED01", "acceptedSpellIds": ["command-reality", "dominate-legion", "erase-soul", "overwhelming-presence", "perfect-mesmerize", "prophecy-fulfilled", "rewrite-loyalty"], "countsAfter": AUTHORITY, "acceptedUnapplied": 0},
        "retainedBlockersOutsideScope": blockers,
        "qualification": "Preparation only. Revalidate the complete historical Time/Fate source conference against refreshed current bindings and included accepted context. Do not edit canonical files, execute supplied programs, or claim runtime, implementation, human-play, balance, cosmology, domain-closure, or release approval.",
    }
    request = (
        "GPT director — review exactly the six current pending Rank9 Time/Fate identities in this packet.\n\n"
        f"Source branch/commit: {branch} / {commit}. Current authority: 777 reviewed-applied / 71 pending / 0 accepted-unapplied; 501 complete reviewed standalone procedures; 173 scoped interfaces.\n\n"
        "Scope only: time-stop, time-fracture, foresight-perfect, fate-rewrite, collapse-timeline, eternal-prophecy. Use the attached current handoff, queue, pending audit, index and catalog as authority. The historical candidate and source archive are provenance; all 140 historical source bindings are refreshed from this exact pushed commit, with sources_current/ holding those bytes. Use current/ for present authority, including the seven accepted Agency/Control9 procedures and their independently reconciled application.\n\n"
        "Recheck all 34 original questions, both focused addenda, and all 12 targeted case requirements against the actual bound source files. Historical recommendations are not selected rules. Preserve each native card, access route, component, duration, save cadence and distinct effect. Resolve source conflicts explicitly. Keep unresolved branches held on exact evidence gaps. Do not invent CR limits, free turns, extra actions, extra saves, resource pools, global mental flags, actor capabilities, or source permissions.\n\n"
        "For Time Stop and Time Fracture, demonstrate actual lawful clocks, triggers, deadlines, rolls, replacement and reroll lineage, useful agency, suppression and terminal cleanup. For Foresight Perfect, retain the native selection and actual effects without adding detection or use depletion. For Fate Rewrite, Collapse Timeline and Eternal Prophecy, demonstrate admissible causality, objective predicates, complete lawful histories, unique custody, witnesses, retained costs, and atomic settlement without duplicating bodies, rewards or guarantees. Use a deterministic authored Director policy where the notes call for one; do not claim external agents or a year of runtime from fixture calculations.\n\n"
        "Return one source-faithful static procedure and complete reversible cases for each identity. Mark only individually passing IDs accepted=true/applied=false; keep all others unaccepted with exact blocker and qualification IDs. Preserve original questions and future obligations, full event/state/cost/provenance histories, deterministic cleanup, and native source bindings. Report procedure, question, case, branch, event, forward/inverse-operation, hold and validation counts. Include a member manifest with exact hashes and a separate delivery JSON bound to the returned ZIP. Carry the named Return190 Agency blockers forward unchanged; keep runtime, implementation, playtest, balance, cosmology, completion and release gates separate. Do not edit canonical files or execute supplied programs. After I independently audit the return, apply only exact accepted IDs and continue in queue order until pending reaches zero."
    )

    files: dict[str, bytes] = {
        "CURRENT_CONTEXT_191.json": json_bytes(context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_191.json": current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9TIMEFATE6_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_191.txt": request.encode("utf-8"),
        **current_files,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(k) for k in files)
    OUT.mkdir(parents=True, exist_ok=False)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_191.json"
    candidate_path.write_bytes(current_raw)
    packet_path = OUT / "DD_Rank9_TimeFate6_CurrentSource_191.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        rows = []
        for name in sorted(files):
            raw = files[name]
            z.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {"id": "RANK9-TIME-FATE6-CURRENT-SOURCE-PACKET-MANIFEST-191", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows}
        z.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet_path) as z:
        assert z.testzip() is None and len(z.namelist()) == len(rows) + 1 and len(set(z.namelist())) == len(rows) + 1
        for row in rows:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]

    packet_binding = bind(packet_path.relative_to(ROOT).as_posix(), packet_path.read_bytes())
    candidate_binding = bind(candidate_path.relative_to(ROOT).as_posix(), current_raw)
    delivery = {"id": "RANK9-TIME-FATE6-CURRENT-SOURCE-DELIVERY-191", "status": "PREPARED_UNSENT", "archive": packet_binding, "members": len(rows) + 1, "manifestBindings": len(rows), "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "historicalSourceArchive": bind(SOURCE_ARCHIVE, archive_raw), "sourceFilesRefreshed": 140, "sourceFilesChangedSinceHistoricalCandidate": changed, "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_TimeFate6_CurrentSource_191_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)

    preparation_path = AUDIT / "RANK9_TIMEFATE6_SOURCE_PREPARATION_191.json"
    checks = [
        ("Source commit is the pushed current branch head", True),
        ("Current queue, handoff, pending audit, index, and catalog agree on 777/71/0", True),
        ("Exactly the six Time/Fate identities remain pending and are next in queue order", True),
        ("All 140 historical source members match the archived exact hashes", True),
        ("All 140 source bindings refreshed from the exact current Git commit", True),
        ("All six current native index entries and catalog pointers match", True),
        ("Return190 accepted context, exact procedures, holds, casebook, and application evidence included", True),
        ("All 34 original questions, two focused addenda, and 12 targeted cases preserved", True),
        ("Historical Time/Fate source archive validates with no duplicate or unsafe members", True),
        ("Packet ZIP CRC and all unique safe members match SHA/CRC manifest", True),
    ]
    preparation = {"id": "RANK9-TIME-FATE6-SOURCE-PREPARATION-191", "recordedAtUtc": now, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "historicalArchive": bind(SOURCE_ARCHIVE, archive_raw), "currentDerivedCandidate": candidate_binding, "sourceFileCount": 140, "changedSinceHistoricalCandidate": changed, "packet": packet_binding, "deliveryManifest": delivery_binding, "memberCount": len(rows) + 1, "checksPassed": len(checks), "checksFailed": 0, "checks": [{"check": title, "passed": passed} for title, passed in checks], "canonicalChangesBeforePreparation": False, "request": request}
    preparation_path.write_bytes(json_bytes(preparation))
    prep_binding = bind(preparation_path.relative_to(ROOT).as_posix(), preparation_path.read_bytes())
    packet_record_path = AUDIT / "RANK9_TIMEFATE6_PACKET_191.json"
    packet_record = {"id": "RANK9-TIME-FATE6-PACKET-191", "status": "PREPARED_UNSENT", "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding, "preparation": prep_binding, "conversation": CHAT, "checksPassed": len(checks), "checksFailed": 0}
    packet_record_path.write_bytes(json_bytes(packet_record))
    packet_record_binding = bind(packet_record_path.relative_to(ROOT).as_posix(), packet_record_path.read_bytes())

    pending_after = copy.deepcopy(pending)
    pending_after.update({"id": "CURRENT71-PENDING-IDENTITY-AUDIT-191", "recordedAtUtc": now, "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding}})
    pending_after_path = AUDIT / "CURRENT71_PENDING_IDENTITY_AUDIT_191.json"
    pending_after_path.write_bytes(json_bytes(pending_after))
    pending_binding = bind(pending_after_path.relative_to(ROOT).as_posix(), pending_after_path.read_bytes())
    next_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": False, "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding, "preparation": prep_binding, "candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "archive": bind(SOURCE_ARCHIVE, archive_raw)}
    queue_after = copy.deepcopy(queue)
    target_after = next(r for r in queue_after["currentPendingGroups"] if r["group"] == GROUP)
    target_after.update({"candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "archive": bind(SOURCE_ARCHIVE, archive_raw), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "preparedPacket": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding, "preparation": prep_binding, "freshPacketRequiredForCurrentAuthority": False})
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-191", "recordedAtUtc": now, "next": next_request, "nextPreparedRequest": next_request, "nextGroup": GROUP, "pendingIdentityAudit": pending_binding, "packetStatus": "RANK9_TIME_FATE6_CURRENT_SOURCE_PACKET_191_PREPARED_UNSENT_777_71", "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding})
    queue_path_after = AUDIT / "CURRENT_SPELL_QUEUE_191.json"
    queue_path_after.write_bytes(json_bytes(queue_after))
    queue_binding = bind(queue_path_after.relative_to(ROOT).as_posix(), queue_path_after.read_bytes())
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-191", "recordedAtUtc": now, "status": "RANK9_TIME_FATE6_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_777_71", "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": len(IDS), "pendingIdentityAudit": pending_binding, "nextPreparedRequest": next_request, "currentQueueBinding": queue_binding, "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding, "resumePriority": "Send the fresh 140-source Time/Fate6 packet to the same GPT director; independently audit exact per-identity returns, apply only accepted IDs, push each batch, and continue in queue order until pending reaches zero."})
    handoff_path_after = AUDIT / "CURRENT_HANDOFF_191.json"
    handoff_path_after.write_bytes(json_bytes(handoff_after))
    snapshot = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_191.md"
    snapshot.write_text(f"# Current ordinary spell-review checkpoint 191\n\nAuthority is **777 reviewed / 71 pending / 0 accepted-unapplied**, with 501 complete reviewed standalone procedures. The next six-identity group is Rank9 Time/Fate6. Its fresh packet refreshes all 140 historical source bindings from the pushed 777/71 commit and includes the accepted Agency/Control9 context and its two retained blockers.\n\nSee [handoff](CURRENT_HANDOFF_191.json), [queue](CURRENT_SPELL_QUEUE_191.json), [pending audit](CURRENT71_PENDING_IDENTITY_AUDIT_191.json), [packet record](RANK9_TIMEFATE6_PACKET_191.json), and [source packet](rank9_timefate6_current_source_191_prepared/DD_Rank9_TimeFate6_CurrentSource_191.zip).\n", encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig")
    start.write_text(f"**Current ordinary spell-review handoff [191](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_191.json):** authority is 777 reviewed / 71 pending / 0 accepted-unapplied. A fresh 140-source packet for Rank9 Time/Fate6 is prepared for the GPT director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_PACKET_191.json).\n\n" + old_start, encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY, "group": GROUP, "sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed, "packet": packet_binding, "deliveryManifest": delivery_binding, "queue": queue_binding, "checksPassed": len(checks)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
