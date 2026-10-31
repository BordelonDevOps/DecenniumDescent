import copy
from datetime import datetime, timezone
import hashlib
import json
import pathlib
import zlib
import zipfile

W = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
B = W / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SOURCE = B / "rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip"
PLAN = B / "UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_252.json"
OUT = B / "UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256.json"

plan = json.loads(PLAN.read_text(encoding="utf-8"))
with zipfile.ZipFile(SOURCE) as z:
    members = z.namelist()

    def source_member(suffix):
        hits = [n for n in members if n.startswith("sources_current/") and n.endswith(suffix)]
        if len(hits) != 1:
            raise RuntimeError((suffix, hits))
        return hits[0], z.read(hits[0])

    mage_path, mage_raw = source_member("data/public/class_playtests/mage.json")
    wizard_path, wizard_raw = source_member("data/public/class_playtests/wizard.json")
    druid_path, druid_raw = source_member("data/public/class_playtests/druid.json")
    catalog_path, catalog_raw = source_member("data/public/spell_playtests/catalog.json")
    repertoire_path, repertoire_raw = source_member("docs/mechanics/CLASS_PLAYTEST_RULES.md")
    mage = json.loads(mage_raw)
    wizard = json.loads(wizard_raw)
    catalog = json.loads(catalog_raw)


def binding(path, raw):
    return {
        "path": path,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}",
    }


def spell_entry(spell_id, cls, acquired_class_level, acquired_character_level):
    hits = [s for s in catalog["spells"] if s["id"] == spell_id]
    if len(hits) != 1:
        raise RuntimeError((spell_id, len(hits)))
    s = hits[0]
    access = s["classAccess"][cls]
    return {
        "id": spell_id,
        "name": s["name"],
        "class": cls,
        "rank": access["rank"],
        "minimumClassLevel": access["minimumClassLevel"],
        "acquiredClassLevel": acquired_class_level,
        "acquiredCharacterLevel": acquired_character_level,
        "operationalStatus": s.get("status", s.get("catalogStatus")),
        "catalogBinding": binding(catalog_path, catalog_raw),
    }


def cantrip_entry(spell_id, cls, acquired_class_level, acquired_character_level):
    x = spell_entry(spell_id, cls, acquired_class_level, acquired_character_level)
    if x["rank"] != 0:
        raise RuntimeError((spell_id, x))
    return x


# Bind the fallback class-repertoire rule separately from the class rank gate.
rules_binding = binding(repertoire_path, repertoire_raw)
assert rules_binding["bytes"] == 17321
assert rules_binding["sha256"] == "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81"
plan["sourceAuthority"]["packet241MemberBindings"]["classPlaytestRules"] = rules_binding
plan["sourceAuthority"]["fallbackRepertoireRule"] = {
    **rules_binding,
    "anchor": "Spell repertoires and acquisition, line 55",
    "rule": "Full casters know 3 cantrips at class level 1, 4 at 4 and 5 at 10; choose 2 ranked spells at first spell access plus 1 at each later class level. Preserve more-specific class spellbook/preparation rules. Known casters may replace one known spell at long rest with a legal same-or-lower-rank selection.",
    "status": "Packet241 source-bound provisional fallback; does not complete unfinished catalog entries.",
}

# Keep Mage ordinary repertoire separate from the ten acquired Mage class cards.
target = plan["qualifiedActors"]["target"]
repertoire = target["repertoire"]
mage_cantrips = [
    cantrip_entry("arcane-ray", "Mage", 1, 2),
    cantrip_entry("flare-spark", "Mage", 1, 2),
    cantrip_entry("sense-magic", "Mage", 1, 2),
    cantrip_entry("mage-light", "Mage", 4, 5),
]
mage_spells = [
    spell_entry("shield", "Mage", 1, 2),
    spell_entry("burning-hands", "Mage", 1, 2),
    spell_entry("mist-step", "Mage", 2, 3),
    spell_entry("lightning-pulse", "Mage", 3, 4),
    spell_entry("dispel-magic-lesser", "Mage", 4, 5),
    spell_entry("remove-curse", "Mage", 5, 6),
]
rank_gates = mage["maxSpellRankByClassLevel"]
assert rank_gates[:5] == [1, 1, 2, 2, 3]
for x in mage_spells:
    assert x["minimumClassLevel"] <= x["acquiredClassLevel"]
    assert x["rank"] <= rank_gates[x["acquiredClassLevel"] - 1]
assert all(x["operationalStatus"] == "operational-playtest-draft" for x in mage_cantrips + mage_spells)
repertoire["mageOrdinaryCantrips"] = mage_cantrips
repertoire["mageOrdinaryCantripCount"] = 4
repertoire["mageOrdinaryCantripRule"] = {
    "source": "CLASS_PLAYTEST_RULES.md, Spell repertoires and acquisition, line 55",
    "acquisition": [{"mageLevel": 1, "characterLevel": 2, "count": 3}, {"mageLevel": 4, "characterLevel": 5, "count": 1}],
}
repertoire["mageOrdinaryKnownSpells"] = mage_spells
repertoire["mageOrdinaryKnownSpellCount"] = 6
repertoire["mageOrdinaryKnownSpellRule"] = {
    "source": "CLASS_PLAYTEST_RULES.md, Spell repertoires and acquisition, line 55",
    "acquisitionSchedule": [
        {"mageLevel": 1, "characterLevel": 2, "newRankedSpells": 2, "maximumRank": 1},
        {"mageLevel": 2, "characterLevel": 3, "newRankedSpells": 1, "maximumRank": 1},
        {"mageLevel": 3, "characterLevel": 4, "newRankedSpells": 1, "maximumRank": 2},
        {"mageLevel": 4, "characterLevel": 5, "newRankedSpells": 1, "maximumRank": 2},
        {"mageLevel": 5, "characterLevel": 6, "newRankedSpells": 1, "maximumRank": 3},
    ],
    "replacementHistory": "No replacement is used; each entry retains its acquisition-time maximum-rank gate.",
}
repertoire["mageOrdinaryKnownSpellCountRule"] = 6
repertoire["mageSelectedClassCardsRemainSeparate"] = list(repertoire["mageSelected"])

# Preserve Wizard's explicit spellbook and add its separate known-cantrip progression.
u = plan["qualifiedActors"]["unravelCaster"]
wizard_cantrips = [
    cantrip_entry("ghost-sound", "Wizard", 1, 1),
    cantrip_entry("minor-image", "Wizard", 1, 1),
    cantrip_entry("minor-illusion", "Wizard", 1, 1),
    cantrip_entry("arcane-ray", "Wizard", 4, 4),
    cantrip_entry("mage-light", "Wizard", 10, 10),
]
assert all(x["operationalStatus"] == "operational-playtest-draft" for x in wizard_cantrips)
u["cantripsKnown"] = wizard_cantrips
u["cantripCount"] = 5
u["cantripAcquisitionRule"] = {
    "source": "wizard.json engine, cantrip completion",
    "schedule": [{"wizardLevel": 1, "count": 3}, {"wizardLevel": 4, "count": 4}, {"wizardLevel": 10, "count": 5}],
    "cantripsDoNotConsumePreparedMatrices": True,
}
u["preparationCapacity"] = 23
u["preparedCount"] = 22
u["unusedPreparationCapacity"] = 1
u["preparation"] = "Wizard17 + INT modifier5 + acquired Floating Preparation1 = capacity23; prepare22, leave one slot explicitly unused. Matrix Efficiency at W4 makes the study45 minutes."
u["profileBinding"] = {
    "profileId": "PROFILE-UNRAVEL-WIZARD17-256",
    "profileRole": "Separate conditional Human Wizard17 Illusion; no target identity, gear, pool or class features inherited.",
    "characterLevel": 17,
    "wizardClassLevel": 17,
    "baseTemplate": "Packet241 prior/ACTOR_PROFILES.json#/ConjurationWizard20.characterFoundation; origin/point-buy template only.",
    "baseTemplateBinding": plan["sourceAuthority"]["return241ActorTemplate"],
    "classProgressionBinding": binding(wizard_path, wizard_raw),
    "ownEquipment": {"AC": 12, "armor": None, "weapon": None, "focus": "Illusion focus in left hand", "rightHand": "free", "spellbook": "own book in satchel"},
}

# Give each helper a distinct, fully bound actor profile and resource/action history.
helper_base = {
    "classLevels": {"Wizard": 17},
    "characterLevel": 17,
    "scores": {"STR": 10, "DEX": 14, "CON": 14, "INT": 20, "WIS": 14, "CHA": 13},
    "HP": {"current": 104, "max": 104},
    "RP": {"current": 64, "max": 64},
    "proficiencyBonus": 6,
    "maxSpellRank": 9,
    "handsAndGear": {"AC": 12, "armor": None, "weapon": None, "focus": "Wizard arcane focus, left hand", "rightHand": "free", "spellbook": "actor-owned satchel"},
    "sourceBindings": {"wizardClass": binding(wizard_path, wizard_raw), "profileTemplate": plan["sourceAuthority"]["return241ActorTemplate"]},
}
mb_helper = copy.deepcopy(helper_base)
mb_helper.update({
    "id": "WITNESS-MINDBLANK-WIZARD17",
    "profileBinding": {"profileId": "PROFILE-MINDBLANK-WIZARD17-256", "source": "Independent conditional Wizard17 actor; uses the bound class route and its own profile, spellbook, RP and turn budgets."},
    "school": "Illusion",
    "spellbookEntriesRelevantToCast": [{"id": "mind-blank", "rank": 8, "learnedWizardLevel": 15}],
    "preparedMatrices": ["mind-blank rank8"],
    "castHistory": [{"time": "2026-10-30T10:00:28Z", "spell": "mind-blank rank8", "Action": "spent", "RP": 21, "Dissonance": 0, "family": "first distinct prepared matrix family"}],
    "turnBudgets": {"beforeCast": {"turn": "MB-T1 10:00:24–10:00:30", "Action": "ready", "BonusAction": "ready", "Reaction": "ready"}, "afterCast": {"Action": "spent: Mind Blank", "BonusAction": "ready", "Reaction": "ready"}},
    "concentration": {"sourceEffectDuration": None, "deadline": None, "status": "UNRESOLVED; no successful interval asserted; exact accepted rank8ward5_reviewed_149/MODEL.json /spells/3/procedure not bound here"},
})
mb_helper["RP"] = {"current": 43, "max": 64}
plan["qualifiedActors"]["mindBlankSuppressor"] = mb_helper

dispel_helper = copy.deepcopy(helper_base)
dispel_helper.update({
    "id": "WITNESS-ARCH-DISPEL-WIZARD17",
    "profileBinding": {"profileId": "PROFILE-ARCH-DISPEL-WIZARD17-256", "source": "Independent conditional Wizard17 actor; own acquired W5 Arch Dispel, prepared Detect Magic, RP pool, concentration and turn budgets."},
    "school": "Illusion",
    "preparedMatrices": ["detect-magic rank1"],
    "acquiredClassCards": ["wizard.arch.dispel-magic acquired at Wizard5"],
    "castHistory": [
        {"time": "2026-10-30T10:00:13Z", "spell": "detect-magic", "rank": 1, "Action": "spent", "RP": 2, "Dissonance": 0, "family": "first distinct prepared matrix family"},
        {"time": "2026-10-30T10:00:28Z", "spell": "wizard.arch.dispel-magic", "Action": "spent", "RP": 3, "Dissonance": 0, "family": "always-prepared Wizard class matrix; outside daily prepared-slot count"},
    ],
    "turnBudgets": {
        "afterDetectMagic": {"turn": "AD-T1 10:00:12–10:00:18", "Action": "spent: Detect Magic", "BonusAction": "ready", "Reaction": "ready"},
        "afterAD-T1-end": {"turn": "AD-T1 END10:00:18", "Action": "spent: Detect Magic", "BonusAction": "available then turn ended", "Reaction": "available then turn ended"},
        "afterAD-T2-start": {"turn": "AD-T2 starts10:00:18", "Action": "ready", "BonusAction": "ready", "Reaction": "ready", "recharge": {"ArchDispel": 0}},
        "afterAD-T2-end": {"turn": "AD-T2 ends10:00:24", "Action": "available then turn ended", "noSpellOrWeave": True, "DissonanceVent": "0→0", "refrain": {"repeatCount": 0, "lastSpell": "detect-magic"}},
        "beforeArchDispel": {"turn": "AD-T3 starts10:00:24", "Action": "ready", "BonusAction": "ready", "Reaction": "ready", "recharge": {"ArchDispel": 0}},
        "afterArchDispel": {"turn": "AD-T3 Action10:00:28", "Action": "spent: Arch Dispel", "BonusAction": "ready", "Reaction": "ready", "recharge": {"ArchDispel": 2}},
        "afterAD-T3-end": {"turn": "AD-T3 ends10:00:30", "Action": "spent: Arch Dispel", "BonusAction": "available then turn ended", "Reaction": "available then turn ended", "recharge": {"ArchDispel": 2}},
        "afterAD-T4-start": {"turn": "AD-T4 starts10:00:30", "Action": "ready", "BonusAction": "ready", "Reaction": "ready", "recharge": {"ArchDispel": 1}},
        "afterAD-T4-end": {"turn": "AD-T4 END10:00:36", "Action": "available then turn ended", "BonusAction": "available then turn ended", "Reaction": "available then turn ended", "recharge": {"ArchDispel": 1}},
        "afterAD-T5-start": {"turn": "AD-T5 START10:00:36", "Action": "ready", "BonusAction": "ready", "Reaction": "ready", "recharge": {"ArchDispel": 0}},
    },
    "recharge": {"ArchDispel": {"printedRounds": 2, "remainingRoundsAtCast": 2, "remainingRoundsAtAD-T4-start": 1, "tickSource": "wizard.json /engine/12: round recharge counters decrease at the start of the regular initiative turn"}},
    "castingFamilyHistory": ["detect-magic prepared matrix family", "wizard.arch.dispel-magic always-prepared class matrix family"],
    "refrainHistory": {"afterDetectMagic": {"repeatCount": 0, "lastSpell": "detect-magic"}, "afterAD-T2-no-spell-turn": {"repeatCount": 0, "lastSpell": "detect-magic"}, "afterArchDispel": {"repeatCount": 0, "lastSpell": "wizard.arch.dispel-magic"}},
    "concentration": {"source": "detect-magic", "started": "2026-10-30T10:00:13Z", "deadline": "2026-10-30T10:10:13Z", "status": "active through the Arch Dispel observation and commitment"},
    "perceptionScene": {"observerPositionFt": [20, 0, 0], "targetPositionFt": [0, 0, 0], "distanceFt": 20, "lineOfSight": "clear", "interveningCover": "none", "ambientLight": "bright", "observationTime": "2026-10-30T10:00:27Z", "observation": "Detect Magic automatically senses the unique active Unravel Identity aura at 20 feet before commitment; no separate examine Action is claimed, and no other active spell aura is present on the target."},
})
dispel_helper["RP"] = {"current": 59, "max": 64}
dispel_helper["recharge"] = {"ArchDispel": {"current": 0, "printedRounds": 2, "atAD-T4Start": 1, "atAD-T5Start": 0}, "tickHistory": [{"time":"2026-10-30T10:00:30Z","before":2,"after":1,"source":"wizard.json /engine/12"},{"time":"2026-10-30T10:00:36Z","before":1,"after":0,"source":"wizard.json /engine/12"}]}
plan["qualifiedActors"]["archDispelRemover"] = dispel_helper
plan["qualifiedActors"]["unravelCaster"]["casterActivity"] = {
    "actor": "WITNESS-UNRAVEL-WIZARD17",
    "profileId": "PROFILE-UNRAVEL-WIZARD17-256",
    "RPBefore": {"current": 64, "max": 64},
    "RPAfter": {"current": 38, "max": 64},
    "turnBudgets": {
        "beforeCast": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready"},
        "afterCast": {"Action": "spent: Unravel Identity", "BonusAction": "ready", "Reaction": "ready"},
    },
    "concentration": None,
    "castHistory": [{"time": "2026-10-30T10:00:27Z", "spell": "unravel-identity rank9", "Action": "spent", "RP": 26, "Dissonance": 0, "family": "first distinct prepared matrix family"}],
    "castingFamilyHistory": ["unravel-identity first prepared matrix family"],
}

target["profileBinding"] = {
    "profileId": "PROFILE-DRUID15-MAGE5-256",
    "profileRole": "Conditional static Human Druid15/Mage5 actor; own progression, class repertoire and equipment are enumerated in this witness.",
    "baseTemplate": "Packet241 prior/ACTOR_PROFILES.json#/ConjurationWizard20.characterFoundation; foundation only, no Wizard equipment or capability inheritance.",
    "baseTemplateBinding": plan["sourceAuthority"]["return241ActorTemplate"],
    "classProgressionBindings": {"druid": binding(druid_path, druid_raw), "mage": binding(mage_path, mage_raw), "classPlaytestRules": rules_binding},
}

# Director-authorized, Unravel-only class-loss callback and source-qualified attack overlays.
plan["dependencyCallbackPlan"][14]["duringUnravel"] = "Unavailable while Mage class loss is active; the target loses Elemental Affinity Fire resistance. The familiar's independent creation-fixed Fire resistance is unaffected."
plan["dependencyCallbackPlan"][14]["recovery"] = "Mage availability returns and the same Elemental Affinity Fire resistance resumes; no other effect or resource resets."
for callback in plan["dependencyCallbackPlan"]:
    if callback.get("sourceId") == "mage.base.resonance-pool":
        callback["duringUnravel"] = "Mage feature use is unavailable; the shared pool is 41/46 at admission and does not change from class loss."
    if callback.get("source") == "NEW UI251-FORM-LOSS (spell-local only)":
        callback["recovery"] = "Class availability only; never recreate form, buffer, tempHP or Detect Magic. No global Druid/antimagic rule is asserted. Preserve HP138, RP41/46, shifts5/6, reserve5/35, Form Surge6/6, elemental uses2/2."
    if callback.get("source", "").startswith("Conjure Elemental Familiar +"):
        callback["duringUnravel"] = "Same Fire familiar 14/14 AC18 with fixed resistance and original10:10:01Z deadline persists; remove owner command permission, with no pending order. It defensively moves/Dodges; no damage/control."
plan["dependencyCallbackPlan"][23]["duringUnravel"] = "For this Unravel procedure only, class-derived proficiency contributions (Druid/Mage skills, saves and class training) are unavailable during active class loss; acquisition records and PB6 scalar remain. Independent ancestry/background contributions remain. No proficiency-dependent check is made in this witness."
plan["dependencyCallbackPlan"][23]["recovery"] = "Eligibility returns with class availability; no acquisition or numeric proficiency scalar changes. This is a spell-local clarification, not a global proficiency rule."
plan["qualifiedActors"]["target"]["earthWardenAttackOverlay"] = {
    "profileBaseAttack": "PB+WIS to hit; 1d8+WIS slashing base claw from the bound Earth Warden form profile.",
    "circleForms": "Acquired druid.base.moon.circle-forms applies its first-natural-form-hit-per-turn S damage rider; kept separate from base dice.",
    "primalStrike": "Acquired druid.arch.moon.primal-strike makes this natural attack count as magical against defenses to nonmagical physical attacks; it does not change the damage type.",
    "sourceBindings": {"druidClass": binding(druid_path, druid_raw), "mageClass": binding(mage_path, mage_raw), "supplementalFormRegister": plan["sourceAuthority"]["supplementalLocalFormRegister"]},
}

# Chronology: six-second rounds; every spell/action is charged, and each no-spell turn vents once.
plan["commonPrehistory"] = [
    {"event": "INITIAL-POST-LONG-REST-FIXTURE", "time": "2026-10-30T10:00:00Z", "fixtureOnly": True, "after": {"HP": "138/138", "RP": "46/46", "Dissonance": "0/12", "shifts": "6/6", "buffer": "35/35", "formSurge": "6/6", "elementalUses": "2/2", "concentration": None, "familiarUse": "ready", "turnCadence": "six-second regular turns; this fully bound post-rest state is the initial fixture, not a claimed rest transition"}},
    {"event": "TARGET-T1-CAST-FIRE-FAMILIAR", "start": "2026-10-30T10:00:00Z", "time": "2026-10-30T10:00:01Z", "end": "2026-10-30T10:00:06Z", "action": "Mage Conjure Elemental Familiar Action; pay4RP; rank3 Dissonance +1; use1/LR spent.", "after": {"RP": "42/46", "Dissonance": "1/12", "Action": "spent: Conjure Elemental Familiar", "BonusAction": "ready", "Reaction": "ready", "Familiar": "FAM-FIRE-01 14/14 AC18 Fire identity/resistance; deadline10:10:01Z", "pendingCommand": None}},
    {"event": "TARGET-T2-NO-SPELL-VENT", "start": "2026-10-30T10:00:06Z", "time": "2026-10-30T10:00:09Z", "end": "2026-10-30T10:00:12Z", "action": "ordinary Dodge Action; no spell or Weave ability; Let the Note Fall applies at END.", "after": {"RP": "42/46", "Dissonance": "0/12", "Action": "spent: Dodge", "BonusAction": "ready", "Reaction": "available then turn ended", "familiar": "unchanged; owner command permission available"}},
    {"event": "TARGET-T3-CAST-DETECT-MAGIC", "start": "2026-10-30T10:00:12Z", "time": "2026-10-30T10:00:13Z", "end": "2026-10-30T10:00:18Z", "action": "Mage class card mage.base.detect-magic Action; pay1RP; Dissonance +1; distinct from the ordinary known detect-magic spell.", "after": {"RP": "41/46", "Dissonance": "1/12", "Action": "spent: Mage Detect Magic", "BonusAction": "ready", "Reaction": "ready", "concentration": "DM-01 active through no later than10:10:13Z", "Refrain": "lastSpell mage.base.detect-magic; first different name adds no repeat increment", "NukeChain": "empty"}},
    {"event": "TARGET-T4-SHIFT-EARTH-WARDEN", "start": "2026-10-30T10:00:18Z", "shiftTime": "2026-10-30T10:00:19Z", "end": "2026-10-30T10:00:24Z", "action": "Druid Earth Warden shift Bonus Action only; spend one shift and draw30 from Buffer Reserve. Shapeshifting changes the body sounding the Weave, clears remembered Refrain and repeat count, and prevents a Let the Note Fall vent this turn. No Mage spell is cast; no Arcane Missile target/damage event is introduced.", "after": {"HP": "138/138", "RP": "41/46", "Dissonance": "1/12", "Action": "ready; unspent", "BonusAction": "spent: Earth Warden shift", "Reaction": "available then turn ended", "shift": "5/6", "buffer": "5/35", "tempHP": "30 tied to FORM-EW-01", "formStart": "10:00:19Z", "formDeadline": "10:10:19Z", "form": "Earth Warden; normal AC12; nonmagical physical resistance; base claw plus separate Circle Forms/Primal Strike overlays", "refrain": {"repeatCount": 0, "lastSpell": None}, "earthSlamRecharge": "printed length2; remaining counter0; no Slam used"}},
    {"event": "TARGET-T5-START", "start": "2026-10-30T10:00:24Z", "time": "2026-10-30T10:00:24Z", "end": "2026-10-30T10:00:30Z", "action": "T5 START; reset target Action/Bonus/Reaction budgets. UI-01 is not yet admitted.", "after": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready", "RP": "41/46", "Dissonance": "1/12", "form": "FORM-EW-01 active"}},
    {"event": "ADMIT-UNRAVEL", "time": "2026-10-30T10:00:27Z", "action": "separate Wizard17 Action; pay26RP; first distinct prepared matrix family, Dissonance0; automatic admission, no save, no concentration. Apply approved Unravel-only UI251-FORM-LOSS during T5; UI196-CLOCK excludes the current turn from the first-future-target-END clock.", "after": {"WizardCasterRP": "38/64", "WizardAction": "spent: Unravel Identity", "WizardDissonance": "0/13", "TargetClassFeatures": "unavailable until T6 END10:00:36Z; T5 END10:00:30Z is excluded because T5 was already in progress at admission", "TargetFalseSelf": "active until first future target regular END10:00:36Z", "TargetIdentity": "unchanged", "TargetHP": "138/138", "TargetRP": "41/46", "TargetDissonance": "1/12", "form": "ended at admission; remove30 form tempHP and physical resistance; base form attacks end; return root anatomy", "concentration": "DM-01 ended terminally at admission", "targetElementalAffinityFireResistance": "unavailable during Mage class loss", "familiar": "same FAM-FIRE-01 14/14, original10:10:01Z deadline; owner command removed; no pending order", "targetTurn": "T5 started10:00:24Z; T5 END10:00:30 excluded; first future END is T6 END10:00:36Z"}},
    {"event": "TARGET-T5-DODGE", "start": "2026-10-30T10:00:24Z", "actionTime": "2026-10-30T10:00:29Z", "end": "2026-10-30T10:00:30Z", "action": "target spends Action on Dodge after Unravel admission; no spell/Weave. At T5 END, vent Dissonance1→0; UI-01 and class loss remain active because T5 was in progress at admission.", "after": {"HP": "138/138", "RP": "41/46", "Dissonance": "0/12", "Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended", "UI-01": "active through T6 END10:00:36Z", "form": None, "tempHP": 0, "DM-01": "ended", "MageFireResistance": "unavailable", "familiarCommandPermission": False}},
    {"event": "TARGET-T5-FAMILIAR-ATTACHED-PHASE", "time": "2026-10-30T10:00:30.1Z", "ownerTurnEnd": "2026-10-30T10:00:30Z", "action": "complete familiar state; defensive Dodge after the whole owner turn; owner class loss/UI-01 remains active and command permission is false", "after": {"Familiar": "FAM-FIRE-01 Fire; HP14/14; AC18; speed30; creation-fixed resistance; original deadline10:10:01Z; no pending order", "ownerClassAvailability": {"Druid": False, "Mage": False}, "ownerCommandPermission": False}},
    {"event": "TARGET-T6-START", "start": "2026-10-30T10:00:30Z", "time": "2026-10-30T10:00:30Z", "end": "2026-10-30T10:00:36Z", "action": "T6 START; reset target Action/Bonus/Reaction budgets. UI-01 remains active; no resource or ended effect is recreated.", "after": {"Action": "ready", "BonusAction": "ready", "Reaction": "ready", "RP": "41/46", "Dissonance": "0/12", "classAvailability": {"Druid": False, "Mage": False}, "familiarCommandPermission": False, "UI-01": "active through T6 END10:00:36Z"}},
    {"event": "TARGET-T6-DODGE-AND-END", "start": "2026-10-30T10:00:30Z", "actionTime": "2026-10-30T10:00:33Z", "end": "2026-10-30T10:00:36Z", "action": "target spends Action on Dodge; no spell/Weave. UI-01 ends at T6 END10:00:36Z; class availability, proficiency eligibility, Mage Fire Affinity and familiar command permission return. Let the Note Fall0→0. Do not recreate form, tempHP, DM-01, resources or per-rest uses.", "after": {"HP": "138/138", "RP": "41/46", "Dissonance": "0/12", "Action": "spent: Dodge", "BonusAction": "available then turn ended", "Reaction": "available then turn ended", "classAvailability": {"Druid": True, "Mage": True}, "classDerivedProficiencyAvailable": True, "subjectiveBelief": None, "familiarCommandPermission": True, "form": None, "tempHP": 0, "DM-01": "ended; not restored", "MageFireResistance": "restored with Mage availability", "familiarDeadline": "original10:10:01Z; unchanged"}},
    {"event": "TARGET-T6-FAMILIAR-ATTACHED-PHASE", "time": "2026-10-30T10:00:36.1Z", "ownerTurnEnd": "2026-10-30T10:00:36Z", "action": "complete familiar state; defensive Dodge after the whole owner turn; command permission has returned with class availability", "after": {"Familiar": "same FAM-FIRE-01 Fire; HP14/14; AC18; speed30; creation-fixed resistance; original deadline10:10:01Z; no pending order", "ownerClassAvailability": {"Druid": True, "Mage": True}, "ownerCommandPermission": True}},
]
plan["proposedPreCastState"].update({
    "status": "source-bound static fixture; exact clocks and operation budgets instantiated in Replay256",
    "sharedRP": "41/46 after Mage Conjure Familiar4RP and Mage Detect Magic1RP; the additional Arcane Missile cast was removed, so it costs no RP.",
    "dissonance": "1/12 at admission; target T5 ends with no spell/Weave and vents1→0 at :30 while UI-01 remains active; T6 ends with no spell/Weave and vents0→0 at :36.",
    "detectMagic": "DM-01 starts10:00:13Z; ends terminally at Unravel admission10:00:27Z; never restored.",
    "druidForm": {"active": "Earth Warden Arch form", "duration": "10 minutes", "entry": "Bonus Action only during target T4; no Mage spell is cast", "entryBuffer": "30 temporary HP drawn from reserve; Buffer Reserve5/35", "formStart": "10:00:19Z", "earthSlamRecharge": {"printedRounds": 2, "remainingRounds": 0, "used": False, "survivesFormLoss": True}, "refrain": {"repeatCount": 0, "lastSpell": None}},
})

plan["coverageAndReversibleEvidencePlan"] = {
    "commonHistory": "Six-second target turns T1–T6: starts :00, :06, :12, :18, :24, :30; ends :06, :12, :18, :24, :30, :36. T5 begins before Unravel admission at :27. UI196-CLOCK excludes the in-progress T5; natural expiration is T6 END :36.",
    "initialFixture": "Fully bound post-long-rest actor state is the declared initial static fixture; no before-rest state or reversible rest event is claimed.",
    "timeline": "T5 START :24; Unravel admission :27; target Dodge :29; T5 END :30 vents Dissonance1→0 but does not end UI-01; familiar attached phase :30.1 has owner class/command unavailable. T6 START :30; Dodge :33; UI-01 expires and availability returns at T6 END :36; familiar phase :36.1 follows the whole owner turn. No form, tempHP, DM-01, RP, HP or per-rest resource is recreated.",
    "ui196ClockRule": "Preserved UI196-CLOCK: first future target regular END excluding the target turn already in progress at admission. Admission at :27 during T5 excludes T5 END :30; the scheduled natural expiry is T6 END :36.",
    "forks": [
        {"id": "NATURAL-EXPIRY", "status": "complete static branch", "events": ["target T5 START :24; Unravel admits :27", "target Dodge :29; T5 END :30 vents1→0 but class loss/UI remain active", "familiar attached phase :30.1 after whole T5 END; owner command permission false", "target T6 START :30; Dodge :33; T6 END :36 naturally ends UI and restores class availability/Fire Affinity/command", "familiar attached phase :36.1 after whole T6 END; original familiar deadline10:10:01Z unchanged", "form/tempHP/DM-01 remain ended; no resources reset"]},
        {"id": "MINDBLANK-SUPPRESSION", "status": "CONDITIONAL_NOT_COUNTED_AS_SUCCESSFUL_WITNESS", "sourceRequirement": "Bind accepted rank8ward5_reviewed_149/MODEL.json /spells/3/procedure and its operative duration before asserting a successful interval. Otherwise no suppression state is claimed.", "events": ["separate helper pays21RP and spends its Action10:00:28; source duration unresolved", "projection only; no successful suppression interval is asserted", "actual target timeline retains UI through T5 END :30 and the T5 familiar phase :30.1 with command permission false; natural expiry is T6 END :36", "T6 Dodge :33; T6 END :36 restores owner availability; attached phase :36.1 follows whole turn"]},
        {"id": "ARCH-DISPEL-REMOVAL", "status": "source-qualified separate removal test", "separateActor": "Wizard17; prepared Detect Magic Action2RP at :13, concentration deadline10:10:13; at :27 observes UI-01 at20ft within30ft with clear sight/no cover; Action Arch Dispel3RP at :28; d20 8 + INT5 + PB6 =19 vs DC19; success; recharge2→1 at helper T4 START :30 per wizard.json /engine/12.", "events": ["target transition at :28 removes only UI-01 after successful Arch Dispel; record original natural expiry :36 separately from actual termination :28", "target Dodge :29; T5 END :30 vents1→0; class availability already restored; familiar phase :30.1 after whole turn", "continue target T6 through END :36; no UI effect returns; familiar source deadline10:10:01Z is unchanged"]},
    ],
    "stateAccounting": "Target T2 vents1→0; T3 Detect Magic adds1; T4 Shapeshift changes the body sounding the Weave, clears Refrain and prevents vent; T5 no-spell Dodge vents1→0 at :30; T6 no-spell Dodge vents0→0 at :36. No RP/HP/reserve/rest/per-rest refill.",
    "familiarAttachedPhase": "Full before/after snapshots at :30.1 and :36.1 follow the owner's whole T5/T6 turns. At :30.1 in natural/conditional branches, UI/class loss remains active and owner command permission is false; at :36.1 natural expiry has restored permission. Preserve the same identity, fixed resistance, HP, AC, speed, use, creation/deadline, order state, position and owner markers; no generic Action/Bonus/Reaction budgets.",
    "mindBlankBoundary": "No source duration is bound. No successful suppression is asserted or counted.",
    "archDispelBoundary": "Detect Magic senses the unique ongoing aura at20ft within30ft with clear sight/no cover; observation identifies this Unravel instance before commitment; a separate target removal transition follows the successful helper check.",
    "statusBoundary": "No identity acceptance/application or canonical change is asserted. Existing Return241 cases remain byte-identical.",
}
plan["reversibleStateOperations"] = [
    {"id": "OP256-01", "forward": "Pay Conjure Familiar4RP; spend1/LR; create source-clocked Fire companion; Action spent.", "inverse": "Static audit restoration of the fully bound initial fixture; no in-world dismissal/refund."},
    {"id": "OP256-02", "forward": "Target T2 Dodge with no spell/Weave; Let the Note Fall1→0; Action spent.", "inverse": "Static audit only; does not restore a spent Action."},
    {"id": "OP256-03", "forward": "Pay Mage Detect Magic1RP; start DM-01; Action spent.", "inverse": "Static audit only; DM-01 is not restored in-world."},
    {"id": "OP256-04", "forward": "Earth Warden shift with Bonus Action; consume one shift and30 Buffer Reserve; clear remembered Refrain and repeat count; no spell is cast and Earth Slam counter remains0 of printed2.", "inverse": "Static audit only; no form/temporary HP/recharge reset."},
    {"id": "OP256-05", "forward": "Wizard17 commits Action/RP26; admit Unravel and belief; apply approved spell-local UI251-FORM-LOSS; end DM-01 and form once.", "inverse": "Static snapshot restoration only; not an in-world reversal/refund/recreated form."},
    {"id": "OP256-06", "forward": "Fork into exact Natural Expiry, conditional Mind Blank projection, or source-qualified Arch Dispel; process each target turn and familiar phase independently.", "inverse": "Static audit only; each helper retains its own costs, casting family and budgets."},
]
plan["directorQuestions"] = [
    "Review the completed actor/feature projection, source-bound chronology, 1→0 final Dissonance vent, and independently budgeted branch transitions.",
    "Mind Blank remains explicitly conditional unless the accepted rank8ward5 procedure and operative duration are bound; do not count it as a successful branch otherwise.",
    "Confirm whether the lawful 20-foot Detect Magic observation completes Arch Dispel perceivability and whether Unravel Identity is accepted for its one-identity scope; otherwise specify only remaining fixes.",
]
plan["id"] = "UNRAVEL-IDENTITY-MD196-B02-INTEGRATED-WITNESS-256"
plan["recordedAtUtc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
plan["status"] = "CORRECTED_INTEGRATED_WITNESS_READY_FOR_DIRECTOR_RECHECK"
plan["accepted"] = False
plan["applied"] = False

OUT.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raw = OUT.read_bytes()
print(json.dumps({"path": str(OUT), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}", "mageCantrips": len(mage_cantrips), "mageSpells": len(mage_spells), "wizardCantrips": len(wizard_cantrips), "fallbackBinding": rules_binding}, ensure_ascii=False, indent=2))
