#!/usr/bin/env python3
"""Verify the source bindings and non-authorizing boundary of Shell B02 preflight 477."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PKG = BASE / "elemental_shell_b02_integrated_preflight_477"
REPORT = PKG / "SHELL_B02_INTEGRATED_PREFLIGHT_477_TESTONLY.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
CHECKS = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, ok):
    CHECKS.append({"check": name, "passed": bool(ok)})
    if not ok:
        raise AssertionError(name)


def main():
    report = json.loads(REPORT.read_text(encoding="utf-8-sig"))
    root = BASE.parents[4]
    expected = {
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
    }
    actual = {x["path"]: x["sha256"] for x in report["sourceBindings"]}
    check("All ten source paths and SHA-256 bindings match exact current bytes", actual == expected and all(sha(root / path) == expected[path] for path in expected))
    queue = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
    check("Current authority remains 831/17/0 and Shell remains next", queue["currentAuthority"]["reviewedApplied"] == 831 and queue["currentAuthority"]["pending"] == 17 and queue["currentAuthority"]["acceptedUnapplied"] == 0 and queue["nextIdentity"] == "elemental-shell")
    check("Caster subpart is bounded to adopted Proposal468", report["sourceDerivedFacts"]["wizard18"]["sourceSupportedAcquisitionAndPreparation"] is True and actual["docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json"] == "af80add79f0f91051f01b0befab2503c36e0cf4e3a7e3957a3fad2c6d0c1f3ab")
    check("Proposed attack and reflected component arithmetic is exact", report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["attack"]["total"] == 20 and report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["damage"]["preDefenseTotal"] == 7 and report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["reflection"]["petDamage"] == 3 and report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["reflection"]["petHPAfter"] == 57)
    check("Pet is the reflected recipient, not Mage controller", report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["reflection"]["recipient"].startswith("GreaterFirePet-R2-PROPOSED"))
    check("Pet/caster and Shell deadlines are separate and unexpired at attack", report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["petDeadline"] == 60.3 and report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["bearer"]["shellDeadline"] == 63.3 and report["proposedOwnerPremises"]["proposedRollsAndSettlement"]["terminalTime"] == 7.0)
    geom = report["proposedOwnerPremises"]["geometryFeet"]
    check("Proposed geometry satisfies summon/command range while excluding Counterspell range", geom["mageToPetCenterDistance"] == 57 and geom["mageToWizardCenterDistance"] == 62 and geom["counterspellRangeFt"] == 60)
    check("W11, W13 and campaign state are not imported", report["scope"]["w11SceneOrOutcomesTransferred"] is False and report["scope"]["noParentStateImported"] is True and report["nonEffects"]["campaignEventClaim"] is False)
    check("Every newly proposed actor/geometry premise requires owner adoption", report["proposedOwnerPremises"]["adopted"] is False and report["proposedOwnerPremises"]["requiresExactOwnerAdoptionBeforeWitness"] is True and len(report["ownerAdoptionRequiredPremises"]) >= 6)
    check("B01 stays separate and both blockers remain open", report["blockerDisposition"]["DF218-B01"].startswith("OPEN") and report["blockerDisposition"]["DF218-B02"].startswith("OPEN") and report["scope"]["B01Addressed"] is False)
    check("No cast, encounter, witness, seal, acceptance/application or queue/canon change", report["blockerDisposition"]["castExecuted"] is False and report["blockerDisposition"]["encounterConstructed"] is False and report["blockerDisposition"]["witnessConstructed"] is False and report["blockerDisposition"]["sealIssued"] is False and report["blockerDisposition"]["blockerClosed"] is False and report["blockerDisposition"]["identityAcceptedOrApplied"] is False and report["nonEffects"]["canonicalRuleChanged"] is False and report["nonEffects"]["queueChanged"] is False)
    result = {"id": "DF218-B02-INTEGRATED-PREFLIGHT-477-INDEPENDENT-VALIDATION", "status": "PASS", "checksPassed": len(CHECKS), "checksFailed": 0,
              "preflightSha256": sha(REPORT), "queueSha256": sha(QUEUE), "authority": queue["currentAuthority"],
              "blockersRemainOpen": ["DF218-B01", "DF218-B02"], "witnessConstructed": False, "checks": CHECKS}
    (PKG / "INDEPENDENT_VALIDATION_477.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
