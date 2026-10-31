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
OUT = A / "rank9_wardcontrol6_reality_anchor_packet_315_prepared_build07"
PACKET_NAME = "DD_Rank9_WardControl6_RealityAnchor_315.zip"
DELIVERY_NAME = "DD_Rank9_WardControl6_RealityAnchor_315_DELIVERY.json"
PACKET = OUT / PACKET_NAME
DELIVERY = OUT / DELIVERY_NAME
RETURN281 = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
RETURN281_DELIVERY = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
RETURN281_AUDIT = A / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
SOURCE312_DIR = A / "rank9_wardcontrol6_source_packet_312_prepared"
SOURCE312 = SOURCE312_DIR / "DD_Rank9_WardControl6_CurrentSource_312.zip"
SOURCE_REFRESH312 = A / "SOURCE_REFRESH_312.json"
QUEUE314 = A / "CURRENT_SPELL_QUEUE_314.json"
HANDOFF314 = A / "CURRENT_HANDOFF_314.json"
AUDIT312 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_312.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
FORGE_DIR = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255"
FORGE_AUDIT = A
TARGET = "reality-anchor"
BLOCKER = "WC188-B02"
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
        "fixtureId": "RA315-C-PREP-01",
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
    s["supplement"]["realityAnchorWitness315"] = {
        "branchId": branch_id,
        "status": "NONCANONICAL_LOCAL_WITNESS_DRAFT_FOR_DIRECTOR_REVIEW",
        "clock": {"id": "RA315-WITNESS-CLOCK", "startSeconds": 172806.6, "dawns": [172800, 259200], "timezone": "fixture absolute seconds; no calendar claim"},
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
    s["scene"]["ra315Geometry"] = s["supplement"]["realityAnchorWitness315"]["scene"]
    return s


def add_event(branch: dict, event_id: str, kind: str, start: float, end: float, description: str, mutate, record: dict) -> None:
    state = branch["state"]
    before = state_sha(state)
    before_state = copy.deepcopy(state)
    mutate(state)
    state["time"] = end
    trace = {"id": event_id, "kind": kind, "timeStartSeconds": start, "timeEndSeconds": end, "description": description, **record}
    state["supplement"]["realityAnchorWitness315"]["events"].append(trace)
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
    s["supplement"]["realityAnchorWitness315"]["dueClockEvents"].append({"kind": "regular-start", "actor": "C", "timeSeconds": 172806.6, "budgetRefreshed": True, "Action": 1, "Reaction": 1, "source": "new bounded witness fixture"})


def add_case_common(branch: dict, actor_c: dict, include_allow_a: bool) -> None:
    branch["state"] = copy.deepcopy(branch["baseState"])
    def m(s):
        seeded = case_state(s, branch["id"], actor_c)
        s.clear()
        s.update(seeded)
        add_actor_c(s, actor_c)
        s["supplement"]["realityAnchorWitness315"]["policyHistory"].append({
            "policyId": "RA315-POLICY-01", "mode": "Permission", "default": "DENY",
            "predeclaredRules": [
                {"order": 1, "effect": "DENY", "applicationId": "castF3", "why": "exact known Eternal Forge imprint under test"},
                *([{"order": 2, "effect": "ALLOW", "casterIdentity": "A", "why": "known W2 owner/caster identity; admits A's Greater Dispel operation"}] if include_allow_a else []),
                {"order": 3 if include_allow_a else 2, "effect": "ALLOW", "applicationId": "castRA1", "why": "keep this already-established Anchor's own field operation addressable"},
            ],
            "firstMatchWins": True,
            "noHiddenIdentityOrInventoryOracle": True,
        })
        s["supplement"]["realityAnchorWitness315"]["preparationAndSourceAudit"] = {
            "completeItemProfile": {"itemId": "bracelet-2", "owner": "A", "custodianAtStart": "A-floor-within-5ft", "HP": 5, "maxHP": 5, "damage": 0, "charges": 1, "maxCharges": 1, "contents": [], "processedDawns": [], "createdAt": 172806.5, "rootId": "castF3", "rootRank": 9, "rootActive": True, "rootSource": "accepted Eternal Forge W2 event MF247-F-W2-E23", "rootNaturalExpiry": None},
            "creationAcquisitionHistory": "exact accepted Eternal Forge W2 continuation, copied only from endpoint hash 684d...109e; bracelet-1/castF2 remains ended and physically preserved",
            "ownerCustodyAndUse": "A is owner/caster; floor custody within 5ft; local fit fixture records an open ordinary left wrist for A before don; no transfer of ownership",
            "itemUseCosts": "no activation RP; an eligible Hide check consumes the existing one charge only when the source expression is permitted and the effect is actually used",
            "originalSourceDeadline": "none; source model says no natural expiry, concentration, caster-survival tether or ongoing range limit",
            "RAProfile": {"class": "Wizard", "level": 18, "rank": 9, "mode": "Permission", "baseRP": 26, "components": "V/S/F", "action": "Action", "rangeFeet": 100, "radiusFeet": 100, "duration": "60 elapsed seconds concentration", "anchorSourceDeadlineSeconds": 172866.7, "centerFeet": [75, 0, 0]},
        }
    add_event(branch, "RA315-" + branch["id"] + "-E01-ENTER-W219-C", "source-fixture-entry-and-policy-predeclaration", 172806.6, 172806.65,
              "Add the separately source-qualified W219 caster and predeclare the exact Permission-mode policy; import no prior W219 case events.", m,
              {"actorProfile": "ACTOR_PROFILES.json#/W219", "historyImported": False, "mode": "Permission", "predeclaredPolicyId": "RA315-POLICY-01"})


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
        s["applications"]["castRA1"] = {"id": "castRA1", "spellId": TARGET, "caster": "C", "class": "Wizard", "classLevel": 18, "generatingSchool": "Abjuration", "generatingRank": 9, "paidRP": 26, "costAdjustments": {"preCastDissonance": 0, "RefrainAdded": 0}, "components": "V/S/F", "originFeet": [75, 0, 0], "centerFeet": [75, 0, 0], "rangeFeet": 100, "radiusFeet": 100, "mode": "Permission", "policyId": "RA315-POLICY-01", "establishedAtSeconds": 172806.7, "endsAtSeconds": 172866.7, "maintainer": "C", "concentration": True, "status": "active", "totalCoverClipped": False}
        s["applications"]["castRA1"]["policy"] = {"id": "RA315-POLICY-01", "revision": 0, "mode": "Permission", "default": "DENY", "rules": copy.deepcopy(s["supplement"]["realityAnchorWitness315"]["policyHistory"][-1]["predeclaredRules"]), "firstMatchWins": True}
        s["fields"]["castRA1"] = {"sourceId": "castRA1", "centerFeet": [75, 0, 0], "radiusFeet": 100, "policyId": "RA315-POLICY-01", "expiresAtSeconds": 172866.7, "owner": "C", "status": "active"}
    add_event(branch, actor_id, "paid-reality-anchor-cast-and-establishment", 172806.65, 172806.7,
              "C pays 26 RP and one Action to establish a fixed Permission-mode Reality Anchor at the perceived center; castF3 falls within the 100-foot field.", m,
              {"caster": "C", "spellId": TARGET, "castId": "castRA1", "costRP": 26, "preCastRP": 68, "postCastRP": 42, "action": "Action", "components": "V/S/F", "mode": "Permission", "defaultPolicy": "DENY", "centerFeet": [75, 0, 0], "centerDistanceFromCasterFeet": 0, "radiusFeet": 100, "expiresAtSeconds": 172866.7, "capturedApplications": [], "itemInsideField": True, "allCostsPaidBeforeEstablishment": True, "counterWindow": {"eligibleCounterers": [], "A": {"distanceFeet": 75, "reason": "outside accepted 60-foot Counterspell range"}, "B": {"distanceFeet": 70, "reason": "noncasting receiver; no Counterspell acquisition"}, "C": {"reason": "cannot counter own cast"}}})


def regular_start(branch: dict, actor_id: str, time_s: float, event_number: int) -> None:
    def m(s):
        actor = s["actors"][actor_id]
        refresh_start(actor, time_s, actor_id)
        s["supplement"]["realityAnchorWitness315"]["dueClockEvents"].append({"kind": "regular-start", "actor": actor_id, "timeSeconds": time_s, "budgetRefreshed": True, "Action": 1, "Reaction": 1, "BonusAction": 1})
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-{actor_id}-START", "regular-start", time_s, time_s,
              f"Process {actor_id}'s due regular start exactly once; refresh Action, Reaction, Bonus Action and movement budget.", m,
              {"actor": actor_id, "ActionAfter": 1, "ReactionAfter": 1, "sourceSchedulePreserved": True})


def regular_end(branch: dict, actor_id: str, time_s: float, event_number: int) -> None:
    def m(s):
        actor = s["actors"][actor_id]
        assert actor.get("turnOpen") is True and math.isclose(float(actor.get("nextRegularEnd")), time_s, abs_tol=1e-6), (actor_id, actor.get("nextRegularEnd"), time_s)
        actor["turnOpen"] = False
        actor.setdefault("regularEndsProcessed", []).append(time_s)
        s["supplement"]["realityAnchorWitness315"]["dueClockEvents"].append({"kind": "regular-end", "actor": actor_id, "timeSeconds": time_s, "turnClosed": True})
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-{actor_id}-END", "regular-end", time_s, time_s,
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
        s["supplement"]["realityAnchorWitness315"]["custodyHistory"] = [{"timeSeconds": 172812.5, "itemId": "bracelet-2", "owner": "A", "from": "A-floor-within-5ft", "to": "A-left-wrist", "cost": "A Action", "consent": True}]
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-A-DON-BRACELET2", "lawful-wear", 172812.41, 172812.5,
              "A spends an Action to don the existing bracelet-2 without changing ownership, body integrity, charge or castF3 history.", m,
              {"actor": "A", "itemId": "bracelet-2", "cost": "Action", "ownerUnchanged": True, "custodyAfter": "A-left-wrist", "HP": 5, "charges": 1})


def denied_hide(branch: dict, event_number: int, termination: bool = False) -> None:
    def m(s):
        a = s["actors"]["A"]
        item = s["items"]["bracelet-2"]
        assert a["Action"] == 1
        a["Action"] = 0
        s["supplement"]["realityAnchorWitness315"]["deniedExpressions"].append({"timeSeconds": 172818.5, "actor": "A", "itemId": "bracelet-2", "sourceId": "castF3", "function": "eligible Hide / Stealth-family item expression", "decision": "DENIED", "reason": "first matching exact applicationId castF3 policy", "underlyingSourceRetained": item["imprintRoot"]["active"], "chargeBefore": item["charges"], "chargeAfter": item["charges"], "bonusApplied": 0, "advantageApplied": False, "actionContinuesWithoutItemExpression": True})
        item["imprintRoot"]["suppressed"] = True
        item["imprintRoot"]["suppressedBy"] = ["castRA1"]
        item["functionalState"] = "item magical expression denied; physical body persists"
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-A-HIDE-DENIED", "permission-denial-of-item-expression", 172818.41, 172818.5,
              "A's otherwise eligible Hide action proceeds, while the exact castF3 item expression is denied; no charge is spent and no magical bonus or advantage is applied.", m,
              {"actor": "A", "itemId": "bracelet-2", "applicationId": "castF3", "policyId": "RA315-POLICY-01", "decision": "DENIED", "chargeBefore": 1, "chargeAfter": 1, "bonusApplied": 0, "advantageApplied": False, "diceInput": {"kind": "DEX-Stealth task input", "d20": 15, "selectedBy": "local test input", "no hidden success or observer result asserted": True}, "physicalBodyAndCustodyRemain": True})


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
        policy_id = f"RA315-POLICY-01-R{policy['revision']}"
        policy["id"] = policy_id
        app["policyId"] = policy_id
        s["fields"]["castRA1"]["policyId"] = policy_id
        s["supplement"]["realityAnchorWitness315"]["policyHistory"].append({"atSeconds": at + 0.01, "actor": "C", "action": "Action", "revision": policy["revision"], "default": policy["default"], "rules": copy.deepcopy(policy["rules"]), "noNewCastOrRP": True, "clockNotReset": True, "afterSourceTermination": after_termination})
        s["actors"]["C"]["Action"] = 0
        if allow_forge and not after_termination:
            item = s["items"]["bracelet-2"]
            item["imprintRoot"]["suppressed"] = False
            item["imprintRoot"].pop("suppressedBy", None)
            item["functionalState"] = "live imprint; policy permits currently eligible expressions"
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-C-POLICY-EDIT", "owner-action-policy-edit", at, at + 0.01,
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
        s["supplement"]["realityAnchorWitness315"]["functionEvents"].append(result)
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-A-HIDE-AFTER-POLICY", "item-expression-after-policy-change", time_s - 0.09, time_s,
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
        s["supplement"]["realityAnchorWitness315"]["imprintEndings"].append({"timeSeconds": time_s, "applicationId": "castF3", "physicalItemId": "bracelet-2", "method": "authorized successful Greater Dispel", "caster": "A", "DC": 28, "roll": {"d20": 17, "INT": 5, "PB": 6, "total": 28}, "RAStillDeniesCastF3AtResolution": True, "physicalBodyPreserved": True, "HP": item["HP"], "custody": item["custodian"], "charges": item["charges"], "contents": [], "resumed": False})
    add_event(branch, f"RA315-{branch['id']}-E{event_number:02d}-PAID-GREATER-DISPEL", "paid-greater-dispel-terminates-denied-imprint", time_s - 0.09, time_s,
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
        cast_ra(b, f"RA315-{bid}-E02-PAID-REALITY-ANCHOR")
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
            "deniedExpressionCount": len(state["supplement"]["realityAnchorWitness315"]["deniedExpressions"]),
            "functionEvents": state["supplement"]["realityAnchorWitness315"].get("functionEvents", []),
            "imprintEndings": state["supplement"]["realityAnchorWitness315"]["imprintEndings"],
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
        "authority/CURRENT_SPELL_QUEUE_314.json": QUEUE314,
        "authority/CURRENT_HANDOFF_314.json": HANDOFF314,
        "authority/CURRENT26_PENDING_IDENTITY_AUDIT_312.json": AUDIT312,
        "authority/authored_review_index.json": INDEX,
        "authority/catalog.json": CATALOG,
        "authority/Return281_INDEPENDENT_AUDIT.json": RETURN281_AUDIT,
        "authority/Return281_DELIVERY.json": RETURN281_DELIVERY,
        "authority/Return281_ARCHIVE.zip": RETURN281,
        "authority/Return312_NULLIFICATION_WAVE_HOLD_RECEIPT.json": A / "NULLIFICATION_WAVE_HOLD_RECEIPT_312.json",
        "authority/Return312_NULLIFICATION_WAVE_DECISION.json": A / "NULLIFICATION_WAVE_DIRECTOR_DECISION_312.json",
    }
    extra_payload = {member: path.read_bytes() for member, path in extra_paths.items()}
    extra_payload["authority/SOURCE_REFRESH_312.json"] = previous_refresh_raw
    extra_payload["authority/WAVE_SOURCE_EXTRA_BINDINGS_312.json"] = old_wave_extra_raw
    extra_bindings = [{"member": member, **bind(path, extra_payload[member], member)} for member, path in extra_paths.items()]
    extra_bindings.extend([
        {"member": "authority/SOURCE_REFRESH_312.json", "path": SOURCE312.relative_to(ROOT).as_posix(), "sourceMember": "SOURCE_REFRESH_312.json", **digest(previous_refresh_raw)},
        {"member": "authority/WAVE_SOURCE_EXTRA_BINDINGS_312.json", "path": SOURCE312.relative_to(ROOT).as_posix(), "sourceMember": "WAVE_SOURCE_EXTRA_BINDINGS_312.json", **digest(old_wave_extra_raw)},
    ])
    source_refresh = {
        "id": "REALITY-ANCHOR-91-SOURCE-REFRESH-315",
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
        "id": "RANK9-WARDCONTROL6-REALITY-ANCHOR-PREPARATION-315",
        "recordedAtUtc": now,
        "status": "PREPARED_UNSENT_DIRECTOR_REVIEW_REQUIRED",
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTHORITY,
        "sourceRefresh": source_refresh,
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
    prep_path = A / "RANK9_WARDCONTROL6_REALITY_ANCHOR_PREPARATION_315.json"
    prep_path.write_bytes(jb(prep))
    witness_path = A / "REALITY_ANCHOR_WITNESS_SUPPLEMENT_315.json"
    witness_path.write_bytes(jb(witnesses))

    pending_audit = {
        "id": "CURRENT26-PENDING-IDENTITY-AUDIT-315",
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_822_26_PREPARING_REALITY_ANCHOR",
        "supersedes": "CURRENT26-PENDING-IDENTITY-AUDIT-312",
        "authority": AUTHORITY,
        "indexBinding": {"path": INDEX.relative_to(ROOT).as_posix(), **digest(index_raw)},
        "catalogBinding": {"path": CATALOG.relative_to(ROOT).as_posix(), **digest(catalog_raw)},
        "pendingCount": 26, "pendingIds": pending_ids,
        "acceptedIds": [], "appliedIds": [], "separatelyHeldIds": ["final-word", "elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave"],
        "allPendingIdsExistInNativeCatalog": True, "noPendingTargetSilentlyAccepted": True,
        "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [], "firstReviewTasksRemaining": 0, "closureTasksRemaining": 26,
        "nextGroup": TARGET, "nextPendingIds": [TARGET], "nextPendingCount": 1,
        "nextStep": "Submit Reality Anchor-only packet315 for Director review; no adjudication, acceptance or application in preparation step.",
        "sourceQueue": {"path": QUEUE314.relative_to(ROOT).as_posix(), **digest(QUEUE314.read_bytes())},
        "canonicalFilesChanged": False,
    }
    audit_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_315.json"
    audit_path.write_bytes(jb(pending_audit))
    queue = read_json(QUEUE314)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-315", "recordedAtUtc": now, "supersedesQueue": queue["id"],
        "activeReview": {"spellId": TARGET, "blockerIds": [BLOCKER], "packet": "PREPARING_315", "status": "PREPARED_UNSENT_DIRECTOR_REVIEW_REQUIRED"},
        "next": TARGET,
        "nextPendingIds": [TARGET], "nextPendingCount": 1,
        "lastDirectorReturn": "RETURN312_NULLIFICATION_WAVE_HELD_NEXT_REALITY_ANCHOR",
        "currentPreparation": {"path": prep_path.relative_to(ROOT).as_posix(), **digest(prep_path.read_bytes())},
        "currentPacketStatus": "PREPARED_UNSENT",
        "pendingIdentityAudit": {"path": audit_path.relative_to(ROOT).as_posix(), **digest(audit_path.read_bytes())},
        "canonicalFilesChanged": False, "applicationPerformed": False,
    })
    queue_path = A / "CURRENT_SPELL_QUEUE_315.json"
    queue_path.write_bytes(jb(queue))
    handoff = {
        "id": "CURRENT-HANDOFF-315", "recordedAtUtc": now, "supersedes": "CURRENT-HANDOFF-314",
        "status": "REALITY_ANCHOR_PACKET315_PREPARED_UNSENT", "authority": AUTHORITY,
        "scopeIds": [TARGET], "blockerIds": [BLOCKER],
        "queue": queue_path.relative_to(ROOT).as_posix(), "queueBinding": digest(queue_path.read_bytes()),
        "pendingIdentityAudit": audit_path.relative_to(ROOT).as_posix(),
        "appliedThisStep": [], "acceptedThisStep": [], "heldThisStep": [],
        "currentBlocker": BLOCKER, "nextPendingGroup": [TARGET],
        "nextStep": "Submit packet315 to GPT Director; receive decision; independently verify any returned archive; apply only Director-accepted IDs.",
        "previousPreparation": {"path": prep_path.relative_to(ROOT).as_posix(), **digest(prep_path.read_bytes())},
        "currentPacketStatus": "PREPARED_UNSENT", "continuingPriorityOrder": next_order,
        "separatelyRetainedHolds": pending_audit["separatelyHeldIds"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "GPT Calibration review part 6; user-authorized upload and send",
        "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    handoff_path = A / "CURRENT_HANDOFF_315.json"
    handoff_path.write_bytes(jb(handoff))

    packet_members = {}
    packet_members.update(source_payload)
    packet_members.update(extra_payload)
    packet_members.update(history_payload)
    packet_members["authority/SOURCE_REFRESH_315.json"] = jb(source_refresh)
    packet_members["authority/CURRENT26_PENDING_IDENTITY_AUDIT_315.json"] = audit_path.read_bytes()
    packet_members["authority/CURRENT_SPELL_QUEUE_315.json"] = queue_path.read_bytes()
    packet_members["authority/CURRENT_HANDOFF_315.json"] = handoff_path.read_bytes()
    packet_members["authority/RANK9_WARDCONTROL6_REALITY_ANCHOR_PREPARATION_315.json"] = prep_path.read_bytes()
    packet_members["witness/REALITY_ANCHOR_WITNESS_SUPPLEMENT_315.json"] = witness_path.read_bytes()
    packet_members["witness/ETERNAL_FORGE_W2_REPLAY_AUDIT_315.json"] = jb({"id": "ETERNAL-FORGE-W2-REPLAY-AUDIT-315", "status": "PASS", "baseSHA256": w2["branch"]["baseStateSHA256"], "finalSHA256": w2["branch"]["finalStateSHA256"], "eventCount": len(w2["branch"]["events"]), "checks": w2["replayChecks"], "source": "SUPPLEMENT255_W2.json#eventReplay/branches/0"})
    # Attach per-branch starting-state documents so a reviewer can inspect the exact boundary without replaying the entire prior W2 history first.
    for b in witnesses["branches"]:
        packet_members[f"witness/{b['id']}_BASE_STATE.json"] = jb(b["baseState"])
        packet_members[f"witness/{b['id']}_FINAL_STATE.json"] = jb(b["finalState"])
    manifests = [{"path": name, **digest(data)} for name, data in sorted(packet_members.items())]
    manifest = {"id": "REALITY-ANCHOR-PACKET-315-MEMBER-MANIFEST", "memberCount": len(manifests), "members": manifests}
    packet_members["MEMBER_MANIFEST.json"] = jb(manifest)
    with zipfile.ZipFile(PACKET, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=7) as zf:
        for name, data in sorted(packet_members.items()):
            zf.writestr(name, data)
    packet_digest = digest(PACKET.read_bytes())
    delivery = {
        "id": "DD-RANK9-WARDCONTROL6-REALITY-ANCHOR-315-DELIVERY",
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
        "id": "REALITY-ANCHOR-PACKET-315-SUBMISSION-RECEIPT",
        "recordedAtUtc": now, "status": "PREPARED_UNSENT",
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
    receipt_path = A / "REALITY_ANCHOR_PACKET_315_SUBMISSION_RECEIPT.json"
    receipt_path.write_bytes(jb(receipt))
    print(json.dumps({"packet": str(PACKET), "packetDigest": packet_digest, "delivery": str(DELIVERY), "receipt": str(receipt_path), "members": len(packet_members), "sourceCount": len(source_rows), "changedSince312": len(changed), "historicalRARecords": len(ra_rows), "branchIds": [x["id"] for x in witnesses["branches"]], "witnessEvents": witnesses["eventCount"], "authority": AUTHORITY}, indent=2))


if __name__ == "__main__":
    main()
