#!/usr/bin/env python3
"""Independent archive, replay, source and narrow semantic verifier for W03 R6."""
import argparse
import copy
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

CARD = "wizard.base.counterspell"
PRIOR_SHA = "9ce22e2a240b0ac92eb98d676c197c3d6e64696e7b59595cec885c6f4d383cd7"
checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def state_hash(state):
    return digest(json.dumps(state, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode())


def replay_ops(state, ops):
    state = copy.deepcopy(state)
    for op in ops:
        require(op["path"].startswith("/") and op["path"] != "/", "field-scoped patch")
        keys = [k.replace("~1", "/").replace("~0", "~") for k in op["path"].split("/")[1:]]
        parent = state
        for key in keys[:-1]:
            parent = parent[int(key)] if isinstance(parent, list) else parent[key]
        key = int(keys[-1]) if isinstance(parent, list) and keys[-1] != "-" else keys[-1]
        if op["op"] == "test":
            require(parent[key] == op["value"], "patch precondition " + op["path"])
        elif op["op"] == "add":
            if isinstance(parent, list):
                parent.append(copy.deepcopy(op["value"])) if key == "-" else parent.insert(key, copy.deepcopy(op["value"]))
            else:
                parent[key] = copy.deepcopy(op["value"])
        elif op["op"] == "replace":
            require(key in parent if isinstance(parent, dict) else 0 <= key < len(parent), "replace existing field")
            parent[key] = copy.deepcopy(op["value"])
        elif op["op"] == "remove":
            parent.pop(key)
        else:
            raise AssertionError("unsupported operation")
    return state


def verify(archive_path, prior_path):
    raw = archive_path.read_bytes()
    oldraw = prior_path.read_bytes()
    require(digest(oldraw) == PRIOR_SHA, "exact previously reviewed input")
    z = zipfile.ZipFile(io.BytesIO(raw))
    old = zipfile.ZipFile(io.BytesIO(oldraw))
    require(z.testzip() is None, "ZIP CRCs")
    require(len(z.namelist()) == len(set(z.namelist())), "unique members")
    require(all(n.startswith("packet/") and ".." not in n.split("/") for n in z.namelist()), "member paths")
    manifest = json.loads(z.read("packet/MANIFEST.json"))
    require(set(z.namelist()) == {"packet/" + v["path"] for v in manifest["files"]} | {"packet/MANIFEST.json"}, "exact member set")
    require(len(manifest["files"]) == manifest["fileCountExcludingManifest"], "manifest count")
    for row in manifest["files"]:
        data = z.read("packet/" + row["path"])
        require(len(data) == row["bytes"] and digest(data) == row["sha256"], "member " + row["path"])
    for name in old.namelist():
        if name.startswith("packet/sources/"):
            require(z.read(name) == old.read(name), "immutable source " + name)
    bindings = json.loads(z.read("packet/SOURCE_BINDINGS_400.json"))
    for row in bindings["sourceFiles"]:
        data = z.read("packet/" + row["member"])
        require(len(data) == row["bytes"] and digest(data) == row["sha256"], "source binding " + row["member"])
    nested = zipfile.ZipFile(io.BytesIO(z.read("packet/sources/W07_Repack01_TESTONLY.zip")))
    engine = z.read("packet/sources/WIZARD_CLASS_ENGINE_W07.md")
    require(engine == nested.read("sources/rules/WIZARD_CLASS_ENGINE.md"), "exact sealed class rule bytes")
    require("always-prepared class matrices" in engine.decode().splitlines()[43], "automatic class matrix readiness rule")
    profile = json.loads(z.read("packet/sources/W07_BOUND_ACTOR_PROFILES_351fe708.json"))["Wizard20"]
    card = profile["automaticCards"][1]
    require(card["id"] == CARD and card["acquisition"] == "automatic" and card["minimumClassLevel"] == 2, "automatic acquired card")
    require(card["activation"] == "Reaction" and card["cost"] == "3 RP" and "60 feet" in card["rangeAndTarget"], "printed counterspell route")
    precedent = json.loads(z.read("packet/sources/W07_GUST_CORPSE_CASE_363.json"))
    require(precedent["events"][2]["before"]["pendingCast"]["counterspellWindow"]["eligibleReactors"][0]["componentsAvailable"] == ["V", "S", "F"], "sealed component witness binding")
    r = json.loads(z.read("packet/W03_REPLAY_400.json"))
    prior = json.loads(old.read("packet/W03_REPLAY_400.json"))
    require(len(r["events"]) == len(prior["events"]) == 13, "event count")
    require(len(r["stateSnapshots"]) == len(prior["stateSnapshots"]) == 14, "snapshot count")
    snaps = {s["id"]: s for s in r["stateSnapshots"]}
    for snap in snaps.values():
        require(state_hash(snap["state"]) == snap["stateSha256"], "snapshot hash " + snap["id"])
    historical = json.loads(z.read("packet/sources/RETURN327_STATIONARY_TYPE_CHANGE_PARENT.json"))["initial"]
    require(r["stateSnapshots"][0] == prior["stateSnapshots"][0], "unmodified parent snapshot")
    require(r["stateSnapshots"][0]["state"] == historical, "exact historical parent /initial")
    state = copy.deepcopy(historical)
    for event in r["events"]:
        require(state == snaps[event["beforeSnapshot"]]["state"], "before reference " + event["id"])
        require(state_hash(state) == event["beforeStateSha256"], "before hash")
        state = replay_ops(state, event["forwardPatch"])
        require(state == snaps[event["afterSnapshot"]]["state"], "after reference " + event["id"])
        require(state_hash(state) == event["afterStateSha256"], "after hash")
    for event in reversed(r["events"]):
        require(state_hash(state) == event["afterStateSha256"], "reverse starting hash")
        state = replay_ops(state, event["inversePatch"])
        require(state == snaps[event["beforeSnapshot"]]["state"] and state_hash(state) == event["beforeStateSha256"], "inverse full comparison")
    require(state == historical, "exact full parent restoration")

    for index, (snap, original) in enumerate(zip(r["stateSnapshots"], prior["stateSnapshots"])):
        require((snap["id"], snap["eventTime"]) == (original["id"], original["eventTime"]), "unchanged time and snapshot identity")
        stripped = copy.deepcopy(snap["state"])
        if index:
            for actor_id in ("B", "D"):
                stripped["actors"][actor_id].pop("handCustody")
                stripped["actors"][actor_id].pop("counterspellReadiness")
                stripped["actors"][actor_id]["recharge"].pop(CARD)
                for key in ("carriedBy", "carryingState", "heldIn"):
                    stripped["items"]["focus-" + actor_id].pop(key)
            stripped["fixture"].pop("counterspellReadinessPremises")
        if index == 4:
            stripped["pendingCast"]["counterspellWindow"] = original["state"]["pendingCast"]["counterspellWindow"]
            stripped["pendingCastStack"] = original["state"]["pendingCastStack"]
        require(stripped == original["state"], "no change outside R6 at snapshot " + str(index))
    for event, original in zip(r["events"], prior["events"]):
        for key in ("id", "kind", "eventTime", "beforeSnapshot", "afterSnapshot"):
            require(event[key] == original[key], "unchanged ordering " + key)
    require(all(a["eventTime"] <= b["eventTime"] for a, b in zip(r["events"], r["events"][1:])), "monotone chronology")

    window = r["events"][3]["authoredInputs"]["counterspellWindow"]
    state = r["stateSnapshots"][4]["state"]
    require(window["eligibleResponders"] == ["B", "D"], "eligible roster")
    require(window["fromEventTime"] == 0 and window["untilEventTime"] == 0.1, "paid pre-resolution window")
    require(state["actors"]["A"]["RP"] == 54 and state["actors"]["A"]["action"] == 0, "caster already paid")
    require(state["pendingCast"]["resolved"] is False and state["actors"]["A"]["concentration"] is None, "not yet resolved")
    for actor_id, rowindex in (("B", 1), ("D", 3)):
        row = window["dispositions"][rowindex]
        actor = state["actors"][actor_id]
        focus = state["items"]["focus-" + actor_id]
        require(actor["class"] == "Wizard" and actor["level"] >= card["minimumClassLevel"], "actual Wizard eligibility")
        require(actor["profileSHA256"] == state_hash(profile), "exact actor profile")
        require(row["source"] == "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json#/Wizard20/automaticCards/1", "operative card source")
        require(row["alwaysPrepared"] and row["acquired"], "acquisition/preparation")
        distance = math.dist(actor["position"], state["actors"]["A"]["position"])
        require(abs(row["distanceFeet"] - distance) < 1e-6 and distance <= 60, "actual distance")
        require(actor["conditions"] == [] and actor["voice"] and actor["handCustody"]["voiceAvailable"], "voice and conditions")
        require(actor["handCustody"]["rightHand"]["free"] and actor["handCustody"]["rightHand"]["usableForSomatic"], "free S hand")
        require(actor["handCustody"]["leftHand"]["itemId"] == focus["id"] and focus["heldIn"] == "left" and focus["custodian"] == actor_id and focus["carriedBy"] == actor_id, "held focus identity/custody")
        require(row["componentsAvailable"] == ["V", "S", "F"] and focus["exists"] and not focus["consumed"], "available components")
        require(actor["counterspellReadiness"]["castPerception"]["perceivesCasting"] and row["perceivesCasting"] and row["lineOfSight"] and row["lineOfEffect"], "perception and line")
        require(state["spaces"]["fixture:origin"]["terrain"] == [], "clear retained scene")
        require(actor["reaction"] == row["reactionBefore"] == 1 and actor["RP"] == row["currentRP"] == 80, "current resource budgets")
        require(actor["recharge"][CARD] == row["rechargeCounter"] == 0 and row["rechargeReady"], "ready recharge")
        require(actor["Dissonance"] == actor["Refrain"] == 0, "no strain eligibility block")
        require(row["eligibility"] == "eligible" and row["decision"] == "decline", "evaluated eligible decline")
        require(not row["attempted"] and row["roll"] is None and row["RPSpent"] == 0 and not row["reactionSpent"] and not row["rechargeChanged"] and not row["castingHistoryChanged"] and not row["strainChanged"], "zero response settlement")
        for field in ("RP", "reaction", "recharge", "spellHistory", "resourceHistory", "Dissonance", "Refrain", "preparedFamiliesUsed", "magicThisTurn"):
            values = [r["stateSnapshots"][i]["state"]["actors"][actor_id][field] for i in (3, 4, 5)]
            require(values[0] == values[1] == values[2], "decline preserves " + actor_id + "/" + field)
    require(window["dispositions"][0]["eligibility"] == "unadjudicated" and "no-attempt" in window["dispositions"][0]["disposition"], "self no-attempt unchanged")
    scenario = json.loads(z.read("packet/W03_SCENARIO_400_TESTONLY.json"))
    require(scenario["gateSetupCast"]["counterspellDisposition"] == window, "scenario/replay window agreement")
    oldscenario = json.loads(old.read("packet/W03_SCENARIO_400_TESTONLY.json"))
    require(scenario["ritualContinuity"] == oldscenario["ritualContinuity"] and len(scenario["ritualContinuity"]["checkpoints"]) == 9, "ritual and nine checkpoints preserved")
    require(scenario["gateSetupCast"]["deadline"] == 600.1 and scenario["gateSetupCast"]["remainingAtFinalTimeSeconds"] == 599.1, "unchanged Gate clock")
    require(scenario["gateSetupCast"]["sourceSchoolOnBoundCatalogRow"] == "Abjuration", "correct identity-specific school")
    delivery = json.loads((archive_path.parent / "ARCHIVE_DELIVERY_400_REPACK03.json").read_bytes())
    require(delivery["archive"]["sha256"] == digest(raw) and delivery["archive"]["bytes"] == len(raw), "delivery archive")
    require({m["path"] for m in delivery["archive"]["zipMembers"]} == set(z.namelist()), "delivery exact member set")
    for member in delivery["archive"]["zipMembers"]:
        data = z.read(member["path"])
        require(member["bytes"] == len(data) and member["sha256"] == digest(data) and member["crc32"] == format(z.getinfo(member["path"]).CRC, "08x"), "delivery member hash/CRC")
    return {"id": "W03-400-REPACK03-INDEPENDENT-VERIFICATION", "result": "PASS", "checks": checks,
            "archiveSha256": digest(raw), "archiveBytes": len(raw), "memberCount": len(z.namelist()),
            "manifestPayloadCount": len(manifest["files"]), "sourceBindings": len(bindings["sourceFiles"]),
            "forwardTransitions": 13, "inverseTransitions": 13, "fullSnapshots": 14,
            "exactParentRestoration": True, "R6": "PASS", "priorPassedResidualsUnchanged": True,
            "scope": "TEST_ONLY verification; no automatic witness seal or identity acceptance",
            "verifierSha256": digest(Path(__file__).read_bytes())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("prior_archive", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = verify(args.archive, args.prior_archive)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))
