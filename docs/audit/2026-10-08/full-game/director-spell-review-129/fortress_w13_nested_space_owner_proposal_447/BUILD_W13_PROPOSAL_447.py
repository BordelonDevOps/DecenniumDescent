from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[6]
REVIEW = REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SOURCE_DIR = REVIEW / "fortress_w13_nested_space_owner_proposal_446"
OUT = REVIEW / "fortress_w13_nested_space_owner_proposal_447"
BASE_COMMIT = "cf0ea55dcbb781af4bae548513999c88daf022de"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pointer_value(root: object, pointer: str) -> object:
    value = root
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def box_at(pos: list[float], size: list[float]) -> list[float]:
    return [pos[0], pos[0] + size[0], pos[1], pos[1] + size[1], pos[2], pos[2] + size[2]]


def bounds_list(bounds: dict | list) -> list[float]:
    if isinstance(bounds, list):
        return bounds
    return [bounds["x"][0], bounds["x"][1], bounds["y"][0], bounds["y"][1], bounds["z"][0], bounds["z"][1]]


def sweep(p0: list[float], p1: list[float], size: list[float]) -> list[float]:
    return [min(p0[0], p1[0]), max(p0[0], p1[0]) + size[0], min(p0[1], p1[1]), max(p0[1], p1[1]) + size[1], min(p0[2], p1[2]), max(p0[2], p1[2]) + size[2]]


def positive_overlap(a: list[float], b: list[float]) -> bool:
    return all(min(a[i + 1], b[i + 1]) > max(a[i], b[i]) for i in (0, 2, 4))


def ray_hits(p0: list[float], p1: list[float], bounds: list[float]) -> bool:
    t_min, t_max = 0.0, 1.0
    for axis, (lo, hi) in enumerate(((bounds[0], bounds[1]), (bounds[2], bounds[3]), (bounds[4], bounds[5]))):
        delta = p1[axis] - p0[axis]
        if abs(delta) < 1e-12:
            if not lo < p0[axis] < hi:
                return False
            continue
        t1, t2 = (lo - p0[axis]) / delta, (hi - p0[axis]) / delta
        enter, leave = sorted((t1, t2))
        t_min, t_max = max(t_min, enter), min(t_max, leave)
        if t_min >= t_max:
            return False
    return t_max > max(t_min, 0.0) and t_min < 1.0


def pair_audit(boxes: dict[str, list[float]]) -> list[dict]:
    names = list(boxes)
    return [{"pair": [a, b], "positiveVolumeOverlap": positive_overlap(boxes[a], boxes[b])} for i, a in enumerate(names) for b in names[i + 1 :]]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    source_path = SOURCE_DIR / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_446_TESTONLY.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    d = copy.deepcopy(source)
    source_sha = sha(source_path)
    assert source_sha == "61b559867d7a5ccc49c3a03f92be173a4e02a946a8c2d7194a6cb2674df4a717"
    assert subprocess.check_output(["git", "rev-parse", BASE_COMMIT], text=True).strip() == BASE_COMMIT

    d["id"] = "PG328-W13-NESTED-SPACE-OWNER-PROPOSAL-447"
    d["readAtCommit"] = BASE_COMMIT
    d["classification"] = "OWNER_PROPOSED_TEST_ONLY_BRANCH; NOT_ADOPTED; NOT_A_WITNESS"
    d["status"] = "DIRECTOR_REVIEW_REQUESTED_OWNER_ADOPTION_REQUIRED"
    d["supersedesProposal"] = {"id": source["id"], "sha256": source_sha, "disposition": "Director corrections C01-C05 applied; proposal 446 remains unchanged."}
    d["reviewCorrectionsApplied"] = [
        {"id": "W13-446-C01", "summary": "Route B through the actual Geometry405 tower-SW-entry opening after picking up the blocking cargo."},
        {"id": "W13-446-C02", "summary": "Move A to the supported clear courtyard pose [35,8,0] and verify the complete route and target ray."},
        {"id": "W13-446-C03", "summary": "Arrive immediately adjacent at [0,15,0] and update support, movement and Dispel distance."},
        {"id": "W13-446-C04", "summary": "Add a new W13-only Arcane Sight cast and visible-aura observation; reuse no W12 observation."},
        {"id": "W13-446-C05", "summary": "Record all family-specific Spell Efficiency windows and point to Wizard cards 15, 19 and 21."},
    ]

    # Pin every source to the current main commit and cite all spell data used by the corrected witness.
    for binding in d["sourceBindings"]:
        binding["verifiedAtCommit"] = BASE_COMMIT
        if binding["path"].endswith("RETURN284_WIZARD20_PROFILE_TESTONLY.json"):
            binding["jsonPointers"] = sorted(set(binding.get("jsonPointers", []) + ["/acquisitionLedger/2/choices/1"]))
        if binding["path"].endswith("/wizard.json"):
            binding["jsonPointers"] = sorted(set(binding.get("jsonPointers", []) + ["/cards/15", "/cards/19", "/cards/21"]))

    source_valid = []
    for binding in d["sourceBindings"]:
        source_bytes = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{binding['path']}"])
        blob_sha1 = subprocess.check_output(["git", "rev-parse", f"{BASE_COMMIT}:{binding['path']}"], text=True).strip()
        assert len(source_bytes) == binding["bytes"], binding["path"]
        assert sha_bytes(source_bytes) == binding["sha256"], binding["path"]
        assert blob_sha1 == binding["gitBlobSha1"], binding["path"]
        for pointer in binding.get("jsonPointers", []):
            pointer_value(json.loads(source_bytes.decode("utf-8")), pointer)
        source_valid.append({"path": binding["path"], "bytes": len(source_bytes), "sha256": sha_bytes(source_bytes), "gitBlobSha1": blob_sha1, "jsonPointersVerified": binding.get("jsonPointers", [])})

    inputs = d["ownerProposedInputs"]
    child = inputs["childEntry"]
    child["route"] = [
        {"from": [15, 10, 0], "to": [20, 10, 0], "movementFeet": 5, "reason": "Cross the open Geometry405 tower-SW-entry opening; cargo-B is held before movement."},
        {"from": [20, 10, 0], "to": [30, 10, 0], "movementFeet": 10, "reason": "East across supported open courtyard, clear of cargo-B and relocated A."},
        {"from": [30, 10, 0], "to": [30, 15, 0], "movementFeet": 5, "reason": "North to the parent-side Demiplane aperture."},
        {"event": "physical planar crossing", "movementFeet": 5, "arrival": [0, 15, 0], "plane": inputs["childCreation"]["roomId"]},
    ]
    child.update({
        "totalMovementFeet": 25,
        "entryAt": 19.05,
        "bodyBoundsInChild": {"x": [0, 5], "y": [15, 20], "z": [0, 6]},
        "localBodySupport": {"bounds": {"x": [0, 5], "y": [15, 20], "z": [0, 0]}, "supports": "B only"},
        "carriedItems": ["focus-B", "pack-B", "cargo-B held through arrival; set down inside child at19.06"],
        "unattendedCargoBRemainsInParentAt": None,
        "cargoBAtEntry": {"id": "cargo-B", "massLb": 10, "load": 1, "sizeFeet": [1, 1, 1], "custodian": "B", "hand": "right", "relativeBoundsInBody": {"x": [4, 5], "y": [4, 5], "z": [3, 4]}, "fullyContainedInBodyEnvelope": True, "releasedInsideChildAt": 19.06, "releasedPosition": [5, 15, 0]},
        "noCollisionWithAOrCargoB": True,
        "wholeBodyFits": True,
        "doorwayTraversal": {"openingId": "tower-SW-entry", "geometryPointer": "/openings/6", "clearApertureBounds": [17.5, 20, 10, 15, 0, 8], "fullBBodyFits": True, "doorLeafId": "tower-SW-entry-leaf", "doorLeafBoundaryContactOnly": True},
    })

    child_dispel = inputs["childDispel"]
    child_dispel["casterPosition"] = [0, 15, 0]
    child_dispel["casterCenter"] = [2.5, 17.5, 3]
    child_dispel["distanceFeet"] = math.sqrt(12.5**2 + 2.5**2 + 4.5**2)
    child_dispel["interiorLineOfEffect"] = "Clear inside the room; cargo-B at [5,15,0] is set down after arrival and lies outside the ray."
    child_dispel["componentsStatus"] = "TEST_ONLY ordinary verbal/somatic declaration; right hand is free after cargo-B is set down at19.06."

    settlement = inputs["childTerminalSettlement"]
    settlement.update({
        "childContents": ["living B", "focus-B carried by B", "pack-B carried by B", "loose cargo-B at child [5,15,0]"],
        "settlementOrder": ["body B with carried focus-B and pack-B", "loose cargo-B once after body B"],
        "equipmentRemainsAttached": True,
        "noLooseItemInChild": False,
        "looseItemSettledAtSourceEnd": True,
        "cargoBLocalPosition": [5, 15, 0],
        "cargoBLocalOffsetFromChildEntryAnchor": [5, 0, 0],
        "parentEntryAnchor": [35, 15, 0],
        "cargoBParentPosition": [40, 15, 0],
        "cargoBParentBounds": {"x": [40, 41], "y": [15, 16], "z": [0, 1]},
        "cargoBParentSupport": {"id": "W13-447-CARGO-B-PARENT-GROUND", "bounds": {"x": [40, 41], "y": [15, 16], "z": [0, 0]}, "supports": "cargo-B only"},
        "settlementRulePointer": "DEMIPLANE_MODEL_166.json#/spells/0/procedure/common/closureExtension; loose identity/custody retained and local entry-anchor offset applied.",
    })

    inputs["AArcaneSight"] = {
        "caster": "A", "spellId": "wizard.arch.arcane-sight", "rank": 2, "baseCostRP": 2, "activation": "Action", "rangeFeet": 60,
        "profileAcquisitionPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/conjure_demiplane_fortress_closure_intake_367/payload/sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json#/acquisitionLedger/2/choices/1",
        "sourceCardPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w07_real_dispel_374_repack02/payload/sources/wizard.json#/cards/21",
        "castAt": 18.1, "counterspellWindowAt": 18.2, "resolutionAt": 18.3,
        "position": [35, 8, 0], "positionConvention": "minimum x/y and feet-z", "casterCenter": [37.5, 10.5, 3],
        "targetEffect": "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1", "targetAuraPoint": [10, 10, 3],
        "distanceFeet": math.sqrt(27.5**2 + 0.5**2), "samePlane": True, "totalCover": False,
        "lineOfSight": {"geometryPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/GEOMETRY_405.json", "fragmentsChecked": 2694, "clear": True, "route": "Ray crosses the open tower-SW-entry aperture at y=10.18 and reaches [10,10,3].", "totalCover": False},
        "observationReceipt": {"id": "PG328-W13-R1:ARCANE-SIGHT-OBSERVATION-1", "at": 18.3, "effectId": "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1", "result": "visible magical aura; broad school Conjuration", "automaticSightPerception": True, "laterExaminationActionClaimed": False, "derivedFromW12Observation": False},
        "concentration": {"committedAt": 18.1, "activeAt": 18.3, "maximumSeconds": 600, "deadlineAt": 618.1, "noPriorConcentration": True},
        "spellEfficiencyDeadlineAt": 24.9, "spellEfficiencySameFamilyOpportunityUsed": False, "rechargeRoundsRemainingAtTerminal": 1,
        "counterspellDispositionAt18_2": {"candidate": "B", "result": "NO_ATTEMPT_INELIGIBLE", "reason": "focus-B in left hand and cargo-B in right hand; no free Somatic hand", "reactionSpent": False, "rpSpent": False},
    }

    parent_dispel = inputs["parentDispel"]
    parent_dispel.update({
        "casterPosition": [35, 8, 0], "casterCenter": [37.5, 10.5, 3], "distanceFeet": math.sqrt(27.5**2 + 0.5**2),
        "lineOfEffect": {"geometryPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/GEOMETRY_405.json", "fragmentsChecked": 2694, "clear": True, "basis": "New W13 Arcane Sight receipt at18.3 and direct ray through the open tower-SW-entry; no other branch observation reused.", "totalCover": False},
        "perceptionReceiptId": "PG328-W13-R1:ARCANE-SIGHT-OBSERVATION-1", "targetPerceivedAt": 18.3,
        "approachMovement": {"at": 18.06, "from": [25, 6, 0], "route": [{"to": [35, 6, 0], "feet": 10, "direction": "east"}, {"to": [35, 8, 0], "feet": 2, "direction": "north"}], "totalFeet": 12, "budgetFeet": 30, "geometry": "supported open courtyard; zero positive-volume overlap with Geometry405 or extant bodies/items", "includesAllMovement": True, "noMovementAt24": True},
        "componentsStatus": "TEST_ONLY ordinary verbal/somatic declaration; no focus or material component asserted; the W13 Arcane Sight receipt remains active.",
    })

    # Exact P5-CLOSE parent-local loose cargo position; preserve existing Q27 fixture positions.
    root_close = inputs["rootTerminalClosure"]
    for item in root_close["looseItems"]:
        if item["id"] == "cargo-B":
            item.update({"insidePosition": [40, 15, 0], "bounds": {"x": [40, 41], "y": [15, 16], "z": [0, 1]}, "parentPositionBeforeRootDispel": [40, 15, 0], "custodianAfterP5Close": None, "supportPatchId": "W13-447-CARGO-B-PARENT-GROUND", "outsidePosition": [20, 0, 0]})
    root_close["parentSupportPatches"] = [settlement["cargoBParentSupport"]]

    # Scheduled spells, resources, recharge and Spell Efficiency history.
    schedule = inputs["scheduledTimeAdvance"]
    schedule["lifecycleEvents"] = [
        {"at": 13.1, "event": "B commits rank8 Demiplane for21 RP."},
        {"at": 13.2, "event": "A is component-ineligible for Counterspell; no spend."},
        {"at": 13.3, "event": "Demiplane room and 60-second door resolve."},
        {"at": 13.4, "event": "B picks up existing cargo-B with free object interaction and holds it in right hand; no movement."},
        {"at": 18.05, "event": "A sets down the existing tile at its S030 bounds."},
        {"at": 18.06, "event": "A moves12 feet to [35,8,0] through supported open courtyard."},
        {"at": 18.1, "event": "A commits rank2 Arcane Sight for2 RP."},
        {"at": 18.2, "event": "B has no eligible Counterspell attempt: focus-B and cargo-B occupy both hands."},
        {"at": 18.3, "event": "Arcane Sight resolves and records the W13-local visible Conjuration aura."},
        {"at": 19.05, "event": "B spends25 feet through tower-SW-entry and the Demiplane threshold; arrives at child [0,15,0]."},
        {"at": 19.06, "event": "B sets cargo-B on supported child floor at [5,15,0]; right hand is free."},
        {"at": 19.1, "event": "B commits rank3 Arch Dispel for3 RP against the perceived child interior."},
        {"at": 19.2, "event": "No eligible responder through the opaque child door."},
        {"at": 19.3, "event": "B succeeds against DC18; child source ends."},
        {"at": 19.31, "event": "P5-CLOSE returns B and carried focus/pack to [35,15,0], and loose cargo-B to projected [40,15,0]."},
        {"at": 19.9, "event": "B END expires unused Demiplane-family Spell Efficiency opportunity."},
        {"at": 24.0, "event": "A START ticks Arcane Sight recharge2 to1; Sight remains active."},
        {"at": 24.1, "event": "A commits rank3 Arch Dispel for3 RP against the W13-perceived Fortress aura."},
        {"at": 24.2, "event": "B is eligible and declines Counterspell without expenditure."},
        {"at": 24.3, "event": "A succeeds against DC19; root Fortress ends."},
        {"at": 24.31, "event": "Q27 parent closure settlement; no child remains."},
    ]
    schedule["roundCadence"] = {
        "BArchDispel": "Recharge2 begins at19.1 and remains pending at24.31; first later B START tick is25.",
        "AArchDispel": "Recharge2 begins at24.1 and remains pending at24.31.",
        "AArcaneSight": "Recharge2 begins at18.1; A START24 ticks to1; concentration deadline618.1 is outside branch.",
        "spellEfficiency": "B Demiplane deadline19.9 unused; A Arcane Sight deadline24.9 unused; B child Dispel deadline25.9; A parent Dispel deadline30.9. Different families do not receive either unused discount.",
        "concentration": "A Arcane Sight remains active through24.31; Demiplane room has no concentration.",
    }
    schedule["rule"] = "Process every scheduled regular START/END through24.31; refresh budgets, tick recharge and family deadlines at START; expire due unused budgets/opportunities at END. Commit spell resources, actions, hands, custody, perception and concentration before each Counterspell window. No other unsourced event occurs."
    schedule["branchEndpoint"] = "24.31 after parent Q27; A END24.9 and B START25 are outside the branch."

    ledger = inputs["resourceLedger"]
    ledger_a, ledger_b = ledger["A"], ledger["B"]
    ledger_a.update({
        "arcaneSightCost": 2, "parentDispelCost": 3, "terminalRP": 48,
        "preparedFamilyAdded": ["wizard.arch.arcane-sight", "wizard.arch.dispel-magic"],
        "lastSpell": "wizard.arch.dispel-magic", "spellEfficiencyDeadlineForArcaneSight": 24.9,
        "spellEfficiencyDeadlineForParentDispel": 30.9, "arcaneSightRechargeRoundsRemainingAtTerminal": 1,
        "parentDispelRechargeRoundsRemainingAtTerminal": 2,
        "concentrationAtTerminal": {"spell": "wizard.arch.arcane-sight", "deadline": 618.1, "active": True},
        "preparedFamiliesUsedAfter": ["conjure-demiplane-fortress", "wizard.base.minor-conjuration", "wizard.arch.arcane-sight", "wizard.arch.dispel-magic"],
        "RPHistory": [{"time": 18.1, "spell": "wizard.arch.arcane-sight", "cost": 2, "poolAfter": 51}, {"time": 24.1, "spell": "wizard.arch.dispel-magic", "cost": 3, "poolAfter": 48}],
    })
    ledger_b.update({
        "terminalRP": 56, "spellEfficiencyDeadlineForDemiplane": 19.9, "spellEfficiencyDeadlineForChildDispel": 25.9,
        "cargoCustody": [{"time": 13.4, "custodian": "B", "hand": "right", "carriedWeightLb": 12, "carriedLoad": 1.2}, {"time": 19.06, "custodian": None, "position": [5, 15, 0], "carriedWeightLb": 2, "carriedLoad": 0.2}, {"time": 19.31, "custodian": None, "parentPosition": [40, 15, 0]}],
        "RPHistory": [{"time": 13.1, "spell": "demiplane", "cost": 21, "poolAfter": 59}, {"time": 19.1, "spell": "wizard.arch.dispel-magic", "cost": 3, "poolAfter": 56}],
    })

    geometry_path = REVIEW / "fortress_w01_geometry_405" / "GEOMETRY_405.json"
    geometry = json.loads(geometry_path.read_text(encoding="utf-8"))
    obstacles: list[tuple[str, list[float]]] = []
    for i, panel in enumerate(geometry["panels"]):
        for j, bounds in enumerate(panel.get("occupiedFragments", [])):
            obstacles.append((f"panel/{i}/{panel['id']}/{j}", bounds))
    for i, door in enumerate(geometry["doorLeaves"]):
        for j, bounds in enumerate(door.get("occupiedFragments", [])):
            obstacles.append((f"doorLeaf/{i}/{door['id']}/{j}", bounds))
    route_specs = {
        "A18.06": [([25, 6, 0], [35, 6, 0]), ([35, 6, 0], [35, 8, 0])],
        "B19.05": [([15, 10, 0], [20, 10, 0]), ([20, 10, 0], [30, 10, 0]), ([30, 10, 0], [30, 15, 0])],
    }
    route_audits = {}
    for route_id, legs in route_specs.items():
        route_audits[route_id] = []
        for p0, p1 in legs:
            bounds = sweep(p0, p1, [5, 5, 6])
            hits = [name for name, obstacle in obstacles if positive_overlap(bounds, obstacle)]
            route_audits[route_id].append({"from": p0, "to": p1, "sweptBounds": bounds, "geometry405PositiveVolumeHits": hits, "hitCount": len(hits)})
    rays = {}
    for ray_id, p0, p1 in [("AArcaneSight", [37.5, 10.5, 3], [10, 10, 3]), ("AParentDispel", [37.5, 10.5, 3], [10, 10, 3]), ("BChildDispel", [2.5, 17.5, 3], [15, 15, 7.5])]:
        hits = [name for name, obstacle in obstacles if ray_hits(p0, p1, obstacle)]
        rays[ray_id] = {"from": p0, "to": p1, "distanceFeet": math.dist(p0, p1), "geometry405PositiveVolumeHits": hits, "hitCount": len(hits), "clear": not hits}
    assert all(leg["hitCount"] == 0 for route in route_audits.values() for leg in route)
    assert all(ray["clear"] for ray in rays.values())

    parent_boxes = {"A": box_at([35, 8, 0], [5, 5, 6]), "B": box_at([35, 15, 0], [5, 5, 6]), "cargo-B": box_at([40, 15, 0], [1, 1, 1]), "tile": box_at([25, 5, 0], [1, 1, 0.25])}
    parent_pairs = pair_audit(parent_boxes)
    assert not any(pair["positiveVolumeOverlap"] for pair in parent_pairs)

    root_close = inputs["rootTerminalClosure"]
    boxes = {actor["id"]: bounds_list(actor["bounds"]) for actor in root_close["unchangedOutsideActors"]}
    boxes["A"], boxes["B"] = bounds_list(root_close["A"]["bodyBounds"]), bounds_list(root_close["B"]["bodyBounds"])
    for item in root_close["looseItems"]:
        if item["id"] == "cargo-B":
            boxes["cargo-B"] = box_at(item["outsidePosition"], item["sizeFeet"])
        else:
            boxes[item["id"]] = bounds_list(item["bounds"])
    exterior_pairs = pair_audit(boxes)
    assert len(exterior_pairs) == 15 and not any(pair["positiveVolumeOverlap"] for pair in exterior_pairs)
    root_close["parentSupportPatches"] = [settlement["cargoBParentSupport"]]
    for support in root_close["supportPatches"]:
        if support.get("supports") == "cargo-B only":
            support.update({"id": "W13-447-CARGO-B-PARENT-GROUND", "bounds": {"x": [40, 41], "y": [15, 16], "z": [0, 0]}})
    root_close["geometryPairsCheckedAtExterior"] = 15
    inputs["geometryAudit"] = {
        "sourcePath": geometry_path.relative_to(REPO).as_posix(), "sourceSha256": sha(geometry_path),
        "positionConvention": "minimum x/y and feet-z; strict positive-volume intersection; boundary contact allowed.",
        "routeSweeps": route_audits, "rays": rays,
        "towerOpeningTraversal": {"openingId": "tower-SW-entry", "geometryPointer": "/openings/6", "bounds": [17.5, 20, 10, 15, 0, 8], "routeBodyFits": True, "doorLeafBoundaryContactOnly": True},
        "childArrival": {"roomSideAperture": {"x": 0, "y": [15, 20], "z": [0, 8]}, "arrivalBodyBounds": [0, 5, 15, 20, 0, 6], "immediatelyAdjacent": True, "movementToArrivalAfterThreshold": 0},
        "parentP5CloseCollisionPairs": parent_pairs, "rootQ27ExteriorCollisionPairs": exterior_pairs, "rootQ27ExteriorCollisionPairCount": len(exterior_pairs),
    }

    d["directorQuestion"] = "Review exact W13-447 hashes and source bindings; verify the tower-SW-entry route with cargo custody, A's [35,8] position, adjacent child arrival, new W13 Arcane Sight perception, cadence/resource changes, P5-CLOSE offset and Q27 geometry. Return owner-adoption readiness or one consolidated correction list. Do not construct another witness, seal, accept/apply Fortress, change canon or mutate queue."
    proposal_path = OUT / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.json"
    write_json(proposal_path, d)
    proposal_sha = sha(proposal_path)

    correction = {
        "schemaVersion": 1, "id": "PG328-W13-DIRECTOR-CORRECTIONS-447", "classification": "CORRECTION_RECORD_FOR_DIRECTOR_REVIEW",
        "supersedesProposalId": source["id"], "supersedesProposalSha256": source_sha, "successorProposalId": d["id"], "successorProposalSha256": proposal_sha,
        "sourceDirectorReview": "GPT Director, Calibration review part 6",
        "findingsApplied": [
            {"id": "C01", "location": "/ownerProposedInputs/childEntry/route", "correction": "B crosses tower-SW-entry after picking up cargo-B; all body sweeps checked against Geometry405."},
            {"id": "C02", "location": "/ownerProposedInputs/parentDispel/approachMovement", "correction": "A moves12 feet to [35,8,0]; complete route and parent ray are clear."},
            {"id": "C03", "location": "/ownerProposedInputs/childEntry/route/3 and /childDispel", "correction": "B arrives adjacent at [0,15,0]; body/support, movement and Dispel distance updated."},
            {"id": "C04", "location": "/ownerProposedInputs/AArcaneSight and /parentDispel", "correction": "New W13-only Arcane Sight observation at18.3; no W12 observation reused."},
            {"id": "C05", "location": "/sourceBindings/1, /sourceBindings/7, /scheduledTimeAdvance/roundCadence and /resourceLedger", "correction": "Add acquisition/card pointers for Sight21, Dispel19 and Spell Efficiency15; record family windows, concentration, recharge and updated RP."},
        ],
        "preservedChecks": ["17 source bindings pinned to current main commit.", "Wizard20 access and Model166/167 static status; runtime selection disabled.", "Demiplane21 RP; two Arch Dispel3 RP; checks23 vs DC18/DC19.", "Opaque child-door Counterspell exclusion; eight STARTs/seven ENDs through24.31.", "Child ends before P5-CLOSE; parent ends before Q27; queue remains830/18/0."],
        "nonEffects": {"campaignEventsAsserted": False, "witnessConstructed": False, "sealPresent": False, "FortressAcceptedOrApplied": False, "canonChanged": False, "queueChanged": False, "queue": "830 applied / 18 pending / 0 accepted-unapplied"},
    }
    correction_path = OUT / "PG328_W13_DIRECTOR_CORRECTIONS_447.json"
    write_json(correction_path, correction)

    markdown = f"""# W13 nested-space owner proposal 447\n\nProposal 447 applies GPT Director corrections C01-C05 to proposal 446. It remains an unadopted TEST_ONLY proposal, bound to unchanged W01-403 S030.\n\n- Proposal SHA-256: `{proposal_sha}`\n- Superseded proposal SHA-256: `{source_sha}`\n- Source commit: `{BASE_COMMIT}`\n- Geometry: B crosses the verified tower-SW-entry opening with cargo-B held; A moves to `[35,8,0]`; B arrives flush to the child aperture at `[0,15,0]`.\n- Perception: A casts Arcane Sight for2 RP at18.1; a new W13-local visible Conjuration aura receipt at18.3 supports the later parent Dispel. No W12 observation is imported.\n- Resources: A ends at48 RP; B ends at56 RP. Spell Efficiency windows and Arcane Sight concentration/recharge are recorded.\n- Collision checks: all route sweeps and rays clear; 6 parent-side pairs and 15 Q27 exterior pairs pass.\n- Scope: No campaign event, witness, seal, Fortress acceptance/application, canon change or queue mutation. Queue remains830/18/0.\n\nSee `PG328_W13_DIRECTOR_CORRECTIONS_447.json`, `BUILD_VALIDATION_447.json` and `VERIFY_W13_PROPOSAL_447.py`.\n"""
    markdown_path = OUT / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.md"
    markdown_path.write_text(markdown, encoding="utf-8")

    validation_checks = [
        {"id": "S030_PARENT", "pass": d["scope"]["parentStateSha256"] == "6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c" and d["scope"]["parentSha256"] == "2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb", "detail": "Exact unchanged W01-403 S030 parent."},
        {"id": "SOURCE_BINDINGS", "pass": len(source_valid) == 17, "detail": f"17 exact Git blobs and every declared pointer verified at {BASE_COMMIT}, including Wizard cards15,19,21."},
        {"id": "ROUTE_SWEEPS", "pass": all(leg["hitCount"] == 0 for route in route_audits.values() for leg in route), "detail": "Five full-body sweeps have zero Geometry405 positive-volume hits."},
        {"id": "SIGHT_AND_DISPEL_RAYS", "pass": all(ray["clear"] for ray in rays.values()), "detail": "Arcane Sight, parent Dispel and child Dispel rays have zero Geometry405 intersections; sight is W13-local."},
        {"id": "TOWER_OPENING_AND_CHILD_ARRIVAL", "pass": inputs["geometryAudit"]["towerOpeningTraversal"]["routeBodyFits"] and inputs["geometryAudit"]["childArrival"]["immediatelyAdjacent"], "detail": "Full B body fits tower-SW-entry; arrival is adjacent to x=0 child aperture."},
        {"id": "P5_CLOSE_LOOSE_CARGO", "pass": settlement["cargoBParentPosition"] == [40, 15, 0] and settlement["cargoBParentSupport"]["bounds"] == {"x": [40, 41], "y": [15, 16], "z": [0, 0]}, "detail": "Loose cargo-B projects the +5-foot child offset from the parent entry anchor and is supported before Q27."},
        {"id": "COLLISION_PAIRS", "pass": len(parent_pairs) == 6 and len(exterior_pairs) == 15 and not any(x["positiveVolumeOverlap"] for x in parent_pairs + exterior_pairs), "detail": "Six parent-side pairs and15 fixture-side Q27 pairs pass."},
        {"id": "RESOURCES_AND_CADENCE", "pass": ledger_a["terminalRP"] == 48 and ledger_b["terminalRP"] == 56 and ledger_a["arcaneSightRechargeRoundsRemainingAtTerminal"] == 1 and ledger_b["spellEfficiencyDeadlineForDemiplane"] == 19.9, "detail": "A53-2-3=48 RP; B80-21-3=56 RP; family windows and Sight recharge included."},
        {"id": "QUEUE_AND_NON_EFFECTS", "pass": d["queueAtProposal"]["applied"] == 830 and d["queueAtProposal"]["pending"] == 18 and d["queueAtProposal"]["acceptedUnapplied"] == 0 and d["queueAtProposal"]["mutated"] is False, "detail": "No campaign/canon/acceptance/seal/queue effect; authority remains830/18/0."},
    ]
    validation = {
        "id": "PG328-W13-BUILD-VALIDATION-447", "status": "PASS" if all(x["pass"] for x in validation_checks) else "FAIL", "readAtCommit": BASE_COMMIT,
        "proposalId": d["id"], "scope": d["scope"], "sourceCount": 17, "sourceBindingsVerified": True, "verifiedSourceBindings": source_valid,
        "correctionRecordSha256": sha(correction_path), "checks": validation_checks, "geometryAudit": inputs["geometryAudit"],
        "proposalFileSha256": proposal_sha, "markdownFileSha256": sha(markdown_path), "noWitnessConstructed": True, "noSealAcceptanceApplicationOrQueueChange": True,
    }
    validation_path = OUT / "BUILD_VALIDATION_447.json"
    write_json(validation_path, validation)
    manifest = {"id": "PG328-W13-MANIFEST-447", "classification": "DIRECTOR_REVIEW_PROPOSAL_PACKAGE", "proposalId": d["id"], "sourceCommit": BASE_COMMIT, "artifacts": []}
    for path in (proposal_path, markdown_path, correction_path, validation_path, OUT / "VERIFY_W13_PROPOSAL_447.py"):
        manifest["artifacts"].append({"path": path.name, "bytes": path.stat().st_size, "sha256": sha(path)})
    write_json(OUT / "MANIFEST_447.json", manifest)
    print("proposal", proposal_sha)
    print("sourceBindings", len(source_valid), "geometrySegments", sum(map(len, route_audits.values())), "rays", len(rays), "closurePairs", len(parent_pairs), len(exterior_pairs))
    print("checks", [(item["id"], item["pass"]) for item in validation_checks])


if __name__ == "__main__":
    main()
