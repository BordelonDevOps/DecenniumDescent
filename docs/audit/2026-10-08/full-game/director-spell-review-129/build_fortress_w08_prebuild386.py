from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PREV = ROOT / "fortress_w08_occupied_antimagic_prebuild_385"
OUT = ROOT / "fortress_w08_occupied_antimagic_prebuild_386"
INTAKE = ROOT / "conjure_demiplane_fortress_closure_intake_367" / "payload"
PACKET_NAME = "PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json"
MANIFEST_NAME = "PG328-W08_PREBUILD_SOURCE_BINDINGS_386.json"
ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_Prebuild386_DirectorRepair.zip"
DELIVERY_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_Prebuild386_DirectorRepair_DELIVERY.json"
SOURCE_SPECS = [
    ("wizard.json", "conjure_demiplane_fortress_closure_intake_367/payload/sources/wizard.json", "payload/sources/wizard.json", ["/engine/11", "/engine/12", "/cards/15", "/cards/17"]),
    ("COMBAT_ACTION_PLAYTEST.md", "conjure_demiplane_fortress_closure_intake_367/payload/sources/COMBAT_ACTION_PLAYTEST.md", "payload/sources/COMBAT_ACTION_PLAYTEST.md", ["#Time and event ordering — NEW"]),
    ("BODY_EQUIPMENT_PLAYTEST.md", "conjure_demiplane_fortress_closure_intake_367/payload/sources/BODY_EQUIPMENT_PLAYTEST.md", "payload/sources/BODY_EQUIPMENT_PLAYTEST.md", ["#Placement and involuntary endings", "#Carrying and Load"]),
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, data) -> bytes:
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def source_record(name: str, relative: str, bundle_member: str, pointers: list[str]) -> dict:
    raw = (ROOT / relative).read_bytes()
    return {
        "name": name,
        "repositoryPath": (Path("docs/audit/2026-10-08/full-game/director-spell-review-129") / relative).as_posix(),
        "bundleMember": bundle_member,
        "sha256": sha(raw),
        "bytes": len(raw),
        "pointers": pointers,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    old_packet = load(PREV / "PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json")
    packet = copy.deepcopy(old_packet)
    now = utc_now()
    packet["id"] = "PG328-W08-OCCUPIED-ANTIMAGIC-PREBUILD-DIRECTOR-REPAIR-386"
    packet["createdAtUtc"] = now
    packet["status"] = "CORRECTED_PREBUILD_WITH_TESTONLY_PROPOSALS_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION"
    packet["scope"]["supersedes"] = "PG328-W08-OCCUPIED-ANTIMAGIC-PREBUILD-385"
    packet["scope"]["actualCastPerformed"] = False
    packet["scope"]["integratedWitnessConstructed"] = False
    packet["scope"]["fortressSettlementExecuted"] = False
    packet["scope"]["spellIdentityAcceptedOrApplied"] = False
    packet["scope"]["fixtureMutated"] = False
    packet["scope"]["ordinarySpellQueueChanged"] = False
    packet["scope"]["noCanonicalRuleChange"] = True

    # The inherited case and the preserved authored sources remain immutable.
    packet["proposedCastState"]["proposedCastAfterRefresh"]["cadenceGate"] = (
        "The inherited Spell Efficiency window is family-specific. Its Fortress-family "
        "discount through case time 6.9 does not prohibit an Abjuration-family cast. "
        "The earliest proposed cast remains after A's actual START refresh at case 6.0 / "
        "world 6.1; recompute all live predicates before any authorized cast."
    )
    packet["proposedCastState"]["proposedCastAfterRefresh"]["postRefreshStateRequired"] = {
        "action": 1,
        "bonusAction": 1,
        "reaction": 1,
        "movementFeet": 30,
        "magicThisTurn": False,
        "RP": 54,
        "precastDissonance": 0,
        "precastRefrain": 0,
        "preserveLastSpell": "conjure-demiplane-fortress until Antimagic commits",
        "preserveInheritedSpellEfficiencyUntilCaseTime": 6.9,
        "priorLastSpell": "conjure-demiplane-fortress",
        "priorPreparedFamiliesUsed": ["conjure-demiplane-fortress"],
        "priorSpellHistoryCount": 1,
        "priorResourceHistoryCount": 1,
        "priorSpellEfficiency": {"family": "conjure-demiplane-fortress", "untilCaseTime": 6.9},
        "pendingNextRegularEndCaseTime": 6.9,
        "doNotCarryForwardPriorTurnMagicThisTurn": True,
    }
    packet["proposedCastState"]["proposedCastAfterRefresh"]["postCommitCandidateState"] = {
        "action": 0,
        "RP": 33,
        "lastSpell": "antimagic-field",
        "preparedFamiliesUsed": ["conjure-demiplane-fortress", "antimagic-field"],
        "firstPreparedFamily": True,
        "baseDissonance": 0,
        "Refrain": 0,
        "DissonanceAfterCommit": 0,
        "magicThisTurn": True,
        "concentration": {
            "spellId": "antimagic-field",
            "owner": "A",
            "establishedAtWorldElapsedSeconds": 6.1,
            "originalMaximumDeadlineWorldElapsedSeconds": 66.1,
            "status": "candidate only; requires a lawful uncountered cast",
        },
        "antimagicFamilySpellEfficiencyEligibilityThrough": {
            "caseTime": 12.9,
            "worldElapsedSeconds": 13.0,
            "meaning": "next future regular END for A; do not reset or transfer the inherited Fortress-family endpoint",
        },
    }
    packet["proposedCastState"]["proposedCastAfterRefresh"]["postCommitHistoryAppend"] = {
        "spellHistory": {
            "castId": "PG328-W08/occupied-antimagic/antimagic-field-cast1",
            "spellId": "antimagic-field",
            "class": "Wizard",
            "school": "Abjuration",
            "rank": 8,
            "cost": 21,
            "firstPreparedFamily": True,
            "baseDissonance": 0,
            "Refrain": 0,
            "originPlane": "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic/cast1/space",
            "targetCenterFeet": [20, 10, 8],
            "components": ["V", "S", "F"],
            "caseTime": 6.0,
            "worldElapsedSeconds": 6.1,
        },
        "resourceHistory": {"event": "PG328-W08/occupied-antimagic/antimagic-field-cast1", "RP": -21, "poolAfter": 33, "discount": False},
        "budgetCommitment": {"ActionBefore": 1, "ActionAfter": 0, "otherBudgetChanges": "none proposed"},
        "status": "candidate append only after a lawful cast; no history is written to the inherited case by this packet",
    }
    packet["proposedCastState"]["sequenceReview386"] = {
        "base": {"caseTime": 0.9, "worldElapsedSeconds": 1.0},
        "events": [
            {"actor": "B", "caseStart": 1.0, "worldStart": 1.1, "caseEnd": 1.9, "worldEnd": 2.0, "branch": "proposed TEST_ONLY no-op/pass; Director review required"},
            {"actor": "C", "caseStart": 2.0, "worldStart": 2.1, "caseEnd": 2.9, "worldEnd": 3.0, "branch": "proposed TEST_ONLY no-op/pass; Director review required"},
            {"actor": "D", "caseStart": 3.0, "worldStart": 3.1, "caseEnd": 3.9, "worldEnd": 4.0, "branch": "proposed TEST_ONLY no-op/pass; Director review required"},
            {"actor": "A", "caseStart": 6.0, "worldStart": 6.1, "caseEnd": 6.9, "worldEnd": 7.0, "branch": "preserve pending END, process actual START refresh, then re-read cast predicates"},
        ],
        "clockRule": "Maintain the inherited 1:1 world/source/effect clock bridge. These are proposed branch events, not executed turns.",
    }
    # Correct the point-to-wall distance and state that this remains non-trigger evidence.
    packet["candidateGeometry"]["secondaryStructureCandidate"]["distanceFeet"] = 16.552945
    packet["candidateGeometry"]["secondaryStructureCandidate"]["calculation"] = "sqrt((20-5)^2 + (10-10)^2 + (8-15)^2) = sqrt(274) = 16.552945 ft"
    packet["candidateGeometry"]["secondaryStructureCandidate"]["status"] = "Within nominal radius; the proposed W01 support/geometry input does not treat this wall point as a target or prove occupied-structure suppression."
    packet["candidateGeometry"]["coverClipping"] = (
        "The proposed W01 sub-witness enumerates the relevant open-courtyard panel set and center rays. "
        "It is an unadopted TEST_ONLY geometry input; do not infer campaign geometry, unobstructed line of effect, "
        "or Q27 trigger until Owner adoption and Director review."
    )

    profile = load(INTAKE / "sources" / "RETURN284_WIZARD20_PROFILE_TESTONLY.json")
    wizard_path = ROOT / "conjure_demiplane_fortress_closure_intake_367" / "payload" / "sources" / "wizard.json"
    wizard = load(wizard_path)
    spell_efficiency_card = wizard["cards"][15] if len(wizard["cards"]) > 15 else None
    wizard_counterspell_card = wizard["cards"][17] if len(wizard["cards"]) > 17 else None
    auto_cards = profile.get("automaticCards", [])
    always_prepared = profile.get("alwaysPrepared", [])
    capabilities = profile.get("allAcquiredClassCapabilities", [])
    packet["counterspellAndSchedule"]["ruleBindings386"] = {
        "wizardEnginePointers": ["wizard.json#/engine/11", "wizard.json#/engine/12"],
        "timingSource": "COMBAT_ACTION_PLAYTEST.md (regular START/END refresh and scheduling passages)",
        "spellEfficiencyPointer": "wizard.json#/cards/15",
        "spellEfficiencyCard": spell_efficiency_card,
        "wizardCounterspellCardPointer": "wizard.json#/cards/17",
        "wizardCounterspellCard": wizard_counterspell_card,
        "profileAutomaticCounterspell": auto_cards[1] if len(auto_cards) > 1 else None,
        "profilePointers": {
            "automaticCard": "/automaticCards/1",
            "alwaysPrepared": "/alwaysPrepared/10",
            "acquiredCapability": "/allAcquiredClassCapabilities/26",
        },
        "wizard20ProfileSha256": packet["conditionalWizardAcquisition"]["sha256"],
        "allProfileFactsRecheckedFromBoundSource": bool(auto_cards and always_prepared and capabilities),
    }
    for name, rel, bundle, pointers in SOURCE_SPECS:
        packet["sourceBindings"] = [b for b in packet["sourceBindings"] if b.get("name") != name]
        packet["sourceBindings"].append(source_record(name, rel, bundle, pointers))
    packet["counterspellAndSchedule"]["boundProfileCheck"] = {
        "actorBindings": {
            "A": {"class": "Wizard", "level": 20, "profileSha256": "ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223", "counterspellAccess": "Wizard20 automatic card and always-prepared access; no self-response proposed"},
            "B": {"class": "Wizard", "level": 20, "profileSha256": "ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223", "counterspellAccess": "Wizard20 automatic card and always-prepared access"},
            "C": {"class": "Cleric", "level": 20, "profileSha256": "5c3da13c7faf84089b8a118a7da67cb4654f5ee0d5b04a09abcc0118aa47e6c8", "counterspellAccess": "No Counterspell source/profile capability is bound in this packet; do not infer access or nonaccess beyond supplied binding."},
            "D": {"class": "Wizard", "level": 20, "profileSha256": "ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223", "counterspellAccess": "Wizard20 automatic card and always-prepared access"},
        },
        "counterspellAcquisition": {"automaticCardPointer": "/automaticCards/1", "alwaysPreparedPointer": "/alwaysPrepared/10", "acquiredCapabilityPointer": "/allAcquiredClassCapabilities/26", "wizardCard": "wizard.json#/cards/17"},
        "counterspellTiming": "Cast-time only under the accepted Antimagic procedure; no reaction occurs after the field resolves.",
        "BAndDEligibility": "Access is present. The inherited outside-plane locations and open entrance do not establish cross-plane perception, range, targetability, or line of effect for this cast. Record trigger/targeting eligibility as NOT ESTABLISHED; no reaction taken.",
        "CEligibility": "Use the actual Cleric20 binding; no Counterspell access is established by this packet.",
        "AEligibility": "No self-Counterspell event is proposed.",
    }
    packet["counterspellAndSchedule"]["finding"] = (
        "Do not infer Counterspell unavailability from the prepared array. A, B, and D have the Wizard20 "
        "automatic/always-prepared Counterspell binding; C is Cleric20. B and D are outside the generated "
        "space and their cross-plane cast-time trigger/target eligibility is NOT ESTABLISHED through the open "
        "entrance. No reaction is taken or assumed. No self-response for A."
    )

    geometry_proposal = {
        "id": "PG328-W01-W08-OCCUPIED-PANEL-GEOMETRY-PROPOSAL-386",
        "createdAtUtc": now,
        "status": "PROPOSED_TEST_ONLY_INPUT_PENDING_OWNER_ADOPTION_AND_DIRECTOR_REVIEW",
        "scope": {"witnessId": "PG328-W08", "subWitnessId": "PG328-W01", "case": "Return284 occupied-antimagic case only", "fixtureMutated": False, "canonicalGeometryChanged": False, "W01CompatibleDamageObligationCompleted": False},
        "sourceBindings": [
            {"path": "PG328_QUESTION_DISPOSITIONS.json#/questions/2/answer", "use": "Q23 authored 5x5 floor-panel dimensions, 120-foot enclosure, courtyard bounds and named elevations; it explicitly leaves the exact support graph unresolved."},
            {"path": "Return284 occupied-antimagic case#/final/actors/A", "sha256": "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900", "use": "A position [15,10,0], Medium bodyBox [5,5,6], and ground contact at z=0."},
            {"path": "Return284 occupied-antimagic case#/final/spaces/<Fortress-space>/support", "sha256": "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900", "use": "Aggregate support plane z=0 only; does not supply named panel IDs or connections."},
            {"path": "ANTIMAGIC_FIELD_MODEL_149.json#/spells/2/procedure", "use": "Fixed center [20,10,8] candidate, 20-foot radius, actual-solid-total-cover clipping."},
        ],
        "proposedCoordinates": {"plane": "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic/cast1/space", "units": "feet", "AFeetPositionConvention": "The inherited Medium [5,5,6] body occupies x/y ±2.5 about position and z=[position.z, position.z+6]; Director must confirm this interpretation."},
        "AOccupancy": {"position": [15,10,0], "bodyBounds": {"x": [12.5,17.5], "y": [7.5,12.5], "z": [0,6]}, "fullFootprintCoveredByPanels": True, "contactSurfaceZ": 0},
        "proposedPanelPremise": {"panelPlanSizeFeet": [5,5], "panelThicknessFeet": 0.5, "panelThicknessStatus": "new fixture premise, not specified by Q23; owner adoption and Director review required", "panelHP": 60, "panelAC": 17, "topSurfaceZ": 0, "bottomSurfaceZ": -0.5, "supportBase": "inherited test fixture support datum z=0 is not reinterpreted; a rigid test-only footing/contact premise beneath the four panels is proposed but is not a campaign fact"},
        "panels": [
            {"id": "W08-FLOOR-10-05", "boundsFeet": {"x": [10,15], "y": [5,10], "z": [-0.5,0]}, "supportsAContactFootprint": True, "coverFromFieldCenter": False},
            {"id": "W08-FLOOR-15-05", "boundsFeet": {"x": [15,20], "y": [5,10], "z": [-0.5,0]}, "supportsAContactFootprint": True, "coverFromFieldCenter": False},
            {"id": "W08-FLOOR-10-10", "boundsFeet": {"x": [10,15], "y": [10,15], "z": [-0.5,0]}, "supportsAContactFootprint": True, "coverFromFieldCenter": False},
            {"id": "W08-FLOOR-15-10", "boundsFeet": {"x": [15,20], "y": [10,15], "z": [-0.5,0]}, "supportsAContactFootprint": True, "coverFromFieldCenter": False},
        ],
        "supportAndConnectionGraph": {
            "AContactSupportEdges": ["W08-FLOOR-10-05 -> A", "W08-FLOOR-15-05 -> A", "W08-FLOOR-10-10 -> A", "W08-FLOOR-15-10 -> A"],
            "panelAdjacencyEdges": [
                ["W08-FLOOR-10-05", "W08-FLOOR-15-05", "shared edge x=15, y=5..10"],
                ["W08-FLOOR-10-05", "W08-FLOOR-10-10", "shared edge y=10, x=10..15"],
                ["W08-FLOOR-15-05", "W08-FLOOR-15-10", "shared edge y=10, x=15..20"],
                ["W08-FLOOR-10-10", "W08-FLOOR-15-10", "shared edge x=15, y=10..15"],
            ],
            "supportModelStatus": "proposed local fixture graph only; it does not bind or complete the campaign W01 structural graph",
        },
        "fieldIntersectionAndCover": {
            "centerFeet": [20,10,8], "radiusFeet": 20, "placementRangeFromAFeet": 9.433981,
            "farthestRelevantPanelCornerFeet": 13.747727, "farthestPoint": [10,5,0],
            "rayEnvironment": "All proposed panel cells and center-to-panel segments remain in the authored open courtyard bounds [5,115]x[5,115]; no wall/door is crossed by these proposed rays. The enclosure is open above the courtyard. This is conditional on the proposed geometry and no additional instantiated obstruction.",
            "secondaryWestWallCheck": {"point": [5,10,15], "distanceFeet": 16.552945, "calculation": "sqrt(274)", "role": "nominal corroboration only, not an occupied-panel target"},
            "sphereContainsAllFourProposedPanelVolumes": True,
        },
        "Q27TriggerQuestion": "If owner-adopted and Director-verified, does suppression of the four proposed panels bearing A's full footprint constitute suppression of an occupied structural region under PG9-Q27? This proposal does not answer that rule question itself.",
        "adoptionBoundary": "This geometry is a new, scoped TEST_ONLY fixture premise. It is not source-backed campaign geometry, does not prove compatible structural damage, does not clear PG200-B06, and cannot be used in an integrated W08 witness until separately owner-adopted and Director-reviewed.",
    }

    carrier_proposal = {
        "id": "PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-386",
        "createdAtUtc": now,
        "status": "PROPOSED_TEST_ONLY_PLACEMENT_INPUT_PENDING_DIRECTOR_REVIEW",
        "scope": "Candidate Q27 projection for the same W08 branch only; no terminal state is executed.",
        "sourceCaseSha256": "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900",
        "sourceFields": "final.actors.A.position/bodyBox/orientation/equipment; final.items.focus-A/pack-A/cargo-A sizeFeet/owner/custodian; effects.<Fortress>.apertures; spaces.fixture:origin.support",
        "bodyConvention": "Proposed fixture convention: A's feet anchor is [15,0,0], horizontal footprint is centered on x/y and bodyBox [5,5,6] occupies z=[0,6].",
        "candidateAnchorFeet": [15,0,0],
        "bodyRelativeBoundsFeet": {"x": [-2.5,2.5], "y": [-2.5,2.5], "z": [0,6]},
        "carriedItems": [
            {"id": "focus-A", "owner": "A", "custodian": "A", "sizeFeet": [0.5,0.5,0.5], "relativeBoundsFeet": {"x": [2.5,3.0], "y": [-0.25,0.25], "z": [1.0,1.5]}},
            {"id": "pack-A", "owner": "A", "custodian": "A", "sizeFeet": [0.5,0.5,0.5], "relativeBoundsFeet": {"x": [3.0,3.5], "y": [-0.25,0.25], "z": [1.0,1.5]}},
            {"id": "cargo-A", "owner": "A", "custodian": "A", "sizeFeet": [1,1,1], "relativeBoundsFeet": {"x": [3.5,4.5], "y": [-0.5,0.5], "z": [1.0,2.0]}},
        ],
        "worldBoundsAtCandidateAnchor": {
            "A": {"x": [12.5,17.5], "y": [-2.5,2.5], "z": [0,6]},
            "focus-A": {"x": [17.5,18.0], "y": [-0.25,0.25], "z": [1,1.5]},
            "pack-A": {"x": [18.0,18.5], "y": [-0.25,0.25], "z": [1,1.5]},
            "cargo-A": {"x": [18.5,19.5], "y": [-0.5,0.5], "z": [1,2]},
        },
        "combinedConflictCheck": {
            "outsideBodies": {
                "B": {"x": [-2.5,2.5], "y": [12.5,17.5], "z": [0,6]},
                "C": {"x": [-2.5,2.5], "y": [-2.5,2.5], "z": [0,6]},
                "D": {"x": [2.5,7.5], "y": [2.5,7.5], "z": [0,6]},
            },
            "result": "Candidate body and three carried-item boxes have no positive-volume overlap with B/C/D under the stated geometry convention; boundaries may touch. All item identities and A custody are retained.",
            "terrainSupport": "fixture:origin support plane z=0 and bounds [-200,200]x[-200,200] contain A and all proposed carried boxes.",
            "reviewLimit": "Relative item slots and feet-anchor convention are new test fixture placement inputs; Director review is required before any terminal placement is certified.",
        },
    }

    terminal_proposal = {
        "id": "OWNER-PG328-W08-ANTIMAGIC-FIELD-TERMINATION-PROPOSAL-386",
        "createdAtUtc": now,
        "status": "PROPOSED_NEW_SCOPED_TEST_ONLY_CONTRACT_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION",
        "scope": {"witnessId": "PG328-W08", "case": "Return284 occupied-antimagic case only", "fieldCastId": "PG328-W08/occupied-antimagic/antimagic-field-cast1", "trigger": "candidate Q27 Fortress whole-source termination following demonstrated occupied-panel suppression", "canonicalRuleChange": False},
        "sourceGap": "ANTIMAGIC_FIELD_MODEL_149 fixes the center, ties the effect to A's concentration and caps duration at 60 seconds; PG9-Q27 settles Fortress occupants/items but neither source disposes of this independent field when its containing generated space ends.",
        "exactProposedTerms": {
            "beforeParentTermination": "The paid, uncountered field remains an independent active effect at its original fixed center and original plane through evaluation of the Q27 trigger; this proposal adds no early suppression or concentration change.",
            "eventOrder": [
                "Resolve the proposed field's center-clipped suppression against the Director-approved occupied panel witness.",
                "If and only if Q27's occupied-structure predicate is met, perform the existing Q27 Fortress body/item terminal settlement at the same event timestamp.",
                "After the Fortress geometry is removed, immediately terminate the independent Antimagic effect because this scoped contract does not permit an effect centered in the ended generated space to relocate or persist there.",
            ],
            "fieldIdentity": "Retain the Antimagic cast/effect identity as an inactive terminal record with end reason PG328-W08 scoped containing-space termination; do not delete its historical record.",
            "center": "Never relocate; retain the original generated-plane center coordinates only as historical provenance.",
            "concentration": "End A's concentration linkage to this effect at the field-termination event; do not transfer concentration to another actor or effect.",
            "originalDeadline": "Preserve the original maximum deadline worldElapsedSeconds=66.1 as a historical cap; termination does not reset, extend or consume additional duration.",
            "costAndHistory": "Keep the 21-RP cast payment and all casting-history/resource entries; no refund or rollback.",
            "noContinuance": "The field has no active volume after the termination event and no effect is asserted in the exterior plane.",
        },
        "adoptionAndReviewLimits": {
            "ownerAdoptionRequired": True,
            "directorReviewRequired": True,
            "useBeforeAdoption": "None; proposal only.",
            "doesNot": ["change canonical rules", "clear PG200-B06", "establish W08", "execute a cast", "settle the Fortress", "change queue/hold/seal state", "settle W03 or Proposal 382"],
            "requestedOwnerReply": "Yes—adopt the exact W08 field-termination proposal 386 for PG328-W08 and the named occupied-antimagic fixture only, subject to GPT Director review.",
        },
    }

    geom_raw = dump(OUT / "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_386_TESTONLY.json", geometry_proposal)
    carrier_raw = dump(OUT / "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_386_TESTONLY.json", carrier_proposal)
    terminal_raw = dump(OUT / "OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json", terminal_proposal)
    packet["proposedGeometryProposal386"] = {
        "path": "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_386_TESTONLY.json",
        "sha256": sha(geom_raw), "status": geometry_proposal["status"],
    }
    packet["proposedCarrierBounds386"] = {
        "path": "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_386_TESTONLY.json",
        "sha256": sha(carrier_raw), "status": carrier_proposal["status"],
    }
    packet["proposedFieldTerminationContract386"] = {
        "path": "OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json",
        "sha256": sha(terminal_raw), "status": terminal_proposal["status"],
    }
    packet["conditionalTerminalPlan"]["antimagicFieldAfterParentEnd"] = {
        "status": "UNRESOLVED_PENDING_DIRECTOR_REVIEW_AND_SEPARATE_OWNER_ADOPTION; blocks integrated W08 terminal state",
        "proposalPath": terminal_proposal["id"],
        "facts": "No current bound source disposes of the independent field at containing-space termination. Proposal 386 supplies exact new test-only terms but is not adopted and cannot be executed.",
        "prohibitedAssumptions": ["no relocation", "no termination except under separately adopted proposal", "no prolongation", "no refund"],
    }
    packet["conditionalTerminalPlan"]["placementBoundsProposal"] = carrier_proposal["id"]
    packet["openRequirementsBeforeIntegratedWitness"] = [
        {"id": "W08-1", "requirement": "Review the exact four-panel geometry/support proposal for A's whole body footprint and center-clipped field coverage; confirm whether it is an acceptable scoped TEST_ONLY W01 sub-witness for Q27.", "sourceStatus": "Proposal 386 is not owner-adopted or Director-approved; does not complete W01's compatible-damage obligation."},
        {"id": "W08-2", "requirement": "Review and, separately, obtain owner adoption of the proposed independent-field end contract before terminal integration.", "sourceStatus": "Proposal 386 is NOT_ADOPTED; current rules remain silent."},
        {"id": "W08-3", "requirement": "Director review of B/C/D explicit pass turns and 1:1 START/END processing.", "sourceStatus": "Proposed test branch choices only."},
        {"id": "W08-4", "requirement": "Only after prerequisite review, revalidate actual center perception/line of effect, refreshed Action, current cost, history, counters, and concentration; do not execute in this packet.", "sourceStatus": "No cast executed."},
        {"id": "W08-5", "requirement": "After approved panel predicate and terminal contract, build a reversible whole-Fortress witness with all live identities, cargo, clocks, and field status.", "sourceStatus": "Not constructed."},
    ]
    packet["review385Repairs"] = [
        {"repair": "Counterspell access", "status": "corrected", "detail": "Wizard20 automatic/always-prepared access for A/B/D; C is Cleric20; B/D cross-plane trigger eligibility unestablished; no reaction taken."},
        {"repair": "Spell Efficiency", "status": "corrected", "detail": "Family-specific discount only; no restriction on this different-family candidate cast at A's refreshed 6.0/6.1 turn."},
        {"repair": "Wall distance", "status": "corrected", "detail": "sqrt(274)=16.552945 feet."},
        {"repair": "JSON root locators", "status": "corrected", "detail": "Whole-document bindings use the valid empty JSON Pointer string \"\"; no slash-only root pointer remains."},
        {"repair": "Prebuild bundle member", "status": "corrected", "detail": "Manifest points to payload/PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json."},
        {"repair": "Placement bounds", "status": "proposed", "detail": "Separate carrier-relative bounds fixture proposal; pending Director review."},
    ]
    for binding in packet.get("sourceBindings", []):
        if binding.get("pointers") == ["/"]:
            binding["pointers"] = [""]
    if any(binding.get("pointers") == ["/"] for binding in packet.get("sourceBindings", [])):
        raise RuntimeError("Packet still contains a slash-only JSON root pointer")
    packet["directorReviewRequest"] = {
        "priority": "Corrected prebuild only; review before any integrated witness.",
        "questions": [
            "Does the proposed four-panel TEST_ONLY sub-witness cover A's entire 5x5 ground footprint and its support connections, and would suppression of those occupied panels meet PG9-Q27 after explicit owner adoption? The proposal is not asserted campaign geometry.",
            "Does the candidate center (20,10,8) remain a lawful perceived point with line of effect to A and the proposed panels under the shown open-courtyard geometry; is sqrt(274)=16.552945 the corrected secondary wall distance?",
            "Confirm the exact A refresh/cast candidate: case6.0/world6.1 after START, Action1 before commitment, payment21 RP to RP33, no transfer of Fortress-family discount, preserve prior END6.9, original field maximum deadline world66.1, and new Antimagic-family eligibility through next END case12.9/world13.0.",
            "Confirm the corrected Counterspell binding: Wizard20 access for A/B/D, Cleric20 for C; B/D cross-plane trigger/target eligibility not established and no reaction taken; A does not counter itself.",
            "Review the exact scoped field-termination proposal, which preserves the cast/effect identity and terminates it only after Q27 closes its containing space, without relocation, continuance, deadline extension, or refund. Is it technically coherent for separate owner adoption?",
            "Review A's candidate exterior anchor and item bounds in the separate proposal; do these bounds provide a defensible collision/support/custody check, or should any relative placement be changed?",
            "Confirm the corrected source/member bindings, valid empty-root JSON Pointers, and preservation of the base case bytes.",
        ],
        "noStateChange": "No cast, support-graph adoption, terminal rule adoption, integrated settlement, identity acceptance/application, fixture mutation, queue change, or hold/seal change is authorized or performed by this review packet.",
    }
    packet_raw = dump(OUT / PACKET_NAME, packet)

    manifest = load(PREV / "PG328-W08_PREBUILD_SOURCE_BINDINGS_385.json")
    manifest["id"] = "PG328-W08-PREBUILD-SOURCE-BINDINGS-386"
    manifest["createdAtUtc"] = now
    manifest["status"] = "HASH_VERIFIED_SOURCE_BUNDLE_WITH_UNADOPTED_TESTONLY_PROPOSALS"
    manifest["prebuildPath"] = PACKET_NAME
    manifest["prebuildSha256"] = sha(packet_raw)
    manifest["supersedesManifest"] = "PG328-W08-PREBUILD-SOURCE-BINDINGS-385"
    manifest["bundleMemberPath"] = "payload/" + PACKET_NAME
    for member in manifest.get("sourceMembers", []):
        if member.get("pointers") == ["/"]:
            member["pointers"] = [""]
    for name, rel, bundle, pointers in SOURCE_SPECS:
        manifest["sourceMembers"] = [m for m in manifest["sourceMembers"] if m["name"] != name]
        manifest["sourceMembers"].append(source_record(name, rel, bundle, pointers))
    manifest["reviewProposals"] = [
        {"name": "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_386_TESTONLY.json", "bundleMember": "payload/proposals/PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_386_TESTONLY.json", "sha256": sha(geom_raw), "bytes": len(geom_raw), "status": geometry_proposal["status"]},
        {"name": "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_386_TESTONLY.json", "bundleMember": "payload/proposals/PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_386_TESTONLY.json", "sha256": sha(carrier_raw), "bytes": len(carrier_raw), "status": carrier_proposal["status"]},
        {"name": "OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json", "bundleMember": "payload/proposals/OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json", "sha256": sha(terminal_raw), "bytes": len(terminal_raw), "status": terminal_proposal["status"]},
    ]
    manifest["nonAdoptionNotice"] = "All three new scenario inputs are review proposals only. None alters canonical rules, the inherited case, W01/W08 status, current holds/seals, or queue counts."
    manifest_raw = dump(OUT / MANIFEST_NAME, manifest)

    archive_rel = Path("conjure_demiplane_fortress_closure_intake_367/payload/authority/PG328_HELD_ARCHIVE.zip")
    archive_path = ROOT / archive_rel
    binding = manifest["caseMemberBinding"]
    with zipfile.ZipFile(archive_path, "r") as zf:
        case_raw = zf.read(binding["archiveMember"])
    if sha(case_raw) != binding["memberSha256"] or len(case_raw) != binding["memberBytes"]:
        raise RuntimeError("Inherited case bytes no longer match the 385 source binding")

    old_zip = PREV / "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_Prebuild385.zip"
    with zipfile.ZipFile(old_zip, "r") as zf:
        members = {name: zf.read(name) for name in zf.namelist() if not name.endswith("/")}
    members.pop("authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_385.json", None)
    members["payload/" + PACKET_NAME] = packet_raw
    members["authority/" + MANIFEST_NAME] = manifest_raw
    members["payload/cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json"] = case_raw
    members["payload/proposals/PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_386_TESTONLY.json"] = geom_raw
    members["payload/proposals/PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_386_TESTONLY.json"] = carrier_raw
    members["payload/proposals/OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json"] = terminal_raw
    for name, rel, bundle, _ in SOURCE_SPECS:
        members[bundle] = (ROOT / rel).read_bytes()
    zip_path = OUT / ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(members):
            zf.writestr(name, members[name])
    with zipfile.ZipFile(zip_path, "r") as zf:
        if len(zf.namelist()) != len(members):
            raise RuntimeError("ZIP member count mismatch")
        for name, raw in members.items():
            if sha(zf.read(name)) != sha(raw):
                raise RuntimeError(f"ZIP byte verification failed for {name}")
        repository = ROOT.parents[4]
        for source in manifest["sourceMembers"]:
            if source.get("pointers") == ["/"]:
                raise RuntimeError(f"Invalid slash-only JSON root pointer remains: {source['name']}")
            source_path = repository / source["repositoryPath"]
            source_bytes = source_path.read_bytes()
            if len(source_bytes) != source["bytes"] or sha(source_bytes) != source["sha256"]:
                raise RuntimeError(f"Repository source binding mismatch: {source['name']}")
            if sha(zf.read(source["bundleMember"])) != source["sha256"]:
                raise RuntimeError(f"Bundle source binding mismatch: {source['name']}")
    delivery = {
        "id": "DD-RANK9-PG328-W08-PREBUILD-386-DIRECTOR-REPAIR-DELIVERY",
        "createdAtUtc": now,
        "status": "READY_FOR_GPT_DIRECTOR_RESUBMISSION",
        "supersedes": "DD-RANK9-PG328-W08-PREBUILD-385-DELIVERY",
        "artifact": ZIP_NAME,
        "sha256": sha(zip_path.read_bytes()),
        "bytes": zip_path.stat().st_size,
        "bundleMemberCount": len(members),
        "prebuildPath": PACKET_NAME,
        "prebuildSha256": sha(packet_raw),
        "sourceBindingsPath": MANIFEST_NAME,
        "sourceBindingsSha256": sha(manifest_raw),
        "directorConversation": old_packet["scope"]["gptConversation"],
        "transmissionStatus": "NOT_YET_RESUBMITTED",
        "queueSnapshot": packet["scope"]["queueSnapshot"],
    }
    dump(OUT / DELIVERY_NAME, delivery)
    print(json.dumps({
        "out": str(OUT),
        "bundle": ZIP_NAME,
        "sha256": delivery["sha256"],
        "bytes": delivery["bytes"],
        "members": len(members),
        "prebuildSha256": manifest["prebuildSha256"],
        "caseSha256": sha(case_raw),
        "newProposalHashes": {p["name"]: p["sha256"] for p in manifest["reviewProposals"]},
    }, indent=2))


if __name__ == "__main__":
    main()
