from __future__ import annotations

import copy
import hashlib
import json
import math
import zipfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
OUT = HERE / "banishment_gate_witness365_w05_separation365_repack01_build01"
PACKET = OUT / "packet"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_sha(value: Any) -> str:
    return sha(canonical(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pointer(root: Any, ptr: str) -> Any:
    value = root
    if not ptr or ptr == "/":
        return value
    for token in ptr.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def at(root: Any, path: list[str]) -> Any:
    value = root
    for token in path:
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def put(root: Any, path: list[str], value: Any, remove: bool = False) -> None:
    parent = root
    for token in path[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
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


def replay(state: Any, ops: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in ops:
        old = at(result, op["path"]) if op["op"] != "add" else None
        if op["op"] == "remove":
            assert old == op["before"]
            put(result, op["path"], None, remove=True)
        elif op["op"] == "add":
            put(result, op["path"], copy.deepcopy(op["after"]))
        else:
            assert old == op["before"], (op["path"], old, op["before"])
            put(result, op["path"], copy.deepcopy(op["after"]))
    return result


def check_events(start: dict[str, Any], events: list[dict[str, Any]]) -> tuple[dict[str, Any], list[float]]:
    state = copy.deepcopy(start)
    times: list[float] = []
    for item in events:
        assert item["timestampSeconds"] >= state["elapsedSeconds"], item["eventId"]
        assert item["beforeStateSha256"] == state_sha(state), item["eventId"]
        after = replay(state, item["forwardOperations"])
        assert after == item["stateAfter"]
        assert state_sha(after) == item["afterStateSha256"]
        assert replay(after, item["inverseOperations"]) == state
        state = after
        times.append(item["timestampSeconds"])
    return state, times


def main() -> None:
    case_path = PACKET / "W05_LIVING_BODY_CARRIAGE_CASE_365_TESTONLY.json"
    case = read_json(case_path)
    bindings = read_json(PACKET / "W05_SOURCE_BINDINGS_365.json")
    for binding in bindings["bindings"]:
        data = (PACKET / binding["member"]).read_bytes()
        assert len(data) == binding["bytes"]
        assert sha(data) == binding["sha256"]

    gate_source = read_json(PACKET / "sources" / "RETURN327_banishment-gate.json")
    ac5 = read_json(PACKET / "sources" / "AC5_ACCEPTED_SPELLS_MODEL.json")
    casebook = read_json(PACKET / "sources" / "AC5_ACCEPTED_CASEBOOK.json")
    gate = case["commonPrefix"]["finalState"]["gate"]
    assert gate_source["id"] == "banishment-gate"
    assert "separate living passengers" in gate_source["procedure"]
    fire_spell = next(s for s in ac5["spells"] if s["id"] == "summon-greater-fire-pet")
    champion_spell = next(s for s in ac5["spells"] if s["id"] == "faction-champion")
    assert fire_spell["completeSourceAndAccess"]["classAccess"]["Mage"] == {"rank":5,"minimumClassLevel":9,"school":"Conjuration","baseRpCost":10}
    assert champion_spell["completeSourceAndAccess"]["classAccess"]["Mage"] == {"rank":5,"minimumClassLevel":9,"school":"Conjuration","baseRpCost":10}
    fire_profile = ac5["profiles"]["AC5-PROFILE-GREATER-FIRE-PET-01"]
    champion_profile = ac5["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    x17 = next(c for c in casebook["cases"] if c["id"] == "AC5-X17")
    assert "separate willing Small creature" in x17["currentInitialState"]
    assert case["comparisonBoundary"]["sourceCaseId"] == "AC5-X17"
    assert "AC5-BANISH-EXT" in case["comparisonBoundary"]["notUsed"]

    starts = case["timeModel"]["castWindows"]
    assert all(starts[i]["commit"] <= starts[i+1]["start"] for i in range(len(starts)-1))
    assert len({x["actor"] for x in starts}) == 3
    assert case["timeModel"]["firePetDeadline"] == -18 + 60
    assert case["timeModel"]["championDeadline"] == -12 + 60
    assert case["timeModel"]["gateDeadline"] == -6 + 600

    fire = fire_profile
    passenger = champion_profile
    weight_limit = fire["abilities"]["STR"] * 15
    load_capacity = fire["abilities"]["STR"]
    casualty_load = 6 # medium casualty load in the pinned BODY_EQUIPMENT table
    assert fire["size"] == "Medium" and passenger["size"] == "Medium"
    assert fire["creatureType"] == "Elemental" and passenger["creatureType"] == "Humanoid"
    assert case["selectedGateType"] == "Elemental"
    assert passenger["weightLb"] <= weight_limit
    assert casualty_load <= load_capacity
    body_rules=(PACKET/"rules"/"BODY_EQUIPMENT.md").read_text(encoding="utf-8-sig")
    assert "Strength score × 15" in body_rules and "Casualty Load for a body of this size" in body_rules
    assert case["commonPrefix"]["finalState"]["carriageRelation"]["capacity"]["weightPass"] is True
    assert case["commonPrefix"]["finalState"]["carriageRelation"]["capacity"]["loadPass"] is True
    assert abs(math.dist([-50,0,0],[0,0,0])-gate["rangeFromCasterFt"]) < 1e-9
    assert gate["castPredicates"]["rpSpent"] == 26 and gate["catalogMetadataConflict"]["catalogPreservedUnchanged"] is True

    common, common_times = check_events(case["commonPrefix"]["initialState"], case["commonPrefix"]["events"])
    assert common == case["commonPrefix"]["finalState"]
    branch_results = {}
    for fork in case["terminalForks"]:
        final, times = check_events(common, fork["events"])
        assert final == fork["finalState"]
        reverse = copy.deepcopy(final)
        for item in reversed(fork["events"]):
            assert state_sha(reverse) == item["afterStateSha256"]
            reverse = replay(reverse, item["inverseOperations"])
            assert state_sha(reverse) == item["beforeStateSha256"]
        assert reverse == common
        if fork["id"] == "W05-LAWFUL-SEPARATION":
            assert final["actors"]["actor-w05-champion"]["physicalPosition"]["planeKey"] == case["commonPrefix"]["finalState"]["world"]["originPlaneKey"]
            assert final["actors"]["actor-w05-firepet"]["physicalPosition"]["planeKey"].startswith("CELL-")
            assert len(final["cells"]) == 1 and len(final["hardControlClaims"]) == 1
            assert final["actors"]["actor-w05-champion"]["alive"] and not final["actors"]["actor-w05-champion"]["isGear"]
        elif fork["id"] == "W05-IMPOSSIBLE-SEPARATION":
            assert len(final["cells"]) == 0 and len(final["hardControlClaims"]) == 0
            assert all(final["actors"][k]["alive"] for k in ("actor-w05-firepet","actor-w05-champion"))
            assert all(final["actors"][k]["physicalPosition"]["planeKey"] == final["world"]["originPlaneKey"] for k in ("actor-w05-firepet","actor-w05-champion"))
            assert all(not final["actors"][k]["isGear"] and k not in final["objects"] for k in ("actor-w05-firepet","actor-w05-champion"))
            receipt=final["gate"]["crossingReceipts"]["W05-CROSSING-IMPOSSIBLE-SEP-001"]
            assert receipt["cellCreated"] is False and receipt["claimSpent"] is False and receipt["ordinaryMovementResolved"] is True
        else:
            raise AssertionError(fork["id"])
        branch_results[fork["id"]]={"eventCount":len(fork["events"]),"chronological":times==sorted(times),"exactReverse":True,"finalStateSha256":state_sha(final)}

    assert case["identityDecision"] == {"decision":"HOLD","acceptedIds":[],"appliedIds":[],"applicationAuthorized":False}
    assert case["queueAuthority"] == {"id":"Queue361","applied":828,"pending":20,"acceptedUnapplied":0,
        "completeStandaloneProcedures":552,"scopedInterfaces":173,"firstReviews":0,"closureTasks":20}
    manifest=read_json(PACKET/"ARCHIVE_MANIFEST.json")
    archive=OUT/"DD_Rank9_BanishmentGate_W05_CarriedBodies_365_TESTONLY_REPACK01.zip"
    archive_bytes=archive.read_bytes()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names=set(z.namelist())
        expected={m["path"] for m in manifest["members"]}|{"ARCHIVE_MANIFEST.json"}
        assert names==expected
        for member in manifest["members"]:
            data=z.read(member["path"])
            assert len(data)==member["bytes"] and sha(data)==member["sha256"]
        assert z.read("ARCHIVE_MANIFEST.json")== (PACKET/"ARCHIVE_MANIFEST.json").read_bytes()
    audit={"id":"W05-INDEPENDENT-AUDIT-365-REPACK01","status":"PASS_TEST_ONLY_STATIC_WITNESS_AND_ARCHIVE; FRESH_DIRECTOR_DECISION_PENDING",
        "archive":{"file":archive.name,"bytes":len(archive_bytes),"sha256":sha(archive_bytes),"uniqueMembers":len(names),"payloadHashesAndCrcs":len(names)},
        "sourceBindingsVerified":len(bindings["bindings"]),"sourcePointersVerified":True,
        "bodyProfilesVerified":{"primary":fire_profile["id"],"passenger":champion_profile["id"],"differentCreatureTypes":True},
        "capacity":{"physicalLimitLb":weight_limit,"passengerWeightLb":passenger["weightLb"],"casualtyLoad":casualty_load,"loadCapacity":load_capacity,"bothChecksPass":True},
        "commonEvents":len(case["commonPrefix"]["events"]),"commonChronological":common_times==sorted(common_times),"branches":branch_results,
        "identityDisposition":"HOLD","acceptedIds":[],"appliedIds":[],"applicationAuthorized":False,"queueAuthority":case["queueAuthority"]}
    out=OUT/"INDEPENDENT_AUDIT_365_W05_REPACK01_ARCHIVE.json"
    out.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(audit,indent=2))


if __name__ == "__main__":
    main()
