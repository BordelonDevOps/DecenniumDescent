#!/usr/bin/env python3
"""Independently verify Shell B02 integrated preflight 477 Repack01."""
import hashlib
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
PKG = BASE / "elemental_shell_b02_integrated_preflight_477_repack01"
REPORT = PKG / "SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
ORIGINAL = BASE / "elemental_shell_b02_integrated_preflight_477" / "SHELL_B02_INTEGRATED_PREFLIGHT_477_TESTONLY.json"
READBACK = PKG / "DIRECTOR_READBACK_477_REPACK01.json"
CHECKS = []

EXPECTED = {
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_firepet_crossbind_466/SOURCE_CROSSBIND_PREFLIGHT_466.json": "a900ba265fc61b8d4be476963e9c0e2d1af9e08881af14d804d4c7543fb060ff",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_firepet_crossbind_466/DIRECTOR_READBACK_466.json": "546cff28ddef4e429a94bb1b8534cc33b47abfa72f5c394edc8617814282a3a3",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_firepet_crossbind_466/payload/sources/AC5_ACCEPTED_SOURCE_MODEL.json": "d782569ed8ef558f4edf54634e0d8c19926e24e2437528f1769b5ef3ce594898",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_firepet_crossbind_466/payload/sources/W11_SELECTION_EVIDENCE_433.json": "06cdf754284ba09bb02acbebfd9356af585ed5e700e31790031972f2f0e46bf4",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/CASTER_PREPARATION_PREMISE_468_TESTONLY.json": "0d66f106211fc705cfdc88d0916494511a30e91472aad36efbc05eafec73e05f",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json": "af80add79f0f91051f01b0befab2503c36e0cf4e3a7e3957a3fad2c6d0c1f3ab",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_qualification_472_repack01/SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json": "53caefc51346af50f224b415ed669f7814aca68738c8e2bb5f3d32963c51d679",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186/ACTOR_PROFILES.json": "05f523187a27ee8d46938b7db9e48ff930782533d2ae23e8da9f0b4ab65e686d",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/ELEMENTAL_SHELL_DIRECTOR_REQUIREMENTS_305.json": "ab1dc248a3dbae5a227b8755ed8f60668b4ea8eef97cb8505800553bba3852f9",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_476_REPACK01.json": "4ae9ed74080e2919e7223aeee54fe1d0a380b0117248648027a3f5dfbc95e9cb",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/wizard.json": "8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_witness365_w05_separation365_repack03_build01/packet/sources/MAGE_CLASS_PLAYTEST.json": "c64782e192e2e63e5abed5728f9213c9d4cf956bce1a75da7a156dbfd1141e0b",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_witness365_w05_separation365_repack03_build01/packet/W05_MAGE_PROFILES_365_TESTONLY.json": "c380750c54c7b2a4f729621fa26ad3b319708d218c4fd3497b1f23277e56433b",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_witness365_w05_separation365_repack03_build01/packet/sources/EQUIPMENT_SOURCE_CATALOG.json": "ff22f5974a1c95b4fb4e2a49b460726b956c093ce7990470c31eaa51238cf5c4",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/ELEMENTAL_SHELL_PROCEDURE_SOURCE.json": "31794a20cfb27e44cab1e2b8b65b79eb22a5b0a9745e378691b8cebbd2242f9f",
    "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md": "55f486de8d38a6734f8f0f2f62066401504f5b1311ebe66693175876b3f7aa6d",
    "DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(name, ok):
    CHECKS.append({"check": name, "passed": bool(ok)})
    if not ok:
        raise AssertionError(name)


def center(bounds):
    return [(lo + hi) / 2 for lo, hi in zip(bounds["x"], bounds["y"])]


def volume_distance(a, b):
    axis_gaps = [max(0, b[k][0] - a[k][1], a[k][0] - b[k][1]) for k in ("x", "y", "z")]
    return math.sqrt(sum(g * g for g in axis_gaps))


def volume_overlaps(a, b):
    return all(max(a[k][0], b[k][0]) < min(a[k][1], b[k][1]) for k in ("x", "y", "z"))


def main():
    report = json.loads(REPORT.read_text(encoding="utf-8-sig"))
    original = json.loads(ORIGINAL.read_text(encoding="utf-8-sig"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
    bindings = {x["path"]: x for x in report["sourceBindings"]}
    root = report["proposedOwnerPremises"]
    states = root["startingStates"]
    mage = states["Mage9-PROPOSED"]
    wizard = states["Wizard18"]
    geo = root["geometryFeet"]
    boxes = {name: actor["bounds"] for name, actor in geo.items() if isinstance(actor, dict) and "bounds" in actor}
    timeline = root["proposedTimelineSeconds"]
    bytime = {x["time"]: x["event"] for x in timeline}
    settlement = root["proposedRollsAndSettlement"]

    check("All 17 source path/hash/byte bindings match exact current source files", set(bindings) == set(EXPECTED) and all(bindings[p]["sha256"] == h and bindings[p]["bytes"] == len((REPO / p).read_bytes()) and digest((REPO / p).read_bytes()) == h for p, h in EXPECTED.items()))
    check("Director readback and original preflight are preserved and exactly bound", READBACK.exists() and json.loads(READBACK.read_text(encoding="utf-8-sig"))["reviewedPreflightSha256"] == digest(ORIGINAL.read_bytes()) == "529245d4a1fc28c7e83a9ba562eb76c8b91ddd5d7d864e1e156c38d88c9739d0" and report["priorDirectorReview"]["reviewedPreflightSha256"] == digest(ORIGINAL.read_bytes()) and report["priorDirectorReview"]["sha256"] == digest(READBACK.read_bytes()))
    check("Current Queue476 authority remains 831/17/0 and Shell is next", queue["currentAuthority"]["reviewedApplied"] == 831 and queue["currentAuthority"]["pending"] == 17 and queue["currentAuthority"]["acceptedUnapplied"] == 0 and queue["nextIdentity"] == "elemental-shell")
    check("Wizard first-family Dissonance correction and adopted force Ward/matrix state are preserved", wizard["dissonance"] == 0 and wizard["refrain"] == 0 and wizard["priorRankedCastFamilies"] == [] and wizard["ArcaneWard"]["type"] == "force" and wizard["matrixModifications"] == {} and facts_force_is_preserved(report))
    check("Mage static level-9 acquisition and full derived profile are source-bound without W11/W05 state transfer", mage["classLevel"] == 9 and mage["abilityScores"]["CON"] == 14 and mage["currentHP"] == mage["maximumHP"] == 80 and mage["currentAC"] == 15 and mage["maximumRP"] == 26 and mage["spellAttack"] == 8 and mage["spellDC"] == 16 and mage["currentRP"] == 26 and "no w11/w05 actor" in mage["spellAccess"].lower())
    check("Mage Fire focus is fresh and source-projected rather than copied from prior actor custody", mage["equipmentCustody"]["focusId"] == "R2-FIRE-FOCUS-001" and mage["focusAndHands"]["right"].startswith("Fresh branch-local R2-FIRE-FOCUS-001") and "W11/W05 object" in mage["focusAndHands"]["right"])
    check("Summon is a rank-5 source candidate only and Mage Counterspell is the selected level-9 card", report["sourceDerivedFacts"]["mage9"]["selectedSummon"]["operationalStatus"] == "blocked-pending-operational-review; source candidate only" and report["sourceDerivedFacts"]["mage9"]["selectedCounterspell"]["cardId"] == "mage.arch.counterspell")
    check("Mage spell DC16 is distinct from rank-specific Counterspell check DCs", mage["spellDC"] == 16 and report["sourceDerivedFacts"]["counterspellRules"]["mage"]["costRP"] == 4 and settlement["counterspellResponses"][1]["checkIfActivated"] == "INT+PB vs DC28 (10+2×rank9)")
    check("Cast costs/cadence commit before interruption and manifestation anchors remain separate", "concentration slot before interruption" in bytime[0.1] and "declines" in bytime[0.2] and "60.3" in bytime[0.3] and "first-family rule yields0 base Dissonance" in bytime[3.1] and "63.3" in bytime[3.3])
    check("All regular ENDs, cast-flag persistence, Dissonance vent and command bookkeeping are explicit", all(t in bytime for t in (0.9, 3.9, 6.9)) and "Dissonance remains1" in bytime[0.9] and "Dissonance1→0" in bytime[6.9] and "shared owner command budget" in bytime[6.1] and "offensive companion Action allowance" in bytime[7.0] and "clear the pending command" in bytime[7.0])
    check("Counterspell responses each name source/access, Reaction, RP, range, recharge and free decline; self eligibility is not decided", len(settlement["counterspellResponses"]) == 2 and all(x["decision"] == "DECLINED_ELIGIBLE_RESPONSE" and x["activated"] is False and x["rpAfter"] == x["currentRPBefore"] and x["reactionAfter"] == "available" and x["rechargeAfter"] == "ready; not triggered" and x["rollMade"] is False for x in settlement["counterspellResponses"]) and "unadjudicated" in settlement["selfCounterspellBoundary"])
    check("Branch-only occupied-bounds convention resolves the 57-ft eligibility while retaining 62-ft center distances", geo["rangeMeasurementConvention"].startswith("For this test-only branch only") and geo["mageToWizardNearestOccupiedBoundsDistance"] == 57 and geo["mageToWizardCenterDistance"] == 62 and geo["counterspellRangeFt"] == 60 and all(x["nearestBoundsDistanceFt"] == 57 and x["centerDistanceFt"] == 62 for x in settlement["counterspellResponses"]))
    check("Pet placement fixes the Mage-Wizard sightline, stays in-floor/supported and has no positive-volume actor overlap", geo["GreaterFirePet-R2-PROPOSED"]["bounds"]["y"] == [23, 28] and geo["GreaterFirePet-R2-PROPOSED"]["bounds"]["y"][1] <= geo["floor"]["bounds"]["y"][1] and not volume_overlaps(boxes["GreaterFirePet-R2-PROPOSED"], boxes["Wizard18"]) and geo["allRelevantLineOfEffect"]["MageToWizardAtShellCounterWindow"]["clear"] is True and "0.5-ft clear lateral gap" in geo["allRelevantLineOfEffect"]["MageToWizardAtShellCounterWindow"]["ray"])
    mage_wizard = volume_distance(boxes["Mage9-PROPOSED"], boxes["Wizard18"])
    mage_pet = volume_distance(boxes["Mage9-PROPOSED"], boxes["GreaterFirePet-R2-PROPOSED"])
    pet_wizard = volume_distance(boxes["GreaterFirePet-R2-PROPOSED"], boxes["Wizard18"])
    check("3D minimum occupied-body distances match the proposed range, command, attack and reflection predicates", mage_wizard == 57 and mage_pet <= 60 and pet_wizard == 0 and round(math.dist(geo["Mage9-PROPOSED"]["center"], geo["GreaterFirePet-R2-PROPOSED"]["center"]), 3) == geo["mageToPetCenterDistance"] and round(math.dist(geo["GreaterFirePet-R2-PROPOSED"]["center"], geo["Wizard18"]["center"]), 3) == geo["petToWizardCenterDistance"])
    check("Pet, Wizard and Mage lines of effect/perception each have explicit witnesses and governing obstruction rule", all(geo["allRelevantLineOfEffect"][key]["clear"] is True for key in ("MageToWizardAtSummonCounterWindow", "MageToWizardAtShellCounterWindow", "MageToPetAtSummonAndCommand", "PetToWizardAtStrikeAndReflection")) and "Total cover blocks direct targeting" in geo["allRelevantLineOfEffect"]["governingSource"])
    check("Fire Strike attack/damage, Shell checkpoint and floor(7/2) reflected damage remain exact", settlement["attack"]["total"] == 20 and settlement["damage"]["preDefenseTotal"] == 7 and settlement["shellCheckpoint"]["reflectedAmount"] == 3 and settlement["bearer"]["wizardHPAfter"] == 110 and settlement["reflection"]["petHPAfter"] == 57)
    check("Arcane Ward is preserved but inapplicable to fire; Pet receives the one reflection with a consumed stable key", "force-only and does not apply to this fire component" in settlement["defensesBeforeShell"] and settlement["reflection"]["recipient"].startswith("GreaterFirePet-R2-PROPOSED") and settlement["reflection"]["onceOnlyKeyConsumed"] is True and settlement["reflection"]["newRoot"] is True and settlement["reflection"]["recursion"] is False)
    check("Stable event/root IDs, before/after settlement, custody and future inverse replay contract are complete", len(set(settlement["eventAndRootIdentity"].values())) == 6 and set(settlement["resourceAndCustodyBeforeAfter"]) == {"Mage9-PROPOSED", "Wizard18", "GreaterFirePet-R2-PROPOSED"} and settlement["futureWitnessReplayContract"]["witnessConstructedNow"] is False and len(settlement["futureWitnessReplayContract"]["requiredBeforeAfterFields"]) >= 8 and "exact branch-start state" in settlement["futureWitnessReplayContract"]["inverseRequirement"])
    check("Every novel scene/resource/build/geometry/response/roll premise remains explicitly unadopted", report["proposedOwnerPremises"]["adopted"] is False and report["proposedOwnerPremises"]["requiresExactOwnerAdoptionBeforeWitness"] is True and len(report["ownerAdoptionRequiredPremises"]) == 7 and report["nonEffects"]["ownerAdoptionRecorded"] is False and report["nonEffects"]["branchPremisesAdopted"] is False)
    check("B01/B02 remain open, Shell held, and no encounter, witness, cast, seal, application or canon/queue change occurs", report["blockerDisposition"]["DF218-B01"].startswith("OPEN") and report["blockerDisposition"]["DF218-B02"].startswith("OPEN") and report["blockerDisposition"]["ElementalShellIdentity"] == "HELD" and report["blockerDisposition"]["castExecuted"] is False and report["blockerDisposition"]["encounterConstructed"] is False and report["blockerDisposition"]["witnessConstructed"] is False and report["blockerDisposition"]["sealIssued"] is False and report["blockerDisposition"]["identityAcceptedOrApplied"] is False and report["nonEffects"]["queueChanged"] is False and report["nonEffects"]["canonicalRuleChanged"] is False)

    result = {
        "id": "DF218-B02-INTEGRATED-PREFLIGHT-477-REPACK01-INDEPENDENT-VALIDATION",
        "status": "PASS",
        "checksPassed": len(CHECKS),
        "checksFailed": 0,
        "preflightSha256": digest(REPORT.read_bytes()),
        "preflightBytes": REPORT.stat().st_size,
        "originalReviewedPreflightSha256": digest(ORIGINAL.read_bytes()),
        "queueSha256": digest(QUEUE.read_bytes()),
        "sourceBindingCount": len(bindings),
        "authority": queue["currentAuthority"],
        "blockersRemainOpen": ["DF218-B01", "DF218-B02"],
        "witnessConstructed": False,
        "ownerAdoptionRecorded": False,
        "checks": CHECKS,
    }
    (PKG / "INDEPENDENT_VALIDATION_477_REPACK01.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def facts_force_is_preserved(report):
    return report["sourceDerivedFacts"]["wizard18"]["ArcaneWard"].get("matrixModifications") == {} and report["sourceDerivedFacts"]["wizard18"]["ArcaneWard"].get("fireComponentApplicability", "").startswith("Does not")


if __name__ == "__main__":
    main()
