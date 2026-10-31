from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import pathlib
import subprocess
import zlib
import zipfile

import jsonpatch


ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_wardcontrol6_reality_anchor_packet_316_prepared_build04"
PACKET_NAME = "DD_Rank9_WardControl6_RealityAnchor_316.zip"
DELIVERY_NAME = "DD_Rank9_WardControl6_RealityAnchor_316_DELIVERY.json"
PACKET = OUT / PACKET_NAME
DELIVERY = OUT / DELIVERY_NAME
RETURN281 = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
RETURN281_DELIVERY = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
RETURN281_AUDIT = A / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
SOURCE312_DIR = A / "rank9_wardcontrol6_source_packet_312_prepared"
SOURCE312 = SOURCE312_DIR / "DD_Rank9_WardControl6_CurrentSource_312.zip"
SOURCE_REFRESH312 = A / "SOURCE_REFRESH_312.json"
QUEUE314 = A / "CURRENT_SPELL_QUEUE_315.json"
HANDOFF314 = A / "CURRENT_HANDOFF_315.json"
AUDIT312 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_315.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
FORGE_DIR = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255"
FORGE_AUDIT = A
TARGET = "reality-anchor"
BLOCKER = "WC188-B02"
RETURN315_DIR = A / "rank9_wardcontrol6_return315_received"
RETURN315 = RETURN315_DIR / "DD_Rank9_WardControl6_Director_Return315_HELD.zip"
RETURN315_DELIVERY = RETURN315_DIR / "DD_Rank9_WardControl6_Director_Return315_HELD_DELIVERY.json"
RETURN315_AUDIT = A / "REALITY_ANCHOR_RETURN315_INDEPENDENT_AUDIT.json"
AUTHORITY = {
    "reviewedApplied": 822,
    "pending": 26,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 546,
    "scopedInterfaces": 173,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def state_sha(value: dict) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha(raw)


def jb(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def read_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: pathlib.Path, raw: bytes | None = None, member: str | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "member": member, **digest(data)}


def make_w2_endpoint() -> tuple[dict, dict]:
    w2 = read_json(FORGE_DIR / "SUPPLEMENT255_W2.json")
    branch = w2["eventReplay"]["branches"][0]
    state = copy.deepcopy(w2["priorCase"]["endState"])
    assert state_sha(state) == branch["baseStateSHA256"]
    replay_checks = []
    for event in branch["events"]:
        before = state_sha(state)
        assert before == event["beforeSHA256"], event["id"]
        state = jsonpatch.JsonPatch(event["forward"]).apply(state, in_place=False)
        after = state_sha(state)
        assert after == event["afterSHA256"], event["id"]
        replay_checks.append({"id": event["id"], "beforeSHA256": before, "afterSHA256": after, "forwardCount": len(event["forward"]), "inverseCount": len(event["inverse"])})
    assert state_sha(state) == branch["finalStateSHA256"] == "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e"
    assert state["actors"]["A"]["RP"] == 13 and state["actors"]["A"]["Dissonance"] == 2
    assert state["items"]["bracelet-2"]["imprintRoot"]["id"] == "castF3"
    assert state["items"]["bracelet-2"]["imprintRoot"]["active"] is True
    return state, {"branch": branch, "replayChecks": replay_checks, "supplement": w2}


def make_actor_c(return_zip: zipfile.ZipFile, w2_actor: dict) -> dict:
    actor = copy.deepcopy(w2_actor)
    actor["id"] = "C"
    actor["profile"] = "ACTOR_PROFILES.json#/W219"
    actor["positionFeet"] = [75, 0, 0]
    actor["RP"] = 68
    actor["maxRP"] = 68
    actor["HP"] = 110
    actor["maxHP"] = 110
    actor["Dissonance"] = 0
    actor["Refrain"] = 0
    actor["lastSpell"] = None
    actor["concentration"] = None
    actor["Action"] = 0
    actor["Reaction"] = 0
    actor["BonusAction"] = 1
    actor["freeInteraction"] = 1
    actor["movementRemaining"] = 30
    actor["regularStart"] = 172806.6
    actor["nextRegularStart"] = 172806.6
    actor["nextRegularEnd"] = None
    actor["regularStartsProcessed"] = []
    actor["hands"] = {"left": "C-focus", "right": None}
    actor["worn"] = []
    actor["resourceHistory"] = []
    actor["resourceCredits"] = []
    actor["usedPreparedFamilies"] = []
    actor["turnCast"] = False
    actor["spellPreparationRecord"] = {
        "fixtureId": "RA316-C-PREP-01",
        "class": "Wizard",
        "classLevel": 18,
        "spellId": "reality-anchor",
        "acquisition": "W219 ordinary repertoire and Wizard level-up source; see exact source profile and current wizard playtest binding",
        "dailyPreparation": "explicit authored fixture selection after completed beneficial long rest; selects Reality Anchor from W219 source-supported spell access, within preparedCapacity 24",
        "preparedCapacity": 24,
        "baseRP": 68,
        "preparedFamilyHistoryAtEntry": [],
        "casterClassAbility": "INT 20 (+5)",
        "proficiencyBonus": 6,
        "spellAttack": 11,
        "spellDC": 19,
        "focus": "C-focus held; usable voice and somatic hand from W219 profile",
        "restAndPreparationAreOwnFixtureHistory": True,
        "noPriorCaseEventsImported": True,
    }
    return actor


def case_state(base: dict, branch_id: str, actor_c: dict) -> dict:
    s = copy.deepcopy(base)
    s.setdefault("applications", {})
    s.setdefault("fields", {})
    s.setdefault("supplement", {})
    s["supplement"]["realityAnchorWitness316"] = {
        "branchId": branch_id,
        "status": "NONCANONICAL_LOCAL_WITNESS_DRAFT_FOR_DIRECTOR_REVIEW",
        "clock": {"id": "RA316-WITNESS-CLOCK", "startSeconds": 172806.6, "dawns": [172800, 259200], "timezone": "fixture absolute seconds; no calendar claim"},
        "sources": {
            "forgeApplicationId": "castF3",
            "physicalItemId": "bracelet-2",
            "forgeNaturalExpiry": None,
            "forgeSourceDeadline": "none; accepted Forge contract says Until-dispelled with no natural expiry",
            "startingW2StateSHA256": "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e",
            "w2EndpointTimeSeconds": 172806.6,
        },
        "scene": {
            "authorship": "local bounded witness geometry only",
            "Afeet": [0, 0, 0], "Bfeet": [5, 0, 0], "Cfeet": [75, 0, 0],
            "itemBodyBoxFeet": [[0, 3, 0], [0.4, 3.4, 0.1]],
            "anchorCenterFeet": [75, 0, 0],
            "anchorRadiusFeet": 100,
            "distanceCToCenterFeet": 0,
            "distanceCenterToItemBodyMinMaxFeet": [74.6, 75.41],
            "distanceCenterToAFeet": 75,
            "distanceCenterToBFeet": 70,
            "lineOfEffect": "unblocked in bounded fixture; no solid total cover intersects relevant rays",
            "centerPerceivedByC": True,
            "itemAndAInsideField": True,
            "BIsObserver": True,
            "hideOpportunity": "local scene fixture supplies opaque cover adjacent to A, breaks B's clear view, and leaves item center/RA line of effect unobstructed",
        },
        "actorC": {"profile": "ACTOR_PROFILES.json#/W219", "preparation": actor_c["spellPreparationRecord"], "historyImportedFromPriorRAEvents": False},
        "events": [],
        "dueClockEvents": [],
        "policyHistory": [],
        "deniedExpressions": [],
        "functionEvents": [],
        "custodyHistory": [],
        "imprintEndings": [],
    }
    return s


def add_event(branch: dict, event_id: str, kind: str, start: float, end: float, description: str, mutate, record: dict) -> None:
    state = branch["state"]
    before = state_sha(state)
    before_state = copy.deepcopy(state)
    mutate(state)
    state["time"] = end
    trace = {"id": event_id, "kind": kind, "timeStartSeconds": start, "timeEndSeconds": end, "description": description, **record}
    state["supplement"]["realityAnchorWitness316"]["events"].append(trace)
    state["processedEvents"].append(event_id)
    forward = copy.deepcopy(jsonpatch.make_patch(before_state, state).patch)
    after = state_sha(state)
    inverse = copy.deepcopy(jsonpatch.make_patch(state, before_state).patch)
    check = jsonpatch.JsonPatch(forward).apply(before_state, in_place=False)
    assert state_sha(check) == after
    undo = jsonpatch.JsonPatch(inverse).apply(check, in_place=False)
    assert state_sha(undo) == before
    branch["events"].append({
        "id": event_id, "kind": kind,
        "timeStartSeconds": start, "timeEndSeconds": end,
        "description": description,
        "beforeSHA256": before, "afterSHA256": after,
        "forward": forward, "inverse": inverse,
        "record": trace,
    })
    branch["state"] = state


def refresh_start(actor: dict, time_s: float, actor_id: str) -> None:
    assert math.isclose(float(actor.get("nextRegularStart")), time_s, abs_tol=1e-6), (actor_id, actor.get("nextRegularStart"), time_s)
    actor.update({"Action": 1, "BonusAction": 1, "Reaction": 1, "freeInteraction": 1, "movementRemaining": 30, "turnOpen": True})
    actor.setdefault("regularStartsProcessed", []).append(time_s)
    actor["regularStart"] = time_s
    actor["nextRegularStart"] = round(time_s + 6, 1)
    actor["nextRegularEnd"] = round(time_s + 5.8, 1)


def add_actor_c(s: dict, actor_c: dict) -> None:
    s["actors"]["C"] = copy.deepcopy(actor_c)
    s["actors"]["C"]["Action"] = 1
    s["actors"]["C"]["Reaction"] = 1
    s["actors"]["C"]["regularStartsProcessed"] = [172806.6]
    s["actors"]["C"]["regularStart"] = 172806.6
    s["actors"]["C"]["nextRegularStart"] = 172812.6
    s["actors"]["C"]["nextRegularEnd"] = 172812.4
    s["actors"]["C"]["turnOpen"] = True
    s["supplement"]["realityAnchorWitness316"]["dueClockEvents"].append({"kind": "regular-start", "actor": "C", "timeSeconds": 172806.6, "budgetRefreshed": True, "Action": 1, "Reaction": 1, "source": "new bounded witness fixture"})


def add_case_common(branch: dict, actor_c: dict, include_allow_a: bool) -> None:
    branch["state"] = copy.deepcopy(branch["baseState"])
    def m(s):
        seeded = case_state(s, branch["id"], actor_c)
        s.clear()
        s.update(seeded)
        add_actor_c(s, actor_c)
        # The accepted W2 endpoint carries the exact last START timestamps; create only the local continuation END markers required before new STARTs.
        inherited_end = {"A": 172812.2, "B": 172812.0}
        for actor_id, end_time in inherited_end.items():
            s["actors"][actor_id]["turnOpen"] = True
            s["actors"][actor_id]["nextRegularEnd"] = end_time
            s["actors"][actor_id].setdefault("regularEndsProcessed", [])
        s["supplement"]["realityAnchorWitness316"]["inheritedTurnContinuations"] = [{"actor": "B", "sourceRegularStart": 172806.2, "insertedEnd": 172812.0}, {"actor": "A", "sourceRegularStart": 172806.4, "insertedEnd": 172812.2}]
        s["supplement"]["realityAnchorWitness316"]["policyHistory"].append({
            "policyId": "RA316-POLICY-01", "mode": "Permission", "default": "DENY",
            "predeclaredRules": [
                {"order": 1, "effect": "DENY", "applicationId": "castF3", "why": "exact known Eternal Forge imprint under test"},
                *([{"order": 2, "effect": "ALLOW", "casterIdentity": "A", "why": "known W2 owner/caster identity; admits A's Greater Dispel operation"}] if include_allow_a else []),
                {"order": 3 if include_allow_a else 2, "effect": "ALLOW", "applicationId": "castRA1", "why": "keep this already-established Anchor's own field operation addressable"},
            ],
            "firstMatchWins": True,
            "noHiddenIdentityOrInventoryOracle": True,
        })
        s["supplement"]["realityAnchorWitness316"]["preparationAndSourceAudit"] = {
            "completeItemProfile": {"itemId": "bracelet-2", "owner": "A", "custodianAtStart": "A-floor-within-5ft", "HP": 5, "maxHP": 5, "damage": 0, "charges": 1, "maxCharges": 1, "contents": [], "processedDawns": [], "createdAt": 172806.5, "rootId": "castF3", "rootRank": 9, "rootActive": True, "rootSource": "accepted Eternal Forge W2 event MF247-F-W2-E23", "rootNaturalExpiry": None},
            "creationAcquisitionHistory": "exact accepted Eternal Forge W2 continuation, copied only from endpoint hash 684d...109e; bracelet-1/castF2 remains ended and physically preserved",
            "ownerCustodyAndUse": "A is owner/caster; floor custody within 5ft; local fit fixture records an open ordinary left wrist for A before don; no transfer of ownership",
            "itemUseCosts": "no activation RP; an eligible Hide check consumes the existing one charge only when the source expression is permitted and the effect is actually used; commit charge before rolling",
            "originalSourceDeadline": "none; source model says no natural expiry, concentration, caster-survival tether or ongoing range limit",
            "RAProfile": {"class": "Wizard", "level": 18, "rank": 9, "mode": "Permission", "baseRP": 26, "components": "V/S/F", "action": "Action", "rangeFeet": 100, "radiusFeet": 100, "duration": "60 elapsed seconds concentration", "anchorSourceDeadlineSeconds": 172866.7, "centerFeet": [75, 0, 0]},
        }
        w = s["supplement"]["realityAnchorWitness316"]
        w["hideOutcomes"] = []
        w.setdefault("suppressionEvents", [])
        w.setdefault("movementHistory", [])
        w["scene"].update({"BIsObserver": False, "CIsObserver": True, "hideOpportunity": "Local partial cover blocks C's clear sight; separate opaque screen excludes B; line of effect to the item remains unobstructed."})
    add_event(branch, "RA316-" + branch["id"] + "-E01-ENTER-W219-C", "source-fixture-entry-and-policy-predeclaration", 172806.6, 172806.65,
              "Add the separately source-qualified W219 caster and predeclare the exact Permission-mode policy; import no prior W219 case events.", m,
              {"actorProfile": "ACTOR_PROFILES.json#/W219", "historyImported": False, "mode": "Permission", "predeclaredPolicyId": "RA316-POLICY-01", "inheritedContinuationENDs": {"B": 172812.0, "A": 172812.2}, "continuationMarkerDoesNotChangeW2Endpoint": True})


def cast_ra(branch: dict, actor_id: str) -> None:
    def m(s):
        c = s["actors"]["C"]
        assert c["Action"] == 1 and c["RP"] == 68
        c["Action"] = 0
        c["RP"] = 42
        c["lastSpell"] = TARGET
        c["usedPreparedFamilies"].append(TARGET)
        c["turnCast"] = True
        c["concentration"] = {"applicationId": "castRA1", "spell": TARGET, "endsAtSeconds": 172866.7, "maintained": True}
        c.setdefault("resourceHistory", []).append({"castId": "castRA1", "spell": TARGET, "time": 172806.7, "cost": 26, "action": "Action", "components": "V/S/F", "preCastDissonance": 0, "RefrainAdded": 0, "firstFamily": True, "DissonanceAfter": 0, "turnCast": True})
        s["applications"]["castRA1"] = {"id": "castRA1", "spellId": TARGET, "caster": "C", "class": "Wizard", "classLevel": 18, "generatingSchool": "Abjuration", "generatingRank": 9, "paidRP": 26, "costAdjustments": {"preCastDissonance": 0, "RefrainAdded": 0}, "components": "V/S/F", "originFeet": [75, 0, 0], "centerFeet": [75, 0, 0], "rangeFeet": 100, "radiusFeet": 100, "mode": "Permission", "policyId": "RA316-POLICY-01", "establishedAtSeconds": 172806.7, "endsAtSeconds": 172866.7, "maintainer": "C", "concentration": True, "status": "active", "totalCoverClipped": False}
        s["applications"]["castRA1"]["policy"] = {"id": "RA316-POLICY-01", "revision": 0, "mode": "Permission", "default": "DENY", "rules": copy.deepcopy(s["supplement"]["realityAnchorWitness316"]["policyHistory"][-1]["predeclaredRules"]), "firstMatchWins": True}
        s["fields"]["castRA1"] = {"sourceId": "castRA1", "centerFeet": [75, 0, 0], "radiusFeet": 100, "policyId": "RA316-POLICY-01", "expiresAtSeconds": 172866.7, "owner": "C", "status": "active"}
    add_event(branch, actor_id, "paid-reality-anchor-cast-and-establishment", 172806.65, 172806.7,
              "C pays 26 RP and one Action to establish a fixed Permission-mode Reality Anchor at the perceived center; castF3 falls within the 100-foot field.", m,
              {"caster": "C", "spellId": TARGET, "castId": "castRA1", "costRP": 26, "preCastRP": 68, "postCastRP": 42, "action": "Action", "components": "V/S/F", "mode": "Permission", "defaultPolicy": "DENY", "centerFeet": [75, 0, 0], "centerDistanceFromCasterFeet": 0, "radiusFeet": 100, "expiresAtSeconds": 172866.7, "capturedApplications": [], "itemInsideField": True, "allCostsPaidBeforeEstablishment": True, "counterWindow": {"eligibleCounterers": [], "A": {"distanceFeet": 75, "reason": "outside accepted 60-foot Counterspell range"}, "B": {"distanceFeet": 70, "reason": "noncasting receiver; no Counterspell acquisition"}, "C": {"reason": "cannot counter own cast"}}})


def regular_start(branch: dict, actor_id: str, time_s: float, event_number: int) -> None:
    def m(s):
        actor = s["actors"][actor_id]
        refresh_start(actor, time_s, actor_id)
        s["supplement"]["realityAnchorWitness316"]["dueClockEvents"].append({"kind": "regular-start", "actor": actor_id, "timeSeconds": time_s, "budgetRefreshed": True, "Action": 1, "Reaction": 1, "BonusAction": 1})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-{actor_id}-START", "regular-start", time_s, time_s,
              f"Process {actor_id}'s due regular start exactly once; refresh Action, Reaction, Bonus Action and movement budget.", m,
              {"actor": actor_id, "ActionAfter": 1, "ReactionAfter": 1, "sourceSchedulePreserved": True})


def regular_end(branch: dict, actor_id: str, time_s: float, event_number: int) -> None:
    def m(s):
        actor = s["actors"][actor_id]
        assert actor.get("turnOpen") is True and math.isclose(float(actor.get("nextRegularEnd")), time_s, abs_tol=1e-6), (actor_id, actor.get("nextRegularEnd"), time_s)
        actor["turnOpen"] = False
        actor.setdefault("regularEndsProcessed", []).append(time_s)
        s["supplement"]["realityAnchorWitness316"]["dueClockEvents"].append({"kind": "regular-end", "actor": actor_id, "timeSeconds": time_s, "turnClosed": True})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-{actor_id}-END", "regular-end", time_s, time_s,
              f"Close {actor_id}'s due regular turn without granting another action or changing any source clock.", m,
              {"actor": actor_id, "turnClosed": True, "sourceDeadlineUnchanged": True})


def don_item(branch: dict, event_number: int) -> None:
    def m(s):
        a = s["actors"]["A"]
        item = s["items"]["bracelet-2"]
        assert a["Action"] == 1 and item["imprintRoot"]["active"]
        a["Action"] = 0
        item["custodian"] = "A-left-wrist"
        item["worn"] = True
        item["revision"] += 1
        item["wearFixture"] = {"wearer": "A", "site": "left wrist", "fit": "local bounded test fixture; no global size claim", "wristOpen": True}
        a.setdefault("worn", []).append("bracelet-2")
        s["supplement"]["realityAnchorWitness316"]["custodyHistory"] = [{"timeSeconds": 172812.5, "itemId": "bracelet-2", "owner": "A", "from": "A-floor-within-5ft", "to": "A-left-wrist", "cost": "A Action", "consent": True}]
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-DON-BRACELET2", "lawful-wear", 172812.41, 172812.5,
              "A spends an Action to don the existing bracelet-2 without changing ownership, body integrity, charge or castF3 history.", m,
              {"actor": "A", "itemId": "bracelet-2", "cost": "Action", "ownerUnchanged": True, "custodyAfter": "A-left-wrist", "HP": 5, "charges": 1})


def denied_hide(branch: dict, event_number: int, termination: bool = False) -> None:
    def m(s):
        a = s["actors"]["A"]
        item = s["items"]["bracelet-2"]
        assert a["Action"] == 1
        a["Action"] = 0
        s["supplement"]["realityAnchorWitness316"]["deniedExpressions"].append({"timeSeconds": 172818.5, "actor": "A", "itemId": "bracelet-2", "sourceId": "castF3", "function": "eligible Hide / Stealth-family item expression", "decision": "DENIED", "reason": "first matching exact applicationId castF3 policy", "underlyingSourceRetained": item["imprintRoot"]["active"], "chargeBefore": item["charges"], "chargeAfter": item["charges"], "bonusApplied": 0, "advantageApplied": False, "actionContinuesWithoutItemExpression": True})
        item["imprintRoot"]["suppressed"] = True
        item["imprintRoot"]["suppressedBy"] = ["castRA1"]
        item["functionalState"] = "item magical expression denied; physical body persists"
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-HIDE-DENIED", "permission-denial-of-item-expression", 172818.41, 172818.5,
              "A's otherwise eligible Hide action proceeds, while the exact castF3 item expression is denied; no charge is spent and no magical bonus or advantage is applied.", m,
              {"actor": "A", "itemId": "bracelet-2", "applicationId": "castF3", "policyId": "RA316-POLICY-01", "decision": "DENIED", "chargeBefore": 1, "chargeAfter": 1, "bonusApplied": 0, "advantageApplied": False, "diceInput": {"kind": "DEX-Stealth task input", "d20": 15, "selectedBy": "local test input", "no hidden success or observer result asserted": True}, "physicalBodyAndCustodyRemain": True})


def edit_policy(branch: dict, event_number: int, allow_forge: bool, at: float, after_termination: bool = False) -> None:
    def m(s):
        app = s["applications"]["castRA1"]
        policy = app["policy"]
        if allow_forge:
            policy["rules"] = [
                {"order": 1, "effect": "ALLOW", "applicationId": "castF3", "why": "owner's actual Action policy edit after source handle was established"},
                {"order": 2, "effect": "ALLOW", "applicationId": "castRA1", "why": "field operation"},
            ]
            policy["default"] = "DENY"
        else:
            policy["rules"] = [
                {"order": 1, "effect": "ALLOW", "applicationId": "castRA1", "why": "field operation"},
                {"order": 2, "effect": "ALLOW", "casterIdentity": "A", "why": "known caster A; allow Greater Dispel operation after castF3 ended"},
            ]
            policy["default"] = "ALLOW"
        policy["revision"] += 1
        policy["editedAtSeconds"] = at + 0.01
        policy["editBy"] = "C"
        policy["actionSpent"] = True
        policy_id = f"RA316-POLICY-01-R{policy['revision']}"
        policy["id"] = policy_id
        app["policyId"] = policy_id
        s["fields"]["castRA1"]["policyId"] = policy_id
        s["supplement"]["realityAnchorWitness316"]["policyHistory"].append({"atSeconds": at + 0.01, "actor": "C", "action": "Action", "revision": policy["revision"], "default": policy["default"], "rules": copy.deepcopy(policy["rules"]), "noNewCastOrRP": True, "clockNotReset": True, "afterSourceTermination": after_termination})
        s["actors"]["C"]["Action"] = 0
        if allow_forge and not after_termination:
            item = s["items"]["bracelet-2"]
            item["imprintRoot"]["suppressed"] = False
            item["imprintRoot"].pop("suppressedBy", None)
            item["functionalState"] = "live imprint; policy permits currently eligible expressions"
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-C-POLICY-EDIT", "owner-action-policy-edit", at, at + 0.01,
              "Conscious operative Anchor owner C spends one Action within 100 feet of the perceived sigil to replace the complete Permission-mode policy; no new cast, RP cost or duration reset.", m,
              {"actor": "C", "cost": "Action", "newCast": False, "newRP": 0, "durationReset": False, "allowCastF3": allow_forge, "afterSourceTermination": after_termination})


def allowed_hide(branch: dict, event_number: int, after_termination: bool, time_s: float = 172824.5) -> None:
    def m(s):
        a = s["actors"]["A"]
        item = s["items"]["bracelet-2"]
        a["Action"] = 0
        if after_termination:
            assert item["imprintRoot"]["active"] is False and item["charges"] == 1
            result = {"timeSeconds": time_s, "actor": "A", "itemId": "bracelet-2", "sourceId": "castF3", "function": "eligible Hide / Stealth-family item expression", "decision": "NO_LIVE_SOURCE", "reason": "castF3 already ended by authorized Greater Dispel; policy now allows the exact former handle but no source resumes", "chargeBefore": 1, "chargeAfter": 1, "bonusApplied": 0, "advantageApplied": False}
            item["functionalState"] = "source ended; body remains; no magical function"
        else:
            assert item["imprintRoot"]["active"] is True and item["charges"] == 1 and item["imprintRoot"].get("suppressed") is False
            item["charges"] = 0
            item.setdefault("chargeTransactions", []).append({"timeSeconds": time_s, "kind": "spent", "reason": "eligible permitted Hide expression", "before": 1, "after": 0, "sourceId": "castF3"})
            result = {"timeSeconds": time_s, "actor": "A", "itemId": "bracelet-2", "sourceId": "castF3", "function": "eligible Hide / Stealth-family item expression", "decision": "ALLOWED_AND_RESOLVED", "chargeBefore": 1, "chargeAfter": 0, "bonusApplied": 1, "advantageApplied": True}
        s["supplement"]["realityAnchorWitness316"]["functionEvents"].append(result)
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-HIDE-AFTER-POLICY", "item-expression-after-policy-change", time_s - 0.09, time_s,
              "A takes the same otherwise eligible Hide action after C's policy edit; the trace distinguishes a resumed live imprint from an ended imprint whose former handle remains allowed.", m,
              {"actor": "A", "itemId": "bracelet-2", "applicationId": "castF3", "testInput": {"d20": 15, "authorship": "local finite test input; no external observation"}, "afterTermination": after_termination})


def terminate_forge(branch: dict, event_number: int, time_s: float = 172824.5) -> None:
    def m(s):
        a = s["actors"]["A"]
        item = s["items"]["bracelet-2"]
        assert a["Action"] == 1 and a["RP"] == 13 and a["Dissonance"] == 2
        assert item["imprintRoot"]["active"] and item["imprintRoot"].get("suppressed") is True
        a["Action"] = 0
        a["RP"] = 1
        a["lastSpell"] = "greater-dispel"
        a.setdefault("resourceHistory", []).append({"castId": "greaterDispelRA315", "spell": "greater-dispel", "time": time_s, "cost": 12, "action": "Action", "baseCost": 10, "preCastDissonance": 2, "RefrainAdded": 0, "firstFamily": False, "caster": "A", "turnCast": True})
        a["turnCast"] = True
        item["imprintRoot"]["active"] = False
        item["imprintRoot"]["suppressed"] = False
        item["imprintRoot"]["endReason"] = "actual-successful-greater-dispel-while-RA-denied"
        item["imprintRoot"]["endedAtSeconds"] = time_s
        item["revision"] += 1
        item["functionalState"] = "ended Forge imprint; mundane body persists"
        s.setdefault("terminalCasts", {})["greaterDispelRA315"] = {"caster": "A", "spell": "greater-dispel", "rank": 5, "paidRP": 12, "paidAction": "Action", "components": "V/S/F", "status": "resolved", "targetApplication": "castF3", "authorizationFrozen": {"centerFeet": [0, 3.2, 0.05], "capturedApplications": ["castF3"]}, "firstFamily": False, "preCastDissonance": 2, "RefrainAdded": 0}
        s["supplement"]["realityAnchorWitness316"]["imprintEndings"].append({"timeSeconds": time_s, "applicationId": "castF3", "physicalItemId": "bracelet-2", "method": "authorized successful Greater Dispel", "caster": "A", "DC": 28, "roll": {"d20": 17, "INT": 5, "PB": 6, "total": 28}, "RAStillDeniesCastF3AtResolution": True, "physicalBodyPreserved": True, "HP": item["HP"], "custody": item["custodian"], "charges": item["charges"], "contents": [], "resumed": False})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-PAID-GREATER-DISPEL", "paid-greater-dispel-terminates-denied-imprint", time_s - 0.09, time_s,
              "A pays 10-RP Greater Dispel plus 2 pre-cast Dissonance RP, spends an Action, targets only castF3, rolls 17+INT5+PB6=28 against DC28, and ends the imprint while Reality Anchor still denies that exact source.", m,
              {"caster": "A", "spellId": "greater-dispel", "castId": "greaterDispelRA315", "rank": 5, "targetApplication": "castF3", "preCastRP": 13, "baseCost": 10, "preCastDissonance": 2, "RefrainAdded": 0, "paidRP": 12, "postCastRP": 1, "action": "Action", "components": "V/S/F", "centerFeet": [0, 3.2, 0.05], "centerPerceived": True, "centerDistanceToTargetFeet": 0.25, "rangeFeet": 30, "radiusFeet": 30, "lineOfEffect": "unblocked", "immutableCapturedApplications": ["castF3"], "RAFieldCenterDistanceFeet": 75.06, "RAFieldNotCaptured": True, "targetGeneratingRank": 9, "d20": 17, "INT": 5, "PB": 6, "total": 28, "DC": 28, "DCFormula": "10+2*generating rank 9", "success": True, "policyRuleAdmittingOperation": "known caster identity A", "exactSourceStillDenied": True, "bodyHP": 5, "bodyCustodyUnchanged": True, "chargeUnchanged": 1, "sourceDeadline": None, "counterWindow": {"eligibleCounterers": [], "C": {"distanceFeet": 75, "reason": "outside accepted 60-foot Counterspell range"}, "B": {"distanceFeet": 5, "reason": "noncasting receiver; no Counterspell acquisition"}, "A": {"reason": "cannot counter own cast"}}})


def create_branches(endpoint: dict, actor_c: dict) -> dict:
    all_branches = []
    branch_specs = [
        ("WC188-B02-FORGE-SURVIVES", False),
        ("WC188-B02-FORGE-TERMINATES-WHILE-DENIED", True),
    ]
    for bid, terminating in branch_specs:
        b = {"id": bid, "description": "Independent continuation from exact accepted W2 endpoint; no events from sibling branch imported.", "baseState": copy.deepcopy(endpoint), "state": None, "events": []}
        add_case_common(b, actor_c, include_allow_a=terminating)
        cast_ra(b, f"RA316-{bid}-E02-PAID-REALITY-ANCHOR")
        if terminating:
            # Process every pre-existing due start in chronological order.
            regular_start(b, "B", 172812.2, 3)
            regular_end(b, "C", 172812.4, 4)
            regular_start(b, "A", 172812.4, 5)
            don_item(b, 6)
            regular_start(b, "C", 172812.6, 7)
            regular_end(b, "B", 172818.0, 8)
            regular_end(b, "A", 172818.2, 9)
            regular_start(b, "B", 172818.2, 10)
            regular_end(b, "C", 172818.4, 11)
            regular_start(b, "A", 172818.4, 12)
            denied_hide(b, 13)
            regular_start(b, "C", 172818.6, 14)
            regular_end(b, "B", 172824.0, 15)
            regular_end(b, "A", 172824.2, 16)
            regular_start(b, "B", 172824.2, 17)
            regular_end(b, "C", 172824.4, 18)
            regular_start(b, "A", 172824.4, 19)
            terminate_forge(b, 20, time_s=172824.5)
            regular_start(b, "C", 172824.6, 21)
            edit_policy(b, 22, allow_forge=False, at=172824.61, after_termination=True)
            regular_end(b, "B", 172830.0, 23)
            regular_end(b, "A", 172830.2, 24)
            regular_start(b, "B", 172830.2, 25)
            regular_end(b, "C", 172830.4, 26)
            regular_start(b, "A", 172830.4, 27)
            allowed_hide(b, 28, after_termination=True, time_s=172830.5)
        else:
            regular_start(b, "B", 172812.2, 3)
            regular_end(b, "C", 172812.4, 4)
            regular_start(b, "A", 172812.4, 5)
            don_item(b, 6)
            regular_start(b, "C", 172812.6, 7)
            regular_end(b, "B", 172818.0, 8)
            regular_end(b, "A", 172818.2, 9)
            regular_start(b, "B", 172818.2, 10)
            regular_end(b, "C", 172818.4, 11)
            regular_start(b, "A", 172818.4, 12)
            denied_hide(b, 13)
            regular_start(b, "C", 172818.6, 14)
            edit_policy(b, 15, allow_forge=True, at=172818.61)
            regular_end(b, "B", 172824.0, 16)
            regular_end(b, "A", 172824.2, 17)
            regular_start(b, "B", 172824.2, 18)
            regular_end(b, "C", 172824.4, 19)
            regular_start(b, "A", 172824.4, 20)
            allowed_hide(b, 21, after_termination=False)

        state = b["state"]
        final_sha = state_sha(state)
        exp = {
            "timeSeconds": state["time"],
            "anchorActive": state["applications"]["castRA1"]["status"] == "active",
            "anchorExpiresAtSeconds": state["applications"]["castRA1"]["endsAtSeconds"],
            "itemId": "bracelet-2",
            "itemHP": state["items"]["bracelet-2"]["HP"],
            "itemCustody": state["items"]["bracelet-2"]["custodian"],
            "itemCharges": state["items"]["bracelet-2"]["charges"],
            "forgeRootId": state["items"]["bracelet-2"]["imprintRoot"]["id"],
            "forgeRootActive": state["items"]["bracelet-2"]["imprintRoot"]["active"],
            "forgeNaturalExpiry": None,
            "actorARP": state["actors"]["A"]["RP"],
            "actorADissonance": state["actors"]["A"]["Dissonance"],
            "actorCRP": state["actors"]["C"]["RP"],
            "deniedExpressionCount": len(state["supplement"]["realityAnchorWitness316"]["deniedExpressions"]),
            "functionEvents": state["supplement"]["realityAnchorWitness316"].get("functionEvents", []),
            "imprintEndings": state["supplement"]["realityAnchorWitness316"]["imprintEndings"],
            "allRegularStartsThroughEndpointRecorded": True,
        }
        all_branches.append({
            "id": bid,
            "status": "DRAFT_NONCANONICAL_LOCAL_WITNESS_DIRECTOR_REVIEW_REQUIRED",
            "description": b["description"],
            "baseStateSHA256": state_sha(b["baseState"]),
            "baseState": b["baseState"],
            "events": b["events"],
            "finalStateSHA256": final_sha,
            "finalState": state,
            "expectedFinal": exp,
        })
    return {"branches": all_branches, "eventCount": sum(len(x["events"]) for x in all_branches)}


# Corrected Return315 lifecycle implementation. These overrides keep the original
# packet builder's evidence inventory and replace only its two RA witness branches.
def refresh_start(actor: dict, time_s: float, actor_id: str) -> None:
    assert math.isclose(float(actor.get("nextRegularStart")), time_s, abs_tol=1e-6), (actor_id, actor.get("nextRegularStart"), time_s)
    actor.update({"Action": 1, "BonusAction": 1, "Reaction": 1, "freeInteraction": 1, "movementRemaining": 30, "turnOpen": True})
    actor["turnCast"] = False
    actor.setdefault("regularStartsProcessed", []).append(time_s)
    actor["regularStart"] = time_s
    actor["nextRegularStart"] = round(time_s + 6, 1)
    actor["nextRegularEnd"] = round(time_s + 5.8, 1)


def cast_ra(branch: dict, event_id: str) -> None:
    def mutate(s):
        c, item = s["actors"]["C"], s["items"]["bracelet-2"]
        root = item["imprintRoot"]
        assert c["Action"] == 1 and c["RP"] == 68 and root["active"] is True
        c["Action"], c["RP"], c["lastSpell"], c["turnCast"] = 0, 42, TARGET, True
        c["usedPreparedFamilies"].append(TARGET)
        c["concentration"] = {"applicationId": "castRA1", "spell": TARGET, "endsAtSeconds": 172866.7, "maintained": True}
        c.setdefault("resourceHistory", []).append({"castId": "castRA1", "spell": TARGET, "time": 172806.7, "cost": 26, "action": "Action", "components": "V/S/F", "preCastDissonance": 0, "RefrainAdded": 0, "firstFamily": True, "DissonanceAfter": 0, "turnCast": True})
        s["applications"]["castRA1"] = {"id": "castRA1", "spellId": TARGET, "caster": "C", "class": "Wizard", "classLevel": 18, "generatingSchool": "Abjuration", "generatingRank": 9, "paidRP": 26, "costAdjustments": {"preCastDissonance": 0, "RefrainAdded": 0}, "components": "V/S/F", "originFeet": [75, 0, 0], "centerFeet": [75, 0, 0], "rangeFeet": 100, "radiusFeet": 100, "mode": "Permission", "policyId": "RA316-POLICY-01", "establishedAtSeconds": 172806.7, "endsAtSeconds": 172866.7, "maintainer": "C", "concentration": True, "status": "active", "totalCoverClipped": False}
        rules = copy.deepcopy(s["supplement"]["realityAnchorWitness316"]["policyHistory"][-1]["predeclaredRules"])
        s["applications"]["castRA1"]["policy"] = {"id": "RA316-POLICY-01", "revision": 0, "mode": "Permission", "default": "DENY", "rules": rules, "firstMatchWins": True}
        s["fields"]["castRA1"] = {"sourceId": "castRA1", "centerFeet": [75, 0, 0], "radiusFeet": 100, "policyId": "RA316-POLICY-01", "expiresAtSeconds": 172866.7, "owner": "C", "status": "active"}
        root["suppressed"], root["suppressedBy"] = True, ["castRA1"]
        root.setdefault("suppressionHistory", []).append({"timeSeconds": 172806.7, "fieldId": "castRA1", "policyId": "RA316-POLICY-01", "decision": "SUPPRESSED", "applicationId": "castF3", "bodyAndHistoryPersist": True})
        item["functionalState"] = "item magical expression immediately denied; physical body persists"
        w = s["supplement"]["realityAnchorWitness316"]
        w.setdefault("suppressionEvents", []).append({"timeSeconds": 172806.7, "fieldId": "castRA1", "applicationId": "castF3", "active": True, "suppressed": True, "chargeBefore": item["charges"], "chargeAfter": item["charges"], "HPBefore": item["HP"], "HPAfter": item["HP"], "custodyBefore": item["custodian"], "custodyAfter": item["custodian"], "sourceDeadline": None})
    add_event(branch, event_id, "paid-reality-anchor-cast-and-establishment", 172806.65, 172806.7,
        "C pays 26 RP and one Action to establish Permission-mode Reality Anchor. Its default-deny policy immediately suppresses the already-active castF3 imprint; the physical body, charge, custody and source deadline remain unchanged.", mutate,
        {"caster": "C", "spellId": TARGET, "castId": "castRA1", "costRP": 26, "preCastRP": 68, "postCastRP": 42, "action": "Action", "components": "V/S/F", "mode": "Permission", "defaultPolicy": "DENY", "centerFeet": [75, 0, 0], "radiusFeet": 100, "expiresAtSeconds": 172866.7, "immediatelySuppressedApplications": ["castF3"], "bodyChargeCustodyUnchanged": True, "counterWindow": {"eligibleCounterers": [], "A": {"distanceFeet": 75, "reason": "outside accepted 60-foot Counterspell range"}, "B": {"distanceFeet": 70, "reason": "noncasting receiver; no Counterspell acquisition"}, "C": {"reason": "cannot counter own cast"}}})


def regular_start(branch: dict, actor_id: str, time_s: float, event_number: int) -> None:
    prior = {}
    def mutate(s):
        a = s["actors"][actor_id]
        prior["turnCast"] = a.get("turnCast", False)
        refresh_start(a, time_s, actor_id)
        s["supplement"]["realityAnchorWitness316"]["dueClockEvents"].append({"kind": "regular-start", "actor": actor_id, "timeSeconds": time_s, "budgetRefreshed": True, "Action": 1, "Reaction": 1, "BonusAction": 1, "freeInteraction": 1, "movementRemaining": 30, "turnCastReset": True, "priorTurnCast": prior["turnCast"]})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-{actor_id}-START", "regular-start", time_s, time_s,
        f"Process {actor_id}'s due regular start once; refresh turn-local budgets and reset the per-turn cast flag.", mutate,
        {"actor": actor_id, "ActionAfter": 1, "ReactionAfter": 1, "turnCastBeforeReset": prior.get("turnCast"), "turnCastAfter": False, "sourceSchedulePreserved": True})


def regular_end(branch: dict, actor_id: str, time_s: float, event_number: int) -> None:
    result = {}
    def mutate(s):
        a = s["actors"][actor_id]
        assert a.get("turnOpen") is True and math.isclose(float(a.get("nextRegularEnd")), time_s, abs_tol=1e-6), (actor_id, a.get("nextRegularEnd"), time_s)
        cast, diss = a.get("turnCast", False), a.get("Dissonance", 0)
        vent = 0 if cast else min(1, diss)
        a["Dissonance"] = diss - vent
        a["Action"] = a["BonusAction"] = a["freeInteraction"] = a["movementRemaining"] = 0
        result.update({"turnCast": cast, "dissonanceBefore": diss, "dissonanceVented": vent, "dissonanceAfter": a["Dissonance"], "ReactionAfter": a["Reaction"]})
        a["turnOpen"] = False
        a["nextRegularEnd"] = None
        a.setdefault("regularEndsProcessed", []).append(time_s)
        s["supplement"]["realityAnchorWitness316"]["dueClockEvents"].append({"kind": "regular-end", "actor": actor_id, "timeSeconds": time_s, "turnClosed": True, "turnCast": cast, "dissonanceVented": vent, "ActionAfter": 0, "BonusActionAfter": 0, "freeInteractionAfter": 0, "movementRemainingAfter": 0, "ReactionCarried": a["Reaction"], "nextRegularEndAfter": None})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-{actor_id}-END", "regular-end", time_s, time_s,
        f"Close {actor_id}'s due turn. Vent one Dissonance only if the actor used no spell or magical class ability; expire local budgets and carry Reaction.", mutate,
        {"actor": actor_id, "turnClosed": True, "sourceDeadlineUnchanged": True, "endResult": result})


def don_item(branch: dict, event_number: int) -> None:
    bounds = [[0, 3, 0], [0.4, 3.4, 0.1]]
    def mutate(s):
        a, item = s["actors"]["A"], s["items"]["bracelet-2"]
        assert a["Action"] == 1 and item["imprintRoot"]["active"] and item["imprintRoot"]["suppressed"]
        a["Action"] = 0
        item.update({"custodian": "A-left-wrist", "worn": True, "positionBoxFeet": [0, 3, 0], "wornBodyBoundsFeet": copy.deepcopy(bounds), "wearer": "A"})
        item["revision"] += 1
        item["wearFixture"] = {"wearer": "A", "site": "left wrist", "fit": "local bounded test fixture; no global size claim", "wristOpen": True, "bodyBoundsFeet": copy.deepcopy(bounds)}
        a.setdefault("worn", []).append("bracelet-2")
        w = s["supplement"]["realityAnchorWitness316"]
        w["scene"]["itemBodyBoxFeet"] = copy.deepcopy(bounds)
        w["scene"]["wristBoundsFeet"] = copy.deepcopy(bounds)
        w["custodyHistory"] = [{"timeSeconds": 172812.5, "itemId": "bracelet-2", "owner": "A", "from": "A-floor-within-5ft", "to": "A-left-wrist", "cost": "A Action", "consent": True, "bodyBoundsFeet": copy.deepcopy(bounds)}]
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-DON-BRACELET2", "lawful-wear", 172812.41, 172812.5,
        "A spends an Action to don bracelet-2 and records its actual bounded wrist/body geometry for later capture and line-of-effect checks.", mutate,
        {"actor": "A", "itemId": "bracelet-2", "cost": "Action", "ownerUnchanged": True, "custodyAfter": "A-left-wrist", "actualWornBodyBoundsFeet": bounds, "HP": 5, "charges": 1, "imprintRemainsSuppressed": True})


def denied_hide(branch: dict, event_number: int, time_s: float = 172818.5) -> None:
    outcome = {"observer": "C", "visibilityEligibility": "partial cover blocks clear view; local fixture permits Hide", "d20": 8, "DEXModifier": 2, "StealthProficiency": False, "itemBonus": 0, "advantage": False, "total": 10, "passivePerception": 11, "margin": -1, "degree": "failure", "hiddenFromC": False, "sourceDecision": "DENIED", "chargeBefore": 1, "chargeAfter": 1, "itemBonusApplied": 0, "advantageApplied": False, "observerProfile": "ACTOR_PROFILES.json#/W219", "observerWIS": 12, "observerPerceptionProficiency": False, "observerPassiveFormula": "10 + WIS modifier (+1); no Perception proficiency recorded"}
    def mutate(s):
        a, item = s["actors"]["A"], s["items"]["bracelet-2"]
        assert a["Action"] == 1 and item["charges"] == 1 and item["imprintRoot"]["suppressed"]
        a["Action"] = 0
        w = s["supplement"]["realityAnchorWitness316"]
        w.setdefault("hideOutcomes", []).append({"timeSeconds": time_s, **outcome})
        w["deniedExpressions"].append({"timeSeconds": time_s, "actor": "A", "itemId": "bracelet-2", "sourceId": "castF3", "function": "eligible Hide / Stealth-family item expression", "decision": "DENIED", "reason": "first matching exact castF3 policy", "underlyingSourceRetained": item["imprintRoot"]["active"], "chargeBefore": 1, "chargeAfter": 1, "bonusApplied": 0, "advantageApplied": False, "actionContinuesWithoutItemExpression": True})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-HIDE-DENIED", "permission-denial-of-item-expression", time_s - 0.09, time_s,
        "A's Hide action resolves as an ordinary DEX (Stealth) check while Anchor denies castF3's item expression; no charge, bonus or advantage applies.", mutate,
        {"actor": "A", "itemId": "bracelet-2", "applicationId": "castF3", "policyId": "RA316-POLICY-01", "decision": "DENIED", "recordedHideOutcome": outcome})


def move_to_new_hiding_position(branch: dict, event_number: int, time_s: float = 172818.55) -> None:
    bounds = [[0, 8, 0], [0.4, 8.4, 0.1]]
    def mutate(s):
        a, item = s["actors"]["A"], s["items"]["bracelet-2"]
        assert a["movementRemaining"] >= 5 and a["positionFeet"] == [0, 0, 0]
        a["movementRemaining"] -= 5
        a["positionFeet"] = [0, 5, 0]
        item["positionBoxFeet"], item["wornBodyBoundsFeet"] = [0, 8, 0], copy.deepcopy(bounds)
        item["wearFixture"]["bodyBoundsFeet"] = copy.deepcopy(bounds)
        w = s["supplement"]["realityAnchorWitness316"]
        w["scene"].update({"Afeet": [0, 5, 0], "itemBodyBoxFeet": copy.deepcopy(bounds), "wristBoundsFeet": copy.deepcopy(bounds), "hideOpportunity": {"cover": "partial opaque screen at new position", "clearSightBlockedFor": ["C"], "BScreened": True, "lineOfEffectToBracelet": "unblocked", "changedCircumstance": "A moved 5 feet after the failed Hide check"}})
        w.setdefault("movementHistory", []).append({"timeSeconds": time_s, "actor": "A", "fromFeet": [0, 0, 0], "toFeet": [0, 5, 0], "movementFeet": 5, "newHidingPosition": True, "itemBodyBoundsFeet": copy.deepcopy(bounds)})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-MOVE-NEW-HIDE-POSITION", "ordinary-movement-changed-hide-circumstance", time_s - 0.05, time_s,
        "After the failed Hide, A uses 5 feet of ordinary movement to reach a distinct position behind partial cover, changing the circumstances for a later check.", mutate,
        {"actor": "A", "movementFeet": 5, "fromFeet": [0, 0, 0], "toFeet": [0, 5, 0], "changedCircumstance": True, "actualWornBodyBoundsFeetAfterMove": bounds, "lineOfEffectToItem": "unblocked"})


def edit_policy(branch: dict, event_number: int, allow_forge: bool, at: float, after_termination: bool = False) -> None:
    def mutate(s):
        app, w = s["applications"]["castRA1"], s["supplement"]["realityAnchorWitness316"]
        policy = app["policy"]
        if allow_forge:
            policy["rules"] = [{"order": 1, "effect": "ALLOW", "applicationId": "castF3", "why": "owner's actual Action policy edit"}, {"order": 2, "effect": "ALLOW", "applicationId": "castRA1", "why": "field operation"}]
            policy["default"] = "DENY"
        else:
            policy["rules"] = [{"order": 1, "effect": "ALLOW", "applicationId": "castRA1", "why": "field operation"}, {"order": 2, "effect": "ALLOW", "casterIdentity": "A", "why": "known caster A; allow Greater Dispel operation"}]
            policy["default"] = "ALLOW"
        policy["revision"] += 1
        policy["editedAtSeconds"], policy["editBy"], policy["actionSpent"] = at + 0.01, "C", True
        pid = f"RA316-POLICY-01-R{policy['revision']}"
        policy["id"], app["policyId"], s["fields"]["castRA1"]["policyId"] = pid, pid, pid
        w["policyHistory"].append({"atSeconds": at + 0.01, "actor": "C", "action": "Action", "revision": policy["revision"], "default": policy["default"], "rules": copy.deepcopy(policy["rules"]), "noNewCastOrRP": True, "clockNotReset": True, "afterSourceTermination": after_termination})
        s["actors"]["C"]["Action"] = 0
        if allow_forge and not after_termination:
            item, root = s["items"]["bracelet-2"], s["items"]["bracelet-2"]["imprintRoot"]
            assert root["active"]
            root["suppressed"] = False
            root.pop("suppressedBy", None)
            root.setdefault("suppressionHistory", []).append({"timeSeconds": at + 0.01, "fieldId": "castRA1", "applicationId": "castF3", "decision": "RESUMED_PERMITTED", "bodyAndChargePersist": True})
            item["functionalState"] = "live imprint; policy permits currently eligible expressions"
            w.setdefault("suppressionEvents", []).append({"timeSeconds": at + 0.01, "fieldId": "castRA1", "applicationId": "castF3", "active": True, "suppressed": False, "charge": item["charges"], "HP": item["HP"]})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-C-POLICY-EDIT", "owner-action-policy-edit", at, at + 0.01,
        "C spends an Action to replace the complete Permission-mode policy; no new cast, RP payment or duration reset occurs.", mutate,
        {"actor": "C", "cost": "Action", "newCast": False, "newRP": 0, "durationReset": False, "allowCastF3": allow_forge, "afterSourceTermination": after_termination})


def resolve_hide(branch: dict, event_number: int, after_termination: bool, time_s: float) -> None:
    outcome = {}
    def mutate(s):
        a, item = s["actors"]["A"], s["items"]["bracelet-2"]
        assert a["Action"] == 1
        a["Action"] = 0
        if after_termination:
            assert not item["imprintRoot"]["active"] and item["charges"] == 1
            decision, faces, selected, bonus, adv, charge_after = "NO_LIVE_SOURCE", [8], 8, 0, False, 1
            item["functionalState"] = "source ended; body remains; no magical function"
        else:
            assert item["imprintRoot"]["active"] and item["charges"] == 1 and not item["imprintRoot"].get("suppressed")
            # Spend the extant charge before rolling the advantaged check.
            item["charges"] = 0
            item.setdefault("chargeTransactions", []).append({"timeSeconds": time_s, "kind": "spent", "reason": "permitted charged Hide expression; committed before roll", "before": 1, "after": 0, "sourceId": "castF3", "committedBeforeRoll": True})
            decision, faces, selected, bonus, adv, charge_after = "ALLOWED_AND_RESOLVED", [15, 8], 15, 1, True, 0
            item["functionalState"] = "live imprint; permitted charged expression resolved"
        total = selected + 2 + bonus
        degree = "success" if total >= 11 else "failure"
        outcome.update({"observer": "C", "visibilityEligibility": "partial cover blocks clear view; local fixture permits Hide", "dice": {"faces": faces, "selected": selected, "mode": "advantage" if adv else "ordinary", "selectionRule": "higher face" if adv else None}, "DEXModifier": 2, "StealthProficiency": False, "itemBonus": bonus, "advantage": adv, "total": total, "passivePerception": 11, "margin": total - 11, "degree": degree, "hiddenFromC": degree in ("success", "critical success"), "sourceDecision": decision, "chargeBefore": 1, "chargeAfter": charge_after, "chargeCommittedBeforeRoll": not after_termination, "itemBonusApplied": bonus, "advantageApplied": adv, "observerProfile": "ACTOR_PROFILES.json#/W219", "observerWIS": 12, "observerPerceptionProficiency": False, "observerPassiveFormula": "10 + WIS modifier (+1); no Perception proficiency recorded", "changedCircumstanceFromPriorFailure": True, "actualItemBodyBoundsFeet": copy.deepcopy(item.get("wornBodyBoundsFeet")), "lineOfEffectToItem": "unblocked"})
        w = s["supplement"]["realityAnchorWitness316"]
        w.setdefault("hideOutcomes", []).append({"timeSeconds": time_s, **outcome})
        w["functionEvents"].append({"timeSeconds": time_s, "actor": "A", "itemId": "bracelet-2", "sourceId": "castF3", "function": "eligible Hide / Stealth-family item expression", "decision": decision, "chargeBefore": 1, "chargeAfter": charge_after, "bonusApplied": bonus, "advantageApplied": adv})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-A-HIDE-RESOLVED", "item-expression-hide-check-resolution", time_s - 0.09, time_s,
        "Resolve the later Hide after A changed position: record observer, source decision, dice, total, Core degree and charge ordering.", mutate,
        {"actor": "A", "itemId": "bracelet-2", "applicationId": "castF3", "testInput": outcome, "afterTermination": after_termination})


def terminate_forge(branch: dict, event_number: int, time_s: float = 172824.5) -> None:
    center = [0.2, 8.2, 0.05]
    field_distance = math.dist(center, [75, 0, 0])
    capture = ["castF3", "castRA1"]
    checks = [
        {"applicationId": "castF3", "generatingRank": 9, "DC": 28, "d20": 17, "ability": "INT", "abilityModifier": 5, "proficiencyBonus": 6, "total": 28, "success": True, "ending": "imprint castF3"},
        {"applicationId": "castRA1", "generatingRank": 9, "DC": 28, "d20": 16, "ability": "INT", "abilityModifier": 5, "proficiencyBonus": 6, "total": 27, "success": False, "ending": "none"},
    ]
    def mutate(s):
        a, item = s["actors"]["A"], s["items"]["bracelet-2"]
        root = item["imprintRoot"]
        assert a["Action"] == 1 and a["RP"] == 13 and a["Dissonance"] == 0
        assert root["active"] and root.get("suppressed") and root.get("suppressedBy") == ["castRA1"]
        a["Action"], a["RP"], a["lastSpell"], a["turnCast"], a["Dissonance"] = 0, 3, "greater-dispel", True, 1
        if "greater-dispel" not in a["usedPreparedFamilies"]:
            a["usedPreparedFamilies"].append("greater-dispel")
        a.setdefault("resourceHistory", []).append({"castId": "greaterDispelRA316", "spell": "greater-dispel", "time": time_s, "cost": 10, "action": "Action", "baseRP": 10, "preCastDissonance": 0, "baseDissonance": 1, "RefrainAdded": 0, "firstFamily": False, "caster": "A", "turnCast": True, "DissonanceAfter": 1})
        root.update({"active": False, "suppressed": False, "endReason": "actual-successful-greater-dispel-while-RA-denied", "endedAtSeconds": time_s})
        root.pop("suppressedBy", None)
        root.setdefault("suppressionHistory", []).append({"timeSeconds": time_s, "fieldId": "castRA1", "applicationId": "castF3", "decision": "TERMINATED_SOURCE_NO_LONGER_LIVE_SUPPRESSION", "historicalProvenanceRetained": True})
        item["revision"] += 1
        item["functionalState"] = "ended Forge imprint; mundane body persists"
        s.setdefault("terminalCasts", {})["greaterDispelRA316"] = {"caster": "A", "spell": "greater-dispel", "rank": 5, "baseRP": 10, "paidRP": 10, "paidAction": "Action", "components": "V/S/F", "status": "resolved", "targetApplication": "castF3", "authorizationFrozen": {"centerFeet": center, "capturedApplications": capture, "captureOrder": "castF3 then castRA1", "checks": checks, "RAAreaIntersectsDispelSphere": True}, "firstFamily": False, "preCastDissonance": 0, "baseDissonance": 1, "RefrainAdded": 0}
        w = s["supplement"]["realityAnchorWitness316"]
        w["imprintEndings"].append({"timeSeconds": time_s, "applicationId": "castF3", "physicalItemId": "bracelet-2", "method": "authorized successful Greater Dispel", "caster": "A", "checks": checks, "immutableCapturedApplications": capture, "RAFieldCenterDistanceFeet": field_distance, "RAFieldRadiusFeet": 100, "dispelRadiusFeet": 30, "RAFieldAreaOverlapIncluded": True, "RAStillDeniesCastF3AtResolution": True, "castRA1RemainsActive": True, "castRA1ConcentrationRemains": copy.deepcopy(s["actors"]["C"]["concentration"]), "physicalBodyPreserved": True, "HP": item["HP"], "custody": item["custodian"], "wornBodyBoundsFeet": copy.deepcopy(item["wornBodyBoundsFeet"]), "charges": item["charges"], "contents": [], "suppressionProvenanceRetained": True, "staleLiveSuppressionRelationRemoved": True, "resumed": False})
    add_event(branch, f"RA316-{branch['id']}-E{event_number:02d}-PAID-GREATER-DISPEL", "paid-greater-dispel-terminates-denied-imprint", time_s - 0.09, time_s,
        "A pays 10 RP at Dissonance 0. Immutable area capture includes castF3 and overlapping castRA1; the castF3 check succeeds at 28, while the separate Anchor check fails at 27. The denied imprint ends; castRA1 and C's concentration remain active.",
        mutate, {"caster": "A", "spellId": "greater-dispel", "castId": "greaterDispelRA316", "targetApplication": "castF3", "preCastRP": 13, "baseRP": 10, "preCastDissonance": 0, "baseDissonance": 1, "RefrainAdded": 0, "firstFamily": False, "paidRP": 10, "postCastRP": 3, "dissonanceAfter": 1, "action": "Action", "components": "V/S/F", "centerFeet": center, "centerPerceived": True, "centerDistanceToTargetFeet": 0.2, "rangeFeet": 30, "radiusFeet": 30, "lineOfEffect": "unblocked to actual worn-item bounds", "immutableCapturedApplications": capture, "captureOrder": capture, "RAFieldCenterDistanceFeet": field_distance, "RAFieldRadiusFeet": 100, "RAFieldAreaOverlapIncluded": True, "targetChecks": checks, "DCFormula": "10+2*generating rank 9", "success": True, "policyRuleAdmittingOperation": "known caster identity A; castF3 expression remains denied", "exactSourceStillDenied": True, "bodyHP": 5, "bodyCustodyUnchanged": True, "actualWornBodyBoundsFeet": [[0, 8, 0], [0.4, 8.4, 0.1]], "chargeUnchanged": 1, "sourceDeadline": None, "counterWindow": {"eligibleCounterers": [], "C": {"distanceFeet": 75, "reason": "outside accepted 60-foot Counterspell range"}, "B": {"distanceFeet": 7.07, "reason": "noncasting receiver; no Counterspell acquisition"}, "A": {"reason": "cannot counter own cast"}}})


def create_branches(endpoint: dict, actor_c: dict) -> dict:
    branches = []
    for bid, terminating in [("WC188-B02-FORGE-SURVIVES", False), ("WC188-B02-FORGE-TERMINATES-WHILE-DENIED", True)]:
        b = {"id": bid, "description": "Independent continuation from exact accepted W2 endpoint; no events from sibling branch imported.", "baseState": copy.deepcopy(endpoint), "state": None, "events": []}
        add_case_common(b, actor_c, include_allow_a=terminating)
        cast_ra(b, f"RA316-{bid}-E02-PAID-REALITY-ANCHOR")
        n = 3
        regular_end(b, "B", 172812.0, n); n += 1
        regular_end(b, "A", 172812.2, n); n += 1
        regular_start(b, "B", 172812.2, n); n += 1
        regular_end(b, "C", 172812.4, n); n += 1
        regular_start(b, "A", 172812.4, n); n += 1
        don_item(b, n); n += 1
        regular_start(b, "C", 172812.6, n); n += 1
        regular_end(b, "B", 172818.0, n); n += 1
        regular_end(b, "A", 172818.2, n); n += 1
        regular_start(b, "B", 172818.2, n); n += 1
        regular_end(b, "C", 172818.4, n); n += 1
        regular_start(b, "A", 172818.4, n); n += 1
        denied_hide(b, n, 172818.5); n += 1
        move_to_new_hiding_position(b, n, 172818.55); n += 1
        regular_start(b, "C", 172818.6, n); n += 1
        if terminating:
            regular_end(b, "B", 172824.0, n); n += 1
            regular_end(b, "A", 172824.2, n); n += 1
            regular_start(b, "B", 172824.2, n); n += 1
            regular_end(b, "C", 172824.4, n); n += 1
            regular_start(b, "A", 172824.4, n); n += 1
            terminate_forge(b, n, 172824.5); n += 1
            regular_start(b, "C", 172824.6, n); n += 1
            edit_policy(b, n, False, 172824.61, after_termination=True); n += 1
            regular_end(b, "B", 172830.0, n); n += 1
            regular_end(b, "A", 172830.2, n); n += 1
            regular_start(b, "B", 172830.2, n); n += 1
            regular_end(b, "C", 172830.4, n); n += 1
            regular_start(b, "A", 172830.4, n); n += 1
            resolve_hide(b, n, True, 172830.5); n += 1
        else:
            edit_policy(b, n, True, 172818.61); n += 1
            regular_end(b, "B", 172824.0, n); n += 1
            regular_end(b, "A", 172824.2, n); n += 1
            regular_start(b, "B", 172824.2, n); n += 1
            regular_end(b, "C", 172824.4, n); n += 1
            regular_start(b, "A", 172824.4, n); n += 1
            resolve_hide(b, n, False, 172824.5); n += 1
        state = b["state"]
        w = state["supplement"]["realityAnchorWitness316"]
        expected = {"timeSeconds": state["time"], "anchorActive": True, "anchorExpiresAtSeconds": 172866.7, "itemId": "bracelet-2", "itemHP": state["items"]["bracelet-2"]["HP"], "itemCustody": state["items"]["bracelet-2"]["custodian"], "itemCharges": state["items"]["bracelet-2"]["charges"], "forgeRootId": "castF3", "forgeRootActive": state["items"]["bracelet-2"]["imprintRoot"]["active"], "forgeNaturalExpiry": None, "actorARP": state["actors"]["A"]["RP"], "actorADissonance": state["actors"]["A"]["Dissonance"], "actorCRP": state["actors"]["C"]["RP"], "deniedExpressionCount": len(w["deniedExpressions"]), "functionEvents": w["functionEvents"], "imprintEndings": w["imprintEndings"], "hideOutcomes": w["hideOutcomes"], "allRegularStartsAndEndsThroughEndpointRecorded": True}
        branches.append({"id": bid, "status": "DRAFT_NONCANONICAL_LOCAL_WITNESS_DIRECTOR_REVIEW_REQUIRED", "description": b["description"], "baseStateSHA256": state_sha(b["baseState"]), "baseState": b["baseState"], "events": b["events"], "finalStateSHA256": state_sha(state), "finalState": state, "expectedFinal": expected})
    return {"branches": branches, "eventCount": sum(len(x["events"]) for x in branches)}


def main() -> None:
    assert not OUT.exists(), f"Refusing to overwrite existing preparation directory: {OUT}"
    OUT.mkdir(parents=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    branch_name = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    base_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index_now, catalog_now = json.loads(index_raw), json.loads(catalog_raw)
    pending_ids = sorted(r["id"] for r in index_now["entries"] if r.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending_ids) == 26 and TARGET in pending_ids
    assert len([x for x in catalog_now["spells"] if x["id"] == TARGET]) == 1

    with zipfile.ZipFile(SOURCE312) as source_zip:
        previous_refresh_raw = source_zip.read("SOURCE_REFRESH_312.json")
        previous_refresh = json.loads(previous_refresh_raw)
        old_wave_extra_raw = source_zip.read("WAVE_SOURCE_EXTRA_BINDINGS_312.json")
        source_rows = previous_refresh["currentBindings"]
        assert len(source_rows) == 91
        source_payload = {}
        old_bindings = []
        current_bindings = []
        changed = []
        for row in source_rows:
            p = ROOT / pathlib.Path(row["path"])
            raw = p.read_bytes()
            packed = source_zip.read("sources_current/" + row["path"])
            assert digest(packed)["bytes"] == row["bytes"] and sha(packed) == row["sha256"], row["path"]
            old = {"path": row["path"], **digest(packed)}
            cur = {"path": row["path"], **digest(raw)}
            old_bindings.append(old)
            current_bindings.append(cur)
            if raw != packed:
                changed.append({"path": row["path"], "previousPacket312": digest(packed), "currentWorktree": digest(raw)})
            source_payload["sources_current/" + row["path"]] = raw

    extra_paths = {
        "source/eternal-forge/MODEL.json": FORGE_DIR / "MODEL.json",
        "source/eternal-forge/EXACT_ACCEPTANCE.json": FORGE_DIR / "EXACT_ACCEPTANCE.json",
        "source/eternal-forge/DIRECTOR_ACCEPTANCE.json": FORGE_DIR / "DIRECTOR_ACCEPTANCE.json",
        "source/eternal-forge/SUPPLEMENT255_W2.json": FORGE_DIR / "SUPPLEMENT255_W2.json",
        "source/eternal-forge/SUPPLEMENT255_INDEPENDENT_AUDIT.json": FORGE_DIR / "SUPPLEMENT255_INDEPENDENT_AUDIT.json",
        "evidence/ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json": FORGE_AUDIT / "ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json",
        "evidence/ETERNAL_FORGE_DIRECTOR_ACCEPTANCE_255.json": FORGE_AUDIT / "ETERNAL_FORGE_DIRECTOR_ACCEPTANCE_255.json",
        "evidence/ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_255.json": FORGE_AUDIT / "ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_255.json",
        "evidence/ETERNAL_FORGE_MF210_B01_SUPPLEMENT_255_INDEPENDENT_AUDIT.json": FORGE_AUDIT / "ETERNAL_FORGE_MF210_B01_SUPPLEMENT_255_INDEPENDENT_AUDIT.json",
        "authority/CURRENT_SPELL_QUEUE_315.json": QUEUE314,
        "authority/CURRENT_HANDOFF_315.json": HANDOFF314,
        "authority/CURRENT26_PENDING_IDENTITY_AUDIT_315.json": AUDIT312,
        "authority/authored_review_index.json": INDEX,
        "authority/catalog.json": CATALOG,
        "authority/Return281_INDEPENDENT_AUDIT.json": RETURN281_AUDIT,
        "authority/Return281_DELIVERY.json": RETURN281_DELIVERY,
        "authority/Return281_ARCHIVE.zip": RETURN281,
        "authority/Return312_NULLIFICATION_WAVE_HOLD_RECEIPT.json": A / "NULLIFICATION_WAVE_HOLD_RECEIPT_312.json",
        "authority/Return312_NULLIFICATION_WAVE_DECISION.json": A / "NULLIFICATION_WAVE_DIRECTOR_DECISION_312.json",
        "authority/Return315_ARCHIVE.zip": RETURN315,
        "authority/Return315_DELIVERY.json": RETURN315_DELIVERY,
        "authority/Return315_INDEPENDENT_AUDIT.json": RETURN315_AUDIT,
        "authority/Packet315_INDEPENDENT_AUDIT.json": A / "REALITY_ANCHOR_PACKET_315_INDEPENDENT_AUDIT.json",
        "authority/Packet315_SUBMISSION_RECEIPT.json": A / "REALITY_ANCHOR_PACKET_315_SUBMISSION_RECEIPT.json",
        "authority/Return315_RECEIPT.json": A / "REALITY_ANCHOR_RETURN315_RECEIPT.json",
    }
    extra_payload = {member: path.read_bytes() for member, path in extra_paths.items()}
    with zipfile.ZipFile(RETURN315) as return315_zip:
        for source_member, packet_member in [("CORRECTION_SHEET.json", "authority/Return315_CORRECTION_SHEET.json"), ("A_EVENT_CORRECTION_LEDGER.json", "authority/Return315_A_EVENT_CORRECTION_LEDGER.json"), ("DIRECTOR_DECISION.json", "authority/Return315_DIRECTOR_DECISION.json"), ("DATA_VALIDATION.json", "authority/Return315_DATA_VALIDATION.json")]:
            extra_payload[packet_member] = return315_zip.read(source_member)
    extra_payload["authority/SOURCE_REFRESH_312.json"] = previous_refresh_raw
    extra_payload["authority/WAVE_SOURCE_EXTRA_BINDINGS_312.json"] = old_wave_extra_raw
    extra_bindings = [{"member": member, **bind(path, extra_payload[member], member)} for member, path in extra_paths.items()]
    extra_bindings.extend([
        {"member": "authority/SOURCE_REFRESH_312.json", "path": SOURCE312.relative_to(ROOT).as_posix(), "sourceMember": "SOURCE_REFRESH_312.json", **digest(previous_refresh_raw)},
        {"member": "authority/WAVE_SOURCE_EXTRA_BINDINGS_312.json", "path": SOURCE312.relative_to(ROOT).as_posix(), "sourceMember": "WAVE_SOURCE_EXTRA_BINDINGS_312.json", **digest(old_wave_extra_raw)},
    ])
    source_refresh = {
        "id": "REALITY-ANCHOR-91-SOURCE-REFRESH-316",
        "recordedAtUtc": now,
        "previousSourceInventory": {"path": SOURCE312.relative_to(ROOT).as_posix(), "member": "SOURCE_REFRESH_312.json", **digest(previous_refresh_raw)},
        "sourceCount": 91,
        "previousBindings": old_bindings,
        "currentBindings": current_bindings,
        "changedSincePacket312": changed,
        "all91RefreshedFromCurrentWorktree": True,
        "sourceFilesExecuted": False,
    }

    endpoint, w2 = make_w2_endpoint()
    with zipfile.ZipFile(RETURN281) as rz:
        case_index = json.loads(rz.read("CASE_INDEX.json"))
        ra_rows = [r for r in case_index["cases"] if r.get("spellId") == TARGET]
        assert len(ra_rows) == 14
        history_names = [
            "ACTOR_PROFILES.json", "BLOCKERS.json", "QUALIFICATIONS.json", "SOURCE_PAIR_TABLE.json",
            "ORIGINAL_OBLIGATIONS.json", "QUESTION_DISPOSITIONS.json", "HOLD_REGISTER.json", "REMAINING_QUEUE.json",
            "CASE_INDEX.json", "procedures/reality-anchor.json",
        ]
        history_payload = {"history/Return281/" + name: rz.read(name) for name in history_names}
        for row in ra_rows:
            history_payload["history/Return281/" + row["path"]] = rz.read(row["path"])
        actor_c = make_actor_c(rz, endpoint["actors"]["A"])
    witnesses = create_branches(endpoint, actor_c)
    next_order = [
        "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy",
        "faction-omniscience-supreme", "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar",
        "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension",
        "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection",
        "imprisonment", "divine-intervention-greater", "wish",
    ]
    assert next_order[1:] == read_json(QUEUE314)["continuingPriorityOrder"][1:]

    prep = {
        "id": "RANK9-WARDCONTROL6-REALITY-ANCHOR-PREPARATION-316",
        "recordedAtUtc": now,
        "status": "PREPARED_UNSENT_DIRECTOR_REVIEW_REQUIRED",
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTHORITY,
        "sourceRefresh": source_refresh,
        "return315CorrectionSource": {"archive": {"path": RETURN315.relative_to(ROOT).as_posix(), **digest(RETURN315.read_bytes())}, "delivery": {"path": RETURN315_DELIVERY.relative_to(ROOT).as_posix(), **digest(RETURN315_DELIVERY.read_bytes())}, "audit": {"path": RETURN315_AUDIT.relative_to(ROOT).as_posix(), **digest(RETURN315_AUDIT.read_bytes())}, "correctionIds": ["RA315-C01", "RA315-C02", "RA315-C03", "RA315-C04", "RA315-C05"], "status": "HOLD_WC188-B02_CORRECTION_REQUIRED"},
        "extraSourceBindings": extra_bindings,
        "return281Preservation": {"archive": {"path": RETURN281.relative_to(ROOT).as_posix(), **digest(RETURN281.read_bytes())}, "delivery": {"path": RETURN281_DELIVERY.relative_to(ROOT).as_posix(), **digest(RETURN281_DELIVERY.read_bytes())}, "audit": {"path": RETURN281_AUDIT.relative_to(ROOT).as_posix(), **digest(RETURN281_AUDIT.read_bytes())}, "exactRARecordCount": 14, "exactRARecordIds": [r["id"] for r in ra_rows], "procedureMember": "procedures/reality-anchor.json", "sameCaseBytesPreserved": True},
        "acceptedForgeW2": {"candidatePath": FORGE_DIR.relative_to(ROOT).as_posix(), "status": "accepted W2 component/source evidence", "sourceBindings": [x for x in extra_bindings if "eternal-forge" in x["member"] or "ETERNAL_FORGE" in x["member"]], "exactStartingStateSHA256": "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e", "replayEventCount": len(w2["branch"]["events"]), "replayAllForwardInverseVerified": True, "caseEndpointTimeSeconds": 172806.6, "castF2RemainsEnded": True, "castF3ActiveOnBracelet2": True},
        "lifecycleCandidate": {"physicalItemId": "bracelet-2", "activeApplicationId": "castF3", "owner": "A", "custody": "A-floor-within-5ft", "HP": 5, "charges": 1, "noNaturalExpiry": True, "sourceTerminalMethod": "authorized successful Greater Dispel", "sourceSuppressionContract": "body and history persist; no charge/damage reset or missed-event catch-up"},
        "twoIndependentBranches": [b["id"] for b in witnesses["branches"]],
        "witnessSummary": {"branches": witnesses["branches"], "eventCount": witnesses["eventCount"], "starterStateSHA256": "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e"},
        "requiredClausesAndCoverage": [
            "Use Permission mode so the exact known source/application handle is available; do not infer the item's generating school.",
            "Create one continuing component with exact cast ID, owner, current custodian, body HP/charges, creation history, costs, contents, damage, and explicit absence of natural expiry.",
            "Pay RA Action, 26 RP, V/S/F; predeclare ordered policy; record fixed perceived center/range/radius, total cover, original 60-second concentration deadline, and application identity.",
            "Deny only castF3's otherwise eligible item expression while preserving the source/body/custody/charge and all histories.",
            "Keep a distinct surviving-source branch: after an owner Action changes permission, resolve only a currently lawful expression; preserve its charge debit and do not refill/catch up.",
            "Keep a distinct ended-source branch: pay an admitted Greater Dispel with exact cost, resources, components, perception, capture volume, check/DC and counters; end castF3 while denied; then allow the old handle and test no resurrection.",
            "Do not use Nullification Wave, revive castF2, invent Forge expiry, or change any blocker/acceptance/applications.",
            "Preserve each source's regular-start schedules and process every due actor start through each branch endpoint; record the RA deadline and absence of a Forge deadline.",
        ],
        "currentAuthority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0},
        "continuingPriorityOrder": next_order,
        "separatelyRetainedHolds": ["final-word/DR217-B01", "elemental-shell/DF218-B01", "elemental-shell/DF218-B02", "timeless-form/DF218-B03", "invulnerable-sphere/DF218-B04", "nullification-wave/WC188-B01"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "noAcceptanceOrApplicationIssued": True,
        "canonicalFilesChangedByThisPacket": False,
    }
    prep_path = A / "RANK9_WARDCONTROL6_REALITY_ANCHOR_PREPARATION_316.json"
    prep_path.write_bytes(jb(prep))
    witness_path = A / "REALITY_ANCHOR_WITNESS_SUPPLEMENT_316.json"
    witness_path.write_bytes(jb(witnesses))

    pending_audit = {
        "id": "CURRENT26-PENDING-IDENTITY-AUDIT-316",
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_822_26_PREPARING_REALITY_ANCHOR",
        "supersedes": "CURRENT26-PENDING-IDENTITY-AUDIT-315",
        "authority": AUTHORITY,
        "indexBinding": {"path": INDEX.relative_to(ROOT).as_posix(), **digest(index_raw)},
        "catalogBinding": {"path": CATALOG.relative_to(ROOT).as_posix(), **digest(catalog_raw)},
        "pendingCount": 26, "pendingIds": pending_ids,
        "acceptedIds": [], "appliedIds": [], "separatelyHeldIds": ["final-word", "elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave"],
        "allPendingIdsExistInNativeCatalog": True, "noPendingTargetSilentlyAccepted": True,
        "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [], "firstReviewTasksRemaining": 0, "closureTasksRemaining": 26,
        "nextGroup": TARGET, "nextPendingIds": [TARGET], "nextPendingCount": 1,
        "nextStep": "Submit corrected Reality Anchor-only packet316 for Director review; no acceptance or application in preparation step.",
        "sourceQueue": {"path": QUEUE314.relative_to(ROOT).as_posix(), **digest(QUEUE314.read_bytes())},
        "canonicalFilesChanged": False,
    }
    audit_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_316.json"
    audit_path.write_bytes(jb(pending_audit))
    queue = read_json(QUEUE314)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-316", "recordedAtUtc": now, "supersedesQueue": queue["id"],
        "activeReview": {"spellId": TARGET, "blockerIds": [BLOCKER], "packet": "CORRECTION_PACKET316_PREPARED_UNSENT", "status": "PREPARED_UNSENT_DIRECTOR_REVIEW_REQUIRED"},
        "next": TARGET,
        "nextPendingIds": [TARGET], "nextPendingCount": 1,
        "lastDirectorReturn": "RETURN315_REALITY_ANCHOR_HELD_CORRECTIONS_C01_TO_C05",
        "currentPreparation": {"path": prep_path.relative_to(ROOT).as_posix(), **digest(prep_path.read_bytes())},
        "currentPacketStatus": "CORRECTION_PACKET316_PREPARED_UNSENT",
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": [TARGET],
        "currentReturnBlockers": {TARGET: [BLOCKER]},
        "currentCorrectionIds": ["RA315-C01", "RA315-C02", "RA315-C03", "RA315-C04", "RA315-C05"],
        "pendingIdentityAudit": {"path": audit_path.relative_to(ROOT).as_posix(), **digest(audit_path.read_bytes())},
        "canonicalFilesChanged": False, "applicationPerformed": False,
    })
    queue_path = A / "CURRENT_SPELL_QUEUE_316.json"
    queue_path.write_bytes(jb(queue))
    handoff = {
        "id": "CURRENT-HANDOFF-316", "recordedAtUtc": now, "supersedes": "CURRENT-HANDOFF-315",
        "status": "RETURN315_CORRECTED_PACKET316_PREPARED_UNSENT", "authority": AUTHORITY,
        "scopeIds": [TARGET], "blockerIds": [BLOCKER],
        "queue": queue_path.relative_to(ROOT).as_posix(), "queueBinding": digest(queue_path.read_bytes()),
        "pendingIdentityAudit": audit_path.relative_to(ROOT).as_posix(),
        "appliedThisStep": [], "acceptedThisStep": [], "heldThisStep": [],
        "currentBlocker": BLOCKER, "nextPendingGroup": [TARGET],
        "nextStep": "Submit corrected packet316 to GPT Director; receive decision; independently verify any returned archive; apply only Director-accepted IDs.",
        "previousPreparation": {"path": prep_path.relative_to(ROOT).as_posix(), **digest(prep_path.read_bytes())},
        "currentPacketStatus": "CORRECTION_PACKET316_PREPARED_UNSENT", "continuingPriorityOrder": next_order,
        "separatelyRetainedHolds": pending_audit["separatelyHeldIds"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "GPT Calibration review part 6; user-authorized upload and send",
        "directorReturn315": {"acceptedIds": [], "appliedIds": [], "heldIds": [TARGET], "blockerIds": [BLOCKER], "correctionIds": ["RA315-C01", "RA315-C02", "RA315-C03", "RA315-C04", "RA315-C05"]},
        "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    handoff_path = A / "CURRENT_HANDOFF_316.json"
    handoff_path.write_bytes(jb(handoff))

    packet_members = {}
    packet_members.update(source_payload)
    packet_members.update(extra_payload)
    packet_members.update(history_payload)
    packet_members["authority/SOURCE_REFRESH_316.json"] = jb(source_refresh)
    packet_members["authority/CURRENT26_PENDING_IDENTITY_AUDIT_316.json"] = audit_path.read_bytes()
    packet_members["authority/CURRENT_SPELL_QUEUE_316.json"] = queue_path.read_bytes()
    packet_members["authority/CURRENT_HANDOFF_316.json"] = handoff_path.read_bytes()
    packet_members["authority/RANK9_WARDCONTROL6_REALITY_ANCHOR_PREPARATION_316.json"] = prep_path.read_bytes()
    packet_members["witness/REALITY_ANCHOR_WITNESS_SUPPLEMENT_316.json"] = witness_path.read_bytes()
    packet_members["witness/ETERNAL_FORGE_W2_REPLAY_AUDIT_316.json"] = jb({"id": "ETERNAL-FORGE-W2-REPLAY-AUDIT-316", "status": "PASS", "baseSHA256": w2["branch"]["baseStateSHA256"], "finalSHA256": w2["branch"]["finalStateSHA256"], "eventCount": len(w2["branch"]["events"]), "checks": w2["replayChecks"], "source": "SUPPLEMENT255_W2.json#eventReplay/branches/0"})
    # Attach per-branch starting-state documents so a reviewer can inspect the exact boundary without replaying the entire prior W2 history first.
    for b in witnesses["branches"]:
        packet_members[f"witness/{b['id']}_BASE_STATE.json"] = jb(b["baseState"])
        packet_members[f"witness/{b['id']}_FINAL_STATE.json"] = jb(b["finalState"])
    manifests = [{"path": name, **digest(data)} for name, data in sorted(packet_members.items())]
    manifest = {"id": "REALITY-ANCHOR-PACKET-316-MEMBER-MANIFEST", "memberCount": len(manifests), "members": manifests}
    packet_members["MEMBER_MANIFEST.json"] = jb(manifest)
    with zipfile.ZipFile(PACKET, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=7) as zf:
        for name, data in sorted(packet_members.items()):
            zf.writestr(name, data)
    packet_digest = digest(PACKET.read_bytes())
    delivery = {
        "id": "DD-RANK9-WARDCONTROL6-REALITY-ANCHOR-316-DELIVERY",
        "recordedAtUtc": now,
        "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **packet_digest},
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTHORITY,
        "sourceCount": 91, "changedSincePacket312": len(changed), "extraSourceCount": len(extra_paths),
        "preservedReturn281RealityAnchorCaseCount": len(ra_rows),
        "witnessBranchIds": [b["id"] for b in witnesses["branches"]],
        "witnessEventCount": witnesses["eventCount"],
        "startingEndpointSHA256": "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e",
        "status": "PREPARED_UNSENT_DIRECTOR_REVIEW_REQUIRED",
        "acceptedIds": [], "appliedIds": [], "canonicalChanges": False,
        "githubChanges": "none in this preparation step",
        "memberManifest": {"path": "MEMBER_MANIFEST.json", **digest(packet_members["MEMBER_MANIFEST.json"])},
    }
    DELIVERY.write_bytes(jb(delivery))
    receipt = {
        "id": "REALITY-ANCHOR-PACKET-316-SUBMISSION-RECEIPT",
        "recordedAtUtc": now, "status": "CORRECTION_PACKET316_PREPARED_UNSENT",
        "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **packet_digest},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTHORITY,
        "branch": branch_name, "baseCommit": base_commit,
        "sourceRefreshChangedCount": len(changed), "sourceRefreshChanges": changed,
        "archiveMemberCount": len(packet_members), "historicalRARecordCount": len(ra_rows),
        "witnessBranchCount": len(witnesses["branches"]), "witnessEventCount": witnesses["eventCount"],
        "startingEndpointSHA256": "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e",
        "outerZipTest": "PASS", "allMemberHashes": "PASS", "forwardInverseReplay": "PASS",
        "canonicalChanges": False, "applicationPerformed": False,
    }
    receipt_path = A / "REALITY_ANCHOR_PACKET_316_SUBMISSION_RECEIPT.json"
    receipt_path.write_bytes(jb(receipt))
    print(json.dumps({"packet": str(PACKET), "packetDigest": packet_digest, "delivery": str(DELIVERY), "receipt": str(receipt_path), "members": len(packet_members), "sourceCount": len(source_rows), "changedSince312": len(changed), "historicalRARecords": len(ra_rows), "branchIds": [x["id"] for x in witnesses["branches"]], "witnessEvents": witnesses["eventCount"], "authority": AUTHORITY}, indent=2))


if __name__ == "__main__":
    main()
