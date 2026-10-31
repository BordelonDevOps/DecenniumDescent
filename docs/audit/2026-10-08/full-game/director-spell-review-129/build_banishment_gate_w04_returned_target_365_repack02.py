from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import zipfile
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
W06_OUT = BASE / "banishment_gate_witness365_w06_planes_shift_repack06_verified04"
W06_ZIP = W06_OUT / "DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack06_TESTONLY.zip"
W06_AUDIT = W06_OUT / "INDEPENDENT_AUDIT_365_REPACK06.json"
W06_SEAL = BASE / "PG327_W06_DIRECTOR_SEAL_365_REPACK06.json"
W04_PREV_OUT = BASE / "banishment_gate_witness365_w04_returned_target_verified02"
W04_PREV_ZIP = W04_PREV_OUT / "DD_Rank9_BanishmentGate_W04_ReturnedTarget_365_Repack01_TESTONLY.zip"
W04_PREV_AUDIT = W04_PREV_OUT / "INDEPENDENT_AUDIT_365_W04_REPACK01.json"
W04_PREV_DELIVERY = W04_PREV_OUT / "ARCHIVE_DELIVERY_365_W04_REPACK01.json"
W04_PREV_HOLD = BASE / "PG327_W04_DIRECTOR_HOLD_365_REPACK01.json"
PLAN = BASE / "PG327_W01_W08_WITNESS_PLAN_361.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_361.json"
OUT = BASE / "banishment_gate_witness365_w04_returned_target_verified03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W04_ReturnedTarget_365_Repack02_TESTONLY.zip"
CASE_NAME = "W04_RETURNED_TARGET_CASE_365_REPACK02.json"
CASE_ID = "W04_RETURNED_TARGET_CASE_365_REPACK02"
GATE_ID = "BG-W06-TESTONLY-GATE-365"
CELL_ID = "BG-W06-TESTONLY-CELL-GUARD-365"
TARGET_ID = "Guard-W06-TESTONLY"
CREATOR_ID = "W20"
ENCOUNTER_ID = "fixture:banishment-gate-w06-365"
ENC = "utf-8"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding=ENC)


def changed_paths(before, after, path=""):
    if type(before) is dict and type(after) is dict:
        result = []
        for key in sorted(before.keys() | after.keys()):
            child = path + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key not in before or key not in after:
                result.append(child)
            else:
                result.extend(changed_paths(before[key], after[key], child))
        return result
    if type(before) is type(after) and before == after:
        return []
    assert path
    return [path]


def pointer_parts(path):
    return [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")] if path else []


def get_at(obj, path):
    value = obj
    for part in pointer_parts(path):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def parent_at(obj, path):
    parts = pointer_parts(path)
    parent = obj
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


def operations(before, after):
    forward, inverse = [], []
    for path in changed_paths(before, after):
        try:
            old = get_at(before, path)
            has_old = True
        except (KeyError, IndexError):
            old, has_old = None, False
        try:
            new = get_at(after, path)
            has_new = True
        except (KeyError, IndexError):
            new, has_new = None, False
        if has_old:
            forward.append({"op": "test", "path": path, "value": old})
        if has_new:
            forward.append({"op": "replace" if has_old else "add", "path": path, "value": new})
        else:
            forward.append({"op": "remove", "path": path})
        if has_new:
            inverse.append({"op": "test", "path": path, "value": new})
        if has_old:
            inverse.append({"op": "replace" if has_new else "add", "path": path, "value": old})
        else:
            inverse.append({"op": "remove", "path": path})
    return forward, inverse


def apply_ops(state, ops):
    current = copy.deepcopy(state)
    for op in ops:
        path, kind = op["path"], op["op"]
        if kind == "test":
            actual = get_at(current, path)
            assert actual == op["value"], f"precondition {path}; actual={actual!r}; expected={op['value']!r}"
            continue
        parent, key = parent_at(current, path)
        if isinstance(parent, list):
            index = int(key)
            if kind == "replace":
                parent[index] = copy.deepcopy(op["value"])
            elif kind == "remove":
                parent.pop(index)
            elif kind == "add":
                parent.insert(index, copy.deepcopy(op["value"]))
            else:
                raise AssertionError(f"unsupported list op: {kind}")
        elif kind == "add":
            assert key not in parent
            parent[key] = copy.deepcopy(op["value"])
        elif kind == "replace":
            assert key in parent
            parent[key] = copy.deepcopy(op["value"])
        elif kind == "remove":
            assert key in parent
            del parent[key]
        else:
            raise AssertionError(f"unsupported op: {kind}")
    return current


if ARCHIVE.exists() or (OUT / "ARCHIVE_DELIVERY_365_W04_REPACK02.json").exists():
    raise SystemExit(f"Refusing to overwrite completed W04 delivery: {OUT}")
assert all(p.is_file() for p in (W06_ZIP, W06_AUDIT, W06_SEAL, W04_PREV_ZIP, W04_PREV_AUDIT,
                                  W04_PREV_DELIVERY, W04_PREV_HOLD, PLAN, QUEUE))
OUT.mkdir(parents=True, exist_ok=True)
PACK.mkdir(parents=True, exist_ok=True)
prior = PACK / "prior"
prior.mkdir(parents=True, exist_ok=True)
(PACK / "authority").mkdir(parents=True, exist_ok=True)
shutil.copyfile(W06_ZIP, prior / W06_ZIP.name)
shutil.copyfile(W06_AUDIT, prior / W06_AUDIT.name)
shutil.copyfile(W06_SEAL, prior / W06_SEAL.name)
shutil.copyfile(W04_PREV_ZIP, prior / W04_PREV_ZIP.name)
shutil.copyfile(W04_PREV_AUDIT, prior / W04_PREV_AUDIT.name)
shutil.copyfile(W04_PREV_DELIVERY, prior / W04_PREV_DELIVERY.name)
shutil.copyfile(W04_PREV_HOLD, prior / W04_PREV_HOLD.name)
previous_supersession = {
    "id": "PG327-W04-SUPERSESSION-365-REPACK02",
    "supersedes": {"archive": W04_PREV_ZIP.name, "archiveSha256": file_sha(W04_PREV_ZIP.read_bytes()),
                   "audit": W04_PREV_AUDIT.name, "directorDisposition": W04_PREV_HOLD.name,
                   "dispositionId": "PG327-W04-365-REPACK01-DIRECTOR-HOLD"},
    "reason": "Closes timeline processing residuals R1/R2/R3 identified by the Director; preserves Repack01 and the HOLD unchanged as review history.",
    "scope": "TEST_ONLY W04 witness evidence; no identity acceptance or application"
}
write_json(prior / "W04_REPACK01_SUPERSESSION_365.json", previous_supersession)
shutil.copyfile(PLAN, PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json")
shutil.copyfile(QUEUE, PACK / "authority/CURRENT_SPELL_QUEUE_361.json")

with zipfile.ZipFile(W06_ZIP) as zf:
    w06_case = json.loads(zf.read("W06_PLANESHIFT_ESCAPE_CASE_365_REPACK06.json"))
    source_bindings = json.loads(zf.read("W06_SOURCE_BINDINGS_365.json"))
    seal_copy = json.loads(W06_SEAL.read_text(encoding=ENC))
    assert w06_case["events"][7]["kind"] == "VOLUNTARY_COMPLETE_CROSSING_AND_ADMISSION"
    initial = copy.deepcopy(w06_case["events"][7]["after"])
    gate_bytes = zf.read(source_bindings["fixtureSpecificBindings"]["Gate"]["packetMember"])
    gate_member = "sources/RETURN327_banishment-gate.json"
    (PACK / gate_member).parent.mkdir(parents=True, exist_ok=True)
    (PACK / gate_member).write_bytes(gate_bytes)
    (PACK / "W06_SOURCE_BINDINGS_365.json").write_bytes(zf.read("W06_SOURCE_BINDINGS_365.json"))
    prior_event = copy.deepcopy(w06_case["events"][7])

source_record = source_bindings["fixtureSpecificBindings"]["Gate"]
source_commit = source_bindings["sourceCommit"]
gate_source_path = source_record["sourcePath"]
assert source_record["sourceBindingIndex"] == 11
assert gate_source_path == source_bindings["bindings"][11]["repositoryPath"]
assert file_sha(gate_bytes) == source_record["sha256"]
assert subprocess.check_output(["git", "show", f"{source_commit}:{gate_source_path}"], cwd=ROOT) == gate_bytes

w06_sha = file_sha(W06_ZIP.read_bytes())
w06_audit = json.loads(W06_AUDIT.read_text(encoding=ENC))
assert seal_copy["archiveSha256"] == w06_sha and w06_audit["archiveSha256"] == w06_sha
assert seal_copy["witnessDecision"] == "SEALED_TEST_ONLY" and seal_copy["identityDecision"] == "HOLD"
assert seal_copy["remainingWitnessIds"][0] == "W01" and "W04" in seal_copy["remainingWitnessIds"]

guard = initial["actors"][TARGET_ID]
gate = initial["effects"][GATE_ID]
cell = initial["cells"][CELL_ID]
assert guard["lifeClassification"] == "ALIVE_LIVING_TEST_ONLY_FIXTURE"
assert gate["status"] == "active" and gate["creatorId"] == CREATOR_ID
assert cell["status"] == "active" and cell["primaryTargetId"] == TARGET_ID and cell["deadline"] == 62.05
claim = {"creatorId": CREATOR_ID, "targetId": TARGET_ID, "encounterId": ENCOUNTER_ID,
         "claimId": "claim-Guard-365", "spentAt": 2.05}
assert claim in initial["hardDenialClaims"]
original_crossing_id = f"{GATE_ID}/crossing/1"
assert original_crossing_id in initial["crossingReceipts"]

events = []
state = copy.deepcopy(initial)


def add_event(event_id, event_time, kind, narrative, authored, mutate):
    global state
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    after["time"] = event_time
    mutate(after)
    if event_id not in after["processedEventIds"] and not authored.get("duplicateDelivery", False):
        after["processedEventIds"].append(event_id)
    fwd, inv = operations(before, after)
    assert apply_ops(before, fwd) == after
    assert apply_ops(after, inv) == before
    events.append({"id": event_id, "time": event_time, "kind": kind, "narrative": narrative,
                   "authoredInputs": authored, "before": before, "after": after,
                   "beforeSHA256": sha(before), "afterSHA256": sha(after), "forward": fwd, "inverse": inv})
    state = after


# Record every scheduled start/end between the original admission and cell deadline.
schedule_events = []
deadline = cell["deadline"]
for actor_id, actor in state["actors"].items():
    sched = actor.get("regularSchedule")
    if not sched:
        continue
    if sched.get("nextEnd", 0) <= sched["nextStart"] and state["time"] < sched["nextEnd"] <= deadline - 0.05 + 1e-9:
        schedule_events.append((sched["nextEnd"], "end", actor_id))
    start = sched["nextStart"]
    while start <= deadline - 0.05 + 1e-9:
        end = start + (sched["endOffset"] - sched["firstStart"])
        schedule_events.append((start, "start", actor_id))
        if end <= deadline - 0.05 + 1e-9:
            schedule_events.append((end, "end", actor_id))
        start += sched["period"]
# Treat the inherited TEST_ONLY observation marker as a once-only no-op after Guard's
# simultaneous regular start. This does not mutate the sealed initial fork.
schedule_events.append((20.0, "marker", "fixture-independence-marker-365"))
phase_order = {"end": 0, "start": 1, "marker": 2}
for t, phase, actor_id in sorted(schedule_events, key=lambda x: (x[0], phase_order[x[1]], x[2])):
    eid = f"W04-365:{actor_id}:{phase}:{t:.2f}"
    if phase == "marker":
        def handle_observation_marker(s, when=t, key=actor_id):
            deadlines = s["clocks"]["otherIndependentDeadlines"]
            assert deadlines.get(key) == when and key not in s.get("clockReceipts", {})
            del deadlines[key]
            s.setdefault("clockReceipts", {})[key] = {
                "markerId": key, "dueAt": when, "handledAt": when,
                "classification": "TEST_ONLY observation-only marker; not a campaign or engine timer",
                "result": "NO_OP", "onceOnly": True, "inWorldConsequence": False,
                "orderedAfter": "Guard regular start at 20.0"
            }
        add_event(eid, t, "OBSERVATION_ONLY_DEADLINE_NOOP",
                  "The inherited TEST_ONLY observation marker is classified and consumed once after Guard's simultaneous regular start; it has no in-world effect.",
                  {"markerId": actor_id, "classification": "TEST_ONLY observation-only marker; not a campaign or engine timer",
                   "result": "NO_OP", "onceOnly": True, "orderedAfter": "Guard regular start at 20.0",
                   "noWorldEffect": True}, handle_observation_marker)
    elif phase == "start":
        def refresh(s, aid=actor_id, when=t):
            a = s["actors"][aid]
            rs = a["regularSchedule"]
            budget = rs["budgetHistory"][-1] if rs["budgetHistory"] else {
                "Action": 1, "BonusAction": 1, "Reaction": 1,
                "Movement": a.get("movementSpeedFeet", a.get("speedFeet", a.get("speed", 30)))
            }
            old_stance = a.get("stance") or {}
            if old_stance and when >= old_stance.get("expiresAtNextRegularStart", float("inf")):
                if a.get("stanceHistory") and "expiredAt" not in a["stanceHistory"][-1]:
                    a["stanceHistory"][-1]["expiredAt"] = when
                a["stance"] = None
            old_allowance = a.get("mobileFirstFiveFeetAllowance")
            if old_allowance and when >= old_allowance.get("expiresAtNextRegularStart", float("inf")):
                old_allowance["remainingFeet"] = 0
                old_allowance["expiredAt"] = when
            a["action"] = budget.get("Action", budget.get("action", 1))
            a["bonusAction"] = budget.get("BonusAction", budget.get("bonusAction", 1))
            a["reaction"] = budget.get("Reaction", budget.get("reaction", 1))
            a["movement"] = budget.get("Movement", budget.get("movement", a.get("speedFeet", a.get("speed", 30))))
            if "magicThisTurn" in a:
                a["magicThisTurn"] = False
            rs["starts"].append(when)
            rs["budgetHistory"].append({"time": when, "Action": a["action"], "BonusAction": a["bonusAction"],
                                        "Reaction": a["reaction"], "Movement": a["movement"]})
            rs["nextStart"] = when + rs["period"]
            rs["nextEnd"] = when + (rs["endOffset"] - rs["firstStart"])
            # Explicit hypothetical TEST_ONLY Mobile choice, recorded at turn start
            # before any activity or idle turn end for every scheduled fixture actor.
            stance = {"id": "Mobile", "selectedAt": when,
                      "expiresAtNextRegularStart": when + rs["period"],
                      "noOpportunityAttackForFirstFiveFeetOfActualVoluntaryMovement": True,
                      "grantsFreeMovement": False, "opportunityAttackDamageDieReduction": 1,
                      "testOnlySelection": True}
            a["stance"] = copy.deepcopy(stance)
            a.setdefault("stanceHistory", []).append(copy.deepcopy(stance))
            a["mobileFirstFiveFeetAllowance"] = {
                "totalFeet": 5, "usedFeet": 0, "remainingFeet": 5,
                "grantsFreeMovement": False,
                "expiresAtNextRegularStart": when + rs["period"]
            }
        add_event(eid, t, "REGULAR_START", f"{actor_id} receives its scheduled regular-start refresh and records a hypothetical TEST_ONLY Mobile stance choice before acting or waiting.",
                  {"actorId": actor_id, "scheduledStart": t, "turnBudgetRefreshed": True,
                   "optionalActionsTaken": [], "testOnlyWaitChoice": True,
                   "testOnlyStanceChoice": "Mobile", "stanceSelectedBeforeActivityOrIdleEnd": True}, refresh)
    else:
        def end_turn(s, aid=actor_id, when=t):
            a = s["actors"][aid]
            rs = a["regularSchedule"]
            assert rs["nextEnd"] == when
            rs["ends"].append(when)
            rs["nextEnd"] = when + rs["period"]
            a["action"] = 0
            a["bonusAction"] = 0
            a["movement"] = 0
            # Reaction intentionally survives regular end.
        before_reaction = state["actors"][actor_id].get("reaction")
        add_event(eid, t, "REGULAR_END", f"{actor_id}'s scheduled regular turn ends; unused Action, Bonus Action and Movement expire, while Reaction remains.",
                  {"actorId": actor_id, "scheduledEnd": t, "optionalActionsTaken": [],
                   "testOnlyWaitChoice": True, "unusedActionExpired": True,
                   "unusedBonusActionExpired": True, "unusedMovementExpired": True,
                   "reactionPreserved": True, "reactionBefore": before_reaction}, end_turn)


def close_expired_cell(s):
    a = s["actors"][TARGET_ID]
    c = s["cells"][CELL_ID]
    g = s["effects"][GATE_ID]
    assert c["status"] == "active" and c["deadline"] == s["time"] == 62.05
    assert s["time"] < g["endsAt"] and g["status"] == "active"
    anchor = c["originAnchor"]
    a["plane"] = anchor["plane"]
    a["position"] = copy.deepcopy(anchor["position"])
    a["bodyBoxWorld"] = copy.deepcopy(anchor["bodyBox"])
    c.update({"status": "destroyed", "closedAt": s["time"], "closeCount": 1, "contents": [],
              "closureReason": "independent 60-second Banishment Gate cell deadline", "terminalIdentityPreserved": True})
    g["cells"].remove(CELL_ID)
    s["settlements"].append({"settlementId": "W04-365-CELL-DEADLINE-RETURN", "cellId": CELL_ID,
                             "trigger": "independent cell deadline", "resolvedAt": s["time"],
                             "returnedTargetId": TARGET_ID, "targetLifeStatus": "alive",
                             "sameIdentityPreserved": True, "claimPreserved": True, "cellDestroyed": True})


add_event("W04-365:CELL-DEADLINE-RETURN", 62.05, "CELL_DEADLINE_AND_LAWFUL_RETURN",
          "At the cell's own 60-second deadline, the same living primary returns to its fixed origin anchor under the mandatory closure rule. The parent Gate and its original encounter claim remain active and unchanged.",
          {"cellId": CELL_ID, "primaryId": TARGET_ID, "admittedAt": 2.05, "deadline": 62.05,
           "trigger": "BAN-CLOSE-03 independent cell deadline", "mandatoryReturn": True,
           "targetRemainsAlive": True, "identityPreserved": True, "creatorId": CREATOR_ID,
           "encounterId": ENCOUNTER_ID, "existingClaimId": "claim-Guard-365", "gateMustRemainActive": True}, close_expired_cell)


def later_crossing(s):
    a = s["actors"][TARGET_ID]
    g = s["effects"][GATE_ID]
    assert g["status"] == "active" and s["time"] < g["endsAt"]
    assert claim in s["hardDenialClaims"]
    assert a["movement"] >= 5 and a["plane"] == "fixture:origin"
    start = copy.deepcopy(a["position"])
    end = [-2.5, -2.5, 0]
    before_box = copy.deepcopy(a["bodyBoxWorld"])
    after_box = {"x": [-5, 0], "y": [-5, 0], "z": [0, 6]}
    a["movement"] -= 5
    mobile = a["mobileFirstFiveFeetAllowance"]
    assert a["stance"]["id"] == "Mobile" and mobile["remainingFeet"] >= 5
    mobile["usedFeet"] += 5
    mobile["remainingFeet"] -= 5
    mobile["usedAt"] = s["time"]
    mobile["opportunityAttacksPrevented"] = 0
    mobile["noOpportunityAttackTriggered"] = True
    a["position"] = end
    a["bodyBoxWorld"] = copy.deepcopy(after_box)
    a["movementHistory"].append({"time": s["time"], "from": start, "to": end, "feetSpent": 5,
                                  "walletBefore": 40, "walletAfter": 35, "pathClear": True,
                                  "difficultTerrain": False, "movementPreventingCondition": False,
                                  "completeBodyCrossing": True, "gateId": GATE_ID, "crossingId": f"{GATE_ID}/crossing/2"})
    s["crossingReceipts"][f"{GATE_ID}/crossing/2"] = {
        "id": f"{GATE_ID}/crossing/2", "targetId": TARGET_ID, "gateId": GATE_ID,
        "encounterId": ENCOUNTER_ID, "creatorId": CREATOR_ID,
        "from": "fixture:origin", "to": "fixture:origin", "movementSource": "voluntary walking",
        "movementSpentFeet": 5, "walletBefore": 40, "walletAfter": 35,
        "bodyBoxBefore": before_box, "bodyBoxAfter": copy.deepcopy(after_box), "completeBodyCrossing": True,
        "admittedAt": None, "cellId": None, "outcome": "NO_ADMISSION_EXISTING_HARD_DENIAL_CLAIM",
        "existingClaimId": "claim-Guard-365", "claimSpent": False,
        "noSecondCell": True, "gateRemainsActive": True, "duplicateDeliveryCount": 0
    }


later_id = f"{GATE_ID}/crossing/2"
add_event("W04-365:LATER-PAID-CROSSING", 62.1, "LATER_PAID_CROSSING_NO_SECOND_ADMISSION",
          "On Guard's genuinely later regular turn, it pays five feet to cross back through the still-active portal. The original creator/target/encounter claim blocks a second admission; movement completes and no new cell or claim is created.",
          {"crossingId": later_id, "targetId": TARGET_ID, "creatorId": CREATOR_ID,
           "encounterId": ENCOUNTER_ID, "actualTurnStartedAt": 62.0, "movementSource": "voluntary walking",
           "movementSpentFeet": 5, "portalPlane": "x=0", "bodyFullyCrosses": True,
           "targetType": "Humanoid", "existingClaimId": "claim-Guard-365",
           "mobileAllowanceUsedFeet": 5, "movementRemainsPaid": True,
           "existingClaimSpentAt": 2.05, "newClaimSpent": False, "expectedCellCount": 0}, later_crossing)


later_receipt = copy.deepcopy(state["crossingReceipts"][later_id])
original_receipt = copy.deepcopy(state["crossingReceipts"][original_crossing_id])

def no_op(s):
    return


add_event("W04-365:DUPLICATE-LATER-CROSSING", 62.1, "DUPLICATE_CROSSING_DELIVERY_RETURNS_EXISTING_RECEIPT",
          "A duplicate callback with crossing/2 returns its existing no-admission receipt without moving the body again or retrying the Gate.",
          {"duplicateDelivery": True, "crossingId": later_id, "returnedReceipt": later_receipt,
           "returnedReceiptSha256": sha(later_receipt), "expectedNoStateChange": True}, no_op)
add_event("W04-365:DUPLICATE-ORIGINAL-ADMISSION", 62.1, "DUPLICATE_ORIGINAL_DELIVERY_RETURNS_EXISTING_RECEIPT",
          "A delayed duplicate delivery of the original successful crossing/1 returns its existing historical admission receipt. It does not recreate the already-closed cell or renew the claim.",
          {"duplicateDelivery": True, "crossingId": original_crossing_id, "returnedReceipt": original_receipt,
           "returnedReceiptSha256": sha(original_receipt), "expectedNoStateChange": True,
           "referencedCellCurrentStatus": "destroyed"}, no_op)

case = {
    "id": CASE_ID,
    "witnessId": "W04",
    "status": "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED",
    "scope": "Banishment Gate W04 returned-target and later-crossing witness only",
    "supersedesSubmissions": previous_supersession,
    "authorizedTestFixture": {"authorization": "User explicitly authorized this hypothetical TEST_ONLY fixture.",
                               "campaignEventsAsserted": False, "identityAcceptanceOrApplication": False},
    "fixturePremises": {"classification": "TEST_ONLY continuation fork of the Director-sealed W06 fixture; not campaign history",
                        "sourceWitness": "W06", "sourceArchive": W06_ZIP.name, "sourceArchiveSha256": w06_sha,
                        "forkEventId": "BG-W06-365:7", "forkKind": "VOLUNTARY_COMPLETE_CROSSING_AND_ADMISSION",
                        "actorIdentity": TARGET_ID, "creatorIdentity": CREATOR_ID, "encounterIdentity": ENCOUNTER_ID},
    "sourceBindings": {"Gate": {**source_record, "selectedType": "Humanoid",
                                   "procedurePointer": "/procedure", "cellExtensionPointer": "/sharedContract/cellExtension",
                                   "requiredClauses": ["PG9-Q14", "PG9-Q16", "PG9-Q29", "BAN-CLOSE-03"]}},
    "priorAdmission": {"event": prior_event, "eventId": prior_event["id"],
                       "eventAfterSha256": prior_event["afterSHA256"],
                       "crossingId": original_crossing_id,
                       "receipt": original_receipt,
                       "claim": claim},
    "initial": initial,
    "initialSHA256": sha(initial),
    "events": events,
    "final": state,
    "finalSHA256": sha(state),
    "inverseRestorationOrder": [e["id"] for e in reversed(events)],
    "assertions": {"startsFromDirectorSealedSuccessfulAdmission": True,
                   "existingCreatorTargetEncounterClaimPreserved": True,
                   "targetReturnedAliveAtIndependentCellDeadline": True,
                   "parentGateRemainsActiveAtReturnAndLaterCrossing": True,
                   "laterCrossingPaysFiveFeet": True,
                   "laterCrossingCreatesNoSecondCellOrClaim": True,
                   "duplicateLaterCrossingReturnsExistingReceipt": True,
                   "duplicateOriginalCrossingReturnsExistingReceipt": True,
                   "queueUnchanged": True, "identityAccepted": False, "identityApplied": False}
}
write_json(PACK / CASE_NAME, case)
write_json(PACK / "W04_SOURCE_BINDING_365_REPACK02.json", {
    "id": "PG327-W04-SOURCE-BINDING-365-REPACK02", "sourceCommit": source_commit,
    "gate": {**source_record, "sha256": file_sha(gate_bytes), "gitShowVerified": True,
              "procedurePointer": "/procedure", "cellExtensionPointer": "/sharedContract/cellExtension"},
    "sourceClauses": {"portalCrossing": "PG9-Q14", "hardDenial": "PG9-Q16",
                       "idempotentReceipt": "PG9-Q29", "cellDeadlineReturn": "sharedContract/cellExtension/closure"},
    "w06SealedArchiveSha256": w06_sha
})

readme = f"""# Banishment Gate W04 — returned target and later crossing (TEST_ONLY)

This witness forks the exact successful Guard admission at W06 event `BG-W06-365:7` from Director-sealed Repack06 ({w06_sha}). The same living Guard, original Gate creator W20, encounter ID, cell, admission receipt, and already-spent creator/target/encounter claim are carried forward.

At the target's independent 60-second cell deadline, the mandatory closure returns that same living identity to the fixed origin anchor. The parent Gate remains active until its separate 600-second deadline. On Guard's scheduled turn at 62.0, it then pays five feet to cross the portal in the opposite direction. The already-spent claim prevents a second cell; the movement completes, with no new claim. A duplicate delivery of the later crossing ID and a delayed duplicate of the original successful crossing both return their existing receipts without state mutation or renewed admission.

The case is a hypothetical continuation of the existing explicitly authorized TEST_ONLY W06 fixture. It asserts no campaign event, changes no canon, accepts/applies no spell identity, and leaves Queue361 unchanged. Director W04 review is required.
"""
(PACK / "README.md").write_text(readme, encoding=ENC)

queue = json.loads((PACK / "authority/CURRENT_SPELL_QUEUE_361.json").read_text(encoding=ENC))
plan = json.loads((PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json").read_text(encoding=ENC))
assert queue["currentAuthority"]["reviewedApplied"] == 828 and queue["currentAuthority"]["pending"] == 20
assert queue["currentAuthority"]["acceptedUnapplied"] == 0
assert next(w for w in plan["requirements"]["witnesses"] if w["id"] == "W04")["requiredEvidence"]

verifier_source = BASE / "verify_banishment_gate_w04_returned_target_365_repack02.py"
verifier_member = PACK / "verification/verify_banishment_gate_w04_returned_target_365_repack02.py"
verifier_member.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(verifier_source, verifier_member)

members = sorted(p for p in PACK.rglob("*") if p.is_file() and p.name not in {"MANIFEST.json", "DELIVERY.json"})
manifest = {"id": "PG327-W04-MANIFEST-365-REPACK02", "members": [
    {"path": p.relative_to(PACK).as_posix(), "bytes": p.stat().st_size,
     "sha256": file_sha(p.read_bytes()), "crc32": f"{zlib.crc32(p.read_bytes()) & 0xffffffff:08x}"} for p in members]}
write_json(PACK / "MANIFEST.json", manifest)
delivery = {"id": "PG327-W04-DELIVERY-365-REPACK02", "archive": ARCHIVE.name,
            "scope": ["banishment-gate/W04"],
            "requestedDirectorAction": "Audit W04 Repack02 only. Confirm R1 complete regular-turn resource, end-marker, nextEnd and magicThisTurn processing; R2 stance expiration, legal TEST_ONLY Mobile selections and paid allowance use; R3 once-only observation-marker no-op ordered after Guard start. Reconfirm same-identity return at the cell deadline, active parent Gate, paid later crossing, no second cell/claim, and idempotent duplicate receipts. Seal W04 only if every predicate and inverse check passes; otherwise return exact paths.",
            "supersedes": {"archive": W04_PREV_ZIP.name, "sha256": file_sha(W04_PREV_ZIP.read_bytes()),
                           "directorDisposition": "PG327-W04-365-REPACK01-DIRECTOR-HOLD"},
            "spellDispositionRequested": "NONE", "applicationRequested": False,
            "authority": {"queue": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0,
                          "heldIds": ["banishment-gate"], "blockers": ["PG200-B03", "PG200-B04"]},
            "priorSealedWitness": {"id": "W06", "archive": W06_ZIP.name, "archiveSha256": w06_sha},
            "members": manifest["members"]}
write_json(PACK / "DELIVERY.json", delivery)
with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(p for p in PACK.rglob("*") if p.is_file()):
        zf.write(path, path.relative_to(PACK).as_posix())
with zipfile.ZipFile(ARCHIVE) as zf:
    infos = zf.infolist()
    names = [x.filename for x in infos]
    assert len(names) == len(set(names)) and zf.testzip() is None
    assert sorted(names) == sorted(p.relative_to(PACK).as_posix() for p in PACK.rglob("*") if p.is_file())
archive_bytes = ARCHIVE.read_bytes()
write_json(OUT / "ARCHIVE_DELIVERY_365_W04_REPACK02.json", {
    "id": "PG327-W04-ARCHIVE-DELIVERY-365-REPACK02", "archive": ARCHIVE.name,
    "bytes": len(archive_bytes), "sha256": file_sha(archive_bytes), "memberCount": len(names), "zipTest": "PASS"})
print(json.dumps({"archive": str(ARCHIVE), "bytes": len(archive_bytes), "sha256": file_sha(archive_bytes),
                  "members": len(names), "events": len(events), "initialSHA256": sha(initial), "finalSHA256": sha(state)}, indent=2))
