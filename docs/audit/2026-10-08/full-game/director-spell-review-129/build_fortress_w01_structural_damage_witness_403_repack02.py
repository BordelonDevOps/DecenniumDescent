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
OUT = BASE / "fortress_w01_structural_damage_witness_403_repack02"
ARCHIVE_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328W01_Witness403_Repack02_TESTONLY.zip"

EXPECTED = {
    "held_archive": "47af8e23be318210229f7fd2b360be809b2b7ed5d73b08abcbeaf7a078c3f1f4",
    "parent_member": "b18e7c3b7acc9867d6448a8a58d98f2d45eeea629144b1a696ef0d7c76844e54",
    "parent_final": "48c34a265c58f12cdb3d24ca6f59ddc53842476f090bfdded3796bd340b49e89",
    "wizard_member": "8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b",
    "profile_member": "a3a3ce0a714c1fa35523719c8c8a0297fc457d5b5f097f6a20a00aad6cd7be55",
    "rulebook": "bccb5121968843fd9ccf17587a9414ae03a1cf6458f2b8f2ad422091ca2d1c68",
    "rulebook_git_blob": "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b",
    "combat": "f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6",
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
    if "w01MobileAllowanceRemainingFeet" in actor:
        actor["w01MobileAllowanceRemainingFeet"] = 0
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

    rulebook = pathlib.Path("docs/reference/Player_Rulebook_v6_source_text.txt")
    combat = pathlib.Path("DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md")
    q23 = INTAKE / "payload" / "rules" / "PG328_QUESTION_DISPOSITIONS.json"
    blocker = INTAKE / "payload" / "authority" / "PG328_BLOCKER_REASSESSMENT.json"
    preflight = BASE / "fortress_w01_structural_damage_source_preflight_396" / "OWNER_PG328_W01_STRUCTURAL_DAMAGE_SOURCE_PREFLIGHT_396_TESTONLY.json"
    git_root = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=BASE, text=True).strip()).resolve()
    rulebook = git_root / rulebook
    combat = git_root / combat
    rulebook_git_path, rulebook_git_raw = git_head_bytes(rulebook, repo_root=git_root)
    combat_git_path, combat_git_raw = git_head_bytes(combat, repo_root=git_root)
    for label, path, raw in (("Rulebook v6", rulebook, rulebook_git_raw), ("Combat Action playtest", combat, combat_git_raw)):
        normalized_raw = raw.replace(b"\r\n", b"\n")
        expected_normalized = EXPECTED["rulebook" if label == "Rulebook v6" else "combat"]
        expected_blob = EXPECTED["rulebook_git_blob"] if label == "Rulebook v6" else expected_normalized
        if sha256(raw) != expected_blob or sha256(normalized_raw) != expected_normalized:
            raise ValueError(f"Pinned Git {label} raw/normalized bytes changed")
        if sha256(path.read_bytes().replace(b"\r\n", b"\n")) != sha256(normalized_raw):
            raise ValueError(f"Working-tree {label} cannot be normalized to the pinned Git source text")
    preflight_git_path, preflight_git_raw = git_head_bytes(preflight, repo_root=git_root)
    if sha256(preflight_git_raw) != EXPECTED["preflight_git_bytes"]:
        raise ValueError("Pinned Git preflight bytes changed")
    if sha256(preflight.read_bytes().replace(b"\r\n", b"\n")) != sha256(preflight_git_raw):
        raise ValueError("Working-tree preflight cannot be normalized to the pinned Git representation")
    source_paths = {
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
    # Branch-only geometry and hand-state premises make the otherwise unlocated
    # historical carried items auditable without changing the parent fixture.
    item_layout = {
        "focus-A": {"relativeBoundsFeet": {"x": [0, 0.5], "y": [0, 0.5], "z": [3, 3.5]}, "sizeFeet": [0.5, 0.5, 0.5]},
        "pack-A": {"relativeBoundsFeet": {"x": [0.5, 1], "y": [0, 0.5], "z": [3, 3.5]}, "sizeFeet": [0.5, 0.5, 0.5]},
        "cargo-A": {"relativeBoundsFeet": {"x": [1, 2], "y": [0, 1], "z": [3, 4]}, "sizeFeet": [1, 1, 1]},
    }
    actor_a_initial = branch_initial["actors"]["A"]
    actor_b_initial = branch_initial["actors"]["B"]
    for actor_id in "ABCD":
        branch_initial["actors"][actor_id]["w01MobileAllowanceRemainingFeet"] = 0
    if actor_b_initial.get("conditions"):
        raise ValueError("B's branch-only voice availability requires no silencing/gagging condition")
    if not {"focus-B", "pack-B"}.issubset(actor_b_initial.get("equipment", [])):
        raise ValueError("B's branch-only focus/hand mapping does not match the immutable parent")
    actor_b_initial["w01HandState"] = {"left": "focus-B", "right": "free", "classification": "TEST_ONLY_BRANCH_AVAILABILITY"}
    actor_b_initial["w01VoiceAvailable"] = True
    for item_id, layout in item_layout.items():
        item = branch_initial["items"].get(item_id)
        if item is None or item.get("custodian") != "A" or item.get("sizeFeet") != layout["sizeFeet"]:
            raise ValueError(f"Historical carried item differs from the bound parent: {item_id}")
        item["testOnlyGeometry"] = {
            "classification": "TEST_ONLY_BRANCH_OCCUPANCY_PREMISE",
            "actorId": "A",
            "relativeBoundsFeet": copy.deepcopy(layout["relativeBoundsFeet"]),
            "occupiedBoundsFeet": {
                axis: [actor_a_initial["position"][idx] + offset for offset in layout["relativeBoundsFeet"][axis]]
                for idx, axis in enumerate(("x", "y", "z"))
            },
            "containedInActorEnvelope": True,
            "containment": "inside actor A's validated [x,x+5]×[y,y+5]×[z,z+6] envelope; no source or fixture location inferred",
        }
    branch_initial["spaces"][space_id]["w01PartialStructureWitness"] = {
        "id": "PG328-W01-LOCAL-GEOMETRY-403",
        "classification": "TEST_ONLY_BRANCH_GEOMETRY; PARTIAL_SUBWITNESS",
        "wholeStructureMapComplete": False,
        "positionConvention": {"classification": "TEST_ONLY_LOCAL_CONVENTION; no canonical rule inferred", "actorPosition": "minimum x/y corner at foot; z is floor height", "bodyBounds": "[x,x+5]×[y,y+5]×[z,z+6]", "sameConventionForAAndB": True, "intersection": "positive-volume overlap; shared boundary is contact"},
        "counterspellCastGeometry": {"A": {"position": [25, 10, 0], "center": [27.5, 12.5, 3]}, "B": {"position": [15, 10, 0], "center": [17.5, 12.5, 3]}, "centerDistanceFeet": 10, "nearestBodyGapFeet": 5, "samePlane": True, "segment": "open courtyard; no intervening structure"},
        "objectGeometry": {"spawnBoundsFeet": {"x": [25, 26], "y": [9, 10], "z": [0, 0.25]}, "bodyAtCreation": {"x": [25, 30], "y": [10, 15], "z": [0, 6]}, "heldOffset": {"x": [0, 1], "y": [-1, 0], "z": [0, 0.25]}, "bodySweepBoundsFeet": {"x": [25, 30], "y": [6, 16], "z": [0, 6]}, "carriedItemSweepBoundsFeet": {"x": [25, 26], "y": [5, 11], "z": [0, 0.25]}, "terminalBodyBoundsFeet": {"x": [25, 30], "y": [6, 11], "z": [0, 6]}, "terminalTileBoundsFeet": {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]}, "preexistingCarriedItems": {item_id: copy.deepcopy(branch_initial["items"][item_id]["testOnlyGeometry"]) for item_id in item_layout}, "wallContactPlane": 5},
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
        add_event(f"PG328-W01-403:TURN-START-{actor_id}-{when:g}", when, "REGULAR_TURN_START", f"{actor_id} regular turn starts; no unrecorded resource refresh is assumed.", action)

    def end(actor_id: str, when: float) -> None:
        def action() -> None:
            turn_end(state, actor_id, when)
        add_event(
            f"PG328-W01-403:TURN-END-{actor_id}-{when:g}",
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
            if "w01MobileAllowanceRemainingFeet" in state["actors"][actor_id]:
                state["actors"][actor_id]["w01MobileAllowanceRemainingFeet"] = 5

        add_event(
            f"PG328-W01-403:STANCE-MOBILE-{actor_id}-{when:g}", when, "REGULAR_TURN_STANCE_CHOICE",
            f"{actor_id} selects Mobile before a stance-relevant event or, on an idle turn, before turn end; it expires at the next regular own-turn start.", action,
            {"actorId": actor_id, "stance": "Mobile", "selectedAt": when, "expiresAtNextRegularStart": expires_at,
             "source": "COMBAT_ACTION_PLAYTEST.md § Stances, lines 113-123",
             "benefit": "first 5 feet of actual voluntary movement does not provoke; no free movement; opportunity attacks reduce only that actor's base weapon die; none occur in this branch",
             "mobileAllowanceRemainingFeetAfterChoice": 5},
        )

    def carried_bounds_at(position: list[float]) -> dict[str, dict[str, list[float]]]:
        return {
            item_id: {
                axis: [position[idx] + offset for offset in item_layout[item_id]["relativeBoundsFeet"][axis]]
                for idx, axis in enumerate(("x", "y", "z"))
            }
            for item_id in item_layout
        }

    def update_carried_item_geometry(actor: dict[str, object]) -> None:
        for item_id, bounds in carried_bounds_at(actor["position"]).items():
            item = state["items"][item_id]
            item["testOnlyGeometry"]["occupiedBoundsFeet"] = bounds
            item["testOnlyGeometry"]["containedInActorEnvelope"] = True

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
        "PG328-W01-403:CLOSE-PARENT-TURN-BUDGETS-A-B",
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
    choose_mobile("A", 6.05)

    cast_id = "PG328-W01-403:MINOR-CONJURATION-1"
    tile_id = "PG328-W01-403:CLAY-TILE-1"
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
    responder_component_availability = {
        "classification": "TEST_ONLY_BRANCH_AVAILABILITY; no new component rule inferred",
        "actorId": "B",
        "card": "current_bound_wizard.json#/cards/17",
        "hands": {"left": "focus-B held/readily accessible", "right": "free"},
        "focusItemId": "focus-B",
        "focusInEquipmentAndCustody": "B carries focus-B in the immutable parent; its physical hand placement is this branch-only availability premise",
        "speakingAvailable": True,
        "silencedOrGagged": False,
        "restrained": False,
        "cardListedComponents": None,
        "materialRequirement": "Omitted card-level component list remains unspecified; no material component is invented or consumed.",
    }
    responder_assessment = {
        "A": {"role": "caster", "eligible": "UNADJUDICATED", "disposition": "NO_ATTEMPT_TEST_ONLY", "decision": "CASTER_EXPLICITLY_MAKES_NO_COUNTERSPELL_ATTEMPT_IN_THIS_BRANCH", "reason": "This branch does not adjudicate whether the caster can counter its own casting; no attempt is made.", "reactionSpent": False, "rpSpent": 0, "rechargeStarted": False},
        "B": {"role": "Wizard20 in the same generated space", "eligible": True, "card": "current_bound_wizard.json#/cards/17", "profilePointer": "/automaticCards/1/id", "componentAvailability": copy.deepcopy(responder_component_availability), "samePlane": True, "centerToCenterDistanceFeet": 10, "nearestBodyEdgeDistanceFeet": 5, "perceivesCasting": True, "lineOfEffect": "open courtyard; no intervening wall", "hostilityRequired": False, "rangeFeet": 60, "reactionAvailable": actor_b["reaction"], "currentRP": actor_b["RP"], "costRP": 3, "rpSufficient": actor_b["RP"] >= 3, "rechargeAvailable": not bool(actor_b["recharge"]), "spellRank": 1, "checkDCIfAttempted": 12, "decision": "PENDING_AT_WINDOW_OPEN"},
        "C": {"role": "Cleric20 on fixture:origin", "eligible": False, "disposition": "NO_WIZARD_COUNTERSPELL_CARD; OUTSIDE_CASTING_PLANE", "plane": state["actors"]["C"]["plane"]},
        "D": {"role": "Wizard20 on fixture:origin", "eligible": False, "disposition": "DIFFERENT_PLANE; NO_CROSS_PLANE_COUNTERSPELL_WINDOW", "plane": state["actors"]["D"]["plane"], "hasCounterspell": True},
    }

    def commit_minor() -> None:
        a = state["actors"]["A"]
        if a["action"] != 1 or a["RP"] < 1 or a["position"] != [25, 10, 0] or "focus-A" not in a["equipment"] or a.get("stance") != "Mobile":
            raise ValueError(f"A lacks the Action, RP, pose, prior stance, or declared component availability: action={a['action']} RP={a['RP']} position={a['position']} focus={'focus-A' in a['equipment']} stance={a.get('stance')}")
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

    add_event(cast_id + ":COUNTERSPELL-WINDOW-OPEN", 6.11, "COUNTERSPELL_WINDOW_OPEN", "The paid cast opens a pre-resolution Counterspell window; B is eligible and A is recorded as making no attempt without adjudicating self-counterspell eligibility.", open_counterspell_window,
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
        "PG328-W01-403:PICKUP-CLAY-TILE",
        6.2,
        "FREE_OBJECT_INTERACTION",
        "A picks up the adjacent created tile with the otherwise-free right hand using the turn's single ordinary free object interaction.",
        pickup_tile,
        {"interactionCountThisTurn": 1, "targetItem": tile_id, "hand": "right", "additionalActionUsed": False},
    )

    def move_one_foot() -> None:
        a = state["actors"]["A"]
        tile = state["items"][tile_id]
        if a["movement"] < 1 or a["position"] != [25, 10, 0] or tile.get("heldBy") != "A:right" or a.get("w01MobileAllowanceRemainingFeet") != 5:
            raise ValueError("A cannot make the selected one-foot carried movement")
        a["movement"] -= 1
        a["w01MobileAllowanceRemainingFeet"] -= 1
        a["position"] = [25, 11, 0]
        tile["heldBoundsFeet"] = {"x": [25, 26], "y": [10, 11], "z": [0, 0.25]}
        update_carried_item_geometry(a)

    add_event("PG328-W01-403:MOVE-1FT-CARRIED-TILE", 6.3, "VOLUNTARY_MOVEMENT", "A moves 1 foot away from the wall while carrying the tile; body and item remain within the local courtyard geometry.", move_one_foot,
        {"from": [25, 10, 0], "to": [25, 11, 0], "movementSpentFeet": 1, "movementRemainingFeet": 29, "mobileAllowanceBeforeFeet": 5, "mobileProtectionAppliedFeet": 1, "mobileAllowanceAfterFeet": 4, "bodyBounds": {"x": [25, 30], "y": [11, 16], "z": [0, 6]}, "tileBounds": {"x": [25, 26], "y": [10, 11], "z": [0, 0.25]}, "preexistingCarriedItemBoundsAfter": carried_bounds_at([25, 11, 0]), "bodyTileIntersection": False, "tileWallIntersection": False})

    def move_adjacent() -> None:
        a = state["actors"]["A"]
        tile = state["items"][tile_id]
        if a["movement"] < 5 or a["position"] != [25, 11, 0] or tile.get("heldBy") != "A:right" or a.get("w01MobileAllowanceRemainingFeet") != 4:
            raise ValueError("A cannot make the selected 5-foot movement")
        a["movement"] -= 5
        a["w01MobileAllowanceRemainingFeet"] = max(0, a["w01MobileAllowanceRemainingFeet"] - 5)
        a["position"] = [25, 6, 0]
        tile["heldBoundsFeet"] = {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]}
        update_carried_item_geometry(a)

    add_event(
        "PG328-W01-403:MOVE-5FT-TO-PANEL",
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
            "mobileAllowanceBeforeFeet": 4,
            "mobileProtectionAppliedFeet": 4,
            "unprotectedVoluntaryMovementFeet": 1,
            "mobileAllowanceAfterFeet": 0,
            "bodyBoundsAfterFeet": {"x": [25, 30], "y": [6, 11], "z": [0, 6]},
            "tileBoundsAfterFeet": {"x": [25, 26], "y": [5, 6], "z": [0, 0.25]},
            "preexistingCarriedItemBoundsAfter": carried_bounds_at([25, 6, 0]),
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
            "eventId": "PG328-W01-403:ATTACK-SUNDER-SOUTH-PANEL",
            "amount": 5,
            "type": "bludgeoning",
            "hpBefore": 60,
            "hpAfter": 55,
        }

    add_event(
        "PG328-W01-403:ATTACK-SUNDER-SOUTH-PANEL",
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
    for actor_id in "ABCD":
        restored_parent["actors"][actor_id].pop("w01MobileAllowanceRemainingFeet", None)
    restored_parent["actors"]["B"].pop("w01HandState", None)
    restored_parent["actors"]["B"].pop("w01VoiceAvailable", None)
    for item_id in item_layout:
        restored_parent["items"][item_id].pop("testOnlyGeometry", None)
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
    open_snapshot = snapshots[window_event["afterStateId"]]["pendingCast"]["responders"]
    decline_snapshot = snapshots[decline_event["afterStateId"]]["pendingCast"]["responders"]
    if open_snapshot["A"]["eligible"] != "UNADJUDICATED" or open_snapshot["A"]["disposition"] != "NO_ATTEMPT_TEST_ONLY" or open_snapshot["A"]["rpSpent"] != 0:
        raise AssertionError("Caster A must be a TEST_ONLY no-attempt with unadjudicated eligibility and no cost")
    if open_snapshot["B"]["componentAvailability"]["hands"] != {"left": "focus-B held/readily accessible", "right": "free"}:
        raise AssertionError("B's actual branch-only hand/focus mapping is missing at window open")
    if decline_snapshot["B"]["decision"] != "DECLINED_TEST_ONLY" or decline_snapshot["A"] != open_snapshot["A"]:
        raise AssertionError("Counterspell responder snapshots do not reconcile across B's decline")
    if replay["actors"]["B"]["reaction"] != 1 or replay["actors"]["B"]["RP"] != 80:
        raise AssertionError("B's declined Counterspell must preserve its Reaction and RP")
    old_expiry = next(e for e in events if e["eventId"] == "PG328-W01-403:TURN-END-A-6.9")
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
    if actual_stances != [("C", 2.8), ("D", 3.8), ("A", 6.05), ("B", 7.8), ("C", 8.8), ("D", 9.8), ("A", 12.05)]:
        raise AssertionError(f"Stance choices are missing, extra, or mistimed: {actual_stances}")
    movement_events = [e for e in events if e["kind"] == "VOLUNTARY_MOVEMENT"]
    if [(e["authoredInputs"]["mobileAllowanceBeforeFeet"], e["authoredInputs"]["mobileAllowanceAfterFeet"], e["authoredInputs"]["movementRemainingFeet"]) for e in movement_events] != [(5, 4, 29), (4, 0, 24)]:
        raise AssertionError("Mobile allowance must track 5→4→0 while movement tracks 30→29→24")
    a_start_12 = next(e for e in events if e["eventId"] == "PG328-W01-403:TURN-START-A-12")
    a_start_snapshot = snapshots[a_start_12["afterStateId"]]["actors"]["A"]
    a_mobile_1205 = next(e for e in events if e["eventId"] == "PG328-W01-403:STANCE-MOBILE-A-12.05")
    a_mobile_snapshot = snapshots[a_mobile_1205["afterStateId"]]["actors"]["A"]
    if a_start_snapshot["stance"] is not None or a_start_snapshot["w01MobileAllowanceRemainingFeet"] != 0 or a_mobile_snapshot["w01MobileAllowanceRemainingFeet"] != 5:
        raise AssertionError("A's prior stance/allowance must expire and reset at 12.0 before the 12.05 choice")

    def overlaps(a: dict[str, list[float]], b: dict[str, list[float]]) -> bool:
        return all(max(a[axis][0], b[axis][0]) < min(a[axis][1], b[axis][1]) for axis in ("x", "y", "z"))

    local = branch_initial["spaces"][space_id]["w01PartialStructureWitness"]
    geom = local["objectGeometry"]
    wall = local["panelInstances"]["W01-SOUTH-WALL-X25-Z0"]["boundsFeet"]
    body_at_spawn = {"x": [25, 30], "y": [10, 15], "z": [0, 6]}
    if overlaps(geom["spawnBoundsFeet"], body_at_spawn) or overlaps(geom["spawnBoundsFeet"], wall):
        raise AssertionError("Created volume is occupied or intersects the selected wall")
    for item_id, layout in item_layout.items():
        item = branch_initial["items"][item_id]
        item_geom = item.get("testOnlyGeometry", {})
        bounds = item_geom.get("occupiedBoundsFeet")
        if item_geom.get("classification") != "TEST_ONLY_BRANCH_OCCUPANCY_PREMISE" or not bounds or overlaps(bounds, geom["spawnBoundsFeet"]):
            raise AssertionError(f"Existing carried item lacks verified branch-only occupancy or overlaps creation volume: {item_id}")
        if not all(body_at_spawn[axis][0] <= bounds[axis][0] <= bounds[axis][1] <= body_at_spawn[axis][1] for axis in ("x", "y", "z")):
            raise AssertionError(f"Existing carried item is not contained in A's body envelope at creation: {item_id}")
        bounds_over_path = [carried_bounds_at(position)[item_id] for position in ([25, 10, 0], [25, 11, 0], [25, 6, 0])]
        sweep = {
            axis: [min(box[axis][0] for box in bounds_over_path), max(box[axis][1] for box in bounds_over_path)]
            for axis in ("x", "y", "z")
        }
        if overlaps(sweep, wall):
            raise AssertionError(f"Existing carried item sweep intersects the selected wall: {item_id}")
        for position, box in zip(([25, 10, 0], [25, 11, 0], [25, 6, 0]), bounds_over_path):
            body_box = {"x": [position[0], position[0] + 5], "y": [position[1], position[1] + 5], "z": [position[2], position[2] + 6]}
            if not all(body_box[axis][0] <= box[axis][0] <= box[axis][1] <= body_box[axis][1] for axis in ("x", "y", "z")):
                raise AssertionError(f"Existing carried item is outside A's body envelope at {position}: {item_id}")
            if overlaps(box, geom["spawnBoundsFeet"]):
                raise AssertionError(f"Existing carried item overlaps the created tile at {position}: {item_id}")
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
        git_path, raw = (rulebook_git_path, rulebook_git_raw) if label == "Rulebook v6" else (combat_git_path, combat_git_raw)
        normalized_raw = raw.replace(b"\r\n", b"\n")
        source_records.append({"label": label, "source": git_path, "textLocator": text_locator, "gitBlobBytes": len(raw), "gitBlobSha256": sha256(raw), "lfNormalizedBytes": len(normalized_raw), "lfNormalizedSha256": sha256(normalized_raw), "textLocatorRepresentation": "LF-normalized repository source text", "representation": "Exact Git HEAD blob bytes and deterministic CRLF-to-LF source-text normalization are both bound"})
    source_records.append({"label": "Director-confirmed W01 preflight Git representation", "source": preflight_git_path, "bytes": len(preflight_git_raw), "sha256": sha256(preflight_git_raw), "representation": "Git HEAD blob bytes; working-tree CRLF normalized and matched"})

    OUT.mkdir(parents=True)
    owner_auth = {
        "id": "OWNER-PG328-W01-CONSTRUCTION-AUTHORIZATION-403",
        "status": "OWNER_AUTHORIZED_TEST_ONLY_BRANCH_CONSTRUCTION",
        "scope": "REVERSIBLE_TEST_ONLY_PG328_W01_DAMAGE_SUBWITNESS",
        "ownerInstruction": "Correct the four packet defects identified in the Director's independent Witness402 review and submit the revised partial witness for review.",
        "directorAuthorization": "Resume the already-authorized TEST_ONLY PG328-W01 construction: lawful non-destructive damage event, reversible state history, and unaffected panel/support/navigation geometry. Construction does not establish witness sufficiency or seal.",
        "directorThread": "Review Time Stop Witness Evidence",
        "directorThreadId": "6ae5c784-afec-83e9-a2ca-5e2638b95750",
        "authorizedActs": ["source-bound reversible test-only construction", "Director review submission"],
        "notAuthorized": ["source repair", "mechanical support/collapse rule", "W01 seal", "Fortress acceptance/application", "canon or fixture mutation", "spell queue mutation"],
    }
    geometry = {
        "id": "PG328-W01-LOCAL-GEOMETRY-403",
        "classification": "TEST_ONLY_BRANCH_GEOMETRY_PARTIAL_SUBWITNESS",
        "source": {"path": str(q23.relative_to(BASE)), "sha256": EXPECTED["q23"], "pointer": "/questions/2/answer"},
        "preservedQ23": {"outerWallThicknessFeet": 5, "outerWallHeightFeet": 30, "panelBoundsFeet": [5, 5, 5], "panelAC": 17, "panelHP": 60, "courtyardBoundsFeet": [5, 115, 5, 115]},
        "positionConvention": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["positionConvention"],
        "counterspellCastGeometry": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["counterspellCastGeometry"],
        "objectGeometry": branch_initial["spaces"][space_id]["w01PartialStructureWitness"]["objectGeometry"],
        "preexistingCarriedItemGeometry": {
            "classification": "TEST_ONLY_BRANCH_OCCUPANCY_PREMISE; no historical item coordinates inferred",
            "actorBodyBoundsConvention": "[x,x+5]×[y,y+5]×[z,z+6]",
            "actorPositionsFeet": [[25, 10, 0], [25, 11, 0], [25, 6, 0]],
            "items": {
                item_id: {
                    "relativeBoundsFeet": copy.deepcopy(item_layout[item_id]["relativeBoundsFeet"]),
                    "boundsAtAStart": copy.deepcopy(branch_initial["items"][item_id]["testOnlyGeometry"]["occupiedBoundsFeet"]),
                    "boundsAfterOneFoot": carried_bounds_at([25, 11, 0])[item_id],
                    "boundsAtTerminal": carried_bounds_at([25, 6, 0])[item_id],
                    "sweepBoundsFeet": {
                        axis: [
                            min(bounds[axis][0] for bounds in (carried_bounds_at([25, 10, 0])[item_id], carried_bounds_at([25, 11, 0])[item_id], carried_bounds_at([25, 6, 0])[item_id])),
                            max(bounds[axis][1] for bounds in (carried_bounds_at([25, 10, 0])[item_id], carried_bounds_at([25, 11, 0])[item_id], carried_bounds_at([25, 6, 0])[item_id])),
                        ]
                        for axis in ("x", "y", "z")
                    },
                }
                for item_id in item_layout
            },
            "clearance": "All item bounds remain contained inside actor A's envelope at every represented position; no item overlaps the created tile or selected wall. Their full sweep is contained by the clear body sweep.",
        },
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
    expected_sweep_y = {"focus-A": [6, 11.5], "pack-A": [6, 11.5], "cargo-A": [6, 12]}
    for item_id, expected_y in expected_sweep_y.items():
        actual_y = geometry["preexistingCarriedItemGeometry"]["items"][item_id]["sweepBoundsFeet"]["y"]
        if actual_y != expected_y:
            raise AssertionError(f"Three-pose carried sweep is incorrect for {item_id}: {actual_y} != {expected_y}")

    replay_record = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-403",
        "classification": "REVERSIBLE_TEST_ONLY_SUBWITNESS_REPACK02_AFTER_DIRECTOR_R6_SWEEP_FIX_SUBMITTED_FOR_REVIEW",
        "supersedesReviewPacket": "fortress_w01_structural_damage_witness_403/W01_REPLAY_403.json",
        "alsoAddressesReview": "fortress_w01_structural_damage_witness_402/W01_REPLAY_402.json, 401 and earlier 400 findings",
        "supersedingCorrections": [
            "source rows use individually resolvable JSON pointers or text locators; rulebook/combat bind exact Git HEAD blob bytes",
            "paid cast commit, eligible Counterspell window, explicit B TEST_ONLY decline and resolution are separate events",
            "A is an explicit TEST_ONLY no-attempt with eligibility unadjudicated; B's branch-only left focus/right free and voice availability are mapped through pendingCast snapshots",
            "A selects Mobile before the cast; allowance tracks 5→4→0 against 30→29→24 movement and resets at A's 12.0 regular start",
            "both Spell Efficiency family lifecycles are recorded without a discount or canonical overlap rule",
            "consistent body coordinates, numeric tile geometry, and contained focus-A/pack-A/cargo-A bounds through every A movement",
            "focus-A/pack-A/cargo-A sweep summaries recomputed from all three recorded poses, including A's intermediate y=11 pose",
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
        "restoration": {"inverseOrder": [e["eventId"] for e in reversed(events)], "restoresBranchInitial": True, "removingDeclaredBranchExtensionsRestoresParentFinal": True, "parentFinalSha256": EXPECTED["parent_final"]},
        "queueAndDecisionState": {"applied": 828, "pending": 20, "acceptedUnapplied": 0, "fortressAccepted": False, "fortressApplied": False, "witnessSealed": False, "applicationAuthorized": False},
    }
    request = """# Director review request: PG328-W01 damage sub-witness 403 Repack02

This is a narrow corrective repack of reviewed Witness403. R1–R5 remain unchanged. The correction updates three derived carried-item sweep envelopes in W01_GEOMETRY_403.json: focus-A y=[6,11.5], pack-A y=[6,11.5], and cargo-A y=[6,12]. Each sweep is computed from all three recorded actor poses [25,10,0], [25,11,0], and [25,6,0], including the intermediate one-foot excursion. The corrected envelopes still clear the wall. No new geometry premise or rule is added.

Please verify the three R6 values, geometry verification, regenerated manifest/archive hashes, and whether any other partial-witness defect remains. This packet is for partial review only.

Current authority is Queue404: 829 applied / 19 pending / 0 accepted-unapplied. Queue counts embedded in the historical replay remain historical. This remains PARTIAL_WITNESS / NO_SEAL: do not seal W01, accept or apply Fortress, mutate canon/fixture/queue, or change other holds/seals. Geometry405's support and usable-volume proposal remains PROPOSAL_ONLY / NOT ADOPTED. Report the corrected partial-witness review and exact remaining predicates only.
"""

    file_map: dict[str, bytes] = {}
    file_map["OWNER_W01_CONSTRUCTION_AUTHORIZATION_403.json"] = write_json(OUT / "OWNER_W01_CONSTRUCTION_AUTHORIZATION_403.json", owner_auth)
    file_map["SOURCE_BINDINGS_403.json"] = write_json(OUT / "SOURCE_BINDINGS_403.json", {"id": "PG328-W01-SOURCE-BINDINGS-403", "sources": source_records})
    file_map["W01_GEOMETRY_403.json"] = write_json(OUT / "W01_GEOMETRY_403.json", geometry)
    file_map["W01_REPLAY_403.json"] = write_json(OUT / "W01_REPLAY_403.json", replay_record)
    file_map["DIRECTOR_REVIEW_REQUEST_403.md"] = write_utf8_lf(OUT / "DIRECTOR_REVIEW_REQUEST_403.md", request)
    readme = """# PG328-W01 TEST_ONLY damage sub-witness 403 Repack02

This narrow corrective repack preserves the reviewed partial branch and corrects the derived focus-A, pack-A, and cargo-A sweep envelopes to include the intermediate y=11 pose. It otherwise retains the source bindings, Counterspell decisions, component availability, Mobile timing, Spell Efficiency markers, tile creation, and one 17-vs-17 Attack/Sunder hit for 5 bludgeoning damage (panel HP 60 to 55).

The corrected bounds are focus-A y=[6,11.5], pack-A y=[6,11.5], and cargo-A y=[6,12]; each uses all three recorded actor positions and still clears the wall. The complete Fortress support and navigation graphs remain open, including Q23 keep-stair/landing geometry. No support/collapse rule, Q23 repair, canonical Spell Efficiency overlap rule, seal, spell acceptance/application, or queue change is included. Current Queue404 authority is 829/19/0.
"""
    file_map["README_403.md"] = write_utf8_lf(OUT / "README_403.md", readme)

    verification = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-VERIFICATION-403-REPACK02",
        "status": "PASS_PARTIAL_TEST_ONLY_REPLAY; R6_CORRECTED; W01_OPEN",
        "checks": {
            "sourceHashesAndPointers": "PASS; Rulebook v6 and Combat Action bind exact Git HEAD blob bytes; Git HEAD preflight pinned; every JSON pointer resolved individually; text lines stored as text locators",
            "historicalParentFinalHash": "PASS",
            "forwardPatchesInOrder": "PASS",
            "inversePatchesReverseOrder": "PASS",
            "fullParentRestoration": "PASS",
            "minorConjurationCost": "1 RP; PASS",
            "tileWithinCardSizeAndWeight": "PASS",
            "firstDistinctMatrixBaseDissonance": "0; PASS",
            "turnAndInteractionBudgets": "PASS for branch turns; spent/unused closeouts recorded; processed nextEnd markers cleared; off-turn Reaction preserved",
            "turnStancesAndMobileAllowance": "PASS; A chooses Mobile at 6.05 before cast, allowance 5→4→0 and movement 30→29→24; prior stance/allowance resets at 12.0; inherited parent turns unchanged",
            "counterspellEligibilityAndDecision": "PASS bounded; A makes no TEST_ONLY attempt with eligibility unadjudicated; B is eligible at 10 ft and explicitly declines; C/D dispositions recorded; no cost/reaction/recharge change",
            "componentAvailability": "PASS as TEST_ONLY premise; A free hand/voice/focus and B left focus-B/right free/voice are mapped; omitted card list does not create an exemption or material cost",
            "spellEfficiencyLifecycle": "PASS TEST_ONLY ledger; old marker ends 6.9, new Minor Conjuration marker ends 12.9; no repeat, discount or canonical overlap rule asserted",
            "bodyAndObjectGeometry": "PASS local predicates; focus-A and pack-A sweep y=[6,11.5], cargo-A sweep y=[6,12], each computed from all three recorded poses including [25,11,0]; corrected sweeps clear the wall and created tile, and occupied bounds remain within A's body envelope at every recorded pose",
            "eventSnapshotReferences": "PASS; every event before/after ID exists",
            "attackArithmetic": "17 vs AC17; hit; PASS",
            "damageArithmetic": "5 bludgeoning; 60 to 55; PASS",
            "unresolvedSupportAndNavigationMarkedOpen": "PASS",
            "witnessSeal": "NOT ISSUED",
            "fortressAcceptanceApplication": "NOT AUTHORIZED",
            "queueMutation": "NONE; historical replay snapshot 828/20/0 preserved; current Queue404 authority 829/19/0",
        },
        "eventCount": len(events),
        "stateSnapshotCount": len(snapshots),
        "eventHashes": [{"eventId": e["eventId"], "before": e["beforeSha256"], "after": e["afterSha256"]} for e in events],
        "openPredicates": ["complete panel/support map", "mechanical support validity", "whole-structure legal navigation", "keep-stair/landing geometry under PG9-Q23", "inherited parent A/B stance records are not rewritten", "canonical Spell Efficiency overlap semantics remain outside this TEST_ONLY packet"],
    }
    file_map["VERIFICATION_403.json"] = write_json(OUT / "VERIFICATION_403.json", verification)
    crc_rows = []
    for name, raw in sorted(file_map.items()):
        crc_rows.append({"path": name, "bytes": len(raw), "sha256": sha256(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
    manifest = {"id": "PG328-W01-DAMAGE-SUBWITNESS-MANIFEST-403-REPACK02", "schemaVersion": 1, "members": crc_rows}
    manifest_raw = write_json(OUT / "MANIFEST_403.json", manifest)
    zip_path = OUT / ARCHIVE_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(file_map):
            zf.writestr(name, file_map[name])
        zf.writestr("MANIFEST_403.json", manifest_raw)
    archive_raw = zip_path.read_bytes()
    delivery = {
        "id": "PG328-W01-DAMAGE-SUBWITNESS-DELIVERY-403-REPACK02",
        "status": "READY_FOR_DIRECTOR_REVIEW; PARTIAL_WITNESS; NO_SEAL",
        "archive": {"path": ARCHIVE_NAME, "bytes": len(archive_raw), "sha256": sha256(archive_raw)},
        "manifest": {"path": "MANIFEST_403.json", "bytes": len(manifest_raw), "sha256": sha256(manifest_raw)},
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["conjure-demiplane-fortress"],
        "blockerIds": ["PG200-B06"],
        "queue": {"applied": 829, "pending": 19, "acceptedUnapplied": 0},
        "witnessSealed": False,
        "applicationAuthorized": False,
        "canonicalMutation": False,
        "fixtureMutation": False,
        "queueMutation": False,
    }
    write_json(OUT / "DELIVERY_403.json", delivery)

    # Check archived members against the manifest and re-open the zip.
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        expected_names = set(file_map) | {"MANIFEST_403.json"}
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
