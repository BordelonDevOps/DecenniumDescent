from __future__ import annotations

import copy
import hashlib
import json
import math
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build_fortress_closure_intake_367 as intake  # noqa: E402


CASE_ID = "PG328-W07-REAL-DISPEL-374-TESTONLY"
OUTPUT = ROOT / "fortress_w07_real_dispel_374_repack01"
PAYLOAD = OUTPUT / "payload"
ARCHIVE_NAME = "DD_Rank9_ConjureDemiplaneFortress_W07_RealDispel_374_Repack01_TESTONLY.zip"
DELIVERY_NAME = "DD_Rank9_ConjureDemiplaneFortress_W07_RealDispel_374_Repack01_DELIVERY.json"
PARENT_ID = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/real-dispel"
PARENT_MEMBER = (
    "evidence/packet328/prior/Return284_cases/"
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__real-dispel.json"
)
SPACE_ID = PARENT_ID + "/cast1/space"
ROOT_EFFECT_ID = PARENT_ID + "/cast1"
SIGHT_ID = "PG328-W07-B-ARCANE-SIGHT-CAST-374"
DISPEL_FAIL_ID = "PG328-W07-B-REAL-DISPEL-FAIL-374"
DISPEL_SUCCESS_ID = "PG328-W07-B-REAL-DISPEL-SUCCESS-374"
SIGHT = "wizard.arch.arcane-sight"
DISPEL = "wizard.arch.dispel-magic"
COUNTERSPELL = "wizard.base.counterspell"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def advance_clock(state: dict, at: float) -> None:
    delta = round(at - state["time"], 6)
    if delta < -1e-9:
        raise AssertionError(f"Time went backwards: {state['time']} -> {at}")
    state["time"] = at
    state["clock"]["elapsedSeconds"] = round(state["clock"]["elapsedSeconds"] + delta, 6)
    state["clock"]["OpeningRemaining"] = round(state["clock"]["OpeningRemaining"] - delta, 6)
    state["clock"]["HornRemaining"] = round(state["clock"]["HornRemaining"] - delta, 6)


def world_time(initiative_time: float) -> float:
    # The preserved source state binds initiative 0.9 to world elapsed 1.0.
    return round(initiative_time + 0.1, 6)


def add_transition(case: dict, state: dict, event_id: str, kind: str, at: float,
                   detail: dict, rationale: str, sources: list[str]) -> dict:
    before = copy.deepcopy(state)
    advance_clock(state, at)
    detail["initiativeSeconds"] = at
    detail["worldElapsedSeconds"] = state["clock"]["elapsedSeconds"]
    detail["stateSHA256Before"] = sha(before)
    detail["stateSHA256AfterClock"] = sha(state)
    transition = intake.make_transition(
        event_id, kind, before, state,
        {"initiativeSeconds": at, "worldElapsedSeconds": state["clock"]["elapsedSeconds"]},
        sources, rationale,
    )
    transition["detail"] = detail
    case["events"].append(transition)
    state["processedEventIds"].append(event_id)
    # The processed-event ledger is itself state, so include it in the final transition.
    transition["after"] = copy.deepcopy(state)
    transition["afterSHA256"] = sha(state)
    transition["forward"] = intake.diff_ops(before, state)
    transition["inverse"] = intake.diff_ops(state, before)
    if intake.apply_ops(before, transition["forward"]) != state:
        raise AssertionError(f"Forward replay failed for {event_id}")
    if intake.apply_ops(state, transition["inverse"]) != before:
        raise AssertionError(f"Inverse replay failed for {event_id}")
    return state


def schedule_start(case: dict, state: dict, actor_id: str, at: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if abs(schedule["nextStart"] - at) > 1e-6:
        raise AssertionError(f"Unexpected START for {actor_id} at {at}; next is {schedule['nextStart']}")
    before = copy.deepcopy(state)
    advance_clock(state, at)
    for rec in actor.get("recharge", {}).values():
        if rec.get("roundsUntilReady", 0) > 0:
            rec["roundsUntilReady"] -= 1
        rec["ready"] = rec.get("roundsUntilReady", 0) == 0
    actor.update({"action": 1, "bonusAction": 1, "reaction": 1, "movement": actor.get("speed", 30),
                  "magicThisTurn": False})
    schedule["starts"].append(at)
    schedule["nextStart"] = round(at + schedule["period"], 6)
    schedule["nextEnd"] = round(at + schedule["period"] + schedule["endOffset"], 6)
    schedule["budgetHistory"].append({
        "time": at, "action": actor["action"], "BA": actor["bonusAction"],
        "Reaction": actor["reaction"], "Move": actor["movement"],
        "recharge": copy.deepcopy(actor.get("recharge", {})),
    })
    event_id = f"{CASE_ID}:START:{actor_id}:{at:.1f}"
    state["time"] = at
    state["processedEventIds"].append(event_id)
    after = copy.deepcopy(state)
    ev = intake.make_transition(
        event_id, "REGULAR_START", before, after,
        {"initiativeSeconds": at, "worldElapsedSeconds": state["clock"]["elapsedSeconds"]},
        ["sources/COMBAT_ACTION_PLAYTEST.md#time-and-event-ordering"],
        "Process this actor's scheduled regular START: refresh ordinary budgets/reaction and tick this actor's recharge only at the actual marker.",
    )
    ev["forward"] = copy.deepcopy(ev["forward"])
    ev["inverse"] = copy.deepcopy(ev["inverse"])
    ev["detail"] = {"actorId": actor_id, "initiativeSeconds": at,
                    "worldElapsedSeconds": state["clock"]["elapsedSeconds"],
                    "rechargeAfterStart": copy.deepcopy(actor.get("recharge", {}))}
    case["events"].append(ev)
    if intake.apply_ops(before, ev["forward"]) != after or intake.apply_ops(after, ev["inverse"]) != before:
        raise AssertionError(f"Schedule START replay failed: {event_id}")


def schedule_end(case: dict, state: dict, actor_id: str, at: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if not schedule["starts"] or abs(schedule["starts"][-1] + schedule["endOffset"] - at) > 1e-6:
        raise AssertionError(f"Unexpected END for {actor_id} at {at}; last START is {schedule['starts'][-1:]}")
    before = copy.deepcopy(state)
    advance_clock(state, at)
    schedule["ends"].append(at)
    if actor.get("spellEfficiency") and actor["spellEfficiency"].get("until", math.inf) <= at + 1e-6:
        actor["spellEfficiency"] = None
    event_id = f"{CASE_ID}:END:{actor_id}:{at:.1f}"
    state["time"] = at
    state["processedEventIds"].append(event_id)
    after = copy.deepcopy(state)
    ev = intake.make_transition(
        event_id, "REGULAR_END", before, after,
        {"initiativeSeconds": at, "worldElapsedSeconds": state["clock"]["elapsedSeconds"]},
        ["sources/COMBAT_ACTION_PLAYTEST.md#time-and-event-ordering"],
        "Process this actor's scheduled regular END without creating a turn; expire only the due next-regular-turn Spell Efficiency window.",
    )
    ev["forward"] = copy.deepcopy(ev["forward"])
    ev["inverse"] = copy.deepcopy(ev["inverse"])
    ev["detail"] = {"actorId": actor_id, "initiativeSeconds": at,
                    "worldElapsedSeconds": state["clock"]["elapsedSeconds"],
                    "spellEfficiencyAfterEnd": copy.deepcopy(actor.get("spellEfficiency"))}
    case["events"].append(ev)
    if intake.apply_ops(before, ev["forward"]) != after or intake.apply_ops(after, ev["inverse"]) != before:
        raise AssertionError(f"Schedule END replay failed: {event_id}")


def counterspell_windows(at: float) -> list[dict]:
    return [
        {"actorId": "D", "abilityId": COUNTERSPELL, "acquisitionVerified": True,
         "perceptionOfCast": "TEST_ONLY_ORDINARY_SIGHT_CLEAR_SAME_PLANE_SCENE", "distanceFeet": 11.18034,
         "rangeStatus": "WITHIN_60_FEET", "targetingStatus": "LEGAL_SAME_PLANE_TARGET",
         "eligible": True, "decision": "DECLINES", "reactionSpent": 0, "rpSpent": 0,
         "counterspellRechargeStarted": False, "responderStateUnchanged": True},
        {"actorId": "A", "abilityId": COUNTERSPELL, "acquisitionVerified": True,
         "perceptionOfCast": "NOT_DEMONSTRATED", "rangeFeet": None,
         "rangeStatus": "NO_AUTHORIZED_CROSS_PLANE_MEASUREMENT",
         "targetingStatus": "NO_AUTHORIZED_TARGETING_ROUTE_THROUGH_ENTRANCE",
         "eligible": False, "decision": None, "reactionSpent": 0, "rpSpent": 0,
         "counterspellRechargeStarted": False},
        {"actorId": "C", "abilityId": COUNTERSPELL, "acquisitionVerified": False,
         "eligibilityStatus": "NO_WIZARD_COUNTERSPELL_ACQUISITION", "eligible": False,
         "decision": None, "reactionSpent": 0, "rpSpent": 0,
         "counterspellRechargeStarted": False},
    ]


def cast_spell(case: dict, state: dict, *, at: float, spell_id: str, cast_id: str,
               rank: int, cost: int, check_face: int | None, target: dict | None,
               outcome: str, concentration: bool = False) -> None:
    actor = state["actors"]["B"]
    if actor["action"] != 1:
        raise AssertionError(f"B has no Action at {at}")
    recharge = actor.setdefault("recharge", {}).get(spell_id)
    if recharge and not recharge.get("ready", False):
        raise AssertionError(f"{spell_id} is not recharged at {at}: {recharge}")
    before = copy.deepcopy(state)
    advance_clock(state, at)
    first = spell_id not in actor["preparedFamiliesUsed"]
    base_dissonance = 0 if first else (1 if rank >= 3 else 0)
    refrain_increment = 0 if first else 1
    strain = base_dissonance + refrain_increment
    if actor["RP"] < cost:
        raise AssertionError("Insufficient RP")
    actor["RP"] -= cost
    actor["resourceHistory"].append({"event": cast_id, "RP": -cost, "poolAfter": actor["RP"], "discount": False})
    actor["action"] -= 1
    actor["magicThisTurn"] = True
    actor["preparedFamiliesUsed"].append(spell_id) if first else None
    actor["Dissonance"] += strain
    actor["Refrain"] = refrain_increment
    actor["spellEfficiency"] = {
        "family": spell_id,
        "until": actor["regularSchedule"]["nextEnd"],
    }
    actor["recharge"][spell_id] = {
        "ready": False, "roundsUntilReady": 2, "rechargeRounds": 2, "lastUsed": at,
    }
    history = {
        "castId": cast_id, "spellId": spell_id, "class": "Wizard",
        "school": "Divination" if spell_id == SIGHT else "Abjuration",
        "rank": rank, "time": at, "cost": cost, "firstPreparedFamily": first,
        "baseDissonance": base_dissonance, "Refrain": refrain_increment,
        "originPlane": "fixture:origin", "target": copy.deepcopy(target),
        "components": ["V", "S"], "componentsStatus": "TEST_ONLY ordinary verbal/somatic declaration; no focus or material component is asserted.",
        "Dissonance": actor["Dissonance"],
        "DissonanceAfterCast": actor["Dissonance"], "RefrainAfterCast": actor["Refrain"],
        "preparedFamiliesUsedAfterCast": copy.deepcopy(actor["preparedFamiliesUsed"]),
    }
    actor["spellHistory"].append(history)
    if concentration:
        started = state["clock"]["elapsedSeconds"]
        effect = {"id": cast_id, "spellId": spell_id, "owner": "B", "rootPlane": "fixture:origin",
                  "rootCastId": cast_id, "rank": rank, "active": True, "suppressed": False,
                  "deadline": round(started + 600, 6), "concentration": True, "target": None,
                  "createdAt": started, "terminalReceipt": None, "visibleBoundary": False,
                  "space": None, "originPlane": "fixture:origin"}
        state["effects"][cast_id] = effect
        actor["concentration"] = {"effectId": cast_id, "spellId": spell_id,
                                   "startedAtSeconds": started,
                                   "deadlineSeconds": round(started + 600, 6), "active": True}
    if check_face is not None:
        check_total = check_face + 11
        dc = 10 + 9
        success = check_total >= dc
        if success != outcome.startswith("SUCCESS"):
            raise AssertionError(f"Declared check result does not match outcome for {cast_id}")
    else:
        check_total = None
        dc = None
        success = None
    event_id = f"{CASE_ID}:CAST:{at:.1f}:{spell_id}"
    state["time"] = at
    state["processedEventIds"].append(event_id)
    detail = {
        "castId": cast_id, "casterId": "B", "spellId": spell_id, "spellRank": rank,
        "preparedAcquisitionVerified": True, "actionAvailableBeforeCast": True,
        "actionSpent": True, "baseCostRP": cost, "discount": False,
        "rpBefore": before["actors"]["B"]["RP"], "rpAfter": actor["RP"],
        "counterspellWindows": counterspell_windows(at),
        "perceptionAndTargeting": copy.deepcopy(target),
        "abilityCheck": None if check_face is None else {
            "type": "TEST_ONLY_DECLARED_INTELLIGENCE_CHECK", "face": check_face,
            "abilityModifier": 5, "proficiencyBonus": 6, "total": check_total,
            "targetRank": 9, "dc": dc, "success": success,
        },
        "outcome": outcome, "fortressRootBeforeCastActive": True,
        "rechargeAfterCast": copy.deepcopy(actor["recharge"][spell_id]),
        "spellEfficiencyAfterCast": copy.deepcopy(actor["spellEfficiency"]),
        "strain": {"firstPreparedFamily": first, "baseDissonance": base_dissonance,
                   "repeatIncrement": refrain_increment, "dissonanceAfter": actor["Dissonance"],
                   "refrainAfter": actor["Refrain"]},
    }
    if spell_id == SIGHT:
        detail["auraPerception"] = {
            "effectId": ROOT_EFFECT_ID, "association": "TEST_ONLY association to the existing Fortress root",
            "auraSchoolOrCategory": "Conjuration", "visibleExteriorManifestation": [10, 4, 7],
            "examinationActionUsed": False,
            "basis": "Arcane Sight perceives magical auras within 60 feet; later examination is not needed merely to perceive.",
        }
    if outcome.startswith("SUCCESS"):
        settle_fortress(state, at, cast_id)
        detail["terminalSettlement"] = copy.deepcopy(state["effects"][ROOT_EFFECT_ID]["terminalReceipt"])
    rationale = (
        "Pay the actual TEST_ONLY Action spell cost before the interrupt window; record eligible and ineligible responders separately; "
        "then resolve the declared ability-check result and only the source-supported consequence."
    )
    ev = intake.make_transition(
        event_id, "TEST_ONLY_CAST_AND_RESOLUTION", before, state,
        {"initiativeSeconds": at, "worldElapsedSeconds": state["clock"]["elapsedSeconds"]},
        ["sources/WIZARD_ARCH_DISPEL_SOURCE.json#/card",
         "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json#/acquisitionLedger",
         "sources/wizard.json#/cards/17,19,21",
         "rules/PG328_PROCEDURE_CURRENT.json#PG9-Q07,PG9-Q27"], rationale,
    )
    ev["forward"] = copy.deepcopy(ev["forward"])
    ev["inverse"] = copy.deepcopy(ev["inverse"])
    ev["detail"] = detail
    case["events"].append(ev)
    if intake.apply_ops(before, ev["forward"]) != state or intake.apply_ops(state, ev["inverse"]) != before:
        raise AssertionError(f"Cast replay failed: {event_id}")


def settle_fortress(state: dict, at: float, dispel_cast_id: str) -> None:
    effect = state["effects"][ROOT_EFFECT_ID]
    space = state["spaces"][SPACE_ID]
    prior_anchor = effect["originAnchor"]
    exterior = prior_anchor
    interior = effect["apertures"][1]["center"]
    admission = state["transitReceipts"][0]
    after_admission = admission["bodyBoxes"]["A"]
    a_pos = state["actors"]["A"]["position"]
    offset = [round(a_pos[i] - interior[i], 6) for i in range(3)]
    terminal_anchor = [round(exterior[i] + offset[i], 6) for i in range(3)]
    if offset != [5, 0, 0] or terminal_anchor != [15, 0, 0]:
        raise AssertionError(f"Unexpected PG9-Q27 anchor derivation: {offset} -> {terminal_anchor}")
    if after_admission != [5, 5, 6] or a_pos != [15, 10, 0]:
        raise AssertionError("Bound actor body or post-admission location changed")
    origin = state["spaces"]["fixture:origin"]
    bounds = origin["bounds"]
    support = origin["support"]
    half_x, half_y, height = 2.5, 2.5, 6
    if not (bounds[0] <= terminal_anchor[0] - half_x and terminal_anchor[0] + half_x <= bounds[1]
            and bounds[2] <= terminal_anchor[1] - half_y and terminal_anchor[1] + half_y <= bounds[3]
            and bounds[4] <= terminal_anchor[2] and terminal_anchor[2] + height <= bounds[5]
            and support["bounds"][0] <= terminal_anchor[0] - half_x
            and terminal_anchor[0] + half_x <= support["bounds"][1]
            and support["bounds"][2] <= terminal_anchor[1] - half_y
            and terminal_anchor[1] + half_y <= support["bounds"][3]
            and abs(terminal_anchor[2] - support["z"]) <= 1e-8):
        raise AssertionError("Returned body does not fit entirely on the preserved origin support")
    for other_id in ("B", "C", "D"):
        other = state["actors"][other_id]
        ox, oy, oz = other["position"]
        obx, oby, oh = other["bodyBox"]
        overlap_x = abs(terminal_anchor[0] - ox) < (half_x + obx / 2)
        overlap_y = abs(terminal_anchor[1] - oy) < (half_y + oby / 2)
        overlap_z = terminal_anchor[2] < oz + oh and oz < terminal_anchor[2] + height
        if overlap_x and overlap_y and overlap_z:
            raise AssertionError(f"Returned A overlaps actor {other_id}")
    settled_actor = {
        "actorId": "A", "fromPlane": SPACE_ID, "toPlane": "fixture:origin",
        "sourcePosition": copy.deepcopy(a_pos), "position": terminal_anchor,
        "bodyBoxFeet": [5, 5, 6], "wholeBodyFit": True,
        "support": "existing continuous origin support at z=0; full 5x5 footprint checked within support bounds",
        "placementConflicts": [], "historicalPreEntryPositionPreserved": [5, 0, 0],
    }
    carried = ["focus-A", "pack-A", "cargo-A"]
    for item_id in carried:
        item = state["items"][item_id]
        if item["plane"] != SPACE_ID or item["owner"] != "A":
            raise AssertionError(f"Carried item binding changed: {item_id}")
        item["plane"] = "fixture:origin"
    state["actors"]["A"]["plane"] = "fixture:origin"
    state["actors"]["A"]["position"] = terminal_anchor
    state["actors"]["A"]["placementConflict"] = False
    space["exists"] = False
    effect["active"] = False
    effect["open"] = False
    effect["terminalReceipt"] = {
        "id": CASE_ID + "/fortress-terminal-settlement",
        "cause": "successful TEST_ONLY Dispel Magic against the rank-9 root effect",
        "sourceRule": "rules/PG328_PROCEDURE_CURRENT.json#PG9-Q27",
        "initiativeSeconds": at,
        "worldElapsedSeconds": state["clock"]["elapsedSeconds"],
        "rootEffectId": ROOT_EFFECT_ID,
        "dispelCastId": dispel_cast_id,
        "settledActors": [settled_actor], "settledCarriedItems": carried,
        "settledExactlyOnce": True,
        "anchorDerivation": {
            "exteriorEntranceWorldPose": exterior,
            "interiorEntrancePose": interior,
            "postAdmissionPosition": a_pos,
            "stableInteriorOffset": offset,
            "alignedCoordinateAxes": True,
            "derivedExteriorClosureAnchor": terminal_anchor,
            "historicalPreEntryPosition": [5, 0, 0],
            "historicalPositionUsedAsAnchor": False,
        },
        "completeLowerCapAndOtherGeneratedGeometryEnded": True,
    }
    state["transitReceipts"].append({
        "id": CASE_ID + "/terminal-return-1", "source": ROOT_EFFECT_ID,
        "group": ["A"], "origin": SPACE_ID, "destination": "fixture:origin",
        "forced": True, "failure": None, "committedMovement": 0, "wholeFit": True,
        "cargo": carried, "approachMovement": 0, "bodyBoxes": {"A": [5, 5, 6]},
        "relativeOffsets": {"A": [0, 0, 0]},
        "support": "existing continuous origin support under the full returned body footprint",
    })
    state["effectReceipts"].append({
        "id": CASE_ID + "/effect-ended", "effectId": ROOT_EFFECT_ID,
        "cause": "successful TEST_ONLY Dispel Magic", "atInitiativeSeconds": at,
        "worldElapsedSeconds": state["clock"]["elapsedSeconds"],
        "generatedSpaceEnded": SPACE_ID, "settledActorIds": ["A"],
        "settledItemIds": carried, "sourceAuthority": "PG9-Q27",
    })


def load_parent() -> tuple[dict, bytes]:
    archive = PAYLOAD / "authority/PG328_HELD_ARCHIVE.zip"
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() is not None:
            raise AssertionError("Parent held archive failed CRC verification")
        raw = zf.read(PARENT_MEMBER)
    case = json.loads(raw.decode("utf-8"))
    if case["id"] != PARENT_ID or sha(case["final"]) != case["finalSHA256"]:
        raise AssertionError("Parent case id/final hash mismatch")
    if case["final"]["time"] != 0.9 or case["final"]["clock"]["elapsedSeconds"] != 1.0:
        raise AssertionError("Parent time bridge differs from the reviewed branch")
    return case, raw


def make_payload() -> dict:
    if (OUTPUT / ARCHIVE_NAME).exists():
        raise SystemExit(f"Refusing to overwrite an already-built packet: {OUTPUT}")
    PAYLOAD.mkdir(parents=True, exist_ok=True)
    intake_payload = ROOT / "conjure_demiplane_fortress_closure_intake_367/payload"
    source_map = {
        "sources/WIZARD_ARCH_DISPEL_SOURCE.json": "sources/WIZARD_ARCH_DISPEL_SOURCE.json",
        "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json": "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json",
        "sources/wizard.json": "sources/wizard.json",
        "sources/COMBAT_ACTION_PLAYTEST.md": "sources/COMBAT_ACTION_PLAYTEST.md",
        "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt",
        "rules/PG328_PROCEDURE_CURRENT.json": "rules/PG328_PROCEDURE_CURRENT.json",
    }
    for dst, src in source_map.items():
        target = PAYLOAD / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(intake_payload / src, target)
    (PAYLOAD / "authority").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(intake_payload / "authority/PG328_HELD_ARCHIVE.zip", PAYLOAD / "authority/PG328_HELD_ARCHIVE.zip")
    parent, parent_raw = load_parent()
    profile = json.loads((PAYLOAD / "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json").read_text(encoding="utf-8-sig"))
    wizard = json.loads((PAYLOAD / "sources/wizard.json").read_text(encoding="utf-8-sig"))
    if profile["acquisitionLedger"][2]["choices"][1]["id"] != SIGHT:
        raise AssertionError("Bound selected Arcane Sight acquisition changed")
    if profile["acquisitionLedger"][8]["choices"][0]["id"] != DISPEL:
        raise AssertionError("Bound selected Arch Dispel acquisition changed")
    if SIGHT not in profile["alwaysPrepared"] or DISPEL not in profile["alwaysPrepared"]:
        raise AssertionError("Bound selected spells are not in the preserved prepared set")
    if wizard["cards"][21]["id"] != SIGHT or wizard["cards"][19]["id"] != DISPEL or wizard["cards"][17]["id"] != COUNTERSPELL:
        raise AssertionError("Bound Wizard card IDs no longer match the selected sources")
    if parent["actorProfileBindings"]["Wizard20"] != parent["final"]["actors"]["B"]["profileSHA256"]:
        raise AssertionError("B's bound source profile differs from the preserved parent profile")
    state = copy.deepcopy(parent["final"])
    initial = copy.deepcopy(state)
    case = {
        "id": CASE_ID, "witnessId": "PG328-W07", "blockerId": "PG200-B06",
        "spellId": "conjure-demiplane-fortress", "caseId": PARENT_ID,
        "status": "TEST_ONLY_UNSEALED_FOR_DIRECTOR_REVIEW",
        "kind": "integrated Arch Dispel failure-recharge-success witness",
        "notCampaignOccurrence": True, "notCanonicalOrRuntimeImplementation": True,
        "acceptanceAuthorized": False, "applicationAuthorized": False,
        "parentCaseSHA256": hashlib.sha256(parent_raw).hexdigest(),
        "parentFinalSHA256": parent["finalSHA256"],
        "initial": initial, "initialSHA256": sha(initial), "events": [],
        "fixturePremises": {
            "sourceBranch": PARENT_ID,
            "FortressRootEffectId": ROOT_EFFECT_ID, "generatedSpaceId": SPACE_ID,
            "testOnlyArcaneSightDetection": True,
            "perceivedAuraAssociation": "The visible exterior manifestation belongs to the already existing Fortress root; it does not grant the spell's exact name before Dispel resolves.",
            "targetingFrame": {"plane": "fixture:origin", "normalAxis": "+X at x=10",
                               "apertureWidthAxis": "+Y", "apertureVerticalAxis": "+Z",
                               "exteriorAperture": {"center": [10, 0, 0], "width": 10, "height": 15},
                               "originAnchor": [10, 0, 0], "terrain": []},
            "targetingPoint": {"point": [10, 4, 7], "visibleExteriorManifestation": True,
                               "insideWidthUnderCenteredOrFloorBasedInterpretation": True,
                               "insideHeightUnderCenteredOrFloorBasedInterpretation": True,
                               "rangeOriginWithinBBodyBox": [0, 15, 5.5],
                               "rangeFeet": 14.941553, "within60Feet": True,
                               "rayEquation": "(10t, 15-11t, 5.5+1.5t), 0<=t<=1",
                               "DIntersection": {"t": [0.681818, 0.75], "zFeet": [6.522727, 6.625],
                                                 "DBodyHeightFeet": 6, "clears": True},
                               "otherActorAndItemObstructionCheck": "C is outside the ray corridor; A is in another plane; carried items have no independent world position; terrain is empty."},
            "closureAnchor": {"exteriorEntranceWorldPose": [10, 0, 0],
                              "interiorEntrancePose": [10, 10, 0],
                              "AImmediatelyAfterAdmission": [15, 10, 0],
                              "derivedInteriorOffset": [5, 0, 0],
                              "alignedAxes": True, "derivedExteriorAnchor": [15, 0, 0],
                              "historicalPreEntryPose": [5, 0, 0],
                              "historicalPoseIsNotClosureAnchor": True},
            "rolls": {"type": "TEST_ONLY declared values, not campaign or recovered rolls",
                      "failureFace": 7, "successFace": 8,
                      "modifier": "+11 (INT +5 plus proficiency +6)", "rank9DC": 19},
        },
        "sourceBindings": [],
    }
    source_bindings = []
    for rel, pointers in [
        ("sources/WIZARD_ARCH_DISPEL_SOURCE.json", ["/card"]),
        ("sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json", ["/acquisitionLedger/2/choices/1", "/acquisitionLedger/8/choices/0", "/alwaysPrepared/5", "/alwaysPrepared/6", "/modifiers/INT"]),
        ("sources/wizard.json", ["/cards/17", "/cards/19", "/cards/21"]),
        ("rules/PG328_PROCEDURE_CURRENT.json", ["/procedure", "/sharedContract"]),
        ("sources/COMBAT_ACTION_PLAYTEST.md", ["#time-and-event-ordering"]),
        ("sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt", ["line 5222", "line 5224", "line 5226"]),
        ("authority/PG328_HELD_ARCHIVE.zip", [PARENT_MEMBER]),
    ]:
        f = PAYLOAD / rel
        source_bindings.append({"path": rel, "sha256": file_sha(f), "locators": pointers})
    case["sourceBindings"] = source_bindings

    # Preserve the inherited schedule and process every real marker through the terminal cast.
    timeline: list[tuple[float, int, str, str]] = []
    for aid, actor in initial["actors"].items():
        sch = actor["regularSchedule"]
        t = sch["nextStart"]
        while t <= 19.0 + 1e-8:
            if t > 0.9 + 1e-8:
                timeline.append((round(t, 6), 0, "START", aid))
            t = round(t + sch["period"], 6)
        t = sch["nextEnd"]
        while t <= 19.1 + 1e-8:
            if t > 0.9 + 1e-8:
                timeline.append((round(t, 6), 2, "END", aid))
            t = round(t + sch["period"], 6)
    for t, spell_id, cast_id, rank, cost, face, target, outcome, concentration in [
        (1.1, SIGHT, SIGHT_ID, 2, 2, None,
         {"kind": "self", "origin": [0, 15, 5.5], "plane": "fixture:origin"}, "ACTIVE", True),
        (7.1, DISPEL, DISPEL_FAIL_ID, 3, 3, 7,
         {"kind": "ongoing magical effect", "effectId": ROOT_EFFECT_ID,
          "manifestationPoint": [10, 4, 7], "rangeOrigin": [0, 15, 5.5],
          "rangeFeet": 14.941553, "within60Feet": True}, "FAILURE_PRESERVES_FORTRESS", False),
        (19.1, DISPEL, DISPEL_SUCCESS_ID, 3, 3, 8,
         {"kind": "ongoing magical effect", "effectId": ROOT_EFFECT_ID,
          "manifestationPoint": [10, 4, 7], "rangeOrigin": [0, 15, 5.5],
          "rangeFeet": 14.941553, "within60Feet": True}, "SUCCESS_ENDS_FORTRESS", False),
    ]:
        timeline.append((t, 1, "CAST", json.dumps([spell_id, cast_id, rank, cost, face, target, outcome, concentration])))
    timeline.sort(key=lambda x: (x[0], x[1], x[3]))
    casts = {1.1: (SIGHT, SIGHT_ID, 2, 2, None,
                   {"kind": "self", "origin": [0, 15, 5.5], "plane": "fixture:origin"}, "ACTIVE", True),
             7.1: (DISPEL, DISPEL_FAIL_ID, 3, 3, 7,
                   {"kind": "ongoing magical effect", "effectId": ROOT_EFFECT_ID,
                    "manifestationPoint": [10, 4, 7], "rangeOrigin": [0, 15, 5.5],
                    "rangeFeet": 14.941553, "within60Feet": True}, "FAILURE_PRESERVES_FORTRESS", False),
             19.1: (DISPEL, DISPEL_SUCCESS_ID, 3, 3, 8,
                    {"kind": "ongoing magical effect", "effectId": ROOT_EFFECT_ID,
                     "manifestationPoint": [10, 4, 7], "rangeOrigin": [0, 15, 5.5],
                     "rangeFeet": 14.941553, "within60Feet": True}, "SUCCESS_ENDS_FORTRESS", False)}
    for at, priority, kind, actor_or_data in timeline:
        if kind == "START":
            schedule_start(case, state, actor_or_data, at)
        elif kind == "END":
            schedule_end(case, state, actor_or_data, at)
        else:
            spell_id, cast_id, rank, cost, face, target, outcome, concentration = casts[at]
            cast_spell(case, state, at=at, spell_id=spell_id, cast_id=cast_id,
                       rank=rank, cost=cost, check_face=face, target=target,
                       outcome=outcome, concentration=concentration)

    case["final"] = copy.deepcopy(state)
    case["finalSHA256"] = sha(state)
    case["replayAssertions"] = {
        "parentFinalReproducedExactly": True,
        "allScheduledMarkersThrough19_1Processed": True,
        "worldClockAt19_1": state["clock"]["elapsedSeconds"],
        "B_RP": state["actors"]["B"]["RP"],
        "B_Dissonance": state["actors"]["B"]["Dissonance"],
        "B_Refrain": state["actors"]["B"]["Refrain"],
        "SightRecharge": state["actors"]["B"]["recharge"][SIGHT],
        "DispelRecharge": state["actors"]["B"]["recharge"][DISPEL],
        "FortressActive": state["effects"][ROOT_EFFECT_ID]["active"],
        "GeneratedSpaceExists": state["spaces"][SPACE_ID]["exists"],
        "APlane": state["actors"]["A"]["plane"],
        "APosition": state["actors"]["A"]["position"],
        "ReturnedCarriedItems": {i: state["items"][i]["plane"] for i in ["focus-A", "pack-A", "cargo-A"]},
        "A_D_Counterspell": "A ineligible cross-plane; D eligible declines; C lacks Wizard Counterspell",
        "allTransitionsForwardAndInverseVerified": True,
        "acceptanceOrApplication": False,
    }
    case_path = PAYLOAD / "case/PG328_W07_REAL_DISPEL_CASE_374.json"
    write_json(case_path, case)

    review = {
        "id": "PG328-W07-374-REVIEW-REQUEST",
        "scope": "Only the W07 real Arch Dispel witness under PG200-B06.",
        "requestedDisposition": "Review the complete source-bound TEST_ONLY witness and identify any remaining repair. If it passes, seal only W07. Do not accept/apply Fortress, adjudicate W03, adopt Sphere B04, change other holds/seals, or alter 828/20/0.",
        "fixture": CASE_ID,
        "parentSource": PARENT_ID,
        "candidateResult": "Dispel failure face7+11=18 at7.1 preserves; successful face8+11=19 at19.1 terminates Fortress and returns A plus all three carried items.",
        "allRollsAndAssumptionsTESTONLY": True,
    }
    write_json(PAYLOAD / "authority/DIRECTOR_REVIEW_REQUEST_374.json", review)
    readme = (
        "# Fortress W07 real Dispel witness 374\n\n"
        "This is a reversible TEST_ONLY branch from the exact Return284 Fortress-B/real-dispel final state. "
        "It records Arcane Sight, a failed then successful rank-9 Dispel check, all inherited regular START/END "
        "markers through initiative 19.1, responder decisions, resource/recharge/strain bookkeeping, and whole-source "
        "terminal settlement. No campaign events or rolls are asserted. The historical parent case and W03 fixture "
        "remain unchanged. No acceptance or application is claimed.\n"
    )
    (PAYLOAD / "README.md").write_text(readme, encoding="utf-8")
    fixture_path = intake_payload / "fixtures/PG328-W03_BENEFICIAL_SHORT_REST_367_TESTONLY.json"
    fixture_sha = file_sha(fixture_path)
    owner_p368 = json.loads((ROOT / "conjure_demiplane_fortress_closure_intake_367/OWNER_P368_W03_TESTONLY_AUTHORIZATION_372.json").read_text(encoding="utf-8"))
    if owner_p368["scope"]["fixtureSha256"] != fixture_sha:
        raise AssertionError("W03 fixture hash no longer matches the explicit P368 owner authorization")
    failed_cast = next(e for e in case["events"] if e.get("detail", {}).get("abilityCheck") and e["detail"]["abilityCheck"]["face"] == 7)
    success_cast = next(e for e in case["events"] if e.get("detail", {}).get("abilityCheck") and e["detail"]["abilityCheck"]["face"] == 8)
    checks = [
        {"id": "parent-final-exact", "passed": case["parentFinalSHA256"] == parent["finalSHA256"]},
        {"id": "selected-source-cards-and-acquisition", "passed": profile["acquisitionLedger"][2]["choices"][1]["id"] == SIGHT and profile["acquisitionLedger"][8]["choices"][0]["id"] == DISPEL and SIGHT in profile["alwaysPrepared"] and DISPEL in profile["alwaysPrepared"]},
        {"id": "28-forward-inverse-replays", "passed": len(case["events"]) == 28 and all(intake.apply_ops(e["before"], e["forward"]) == e["after"] and intake.apply_ops(e["after"], e["inverse"]) == e["before"] for e in case["events"])},
        {"id": "full-scheduled-marker-continuity", "passed": {a: len(state["actors"][a]["regularSchedule"]["starts"]) for a in "ABCD"} == {"A": 4, "B": 4, "C": 3, "D": 3} and {a: len(state["actors"][a]["regularSchedule"]["ends"]) for a in "ABCD"} == {"A": 4, "B": 3, "C": 3, "D": 3}},
        {"id": "declared-rolls", "passed": failed_cast["detail"]["abilityCheck"]["total"] == 18 and failed_cast["detail"]["abilityCheck"]["success"] is False and success_cast["detail"]["abilityCheck"]["total"] == 19 and success_cast["detail"]["abilityCheck"]["success"] is True},
        {"id": "rp-strain-and-recharge", "passed": state["actors"]["B"]["RP"] == 72 and state["actors"]["B"]["Dissonance"] == 2 and state["actors"]["B"]["Refrain"] == 1 and state["actors"]["B"]["recharge"][DISPEL]["roundsUntilReady"] == 2 and state["actors"]["B"]["recharge"][SIGHT]["ready"] is True},
        {"id": "whole-source-termination-and-return", "passed": not state["effects"][ROOT_EFFECT_ID]["active"] and not state["spaces"][SPACE_ID]["exists"] and state["actors"]["A"]["plane"] == "fixture:origin" and state["actors"]["A"]["position"] == [15, 0, 0] and all(state["items"][i]["plane"] == "fixture:origin" for i in ["focus-A", "pack-A", "cargo-A"])},
        {"id": "independent-concentration-persists", "passed": state["actors"]["B"]["concentration"]["effectId"] == SIGHT_ID and state["actors"]["B"]["concentration"]["active"] is True},
        {"id": "queue-canon-fixture-preserved", "passed": fixture_sha == "d0ef9a698b2fdfd0c18b5b881b7e3448cc5b314d9306a9b70fd4c795eed547f7"},
    ]
    if not all(check["passed"] for check in checks):
        raise AssertionError("Independent W07 packet audit failed: " + json.dumps([c for c in checks if not c["passed"]]))
    write_json(PAYLOAD / "authority/INDEPENDENT_AUDIT_374.json", {
        "id": "PG328-W07-REAL-DISPEL-374-INDEPENDENT-AUDIT",
        "result": "PASS_TESTONLY_WITNESS_PACKET_INTEGRITY_AND_REPLAY",
        "checks": checks,
        "w03Fixture367SHA256": fixture_sha,
        "w03FixtureCopiedOrMutated": False,
        "spellQueueMutation": False,
        "canonicalMutation": False,
        "acceptanceOrApplication": False,
    })
    manifest_files = [p for p in PAYLOAD.rglob("*") if p.is_file() and p.name != "MANIFEST.json"]
    manifest = {
        "id": "PG328-W07-REAL-DISPEL-374-MANIFEST",
        "caseId": CASE_ID,
        "parentCaseId": PARENT_ID,
        "payloadFileCount": len(manifest_files) + 1,
        "files": [{"path": p.relative_to(PAYLOAD).as_posix(), "bytes": p.stat().st_size, "sha256": file_sha(p)}
                  for p in sorted(manifest_files)],
        "sha256Algorithm": "SHA-256",
        "deterministicStateHashAlgorithm": "UTF-8 JSON sorted keys compact separators",
    }
    write_json(PAYLOAD / "MANIFEST.json", manifest)
    archive_path = OUTPUT / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in sorted(PAYLOAD.rglob("*")):
            if f.is_file():
                zf.write(f, f"payload/{f.relative_to(PAYLOAD).as_posix()}")
    if zipfile.ZipFile(archive_path).testzip() is not None:
        raise AssertionError("Generated archive failed CRC validation")
    delivery = {
        "id": "PG328-W07-REAL-DISPEL-374-DELIVERY",
        "targetId": "conjure-demiplane-fortress", "witnessId": "PG328-W07",
        "blockerId": "PG200-B06", "status": "TEST_ONLY_UNSEALED_FOR_DIRECTOR_REVIEW",
        "archive": {"fileName": ARCHIVE_NAME, "bytes": archive_path.stat().st_size,
                    "sha256": file_sha(archive_path)},
        "payloadFileCount": manifest["payloadFileCount"],
        "parentCaseId": PARENT_ID, "parentFinalSHA256": parent["finalSHA256"],
        "w03Fixture367SHA256": fixture_sha, "w03FixtureMutated": False,
        "requestedDirectorAction": review["requestedDisposition"],
        "acceptanceAuthorized": False, "applicationAuthorized": False,
        "queueBeforeAndAfter": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
        "preservation": {"W03": "OPEN; no fixture mutation", "B04": "unchanged", "otherHoldsAndSeals": "unchanged"},
    }
    write_json(OUTPUT / DELIVERY_NAME, delivery)
    # Bind the external delivery record after it exists, in a sidecar manifest.
    write_json(OUTPUT / "BUILD_VALIDATION_374.json", {
        "caseFile": str(case_path.relative_to(ROOT).as_posix()),
        "caseSHA256": file_sha(case_path), "finalStateSHA256": case["finalSHA256"],
        "archiveSHA256": file_sha(archive_path), "deliverySHA256": file_sha(OUTPUT / DELIVERY_NAME),
        "eventCount": len(case["events"]), "forwardInverseReplay": "PASS",
        "parentFinalHash": parent["finalSHA256"], "fixture367Unchanged": True,
        "worldElapsedAtTerminal": state["clock"]["elapsedSeconds"],
        "finalRpB": state["actors"]["B"]["RP"], "finalDissonanceB": state["actors"]["B"]["Dissonance"],
        "finalRefrainB": state["actors"]["B"]["Refrain"], "fortressEnded": not state["effects"][ROOT_EFFECT_ID]["active"],
        "spellQueueMutation": False, "canonicalMutation": False,
    })
    return {"archive": str(archive_path), "delivery": str(OUTPUT / DELIVERY_NAME),
            "archiveBytes": archive_path.stat().st_size, "archiveSha256": file_sha(archive_path),
            "caseSHA256": file_sha(case_path), "events": len(case["events"]),
            "finalStateSHA256": case["finalSHA256"], "finalWorldTime": state["clock"]["elapsedSeconds"]}


if __name__ == "__main__":
    print(json.dumps(make_payload(), indent=2))
