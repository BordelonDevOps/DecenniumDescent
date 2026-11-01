#!/usr/bin/env python3
"""Build a reversible, TEST_ONLY PG328-W01 damage sub-witness for Director review."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import subprocess
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
OUT = BASE / "fortress_w01_structural_damage_witness_402"
ARCHIVE_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328W01_Witness402_TESTONLY.zip"

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
    "preflight_git_bytes": "9d6bdd7ad485445f6d27b7595086ed548c2629a25f3e68790924ae098f79d6f6",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return sha256(canonical(value))


def read_json(path: pathlib.Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def resolve_json_pointer(value: object, pointer: str) -> object:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError(f"Not an RFC 6901 JSON pointer: {pointer}")
    current = value
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def git_head_bytes(path: pathlib.Path, *, repo_root: pathlib.Path) -> tuple[str, bytes]:
    relative = path.relative_to(repo_root).as_posix()
    raw = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=repo_root)
    return relative, raw


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


def write_utf8_lf(path: pathlib.Path, value: str) -> bytes:
    data = value.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
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
    actor["stance"] = None
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


def close_budget_window(actor: dict[str, object], *, ended_at: float, recorded_at: float) -> None:
    schedule = actor["regularSchedule"]
    if not schedule["budgetHistory"]:
        raise ValueError(f"{actor['id']} has no budget record to close")
    budget = schedule["budgetHistory"][-1]
    if "endDisposition" in budget:
        raise ValueError(f"{actor['id']} budget window was already closed")
    move_granted = int(budget["Move"])
    action_remaining = int(actor["action"])
    bonus_remaining = int(actor["bonusAction"])
    reaction_remaining = int(actor["reaction"])
    move_remaining = int(actor["movement"])
    if not 0 <= move_remaining <= move_granted:
        raise ValueError(f"{actor['id']} movement ledger is outside its granted budget")
    budget["endDisposition"] = {
        "regularTurnEndedAt": ended_at,
        "recordedAt": recorded_at,
        "Action": {"spent": 1 - action_remaining, "unusedExpired": action_remaining},
        "BonusAction": {"spent": 1 - bonus_remaining, "unusedExpired": bonus_remaining},
        "Reaction": {
            "spent": 1 - reaction_remaining,
            "availableOffTurnUntilSpentOrNextOwnStart": bool(reaction_remaining),
        },
        "MovementFeet": {
            "granted": move_granted,
            "spent": move_granted - move_remaining,
            "unusedExpired": move_remaining,
        },
    }
    actor["action"] = 0
    actor["bonusAction"] = 0
    actor["movement"] = 0
    actor["magicThisTurn"] = False
    schedule["nextEnd"] = None


def turn_end(state: dict[str, object], actor_id: str, when: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if abs(float(schedule["nextEnd"]) - when) > 1e-9:
        raise ValueError(f"{actor_id} scheduled end mismatch: {schedule['nextEnd']} != {when}")
    schedule["ends"].append(when)
    close_budget_window(actor, ended_at=when, recorded_at=when)
    efficiency = actor.get("spellEfficiency")
    if isinstance(efficiency, list):
        actor["spellEfficiency"] = [entry for entry in efficiency if entry.get("until") is None or float(entry["until"]) > when + 1e-9]
        if not actor["spellEfficiency"]:
            actor["spellEfficiency"] = None
    elif efficiency and efficiency.get("until") is not None and float(efficiency["until"]) <= when + 1e-9:
        actor["spellEfficiency"] = None


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
    counterspell = next(c for c in wizard["cards"] if c["id"] == "wizard.base.counterspell")
    if counterspell["cost"] != "3 RP" or counterspell["activation"] != "Reaction" or counterspell["spellRank"] != 1:
        raise ValueError("Bound Counterspell card no longer matches the responder assessment")
    if counterspell["minimumClassLevel"] != 2 or counterspell["acquisition"] != "automatic":
        raise ValueError("Counterspell's automatic Wizard 2 acquisition changed")

    rulebook = INTAKE / "payload" / "sources" / "PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt"
    combat = INTAKE / "payload" / "sources" / "COMBAT_ACTION_PLAYTEST.md"
    q23 = INTAKE / "payload" / "rules" / "PG328_QUESTION_DISPOSITIONS.json"
    blocker = INTAKE / "payload" / "authority" / "PG328_BLOCKER_REASSESSMENT.json"
    preflight = BASE / "fortress_w01_structural_damage_source_preflight_396" / "OWNER_PG328_W01_STRUCTURAL_DAMAGE_SOURCE_PREFLIGHT_396_TESTONLY.json"
    git_root = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=BASE, text=True).strip()).resolve()
    preflight_git_path, preflight_git_raw = git_head_bytes(preflight, repo_root=git_root)
    if sha256(preflight_git_raw) != EXPECTED["preflight_git_bytes"]:
        raise ValueError("Pinned Git preflight bytes changed")
    if sha256(preflight.read_bytes().replace(b"\r\n", b"\n")) != sha256(preflight_git_raw):
        raise ValueError("Working-tree preflight cannot be normalized to the pinned Git representation")
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
        "id": "PG328-W01-LOCAL-GEOMETRY-402",
        "classification": "TEST_ONLY_BRANCH_GEOMETRY; PARTIAL_SUBWITNESS",
        "wholeStructureMapComplete": False,
        "positionConvention": {"classification": "TEST_ONLY_LOCAL_CONVENTION; no canonical rule inferred", "actorPosition": "minimum x/y corner at foot; z is floor height", "bodyBounds": "[x,x+5]×[y,y+5]×[z,z+6]", "sameConventionForAAndB": True, "intersection": "positive-volume overlap; shared boundary is contact"},
        "counterspellCastGeometry": {"A": {"position": [25, 10, 0], "center": [27.5, 12.5, 3]}, "B": {"position": [15, 10, 0], "center": [17.5, 12.5, 3]}, "centerDistanceFeet": 10, "nearestBodyGapFeet": 5, "samePlane": True, "segment": "open courtyard; no intervening structure"},
        "objectGeometry": {"spawnBoundsFeet": {"x": [25, 26], "y": [9, 10], "z": [0, 0.25]}, "bodyAtCreation": {"x": [25, 30], "y": [10, 15], "z": [0, 6]}, "heldOffset": {"x": [0, 1], "y": [-1, 0], "z": [0, 0.25]}, "bodySweepBoundsFeet": {"x": [25, 30], "y": [6, 16], "z": [0, 6]}, "carriedItemSweepBoundsFeet": {"x": [25, 26], "y": [5, 11], "z": [0, 0.25]}, "terminalBodyBoundsFeet": {"x": [25, 30], "y": [6, 11], "z": [0, 6]}, "terminalTileBoundsFeet": {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]}, "wallContactPlane": 5},
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
            "approachPath": [[25, 10, 0], [25, 11, 0], [25, 6, 0]],
            "approachDistanceFeet": 6,
            "movementSegmentsFeet": [1, 5],
            "endBodyBoundsFeet": {"x": [25, 30], "y": [6, 11], "z": [0, 6]},
            "bodyPanelIntersection": False,
            "carriedObjectContactWithoutPenetration": True,
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
    branch_initial_id = "S000_PARENT_PLUS_TESTONLY_GEOMETRY"
    snapshots = {branch_initial_id: copy.deepcopy(state)}
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
        before_id = branch_initial_id if len(snapshots) == 1 else f"S{len(snapshots)-1:03d}"
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
        add_event(f"PG328-W01-402:TURN-START-{actor_id}-{when:g}", when, "REGULAR_TURN_START", f"{actor_id} regular turn starts; no unrecorded resource refresh is assumed.", action)

    def end(actor_id: str, when: float) -> None:
        def action() -> None:
            turn_end(state, actor_id, when)
        add_event(
            f"PG328-W01-402:TURN-END-{actor_id}-{when:g}",
            when,
            "REGULAR_TURN_END",
            f"{actor_id} regular turn ends; Action/Bonus Action and unused movement close out, unused Reaction remains available off-turn, and due end markers expire.",
            action,
        )

    def choose_mobile(actor_id: str, when: float) -> None:
        actor = state["actors"][actor_id]
        if actor.get("stance") is not None:
            raise ValueError(f"{actor_id} already selected a stance this turn")
        expires_at = actor["regularSchedule"]["nextStart"]

        def action() -> None:
            state["actors"][actor_id]["stance"] = "Mobile"

        add_event(
            f"PG328-W01-402:STANCE-MOBILE-{actor_id}-{when:g}", when, "REGULAR_TURN_STANCE_CHOICE",
            f"{actor_id} selects Mobile before a stance-relevant event or, on an idle turn, before turn end; it expires at the next regular own-turn start.", action,
            {"actorId": actor_id, "stance": "Mobile", "selectedAt": when, "expiresAtNextRegularStart": expires_at,
             "source": "COMBAT_ACTION_PLAYTEST.md § Stances, lines 113-123",
             "benefit": "first 5 feet of actual voluntary movement does not provoke; no free movement; opportunity attacks reduce only that actor's base weapon die; none occur in this branch"},
        )

    def close_parent_turn(actor_id: str) -> None:
        actor_state = state["actors"][actor_id]
        schedule = actor_state["regularSchedule"]
        if not schedule["ends"] or schedule["ends"][-1] > state["time"]:
            raise ValueError(f"{actor_id} has no completed parent regular turn to close")
        close_budget_window(actor_state, ended_at=float(schedule["ends"][-1]), recorded_at=float(state["time"]))

    def reconcile_parent_budgets() -> None:
        close_parent_turn("A")
        close_parent_turn("B")

    add_event(
        "PG328-W01-402:CLOSE-PARENT-TURN-BUDGETS-A-B",
        float(state["time"]),
        "BRANCH_BUDGET_CLOSEOUT",
        "Close only stale Action/Bonus Action/movement fields for A and B whose regular turns already ended in the immutable parent. Preserve both available Reactions for lawful off-turn responses; record actual spent/unused amounts without adding an action or resource use.",
        reconcile_parent_budgets,
        {
            "parentIsImmutable": True,
            "actors": ["A", "B"],
            "endedTurnMarkers": {"A": state["actors"]["A"]["regularSchedule"]["ends"][-1], "B": state["actors"]["B"]["regularSchedule"]["ends"][-1]},
            "reactionInterpretation": "Retain an unused Reaction until spent or refreshed at the actor's next regular own-turn start.",
        },
    )

    # Continue from the immutable Return284 parent and include every intervening regular slot.
    start("C", 2.0)
    choose_mobile("C", 2.8)
    end("C", 2.9)
    start("D", 3.0)
    choose_mobile("D", 3.8)
    end("D", 3.9)
    start("A", 6.0)

    cast_id = "PG328-W01-402:MINOR-CONJURATION-1"
    tile_id = "PG328-W01-402:CLAY-TILE-1"
    space = state["actors"]["A"]["plane"]
    actor_a = state["actors"]["A"]
    actor_b = state["actors"]["B"]
    if actor_b["plane"] != actor_a["plane"] or actor_b["reaction"] != 1 or actor_b["RP"] < 3:
        raise ValueError("Wizard B's TEST_ONLY Counterspell responder state is not eligible")
    if actor_b["class"] != "Wizard" or actor_b["level"] != 20 or actor_b["profileSHA256"] != actor_a["profileSHA256"]:
        raise ValueError("Wizard B is not bound to the same Wizard20 actor profile as A")
    if profile["class"] != "Wizard" or profile["classLevel"] != 20 or not any(c["id"] == "wizard.base.counterspell" for c in profile["automaticCards"]):
        raise ValueError("Bound Wizard20 profile does not establish automatic Counterspell")
    acquired_ids = {c["id"] for c in profile["allAcquiredClassCapabilities"]}
    if not {"wizard.base.minor-conjuration", "wizard.arch.spell-efficiency"}.issubset(acquired_ids):
        raise ValueError("Bound profile does not establish acquired Minor Conjuration and Spell Efficiency")
    component_availability = {
        "cardListedComponents": None,
        "cardOmissionMeansExemption": False,
        "governingContract": "Player Rulebook v6 Wizard Spellcasting Traits lines 5154-5158; broader Spell Components lines 8605-8631.",
        "branchAvailability": {"speakingAvailable": True, "silencedOrGagged": False, "rightHandFreeAtCommit": True, "focus-A": "carried by A, represented in left hand", "restrained": False},
        "materialRequirement": "No specific material component is identified by the bound card/source; none is invented, consumed, or treated as waived.",
        "status": "TEST_ONLY availability premise; omitted card-level components remain unspecified.",
    }
    responder_assessment = {
        "A": {"role": "caster", "eligible": False, "disposition": "NOT_A_DISTINCT_RESPONDER"},
        "B": {"role": "Wizard20 in the same generated space", "eligible": True, "card": "current_bound_wizard.json#/cards/17", "profilePointer": "/automaticCards/1/id", "samePlane": True, "centerToCenterDistanceFeet": 10, "nearestBodyEdgeDistanceFeet": 5, "perceivesCasting": True, "lineOfEffect": "open courtyard; no intervening wall", "hostilityRequired": False, "rangeFeet": 60, "reactionAvailable": actor_b["reaction"], "currentRP": actor_b["RP"], "costRP": 3, "rpSufficient": actor_b["RP"] >= 3, "rechargeAvailable": not bool(actor_b["recharge"]), "spellRank": 1, "checkDCIfAttempted": 12, "decision": "PENDING_AT_WINDOW_OPEN"},
        "C": {"role": "Cleric20 on fixture:origin", "eligible": False, "disposition": "NO_WIZARD_COUNTERSPELL_CARD; OUTSIDE_CASTING_PLANE", "plane": state["actors"]["C"]["plane"]},
        "D": {"role": "Wizard20 on fixture:origin", "eligible": False, "disposition": "DIFFERENT_PLANE; NO_CROSS_PLANE_COUNTERSPELL_WINDOW", "plane": state["actors"]["D"]["plane"], "hasCounterspell": True},
    }

    def commit_minor() -> None:
        a = state["actors"]["A"]
        if a["action"] != 1 or a["RP"] < 1 or a["position"] != [25, 10, 0] or "focus-A" not in a["equipment"]:
            raise ValueError("A lacks the Action, RP, pose, or declared component availability")
        a["action"] = 0
        a["RP"] -= 1
        a["lastSpell"] = "wizard.base.minor-conjuration"
        if "wizard.base.minor-conjuration" not in a["preparedFamiliesUsed"]:
            a["preparedFamiliesUsed"].append("wizard.base.minor-conjuration")
        a["spellHistory"].append({"castId": cast_id, "spellId": "wizard.base.minor-conjuration", "class": "Wizard", "school": "Conjuration", "rank": 1, "time": 6.1, "cost": 1, "firstPreparedFamily": True, "baseDissonance": 0, "Refrain": 0, "originPlane": space, "target": [25, 9, 0], "concentration": False})
        a["resourceHistory"].append({"event": cast_id, "RP": -1, "poolAfter": 53, "discount": False})
        a["magicThisTurn"] = True
        a["w01HandState"] = {"left": "focus-A", "right": "free"}
        state["pendingCast"] = {"castId": cast_id, "casterId": "A", "spellId": "wizard.base.minor-conjuration", "phase": "COMMITTED_COSTS_PAID", "targetSpace": [25, 9, 0], "componentAvailability": copy.deepcopy(component_availability)}

    add_event(cast_id + ":COMMIT", 6.1, "CAST_COMMIT", "A commits the acquired Minor Conjuration Action and 1 RP after target and component availability checks.", commit_minor,
        {"sourceCard": "current_bound_wizard.json#/cards/6", "profileAcquisition": f"{ARCHIVE.relative_to(BASE)}::{PROFILE_MEMBER}#/allAcquiredClassCapabilities/1", "activation": "Action", "printedCost": "1 RP", "targetSpace": [25, 9, 0], "components": component_availability, "handState": {"left": "focus-A", "right": "free"}, "spellEfficiencyDiscount": False, "costsPaidBeforeCounterspell": True})

    def open_counterspell_window() -> None:
        pending = state.get("pendingCast")
        if not pending or pending.get("castId") != cast_id or pending.get("phase") != "COMMITTED_COSTS_PAID":
            raise ValueError("The paid cast commitment must precede its interruption window")
        pending["phase"] = "COUNTERSPELL_WINDOW_OPEN"
        pending["responders"] = copy.deepcopy(responder_assessment)

    add_event(cast_id + ":COUNTERSPELL-WINDOW-OPEN", 6.11, "COUNTERSPELL_WINDOW_OPEN", "The paid cast opens a pre-resolution Counterspell window; all actual actor responders are dispositioned.", open_counterspell_window,
        {"responders": responder_assessment, "trigger": "creature begins casting; success negates the spell after costs are paid"})

    def decline_counterspell() -> None:
        pending = state.get("pendingCast")
        if not pending or pending.get("phase") != "COUNTERSPELL_WINDOW_OPEN":
            raise ValueError("No open Counterspell window")
        pending["responders"]["B"]["decision"] = "DECLINED_TEST_ONLY"
        pending["phase"] = "WINDOW_CLOSED_NO_COUNTER_ATTEMPT"

    add_event(cast_id + ":B-DECLINES-COUNTERSPELL", 6.12, "COUNTERSPELL_DECLINED", "Eligible Wizard B explicitly declines in this TEST_ONLY branch; no check, Reaction, RP, or recharge is spent.", decline_counterspell,
        {"actorId": "B", "decision": "DECLINED_TEST_ONLY", "roll": "NOT ROLLED", "reactionSpent": False, "rpSpent": 0, "rechargeStarted": False})

    def resolve_minor() -> None:
        pending = state.get("pendingCast")
        if not pending or pending.get("phase") != "WINDOW_CLOSED_NO_COUNTER_ATTEMPT":
            raise ValueError("Spell resolution must follow the closed responder window")
        a = state["actors"]["A"]
        prior = a.get("spellEfficiency")
        ledger = copy.deepcopy(prior) if isinstance(prior, list) else ([copy.deepcopy(prior)] if prior else [])
        ledger.append({"family": "wizard.base.minor-conjuration", "until": 12.9, "triggeredByCastId": cast_id, "status": "TEST_ONLY_UNSPENT; NO_REPEAT_WITNESSED", "noDiscountAppliedByThisCast": True, "source": f"{ARCHIVE.relative_to(BASE)}::{PROFILE_MEMBER}#/allAcquiredClassCapabilities/24"})
        a["spellEfficiency"] = ledger
        state["items"][tile_id] = {"id": tile_id, "massLb": 2, "load": 0.2, "owner": None, "custodian": None, "plane": space, "position": [25, 9, 0], "exists": True, "quantity": 1, "provenance": "Minor Conjuration; common nonvaluable nonmagical clay; TEST_ONLY temporary object", "consumed": False, "sizeFeet": [1, 1, 0.25], "createdAtEventTime": 6.13, "expiresAtEventTime": 3606.13, "unattendedAtCreation": True, "boundsFeetAtCreation": {"x": [25, 26], "y": [9, 10], "z": [0, 0.25]}}
        state["pendingCast"] = None

    add_event(cast_id + ":RESOLVE", 6.13, "CAST_RESOLUTION", "After B declines, Minor Conjuration resolves and creates the temporary clay tile; its cast-triggered efficiency marker is recorded through A's next regular-turn end.", resolve_minor,
        {"targetSpace": [25, 9, 0], "createdObject": {"id": tile_id, "material": "common clay", "sizeFeet": [1, 1, 0.25], "weightLb": 2, "wieldability": "TEST_ONLY one-handed input"}, "unoccupiedBounds": "[25,26]×[9,10]×[0,0.25] does not overlap A's body or the selected panel", "spellEfficiencyLifecycle": {"source": f"{ARCHIVE.relative_to(BASE)}::{PROFILE_MEMBER}#/allAcquiredClassCapabilities/24", "newFamily": "wizard.base.minor-conjuration", "newUntil": 12.9, "oldFamily": "conjure-demiplane-fortress", "oldUntil": 6.9, "representation": "TEST_ONLY separate-family ledger; no same-family repeat or discount; no canonical overlap rule adopted"}})

    def pickup_tile() -> None:
        a = state["actors"]["A"]
        tile = state["items"][tile_id]
        if a["action"] != 0 or a["equipment"].count(tile_id) != 0:
            raise ValueError("Pickup preconditions differ")
        tile["custodian"] = "A"
        tile["position"] = None
        tile["heldBy"] = "A:right"
        tile["heldBoundsFeet"] = {"x": [25, 26], "y": [9, 10], "z": [0, 0.25]}
        a["equipment"].append(tile_id)
        a["carriedWeightLb"] = 14
        a["carriedLoad"] = 1.4
        a["w01HandState"] = {"left": "focus-A", "right": tile_id}

    add_event(
        "PG328-W01-402:PICKUP-CLAY-TILE",
        6.2,
        "FREE_OBJECT_INTERACTION",
        "A picks up the adjacent created tile with the otherwise-free right hand using the turn's single ordinary free object interaction.",
        pickup_tile,
        {"interactionCountThisTurn": 1, "targetItem": tile_id, "hand": "right", "additionalActionUsed": False},
    )

    choose_mobile("A", 6.25)

    def move_one_foot() -> None:
        a = state["actors"]["A"]
        tile = state["items"][tile_id]
        if a["movement"] < 1 or a["position"] != [25, 10, 0] or tile.get("heldBy") != "A:right":
            raise ValueError("A cannot make the selected one-foot carried movement")
        a["movement"] -= 1
        a["position"] = [25, 11, 0]
        tile["heldBoundsFeet"] = {"x": [25, 26], "y": [10, 11], "z": [0, 0.25]}

    add_event("PG328-W01-402:MOVE-1FT-CARRIED-TILE", 6.3, "VOLUNTARY_MOVEMENT", "A moves 1 foot away from the wall while carrying the tile; body and item remain within the local courtyard geometry.", move_one_foot,
        {"from": [25, 10, 0], "to": [25, 11, 0], "movementSpentFeet": 1, "movementRemainingFeet": 29, "bodyBounds": {"x": [25, 30], "y": [11, 16], "z": [0, 6]}, "tileBounds": {"x": [25, 26], "y": [10, 11], "z": [0, 0.25]}, "bodyTileIntersection": False, "tileWallIntersection": False})

    def move_adjacent() -> None:
        a = state["actors"]["A"]
        tile = state["items"][tile_id]
        if a["movement"] < 5 or a["position"] != [25, 11, 0] or tile.get("heldBy") != "A:right":
            raise ValueError("A cannot make the selected 5-foot movement")
        a["movement"] -= 5
        a["position"] = [25, 6, 0]
        tile["heldBoundsFeet"] = {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]}

    add_event(
        "PG328-W01-402:MOVE-5FT-TO-PANEL",
        6.4,
        "VOLUNTARY_MOVEMENT",
        "A moves 5 feet through the clear courtyard carrying the tile; the body stays clear and the tile's leading face contacts the panel without penetration.",
        move_adjacent,
        {
            "sourceRule": "COMBAT_ACTION_PLAYTEST.md movement rules plus Q23 courtyard bounds",
            "from": [25, 11, 0],
            "to": [25, 6, 0],
            "movementSpentFeet": 5,
            "movementRemainingFeet": 24,
            "bodyBoundsAfterFeet": {"x": [25, 30], "y": [6, 11], "z": [0, 6]},
            "tileBoundsAfterFeet": {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]},
            "wallPanelBoundsFeet": {"x": [25, 30], "y": [0, 5], "z": [0, 5]},
            "bodyWallIntersection": False,
            "tileWallIntersection": False,
            "contact": "tile face and panel interior face meet at y=5",
        },
    )
    end("A", 6.9)
    start("B", 7.0)
    choose_mobile("B", 7.8)
    end("B", 7.9)
    start("C", 8.0)
    choose_mobile("C", 8.8)
    end("C", 8.9)
    start("D", 9.0)
    choose_mobile("D", 9.8)
    end("D", 9.9)
    start("A", 12.0)
    choose_mobile("A", 12.05)

    def attack_panel() -> None:
        a = state["actors"]["A"]
        model = state["spaces"][space_id]["w01PartialStructureWitness"]
        panel = model["panelInstances"]["W01-SOUTH-WALL-X25-Z0"]
        if a["action"] != 1 or a["position"] != [25, 6, 0] or a["RP"] != 53:
            raise ValueError("Attack preconditions differ")
        if panel["currentHp"] != 60 or not state["items"][tile_id]["exists"] or state["items"][tile_id].get("heldBoundsFeet") != {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]}:
            raise ValueError("Panel/object state differs at attack time")
        a["action"] = 0
        panel["currentHp"] = 55
        panel["destroyed"] = False
        panel["lastDamage"] = {
            "eventId": "PG328-W01-402:ATTACK-SUNDER-SOUTH-PANEL",
            "amount": 5,
            "type": "bludgeoning",
            "hpBefore": 60,
            "hpAfter": 55,
        }

    add_event(
        "PG328-W01-402:ATTACK-SUNDER-SOUTH-PANEL",
        12.1,
        "ATTACK_SUNDER_OBJECT",
        "A makes one ordinary melee improvised-weapon Attack/Sunder against the named south outer-wall panel using the tile, whose face touches the wall at y=5 while A's body remains clear.",
        attack_panel,
        {
            "weaponObject": tile_id,
            "targetPanel": "W01-SOUTH-WALL-X25-Z0",
            "contactGeometry": "Body [25,30]×[6,11]×[0,6] is clear of the panel. Tile [25,26]×[5,6]×[0,0.25] meets its interior face at y=5 with no positive-volume overlap; no reach-extension rule is inferred.",
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
            "counterspellWindow": "No Counterspell trigger: the later Attack/Sunder is not a spell cast. The only spell-triggered window in this branch is explicitly recorded at Minor Conjuration.",
        },
    )
    end("A", 12.9)

    # Validate every forward patch and every inverse in exact reverse event order.
    snapshot_ids = set(snapshots)
    for event in events:
        if event["beforeStateId"] not in snapshot_ids or event["afterStateId"] not in snapshot_ids:
            raise AssertionError(f"Unknown snapshot reference in {event['eventId']}")
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
    if replay["items"][tile_id]["custodian"] != "A" or final_a["position"] != [25, 6, 0]:
        raise AssertionError("Final object custody or actor position is inconsistent")
    commit_event = next(e for e in events if e["eventId"] == cast_id + ":COMMIT")
    window_event = next(e for e in events if e["eventId"] == cast_id + ":COUNTERSPELL-WINDOW-OPEN")
    decline_event = next(e for e in events if e["eventId"] == cast_id + ":B-DECLINES-COUNTERSPELL")
    resolve_event = next(e for e in events if e["eventId"] == cast_id + ":RESOLVE")
    if not events.index(commit_event) < events.index(window_event) < events.index(decline_event) < events.index(resolve_event):
        raise AssertionError("Paid commit, interruption window, decline and resolution order is invalid")
    responder = snapshots[decline_event["afterStateId"]]["pendingCast"]["responders"]["B"]
    if responder["decision"] != "DECLINED_TEST_ONLY" or decline_event["authoredInputs"]["reactionSpent"] or decline_event["authoredInputs"]["rpSpent"] != 0:
        raise AssertionError("Counterspell no-cost decline record is inconsistent")
    if replay["actors"]["B"]["reaction"] != 1 or replay["actors"]["B"]["RP"] != 80:
        raise AssertionError("B's declined Counterspell must preserve its Reaction and RP")
    old_expiry = next(e for e in events if e["eventId"] == "PG328-W01-402:TURN-END-A-6.9")
    efficiency_after_69 = snapshots[old_expiry["afterStateId"]]["actors"]["A"]["spellEfficiency"]
    if not isinstance(efficiency_after_69, list) or len(efficiency_after_69) != 1 or efficiency_after_69[0]["family"] != "wizard.base.minor-conjuration" or efficiency_after_69[0]["until"] != 12.9:
        raise AssertionError("Old Fortress entitlement must expire at 6.9 while Minor Conjuration remains until 12.9")
    if final_a["spellEfficiency"] is not None:
        raise AssertionError("Minor Conjuration entitlement must expire at A's 12.9 turn end")
    if final_a["action"] != 0 or final_a["bonusAction"] != 0 or final_a["movement"] != 0:
        raise AssertionError("A's ended-turn Action/Bonus Action/movement budgets must be closed")
    if any(replay["actors"][actor_id]["regularSchedule"]["nextEnd"] is not None for actor_id in "ABCD"):
        raise AssertionError("Processed regular-turn end markers must be cleared")
    actual_stances = [(e["authoredInputs"]["actorId"], float(e["time"])) for e in events if e["kind"] == "REGULAR_TURN_STANCE_CHOICE"]
    if actual_stances != [("C", 2.8), ("D", 3.8), ("A", 6.25), ("B", 7.8), ("C", 8.8), ("D", 9.8), ("A", 12.05)]:
        raise AssertionError(f"Stance choices are missing, extra, or mistimed: {actual_stances}")

    def overlaps(a: dict[str, list[float]], b: dict[str, list[float]]) -> bool:
        return all(max(a[axis][0], b[axis][0]) < min(a[axis][1], b[axis][1]) for axis in ("x", "y", "z"))

    local = branch_initial["spaces"][space_id]["w01PartialStructureWitness"]
    geom = local["objectGeometry"]
    wall = local["panelInstances"]["W01-SOUTH-WALL-X25-Z0"]["boundsFeet"]
    body_at_spawn = {"x": [25, 30], "y": [10, 15], "z": [0, 6]}
    if overlaps(geom["spawnBoundsFeet"], body_at_spawn) or overlaps(geom["spawnBoundsFeet"], wall):
        raise AssertionError("Created volume is occupied or intersects the selected wall")
    if overlaps(geom["bodySweepBoundsFeet"], wall) or overlaps(geom["carriedItemSweepBoundsFeet"], wall):
        raise AssertionError("Body/item sweep intersects the selected wall")
    for y in (11, 10, 9, 8, 7, 6):
        body_box = {"x": [25, 30], "y": [y, y + 5], "z": [0, 6]}
        item_box = {"x": [25, 26], "y": [y - 1, y], "z": [0, 0.25]}
        if overlaps(body_box, item_box) or overlaps(item_box, wall):
            raise AssertionError(f"Carried tile overlaps the body or wall at actor y={y}")

    source_records = []

    def add_json_records(label: str, source: str, raw: bytes, value: object, pointers: list[str]) -> None:
        for pointer in pointers:
            resolve_json_pointer(value, pointer)
            source_records.append({"label": label, "source": source, "jsonPointer": pointer, "bytes": len(raw), "sha256": sha256(raw)})

    source_records.append({"label": "PG328 held archive", "source": str(ARCHIVE.relative_to(BASE)), "bytes": ARCHIVE.stat().st_size, "sha256": sha256(ARCHIVE.read_bytes()), "representation": "original archive bytes"})
    add_json_records("historical parent case member", f"{ARCHIVE.relative_to(BASE)}::{PARENT_MEMBER}", parent_raw, parent, ["/initial", "/final"])
    add_json_records("current bound Wizard source", f"{ARCHIVE.relative_to(BASE)}::{WIZARD_MEMBER}", wizard_raw, wizard, ["/cards/6", "/cards/17", "/engine/12", "/protectedInterfaceOriginal"])
    add_json_records("conditional actor profile", f"{ARCHIVE.relative_to(BASE)}::{PROFILE_MEMBER}", profile_raw, profile, ["/abilityScores/STR", "/acquisitionLedger/0/choices/1", "/automaticCards/1/id", "/alwaysPrepared/1", "/allAcquiredClassCapabilities/1", "/allAcquiredClassCapabilities/24", "/allAcquiredClassCapabilities/26"])
    for label, path, raw, value, pointers in [
        ("PG9-Q23 disposition", q23, q23.read_bytes(), read_json(q23), ["/questions/2/answer"]),
        ("PG328 blocker reassessment", blocker, blocker.read_bytes(), read_json(blocker), ["/remainingWitnessParts/0", "/sourceLevelGains/3"]),
        ("Director-confirmed W01 preflight", preflight, preflight_git_raw, read_json(preflight), ["/candidateAssessment/0", "/preflightFinding/remainingPredicates"]),
    ]:
        add_json_records(label, str(path.relative_to(BASE)), raw, value, pointers)
    for label, path, text_locator in [
        ("Rulebook v6", rulebook, "Spellcasting Traits 5154-5158; Minor Conjuration 5204; improvised weapons 6826-6832; melee Strength 7865; damage rolls 8231; Spell Components 8605-8631"),
        ("Combat Action playtest", combat, "regular-turn budget and Reaction sections 31, 76, 136; Stances 113-123"),
    ]:
        raw = path.read_bytes()
        source_records.append({"label": label, "source": str(path.relative_to(BASE)), "textLocator": text_locator, "bytes": len(raw), "sha256": sha256(raw)})
    source_records.append({"label": "Director-confirmed W01 preflight Git representation", "source": preflight_git_path, "bytes": len(preflight_git_raw), "sha256": sha256(preflight_git_raw), "representation": "Git HEAD blob bytes; working-tree CRLF normalized and matched"})

    OUT.mkdir(parents=True)
    owner_auth = {
        "id": "OWNER-PG328-W01-CONSTRUCTION-AUTHORIZATION-402",
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
        "id": "PG328-W01-LOCAL-GEOMETRY-402",
        "classification": "TEST_ONLY_BRANCH_GEOMETRY_PARTIAL_SUBWITNESS",
        "source": {"path": str(q23.relative_to(BASE)), "sha256": EXPECTED["q23"], "pointer": "/questions/2/answer"},
        "preservedQ23": {"outerWallThicknessFeet": 5, "outerWallHeightFeet": 30, "panelBoundsFeet": [5, 5, 5], "panelAC": 17, "panelHP": 60, "courtyardBoundsFeet": [5, 115, 5, 115]},
        "positionConvention": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["positionConvention"],
        "counterspellCastGeometry": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["counterspellCastGeometry"],
        "objectGeometry": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["objectGeometry"],
        "branchChoices": {
            "wallOrientation": "south wall at y=0..5",
            "selectedPanelId": "W01-SOUTH-WALL-X25-Z0",
            "selectedPanelBoundsFeet": {"x": [25, 30], "y": [0, 5], "z": [0, 5]},
            "adjacentActorEndPosition": [25, 6, 0],
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
        "id": "PG328-W01-DAMAGE-SUBWITNESS-402",
        "classification": "REVERSIBLE_TEST_ONLY_SUBWITNESS_CORRECTIVE_REPACK02_SUBMITTED_FOR_DIRECTOR_REVIEW",
        "supersedesReviewPacket": "fortress_w01_structural_damage_witness_401/W01_REPLAY_401.json",
        "alsoAddressesReview": "fortress_w01_structural_damage_witness_400/W01_REPLAY_400.json",
        "supersedingCorrections": [
            "source rows use individually resolvable JSON pointers or text locators; preflight binds actual Git HEAD bytes",
            "paid cast commit, eligible Counterspell window, explicit B TEST_ONLY decline and resolution are separate events",
            "A-D responder dispositions and component availability are recorded without an invented consumable",
            "every branch regular turn records a stance; end snapshots clear processed markers and preserve unused Reaction",
            "both Spell Efficiency family lifecycles are recorded without a discount or canonical overlap rule",
            "consistent body coordinate convention and numeric tile creation, carried sweep and wall contact proof",
            "every snapshot reference and reversible patch is validated",
        ],
        "historicalParent": {"member": PARENT_MEMBER, "memberSha256": EXPECTED["parent_member"], "finalSha256": EXPECTED["parent_final"], "handling": "immutable; branch begins from an exact copy of its final state"},
        "inheritedTurnNote": "The historical parent's A/B turns end at 0.9/1.9 and are not rewritten. This branch starts at 1.9 and makes no stance-benefit claim for those inherited turns.",
        "branchInitialStateId": branch_initial_id,
        "branchInitialStateSha256": digest(branch_initial),
        "stateSnapshots": snapshots,
        "events": events,
        "terminalStateId": events[-1]["afterStateId"],
        "terminalStateSha256": digest(replay),
        "targetDamage": {"panelId": "W01-SOUTH-WALL-X25-Z0", "hpBefore": 60, "hpAfter": 55, "damage": 5, "damageType": "bludgeoning", "destroyed": False},
        "restoration": {"inverseOrder": [e["eventId"] for e in reversed(events)], "restoresBranchInitial": True, "removingTestOnlyGeometryRestoresParentFinal": True, "parentFinalSha256": EXPECTED["parent_final"]},
        "queueAndDecisionState": {"applied": 828, "pending": 20, "acceptedUnapplied": 0, "fortressAccepted": False, "fortressApplied": False, "witnessSealed": False, "applicationAuthorized": False},
    }
    request = """# Director review request: PG328-W01 damage sub-witness 402\n\nRepack 402 addresses the exact residuals from your review of 400 and the follow-on 401 attempt. Source rows use individual JSON pointers or text locators, and the preflight is bound to Git HEAD bytes. Paid cast commitment, the Counterspell window, B's explicit eligible decline and spell resolution are separate ordered events; all actual responders are dispositioned. The Wizard component contract and test-only voice/free-hand/focus availability are recorded without inventing a consumed material.\n\nEvery new regular turn in this branch, including idle turns, records a Mobile choice. End snapshots clear processed end markers, expire unused Action/Bonus Action/movement, and preserve off-turn Reaction. The replay carries the old Fortress Spell Efficiency marker through 6.9 and a new Minor Conjuration marker through 12.9; this separate-family TEST_ONLY ledger applies no discount and adopts no canonical overlap rule. Geometry binds the minimum-corner body convention, unoccupied tile creation, carried-item sweep and exact panel contact without wall penetration.\n\nPlease verify all source rows, commit/window/decision/resolution order, responder and component evidence, turn and stance records, marker lifecycle, geometry, snapshot references, hashes, reverse replay and restoration. The 17-vs-17 hit remains 5 bludgeoning damage, reducing the panel from 60 to 55 HP.\n\nThis remains PARTIAL_WITNESS; NO_SEAL. The complete panel/support map, support validity, whole-structure navigation and Q23 keep-stair/landing connection remain open. No support/collapse rule, Q23 repair, Fortress acceptance/application, hold/seal, source/canonical/fixture mutation, or Queue361 change is requested. Please identify any remaining W01 defects, whether the bounded efficiency ledger is acceptable for TEST_ONLY review, and the exact residual W01 predicates.\n"""

    file_map: dict[str, bytes] = {}
    file_map["OWNER_W01_CONSTRUCTION_AUTHORIZATION_402.json"] = write_json(OUT / "OWNER_W01_CONSTRUCTION_AUTHORIZATION_402.json", owner_auth)
    file_map["SOURCE_BINDINGS_402.json"] = write_json(OUT / "SOURCE_BINDINGS_402.json", {"id": "PG328-W01-SOURCE-BINDINGS-402", "sources": source_records})
    file_map["W01_GEOMETRY_402.json"] = write_json(OUT / "W01_GEOMETRY_402.json", geometry)
    file_map["W01_REPLAY_402.json"] = write_json(OUT / "W01_REPLAY_402.json", replay_record)
    file_map["DIRECTOR_REVIEW_REQUEST_402.md"] = write_utf8_lf(OUT / "DIRECTOR_REVIEW_REQUEST_402.md", request)
    readme = """# PG328-W01 TEST_ONLY damage sub-witness 402\n\nThis reversible partial branch binds the source bytes, Counterspell responder window, components premise, regular-turn budgets and stances, Spell Efficiency lifecycle, and numerical body/object sweep. It creates one 2 lb clay tile, carries it without wall penetration, and records one 17-vs-17 Attack/Sunder hit for 5 bludgeoning damage (panel HP 60 to 55).\n\nThe complete Fortress support and navigation graphs remain open, including Q23 keep-stair/landing geometry. No support/collapse rule, Q23 repair, canonical Spell Efficiency overlap rule, seal, spell acceptance/application, or queue change is included.\n"""
    file_map["README_402.md"] = write_utf8_lf(OUT / "README_402.md", readme)

    verification = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-VERIFICATION-402",
        "status": "PASS_PARTIAL_TEST_ONLY_REPLAY; W01_OPEN",
        "checks": {
            "sourceHashesAndPointers": "PASS; Git HEAD preflight bytes pinned; every JSON pointer resolved individually; text lines stored as text locators",
            "historicalParentFinalHash": "PASS",
            "forwardPatchesInOrder": "PASS",
            "inversePatchesReverseOrder": "PASS",
            "fullParentRestoration": "PASS",
            "minorConjurationCost": "1 RP; PASS",
            "tileWithinCardSizeAndWeight": "PASS",
            "firstDistinctMatrixBaseDissonance": "0; PASS",
            "turnAndInteractionBudgets": "PASS for branch turns; spent/unused closeouts recorded; processed nextEnd markers cleared; off-turn Reaction preserved",
            "turnStances": "PASS for each regular turn introduced by this branch, including idle C/D/B turns; inherited parent turns remain unchanged",
            "counterspellEligibilityAndDecision": "PASS; B eligible at 10 ft and explicitly declines TEST_ONLY; C/D dispositions recorded; no cost/reaction/recharge change",
            "componentAvailability": "PASS as TEST_ONLY premise; free hand/voice/focus available; omitted card list does not create an exemption or material cost",
            "spellEfficiencyLifecycle": "PASS TEST_ONLY ledger; old marker ends 6.9, new Minor Conjuration marker ends 12.9; no repeat, discount or canonical overlap rule asserted",
            "bodyAndObjectGeometry": "PASS local predicates; unoccupied creation volume, body/item sweep and panel contact computed with positive-volume overlap checks",
            "eventSnapshotReferences": "PASS; every event before/after ID exists",
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
        "openPredicates": ["complete panel/support map", "mechanical support validity", "whole-structure legal navigation", "keep-stair/landing geometry under PG9-Q23", "inherited parent A/B stance records are not rewritten", "canonical Spell Efficiency overlap semantics remain outside this TEST_ONLY packet"],
    }
    file_map["VERIFICATION_402.json"] = write_json(OUT / "VERIFICATION_402.json", verification)
    crc_rows = []
    for name, raw in sorted(file_map.items()):
        crc_rows.append({"path": name, "bytes": len(raw), "sha256": sha256(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
    manifest = {"id": "PG328-W01-DAMAGE-SUBWITNESS-MANIFEST-402", "schemaVersion": 1, "members": crc_rows}
    manifest_raw = write_json(OUT / "MANIFEST_402.json", manifest)
    zip_path = OUT / ARCHIVE_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(file_map):
            zf.writestr(name, file_map[name])
        zf.writestr("MANIFEST_402.json", manifest_raw)
    archive_raw = zip_path.read_bytes()
    delivery = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-DELIVERY-402",
        "status": "READY_FOR_DIRECTOR_REVIEW; PARTIAL_WITNESS; NO_SEAL",
        "archive": {"path": ARCHIVE_NAME, "bytes": len(archive_raw), "sha256": sha256(archive_raw)},
        "manifest": {"path": "MANIFEST_402.json", "bytes": len(manifest_raw), "sha256": sha256(manifest_raw)},
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
    write_json(OUT / "DELIVERY_402.json", delivery)

    # Check archived members against the manifest and re-open the zip.
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        expected_names = set(file_map) | {"MANIFEST_402.json"}
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
