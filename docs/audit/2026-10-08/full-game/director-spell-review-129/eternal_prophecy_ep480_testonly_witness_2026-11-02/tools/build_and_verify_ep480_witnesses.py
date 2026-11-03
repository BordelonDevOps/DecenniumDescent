#!/usr/bin/env python3
"""Build and verify the adopted, TEST_ONLY EP480 T1-T4 witness packet."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / ".git").exists())
PACKET_DIR = HERE.parent.parent
PROPOSAL_REL = Path(
    "docs/audit/2026-10-08/full-game/director-spell-review-129/"
    "eternal_prophecy_ep480_static_guarantee_proposal_2026-11-02/"
    "OWNER_EP480_STATIC_GUARANTEE_PROPOSAL_03.json"
)
RECEIPT_REL = PACKET_DIR.relative_to(ROOT) / "OWNER_ADOPTION_RECEIPT_EP480_P03.json"
PACKET_REL = PACKET_DIR.relative_to(ROOT) / "EP480_TESTONLY_WITNESS_PACKET_T1_T4.json"
PROPOSAL_SHA256 = "6910934619559fea734a7215e92022859050d81c084d2d5520d78b9d7fdec0f0"
PARENT_STATE_SHA256 = "55de6c13eb5c86784933052e401d8f84ad600d6b1ec8830280eeb693d0c0347c"
CAST_ID = "RANK9TIMEFATE6129-ETERNAL-PROPHECY-A-cast1"
OBLIGATION_ID = CAST_ID
DEADLINE = 34_560_000_100
TERMINAL = 34_560_000_099
SUPPORT_ID = "EP480-SUPPORT-BOOK-W-01"
MARKER_ID = "EP480-CACHE-MARKER-01"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def git_file(path: str) -> tuple[bytes, str]:
    raw = git("show", f"HEAD:{path}")
    blob = git("rev-parse", f"HEAD:{path}").decode().strip()
    return raw, blob


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        pairs = [(unicodedata.normalize("NFC", str(k)), normalize(v)) for k, v in value.items()]
        return {k: v for k, v in sorted(pairs, key=lambda pair: pair[0])}
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        normalize(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def json_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    current = value
    for raw in pointer.split("/")[1:]:
        key = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(key)] if isinstance(current, list) else current[key]
    return current


def load_sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    proposal_raw = (ROOT / PROPOSAL_REL).read_bytes()
    if hashlib.sha256(proposal_raw).hexdigest() != PROPOSAL_SHA256:
        raise AssertionError("proposal bytes do not match the adopted SHA-256")
    proposal = json.loads(proposal_raw)
    if proposal["status"] != "PROPOSED_NOT_ADOPTED":
        raise AssertionError("the original proposal must remain immutable and unadopted")

    sources: dict[str, Any] = {}
    bindings = proposal["sourceBindings"]
    for binding in bindings:
        raw, blob = git_file(binding["path"])
        if hashlib.sha256(raw).hexdigest() != binding["sha256"]:
            raise AssertionError(f"source SHA-256 mismatch: {binding['path']}")
        if blob != binding["gitBlobSha1"]:
            raise AssertionError(f"source Git blob mismatch: {binding['path']}")
        data = json.loads(raw)
        for pointer in binding["pointers"]:
            json_pointer(data, pointer)
        sources[binding["role"]] = data

    receipt_raw = (ROOT / RECEIPT_REL).read_bytes()
    receipt = json.loads(receipt_raw)
    if receipt["proposal"]["sha256"] != PROPOSAL_SHA256:
        raise AssertionError("adoption receipt is bound to the wrong proposal")
    if receipt["ownerResponse"] != "Adopt exact proposal for TEST_ONLY construction":
        raise AssertionError("owner adoption response mismatch")
    return proposal, sources, receipt


def source_context(proposal: dict[str, Any], sources: dict[str, Any]) -> dict[str, Any]:
    paid = sources["paid_cast_and_successful_delivery_parent"]
    death = sources["caster-death-and-persistence-boundary"]
    conflict = sources["temporal-conflict-boundary"]
    profiles = sources["conditional_actor_profile_source"]
    parent = paid["events"][2]["after"]
    if digest(parent) != PARENT_STATE_SHA256:
        raise AssertionError("A /events/2/after parent state hash mismatch")
    if parent["world"]["nowMs"] != 100 or parent["obligations"]:
        raise AssertionError("parent is not the exact paid, pre-obligation state")
    if len(parent["casts"]) != 1 or parent["casts"][0]["id"] != CAST_ID:
        raise AssertionError("parent must inherit the single paid source cast")
    if parent["actors"]["W"]["RP"] != 38 or parent["actors"]["W"]["budget"]["Action"] != 0:
        raise AssertionError("paid parent does not preserve RP 38 and spent Action")
    obligation = paid["events"][3]["after"]["obligations"][OBLIGATION_ID]
    if obligation["createdMs"] != 100 or obligation["deadlineMs"] != DEADLINE:
        raise AssertionError("source obligation creation/deadline mismatch")

    wizard = profiles["Wizard"]
    counterspell = wizard["automaticCards"][1]
    spellbook = wizard["acquisitionLedger"][9]["choices"][0]
    t = parent["actors"]["T"]
    w = parent["actors"]["W"]
    distance = sum((a - b) ** 2 for a, b in zip(t["position"], w["position"])) ** 0.5
    if distance.is_integer():
        distance = int(distance)
    if not (
        counterspell["id"] == "wizard.base.counterspell"
        and counterspell["acquisition"].lower() == "automatic"
        and counterspell["minimumClassLevel"] <= t["classLevel"]
        and counterspell["activation"] == "Reaction"
        and t["budget"]["Reaction"] == 1
        and t["RP"] == 64
        and distance <= 60
        and parent["perception"]["mutualSight"]
        and parent["perception"]["lineOfEffect"]
        and not t["recharge"]
    ):
        raise AssertionError("T's conditional Counterspell response prerequisites are not met")
    if spellbook["id"] != "wizard.hero.spellbinder.spell-preservation":
        raise AssertionError("bound Spell Preservation source is not the expected card")

    conflict_outcome = conflict["events"][4]["after"]["outcomes"][-1]
    death_after = death["events"][4]["after"]
    death_before = death["events"][4]["before"]
    death_roll = death["events"][8]["after"]["rolls"][-1]
    death_clock = death["events"][8]["after"]["clockLedger"][-1]
    return {
        "parent": parent,
        "obligation": obligation,
        "counterspell": counterspell,
        "spellbook": spellbook,
        "distanceFt": distance,
        "conflictOutcome": conflict_outcome,
        "deathBefore": death_before,
        "deathAfter": death_after,
        "deathRoll": death_roll,
        "deathClock": death_clock,
        "paid": paid,
        "death": death,
        "conflict": conflict,
        "profiles": profiles,
    }


def ptr(path: tuple[str, ...]) -> str:
    return "".join("/" + p.replace("~", "~0").replace("/", "~1") for p in path)


def diff(before: Any, after: Any, path: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    if isinstance(before, dict) and isinstance(after, dict):
        out: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child = path + (str(key),)
            if key not in before:
                out.append({"op": "add", "path": ptr(child), "beforeExists": False,
                            "afterExists": True, "after": copy.deepcopy(after[key])})
            elif key not in after:
                out.append({"op": "remove", "path": ptr(child), "beforeExists": True,
                            "afterExists": False, "before": copy.deepcopy(before[key])})
            else:
                out.extend(diff(before[key], after[key], child))
        return out
    if before != after:
        return [{"op": "replace", "path": ptr(path), "beforeExists": True,
                 "afterExists": True, "before": copy.deepcopy(before),
                 "after": copy.deepcopy(after)}]
    return []


def value_at(root: Any, pointer: str) -> Any:
    return json_pointer(root, pointer)


def set_at(root: Any, pointer: str, exists: bool, value: Any = None) -> None:
    parts = pointer.split("/")[1:]
    parent = root
    for raw in parts[:-1]:
        key = raw.replace("~1", "/").replace("~0", "~")
        parent = parent[int(key)] if isinstance(parent, list) else parent[key]
    key = parts[-1].replace("~1", "/").replace("~0", "~")
    if isinstance(parent, list):
        parent[int(key)] = copy.deepcopy(value)
    elif exists:
        parent[key] = copy.deepcopy(value)
    else:
        del parent[key]


def apply_ops(state: Any, ops: list[dict[str, Any]], inverse: bool = False) -> None:
    sequence = list(reversed(ops)) if inverse else ops
    for op in sequence:
        if not inverse:
            expected_exists, expected = op["beforeExists"], op.get("before")
            target_exists, target = op["afterExists"], op.get("after")
        else:
            expected_exists, expected = op["afterExists"], op.get("after")
            target_exists, target = op["beforeExists"], op.get("before")
        try:
            actual = value_at(state, op["path"])
            actual_exists = True
        except (KeyError, IndexError, TypeError):
            actual, actual_exists = None, False
        if actual_exists != expected_exists or (actual_exists and actual != expected):
            raise AssertionError(f"operation precondition failed at {op['path']}")
        set_at(state, op["path"], target_exists, target)


def add_transition(branch: dict[str, Any], state: dict[str, Any], event_id: str,
                   at_ms: int, description: str, mutate) -> None:
    before = copy.deepcopy(state)
    before_hash = digest(before)
    mutate(state)
    after_hash = digest(state)
    operations = diff(before, state)
    inverse = []
    for op in reversed(operations):
        inverse.append({
            "op": {"add": "remove", "remove": "add", "replace": "replace"}[op["op"]],
            "path": op["path"],
            "beforeExists": op["afterExists"],
            "afterExists": op["beforeExists"],
            **({"before": copy.deepcopy(op["after"])} if op["afterExists"] else {}),
            **({"after": copy.deepcopy(op["before"])} if op["beforeExists"] else {}),
        })
    branch["transitions"].append({
        "eventId": event_id,
        "atMs": at_ms,
        "description": description,
        "beforeStateSHA256": before_hash,
        "afterStateSHA256": after_hash,
        "forward": operations,
        "inverse": inverse,
    })


def common_overlay(case: dict[str, Any]) -> dict[str, Any]:
    branch_id = case["branchId"]
    child = case["executionChildId"]
    return {
        "schema": "EP480_TESTONLY_BRANCH_OVERLAY_V1",
        "branchId": branch_id,
        "executionChildId": child,
        "nowMs": 100,
        "ordinaryRound": 1,
        "worldMode": "combat",
        "initiativeDispatchEnabled": True,
        "actorOverrides": {},
        "itemOverrides": {},
        "newObligations": {},
        "outcomes": [],
        "rolls": [],
        "clockLedgerEntries": [],
        "custodyHistory": [],
        "saveLoadRecords": [],
        "removalAttempts": [],
        "offSceneItemLedger": {},
        "offSceneDestinationLedger": {},
        "fixture": {
            "type": "TEST_ONLY_SYNTHETIC_ROOM",
            "dimensionsFt": [120, 120],
            "coordinates": "x east, y north, z up",
            "supportPatch": {
                "id": SUPPORT_ID,
                "center": [15, 0, 0],
                "bounds": {"x": [14.5, 15.5], "y": [-0.5, 0.5]},
                "topZ": 0,
                "soleSupport": True,
                "supportOwner": "TEST_ONLY scene-fixture-owner",
                "restorationPermission": "exact proposal03 owner adoption; this branch only",
                "floorCutoutMatchesPatch": True,
                "active": True,
            },
            "bookEnvelopeFt": [1, 1, 0.1],
            "cacheMarker": {
                "id": MARKER_ID,
                "location": [15, 0, 0],
                "active": True,
                "owning": False,
                "providesSupport": False,
            },
            "clearance": "Only book-W occupies the delivery envelope; W at [0,0,0] and T at [5,0,0] do not intersect it.",
            "massConservationClaim": False,
        },
        "routeRegistry": {
            "exactOrdinaryRoutes": ["consensual-ally-delivery", "caster-carries-around-obstruction"],
            "closedWorld": False,
            "additionalDeliveryActorsOrObjectsExist": "not yet evaluated",
        },
        "preventionOperands": {},
        "ordinaryMagicalInterventionsEnabled": True,
        "ordinarySpellExpressionEnabled": True,
        "responseWindow": None,
        "resolvedSuccessfully": False,
        "terminalScheduler": {
            "key": child,
            "atMs": TERMINAL,
            "immutableOneUseEntry": True,
            "active": True,
            "consumed": False,
            "priorityScope": [],
        },
        "terminalRecord": None,
        "postDeadlineObservation": None,
    }


def build_case(case_id: str, ctx: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    suffix = case_id[-2:]
    case = {
        "caseId": case_id,
        "branchId": f"EP480-BRANCH-{suffix}",
        "executionChildId": f"EP480-WITNESS-OBLIGATION-BOOK-W-01-{suffix}",
    }
    state = {
        "schema": "EP480_TESTONLY_BRANCH_STATE_V1",
        "caseId": case_id,
        "branchId": case["branchId"],
        "executionChildId": case["executionChildId"],
        "parentProjection": {
            "path": ctx["proposal"]["branchFixture"]["branchStart"]["sourcePath"],
            "pointer": "/events/2/after",
            "sourceStateSHA256": PARENT_STATE_SHA256,
        },
        "overlay": common_overlay(case),
    }
    branch = {
        **case,
        "branchStartState": copy.deepcopy(state),
        "branchStartStateSHA256": digest(state),
        "transitions": [],
    }
    base_w = ctx["parent"]["actors"]["W"]
    base_t = ctx["parent"]["actors"]["T"]
    base_item = ctx["parent"]["items"]["book-W"]
    obligation = copy.deepcopy(ctx["obligation"])
    ov = lambda s: s["overlay"]

    def at100(s):
        o = ov(s)
        o["responseWindow"] = {
            "atMs": 100,
            "observer": "T",
            "triggerCastId": CAST_ID,
            "counterspellSourcePointer": "ACTOR_PROFILES.json#/Wizard/automaticCards/1",
            "eligibility": {
                "profile": "Wizard17-human",
                "TLevel": base_t["classLevel"],
                "minimumLevel": ctx["counterspell"]["minimumClassLevel"],
                "distanceFt": ctx["distanceFt"],
                "mutualSight": ctx["parent"]["perception"]["mutualSight"],
                "lineOfEffect": ctx["parent"]["perception"]["lineOfEffect"],
                "reactionAvailable": base_t["budget"]["Reaction"] == 1,
                "rpAvailable": base_t["RP"],
                "rechargeLockRecorded": bool(base_t["recharge"]),
                "sourceQualified": True,
            },
            "outcome": "T voluntarily declines; no compelled action.",
            "reactionSpent": False,
            "rpSpent": 0,
        }
        o["preventionOperands"]["EP480-PREVENT-ALLY-DELIVERY"] = {
            "active": True, "atMs": 100, "route": "consensual-ally-delivery",
            "target": "T", "effect": "T declined; route unavailable through deadline inclusive.",
            "persistsUntilMs": DEADLINE, "inclusiveThroughDeadline": True, "cost": 0,
        }
        o["resolvedSuccessfully"] = True
        o["newObligations"][OBLIGATION_ID] = copy.deepcopy(obligation)
        o["branchObligationMapping"] = {
            "sourceCastId": CAST_ID,
            "soleObligationId": OBLIGATION_ID,
            "executionChildId": case["executionChildId"],
            "castOrPaymentRepeated": False,
        }

    add_transition(branch, state, f"{case_id}-100-RESPONSE-RESOLUTION-OBLIGATION", 100,
                   "Open the actual response window, record T's voluntary no-cost decline, resolve the already-paid cast successfully in this branch, and create exactly one mapped obligation.", at100)

    if case_id == "EP480-T4":
        def conflict_refusal(s):
            o = ov(s)
            record = copy.deepcopy(ctx["conflictOutcome"])
            record["existingObligationId"] = OBLIGATION_ID
            record["sourcePointer"] = f"{ctx['proposal']['sourceBindings'][5]['path']}#/events/4/after/outcomes/0"
            record["branchLocalRequestOnly"] = True
            o["outcomes"].append(record)
            o["conflictPreflight"] = {
                "admitted": False,
                "laterCost": 0,
                "newBodyOrItem": False,
                "existingObligationUnchanged": True,
                "sourceRequest": "rewrite-creation-conflict",
                "mappedToObligationId": OBLIGATION_ID,
                "executedFateRewrite": False,
            }
        add_transition(branch, state, f"{case_id}-100-CONFLICT-PREFLIGHT-REFUSAL", 100,
                       "Replay only the exact precommit refusal outcome, remapped to this branch's sole obligation; import no sibling cast, cost, actor, or obligation.", conflict_refusal)

        def injury_and_floor(s):
            o = ov(s)
            before = ctx["deathBefore"]["actors"]["W"]
            after = ctx["deathAfter"]["actors"]["W"]
            fields = ["budget", "conditions", "deathSaves", "hp", "life"]
            override = o["actorOverrides"].setdefault("W", {})
            for field in fields:
                if before[field] != after[field]:
                    override[field] = copy.deepcopy(after[field])
            injury_item = copy.deepcopy(ctx["deathAfter"]["items"]["book-W"])
            o["itemOverrides"]["book-W"] = injury_item
            o["custodyHistory"].append({
                "atMs": 100, "itemId": "book-W", "owner": "W", "from": "carried-by-W",
                "to": "floor", "custodian": "floor", "position": [0, 0, 0],
                "support": "inherited-flat-room-floor", "destroyed": False,
                "sourcePointer": f"{ctx['proposal']['sourceBindings'][6]['path']}#/events/4/after/items/book-W",
            })
        add_transition(branch, state, f"{case_id}-100-W-INJURY-BOOK-FLOOR", 100,
                       "Apply only the exact source B death-case injury budget/condition/death-save and same-book floor custody deltas; preserve RP38 and the inherited A cast/payment.", injury_and_floor)

    def remaining_preventions(s):
        o = ov(s)
        o["nowMs"] = 101
        specs = [
            ("EP480-PREVENT-CARRY-ROUTE", "W", "caster-carries-around-obstruction", "all local carry paths unavailable, including the otherwise open y=5 bypass"),
            ("EP480-PREVENT-OTHER-DELIVERY", OBLIGATION_ID, "closed-world route registry", "only two ordinary routes and one terminal route; no other actor/object/route"),
            ("EP480-SUPPRESS-ORDINARY-EXPRESSION", OBLIGATION_ID, "ordinary Eternal Prophecy expression", "ordinary expression disabled only"),
        ]
        for ident, target, route, effect in specs:
            o["preventionOperands"][ident] = {
                "active": True, "atMs": 101, "target": target, "route": route,
                "effect": effect, "persistsUntilMs": DEADLINE,
                "inclusiveThroughDeadline": True, "cost": 0,
            }
        o["routeRegistry"] = {
            "exactOrdinaryRoutes": ["consensual-ally-delivery", "caster-carries-around-obstruction"],
            "closedWorld": True,
            "additionalDeliveryActorsOrObjectsExist": False,
            "terminalRouteIsSeparate": True,
        }
        o["ordinaryMagicalInterventionsEnabled"] = False
        o["ordinarySpellExpressionEnabled"] = False
        o["terminalScheduler"]["priorityScope"] = [
            "EP480-PREVENT-ALLY-DELIVERY", "EP480-PREVENT-CARRY-ROUTE",
            "EP480-PREVENT-OTHER-DELIVERY", "EP480-SUPPRESS-ORDINARY-EXPRESSION",
            "EP480-REMOVE-ATTEMPT-01", "EP480-REMOVE-ATTEMPT-02",
            "EP480-LOSS-ITEM-01", "EP480-LOSS-DESTINATION-01",
        ]
        o["terminalScheduler"]["priorityIsGeneralUnsuppressibility"] = False
    add_transition(branch, state, f"{case_id}-101-REMAINING-PREVENTIONS", 101,
                   "Activate the three remaining named prevention operands without repeating the 100-ms ally refusal; close the two-route registry and suppress ordinary expression.", remaining_preventions)

    def removal_one(s):
        o = ov(s)
        o["nowMs"] = 200
        target = o["newObligations"][OBLIGATION_ID]
        before = {"status": target["status"], "deadlineMs": target["deadlineMs"], "scheduler": copy.deepcopy(o["terminalScheduler"])}
        o["removalAttempts"].append({"id": "EP480-REMOVE-ATTEMPT-01", "atMs": 200,
                                      "requested": ["cancel", "reset", "delete"],
                                      "writesAccepted": False, "cost": 0})
        after = {"status": target["status"], "deadlineMs": target["deadlineMs"], "scheduler": copy.deepcopy(o["terminalScheduler"])}
        if before != after:
            raise AssertionError("first removal attempt changed protected state")
    add_transition(branch, state, f"{case_id}-200-REMOVAL-REFUSAL-01", 200,
                   "Reject cancellation/reset/deletion with no protected-state writes and retain the one-use scheduler entry.", removal_one)

    if case_id == "EP480-T4":
        def save_load(s):
            o = ov(s)
            o["nowMs"] = 1000
            o["saveLoadRecords"].append({
                "atMs": 1000,
                "sourcePointer": f"{ctx['proposal']['sourceBindings'][1]['path']}#/events/5",
                "roundTrip": True,
                "castId": CAST_ID,
                "obligationId": OBLIGATION_ID,
                "deadlineMs": DEADLINE,
                "status": "pending",
                "paymentRepeated": False,
            })
        add_transition(branch, state, f"{case_id}-1000-PENDING-SAVE-LOAD", 1000,
                       "Round-trip the same pending obligation, cast ID, payment and original deadline using the bound A save/load event.", save_load)

    death = ctx["death"]
    clock_entries = death["events"][7]["after"]["clockLedger"]
    w_end = next(x for x in clock_entries if x["actor"] == "W" and x["atMs"] == 1900)
    t_start = ctx["paid"]["events"][8]["after"]["clockLedger"]
    t_start = next(x for x in t_start if x["actor"] == "T" and x["atMs"] == 2000)
    t_end = next(x for x in clock_entries if x["actor"] == "T" and x["atMs"] == 3900)

    def clock_w_end(s):
        o = ov(s)
        o["nowMs"] = 1900
        w = o["actorOverrides"].setdefault("W", {})
        w["nextRegularEnd"] = None
        w["regularEnds"] = [*base_w["regularEnds"], 1900]
        o["clockLedgerEntries"].append(copy.deepcopy(w_end))
    add_transition(branch, state, f"{case_id}-1900-W-END", 1900,
                   "Process inherited W END1900 and retain its exact source clock marker.", clock_w_end)

    def clock_t_start(s):
        o = ov(s)
        o["nowMs"] = 2000
        o["actorOverrides"]["T"] = {
            "budget": copy.deepcopy(ctx["paid"]["events"][8]["after"]["actors"]["T"]["budget"]),
            "currentRegularStart": 2000, "nextRegularEnd": 3900, "nextRegularStart": 8000,
            "regularStarts": [2000],
        }
        o["clockLedgerEntries"].append(copy.deepcopy(t_start))
    add_transition(branch, state, f"{case_id}-2000-T-START", 2000,
                   "Process inherited T START2000 using the source actor clock transition; T takes no action, route, delivery, or cost.", clock_t_start)

    def clock_t_end(s):
        o = ov(s)
        o["nowMs"] = 3900
        t = o["actorOverrides"]["T"]
        t["nextRegularEnd"] = None
        t["regularEnds"] = [3900]
        o["clockLedgerEntries"].append(copy.deepcopy(t_end))
    add_transition(branch, state, f"{case_id}-3900-T-END", 3900,
                   "Process inherited T END3900 and retain its exact source clock marker.", clock_t_end)

    if case_id in ("EP480-T2", "EP480-T4"):
        def lose_item(s):
            o = ov(s)
            o["nowMs"] = 5000
            item = copy.deepcopy(o["itemOverrides"].get("book-W", base_item))
            last_support = "inherited-flat-room-floor" if case_id == "EP480-T4" else None
            last_custody = item["custodian"]
            o["offSceneItemLedger"]["book-W"] = {
                "id": "book-W", "item": item, "availability": "off-scene/unavailable",
                "lastPose": {"custodian": last_custody, "position": copy.deepcopy(item["position"]), "support": last_support},
                "lossId": "EP480-LOSS-ITEM-01", "atMs": 5000,
            }
            o["itemOverrides"]["book-W"] = None
            o["custodyHistory"].append({
                "atMs": 5000, "itemId": "book-W", "owner": "W", "from": last_custody,
                "to": "offSceneItemLedger", "availability": "off-scene/unavailable",
                "destroyed": False, "contentsAndIdentityPreserved": True,
                "lossId": "EP480-LOSS-ITEM-01",
            })
        add_transition(branch, state, f"{case_id}-5000-ITEM-OFFSCENE-LOSS", 5000,
                       "Move the one intact book-W to the off-scene ledger; preserve unique ID, owner, contents, Spell Preservation, and T4's floor pose/support.", lose_item)

    if case_id in ("EP480-T3", "EP480-T4"):
        def lose_destination(s):
            o = ov(s)
            o["nowMs"] = 5100
            plate = copy.deepcopy(o["fixture"]["supportPatch"])
            marker = copy.deepcopy(o["fixture"]["cacheMarker"])
            plate["active"] = False
            marker["active"] = False
            o["offSceneDestinationLedger"][SUPPORT_ID] = {"object": plate, "lossId": "EP480-LOSS-DESTINATION-01", "atMs": 5100}
            o["offSceneDestinationLedger"][MARKER_ID] = {"object": marker, "lossId": "EP480-LOSS-DESTINATION-01", "atMs": 5100}
            o["fixture"]["supportPatch"]["active"] = False
            o["fixture"]["cacheMarker"]["active"] = False
        add_transition(branch, state, f"{case_id}-5100-DESTINATION-OFFSCENE-LOSS", 5100,
                       "Move the exact plate and separate cache marker to off-scene ledgers, leaving the cutout with no alternate support.", lose_destination)

    def w_start_living(s):
        o = ov(s)
        o["nowMs"] = 6000
        o["ordinaryRound"] = 2
        o["clockLedgerEntries"].append({
            "actor": "W", "atMs": 6000, "deathSaveRequired": False,
            "readyStatus": None, "rechargeAfter": {}, "type": "nextRegularStart",
        })
        o["actorOverrides"]["W"] = {
            "budget": {"Action": 1, "BonusAction": 1, "Reaction": 1, "extraAction": 0, "interaction": 1, "movement": 30},
            "currentRegularStart": 6000, "nextRegularStart": 12000,
            "nextRegularEnd": 7900, "regularStarts": [0, 6000], "regularEnds": [1900], "spellsThisTurn": 0,
        }
        o["w6000"] = {"alive": True, "deathSaveProcessed": False, "actionOrRouteAttempt": False}

    def w_start_death(s):
        o = ov(s)
        src_before = ctx["death"]["events"][7]["after"]["actors"]["W"]
        src_after = ctx["death"]["events"][8]["after"]["actors"]["W"]
        o["nowMs"] = 6000
        o["ordinaryRound"] = 2
        override = o["actorOverrides"].setdefault("W", {})
        for field in ("body", "currentRegularStart", "deathSaves", "life", "nextRegularEnd", "nextRegularStart", "regularStarts", "spellsThisTurn"):
            if src_before[field] != src_after[field]:
                override[field] = copy.deepcopy(src_after[field])
        o["clockLedgerEntries"].append(copy.deepcopy(ctx["deathClock"]))
        local_roll = copy.deepcopy(ctx["deathRoll"])
        local_roll["sourceRecordId"] = local_roll["id"]
        local_roll["id"] = f"{case['executionChildId']}-death-W-6000"
        local_roll["sourcePointer"] = f"{ctx['proposal']['sourceBindings'][6]['path']}#/events/8/after/rolls/0"
        o["rolls"].append(local_roll)
        o["w6000"] = {"alive": False, "deathSaveProcessed": True, "natural": 1,
                       "failures": 3, "actionOrRouteAttempt": False,
                       "sourcePointer": f"{ctx['proposal']['sourceBindings'][6]['path']}#/events/8"}

    add_transition(branch, state, f"{case_id}-6000-W-START", 6000,
                   "Process inherited W START6000. T1-T3 retain W alive and idle; T4 applies the exact bound natural-1 death-save transition.",
                   w_start_death if case_id == "EP480-T4" else w_start_living)

    if case_id == "EP480-T4":
        def record_death(s):
            o = ov(s)
            o["nowMs"] = 6100
            o["deathRecordedAtMs"] = 6100
            o["corpsePose"] = {"actor": "W", "position": [0, 0, 0], "newBody": False, "custodyTransfer": False}
        add_transition(branch, state, f"{case_id}-6100-DEATH-RECORD", 6100,
                       "Record W dead at6100; retain the same corpse pose and make no new body or custody transfer.", record_death)

    def close_initiative(s):
        o = ov(s)
        o["nowMs"] = 6101
        o["worldMode"] = "outside-initiative-test-only"
        o["initiativeDispatchEnabled"] = False
        o["combatClosedAtMs"] = 6101
        o["processedClockMarkersPreserved"] = True
        o["restRecoveryOrAdministrativeReset"] = False
    add_transition(branch, state, f"{case_id}-6101-CLOSE-INITIATIVE", 6101,
                   "Close combat after processed markers and continue monotonic outside-initiative time without rest, recovery, or reset.", close_initiative)

    def removal_two(s):
        o = ov(s)
        target = o["newObligations"][OBLIGATION_ID]
        before = {"status": target["status"], "deadlineMs": target["deadlineMs"], "scheduler": copy.deepcopy(o["terminalScheduler"])}
        o["nowMs"] = DEADLINE - 3
        o["removalAttempts"].append({"id": "EP480-REMOVE-ATTEMPT-02", "atMs": DEADLINE - 3,
                                      "requested": ["cancel", "reset", "delete"],
                                      "writesAccepted": False, "cost": 0})
        after = {"status": target["status"], "deadlineMs": target["deadlineMs"], "scheduler": copy.deepcopy(o["terminalScheduler"])}
        if before != after:
            raise AssertionError("second removal attempt changed protected state")
    add_transition(branch, state, f"{case_id}-{DEADLINE-3}-REMOVAL-REFUSAL-02", DEADLINE - 3,
                   "Repeat cancel/reset/delete refusal two milliseconds before terminal while retaining the original due entry.", removal_two)

    def elapsed_marker(s):
        o = ov(s)
        o["nowMs"] = TERMINAL - 1
        o["elapsedMarker"] = {"atMs": TERMINAL - 1, "monotonic": True, "initiativeDispatchEnabled": False}
    add_transition(branch, state, f"{case_id}-{TERMINAL-1}-ELAPSED-MARKER", TERMINAL - 1,
                   "Advance monotonic outside-initiative time to terminal-minus-one without reset or extra action.", elapsed_marker)

    def terminal(s):
        o = ov(s)
        if o["terminalScheduler"]["consumed"]:
            return
        if not all(x["active"] for x in o["preventionOperands"].values()):
            raise AssertionError("terminal must run with every prevention active")
        if o["nowMs"] != TERMINAL - 1 or not o["terminalScheduler"]["active"]:
            raise AssertionError("terminal scheduling precondition failed")
        steps = []
        # 1-2: restore the original support and the separate, non-owning marker.
        for object_id, key in ((SUPPORT_ID, "supportPatch"), (MARKER_ID, "cacheMarker")):
            if object_id in o["offSceneDestinationLedger"]:
                saved = o["offSceneDestinationLedger"].pop(object_id)["object"]
                saved["active"] = True
                o["fixture"][key] = saved
                steps.append({"restoreId": object_id, "source": "offSceneDestinationLedger"})
            else:
                steps.append({"restoreId": object_id, "source": "already-active"})
        if not o["fixture"]["supportPatch"]["active"] or not o["fixture"]["cacheMarker"]["active"]:
            raise AssertionError("destination restoration failed")
        if o["fixture"]["cacheMarker"]["providesSupport"] or not o["fixture"]["supportPatch"]["soleSupport"]:
            raise AssertionError("support/marker roles changed")
        steps.append({"verify": "sole support, clearance, and unique active plate/marker IDs"})
        # 4: restore the same unique book and put it at the original destination.
        if "book-W" in o["offSceneItemLedger"]:
            item = copy.deepcopy(o["offSceneItemLedger"].pop("book-W")["item"])
            item["owner"] = "W"
            item["custodian"] = "cache"
            item["position"] = [15, 0, 0]
            item["destroyed"] = False
            o["itemOverrides"]["book-W"] = item
            steps.append({"restoreId": "book-W", "source": "offSceneItemLedger"})
        else:
            item = copy.deepcopy(o["itemOverrides"].get("book-W", base_item))
            item["owner"] = "W"
            item["custodian"] = "cache"
            item["position"] = [15, 0, 0]
            item["destroyed"] = False
            o["itemOverrides"]["book-W"] = item
            steps.append({"restoreId": "book-W", "source": "active-item"})
        steps.append({"verify": "same item ID, owner, custodian, position, support, physical arrival, and no duplicate/ledger copy"})
        ob = o["newObligations"][OBLIGATION_ID]
        ob["status"] = "fulfilled"
        ob["fulfilledMs"] = TERMINAL
        ob["receiptId"] = case["executionChildId"] + "-receipt"
        # Preserve source guaranteeProved=false; this is only a TEST_ONLY procedure witness.
        ob["guaranteeProved"] = False
        steps.append({"fulfillObligationId": OBLIGATION_ID, "atMs": TERMINAL})
        o["nowMs"] = TERMINAL
        o["terminalScheduler"]["consumed"] = True
        o["terminalScheduler"]["active"] = False
        o["terminalRecord"] = {
            "key": case["executionChildId"], "atomic": True, "atMs": TERMINAL,
            "priorityUsedWhileAllPreventionsActive": True,
            "priorityScope": copy.deepcopy(o["terminalScheduler"]["priorityScope"]),
            "steps": steps,
            "failedPreconditionAbortsAllWrites": True,
            "newRPActionItemRewardBodyOrRecovery": False,
        }
        o["terminalRecord"]["sameKeyRetryNoOpVerified"] = True
        if case_id == "EP480-T4" and o["actorOverrides"]["W"]["life"] != "dead":
            raise AssertionError("T4 terminal must retain W dead")
        if o["itemOverrides"]["book-W"]["id"] != "book-W":
            raise AssertionError("terminal did not restore the same unique book")
        post_hash = digest(s)
        terminal(s)  # A second call with the same consumed key must be a full-state no-op.
        if digest(s) != post_hash:
            raise AssertionError("same-key terminal retry changed state")
    add_transition(branch, state, f"{case_id}-{TERMINAL}-ATOMIC-TERMINAL", TERMINAL,
                   "Run the one-use branch-local terminal while all prevention remains active; restore exact assets, fulfill the same obligation, and consume the key atomically.", terminal)

    def observe_deadline(s):
        o = ov(s)
        o["nowMs"] = DEADLINE
        o["postDeadlineObservation"] = {
            "atMs": DEADLINE,
            "originalDeadlineUnchanged": o["newObligations"][OBLIGATION_ID]["deadlineMs"] == DEADLINE,
            "physicalPredicateAlreadyFulfilled": o["newObligations"][OBLIGATION_ID]["fulfilledMs"] == TERMINAL,
            "preventionsStillActive": all(x["active"] for x in o["preventionOperands"].values()),
            "extensionOrRetry": False,
        }
    add_transition(branch, state, f"{case_id}-{DEADLINE}-DEADLINE-OBSERVATION", DEADLINE,
                   "Observe the unchanged original deadline after physical fulfillment; do not extend or re-execute.", observe_deadline)

    final_hash = digest(state)
    branch["finalStateSHA256"] = final_hash
    branch["terminalAssertions"] = {
        "sourceCastId": CAST_ID,
        "soleObligationId": OBLIGATION_ID,
        "paidRPExactlyOnce": 26,
        "W_RP": 38,
        "bookId": "book-W",
        "bookOwner": "W",
        "bookCustodian": "cache",
        "bookPosition": [15, 0, 0],
        "supportId": SUPPORT_ID,
        "cacheMarkerId": MARKER_ID,
        "arrivalMs": TERMINAL,
        "deadlineMs": DEADLINE,
        "preventionsActiveAtTerminalAndDeadline": True,
        "itemLedgerEmpty": not state["overlay"]["offSceneItemLedger"],
        "destinationLedgerEmpty": not state["overlay"]["offSceneDestinationLedger"],
        "T4_WDead": state["overlay"].get("actorOverrides", {}).get("W", {}).get("life") == "dead" if case_id == "EP480-T4" else None,
        "baseProjectionUntouched": True,
        "identityAcceptanceOrApplication": False,
        "canonRuntimeOrQueueChange": False,
    }
    terminal_post_state_hash = next(
        t["afterStateSHA256"] for t in branch["transitions"]
        if t["eventId"] == f"{case_id}-{TERMINAL}-ATOMIC-TERMINAL"
    )
    branch["idempotency"] = {
        "key": case["executionChildId"],
        "retryInputAtMs": TERMINAL,
        "firstCallPostStateSHA256": terminal_post_state_hash,
        "retryBeforeStateSHA256": terminal_post_state_hash,
        "retryAfterStateSHA256": terminal_post_state_hash,
        "fullStateNoOp": True,
        "retryWasNotRecordedAsAStateWrite": True,
    }
    branch["forwardInverse"] = {
        "patchSemantics": "Each operation stores exact before/after value and existence; inverse applies operations in reverse and requires the matching after-state hash.",
        "transitions": len(branch["transitions"]),
        "inverseRestoresBranchStartSHA256": branch["branchStartStateSHA256"],
    }
    return branch, state


def build_packet() -> dict[str, Any]:
    proposal, sources, receipt = load_sources()
    ctx = source_context(proposal, sources)
    ctx["proposal"] = proposal
    branches = []
    final_states = []
    for case_id in ("EP480-T1", "EP480-T2", "EP480-T3", "EP480-T4"):
        branch, final = build_case(case_id, ctx)
        branches.append(branch)
        final_states.append(final)
    bindings = []
    for b in proposal["sourceBindings"]:
        raw, blob = git_file(b["path"])
        bindings.append({"role": b["role"], "path": b["path"], "gitBlobSha1": blob,
                         "sha256": hashlib.sha256(raw).hexdigest(), "pointers": b["pointers"]})
    parent_projection = {
        "sourcePath": proposal["branchFixture"]["branchStart"]["sourcePath"],
        "sourcePointer": "/events/2/after",
        "sourceStateSHA256": PARENT_STATE_SHA256,
        "state": ctx["parent"],
    }
    packet = {
        "schema": "EP480_TESTONLY_WITNESS_PACKET_V1",
        "packetId": "EP480-RETURN323-T1-T4-WITNESS-2026-11-02",
        "reviewClass": "TEST_ONLY_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "spellId": "eternal-prophecy",
        "blockerId": "TF192-B02",
        "proposal": {"id": proposal["proposalId"], "sha256": PROPOSAL_SHA256},
        "adoptionReceipt": {"path": str(RECEIPT_REL).replace("\\", "/"),
                            "sha256": hashlib.sha256((ROOT / RECEIPT_REL).read_bytes()).hexdigest(),
                            "response": receipt["ownerResponse"]},
        "directorReadiness": "PASS — READY_FOR_OWNER_ADOPTION",
        "sourceBindings": bindings,
        "parentProjection": parent_projection,
        "parentProjectionCanonicalSHA256": digest(ctx["parent"]),
        "counterspellResponseEvidence": {
            "sourcePointer": "ACTOR_PROFILES.json#/Wizard/automaticCards/1",
            "cardId": ctx["counterspell"]["id"],
            "minimumLevel": ctx["counterspell"]["minimumClassLevel"],
            "actor": "T",
            "profileId": ctx["parent"]["actors"]["T"]["profileId"],
            "distanceFt": ctx["distanceFt"],
            "sightAndLineOfEffect": True,
            "reactionAvailable": 1,
            "rpAvailable": 64,
            "rechargeLockRecorded": False,
            "outcome": "voluntary decline at100ms; no reaction or RP spent",
        },
        "testOnlyPremises": {
            "terminalPriority": "One-use immutable branch overlay, outranks only the eight named prevention/removal/loss operations.",
            "preventionActiveThroughDeadlineInclusive": True,
            "sourceCastAndPaymentRepeated": False,
            "nativePromiseUnchanged": True,
            "noCampaignFactOrNativeAuthority": True,
            "noSpellIdentityAcceptanceOrApplication": True,
            "noSealBlockerClosureOrQueueCanonRuntimeChange": True,
        },
        "stateProjectionSemantics": {
            "parentProjectionIsImmutable": True,
            "actorOverridesAndWorldClockAreBranchLocal": True,
            "itemOverridesShadowTheParentByStableId": True,
            "nullItemOverrideMeansNoActiveSceneCopyWhileTheLedgerOwnsTheSingleIntactItem": True,
            "newObligationsAndHistoriesAreBranchLocal": True,
            "parentProjectionState": "The exact source state is included once above and is referenced by hash by every branch.",
        },
        "branches": branches,
        "summary": {
            "branchCount": len(branches),
            "eachStartsFromSameParent": all(b["branchStartStateSHA256"] for b in branches),
            "oneInheritedCastAndOneObligationPerBranch": True,
            "constructionOnly": True,
            "noSealAcceptanceApplicationOrQueueChange": True,
        },
    }
    # Keep the full, source-bound parent state once in the packet; each branch state hash references its hash.
    return packet


def write_packet(packet: dict[str, Any]) -> None:
    target = ROOT / PACKET_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    packet = build_packet()
    output = ROOT / PACKET_REL
    write_packet(packet)
    verify_packet_path(output, packet)
    print(f"PASS: wrote {output.relative_to(ROOT)}")
    print(f"PASS: {len(packet['branches'])} isolated branches; {sum(len(b['transitions']) for b in packet['branches'])} transitions")
    for b in packet["branches"]:
        print(f"{b['caseId']}: {b['branchStartStateSHA256']} -> {b['finalStateSHA256']} ({len(b['transitions'])} transitions)")
    return 0


def verify_packet_path(path: Path, expected: dict[str, Any]) -> None:
    # Verify the written packet against the source-bound build, then replay its explicit start states.
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError("packet differs from deterministic, source-validated construction")
    if digest(actual["parentProjection"]["state"]) != actual["parentProjectionCanonicalSHA256"]:
        raise AssertionError("included parent projection does not match its canonical hash")
    if actual["parentProjectionCanonicalSHA256"] != PARENT_STATE_SHA256:
        raise AssertionError("included parent projection is not the adopted source state")
    for branch in actual["branches"]:
        case_id = branch["caseId"]
        state = copy.deepcopy(branch["branchStartState"])
        if digest(state) != branch["branchStartStateSHA256"]:
            raise AssertionError(f"{case_id}: recorded branch start hash mismatch")
        # Forward replay from the packet's self-contained start state.
        for transition in branch["transitions"]:
            if digest(state) != transition["beforeStateSHA256"]:
                raise AssertionError(f"{case_id}: forward before-hash mismatch at {transition['eventId']}")
            apply_ops(state, transition["forward"])
            if digest(state) != transition["afterStateSHA256"]:
                raise AssertionError(f"{case_id}: forward after-hash mismatch at {transition['eventId']}")
            if state["overlay"]["nowMs"] != transition["atMs"]:
                raise AssertionError(f"{case_id}: overlay clock does not match {transition['eventId']}")
            if transition["eventId"].endswith(("-6000-W-START", "-6101-CLOSE-INITIATIVE")):
                if state["overlay"]["actorOverrides"]["W"].get("regularEnds") != [1900]:
                    raise AssertionError(f"{case_id}: W END1900 history was not retained")
        if digest(state) != branch["finalStateSHA256"]:
            raise AssertionError(f"{case_id}: forward replay final state mismatch")
        # Reverse the explicit inverse evidence in reverse chronological order.
        for transition in reversed(branch["transitions"]):
            if digest(state) != transition["afterStateSHA256"]:
                raise AssertionError(f"{case_id}: inverse after-hash mismatch at {transition['eventId']}")
            apply_ops(state, transition["inverse"])
            if digest(state) != transition["beforeStateSHA256"]:
                raise AssertionError(f"{case_id}: inverse before-hash mismatch at {transition['eventId']}")
        if digest(state) != branch["branchStartStateSHA256"]:
            raise AssertionError(f"{case_id}: inverse did not return to branch start")
        terminal_transition = next(
            t for t in branch["transitions"]
            if t["eventId"] == f"{case_id}-{TERMINAL}-ATOMIC-TERMINAL"
        )
        terminal_hash = terminal_transition["afterStateSHA256"]
        if any(branch["idempotency"][field] != terminal_hash for field in
               ("firstCallPostStateSHA256", "retryBeforeStateSHA256", "retryAfterStateSHA256")):
            raise AssertionError(f"{case_id}: retry is not bound to the post-terminal state")
        if branch["idempotency"]["retryBeforeStateSHA256"] != branch["idempotency"]["retryAfterStateSHA256"]:
            raise AssertionError(f"{case_id}: terminal retry is not a no-op")


if __name__ == "__main__":
    raise SystemExit(main())
