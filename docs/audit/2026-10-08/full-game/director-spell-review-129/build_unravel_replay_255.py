import copy
import hashlib
import json
import pathlib
import zlib

W = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
B = W / "docs/audit/2026-10-08/full-game/director-spell-review-129"
P = B / "UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_255.json"
OUT = B / "UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_255.json"
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
    "subjectiveBelief": {"text": "I am Rowan Vale, a traveling herbalist.", "endMarker": "first future target regular END10:00:30Z", "autonomous": True},
    "form": None, "formTempHP": 0, "rootAnatomy": True, "AC": 12,
    "resistances": [], "concentration": None, "familiarCommandAvailable": False,
    "equipment": {"woodenDruidicFocusStaff": "owned; returned to root right hand", "commonClothes": "owned; worn on root anatomy", "coin": "74gp 5sp"},
    "ordinaryTurnBudgets": {"Action": "ready at T5 START10:00:24Z; not yet spent at admission10:00:27Z", "BonusAction": "ready at T5 START10:00:24Z", "Reaction": "ready at T5 START10:00:24Z"},
    "currentTargetTurn": "T5 starts10:00:24Z; Unravel admitted10:00:27Z; first future target END10:00:30Z",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:30Z", "classLoss": "active until first future target END", "belief": "active until first future target END", "initialSave": "none", "concentration": False, "formLossRule": "approved Unravel-only NEW UI251-FORM-LOSS"},
    "formSourceCounters": {"earthSlam": {"printedRechargeRounds": 2, "remainingRounds": 0, "used": False, "persistsAcrossFormLoss": True}},
})

# Three explicit T5 starts share the same :24 target-turn marker but retain separate fork labels.
natural_start = copy.deepcopy(target_t5_start)
natural_start["branch"] = "NATURAL-EXPIRY"
natural_start["currentTargetTurn"] = "NATURAL-EXPIRY T5 START10:00:24Z; no action yet"
mb_start = copy.deepcopy(target_t5_start)
mb_start["branch"] = "MINDBLANK-CONDITIONAL"
mb_start["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T5 START10:00:24Z; no successful suppression interval asserted"
dispel_start = copy.deepcopy(target_t5_start)
dispel_start["branch"] = "ARCH-DISPEL-REMOVAL"
dispel_start["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T5 START10:00:24Z; UI-01 active until a later removal"

ui_natural = copy.deepcopy(ui); ui_natural["branch"] = "NATURAL-EXPIRY"
ui_mb = copy.deepcopy(ui); ui_mb["branch"] = "MINDBLANK-CONDITIONAL"
ui_dis = copy.deepcopy(ui); ui_dis["branch"] = "ARCH-DISPEL-REMOVAL"

# Natural-end branch: Unravel is admitted at :27, Dodge at :29, and expires at the first future END :30.
natural_dodge = copy.deepcopy(ui_natural)
natural_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:29Z", "BonusAction": "ready", "Reaction": "ready"}
natural_dodge["currentTargetTurn"] = "NATURAL-EXPIRY T5 Action Dodge10:00:29Z; END10:00:30Z scheduled"
natural_end = copy.deepcopy(natural_dodge)
natural_end.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": None,
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored with Mage availability"}],
    "familiarCommandAvailable": True,
    "dissonance": {"current": 0, "limit": 12},
    "ordinaryTurnBudgets": {"Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"},
    "currentTargetTurn": "NATURAL-EXPIRY T5 END10:00:30Z; Let the Note Fall1→0; Unravel naturally ended",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:30Z", "classLoss": "ended at first future target END", "belief": "ended at first future target END", "initialSave": "none", "concentration": False, "formLossRule": "approved Unravel-only NEW UI251-FORM-LOSS"},
})

# Conditional callback projection only; no successful Mind Blank suppression interval is claimed.
mb_suppressed = copy.deepcopy(ui_mb)
mb_suppressed.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": {"text": "I am Rowan Vale, a traveling herbalist.", "status": "suppressed; conditional only"},
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored only if a bound Mind Blank duration legally suppresses class loss"}],
    "familiarCommandAvailable": True,
    "suppressionBranchStatus": "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS; operative duration unbound",
    "currentTargetTurn": "conditional projection at10:00:28Z; no successful suppression interval asserted; Dodge10:00:29Z; END10:00:30Z",
})
mb_dodge = copy.deepcopy(mb_suppressed)
mb_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:29Z", "BonusAction": "ready", "Reaction": "ready"}
mb_dodge["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T5 Action Dodge10:00:29Z; END10:00:30Z scheduled"
mb_end = copy.deepcopy(natural_end)
mb_end["suppressionBranchStatus"] = "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS"
mb_end["currentTargetTurn"] = "MINDBLANK-CONDITIONAL T5 END10:00:30Z; UI naturally expires; Dissonance1→0"

# Dispel branch ends only UI-01 at :28; all later T5 events remain explicit.
dispelled = copy.deepcopy(ui_dis)
dispelled.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": None,
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored with Mage availability"}],
    "familiarCommandAvailable": True,
    "currentTargetTurn": "ARCH-DISPEL-REMOVAL ended UI-01 at10:00:28Z during target T5; Dodge10:00:29Z; END10:00:30Z",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:28Z", "classLoss": "ended by Arch Dispel at10:00:28Z", "belief": "ended by Arch Dispel at10:00:28Z", "initialSave": "none", "concentration": False},
})
dispel_dodge = copy.deepcopy(dispelled)
dispel_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge at10:00:29Z", "BonusAction": "ready", "Reaction": "ready"}
dispel_dodge["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T5 Action Dodge10:00:29Z; END10:00:30Z scheduled"
dispel_end = copy.deepcopy(natural_end)
dispel_end["branch"] = "ARCH-DISPEL-REMOVAL"
dispel_end["unravel"]["endsAt"] = "2026-10-30T10:00:28Z"
dispel_end["unravel"]["classLoss"] = "ended by Arch Dispel at10:00:28Z"
dispel_end["unravel"]["belief"] = "ended by Arch Dispel at10:00:28Z"
dispel_end["currentTargetTurn"] = "ARCH-DISPEL-REMOVAL T5 END10:00:30Z after UI-01 removal; Let the Note Fall1→0"

def familiar_phase(branch, resolution, owner_state):
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
        "pendingOrder": None, "mode": "no pending order; defensive Dodge in place; no independent attack/control",
        "conjureFamiliarUse": "spent", "commandHistory": [],
        "attachedPhase": {"ownerTurn": "target T5", "ownerTurnStart": "2026-10-30T10:00:24Z", "ownerTurnEnd": "2026-10-30T10:00:30Z", "phaseTime": "2026-10-30T10:00:30.1Z", "resolution": resolution},
        "phase": "defensively Dodges after the whole owner turn; position unchanged; no independent turn, damage or control",
    }


ph_nat_before = familiar_phase("NATURAL-EXPIRY", "pending after owner END", natural_end)
ph_nat = familiar_phase("NATURAL-EXPIRY", "resolved after owner END", natural_end)
ph_mb_before = familiar_phase("MINDBLANK-CONDITIONAL", "pending after owner END", mb_end)
ph_mb = familiar_phase("MINDBLANK-CONDITIONAL", "resolved after owner END", mb_end) | {"qualification": "Mind Blank suppression remains conditional and is not counted; the owner's UI naturally expires at T5 END before this phase."}
ph_dis_before = familiar_phase("ARCH-DISPEL-REMOVAL", "pending after owner END", dispel_end)
ph_dis = familiar_phase("ARCH-DISPEL-REMOVAL", "resolved after owner END", dispel_end)

# Caster profiles retain independent pools, turn budgets, casting families and concentrations.
u_before = {"actor": "WITNESS-UNRAVEL-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "spell": "unravel-identity rank9", "prepared": True, "focus": "Illusion left hand", "rightHand": "free", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": None, "castingFamilyHistory": []}
u_after = copy.deepcopy(u_before)
u_after.update({"RP": {"current": 38, "max": 64}, "turnBudgets": {"Action": "spent: Unravel Identity", "BonusAction": "ready", "Reaction": "ready"}, "castHistory": [{"time": "2026-10-30T10:00:27Z", "Action": "paid", "RP": 26, "Dissonance": 0, "family": "first distinct prepared Wizard matrix family"}], "castingFamilyHistory": ["unravel-identity first prepared matrix family"], "targetPositionFt": [0, 0, 0], "targetRegularEnd": "2026-10-30T10:00:30Z"})

mb_before = {"actor": "WITNESS-MINDBLANK-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "prepared": "mind-blank rank8", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": {"duration": "not established", "deadline": None, "status": "unknown"}, "castingFamilyHistory": []}
mb_after = copy.deepcopy(mb_before)
mb_after.update({"RP": {"current": 43, "max": 64}, "turnBudgets": {"Action": "spent: Mind Blank", "BonusAction": "ready", "Reaction": "ready"}, "castHistory": [{"time": "2026-10-30T10:00:28Z", "Action": "paid", "RP": 21, "Dissonance": 0, "family": "first distinct prepared Wizard matrix family"}], "castingFamilyHistory": ["mind-blank first prepared matrix family"], "sourceEffect": {"status": "duration unresolved; not asserted to suppress UI-01", "requiredBinding": "rank8ward5_reviewed_149/MODEL.json /spells/3/procedure"}})

dispel_before = {"actor": "WITNESS-ARCH-DISPEL-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "prepared": "detect-magic rank1", "archDispel": {"id": "wizard.arch.dispel-magic", "acquiredAtWizardLevel": 5, "alwaysPreparedClassMatrix": True, "outsideDailyPreparedSlotCount": True}, "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": None, "recharge": {"ArchDispel": 0}, "refrain": {"repeatCount": 0, "lastSpell": None}, "nukeChain": [], "castHistory": [], "castingFamilyHistory": [], "currentRegularTurn": "AD-T1 START10:00:12Z; Detect Magic Action10:00:13Z; END10:00:18Z"}
dispel_sensed = copy.deepcopy(dispel_before)
dispel_sensed.update({"RP": {"current": 62, "max": 64}, "turnBudgets": {"Action": "spent: Detect Magic", "BonusAction": "ready", "Reaction": "ready"}, "concentration": {"source": "Wizard detect-magic rank1", "started": "2026-10-30T10:00:13Z", "deadline": "2026-10-30T10:10:13Z", "active": True}, "refrain": {"repeatCount": 0, "lastSpell": "wizard.base.detect-magic"}, "castHistory": [{"time": "2026-10-30T10:00:13Z", "Action": "paid", "RP": 2, "Dissonance": 0, "family": "first distinct prepared matrix family"}], "castingFamilyHistory": ["detect-magic prepared matrix family"], "currentRegularTurn": "AD-T1 START10:00:12Z; Detect Magic Action10:00:13Z; END10:00:18Z"})
dispel_t2_start = copy.deepcopy(dispel_sensed)
dispel_t2_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T2 START10:00:18Z"})
dispel_t2_end = copy.deepcopy(dispel_t2_start)
dispel_t2_end.update({"turnBudgets": {"Action": "available then turn ended", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "dissonance": {"current": 0, "limit": 13}, "currentRegularTurn": "AD-T2 END10:00:24Z; no spell/Weave; Let the Note Fall0→0"})
dispel_t3_start = copy.deepcopy(dispel_t2_end)
dispel_t3_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T3 START10:00:24Z; Detect Magic concentration active"})
dispel_after_cast = copy.deepcopy(dispel_t3_start)
dispel_after_cast.update({"RP": {"current": 59, "max": 64}, "turnBudgets": {"Action": "spent: Arch Dispel", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 2}, "refrain": {"repeatCount": 0, "lastSpell": "wizard.arch.dispel-magic"}, "castHistory": dispel_t3_start["castHistory"] + [{"time": "2026-10-30T10:00:28Z", "Action": "paid", "RP": 3, "Dissonance": 0, "selectedEffect": "UI-01 ongoing spell aura perceived at20ft before commitment", "family": "always-prepared Wizard class matrix; outside daily prepared-slot count"}], "castingFamilyHistory": ["detect-magic prepared matrix family", "wizard.arch.dispel-magic always-prepared Wizard class matrix family"], "currentRegularTurn": "AD-T3 START10:00:24Z; Arch Dispel Action10:00:28Z; END10:00:30Z", "perception": {"distanceFt": 20, "DetectMagicRangeFt": 30, "lineOfSight": "clear", "cover": "none", "activeAuraCountOnTarget": 1, "observedAt": "2026-10-30T10:00:27Z", "observation": "the unique ongoing spell aura on the target is UI-01; no other active spell aura is present"}, "check": {"roll": 8, "INT": 5, "PB": 6, "total": 19, "DC": 19, "result": "success"}})
dispel_t3_end = copy.deepcopy(dispel_after_cast)
dispel_t3_end.update({"turnBudgets": {"Action": "available then turn ended", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentRegularTurn": "AD-T3 END10:00:30Z; recharge remains2 until next regular start"})
dispel_after = copy.deepcopy(dispel_t3_end)
dispel_after.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 1}, "currentRegularTurn": "AD-T4 START10:00:30Z; Arch Dispel recharge ticks2→1 at regular initiative start", "rechargeTickHistory": [{"time": "2026-10-30T10:00:30Z", "before": 2, "after": 1, "source": "wizard.json /engine/12"}]})

# Helper regular-turn snapshots preserve spell-family history and pay the printed recharge clock at AD-T4 START.
dispel_t1_end = copy.deepcopy(dispel_sensed)
dispel_t1_end.update({"turnBudgets": {"Action": "available then turn ended", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"}, "currentRegularTurn": "AD-T1 END10:00:18Z; Detect Magic concentration continues"})
dispel_t2_start = copy.deepcopy(dispel_t1_end)
dispel_t2_start.update({"turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 0}, "currentRegularTurn": "AD-T2 START10:00:18Z"})

transitions = []


def add_transition(id, actor, branch, before, after, changed, at, source):
    b = copy.deepcopy(before)
    a = copy.deepcopy(after)
    transitions.append({
        "id": id, "actor": actor, "branch": branch, "timestamp": at, "source": source,
        "before": b, "beforeSha256": sha(b), "after": a, "afterSha256": sha(a),
        "changedPaths": changed,
        "inverseOperation": {"id": "INV-" + id, "meaning": "Static snapshot restoration only; not an in-world refund, reversal, recreated effect, or reset.", "restoreSnapshot": b, "restoreSha256": sha(b)},
    })


# Shared target chronology: T5 starts at :24; UI-01 is admitted at :27 and ends at :30.
add_transition("OP255-01-TARGET-FAMILIAR", "target", "COMMON", base, fam, ["sharedRP", "dissonance", "refrain", "conjureFamiliarUse", "familiar", "ordinaryTurnBudgets"], "2026-10-30T10:00:01Z", "mage.arch.conjure-elemental-familiar; source clock ten minutes")
add_transition("OP255-02-TARGET-T2-END-VENT", "target", "COMMON", fam, vent, ["dissonance", "ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:12Z", "RESONANCE_CANON.md Let the Note Fall; T2 used no spell/Weave")
add_transition("OP255-03-TARGET-DETECT-MAGIC", "target", "COMMON", vent, dm, ["sharedRP", "dissonance", "refrain", "concentration", "ordinaryTurnBudgets"], "2026-10-30T10:00:13Z", "mage.base.detect-magic Action, exact Mage class card cost1RP")
add_transition("OP255-04-HELPER-DETECT-MAGIC", "helper", "ARCH-DISPEL-REMOVAL", dispel_before, dispel_sensed, ["RP", "turnBudgets", "concentration", "refrain", "castHistory", "castingFamilyHistory"], "2026-10-30T10:00:13Z", "Wizard helper T1 START10:00:12; prepared Detect Magic Action2RP; prepared-matrix family")
add_transition("OP255-05-HELPER-T1-END", "helper", "ARCH-DISPEL-REMOVAL", dispel_sensed, dispel_t1_end, ["turnBudgets", "currentRegularTurn"], "2026-10-30T10:00:18Z", "Wizard helper T1 END; Detect Magic concentration remains active")
add_transition("OP255-06-HELPER-T2-START", "helper", "ARCH-DISPEL-REMOVAL", dispel_t1_end, dispel_t2_start, ["turnBudgets", "currentRegularTurn"], "2026-10-30T10:00:18Z", "Wizard helper T2 START; recharge stays0; prior spell/Refrain history preserved")
add_transition("OP255-07-TARGET-EARTH-WARDEN-SHIFT", "target", "COMMON", dm, form, ["refrain", "form", "formTempHP", "resistances", "shiftUses", "bufferReserve", "ordinaryTurnBudgets", "formSourceCounters"], "2026-10-30T10:00:19Z", "Druid Earth Warden Bonus Action; shapeshift clears remembered Refrain; no Mage spell cast")

for branch, start_state in [("NATURAL-EXPIRY", natural_start), ("MINDBLANK-CONDITIONAL", mb_start), ("ARCH-DISPEL-REMOVAL", dispel_start)]:
    add_transition("OP255-08-" + branch + "-T5-START", "target", branch, form, start_state, ["ordinaryTurnBudgets", "currentTargetTurn", "branch"], "2026-10-30T10:00:24Z", "Six-second target T5 START; reset target budgets before any :27 admission")
add_transition("OP255-09-HELPER-T2-END", "helper", "ARCH-DISPEL-REMOVAL", dispel_t2_start, dispel_t2_end, ["dissonance", "turnBudgets", "currentRegularTurn"], "2026-10-30T10:00:24Z", "Wizard helper T2 END; no spell/Weave, Let the Note Fall0→0")
add_transition("OP255-10-HELPER-T3-START", "helper", "ARCH-DISPEL-REMOVAL", dispel_t2_end, dispel_t3_start, ["turnBudgets", "currentRegularTurn"], "2026-10-30T10:00:24Z", "Wizard helper T3 START; Detect Magic concentration still active")
for branch, start_state, ui_state in [("NATURAL-EXPIRY", natural_start, ui_natural), ("MINDBLANK-CONDITIONAL", mb_start, ui_mb), ("ARCH-DISPEL-REMOVAL", dispel_start, ui_dis)]:
    add_transition("OP255-11-" + branch + "-UNRAVEL-ADMISSION", "target", branch, start_state, ui_state, ["classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "form", "formTempHP", "resistances", "concentration", "familiarCommandAvailable", "unravel", "equipment", "formSourceCounters"], "2026-10-30T10:00:27Z", "Return241 procedure plus director-approved spell-local UI251-FORM-LOSS; first future target regular END is :30")
add_transition("OP255-12-UNRAVEL-CASTER", "caster", "COMMON", u_before, u_after, ["RP", "turnBudgets", "castHistory", "castingFamilyHistory"], "2026-10-30T10:00:27Z", "Wizard17 rank9 Unravel; Action/RP26; first distinct prepared matrix family")
add_transition("OP255-13-MINDBLANK-CONDITIONAL-PROJECTION", "target", "MINDBLANK-CONDITIONAL", ui_mb, mb_suppressed, ["classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "resistances", "familiarCommandAvailable", "suppressionBranchStatus"], "2026-10-30T10:00:28Z", "Conditional callback projection only; no successful suppression or duration-backed interval asserted")
add_transition("OP255-14-MINDBLANK-CASTER", "caster", "MINDBLANK-CONDITIONAL", mb_before, mb_after, ["RP", "turnBudgets", "castHistory", "sourceEffect"], "2026-10-30T10:00:28Z", "Wizard17 rank8 Mind Blank; duration unresolved; no successful target suppression asserted")
add_transition("OP255-15-ARCH-DISPEL-USE", "helper", "ARCH-DISPEL-REMOVAL", dispel_t3_start, dispel_after_cast, ["RP", "turnBudgets", "recharge", "perception", "check", "refrain", "castHistory", "castingFamilyHistory"], "2026-10-30T10:00:28Z", "Always-prepared Wizard class matrix; Action3RP; sensed UI-01 at20ft within30ft, clear sight/no cover; 8+5+6=19 vs19")
add_transition("OP255-16-NATURAL-T5-DODGE", "target", "NATURAL-EXPIRY", ui_natural, natural_dodge, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:29Z", "Target Dodge Action; no spell or Weave ability")
add_transition("OP255-17-MINDBLANK-T5-DODGE", "target", "MINDBLANK-CONDITIONAL", mb_suppressed, mb_dodge, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:29Z", "Conditional branch target Dodge; no spell or Weave ability")
add_transition("OP255-18-ARCH-DISPEL-T5-DODGE", "target", "ARCH-DISPEL-REMOVAL", dispelled, dispel_dodge, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:29Z", "Target Dodge after successful UI-01 removal; no spell or Weave ability")
add_transition("OP255-19-NATURAL-T5-END", "target", "NATURAL-EXPIRY", natural_dodge, natural_end, ["dissonance", "classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "resistances", "familiarCommandAvailable", "unravel", "ordinaryTurnBudgets"], "2026-10-30T10:00:30Z", "First future target regular END; Let the Note Fall1→0; Unravel naturally ends")
add_transition("OP255-20-MINDBLANK-T5-END", "target", "MINDBLANK-CONDITIONAL", mb_dodge, mb_end, ["dissonance", "unravel", "ordinaryTurnBudgets", "suppressionBranchStatus"], "2026-10-30T10:00:30Z", "Conditional branch END; no successful Mind Blank suppression is counted; natural Unravel expiration")
add_transition("OP255-21-ARCH-DISPEL-T5-END", "target", "ARCH-DISPEL-REMOVAL", dispel_dodge, dispel_end, ["dissonance", "unravel", "ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:30Z", "Target END after UI-01 removal; Let the Note Fall1→0")
add_transition("OP255-22-HELPER-T3-END", "helper", "ARCH-DISPEL-REMOVAL", dispel_after_cast, dispel_t3_end, ["turnBudgets", "currentRegularTurn"], "2026-10-30T10:00:30Z", "Wizard helper T3 END; recharge remains2 until its next regular START")
add_transition("OP255-23-HELPER-T4-START-RECHARGE", "helper", "ARCH-DISPEL-REMOVAL", dispel_t3_end, dispel_after, ["turnBudgets", "recharge", "currentRegularTurn", "rechargeTickHistory"], "2026-10-30T10:00:30Z", "Wizard /engine/12: round recharge ticks at regular initiative START even if unable to act; 2→1")
for branch, owner_end, before_phase, after_phase in [
    ("NATURAL-EXPIRY", natural_end, ph_nat_before, ph_nat),
    ("MINDBLANK-CONDITIONAL", mb_end, ph_mb_before, ph_mb),
    ("ARCH-DISPEL-REMOVAL", dispel_end, ph_dis_before, ph_dis),
]:
    add_transition("OP255-24-" + branch + "-FAMILIAR-ATTACHED-PHASE", "familiar", branch, before_phase, after_phase, ["attachedPhase.resolution"], "2026-10-30T10:00:30.1Z", "CREATURE_LIFECYCLE_PLAYTEST.md: attached familiar phase only after the owner's whole T5 END at :30; complete before/after familiar and owner state")

replay = {
    "id": "UNRAVEL-IDENTITY-MD196-B02-FORWARD-INVERSE-REPLAY-255",
    "recordedAtUtc": "2026-10-30T12:34:00+00:00",
    "status": "SOURCE_BOUND_BRANCH_REPLAY_READY_FOR_DIRECTOR_RECHECK",
    "accepted": False,
    "applied": False,
    "planBinding": {"path": str(P.relative_to(W)).replace("\\", "/"), "bytes": P.stat().st_size, "sha256": hashlib.sha256(P.read_bytes()).hexdigest()},
    "initialFixture": {"postLongRestState": "commonTargetSnapshots.afterLongRest", "claimedRestTransition": False, "roundPeriodSeconds": 6},
    "commonTargetSnapshots": {
        "afterLongRest": base,
        "afterFamiliar": fam,
        "afterNoSpellVentT2": vent,
        "afterDetectMagic": dm,
        "afterEarthWardenShift": form,
        "afterTargetT5Start": target_t5_start,
        "afterUnravelAdmission": ui,
        "afterNaturalT5Start": natural_start,
        "afterNaturalT5Dodge": natural_dodge,
        "afterNaturalExpiry": natural_end,
        "afterMindBlankT5Start": mb_start,
        "afterMindBlankConditionalProjection": mb_suppressed,
        "afterMindBlankT5Dodge": mb_dodge,
        "afterMindBlankT5EndConditional": mb_end,
        "afterArchDispelT5Start": dispel_start,
        "afterArchDispelBeforeTargetDodge": dispelled,
        "afterArchDispelT5Dodge": dispel_dodge,
        "afterArchDispelT5End": dispel_end,
    },
    "branchTurnLedgers": {
        "NATURAL-EXPIRY": [
            {"time": "2026-10-30T10:00:24Z", "marker": "target T5 START; budgets reset", "transition": "OP255-08-NATURAL-EXPIRY-T5-START"},
            {"time": "2026-10-30T10:00:27Z", "marker": "UI-01 admitted; first future target END :30", "transition": "OP255-11-NATURAL-EXPIRY-UNRAVEL-ADMISSION"},
            {"time": "2026-10-30T10:00:29Z", "marker": "target Dodge Action"},
            {"time": "2026-10-30T10:00:30Z", "marker": "target T5 END; UI-01 expires; Dissonance1→0"},
            {"time": "2026-10-30T10:00:30.1Z", "marker": "familiar attached defensive phase after whole owner turn"},
        ],
        "MINDBLANK-CONDITIONAL": [
            {"time": "2026-10-30T10:00:24Z", "marker": "target T5 START; budgets reset", "transition": "OP255-08-MINDBLANK-CONDITIONAL-T5-START"},
            {"time": "2026-10-30T10:00:27Z", "marker": "UI-01 admitted; first future target END :30", "transition": "OP255-11-MINDBLANK-CONDITIONAL-UNRAVEL-ADMISSION"},
            {"time": "2026-10-30T10:00:28Z", "marker": "conditional projection only; no source-bound successful suppression"},
            {"time": "2026-10-30T10:00:29Z", "marker": "target Dodge Action"},
            {"time": "2026-10-30T10:00:30Z", "marker": "target T5 END; natural UI-01 expiry; Dissonance1→0"},
            {"time": "2026-10-30T10:00:30.1Z", "marker": "familiar attached defensive phase after whole owner turn"},
        ],
        "ARCH-DISPEL-REMOVAL": [
            {"time": "2026-10-30T10:00:24Z", "marker": "target T5 START; budgets reset", "transition": "OP255-08-ARCH-DISPEL-REMOVAL-T5-START"},
            {"time": "2026-10-30T10:00:27Z", "marker": "UI-01 admitted; first future target END :30", "transition": "OP255-11-ARCH-DISPEL-REMOVAL-UNRAVEL-ADMISSION"},
            {"time": "2026-10-30T10:00:28Z", "marker": "Arch Dispel ends UI-01; class/command availability returns"},
            {"time": "2026-10-30T10:00:29Z", "marker": "target Dodge Action"},
            {"time": "2026-10-30T10:00:30Z", "marker": "target T5 END; Dissonance1→0"},
            {"time": "2026-10-30T10:00:30.1Z", "marker": "familiar attached defensive phase after whole owner turn"},
        ],
    },
    "familiarAttachedPhases": {
        "naturalExpiry": {"before": ph_nat_before, "after": ph_nat},
        "mindBlankConditional": {"before": ph_mb_before, "after": ph_mb},
        "archDispel": {"before": ph_dis_before, "after": ph_dis},
    },
    "casterSnapshots": {
        "unravelBefore": u_before, "unravelAfter": u_after,
        "mindBlankBefore": mb_before, "mindBlankAfter": mb_after,
        "dispelBefore": dispel_before, "dispelAfterDetectMagic": dispel_sensed,
        "dispelAfterArchDispelCast": dispel_after_cast, "dispelAfterArchDispelT3End": dispel_t3_end,
        "dispelAfterArchDispel": dispel_after,
    },
    "helperRegularTurnLedger": [
        {"turn": "AD-T1", "start": "2026-10-30T10:00:12Z", "action": "prepared Detect Magic Action at :13 for2RP", "end": "2026-10-30T10:00:18Z", "refrainAfter": {"repeatCount": 0, "lastSpell": "wizard.base.detect-magic"}, "castingFamilies": ["detect-magic prepared matrix family"]},
        {"turn": "AD-T2", "start": "2026-10-30T10:00:18Z", "action": "none; no spell/Weave", "end": "2026-10-30T10:00:24Z", "dissonance": "0→0", "refrainPreserved": True, "castingFamiliesPreserved": True},
        {"turn": "AD-T3", "start": "2026-10-30T10:00:24Z", "action": "always-prepared wizard.arch.dispel-magic Action at :28 for3RP; recharge2", "end": "2026-10-30T10:00:30Z", "refrainAfter": {"repeatCount": 0, "lastSpell": "wizard.arch.dispel-magic"}, "castingFamilies": ["detect-magic prepared matrix family", "wizard.arch.dispel-magic always-prepared Wizard class matrix family"]},
        {"turn": "AD-T4", "start": "2026-10-30T10:00:30Z", "action": "Action/Bonus/Reaction budgets reset; Arch Dispel recharge ticks2→1", "rechargeSource": "wizard.json /engine/12", "rechargeAfter": 1},
    ],
    "helperRegularTurnSnapshots": {"T1Start": dispel_before, "T1AfterDetectMagic": dispel_sensed, "T1End": dispel_t1_end, "T2Start": dispel_t2_start, "T2End": dispel_t2_end, "T3Start": dispel_t3_start, "T3AfterArchDispel": dispel_after_cast, "T3End": dispel_t3_end, "T4StartAfterRechargeTick": dispel_after},
    "forwardInverseTransitions": transitions,
    "coverage": {
        "naturalExpiry": "Complete: target T5 START :24, admission :27, Dodge :29, first future END :30; Dissonance1→0 at END; full familiar phase :30.1 after whole owner turn.",
        "mindBlank": "Conditional only. Duration source is not bound; no successful suppression is asserted or counted. The conditional projection restores class/command markers only for analysis and grants no familiar order or activity.",
        "archDispel": "Complete source-qualified removal test: always-prepared wizard.arch.dispel-magic is outside the daily prepared-slot count; helper's prepared Detect Magic observes the unique UI-01 aura at20ft within30ft with clear sight/no cover. Helper T1–T4 schedule, cast families/Refrain history, T3 END, and T4 START recharge2→1 are recorded.",
        "letTheNoteFall": "Explicit cadence: target T2 no-spell turn vents1→0; T3 Detect Magic adds1; T4 shapeshift changes the body sounding the Weave and prevents vent; T5 no-spell Dodge vents1→0 at END :30. No RP/HP/reserve/rest/per-rest refill.",
        "formLoss": "Successful Unravel admission at :27 ends Earth Warden/tempHP30/physical resistance/attacks once. Mage Fire resistance is unavailable during class loss. DM-01 ends terminally; the first future target regular END is :30.",
        "familiar": "Every branch carries a complete familiar before/after snapshot: identity, HP14/14, AC18, speed30, creation-fixed Fire resistance, creation/use/deadline, position, order and command history, plus owner class/proficiency/command, UI and resistance state. Attached defensive phase is at :30.1 after owner T5 END :30; no generic Action/Bonus/Reaction budgets or independent turn are assigned.",
        "earthWardenAttack": "Base claw, Circle Forms first-hit S rider and Primal Strike magical-defense modifier are separate. Earth Slam recharge length2/current0; counter survives form loss.",
        "removedArcaneMissile": "No Arcane Missile is cast; no target, attack, damage, Action, or RP event is part of this witness.",
        "existingCases": "Return241 cases unchanged; only a new static witness/replay is authored.",
    },
    "qualification": "Static source-qualified data replay; no runtime or campaign execution claim. Mind Blank remains conditional and no identity acceptance/application/canonical change is asserted.",
}
OUT.write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raw = OUT.read_bytes()
print(json.dumps({"path": str(OUT), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}", "transitionCount": len(transitions), "transitionIds": [x["id"] for x in transitions]}, ensure_ascii=False, indent=2))
