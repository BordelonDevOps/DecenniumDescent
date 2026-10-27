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
GROUP = "rank9-planar-gates5"
IDS = ["gate", "absolute-gate", "banishment-gate", "planar-sanctuary", "conjure-demiplane-fortress"]
AUTHORITY = {"reviewedApplied": 790, "pending": 58, "acceptedUnapplied": 0, "completeStandaloneProcedures": 514, "scopedInterfaces": 173}
BRANCH = "codex/ordinary-spell-review-complete"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_198.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT58_PENDING_IDENTITY_AUDIT_198.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_198.json"
CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_planar_gates_5_source_conference_01.json"
ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Planar_Gates_5_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PLANARGATES5_NEXT_CONFERENCE_NOTES_129.json"
OUT = AUDIT / "rank9_planargates5_current_source_199_prepared"
PACKET = AUDIT / "RANK9PLANARGATES5_PACKET_199.json"
PREP = AUDIT / "RANK9PLANARGATES5_SOURCE_PREPARATION_199.json"
PENDING_OUT = AUDIT / "CURRENT58_PENDING_IDENTITY_AUDIT_199.json"
QUEUE_OUT = AUDIT / "CURRENT_SPELL_QUEUE_199.json"
HANDOFF_OUT = AUDIT / "CURRENT_HANDOFF_199.json"
SNAPSHOT = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_199.md"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def bind(path: str, raw: bytes):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def add(checks: list, name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == BRANCH
    remote_row = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=ROOT, text=True).split()
    assert remote_row and remote_row[0] == commit, (commit, remote_row)
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    assert all(line[3:].startswith("docs/audit/2026-10-08/full-game/director-spell-review-129/__pycache__/" ) or line[3:] == "docs/audit/2026-10-08/full-game/director-spell-review-129/prepare_planar_gates5_current_199.py" for line in dirty), dirty
    assert not OUT.exists() and not any(path.exists() for path in (PACKET, PREP, PENDING_OUT, QUEUE_OUT, HANDOFF_OUT, SNAPSHOT))

    queue, pending, handoff, index, catalog = [read(git_blob(commit, path)) for path in (QUEUE, PENDING, HANDOFF, INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 790, "pending": 58}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 514
    assert pending["pendingCount"] == len(pending["pendingIds"]) == queue["pendingCount"] == 58
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == 5 and target["freshPacketRequiredForCurrentAuthority"] is True
    candidate_raw = git_blob(commit, CANDIDATE)
    archive_raw = (ROOT / ARCHIVE).read_bytes()
    notes_raw = git_blob(commit, NOTES)
    historical, notes = read(candidate_raw), read(notes_raw)
    assert sha(candidate_raw) == target["candidate"]["sha256"] and len(candidate_raw) == target["candidate"]["bytes"]
    assert sha(archive_raw) == target["archive"]["sha256"] and len(archive_raw) == target["archive"]["bytes"]
    assert [record["spellId"] for record in historical["records"]] == IDS
    assert len(historical["sourceBindings"]) == 132
    assert notes["identities"] == IDS
    assert len(notes["completeOriginalQuestionsUnchanged"]) == 30
    assert len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["allQuestions"]) == 32
    assert len(notes["requiredNewCases"]) == 10 and len(notes["originalFutureCaseRequirementsUnchanged"]) == 9

    entries = {entry["id"]: entry for entry in index["entries"]}
    catalog_rows = {entry["id"]: entry for entry in catalog["spells"]}
    pending_ids = set(pending["pendingIds"])
    assert set(IDS) <= pending_ids
    for sid in IDS:
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        pointer = int(entries[sid]["wholeCardPointer"].rsplit("/", 1)[1])
        assert catalog["spells"][pointer]["id"] == sid == catalog_rows[sid]["id"]

    historical_members = {}
    with zipfile.ZipFile(ROOT / ARCHIVE) as old_archive:
        assert old_archive.testzip() is None and len(old_archive.namelist()) == len(set(old_archive.namelist()))
        for source in historical["sourceBindings"]:
            raw = old_archive.read("sources/" + source["path"])
            assert len(raw) == source["bytes"] and sha(raw) == source["sha256"]
            historical_members[source["path"]] = raw

    refreshed, current_sources, changed = [], {}, []
    for old in historical["sourceBindings"]:
        path = old["path"]
        assert safe_member(path) and not Path(path).is_absolute()
        raw = git_blob(commit, path)
        row = {"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": git_blob_id(commit, path)}
        refreshed.append(row)
        current_sources["sources_current/" + path] = raw
        if raw != historical_members[path]:
            changed.append({"path": path, "historicalBytes": len(historical_members[path]), "historicalSha256": sha(historical_members[path]), "currentBytes": len(raw), "currentSha256": sha(raw)})
    assert len(refreshed) == 132 and len({row["path"] for row in refreshed}) == 132

    now = datetime.now(timezone.utc).isoformat()
    current = copy.deepcopy(historical)
    current["historicalSourceBindings"] = copy.deepcopy(historical["sourceBindings"])
    current["sourceBindings"] = refreshed
    current["currentSourceCommit"] = commit
    current["currentBranch"] = branch
    current["currentAuthority"] = AUTHORITY
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": 5}
    current["historicalCandidateBinding"] = bind(CANDIDATE, candidate_raw)
    current["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    current["historicalSourceArchiveBinding"] = bind(ARCHIVE, archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed, "sourceContentsFromGitCommit": commit, "allSourceBindingsRefreshed": True}
    current["countsUnchanged"] = {"reviewed": 790, "pending": 58}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_790_REVIEWED_58_PENDING_AUTHORITY"
    current["id"] = "RANK9-PLANAR-GATES5-CURRENT-SOURCE-CONTEXT-199"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        sid = record["spellId"]
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
    current_raw = json_bytes(current)

    carried = {key: pending.get(key, {}) for key in pending if key.startswith("retainedReturn")}
    current_paths = [INDEX, CATALOG, QUEUE, PENDING, HANDOFF, "START_HERE.md"]
    current_paths += [
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/PROCEDURES.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/SHARED_RULES.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/HOLD_REGISTER.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/REVIEW_RECEIPT.json",
        "DescentReviewChanges/ReviewBible/docs/spells/candidates/TRANSPORT6_REVIEWED_128.md",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/CANDIDATE_PACKAGE_MANIFEST.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/HOLD_REGISTER.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/procedures/faction-omniscience-supreme.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_EXACT_ACCEPTANCE_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_APPLICATION_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_APPLICATION_VALIDATION_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_DIRECTOR_DECISION_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_RETURN198_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_RETURN198_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT58_PENDING_IDENTITY_AUDIT_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_198.md",
    ]
    current_files = {"current/" + path: git_blob(commit, path) for path in current_paths}
    latest_context = {
        "id": "RANK9-PLANAR-GATES5-CURRENT-DIRECTOR-CONTEXT-199",
        "recordedAtUtc": now,
        "sourceCommit": commit,
        "sourceBranch": branch,
        "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": 5},
        "currentIndexCounts": index["authoredCounts"],
        "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": target["candidate"],
        "historicalCandidateBinding": bind(CANDIDATE, candidate_raw),
        "historicalSourceArchiveBinding": bind(ARCHIVE, archive_raw),
        "sourceRefresh": {"sourceFileCount": len(refreshed), "changedSinceCandidate": changed},
        "latestAcceptedOrdinarySpellBatch": {
            "application": "RANK9-KNOWLEDGEREVELATION5-APPLICATION-198",
            "acceptedIds": ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"],
            "unacceptedIds": ["faction-omniscience-supreme"],
            "retainedBlockers": {"faction-omniscience-supreme": ["KR198-B01"]},
            "countsAfter": AUTHORITY,
            "runtimeSelectionEnabled": False,
            "procedureModel": "current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json",
            "independentAudit": "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_RETURN198_INDEPENDENT_AUDIT.json",
        },
        "acceptedTransport6Context": {
            "status": "Static authored procedures applied; do not broaden exact spell-local predicates or terminal settlements.",
            "model": "current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/MODEL.json",
            "scope": "Use the exact accepted Transport6 contracts and applicable predicates for planar transit, terminal settlement, object/circle travel, persistent gates and source endings. Preserve its scoped exceptions and do not convert every portal into generic teleportation.",
        },
        "retainedNamedBlockersOutsideScope": carried,
        "qualification": "Preparation only. Refresh every source binding against the exact pushed source commit. The historical source conference is provenance, not current authority. Preserve accepted Transport6 and Knowledge/Revelation scopes, native spell cards, current access, pending identities, and all retained blockers; do not infer new cosmology or alter canonical rules.",
    }
    context_raw = json_bytes(latest_context)

    extra_text = "\n\n".join(f"{item['id']}: {item['exactSourceOrConflict']} {item['request']}" for item in notes["focusedAdditionalQuestions"])
    request = (
        "GPT director — review exactly the five current pending Rank9 Planar Gates5 identities in this packet.\n\n"
        f"Source branch and commit: {branch} / {commit}. Current authority: 790 reviewed-applied / 58 pending / 0 accepted-unapplied; 514 complete standalone procedures; 173 scoped interfaces.\n\n"
        f"Scope only: {', '.join(IDS)}. Use the attached refreshed 132-source bindings, exact current queue, handoff, pending audit, index, catalog, accepted Transport6 package, and the current Knowledge/Revelation5 application context. Preserve all 30 original questions, both focused addenda, all 10 required new cases, and all 9 future-case requirements. Do not reopen closed feat identities, completed spell cohorts, or the one current KR198-B01 faction hold.\n\n"
        "Resolve source route and placement separately for Gate: preserve its three actual placements and class access, including the broader printed destination language without inventing Transmutation access, a fourth identity, creature calling, or command power. Distinguish local opening range from destination selection; specify portal topology, aperture, passage classification, concentration/open duration and closure as explicit NEW choices. Preserve actual body fit, carried inventory, mounts, forced movement, custody, and safe complete transit.\n\n"
        "For Absolute Gate, retain the real ten-minute paid cast, known-site qualification, indefinite reuse, and exact permission records. For Banishment Gate, demonstrate genuine source-qualified triggers and multiple independently timed occupants, cargo, death, expired summons and return/closure settlement. For Planar Sanctuary, bind effect immunity to actual origin and selected plane, including beneficial, physical, magical, informational and ongoing effects; handle self-plane selection, movement/copy/transfer and source provenance without origin laundering. For Conjure Demiplane Fortress, give a useful permanent navigable fortified space, access and custody, actual work/rest inputs, creator absence, and complete occupied closure/dispel/destruction settlement with all identities and clocks preserved.\n\n"
        "Current accepted Transport6 distinguishes teleport transactions, nonteleport planar passage, and terminal settlement. Apply its exact spell-local predicates and adopted exceptions; do not treat every portal as teleportation or change older sources by implication. Keep generated spaces distinct from canonical planes. No disappearance, duplication, resurrection, free relocation, free inputs, unbounded refresh, invented realm, or unsupported source exception. The current Knowledge/Revelation5 batch has four accepted static procedures; Faction Omniscience Supreme remains held under KR198-B01. Carry all preexisting blocker IDs forward unchanged.\n\n"
        f"Focused director addenda:\n{extra_text}\n\n"
        "Return one complete source-faithful static procedure per identity, with concrete positive, boundary and failure branches; full lifecycle and exact procedure text; accepted access and class placement; preserved original obligations; per-question/case/future-obligation dispositions; full reversible event/state operations; exact source bindings and package manifests. Mark only individually passing identities accepted=true and applied=false. Name specific blockers for every held identity. No runtime, canonical card/rule, cosmology, human-play, balance, completion or release approval. The exact accepted IDs will be independently audited, applied and pushed before the next group proceeds."
    )

    files = {
        "CURRENT_CONTEXT_199.json": context_raw,
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json": current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9PLANARGATES5_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_199.txt": request.encode("utf-8"),
        **current_files,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)
    OUT.mkdir(parents=True, exist_ok=False)
    current_candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"
    current_candidate_path.write_bytes(current_raw)
    archive_path = OUT / "DD_Rank9_PlanarGates5_CurrentSource_199.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        member_rows = []
        for name in sorted(files):
            raw = files[name]
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            member_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {"id": "RANK9-PLANAR-GATES5-CURRENT-SOURCE-PACKET-MANIFEST-199", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(member_rows), "members": member_rows}
        packet.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    checks = []
    with zipfile.ZipFile(archive_path) as packet:
        names = packet.namelist()
        add(checks, "ZIP manifest, uniqueness, and CRC are valid", packet.testzip() is None and len(names) == len(member_rows) + 1 and len(names) == len(set(names)), {"members": len(names), "manifestRows": len(member_rows)})
        packet_members_verified = True
        for row in member_rows:
            h, crc, size = hashlib.sha256(), 0, 0
            with packet.open(row["path"]) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(chunk)
                    h.update(chunk)
                    crc = zlib.crc32(chunk, crc)
            if not (size == row["bytes"] and h.hexdigest() == row["sha256"] and f"{crc & 0xffffffff:08x}" == row["crc32"]):
                packet_members_verified = False
            assert packet_members_verified
    archive_raw_out = archive_path.read_bytes()
    archive_binding = bind(archive_path.relative_to(ROOT).as_posix(), archive_raw_out)
    candidate_binding = bind(current_candidate_path.relative_to(ROOT).as_posix(), current_raw)
    delivery = {"id": "RANK9-PLANAR-GATES5-CURRENT-SOURCE-DELIVERY-199", "status": "PREPARED_UNSENT", "archive": archive_binding, "members": len(member_rows) + 1, "manifestBindings": len(member_rows), "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding, "historicalCandidate": bind(CANDIDATE, candidate_raw), "historicalSourceArchive": bind(ARCHIVE, archive_raw), "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceHistoricalCandidate": changed, "accepted": False, "applied": False, "conversation": CHAT}
    delivery_raw = json_bytes(delivery)
    delivery_path = OUT / "DD_Rank9_PlanarGates5_CurrentSource_199_DELIVERY.json"
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)
    prep = {"id": "RANK9-PLANAR-GATES5-SOURCE-PREPARATION-199", "recordedAtUtc": now, "status": "PASS", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": IDS, "currentCandidate": candidate_binding, "historicalCandidate": bind(CANDIDATE, candidate_raw), "historicalArchive": bind(ARCHIVE, archive_raw), "packet": archive_binding, "deliveryManifest": delivery_binding, "refreshedBindings": len(refreshed), "changedHistoricalBindings": changed, "questions": {"original": 30, "addenda": 2, "total": 32}, "requiredMainCases": 10, "futureCaseRequirements": 9, "canonicalChanges": False, "accepted": False, "applied": False}
    (AUDIT / "RANK9PLANARGATES5_SOURCE_PREPARATION_199.json").write_bytes(json_bytes(prep))
    packet_record = {"id": "RANK9PLANARGATES5-PACKET-199", "status": "PREPARED_UNSENT", "group": GROUP, "pendingIds": IDS, "sourceAuthority": AUTHORITY, "sourceCommit": commit, "archive": archive_binding, "deliveryManifest": delivery_binding, "candidate": candidate_binding, "questions": 32, "requiredMainCases": 10, "futureCaseRequirements": 9, "refreshedSourceBindings": len(refreshed), "canonicalChanges": False}
    (AUDIT / "RANK9PLANARGATES5_PACKET_199.json").write_bytes(json_bytes(packet_record))

    pending_audit = {key: copy.deepcopy(value) for key, value in pending.items() if key.startswith("retainedReturn")}
    pending_audit.update({"id": "CURRENT58-PENDING-IDENTITY-AUDIT-199", "recordedAtUtc": now, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX, git_blob(commit, INDEX)), "catalogBinding": bind(CATALOG, git_blob(commit, CATALOG)), "authoredCounts": index["authoredCounts"], "pendingCount": 58, "pendingIds": pending["pendingIds"], "allPendingExistInSourceCatalog": set(pending["pendingIds"]) <= set(catalog_rows), "acceptedUnapplied": 0, "retainedReturn198Blockers": pending.get("retainedReturn198Blockers", {}), "closed335AndCompletedCohortsReopened": False, "currentAuthority": AUTHORITY})
    PENDING_OUT.write_bytes(json_bytes(pending_audit))
    packet_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": 5, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": False, "packet": archive_binding, "deliveryManifest": delivery_binding, "packetRecord": bind(PACKET.relative_to(ROOT).as_posix(), (AUDIT / PACKET.name).read_bytes()), "sourcePreparation": bind(PREP.relative_to(ROOT).as_posix(), (AUDIT / PREP.name).read_bytes())}
    q1 = copy.deepcopy(queue)
    q1.update({"id": "SPELL-REVIEW-QUEUE-199", "recordedAtUtc": now, "nextGroup": GROUP, "next": packet_request, "nextPreparedRequest": packet_request, "packetStatus": "RANK9_PLANAR_GATES5_PACKET_199_PREPARED_UNSENT_790_58", "currentPacket": archive_binding, "currentPacketDelivery": delivery_binding, "currentPreparation": bind(PREP.relative_to(ROOT).as_posix(), (AUDIT / PREP.name).read_bytes()), "pendingIdentityAudit": {"path": PENDING_OUT.relative_to(ROOT).as_posix(), "pending": 58, "sha256": sha(PENDING_OUT.read_bytes())}})
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        q1.pop(key, None)
    q1.update({"currentPacket": archive_binding, "currentPacketDelivery": delivery_binding, "currentPreparation": bind(PREP.relative_to(ROOT).as_posix(), (AUDIT / PREP.name).read_bytes())})
    new_groups = []
    for old_group in q1["currentPendingGroups"]:
        if old_group["group"] == GROUP:
            old_group = copy.deepcopy(old_group)
            old_group.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_790_58", "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": archive_binding, "preparedDelivery": delivery_binding})
        new_groups.append(old_group)
    q1["currentPendingGroups"] = new_groups
    (AUDIT / QUEUE_OUT.name).write_bytes(json_bytes(q1))
    h1 = copy.deepcopy(handoff)
    h1.update({"id": "CURRENT-HANDOFF-199", "recordedAtUtc": now, "status": "RANK9_PLANAR_GATES5_PACKET_199_PREPARED_UNSENT_790_58", "currentAuthority": AUTHORITY, "currentIndexBinding": bind(INDEX, git_blob(commit, INDEX)), "currentCatalogBinding": bind(CATALOG, git_blob(commit, CATALOG)), "pendingIdentityAudit": {"id": pending_audit["id"], "path": PENDING_OUT.relative_to(ROOT).as_posix(), "pendingCount": 58, "sha256": sha(PENDING_OUT.read_bytes())}, "nextGroup": GROUP, "nextPreparedRequest": packet_request, "currentQueueBinding": bind(QUEUE_OUT.relative_to(ROOT).as_posix(), (AUDIT / QUEUE_OUT.name).read_bytes()), "currentPacket": archive_binding, "currentPacketDelivery": delivery_binding, "sourcePreparation": bind(PREP.relative_to(ROOT).as_posix(), (AUDIT / PREP.name).read_bytes()), "resumePriority": "Submit the fresh Rank9 Planar Gates5 packet 199 to the GPT director; independently audit its return, apply and push only exact accepted IDs, and continue until pending is zero."})
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        h1.pop(key, None)
    h1.update({"currentPacket": archive_binding, "currentPacketDelivery": delivery_binding, "currentPreparation": bind(PREP.relative_to(ROOT).as_posix(), (AUDIT / PREP.name).read_bytes())})
    (AUDIT / HANDOFF_OUT.name).write_bytes(json_bytes(h1))
    SNAPSHOT.write_text("# Current ordinary spell-review checkpoint 199\n\n" f"Applied the four accepted Knowledge/Revelation5 procedures. Faction Omniscience Supreme remains held under KR198-B01. Authority: **790 reviewed / 58 pending / 0 accepted-unapplied**, 514 complete procedures. The next exact group is Rank9 Planar Gates5; its fresh source packet is prepared for the GPT director at this authority.\n", encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(f"**Current ordinary spell-review handoff [199](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_199.json):** Authority is **790 reviewed / 58 pending / 0 accepted-unapplied**. The fresh Rank9 Planar Gates5 packet is prepared for the GPT director. Faction Omniscience Supreme remains pending under KR198-B01.\n\n" + old_start, encoding="utf-8", newline="\n")

    checks = [
        {"check": "Preparation binds the pushed HEAD and exact 790/58/0 authority", "passed": commit == remote_row[0] and q1["currentAuthority"] == AUTHORITY and h1["currentAuthority"] == AUTHORITY},
        {"check": "Exactly five current pending Planar Gates5 identities are next in queue order", "passed": target["pendingIds"] == IDS and set(IDS) <= pending_ids and pending_audit["pendingCount"] == 58},
        {"check": "All 132 historical source members match original bytes and hashes", "passed": len(historical_members) == len(refreshed) == 132},
        {"check": "All source bindings are refreshed from the exact current Git commit", "passed": current["currentSourceCommit"] == commit and current["currentAuthority"] == AUTHORITY and current["sourceBindingRefresh"]["allSourceBindingsRefreshed"]},
        {"check": "All five native entries, access routes, and catalog pointers remain pending and exact", "passed": all(entries[s]["authoredStatus"] == "pending-authored-procedure" and entries[s]["sourceStatus"] == "blocked-pending-operational-review" for s in IDS)},
        {"check": "Transport6 and current Knowledge/Revelation5 contexts are included", "passed": all("current/" + path in files for path in current_paths if "transport6_reviewed_128" in path or "rank9knowledgerevelation5_reviewed_198" in path)},
        {"check": "All 30 original questions, two addenda, ten required cases, and nine future requirements are retained", "passed": len(notes["allQuestions"]) == 32 and len(notes["requiredNewCases"]) == 10 and len(notes["originalFutureCaseRequirementsUnchanged"]) == 9},
        {"check": "Current KR198 blocker and all carried blocker records remain outside scope", "passed": "KR198-B01" in json.dumps(carried) and len(carried) >= 1},
        {"check": "Every packet member matches the manifest size, SHA, and CRC", "passed": packet_members_verified and len(member_rows) + 1 == delivery["members"] and archive_binding["bytes"] == len(archive_raw_out) and archive_binding["sha256"] == sha(archive_raw_out)},
    ]
    failed = [check for check in checks if not check["passed"]]
    verification = {"id": "RANK9-PLANAR-GATES5-PACKET199-INDEPENDENT-VERIFICATION", "recordedAtUtc": now, "status": "PASS" if not failed else "FAIL", "checksPassed": len(checks) - len(failed), "checksFailed": len(failed), "checks": checks, "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "packet": archive_binding, "delivery": delivery_binding, "accepted": False, "applied": False}
    (AUDIT / "RANK9PLANARGATES5_PACKET199_INDEPENDENT_VERIFICATION.json").write_bytes(json_bytes(verification))
    assert not failed, failed
    print(json.dumps({"status": verification["status"], "checksPassed": verification["checksPassed"], "checksFailed": verification["checksFailed"], "packet": archive_binding, "delivery": delivery_binding, "changedSourceBindings": len(changed), "changedPaths": [item["path"] for item in changed], "questionCount": 32, "mainCases": 10, "futureRequirements": 9}, indent=2))


if __name__ == "__main__":
    main()
