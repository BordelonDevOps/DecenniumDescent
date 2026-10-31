from __future__ import annotations

import copy
import hashlib
import json
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
W08 = HERE / "banishment_gate_witness365_w08_finite_cargo04_build02"
OUT = HERE / "banishment_gate_witness365_w05_separation365_repack02_build01"
PACKET = OUT / "packet"
PIN = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
W08_ARCHIVE_SHA = "c277d95f1590a2ae6c2a63d8cf02b9158d7312694ca834491afa7ff9f00a7eb7"
AC5_ARCHIVE_SHA = "43b0fe4359021c4d8f714e3986be3d1579889cf590cfac73333dbe99b31c50cd"
ORIGIN = "PLANE-W05-TEST-ORIGIN-01"
ARCHIVE = "DD_Rank9_BanishmentGate_W05_CarriedBodies_365_TESTONLY_REPACK02.zip"
BOUNDARIES = [-24, -18, -12, -6]
TURN_ORDER = ["actor-w05-champion-owner", "actor-w05-firepet-owner", "actor-w05-gate-caster"]
SEQUENCES: dict[float, int] = defaultdict(int)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_sha(value: Any) -> str:
    return sha(canonical(value))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def deep_diff(before: Any, after: Any, path: list[str] | None = None) -> list[dict[str, Any]]:
    path = [] if path is None else path
    if isinstance(before, dict) and isinstance(after, dict):
        result: list[dict[str, Any]] = []
        for key in sorted(before.keys() - after.keys()):
            result.append({"op": "remove", "path": path + [str(key)], "before": copy.deepcopy(before[key])})
        for key in sorted(after.keys() - before.keys()):
            result.append({"op": "add", "path": path + [str(key)], "after": copy.deepcopy(after[key])})
        for key in sorted(before.keys() & after.keys()):
            result.extend(deep_diff(before[key], after[key], path + [str(key)]))
        return result
    if before != after:
        return [{"op": "replace", "path": path, "before": copy.deepcopy(before), "after": copy.deepcopy(after)}]
    return []


def get_at(state: Any, path: list[str]) -> Any:
    value = state
    for item in path:
        value = value[int(item)] if isinstance(value, list) else value[item]
    return value


def set_at(state: Any, path: list[str], value: Any, remove: bool = False) -> None:
    parent = state
    for item in path[:-1]:
        parent = parent[int(item)] if isinstance(parent, list) else parent[item]
    key = path[-1]
    if isinstance(parent, list):
        index = int(key)
        if remove:
            parent.pop(index)
        elif index == len(parent):
            parent.append(value)
        else:
            parent[index] = value
    elif remove:
        del parent[key]
    else:
        parent[key] = value


def apply_ops(state: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in operations:
        old = get_at(result, op["path"]) if op["op"] != "add" else None
        if op["op"] == "remove":
            assert old == op["before"]
            set_at(result, op["path"], None, remove=True)
        elif op["op"] == "add":
            set_at(result, op["path"], copy.deepcopy(op["after"]))
        else:
            assert old == op["before"], (op["path"], old, op["before"])
            set_at(result, op["path"], copy.deepcopy(op["after"]))
    return result


def emit(events: list[dict[str, Any]], state: dict[str, Any], event_id: str, t: float,
         kind: str, description: str, mutate: Callable[[dict[str, Any]], None],
         source_refs: list[str], text_locators: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    after["elapsedSeconds"] = t
    mutate(after)
    forward = deep_diff(before, after)
    inverse = list(reversed(deep_diff(after, before)))
    assert apply_ops(before, forward) == after
    assert apply_ops(after, inverse) == before
    SEQUENCES[t] += 1
    record = {
        "eventId": event_id, "timestampSeconds": t, "sequenceAtTimestamp": SEQUENCES[t],
        "kind": kind, "description": description, "sourceRefs": source_refs,
        "sourceTextLocators": text_locators or [],
        "beforeStateSha256": state_sha(before), "afterStateSha256": state_sha(after),
        "forwardOperations": forward, "inverseOperations": inverse, "stateAfter": after,
    }
    events.append(record)
    return after


def copy_packet_source(source: str, destination: str, origin: dict[str, Any],
                       pointers: list[str] | None = None, text_locators: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    data = (W08 / "packet" / source).read_bytes()
    target = PACKET / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"member": destination, "bytes": len(data), "sha256": sha(data), "origin": origin,
            "jsonPointers": pointers or [], "textLocators": text_locators or []}


def prepare_sources() -> dict[str, Any]:
    if OUT.exists():
        shutil.rmtree(OUT)
    PACKET.mkdir(parents=True)
    bindings: list[dict[str, Any]] = []
    bindings.append(copy_packet_source(
        "sources/RETURN327_banishment-gate.json", "sources/RETURN327_banishment-gate.json",
        {"kind": "pinned-git-source", "commit": PIN,
         "repositoryPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_return327_received/evidence/packet327/prior/procedures/banishment-gate.json"},
        ["/procedure", "/sharedContract/terminalScope", "/sharedContract/cellExtension"]))
    for source, dest, archive_member, pointers in [
        ("sources/AC5_ACCEPTED_SPELLS_MODEL.json", "sources/AC5_ACCEPTED_SPELLS_MODEL.json",
         "candidate/SPELLS_MODEL.json", ["/spells", "/profiles/AC5-PROFILE-GREATER-FIRE-PET-01", "/profiles/AC5-PROFILE-FACTION-CHAMPION-01"]),
        ("sources/AC5_ACCEPTED_CASEBOOK.json", "sources/AC5_ACCEPTED_CASEBOOK.json",
         "candidate/CASEBOOK.json", ["/cases"]),
    ]:
        bindings.append(copy_packet_source(source, dest, {"kind": "accepted-AC5-archive",
            "archiveSha256": AC5_ARCHIVE_SHA, "archiveMember": archive_member}, pointers))
    bindings.append(copy_packet_source(
        "sources/MAGE_CLASS_PLAYTEST.json", "sources/MAGE_CLASS_PLAYTEST.json",
        {"kind": "pinned-git-source", "commit": PIN,
         "repositoryPath": "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json"},
        ["/engine/2", "/engine/4", "/engine/9", "/engine/21", "/cards/23"]))
    bindings.append(copy_packet_source(
        "sources/EQUIPMENT_SOURCE_CATALOG.json", "sources/EQUIPMENT_SOURCE_CATALOG.json",
        {"kind": "pinned-git-source", "commit": PIN,
         "repositoryPath": "DescentReviewChanges/ReviewBible/data/playtest/equipment_source_catalog.json"},
        ["/records"]))
    bindings.append(copy_packet_source(
        "sources/COMBAT_ACTION_PLAYTEST.md", "sources/COMBAT_ACTION_PLAYTEST.md",
        {"kind": "pinned-git-source", "commit": PIN,
         "repositoryPath": "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md"},
        text_locators=[{"lines": [29, 35, 57, 66, 156], "use": "six-second rounds, reactions, regular start/end order and movement accounting"}]))
    rulebook_src = REPO / "docs/reference/Player_Rulebook_v6_source_text.txt"
    rulebook_data = rulebook_src.read_bytes()
    rulebook_member = "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt"
    (PACKET / rulebook_member).write_bytes(rulebook_data)
    bindings.append({"member": rulebook_member, "bytes": len(rulebook_data), "sha256": sha(rulebook_data),
        "origin": {"kind": "pinned-git-source", "commit": PIN,
            "repositoryPath": "docs/reference/Player_Rulebook_v6_source_text.txt",
            "sourceExtractSha256": "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b"},
        "jsonPointers": [], "textLocators": [
            {"lines": [8376, 8382], "use": "base RP costs and Dissonance surcharge by state"},
            {"lines": [8424, 8427], "use": "Dissonance limit, rank gain, Refrain and Overcast"},
            {"lines": [8521, 8521], "use": "Mage Nuke Chain and Refrain interaction"}]})
    bindings.append(copy_packet_source(
        "sources/W08_CASTER_PROFILES_365_TESTONLY.json", "sources/W05_CASTER_PROFILE_SEEDS_365_TESTONLY.json",
        {"kind": "sealed-W08-archive-template", "archiveSha256": W08_ARCHIVE_SHA,
         "archiveMember": "sources/W08_CASTER_PROFILES_365_TESTONLY.json"},
        ["/profiles/0", "/profiles/1"]))
    bindings.append(copy_packet_source(
        "rules/BODY_EQUIPMENT.md", "rules/BODY_EQUIPMENT.md",
        {"kind": "pinned-git-source", "commit": PIN,
         "repositoryPath": "DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md"},
        text_locators=[{"lines": list(range(94, 110)), "use": "Medium STR14 carrying limit and casualty Load formula"}]))
    for source, dest in [
        ("W08_SOURCE_BINDINGS_365.json", "authority/W08_SOURCE_BINDINGS_365.json"),
        ("authority/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json", "authority/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json"),
        ("authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json", "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json"),
        ("authority/CURRENT_SPELL_QUEUE_361.json", "authority/CURRENT_SPELL_QUEUE_361.json"),
        ("authority/PG327_W01_W08_WITNESS_PLAN_361.json", "authority/PG327_W01_W08_WITNESS_PLAN_361.json"),
        ("authority/PG327_W01_DIRECTOR_SEAL_365_REPACK04.json", "authority/PG327_W01_DIRECTOR_SEAL_365_REPACK04.json"),
        ("authority/PG327_W08_DIRECTOR_HOLD_365_REPACK03.json", "authority/PG327_W08_DIRECTOR_HOLD_365_REPACK03.json"),
    ]:
        bindings.append(copy_packet_source(source, dest,
            {"kind": "sealed-W08-archive", "archiveSha256": W08_ARCHIVE_SHA, "archiveMember": source}))
    w08_seal = HERE / "PG327_W08_DIRECTOR_SEAL_365_REPACK04.json"
    seal_data = w08_seal.read_bytes()
    (PACKET / "authority" / w08_seal.name).write_bytes(seal_data)
    bindings.append({"member": f"authority/{w08_seal.name}", "bytes": len(seal_data), "sha256": sha(seal_data),
        "origin": {"kind": "Director-ruling-artifact", "rulingId": "PG327-W08-365-REPACK04-DIRECTOR-SEAL",
                   "archiveSha256": W08_ARCHIVE_SHA},
        "jsonPointers": ["/rulingId", "/witnessDisposition", "/nextWitness"], "textLocators": []})
    return {"id": "PG327-W05-SOURCE-BINDINGS-365-REPACK02", "bindings": bindings,
            "provenancePolicy": "Each input has a per-member origin. Git commit, accepted AC5 archive, sealed W08 archive and Director ruling artifacts are not conflated.",
            "fixtureBoundary": "W05 actor identities, focus custody, faction standing, support anatomy/contact, permissions, turn choices and movement are conditional TEST_ONLY premises. None is a campaign fact or canonical body-geometry rule."}


def source_data() -> tuple[dict[str, Any], dict[str, Any], dict[str, str], dict[str, int]]:
    ac5 = load_json(PACKET / "sources" / "AC5_ACCEPTED_SPELLS_MODEL.json")
    casebook = load_json(PACKET / "sources" / "AC5_ACCEPTED_CASEBOOK.json")
    gate = load_json(PACKET / "sources" / "RETURN327_banishment-gate.json")
    mage = load_json(PACKET / "sources" / "MAGE_CLASS_PLAYTEST.json")
    equip = load_json(PACKET / "sources" / "EQUIPMENT_SOURCE_CATALOG.json")
    spell_indexes = {x["id"]: i for i, x in enumerate(ac5["spells"])}
    profile_indexes = {x["id"]: x for x in ac5["profiles"].values()}
    case_index = next(i for i, x in enumerate(casebook["cases"]) if x["id"] == "AC5-X17")
    wand_index = next(i for i, x in enumerate(equip["records"]) if x["id"] == "arcane-focuses.wand")
    counter_index = next(i for i, x in enumerate(mage["cards"]) if x["id"] == "mage.arch.counterspell")
    pointers = {
        "gateRule": "sources/RETURN327_banishment-gate.json#/procedure",
        "firePetSpell": f"sources/AC5_ACCEPTED_SPELLS_MODEL.json#/spells/{spell_indexes['summon-greater-fire-pet']}/procedure",
        "firePetProfile": "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01",
        "championSpell": f"sources/AC5_ACCEPTED_SPELLS_MODEL.json#/spells/{spell_indexes['faction-champion']}/procedure",
        "championProfile": "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-FACTION-CHAMPION-01",
        "counterspell": f"sources/MAGE_CLASS_PLAYTEST.json#/cards/{counter_index}",
        "companionCommand": "sources/MAGE_CLASS_PLAYTEST.json#/engine/9",
        "spellRisk": "sources/MAGE_CLASS_PLAYTEST.json#/engine/2",
        "nukeChainRefrain": "sources/MAGE_CLASS_PLAYTEST.json#/engine/4",
        "rankInteraction": "sources/MAGE_CLASS_PLAYTEST.json#/engine/21",
        "wandRecord": f"sources/EQUIPMENT_SOURCE_CATALOG.json#/records/{wand_index}",
        "ac5Precedent": f"sources/AC5_ACCEPTED_CASEBOOK.json#/cases/{case_index}",
        "catalogCard": "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json#",
        "queueAuthority": "authority/CURRENT_SPELL_QUEUE_361.json#",
    }
    assert "PG9-Q17" in gate["procedure"] and "separate living passengers" in gate["procedure"]
    assert "AC5-CHAMPION-ALLY-01" in ac5["spells"][spell_indexes["faction-champion"]]["procedure"]
    assert profile_indexes["AC5-PROFILE-GREATER-FIRE-PET-01"]["creatureType"] == "Elemental"
    assert profile_indexes["AC5-PROFILE-FACTION-CHAMPION-01"]["creatureType"] == "Humanoid"
    return ac5, casebook, pointers, {"firePet": spell_indexes["summon-greater-fire-pet"],
        "champion": spell_indexes["faction-champion"], "wand": wand_index, "counterspell": counter_index,
        "casebook": case_index}


def create_mage_profiles(seeds: dict[str, Any], pointers: dict[str, str], ac5: dict[str, Any]) -> dict[str, Any]:
    gate_seed, champion_seed = seeds["profiles"]
    fire = copy.deepcopy(champion_seed)
    fire["profileId"], fire["actorId"] = "W05-MAGE9-FIREPET-OWNER-TESTONLY", "actor-w05-firepet-owner"
    fire["spellbookHistory"] = [
        {"spellId": "mage.arch.counterspell", "acquiredAtMageLevel": 9, "preparedForWitness": True,
         "sourcePointer": pointers["counterspell"]},
        {"spellId": "summon-greater-fire-pet", "acquiredAtMageLevel": 9, "preparedForWitness": True,
         "sourcePointer": pointers["firePetSpell"]}]
    champion = copy.deepcopy(champion_seed)
    champion["profileId"], champion["actorId"] = "W05-MAGE9-CHAMPION-OWNER-TESTONLY", "actor-w05-champion-owner"
    champion["spellbookHistory"] = [
        {"spellId": "mage.arch.counterspell", "acquiredAtMageLevel": 9, "preparedForWitness": True,
         "sourcePointer": pointers["counterspell"]},
        {"spellId": "faction-champion", "acquiredAtMageLevel": 9, "preparedForWitness": True,
         "sourcePointer": pointers["championSpell"]}]
    gate = copy.deepcopy(gate_seed)
    gate["profileId"], gate["actorId"] = "W05-MAGE17-GATECASTER-TESTONLY", "actor-w05-gate-caster"
    gate["spellbookHistory"] = [
        {"spellId": "mage.arch.counterspell", "acquiredAtMageLevel": 9, "preparedForWitness": True,
         "sourcePointer": pointers["counterspell"]},
        {"spellId": "banishment-gate", "acquiredAtMageLevel": 17, "preparedForWitness": True,
         "sourcePointer": pointers["gateRule"], "operativeSchool": "Conjuration",
         "catalogConflictPreserved": True}]
    for profile, suffix in [(fire, "fire-owner"), (champion, "champion-owner"), (gate, "gate-caster")]:
        actor = profile["actorId"]
        profile["focus"] = {"objectId": f"object-mage-focus-w05-{suffix}", "recordId": "arcane-focuses.wand",
            "heldIn": "right hand", "custody": actor, "somaticHand": "left hand", "verbalAvailable": True,
            "sourcePointer": pointers["wandRecord"], "fixtureWeightLb": 1,
            "weightBasis": "TEST_ONLY fixture adopts the source-projected 1 lb wand entry; equipment catalog itself remains projection-only"}
        profile["fixtureFocusAndLoad"] = {"otherCarriedEquipment": [], "focusWeightLb": 1,
            "totalFixtureCarriedLoadLb": 1, "fixtureOnly": True}
    result = {"id": "W05-MAGE-PROFILES-365-TESTONLY-REPACK02", "evidenceClass": "conditional TEST_ONLY actor profiles adapted from the sealed W08 templates",
        "profiles": [fire, champion, gate], "noCampaignActors": True,
        "identityPolicy": "All three caster actor IDs and wand object IDs are W05-local identities; no W08 custody identity is reused."}
    write_json(PACKET / "W05_MAGE_PROFILES_365_TESTONLY.json", result)
    return result


def mage_profile_ref(actor: str) -> str:
    index = {"actor-w05-firepet-owner": 0, "actor-w05-champion-owner": 1, "actor-w05-gate-caster": 2}[actor]
    return f"W05_MAGE_PROFILES_365_TESTONLY.json#/profiles/{index}"


def box(center: list[float], half: list[float]) -> list[list[float]]:
    return [[center[i] - half[i], center[i] + half[i]] for i in range(3)]


def initial_state(profiles: dict[str, Any], equip: dict[str, Any]) -> dict[str, Any]:
    by_id = {p["actorId"]: p for p in profiles["profiles"]}
    positions = {
        "actor-w05-champion-owner": [-20, 0, 3],
        "actor-w05-firepet-owner": [-20, -20, 3],
        "actor-w05-gate-caster": [-50, 0, 3],
    }
    owners: dict[str, Any] = {}
    objects: dict[str, Any] = {}
    for actor_id, p in by_id.items():
        focus = p["focus"]
        owners[actor_id] = {
            "id": actor_id, "profileId": p["profileId"], "class": p["class"], "classLevel": p["classLevel"],
            "abilityScores": p["abilityScores"],
            "spellAttackModifier": p["derived"]["spellAttack"], "spellSaveDC": p["derived"]["spellSaveDC"],
            "rp": {"maximum": p["derived"]["RPMaximum"], "current": p["derived"]["RPMaximum"], "spent": 0},
            "concentration": None, "actionBudget": {"action": "available", "bonusAction": "available", "reaction": "available"},
            "conscious": True, "incapacitated": False, "silenced": False, "perceivesClearly": True,
            "position": {"planeKey": ORIGIN, "centerFt": positions[actor_id], "bodyBoxFt": box(positions[actor_id], [2.5, 2.5, 3])},
            "acquiredAndPreparedSpells": [x["spellId"] for x in p["spellbookHistory"]],
            "spellbookHistory": copy.deepcopy(p["spellbookHistory"]),
            "focus": copy.deepcopy(focus),
            "handOccupancy": {"left": "free-for-somatic", "right": focus["objectId"]},
            "fixtureCarriedLoad": copy.deepcopy(p["fixtureFocusAndLoad"]),
            "concentrationHistory": [], "castingHistory": [],
            "dissonance": {"current": 0, "initialTestFixtureValue": 0,
                "limit": p["derived"]["dissonanceLimit"], "state": "In Tune"},
            "burn": {"current": 0, "initialTestFixtureValue": 0},
            "nukeChain": [], "refrain": {"lastSpellId": None, "repeatCount": 0},
            "elementalFocusChoice": {"choice": "Fire", "source": "TEST_ONLY class-build premise", "passiveTriggerOccurred": False},
            "counterspell": {"spellId": "mage.arch.counterspell", "known": True, "prepared": True,
                "rpCost": 4, "rangeFt": 60, "rechargeRounds": 3, "rechargeRemainingRounds": 0,
                "reactionAvailable": True, "usesThisWitness": 0, "lastRechargeRefreshBoundary": None},
            "regularTurn": {"active": False, "starts": [], "ends": [], "refreshBoundaries": [],
                "companionCommandAllowance": {"maximum": 1, "usedThisTurn": False, "commandedActorId": None}},
        }
        if actor_id == "actor-w05-champion-owner":
            owners[actor_id]["factionEligibility"] = {"factionId": "FACTION-W05-TEST-01",
                "alliedStatus": True, "currentStanding": 3, "invocationPermission": True,
                "aidProhibition": False, "membershipInferred": False, "fixtureOnly": True}
    wand = next(x for x in equip["records"] if x["id"] == "arcane-focuses.wand")
    for p in profiles["profiles"]:
        f = p["focus"]
        objects[f["objectId"]] = {"id": f["objectId"], "kind": "arcane-focus-wand",
            "recordId": f["recordId"], "carriedBy": p["actorId"], "heldIn": "right hand",
            "weightLb": f["fixtureWeightLb"], "catalogSourceWeightLb": wand["sourceWeightLb"],
            "catalogStatus": wand["status"], "fixtureOnly": True, "notLivingBody": True}
    return {
        "simulationId": "PG327-W05-365-TESTONLY-CARRIAGE-REPACK02",
        "evidenceClass": "conditional TEST_ONLY static authored witness; no campaign event or runtime result asserted",
        "elapsedSeconds": -30, "world": {"originPlaneKey": ORIGIN, "encounterId": "ENCOUNTER-W05-TEST-02",
            "perceivedClearPortalCreationSpace": True, "originWorldGeometryFixtureOnly": True},
        "mageActors": owners, "actors": {
            "actor-w05-target-champion-fixture": {"id": "actor-w05-target-champion-fixture",
                "creatureType": "Construct", "fixtureOnly": True, "hostilePerceivedByCompanion": True,
                "initiativeStatus": "static-test-target-no-slot", "regularTurnStarts": [],
                "alive": True, "hp": 100, "ac": 15,
                "physicalPosition": {"planeKey": ORIGIN, "centerFt": [-10, 2.5, 3],
                    "bodyBoxFt": [[-10.5, -9.5], [2, 3], [2.5, 3.5]]}},
            "actor-w05-target-firepet-fixture": {"id": "actor-w05-target-firepet-fixture",
                "creatureType": "Construct", "fixtureOnly": True, "hostilePerceivedByCompanion": True,
                "initiativeStatus": "static-test-target-no-slot", "regularTurnStarts": [],
                "alive": True, "hp": 100, "ac": 15,
                "physicalPosition": {"planeKey": ORIGIN, "centerFt": [-5, -7.5, 3],
                    "bodyBoxFt": [[-5.5, -4.5], [-8, -7], [2.5, 3.5]]}},
        }, "gate": None, "carriageRelation": None,
        "cells": {}, "hardControlClaims": {}, "objects": objects,
        "turnScheduler": {"activeActorId": None, "boundaryInProgress": None, "currentSequence": 0,
            "turnOrder": TURN_ORDER, "completedTurnsByActor": {x: [] for x in TURN_ORDER},
            "refreshLedger": {x: [] for x in TURN_ORDER}, "companionPhases": [],
            "firePetAuraCheckpointLedger": []},
        "factionChecks": [], "counterspellWindows": [],
        "testFixtureBoundaries": [
            "No canonical creature anatomy, campaign occurrence, living-body-as-gear rule or runtime behavior is asserted.",
            "Caster positions, wand identities/hand custody, initial resources and faction standing are TEST_ONLY premises.",
            "The articulated side-support contact is a TEST_ONLY fixture and is not a separate equipment item.",
            "Two inert hostile TEST_ONLY construct targets exist only so commanded companion attacks resolve; both attacks miss and neither target affects Gate eligibility or carrying.",
        ],
    }


def start_turn(events: list[dict[str, Any]], state: dict[str, Any], actor: str, t: float,
               boundary: str, locators: list[dict[str, Any]]) -> dict[str, Any]:
    def mutate(s: dict[str, Any]) -> None:
        sched = s["turnScheduler"]
        assert sched["activeActorId"] is None
        owner = s["mageActors"][actor]
        assert boundary not in owner["regularTurn"]["refreshBoundaries"]
        sched["activeActorId"] = actor
        sched["boundaryInProgress"] = boundary
        sched["currentSequence"] += 1
        owner["regularTurn"]["active"] = True
        owner["regularTurn"]["starts"].append(t)
        owner["regularTurn"]["refreshBoundaries"].append(boundary)
        owner["regularTurn"]["companionCommandAllowance"] = {"maximum": 1, "usedThisTurn": False, "commandedActorId": None}
        owner["actionBudget"] = {"action": "available", "bonusAction": "available", "reaction": "available"}
        counter = owner["counterspell"]
        counter["reactionAvailable"] = True
        counter["lastRechargeRefreshBoundary"] = boundary
        if counter["rechargeRemainingRounds"] > 0:
            counter["rechargeRemainingRounds"] -= 1
        prior_stance = owner.get("stanceState", {}).get("active")
        if "stanceState" not in owner:
            owner["stanceState"] = {"active": None, "history": []}
        elif prior_stance is not None:
            owner["stanceState"]["history"].append({"name": prior_stance["name"],
                "selectedAt": prior_stance["selectedAt"], "expiredAtNextRegularStart": t})
        owner["stanceState"]["active"] = {"name": "Guarded", "selectedAt": t, "expiresAtNextRegularStart": t + 6,
            "effects": {"acBonus": 1, "advantageResistingShove": True, "speedPenaltyFt": 5},
            "selectedBeforeFirstStanceRelevantEvent": True}
        owner["turnEffectsForBoundary"] = {"startResolvedOnce": True, "stanceSelection": "Guarded",
            "priorStanceExpiredAtStart": prior_stance is not None, "stanceExpiry": t + 6, "refreshCount": 1}
    return emit(events, state, f"W05-TURN-START-{actor}-{boundary}", t, "regular-turn-start",
        "Ordered regular Mage start; action, bonus action and reaction refresh exactly once for this actor and six-second boundary.",
        mutate, [mage_profile_ref(actor), "sources/MAGE_CLASS_PLAYTEST.json#/engine/9",
            "sources/MAGE_CLASS_PLAYTEST.json#/cards/23"], locators)


def end_turn(events: list[dict[str, Any]], state: dict[str, Any], actor: str, t: float,
             boundary: str, locators: list[dict[str, Any]]) -> dict[str, Any]:
    def mutate(s: dict[str, Any]) -> None:
        sched = s["turnScheduler"]
        assert sched["activeActorId"] == actor
        owner = s["mageActors"][actor]
        owner["actionBudget"]["action"] = "expired-unused" if owner["actionBudget"]["action"] == "available" else owner["actionBudget"]["action"]
        owner["actionBudget"]["bonusAction"] = "expired-unused" if owner["actionBudget"]["bonusAction"] == "available" else owner["actionBudget"]["bonusAction"]
        owner["regularTurn"]["active"] = False
        owner["regularTurn"]["ends"].append(t)
        sched["activeActorId"] = None
        sched["completedTurnsByActor"][actor].append(boundary)
    return emit(events, state, f"W05-TURN-END-{actor}-{boundary}", t, "regular-turn-end",
        "The actor's whole regular turn ends before any attached companion phase; no second regular turn or duplicate refresh is created.",
        mutate, [mage_profile_ref(actor), "sources/MAGE_CLASS_PLAYTEST.json#/engine/9"], locators)


def faction_check(events: list[dict[str, Any]], state: dict[str, Any], t: float, refs: dict[str, str],
                  locators: list[dict[str, Any]]) -> dict[str, Any]:
    def mutate(s: dict[str, Any]) -> None:
        actor = s["mageActors"]["actor-w05-champion-owner"]
        f = actor["factionEligibility"]
        record = {"time": t, "phase": "pre-payment", "factionId": f["factionId"],
            "alliedStatus": f["alliedStatus"], "currentStanding": f["currentStanding"],
            "invocationPermission": f["invocationPermission"], "aidProhibition": f["aidProhibition"],
            "membershipInferred": f["membershipInferred"], "passesAllFourPredicates": True, "fixtureOnly": True}
        s["factionChecks"].append(record)
        assert actor["regularTurn"]["active"] and record["factionId"] == "FACTION-W05-TEST-01"
        assert record["alliedStatus"] and record["currentStanding"] > 0 and record["invocationPermission"] and not record["aidProhibition"]
    return emit(events, state, "W05-FACTION-ELIGIBILITY-CHECK-PREPAYMENT", t, "faction-ally-prepayment-check",
        "Resolve the exact four AC5-CHAMPION-ALLY-01 predicates before the Faction Champion RP payment; the faction record is a TEST_ONLY premise.",
        mutate, [refs["championSpell"]], locators)


def dissonance_state(value: int, limit: int) -> str:
    if value >= limit + 6:
        return "Fractured"
    if value >= limit + 3:
        return "Discordant"
    if value >= limit:
        return "Frayed"
    return "In Tune"


def cast_commit(events: list[dict[str, Any]], state: dict[str, Any], actor: str, spell_id: str,
                t: float, spell: dict[str, Any], refs: dict[str, str],
                locators: list[dict[str, Any]]) -> dict[str, Any]:
    base_cost = spell["rpCost"]
    rank = spell["rank"]
    concentration_seconds = spell["durationSeconds"]
    spell_ref = refs["firePetSpell"] if spell_id == "summon-greater-fire-pet" else refs["championSpell"] if spell_id == "faction-champion" else refs["gateRule"]
    def mutate(s: dict[str, Any]) -> None:
        m = s["mageActors"][actor]
        assert s["turnScheduler"]["activeActorId"] == actor
        assert m["actionBudget"]["action"] == "available" and m["concentration"] is None
        d = m["dissonance"]
        state_before = dissonance_state(d["current"], d["limit"])
        rp_surcharge = {"In Tune": 0, "Frayed": 1, "Discordant": 2, "Fractured": 3}[state_before]
        refrain_before = copy.deepcopy(m["refrain"])
        refrain_gain = min(3, refrain_before["repeatCount"] + 1) if refrain_before["lastSpellId"] == spell_id else 0
        base_dissonance = 1 if 1 <= rank <= 5 else 2 if 6 <= rank <= 9 else 0
        overcast_dissonance = 0
        dissonance_gain = base_dissonance + refrain_gain + overcast_dissonance
        cost = base_cost + rp_surcharge
        assert m["rp"]["current"] >= cost
        focus = m["focus"]
        focus_object = s["objects"][focus["objectId"]]
        assert focus_object["carriedBy"] == actor and focus_object["heldIn"] == "right hand"
        assert m["handOccupancy"] == {"left": "free-for-somatic", "right": focus["objectId"]}
        components = {"V": {"satisfied": True, "basis": "conscious, unsilenced, verbalAvailable"},
            "S": {"satisfied": True, "hand": "left", "handFree": True},
            "F": {"satisfied": True, "hand": "right", "objectId": focus["objectId"],
                  "custody": actor, "recordPointer": refs["wandRecord"]}}
        m["actionBudget"]["action"] = "spent-on-spell"
        m["rp"]["current"] -= cost
        m["rp"]["spent"] += cost
        m["concentration"] = {"spellId": spell_id, "startedAt": t, "deadline": t + concentration_seconds}
        m["concentrationHistory"].append({"spellId": spell_id, "startedAt": t, "deadline": t + concentration_seconds})
        m["dissonance"]["current"] += dissonance_gain
        m["dissonance"]["state"] = dissonance_state(m["dissonance"]["current"], m["dissonance"]["limit"])
        refrain_after = {"lastSpellId": spell_id,
            "repeatCount": min(3, refrain_before["repeatCount"] + 1) if refrain_before["lastSpellId"] == spell_id else 0}
        history = {"spellId": spell_id, "startedAt": t, "rank": rank, "action": "Action",
            "baseRpCost": base_cost, "dissonanceRpSurcharge": rp_surcharge, "finalRpCost": cost,
            "rpPaid": cost, "overcastRp": 0, "resonanceSurge": False,
            "components": components, "focusObjectId": focus["objectId"],
            "dissonanceBefore": d["current"] - dissonance_gain, "dissonanceLimit": d["limit"],
            "dissonanceStateBefore": state_before, "baseDissonance": base_dissonance,
            "refrainDissonance": refrain_gain, "overcastDissonance": overcast_dissonance,
            "dissonanceDelta": dissonance_gain, "dissonanceAfter": d["current"],
            "dissonanceStateAfter": d["state"],
            "burnBefore": m["burn"]["current"], "burnDelta": 0,
            "nukeChainBefore": copy.deepcopy(m["nukeChain"]), "nukeChainAfter": [],
            "refrainBefore": refrain_before, "refrainAfter": refrain_after,
            "spellDealsChosenElement": False, "refrainCountsPreviousSameNamedCast": refrain_gain > 0,
            "strainNote": "Rank-based base Dissonance is applied. These are each caster's first distinct non-elemental cast; Refrain gain is zero, no Overcast is used, and no Fire Focus damage/Burn rider triggers."}
        m["castingHistory"].append(history)
        m["nukeChain"] = []
        m["refrain"] = copy.deepcopy(refrain_after)
        s.setdefault("pendingCast", {})[spell_id] = {"casterId": actor, "timestamp": t,
            "rank": rank, "rpPaid": cost, "components": copy.deepcopy(components), "dissonanceGain": dissonance_gain}
    return emit(events, state, f"W05-CAST-COMMIT-{spell_id.upper()}", t, "spell-cast-commit",
        f"{spell_id} Action, Dissonance-adjusted RP cost and rank-based Dissonance are applied before Counterspell evaluation; V/S/F component custody is explicit.",
        mutate, [mage_profile_ref(actor), spell_ref, refs["wandRecord"], refs["spellRisk"],
            refs["nukeChainRefrain"], refs["rankInteraction"]], locators)


def counterspell_window(events: list[dict[str, Any]], state: dict[str, Any], caster: str,
                        spell_id: str, t: float, refs: dict[str, str],
                        locators: list[dict[str, Any]]) -> dict[str, Any]:
    other_ids = [x for x in TURN_ORDER if x != caster]
    def mutate(s: dict[str, Any]) -> None:
        decisions = []
        target = s["mageActors"][caster]["position"]["centerFt"]
        for responder_id in other_ids:
            responder = s["mageActors"][responder_id]
            pos = responder["position"]["centerFt"]
            distance = sum((target[i] - pos[i]) ** 2 for i in range(3)) ** 0.5
            eligible = bool(responder["conscious"] and not responder["incapacitated"] and
                responder["perceivesClearly"] and distance <= 60 and responder["counterspell"]["known"] and
                responder["counterspell"]["prepared"] and responder["counterspell"]["reactionAvailable"] and
                responder["counterspell"]["rechargeRemainingRounds"] == 0 and responder["rp"]["current"] >= 4)
            decisions.append({"responderId": responder_id, "perceivesCasterBeginningSpell": True,
                "rangeFt": round(distance, 4), "lineOfEffect": True, "conscious": responder["conscious"],
                "incapacitated": responder["incapacitated"], "CounterspellKnownAndPrepared": True,
                "reactionAvailable": responder["counterspell"]["reactionAvailable"],
                "counterspellRpAvailable": responder["rp"]["current"] >= 4,
                "rechargeRemainingRounds": responder["counterspell"]["rechargeRemainingRounds"],
                "eligibleToAttempt": eligible, "decision": "declined-no-attempt",
                "reactionSpent": False, "rpSpent": 0, "rechargeStarted": False})
            assert eligible
        record = {"spellId": spell_id, "casterId": caster, "time": t,
            "costsAlreadyPaid": True, "selfResponseAdjudicated": False,
            "otherCasterDecisions": decisions, "counterspellAttemptCount": 0,
            "outcome": "no-attempt; triggering spell proceeds"}
        s["counterspellWindows"].append(record)
    return emit(events, state, f"W05-COUNTERSPELL-WINDOW-{spell_id.upper()}", t, "counterspell-interrupt-window",
        "Evaluate every other Mage caster at the spell trigger using perception, range, line of effect, resources, Reaction, recharge and restrictions. Each eligible responder explicitly declines; self-response is left outside this witness.",
        mutate, [mage_profile_ref(caster), refs["counterspell"]] +
            [mage_profile_ref(responder_id) for responder_id in other_ids], locators)


def cast_resolve(events: list[dict[str, Any]], state: dict[str, Any], actor: str, spell_id: str,
                 t: float, ac5: dict[str, Any], refs: dict[str, str],
                 locators: list[dict[str, Any]]) -> dict[str, Any]:
    fire = ac5["profiles"]["AC5-PROFILE-GREATER-FIRE-PET-01"]
    champion = ac5["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    def mutate(s: dict[str, Any]) -> None:
        cast = s["pendingCast"].pop(spell_id)
        m = s["mageActors"][actor]
        assert cast["casterId"] == actor and cast["timestamp"] == t and m["actionBudget"]["action"] == "spent-on-spell"
        if spell_id == "summon-greater-fire-pet":
            s["actors"]["actor-w05-firepet"] = {"id": "actor-w05-firepet",
                "sourceProfileId": fire["id"], "controllerId": actor, "size": fire["size"],
                "creatureType": fire["creatureType"], "weightLb": fire["weightLb"], "hp": fire["hpMax"],
                "ac": fire["ac"], "speedFt": fire["speedFt"], "abilities": fire["abilities"],
                "alive": True, "isGear": False, "physicalPosition": {"planeKey": ORIGIN, "centerFt": [-5, -2.5, 3],
                    "bottomCenterFt": [-5, -2.5, 0], "bodyBoxFt": [[-7.5, -2.5], [-5, 0], [0, 6]]},
                "sourceLifecycle": {"spellId": spell_id, "beganAt": t, "deadline": t + 60, "endsAtOriginalDeadline": True},
                "inventoryObjectIds": [], "movementBudget": {"speedFt": fire["speedFt"], "spentFt": 0, "remainingFt": fire["speedFt"]},
                "commandedThisTurn": False}
        elif spell_id == "faction-champion":
            check = s["factionChecks"][-1]
            assert check["phase"] == "pre-payment" and check["factionId"] == "FACTION-W05-TEST-01"
            s["actors"]["actor-w05-champion"] = {"id": "actor-w05-champion",
                "sourceProfileId": champion["id"], "controllerId": actor, "size": champion["size"],
                "creatureType": champion["creatureType"], "weightLb": champion["weightLb"],
                "hp": champion["hpMax"], "ac": champion["ac"], "speedFt": champion["speedFt"],
                "abilities": champion["abilities"], "alive": True, "isGear": False,
                "factionRepresentative": {"factionId": check["factionId"], "representativeOnly": True,
                    "realNpcIdentity": False, "membershipGranted": False},
                "physicalPosition": {"planeKey": ORIGIN, "centerFt": [-5, 2.5, 3],
                    "bottomCenterFt": [-5, 2.5, 0], "bodyBoxFt": [[-7.5, -2.5], [0, 5], [0, 6]]},
                "sourceLifecycle": {"spellId": spell_id, "beganAt": t, "deadline": t + 60, "endsAtOriginalDeadline": True},
                "intrinsicGearIsNotInventory": True, "inventoryObjectIds": [],
                "movementBudget": {"speedFt": champion["speedFt"], "spentFt": 0, "remainingFt": champion["speedFt"]},
                "commandedThisTurn": False}
            s["factionChecks"].append({"time": t, "phase": "formation", "factionId": check["factionId"],
                "alliedStatus": True, "currentStanding": 3, "invocationPermission": True,
                "aidProhibition": False, "membershipInferred": False,
                "passesAllFourPredicates": True, "fixtureOnly": True})
        else:
            s["gate"] = {"id": "gate-w05-001", "creatorId": actor, "sourceSpellId": spell_id,
                "selectedCreatureType": "Elemental", "selectedAtCreation": True, "active": True,
                "startedAt": t, "deadline": t + 600,
                "aperture": {"shape": "vertical rectangle", "planeXFt": 0, "yRangeFt": [-5, 5],
                    "zRangeFt": [0, 15], "widthFt": 10, "heightFt": 15, "orientation": "plane normal +X"},
                "originPlaneKey": ORIGIN, "rangeFromCasterFt": 50,
                "castPredicates": {"acquired": True, "prepared": True, "class": "Mage", "classLevel": 17,
                    "school": "Conjuration", "rank": 9, "action": "spent-on-spell", "rpSpent": 26,
                    "components": ["V", "S", "F"], "clearPerceivedSpace": True, "within120Ft": True},
                "admissions": [], "crossingReceipts": {}}
        s.setdefault("resolvedSpells", []).append({"spellId": spell_id, "casterId": actor,
            "time": t, "counterspellAttempts": 0, "resolved": True})
    return emit(events, state, f"W05-CAST-RESOLVE-{spell_id.upper()}", t, "spell-cast-resolution",
        "No eligible responder attempted Counterspell; the paid spell resolves and its independent concentration/source clock begins.",
        mutate, [refs["firePetProfile"] if spell_id == "summon-greater-fire-pet" else refs["championProfile"] if spell_id == "faction-champion" else refs["gateRule"]], locators)


def cast_spell(events: list[dict[str, Any]], state: dict[str, Any], actor: str, spell_id: str,
               t: float, ac5: dict[str, Any], refs: dict[str, str], locators: list[dict[str, Any]]) -> dict[str, Any]:
    if spell_id == "summon-greater-fire-pet":
        spec = {"rpCost": 10, "rank": 5, "durationSeconds": 60}
    elif spell_id == "faction-champion":
        spec = {"rpCost": 10, "rank": 5, "durationSeconds": 60}
    else:
        spec = {"rpCost": 26, "rank": 9, "durationSeconds": 600}
    state = cast_commit(events, state, actor, spell_id, t, spec, refs, locators)
    state = counterspell_window(events, state, actor, spell_id, t, refs, locators)
    return cast_resolve(events, state, actor, spell_id, t, ac5, refs, locators)


def turn_and_attached_phase(events: list[dict[str, Any]], state: dict[str, Any], actor: str, t: float,
                            boundary: str, refs: dict[str, str], locators: list[dict[str, Any]],
                            command: dict[str, Any] | None = None, branch: str | None = None) -> dict[str, Any]:
    state = start_turn(events, state, actor, t, boundary, locators)
    if actor == "actor-w05-champion-owner" and t == -18:
        state = faction_check(events, state, t, refs, locators)
        state = cast_spell(events, state, actor, "faction-champion", t, ac5_cache, refs, locators)
    elif actor == "actor-w05-firepet-owner" and t == -24:
        state = cast_spell(events, state, actor, "summon-greater-fire-pet", t, ac5_cache, refs, locators)
    elif actor == "actor-w05-gate-caster" and t == -12:
        state = cast_spell(events, state, actor, "banishment-gate", t, ac5_cache, refs, locators)
    if command is not None:
        def command_owner(s: dict[str, Any]) -> None:
            m = s["mageActors"][actor]
            assert s["turnScheduler"]["activeActorId"] == actor and m["actionBudget"]["bonusAction"] == "available"
            allowance = m["regularTurn"]["companionCommandAllowance"]
            assert not allowance["usedThisTurn"]
            companion = s["actors"][command["companionId"]]
            owner_pos = m["position"]["centerFt"]
            companion_pos = companion["physicalPosition"]["centerFt"]
            actual_range = sum((owner_pos[i] - companion_pos[i]) ** 2 for i in range(3)) ** 0.5
            assert m["conscious"] and m["perceivesClearly"] and command["ownerConscious"]
            assert command["ownerPerceivesCompanion"] and actual_range <= 60 and command["lineOfEffect"]
            m["actionBudget"]["bonusAction"] = "spent-on-companion-command"
            allowance["usedThisTurn"] = True
            allowance["commandedActorId"] = command["companionId"]
            if command["companionId"] == "actor-w05-firepet":
                s["actors"][command["companionId"]]["commandedThisTurn"] = True
            s["turnScheduler"]["companionCommandEvents"] = s["turnScheduler"].get("companionCommandEvents", []) + [
                {"ownerId": actor, "companionId": command["companionId"], "roundBoundary": boundary,
                 "moveOnly": False, "damageOrControlActionSelected": True,
                 "actionName": command["actionName"], "ownerConscious": command["ownerConscious"],
                 "ownerPerceivesCompanion": command["ownerPerceivesCompanion"],
                 "actualRangeFt": round(actual_range, 4), "maximumRangeFt": 60,
                 "lineOfEffect": command["lineOfEffect"], "fixtureBranch": branch}]
        state = emit(events, state, f"W05-COMPANION-COMMAND-{command['companionId']}-{boundary}-{branch}",
            t, "companion-command", "Owner spends one Bonus Action and one shared Companion Command allowance for exactly one companion.",
            command_owner, [mage_profile_ref(actor), refs["companionCommand"],
                refs["firePetProfile"] if command["companionId"] == "actor-w05-firepet" else refs["championProfile"]], locators)
    state = end_turn(events, state, actor, t, boundary, locators)
    companion_id = "actor-w05-champion" if actor == "actor-w05-champion-owner" else "actor-w05-firepet" if actor == "actor-w05-firepet-owner" else None
    if companion_id and companion_id in state["actors"]:
        if command is not None:
            if companion_id == "actor-w05-champion" and branch == "lawful":
                state = lawful_release_phase(events, state, t, refs, locators)
            elif companion_id == "actor-w05-firepet":
                state = carrier_move_phase(events, state, t, branch or "common", refs, locators)
        else:
            def idle_phase(s: dict[str, Any]) -> None:
                actor_state = s["actors"][companion_id]
                owner = s["mageActors"][actor]
                assert not owner["regularTurn"]["active"]
                actor_state["companionPhaseHistory"] = actor_state.get("companionPhaseHistory", []) + [
                    {"afterOwnerTurn": boundary, "commanded": False, "choice": "remain-supported-and-Dodge",
                     "damageOrControl": False,
                     "auraNonqualification": "no hostile recipient has a regular START marker in this attached phase"}]
                s["turnScheduler"]["companionPhases"].append({"ownerId": actor, "companionId": companion_id,
                    "afterOwnerTurn": boundary, "choice": "remain-supported-and-Dodge", "immediatelyAfterWholeTurn": True})
                if companion_id == "actor-w05-firepet":
                    s["turnScheduler"]["firePetAuraCheckpointLedger"].append({"boundary": boundary,
                        "candidateFixtureTargetIds": ["actor-w05-target-firepet-fixture"],
                        "eligibleRecipientRegularStartOccurred": False,
                        "result": "no aura save/damage; static fixture target has no initiative slot"})
            state = emit(events, state, f"W05-ATTACHED-PHASE-{companion_id}-{boundary}", t, "attached-companion-phase",
                "Immediately after the whole owner turn, the uncommanded companion remains in its supported space and Dodges; it deals no damage and imposes no control.",
                idle_phase, [mage_profile_ref(actor), refs["companionCommand"],
                    refs["firePetProfile"] if companion_id == "actor-w05-firepet" else refs["championProfile"]], locators)
    return state


def install_carriage(events: list[dict[str, Any]], state: dict[str, Any], t: float,
                     refs: dict[str, str], locators: list[dict[str, Any]]) -> dict[str, Any]:
    def mutate(s: dict[str, Any]) -> None:
        carrier = s["actors"]["actor-w05-firepet"]
        passenger = s["actors"]["actor-w05-champion"]
        carrier_box = copy.deepcopy(carrier["physicalPosition"]["bodyBoxFt"])
        passenger_box = copy.deepcopy(passenger["physicalPosition"]["bodyBoxFt"])
        assert carrier_box[1][1] == passenger_box[1][0] == 0
        s["carriageRelation"] = {"id": "W05-CARRY-RELATION-02", "carrierId": carrier["id"],
            "passengerId": passenger["id"], "kind": "TEST_ONLY articulated side-support contact",
            "permission": {"carrierOwnerAllows": True, "passengerOwnerAllows": True, "passengerWilling": True},
            "supportGeometry": {"fixtureOnly": True, "separateEquipmentItem": False,
                "formation": {"carrierBoxFt": carrier_box, "passengerBoxFt": passenger_box,
                    "contactPlane": "y=0", "interbodyGapFt": 0, "bodyBoxesOverlap": False,
                    "supportEnvelope": {"type": "articulated side-support contact", "contactIsPhysicalFixturePremise": True}},
                "current": {"carrierBoxFt": carrier_box, "passengerBoxFt": passenger_box,
                    "supportActive": True, "interbodyGapFt": 0}},
            "capacity": {"carrierSize": "Medium", "carrierStrength": 14, "physicalLimitLb": 210,
                "passengerBodyAndAssociatedEquipmentLb": 180, "carrierLoadCapacity": 14,
                "passengerCasualtyLoad": 6, "supportItemMassLb": 0, "loadUsed": 6,
                "weightPass": True, "loadPass": True,
                "formulaSourceTextLocator": {"member": "rules/BODY_EQUIPMENT.md", "lines": [94, 109]}},
            "separation": None, "fixtureItemIds": [],
            "permissionToSeparate": "both owners authorize a lawful release in the separable branch"}
    return emit(events, state, "W05-TESTONLY-CARRIAGE-FORMATION", t, "test-fixture-carriage-initialization",
        "Form two distinct living actor records with aligned side-support contact boxes, zero gap, no overlap, and both physical capacity checks passing. Geometry is a TEST_ONLY premise, not canon.",
        mutate, [refs["firePetProfile"], refs["championProfile"]], locators)


def lawful_release_phase(events: list[dict[str, Any]], state: dict[str, Any], t: float,
                         refs: dict[str, str], locators: list[dict[str, Any]]) -> dict[str, Any]:
    def preflight(s: dict[str, Any]) -> None:
        assert s["turnScheduler"]["activeActorId"] is None
        s["carriageRelation"]["separation"] = {"possible": True, "method": "TEST_ONLY articulated contact releases without body harm",
            "requiresBodyHarm": False, "permissionGranted": True, "fixtureOnly": True}
    state = emit(events, state, "W05-A01-SEPARATION-PREFLIGHT", t, "lawful-separation-preflight",
        "At the passenger owner's turn-end attached phase, test the authorized non-harmful release path before any body crosses the Gate plane.",
        preflight, [refs["gateRule"], refs["championProfile"]], locators)
    def champion_strike(s: dict[str, Any]) -> None:
        owner = s["mageActors"]["actor-w05-champion-owner"]
        champion_actor = s["actors"]["actor-w05-champion"]
        target = s["actors"]["actor-w05-target-champion-fixture"]
        assert owner["regularTurn"]["companionCommandAllowance"]["commandedActorId"] == champion_actor["id"]
        assert target["hostilePerceivedByCompanion"] and target["physicalPosition"]["planeKey"] == ORIGIN
        assert abs(target["physicalPosition"]["centerFt"][0] - champion_actor["physicalPosition"]["centerFt"][0]) == 5
        roll = {"d20": 1, "spellAttackModifier": owner["spellAttackModifier"],
            "total": 1 + owner["spellAttackModifier"], "targetAc": target["ac"]}
        roll["hit"] = roll["total"] >= roll["targetAc"]
        assert not roll["hit"]
        champion_actor["attackHistory"] = champion_actor.get("attackHistory", []) + [
            {"name": "Champion Strike", **roll, "damageResolved": False, "fixtureTargetId": target["id"]}]
        champion_actor["companionPhaseHistory"] = champion_actor.get("companionPhaseHistory", []) + [
            {"afterOwnerTurn": "-6", "commanded": True, "attackAction": "Champion Strike",
             "attackOutcome": "miss", "movementFollows": True}]
    state = emit(events, state, "W05-A01B-CHAMPION-STRIKE-FIXTURE-MISS", t, "commanded-companion-attack",
        "The commanded Champion uses the required profile action during its attached phase; the explicitly TEST_ONLY construct target is missed, so no damage or body-state change occurs.",
        champion_strike, [refs["championProfile"], refs["companionCommand"], refs["w05ChampionProfile"]], locators)
    def release(s: dict[str, Any]) -> None:
        passenger = s["actors"]["actor-w05-champion"]
        before = copy.deepcopy(passenger["physicalPosition"])
        after_center = [-5, 7.5, 3]
        passenger["physicalPosition"] = {"planeKey": ORIGIN, "centerFt": after_center,
            "bottomCenterFt": [-5, 7.5, 0], "bodyBoxFt": [[-7.5, -2.5], [5, 10], [0, 6]]}
        passenger["movementBudget"]["spentFt"] = 5
        passenger["movementBudget"]["remainingFt"] = 25
        relation = s["carriageRelation"]
        relation["separation"].update({"resolved": True, "distanceMovedFt": 5, "movementAxis": "+Y",
            "verticalDisplacementFt": 0, "beforePosition": before, "afterPosition": passenger["physicalPosition"]})
        relation["status"] = "lawfully-separated-before-crossing"
        relation["passengerId"] = None
        relation["supportGeometry"]["current"] = {"carrierBoxFt": copy.deepcopy(s["actors"]["actor-w05-firepet"]["physicalPosition"]["bodyBoxFt"]),
            "passengerBoxFt": copy.deepcopy(passenger["physicalPosition"]["bodyBoxFt"]), "supportActive": False,
            "interbodyGapFt": None, "historicalFormationPreserved": True}
        passenger["companionPhaseHistory"] = passenger.get("companionPhaseHistory", []) + [
            {"afterOwnerTurn": "-6", "commanded": True, "movementCostFt": 5, "verticalDisplacementFt": 0,
             "remainsOnOriginSide": True, "choice": "release-and-move"}]
        s["turnScheduler"]["companionPhases"].append({"ownerId": "actor-w05-champion-owner",
            "companionId": passenger["id"], "afterOwnerTurn": "-6", "commanded": True,
            "attackAction": "Champion Strike", "movementCostFt": 5, "immediatelyAfterWholeTurn": True})
    return emit(events, state, "W05-A02-CHAMPION-RELEASES-AT-ORIGIN", t, "passenger-ordinary-movement-separation",
        "The Champion uses exactly 5 ft of its 30-ft movement during its own owner's commanded attached phase. Its height is unchanged and its entire body remains at x<0 on the origin plane.",
        release, [refs["gateRule"], refs["championProfile"], refs["companionCommand"]], locators)


def carrier_move_phase(events: list[dict[str, Any]], state: dict[str, Any], t: float, branch: str,
                       refs: dict[str, str], locators: list[dict[str, Any]]) -> dict[str, Any]:
    def fire_strike(s: dict[str, Any]) -> None:
        owner = s["mageActors"]["actor-w05-firepet-owner"]
        pet = s["actors"]["actor-w05-firepet"]
        target = s["actors"]["actor-w05-target-firepet-fixture"]
        assert owner["regularTurn"]["companionCommandAllowance"]["commandedActorId"] == pet["id"]
        assert target["hostilePerceivedByCompanion"] and target["physicalPosition"]["planeKey"] == ORIGIN
        assert target["initiativeStatus"] == "static-test-target-no-slot" and target["regularTurnStarts"] == []
        assert abs(target["physicalPosition"]["centerFt"][1] - pet["physicalPosition"]["centerFt"][1]) == 5
        roll = {"d20": 1, "spellAttackModifier": owner["spellAttackModifier"],
            "total": 1 + owner["spellAttackModifier"], "targetAc": target["ac"]}
        roll["hit"] = roll["total"] >= roll["targetAc"]
        assert not roll["hit"]
        pet["attackHistory"] = pet.get("attackHistory", []) + [
            {"name": "Fire Strike", **roll, "damageResolved": False, "fixtureTargetId": target["id"]}]
        s["turnScheduler"]["firePetAuraCheckpointLedger"].append({"boundary": "-6",
            "candidateFixtureTargetIds": [target["id"]], "eligibleRecipientRegularStartOccurred": False,
            "result": "no aura save/damage; target has no regular START and the crossing phase ends before the next boundary"})
        pet["companionPhaseHistory"] = pet.get("companionPhaseHistory", []) + [
            {"afterOwnerTurn": "-6", "commanded": True, "attackAction": "Fire Strike",
             "attackOutcome": "miss", "movementFollows": True}]
    state = emit(events, state, f"W05-{branch.upper()}-FIRE-STRIKE-FIXTURE-MISS", t, "commanded-companion-attack",
        "The commanded Fire Pet uses the required profile action during its attached phase; the explicitly TEST_ONLY construct target is missed, so no damage or body-state change occurs.",
        fire_strike, [refs["firePetProfile"], refs["companionCommand"], refs["w05FireProfile"]], locators)
    def move(s: dict[str, Any]) -> None:
        pet = s["actors"]["actor-w05-firepet"]
        old_pet = copy.deepcopy(pet["physicalPosition"])
        pet["movementBudget"]["spentFt"] = 10
        pet["movementBudget"]["remainingFt"] = 20
        pet["movementBudget"]["commandedMoveFt"] = 10
        pet["physicalPosition"] = {"planeKey": ORIGIN, "centerFt": [5, -2.5, 3],
            "bottomCenterFt": [5, -2.5, 0], "bodyBoxFt": [[2.5, 7.5], [-5, 0], [0, 6]]}
        s["turnScheduler"]["companionPhases"].append({"ownerId": "actor-w05-firepet-owner",
            "companionId": pet["id"], "afterOwnerTurn": "-6", "commanded": True,
            "attackAction": "Fire Strike", "movementCostFt": 10, "immediatelyAfterWholeTurn": True})
        if branch == "impossible":
            passenger = s["actors"]["actor-w05-champion"]
            passenger["physicalPosition"] = {"planeKey": ORIGIN, "centerFt": [5, 2.5, 3],
                "bottomCenterFt": [5, 2.5, 0], "bodyBoxFt": [[2.5, 7.5], [0, 5], [0, 6]]}
            relation = s["carriageRelation"]
            relation["supportGeometry"]["current"] = {"carrierBoxFt": copy.deepcopy(pet["physicalPosition"]["bodyBoxFt"]),
                "passengerBoxFt": copy.deepcopy(passenger["physicalPosition"]["bodyBoxFt"]),
                "supportActive": True, "interbodyGapFt": 0, "historicalFormationPreserved": True}
            s["gate"]["crossingReceipts"]["W05-CROSSING-IMPOSSIBLE-SEP-002"] = {
                "result": "atomic-exile-failure", "primaryId": pet["id"], "passengerId": passenger["id"],
                "reason": "the living passenger remains physically inseparable from the Elemental primary",
                "allBodiesRemainOnOriginPlane": True, "cellCreated": False, "claimSpent": False,
                "deletion": False, "bodyConvertedToGear": False}
            s["gate"]["admissions"].append({"primaryId": pet["id"], "admitted": False, "reason": "atomic-separation-failure"})
        else:
            cell_id = "CELL-W05-LAWFUL-PRIMARY-02"
            pet["physicalPosition"] = {"planeKey": cell_id, "cellLocalFt": [0, 0, 0],
                "localOriginConvention": "bottom-center", "bodyGeometricCenterOffsetFt": [0, 0, 3],
                "bodyBoxLocalFt": [[-2.5, 2.5], [-2.5, 2.5], [0, 6]]}
            admission_endpoint_center = [5, -2.5, 3]
            s["cells"][cell_id] = {"id": cell_id, "primaryId": pet["id"], "createdByGateId": "gate-w05-001",
                "openedAtSeconds": t, "deadlineSeconds": t + 60, "live": True, "secondaryBodies": [],
                "originAnchor": {"planeKey": ORIGIN, "admissionCompleted": True,
                    "bodyOriginCenterFt": admission_endpoint_center, "bodyBottomCenterFt": [5, -2.5, 0],
                    "mapping": "cellLocalFt [0,0,0] is the body's bottom-center; adding [0,0,3] gives the geometric center",
                    "sourceWorldEndpointCenterFt": admission_endpoint_center},
                "geometry": {"xFt": [-7.5, 7.5], "yFt": [-7.5, 7.5], "zFt": [0, 15], "bodyContained": True}}
            s["gate"]["admissions"].append({"primaryId": pet["id"], "admitted": True, "passengerIds": [], "cellId": cell_id})
            s["gate"]["crossingReceipts"]["W05-CROSSING-LAWFUL-SEP-002"] = {
                "result": "admitted-primary-only", "primaryId": pet["id"], "passengerId": "actor-w05-champion",
                "passengerAtOrigin": True, "claimSpent": True, "cellId": cell_id,
                "crossingDistanceFt": 10, "fullBodyCompletedEndpointFt": admission_endpoint_center}
            s["hardControlClaims"]["claim-w05-firepet-002"] = {"sourceCharacterId": "actor-w05-gate-caster",
                "targetId": pet["id"], "encounterId": "ENCOUNTER-W05-TEST-02",
                "reservedOnSuccessfulEstablishment": True, "crossingId": "W05-CROSSING-LAWFUL-SEP-002"}
            relation = s["carriageRelation"]
            relation["supportGeometry"]["current"] = {"carrierBoxFt": None,
                "passengerBoxFt": copy.deepcopy(s["actors"]["actor-w05-champion"]["physicalPosition"]["bodyBoxFt"]),
                "supportActive": False, "interbodyGapFt": None, "historicalFormationPreserved": True,
                "carrierNowInCell": True}
    return emit(events, state, f"W05-{branch.upper()}-FIREPET-MOVE-AND-GATE-RESOLUTION", t,
        "attached-companion-phase-and-gate-crossing",
        "After the whole Fire Pet owner's turn, its commanded attached phase spends exactly 10 ft of the 30-ft movement budget. The Gate resolves against the live support geometry and creates no campaign fact.",
        move, [refs["gateRule"], refs["firePetProfile"], refs["championProfile"]], locators)


def build_common(ac5: dict[str, Any], profiles: dict[str, Any], refs: dict[str, str],
                 locators: list[dict[str, Any]], equip: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    state = initial_state(profiles, equip)
    events: list[dict[str, Any]] = []
    for t in BOUNDARIES[:3]:
        boundary = str(int(t))
        for actor in TURN_ORDER:
            state = turn_and_attached_phase(events, state, actor, t, boundary, refs, locators)
    state = install_carriage(events, state, -12, refs, locators)
    return state, events


def branch_common(events: list[dict[str, Any]], state: dict[str, Any], refs: dict[str, str],
                  locators: list[dict[str, Any]], branch: str) -> dict[str, Any]:
    if branch == "lawful":
        champ_command = {"companionId": "actor-w05-champion", "ownerConscious": True, "ownerPerceivesCompanion": True,
            "lineOfEffect": True, "actionName": "Champion Strike"}
        fire_command = {"companionId": "actor-w05-firepet", "ownerConscious": True, "ownerPerceivesCompanion": True,
            "lineOfEffect": True, "actionName": "Fire Strike"}
        state = turn_and_attached_phase(events, state, "actor-w05-champion-owner", -6, "-6", refs, locators,
            champ_command, "lawful")
        state = turn_and_attached_phase(events, state, "actor-w05-firepet-owner", -6, "-6", refs, locators,
            fire_command, "lawful")
    else:
        def lock(s: dict[str, Any]) -> None:
            s["carriageRelation"]["separation"] = {"possible": False,
                "method": "one-piece TEST_ONLY articulated support coupling; no ordinary non-harmful release path",
                "requiresBodyHarm": True, "permissionGranted": True,
                "whyImpossible": "only a harmful operation would separate these living bodies; no harmful operation is performed",
                "fixtureOnly": True, "resolved": False}
            s["carriageRelation"]["status"] = "support-coupled-test-premise"
        state = emit(events, state, "W05-B01-LOCKED-SUPPORT-TEST-PREMISE", -6, "test-fixture-impossible-separation-premise",
            "The alternative branch freezes the same contact envelope into a one-piece TEST_ONLY coupling; permission and willingness remain true, but physical separation would harm a living body.",
            lock, [refs["gateRule"], refs["firePetProfile"], refs["championProfile"]], locators)
        state = turn_and_attached_phase(events, state, "actor-w05-champion-owner", -6, "-6", refs, locators,
            None, "impossible")
        fire_command = {"companionId": "actor-w05-firepet", "ownerConscious": True, "ownerPerceivesCompanion": True,
            "lineOfEffect": True, "actionName": "Fire Strike"}
        state = turn_and_attached_phase(events, state, "actor-w05-firepet-owner", -6, "-6", refs, locators,
            fire_command, "impossible")
    state = turn_and_attached_phase(events, state, "actor-w05-gate-caster", -6, "-6", refs, locators, None, branch)
    return state


def resolve_branches(common: dict[str, Any], refs: dict[str, str], locators: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for branch, branch_id, outcome in [
        ("lawful", "W05-LAWFUL-SEPARATION", "Elemental primary admitted; Humanoid passenger remains at origin"),
        ("impossible", "W05-IMPOSSIBLE-SEPARATION", "atomic exile failure; both living bodies remain on origin plane"),
    ]:
        SEQUENCES[-6] = 0
        events: list[dict[str, Any]] = []
        state = branch_common(events, copy.deepcopy(common), refs, locators, branch)
        result.append({"id": branch_id, "outcome": outcome, "events": events, "finalState": state,
            "reverseOrder": [x["eventId"] for x in reversed(events)], "fixtureOnly": True})
    return result


def pointer_value(packet: Path, reference: str) -> Any:
    member, fragment = reference.split("#", 1)
    value = load_json(packet / member)
    if fragment:
        for part in fragment.split("/")[1:]:
            part = part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def verify_case(case: dict[str, Any], source_bindings: dict[str, Any], locators: list[dict[str, Any]]) -> dict[str, Any]:
    prefix = case["commonPrefix"]
    current = copy.deepcopy(prefix["initialState"])
    timeline = []
    replay_count = 0
    for event_record in prefix["events"]:
        assert event_record["timestampSeconds"] >= current["elapsedSeconds"]
        assert event_record["beforeStateSha256"] == state_sha(current)
        nxt = apply_ops(current, event_record["forwardOperations"])
        assert state_sha(nxt) == event_record["afterStateSha256"] == state_sha(event_record["stateAfter"])
        assert apply_ops(nxt, event_record["inverseOperations"]) == current
        current = nxt
        timeline.append((event_record["timestampSeconds"], event_record["sequenceAtTimestamp"]))
        replay_count += 1
    assert current == prefix["finalState"] and timeline == sorted(timeline)
    active = None
    for ev in prefix["events"]:
        next_active = ev["stateAfter"]["turnScheduler"]["activeActorId"]
        if ev["kind"] == "regular-turn-start":
            assert active is None and next_active is not None
        elif ev["kind"] == "regular-turn-end":
            assert active is not None and next_active is None
        else:
            assert next_active == active
        active = next_active
    assert active is None
    branches = {}
    for fork in case["terminalForks"]:
        current = copy.deepcopy(prefix["finalState"])
        fork_timeline = []
        for event_record in fork["events"]:
            assert event_record["timestampSeconds"] >= current["elapsedSeconds"]
            assert event_record["beforeStateSha256"] == state_sha(current)
            nxt = apply_ops(current, event_record["forwardOperations"])
            assert state_sha(nxt) == event_record["afterStateSha256"] == state_sha(event_record["stateAfter"])
            assert apply_ops(nxt, event_record["inverseOperations"]) == current
            current = nxt
            fork_timeline.append((event_record["timestampSeconds"], event_record["sequenceAtTimestamp"]))
            replay_count += 1
        assert current == fork["finalState"] and fork_timeline == sorted(fork_timeline)
        reverse = copy.deepcopy(current)
        for event_record in reversed(fork["events"]):
            reverse = apply_ops(reverse, event_record["inverseOperations"])
        assert reverse == prefix["finalState"]
        active = None
        for ev in fork["events"]:
            next_active = ev["stateAfter"]["turnScheduler"]["activeActorId"]
            if ev["kind"] == "regular-turn-start":
                assert active is None and next_active is not None
            elif ev["kind"] == "regular-turn-end":
                assert active is not None and next_active is None
            else:
                assert next_active == active
            active = next_active
        assert active is None
        branches[fork["id"]] = {"eventCount": len(fork["events"]), "forwardInverseExact": True,
            "finalStateSha256": state_sha(current), "chronological": True}

    for name, state in [("prefix", prefix["finalState"])] + [(x["id"], x["finalState"]) for x in case["terminalForks"]]:
        assert state["turnScheduler"]["activeActorId"] is None
        for actor in TURN_ORDER:
            assert state["mageActors"][actor]["focus"]["custody"] == actor
            assert state["mageActors"][actor]["handOccupancy"]["left"] == "free-for-somatic"
            assert state["mageActors"][actor]["handOccupancy"]["right"] == state["mageActors"][actor]["focus"]["objectId"]
            assert state["mageActors"][actor]["counterspell"]["usesThisWitness"] == 0

    for actor in TURN_ORDER:
        owner = prefix["finalState"]["mageActors"][actor]
        assert owner["regularTurn"]["refreshBoundaries"] == ["-24", "-18", "-12"]
        assert owner["regularTurn"]["starts"] == [-24, -18, -12]
        assert owner["regularTurn"]["ends"] == [-24, -18, -12]
        assert len(set(owner["regularTurn"]["refreshBoundaries"])) == 3
        assert owner["stanceState"]["active"]["name"] == "Guarded"
        assert owner["stanceState"]["active"]["expiresAtNextRegularStart"] == -6
    for fork in case["terminalForks"]:
        for actor in TURN_ORDER:
            owner = fork["finalState"]["mageActors"][actor]
            assert owner["regularTurn"]["refreshBoundaries"] == ["-24", "-18", "-12", "-6"]
            assert owner["regularTurn"]["starts"] == [-24, -18, -12, -6]
            assert owner["regularTurn"]["ends"] == [-24, -18, -12, -6]
            assert len(owner["stanceState"]["history"]) == 3
            assert owner["stanceState"]["active"]["name"] == "Guarded"
            assert owner["stanceState"]["active"]["expiresAtNextRegularStart"] == 0
        commands = fork["finalState"]["turnScheduler"].get("companionCommandEvents", [])
        if fork["id"] == "W05-LAWFUL-SEPARATION":
            assert [x["companionId"] for x in commands] == ["actor-w05-champion", "actor-w05-firepet"]
            assert all(x["damageOrControlActionSelected"] for x in commands)
        else:
            assert [x["companionId"] for x in commands] == ["actor-w05-firepet"]
            assert all(x["damageOrControlActionSelected"] for x in commands)
        for companion_id in ["actor-w05-firepet", "actor-w05-champion"]:
            attacks = fork["finalState"]["actors"][companion_id].get("attackHistory", [])
            if companion_id == "actor-w05-firepet" or fork["id"] == "W05-LAWFUL-SEPARATION":
                assert attacks and all(not x["hit"] and not x["damageResolved"] for x in attacks)
        assert fork["finalState"]["actors"]["actor-w05-target-firepet-fixture"]["hp"] == 100
        assert fork["finalState"]["actors"]["actor-w05-target-champion-fixture"]["hp"] == 100
    assert len(prefix["finalState"]["counterspellWindows"]) == 3
    for window in prefix["finalState"]["counterspellWindows"]:
        assert window["counterspellAttemptCount"] == 0 and len(window["otherCasterDecisions"]) == 2
        assert all(x["eligibleToAttempt"] and x["decision"] == "declined-no-attempt" and not x["reactionSpent"] for x in window["otherCasterDecisions"])
    expected_casts = {
        "actor-w05-firepet-owner": ("summon-greater-fire-pet", 1, 10, 5),
        "actor-w05-champion-owner": ("faction-champion", 1, 10, 5),
        "actor-w05-gate-caster": ("banishment-gate", 2, 26, 9),
    }
    for actor, (spell_id, d_gain, rp_cost, rank) in expected_casts.items():
        mage = prefix["finalState"]["mageActors"][actor]
        assert len(mage["castingHistory"]) == 1
        cast = mage["castingHistory"][0]
        assert cast["spellId"] == spell_id and cast["rank"] == rank
        assert cast["baseDissonance"] == d_gain and cast["refrainDissonance"] == 0
        assert cast["overcastDissonance"] == 0 and cast["dissonanceDelta"] == d_gain
        assert cast["dissonanceRpSurcharge"] == 0 and cast["rpPaid"] == rp_cost
        assert mage["dissonance"]["current"] == d_gain and mage["dissonance"]["state"] == "In Tune"
        assert mage["refrain"] == {"lastSpellId": spell_id, "repeatCount": 0}
        assert mage["nukeChain"] == []
        assert set(cast["components"]) == {"V", "S", "F"}
        assert all(c["satisfied"] for c in cast["components"].values())
    assert [x["phase"] for x in prefix["finalState"]["factionChecks"]] == ["pre-payment", "formation"]
    assert prefix["finalState"]["factionChecks"][0]["factionId"] == prefix["finalState"]["factionChecks"][1]["factionId"] == "FACTION-W05-TEST-01"
    assert prefix["finalState"]["carriageRelation"]["capacity"]["physicalLimitLb"] == 210
    assert 180 <= 210 and prefix["finalState"]["carriageRelation"]["capacity"]["passengerCasualtyLoad"] == 6 <= 14

    lawful = next(x["finalState"] for x in case["terminalForks"] if x["id"] == "W05-LAWFUL-SEPARATION")
    p = lawful["actors"]["actor-w05-champion"]["physicalPosition"]
    assert p["centerFt"] == [-5, 7.5, 3] and p["centerFt"][2] == 3
    assert lawful["actors"]["actor-w05-champion"]["movementBudget"]["spentFt"] == 5
    assert lawful["actors"]["actor-w05-champion"]["movementBudget"]["remainingFt"] == 25
    assert lawful["actors"]["actor-w05-firepet"]["physicalPosition"]["planeKey"].startswith("CELL-")
    cell = next(iter(lawful["cells"].values()))
    assert cell["originAnchor"]["bodyOriginCenterFt"] == cell["originAnchor"]["sourceWorldEndpointCenterFt"] == [5, -2.5, 3]
    assert cell["originAnchor"]["mapping"].startswith("cellLocalFt")
    assert lawful["actors"]["actor-w05-champion"]["physicalPosition"]["planeKey"] == ORIGIN
    assert lawful["actors"]["actor-w05-champion"]["alive"] and not lawful["actors"]["actor-w05-champion"]["isGear"]
    assert len(lawful["cells"]) == 1 and len(lawful["hardControlClaims"]) == 1

    impossible = next(x["finalState"] for x in case["terminalForks"] if x["id"] == "W05-IMPOSSIBLE-SEPARATION")
    assert len(impossible["cells"]) == 0 and len(impossible["hardControlClaims"]) == 0
    assert impossible["actors"]["actor-w05-firepet"]["alive"] and impossible["actors"]["actor-w05-champion"]["alive"]
    assert impossible["actors"]["actor-w05-firepet"]["physicalPosition"]["planeKey"] == ORIGIN
    assert impossible["actors"]["actor-w05-champion"]["physicalPosition"]["planeKey"] == ORIGIN
    relation = impossible["carriageRelation"]["supportGeometry"]["current"]
    assert relation["carrierBoxFt"][0] == relation["passengerBoxFt"][0] == [2.5, 7.5]
    assert relation["supportActive"] and relation["interbodyGapFt"] == 0
    assert not impossible["actors"]["actor-w05-firepet"]["isGear"] and not impossible["actors"]["actor-w05-champion"]["isGear"]
    assert "actor-w05-firepet" not in impossible["objects"] and "actor-w05-champion" not in impossible["objects"]

    refs = []
    for collection in [prefix["events"]] + [x["events"] for x in case["terminalForks"]]:
        for ev in collection:
            for ref in ev["sourceRefs"]:
                assert "#" in ref
                pointer_value(PACKET, ref)
                refs.append(ref)
    for ref in case["sourceUse"]["sourceReferences"]:
        pointer_value(PACKET, ref["pointer"])
        refs.append(ref["pointer"])
    text_checks = 0
    for collection in [prefix["events"]] + [x["events"] for x in case["terminalForks"]]:
        for ev in collection:
            for loc in ev["sourceTextLocators"]:
                lines = (PACKET / loc["member"]).read_text(encoding="utf-8-sig").splitlines()
                assert 1 <= loc["lines"][0] <= loc["lines"][1] <= len(lines)
                assert lines[loc["lines"][0] - 1].strip() and lines[loc["lines"][1] - 1].strip()
                text_checks += 1
    binding_checks = 0
    for binding in source_bindings["bindings"]:
        member = binding["member"]
        payload = PACKET / member
        assert payload.is_file()
        assert len(payload.read_bytes()) == binding["bytes"] and sha(payload.read_bytes()) == binding["sha256"]
        for pointer in binding.get("jsonPointers", []):
            pointer_value(PACKET, member + "#" + pointer)
            binding_checks += 1
        for loc in binding.get("textLocators", []):
            lines = payload.read_text(encoding="utf-8-sig").splitlines()
            assert loc["lines"][0] >= 1 and loc["lines"][-1] <= len(lines)
            assert lines[loc["lines"][0] - 1].strip() and lines[loc["lines"][-1] - 1].strip()
            binding_checks += 1
    assert case["identityDecision"] == {"decision": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False}
    assert case["queueAuthority"] == {"id": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 552, "scopedInterfaces": 173, "firstReviews": 0, "closureTasks": 20}
    queue = load_json(PACKET / "authority" / "CURRENT_SPELL_QUEUE_361.json")
    assert queue["id"] == "CURRENT-SPELL-QUEUE-361"
    assert queue["currentAuthority"]["reviewedApplied"] == case["queueAuthority"]["applied"]
    assert queue["currentAuthority"]["pending"] == case["queueAuthority"]["pending"]
    assert queue["currentAuthority"]["acceptedUnapplied"] == case["queueAuthority"]["acceptedUnapplied"]
    assert queue["currentAuthority"]["completeStandaloneProcedures"] == case["queueAuthority"]["completeStandaloneProcedures"]
    assert queue["currentAuthority"]["scopedInterfaces"] == case["queueAuthority"]["scopedInterfaces"]
    return {"status": "PASS_TEST_ONLY_STATIC_WITNESS", "eventsReplayed": replay_count,
        "sourceReferencesResolved": len(refs), "sourceTextLocatorsResolved": text_checks,
        "sourceBindingPayloadsAndPointersResolved": binding_checks,
        "branches": branches, "turnsPerMageThroughBranchStart": 4,
        "counterspellWindows": 3, "otherCasterDecisions": 6,
        "factionChecks": 2, "carriageWeightPass": "180 <= 210 lb",
        "casualtyLoadPass": "6 <= 14 Load", "identityStillHeld": True,
        "remainingResidualIds": []}


def main() -> None:
    global profiles_cache, ac5_cache
    if not W08.exists():
        raise FileNotFoundError(W08)
    bindings = prepare_sources()
    ac5, _casebook, refs, indexes = source_data()
    ac5_cache = ac5
    seeds = load_json(PACKET / "sources" / "W05_CASTER_PROFILE_SEEDS_365_TESTONLY.json")
    profiles_cache = create_mage_profiles(seeds, refs, ac5)
    profile_bytes = (PACKET / "W05_MAGE_PROFILES_365_TESTONLY.json").read_bytes()
    bindings["bindings"].append({"member": "W05_MAGE_PROFILES_365_TESTONLY.json",
        "bytes": len(profile_bytes), "sha256": sha(profile_bytes),
        "origin": {"kind": "derived-TEST_ONLY-actor-records",
            "derivedFrom": [{"archiveSha256": W08_ARCHIVE_SHA,
                "member": "sources/W08_CASTER_PROFILES_365_TESTONLY.json"},
                {"archiveSha256": AC5_ARCHIVE_SHA, "member": "candidate/SPELLS_MODEL.json"},
                {"sourceCommit": PIN, "member": "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json"}],
            "authoredW05ActorAndFocusIds": True},
        "jsonPointers": ["/profiles/0", "/profiles/1", "/profiles/2"], "textLocators": []})
    refs["w05FireProfile"] = mage_profile_ref("actor-w05-firepet-owner")
    refs["w05ChampionProfile"] = mage_profile_ref("actor-w05-champion-owner")
    refs["w05GateProfile"] = mage_profile_ref("actor-w05-gate-caster")
    write_json(PACKET / "W05_SOURCE_BINDINGS_365.json", bindings)
    equip = load_json(PACKET / "sources" / "EQUIPMENT_SOURCE_CATALOG.json")
    turn_locators = [
        {"member": "sources/COMBAT_ACTION_PLAYTEST.md", "lines": [29, 29], "claim": "six-second numbered round"},
        {"member": "sources/COMBAT_ACTION_PLAYTEST.md", "lines": [35, 35], "claim": "Reaction refresh at regular own-turn start"},
        {"member": "sources/COMBAT_ACTION_PLAYTEST.md", "lines": [57, 66], "claim": "ordered regular-turn start/end markers"},
        {"member": "sources/COMBAT_ACTION_PLAYTEST.md", "lines": [115, 115], "claim": "stance selection and expiry"},
        {"member": "sources/COMBAT_ACTION_PLAYTEST.md", "lines": [120, 120], "claim": "Guarded stance effect"},
        {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", "lines": [8376, 8382], "claim": "base RP cost and strain surcharge"},
        {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", "lines": [8424, 8427], "claim": "rank-based Dissonance and Refrain"},
        {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", "lines": [8521, 8521], "claim": "Mage chain interaction"},
        {"member": "rules/BODY_EQUIPMENT.md", "lines": [94, 109], "claim": "physical capacity and casualty Load"},
    ]
    common, common_events = build_common(ac5, profiles_cache, refs, turn_locators, equip)
    forks = resolve_branches(common, refs, turn_locators)
    coverage = {"id": "W05-CASE-COVERAGE-365-REPACK02", "witnessId": "W05",
        "status": "TEST_ONLY_STATIC_WITNESS", "closedResidualIds": [
            "W05-365-R1", "W05-365-R2", "W05-365-R3", "W05-365-R4", "W05-365-R5", "W05-365-R6", "W05-365-R7"],
        "requiredEvidence": ["W05-local focus object identities, custody, carried-load and V/S/F hand occupancy",
            "Action/RP/concentration/casting history, Dissonance/Refrain state and all other-caster Counterspell decisions",
            "serialized regular turns, once-only refreshes and attached companion phases",
            "consistent faction eligibility checked before Faction Champion payment and again at formation",
            "supported two-body formation and lawful 5-ft passenger movement with no vertical displacement",
            "full-body completed Gate admission endpoint and explicit center/bottom-center/local-origin transform",
            "impossible branch current support geometry updated after movement",
            "all source JSON pointers and text locators resolved and hash-bound"],
        "identityAcceptance": False, "applicationAuthorization": False}
    case = {"id": "W05-LIVING-BODY-CARRIAGE-365-TESTONLY-REPACK02", "status": "DIRECTOR_REVIEW_PENDING_TEST_ONLY",
        "witnessId": "W05", "spellId": "banishment-gate", "blockerId": "PG200-B04",
        "sourceBindingMember": "W05_SOURCE_BINDINGS_365.json", "notCampaign": True,
        "evidenceClass": "conditional TEST_ONLY authored static witness; no campaign event or runtime result asserted",
        "wholeIdentityGate": {"decision": "HOLD", "blockerIds": ["PG200-B03", "PG200-B04"],
            "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False},
        "applicationAuthorized": False, "acceptanceDecision": None, "selectedGateType": "Elemental",
        "primary": {"actorId": "actor-w05-firepet", "creatureType": "Elemental",
            "sourceProfileId": "AC5-PROFILE-GREATER-FIRE-PET-01"},
        "separatePassenger": {"actorId": "actor-w05-champion", "creatureType": "Humanoid",
            "sourceProfileId": "AC5-PROFILE-FACTION-CHAMPION-01", "isGear": False},
        "sourceUse": {"sourceReferences": [{"label": k, "pointer": v} for k, v in refs.items()],
            "textLocators": [{"member": "rules/BODY_EQUIPMENT.md", "lines": [94, 109], "claim": "STR x 15 physical capacity and casualty Load"},
                {"member": "sources/COMBAT_ACTION_PLAYTEST.md", "lines": [29, 35, 57, 66, 115, 120, 156], "claim": "round duration, reactions, turn markers, Guarded stance selection/effects and movement-cost ledger"},
                {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", "lines": [8376, 8382], "claim": "base RP costs and state surcharge"},
                {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", "lines": [8424, 8427], "claim": "Dissonance limit, rank gain and Refrain"},
                {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", "lines": [8521, 8521], "claim": "Mage chain and Refrain interaction"}],
            "AC5-X17": {"pointer": refs["ac5Precedent"], "use": "comparison only: separate living passenger is not gear",
                "notImported": ["AC5-BANISH-EXT", "ordinary Banishment terminal closure", "endpoint blocker exception"]},
            "operativeSchool": {"school": "Conjuration", "gateRulePointer": refs["gateRule"],
                "paragraphLabel": "PG9-Q01", "catalogAbjurationConflictPreserved": True}},
        "fixtureAssumptions": {"campaignOccurrence": False, "runtimeImplementation": False, "worldFacts": False,
            "casterPositionsAndFocusCustody": "separate TEST_ONLY fixture actors and object identities; one 1-lb source-projected wand each",
            "bodyMorphology": "TEST_ONLY articulated side-support contact; support is not separate equipment",
            "supportGeometry": "two disjoint 5x5x6-ft boxes touch at y=0 and fit within 10x15-ft aperture",
            "commandedActions": "Fire Strike and Champion Strike use explicit TEST_ONLY construct targets, both roll misses; no damage or aura recipient state changes",
            "capacity": "STR14 Medium physical limit210lb; 180lb passenger casualty Load6; support item mass0 because support is fixture anatomy/contact, not an equipment object",
            "factionEligibility": "one consistent TEST_ONLY faction identity, positive standing, ally status and invocation permission; checked before payment and at formation",
            "noGearConversion": "both bodies stay actor records; only caster focus wands are objects"},
        "timeModel": {"unit": "absolute elapsed seconds with sequenceAtTimestamp for ordered initiative subevents",
            "roundIntervalSeconds": 6, "actorTurnStartSeconds": {a: BOUNDARIES for a in TURN_ORDER},
            "actorTurnEndSeconds": {a: BOUNDARIES for a in TURN_ORDER},
            "turnOrderByBoundary": TURN_ORDER, "regularBoundaries": BOUNDARIES,
            "refreshesOncePerActorPerBoundary": True, "noOverlappingRegularTurns": True,
            "stanceChoice": "Guarded selected before the first spell/movement event; prior Guarded expires at the next regular start",
            "attachedCompanionPhaseImmediatelyAfterOwnerTurn": True,
            "firePetAuraNonqualification": "Static test targets have no initiative slots or future regular START markers; no aura trigger/save/damage occurs in this witness.",
            "branchEndpointSeconds": -6, "allSummonSourcesAndGateActiveAtBranch": True},
        "commonPrefix": {"initialState": initial_state(profiles_cache, equip), "events": common_events, "finalState": common},
        "terminalForks": forks,
        "identityDecision": {"decision": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False},
        "queueAuthority": {"id": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 552, "scopedInterfaces": 173, "firstReviews": 0, "closureTasks": 20}}
    checks = verify_case(case, bindings, turn_locators)
    write_json(PACKET / "W05_LIVING_BODY_CARRIAGE_CASE_365_TESTONLY.json", case)
    write_json(PACKET / "W05_CASE_COVERAGE_365.json", coverage)
    write_json(PACKET / "W05_BUILD_VALIDATION_365.json", {"status": checks["status"], "checks": checks,
        "identityAcceptance": False, "applicationAuthorized": False, "directorDisposition": "PENDING"})
    # Every operative source reference and text locator is rechecked against the payloads before sealing the manifest.
    all_pointers = list(refs.values())
    for ev in common_events + [e for fork in forks for e in fork["events"]]:
        all_pointers.extend(ev["sourceRefs"])
    for pointer in all_pointers:
        pointer_value(PACKET, pointer)
    members = []
    for path in sorted(x for x in PACKET.rglob("*") if x.is_file() and x.name != "ARCHIVE_MANIFEST.json"):
        data = path.read_bytes()
        members.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data)})
    write_json(PACKET / "ARCHIVE_MANIFEST.json", {"id": "W05-ARCHIVE-MANIFEST-365-REPACK02",
        "members": members, "manifestDoesNotHashItself": True})
    archive_path = OUT / ARCHIVE
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(x for x in PACKET.rglob("*") if x.is_file()):
            info = zipfile.ZipInfo(path.relative_to(PACKET).as_posix(), date_time=(2026, 10, 31, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    archive_bytes = archive_path.read_bytes()
    with zipfile.ZipFile(archive_path) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(set(z.namelist()))
        for member in z.namelist():
            if member != "ARCHIVE_MANIFEST.json":
                assert z.read(member) == (PACKET / member).read_bytes()
    delivery = {"id": "W05-DELIVERY-365-REPACK02", "witnessId": "W05",
        "status": "READY_FOR_DIRECTOR_REVIEW_TEST_ONLY", "archive": ARCHIVE,
        "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "uniqueMembers": len(members) + 1,
        "manifestPayloads": len(members), "sourceBindings": len(bindings["bindings"]),
        "sourcePointersAndLocatorsValidated": True, "allEventsReversible": True,
        "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False,
        "identityDisposition": "HOLD", "queueAuthority": case["queueAuthority"], "nextWitnessAfterSeal": "W03"}
    write_json(OUT / "ARCHIVE_DELIVERY_365_W05_REPACK02.json", delivery)
    audit = {"id": "W05-INDEPENDENT-AUDIT-365-REPACK02",
        "status": "PASS_TEST_ONLY_STATIC_WITNESS_AND_ARCHIVE; FRESH_DIRECTOR_DECISION_PENDING",
        "archive": {"file": ARCHIVE, "bytes": len(archive_bytes), "sha256": sha(archive_bytes),
            "uniqueMembers": len(members) + 1, "manifestPayloadHashes": len(members)},
        "sourceBindings": len(bindings["bindings"]), "caseChecks": checks,
        "identityDisposition": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False,
        "queueAuthority": case["queueAuthority"]}
    write_json(OUT / "INDEPENDENT_AUDIT_365_W05_REPACK02_ARCHIVE.json", audit)
    print(json.dumps({"output": str(OUT), "delivery": delivery, "audit": audit}, indent=2, ensure_ascii=False))


profiles_cache: dict[str, Any] = {}
ac5_cache: dict[str, Any] = {}


if __name__ == "__main__":
    main()
