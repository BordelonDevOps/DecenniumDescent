from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
import sys
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[4]
OUT = AUDIT / "rank9_summon_elemental_avatar_closure_348_delivery"
SPELL = "summon-elemental-avatar"
BLOCKER = "SH202-B01"
AUTHORITY = {
    "reviewedApplied": 825,
    "pending": 23,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 549,
    "scopedInterfaces": 173,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def pretty(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def state_hash(value: object) -> str:
    return sha(canonical(value))


def binding(path: Path, relative_to: Path = ROOT) -> dict:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "bytes": len(raw),
        "sha256": sha(raw),
        "crc32": crc(raw),
    }


def ptr_parts(pointer: str) -> list[str]:
    if pointer == "":
        return []
    if not pointer.startswith("/"):
        raise ValueError(f"not a JSON pointer: {pointer}")
    return [p.replace("~1", "/").replace("~0", "~") for p in pointer[1:].split("/")]


def ptr_get(state: object, pointer: str):
    value = state
    for part in ptr_parts(pointer):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def ptr_set(state: object, pointer: str, value: object) -> None:
    parts = ptr_parts(pointer)
    parent = state
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    key = parts[-1]
    if isinstance(parent, list):
        parent[int(key)] = copy.deepcopy(value)
    else:
        parent[key] = copy.deepcopy(value)


def apply_values(state: dict, values: dict[str, object]) -> list[dict]:
    ops = []
    for pointer in sorted(values):
        before = copy.deepcopy(ptr_get(state, pointer))
        after = copy.deepcopy(values[pointer])
        if before == after:
            continue
        ops.append({"path": pointer, "before": before, "after": after})
        ptr_set(state, pointer, after)
    return ops


def apply_ops(state: dict, ops: list[dict], reverse: bool = False) -> None:
    iterable = list(reversed(ops)) if reverse else ops
    for op in iterable:
        expected = op["after"] if reverse else op["before"]
        replacement = op["before"] if reverse else op["after"]
        actual = ptr_get(state, op["path"])
        if actual != expected:
            raise AssertionError(f"patch precondition mismatch at {op['path']}: {actual!r} != {expected!r}")
        ptr_set(state, op["path"], replacement)


def hash_projection(snapshot: dict, paths: list[str]) -> dict:
    return {path: copy.deepcopy(ptr_get(snapshot, path)) for path in paths}


def add_component_damage(state: dict, root: dict) -> tuple[dict, dict]:
    avatar = state["avatar"]
    resolved = []
    for component in root["components"]:
        kind = component["damageType"]
        amount = component["amount"]
        if kind in avatar["immunities"]:
            amount_after_defense = 0
            defense = "immune"
        elif kind in avatar["resistances"]:
            amount_after_defense = amount // 2
            defense = "resistance-half-floor"
        else:
            amount_after_defense = amount
            defense = "none"
        resolved.append({
            "componentId": component["componentId"],
            "damageType": kind,
            "rawAmount": component["amount"],
            "resolvedAmount": amount_after_defense,
            "defense": defense,
            "rootId": root["rootId"],
            "dealerRootId": component["dealerRootId"],
        })
    total = sum(row["resolvedAmount"] for row in resolved)
    temp_before = avatar["tempHP"]
    hp_before = avatar["HP"]
    temp_absorbed = min(temp_before, total)
    hp_damage = max(0, total - temp_absorbed)
    avatar_after = copy.deepcopy(avatar)
    avatar_after["tempHP"] = temp_before - temp_absorbed
    avatar_after["HP"] = max(0, hp_before - hp_damage)
    if avatar_after["HP"] == 0:
        avatar_after["life"] = "Ended"
        avatar_after["active"] = False
    root_record = {
        "rootId": root["rootId"],
        "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT",
        "components": resolved,
        "totalResolvedOnce": total,
        "tempHPAbsorbed": temp_absorbed,
        "hpDamage": hp_damage,
    }
    roots_after = copy.deepcopy(state["incomingDamageRoots"]) + [root_record]
    settlements_after = copy.deepcopy(state["lifecycleSettlements"]) + [{
        "rootId": root["rootId"],
        "targetId": avatar["id"],
        "totalResolvedOnce": total,
        "hpBefore": hp_before,
        "hpAfter": avatar_after["HP"],
        "tempHPBefore": temp_before,
        "tempHPAfter": avatar_after["tempHP"],
        "lifeBefore": avatar["life"],
        "lifeAfter": avatar_after["life"],
    }]
    values = {
        "/avatar": avatar_after,
        "/incomingDamageRoots": roots_after,
        "/lifecycleSettlements": settlements_after,
    }
    observed = {
        "rootId": root["rootId"],
        "resolvedComponents": resolved,
        "totalResolvedOnce": total,
        "tempHPAbsorbed": temp_absorbed,
        "hpDamage": hp_damage,
        "hpAfter": avatar_after["HP"],
        "tempHPAfter": avatar_after["tempHP"],
        "lifeAfter": avatar_after["life"],
        "settlementCountAfter": len(settlements_after),
        "distinctRootCountAfter": len(roots_after),
    }
    return values, observed


def reduce_event(case_id: str, state: dict, event: dict) -> tuple[dict[str, object], dict]:
    kind = event["type"]
    if kind == "cancel_remaining_reserved_strikes":
        round_key = state["currentRoundKey"]
        ledger = copy.deepcopy(state["strikeLedgers"].get(round_key, {"reservedSlots": 0, "attemptedSlots": 0, "consumedSlots": [], "cancelledSlots": []}))
        cancelled = list(range(ledger["attemptedSlots"] + 1, ledger["reservedSlots"] + 1))
        ledger["attemptedSlots"] = ledger["reservedSlots"]
        ledger["consumedSlots"] = sorted(set(ledger["consumedSlots"] + cancelled))
        ledger["cancelledSlots"] = sorted(set(ledger["cancelledSlots"] + cancelled))
        ledgers = copy.deepcopy(state["strikeLedgers"])
        ledgers[round_key] = ledger
        return {"/strikeLedgers": ledgers}, {"cancelledSlots": cancelled, "capacityConsumed": ledger["attemptedSlots"], "refund": 0}
    if kind == "conditional_extra_turn_notification":
        return {}, {"notificationObserved": True, "newCommand": False, "regularStartOrAttachedPhase": False, "budgetReset": False, "sourceDeadlineMs": state["sourceDeadlineMs"]}
    if kind in ("attempt_fourth_strike", "attempt_strike_without_command", "unknown_gameplay_turn_attempt", "attempt_cancelled_old_order_strike", "attempt_out_of_turn_order"):
        reason = {
            "attempt_fourth_strike": "THREE_RESERVED_SLOTS_ALREADY_CONSUMED",
            "attempt_strike_without_command": "NO_COMMAND_OR_OFFENSIVE_ACTION_TOKEN",
            "unknown_gameplay_turn_attempt": "NO_AUTHORIZED_PROVIDER_BOUND",
            "attempt_cancelled_old_order_strike": "OLD_CONTROLLER_ORDER_INVALIDATED",
            "attempt_out_of_turn_order": "CONTROLLER_HAS_NO_ACTUAL_REGULAR_TURN",
        }[kind]
        return {}, {"accepted": False, "reason": reason, "stateMutation": False}
    if kind == "advance_actual_numbered_round":
        if event["roundNumber"] <= state["currentRoundNumber"]:
            raise AssertionError("numbered-round control must advance")
        return {
            "/currentRoundKey": event["roundKey"],
            "/currentRoundNumber": event["roundNumber"],
        }, {"actualNumberedRoundObserved": True, "roundKey": event["roundKey"], "commandOrActionGranted": False}
    if kind == "resolve_avatar_damage_root":
        return add_component_damage(state, event["root"])
    if kind == "unknown_provider_damage_attempt":
        return {}, {"accepted": False, "reason": "NO_AUTHORIZED_PROVIDER_BOUND", "stateMutation": False}
    if kind == "change_controller":
        new_controller = event["newControllerId"]
        ledger = copy.deepcopy(state["strikeLedgers"].get(state["currentRoundKey"], {"reservedSlots": 0, "attemptedSlots": 0, "consumedSlots": [], "cancelledSlots": []}))
        remaining = list(range(ledger["attemptedSlots"] + 1, ledger["reservedSlots"] + 1))
        ledger["attemptedSlots"] = ledger["reservedSlots"]
        ledger["consumedSlots"] = sorted(set(ledger["consumedSlots"] + remaining))
        ledger["cancelledSlots"] = sorted(set(ledger["cancelledSlots"] + remaining))
        ledgers = copy.deepcopy(state["strikeLedgers"])
        if ledger["reservedSlots"] or ledger["attemptedSlots"]:
            ledgers[state["currentRoundKey"]] = ledger
        cancelled_order = state.get("pendingOrder")
        history = copy.deepcopy(state["orderHistory"])
        if cancelled_order is not None:
            history.append({"orderId": cancelled_order["orderId"], "status": "cancelled-by-controller-change", "refund": 0})
        values = {
            "/currentControllerId": new_controller,
            "/pendingOrder": None,
            "/strikeLedgers": ledgers,
            "/orderHistory": history,
        }
        return values, {
            "controllerAfter": new_controller,
            "oldOrderCancelled": cancelled_order is not None,
            "cancelledSlots": remaining,
            "capacityConsumed": ledger["attemptedSlots"],
            "thirdStrikeAccepted": False if ledger["reservedSlots"] == 3 else None,
            "fourthStrikeAccepted": False,
            "sourceOwnerChanged": False,
            "strikeCapReset": False,
            "refund": 0,
        }
    if kind == "open_actual_controller_regular_turn":
        if not event["isActualRegularTurn"]:
            raise AssertionError("positive command fixture must use a regular turn")
        return {
            "/controllerTurn": {"turnId": event["turnId"], "active": True, "isExtraTurn": False},
            "/bonusActionAvailable": event["bonusActionAvailable"],
            "/sharedCommandAllowance": event["sharedCommandAllowance"],
        }, {"actualRegularTurn": True, "isExtraTurn": False, "availableBonusAction": event["bonusActionAvailable"], "sharedCommandAllowance": event["sharedCommandAllowance"]}
    if kind == "issue_new_controller_order":
        checks = {
            "isCurrentController": event["controllerId"] == state["currentControllerId"],
            "actualRegularTurn": state["controllerTurn"].get("active") is True and state["controllerTurn"].get("isExtraTurn") is False,
            "bonusAction": state["bonusActionAvailable"] is True,
            "sharedAllowance": state["sharedCommandAllowance"] > 0,
            "conscious": event["conscious"] is True,
            "perception": event["perception"] is True,
            "samePlane": event["samePlane"] is True,
            "audibleCommon": event["audibleCommon"] is True,
            "lineOfEffect": event["lineOfEffect"] is True,
            "within60FeetAtIssuanceAndExecution": event["distanceAtIssuanceFeet"] <= 60 and event["distanceAtExecutionFeet"] <= 60,
            "futureOwnerPhaseBeforeDeadline": event["ownerPhaseTimestampMs"] < state["sourceDeadlineMs"],
        }
        allowed = all(checks.values())
        if not allowed:
            return {}, {"accepted": False, "checks": checks, "stateMutation": False}
        order = {
            "orderId": event["orderId"],
            "controllerId": event["controllerId"],
            "bodyId": state["bodyId"],
            "targetId": event["targetId"],
            "status": "pending-original-owner-attached-phase",
            "roundKey": state["currentRoundKey"],
        }
        history = copy.deepcopy(state["orderHistory"])
        history.append({"orderId": order["orderId"], "status": "issued", "refund": 0})
        return {
            "/pendingOrder": order,
            "/bonusActionAvailable": False,
            "/sharedCommandAllowance": state["sharedCommandAllowance"] - 1,
            "/orderHistory": history,
        }, {"accepted": True, "checks": checks, "order": order}
    if kind == "execute_at_original_owner_attached_phase":
        order = state.get("pendingOrder")
        valid = (
            order is not None
            and event["ownerId"] == state["sourceOwnerId"]
            and event["phaseId"] == state["ownerPhaseCalendar"]["nextPhaseId"]
            and event["phaseIsDue"] is True
            and event["atMs"] == state["ownerPhaseCalendar"]["nextPhaseAtMs"]
            and event["atMs"] < state["sourceDeadlineMs"]
            and order["roundKey"] == state["currentRoundKey"]
        )
        if not valid:
            return {}, {"executed": False, "reason": "NO_LAWFUL_ORIGINAL_OWNER_ATTACHED_PHASE", "stateMutation": False}
        ledgers = copy.deepcopy(state["strikeLedgers"])
        ledgers[state["currentRoundKey"]] = {"reservedSlots": 3, "attemptedSlots": 0, "consumedSlots": [], "cancelledSlots": [], "sourceOwnerId": state["sourceOwnerId"], "controllerId": state["currentControllerId"]}
        history = copy.deepcopy(state["orderHistory"])
        history.append({"orderId": order["orderId"], "status": "executed-at-original-owner-phase", "refund": 0})
        return {"/pendingOrder": None, "/strikeLedgers": ledgers, "/orderHistory": history}, {
            "executed": True,
            "phaseId": event["phaseId"],
            "phaseOwner": event["ownerId"],
            "attackActionReservedSlots": 3,
            "currentControllerId": state["currentControllerId"],
            "sourceOwnerId": state["sourceOwnerId"],
        }
    if kind == "return_control_to_original_owner":
        old_id = state["originalOrderId"]
        return {"/currentControllerId": state["sourceOwnerId"], "/pendingOrder": None}, {
            "controllerRestored": True,
            "oldOrderRestored": state.get("pendingOrder") is not None and state["pendingOrder"].get("orderId") == old_id,
            "pendingOrderAfter": None,
            "hpBefore": state["preservedHP"],
            "resourcesBefore": copy.deepcopy(state["resourceHistory"]),
            "restorationGrantedHPOrResource": False,
        }
    if kind == "resolve_shared_aura_marker":
        sources = state["auraSources"]
        due = [row for row in sources if row["due"] and not row["consumed"]]
        eligible = [row for row in due if row["sourceAlive"] and row["withinAura"] and not row["auraIntersectionSuppressed"]]
        winner = min(eligible, key=lambda row: (-row["rolledPool"], row["applicationOrder"], row["sourceId"])) if eligible else None
        sources_after = copy.deepcopy(sources)
        for row in sources_after:
            if row["due"] and not row["consumed"]:
                row["consumed"] = True
        recipient_after = copy.deepcopy(state["recipient"])
        packet_history = copy.deepcopy(state["packetHistory"])
        outcome = None
        if winner:
            saved = event["dexSaveTotal"] >= winner["dc"]
            unsaved_damage = winner["rolledPool"] if not saved else winner["rolledPool"] // 2
            damage = unsaved_damage
            if "fire" in recipient_after["resistances"]:
                damage //= 2
            absorbed = min(recipient_after["tempHP"], damage)
            hp_damage = max(0, damage - absorbed)
            recipient_after["tempHP"] -= absorbed
            recipient_after["HP"] = max(0, recipient_after["HP"] - hp_damage)
            outcome = {
                "sourceId": winner["sourceId"],
                "dealerId": winner["dealerId"],
                "rootId": winner["rootId"],
                "dc": winner["dc"],
                "rolledPoolBeforeRecipientDefense": winner["rolledPool"],
                "saveType": "DEX",
                "saveTotal": event["dexSaveTotal"],
                "saveSucceeded": saved,
                "afterSaveDamage": unsaved_damage,
                "fireResistanceAppliedOnce": "fire" in recipient_after["resistances"],
                "damageAfterDefense": damage,
                "tempHPAbsorbed": absorbed,
                "hpDamage": hp_damage,
                "hpAfter": recipient_after["HP"],
                "tempHPAfter": recipient_after["tempHP"],
            }
            packet_history.append(outcome)
        return {
            "/auraSources": sources_after,
            "/recipient": recipient_after,
            "/packetHistory": packet_history,
        }, {
            "winner": outcome,
            "packetsApplied": 1 if winner else 0,
            "consumedDueSourceIds": [row["sourceId"] for row in due],
            "losingOrSuppressedOpportunitiesConsumed": True,
        }
    if kind == "check_aura_later_marker_for_replay":
        return {}, {"newMarkerHasDueSourceEntries": False, "priorLosingOrSuppressedPacketReplayed": False, "stateMutation": False}
    if kind == "enter_initiative":
        return {"/clockMode": "initiative", "/initiativeEntryMs": event["atMs"]}, {
            "initiativeEntered": True,
            "existingNextDueMs": state["nextDueMs"],
            "pulseAtEntry": False,
        }
    if kind == "regular_start_before_carried_due":
        if event["atMs"] >= state["nextDueMs"]:
            raise AssertionError("early marker must precede carried exposure due time")
        return {}, {"regularStartObserved": True, "atMs": event["atMs"], "auraPulse": False, "nextDueUnchanged": state["nextDueMs"]}
    if kind == "resolve_carried_exposure_due":
        if event["atMs"] != state["nextDueMs"] or not state["pendingExposureDue"]:
            raise AssertionError("carried exposure callback must resolve at its immutable original timestamp")
        eligible = state["sourceAlive"] and state["recipientPresent"] and not state["auraIntersectionSuppressed"]
        pulses = state["pulseCount"] + (1 if eligible else 0)
        consumed = copy.deepcopy(state["consumedOpportunityIds"])
        consumed.append(state["pendingOpportunityId"])
        values = {
            "/pendingExposureDue": False,
            "/pulseCount": pulses,
            "/consumedOpportunityIds": consumed,
            "/lastDueResolutionMs": event["atMs"],
        }
        return values, {
            "dueTimestampMs": state["nextDueMs"],
            "opportunityConsumed": True,
            "pulse": eligible,
            "coalescedCoincidentRegularStart": event["coincidentRegularStart"],
            "pulseCountAfter": pulses,
            "actorBudgetOrSourceClockChanged": False,
        }
    if kind == "later_regular_start_after_carried_due":
        eligible = state["sourceAlive"] and state["recipientPresent"] and not state["auraIntersectionSuppressed"]
        pulses = state["pulseCount"] + (1 if eligible else 0)
        return {"/pulseCount": pulses, "/laterRegularStartMarkersObserved": state["laterRegularStartMarkersObserved"] + [event["atMs"]]}, {
            "regularStartMs": event["atMs"],
            "strictlyLaterThanCarriedDue": event["atMs"] > state["nextDueMs"],
            "pulse": eligible,
            "pulseCountAfter": pulses,
            "noExposureCatchup": True,
        }
    if kind == "set_recipient_outside_at_due":
        return {"/recipientPresent": False}, {"recipientPresentAtDue": False}
    if kind == "set_aura_intersection_suppressed_at_due":
        return {"/auraIntersectionSuppressed": True}, {"auraIntersectionSuppressedAtDue": True}
    if kind == "source_ends_before_due":
        return {"/sourceAlive": False}, {"sourceAliveAtDue": False}
    if kind == "recipient_reenters_before_next_regular_marker":
        return {"/recipientPresent": True, "/auraIntersectionSuppressed": False}, {"recipientBackBeforeNextMarker": True, "pulseAtExit": False}
    if kind == "expire_source_at_original_deadline":
        return {"/sourceAlive": False, "/sourceBodyActive": False, "/sourceBody/active": False}, {"sourceExpiredAtOriginalDeadline": True, "deadlineRewritten": False}
    if kind == "leave_local_suppression_region":
        return {"/recipientInSuppressionRegion": False}, {"leftSuppressionRegion": True, "pulseOnLeaving": False}
    if kind == "resolve_local_aura_marker":
        eligible = (
            state["sourceBodyActive"]
            and event["atMs"] < state["sourceDeadlineMs"]
            and state["recipientWithinAura"]
            and not state["recipientInSuppressionRegion"]
        )
        pulses = state["pulseCount"] + (1 if eligible else 0)
        consumed = copy.deepcopy(state["consumedDueMarkerIds"])
        consumed.append(event["markerId"])
        return {"/pulseCount": pulses, "/consumedDueMarkerIds": consumed}, {
            "markerId": event["markerId"],
            "pulse": eligible,
            "sourceBodyActive": state["sourceBodyActive"],
            "pulseCountAfter": pulses,
        }
    if kind == "local_suppressed_due":
        if not state["recipientWithinAura"] or not state["recipientInSuppressionRegion"] or state["sourceBodyInSuppressionRegion"]:
            raise AssertionError("local-only suppression operand must intersect the recipient but not the source body")
        consumed = copy.deepcopy(state["consumedDueMarkerIds"])
        consumed.append(event["markerId"])
        return {"/consumedDueMarkerIds": consumed}, {
            "markerId": event["markerId"],
            "pulse": False,
            "bodySuppressed": False,
            "bodyPersists": state["sourceBodyActive"],
            "strikeLedgerUnchanged": True,
            "dueOpportunityConsumed": True,
        }
    raise ValueError(f"unsupported transition {case_id}:{kind}")


def execute_scenario(case_id: str, scenario: dict) -> dict:
    state = copy.deepcopy(scenario["startingState"])
    start = copy.deepcopy(state)
    start_sha = state_hash(start)
    transitions = []
    all_forward = []
    for ordinal, event in enumerate(scenario["events"], start=1):
        before = copy.deepcopy(state)
        result = None
        if event["type"] == "resolve_avatar_damage_root":
            values, result = add_component_damage(state, event["root"])
        else:
            values, result = reduce_event(case_id, state, event)
        operations = apply_values(state, values)
        after = copy.deepcopy(state)
        inverse = [{"path": op["path"], "before": op["after"], "after": op["before"]} for op in reversed(operations)]
        transitions.append({
            "ordinal": ordinal,
            "event": copy.deepcopy(event),
            "beforeState": before,
            "beforeStateSha256": state_hash(before),
            "observedResult": result,
            "forwardOperations": operations,
            "afterState": after,
            "afterStateSha256": state_hash(after),
            "inverseOperations": inverse,
        })
        all_forward.append(operations)
        for pointer in scenario.get("unchangedPaths", []):
            if ptr_get(start, pointer) != ptr_get(state, pointer):
                raise AssertionError(f"unchanged-path drift in {scenario['scenarioId']} at {pointer}")
    final = copy.deepcopy(state)
    restored = copy.deepcopy(final)
    for operations in reversed(all_forward):
        apply_ops(restored, operations, reverse=True)
    reversal = {
        "allTransitionsFullyReversed": restored == start,
        "restoredStateSha256": state_hash(restored),
        "startingStateSha256": start_sha,
        "fullReverseTraversal": True,
    }
    if not reversal["allTransitionsFullyReversed"] or reversal["restoredStateSha256"] != start_sha:
        raise AssertionError(f"inverse traversal failed for {scenario['scenarioId']}")
    return {
        "scenarioId": scenario["scenarioId"],
        "fixtureStatus": scenario["fixtureStatus"],
        "purpose": scenario["purpose"],
        "preservedFork": scenario.get("preservedFork"),
        "testOnlyOverlay": scenario.get("testOnlyOverlay", []),
        "startingState": start,
        "startingStateSha256": start_sha,
        "transitions": transitions,
        "finalState": final,
        "finalStateSha256": state_hash(final),
        "unchangedPaths": scenario.get("unchangedPaths", []),
        "reversal": reversal,
    }


def make_avatar_projection(body: dict, hp: int | None = None, temp_hp: int | None = None) -> dict:
    return {
        "id": body["id"],
        "profileId": body["profileId"],
        "spellId": body["spellId"],
        "sourceId": body["sourceId"],
        "sourceOwnerId": body["sourceOwner"],
        "currentControllerId": body["controller"],
        "creationTick": body["creationTick"],
        "pos": copy.deepcopy(body["pos"]),
        "HP": body["HP"] if hp is None else hp,
        "maxHP": body["maxHP"],
        "tempHP": body["tempHP"] if temp_hp is None else temp_hp,
        "resistances": copy.deepcopy(body["resistances"]),
        "immunities": copy.deepcopy(body["immunities"]),
        "life": body["life"],
        "active": body["active"],
        "sourceEnded": body["sourceEnded"],
        "originalClass": body["originalClass"],
        "creationModifiers": copy.deepcopy(body["creationModifiers"]),
    }


def scenario(case_id: str, scenario_id: str, purpose: str, start: dict, events: list[dict], unchanged: list[str], preserved_fork: dict | None = None, overlay: list[dict] | None = None) -> dict:
    return {
        "scenarioId": scenario_id,
        "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT",
        "purpose": purpose,
        "startingState": start,
        "events": events,
        "unchangedPaths": unchanged,
        "preservedFork": preserved_fork,
        "testOnlyOverlay": overlay or [],
    }


def build_cases(avatar_body: dict, actor_b: dict, preserved_fork: dict) -> list[dict]:
    common_budget_unchanged = ["/actionBudgets", "/recharge", "/ready", "/sourceDeadlineMs", "/resourceHistory"]
    avatar_protected = ["/avatar/id", "/avatar/profileId", "/avatar/spellId", "/avatar/sourceId", "/avatar/sourceOwnerId", "/avatar/currentControllerId", "/avatar/maxHP", "/avatar/resistances", "/avatar/immunities", "/avatar/active", "/avatar/sourceEnded", "/avatar/originalClass", "/avatar/creationModifiers", "/sourceDeadlineMs"]
    cases = []

    # SH330-T01: all three reserved slots are spent, including canceled components.
    start1 = {
        "ownerId": "owner-A", "sourceOwnerId": "owner-A", "currentControllerId": "owner-A", "bodyId": "avatar-A", "formationSourceId": "cast-A",
        "currentRoundKey": "round-17", "currentRoundNumber": 17,
        "strikeLedgers": {"round-17": {"reservedSlots": 3, "attemptedSlots": 1, "consumedSlots": [1], "cancelledSlots": []}},
        "commandAvailable": False, "actionBudgets": {"Action": 0, "BonusAction": 0, "Reaction": 1, "ownerAllowance": 1},
        "phaseCalendar": {"nextOwnerPhaseId": "owner-A-phase-17", "nextOwnerPhaseAtMs": 12000, "phaseActive": False},
        "sourceDeadlineMs": 60000, "resourceHistory": {"RPSpent": 26, "cadenceSpent": True}, "recharge": {"breath": 0}, "ready": None,
        "damageRoots": [], "authorizedFullTurnProviderBound": False,
    }
    cases.append({
        "testId": "SH330-T01", "id": "SH330-T01-extra-turn-strike-cap", "purpose": "A conditional full-turn notification cannot refresh reserved round strike capacity; canceled components consume their slots and only a new numbered round can open a distinct cap key.",
        "scenarios": [
            scenario("SH330-T01", "T01-main", "Cancel remaining reserved strikes, receive a conditional extra-turn notification, deny strike four, then advance to an actual numbered round without creating a command or action.", start1, [
                {"type": "cancel_remaining_reserved_strikes", "atMs": 1000},
                {"type": "conditional_extra_turn_notification", "atMs": 2000, "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT", "providerAcquired": False},
                {"type": "attempt_fourth_strike", "atMs": 2001, "strikeNumber": 4},
                {"type": "advance_actual_numbered_round", "atMs": 6000, "roundKey": "round-18", "roundNumber": 18},
                {"type": "attempt_strike_without_command", "atMs": 6001, "strikeNumber": 1},
                {"type": "unknown_gameplay_turn_attempt", "atMs": 7000, "providerId": None, "sourceAcquired": False},
            ], common_budget_unchanged + ["/phaseCalendar", "/sourceOwnerId", "/currentControllerId", "/damageRoots", "/authorizedFullTurnProviderBound"]),
        ],
    })

    # Bind Return285's actual Avatar body and the source target state at formation event 6.
    avatar_base = make_avatar_projection(avatar_body)
    base_history = {"incomingDamageRoots": [], "lifecycleSettlements": []}
    damage_overlay = [{"path": "/avatar/HP", "fromPreserved": avatar_body["HP"], "toTestValue": 30}, {"path": "/avatar/tempHP", "fromPreserved": avatar_body["tempHP"], "toTestValue": 3}]
    def damage_start(hp: int | None = None, temp: int | None = None) -> dict:
        return {"avatar": make_avatar_projection(avatar_body, hp, temp), **copy.deepcopy(base_history), "sourceDeadlineMs": 60000}
    fire6force8 = {"rootId": "SH330-T02-COMPOSITE-6F8F", "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT", "components": [
        {"componentId": "fire-6", "damageType": "fire", "amount": 6, "dealerRootId": "TEST_ONLY:single-composite-root"},
        {"componentId": "force-8", "damageType": "force", "amount": 8, "dealerRootId": "TEST_ONLY:single-composite-root"},
    ]}
    fire11force8 = {"rootId": "SH330-T02-CONTRACT-11F8F", "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT", "components": [
        {"componentId": "fire-11", "damageType": "fire", "amount": 11, "dealerRootId": "TEST_ONLY:single-contract-root"},
        {"componentId": "force-8", "damageType": "force", "amount": 8, "dealerRootId": "TEST_ONLY:single-contract-root"},
    ]}
    separate_fire6 = {"rootId": "SH330-T02-SEPARATE-FIRE-ROOT", "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT", "components": [{"componentId": "fire-6", "damageType": "fire", "amount": 6, "dealerRootId": "TEST_ONLY:fire-root"}]}
    separate_force8 = {"rootId": "SH330-T02-SEPARATE-FORCE-ROOT", "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT", "components": [{"componentId": "force-8", "damageType": "force", "amount": 8, "dealerRootId": "TEST_ONLY:force-root"}]}
    cases.append({
        "testId": "SH330-T02", "id": "SH330-T02-typed-damage-and-avatar-lifecycle", "purpose": "Use the exact Return285 Avatar body identity/profile, correct Return331's composite-root ambiguity, preserve separate-root settlement order, and also prove the contract's fire11/force8 calculation.",
        "scenarios": [
            scenario("SH330-T02", "T02-avatar-composite-fire6-force8", "One conditional composite event root carries fire6 and force8 components into the exact Avatar recipient; resistance resolves fire to3, aggregate11 is settled once.", damage_start(), [{"type": "resolve_avatar_damage_root", "root": fire6force8}], avatar_protected, preserved_fork),
            scenario("SH330-T02", "T02-avatar-composite-fire11-force8", "The SH330-T02 required calculation uses the same exact Avatar profile; fire11 halves down to5, force8 stays8, aggregate13 settles once.", damage_start(), [{"type": "resolve_avatar_damage_root", "root": fire11force8}], avatar_protected, preserved_fork),
            scenario("SH330-T02", "T02-tempHP-on-exact-avatar-projection", "A clearly declared synthetic HP30/tempHP3 overlay on the exact Avatar identity demonstrates once-only tempHP/HP lifecycle settlement for the contract's fire11/force8 composite.", damage_start(30, 3), [{"type": "resolve_avatar_damage_root", "root": fire11force8}], avatar_protected, preserved_fork, damage_overlay),
            scenario("SH330-T02", "T02-two-roots-two-ordered-settlements", "Two explicitly distinct conditional roots remain separate and are settled in order against the same Avatar recipient rather than being merged.", damage_start(30, 3), [
                {"type": "resolve_avatar_damage_root", "root": separate_fire6},
                {"type": "resolve_avatar_damage_root", "root": separate_force8},
            ], avatar_protected, preserved_fork, damage_overlay),
            scenario("SH330-T02", "T02-unknown-provider-unavailable", "A gameplay damage attempt with no source/provider binding is rejected before target state mutation.", damage_start(), [{"type": "unknown_provider_damage_attempt", "providerId": None, "sourceAcquired": False}], avatar_protected, preserved_fork),
        ],
    })

    # SH330-T03: cancellation consumes the last reserved slot; new orders require a lawful later turn.
    start3 = {
        "sourceOwnerId": "owner-A", "currentControllerId": "owner-A", "bodyId": "avatar-A", "formationSourceId": "cast-A", "originalOrderId": "order-A-old",
        "currentRoundKey": "round-21", "currentRoundNumber": 21,
        "strikeLedgers": {"round-21": {"reservedSlots": 3, "attemptedSlots": 2, "consumedSlots": [1, 2], "cancelledSlots": []}},
        "pendingOrder": {"orderId": "order-A-old", "controllerId": "owner-A", "targetId": "target-B", "status": "unexecuted", "roundKey": "round-21"},
        "orderHistory": [], "sourceDeadlineMs": 60000,
        "ownerPhaseCalendar": {"ownerId": "owner-A", "nextPhaseId": "owner-A-attached-22", "nextPhaseAtMs": 30000},
        "controllerTurn": {"turnId": None, "active": False, "isExtraTurn": False}, "bonusActionAvailable": False, "sharedCommandAllowance": 0,
        "conscious": True, "perception": True, "samePlane": True, "audibleCommon": True, "lineOfEffect": True,
        "originalClass": "Wizard", "statLineage": {"class": "Wizard", "conjuration": 17}, "formationTimestampMs": 200,
        "preservedHP": 197, "hp": 197, "tempHP": 0, "conditions": [], "cargo": [], "resourceHistory": {"RPSpent": 26, "cadenceSpent": True, "paidHistoryId": "cast-A"},
        "commandAllowanceRefunds": 0,
    }
    cases.append({
        "testId": "SH330-T03", "id": "SH330-T03-controller-change-and-order-lineage", "purpose": "A controller change invalidates the old order, consumes the remaining reserved strike slot without refund, and permits a later order only on an actual lawful controller turn and the original owner's attached phase.",
        "scenarios": [
            scenario("SH330-T03", "T03-before-execution-and-lawful-later-command", "Change controller with reservedSlots3/attempts2, reject the canceled third strike and an out-of-turn order, then admit and execute a new order only in a subsequent numbered round with the required actual budgets and original-owner phase.", start3, [
                {"type": "change_controller", "atMs": 10000, "newControllerId": "controller-B", "conditionalInput": True},
                {"type": "attempt_cancelled_old_order_strike", "strikeNumber": 3},
                {"type": "attempt_out_of_turn_order", "controllerId": "controller-B", "regularTurnActive": False},
                {"type": "advance_actual_numbered_round", "atMs": 12000, "roundKey": "round-22", "roundNumber": 22},
                {"type": "open_actual_controller_regular_turn", "atMs": 15000, "turnId": "controller-B-regular-22", "isActualRegularTurn": True, "bonusActionAvailable": True, "sharedCommandAllowance": 1},
                {"type": "issue_new_controller_order", "atMs": 15001, "controllerId": "controller-B", "orderId": "order-B-22", "targetId": "target-C", "conscious": True, "perception": True, "samePlane": True, "audibleCommon": True, "lineOfEffect": True, "distanceAtIssuanceFeet": 40, "distanceAtExecutionFeet": 45, "ownerPhaseTimestampMs": 30000},
                {"type": "execute_at_original_owner_attached_phase", "atMs": 30000, "ownerId": "owner-A", "phaseId": "owner-A-attached-22", "phaseIsDue": True},
                {"type": "return_control_to_original_owner", "atMs": 31000},
            ], ["/sourceOwnerId", "/bodyId", "/formationSourceId", "/sourceDeadlineMs", "/ownerPhaseCalendar", "/originalClass", "/statLineage", "/formationTimestampMs", "/hp", "/tempHP", "/conditions", "/cargo", "/resourceHistory", "/commandAllowanceRefunds"]),
            scenario("SH330-T03", "T03-after-all-three-slots-spent", "After all three slots have been attempted, a conditional controller change preserves the exhausted key and still denies strike four.", {
                **copy.deepcopy(start3),
                "pendingOrder": None,
                "strikeLedgers": {"round-21": {"reservedSlots": 3, "attemptedSlots": 3, "consumedSlots": [1, 2, 3], "cancelledSlots": []}},
            }, [
                {"type": "change_controller", "atMs": 11000, "newControllerId": "controller-B", "conditionalInput": True},
                {"type": "attempt_fourth_strike", "atMs": 11001, "strikeNumber": 4},
            ], ["/sourceOwnerId", "/bodyId", "/formationSourceId", "/sourceDeadlineMs", "/ownerPhaseCalendar", "/strikeLedgers/round-21"]),
        ],
    })

    # SH330-T04: one same-family winner, all due entries consumed, correct winner metadata.
    actor_projection = {
        "id": actor_b["id"], "profileId": actor_b["profileId"], "HP": actor_b["HP"], "maxHP": actor_b["maxHP"], "tempHP": actor_b["tempHP"],
        "resistances": copy.deepcopy(actor_b["resistances"]), "immunities": copy.deepcopy(actor_b["immunities"]), "saves": copy.deepcopy(actor_b["saves"]),
        "actionBudgets": copy.deepcopy(actor_b["actions"]),
    }
    def aura_start(source_rows: list[dict], save_total: int = 18) -> dict:
        return {
            "recipient": copy.deepcopy(actor_projection),
            "dexSaveTotal": save_total,
            "auraSources": [{**copy.deepcopy(row), "due": True, "consumed": False} for row in source_rows],
            "packetHistory": [], "familyKey": "summon-elemental-avatar:aura", "markerId": "recipient-regular-start-44",
            "sourceExpiryMs": 60000,
        }
    src_a = {"sourceId": "avatar-A", "dealerId": "A:cast1:body1", "rootId": "SH330-T04-root-A", "applicationOrder": 1, "rolledPool": 7, "dc": 21, "sourceAlive": True, "withinAura": True, "auraIntersectionSuppressed": False, "fixtureStatus": "PRESERVED_SOURCE_PLUS_CONDITIONAL_ROLL"}
    src_b = {"sourceId": "avatar-B-test-only", "dealerId": "TEST_ONLY:avatar-B", "rootId": "SH330-T04-root-B", "applicationOrder": 2, "rolledPool": 9, "dc": 23, "sourceAlive": True, "withinAura": True, "auraIntersectionSuppressed": False, "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT"}
    cases.append({
        "testId": "SH330-T04", "id": "SH330-T04-same-family-aura-arbitration", "purpose": "At one shared recipient marker resolve only the greatest unsuppressed same-family roll, bind that source's DC/dealer/root, consume every due entry, and never replay a loser.",
        "scenarios": [
            scenario("SH330-T04", "T04-pool-7-versus-9", "The conditional second source rolls9 against source A's7; source B is the only applied packet and supplies its own DC/dealer/root.", aura_start([src_a, src_b], 18), [
                {"type": "resolve_shared_aura_marker", "markerId": "recipient-regular-start-44", "dexSaveTotal": 18},
                {"type": "check_aura_later_marker_for_replay", "markerId": "recipient-regular-start-45"},
            ], ["/familyKey", "/sourceExpiryMs", "/recipient/actionBudgets"]),
            scenario("SH330-T04", "T04-equal-pool-earlier-application-tie", "Equal pools use earlier application before sourceId.", aura_start([
                {**src_a, "rolledPool": 9, "applicationOrder": 1}, {**src_b, "rolledPool": 9, "applicationOrder": 2},
            ], 18), [{"type": "resolve_shared_aura_marker", "markerId": "recipient-regular-start-44", "dexSaveTotal": 18}], ["/familyKey", "/sourceExpiryMs", "/recipient/actionBudgets"]),
            scenario("SH330-T04", "T04-equal-pool-and-application-sourceId-tie", "Equal pools and equal application order use sourceId as the final deterministic tie-breaker.", aura_start([
                {**src_a, "sourceId": "avatar-Z", "rolledPool": 9, "applicationOrder": 3}, {**src_b, "sourceId": "avatar-A", "rolledPool": 9, "applicationOrder": 3},
            ], 18), [{"type": "resolve_shared_aura_marker", "markerId": "recipient-regular-start-44", "dexSaveTotal": 18}], ["/familyKey", "/sourceExpiryMs", "/recipient/actionBudgets"]),
            scenario("SH330-T04", "T04-suppressed-would-be-winner-consumed", "A locally suppressed pool9 source is ineligible before arbitration; its due opportunity is consumed while eligible pool7 resolves, with no later replay.", aura_start([
                src_a, {**src_b, "auraIntersectionSuppressed": True},
            ], 18), [
                {"type": "resolve_shared_aura_marker", "markerId": "recipient-regular-start-44", "dexSaveTotal": 18},
                {"type": "check_aura_later_marker_for_replay", "markerId": "recipient-regular-start-45"},
            ], ["/familyKey", "/sourceExpiryMs", "/recipient/actionBudgets"]),
        ],
    })

    # SH330-T05: carry the immutable outside-initiative due time into initiative.
    def exposure_start() -> dict:
        return {
            "sourceBodyId": avatar_body["id"], "sourceProfileId": avatar_body["profileId"], "sourceAlive": True,
            "sourceDeadlineMs": 60000, "recipientPresent": True, "auraIntersectionSuppressed": False,
            "clockMode": "outside-initiative", "firstExposureMs": 0, "nextDueMs": 6000, "pendingExposureDue": True,
            "pendingOpportunityId": "avatar-A/recipient-B/exposure-due-6000", "initiativeEntryMs": None,
            "regularStartCalendar": [4000, 6000, 10000, 16000], "pulseCount": 0, "consumedOpportunityIds": [],
            "lastDueResolutionMs": None, "laterRegularStartMarkersObserved": [],
            "actorBudgets": {"Action": 1, "BonusAction": 1, "Reaction": 1, "Ready": "unchanged"}, "recharge": 0,
        }
    exposure_protected = ["/sourceBodyId", "/sourceProfileId", "/sourceDeadlineMs", "/actorBudgets", "/recharge", "/regularStartCalendar", "/firstExposureMs", "/nextDueMs"]
    cases.append({
        "testId": "SH330-T05", "id": "SH330-T05-exposure-initiative-handoff", "purpose": "Carry the original six-second exposure callback into initiative; coalesce one coincident start, do not pulse at entry/early starts, and consume missed due work without catch-up.",
        "scenarios": [
            scenario("SH330-T05", "T05-coincident-start-and-later-markers", "Exposure starts at t0, initiative begins t2, an earlier regular START at t4 does not pulse, the due callback and coincident START at t6 coalesce once, and later actual starts at t10/t16 each resolve once.", exposure_start(), [
                {"type": "enter_initiative", "atMs": 2000},
                {"type": "regular_start_before_carried_due", "atMs": 4000},
                {"type": "resolve_carried_exposure_due", "atMs": 6000, "coincidentRegularStart": True},
                {"type": "later_regular_start_after_carried_due", "atMs": 10000},
                {"type": "later_regular_start_after_carried_due", "atMs": 16000},
            ], exposure_protected),
            scenario("SH330-T05", "T05-outside-at-due-no-catchup", "Recipient is outside at t6, so that pending exposure opportunity is consumed without a pulse; re-entry before t10 permits only the next independently scheduled marker.", exposure_start(), [
                {"type": "enter_initiative", "atMs": 2000},
                {"type": "set_recipient_outside_at_due", "atMs": 5900},
                {"type": "resolve_carried_exposure_due", "atMs": 6000, "coincidentRegularStart": False},
                {"type": "recipient_reenters_before_next_regular_marker", "atMs": 8000},
                {"type": "later_regular_start_after_carried_due", "atMs": 10000},
            ], exposure_protected),
            scenario("SH330-T05", "T05-clipped-at-due-no-catchup", "A clipped recipient intersection at the immutable due time consumes the opportunity; removing the clip before t10 does not replay it before that marker.", exposure_start(), [
                {"type": "enter_initiative", "atMs": 2000},
                {"type": "set_aura_intersection_suppressed_at_due", "atMs": 5900},
                {"type": "resolve_carried_exposure_due", "atMs": 6000, "coincidentRegularStart": False},
                {"type": "recipient_reenters_before_next_regular_marker", "atMs": 8000},
                {"type": "later_regular_start_after_carried_due", "atMs": 10000},
            ], exposure_protected),
            scenario("SH330-T05", "T05-source-ended-at-due", "A source ending before the due marker cannot resolve or revive the pending exposure callback.", exposure_start(), [
                {"type": "enter_initiative", "atMs": 2000},
                {"type": "source_ends_before_due", "atMs": 5000},
                {"type": "resolve_carried_exposure_due", "atMs": 6000, "coincidentRegularStart": False},
                {"type": "later_regular_start_after_carried_due", "atMs": 10000},
            ], exposure_protected),
        ],
    })

    # SH330-T06: local aura-only suppression consumes the recipient marker, not the body.
    local_start = {
        "sourceBody": {"id": avatar_body["id"], "profileId": avatar_body["profileId"], "active": True, "sourceOwnerId": avatar_body["sourceOwner"], "controllerId": avatar_body["controller"], "position": [0, 0, 0], "suppressionIntersection": False},
        "sourceBodyInSuppressionRegion": False, "recipientPosition": [8, 0, 0], "auraRadiusFeet": 10, "recipientWithinAura": True, "recipientInSuppressionRegion": True,
        "suppressionRegion": {"id": "TEST_ONLY:local-field-1", "boundsX": [7, 9]}, "sourceDeadlineMs": 60000,
        "sourceBodyActive": True, "strikeLedger": {"round-21": {"reservedSlots": 3, "attemptedSlots": 1, "consumedSlots": [1], "cancelledSlots": []}},
        "commandEligible": True, "sourceAlive": True, "pulseCount": 0, "consumedDueMarkerIds": [],
    }
    cases.append({
        "testId": "SH330-T06", "id": "SH330-T06-aura-only-suppression", "purpose": "Clip only the recipient's aura intersection; consume the due pulse while preserving an outside Avatar body, its commands and strike ledger; leaving the region does not replay, and source expiry prevents resumption.",
        "scenarios": [
            scenario("SH330-T06", "T06-body-outside-recipient-intersection-clipped", "The exact Avatar body at x0 is outside the conditional field; recipient B at x8 remains within the10ft aura but its local intersection is clipped at t6. Leaving at t8 creates no pulse; the next independent marker t12 resolves.", local_start, [
                {"type": "local_suppressed_due", "atMs": 6000, "markerId": "recipient-B-start-6"},
                {"type": "leave_local_suppression_region", "atMs": 8000},
                {"type": "resolve_local_aura_marker", "atMs": 12000, "markerId": "recipient-B-start-12"},
            ], ["/sourceBody/id", "/sourceBody/profileId", "/sourceBody/active", "/sourceBody/sourceOwnerId", "/sourceBody/controllerId", "/sourceBody/position", "/strikeLedger", "/commandEligible", "/sourceDeadlineMs"]),
            scenario("SH330-T06", "T06-expiry-during-suppression-no-resumption", "The same local clip consumes t6; the original 60-second deadline ends the source before t12, so leaving the field cannot resurrect the body or its aura.", local_start, [
                {"type": "local_suppressed_due", "atMs": 6000, "markerId": "recipient-B-start-6"},
                {"type": "expire_source_at_original_deadline", "atMs": 60000},
                {"type": "leave_local_suppression_region", "atMs": 61000},
                {"type": "resolve_local_aura_marker", "atMs": 62000, "markerId": "recipient-B-start-12"},
            ], ["/sourceBody/id", "/sourceBody/profileId", "/sourceBody/sourceOwnerId", "/sourceBody/controllerId", "/sourceBody/position", "/strikeLedger", "/commandEligible", "/sourceDeadlineMs"]),
        ],
    })
    return cases


def load_preserved_avatar_fork() -> tuple[dict, dict, dict]:
    archive_path = AUDIT / "rank9_summonhosts5_return285_received" / "DD_Rank9_SummonHosts5_Director_Return285_HELD.zip"
    member_name = "cases/RANK9SUMMONHOSTS5129-SUMMON-ELEMENTAL-AVATAR-B.json"
    archive_raw = archive_path.read_bytes()
    with zipfile.ZipFile(archive_path) as archive:
        member_raw = archive.read(member_name)
    case_data = json.loads(member_raw)
    formation_event = case_data["events"][5]
    if formation_event["kind"] != "formation" or formation_event["details"]["profileId"] != "SH202-ELEMENTAL":
        raise AssertionError("Return285 formation event no longer binds the expected Avatar profile")
    full_state = formation_event["after"]
    avatar_body = full_state["bodies"]["A:cast1:body1"]
    actor_b = full_state["actors"]["B"]
    fork = {
        "archivePath": archive_path.relative_to(ROOT).as_posix(),
        "archiveBytes": len(archive_raw),
        "archiveSha256": sha(archive_raw),
        "memberPath": member_name,
        "memberBytes": len(member_raw),
        "memberSha256": sha(member_raw),
        "caseId": case_data["id"],
        "caseStatus": case_data["status"],
        "eventId": formation_event["id"],
        "eventIndexZeroBased": 5,
        "tick": formation_event["after"]["tick"],
        "fullPostEventStateSha256": state_hash(full_state),
        "avatarBodyId": avatar_body["id"],
        "avatarProfileId": avatar_body["profileId"],
        "avatarBodySha256": state_hash(avatar_body),
        "recipientActorId": actor_b["id"],
        "recipientActorProfileId": actor_b["profileId"],
        "recipientActorSha256": state_hash(actor_b),
        "inheritedFixtureStatus": "CONDITIONAL_AUTHORED_FIXTURE_NOT_GAMEPLAY",
    }
    if len(full_state.get("rootLedger", {})) != 0 or len(full_state.get("settlements", [])) != 0:
        raise AssertionError("T02 fork expected the preserved just-formed Avatar with no prior damage settlement")
    return avatar_body, actor_b, fork


def run_cases(cases: list[dict]) -> list[dict]:
    outputs = []
    for case in cases:
        outputs.append({
            "testId": case["testId"],
            "id": case["id"],
            "purpose": case["purpose"],
            "scenarios": [execute_scenario(case["testId"], sc) for sc in case["scenarios"]],
        })
    return outputs


def verify_outputs(cases: list[dict], outputs: list[dict]) -> list[dict]:
    checks = []
    def check(name: str, ok: bool, evidence: object = None) -> None:
        checks.append({"check": name, "passed": bool(ok), "evidence": evidence})
        if not ok:
            raise AssertionError(f"{name}: {evidence}")

    check("exact six SH330 tests with conditional fixtures", [c["testId"] for c in outputs] == [f"SH330-T0{i}" for i in range(1, 7)], [c["testId"] for c in outputs])
    scenario_count = sum(len(c["scenarios"]) for c in outputs)
    transitions = [t for c in outputs for s in c["scenarios"] for t in s["transitions"]]
    check("every scenario has complete start/end states and a full reversible hash chain", all(s["startingStateSha256"] == state_hash(s["startingState"]) and s["finalStateSha256"] == state_hash(s["finalState"]) and s["reversal"]["allTransitionsFullyReversed"] and s["reversal"]["restoredStateSha256"] == s["startingStateSha256"] for c in outputs for s in c["scenarios"]), {"scenarios": scenario_count, "transitions": len(transitions)})
    check("all event before/after hashes and ordered forward/inverse patches agree", all(t["beforeStateSha256"] == state_hash(t["beforeState"]) and t["afterStateSha256"] == state_hash(t["afterState"]) for t in transitions), len(transitions))
    t01 = outputs[0]["scenarios"][0]
    t01results = [t["observedResult"] for t in t01["transitions"]]
    check("T01 canceled reserved slots consume three; extra turn/fourth strike/no-command controls do not reset", t01results[0]["cancelledSlots"] == [2, 3] and t01results[0]["capacityConsumed"] == 3 and t01results[1]["budgetReset"] is False and t01results[2]["accepted"] is False and t01results[3]["commandOrActionGranted"] is False and t01results[4]["accepted"] is False and t01results[5]["accepted"] is False, t01results)
    t02 = outputs[1]["scenarios"]
    composite_6_8 = t02[0]["transitions"][0]["observedResult"]
    composite_11_8 = t02[1]["transitions"][0]["observedResult"]
    overlay = t02[2]["transitions"][0]["observedResult"]
    separate = t02[3]["transitions"]
    check("T02 exact Avatar recipient and fire6/force8 one-root correction resolves once", t02[0]["startingState"]["avatar"]["id"] == "A:cast1:body1" and t02[0]["startingState"]["avatar"]["profileId"] == "SH202-ELEMENTAL" and composite_6_8["totalResolvedOnce"] == 11 and composite_6_8["settlementCountAfter"] == 1 and composite_6_8["hpAfter"] == 186, composite_6_8)
    check("T02 SH330 fire11/force8 requirement and tempHP/HP settlement pass", composite_11_8["totalResolvedOnce"] == 13 and overlay["resolvedComponents"][0]["resolvedAmount"] == 5 and overlay["resolvedComponents"][1]["resolvedAmount"] == 8 and overlay["hpAfter"] == 20 and overlay["tempHPAfter"] == 0 and overlay["settlementCountAfter"] == 1, {"fire11_force8": composite_11_8, "tempHP_overlay": overlay})
    check("T02 distinct roots remain ordered with two settlements", separate[0]["observedResult"]["rootId"] != separate[1]["observedResult"]["rootId"] and separate[0]["observedResult"]["totalResolvedOnce"] == 3 and separate[1]["observedResult"]["totalResolvedOnce"] == 8 and separate[1]["observedResult"]["settlementCountAfter"] == 2 and separate[1]["observedResult"]["hpAfter"] == 22, [x["observedResult"] for x in separate])
    t03 = outputs[2]["scenarios"]
    first_transition = t03[0]["transitions"][0]["observedResult"]
    later_order = next(t["observedResult"] for t in t03[0]["transitions"] if t["event"]["type"] == "issue_new_controller_order")
    owner_phase = next(t["observedResult"] for t in t03[0]["transitions"] if t["event"]["type"] == "execute_at_original_owner_attached_phase")
    second_strike = t03[1]["transitions"][0]["observedResult"]
    check("T03 Return331 reservedSlots3/attempts2 cancellation consumes third slot without refund", first_transition["cancelledSlots"] == [3] and first_transition["capacityConsumed"] == 3 and first_transition["thirdStrikeAccepted"] is False and first_transition["fourthStrikeAccepted"] is False and first_transition["refund"] == 0, first_transition)
    check("T03 later command requires and uses a lawful actual turn, allowance, and original owner phase", later_order["accepted"] is True and all(later_order["checks"].values()) and owner_phase["executed"] is True and owner_phase["phaseOwner"] == "owner-A" and owner_phase["attackActionReservedSlots"] == 3, {"order": later_order, "execution": owner_phase})
    check("T03 exhausted post-spend controller change cannot create fourth strike", second_strike["capacityConsumed"] == 3 and second_strike["strikeCapReset"] is False and t03[1]["transitions"][1]["observedResult"]["accepted"] is False, second_strike)
    t04 = outputs[3]["scenarios"]
    winners = [s["transitions"][0]["observedResult"]["winner"]["sourceId"] for s in t04]
    check("T04 max pool and deterministic tie rules select only the correct source", winners == ["avatar-B-test-only", "avatar-A", "avatar-A", "avatar-A"], winners)
    check("T04 one packet only, source metadata bound, due opportunities consumed, no replay", all(s["transitions"][0]["observedResult"]["packetsApplied"] == 1 and s["transitions"][0]["observedResult"]["losingOrSuppressedOpportunitiesConsumed"] and (len(s["transitions"]) < 2 or s["transitions"][1]["observedResult"]["priorLosingOrSuppressedPacketReplayed"] is False) for s in t04), [s["transitions"][0]["observedResult"] for s in t04])
    t05 = outputs[4]["scenarios"]
    standard = t05[0]["transitions"]
    due = standard[2]["observedResult"]
    check("T05 initiative entry preserves due6; early start is empty; coincident due/start resolves exactly once", standard[0]["observedResult"]["existingNextDueMs"] == 6000 and standard[1]["observedResult"]["auraPulse"] is False and due["pulse"] is True and due["coalescedCoincidentRegularStart"] is True and due["pulseCountAfter"] == 1, due)
    check("T05 later actual markers and outside/clipped/dead-source branches have no catchup", standard[3]["observedResult"]["pulseCountAfter"] == 2 and standard[4]["observedResult"]["pulseCountAfter"] == 3 and all(not x["transitions"][2]["observedResult"]["pulse"] for x in t05[1:]) and t05[3]["transitions"][3]["observedResult"]["pulse"] is False, [s["transitions"][-1]["observedResult"] for s in t05])
    t06 = outputs[5]["scenarios"]
    local_due = t06[0]["transitions"][0]["observedResult"]
    check("T06 source body is outside local field; only due aura intersection is clipped and consumed", local_due["bodyPersists"] is True and local_due["bodySuppressed"] is False and local_due["dueOpportunityConsumed"] is True and t06[0]["startingState"]["sourceBody"]["position"] == [0, 0, 0] and t06[0]["startingState"]["recipientPosition"] == [8, 0, 0], local_due)
    check("T06 leaving local field does not replay; next independent marker resumes only before original expiry", t06[0]["transitions"][1]["observedResult"]["pulseOnLeaving"] is False and t06[0]["transitions"][2]["observedResult"]["pulse"] is True and t06[1]["transitions"][3]["observedResult"]["pulse"] is False, [s["transitions"][-1]["observedResult"] for s in t06])
    check("no real acquisition, gameplay occurrence, runtime execution, or application is claimed", True, {"fixtureType": "TEST_ONLY_CONDITIONAL_INPUT", "runtimeExecuted": False, "applicationAuthorized": False})
    return checks


def build_queue_revision(queue345: dict, handoff345: dict, audit345: dict, package_path: str) -> tuple[dict, dict, dict]:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    queue = copy.deepcopy(queue345)
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_348.json"
    handoff_path = AUDIT / "CURRENT_HANDOFF_348.json"
    audit_path = AUDIT / "CURRENT23_PENDING_IDENTITY_AUDIT_348.json"
    queue["id"] = "SPELL-REVIEW-QUEUE-348"
    queue["recordedAtUtc"] = timestamp
    queue["supersedesQueue"] = binding(AUDIT / "CURRENT_SPELL_QUEUE_345.json")
    queue["timeStopDisposition"]["linkedPendingComparisonId"] = None
    queue["timeStopDisposition"]["linkedPendingBlockerIds"] = []
    queue["timeStopDisposition"]["linkedHistoricalComparisonId"] = "timeless-form"
    queue["timeStopDisposition"]["linkedHistoricalBlockerIds"] = ["DF218-B03"]
    queue["timeStopDisposition"]["linkedHistoricalDisposition"] = "SEALED_ACCEPT_APPLIED_CLOSURE346"
    queue["timeStopDisposition"]["linkClassification"] = "HISTORICAL_CLOSED_NOT_PENDING"
    queue["activeReview"] = {"spellId": SPELL, "blockerIds": [BLOCKER], "packet": package_path, "status": "DIRECTOR_AUTHORIZED_SH330_CORRECTION_DELTA_IN_PROGRESS"}
    queue["next"] = f"{SPELL} / {BLOCKER}"
    queue["nextActionablePriority"] = {"identity": SPELL, "blockerIds": [BLOCKER], "reason": "Director found no qualifying new Fate Rewrite evidence; existing SH330 contract authorizes this correction delta."}
    queue["currentCorrectionIds"] = ["SH331-C01", "SH331-C02", "SH331-C03"]
    queue["currentPacketStatus"] = "DIRECTOR_RETURN_CONFIRMED_SH202_B01_SIX_TEST_DELTA_REQUIRED; NO_NEW_ACCEPTANCE_OR_APPLICATION"
    queue["currentDirectorInstruction"] = "Fate Rewrite / TF192-B04 remains open with TF192-B02 retained; no qualifying new evidence was found. Next actionable work is Summon Elemental Avatar / SH202-B01: complete SH330-T01 through T06 and reclassify the stale Timeless Form link as historical/closed."
    queue["correctionAuthority"] = {"acceptedIds": [], "appliedIds": [], "applicationAuthorizedIds": [], "heldIds": [SPELL], "blockerIds": [BLOCKER], "canonicalFilesChanged": False, "runtimeExecuted": False}
    queue["pendingIdentityAudit"] = audit_path.relative_to(ROOT).as_posix()
    queue["currentPendingIdentityAudit"] = queue["pendingIdentityAudit"]
    queue["currentHandoff"] = handoff_path.relative_to(ROOT).as_posix()
    queue["currentPacket"] = package_path
    queue["currentPacketSubmission"] = None

    pending = copy.deepcopy(audit345)
    pending["id"] = "SPELL-REVIEW-CURRENT23-PENDING-IDENTITY-AUDIT-348"
    pending["recordedAtUtc"] = timestamp
    pending["supersedes"] = binding(AUDIT / "CURRENT23_PENDING_IDENTITY_AUDIT_345.json")
    pending["status"] = "PASS_CURRENT_825_23_SH202_B01_CORRECTION_DELTA_PREPARED"
    pending["sourceQueue"] = queue_path.relative_to(ROOT).as_posix()
    pending["nextStep"] = "Fate Rewrite / TF192-B04 remains open with TF192-B02 retained; no qualifying new evidence was found. Next actionable work is Summon Elemental Avatar / SH202-B01: complete SH330-T01 through T06 under the sealed SH330 contract. No identity has been accepted or applied by this packet."
    pending["nextIdentity"] = SPELL
    pending["nextBlockerIds"] = [BLOCKER]
    pending["currentPacketStatus"] = queue["currentPacketStatus"]
    pending["currentHandoff"] = handoff_path.relative_to(ROOT).as_posix()
    pending["currentReturnAcceptedIds"] = ["timeless-form"]
    pending["currentReturnAppliedIds"] = ["timeless-form"]
    pending["currentReturnHeldIds"] = []
    pending["canonicalFilesChanged"] = False
    pending["applicationPerformed"] = False
    pending["closedBlockerIdsThisStep"] = []
    pending["heldThisStep"] = [SPELL]
    pending["currentCorrectionIds"] = ["SH331-C01", "SH331-C02", "SH331-C03"]
    queue_raw = pretty(queue)
    queue_path.write_bytes(queue_raw)
    pending["currentQueueBinding"] = binding(queue_path)

    handoff = copy.deepcopy(handoff345)
    handoff["id"] = "SPELL-REVIEW-CURRENT-HANDOFF-348"
    handoff["recordedAtUtc"] = timestamp
    handoff["supersedes"] = binding(AUDIT / "CURRENT_HANDOFF_345.json")
    handoff["status"] = "SH202_B01_CORRECTION_DELTA_348_PREPARED"
    handoff["scopeIds"] = [SPELL]
    handoff["blockerIds"] = [BLOCKER]
    handoff["queue"] = queue_path.relative_to(ROOT).as_posix()
    handoff["queueBinding"] = binding(queue_path)
    handoff["pendingIdentityAudit"] = audit_path.relative_to(ROOT).as_posix()
    handoff["authority"] = AUTHORITY
    handoff["currentAuthority"] = AUTHORITY
    handoff["pendingIdentityAuditBinding"] = {"path": audit_path.relative_to(ROOT).as_posix(), "bytes": len(pretty(pending)), "sha256": sha(pretty(pending)), "crc32": crc(pretty(pending))}
    handoff["closureTasksRemaining"] = 23
    handoff["firstReviewTasksRemaining"] = 0
    handoff["nextPendingGroup"] = None
    handoff["nextStep"] = pending["nextStep"]
    handoff["currentPacketStatus"] = queue["currentPacketStatus"]
    handoff["directorConnectionStatus"] = "GPT confirmed no qualifying Fate Rewrite evidence and named SH202-B01 with SH331-C01/C02/C03 exact residuals; no identity accepted or applied."
    handoff["currentDirectorInstruction"] = queue["currentDirectorInstruction"]
    handoff["currentReview"] = {"spellId": SPELL, "blockerIds": [BLOCKER], "contractId": "SH330-LOCAL-CLOSURE-CONTRACT-01", "testIds": [f"SH330-T0{i}" for i in range(1, 7)]}
    handoff["canonicalFilesChanged"] = False
    handoff["applicationPerformed"] = False
    handoff["runtimeExecuted"] = False
    handoff["acceptedIds"] = []
    handoff["appliedIds"] = []
    handoff["currentPacketSubmission"] = None
    audit_path.write_bytes(pretty(pending))
    handoff_path.write_bytes(pretty(handoff))
    for source in (queue_path, handoff_path, audit_path):
        (OUT / source.name).write_bytes(source.read_bytes())
    return queue, handoff, pending


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    names = {
        "queue": AUDIT / "CURRENT_SPELL_QUEUE_345.json",
        "handoff": AUDIT / "CURRENT_HANDOFF_345.json",
        "pending": AUDIT / "CURRENT23_PENDING_IDENTITY_AUDIT_345.json",
        "contract": AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "director_context" / "SH330_LOCAL_CLOSURE_CONTRACT.md",
        "findings": AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "EXACT_REMAINING_FINDINGS.json",
        "returnDecision": AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "DIRECTOR_DECISION.json",
        "returnDelivery": AUDIT / "rank9_summon_elemental_avatar_return331_received" / "DD_SummonElementalAvatar_Director_Return331_HELD_DELIVERY.json",
        "returnArchive": AUDIT / "rank9_summon_elemental_avatar_return331_received" / "DD_SummonElementalAvatar_Director_Return331_HELD.zip",
        "index": ROOT / "DescentReviewChanges" / "ReviewBible" / "data" / "public" / "spell_playtests" / "authored_review_index.json",
        "catalog": ROOT / "DescentReviewChanges" / "ReviewBible" / "data" / "public" / "spell_playtests" / "catalog.json",
    }
    source_queue = json.loads(names["queue"].read_text(encoding="utf-8"))
    source_handoff = json.loads(names["handoff"].read_text(encoding="utf-8"))
    source_pending = json.loads(names["pending"].read_text(encoding="utf-8"))
    if source_queue["currentAuthority"] != AUTHORITY or source_pending["authority"] != AUTHORITY:
        raise AssertionError("current authority changed; rebuild only after reconciling the current queue")
    if source_pending["pendingCount"] != 23 or SPELL not in source_pending["pendingIds"]:
        raise AssertionError("Summon Elemental Avatar must remain one of the current 23 pending identities")

    contract_binding = source_queue["currentReturnBlockers"][SPELL]
    if contract_binding != [BLOCKER]:
        raise AssertionError("current queue blocker changed")
    contract_record = json.loads(names["returnDelivery"].read_text(encoding="utf-8"))
    contract_copy = names["contract"].read_bytes()
    contract_hash = sha(contract_copy)
    contract_anchor = json.loads((AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "DIRECTOR_CONTRACT_BINDING.json").read_text(encoding="utf-8"))
    if contract_hash != contract_anchor["fileBinding"]["sha256"]:
        raise AssertionError("Return331's SH330 contract binding does not match its exact bytes")

    avatar_body, actor_b, preserved_fork = load_preserved_avatar_fork()
    cases = build_cases(avatar_body, actor_b, preserved_fork)
    outputs = run_cases(cases)
    checks = verify_outputs(cases, outputs)

    package_path = (OUT / "DD_Rank9_SummonElementalAvatar_SH202B01_Closure348.zip").relative_to(ROOT).as_posix()
    queue, handoff, pending = build_queue_revision(source_queue, source_handoff, source_pending, package_path)
    # Rebind handoff to the exact written pending-audit bytes after queue/hash construction.
    handoff["pendingIdentityAuditBinding"] = binding(AUDIT / "CURRENT23_PENDING_IDENTITY_AUDIT_348.json")
    (AUDIT / "CURRENT_HANDOFF_348.json").write_bytes(pretty(handoff))
    (OUT / "CURRENT_HANDOFF_348.json").write_bytes(pretty(handoff))

    current_bindings = {key: binding(path) for key, path in names.items() if key in {"queue", "handoff", "pending", "index", "catalog", "returnDecision", "returnDelivery", "returnArchive"}}
    current_bindings["sh330Contract"] = {"path": names["contract"].relative_to(ROOT).as_posix(), "bytes": len(contract_copy), "sha256": contract_hash, "crc32": crc(contract_copy)}
    current_bindings["return331Findings"] = binding(names["findings"])
    corrected_queue_bindings = {
        "queue348": binding(AUDIT / "CURRENT_SPELL_QUEUE_348.json"),
        "handoff348": binding(AUDIT / "CURRENT_HANDOFF_348.json"),
        "pendingAudit348": binding(AUDIT / "CURRENT23_PENDING_IDENTITY_AUDIT_348.json"),
    }
    delta = {
        "id": "SH202-B01-SH330-CONDITIONAL-TRANSITION-DELTA-348",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "SIX_SH330_TESTS_EXECUTED_AS_CONDITIONAL_REVERSIBLE_TRANSITIONS_READY_FOR_DIRECTOR_REVIEW",
        "scopeIds": [SPELL], "blockerIds": [BLOCKER],
        "authorityBefore": AUTHORITY, "authorityAfter": AUTHORITY,
        "acceptedIds": [], "appliedIds": [], "applicationAuthorizedIds": [], "heldIds": [SPELL],
        "directorRuling": {
            "responseCommit": "9470c60ba768220bd38fb758f6f89d877933e594",
            "nextActionablePriority": "Produce the Summon Elemental Avatar / SH202-B01 correction delta under SH330-LOCAL-CLOSURE-CONTRACT-01.",
            "exactFindings": ["SH331-C01", "SH331-C02", "SH331-C03"],
            "noNewAcceptanceOrApplication": True,
            "noAdditionalPermissionOrSourceSearchRequired": True,
            "preserveAllOtherDispositions": True,
        },
        "contractBinding": contract_anchor,
        "currentAuthorityBindingsBeforeCorrection": current_bindings,
        "currentAuthorityBindingsAfterCorrection": corrected_queue_bindings,
        "queueMetadataCorrection": {
            "sourceQueue": current_bindings["queue"],
            "fieldBefore": {"linkedPendingComparisonId": "timeless-form", "linkedPendingBlockerIds": ["DF218-B03"]},
            "fieldAfter": {"linkedPendingComparisonId": None, "linkedPendingBlockerIds": [], "linkedHistoricalComparisonId": "timeless-form", "linkedHistoricalBlockerIds": ["DF218-B03"], "linkedHistoricalDisposition": "SEALED_ACCEPT_APPLIED_CLOSURE346", "linkClassification": "HISTORICAL_CLOSED_NOT_PENDING"},
            "correctedQueueBinding": corrected_queue_bindings["queue348"],
            "acceptedOrAppliedSetChanged": False,
        },
        "preservedSourceFork": preserved_fork,
        "testSpecification": {
            "fixtureStatus": "TEST_ONLY_CONDITIONAL_INPUT",
            "gameplayOccurrenceClaim": False,
            "runtimeExecuted": False,
            "unrelatedPriorCasesFreshlyReplayed": False,
            "retainedQualifications": ["SH202-H01", "SH202-H02", "SH202-H03", "SH202-H04", "SH202-H05", "SH202-H06", "SH202-H07", "SH202-H08", "SH202-H09", "SH202-H10", "SH202-H11", "SH202-H12", "SH330-Q-EXTERNAL-INPUTS", "SH330-Q-TEST-PROVENANCE"],
            "testIds": [f"SH330-T0{i}" for i in range(1, 7)],
            "scenarioCount": sum(len(c["scenarios"]) for c in outputs),
        },
        "cases": outputs,
        "verification": {"checkCount": len(checks), "passedChecks": sum(c["passed"] for c in checks), "failedChecks": sum(not c["passed"] for c in checks), "status": "PASS" if all(c["passed"] for c in checks) else "FAIL"},
        "provenance": {"conditionalFixturesAreGameplay": False, "userAuthorshipClaim": False, "canonicalMutation": False, "runtimeExecuted": False, "identityAccepted": False, "applicationPerformed": False},
        "requestedDisposition": "Review only summon-elemental-avatar / SH202-B01. If the six reversible transitions and preserved source bindings close SH331-C01 through C03 under SH330, issue an exact sealed one-identity acceptance and application authorization. Otherwise identify only the failed test and minimum correction. Preserve all other identities, all 14 retained qualifications, the 23-pending authority count, and disabled runtime/downstream gates.",
    }
    delta_path = OUT / "SH202_B01_SH330_CONDITIONAL_TRANSITION_DELTA_348.json"
    delta_path.write_bytes(pretty(delta))
    checks_path = OUT / "SH202_B01_SH330_INDEPENDENT_TRANSITION_AUDIT_348.json"
    verifier_path = AUDIT / "verify_summon_elemental_avatar_closure348.py"
    replay_report_path = OUT / "SH202_B01_SH330_REPLAY_VERIFICATION_348.json"
    subprocess.run([sys.executable, str(verifier_path)], cwd=ROOT, check=True, capture_output=True, text=True)
    independent_replay = json.loads(replay_report_path.read_text(encoding="utf-8"))
    if independent_replay["status"] != "PASS":
        raise AssertionError("independent replay verification did not pass")
    combined_checks = checks + independent_replay["checks"]
    audit_record = {
        "id": "SH202-B01-SH330-INDEPENDENT-TRANSITION-AUDIT-348",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS" if all(c["passed"] for c in combined_checks) else "FAIL",
        "checks": checks,
        "checkCount": len(checks), "passedChecks": sum(c["passed"] for c in checks), "failedChecks": sum(not c["passed"] for c in checks),
        "scenarioCount": sum(len(c["scenarios"]) for c in outputs),
        "transitionCount": sum(len(s["transitions"]) for c in outputs for s in c["scenarios"]),
        "fullInverseTraversals": sum(s["reversal"]["allTransitionsFullyReversed"] for c in outputs for s in c["scenarios"]),
        "independentReplayVerification": {"path": replay_report_path.name, "status": independent_replay["status"], "checkCount": independent_replay["checkCount"], "passedChecks": independent_replay["passedChecks"], "sha256": sha(replay_report_path.read_bytes())},
        "acceptedIds": [], "appliedIds": [], "applicationAuthorizedIds": [], "blockerIds": [BLOCKER],
        "authority": AUTHORITY, "runtimeExecuted": False, "canonicalFilesChanged": False,
    }
    checks_path.write_bytes(pretty(audit_record))

    request_text = (
        "Director: review only Summon Elemental Avatar / SH202-B01. This is the SH330-LOCAL-CLOSURE-CONTRACT-01 correction delta, bound to the current 825/23 authority and Return331's exact SH331-C01/C02/C03 findings. It executes SH330-T01 through T06 as TEST_ONLY_CONDITIONAL_INPUT transitions with exact start/end projections, ordered patches, state hashes, full inverse traversals and unchanged-path assertions. T02 binds the actual Return285 Avatar recipient A:cast1:body1 / SH202-ELEMENTAL, resolves a single fire6+force8 composite root to11 once, preserves two different roots as two ordered settlements, and separately demonstrates fire11+force8 -> 13 with HP30/tempHP3 -> HP20/tempHP0. The existing Return285 casebook/profile and all prior passing evidence remain byte-preserved. Queue348 reclassifies Timeless Form/DF218-B03 as historical/closed, not pending. No source acquisition, campaign occurrence, runtime execution, acceptance, application, canon promotion or downstream approval is claimed. Please return an exact sealed disposition for this identity only; preserve every other hold and qualification."
    )
    request_path = OUT / "SH202_B01_SH330_CLOSURE348_DIRECTOR_REQUEST.md"
    request_path.write_text(request_text, encoding="utf-8", newline="\n")

    payload_files = [
        delta_path,
        checks_path,
        OUT / "CURRENT_SPELL_QUEUE_348.json",
        OUT / "CURRENT_HANDOFF_348.json",
        OUT / "CURRENT23_PENDING_IDENTITY_AUDIT_348.json",
        request_path,
        verifier_path,
        replay_report_path,
        names["contract"],
        names["findings"],
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "DIRECTOR_CONTRACT_BINDING.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "DIRECTOR_DECISION.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "CASE_RESULTS.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "input" / "SH202_B01_CORRECTION_DELTA_329.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "input" / "SH202_B01_CORRECTION_AUDIT_329.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "input" / "verify_sh202_b01_correction_329.py",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "input" / "CURRENT25_PENDING_IDENTITY_AUDIT_329.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "input" / "CURRENT_SPELL_QUEUE_329.json",
        AUDIT / "rank9_summon_elemental_avatar_return331_received" / "payload" / "input" / "CURRENT_HANDOFF_329.json",
        names["returnDelivery"],
        names["returnArchive"],
    ]
    archive_path = OUT / "DD_Rank9_SummonElementalAvatar_SH202B01_Closure348.zip"
    member_bindings = []
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in payload_files:
            raw = path.read_bytes()
            name = path.name if path.parent != OUT else path.name
            archive.writestr(name, raw)
            member_bindings.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
    archive_raw = archive_path.read_bytes()
    delivery = {
        "id": "SH202-B01-SH330-CLOSURE348-DELIVERY",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PREPARED_READBACK_PASS_FOR_DIRECTOR_REVIEW",
        "scopeIds": [SPELL], "blockerIds": [BLOCKER], "authority": AUTHORITY,
        "acceptedIds": [], "appliedIds": [], "applicationAuthorizedIds": [], "heldIds": [SPELL],
        "archive": {"fileName": archive_path.name, "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)},
        "memberCount": len(member_bindings), "memberBindings": member_bindings,
        "mirroredSidecars": [binding(path) for path in [delta_path, checks_path, request_path, OUT / "CURRENT_SPELL_QUEUE_348.json", OUT / "CURRENT_HANDOFF_348.json", OUT / "CURRENT23_PENDING_IDENTITY_AUDIT_348.json"]],
        "contractId": "SH330-LOCAL-CLOSURE-CONTRACT-01",
        "findingIds": ["SH331-C01", "SH331-C02", "SH331-C03"],
        "testIds": [f"SH330-T0{i}" for i in range(1, 7)],
        "scenarioCount": sum(len(c["scenarios"]) for c in outputs),
        "transitionCount": sum(len(s["transitions"]) for c in outputs for s in c["scenarios"]),
        "audit": {"status": audit_record["status"], "generatorChecksPassed": audit_record["passedChecks"], "generatorCheckCount": audit_record["checkCount"], "independentReplayStatus": independent_replay["status"], "independentReplayChecksPassed": independent_replay["passedChecks"], "independentReplayCheckCount": independent_replay["checkCount"]},
        "provenance": delta["provenance"],
    }
    delivery_path = OUT / "DD_Rank9_SummonElementalAvatar_SH202B01_Closure348_DELIVERY.json"
    delivery_path.write_bytes(pretty(delivery))

    # Read back every archive member and every byte-bound mirror before finalizing.
    with zipfile.ZipFile(archive_path) as archive:
        for member in member_bindings:
            raw = archive.read(member["path"])
            if len(raw) != member["bytes"] or sha(raw) != member["sha256"] or crc(raw) != member["crc32"]:
                raise AssertionError(f"archive member mismatch: {member['path']}")
            if member["path"] in {p.name for p in payload_files if p.parent == OUT}:
                mirror = OUT / member["path"]
                if mirror.read_bytes() != raw:
                    raise AssertionError(f"archive mirror mismatch: {member['path']}")
    if audit_record["status"] != "PASS":
        raise AssertionError("independent transition audit failed")

    print(json.dumps({
        "status": "PASS",
        "archive": archive_path.relative_to(ROOT).as_posix(),
        "archiveBytes": len(archive_raw),
        "archiveSha256": sha(archive_raw),
        "audit": audit_record["status"],
        "checks": {"generator": audit_record["passedChecks"], "independentReplay": independent_replay["passedChecks"]},
        "scenarios": audit_record["scenarioCount"],
        "transitions": audit_record["transitionCount"],
        "queueMetadataCorrected": queue["timeStopDisposition"]["linkClassification"],
        "authority": AUTHORITY,
    }, indent=2))


if __name__ == "__main__":
    main()
