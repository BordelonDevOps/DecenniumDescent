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
GROUP = "rank9-impact-exile4"
IDS = ["eternal-anvil", "reverse-gravity-field", "transmute-flesh-to-energy", "planar-collapse"]
AUTHORITY = {"reviewedApplied": 795, "pending": 53, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 519, "scopedInterfaces": 173}
BRANCH = "codex/ordinary-spell-review-complete"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_202.json"
PENDING = AUDIT / "CURRENT53_PENDING_IDENTITY_AUDIT_202.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_202.json"
CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_impact_exile_4_source_conference_01.json"
ARCHIVE = FULL / "DD_Rank9_Impact_Exile_4_Source_Conference_01.zip"
OLD_NOTES = AUDIT / "RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json"
OUT = AUDIT / "rank9_impactexile4_current_source_203_prepared"
PACKET = AUDIT / "RANK9IMPACTEXILE4_PACKET_203.json"
PREP = AUDIT / "RANK9IMPACTEXILE4_SOURCE_PREPARATION_203.json"
PENDING_OUT = AUDIT / "CURRENT53_PENDING_IDENTITY_AUDIT_203.json"
QUEUE_OUT = AUDIT / "CURRENT_SPELL_QUEUE_203.json"
HANDOFF_OUT = AUDIT / "CURRENT_HANDOFF_203.json"
SNAPSHOT = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_203.md"
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
    return bool(name) and "\\" not in name and not path.is_absolute() and all(
        part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def add(checks: list, name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == BRANCH
    remote_row = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=ROOT, text=True).split()
    assert remote_row and remote_row[0] == commit, (commit, remote_row)
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
    allowed_dirty = {
        "docs/audit/2026-10-08/full-game/director-spell-review-129/prepare_impactexile4_current_203.py",
        "START_HERE.md",
    }
    assert all(line[3:] in allowed_dirty for line in dirty), dirty
    assert not OUT.exists() and not any(path.exists() for path in (PACKET, PREP, PENDING_OUT, QUEUE_OUT, HANDOFF_OUT, SNAPSHOT))

    queue, pending, handoff, index, catalog = [read(git_blob(commit, path)) for path in (
        QUEUE.relative_to(ROOT).as_posix(), PENDING.relative_to(ROOT).as_posix(),
        HANDOFF.relative_to(ROOT).as_posix(), INDEX, CATALOG)]
    assert queue["nextGroup"] == handoff["nextGroup"] == GROUP
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 795, "pending": 53}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 519
    assert pending["pendingCount"] == len(pending["pendingIds"]) == queue["pendingCount"] == 53
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == len(IDS)
    assert target["freshPacketRequiredForCurrentAuthority"] is True
    candidate_raw = git_blob(commit, CANDIDATE)
    archive_raw = ARCHIVE.read_bytes()
    notes_raw = git_blob(commit, OLD_NOTES.relative_to(ROOT).as_posix())
    historical, old_notes = read(candidate_raw), read(notes_raw)
    assert sha(candidate_raw) == target["candidate"]["sha256"] and len(candidate_raw) == target["candidate"]["bytes"]
    assert sha(archive_raw) == target["archive"]["sha256"] and len(archive_raw) == target["archive"]["bytes"]
    assert [record["spellId"] for record in historical["records"]] == IDS
    assert len(historical["sourceBindings"]) == 149
    assert old_notes["identities"] == IDS
    assert len(historical["questions"]) == 26
    assert len(old_notes["focusedAdditionalQuestions"]) == 2
    assert len(old_notes["requiredNewCases"]) == 8
    assert len(historical["futureCaseRequirements"]) == 7

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
    with zipfile.ZipFile(ARCHIVE) as old_archive:
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
            changed.append({"path": path, "historicalBytes": len(historical_members[path]),
                           "historicalSha256": sha(historical_members[path]),
                           "currentBytes": len(raw), "currentSha256": sha(raw)})
    assert len(refreshed) == 149 and len({row["path"] for row in refreshed}) == 149

    now = datetime.now(timezone.utc).isoformat()
    current = copy.deepcopy(historical)
    current["historicalSourceBindings"] = copy.deepcopy(historical["sourceBindings"])
    current["sourceBindings"] = refreshed
    current["currentSourceCommit"] = commit
    current["currentBranch"] = branch
    current["currentAuthority"] = AUTHORITY
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current["historicalCandidateBinding"] = bind(CANDIDATE, candidate_raw)
    current["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    current["historicalSourceArchiveBinding"] = bind(ARCHIVE.relative_to(ROOT).as_posix(), archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed),
                                       "changedSinceCandidate": changed,
                                       "sourceContentsFromGitCommit": commit,
                                       "allSourceBindingsRefreshed": True}
    current["countsUnchanged"] = {"reviewed": 795, "pending": 53}
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_795_REVIEWED_53_PENDING_AUTHORITY"
    current["id"] = "RANK9-IMPACT-EXILE4-CURRENT-SOURCE-CONTEXT-203"
    current["recordedAtUtc"] = now
    for record in current["records"]:
        sid = record["spellId"]
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
    current_raw = json_bytes(current)

    current_paths = [INDEX, CATALOG, QUEUE.relative_to(ROOT).as_posix(), PENDING.relative_to(ROOT).as_posix(),
                     HANDOFF.relative_to(ROOT).as_posix(), "START_HERE.md"]
    current_paths += [
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/PROCEDURES.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/SHARED_RULES.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/HOLD_REGISTER.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/REVIEW_RECEIPT.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/CANDIDATE_PACKAGE_MANIFEST.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/STANDALONE_PROCEDURES.md",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202/STANDALONE_PROCEDURES.md",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/damage_control_25_reviewed_10.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/persistent_damage_20_reviewed_07.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PLANARGATES5_EXACT_ACCEPTANCE_200.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PLANARGATES5_APPLICATION_200.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PLANARGATES5_RETURN200_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_EXACT_ACCEPTANCE_196.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_APPLICATION_196.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_EXACT_ACCEPTANCE_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_APPLICATION_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_SUMMONHOSTS5_EXACT_ACCEPTANCE_202.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_SUMMONHOSTS5_APPLICATION_202.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_SUMMONHOSTS5_RETURN202_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_SUMMONHOSTS5_RETURN202_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT53_PENDING_IDENTITY_AUDIT_202.json",
    ]
    current_files = {"current/" + path: git_blob(commit, path) for path in current_paths}

    notes = copy.deepcopy(old_notes)
    notes.update({"id": "RANK9IMPACTEXILE4-INDEPENDENT-CONFERENCE-203",
                  "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_NOT_ACCEPTED",
                  "recordedAtUtc": now, "sourceCommit": commit, "sourceBranch": branch,
                  "currentAppliedCounts": {"reviewed": 795, "pending": 53, "acceptedUnapplied": 0,
                                           "completeStandaloneProcedures": 519},
                  "sourceChecks": [{"path": row["path"], "historicalExact": True,
                                    "currentCommit": commit, "currentSha256": row["sha256"]}
                                   for row in refreshed],
                  "scope": "Preparation only. Preserve accepted interfaces and exact carried blockers. No new rule adopted. No supplied program execution or runtime, implementation, human-play, balance, cosmology, domain-closure or release claim."})
    notes_raw = json_bytes(notes)
    carried = {key: pending.get(key, {}) for key in pending if key.startswith("retainedReturn")}
    current_context = {
        "id": "RANK9-IMPACT-EXILE4-CURRENT-DIRECTOR-CONTEXT-203",
        "recordedAtUtc": now, "sourceCommit": commit, "sourceBranch": branch,
        "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": len(IDS)},
        "currentIndexCounts": index["authoredCounts"], "currentPendingAudit": pending["id"],
        "historicalQueueCandidateBinding": target["candidate"],
        "historicalCandidateBinding": bind(CANDIDATE, candidate_raw),
        "historicalSourceArchiveBinding": bind(ARCHIVE.relative_to(ROOT).as_posix(), archive_raw),
        "sourceRefresh": {"sourceFileCount": len(refreshed), "changedSinceCandidate": changed},
        "latestAcceptedOrdinarySpellBatch": {
            "application": "RANK9-SUMMONHOSTS5-APPLICATION-202",
            "acceptedIds": ["conjure-magmatic-wyrm", "planar-army"],
            "unacceptedIds": ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"],
            "retainedBlockers": {"summon-elemental-avatar": ["SH202-B01"],
                                 "summon-herald-of-the-planes": ["SH202-B02"],
                                 "summon-avatar-of-decay": ["SH202-B03"]},
            "countsAfter": AUTHORITY,
            "model": "current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202/MODEL.json",
            "independentAudit": "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_SUMMONHOSTS5_RETURN202_INDEPENDENT_AUDIT.json",
            "scope": "Preserve Wyrm and Army exact accepted static procedures; the three listed source blockers remain pending and are outside this review.",
        },
        "acceptedTransport6Context": {
            "model": "current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/MODEL.json",
            "scope": "Use exact accepted transit and terminal-settlement predicates. Planar Collapse has no automatic destination, return privilege, or global teleportation exception.",
        },
        "acceptedDamageAndBodyContexts": [
            "DescentReviewChanges/ReviewBible/data/public/spell_candidates/damage_control_25_reviewed_10.json",
            "DescentReviewChanges/ReviewBible/data/public/spell_candidates/persistent_damage_20_reviewed_07.json",
            "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/MODEL.json",
        ],
        "retainedNamedBlockersOutsideScope": carried,
        "qualification": "Preparation only. Refresh all source bindings from the exact pushed commit. Preserve native spell cards and access, accepted interfaces, source-qualified defenses, and all exact blockers. No canonical spell, class, damage, condition, transport or cosmology rule is adopted by this packet.",
    }

    files = {
        "CURRENT_CONTEXT_203.json": json_bytes(current_context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_203.json": current_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": archive_raw,
        "HISTORICAL_NOTES/RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_203.txt": b"", **current_files, **current_sources,
    }
    request = (
        "GPT director — review exactly the four current pending Rank9 Impact/Exile4 identities in this packet.\n\n"
        f"Source branch and commit: {branch} / {commit}. Current authority: 795 reviewed-applied / 53 pending / 0 accepted-unapplied; 519 complete standalone procedures; 173 scoped interfaces.\n\n"
        f"Scope only: {', '.join(IDS)}. Use the refreshed 149-source bindings, exact 795/53 queue, handoff, pending audit, index, catalog, and attached historical source conference. Preserve all 26 original questions, both focused addenda, all 8 required new cases, and all 7 future-case requirements. Do not reopen completed feat identities, prior completed spell cohorts, or other pending identities.\n\n"
        "For Eternal Anvil, provide a full-use lawful 5d12 force manifestation with the printed one-round Stunned endpoint, genuine actor opportunity and independently defended failure. For Reverse Gravity Field, show several actual bodies and objects lifting the full unobstructed 60 feet with real support, cargo and swept geometry; resolve obstruction, field end, falling, markers and ordinary 60-foot 3d6 landing damage. For Transmute Flesh to Energy, separate flesh eligibility, the chosen full 12d10 type and printed resistance bypass from immunity, prevention, temporary HP, death, Null, surviving body and gear; do not invent fuel or double damage. For Planar Collapse, bind exact current force, Prone and exile scope, real eligible recipients, destination/cell/cargo/agency/clocks, blocked or defended rider branches, and lawful occupied/warded endpoint settlement without a generic Transport6 extension.\n\n"
        "Every positive case must use a complete actual level-17 caster and acquired lawful class repertoire, real 26 RP plus actual modifiers, current action/reaction/ready and concentration history, source-qualified target/body/save values, real geometry and committed resources. Resolve defenses per recipient and numbered round; distinguish immunity, resistance bypass, ward, prevention, zero damage, condition admission, movement and terminal transport. Preserve current damage sharing, body/gear, control, Fall, Transport6 and cosmology scopes. A proposed context or complete worked record is not canonical authority.\n\n"
        "Keep the current accepted state exactly: Return202 accepts only Conjure Magmatic Wyrm and Planar Army; retain SH202-B01/B02/B03 and inherited holds unchanged. Preserve all earlier applied cohorts and blockers. Return one complete source-faithful static procedure per identity, exact class access and source bindings, original question dispositions, all required positive/adverse cases, future-obligation dispositions, reversible state/event operations and an exact package manifest. Mark only individually passing identities accepted=true and applied=false; name evidence-specific blockers for every held identity. No runtime, canonical card/rule, implementation, human-play, balance, cosmology, domain closure, completion or release approval. The exact accepted IDs will be independently audited, applied and pushed before the next group proceeds."
    )
    files["REQUEST_203.txt"] = request.encode("utf-8")
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)
    OUT.mkdir(parents=True, exist_ok=False)
    current_candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_203.json"
    current_candidate_path.write_bytes(current_raw)
    archive_path = OUT / "DD_Rank9_ImpactExile4_CurrentSource_203.zip"
    member_rows = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        for name in sorted(files):
            raw = files[name]
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            member_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw),
                                "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {"id": "RANK9-IMPACT-EXILE4-CURRENT-SOURCE-PACKET-MANIFEST-203",
                    "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                    "group": GROUP, "pendingIds": IDS,
                    "memberCountExcludingSelf": len(member_rows), "members": member_rows}
        packet.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    checks = []
    packet_members_verified = True
    with zipfile.ZipFile(archive_path) as packet:
        names = packet.namelist()
        add(checks, "ZIP manifest, uniqueness and CRC are valid",
            packet.testzip() is None and len(names) == len(member_rows) + 1 and len(names) == len(set(names)),
            {"members": len(names), "manifestRows": len(member_rows)})
        for row in member_rows:
            h, crc, size = hashlib.sha256(), 0, 0
            with packet.open(row["path"]) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(chunk); h.update(chunk); crc = zlib.crc32(chunk, crc)
            valid = size == row["bytes"] and h.hexdigest() == row["sha256"] and f"{crc & 0xffffffff:08x}" == row["crc32"]
            packet_members_verified &= valid
        add(checks, "Every packet member matches exact manifest size, SHA-256 and CRC",
            packet_members_verified and len(member_rows) == len(files), {"verified": len(member_rows)})
    packet_raw = archive_path.read_bytes()
    packet_rel = archive_path.relative_to(ROOT).as_posix()
    packet_binding = bind(packet_rel, packet_raw)
    candidate_binding = bind((OUT / current_candidate_path.name).relative_to(ROOT).as_posix(), current_raw)
    delivery = {"id": "RANK9-IMPACT-EXILE4-CURRENT-SOURCE-DELIVERY-203",
                "status": "PREPARED_UNSENT", "archive": packet_binding,
                "members": len(member_rows) + 1, "manifestBindings": len(member_rows),
                "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
                "historicalCandidate": bind(CANDIDATE, candidate_raw),
                "historicalSourceArchive": bind(ARCHIVE.relative_to(ROOT).as_posix(), archive_raw),
                "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceHistoricalCandidate": changed,
                "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_ImpactExile4_CurrentSource_203_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)
    prep = {"id": "RANK9-IMPACT-EXILE4-SOURCE-PREPARATION-203", "recordedAtUtc": now,
            "status": "PASS", "sourceCommit": commit, "sourceBranch": branch,
            "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": IDS,
            "currentCandidate": candidate_binding, "historicalCandidate": bind(CANDIDATE, candidate_raw),
            "historicalArchive": bind(ARCHIVE.relative_to(ROOT).as_posix(), archive_raw),
            "packet": packet_binding, "deliveryManifest": delivery_binding,
            "refreshedBindings": len(refreshed), "changedHistoricalBindings": changed,
            "questions": {"original": 26, "addenda": 2, "total": 28},
            "requiredMainCases": 8, "futureCaseRequirements": 7,
            "canonicalChanges": False, "accepted": False, "applied": False}
    prep_path = AUDIT / "RANK9IMPACTEXILE4_SOURCE_PREPARATION_203.json"
    prep_raw = json_bytes(prep); prep_path.write_bytes(prep_raw)
    packet_record = {"id": "RANK9IMPACTEXILE4-PACKET-203", "status": "PREPARED_UNSENT",
                     "group": GROUP, "pendingIds": IDS, "sourceAuthority": AUTHORITY,
                     "sourceCommit": commit, "archive": packet_binding,
                     "deliveryManifest": delivery_binding, "candidate": candidate_binding,
                     "questions": 28, "requiredMainCases": 8, "futureCaseRequirements": 7,
                     "refreshedSourceBindings": len(refreshed), "canonicalChanges": False}
    packet_path = AUDIT / "RANK9IMPACTEXILE4_PACKET_203.json"
    packet_record_raw = json_bytes(packet_record); packet_path.write_bytes(packet_record_raw)

    pending_audit = {key: copy.deepcopy(value) for key, value in pending.items() if key.startswith("retainedReturn")}
    pending_audit.update({"id": "CURRENT53-PENDING-IDENTITY-AUDIT-203", "recordedAtUtc": now,
                          "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
                          "indexBinding": bind(INDEX, git_blob(commit, INDEX)),
                          "catalogBinding": bind(CATALOG, git_blob(commit, CATALOG)),
                          "authoredCounts": index["authoredCounts"], "pendingCount": 53,
                          "pendingIds": pending["pendingIds"],
                          "allPendingExistInSourceCatalog": set(pending["pendingIds"]) <= set(catalog_rows),
                          "acceptedUnapplied": 0, "closed335AndCompletedCohortsReopened": False,
                          "currentAuthority": AUTHORITY})
    PENDING_OUT.write_bytes(json_bytes(pending_audit))
    packet_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS),
                      "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                      "freshPacketRequiredForCurrentAuthority": False,
                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                      "packetRecord": bind(packet_path.relative_to(ROOT).as_posix(), packet_record_raw),
                      "sourcePreparation": bind(prep_path.relative_to(ROOT).as_posix(), prep_raw)}
    q1 = copy.deepcopy(queue)
    q1.update({"id": "SPELL-REVIEW-QUEUE-203", "recordedAtUtc": now,
               "nextGroup": GROUP, "next": packet_request, "nextPreparedRequest": packet_request,
               "packetStatus": "RANK9_IMPACT_EXILE4_PACKET_203_PREPARED_UNSENT_795_53",
               "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
               "currentPreparation": bind(prep_path.relative_to(ROOT).as_posix(), prep_raw),
               "pendingIdentityAudit": {"path": PENDING_OUT.relative_to(ROOT).as_posix(),
                                        "pending": 53, "sha256": sha(PENDING_OUT.read_bytes())}})
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        q1.pop(key, None)
    q1.update({"currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
               "currentPreparation": bind(prep_path.relative_to(ROOT).as_posix(), prep_raw)})
    groups = []
    for old_group in q1["currentPendingGroups"]:
        if old_group["group"] == GROUP:
            old_group = copy.deepcopy(old_group)
            old_group.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_795_53",
                              "freshPacketRequiredForCurrentAuthority": False,
                              "preparedPacket": packet_binding, "preparedDelivery": delivery_binding})
        groups.append(old_group)
    q1["currentPendingGroups"] = groups
    QUEUE_OUT.write_bytes(json_bytes(q1))
    h1 = copy.deepcopy(handoff)
    h1.update({"id": "CURRENT-HANDOFF-203", "recordedAtUtc": now,
               "status": "RANK9_IMPACT_EXILE4_PACKET_203_PREPARED_UNSENT_795_53",
               "currentAuthority": AUTHORITY,
               "currentIndexBinding": bind(INDEX, git_blob(commit, INDEX)),
               "currentCatalogBinding": bind(CATALOG, git_blob(commit, CATALOG)),
               "pendingIdentityAudit": {"id": pending_audit["id"],
                                        "path": PENDING_OUT.relative_to(ROOT).as_posix(),
                                        "pendingCount": 53, "sha256": sha(PENDING_OUT.read_bytes())},
               "nextGroup": GROUP, "nextPreparedRequest": packet_request,
               "currentQueueBinding": bind(QUEUE_OUT.relative_to(ROOT).as_posix(), (AUDIT / QUEUE_OUT.name).read_bytes()),
               "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
               "sourcePreparation": bind(prep_path.relative_to(ROOT).as_posix(), prep_raw),
               "resumePriority": "Submit the fresh Rank9 Impact/Exile4 packet 203 to the GPT director; independently audit its return, apply and push only exact accepted IDs, and continue until pending is zero."})
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        h1.pop(key, None)
    h1.update({"currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
               "sourcePreparation": bind(prep_path.relative_to(ROOT).as_posix(), prep_raw)})
    HANDOFF_OUT.write_bytes(json_bytes(h1))
    SNAPSHOT.write_text(
        "# Current ordinary spell-review checkpoint 203\n\n"
        "Return202 applied exactly Conjure Magmatic Wyrm and Planar Army; Summon Elemental Avatar, Summon Herald of the Planes, and Summon Avatar of Decay remain held under SH202-B01/B02/B03. Authority is **795 reviewed / 53 pending / 0 accepted-unapplied**, with 519 complete standalone procedures. The fresh Rank9 Impact/Exile4 packet is prepared for the GPT director at this authority.\n",
        encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    prior_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(
        f"**Current ordinary spell-review handoff [203](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_203.json):** Authority is **795 reviewed / 53 pending / 0 accepted-unapplied**. The fresh Rank9 Impact/Exile4 packet is prepared for the GPT director. Summon Elemental Avatar, Summon Herald of the Planes and Summon Avatar of Decay remain pending under SH202-B01/B02/B03.\n\n" + prior_start,
        encoding="utf-8", newline="\n")

    checks = [
        ("Preparation binds the pushed HEAD and exact 795/53/0 authority", commit == remote_row[0] and q1["currentAuthority"] == AUTHORITY and h1["currentAuthority"] == AUTHORITY),
        ("Exactly four current pending Impact/Exile4 identities are next in queue order", target["pendingIds"] == IDS and set(IDS) <= pending_ids and pending_audit["pendingCount"] == 53),
        ("All 149 historical source members match their archived hashes", len(historical_members) == len(refreshed) == 149),
        ("All source bindings are refreshed from the exact current Git commit", current["currentSourceCommit"] == commit and current["currentAuthority"] == AUTHORITY and current["sourceBindingRefresh"]["allSourceBindingsRefreshed"]),
        ("All four native entries, access routes and catalog pointers remain pending and exact", all(entries[s]["authoredStatus"] == "pending-authored-procedure" and entries[s]["sourceStatus"] == "blocked-pending-operational-review" for s in IDS)),
        ("Return202 accepted procedures, blockers, and relevant accepted mechanics are included", all("current/" + path in current_files for path in current_paths if path.endswith("MODEL.json") or "REVIEWED_202" in path)),
        ("All 26 original questions, two addenda, eight cases and seven future requirements are retained", len(notes["completeOriginalQuestionsUnchanged"]) == 26 and len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["requiredNewCases"]) == 8 and len(notes["originalFutureCaseRequirementsUnchanged"]) == 7),
        ("All packet members match the manifest size, SHA and CRC", packet_members_verified and len(member_rows) + 1 == delivery["members"] and packet_binding["bytes"] == len(packet_raw) and packet_binding["sha256"] == sha(packet_raw)),
    ]
    failed = [name for name, passed in checks if not passed]
    verification = {"id": "RANK9-IMPACT-EXILE4-PACKET203-INDEPENDENT-VERIFICATION",
                    "recordedAtUtc": now, "status": "PASS" if not failed else "FAIL",
                    "checksPassed": len(checks) - len(failed), "checksFailed": len(failed),
                    "checks": [{"check": name, "passed": passed} for name, passed in checks],
                    "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                    "packet": packet_binding, "delivery": delivery_binding,
                    "accepted": False, "applied": False}
    verify_path = AUDIT / "RANK9IMPACTEXILE4_PACKET203_INDEPENDENT_VERIFICATION.json"
    verify_path.write_bytes(json_bytes(verification))
    assert not failed, failed
    q1["currentPacketAudit"] = bind(verify_path.relative_to(ROOT).as_posix(), verify_path.read_bytes())
    QUEUE_OUT.write_bytes(json_bytes(q1))
    h1["currentPacketAudit"] = q1["currentPacketAudit"]
    h1["currentQueueBinding"] = bind(QUEUE_OUT.relative_to(ROOT).as_posix(), QUEUE_OUT.read_bytes())
    HANDOFF_OUT.write_bytes(json_bytes(h1))
    print(json.dumps({"status": verification["status"], "checksPassed": verification["checksPassed"],
                      "checksFailed": verification["checksFailed"], "packet": packet_binding,
                      "delivery": delivery_binding, "changedSourceBindings": len(changed),
                      "changedPaths": [item["path"] for item in changed],
                      "questionCount": 28, "requiredCases": 8, "futureRequirements": 7}, indent=2))


if __name__ == "__main__":
    main()
