#!/usr/bin/env python3
"""Build and verify the reversible, TEST_ONLY Banishment Gate W03 witness 400."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[5]
BASE = REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_w03_lich_taxonomy_witness400_repack01"
PKT = OUT / "packet"
SOURCES = PKT / "sources"
ARCHIVE_NAME = "DD_Rank9_BanishmentGate_PG327W03_LichTaxonomy_Witness400_Repack01_TESTONLY.zip"
ARCHIVE = OUT / ARCHIVE_NAME
DELIVERY = OUT / "ARCHIVE_DELIVERY_400_REPACK01.json"
PARENT_REL = (
    "banishment_gate_return327_received/evidence/packet327/prior/cases/"
    "RANK9PLANARGATES5129-BANISHMENT-GATE-A__stationary-type-change.json"
)
PARENT = BASE / PARENT_REL
PARENT_SHA256 = "2f3a5a697cd9effda2a921dbf22eca060716d2584340cdf8e9611b6dd66f2e3f"
PARENT_INITIAL_SHA256 = "0c0ce87d9a855a9e91b9837e34468d28cab76294fa8c48878cd519bddd27b55b"
PROPOSAL_DIR = BASE / "banishment_gate_w03_lich_taxonomy_source_proposal_398/repack03"
PROPOSAL = PROPOSAL_DIR / "OWNER_PG327_W03_LICH_TAXONOMY_SOURCE_PROPOSAL_398_REPACK03.json"
PROPOSAL_SHA256 = "a0d22b2c54958e12e93df890b169e70b578f4f66e055c5fc75f172f64271fac1"
PROPOSAL_ZIP = PROPOSAL_DIR / "PG327_W03_LichTaxonomySourceProposal398_Repack03.zip"
PROPOSAL_ZIP_SHA256 = "67c8d46883236b309f0e3eb7ba3e54bcd15477518edf321b30a95481b5741288"
OWNER_ACCEPTANCE = PROPOSAL_DIR / "OWNER_PG327_W03_LICH_TAXONOMY_SOURCE_ACCEPTANCE_399_TESTONLY.json"
DIRECTOR_READBACK = PROPOSAL_DIR / "DIRECTOR_PG398_REPACK03_REVIEW_READBACK.json"
W07_DIR = BASE / "banishment_gate_witness363_repack01/packet"
W07_REUSE_DIR = BASE / "banishment_gate_witness364_repack03/packet"
W07_SOURCE_COMMIT = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
W07_PROFILE_PATH = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/ACTOR_PROFILES.json"
W07_CATALOG_PATH = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PROCEDURE = BASE / "banishment_gate_return327_received/evidence/packet327/prior/procedures/banishment-gate.json"
PROCEDURE_SHA256 = "39c216e978e1c06da3dbea7fb27a60f8611ce08b36143c403fbca989f155fb00"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha(value: Any) -> str:
    return sha256(canonical_bytes(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def copy_bytes(source: Path, destination: Path) -> bytes:
    raw = source.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    return raw


def git_show(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=REPO)


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()


def adoption_commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "ad6b3bea"], cwd=REPO, text=True).strip()


def pointer(parts: list[str]) -> str:
    return "/" + "/".join(str(x).replace("~", "~0").replace("/", "~1") for x in parts)


def child_pointer(path: str, key: str) -> str:
    escaped = str(key).replace("~", "~0").replace("/", "~1")
    return (path or "") + "/" + escaped


def make_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    if type(before) is not type(after):
        return [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]
    if isinstance(before, dict):
        ops: list[dict[str, Any]] = []
        for key in sorted(before.keys() - after.keys()):
            ops.append({"op": "remove", "path": child_pointer(path, key)})
        for key in sorted(after.keys() - before.keys()):
            ops.append({"op": "add", "path": child_pointer(path, key), "value": copy.deepcopy(after[key])})
        for key in sorted(before.keys() & after.keys()):
            next_path = child_pointer(path, key)
            ops.extend(make_diff(before[key], after[key], next_path))
        return ops
    if isinstance(before, list):
        return [] if before == after else [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]
    return [] if before == after else [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]


def apply_patch(document: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(document)
    for op in operations:
        parts = [] if op["path"] == "" else [p.replace("~1", "/").replace("~0", "~") for p in op["path"][1:].split("/")]
        if not parts:
            if op["op"] == "remove":
                result = None
            elif op["op"] in ("add", "replace"):
                result = copy.deepcopy(op["value"])
            else:
                raise AssertionError(op)
            continue
        parent = result
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = parts[-1]
        if isinstance(parent, list):
            ix = int(key)
            if op["op"] == "remove":
                parent.pop(ix)
            elif op["op"] == "add":
                parent.insert(ix, copy.deepcopy(op["value"]))
            elif op["op"] == "replace":
                parent[ix] = copy.deepcopy(op["value"])
        elif op["op"] == "remove":
            del parent[key]
        elif op["op"] in ("add", "replace"):
            parent[key] = copy.deepcopy(op["value"])
        else:
            raise AssertionError(op)
    return result


def point_distance(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def source_file(rel: str) -> Path:
    return REPO / Path(rel)


def prepare_sources() -> dict[str, dict[str, Any]]:
    SOURCES.mkdir(parents=True, exist_ok=True)
    catalog_bytes = git_show(W07_SOURCE_COMMIT, W07_CATALOG_PATH)
    profile_bytes = git_show(W07_SOURCE_COMMIT, W07_PROFILE_PATH)
    payload_map: dict[str, tuple[bytes, str, str, str | None]] = {}

    def add_file(source: Path, member: str, source_path: str | None = None) -> None:
        raw = source.read_bytes()
        (PKT / member).parent.mkdir(parents=True, exist_ok=True)
        (PKT / member).write_bytes(raw)
        payload_map[member] = (raw, source_path or str(source.relative_to(REPO)), "exact source bytes", None)

    def add_raw(raw: bytes, member: str, repository_path: str, representation: str, commit: str | None = None) -> None:
        (PKT / member).parent.mkdir(parents=True, exist_ok=True)
        (PKT / member).write_bytes(raw)
        payload_map[member] = (raw, repository_path, representation, commit)

    add_file(PROPOSAL, "sources/PROPOSAL_398_REPACK03.json")
    add_file(PROPOSAL_ZIP, "sources/PROPOSAL_398_REPACK03.zip")
    add_file(OWNER_ACCEPTANCE, "sources/OWNER_SOURCE_ACCEPTANCE_399.json")
    add_file(DIRECTOR_READBACK, "sources/DIRECTOR_PROPOSAL_REVIEW_READBACK_398.json")
    add_file(PARENT, "sources/RETURN327_STATIONARY_TYPE_CHANGE_PARENT.json")
    add_file(PROCEDURE, "sources/RETURN327_BANISHMENT_GATE_PROCEDURE.json")
    add_file(W07_DIR / "SOURCE_BINDINGS_363.json", "sources/W07_SOURCE_BINDINGS_363.json")
    add_file(W07_DIR / "W07_DIRECTOR_RULING_363.json", "sources/W07_DIRECTOR_RULING_363.json")
    add_file(BASE / "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json", "sources/W07_DIRECTOR_SEAL_363_REPACK01.json")
    add_file(W07_REUSE_DIR / "W07_SOURCE_REUSE_364.json", "sources/W07_SOURCE_REUSE_364.json")
    add_file(W07_DIR / "W07_GUST_CORPSE_CASE_363.json", "sources/W07_GUST_CORPSE_CASE_363.json")
    add_file(W07_REUSE_DIR / "prior/W07_Repack01_TESTONLY.zip", "sources/W07_Repack01_TESTONLY.zip")
    add_file(W07_DIR / "sources/rules/COMBAT_ACTION.md", "sources/COMBAT_ACTION_PLAYTEST.md")
    add_file(W07_DIR / "authority/CURRENT_SPELL_QUEUE_361.json", "sources/CURRENT_SPELL_QUEUE_361.json")
    add_file(W07_DIR / "authority/CURRENT_HANDOFF_361.json", "sources/CURRENT_HANDOFF_361.json")
    add_file(source_file("DescentReviewChanges/ReviewBible/docs/mechanics/classes/mage.md"), "sources/mage.md")
    add_file(source_file("DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json"), "sources/mage.json")
    add_file(source_file("DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md"), "sources/ANCESTRY_BACKGROUND_PLAYTEST.md")
    add_raw(catalog_bytes, "sources/W07_BOUND_CATALOG_351fe708.json", W07_CATALOG_PATH, "exact git show bytes", W07_SOURCE_COMMIT)
    add_raw(profile_bytes, "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json", W07_PROFILE_PATH, "exact git show bytes", W07_SOURCE_COMMIT)

    with zipfile.ZipFile(PROPOSAL_ZIP) as zf:
        assert zf.testzip() is None
        proposal_members = [name for name in zf.namelist() if name.endswith("OWNER_PG327_W03_LICH_TAXONOMY_SOURCE_PROPOSAL_398_REPACK03.json")]
        assert len(proposal_members) == 1 and zf.read(proposal_members[0]) == PROPOSAL.read_bytes()
    proposed = read_json(PROPOSAL)
    staged_source_by_path = {
        "DescentReviewChanges/ReviewBible/docs/mechanics/classes/mage.md": PKT / "sources/mage.md",
        "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json": PKT / "sources/mage.json",
        "DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md": PKT / "sources/ANCESTRY_BACKGROUND_PLAYTEST.md",
    }
    for row in proposed["sourceBindings"]:
        if row["path"] in staged_source_by_path:
            raw = staged_source_by_path[row["path"]].read_bytes()
            assert len(raw) == row["bytes"] and sha256(raw) == row["sha256"]
    seal = read_json(BASE / "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json")
    w07_archive_copy = PKT / "sources/W07_Repack01_TESTONLY.zip"
    assert len(w07_archive_copy.read_bytes()) == seal["archiveBytes"]
    assert sha256(w07_archive_copy.read_bytes()) == seal["archiveSha256"]
    reuse = read_json(PKT / "sources/W07_SOURCE_REUSE_364.json")
    assert reuse["w07ArchiveSha256"] == seal["archiveSha256"]
    assert reuse["w07SourceBindingsSha256"] == sha256((PKT / "sources/W07_SOURCE_BINDINGS_363.json").read_bytes())

    return {
        member: {
            "member": member,
            "repositoryPath": repo_path,
            "representation": representation,
            "sourceCommit": commit,
            "bytes": len(raw),
            "sha256": sha256(raw),
        }
        for member, (raw, repo_path, representation, commit) in payload_map.items()
    }


def make_mage() -> dict[str, Any]:
    return {
        "id": "M-W03-400",
        "origin": "authored branch-only TEST_ONLY actor; not a campaign character",
        "class": "Mage",
        "classLevel": 10,
        "pathBeforeFinalRoll": None,
        "lawfulLevel10PathOpportunity": "Lich, conditional on successful ritual; no second path or respec",
        "ancestryId": "TEST-ANCESTRY-HUMAN-01",
        "ancestryVariant": None,
        "abilityScores": {"INT": 18, "CON": 14},
        "modifiers": {"INT": 4, "CON": 2},
        "creatureTypes": ["Humanoid"],
        "lifeState": "active-alive",
        "hp": 60,
        "maxHP": 60,
        "RP": 29,
        "maxRP": 29,
        "Dissonance": 0,
        "tempHP": 0,
        "wounds": 0,
        "death": {"status": "alive", "successes": 0, "failures": 0},
        "classResources": {},
        "actionBudget": 0,
        "bonusActionBudget": 0,
        "reactionBudget": 0,
        "movementBudget": 0,
        "restCounters": {"shortRestsSinceLong": 0, "arcaneRecoveryUsed": False},
        "conditions": [],
        "body": {
            "id": "M-W03-400-BODY-01",
            "exists": True,
            "state": "extant",
            "size": "Medium",
            "bodyBoxFeet": [5, 5, 6],
            "occupiedVolumeCubicFeet": 150,
            "positionConvention": "horizontal center and feet/base elevation",
            "position": [0, 30, 0],
            "orientation": [0, 1, 0],
            "plane": "fixture:origin",
        },
        "position": [0, 30, 0],
        "orientation": [0, 1, 0],
        "equipmentIds": [],
        "cargoIds": [],
        "custody": {"holder": "M-W03-400", "items": []},
        "ritual": {
            "stateAtFork": "in-progress",
            "startEventTime": -3599.0,
            "durationSeconds": 3600,
            "elapsedAtForkSeconds": 3598.9,
            "remainingAtForkSeconds": 1.1,
            "voluntaryActivity": "the Lich final ritual only",
            "initiativeTurnsGrantedDuringRitual": 0,
            "actionGrantedDuringRitual": 0,
            "reactionGrantedDuringRitual": 0,
            "resourceRefreshesDuringRitual": 0,
        },
    }


def make_caster(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "W03-WIZARD20-400",
        "origin": "branch-only TEST_ONLY instantiation of the sealed W07 Wizard20 profile; no campaign existence claimed",
        "profileId": profile["id"],
        "profilePointer": "/Wizard20",
        "profileSha256": "031e83195692df0359c39908dc5cd4673ce573559f233179be90e467e0c1cfbd",
        "class": "Wizard",
        "classLevel": 20,
        "PB": profile["PB"],
        "M": profile["M"],
        "S": profile["S"],
        "abilityScores": copy.deepcopy(profile["abilityScores"]),
        "spellAttack": profile["spellAttack"],
        "spellDC": profile["spellDC"],
        "HP": 122,
        "maxHP": 122,
        "RP": 80,
        "maxRP": 80,
        "Dissonance": 0,
        "Refrain": 0,
        "lastSpell": None,
        "preparedFamiliesUsed": [],
        "spellHistory": [],
        "resourceHistory": [],
        "concentration": None,
        "conditions": [],
        "death": {"status": "alive", "successes": 0, "failures": 0},
        "plane": "fixture:origin",
        "position": [200, 0, 0],
        "size": "Medium",
        "bodyBox": [5, 5, 6],
        "orientation": "standing",
        "voice": True,
        "hands": 2,
        "focusAccessible": True,
        "equipment": ["focus-W03-400"],
        "carriedItemIds": [],
        "action": 0,
        "bonusAction": 0,
        "reaction": 1,
        "movement": 0,
        "regularSchedule": {
            "firstStart": 0.0,
            "period": 6.0,
            "endOffset": 0.9,
            "nextStart": 0.0,
            "nextEnd": 0.9,
            "starts": [],
            "ends": [],
            "budgetHistory": [],
        },
        "knownSpells": ["banishment-gate", "counterspell"],
        "spellbookIncludes": ["banishment-gate", "counterspell"],
        "preparedSpells": copy.deepcopy(profile["prepared"]),
        "gateAcquisition": {
            "classLevel": 17,
            "spellRank": 9,
            "source": "sealed W07 Director ruling 363; profile-bound Wizard20 access",
            "campaignExistenceVerified": False,
        },
    }


def set_time(state: dict[str, Any], event_time: float) -> None:
    state["time"] = round(event_time, 10)
    state["clock"] = {
        "elapsedSeconds": round(event_time + 0.1, 10),
        "eventTimeOffsetSeconds": 0.1,
        "sourceMapping": "Preserves Return327 event/world-clock offset: elapsedSeconds = eventTime + 0.1.",
    }
    if "ritual" in state:
        elapsed = min(3600.0, max(0.0, event_time - (-3599.0)))
        state["ritual"]["elapsedSeconds"] = round(elapsed, 10)
        state["ritual"]["remainingSeconds"] = round(3600.0 - elapsed, 10)


def schedule_start(actor: dict[str, Any], start_time: float) -> None:
    schedule = actor["regularSchedule"]
    schedule["starts"].append(start_time)
    schedule["nextStart"] = round(start_time + schedule["period"], 10)
    schedule["nextEnd"] = round(start_time + schedule["endOffset"], 10)
    actor["action"] = 1
    actor["bonusAction"] = 1
    actor["reaction"] = 1
    actor["movement"] = actor.get("speed", 30)
    schedule["budgetHistory"].append({"time": start_time, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": actor["movement"]})


def schedule_end(actor: dict[str, Any], end_time: float) -> None:
    schedule = actor["regularSchedule"]
    schedule["ends"].append(end_time)
    schedule["nextEnd"] = round(schedule["nextStart"] + schedule["endOffset"], 10)
    actor["action"] = 0
    actor["bonusAction"] = 0
    actor["movement"] = 0


def build_replay(parent: dict[str, Any], profile: dict[str, Any], catalog: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    base_state = copy.deepcopy(parent["initial"])
    state = copy.deepcopy(base_state)
    snapshots: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []

    def add_snapshot(snapshot_id: str, label: str, event_time: float, live_state: dict[str, Any]) -> None:
        snapshots.append({"id": snapshot_id, "label": label, "eventTime": event_time, "stateSha256": canonical_sha(live_state), "state": copy.deepcopy(live_state)})

    add_snapshot("S000", "Exact historical /initial before branch extensions", -0.1, state)

    def event(event_id: str, event_time: float, kind: str, description: str, source: str, inputs: dict[str, Any], mutate) -> None:
        before = copy.deepcopy(state)
        mutate(state)
        set_time(state, event_time)
        after = copy.deepcopy(state)
        before_id = snapshots[-1]["id"]
        after_id = f"S{len(snapshots):03d}"
        add_snapshot(after_id, f"After {kind}: {description}", event_time, after)
        forward = make_diff(before, after)
        inverse = make_diff(after, before)
        assert canonical_sha(apply_patch(before, forward)) == canonical_sha(after)
        assert canonical_sha(apply_patch(after, inverse)) == canonical_sha(before)
        events.append({
            "id": event_id,
            "eventTime": event_time,
            "kind": kind,
            "description": description,
            "source": source,
            "authoredInputs": inputs,
            "beforeSnapshot": before_id,
            "afterSnapshot": after_id,
            "beforeStateSha256": canonical_sha(before),
            "afterStateSha256": canonical_sha(after),
            "forwardPatch": forward,
            "inversePatch": inverse,
        })

    def branch_setup(s: dict[str, Any]) -> None:
        w07 = make_caster(profile)
        mage = make_mage()
        s["fixture"] = {
            "id": "PG327-W03-400-TESTONLY",
            "campaignFact": False,
            "liveFixtureMutation": False,
            "originTerrain": "clear open fixture; no walls, blockers, hazards, or unlisted bodies",
            "distanceUnit": "feet",
            "baseFork": {"sourceCase": PARENT_REL.replace("\\", "/"), "sourcePointer": "/initial", "stateSha256": PARENT_INITIAL_SHA256},
            "unlistedBodies": "absent",
        }
        s["clock"] = {"elapsedSeconds": 0.0, "eventTimeOffsetSeconds": 0.1, "sourceMapping": "elapsedSeconds = eventTime + 0.1"}
        s["ritual"] = {
            "id": "W03-RITUAL-400",
            "status": "in-progress",
            "startEventTime": -3599.0,
            "deadlineEventTime": 1.0,
            "durationSeconds": 3600,
            "elapsedSeconds": 3598.9,
            "remainingSeconds": 1.1,
            "clockPaused": False,
            "turnOrActionGranted": False,
            "reactionGranted": False,
            "resourceRefreshGranted": False,
            "mageId": mage["id"],
            "selectedPaymentRoute": "TWO_AVAILABLE_PARTICIPANTS",
        }
        s["actors"][mage["id"]] = mage
        s["actors"][w07["id"]] = w07
        s["ritualParticipants"] = [
            {"id": "W03-PARTICIPANT-01", "name": "Test Participant One", "origin": "authored TEST_ONLY premise", "position": [-10, 30, 0], "available": True, "willing": True, "consumed": False},
            {"id": "W03-PARTICIPANT-02", "name": "Test Participant Two", "origin": "authored TEST_ONLY premise", "position": [10, 30, 0], "available": True, "willing": True, "consumed": False},
        ]
        s["ritualGuardians"] = [
            {"id": "W03-MINIBOSS-01", "name": "Test Mini-Boss One", "position": [-20, 30, 0], "bound": True, "named": True, "miniBoss": True},
            {"id": "W03-MINIBOSS-02", "name": "Test Mini-Boss Two", "position": [20, 30, 0], "bound": True, "named": True, "miniBoss": True},
        ]
        s["ritualNexus"] = {"id": "W03-PLANAR-NEXUS-01", "position": [0, 30, 0], "secured": True, "securedThroughout": True}
        s["effects"] = {}
        s["gateClaims"] = []
        s["banishmentCells"] = []
        s["branchOnlyPremises"] = {
            "sourceAcceptance": "Proposal 398 Repack03 accepted TEST_ONLY by owner and Director, W03 only",
            "divineEchoEncounter": {"completed": True, "survived": True},
            "historicalFailureStakesDisclosed": [
                "permanent loss of spellcasting",
                "transformation into a cursed melee undead NPC",
                "hostile faction consequences",
                "cursed-gear restriction",
                "no further XP as the retired PC",
            ],
            "explicitPlayerOptInBeforeRitual": True,
            "explicitConsentAtFork": True,
            "consentWithdrawnBeforeFinalRoll": False,
            "soulCoinRouteSelected": False,
            "soulCoinConsumed": False,
            "thirdGuardianPresent": False,
            "thirdGuardianModifier": 0,
        }

    event(
        "W03-400-BRANCH-SETUP",
        -0.1,
        "TESTONLY_BRANCH_SETUP",
        "Add only authored W03 branch actors and premises over the untouched Return327 /initial fork.",
        "Owner acceptance 399 + Director SOURCE_ACCEPTED_TEST_ONLY_W03 and setup-cast authorization",
        {"parentFileSha256": PARENT_SHA256, "parentInitialCanonicalSha256": PARENT_INITIAL_SHA256, "noParentBytesChanged": True},
        branch_setup,
    )

    def start_actor(actor_id: str):
        return lambda s: schedule_start(s["actors"][actor_id], 0.0)

    event("W03-400-START-A", 0.0, "REGULAR_START", "Process inherited actor A's due original start marker.", "Return327 parent /initial regularSchedule; Combat Action regular-turn rule", {"actorId": "A", "scheduledTime": 0.0}, start_actor("A"))
    wizard_id = "W03-WIZARD20-400"
    event("W03-400-START-WIZARD", 0.0, "REGULAR_START", "Process the TEST_ONLY W07 Wizard20 creator's due start marker before casting.", "Sealed W07 Wizard20 profile + Combat Action regular-turn rule", {"actorId": wizard_id, "scheduledTime": 0.0}, start_actor(wizard_id))

    def commit_cast(s: dict[str, Any]) -> None:
        actor = s["actors"][wizard_id]
        actor["RP"] -= 26
        actor["action"] -= 1
        actor["lastSpell"] = "banishment-gate"
        actor["preparedFamiliesUsed"].append("banishment-gate")
        actor["spellHistory"].append({
            "castId": "W03-400-BANISHMENT-GATE-CAST01",
            "spellId": "banishment-gate",
            "class": "Wizard",
            "rank": 9,
            "school": "Abjuration",
            "commitEventTime": 0.0,
            "resolveEventTime": 0.1,
            "costRP": 26,
            "components": ["V", "S", "F"],
            "target": None,
            "selectedType": "Undead",
            "concentration": True,
            "firstPreparedFamily": True,
            "baseDissonance": 0,
            "Refrain": 0,
        })
        actor["resourceHistory"].append({"event": "W03-400-BANISHMENT-GATE-CAST01", "RP": -26, "poolAfter": 54, "discount": False})
        actor["concentration"] = "W03-400-BANISHMENT-GATE-CAST01"

    point = [300, 0, 7.5]
    caster_position = [200, 0, 0]
    distance = point_distance(caster_position, point)
    responders = []
    for actor_id in ["A", "B", "C", "D", "M-W03-400", "W03-MINIBOSS-01", "W03-MINIBOSS-02"]:
        actor = build_replay_actor_lookup(actor_id)
        distance_to_caster = point_distance(actor["position"], caster_position)
        responders.append({"actorId": actor_id, "distanceFeet": round(distance_to_caster, 6), "counterspellRangeFeet": 60, "withinRange": distance_to_caster <= 60, "disposition": "out of range; cannot respond" if distance_to_caster > 60 else "in range; no response authored"})
    responders.extend([
        {"actorId": "W03-PARTICIPANT-01", "distanceFeet": round(point_distance([-10, 30, 0], caster_position), 6), "counterspellRangeFeet": 60, "withinRange": False, "disposition": "ritual participant; out of range"},
        {"actorId": "W03-PARTICIPANT-02", "distanceFeet": round(point_distance([10, 30, 0], caster_position), 6), "counterspellRangeFeet": 60, "withinRange": False, "disposition": "ritual participant; out of range"},
    ])
    event(
        "W03-400-CAST-COMMIT",
        0.0,
        "CAST_COMMIT",
        "Commit one expressly authorized TEST_ONLY Gate setup cast using the sealed W07 Wizard20 access binding.",
        "W07 source/access binding; Banishment Gate PG9-Q01/Q13-Q15; Combat Action cast procedure",
        {
            "castId": "W03-400-BANISHMENT-GATE-CAST01",
            "freshCastAndEffectIdentity": True,
            "spellId": "banishment-gate",
            "access": {"class": "Wizard", "classLevel": 20, "acquiredAtLevel": 17, "rank": 9, "inSpellbook": True, "prepared": True, "campaignExistenceClaimed": False},
            "actionAvailableAfterStart": True,
            "actionCost": 1,
            "rpBefore": 80,
            "rpCost": 26,
            "rpAfterCommit": 54,
            "components": {"V": True, "S": True, "F": True, "voice": True, "hands": 2, "focusAccessible": True},
            "selectedType": "Undead",
            "target": None,
            "concentration": True,
            "counterspellWindow": {"fromEventTime": 0.0, "untilEventTime": 0.1, "eligibleResponders": [], "dispositions": responders, "attempted": False, "responseResourceSpent": False},
            "point": point,
            "aperture": {"plane": "x=300", "center": point, "normal": [1, 0, 0], "widthAxis": [0, 1, 0], "verticalAxis": [0, 0, 1], "widthFeet": 10, "heightFeet": 15, "yBounds": [-5, 5], "zBounds": [0, 15]},
            "casterPosition": caster_position,
            "rangeFeet": 120,
            "distanceFeet": round(distance, 6),
            "clearPerceivedSpace": True,
            "lineOfSightAndPlacementClear": True,
        },
        commit_cast,
    )

    def resolve_gate(s: dict[str, Any]) -> None:
        s["effects"]["W03-400-BANISHMENT-GATE-EFFECT01"] = {
            "effectId": "W03-400-BANISHMENT-GATE-EFFECT01",
            "castId": "W03-400-BANISHMENT-GATE-CAST01",
            "spellId": "banishment-gate",
            "creatorId": wizard_id,
            "selectedType": "Undead",
            "active": True,
            "concentration": True,
            "createdAt": 0.1,
            "deadline": 600.1,
            "aperture": {"plane": "x=300", "center": point, "normal": [1, 0, 0], "widthFeet": 10, "heightFeet": 15, "yBounds": [-5, 5], "zBounds": [0, 15]},
            "crossings": [],
            "claims": [],
            "cells": [],
        }

    event(
        "W03-400-CAST-RESOLVE",
        0.1,
        "CAST_RESOLVE",
        "Resolve the setup cast and open the fixed Undead-selected Gate at event time 0.1.",
        "Banishment Gate PG9-Q01/Q13/Q14/Q15 + W07 sealed setup-cast permission",
        {"effectId": "W03-400-BANISHMENT-GATE-EFFECT01", "selectedType": "Undead", "createdAt": 0.1, "deadline": 600.1, "unresolvedCounterspell": False},
        resolve_gate,
    )

    def end_actor(actor_id: str):
        return lambda s: schedule_end(s["actors"][actor_id], 0.9)

    event("W03-400-END-A", 0.9, "TURN_END", "Process A's scheduled turn end before the final ritual operations.", "Return327 parent regularSchedule + Combat Action regular-turn rule", {"actorId": "A", "scheduledTime": 0.9, "GateConcentrationContinues": True}, end_actor("A"))
    event("W03-400-END-WIZARD", 0.9, "TURN_END", "Process the Wizard20 creator's turn end; Gate concentration continues.", "W07 profile schedule + Combat Action regular-turn rule", {"actorId": wizard_id, "scheduledTime": 0.9, "GateConcentrationContinues": True}, end_actor(wizard_id))

    def start_b(s: dict[str, Any]) -> None:
        schedule_start(s["actors"]["B"], 1.0)

    event("W03-400-START-B", 1.0, "REGULAR_START", "Resolve B's due scheduled start before any final ritual operation at event time 1.0.", "Return327 parent /initial regularSchedule; Combat Action regular-turn rule", {"actorId": "B", "scheduledTime": 1.0, "orderedBeforeFinalRitualOperations": True}, start_b)

    def complete_ritual(s: dict[str, Any]) -> None:
        s["ritual"]["status"] = "continuous-interval-complete"
        s["ritual"]["elapsedSeconds"] = 3600.0
        s["ritual"]["remainingSeconds"] = 0.0

    event("W03-400-RITUAL-COMPLETE", 1.0, "RITUAL_INTERVAL_COMPLETE", "Complete the full continuous 3,600-second interval after due regular markers.", "Accepted Proposal 398 Repack03 /proposedRule/ritualTimingAndInterruption", {"startEventTime": -3599.0, "endEventTime": 1.0, "durationSeconds": 3600.0, "clockPaused": False}, complete_ritual)

    def final_recheck(s: dict[str, Any]) -> None:
        s["ritual"]["finalRecheck"] = {
            "eventTime": 1.0,
            "mageLevel10AndPathOpportunity": True,
            "typesExactlyHumanoid": s["actors"]["M-W03-400"]["creatureTypes"] == ["Humanoid"],
            "divineEchoSurvived": s["branchOnlyPremises"]["divineEchoEncounter"]["survived"],
            "nexusSecured": s["ritualNexus"]["secured"],
            "namedBoundMiniBossGuardians": len(s["ritualGuardians"]),
            "thirdGuardianModifier": 0 if len(s["ritualGuardians"]) == 2 else 2,
            "selectedPaymentRoute": s["ritual"]["selectedPaymentRoute"],
            "coinRouteNotSelected": s["ritual"]["selectedPaymentRoute"] == "TWO_AVAILABLE_PARTICIPANTS",
            "twoParticipantsAvailable": all(p["available"] for p in s["ritualParticipants"]),
            "bothParticipantsWilling": all(p["willing"] for p in s["ritualParticipants"]),
            "explicitConsent": s["branchOnlyPremises"]["explicitConsentAtFork"] and not s["branchOnlyPremises"]["consentWithdrawnBeforeFinalRoll"],
            "interruptionConditions": {"incapacitated": False, "leftOrForcedFromNexus": False, "nexusUnsecured": False, "fewerThanTwoGuardiansBound": False, "participantsUnavailable": False, "consentWithdrawn": False},
        }

    event("W03-400-FINAL-RECHECK", 1.0, "FINAL_PREREQUISITE_RECHECK", "Recheck every eligibility, readiness, nexus, guardian, payment-route and consent predicate immediately before the final roll.", "Accepted Proposal 398 Repack03 /accessAndTiming + /ritualTimingAndInterruption", {"orderedAfterDueMarkers": True, "beforePaymentAndRoll": True}, final_recheck)

    def commit_participant_route(s: dict[str, Any]) -> None:
        s["ritual"]["paymentCommit"] = {"eventTime": 1.0, "route": "TWO_AVAILABLE_PARTICIPANTS", "committedImmediatelyBeforeRoll": True, "participantIds": [p["id"] for p in s["ritualParticipants"]], "soulCoinConsumed": False, "RPSpent": 0, "spellSlotSpent": False, "participantsConsumed": False}

    event("W03-400-PARTICIPANT-ROUTE-COMMIT", 1.0, "PAYMENT_ROUTE_COMMIT", "Commit the accepted participant route immediately before the roll; no consumable is spent.", "Accepted Proposal 398 Repack03 /paymentAndConsumptionClarification", {"selectedRoute": "TWO_AVAILABLE_PARTICIPANTS", "coinRouteNotSelected": True, "paymentImmediatelyBeforeRoll": True}, commit_participant_route)

    def ritual_roll(s: dict[str, Any]) -> None:
        s["ritual"]["finalCheck"] = {
            "eventTime": 1.0,
            "testOnlyDeterministicInput": True,
            "d20Faces": [11, 15],
            "advantage": True,
            "advantageBasis": "both available ritual participants are willing at the final check",
            "keptD20": 15,
            "INTModifier": 4,
            "CONModifier": 2,
            "thirdGuardianModifier": 0,
            "total": 21,
            "DC": 20,
            "success": True,
            "notCampaignRandomness": True,
        }
        s["ritual"]["status"] = "successful"

    event("W03-400-FINAL-ROLL", 1.0, "RITUAL_FINAL_CHECK", "Resolve the disclosed and consented TEST_ONLY Lich ritual check.", "Accepted Proposal 398 Repack03 /checkAndResolution + Mage source /engine/15-/engine/17", {"d20Faces": [11, 15], "formula": "d20 + INT + CON", "DC": 20}, ritual_roll)

    def taxonomy_update(s: dict[str, Any]) -> None:
        mage = s["actors"]["M-W03-400"]
        mage["creatureTypes"] = ["Humanoid", "Undead"]
        mage["classPath"] = "Lich"
        mage["successfulLichTransformation"] = True
        mage["lichPathUnlocks"] = {"eligibleCards": ["mage.hero.lich.lingering-malice", "mage.hero.lich.resonance-to-flesh"], "eliteCompanionOptionsUnlocked": True, "eliteCompanionSelectedOrSpawned": False, "automaticCardSelection": False}
        mage["selectedPathCards"] = []
        mage["taxonomyRemovalMechanism"] = None

    event("W03-400-TAXONOMY-UPDATE", 1.0, "SUCCESSFUL_TAXONOMY_UPDATE", "After actual successful resolution only, atomically add Undead while retaining Humanoid on the same Mage and body.", "Accepted Proposal 398 Repack03 /proposedInsertionText + /taxonomyAndInteractions", {"requiresSuccessfulRoll": True, "from": ["Humanoid"], "to": ["Humanoid", "Undead"], "sameActorAndBody": True, "noGateCrossing": True}, taxonomy_update)

    def select_l10_cards(s: dict[str, Any]) -> None:
        s["actors"]["M-W03-400"]["selectedPathCards"] = ["mage.hero.lich.lingering-malice", "mage.hero.lich.resonance-to-flesh"]
        s["actors"]["M-W03-400"]["pathCardSelectionEvidence"] = {
            "selectionIsExplicitScenarioInput": True,
            "classLevel": 10,
            "path": "Lich",
            "cardIds": ["mage.hero.lich.lingering-malice", "mage.hero.lich.resonance-to-flesh"],
            "eachMinimumClassLevel": 10,
            "minimumActiveChoiceSatisfied": True,
            "cardEffectsActivated": False,
            "undeadImmunitiesSelected": False,
        }

    event("W03-400-L10-CARD-SELECTION", 1.0, "EXPLICIT_LEVEL10_PATH_CARD_SELECTION", "Record the two authored legal level-10 Lich card choices separately; neither card is activated and no immunity is acquired.", "Mage source /engine/19 and mage.json /schedule/9, /cards/46-/cards/47", {"cardIds": ["mage.hero.lich.lingering-malice", "mage.hero.lich.resonance-to-flesh"], "notAutomatic": True}, select_l10_cards)

    replay = {
        "id": "PG327-W03-LICH-TAXONOMY-WITNESS-400-REPLAY",
        "status": "TEST_ONLY_OPEN_UNSEALED",
        "eventTimeToParentClockMapping": "parent elapsedSeconds = eventTime + 0.1",
        "parent": {"path": PARENT_REL.replace("\\", "/"), "fileSha256": PARENT_SHA256, "forkPointer": "/initial", "initialCanonicalSha256": PARENT_INITIAL_SHA256, "parentContainsBanishmentGate": False, "parentSelectedTypeInvented": False},
        "parentClockOffsetEvidence": {"sourceFinalEventTime": parent["final"]["time"], "sourceFinalClockElapsedSeconds": parent["final"]["clock"]["elapsedSeconds"], "offsetSeconds": round(parent["final"]["clock"]["elapsedSeconds"] - parent["final"]["time"], 10), "mapping": "elapsedSeconds = eventTime + 0.1", "newWitnessFinalEventTime": 1.0, "newWitnessFinalClockElapsedSeconds": 1.1},
        "ritualInterval": {"startEventTime": -3599.0, "endEventTime": 1.0, "durationSeconds": 3600.0, "intervalEvidencePath": "W03_SCENARIO_400_TESTONLY.json#/ritualContinuity/checkpoints"},
        "events": events,
        "stateSnapshots": snapshots,
        "inverseRestorationOrder": [event["id"] for event in reversed(events)],
        "finalSnapshotId": snapshots[-1]["id"],
        "nonClaims": ["no live/campaign Gate cast", "no source modification", "no crossing", "no admission", "no cell", "no hard-denial claim", "no W03 seal", "no spell acceptance/application", "no queue change"],
    }

    # Replay proof: every stored transition is exactly reversible to the original /initial.
    state_restore = copy.deepcopy(snapshots[-1]["state"])
    by_id = {snap["id"]: snap for snap in snapshots}
    for ev in reversed(events):
        assert canonical_sha(state_restore) == ev["afterStateSha256"], ev["id"]
        state_restore = apply_patch(state_restore, ev["inversePatch"])
        assert canonical_sha(state_restore) == ev["beforeStateSha256"], ev["id"]
    assert canonical_sha(state_restore) == PARENT_INITIAL_SHA256
    assert state_restore == parent["initial"]

    # Semantic assertions compare the successful taxonomy transition only.
    before_tax = by_id[next(e["beforeSnapshot"] for e in events if e["kind"] == "SUCCESSFUL_TAXONOMY_UPDATE")]["state"]
    after_tax = by_id[next(e["afterSnapshot"] for e in events if e["kind"] == "SUCCESSFUL_TAXONOMY_UPDATE")]["state"]
    m0 = before_tax["actors"]["M-W03-400"]
    m1 = after_tax["actors"]["M-W03-400"]
    preserved = ["id", "ancestryId", "ancestryVariant", "lifeState", "hp", "maxHP", "RP", "maxRP", "Dissonance", "tempHP", "wounds", "death", "classResources", "actionBudget", "bonusActionBudget", "reactionBudget", "movementBudget", "restCounters", "conditions", "body", "position", "orientation", "equipmentIds", "cargoIds", "custody"]
    assert all(m0[k] == m1[k] for k in preserved)
    assert m0["creatureTypes"] == ["Humanoid"] and m1["creatureTypes"] == ["Humanoid", "Undead"]
    final = snapshots[-1]["state"]
    gate = final["effects"]["W03-400-BANISHMENT-GATE-EFFECT01"]
    assert gate["active"] and gate["selectedType"] == "Undead" and gate["deadline"] - final["time"] == 599.1
    assert not final["gateClaims"] and not final["banishmentCells"] and gate["crossings"] == [] and gate["cells"] == []
    return replay, {"beforeTaxonomySnapshot": next(e["beforeSnapshot"] for e in events if e["kind"] == "SUCCESSFUL_TAXONOMY_UPDATE"), "afterTaxonomySnapshot": next(e["afterSnapshot"] for e in events if e["kind"] == "SUCCESSFUL_TAXONOMY_UPDATE"), "preservedMageFields": preserved}


def build_replay_actor_lookup(actor_id: str) -> dict[str, Any]:
    # Positions in the exact inherited parent are static for this zero-crossing setup.
    parent = read_json(PARENT)
    if actor_id in parent["initial"]["actors"]:
        return parent["initial"]["actors"][actor_id]
    return {
        "M-W03-400": {"position": [0, 30, 0]},
        "W03-MINIBOSS-01": {"position": [-20, 30, 0]},
        "W03-MINIBOSS-02": {"position": [20, 30, 0]},
    }[actor_id]


def build_scenario(parent: dict[str, Any]) -> dict[str, Any]:
    proposal = read_json(PROPOSAL)
    mage = read_json(PKT / "sources/mage.json")
    wizard20 = read_json(PKT / "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json")["Wizard20"]
    cat = read_json(PKT / "sources/W07_BOUND_CATALOG_351fe708.json")
    gate_rows = [(i, x) for i, x in enumerate(cat["spells"]) if x.get("id") == "banishment-gate"]
    assert len(gate_rows) == 1
    gate_index, gate_card = gate_rows[0]
    wizard_access = gate_card["classAccess"]["Wizard"]
    mage_level10 = mage["schedule"][9]
    mage_cards = {card["id"]: card for card in mage["cards"]}
    selected_cards = ["mage.hero.lich.lingering-malice", "mage.hero.lich.resonance-to-flesh"]
    assert all(mage_cards[c]["minimumClassLevel"] == 10 and mage_cards[c]["path"] == "Lich" and mage_cards[c]["sourceKind"] == "active" for c in selected_cards)

    gates = [
        "mage incapacitated",
        "mage leaves or is forced away from secured nexus",
        "nexus ceases to be secured",
        "fewer than two named mini-boss guardians remain bound",
        "selected Soul Coin route loses its qualifying coin",
        "selected participant route loses two available participants",
        "player withdraws explicit consent before final roll",
    ]
    checkpoints = []
    for t in [-3599.0, -2699.0, -1799.0, -899.0, -0.1, 0.0, 0.1, 0.9, 1.0]:
        elapsed = round(t + 3599.0, 10)
        checkpoints.append({
            "eventTime": t,
            "elapsedSinceRitualStartSeconds": elapsed,
            "remainingSeconds": round(3600.0 - elapsed, 10),
            "clockRunning": True,
            "mageIdentity": "M-W03-400",
            "lifeState": "active-alive",
            "bodyPosition": [0, 30, 0],
            "bodyOrientation": [0, 1, 0],
            "bodyVolumeCubicFeet": 150,
            "movementSincePreviousCheckpoint": [0, 0, 0],
            "typesBeforeFinalRoll": ["Humanoid"],
            "nexusSecured": True,
            "twoNamedGuardiansBound": True,
            "twoParticipantsAvailable": True,
            "bothParticipantsWilling": True,
            "consentPresent": True,
            "interruptionConditions": {name: False for name in gates},
            "mageTakesOtherVoluntaryActivity": False,
            "mageTurnActionReactionOrRefreshGranted": False,
            "worldEffectsAndClocksPaused": False,
            "damageEvent": False,
        })

    return {
        "id": "PG327-W03-LICH-TAXONOMY-WITNESS-400-TESTONLY",
        "status": "TEST_ONLY_OPEN_UNSEALED",
        "spellId": "banishment-gate",
        "witnessId": "W03",
        "blockerIds": ["PG200-B03", "PG200-B04"],
        "scenarioQualification": {
            "testOnly": True,
            "campaignFact": False,
            "ownerAuthorizedSource": "Proposal 398 Repack03; exact SHA-256 bound in SOURCE_BINDINGS_400.json",
            "directorAcceptedSourceAndAuthorizedConstruction": True,
            "worldOrFixtureMutation": False,
            "purpose": "Demonstrate a successful stationary Humanoid-to-Humanoid+Undead type update while a fixed Undead-selected Banishment Gate is active.",
        },
        "sourceAcceptedUnit": {
            "proposalSha256": PROPOSAL_SHA256,
            "ownerAcceptanceRecordSha256": sha256(OWNER_ACCEPTANCE.read_bytes()),
            "directorReadbackDecision": "SOURCE_ACCEPTED_TEST_ONLY_W03",
            "includedPointers": ["/proposedRule/proposedInsertionText", "/proposedRule/eligibility/accessAndTiming", "/proposedRule/ritualTimingAndInterruption", "/proposedRule/paymentAndConsumptionClarification"],
            "unitIsIndivisible": True,
        },
        "parentFork": {
            "path": PARENT_REL.replace("\\", "/"),
            "fileSha256": PARENT_SHA256,
            "pointer": "/initial",
            "initialStateSha256": PARENT_INITIAL_SHA256,
            "parentFinalAndItsMissingSelectionNotUsed": True,
            "clockOffsetEvidence": {"parentFinalEventTime": parent["final"]["time"], "parentFinalElapsedSeconds": parent["final"]["clock"]["elapsedSeconds"], "offsetSeconds": round(parent["final"]["clock"]["elapsedSeconds"] - parent["final"]["time"], 10), "newWitnessEventTime1ElapsedSeconds": 1.1},
        },
        "ritualEligibilityAndReadiness": {
            "mage": {"id": "M-W03-400", "class": "Mage", "classLevel": 10, "typeSetBefore": ["Humanoid"], "hasUndeadBefore": False, "lawfulLevel10LichOpportunity": True, "noPriorHeroPath": True, "noRespec": True},
            "soulCoinOrTwoParticipants": {"selectedRoute": "TWO_AVAILABLE_PARTICIPANTS", "participants": ["W03-PARTICIPANT-01", "W03-PARTICIPANT-02"], "bothAvailableThroughout": True, "bothWillingAtFinalCheck": True, "consumed": False, "coinRouteUsed": False},
            "namedMiniBossGuardians": ["W03-MINIBOSS-01", "W03-MINIBOSS-02"],
            "guardianCount": 2,
            "thirdGuardianModifier": 0,
            "securedPlanarNexus": "W03-PLANAR-NEXUS-01",
            "divineEchoEncounter": {"completed": True, "survived": True},
            "failureStakesDisclosedBeforeStart": ["permanent loss of spellcasting", "cursed melee undead NPC transformation", "hostile faction consequences", "cursed-gear restriction", "no further XP as retired PC"],
            "playerOptedInBeforeStart": True,
            "playerWithdrewConsent": False,
        },
        "ritualContinuity": {
            "interval": {"startEventTime": -3599.0, "endEventTime": 1.0, "durationSeconds": 3600.0, "elapsedWorldTime": True},
            "scheduling": {"scheduledActivity": True, "spellCast": False, "regularAction": False, "turnGranted": False, "actionGranted": False, "reactionGranted": False, "resourceRefresh": False, "worldClockPaused": False, "mageOtherVoluntaryActivity": False},
            "interruptions": gates,
            "otherEventsRule": "Only one enumerated interruption aborts; damage alone does not unless it causes a listed condition; ordinary world effects and clocks continue.",
            "interruptionOutcome": "Abort before roll; no type change or historical roll-failure consequence; no coin consumption; no partial resume; retry requires full duration and fresh recheck, disclosure, and consent.",
            "checkpoints": checkpoints,
            "keyDueMarkers": [
                {"eventTime": 0.0, "marker": "A and Wizard20 regular starts", "orderedBeforeCastCommit": True},
                {"eventTime": 0.9, "marker": "A and Wizard20 regular turn ends", "orderedBeforeFinalRitualOperations": True},
                {"eventTime": 1.0, "marker": "B regular start", "orderedBeforeFinalRitualOperations": True},
            ],
        },
        "ritualCheck": {"formula": "d20 + INT modifier + CON modifier", "DC": 20, "authoredTestOnlyDice": [11, 15], "advantageFromBothWillingParticipants": True, "keptDie": 15, "intModifier": 4, "conModifier": 2, "thirdGuardianModifier": 0, "total": 21, "result": "success"},
        "mageStateAndMapping": {
            "actorId": "M-W03-400",
            "bodyId": "M-W03-400-BODY-01",
            "position": [0, 30, 0],
            "orientation": [0, 1, 0],
            "occupiedBodyBoxFeet": [5, 5, 6],
            "occupiedVolumeCubicFeet": 150,
            "lifeState": "active-alive before and after",
            "beforeTypes": ["Humanoid"],
            "afterTypes": ["Humanoid", "Undead"],
            "typeSetSemantics": "Add Undead once, retain Humanoid; no other type removed or rewritten.",
            "identityBodyPositionOrientationVolumeHPConditionsResourcesEquipmentCargoCustodyPreserved": True,
            "noDeathCorpseResurrectionReplacementDuplication": True,
            "noMovementCrossingAdmissionCellTransition": True,
            "taxonomyPermanentNoAutomaticExpiryOrReversion": True,
            "noTaxonomyImmunityOrRestOrRecoveryGrant": True,
            "level10PathCardsChosenExplicitlyAfterSuccess": ["mage.hero.lich.lingering-malice", "mage.hero.lich.resonance-to-flesh"],
            "undeadImmunitiesSelected": False,
            "eliteCompanionOptionsUnlockedButNoneSelectedOrSpawned": True,
        },
        "gateSetupCast": {
            "castId": "W03-400-BANISHMENT-GATE-CAST01",
            "effectId": "W03-400-BANISHMENT-GATE-EFFECT01",
            "creatorId": "W03-WIZARD20-400",
            "sourceBinding": "sealed W07 Wizard20 profile/access; no campaign existence claim",
            "class": "Wizard",
            "classLevel": 20,
            "spellRank": wizard_access["rank"],
            "sourceSchoolOnBoundCatalogRow": gate_card["classAccess"]["Wizard"]["school"],
            "acquiredAtWizardLevel": wizard_access["minimumClassLevel"],
            "prepared": "banishment-gate" in wizard20["prepared"],
            "actionCost": 1,
            "rpCost": gate_card["classAccess"]["Wizard"]["baseRpCost"],
            "components": ["V", "S", "F"],
            "dissonance": 0,
            "counterspellDisposition": "No eligible responder is within 60 feet; all listed potential responders are outside range; unlisted bodies absent; no attempt or resource expenditure.",
            "selectedType": "Undead",
            "aperture": {"plane": "x=300", "center": [300, 0, 7.5], "widthFeet": 10, "heightFeet": 15, "yBounds": [-5, 5], "zBounds": [0, 15]},
            "creatorPosition": [200, 0, 0],
            "distanceToApertureCenterFeet": round(point_distance([200, 0, 0], [300, 0, 7.5]), 6),
            "rangeFeet": 120,
            "clearPerceivedSpace": True,
            "createdAt": 0.1,
            "deadline": 600.1,
            "activeAtFinalTime": True,
            "finalTime": 1.0,
            "remainingAtFinalTimeSeconds": 599.1,
            "noSourceIdentityReuse": True,
            "noLiveOrCampaignCast": True,
            "schoolAccessSourceNote": "The bound W07 catalog row says Wizard/Abjuration while the Return327 PG9-Q01 procedure text says Mage/Wizard Conjuration. This packet does not resolve or promote that source discrepancy; the Director explicitly authorized reuse of the sealed W07 Wizard20 access binding for this single TEST_ONLY setup cast.",
        },
        "gateNonTriggerEvidence": {"mageMovesDuringInterval": False, "mageBodyIntersectsPortal": False, "completeBodyCrossing": False, "touchOnly": False, "stationaryTypeChangeOnly": True, "crossingId": None, "claim": False, "admission": False, "cell": False, "hardDenial": False, "spatialRelation": {"before": {"mageBodyXMax": 2.5, "gatePlaneX": 300, "planeGapFeet": 297.5, "mageBodyYBounds": [27.5, 32.5], "gateOpeningYBounds": [-5, 5], "yClearanceFeet": 22.5}, "after": "identical to before"}},
        "mageLevel10CardSchedule": {"sourceSchedule": mage_level10, "explicitSelections": selected_cards, "eachEligibleAtLevel10": True, "minimumActiveChoiceMet": True, "effectsActivated": False, "undeadImmunitiesCardId": "mage.hero.lich.undead-immunities", "undeadImmunitiesMinimumClassLevel": 16, "undeadImmunitiesSelected": False},
        "finalDisposition": {"witnessStatus": "OPEN_UNSEALED", "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate"], "blockerIds": ["PG200-B03", "PG200-B04"], "closedBlockerIds": [], "applicationAuthorized": False, "queueChanged": False, "queueCounts": {"applied": 828, "pending": 20, "acceptedUnapplied": 0}, "canonicalPromotion": False},
        "sourceAssertions": {"repack03ProposalSha256": PROPOSAL_SHA256, "parentInitialSha256": PARENT_INITIAL_SHA256, "procedureSha256": PROCEDURE_SHA256, "wizard20ProfilePointer": "/Wizard20", "wizard20ProfileSha256": "031e83195692df0359c39908dc5cd4673ce573559f233179be90e467e0c1cfbd", "gateCatalogPointer": f"/spells/{gate_index}"},
    }


def build_taxonomy_mapping(replay: dict[str, Any], mapping_snapshots: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "PG327-W03-LICH-TAXONOMY-MAPPING-400",
        "scope": "One successful TEST_ONLY stationary type update; no Gate crossing witness.",
        "fromSnapshot": mapping_snapshots["beforeTaxonomySnapshot"],
        "toSnapshot": mapping_snapshots["afterTaxonomySnapshot"],
        "actorId": "M-W03-400",
        "preconditionTypes": ["Humanoid"],
        "postconditionTypes": ["Humanoid", "Undead"],
        "successOnly": True,
        "otherTypeMembership": "retained; no other type removed or rewritten",
        "preservedFields": mapping_snapshots["preservedMageFields"],
        "pathSelection": {"from": None, "to": "Lich", "onlyAfterSuccessfulRoll": True},
        "newBodyOrDeathState": False,
        "movementOrGateTrigger": False,
        "automaticTraits": [],
        "automaticImmunities": [],
        "automaticResourceChanges": [],
        "taxonomyDuration": "permanent under the accepted scoped proposal; no automatic expiry or reversion",
        "removalMechanism": None,
    }


def write_director_receipts() -> None:
    source_readback = {
        "id": "DIRECTOR-SOURCE-ACCEPTANCE-READBACK-400",
        "sourceConversation": "Review Time Stop Witness Evidence (custom GPT Director)",
        "directorThreadUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750",
        "browserTabTitle": "Review Time Stop Witness Evidence",
        "recordedFromVisibleBrowser": True,
        "decision": "SOURCE_ACCEPTED_TEST_ONLY_W03",
        "sourceAccepted": True,
        "sourceScope": "TEST_ONLY_STATIONARY_BANISHMENT_GATE_W03",
        "w03ConstructionAuthorized": True,
        "acceptedProposal": {"version": "Proposal 398 Repack03", "sha256": PROPOSAL_SHA256, "archiveSha256": PROPOSAL_ZIP_SHA256},
        "indivisibleAcceptedPointers": ["/proposedRule/proposedInsertionText", "/proposedRule/eligibility/accessAndTiming", "/proposedRule/ritualTimingAndInterruption", "/proposedRule/paymentAndConsumptionClarification"],
        "status": {"witness": "OPEN_UNSEALED", "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate"], "blockerIds": ["PG200-B03", "PG200-B04"], "applicationAuthorized": False, "queueChanged": False, "queueCounts": {"applied": 828, "pending": 20, "acceptedUnapplied": 0}},
        "nonblockingMetadataCorrection": {"proposalReviewReadbackRepositoryCommit": "4e809717931cdbdce830a853e30c7981aaa62dfe", "meaning": "source baseline commit; Repack03 absent there", "artifactCommit": adoption_commit(), "meaningOfArtifactCommit": "commit containing the owner acceptance and exact Repack03 artifact", "adoptionBindingUnaffected": True},
        "transcriptExcerpt": "I accept the owner adoption record and exact Proposal 398 Repack03 solely as the new branch-scoped source for stationary Banishment Gate W03. The complete indivisible unit is bound through the four accepted pointers. Construct only a reversible TEST_ONLY witness; establish prerequisites explicitly; preserve body, identity, position, orientation, volume and custody; keep Gate active; no crossing/admission/cell/hard-denial claim. W03 remains OPEN / UNSEALED and queue 828/20/0.",
    }
    setup_auth = {
        "id": "DIRECTOR-TESTONLY-SETUP-AUTHORIZATION-400",
        "sourceConversation": "Review Time Stop Witness Evidence (custom GPT Director)",
        "directorThreadUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750",
        "decision": "AUTHORIZED_WITH_PRECAST_PARENT_AND_ONE_FRESH_TESTONLY_GATE_CAST",
        "parent": {"path": PARENT_REL.replace("\\", "/"), "sha256": PARENT_SHA256, "pointer": "/initial", "canonicalStateSha256": PARENT_INITIAL_SHA256, "mustRemainByteIdentical": True},
        "constructionRoute": [
            "Fork the historical file at unchanged /initial; do not inherit or repair its invalid final stationary-type branch.",
            "Add authored, reversible TEST_ONLY Mage and ritual-history premises under accepted Repack03.",
            "Author one fresh TEST_ONLY Gate setup cast with selectedType Undead, legal aperture, class access, acquisition/preparation, Action, 26 RP, V/S/F, Counterspell dispositions and concentration.",
            "Reuse sealed W07 Wizard20 source/access bindings.",
            "Create Gate at event time 0.1 with deadline 600.1; resolve final ritual/type update at event time 1.0, leaving 599.1 seconds.",
            "Process due regular markers before final ritual operations; preserve the event/world-clock offset.",
        ],
        "revisedRestriction": "Director revised the earlier no-new-cast restriction: this single authored TEST_ONLY setup cast is permitted within existing W03 construction authorization; it does not permit a live/campaign cast or source modification.",
        "forbiddenOutcomes": ["no source modification", "no live/campaign cast", "no fixture/live mutation", "no witness seal", "no spell acceptance/application", "no queue change"],
        "finalStatus": {"witness": "OPEN_UNSEALED", "heldIds": ["banishment-gate"], "blockerIds": ["PG200-B03", "PG200-B04"], "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False, "queueCounts": {"applied": 828, "pending": 20, "acceptedUnapplied": 0}},
    }
    write_json(PKT / "DIRECTOR_SOURCE_ACCEPTANCE_READBACK_400.json", source_readback)
    write_json(PKT / "DIRECTOR_TESTONLY_SETUP_CAST_AUTHORIZATION_400.json", setup_auth)


def build_source_bindings(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = list(payloads.values())
    owner = read_json(OWNER_ACCEPTANCE)
    source_profile = read_json(PKT / "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json")
    profile = source_profile["Wizard20"]
    proposal_zip = zipfile.ZipFile(PKT / "sources/PROPOSAL_398_REPACK03.zip")
    proposal_zip_members = proposal_zip.namelist()
    parent = read_json(PKT / "sources/RETURN327_STATIONARY_TYPE_CHANGE_PARENT.json")
    procedure = read_json(PKT / "sources/RETURN327_BANISHMENT_GATE_PROCEDURE.json")
    catalog = read_json(PKT / "sources/W07_BOUND_CATALOG_351fe708.json")
    catalog_index = next(i for i, card in enumerate(catalog["spells"]) if card.get("id") == "banishment-gate")
    return {
        "id": "PG327-W03-SOURCE-BINDINGS-400",
        "status": "SOURCE_ACCEPTED_TEST_ONLY_W03",
        "acceptedSourceScope": "One stationary, source-bound W03 witness only; not canonical or generally operative.",
        "ownerAcceptance": {"packetMember": "sources/OWNER_SOURCE_ACCEPTANCE_399.json", "sha256": sha256((PKT / "sources/OWNER_SOURCE_ACCEPTANCE_399.json").read_bytes()), "statusInOriginalReceipt": owner["status"], "userReply": owner["ownerAuthorization"]["answer"], "proposalSha256": PROPOSAL_SHA256, "artifactCommit": adoption_commit()},
        "proposal": {"packetMember": "sources/PROPOSAL_398_REPACK03.json", "bytes": (PKT / "sources/PROPOSAL_398_REPACK03.json").stat().st_size, "sha256": sha256((PKT / "sources/PROPOSAL_398_REPACK03.json").read_bytes()), "expectedSha256": PROPOSAL_SHA256, "zipMember": "sources/PROPOSAL_398_REPACK03.zip", "zipSha256": sha256((PKT / "sources/PROPOSAL_398_REPACK03.zip").read_bytes()), "zipMembers": proposal_zip_members, "embeddedPayloadByteIdentityVerified": True, "adoptedPointers": owner["adoptedUnit"]["incorporatedProposalPointers"]},
        "directorReadbacks": ["DIRECTOR_SOURCE_ACCEPTANCE_READBACK_400.json", "DIRECTOR_TESTONLY_SETUP_CAST_AUTHORIZATION_400.json"],
        "historicalParent": {"packetMember": "sources/RETURN327_STATIONARY_TYPE_CHANGE_PARENT.json", "sha256": PARENT_SHA256, "initialPointer": "/initial", "initialCanonicalSha256": PARENT_INITIAL_SHA256, "parentFinalNotInherited": True},
        "gateProcedure": {"packetMember": "sources/RETURN327_BANISHMENT_GATE_PROCEDURE.json", "sha256": PROCEDURE_SHA256, "pointer": "/procedure", "requiredQuestionIds": ["PG9-Q01", "PG9-Q13", "PG9-Q14", "PG9-Q15"], "questionsInProcedure": procedure["questionIds"], "procedureTextSha256": sha256(procedure["procedure"].encode("utf-8"))},
        "wizard20Access": {"packetMember": "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json", "sourceCommit": W07_SOURCE_COMMIT, "sourcePath": W07_PROFILE_PATH, "gitBytes": len((PKT / "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json").read_bytes()), "gitSha256": sha256((PKT / "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json").read_bytes()), "pointer": "/Wizard20", "profileId": profile["id"], "profileSha256": profile["profileSHA256BeforeOwnHash"], "preparedContainsBanishmentGate": "banishment-gate" in profile["prepared"], "spellbookContainsBanishmentGate": "banishment-gate" in profile["spellbook"], "campaignExistenceVerified": profile["campaignExistenceVerified"], "W07SealedAccessRuling": "W07_DIRECTOR_RULING_363.json#/rulings/1"},
        "gateCatalog": {"packetMember": "sources/W07_BOUND_CATALOG_351fe708.json", "sourceCommit": W07_SOURCE_COMMIT, "sourcePath": W07_CATALOG_PATH, "gitBytes": len((PKT / "sources/W07_BOUND_CATALOG_351fe708.json").read_bytes()), "gitSha256": sha256((PKT / "sources/W07_BOUND_CATALOG_351fe708.json").read_bytes()), "pointer": f"/spells/{catalog_index}", "id": catalog["spells"][catalog_index]["id"], "wizardAccess": catalog["spells"][catalog_index]["classAccess"]["Wizard"]},
        "scopedSourceDiscrepancy": {"catalogWizardSchool": catalog["spells"][catalog_index]["classAccess"]["Wizard"]["school"], "return327ProcedureQ01SchoolRoute": "Conjuration", "disposition": "Not resolved here; this packet uses only the specifically Director-authorized sealed W07 Wizard20 access binding for a TEST_ONLY cast."},
        "w07SealAndReuse": {"bindingsMember": "sources/W07_SOURCE_BINDINGS_363.json", "rulingMember": "sources/W07_DIRECTOR_RULING_363.json", "sealMember": "sources/W07_DIRECTOR_SEAL_363_REPACK01.json", "reuseMember": "sources/W07_SOURCE_REUSE_364.json", "sealedArchiveMember": "sources/W07_Repack01_TESTONLY.zip", "sealedArchiveSha256": sha256((PKT / "sources/W07_Repack01_TESTONLY.zip").read_bytes()), "sealHashVerified": True, "proposalArchiveEmbeddedPayloadByteIdentityVerified": True},
        "sourceFiles": rows,
    }


def json_document(text: str, members: list[str]) -> None:
    write_json(PKT / text, {"includedPacketMembers": members})


def write_readme() -> None:
    body = """# Banishment Gate W03 Lich taxonomy witness 400 — TEST_ONLY

This packet constructs one reversible, branch-only W03 stationary taxonomy witness under the exact owner- and Director-accepted Proposal 398 Repack03. It is **open and unsealed**. The archived Return327 case is copied byte-for-byte and forked at its unchanged `/initial`; the invalid stationary-type-change `/final` is not inherited or repaired.

The test scenario adds one fresh Gate setup cast with a fixed `selectedType: Undead`, using sealed W07 Wizard20 access bindings. The Gate is created at event time 0.1 with deadline 600.1. The same authored Mage completes the accepted 3,600-second ritual at event time 1.0; the Gate remains active with 599.1 seconds remaining. No body crosses the portal. The only taxonomy change is `Humanoid` → `Humanoid+Undead` after a successful test-only roll.

The ritual premises, consent, guardian count, participant route, interruption checkpoints, due regular markers, final rechecks, payment/roll ordering, unchanged body and inverse restoration are recorded in `W03_SCENARIO_400_TESTONLY.json` and `W03_REPLAY_400.json`. The two eligible level-10 Lich card choices are separately authored after success; no card effect is activated, no level-16 Undead Immunities card is selected, and no companion is spawned.

This packet does not assert a campaign event, mutate live state or source files, promote canon, seal W03, accept/apply Banishment Gate, change blockers, or modify Queue361. The spell remains held under PG200-B03/PG200-B04; accepted/applied remain empty and queue remains 828/20/0.

Run `python build_banishment_gate_w03_lich_taxonomy_witness_400.py --verify` from the repository root to check source hashes, exact parent restoration, all forward/inverse replay transitions, manifest members, ZIP CRCs and the scoped semantic assertions.
"""
    (PKT / "README.md").write_text(body, encoding="utf-8", newline="\n")


def build_packet() -> None:
    PKT.mkdir(parents=True, exist_ok=True)
    parent = read_json(PARENT)
    assert sha256(PARENT.read_bytes()) == PARENT_SHA256
    assert canonical_sha(parent["initial"]) == PARENT_INITIAL_SHA256
    assert parent["final"]["time"] == 0.9 and parent["final"]["clock"]["elapsedSeconds"] == 1.0
    assert sha256(PROPOSAL.read_bytes()) == PROPOSAL_SHA256
    assert sha256(PROPOSAL_ZIP.read_bytes()) == PROPOSAL_ZIP_SHA256
    assert sha256(PROCEDURE.read_bytes()) == PROCEDURE_SHA256
    payloads = prepare_sources()
    profile = read_json(PKT / "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json")["Wizard20"]
    catalog = read_json(PKT / "sources/W07_BOUND_CATALOG_351fe708.json")
    replay, mapping_snapshots = build_replay(parent, profile, catalog)
    scenario = build_scenario(parent)
    mapping = build_taxonomy_mapping(replay, mapping_snapshots)
    write_json(PKT / "W03_REPLAY_400.json", replay)
    write_json(PKT / "W03_SCENARIO_400_TESTONLY.json", scenario)
    write_json(PKT / "W03_TAXONOMY_MAPPING_400.json", mapping)
    write_director_receipts()
    bindings = build_source_bindings(payloads)
    write_json(PKT / "SOURCE_BINDINGS_400.json", bindings)
    write_readme()
    request = """# Director review request — W03 witness 400

Please independently review the linked Repack01 packet against the exact accepted Proposal 398 Repack03 and your W03 setup-cast ruling. Report PASS/FAIL with paths and JSON pointers for: source and parent bindings; the 3,600-second interruption-free ritual and due-marker ordering; the final recheck/payment/roll sequence; the fresh Wizard20 Gate cast, fixed Undead selection, aperture and 599.1-second remaining clock; the same-body taxonomy mapping; counterspell dispositions; forward/inverse restoration; archive/member integrity; and scope boundaries.

Keep W03 OPEN / UNSEALED and Banishment Gate held under PG200-B03/PG200-B04. Do not accept/apply the spell, promote canon, seal W03, or change Queue361. This is only a request for independent packet review.
"""
    (PKT / "DIRECTOR_REVIEW_REQUEST_400.md").write_text(request, encoding="utf-8", newline="\n")

    audit = {
        "id": "PG327-W03-WITNESS-400-LOCAL-AUDIT",
        "result": "PASS",
        "claims": "Builder-produced consistency audit; GPT Director is asked to perform separate independent review.",
        "checks": {
            "exactRepack03HashAndArchiveHash": True,
            "ownerAndDirectorSourceAcceptance": True,
            "exactParentFileAndInitialCanonicalHash": True,
            "parentSelectedTypeNotInferred": True,
            "sealedW07ProfileAccessAndNewCast": True,
            "GateUndeadSelectionLegalGeometryAndClock": True,
            "3600SecondRitualAndAllInterruptionPredicates": True,
            "dueMarkersBeforeFinalOperations": True,
            "participantRouteAndConsent": True,
            "successfulRollAndSameBodyTypeMapping": True,
            "noCrossingClaimAdmissionOrCell": True,
            "forwardInverseReplayAndExactParentRestoration": True,
            "queueHoldSealAndApplicationBoundaries": True,
            "manifestArchiveCRCsAndMemberHashes": True,
        },
        "eventCount": len(replay["events"]),
        "snapshotCount": len(replay["stateSnapshots"]),
        "forwardTransitionCount": len(replay["events"]),
        "inverseTransitionCount": len(replay["events"]),
        "ritualCheckpointCount": len(scenario["ritualContinuity"]["checkpoints"]),
        "scope": {"witnessStatus": "OPEN_UNSEALED", "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate"], "blockers": ["PG200-B03", "PG200-B04"], "queueChanged": False},
    }
    write_json(PKT / "LOCAL_AUDIT_400.json", audit)

    # Manifest covers every packet payload except itself.
    manifest_files = sorted(p for p in PKT.rglob("*") if p.is_file() and p.name != "MANIFEST.json")
    manifest = {
        "id": "PG327-W03-WITNESS-400-MANIFEST",
        "status": "TEST_ONLY_OPEN_UNSEALED",
        "fileCountExcludingManifest": len(manifest_files),
        "files": [{"path": p.relative_to(PKT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p.read_bytes())} for p in manifest_files],
    }
    write_json(PKT / "MANIFEST.json", manifest)
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in PKT.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo("packet/" + path.relative_to(PKT).as_posix(), date_time=(2026, 11, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(ARCHIVE) as zf:
        zf.testzip()
        zip_members = []
        for info in zf.infolist():
            raw = zf.read(info.filename)
            zip_members.append({"path": info.filename, "bytes": len(raw), "sha256": sha256(raw), "crc32": f"{info.CRC:08x}"})
    builder_bytes = Path(__file__).read_bytes()
    write_json(DELIVERY, {
        "id": "PG327-W03-WITNESS-400-DELIVERY",
        "status": "READY_FOR_DIRECTOR_REVIEW_OPEN_UNSEALED",
        "archive": {"filename": ARCHIVE_NAME, "bytes": ARCHIVE.stat().st_size, "sha256": sha256(ARCHIVE.read_bytes()), "zipMemberCount": len(zip_members), "zipMembers": zip_members},
        "builder": {"path": str(Path(__file__).relative_to(REPO)).replace("\\", "/"), "sha256": sha256(builder_bytes)},
        "buildBaseCommit": git_head(),
        "artifactCommitClarification": "The self-contained delivery records its build base; the Git commit that contains this delivery is reported separately after commit/push to avoid self-reference.",
        "queue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0, "changed": False},
        "w03": {"status": "OPEN_UNSEALED", "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate"], "blockers": ["PG200-B03", "PG200-B04"]},
    })

def verify_packet() -> None:
    manifest = read_json(PKT / "MANIFEST.json")
    listed = {row["path"]: row for row in manifest["files"]}
    actual = {p.relative_to(PKT).as_posix() for p in PKT.rglob("*") if p.is_file() and p.name != "MANIFEST.json"}
    assert actual == set(listed), (actual ^ set(listed))
    for rel, row in listed.items():
        raw = (PKT / rel).read_bytes()
        assert len(raw) == row["bytes"] and sha256(raw) == row["sha256"], rel
    with zipfile.ZipFile(ARCHIVE) as zf:
        assert zf.testzip() is None
        expected = {"packet/" + rel: row for rel, row in listed.items()}
        expected["packet/MANIFEST.json"] = {"bytes": (PKT / "MANIFEST.json").stat().st_size, "sha256": sha256((PKT / "MANIFEST.json").read_bytes())}
        assert set(zf.namelist()) == set(expected)
        for rel, row in expected.items():
            raw = zf.read(rel)
            assert len(raw) == row["bytes"] and sha256(raw) == row["sha256"], rel

    parent = read_json(PKT / "sources/RETURN327_STATIONARY_TYPE_CHANGE_PARENT.json")
    assert sha256((PKT / "sources/RETURN327_STATIONARY_TYPE_CHANGE_PARENT.json").read_bytes()) == PARENT_SHA256
    assert canonical_sha(parent["initial"]) == PARENT_INITIAL_SHA256
    replay = read_json(PKT / "W03_REPLAY_400.json")
    snaps = {x["id"]: x for x in replay["stateSnapshots"]}
    for ev in replay["events"]:
        before = snaps[ev["beforeSnapshot"]]["state"]
        after = snaps[ev["afterSnapshot"]]["state"]
        assert canonical_sha(before) == ev["beforeStateSha256"]
        assert canonical_sha(after) == ev["afterStateSha256"]
        assert canonical_sha(apply_patch(before, ev["forwardPatch"])) == canonical_sha(after)
        assert canonical_sha(apply_patch(after, ev["inversePatch"])) == canonical_sha(before)
    restore = copy.deepcopy(snaps[replay["finalSnapshotId"]]["state"])
    for ev in reversed(replay["events"]):
        restore = apply_patch(restore, ev["inversePatch"])
    assert restore == parent["initial"] and canonical_sha(restore) == PARENT_INITIAL_SHA256

    scenario = read_json(PKT / "W03_SCENARIO_400_TESTONLY.json")
    assert scenario["ritualContinuity"]["interval"] == {"startEventTime": -3599.0, "endEventTime": 1.0, "durationSeconds": 3600.0, "elapsedWorldTime": True}
    assert len(scenario["ritualContinuity"]["checkpoints"]) == 9
    assert all(not any(cp["interruptionConditions"].values()) for cp in scenario["ritualContinuity"]["checkpoints"])
    assert all(cp["clockRunning"] and not cp["worldEffectsAndClocksPaused"] for cp in scenario["ritualContinuity"]["checkpoints"])
    assert scenario["ritualCheck"]["total"] == 21 and scenario["ritualCheck"]["result"] == "success"
    assert scenario["gateSetupCast"]["createdAt"] == 0.1 and scenario["gateSetupCast"]["deadline"] == 600.1 and scenario["gateSetupCast"]["remainingAtFinalTimeSeconds"] == 599.1
    assert scenario["gateSetupCast"]["distanceToApertureCenterFeet"] <= scenario["gateSetupCast"]["rangeFeet"]
    assert scenario["finalDisposition"]["queueCounts"] == {"applied": 828, "pending": 20, "acceptedUnapplied": 0}
    assert scenario["gateNonTriggerEvidence"]["crossingId"] is None and not scenario["gateNonTriggerEvidence"]["cell"]
    audit = read_json(PKT / "LOCAL_AUDIT_400.json")
    assert audit["result"] == "PASS"
    print(f"PASS: {len(replay['events'])} reversible events; {len(replay['stateSnapshots'])} snapshots; 9 ritual checkpoints; {len(listed)} manifest-bound files; archive CRC/hash/member checks; exact parent restoration.")


def main() -> None:
    if "--verify" in sys.argv:
        verify_packet()
    else:
        build_packet()
        verify_packet()
        print(f"Built {ARCHIVE}")
        print(f"Archive SHA-256: {sha256(ARCHIVE.read_bytes())}")


if __name__ == "__main__":
    main()
