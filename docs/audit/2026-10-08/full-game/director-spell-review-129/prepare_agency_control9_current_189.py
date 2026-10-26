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
GROUP = "rank9-agency-control9"
IDS = ["absolute-domination", "command-reality", "dominate-legion", "erase-soul", "overwhelming-presence", "perfect-mesmerize", "prophecy-fulfilled", "puppetmaster-s-realm", "rewrite-loyalty"]
AUTHORITY = {"reviewedApplied": 770, "pending": 78, "acceptedUnapplied": 0, "completeStandaloneProcedures": 494, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_188.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT78_PENDING_IDENTITY_AUDIT_188.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_188.json"
SOURCE_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_agency_control_9_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Agency_Control_9_Source_Conference_01.zip"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_agencycontrol9_return189_prepared"


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
    assert all(line.endswith("prepare_agency_control9_current_189.py") for line in dirty), dirty
    assert not OUT.exists()
    queue, pending, handoff, index, catalog = [read(blob(commit, p)) for p in (QUEUE, PENDING, HANDOFF, INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 770, "pending": 78}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 494
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 78
    target = next(r for r in queue["currentPendingGroups"] if r["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    candidate_raw, archive_raw = blob(commit, SOURCE_CANDIDATE), blob(commit, SOURCE_ARCHIVE)
    old_candidate = read(candidate_raw)
    assert [r["spellId"] for r in old_candidate["records"]] == IDS
    assert len(old_candidate["sourceBindings"]) == 96
    assert target["candidate"] == bind(SOURCE_CANDIDATE, candidate_raw)
    assert target["archive"]["path"] == SOURCE_ARCHIVE and target["archive"]["bytes"] == len(archive_raw) and target["archive"]["sha256"] == sha(archive_raw)
    entries = {r["id"]: r for r in index["entries"]}
    pending_ids = set(pending["pendingIds"])
    catalog_rows = {r["id"]: r for r in catalog["spells"]}
    assert set(IDS) <= pending_ids
    for sid in IDS:
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert entries[sid]["wholeCardPointer"] == next(r for r in old_candidate["records"] if r["spellId"] == sid)["currentIndexEntry"]["wholeCardPointer"]
        assert catalog_rows[sid] == next(r for r in old_candidate["records"] if r["spellId"] == sid)["completeCurrentCatalogSourceAndAccess"]

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
    assert len(refreshed) == 96

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
    current["countsUnchanged"] = {"reviewed": 770, "pending": 78}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_770_REVIEWED_78_PENDING_AUTHORITY"
    current["id"] = "RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-CONTEXT-189"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        sid = record["spellId"]
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        assert record["completeCurrentCatalogSourceAndAccess"] == catalog_rows[sid]
    current_raw = json_bytes(current)

    notes_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9AGENCYCONTROL9_NEXT_CONFERENCE_NOTES_129.json"
    notes_raw = blob(commit, notes_path)
    notes = read(notes_raw)
    assert notes["identities"] == IDS and len(notes["allQuestions"]) == 34 and len(notes["requiredNewCases"]) == 18
    latest = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9wardcontrol6_reviewed_188"
    current_paths = [
        INDEX, CATALOG, QUEUE, PENDING, HANDOFF,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_EXACT_ACCEPTANCE_188.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_APPLICATION_188.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_APPLICATION_VALIDATION_188.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_RETURN188_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_RETURN188_RECEIPT.json",
        f"{latest}/MODEL.json", f"{latest}/CASEBOOK.json.gz", f"{latest}/HOLD_REGISTER.json",
        f"{latest}/PROCEDURES.json", f"{latest}/CANDIDATE_PACKAGE_MANIFEST.json",
    ]
    current_files = {"current/" + p: blob(commit, p) for p in current_paths}
    source_name = "CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json"
    context = {"id": "RANK9-AGENCY-CONTROL9-CURRENT-DIRECTOR-CONTEXT-189", "recordedAtUtc": now, "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)}, "currentIndexCounts": index["authoredCounts"], "currentPendingAudit": pending["id"], "historicalQueueCandidateBinding": target["candidate"], "currentHistoricalCandidateBinding": bind(SOURCE_CANDIDATE, candidate_raw), "sourceRefresh": {"sourceFileCount": 96, "changedSinceCandidate": changed}, "previousAppliedBatch": {"reviewId": "RANK9-WARDCONTROL6-APPLICATION-188", "ids": ["greater-spell-turning", "eternal-ward", "ultimate-ward", "prismatic-sphere"], "countsAfter": AUTHORITY, "acceptedUnapplied": 0}, "retainedReturn188Holds": {"nullification-wave": ["WC188-B01", "WC188-H-UNIQUE-PROPERTY"], "reality-anchor": ["WC188-B02", "WC188-H-UNIQUE-PROPERTY"]}, "qualification": "Preparation only. Revalidate the complete historical source conference against the refreshed current bindings and included accepted context. Do not edit canonical files, execute supplied programs, or claim runtime, implementation, human-play, balance, cosmology, domain-closure, or release approval."}
    request = (
        "GPT director — review exactly the nine current pending Rank9 Agency/Control9 identities in this packet.\n\n"
        f"Source branch/commit: {branch} / {commit}. Current authority: 770 reviewed-applied / 78 pending / 0 accepted-unapplied; 494 complete reviewed standalone procedures; 173 scoped interfaces.\n\n"
        "Scope only: absolute-domination, command-reality, dominate-legion, erase-soul, overwhelming-presence, perfect-mesmerize, prophecy-fulfilled, puppetmaster-s-realm, rewrite-loyalty. Use the attached current handoff, queue, pending audit, index and catalog as authority. The historical candidate and source archive are preserved as provenance; all 96 historical source bindings are refreshed from the exact current Git commit and current index entries. Use sources_current/ and current/ for present authority.\n\n"
        "Recheck all 34 original unselected questions and 18 targeted case requirements against the actual source files. Historical question recommendations are not selected rules. Preserve each native card, access route, component, duration, save cadence and distinct mental/command/identity component. Show useful lawful outcomes and complete actual actor/resource histories; preserve original memories and institutional facts where relevant. Do not invent CR limits, free turns, extra actions, extra saves, resource pools, global mental flags or source permissions. Resolve source conflicts explicitly and keep unresolved identity branches held on exact evidence gaps. Carry WC188-B01 and WC188-B02 forward without reopening or weakening those two identities.\n\n"
        "Return one source-faithful static procedure and complete reversible cases for each identity. Mark only individually passing IDs accepted=true/applied=false; keep every other ID unaccepted with exact blocker and qualification IDs. Preserve original questions and future obligations, full event/state/cost/provenance histories, deterministic cleanup, and native source bindings. Report procedure, question, case, branch, event, forward/inverse-operation, hold and validation counts. Include a member manifest with exact hashes and a separate delivery JSON bound to the returned ZIP. Keep runtime, implementation, playtest, balance, cosmology, completion and release gates separate. Do not edit canonical files or execute supplied programs. After I independently audit the return, apply only exact accepted IDs and continue in queue order until pending reaches zero."
    )
    files: dict[str, bytes] = {
        "CURRENT_CONTEXT_189.json": json_bytes(context), source_name: current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9AGENCYCONTROL9_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_189.txt": request.encode("utf-8"), **current_files, **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(k) for k in files)
    OUT.mkdir(parents=True, exist_ok=False)
    candidate_path = OUT / source_name
    candidate_path.write_bytes(current_raw)
    packet_path = OUT / "DD_Rank9_AgencyControl9_CurrentSource_189.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        rows = []
        for name in sorted(files):
            raw = files[name]
            z.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        z.writestr("MANIFEST.json", json_bytes({"id": "RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-PACKET-MANIFEST-189", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows}), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet_path) as z:
        assert z.testzip() is None and len(z.namelist()) == len(rows) + 1 and len(set(z.namelist())) == len(rows) + 1
        for row in rows:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]

    packet_binding = bind(packet_path.relative_to(ROOT).as_posix(), packet_path.read_bytes())
    candidate_binding = bind(candidate_path.relative_to(ROOT).as_posix(), current_raw)
    delivery = {"id": "RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-DELIVERY-189", "status": "PREPARED_UNSENT", "archive": packet_binding, "members": len(rows) + 1, "manifestBindings": len(rows), "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding, "historicalSourceArchive": bind(SOURCE_ARCHIVE, archive_raw), "sourceFilesRefreshed": 96, "sourceFilesChangedSinceHistoricalCandidate": changed, "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_AgencyControl9_CurrentSource_189_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)
    preparation_path = AUDIT / "RANK9_AGENCYCONTROL9_SOURCE_PREPARATION_189.json"
    preparation = {"id": "RANK9-AGENCY-CONTROL9-SOURCE-PREPARATION-189", "recordedAtUtc": now, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "historicalArchive": bind(SOURCE_ARCHIVE, archive_raw), "currentDerivedCandidate": candidate_binding, "sourceFileCount": 96, "changedSinceHistoricalCandidate": changed, "packet": packet_binding, "deliveryManifest": delivery_binding, "memberCount": len(rows) + 1, "checksPassed": 9, "checksFailed": 0, "checks": [{"check": "Source commit is the pushed current branch head", "passed": True}, {"check": "Current queue, handoff, pending identity set, index, and catalog agree on 770/78/0", "passed": True}, {"check": "Exactly the nine Agency/Control9 identities remain pending", "passed": True}, {"check": "All 96 historical source members match their archived exact hashes", "passed": True}, {"check": "All 96 source bindings refreshed from the exact current Git commit", "passed": True}, {"check": "All nine current native cards and pending index entries match historical conference records", "passed": True}, {"check": "Return188 accepted context, holds, current candidate, casebook and receipts included", "passed": True}, {"check": "All 34 source questions and 18 targeted cases preserved", "passed": True}, {"check": "Packet ZIP CRC and all unique safe members match SHA/CRC manifest", "passed": True}], "canonicalChangesBeforePreparation": False, "request": request}
    preparation_path.write_bytes(json_bytes(preparation))
    prep_binding = bind(preparation_path.relative_to(ROOT).as_posix(), preparation_path.read_bytes())
    packet_record_path = AUDIT / "RANK9_AGENCYCONTROL9_PACKET_189.json"
    packet_record = {"id": "RANK9-AGENCYCONTROL9-PACKET-189", "status": "PREPARED_UNSENT", "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding, "preparation": prep_binding, "conversation": CHAT, "checksPassed": 9, "checksFailed": 0}
    packet_record_path.write_bytes(json_bytes(packet_record))
    packet_record_binding = bind(packet_record_path.relative_to(ROOT).as_posix(), packet_record_path.read_bytes())

    pending_after = copy.deepcopy(pending)
    pending_after.update({"id": "CURRENT78-PENDING-IDENTITY-AUDIT-189", "recordedAtUtc": now, "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding}})
    pending_after_path = AUDIT / "CURRENT78_PENDING_IDENTITY_AUDIT_189.json"
    pending_after_path.write_bytes(json_bytes(pending_after))
    pending_binding = bind(pending_after_path.relative_to(ROOT).as_posix(), pending_after_path.read_bytes())
    next_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": False, "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding, "preparation": prep_binding, "candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "archive": bind(SOURCE_ARCHIVE, archive_raw)}
    queue_after = copy.deepcopy(queue)
    target_after = next(r for r in queue_after["currentPendingGroups"] if r["group"] == GROUP)
    target_after.update({"candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "archive": bind(SOURCE_ARCHIVE, archive_raw), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "preparedPacket": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding, "preparation": prep_binding, "freshPacketRequiredForCurrentAuthority": False})
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-189", "recordedAtUtc": now, "next": next_request, "nextPreparedRequest": next_request, "nextGroup": GROUP, "pendingIdentityAudit": pending_binding, "packetStatus": "RANK9_AGENCY_CONTROL9_CURRENT_SOURCE_PACKET_189_PREPARED_UNSENT_770_78", "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding})
    queue_path_after = AUDIT / "CURRENT_SPELL_QUEUE_189.json"
    queue_path_after.write_bytes(json_bytes(queue_after))
    queue_binding = bind(queue_path_after.relative_to(ROOT).as_posix(), queue_path_after.read_bytes())
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-189", "recordedAtUtc": now, "status": "RANK9_AGENCY_CONTROL9_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_770_78", "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": len(IDS), "pendingIdentityAudit": pending_binding, "nextPreparedRequest": next_request, "currentQueueBinding": queue_binding, "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding, "resumePriority": "Send the fresh 96-source Agency/Control9 packet to the same GPT director; independently audit exact per-identity returns, apply only accepted IDs, push each batch, and continue in queue order until pending reaches zero."})
    handoff_path_after = AUDIT / "CURRENT_HANDOFF_189.json"
    handoff_path_after.write_bytes(json_bytes(handoff_after))
    snapshot = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_189.md"
    snapshot.write_text(f"# Current ordinary spell-review checkpoint 189\n\nAuthority is **770 reviewed / 78 pending / 0 accepted-unapplied**, with 494 complete reviewed standalone procedures. The next nine-identity group is Rank9 Agency/Control9. Its fresh packet refreshes all 96 historical source bindings from the pushed 770/78 commit and includes Return188's accepted context and retained blockers.\n\nSee [handoff](CURRENT_HANDOFF_189.json), [queue](CURRENT_SPELL_QUEUE_189.json), [pending audit](CURRENT78_PENDING_IDENTITY_AUDIT_189.json), [packet record](RANK9_AGENCYCONTROL9_PACKET_189.json), and [source packet](rank9_agencycontrol9_return189_prepared/DD_Rank9_AgencyControl9_CurrentSource_189.zip).\n", encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig")
    start.write_text(f"**Current ordinary spell-review handoff [189](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_189.json):** authority is 770 reviewed / 78 pending / 0 accepted-unapplied. A fresh 96-source packet for Rank9 Agency/Control9 is prepared for the GPT director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_PACKET_189.json).\n\n" + old_start, encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY, "group": GROUP, "sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed, "packet": packet_binding, "deliveryManifest": delivery_binding, "queue": queue_binding, "checksPassed": 9}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
