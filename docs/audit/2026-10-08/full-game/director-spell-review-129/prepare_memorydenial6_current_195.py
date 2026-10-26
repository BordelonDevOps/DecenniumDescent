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
GROUP = "rank9-memory-denial6"
IDS = ["mass-willbreaker", "mind-collapse", "mind-prison-mass", "mind-wipe", "unmake-spell", "unravel-identity"]
AUTHORITY = {"reviewedApplied": 782, "pending": 66, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 506, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_194.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT66_PENDING_IDENTITY_AUDIT_194.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_194.json"
SOURCE_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_memory_denial_6_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Memory_Denial_6_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_NEXT_CONFERENCE_NOTES_129.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_memorydenial6_current_source_195_prepared"
PACKET_PATH = AUDIT / "RANK9MEMORYDENIAL6_PACKET_195.json"
PREP_PATH = AUDIT / "RANK9MEMORYDENIAL6_SOURCE_PREPARATION_195.json"
PENDING_PATH = AUDIT / "CURRENT66_PENDING_IDENTITY_AUDIT_195.json"
QUEUE_PATH = AUDIT / "CURRENT_SPELL_QUEUE_195.json"
HANDOFF_PATH = AUDIT / "CURRENT_HANDOFF_195.json"
SNAPSHOT_PATH = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_195.md"


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
    return bool(name) and "\\" not in name and not path.is_absolute() and all(
        part not in ("", ".", "..") and not part.startswith(".") for part in path.parts
    )


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "codex/ordinary-spell-review-complete"
    remote = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=ROOT, text=True).split()[0]
    assert remote == commit, (remote, commit)
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    allowed_dirty = {
        "docs/audit/2026-10-08/full-game/director-spell-review-129/prepare_memorydenial6_current_195.py",
    }
    assert all(line[3:] in allowed_dirty or line[3:].startswith(
        "docs/audit/2026-10-08/full-game/director-spell-review-129/__pycache__/") for line in dirty), dirty
    assert not OUT.exists() and not PACKET_PATH.exists() and not PREP_PATH.exists()
    assert not PENDING_PATH.exists() and not QUEUE_PATH.exists() and not HANDOFF_PATH.exists() and not SNAPSHOT_PATH.exists()

    queue, pending, handoff, index, catalog = [read(blob(commit, p)) for p in (QUEUE, PENDING, HANDOFF, INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 782, "pending": 66}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 506
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 66
    assert queue["pendingCount"] == 66
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    assert target["freshPacketRequiredForCurrentAuthority"] is True
    candidate_raw, archive_raw, notes_raw = [blob(commit, p) for p in (SOURCE_CANDIDATE, SOURCE_ARCHIVE, NOTES)]
    old_candidate, notes = read(candidate_raw), read(notes_raw)
    assert sha(candidate_raw) == target["candidate"]["sha256"] and len(candidate_raw) == target["candidate"]["bytes"]
    assert sha(archive_raw) == target["archive"]["sha256"] and len(archive_raw) == target["archive"]["bytes"]
    assert [row["spellId"] for row in old_candidate["records"]] == IDS
    assert len(old_candidate["sourceBindings"]) == 120
    assert notes["identities"] == IDS and len(notes["completeOriginalQuestionsUnchanged"]) == 28
    assert len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["allQuestions"]) == 30
    assert len(notes["requiredNewCases"]) == 12 and len(notes["originalFutureCaseRequirementsUnchanged"]) == 10

    entries = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    pending_ids = set(pending["pendingIds"])
    assert set(IDS) <= pending_ids
    for sid in IDS:
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert catalog_rows[sid]["id"] == sid
        ptr = int(entries[sid]["wholeCardPointer"].rsplit("/", 1)[1])
        assert catalog["spells"][ptr]["id"] == sid

    historical_members: dict[str, bytes] = {}
    with zipfile.ZipFile(FULL / Path(SOURCE_ARCHIVE).name) as archive:
        names = archive.namelist()
        assert archive.testzip() is None and len(names) == len(set(names)) and all(safe_member(name) for name in names)
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
    current["countsUnchanged"] = {"reviewed": 782, "pending": 66}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_782_REVIEWED_66_PENDING_AUTHORITY"
    current["id"] = "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-CONTEXT-195"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        sid = record["spellId"]
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
    current_raw = json_bytes(current)

    candidate_root = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_194"
    current_paths = [
        INDEX, CATALOG, QUEUE, PENDING, HANDOFF, "START_HERE.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_194.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_APPLICATION_194.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_APPLICATION_VALIDATION_194.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_DIRECTOR_DECISION_194.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN194_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN194_RECEIPT.json",
        *[f"{candidate_root}/{name}" for name in [
            "MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json", "INDEPENDENT_RETURN_AUDIT.json",
            "procedures/ritual-mastery.json", "procedures/world-rewrite.json", "procedures/resonance-perfection.json",
        ]],
    ]
    current_files = {"current/" + path: blob(commit, path) for path in current_paths}
    current_context = {
        "id": "RANK9-MEMORY-DENIAL6-CURRENT-DIRECTOR-CONTEXT-195", "recordedAtUtc": now,
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"], "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": target["candidate"],
        "historicalCandidateBinding": bind(SOURCE_CANDIDATE, candidate_raw),
        "historicalSourceArchiveBinding": bind(SOURCE_ARCHIVE, archive_raw),
        "sourceRefresh": {"sourceFileCount": len(refreshed), "changedSinceCandidate": changed},
        "latestAcceptedOrdinarySpellBatch": {
            "application": "RANK9-CASTINGCOST5-APPLICATION-194",
            "acceptedIds": ["ritual-mastery", "world-rewrite", "resonance-perfection"],
            "unacceptedIds": ["perfect-spell", "unholy-ascendance"],
            "retainedBlockers": {"perfect-spell": ["CC194-B01"], "unholy-ascendance": ["CC194-B04"]},
            "countsAfter": AUTHORITY, "runtimeSelectionEnabled": False,
            "worldRewriteProcedure": f"current/{candidate_root}/procedures/world-rewrite.json",
        },
        "retainedBlockersOutsideScope": {
            "AG190": {"ids": ["absolute-domination", "puppetmaster-s-realm"], "blockers": ["AG190-B01", "AG190-B02"]},
            "TF192": {"ids": ["time-stop", "eternal-prophecy", "fate-rewrite", "collapse-timeline"],
                      "blockers": ["TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"]},
            "CC194": {"ids": ["perfect-spell", "unholy-ascendance"], "blockers": ["CC194-B01", "CC194-B04"]},
        },
        "qualification": "Preparation only. Revalidate every source and accepted context against the refreshed current bindings. The historical source candidate is provenance, not authority. Do not alter canonical spell cards, execute supplied programs, or claim runtime, implementation, human-play, balance, cosmology, completion, or release approval.",
    }
    request = (
        "GPT director — review exactly the six current pending Rank9 Memory/Denial6 identities in this packet.\n\n"
        f"Source branch/commit: {branch} / {commit}. Current authority: 782 reviewed-applied / 66 pending / 0 accepted-unapplied; 506 complete standalone procedures; 173 scoped interfaces.\n\n"
        "Scope only: mass-willbreaker, mind-collapse, mind-prison-mass, mind-wipe, unmake-spell, unravel-identity. Use the attached current handoff, queue, pending audit, index, catalog, refreshed 120-source bindings, and exact current applied context as authority. The historical candidate and conference archive are provenance. Current Casting Cost5 has three accepted static procedures (including World Rewrite), two retained blockers, and no runtime selection. Preserve the carried AG190 and TF192 blockers.\n\n"
        "Independently reconcile all 28 original questions and both focused addenda, the 12 required new cases, all ten future-case requirements, and every source conflict. Preserve each native card, actual class/school/rank route, source text, full history, and genuine reversibility. Return one complete source-faithful static procedure per identity with concrete branch cases, explicit lifecycle, all original and newly required evidence, and forward/inverse state operations. Do not promote a proposal or historical extraction into authority by repetition.\n\n"
        "For Mass Willbreaker, resolve exact all-enemy membership within 120 feet, abilities-and-spells denial, WIS ending cadence, original lifetime, and real Ready, concentration, passive, companion, and resource behavior. For rank9 Mind Collapse, keep it distinct from rank8 Mental Collapse and reconcile its actual three-round Stunned/INT-save text, clock, initial save, concentration end, and suppressed early escape. For Mind Prison (Mass), demonstrate five separate meaningful private realities, exact immunity/True Seeing/dispel boundaries, independent resistance or release, and finite lifecycle without importing lower-rank damage or a phantom plane. For Mind Wipe, resolve permanent memory/personality erasure against the native duration, preserving the subject's autonomous identity, original record, later experiences, and private audit boundary. For Unmake Spell, identify the actual enemy spell and all acquired routes; distinguish future casts, paid Ready release, and ongoing effects; give genuine loss/relearning/recovery rules and explicitly apply or distinguish accepted World Rewrite's temporary granted repertoire. For Unravel Identity, account for every actual Base/Arch/Hero class capability, multiclass/passive/form/companion dependency, maxima and resources while preserving the one-round false-self belief and exact recovery without free refill or revived ended effects.\n\n"
        "Accept only individually passing identities with accepted=true/applied=false. Give exact blocker and qualification IDs for every unaccepted identity; retain all future obligations and original question/case requirements. Report procedures, questions, cases, branches, events, forward/inverse operations, holds, source bindings, and validation counts. Include a safe member manifest with exact hashes and a separate delivery JSON bound to the returned ZIP. Do not edit canonical files or execute supplied programs. After independent audit, only exact accepted IDs will be applied and pushed before the next queue group."
    )

    files: dict[str, bytes] = {
        "CURRENT_CONTEXT_195.json": json_bytes(current_context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json": current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9MEMORYDENIAL6_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_195.txt": request.encode("utf-8"),
        **current_files,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)
    OUT.mkdir(parents=True, exist_ok=False)
    current_candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json"
    current_candidate_path.write_bytes(current_raw)
    packet_path = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_195.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        rows = []
        for name in sorted(files):
            raw = files[name]
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw),
                         "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
        manifest = {"id": "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-PACKET-MANIFEST-195",
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

    packet_binding = bind(packet_path.relative_to(ROOT).as_posix(), packet_path.read_bytes())
    candidate_binding = bind(current_candidate_path.relative_to(ROOT).as_posix(), current_raw)
    delivery = {"id": "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-DELIVERY-195", "status": "PREPARED_UNSENT",
                "archive": packet_binding, "members": len(rows) + 1, "manifestBindings": len(rows),
                "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
                "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
                "historicalSourceArchive": bind(SOURCE_ARCHIVE, archive_raw),
                "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceHistoricalCandidate": changed,
                "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_195_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)

    checks = [
        "Packet binds the pushed current branch head and exact 782/66/0 authority.",
        "Exactly six current pending Memory/Denial6 identities are next in queue order.",
        "All 120 historical source members match the archived hashes and CRCs.",
        "All 120 source bindings are refreshed from the exact current Git commit.",
        "All six native entries and catalog pointers remain exact and pending.",
        "Return194's accepted World Rewrite procedure and two blockers are current context.",
        "AG190 and TF192 blockers remain explicitly carried outside this group.",
        "All 28 original questions, two addenda, 12 required cases, and ten future obligations are preserved.",
        "Historical archive paths and current packet member SHA/CRC validate.",
        "Returned packet has a separate exact delivery manifest and no canonical changes.",
    ]
    prep = {"id": "RANK9-MEMORY-DENIAL6-SOURCE-PREPARATION-195", "recordedAtUtc": now,
            "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "sourceCommit": commit, "sourceBranch": branch,
            "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
            "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
            "historicalArchive": bind(SOURCE_ARCHIVE, archive_raw), "currentDerivedCandidate": candidate_binding,
            "sourceFileCount": len(refreshed), "changedSinceHistoricalCandidate": changed,
            "packet": packet_binding, "deliveryManifest": delivery_binding, "memberCount": len(rows) + 1,
            "checksPassed": len(checks), "checksFailed": 0,
            "checks": [{"check": label, "passed": True} for label in checks],
            "canonicalChangesBeforePreparation": False, "request": request}
    PREP_PATH.write_bytes(json_bytes(prep))
    prep_binding = bind(PREP_PATH.relative_to(ROOT).as_posix(), PREP_PATH.read_bytes())
    packet_record = {"id": "RANK9MEMORYDENIAL6-PACKET-195", "status": "PREPARED_UNSENT",
                     "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
                     "packet": packet_binding, "deliveryManifest": delivery_binding,
                     "preparation": prep_binding, "conversation": CHAT,
                     "checksPassed": len(checks), "checksFailed": 0}
    PACKET_PATH.write_bytes(json_bytes(packet_record))
    packet_record_binding = bind(PACKET_PATH.relative_to(ROOT).as_posix(), PACKET_PATH.read_bytes())

    pending_after = copy.deepcopy(pending)
    pending_after.update({"id": "CURRENT66-PENDING-IDENTITY-AUDIT-195", "recordedAtUtc": now,
                          "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding}})
    PENDING_PATH.write_bytes(json_bytes(pending_after))
    pending_binding = bind(PENDING_PATH.relative_to(ROOT).as_posix(), PENDING_PATH.read_bytes())
    next_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS),
                    "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": False,
                    "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding,
                    "preparation": prep_binding, "candidate": candidate_binding,
                    "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
                    "archive": bind(SOURCE_ARCHIVE, archive_raw)}
    queue_after = copy.deepcopy(queue)
    target_after = next(row for row in queue_after["currentPendingGroups"] if row["group"] == GROUP)
    target_after.update({"candidate": candidate_binding, "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
                         "archive": bind(SOURCE_ARCHIVE, archive_raw), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                         "preparedPacket": packet_binding, "deliveryManifest": delivery_binding,
                         "packetRecord": packet_record_binding, "preparation": prep_binding,
                         "freshPacketRequiredForCurrentAuthority": False})
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-195", "recordedAtUtc": now, "next": next_request,
                        "nextPreparedRequest": next_request, "nextGroup": GROUP,
                        "pendingIdentityAudit": pending_binding,
                        "packetStatus": "RANK9_MEMORY_DENIAL6_CURRENT_SOURCE_PACKET_195_PREPARED_UNSENT_782_66",
                        "currentPreparation": prep_binding, "currentPacket": packet_binding,
                        "currentPacketDelivery": delivery_binding})
    QUEUE_PATH.write_bytes(json_bytes(queue_after))
    queue_binding = bind(QUEUE_PATH.relative_to(ROOT).as_posix(), QUEUE_PATH.read_bytes())
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-195", "recordedAtUtc": now,
                          "status": "RANK9_MEMORY_DENIAL6_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_782_66",
                          "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": len(IDS),
                          "pendingIdentityAudit": pending_binding, "nextPreparedRequest": next_request,
                          "currentQueueBinding": queue_binding, "currentPreparation": prep_binding,
                          "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
                          "resumePriority": "Send the fresh 120-source Memory/Denial6 packet to the same GPT director; independently audit exact per-identity decisions, apply only accepted IDs, push, and continue until pending reaches zero."})
    HANDOFF_PATH.write_bytes(json_bytes(handoff_after))
    SNAPSHOT_PATH.write_text(
        f"# Current ordinary spell-review checkpoint 195\n\nAuthority is **782 reviewed / 66 pending / 0 accepted-unapplied**, with 506 complete standalone procedures. The next six-identity group is Rank9 Memory/Denial6. Its fresh packet refreshes all {len(refreshed)} historical source bindings from pushed commit {commit} and includes current Casting Cost5 acceptances, blockers, and the exact World Rewrite procedure.\n\nSee [handoff](CURRENT_HANDOFF_195.json), [queue](CURRENT_SPELL_QUEUE_195.json), [pending audit](CURRENT66_PENDING_IDENTITY_AUDIT_195.json), [packet record](RANK9MEMORYDENIAL6_PACKET_195.json), and [source packet](rank9_memorydenial6_current_source_195_prepared/DD_Rank9_MemoryDenial6_CurrentSource_195.zip).\n",
        encoding="utf-8", newline="\n")
    start_path = ROOT / "START_HERE.md"
    old_start = blob(commit, "START_HERE.md").decode("utf-8-sig")
    start_path.write_text(
        f"**Current ordinary spell-review handoff [195](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_195.json):** authority is 782 reviewed / 66 pending / 0 accepted-unapplied. A fresh 120-source packet for Rank9 Memory/Denial6 is prepared for the GPT director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET_195.json).\n\n" + old_start,
        encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY,
                      "group": GROUP, "sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed,
                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                      "queue": queue_binding, "checksPassed": len(checks)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
