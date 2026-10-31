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
OUT = HERE / "banishment_gate_witness365_w08_finite_cargo03_build03"
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
            assert get_at(result, path) == op["before"], f"replace mismatch at {path}: {get_at(result, path)!r} != {op['before']!r}"
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
                                         "sources/COMBAT_ACTION_PLAYTEST.md#lines-31-32"])

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


def _blocker(blocker_id: str, kind: str, minimum: list[float], maximum: list[float]) -> dict[str, Any]:
    return {"id": blocker_id, "kind": kind, "aabbFt": {"min": minimum, "max": maximum},
            "stationary": True, "movableByResolution": False, "fixtureStatus": "TEST_ONLY physical geometry"}


def _terminal_geometry(branch_id: str) -> dict[str, Any]:
    anchor = [107, 100, 0.25]
    floor = {"planeZFt": 0, "boundsFt": {"min": [104, 97, 0], "max": [112, 103, 0]},
             "continuousSupport": True}
    model = {"itemId": ITEM_ID, "itemAabbSizeFt": [0.5, 0.5, 0.5], "orientationFixed": True,
             "boundaryTouchingIsNonOverlap": True, "requiresGroundSupport": True,
             "centerCoordinatesContinuous": True, "allGeometryIsTEST_ONLY": True}
    if branch_id == "W08-DIRECT-ANCHOR-PLACEMENT":
        return {"fixtureId": branch_id, "evidenceClass": "TEST_ONLY authored physical geometry",
                "projectedItemAnchorFt": anchor, "itemPlacementModel": model, "floorSupport": floor,
                "blockers": [], "adjacentBay": None,
                "derivedDecision": {"anchorAabbClear": True, "anchorSupported": True,
                                    "nearestLegalCandidateFt": anchor, "unique": True}}
    if branch_id == "W08-OCCUPIED-ANCHOR-ADJACENT-DROP":
        blockers = [
            _blocker("fixture-occupant-adjacent-01", "stationary occupied 0.5x0.5x6ft body",
                     [106.75, 99.75, 0], [107.25, 100.25, 6]),
            _blocker("barrier-west-01", "solid barrier", [106, 99.75, 0], [106.75, 100.25, 6]),
            _blocker("barrier-north-01", "solid barrier", [106, 100.25, 0], [112, 101, 6]),
            _blocker("barrier-south-01", "solid barrier", [106, 99, 0], [112, 99.75, 6]),
        ]
        return {"fixtureId": branch_id, "evidenceClass": "TEST_ONLY authored physical geometry",
                "projectedItemAnchorFt": anchor, "itemPlacementModel": model, "floorSupport": floor,
                "blockers": blockers,
                "adjacentBay": {"kind": "continuous one-way floor corridor", "centerYFt": 100,
                                "centerZFt": 0.25, "minimumLegalCenterXFt": 107.5,
                                "derivedFrom": ["anchor occupant east face at x=107.25", "item half-width 0.25ft",
                                                "north/south barriers constrain centerY to 100ft"]},
                "derivedDecision": {"anchorAabbClear": False, "anchorBlockerIds": ["fixture-occupant-adjacent-01"],
                                    "nearestLegalCandidateFt": [107.5, 100, 0.25],
                                    "nearestDistanceFt": 0.5, "unique": True,
                                    "continuousNearestSet": {"x": [107.5, 107.5], "y": [100, 100], "z": [0.25, 0.25]},
                                    "placementPathCrossesWall": False, "wouldDisplaceBlocker": False}}
    if branch_id == "W08-OCCUPIED-AND-BLOCKED-PENDING-ITEM":
        blockers = [_blocker("fixture-occupant-pending-01", "stationary occupied anchor body",
                             [106.5, 99.5, 0], [107.5, 100.5, 6])]
        xs = [105.5, 106.5, 107.5, 108.5]
        ys = [98.5, 99.5, 100.5, 101.5]
        for yi in range(3):
            for xi in range(3):
                if xi == 1 and yi == 1:
                    continue
                blockers.append(_blocker(f"sealed-bay-blocker-{xi}-{yi}", "contiguous solid full-height barrier",
                                         [xs[xi], ys[yi], 0], [xs[xi + 1], ys[yi + 1], 6]))
        return {"fixtureId": branch_id, "evidenceClass": "TEST_ONLY authored physical geometry",
                "projectedItemAnchorFt": anchor, "itemPlacementModel": model, "floorSupport": floor,
                "blockers": blockers,
                "adjacentBay": {"kind": "sealed 3x3-foot floor bay", "centerBoundsFt": {"min": [106, 99, 0.25],
                                                                                       "max": [108, 101, 0.25]},
                                "solidRegionBoundsFt": {"min": [105.5, 98.5, 0], "max": [108.5, 101.5, 6]},
                                "adjacentPlacementCenterRadiusFt": 1,
                                "barriersTileEveryNeighborVolume": True,
                                "outsideBaySeparatedByContinuousWalls": True,
                                "noLegalVerticalShelfWithinAdjacentRadius": True},
                "derivedDecision": {"anchorAabbClear": False,
                                    "anchorBlockerIds": ["fixture-occupant-pending-01"],
                                    "adjacentDomainFullyOccupied": True,
                                    "adjacentLegalCandidateCount": 0,
                                    "displacedBlockerIds": [], "placementPathCrossesWall": False}}
    raise ValueError(branch_id)


def build_branches(common_state: dict[str, Any]) -> list[dict[str, Any]]:
    base_hash = state_hash(common_state)
    specs = [
        ("W08-DIRECT-ANCHOR-PLACEMENT", "placed-at-origin-anchor"),
        ("W08-OCCUPIED-ANCHOR-ADJACENT-DROP", "placed-at-nearest-legal-adjacent-position"),
        ("W08-OCCUPIED-AND-BLOCKED-PENDING-ITEM", "pending-origin-plane-item-placement"),
    ]
    results: list[dict[str, Any]] = []
    closure_pointers = [
        "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/originPlane",
        "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/looseObjectAnchors",
        "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/mandatoryPlaneReturn",
        "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/objects",
        "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/deathAndRemoval",
        "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/cellEnd",
        "rules/BODY_EQUIPMENT.md#lines-50-51",
    ]
    for branch_id, expected in specs:
        state = copy.deepcopy(common_state)
        events: list[dict[str, Any]] = []
        order_by_time: dict[int, int] = {}

        def emit(event_id: str, kind: str, description: str, mutate: Callable[[dict[str, Any]], None],
                 sources: list[str], labels: list[str] | None = None,
                 marker: dict[str, Any] | None = None) -> None:
            def wrapped(s: dict[str, Any]) -> None:
                s["elapsedSeconds"] = 66
                mutate(s)
            updated = record_event(events, state, event_id, 66, kind, description, wrapped, sources)
            state.clear()
            state.update(updated)
            order_by_time[66] = order_by_time.get(66, 0) + 1
            events[-1]["sequenceAtTimestamp"] = order_by_time[66]
            events[-1]["sourceParagraphLabels"] = list(labels or [])
            if marker is not None:
                events[-1]["regularTurnMarker"] = copy.deepcopy(marker)

        def set_geometry(s: dict[str, Any]) -> None:
            fixture = _terminal_geometry(branch_id)
            s["world"]["terminalGeometryFixture"] = fixture
            s["eventReceipts"][f"{branch_id}-GEOMETRY"] = {
                "branchId": branch_id, "capturedAtSeconds": 66,
                "projectedItemAnchorFt": [107, 100, 0.25], "geometryFixtureId": fixture["fixtureId"],
                "blockerIds": [b["id"] for b in fixture["blockers"]], "fixtureOnly": True}
        emit(f"{branch_id}-GEOMETRY", "terminal-placement-geometry",
             "Bind concrete TEST_ONLY floor support, item volume, stationary occupied bodies, barriers and continuous placement domains before closure; geometry is independent of spell identity.",
             set_geometry, ["sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/looseObjectAnchors",
                            "rules/BODY_EQUIPMENT.md#lines-50-51"], labels=["PG9-Q29"])

        def close_cell(s: dict[str, Any]) -> None:
            cell = s["cell"]
            item = s["objects"][ITEM_ID]
            fixture = s["world"]["terminalGeometryFixture"]
            origin_anchor = cell["originAnchor"]["worldFt"]
            local = [2, 0, 0.25]
            projected = [origin_anchor[0] + local[0], origin_anchor[1] + local[1], origin_anchor[2] + local[2]]
            size = fixture["itemPlacementModel"]["itemAabbSizeFt"]

            def aabb(center: list[float]) -> dict[str, list[float]]:
                return {"min": [center[i] - size[i] / 2 for i in range(3)],
                        "max": [center[i] + size[i] / 2 for i in range(3)]}

            def overlaps(a: dict[str, list[float]], b: dict[str, list[float]]) -> bool:
                return all(a["min"][i] < b["max"][i] and b["min"][i] < a["max"][i] for i in range(3))

            anchor_box = aabb(projected)
            anchor_blockers = [b["id"] for b in fixture["blockers"] if overlaps(anchor_box, b["aabbFt"])]
            result: dict[str, Any] = {"projectedAnchorFt": projected, "anchorItemAabbFt": anchor_box,
                                      "anchorBlockerIds": anchor_blockers, "supportPlaneZFt": 0,
                                      "objectSizeFt": size, "boundaryTouchingIsNonOverlap": True}
            if branch_id == "W08-DIRECT-ANCHOR-PLACEMENT":
                assert not anchor_blockers
                placed = projected
                result.update({"placement": "anchor", "candidateFt": placed, "candidateLegal": True,
                               "supportLegal": True, "uniqueNearest": True})
                item_status = "placed-at-origin-anchor"
            elif branch_id == "W08-OCCUPIED-ANCHOR-ADJACENT-DROP":
                assert anchor_blockers == ["fixture-occupant-adjacent-01"]
                placed = [107.5, 100, 0.25]
                placed_box = aabb(placed)
                candidate_blockers = [b["id"] for b in fixture["blockers"] if overlaps(placed_box, b["aabbFt"])]
                assert not candidate_blockers
                assert fixture["adjacentBay"]["centerYFt"] == placed[1]
                assert fixture["adjacentBay"]["minimumLegalCenterXFt"] == placed[0]
                result.update({"placement": "nearest-adjacent", "candidateFt": placed,
                               "candidateAabbFt": placed_box, "candidateBlockerIds": candidate_blockers,
                               "centerDistanceFt": 0.5, "continuousNearestSetCardinality": 1,
                               "uniqueNearest": True, "supportLegal": True,
                               "noOccupantDisplaced": True, "wallIntersectionCount": 0})
                item_status = "placed-at-nearest-legal-adjacent-position"
            else:
                assert anchor_blockers == ["fixture-occupant-pending-01"]
                assert fixture["adjacentBay"]["barriersTileEveryNeighborVolume"] is True
                assert fixture["adjacentBay"]["outsideBaySeparatedByContinuousWalls"] is True
                placed = None
                result.update({"placement": "pending", "candidateFt": None,
                               "adjacentDomainFullyOccupied": True, "adjacentLegalCandidateCount": 0,
                               "noOccupantDisplaced": True, "wallIntersectionCount": 0})
                item_status = "pending-origin-plane-item-placement"

            cell["closureTrigger"] = "independent Gate admission-plus-60-second cell deadline"
            cell["closureStartedAtSeconds"] = 66
            cell["mandatoryPlaneReturn"] = {"completed": True, "toPlaneKey": ORIGIN,
                                             "endpointBlockerPresent": False, "endpointBlockerExceptionUsed": False,
                                             "itemReturnedBeforePlacement": True, "sameObjectId": ITEM_ID}
            cell["projectedItemAnchor"] = {"planeKey": ORIGIN, "worldFt": projected,
                                           "projectedFromCellLocalFt": local,
                                           "fixedOriginAnchorFt": origin_anchor,
                                           "anchorSnapshotUnchanged": True}
            cell["physicalPlacementOutcome"] = item_status
            item["status"] = item_status
            item["custodianId"] = None
            if placed is not None:
                item["physicalPosition"] = {"planeKey": ORIGIN, "worldFt": placed,
                                            "custodianId": None, "placementPending": False,
                                            "projectedAnchorWorldFt": projected,
                                            "placementSearchIsNotPhysicalMovement": True,
                                            "displacedOccupant": False, "wallPassage": False}
            else:
                item["physicalPosition"] = {"planeKey": ORIGIN, "worldFt": None,
                                            "pendingAnchorWorldFt": projected, "custodianId": None,
                                            "placementPending": True, "creaturePlacementConflict": False,
                                            "sameObjectIdPreserved": True}
            cell["geometry"]["lastCargoEnvelopeBeforeClosureAabbFt"] = copy.deepcopy(
                cell["geometry"].get("currentCargoEnvelopeAabbFt"))
            cell["geometry"]["cargoEnvelopeAabbFt"] = None
            cell["geometry"]["currentCargoEnvelopeAabbFt"] = None
            cell["geometry"]["cargoGeometryStage"] = "cell-destroyed; cargo returned to origin plane"
            cell.update({"status": "closed", "destroyed": True, "closedAtSeconds": 66,
                         "closureCount": cell["closureCount"] + 1, "contents": [], "looseCargoIds": [],
                         "closureReceiptId": f"receipt-{branch_id}-CLOSE-01"})
            s["gate"]["liveCellIds"].remove(CELL_ID)
            blockers_after = copy.deepcopy(fixture["blockers"])
            s["eventReceipts"][f"{branch_id}-CLOSE"] = {
                "receiptId": cell["closureReceiptId"], "cellDestroyed": True, "closureCount": 1,
                "cargoId": ITEM_ID, "cargoQuantity": item["quantity"], "cargoStatus": item_status,
                "projectedAnchorWorldFt": projected, "placementEvidence": result,
                "pendingCargoKeepsCellAlive": False, "bodyRecreated": False, "secondEnding": False,
                "refundRp": 0, "blockersUnchanged": blockers_after == fixture["blockers"],
                "displacedOccupant": False, "wallPassage": False,
            }
        emit(f"{branch_id}-CLOSE", "gate-cell-terminal-closure",
             "At the independent 66-second cell deadline, project the same loose lantern's current cell-local position onto the fixed admission anchor, return it to the origin plane before placement, resolve actual geometry, then destroy the cell even if placement remains pending.",
             close_cell, closure_pointers, labels=["PG9-Q15", "PG9-Q17", "PG9-Q29"])

        # The cell deadline is processed before any regular turn beginning at
        # the same timestamp. These are real state transitions in the replay.
        for actor_key in ("gateCaster", "championOwner"):
            actor_id = GATE_CASTER_ID if actor_key == "gateCaster" else OWNER_ID
            actor = state["actors"][actor_key]
            turn_id = f"{actor_id}-turn-{actor['turnState']['turnNumber'] + 1}"
            def start_turn(s: dict[str, Any], key: str = actor_key, tid: str = turn_id) -> None:
                a = s["actors"][key]
                ts = a["turnState"]
                assert ts["active"] is False
                combat = a["combatState"]
                previous_stance = combat.get("activeStance")
                if previous_stance is not None:
                    previous_stance["expiredAtSeconds"] = 66
                    previous_stance["expiryReason"] = "next regular own-turn start"
                    if combat["stanceHistory"]:
                        combat["stanceHistory"][-1]["expiredAtSeconds"] = 66
                        combat["stanceHistory"][-1]["expiryReason"] = "next regular own-turn start"
                stance = {"name": "Guarded", "selectedAtSeconds": 66,
                          "expiresAtNextRegularStart": True, "expiresAtSeconds": None,
                          "source": "sources/COMBAT_ACTION_PLAYTEST.md#lines-111-115",
                          "effects": {"acBonus": 1, "speedChangeFt": -5,
                                      "explicitShoveResistanceAdvantage": True}}
                combat["stanceHistory"].append(copy.deepcopy(stance))
                combat["activeStance"] = stance
                combat["activeAC"] = combat["baseAC"] + 1
                combat["activeSpeedFt"] = max(0, combat["baseSpeedFt"] - 5)
                stance_receipt = {**copy.deepcopy(stance), "dependentAllowances": {
                    "movementBudgetFt": combat["activeSpeedFt"], "activeAC": combat["activeAC"]}}
                ts["turnNumber"] += 1
                ts["refreshCount"] += 1
                ts.update({"active": True, "actionAvailable": True, "bonusActionAvailable": True,
                           "reactionAvailable": True, "movementBudgetFt": combat["activeSpeedFt"],
                           "movementRemainingFt": combat["activeSpeedFt"],
                           "stanceSelection": copy.deepcopy(stance_receipt),
                           "companionCommandAllowanceAvailable": key == "championOwner",
                           "spellcastsThisTurn": 0, "weaveAbilitiesThisTurn": 0, "expiredAllowances": []})
                if key == "championOwner":
                    a["companionCommandUse"] = None
                s["turnScheduleLog"].append({"actorId": a["id"], "actorKey": key,
                                             "turnNumber": ts["turnNumber"], "roundBoundarySeconds": 66,
                                             "marker": "START", "onceOnlyRefresh": True,
                                             "stanceSelection": copy.deepcopy(stance_receipt)})
                s["eventReceipts"][f"TURN-START-{key}-66"] = {
                    "actorId": a["id"], "refreshedOnce": True, "movementFt": combat["activeSpeedFt"],
                    "stanceSelection": copy.deepcopy(stance_receipt),
                    "expiredPriorStance": copy.deepcopy(previous_stance)}
            marker = {"actorKey": actor_key, "actorId": actor_id, "roundBoundarySeconds": 66,
                      "turnId": turn_id, "marker": "START", "onceOnlyRefresh": True,
                      "mandatoryCellClosurePrecedesStart": True}
            emit(f"{branch_id}-TURN-{actor_key}-START-T66", "regular-turn-start",
                 f"{actor_key} receives its once-only regular-turn refresh after the 66-second mandatory cell closure.",
                 start_turn, ["sources/MAGE_CLASS_PLAYTEST.json#/engine/8",
                              "sources/COMBAT_ACTION_PLAYTEST.md#lines-60-62",
                              "sources/COMBAT_ACTION_PLAYTEST.md#lines-111-115"], marker=marker)

            def end_turn(s: dict[str, Any], key: str = actor_key) -> None:
                a = s["actors"][key]
                ts = a["turnState"]
                assert ts["active"] is True
                before_dissonance = a["magicState"]["dissonance"]
                no_magic = ts["spellcastsThisTurn"] == 0 and ts["weaveAbilitiesThisTurn"] == 0
                if no_magic:
                    a["magicState"]["dissonance"] = max(0, before_dissonance - 1)
                unused = {"action": ts["actionAvailable"], "bonusAction": ts["bonusActionAvailable"],
                          "movementFt": ts["movementRemainingFt"],
                          "companionCommand": ts["companionCommandAllowanceAvailable"]}
                ts["expiredAllowances"].append({"roundBoundarySeconds": 66, "unused": copy.deepcopy(unused)})
                ts.update({"active": False, "actionAvailable": False, "bonusActionAvailable": False,
                           "movementRemainingFt": 0, "companionCommandAllowanceAvailable": False})
                s["turnScheduleLog"].append({"actorId": a["id"], "actorKey": key,
                                             "turnNumber": ts["turnNumber"], "roundBoundarySeconds": 66,
                                             "marker": "END", "noSpellOrWeave": no_magic,
                                             "dissonanceBefore": before_dissonance,
                                             "dissonanceAfter": a["magicState"]["dissonance"],
                                             "stanceContinuesUntilNextRegularStart": copy.deepcopy(a["combatState"]["activeStance"]),
                                             "unusedAllowancesExpired": copy.deepcopy(unused)})
            marker_end = {"actorKey": actor_key, "actorId": actor_id, "roundBoundarySeconds": 66,
                          "turnId": turn_id, "marker": "END", "onceOnlyRefresh": False,
                          "unusedAllowancesExpire": True}
            emit(f"{branch_id}-TURN-{actor_key}-END-T66", "regular-turn-end",
                 f"{actor_key}'s 66-second regular turn ends; unused action, bonus action, movement and command allowances expire.",
                 end_turn, ["sources/MAGE_CLASS_PLAYTEST.json#/engine/8",
                            "sources/COMBAT_ACTION_PLAYTEST.md#lines-60-62",
                            "sources/COMBAT_ACTION_PLAYTEST.md#lines-111-115"], marker=marker_end)

        close_event = next(e for e in events if e["kind"] == "gate-cell-terminal-closure")
        before_duplicate_hash = state_hash(state)
        duplicate_receipt = state["eventReceipts"][f"{branch_id}-CLOSE"]
        duplicate = {
            "eventId": f"{branch_id}-DUPLICATE-CLOSE-DELIVERY", "timestampSeconds": 66,
            "sequenceAtTimestamp": order_by_time[66] + 1, "kind": "duplicate-terminal-callback",
            "description": "A repeated delivery of the same terminal closure key returns its existing receipt and changes no state.",
            "sourcePointers": ["sources/RETURN327_banishment-gate.json#/procedure"],
            "sourceParagraphLabels": ["PG9-Q29"], "beforeStateSha256": before_duplicate_hash,
            "afterStateSha256": before_duplicate_hash, "forwardOperations": [], "inverseOperations": [],
            "stateAfter": copy.deepcopy(state), "duplicateClosureKey": f"{branch_id}-CLOSE",
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
            "branchId": branch_id, "startStateSha256": base_hash,
            "terminalStateSha256": state_hash(state), "expectedOutcome": expected,
            "events": events, "finalState": state,
            "reverseOrder": [e["eventId"] for e in reversed(events)],
            "reverseChecks": reverse_checks, "restoresCommonPrefix": state_hash(reverse) == base_hash,
        })
    return results


def _director_hold_repack01() -> dict[str, Any]:
    return {
        "rulingId": "PG327-W08-365-DIRECTOR-HOLD",
        "sourceChat": "Review Time Stop Witness Evidence",
        "sourceSurface": "GPT browser review response, read 2026-10-31",
        "witnessId": "W08", "witnessDisposition": "HOLD",
        "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate"],
        "blockerIds": ["PG200-B03", "PG200-B04"],
        "closedBlockerIds": [], "closedResidualIds": [],
        "remainingResidualIds": [f"W08-365-R{i}" for i in range(1, 8)],
        "applicationAuthorized": False,
        "queueAuthority": {"applied": 828, "pending": 20, "acceptedUnapplied": 0,
                           "completeStandaloneProcedures": 552, "scopedInterfaces": 173,
                           "firstReviews": 0, "closureTasks": 20},
        "priorArchive": {"name": "DD_Rank9_BanishmentGate_W08_FiniteCargo_365_TESTONLY.zip",
                         "bytes": 467545,
                         "sha256": "988183e5eaadb73948d4d76c8e4a2324e034b9f7c878f25220b5a9a1a6f94e8c"},
        "integrityFindings": {"uniqueMembers": 22, "payloadHashesAndCrcs": 21,
                              "includedMemberBindings": 14, "forwardEvents": 15,
                              "inverseEvents": 15, "lifecycleReplay": "PASS",
                              "semanticPredicates": "NOT_ESTABLISHED_BY_REPLAY"},
        "residuals": [
            {"id": "W08-365-R1", "title": "Actor/source qualification",
             "defect": "Profiles lacked source-bound legal acquisition/preparation histories, class engine, derived resources, conditions, repertoires and spell histories. RP exceeded Mage maxima (60 vs 50 at level17; 40 vs 26 at level9), and standing 5 exceeded the ordinary -3..+3 range.",
             "required": "Use the exact Mage table and bind full TEST_ONLY caster profiles; Mage17 RP 50->24, Mage9 RP 26->16; use sourced valid standing."},
            {"id": "W08-365-R2", "title": "Actual casting predicates",
             "defect": "Gate/Champion casts lacked V/S/F availability, identified held focus and hand custody, Gate caster position/range/LoE, Champion Action consumption, Conjuration/class history, Dissonance/Refrain, concentration and participant Counterspell eligibility/decision.",
             "required": "Record commitment, windows and resolution, spell components, focus custody, distances, source-bound spell access, class history and every participant's selected Mage Counterspell eligibility/decision."},
            {"id": "W08-365-R3", "title": "Scheduled opportunities and command phase",
             "defect": "Regular starts/ends, once-only refreshes, stance choices, allowance expiry and t66 equal-time ordering were absent; attached movement lacked the owner's whole-turn end and phase start/end; command eligibility was not bound.",
             "required": "Replay all six-second turn markers through t66, command predicates/global allowance, turn/phase order, and expiration of unused movement."},
            {"id": "W08-365-R4", "title": "Cargo custody and occupied geometry",
             "defect": "Hand snapshot contradicted carriedSlot and no numeric cargo envelope/offset, full admission sweep, cell-local map or BAN-CELL-03 dimensions were present.",
             "required": "Bind one consistent hand/custody record, occupied item volume and offset, full body/cargo sweep, cell-local mapping and numeric bounds."},
            {"id": "W08-365-R5", "title": "Wrong fixed origin anchor",
             "defect": "The cell anchor was portal-plane [100,100,0], but the recorded admission endpoint was [105,100,0].",
             "required": "Fix the anchor at the actual admission endpoint and recompute all projections and receipts."},
            {"id": "W08-365-R6", "title": "Placement conclusions lack geometry",
             "defect": "Placement forks used occupancy booleans and grid centers without occupant volumes, barrier/support geometry, lantern fit, displacement or unobstructed-region proof.",
             "required": "Provide continuous TEST_ONLY physical geometry, derive candidate fit/nearest position, and prove no legal adjacent placement in the pending branch without displacement or wall passage."},
            {"id": "W08-365-R7", "title": "Broken locators and overstated coverage",
             "defect": "Some source locators were malformed or pointed to nonexistent records, delivery named a staging manifest path, and coverage blurred replay integrity with unresolved semantics.",
             "required": "Use exact JSON pointers plus separate paragraph labels, actual packet member paths, ARCHIVE_MANIFEST.json delivery path, and retain W08 as outstanding until sealed."},
        ],
        "lifecycleFinding": "The submitted lifecycle ordering correctly removed body/intrinsic gear at t60, retained genuine lantern cargo, kept the cell until t66, destroyed it with pending cargo, and made duplicate closure a no-op. That does not close the seven residuals.",
        "scopeFinding": "No AC5-BANISH-EXT/AC5-X17 mechanics or magical endpoint-blocker exception were exercised. W01 stays sealed; W05 follows W08; W03 stays on its separate source HOLD.",
    }


def _caster_profile_artifact(mage_json: dict[str, Any], mage_sha: str, card_index: int,
                             rulebook_bytes: bytes, ac5_extract: dict[str, Any],
                             gate_card: dict[str, Any], equip_catalog: dict[str, Any]) -> dict[str, Any]:
    lines = rulebook_bytes.decode("utf-8").splitlines()
    def line_containing(text: str) -> int:
        return next(i for i, line in enumerate(lines, 1) if text in line)
    advancement_line = line_containing("The Character Advancement table summarizes")
    dissonance_line = line_containing("Dissonance Limit: 2 + proficiency bonus")
    rank_line = line_containing("Base Dissonance: A Rank 1-5 spell generates 1 Dissonance")
    focus_index = next(i for i, row in enumerate(equip_catalog["records"]) if row.get("id") == "arcane-focuses.wand")
    return {
        "id": "W08-CASTER-PROFILES-365-TESTONLY-REPACK03",
        "evidenceClass": "explicit conditional TEST_ONLY actor profiles; not campaign characters",
        "profileSourceBindings": {
            "mageClass": {"member": "sources/MAGE_CLASS_PLAYTEST.json", "sha256": mage_sha,
                          "enginePointer": "/engine", "rpLevel9Pointer": "/rpByClassLevel/8",
                          "rpLevel17Pointer": "/rpByClassLevel/16", "counterspellPointer": f"/cards/{card_index}"},
            "rulebook": {"member": "sources/PLAYER_RULEBOOK_V6_SOURCE.txt",
                         "proficiencyRuleLine": advancement_line, "dissonanceLimitLine": dissonance_line,
                         "rankDissonanceLine": rank_line},
            "gateAccess": {"member": "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json",
                           "pointer": "/classAccess/Mage", "record": gate_card["classAccess"]["Mage"]},
            "factionChampion": ac5_extract["sourceMemberBindings"]["spellModel"],
            "focusItem": {"member": "sources/EQUIPMENT_SOURCE_CATALOG.json", "pointer": f"/records/{focus_index}",
                          "recordId": "arcane-focuses.wand"},
        },
        "derivedFormulas": {"spellAttack": "normal total-character PB + Intelligence modifier",
                            "spellSaveDC": "8 + normal total-character PB + Intelligence modifier",
                            "MageM": "max(1, Intelligence modifier)",
                            "MageS": "1/2/3/4 at Mage levels 1/5/11/17",
                            "dissonanceLimit": "2 + PB + positive spellcasting ability modifier",
                            "rankDissonance": "rank1-5 +1; rank6-9 +2; immediate repeats add Refrain"},
        "profiles": [
            {
                "profileId": "W08-MAGE17-GATECASTER-TESTONLY", "actorId": GATE_CASTER_ID,
                "class": "Mage", "classLevel": 17, "totalCharacterLevel": 17,
                "classPathHistory": [{"level": 3, "path": "Arcanist"}, {"level": 10, "path": "Archmage"}],
                "abilityScores": {"STR": 10, "DEX": 14, "CON": 14, "INT": 18, "WIS": 12, "CHA": 10},
                "derived": {"PB": 6, "IntModifier": 4, "M": 4, "S": 4, "RPMaximum": mage_json["rpByClassLevel"][16],
                            "spellAttack": 10, "spellSaveDC": 18, "dissonanceLimit": 12},
                "testOnlyVitals": {"hp": 100, "ac": 15, "usedByW08Predicates": False},
                "conditions": [], "conscious": True, "incapacitated": False, "silenced": False,
                "concentrationBeforeGate": None,
                "classCardHistory": [{"cardId": "mage.arch.counterspell", "selectedAtMageLevel": 9,
                                      "selectionMethod": "Mage class-card choice; card minimum level 9",
                                      "selected": True, "sourcePointer": f"/cards/{card_index}"}],
                "spellbookHistory": [
                    {"spellId": "mage.arch.counterspell", "kind": "Mage class card", "acquiredAtMageLevel": 9,
                     "preparedForWitness": True, "sourcePointer": f"/cards/{card_index}"},
                    {"spellId": "banishment-gate", "kind": "ordinary Mage spell", "acquiredAtMageLevel": 17,
                     "preparedForWitness": True, "sourceAccess": gate_card["classAccess"]["Mage"],
                     "acquisitionFact": "explicit TEST_ONLY spellbook history; no automatic Wizard access assumed",
                     "operativeSchool": "Conjuration",
                     "operativeSchoolSource": "sources/RETURN327_banishment-gate.json#/procedure; PG9-Q01",
                     "catalogMetadataConflict": {"catalogSchool": "Abjuration",
                         "catalogMember": "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json",
                         "catalogPreservedUnchanged": True,
                         "ruleForThisWitness": "use pinned Return327 operative Mage Conjuration route"}},
                ],
                "focus": {"objectId": FOCUS_GATE_ID, "recordId": "arcane-focuses.wand", "heldIn": "right hand",
                          "custody": GATE_CASTER_ID, "somaticHand": "left hand", "verbalAvailable": True},
            },
            {
                "profileId": "W08-MAGE9-CHAMPION-OWNER-TESTONLY", "actorId": OWNER_ID,
                "class": "Mage", "classLevel": 9, "totalCharacterLevel": 9,
                "classPathHistory": [{"level": 3, "path": "Arcanist"}],
                "abilityScores": {"STR": 10, "DEX": 14, "CON": 14, "INT": 18, "WIS": 12, "CHA": 10},
                "derived": {"PB": 4, "IntModifier": 4, "M": 4, "S": 2, "RPMaximum": mage_json["rpByClassLevel"][8],
                            "spellAttack": 8, "spellSaveDC": 16, "dissonanceLimit": 10},
                "testOnlyVitals": {"hp": 80, "ac": 15, "usedByW08Predicates": False},
                "conditions": [], "conscious": True, "incapacitated": False, "silenced": False,
                "concentrationBeforeChampion": None,
                "classCardHistory": [{"cardId": "mage.arch.counterspell", "selectedAtMageLevel": 9,
                                      "selectionMethod": "Mage class-card choice; card minimum level 9",
                                      "selected": True, "sourcePointer": f"/cards/{card_index}"}],
                "spellbookHistory": [
                    {"spellId": "mage.arch.counterspell", "kind": "Mage class card", "acquiredAtMageLevel": 9,
                     "preparedForWitness": True, "sourcePointer": f"/cards/{card_index}"},
                    {"spellId": "faction-champion", "kind": "ordinary Mage spell", "acquiredAtMageLevel": 9,
                     "preparedForWitness": True, "sourceAccess": ac5_extract["spellAccessAndRoute"]["completeSourceAndAccess"]["classAccess"]["Mage"],
                     "acquisitionFact": "explicit TEST_ONLY spellbook history; class access and minimum level are source-bound"},
                ],
                "factionEligibility": {"factionId": "FACTION-W08-TEST-A", "alliedStatus": True,
                                       "currentStanding": 3, "invocationPermission": True,
                                       "aidProhibition": False, "membershipInferred": False},
                "focus": {"objectId": FOCUS_OWNER_ID, "recordId": "arcane-focuses.wand", "heldIn": "right hand",
                          "custody": OWNER_ID, "somaticHand": "left hand", "verbalAvailable": True},
            },
        ],
        "scopeNote": "The selected-elemental focus is Fire only as an explicit profile field; neither test spell is elemental, so no Nuke Chain benefit is invoked. No actual HP/AC-derived result is tested.",
    }


def _finalize_repack03() -> None:
    import shutil
    case_path = PACKET / "W08_FINITE_SUMMON_CARGO_CASE_365_TESTONLY.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    bindings_path = PACKET / "W08_SOURCE_BINDINGS_365.json"
    source_bindings = json.loads(bindings_path.read_text(encoding="utf-8"))
    binding_rows = source_bindings["bindings"]

    gate_binding = next(b for b in binding_rows if b.get("packetMember") == "sources/RETURN327_banishment-gate.json")
    gate_binding["jsonPointers"] = ["/procedure", "/sharedContract/terminalScope", "/sharedContract/cellExtension",
                                    "/sharedContract/cellExtension/closure"]
    gate_binding["paragraphLabels"] = ["PG9-Q01", "PG9-Q13", "PG9-Q15", "PG9-Q17", "PG9-Q29"]
    def normalize_locators(event: dict[str, Any]) -> None:
        json_pointers: list[str] = []
        text_locations: list[str] = list(event.get("sourceTextLocations", []))
        for locator in event.get("sourcePointers", []):
            locator = locator.replace("sources/rules/BODY_EQUIPMENT.md", "rules/BODY_EQUIPMENT.md")
            locator = locator.replace("#/procedure#PG9-Q17", "#/procedure")
            locator = locator.replace("#/procedure#PG9-Q15", "#/procedure")
            locator = locator.replace("#/procedure#PG9-Q29", "#/procedure")
            locator = locator.replace("/records/adventuring-gear.lantern-hooded", "/records/169")
            member, _, fragment = locator.partition("#")
            if member.lower().endswith(".json") and fragment.startswith("/"):
                json_pointers.append(locator)
            elif member.lower().endswith((".md", ".txt")):
                text_locations.append(locator)
            else:
                raise ValueError(f"Unclassified source locator in {event['eventId']}: {locator}")
        event["sourcePointers"] = sorted(set(json_pointers))
        event["sourceTextLocations"] = sorted(set(text_locations))

    for event in case["commonPrefix"]["events"]:
        normalize_locators(event)
    for fork in case["terminalForks"]:
        for event in fork["events"]:
            normalize_locators(event)

    mage_data = git_bytes(SOURCE_COMMIT, "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json")
    mage_json = read_json_bytes(mage_data)
    mage_sha = raw_sha(mage_data)
    expected_mage_sha = "c64782e192e2e63e5abed5728f9213c9d4cf956bce1a75da7a156dbfd1141e0b"
    if mage_sha != expected_mage_sha:
        raise ValueError(f"Pinned Mage class bytes changed: {mage_sha}")
    card_index = next(i for i, row in enumerate(mage_json["cards"]) if row.get("id") == "mage.arch.counterspell")
    mage_member = PACKET / "sources" / "MAGE_CLASS_PLAYTEST.json"
    mage_member.write_bytes(mage_data)

    rulebook_data = (PACKET / "sources" / "PLAYER_RULEBOOK_V6_SOURCE.txt").read_bytes()
    ac5_extract = json.loads((PACKET / "sources" / "AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json").read_text(encoding="utf-8"))
    gate_card = json.loads((PACKET / "authority" / "CURRENT_BANISHMENT_GATE_CATALOG_CARD.json").read_text(encoding="utf-8"))
    equip_catalog = json.loads((PACKET / "sources" / "EQUIPMENT_SOURCE_CATALOG.json").read_text(encoding="utf-8"))
    profiles = _caster_profile_artifact(mage_json, mage_sha, card_index, rulebook_data, ac5_extract, gate_card, equip_catalog)
    profiles_path = PACKET / "sources" / "W08_CASTER_PROFILES_365_TESTONLY.json"
    write_json(profiles_path, profiles)
    binding_rows.append({"repositoryPath": "TEST_ONLY authored W08 caster profile artifact",
                         "packetMember": profiles_path.relative_to(PACKET).as_posix(), **file_binding(profiles_path),
                         "evidenceClass": "explicit conditional TEST_ONLY premises; no campaign facts"})
    binding_rows.append({"repositoryPath": "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json",
                         "packetMember": "sources/MAGE_CLASS_PLAYTEST.json", "sourceCommit": SOURCE_COMMIT,
                         **file_binding(mage_member), "jsonPointers": ["/engine", "/rpByClassLevel/8", "/rpByClassLevel/16",
                                                                         f"/cards/{card_index}"],
                         "sourceStatus": mage_json.get("status"),
                         "acceptedAC5SourceHash": expected_mage_sha,
                         "use": "Mage RP table, class engine and selected Counterspell card; TEST_ONLY profiles"})

    previous_dir = HERE / "banishment_gate_witness365_w08_finite_cargo01"
    prior_names = ["DD_Rank9_BanishmentGate_W08_FiniteCargo_365_TESTONLY.zip",
                   "ARCHIVE_DELIVERY_365_W08.json", "INDEPENDENT_AUDIT_365_W08_FINAL.json"]
    prior_root = PACKET / "authority" / "prior" / "W08_REPACK01"
    prior_root.mkdir(parents=True, exist_ok=True)
    for name in prior_names:
        src = previous_dir / name
        dest = prior_root / name
        shutil.copyfile(src, dest)
        binding_rows.append({"repositoryPath": str(src.relative_to(REPO)).replace("\\", "/"),
                             "packetMember": dest.relative_to(PACKET).as_posix(), **file_binding(dest),
                             "preservationRole": "prior Director-reviewed W08 evidence; immutable history"})

    previous02_dir = HERE / "banishment_gate_witness365_w08_finite_cargo02_final03"
    prior02_names = ["DD_Rank9_BanishmentGate_W08_FiniteCargo_365_TESTONLY_REPACK02.zip",
                     "ARCHIVE_DELIVERY_365_W08_REPACK02.json",
                     "INDEPENDENT_AUDIT_365_W08_REPACK02_ARCHIVE.json"]
    prior02_root = PACKET / "authority" / "prior" / "W08_REPACK02"
    prior02_root.mkdir(parents=True, exist_ok=True)
    for name in prior02_names:
        src = previous02_dir / name
        dest = prior02_root / name
        shutil.copyfile(src, dest)
        binding_rows.append({"repositoryPath": str(src.relative_to(REPO)).replace("\\", "/"),
                             "packetMember": dest.relative_to(PACKET).as_posix(), **file_binding(dest),
                             "preservationRole": "prior Director-adjudicated W08 REPACK02 evidence; immutable history"})

    ruling = _director_hold_repack01()
    ruling_path = PACKET / "authority" / "PG327_W08_DIRECTOR_HOLD_365_REPACK01.json"
    write_json(ruling_path, ruling)
    binding_rows.append({"repositoryPath": "GPT browser ruling transcribed from Review Time Stop Witness Evidence",
                         "packetMember": ruling_path.relative_to(PACKET).as_posix(), **file_binding(ruling_path),
                         "evidenceClass": "prior Director ruling; not a seal or acceptance"})

    ruling02 = {
        "rulingId": "PG327-W08-365-REPACK02-DIRECTOR-HOLD", "witnessId": "W08",
        "witnessDisposition": "HOLD", "acceptedIds": [], "appliedIds": [],
        "heldIds": ["banishment-gate"], "blockerIds": ["PG200-B03", "PG200-B04"],
        "closedBlockerIds": [], "closedResidualIds": ["W08-365-R1", "W08-365-R5", "W08-365-R6"],
        "remainingResidualIds": ["W08-365-R2", "W08-365-R3", "W08-365-R4", "W08-365-R7", "W08-365-R8"],
        "applicationAuthorized": False,
        "source": "GPT browser response in Review Time Stop Witness Evidence, 2026-10-31; transcribed verbatim in disposition fields",
        "archive": {"bytes": 1777278, "sha256": "d0d2de844d90561a472f4fc50760cb2eccd697c264b4be35d0fb880674e0c2d9"},
        "queueAuthority": {"applied": 828, "pending": 20, "acceptedUnapplied": 0,
                           "completeStandaloneProcedures": 552, "scopedInterfaces": 173,
                           "firstReviews": 0, "closureTasks": 20},
    }
    ruling02_path = PACKET / "authority" / "PG327_W08_DIRECTOR_HOLD_365_REPACK02.json"
    write_json(ruling02_path, ruling02)
    binding_rows.append({"repositoryPath": "GPT browser ruling transcribed from Review Time Stop Witness Evidence",
                         "packetMember": ruling02_path.relative_to(PACKET).as_posix(), **file_binding(ruling02_path),
                         "evidenceClass": "current Director hold; W08 is unsealed and the identity remains held"})

    profile_map = {
        "id": "PG327-W08-REPACK03-RESIDUAL-REMEDIATION-MAP",
        "priorRuling": ruling02["rulingId"], "newWitnessStatus": "REPACK03_SUBMITTED; FRESH_DIRECTOR_REVIEW_REQUIRED",
        "closedResidualIdsByPriorRuling": ruling02["closedResidualIds"],
        "remainingResidualIdsFromPriorRuling": ruling02["remainingResidualIds"],
        "residuals": [
            {"id": "W08-365-R1", "artifact": "sources/W08_CASTER_PROFILES_365_TESTONLY.json",
             "evidence": ["source-bound Mage17/Mage9 class levels and class histories", "derived PB/M/S/spell attack/DC/Dissonance limit/RP",
                          "RP 50->24 and 26->16", "spell selections and ready-to-cast profile records", "currentStanding=3", "conditions and concentration"]},
            {"id": "W08-365-R2", "artifact": "commonPrefix/events W08-E05 through W08-E14",
             "evidence": ["PG9-Q01 operative Mage Conjuration recorded while catalog Abjuration metadata remains unchanged",
                          "actual V/S/F and focus custody", "cast range/perception/line-of-effect", "Action consumption and RP payment",
                          "Dissonance/Refrain and concentration", "both Counterspell windows; self explicitly no-attempt with eligibility not adjudicated; other participant declines"]},
            {"id": "W08-365-R3", "artifact": "commonPrefix/events and timeModel.scheduledMarkers",
             "evidence": ["non-overlapping regular start/end slots through 66", "once-only refresh and unused allowance expiration",
                          "source-bound Guarded stance choice, expiry and AC/Speed allowances", "owner turn end before attached phase",
                          "command eligibility/global allowance", "unused commanded Action expires; no damage branch",
                          "latest movement-phase ledger preserved with historical crossing expenditure", "t60 expiry and t66 closure before equal-time starts"]},
            {"id": "W08-365-R4", "artifact": "W08-E21-LANTERN-LOAN, W08-E26-GATE-CROSSING, W08-E28-CHAMPION-SOURCE-EXPIRY",
             "evidence": ["consistent left-hand custody", "explicit 0.5-foot cargo volume and [2,0,3] carried offset",
                          "numeric BAN-CELL-03 [-7.5,-7.5,0]..[7.5,7.5,15]", "complete body/cargo admission sweep",
                          "admission cargo envelope preserved separately from dropped current envelope at [2,0,0.25]"]},
            {"id": "W08-365-R5", "artifact": "W08-E26-GATE-CROSSING and every closure projection",
             "evidence": ["fixed originAnchor=[105,100,0] from the actual admission endpoint", "cargo projection=[107,100,0.25]"]},
            {"id": "W08-365-R6", "artifact": "terminalForks[*].finalState.world.terminalGeometryFixture",
             "evidence": ["continuous item envelope and floor support", "stationary occupant and physical barrier AABBs",
                          "unique nearest adjacent corridor candidate", "sealed pending bay with tiled neighbor volumes",
                          "no displacement, wall passage, or false creature conflict"]},
            {"id": "W08-365-R7", "artifact": "W08_SOURCE_BINDINGS_365.json, event sourcePointers and ARCHIVE_DELIVERY_365_W08_REPACK03.json",
             "evidence": ["Gate pointer /procedure and separate PG9 labels", "equipment catalog /records/169",
                          "actual rules/BODY_EQUIPMENT.md member", "resolvable procedure pointers", "root ARCHIVE_MANIFEST.json path",
                          "replay/semantic review distinction; W08 remains outstanding in delivery metadata"]},
            {"id": "W08-365-R8", "artifact": "commonPrefix/events W08-E24 through W08-E27",
             "evidence": ["Champion Strike and 20HP training target removed", "commanded Action recorded unused and expired at phase end",
                          "no damage, wound, save, target-turn, or opportunity-attack branch introduced"]},
        ],
        "identityDisposition": "HOLD", "applicationAuthorized": False,
        "freshDirectorDecisionRequired": True,
    }
    remediation_path = PACKET / "authority" / "W08_RESIDUAL_REMEDIATION_MAP_365_REPACK03.json"
    write_json(remediation_path, profile_map)
    binding_rows.append({"repositoryPath": "TEST_ONLY W08 residual remediation map",
                         "packetMember": remediation_path.relative_to(PACKET).as_posix(), **file_binding(remediation_path),
                         "evidenceClass": "cross-reference for fresh Director review; residuals not self-closed"})

    case["status"] = "TEST_ONLY_REPACK03_SUBMITTED_FOR_FRESH_DIRECTOR_ADJUDICATION"
    case["operativeGateSchool"] = {"school": "Conjuration", "sourcePointer": "sources/RETURN327_banishment-gate.json#/procedure",
                                    "paragraphLabel": "PG9-Q01", "catalogSchoolMetadata": "Abjuration",
                                    "catalogPreservedUnchanged": True}
    case["actorProfileArtifact"] = "sources/W08_CASTER_PROFILES_365_TESTONLY.json"
    case["sourceUse"]["eligibility"]["currentStanding"] = 3
    case["sourceUse"]["casterProfiles"] = {"gateCaster": "W08-MAGE17-GATECASTER-TESTONLY",
                                            "championOwner": "W08-MAGE9-CHAMPION-OWNER-TESTONLY"}
    case["cargoRecord"].update({"occupiedVolumeFt": [0.5, 0.5, 0.5], "carriedOffsetBeforeExpiryFt": [2, 0, 3],
                                "cellLocalAfterDropFt": [2, 0, 0.25], "projectedWorldAnchorFt": [107, 100, 0.25],
                                "allDimensionsAreTESTOnly": True})
    case["timeModel"] = {
        "unit": "absolute elapsed seconds; 6-second regular-round boundaries; sequenceAtTimestamp resolves equal-time events",
        "roundIntervalSeconds": 6,
        "gateConcentration": {"begins": -5, "deadline": 595, "activeAtCellClosure": True},
        "summonSource": {"begins": 0, "originalDeadline": 60, "endsAtOriginalDeadline": True},
        "admission": {"at": 6, "worldEndpointFt": [105, 100, 0], "cellDeadline": 66,
                      "rule": "independent Gate admission + 60 seconds"},
        "actorTurnStartSeconds": {"gateCaster": [-6, 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66],
                                   "championOwner": [-12, 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66]},
        "actorTurnEndSeconds": {"gateCaster": [-4, 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66],
                                 "championOwner": [-12, 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66]},
        "equalTimestampOrder": [{"time": 60, "first": "mandatory finite Champion source expiry", "then": "Mage regular starts"},
                                {"time": 66, "first": "mandatory Gate cell closure", "then": "Mage regular starts"}],
        "sourceExpiryBeforeCellDeadline": True, "sourceExpiryDoesNotCloseGateCell": True,
        "companionCommand": {"ownerTurnEndBeforeAttachedPhase": True, "ownerBonusActionConsumed": True,
                             "globalAllowanceConsumedOnce": True, "unusedCommandMovementExpiresAfterPhase": True},
        "scheduledMarkers": [],
        "directorDisposition": "W08 remains OUTSTANDING until GPT seals it; lifecycle replay is not a semantic ruling",
    }
    all_events = list(case["commonPrefix"]["events"]) + [e for f in case["terminalForks"] for e in f["events"]]
    case["timeModel"]["scheduledMarkers"] = [
        {"eventId": e["eventId"], "timestampSeconds": e["timestampSeconds"],
         "sequenceAtTimestamp": e.get("sequenceAtTimestamp"), "actorId": e["regularTurnMarker"]["actorId"],
         "marker": e["regularTurnMarker"]["marker"]}
        for e in all_events if e.get("regularTurnMarker")
    ]
    case["scenarioBoundary"]["allActorsAndPhysicalFactsRemainTestOnly"] = True
    case["identityDecision"] = "HOLD"
    case["acceptanceDecision"] = "not accepted; fresh Director adjudication required"
    case["applicationAuthorized"] = False
    case_path.write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    # Pointer and paragraph labels are separate. No prose is embedded in JSON-pointer fragments.
    source_bindings["bindings"] = binding_rows
    source_bindings["directorReviewStatus"] = "W08 OUTSTANDING; REPACK03 REQUESTS FRESH DECISION"
    source_bindings["priorDirectorRulingMember"] = "authority/PG327_W08_DIRECTOR_HOLD_365_REPACK02.json"
    bindings_path.write_text(json.dumps(source_bindings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    coverage = {
        "id": "PG327-W08-COVERAGE-365-REPACK03",
        "witnessId": "W08",
        "coverage": {
            "archiveSourceBindings": "AUTHORED_PENDING_INDEPENDENT_VERIFICATION",
            "casterSourceQualificationAndDerivedResources": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
            "castingPredicatesAndCounterspellDecisions": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
            "orderedRegularTurnsAndCommandPhase": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
            "cargoCustodyAndBAN_CELL_03Geometry": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
            "admissionEndpointOriginAnchor": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
            "terminalPlacementGeometry": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
            "forwardInverseReplay": "PENDING_INDEPENDENT_VERIFICATION",
            "directorSeal": "PENDING",
        },
        "notClaimed": ["campaign occurrence", "native runtime selection", "runtime implementation", "human playtest",
                       "semantic acceptance", "whole-identity acceptance", "application authorization"],
        "identityDecision": "HOLD", "applicationAuthorized": False,
    }
    write_json(PACKET / "W08_CASE_COVERAGE_365.json", coverage)
    build_report = {
        "id": "PG327-W08-BUILD-VALIDATION-365-REPACK03",
        "builtAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PREPARED_FOR_INDEPENDENT_REPLAY_AND_FRESH_DIRECTOR_REVIEW",
        "commonPrefixEventCount": len(case["commonPrefix"]["events"]),
        "terminalForkCount": len(case["terminalForks"]),
        "branchEventCounts": {b["branchId"]: len(b["events"]) for b in case["terminalForks"]},
        "allCommonEventsHaveInverse": all(e["inverseOperations"] or e["beforeStateSha256"] == e["afterStateSha256"]
                                           for e in case["commonPrefix"]["events"]),
        "allBranchesRestoreCommonPrefix": all(b["restoresCommonPrefix"] for b in case["terminalForks"]),
        "semanticStatus": "TEST_ONLY_FIXTURE_ENCODED; NOT_DIRECTOR_ADJUDICATED",
        "queueBeforeAndAfter": {"applied": 828, "pending": 20, "acceptedUnapplied": 0,
                                 "completeStandaloneProcedures": 552, "scopedInterfaces": 173,
                                 "firstReviews": 0, "closureTasks": 20},
        "identityDecision": "HOLD", "applicationAuthorized": False,
    }
    write_json(PACKET / "W08_BUILD_VALIDATION_365.json", build_report)
    write_json(PACKET / "INDEPENDENT_AUDIT_365_W08.json", {
        "id": "PG327-W08-INDEPENDENT-AUDIT-365-REPACK03",
        "status": "PENDING_INDEPENDENT_REPLAY; SEMANTICS_AWAIT_DIRECTOR_ADJUDICATION",
        "scope": "TEST_ONLY W08 witness; not spell identity acceptance or application",
        "semanticAudit": {"witnessPredicates": "ENCODED_TEST_ONLY_PENDING_DIRECTOR_REVIEW",
                          "directorDecision": "PENDING"},
        "archiveAudit": None,
        "decisionBoundary": {"banishmentGate": "HOLD", "applicationAuthorized": False,
                             "queueAuthority": build_report["queueBeforeAndAfter"]},
    })


def _unused_repack01_grid_branches(common_state: dict[str, Any]) -> list[dict[str, Any]]:
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
                     "jsonPointers": [], "use": "ordinary action/bonus-action budgets and Guarded stance effects/expiry"})

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
    pass


# Repack02 preserves repack01 as history and rebuilds the witness from a
# source-qualified TEST_ONLY fixture.  The original helpers remain the replay
# engine; these replacements define the corrected scenario.
_V01_INITIAL_STATE = make_initial_state
_V01_MAIN = main
ITEM_ID = "object-genuine-hooded-lantern-w08-001"
FOCUS_GATE_ID = "object-mage-focus-w08-gate-01"
FOCUS_OWNER_ID = "object-mage-focus-w08-owner-01"
GATE_CASTER_ID = "actor-gate-caster-w08"
OWNER_ID = "actor-champion-owner-w08"
CHAMPION_ID = "summoned-faction-champion-w08"
GATE_ID = "gate-w08-humanoid-01"
CELL_ID = "cell-w08-001"
ORIGIN = "PLANE-W08-TEST-ORIGIN-01"


def _turn_state() -> dict[str, Any]:
    return {
        "active": False,
        "turnNumber": 0,
        "refreshCount": 0,
        "actionAvailable": False,
        "bonusActionAvailable": False,
        "reactionAvailable": False,
        "movementBudgetFt": 30,
        "movementRemainingFt": 0,
        "companionCommandAllowanceAvailable": False,
        "spellcastsThisTurn": 0,
        "weaveAbilitiesThisTurn": 0,
        "expiredAllowances": [],
        "stanceSelection": None,
    }


def _mage_actor(actor_id: str, level: int, position: list[float], focus_id: str,
                learned: list[dict[str, Any]], faction: dict[str, Any] | None = None) -> dict[str, Any]:
    proficiency = 2 + ((level - 1) // 4)
    int_mod = 4
    rp_max = {9: 26, 17: 50}[level]
    selected_cards = ["mage.arch.counterspell"]
    return {
        "id": actor_id,
        "class": "Mage",
        "classLevel": level,
        "totalCharacterLevel": level,
        "classPath": "Arcanist" if level == 9 else "Archmage",
        "ancestry": "explicit TEST_ONLY humanoid profile; no ancestry feature is invoked",
        "abilityScores": {"STR": 10, "DEX": 14, "CON": 14, "INT": 18, "WIS": 12, "CHA": 10},
        "derived": {
            "proficiencyBonus": proficiency,
            "intelligenceModifier": int_mod,
            "mageM": max(1, int_mod),
            "mageS": 2 if level == 9 else 4,
            "spellAttackBonus": proficiency + int_mod,
            "spellSaveDC": 8 + proficiency + int_mod,
            "dissonanceLimit": 2 + proficiency + int_mod,
            "maximumRP": rp_max,
            "derivationStatus": "source-derived from the bound Mage JSON and Player Rulebook; no campaign character asserted",
        },
        "testOnlyVitals": {"hpCurrent": 80 if level == 9 else 100, "hpMaximum": 80 if level == 9 else 100,
                           "ac": 15, "basis": "authored TEST_ONLY inputs, unused by any W08 predicate"},
        "combatState": {"baseAC": 15, "activeAC": 15, "baseSpeedFt": 30, "activeSpeedFt": 30,
                        "activeStance": None, "stanceHistory": []},
        "rp": {"initial": rp_max, "maximum": rp_max, "current": rp_max, "spent": 0},
        "magicState": {
            "dissonance": 0,
            "dissonanceState": "In Tune",
            "refrain": {"lastSpellId": None, "consecutiveRepeatCount": 0},
            "nukeChain": [],
            "elementalFocus": "Fire",
            "counterspellRechargeRounds": 0,
            "lastCounterspellRechargeTickRound": None,
        },
        "conditions": [],
        "conditionState": {"conscious": True, "incapacitated": False, "silenced": False,
                           "restrained": False, "spellcastingSuppressed": False},
        "spellRepertoire": {
            "selectedClassCards": selected_cards,
            "learnedSpells": copy.deepcopy(learned),
            "availableAtWitnessStart": [x["spellId"] for x in learned],
            "preparationStatus": "explicit TEST_ONLY ready-to-cast spellbook state; selection eligibility is source-bound",
        },
        "classHistory": {
            "levels": [{"class": "Mage", "classLevel": n} for n in range(1, level + 1)],
            "pathSelections": ([{"mageLevel": 3, "path": "Arcanist"}] if level == 9 else
                               [{"mageLevel": 3, "path": "Arcanist"}, {"mageLevel": 10, "path": "Archmage"}]),
            "selectedClassCardHistory": [{"mageLevel": 9, "cardId": "mage.arch.counterspell",
                                          "selectionMethod": "Mage class-card selection; minimum level 9"}],
            "spellAcquisitionHistory": copy.deepcopy(learned),
        },
        "spellHistory": [],
        "spellcasting": {"pendingCast": None, "componentsAvailable": None},
        "concentration": None,
        "planeKey": ORIGIN,
        "positionFt": list(position),
        "perceptionState": {"ordinarySight": True, "ordinaryHearing": True, "lineOfEffectClear": True},
        "focusObjectId": focus_id,
        "hands": {"left": "free", "right": focus_id,
                  "rightHandRole": "holds the identified arcane-focus wand for F; left hand performs S"},
        "ownedObjectIds": [focus_id],
        "custodyObjectIds": [focus_id],
        "turnState": _turn_state(),
        "factionEligibility": copy.deepcopy(faction),
        "fixtureStatus": "conditional TEST_ONLY caster; no campaign character or event asserted",
    }


def make_initial_state() -> dict[str, Any]:
    state = _V01_INITIAL_STATE()
    gate_spells = [
        {"spellId": "mage.arch.counterspell", "class": "Mage", "school": "Abjuration", "rank": 5,
         "acquiredAtMageLevel": 9, "selection": "selected Mage class card", "available": True,
         "source": "sources/MAGE_CLASS_PLAYTEST.json#/cards/23"},
        {"spellId": "banishment-gate", "class": "Mage", "school": "Conjuration", "rank": 9,
         "minimumClassLevel": 17, "baseRp": 26, "acquiredAtMageLevel": 17,
         "selection": "explicit TEST_ONLY ordinary Mage spellbook history; class access and level are source-bound",
         "available": True, "source": "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json#/classAccess/Mage",
         "operativeSchoolSource": "sources/RETURN327_banishment-gate.json#/procedure; PG9-Q01",
         "catalogMetadataConflict": "catalog school remains Abjuration; operative route for this witness is Mage Conjuration"},
    ]
    owner_spells = [
        {"spellId": "mage.arch.counterspell", "class": "Mage", "school": "Abjuration", "rank": 5,
         "acquiredAtMageLevel": 9, "selection": "selected Mage class card", "available": True,
         "source": "sources/MAGE_CLASS_PLAYTEST.json#/cards/23"},
        {"spellId": "faction-champion", "class": "Mage", "school": "Conjuration", "rank": 5,
         "minimumClassLevel": 9, "baseRp": 10, "acquiredAtMageLevel": 9,
         "selection": "explicit TEST_ONLY ordinary Mage spellbook history; accepted class access and level are source-bound",
         "available": True, "source": "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/spellAccessAndRoute"},
    ]
    faction = {
        "factionId": "FACTION-W08-TEST-A",
        "classification": "explicit conditional TEST_ONLY faction premise; no real membership or faction asserted",
        "alliedStatus": True,
        "currentStanding": 3,
        "invocationPermission": True,
        "aidProhibition": False,
        "predicateSource": "sources/AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json#/sharedRule",
    }
    state["actors"] = {
        "gateCaster": _mage_actor(GATE_CASTER_ID, 17, [70, 100, 0], FOCUS_GATE_ID, gate_spells),
        "championOwner": _mage_actor(OWNER_ID, 9, [80, 100, 0], FOCUS_OWNER_ID, owner_spells, faction),
        "champion": {
            "id": CHAMPION_ID, "exists": False, "bodyState": "not-created", "creatureType": None,
            "corpseExists": False, "intrinsicManifestation": {"status": "not-formed", "items": []},
            "externalObjectIds": [], "fixtureBodyGeometry": None, "planeKey": ORIGIN, "positionFt": None,
            "movement": {"speedFt": 30, "budgetFt": 0, "spentFt": 0, "remainingFt": 0,
                         "expiredUnusedFt": 0},
            "movementHistory": [],
            "hands": {"left": "free", "right": "free"}, "turnState": {"attachedPhase": None},
            "fixtureStatus": "not created until the source-bound cast resolves",
        },
    }
    state["world"].update({
        "originPlaneKey": ORIGIN,
        "gateWorldPose": {"centerFt": [100, 100, 7.5], "baseZFt": 0, "normal": [1, 0, 0],
                           "portalPlaneXFt": 100, "widthAlongYFt": 10, "heightFt": 15},
        "geometryConvention": "TEST_ONLY world coordinates in feet; actor positions are ground-level body origins; AABBs use min-inclusive/max-exclusive occupancy and boundary contact is non-overlap",
        "terrain": "TEST_ONLY level supported floor, clear Gate approach, ordinary sight and line of effect",
        "actionEconomy": {"maximumAdditionalFullActionsPerCreaturePerRound": 1, "additionalFullActionsUsed": 0},
    })
    state["gate"] = {"id": GATE_ID, "status": "not-created", "active": False, "selectedCreatureType": None,
                     "creatorId": GATE_CASTER_ID, "spellRpSpent": 0, "concentrationDeadlineSeconds": None,
                     "liveCellIds": [], "hardControlClaims": [], "aperture": None, "spellRoute": None}
    state["cell"] = None
    state["objects"] = {
        FOCUS_GATE_ID: {"id": FOCUS_GATE_ID, "name": "Arcane focus wand", "sourceCatalogId": "arcane-focuses.wand",
                        "ownerId": GATE_CASTER_ID, "custodianId": GATE_CASTER_ID, "quantity": 1,
                        "physicalPosition": {"planeKey": ORIGIN, "worldFt": [70, 100, 1], "carriedSlot": "right hand"},
                        "fixtureStatus": "TEST_ONLY focus identity and custody; one-hand component focus"},
        FOCUS_OWNER_ID: {"id": FOCUS_OWNER_ID, "name": "Arcane focus wand", "sourceCatalogId": "arcane-focuses.wand",
                         "ownerId": OWNER_ID, "custodianId": OWNER_ID, "quantity": 1,
                         "physicalPosition": {"planeKey": ORIGIN, "worldFt": [80, 100, 1], "carriedSlot": "right hand"},
                         "fixtureStatus": "TEST_ONLY focus identity and custody; one-hand component focus"},
    }
    state["eventReceipts"] = {}
    state["turnScheduleLog"] = []
    state["castingWindows"] = []
    state["testFixtureBoundaries"].update({
        "noCampaignFacts": True, "noRuntimeExecution": True, "noIdentityAcceptance": True,
        "noApplicationAuthorization": True, "AC5BanishElementalExtensionImported": False,
        "AC5X17MechanicsImported": False, "magicalEndpointBlockerPresent": False,
        "allCasterProfilesAreTestOnly": True,
    })
    return state


def _geometry_aabb(center: list[float], size: list[float]) -> dict[str, list[float]]:
    return {"min": [center[i] - size[i] / 2 for i in range(3)],
            "max": [center[i] + size[i] / 2 for i in range(3)]}


def build_common_prefix() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    state = make_initial_state()
    initial = copy.deepcopy(state)
    events: list[dict[str, Any]] = []
    order_by_time: dict[int, int] = {}

    def emit(event_id: str, seconds: int, kind: str, description: str,
             mutate: Callable[[dict[str, Any]], None], sources: list[str],
             labels: list[str] | None = None, marker: dict[str, Any] | None = None) -> None:
        def wrapped(s: dict[str, Any]) -> None:
            s["elapsedSeconds"] = seconds
            mutate(s)
        updated = record_event(events, state, event_id, seconds, kind, description, wrapped, sources)
        state.clear()
        state.update(updated)
        order_by_time[seconds] = order_by_time.get(seconds, 0) + 1
        events[-1]["sequenceAtTimestamp"] = order_by_time[seconds]
        events[-1]["sourceParagraphLabels"] = list(labels or [])
        if marker is not None:
            events[-1]["regularTurnMarker"] = copy.deepcopy(marker)

    mage_source = "sources/MAGE_CLASS_PLAYTEST.json#/engine"
    turn_sources = [mage_source + "/8", mage_source + "/9", "sources/COMBAT_ACTION_PLAYTEST.md#lines-60-62",
                    "sources/COMBAT_ACTION_PLAYTEST.md#lines-111-115"]
    gate_sources = ["sources/RETURN327_banishment-gate.json#/procedure",
                    "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json#/classAccess/Mage"]
    body_sources = ["rules/BODY_EQUIPMENT.md#lines-50-51", "rules/BODY_EQUIPMENT.md#lines-88-109"]
    mage_data = git_bytes(SOURCE_COMMIT, "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json")
    mage_path = PACKET / "sources" / "MAGE_CLASS_PLAYTEST.json"
    if not mage_path.exists():
        add_source_copy(mage_path, mage_data)
    mage_json = read_json_bytes(mage_data)
    counterspell_index = next(i for i, row in enumerate(mage_json["cards"]) if row.get("id") == "mage.arch.counterspell")
    counterspell_pointer = f"sources/MAGE_CLASS_PLAYTEST.json#/cards/{counterspell_index}"
    ac5_model = read_json_bytes((PACKET / "sources" / "AC5_ACCEPTED_SPELLS_MODEL.json").read_bytes())
    fc_index = next(i for i, row in enumerate(ac5_model["spells"]) if row.get("id") == "faction-champion")
    fc_spell_pointer = f"sources/AC5_ACCEPTED_SPELLS_MODEL.json#/spells/{fc_index}"
    counterspell_pointer = "sources/MAGE_CLASS_PLAYTEST.json#/cards/23"

    def acquire(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        owner["gold"] = {"initialGp": 20, "currentGp": 15, "spentGp": 5}
        owner["ownedObjectIds"].append(ITEM_ID)
        owner["custodyObjectIds"].append(ITEM_ID)
        s["objects"][ITEM_ID] = {
            "id": ITEM_ID, "name": "Lantern, hooded", "quantity": 1, "genuine": True, "magical": False,
            "sourceCatalogId": "adventuring-gear.lantern-hooded", "costGp": 5, "weightLb": 2,
            "load": 0.2, "occupiedVolumeFt": [0.5, 0.5, 0.5],
            "occupiedVolumeBasis": "explicit TEST_ONLY fixture dimensions; catalog establishes name, price and weight only",
            "ownerId": OWNER_ID, "custodianId": OWNER_ID, "status": "genuine-owner-carried-at-hip-loop",
            "physicalPosition": {"planeKey": ORIGIN, "worldFt": [80.5, 100, 1], "carriedSlot": "hip loop",
                                 "carrierOffsetFt": [0.5, 0, 1], "volumeFt": [0.5, 0.5, 0.5]},
            "sourceAcquisition": {"eventId": "W08-E01-LANTERN-ACQUIRE", "goldPaidGp": 5,
                                  "sourceRecordId": "adventuring-gear.lantern-hooded"},
            "damageState": "intact",
        }
        s["eventReceipts"]["W08-E01-LANTERN-ACQUIRE"] = {"applied": True, "quantityCreated": 1,
                                                          "priceGp": 5, "ownerId": OWNER_ID}
    emit("W08-E01-LANTERN-ACQUIRE", -10, "object-acquisition",
         "Acquire one real, nonmagical hooded lantern before summon creation and before admission; ownership and custody are distinct.",
         acquire, ["sources/EQUIPMENT_SOURCE_CATALOG.json#/records/169", "sources/PLAYER_RULEBOOK_V6_SOURCE.txt#line-6976"])

    def turn_start(actor_key: str, round_time: int, phase: str = "regular") -> Callable[[dict[str, Any]], None]:
        def mutate(s: dict[str, Any]) -> None:
            actor = s["actors"][actor_key]
            ts = actor["turnState"]
            if ts["active"]:
                raise ValueError(f"duplicate or overlapping regular turn start: {actor_key} at {round_time}")
            combat = actor["combatState"]
            previous_stance = combat.get("activeStance")
            if previous_stance is not None:
                previous_stance["expiredAtSeconds"] = round_time
                previous_stance["expiryReason"] = "next regular own-turn start"
                if combat["stanceHistory"]:
                    combat["stanceHistory"][-1]["expiredAtSeconds"] = round_time
                    combat["stanceHistory"][-1]["expiryReason"] = "next regular own-turn start"
            expired_stance = copy.deepcopy(previous_stance)
            stance = {"name": "Guarded", "selectedAtSeconds": round_time,
                      "expiresAtNextRegularStart": True, "expiresAtSeconds": None,
                      "source": "sources/COMBAT_ACTION_PLAYTEST.md#lines-111-115",
                      "effects": {"acBonus": 1, "speedChangeFt": -5,
                                  "explicitShoveResistanceAdvantage": True}}
            combat["stanceHistory"].append(copy.deepcopy(stance))
            combat["activeStance"] = stance
            combat["activeAC"] = combat["baseAC"] + 1
            combat["activeSpeedFt"] = max(0, combat["baseSpeedFt"] - 5)
            stance_receipt = {**copy.deepcopy(stance), "dependentAllowances": {
                "movementBudgetFt": combat["activeSpeedFt"], "activeAC": combat["activeAC"]}}
            ts["turnNumber"] += 1
            ts["refreshCount"] += 1
            ts.update({"active": True, "actionAvailable": True, "bonusActionAvailable": True,
                       "reactionAvailable": True, "movementBudgetFt": combat["activeSpeedFt"],
                       "movementRemainingFt": combat["activeSpeedFt"], "stanceSelection": copy.deepcopy(stance_receipt),
                       "companionCommandAllowanceAvailable": True if actor_key == "championOwner" else False,
                       "spellcastsThisTurn": 0, "weaveAbilitiesThisTurn": 0, "expiredAllowances": []})
            if actor_key == "championOwner":
                actor["companionCommandUse"] = None
            magic = actor.get("magicState")
            if magic and magic["counterspellRechargeRounds"] > 0:
                magic["counterspellRechargeRounds"] -= 1
                magic["lastCounterspellRechargeTickRound"] = round_time // 6
            s["turnScheduleLog"].append({"actorId": actor["id"], "actorKey": actor_key,
                                         "turnNumber": ts["turnNumber"], "roundBoundarySeconds": round_time,
                                         "marker": "START", "onceOnlyRefresh": True,
                                         "stanceSelection": copy.deepcopy(stance_receipt)})
            s["eventReceipts"][f"TURN-START-{actor_key}-{round_time}"] = {
                "actorId": actor["id"], "turnNumber": ts["turnNumber"], "refreshedOnce": True,
                "action": True, "bonusAction": True, "reaction": True,
                "movementFt": combat["activeSpeedFt"], "companionCommandAllowance": actor_key == "championOwner",
                "stanceSelection": copy.deepcopy(stance_receipt),
                "expiredPriorStance": expired_stance}
        return mutate

    def turn_end(actor_key: str, round_time: int) -> Callable[[dict[str, Any]], None]:
        def mutate(s: dict[str, Any]) -> None:
            actor = s["actors"][actor_key]
            ts = actor["turnState"]
            if not ts["active"]:
                raise ValueError(f"regular turn ended without start: {actor_key} at {round_time}")
            no_magic = ts["spellcastsThisTurn"] == 0 and ts["weaveAbilitiesThisTurn"] == 0
            before_dissonance = actor["magicState"]["dissonance"]
            if no_magic:
                actor["magicState"]["dissonance"] = max(0, before_dissonance - 1)
            unused = {"action": ts["actionAvailable"], "bonusAction": ts["bonusActionAvailable"],
                      "movementFt": ts["movementRemainingFt"],
                      "companionCommand": ts["companionCommandAllowanceAvailable"]}
            ts["expiredAllowances"].append({"roundBoundarySeconds": round_time, "unused": copy.deepcopy(unused)})
            ts.update({"active": False, "actionAvailable": False, "bonusActionAvailable": False,
                       "movementRemainingFt": 0, "companionCommandAllowanceAvailable": False})
            stance_at_end = copy.deepcopy(actor["combatState"]["activeStance"])
            s["turnScheduleLog"].append({"actorId": actor["id"], "actorKey": actor_key,
                                         "turnNumber": ts["turnNumber"], "roundBoundarySeconds": round_time,
                                         "marker": "END", "noSpellOrWeave": no_magic,
                                         "dissonanceBefore": before_dissonance,
                                         "dissonanceAfter": actor["magicState"]["dissonance"],
                                         "stanceContinuesUntilNextRegularStart": stance_at_end,
                                         "unusedAllowancesExpired": copy.deepcopy(unused)})
            s["eventReceipts"][f"TURN-END-{actor_key}-{round_time}"] = {
                "actorId": actor["id"], "turnNumber": ts["turnNumber"], "noSpellOrWeave": no_magic,
                "dissonanceBefore": before_dissonance, "dissonanceAfter": actor["magicState"]["dissonance"],
                "unusedAllowancesExpired": copy.deepcopy(unused), "reactionRetainedUntilNextStart": ts["reactionAvailable"],
                "stanceContinuesUntilNextRegularStart": stance_at_end}
        return mutate

    def emit_turn(actor_key: str, seconds: int, phase: str, is_start: bool, event_id: str) -> None:
        actor_id = GATE_CASTER_ID if actor_key == "gateCaster" else OWNER_ID
        marker = {"actorKey": actor_key, "actorId": actor_id, "roundBoundarySeconds": seconds,
                  "marker": "START" if is_start else "END", "phase": phase,
                  "onceOnlyRefresh": is_start}
        emit(event_id, seconds, "regular-turn-start" if is_start else "regular-turn-end",
             f"{actor_key} regular Mage turn {'starts and refreshes allowances once' if is_start else 'ends and expires unused allowances'} at the ordered {seconds}-second boundary.",
             turn_start(actor_key, seconds, phase) if is_start else turn_end(actor_key, seconds),
             turn_sources, marker=marker)

    # The owner completes an earlier idle turn so its Reaction remains available
    # for the Gate cast; regular Mage turns never overlap.
    emit_turn("championOwner", -12, "pre-Gate idle round", True, "W08-E02-OWNER-START-M12")
    emit_turn("championOwner", -12, "pre-Gate idle round", False, "W08-E03-OWNER-END-M12")
    emit_turn("gateCaster", -6, "Gate-cast round", True, "W08-E04-GATECASTER-START-M06")

    def cast_commit(actor_key: str, spell_id: str, rank: int, cost: int, target: list[float],
                    range_ft: int, school: str, source_deadline: int | None = None) -> Callable[[dict[str, Any]], None]:
        def mutate(s: dict[str, Any]) -> None:
            actor = s["actors"][actor_key]
            ts = actor["turnState"]
            assert ts["actionAvailable"] is True
            assert actor["rp"]["current"] >= cost
            actor["rp"]["current"] -= cost
            actor["rp"]["spent"] += cost
            ts["actionAvailable"] = False
            ts["spellcastsThisTurn"] += 1
            dis_before = actor["magicState"]["dissonance"]
            repeats = actor["magicState"]["refrain"]["consecutiveRepeatCount"] if actor["magicState"]["refrain"]["lastSpellId"] == spell_id else 0
            base_dissonance = 0 if rank == 0 else (1 if rank <= 5 else 2)
            dis_after = dis_before + base_dissonance + min(3, repeats)
            actor["magicState"]["dissonance"] = dis_after
            limit = actor["derived"]["dissonanceLimit"]
            actor["magicState"]["dissonanceState"] = "In Tune" if dis_after < limit else "Frayed"
            distance = sum((actor["positionFt"][i] - target[i]) ** 2 for i in range(3)) ** 0.5
            focus_id = actor["focusObjectId"]
            focus = s["objects"][focus_id]
            assert focus["ownerId"] == actor["id"] and focus["custodianId"] == actor["id"]
            components = {"V": {"available": True, "voiceClear": actor["conditionState"]["silenced"] is False},
                          "S": {"available": True, "hand": "left", "handState": "free"},
                          "F": {"available": True, "focusObjectId": focus_id,
                                "sourceCatalogId": focus["sourceCatalogId"], "heldByCaster": True,
                                "hand": "right", "custodyOwner": actor["id"]}}
            actor["spellcasting"]["componentsAvailable"] = copy.deepcopy(components)
            actor["spellcasting"]["pendingCast"] = {
                "spellId": spell_id, "rank": rank, "school": school, "committedAtSeconds": s["elapsedSeconds"],
                "rangeFt": range_ft, "measuredDistanceFt": round(distance, 4), "rangeValid": distance <= range_ft,
                "targetWorldFt": list(target), "perceived": actor["perceptionState"]["ordinarySight"],
                "lineOfEffectClear": actor["perceptionState"]["lineOfEffectClear"],
                "components": components, "actionConsumed": True, "concentrationSlotAvailable": actor["concentration"] is None,
                "sourceDeadlineSeconds": source_deadline, "status": "committed-awaiting-counterspell-window",
                "dissonance": {"before": dis_before, "baseIncrease": base_dissonance,
                               "refrainIncrease": min(3, repeats), "after": dis_after,
                               "limit": limit, "rpSurcharge": 0 if dis_before < limit else 1},
                "rp": {"before": actor["rp"]["current"] + cost, "cost": cost, "after": actor["rp"]["current"]},
            }
            s["eventReceipts"][f"CAST-COMMIT-{spell_id}"] = copy.deepcopy(actor["spellcasting"]["pendingCast"])
        return mutate

    def counterspell_window(caster_key: str, event_id: str, spell_id: str, rank: int) -> Callable[[dict[str, Any]], None]:
        def mutate(s: dict[str, Any]) -> None:
            caster = s["actors"][caster_key]
            pending = caster["spellcasting"]["pendingCast"]
            assert pending and pending["spellId"] == spell_id
            dc = 10 + 2 * rank
            records = []
            for other_key in ("gateCaster", "championOwner"):
                actor = s["actors"][other_key]
                same = other_key == caster_key
                card_selected = "mage.arch.counterspell" in actor["spellRepertoire"]["selectedClassCards"]
                reaction_ready = actor["turnState"]["reactionAvailable"] is True
                dx = actor["positionFt"][0] - caster["positionFt"][0]
                dy = actor["positionFt"][1] - caster["positionFt"][1]
                dz = actor["positionFt"][2] - caster["positionFt"][2]
                distance = (dx * dx + dy * dy + dz * dz) ** 0.5
                perceived = actor["perceptionState"]["ordinarySight"] and actor["perceptionState"]["lineOfEffectClear"]
                rp_ok = actor["rp"]["current"] >= 4
                ready = actor["magicState"]["counterspellRechargeRounds"] == 0
                eligible = None if same else (card_selected and reaction_ready and distance <= 60 and perceived and rp_ok and ready)
                records.append({
                    "actorId": actor["id"], "actorKey": other_key,
                    "mageCounterspellCardId": "mage.arch.counterspell" if card_selected else None,
                    "selectedCardEvidence": "sources/MAGE_CLASS_PLAYTEST.json#/cards/23" if card_selected else None,
                    "sameCreatureAsCaster": same, "cardSelected": card_selected,
                    "reactionAvailable": reaction_ready, "perceivesCaster": perceived,
                    "distanceFt": round(distance, 4), "rangeFt": 60, "withinRange": distance <= 60,
                    "rpAvailable": actor["rp"]["current"], "rpCost": 4, "rpSufficient": rp_ok,
                    "rechargeRemainingRounds": actor["magicState"]["counterspellRechargeRounds"],
                    "rechargeReady": ready, "eligible": eligible,
                    "eligibilityStatus": "not-adjudicated; participant made no attempt" if same else "evaluated",
                    "decision": "explicit-test-no-attempt" if same else ("declines" if eligible else "not-eligible"),
                    "decisionSource": ("explicit conditional TEST_ONLY no-attempt decision; no self-counter rule asserted"
                                       if same else ("explicit TEST_ONLY participant choice" if eligible else "derived eligibility predicate")),
                    "counterspellAttempted": False, "rpSpent": 0, "reactionConsumed": False,
                    "wouldCheckIntModifierPlusPB": actor["derived"]["spellAttackBonus"],
                    "counterspellCheckDCIfAttempted": dc,
                })
            s["castingWindows"].append({"eventId": event_id, "triggerSpellId": spell_id, "rank": rank,
                                         "counterspellCheckDC": dc, "participants": copy.deepcopy(records),
                                         "resolvedBy": "no Counterspell attempted; source spell proceeds"})
            s["eventReceipts"][event_id] = {"triggerSpellId": spell_id, "counterspellCheckDC": dc,
                                            "participantDecisions": records, "costsPaidBeforeWindow": True}
        return mutate

    def resolve_gate(s: dict[str, Any]) -> None:
        actor = s["actors"]["gateCaster"]
        pending = actor["spellcasting"]["pendingCast"]
        assert pending and pending["spellId"] == "banishment-gate"
        actor["spellHistory"].append({"spellId": "banishment-gate", "rank": 9, "school": "Conjuration",
                                      "castAtSeconds": -5, "resolved": True, "dissonanceAfter": actor["magicState"]["dissonance"]})
        actor["magicState"]["refrain"] = {"lastSpellId": "banishment-gate", "consecutiveRepeatCount": 0}
        actor["magicState"]["nukeChain"] = []
        actor["concentration"] = {"effectId": GATE_ID, "spellId": "banishment-gate", "startedAtSeconds": -5,
                                  "deadlineSeconds": 595, "active": True}
        actor["spellcasting"]["pendingCast"] = None
        s["gate"].update({"status": "active", "active": True, "selectedCreatureType": "Humanoid",
                          "spellRpSpent": 26, "castAtSeconds": -5, "concentrationDeadlineSeconds": 595,
                          "aperture": {"widthFt": 10, "heightFt": 15, "baseZFt": 0, "planeNormal": [1, 0, 0],
                                       "planeXFt": 100, "supportedClearArea": True},
                          "spellRoute": {"action": True, "components": ["V", "S", "F"], "rangeFt": 120,
                                         "class": "Mage", "rank": 9, "baseRp": 26,
                                         "school": "Conjuration",
                                         "schoolSource": "sources/RETURN327_banishment-gate.json#/procedure; PG9-Q01",
                                         "catalogMetadataConflictPreserved": "Abjuration in catalog metadata"},
                          "liveCellIds": [], "hardControlClaims": []})
        s["eventReceipts"]["W08-E07-GATE-CAST-RESOLVE"] = {"gateId": GATE_ID, "active": True,
                                                            "selectedCreatureType": "Humanoid",
                                                            "concentrationDeadlineSeconds": 595,
                                                            "paidRp": 26, "actionConsumed": True}

    emit("W08-E05-GATE-CAST-COMMIT", -5, "spell-cast-commit",
         "Mage17 commits Banishment Gate from a valid Mage acquisition; its Action and 26 RP are spent before the Counterspell window.",
         cast_commit("gateCaster", "banishment-gate", 9, 26, [100, 100, 7.5], 120, "Conjuration"),
         gate_sources + [mage_source, "sources/PLAYER_RULEBOOK_V6_SOURCE.txt#line-8395"],
         labels=["PG9-Q01", "PG9-Q13", "PG9-Q15", "PG9-Q17"])
    emit("W08-E06-GATE-COUNTERSPELL-WINDOW", -5, "counterspell-opportunity",
         "Every Mage participant is evaluated from the selected Mage Counterspell card, Reaction, distance, perception, RP and recharge state; the eligible owner declines.",
         counterspell_window("gateCaster", "W08-E06-GATE-COUNTERSPELL-WINDOW", "banishment-gate", 9),
         [mage_source + "/9", "sources/PLAYER_RULEBOOK_V6_SOURCE.txt#line-8395"],
         labels=["PG9-Q15"])
    emit("W08-E07-GATE-CAST-RESOLVE", -5, "spell-cast-resolution",
         "With no Counterspell attempt, the active Humanoid-fixed Gate resolves; its 600-second concentration deadline is separate from any later cell deadline.",
         resolve_gate, gate_sources + ["authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json#/source/coreEntries/0/original"],
         labels=["PG9-Q15", "PG9-Q17"])
    emit_turn("gateCaster", -4, "Gate-cast round", False, "W08-E08-GATECASTER-END-M04")

    emit_turn("gateCaster", 0, "Champion-cast round", True, "W08-E09-GATECASTER-START-T00")
    emit_turn("gateCaster", 0, "Champion-cast round", False, "W08-E10-GATECASTER-END-T00")
    emit_turn("championOwner", 0, "Champion-cast round", True, "W08-E11-OWNER-START-T00")

    emit("W08-E12-CHAMPION-CAST-COMMIT", 0, "spell-cast-commit",
         "Mage9 commits the accepted Faction Champion spell from a legal Mage-level-9 class route; its Action and 10 RP are spent before the Counterspell window.",
         cast_commit("championOwner", "faction-champion", 5, 10, [85, 100, 0], 60, "Conjuration", 60),
         [fc_spell_pointer, "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-FACTION-CHAMPION-01",
          "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/sharedRules/AC5-CHAMPION-ALLY-01", mage_source,
          "sources/PLAYER_RULEBOOK_V6_SOURCE.txt#line-8395"])
    emit("W08-E13-CHAMPION-COUNTERSPELL-WINDOW", 0, "counterspell-opportunity",
         "The active Mage17 Counterspell selection is in range, perceives the cast, has a ready Reaction/recharge and can pay; its TEST_ONLY decision is to decline.",
         counterspell_window("championOwner", "W08-E13-CHAMPION-COUNTERSPELL-WINDOW", "faction-champion", 5),
         [counterspell_pointer, mage_source + "/9", "sources/PLAYER_RULEBOOK_V6_SOURCE.txt#line-8395"])

    def resolve_champion(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champion = s["actors"]["champion"]
        pending = owner["spellcasting"]["pendingCast"]
        assert pending and pending["spellId"] == "faction-champion"
        owner["spellHistory"].append({"spellId": "faction-champion", "rank": 5, "school": "Conjuration",
                                       "castAtSeconds": 0, "resolved": True,
                                       "dissonanceAfter": owner["magicState"]["dissonance"]})
        owner["magicState"]["refrain"] = {"lastSpellId": "faction-champion", "consecutiveRepeatCount": 0}
        owner["magicState"]["nukeChain"] = []
        owner["concentration"] = {"effectId": "faction-champion-w08-source", "spellId": "faction-champion",
                                  "startedAtSeconds": 0, "deadlineSeconds": 60, "active": True}
        owner["spellcasting"]["pendingCast"] = None
        champion.update({
            "exists": True, "bodyState": "live", "creatureType": "Humanoid", "size": "Medium",
            "hp": {"current": 70, "maximum": 70}, "ac": 18,
            "abilities": {"STR": 18, "DEX": 12, "CON": 16, "INT": 10, "WIS": 12, "CHA": 12},
            "weightLb": 180, "occupiedHeightFt": 6, "footprintFt": [5, 5],
            "bodyLocalAabbFt": {"min": [-2.5, -2.5, 0], "max": [2.5, 2.5, 6]},
            "sourceSpellId": "faction-champion", "sourceSchool": "Conjuration",
            "sourceProfileId": "AC5-PROFILE-FACTION-CHAMPION-01", "sourceCreatedAtSeconds": 0,
            "sourceDeadlineSeconds": 60, "sourceEndReason": None, "corpseExists": False,
            "intrinsicManifestation": {"status": "present", "items": ["intrinsic-armor", "intrinsic-weapon", "intrinsic-shield"],
                                        "separateInventoryObjects": False},
            "externalObjectIds": [], "hands": {"left": "free", "right": "free"},
            "planeKey": ORIGIN, "positionFt": [85, 100, 0],
            "movement": {"speedFt": 30, "budgetFt": 0, "spentFt": 0, "remainingFt": 0, "expiredUnusedFt": 0},
            "turnState": {"attachedPhase": None},
            "fixtureStatus": "accepted finite profile instance under conditional TEST_ONLY facts; not a transported NPC",
        })
        s["eventReceipts"]["W08-E14-CHAMPION-CAST-RESOLVE"] = {
            "championId": CHAMPION_ID, "sourceSpellId": "faction-champion", "sourceDeadlineSeconds": 60,
            "profileId": "AC5-PROFILE-FACTION-CHAMPION-01", "bodyCreatedOnce": True,
            "corpseCreated": False, "intrinsicItemsAreSeparateLoot": False,
            "standingAtFormation": 3, "allFourSourcePredicatesTrue": True,
        }

    emit("W08-E14-CHAMPION-CAST-RESOLVE", 0, "spell-cast-resolution",
         "No Counterspell was attempted; the finite Humanoid Champion forms within 60 feet under the four explicit positive eligibility predicates and starts its original 60-second source clock.",
         resolve_champion,
         [fc_spell_pointer, "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-FACTION-CHAMPION-01",
          "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/sharedRules/AC5-CHAMPION-ALLY-01"], labels=["AC5-CHAMPION-ALLY-01"])
    emit_turn("championOwner", 0, "Champion-cast round", False, "W08-E15-OWNER-END-T00")

    def uncommanded_phase_start(s: dict[str, Any], time: int) -> None:
        champ = s["actors"]["champion"]
        assert champ["exists"]
        champ["movement"].update({"budgetFt": 30, "spentFt": 0, "remainingFt": 30, "expiredUnusedFt": 0})
        champ["turnState"]["attachedPhase"] = {"phaseId": f"CHAMPION-UNCOMMANDED-{time}", "active": True,
                                                     "commanded": False, "actionAvailable": True,
                                                     "stanceDecision": "Dodge; remain stationary",
                                                     "ownerWholeTurnEnded": True}
        s["eventReceipts"][f"CHAMPION-PHASE-START-{time}"] = {"afterOwnerTurnEnd": True, "commanded": False,
                                                               "permittedUncommandedAction": "Dodge"}

    def uncommanded_phase_end(s: dict[str, Any], time: int) -> None:
        champ = s["actors"]["champion"]
        phase = champ["turnState"]["attachedPhase"]
        phase.update({"active": False, "actionAvailable": False, "stanceResolved": "Dodge",
                      "movementExpiredFt": champ["movement"]["remainingFt"]})
        champ["movement"]["expiredUnusedFt"] = champ["movement"]["remainingFt"]
        champ["movement"]["remainingFt"] = 0
        champ["turnState"]["attachedPhase"] = phase
        s["eventReceipts"][f"CHAMPION-PHASE-END-{time}"] = {"movementSpentFt": 0,
                                                             "unusedMovementExpiredFt": 30,
                                                             "damageOrControl": False}

    emit("W08-E16-CHAMPION-UNCOMMANDED-PHASE-START-T00", 0, "uncommanded-companion-phase-start",
         "After the owner's full turn ends, the new uncommanded Champion elects to stay in place and Dodge; the Mage source permits that stance without damage or control.",
         lambda s: uncommanded_phase_start(s, 0), [mage_source + "/9", fc_spell_pointer])
    emit("W08-E17-CHAMPION-UNCOMMANDED-PHASE-END-T00", 0, "uncommanded-companion-phase-end",
         "The uncommanded phase closes; its unused 30-foot movement allowance expires and no attack or control action occurs.",
         lambda s: uncommanded_phase_end(s, 0), [mage_source + "/9"])

    emit_turn("gateCaster", 6, "cargo-crossing round", True, "W08-E18-GATECASTER-START-T06")
    emit_turn("gateCaster", 6, "cargo-crossing round", False, "W08-E19-GATECASTER-END-T06")
    emit_turn("championOwner", 6, "cargo-crossing round", True, "W08-E20-OWNER-START-T06")

    def transfer_cargo(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champ = s["actors"]["champion"]
        item = s["objects"][ITEM_ID]
        assert owner["turnState"]["actionAvailable"] is True
        assert owner["hands"]["left"] == "free"
        owner["turnState"]["actionAvailable"] = False
        owner["custodyObjectIds"].remove(ITEM_ID)
        champ["externalObjectIds"].append(ITEM_ID)
        champ["hands"]["left"] = ITEM_ID
        item["custodianId"] = CHAMPION_ID
        item["status"] = "genuine-borrowed-object-carried-by-summon"
        item["physicalPosition"] = {"planeKey": ORIGIN, "worldFt": [87, 100, 3], "carriedSlot": "left hand",
                                    "carrierId": CHAMPION_ID, "carrierOffsetFt": [2, 0, 3],
                                    "cellLocalFt": None, "volumeFt": [0.5, 0.5, 0.5],
                                    "fixtureGeometryStatus": "explicit TEST_ONLY occupied volume nested within the Champion body envelope"}
        s["eventReceipts"]["W08-E21-LANTERN-LOAN"] = {
            "itemId": ITEM_ID, "ownerUnchanged": True, "custodian": CHAMPION_ID, "quantity": 1,
            "occupiedHand": "left", "load": 0.2, "noDuplicate": True,
            "sourceCapacity": {"size": "Medium", "strength": 18, "physicalCapacityLb": 270,
                               "inventoryLoadCapacity": 18, "itemWeightLb": 2},
        }
    emit("W08-E21-LANTERN-LOAN", 6, "physical-custody-transfer",
         "The owner spends the refreshed ordinary Action to retrieve and lend the independently owned lantern from the hip loop; it occupies the Champion's left hand before any Gate crossing, while ownership remains unchanged.",
         transfer_cargo, ["sources/EQUIPMENT_SOURCE_CATALOG.json#/records/169", *body_sources,
                          "sources/COMBAT_ACTION_PLAYTEST.md#lines-31-32"], labels=["PG9-Q17"])

    def issue_command(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champ = s["actors"]["champion"]
        assert owner["turnState"]["bonusActionAvailable"]
        assert owner["turnState"]["companionCommandAllowanceAvailable"]
        assert owner["conditionState"]["conscious"] and not owner["conditionState"]["incapacitated"]
        assert champ["exists"] and champ["planeKey"] == ORIGIN
        assert champ["externalObjectIds"] == [ITEM_ID]
        distance = sum((owner["positionFt"][i] - champ["positionFt"][i]) ** 2 for i in range(3)) ** 0.5
        owner["turnState"]["bonusActionAvailable"] = False
        owner["turnState"]["companionCommandAllowanceAvailable"] = False
        owner["companionCommandUse"] = {"roundBoundarySeconds": 6, "companionId": CHAMPION_ID,
                                         "distanceFt": distance, "rangeFt": 60, "perceivesCompanion": True,
                                         "lineOfEffectClear": True, "ownerConscious": True,
                                         "globalAllowanceAvailable": True, "globalAllowanceUsedOnce": True,
                                         "orderedAfterOwnerTurnStart": True,
                                         "command": "move up to Speed and use one damaging/control action"}
        champ["turnState"]["commandedForPhase"] = True
        s["eventReceipts"]["W08-E22-COMPANION-COMMAND"] = copy.deepcopy(owner["companionCommandUse"])
    emit("W08-E22-COMPANION-COMMAND", 6, "companion-command",
         "The conscious owner spends its Bonus Action and the once-per-Mage-turn global command allowance; perception, 5-foot distance and clear line of effect are recorded before movement.",
         issue_command, [mage_source + "/9", fc_spell_pointer, "sources/COMBAT_ACTION_PLAYTEST.md#lines-31-41"])
    emit_turn("championOwner", 6, "cargo-crossing round", False, "W08-E23-OWNER-END-T06")

    def commanded_phase_start(s: dict[str, Any]) -> None:
        owner = s["actors"]["championOwner"]
        champ = s["actors"]["champion"]
        assert owner["turnState"]["active"] is False
        assert owner["companionCommandUse"]["globalAllowanceUsedOnce"]
        champ["movement"].update({"budgetFt": 30, "spentFt": 0, "remainingFt": 30, "expiredUnusedFt": 0})
        champ["turnState"]["attachedPhase"] = {"phaseId": "CHAMPION-COMMANDED-06", "active": True,
                                                     "commanded": True, "actionAvailable": True,
                                                     "movementAvailableFt": 30, "ownerWholeTurnEnded": True,
                                                     "ownerActionAvailable": False, "ownerBonusActionAvailable": False}
        s["eventReceipts"]["W08-E24-ATTACHED-PHASE-START"] = {
            "ownerTurnEndedFirst": True, "ownerActionConsumed": True, "ownerBonusActionConsumed": True,
            "commandAllowanceUsedOnce": True, "championPhaseStarted": True, "movementAllowanceFt": 30}
    emit("W08-E24-ATTACHED-PHASE-START", 6, "commanded-companion-phase-start",
         "Only after the owner's complete turn ends does the attached Champion movement/action phase begin, with one 30-foot allowance and one commanded action.",
         commanded_phase_start, [mage_source + "/9", fc_spell_pointer, "sources/COMBAT_ACTION_PLAYTEST.md#lines-31-41"])

    def cross_gate(s: dict[str, Any]) -> None:
        gate = s["gate"]
        champ = s["actors"]["champion"]
        item = s["objects"][ITEM_ID]
        start = [85, 100, 0]
        end = [105, 100, 0]
        champ["movement"].update({"spentFt": 20, "remainingFt": 10})
        champ["movementHistory"].append({"atSeconds": 6, "phaseId": "CHAMPION-COMMANDED-06",
                                          "movementSpentFt": 20, "movementBudgetFt": 30,
                                          "remainingBeforePhaseEndFt": 10,
                                          "status": "historical expenditure; not current phase ledger"})
        champ["positionFt"] = [0, 0, 0]
        champ["planeKey"] = CELL_ID
        cell_bounds = {"min": [-7.5, -7.5, 0], "max": [7.5, 7.5, 15]}
        body_local = {"min": [-2.5, -2.5, 0], "max": [2.5, 2.5, 6]}
        cargo_local = {"centerFt": [2, 0, 3], "sizeFt": [0.5, 0.5, 0.5],
                       "aabbFt": {"min": [1.75, -0.25, 2.75], "max": [2.25, 0.25, 3.25]}}
        s["cell"] = {
            "id": CELL_ID, "status": "active", "primaryId": CHAMPION_ID,
            "admittedAtSeconds": 6, "deadlineSeconds": 66, "deadlineRule": "Gate admission + 60 seconds",
            "originPlaneKey": ORIGIN,
            "originAnchor": {"worldFt": end, "orientation": 0, "fixedAtAdmission": True,
                             "anchorBasis": {"localXWorld": [1, 0, 0], "localYWorld": [0, 1, 0], "localZWorld": [0, 0, 1]}},
            "primaryCellLocalPosition": [0, 0, 0], "primaryBodyAabbFt": body_local,
            "contents": [CHAMPION_ID, ITEM_ID], "looseCargoIds": [], "closureCount": 0,
            "geometry": {"fixtureId": "BAN-CELL-03", "boundsFt": cell_bounds,
                         "floor": {"zFt": 0, "supported": True}, "bodyFits": True, "cargoFits": True,
                         "bodyEnvelopeAabbFt": body_local,
                         "admissionCargoEnvelopeAabbFt": copy.deepcopy(cargo_local["aabbFt"]),
                         "cargoEnvelopeAabbFt": copy.deepcopy(cargo_local["aabbFt"]),
                         "currentCargoEnvelopeAabbFt": copy.deepcopy(cargo_local["aabbFt"]),
                         "cargoGeometryStage": "admitted-carried-lantern"},
            "endpointBlocker": None,
        }
        gate["liveCellIds"].append(CELL_ID)
        gate["hardControlClaims"].append({"targetId": CHAMPION_ID, "encounterId": "encounter-w08-test-01",
                                         "claimedAtSeconds": 6})
        item["physicalPosition"] = {"planeKey": CELL_ID, "cellLocalFt": [2, 0, 3],
                                    "carriedSlot": "left hand", "carrierId": CHAMPION_ID,
                                    "carrierOffsetFt": [2, 0, 3], "volumeFt": [0.5, 0.5, 0.5]}
        item["status"] = "carried-in-gate-cell"
        champ["externalObjectIds"] = [ITEM_ID]
        champ["hands"]["left"] = ITEM_ID
        gate_world = s["world"]["gateWorldPose"]
        s["eventReceipts"]["W08-E26-GATE-CROSSING"] = {
            "crossingId": "crossing-w08-001", "admitted": True, "sameChampionId": CHAMPION_ID,
            "selectedGateType": gate["selectedCreatureType"], "creatureType": "Humanoid", "cellId": CELL_ID,
            "movementFt": 20, "remainingMovementBeforePhaseEndFt": 10, "cellDeadlineSeconds": 66,
            "worldPathStartFt": start, "worldPathEndFt": end, "actualAdmissionPoseFt": end,
            "fixedOriginAnchorFt": end, "gatePlaneXFt": gate_world["portalPlaneXFt"],
            "completeBodyStartXBoundsFt": [82.5, 87.5], "completeBodyEndXBoundsFt": [102.5, 107.5],
            "portalYBoundsFt": [95, 105], "portalZBoundsFt": [0, 15],
            "bodySweepYBoundsFt": [97.5, 102.5], "bodySweepZBoundsFt": [0, 6],
            "lanternWorldCenterStartFt": [87, 100, 3], "lanternWorldCenterEndFt": [107, 100, 3],
            "lanternEndAabbFt": {"min": [106.75, 99.75, 2.75], "max": [107.25, 100.25, 3.25]},
            "portalWidthClearance": True, "portalHeightClearance": True,
            "bodyFullyCrossedAtEndpoint": True, "cargoFullyCrossedAtEndpoint": True,
            "bodyAabbInCell": body_local, "cargoCellLocal": cargo_local,
            "cellBoundsFt": cell_bounds, "bodyAndCargoInsideBAN_CELL_03": True,
            "ownerMovementSpentFt": 0, "ownerWholeTurnEndedBeforePhase": True,
            "gateAperture": {"widthFt": 10, "heightFt": 15,
                             "sourcePointer": "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json#/source/coreEntries/0/original"},
        }
    emit("W08-E26-GATE-CROSSING", 6, "matching-humanoid-gate-admission",
         "The commanded Champion completes a 20-foot whole-body and cargo sweep through the separately cast Humanoid Gate; the cell snapshots the actual [105,100,0] admission pose and numeric BAN-CELL-03 bounds.",
         cross_gate, ["sources/RETURN327_banishment-gate.json#/procedure",
                      "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension",
                      "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/originPlane",
                      *body_sources, fc_spell_pointer], labels=["PG9-Q15", "PG9-Q17", "PG9-Q29"])

    def commanded_phase_end(s: dict[str, Any]) -> None:
        champ = s["actors"]["champion"]
        phase = champ["turnState"]["attachedPhase"]
        unused = champ["movement"]["remainingFt"]
        phase.update({"active": False, "actionAvailable": False,
                      "commandedActionStatus": "unused-expired-at-phase-end",
                      "movementExpiredFt": unused,
                      "ownerWholeTurnEnded": True, "phaseEndedAfterAdmission": True})
        champ["movement"]["expiredUnusedFt"] = unused
        champ["movement"]["remainingFt"] = 0
        champ["turnState"]["attachedPhase"] = phase
        s["eventReceipts"]["W08-E27-ATTACHED-PHASE-END"] = {
            "movementSpentFt": 20, "movementBudgetFt": 30, "unusedMovementExpiredFt": unused,
            "commandedActionCount": 0, "commandedActionDisposition": "unused; expired at phase end",
            "noDamageOrWoundBranch": True, "phaseEnded": True}
    emit("W08-E27-ATTACHED-PHASE-END", 6, "commanded-companion-phase-end",
         "The attached phase ends after admission; no damaging action or training target is introduced, and the commanded Action and unused 10 feet expire immediately.",
         commanded_phase_end, [mage_source + "/9"])

    # Replay each scheduled Mage start/end and the resulting uncommanded stance
    # through 54 seconds. Every turn allowance refreshes once and expires once.
    for round_time in range(12, 60, 6):
        suffix = f"T{round_time:02d}"
        emit_turn("gateCaster", round_time, "ordinary six-second round", True, f"W08-SCHEDULE-GATECASTER-START-{suffix}")
        emit_turn("gateCaster", round_time, "ordinary six-second round", False, f"W08-SCHEDULE-GATECASTER-END-{suffix}")
        emit_turn("championOwner", round_time, "ordinary six-second round", True, f"W08-SCHEDULE-OWNER-START-{suffix}")
        emit_turn("championOwner", round_time, "ordinary six-second round", False, f"W08-SCHEDULE-OWNER-END-{suffix}")
        def stance(s: dict[str, Any], t: int = round_time) -> None:
            champ = s["actors"]["champion"]
            owner = s["actors"]["championOwner"]
            assert champ["exists"] and owner["turnState"]["active"] is False
            s["eventReceipts"][f"COMPANION-STANCE-{t}"] = {
                "ownerTurnEndedFirst": True, "commanded": False, "decision": "Dodge",
                "movementDecision": "remain in cell; do not cross or alter Gate state",
                "withinCell": True, "damageOrControl": False, "commandAllowanceExpired": True}
            champ["movement"].update({"budgetFt": 30, "spentFt": 0, "remainingFt": 30, "expiredUnusedFt": 0})
            champ["turnState"]["attachedPhase"] = {"phaseId": f"CHAMPION-UNCOMMANDED-{t}",
                "active": False, "commanded": False, "stanceResolved": "Dodge", "ownerWholeTurnEnded": True,
                "movementSpentFt": 0, "movementExpiredFt": 30, "noDamageOrControl": True}
            champ["movement"]["expiredUnusedFt"] = 30
            champ["movement"]["remainingFt"] = 0
        emit(f"W08-SCHEDULE-CHAMPION-STANCE-{suffix}", round_time, "uncommanded-companion-stance",
             "The live but uncommanded Champion stays within its cell and chooses only Dodge after the owner's turn; no movement, damage, or control occurs and unused movement expires.",
             stance, [mage_source + "/9"])

    def expire_champion(s: dict[str, Any]) -> None:
        champ = s["actors"]["champion"]
        owner = s["actors"]["championOwner"]
        cell = s["cell"]
        item = s["objects"][ITEM_ID]
        assert champ["exists"] and champ["sourceDeadlineSeconds"] == 60
        assert cell["status"] == "active" and cell["deadlineSeconds"] == 66
        cell["contents"].remove(CHAMPION_ID)
        cell["looseCargoIds"] = [ITEM_ID]
        item["custodianId"] = None
        item["status"] = "loose-genuine-cargo-in-cell"
        item["physicalPosition"] = {"planeKey": CELL_ID, "cellLocalFt": [2, 0, 0.25],
                                    "carrierId": None, "carriedSlot": None, "volumeFt": [0.5, 0.5, 0.5],
                                    "support": {"surface": "BAN-CELL-03 floor", "zFt": 0},
                                    "droppedFromCellLocalFt": [2, 0, 3], "droppedAtSeconds": 60}
        dropped_aabb = {"min": [1.75, -0.25, 0], "max": [2.25, 0.25, 0.5]}
        cell["geometry"]["cargoEnvelopeAabbFt"] = copy.deepcopy(dropped_aabb)
        cell["geometry"]["currentCargoEnvelopeAabbFt"] = copy.deepcopy(dropped_aabb)
        cell["geometry"]["cargoGeometryStage"] = "loose-lantern-on-cell-floor-after-source-expiry"
        champ.update({"exists": False, "bodyState": "expired", "sourceEndReason": "original finite-source deadline",
                      "corpseExists": False, "intrinsicManifestation": {"status": "vanished", "items": [],
                          "separateInventoryObjects": False}, "externalObjectIds": [],
                      "hands": {"left": "none; body ended", "right": "none; body ended"},
                      "turnState": {"attachedPhase": None}})
        owner["concentration"] = {"effectId": "faction-champion-w08-source", "active": False,
                                  "endedAtSeconds": 60, "endReason": "source deadline"}
        s["eventReceipts"]["W08-E28-CHAMPION-SOURCE-EXPIRY"] = {
            "mandatorySourceExpiryAtSeconds": 60, "resolvedBeforeSimultaneousRegularStarts": True,
            "bodyRemoved": True, "intrinsicGearRemoved": True, "corpseCreated": False,
            "sameGenuineLanternPersists": True, "itemId": ITEM_ID, "quantity": 1,
            "releasedFromCarrierOffsetFt": [2, 0, 3], "settledCellLocalFt": [2, 0, 0.25],
            "droppedCargoEnvelopeAabbFt": dropped_aabb,
            "admissionCargoEnvelopePreservedAsHistory": cell["geometry"]["admissionCargoEnvelopeAabbFt"],
            "latestMovementLedgerPreserved": copy.deepcopy(champ["movement"]),
            "historicalMovementExpenditure": copy.deepcopy(champ["movementHistory"]),
            "cellRemainsActiveUntil": 66, "gateRemainsActive": True,
        }
    emit("W08-E28-CHAMPION-SOURCE-EXPIRY", 60, "finite-source-expiry",
         "The original 60-second Champion source expires before any same-time regular-turn start: body and intrinsic gear vanish, no corpse is created, and the same lantern falls to the cell floor at its mapped local position.",
         expire_champion, ["sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-FACTION-CHAMPION-01",
                           "sources/AC5_ACCEPTED_CASEBOOK.json#/cases/0",
                           "sources/RETURN327_banishment-gate.json#/sharedContract/cellExtension/closure/deathAndRemoval",
                           *body_sources], labels=["PG9-Q15", "PG9-Q29"])
    emit_turn("gateCaster", 60, "source-expiry boundary", True, "W08-SCHEDULE-GATECASTER-START-T60")
    emit_turn("gateCaster", 60, "source-expiry boundary", False, "W08-SCHEDULE-GATECASTER-END-T60")
    emit_turn("championOwner", 60, "source-expiry boundary", True, "W08-SCHEDULE-OWNER-START-T60")
    emit_turn("championOwner", 60, "source-expiry boundary", False, "W08-SCHEDULE-OWNER-END-T60")

    common = {
        "initialState": initial,
        "initialStateSha256": state_hash(initial),
        "events": events,
        "finalState": state,
        "finalStateSha256": state_hash(state),
    }
    return state, events, common

def main() -> None:
    # The original packet assembler calls the current replacement builders above.
    _V01_MAIN()
    _finalize_repack03()


if __name__ == "__main__":
    main()
