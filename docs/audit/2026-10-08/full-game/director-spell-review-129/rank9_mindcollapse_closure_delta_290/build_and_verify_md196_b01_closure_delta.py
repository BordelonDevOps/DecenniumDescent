#!/usr/bin/env python3
"""Build and verify the Director-authorized MD196-B01 closure delta.

Data-only audit helper. Reads the bound packet and source files; does not execute game
or authoring programs, alter canonical spell records, or apply acceptance.
Run from the repository root: python <this-file>.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path.cwd()
OUT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_mindcollapse_closure_delta_290"
PACKET = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196"
CASEBOOK = PACKET / "CASEBOOK.json.gz"
CASE_INDEX = PACKET / "CASE_INDEX.json"
PROCEDURE = PACKET / "procedures/mind-collapse.json"
ACTOR_PROFILES = PACKET / "ACTOR_PROFILES.json"
WIZARD_SOURCE = ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json"
COMBAT_SOURCE = ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md"
CATALOG_SOURCE = ROOT / "DescentReviewChanges/ReviewBible/src/data/spells.js"
RULEBOOK_SOURCE = ROOT / "docs/reference/Player_Rulebook_v6_source_text.txt"
COMMON_PROCEDURE = PACKET / "COMMON_PROCEDURE.json"
BASE_CASE_ID = "RANK9MEMORYDENIAL6129-MIND-COLLAPSE-B/extra-action-not-turn"
CLOSURE_CASE_ID = "RANK9MEMORYDENIAL6129-MIND-COLLAPSE-B/MD290-closure-extra-turn-boundary"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_json(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def walk_ids(value: Any, wanted: set[str]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    def visit(item: Any) -> None:
        if isinstance(item, dict):
            if item.get("id") in wanted:
                found.append(copy.deepcopy(item))
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)
    visit(value)
    return found


def json_pointer(path: str) -> list[str]:
    if path == "":
        return []
    return [part.replace("~1", "/").replace("~0", "~") for part in path.lstrip("/").split("/")]


def get_parent(root: Any, path: str) -> tuple[Any, str]:
    parts = json_pointer(path)
    if not parts:
        return None, ""
    parent = root
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


def apply_ops(state: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in operations:
        name, path = op["op"], op["path"]
        if path == "":
            if name not in ("replace", "add"):
                raise ValueError(f"unsupported root operation {name}")
            result = copy.deepcopy(op["value"])
            continue
        parent, key = get_parent(result, path)
        if name in ("add", "replace"):
            value = copy.deepcopy(op["value"])
            if isinstance(parent, list):
                if name == "add" and key == "-":
                    parent.append(value)
                elif name == "add":
                    parent.insert(int(key), value)
                else:
                    parent[int(key)] = value
            else:
                parent[key] = value
        elif name == "remove":
            if isinstance(parent, list):
                del parent[int(key)]
            else:
                del parent[key]
        else:
            raise ValueError(f"unsupported operation {name}")
    return result


def make_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        ops: list[dict[str, Any]] = []
        for key in sorted(before.keys() - after.keys()):
            escaped = key.replace("~", "~0").replace("/", "~1")
            ops.append({"op": "remove", "path": f"{path}/{escaped}"})
        for key in sorted(after.keys() - before.keys()):
            escaped = key.replace("~", "~0").replace("/", "~1")
            # Patch records must own their payloads. Without this copy, a later
            # event mutating an appended history/list can silently rewrite every
            # earlier event's forward and inverse patch in memory.
            ops.append({"op": "add", "path": f"{path}/{escaped}", "value": copy.deepcopy(after[key])})
        for key in sorted(before.keys() & after.keys()):
            escaped = key.replace("~", "~0").replace("/", "~1")
            ops.extend(make_diff(before[key], after[key], f"{path}/{escaped}"))
        return ops
    return [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]


def pointer_record(path: Path, root: Path = ROOT) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def relevant_knowledge(actor_state: dict[str, Any]) -> dict[str, Any]:
    knowledge = actor_state["knowledge"]
    target_ids = {"mind-collapse", "wizard.base.arcane-bolt", "wizard.base.counterspell"}
    return {
        "knowledgeSha256": sha_json(knowledge),
        "classSpells": [x for x in knowledge.get("classSpells", []) if x in target_ids],
        "bookIds": [x for x in knowledge.get("bookIds", []) if x == "mind-collapse"],
        "preparedIds": [x for x in knowledge.get("preparedIds", []) if x == "mind-collapse"],
        "everKnownRelevant": {k: v for k, v in knowledge.get("everKnown", {}).items() if k in target_ids},
        "temporaryGrants": [x for x in knowledge.get("temporaryGrants", []) if x in target_ids],
    }


def initial_actor(name: str, actor_state: dict[str, Any], profile: dict[str, Any], profile_file_sha: str) -> dict[str, Any]:
    return {
        "id": name,
        "profileId": actor_state["profile"],
        "profileSnapshotSha256": actor_state["profileSHA256"],
        "profilePointer": "/Wizard20",
        "profileFileSha256": profile_file_sha,
        "profileQualification": {
            "class": profile["class"], "classLevel": profile["classLevel"], "school": profile.get("school"),
            "castingAbility": profile.get("castingAbility"), "spellDC": profile.get("spellDC"), "PB": profile.get("PB"),
            "M": profile.get("M"), "campaignExistenceVerified": profile.get("campaignExistenceVerified"),
        },
        "sourceActorStateSha256": sha_json(actor_state),
        "position": copy.deepcopy(actor_state["position"]),
        "body": {k: copy.deepcopy(actor_state["body"].get(k)) for k in ["hands", "voice", "living", "ordinarySight", "ordinaryHearing", "support"]},
        "equipment": copy.deepcopy(actor_state["equipment"]),
        "acquisitionEvidence": relevant_knowledge(actor_state),
        "classCapabilityProjection": copy.deepcopy(actor_state.get("classCapabilityProjection")),
        "resources": {
            "RP": actor_state["RP"], "maximumRP": actor_state["maximumRP"],
            "Dissonance": actor_state["Dissonance"], "DissonanceLimit": actor_state["limit"],
            "Refrain": actor_state["refrain"], "budget": copy.deepcopy(actor_state["budget"]),
            "recharge": copy.deepcopy(actor_state["recharge"]), "ready": copy.deepcopy(actor_state["ready"]),
            "concentration": copy.deepcopy(actor_state["concentration"]),
            "preparedFamiliesCast": copy.deepcopy(actor_state["preparedFamiliesCast"]),
            "resourceHistory": copy.deepcopy(actor_state["resourceHistory"]), "lastSpell": actor_state["lastSpell"],
        },
        "clock": copy.deepcopy(actor_state["clock"]),
        "conditions": copy.deepcopy(actor_state["conditions"]),
        "availability": copy.deepcopy(actor_state["availability"]),
        "saveHistory": copy.deepcopy(actor_state["saveHistory"]),
        "readyHistory": [],
        "rechargeHistory": [],
    }


def add_family(actor: dict[str, Any], spell_id: str) -> bool:
    families = actor["resources"]["preparedFamiliesCast"]
    if spell_id in families:
        return False
    families.append(spell_id)
    return True


def base_event_ref(event: dict[str, Any]) -> dict[str, Any]:
    return {"id": event["id"], "timeMs": event["timeMs"], "kind": event["kind"],
            "beforeSHA256": event["beforeSHA256"], "afterSHA256": event["afterSHA256"]}


def class_source_evidence(profile: dict[str, Any], actor_state: dict[str, Any], wizard: dict[str, Any]) -> dict[str, Any]:
    return {
        "arcaneBoltProfileRecord": walk_ids(profile.get("acquisitionLedger", []), {"wizard.base.arcane-bolt"}),
        "counterspellProfileRecord": walk_ids(profile.get("acquisitionLedger", []), {"wizard.base.counterspell"}),
        "arcaneBoltClassCard": copy.deepcopy(wizard["cards"][5]),
        "counterspellClassCard": copy.deepcopy(wizard["cards"][17]),
        "classFamilyRules": {"firstDistinctFamily": copy.deepcopy(wizard["engine"][11]), "matrixAccounting": copy.deepcopy(wizard["engine"][12])},
        "actorKnowledge": relevant_knowledge(actor_state),
    }


def set_budget_from_base(actor: dict[str, Any], base_after_actor: dict[str, Any]) -> None:
    actor["resources"]["budget"] = copy.deepcopy(base_after_actor["budget"])
    actor["clock"] = copy.deepcopy(base_after_actor["clock"])
    actor["availability"] = copy.deepcopy(base_after_actor["availability"])


def mutate_for_spec(state: dict[str, Any], spec: dict[str, Any], base_event: dict[str, Any] | None) -> None:
    t = spec["timeMs"]
    state["timeMs"] = t
    kind = spec["kind"]
    if kind.startswith("regular-start:"):
        actor_id = kind.split(":", 1)[1]
        actor = state["actors"][actor_id]
        state["regularMarkers"][actor_id]["starts"].append(t)
        if base_event:
            set_budget_from_base(actor, base_event["after"]["actors"][actor_id])
        if actor_id == "T" and t >= 7100:
            key = "wizard.base.counterspell"
            old = actor["resources"]["recharge"].get(key, 0)
            new = max(0, old - 1)
            actor["resources"]["recharge"][key] = new
            actor["rechargeHistory"].append({"atMs": t, "source": "T regular START", "ability": key, "before": old, "after": new})
            if t == 7100:
                actor["readyHistory"].append({"atMs": t, "scheduledExpiry": 7100,
                    "result": "no-op; Ready already terminated at 6205", "refund": False, "revived": False})
    elif kind.startswith("regular-end:"):
        actor_id = kind.split(":", 1)[1]
        actor = state["actors"][actor_id]
        state["regularMarkers"][actor_id]["ends"].append(t)
        if base_event:
            cast_this_turn = actor["clock"].get("magicThisTurn", False)
            actor["clock"] = copy.deepcopy(base_event["after"]["actors"][actor_id]["clock"])
            # Regular END records the boundary without erasing a paid cast
            # already made during that regular turn. The next START resets it.
            actor["clock"]["magicThisTurn"] = cast_this_turn
        if actor_id == "T" and t in (7900, 13900, 19900) and state["mindCollapse"]["status"] == "active":
            save = {"atMs": t, "stat": "INT", "die": 2, "modifierPlusProficiency": 11, "total": 13, "DC": 19,
                    "passed": False, "marker": "future regular target END", "beforePhase20Expiry": True}
            actor["saveHistory"].append(copy.deepcopy(save))
            state["mindCollapse"]["repeatSaves"].append(copy.deepcopy(save))
    elif kind == "ready-arcane-bolt":
        actor = state["actors"]["T"]
        if actor["resources"]["budget"]["Action"] != 1 or actor["resources"]["RP"] != 80:
            raise ValueError("T is not eligible for the authored Ready setup")
        actor["resources"]["budget"]["Action"] = 0
        actor["resources"]["RP"] = 79
        actor["resources"]["lastSpell"] = "wizard.base.arcane-bolt"
        first = add_family(actor, "wizard.base.arcane-bolt")
        cast_id = CLOSURE_CASE_ID + "#Tcast1"
        actor["resources"]["resourceHistory"].append({
            "castId": cast_id, "at": 1200, "spell": "wizard.base.arcane-bolt", "class": "Wizard", "rank": 1,
            "school": "Universal", "action": "Action", "actualBasePaid": 1, "surchargePaid": 0, "totalPaid": 1,
            "RPAfter": 79, "firstPreparedFamily": first, "Refrain": 0, "DissonanceAdded": 0, "DissonanceAfter": 0,
            "components": ["V", "S", "F"], "focusCustodian": "T", "knownAndPrepared": True, "outcome": "committed-ready-hold"
        })
        actor["resources"]["ready"] = {"id": cast_id, "spell": "wizard.base.arcane-bolt", "paid": 1, "castAt": 1200,
            "expiresAt": 7100, "trigger": "H raises an empty right hand (visual; selected at preparation)", "targetChosenAtRelease": True}
        actor["resources"]["concentration"] = cast_id
        actor["clock"]["magicThisTurn"] = True
        actor["readyHistory"].append({"atMs": 1200, "status": "prepared", "spell": "wizard.base.arcane-bolt", "paidRP": 1,
            "expiry": 7100, "trigger": actor["resources"]["ready"]["trigger"],
            "castWindow": {"openedAtMs": 1200, "kind": "spell-cast interruption at Ready preparation",
                "authority": "COMMON_PROCEDURE ordinary Ready clause + Wizard Counterspell card trigger",
                "spell": "wizard.base.arcane-bolt", "rank": 1, "counterspellDC": 12,
                "costsAndComponentsCommittedBeforeWindow": {"actionSpent": True, "RPSpent": 1, "components": ["V", "S", "F"]},
                "eligibleResponders": [
                    {"actor": "A", "profile": "Wizard20", "distanceFeet": 20.0, "within60Feet": True,
                     "perceivesCasting": True, "lineOfEffect": True, "counterspellAcquired": True,
                     "reactionAvailable": True, "RPBefore": 80, "decision": "declined", "resourceSpent": 0},
                    {"actor": "H", "profile": "Wizard20", "distanceFeet": 22.361, "within60Feet": True,
                     "perceivesCasting": True, "lineOfEffect": True, "counterspellAcquired": True,
                     "reactionAvailable": True, "RPBefore": 80, "decision": "declined", "resourceSpent": 0}],
                "windowClosed": True, "counterspellCast": False},
            "targetChosenAtRelease": True})
    elif kind == "mind-collapse-commitment":
        actor = state["actors"]["A"]
        if actor["resources"]["budget"]["Action"] != 1 or actor["resources"]["RP"] != 80:
            raise ValueError("A is not eligible for the preserved Mind Collapse commitment")
        actor["resources"]["budget"]["Action"] = 0
        actor["resources"]["RP"] = 54
        actor["resources"]["lastSpell"] = "mind-collapse"
        actor["clock"]["magicThisTurn"] = True
        first = add_family(actor, "mind-collapse")
        actor["resources"]["resourceHistory"].append({
            "castId": CLOSURE_CASE_ID + "#Acast1", "at": 6200, "spell": "mind-collapse", "class": "Wizard", "rank": 9,
            "school": "Illusion", "action": "Action", "actualBasePaid": 26, "surchargePaid": 0, "totalPaid": 26,
            "RPAfter": 54, "firstPreparedFamily": first, "Refrain": 0, "DissonanceAdded": 0, "DissonanceAfter": 0,
            "components": ["V", "S", "F"], "focusCustodian": "A", "knownAndPrepared": True, "outcome": "committed"
        })
        state["mindCollapse"] = {"status": "committed", "owner": "A", "target": "T", "rank": 9, "DC": 19,
            "committedAtMs": 6200, "baseCostRP": 26, "admittedAtMs": None, "deadlineMs": None,
            "repeatEnds": [], "repeatSaves": [], "conditionalSource": "none"}
    elif kind == "counterspell-response":
        actor = state["actors"]["T"]
        if actor["resources"]["budget"]["Reaction"] != 1 or actor["resources"]["RP"] != 79:
            raise ValueError("T is not eligible for the authored Counterspell response")
        actor["resources"]["budget"]["Reaction"] = 0
        actor["resources"]["RP"] = 76
        actor["resources"]["recharge"]["wizard.base.counterspell"] = 2
        actor["resources"]["lastSpell"] = "wizard.base.counterspell"
        first = add_family(actor, "wizard.base.counterspell")
        actor["resources"]["resourceHistory"].append({
            "castId": CLOSURE_CASE_ID + "#Tcounterspell1", "at": 6201, "spell": "wizard.base.counterspell", "class": "Wizard",
            "rank": 1, "school": "Abjuration", "action": "Reaction", "actualBasePaid": 3, "surchargePaid": 0, "totalPaid": 3,
            "RPAfter": 76, "firstPreparedFamily": first, "Refrain": 0, "DissonanceAdded": 0, "DissonanceAfter": 0,
            "components": ["V", "S"], "focusCustodian": "T", "knownAndPrepared": True, "outcome": "check-failed; triggering spell proceeds"
        })
        actor["rechargeHistory"].append({"atMs": 6201, "source": "Counterspell use", "ability": "wizard.base.counterspell", "before": 0, "after": 2})
        state["mindCollapse"]["counterspell"] = {"caster": "T", "triggeringCaster": "A", "atMs": 6201, "targetSpellRank": 9,
            "check": {"die": 5, "INTPlusPB": 11, "total": 16, "DC": 28, "success": False},
            "result": "failed; Mind Collapse proceeds",
            "eligibleNestedResponders": [
                {"actor": "A", "profile": "Wizard20", "position": [0, 0, 0], "within60Feet": True, "lineOfEffect": True,
                 "counterspellAcquired": True, "reactionAvailable": True, "decision": "declined", "resourceSpent": 0},
                {"actor": "H", "profile": "Wizard20", "position": [0, 10, 0], "within60Feet": True, "lineOfEffect": True,
                 "counterspellAcquired": True, "reactionAvailable": True, "decision": "declined", "resourceSpent": 0},
            ]}
    elif kind == "mind-collapse-resolution":
        state["mindCollapse"]["status"] = "resolved-before-admission"
        state["mindCollapse"]["resolvedAtMs"] = 6203
        state["mindCollapse"]["counterspellOutcome"] = "failure; source resolves"
    elif kind == "mind-collapse-admission":
        actor = state["actors"]["T"]
        actor["conditions"] = ["Stunned"]
        actor["availability"] = {"Action": False, "BonusAction": False, "Reaction": False, "movement": False,
            "spellCommit": False, "abilityUse": False, "readyRelease": False, "basicActions": False}
        ready = actor["resources"]["ready"]
        actor["resources"]["ready"] = None
        actor["resources"]["concentration"] = None
        actor["readyHistory"].append({"atMs": 6205, "status": "terminated-by-Incapacitated/concentration-loss",
            "spell": "wizard.base.arcane-bolt", "paidRP": 1, "refund": 0, "scheduledExpiry": ready["expiresAt"] if ready else 7100,
            "futureTrigger": "H raises an empty right hand", "triggerOccurredBeforeAdmission": False,
            "releaseAttempted": False, "resurrectedAtScheduledExpiry": False})
        state["mindCollapse"].update({"status": "active", "admittedAtMs": 6205, "deadlineMs": 19900, "repeatEnds": [7900, 13900, 19900],
            "initialSave": {"atMs": 6205, "stat": "INT", "die": 2, "modifierPlusProficiency": 11, "total": 13, "DC": 19, "passed": False},
            "conditionalSource": "no acquired external provider asserted"})
    elif kind == "source-boundary-no-provider":
        state["sourceGrantBoundary"] = {"atMs": 6300, "providerFound": False, "providerAcquired": False, "providerActivated": False,
            "insertedTurnOccurred": False, "classification": "source boundary, not a turn",
            "historicalEventRef": spec.get("baseEventRef", {}).get("id")}
    elif kind == "END-phase20-expiry":
        state["mindCollapse"]["status"] = "expired"
        state["mindCollapse"]["endedAtMs"] = 19900
        state["mindCollapse"]["endReason"] = "third future regular target END then phase20 expiry"
        actor = state["actors"]["T"]
        actor["conditions"] = []
        actor["availability"] = {"Action": True, "BonusAction": True, "Reaction": True, "movement": True,
            "spellCommit": True, "abilityUse": True, "readyRelease": True, "basicActions": True}
    elif kind == "final-source-qualified-snapshot":
        state["finalSnapshotAtMs"] = 20000
    else:
        raise ValueError(f"unhandled source event kind: {kind}")


def build_delta() -> dict[str, Any]:
    if not (ROOT / "DescentReviewChanges").exists():
        raise SystemExit("Run this script from the repository root")
    OUT.mkdir(parents=True, exist_ok=True)
    with gzip.open(CASEBOOK, "rt", encoding="utf-8") as stream:
        casebook = json.load(stream)
    base_case = next(x for x in casebook["cases"] if x["id"] == BASE_CASE_ID)
    case_index = read_json(CASE_INDEX)
    index_record = next(x for x in case_index["cases"] if x["id"] == BASE_CASE_ID)
    if index_record["initialSHA256"] != base_case["initialSHA256"] or index_record["finalSHA256"] != base_case["finalSHA256"]:
        raise ValueError("the preserved base case no longer matches CASE_INDEX")
    procedure = read_json(PROCEDURE)
    profiles_file = read_json(ACTOR_PROFILES)
    wizard = read_json(WIZARD_SOURCE)
    profile = profiles_file["Wizard20"]
    base_initial_actors = base_case["initialState"]["actors"]
    profile_file_sha = sha_file(ACTOR_PROFILES)
    actors = {name: initial_actor(name, base_initial_actors[name], profile, profile_file_sha) for name in ("A", "T", "H")}
    acq = class_source_evidence(profile, base_initial_actors["T"], wizard)
    if wizard["cards"][5]["id"] != "wizard.base.arcane-bolt" or wizard["cards"][17]["id"] != "wizard.base.counterspell":
        raise ValueError("Wizard card pointers changed")
    if procedure["completeSourceAndAccess"]["id"] != "mind-collapse":
        raise ValueError("unexpected Mind Collapse procedure source")

    initial = {
        "schema": "MD196-closure-projection-v1", "caseId": CLOSURE_CASE_ID, "timeMs": 0,
        "authority": {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173},
        "regularMarkers": {k: {"starts": [], "ends": []} for k in ("A", "T", "H")},
        "actors": actors,
        "mindCollapse": {"status": "not-started", "owner": "A", "target": "T", "conditionalSource": "none", "repeatEnds": [], "repeatSaves": []},
        "sourceGrantBoundary": None, "finalSnapshotAtMs": None,
    }

    specs: list[dict[str, Any]] = []
    for event in base_case["events"]:
        ref, kind = base_event_ref(event), event["kind"]
        if kind == "cast commitment mind-collapse":
            spec = {"timeMs": event["timeMs"], "kind": "mind-collapse-commitment", "baseEventRef": ref,
                "evidence": "Preserved actual Wizard rank-9 commitment; 26 RP, Action, components, class access and save DC remain as in the held case."}
        elif kind == "cast resolution mind-collapse":
            spec = {"timeMs": event["timeMs"], "kind": "mind-collapse-resolution", "baseEventRef": ref,
                "evidence": "Counterspell check fails; the paid Mind Collapse source resolves."}
        elif kind == "recipient admission T":
            spec = {"timeMs": event["timeMs"], "kind": "mind-collapse-admission", "baseEventRef": ref,
                "evidence": "Initial INT save fails at 6.205; native Stunned/Incapacitated begins and ends the held spell without refund."}
        elif kind == "extra-turn source evidence boundary":
            spec = {"timeMs": event["timeMs"], "kind": "source-boundary-no-provider", "baseEventRef": ref,
                "evidence": "Retain 6.300 as a boundary observation. It is not a turn and establishes no acquired provider."}
        elif kind == "END-phase20 expiry":
            spec = {"timeMs": event["timeMs"], "kind": "END-phase20-expiry", "baseEventRef": ref,
                "evidence": "Phase-20 expiry follows the third failed INT save; no refund, refill or Ready restoration."}
        elif kind == "final source-qualified snapshot":
            spec = {"timeMs": event["timeMs"], "kind": "final-source-qualified-snapshot", "baseEventRef": ref,
                "evidence": "Final snapshot after all original regular markers and natural expiry."}
        else:
            spec = {"timeMs": event["timeMs"], "kind": kind, "baseEventRef": ref, "evidence": copy.deepcopy(event.get("evidence"))}
        specs.append(spec)
        if event["timeMs"] == 1100 and kind == "regular-start:T":
            specs.append({"timeMs": 1200, "kind": "ready-arcane-bolt",
                "evidence": "New closure delta event bound to Wizard card 5 and T's existing Wizard20 acquisition/access ledger."})
        if event["timeMs"] == 6200 and kind == "cast commitment mind-collapse":
            specs.append({"timeMs": 6201, "kind": "counterspell-response",
                "evidence": "New closure delta event bound to Wizard card 17; check fails 16 < DC28; A and H decline nested responses."})

    events: list[dict[str, Any]] = []
    state = copy.deepcopy(initial)
    snapshots: dict[str, dict[str, Any]] = {}
    base_by_id = {e["id"]: e for e in base_case["events"]}
    for ordinal, spec in enumerate(specs, start=1):
        before = copy.deepcopy(state)
        base_event = base_by_id.get(spec.get("baseEventRef", {}).get("id"))
        mutate_for_spec(state, spec, base_event)
        forward, inverse = make_diff(before, state), make_diff(state, before)
        ev = {"id": f"{CLOSURE_CASE_ID}:{ordinal}", "timeMs": spec["timeMs"], "kind": spec["kind"],
              "baseEventRef": spec.get("baseEventRef"), "evidence": spec.get("evidence"),
              "beforeSHA256": sha_json(before), "afterSHA256": sha_json(state), "forward": forward, "inverse": inverse}
        if apply_ops(before, forward) != state or apply_ops(state, inverse) != before:
            raise ValueError(f"patch round-trip failed for event {ev['id']}")
        events.append(ev)
        snapshots[ev["id"]] = copy.deepcopy(state)

    boundary_event = next(e for e in events if e["kind"] == "source-boundary-no-provider")
    boundary_state = snapshots[boundary_event["id"]]
    t = boundary_state["actors"]["T"]
    interface_view = {
        "T": {"conditions": copy.deepcopy(t["conditions"]), "availability": copy.deepcopy(t["availability"]),
              "resources": {"RP": t["resources"]["RP"], "budget": copy.deepcopy(t["resources"]["budget"]),
                  "recharge": copy.deepcopy(t["resources"]["recharge"]), "ready": copy.deepcopy(t["resources"]["ready"]),
                  "concentration": t["resources"]["concentration"], "Dissonance": t["resources"]["Dissonance"],
                  "Refrain": t["resources"]["Refrain"], "preparedFamiliesCast": copy.deepcopy(t["resources"]["preparedFamiliesCast"])},
              "clock": copy.deepcopy(t["clock"])},
        "regularMarkers": copy.deepcopy(boundary_state["regularMarkers"]), "mindCollapse": copy.deepcopy(boundary_state["mindCollapse"]),
    }
    interface_hash = sha_json(boundary_state)
    conditional_test = {
        "id": "MD290-CI-EXTRA-TURN-BOUNDARY-01", "kind": "conditional interface-injection START/END test",
        "testOnly": True, "actualGameplayEvent": False, "acquiredProviderAsserted": False, "providerSource": None, "actor": "T",
        "intervalLabel": "6.300–6.400 (interface envelope only; does not advance the authored world clock)",
        "triggerStimulus": {"actor": "H", "cue": "raises an empty right hand", "perceivableByT": True, "actualCampaignEvent": False},
        "readyRelease": {"attempted": False, "reason": "the paid Ready hold and concentration ended at 6.205; Stunned also bars Reaction use"},
        "stages": [
            {"atMs": 6300, "stage": "START", "turnContext": "inserted", "recipientCondition": ["Stunned"], "resourceMutation": False},
            {"atMs": 6300, "stage": "eligibility-evaluation", "voluntaryAction": False, "bonusAction": False, "reaction": False, "movement": False,
             "reason": "Stunned/Incapacitated remain operative; turn-local opportunities are subject to those conditions"},
            {"atMs": 6400, "stage": "END", "restoreContext": "interrupted regular schedule", "resourceMutation": False},
        ],
        "stateBeforeSHA256": interface_hash, "stateAfterSHA256": interface_hash,
        "stateBeforeProjection": interface_view, "stateAfterProjection": copy.deepcopy(interface_view),
        "assertions": {"allThreeRegularEndMarkersUnchanged": True, "noMindCollapseRepeatSaveOrDurationTick": True,
            "noRechargeTick": True, "noReactionRefresh": True, "noReadyDeadlineShiftOrRevival": True,
            "noRPChange": True, "noDissonanceOrRefrainChange": True, "noActionOrMovementOccurrence": True,
            "schedulingContextRestoredWithoutResourceRestoration": True},
    }

    source_paths = [CASEBOOK, CASE_INDEX, PROCEDURE, ACTOR_PROFILES, WIZARD_SOURCE, COMBAT_SOURCE, CATALOG_SOURCE, RULEBOOK_SOURCE, COMMON_PROCEDURE]
    source_files = {p.relative_to(ROOT).as_posix(): pointer_record(p) for p in source_paths}
    proc_source = procedure["completeSourceAndAccess"]["source"]
    profile_records = walk_ids(profile.get("acquisitionLedger", []), {"wizard.base.arcane-bolt", "wizard.base.counterspell"})
    closure = {
        "schema": "DD-MD196-B01-closure-delta-v1",
        "createdAtUtc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "directorDecision": {
            "id": "MD290-OBLIGATION-REVISION-01", "source": "GPT Director response in Calibration review part 6 after Return289",
            "scope": ["mind-collapse"],
            "supersedesRequirement": "MD196-B01's requirement to demonstrate an acquired, operational inserted-turn provider as a prerequisite for Mind Collapse acceptance. Preserve the historical finding unchanged.",
            "ruling": "The missing external provider is a conditional qualification rather than a whole-spell acceptance gate. Mind Collapse itself grants no turns. The bound combat rules distinguish inserted turns from regular clock markers; requiring another unresolved ability before accepting that distinction was an unnecessary dependency.",
            "explicitlyDoesNotClose": ["absolute-domination / AG190-B01", "psychic-scream / PF182-B02", "mass-phantom-killer / PF182-B02",
                "weird / PF182-B02", "summon-elemental-avatar / SH202-B01", "time-stop / TF192-B01"],
        },
        "authority": {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "acceptedIds": [], "appliedIds": []},
        "historicalFinding": {"id": "MD196-B01", "preservedUnchanged": True,
            "historicalText": "No exact acquired source granting a genuine full extra turn and complete legal actor had been bound for the positive branch; additional Actions and initiative movement were insufficient.",
            "currentDisposition": "Superseded as a Mind Collapse acceptance prerequisite by MD290-OBLIGATION-REVISION-01; retained as historical evidence and as a conditional qualification for actual use of any external provider."},
        "conditionalQualifications": [{"id": "MD290-Q-EXTRA-SOURCE",
            "text": "Actual use of an external inserted-turn provider remains conditional on its separately authorized procedure, lawful acquisition, activation, recipient eligibility and history. This review grants no such ability."}],
        "procedureAmendment": {"id": "MC290-EXTRA-TURN-BOUNDARY", "scope": "Mind Collapse only",
            "text": "An independently lawful inserted turn does not advance or replace Mind Collapse's three original regular-END markers. It supplies no additional Mind Collapse repeat save, duration decrement, regular-start recharge, Reaction refresh, Ready deadline or regular recovery tick. Stunned and Incapacitated remain operative throughout it. Any turn-local opportunities supplied by the external source remain subject to those conditions. Ending that inserted turn restores the interrupted scheduling context without restoring spent resources or ended effects."},
        "sourceBindings": {
            "files": source_files,
            "mindCollapseNativeSource": {"catalogPath": proc_source["catalogPath"], "catalogSha256": proc_source["catalogSha256"],
                "catalogKey": proc_source["catalogKey"], "corePath": proc_source["corePath"], "coreSha256": proc_source["coreSha256"],
                "coreEntryIndex": proc_source["coreEntries"][0]["index"], "coreOriginal": copy.deepcopy(proc_source["coreEntries"][0]["original"]),
                "catalogOriginal": copy.deepcopy(proc_source["original"]), "bindingInheritedFrom": "the unchanged MemoryDenial6 procedure and source evidence manifest"},
            "classCards": {
                "arcaneBolt": {"pointer": "/cards/5", "id": wizard["cards"][5]["id"], "name": wizard["cards"][5]["name"],
                    "acquisition": wizard["cards"][5]["acquisition"], "cost": wizard["cards"][5]["cost"]},
                "counterspell": {"pointer": "/cards/17", "id": wizard["cards"][17]["id"], "name": wizard["cards"][17]["name"],
                    "acquisition": wizard["cards"][17]["acquisition"], "cost": wizard["cards"][17]["cost"],
                    "rangeAndTarget": wizard["cards"][17]["rangeAndTarget"], "frequency": wizard["cards"][17]["frequency"]},
                "wizardClassSourceSha256": sha_file(WIZARD_SOURCE)},
            "profileAcquisitionRecords": profile_records,
            "clockAnchors": {"path": "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
                "sha256": sha_file(COMBAT_SOURCE), "lines": ["29-35", "47-66", "97-111"]},
            "procedureSourceSha256": sha_file(PROCEDURE),
        },
        "closureCase": {
            "id": CLOSURE_CASE_ID,
            "forkOf": {"id": BASE_CASE_ID, "initialSHA256": base_case["initialSHA256"], "finalSHA256": base_case["finalSHA256"],
                "casebookPath": CASEBOOK.relative_to(ROOT).as_posix(), "casebookSha256": sha_file(CASEBOOK), "casebookBytes": CASEBOOK.stat().st_size,
                "caseIndexPath": CASE_INDEX.relative_to(ROOT).as_posix(), "caseIndexSha256": sha_file(CASE_INDEX)},
            "preserveOriginalCaseBytes": True,
            "fixtureQualification": "Existing A/T/H Wizard20 profile and acquisition fixtures; data-only conditional actors, not authenticated campaign people or events.",
            "actorBindings": {name: copy.deepcopy(actor) for name, actor in actors.items()},
            "acquisitionEvidence": acq,
            "regularScheduleFromPreservedCase": {k: {"starts": [e["timeMs"] for e in base_case["events"] if e["kind"] == f"regular-start:{k}"],
                "ends": [e["timeMs"] for e in base_case["events"] if e["kind"] == f"regular-end:{k}"]} for k in ("A", "T", "H")},
            "initialState": initial, "events": events, "finalStateSHA256": sha_json(state),
            "conditionalInterfaceTests": [conditional_test],
            "expected": {"initialINTSave": "2+11=13 < DC19 at 6.205; Stunned begins", "regularENDs": [7900, 13900, 19900],
                "counterspell": "5+11=16 < DC28; paid Counterspell fails and Mind Collapse proceeds",
                "ready": "1 RP spent at 1.200; Ready ends with concentration at 6.205; 7.100 scheduled expiry is a no-op",
                "insertedTurnProvider": "not established; interface test is conditional and is not gameplay history"},
        },
        "acceptanceGate": ["Exact source/profile bindings and actual paid-cast legality", "Forward/inverse replay and full reverse traversal",
            "Unchanged admission and regular-END markers", "Nontrivial recharge, Reaction and Ready accounting",
            "Clear separation of actual gameplay history from conditional interface injection",
            "Preservation of other passing Mind Collapse cases and MD196-H01/H02/H03/H04/H06/H08"],
        "noCanonicalApplication": True,
    }
    return closure


def verify_delta(delta: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(f"failed: {name}; detail={detail}")

    for rel, binding in delta["sourceBindings"]["files"].items():
        p = ROOT / rel
        check(f"source bytes/hash: {rel}", p.exists() and p.stat().st_size == binding["bytes"] and sha_file(p) == binding["sha256"], binding)

    with gzip.open(CASEBOOK, "rt", encoding="utf-8") as stream:
        casebook = json.load(stream)
    base = next(x for x in casebook["cases"] if x["id"] == BASE_CASE_ID)
    fork = delta["closureCase"]["forkOf"]
    check("preserved base case identity and hashes",
        base["initialSHA256"] == fork["initialSHA256"] and base["finalSHA256"] == fork["finalSHA256"], fork)
    check("all source/profile actors retain Wizard20 profile hash",
        all(delta["closureCase"]["actorBindings"][x]["profileId"] == "Wizard20" and
            delta["closureCase"]["actorBindings"][x]["profileSnapshotSha256"] == "3cd3c9baa0b24f9389757f56ee7b6e4ae919d7a67359beb79dcc0e51e8a69aa4" for x in ("A", "T", "H")))
    native = delta["sourceBindings"]["mindCollapseNativeSource"]
    check("inherited Mind Collapse catalog/core hashes are exact",
        native["catalogSha256"] == "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078" and
        native["coreSha256"] == "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f")
    check("Wizard class card pointers are exact",
        delta["sourceBindings"]["classCards"]["arcaneBolt"]["pointer"] == "/cards/5" and
        delta["sourceBindings"]["classCards"]["counterspell"]["pointer"] == "/cards/17")
    check("authority remains 816/32/0, no accept or apply",
        delta["authority"] == {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "acceptedIds": [], "appliedIds": []})

    state = copy.deepcopy(delta["closureCase"]["initialState"])
    initial_hash = sha_json(state)
    snapshots: dict[str, dict[str, Any]] = {}
    last_time = -1
    for ev in delta["closureCase"]["events"]:
        check(f"event order {ev['id']}", ev["timeMs"] >= last_time, {"timeMs": ev["timeMs"], "previous": last_time})
        check(f"forward prehash {ev['id']}", sha_json(state) == ev["beforeSHA256"])
        state = apply_ops(state, ev["forward"])
        check(f"forward posthash {ev['id']}", sha_json(state) == ev["afterSHA256"])
        snapshots[ev["id"]] = copy.deepcopy(state)
        last_time = ev["timeMs"]
    final_hash = sha_json(state)
    check("final state hash", final_hash == delta["closureCase"]["finalStateSHA256"])
    for ev in reversed(delta["closureCase"]["events"]):
        check(f"inverse prehash {ev['id']}", sha_json(state) == ev["afterSHA256"])
        state = apply_ops(state, ev["inverse"])
        check(f"inverse posthash {ev['id']}", sha_json(state) == ev["beforeSHA256"])
    check("full reverse traversal returns exact initial state", sha_json(state) == initial_hash)

    case = delta["closureCase"]
    schedule = case["regularScheduleFromPreservedCase"]
    final_state = snapshots[case["events"][-1]["id"]]
    for actor_id in ("A", "T", "H"):
        check(f"unchanged regular schedule for {actor_id}", final_state["regularMarkers"][actor_id] == schedule[actor_id],
              final_state["regularMarkers"][actor_id])
    check("exact three Mind Collapse regular ENDs", final_state["mindCollapse"]["repeatEnds"] == [7900, 13900, 19900])

    ready_event = next(e for e in case["events"] if e["kind"] == "ready-arcane-bolt")
    ready_state = snapshots[ready_event["id"]]["actors"]["T"]
    check("paid Arcane Bolt Ready at 1.200", ready_state["resources"]["RP"] == 79 and
        ready_state["resources"]["budget"]["Action"] == 0 and ready_state["resources"]["ready"]["expiresAt"] == 7100 and
        ready_state["resources"]["concentration"] is not None and ready_state["clock"]["magicThisTurn"] is True)
    ready_record = ready_state["readyHistory"][-1]
    ready_window = ready_record["castWindow"]
    check("Ready spell cast-interruption window is recorded at preparation",
        ready_window["openedAtMs"] == 1200 and ready_window["spell"] == "wizard.base.arcane-bolt" and
        ready_window["rank"] == 1 and ready_window["counterspellDC"] == 12 and ready_window["windowClosed"] and
        not ready_window["counterspellCast"] and ready_window["costsAndComponentsCommittedBeforeWindow"] ==
        {"actionSpent": True, "RPSpent": 1, "components": ["V", "S", "F"]})
    ready_responders = ready_window["eligibleResponders"]
    check("A and H are eligible Ready-window Counterspell responders and explicitly decline",
        [x["actor"] for x in ready_responders] == ["A", "H"] and
        all(x["within60Feet"] and x["perceivesCasting"] and x["lineOfEffect"] and x["counterspellAcquired"] and
            x["reactionAvailable"] and x["decision"] == "declined" and x["resourceSpent"] == 0 and x["RPBefore"] == 80
            for x in ready_responders))
    counter_event = next(e for e in case["events"] if e["kind"] == "counterspell-response")
    counter_state = snapshots[counter_event["id"]]
    t_counter = counter_state["actors"]["T"]
    check("paid Counterspell failure at 6.201", t_counter["resources"]["RP"] == 76 and
        t_counter["resources"]["budget"]["Reaction"] == 0 and t_counter["resources"]["recharge"]["wizard.base.counterspell"] == 2 and
        counter_state["mindCollapse"]["counterspell"]["check"] == {"die": 5, "INTPlusPB": 11, "total": 16, "DC": 28, "success": False})
    nested = counter_state["mindCollapse"]["counterspell"]["eligibleNestedResponders"]
    check("A and H nested responses explicitly decline without spending",
        [x["decision"] for x in nested] == ["declined", "declined"] and all(x["resourceSpent"] == 0 for x in nested))
    mind_cast_event = next(e for e in case["events"] if e["kind"] == "mind-collapse-commitment")
    mind_cast_state = snapshots[mind_cast_event["id"]]["actors"]["A"]
    check("Mind Collapse paid commitment preserves the cast-this-regular-turn flag",
        mind_cast_state["clock"]["magicThisTurn"] is True and mind_cast_state["resources"]["lastSpell"] == "mind-collapse" and
        mind_cast_state["resources"]["RP"] == 54 and mind_cast_state["resources"]["budget"]["Action"] == 0)
    t_end_1900 = next(e for e in case["events"] if e["kind"] == "regular-end:T" and e["timeMs"] == 1900)
    a_end_6900 = next(e for e in case["events"] if e["kind"] == "regular-end:A" and e["timeMs"] == 6900)
    check("regular END preserves prior paid-cast magicThisTurn flags",
        snapshots[t_end_1900["id"]]["actors"]["T"]["clock"]["magicThisTurn"] is True and
        snapshots[a_end_6900["id"]]["actors"]["A"]["clock"]["magicThisTurn"] is True)
    admission_event = next(e for e in case["events"] if e["kind"] == "mind-collapse-admission")
    admitted = snapshots[admission_event["id"]]
    t_admitted = admitted["actors"]["T"]
    check("admission, Stunned and Ready/concentration loss", admitted["mindCollapse"]["admittedAtMs"] == 6205 and
        admitted["mindCollapse"]["initialSave"]["total"] == 13 and t_admitted["conditions"] == ["Stunned"] and
        t_admitted["resources"]["ready"] is None and t_admitted["resources"]["concentration"] is None and
        t_admitted["resources"]["RP"] == 76)
    boundary_event = next(e for e in case["events"] if e["kind"] == "source-boundary-no-provider")
    boundary_state = snapshots[boundary_event["id"]]
    interface = case["conditionalInterfaceTests"][0]
    check("source boundary remains no turn/provider",
        boundary_state["sourceGrantBoundary"]["providerFound"] is False and
        boundary_state["sourceGrantBoundary"]["insertedTurnOccurred"] is False)
    check("conditional interface injection is a state no-op",
        interface["testOnly"] and not interface["actualGameplayEvent"] and not interface["acquiredProviderAsserted"] and
        interface["stateBeforeSHA256"] == interface["stateAfterSHA256"] == sha_json(boundary_state))
    view_t = interface["stateBeforeProjection"]["T"]
    check("Stunned prevents every tested turn-local opportunity",
        view_t["conditions"] == ["Stunned"] and all(view_t["availability"][x] is False for x in ("Action", "BonusAction", "Reaction", "movement")))
    check("conditional interface no-op preserves the paid-cast flag in both projections",
        view_t["clock"]["magicThisTurn"] is True and
        interface["stateAfterProjection"]["T"]["clock"]["magicThisTurn"] is True)
    t_start_7100 = next(e for e in case["events"] if e["kind"] == "regular-start:T" and e["timeMs"] == 7100)
    check("T regular START resets magicThisTurn for the new regular turn",
        snapshots[t_start_7100["id"]]["actors"]["T"]["clock"]["magicThisTurn"] is False)
    check("Ready scheduled expiry is a no-op at 7.100",
        any(x.get("result", "").startswith("no-op") and x["atMs"] == 7100 for x in snapshots[t_start_7100["id"]]["actors"]["T"]["readyHistory"]))
    for tm, expected_recharge in ((7100, 1), (13100, 0), (19100, 0)):
        event = next(e for e in case["events"] if e["kind"] == "regular-start:T" and e["timeMs"] == tm)
        actor_at_start = snapshots[event["id"]]["actors"]["T"]
        check(f"Counterspell recharge at T regular START {tm}",
            actor_at_start["resources"]["recharge"]["wizard.base.counterspell"] == expected_recharge)
        check(f"Stunned prohibits use of refreshed opportunities at T regular START {tm}",
            actor_at_start["conditions"] == ["Stunned"] and
            all(actor_at_start["availability"][x] is False for x in
                ("Action", "BonusAction", "Reaction", "movement", "spellCommit", "abilityUse", "readyRelease", "basicActions")))
    check("three failed target-END saves occur before natural expiry",
        [x["atMs"] for x in final_state["mindCollapse"]["repeatSaves"]] == [7900, 13900, 19900] and
        final_state["mindCollapse"]["status"] == "expired")
    check("spell family, Dissonance and Refrain histories are preserved",
        final_state["actors"]["T"]["resources"]["preparedFamiliesCast"] == ["wizard.base.arcane-bolt", "wizard.base.counterspell"] and
        final_state["actors"]["T"]["resources"]["Dissonance"] == 0 and final_state["actors"]["T"]["resources"]["Refrain"] == 0)
    check("historical case remains an unchanged base reference", case["preserveOriginalCaseBytes"] and case["forkOf"]["id"] == BASE_CASE_ID)
    gate_text = " ".join(delta["acceptanceGate"])
    check("other passing Mind Collapse qualifiers remain in the acceptance gate",
        "MD196-H01/H02/H03/H04/H06/H08" in gate_text)

    return {"id": "MD196-B01-CLOSURE-DELTA-INDEPENDENT-AUDIT", "status": "PASS",
        "checksPassed": sum(1 for x in checks if x["passed"]), "checksFailed": sum(1 for x in checks if not x["passed"]),
        "checks": checks, "closureDeltaSha256": sha_json(delta),
        "closureDeltaStatus": "submitted for final Director acceptance; not accepted or applied",
        "qualifications": ["Static authored witness and focused interface test only; no runtime or human-play claim.",
            "The conditional interface injection is never represented as an acquired gameplay grant.",
            "The Director's obligation revision applies only to Mind Collapse and does not close any other pending spell."]}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    delta_path = OUT / "MD196_B01_CLOSURE_DELTA.json"
    audit_path = OUT / "MD196_B01_CLOSURE_DELTA_INDEPENDENT_AUDIT.json"
    delta = build_delta()
    delta_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    loaded = read_json(delta_path)
    audit = verify_delta(loaded)
    audit["closureDeltaFileSha256"] = sha_file(delta_path)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": audit["status"], "checksPassed": audit["checksPassed"], "checksFailed": audit["checksFailed"],
        "delta": str(delta_path), "deltaSha256": audit["closureDeltaFileSha256"], "audit": str(audit_path)}, indent=2))


if __name__ == "__main__":
    main()

