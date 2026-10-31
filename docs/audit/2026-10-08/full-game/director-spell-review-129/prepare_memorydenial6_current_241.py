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
IDS = ["mind-collapse", "unravel-identity"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_240.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_240.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_240.json"
SOURCE_CANDIDATE = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_224_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json"
SOURCE_CANDIDATE_195 = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_195_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json"
HISTORICAL_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_memory_denial_6_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Memory_Denial_6_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_NEXT_CONFERENCE_NOTES_129.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_memorydenial6_current_source_241_prepared"
PACKET_PATH = AUDIT / "RANK9MEMORYDENIAL6_PACKET_241.json"
PREP_PATH = AUDIT / "RANK9MEMORYDENIAL6_SOURCE_PREPARATION_241.json"
PENDING_PATH = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_241.json"
QUEUE_PATH = AUDIT / "CURRENT_SPELL_QUEUE_241.json"
HANDOFF_PATH = AUDIT / "CURRENT_HANDOFF_241.json"
SNAPSHOT_PATH = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_241.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def bind(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def blob(commit: str, path: str) -> bytes:
    local = ROOT / Path(path)
    if local.is_file():
        return local.read_bytes()
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def blob_id(commit: str, path: str) -> str:
    raw = blob(commit, path)
    return subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=raw).decode().strip()


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(
        part not in ("", ".", "..") and not part.startswith(".") for part in path.parts
    )


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch

    queue, pending, handoff, index, catalog = [read(blob(commit, p)) for p in (QUEUE, PENDING, HANDOFF, INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 37
    assert queue["pendingCount"] == 37
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    assert target["freshPacketRequiredForCurrentAuthority"] is True
    local_candidate_copy_raw = blob(commit, SOURCE_CANDIDATE)
    prior_packet_path = AUDIT / "rank9_memorydenial6_current_source_224_prepared/DD_Rank9_MemoryDenial6_CurrentSource_224.zip"
    with zipfile.ZipFile(prior_packet_path) as prior_packet:
        candidate_raw = prior_packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json")
    original_packet_path = AUDIT / "rank9_memorydenial6_current_source_195_prepared/DD_Rank9_MemoryDenial6_CurrentSource_195.zip"
    with zipfile.ZipFile(original_packet_path) as original_packet:
        candidate_195_raw = original_packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json")
    candidate_195 = read(candidate_195_raw)
    archive_raw, notes_raw = [blob(commit, p) for p in (SOURCE_ARCHIVE, NOTES)]
    old_candidate, notes = read(candidate_raw), read(notes_raw)
    assert read(local_candidate_copy_raw) == old_candidate
    assert sha(candidate_raw) == target["candidate"]["sha256"] and len(candidate_raw) == target["candidate"]["bytes"]
    assert sha(archive_raw) == target["archive"]["sha256"] and len(archive_raw) == target["archive"]["bytes"]
    assert {row["spellId"] for row in old_candidate["records"]} == set(IDS)
    assert len(old_candidate["sourceBindings"]) == len(old_candidate["historicalSourceBindings"]) == 120
    assert len(candidate_195["historicalSourceBindings"]) == 120
    assert set(IDS) <= set(notes["identities"]) and len(notes["completeOriginalQuestionsUnchanged"]) == 28
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
        for source in candidate_195["historicalSourceBindings"]:
            raw = archive.read("sources/" + source["path"])
            assert len(raw) == source["bytes"] and sha(raw) == source["sha256"]
            historical_members[source["path"]] = raw

    refreshed, current_sources, changed = [], {}, []
    with zipfile.ZipFile(prior_packet_path) as prior_packet:
        for old in old_candidate["sourceBindings"]:
            path = old["path"]
            assert safe_member(path) and not Path(path).is_absolute()
            raw = blob(commit, path)
            refreshed.append({"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": blob_id(commit, path)})
            current_sources["sources_current/" + path] = raw
            prior_raw = prior_packet.read("sources_current/" + path)
            if len(prior_raw) != old["bytes"] or sha(prior_raw) != old["sha256"]:
                raise AssertionError(f"Packet224 source member does not match candidate binding: {path}")
            if raw != prior_raw:
                changed.append({"path": path, "priorBytes": len(prior_raw),
                                "priorSha256": sha(prior_raw), "currentBytes": len(raw),
                                "currentSha256": sha(raw)})

    now = datetime.now(timezone.utc).isoformat()
    current = copy.deepcopy(old_candidate)
    current["records"] = [copy.deepcopy(row) for row in old_candidate["records"] if row["spellId"] in IDS]
    assert [row["spellId"] for row in current["records"]] == IDS
    current["historicalSourceBindings"] = copy.deepcopy(old_candidate["sourceBindings"])
    current["sourceBindings"] = refreshed
    current["currentSourceCommit"] = commit
    current["currentBranch"] = branch
    current["currentAuthority"] = AUTHORITY
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current["historicalCandidateBinding"] = bind(SOURCE_CANDIDATE, candidate_raw)
    current["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    current["historicalSourceArchiveBinding"] = bind(SOURCE_ARCHIVE, archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSincePriorCurrentPacket224": changed,
                                        "sourceContentsFromCurrentWorkspaceSnapshot": True, "headCommit": commit, "allSourceBindingsRefreshed": True}
    current["countsUnchanged"] = {"reviewed": 811, "pending": 37}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_811_REVIEWED_37_PENDING_AUTHORITY"
    current["id"] = "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-CONTEXT-241"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        sid = record["spellId"]
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
    current_raw = json_bytes(current)

    candidate_root = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_222_final"
    current_paths = [
        INDEX, CATALOG, QUEUE, PENDING, HANDOFF, "START_HERE.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_222.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_APPLICATION_222.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_APPLICATION_VALIDATION_222.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN222_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_INDEX_OPERATIONS_222.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_DIRECTOR_DECISION_222.json",
        *[f"docs/audit/2026-10-08/full-game/director-spell-review-129/{name}" for name in [
            "RANK9_CASTINGCOST5_PACKET_240_SUBMISSION.json",
            "RANK9_CASTINGCOST5_PACKET240_INDEPENDENT_AUDIT.json",
            "RANK9_CASTINGCOST5_PACKET240_RECEIPT.json",
            "RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json",
            "RANK9_CASTINGCOST5_RETURN240_RECEIPT.json",
            "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json",
            "RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
            "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json",
            "RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json",
            "RANK9_MEMORYDENIAL6_RETURN196_INDEPENDENT_AUDIT.json",
            "RANK9_MEMORYDENIAL6_RETURN196_RECEIPT.json",
            "RANK9_MEMORYDENIAL6_EXACT_ACCEPTANCE_196.json",
            "RANK9_MEMORYDENIAL6_DIRECTOR_DECISION_196.json",
            "RANK9_MEMORYDENIAL6_RETURN224_INDEPENDENT_AUDIT.json",
            "RANK9_MEMORYDENIAL6_RETURN224_RECEIPT.json",
        ]],
        *[f"docs/audit/2026-10-08/full-game/director-spell-review-129/{name}" for name in [
            "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip",
            "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD_DELIVERY.json",
            "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip",
            "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json",
            "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip",
            "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json",
            "rank9_memorydenial6_return224_received/DD_Rank9_MemoryDenial2_Director_Return224.zip",
            "rank9_memorydenial6_return224_received/DD_Rank9_MemoryDenial2_Director_Return224_DELIVERY.json",
            "rank9_memorydenial6_return196_witness_supplement_224/DD_Rank9_MemoryDenial6_Return196_TargetWitnesses_224.zip",
            "rank9_memorydenial6_return196_witness_supplement_224/DD_Rank9_MemoryDenial6_Return196_TargetWitnesses_224_DELIVERY.json",
        ]],
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET_195.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_SOURCE_PREPARATION_195.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET_224.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_SOURCE_PREPARATION_224.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_224_prepared/DD_Rank9_MemoryDenial6_CurrentSource_224_DELIVERY.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_224_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json",
        *[f"docs/audit/2026-10-08/full-game/director-spell-review-129/{name}" for name in [
            "RANK9_MEMORYDENIAL6_RETURN196_INDEPENDENT_AUDIT.json",
            "RANK9_MEMORYDENIAL6_RETURN196_RECEIPT.json",
            "RANK9_MEMORYDENIAL6_EXACT_ACCEPTANCE_196.json",
            "RANK9_MEMORYDENIAL6_DIRECTOR_DECISION_196.json",
        ]],
        *[f"{candidate_root}/{name}" for name in [
            "MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
            "procedures/perfect-spell.json", "procedures/unholy-ascendance.json",
        ]],
    ]
    current_files = {"current/" + path: blob(commit, path) for path in current_paths}
    current_context = {
        "id": "RANK9-MEMORY-DENIAL6-CURRENT-DIRECTOR-CONTEXT-241", "recordedAtUtc": now,
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"], "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": target["candidate"],
        "historicalCandidateBinding": bind(SOURCE_CANDIDATE, candidate_raw),
        "localCandidateCopySerializationOnlyDifference": {"path": SOURCE_CANDIDATE,
            "bytes": len(local_candidate_copy_raw), "sha256": sha(local_candidate_copy_raw),
            "semanticJsonEqualToQueueBoundCandidate": True},
        "historicalSourceArchiveBinding": bind(SOURCE_ARCHIVE, archive_raw),
        "sourceRefresh": {"sourceFileCount": len(refreshed), "changedSinceCandidate": changed,
                          "priorCandidateLocalCopySerializationOnlyDifference": {"bytes": len(local_candidate_copy_raw),
                              "sha256": sha(local_candidate_copy_raw), "semanticJsonEqual": True},
                          "currentSnapshotBindings": [{"path": path, "bytes": len(raw), "sha256": sha(raw)}
                                                       for path, raw in sorted(current_files.items())]},
        "latestAcceptedOrdinarySpellBatch": {
            "application": "RANK9-CASTINGCOST5-APPLICATION-222",
            "acceptedIds": ["perfect-spell"],
            "unacceptedIds": ["unholy-ascendance"],
            "retainedBlockers": {"unholy-ascendance": ["CC194-B04"]},
            "countsAfter": AUTHORITY, "runtimeSelectionEnabled": False,
            "perfectSpellProcedure": f"current/{candidate_root}/procedures/perfect-spell.json",
        },
        "retainedBlockersOutsideScope": {
            "AG190": {"ids": ["absolute-domination", "puppetmaster-s-realm"], "blockers": ["AG190-B01", "AG190-B02"]},
            "TF192": {"ids": ["time-stop", "eternal-prophecy", "fate-rewrite", "collapse-timeline"],
                      "blockers": ["TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"]},
            "CC194": {"ids": ["unholy-ascendance"], "blockers": ["CC194-B04"]},
        },
        "latestAuditedSpellReturn": {"return": 240, "group": "rank9-casting-cost5",
            "heldIds": ["unholy-ascendance"], "blockerIds": ["CC194-B04"],
            "independentAudit": "current/RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json"},
        "qualification": "Preparation only. Revalidate every source and accepted context against the refreshed current bindings. The historical source candidate is provenance, not authority. Do not alter canonical spell cards, execute supplied programs, or claim runtime, implementation, human-play, balance, cosmology, completion, or release approval.",
    }
    request = (
        "GPT director — continue your selected ordinary-spell review. Review exactly the two current pending Rank9 Memory/Denial6 identities in this packet: mind-collapse and unravel-identity.\n\n"
        f"Workspace branch/HEAD: {branch} / {commit}; current working-tree authority is 811 reviewed-applied / 37 pending / 0 accepted-unapplied, 535 complete standalone procedures and 173 scoped interfaces. The packet hashes every current overlay file, including the applied Return222 index.\n\n"
        "Use the current handoff, queue, pending audit, authored index, catalog, 120 refreshed source bindings, the complete 28 original questions, two focused addenda, 12 required new cases, and ten unchanged future-case obligations. The exact prior Return196 and Return224 audits/receipts/decisions, complete earlier source packets, and latest independently audited Return240 / Return239 / Return238 hold evidence are included. Scope decision-making to the two pending identities only; do not reopen or re-review the four identities accepted in Return196 or anything accepted in Return222. Preserve Return240's CC194-B04 hold for unholy-ascendance; Return239's TF192-B01, TF192-B02, TF192-B04 and TF192-B05 holds; Return238's AG190-B01 and AG190-B02 holds; and all unrelated pending spells.\n\n"
        "Mind Collapse remains under MD196-B01 with MD196-H01/H02/H03/H04/H06/H08 unless resolved by newly bound evidence. Its missing positive witness is an acquired genuine full-turn grant plus complete source-legal actor, preserving the original three-regular-END clock, recharge, Ready history, and all passing evidence. Wizard extra Actions, echoes, initiative reorder, and restricted additional actions are not a full turn. Keep this rank9 spell distinct from rank8 Mental Collapse; preserve its actual three-round Stunned/INT-save text, clock, initial save, concentration-end and suppressed early-escape semantics.\n\n"
        "Unravel Identity remains under MD196-B02 with MD196-H01/H02/H03/H06/H08 unless resolved by newly bound evidence. The missing witness is one actual source-legal multiclass/class-form/maxima/companion dependency integration across affected Base/Arch/Hero capabilities, passives, resources, suppression callbacks and exact recovery. The 16 supplied class files are preserved; do not claim they are absent. No free refill or revival of ended effects. Preserve its one-round false-self belief and exact lifecycle.\n\n"
        "Independently reconcile all relevant original questions and focused addenda, all required cases/future obligations, sources, native card text, acquired routes, histories and reversible state. Return one source-faithful static procedure per identity with concrete branches, explicit lifecycle and forward/inverse operations. Accept only individually passing identities with accepted=true/applied=false. Otherwise retain exact blocker/hold IDs and narrowly identify the minimum missing witness. Provide complete validation counts, safe member manifest with exact hashes, and separate delivery JSON bound to the returned ZIP. Do not edit canonical files or execute supplied programs.\n\n"
    )
    files: dict[str, bytes] = {
        "CURRENT_CONTEXT_241.json": json_bytes(current_context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_241.json": current_raw,
        "PRIOR_CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json": candidate_raw,
        "PRIOR_CURRENT_SOURCE_CONFERENCE_CANDIDATE_224_LOCAL_COPY.json": local_candidate_copy_raw,
        "HISTORICAL_CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json": candidate_195_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": blob(commit, HISTORICAL_CANDIDATE),
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9MEMORYDENIAL6_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_241.txt": request.encode("utf-8"),
        **current_files,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)
    OUT.mkdir(parents=True, exist_ok=True)
    current_candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_241.json"
    current_candidate_path.write_bytes(current_raw)
    packet_path = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_241.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        rows = []
        for name in sorted(files):
            raw = files[name]
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw),
                         "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
        manifest = {"id": "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-PACKET-MANIFEST-241",
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
    delivery = {"id": "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-DELIVERY-241", "status": "PREPARED_UNSENT",
                "archive": packet_binding, "members": len(rows) + 1, "manifestBindings": len(rows),
                "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
                "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
                "historicalSourceArchive": bind(SOURCE_ARCHIVE, archive_raw),
                "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSincePacket224": changed,
                "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_241_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)

    checks = [
        "Packet identifies main/HEAD and binds the current workspace overlay plus exact 811/37/0 authority.",
        "Exactly two current pending Memory/Denial6 identities are next in queue order.",
        "All 120 historical source members match the archived hashes and CRCs.",
        "All 120 source bindings are refreshed from the exact current workspace snapshot, with main/HEAD disclosed separately.",
        "Both native entries and catalog pointers remain exact and pending.",
        "Return222's accepted Perfect Spell procedure and retained Unholy Ascendance blocker are current context.",
        "AG190 and TF192 blockers remain explicitly carried outside this group.",
        "All 28 original questions, two addenda, 12 required cases, and ten future obligations are preserved.",
        "Historical archive paths and current packet member SHA/CRC validate.",
        "Queue-bound prior candidate is taken from its packet archive; the local JSON copy differs only in serialization and parses identically.",
        "Returned packet has a separate exact delivery manifest and no canonical changes.",
    ]
    prep = {"id": "RANK9-MEMORY-DENIAL6-SOURCE-PREPARATION-241", "recordedAtUtc": now,
            "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "sourceCommit": commit, "sourceBranch": branch,
            "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
            "historicalCandidate": bind(SOURCE_CANDIDATE, candidate_raw),
            "historicalArchive": bind(SOURCE_ARCHIVE, archive_raw), "currentDerivedCandidate": candidate_binding,
            "sourceFileCount": len(refreshed), "changedSincePacket224": changed,
            "packet": packet_binding, "deliveryManifest": delivery_binding, "memberCount": len(rows) + 1,
            "checksPassed": len(checks), "checksFailed": 0,
            "checks": [{"check": label, "passed": True} for label in checks],
            "canonicalSpellCardChangesDuringPreparation": False,
            "preexistingReviewIndexOverlay": {"path": INDEX, "bytes": len(blob(commit, INDEX)), "sha256": sha(blob(commit, INDEX))},
            "request": request}
    PREP_PATH.write_bytes(json_bytes(prep))
    prep_binding = bind(PREP_PATH.relative_to(ROOT).as_posix(), PREP_PATH.read_bytes())
    packet_record = {"id": "RANK9MEMORYDENIAL6-PACKET-241", "status": "PREPARED_UNSENT",
                     "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
                     "packet": packet_binding, "deliveryManifest": delivery_binding,
                     "preparation": prep_binding, "conversation": CHAT,
                     "checksPassed": len(checks), "checksFailed": 0}
    PACKET_PATH.write_bytes(json_bytes(packet_record))
    packet_record_binding = bind(PACKET_PATH.relative_to(ROOT).as_posix(), PACKET_PATH.read_bytes())

    pending_after = copy.deepcopy(pending)
    pending_after.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-241", "recordedAtUtc": now,
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
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-241", "recordedAtUtc": now, "next": next_request,
                        "nextPreparedRequest": next_request, "nextGroup": GROUP,
                        "pendingIdentityAudit": pending_binding,
                        "packetStatus": "RANK9_MEMORY_DENIAL6_CURRENT_SOURCE_PACKET_241_PREPARED_UNSENT_811_37",
                        "currentPreparation": prep_binding, "currentPacket": packet_binding,
                        "currentPacketDelivery": delivery_binding})
    QUEUE_PATH.write_bytes(json_bytes(queue_after))
    queue_binding = bind(QUEUE_PATH.relative_to(ROOT).as_posix(), QUEUE_PATH.read_bytes())
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-241", "recordedAtUtc": now,
                          "status": "RANK9_MEMORY_DENIAL6_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37",
                          "currentAuthority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": len(IDS),
                          "pendingIdentityAudit": pending_binding, "nextPreparedRequest": next_request,
                          "currentQueueBinding": queue_binding, "currentPreparation": prep_binding,
                          "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
                          "resumePriority": "Send the fresh 120-source Memory/Denial6 packet to the same GPT director; independently audit exact per-identity decisions, apply only accepted IDs, push, and continue until pending reaches zero."})
    HANDOFF_PATH.write_bytes(json_bytes(handoff_after))
    SNAPSHOT_PATH.write_text(
        f"# Current ordinary spell-review checkpoint 241\n\nAuthority is **811 reviewed / 37 pending / 0 accepted-unapplied**, with 535 complete standalone procedures. The next two-identity group is Rank9 Memory/Denial6. Its fresh packet refreshes all {len(refreshed)} historical source bindings from the current workspace snapshot based on main/HEAD {commit}; overlay hashes are included. It carries Return222's Perfect Spell acceptance and Unholy Ascendance hold.\n\nSee [handoff](CURRENT_HANDOFF_241.json), [queue](CURRENT_SPELL_QUEUE_241.json), [pending audit](CURRENT37_PENDING_IDENTITY_AUDIT_241.json), [packet record](RANK9MEMORYDENIAL6_PACKET_241.json), and [source packet](rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip).\n",
        encoding="utf-8", newline="\n")
    start_path = ROOT / "START_HERE.md"
    old_start = subprocess.check_output(["git", "show", f"{commit}:START_HERE.md"], cwd=ROOT).decode("utf-8-sig")
    start_path.write_text(
        f"**Current ordinary spell-review handoff [241](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_241.json):** authority is 811 reviewed / 37 pending / 0 accepted-unapplied. A fresh 120-source packet for Rank9 Memory/Denial6 is prepared for the GPT director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET_241.json).\n\n" + old_start,
        encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY,
                      "group": GROUP, "sourceFiles": len(refreshed), "changedSincePacket224": changed,
                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                      "queue": queue_binding, "checksPassed": len(checks)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
