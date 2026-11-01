#!/usr/bin/env python3
"""Build a reversible, TEST_ONLY PG328-W01 damage sub-witness for Director review."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import struct
import zipfile
import zlib


BASE = pathlib.Path(__file__).resolve().parent
INTAKE = BASE / "conjure_demiplane_fortress_closure_intake_367"
ARCHIVE = INTAKE / "payload" / "authority" / "PG328_HELD_ARCHIVE.zip"
PARENT_MEMBER = (
    "evidence/packet328/prior/Return284_cases/"
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A.json"
)
WIZARD_MEMBER = "evidence/current_bound_wizard.json"
PROFILE_MEMBER = "evidence/RETURN284_WIZARD20_PROFILE.json"
OUT = BASE / "fortress_w01_structural_damage_witness_400"
ARCHIVE_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328W01_Witness400_TESTONLY.zip"

EXPECTED = {
    "held_archive": "47af8e23be318210229f7fd2b360be809b2b7ed5d73b08abcbeaf7a078c3f1f4",
    "parent_member": "b18e7c3b7acc9867d6448a8a58d98f2d45eeea629144b1a696ef0d7c76844e54",
    "parent_final": "48c34a265c58f12cdb3d24ca6f59ddc53842476f090bfdded3796bd340b49e89",
    "wizard_member": "8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b",
    "profile_member": "a3a3ce0a714c1fa35523719c8c8a0297fc457d5b5f097f6a20a00aad6cd7be55",
    "rulebook": "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b",
    "combat": "9118101f0907e0cd52a78cef83affa9e6fcae1b3d958c8a576499dfddc424f60",
    "q23": "149d4098591799f51afa37837ccca722eb9ae08c3ea437c640d943f33b1bb637",
    "blocker": "8f50b284846ef373ada5bae610c2a8d584cf695c3922cf9c30f34bb48fc4bd4b",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return sha256(canonical(value))


def read_json(path: pathlib.Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def archive_bytes(member: str) -> bytes:
    with zipfile.ZipFile(ARCHIVE) as zf:
        return zf.read(member)


def ptr(parts: tuple[str, ...]) -> str:
    return "/" + "/".join(p.replace("~", "~0").replace("/", "~1") for p in parts)


def diff(before: object, after: object, path: tuple[str, ...] = ()) -> list[dict[str, object]]:
    if type(before) is dict and type(after) is dict:
        ops: list[dict[str, object]] = []
        for key in sorted(before.keys() - after.keys()):
            ops.append({"op": "remove", "path": ptr(path + (key,))})
        for key in sorted(after.keys() - before.keys()):
            ops.append({"op": "add", "path": ptr(path + (key,)), "value": after[key]})
        for key in sorted(before.keys() & after.keys()):
            ops.extend(diff(before[key], after[key], path + (key,)))
        return ops
    if before == after and type(before) is type(after):
        return []
    return [{"op": "replace", "path": ptr(path), "value": after}]


def apply_patch(state: object, operations: list[dict[str, object]]) -> object:
    root = copy.deepcopy(state)
    for operation in operations:
        tokens = [
            token.replace("~1", "/").replace("~0", "~")
            for token in str(operation["path"]).split("/")[1:]
        ]
        parent = root
        for token in tokens[:-1]:
            parent = parent[token]
        key = tokens[-1]
        op = operation["op"]
        if op == "remove":
            del parent[key]
        elif op == "add":
            parent[key] = copy.deepcopy(operation["value"])
        elif op == "replace":
            parent[key] = copy.deepcopy(operation["value"])
        else:
            raise ValueError(f"Unknown patch operation: {op}")
    return root


def write_json(path: pathlib.Path, value: object) -> bytes:
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(data)
    return data


def turn_start(state: dict[str, object], actor_id: str, when: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if abs(float(schedule["nextStart"]) - when) > 1e-9:
        raise ValueError(f"{actor_id} scheduled start mismatch: {schedule['nextStart']} != {when}")
    schedule["starts"].append(when)
    schedule["nextEnd"] = when + float(schedule["endOffset"])
    schedule["nextStart"] = when + float(schedule["period"])
    actor["action"] = 1
    actor["bonusAction"] = 1
    actor["reaction"] = 1
    actor["movement"] = actor["speed"]
    actor["magicThisTurn"] = False
    schedule["budgetHistory"].append(
        {
            "time": when,
            "action": 1,
            "BA": 1,
            "Reaction": 1,
            "Move": actor["speed"],
            "recharge": copy.deepcopy(actor["recharge"]),
        }
    )


def turn_end(state: dict[str, object], actor_id: str, when: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if abs(float(schedule["nextEnd"]) - when) > 1e-9:
        raise ValueError(f"{actor_id} scheduled end mismatch: {schedule['nextEnd']} != {when}")
    schedule["ends"].append(when)


def main() -> None:
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing packet directory: {OUT}")
    if sha256(ARCHIVE.read_bytes()) != EXPECTED["held_archive"]:
        raise ValueError("Held archive SHA-256 changed")

    parent_raw = archive_bytes(PARENT_MEMBER)
    wizard_raw = archive_bytes(WIZARD_MEMBER)
    profile_raw = archive_bytes(PROFILE_MEMBER)
    if sha256(parent_raw) != EXPECTED["parent_member"]:
        raise ValueError("Historical parent member SHA-256 changed")
    if sha256(wizard_raw) != EXPECTED["wizard_member"]:
        raise ValueError("Bound Wizard source member SHA-256 changed")
    if sha256(profile_raw) != EXPECTED["profile_member"]:
        raise ValueError("Bound actor profile member SHA-256 changed")

    parent = json.loads(parent_raw)
    wizard = json.loads(wizard_raw)
    profile = json.loads(profile_raw)
    if parent["finalSHA256"] != EXPECTED["parent_final"]:
        raise ValueError("Historical parent final state hash changed")
    if digest(parent["final"]) != EXPECTED["parent_final"]:
        raise ValueError("Canonical parent final state hash does not match its receipt")
    actor = parent["final"]["actors"]["A"]
    if actor["position"] != [25, 10, 0]:
        raise ValueError("Parent actor position differs from the reviewed fixture")
    if actor["RP"] != 54 or actor["Dissonance"] != 0 or actor["Refrain"] != 0:
        raise ValueError("Parent actor resource state differs from the reviewed fixture")
    if profile["abilityScores"]["STR"] != 12:
        raise ValueError("Bound actor Strength score differs from the reviewed profile")
    minor = next(c for c in wizard["cards"] if c["id"] == "wizard.base.minor-conjuration")
    if minor["cost"] != "1 RP" or minor["activation"] != "Action" or minor["spellRank"] != 1:
        raise ValueError("Bound Minor Conjuration card no longer matches the witness route")

    rulebook = INTAKE / "payload" / "sources" / "PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt"
    combat = INTAKE / "payload" / "sources" / "COMBAT_ACTION_PLAYTEST.md"
    q23 = INTAKE / "payload" / "rules" / "PG328_QUESTION_DISPOSITIONS.json"
    blocker = INTAKE / "payload" / "authority" / "PG328_BLOCKER_REASSESSMENT.json"
    preflight = BASE / "fortress_w01_structural_damage_source_preflight_396" / "OWNER_PG328_W01_STRUCTURAL_DAMAGE_SOURCE_PREFLIGHT_396_TESTONLY.json"
    source_paths = {
        "rulebook": rulebook,
        "combat": combat,
        "q23": q23,
        "blocker": blocker,
        "preflight": preflight,
        "queue": BASE / "CURRENT_SPELL_QUEUE_361.json",
        "handoff": BASE / "CURRENT_HANDOFF_361.json",
    }
    for name, expected in EXPECTED.items():
        if name in source_paths and sha256(source_paths[name].read_bytes()) != expected:
            raise ValueError(f"Bound source hash changed: {name}")

    base_state = copy.deepcopy(parent["final"])
    space_id = parent["final"]["effects"]["RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1"]["space"]
    branch_initial = copy.deepcopy(base_state)
    branch_initial["spaces"][space_id]["w01PartialStructureWitness"] = {
        "id": "PG328-W01-LOCAL-GEOMETRY-400",
        "classification": "TEST_ONLY_BRANCH_GEOMETRY; PARTIAL_SUBWITNESS",
        "wholeStructureMapComplete": False,
        "panelInstances": {
            "W01-SOUTH-WALL-X25-Z0": {
                "kind": "outer-wall panel",
                "boundsFeet": {"x": [25, 30], "y": [0, 5], "z": [0, 5]},
                "ac": 17,
                "initialHp": 60,
                "currentHp": 60,
                "material": "stone-like, matching Q23 profile",
                "geometryProvenance": "TEST_ONLY exact 5-foot panel coordinate choice within Q23's 5-foot-thick, 30-foot-high outer wall; no source dimension changed",
                "mechanicalSupportStatus": "UNADJUDICATED",
                "destroyed": False,
            },
            "W01-SOUTH-WALL-X20-Z0": {
                "boundsFeet": {"x": [20, 25], "y": [0, 5], "z": [0, 5]},
                "ac": 17,
                "hp": 60,
                "mechanicalSupportStatus": "UNADJUDICATED",
            },
            "W01-SOUTH-WALL-X30-Z0": {
                "boundsFeet": {"x": [30, 35], "y": [0, 5], "z": [0, 5]},
                "ac": 17,
                "hp": 60,
                "mechanicalSupportStatus": "UNADJUDICATED",
            },
            "W01-SOUTH-WALL-X25-Z5": {
                "boundsFeet": {"x": [25, 30], "y": [0, 5], "z": [5, 10]},
                "ac": 17,
                "hp": 60,
                "mechanicalSupportStatus": "UNADJUDICATED",
            },
        },
        "geometricContacts": [
            {"a": "W01-SOUTH-WALL-X25-Z0", "b": "W01-SOUTH-WALL-X20-Z0", "surface": "shared x=25 plane", "mechanicalMeaning": "none inferred"},
            {"a": "W01-SOUTH-WALL-X25-Z0", "b": "W01-SOUTH-WALL-X30-Z0", "surface": "shared x=30 plane", "mechanicalMeaning": "none inferred"},
            {"a": "W01-SOUTH-WALL-X25-Z0", "b": "W01-SOUTH-WALL-X25-Z5", "surface": "shared z=5 plane", "mechanicalMeaning": "none inferred"},
            {"a": "W01-SOUTH-WALL-X25-Z0", "b": "Q23-GROUND-SUPPORT-z0", "surface": "shared z=0 plane", "mechanicalMeaning": "none inferred"},
        ],
        "supportDisposition": "All listed relationships are geometric contact only. No load capacity, valid-support edge, threshold, propagation, collapse, or Falling rule is adopted. Support validity remains UNADJUDICATED.",
        "localNavigation": {
            "actorStart": [25, 10, 0],
            "actorBodyFeet": [5, 5, 6],
            "openCourtyardBounds": [5, 115, 5, 115],
            "selectedPanelInteriorFace": {"y": 5, "x": [25, 30], "z": [0, 5]},
            "approachPath": [[25, 10, 0], [25, 5, 0]],
            "approachDistanceFeet": 5,
            "endBodyBoundsFeet": {"x": [25, 30], "y": [5, 10], "z": [0, 6]},
            "bodyPanelIntersection": False,
            "status": "LOCAL COURTYARD APPROACH REPRESENTED; WHOLE FORTRESS NAVIGATION NOT VALIDATED",
        },
        "requiredOpenPredicate": {
            "id": "PG328-W01-KEEP-STAIR-LANDING-GEOMETRY",
            "sourcePointer": "payload/rules/PG328_QUESTION_DISPOSITIONS.json#/questions/2/answer",
            "status": "UNADJUDICATED",
            "reason": "Q23's 5x15-foot stairwell, thirty half-foot treads and two 5x5-foot landings do not fit the full stated run-plus-landings; Director found the proposed adjacent-landing arrangement cannot prove a continuous supported approach for a 5x5x6 body. No owner-approved source repair is included.",
        },
    }

    state = copy.deepcopy(branch_initial)
    snapshots = {"S000_PARENT_PLUS_TESTONLY_GEOMETRY": copy.deepcopy(state)}
    events: list[dict[str, object]] = []

    def advance_to(when: float) -> None:
        prior = float(state["time"])
        if when < prior:
            raise ValueError(f"Non-monotonic time: {when} < {prior}")
        delta = when - prior
        state["time"] = when
        clock = state["clock"]
        clock["elapsedSeconds"] = float(clock["elapsedSeconds"]) + delta
        for name in ("OpeningRemaining", "HornRemaining"):
            clock[name] = float(clock[name]) - delta

    def add_event(event_id: str, when: float, kind: str, narrative: str, apply=None, inputs=None) -> None:
        before = copy.deepcopy(state)
        advance_to(when)
        if apply is not None:
            apply()
        state["processedEventIds"].append(event_id)
        after = copy.deepcopy(state)
        forward = diff(before, after)
        inverse = diff(after, before)
        if apply_patch(before, forward) != after or apply_patch(after, inverse) != before:
            raise AssertionError(f"Patch replay failed: {event_id}")
        before_id = f"S{len(snapshots)-1:03d}"
        after_id = f"S{len(snapshots):03d}"
        snapshots[after_id] = after
        events.append(
            {
                "eventId": event_id,
                "time": when,
                "kind": kind,
                "narrative": narrative,
                "authoredInputs": inputs or {},
                "beforeStateId": before_id,
                "afterStateId": after_id,
                "beforeSha256": digest(before),
                "afterSha256": digest(after),
                "forwardPatch": forward,
                "inversePatch": inverse,
            }
        )

    def start(actor_id: str, when: float) -> None:
        def action() -> None:
            turn_start(state, actor_id, when)
        add_event(f"PG328-W01-400:TURN-START-{actor_id}-{when:g}", when, "REGULAR_TURN_START", f"{actor_id} regular turn starts; no unrecorded resource refresh is assumed.", action)

    def end(actor_id: str, when: float) -> None:
        def action() -> None:
            turn_end(state, actor_id, when)
        add_event(f"PG328-W01-400:TURN-END-{actor_id}-{when:g}", when, "REGULAR_TURN_END", f"{actor_id} regular turn ends; no action or resource use is added beyond listed events.", action)

    # Continue from the immutable Return284 parent and include every intervening regular slot.
    start("C", 2.0)
    end("C", 2.9)
    start("D", 3.0)
    end("D", 3.9)
    start("A", 6.0)

    cast_id = "PG328-W01-400:MINOR-CONJURATION-1"
    tile_id = "PG328-W01-400:CLAY-TILE-1"
    space = state["actors"]["A"]["plane"]

    def cast_minor() -> None:
        a = state["actors"]["A"]
        if a["action"] != 1 or a["RP"] < 1:
            raise ValueError("A lacks the scheduled Action or 1 RP")
        a["action"] = 0
        a["RP"] -= 1
        a["lastSpell"] = "wizard.base.minor-conjuration"
        if "wizard.base.minor-conjuration" not in a["preparedFamiliesUsed"]:
            a["preparedFamiliesUsed"].append("wizard.base.minor-conjuration")
        a["spellHistory"].append(
            {
                "castId": cast_id,
                "spellId": "wizard.base.minor-conjuration",
                "class": "Wizard",
                "school": "Conjuration",
                "rank": 1,
                "time": 6.1,
                "cost": 1,
                "firstPreparedFamily": True,
                "baseDissonance": 0,
                "Refrain": 0,
                "originPlane": space,
                "target": [25, 9, 0],
                "concentration": False,
            }
        )
        a["resourceHistory"].append({"event": cast_id, "RP": -1, "poolAfter": 53, "discount": False})
        a["magicThisTurn"] = True
        state["items"][tile_id] = {
            "id": tile_id,
            "massLb": 2,
            "load": 0.2,
            "owner": None,
            "custodian": None,
            "plane": space,
            "position": [25, 9, 0],
            "exists": True,
            "quantity": 1,
            "provenance": "Minor Conjuration; common nonvaluable nonmagical clay; TEST_ONLY temporary object",
            "consumed": False,
            "sizeFeet": [1, 1, 0.25],
            "createdAtEventTime": 6.1,
            "expiresAtEventTime": 3606.1,
            "unattendedAtCreation": True,
        }

    add_event(
        cast_id,
        6.1,
        "CAST_COMMIT_AND_RESOLVE",
        "A casts its acquired, always-prepared Minor Conjuration as its Action and creates one qualifying temporary clay tile.",
        cast_minor,
        {
            "sourceCard": "current_bound_wizard.json#/cards/6",
            "activation": "Action",
            "printedCost": "1 RP",
            "range": "one unoccupied space within 10 feet",
            "createdObject": {"id": tile_id, "material": "common clay", "sizeFeet": [1, 1, 0.25], "weightLb": 2, "wieldability": "one-handed TEST_ONLY physical input; no weapon proficiency asserted"},
            "targetSpace": [25, 9, 0],
            "components": "No component list is printed on the bound card; no unprinted component or material cost is assumed.",
            "focus": {"focusAccessible": True, "focusItem": "focus-A", "profileHand": "left", "rightHandFreeBeforePickup": True},
            "strain": {"preparedMatrixFamily": "wizard.base.minor-conjuration", "firstDistinctFamilyInEncounter": True, "baseDissonance": 0, "Refrain": 0, "spellEfficiencyDiscount": False},
            "interrupts": "No interruption event is authored. No hostile counterspell actor/eligibility is established by the parent; this is not a counterspell-negative witness.",
            "duration": "1 hour; object expiry at event time 3606.1, well after the witnessed 12.1 attack.",
        },
    )

    def pickup_tile() -> None:
        a = state["actors"]["A"]
        tile = state["items"][tile_id]
        if a["action"] != 0 or a["equipment"].count(tile_id) != 0:
            raise ValueError("Pickup preconditions differ")
        tile["custodian"] = "A"
        tile["position"] = None
        tile["heldBy"] = "A:right"
        a["equipment"].append(tile_id)
        a["carriedWeightLb"] = 14
        a["carriedLoad"] = 1.4
        a["w01HandState"] = {"left": "focus-A", "right": tile_id}

    add_event(
        "PG328-W01-400:PICKUP-CLAY-TILE",
        6.2,
        "FREE_OBJECT_INTERACTION",
        "A picks up the adjacent created tile with the otherwise-free right hand using the turn's single ordinary free object interaction.",
        pickup_tile,
        {"interactionCountThisTurn": 1, "targetItem": tile_id, "hand": "right", "additionalActionUsed": False},
    )

    def move_adjacent() -> None:
        a = state["actors"]["A"]
        if a["movement"] < 5 or a["position"] != [25, 10, 0]:
            raise ValueError("A cannot make the selected 5-foot movement")
        a["movement"] -= 5
        a["position"] = [25, 5, 0]

    add_event(
        "PG328-W01-400:MOVE-5FT-TO-PANEL",
        6.3,
        "VOLUNTARY_MOVEMENT",
        "A moves 5 feet through the clear courtyard to the selected panel's inside face; the 5x5x6 body ends face-adjacent without intersecting the wall.",
        move_adjacent,
        {
            "sourceRule": "COMBAT_ACTION_PLAYTEST.md movement rules plus Q23 courtyard bounds",
            "from": [25, 10, 0],
            "to": [25, 5, 0],
            "movementSpentFeet": 5,
            "movementRemainingFeet": 25,
            "bodyBoundsAfterFeet": {"x": [25, 30], "y": [5, 10], "z": [0, 6]},
            "wallPanelBoundsFeet": {"x": [25, 30], "y": [0, 5], "z": [0, 5]},
            "intersection": False,
        },
    )
    end("A", 6.9)
    start("B", 7.0)
    end("B", 7.9)
    start("C", 8.0)
    end("C", 8.9)
    start("D", 9.0)
    end("D", 9.9)
    start("A", 12.0)

    def attack_panel() -> None:
        a = state["actors"]["A"]
        model = state["spaces"][space_id]["w01PartialStructureWitness"]
        panel = model["panelInstances"]["W01-SOUTH-WALL-X25-Z0"]
        if a["action"] != 1 or a["position"] != [25, 5, 0] or a["RP"] != 53:
            raise ValueError("Attack preconditions differ")
        if panel["currentHp"] != 60 or not state["items"][tile_id]["exists"]:
            raise ValueError("Panel/object state differs at attack time")
        a["action"] = 0
        panel["currentHp"] = 55
        panel["destroyed"] = False
        panel["lastDamage"] = {
            "eventId": "PG328-W01-400:ATTACK-SUNDER-SOUTH-PANEL",
            "amount": 5,
            "type": "bludgeoning",
            "hpBefore": 60,
            "hpAfter": 55,
        }

    add_event(
        "PG328-W01-400:ATTACK-SUNDER-SOUTH-PANEL",
        12.1,
        "ATTACK_SUNDER_OBJECT",
        "A makes one ordinary melee improvised-weapon Attack/Sunder against the named south outer-wall panel using the still-existing tile.",
        attack_panel,
        {
            "weaponObject": tile_id,
            "targetPanel": "W01-SOUTH-WALL-X25-Z0",
            "contactGeometry": "A's body is face-adjacent to the panel's interior face at y=5; the wielded tile contacts the panel. No reach extension is claimed.",
            "attack": {"d20": 16, "strengthModifier": 1, "proficiencyBonus": 0, "total": 17, "panelAC": 17, "result": "hit"},
            "damage": {"d4": 4, "strengthModifier": 1, "total": 5, "type": "bludgeoning", "directorAssignment": True},
            "economy": {"actionUsed": True, "RPSpent": 0, "DissonanceChange": 0, "RefrainChange": 0, "tileConsumed": False},
            "structuralConsequence": {
                "panelHpBefore": 60,
                "panelHpAfter": 55,
                "panelDestroyed": False,
                "supportRemovalTriggered": False,
                "navigationOpeningCreated": False,
                "supportValidity": "UNADJUDICATED",
                "wholeNavigation": "UNADJUDICATED; keep stair predicate remains open",
            },
            "sourceBindings": [
                "PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt lines 6828, 6832, 6732, 7865, 8227, 8231",
                "COMBAT_ACTION_PLAYTEST.md lines 31, 76, 136",
                "Q23 /questions/2/answer",
                "Director assignment: bludgeoning for the nonweaponlike clay object's impact",
            ],
            "interrupts": "No interruption event is authored; no hostile counterspell actor/eligibility is established by the parent; this is not a counterspell-negative witness.",
        },
    )
    end("A", 12.9)

    # Validate every forward patch and every inverse in exact reverse event order.
    replay = copy.deepcopy(branch_initial)
    for event in events:
        if digest(replay) != event["beforeSha256"]:
            raise AssertionError(f"Wrong before-state for {event['eventId']}")
        replay = apply_patch(replay, event["forwardPatch"])
        if digest(replay) != event["afterSha256"]:
            raise AssertionError(f"Wrong after-state for {event['eventId']}")
    terminal = copy.deepcopy(replay)
    for event in reversed(events):
        terminal = apply_patch(terminal, event["inversePatch"])
    if terminal != branch_initial:
        raise AssertionError("Inverse replay did not restore the branch start")
    restored_parent = copy.deepcopy(terminal)
    del restored_parent["spaces"][space_id]["w01PartialStructureWitness"]
    if restored_parent != base_state:
        raise AssertionError("Removing the TEST_ONLY annotation did not restore the immutable parent final state")
    final_panel = replay["spaces"][space_id]["w01PartialStructureWitness"]["panelInstances"]["W01-SOUTH-WALL-X25-Z0"]
    final_a = replay["actors"]["A"]
    if final_panel["currentHp"] != 55 or final_panel["destroyed"] or final_a["RP"] != 53:
        raise AssertionError("Final W01 sub-witness state is inconsistent")
    if replay["items"][tile_id]["custodian"] != "A" or final_a["position"] != [25, 5, 0]:
        raise AssertionError("Final object custody or actor position is inconsistent")

    source_records = []
    for label, raw, name, pointer in [
        ("PG328 held archive", ARCHIVE.read_bytes(), str(ARCHIVE.relative_to(BASE)), None),
        ("historical parent case member", parent_raw, f"{ARCHIVE.relative_to(BASE)}::{PARENT_MEMBER}", "/final"),
        ("current bound Wizard source", wizard_raw, f"{ARCHIVE.relative_to(BASE)}::{WIZARD_MEMBER}", "/cards/6; /engine/12; protectedInterfaceOriginal"),
        ("conditional actor profile", profile_raw, f"{ARCHIVE.relative_to(BASE)}::{PROFILE_MEMBER}", "/abilityScores/STR; /acquisitionLedger/0/choices/1; /alwaysPrepared/1"),
    ]:
        source_records.append({"label": label, "source": name, "jsonPointer": pointer, "bytes": len(raw), "sha256": sha256(raw)})
    for label, path, pointer in [
        ("Rulebook v6", rulebook, "lines 6828, 6832, 6732, 7865, 8227, 8231"),
        ("Combat Action playtest", combat, "lines 31, 76, 136"),
        ("PG9-Q23 disposition", q23, "/questions/2/answer"),
        ("PG328 blocker reassessment", blocker, "/remainingWitnessParts/0; /sourceLevelGains/3"),
        ("Director-confirmed W01 preflight", preflight, "/candidateAssessment/0; /preflightFinding/remainingPredicates"),
    ]:
        raw = path.read_bytes()
        source_records.append({"label": label, "source": str(path.relative_to(BASE)), "jsonPointer": pointer, "bytes": len(raw), "sha256": sha256(raw)})

    OUT.mkdir(parents=True)
    owner_auth = {
        "id": "OWNER-PG328-W01-CONSTRUCTION-AUTHORIZATION-400",
        "status": "OWNER_AUTHORIZED_TEST_ONLY_BRANCH_CONSTRUCTION",
        "scope": "REVERSIBLE_TEST_ONLY_PG328_W01_DAMAGE_SUBWITNESS",
        "ownerInstruction": "Complete the remaining pending spell review identities; continue until pending reaches zero.",
        "directorAuthorization": "Resume the already-authorized TEST_ONLY PG328-W01 construction: lawful non-destructive damage event, reversible state history, and unaffected panel/support/navigation geometry. Construction does not establish witness sufficiency or seal.",
        "directorThread": "Review Time Stop Witness Evidence",
        "directorThreadId": "6ae5c784-afec-83e9-a2ca-5e2638b95750",
        "authorizedActs": ["source-bound reversible test-only construction", "Director review submission"],
        "notAuthorized": ["source repair", "mechanical support/collapse rule", "W01 seal", "Fortress acceptance/application", "canon or fixture mutation", "spell queue mutation"],
    }
    geometry = {
        "id": "PG328-W01-LOCAL-GEOMETRY-400",
        "classification": "TEST_ONLY_BRANCH_GEOMETRY_PARTIAL_SUBWITNESS",
        "source": {"path": str(q23.relative_to(BASE)), "sha256": EXPECTED["q23"], "pointer": "/questions/2/answer"},
        "preservedQ23": {"outerWallThicknessFeet": 5, "outerWallHeightFeet": 30, "panelBoundsFeet": [5, 5, 5], "panelAC": 17, "panelHP": 60, "courtyardBoundsFeet": [5, 115, 5, 115]},
        "branchChoices": {
            "wallOrientation": "south wall at y=0..5",
            "selectedPanelId": "W01-SOUTH-WALL-X25-Z0",
            "selectedPanelBoundsFeet": {"x": [25, 30], "y": [0, 5], "z": [0, 5]},
            "adjacentActorEndPosition": [25, 5, 0],
            "actorBodyFeet": [5, 5, 6],
            "mainGateCoordinateChoice": "Not used for this local approach; the historical aperture and entry path are preserved from the parent.",
        },
        "contactGraph": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["geometricContacts"],
        "mechanicalSupportGraph": "UNADJUDICATED. Contacts are not support edges; no threshold, capacity, collapse propagation or Falling rule is introduced.",
        "localNavigation": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["localNavigation"],
        "wholeStructureNavigation": "UNADJUDICATED; not a complete Fortress map. The keep-stair contradiction remains open under Q23, and no source repair is adopted.",
        "sealEligibility": False,
    }
    replay_record = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-400",
        "classification": "REVERSIBLE_TEST_ONLY_SUBWITNESS_SUBMITTED_FOR_DIRECTOR_REVIEW",
        "historicalParent": {"member": PARENT_MEMBER, "memberSha256": EXPECTED["parent_member"], "finalSha256": EXPECTED["parent_final"], "handling": "immutable; branch begins from an exact copy"},
        "branchInitialStateId": "S000_PARENT_PLUS_TESTONLY_GEOMETRY",
        "branchInitialStateSha256": digest(branch_initial),
        "stateSnapshots": snapshots,
        "events": events,
        "terminalStateId": events[-1]["afterStateId"],
        "terminalStateSha256": digest(replay),
        "targetDamage": {"panelId": "W01-SOUTH-WALL-X25-Z0", "hpBefore": 60, "hpAfter": 55, "damage": 5, "damageType": "bludgeoning", "destroyed": False},
        "restoration": {"inverseOrder": [e["eventId"] for e in reversed(events)], "restoresBranchInitial": True, "removingTestOnlyGeometryRestoresParentFinal": True, "parentFinalSha256": EXPECTED["parent_final"]},
        "queueAndDecisionState": {"applied": 828, "pending": 20, "acceptedUnapplied": 0, "fortressAccepted": False, "fortressApplied": False, "witnessSealed": False, "applicationAuthorized": False},
    }
    request = """# Director review request: PG328-W01 damage sub-witness 400\n\nPlease review the attached TEST_ONLY partial construction against PG328-W01. It binds the immutable Return284 parent, Minor Conjuration, a lawful improvised-object/Sunder route, the one-RP resource/action timeline, a five-foot courtyard approach to a specifically named Q23 wall panel, and a reversible d20/d4 hit that changes the selected panel from 60 to 55 HP.\n\nThe packet deliberately does not seal W01. It leaves whole-structure support validity and the keep-stair landing connection UNADJUDICATED, and it does not adopt a support, collapse, or source-repair rule. Please state whether the damage subpredicate and local contact/approach portion are source-sufficient; list exact residual predicates for a complete W01; and confirm that this submission changes no Fortress acceptance, application, hold, seal, source rule, canonical file, fixture, or Queue361 state.\n"""

    file_map: dict[str, bytes] = {}
    file_map["OWNER_W01_CONSTRUCTION_AUTHORIZATION_400.json"] = write_json(OUT / "OWNER_W01_CONSTRUCTION_AUTHORIZATION_400.json", owner_auth)
    file_map["SOURCE_BINDINGS_400.json"] = write_json(OUT / "SOURCE_BINDINGS_400.json", {"id": "PG328-W01-SOURCE-BINDINGS-400", "sources": source_records})
    file_map["W01_GEOMETRY_400.json"] = write_json(OUT / "W01_GEOMETRY_400.json", geometry)
    file_map["W01_REPLAY_400.json"] = write_json(OUT / "W01_REPLAY_400.json", replay_record)
    file_map["DIRECTOR_REVIEW_REQUEST_400.md"] = (OUT / "DIRECTOR_REVIEW_REQUEST_400.md").write_text(request, encoding="utf-8") and (OUT / "DIRECTOR_REVIEW_REQUEST_400.md").read_bytes()
    readme = """# PG328-W01 TEST_ONLY damage sub-witness 400\n\nThis packet records one reversible, source-bound, non-destructive wall-panel damage branch. It uses the preserved Return284 final state, acquired/always-prepared Minor Conjuration, a temporary 2 lb clay tile, one ordinary free pickup, a 5 ft courtyard approach, and one Attack/Sunder hit. The chosen wall panel moves from 60 to 55 HP.\n\nThis is a partial sub-witness. It does not establish the complete Fortress support graph or navigation graph; the keep stair remains UNADJUDICATED. No support/collapse rule is added, and no seal, spell acceptance/application, source mutation, fixture mutation, or queue change is requested.\n"""
    file_map["README_400.md"] = (OUT / "README_400.md").write_text(readme, encoding="utf-8") and (OUT / "README_400.md").read_bytes()

    verification = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-VERIFICATION-400",
        "status": "PASS_PARTIAL_TEST_ONLY_REPLAY; W01_OPEN",
        "checks": {
            "sourceHashes": "PASS",
            "historicalParentFinalHash": "PASS",
            "forwardPatchesInOrder": "PASS",
            "inversePatchesReverseOrder": "PASS",
            "fullParentRestoration": "PASS",
            "minorConjurationCost": "1 RP; PASS",
            "tileWithinCardSizeAndWeight": "PASS",
            "firstDistinctMatrixBaseDissonance": "0; PASS",
            "turnAndInteractionBudgets": "PASS",
            "attackArithmetic": "17 vs AC17; hit; PASS",
            "damageArithmetic": "5 bludgeoning; 60 to 55; PASS",
            "unresolvedSupportAndNavigationMarkedOpen": "PASS",
            "witnessSeal": "NOT ISSUED",
            "fortressAcceptanceApplication": "NOT AUTHORIZED",
            "queueMutation": "NONE; 828/20/0 preserved",
        },
        "eventCount": len(events),
        "stateSnapshotCount": len(snapshots),
        "eventHashes": [{"eventId": e["eventId"], "before": e["beforeSha256"], "after": e["afterSha256"]} for e in events],
        "openPredicates": ["complete panel/support map", "mechanical support validity", "whole-structure legal navigation", "keep-stair/landing geometry under PG9-Q23"],
    }
    file_map["VERIFICATION_400.json"] = write_json(OUT / "VERIFICATION_400.json", verification)
    crc_rows = []
    for name, raw in sorted(file_map.items()):
        crc_rows.append({"path": name, "bytes": len(raw), "sha256": sha256(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
    manifest = {"id": "PG328-W01-DAMAGE-SUBWITNESS-MANIFEST-400", "schemaVersion": 1, "members": crc_rows}
    manifest_raw = write_json(OUT / "MANIFEST_400.json", manifest)
    zip_path = OUT / ARCHIVE_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(file_map):
            zf.writestr(name, file_map[name])
        zf.writestr("MANIFEST_400.json", manifest_raw)
    archive_raw = zip_path.read_bytes()
    delivery = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-DELIVERY-400",
        "status": "READY_FOR_DIRECTOR_REVIEW; PARTIAL_WITNESS; NO_SEAL",
        "archive": {"path": ARCHIVE_NAME, "bytes": len(archive_raw), "sha256": sha256(archive_raw)},
        "manifest": {"path": "MANIFEST_400.json", "bytes": len(manifest_raw), "sha256": sha256(manifest_raw)},
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["conjure-demiplane-fortress"],
        "blockerIds": ["PG200-B06"],
        "queue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
        "witnessSealed": False,
        "applicationAuthorized": False,
        "canonicalMutation": False,
        "fixtureMutation": False,
        "queueMutation": False,
    }
    write_json(OUT / "DELIVERY_400.json", delivery)

    # Check archived members against the manifest and re-open the zip.
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        expected_names = set(file_map) | {"MANIFEST_400.json"}
        if names != expected_names:
            raise AssertionError("Archive member set differs from the generated manifest")
        for row in crc_rows:
            raw = zf.read(row["path"])
            if len(raw) != row["bytes"] or sha256(raw) != row["sha256"] or f"{zlib.crc32(raw) & 0xffffffff:08x}" != row["crc32"]:
                raise AssertionError(f"Archive member integrity mismatch: {row['path']}")
        if zf.testzip() is not None:
            raise AssertionError("Zip CRC/decompression verification failed")

    print(json.dumps({"output": str(OUT), "archive": str(zip_path), "archiveSha256": sha256(archive_raw), "eventCount": len(events), "stateCount": len(snapshots), "status": "PASS_PARTIAL_TEST_ONLY_REPLAY; W01_OPEN"}, indent=2))


if __name__ == "__main__":
    main()
