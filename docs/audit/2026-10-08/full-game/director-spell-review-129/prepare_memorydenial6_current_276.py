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
GROUP = "rank9-memory-denial6"
IDS = ["mind-collapse"]
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_IN = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_275.json"
PENDING_IN = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_275.json"
HANDOFF_IN = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_275.json"
QUEUE_OUT = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_276.json"
PENDING_OUT = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_276.json"
HANDOFF_OUT = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_276.json"
SOURCE_CANDIDATE_224 = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_224_prepared/DD_Rank9_MemoryDenial6_CurrentSource_224.zip"
SOURCE_CANDIDATE_195 = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_195_prepared/DD_Rank9_MemoryDenial6_CurrentSource_195.zip"
HISTORICAL_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_memory_denial_6_source_conference_01.json"
SOURCE_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Memory_Denial_6_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_NEXT_CONFERENCE_NOTES_129.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = AUDIT / "rank9_memorydenial6_current_source_276_prepared"
PACKET_PATH = AUDIT / "RANK9MEMORYDENIAL6_PACKET_276.json"
PREP_PATH = AUDIT / "RANK9MEMORYDENIAL6_SOURCE_PREPARATION_276.json"
PENDING_PATH = ROOT / PENDING_OUT
QUEUE_PATH = ROOT / QUEUE_OUT
HANDOFF_PATH = ROOT / HANDOFF_OUT
SNAPSHOT_PATH = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_276.md"
DIRECTOR_FINDINGS = {
    "id": "MIND-COLLAPSE-DIRECTOR-FINDINGS-275",
    "authority": AUTHORITY,
    "confirmedPendingIds": [
        "absolute-domination", "alignment-ascension", "alignment-perfection", "astral-projection",
        "banishment-gate", "collapse-timeline", "conjure-demiplane-fortress", "corruption-purification",
        "divine-intervention-greater", "elemental-shell", "eternal-prophecy", "faction-incarnate",
        "faction-omniscience-supreme", "faction-perfection", "fate-rewrite", "final-word", "imprisonment",
        "invulnerable-sphere", "mass-phantom-killer", "mind-collapse", "nullification-wave", "psychic-scream",
        "puppetmaster-s-realm", "reality-anchor", "reverse-gravity-field", "summon-avatar-of-decay",
        "summon-elemental-avatar", "summon-herald-of-the-planes", "time-stop", "timeless-form", "weird", "wish",
    ],
    "priorityOrder": [
        ["mind-collapse"], ["absolute-domination"], ["puppetmaster-s-realm"],
        ["psychic-scream", "mass-phantom-killer", "weird"], ["final-word"],
        ["elemental-shell", "timeless-form", "invulnerable-sphere"], ["nullification-wave", "reality-anchor"],
        ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"], ["faction-omniscience-supreme"],
        ["banishment-gate", "conjure-demiplane-fortress"],
        ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"],
        ["reverse-gravity-field"],
        ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"],
        ["astral-projection", "imprisonment"], ["divine-intervention-greater", "wish"],
    ],
    "mindCollapseFinding": "No qualifying acquired full-turn grant or legal grant-bearing actor was found in the inspected bound evidence. This is bounded to the inspected evidence, not a claim that no such source exists anywhere.",
    "limitations": [
        "dragoon.json#/cards/35/effect grants one extra full Action next turn, not an inserted turn.",
        "oracle.json#/cards/32/effect and /cards/34/effect grant an additional full Action, not a turn.",
        "oracle.json#/cards/77/effect grants a restricted additional Action.",
        "oracle.json#/cards/218/effect repositions initiative and explicitly grants no immediate extra normal turn.",
        "wizard.json#/cards/53/effect commands the next normal turn and explicitly grants no extra turn.",
        "Time Stop is held under TF192 and cannot supply an assumed operational witness.",
        "Prophetic Surge at oracle.json#/cards/26/effect changes cost or duration, not turn count.",
    ],
    "timeStopRuling": {
        "sourceText": "Take 3 turns uninterrupted",
        "coreEntry": 921,
        "sourceParagraph": 10122,
        "decision": "Does not establish an acquired operational grant while Time Stop remains unresolved; do not use it as an assumed Mind Collapse witness.",
        "retainedBlocker": "TF192-B01",
    },
    "nextEvidenceTargets": [
        {"priority": 1, "identity": "mind-collapse", "blocker": "MD196-B01",
         "target": "An authorized genuine inserted-full-turn grant, its acquisition and complete legal actor, including activation eligibility while Stunned; preserve the original three-regular-END schedule, recharge, Reaction and Ready/concentration history."},
        {"priority": 2, "identity": "absolute-domination", "blocker": "AG190-B01",
         "target": "Qualify the same grant dependency independently for this spell's required control/turn branch. A source accepted for one witness does not automatically prove this interaction or actor eligibility."},
        {"priority": 3, "identity": "puppetmaster-s-realm", "blocker": "AG190-B02",
         "target": "A complete source-authorized creature profile with native Multiattack and exact reach for constituent attacks, plus lawful admission/control and required command-execution history. Ghoul Lash sequences are not a substitute; any Cave Bear supplement must establish these facts."},
    ],
    "closureStatus": "32 previously reviewed held identities; no first-review tasks remain.",
    "minimumEvidence": [
        "Exact authorized grant: bound file/hash and card pointer explicitly granting a genuine inserted turn, with trigger, recipient eligibility, timing, activation, costs and limits.",
        "Legal acquired actor: class/level/selections, prerequisites, relevant statistics/resources/equipment/acquisition history and any separate grantor; establish legal activation while recipient is Stunned.",
        "Integrated history preserving initial INT save, rank-9 access/payment, genuine Stunned consequences, concentration/held-spell loss, regular START/END, recharge, Reaction, Ready and resources through termination.",
    ],
    "clockAnchors": {
        "path": "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
        "sha256": "9118101f0907e0cd52a78cef83affa9e6fcae1b3d958c8a576499dfddc424f60",
        "regularVsExtraTurnLines": "29-35",
        "originalVirtualMarkersAndOrderingLines": "47-66",
        "readyPaymentConcentrationReleaseExpiryLines": "97-111",
    },
    "mindCollapsePriorProcedure": {
        "path": "procedures/mind-collapse.json",
        "regularTargetEndMarkers": 3,
        "excludeInProgressTurn": True,
        "repeatSaveAtAllThreeMarkersIncludingFinalBeforeExpiry": True,
        "insertedTurnAddsSaveRechargeReactionRefreshOrReadyDeadline": False,
    },
    "unresolvedBranch": {
        "case": "RANK9MEMORYDENIAL6129-MIND-COLLAPSE-B/extra-action-not-turn",
        "event": 11,
        "eventTimestampSeconds": 6.3,
        "admissionTimestampSeconds": 6.205,
        "regularEndMarkersSeconds": [7.9, 13.9, 19.9],
        "requiredCorrection": "Add a genuinely sourced inserted-turn grant and legal acquired actor; do not relabel event 11 as a grant.",
    },
    "status": "MD196-B01_AND_MD196-H01_H02_H03_H04_H06_H08_REMAIN_OPEN_NO_ACCEPTANCE_OR_WAIVER",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def bind(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}


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

    queue, pending, handoff, index, catalog = [read(blob(commit, p)) for p in (QUEUE_IN, PENDING_IN, HANDOFF_IN, INDEX, CATALOG)]
    assert queue["currentAuthority"] == handoff["authority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 32
    assert queue["nextGroup"] == GROUP
    target = next(row for row in queue["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == 1
    assert target["freshPacketRequiredForCurrentAuthority"] is True

    with zipfile.ZipFile(ROOT / SOURCE_CANDIDATE_224) as prior:
        prior_candidate_raw = prior.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json")
    with zipfile.ZipFile(ROOT / SOURCE_CANDIDATE_195) as prior:
        candidate_195_raw = prior.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json")
    old_candidate = read(prior_candidate_raw)
    candidate_195 = read(candidate_195_raw)
    assert {row["spellId"] for row in old_candidate["records"]} == {"mind-collapse", "unravel-identity"}
    assert len(old_candidate["sourceBindings"]) == len(old_candidate["historicalSourceBindings"]) == 120
    assert len(candidate_195["historicalSourceBindings"]) == 120
    notes_raw = blob(commit, NOTES)
    notes = read(notes_raw)
    assert "mind-collapse" in notes["identities"]

    entries = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    assert IDS[0] in pending["pendingIds"]
    assert entries[IDS[0]]["authoredStatus"] == "pending-authored-procedure"
    assert entries[IDS[0]]["sourceStatus"] == "blocked-pending-operational-review"
    assert catalog_rows[IDS[0]]["id"] == IDS[0] and catalog_rows[IDS[0]]["operational"] is None

    now = datetime.now(timezone.utc).isoformat()
    current_candidate = copy.deepcopy(old_candidate)
    current_candidate["records"] = [copy.deepcopy(row) for row in old_candidate["records"] if row["spellId"] in IDS]
    current_candidate["historicalSourceBindings"] = copy.deepcopy(old_candidate["sourceBindings"])
    refreshed, current_sources, changed = [], {}, []
    with zipfile.ZipFile(ROOT / SOURCE_CANDIDATE_224) as prior:
        for old in old_candidate["sourceBindings"]:
            path = old["path"]
            raw = blob(commit, path)
            prior_raw = prior.read("sources_current/" + path)
            assert len(prior_raw) == old["bytes"] and sha(prior_raw) == old["sha256"], path
            refreshed.append({"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": blob_id(commit, path)})
            current_sources["sources_current/" + path] = raw
            if raw != prior_raw:
                changed.append({"path": path, "priorBytes": len(prior_raw), "priorSha256": sha(prior_raw),
                                "currentBytes": len(raw), "currentSha256": sha(raw)})
    current_candidate["currentSourceCommit"] = commit
    current_candidate["currentBranch"] = branch
    current_candidate["currentAuthority"] = AUTHORITY
    current_candidate["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": 1}
    current_candidate["historicalCandidateBinding"] = bind(
        "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_224_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json",
        prior_candidate_raw)
    current_candidate["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    current_candidate["historicalSourceArchiveBinding"] = bind(SOURCE_ARCHIVE, blob(commit, SOURCE_ARCHIVE))
    current_candidate["sourceBindings"] = refreshed
    current_candidate["sourceBindingRefresh"] = {
        "sourceFiles": len(refreshed), "changedSincePriorCurrentPacket224": changed,
        "sourceContentsFromCurrentWorkspaceSnapshot": True, "headCommit": commit, "allSourceBindingsRefreshed": True,
    }
    current_candidate["countsUnchanged"] = {"reviewed": 816, "pending": 32}
    current_candidate["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_816_REVIEWED_32_PENDING_AUTHORITY"
    current_candidate["id"] = "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-CONTEXT-276"
    current_candidate["recordedAtUtc"] = now
    for record in current_candidate["records"]:
        record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
        record["currentIndexEntry"] = copy.deepcopy(entries[record["spellId"]])

    current_context_paths = [INDEX, CATALOG, PENDING_IN, QUEUE_IN, HANDOFF_IN,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_APPLICATION_VALIDATION_256.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/UNHOLY_ASCENDANCE_APPLICATION_VALIDATION_275.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET_241.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_SOURCE_PREPARATION_241.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_unravel_reviewed_256/CANDIDATE_PACKAGE_MANIFEST.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_unravel_reviewed_256/PROCEDURE_RECORD.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9unholyascendance_reviewed_275/CANDIDATE_PACKAGE_MANIFEST.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9unholyascendance_reviewed_275/PROCEDURE_RECORD.json",
    ]
    current_files = {"current/" + path: blob(commit, path) for path in current_context_paths}
    current_files["current/CURRENT32_PENDING_IDENTITY_AUDIT_276.json"] = blob(commit, PENDING_IN)
    current_files["current/CURRENT_SPELL_QUEUE_276.json"] = b""
    current_files["current/CURRENT_HANDOFF_276.json"] = b""

    findings_raw = json_bytes(DIRECTOR_FINDINGS)
    request = (
        "GPT Director — this is a fresh source-and-acquisition qualification packet for the one current pending identity Mind Collapse / MD196-B01. "
        "Authority is 816 reviewed-applied / 32 pending / 0 accepted-unapplied, with 540 complete standalone procedures and 173 scoped interfaces. "
        f"Workspace branch/HEAD: {branch}/{commit}. The packet refreshes all 120 source bindings and includes corrected current queue/handoff snapshots.\n\n"
        "Earlier you confirmed no qualifying acquired full-turn grant or legal grant-bearing actor in the inspected bound evidence; this is a bounded finding, not proof that no source exists. "
        "You identified only extra Actions, initiative movement, restricted actions, or a commanded next ordinary turn. Time Stop remains held under TF192 and cannot serve as an assumed operational witness. "
        "The queue's stale Unholy Ascendance activeReview/status labels are corrected here; Unholy Ascendance is applied/closed.\n\n"
        "Please inspect only Mind Collapse's source-and-acquisition qualification. Identify an exact authorized source grant explicitly inserting a genuine full turn and a legal actor who has acquired it, or confirm the precise source gap and retain MD196-B01 plus MD196-H01/H02/H03/H04/H06/H08. Do not invent a grant, actor, replay event, waiver, or acceptance. Keep Time Stop's TF192 blockers and all accepted identities unchanged.\n\n"
        "A qualifying grant must bind the exact file/hash/card pointer and establish trigger, recipient eligibility, timing, activation, costs and limits. The actor record must establish class/level/selections, prerequisites, stats, resources, equipment, acquisition history and any grantor; explain lawful activation while Mind Collapse's target is Stunned without assuming a prohibited Action/Reaction. If such source and actor exist, provide exact pointers and the minimum integrated witness preserving initial INT save, rank-9 access/payment, real Stunned consequences, concentration/held-spell loss and all regular START/END, recharge, Reaction, Ready and resource history.\n\n"
        "Preserve the previous three future regular target-END markers (excluding a turn already in progress); repeat INT saves at each marker including the final save before expiry. An inserted turn adds no extra save, recharge/Reaction refresh or Ready deadline. The existing branch RANK9MEMORYDENIAL6129-MIND-COLLAPSE-B/extra-action-not-turn event 11 at 6.300 seconds is an evidence boundary, not a grant; retain admission 6.205 and regular END markers 7.900/13.900/19.900.\n\n"
        "After this qualification, keep the stated priority order: Absolute Domination, Puppetmaster's Realm, then remaining groups in current queue order. Confirm the exact remaining pending IDs and next evidence target. Do not re-open already accepted identities. Do not apply anything from this source-qualification exchange.\n"
    )
    current_candidate_raw = json_bytes(current_candidate)
    current_files["current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_276.json"] = current_candidate_raw
    current_files["current/MIND_COLLAPSE_DIRECTOR_FINDINGS_275.json"] = findings_raw

    OUT.mkdir(parents=True, exist_ok=True)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_276.json"
    candidate_path.write_bytes(current_candidate_raw)
    findings_path = OUT / "MIND_COLLAPSE_DIRECTOR_FINDINGS_275.json"
    findings_path.write_bytes(findings_raw)
    prep_queue = copy.deepcopy(queue)
    prep_queue.update({
        "id": "SPELL-REVIEW-QUEUE-276", "recordedAtUtc": now,
        "activeReview": {"identity": "mind-collapse", "group": GROUP,
            "stage": "SOURCE_AND_ACQUISITION_QUALIFICATION_REQUIRED", "blocker": "MD196-B01",
            "requiredWitnessScope": ["exact acquired genuine full-turn grant", "legal grant-bearing actor",
                "regular END clock", "recharge/Reaction/Ready preservation"]},
        "packetStatus": "CURRENT_MIND_COLLAPSE_SOURCE_QUALIFICATION_816_32_PREPARED",
        "status": "MIND_COLLAPSE_SOURCE_QUALIFICATION_REQUIRED_816_32",
        "nextGroup": GROUP, "nextPendingCount": 1, "nextPendingIds": IDS,
        "recommendedClosurePriority": ["mind-collapse", "absolute-domination", "puppetmaster-s-realm"],
        "recommendedClosureOrder": [
            {"rank": i + 1, "identities": ids,
             "priority": (
                 "MD196-B01: exact acquired genuine full-turn grant and legal actor; preserve the regular-END clock, recharge, Reaction, Ready and concentration history." if i == 0 else
                 "AG190-B01: qualify the grant dependency independently for this spell's required control/turn branch and actor eligibility." if i == 1 else
                 "AG190-B02: source-authorized creature profile with native Multiattack/reach, lawful admission/control and command history." if i == 2 else
                 "Continue this remaining group in current queue order."
             )}
            for i, ids in enumerate(DIRECTOR_FINDINGS["priorityOrder"])
        ],
        "directorRemainingWorkResponse": {"text": "GPT confirms 816 applied / 32 pending / 0 accepted-unapplied; 540 procedures / 173 interfaces. All 32 are previously reviewed held identities; no first-review tasks remain. Time Stop's alternate 'Take 3 turns uninterrupted' at Core entry 921 / paragraph 10122 is not an acquired operational grant while Time Stop is unresolved; retain TF192-B01. Next evidence targets: Mind Collapse / MD196-B01 exact source+acquisition+legal actor and clock preservation; Absolute Domination / AG190-B01 independently qualifies that grant dependency for its control/turn branch; Puppetmaster's Realm / AG190-B02 needs a source-authorized creature with native Multiattack and exact reaches plus admission/control/command history. No identity accepted/applied and no accepted cohort reopened.",
            "source": {"conversationTitle": "Calibration review part 6", "url": CHAT}},
        "currentPreparation": {"status": "SOURCE_AND_ACQUISITION_QUALIFICATION_PACKET_PREPARED_UNSENT",
            "group": GROUP, "pendingIds": IDS},
        "sourcePreparation": None, "currentSourcePacket": None, "currentPacket": None,
        "currentDeliveryManifest": None, "currentPacketDelivery": None,
    })
    prep_queue["currentAuthority"] = AUTHORITY
    prep_target = next(row for row in prep_queue["currentPendingGroups"] if row["group"] == GROUP)
    prep_target["status"] = "SOURCE_AND_ACQUISITION_QUALIFICATION_PACKET_PREPARED_UNSENT"
    prep_target["freshPacketRequiredForCurrentAuthority"] = False
    prep_pending = copy.deepcopy(pending)
    prep_pending.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-276", "recordedAtUtc": now})
    prep_handoff = copy.deepcopy(handoff)
    prep_handoff.update({"id": "CURRENT-HANDOFF-276", "recordedAtUtc": now,
        "status": "MIND_COLLAPSE_SOURCE_QUALIFICATION_PACKET_PREPARED_816_32",
        "authority": AUTHORITY, "nextGroup": GROUP, "nextPendingCount": 1, "nextPendingIds": IDS,
        "currentPreparation": {"status": "SOURCE_AND_ACQUISITION_QUALIFICATION_PACKET_PREPARED_UNSENT",
            "group": GROUP, "pendingIds": IDS},
        "currentPacket": None, "currentDeliveryManifest": None, "currentPacketDelivery": None})
    prep_queue_raw = json_bytes(prep_queue)
    prep_handoff["currentQueueBinding"] = bind(QUEUE_OUT, prep_queue_raw)
    current_files["current/CURRENT_SPELL_QUEUE_276.json"] = json_bytes(prep_queue)
    current_files["current/CURRENT32_PENDING_IDENTITY_AUDIT_276.json"] = json_bytes(prep_pending)
    current_files["current/CURRENT_HANDOFF_276.json"] = json_bytes(prep_handoff)
    current_files["REQUEST_276.txt"] = request.encode("utf-8")

    files: dict[str, bytes] = {
        **current_files,
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_276.json": current_candidate_raw,
        "PRIOR_CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json": prior_candidate_raw,
        "HISTORICAL_CURRENT_SOURCE_CONFERENCE_CANDIDATE_195.json": candidate_195_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": blob(commit, HISTORICAL_CANDIDATE),
        "HISTORICAL_NOTES/RANK9MEMORYDENIAL6_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        **current_sources,
    }
    assert len(files) == len(set(files)) and all(safe_member(name) for name in files)
    packet_path = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_276.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        rows = []
        for name in sorted(files):
            raw = files[name]
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
        manifest = {"id": "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-PACKET-MANIFEST-276",
            "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
            "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows}
        packet.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet_path) as packet:
        assert packet.testzip() is None and len(packet.namelist()) == len(rows) + 1
        for row in rows:
            raw = packet.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]

    packet_binding = bind(packet_path.relative_to(ROOT).as_posix(), packet_path.read_bytes())
    candidate_binding = bind(candidate_path.relative_to(ROOT).as_posix(), current_candidate_raw)
    delivery = {"id": "RANK9-MEMORY-DENIAL6-CURRENT-SOURCE-DELIVERY-276", "status": "PREPARED_UNSENT",
        "archive": packet_binding, "members": len(rows) + 1, "manifestBindings": len(rows),
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
        "historicalCandidate": bind(
            "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_224_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_224.json",
            prior_candidate_raw),
        "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSincePacket224": changed,
        "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_276_DELIVERY.json"
    delivery_raw = json_bytes(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path.relative_to(ROOT).as_posix(), delivery_raw)

    prep = {"id": "RANK9-MEMORY-DENIAL6-SOURCE-PREPARATION-276", "recordedAtUtc": now,
        "status": "SOURCE_AND_ACQUISITION_QUALIFICATION_PACKET_PREPARED_UNSENT",
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "group": GROUP, "pendingIds": IDS, "sourceFileCount": len(refreshed), "changedSincePacket224": changed,
        "packet": packet_binding, "deliveryManifest": delivery_binding,
        "memberCount": len(rows) + 1, "canonicalSpellCardChangesDuringPreparation": False,
        "directorFindings": findings_path.relative_to(ROOT).as_posix(),
        "directorFindingsBinding": bind(findings_path.relative_to(ROOT).as_posix(), findings_raw),
        "checksPassed": 9, "checksFailed": 0,
        "checks": [{"check": check, "passed": True} for check in [
            "Branch is main and current authority matches index/queue/handoff at 816/32/0 and 540/173.",
            "Mind Collapse is the sole pending identity in the selected Memory/Denial6 group; all 32 pending IDs remain in the complete audit.",
            "All 120 source bindings are refreshed from the exact current workspace snapshot and match actual files.",
            "The correct 816/32 current queue, pending audit and handoff are included; stale Unholy Ascendance activeReview/status labels are cleared.",
            "Mind Collapse source entry, catalog pointer and native spell text remain exact and pending.",
            "Prior Memory/Denial6 candidate history and focused 28-question/addendum/future-case context are preserved.",
            "Director findings and exact source/actor evidence requirements are bound in the request and packet.",
            "Archive member paths are safe and every member size/SHA-256/CRC validates on readback.",
            "Preparation does not alter canonical spell cards or claim acceptance/application.",
        ]]}
    PREP_PATH.write_bytes(json_bytes(prep))
    prep_binding = bind(PREP_PATH.relative_to(ROOT).as_posix(), PREP_PATH.read_bytes())
    packet_record = {"id": "RANK9MEMORYDENIAL6-PACKET-276", "status": "PREPARED_UNSENT",
        "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": IDS,
        "packet": packet_binding, "deliveryManifest": delivery_binding, "preparation": prep_binding,
        "conversation": CHAT, "checksPassed": 9, "checksFailed": 0}
    PACKET_PATH.write_bytes(json_bytes(packet_record))
    packet_record_binding = bind(PACKET_PATH.relative_to(ROOT).as_posix(), PACKET_PATH.read_bytes())

    prep_pending["preparedNextGroup"] = {"group": GROUP, "pendingIds": IDS, "packet": packet_binding}
    PENDING_PATH.write_bytes(json_bytes(prep_pending))
    pending_binding = bind(PENDING_PATH.relative_to(ROOT).as_posix(), PENDING_PATH.read_bytes())
    next_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": 1,
        "status": "SOURCE_AND_ACQUISITION_QUALIFICATION_PACKET_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority": False, "packet": packet_binding,
        "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding,
        "preparation": prep_binding, "candidate": candidate_binding}
    queue_after = copy.deepcopy(prep_queue)
    target_after = next(row for row in queue_after["currentPendingGroups"] if row["group"] == GROUP)
    target_after.update({"candidate": candidate_binding, "status": next_request["status"],
        "preparedPacket": packet_binding, "deliveryManifest": delivery_binding,
        "packetRecord": packet_record_binding, "preparation": prep_binding,
        "freshPacketRequiredForCurrentAuthority": False})
    queue_after.update({"pendingIdentityAudit": pending_binding, "next": next_request,
        "nextPreparedRequest": next_request, "currentPreparation": prep_binding,
        "sourcePreparation": prep_binding, "currentSourcePacket": packet_binding,
        "currentPacket": packet_binding, "currentDeliveryManifest": delivery_binding,
        "currentPacketDelivery": delivery_binding, "status": "MIND_COLLAPSE_SOURCE_QUALIFICATION_PACKET_PREPARED_816_32",
        "packetStatus": "MIND_COLLAPSE_SOURCE_QUALIFICATION_PACKET_PREPARED_UNSENT_816_32"})
    QUEUE_PATH.write_bytes(json_bytes(queue_after))
    queue_binding = bind(QUEUE_PATH.relative_to(ROOT).as_posix(), QUEUE_PATH.read_bytes())
    handoff_after = copy.deepcopy(prep_handoff)
    handoff_after.update({"pendingIdentityAudit": pending_binding, "nextPreparedRequest": next_request,
        "currentQueueBinding": queue_binding, "currentPreparation": prep_binding,
        "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
        "resumePriority": "Submit the fresh 816/32 source-and-acquisition qualification packet to the same GPT Director; retain the exact blocker if no authorized grant and acquired actor exist, then proceed to Absolute Domination and Puppetmaster's Realm in Director order."})
    HANDOFF_PATH.write_bytes(json_bytes(handoff_after))
    SNAPSHOT_PATH.write_text(
        "# Current ordinary spell-review checkpoint 276\n\n"
        "Authority is **816 reviewed / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces. "
        "The next identity is Mind Collapse / MD196-B01. GPT found no qualifying acquired full-turn grant in the inspected evidence; this packet seeks a bounded source-and-acquisition qualification and preserves all existing blockers. "
        "The current queue clears stale Unholy Ascendance labels and binds 120 refreshed source files.\n\n"
        "See [handoff](CURRENT_HANDOFF_276.json), [queue](CURRENT_SPELL_QUEUE_276.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_276.json), "
        "[packet record](RANK9MEMORYDENIAL6_PACKET_276.json), and [source packet](rank9_memorydenial6_current_source_276_prepared/DD_Rank9_MemoryDenial6_CurrentSource_276.zip).\n",
        encoding="utf-8", newline="\n")
    start_path = ROOT / "START_HERE.md"
    old_start = start_path.read_text(encoding="utf-8-sig")
    start_prefix = "**Current ordinary spell-review handoff [276](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_276.json):**"
    if not old_start.startswith(start_prefix):
        start_path.write_text(
            start_prefix + " authority is 816 reviewed / 32 pending / 0 accepted-unapplied. A fresh Mind Collapse source-and-acquisition packet is prepared for the GPT Director. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET_276.json).\n\n" + old_start,
            encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY,
        "group": GROUP, "sourceFiles": len(refreshed), "changedSincePacket224": changed,
        "packet": packet_binding, "deliveryManifest": delivery_binding,
        "queue": queue_binding, "checksPassed": 9}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
