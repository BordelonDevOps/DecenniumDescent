import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = REVIEW.parents[4]
PROPOSAL_DIR = REVIEW / "fortress_w13_nested_space_owner_proposal_448"
PROPOSAL = PROPOSAL_DIR / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json"
ADOPTION = PROPOSAL_DIR / "OWNER_PG328_W13_ADOPTION_448_TESTONLY.json"
PARENT = REVIEW / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
DIRECTOR = REVIEW / "DIRECTOR_READBACK_464.json"
QUEUE = REVIEW / "CURRENT_SPELL_QUEUE_451_REPACK01.json"
WITNESS = ROOT / "W13_WITNESS_469_TESTONLY.json"
TRACE = ROOT / "W13_LIFECYCLE_TRACE_469.json"
VALIDATION = ROOT / "BUILD_VALIDATION_469.json"
README = ROOT / "README_WITNESS_469.md"
MANIFEST = ROOT / "MANIFEST_469.json"
ARCHIVE = ROOT / "DD_Fortress_W13_Reversible_Witness_469_TESTONLY.zip"
DELIVERY = ROOT / "DELIVERY_469.json"
VERIFIER = ROOT / "VERIFY_W13_WITNESS_469.py"

PROPOSAL_SHA = "9254bee8a314de50cbe0c6aa71bef45e22fbea988d8668c089151b8e7f80051a"
ADOPTION_SHA = "a118fa592228d6747c546364007f5b125153f2d4845374ab01525141fe20fd05"
PARENT_REPLAY_SHA = "2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb"
S030_SHA = "6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c"
ROOT_ID = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1"
ROOT_SPACE = ROOT_ID + "/space"
CHILD_ID = "PG328-W13-R1:DEMIPLANE-B/cast1/space"
CHILD_SPACE = CHILD_ID
TILE_ID = "PG328-W01-403:CLAY-TILE-1"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def object_sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def repo_path(path):
    return Path(path).resolve().relative_to(REPO.resolve()).as_posix()


def json_pointer(parts):
    return "/" + "/".join(str(x).replace("~", "~0").replace("/", "~1") for x in parts)


def diff(before, after, path=None):
    path = [] if path is None else path
    if isinstance(before, dict) and isinstance(after, dict):
        out = []
        for key in sorted(before.keys() - after.keys()):
            out.append({"op": "remove", "path": json_pointer(path + [key]), "oldValue": copy.deepcopy(before[key])})
        for key in sorted(after.keys() - before.keys()):
            out.append({"op": "add", "path": json_pointer(path + [key]), "value": copy.deepcopy(after[key])})
        for key in sorted(before.keys() & after.keys()):
            out.extend(diff(before[key], after[key], path + [key]))
        return out
    if isinstance(before, list) and isinstance(after, list):
        if len(before) <= len(after) and before == after[:len(before)]:
            return [{"op": "add", "path": json_pointer(path + [i]), "value": copy.deepcopy(after[i])} for i in range(len(before), len(after))]
        if len(after) <= len(before) and after == before[:len(after)]:
            return [{"op": "remove", "path": json_pointer(path + [i]), "oldValue": copy.deepcopy(before[i])} for i in range(len(before) - 1, len(after) - 1, -1)]
        return [] if before == after else [{"op": "replace", "path": json_pointer(path), "oldValue": copy.deepcopy(before), "value": copy.deepcopy(after)}]
    return [] if before == after else [{"op": "replace", "path": json_pointer(path), "oldValue": copy.deepcopy(before), "value": copy.deepcopy(after)}]


def inverse(ops):
    out = []
    for op in reversed(ops):
        if op["op"] == "add":
            out.append({"op": "remove", "path": op["path"], "oldValue": copy.deepcopy(op["value"])})
        elif op["op"] == "remove":
            out.append({"op": "add", "path": op["path"], "value": copy.deepcopy(op["oldValue"])})
        else:
            out.append({"op": "replace", "path": op["path"], "oldValue": copy.deepcopy(op["value"]), "value": copy.deepcopy(op["oldValue"])})
    return out


def apply_ops(state, ops):
    result = copy.deepcopy(state)
    for op in ops:
        path = [x.replace("~1", "/").replace("~0", "~") for x in op["path"].lstrip("/").split("/")]
        parent = result
        for part in path[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = path[-1]
        if isinstance(parent, list):
            index = int(key)
            if op["op"] == "add":
                parent.insert(index, copy.deepcopy(op["value"]))
            elif op["op"] == "remove":
                parent.pop(index)
            else:
                parent[index] = copy.deepcopy(op["value"])
        elif op["op"] == "add":
            parent[key] = copy.deepcopy(op["value"])
        elif op["op"] == "remove":
            del parent[key]
        else:
            parent[key] = copy.deepcopy(op["value"])
    return result


def add_event(specs, time, order, kind, details):
    specs.append({"timeSeconds": float(time), "orderAtTime": order, "kind": kind, "details": copy.deepcopy(details)})


def bounds_overlap(a, b):
    return all(min(a[axis][1], b[axis][1]) - max(a[axis][0], b[axis][0]) > 1e-9 for axis in ("x", "y", "z"))


def source_bindings(proposal, verification_commit):
    result = []
    for declared in proposal["sourceBindings"]:
        raw = subprocess.check_output(["git", "show", proposal["readAtCommit"] + ":" + declared["path"]], cwd=REPO)
        actual = hashlib.sha256(raw).hexdigest()
        git_sha = subprocess.check_output(["git", "hash-object", "--stdin"], input=raw, cwd=REPO).decode().strip()
        result.append({**declared, "actualSha256": actual, "actualGitBlobSha1": git_sha, "matches": actual == declared["sha256"] and git_sha == declared["gitBlobSha1"], "resolvedAtCommit": proposal["readAtCommit"], "alsoPresentAtCommit": verification_commit})
    return result


def main():
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    adoption = json.loads(ADOPTION.read_text(encoding="utf-8"))
    parent_doc = json.loads(PARENT.read_text(encoding="utf-8"))
    director = json.loads(DIRECTOR.read_text(encoding="utf-8"))
    queue_doc = json.loads(QUEUE.read_text(encoding="utf-8"))
    inputs = proposal["ownerProposedInputs"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO).decode().strip()
    actual_proposal_sha = file_sha(PROPOSAL)
    actual_adoption_sha = file_sha(ADOPTION)
    parent_state = copy.deepcopy(parent_doc["stateSnapshots"]["S030"])
    if actual_proposal_sha != PROPOSAL_SHA or actual_adoption_sha != ADOPTION_SHA:
        raise ValueError("Exact proposal/adoption binding failed")
    if file_sha(PARENT) != PARENT_REPLAY_SHA or object_sha(parent_state) != S030_SHA:
        raise ValueError("Exact W01-403 S030 binding failed")
    if adoption["scope"]["branchId"] != "PG328-W13-R1" or adoption["scope"]["proposalSha256"] != PROPOSAL_SHA:
        raise ValueError("Owner adoption scope/hash mismatch")
    if director.get("W13", {}).get("status") != "READY_FOR_OWNER_ADOPTION" or director.get("W13", {}).get("proposalSha256") != PROPOSAL_SHA:
        raise ValueError("Director 464 readiness receipt mismatch")
    if inputs["branchAuthority"]["noExternalEventsClaimed"] is not True or inputs["parentAtS030"]["noParentMutation"] is not True:
        raise ValueError("W13 branch or no-mutation boundary changed")

    bindings = source_bindings(proposal, head)
    if len(bindings) != 17 or not all(x["matches"] for x in bindings):
        raise ValueError("One or more of the 17 adopted proposal source bindings failed")

    initial = copy.deepcopy(parent_state)
    state = copy.deepcopy(initial)
    base_clock = copy.deepcopy(state["clock"])
    base_time = state["time"]
    specs = []
    marker_merge = {(19.9, "B"): "B_END_EFF_EXPIRY", (24.0, "A"): "A_START_SIGHT_TICK", (25.0, "B"): "B_START_CHILD_DISPEL", (30.0, "A"): "A_START_PARENT_DISPEL"}
    merged_lifecycle = {"B_END_EFF_EXPIRY": 12, "A_START_SIGHT_TICK": 13, "B_START_CHILD_DISPEL": 14, "A_START_PARENT_DISPEL": 19}
    life = inputs["scheduledTimeAdvance"]["lifecycleEvents"]
    for aid, markers in inputs["scheduledTimeAdvance"]["markersByActor"].items():
        for time in markers["starts"]:
            merge = marker_merge.get((float(time), aid))
            if merge:
                add_event(specs, time, 10, merge, {"actorId": aid, "lifecycleEvent": life[merged_lifecycle[merge] - 1], "lifecyclePointer": f"/ownerProposedInputs/scheduledTimeAdvance/lifecycleEvents/{merged_lifecycle[merge]-1}"})
            else:
                add_event(specs, time, 10, "START", {"actorId": aid})
        for time in markers["ends"]:
            merge = marker_merge.get((float(time), aid))
            if merge:
                add_event(specs, time, 90, merge, {"actorId": aid, "lifecycleEvent": life[merged_lifecycle[merge] - 1], "lifecyclePointer": f"/ownerProposedInputs/scheduledTimeAdvance/lifecycleEvents/{merged_lifecycle[merge]-1}"})
            else:
                add_event(specs, time, 90, "END", {"actorId": aid})

    life_handlers = {
        1: (13.1, 20, "DEMIPLANE_COMMIT"), 2: (13.2, 30, "COUNTER_DEMIPLANE"), 3: (13.3, 40, "DEMIPLANE_RESOLVE"),
        4: (18.05, 20, "TILE_DROP"), 5: (18.06, 20, "A_MOVE"), 6: (18.1, 20, "SIGHT_COMMIT"), 7: (18.2, 30, "COUNTER_SIGHT"),
        8: (18.3, 40, "SIGHT_RESOLVE"), 9: (19.01, 20, "SECURE_CARGO"), 10: (19.05, 20, "CHILD_ENTRY"),
        11: (19.06, 20, "CARGO_SETDOWN"), 15: (25.1, 20, "CHILD_DISPEL_COMMIT"), 16: (25.2, 30, "COUNTER_CHILD_DISPEL"),
        17: (25.3, 40, "CHILD_DISPEL_RESOLVE"), 18: (25.31, 20, "P5_CLOSE_BODY"), 20: (30.1, 20, "PARENT_DISPEL_COMMIT"),
        21: (30.2, 30, "COUNTER_PARENT_DISPEL"), 22: (30.3, 40, "PARENT_DISPEL_RESOLVE"), 23: (30.31, 10, "Q27_ROOT_END")
    }
    lifecycle_pointers = {}
    for index, (time, order, kind) in life_handlers.items():
        event = life[index - 1]
        lifecycle_pointers[kind] = index - 1
        add_event(specs, time, order, kind, {"lifecycleEvent": event, "lifecyclePointer": f"/ownerProposedInputs/scheduledTimeAdvance/lifecycleEvents/{index-1}"})
    add_event(specs, 25.31, 30, "P5_CLOSE_LOOSE", {"sourcePointer": "/ownerProposedInputs/childTerminalSettlement"})
    add_event(specs, 30.31, 20, "Q27_BODY", {"actor": "A", "sourcePointer": "/ownerProposedInputs/rootTerminalClosure/A"})
    add_event(specs, 30.31, 30, "Q27_BODY", {"actor": "B", "sourcePointer": "/ownerProposedInputs/rootTerminalClosure/B"})
    for order, item in enumerate(inputs["rootTerminalClosure"]["looseItems"], 40):
        add_event(specs, 30.31, order, "Q27_LOOSE", {"itemId": item["id"], "sourcePointer": f"/ownerProposedInputs/rootTerminalClosure/looseItems/{order-40}"})
    specs.sort(key=lambda x: (x["timeSeconds"], x["orderAtTime"], x["kind"]))

    turns = {}
    events = []
    casts = {}
    spell_specs = {
        "DEMIPLANE_COMMIT": ("B", "demiplane", "Conjuration", 8, 21, None, "child-room", None),
        "SIGHT_COMMIT": ("A", "wizard.arch.arcane-sight", "Divination", 2, 2, 2, "self", 600),
        "CHILD_DISPEL_COMMIT": ("B", "wizard.arch.dispel-magic", "Abjuration", 3, 3, 2, CHILD_SPACE, None),
        "PARENT_DISPEL_COMMIT": ("A", "wizard.arch.dispel-magic", "Abjuration", 3, 3, 2, ROOT_ID, None),
    }

    def advance(time):
        delta = time - base_time
        state["time"] = time
        state["clock"]["elapsedSeconds"] = base_clock["elapsedSeconds"] + delta
        for key in ("OpeningRemaining", "HornRemaining"):
            if key in base_clock and base_clock[key] is not None:
                state["clock"][key] = base_clock[key] - delta

    def commit_spell(kind, entry):
        actor_id, spell_id, school, rank, base_cost, recharge, target, duration = spell_specs[kind]
        actor = state["actors"][actor_id]
        time = entry["timeSeconds"]
        context = turns.get(actor_id)
        if context is None or actor["action"] != 1:
            raise ValueError(f"No available action for {spell_id} at {time}")
        context["spent"] = 1
        context["kind"] = "CAST"
        actor["action"] = 0
        actor["magicThisTurn"] = True
        first = spell_id not in actor["preparedFamiliesUsed"]
        refrain = min(3, actor["Refrain"] + 1) if actor["lastSpell"] == spell_id else 0
        base_dissonance = 0 if first else (1 if rank <= 5 else 2)
        dissonance_limit = max(4, 2 + actor["PB"] + max(0, actor["M"]))
        surcharge = 1 if actor["Dissonance"] >= dissonance_limit else 2 if actor["Dissonance"] >= dissonance_limit + 3 else 3 if actor["Dissonance"] >= dissonance_limit + 6 else 0
        deadline = context["turnStart"] + actor["regularSchedule"]["period"] + actor["regularSchedule"]["endOffset"]
        discount = False
        paid = max(1, base_cost - (1 if discount else 0)) + surcharge
        before_rp = actor["RP"]
        actor["RP"] -= paid
        actor["Dissonance"] += base_dissonance + refrain
        actor["Refrain"] = refrain
        actor["lastSpell"] = spell_id
        if first:
            actor["preparedFamiliesUsed"].append(spell_id)
        cast_id = f"PG328-W13-R1:{spell_id}:{time:.2f}"
        casts[kind] = cast_id
        history = {"castId": cast_id, "spellId": spell_id, "class": "Wizard", "school": school, "rank": rank, "time": time, "cost": paid, "firstPreparedFamily": first, "baseDissonance": base_dissonance, "Refrain": refrain, "originPlane": actor["plane"], "target": target, "spellEfficiencyDiscountApplied": False, "spellEfficiencyWindowExpiresAt": deadline, "resolutionStatus": "PENDING"}
        if duration is not None:
            history["concentration"] = {"activeFromCommit": True, "startedAt": time, "maximumDurationSeconds": duration, "deadline": time + duration}
            actor["concentration"] = {"spellId": spell_id, "active": True, "startedAt": time, "maximumDurationSeconds": duration, "deadline": time + duration, "classification": "TEST_ONLY_HYPOTHETICAL_BRANCH"}
        actor["spellHistory"].append(history)
        actor["resourceHistory"].append({"event": cast_id, "RP": -paid, "poolAfter": actor["RP"], "discount": False, "spellId": spell_id, "DissonanceBefore": actor["Dissonance"] - base_dissonance - refrain, "DissonanceAfter": actor["Dissonance"], "Refrain": refrain, "surchargeRP": surcharge})
        actor.setdefault("testOnlySpellEfficiencyHistory", []).append({"family": spell_id, "castId": cast_id, "createdAt": time, "expiresAt": float(deadline), "discountRP": 1, "minimumCostRP": 1, "status": "PENDING", "consumedAt": None})
        if recharge is not None:
            actor["recharge"][spell_id] = recharge
        state["pendingCast"] = {"castId": cast_id, "spellId": spell_id, "caster": actor_id, "target": target, "commitTime": time, "costCommitted": paid, "status": "PENDING_RESOLUTION", "classification": "TEST_ONLY_HYPOTHETICAL_BRANCH"}
        entry["details"].update({"actorId": actor_id, "castId": cast_id, "spellId": spell_id, "target": target, "school": school, "rank": rank, "baseCostRP": base_cost, "costRP": paid, "RPBefore": before_rp, "RPAfter": actor["RP"], "firstPreparedFamily": first, "DissonanceAfter": actor["Dissonance"], "RefrainAfter": refrain, "spellEfficiencyDiscountApplied": False, "spellEfficiencyWindowExpiresAt": deadline, "ActionSpent": 1, "rechargeAfterCommit": actor["recharge"].get(spell_id), "concentrationAfterCommit": copy.deepcopy(actor["concentration"])})

    for number, entry in enumerate(specs, 1):
        entry = copy.deepcopy(entry)
        time, kind, details = entry["timeSeconds"], entry["kind"], entry["details"]
        before = copy.deepcopy(state)
        advance(time)
        if kind in {"START", "A_START_SIGHT_TICK", "B_START_CHILD_DISPEL", "A_START_PARENT_DISPEL"}:
            actor_id = details["actorId"]
            actor = state["actors"][actor_id]
            schedule = actor["regularSchedule"]
            recharge_before = copy.deepcopy(actor["recharge"])
            for spell_id, value in list(actor["recharge"].items()):
                actor["recharge"][spell_id] = max(0, int(value) - 1)
            speed = int(actor.get("speed", 30))
            schedule["starts"].append(time)
            schedule["nextStart"] = time + schedule["period"]
            schedule["nextEnd"] = time + schedule["endOffset"]
            actor.update({"action": 1, "bonusAction": 1, "reaction": 1, "movement": speed, "magicThisTurn": False})
            turns[actor_id] = {"turnStart": time, "spent": 0, "kind": None, "BA": 0, "reaction": 0, "move": 0, "moveGranted": speed}
            details.update({"budgetsAfterStart": {"Action": 1, "BonusAction": 1, "Reaction": 1, "MovementFeet": speed}, "operativeSpeedFeet": speed, "rechargeBefore": recharge_before, "rechargeAfter": copy.deepcopy(actor["recharge"]), "nextStart": schedule["nextStart"], "nextEnd": schedule["nextEnd"], "magicThisTurn": False, "HP": actor["HP"], "RP": actor["RP"], "Dissonance": actor["Dissonance"], "Refrain": actor["Refrain"]})
        elif kind in {"END", "B_END_EFF_EXPIRY"}:
            actor_id = details["actorId"]
            actor = state["actors"][actor_id]
            context = turns.pop(actor_id)
            before_dissonance = actor["Dissonance"]
            decay = context["kind"] != "CAST"
            if decay:
                actor["Dissonance"] = max(0, before_dissonance - 1)
            expired = []
            for record in actor.get("testOnlySpellEfficiencyHistory", []):
                if record["status"] == "PENDING" and record["expiresAt"] <= time:
                    record["status"] = "EXPIRED_UNUSED"
                    record["expiredAt"] = time
                    expired.append(record["family"])
            schedule = actor["regularSchedule"]
            schedule["ends"].append(time)
            remaining = actor["movement"]
            disposition = {"regularTurnEndedAt": time, "recordedAt": time, "Action": {"spent": context["spent"], "unusedExpired": 1-context["spent"]}, "BonusAction": {"spent": context["BA"], "unusedExpired": 1-context["BA"]}, "Reaction": {"spent": context["reaction"], "availableOffTurnUntilSpentOrNextOwnStart": actor["reaction"] == 1}, "MovementFeet": {"granted": context["moveGranted"], "spent": context["move"], "unusedExpired": remaining, "recalculatedAway": max(0, context["moveGranted"]-context["move"]-remaining)}}
            schedule["budgetHistory"].append({"time": context["turnStart"], "action": 1, "BA": 1, "Reaction": 1, "Move": context["moveGranted"], "recharge": copy.deepcopy(actor["recharge"]), "endDisposition": disposition})
            actor.update({"action": 0, "bonusAction": 0, "movement": 0})
            schedule["nextEnd"] = None
            details.update({"turnStart": context["turnStart"], "actionSpent": context["spent"], "actionKind": context["kind"], "DissonanceBeforeEnd": before_dissonance, "DissonanceAfterEnd": actor["Dissonance"], "idleDissonanceDecayApplied": decay, "unusedBudgetDisposition": disposition, "magicThisTurnAfterEnd": actor["magicThisTurn"], "nextStartPreserved": schedule["nextStart"], "nextEndAfter": None})
            if expired:
                details["efficiencyExpiredUnused"] = expired
        elif kind in spell_specs:
            commit_spell(kind, entry)
        elif kind == "TILE_DROP":
            actor = state["actors"]["A"]
            item = state["items"][TILE_ID]
            interaction = inputs["preParentTileInteraction"]
            if actor["w01HandState"].get("right") != TILE_ID or actor["action"] != 1:
                raise ValueError("A's tile or action state differs from S030/Proposal448")
            actor["equipment"].remove(TILE_ID)
            actor["carriedWeightLb"] = 12
            actor["carriedLoad"] = 1.2
            actor["w01HandState"]["right"] = "free"
            item.update({"custodian": None, "plane": interaction["to"]["plane"], "position": interaction["to"]["position"], "heldBy": None, "heldBoundsFeet": None})
            item.setdefault("testOnlyGeometry", {})["currentBoundsFeet"] = interaction["to"]["bounds"]
            item["testOnlyGeometry"]["supportPatch"] = copy.deepcopy(interaction["to"]["supportPatch"])
            turns["A"]["kind"] = "FREE_INTERACTION"
            details.update({"handsAfter": copy.deepcopy(actor["w01HandState"]), "custodianAfter": None, "positionAfter": item["position"], "boundsFeet": interaction["to"]["bounds"], "expiryPreserved": item["expiresAtEventTime"], "weightAfterLb": 12, "loadAfter": 1.2, "ActionSpent": 0})
        elif kind == "A_MOVE":
            actor = state["actors"]["A"]
            movement = inputs["parentDispel"]["approachMovement"]
            context = turns["A"]
            if actor["position"] != movement["from"] or context["moveGranted"] < movement["totalFeet"]:
                raise ValueError("A movement does not start at adopted S030 pose or exceed budget")
            context["move"] += movement["totalFeet"]
            actor["movement"] -= movement["totalFeet"]
            actor["position"] = movement["route"][-1]["to"]
            details.update({"from": movement["from"], "to": actor["position"], "movementFeet": movement["totalFeet"], "remainingMovementFeet": actor["movement"], "routeSweeps": inputs["geometryAudit"]["routeSweeps"]["A18.06"]})
        elif kind == "COUNTER_DEMIPLANE":
            details.update(copy.deepcopy(inputs["childCreation"]["counterspellDispositionAt13_2"]))
        elif kind == "DEMIPLANE_RESOLVE":
            source = inputs["childCreation"]
            cast = state["pendingCast"]
            if not cast or cast["spellId"] != "demiplane":
                raise ValueError("Demiplane resolution lacks its paid pending cast")
            state["pendingCast"] = None
            next(x for x in reversed(state["actors"]["B"]["spellHistory"]) if x["castId"] == cast["castId"]).update({"resolutionStatus": "SUCCESSFUL", "resolvedAt": time})
            state["effects"][CHILD_ID] = {"id": CHILD_ID, "spellId": "demiplane", "owner": "B", "active": True, "concentration": False, "createdAt": time, "doorExpiryAt": source["doorExpiryAt"], "parentEffect": ROOT_ID, "doorId": source["doorId"], "classification": "TEST_ONLY_HYPOTHETICAL_BRANCH"}
            state["spaces"][CHILD_SPACE] = {"kind": "TEST_ONLY generated Demiplane room", "exists": True, "bounds": [0, 30, 0, 30, 0, 15], "support": {"z": 0, "bounds": [0, 30, 0, 30]}, "roomSizeFeet": source["roomSizeFeet"], "owner": "B", "admissionList": ["B"], "doors": [{"id": source["doorId"], "open": True, "doorExpiryAt": source["doorExpiryAt"], "parentAperture": source["doorApertureInParent"], "roomAperture": source["roomSideAperture"], "opaque": True}]}
            details.update({"pendingCastAfter": None, "roomId": CHILD_ID, "roomSpace": CHILD_SPACE, "doorId": source["doorId"], "roomBounds": source["roomBounds"], "doorExpiryAt": source["doorExpiryAt"], "parentRemainsActive": state["effects"][ROOT_ID]["active"], "runtimeSelectionEnabled": False})
        elif kind == "COUNTER_SIGHT":
            details.update(copy.deepcopy(inputs["AArcaneSight"]["counterspellDispositionAt18_2"]))
        elif kind == "SIGHT_RESOLVE":
            cast = state["pendingCast"]
            if not cast or cast["spellId"] != "wizard.arch.arcane-sight":
                raise ValueError("Arcane Sight resolution lacks its paid pending cast")
            state["pendingCast"] = None
            actor = state["actors"]["A"]
            next(x for x in reversed(actor["spellHistory"]) if x["castId"] == cast["castId"]).update({"resolutionStatus": "SUCCESSFUL", "resolvedAt": time})
            effect_id = "TEST_ONLY:PG328-W13-R1:ARCANE-SIGHT:A"
            sight = inputs["AArcaneSight"]
            state["effects"][effect_id] = {"id": effect_id, "spellId": sight["spellId"], "owner": "A", "active": True, "concentration": True, "createdAt": time, "deadline": sight["concentration"]["deadlineAt"], "classification": "TEST_ONLY_HYPOTHETICAL_BRANCH"}
            observation = {"id": sight["observationReceipt"]["id"], "time": time, "observer": "A", "spellId": sight["spellId"], "subject": ROOT_ID, "auraPoint": sight["targetAuraPoint"], "distanceFeet": sight["distanceFeet"], "samePlane": True, "totalCover": False, "lineClear": True, "knownCategory": "Conjuration", "branchId": "PG328-W13-R1", "classification": "TEST_ONLY"}
            state["observations"].append(observation)
            details.update({"pendingCastAfter": None, "observation": observation, "concentrationAfter": copy.deepcopy(actor["concentration"]), "FortressAuraPerceived": True})
        elif kind == "COUNTER_CHILD_DISPEL":
            details.update(copy.deepcopy(inputs["childDispel"]["counterspellDispositionAt25_2"]))
        elif kind == "SECURE_CARGO":
            actor = state["actors"]["B"]
            item = state["items"]["cargo-B"]
            action = inputs["resourceLedger"]["B"]["cargoSecureAction"]
            if actor["action"] != 1 or item["custodian"] is not None or action["actor"] != "B":
                raise ValueError("Secure Cargo action does not match the adopted source state")
            actor["action"] = 0
            turns["B"]["spent"] = 1
            turns["B"]["kind"] = "SECURE_CARGO"
            actor["equipment"].append("cargo-B")
            actor["carriedWeightLb"] = 12
            actor["carriedLoad"] = 1.2
            item.update({"custodian": "B", "plane": actor["plane"], "position": None, "heldBy": "B:right", "heldBoundsFeet": None})
            details.update({"action": "Secure Cargo", "ActionSpent": 1, "custodianAfter": "B", "hand": "right", "extractionClass": 0, "classification": "OWNER_ADOPTED_TEST_ONLY_PREMISE", "weightAfterLb": 12, "loadAfter": 1.2})
        elif kind == "CHILD_ENTRY":
            actor = state["actors"]["B"]
            route_data = inputs["childEntry"]
            context = turns["B"]
            if actor["plane"] != ROOT_SPACE or actor["position"] != [15, 10, 0] or "cargo-B" not in actor["equipment"]:
                raise ValueError("Child route starts from unexpected B/cargo state")
            context["move"] += route_data["totalMovementFeet"]
            actor["movement"] -= route_data["totalMovementFeet"]
            actor["plane"] = CHILD_SPACE
            actor["position"] = route_data["route"][-1]["arrival"]
            item = state["items"]["cargo-B"]
            item["plane"] = CHILD_SPACE
            item["heldBoundsFeet"] = {"x": [4, 5], "y": [19, 20], "z": [3, 4]}
            details.update({"route": route_data["route"], "movementFeet": route_data["totalMovementFeet"], "remainingMovementFeet": actor["movement"], "arrivalPlane": actor["plane"], "arrivalPosition": actor["position"], "bodyFits": route_data["wholeBodyFits"], "cargoBRemainsHeld": True, "routeSweeps": inputs["geometryAudit"]["routeSweeps"]["B19.05"], "towerOpeningTraversal": inputs["geometryAudit"]["towerOpeningTraversal"], "doorClearance": inputs["geometryAudit"]["childArrival"]})
        elif kind == "CARGO_SETDOWN":
            actor = state["actors"]["B"]
            item = state["items"]["cargo-B"]
            placement = inputs["childEntry"]["cargoBAtEntry"]
            actor["equipment"].remove("cargo-B")
            actor["carriedWeightLb"] = 2
            actor["carriedLoad"] = 0.2
            item.update({"plane": CHILD_SPACE, "position": placement["releasedPosition"], "custodian": None, "heldBy": None, "heldBoundsFeet": None})
            item.setdefault("testOnlyGeometry", {})["currentBoundsFeet"] = {"x": [5, 6], "y": [15, 16], "z": [0, 1]}
            item["testOnlyGeometry"]["supportPatch"] = copy.deepcopy(inputs["childEntry"]["childFloorSupport"])
            details.update({"positionAfter": item["position"], "custodianAfter": None, "handAfter": "free", "carriedWeightAfterLb": 2, "carriedLoadAfter": 0.2, "supported": True})
        elif kind == "CHILD_DISPEL_RESOLVE":
            cast = state["pendingCast"]
            if not cast or cast["spellId"] != "wizard.arch.dispel-magic" or cast["caster"] != "B":
                raise ValueError("Child Dispel resolution lacks B's pending cast")
            state["pendingCast"] = None
            next(x for x in reversed(state["actors"]["B"]["spellHistory"]) if x["castId"] == cast["castId"]).update({"resolutionStatus": "SUCCESSFUL", "resolvedAt": time, "testOnlyCheck": inputs["childDispel"]["testOnlyIntelligenceCheck"]})
            state["effects"][CHILD_ID].update({"active": False, "endedAt": time, "terminalReason": "SUCCESSFUL_TEST_ONLY_ARCH_DISPEL", "doorEnded": True})
            state["spaces"][CHILD_SPACE].update({"exists": False, "endedAt": time})
            state["spaces"][CHILD_SPACE]["doors"][0]["open"] = False
            check = inputs["childDispel"]["testOnlyIntelligenceCheck"]
            details.update({"pendingCastAfter": None, "successful": check["success"], "check": check, "childEndedAt": time, "parentRemainsActive": state["effects"][ROOT_ID]["active"], "noEligibleResponder": True})
        elif kind == "P5_CLOSE_BODY":
            actor = state["actors"]["B"]
            settlement = inputs["childTerminalSettlement"]
            if state["effects"][CHILD_ID]["active"] or not state["effects"][ROOT_ID]["active"]:
                raise ValueError("P5-CLOSE requires child ended and parent active")
            actor["plane"] = ROOT_SPACE
            actor["position"] = settlement["BParentPosition"]
            actor["testOnlyP5CloseBodySupport"] = {"sourceRule": settlement["settlementRulePointer"], "parentPosition": settlement["BParentPosition"], "livingIdentityPreserved": True, "attachedItems": ["focus-B", "pack-B"]}
            for item_id in ("focus-B", "pack-B"):
                state["items"][item_id]["plane"] = ROOT_SPACE
            details.update({"actor": "B", "planeAfter": ROOT_SPACE, "positionAfter": actor["position"], "livingIdentityPreserved": True, "attachedItemsPreserved": True, "parentStillActive": True})
        elif kind == "P5_CLOSE_LOOSE":
            item = state["items"]["cargo-B"]
            settlement = inputs["childTerminalSettlement"]
            item.update({"plane": ROOT_SPACE, "position": settlement["cargoBParentPosition"], "custodian": None, "heldBy": None, "heldBoundsFeet": None})
            item.setdefault("testOnlyGeometry", {})["currentBoundsFeet"] = settlement["cargoBParentBounds"]
            item["testOnlyGeometry"]["supportPatchId"] = settlement["cargoBParentSupport"]["id"]
            details.update({"itemId": "cargo-B", "planeAfter": ROOT_SPACE, "positionAfter": item["position"], "custodianAfter": None, "supported": True, "parentStillActive": state["effects"][ROOT_ID]["active"], "settledExactlyOnce": True})
        elif kind == "COUNTER_PARENT_DISPEL":
            details.update(copy.deepcopy(inputs["parentDispel"]["counterspellDispositionAt30_2"]))
        elif kind == "PARENT_DISPEL_RESOLVE":
            cast = state["pendingCast"]
            if not cast or cast["spellId"] != "wizard.arch.dispel-magic" or cast["caster"] != "A":
                raise ValueError("Parent Dispel resolution lacks A's pending cast")
            state["pendingCast"] = None
            check = inputs["parentDispel"]["testOnlyIntelligenceCheck"]
            next(x for x in reversed(state["actors"]["A"]["spellHistory"]) if x["castId"] == cast["castId"]).update({"resolutionStatus": "SUCCESSFUL", "resolvedAt": time, "testOnlyCheck": check})
            details.update({"pendingCastAfter": None, "check": check, "successful": check["success"], "rootStillActiveUntilQ27": state["effects"][ROOT_ID]["active"], "AConcentrationPreserved": copy.deepcopy(state["actors"]["A"]["concentration"])})
        elif kind == "Q27_ROOT_END":
            effect = state["effects"][ROOT_ID]
            if effect["active"] is not True or state["pendingCast"] is not None:
                raise ValueError("Q27 cannot begin before successful parent Dispel resolution")
            effect.update({"active": False, "open": False, "terminalReceipt": {"time": time, "status": "ENDED_BY_SUCCESSFUL_DISPEL", "spellId": "wizard.arch.dispel-magic", "castId": casts["PARENT_DISPEL_COMMIT"], "scope": "TEST_ONLY PG328-W13-R1"}})
            state["spaces"][ROOT_SPACE]["exists"] = False
            for door in state["spaces"][ROOT_SPACE].get("doors", []):
                door["open"] = False
            details.update({"rootActiveAfter": False, "rootSpaceExistsAfter": False, "terminalReceipt": effect["terminalReceipt"], "campaignEventAsserted": False})
        elif kind == "Q27_BODY":
            actor_id = details["actor"]
            placement = inputs["rootTerminalClosure"][actor_id]
            actor = state["actors"][actor_id]
            if actor["death"]["status"] != "alive" or actor["HP"] != placement["HP"] or (actor_id == "A" and actor["form"] is not None):
                raise ValueError(f"Q27 body settlement precondition failed for {actor_id}")
            actor.update({"plane": "fixture:origin", "position": placement["reference"], "carriedWeightLb": placement["carriedWeightLb"], "carriedLoad": placement["carriedLoad"], "testOnlyQ27ClosurePose": {"bodyBounds": placement["bodyBounds"], "supportPatchId": placement["supportPatchId"], "attachedItems": placement["attachedItems"]}})
            for item_id, placement_data in placement["attachedItems"].items():
                item = state["items"][item_id]
                item["plane"] = "fixture:origin"
                item.setdefault("testOnlyGeometry", {})["currentBoundsFeet"] = placement_data["closureBounds"]
                item["testOnlyGeometry"]["containedInActorEnvelope"] = True
            details.update({"planeAfter": actor["plane"], "positionAfter": actor["position"], "bodyBoundsAfter": placement["bodyBounds"], "supportPatchId": placement["supportPatchId"], "livingIdentityPreserved": True, "HP": actor["HP"], "attachedItems": list(placement["attachedItems"])})
        elif kind == "Q27_LOOSE":
            item_id = details["itemId"]
            placement = next(x for x in inputs["rootTerminalClosure"]["looseItems"] if x["id"] == item_id)
            item = state["items"][item_id]
            item.update({"plane": "fixture:origin", "position": placement["outsidePosition"], "owner": placement["owner"], "custodian": placement["custodian"]})
            item.setdefault("testOnlyGeometry", {})["currentBoundsFeet"] = placement["bounds"]
            item["testOnlyGeometry"]["supportPatchId"] = placement["supportPatchId"]
            if item_id == TILE_ID:
                item["expiresAtEventTime"] = placement["expiry"]
            details.update({"planeAfter": item["plane"], "positionAfter": item["position"], "boundsAfter": placement["bounds"], "ownerAfter": item["owner"], "custodianAfter": item["custodian"], "expiryAfter": item.get("expiresAtEventTime"), "settledExactlyOnce": True})
        else:
            raise ValueError(f"Unhandled W13 event type {kind}")

        event_id = f"PG328-W13-R1-E{number:03d}"
        state["processedEventIds"].append(event_id)
        ops = diff(before, state)
        inverse_ops = inverse(ops)
        if apply_ops(before, ops) != state or apply_ops(state, inverse_ops) != before:
            raise ValueError(f"Local forward/inverse patch failed at {event_id}")
        entry["eventId"] = event_id
        entry["details"] = details
        entry["stateTransition"] = {"beforeStateSha256": object_sha(before), "afterStateSha256": object_sha(state), "forwardOperations": ops, "inverseOperations": inverse_ops}
        events.append(entry)

    if events and "kind" not in events[0]:
        raise ValueError(f"Internal event lost kind; keys={list(events[0])}")
    starts = sum(x["kind"] in {"START", "A_START_SIGHT_TICK", "B_START_CHILD_DISPEL", "A_START_PARENT_DISPEL"} for x in events)
    ends = sum(x["kind"] in {"END", "B_END_EFF_EXPIRY"} for x in events)
    if (starts, ends, state["time"]) != (12, 11, 30.31):
        raise ValueError(f"Unexpected W13 marker counts or endpoint: {starts}/{ends}/{state['time']}")

    forward_state = copy.deepcopy(initial)
    forward_pass = True
    for event in events:
        transition = event["stateTransition"]
        if object_sha(forward_state) != transition["beforeStateSha256"]:
            forward_pass = False
            break
        forward_state = apply_ops(forward_state, transition["forwardOperations"])
        if object_sha(forward_state) != transition["afterStateSha256"]:
            forward_pass = False
            break
    reverse_state = copy.deepcopy(forward_state)
    inverse_pass = True
    for event in reversed(events):
        transition = event["stateTransition"]
        if object_sha(reverse_state) != transition["afterStateSha256"]:
            inverse_pass = False
            break
        reverse_state = apply_ops(reverse_state, transition["inverseOperations"])
        if object_sha(reverse_state) != transition["beforeStateSha256"]:
            inverse_pass = False
            break
    if not forward_pass or forward_state != state or not inverse_pass or reverse_state != initial or object_sha(reverse_state) != S030_SHA:
        raise ValueError("W13 forward/inverse replay did not restore exact S030")

    closure = inputs["rootTerminalClosure"]
    bounds = {"A": closure["A"]["bodyBounds"], "B": closure["B"]["bodyBounds"]}
    bounds.update({x["id"]: x["bounds"] for x in closure["unchangedOutsideActors"]})
    bounds.update({x["id"]: x["bounds"] for x in closure["looseItems"]})
    names = list(bounds)
    collision_pairs = [{"pair": [left, right], "positiveVolumeOverlap": bounds_overlap(bounds[left], bounds[right])} for i, left in enumerate(names) for right in names[i+1:]]
    if len(collision_pairs) != inputs["geometryAudit"]["rootQ27ExteriorCollisionPairCount"] or any(x["positiveVolumeOverlap"] for x in collision_pairs):
        raise ValueError("W13 Q27 origin-plane collision test failed")
    geometry = inputs["geometryAudit"]
    if any(x["hitCount"] != 0 for group in geometry["routeSweeps"].values() for x in group):
        raise ValueError("Adopted route sweep has a Geometry405 positive-volume collision")
    if not geometry["towerOpeningTraversal"]["routeBodyFits"] or not geometry["childArrival"]["immediatelyAdjacent"] or len(geometry["parentP5CloseCollisionPairs"]) != 6 or any(x["positiveVolumeOverlap"] for x in geometry["parentP5CloseCollisionPairs"]):
        raise ValueError("Adopted route/child-entry/P5-CLOSE geometry checks failed")
    if geometry["rays"]["AArcaneSight"]["clear"] is not True or geometry["rays"]["AParentDispel"]["clear"] is not True or geometry["rays"]["BChildDispel"]["clear"] is not True:
        raise ValueError("A W13 perception/Dispel ray is not clear")

    actor_a, actor_b = state["actors"]["A"], state["actors"]["B"]
    terminal_checks = {
        "A_RP": actor_a["RP"], "B_RP": actor_b["RP"], "A_SightRecharge": actor_a["recharge"].get("wizard.arch.arcane-sight"),
        "A_DispelRecharge": actor_a["recharge"].get("wizard.arch.dispel-magic"), "B_DispelRecharge": actor_b["recharge"].get("wizard.arch.dispel-magic"),
        "A_SightConcentrationDeadline": actor_a["concentration"]["deadline"], "B_position": actor_b["position"],
        "childEndedBeforeParent": state["effects"][CHILD_ID]["active"] is False and state["effects"][ROOT_ID]["active"] is False,
        "pendingCast": state["pendingCast"], "tileExpiry": state["items"][TILE_ID]["expiresAtEventTime"]
    }
    expected = {"A_RP": 48, "B_RP": 56, "A_SightRecharge": 0, "A_DispelRecharge": 2, "B_DispelRecharge": 2, "A_SightConcentrationDeadline": 618.1, "B_position": [5, 15, 0], "childEndedBeforeParent": True, "pendingCast": None, "tileExpiry": 3606.13}
    if terminal_checks != expected:
        raise ValueError(f"W13 terminal ledger mismatch: {terminal_checks}")

    director_meta = {"path": repo_path(DIRECTOR), "bytes": DIRECTOR.stat().st_size, "sha256": file_sha(DIRECTOR), "W13Status": director["W13"]["status"], "proposalSha256": director["W13"]["proposalSha256"]}
    queue_meta = {"path": repo_path(QUEUE), "bytes": QUEUE.stat().st_size, "sha256": file_sha(QUEUE), "reviewedApplied": queue_doc["currentAuthority"]["reviewedApplied"], "pending": queue_doc["currentAuthority"]["pending"], "acceptedUnapplied": queue_doc["currentAuthority"]["acceptedUnapplied"], "mutated": False}
    if (queue_meta["reviewedApplied"], queue_meta["pending"], queue_meta["acceptedUnapplied"]) != (830, 18, 0):
        raise ValueError("Queue authority changed during W13 witness construction")

    witness = {
        "schemaVersion": 1,
        "id": "PG328-W13-REVERSIBLE-WITNESS-469",
        "classification": "OWNER_ADOPTED_TEST_ONLY_BRANCH_WITNESS",
        "status": "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW",
        "branchId": "PG328-W13-R1",
        "component": "PG328-W13",
        "hypotheticalOnly": True,
        "noCampaignEventClaim": True,
        "adoption": {"path": repo_path(ADOPTION), "sha256": actual_adoption_sha, "proposalPath": repo_path(PROPOSAL), "exactProposalSha256": actual_proposal_sha, "ownerAdopted": True, "scope": "PG328-W13-R1 only"},
        "adoptedBranchPremises": [{"proposalPointer": "/ownerProposedInputs/resourceLedger/B/cargoExtractionClassPremise", "adoptionPath": repo_path(ADOPTION), "proposalSha256": actual_proposal_sha, "statusInThisWitness": "OWNER_ADOPTED_TEST_ONLY_PREMISE", "scope": "PG328-W13-R1 only", "canonicalOrCampaignEffect": False, "note": "Proposal448's embedded pre-adoption status text is retained byte-for-byte in adoptedScenario; this separate readback records the later exact owner adoption."}],
        "parent": {"path": repo_path(PARENT), "pointer": "/stateSnapshots/S030", "replaySha256": file_sha(PARENT), "snapshotSha256": object_sha(initial), "timeSeconds": initial["time"], "parentMutated": False},
        "directorReadiness": director_meta,
        "sourceBindings": bindings,
        "adoptedScenario": inputs,
        "eventTrace": {"semantics": "Ordered TEST_ONLY state reconstruction from exact W01-403 S030; Proposal448 inputs only; P5-CLOSE ends the child while the parent remains active, then Q27 ends the parent and settles the declared root identities.", "eventCount": len(events), "regularTurnStartCount": starts, "regularTurnEndCount": ends, "events": events, "lifecycleEvents": life, "terminalProjection": closure, "q27CollisionPairs": collision_pairs, "closureOrder": ["P5-CLOSE child source", "P5-CLOSE B body and attached equipment", "P5-CLOSE loose cargo-B", "Q27 parent source", "Q27 A body", "Q27 B body", *closure["looseItemOrderByStableId"]]},
        "stateTransitionReplay": {"classification": "TEST_ONLY_REVERSIBLE_BRANCH_STATE_RECONSTRUCTION", "initialStatePath": repo_path(PARENT) + "#/stateSnapshots/S030", "initialState": initial, "initialStateSha256": object_sha(initial), "terminalState": state, "terminalStateSha256": object_sha(state), "eventsAreAppliedInOrder": True, "eventCount": len(events), "forwardOperationsTotal": sum(len(x["stateTransition"]["forwardOperations"]) for x in events), "inverseOperationsTotal": sum(len(x["stateTransition"]["inverseOperations"]) for x in events), "reverseRestorationExpectedSha256": S030_SHA, "forwardReplayPass": forward_pass, "inverseReplayPass": inverse_pass},
        "terminalStateSummary": {"A": {"RP": actor_a["RP"], "HP": actor_a["HP"], "position": actor_a["position"], "plane": actor_a["plane"], "concentration": actor_a["concentration"], "recharge": actor_a["recharge"]}, "B": {"RP": actor_b["RP"], "HP": actor_b["HP"], "position": actor_b["position"], "plane": actor_b["plane"], "concentration": actor_b["concentration"], "recharge": actor_b["recharge"]}, "tileExpiry": state["items"][TILE_ID]["expiresAtEventTime"], "childActive": state["effects"][CHILD_ID]["active"], "rootActive": state["effects"][ROOT_ID]["active"], "pendingCast": state["pendingCast"]},
        "queue": queue_meta,
        "scopeBoundary": {"testOnly": True, "sealPresent": False, "FortressAcceptedOrApplied": False, "canonicalRuleChanged": False, "campaignEventsAsserted": False, "queueChanged": False, "PG200_B06Closed": False, "W05W10W11W12OutcomesImported": False, "ElementalShellEncounterConstructed": False}
    }
    dump(WITNESS, witness)
    trace = {"classification": "TEST_ONLY_REVERSIBLE_BRANCH_STATE_RECONSTRUCTION", "witnessPath": repo_path(WITNESS), "witnessSha256": file_sha(WITNESS), "initialStateSha256": S030_SHA, "terminalStateSha256": object_sha(state), "terminalTime": state["time"], "starts": starts, "ends": ends, "eventCount": len(events), "events": events, "terminalState": state, "q27CollisionPairs": collision_pairs, "authority": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0, "mutation": False}}
    dump(TRACE, trace)

    validation_checks = {
        "exact Proposal448 hash and owner adoption scope": actual_proposal_sha == PROPOSAL_SHA and actual_adoption_sha == ADOPTION_SHA and adoption["scope"]["branchId"] == "PG328-W13-R1",
        "exact W01-403 S030 parent bytes and state hash": file_sha(PARENT) == PARENT_REPLAY_SHA and object_sha(initial) == S030_SHA,
        "all 17 adopted source bindings match SHA and Git blob": len(bindings) == 17 and all(x["matches"] for x in bindings),
        "adopted scenario preserved without added premises": witness["adoptedScenario"] == inputs,
        "12 START and 11 END markers processed": starts == 12 and ends == 11,
        "four spell casts paid at adopted base cost": [(x["details"].get("spellId"), x["details"].get("costRP")) for x in events if x["kind"] in spell_specs] == [("demiplane", 21), ("wizard.arch.arcane-sight", 2), ("wizard.arch.dispel-magic", 3), ("wizard.arch.dispel-magic", 3)],
        "Counterspell decisions preserve ineligible/no-responder/declines": all(x["kind"] in {"COUNTER_DEMIPLANE", "COUNTER_SIGHT", "COUNTER_CHILD_DISPEL", "COUNTER_PARENT_DISPEL"} for x in events if x["kind"].startswith("COUNTER_")),
        "child room closes before parent and parent survives P5-CLOSE": state["effects"][CHILD_ID]["active"] is False and state["effects"][ROOT_ID]["active"] is False and next(x for x in events if x["kind"] == "P5_CLOSE_BODY")["details"]["parentStillActive"],
        "all adopted movement/ray/door geometry checks clear": all(x["hitCount"] == 0 for group in geometry["routeSweeps"].values() for x in group) and geometry["towerOpeningTraversal"]["routeBodyFits"] and all(x["clear"] for x in geometry["rays"].values()),
        "15 Q27 collision pairs have no positive-volume overlap": len(collision_pairs) == 15 and not any(x["positiveVolumeOverlap"] for x in collision_pairs),
        "terminal RP, recharge, concentration, expiry and child closure match Proposal448": terminal_checks == expected,
        "forward event replay and inverse restoration pass": forward_pass and inverse_pass and reverse_state == initial,
        "queue and Fortress hold preserved": (queue_meta["reviewedApplied"], queue_meta["pending"], queue_meta["acceptedUnapplied"]) == (830, 18, 0) and witness["scopeBoundary"]["PG200_B06Closed"] is False,
        "no seal, acceptance, application, canon or campaign event asserted": witness["status"] == "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW" and not witness["scopeBoundary"]["sealPresent"] and not witness["scopeBoundary"]["FortressAcceptedOrApplied"] and witness["noCampaignEventClaim"]
    }
    failed = [name for name, passed in validation_checks.items() if not passed]
    if failed:
        raise ValueError("Validation failed: " + "; ".join(failed))
    dump(VALIDATION, {"id": "BUILD-VALIDATION-W13-469", "status": "PASS", "passed": len(validation_checks), "failed": 0, "checks": [{"name": name, "passed": passed} for name, passed in validation_checks.items()], "witnessSha256": file_sha(WITNESS), "traceSha256": file_sha(TRACE), "events": len(events), "starts": starts, "ends": ends, "forwardOperations": witness["stateTransitionReplay"]["forwardOperationsTotal"], "inverseOperations": witness["stateTransitionReplay"]["inverseOperationsTotal"], "terminalStateSha256": object_sha(state), "sourceBindings": len(bindings), "queue": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0}, "Fortress": "HELD_UNDER_PG200-B06", "sealed": False})

    README.write_text("""# W13 reversible witness 469 — TEST_ONLY / unsealed

This package constructs only the owner-adopted PG328-W13-R1 hypothetical branch under the exact Proposal448 hash. It starts from unchanged W01-403 terminal S030, records the 12 START and 11 END markers, and applies only Proposal448's Demiplane, cargo, movement, perception, Dispel, P5-CLOSE, and Q27 inputs.

The ordered replay preserves cast costs, budgets, recharge, concentration, Spell Efficiency deadlines, hand state, cargo custody, child-room creation and termination, parent survival at P5-CLOSE, and the later Fortress closure. It checks the adopted route/ray/aperture evidence and all 15 Q27 placement pairs. Forward and inverse state operations restore the exact S030 hash.

The witness is TEST_ONLY and unsealed. It asserts no campaign event, changes no canonical rule or queue state, and does not accept or apply the Fortress identity. PG200-B06 remains held; the recorded queue authority is 830 applied / 18 pending / 0 accepted-unapplied. No W05/W10/W11/W12 outcomes are imported.
""", encoding="utf-8", newline="\n")

    package_paths = [WITNESS, TRACE, VALIDATION, README, VERIFIER, PROPOSAL, ADOPTION, DIRECTOR]
    manifest_artifacts = []
    for path in package_paths:
        raw = path.read_bytes()
        manifest_artifacts.append({"path": repo_path(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
    manifest = {"id": "MANIFEST-W13-469", "classification": "TEST_ONLY_REVERSIBLE_WITNESS", "branchId": "PG328-W13-R1", "artifacts": manifest_artifacts, "sourceBindings": bindings, "authority": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0}, "Fortress": "HELD_UNDER_PG200-B06", "sealed": False}
    dump(MANIFEST, manifest)
    archive_members = [WITNESS, TRACE, VALIDATION, README, VERIFIER, MANIFEST, PROPOSAL, ADOPTION, DIRECTOR]
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in archive_members:
            archive.write(path, arcname=path.name)
    archive_sha = file_sha(ARCHIVE)
    delivery = {"id": "DELIVERY-W13-469", "status": "READY_FOR_DIRECTOR_REVIEW", "classification": "TEST_ONLY_UNSEALED", "witness": {"path": repo_path(WITNESS), "bytes": WITNESS.stat().st_size, "sha256": file_sha(WITNESS)}, "trace": {"path": repo_path(TRACE), "bytes": TRACE.stat().st_size, "sha256": file_sha(TRACE)}, "validation": {"path": repo_path(VALIDATION), "bytes": VALIDATION.stat().st_size, "sha256": file_sha(VALIDATION)}, "manifest": {"path": repo_path(MANIFEST), "bytes": MANIFEST.stat().st_size, "sha256": file_sha(MANIFEST)}, "archive": {"path": repo_path(ARCHIVE), "bytes": ARCHIVE.stat().st_size, "sha256": archive_sha}, "sourceBindingCount": len(bindings), "eventCount": len(events), "starts": starts, "ends": ends, "forwardReplayPass": forward_pass, "inverseReplayPass": inverse_pass, "authority": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0}, "Fortress": "HELD_UNDER_PG200-B06", "sealed": False, "campaignEventAsserted": False, "canonChanged": False}
    dump(DELIVERY, delivery)
    print(json.dumps({"status": "PASS", "checks": len(validation_checks), "events": len(events), "starts": starts, "ends": ends, "sourceBindings": len(bindings), "forwardOperations": witness["stateTransitionReplay"]["forwardOperationsTotal"], "inverseOperations": witness["stateTransitionReplay"]["inverseOperationsTotal"], "witnessSha256": file_sha(WITNESS), "traceSha256": file_sha(TRACE), "archiveSha256": archive_sha, "terminalStateSha256": object_sha(state)}, indent=2))


if __name__ == "__main__":
    main()
