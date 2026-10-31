from __future__ import annotations

import copy
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
W08 = HERE / "banishment_gate_witness365_w08_finite_cargo04_build02"
OUT = HERE / "banishment_gate_witness365_w05_separation365_repack01_build01"
PACKET = OUT / "packet"
PINNED_SOURCE_COMMIT = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
CURRENT_REPO_COMMIT = "c4772af0"
ARCHIVE_NAME = "DD_Rank9_BanishmentGate_W05_CarriedBodies_365_TESTONLY_REPACK01.zip"
ORIGIN = "PLANE-W05-TEST-ORIGIN-01"


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


def apply(state: Any, ops: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in ops:
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


def event(events: list[dict[str, Any]], state: dict[str, Any], event_id: str, t: float,
          kind: str, description: str, mutate: Callable[[dict[str, Any]], None],
          source_refs: list[str], sequence: int | None = None) -> dict[str, Any]:
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    after["elapsedSeconds"] = t
    mutate(after)
    forward = deep_diff(before, after)
    inverse = list(reversed(deep_diff(after, before)))
    assert apply(before, forward) == after
    assert apply(after, inverse) == before
    record = {
        "eventId": event_id,
        "timestampSeconds": t,
        "kind": kind,
        "description": description,
        "sourceRefs": source_refs,
        "beforeStateSha256": state_sha(before),
        "afterStateSha256": state_sha(after),
        "forwardOperations": forward,
        "inverseOperations": inverse,
        "stateAfter": after,
    }
    if sequence is not None:
        record["sequenceAtTimestamp"] = sequence
    events.append(record)
    return after


def get_member(filename: str) -> bytes:
    return (W08 / "packet" / filename).read_bytes()


def copy_member(filename: str, destination: str, provenance: str,
                json_pointers: list[str] | None = None, source_commit: str | None = PINNED_SOURCE_COMMIT) -> dict[str, Any]:
    data = get_member(filename)
    target = PACKET / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {
        "member": destination,
        "bytes": len(data),
        "sha256": sha(data),
        "provenance": provenance,
        "sourceCommit": source_commit,
        "jsonPointers": json_pointers or [],
    }


def setup_sources() -> dict[str, Any]:
    if OUT.exists():
        shutil.rmtree(OUT)
    PACKET.mkdir(parents=True)
    bindings: list[dict[str, Any]] = []
    source_files = [
        ("sources/RETURN327_banishment-gate.json", "sources/RETURN327_banishment-gate.json", "Return327 source authority", ["/procedure", "/sharedContract/cellExtension"]),
        ("sources/AC5_ACCEPTED_SPELLS_MODEL.json", "sources/AC5_ACCEPTED_SPELLS_MODEL.json", "accepted AC5 spell/profile source; comparison scope remains narrow", ["/profiles/AC5-PROFILE-GREATER-FIRE-PET-01", "/profiles/AC5-PROFILE-FACTION-CHAMPION-01"]),
        ("sources/AC5_ACCEPTED_CASEBOOK.json", "sources/AC5_ACCEPTED_CASEBOOK.json", "accepted AC5 casebook; AC5-X17 is comparison precedent only", ["/cases/38"]),
        ("sources/MAGE_CLASS_PLAYTEST.json", "sources/MAGE_CLASS_PLAYTEST.json", "Mage spell acquisition and class resources", []),
        ("sources/W08_CASTER_PROFILES_365_TESTONLY.json", "sources/W05_CASTER_PROFILE_SEEDS_365_TESTONLY.json", "sealed W08 caster records used as transparent fixture templates", []),
        ("rules/BODY_EQUIPMENT.md", "rules/BODY_EQUIPMENT.md", "pinned physical carrying and casualty-load procedure", []),
        ("W08_SOURCE_BINDINGS_365.json", "authority/W08_SOURCE_BINDINGS_365.json", "prior source-binding ledger", []),
        ("authority/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json", "authority/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json", "AC5 accepted-scope receipt", []),
        ("authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json", "authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json", "unchanged native catalog card and school conflict record", []),
        ("authority/CURRENT_SPELL_QUEUE_361.json", "authority/CURRENT_SPELL_QUEUE_361.json", "current queue authority preserved from W08 review", []),
        ("authority/PG327_W01_W08_WITNESS_PLAN_361.json", "authority/PG327_W01_W08_WITNESS_PLAN_361.json", "Director witness minimum", []),
        ("authority/PG327_W01_DIRECTOR_SEAL_365_REPACK04.json", "authority/PG327_W01_DIRECTOR_SEAL_365_REPACK04.json", "prior W01 sealed witness", []),
        ("authority/PG327_W08_DIRECTOR_HOLD_365_REPACK03.json", "authority/PG327_W08_DIRECTOR_HOLD_365_REPACK03.json", "prior W08 R3 hold; retained as history", []),
    ]
    for source, dest, provenance, pointers in source_files:
        bindings.append(copy_member(source, dest, provenance, pointers))
    seal_path = HERE / "PG327_W08_DIRECTOR_SEAL_365_REPACK04.json"
    seal_data = seal_path.read_bytes()
    (PACKET / "authority" / seal_path.name).write_bytes(seal_data)
    bindings.append({"member": f"authority/{seal_path.name}", "bytes": len(seal_data), "sha256": sha(seal_data),
                     "provenance": "Director W08 REPACK04 seal, saved from the current GPT Director response",
                     "sourceCommit": CURRENT_REPO_COMMIT, "jsonPointers": ["/rulingId", "/witnessDisposition", "/nextWitness"]})
    return {"id": "PG327-W05-SOURCE-BINDINGS-365-REPACK01", "sourceCommit": PINNED_SOURCE_COMMIT,
            "bindings": bindings, "fixtureBoundary": "All W05 body placement, support geometry, relationship permissions and release-lock conditions are declared TEST_ONLY premises; they are not promoted to canonical body anatomy or campaign history."}


def source_data() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    ac5 = load_json(PACKET / "sources" / "AC5_ACCEPTED_SPELLS_MODEL.json")
    casebook = load_json(PACKET / "sources" / "AC5_ACCEPTED_CASEBOOK.json")
    gate = load_json(PACKET / "sources" / "RETURN327_banishment-gate.json")
    fire_idx = next(i for i, item in enumerate(ac5["spells"]) if item["id"] == "summon-greater-fire-pet")
    champ_idx = next(i for i, item in enumerate(ac5["spells"]) if item["id"] == "faction-champion")
    x17_idx = next(i for i, item in enumerate(casebook["cases"]) if item["id"] == "AC5-X17")
    q17 = gate["procedure"].split("PG9-Q17", 1)[1].split("PG9-Q29", 1)[0]
    refs = {
        "gateRule": "sources/RETURN327_banishment-gate.json#/procedure (PG9-Q01, PG9-Q13, PG9-Q14, PG9-Q16, PG9-Q17)",
        "firePetSpell": f"sources/AC5_ACCEPTED_SPELLS_MODEL.json#/spells/{fire_idx}",
        "firePetProfile": "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01",
        "championSpell": f"sources/AC5_ACCEPTED_SPELLS_MODEL.json#/spells/{champ_idx}",
        "championProfile": "sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-FACTION-CHAMPION-01",
        "carryingRule": "rules/BODY_EQUIPMENT.md#lines-94-109",
        "ac5Precedent": f"sources/AC5_ACCEPTED_CASEBOOK.json#/cases/{x17_idx} (AC5-X17; comparison only, no AC5-BANISH-EXT mechanics imported)",
    }
    assert "separate living passengers" in q17
    return ac5, casebook, refs


def mage_profiles(seeds: dict[str, Any]) -> dict[str, Any]:
    gate_seed, champion_seed = seeds["profiles"]
    fire_owner = copy.deepcopy(champion_seed)
    fire_owner["profileId"] = "W05-MAGE9-FIREPET-OWNER-TESTONLY"
    fire_owner["actorId"] = "actor-w05-firepet-owner"
    fire_owner["concentrationBeforeFirePet"] = None
    fire_owner["spellbookHistory"] = [
        {"spellId": "mage.arch.counterspell", "kind": "Mage class card", "acquiredAtMageLevel": 9,
         "preparedForWitness": True, "sourcePointer": "/cards/23"},
        {"spellId": "summon-greater-fire-pet", "kind": "accepted AC5 ordinary Mage spell", "acquiredAtMageLevel": 9,
         "preparedForWitness": True, "sourceAccess": {"rank": 5, "minimumClassLevel": 9,
         "school": "Conjuration", "baseRpCost": 10}, "acquisitionFact": "explicit TEST_ONLY spellbook history; pinned AC5 source confirms class access"},
    ]
    champion = copy.deepcopy(champion_seed)
    champion["profileId"] = "W05-MAGE9-CHAMPION-OWNER-TESTONLY"
    champion["actorId"] = "actor-w05-champion-owner"
    gate = copy.deepcopy(gate_seed)
    gate["profileId"] = "W05-MAGE17-GATECASTER-TESTONLY"
    gate["actorId"] = "actor-w05-gate-caster"
    return {"id": "W05-MAGE-PROFILES-365-TESTONLY", "evidenceClass": "conditional TEST_ONLY actor profiles copied/adapted from pinned Mage records",
            "profiles": [fire_owner, champion, gate], "noCampaignActors": True}


def initial_state(profiles: dict[str, Any]) -> dict[str, Any]:
    owners = {}
    for p in profiles["profiles"]:
        owners[p["actorId"]] = {
            "id": p["actorId"], "profileId": p["profileId"], "class": p["class"], "classLevel": p["classLevel"],
            "abilityScores": p["abilityScores"], "rp": {"maximum": p["derived"]["RPMaximum"], "current": p["derived"]["RPMaximum"], "spent": 0},
            "concentration": None, "actionBudget": {"action": "available", "bonusAction": "available", "reaction": "available"},
            "conditions": [], "conscious": True, "incapacitated": False, "silenced": False,
            "acquiredAndPreparedSpells": [x["spellId"] for x in p.get("spellbookHistory", [])],
            "testPositionFt": [-50, 0, 0] if p["actorId"] == "actor-w05-gate-caster" else [-20, 0, 0],
        }
    return {
        "simulationId": "PG327-W05-365-TESTONLY-CARRIAGE",
        "evidenceClass": "conditional TEST_ONLY static authored witness; no campaign event asserted",
        "elapsedSeconds": -24,
        "world": {"originPlaneKey": ORIGIN, "portal": None, "encounterId": "ENCOUNTER-W05-TEST-01",
                  "perceivedClearPortalCreationSpace": True, "originWorldGeometryFixtureOnly": True},
        "mageActors": owners,
        "actors": {},
        "gate": None,
        "carriageRelation": None,
        "cells": {},
        "hardControlClaims": {},
        "objects": {},
        "testFixtureBoundaries": ["No canonical creature anatomy, living-body-as-gear rule, campaign event or runtime behavior is asserted.",
                                   "The contact support, box dimensions, permissions and release/locked relationship are authored fixture inputs only."],
    }


def build_common(ac5: dict[str, Any], refs: dict[str, str], profiles: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    fire_spell = next(x for x in ac5["spells"] if x["id"] == "summon-greater-fire-pet")
    champ_spell = next(x for x in ac5["spells"] if x["id"] == "faction-champion")
    fire_profile = ac5["profiles"]["AC5-PROFILE-GREATER-FIRE-PET-01"]
    champ_profile = ac5["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    state = initial_state(profiles)
    events: list[dict[str, Any]] = []
    sources = [refs["firePetSpell"], refs["firePetProfile"], "sources/MAGE_CLASS_PLAYTEST.json"]

    def cast_fire(s: dict[str, Any]) -> None:
        owner = s["mageActors"]["actor-w05-firepet-owner"]
        owner["rp"].update(current=16, spent=10)
        owner["concentration"] = {"spellId": "summon-greater-fire-pet", "startedAt": -18, "deadline": 42}
        s["actors"]["actor-w05-firepet"] = {"id": "actor-w05-firepet", "sourceProfileId": fire_profile["id"],
            "controllerId": "actor-w05-firepet-owner", "size": fire_profile["size"], "creatureType": fire_profile["creatureType"],
            "weightLb": fire_profile["weightLb"], "hp": fire_profile["hpMax"], "ac": fire_profile["ac"], "speedFt": fire_profile["speedFt"],
            "abilities": fire_profile["abilities"], "alive": True, "isGear": False, "physicalPosition": {"planeKey": ORIGIN, "centerFt": [-5, 0, 3], "bodyBoxFt": [[-7.5,-2.5],[ -2.5,2.5],[0,6]]},
            "sourceLifecycle": {"spellId": "summon-greater-fire-pet", "beganAt": -18, "deadline": 42, "endsAtDeadline": True},
            "inventoryObjectIds": [], "movementFeetAvailable": 30, "commandedMove": False}
        s["elapsedSeconds"] = -18
    state = event(events, state, "W05-E01-FIREPET-SUMMON", -18, "accepted-finite-summon-cast",
                  "Mage level 9 completes the accepted Summon Greater Fire Pet Action, spends 10 RP and creates the complete source-bound Medium Elemental profile; the one-minute source deadline is 42 seconds.",
                  cast_fire, sources)
    events[-1]["actionWindowSeconds"] = [-24, -18]

    def cast_champion(s: dict[str, Any]) -> None:
        owner = s["mageActors"]["actor-w05-champion-owner"]
        owner["rp"].update(current=16, spent=10)
        owner["concentration"] = {"spellId": "faction-champion", "startedAt": -12, "deadline": 48}
        s["actors"]["actor-w05-champion"] = {"id": "actor-w05-champion", "sourceProfileId": champ_profile["id"],
            "controllerId": "actor-w05-champion-owner", "size": champ_profile["size"], "creatureType": champ_profile["creatureType"],
            "weightLb": champ_profile["weightLb"], "hp": champ_profile["hpMax"], "ac": champ_profile["ac"], "speedFt": champ_profile["speedFt"],
            "abilities": champ_profile["abilities"], "alive": True, "isGear": False, "physicalPosition": {"planeKey": ORIGIN, "centerFt": [-5,0,9.5], "bodyBoxFt":[[-7.5,-2.5],[-2.5,2.5],[6.5,12.5]]},
            "sourceLifecycle": {"spellId":"faction-champion","beganAt":-12,"deadline":48,"endsAtDeadline":True},
            "intrinsicGearIsNotInventory": True, "inventoryObjectIds": [], "movementFeetAvailable": 30}
        owner["factionEligibility"] = {"factionId":"FACTION-W05-TEST-01","alliedStatus":True,"currentStanding":3,
            "invocationPermission":True,"aidProhibition":False,"membershipInferred":False}
        s["elapsedSeconds"] = -12
    state = event(events, state, "W05-E02-CHAMPION-SUMMON", -12, "accepted-finite-summon-cast",
                  "A distinct Mage level 9 completes Faction Champion; its own concentration, faction eligibility, complete Medium Humanoid profile and 60-second deadline are recorded.",
                  cast_champion, [refs["championSpell"], refs["championProfile"], "sources/MAGE_CLASS_PLAYTEST.json"])
    events[-1]["actionWindowSeconds"] = [-18, -12]

    def cast_gate(s: dict[str, Any]) -> None:
        caster = s["mageActors"]["actor-w05-gate-caster"]
        caster["rp"].update(current=24, spent=26)
        caster["concentration"] = {"spellId":"banishment-gate","startedAt":-6,"deadline":594}
        s["gate"] = {"id":"gate-w05-001","creatorId":"actor-w05-gate-caster","sourceSpellId":"banishment-gate",
            "selectedCreatureType":"Elemental","selectedAtCreation":True,"active":True,"startedAt":-6,"deadline":594,
            "aperture":{"shape":"vertical rectangle","widthFt":10,"heightFt":15,"planeXFt":0,"yRangeFt":[-5,5],"zRangeFt":[0,15],"orientation":"plane normal +X"},
            "originPlaneKey":ORIGIN,"rangeFromCasterFt":50,"castPredicates":{"acquired":True,"prepared":True,"class":"Mage","classLevel":17,"school":"Conjuration","rank":9,"action":True,"rpSpent":26,"components":["V","S","F"],"clearPerceivedSpace":True,"within120Ft":True},
            "operativeSchoolSource":"sources/RETURN327_banishment-gate.json#/procedure (PG9-Q01)",
            "catalogMetadataConflict":{"catalogSchool":"Abjuration","operativeMageSchool":"Conjuration","catalogMember":"authority/CURRENT_BANISHMENT_GATE_CATALOG_CARD.json","catalogPreservedUnchanged":True},
            "admissions":[],"crossingReceipts":{}}
        s["elapsedSeconds"] = -6
    state = event(events, state, "W05-E03-GATE-CAST", -6, "banishment-gate-cast",
                  "Mage level 17 completes the lawful Gate Action, commits 26 RP and creates a fixed Elemental portal for 600 seconds. The two summons have separate owners, avoiding concentration overlap.",
                  cast_gate, [refs["gateRule"], "sources/W08_CASTER_PROFILES_365_TESTONLY.json"])
    events[-1]["actionWindowSeconds"] = [-12, -6]

    def attach_fixture(s: dict[str, Any]) -> None:
        s["carriageRelation"] = {"id":"W05-CARRY-RELATION-01","carrierId":"actor-w05-firepet","passengerId":"actor-w05-champion",
            "kind":"physical back-support; both remain separate living actor records","permission":{"carrierOwnerAllows":True,"passengerOwnerAllows":True,"passengerWilling":True},
            "sourceBodyGeometry":"TEST_ONLY articulated support fixture; AC5 profile does not establish anatomy",
            "supportGeometry":{"carrierBoxFt":[[-7.5,-2.5],[-2.5,2.5],[0,6]],"passengerBoxFt":[[-7.5,-2.5],[-2.5,2.5],[6.5,12.5]],"interbodyGapFt":0.5,"apertureClearance":{"xFt":10,"zFt":15,"bothBodiesFit":True}},
            "capacity":{"carrierSize":"Medium","carrierStrength":14,"physicalLimitLb":210,"passengerBodyAndAssociatedEquipmentLb":180,
                "carrierLoadCapacity":14,"passengerCasualtyLoad":6,"equipmentLoad":0,"capacityLoadUsed":6,"weightPass":True,"loadPass":True,
                "formulaSource":"BODY_EQUIPMENT.md lines 94-109; physical limit STR x 15 for Medium; casualty Load 6 for Medium"},
            "fixtureItemIds":[],"permissionToSeparate":"case-fork premise; both owners authorize a lawful release where available"}
    state = event(events, state, "W05-E04-TESTONLY-CARRIAGE-SETUP", -5.5, "test-fixture-carriage-initialization",
                  "Establish a consented, physically supported relationship between two distinct complete living bodies. Weight and Load both pass the pinned carrying rule. This morphology and support geometry are explicit TEST_ONLY premises, not campaign or canonical facts.",
                  attach_fixture, [refs["carryingRule"], refs["firePetProfile"], refs["championProfile"]])
    return state, events


def branch_legal(common_state: dict[str, Any], refs: dict[str, str]) -> dict[str, Any]:
    state = copy.deepcopy(common_state)
    events: list[dict[str, Any]] = []
    def allow_release(s: dict[str, Any]) -> None:
        s["carriageRelation"]["separation"] = {"possible":True,"method":"passenger voluntarily releases from fixture support and steps 5 ft laterally on origin side","requiresBodyHarm":False,"permissionGranted":True,"testOnlyPremise":True}
        s["elapsedSeconds"] = -5.25
    state = event(events,state,"W05-A01-SEPARATION-PRECHECK",-5.25,"lawful-separation-preflight",
        "Before any qualifying body crosses, the separate passenger uses 5 ft of its ordinary 30-ft movement to release from the carry relation and remains wholly outside the portal plane.",allow_release,
        [refs["gateRule"],refs["carryingRule"]],1)
    def detach(s: dict[str, Any]) -> None:
        s["actors"]["actor-w05-champion"]["physicalPosition"]={"planeKey":ORIGIN,"centerFt":[-10,0,3],"bodyBoxFt":[[-12.5,-7.5],[-2.5,2.5],[0,6]]}
        s["actors"]["actor-w05-champion"]["movementFeetAvailable"] = 25
        s["carriageRelation"].update(status="lawfully-separated-before-crossing",passengerId=None,carrierId="actor-w05-firepet")
        s["elapsedSeconds"] = -5.0
    state=event(events,state,"W05-A02-PASSENGER-RELEASES-AT-ORIGIN",-5.0,"passenger-ordinary-movement-separation",
        "The passenger is a living actor, not gear. It remains on the origin plane at x=-10; the body boxes are disjoint and do not overlap the Gate plane.",detach,
        [refs["gateRule"],refs["carryingRule"]],2)
    def command(s: dict[str, Any]) -> None:
        owner=s["mageActors"]["actor-w05-firepet-owner"]
        owner["actionBudget"]["bonusAction"]="spent-on-command"
        s["actors"]["actor-w05-firepet"]["commandedMove"]=True
        s["actors"]["actor-w05-firepet"]["movementCommand"]={"ownerId":owner["id"],"kind":"Move","authorized":True}
        s["elapsedSeconds"]=-4.75
    state=event(events,state,"W05-A03-OWNER-COMMANDS-CARRIER",-4.75,"companion-move-command",
        "The Fire Pet owner uses its actual Bonus Action to authorize the carrier's Move; the command is consumed once.",command,
        ["sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01/command","sources/MAGE_CLASS_PLAYTEST.json"],3)
    def admit(s: dict[str, Any]) -> None:
        pet=s["actors"]["actor-w05-firepet"]
        pet["physicalPosition"]={"planeKey":"CELL-W05-LAWFUL-PRIMARY-01","cellLocalFt":[0,0,0],"bodyBoxFt":[[-2.5,2.5],[-2.5,2.5],[0,6]]}
        pet["movementFeetAvailable"] = 20
        s["cells"]["CELL-W05-LAWFUL-PRIMARY-01"]={"id":"CELL-W05-LAWFUL-PRIMARY-01","primaryId":"actor-w05-firepet","createdByGateId":"gate-w05-001",
            "openedAtSeconds":-4.5,"deadlineSeconds":55.5,"live":True,"secondaryBodies":[],"originAnchor":{"planeKey":ORIGIN,"bodyOriginCenterFt":[-5,0,3]},
            "geometry":{"xFt":[-7.5,7.5],"yFt":[-7.5,7.5],"zFt":[0,15],"bodyContained":True}}
        s["gate"]["admissions"].append({"primaryId":"actor-w05-firepet","admitted":True,"passengerIds":[],"cellId":"CELL-W05-LAWFUL-PRIMARY-01"})
        s["gate"]["crossingReceipts"]["W05-CROSSING-LAWFUL-SEP-001"]={"result":"admitted-primary-only","primaryId":"actor-w05-firepet","passengerId":"actor-w05-champion","passengerAtOrigin":True,"claimSpent":True,"cellId":"CELL-W05-LAWFUL-PRIMARY-01"}
        s["hardControlClaims"]["claim-w05-firepet-001"]={"sourceCharacterId":"actor-w05-gate-caster","targetId":"actor-w05-firepet","encounterId":"ENCOUNTER-W05-TEST-01","reservedOnSuccessfulEstablishment":True,"crossingId":"W05-CROSSING-LAWFUL-SEP-001"}
        s["elapsedSeconds"]=-4.5
    state=event(events,state,"W05-A04-PRIMARY-CROSSES-AND-ADMITS",-4.5,"lawful-primary-only-gate-admission",
        "The Elemental Fire Pet alone crosses and receives one cell. The Humanoid passenger remains on the origin plane; it is not cargo and receives no cell.",admit,
        [refs["gateRule"],refs["firePetProfile"],refs["championProfile"]],4)
    return {"id":"W05-LAWFUL-SEPARATION","outcome":"primary admitted; passenger remains at origin","forkPremise":{"separationPossible":True,"why":"the consenting passenger can lawfully release before the Gate plane"},
            "events":events,"finalState":state,"reverseOrder":[e["eventId"] for e in reversed(events)]}


def branch_impossible(common_state: dict[str, Any], refs: dict[str, str]) -> dict[str, Any]:
    state=copy.deepcopy(common_state)
    events: list[dict[str,Any]]=[]
    def lock_relation(s:dict[str,Any])->None:
        s["carriageRelation"]["separation"]={"possible":False,"method":"one-piece TEST_ONLY body-support coupling; no ordinary release path exists","requiresBodyHarm":True,
            "permissionGranted":True,"whyImpossible":"the only separating operation would harm one of the living bodies; no such operation is performed","testOnlyPremise":True}
        s["elapsedSeconds"]=-5.25
    state=event(events,state,"W05-B01-LOCKED-RELATION-PREMISE",-5.25,"test-fixture-impossible-separation-premise",
        "Alternative TEST_ONLY geometry uses a one-piece support coupling with no lawful non-destructive release. Consent and permission remain recorded; impossibility is physical, not a campaign fact or a magical exception.",lock_relation,
        [refs["gateRule"],refs["carryingRule"]],1)
    def command(s:dict[str,Any])->None:
        owner=s["mageActors"]["actor-w05-firepet-owner"]
        owner["actionBudget"]["bonusAction"]="spent-on-command"
        s["actors"]["actor-w05-firepet"]["commandedMove"]=True
        s["actors"]["actor-w05-firepet"]["movementCommand"]={"ownerId":owner["id"],"kind":"Move","authorized":True}
        s["elapsedSeconds"]=-5.0
    state=event(events,state,"W05-B02-OWNER-COMMANDS-CARRIER",-5.0,"companion-move-command",
        "The Fire Pet owner authorizes one Move by Bonus Action; it does not authorize breaking the passenger/body coupling.",command,
        ["sources/AC5_ACCEPTED_SPELLS_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01/command","sources/MAGE_CLASS_PLAYTEST.json"],2)
    def fail_atomic(s:dict[str,Any])->None:
        pet=s["actors"]["actor-w05-firepet"]
        passenger=s["actors"]["actor-w05-champion"]
        pet["physicalPosition"]={"planeKey":ORIGIN,"centerFt":[5,0,3],"bodyBoxFt":[[2.5,7.5],[-2.5,2.5],[0,6]]}
        passenger["physicalPosition"]={"planeKey":ORIGIN,"centerFt":[5,0,9.5],"bodyBoxFt":[[2.5,7.5],[-2.5,2.5],[6.5,12.5]]}
        pet["movementFeetAvailable"]=20
        s["gate"]["crossingReceipts"]["W05-CROSSING-IMPOSSIBLE-SEP-001"]={"result":"atomic-exile-failure","primaryId":"actor-w05-firepet","passengerId":"actor-w05-champion",
            "reason":"separate living passenger cannot lawfully be separated","ordinaryMovementResolved":True,"bothRemainOnOriginPlane":True,"cellCreated":False,"claimSpent":False}
        s["gate"]["admissions"].append({"primaryId":"actor-w05-firepet","admitted":False,"reason":"atomic-separation-failure"})
        s["elapsedSeconds"]=-4.5
    state=event(events,state,"W05-B03-IMPOSSIBLE-SEPARATION-ATOMIC-FAILURE",-4.5,"atomic-exile-failure",
        "The movement group reaches the far side of the physical Gate plane by ordinary movement, but Banishment Gate creates no exile transition: both bodies remain on their origin plane, no cell or hard-control claim is created, and neither body becomes an object or gear.",fail_atomic,
        [refs["gateRule"],refs["carryingRule"]],3)
    return {"id":"W05-IMPOSSIBLE-SEPARATION","outcome":"atomic exile failure; both living bodies remain on origin plane","forkPremise":{"separationPossible":False,"why":"the only physical separation method would harm a living body"},
            "events":events,"finalState":state,"reverseOrder":[e["eventId"] for e in reversed(events)]}


def verify_case(case: dict[str, Any], refs: dict[str, str]) -> dict[str, Any]:
    prefix=case["commonPrefix"]
    state=copy.deepcopy(prefix["initialState"])
    all_times=[]
    for ev in prefix["events"]:
        assert ev["beforeStateSha256"]==state_sha(state)
        assert ev["timestampSeconds"]>=state["elapsedSeconds"]
        nxt=apply(state,ev["forwardOperations"])
        assert state_sha(nxt)==ev["afterStateSha256"]==state_sha(ev["stateAfter"])
        assert apply(nxt,ev["inverseOperations"])==state
        state=nxt; all_times.append(ev["timestampSeconds"])
    assert state==prefix["finalState"]
    results={}
    for fork in case["terminalForks"]:
        cur=copy.deepcopy(state)
        fork_times=[]
        for ev in fork["events"]:
            assert ev["beforeStateSha256"]==state_sha(cur)
            assert ev["timestampSeconds"]>=cur["elapsedSeconds"]
            nxt=apply(cur,ev["forwardOperations"])
            assert state_sha(nxt)==ev["afterStateSha256"]==state_sha(ev["stateAfter"])
            assert apply(nxt,ev["inverseOperations"])==cur
            cur=nxt; fork_times.append(ev["timestampSeconds"])
        assert cur==fork["finalState"]
        if fork["id"]=="W05-LAWFUL-SEPARATION":
            assert cur["actors"]["actor-w05-firepet"]["physicalPosition"]["planeKey"].startswith("CELL-")
            assert cur["actors"]["actor-w05-champion"]["physicalPosition"]["planeKey"]==ORIGIN
            assert len(cur["cells"])==1 and len(cur["hardControlClaims"])==1
            assert cur["gate"]["admissions"][-1]["passengerIds"]==[]
            assert not cur["actors"]["actor-w05-champion"]["isGear"]
            assert cur["actors"]["actor-w05-champion"]["id"] not in cur["objects"]
        else:
            assert len(cur["cells"])==0 and len(cur["hardControlClaims"])==0
            assert cur["actors"]["actor-w05-firepet"]["physicalPosition"]["planeKey"]==ORIGIN
            assert cur["actors"]["actor-w05-champion"]["physicalPosition"]["planeKey"]==ORIGIN
            assert cur["actors"]["actor-w05-firepet"]["alive"] and cur["actors"]["actor-w05-champion"]["alive"]
            assert not cur["actors"]["actor-w05-firepet"]["isGear"] and not cur["actors"]["actor-w05-champion"]["isGear"]
            assert "actor-w05-firepet" not in cur["objects"] and "actor-w05-champion" not in cur["objects"]
            assert cur["gate"]["crossingReceipts"]["W05-CROSSING-IMPOSSIBLE-SEP-001"]["claimSpent"] is False if "claimSpent" in cur["gate"]["crossingReceipts"]["W05-CROSSING-IMPOSSIBLE-SEP-001"] else True
        # Exact reverse order restores the common-prefix branch point.
        reverse=copy.deepcopy(cur)
        for ev in reversed(fork["events"]):
            assert state_sha(reverse)==ev["afterStateSha256"]
            reverse=apply(reverse,ev["inverseOperations"])
            assert state_sha(reverse)==ev["beforeStateSha256"]
        assert reverse==state
        results[fork["id"]]={"eventCount":len(fork["events"]),"forwardInverseExact":True,"finalStateSha256":state_sha(cur),"chronological":fork_times==sorted(fork_times)}
    assert case["identityDecision"]=={"decision":"HOLD","acceptedIds":[],"appliedIds":[],"applicationAuthorized":False}
    return {"commonEventCount":len(prefix["events"]),"branches":results,"gateIdentityStillHeld":True}


def main() -> None:
    bindings=setup_sources()
    write_json(PACKET/"W05_SOURCE_BINDINGS_365.json",bindings)
    seeds=load_json(PACKET/"sources"/"W05_CASTER_PROFILE_SEEDS_365_TESTONLY.json")
    profiles=mage_profiles(seeds)
    write_json(PACKET/"W05_MAGE_PROFILES_365_TESTONLY.json",profiles)
    ac5,casebook,refs=source_data()
    common,common_events=build_common(ac5,refs,profiles)
    coverage={"id":"W05-CASE-COVERAGE-365-REPACK01","witnessId":"W05","status":"TEST_ONLY_STATIC_WITNESS",
        "requiredEvidence":["two complete, source-bound living body records","lawful carrier/passenger permissions and consent","physical body support geometry","both pound and Load capacity checks","matching primary and nonmatching passenger type","lawful separation leaves passenger at origin","impossible separation fails exile atomically with no cell/claim/deletion/gear conversion"],
        "branches":["W05-LAWFUL-SEPARATION","W05-IMPOSSIBLE-SEPARATION"],"uncoveredCampaignFacts":True,"identityAcceptance":False,"applicationAuthorization":False}
    lawful=branch_legal(common,refs)
    impossible=branch_impossible(common,refs)
    case={"id":"W05-LIVING-BODY-CARRIAGE-365-TESTONLY-REPACK01","status":"DIRECTOR_REVIEW_PENDING_TEST_ONLY",
        "spellId":"banishment-gate","blockerId":"PG200-B04","witnessId":"W05","sourceCommit":PINNED_SOURCE_COMMIT,
        "notCampaign":True,"evidenceClass":"conditional TEST_ONLY static authored witness; no campaign event or runtime result asserted",
        "wholeIdentityGate":{"decision":"HOLD","blockerIds":["PG200-B03","PG200-B04"],"acceptedIds":[],"appliedIds":[],"applicationAuthorized":False},
        "applicationAuthorized":False,"acceptanceDecision":None,"selectedGateType":"Elemental",
        "primary":{"actorId":"actor-w05-firepet","creatureType":"Elemental","sourceProfileId":"AC5-PROFILE-GREATER-FIRE-PET-01"},
        "separatePassenger":{"actorId":"actor-w05-champion","creatureType":"Humanoid","sourceProfileId":"AC5-PROFILE-FACTION-CHAMPION-01","isGear":False},
        "sourceUse":{"gate":"Mage17 Conjuration rank9; explicit acquired/prepared spellbook record; 26 RP; Action; V/S/F; clear 10x15 portal within120ft; 600-second concentration",
            "firePet":"Mage9 Conjuration rank5; 10 RP; Action; V/S/F; concentration up to60s; complete Medium Elemental profile",
            "champion":"distinct Mage9 Conjuration rank5; 10 RP; Action; V/S/F; concentration up to60s; explicit alliance/standing/invocation permission and complete Medium Humanoid profile",
            "distinctOwnersAvoidConcentrationConflict":True,"sourceReferences":refs,
            "AC5-X17":"comparison only for the fact a separate living passenger is not gear; no AC5-BANISH-EXT spell effect or closure mechanic is imported"},
        "fixtureAssumptions":{"campaignOccurrence":False,"runtimeImplementation":False,"worldFacts":False,
            "bodyMorphology":"explicit TEST_ONLY articulated support surface; not inferred from AC5 profile",
            "supportClearance":"two 5x5x6 ft medium body boxes vertically separated by 0.5 ft fit the 10x15 ft portal; box dimensions are fixture premises",
            "capacity":"carrier STR14 / Medium physical limit210lb; passenger180lb and casualty Load6; total Load6; both checks pass per pinned BODY_EQUIPMENT rule",
            "permissions":"carrier owner authorizes; passenger owner authorizes; passenger willing; impossible branch changes only physical release feasibility, not consent",
            "noGearConversion":"both bodies remain actor records; neither is stored in inventory/object collection"},
        "timeModel":{"unit":"absolute elapsed seconds","roundIntervalSeconds":6,"castWindows":[
            {"actor":"actor-w05-firepet-owner","start":-24,"commit":-18},{"actor":"actor-w05-champion-owner","start":-18,"commit":-12},{"actor":"actor-w05-gate-caster","start":-12,"commit":-6}],
            "firePetDeadline":42,"championDeadline":48,"gateDeadline":594,"allTimesMonotone":True,
            "branchWindow":{"from":-5.5,"to":-4.5,"withinAllSourceDeadlines":True,"sequentialEvents":True}},
        "commonPrefix":{"initialState":initial_state(profiles),"events":common_events,"finalState":common},
        "terminalForks":[lawful,impossible],
        "comparisonBoundary":{"sourceCaseId":"AC5-X17","use":"passenger remains a separate body, not cargo","notUsed":["AC5-BANISH-EXT","ordinary Banishment terminal closure","AC5 endpoint blocker exception"]},
        "identityDecision":{"decision":"HOLD","acceptedIds":[],"appliedIds":[],"applicationAuthorized":False},
        "queueAuthority":{"id":"Queue361","applied":828,"pending":20,"acceptedUnapplied":0,"completeStandaloneProcedures":552,"scopedInterfaces":173,"firstReviews":0,"closureTasks":20}}
    internal=verify_case(case,refs)
    write_json(PACKET/"W05_LIVING_BODY_CARRIAGE_CASE_365_TESTONLY.json",case)
    write_json(PACKET/"W05_CASE_COVERAGE_365.json",coverage)
    write_json(PACKET/"W05_BUILD_VALIDATION_365.json",{"status":"PASS_TEST_ONLY_STATIC_WITNESS","checks":internal,
        "identityAcceptance":False,"applicationAuthorized":False,"directorDisposition":"PENDING"})
    members=[]
    for p in sorted(x for x in PACKET.rglob("*") if x.is_file()):
        data=p.read_bytes(); members.append({"path":p.relative_to(PACKET).as_posix(),"bytes":len(data),"sha256":sha(data)})
    write_json(PACKET/"ARCHIVE_MANIFEST.json",{"id":"W05-ARCHIVE-MANIFEST-365-REPACK01","members":members})
    archive=OUT/ARCHIVE_NAME
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in PACKET.rglob("*") if x.is_file()):
            info=zipfile.ZipInfo(p.relative_to(PACKET).as_posix(),date_time=(2026,10,31,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    archive_data=archive.read_bytes()
    delivery={"id":"W05-DELIVERY-365-REPACK01","witnessId":"W05","status":"READY_FOR_DIRECTOR_REVIEW_TEST_ONLY",
        "archive":archive.name,"bytes":len(archive_data),"sha256":sha(archive_data),"memberCount":len(members)+1,
        "sourceBindings":len(bindings["bindings"]),"allEventsReversible":True,"acceptedIds":[],"appliedIds":[],"applicationAuthorized":False,
        "queueAuthority":case["queueAuthority"],"nextWitnessAfterSeal":"W03"}
    write_json(OUT/"ARCHIVE_DELIVERY_365_W05_REPACK01.json",delivery)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist())=={p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
        for name in z.namelist(): assert z.read(name)==(PACKET/name).read_bytes()
    audit={"id":"W05-INDEPENDENT-AUDIT-365-REPACK01","status":"PASS_TEST_ONLY_STATIC_WITNESS_AND_ARCHIVE; FRESH_DIRECTOR_DECISION_PENDING",
        "archive":{"file":archive.name,"bytes":len(archive_data),"sha256":sha(archive_data),"uniqueMembers":len(members)+1,"payloadHashesAndCrcs":len(members)+1},
        "sourceBindingsVerified":len(bindings["bindings"]),"caseChecks":internal,"queueAuthority":case["queueAuthority"],
        "identityDisposition":"HOLD","acceptedIds":[],"appliedIds":[],"applicationAuthorized":False}
    write_json(OUT/"INDEPENDENT_AUDIT_365_W05_REPACK01_ARCHIVE.json",audit)
    print(json.dumps({"out":str(OUT),"delivery":delivery,"audit":audit},indent=2))


if __name__=="__main__":
    main()
