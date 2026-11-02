#!/usr/bin/env python3
"""Build the Director-corrected, proposal-only Shell B02 preflight successor."""
import copy
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
SOURCE = BASE / "elemental_shell_b02_integrated_preflight_477" / "SHELL_B02_INTEGRATED_PREFLIGHT_477_TESTONLY.json"
PKG = BASE / "elemental_shell_b02_integrated_preflight_477_repack01"
OUTPUT = PKG / "SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json"

NEW_BINDINGS = [
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/wizard.json",
        "sha256": "8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b",
        "jsonPointers": ["/engine/11", "/cards/17"],
        "use": "Wizard first-prepared-family Dissonance exemption and automatic Wizard Counterspell card, including cost, Reaction, range, check and recharge.",
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_witness365_w05_separation365_repack03_build01/packet/sources/MAGE_CLASS_PLAYTEST.json",
        "sha256": "c64782e192e2e63e5abed5728f9213c9d4cf956bce1a75da7a156dbfd1141e0b",
        "jsonPointers": ["/engine/0", "/engine/19", "/cards/23"],
        "use": "Mage spell attack/DC derivation, class acquisition schedule and Mage Counterspell card cost, Reaction, range and recharge.",
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_firepet_crossbind_466/payload/sources/W11_SELECTION_EVIDENCE_433.json",
        "sha256": "06cdf754284ba09bb02acbebfd9356af585ed5e700e31790031972f2f0e46bf4",
        "jsonPointers": ["/ordinaryRankedSelections", "/cantripSelections", "/classCardSelections", "/classPathAndAutomaticGains"],
        "use": "Static Mage9 selection specification only: ten ranked selections, four cantrips, Counterspell at Mage9, Summon Greater Fire Pet selection, Arcanist path and automatic Fire Focus. No W11 actor/scene/custody transfers.",
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_witness365_w05_separation365_repack03_build01/packet/W05_MAGE_PROFILES_365_TESTONLY.json",
        "sha256": "c380750c54c7b2a4f729621fa26ad3b319708d218c4fd3497b1f23277e56433b",
        "jsonPointers": ["/profiles/0/abilityScores", "/profiles/0/derived", "/profiles/0/testOnlyVitals", "/profiles/0/focus"],
        "use": "Static Mage9 build/derived-stat evidence for ability scores, CON14, 80 HP, AC15, RP26, attack +8, save DC16 and a one-pound source-projected focus. Only derivation is reused; actor identity, prior state, item ID and custody are not.",
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_witness365_w05_separation365_repack03_build01/packet/sources/EQUIPMENT_SOURCE_CATALOG.json",
        "sha256": "ff22f5974a1c95b4fb4e2a49b460726b956c093ce7990470c31eaa51238cf5c4",
        "jsonPointers": ["/records/111"],
        "use": "Source-projected one-pound wand/focus fixture record only; proposed Mage9-R2 focus gets a fresh branch-local object ID and custody.",
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/ELEMENTAL_SHELL_PROCEDURE_SOURCE.json",
        "sha256": "31794a20cfb27e44cab1e2b8b65b79eb22a5b0a9745e378691b8cebbd2242f9f",
        "jsonPointers": ["/sharedRules/casting", "/sharedRules/cadence", "/sharedRules/clocks", "/sharedRules/geometry", "/selectedRules/1", "/selectedRules/2", "/selectedRules/3", "/selectedRules/4"],
        "use": "Operative retained Elemental Shell casting, Dissonance, deadlines, full 3D geometry/LoE and selected DF9-Q12 through Q15 procedures.",
    },
    {
        "path": "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
        "sha256": "55f486de8d38a6734f8f0f2f62066401504f5b1311ebe66693175876b3f7aa6d",
        "note": "Resolve a cast at the table, steps 1-7; pre-interruption cost/components/cadence commitment and Counterspell response requirements.",
        "use": "Direct operative casting/response order and costs. This manuscript binding does not claim runtime implementation.",
    },
    {
        "path": "DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md",
        "sha256": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81",
        "note": "Mage/Wizard spellcasting derivation and regular-turn Dissonance vent.",
        "use": "Direct operative class-stat and regular-turn cadence rules for the proposed branch.",
    },
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_binding(entry):
    raw = (REPO / entry["path"]).read_bytes()
    actual = sha(raw)
    if actual != entry["sha256"]:
        raise SystemExit(f"Source changed: {entry['path']} expected {entry['sha256']} got {actual}")
    binding = {"path": entry["path"], "bytes": len(raw), "sha256": actual}
    if "jsonPointers" in entry:
        binding["jsonPointers"] = entry["jsonPointers"]
    if "note" in entry:
        binding["note"] = entry["note"]
    binding["use"] = entry["use"]
    return binding


def main():
    PKG.mkdir(parents=True, exist_ok=True)
    report = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    report["id"] = "DF218-B02-INTEGRATED-ENCOUNTER-PREFLIGHT-477-REPACK01"
    report["status"] = "CORRECTED_READY_FOR_DIRECTOR_ADOPTION_READINESS_REVIEW"
    report["classification"] = "PROPOSAL_ONLY_TEST_ONLY_PREMISES_NOT_ADOPTED_NOT_A_WITNESS"
    report["priorDirectorReview"] = {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01.json",
        "sha256": sha((PKG / "DIRECTOR_READBACK_477_REPACK01.json").read_bytes()),
        "reviewedPreflightSha256": "529245d4a1fc28c7e83a9ba562eb76c8b91ddd5d7d864e1e156c38d88c9739d0",
        "status": "NOT_READY_FOR_OWNER_ADOPTION",
        "correctionsAddressed": ["477-C01", "477-C02", "477-C03", "477-C04", "477-C05", "477-C06", "477-C07"],
    }

    existing = {item["path"]: item for item in report["sourceBindings"]}
    for item in NEW_BINDINGS:
        binding = source_binding(item)
        if item["path"] in existing:
            existing[item["path"]].update(binding)
        else:
            report["sourceBindings"].append(binding)

    facts = report["sourceDerivedFacts"]
    facts["wizard18"]["ArcaneWard"] = {
        "type": "force",
        "basis": "Exact adopted Proposal468 fallback; no prepared Divination spell deals damage.",
        "matrixModifications": {},
        "fireComponentApplicability": "Does not reduce or alter this proposed fire component.",
    }
    facts["elementalShell"]["durationBasis"] = "Bound Elemental Shell procedure source: nonconcentration 60 elapsed seconds from manifestation; proposal branch use only."
    facts["mage9"] = {
        "sourceProfile": "W05_MAGE_PROFILES_365_TESTONLY.json#/profiles/0, used only as static build/derivation evidence; no W05 or W11 actor state or item custody transfers.",
        "classLevel": 9,
        "classPathHistory": [{"level": 3, "path": "Arcanist"}],
        "abilityScores": {"STR": 10, "DEX": 14, "CON": 14, "INT": 18, "WIS": 12, "CHA": 10},
        "proficiencyBonus": 4,
        "intelligenceModifier": 4,
        "maximumHP": 80,
        "maximumRP": 26,
        "spellAttack": 8,
        "spellDC": 16,
        "ordinaryRankedSelections": 10,
        "cantrips": 4,
        "selectedSummon": {"spellId": "summon-greater-fire-pet", "selectedAtMageLevel": 9, "rank": 5, "sourcePointer": "W11_SELECTION_EVIDENCE_433.json#/ordinaryRankedSelections/9", "operationalStatus": "blocked-pending-operational-review; source candidate only"},
        "selectedCounterspell": {"cardId": "mage.arch.counterspell", "selectedAtMageLevel": 9, "sourcePointer": "W11_SELECTION_EVIDENCE_433.json#/classCardSelections/13", "costRP": 4, "activation": "Reaction", "rangeFeet": 60, "rechargeRounds": 3},
        "automaticFireFocus": {"gainedAtMageLevel": 2, "sourcePointer": "W11_SELECTION_EVIDENCE_433.json#/classPathAndAutomaticGains"},
        "testOnlyBuildBoundary": "Static selection/build evidence does not transfer W11/W05 actor IDs, current state, scene, inventory identity, custody or campaign history.",
    }
    facts["counterspellRules"] = {
        "wizard": {"cardId": "wizard.base.counterspell", "sourcePointer": "wizard.json#/cards/17", "acquisition": "Automatic at Wizard2", "costRP": 3, "activation": "Reaction", "rangeFeet": 60, "rechargeRounds": 2, "check": "INT + PB vs DC 10 + 2 × triggering spell rank"},
        "mage": {"cardId": "mage.arch.counterspell", "sourcePointer": "MAGE_CLASS_PLAYTEST.json#/cards/23", "acquisition": "Selected at Mage9 in selection433", "costRP": 4, "activation": "Reaction", "rangeFeet": 60, "rechargeRounds": 3, "check": "INT + PB vs DC 10 + 2 × triggering spell rank"},
        "responseConvention": "The test branch measures range by the minimum 3D Euclidean distance between occupied body bounds. This is a proposed branch-only premise, not a global rule amendment.",
    }

    premises = report["proposedOwnerPremises"]
    premises["scenario"]["relationship"] = "Wizard18 is a willing self-bearer in a consensual sparring fixture. Mage9-PROPOSED does not regard Wizard18 as hostile for aura qualification; the commanded Fire Strike is a controlled test attack."
    wizard = premises["startingStates"]["Wizard18"]
    wizard["woundsConditionsAndOtherDefenses"] = "No defense applies to this proposed fire component other than Shell's own selected-fire immunity/reflection stage. The exact adopted force ArcaneWard and empty matrixModifications are preserved; ArcaneWard does not apply to fire. No other resistance, immunity, flat reduction, transfer or Null Veil is active."
    wizard["postShellDissonance"] = 0
    wizard["postShellRefrain"] = 0
    wizard["ArcaneWard"] = copy.deepcopy(facts["wizard18"]["ArcaneWard"])
    wizard["matrixModifications"] = {}
    mage = premises["startingStates"]["Mage9-PROPOSED"]
    mage.update({
        "classPathHistory": [{"level": 3, "path": "Arcanist"}],
        "abilityScores": copy.deepcopy(facts["mage9"]["abilityScores"]),
        "PB": 4,
        "INTModifier": 4,
        "spellAttack": 8,
        "spellDC": 16,
        "currentHP": 80,
        "maximumHP": 80,
        "currentAC": 15,
        "currentRP": 26,
        "maximumRP": 26,
        "dissonanceLimit": 10,
        "spellAccess": "Exact static Mage9 selection/build specification is bound to W11_SELECTION_EVIDENCE_433 plus W05_MAGE_PROFILES_365_TESTONLY#/profiles/0. This new actor independently adopts the branch-local proposed build: rank-5 Summon Greater Fire Pet selected at Mage9 (still operationally held), four cantrips, ten ordinary ranked selections, Counterspell class card selected at Mage9, Arcanist at level3, Fire Elemental Focus automatically gained at level2, INT18/PB4/CON14 and profile-derived 80 HP/AC15/RP26/spell attack+8/DC16. No W11/W05 actor, state, scene, item ID or campaign history transfers.",
        "focusAndHands": {"right": "Fresh branch-local R2-FIRE-FOCUS-001 (source-projected 1 lb wand focus; no W11/W05 object or custody transferred)", "left": "Free for somatic component"},
        "voice": "audible",
        "equipmentCustody": {"focusId": "R2-FIRE-FOCUS-001", "custodian": "Mage9-PROPOSED", "otherCarriedItems": []},
        "counterspellSelectionAndState": "mage.arch.counterspell selected at Mage9; available at both relevant external windows; no previous use or recharge clock.",
    })
    mage["perceptionAndControl"] = "Conscious and perceives the new Pet within 60 feet by the proposed occupied-bounds range convention with a recorded clear line of effect; after the Pet is placed, perceives Wizard18's Shell casting along the recorded clear witness path. Issues exactly one proposed command."
    mage["status"] = "NEW_TEST_ONLY_PREMISE_REQUIRES_OWNER_ADOPTION"
    pet = premises["startingStates"]["GreaterFirePet-R2-PROPOSED"]
    pet["sourceProfile"] = "AC5_ACCEPTED_SOURCE_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01"
    pet["sizeAndWeight"] = {"size": "Medium", "weightLb": 100}
    pet["proposedBodyHeightFt"] = 6
    pet["relationToWizard"] = "Mage9-PROPOSED does not regard the consenting Wizard18 as hostile; no aura attempt is eligible."

    geom = premises["geometryFeet"]
    geom["rangeMeasurementConvention"] = "For this test-only branch only, range is the minimum 3D Euclidean separation between occupied body bounds; center distances are also recorded. This is a proposed owner premise and does not amend global rules."
    geom["GreaterFirePet-R2-PROPOSED"]["bounds"]["y"] = [23, 28]
    geom["GreaterFirePet-R2-PROPOSED"]["center"] = [27.5, 25.5, 3]
    geom["mageToPetCenterDistance"] = 57.079
    geom["mageToWizardCenterDistance"] = 62
    geom["mageToWizardNearestOccupiedBoundsDistance"] = 57
    geom["petToWizardCenterDistance"] = 5.831
    geom["petToWizardNearestOccupiedBoundsDistance"] = 0
    geom["fireStrikeReachFt"] = 5
    geom["bearerToPetSurfaceGap"] = 0
    geom["counterspellRangeFt"] = 60
    geom["allRelevantLineOfEffect"] = {
        "governingSource": "ELEMENTAL_SHELL_PROCEDURE_SOURCE.json#/sharedRules/geometry; SPELL_INTEGRATION_RULES.md, Resolve a cast at the table, step1. Total cover blocks direct targeting; every relevant body and path is recorded below.",
        "MageToWizardAtSummonCounterWindow": {"time": 0.2, "clear": True, "interveningBodies": [], "reason": "Pet does not exist until0.3; open plane, no wall/field/item."},
        "MageToWizardAtShellCounterWindow": {"time": 3.2, "clear": True, "interveningBodies": [], "ray": "Centerline at y=22.5,z=3.0; Pet occupies y=23..28, leaving a0.5-ft clear lateral gap. The old y20..25 Pet box would have intersected this line and is corrected here."},
        "MageToPetAtSummonAndCommand": {"times": [0.3, 6.1], "clear": True, "interveningBodies": [], "reason": "Open supported plane; Mage perceives the occupied Pet bounds."},
        "PetToWizardAtStrikeAndReflection": {"times": [7.0], "clear": True, "interveningBodies": [], "reason": "The two body bounds touch at x=30 with overlapping y intervals; the exact path has no third body, wall, field or item."},
        "WizardSelfShellTarget": {"time": 3.1, "clear": True, "reason": "Self-target at distance0; no external line is required."},
        "obstructionFinding": "Pet presence is stated rather than erased. Its corrected box does not intersect the Wizard–Mage counterspell sightline; no total-cover conclusion is inferred from a body centerline.",
    }
    geom["arenaSupportAndCollision"] = "New supported floor fixture; no positive-volume overlap. Pet footprint is supported and unoccupied at creation; Pet and Wizard touch at the x=30 boundary only."
    geom["counterspellEligibility"] = "At0.2 Wizard18 is57 feet from Mage9-PROPOSED by the proposed occupied-bounds convention and can perceive the casting before Pet creation; automatic Wizard Counterspell is an eligible response and is declined. At3.2 Mage9-PROPOSED is57 feet from Wizard18 under the same convention with the clear recorded sightline; selected Mage Counterspell is an eligible response and is declined. Centers are62 feet apart; no center-only exclusion is claimed. Self-counterspell eligibility for either caster is not adjudicated; neither attempts it."
    geom["status"] = "NEW_TEST_ONLY_GEOMETRY_REQUIRES_OWNER_ADOPTION"

    premises["proposedTimelineSeconds"] = [
        {"time": 0.0, "event": "Mage9-PROPOSED regular START; reset turn cast flag; Action/Bonus Action/Reaction, shared command and offense budgets are available."},
        {"time": 0.1, "event": "Commit rank-5 Summon Greater Fire Pet: pay10 RP (26→16), commit Action and V/S/F with fresh right-hand Fire focus and free left somatic hand; Dissonance0→1, record spell/cast-family flag and commit the concentration slot before interruption. No other concentration is active."},
        {"time": 0.2, "event": "Wizard18's eligible automatic Counterspell window: source is wizard.base.counterspell (automatic at Wizard2; Reaction;3 RP;60 ft; recharge2 rounds). Wizard perceives Mage at57 ft by the proposed occupied-bounds convention and declines. No Counterspell activation, roll, RP, Reaction, components or recharge is consumed; Wizard remains at68 RP with Reaction and card ready. Mage self-counter eligibility is not adjudicated; no self-attempt is made."},
        {"time": 0.3, "event": "Summon resolves successfully; create the new Pet in the exact supported footprint. On successful manifestation, Mage concentration and the Pet duration anchor to60 elapsed seconds (deadline60.3). Mage's action/cast commitment remains spent."},
        {"time": 0.9, "event": "Mage END: preserve the cast flag through END; this turn included a spell, so Dissonance remains1. Reset the cast flag only at the next regular START."},
        {"time": 0.91, "event": "First Pet attached phase after Mage's whole turn: no command is pending, so Pet takes defensive Dodge only; no movement/attack/offense budget is spent and no hostile-aura attempt occurs."},
        {"time": 3.0, "event": "Wizard18 regular START; reset turn cast flag and refresh normal budgets. No other turn or clock is inserted."},
        {"time": 3.1, "event": "Commit rank-9 Elemental Shell on consenting self, select fire, pay26 RP (68→42), commit Action and V/S/F using left-hand focus with right hand free, record cast flag and first prepared-family history before interruption. The exact adopted Wizard first-family rule yields0 base Dissonance; Refrain stays0."},
        {"time": 3.2, "event": "Mage9-PROPOSED's eligible selected mage.arch.counterspell window (Mage9 selection433; Reaction;4 RP;60 ft; recharge3 rounds). Mage perceives Wizard on the clear recorded ray at57 ft under the proposed occupied-bounds convention and declines. No Counterspell activation, roll, RP, Reaction, components or recharge is consumed; Mage remains at16 RP with Reaction and card ready. Wizard self-counter eligibility is not adjudicated; no self-attempt is made."},
        {"time": 3.3, "event": "Shell manifests successfully; selected-fire Shell deadline is63.3 (60 seconds from manifestation). Retain Wizard ArcaneWard type=force and matrixModifications={} unchanged; Wizard Dissonance/Refrain remain0."},
        {"time": 3.9, "event": "Wizard18 END: preserve the cast flag through END; Wizard Dissonance/Refrain remain0. The flag resets at its next regular START, outside this bounded interval."},
        {"time": 6.0, "event": "Mage9-PROPOSED next regular START; reset cast flag and refresh Action/Bonus Action normally. Dissonance remains1 pending this turn's exact END; Reaction remains available."},
        {"time": 6.1, "event": "Mage pays Bonus Action and consumes the one shared owner command budget for this numbered round; register one pending Fire Strike execution command for the attached Pet phase. This command is not a spell or magical class ability and is not a cast."},
        {"time": 6.9, "event": "Mage9-PROPOSED END with no spell or magical class ability this regular turn; vent Dissonance1→0. Preserve the turn cast flag through END; clear it at the next regular START. Pending Pet command remains for the attached phase."},
        {"time": 7.0, "event": "Pet attached phase executes exactly one commanded Fire Strike; consume the one offensive companion Action allowance, clear the pending command and retain its execution receipt. No aura tick or other attack occurs; resolve attack and one once-only Shell reflection."},
    ]

    settlement = premises["proposedRollsAndSettlement"]
    settlement["counterspellResponses"] = [
        {"time": 0.2, "responder": "Wizard18", "source": "wizard.base.counterspell", "sourceBinding": "wizard.json#/cards/17", "rankAndAccess": "Automatic at Wizard2; no preparation requirement", "reactionAvailable": True, "currentRPBefore": 68, "costIfActivatedRP": 3, "rangeFt": 60, "nearestBoundsDistanceFt": 57, "centerDistanceFt": 62, "rechargeIfActivatedRounds": 2, "checkIfActivated": "INT+PB vs DC20 (10+2×rank5)", "components": "No activation, component performance or component/material consumption on decline.", "decision": "DECLINED_ELIGIBLE_RESPONSE", "activated": False, "rpAfter": 68, "reactionAfter": "available", "rechargeAfter": "ready; not triggered", "rollMade": False},
        {"time": 3.2, "responder": "Mage9-PROPOSED", "source": "mage.arch.counterspell", "sourceBinding": "MAGE_CLASS_PLAYTEST.json#/cards/23 and W11_SELECTION_EVIDENCE_433.json#/classCardSelections/13", "rankAndAccess": "Selected Mage9 class card", "reactionAvailable": True, "currentRPBefore": 16, "costIfActivatedRP": 4, "rangeFt": 60, "nearestBoundsDistanceFt": 57, "centerDistanceFt": 62, "rechargeIfActivatedRounds": 3, "checkIfActivated": "INT+PB vs DC28 (10+2×rank9)", "components": "No activation, component performance or component/material consumption on decline.", "decision": "DECLINED_ELIGIBLE_RESPONSE", "activated": False, "rpAfter": 16, "reactionAfter": "available", "rechargeAfter": "ready; not triggered", "rollMade": False},
    ]
    settlement["selfCounterspellBoundary"] = "Caster self-counterspell eligibility is deliberately unadjudicated. Neither caster attempts a self-counter; no categorical eligibility ruling is made."
    settlement["optionalAttackAndDamageReactions"] = "Any optional attack/damage reaction prompt in this bounded fixture is explicitly declined; no Reaction, RP, component, charge, recharge, or effect is spent."
    settlement["eventAndRootIdentity"] = {
        "summonCastId": "CAST-DF218-SHELL-B02-R2-SUMMON-001",
        "shellCastId": "CAST-DF218-SHELL-B02-R2-SHELL-001",
        "fireStrikeEventId": "ATTACK-DF218-SHELL-B02-R2-FIRESTRIKE-001",
        "originalDamageRootId": "ROOT-DF218-SHELL-B02-R2-FIRESTRIKE-001",
        "reflectedDamageRootId": "ROOT-DF218-SHELL-B02-R2-SHELL-REFLECTION-001",
        "onceOnlyConsumedReflectionKey": "REFLECT-DF218-SHELL-B02-R2-FIRESTRIKE-001-SELECTED-FIRE",
    }
    settlement["reflection"].update({
        "distanceFeet": 0,
        "distanceConvention": "minimum separation between occupied body bounds; center distance 5.831 ft",
        "sourceRoot": "ROOT-DF218-SHELL-B02-R2-FIRESTRIKE-001",
        "reflectedRootId": "ROOT-DF218-SHELL-B02-R2-SHELL-REFLECTION-001",
        "onceOnlyKey": "REFLECT-DF218-SHELL-B02-R2-FIRESTRIKE-001-SELECTED-FIRE",
        "onceOnlyKeyConsumed": True,
        "dealer": "Wizard18 (Shell bearer), as required for the new reflected damage root",
        "nullFlagAtCreation": False,
    })
    settlement["defensesBeforeShell"] = "No save scaling, flat reduction, independent fire resistance/immunity or transfer applies. Preserved ArcaneWard is force-only and does not apply to this fire component; no Null Veil is active. These remain proposed fixture facts."
    settlement["resourceAndCustodyBeforeAfter"] = {
        "Mage9-PROPOSED": {"HP": "80→80", "RP": "26→16", "Dissonance": "0→1→0", "Refrain": "0→0", "action": "spent on summon", "bonusAction": "spent on one shared command at6.1", "reaction": "remains available; both counterspell windows declined", "concentration": "null→Summon Greater Fire Pet, deadline60.3", "focusCustody": "R2-FIRE-FOCUS-001 remains in Mage's right hand", "otherInventory": "none"},
        "Wizard18": {"HP": "110→110", "RP": "68→42", "Dissonance": "0→0", "Refrain": "0→0", "action": "spent on Shell", "reaction": "remains available; Counterspell window at0.2 declined", "concentration": "none", "ArcaneWard": "force type preserved; matrixModifications remains{}", "focusCustody": "adopted Wizard focus remains in left hand", "otherInventory": "unchanged"},
        "GreaterFirePet-R2-PROPOSED": {"HP": "nonexistent→60→57", "position": "uncreated→[27.5,25.5,3]", "deadline": "not present→60.3", "commandBudget": "none→one pending command→executed once", "attackAllowance": "available→spent once", "inventory": "none throughout", "custody": "no carried objects"},
    }
    settlement["futureWitnessReplayContract"] = {
        "witnessConstructedNow": False,
        "requiredBeforeAfterFields": ["all three actor identities and full HP/RP/AC/abilities/conditions", "Action/Bonus Action/Reaction and cast flags", "Dissonance/Refrain/last-spell and prepared-family histories", "concentration slots/deadlines and Shell/Pet source IDs", "positions/body bounds/support/LoE/consent/relationship", "focus/item IDs and custody", "command/offense budgets and pending/executed command receipts", "damage packet/root/parent-root/Null provenance/once-only reflection key", "HP and lifecycle changes"],
        "inverseRequirement": "Any later witness must record complete pre/post state for every event and inverse operations that restore the exact branch-start state, remove the hypothetical Pet/Shell sources, restore all budgets/resources/custody/roots/deadlines, and leave the independent campaign/native state untouched.",
    }

    report["ownerAdoptionRequiredPremises"] = [
        "A new isolated hypothetical plane, three new branch-local actor/body identities, full occupied bounds and exact coordinates; the branch-only nearest-occupied-bounds range metric; support, collision and every listed perception/LoE ray. Pet/Wizard contact at x=30 is boundary-only with no positive-volume overlap.",
        "Wizard18's proposed current HP/RP/AC, concentration, Dissonance/Refrain/cast history, force-only ArcaneWard and empty matrix modifications, defenses/Null state, self-consent, voice, focus and hands. Proposal468 supplies only the adopted caster preparation and its exact preserved Ward/matrix premise.",
        "A fresh Mage9 actor with the exact static acquisition/build specification from selection433 and W05 Mage profile: ability scores including CON14; profile-derived 80 HP, AC15, RP26, spell attack+8 and spell DC16; ten ranked selections/four cantrips; level-9 Summon and Counterspell selections; Arcanist path and automatic Fire Focus. Use a new one-pound focus object and custody; do not transfer W05/W11 actor IDs, current state, item IDs, scene or history.",
        "A new Greater Fire Pet using the bound AC5 branch profile: Medium elemental, 100 lb, HP60, AC17, 5-ft Fire Strike and passive aura limits; exact branch body bounds/position, nonhostile relation, no resistance/immunity/Null, no prior command/attack history, no carried items, creation/deadline and attached phase.",
        "Exact summon/Shell commitments, actions, V/S/F, RP, concentration/cast-history timing, interruption windows, manifestation times/deadlines, END processing and no-refund behavior. Wizard's eligible Counterspell decline and Mage's eligible Counterspell decline with their exact source/access, Reaction/RP/range/recharge, clear sightline, no activation/cost/component use; self-counter eligibility remains unadjudicated.",
        "The consenting controlled sparring relationship, no aura hostility, no unrelated attacks, optional attack/damage reactions declined, attack/damage dice, AC12, absence of other fire defenses, Shell checkpoint, stable root IDs, once-only reflection key, Null state, lifecycle and exact before/after settlement.",
        "No first-use, resource, actor, item, event, roll or scene fact is imported from W11, W13, Proposal448, the campaign or another spell branch; no campaign event is asserted.",
    ]
    report["blockerDisposition"]["DF218-B02"] = "OPEN_PENDING_DIRECTOR_ADOPTION_READINESS_REVIEW_AND_EXACT_OWNER_ADOPTION_OF_ANY_PROPOSED_FIXTURE_PREMISES"
    report["nonEffects"]["ownerAdoptionRecorded"] = False
    report["nonEffects"]["branchPremisesAdopted"] = False
    report["directorRequest"] = "Review this corrected proposal-only successor against the exact seven 477 corrections, the new direct operative bindings and the prior approved crossbind466/qualification472 limits. Confirm exact source bindings, state/cadence/END/counterspell/geometry/LoE/command/root/settlement checks; identify any remaining exact corrections or missing bindings; state whether this exact successor is ready to present for owner adoption and list precisely what adoption would cover. Do not treat any premise as adopted, authorize cast/encounter/witness/seal, close B01/B02, accept/apply Elemental Shell, or change canon/queue."

    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(OUTPUT), "sha256": sha(OUTPUT.read_bytes()), "bytes": OUTPUT.stat().st_size, "bindings": len(report["sourceBindings"])}, indent=2))


if __name__ == "__main__":
    main()
