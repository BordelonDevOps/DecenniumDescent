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
GROUP = "rank9-casting-cost5"
IDS = ["perfect-spell", "ritual-mastery", "world-rewrite", "resonance-perfection", "unholy-ascendance"]
AUTHORITY = {"reviewedApplied": 779, "pending": 69, "acceptedUnapplied": 0, "completeStandaloneProcedures": 503, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_192.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT69_PENDING_IDENTITY_AUDIT_192.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_192.json"
SOURCE_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_casting_cost_5_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Casting_Cost_5_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9CASTINGCOST5_NEXT_CONFERENCE_NOTES_129.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_castingcost5_current_source_193_prepared"
PREPARATION_PATH = AUDIT / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_193.json"
PACKET_RECORD_PATH = AUDIT / "RANK9_CASTINGCOST5_PACKET_193.json"


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
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "codex/ordinary-spell-review-complete"
    remote_head = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=ROOT, text=True).split()[0]
    assert remote_head == commit, (remote_head, commit)
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    allowed = {"docs/audit/2026-10-08/full-game/director-spell-review-129/prepare_castingcost5_current_193.py"}
    assert all(line[3:] in allowed or line[3:].startswith("docs/audit/2026-10-08/full-game/director-spell-review-129/__pycache__/") for line in dirty), dirty
    assert not OUT.exists() and not PREPARATION_PATH.exists() and not PACKET_RECORD_PATH.exists()

    queue, pending, handoff, index, catalog = [read(blob(commit, path)) for path in (QUEUE, PENDING, HANDOFF, INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 779, "pending": 69}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 503
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 69
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    assert target["freshPacketRequiredForCurrentAuthority"] is True
    candidate_raw, archive_raw = blob(commit, SOURCE_CANDIDATE), blob(commit, SOURCE_ARCHIVE)
    old_candidate = read(candidate_raw)
    assert [row["spellId"] for row in old_candidate["records"]] == IDS
    assert len(old_candidate["sourceBindings"]) == 117
    assert target["candidate"] == bind(SOURCE_CANDIDATE, candidate_raw)
    assert target["archive"]["path"] == SOURCE_ARCHIVE and target["archive"]["bytes"] == len(archive_raw) and target["archive"]["sha256"] == sha(archive_raw)
    entries = {row["id"]: row for row in index["entries"]}
    pending_ids = set(pending["pendingIds"])
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    assert set(IDS) <= pending_ids
    for record in old_candidate["records"]:
        sid = record["spellId"]
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert catalog_rows[sid]["id"] == sid
        assert int(entries[sid]["wholeCardPointer"].rsplit("/", 1)[1]) < len(catalog["spells"])
        assert catalog["spells"][int(entries[sid]["wholeCardPointer"].rsplit("/", 1)[1])]["id"] == sid

    historical_members = {}
    with zipfile.ZipFile(FULL / Path(SOURCE_ARCHIVE).name) as source_archive:
        names = source_archive.namelist()
        assert source_archive.testzip() is None and len(names) == len(set(names)) and all(safe_member(name) for name in names)
        for source in old_candidate["sourceBindings"]:
            raw = source_archive.read("sources/" + source["path"])
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
            changed.append({"path": path, "historicalBytes": len(historical_members[path]),
                            "historicalSha256": sha(historical_members[path]), "currentBytes": len(raw),
                            "currentSha256": sha(raw)})

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
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed,
                                       "sourceContentsFromGitCommit": commit, "allSourceBindingsRefreshed": True}
    current["countsUnchanged"] = {"reviewed": 779, "pending": 69}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_779_REVIEWED_69_PENDING_AUTHORITY"
    current["id"] = "RANK9-CASTING-COST5-CURRENT-SOURCE-CONTEXT-193"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        sid = record["spellId"]
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
    current_raw = json_bytes(current)

    notes_raw = blob(commit, NOTES)
    notes = read(notes_raw)
    assert notes["identities"] == IDS and len(notes["allQuestions"]) == 34
    assert len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["requiredNewCases"]) == 10

    candidate_root = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192"
    current_paths = [
        INDEX, CATALOG, QUEUE, PENDING, HANDOFF, "START_HERE.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_EXACT_ACCEPTANCE_192.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_APPLICATION_192.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_APPLICATION_VALIDATION_192.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_DIRECTOR_DECISION_192.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_RETURN192_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_RETURN192_RECEIPT.json",
        *[f"{candidate_root}/{name}" for name in [
            "MODEL.json", "CASEBOOK.json.gz", "HOLD_REGISTER.json", "PROCEDURES.json",
            "CANDIDATE_PACKAGE_MANIFEST.json", "INDEPENDENT_RETURN_AUDIT.json",
        ]],
        *[f"{candidate_root}/procedures/{sid}.json" for sid in ["time-fracture", "foresight-perfect"]],
    ]
    current_files = {"current/" + path: blob(commit, path) for path in current_paths}
    blocker_carry = {
        "AG190": {"ids": ["absolute-domination", "puppetmaster-s-realm"], "blockers": ["AG190-B01", "AG190-B02"]},
        "TF192": {"ids": ["time-stop", "eternal-prophecy", "fate-rewrite", "collapse-timeline"],
                  "blockers": ["TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"]},
    }
    context = {
        "id": "RANK9-CASTING-COST5-CURRENT-DIRECTOR-CONTEXT-193", "recordedAtUtc": now,
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"], "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": target["candidate"], "historicalCandidateBinding": bind(SOURCE_CANDIDATE, candidate_raw),
        "historicalSourceArchiveBinding": bind(SOURCE_ARCHIVE, archive_raw),
        "sourceRefresh": {"sourceFileCount": len(refreshed), "changedSinceCandidate": changed},
        "previousAppliedBatch": {"reviewId": "RANK9-TIMEFATE6-APPLICATION-192",
                                 "acceptedSpellIds": ["time-fracture", "foresight-perfect"],
                                 "countsAfter": AUTHORITY, "acceptedUnapplied": 0},
        "retainedBlockersOutsideScope": blocker_carry,
        "qualification": "Preparation only. Revalidate every casting/cost/sacrifice source against refreshed current bindings and exact accepted context. The historical candidate is not authority. Do not alter canonical spell cards, execute supplied programs, or claim runtime, implementation, human-play, balance, cosmology, completion, or release approval.",
    }
    request = (
        "GPT director — review exactly the five current pending Rank9 Casting Cost5 identities in this packet.\n\n"
        f"Source branch/commit: {branch} / {commit}. Current authority: 779 reviewed-applied / 69 pending / 0 accepted-unapplied; 503 complete standalone procedures; 173 scoped interfaces.\n\n"
        "Scope only: perfect-spell, ritual-mastery, world-rewrite, resonance-perfection, unholy-ascendance. Use the attached current handoff, queue, pending audit, index, catalog and refreshed source files as authority. The historical candidate and conference archive are provenance, not selected rules. The exact Time/Fate6 batch now has two accepted static procedures (Time Fracture and Foresight Perfect) and four retained blockers; Return190's two blockers also remain carried forward.\n\n"
        "Independently check the 34 original questions, two focused addenda, and 10 required new case specifications against the actual bound sources. Preserve each native card, class route, source text and current accepted context. Resolve source conflicts explicitly; historical proposals and extracted corpus material do not become law by repetition.\n\n"
        "Address every identity separately. For Perfect Spell, distinguish actually waiving costs/timing/components from retained prerequisites and resolve real wrapper composition/cycles. For Ritual Mastery, show a source-qualified ritual through the complete outer casting and inner completion timing, with genuine prerequisites, participants, cost, interruption and only a true ritual. For World Rewrite, prove the actual acquisition record, legal spell and rank route, and spell-to-spell conflict behavior without turning observed knowledge into known spells. For Resonance Perfection, audit quote, final modifier order, available RP, payment, strain, cadence, valid repeated use and stale/recovery behavior, including zero RP and funded output. For Unholy Ascendance, bind its body/form, duration, costs, qualifying spell and actual physical/damage cases without borrowing unprinted Lich powers.\n\n"
        "Return a source-faithful static procedure and complete reversible cases for each identity. Accept only individually passing IDs with accepted=true/applied=false, and retain exact blocker/qualification IDs for every unaccepted identity. Preserve all future obligations and original question/case requirements. Report procedure, question, case, branch, event, forward/inverse-operation, hold and validation counts. Include a safe member manifest with exact hashes and a separate delivery JSON bound to the returned ZIP. Do not edit canonical files or execute supplied programs. After independent audit, only exact accepted IDs will be applied before continuing in queue order."
    )

    files: dict[str, bytes] = {
        "CURRENT_CONTEXT_193.json": json_bytes(context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_193.json": current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9CASTINGCOST5_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_193.txt": request.encode("utf-8"),
        **current_files,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)
    OUT.mkdir(parents=True, exist_ok=False)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_193.json"
    candidate_path.write_bytes(current_raw)
    packet_path = OUT / "DD_Rank9_CastingCost5_CurrentSource_193.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        rows = []
        for name in sorted(files):
            raw = files[name]
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw),
                         "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
        manifest = {"id": "RANK9-CASTING-COST5-CURRENT-SOURCE-PACKET-MANIFEST-193",
                    "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                    "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows}
        packet.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet_path) as packet:
        names = packet.namelist()
        assert packet.testzip() is None and len(names) == len(rows) + 1 and len(set(names)) == len(rows) + 1
        for row in rows:
            raw = packet.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]

    packet_rel = packet_path.relative_to(ROOT).as_posix()
    candidate_rel = candidate_path.relative_to(ROOT).as_posix()
    packet_binding = bind(packet_rel, packet_path.read_bytes())
    candidate_binding = bind(candidate_rel, current_raw)
    delivery = {"id": "RANK9-CASTING-COST5-CURRENT-SOURCE-DELIVERY-193", "status": "PREPARED_UNSENT",
                "archive": packet_binding, "members": len(rows) + 1, "manifestBindings": len(rows),
                "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
                "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
                "historicalSourceArchive": bind(SOURCE_ARCHIVE, archive_raw),
                "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceHistoricalCandidate": changed,
                "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_CastingCost5_CurrentSource_193_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_rel = delivery_path.relative_to(ROOT).as_posix()
    delivery_binding = bind(delivery_rel, delivery_raw)

    checks = [
        "Packet source is the pushed current branch head and authority is exactly 779/69/0.",
        "Exactly five current pending Casting Cost5 identities are next in queue order.",
        "All 117 historical source members match the archived hashes.",
        "All 117 source bindings are refreshed from the exact current Git commit.",
        "All five current native entries and source catalog pointers are checked.",
        "Current Time/Fate6 accepted procedures and unresolved blockers are included.",
        "Return190 and Return192 blockers remain explicitly carried outside this group.",
        "All 34 original questions, two focused addenda and 10 required cases are preserved.",
        "Historical archive CRC, member paths and exact source bindings validate.",
        "Packet ZIP CRC and every member SHA/CRC match its safe manifest.",
    ]
    prep = {"id": "RANK9-CASTING-COST5-SOURCE-PREPARATION-193", "recordedAtUtc": now,
            "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "sourceCommit": commit, "sourceBranch": branch,
            "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
            "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
            "historicalArchive": bind(SOURCE_ARCHIVE, archive_raw), "currentDerivedCandidate": candidate_binding,
            "sourceFileCount": len(refreshed), "changedSinceHistoricalCandidate": changed,
            "packet": packet_binding, "deliveryManifest": delivery_binding, "memberCount": len(rows) + 1,
            "checksPassed": len(checks), "checksFailed": 0,
            "checks": [{"check": label, "passed": True} for label in checks],
            "canonicalChangesBeforePreparation": False, "request": request}
    PREPARATION_PATH.write_bytes(json_bytes(prep))
    prep_binding = bind(PREPARATION_PATH.relative_to(ROOT).as_posix(), PREPARATION_PATH.read_bytes())
    packet_record = {"id": "RANK9-CASTING-COST5-PACKET-193", "status": "PREPARED_UNSENT",
                     "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
                     "packet": packet_binding, "deliveryManifest": delivery_binding,
                     "preparation": prep_binding, "conversation": CHAT,
                     "checksPassed": len(checks), "checksFailed": 0}
    PACKET_RECORD_PATH.write_bytes(json_bytes(packet_record))
    packet_record_binding = bind(PACKET_RECORD_PATH.relative_to(ROOT).as_posix(), PACKET_RECORD_PATH.read_bytes())

    pending_after = copy.deepcopy(pending)
    pending_after.update({"id": "CURRENT69-PENDING-IDENTITY-AUDIT-193", "recordedAtUtc": now,
                          "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding}})
    pending_path = AUDIT / "CURRENT69_PENDING_IDENTITY_AUDIT_193.json"
    pending_path.write_bytes(json_bytes(pending_after))
    pending_binding = bind(pending_path.relative_to(ROOT).as_posix(), pending_path.read_bytes())
    next_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS),
                    "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": False,
                    "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding,
                    "preparation": prep_binding, "candidate": candidate_binding,
                    "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw), "archive": bind(SOURCE_ARCHIVE, archive_raw)}
    queue_after = copy.deepcopy(queue)
    target_after = next(row for row in queue_after["currentPendingGroups"] if row["group"] == GROUP)
    target_after.update({"candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
                         "archive": bind(SOURCE_ARCHIVE, archive_raw), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                         "preparedPacket": packet_binding, "deliveryManifest": delivery_binding,
                         "packetRecord": packet_record_binding, "preparation": prep_binding,
                         "freshPacketRequiredForCurrentAuthority": False})
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-193", "recordedAtUtc": now, "next": next_request,
                        "nextPreparedRequest": next_request, "nextGroup": GROUP,
                        "pendingIdentityAudit": pending_binding,
                        "packetStatus": "RANK9_CASTING_COST5_CURRENT_SOURCE_PACKET_193_PREPARED_UNSENT_779_69",
                        "currentPreparation": prep_binding, "currentPacket": packet_binding,
                        "currentPacketDelivery": delivery_binding})
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_193.json"
    queue_path.write_bytes(json_bytes(queue_after))
    queue_binding = bind(queue_path.relative_to(ROOT).as_posix(), queue_path.read_bytes())
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-193", "recordedAtUtc": now,
                          "status": "RANK9_CASTING_COST5_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_779_69",
                          "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": len(IDS),
                          "pendingIdentityAudit": pending_binding, "nextPreparedRequest": next_request,
                          "currentQueueBinding": queue_binding, "currentPreparation": prep_binding,
                          "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
                          "resumePriority": "Send the fresh 117-source Casting Cost5 packet to the same GPT director; independently audit each exact per-identity return, apply only accepted IDs, push, and continue in queue order until pending reaches zero."})
    handoff_path = AUDIT / "CURRENT_HANDOFF_193.json"
    handoff_path.write_bytes(json_bytes(handoff_after))
    snapshot = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_193.md"
    snapshot.write_text(
        f"# Current ordinary spell-review checkpoint 193\n\nAuthority is **779 reviewed / 69 pending / 0 accepted-unapplied**, with 503 complete standalone procedures. The next five-identity group is Rank9 Casting Cost5. Its fresh packet refreshes all {len(refreshed)} historical source bindings from the pushed 779/69 commit and includes the exact Time/Fate6 accepted procedures and retained blockers.\n\nSee [handoff](CURRENT_HANDOFF_193.json), [queue](CURRENT_SPELL_QUEUE_193.json), [pending audit](CURRENT69_PENDING_IDENTITY_AUDIT_193.json), [packet record](RANK9CASTINGCOST5_PACKET_193.json), and [source packet](rank9_castingcost5_current_source_193_prepared/DD_Rank9_CastingCost5_CurrentSource_193.zip).\n",
        encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig")
    start.write_text(f"**Current ordinary spell-review handoff [193](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_193.json):** authority is 779 reviewed / 69 pending / 0 accepted-unapplied. A fresh {len(refreshed)}-source packet for Rank9 Casting Cost5 is prepared for the GPT director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9CASTINGCOST5_PACKET_193.json).\n\n" + old_start,
                     encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY,
                      "group": GROUP, "sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed,
                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                      "queue": queue_binding, "checksPassed": len(checks)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
