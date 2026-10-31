from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = HERE / "banishment_gate_witness365_w08_finite_cargo01"
PACKET = OUT / "packet"
SOURCE_COMMIT = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
W01_DIR = HERE / "banishment_gate_witness365_w01_faction_champion_verified04"
W06_DIR = HERE / "banishment_gate_witness365_w06_planes_shift_repack06_verified04"
AC5_ARCHIVE = W01_DIR / "packet" / "authority" / "AC5_ACCEPTANCE" / "DD_AC5_Local_Final_05.zip"
AC5_RECEIPT = W01_DIR / "packet" / "authority" / "AC5_ACCEPTANCE" / "AC5_EXACT_ACCEPTANCE_05_RECEIPT.json"
GATE_SOURCE = W06_DIR / "packet" / "sources" / "RETURN327_banishment-gate.json"
BODY_SOURCE = W06_DIR / "packet" / "sources" / "rules" / "BODY_EQUIPMENT.md"
COMBAT_SOURCE = W01_DIR / "packet" / "sources" / "COMBAT_ACTION_PLAYTEST.md"


def raw_sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_binding(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": raw_sha(data)}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_hash(value: Any) -> str:
    return raw_sha(canonical(value))


def git_bytes(commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def read_json_bytes(data: bytes) -> Any:
    return json.loads(data.decode("utf-8"))


def diff(before: Any, after: Any, path: list[str] | None = None) -> list[dict[str, Any]]:
    path = [] if path is None else path
    if isinstance(before, dict) and isinstance(after, dict):
        ops: list[dict[str, Any]] = []
        for key in sorted(before.keys() - after.keys()):
            ops.append({"op": "remove", "path": path + [str(key)], "before": copy.deepcopy(before[key])})
        for key in sorted(after.keys() - before.keys()):
            ops.append({"op": "add", "path": path + [str(key)], "after": copy.deepcopy(after[key])})
        for key in sorted(before.keys() & after.keys()):
            ops.extend(diff(before[key], after[key], path + [str(key)]))
        return ops
    if before != after:
        return [{"op": "replace", "path": path, "before": copy.deepcopy(before), "after": copy.deepcopy(after)}]
    return []


def get_at(root: Any, path: list[str]) -> Any:
    current = root
    for part in path:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def set_at(root: Any, path: list[str], value: Any, remove: bool = False) -> None:
    if not path:
        raise ValueError("root replacement is not used by W08 patches")
    current = root
    for part in path[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    key = path[-1]
    if isinstance(current, list):
        idx = int(key)
        if remove:
            current.pop(idx)
        elif idx == len(current):
            current.append(value)
        else:
            current[idx] = value
    elif remove:
        del current[key]
    else:
        current[key] = value


def apply_ops(state: Any, ops: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in ops:
        path = op["path"]
        if op["op"] == "remove":
            assert get_at(result, path) == op["before"]
            set_at(result, path, None, remove=True)
        elif op["op"] == "add":
            set_at(result, path, copy.deepcopy(op["after"]))
        elif op["op"] == "replace":
            assert get_at(result, path) == op["before"]
            set_at(result, path, copy.deepcopy(op["after"]))
        else:
            raise ValueError(f"unknown patch operation {op['op']}")
    return result


def record_event(
    events: list[dict[str, Any]],
    state: dict[str, Any],
    event_id: str,
    seconds: int,
    kind: str,
    description: str,
    mutate: Callable[[dict[str, Any]], None],
    source_pointers: list[str],
) -> dict[str, Any]:
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    mutate(after)
    forward = diff(before, after)
    inverse = list(reversed(diff(after, before)))
    assert apply_ops(before, forward) == after
    assert apply_ops(after, inverse) == before
    event = {
        "eventId": event_id,
        "timestampSeconds": seconds,
        "kind": kind,
        "description": description,
        "sourcePointers": source_pointers,
        "beforeStateSha256": state_hash(before),
        "afterStateSha256": state_hash(after),
        "forwardOperations": forward,
        "inverseOperations": inverse,
        "stateAfter": after,
    }
    events.append(event)
    return after


def add_source_copy(dest: Path, data: bytes) -> dict[str, Any]:
    atomic_write(dest, data)
    return {"member": dest.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": raw_sha(data)}


def make_initial_state() -> dict[str, Any]:
    return {
        "simulationId": "PG327-W08-365-TESTONLY-CARGO-A",
        "evidenceClass": "conditional TEST_ONLY static authored witness; no campaign event asserted",
        "elapsedSeconds": -10,
        "world": {
            "originPlaneKey": "PLANE-W08-TEST-ORIGIN-01",
            "planeIdentityStatus": "opaque conditional fixture reference; no named cosmology asserted",
            "gateWorldPose": {"centerFt": [100, 100, 7.5], "baseZFt": 0, "normal": [1, 0, 0]},
            "terrain": "clear, level, supported, unobstructed outside the gate; all coordinates are TEST_ONLY premises",
        },
        "actors": {
            "gateCaster": {
                "id": "actor-gate-caster-w08",
                "class": "Mage",
                "classLevel": 17,
                "acquiredSpellIds": ["banishment-gate"],
                "spellAccess": {"id": "banishment-gate", "class": "Mage", "rank": 9, "minimumClassLevel": 17, "baseRp": 26},
                "rp": {"initial": 60, "current": 60, "spent": 0},
                "concentration": None,
                "actions": {"actionAvailable": True, "reactionAvailable": True},
                "planeKey": "PLANE-W08-TEST-ORIGIN-01",
                "fixtureStatus": "conditional test actor; not a campaign character",
            },
            "championOwner": {
                "id": "actor-champion-owner-w08",
                "class": "Mage",
                "classLevel": 9,
                "acquiredSpellIds": ["faction-champion"],
                "spellAccess": {"id": "faction-champion", "class": "Mage", "rank": 5, "minimumClassLevel": 9, "baseRp": 10},
                "rp": {"initial": 40, "current": 40, "spent": 0},
                "gold": {"initialGp": 20, "currentGp": 20, "spentGp": 0},
                "concentration": None,
                "factionEligibility": {
                    "factionId": "FACTION-W08-TEST-A",
                    "classification": "explicit conditional TEST_ONLY faction fixture; no real membership asserted",
                    "alliedStatus": True,
                    "currentStanding": 5,
                    "invocationPermission": True,
                    "aidProhibition": False,
                },
                "ownedObjectIds": [],
                "custodyObjectIds": [],
                "actionsAtTurn6": {"actionAvailable": True, "bonusActionAvailable": True},
                "planeKey": "PLANE-W08-TEST-ORIGIN-01",
                "positionFt": [80, 100, 0],
                "fixtureStatus": "conditional test actor; not a campaign character",
            },
            "champion": {
                "id": "summoned-faction-champion-w08",
                "exists": False,
                "bodyState": "not-created",
                "corpseExists": False,
                "intrinsicManifestation": {"status": "not-formed", "worldItems": []},
                "externalObjectIds": [],
                "fixtureBodyGeometry": None,
                "planeKey": "PLANE-W08-TEST-ORIGIN-01",
                "positionFt": None,
                "movement": {"speedFt": 30, "budgetFt": 30, "spentFt": 0, "remainingFt": 30},
            },
        },
        "gate": {"id": "gate-w08-humanoid-01", "status": "not-created", "active": False, "selectedCreatureType": None,
                 "creatorId": "actor-gate-caster-w08", "spellRpSpent": 0, "concentrationDeadlineSeconds": None,
                 "liveCellIds": [], "hardControlClaims": []},
        "cell": None,
        "objects": {},
        "eventReceipts": {},
        "testFixtureBoundaries": {
            "noCampaignFacts": True,
            "noRuntimeExecution": True,
            "noIdentityAcceptance": True,
            "noApplicationAuthorization": True,
            "AC5BanishElementalExtensionImported": False,
            "AC5X17MechanicsImported": False,
            "magicalEndpointBlockerPresent": False,
        },
    }


def build_common_prefix() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    state = make_initial_state()
    initial = copy.deepcopy(state)
    events: list[dict[str, Any]] = []
    object_id = "object-genuine-hooded-lantern-w08-001"

    def acquire(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        owner["gold"]["currentGp"] -= 5
        owner["gold"]["spentGp"] += 5
        owner["ownedObjectIds"].append(object_id)
        owner["custodyObjectIds"].append(object_id)
        s["objects"][object_id] = {
            "id": object_id,
            "name": "Lantern, hooded",
            "quantity": 1,
            "genuine": True,
            "magical": False,
            "sourceCatalogId": "adventuring-gear.lantern-hooded",
            "costGp": 5,
            "weightLb": 2,
            "load": 0.2,
            "ownerId": owner["id"],
            "custodianId": owner["id"],
            "status": "carried-by-owner",
            "physicalPosition": {"planeKey": owner["planeKey"], "worldFt": [80, 100, 0]},
            "sourceAcquisition": {"eventId": "W08-E01-LANTERN-ACQUIRE", "goldPaidGp": 5, "sourceRecordId": "adventuring-gear.lantern-hooded"},
            "damageState": "intact",
        }
        s["elapsedSeconds"] = -10
        s["eventReceipts"]["W08-E01-LANTERN-ACQUIRE"] = {"applied": True, "quantityCreated": 1}

    state = record_event(events, state, "W08-E01-LANTERN-ACQUIRE", -10, "object-acquisition",
                         "Owner pays 5 gp for one source-listed 2 lb hooded lantern; item is genuine and independently acquired.",
                         acquire, ["sources/EQUIPMENT_SOURCE_CATALOG.json#/records/adventuring-gear.lantern-hooded",
                                   "sources/PLAYER_RULEBOOK_V6_SOURCE.txt#line-6976"])

    def cast_gate(s: dict[str, Any]) -> None:
        actor = s["actors"]["gateCaster"]
        actor["rp"]["current"] -= 26
        actor["rp"]["spent"] += 26
        actor["actions"]["actionAvailable"] = False
        actor["concentration"] = {"effectId": "gate-w08-humanoid-01", "startedAtSeconds": -5,
                                  "deadlineSeconds": 595, "maxDurationSeconds": 600, "active": True}
        s["gate"].update({"status": "active", "active": True, "selectedCreatureType": "Humanoid",
                          "spellRpSpent": 26, "castAtSeconds": -5, "concentrationDeadlineSeconds": 595,
                          "aperture": {"widthFt": 10, "heightFt": 15, "baseZFt": 0, "planeNormal": [1, 0, 0],
                                       "supportedClearArea": True},
                          "spellRoute": {"action": True, "components": ["V", "S", "F"], "rangeFt": 120,
                                         "class": "Mage", "rank": 9, "baseRp": 26},
                          "liveCellIds": [], "hardControlClaims": []})
        s["elapsedSeconds"] = -5
        s["eventReceipts"]["W08-E02-GATE-CAST"] = {"paidRp": 26, "gateId": "gate-w08-humanoid-01", "selectedType": "Humanoid"}

    state = record_event(events, state, "W08-E02-GATE-CAST", -5, "gate-creation",
                         "Separate Mage17 Gate caster spends the authored test-route 26 RP and creates a 10x15 ft Gate fixed to the source-qualified Humanoid type; 600-second Gate concentration is separate from later cell deadlines.",
                         cast_gate, ["sources/RETURN327_banishment-gate.json#/procedure#PG9-Q01",
                                     "sources/RETURN327_banishment-gate.json#/procedure#PG9-Q13",
                                     "sources/RETURN327_banishment-gate.json#/procedure#PG9-Q15"])

    def cast_champion(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        owner["rp"]["current"] -= 10
        owner["rp"]["spent"] += 10
        owner["actionsAtTurn6"]["actionAvailable"] = True
        owner["actionsAtTurn6"]["bonusActionAvailable"] = True
        owner["concentration"] = {"effectId": "faction-champion-w08-source", "startedAtSeconds": 0,
                                  "deadlineSeconds": 60, "maxDurationSeconds": 60, "active": True}
        champ = s["actors"]["champion"]
        champ.update({"exists": True, "bodyState": "live", "creatureType": "Humanoid", "size": "Medium",
                      "hp": {"current": 70, "maximum": 70}, "ac": 18, "abilities": {"STR": 18, "DEX": 12, "CON": 16, "INT": 10, "WIS": 12, "CHA": 12},
                      "weightLb": 180, "occupiedHeightFt": 6, "footprintFt": [5, 5],
                      "sourceSpellId": "faction-champion", "sourceProfileId": "AC5-PROFILE-FACTION-CHAMPION-01",
                      "sourceCreatedAtSeconds": 0, "sourceDeadlineSeconds": 60, "sourceEndReason": None,
                      "corpseExists": False,
                      "intrinsicManifestation": {"status": "present", "items": ["intrinsic-armor", "intrinsic-weapon", "intrinsic-shield"],
                                                  "separateInventoryObjects": False},
                      "externalObjectIds": [], "hands": {"left": "free", "right": "free", "basis": "explicit TEST_ONLY anatomy/occupancy fact"},
                      "planeKey": owner["planeKey"], "positionFt": [85, 100, 0],
                      "movement": {"speedFt": 30, "budgetFt": 30, "spentFt": 0, "remainingFt": 30}})
        s["elapsedSeconds"] = 0
        s["eventReceipts"]["W08-E03-CHAMPION-CAST"] = {"paidRp": 10, "championId": champ["id"], "sourceDeadlineSeconds": 60}

    state = record_event(events, state, "W08-E03-CHAMPION-CAST", 0, "finite-summon-creation",
                         "Mage9 with acquired rank5 Faction Champion meets all four conditional AC5 ally predicates and pays 10 RP; a single Medium Humanoid Champion is created with its 60-second original source deadline.",
                         cast_champion, ["sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/profile",
                                         "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/spellAccessAndRoute",
                                         "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/sharedRule"])

    def transfer_cargo(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champ = s["actors"]["champion"]
        item = s["objects"][object_id]
        owner["actionsAtTurn6"]["actionAvailable"] = False
        owner["custodyObjectIds"].remove(object_id)
        champ["externalObjectIds"].append(object_id)
        item["custodianId"] = champ["id"]
        item["status"] = "genuine-borrowed-object-carried-by-summon"
        item["physicalPosition"] = {"planeKey": champ["planeKey"], "worldFt": [85, 100, 0],
                                    "carriedSlot": "left hand", "fixtureFit": "2 lb object; explicitly supplied Medium Humanoid hand/custody fixture"}
        s["eventReceipts"]["W08-E04-LANTERN-LOAN"] = {"itemId": object_id, "ownerUnchanged": True,
                                                       "custodian": champ["id"], "quantity": 1,
                                                       "load": 0.2, "capacityBasis": "Medium STR18: 270 lb physical / 18 Load; item is 2 lb / 0.2 Load"}
        s["elapsedSeconds"] = 6

    state = record_event(events, state, "W08-E04-LANTERN-LOAN", 6, "physical-custody-transfer",
                         "Owner uses one ordinary Action to lend the independently acquired lantern to the Champion; owner remains legal owner. The item is held in a free hand under explicit TEST_ONLY anatomy. 2 lb / 0.2 Load is below the sourced Medium STR18 carrying limits.",
                         transfer_cargo, ["sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/cargoExample",
                                         "sources/rules/BODY_EQUIPMENT.md#lines-88-109",
                                         "sources/COMBAT_ACTION_PLAYTEST.md#turn-object-interaction"])

    def cross_gate(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champ = s["actors"]["champion"]
        gate = s["gate"]
        owner["actionsAtTurn6"]["bonusActionAvailable"] = False
        champ["movement"]["spentFt"] = 20
        champ["movement"]["remainingFt"] = 10
        champ["positionFt"] = [0, 0, 0]
        champ["planeKey"] = "CELL-W08-001"
        s["cell"] = {
            "id": "cell-w08-001", "status": "active", "primaryId": champ["id"],
            "admittedAtSeconds": 6, "deadlineSeconds": 66, "deadlineRule": "Gate admission + 60 seconds",
            "originPlaneKey": s["world"]["originPlaneKey"],
            "originAnchor": {"worldFt": [100, 100, 0], "orientation": 0, "fixedAtAdmission": True},
            "primaryCellLocalPosition": [0, 0, 0], "contents": [champ["id"], object_id],
            "looseCargoIds": [], "closureCount": 0,
            "geometry": {"floor": "level ephemeral support", "bodyFits": True, "lanternFits": True},
            "endpointBlocker": None,
        }
        gate["liveCellIds"].append(s["cell"]["id"])
        gate["hardControlClaims"].append({"targetId": champ["id"], "encounterId": "encounter-w08-test-01", "claimedAtSeconds": 6})
        item = s["objects"][object_id]
        item["physicalPosition"] = {"planeKey": "CELL-W08-001", "cellLocalFt": [0, 0, 0], "carriedSlot": "left hand"}
        item["status"] = "carried-in-gate-cell"
        s["eventReceipts"]["W08-E05-GATE-CROSSING"] = {"crossingId": "crossing-w08-001", "admitted": True,
                                                        "sameChampionId": champ["id"], "cellId": s["cell"]["id"],
                                                        "movementFt": 20, "cellDeadlineSeconds": 66,
                                                        "worldPathStartFt": [85, 100, 0], "worldPathEndFt": [105, 100, 0],
                                                        "gatePlaneXFt": 100, "completeBodyStartXBoundsFt": [82.5, 87.5],
                                                        "completeBodyEndXBoundsFt": [102.5, 107.5],
                                                        "portalWidthClearance": "5-ft body <= 10-ft aperture",
                                                        "portalHeightClearance": "6-ft fixture body <= 15-ft aperture",
                                                        "movementPhase": "attached companion movement after owner turn"}
        s["elapsedSeconds"] = 6

    state = record_event(events, state, "W08-E05-GATE-CROSSING", 6, "matching-full-body-crossing-and-admission",
                         "After the Owner's Action and Bonus Action, the Champion's attached movement phase moves it 20 ft through the clear 10x15 ft aperture. Its complete 5x5 ft footprint and 6 ft fixture height fit; selected type is Humanoid. The same body and carried item enter one distinct Gate cell; no save is used.",
                         cross_gate, ["sources/RETURN327_banishment-gate.json#/procedure#PG9-Q13",
                                     "sources/RETURN327_banishment-gate.json#/procedure#PG9-Q14",
                                     "sources/RETURN327_banishment-gate.json#/procedure#PG9-Q15",
                                     "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/profile"])

    def expire_champion(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champ = s["actors"]["champion"]
        item = s["objects"][object_id]
        owner["concentration"] = None
        champ.update({"exists": False, "bodyState": "expired", "sourceEndReason": "original 60-second concentration deadline",
                      "corpseExists": False, "positionFt": None, "planeKey": None,
                      "intrinsicManifestation": {"status": "vanished", "items": [], "separateInventoryObjects": False},
                      "externalObjectIds": []})
        item["custodianId"] = None
        item["status"] = "loose-genuine-cargo-in-cell"
        item["physicalPosition"] = {"planeKey": "CELL-W08-001", "cellLocalFt": [0, 0, 0], "custodianId": None}
        s["cell"]["contents"] = [object_id]
        s["cell"]["looseCargoIds"] = [object_id]
        s["eventReceipts"]["W08-E06-SUMMON-EXPIRY"] = {"sourceEndedOnce": True, "bodyExists": False,
                                                        "corpseExists": False, "intrinsicGearWorldObjects": 0,
                                                        "genuineCargoSurvives": [object_id], "cellStillActive": True}
        s["elapsedSeconds"] = 60

    state = record_event(events, state, "W08-E06-SUMMON-EXPIRY", 60, "original-summon-source-deadline",
                         "At the Champion's original t=60 source deadline, its body and intrinsic armor/weapon/shield manifestation end without corpse or loot. The one separately acquired lantern becomes loose at its current cell-local position. The Gate cell remains active until its independent t=66 deadline.",
                         expire_champion, ["sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/profile/ending",
                                         "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/profile/intrinsicGear",
                                         "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/cargoExample",
                                         "sources/RETURN327_banishment-gate.json#/procedure#PG9-Q15",
                                         "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/deathAndRemoval"])

    common = {
        "initialState": initial,
        "initialStateSha256": state_hash(initial),
        "events": events,
        "finalState": state,
        "finalStateSha256": state_hash(state),
    }
    return state, events, common


def build_branches(common_state: dict[str, Any]) -> list[dict[str, Any]]:
    object_id = "object-genuine-hooded-lantern-w08-001"
    base_hash = state_hash(common_state)
    anchor = [100, 100, 0]
    specs = [
        {
            "id": "W08-DIRECT-ANCHOR-PLACEMENT",
            "geometry": {"anchorOccupied": False, "anchorBlocked": False, "legalAdjacentItemPositions": [[105, 100, 0]], "blockedAdjacentPositions": []},
            "expected": "placed-at-projected-anchor",
        },
        {
            "id": "W08-OCCUPIED-ANCHOR-ADJACENT-DROP",
            "geometry": {"anchorOccupied": True, "anchorOccupantId": "fixture-occupant-north-01", "anchorBlocked": False,
                          "legalAdjacentItemPositions": [[105, 100, 0]],
                          "blockedAdjacentPositions": [[95, 100, 0], [100, 95, 0], [100, 105, 0], [95, 95, 0], [95, 105, 0], [105, 95, 0], [105, 105, 0]]},
            "expected": "placed-at-nearest-legal-adjacent-position",
        },
        {
            "id": "W08-OCCUPIED-AND-BLOCKED-PENDING-ITEM",
            "geometry": {"anchorOccupied": True, "anchorOccupantId": "fixture-occupant-north-02", "anchorBlocked": True,
                          "legalAdjacentItemPositions": [],
                          "blockedAdjacentPositions": [[95, 100, 0], [105, 100, 0], [100, 95, 0], [100, 105, 0],
                                                       [95, 95, 0], [95, 105, 0], [105, 95, 0], [105, 105, 0]],
                          "blockedBy": "explicit TEST_ONLY solid barriers or stationary fixtures; no item candidate is in the same unobstructed region"},
            "expected": "pending-on-origin-plane; cell-still-destroyed",
        },
    ]
    results: list[dict[str, Any]] = []
    for spec in specs:
        state = copy.deepcopy(common_state)
        events: list[dict[str, Any]] = []

        def set_geometry(s: dict[str, Any], geometry: dict[str, Any] = spec["geometry"]) -> None:
            s["world"]["terminalGeometryFixture"] = copy.deepcopy(geometry)
            s["elapsedSeconds"] = 66
            s["eventReceipts"][f"{spec['id']}-GEOMETRY"] = {"branchId": spec["id"], "capturedAtSeconds": 66,
                                                              "anchor": anchor, "fixtureOnly": True}

        state = record_event(events, state, f"{spec['id']}-GEOMETRY", 66, "terminal-placement-fork",
                             "Create one alternative TEST_ONLY terminal geometry from the common cargo-bearing admission and summon-expiry prefix; no prior history is mutated.",
                             set_geometry, ["sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/looseObjectAnchors",
                                            "sources/rules/BODY_EQUIPMENT.md#lines-50-51"])

        def close_cell(s: dict[str, Any], expected: str = spec["expected"], branch_id: str = spec["id"]) -> None:
            cell = s["cell"]
            item = s["objects"][object_id]
            cell["closureTrigger"] = "independent admission-plus-60-second Gate cell deadline"
            cell["closureStartedAtSeconds"] = 66
            cell["mandatoryPlaneReturn"] = {"completed": True, "toPlaneKey": s["world"]["originPlaneKey"],
                                              "endpointBlockerPresent": False, "endpointBlockerExceptionUsed": False}
            cell["projectedItemAnchor"] = {"planeKey": s["world"]["originPlaneKey"], "worldFt": anchor,
                                           "projectedFromCellLocalFt": [0, 0, 0], "anchorSnapshotUnchanged": True}
            cell["physicalPlacementOutcome"] = expected
            geometry = s["world"]["terminalGeometryFixture"]
            if expected == "placed-at-projected-anchor":
                item["status"] = "placed-at-origin-anchor"
                item["physicalPosition"] = {"planeKey": s["world"]["originPlaneKey"], "worldFt": anchor,
                                            "custodianId": None, "placementPending": False}
            elif expected == "placed-at-nearest-legal-adjacent-position":
                assert geometry["anchorOccupied"] and len(geometry["legalAdjacentItemPositions"]) == 1
                item["status"] = "placed-at-nearest-legal-adjacent-position"
                item["physicalPosition"] = {"planeKey": s["world"]["originPlaneKey"],
                                            "worldFt": geometry["legalAdjacentItemPositions"][0],
                                            "custodianId": None, "placementPending": False,
                                            "displacedOccupant": False}
            else:
                assert geometry["anchorOccupied"] and geometry["anchorBlocked"] and not geometry["legalAdjacentItemPositions"]
                item["status"] = "pending-origin-plane-item-placement"
                item["physicalPosition"] = {"planeKey": s["world"]["originPlaneKey"], "worldFt": None,
                                            "pendingAnchorWorldFt": anchor, "custodianId": None,
                                            "placementPending": True, "creaturePlacementConflict": False}
            cell.update({"status": "closed", "destroyed": True, "closedAtSeconds": 66,
                         "closureCount": cell["closureCount"] + 1,
                         "contents": [], "looseCargoIds": [],
                         "closureReceiptId": f"receipt-{branch_id}-CLOSE-01"})
            s["gate"]["liveCellIds"].remove(cell["id"])
            s["eventReceipts"][f"{branch_id}-CLOSE"] = {
                "receiptId": cell["closureReceiptId"], "cellDestroyed": True, "closureCount": cell["closureCount"],
                "cargoId": object_id, "cargoQuantity": item["quantity"], "cargoStatus": item["status"],
                "bodyRecreated": False, "secondEnding": False, "refundRp": 0,
            }
            s["elapsedSeconds"] = 66

        state = record_event(events, state, f"{spec['id']}-CLOSE", 66, "gate-cell-terminal-closure",
                             "Apply only the Gate's PG200-CELL-EXT terminal return and item-placement rules. Mandatory plane return occurs before physical item placement; cell destruction is independent of pending placement.",
                             close_cell, ["sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/originPlane",
                                         "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/looseObjectAnchors",
                                         "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/mandatoryPlaneReturn",
                                         "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/endpointBlockerException",
                                         "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/objects",
                                         "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/cellEnd",
                                         "sources/rules/BODY_EQUIPMENT.md#lines-50-51"])

        before_duplicate_hash = state_hash(state)
        duplicate_receipt = state["eventReceipts"][f"{spec['id']}-CLOSE"]
        duplicate = {
            "eventId": f"{spec['id']}-DUPLICATE-CLOSE-DELIVERY",
            "timestampSeconds": 66,
            "kind": "duplicate-terminal-callback",
            "description": "A repeated delivery of the same terminal closure key returns its existing receipt and changes no state.",
            "sourcePointers": ["sources/RETURN327_banishment-gate.json#/procedure#PG9-Q29"],
            "beforeStateSha256": before_duplicate_hash,
            "afterStateSha256": before_duplicate_hash,
            "forwardOperations": [],
            "inverseOperations": [],
            "stateAfter": copy.deepcopy(state),
            "duplicateClosureKey": f"{spec['id']}-CLOSE",
            "returnedReceiptId": duplicate_receipt["receiptId"],
        }
        events.append(duplicate)

        reverse = copy.deepcopy(state)
        reverse_checks = []
        for event in reversed(events):
            assert state_hash(reverse) == event["afterStateSha256"]
            reverse = apply_ops(reverse, event["inverseOperations"])
            assert state_hash(reverse) == event["beforeStateSha256"]
            reverse_checks.append({"eventId": event["eventId"], "restoredBeforeHash": state_hash(reverse)})
        assert state_hash(reverse) == base_hash

        results.append({
            "branchId": spec["id"],
            "startStateSha256": base_hash,
            "terminalStateSha256": state_hash(state),
            "expectedOutcome": spec["expected"],
            "events": events,
            "finalState": state,
            "reverseOrder": [e["eventId"] for e in reversed(events)],
            "reverseChecks": reverse_checks,
            "restoresCommonPrefix": state_hash(reverse) == base_hash,
        })
    return results


def main() -> None:
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite existing W08 packet directory: {OUT}")
    PACKET.mkdir(parents=True)
    (PACKET / "sources").mkdir()
    (PACKET / "authority").mkdir()
    (PACKET / "rules").mkdir()

    source_root = PACKET / "sources"
    bindings: list[dict[str, Any]] = []

    gate_src = GATE_SOURCE.read_bytes()
    binding = add_source_copy(source_root / "RETURN327_banishment-gate.json", gate_src)
    bindings.append({"repositoryPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_return327_received/evidence/packet327/prior/procedures/banishment-gate.json",
                     "packetMember": binding["member"], "sourceCommit": SOURCE_COMMIT, **binding,
                     "jsonPointers": ["/procedure (PG9-Q17 adoption; also PG9-Q15 and PG9-Q29)",
                                      "/sharedContract/terminalScope", "/sharedContract/cellExtension",
                                      "/sharedContract/cellExtension/closure"],
                     "directorConfirmed": True})

    body_src = BODY_SOURCE.read_bytes()
    binding = add_source_copy(PACKET / "rules" / "BODY_EQUIPMENT.md", body_src)
    bindings.append({"repositoryPath": "DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md",
                     "packetMember": binding["member"], "sourceCommit": SOURCE_COMMIT,
                     "gitBlobSha1": "60f81c5706857c5528d9d19e3da9ac15dcd7fb85", **binding,
                     "jsonPointers": [], "operativeLines": [50, 51, 88, 89, 90, 94, 95, 96, 97, 98, 99, 100, 101, 103, 109, 145],
                     "reusedFromSealedW07W06": True})

    combat_src = COMBAT_SOURCE.read_bytes()
    binding = add_source_copy(PACKET / "sources" / "COMBAT_ACTION_PLAYTEST.md", combat_src)
    bindings.append({"repositoryPath": "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
                     "packetMember": binding["member"], "sourceCommit": SOURCE_COMMIT, **binding,
                     "jsonPointers": [], "use": "ordinary action/bonus-action budgets only"})

    ac5_zip_data = AC5_ARCHIVE.read_bytes()
    ac5_zip_sha = raw_sha(ac5_zip_data)
    receipt = json.loads(AC5_RECEIPT.read_text(encoding="utf-8"))
    assert receipt["reviewedArchive"]["sha256"] == ac5_zip_sha
    with zipfile.ZipFile(AC5_ARCHIVE) as zf:
        model_data = zf.read("candidate/SPELLS_MODEL.json")
        casebook_data = zf.read("candidate/CASEBOOK.json")
    assert raw_sha(model_data) == "d782569ed8ef558f4edf54634e0d8c19926e24e2437528f1769b5ef3ce594898"
    assert raw_sha(casebook_data) == "9f35f59083b87ca85b40b123150266db71236dbed6d0d216d1760abd22345b58"
    model = read_json_bytes(model_data)
    casebook = read_json_bytes(casebook_data)
    binding = add_source_copy(source_root / "AC5_ACCEPTED_SPELLS_MODEL.json", model_data)
    bindings.append({"repositoryPath": "docs/audit/2026-10-08/full-game/ac5-local-final-05-candidate/SPELLS_MODEL.json",
                     "packetMember": binding["member"], **binding, "acceptedArchiveMember": "candidate/SPELLS_MODEL.json",
                     "acceptedArchiveSha256": ac5_zip_sha})
    binding = add_source_copy(source_root / "AC5_ACCEPTED_CASEBOOK.json", casebook_data)
    bindings.append({"repositoryPath": "docs/audit/2026-10-08/full-game/ac5-local-final-05-candidate/CASEBOOK.json",
                     "packetMember": binding["member"], **binding, "acceptedArchiveMember": "candidate/CASEBOOK.json",
                     "acceptedArchiveSha256": ac5_zip_sha})
    spell = next(x for x in model["spells"] if x.get("id") == "faction-champion")
    profile = model["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    shared = model["sharedRules"]["AC5-CHAMPION-ALLY-01"]
    cargo_case = next(x for x in casebook["cases"] if x.get("id") == "CJ5-07-B")
    case_index = next(i for i, x in enumerate(casebook["cases"]) if x.get("id") == "CJ5-07-B")
    if "faction-champion" not in receipt["acceptedSpellIds"]:
        raise ValueError("AC5 acceptance receipt does not include Faction Champion")
    ac5_extract = {
        "id": "AC5-FACTION-CHAMPION-W08-SOURCE-EXTRACT",
        "evidenceClass": "exact JSON extracts from the accepted AC5 Local Final 05 artifact; source mechanic only, not runtime",
        "acceptance": {"reviewId": receipt["reviewId"], "status": receipt["status"],
                       "reviewedArchiveSha256": ac5_zip_sha, "acceptedSpellId": "faction-champion",
                       "runtimeSelectionEnabled": receipt["runtimeSelectionEnabled"],
                       "runtimeImplemented": receipt["runtimeImplemented"]},
        "sourceMemberBindings": {
            "spellModel": {"archiveMember": "candidate/SPELLS_MODEL.json", "bytes": len(model_data), "sha256": raw_sha(model_data),
                           "sourceJsonPointer": f"/spells/{next(i for i,x in enumerate(model['spells']) if x.get('id') == 'faction-champion')}",
                           "profilePointer": "/profiles/AC5-PROFILE-FACTION-CHAMPION-01",
                           "sharedRulePointer": "/sharedRules/AC5-CHAMPION-ALLY-01"},
            "casebook": {"archiveMember": "candidate/CASEBOOK.json", "bytes": len(casebook_data), "sha256": raw_sha(casebook_data),
                         "casePointer": f"/cases/{case_index}", "caseId": "CJ5-07-B"},
        },
        "spellAccessAndRoute": spell,
        "profile": profile,
        "sharedRule": shared,
        "cargoExample": cargo_case,
        "scopeLimits": [
            "The Faction Champion source is an accepted finite authored profile; native spell selection remains disabled.",
            "Only the Faction Champion's own 60-second finite source, intrinsic manifestation and genuine-object custody/expiry are used.",
            "AC5-BANISH-EXT-01 and AC5-X17 are not used as Gate rules or closure mechanics.",
            "No campaign faction, actor, item loan, or event is asserted. All instance facts are conditional TEST_ONLY fixtures.",
        ],
    }
    write_json(source_root / "AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json", ac5_extract)
    bindings.append({"repositoryPath": receipt["reviewedArchive"]["path"], "sourceArchivePath": receipt["reviewedArchive"]["path"],
                     "sourceCommit": None, "sourceArchiveBytes": len(ac5_zip_data), "sourceArchiveSha256": ac5_zip_sha,
                     "archiveMembers": [
                         {"path": "candidate/SPELLS_MODEL.json", "bytes": len(model_data), "sha256": raw_sha(model_data),
                          "jsonPointers": [ac5_extract["sourceMemberBindings"]["spellModel"]["sourceJsonPointer"],
                                           "/profiles/AC5-PROFILE-FACTION-CHAMPION-01", "/sharedRules/AC5-CHAMPION-ALLY-01"]},
                         {"path": "candidate/CASEBOOK.json", "bytes": len(casebook_data), "sha256": raw_sha(casebook_data),
                          "jsonPointers": [f"/cases/{case_index}"], "caseId": "CJ5-07-B"},
                     ], "use": "accepted finite summon route/profile and same-profile borrowed lantern expiry evidence only"})

    receipt_data = AC5_RECEIPT.read_bytes()
    binding = add_source_copy(PACKET / "authority" / "AC5_EXACT_ACCEPTANCE_05_RECEIPT.json", receipt_data)
    bindings.append({"repositoryPath": "docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json",
                     "packetMember": binding["member"], **binding, "jsonPointers": ["/acceptedSpellIds", "/reviewedArchive", "/runtimeSelectionEnabled"]})

    equip_catalog_data = git_bytes(SOURCE_COMMIT, "DescentReviewChanges/ReviewBible/data/playtest/equipment_source_catalog.json")
    binding = add_source_copy(source_root / "EQUIPMENT_SOURCE_CATALOG.json", equip_catalog_data)
    equip_catalog = read_json_bytes(equip_catalog_data)
    lantern_index = next(i for i, row in enumerate(equip_catalog["records"]) if row.get("id") == "adventuring-gear.lantern-hooded")
    lantern_row = equip_catalog["records"][lantern_index]
    assert lantern_row["sourcePriceCp"] == 500 and lantern_row["sourceWeightLb"] == 2.0
    bindings.append({"repositoryPath": "DescentReviewChanges/ReviewBible/data/playtest/equipment_source_catalog.json",
                     "packetMember": binding["member"], "sourceCommit": SOURCE_COMMIT, **binding,
                     "jsonPointers": [f"/records/{lantern_index}"], "recordId": "adventuring-gear.lantern-hooded",
                     "projectionStatus": lantern_row["status"]})

    rulebook_data = git_bytes(SOURCE_COMMIT, "docs/reference/Player_Rulebook_v6_source_text.txt")
    binding = add_source_copy(source_root / "PLAYER_RULEBOOK_V6_SOURCE.txt", rulebook_data)
    source_lines = rulebook_data.decode("utf-8").splitlines()
    if "Lantern, hooded" not in source_lines[6975]:
        raise ValueError("Pinned Player Rulebook line 6976 does not match hooded lantern record")
    write_json(source_root / "HOODED_LANTERN_SOURCE_EXTRACT.json", {
        "id": "W08-HOODED-LANTERN-SOURCE-EXTRACT",
        "source": {"path": "docs/reference/Player_Rulebook_v6_source_text.txt", "sourceCommit": SOURCE_COMMIT,
                   **binding, "lineNumber": 6976, "exactLine": source_lines[6975]},
        "equipmentProjection": {"recordId": lantern_row["id"], "record": lantern_row,
                                "catalogPath": "DescentReviewChanges/ReviewBible/data/playtest/equipment_source_catalog.json",
                                "catalogSha256": raw_sha(equip_catalog_data), "catalogPointer": f"/records/{lantern_index}"},
        "use": "item identity, 5 gp cost and 2 lb source weight only; no lantern lighting, fuel, or other property is tested",
    })
    bindings.append({"repositoryPath": "docs/reference/Player_Rulebook_v6_source_text.txt",
                     "packetMember": binding["member"], "sourceCommit": SOURCE_COMMIT, **binding,
                     "textLine": 6976, "use": "hooded lantern name, price, and weight source text"})

    authority_files = {
        "CURRENT_BANISHMENT_GATE_CATALOG_CARD.json": HERE / "banishment_gate_current_authority_361" / "CURRENT_BANISHMENT_GATE_CATALOG_CARD.json",
        "PG327_W01_DIRECTOR_SEAL_365_REPACK04.json": HERE / "PG327_W01_DIRECTOR_SEAL_365_REPACK04.json",
        "PG327_W01_W08_WITNESS_PLAN_361.json": HERE / "PG327_W01_W08_WITNESS_PLAN_361.json",
        "CURRENT_SPELL_QUEUE_361.json": HERE / "CURRENT_SPELL_QUEUE_361.json",
        "PG327_W03_W06_W07_SOURCE_AUDIT_362.json": HERE / "PG327_W03_W06_W07_SOURCE_AUDIT_362.json",
    }
    for name, src in authority_files.items():
        data = src.read_bytes()
        binding = add_source_copy(PACKET / "authority" / name, data)
        bindings.append({"repositoryPath": str(src.relative_to(REPO)).replace("\\", "/"), **binding})

    clarif = {
        "id": "PG327-W08-TERMINAL-SETTLEMENT-CLARIFICATION-365",
        "status": "DIRECTOR_GUIDANCE; NOT A SEALED W08 DECISION",
        "sourceChat": "Review Time Stop Witness Evidence",
        "gateSourceBinding": {
            "packetMember": "sources/RETURN327_banishment-gate.json",
            "repositoryPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_return327_received/evidence/packet327/prior/procedures/banishment-gate.json",
            "sourceCommit": SOURCE_COMMIT, "bytes": 34990,
            "sha256": "39c216e978e1c06da3dbea7fb27a60f8611ce08b36143c403fbca989f155fb00",
            "adoptionPointer": "/procedure", "extensionPointer": "/sharedContract/cellExtension",
            "terminalSettlementPointer": "/sharedContract/cellExtension/closure",
        },
        "operativeClosureFields": ["originPlane", "looseObjectAnchors", "mandatoryPlaneReturn", "endpointBlockerException", "objects", "deathAndRemoval", "cellEnd"],
        "equipmentSourceBinding": {"repositoryPath": "DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md",
                                   "packetMember": "rules/BODY_EQUIPMENT.md", "sha256": "d93f9cb0ec8a8398560511f23029d38d9b9a8b901e816373579c8f72b0bec1f3",
                                   "lines": {"items": [50, 51], "creaturePlacement": [57, 61]}},
        "requiredForkOutcomes": {
            "legalAnchor": "place the same genuine item at its projected anchor once",
            "occupiedAnchorAdjacentAvailable": "place at the unambiguous nearest legal adjacent item position without passing a wall or displacing an occupant",
            "anchorAndAdjacentUnavailable": "same item returns to origin plane with pending placement and preserved projected anchor; destroy cell immediately; do not apply creature placement-conflict benefits to cargo",
        },
        "clockBoundary": "source expiry removes body/intrinsic gear and releases genuine cargo; Gate cell remains until its independent admission+60-second deadline. No AC5 immediate primary-expiry closure is imported.",
        "endpointBlocker": "not present in this fixture; no magical source invoked",
        "verbatimDirective": "Use one demonstrated lawful cargo-bearing primary admission as common prefix. Preserve W01/Queue/HOLD; do not import AC5-BANISH-EXT or AC5-X17 mechanics into Gate.",
    }
    clarification_path = PACKET / "authority" / "PG327_W08_TERMINAL_SETTLEMENT_SOURCE_CLARIFICATION_365.json"
    write_json(clarification_path, clarif)
    clarification_binding = file_binding(clarification_path)
    bindings.append({"repositoryPath": "GPT Director guidance received 2026-10-31",
                     "packetMember": "authority/PG327_W08_TERMINAL_SETTLEMENT_SOURCE_CLARIFICATION_365.json",
                     **clarification_binding})

    source_bindings = {
        "id": "PG327-W08-SOURCE-BINDINGS-365-01",
        "sourceCommit": SOURCE_COMMIT,
        "bindings": bindings,
        "nonUseDeclaration": [
            "The Banishment Gate witness uses only PG200-CELL-EXT as expressly adopted by PG9-Q17 and the embedded closure fields.",
            "AC5-BANISH-EXT-01 and AC5-X17 are not used as Gate rules, clocks, admission mechanics, or closure mechanics.",
            "AC5 contributes only the accepted Faction Champion's finite source, intrinsic manifestation, source deadline, and genuine borrowed-object persistence.",
            "The spell catalog remains blocked for runtime selection; this packet is static authored-review evidence only.",
        ],
    }
    write_json(PACKET / "W08_SOURCE_BINDINGS_365.json", source_bindings)

    common_state, common_events, common = build_common_prefix()
    branches = build_branches(common_state)
    case = {
        "id": "PG327-W08-365-FINITE-SUMMON-CARGO",
        "status": "TEST_ONLY_AUTHORED_WITNESS_SUBMITTED_FOR_DIRECTOR_REVIEW",
        "spellId": "banishment-gate",
        "blockerId": "PG200-B04",
        "witnessId": "W08",
        "sourceCommit": SOURCE_COMMIT,
        "notCampaign": True,
        "wholeIdentityGate": "HOLD",
        "applicationAuthorized": False,
        "acceptanceDecision": "not yet requested; Director review pending",
        "selectedGateType": "Humanoid",
        "admissionSource": "the separately cast gate-w08-humanoid-01; not W01's Elemental-fixed Gate instance",
        "scenarioBoundary": {
            "noCampaignEvent": True,
            "allActorFactionAndWorldFactsAreConditionalTestPremises": True,
            "nativeRuntimeSelectionEnabled": False,
            "spellImplementationOrRuntimeTestClaimed": False,
            "identityAcceptanceOrApplicationClaimed": False,
            "noAC5BanishElementalMechanicImported": True,
            "noAC5X17MechanicImported": True,
        },
        "sourceUse": {
            "acceptedFiniteSummonSpellId": "faction-champion",
            "profileId": "AC5-PROFILE-FACTION-CHAMPION-01",
            "profileType": "Humanoid",
            "spellAccess": "Mage rank5, minimum level9, base10 RP",
            "eligibility": {"alliedStatus": True, "currentStanding": 5, "invocationPermission": True, "aidProhibition": False},
            "originalSourceDeadlineSeconds": 60,
            "originalSourceExpiry": "body and intrinsic armor/weapon/shield manifestation end without corpse; genuine separately supplied lantern persists",
        },
        "cargoRecord": {
            "itemId": "object-genuine-hooded-lantern-w08-001",
            "sourceItemId": "adventuring-gear.lantern-hooded",
            "identity": "Lantern, hooded",
            "ownerId": "actor-champion-owner-w08",
            "custodianBeforeAdmission": "summoned-faction-champion-w08",
            "quantity": 1,
            "sourceCostGp": 5,
            "sourceWeightLb": 2,
            "derivedProvisionalLoad": 0.2,
            "carrierCapacity": {"profileSize": "Medium", "strength": 18, "physicalCapacityLb": 270, "inventoryLoadCapacity": 18,
                                 "source": "exact pinned BODY_EQUIPMENT lines 94-103"},
            "carriedBy": "explicitly occupied left hand in conditional body fixture; body has a 5x5-ft footprint and 6-ft occupied height for portal fit only",
            "ownershipChanges": 0,
            "sourceCreatesItem": False,
        },
        "timeModel": {
            "unit": "absolute elapsed seconds in one TEST_ONLY scenario",
            "gateConcentration": {"begins": -5, "deadline": 595, "activeAtCellClosure": True},
            "summonConcentration": {"begins": 0, "originalDeadline": 60, "endsAtOriginalDeadline": True},
            "admission": {"at": 6, "cellDeadline": 66, "rule": "independent admission + 60 seconds"},
            "sourceExpiryBeforeCellDeadline": True,
            "sourceExpiryDoesNotCloseGateCell": True,
        },
        "commonPrefix": common,
        "terminalForks": branches,
        "closureInvariants": [
            "all branches share the same complete acquisition, legal creation, pre-admission cargo custody, matching complete-body crossing, and source-expiry history",
            "mandatory body/source expiry resolves at t=60; no corpse and no intrinsic gear item is created",
            "only the genuine lantern survives in the Gate cell; at t=66 Gate closure returns the same item exactly once",
            "the Gate remains active and its 600-second concentration continues after the one cell is destroyed",
            "Gate and summon RP remain spent; no refund, refill, new summon, second ending, duplicate item, or body recreation",
            "the blocked-placement branch uses pending item placement only; no creature placementConflict state or benefits are granted to cargo",
            "no magical endpoint blocker is present; physical occupancy/blocking is separately represented",
        ],
    }
    write_json(PACKET / "W08_FINITE_SUMMON_CARGO_CASE_365_TESTONLY.json", case)

    coverage = {
        "id": "PG327-W08-COVERAGE-365-01",
        "witnessId": "W08",
        "coverage": {
            "acceptedFiniteSummonSourceAndRoute": True,
            "factionEligibility": True,
            "originalSourceDeadline": True,
            "independentlyAcquiredGenuineCargoBeforeAdmission": True,
            "ownerCustodianPhysicalIdentity": True,
            "matchingTypeGateAdmission": True,
            "sourceBodyAndIntrinsicGearEndWithoutCorpse": True,
            "independentGateCellDeadlineContinues": True,
            "legalProjectedAnchorPlacement": True,
            "occupiedAnchorNearestAdjacentPlacement": True,
            "fullyBlockedPendingItemPlacementAndCellDestruction": True,
            "noDuplicationRecreationSecondEndingOrRefund": True,
            "completeForwardAndInverseReplay": True,
        },
        "notClaimed": ["campaign occurrence", "native runtime selection", "runtime implementation", "human playtest", "whole-identity acceptance", "application authorization"],
    }
    write_json(PACKET / "W08_CASE_COVERAGE_365.json", coverage)

    build_report = {
        "id": "PG327-W08-BUILD-VALIDATION-365-01",
        "builtAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PREPARED_FOR_INDEPENDENT_VALIDATION",
        "commonPrefixEventCount": len(common_events),
        "terminalForkCount": len(branches),
        "branchEventCounts": {b["branchId"]: len(b["events"]) for b in branches},
        "allCommonEventsHaveInverse": all(bool(e["inverseOperations"]) for e in common_events),
        "allBranchesRestoreCommonPrefix": all(b["restoresCommonPrefix"] for b in branches),
        "queueBeforeAndAfter": {"applied": 828, "pending": 20, "acceptedUnapplied": 0, "completeStandaloneProcedures": 552,
                                "scopedInterfaces": 173, "firstReviews": 0, "closureTasks": 20},
        "identityDecision": "HOLD",
        "applicationAuthorized": False,
    }
    write_json(PACKET / "W08_BUILD_VALIDATION_365.json", build_report)

    # Source manifest is regenerated after the independent audit is added.
    print(json.dumps({"packetRoot": str(PACKET), "sourceBindingCount": len(bindings),
                      "commonPrefixEvents": len(common_events), "forks": len(branches),
                      "sourceCasebookIndex": case_index, "equipmentRecordIndex": lantern_index}, indent=2))


if __name__ == "__main__":
    main()
