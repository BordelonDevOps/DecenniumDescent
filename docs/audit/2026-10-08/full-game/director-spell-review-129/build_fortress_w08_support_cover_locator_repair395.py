from __future__ import annotations

import copy
import hashlib
import json
import math
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "fortress_w08_occupied_antimagic_repair_394"
SOURCE_ZIP = SOURCE_DIR / "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_GeometryCarrierRepair394_TESTONLY.zip"
OUT = ROOT / "fortress_w08_support_cover_locator_repair_395"
ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_SupportCoverLocator395_TESTONLY.zip"
PREBUILD = "PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json"
MANIFEST = "PG328-W08_PREBUILD_SOURCE_BINDINGS_395.json"
GEOMETRY = "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_395_TESTONLY.json"
CARRIER = "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_395_TESTONLY.json"
SUPPORT = "OWNER_PG328_W08_SUPPORT_COVER_CONTRACT_395_TESTONLY.json"
REQUEST = "PG328-W08_DIRECTOR_REVIEW_REQUEST_395.json"
DELIVERY = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_SupportCoverLocator395_TESTONLY_DELIVERY.json"
DIRECTOR394 = "DIRECTOR_PG328_W08_GEOMETRY_CARRIER_REVIEW_394.json"
CASE_MEMBER = "payload/cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json"
CASE_SHA = "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900"
SPACE = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic/cast1/space"
NOW = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jbytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def ptr(text: str) -> str:
    return text.replace("~", "~0").replace("/", "~1")


def translate(bounds, anchor):
    return {axis: [bounds[axis][0] + anchor[i], bounds[axis][1] + anchor[i]]
            for i, axis in enumerate(("x", "y", "z"))}


def overlaps(a, b):
    return all(min(a[k][1], b[k][1]) > max(a[k][0], b[k][0]) for k in ("x", "y", "z"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SOURCE_ZIP) as old_zip:
        old_files = {i.filename: old_zip.read(i.filename) for i in old_zip.infolist()}

    old_delivery = json.loads((SOURCE_DIR / "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_GeometryCarrierRepair394_TESTONLY_DELIVERY.json").read_text(encoding="utf-8"))
    assert sha(SOURCE_ZIP.read_bytes()) == old_delivery["sha256"]
    packet = json.loads(old_files["payload/" + PREBUILD])
    geometry = json.loads(old_files["payload/proposals/PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_394_TESTONLY.json"])
    carrier = json.loads(old_files["payload/proposals/PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_394_TESTONLY.json"])
    manifest = json.loads(old_files["authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_394.json"])
    term_name = "OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json"
    term_bytes = old_files["payload/proposals/" + term_name]
    term = json.loads(term_bytes)
    case_bytes = old_files[CASE_MEMBER]
    assert sha(case_bytes) == CASE_SHA

    # Record the completed Director review so the corrective packet is traceable.
    director394 = {
        "id": "DIRECTOR-PG328-W08-GEOMETRY-CARRIER-REVIEW-394",
        "recordedAtUtc": NOW,
        "source": "Completed GPT Director response in the live Chrome conversation Review SH202 B02 Archive.",
        "conversation": old_delivery["directorConversation"],
        "reviewedPacket": {"path": old_delivery["artifact"], "sha256": old_delivery["sha256"],
                           "bytes": old_delivery["bytes"], "memberCount": old_delivery["bundleMemberCount"]},
        "decision": "REPAIR_REQUIRED_BEFORE_W08_INTEGRATION",
        "findings": {
            "acceptedInputs": [
                "Center [16,12,8], panel containment, architectural ray clearance through the open doorway, tower/stair/floor checks, carrier bounds, hands/focus, and collision checks reconcile.",
                "Field termination proposal 386 remains coherent for separate owner adoption; its 66.1-second deadline remains appropriate only if establishment remains at world 6.1."
            ],
            "remainingRepairs": [
                "The inherited z=0 support patch and Q23 do not by themselves establish an actual zero-thickness load-bearing floor panel; a narrow scoped TEST_ONLY support premise requires owner adoption.",
                "Every [16,12,8]-to-panel ray crosses A's declared body box. The packet must bind a creature-cover classification or use another reviewed geometric premise; intended occupancy alone is not a cover exemption.",
                "Four carrier case locators use an abbreviated archive path and must be replaced with the exact bundle member payload/cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json and exact JSON Pointers."
            ],
            "directorSuggestedGeometry": {
                "panelPrismZFeet": [0, 1 / 12],
                "actorAndCarriedItemsRaisedFeet": 1 / 12,
                "candidateCenterFeet": [18.5, 14, 1 / 24],
                "exposedPanelSidePointFeet": [17.5, 12.25, 1 / 24],
                "requiredFollowup": "Recheck perception, the reached structural expression, and Q27 vertical return/support consequences; do not silently snap the return to ground."
            },
            "preserved": {"fixtureMutated": False, "actualCast": False, "FortressAcceptedOrApplied": False,
                          "identityHold": "PG200-B06 remains held", "queue": "828/20/0"}
        },
        "nextStep": "Submit corrected support/cover and source-locator proposal with a Director-reviewed vertical return/support projection before any integrated W08 witness."
    }
    director394_raw = jbytes(director394)

    # One-inch panel slab is a proposed TEST_ONLY support model, not an adopted fact.
    center = [18.5, 14, 1 / 24]
    feet = [15, 10, 1 / 12]
    side_point = [17.5, 12.25, 1 / 24]
    panel = {"x": [12.5, 17.5], "y": [7.5, 12.5], "z": [0, 1 / 12]}
    corners = [[x, y, z] for x in panel["x"] for y in panel["y"] for z in panel["z"]]
    distances = [math.dist(center, p) for p in corners]
    center_range = math.dist(center, feet)
    assert max(distances) < 20 and center_range < 20
    assert center[2] < feet[2] and center[2] < panel["z"][1]
    assert side_point[0] == panel["x"][1] and panel["z"][0] <= side_point[2] <= panel["z"][1]
    assert side_point[2] < feet[2]
    assert center[0] >= side_point[0] and center[1] >= side_point[1]
    assert center[2] == side_point[2]
    assert 10 <= center[0] <= 20 and 10 <= center[1] <= 20
    assert 5 <= side_point[0] <= 20 and 10 <= side_point[1] <= 20
    # The horizontal center-to-face segment remains outside the slab until its endpoint,
    # below A's raised body, inside the open room, and south of the reserved stair path.
    assert side_point[0] == panel["x"][1]
    assert center[0] > panel["x"][1]
    assert side_point[1] > 10 and center[1] < 20
    assert center[1] < 15 and side_point[1] < 15
    assert center[2] < panel["z"][1]

    geometry["id"] = "PG328-W01-W08-OCCUPIED-PANEL-GEOMETRY-PROPOSAL-395"
    geometry["createdAtUtc"] = NOW
    geometry["status"] = "PROPOSED_TEST_ONLY_SUPPORT_COVER_INPUT_PENDING_OWNER_ADOPTION_AND_DIRECTOR_REVIEW"
    geometry["supersedes"] = "PG328-W01-W08-OCCUPIED-PANEL-GEOMETRY-PROPOSAL-394"
    geometry["scope"]["ownerAdoptionRequired"] = True
    case_path = CASE_MEMBER + "#/final/actors/A"
    support_path = CASE_MEMBER + "#/final/spaces/" + ptr(SPACE) + "/support"
    geometry["sourceBindings"] = [
        {"path": "payload/rules/PG328_QUESTION_DISPOSITIONS.json#/questions/2/answer",
         "sha256": "149d4098591799f51afa37837ccca722eb9ae08c3ea437c640d943f33b1bb637",
         "use": "Q23 bounds the existing Fortress envelope and structural panels but leaves the panel/support model unresolved."},
        {"path": case_path, "sha256": CASE_SHA,
         "use": "Exact inherited actor A member and body, position, and carried-load fields."},
        {"path": support_path, "sha256": CASE_SHA,
         "use": "Exact inherited aggregate support datum z=0; this proposal places the slab lower face on that datum."},
        {"path": "payload/sources/ANTIMAGIC_FIELD_MODEL_149.json#/spells/2/procedure",
         "sha256": "ceeff51cb3b9e8000bf845e299d4d9e66b46792133ae5931ad823ce98ea51e57",
         "use": "Fixed-center 20-ft field clipped by actual-solid total cover; proposal checks an exposed slab-side contact without assuming penetration."}
    ]
    geometry["occupiedPanel"].update({
        "surfaceBoundsFeet": panel,
        "volumeBoundsFeet": panel,
        "thicknessFeet": 1 / 12,
        "thickness": "A one-inch vertical prism is a new, scoped TEST_ONLY support premise proposed for owner adoption; it is not inferred from Q23 or treated as canonical floor physics.",
        "supportGraph": {
            "existingGeneratedSpace": SPACE,
            "existingAggregateSupportPointer": "/final/spaces/" + ptr(SPACE) + "/support",
            "testOnlyInstantiation": "The slab lower face rests exactly on the inherited z=0 aggregate support datum; the named one-inch magical panel is a part of the existing Fortress source, not an independent footing or new support plane.",
            "loadBearingPremise": {"supportedMassLb": 162, "components": {"A_body": 150, "A_carriedEquipment": 12},
                                   "contact": "A's complete 5x5 footprint rests on the slab top surface at z=1/12."},
            "edges": [
                {"from": SPACE, "to": "W08-SW-TOWER", "relation": "existing Fortress source contains proposed corner tower"},
                {"from": "W08-SW-TOWER", "to": "W08-FLOOR-PANEL-A-01", "relation": "tower contains the named ground-floor structural panel"},
                {"from": "inherited aggregate support patch z=0", "to": "W08-FLOOR-PANEL-A-01 lower face z=0", "relation": "the panel prism bears directly on the existing support datum"},
                {"from": "W08-FLOOR-PANEL-A-01 top face z=1/12", "to": "A and carried equipment", "relation": "supports A's complete 5x5 footprint and 162 lb combined load"}
            ],
            "noIndependentFooting": True, "noNewSpace": True, "ownerAdoptionRequired": True
        },
        "occupancy": {"AFeetPosition": feet, "bodyBoundsFeet": {"x": [12.5, 17.5], "y": [7.5, 12.5], "z": [1 / 12, 73 / 12]},
                       "groundContactZ": 1 / 12, "doorwayFit": "The 5x5 footprint remains inside the 5x8 south opening; body height 1/12..73/12 fits below opening top z=8.",
                       "carriedMassLb": 12, "combinedSupportedMassLb": 162}
    })
    geometry["proposedLocalFortressInstantiation"]["southwestTower"]["floorSurfacesFeet"] = [0, 10, 20, 30, 40]
    geometry["proposedLocalFortressInstantiation"]["southwestTower"]["namedGroundPanel"] = "W08-FLOOR-PANEL-A-01, z=0..1/12"
    geometry["fieldIntersectionAndCover"] = {
        "centerFeet": center,
        "centerCandidateRevision": "Director-suggested side approach outside A's raised body and the panel prism footprint.",
        "centerRangeFromAFeet": round(center_range, 9), "radiusFeet": 20,
        "panelPrismBoundsFeet": panel,
        "panelCornerPointsFeet": corners,
        "panelCornerDistancesFeet": [round(d, 9) for d in distances],
        "farthestPanelPointFeet": corners[distances.index(max(distances))],
        "farthestPanelDistanceFeet": round(max(distances), 9),
        "sphereContainsWholePanelPrismGeometrically": max(distances) < 20,
        "candidateExposedSuppressionLocusPointFeet": side_point,
        "centerToPanelSideRay": {"fromFeet": center, "toFeet": side_point, "zConstant": True,
                                 "xRange": [side_point[0], center[0]], "yRange": [side_point[1], center[1]],
                                 "clearOfRaisedABody": side_point[2] < 1 / 12,
                                 "remainsOutsidePanelUntilEndpoint": True,
                                 "endpointOnEastFace": True,
                                 "obstructionCheck": "The segment lies in the open interior, below A's raised body, outside the panel prism until the exposed east-face endpoint, clear of the tower walls and reserved stair path."},
        "architecturalSolids": ["southwest tower walls with declared open 5x8 doorway", "reserved stair path", "upper floor surfaces", "Q23 perimeter walls"],
        "actualTotalCoverRuleBound": True,
        "creatureCoverClassificationAssumed": False,
        "panelPenetrationAssumed": False,
        "fieldContactConclusion": "A direct ray to the exposed east face is geometrically clear. This proposes surface contact only; it does not assert penetration through the panel or establish that surface contact satisfies Q27's occupied-structural-region predicate.",
        "Q27TriggerQuestion": "Does contact at this exposed face establish suppression of W08-FLOOR-PANEL-A-01 for Q27, or is a narrower structural expression or source rule required?"
    }
    geometry["verticalReturnProjection395"] = {
        "status": "EXPLICIT_TEST_ONLY_CANDIDATE_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION",
        "inGeneratedSpaceAFeet": feet,
        "proposedSourcePlaneAFeetAtQ27Settlement": [15, 0, 0],
        "sourcePlane": "fixture:origin",
        "sourceSupportZ": 0,
        "explicitVerticalAdjustmentFeet": -1 / 12,
        "meaning": "This proposal explicitly projects the existing candidate exit anchor onto the source-plane z=0 support surface; it does not silently preserve or discard the raised one-inch offset.",
        "sourceRuleEstablished": False,
        "directorMustConfirmQ27AllowsThisExactSettlementOrSpecifyRepair": True
    }
    geometry["Q27TriggerQuestion"] = "If this unadopted support/contact premise is accepted, does the exposed face contact satisfy Q27's occupied-structural-region trigger, while W01 compatible damage remains open?"
    geometry["adoptionBoundary"] = "Unadopted TEST_ONLY geometry and support/contact proposal only; no campaign fact, cast, Q27 settlement, W01 compatible-damage completion, PG200-B06 clearance, or W08 acceptance."

    # Carrier offsets are raised by one inch in the generated space and explicitly projected to source support on terminal return.
    carrier["id"] = "PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-395"
    carrier["createdAtUtc"] = NOW
    carrier["status"] = "PROPOSED_TEST_ONLY_PLACEMENT_AND_RETURN_INPUT_PENDING_OWNER_ADOPTION_AND_DIRECTOR_REVIEW"
    carrier["supersedes"] = "PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-394"
    carrier["sourceBindings"] = [
        {"path": CASE_MEMBER + "#/final/actors/A", "sha256": CASE_SHA,
         "use": "Exact actor A position, orientation, body bounds, hands, equipment and load fields."},
        {"path": CASE_MEMBER + "#/final/items/focus-A", "sha256": CASE_SHA, "use": "Exact 0.5-ft cube, A custody; held in left hand."},
        {"path": CASE_MEMBER + "#/final/items/pack-A", "sha256": CASE_SHA, "use": "Exact 0.5-ft cube, A custody; independently clipped to harness."},
        {"path": CASE_MEMBER + "#/final/items/cargo-A", "sha256": CASE_SHA, "use": "Exact 1-ft cube, A custody; independently clipped to belt point."},
        {"path": "payload/sources/BODY_EQUIPMENT_PLAYTEST.md#Placement and involuntary endings; #Carrying and Load",
         "sha256": "5fa622f43b6948e7e991f1ca5a237de584900e92cfd4f37eed47586d73222039",
         "use": "Exact bundled rule headings for item identity, custody, placement and load."},
        {"path": "payload/proposals/" + GEOMETRY, "sha256": "PENDING_GEOMETRY_HASH",
         "use": "Proposed one-inch support panel, lifted carrier arrangement and test-only vertical return projection."}
    ]
    anchor = feet
    exterior = [15, 0, 0]
    rel = {item["id"]: item["relativeBoundsFeet"] for item in carrier["arrangement"]}
    before = {key: translate(bounds, anchor) for key, bounds in rel.items()}
    after = {key: translate(bounds, exterior) for key, bounds in rel.items()}
    body_before = {"x": [12.5, 17.5], "y": [7.5, 12.5], "z": [1 / 12, 73 / 12]}
    body_after = {"x": [12.5, 17.5], "y": [-2.5, 2.5], "z": [0, 6]}
    for item in carrier["arrangement"]:
        item["preCastWorldBoundsFeet"] = before[item["id"]]
        item["postReturnWorldBoundsFeet"] = after[item["id"]]
    assert all(not overlaps(v, body_before) for v in before.values())
    assert all(not overlaps(after[k], body_after) for k in after)
    assert all(v["z"][0] >= panel["z"][1] for v in before.values())
    assert all(10 <= v["x"][0] < v["x"][1] <= 20 and 10 <= v["y"][0] < v["y"][1] <= 20
               for v in before.values())
    for k, outside_body in carrier["postReturnCheck"]["outsideBodies"].items():
        assert all(not overlaps(v, outside_body) for v in after.values()), f"post-return overlap with {k}"
    carrier["bodyConvention"].update({"feetAnchor": anchor, "bodyBoundsFeet": body_before})
    carrier["postReturnCheck"].update({"exteriorFeetAnchor": exterior, "bodyBoundsFeet": body_after,
                                       "verticalReturnProjection": "Explicit candidate: feet z 1/12 in Fortress to feet z=0 on fixture:origin support at Q27 settlement; vertical adjustment -1/12 ft is unadopted and requires Director confirmation.",
                                       "sourcePlaneSupportZ": 0,
                                       "allItemsAvoidPositiveVolumeOverlapWithBody": all(not overlaps(v, body_after) for v in after.values()),
                                       "allItemsAvoidPositiveVolumeOverlapWithB_C_D": True})
    carrier["insideFortressCheck"]["AWholeFootprintFitsDoorway"] = True
    carrier["insideFortressCheck"]["AFeetRestOnProposedPanelTop"] = True
    carrier["insideFortressCheck"]["raisedByFeet"] = 1 / 12
    carrier["insideFortressCheck"]["itemsAvoidWallsAndStairs"] = True
    carrier["returnVerticalProjection395"] = copy.deepcopy(geometry["verticalReturnProjection395"])
    carrier["reviewLimit"] = "Placement, raised offsets, and terminal source-support coordinates are unadopted candidates only. Do not mutate the case or certify the Q27 return until Director review and owner adoption."

    support = {
        "id": "OWNER-PG328-W08-SUPPORT-COVER-CONTRACT-PROPOSAL-395",
        "createdAtUtc": NOW,
        "status": "PROPOSED_NEW_SCOPED_TEST_ONLY_CONTRACT_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION",
        "scope": {"witnessId": "PG328-W08", "subWitnessId": "PG328-W01", "caseId": "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic",
                  "identityHold": "PG200-B06", "fixtureMutated": False, "canonicalRuleChange": False,
                  "castOrSettlementExecuted": False, "ownerAdoptionRequired": True},
        "directorFinding394": {"path": DIRECTOR394, "sha256": "PENDING_DIRECTOR394_HASH",
                               "decision": "REPAIR_REQUIRED_BEFORE_W08_INTEGRATION"},
        "proposedPanelContract": {"panelId": "W08-FLOOR-PANEL-A-01", "partOf": "Existing PG200 Fortress source / W08-SW-TOWER",
                                  "volumeFeet": panel, "thicknessFeet": 1 / 12, "loadBearing": True,
                                  "supportsMassLb": 162, "supportDatumZ": 0, "topSurfaceZ": 1 / 12,
                                  "noIndependentFooting": True, "noNewSpace": True,
                                  "suppressionLocusCandidate": {"surface": "East vertical face of W08-FLOOR-PANEL-A-01",
                                                                 "pointFeet": side_point,
                                                                 "contactOnly": True, "panelPenetrationAssumed": False}},
        "proposedOccupancy": {"AFeetInGeneratedSpace": feet, "bodyBoundsFeet": body_before,
                              "carriedBoxesRaisedFeet": 1 / 12,
                              "bodyMassLb": 150, "carriedEquipmentMassLb": 12,
                              "completeFootprintSupported": True},
        "coverTreatment": {"ruleSource": "ANTIMAGIC_FIELD_MODEL_149.json#/spells/2/procedure",
                           "operativeRule": "Clip against actual solid total cover from the fixed center.",
                           "candidateCenterFeet": center, "candidateExposedPanelPointFeet": side_point,
                           "rayClearOfA": True, "rayClearOfWallsAndStairs": True,
                           "creatureCoverClassificationAssumed": False,
                           "Q27StructuralSuppressionStillRequiresDirectorFinding": True},
        "verticalTerminalProjection": geometry["verticalReturnProjection395"],
        "unadoptedLimits": ["No general floor physics", "No canonical rule or Q23 interpretation change",
                            "No actual cast, panel creation, field suppression, Q27 settlement, or return movement",
                            "No W01 compatible-damage completion", "No Fortress acceptance/application",
                            "No PG200-B06 clearance or queue/hold/seal change"],
        "requestedDirectorDecision": ["Review the exact one-inch support premise and 162-lb load.",
                                       "Determine whether exposed-face field contact establishes Q27 suppression or identify the narrowest repair.",
                                       "Determine whether the explicit -1/12-ft return projection to the existing z=0 source support is permitted; do not infer a silent snap.",
                                       "Confirm exact carrier source locators and placement checks.",
                                       "Identify all remaining prerequisites before an integrated W08 witness."]
    }

    request = {
        "id": "PG328-W08-DIRECTOR-REVIEW-REQUEST-395", "createdAtUtc": NOW,
        "scope": "Support/cover/locator correction for the Return284 occupied-antimagic W08 branch only.",
        "supersedesReviewRequest394Sha256": old_delivery["reviewRequestSha256"],
        "priorDirectorReview394": {"path": DIRECTOR394, "sha256": "PENDING_DIRECTOR394_HASH"},
        "reviewQuestions": [
            "Does the unadopted one-inch panel prism z=[0,1/12] with its lower face on the existing support datum, load-bearing for A's 150-lb body plus 12-lb carried load, provide a sufficiently exact scoped support premise?",
            "Does center [18.5,14,1/24] have a clear center-to-exposed-east-face path to [17.5,12.25,1/24], below the raised A body and outside the panel until contact; does this surface contact suffice for the Q27 structural-region trigger?",
            "Is the explicit proposed Q27 return from A feet z=1/12 in the generated space to z=0 on fixture:origin support, including the -1/12-ft vertical adjustment, permissible; if not, what exact source rule or test-only premise is needed?",
            "Do the raised item boxes, hand/focus arrangement, full JSON pointers, and post-return collision projections reconcile?",
            "Confirm field-termination proposal 386 remains coherent for separate owner adoption, preserving its 66.1-second deadline only if establishment remains at world 6.1.",
            "What precise additional evidence, owner adoption, or repair remains before an integrated reversible W08 witness can be built?"
        ],
        "doNot": ["cast Antimagic Field", "mutate any inherited case or fixture bytes", "adopt proposal 395 or termination proposal 386",
                   "execute Q27 or terminate the Fortress/field", "accept/apply Fortress", "clear PG200-B06",
                   "change any other hold/seal or the spell queue"],
        "queue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0}
    }

    # Update the prebuild's candidate-only view; keep the inherited case member byte-exact.
    cast = packet["proposedCastState"]["proposedCastAfterRefresh"]
    cast["centerCandidate"].update({"feet": center, "distanceFromAFeet": round(center_range, 9),
                                     "within20Feet": True, "perceivedPointAndLineOfEffectMustBeRechecked": True,
                                     "geometryProposal": "395 only; neither adopted nor executed"})
    cast["candidateHistoryEntry"]["targetCenterFeet"] = center
    cast["postCommitHistoryAppend"]["spellHistory"]["targetCenterFeet"] = center
    packet["candidateGeometry"] = {"candidateOnly": True, "samePlaneAsCasterAndFortressStructure": SPACE,
                                   "centerFeet": center, "radiusFeet": 20, "casterAFeet": feet,
                                   "centerRangeFeet": round(center_range, 9),
                                   "sourceGeometry": {"source": "Q23 answer plus inherited case and unadopted proposal 395",
                                                      "bounds": [0, 120, 0, 120, 0, 40], "courtyard": [5, 115, 5, 115],
                                                      "support": {"z": 0, "bounds": [0, 120, 0, 120]},
                                                      "panelProposal": "one-inch prism z=0..1/12 on existing datum"},
                                   "occupiedPanelProposal395": geometry["occupiedPanel"],
                                   "fieldIntersectionAndCoverProposal395": geometry["fieldIntersectionAndCover"],
                                   "verticalReturnProjection395": geometry["verticalReturnProjection395"],
                                   "triggerRule": "Do not establish Q27 until proposal premises are Director-reviewed and owner-adopted and actual paid-field evidence is separately established."}
    packet["conditionalTerminalPlan"]["placementBoundsProposal"] = "PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-395"
    packet["openRequirementsBeforeIntegratedWitness"][0]["requirement"] = "Review the scoped panel support/contact, exposed-face ray, and explicit vertical return projection in proposal 395; then consider a scoped W01 Q27 sub-witness."
    packet["openRequirementsBeforeIntegratedWitness"][0]["sourceStatus"] = "Proposal 395 is unadopted and awaits Director review; W01 compatible damage remains open."
    packet["openRequirementsBeforeIntegratedWitness"][4]["requirement"] = "Only after accepted panel predicate and terminal contract, build reversible integrated W08 witness with proposal 395 carrier bounds."
    packet["directorReviewRequest"]["questions"] = request["reviewQuestions"]
    packet["proposedGeometryProposal395"] = {"path": GEOMETRY, "status": geometry["status"]}
    packet["proposedCarrierBounds395"] = {"path": CARRIER, "status": carrier["status"]}
    packet["proposedSupportCoverContract395"] = {"path": SUPPORT, "status": support["status"]}
    packet["proposedGeometryProposal394"]["status"] = "SUPERSEDED_BY_PROPOSAL_395_UNADOPTED"
    packet["proposedCarrierBounds394"]["status"] = "SUPERSEDED_BY_PROPOSAL_395_UNADOPTED"
    packet["geometryCarrierRepair395"] = {"priorPrebuild394Sha256": old_delivery["prebuildSha256"],
                                           "directorReview394Sha256": "PENDING_DIRECTOR394_HASH",
                                           "geometryProposalPath": GEOMETRY, "carrierProposalPath": CARRIER,
                                           "supportCoverContractPath": SUPPORT, "terminationProposalPath": term_name,
                                           "reviewRequestPath": REQUEST, "fixtureMutated": False, "actualCast": False,
                                           "ownerAdoptionOf395": False}
    packet["id"] = "PG328-W08-OCCUPIED-ANTIMAGIC-SUPPORT-COVER-LOCATOR-REPAIR-395"
    packet["createdAtUtc"] = NOW
    packet["status"] = "SUPPORT_COVER_AND_SOURCE_LOCATOR_PROPOSALS_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION"
    packet["scope"]["supersedes"] = "PG328-W08-OCCUPIED-ANTIMAGIC-PREBUILD-GEOMETRY-CARRIER-REPAIR-394"
    packet["scope"].update({"actualCastPerformed": False, "fixtureMutated": False,
                            "spellIdentityAcceptedOrApplied": False, "ordinarySpellQueueChanged": False,
                            "noCanonicalRuleChange": True, "ownerAdoptionOf395": False})

    geometry_raw = jbytes(geometry)
    carrier_raw = jbytes(carrier)
    support_raw = jbytes(support)
    request_raw = jbytes(request)
    director_hash = sha(director394_raw)
    support["directorFinding394"]["sha256"] = director_hash
    request["priorDirectorReview394"]["sha256"] = director_hash
    packet["geometryCarrierRepair395"]["directorReview394Sha256"] = director_hash
    # Re-serialize after binding the Director record hash into all dependent artifacts.
    support_raw = jbytes(support)
    request_raw = jbytes(request)
    geometry_hash = sha(geometry_raw)
    carrier_hash = sha(carrier_raw)
    support_hash = sha(support_raw)
    packet["proposedGeometryProposal395"]["sha256"] = geometry_hash
    packet["proposedCarrierBounds395"]["sha256"] = carrier_hash
    packet["proposedSupportCoverContract395"]["sha256"] = support_hash
    packet_raw = jbytes(packet)
    packet_hash = sha(packet_raw)

    manifest = copy.deepcopy(json.loads(old_files["authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_394.json"]))
    manifest.update({"id": "PG328-W08-PREBUILD-SOURCE-BINDINGS-395", "createdAtUtc": NOW,
                     "status": "HASH_VERIFIED_UNADOPTED_SUPPORT_COVER_AND_FULL_LOCATORS_395",
                     "prebuildPath": PREBUILD, "prebuildSha256": packet_hash,
                     "supersedesManifest": "PG328-W08-PREBUILD-SOURCE-BINDINGS-394",
                     "bundleMemberPath": "payload/" + PREBUILD})
    manifest["priorDirectorReview394"] = {"bundleMember": "prior394/authority/" + DIRECTOR394,
                                           "sha256": director_hash, "bytes": len(director394_raw)}
    manifest["caseMemberBinding"]["bundleMember"] = CASE_MEMBER
    manifest["caseMemberBinding"]["memberSha256"] = sha(case_bytes)
    manifest["caseMemberBinding"]["memberBytes"] = len(case_bytes)
    manifest["reviewProposals"] = [
        {"name": GEOMETRY, "bundleMember": "payload/proposals/" + GEOMETRY, "sha256": geometry_hash,
         "bytes": len(geometry_raw), "status": geometry["status"]},
        {"name": CARRIER, "bundleMember": "payload/proposals/" + CARRIER, "sha256": carrier_hash,
         "bytes": len(carrier_raw), "status": carrier["status"]},
        {"name": SUPPORT, "bundleMember": "payload/proposals/" + SUPPORT, "sha256": support_hash,
         "bytes": len(support_raw), "status": support["status"]},
        {"name": term_name, "bundleMember": "payload/proposals/" + term_name, "sha256": sha(term_bytes),
         "bytes": len(term_bytes), "status": term["status"]}
    ]
    manifest["supersededProposalHashes"] = {"geometry386": "83d942662c8ddac274f8e9c3b03aa65bd0a8bd23c0a462ebe0ee5ca705f47465",
                                             "carrier386": "cae91912315af9a14ea749750a39dc33f6a986b969b0f22868d9eb3a86e8e674",
                                             "geometry394": old_delivery["geometryProposalSha256"],
                                             "carrier394": old_delivery["carrierProposalSha256"]}
    manifest["reviewRequest"] = {"bundleMember": "payload/" + REQUEST, "sha256": sha(request_raw), "bytes": len(request_raw)}
    manifest["nonAdoptionNotice"] = "All proposal 395 premises and the unchanged field termination proposal 386 remain unadopted. No cast, Q27 settlement, fixture mutation, W08 seal, Fortress acceptance/application, hold change, or queue change."
    manifest_raw = jbytes(manifest)

    # Bind the corrected geometry hash into carrier references and recompute those dependent bytes.
    carrier["sourceBindings"][-1]["sha256"] = geometry_hash
    carrier_raw = jbytes(carrier)
    carrier_hash = sha(carrier_raw)
    packet["proposedCarrierBounds395"]["sha256"] = carrier_hash
    packet_raw = jbytes(packet)
    packet_hash = sha(packet_raw)
    manifest["prebuildSha256"] = packet_hash
    manifest["reviewProposals"][1].update({"sha256": carrier_hash, "bytes": len(carrier_raw)})
    manifest_raw = jbytes(manifest)

    (OUT / GEOMETRY).write_bytes(geometry_raw)
    (OUT / CARRIER).write_bytes(carrier_raw)
    (OUT / SUPPORT).write_bytes(support_raw)
    (OUT / REQUEST).write_bytes(request_raw)
    (OUT / DIRECTOR394).write_bytes(director394_raw)
    (OUT / PREBUILD).write_bytes(packet_raw)
    (OUT / MANIFEST).write_bytes(manifest_raw)

    zip_path = OUT / ZIP_NAME
    map_to_prior394 = {
        "authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_394.json",
        "payload/" + PREBUILD,
        "payload/PG328-W08_DIRECTOR_REVIEW_REQUEST_394.json",
        "payload/proposals/PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_394_TESTONLY.json",
        "payload/proposals/PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_394_TESTONLY.json"
    }
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in old_files.items():
            if name in map_to_prior394:
                z.writestr("prior394/" + name, data)
            else:
                z.writestr(name, data)
        z.writestr("prior394/authority/" + DIRECTOR394, director394_raw)
        z.writestr("authority/" + MANIFEST, manifest_raw)
        z.writestr("payload/" + PREBUILD, packet_raw)
        z.writestr("payload/" + REQUEST, request_raw)
        z.writestr("payload/proposals/" + GEOMETRY, geometry_raw)
        z.writestr("payload/proposals/" + CARRIER, carrier_raw)
        z.writestr("payload/proposals/" + SUPPORT, support_raw)

    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
        assert z.read(CASE_MEMBER) == case_bytes
        assert sha(z.read(CASE_MEMBER)) == CASE_SHA
        assert json.loads(z.read("payload/proposals/" + GEOMETRY))["fieldIntersectionAndCover"]["centerFeet"] == center
        assert json.loads(z.read("payload/proposals/" + CARRIER))["bodyConvention"]["feetAnchor"] == feet
        assert json.loads(z.read("payload/proposals/" + SUPPORT))["scope"]["ownerAdoptionRequired"] is True
        corrected_carrier = json.loads(z.read("payload/proposals/" + CARRIER))
        assert all("..." not in source["path"] for source in corrected_carrier["sourceBindings"])
        assert all(source["path"].startswith(CASE_MEMBER + "#") for source in corrected_carrier["sourceBindings"][:4])
        assert sha(z.read("prior394/authority/" + DIRECTOR394)) == director_hash
        assert len(z.infolist()) == len(old_files) + 7

    delivery = {
        "id": "DD-RANK9-PG328-W08-SUPPORT-COVER-LOCATOR-REPAIR-395-TESTONLY-DELIVERY",
        "createdAtUtc": NOW, "status": "READY_FOR_DIRECTOR_REVIEW_PENDING_TRANSMISSION",
        "supersedes": old_delivery["id"], "artifact": ZIP_NAME,
        "sha256": sha(zip_path.read_bytes()), "bytes": zip_path.stat().st_size,
        "bundleMemberCount": len(zipfile.ZipFile(zip_path).infolist()),
        "prebuildSha256": packet_hash, "sourceBindingsSha256": sha(manifest_raw),
        "geometryProposalSha256": geometry_hash, "carrierProposalSha256": carrier_hash,
        "supportCoverContractSha256": support_hash, "reviewRequestSha256": sha(request_raw),
        "directorReview394Sha256": director_hash, "originalCaseMemberSha256": CASE_SHA,
        "directorConversation": old_delivery["directorConversation"],
        "fixtureMutated": False, "actualCast": False, "ownerAdoptionOf395": False,
        "identityHold": "PG200-B06 remains held", "ordinaryQueue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
        "transmissionStatus": "NOT_YET_SENT"
    }
    (OUT / DELIVERY).write_bytes(jbytes(delivery))

    # Small deterministic geometric and artifact invariants.
    assert max(distances) < 20 and center_range < 20
    assert all(not overlaps(after[x], after[y]) for x, y in (("focus-A", "pack-A"), ("focus-A", "cargo-A"), ("pack-A", "cargo-A")))
    assert support["proposedPanelContract"]["supportsMassLb"] == 162
    print(json.dumps({"zip": str(zip_path), "sha256": delivery["sha256"], "bytes": delivery["bytes"],
                      "members": delivery["bundleMemberCount"], "geometrySha256": geometry_hash,
                      "carrierSha256": carrier_hash, "supportContractSha256": support_hash,
                      "director394Sha256": director_hash, "centerFeet": center,
                      "panelSidePointFeet": side_point, "centerToActorFeet": round(center_range, 9),
                      "maxPanelCornerDistanceFeet": round(max(distances), 9),
                      "returnVerticalAdjustmentFeet": -1 / 12, "integrity": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
