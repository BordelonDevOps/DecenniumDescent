#!/usr/bin/env python3
"""Build the adopted DF218-B04 incoming-Steed TEST_ONLY witness replay."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "invulnerable_sphere_witness_423"
ADOPTION = BASE / "invulnerable_sphere_owner_adoption_422/OWNER_SPHERE_PREMISES_ADOPTION_422_TESTONLY.json"
RETURN_ZIP = BASE / "invulnerable_sphere_director_candidate_421/W02_Repack02_Readback_Sphere_Candidate.zip"
PROFILE_O = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/planartravel6_reviewed_133/ACTOR_PROFILES.json"
PROFILE_C = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186/ACTOR_PROFILES.json"
STEED_CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SPHERE_PROCEDURE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218/DIRECTOR_RETURN/procedures/invulnerable-sphere.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_404.json"
PACKET_NAME = "DD_Rank9_InvulnerableSphere_DF218-B04_Witness_423_TESTONLY.zip"
INITIAL_TIME = -3300.0
ORIGIN_MOUNT_BOX = [[-5, 5], [-5, 5], [0, 6]]


def raw_sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return raw_sha(canonical(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    if isinstance(before, dict) and isinstance(after, dict):
        ops: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child = f"{path}/{key.replace('~', '~0').replace('/', '~1')}"
            if key not in before:
                ops.append({"op": "add", "path": child, "value": copy.deepcopy(after[key])})
            elif key not in after:
                ops.append({"op": "remove", "path": child})
            else:
                ops.extend(patch_diff(before[key], after[key], child))
        return ops
    if isinstance(before, list) and isinstance(after, list):
        if before != after:
            return [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]
        return []
    if before != after:
        if not path:
            raise ValueError("Root replacement is not used")
        return [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]
    return []


def apply_patch(document: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(document)
    for operation in operations:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in operation["path"][1:].split("/")]
        parent: Any = result
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = parts[-1]
        if operation["op"] == "add":
            if isinstance(parent, list):
                parent.insert(int(key), copy.deepcopy(operation["value"]))
            else:
                if key in parent:
                    raise ValueError(f"Add target exists: {operation['path']}")
                parent[key] = copy.deepcopy(operation["value"])
        elif operation["op"] == "remove":
            if isinstance(parent, list):
                del parent[int(key)]
            else:
                del parent[key]
        elif operation["op"] == "replace":
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                parent[key] = copy.deepcopy(operation["value"])
        else:
            raise ValueError(f"Unsupported patch op {operation['op']}")
    return result


def invert(operations: list[dict[str, Any]], before: Any) -> list[dict[str, Any]]:
    inverse: list[dict[str, Any]] = []
    for operation in reversed(operations):
        op = operation["op"]
        path = operation["path"]
        if op == "add":
            inverse.append({"op": "remove", "path": path})
        elif op == "remove":
            parts = [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")]
            old: Any = before
            for part in parts:
                old = old[int(part)] if isinstance(old, list) else old[part]
            inverse.append({"op": "add", "path": path, "value": copy.deepcopy(old)})
        elif op == "replace":
            parts = [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")]
            old: Any = before
            for part in parts:
                old = old[int(part)] if isinstance(old, list) else old[part]
            inverse.append({"op": "replace", "path": path, "value": copy.deepcopy(old)})
    return inverse


def geometry_box(anchor: list[float], extent: list[float]) -> list[list[float]]:
    x, y, z = anchor
    w, d, h = extent
    return [[x - w / 2, x + w / 2], [y - d / 2, y + d / 2], [z, z + h]]


def add_event(specs: list[dict[str, Any]], time: float, order: int, actor: str, kind: str, detail: str) -> None:
    specs.append({"timeSeconds": round(time, 10), "order": order, "actor": actor, "kind": kind, "details": detail})


def make_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    add_event(specs, -3300, 10, "C", "C_PREPARATION_BEGIN", "Begin ordinary 45-minute preparation of the unchanged 24-entry Wizard18 repertoire.")
    add_event(specs, -600, 10, "C", "C_PREPARATION_COMPLETE", "Complete the 45-minute preparation; Invulnerable Sphere is in the 24-entry repertoire. No rest or RP recovery is granted.")
    add_event(specs, -600, 20, "O", "O_STUDY_BEGIN", "Begin the existing once-per-long-rest, 10-minute Spellbook Study substitution with the accessible original book; reserve the single use.")
    add_event(specs, 0, 10, "O", "O_STUDY_COMPLETE", "Replace true-polymorph with summon-spectral-steed; keep shield. Consume the Study use. Preserve all spellbook entries and encounter family history.")

    for n in range(11):
        t = n * 6.0
        add_event(specs, t, 20, "C", "REGULAR_START", f"C regular START {n + 1}; refresh C's actual turn budget and cast flag.")
        add_event(specs, t + 1.9, 20, "C", "REGULAR_END", f"C regular END {n + 1}; close the turn without resetting cast/Dissonance history.")
    for n in range(11):
        t = 2.0 + n * 6.0
        add_event(specs, t, 20, "O", "REGULAR_START", f"O regular START {n + 1}; refresh O's actual turn budget and cast flag.")
        if t < 62.0:
            add_event(specs, t + 1.9, 20, "O", "REGULAR_END", f"O regular END {n + 1}; close the turn without resetting cast/Dissonance history.")
    for n in range(10):
        t = 3.91 + n * 6.0
        add_event(specs, t, 30, "S1", "STEED_ATTACHED_PHASE", "Dispatch S1's attached phase after O's whole turn. At the commanded phase it performs Planar Crossing; at all other phases it defaults to Dodge.")

    fixed = [
        (0.2, 10, "C", "CAST_SPHERE", "Commit C's paid Action/V/S/F Sphere cast: 26 RP; first distinct family protected, Refrain 0. Resolve the cast window; no eligible responder exists across planes."),
        (0.21, 10, "C", "MANIFEST_SPHERE", "Manifest the fixed 10-ft-radius, 1-inch closed shell at DESTINATION [0,0,20]. Initial enclosure roster is empty; deadline is 60.21."),
        (2.2, 10, "O", "CAST_STEED", "Commit O's paid Action/V/S/F Steed cast: 5 RP; first distinct family protected, Refrain 0. Resolve the cast window; no eligible responder exists across planes."),
        (2.21, 10, "O", "CREATE_STEED", "Create S1 in the perceived clear ORIGIN mount footprint [0,0,0], within 60 ft and line of effect. Initialize its single crossing use and original deadline at O's tenth future regular START, 62.0."),
        (8.2, 10, "O", "MOUNT_STEED", "Spend O's Action to mount stationary adjacent S1 at the selected 5-ft footprint portion; rider position [2.5,0,6]. Total 170 lb / 7 Load is within capacity and Burdened."),
        (8.3, 10, "O", "COMMAND_CROSSING", "Spend O's shared Bonus Action command for Planar Crossing to the previously known DESTINATION site; O is willing and the command is perceived within 60 ft."),
        (9.92, 10, "S1", "COMMIT_CROSSING_ATTEMPT", "Spend S1's Action and its one crossing use at attempt start; snapshot the complete mounted group and all O-custodied gear for atomic resolution."),
        (9.93, 10, "S1", "SPHERE_DENIAL", "The complete Sphere is the sole blocker. Deny planar entry atomically; no translation or arrival occurs; preserve exact origin poses/custody and both original concentration deadlines. Give no refund, retry, hidden reason, or hidden coordinates."),
        (14.2, 10, "O", "DISMOUNT", "After actual O START 3, spend Action to dismount stationary S1 to legal adjacent ORIGIN box [5,10] x [-2.5,2.5] x [0,6]. No teleport or refunded command/attempt."),
        (60.21, 10, "C", "SPHERE_EXPIRES", "End Sphere at its original 60-second deadline. Do not retry or restore the Steed crossing use."),
        (62.0, 30, "S1", "STEED_EXPIRES", "At O's tenth future regular START, end the original Steed application and its concentration. O is already dismounted; create no corpse/loot/resource trigger and do not delete O's property."),
    ]
    for time, order, actor, kind, detail in fixed:
        add_event(specs, time, order, actor, kind, detail)
    return sorted(specs, key=lambda s: (s["timeSeconds"], s["order"], s["actor"], s["kind"]))


def build_state(proposal: dict[str, Any], owner_adoption: dict[str, Any], profiles_o: dict[str, Any], profiles_c: dict[str, Any], bindings: dict[str, Any]) -> dict[str, Any]:
    o_profile = profiles_o["WTRUE17"]
    c_profile = profiles_c["Wizard18"]
    destination_repertoire = list(c_profile["ordinaryRepertoire"])
    if len(destination_repertoire) != 24 or "invulnerable-sphere" not in destination_repertoire:
        raise ValueError("Bound Wizard18 24-entry repertoire does not contain Sphere as expected")
    if not any(item.get("spellId") == "summon-spectral-steed" for item in o_profile["spellbook"]):
        raise ValueError("WTRUE17 source spellbook does not include Summon Spectral Steed")

    destination_mount = [[-5, 5], [-5, 5], [14, 20]]
    destination_rider = [[0, 5], [-2.5, 2.5], [20, 26]]
    destination_caster = [[27.5, 32.5], [-2.5, 2.5], [0, 6]]
    shell_center = [0, 0, 20]
    sphere = proposal["geometry"]

    state: dict[str, Any] = {
        "schemaVersion": 1,
        "caseId": "DF218-B04-INCOMING-STEED-CANDIDATE-2026-11-01",
        "witnessId": "DF218-B04-WITNESS-423",
        "classification": "OWNER_ADOPTED_TEST_ONLY_HYPOTHETICAL_WITNESS_PENDING_DIRECTOR_REVIEW",
        "timeSeconds": INITIAL_TIME,
        "elapsedSecondsFromWitnessStart": 0.0,
        "processedEventIds": [],
        "queueAuthority": {"queueId": "CURRENT-SPELL-QUEUE-404", "applied": 829, "pending": 19, "acceptedUnapplied": 0},
        "disposition": {"acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"], "blockerIds": ["DF218-B04"], "accepted": False, "applied": False, "sealed": False},
        "scene": {
            "premiseAdoptionRecord": "OWNER-DF218-B04-SP-CAND-P01-P05-ADOPTION-422",
            "planeFrames": {
                "ORIGIN": {"classification": "TEST_ONLY abstract frame", "planeDistinctFrom": "DESTINATION", "groundZ": 0, "workingVolume": [[-100, 100], [-100, 100], [-20, 100]], "ordinaryGroundClear": True},
                "DESTINATION": {"classification": "TEST_ONLY abstract frame", "planeDistinctFrom": "ORIGIN", "groundZ": 0, "workingVolume": [[-100, 100], [-100, 100], [-20, 100]], "ordinaryGroundClear": True},
            },
            "knowledgeRecord": {
                "id": "SP-CAND-SITE-01", "reader": "O", "readBeforePreparation": True,
                "uniquelyIdentifiesFrame": "DESTINATION", "arrivalSteedAnchor": [0, 0, 14],
                "orientationBasis": "identity; preserve all relative positions without rotation",
                "clearArrivalVolume": [destination_mount, destination_rider],
                "unsupportedArrivalRule": "legal arrival begins ordinary Falling under bound Steed procedure",
                "revealsSphereOrCaster": False, "itemInCargo": False,
            },
            "objects": {"sphere": None, "mount": None},
            "noOtherActorsObjectsWardsOrInterference": True,
        },
        "actors": {
            "O": {
                "profileId": "WTRUE17", "frame": "ORIGIN", "class": "Wizard", "level": 17,
                "hp": 104, "maxHp": 104, "rp": 40, "maxRp": 64, "temporaryHp": 0,
                "wounds": 0, "injuries": 0, "deathCounters": 0, "alive": True,
                "conditions": [], "null": False, "recharge": 0, "dissonance": 0, "refrain": 0,
                "prepared": ["true-polymorph", "shield"],
                "spellbookEntriesSourcePath": "DescentReviewChanges/ReviewBible/data/public/spell_candidates/planartravel6_reviewed_133/ACTOR_PROFILES.json#/WTRUE17/spellbook",
                "spellbookSha256": bindings["wtrue17Profile"]["sha256"],
                "studyUse": "AVAILABLE", "preparationState": "CURRENT",
                "positionAnchor": "center-XY/feet-Z", "position": [7.5, 0, 0], "bodyBox": [[5, 10], [-2.5, 2.5], [0, 6]],
                "body": {"massLb": 160, "load": 6, "extentFeet": [5, 5, 6]},
                "inventory": [{"id": "O-KIT-01", "weightLb": 10, "load": 1, "owner": "O", "custodian": "O", "nestedUniqueItemIds": ["O-BOOK-WTRUE17", "O-FOCUS-WTRUE17", "O-COMPONENTS-WTRUE17"], "accessibleFocus": True, "freeSHand": True, "stowedInsideRiderEnvelope": True}],
                "bookAccess": {"bookId": "O-BOOK-WTRUE17", "custody": "O", "location": "O-KIT-01", "status": "STOWED_IN_KIT", "availableForStudy": True, "repackedAfterStudy": False, "weightCountedOnceInAggregate": True},
                "totalRiderPayload": {"weightLb": 170, "load": 7, "limits": {"weightLb": 350, "load": 12}, "withinCapacity": True, "burdened": True, "speedFeet": 50},
                "consent": {"mount": False, "crossing": False},
                "mountedOn": None,
                "concentration": None,
                "castingHistory": [],
                "turn": {"startCount": 0, "endCount": 0, "open": False, "actions": {"action": "UNINITIALIZED", "bonusAction": "UNINITIALIZED", "reaction": "UNINITIALIZED", "movement": "UNINITIALIZED"}, "magicThisTurn": False, "sharedCommandUsed": False},
            },
            "C": {
                "profileId": "Wizard18", "frame": "DESTINATION", "class": "Wizard", "level": 18,
                "hp": 110, "maxHp": 110, "rp": 40, "maxRp": 68, "temporaryHp": 0,
                "wounds": 0, "injuries": 0, "deathCounters": 0, "alive": True,
                "conditions": [], "null": False, "recharge": 0, "dissonance": 0, "refrain": 0,
                "spellbookEntriesSourcePath": "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186/ACTOR_PROFILES.json#/Wizard18/spellbook",
                "spellbookSha256": bindings["wizard18Profile"]["sha256"],
                "preparationBookAccess": {"bookId": "C-BOOK-WIZARD18", "custody": "C", "location": "OFFSCENE_PREPARATION_STATION", "status": "NOT_YET_ACCESSED", "accessedAt": None, "repackedAt": None, "carriedIntoEncounter": False, "includedInC-KIT-01": False},
                "ordinaryRepertoireSourcePath": "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186/ACTOR_PROFILES.json#/Wizard18/ordinaryRepertoire",
                "prepared": [], "preparedCapacity": 24, "preparation": {"status": "NOT_STARTED", "durationSeconds": 2700, "startTime": None, "completionTime": None},
                "positionAnchor": "center-XY/feet-Z", "position": [30, 0, 0], "bodyBox": destination_caster,
                "body": {"massLb": 180, "load": 6, "extentFeet": [5, 5, 6]},
                "inventory": [{"id": "C-KIT-01", "weightLb": 4, "load": 0.4, "owner": "C", "custodian": "C", "nestedUniqueItemIds": ["C-FOCUS-WIZARD18", "C-CLOTHES-WIZARD18"], "accessibleFocus": True, "freeSHand": True}],
                "concentration": None,
                "castingHistory": [],
                "turn": {"startCount": 0, "endCount": 0, "open": False, "actions": {"action": "UNINITIALIZED", "bonusAction": "UNINITIALIZED", "reaction": "UNINITIALIZED", "movement": "UNINITIALIZED"}, "magicThisTurn": False, "sharedCommandUsed": False},
            },
            "S1": None,
        },
        "applications": [],
        "transaction": {"pendingCommand": None, "crossingAttempt": None, "terminalOutcome": None, "automaticRetry": False},
        "sourceBindings": bindings,
    }
    return state


def apply_event(state: dict[str, Any], spec: dict[str, Any], profiles_c: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(state)
    time = float(spec["timeSeconds"])
    if time < float(state["timeSeconds"]):
        raise ValueError("Event clock moved backward")
    result["timeSeconds"] = time
    result["elapsedSecondsFromWitnessStart"] = round(time - INITIAL_TIME, 10)
    event_id = f"SPHERE423:{len(state['processedEventIds']) + 1:03d}:{spec['kind']}"
    result["processedEventIds"].append(event_id)
    kind = spec["kind"]
    actor_id = spec["actor"]

    if kind == "C_PREPARATION_BEGIN":
        c = result["actors"]["C"]
        p = c["preparation"]
        p.update({"status": "IN_PROGRESS", "startTime": time, "completionTime": None})
        c["preparationBookAccess"].update({"status": "OPEN_FOR_PREPARATION", "accessedAt": time})
    elif kind == "C_PREPARATION_COMPLETE":
        c = result["actors"]["C"]
        c["prepared"] = list(profiles_c["Wizard18"]["ordinaryRepertoire"])
        c["preparation"].update({"status": "COMPLETE", "completionTime": time})
        c["preparationBookAccess"].update({"status": "REPACKED_OFFSCENE", "repackedAt": time})
    elif kind == "O_STUDY_BEGIN":
        o = result["actors"]["O"]
        o["studyUse"] = "RESERVED"
        o["preparationState"] = "STUDY_IN_PROGRESS"
        o["bookAccess"].update({"status": "OPEN_FOR_STUDY", "openedAt": time})
    elif kind == "O_STUDY_COMPLETE":
        o = result["actors"]["O"]
        o["prepared"] = ["summon-spectral-steed", "shield"]
        o["studyUse"] = "SPENT"
        o["preparationState"] = "STUDY_COMPLETE"
        o["bookAccess"].update({"status": "REPACKED_IN_KIT", "repackedAt": time})
    elif kind == "REGULAR_START":
        a = result["actors"][actor_id]
        a["turn"]["startCount"] += 1
        a["turn"]["open"] = True
        a["turn"]["lastStartTime"] = time
        a["turn"]["actions"] = {"action": "AVAILABLE", "bonusAction": "AVAILABLE", "reaction": "AVAILABLE", "movement": "AVAILABLE"}
        a["turn"]["magicThisTurn"] = False
        a["turn"]["sharedCommandUsed"] = False
    elif kind == "REGULAR_END":
        a = result["actors"][actor_id]
        if not a["turn"]["open"]:
            raise ValueError(f"Regular END without open turn: {actor_id} at {time}")
        a["turn"]["endCount"] += 1
        a["turn"]["open"] = False
        a["turn"]["lastEndTime"] = time
    elif kind == "CAST_SPHERE":
        c = result["actors"]["C"]
        if c["rp"] < 26 or c["turn"]["actions"]["action"] != "AVAILABLE" or "invulnerable-sphere" not in c["prepared"]:
            raise ValueError("C's Sphere cast failed source preflight")
        c["rp"] -= 26
        c["turn"]["actions"]["action"] = "SPENT"
        c["turn"]["magicThisTurn"] = True
        c["concentration"] = {"status": "PENDING_MANIFESTATION", "applicationId": "DF218-B04-W423-SPHERE-01", "originalDeadline": 60.21}
        c["castingHistory"].append({"spell": "invulnerable-sphere", "family": "invulnerable-sphere", "time": time, "rpPaid": 26, "firstDistinctFamily": True, "protectedBaseDissonance": 2, "effectiveDissonance": 0, "refrain": 0, "components": ["V", "S", "F"], "componentCustodyAtCast": {"voice": "C", "freeSHand": True, "focusId": "C-FOCUS-WIZARD18", "focusAccessible": True}, "preparationBookRepackedBeforeCast": c["preparationBookAccess"]["status"] == "REPACKED_OFFSCENE", "eligibleCounterResponders": [], "interruptionWindow": "RESOLVED_NO_ELIGIBLE_RESPONDER"})
        result["scene"]["objects"]["sphere"] = {"status": "CAST_PENDING", "caster": "C", "center": [0, 0, 20], "radiusFeet": 10, "thicknessFeet": 1 / 12, "deadline": None, "insideCreatures": [], "complete": True}
    elif kind == "MANIFEST_SPHERE":
        sphere = result["scene"]["objects"]["sphere"]
        if not sphere or sphere["status"] != "CAST_PENDING":
            raise ValueError("Sphere manifestation without committed cast")
        sphere.update({"status": "ACTIVE", "manifestationTime": time, "deadline": time + 60, "clearAtEstablishment": True, "consentingEnclosureRoster": [], "boundaryIntersectsBodyOrSolid": False, "fixedAtManifestation": True})
        result["actors"]["C"]["concentration"]["status"] = "ACTIVE"
        result["applications"].append({"applicationId": "DF218-B04-W423-SPHERE-01", "spell": "invulnerable-sphere", "caster": "C", "manifestationTime": time, "deadline": time + 60, "status": "ACTIVE"})
    elif kind == "CAST_STEED":
        o = result["actors"]["O"]
        if o["rp"] < 5 or o["turn"]["actions"]["action"] != "AVAILABLE" or "summon-spectral-steed" not in o["prepared"]:
            raise ValueError("O's Steed cast failed source preflight")
        o["rp"] -= 5
        o["turn"]["actions"]["action"] = "SPENT"
        o["turn"]["magicThisTurn"] = True
        o["concentration"] = {"status": "PENDING_MANIFESTATION", "applicationId": "DF218-B04-W423-STEED-01", "originalDeadline": 62.0}
        o["castingHistory"].append({"spell": "summon-spectral-steed", "family": "summon-spectral-steed", "time": time, "rpPaid": 5, "firstDistinctFamily": True, "protectedBaseDissonance": 1, "effectiveDissonance": 0, "refrain": 0, "components": ["V", "S", "F"], "componentCustodyAtCast": {"voice": "O", "freeSHand": True, "focusId": "O-FOCUS-WTRUE17", "focusAccessible": True}, "bookRepackedBeforeCast": o["bookAccess"]["status"] == "REPACKED_IN_KIT", "eligibleCounterResponders": [], "interruptionWindow": "RESOLVED_NO_ELIGIBLE_RESPONDER"})
    elif kind == "CREATE_STEED":
        result["actors"]["O"]["concentration"]["status"] = "ACTIVE"
        result["actors"]["S1"] = {
            "id": "S1", "profile": "Summon Spectral Steed", "frame": "ORIGIN", "status": "ACTIVE",
            "positionAnchor": "center-XY/feet-Z", "position": [0, 0, 0], "bodyBox": copy.deepcopy(ORIGIN_MOUNT_BOX),
            "body": {"massLb": 500, "extentFeet": [10, 10, 6], "ac": 14, "hp": 30, "maxHp": 30, "saves": "owner PB 6", "otherChecks": 0},
            "speedFeet": 50, "baseSpeedFeet": 60, "burdened": True, "owner": "O", "rider": None,
            "crossingUsesRemaining": 1, "originalExpiryAtOwnerFutureStartNumber": 10, "originalDeadline": 62.0,
            "attachedPhases": 0, "action": "AVAILABLE", "command": None, "lastAction": None,
        }
        result["scene"]["objects"]["mount"] = {"id": "S1", "applicationId": "DF218-B04-W423-STEED-01", "status": "ACTIVE", "position": [0, 0, 0]}
        result["applications"].append({"applicationId": "DF218-B04-W423-STEED-01", "spell": "summon-spectral-steed", "caster": "O", "manifestationTime": time, "deadline": 62.0, "status": "ACTIVE"})
    elif kind == "MOUNT_STEED":
        o, s = result["actors"]["O"], result["actors"]["S1"]
        o["turn"]["actions"]["action"] = "SPENT"
        o["consent"]["mount"] = True
        o["mountedOn"] = "S1"
        o["position"] = [2.5, 0, 6]
        o["bodyBox"] = [[0, 5], [-2.5, 2.5], [6, 12]]
        s["rider"] = "O"
        s["riderFootprintPortion"] = [[0, 5], [-2.5, 2.5]]
    elif kind == "COMMAND_CROSSING":
        o, s = result["actors"]["O"], result["actors"]["S1"]
        o["turn"]["actions"]["bonusAction"] = "SPENT"
        o["turn"]["sharedCommandUsed"] = True
        o["consent"]["crossing"] = True
        s["command"] = {"type": "Planar Crossing", "destination": "DESTINATION", "issuedTime": time, "perceived": True, "ownerBonusActionSpent": True}
        result["transaction"]["pendingCommand"] = copy.deepcopy(s["command"])
    elif kind == "STEED_ATTACHED_PHASE":
        s = result["actors"]["S1"]
        if not s or s["status"] != "ACTIVE":
            raise ValueError("Attached phase dispatched for inactive Steed")
        s["attachedPhases"] += 1
        s["action"] = "AVAILABLE"
        if s["command"] and s["command"]["type"] == "Planar Crossing" and not result["transaction"]["crossingAttempt"]:
            s["lastAction"] = "Planar Crossing"
        else:
            s["lastAction"] = "Dodge"
            s["action"] = "SPENT"
    elif kind == "COMMIT_CROSSING_ATTEMPT":
        s = result["actors"]["S1"]
        if s["lastAction"] != "Planar Crossing" or s["crossingUsesRemaining"] != 1 or not result["actors"]["O"]["consent"]["crossing"]:
            raise ValueError("Crossing attempt lacks valid command, phase, consent or remaining use")
        s["action"] = "SPENT"
        s["crossingUsesRemaining"] = 0
        result["transaction"]["crossingAttempt"] = {"startTime": time, "status": "COMMITTED", "useSpent": True, "actionSpent": True, "payload": ["S1", "O", "O-KIT-01", "O-BOOK-WTRUE17", "O-FOCUS-WTRUE17", "O-COMPONENTS-WTRUE17"], "originPoses": {"O": [2.5, 0, 6], "S1": [0, 0, 0]}}
    elif kind == "SPHERE_DENIAL":
        tx = result["transaction"]["crossingAttempt"]
        if not tx or tx["status"] != "COMMITTED" or not result["scene"]["objects"]["sphere"]["complete"]:
            raise ValueError("Sphere denial lacks a committed attempt or complete Sphere")
        tx.update({"status": "DENIED_AT_ORIGIN", "resultTime": time, "soleBlocker": "complete Invulnerable Sphere excludes planar entry", "translated": False, "refund": False, "retryQueued": False, "hiddenReasonDisclosed": False, "hiddenCoordinatesDisclosed": False})
        result["transaction"]["terminalOutcome"] = "SPHERE_DENIAL_AT_ORIGIN"
    elif kind == "DISMOUNT":
        o, s = result["actors"]["O"], result["actors"]["S1"]
        if not o["turn"]["open"] or o["turn"]["actions"]["action"] != "AVAILABLE" or o["mountedOn"] != "S1":
            raise ValueError("Dismount lacks an available Action, open turn or rider")
        o["turn"]["actions"]["action"] = "SPENT"
        o["mountedOn"] = None
        o["position"] = [7.5, 0, 0]
        o["bodyBox"] = [[5, 10], [-2.5, 2.5], [0, 6]]
        s["rider"] = None
    elif kind == "SPHERE_EXPIRES":
        sphere = result["scene"]["objects"]["sphere"]
        if sphere["status"] != "ACTIVE" or abs(time - sphere["deadline"]) > 1e-8:
            raise ValueError("Sphere expiration is not at its original deadline")
        sphere["status"] = "EXPIRED"
        sphere["endedTime"] = time
        result["actors"]["C"]["concentration"] = None
        result["applications"][0]["status"] = "EXPIRED"
        result["transaction"]["automaticRetry"] = False
    elif kind == "STEED_EXPIRES":
        s = result["actors"]["S1"]
        if s["status"] != "ACTIVE" or abs(time - s["originalDeadline"]) > 1e-8 or s["rider"] is not None:
            raise ValueError("Steed expiration is mistimed or still has a rider")
        s["status"] = "EXPIRED"
        s["endedTime"] = time
        s["action"] = "ENDED"
        result["scene"]["objects"]["mount"]["status"] = "EXPIRED"
        result["actors"]["O"]["concentration"] = None
        result["applications"][1]["status"] = "EXPIRED"
        result["transaction"]["automaticRetry"] = False
    else:
        raise ValueError(f"Unknown event kind: {kind}")
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    adoption = read_json(ADOPTION)
    with zipfile.ZipFile(RETURN_ZIP) as archive:
        proposal_bytes = archive.read("SPHERE_CANDIDATE_PROPOSAL.json")
        proposal = json.loads(proposal_bytes)
    if raw_sha(proposal_bytes) != adoption["scope"]["proposalSha256"]:
        raise ValueError("Adoption record does not bind the exact candidate premise bytes")
    profile_o_raw, profile_c_raw, catalog_raw, sphere_raw = [p.read_bytes() for p in (PROFILE_O, PROFILE_C, STEED_CATALOG, SPHERE_PROCEDURE)]
    profile_o, profile_c, catalog, sphere_proc = [json.loads(raw) for raw in (profile_o_raw, profile_c_raw, catalog_raw, sphere_raw)]
    owner_profile = profile_o["WTRUE17"]
    c_profile = profile_c["Wizard18"]
    steed_card = catalog["spells"][143]["operational"]
    if steed_card["id"] != "summon-spectral-steed":
        raise ValueError("Catalog index 143 no longer binds Summon Spectral Steed")
    if "DF9-Q23" not in sphere_proc.get("procedureText", "") or "DF9-Q24" not in sphere_proc.get("procedureText", ""):
        raise ValueError("Bound Sphere procedure is missing Q23/Q24 clauses")

    bindings = {
        "candidateProposal": {"path": str(RETURN_ZIP.relative_to(ROOT).as_posix()) + "#SPHERE_CANDIDATE_PROPOSAL.json", "sha256": raw_sha(proposal_bytes)},
        "ownerAdoption": {"path": str(ADOPTION.relative_to(ROOT).as_posix()), "sha256": raw_sha(ADOPTION.read_bytes())},
        "wtrue17Profile": {"path": PROFILE_O.relative_to(ROOT).as_posix(), "sha256": raw_sha(profile_o_raw), "pointer": "/WTRUE17"},
        "wizard18Profile": {"path": PROFILE_C.relative_to(ROOT).as_posix(), "sha256": raw_sha(profile_c_raw), "pointer": "/Wizard18"},
        "steedOperationalCatalog": {"path": STEED_CATALOG.relative_to(ROOT).as_posix(), "sha256": raw_sha(catalog_raw), "pointer": "/spells/143/operational"},
        "sphereProcedure": {"path": SPHERE_PROCEDURE.relative_to(ROOT).as_posix(), "sha256": raw_sha(sphere_raw), "pointers": ["/procedureText", "/nativeCardAndAccessUnchanged"]},
        "queue404": {"path": QUEUE.relative_to(ROOT).as_posix(), "sha256": raw_sha(QUEUE.read_bytes()), "applied": 829, "pending": 19, "acceptedUnapplied": 0},
        "heldB4Parent": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_defenseform8_return310_received/DD_Rank9_DefenseForm8_Director_Return310_HELD.zip#cases/RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR.json", "sha256": "fc646a10dc7df8bdac967caf6c9233fe08752a783162fce7f2057a1d0cd559f8", "readOnly": True},
    }
    state = build_state(proposal, adoption, profile_o, profile_c, bindings)
    initial_state = copy.deepcopy(state)
    event_rows: list[dict[str, Any]] = []
    previous_hash = "0" * 64
    specs = make_specs()
    for number, spec in enumerate(specs, start=1):
        before = copy.deepcopy(state)
        state = apply_event(state, spec, profile_c)
        forward = patch_diff(before, state)
        inverse = invert(forward, before)
        if canonical(apply_patch(before, forward)) != canonical(state) or canonical(apply_patch(state, inverse)) != canonical(before):
            raise ValueError(f"Patch reversibility failed at event {number}")
        row = {
            "id": state["processedEventIds"][-1], "timeSeconds": spec["timeSeconds"], "orderAtTimestamp": spec["order"],
            "actor": spec["actor"], "kind": spec["kind"], "details": spec["details"],
            "beforeSHA256": digest(before), "afterSHA256": digest(state),
            "beforeState": before, "afterState": copy.deepcopy(state),
            "forward": forward, "inverse": inverse, "previousEventHash": previous_hash,
        }
        row["eventHash"] = digest({k: v for k, v in row.items() if k != "eventHash"})
        previous_hash = row["eventHash"]
        event_rows.append(row)

    replay = {
        "schemaVersion": 1,
        "id": "DF218-B04-WITNESS-423-REPLAY",
        "classification": "OWNER_ADOPTED_TEST_ONLY_HYPOTHETICAL_WITNESS_PENDING_DIRECTOR_REVIEW",
        "scope": {"identity": "invulnerable-sphere", "blockerId": "DF218-B04", "adoptedPremiseIds": adoption["scope"]["premiseIds"], "parentCaseSha256": adoption["scope"]["heldB4ParentSha256"]},
        "initialState": initial_state,
        "events": event_rows,
        "finalState": state,
        "inverseRestorationOrder": [row["id"] for row in reversed(event_rows)],
        "replaySummary": {"eventCount": len(event_rows), "forwardOperations": sum(len(row["forward"]) for row in event_rows), "inverseOperations": sum(len(row["inverse"]) for row in event_rows), "eventChainHead": previous_hash},
        "limits": {"parentChanged": False, "fixtureChanged": False, "canonicalRuleChanged": False, "queueChanged": False, "accepted": False, "applied": False, "sealed": False, "campaignOrActualPlayClaimed": False},
    }
    write_json(OUT / "SPHERE_WITNESS_REPLAY_423_TESTONLY.json", replay)
    (OUT / "OWNER_SPHERE_PREMISES_ADOPTION_422_TESTONLY.json").write_bytes(ADOPTION.read_bytes())
    (OUT / "SPHERE_CANDIDATE_PROPOSAL_421.json").write_bytes(proposal_bytes)
    write_json(OUT / "SOURCE_BINDINGS_423.json", {"schemaVersion": 1, "id": "DF218-B04-WITNESS-423-SOURCE-BINDINGS", "classification": "READ_ONLY_SOURCE_BINDINGS_FOR_TEST_ONLY_WITNESS", "bindings": bindings})
    readme = """# Invulnerable Sphere DF218-B04 witness 423 (TEST_ONLY)

This packet implements Director proposal 421 only after the owner adopted its exact scene premises SP-CAND-P01 through SP-CAND-P05 in adoption record 422. It is a hypothetical incoming Summon Spectral Steed crossing-denial witness in new abstract ORIGIN and DESTINATION frames. The preserved B4 parent remains held and byte-identical.

The replay contains full before/after state snapshots, hashes, reversible forward/inverse patches, all regular START/END markers for both characters, every attached Steed phase, and the original Sphere and Steed deadlines. It is awaiting independent audit and GPT Director readback.

The witness does not accept or apply Invulnerable Sphere, change canon, mutate any live fixture, repair or relocate B4, change Queue404, or close the DF218-B04 hold. Queue404 remains 829 applied / 19 pending / 0 accepted-unapplied.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    (OUT / "DIRECTOR_REVIEW_REQUEST_423.md").write_text(
        """# GPT Director review request — DF218-B04 witness 423

Please audit the attached `DD_Rank9_InvulnerableSphere_DF218-B04_Witness_423_TESTONLY.zip` against the exact candidate proposal 421, the owner adoption 422, the unchanged source bindings, and the replay invariants. Confirm whether this is a valid separate TEST_ONLY Sphere-denial witness, identify any corrections, and state expressly whether the incoming planar attempt is denied solely by the complete Sphere while preserving the origin group and original clocks.

Do not accept or apply Invulnerable Sphere, edit the held B4 parent, change canon, close DF218-B04, alter any fixture or Queue404, or infer an actual campaign event. Preserve Queue404 at 829/19/0 and all unrelated holds.
""", encoding="utf-8")
    print(json.dumps({"out": str(OUT), "events": len(event_rows), "forwardOperations": replay["replaySummary"]["forwardOperations"], "inverseOperations": replay["replaySummary"]["inverseOperations"], "eventChainHead": previous_hash}, indent=2))


if __name__ == "__main__":
    main()
