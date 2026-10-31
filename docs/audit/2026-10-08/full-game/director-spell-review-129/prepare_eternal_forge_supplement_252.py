from __future__ import annotations

import copy
import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
SOURCE = ROOT / "ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_250.json"
OUTPUT = ROOT / "ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_252.json"

data = json.loads(SOURCE.read_text(encoding="utf-8"))
data["id"] = "ETERNAL-FORGE-MF210-B01-WITNESS-SUPPLEMENT-252"
data["recordedAtUtc"] = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
data["status"] = "DRAFT_WITH_FORWARD_INVERSE_REPLAY_AND_LOCAL_CONSISTENCY_AUDIT_DIRECTOR_REVIEW_REQUIRED"
data["authority"] = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0}
data["sourceDecision"]["summary"] = (
    "Fixture permission is director-authorized for one-case authored test inputs. This revision "
    "source-binds Warrior skills, declares a local initiative order, corrects source-case event "
    "timing, and adds finite stock/payment and reversible event records. No identity acceptance "
    "or canonical/application change."
)

actor = data["repairActor"]
actor["serumLoadout"]["preparedDoses"][0] = {
    "id": "warrior.supplement.overdrive",
    "chosenAbility": "STR",
    "chosenAt": "pre-case serum preparation after the prior fixture long rest",
    "choiceSource": "warrior.json /cards/66/effect: choose Strength or Dexterity on preparation",
}
actor["serumLoadout"]["preparationChoiceRecord"] = "Overdrive's STR choice is fixed before the encounter; it is not activated or consumed in this witness."
actor["skillProficiencies"] = ["Athletics", "Insight", "Intimidation", "Survival"]
actor["classSkillSelection"] = {
    "required": 2,
    "candidateSkills": ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"],
    "selectedSkills": ["Intimidation", "Survival"],
    "status": "SOURCE_BOUND_COMPLETE",
    "qualification": (
        "Warrior list in CHARACTER_FOUNDATION_TABLES.md; Athletics is already granted by the "
        "selected background, so this selectable class grant uses two other legal options."
    ),
    "source": {
        "path": "DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md",
        "selectionRule": "Warrior choose 2 from Animal Handling, Athletics, Intimidation, Nature, Perception, Survival.",
    },
}
actor["sourceRefs"] = list(dict.fromkeys(actor.get("sourceRefs", []) + [
    "DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md"
]))
actor["level1Schedule"]["automaticAtLevel1"] = ["Mutation Slot I", "Brutality Threshold tracker"]
actor["level1Schedule"]["fourChoices"] = {
    "active": ["warrior.base.serum-injection", "warrior.base.brutal-strike"],
    "passive": ["warrior.base.serum-tolerance", "warrior.base.combat-instinct"],
    "minimumActiveSatisfied": True,
}
actor["classFeaturesUsedInWitness"] = [
    "warrior.base.combat-instinct (+1 initiative)",
    "Mountain Dwarf selected Smith's-tools proficiency (repair checks)",
]
actor["classFeaturesNotUsedInWitness"] = [
    "warrior.base.serum-injection",
    "warrior.base.brutal-strike",
    "warrior.base.serum-tolerance",
    "warrior.supplement.ironhide-graft",
    "prepared serum doses",
    "Brutality Threshold tracker",
    "Mutation Recovery Reserve",
]
actor["classProficiencies"] = {
    "savingThrows": ["Strength", "Constitution"],
    "armor": ["Medium", "Heavy"],
    "weapons": ["Martial weapons"],
    "tools": [],
    "classSkills": ["Intimidation", "Survival"],
    "backgroundSkills": ["Athletics", "Insight"],
    "backgroundTools": ["dice gaming set", "Vehicles (Land)"],
    "ancestrySkills": [],
    "ancestryTools": ["Smith's tools"],
    "ancestryWeapons": ["battleaxe", "handaxe", "light hammer", "warhammer"],
    "ancestryArmor": ["Light", "Medium"],
}
actor["body"] = {
    "size": "Medium",
    "movementFeet": 25,
    "handsAtFixtureEntry": {"left": None, "right": None},
    "conditions": [],
    "carriedWeightLb": 9,
    "carryingCapacityLb": 180,
    "equipment": "Only the two documented wealth purchases; no starting-package gear also granted.",
}
actor["armorClass"] = {
    "base": 10, "dexterityModifier": 2, "armorBonus": 0, "shieldBonus": 0, "total": 12,
    "basis": "No armor or shield purchased on the wealth route.",
}
actor["priorRestFixture"] = {
    "kind": "authored-static-actor-initialization",
    "completedLongRestBeforeScenario": True,
    "time": "pre-case; not campaign chronology",
    "effects": ["mutation slot loadout may be equipped", "two serum doses prepared", "Strain 0", "Mutation Recovery Reserve 4"],
}
actor["startingWealth"]["sourceRef"] = "DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md"
actor["startingWealth"]["diceInputStatus"] = "authored static test input; 2d4 Warrior result, not Wizard wealth"

for transaction, paid in zip(data["acquisitions"]["transactions"], [2000, 2500]):
    transaction.update({"paidCp": paid, "tenderCp": paid, "changeReturnedCp": 0, "timeSeconds": 6.2})
data["acquisitions"]["repairMaterialLots"] = {
    "priceBasis": (
        "Source repair procedure: 25% of Standard mundane base reference for functioning repair; "
        "25% of undamaged finished per-item reference for HP0 reconstruction."
    ),
    "functionalRepairEachGp": 3.75,
    "functionalRepairEachCp": 375,
    "reconstructionGp": 26.75,
    "reconstructionCp": 2675,
    "physicalInput": "A separately identified finite lot of compatible repair material; no invented composition, mass or ingredient recipe.",
}
data["acquisitions"]["fixtureSupply"] = {
    "seller": "WH250-01-OPERATOR",
    "scope": "Synthetic finite stock for this one-case test fixture only; no canonical market or universal inventory.",
    "commonItems": [
        {
            "stockId": "WH250-01-STOCK-TOOLS", "itemId": "tools.smith-s-tools", "quantity": 1,
            "ownerBeforeSale": "WH250-01-OPERATOR", "custodyBeforeSale": "WH250-01-supply-bin",
            "priceCp": 2000, "soldAtSeconds": 6.2,
        },
        {
            "stockId": "WH250-01-STOCK-ACID", "itemId": "adventuring-gear.acid-vial", "quantity": 1,
            "ownerBeforeSale": "WH250-01-OPERATOR", "custodyBeforeSale": "WH250-01-supply-bin",
            "priceCp": 2500, "soldAtSeconds": 6.2,
        },
    ],
    "repairLots": [],
    "changeReserveCp": 125,
    "changePolicy": (
        "Each 3.75 gp or 26.75 gp transaction tenders the next whole-gp amount and returns 25 cp; "
        "the fixture owner has a finite 125 cp change reserve at the branch base."
    ),
}
lot_specs = [
    ("MF251-RM-01", "functioning-item-repair", 375, "MF251-W1-FUNCTIONAL-REPAIR-SUCCESS"),
    ("MF251-RM-02A", "functioning-item-repair", 375, "MF251-W1-REPAIR-FAIL-THEN-SUCCESS / attempt 1"),
    ("MF251-RM-02B", "functioning-item-repair", 375, "MF251-W1-REPAIR-FAIL-THEN-SUCCESS / attempt 2"),
    ("MF251-RM-03S", "hp0-reconstruction", 2675, "MF251-W1-ZERO-HP-RECONSTRUCTION-SUCCESS"),
    ("MF251-RM-03F", "hp0-reconstruction", 2675, "MF251-W1-ZERO-HP-RECONSTRUCTION-FAILURE"),
]
for lot_id, mode, cost, branch in lot_specs:
    data["acquisitions"]["fixtureSupply"]["repairLots"].append({
        "lotId": lot_id,
        "quantity": 1,
        "mode": mode,
        "compatibleItemId": "sword-1",
        "model": "Standard longsword",
        "ownerBeforeSale": "WH250-01-OPERATOR",
        "custodyBeforeSale": "WH250-01-material-bin",
        "priceCp": cost,
        "priceGp": cost / 100,
        "sourcePriceBound": True,
        "availableAtSeconds": 6.2,
        "branchUse": branch,
        "mass": "unspecified; remains in station custody; no carried mass asserted",
        "ingredientRecipe": "none asserted",
    })
data["worksite"]["availability"] = (
    "Continuous from t=6.2 through the longest alternative branch ending at t=28812.3; "
    "operator and explicit owner permission remain available through the two-attempt retry branch. "
    "No quantified fuel cost."
)
data["worksite"]["permissionRecord"].update({
    "task": (
        "One acid-vial test attack, followed by zero repair attempts on a miss, one attempt in each "
        "single-attempt branch, or two attempts only in the retry branch."
    ),
    "availableThroughRetry": True,
    "terms": (
        "One-case free station access; owner A expressly consents; operator expressly authorizes "
        "the named repairer and the stated test/repair task; no general entitlement."
    ),
})
data["worksite"]["materialStock"] = {
    "finiteLots": data["acquisitions"]["fixtureSupply"]["repairLots"],
    "changeReserveCp": 125,
    "stockOwner": "WH250-01-OPERATOR",
    "status": "local fixture inventory only",
}
data["worksite"]["bench"]["status"] = (
    "Supported, stable, visible work surface. Separate from the Forge/Anvil/Tongs; same source scene."
)

# The source case's free interaction and weapon attack each occupy a 0.1-second event step.
data["timeline"]["fixtureStart"]["timeSeconds"] = 12.0
data["timeline"]["placement"]["timeSeconds"] = 12.0
data["timeline"]["placement"]["endSeconds"] = 12.1
data["timeline"]["acidAction"] = {
    "actor": "MF250-DWARF-WARRIOR1",
    "turnSlotStartSeconds": 12.1,
    "timeSeconds": 12.1,
    "endSeconds": 12.2,
    "durationSeconds": 0.1,
    "action": "Action",
    "attackType": "20-foot ranged improvised attack per acid-vial procedure",
    "actualTargetDistanceFeet": 5,
    "maximumRangeFeet": 20,
    "target": "sword-1 unattended at AC19",
    "DEX": 14,
    "DEXModifier": 2,
    "applicableImprovisedAttackProficiency": False,
    "PBAdded": 0,
    "attackRollsByBranch": {
        "miss": {"d20": 16, "total": 18, "hit": False},
        "hitBranches": {"d20": 17, "total": 19, "hit": True},
    },
    "damageDiceByBranch": {"threeDamageBranches": [1, 2], "fiveDamageBranches": [2, 3]},
    "acidDamageByBranch": {"miss": 0, "threeDamage": 3, "fiveDamage": 5},
    "vialConsumedOnHitOrMiss": True,
    "postUseCarriedWeightLb": 8,
    "emptyContainerCustody": "WH250-01-empty-vial-bin; retained by fixture, not carried",
    "lineOfEffect": "unblocked",
    "noHostileCreatureWithin5Feet": "authored static scene input; no ranged-attack disadvantage from an adjacent hostile creature",
}
data["timeline"]["initiativeExit"] = {
    "startSeconds": 12.2,
    "endSeconds": 12.3,
    "condition": "The bounded authored test encounter ends after B passes its slot; the local test fixture states no active threat remains.",
    "type": "local authored encounter fact only",
    "effect": "Leave initiative before any repair hours; preserve all participant positions, HP and unspent actions; no rest, relocation or free action is created.",
}
data["timeline"]["workClocks"] = {
    "commonStartingTimeSeconds": 12.3,
    "functioningRepair": {"startSeconds": 12.3, "activeSeconds": 3600, "endSeconds": 3612.3, "nonoverlapAttested": True},
    "repairRetry": {
        "attempt1StartSeconds": 12.3, "attempt1ActiveSeconds": 3600, "attempt1EndSeconds": 3612.3,
        "attempt2StartSeconds": 3612.3, "attempt2ActiveSeconds": 3600, "attempt2EndSeconds": 7212.3,
        "freshMaterialLotRequired": True, "nonoverlapAttested": True,
    },
    "reconstruction": {"startSeconds": 12.3, "activeSeconds": 28800, "endSeconds": 28812.3, "nonoverlapAttested": True},
    "rest": "No short or long rest occurs during any branch.",
}
data["timeline"]["lineageInvariant"] = (
    "Throughout each branch owner=A, itemId=sword-1, recipe=recipe-42, origin/castF1 root and "
    "provenance=[castF1]. Item HP/custody/operational state and finite fixture transactions are "
    "the only item lifecycle changes; the castF1 source record remains resolved, active and "
    "unsuppressed (Core duration: until dispelled)."
)
turns = {
    "scheduledStartSeconds": 12.0,
    "order": ["A", "MF250-DWARF-WARRIOR1", "B"],
    "initiativeRolls": [
        {"actor": "A", "d20": 18, "DEXModifier": 2, "otherModifier": 0, "total": 20},
        {"actor": "MF250-DWARF-WARRIOR1", "d20": 12, "DEXModifier": 2, "warrior.base.combat-instinct": 1, "total": 15},
        {"actor": "B", "d20": 8, "DEXModifier": 2, "otherModifier": 0, "total": 10},
    ],
    "status": "explicit local fixture order input, confirmed by declared test initiative dice; not a campaign or universal order claim",
    "AFreeInteraction": "reset at A's actual start; A places sword-1 on supported bench at 12.0-12.1; consumes that free interaction.",
    "repairerAction": "C's own initiative slot begins at 12.1; the Action is available because C's own start was processed at 12.0.",
    "BState": "B receives its actual start, remains at HP98/104, passes without spending Action/Reaction/Bonus Action or moving; its slot is recorded at 12.2-12.3.",
    "sourceBasis": "MF210-F01 events 4 and 5 each use 0.1-second event steps; the continuation uses the same event-step scale.",
}
data["timeline"]["turnScheduleAt12"] = turns
data["timeline"]["continuation"]["repairerInsertion"] = {
    "id": "MF250-DWARF-WARRIOR1",
    "timeSeconds": 6.2,
    "positionFeet": [0, 12, 0],
    "status": "new authored witness actor input; not retroactively added to MF210-F01",
    "attackDistanceFeet": "5 feet to closest supported-bench surface; within 20-foot maximum range",
    "lineOfEffect": "unblocked",
}
data["timeline"]["continuation"]["turnScheduleAt12"] = turns
data["timeline"]["continuation"]["fixtureLocation"] = "same MF210-isolated-scene; no actor or sword relocation and no travel time"
data["timeline"]["continuation"]["noTravel"] = {"distanceFeet": 0, "elapsedSeconds": 0, "basis": "one-case worksite fixture at the prior case scene"}
data["timeline"]["continuation"]["initiativeEndsAtSeconds"] = 12.3

cases = []
for case in data["witnessCases"]:
    case["id"] = case["id"].replace("MF250-", "MF251-")
    case["qualification"] = (
        "One-case authored fixture input; not campaign fact. Owner, item identity, cast root, "
        "finite transaction, roll and alternative timeline are independently recorded."
    )
    case["timeline"]["acidAttackStartSeconds"] = 12.1
    case["timeline"]["acidAttackCompleteSeconds"] = 12.2
    case["timeline"]["initiativeExitSeconds"] = 12.3
    case["swordCustody"] = "WH250-01-workbench"
    case["owner"] = "A"
    case["castRoot"] = "castF1"
    case["transactions"]["openingCp"] = 3500
    case["transactions"]["balanceBasis"] = (
        "This alternative starts after one-time Warrior wealth purchases: 8000 cp minus 2000 cp "
        "Smith's tools minus 2500 cp acid vial = 3500 cp. Branches fork from the same state and "
        "do not share expenditures."
    )
    if case["id"].endswith("ACID-MISS"):
        case["transactions"]["closingCp"] = 3500
        case["timeline"].update({"repairWork": None, "custody": "WH250-01-workbench", "branchEndSeconds": 12.3})
        case["swordHP"]["final"] = 5
        case["materialLots"] = []
        final_hp = 5
    elif case["id"].endswith("FUNCTIONAL-REPAIR-SUCCESS"):
        case["repair"]["checkTotal"] = 10
        case["repair"]["naturalShiftApplied"] = False
        case["repair"]["toolProficiencyAppliedOnce"] = True
        case["transactions"]["closingCp"] = 3125
        case["transactions"]["repairStockPurchasedCp"] = 375
        case["transactions"]["repairStock"] = [{
            "lotId": "MF251-RM-01", "mode": "functioning-item-repair",
            "ownerBeforeSale": "WH250-01-OPERATOR", "buyer": "MF250-DWARF-WARRIOR1",
            "custody": "station bin; owned by buyer and reserved for attempt until completion",
            "reservationId": "MF251-W1-FUNCTIONAL-REPAIR-SUCCESS:ATTEMPT-1",
            "consumedAtSeconds": 3612.3, "priceCp": 375, "tenderCp": 400,
            "changeReturnedCp": 25, "sellerReceiptCp": 375, "consumedOnSuccess": True,
        }]
        case["transactions"]["closingGp"] = 31.25
        case["timeline"].update({"repairStartSeconds": 12.3, "repairCompleteSeconds": 3612.3, "branchEndSeconds": 3612.3})
        case["materialLots"] = ["MF251-RM-01"]
        final_hp = 5
    elif case["id"].endswith("REPAIR-FAIL-THEN-SUCCESS"):
        for attempt in case["attempts"]:
            attempt["checkTotal"] = attempt["total"]
            attempt["naturalShiftApplied"] = False
            attempt["toolProficiencyAppliedOnce"] = True
        case["transactions"]["closingCp"] = 2750
        case["transactions"]["repairStockPurchasedCp"] = 750
        case["transactions"]["repairStock"] = [
            {
                "lotId": "MF251-RM-02A", "mode": "functioning-item-repair",
                "ownerBeforeSale": "WH250-01-OPERATOR", "buyer": "MF250-DWARF-WARRIOR1",
                "custody": "station bin; owned by buyer and reserved for attempt until completion",
                "reservationId": "MF251-W1-REPAIR-FAIL-THEN-SUCCESS:ATTEMPT-1",
                "consumedAtSeconds": 3612.3, "priceCp": 375, "tenderCp": 400,
                "changeReturnedCp": 25, "sellerReceiptCp": 375, "consumedOnFailure": True,
            },
            {
                "lotId": "MF251-RM-02B", "mode": "functioning-item-repair",
                "ownerBeforeSale": "WH250-01-OPERATOR", "buyer": "MF250-DWARF-WARRIOR1",
                "custody": "station bin; owned by buyer and reserved for retry until completion",
                "reservationId": "MF251-W1-REPAIR-FAIL-THEN-SUCCESS:ATTEMPT-2",
                "consumedAtSeconds": 7212.3, "priceCp": 375, "tenderCp": 400,
                "changeReturnedCp": 25, "sellerReceiptCp": 375, "consumedOnSuccess": True,
            },
        ]
        case["transactions"]["closingGp"] = 27.5
        case["timeline"].update({
            "failedRepairStartSeconds": 12.3, "failedRepairCompleteSeconds": 3612.3,
            "retryStartSeconds": 3612.3, "retryCompleteSeconds": 7212.3, "branchEndSeconds": 7212.3,
        })
        case["materialLots"] = ["MF251-RM-02A", "MF251-RM-02B"]
        final_hp = 5
    else:
        case["repair"]["checkTotal"] = case["repair"]["total"]
        case["repair"]["naturalShiftApplied"] = False
        case["repair"]["toolProficiencyAppliedOnce"] = True
        is_success = case["id"].endswith("RECONSTRUCTION-SUCCESS")
        lot = "MF251-RM-03S" if is_success else "MF251-RM-03F"
        case["transactions"]["closingCp"] = 825
        case["transactions"]["repairStockPurchasedCp"] = 2675
        case["transactions"]["closingGp"] = 8.25
        sale = {
            "lotId": lot, "mode": "hp0-reconstruction",
            "ownerBeforeSale": "WH250-01-OPERATOR", "buyer": "MF250-DWARF-WARRIOR1",
            "custody": "station bin; owned by buyer and reserved for reconstruction until completion",
            "reservationId": case["id"] + ":ATTEMPT-1", "consumedAtSeconds": 28812.3,
            "priceCp": 2675, "tenderCp": 2700, "changeReturnedCp": 25, "sellerReceiptCp": 2675,
        }
        sale["consumedOnSuccess" if is_success else "consumedOnFailure"] = True
        case["transactions"]["repairStock"] = [sale]
        case["timeline"].update({"reconstructionStartSeconds": 12.3, "reconstructionCompleteSeconds": 28812.3, "branchEndSeconds": 28812.3})
        case["materialLots"] = [lot]
        final_hp = 5 if is_success else 0
    case["finalItemState"] = {
        "id": "sword-1", "owner": "A", "custody": "WH250-01-workbench",
        "model": "martial-melee-weapons.longsword", "recipe": "recipe-42",
        "HP": final_hp, "maxHP": 5, "AC": 19,
        "structuralState": "functional" if final_hp == 5 else "functional-damaged" if final_hp > 0 else "Broken",
        "imprintRoot": "castF1",
        "rootActive": True, "rootSuppressed": False, "imprintOperational": final_hp > 0,
        "mainBodyRecoverable": True,
    }
    cases.append(case)
data["witnessCases"] = cases

# Bind the exact character-foundation skill and wealth table used above.
foundation_path = pathlib.Path("DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md")
foundation_bytes = foundation_path.read_bytes()
data["sourceBindings"].append({
    "path": str(foundation_path).replace("\\", "/"),
    "status": "source-binding-for-Warrior-skill-list-and-wealth",
    "bytes": len(foundation_bytes),
    "sha256": hashlib.sha256(foundation_bytes).hexdigest(),
})
for binding in data["sourceBindings"]:
    path = pathlib.Path(binding["path"])
    if path.exists():
        raw = path.read_bytes()
        binding["bytes"] = len(raw)
        binding["sha256"] = hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def state_sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def pointer(path, key):
    escaped = str(key).replace("~", "~0").replace("/", "~1")
    return (path + "/" + escaped) if path else "/" + escaped


def patch_diff(before, after, path=""):
    forward, inverse = [], []
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) - set(after), reverse=True):
            p = pointer(path, key)
            forward.extend([{"op": "test", "path": p, "value": copy.deepcopy(before[key])}, {"op": "remove", "path": p}])
            inverse.insert(0, {"op": "add", "path": p, "value": copy.deepcopy(before[key])})
        for key in sorted(set(after) - set(before)):
            p = pointer(path, key)
            forward.append({"op": "add", "path": p, "value": copy.deepcopy(after[key])})
            inverse[0:0] = [{"op": "test", "path": p, "value": copy.deepcopy(after[key])}, {"op": "remove", "path": p}]
        for key in sorted(set(before) & set(after)):
            f, i = patch_diff(before[key], after[key], pointer(path, key))
            forward.extend(f)
            inverse = i + inverse
    elif before != after:
        forward = [{"op": "test", "path": path, "value": copy.deepcopy(before)}, {"op": "replace", "path": path, "value": copy.deepcopy(after)}]
        inverse = [{"op": "test", "path": path, "value": copy.deepcopy(after)}, {"op": "replace", "path": path, "value": copy.deepcopy(before)}]
    return forward, inverse


def make_event(event_id, kind, start, end, before, after, description, branch=None):
    forward, inverse = patch_diff(before, after)
    return {
        "id": event_id,
        "kind": kind,
        "branch": branch,
        "timeStartSeconds": start,
        "timeEndSeconds": end,
        "description": description,
        "beforeSHA256": state_sha(before),
        "afterSHA256": state_sha(after),
        "forward": forward,
        "inverse": inverse,
    }


def actor_state():
    profile = {
        "id": "MF250-DWARF-WARRIOR1", "class": "Warrior", "classLevel": 1,
        "hero": None, "ancestry": "Mountain Dwarf",
        "abilities": {"STR": 12, "DEX": 14, "CON": 14, "INT": 13, "WIS": 12, "CHA": 9},
        "modifiers": {"STR": 1, "DEX": 2, "CON": 2, "INT": 1, "WIS": 1, "CHA": -1},
        "PB": 2, "ac": 12, "HP": 14, "maxHP": 14,
        "body": {"size": "Medium", "walkFeet": 25, "hands": {"left": None, "right": None}, "conditions": []},
        "saves": ["Strength", "Constitution"],
        "skills": ["Athletics", "Insight", "Intimidation", "Survival"],
        "toolProficiencies": ["Smith's tools", "dice gaming set", "Vehicles (Land)"],
        "armorProficiencies": ["Medium", "Heavy", "Light"],
        "weaponProficiencies": ["Martial weapons", "battleaxe", "handaxe", "light hammer", "warhammer"],
        "classAbility": "Strength",
        "classChoices": [
            "warrior.base.serum-injection", "warrior.base.brutal-strike",
            "warrior.base.serum-tolerance", "warrior.base.combat-instinct",
        ],
        "automaticClassGrants": ["Mutation Slot I", "Brutality Threshold tracker"],
        "spellCasting": "none; RP0; maximum spell rank0",
        "background": "aethel-city-guard-veteran",
        "initiativeBonus": 3,
        "sourceClassLevel1SelectionsComplete": True,
    }
    return {
        "id": "MF250-DWARF-WARRIOR1", "profile": profile, "positionFeet": [0, 12, 0],
        "HP": 14, "maxHP": 14, "RP": 0, "maxRP": 0, "Dissonance": 0, "Refrain": 0,
        "lastSpell": None, "usedPreparedFamilies": [], "regularStart": None, "nextRegularStart": 12.0,
        "regularStartsProcessed": [], "Action": 0, "Reaction": 0, "BonusAction": 0,
        "freeInteraction": 0, "movementRemaining": 0, "recharge": {"warrior.base.brutal-strike": 0},
        "ready": None, "concentration": None, "hands": {"left": None, "right": None},
        "worn": [], "resourceHistory": [], "resourceCredits": [], "deathSaves": 0,
        "conditions": [], "turnCast": False,
        "carriedItems": {
            "tools.smith-s-tools": {"quantity": 1, "weightLb": 8, "condition": "usable"},
            "adventuring-gear.acid-vial": {"quantity": 1, "weightLb": 1, "condition": "usable"},
        },
        "carriedWeightLb": 9, "balanceCp": 3500,
        "classResources": {
            "BT": 0, "BTcap": 3, "BrutalityProgress": 0, "Strain": 0, "StrainMax": 3,
            "MutationRecoveryReserve": {"current": 4, "maximum": 4}, "mutationSlots": 1,
            "equippedMutations": ["warrior.supplement.ironhide-graft"], "activeMutations": [],
            "preparedSerums": [
                {
                    "id": "warrior.supplement.overdrive",
                    "chosenAbility": "STR",
                    "chosenAt": "pre-case serum preparation after the prior fixture long rest",
                    "choiceSource": "warrior.json /cards/66/effect",
                },
                "warrior.supplement.stonecore",
            ],
            "activeSerum": None,
        },
    }


def fixture_state():
    lots = []
    for lot_id, mode, cost, branch in lot_specs:
        lots.append({
            "lotId": lot_id, "mode": mode, "priceCp": cost, "quantity": 1,
            "compatibleItemId": "sword-1", "model": "Standard longsword",
            "owner": "WH250-01-OPERATOR", "custodian": "WH250-01-material-bin",
            "status": "available", "reservedBy": None, "branchUse": branch,
        })
    return {
        "status": "local authored noncanonical one-case fixture; no promoted campaign facts",
        "commonStartSeconds": 6.2, "actorId": "MF250-DWARF-WARRIOR1",
        "actorStartingWealthCp": 8000, "actorBalanceCp": 3500,
        "commonTransactions": [
            {
                "id": "MF251-ACQ-TOOLS", "itemId": "tools.smith-s-tools", "quantity": 1,
                "buyer": "MF250-DWARF-WARRIOR1", "seller": "WH250-01-OPERATOR",
                "stockId": "WH250-01-STOCK-TOOLS", "paidCp": 2000, "timeSeconds": 6.2,
            },
            {
                "id": "MF251-ACQ-ACID", "itemId": "adventuring-gear.acid-vial", "quantity": 1,
                "buyer": "MF250-DWARF-WARRIOR1", "seller": "WH250-01-OPERATOR",
                "stockId": "WH250-01-STOCK-ACID", "paidCp": 2500, "timeSeconds": 6.2,
            },
        ],
        "worksite": {
            "id": "WH250-01", "sceneId": "MF210-isolated-scene", "locationFeet": [0, 0, 0],
            "fixtures": ["Forge", "Anvil", "Tongs"], "benchId": "WH250-01-workbench",
            "benchBoxFeet": [[-0.1, 3, 0], [0.1, 7, 0.1]],
            "ownerCustodian": "WH250-01-OPERATOR", "permissionId": "WH250-01-PERMISSION",
            "emptyContainerBinId": "WH250-01-empty-vial-bin",
            "accessFeeCp": 0, "availableFromSeconds": 6.2, "availableThroughSeconds": 28812.3,
            "changeReserveCp": 125, "operatorReceiptsCp": 0, "materialLots": lots,
        },
        "initiativeAt12": {
            "rolls": [
                {"actor": "A", "d20": 18, "modifier": 2, "total": 20},
                {"actor": "MF250-DWARF-WARRIOR1", "d20": 12, "modifier": 3, "total": 15},
                {"actor": "B", "d20": 8, "modifier": 2, "total": 10},
            ],
            "order": ["A", "MF250-DWARF-WARRIOR1", "B"],
        },
        "consent": {
            "owner": "A", "repairer": "MF250-DWARF-WARRIOR1",
            "task": "acid-vial test damage and one permitted repair/reconstruction path",
            "permissionId": "WH250-01-PERMISSION", "confirmedAtSeconds": 6.2,
        },
        "branchTransactions": [], "repairChecks": [],
        "initiativeStatus": "active-until-bounded-test-exit",
    }


base_state = copy.deepcopy(data["priorCase"]["endState"])


def state_hash(value):
    return state_sha(value)


base_hash = state_hash(base_state)
if base_hash != data["priorCase"]["endSnapshotSHA256"]:
    raise SystemExit("Embedded MF210-F01 end-state hash mismatch")

common_events = []
state = copy.deepcopy(base_state)
after = copy.deepcopy(state)
after["actors"]["MF250-DWARF-WARRIOR1"] = actor_state()
after["supplement"] = fixture_state()
after["supplement"]["worksite"]["commonStock"] = [
    {
        "stockId": "WH250-01-STOCK-TOOLS", "itemId": "tools.smith-s-tools",
        "quantity": 0, "status": "sold-at-6.2", "owner": "MF250-DWARF-WARRIOR1",
    },
    {
        "stockId": "WH250-01-STOCK-ACID", "itemId": "adventuring-gear.acid-vial",
        "quantity": 0, "status": "sold-at-6.2", "owner": "MF250-DWARF-WARRIOR1",
    },
]
common_events.append(make_event(
    "MF251-COMMON-01-FIXTURE-AND-ACQUISITIONS",
    "authored-fixture-inputs-and-common-purchases", 6.2, 6.2, state, after,
    "Insert the new Mountain Dwarf Warrior1 as a clearly supplemental static actor at the same scene; "
    "instantiate the one-case station and finite supply; record source-priced kit/vial purchases once "
    "and leave 3500 cp. MF210-F01 remains unchanged.",
))
state = after
after = copy.deepcopy(state)
after["time"] = 12.0
for actor_id in ["A", "B", "MF250-DWARF-WARRIOR1"]:
    current = after["actors"][actor_id]
    current["regularStart"] = 12.0
    current["nextRegularStart"] = 18.0
    if 12 not in current["regularStartsProcessed"]:
        current["regularStartsProcessed"].append(12)
    current["Action"] = 1
    current["Reaction"] = 1
    current["BonusAction"] = 1
    current["freeInteraction"] = 1
    current["turnCast"] = False
after["actors"]["A"]["movementRemaining"] = 30
after["actors"]["B"]["movementRemaining"] = 30
after["actors"]["MF250-DWARF-WARRIOR1"]["movementRemaining"] = 25
after["supplement"]["initiativeStatus"] = "scheduled-starts-processed; order A-C-B"
common_events.append(make_event(
    "MF251-COMMON-02-REGULAR-STARTS-AND-INITIATIVE",
    "scheduled-starts-and-declared-initiative", 6.2, 12.0, state, after,
    "Advance to the actual next scheduled start at t=12.0. Process A, B and C; reset their regular "
    "turn resources; use declared local initiative scores A20, C15 (including Combat Instinct), B10.",
))
state = after
fork_state = copy.deepcopy(state)
fork_hash = state_hash(fork_state)

branch_definitions = [
    {"id": "MF251-W1-ACID-MISS", "d20": 16, "acidDice": None, "damage": 0, "attempts": []},
    {
        "id": "MF251-W1-FUNCTIONAL-REPAIR-SUCCESS", "d20": 17, "acidDice": [1, 2], "damage": 3,
        "attempts": [("MF251-RM-01", 375, 10, 7, "functioning-item-repair", 3600, True)],
    },
    {
        "id": "MF251-W1-REPAIR-FAIL-THEN-SUCCESS", "d20": 17, "acidDice": [1, 2], "damage": 3,
        "attempts": [
            ("MF251-RM-02A", 375, 10, 6, "functioning-item-repair", 3600, False),
            ("MF251-RM-02B", 375, 10, 7, "functioning-item-repair", 3600, True),
        ],
    },
    {
        "id": "MF251-W1-ZERO-HP-RECONSTRUCTION-SUCCESS", "d20": 17, "acidDice": [2, 3], "damage": 5,
        "attempts": [("MF251-RM-03S", 2675, 12, 9, "hp0-reconstruction", 28800, True)],
    },
    {
        "id": "MF251-W1-ZERO-HP-RECONSTRUCTION-FAILURE", "d20": 17, "acidDice": [2, 3], "damage": 5,
        "attempts": [("MF251-RM-03F", 2675, 12, 8, "hp0-reconstruction", 28800, False)],
    },
]

branches = []
for spec in branch_definitions:
    current = copy.deepcopy(fork_state)
    events = []
    branch_id = spec["id"]

    before = copy.deepcopy(current)
    current["time"] = 12.1
    current["actors"]["A"]["freeInteraction"] = 0
    current["actors"]["A"]["hands"]["right"] = None
    item = current["items"]["sword-1"]
    item["custodian"] = "WH250-01-workbench"
    item["positionBoxFeet"] = [[-0.1, 3, 0], [0.1, 7, 0.1]]
    current["supplement"]["consent"]["ownerPlacementAtSeconds"] = 12.0
    current["supplement"]["consent"]["ownerPlacementAction"] = (
        "one free object interaction; A's consent remains explicit"
    )
    events.append(make_event(
        branch_id + ":01-PLACE-SWORD", "free-interaction-placement", 12.0, 12.1,
        before, current,
        "A places the same sword-1 on the supported bench; ownership and root lineage do not change.",
        branch_id,
    ))

    before = copy.deepcopy(current)
    current["time"] = 12.2
    current["actors"]["MF250-DWARF-WARRIOR1"]["Action"] = 0
    current["actors"]["MF250-DWARF-WARRIOR1"]["carriedItems"]["adventuring-gear.acid-vial"]["quantity"] = 0
    current["actors"]["MF250-DWARF-WARRIOR1"]["carriedWeightLb"] = 8
    current["supplement"]["emptyVialDisposition"] = {
        "originalPurchasedItemId": "adventuring-gear.acid-vial",
        "acquisitionTransactionId": "MF251-ACQ-ACID",
        "owner": "MF250-DWARF-WARRIOR1",
        "custodian": "WH250-01-empty-vial-bin",
        "condition": "empty-after-acid-use",
        "massLb": 1,
        "status": "retained-by-fixture-instead-of-carried",
        "timeSeconds": 12.2,
    }
    attack_total = spec["d20"] + 2
    hit = attack_total >= 19
    roll = {
        "kind": "acid-vial-ranged-improvised-attack", "actor": "MF250-DWARF-WARRIOR1",
        "d20Input": spec["d20"], "DEXmodifier": 2, "PBAdded": 0, "total": attack_total,
        "actualDistanceFeet": 5, "maximumRangeFeet": 20, "target": "sword-1",
        "targetAC": 19, "hit": hit, "critical": False, "acidDice": spec["acidDice"],
        "acidDamage": spec["damage"], "vialConsumedHitOrMiss": True,
    }
    current["rolls"].append(roll)
    item = current["items"]["sword-1"]
    item["HP"] = 5 - spec["damage"]
    item["damageDeficit"] = spec["damage"]
    if spec["damage"]:
        item["revision"] += 1
    item["structuralState"] = (
        "functional" if item["HP"] == item["maxHP"]
        else "functional-damaged" if item["HP"] > 0
        else "Broken"
    )
    item["imprintOperational"] = item["HP"] > 0 and item["imprintRoot"]["active"] and not item["imprintRoot"]["suppressed"]
    item["imprintDormantDueToBroken"] = item["HP"] == 0
    item["mainBodyRecoverable"] = True
    current["supplement"]["acidOutcome"] = {
        "attack": roll, "beforeHP": 5, "afterHP": item["HP"], "owner": "A",
        "custodian": "WH250-01-workbench", "imprintRoot": "castF1",
        "rootActive": True, "rootSuppressed": False,
    }
    events.append(make_event(
        branch_id + ":02-ACID-ATTACK", "acid-vial-attack-and-item-damage", 12.1, 12.2,
        before, current,
        "C spends its own Action; use DEX +2 with no PB, target AC19. The vial is consumed on hit or miss; "
        "the item body and cast root remain. The empty vial moves to the fixture bin, so carried weight falls from 9 lb to 8 lb.",
        branch_id,
    ))

    before = copy.deepcopy(current)
    current["time"] = 12.3
    current["supplement"]["initiativeStatus"] = "ended-at-12.3; downtime repair now out of initiative"
    for actor_id in ["A", "B", "MF250-DWARF-WARRIOR1"]:
        current["actors"][actor_id]["nextRegularStart"] = None
    current["supplement"]["BPass"] = {
        "actor": "B", "slotStartSeconds": 12.2, "slotEndSeconds": 12.3,
        "ActionSpent": False, "ReactionSpent": False, "BonusActionSpent": False,
        "positionFeet": [5, 0, 0], "HP": 98, "maxHP": 104,
    }
    current["supplement"]["localEncounterExit"] = {
        "timeSeconds": 12.3, "noActiveThreat": True,
        "evidenceClass": "authored one-case scene fact",
        "changesToPriorActors": "none to B HP, A/B position, or unspent actions beyond scheduled-start reset",
    }
    events.append(make_event(
        branch_id + ":03-EXIT-INITIATIVE", "local-encounter-exit-before-downtime",
        12.2, 12.3, before, current,
        "B passes without spending resources; the bounded test encounter ends as a local authored fact "
        "before any hour-scale work.",
        branch_id,
    ))

    for attempt_index, (lot_id, cost, dc, d20, mode, seconds, success) in enumerate(spec["attempts"], 1):
        attempt_id = branch_id + f":ATTEMPT-{attempt_index}"
        before = copy.deepcopy(current)
        lot = next(x for x in current["supplement"]["worksite"]["materialLots"] if x["lotId"] == lot_id)
        if lot["status"] != "available" or lot["owner"] != "WH250-01-OPERATOR":
            raise SystemExit("lot not available at branch base: " + lot_id)
        balance = current["supplement"]["actorBalanceCp"]
        tender = ((cost + 99) // 100) * 100
        change = tender - cost
        change_reserve = current["supplement"]["worksite"]["changeReserveCp"]
        if balance < tender or change_reserve < change:
            raise SystemExit("insufficient actual tender/change")
        current["supplement"]["actorBalanceCp"] = balance - tender + change
        current["actors"]["MF250-DWARF-WARRIOR1"]["balanceCp"] = balance - tender + change
        current["supplement"]["worksite"]["changeReserveCp"] = change_reserve - change
        current["supplement"]["worksite"]["operatorReceiptsCp"] += cost
        lot.update({
            "owner": "MF250-DWARF-WARRIOR1", "status": "purchased-reserved",
            "reservedBy": attempt_id, "custodian": "WH250-01-material-bin",
        })
        item = current["items"]["sword-1"]
        item["reservedBy"] = attempt_id
        item["custodian"] = "MF250-DWARF-WARRIOR1"
        transaction = {
            "id": attempt_id + ":PURCHASE", "branch": branch_id, "lotId": lot_id,
            "buyer": "MF250-DWARF-WARRIOR1", "seller": "WH250-01-OPERATOR",
            "ownerBefore": "WH250-01-OPERATOR", "ownerAfter": "MF250-DWARF-WARRIOR1",
            "custody": "WH250-01-material-bin", "reservationId": attempt_id,
            "priceCp": cost, "sellerReceiptCp": cost, "tenderCp": tender, "changeReturnedCp": change,
            "changeReserveBeforeCp": change_reserve, "changeReserveAfterCp": change_reserve - change,
            "actorFundsBeforeCp": balance, "actorFundsAfterCp": balance - cost,
            "timeSeconds": current["time"], "finiteStockId": lot_id,
        }
        current["supplement"]["branchTransactions"].append(transaction)
        events.append(make_event(
            branch_id + f":{10 + attempt_index * 2:02d}-RESERVE-" + lot_id,
            "finite-material-purchase-and-reservation",
            current["time"], current["time"], before, current,
            "Buyer C acquires one source-priced finite compatible lot from the identified fixture operator, "
            "reserves it for this one attempt, and tenders actual available funds.",
            branch_id,
        ))

        before = copy.deepcopy(current)
        start = current["time"]
        end = start + seconds
        current["time"] = end
        lot.update({"status": "consumed", "reservedBy": None, "custodian": "consumed-in-work"})
        item = current["items"]["sword-1"]
        item["reservedBy"] = None
        item["custodian"] = "WH250-01-workbench"
        total = d20 + 1 + 2
        check = {
            "attemptId": attempt_id, "mode": mode, "ability": "INT", "abilityModifier": 1,
            "toolProficiency": "Smith's tools", "PB": 2, "toolProficiencyAppliedOnce": True,
            "d20": d20, "total": total, "DC": dc, "success": success,
            "naturalShiftApplied": False, "activeWorkSeconds": seconds,
            "lotId": lot_id, "lotConsumedOnSuccessOrFailure": True,
        }
        if success:
            item["HP"] = item["maxHP"]
            item["damageDeficit"] = 0
            item["revision"] += 1
            item["structuralState"] = "functional"
            item["imprintDormantDueToBroken"] = False
            item["imprintOperational"] = item["imprintRoot"]["active"] and not item["imprintRoot"]["suppressed"]
        else:
            item["structuralState"] = "Broken" if item["HP"] == 0 else "functional-damaged"
            item["imprintDormantDueToBroken"] = item["HP"] == 0
            item["imprintOperational"] = item["HP"] > 0 and item["imprintRoot"]["active"] and not item["imprintRoot"]["suppressed"]
        current["supplement"]["repairChecks"].append(check)
        events.append(make_event(
            branch_id + f":{11 + attempt_index * 2:02d}-COMPLETE-" + lot_id,
            "repair-or-reconstruction-completion", start, end, before, current,
            "Complete the full source-defined active work interval, resolve one binary check at +1 ability "
            "and +2 Smith's-tools proficiency, consume the reserved lot on either result, return custody "
            "to the workbench, and preserve the same body/root.",
            branch_id,
        ))

    branches.append({
        "id": branch_id,
        "baseStateSHA256": fork_hash,
        "baseTimeSeconds": 12.0,
        "events": events,
        "expectedFinal": {
            "timeSeconds": current["time"],
            "actorBalanceCp": current["supplement"]["actorBalanceCp"],
            "item": copy.deepcopy(current["items"]["sword-1"]),
            "BHP": current["actors"]["B"]["HP"],
            "BMaxHP": current["actors"]["B"]["maxHP"],
            "owner": "A",
            "rootId": "castF1",
            "rootActive": True,
            "rootSuppressed": False,
            "repairChecks": copy.deepcopy(current["supplement"]["repairChecks"]),
            "branchTransactions": copy.deepcopy(current["supplement"]["branchTransactions"]),
        },
        "finalStateSHA256": state_hash(current),
    })

data["eventReplay"] = {
    "method": (
        "Reversible JSON-Patch event stream from the exact embedded MF210-F01 end-state. Each event "
        "carries before/after SHA-256 and forward/inverse operations; common events are applied once, "
        "then each alternative branch forks from the common t=12.0 state. No branch expenditure is shared."
    ),
    "baseStateSHA256": base_hash,
    "commonForkStateSHA256": fork_hash,
    "commonEvents": common_events,
    "branches": branches,
    "eventCount": len(common_events) + sum(len(branch["events"]) for branch in branches),
}
data["replayStatus"] = {
    "status": "REPLAY_BUILT_PENDING_STANDALONE_INDEPENDENT_VERIFIER",
    "fullPriorStateEmbedded": True,
    "forwardEvents": data["eventReplay"]["eventCount"],
    "inverseEvents": data["eventReplay"]["eventCount"],
    "independentAudit": "PENDING_STANDALONE_VERIFIER",
    "openItems": [
        "Run the separate replay/transaction/lineage verifier and record its result.",
        "Send exact 252 JSON and its independent audit to GPT for semantic review; 251 was held on three narrow corrections.",
        "MF247-F-W2 remains a separate Eternal Forge closure requirement; all other pending identity holds remain open.",
    ],
}
data["sharedRequirementsStillToBind"] = [
    "Separate charged-item transfer, dawn, damage, suppression/ending and genuinely paid new-creation witness MF247-F-W2 remains separate and unproved.",
    "The other 36 pending identities remain held; none is accepted or applied by this supplement.",
    "The five W1 branches are independent forks; no common-source file, prior case, or canonical rule is altered.",
]
data["directorRuling"]["remainingStatus"] = (
    "W1 has a complete authored event candidate and a standalone verifier is pending. GPT acceptance "
    "has not been issued. Authority remains 811 applied / 37 pending / 0 accepted-unapplied."
)
data["acceptedIds"] = []
data["appliedIds"] = []
data["canonicalChanges"] = False
data["applicationChanges"] = False
data["githubChanges"] = False
OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
print("common events:", len(common_events), "branch events:", [len(branch["events"]) for branch in branches])
print("base:", base_hash, "fork:", fork_hash)
