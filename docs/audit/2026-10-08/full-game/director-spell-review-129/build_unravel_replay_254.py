import copy
import hashlib
import json
import pathlib
import zlib

W = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
B = W / "docs/audit/2026-10-08/full-game/director-spell-review-129"
P = B / "UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_254.json"
OUT = B / "UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_254.json"
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
    "sharedRP": {"current": 40, "max": 46},
    "dissonance": {"current": 2, "limit": 12},
    "refrain": {"repeatCount": 0, "lastSpell": "mage.base.arcane-missile"},
    "nukeChain": [],
    "form": {
        "id": "FORM-EW-01", "source": "druid.arch.earth-warden-dire-bear",
        "started": "2026-10-30T10:00:20Z", "ordinaryDeadline": "2026-10-30T10:10:20Z",
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
    "ordinaryTurnBudgets": {"Action": "spent: Mage Arcane Missile", "BonusAction": "spent: Earth Warden shift", "Reaction": "available then turn ended"},
    "equipment": {"woodenDruidicFocusStaff": "owned; melded/inaccessible", "commonClothes": "owned; melded/inaccessible", "coin": "74gp 5sp"},
    "currentTargetTurn": "T4 starts10:00:18Z; Arcane Missile Action10:00:19Z; shift Bonus Action10:00:20Z; T4 END10:00:24Z",
    "formSourceCounters": {"earthSlam": {"printedRechargeRounds": 2, "remainingRounds": 0, "used": False, "persistsAcrossFormLoss": True}},
})

ui = copy.deepcopy(form)
ui.update({
    "classAvailability": {"Druid": False, "Mage": False},
    "classDerivedProficiencyAvailable": False,
    "subjectiveBelief": {"text": "I am Rowan Vale, a traveling herbalist.", "endMarker": "first future target regular END10:00:36Z", "autonomous": True},
    "form": None, "formTempHP": 0, "rootAnatomy": True, "AC": 12,
    "resistances": [], "concentration": None, "familiarCommandAvailable": False,
    "equipment": {"woodenDruidicFocusStaff": "owned; returned to root right hand", "commonClothes": "owned; worn on root anatomy", "coin": "74gp 5sp"},
    "ordinaryTurnBudgets": {"Action": "T5 not started; ready at scheduled START10:00:30Z", "BonusAction": "T5 not started; ready at scheduled START10:00:30Z", "Reaction": "T5 not started; ready at scheduled START10:00:30Z"},
    "currentTargetTurn": "T4 ended10:00:24Z; T5 starts10:00:30Z; first future target END10:00:36Z",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:36Z", "classLoss": "active", "belief": "active", "initialSave": "none", "concentration": False, "formLossRule": "approved Unravel-only NEW UI251-FORM-LOSS"},
    "formSourceCounters": {"earthSlam": {"printedRechargeRounds": 2, "remainingRounds": 0, "used": False, "persistsAcrossFormLoss": True}},
})

# Natural-end branch target turn states.
natural_start = copy.deepcopy(ui)
natural_start["ordinaryTurnBudgets"] = {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}
natural_start["currentTargetTurn"] = "T5 START10:00:30Z; class loss active"
natural_dodge = copy.deepcopy(natural_start)
natural_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge", "BonusAction": "ready", "Reaction": "ready"}
natural_dodge["currentTargetTurn"] = "T5 Action Dodge10:00:31Z; end scheduled10:00:36Z"
natural_end = copy.deepcopy(natural_dodge)
natural_end.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": None,
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored with Mage availability"}],
    "familiarCommandAvailable": True,
    "dissonance": {"current": 1, "limit": 12},
    "ordinaryTurnBudgets": {"Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"},
    "currentTargetTurn": "T5 END10:00:36Z; Let the Note Fall2→1; Unravel naturally ended",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:36Z", "classLoss": "ended at first future target END", "belief": "ended at first future target END", "initialSave": "none", "concentration": False, "formLossRule": "approved Unravel-only NEW UI251-FORM-LOSS"},
})

# Hypothetical callback state is explicitly conditional and not accepted as a successful spell witness.
mb_suppressed = copy.deepcopy(ui)
mb_suppressed.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": {"text": "I am Rowan Vale, a traveling herbalist.", "status": "suppressed; conditional only"},
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored only if a bound Mind Blank duration legally suppresses class loss"}],
    "familiarCommandAvailable": True,
    "ordinaryTurnBudgets": {"Action": "not started; ready at10:00:30Z", "BonusAction": "not started; ready at10:00:30Z", "Reaction": "not started; ready at10:00:30Z"},
    "suppressionBranchStatus": "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS; operative duration unbound",
    "currentTargetTurn": "hypothetical class restoration before T5; no order/action/HP/deadline/refresh granted",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:36Z", "classLoss": "hypothetically suppressed/live if exact accepted duration supports it", "belief": "hypothetically suppressed/live if exact accepted duration supports it", "initialSave": "none", "concentration": False},
})
mb_start = copy.deepcopy(mb_suppressed)
mb_start["ordinaryTurnBudgets"] = {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}
mb_start["currentTargetTurn"] = "conditional T5 START10:00:30Z; no successful interval asserted"
mb_dodge = copy.deepcopy(mb_start)
mb_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge", "BonusAction": "ready", "Reaction": "ready"}
mb_dodge["currentTargetTurn"] = "conditional T5 Action Dodge10:00:31Z"
mb_end = copy.deepcopy(natural_end)
mb_end["suppressionBranchStatus"] = "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS"
mb_end["currentTargetTurn"] = "conditional branch reaches target END10:00:36Z; UI naturally expires; Dissonance2→1"

# Dispel branch ends the exact instance before target T5, without recreating form/concentration.
dispelled = copy.deepcopy(ui)
dispelled.update({
    "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True,
    "subjectiveBelief": None,
    "resistances": [{"source": "mage.base.elemental-affinity", "type": "fire", "status": "restored with Mage availability"}],
    "familiarCommandAvailable": True,
    "ordinaryTurnBudgets": {"Action": "T5 not started; ready at scheduled START10:00:30Z", "BonusAction": "T5 not started; ready at scheduled START10:00:30Z", "Reaction": "T5 not started; ready at scheduled START10:00:30Z"},
    "currentTargetTurn": "Arch Dispel ended UI-01 at10:00:28Z before T5 START10:00:30Z",
    "unravel": {"id": "UI-01", "admitted": "2026-10-30T10:00:27Z", "endsAt": "2026-10-30T10:00:28Z", "classLoss": "ended by Arch Dispel at10:00:28Z", "belief": "ended by Arch Dispel at10:00:28Z", "initialSave": "none", "concentration": False},
})
dispel_start = copy.deepcopy(dispelled)
dispel_start["ordinaryTurnBudgets"] = {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}
dispel_start["currentTargetTurn"] = "T5 START10:00:30Z; Unravel already ended by Arch Dispel"
dispel_dodge = copy.deepcopy(dispel_start)
dispel_dodge["ordinaryTurnBudgets"] = {"Action": "spent: Dodge", "BonusAction": "ready", "Reaction": "ready"}
dispel_dodge["currentTargetTurn"] = "T5 Action Dodge10:00:31Z"
dispel_end = copy.deepcopy(natural_end)
dispel_end["unravel"]["endsAt"] = "2026-10-30T10:00:28Z"
dispel_end["unravel"]["classLoss"] = "ended by Arch Dispel at10:00:28Z"
dispel_end["unravel"]["belief"] = "ended by Arch Dispel at10:00:28Z"
dispel_end["currentTargetTurn"] = "T5 END10:00:36Z after Arch Dispel removal; Let the Note Fall2→1"


def familiar_phase(owner_class_loss, owner_command, branch):
    return {
        "actor": "FAM-FIRE-01", "branch": branch,
        "time": "2026-10-30T10:00:33Z", "targetTurnStart": "2026-10-30T10:00:30Z",
        "source": "CREATURE_LIFECYCLE_PLAYTEST.md, At the table; mage.arch.conjure-elemental-familiar",
        "HP": {"current": 14, "max": 14}, "AC": 18, "identity": "Fire", "fireResistance": True,
        "created": "2026-10-30T10:00:01Z", "deadline": "2026-10-30T10:10:01Z",
        "ownerClassAvailability": {"Druid": not owner_class_loss, "Mage": not owner_class_loss},
        "ownerCommandPermission": owner_command, "pendingOrder": None,
        "phase": "moves and Dodges defensively; no independent damage/control",
        "turnBudgets": {"Action": "spent: Dodge", "BonusAction": "available", "Reaction": "available"},
    }


ph_nat = familiar_phase(True, False, "NATURAL-EXPIRY")
ph_mb = familiar_phase(False, True, "MINDBLANK-CONDITIONAL") | {"qualification": "Conditional only; no successful suppression duration established."}
ph_dis = familiar_phase(False, True, "ARCH-DISPEL-REMOVAL")

# Caster profiles retain independent pools, turn budgets, casting families and concentrations.
u_before = {"actor": "WITNESS-UNRAVEL-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "spell": "unravel-identity rank9", "prepared": True, "focus": "Illusion left hand", "rightHand": "free", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": None, "castingFamilyHistory": []}
u_after = copy.deepcopy(u_before)
u_after.update({"RP": {"current": 38, "max": 64}, "turnBudgets": {"Action": "spent: Unravel Identity", "BonusAction": "ready", "Reaction": "ready"}, "castHistory": [{"time": "2026-10-30T10:00:27Z", "Action": "paid", "RP": 26, "Dissonance": 0, "family": "first distinct prepared Wizard matrix family"}], "castingFamilyHistory": ["unravel-identity first prepared matrix family"], "targetPositionFt": [0, 0, 0], "targetRegularEnd": "2026-10-30T10:00:36Z"})

mb_before = {"actor": "WITNESS-MINDBLANK-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "prepared": "mind-blank rank8", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": {"duration": "not established", "deadline": None, "status": "unknown"}, "castingFamilyHistory": []}
mb_after = copy.deepcopy(mb_before)
mb_after.update({"RP": {"current": 43, "max": 64}, "turnBudgets": {"Action": "spent: Mind Blank", "BonusAction": "ready", "Reaction": "ready"}, "castHistory": [{"time": "2026-10-30T10:00:28Z", "Action": "paid", "RP": 21, "Dissonance": 0, "family": "first distinct prepared Wizard matrix family"}], "castingFamilyHistory": ["mind-blank first prepared matrix family"], "sourceEffect": {"status": "duration unresolved; not asserted to suppress UI-01", "requiredBinding": "rank8ward5_reviewed_149/MODEL.json /spells/3/procedure"}})

dispel_before = {"actor": "WITNESS-ARCH-DISPEL-WIZARD17", "WizardLevel": 17, "HP": "104/104", "RP": {"current": 64, "max": 64}, "dissonance": {"current": 0, "limit": 13}, "prepared": "detect-magic rank1", "archDispel": "wizard.arch.dispel-magic acquired W5", "turnBudgets": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "concentration": None, "recharge": {"ArchDispel": 0}, "castingFamilyHistory": []}
dispel_sensed = copy.deepcopy(dispel_before)
dispel_sensed.update({"RP": {"current": 62, "max": 64}, "turnBudgets": {"Action": "spent: Detect Magic", "BonusAction": "ready", "Reaction": "ready"}, "concentration": {"source": "Wizard detect-magic rank1", "started": "2026-10-30T10:00:13Z", "deadline": "2026-10-30T10:10:13Z", "active": True}, "castHistory": [{"time": "2026-10-30T10:00:13Z", "Action": "paid", "RP": 2, "Dissonance": 0, "family": "first distinct prepared matrix family"}], "castingFamilyHistory": ["detect-magic first prepared matrix family"]})
dispel_after = copy.deepcopy(dispel_sensed)
dispel_after.update({"RP": {"current": 59, "max": 64}, "turnBudgets": {"Action": "spent: Arch Dispel", "BonusAction": "ready", "Reaction": "ready"}, "recharge": {"ArchDispel": 2}, "castHistory": dispel_sensed["castHistory"] + [{"time": "2026-10-30T10:00:28Z", "Action": "paid", "RP": 3, "Dissonance": 0, "selectedEffect": "UI-01 ongoing spell aura perceived at20ft before commitment", "family": "acquired class card, not prepared matrix"}], "perception": {"distanceFt": 20, "DetectMagicRangeFt": 30, "lineOfSight": "clear", "cover": "none", "activeAuraCountOnTarget": 1, "observedAt": "2026-10-30T10:00:27Z", "observation": "the unique ongoing spell aura on the target is UI-01; no other active spell aura is present"}, "check": {"roll": 8, "INT": 5, "PB": 6, "total": 19, "DC": 19, "result": "success"}})

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


# The first transition starts from a fully bound post-rest initial fixture. No rest event is claimed.
add_transition("OP254-01-FAMILIAR", "target", "COMMON", base, fam, ["sharedRP", "dissonance", "refrain", "conjureFamiliarUse", "familiar", "ordinaryTurnBudgets"], "2026-10-30T10:00:01Z", "mage.arch.conjure-elemental-familiar; source clock ten minutes")
add_transition("OP254-02-LET-NOTE-FALL-T2", "target", "COMMON", fam, vent, ["dissonance", "ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:12Z", "RESONANCE_CANON.md Let the Note Fall; T2 used no spell/Weave")
add_transition("OP254-03-DETECT-MAGIC", "target", "COMMON", vent, dm, ["sharedRP", "dissonance", "refrain", "concentration", "ordinaryTurnBudgets"], "2026-10-30T10:00:13Z", "mage.base.detect-magic Action, exact Mage class card cost1RP")
add_transition("OP254-04-ARCANE-MISSILE-AND-EARTH-WARDEN", "target", "COMMON", dm, form, ["sharedRP", "dissonance", "refrain", "form", "formTempHP", "resistances", "shiftUses", "bufferReserve", "ordinaryTurnBudgets", "formSourceCounters"], "2026-10-30T10:00:20Z", "mage.base.arcane-missile Action then Druid shift Bonus Action; Earth Warden, Circle Forms and Primal Strike source bindings")
add_transition("OP254-05-UNRAVEL-ADMISSION", "target", "COMMON", form, ui, ["classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "form", "formTempHP", "resistances", "concentration", "familiarCommandAvailable", "unravel", "equipment", "formSourceCounters"], "2026-10-30T10:00:27Z", "Return241 procedure plus director-approved Unravel-only UI251-FORM-LOSS")
add_transition("OP254-06-NATURAL-T5-START", "target", "NATURAL-EXPIRY", ui, natural_start, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:30Z", "first regular target START under active Unravel")
# Index 6 is intentionally the conditional suppression mirror: restored class means familiar command is true.
add_transition("OP254-07-MINDBLANK-CONDITIONAL-SUPPRESSION", "target", "MINDBLANK-CONDITIONAL", ui, mb_suppressed, ["classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "resistances", "familiarCommandAvailable", "suppressionBranchStatus"], "2026-10-30T10:00:28Z", "Hypothetical callback projection only; no accepted duration or successful suppression is claimed")
add_transition("OP254-08-ARCH-DISPEL-REMOVAL", "target", "ARCH-DISPEL-REMOVAL", ui, dispelled, ["classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "resistances", "familiarCommandAvailable", "unravel"], "2026-10-30T10:00:28Z", "wizard.arch.dispel-magic; unique UI-01 aura sensed within Detect Magic30ft, clear sight/no cover")

add_transition("OP254-09-NATURAL-T5-DODGE", "target", "NATURAL-EXPIRY", natural_start, natural_dodge, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:31Z", "ordinary Dodge Action; no spell or Weave ability")
add_transition("OP254-10-NATURAL-FAMILIAR-PHASE", "familiar", "NATURAL-EXPIRY", {"actor": "FAM-FIRE-01", "phase": "not yet resolved", "ownerCommandPermission": False}, ph_nat, ["phase", "turnBudgets", "ownerCommandPermission"], "2026-10-30T10:00:33Z", "Familiar's separate attached phase after target START; class-loss owner marker preserved")
add_transition("OP254-11-NATURAL-T5-END", "target", "NATURAL-EXPIRY", natural_dodge, natural_end, ["dissonance", "classAvailability", "classDerivedProficiencyAvailable", "subjectiveBelief", "resistances", "familiarCommandAvailable", "unravel", "ordinaryTurnBudgets"], "2026-10-30T10:00:36Z", "target END; Let the Note Fall2→1 and first-future-END Unravel natural expiry")

add_transition("OP254-12-MINDBLANK-T5-START", "target", "MINDBLANK-CONDITIONAL", mb_suppressed, mb_start, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:30Z", "Conditional only; no duration-backed success asserted")
add_transition("OP254-13-MINDBLANK-T5-DODGE", "target", "MINDBLANK-CONDITIONAL", mb_start, mb_dodge, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:31Z", "Conditional target Dodge; no spell/Weave")
add_transition("OP254-14-MINDBLANK-FAMILIAR-PHASE", "familiar", "MINDBLANK-CONDITIONAL", {"actor": "FAM-FIRE-01", "phase": "not yet resolved", "ownerCommandPermission": True}, ph_mb, ["phase", "turnBudgets", "ownerCommandPermission"], "2026-10-30T10:00:33Z", "Conditional familiar phase; restored permission grants no order/action/healing/refresh")
add_transition("OP254-15-MINDBLANK-T5-END", "target", "MINDBLANK-CONDITIONAL", mb_dodge, mb_end, ["dissonance", "unravel", "ordinaryTurnBudgets", "suppressionBranchStatus"], "2026-10-30T10:00:36Z", "Conditional branch reaches original target END; not counted without source-bound duration")

add_transition("OP254-16-ARCH-T5-START", "target", "ARCH-DISPEL-REMOVAL", dispelled, dispel_start, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:30Z", "target START after successful Arch Dispel removal")
add_transition("OP254-17-ARCH-T5-DODGE", "target", "ARCH-DISPEL-REMOVAL", dispel_start, dispel_dodge, ["ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:31Z", "ordinary target Dodge; no spell/Weave")
add_transition("OP254-18-ARCH-FAMILIAR-PHASE", "familiar", "ARCH-DISPEL-REMOVAL", {"actor": "FAM-FIRE-01", "phase": "not yet resolved", "ownerCommandPermission": True}, ph_dis, ["phase", "turnBudgets", "ownerCommandPermission"], "2026-10-30T10:00:33Z", "Familiar's separate attached phase after target START; Dispel restored owner availability only")
add_transition("OP254-19-ARCH-T5-END", "target", "ARCH-DISPEL-REMOVAL", dispel_dodge, dispel_end, ["dissonance", "ordinaryTurnBudgets", "currentTargetTurn"], "2026-10-30T10:00:36Z", "target END; Let the Note Fall2→1; UI-01 was already ended by Dispel")

add_transition("OP254-20-UNRAVEL-CASTER", "caster", "COMMON", u_before, u_after, ["RP", "turnBudgets", "castHistory", "castingFamilyHistory"], "2026-10-30T10:00:27Z", "Wizard17 rank9 Unravel; first distinct prepared matrix family")
add_transition("OP254-21-MINDBLANK-CASTER", "caster", "MINDBLANK-CONDITIONAL", mb_before, mb_after, ["RP", "turnBudgets", "castHistory", "sourceEffect"], "2026-10-30T10:00:28Z", "Wizard17 rank8 Mind Blank; effect duration unresolved; no target suppression assertion")
add_transition("OP254-22-DISPEL-SENSE", "caster", "ARCH-DISPEL-REMOVAL", dispel_before, dispel_sensed, ["RP", "turnBudgets", "concentration", "castHistory"], "2026-10-30T10:00:13Z", "Separate Wizard17 prepared Detect Magic rank1; 2RP and 10-minute concentration")
add_transition("OP254-23-DISPEL-USE", "caster", "ARCH-DISPEL-REMOVAL", dispel_sensed, dispel_after, ["RP", "turnBudgets", "recharge", "perception", "check", "castHistory"], "2026-10-30T10:00:28Z", "wizard.arch.dispel-magic; Action3RP, recharge2, roll8+INT5+PB6=19 vs DC19")

replay = {
    "id": "UNRAVEL-IDENTITY-MD196-B02-FORWARD-INVERSE-REPLAY-254",
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
        "afterEarthWarden": form,
        "afterUnravelAdmission": ui,
        "afterNaturalT5Start": natural_start,
        "afterNaturalT5Dodge": natural_dodge,
        "afterNaturalExpiry": natural_end,
        "afterMindBlankSuppressionBeforeEND": mb_suppressed,
        "afterMindBlankT5Start": mb_start,
        "afterMindBlankT5Dodge": mb_dodge,
        "afterMindBlankT5EndConditional": mb_end,
        "afterArchDispelBeforeTargetTurn": dispelled,
        "afterArchDispelT5Start": dispel_start,
        "afterArchDispelT5Dodge": dispel_dodge,
        "afterArchDispelT5End": dispel_end,
    },
    "familiarAttachedPhases": {"naturalExpiry": ph_nat, "mindBlankConditional": ph_mb, "archDispel": ph_dis},
    "casterSnapshots": {"unravelBefore": u_before, "unravelAfter": u_after, "mindBlankBefore": mb_before, "mindBlankAfter": mb_after, "dispelBefore": dispel_before, "dispelAfterDetectMagic": dispel_sensed, "dispelAfterArchDispel": dispel_after},
    "forwardInverseTransitions": transitions,
    "coverage": {
        "naturalExpiry": "Complete: target START/Dodge/familiar phase/END are separate; Dissonance2→1 at first future END.",
        "mindBlank": "Conditional only. Duration source is not bound, no successful interval is asserted or counted. Hypothetical restoration correctly restores familiar command permission and Elemental Affinity Fire resistance without granting an order or resetting anything.",
        "archDispel": "Complete source-qualified removal test: Detect Magic senses unique ongoing aura at20ft within30ft, clear LoS/no cover; Action3RP; recharge2; roll8+INT5+PB6=19 vs DC19. Separate target START/Dodge/familiar phase/END included.",
        "letTheNoteFall": "Explicit cadence: target T2 no-spell turn vents1→0; T3 and T4 contain spells; T5 no-spell Dodge vents2→1 at END. No RP/HP/reserve/rest/per-rest refill.",
        "formLoss": "Successful Unravel admission ends Earth Warden/tempHP30/physical resistance/attacks once. Mage Fire resistance is independently unavailable during class loss. DM-01 ends terminally.",
        "familiar": "Same Fire identity,14/14,AC18,creation-fixed resistance,use spent,deadline10:10:01. Owner command removed during class loss; separate companion phase appears10:00:33 after target START, no pending order or damage/control.",
        "earthWardenAttack": "Base claw, Circle Forms first-hit S rider and Primal Strike magical-defense modifier are separate. Earth Slam recharge length2/current0; counter survives form loss.",
        "existingCases": "Return241 cases unchanged; only a new static witness/replay is authored.",
    },
    "qualification": "Static source-qualified data replay; no runtime or campaign execution claim. Mind Blank remains conditional and no identity acceptance/application/canonical change is asserted.",
}
OUT.write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raw = OUT.read_bytes()
print(json.dumps({"path": str(OUT), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}", "transitionCount": len(transitions), "mindBlankMirrorIndex6": transitions[6]["id"], "mindBlankCommandAfter": transitions[6]["after"]["familiarCommandAvailable"]}, ensure_ascii=False, indent=2))
