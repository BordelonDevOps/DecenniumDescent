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
GROUP = "rank9-elemental-pets2"
IDS = ["elemental-convergence", "elemental-fusion"]
AUTHORITY = {"reviewedApplied": 802, "pending": 46, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 526, "scopedInterfaces": 173}
BRANCH = "codex/ordinary-spell-review-complete"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
CANDIDATE_PATH = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_elemental_pets_2_source_conference_01.json"
ARCHIVE_PATH = "docs/audit/2026-10-08/full-game/DD_Rank9_Elemental_Pets_2_Source_Conference_01.zip"
INDEX_PATH = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG_PATH = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_207.json"
PENDING = AUDIT / "CURRENT46_PENDING_IDENTITY_AUDIT_207.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_207.json"
OUT = AUDIT / "rank9_elementalpets2_current_source_208_prepared"
PACKET = AUDIT / "RANK9ELEMENTALPETS2_PACKET_208.json"
PREP = AUDIT / "RANK9ELEMENTALPETS2_SOURCE_PREPARATION_208.json"
QUEUE_OUT = AUDIT / "CURRENT_SPELL_QUEUE_208.json"
PENDING_OUT = AUDIT / "CURRENT46_PENDING_IDENTITY_AUDIT_208.json"
HANDOFF_OUT = AUDIT / "CURRENT_HANDOFF_208.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def bind(path: str, raw: bytes):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(
        part not in ("", ".", "..") and not part.startswith(".") for part in path.parts
    )


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == BRANCH
    remote = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"],
                                     cwd=ROOT, text=True).split()
    assert remote and remote[0] == commit, (commit, remote)
    assert not OUT.exists() and not any(path.exists() for path in (PACKET, PREP, QUEUE_OUT, PENDING_OUT, HANDOFF_OUT))

    queue_raw, pending_raw, handoff_raw, index_raw, catalog_raw = [
        git_blob(commit, path) for path in (
            QUEUE.relative_to(ROOT).as_posix(), PENDING.relative_to(ROOT).as_posix(),
            HANDOFF.relative_to(ROOT).as_posix(), INDEX_PATH, CATALOG_PATH,
        )
    ]
    queue, pending, handoff, index, catalog = map(read, (queue_raw, pending_raw, handoff_raw, index_raw, catalog_raw))
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 802, "pending": 46}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 526
    assert pending["pendingCount"] == queue["pendingCount"] == 46
    assert pending["currentAuthority"] == AUTHORITY
    assert set(IDS) <= set(pending["pendingIds"])
    target = queue["nextPreparedRequest"]
    assert target["group"] == GROUP and target["pendingIds"] == IDS and target["freshPacketRequiredForCurrentAuthority"] is True

    candidate_raw = git_blob(commit, CANDIDATE_PATH)
    historical_archive_raw = git_blob(commit, ARCHIVE_PATH)
    historical_candidate = read(candidate_raw)
    old_index = {row["id"]: row for row in index["entries"]}
    cards = {row["id"]: row for row in catalog["spells"]}
    assert [row["spellId"] for row in historical_candidate["records"]] == IDS
    assert len(historical_candidate["sourceBindings"]) == 107
    assert len(historical_candidate["questions"]) == 24
    assert len(historical_candidate["futureCaseRequirements"]) == 8
    for sid in IDS:
        assert sid in old_index and old_index[sid]["authoredStatus"] == "pending-authored-procedure"
        assert old_index[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert sid in cards

    historical_sources: dict[str, bytes] = {}
    with zipfile.ZipFile(__import__("io").BytesIO(historical_archive_raw)) as old_zip:
        assert old_zip.testzip() is None and len(old_zip.namelist()) == len(set(old_zip.namelist()))
        for row in historical_candidate["sourceBindings"]:
            raw = old_zip.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            historical_sources[row["path"]] = raw
        archived_candidate = old_zip.read("CANDIDATE.json")
        assert archived_candidate == candidate_raw

    refreshed = []
    changed = []
    current_sources: dict[str, bytes] = {}
    for row in historical_candidate["sourceBindings"]:
        path = row["path"]
        assert safe(path)
        raw = git_blob(commit, path)
        fresh = {**bind(path, raw), "gitBlobSHA1": git_blob_id(commit, path)}
        refreshed.append(fresh)
        current_sources["sources_current/" + path] = raw
        if raw != historical_sources[path]:
            changed.append({"path": path, "historicalBytes": len(historical_sources[path]),
                            "historicalSha256": sha(historical_sources[path]),
                            "currentBytes": len(raw), "currentSha256": sha(raw)})
    assert len(refreshed) == 107 and len({row["path"] for row in refreshed}) == 107

    current = copy.deepcopy(historical_candidate)
    current["historicalSourceBindings"] = copy.deepcopy(historical_candidate["sourceBindings"])
    current["sourceBindings"] = refreshed
    current["currentSourceCommit"] = commit
    current["currentBranch"] = branch
    current["currentAuthority"] = AUTHORITY
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current["historicalCandidateBinding"] = bind(CANDIDATE_PATH, candidate_raw)
    current["historicalSourceArchiveBinding"] = bind(ARCHIVE_PATH, historical_archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed,
                                        "sourceContentsFromGitCommit": commit, "allSourceBindingsRefreshed": True}
    current["countsUnchanged"] = {"reviewed": 802, "pending": 46, "acceptedUnapplied": 0,
                                  "completeStandaloneProcedures": 526}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_802_REVIEWED_46_PENDING"
    current["id"] = "RANK9-ELEMENTAL-PETS2-CURRENT-SOURCE-CONTEXT-208"
    recorded_at = datetime.now(timezone.utc).isoformat()
    current["recordedAtUtc"] = recorded_at
    for row in current["records"]:
        sid = row["spellId"]
        row["historicalIndexEntry"] = copy.deepcopy(row.get("currentIndexEntry"))
        row["currentIndexEntry"] = copy.deepcopy(old_index[sid])
        row["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(cards[sid])
    current_raw = enc(current)

    notes = {
        "id": "RANK9ELEMENTALPETS2-INDEPENDENT-CONFERENCE-208",
        "recordedAtUtc": recorded_at,
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_NOT_ACCEPTED",
        "identities": IDS,
        "sourceCommit": commit,
        "sourceBranch": branch,
        "currentAppliedCounts": {"reviewed": 802, "pending": 46, "acceptedUnapplied": 0,
                                 "completeStandaloneProcedures": 526, "scopedInterfaces": 173},
        "originalQuestionsPreserved": copy.deepcopy(historical_candidate["questions"]),
        "futureCaseRequirementsPreserved": copy.deepcopy(historical_candidate["futureCaseRequirements"]),
        "sourceChecks": [{"path": row["path"], "historicalExact": True, "currentCommit": commit,
                          "currentSha256": row["sha256"]} for row in refreshed],
        "sourceFilesChangedSinceHistoricalCandidate": changed,
        "scope": "Preparation only. The exact current 802/46 authority supersedes historical counts. Preserve all 24 original questions and eight named future-case requirements unchanged. No new rule is adopted; runtime, implementation, human play, balance, cosmology, domain closure, completion, or release is not claimed.",
    }
    notes_raw = enc(notes)
    current_paths = [
        INDEX_PATH, CATALOG_PATH,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT46_PENDING_IDENTITY_AUDIT_207.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_207.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_207.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_RETURN207_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_APPLICATION_207.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_EXACT_ACCEPTANCE_207.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_APPLICATION_VALIDATION_207.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_RETURN207_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_207.md",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9illusionreality5_reviewed_207/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9illusionreality5_reviewed_207/STANDALONE_PROCEDURES.md",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9illusionreality5_reviewed_207/CANDIDATE_PACKAGE_MANIFEST.json",
    ]
    current_files = {"current/" + path: git_blob(commit, path) for path in current_paths}
    current_context = {
        "id": "RANK9-ELEMENTAL-PETS2-CURRENT-DIRECTOR-CONTEXT-208",
        "recordedAtUtc": recorded_at,
        "sourceCommit": commit,
        "sourceBranch": branch,
        "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"],
        "pendingIdentityAudit": pending["id"],
        "currentQueue": queue["id"],
        "latestAppliedBatch": {
            "reviewId": "RANK9-ILLUSIONREALITY5-EXACT-AUTHORED-ACCEPTANCE-207",
            "acceptedIds": ["supreme-illusion", "mirrored-world", "ethereal-disjunction", "illusory-reality"],
            "unacceptedIds": ["soul-reflection"], "blocker": "IR207-B02",
            "scope": "Four exact static-authored procedures are applied. Soul Reflection stays pending for missing source-bound changed-form, attached-phase, death, cargo and concentration lifecycle traces.",
        },
        "historicalCandidateBinding": bind(CANDIDATE_PATH, candidate_raw),
        "historicalArchiveBinding": bind(ARCHIVE_PATH, historical_archive_raw),
        "sourceRefresh": {"sourceFileCount": len(refreshed), "changedSinceHistoricalCandidate": changed},
        "scopeBoundary": "Review only Elemental Convergence and Elemental Fusion. Do not reopen feats, the completed 16, completed spell batches, or other identities. Keep Soul Reflection pending under IR207-B02. Runtime, source/access, implementation, human-play, balance, cosmology, domain closure, completion, and release remain unapproved.",
    }
    request = (
        f"GPT director — review exactly these two current pending ordinary spells: {', '.join(IDS)}.\n\n"
        f"Source branch and commit: {branch} / {commit}. Current authority: 802 reviewed-applied / 46 pending / 0 accepted-unapplied; 526 complete standalone procedures; 173 scoped interfaces.\n\n"
        "Use the refreshed 107 source bindings and exact current catalog, index, pending audit, queue, handoff, and Return207 application evidence. Preserve all 24 original questions and all eight named future-case requirements. The older Water-pending language and 616/232 counts are historical only.\n\n"
        "Return complete source-faithful static procedures, exact class access/source bindings, question dispositions, all required positive and adverse cases, future-obligation dispositions, reversible state/event operations, and an exact manifest. Mark only individually complete identities accepted=true and applied=false; name evidence-specific blockers for each held identity. Do not claim runtime, canonical card/rule, implementation, human-play, balance, cosmology, domain closure, completion, or release approval. Apply only exact independently audited accepted IDs after return. Keep Soul Reflection and all other groups unchanged.\n"
    )
    files = {
        "CURRENT_CONTEXT_208.json": enc(current_context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_208.json": current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": historical_archive_raw,
        "NOTES/INDEPENDENT_CONFERENCE_208.json": notes_raw,
        "REQUEST_208.txt": request.encode("utf-8"),
        **current_files,
        **current_sources,
    }
    for name in files:
        assert safe(name), name
    OUT.mkdir(parents=True)
    current_candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_208.json"
    current_candidate_path.write_bytes(current_raw)
    rows = []
    zip_path = OUT / "DD_Rank9_ElementalPets2_CurrentSource_208.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet_zip:
        for name, raw in sorted(files.items()):
            packet_zip.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw),
                         "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {"id": "RANK9-ELEMENTAL-PETS2-CURRENT-SOURCE-MANIFEST-208",
                    "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                    "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows}
        packet_zip.writestr("MANIFEST.json", enc(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(zip_path) as packet_zip:
        assert packet_zip.testzip() is None and len(packet_zip.namelist()) == len(rows) + 1
        assert len(packet_zip.namelist()) == len(set(packet_zip.namelist()))
        for row in rows:
            raw = packet_zip.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]

    packet_bytes = zip_path.read_bytes()
    archive_binding = bind(zip_path.relative_to(ROOT).as_posix(), packet_bytes)
    candidate_binding = bind(current_candidate_path.relative_to(ROOT).as_posix(), current_raw)
    delivery = {
        "id": "RANK9-ELEMENTAL-PETS2-CURRENT-SOURCE-DELIVERY-208",
        "status": "PREPARED_UNSENT", "archive": archive_binding,
        "members": len(rows) + 1, "manifestBindings": len(rows),
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
        "historicalCandidate": bind(CANDIDATE_PATH, candidate_raw),
        "historicalSourceArchive": bind(ARCHIVE_PATH, historical_archive_raw),
        "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceHistoricalCandidate": changed,
        "originalQuestions": 24, "futureCaseRequirements": 8,
        "accepted": False, "applied": False, "conversation": CHAT,
    }
    delivery_raw = enc(delivery)
    delivery_path = OUT / "DD_Rank9_ElementalPets2_CurrentSource_208_DELIVERY.json"
    delivery_path.write_bytes(delivery_raw)
    preparation = {
        "id": "RANK9-ELEMENTAL-PETS2-SOURCE-PREPARATION-208",
        "recordedAtUtc": recorded_at, "status": "PASS", "sourceCommit": commit,
        "sourceBranch": branch, "sourceAuthority": AUTHORITY, "targetGroup": GROUP,
        "pendingIds": IDS, "currentCandidate": candidate_binding,
        "historicalCandidate": bind(CANDIDATE_PATH, candidate_raw),
        "historicalArchive": bind(ARCHIVE_PATH, historical_archive_raw),
        "packet": archive_binding,
        "deliveryManifest": bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw),
        "refreshedBindings": len(refreshed), "changedHistoricalBindings": changed,
        "originalQuestions": 24, "futureCaseRequirements": 8,
        "canonicalChanges": False, "accepted": False, "applied": False,
    }
    PREP.write_bytes(enc(preparation))
    packet_record = {
        "id": "RANK9ELEMENTALPETS2-PACKET-208", "status": "PREPARED_UNSENT",
        "group": GROUP, "pendingIds": IDS, "sourceAuthority": AUTHORITY,
        "sourceCommit": commit, "archive": archive_binding,
        "deliveryManifest": bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw),
        "candidate": candidate_binding, "originalQuestions": 24,
        "futureCaseRequirements": 8, "refreshedSourceBindings": len(refreshed),
        "canonicalChanges": False,
    }
    PACKET.write_bytes(enc(packet_record))

    pending_copy = copy.deepcopy(pending)
    pending_copy.update({
        "id": "CURRENT46-PENDING-IDENTITY-AUDIT-208", "recordedAtUtc": recorded_at,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": bind(INDEX_PATH, index_raw), "catalogBinding": bind(CATALOG_PATH, catalog_raw),
        "authoredCounts": index["authoredCounts"], "currentAuthority": AUTHORITY,
    })
    PENDING_OUT.write_bytes(enc(pending_copy))
    queue_copy = copy.deepcopy(queue)
    queue_copy.update({"id": "SPELL-REVIEW-QUEUE-208", "recordedAtUtc": recorded_at,
                       "packetStatus": "RANK9_ELEMENTAL_PETS2_FRESH_CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                       "parentQueue": queue["id"], "currentAuthority": AUTHORITY})
    queue_copy["pendingIdentityAudit"] = {
        "id": pending_copy["id"], "path": PENDING_OUT.relative_to(ROOT).as_posix(),
        "pendingCount": 46, "sha256": sha(PENDING_OUT.read_bytes()),
    }
    queue_copy["currentPreparation"] = bind(PREP.relative_to(ROOT).as_posix(), PREP.read_bytes())
    queue_copy["currentPacket"] = archive_binding
    queue_copy["currentPacketDelivery"] = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)
    queue_copy["currentPacketCandidate"] = candidate_binding
    queue_copy["currentPacketAudit"] = {"path": PACKET.relative_to(ROOT).as_posix(), "sha256": sha(PACKET.read_bytes())}
    queue_copy["directorSubmission"] = {"status": "prepared-unsent", "conversation": CHAT}
    queue_copy["nextPreparedRequest"].update({
        "status": "FRESH_CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority": False,
        "currentCandidate": candidate_binding, "currentPacket": archive_binding,
        "deliveryManifest": bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw),
        "originalQuestions": 24, "futureCaseRequirements": 8,
    })
    QUEUE_OUT.write_bytes(enc(queue_copy))
    handoff_copy = copy.deepcopy(handoff)
    handoff_copy.update({
        "id": "CURRENT-HANDOFF-208", "recordedAtUtc": recorded_at,
        "status": "RANK9_ELEMENTAL_PETS2_FRESH_SOURCE_PACKET_PREPARED_UNSENT_46_PENDING",
        "parentHandoff": handoff["id"], "currentQueue": {"path": QUEUE_OUT.relative_to(ROOT).as_posix(),
                                                            "sha256": sha(QUEUE_OUT.read_bytes())},
        "currentQueueBinding": bind(QUEUE_OUT.relative_to(ROOT).as_posix(), QUEUE_OUT.read_bytes()),
        "pendingIdentityAudit": {"id": pending_copy["id"], "path": PENDING_OUT.relative_to(ROOT).as_posix(),
                                 "pendingCount": 46, "sha256": sha(PENDING_OUT.read_bytes())},
        "sourcePreparation": bind(PREP.relative_to(ROOT).as_posix(), PREP.read_bytes()),
        "currentPacket": archive_binding, "currentPacketCandidate": candidate_binding,
        "currentPacketDeliveryManifest": bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw),
        "directorSubmission": {"status": "prepared-unsent", "conversation": CHAT},
    })
    handoff_copy["nextPreparedRequest"].update({
        "status": "FRESH_CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority": False,
        "currentCandidate": candidate_binding, "currentPacket": archive_binding,
        "deliveryManifest": bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw),
        "originalQuestions": 24, "futureCaseRequirements": 8,
    })
    HANDOFF_OUT.write_bytes(enc(handoff_copy))
    print(json.dumps({
        "status": "PASS", "sourceCommit": commit, "sourceAuthority": AUTHORITY,
        "refreshedBindings": len(refreshed), "changedBindings": len(changed),
        "originalQuestions": 24, "futureCaseRequirements": 8,
        "packetMembers": len(rows) + 1, "packetBytes": archive_binding["bytes"],
        "packetSha256": archive_binding["sha256"], "out": str(zip_path),
    }, indent=2))


if __name__ == "__main__":
    main()
