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
REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
import build_fortress_closure_intake_367 as intake  # noqa: E402


CASE_ID = "PG328-W06-PERMISSIONS-REENTRY-375-REPACK03-TESTONLY"
WITNESS_ID = "PG328-W06"
PARENT_ID = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/permissions-reentry"
PARENT_MEMBER = (
    "evidence/packet328/prior/Return284_cases/"
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A__permissions-reentry.json"
)
ROOT_EFFECT_ID = PARENT_ID + "/cast1"
SPACE_ID = PARENT_ID + "/cast1/space"
OUTPUT = ROOT / "fortress_w06_permissions_reentry_375_repack03"
PAYLOAD = OUTPUT / "payload"
ARCHIVE_NAME = "DD_Rank9_ConjureDemiplaneFortress_W06_PermissionsReentry_375_Repack03_TESTONLY.zip"
DELIVERY_NAME = "DD_Rank9_ConjureDemiplaneFortress_W06_PermissionsReentry_375_Repack03_DELIVERY.json"

SRC_Q25 = "w06.source.fortress.pg9-q25"
SRC_Q05 = "w06.source.gate.pg9-q05"
SRC_Q11 = "w06.source.absolute-gate.pg9-q11"
SRC_Q06 = "w06.source.gate.pg9-q06"
SRC_Q12 = "w06.source.gate.pg9-q12"
SRC_COMBAT_START = "w06.source.combat.regular-start"
SRC_COMBAT_END = "w06.source.combat.regular-end"
SRC_COMBAT_MOVEMENT = "w06.source.combat.movement-metric"
SRC_COMBAT_DASH = "w06.source.combat.dash-action"
SRC_BODY_EQUIPMENT = "w06.source.body-equipment.carrying"
SRC_COVERAGE = "w06.authority.intake367-witnesspart"
SRC_BLOCKER = "w06.authority.return328-blocker"
SRC_PARENT = "w06.authority.parent-case"
SRC_QUEUE = "w06.authority.queue361"

TRAVELERS = ["A", "B"]
GLYPH = [18, 12.5, 3]
GLYPH_MOUNT_BOUNDS = {"min": [17.75, 12.5, 0], "max": [18.25, 13, 3.25]}
ORIGIN_APERTURE_CENTER = [10, 0, 0]
INTERIOR_APERTURE_CENTER = [10, 10, 0]
ORIGIN_CROSSING_POSE = [5, 0, 0]
INTERIOR_CROSSING_POSE = [15, 10, 0]
BODY_BOX = [5, 5, 6]
CARGO_BOUNDS = {
    "focus": {"min": [-2.5, -2.5, 0], "max": [-2.0, -2.0, 0.5]},
    "pack": {"min": [2.0, -2.5, 0], "max": [2.5, -2.0, 0.5]},
    "cargo": {"min": [-0.5, -0.5, 0], "max": [0.5, 0.5, 1.0]},
}


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


def json_pointer_value(document: object, pointer: str) -> object:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise AssertionError(f"Invalid JSON Pointer: {pointer}")
    value = document
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def validate_source_bindings(bindings: list[dict]) -> None:
    binding_ids = {binding["id"] for binding in bindings}
    if len(binding_ids) != len(bindings):
        raise AssertionError("Duplicate W06 source binding ID")
    for binding in bindings:
        path = PAYLOAD / binding["path"]
        if not path.is_file() or file_sha(path) != binding["sha256"]:
            raise AssertionError(f"Missing or changed W06 source: {binding['path']}")
        for locator in binding["locators"]:
            kind = locator["kind"]
            if kind == "json_pointer":
                document = json.loads(path.read_text(encoding="utf-8-sig"))
                value = json_pointer_value(document, locator["pointer"])
                if "paragraphLabel" in locator and locator["paragraphLabel"] not in str(value):
                    raise AssertionError(f"Missing {locator['paragraphLabel']} at {binding['path']}#{locator['pointer']}")
            elif kind == "text_line":
                lines = path.read_text(encoding="utf-8-sig").splitlines()
                number = locator["line"]
                if number < 1 or number > len(lines) or locator["expectedContains"] not in lines[number - 1]:
                    raise AssertionError(f"Invalid text binding {binding['path']}:{number}")
            elif kind == "zip_member":
                with zipfile.ZipFile(path) as archive:
                    if locator["member"] not in archive.namelist():
                        raise AssertionError(f"Missing parent member {locator['member']}")
            else:
                raise AssertionError(f"Unknown W06 locator kind {kind}")


def add_event(case: dict, state: dict, event_id: str, kind: str, at: float,
              detail: dict, rationale: str, sources: list[str], mutate) -> dict:
    before = copy.deepcopy(state)
    advance_clock(state, at)
    mutate(state)
    state["time"] = at
    state["processedEventIds"].append(event_id)
    after = copy.deepcopy(state)
    event = intake.make_transition(
        event_id, kind, before, after,
        {"initiativeSeconds": at, "worldElapsedSeconds": state["clock"]["elapsedSeconds"]},
        sources, rationale,
    )
    event["detail"] = copy.deepcopy(detail)
    case["events"].append(event)
    if intake.apply_ops(before, event["forward"]) != after:
        raise AssertionError(f"Forward replay failed for {event_id}")
    if intake.apply_ops(after, event["inverse"]) != before:
        raise AssertionError(f"Inverse replay failed for {event_id}")
    return event


def schedule_start(case: dict, state: dict, actor_id: str, at: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if abs(schedule["nextStart"] - at) > 1e-6:
        raise AssertionError(f"Unexpected START {actor_id} {at}; expected {schedule['nextStart']}")
    recharge_before = copy.deepcopy(actor.get("recharge", {}))
    event_id = f"{CASE_ID}:START:{actor_id}:{at:.1f}"
    detail = {
        "actorId": actor_id, "initiativeSeconds": at,
        "nextStartAfterStart": round(at + schedule["period"], 6),
        "pendingNextEndPreserved": schedule["nextEnd"],
        "rechargeBeforeStart": recharge_before,
        "actionBonusReactionMovementRefreshed": True,
    }

    def mutate(s: dict) -> None:
        a = s["actors"][actor_id]
        for record in a.get("recharge", {}).values():
            if record.get("roundsUntilReady", 0) > 0:
                record["roundsUntilReady"] -= 1
            record["ready"] = record.get("roundsUntilReady", 0) == 0
        a.update({"action": 1, "bonusAction": 1, "reaction": 1,
                  "movement": a.get("speed", 30), "magicThisTurn": False})
        a["regularSchedule"]["starts"].append(at)
        a["regularSchedule"]["nextStart"] = round(at + a["regularSchedule"]["period"], 6)
        a["regularSchedule"]["budgetHistory"].append({
            "time": at, "action": a["action"], "BA": a["bonusAction"],
            "Reaction": a["reaction"], "Move": a["movement"],
            "recharge": copy.deepcopy(a.get("recharge", {})),
        })

    event = add_event(case, state, event_id, "REGULAR_START", at, detail,
                      "At this actor's scheduled regular START, refresh its ordinary budgets and preserve its pending END marker. No extra turn or clock pulse is created.",
                      [SRC_COMBAT_START], mutate)
    event["detail"]["rechargeAfterStart"] = copy.deepcopy(state["actors"][actor_id].get("recharge", {}))


def schedule_end(case: dict, state: dict, actor_id: str, at: float) -> None:
    actor = state["actors"][actor_id]
    schedule = actor["regularSchedule"]
    if not schedule["starts"] or abs(schedule["starts"][-1] + schedule["endOffset"] - at) > 1e-6:
        raise AssertionError(f"Unexpected END {actor_id} {at}")
    if abs(schedule["nextEnd"] - at) > 1e-6:
        raise AssertionError(f"END does not match pending marker for {actor_id}: {schedule['nextEnd']} != {at}")
    spell_efficiency = copy.deepcopy(actor.get("spellEfficiency"))
    expire_spell_efficiency = (
        spell_efficiency is not None
        and spell_efficiency.get("until") is not None
        and spell_efficiency["until"] <= at + 1e-8
    )

    def mutate(s: dict) -> None:
        a = s["actors"][actor_id]
        a["regularSchedule"]["ends"].append(at)
        a["regularSchedule"]["nextEnd"] = round(at + a["regularSchedule"]["period"], 6)
        if expire_spell_efficiency:
            a["spellEfficiency"] = None

    event_id = f"{CASE_ID}:END:{actor_id}:{at:.1f}"
    detail = {
        "actorId": actor_id, "initiativeSeconds": at,
        "nextEndBeforeResolution": schedule["nextEnd"],
        "nextEndAfterResolution": round(at + schedule["period"], 6),
        "spellEfficiencyBefore": spell_efficiency,
        "spellEfficiencyExpiredAtThisEnd": expire_spell_efficiency,
        "spellEfficiencyAfter": None if expire_spell_efficiency else spell_efficiency,
        "lastSpellPreserved": actor.get("lastSpell"),
        "noAdditionalTurnCreated": True,
    }
    add_event(case, state, event_id, "REGULAR_END", at, detail,
              "Resolve the actor's already-pending regular END, expire any temporary benefit whose deadline is reached, and then advance it by one period.",
              [SRC_COMBAT_END], mutate)


def movement_cost(path: list[list[float]]) -> float:
    total = 0.0
    for a, b in zip(path, path[1:]):
        deltas = [abs(b[i] - a[i]) for i in range(3)]
        if sum(delta > 1e-8 for delta in deltas) != 1:
            raise AssertionError("W06 movement paths use explicit orthogonal segments only")
        if deltas[2] > 1e-8 or abs(deltas[0] / 5 - round(deltas[0] / 5)) > 1e-8 or abs(deltas[1] / 5 - round(deltas[1] / 5)) > 1e-8:
            raise AssertionError("W06 ground movement must follow five-foot orthogonal grid segments")
        total += sum(deltas)
    return round(total, 6)


def body_bounds(center: list[float], body: list[float] = BODY_BOX) -> tuple[list[float], list[float]]:
    return (
        [center[0] - body[0] / 2, center[1] - body[1] / 2, center[2]],
        [center[0] + body[0] / 2, center[1] + body[1] / 2, center[2] + body[2]],
    )


def positive_volume_overlap(a: tuple[list[float], list[float]], b: tuple[list[float], list[float]]) -> bool:
    return all(min(a[1][i], b[1][i]) - max(a[0][i], b[0][i]) > 1e-8 for i in range(3))


def aabb_clearance(a: tuple[list[float], list[float]], b: tuple[list[float], list[float]]) -> float:
    gaps = [max(a[0][i] - b[1][i], b[0][i] - a[1][i], 0) for i in range(3)]
    return math.sqrt(sum(gap * gap for gap in gaps))


def swept_segment_bounds(start: list[float], end: list[float], body: list[float] = BODY_BOX) -> tuple[list[float], list[float]]:
    first = body_bounds(start, body)
    last = body_bounds(end, body)
    return ([min(first[0][i], last[0][i]) for i in range(3)],
            [max(first[1][i], last[1][i]) for i in range(3)])


def actor_collision_check(state: dict, actor_id: str, plane: str, center: list[float]) -> list[str]:
    bounds = body_bounds(center)
    conflicts = []
    for other_id, other in state["actors"].items():
        if other_id == actor_id or other["plane"] != plane:
            continue
        if positive_volume_overlap(bounds, body_bounds(other["position"], other["bodyBox"])):
            conflicts.append(other_id)
    if conflicts:
        raise AssertionError(f"TEST_ONLY body placement overlaps {conflicts} for {actor_id}")
    return conflicts


def structural_doors(state: dict) -> list[dict]:
    return state["spaces"][SPACE_ID]["doors"]


def assert_fixed_entrance(state: dict) -> None:
    apertures = state["effects"][ROOT_EFFECT_ID]["apertures"]
    expected = [
        {"plane": "fixture:origin", "center": ORIGIN_APERTURE_CENTER, "width": 10, "height": 15},
        {"plane": SPACE_ID, "center": INTERIOR_APERTURE_CENTER, "width": 10, "height": 15},
    ]
    actual = [{key: aperture[key] for key in ("plane", "center", "width", "height")} for aperture in apertures]
    if actual != expected:
        raise AssertionError("The inherited fixed entrance identity, endpoints, or dimensions changed")


def support_and_fit(state: dict, actor_id: str, plane: str, center: list[float]) -> dict:
    actor = state["actors"][actor_id]
    bounds = body_bounds(center, actor["bodyBox"])
    if plane == "fixture:origin":
        space = state["spaces"][plane]
        support = space["support"]
        allowed = space["bounds"]
        support_label = "existing continuous TEST_ONLY origin ground support"
    elif plane == SPACE_ID:
        space = state["spaces"][plane]
        support = space["support"]
        allowed = [space["courtyard"][0], space["courtyard"][1],
                   space["courtyard"][2], space["courtyard"][3], 0, 40]
        support_label = "existing generated-courtyard floor support in the preserved parent space"
    else:
        raise AssertionError(f"Unbound plane {plane}")
    if not (allowed[0] <= bounds[0][0] and bounds[1][0] <= allowed[1]
            and allowed[2] <= bounds[0][1] and bounds[1][1] <= allowed[3]
            and allowed[4] <= bounds[0][2] and bounds[1][2] <= allowed[5]
            and support["bounds"][0] <= bounds[0][0] and bounds[1][0] <= support["bounds"][1]
            and support["bounds"][2] <= bounds[0][1] and bounds[1][1] <= support["bounds"][3]
            and abs(bounds[0][2] - support["z"]) <= 1e-8):
        raise AssertionError(f"{actor_id} body does not fit and receive support at {plane}:{center}")
    cargo = []
    for item_id in actor["equipment"]:
        item = state["items"][item_id]
        kind = item_id.split("-")[0]
        local = CARGO_BOUNDS[kind]
        expected_size = [round(local["max"][i] - local["min"][i], 6) for i in range(3)]
        if item["sizeFeet"] != expected_size or item["owner"] != actor_id or item["custodian"] != actor_id:
            raise AssertionError(f"TEST_ONLY cargo geometry does not match inherited item {item_id}")
        if any(local["min"][i] < -actor["bodyBox"][i] / 2 - 1e-8
               or local["max"][i] > actor["bodyBox"][i] / 2 + 1e-8 for i in range(2)):
            raise AssertionError(f"{item_id} exceeds carrier horizontal bounds")
        if local["min"][2] < 0 or local["max"][2] > actor["bodyBox"][2]:
            raise AssertionError(f"{item_id} exceeds carrier vertical bounds")
        world_min = [round(center[i] + local["min"][i], 6) for i in range(3)]
        world_max = [round(center[i] + local["max"][i], 6) for i in range(3)]
        cargo.append({
            "itemId": item_id, "ownerId": actor_id, "custodianId": actor_id,
            "bodyRelativeBoundsFeet": copy.deepcopy(local),
            "worldBoundsFeetAtEndpoint": {"min": world_min, "max": world_max},
            "fullyInsideCarrierBody": True, "itemPositionFieldRemainsNull": item["position"] is None,
            "identityAndCustodyPreserved": True,
        })
    conflicts = actor_collision_check(state, actor_id, plane, center)
    glyph_mount_receipt = None
    if plane == SPACE_ID:
        glyph_mount = (GLYPH_MOUNT_BOUNDS["min"], GLYPH_MOUNT_BOUNDS["max"])
        if positive_volume_overlap(bounds, glyph_mount):
            raise AssertionError(f"{actor_id} body intersects the TEST_ONLY glyph mount at a crossing endpoint")
        glyph_mount_receipt = {
            "boundsFeet": copy.deepcopy(GLYPH_MOUNT_BOUNDS),
            "positiveVolumeConflict": False,
            "bodyToMountClearanceFeet": round(aabb_clearance(bounds, glyph_mount), 6),
        }
    return {
        "plane": plane, "centerFeet": copy.deepcopy(center),
        "bodyBoxFeet": copy.deepcopy(actor["bodyBox"]),
        "bodyBoundsFeet": {"min": bounds[0], "max": bounds[1]},
        "fullBodySupported": True, "support": support_label,
        "otherActorPositiveVolumeConflicts": conflicts,
        "glyphMountCollisionCheck": glyph_mount_receipt,
        "cargo": cargo,
        "actualCarriedWeightLb": actor["carriedWeightLb"],
        "actualCarriedLoad": actor["carriedLoad"],
        "allCargoInsideTheBodyForThisBoundFixture": True,
    }


def aperture_fit(state: dict, actor_id: str, endpoint: list[float]) -> dict:
    actor = state["actors"][actor_id]
    # Preserve the parent's z=0 aperture coordinate while proving fit under both plausible
    # readings of its "center": a floor/base anchor and a geometric center.
    aperture_min_y, aperture_max_y = endpoint[1] - 5, endpoint[1] + 5
    body_min_y = endpoint[1] - actor["bodyBox"][1] / 2
    body_max_y = endpoint[1] + actor["bodyBox"][1] / 2
    body_min_z = endpoint[2]
    body_max_z = endpoint[2] + actor["bodyBox"][2]
    full_width = body_min_y >= aperture_min_y and body_max_y <= aperture_max_y
    vertical_bounds = {
        "bottomAnchored": [endpoint[2], endpoint[2] + 15],
        "geometricCenter": [endpoint[2] - 7.5, endpoint[2] + 7.5],
    }
    vertical_fits = {
        key: body_min_z >= bounds[0] and body_max_z <= bounds[1]
        for key, bounds in vertical_bounds.items()
    }
    if not (full_width and all(vertical_fits.values())):
        raise AssertionError("Whole body does not fit within the fixed 10x15 entrance")
    vertical_clearance = {
        "bottomAnchored": round(vertical_bounds["bottomAnchored"][1] - body_max_z, 6),
        "geometricCenter": round(vertical_bounds["geometricCenter"][1] - body_max_z, 6),
    }
    return {
        "entranceId": ROOT_EFFECT_ID + "/fixed-entry",
        "center": copy.deepcopy(endpoint), "widthFeet": 10, "heightFeet": 15,
        "widthAxis": "+Y", "verticalAxis": "+Z",
        "apertureBoundsFeet": {"widthY": [aperture_min_y, aperture_max_y],
                               "heightZInterpretations": vertical_bounds},
        "bodyProjectionFeet": {"widthY": [body_min_y, body_max_y],
                               "heightZ": [body_min_z, body_max_z]},
        "bodyWidthFeet": actor["bodyBox"][1], "bodyHeightFeet": actor["bodyBox"][2],
        "wholeBodyAndContainedCargoFit": True,
        "verticalFitsUnderBothInterpretations": vertical_fits,
        "clearance": {"widthEachSideFeet": 2.5,
                      "heightAboveBodyFeetByInterpretation": vertical_clearance,
                      "minimumProvenHeightAboveBodyFeet": min(vertical_clearance.values())},
        "bodyVerticalConvention": "Actor position z is the feet plane; body extends upward by its recorded height.",
        "apertureVerticalConvention": "Unresolved by the parent center field; fit is proven under both readings.",
        "noForcedDisplacement": True,
    }


def move_actor(case: dict, state: dict, *, actor_id: str, at: float,
               path: list[list[float]], purpose: str) -> dict:
    actor = state["actors"][actor_id]
    if path[0] != actor["position"]:
        raise AssertionError(f"Movement path does not start at inherited/current position for {actor_id}")
    cost = movement_cost(path)
    if actor["movement"] + 1e-8 < cost:
        raise AssertionError(f"{actor_id} lacks movement for {cost} ft")
    plane = actor["plane"]
    swept_checks = []
    glyph_mount = (GLYPH_MOUNT_BOUNDS["min"], GLYPH_MOUNT_BOUNDS["max"])
    for start, end in zip(path, path[1:]):
        swept = swept_segment_bounds(start, end, actor["bodyBox"])
        conflicts = []
        for other_id, other in state["actors"].items():
            if other_id == actor_id or other["plane"] != plane:
                continue
            if positive_volume_overlap(swept, body_bounds(other["position"], other["bodyBox"])):
                conflicts.append(other_id)
        if conflicts:
            raise AssertionError(f"TEST_ONLY swept movement intersects actors {conflicts} for {actor_id}")
        glyph_mount_conflict = plane == SPACE_ID and positive_volume_overlap(swept, glyph_mount)
        if glyph_mount_conflict:
            raise AssertionError(f"TEST_ONLY swept movement intersects the glyph mount for {actor_id}")
        courtyard_clearance = None
        if plane == SPACE_ID:
            courtyard = state["spaces"][SPACE_ID]["courtyard"]
            courtyard_clearance = round(min(
                swept[0][0] - courtyard[0], courtyard[1] - swept[1][0],
                swept[0][1] - courtyard[2], courtyard[3] - swept[1][1],
            ), 6)
            if courtyard_clearance <= 0:
                raise AssertionError(f"TEST_ONLY swept body enters the Fortress outer-wall band for {actor_id}")
        swept_checks.append({
            "startCenter": copy.deepcopy(start), "endCenter": copy.deepcopy(end),
            "sweptBodyBoundsFeet": {"min": swept[0], "max": swept[1]},
            "otherActorPositiveVolumeConflicts": conflicts,
            "glyphMountBoundsFeet": {"min": glyph_mount[0], "max": glyph_mount[1]} if plane == SPACE_ID else None,
            "glyphMountPositiveVolumeConflict": glyph_mount_conflict,
            "courtyardClearanceFromFiveFootOuterWallBandFeet": courtyard_clearance,
            "sweptBodyRemainsInsideUnobstructedCourtyard": courtyard_clearance is None or courtyard_clearance > 0,
            "touchingBoundariesDoNotCountAsPositiveVolumeOverlap": True,
        })
    event_id = f"{CASE_ID}:MOVE:{actor_id}:{at:.1f}"
    detail = {
        "actorId": actor_id, "purpose": purpose, "plane": plane,
        "pathFeet": copy.deepcopy(path), "movementMetric": "orthogonal five-foot grid segments",
        "movementCostFeet": cost, "movementBeforeFeet": actor["movement"],
        "movementAfterFeet": round(actor["movement"] - cost, 6),
        "actionSpent": False, "bodyAndCarriedItemsRemainTogether": True,
        "sweptBodyCollisionChecks": swept_checks,
    }
    if plane == "fixture:origin" and actor_id in ("B", "C"):
        max_body_x = max(point[0] for point in path) + actor["bodyBox"][0] / 2
        detail["exteriorEntrancePlaneX"] = 10
        detail["minimumBodyClearanceBeforeEntrancePlaneFeet"] = round(10 - max_body_x, 6)
        detail["pathRemainsOutsideEntrancePlaneWithoutCrossing"] = max_body_x <= 10

    def mutate(s: dict) -> None:
        a = s["actors"][actor_id]
        a["movement"] = round(a["movement"] - cost, 6)
        a["position"] = copy.deepcopy(path[-1])

    sources = [SRC_COMBAT_MOVEMENT, SRC_BODY_EQUIPMENT]
    return add_event(case, state, event_id, "TEST_ONLY_VOLUNTARY_MOVEMENT", at, detail,
                     "Charge actual orthogonal approach movement before any crossing attempt; no spell or portal creates a free relocation.",
                     sources, mutate)


def dash_action(case: dict, state: dict, *, actor_id: str, at: float) -> dict:
    actor = state["actors"][actor_id]
    if actor["action"] != 1:
        raise AssertionError(f"{actor_id} has no Action to Dash")
    speed = actor["speed"]
    movement_before = actor["movement"]
    event_id = f"{CASE_ID}:DASH:{actor_id}:{at:.2f}"
    detail = {
        "actorId": actor_id, "ActionBefore": 1, "ActionAfter": 0,
        "currentSpeedFeet": speed, "movementBeforeFeet": movement_before,
        "DashBonusMovementFeet": speed, "movementAfterFeet": movement_before + speed,
        "noBonusActionOrReactionGranted": True,
    }

    def mutate(s: dict) -> None:
        a = s["actors"][actor_id]
        a["action"] -= 1
        a["movement"] += a["speed"]

    return add_event(case, state, event_id, "TEST_ONLY_DASH_ACTION", at, detail,
                     "Spend the standard Action to Dash and add one current Speed to this regular turn's movement cap.",
                     [SRC_COMBAT_DASH], mutate)


def operator_action(case: dict, state: dict, *, actor_id: str, at: float,
                    operation: str, new_travelers: list[str] | None = None) -> dict:
    effect = state["effects"][ROOT_EFFECT_ID]
    actor = state["actors"][actor_id]
    assert_fixed_entrance(state)
    if actor_id not in effect.get("operators", []):
        raise AssertionError(f"{actor_id} is not a bound operator")
    if actor["plane"] != SPACE_ID or actor["action"] != 1:
        raise AssertionError("Operator action requires a present operator with a refreshed Action")
    if actor["position"] != [15, 15, 0] or GLYPH != [18, 12.5, 3]:
        raise AssertionError("Unexpected operator/control glyph fixture")
    glyph_mount = (GLYPH_MOUNT_BOUNDS["min"], GLYPH_MOUNT_BOUNDS["max"])
    actor_bounds = body_bounds(actor["position"], actor["bodyBox"])
    if positive_volume_overlap(actor_bounds, glyph_mount):
        raise AssertionError("Operator body intersects the TEST_ONLY glyph mount")
    distance = math.sqrt(sum((actor["position"][i] - GLYPH[i]) ** 2 for i in range(3)))
    body_to_glyph = math.sqrt(sum(
        max(actor_bounds[0][i] - GLYPH[i], 0, GLYPH[i] - actor_bounds[1][i]) ** 2
        for i in range(3)))
    if distance > 5:
        raise AssertionError("Operator is not within five feet of the control glyph")
    if operation == "set_named_allowlist":
        if effect["travelerPolicy"] != "public" or new_travelers != TRAVELERS:
            raise AssertionError("The inherited public policy or declared TEST_ONLY allowlist changed")
    elif operation in ("close", "open"):
        expected_open = operation == "close"
        if effect["open"] != expected_open:
            raise AssertionError(f"Operator {operation} is not a real entrance-state change")
    else:
        raise AssertionError(operation)
    event_id = f"{CASE_ID}:OPERATOR:{actor_id}:{operation}:{at:.1f}"
    detail = {
        "actorId": actor_id, "operation": operation,
        "operatorIdentityVerified": True, "operatorId": actor_id,
        "operatorPresentInFortressSpace": actor["plane"] == SPACE_ID,
        "controlGlyphPositionFeet": copy.deepcopy(GLYPH),
        "controlGlyphMountBoundsFeet": copy.deepcopy(GLYPH_MOUNT_BOUNDS),
        "operatorBodyCenterFeet": copy.deepcopy(actor["position"]),
        "operatorCenterDistanceFeet": round(distance, 6),
        "closestOccupiedBodyPointDistanceFeet": round(body_to_glyph, 6),
        "operatorBodyDoesNotIntersectMount": True,
        "measurementConvention": "Both actor-center-to-glyph and occupied-body-to-glyph-point distances are recorded; the TEST_ONLY mount has explicit bounds.",
        "paidAction": True, "actionBefore": actor["action"], "actionAfter": 0,
        "policyBefore": effect["travelerPolicy"],
        "travelerIdsBefore": copy.deepcopy(effect.get("authorizedTravelerIds")),
        "openBefore": effect["open"],
        "openAfter": effect["open"] if operation == "set_named_allowlist" else operation == "open",
        "structuralDoorsBefore": copy.deepcopy(structural_doors(state)),
        "structuralDoorsAfter": copy.deepcopy(structural_doors(state)),
        "structuralDoorsUnchanged": True,
        "fixedEntranceIdentityAndEndpointsUnchanged": True,
        "changesProspectiveOnly": operation == "set_named_allowlist",
        "allValuesAreTESTONLY": True,
    }
    if operation == "set_named_allowlist":
        detail["travelerIdsAfter"] = copy.deepcopy(new_travelers)
        detail["policyAfter"] = "explicit named-ID allowlist"

    def mutate(s: dict) -> None:
        a = s["actors"][actor_id]
        e = s["effects"][ROOT_EFFECT_ID]
        a["action"] -= 1
        if operation == "set_named_allowlist":
            e["travelerPolicy"] = "explicit named-ID allowlist"
            e["authorizedTravelerIds"] = copy.deepcopy(new_travelers)
        else:
            e["open"] = operation == "open"

    return add_event(case, state, event_id, "TEST_ONLY_OPERATOR_CONTROL_ACTION", at, detail,
                     "A present first operator pays one Action at the fixed entrance control glyph; this changes only the TEST_ONLY branch state.",
                     [SRC_Q11, SRC_Q25, SRC_COMBAT_START], mutate)


def check_transit_graph(state: dict, actor_id: str, source_plane: str, destination_plane: str,
                        source_center: list[float], destination_center: list[float]) -> dict:
    actor = state["actors"][actor_id]
    source_support = support_and_fit(state, actor_id, source_plane, source_center)
    destination_support = support_and_fit(state, actor_id, destination_plane, destination_center)
    source_aperture = aperture_fit(state, actor_id, ORIGIN_APERTURE_CENTER)
    destination_aperture = aperture_fit(state, actor_id, INTERIOR_APERTURE_CENTER)
    return {
        "actorId": actor_id, "completeGraph": [actor_id] + list(actor["equipment"]),
        "sourceEndpoint": source_support, "destinationEndpoint": destination_support,
        "originApertureFit": source_aperture, "interiorApertureFit": destination_aperture,
        "wholeGraphFitSupportAndCarryingCapacityPass": True,
        "carriedWeightWithinRecordedPhysicalCapacity": actor["carriedWeightLb"] <= actor["S"] * 15,
        "carriedLoadWithinRecordedInventoryCapacity": actor["carriedLoad"] <= actor["S"],
        "itemOwnersAndCustodiansUnchanged": True,
    }


def cross(case: dict, state: dict, *, actor_id: str, at: float, direction: str) -> dict:
    effect = state["effects"][ROOT_EFFECT_ID]
    actor = state["actors"][actor_id]
    assert_fixed_entrance(state)
    if direction == "enter":
        source_plane, destination_plane = "fixture:origin", SPACE_ID
        source_center, destination_center = ORIGIN_CROSSING_POSE, INTERIOR_CROSSING_POSE
        source_aperture = effect["apertures"][0]
        destination_aperture = effect["apertures"][1]
    elif direction == "exit":
        source_plane, destination_plane = SPACE_ID, "fixture:origin"
        source_center, destination_center = INTERIOR_CROSSING_POSE, ORIGIN_CROSSING_POSE
        source_aperture = effect["apertures"][1]
        destination_aperture = effect["apertures"][0]
    else:
        raise AssertionError(direction)
    if actor["plane"] != source_plane or actor["position"] != source_center:
        raise AssertionError(f"{actor_id} is not at the declared {direction} threshold")
    if not effect["active"] or effect["suppressed"] or not effect["open"]:
        raise AssertionError("The source or required open-state predicate fails")
    allowed = effect.get("authorizedTravelerIds")
    if effect["travelerPolicy"] == "explicit named-ID allowlist" and actor_id not in (allowed or []):
        raise AssertionError(f"Crossing denied for unlisted traveler {actor_id}")
    if effect["travelerPolicy"] == "public" and not allowed:
        pass
    elif effect["travelerPolicy"] != "explicit named-ID allowlist":
        raise AssertionError("Unsupported TEST_ONLY traveler policy")
    if actor["action"] < 0 or actor["movement"] < 5:
        raise AssertionError("Crossing requires five remaining movement feet")
    graph = check_transit_graph(state, actor_id, source_plane, destination_plane, source_center, destination_center)
    movement_before = actor["movement"]
    cargo_ids = list(actor["equipment"])
    transit_id = f"{CASE_ID}/transit-{len(state['transitReceipts']) + 1}"
    event_id = f"{CASE_ID}:CROSS:{actor_id}:{direction}:{at:.1f}"
    detail = {
        "actorId": actor_id, "direction": direction, "transitId": transit_id,
        "sourcePlane": source_plane, "destinationPlane": destination_plane,
        "sourcePosition": copy.deepcopy(source_center), "destinationPosition": copy.deepcopy(destination_center),
        "lastArrivedFromPlaneKeyBefore": actor.get("lastArrivedFromPlaneKey"),
        "lastArrivedFromPlaneKeyAfter": source_plane,
        "sourceEntranceEndpoint": copy.deepcopy(source_aperture),
        "destinationEntranceEndpoint": copy.deepcopy(destination_aperture),
        "rootEffectActive": True, "sourceNotSuppressed": True, "operatorOpen": True,
        "structuralDoorRecords": copy.deepcopy(structural_doors(state)),
        "structuralDoorsUnchanged": True,
        "authorizedTravelerCheck": {"policy": effect["travelerPolicy"], "travelerIds": allowed,
                                    "actorId": actor_id, "authorized": True},
        "movementBaseCostFeet": 5, "movementBeforeFeet": movement_before,
        "movementAfterFeet": round(movement_before - 5, 6),
        "actionSpent": False, "wholeTransitGraph": graph,
        "cargoIdentities": cargo_ids, "cargoPlaneBefore": source_plane, "cargoPlaneAfter": destination_plane,
        "cargoOwnerCustodianAndPositionFieldsPreserved": True,
        "singleAtomicCrossingCommit": True,
        "fixedEndpointsAndEntranceIdentityUnchanged": True,
    }

    def mutate(s: dict) -> None:
        a = s["actors"][actor_id]
        a["movement"] = round(a["movement"] - 5, 6)
        a["plane"] = destination_plane
        a["position"] = copy.deepcopy(destination_center)
        a["lastArrivedFromPlaneKey"] = source_plane
        for item_id in cargo_ids:
            s["items"][item_id]["plane"] = destination_plane
        s["transitReceipts"].append({
            "id": transit_id, "source": ROOT_EFFECT_ID,
            "group": [actor_id], "origin": source_plane, "destination": destination_plane,
            "lastArrivedFromPlaneKey": source_plane,
            "forced": False, "failure": None, "committedMovement": 5,
            "wholeFit": True, "cargo": cargo_ids, "approachMovement": 0,
            "bodyBoxes": {actor_id: copy.deepcopy(a["bodyBox"])},
            "relativeOffsets": {actor_id: [0, 0, 0]},
            "sourcePosition": copy.deepcopy(source_center),
            "destinationPosition": copy.deepcopy(destination_center),
            "sourceSupportFitReceipt": copy.deepcopy(graph["sourceEndpoint"]),
            "destinationSupportFitReceipt": copy.deepcopy(graph["destinationEndpoint"]),
            "sourceAndDestinationApertureFitReceipt": {
                "origin": copy.deepcopy(graph["originApertureFit"]),
                "interior": copy.deepcopy(graph["interiorApertureFit"]),
            },
            "TEST_ONLY_WholeTransitGraph": True,
        })

    return add_event(case, state, event_id, "TEST_ONLY_ATOMIC_WHOLE_GRAPH_CROSSING", at, detail,
                     "Commit one permitted physical passage only after rechecking the active/open source, fixed endpoints, whole-body/cargo fit, capacity, and support; update arrival provenance atomically with the destination state and charge the Gate's five-foot crossing cost.",
                     [SRC_Q05, SRC_Q06, SRC_Q12, SRC_Q25, SRC_BODY_EQUIPMENT], mutate)


def occupant_exit_glyph(case: dict, state: dict, *, actor_id: str, at: float) -> dict:
    effect = state["effects"][ROOT_EFFECT_ID]
    actor = state["actors"][actor_id]
    assert_fixed_entrance(state)
    if actor["plane"] != SPACE_ID or not effect["active"] or actor["action"] != 1:
        raise AssertionError("Exit glyph requires an occupant and an available Action")
    if actor_id in effect.get("operators", []):
        raise AssertionError("The exit-glyph witness must show a non-operator occupant can request exit")
    actor_distance = math.sqrt(sum((actor["position"][i] - GLYPH[i]) ** 2 for i in range(3)))
    actor_bounds = body_bounds(actor["position"], actor["bodyBox"])
    glyph_mount = (GLYPH_MOUNT_BOUNDS["min"], GLYPH_MOUNT_BOUNDS["max"])
    body_to_glyph = math.sqrt(sum(
        max(actor_bounds[0][i] - GLYPH[i], 0, GLYPH[i] - actor_bounds[1][i]) ** 2
        for i in range(3)))
    if positive_volume_overlap(actor_bounds, glyph_mount):
        raise AssertionError("Occupant body intersects the TEST_ONLY glyph mount")
    if actor_distance > 5:
        raise AssertionError("Occupant is outside the fixture glyph interaction range")
    if effect["open"]:
        raise AssertionError("This witness must use the glyph while the entrance is shut")
    event_id = f"{CASE_ID}:EXIT-GLYPH:{actor_id}:{at:.1f}"
    detail = {
        "actorId": actor_id, "occupantPresent": True, "occupantPlane": SPACE_ID,
        "occupantPosition": copy.deepcopy(actor["position"]),
        "glyphPosition": copy.deepcopy(GLYPH), "glyphMountBoundsFeet": copy.deepcopy(GLYPH_MOUNT_BOUNDS),
        "centerDistanceFeet": actor_distance, "bodyToGlyphPointDistanceFeet": round(body_to_glyph, 6),
        "bodyDoesNotIntersectGlyphMount": True,
        "ActionPaid": True, "actionBefore": 1, "actionAfter": 0,
        "entranceOpenBefore": False, "entranceOpenAfter": True,
        "structuralDoorsBefore": copy.deepcopy(structural_doors(state)),
        "structuralDoorsUnchanged": True,
        "shutEntranceOpenedFromWithinByThisAction": True,
        "actorIsOperator": False, "operatorPermissionRequired": False,
        "outwardPassageRequested": True,
        "physicalCrossingMovementCostStillAppliesSeparately": 5,
        "fixedEntranceIdentityAndEndpointsUnchanged": True,
    }

    def mutate(s: dict) -> None:
        s["actors"][actor_id]["action"] -= 1
        s["effects"][ROOT_EFFECT_ID]["open"] = True

    return add_event(case, state, event_id, "TEST_ONLY_OCCUPANT_EXIT_GLYPH_ACTION", at, detail,
                     "An occupant pays an Action to use the always-present interior glyph; it opens a shut entrance and requests outward passage without granting a free crossing.",
                     [SRC_Q25, SRC_COMBAT_START], mutate)


def deny_unlisted_traveler(case: dict, state: dict, *, actor_id: str, at: float) -> dict:
    effect = state["effects"][ROOT_EFFECT_ID]
    actor = state["actors"][actor_id]
    assert_fixed_entrance(state)
    if actor["plane"] != "fixture:origin" or actor["position"] != ORIGIN_CROSSING_POSE:
        raise AssertionError("Denied traveler is not at the exterior aperture")
    if not effect["active"] or effect["suppressed"] or not effect["open"]:
        raise AssertionError("Denial witness requires an otherwise active and open entrance")
    if effect["travelerPolicy"] != "explicit named-ID allowlist":
        raise AssertionError("The explicit allowlist is not active")
    if actor_id in effect.get("authorizedTravelerIds", []):
        raise AssertionError("The chosen denied traveler is authorized")
    fit_receipt = check_transit_graph(state, actor_id, "fixture:origin", SPACE_ID,
                                      ORIGIN_CROSSING_POSE, INTERIOR_CROSSING_POSE)
    movement_before = actor["movement"]
    event_id = f"{CASE_ID}:DENY:{actor_id}:{at:.1f}"
    receipt = {
        "id": f"{CASE_ID}/denial-{actor_id}-open-gate",
        "actorId": actor_id, "time": at,
        "sourceEffectId": ROOT_EFFECT_ID,
        "lastArrivedFromPlaneKeyBefore": actor.get("lastArrivedFromPlaneKey"),
        "lastArrivedFromPlaneKeyAfter": actor.get("lastArrivedFromPlaneKey"),
        "result": "ACCESS_DENIED",
        "publicReason": "The visible TEST_ONLY named-ID list does not include this actor.",
        "privateProtectedStateDisclosed": False,
        "sourceActive": True, "sourceOpen": True, "sourceSuppressed": False,
        "structuralDoorRecords": copy.deepcopy(structural_doors(state)),
        "structuralDoorsUnchanged": True,
        "actorListed": False, "travelerPolicy": effect["travelerPolicy"],
        "fixedEndpointsUnchanged": True,
        "internalTestOnlyFitAudit": fit_receipt,
        "approachMovementPreviouslySpentFeet": 5,
        "crossingMovementAttemptedFeet": 5, "crossingMovementCommittedFeet": 0,
        "movementBeforeAttemptFeet": movement_before,
        "movementAfterAttemptFeet": movement_before,
        "actionSpent": False,
        "positionAndPlaneUnchanged": True,
        "noTransitReceiptCreated": True,
        "knownPermissionFailureSpendsNoCrossingMovement": True,
    }
    detail = copy.deepcopy(receipt)

    def mutate(s: dict) -> None:
        s.setdefault("denialReceipts", []).append(copy.deepcopy(receipt))

    return add_event(case, state, event_id, "TEST_ONLY_KNOWN_PERMISSION_FAILURE", at, detail,
                     "The entrance is open and geometrically usable, but the visible named-ID allowlist excludes C. Record a known failure before crossing commit: the paid approach remains spent and the five-foot crossing cost is not charged.",
                     [SRC_Q06, SRC_Q11, SRC_Q12, SRC_Q25], mutate)


def load_parent(archive_path: Path) -> tuple[dict, bytes]:
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise AssertionError("Parent held archive fails CRC")
        raw = archive.read(PARENT_MEMBER)
    parent = json.loads(raw.decode("utf-8"))
    if parent["id"] != PARENT_ID or sha(parent["final"]) != parent["finalSHA256"]:
        raise AssertionError("W06 parent case/final state binding failed")
    return parent, raw


def make_payload() -> dict:
    if (OUTPUT / ARCHIVE_NAME).exists():
        raise SystemExit(f"Refusing to overwrite an existing W06 packet: {OUTPUT}")
    PAYLOAD.mkdir(parents=True, exist_ok=True)
    intake_payload = ROOT / "conjure_demiplane_fortress_closure_intake_367/payload"
    source_map = {
        "rules/PG328_PROCEDURE_CURRENT.json": intake_payload / "rules/PG328_PROCEDURE_CURRENT.json",
        "authority/COVERAGE_MAP_367.json": intake_payload / "COVERAGE_MAP_367.json",
        "authority/PG328_BLOCKER_REASSESSMENT.json": intake_payload / "authority/PG328_BLOCKER_REASSESSMENT.json",
        "authority/PG328_HELD_DELIVERY.json": intake_payload / "authority/PG328_HELD_DELIVERY.json",
        "authority/CURRENT_SPELL_QUEUE_361.json": intake_payload / "authority/CURRENT_SPELL_QUEUE_361.json",
        "sources/COMBAT_ACTION_PLAYTEST.md": intake_payload / "sources/COMBAT_ACTION_PLAYTEST.md",
        "sources/BODY_EQUIPMENT_PLAYTEST.md": intake_payload / "sources/BODY_EQUIPMENT_PLAYTEST.md",
    }
    for destination, source in source_map.items():
        target = PAYLOAD / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    gate_source = REPO_ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_PLANAR_GATES5_REVIEWED_200.md"
    shutil.copyfile(gate_source, PAYLOAD / "sources/RANK9_PLANAR_GATES5_REVIEWED_200.md")
    parent_archive = intake_payload / "authority/PG328_HELD_ARCHIVE.zip"
    shutil.copyfile(parent_archive, PAYLOAD / "authority/PG328_HELD_ARCHIVE.zip")
    parent, parent_raw = load_parent(parent_archive)
    if parent["final"]["time"] != 0.9 or parent["final"]["clock"]["elapsedSeconds"] != 1.0:
        raise AssertionError("W06 must start from the exact reviewed 0.9 / world 1.0 parent state")
    if parent["final"]["actors"]["A"]["plane"] != SPACE_ID:
        raise AssertionError("Parent A is not inside the bound Fortress space")
    effect0 = parent["final"]["effects"][ROOT_EFFECT_ID]
    if not effect0["active"] or not effect0["open"] or effect0["operators"] != ["A"] or effect0["travelerPolicy"] != "public":
        raise AssertionError("Parent gate state differs from the reviewed public/open first-operator state")
    if len(parent["final"]["transitReceipts"]) != 1:
        raise AssertionError("The exact parent admission receipt is missing")

    state = copy.deepcopy(parent["final"])
    initial = copy.deepcopy(state)
    inherited_structural_doors = copy.deepcopy(structural_doors(state))
    glyph_mount = (GLYPH_MOUNT_BOUNDS["min"], GLYPH_MOUNT_BOUNDS["max"])
    glyph_clearance_a = aabb_clearance(body_bounds([15, 15, 0], state["actors"]["A"]["bodyBox"]), glyph_mount)
    glyph_clearance_b = aabb_clearance(body_bounds(INTERIOR_CROSSING_POSE, state["actors"]["B"]["bodyBox"]), glyph_mount)
    fixture_geo = {
        "kind": "TEST_ONLY_FIXED_ENTRANCE_AND_TRANSIT_FIXTURE",
        "canonicalOrCampaignFact": False,
        "parentCaseId": PARENT_ID,
        "rootEffectId": ROOT_EFFECT_ID,
        "spaceId": SPACE_ID,
        "fixedEntranceId": ROOT_EFFECT_ID + "/fixed-entry",
        "origin": {"plane": "fixture:origin", "center": ORIGIN_APERTURE_CENTER,
                   "widthFeet": 10, "heightFeet": 15, "widthAxis": "+Y", "verticalAxis": "+Z"},
        "interior": {"plane": SPACE_ID, "center": INTERIOR_APERTURE_CENTER,
                     "widthFeet": 10, "heightFeet": 15, "widthAxis": "+Y", "verticalAxis": "+Z"},
        "normalCrossingPoses": {
            "outsideOriginBodyCenter": ORIGIN_CROSSING_POSE,
            "insideFortressBodyCenter": INTERIOR_CROSSING_POSE,
            "actorPositionConvention": "Actor z coordinate is the feet plane; the recorded body box extends upward.",
            "apertureVerticalConvention": "Parent aperture center z=0 has unresolved anchor semantics; body fit is independently proven under bottom-anchored and geometric-center readings.",
            "parentAAdmissionUsesTheSameFiveFeetAfterPlanePose": True,
            "mapping": "aligned fixed entrance frames; the body center moves from five feet before the exterior plane to five feet beyond the interior plane",
        },
        "interiorExitControlGlyph": {
            "positionFeet": GLYPH,
            "mounting": {
                "kind": "TEST_ONLY_BOUNDED_GLYPH_POST",
                "boundsFeet": copy.deepcopy(GLYPH_MOUNT_BOUNDS),
                "baseSupportedOnInheritedCourtyardFloor": GLYPH_MOUNT_BOUNDS["min"][2] == 0,
                "separateCanonicalPlinthOrLandingAsserted": False,
                "collisionModel": "closed AABB; positive-volume overlap blocks actor movement",
            },
            "distanceRule": "shortest Euclidean distance from occupied body box to glyph point, plus actor-center distance recorded for audit",
            "operatorACenterDistanceAfterMove": round(math.sqrt(sum(([15, 15, 0][i] - GLYPH[i]) ** 2 for i in range(3))), 6),
            "occupantBCenterDistanceAtArrival": round(math.sqrt(sum((INTERIOR_CROSSING_POSE[i] - GLYPH[i]) ** 2 for i in range(3))), 6),
            "operatorABodyToMountClearanceFeet": round(glyph_clearance_a, 6),
            "occupantBBodyToMountClearanceFeet": round(glyph_clearance_b, 6),
            "nonIntersectingPathRequirements": [
                "A's approach to its operator pose clears the mount bounds.",
                "B's direct post-reentry route stays within the unobstructed courtyard and avoids positive-volume contact with the mount.",
                "All movement sweeps and crossing endpoints are checked against the five-foot outer-wall band and mount bounds.",
            ],
        },
        "outsideSupport": copy.deepcopy(state["spaces"]["fixture:origin"]["support"]),
        "fortressCourtyard": copy.deepcopy(state["spaces"][SPACE_ID]["courtyard"]),
        "fortressSupport": copy.deepcopy(state["spaces"][SPACE_ID]["support"]),
        "terrainAndInterveningObstructions": [],
        "occupantsAndTheirCarrierRelativeCargoBounds": {},
        "policyVisibility": "The TEST_ONLY named-ID allowlist is posted at the exterior entrance; a denied traveler receives only ACCESS_DENIED, not protected site or ward information.",
    }
    for actor_id, actor in state["actors"].items():
        fixture_geo["occupantsAndTheirCarrierRelativeCargoBounds"][actor_id] = {
            "bodyBoxFeet": copy.deepcopy(actor["bodyBox"]),
            "carrierPositionConvention": "body-box horizontal center at feet plane",
            "items": {
                item_id: {
                    "sizeFeet": copy.deepcopy(state["items"][item_id]["sizeFeet"]),
                    "carrierRelativeBoundsFeet": copy.deepcopy(CARGO_BOUNDS[item_id.split("-")[0]]),
                    "owner": actor_id, "custodian": actor_id,
                    "positionFieldRemainsNull": state["items"][item_id]["position"] is None,
                }
                for item_id in actor["equipment"]
            },
        }

    case = {
        "id": CASE_ID, "witnessId": WITNESS_ID, "blockerId": "PG200-B06",
        "spellId": "conjure-demiplane-fortress", "caseId": PARENT_ID,
        "status": "TEST_ONLY_UNSEALED_FOR_DIRECTOR_REVIEW",
        "kind": "integrated Fortress permissions, entrance controls, exit and re-entry witness",
        "notCampaignOccurrence": True, "notCanonicalOrRuntimeImplementation": True,
        "acceptanceAuthorized": False, "applicationAuthorized": False,
        "parentCaseSHA256": hashlib.sha256(parent_raw).hexdigest(),
        "parentFinalSHA256": parent["finalSHA256"],
        "initial": initial, "initialSHA256": sha(initial), "events": [],
        "fixturePremises": {
            "allNewActorsActionsMovementAndPolicyChangesAreTESTONLY": True,
            "sourceBranch": PARENT_ID,
            "fortressRootEffectId": ROOT_EFFECT_ID, "generatedSpaceId": SPACE_ID,
            "preservedInitialState": {
                "initiativeSeconds": 0.9, "worldElapsedSeconds": 1.0,
                "rootActive": effect0["active"], "entranceOpen": effect0["open"],
                "firstOperatorIds": copy.deepcopy(effect0["operators"]),
                "travelerPolicy": effect0["travelerPolicy"],
                "AInsideAt": copy.deepcopy(state["actors"]["A"]["position"]),
                "itemsAndCustodyInheritedWithoutChange": True,
            },
            "fixedGeometryAndCarrierBounds": fixture_geo,
            "controlContract": {
                "initialPublicPolicy": True,
                "AIsTheInheritedFirstOperator": True,
                "AAmendsProspectivelyToNamedIds": TRAVELERS,
                "listedTravelerBMayEnterExitAndReenter": True,
                "unlistedTravelerCIsDeniedWhileEntranceIsOpen": True,
                "denialOutput": "ACCESS_DENIED only; visible policy explains exclusion without exposing protected data",
                "knownDenialCrossingMovement": 0,
            },
            "structuralDoorRelationship": {
                "entranceRootStateControlsStructuralMainDoor": False,
                "aliasRelationshipEstablished": False,
                "inheritedDoors": inherited_structural_doors,
                "doorRecordsMutated": False,
                "scopeNote": "The root entrance portal is tested independently; inherited Q23 structural doors remain exactly as in the parent.",
            },
            "plannedBranch": [
                "A pays an Action to change public travel prospectively to explicit named-ID A/B.",
                "B pays a Dash Action, spends 40 of 60 available movement feet to approach without crossing, then pays the Gate's five-foot crossing cost to enter with all actual carried items.",
                "A uses a paid operator Action to close the entrance.",
                "B, as an occupant, pays an Action to use the interior exit glyph; it opens the shut entrance, then B pays five crossing movement to exit.",
                "A uses paid operator Actions to close and reopen the fixed entrance.",
                "B re-enters with a new five-foot crossing cost, then routes clear of the bounded glyph post; C pays five feet to approach and is denied while the portal is open, without paying the crossing cost.",
            ],
        },
        "sourceBindings": [],
    }
    case["fixturePremises"]["fixedGeometryAndCarrierBounds"] = fixture_geo
    source_bindings: list[dict] = []

    def bind(source_id: str, rel: str, locators: list[dict]) -> None:
        source_path = PAYLOAD / rel
        source_bindings.append({"id": source_id, "path": rel, "sha256": file_sha(source_path), "locators": locators})

    bind(SRC_Q25, "rules/PG328_PROCEDURE_CURRENT.json",
         [{"kind": "json_pointer", "pointer": "/procedure", "paragraphLabel": "PG9-Q25"}])
    bind(SRC_Q05, "sources/RANK9_PLANAR_GATES5_REVIEWED_200.md",
         [{"kind": "text_line", "line": 207, "expectedContains": "PG9-Q05"}])
    bind(SRC_Q11, "sources/RANK9_PLANAR_GATES5_REVIEWED_200.md",
         [{"kind": "text_line", "line": 539, "expectedContains": "PG9-Q11"}])
    bind(SRC_Q06, "sources/RANK9_PLANAR_GATES5_REVIEWED_200.md",
         [{"kind": "text_line", "line": 209, "expectedContains": "PG9-Q06"}])
    bind(SRC_Q12, "sources/RANK9_PLANAR_GATES5_REVIEWED_200.md",
         [{"kind": "text_line", "line": 213, "expectedContains": "PG9-Q12"}])
    bind(SRC_COMBAT_START, "sources/COMBAT_ACTION_PLAYTEST.md",
         [{"kind": "text_line", "line": 57, "expectedContains": "At a regular turn's **start**"}])
    bind(SRC_COMBAT_END, "sources/COMBAT_ACTION_PLAYTEST.md",
         [{"kind": "text_line", "line": 66, "expectedContains": "At **end**"}])
    bind(SRC_COMBAT_MOVEMENT, "sources/COMBAT_ACTION_PLAYTEST.md",
         [{"kind": "text_line", "line": 164, "expectedContains": "NEW grid metric"}])
    bind(SRC_COMBAT_DASH, "sources/COMBAT_ACTION_PLAYTEST.md",
         [{"kind": "text_line", "line": 78, "expectedContains": "| Dash | Add one current Speed"}])
    bind(SRC_BODY_EQUIPMENT, "sources/BODY_EQUIPMENT_PLAYTEST.md",
         [{"kind": "text_line", "line": 90, "expectedContains": "Use pounds for actual weight"},
          {"kind": "text_line", "line": 94, "expectedContains": "| Carrier size |"}])
    bind(SRC_COVERAGE, "authority/COVERAGE_MAP_367.json",
         [{"kind": "json_pointer", "pointer": "/witnessParts/5", "paragraphLabel": "PG328-W06"}])
    bind(SRC_BLOCKER, "authority/PG328_BLOCKER_REASSESSMENT.json",
         [{"kind": "json_pointer", "pointer": "/remainingWitnessParts/5"}])
    bind(SRC_PARENT, "authority/PG328_HELD_ARCHIVE.zip",
         [{"kind": "zip_member", "member": PARENT_MEMBER}])
    bind(SRC_QUEUE, "authority/CURRENT_SPELL_QUEUE_361.json",
         [{"kind": "json_pointer", "pointer": "/currentAuthority"}])
    validate_source_bindings(source_bindings)
    case["sourceBindings"] = source_bindings

    schedule: list[tuple[float, int, str, str]] = []
    for actor_id, actor in initial["actors"].items():
        record = actor["regularSchedule"]
        start = record["nextStart"]
        while start <= 32.0 + 1e-8:
            if start > 0.9 + 1e-8:
                schedule.append((round(start, 6), 0, "START", actor_id))
            start = round(start + record["period"], 6)
        end = record["nextEnd"]
        while end <= 32.2 + 1e-8:
            if end > 0.9 + 1e-8:
                schedule.append((round(end, 6), 2, "END", actor_id))
            end = round(end + record["period"], 6)

    operations = [
        (1.05, 1, "dash", {"actor": "B"}),
        (1.1, 1, "move", {"actor": "B", "path": [[0, 15, 0], [0, 10, 0], [-5, 10, 0],
                                                   [-5, -5, 0], [5, -5, 0], [5, 0, 0]],
                          "purpose": "use paid Dash movement to route around the other actors and reach the exterior crossing pose without crossing"}),
        (6.05, 1, "move", {"actor": "A", "path": [[15, 10, 0], [15, 15, 0]],
                           "purpose": "move within the interior courtyard to the control position while clearing the bounded glyph post"}),
        (6.1, 1, "operator", {"actor": "A", "operation": "set_named_allowlist", "travelers": TRAVELERS}),
        (7.2, 1, "cross", {"actor": "B", "direction": "enter"}),
        (12.1, 1, "operator", {"actor": "A", "operation": "close"}),
        (13.1, 1, "glyph", {"actor": "B"}),
        (13.2, 1, "cross", {"actor": "B", "direction": "exit"}),
        (18.1, 1, "operator", {"actor": "A", "operation": "close"}),
        (24.1, 1, "operator", {"actor": "A", "operation": "open"}),
        (25.1, 1, "cross", {"actor": "B", "direction": "enter"}),
        (31.1, 1, "move", {"actor": "B", "path": [[15, 10, 0], [20, 10, 0]],
                           "purpose": "use the Director-directed five-foot direct courtyard route after re-entry before C's denied open-portal test"}),
        (32.1, 1, "move", {"actor": "C", "path": [[0, 0, 0], [5, 0, 0]],
                           "purpose": "approach the open exterior entrance before a permission-denied crossing attempt"}),
        (32.2, 1, "deny", {"actor": "C"}),
    ]
    operation_records = [(at, priority, "OP", {"op": operation, "payload": payload})
                         for at, priority, operation, payload in operations]
    timeline: list[tuple[float, int, str, object]] = []
    timeline.extend((at, priority, kind, actor) for at, priority, kind, actor in schedule)
    timeline.extend((at, priority, kind, payload) for at, priority, kind, payload in operation_records)
    timeline.sort(key=lambda item: (item[0], item[1], str(item[3])))

    for at, _, event_kind, value in timeline:
        if event_kind == "START":
            schedule_start(case, state, value, at)
        elif event_kind == "END":
            schedule_end(case, state, value, at)
        else:
            operation, payload = value["op"], value["payload"]
            if operation == "dash":
                dash_action(case, state, actor_id=payload["actor"], at=at)
            elif operation == "move":
                move_actor(case, state, actor_id=payload["actor"], at=at,
                           path=payload["path"], purpose=payload["purpose"])
            elif operation == "operator":
                operator_action(case, state, actor_id=payload["actor"], at=at,
                                operation=payload["operation"], new_travelers=payload.get("travelers"))
            elif operation == "glyph":
                occupant_exit_glyph(case, state, actor_id=payload["actor"], at=at)
            elif operation == "cross":
                cross(case, state, actor_id=payload["actor"], at=at, direction=payload["direction"])
            elif operation == "deny":
                deny_unlisted_traveler(case, state, actor_id=payload["actor"], at=at)
            else:
                raise AssertionError(operation)

    case["final"] = copy.deepcopy(state)
    case["finalSHA256"] = sha(state)
    case["replayAssertions"] = {
        "parentFinalReproducedExactly": case["parentFinalSHA256"] == sha(initial),
        "allForwardInverseTransitionsPass": all(
            intake.apply_ops(event["before"], event["forward"]) == event["after"]
            and intake.apply_ops(event["after"], event["inverse"]) == event["before"]
            for event in case["events"]),
        "fullReverseReplayRestoresParent": True,
        "finalInitiativeSeconds": state["time"],
        "finalWorldElapsedSeconds": state["clock"]["elapsedSeconds"],
        "FortressRootActive": state["effects"][ROOT_EFFECT_ID]["active"],
        "FortressSpaceExists": state["spaces"][SPACE_ID]["exists"],
        "FortressOpen": state["effects"][ROOT_EFFECT_ID]["open"],
        "FortressOperatorIds": state["effects"][ROOT_EFFECT_ID]["operators"],
        "FortressTravelerPolicy": state["effects"][ROOT_EFFECT_ID]["travelerPolicy"],
        "FortressTravelerIds": state["effects"][ROOT_EFFECT_ID].get("authorizedTravelerIds"),
        "BLocationAfterReentry": {"plane": state["actors"]["B"]["plane"], "position": state["actors"]["B"]["position"]},
        "BLastArrivedFromPlaneKeyAfterReentry": state["actors"]["B"]["lastArrivedFromPlaneKey"],
        "BItemsAfterReentry": {item_id: state["items"][item_id]["plane"] for item_id in state["actors"]["B"]["equipment"]},
        "CApproachMovementSpentFeet": 5,
        "CDeniedCrossingMovementSpentFeet": 0,
        "BTransitReceipts": len([r for r in state["transitReceipts"] if r["group"] == ["B"]]),
        "NoAcceptanceOrApplication": True,
        "QueueBeforeAndAfter": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
    }
    case_path = PAYLOAD / "case/PG328_W06_PERMISSIONS_REENTRY_CASE_375_REPACK03_TESTONLY.json"
    write_json(case_path, case)

    source_ids = {binding["id"] for binding in case["sourceBindings"]}
    event_source_ids = {source_id for event in case["events"] for source_id in event["sourceBindings"]}
    starts_by_actor = {actor: len(state["actors"][actor]["regularSchedule"]["starts"]) for actor in "ABCD"}
    ends_by_actor = {actor: len(state["actors"][actor]["regularSchedule"]["ends"]) for actor in "ABCD"}
    b_transits = [receipt for receipt in state["transitReceipts"] if receipt["group"] == ["B"]]
    b_dash = next(event for event in case["events"] if event["kind"] == "TEST_ONLY_DASH_ACTION" and event["detail"]["actorId"] == "B")
    b_first_approach = next(event for event in case["events"] if event["kind"] == "TEST_ONLY_VOLUNTARY_MOVEMENT" and event["detail"]["actorId"] == "B")
    c_approach = next(event for event in case["events"] if event["kind"] == "TEST_ONLY_VOLUNTARY_MOVEMENT" and event["detail"]["actorId"] == "C")
    denial = state["denialReceipts"][0]
    actual_fixture367 = file_sha(intake_payload / "fixtures/PG328-W03_BENEFICIAL_SHORT_REST_367_TESTONLY.json")
    owner_p368 = json.loads((ROOT / "conjure_demiplane_fortress_closure_intake_367/OWNER_P368_W03_TESTONLY_AUTHORIZATION_372.json").read_text(encoding="utf-8"))
    queue361 = json.loads((PAYLOAD / "authority/CURRENT_SPELL_QUEUE_361.json").read_text(encoding="utf-8-sig"))
    if owner_p368["scope"]["fixtureSha256"] != actual_fixture367:
        raise AssertionError("W06 build observed a changed P368-bound W03 fixture")

    reversed_state = copy.deepcopy(state)
    for event in reversed(case["events"]):
        reversed_state = intake.apply_ops(reversed_state, event["inverse"])
    replay_restores = reversed_state == initial
    case["replayAssertions"]["fullReverseReplayRestoresParent"] = replay_restores
    write_json(case_path, case)
    checks = [
        {"id": "exact-parent-state-and-archive-member", "passed": case["parentFinalSHA256"] == parent["finalSHA256"] and sha(initial) == parent["finalSHA256"] and len(parent["events"]) == 9},
        {"id": "all-source-locators-resolve", "passed": len(source_ids) == len(case["sourceBindings"]) and event_source_ids <= source_ids},
        {"id": "forward-inverse-and-complete-reverse-replay", "passed": replay_restores and all(intake.apply_ops(e["before"], e["forward"]) == e["after"] and intake.apply_ops(e["after"], e["inverse"]) == e["before"] for e in case["events"])},
        {"id": "scheduled-markers-and-pending-end-continuity", "passed": starts_by_actor == {"A": 6, "B": 6, "C": 6, "D": 5} and ends_by_actor == {"A": 6, "B": 6, "C": 5, "D": 5} and all(abs(state["actors"][a]["regularSchedule"]["nextEnd"] - (state["actors"][a]["regularSchedule"]["ends"][-1] + 6)) < 1e-8 for a in "ABCD")},
        {"id": "expired-spell-efficiency-clears-at-A-end-6-9", "passed": case["events"][11]["kind"] == "REGULAR_END" and case["events"][11]["detail"]["actorId"] == "A" and case["events"][11]["detail"]["spellEfficiencyExpiredAtThisEnd"] and case["events"][11]["before"]["actors"]["A"]["spellEfficiency"]["until"] == 6.9 and case["events"][11]["after"]["actors"]["A"]["spellEfficiency"] is None and case["events"][11]["before"]["actors"]["A"]["lastSpell"] == case["events"][11]["after"]["actors"]["A"]["lastSpell"] and case["events"][11]["before"]["actors"]["A"]["spellHistory"] == case["events"][11]["after"]["actors"]["A"]["spellHistory"] and all(event["after"]["actors"]["A"]["spellEfficiency"] is None for event in case["events"] if event["after"]["time"] > 6.9)},
        {"id": "approach-dash-cost-and-no-premature-crossing", "passed": b_dash["detail"]["ActionBefore"] == 1 and b_dash["detail"]["ActionAfter"] == 0 and b_dash["detail"]["movementAfterFeet"] == 60 and b_first_approach["detail"]["movementCostFeet"] == 40 and b_first_approach["detail"]["movementAfterFeet"] == 20 and b_first_approach["detail"]["pathRemainsOutsideEntrancePlaneWithoutCrossing"] and b_first_approach["detail"]["minimumBodyClearanceBeforeEntrancePlaneFeet"] == 2.5 and c_approach["detail"]["movementCostFeet"] == 5 and c_approach["detail"]["pathRemainsOutsideEntrancePlaneWithoutCrossing"]},
        {"id": "prospective-permission-change-paid-by-first-operator", "passed": state["effects"][ROOT_EFFECT_ID]["operators"] == ["A"] and state["effects"][ROOT_EFFECT_ID]["travelerPolicy"] == "explicit named-ID allowlist" and state["effects"][ROOT_EFFECT_ID]["authorizedTravelerIds"] == TRAVELERS},
        {"id": "actual-operator-close-and-open-root-entrance-only", "passed": [(e["detail"]["operation"], e["detail"]["openBefore"], e["detail"]["openAfter"]) for e in case["events"] if e["kind"] == "TEST_ONLY_OPERATOR_CONTROL_ACTION" and e["detail"]["operation"] in ("open", "close")] == [("close", True, False), ("close", True, False), ("open", False, True)] and all(e["detail"]["structuralDoorsUnchanged"] and e["detail"]["structuralDoorsBefore"] == inherited_structural_doors and e["detail"]["structuralDoorsAfter"] == inherited_structural_doors for e in case["events"] if e["kind"] == "TEST_ONLY_OPERATOR_CONTROL_ACTION")},
        {"id": "nonoperator-occupant-glyph-opens-shut-portal-and-requests-exit", "passed": sum(e["kind"] == "TEST_ONLY_OCCUPANT_EXIT_GLYPH_ACTION" and e["detail"]["shutEntranceOpenedFromWithinByThisAction"] and e["detail"]["actorIsOperator"] is False and e["detail"]["structuralDoorsUnchanged"] and e["detail"]["bodyDoesNotIntersectGlyphMount"] for e in case["events"]) == 1},
        {"id": "B-enters-exits-and-reenters-with-whole-graph-and-arrival-provenance", "passed": [r["destination"] for r in b_transits] == [SPACE_ID, "fixture:origin", SPACE_ID] and [r["lastArrivedFromPlaneKey"] for r in b_transits] == ["fixture:origin", SPACE_ID, "fixture:origin"] and all(e["detail"]["lastArrivedFromPlaneKeyAfter"] == e["detail"]["sourcePlane"] for e in case["events"] if e["kind"] == "TEST_ONLY_ATOMIC_WHOLE_GRAPH_CROSSING" and e["detail"]["actorId"] == "B") and state["actors"]["B"]["lastArrivedFromPlaneKey"] == "fixture:origin" and state["actors"]["B"]["plane"] == SPACE_ID and all(state["items"][i]["plane"] == SPACE_ID for i in state["actors"]["B"]["equipment"])},
        {"id": "C-known-denial-on-open-root-portal-spends-approach-only", "passed": len(state["denialReceipts"]) == 1 and denial["result"] == "ACCESS_DENIED" and denial["sourceOpen"] and denial["crossingMovementCommittedFeet"] == 0 and denial["approachMovementPreviouslySpentFeet"] == 5 and denial["positionAndPlaneUnchanged"] and denial["noTransitReceiptCreated"] and denial["lastArrivedFromPlaneKeyBefore"] == denial["lastArrivedFromPlaneKeyAfter"]},
        {"id": "fixed-endpoints-active-source-and-custody-preserved", "passed": state["effects"][ROOT_EFFECT_ID]["active"] and state["spaces"][SPACE_ID]["exists"] and structural_doors(state) == inherited_structural_doors and all(event["before"]["spaces"][SPACE_ID]["doors"] == inherited_structural_doors and event["after"]["spaces"][SPACE_ID]["doors"] == inherited_structural_doors for event in case["events"]) and [ap["center"] for ap in state["effects"][ROOT_EFFECT_ID]["apertures"]] == [ORIGIN_APERTURE_CENTER, INTERIOR_APERTURE_CENTER] and all(state["items"][i]["owner"] == "B" and state["items"][i]["custodian"] == "B" for i in state["actors"]["B"]["equipment"])},
        {"id": "glyph-mount-courtyard-wall-band-and-nonintersecting-movement", "passed": fixture_geo["interiorExitControlGlyph"]["positionFeet"] == [18, 12.5, 3] and fixture_geo["interiorExitControlGlyph"]["mounting"]["boundsFeet"] == {"min": [17.75, 12.5, 0], "max": [18.25, 13, 3.25]} and glyph_clearance_a > 0 and glyph_clearance_b > 0 and all(not check["glyphMountPositiveVolumeConflict"] and check["sweptBodyRemainsInsideUnobstructedCourtyard"] for event in case["events"] if event["kind"] == "TEST_ONLY_VOLUNTARY_MOVEMENT" for check in event["detail"]["sweptBodyCollisionChecks"]) and all(not (receipt["destinationSupportFitReceipt"].get("glyphMountCollisionCheck") or {}).get("positiveVolumeConflict", False) and not (receipt["sourceSupportFitReceipt"].get("glyphMountCollisionCheck") or {}).get("positiveVolumeConflict", False) for receipt in b_transits)},
        {"id": "B-post-reentry-direct-five-foot-route", "passed": any(event["kind"] == "TEST_ONLY_VOLUNTARY_MOVEMENT" and event["detail"]["actorId"] == "B" and event["detail"]["pathFeet"] == [[15, 10, 0], [20, 10, 0]] and event["detail"]["movementCostFeet"] == 5 and event["detail"]["movementAfterFeet"] == 25 and all(receipt["courtyardClearanceFromFiveFootOuterWallBandFeet"] == 2.5 for receipt in event["detail"]["sweptBodyCollisionChecks"]) for event in case["events"])},
        {"id": "all-aperture-fit-under-both-vertical-interpretations", "passed": all(all(endpoint["verticalFitsUnderBothInterpretations"].values()) and endpoint["clearance"]["minimumProvenHeightAboveBodyFeet"] == 1.5 for receipt in b_transits for endpoint in receipt["sourceAndDestinationApertureFitReceipt"].values())},
        {"id": "W03-B04-W07-and-authority-queue-unchanged", "passed": actual_fixture367 == owner_p368["scope"]["fixtureSha256"] and queue361["currentAuthority"] == {"reviewedApplied": 828, "pending": 20, "acceptedUnapplied": 0, "completeStandaloneProcedures": 552, "scopedInterfaces": 173} and queue361["pendingCount"] == 20 and queue361["acceptedUnapplied"] == 0},
    ]
    if not all(check["passed"] for check in checks):
        raise AssertionError("Independent W06 audit failed: " + json.dumps([c for c in checks if not c["passed"]], ensure_ascii=False))
    write_json(PAYLOAD / "authority/INDEPENDENT_AUDIT_375.json", {
        "id": "PG328-W06-PERMISSIONS-REENTRY-375-REPACK03-INDEPENDENT-AUDIT",
        "result": "PASS_TESTONLY_WITNESS_PACKET_INTEGRITY_AND_REPLAY",
        "checks": checks, "w03Fixture367SHA256": actual_fixture367,
        "w03FixtureCopiedOrMutated": False, "spellQueueMutation": False,
        "canonicalMutation": False, "acceptanceOrApplication": False,
    })
    review_request = {
        "id": "PG328-W06-375-REPACK03-DIRECTOR-REVIEW-REQUEST",
        "scope": "Only Fortress W06 permissions, closed entrance, interior exit glyph, movement, exit, and re-entry.",
        "authority": {
            "return328": "BLOCKER_REASSESSMENT.json#/remainingWitnessParts/5",
            "intake367": "COVERAGE_MAP_367.json#/witnessParts/5",
            "parentCaseId": PARENT_ID,
            "parentFinalSHA256": parent["finalSHA256"],
        },
        "requestedDisposition": "Review all source bindings and the complete TEST_ONLY W06-only trace. If every requirement passes, seal PG328-W06 only. Fortress identity acceptance/application are out of scope.",
        "reviewPoints": [
            "Exact parent initial binding, preserved fixed entrance and source identity.",
            "Absolute Gate Q11 operator identity, within-five-foot control geometry, actual paid Actions, prospective named traveler allowlist.",
            "Fortress Q25 close/open operations and an occupant using the interior exit glyph while the root portal is shut.",
            "Gate Q05/Q06/Q12 arrival provenance, complete body/cargo fit, support, endpoint rechecks, movement approach and five-foot crossing costs.",
            "The root portal state is independent of the inherited structural doors; every structural door record remains unchanged.",
            "The bounded TEST_ONLY glyph post, all movement sweeps, crossing endpoints, and the five-foot outer-wall band have explicit positive-volume clearance checks.",
            "B enters, exits and re-enters; C pays five feet to approach and is denied at an otherwise open root portal with zero crossing movement committed.",
            "The aperture fits under both bottom-anchor and geometric-center vertical interpretations; nine-foot clearance is not asserted unconditionally.",
            "All regular START/END markers, clocks, hashes, forward/inverse patches and complete reverse restoration.",
            "Manifest/delivery binding, preservation of W03, B04, W07, all other holds/seals, and queue 828/20/0.",
        ],
        "allNewFixtureValuesAreTESTONLY": True,
        "acceptanceAuthorized": False, "applicationAuthorized": False,
        "queueBeforeAndAfter": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
    }
    write_json(PAYLOAD / "authority/DIRECTOR_REVIEW_REQUEST_375.json", review_request)
    readme = (
        "# Fortress W06 permissions and re-entry witness 375 Repack03\n\n"
        "This archive is a reversible TEST_ONLY branch from the exact Return328/Return284 "
        "permissions-reentry parent. It changes only the branch state. A paid first-operator "
        "Action prospectively replaces public travel with a named A/B allowlist; B enters, "
        "an operator closes the root portal, B opens it from within with the bounded exit glyph and exits, "
        "A closes and opens the root portal through paid operator Actions while inherited structural doors stay unchanged, "
        "B re-enters and takes the Director-directed five-foot direct courtyard route clear of the glyph post and outer-wall band, and C is denied at an otherwise open portal after a paid approach. "
        "Every body/cargo endpoint fit, arrival-provenance update, dual-interpreted aperture clearance, glyph mount, movement cost, "
        "custody change, scheduled marker, state hash and inverse "
        "is recorded. None of the branch events is a campaign event or canonical implementation. "
        "No identity-level acceptance or application is requested.\n"
    )
    (PAYLOAD / "README.md").write_text(readme, encoding="utf-8")

    manifest_files = [path for path in PAYLOAD.rglob("*") if path.is_file() and path.name != "MANIFEST.json"]
    manifest = {
        "id": "PG328-W06-PERMISSIONS-REENTRY-375-REPACK03-MANIFEST",
        "caseId": CASE_ID, "parentCaseId": PARENT_ID, "payloadFileCount": len(manifest_files) + 1,
        "files": [{"path": path.relative_to(PAYLOAD).as_posix(),
                   "bytes": path.stat().st_size, "sha256": file_sha(path)}
                  for path in sorted(manifest_files)],
        "sha256Algorithm": "SHA-256",
        "deterministicStateHashAlgorithm": "UTF-8 JSON sorted keys compact separators",
    }
    write_json(PAYLOAD / "MANIFEST.json", manifest)
    archive_path = OUTPUT / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(PAYLOAD.rglob("*")):
            if path.is_file():
                archive.write(path, f"payload/{path.relative_to(PAYLOAD).as_posix()}")
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise AssertionError("W06 archive CRC check failed")
    delivery = {
        "id": "PG328-W06-PERMISSIONS-REENTRY-375-REPACK03-DELIVERY",
        "targetId": "conjure-demiplane-fortress", "witnessId": WITNESS_ID,
        "blockerId": "PG200-B06", "status": "TEST_ONLY_UNSEALED_FOR_DIRECTOR_REVIEW",
        "archive": {"fileName": ARCHIVE_NAME, "bytes": archive_path.stat().st_size,
                    "sha256": file_sha(archive_path)},
        "payloadFileCount": manifest["payloadFileCount"],
        "parentCaseId": PARENT_ID, "parentFinalSHA256": parent["finalSHA256"],
        "w03Fixture367SHA256": actual_fixture367, "w03FixtureMutated": False,
        "requestedDirectorAction": review_request["requestedDisposition"],
        "acceptanceAuthorized": False, "applicationAuthorized": False,
        "queueBeforeAndAfter": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
        "preservation": {
            "W03": "P368-bound fixture unchanged; no W03 state or witness reopened",
            "B04": "unchanged",
            "W07": "Repack02 Director seal unchanged",
            "otherHoldsAndSeals": "unchanged",
            "canonicalRules": "unchanged",
        },
    }
    write_json(OUTPUT / DELIVERY_NAME, delivery)
    write_json(OUTPUT / "BUILD_VALIDATION_375.json", {
        "casePath": case_path.relative_to(ROOT).as_posix(), "caseFileSHA256": file_sha(case_path),
        "finalStateSHA256": case["finalSHA256"], "archiveSHA256": file_sha(archive_path),
        "deliverySHA256": file_sha(OUTPUT / DELIVERY_NAME), "eventCount": len(case["events"]),
        "forwardInverseReplay": "PASS", "fullReverseRestoration": replay_restores,
        "parentFinalHash": parent["finalSHA256"], "fixture367Unchanged": True,
        "finalInitiative": state["time"], "finalWorldElapsed": state["clock"]["elapsedSeconds"],
        "queueMutation": False, "canonicalMutation": False,
    })
    return {
        "archive": str(archive_path), "delivery": str(OUTPUT / DELIVERY_NAME),
        "archiveBytes": archive_path.stat().st_size, "archiveSha256": file_sha(archive_path),
        "caseSHA256": file_sha(case_path), "eventCount": len(case["events"]),
        "finalStateSHA256": case["finalSHA256"],
        "finalInitiative": state["time"], "finalWorldElapsed": state["clock"]["elapsedSeconds"],
    }


if __name__ == "__main__":
    print(json.dumps(make_payload(), indent=2))
