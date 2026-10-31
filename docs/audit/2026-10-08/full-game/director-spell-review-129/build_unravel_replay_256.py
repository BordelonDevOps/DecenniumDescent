import copy
from datetime import datetime, timezone
import hashlib
import json
import pathlib
import zlib

W = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
B = W / "docs/audit/2026-10-08/full-game/director-spell-review-129"
P = B / "UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256.json"
OUT = B / "UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256.json"
plan = json.loads(P.read_text(encoding="utf-8"))


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def actor_base():
    return {
        "actor": "MD196-TARGET-HUMAN-DRUID15-MAGE5",
        "characterLevel": 20,
        "classes": {"Druid": 15, "Mage": 5},
        "HP": {"current": 138, "max": 138},
        "sharedRP": {"current": 46, "max": 46},
        "dissonance": {"current": 0, "limit": 12},
        "refrain": {"repeatCount": 0, "lastSpell": None},
        "nukeChain": [],
        "classAvailability": {"Druid": True, "Mage": True},
        "classDerivedProficiencyAvailable": True,
        "objectiveIdentity": "unchanged",
        "subjectiveBelief": None,
        "form": None,
        "rootAnatomy": True,
        "AC": 12,
        "formTempHP": 0,
        "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "active"}],
        "concentration": None,
        "shiftUses": {"current": 6, "max": 6},
        "bufferReserve": {"current": 35, "max": 35},
        "formSurge": {"current": 6, "max": 6},
        "elementalShapeshiftingUses": {"current": 2, "max": 2},
        "conjureFamiliarUse": "ready",
        "familiar": None,
        "familiarCommandAvailable": True,
        "equipment": {
            "woodenDruidicFocusStaff": "owned; held right hand",
            "commonClothes": "owned; worn",
            "coin": "74gp 5sp",
        },
        "ordinaryTurnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"},
        "currentTargetTurn": "initial post-long-rest fixture; T1 starts10:00:00Z",
        "positionFt": [0, 0, 0],
        "formSourceCounters": {},
    }


base = actor_base()  # fully bound post-rest static fixture; no rest event is claimed
fam = copy.deepcopy(base)
fam.update({
    "sharedRP": {"current": 42, "max": 46},
    "dissonance": {"current": 1, "limit": 12},
    "refrain": {"repeatCount": 0, "lastSpell": "mage.arch.conjure-elemental-familiar"},
    "conjureFamiliarUse": "spent",
    "familiar": {
        "id": "FAM-FIRE-01", "source": "mage.arch.conjure-elemental-familiar", "identity": "Fire",
        "HP": {"current": 14, "max": 14}, "AC": 18, "speed": 30, "fireResistance": True,
        "created": "2026-10-30T10:00:01Z", "deadline": "2026-10-30T10:10:01Z",
        "pendingOrder": None, "mode": "defensive; no command yet", "positionFt": [5, 0, 0],
    },
    "ordinaryTurnBudgets": {"Action": "spent: Conjure Elemental Familiar", "BonusAction": "ready", "Reaction": "ready"},
    "currentTargetTurn": "T1 starts10:00:00Z; familiar Action10:00:01Z; T1 END10:00:06Z",
})
vent = copy.deepcopy(fam)
vent["dissonance"]["current"] = 0
vent["refrain"] = {"repeatCount": 0, "lastSpell": "mage.arch.conjure-elemental-familiar"}
vent["ordinaryTurnBudgets"] = {"Action": "spent: Dodge", "BonusAction": "ready", "Reaction": "available then turn ended"}
vent["currentTargetTurn"] = "T2 starts10:00:06Z; Dodge10:00:09Z; Let the Note Fall at END10:00:12Z"

dm = copy.deepcopy(vent)
dm.update({
    "sharedRP": {"current": 41, "max": 46},
    "dissonance": {"current": 1, "limit": 12},
    "refrain": {"repeatCount": 0, "lastSpell": "mage.base.detect-magic"},
    "concentration": {"id": "DM-01", "source": "mage.base.detect-magic", "started": "2026-10-30T10:00:13Z", "deadline": "2026-10-30T10:10:13Z", "active": True},
    "ordinaryTurnBudgets": {"Action": "spent: Mage Detect Magic", "BonusAction": "ready", "Reaction": "ready"},
    "currentTargetTurn": "T3 starts10:00:12Z; Mage Detect Magic Action10:00:13Z; T3 END10:00:18Z",
})

form = copy.deepcopy(dm)
form.update({
    "sharedRP": {"current": 41, "max": 46},
    "dissonance": {"current": 1, "limit": 12},
    "refrain": {"repeatCount": 0, "lastSpell": None},
    "nukeChain": [],
    "form": {
        "id": "FORM-EW-01", "source": "druid.arch.earth-warden-dire-bear",
        "started": "2026-10-30T10:00:19Z", "ordinaryDeadline": "2026-10-30T10:10:19Z",
        "ACMode": "normal", "AC": 12, "physicalResistance": "nonmagical physical",
        "naturalAttack": {
            "sourceProfileBase": "PB+WIS to hit; 1d8+WIS slashing base claw",
            "circleForms": {"source": "druid.base.moon.circle-forms", "effect": "add S damage to first natural-form hit each turn"},
            "primalStrike": {"source": "druid.arch.moon.primal-strike", "effect": "counts magical against defenses to nonmagical physical attacks; damage type unchanged"},
        },
        "canSpeak": True, "canCastSpells": False, "handEquipmentUse": False,
        "earthSlamRecharge": {"source": "druid.arch.earth-warden-dire-bear", "printedRounds": 2, "remainingRounds": 0, "used": False, "owner": "MD196-TARGET-HUMAN-DRUID15-MAGE5", "survivesFormLoss": True},
        "equipmentMelded": ["woodenDruidicFocusStaff", "commonClothes"],
    },
    "rootAnatomy": False,
    "formTempHP": 30,
    "resistances": [
        {"source": "mage.base.elemental-affinity", "type": "fire", "status": "active"},
        {"source": "druid.arch.earth-warden-dire-bear", "type": "nonmagical physical", "status": "active while form exists"},
    ],
    "shiftUses": {"current": 5, "max": 6},
    "bufferReserve": {"current": 5, "max": 35},
    "ordinaryTurnBudgets": {"Action": "ready; unspent", "BonusAction": "spent: Earth Warden shift", "Reaction": "available then turn ended"},
    "equipment": {"woodenDruidicFocusStaff": "owned; melded/inaccessible", "commonClothes": "owned; melded/inaccessible", "coin": "74gp 5sp"},
    "currentTargetTurn": "T4 starts10:00:18Z; Earth Warden shift Bonus Action10:00:19Z; T4 END10:00:24Z",
    "formSourceCounters": {"earthSlam": {"printedRechargeRounds": 2, "remainingRounds": 0, "used": False, "persistsAcrossFormLoss": True}},
})

target_t5_start = copy.deepcopy(form)
target_t5_start.update({
    "ordinaryTurnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"},
    "currentTargetTurn": "T5 START10:00:24Z; Earth Warden active; no action yet",
})

ui = copy.deepcopy(target_t5_start)
ui.update({
    "classAvailability": {"Druid": False, "Mage": False},
    "classDerivedProficiencyAvailable": False,
    "subjectiveBelief": {"text": "I am Rowan Vale, a traveling herbalist.", "endMarker": "first future target regular END excluding current T5: T6 END10:00:36Z", "autonomous": True},
    "form": None, "formTempHP": 0, "rootAnatomy": True, "AC": 12,
    "resistances": [], "concentration": None, "familiarCommandAvailable": False,
    "equipment": {"woodenDruidicFocusStaff": "owned; returned to root right hand", "commonClothes": "owned; worn on root anatomy", "coin": "74gp 5sp"},
    "ordinaryTurnBudgets": {"Action": "ready at T5 START10:00:24Z; not yet spent at admission10:00:27Z", "BonusAction": "ready at T5 START10:00:24Z", "Reaction": "ready at T5 START10:00:24Z"},
    "currentTargetTurn": "T5 START10:00:24Z; Unravel admitted10:00:27Z; T5 END10:00:30Z excluded; first future target END T6 END10:00:36Z",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:36Z", "classLoss": "active through current T5 END; ends at first future regular END T6 END10:00:36Z", "belief": "active through current T5 END; ends at first future regular END T6 END10:00:36Z", "initialSave": "none", "concentration": False, "formLossRule": "approved Unravel-only NEW UI251-FORM-LOSS"},
    "formSourceCounters": {"earthSlam": {"printedRechargeRounds": 2, "remainingRounds": 0, "used": False, "persistsAcrossFormLoss": True}},
})

# Explicit T5 and T6 branch states. UI196-CLOCK excludes the turn already in progress at :27.
natural_start = copy.deepcopy(target_t5_start); natural_start["branch"] = "NATURAL-EXPIRY"
natural_start["currentTargetTurn"] = "NATURAL-EXPIRY T5 START10:00:24Z; no action yet"
mb_start = copy.deepcopy(target_t5_start); mb_start["branch"] = "MINDBLANK-CONDITIONAL"
mb_start["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T5 START10:00:24Z; no successful suppression interval asserted"
dispel_start = copy.deepcopy(target_t5_start); dispel_start["branch"] = "ARCH-DISPEL-REMOVAL"
dispel_start["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T5 START10:00:24Z; UI-01 active until a later removal"
ui_natural = copy.deepcopy(ui); ui_natural["branch"] = "NATURAL-EXPIRY"
ui_mb = copy.deepcopy(ui); ui_mb["branch"] = "MINDBLANK-CONDITIONAL"
ui_dis = copy.deepcopy(ui); ui_dis["branch"] = "ARCH-DISPEL-REMOVAL"

natural_dodge = copy.deepcopy(ui_natural)
natural_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:29Z", "BonusAction": "ready", "Reaction": "ready"}
natural_dodge["currentTargetTurn"] = "NATURAL-EXPIRY T5 Action Dodge10:00:29Z; END10:00:30Z scheduled"
natural_t5_end = copy.deepcopy(natural_dodge)
natural_t5_end.update({
    "classAvailability": {"Druid": False, "Mage": False}, "classDerivedProficiencyAvailable": False,
    "familiarCommandAvailable": False,
    "dissonance": {"current": 0, "limit": 12},
    "ordinaryTurnBudgets": {"Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"},
    "currentTargetTurn": "NATURAL-EXPIRY T5 END10:00:30Z; Let the Note Fall1→0; UI-01/class loss remain active through T6 END10:00:36Z",
})
natural_t6_start = copy.deepcopy(natural_t5_end)
natural_t6_start["ordinaryTurnBudgets"] = {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}
natural_t6_start["currentTargetTurn"] = "NATURAL-EXPIRY T6 START10:00:30Z; UI-01 remains active; command unavailable"
natural_t6_dodge = copy.deepcopy(natural_t6_start)
natural_t6_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:33Z", "BonusAction": "ready", "Reaction": "ready"}
natural_t6_dodge["currentTargetTurn"] = "NATURAL-EXPIRY T6 Dodge10:00:33Z; END10:00:36Z scheduled"
natural_end = copy.deepcopy(natural_t6_dodge)
natural_end.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": None,
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored with Mage availability at T6 END"}],
    "familiarCommandAvailable": True,
    "ordinaryTurnBudgets": {"Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"},
    "currentTargetTurn": "NATURAL-EXPIRY T6 END10:00:36Z; Let the Note Fall0→0; UI-01 naturally ends",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:36Z", "clockRule": "first future target regular END excluding T5 already in progress at admission", "classLoss": "ended at T6 END", "belief": "ended at T6 END", "initialSave": "none", "concentration": False, "formLossRule": "approved Unravel-only NEW UI251-FORM-LOSS"},
})

# Mind Blank remains a non-operative conditional projection; the actual branch follows natural expiry.
mb_suppressed = copy.deepcopy(ui_mb)
mb_suppressed.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": {"text": "I am Rowan Vale, a traveling herbalist.", "status": "hypothetically suppressed; conditional only"},
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "conditional projection only if bound duration supports suppression"}],
    "familiarCommandAvailable": True,
    "suppressionBranchStatus": "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS; operative duration unbound",
    "currentTargetTurn": "conditional projection at10:00:28Z only; not used by actual target-turn path",
})
mb_dodge = copy.deepcopy(ui_mb)
mb_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:29Z", "BonusAction": "ready", "Reaction": "ready"}
mb_dodge["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T5 Action Dodge10:00:29Z; END10:00:30Z scheduled"
mb_t5_end = copy.deepcopy(natural_t5_end); mb_t5_end["branch"] = "MINDBLANK-CONDITIONAL"
mb_t5_end["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T5 END10:00:30Z; UI-01 remains active; conditional duration not established"
mb_t6_start = copy.deepcopy(natural_t6_start); mb_t6_start["branch"] = "MINDBLANK-CONDITIONAL"
mb_t6_dodge = copy.deepcopy(natural_t6_dodge); mb_t6_dodge["branch"] = "MINDBLANK-CONDITIONAL"
mb_end = copy.deepcopy(natural_end); mb_end["branch"] = "MINDBLANK-CONDITIONAL"
mb_end["suppressionBranchStatus"] = "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS"
mb_end["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T6 END10:00:36Z; natural UI-01 expiry; Dissonance0→0"

# The successful Arch Dispel branch has its own exact target removal at :28.
dispelled = copy.deepcopy(ui_dis)
dispelled.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": None,
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored with Mage availability after Dispel"}],
    "familiarCommandAvailable": True,
    "currentTargetTurn": "ARCH-DISPEL-REMOVAL removed UI-01 at10:00:28Z; original scheduled natural expiry remains10:00:36Z",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:28Z", "actualTerminationAt": "2026-10-30T10:00:28Z", "scheduledNaturalExpiry": "2026-10-30T10:00:36Z", "clockRule": "first future target regular END excluding T5 already in progress at admission", "termination": "successful Arch Dispel; no longer active", "classLoss": "ended by Arch Dispel", "belief": "ended by Arch Dispel", "initialSave": "none", "concentration": False},
})
dispel_dodge = copy.deepcopy(dispelled)
dispel_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:29Z", "BonusAction": "ready", "Reaction": "ready"}
dispel_dodge["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T5 Action Dodge10:00:29Z; END10:00:30Z scheduled"
dispel_t5_end = copy.deepcopy(dispel_dodge)
dispel_t5_end.update({"dissonance": {"current": 0, "limit": 12}, "ordinaryTurnBudgets": {"Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentTargetTurn": "ARCH-DISPEL-REMOVAL T5 END10:00:30Z after actual UI-01 termination at :28; Let the Note Fall0→0"})
dispel_t6_start = copy.deepcopy(dispel_t5_end); dispel_t6_start["ordinaryTurnBudgets"] = {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}; dispel_t6_start["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T6 START10:00:30Z; UI-01 remains ended"
dispel_t6_dodge = copy.deepcopy(dispel_t6_start); dispel_t6_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:33Z", "BonusAction": "ready", "Reaction": "ready"}; dispel_t6_dodge["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T6 Dodge10:00:33Z; END10:00:36Z scheduled"
dispel_end = copy.deepcopy(dispel_t6_dodge); dispel_end.update({"ordinaryTurnBudgets": {"Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentTargetTurn": "ARCH-DISPEL-REMOVAL T6 END10:00:36Z; UI-01 remains ended; Let the Note Fall0→0"})


def familiar_phase(branch, resolution, owner_state, turn, start, end, phase_time):
    return {
        "actor": "FAM-FIRE-01", "id": "FAM-FIRE-01", "branch": branch,
        "source": "CREATURE_LIFECYCLE_PLAYTEST.md, At the table; mage.arch.conjure-elemental-familiar",
        "identity": "Fire", "HP": {"current": 14, "max": 14}, "AC": 18, "speed": 30, "fireResistance": True,
        "created": "2026-10-30T10:00:01Z", "deadline": "2026-10-30T10:10:01Z",
        "positionFt": [5, 0, 0], "ownerId": "MD196-TARGET-HUMAN-DRUID15-MAGE5",
        "ownerClassAvailability": copy.deepcopy(owner_state["classAvailability"]),
        "ownerClassDerivedProficiencyAvailable": owner_state["classDerivedProficiencyAvailable"],
        "ownerCommandPermission": owner_state["familiarCommandAvailable"],
        "ownerUnravel": copy.deepcopy(owner_state.get("unravel")),
        "ownerSubjectiveBelief": copy.deepcopy(owner_state.get("subjectiveBelief")),
        "ownerResistances": copy.deepcopy(owner_state["resistances"]),
        "ownerSnapshot": copy.deepcopy(owner_state),
        "pendingOrder": None, "mode": "no pending order; defensive Dodge in place; no independent attack/control",
        "conjureFamiliarUse": "spent", "commandHistory": [],
        "attachedPhase": {"ownerTurn": "target " + turn, "ownerTurnStart": start, "ownerTurnEnd": end, "phaseTime": phase_time, "resolution": resolution},
        "phase": "defensively Dodges after the whole owner turn; position unchanged; no independent turn, damage or control",
    }


phase_times = {"T5": ("2026-10-30T10:00:24Z", "2026-10-30T10:00:30Z", "2026-10-30T10:00:30.1Z"), "T6": ("2026-10-30T10:00:30Z", "2026-10-30T10:00:36Z", "2026-10-30T10:00:36.1Z")}
def phases(branch, owner_t5, owner_t6):
    a=phase_times["T5"]; b=phase_times["T6"]
    return {
        "T5": {"before": familiar_phase(branch,"pending after owner T5 END",owner_t5,"T5",*a), "after": familiar_phase(branch,"resolved after owner T5 END",owner_t5,"T5",*a)},
        "T6": {"before": familiar_phase(branch,"pending after owner T6 END",owner_t6,"T6",*b), "after": familiar_phase(branch,"resolved after owner T6 END",owner_t6,"T6",*b)},
    }
ph_nat = phases("NATURAL-EXPIRY",natural_t5_end,natural_end)
ph_mb = phases("MINDBLANK-CONDITIONAL",mb_t5_end,mb_end)
ph_dis = phases("ARCH-DISPEL-REMOVAL",dispel_t5_end,dispel_end)

# Caster profiles retain independent pools, turn budgets, casting families and concentrations.
u_before = {"actor": "WITNESS-UNRAVEL-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "spell": "unravel-identity rank9", "prepared": True, "focus": "Illusion left hand", "rightHand": "free", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": None, "castingFamilyHistory": []}
u_after = copy.deepcopy(u_before)
u_after.update({"RP": {"current": 38, "max": 64}, "turnBudgets": {"Action": "spent: Unravel Identity", "BonusAction": "ready", "Reaction": "ready"}, "castHistory": [{"time": "2026-10-30T10:00:27Z", "Action": "paid", "RP": 26, "Dissonance": 0, "family": "first distinct prepared Wizard matrix family"}], "castingFamilyHistory": ["unravel-identity first prepared matrix family"], "targetPositionFt": [0, 0, 0], "targetRegularEnd": "2026-10-30T10:00:36Z"})

mb_before = {"actor": "WITNESS-MINDBLANK-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "prepared": "mind-blank rank8", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": {"duration": "not established", "deadline": None, "status": "unknown"}, "castingFamilyHistory": []}
mb_after = copy.deepcopy(mb_before)
mb_after.update({"RP": {"current": 43, "max": 64}, "turnBudgets": {"Action": "spent: Mind Blank", "BonusAction": "ready", "Reaction": "ready"}, "castHistory": [{"time": "2026-10-30T10:00:28Z", "Action": "paid", "RP": 21, "Dissonance": 0, "family": "first distinct prepared Wizard matrix family"}], "castingFamilyHistory": ["mind-blank first prepared matrix family"], "sourceEffect": {"status": "duration unresolved; not asserted to suppress UI-01", "requiredBinding": "rank8ward5_reviewed_149/MODEL.json /spells/3/procedure"}})

dispel_before = {"actor": "WITNESS-ARCH-DISPEL-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "prepared": "detect-magic rank1", "archDispel": {"id": "wizard.arch.dispel-magic", "acquiredAtWizardLevel": 5, "alwaysPreparedClassMatrix": True, "outsideDailyPreparedSlotCount": True}, "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": None, "recharge": {"ArchDispel": 0}, "refrain": {"repeatCount": 0, "lastSpell": None}, "nukeChain": [], "castHistory": [], "castingFamilyHistory": [], "currentRegularTurn": "AD-T1 START10:00:12Z; Detect Magic Action10:00:13Z; END10:00:18Z"}
dispel_sensed = copy.deepcopy(dispel_before)
dispel_sensed.update({"RP": {"current": 62, "max": 64}, "turnBudgets": {"Action": "spent: Detect Magic", "BonusAction": "ready", "Reaction": "ready"}, "concentration": {"source": "Wizard detect-magic rank1", "started": "2026-10-30T10:00:13Z", "deadline": "2026-10-30T10:10:13Z", "active": True}, "refrain": {"repeatCount": 0, "lastSpell": "detect-magic"}, "castHistory": [{"time": "2026-10-30T10:00:13Z", "spell": "detect-magic", "Action": "paid", "RP": 2, "Dissonance": 0, "family": "first distinct prepared matrix family"}], "castingFamilyHistory": ["detect-magic prepared matrix family"], "currentRegularTurn": "AD-T1 START10:00:12Z; Detect Magic Action10:00:13Z; END10:00:18Z"})
dispel_t2_start = copy.deepcopy(dispel_sensed)
dispel_t2_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T2 START10:00:18Z"})
dispel_t2_end = copy.deepcopy(dispel_t2_start)
dispel_t2_end.update({"turnBudgets": {"Action": "available then turn ended", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "dissonance": {"current": 0, "limit": 13}, "currentRegularTurn": "AD-T2 END10:00:24Z; no spell/Weave; Let the Note Fall0→0"})
dispel_t3_start = copy.deepcopy(dispel_t2_end)
dispel_t3_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T3 START10:00:24Z; Detect Magic concentration active"})
dispel_after_cast = copy.deepcopy(dispel_t3_start)
dispel_after_cast.update({"RP": {"current": 59, "max": 64}, "turnBudgets": {"Action": "spent: Arch Dispel", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 2}, "refrain": {"repeatCount": 0, "lastSpell": "wizard.arch.dispel-magic"}, "castHistory": dispel_t3_start["castHistory"] + [{"time": "2026-10-30T10:00:28Z", "Action": "paid", "RP": 3, "Dissonance": 0, "selectedEffect": "UI-01 ongoing spell aura perceived at20ft before commitment", "family": "always-prepared Wizard class matrix; outside daily prepared-slot count"}], "castingFamilyHistory": ["detect-magic prepared matrix family", "wizard.arch.dispel-magic always-prepared Wizard class matrix family"], "currentRegularTurn": "AD-T3 START10:00:24Z; Arch Dispel Action10:00:28Z; END10:00:30Z", "perception": {"distanceFt": 20, "DetectMagicRangeFt": 30, "lineOfSight": "clear", "cover": "none", "activeAuraCountOnTarget": 1, "observedAt": "2026-10-30T10:00:27Z", "observation": "the unique ongoing spell aura on the target is UI-01; no other active spell aura is present"}, "check": {"roll": 8, "INT": 5, "PB": 6, "total": 19, "DC": 19, "result": "success"}})
dispel_t3_end = copy.deepcopy(dispel_after_cast)
dispel_t3_end.update({"turnBudgets": {"Action": "spent: Arch Dispel", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentRegularTurn": "AD-T3 END10:00:30Z; recharge remains2 until next regular start"})
dispel_after = copy.deepcopy(dispel_t3_end)
dispel_after.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 1}, "currentRegularTurn": "AD-T4 START10:00:30Z; Arch Dispel recharge ticks2→1 at regular initiative start", "rechargeTickHistory": [{"time": "2026-10-30T10:00:30Z", "before": 2, "after": 1, "source": "wizard.json /engine/12"}]})
dispel_t4_end = copy.deepcopy(dispel_after)
dispel_t4_end.update({"turnBudgets": {"Action": "available then turn ended", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentRegularTurn": "AD-T4 END10:00:36Z; no action/extra turn; recharge remains1"})
dispel_t5_start = copy.deepcopy(dispel_t4_end)
dispel_t5_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T5 START10:00:36Z; regular recharge ticks1→0", "rechargeTickHistory": dispel_after["rechargeTickHistory"] + [{"time": "2026-10-30T10:00:36Z", "before": 1, "after": 0, "source": "wizard.json /engine/12"}]})

# Helper regular-turn snapshots preserve spell-family history and pay the printed recharge clock at AD-T4 START.
dispel_t1_end = copy.deepcopy(dispel_sensed)
dispel_t1_end.update({"turnBudgets": {"Action": "spent: Detect Magic", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentRegularTurn": "AD-T1 END10:00:18Z; Detect Magic concentration continues"})
dispel_t2_start = copy.deepcopy(dispel_t1_end)
dispel_t2_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T2 START10:00:18Z"})

# Helper regular-turn snapshots preserve paid Action through END and tick recharge only at START.
dispel_t1_end = copy.deepcopy(dispel_sensed)
dispel_t1_end.update({"turnBudgets": {"Action": "spent: Detect Magic", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentRegularTurn": "AD-T1 END10:00:18Z; Detect Magic concentration continues"})
dispel_t2_start = copy.deepcopy(dispel_t1_end)
dispel_t2_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T2 START10:00:18Z"})
dispel_t3_end["turnBudgets"]["Action"] = "spent: Arch Dispel"

transitions = []

def add_transition(id, actor, branch, before, after, changed, at, source):
    b=copy.deepcopy(before); a=copy.deepcopy(after)
    transitions.append({"id":id,"actor":actor,"branch":branch,"timestamp":at,"source":source,"before":b,"beforeSha256":sha(b),"after":a,"afterSha256":sha(a),"changedPaths":changed,"inverseOperation":{"id":"INV-"+id,"meaning":"Static snapshot restoration only; not an in-world refund, reversal, recreated effect, or reset.","restoreSnapshot":b,"restoreSha256":sha(b)}})

# Shared target and helper chronology.
add_transition("OP256-01-TARGET-FAMILIAR","target","COMMON",base,fam,["sharedRP","dissonance","refrain","conjureFamiliarUse","familiar","ordinaryTurnBudgets"],"2026-10-30T10:00:01Z","mage.arch.conjure-elemental-familiar; source clock ten minutes")
add_transition("OP256-02-TARGET-T2-END-VENT","target","COMMON",fam,vent,["dissonance","ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:12Z","RESONANCE_CANON.md Let the Note Fall; T2 used no spell/Weave")
add_transition("OP256-03-TARGET-DETECT-MAGIC","target","COMMON",vent,dm,["sharedRP","dissonance","refrain","concentration","ordinaryTurnBudgets"],"2026-10-30T10:00:13Z","mage.base.detect-magic Action, exact Mage class card cost1RP")
add_transition("OP256-04-HELPER-DETECT-MAGIC","helper","ARCH-DISPEL-REMOVAL",dispel_before,dispel_sensed,["RP","turnBudgets","concentration","refrain","castHistory","castingFamilyHistory"],"2026-10-30T10:00:13Z","Wizard helper AD-T1 START :12; ordinary prepared detect-magic Action2RP; prepared-matrix family")
add_transition("OP256-05-HELPER-T1-END","helper","ARCH-DISPEL-REMOVAL",dispel_sensed,dispel_t1_end,["turnBudgets","currentRegularTurn"],"2026-10-30T10:00:18Z","Paid Detect Magic Action remains spent through T1 END")
add_transition("OP256-06-HELPER-T2-START","helper","ARCH-DISPEL-REMOVAL",dispel_t1_end,dispel_t2_start,["turnBudgets","currentRegularTurn"],"2026-10-30T10:00:18Z","AD-T2 START refreshes Action; recharge stays0 and Refrain/history persist")
add_transition("OP256-07-TARGET-EARTH-WARDEN-SHIFT","target","COMMON",dm,form,["refrain","form","formTempHP","resistances","shiftUses","bufferReserve","ordinaryTurnBudgets","formSourceCounters"],"2026-10-30T10:00:19Z","Druid Earth Warden Bonus Action; shapeshift clears remembered Refrain; no Mage spell cast")
for b,st in [("NATURAL-EXPIRY",natural_start),("MINDBLANK-CONDITIONAL",mb_start),("ARCH-DISPEL-REMOVAL",dispel_start)]:
    add_transition("OP256-08-"+b+"-T5-START","target",b,form,st,["ordinaryTurnBudgets","currentTargetTurn","branch"],"2026-10-30T10:00:24Z","Six-second target T5 START; reset budgets before :27 admission")
add_transition("OP256-09-HELPER-T2-END","helper","ARCH-DISPEL-REMOVAL",dispel_t2_start,dispel_t2_end,["dissonance","turnBudgets","currentRegularTurn"],"2026-10-30T10:00:24Z","AD-T2 no-spell/no-Weave turn; Let the Note Fall0→0")
add_transition("OP256-10-HELPER-T3-START","helper","ARCH-DISPEL-REMOVAL",dispel_t2_end,dispel_t3_start,["turnBudgets","currentRegularTurn"],"2026-10-30T10:00:24Z","AD-T3 START refreshes budgets; Detect Magic concentration remains active")
for b,st,ui_branch in [("NATURAL-EXPIRY",natural_start,ui_natural),("MINDBLANK-CONDITIONAL",mb_start,ui_mb),("ARCH-DISPEL-REMOVAL",dispel_start,ui_dis)]:
    add_transition("OP256-11-"+b+"-UNRAVEL-ADMISSION","target",b,st,ui_branch,["classAvailability","classDerivedProficiencyAvailable","subjectiveBelief","form","formTempHP","resistances","concentration","familiarCommandAvailable","unravel","equipment","formSourceCounters"],"2026-10-30T10:00:27Z","UI196-CLOCK excludes T5 already in progress; first future regular END is T6 END :36")
add_transition("OP256-12-UNRAVEL-CASTER","caster","COMMON",u_before,u_after,["RP","turnBudgets","castHistory","castingFamilyHistory","targetRegularEnd"],"2026-10-30T10:00:27Z","Wizard17 rank9 Unravel; Action/RP26; endpoint T6 END :36")
add_transition("OP256-13-MINDBLANK-CONDITIONAL-PROJECTION","target","MINDBLANK-CONDITIONAL-PROJECTION",ui_mb,mb_suppressed,["classAvailability","classDerivedProficiencyAvailable","subjectiveBelief","resistances","familiarCommandAvailable","suppressionBranchStatus"],"2026-10-30T10:00:28Z","Projection only; no successful suppression or duration-backed interval; excluded from actual target branch")
add_transition("OP256-14-MINDBLANK-CASTER","caster","MINDBLANK-CONDITIONAL",mb_before,mb_after,["RP","turnBudgets","castHistory","sourceEffect"],"2026-10-30T10:00:28Z","Wizard17 rank8 Mind Blank; duration unresolved; no successful suppression asserted")
add_transition("OP256-15-ARCH-DISPEL-USE","helper","ARCH-DISPEL-REMOVAL",dispel_t3_start,dispel_after_cast,["RP","turnBudgets","recharge","perception","check","refrain","castHistory","castingFamilyHistory"],"2026-10-30T10:00:28Z","Always-prepared Wizard class matrix; Action3RP; UI-01 at20ft within30ft, clear sight/no cover; 8+5+6=19 vs19")
add_transition("OP256-16-ARCH-DISPEL-TARGET-REMOVAL","target","ARCH-DISPEL-REMOVAL",ui_dis,dispelled,["classAvailability","classDerivedProficiencyAvailable","subjectiveBelief","resistances","familiarCommandAvailable","unravel"],"2026-10-30T10:00:28Z","Exact target UI-01 removal linked to OP256-15 successful Arch Dispel check; scheduled natural expiry :36 retained separately")

# T5 has its own end and attached familiar phase; natural/conditional class loss persists through :30.
add_transition("OP256-17-NATURAL-T5-DODGE","target","NATURAL-EXPIRY",ui_natural,natural_dodge,["ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:29Z","Target Dodge; no spell/Weave")
add_transition("OP256-18-MINDBLANK-T5-DODGE","target","MINDBLANK-CONDITIONAL",ui_mb,mb_dodge,["ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:29Z","Actual conditional branch remains unsuppressed; target Dodge")
add_transition("OP256-19-ARCH-DISPEL-T5-DODGE","target","ARCH-DISPEL-REMOVAL",dispelled,dispel_dodge,["ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:29Z","Target Dodge after recorded successful removal")
add_transition("OP256-20-NATURAL-T5-END","target","NATURAL-EXPIRY",natural_dodge,natural_t5_end,["dissonance","ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:30Z","T5 is excluded from UI clock; vent1→0 but class loss/UI remain active")
add_transition("OP256-21-MINDBLANK-T5-END","target","MINDBLANK-CONDITIONAL",mb_dodge,mb_t5_end,["dissonance","ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:30Z","No successful suppression; T5 vent1→0 and UI remains active")
add_transition("OP256-22-ARCH-DISPEL-T5-END","target","ARCH-DISPEL-REMOVAL",dispel_dodge,dispel_t5_end,["dissonance","ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:30Z","After earlier UI removal; T5 no-spell vent0→0")
add_transition("OP256-23-HELPER-T3-END","helper","ARCH-DISPEL-REMOVAL",dispel_after_cast,dispel_t3_end,["turnBudgets","currentRegularTurn"],"2026-10-30T10:00:30Z","Paid Arch Dispel Action remains spent through AD-T3 END; recharge remains2 until next START")
add_transition("OP256-24-HELPER-T4-START-RECHARGE","helper","ARCH-DISPEL-REMOVAL",dispel_t3_end,dispel_after,["turnBudgets","recharge","currentRegularTurn","rechargeTickHistory"],"2026-10-30T10:00:30Z","wizard.json /engine/12 regular START tick: recharge2→1")
for b,end_state,pair in [("NATURAL-EXPIRY",natural_t5_end,ph_nat["T5"]),("MINDBLANK-CONDITIONAL",mb_t5_end,ph_mb["T5"]),("ARCH-DISPEL-REMOVAL",dispel_t5_end,ph_dis["T5"])]:
    add_transition("OP256-25-"+b+"-T5-FAMILIAR-PHASE","familiar",b,pair["before"],pair["after"],["attachedPhase.resolution"],"2026-10-30T10:00:30.1Z","Complete familiar/owner state; attached phase after whole T5 END :30")

# All branches then complete T6; natural/conditional expiry happens at its END, never recreating earlier effects.
for b,st in [("NATURAL-EXPIRY",natural_t6_start),("MINDBLANK-CONDITIONAL",mb_t6_start),("ARCH-DISPEL-REMOVAL",dispel_t6_start)]:
    prev={"NATURAL-EXPIRY":natural_t5_end,"MINDBLANK-CONDITIONAL":mb_t5_end,"ARCH-DISPEL-REMOVAL":dispel_t5_end}[b]
    add_transition("OP256-26-"+b+"-T6-START","target",b,prev,st,["ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:30Z","T6 START resets turn budgets; UI state and resources carry forward")
for b,st,after in [("NATURAL-EXPIRY",natural_t6_start,natural_t6_dodge),("MINDBLANK-CONDITIONAL",mb_t6_start,mb_t6_dodge),("ARCH-DISPEL-REMOVAL",dispel_t6_start,dispel_t6_dodge)]:
    add_transition("OP256-27-"+b+"-T6-DODGE","target",b,st,after,["ordinaryTurnBudgets","currentTargetTurn"],"2026-10-30T10:00:33Z","Target Dodge Action; no spell/Weave")
for b,st,after in [("NATURAL-EXPIRY",natural_t6_dodge,natural_end),("MINDBLANK-CONDITIONAL",mb_t6_dodge,mb_end),("ARCH-DISPEL-REMOVAL",dispel_t6_dodge,dispel_end)]:
    add_transition("OP256-28-"+b+"-T6-END","target",b,st,after,["dissonance","classAvailability","classDerivedProficiencyAvailable","subjectiveBelief","resistances","familiarCommandAvailable","unravel","ordinaryTurnBudgets"],"2026-10-30T10:00:36Z","T6 END :36; natural UI expires only in natural/conditional branch; no effects/resources are recreated")
add_transition("OP256-29-HELPER-T4-END","helper","ARCH-DISPEL-REMOVAL",dispel_after,dispel_t4_end,["turnBudgets","currentRegularTurn"],"2026-10-30T10:00:36Z","AD-T4 END; no action; recharge remains1")
add_transition("OP256-30-HELPER-T5-START-RECHARGE","helper","ARCH-DISPEL-REMOVAL",dispel_t4_end,dispel_t5_start,["turnBudgets","recharge","currentRegularTurn","rechargeTickHistory"],"2026-10-30T10:00:36Z","wizard.json /engine/12 regular START tick: recharge1→0")
for b,pair in [("NATURAL-EXPIRY",ph_nat["T6"]),("MINDBLANK-CONDITIONAL",ph_mb["T6"]),("ARCH-DISPEL-REMOVAL",ph_dis["T6"])]:
    add_transition("OP256-31-"+b+"-T6-FAMILIAR-PHASE","familiar",b,pair["before"],pair["after"],["attachedPhase.resolution"],"2026-10-30T10:00:36.1Z","Complete familiar/owner state; attached phase after whole T6 END :36")

replay = {
    "id": "UNRAVEL-IDENTITY-MD196-B02-FORWARD-INVERSE-REPLAY-256",
    "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "status": "SOURCE_BOUND_BRANCH_REPLAY_READY_FOR_DIRECTOR_RECHECK",
    "accepted": False,
    "applied": False,
    "planBinding": {"path": str(P.relative_to(W)).replace("\\", "/"), "bytes": P.stat().st_size, "sha256": hashlib.sha256(P.read_bytes()).hexdigest()},
    "initialFixture": {"postLongRestState": "commonTargetSnapshots.afterLongRest", "claimedRestTransition": False, "roundPeriodSeconds": 6},
    "clockRule": {"id": "UI196-CLOCK", "rule": "first future target regular END excluding the target turn already in progress at admission", "admittedAt": "2026-10-30T10:00:27Z", "currentTurn": "T5 10:00:24–10:00:30", "excludedEnd": "2026-10-30T10:00:30Z", "firstFutureEnd": "2026-10-30T10:00:36Z"},
    "commonTargetSnapshots": {
        "afterLongRest": base, "afterFamiliar": fam, "afterNoSpellVentT2": vent,
        "afterDetectMagic": dm, "afterEarthWardenShift": form, "afterTargetT5Start": target_t5_start,
        "afterUnravelAdmission": ui,
        "afterNaturalT5Dodge": natural_dodge, "afterNaturalT5EndStillUnderUI": natural_t5_end,
        "afterNaturalT6Start": natural_t6_start, "afterNaturalT6Dodge": natural_t6_dodge, "afterNaturalExpiry": natural_end,
        "afterMindBlankConditionalProjection": mb_suppressed, "afterMindBlankT5Dodge": mb_dodge, "afterMindBlankT5EndStillUnderUI": mb_t5_end,
        "afterMindBlankT6Start": mb_t6_start, "afterMindBlankT6Dodge": mb_t6_dodge, "afterMindBlankT6EndConditional": mb_end,
        "afterArchDispelT5Start": dispel_start, "afterArchDispelRemoval": dispelled, "afterArchDispelT5Dodge": dispel_dodge,
        "afterArchDispelT5End": dispel_t5_end, "afterArchDispelT6Start": dispel_t6_start,
        "afterArchDispelT6Dodge": dispel_t6_dodge, "afterArchDispelT6End": dispel_end,
    },
    "branchTurnLedgers": {
        "NATURAL-EXPIRY": [
            {"time":"2026-10-30T10:00:24Z","marker":"target T5 START; budgets reset","transition":"OP256-08-NATURAL-EXPIRY-T5-START"},
            {"time":"2026-10-30T10:00:27Z","marker":"Unravel admitted; current T5 excluded by UI196-CLOCK; scheduled natural expiry T6 END :36","transition":"OP256-11-NATURAL-EXPIRY-UNRAVEL-ADMISSION"},
            {"time":"2026-10-30T10:00:29Z","marker":"target T5 Dodge Action","transition":"OP256-17-NATURAL-T5-DODGE"},
            {"time":"2026-10-30T10:00:30Z","marker":"T5 END; Dissonance1→0; class loss/UI remain active","transition":"OP256-20-NATURAL-T5-END"},
            {"time":"2026-10-30T10:00:30Z","marker":"target T6 START; budgets reset; UI/class loss remain active","transition":"OP256-26-NATURAL-EXPIRY-T6-START"},
            {"time":"2026-10-30T10:00:30.1Z","marker":"familiar attached phase after whole T5; command permission false","transition":"OP256-25-NATURAL-EXPIRY-T5-FAMILIAR-PHASE"},
            {"time":"2026-10-30T10:00:33Z","marker":"target T6 Dodge Action","transition":"OP256-27-NATURAL-EXPIRY-T6-DODGE"},
            {"time":"2026-10-30T10:00:36Z","marker":"T6 END; natural expiry; Dissonance0→0; restore availability","transition":"OP256-28-NATURAL-EXPIRY-T6-END"},
            {"time":"2026-10-30T10:00:36.1Z","marker":"familiar attached phase after whole T6; command permission true","transition":"OP256-31-NATURAL-EXPIRY-T6-FAMILIAR-PHASE"},
        ],
        "MINDBLANK-CONDITIONAL": [
            {"time":"2026-10-30T10:00:24Z","marker":"target T5 START; budgets reset","transition":"OP256-08-MINDBLANK-CONDITIONAL-T5-START"},
            {"time":"2026-10-30T10:00:27Z","marker":"Unravel admitted; current T5 excluded; natural expiry T6 END :36","transition":"OP256-11-MINDBLANK-CONDITIONAL-UNRAVEL-ADMISSION"},
            {"time":"2026-10-30T10:00:28Z","marker":"conditional projection only; not part of actual branch"},
            {"time":"2026-10-30T10:00:29Z","marker":"target T5 Dodge Action","transition":"OP256-18-MINDBLANK-T5-DODGE"},
            {"time":"2026-10-30T10:00:30Z","marker":"T5 END; Dissonance1→0; UI/class loss remain active","transition":"OP256-21-MINDBLANK-T5-END"},
            {"time":"2026-10-30T10:00:30Z","marker":"target T6 START; budgets reset; UI/class loss remain active","transition":"OP256-26-MINDBLANK-CONDITIONAL-T6-START"},
            {"time":"2026-10-30T10:00:30.1Z","marker":"familiar attached phase after whole T5; command permission false","transition":"OP256-25-MINDBLANK-CONDITIONAL-T5-FAMILIAR-PHASE"},
            {"time":"2026-10-30T10:00:33Z","marker":"target T6 Dodge Action","transition":"OP256-27-MINDBLANK-CONDITIONAL-T6-DODGE"},
            {"time":"2026-10-30T10:00:36Z","marker":"T6 END; natural expiry; Dissonance0→0; restore availability","transition":"OP256-28-MINDBLANK-CONDITIONAL-T6-END"},
            {"time":"2026-10-30T10:00:36.1Z","marker":"familiar attached phase after whole T6; command permission true","transition":"OP256-31-MINDBLANK-CONDITIONAL-T6-FAMILIAR-PHASE"},
        ],
        "ARCH-DISPEL-REMOVAL": [
            {"time":"2026-10-30T10:00:24Z","marker":"target T5 START; budgets reset","transition":"OP256-08-ARCH-DISPEL-REMOVAL-T5-START"},
            {"time":"2026-10-30T10:00:27Z","marker":"Unravel admitted; scheduled natural expiry :36","transition":"OP256-11-ARCH-DISPEL-REMOVAL-UNRAVEL-ADMISSION"},
            {"time":"2026-10-30T10:00:28Z","marker":"successful helper check; target transition terminates UI-01; preserve scheduled natural expiry :36","transition":"OP256-16-ARCH-DISPEL-TARGET-REMOVAL"},
            {"time":"2026-10-30T10:00:29Z","marker":"target T5 Dodge Action","transition":"OP256-19-ARCH-DISPEL-T5-DODGE"},
            {"time":"2026-10-30T10:00:30Z","marker":"T5 END; Dissonance0→0","transition":"OP256-22-ARCH-DISPEL-T5-END"},
            {"time":"2026-10-30T10:00:30Z","marker":"target T6 START; UI remains ended","transition":"OP256-26-ARCH-DISPEL-REMOVAL-T6-START"},
            {"time":"2026-10-30T10:00:30.1Z","marker":"familiar attached phase after whole T5; command permission true","transition":"OP256-25-ARCH-DISPEL-REMOVAL-T5-FAMILIAR-PHASE"},
            {"time":"2026-10-30T10:00:33Z","marker":"target T6 Dodge Action","transition":"OP256-27-ARCH-DISPEL-REMOVAL-T6-DODGE"},
            {"time":"2026-10-30T10:00:36Z","marker":"T6 END; UI remains ended; Dissonance0→0","transition":"OP256-28-ARCH-DISPEL-REMOVAL-T6-END"},
            {"time":"2026-10-30T10:00:36.1Z","marker":"familiar attached phase after whole T6; command permission true","transition":"OP256-31-ARCH-DISPEL-REMOVAL-T6-FAMILIAR-PHASE"},
        ],
    },
    "familiarAttachedPhases": {"naturalExpiry":ph_nat,"mindBlankConditional":ph_mb,"archDispel":ph_dis},
    "casterSnapshots": {
        "unravelBefore":u_before,"unravelAfter":u_after,"mindBlankBefore":mb_before,"mindBlankAfter":mb_after,
        "dispelBefore":dispel_before,"dispelAfterDetectMagic":dispel_sensed,"dispelAfterT1End":dispel_t1_end,
        "dispelAfterT2Start":dispel_t2_start,"dispelAfterT2End":dispel_t2_end,"dispelAfterT3Start":dispel_t3_start,
        "dispelAfterArchDispelCast":dispel_after_cast,"dispelAfterT3End":dispel_t3_end,"dispelAfterT4Start":dispel_after,
        "dispelAfterT4End":dispel_t4_end,"dispelAfterT5Start":dispel_t5_start,
    },
    "helperRegularTurnLedger": [
        {"turn":"AD-T1","start":"2026-10-30T10:00:12Z","action":"ordinary prepared detect-magic Action :13; pay2RP","end":"2026-10-30T10:00:18Z","actionAtEnd":"spent: Detect Magic","refrainAfter":{"repeatCount":0,"lastSpell":"detect-magic"},"castingFamilies":["detect-magic prepared matrix family"]},
        {"turn":"AD-T2","start":"2026-10-30T10:00:18Z","action":"none; no spell/Weave","end":"2026-10-30T10:00:24Z","dissonance":"0→0","refrainPreserved":True,"castingFamiliesPreserved":True},
        {"turn":"AD-T3","start":"2026-10-30T10:00:24Z","action":"always-prepared wizard.arch.dispel-magic Action :28; pay3RP; recharge2","end":"2026-10-30T10:00:30Z","actionAtEnd":"spent: Arch Dispel","refrainAfter":{"repeatCount":0,"lastSpell":"wizard.arch.dispel-magic"},"castingFamilies":["detect-magic prepared matrix family","wizard.arch.dispel-magic always-prepared Wizard class matrix family"]},
        {"turn":"AD-T4","start":"2026-10-30T10:00:30Z","action":"no action; recharge2→1 at START","end":"2026-10-30T10:00:36Z","rechargeAtEnd":1},
        {"turn":"AD-T5","start":"2026-10-30T10:00:36Z","action":"no action; recharge1→0 at START","rechargeAtStart":0,"source":"wizard.json /engine/12"},
    ],
    "helperRegularTurnSnapshots": {"T1Start":dispel_before,"T1AfterDetectMagic":dispel_sensed,"T1End":dispel_t1_end,"T2Start":dispel_t2_start,"T2End":dispel_t2_end,"T3Start":dispel_t3_start,"T3AfterArchDispel":dispel_after_cast,"T3End":dispel_t3_end,"T4StartAfterRechargeTick":dispel_after,"T4End":dispel_t4_end,"T5StartAfterRechargeTick":dispel_t5_start},
    "forwardInverseTransitions": transitions,
    "coverage": {
        "naturalExpiry":"Complete UI196-CLOCK schedule: admission :27 during T5 excludes T5 END :30; T5 vents1→0, T6 ends :36 and restores availability; familiar phases :30.1 (command false) and :36.1 (true).",
        "mindBlank":"Conditional only. Duration is unbound and no successful suppression is counted. Actual branch follows the same T5/T6 natural clock; hypothetical projection is isolated from target continuity.",
        "archDispel":"Helper observes unique UI-01 at20ft within30ft with clear sight/no cover; successful check at :28 is followed by its exact target removal transition. Scheduled natural expiry :36 is separately retained; helper T1–T5 schedule includes Action-end persistence and recharge ticks2→1→0 at starts :30/:36.",
        "letTheNoteFall":"Target T2 vents1→0; T3 Detect Magic adds1; T4 shift uses Weave and clears Refrain; target T5 no-spell Dodge vents1→0 at :30; T6 no-spell Dodge vents0→0 at :36. No RP/HP/reserve/rest/per-rest refill.",
        "formLoss":"Unravel at :27 ends Earth Warden/tempHP30/physical resistance/attacks once; Mage Fire resistance unavailable through T5 and restored at T6 END (or by exact Dispel at :28). DM-01 ends terminally and is never restored.",
        "familiar":"Complete before/after snapshots at each :30.1 and :36.1 attached phase include all familiar and owner state. Natural/conditional :30.1 command false; :36.1 command true. No generic Action/Bonus/Reaction budget or independent turn.",
        "helperIdentity":"Ordinary prepared detect-magic records Refrain identity exactly as detect-magic; acquired wizard.arch.dispel-magic remains its distinct always-prepared class-matrix family.",
        "removedArcaneMissile":"No Arcane Missile is cast; no target, damage, Action or RP event is part of this witness.",
        "earthWardenAttack":"Base claw, Circle Forms first-hit S rider and Primal Strike magical-defense modifier are separate. Earth Slam recharge length2/current0 survives form loss.",
        "existingCases":"Return241 cases unchanged; only a new static witness/replay is authored.",
    },
    "qualification":"Static source-qualified data replay; no runtime or campaign execution claim. Mind Blank remains conditional. No identity acceptance/application/canonical change is asserted.",
}
OUT.write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raw = OUT.read_bytes()
print(json.dumps({"path": str(OUT), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}", "transitionCount": len(transitions), "transitionIds": [x["id"] for x in transitions]}, ensure_ascii=False, indent=2))
