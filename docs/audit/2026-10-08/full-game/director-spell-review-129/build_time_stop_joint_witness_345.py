from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zipfile
import zlib
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
OUT = AUDIT / "rank9_time_stop_joint_witness_345_build_output_r4"
PUBLISH = AUDIT / "rank9_time_stop_joint_witness_345_delivery_r4"
RETURN318 = AUDIT / "rank9_time_stop_return318_received"
SOURCES = {
    "catalog": ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "index": ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "core": ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "spells": ROOT / "DescentReviewChanges/ReviewBible/src/data/spells.js",
    "placements": ROOT / "DescentReviewChanges/ReviewBible/src/data/spell-placements.json",
    "wizard": ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json",
    "cleric": ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json",
    "integration": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "combat": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
    "ancestry_background": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def binding(path: pathlib.Path, display: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": display or path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def card_map(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {card["id"]: card for card in source["cards"]}


WIZARD_CHOICES = {
    1: ["wizard.base.arcane-recovery", "wizard.base.spell-scribing", "wizard.base.arcane-bolt", "wizard.base.arcane-shield"],
    2: ["wizard.base.arcane-insight", "wizard.base.matrix-efficiency"],
    3: ["wizard.arch.arcane-sight", "wizard.arch.floating-preparation"],
    4: ["wizard.base.spellbook-study"],
    5: ["wizard.arch.dispel-magic"],
    6: ["wizard.arch.spell-tether"],
    7: ["wizard.arch.spell-efficiency"],
    8: ["wizard.arch.improved-concentration"],
    9: ["wizard.arch.dimensional-pocket"],
    11: ["wizard.arch.arcane-lock"],
    13: ["wizard.base.minor-conjuration"],
    15: ["wizard.base.analyze-magic"],
    17: ["wizard.arch.matrix-mastery"],
}
WIZARD_HERO = {
    10: ["wizard.hero.spellbinder.sigil-authority", "wizard.hero.spellbinder.seal-magic"],
    12: ["wizard.hero.spellbinder.knowledge-shield"],
    14: ["wizard.hero.spellbinder.matrix-sharing"],
    16: ["wizard.hero.spellbinder.arcane-memory"],
}
CLERIC_CHOICES = {
    1: ["cleric.base.conviction-pool", "cleric.base.consecrated-ground", "cleric.base.divine-smite", "cleric.base.healing-rite"],
    2: ["cleric.base.judging-light", "cleric.base.sacred-chant"],
    3: ["cleric.arch.aura-of-faith", "cleric.arch.divine-invocation"],
    4: ["cleric.base.fervent-ritualist"],
    5: ["cleric.arch.liturgical-flow"],
    6: ["cleric.arch.anointed-guardian"],
    7: ["cleric.arch.sanctified-reprisal"],
    8: ["cleric.arch.banish-unholy"],
    9: ["cleric.arch.commune"],
    11: ["cleric.arch.sacrament"],
    13: ["cleric.arch.blessing-of-protection"],
    15: ["cleric.arch.sermon-of-purpose"],
    17: ["cleric.base.consecrate"],
}
CLERIC_HERO = {
    10: ["cleric.hero.priest.scriptural-echo", "cleric.hero.priest.divine-judgment"],
    12: ["cleric.hero.priest.words-of-equilibrium"],
    14: ["cleric.hero.priest.balanced-scales"],
    16: ["cleric.hero.priest.cosmic-equilibrium"],
}


def validate_class_choices(class_id: str, source: dict[str, Any], base: dict[int, list[str]], hero: dict[int, list[str]],
                           hero_path: str, auto: list[dict[str, Any]]) -> None:
    cards = card_map(source)
    schedule = {row["classLevel"]: row for row in source["schedule"]}
    chosen_by_level = {**base, **hero}
    all_ids = [card_id for ids in chosen_by_level.values() for card_id in ids]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError(f"{class_id} build repeats a selectable class card")
    for level in range(1, 18):
        row = schedule[level]
        selected = chosen_by_level.get(level, [])
        if len(selected) != row["choose"]:
            raise ValueError(f"{class_id} level {level}: expected {row['choose']} choices, found {len(selected)}")
        selected_cards = []
        for card_id in selected:
            card = cards.get(card_id)
            if not card:
                raise ValueError(f"unknown {class_id} card: {card_id}")
            if card["minimumClassLevel"] > level:
                raise ValueError(f"{card_id} acquired before its class-level gate")
            if card["band"] not in row["bands"]:
                raise ValueError(f"{card_id} band is illegal at level {level}")
            if card["band"] == "Hero" and not card_id.startswith(f"{class_id.lower()}.hero.{hero_path}."):
                raise ValueError(f"{card_id} is outside the selected Hero path {hero_path}")
            selected_cards.append(card)
        active_count = sum(1 for card in selected_cards if card["sourceKind"] == "active")
        if active_count < row["minimumActives"]:
            raise ValueError(f"{class_id} level {level}: minimum active-card count not met")
    if sorted(hero) != [10, 12, 14, 16]:
        raise ValueError(f"{class_id} Hero choice schedule incomplete")
    if len(auto) != len({item["id"] for item in auto}):
        raise ValueError(f"{class_id} automatic features contain duplicates")


def catalog_index(catalog: dict[str, Any], spell_id: str) -> int:
    for index, row in enumerate(catalog["spells"]):
        if row.get("id") == spell_id:
            return index
    raise ValueError(f"spell is not present in the bound catalog: {spell_id}")


def wizard_cantrips(catalog: dict[str, Any]) -> list[str]:
    rows = []
    for spell in catalog["spells"]:
        access = spell.get("classAccess", {}).get("Wizard")
        if access and access["rank"] == 0 and access["minimumClassLevel"] <= 1:
            rows.append(spell["id"])
    rows.sort()
    if len(rows) < 5:
        raise ValueError("the current Wizard catalog has fewer than five legal cantrips")
    return rows[:5]


def arcane_ward_damage_type(catalog: dict[str, Any], prepared_ids: list[str], school: str) -> tuple[str, str]:
    allowed = ("acid", "cold", "fire", "force", "lightning", "necrotic", "psychic", "radiant", "thunder")
    by_id = {row["id"]: row for row in catalog["spells"]}
    observed: set[str] = set()
    for spell_id in prepared_ids:
        spell = by_id.get(spell_id, {})
        access = spell.get("classAccess", {}).get("Wizard", {})
        if access.get("school") != school:
            continue
        effect_text = " ".join(entry.get("original", {}).get("effect", "")
                                for entry in spell.get("source", {}).get("coreEntries", [])).lower()
        for damage_type in allowed:
            if damage_type in effect_text:
                observed.add(damage_type)
    if observed:
        selected = next(damage_type for damage_type in allowed if damage_type in observed)
        return selected, f"Prepared {school} spell(s) explicitly deal {selected} damage in bound Core entries."
    return "force", f"No prepared {school} spell deals a listed Arcane Ward damage type; force is the source fallback."


def wizard_spellbook(catalog: dict[str, Any], target: str, school: str) -> list[dict[str, Any]]:
    rows = catalog["spells"]
    eligible = []
    for row in rows:
        access = row.get("classAccess", {}).get("Wizard")
        if access and access["rank"] >= 1:
            eligible.append({"id": row["id"], "rank": access["rank"], "minimumClassLevel": access["minimumClassLevel"],
                             "school": access.get("school", row.get("school")),
                             "sourcePath": f"catalog.json#/spells/{catalog_index(catalog, row['id'])}/classAccess/Wizard"})
    book: list[dict[str, Any]] = []
    existing: set[str] = set()
    additions = {1: 6, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
                 9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 5, 16: 5, 17: 6}
    for level, count in additions.items():
        maximum_rank = min(9, (level + 1) // 2)
        pool = [item for item in eligible if item["id"] not in existing and item["minimumClassLevel"] <= level and item["rank"] <= maximum_rank]
        pool.sort(key=lambda item: (item["rank"], item["id"]))
        selected: list[dict[str, Any]] = []
        if level == 1:
            # The six chosen level-one spells are distinct from the separate school bonus.
            selected.extend(pool[:count])
            pool = [item for item in pool if item["id"] not in {row["id"] for row in selected}]
        if level == 17:
            forced = next((item for item in pool if item["id"] == target), None)
            if not forced:
                raise ValueError(f"target spell is not eligible for Wizard acquisition at level 17: {target}")
            selected.append(forced)
            pool.remove(forced)
        if level != 1:
            selected.extend(pool[:count - len(selected)])
        if len(selected) != count:
            raise ValueError(f"Wizard level {level} needs {count} distinct legal spell additions, found {len(selected)}")
        for item in selected:
            entry = {**item, "acquiredAtClassLevel": level,
                     "acquisitionKind": "candidate-level-up-spellbook-entry" if item["id"] == target else "class-playtest-level-up-entry",
                     "sourceStatus": "conditional-pending-spell" if item["id"] == target else "current-catalog-class-access"}
            book.append(entry)
            existing.add(item["id"])
    school_bonus = next((item for item in sorted(eligible, key=lambda row: row["id"])
                         if item["rank"] == 1 and item["minimumClassLevel"] <= 1 and item["school"] == school and item["id"] not in existing), None)
    if not school_bonus:
        raise ValueError(f"no separate legal rank-1 {school} school-bonus spell is available")
    book.insert(6, {**school_bonus, "acquiredAtClassLevel": 1, "acquisitionKind": "arcane-school-specialization-bonus-spell",
                    "sourceStatus": "current-catalog-class-access"})
    existing.add(school_bonus["id"])
    if len(book) != 67 or target not in existing or any(row["rank"] < 1 for row in book):
        raise ValueError("Wizard level-17 spellbook inventory is incomplete")
    return book


def build(actor_id: str, class_name: str, level: int, role: str, target_spell: str,
          catalog: dict[str, Any], wizard_source: dict[str, Any], cleric_source: dict[str, Any],
          casting_school: str, position: list[int], start_rp: int, background: str) -> dict[str, Any]:
    is_wizard = class_name == "Wizard"
    source = wizard_source if is_wizard else cleric_source
    choices = WIZARD_CHOICES if is_wizard else CLERIC_CHOICES
    hero = WIZARD_HERO if is_wizard else CLERIC_HERO
    hero_path = "spellbinder" if is_wizard else "priest"
    auto = ([{"id": "wizard.base.counterspell", "acquiredAtClassLevel": 2, "kind": "automatic", "availability": "candidate-provisional-class-feature",
              "sourcePath": "wizard.json#/engine/26"},
             {"id": "wizard.supplement.ritual-casting", "acquiredAtClassLevel": 2, "kind": "automatic", "sourcePath": "wizard.json#/engine/26"},
             {"id": "wizard.class.arcane-school-specialization", "acquiredAtClassLevel": 1, "kind": "automatic", "selectedSchool": casting_school,
              "sourcePath": "wizard.json#/engine/9"},
             {"id": "wizard.class.arcane-tradition", "acquiredAtClassLevel": 3, "kind": "automatic", "sameSchoolAs": casting_school,
              "sourcePath": "wizard.json#/engine/27"},
             {"id": "wizard.supplement.school-mastery", "acquiredAtClassLevel": 5, "kind": "automatic", "schoolBonusTotal": 2,
              "sourcePath": "wizard.json#/engine/27"},
             {"id": "wizard.supplement.arcane-ward", "acquiredAtClassLevel": 6, "kind": "automatic",
              "sourcePath": "wizard.json#/engine/27"},
             {"id": "wizard.supplement.dual-cast", "acquiredAtClassLevel": 9, "kind": "automatic", "availability": "acquired-uninvoked",
              "invoked": False, "sourcePath": "wizard.json#/engine/27"}]
            if is_wizard else
            [{"id": "cleric.base.invocation-attunement", "acquiredAtClassLevel": 2, "kind": "automatic", "selectedPath": "radiance"},
             {"id": "cleric.arch.bishop-s-mandate", "acquiredAtClassLevel": 9, "kind": "automatic", "selected": False}])
    validate_class_choices(class_name, source, choices, hero, hero_path, auto)

    template_path = RETURN318 / "cases" / ("RANK9TIMEFATE6129-TIME-STOP-A__illusion-max.json" if is_wizard else "RANK9TIMEFATE6129-TIME-STOP-A__universal-reaction.json")
    template = load(template_path)["initialState"]["actors"]["T" if is_wizard else "W"]
    actor = copy.deepcopy(template)
    ancestry = "Scholarly Human" if is_wizard else "Nomadic Human"
    background_record = {
        "name": background,
        "equipment": ["spell focus", "book", "common clothes", "pouch"],
        "featureInvoked": False,
        "sourcePath": "ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
    }
    if background == "Seeker of the Lost Pantheon":
        background_record = {
            "name": background,
            "equipment": ["holy symbol", "fragmented myths", "common clothes", "incense", "pouch"],
            "featureInvoked": False,
            "sourcePath": "ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
        }
    actor.update({
        "id": actor_id,
        "role": role,
        "class": class_name,
        "classLevel": level,
        "classLevels": {class_name: level},
        "ancestry": ancestry,
        "background": background_record,
        "profileId": f"{class_name}{level}-fixture-{actor_id}",
        "abilityScores": ({"STR": 9, "DEX": 14, "CON": 15, "INT": 20, "WIS": 13, "CHA": 11}
                          if is_wizard else {"STR": 10, "DEX": 14, "CON": 14, "INT": 12, "WIS": 20, "CHA": 10}),
        "abilityModifiers": ({"STR": -1, "DEX": 2, "CON": 2, "INT": 5, "WIS": 1, "CHA": 0}
                             if is_wizard else {"STR": 0, "DEX": 2, "CON": 2, "INT": 1, "WIS": 5, "CHA": 0}),
        "proficiencyBonus": 6,
        "PB": 6,
        "castingModifier": 5,
        "saveModifiers": ({"STR": -1, "DEX": 2, "CON": 2, "INT": 11, "WIS": 7, "CHA": 0, "death": 0}
                           if is_wizard else {"STR": 0, "DEX": 2, "CON": 2, "INT": 1, "WIS": 11, "CHA": 0, "death": 0}),
        "abilityScoreHistory": ([{"level": 4, "increase": {"INT": 2}}, {"level": 8, "increase": {"INT": 2}},
                                  {"level": 12, "increase": {"CON": 2}}, {"level": 16, "increase": {"CON": 2}}]
                                 if is_wizard else [{"level": 4, "increase": {"WIS": 2}}, {"level": 8, "increase": {"WIS": 2}},
                                                    {"level": 12, "increase": {"DEX": 1, "CON": 1}}, {"level": 16, "increase": {"DEX": 1, "CON": 1}}]),
        "HP": {"max": 104 if is_wizard else 105, "current": 104 if is_wizard else 105,
               "calculation": ("Level 1 d6 maximum 6 + CON 2; levels 2-17: sixteen d6 rolls of 4 + CON 2 each" if is_wizard
                               else "Level 1 d8 maximum 8 + CON 2; levels 2-16: fifteen d8 rolls of 4 + CON 2 each; level 17 d8 roll of 3 + CON 2; total 105")},
        "hp": 104 if is_wizard else 105,
        "maxHP": 104 if is_wizard else 105,
        "wounds": [],
        "temporaryHP": 0,
        "life": "alive",
        "deathSaves": {"successes": 0, "failures": 0},
        "conditions": [],
        "body": {"living": True, "size": "Medium", "heightFeet": 6, "footprintFeet": [5, 5], "hands": 2,
                 "support": "flat supported floor", "usableHandsBeforeCast": ["left", "right"]},
        "position": position,
        "speed": 30,
        "classPath": hero_path,
        "invocationPath": "radiance" if not is_wizard else None,
        "selectedFeatures": [{"classLevel": level, "cardId": card_id} for level, ids in sorted(choices.items()) for card_id in ids]
                            + [{"classLevel": level, "cardId": card_id} for level, ids in sorted(hero.items()) for card_id in ids],
        "automaticFeatures": auto,
        "unselectedOrUninvokedFeatures": "Every selected class card is listed; all other optional class features, supplements, bonuses and items are explicitly unselected/uninvoked.",
        "spellbook": (wizard_spellbook(catalog, target_spell, casting_school) if is_wizard else None),
        "knownRankedSpellIds": ([item["id"] for item in wizard_spellbook(catalog, target_spell, casting_school)] if is_wizard else [target_spell]),
        "knownCantripIds": wizard_cantrips(catalog) if is_wizard else [],
        "knownCantripAcquisitionHistory": [],
        "preparedRankedSpellIds": ([item["id"] for item in wizard_spellbook(catalog, target_spell, casting_school)
                                     if item["id"] != target_spell][:21] + [target_spell] if is_wizard else [target_spell]),
        "alwaysPreparedClassMatrices": [],
        "preparationLimit": 22 if is_wizard else "not bounded by a numeric count in the bound Cleric source; only the one candidate target is prepared for this fixture",
        "preparationHistory": [],
        "preparedFamilyHistory": [],
        "RP": start_rp,
        "rpMaximum": start_rp,
        "resourceHistory": [],
        "seenFamilies": [],
        "lastSpell": None,
        "spellsThisTurn": 0,
        "regularTurnMagicalCastFlag": False,
        "personalTurnMagicalCastFlag": False,
        "candidateSpellAcquisitions": [{
            "spellId": target_spell,
            "classLevel": 17,
            "rank": 9,
            "school": casting_school,
            "status": "candidate-only; identity pending; no prior/campaign acquisition claimed",
            "sourcePath": f"catalog.json#/spells/{catalog_index(catalog, target_spell)}/classAccess/{class_name}",
        }],
        "knowledge": [{"id": "class-access:" + target_spell, "status": "candidate", "sourcePointer": "catalog.classAccess." + class_name}],
        "spellAccessSource": "current catalog classAccess plus Core Systems V2 rank/class-level facts; candidate spell is not operational or accepted",
        "initiative": {"score": 12, "tieBreakerActorId": actor_id, "order": 1 if actor_id in ("C", "T") else 2},
        "regularSchedule": {"startMarkersMs": [], "endMarkersMs": [], "nextStartMs": 6000, "nextEndMs": None},
        "nextRegularStart": 6000,
        "nextRegularEnd": None,
        "currentRegularStart": None,
        "regularStarts": [],
        "regularEnds": [],
        "recharge": {},
        "resistances": [],
        "concentration": None,
        "ready": None,
        "nullExposure": {},
        "nullVeil": False,
        "outsideTicks": [],
        "injuries": [],
        "awards": [],
        "nukeChain": [],
    })
    actor["RP"] = start_rp
    actor["rpMaximum"] = start_rp
    if is_wizard:
        book = actor["spellbook"]
        prepared = actor["preparedRankedSpellIds"]
        actor["preparationHistory"] = [{"sourcePath": "wizard.json#/engine/4", "completedAfterLongRest": True,
            "durationMinutes": 45, "matrixEfficiencyApplied": True, "preparedRankedSpellIds": copy.deepcopy(prepared),
            "preparationLimit": 22, "modifications": [], "preparedFamilyHistory": [],
            "spellbookSnapshotIds": [row["id"] for row in book], "candidateFixtureOnly": True}]
        actor["knownCantripAcquisitionHistory"] = [{"classLevel": level, "spellIds": actor["knownCantripIds"][offset:offset + count],
            "sourcePath": "wizard.json#/engine/31", "knownDirectly": True, "preparedMatrixPositionUsed": False}
            for level, offset, count in ((1, 0, 3), (4, 3, 1), (10, 4, 1))]
        actor["preparedFamilyHistory"] = [{"matrixSpellId": spell_id, "familyId": spell_id, "initialEncounterFamilyCast": False}
            for spell_id in prepared]
        selected_ids = [row["cardId"] for row in actor["selectedFeatures"]]
        class_matrix_ids = []
        for card in wizard_source["cards"]:
            if card["id"] in selected_ids and "wizard-spell" in card.get("effect", ""):
                class_matrix_ids.append(card["id"])
        if "wizard.base.counterspell" in card_map(wizard_source):
            class_matrix_ids.append("wizard.base.counterspell")
        actor["alwaysPreparedClassMatrices"] = [{"cardId": card_id,
            "rank": (1 if card_id == "wizard.base.counterspell" else card_map(wizard_source)[card_id].get("spellRank")),
            "sourcePath": f"wizard.json#/cards/{next(i for i, card in enumerate(wizard_source['cards']) if card['id'] == card_id)}",
            "preparedMatrixPositionUsed": False, "acquisitionStatus": "selected-or-automatic-candidate-fixture"}
            for card_id in sorted(set(class_matrix_ids))]
        actor["spellbookAcquisitionHistory"] = [{"spellId": row["id"], "rank": row["rank"],
            "acquiredAtClassLevel": row["acquiredAtClassLevel"], "sourcePath": row["sourcePath"],
            "acquisitionKind": row["acquisitionKind"], "cost": "no money or scribing time for level-up entry"}
            for row in book]
        actor["schoolBonuses"] = {"selectedSchool": casting_school, "spellAttackBonus": 2, "spellSaveDCBonus": 2,
            "sourcePaths": ["wizard.json#/engine/9", "wizard.json#/engine/27"], "schoolMasteryAddsToSpecializationTotal": True}
        actor["abilityCheckBonuses"] = {"counterspell": 1, "dispelMagic": 1,
            "sourceCardId": "wizard.hero.spellbinder.sigil-authority", "sourcePath": "wizard.json#/cards/" +
            str(next(i for i, card in enumerate(wizard_source["cards"]) if card["id"] == "wizard.hero.spellbinder.sigil-authority"))}
        ward_type, ward_reason = arcane_ward_damage_type(catalog, prepared, casting_school)
        actor["resistances"] = [ward_type]
        actor["arcaneWardChoice"] = {"damageType": ward_type, "reason": ward_reason,
            "sourcePath": "wizard.json#/cards/" + str(next(i for i, card in enumerate(wizard_source["cards"]) if card["id"] == "wizard.supplement.arcane-ward"))}
        ward_feature = next(row for row in actor["automaticFeatures"] if row["id"] == "wizard.supplement.arcane-ward")
        ward_feature["resistanceChoice"] = ward_type
    if not (is_wizard and casting_school == "Divination"):
        actor["finiteUses"].pop("divinationFailedSaveReroll", None)
    return actor


def prepare_arcane_sight_before_encounter(actor: dict[str, Any], wizard_source: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    selected = {row["cardId"] for row in actor.get("selectedFeatures", [])}
    if actor["class"] != "Wizard" or "wizard.arch.arcane-sight" not in selected:
        return None
    card = card_map(wizard_source)["wizard.arch.arcane-sight"]
    if card.get("activation") != "Action" or card.get("cost") != "2 RP" or "Concentration" not in card.get("duration", ""):
        raise ValueError("bound Arcane Sight card does not support the required paid activation and concentration")
    before = actor["RP"]
    if before < 2:
        raise ValueError(f"{actor['id']} lacks RP for Arcane Sight")
    actor["RP"] -= 2
    cast_id = f"{actor['id']}-ARCANE-SIGHT-PRE-ENCOUNTER"
    effect_id = f"arcane-sight-{actor['id']}"
    card_index = next(i for i, row in enumerate(wizard_source["cards"]) if row["id"] == "wizard.arch.arcane-sight")
    cast = {"id": cast_id, "actor": actor["id"], "spellId": "wizard.arch.arcane-sight", "sourceCardId": "wizard.arch.arcane-sight",
        "rank": card.get("spellRank"), "school": "Divination", "activation": "Action", "actualPaid": 2, "basePaid": 2,
        "RPBefore": before, "RPAfter": actor["RP"], "DissonanceBefore": actor["Dissonance"], "baseDissonanceApplied": 0,
        "DissonanceAfter": actor["Dissonance"], "RefrainBefore": actor["Refrain"], "RefrainAfter": actor["Refrain"],
        "firstSameNameFamilyCast": True, "atWorldMs": -60000,
        "counterWindow": "pre-encounter; no eligible responder", "status": "candidate-pre-encounter-paid-activation",
        "encounterFamilyRecorded": False, "candidateAcquisitionOnly": True,
        "sourcePath": f"wizard.json#/cards/{card_index}", "concentrationEffectId": effect_id}
    actor["resourceHistory"].append(copy.deepcopy(cast))
    actor["lastSpell"] = "wizard.arch.arcane-sight"
    actor["recharge"]["wizard.arch.arcane-sight"] = {"roundsRemaining": 0, "roundsRequired": 2,
        "castAtWorldMs": -60000, "rechargedByWorldTimeBeforeEncounter": -48000,
        "ticksDuringPersonalTurns": 0, "sourcePath": f"wizard.json#/cards/{card_index}"}
    actor["concentration"] = {"id": effect_id, "spellId": "wizard.arch.arcane-sight", "sourceCardId": "wizard.arch.arcane-sight",
        "startedAtWorldMs": -60000, "maxDeadlineWorldMs": 540000, "status": "active", "sourcePath": f"wizard.json#/cards/{card_index}"}
    effect = {"applicationId": effect_id, "sourceCastId": cast_id, "spellId": "wizard.arch.arcane-sight",
        "sourceCardId": "wizard.arch.arcane-sight", "caster": actor["id"], "recipient": actor["id"], "status": "active",
        "startedAtWorldMs": -60000, "originalDeadlineWorldMs": 540000, "maxDurationMs": 600000, "concentration": True,
        "rangeFeet": 60, "totalCoverBlocksSight": True, "detectsVisibleMagicAuras": True, "candidateAcquisitionOnly": True,
        "sourcePath": f"wizard.json#/cards/{card_index}"}
    transaction = {"id": cast_id + "-PAY", "actor": actor["id"], "kind": "RP_COMMIT", "amount": 2,
        "before": before, "after": actor["RP"], "atWorldMs": -60000, "sourcePath": f"wizard.json#/cards/{card_index}"}
    return cast, effect, transaction


def root_state(caster: dict[str, Any], peer: dict[str, Any], mode: str, wizard_source: dict[str, Any]) -> dict[str, Any]:
    peer["budget"] = {"Action": 1, "BonusAction": 1, "Reaction": 1, "extraAction": 0, "interaction": 1, "movement": 30}
    peer["currentRegularStart"] = 0
    peer["regularStarts"] = [0]
    peer["regularSchedule"]["startMarkersMs"] = [0]
    peer["nextRegularStart"] = 6000
    peer["regularSchedule"]["nextStartMs"] = 6000
    caster["budget"] = {"Action": 1, "BonusAction": 1, "Reaction": 1, "extraAction": 0, "interaction": 1, "movement": 30}
    caster["currentRegularStart"] = None
    caster["nextRegularStart"] = 6000
    caster["regularSchedule"]["nextStartMs"] = 6000
    peer["initiative"] = {"score": 15, "tieBreakerActorId": "P", "order": 1}
    caster["initiative"] = {"score": 12, "tieBreakerActorId": "C", "order": 2}
    precasts = [prepare_arcane_sight_before_encounter(actor, wizard_source) for actor in (caster, peer)]
    precasts = [row for row in precasts if row is not None]
    pre_casts = [row[0] for row in precasts]
    pre_effects = {row[1]["applicationId"]: row[1] for row in precasts}
    pre_transactions = [row[2] for row in precasts]
    clock_ledger = [{"kind": "PRE_ENCOUNTER_PAID_ACTION_CAST", "actor": row[0]["actor"], "sourceCastId": row[0]["id"],
        "atWorldMs": -60000, "effectDeadlineWorldMs": 540000, "outsideEncounter": True, "sourcePath": row[0]["sourcePath"]}
        for row in precasts]
    clock_ledger.append({"kind": "REGULAR_START", "actor": "P", "atWorldMs": 0, "scheduleRound": 1,
        "initiativeOrder": 1, "sourcePath": "COMBAT_ACTION_PLAYTEST.md#L60"})
    return {
        "actors": {caster["id"]: caster, peer["id"]: peer},
        "auditHistory": [], "awards": [], "casts": pre_casts, "causalHistory": [], "clockLedger": clock_ledger,
        "custodyHistory": [], "damage": [], "effects": pre_effects, "futureEvidence": None, "heldFacts": [],
        "items": {
            "focus-C": {"id": "focus-C", "type": "class casting focus", "owner": caster["id"], "custodian": caster["id"], "position": caster["position"], "destroyed": False, "heldIn": "left", "use": "F component; no consumption"},
            "focus-P": {"id": "focus-P", "type": "class casting focus", "owner": peer["id"], "custodian": peer["id"], "position": peer["position"], "destroyed": False, "heldIn": "left", "use": "F component; no consumption"},
            "door": {"id": "door", "type": "existing unlocked supported hinged door", "owner": "scene", "custodian": "scene", "position": [0, 5, 0], "open": False, "destroyed": False, "clearance": "hinge and swing have verified empty adjacent space"},
            "book-C": {"id": "book-C", "type": "spellbook or class list ledger", "owner": caster["id"], "custodian": caster["id"], "destroyed": False, "contents": caster["knownRankedSpellIds"]},
            "book-P": {"id": "book-P", "type": "spellbook or class list ledger", "owner": peer["id"], "custodian": peer["id"], "destroyed": False, "contents": peer["knownRankedSpellIds"]},
        },
        "obligations": {}, "outcomes": [], "perception": {"lineOfEffect": True, "mutualSight": True,
            "perceivedCasting": [], "publicRollPolicy": "fixture die results are explicitly labeled; no live RNG"},
        "rolls": [], "schema": "TF192-FULL-STATE-1", "transactions": pre_transactions,
        "world": {"activeHistory": "TF318-WITNESS-FIXTURE-345", "calendarYearSeconds": 34560000,
                  "encounterEpochMs": 0, "historyVersion": 0, "mode": "combat", "nowMs": 0,
                  "ordinaryRound": 1, "paused": False,
                  "scene": "finite supported room: open floor, one unlocked hinged door, no hidden actors/solids/remotes",
                  "temporalInterval": None},
        "fixtureMode": "AUTHORED_CONDITIONAL_REVIEW_FIXTURE_ONLY",
        "campaignEvent": False,
        "runtimeExecuted": False,
        "humanPlayExecuted": False,
    }


def add_event(case: dict[str, Any], state: dict[str, Any], kind: str, inputs: dict[str, Any], narrative: str,
              mutate) -> None:
    before = copy.deepcopy(state)
    mutate(state)
    after = copy.deepcopy(state)
    event_id = f"{case['id']}:{len(case['events']) + 1}"
    case["events"].append({
        "id": event_id, "kind": kind, "inputs": inputs, "narrative": narrative,
        "beforeSHA256": sha(canonical(before)), "afterSHA256": sha(canonical(after)),
        "before": before, "after": after,
        "forward": [{"op": "test", "path": "", "value": before}, {"op": "replace", "path": "", "value": after}],
        "inverse": [{"op": "test", "path": "", "value": after}, {"op": "replace", "path": "", "value": before}],
    })


def cast_record(actor: dict[str, Any], spell_id: str, at: int, cost: int, school: str, cast_id: str,
                budget: str, action: str = "commit") -> dict[str, Any]:
    before_rp = actor["RP"]
    if before_rp < cost:
        raise ValueError(f"{actor['id']} lacks RP for {spell_id}")
    first_family = spell_id not in actor["seenFamilies"]
    base_dissonance = 0 if actor["class"] == "Wizard" and first_family else 2
    before_dissonance = actor["Dissonance"]
    actor["RP"] -= cost
    actor["Dissonance"] += base_dissonance
    actor["lastSpell"] = spell_id
    actor["spellsThisTurn"] += 1
    actor["regularTurnMagicalCastFlag"] = True
    actor["seenFamilies"].append(spell_id)
    rec = {"id": cast_id, "actor": actor["id"], "spellId": spell_id, "rank": 9 if spell_id in ("time-stop", "timeless-form") else 3,
           "school": school, "actualPaid": cost, "basePaid": cost, "surcharge": 0, "RPBefore": before_rp,
           "RPAfter": actor["RP"], "DissonanceBefore": before_dissonance, "baseDissonanceApplied": base_dissonance,
           "preDissonance": before_dissonance, "DissonanceAfter": actor["Dissonance"],
           "RefrainBefore": actor["Refrain"], "RefrainAfter": actor["Refrain"], "firstSameNameFamilyCast": first_family,
           "firstPreparedMatrixFamilyCast": first_family, "dissonanceRule": "wizard.json#/engine/11" if actor["class"] == "Wizard" else "ordinary Cleric base Dissonance",
           "components": ["V", "S", "F"], "focusItemId": f"focus-{actor['id']}", "budget": budget,
           "atWorldMs": at, "status": "candidate-committed-review-fixture", "candidateAcquisitionOnly": True,
           "counterWindow": "pending"}
    actor["resourceHistory"].append(copy.deepcopy(rec))
    return rec


def start_case(case_id: str, scope: str, caster_class: str, mode: str, catalog: dict[str, Any],
               wizard_source: dict[str, Any], cleric_source: dict[str, Any], target_behavior: str) -> dict[str, Any]:
    caster_school = "Universal" if caster_class == "Cleric" else "Illusion"
    caster_rp = 48 if caster_class == "Cleric" else 64
    caster = build("C", caster_class, 17, "time-stop-caster", "time-stop", catalog, wizard_source, cleric_source,
                   caster_school, [50, 0, 0], caster_rp,
                   "Seeker of the Lost Pantheon" if caster_class == "Cleric" else "Arcane Academy Dropout")
    peer = build("P", "Wizard", 17, "independent-timeless-form-peer", "timeless-form", catalog, wizard_source, cleric_source,
                 "Transmutation", [0, 0, 0], 64, "Arcane Academy Dropout")
    state = root_state(caster, peer, mode, wizard_source)
    case = {"id": case_id, "schema": "TF192-FULL-STATE-1", "spellId": "time-stop", "linkedSpellId": "timeless-form",
            "kind": "conditional-authored-witness", "branch": target_behavior, "status": "CANDIDATE_FIXTURE_REPLAY_REQUIRED",
            "requirementIds": ["TF9-STOP-MODES", "TF9-PERSISTENCE", "TF318-JOINT-INTERFACE-01"],
            "holdIds": ["TF192-B01", "DF218-B03"], "scenarioPremise": "Authored conditional fixture characters only. Every spell acquisition and paid cast is a candidate under TF318; no campaign, runtime, RNG service or human-play event is claimed.",
            "initialState": copy.deepcopy(state), "events": []}

    # The peer casts Timeless Form during a real scheduled Action; its original
    # sixty-second world deadline is stored once and is never restarted.
    def peer_commit_tf(s: dict[str, Any]) -> None:
        p = s["actors"]["P"]
        rec = cast_record(p, "timeless-form", 0, 26, "Transmutation", case_id + "-TF", "Action")
        s["casts"].append(rec)
        s["transactions"].append({"id": case_id + "-TF-PAYMENT", "actor": "P", "kind": "RP_COMMIT", "amount": 26,
            "before": rec["RPBefore"], "after": rec["RPAfter"], "atWorldMs": s["world"]["nowMs"]})
        p["budget"]["Action"] = 0
    add_event(case, state, "TIMELESS_FORM_CAST_COMMIT", {"actor": "P", "target": "P", "baseRP": 26, "atWorldMs": 0},
              "Commit Timeless Form's Action and RP once. Its effect has not resolved yet; the eligible interruption window follows commitment.", peer_commit_tf)

    def timeless_counter_window(s: dict[str, Any]) -> None:
        if mode == "Action":
            s["actors"]["C"].setdefault("decisions", []).append({"kind": "COUNTERSPELL_DECLINE", "triggeringCastId": case_id + "-TF",
                "sourceCardId": "wizard.base.counterspell", "eligible": True, "perceived": True, "rangeFeet": 50, "rangeLimitFeet": 60,
                "reactionBefore": 1, "decision": "decline", "RPSpent": 0, "ReactionSpent": False})
            s["auditHistory"].append({"kind": "COUNTER_WINDOW_CLOSED", "castId": case_id + "-TF", "eligibleResponders": ["C"], "allDecisionsRecorded": True})
        else:
            s["auditHistory"].append({"kind": "COUNTER_WINDOW_CLOSED", "castId": case_id + "-TF", "eligibleResponders": [],
                "noOtherCreatureHasAnAcquiredCounterspell": True, "allDecisionsRecorded": True})
    add_event(case, state, "TIMELESS_FORM_COUNTER_WINDOW", {"triggeringCastId": case_id + "-TF", "casterMode": mode},
              "After commitment and before resolution, resolve every eligible Timeless Form cast interrupter: the other Wizard explicitly declines in Action mode; the Cleric mode has no qualified Counterspell responder.", timeless_counter_window)

    def resolve_timeless_form(s: dict[str, Any]) -> None:
        p = s["actors"]["P"]
        p["resourceHistory"][-1]["counterWindow"] = "resolved before surviving cast effect"
        s["casts"][-1]["counterWindow"] = "resolved before surviving cast effect"
        s["casts"][-1]["status"] = "candidate-cast-resolved-review-fixture"
        p["speed"] = 35
        p["budget"]["movement"] = 35
        p["turnScopedSpeedBonus"] = {"amount": 5, "sourcePath": "wizard.json#/engine/10",
            "triggerCastId": case_id + "-TF", "expiresAt": "end-of-current-regular-turn", "status": "active"}
        s["effects"]["timeless-form-P"] = {"applicationId": case_id + "-TF-APP", "spellId": "timeless-form", "caster": "P", "recipient": "P",
            "status": "active", "concentration": False, "startedAtWorldMs": 0, "originalDeadlineWorldMs": 60000,
            "remainingMsAtStart": 60000, "protections": ["aging", "time-stop", "haste", "slow"],
            "candidateAcquisitionOnly": True, "sourceCastId": case_id + "-TF"}
        s["clockLedger"].append({"kind": "SOURCE_START", "sourceId": "timeless-form-P", "atWorldMs": 0,
            "originalDeadlineWorldMs": 60000, "clockDomain": "world-elapsed-ms", "afterCounterWindow": True})
        s["custodyHistory"].append({"itemId": "focus-P", "from": "P", "to": "P", "atWorldMs": 0, "event": "used as F; remains in custody; not consumed"})
    add_event(case, state, "TIMELESS_FORM_SURVIVING_CAST_RESOLUTION", {"triggeringCastId": case_id + "-TF", "atWorldMs": 0},
              "The explicit interruption window closed without a successful counter, so Timeless Form resolves now and its original 60,000ms deadline begins.", resolve_timeless_form)

    def end_peer_regular(s: dict[str, Any]) -> None:
        p = s["actors"]["P"]
        p["regularEnds"].append(50)
        p["regularSchedule"]["endMarkersMs"].append(50)
        p["currentRegularStart"] = None
        p["budget"] = {"Action": 0, "BonusAction": 0, "Reaction": 1, "extraAction": 0, "interaction": 0, "movement": 0}
        p["regularTurnMagicalCastFlag"] = True
        p["speed"] = 30
        p["turnScopedSpeedBonus"] = {"amount": 5, "sourcePath": "wizard.json#/engine/10",
            "triggerCastId": case_id + "-TF", "expiresAt": 50, "status": "expired-at-regular-turn-end"}
        p["nextRegularStart"] = 6000
        s["world"]["nowMs"] = 50
        s["clockLedger"].append({"kind": "REGULAR_END", "actor": "P", "atWorldMs": 50, "candidateCastFlagRetained": True,
            "transmutationSpeedBonusExpired": True, "sourcePath": "wizard.json#/engine/10"})
    if mode == "Action":
        add_event(case, state, "REGULAR_TURN_END", {"actor": "P", "atWorldMs": 50}, "P ends the ordinary turn; unused wallet is discarded and the actual regular cast flag remains set.", end_peer_regular)

    def advance_to_caster(s: dict[str, Any]) -> None:
        s["world"]["nowMs"] = 100
        c = s["actors"]["C"]
        c["currentRegularStart"] = 100
        if mode == "Action":
            c["regularStarts"].append(100)
            c["regularSchedule"]["startMarkersMs"].append(100)
            c["budget"] = {"Action": 1, "BonusAction": 1, "Reaction": 1, "extraAction": 0, "interaction": 1, "movement": 30}
        else:
            c["currentRegularStart"] = None
            c["budget"] = {"Action": 0, "BonusAction": 0, "Reaction": 1, "extraAction": 0, "interaction": 0, "movement": 0}
        s["clockLedger"].append({"kind": "WORLD_ADVANCE", "fromWorldMs": 50, "toWorldMs": 100,
            "dueMarkersProcessed": [], "ordinaryRound": 1})
        if mode == "Action":
            s["clockLedger"].append({"kind": "REGULAR_START", "actor": "C", "atWorldMs": 100,
                "scheduleRound": 1, "ordinaryRound": 1, "sourcePath": "COMBAT_ACTION_PLAYTEST.md#L60"})
    if mode == "Action":
        add_event(case, state, "ADVANCE_TO_CAST", {"fromWorldMs": 50, "toWorldMs": 100}, "Advance to the next resolved cast window; no source marker is due.", advance_to_caster)

    if mode == "Universal":
        def universal_trigger(s: dict[str, Any]) -> None:
            s["perception"]["perceivedCasting"].append({"observer": "C", "actor": "P", "action": "cast timeless-form", "distanceFeet": 50,
                "lineOfEffect": True, "segmentFullyResolved": True, "nextAtomicEventPending": True})
            s["clockLedger"].append({"kind": "OTHER_CREATURE_ACTION_SEGMENT_RESOLVED", "actor": "P", "eventId": case_id + "-TF", "atWorldMs": s["world"]["nowMs"]})
        add_event(case, state, "UNIVERSAL_REACTION_TRIGGER", {"actor": "P", "action": "Timeless Form cast", "observer": "C", "distanceFeet": 50,
             "loE": True, "beforeNextAtomicEvent": True}, "The triggering Action is fully resolved and perceived within 120ft/LoE; Cleric has one real Reaction remaining.", universal_trigger)

    def commit_time_stop(s: dict[str, Any]) -> None:
        c = s["actors"]["C"]
        at = s["world"]["nowMs"]
        rec = cast_record(c, "time-stop", at, 26, caster_school, case_id + "-TS", "Reaction" if mode == "Universal" else "Action")
        rec["mode"] = mode
        rec["route"] = "Cleric/Universal/Reaction/3 turns" if mode == "Universal" else "Wizard/Illusion/Action/1d4+1 rounds"
        rec["d4"] = 1 if mode == "Action" else None
        rec["turnsGranted"] = 3 if mode == "Universal" else 2
        rec["triggeringEventId"] = case_id + "-TF" if mode == "Universal" else None
        s["casts"].append(rec)
        s["transactions"].append({"id": case_id + "-TS-PAYMENT", "actor": "C", "kind": "RP_COMMIT", "amount": 26,
            "before": rec["RPBefore"], "after": rec["RPAfter"], "atWorldMs": at})
        c["budget"]["Action"] = 0 if mode == "Action" else c["budget"]["Action"]
        if mode == "Universal":
            c["budget"]["Reaction"] = 0
            s["clockLedger"].append({"kind": "REACTION_SPENT", "actor": "C", "triggeringEventId": case_id + "-TF", "atWorldMs": at})
        s["perception"]["perceivedCasting"].append({"observer": "P", "actor": "C", "action": "cast time-stop", "distanceFeet": 50,
            "lineOfEffect": True, "identifiedEffect": "time-stop", "atWorldMs": at})
    add_event(case, state, "PAID_TIME_STOP_COMMIT", {"actor": "C", "mode": mode, "baseRP": 26, "atWorldMs": state["world"]["nowMs"],
             "d4": 1 if mode == "Action" else None, "turnsGranted": 3 if mode == "Universal" else 2},
             "Commit the exact class route/cost/components once; the d4 result is fixed before resolution for Action mode.", commit_time_stop)

    def counter_decision(s: dict[str, Any]) -> None:
        s["actors"]["P"]["decisions"] = s["actors"]["P"].get("decisions", []) + [{"kind": "COUNTERSPELL_DECLINE", "triggeringCastId": case_id + "-TS",
            "sourceCardId": "wizard.base.counterspell", "eligible": True, "perceived": True, "rangeFeet": 50, "rangeLimitFeet": 60,
            "reactionBefore": 1, "decision": "decline", "RPSpent": 0, "ReactionSpent": False}]
        s["auditHistory"].append({"kind": "COUNTER_WINDOW_CLOSED", "castId": case_id + "-TS", "eligibleResponders": ["P"], "allDecisionsRecorded": True})
        s["actors"]["C"]["resourceHistory"][-1]["counterWindow"] = "resolved after eligible responder explicitly declined"
        s["casts"][-1]["counterWindow"] = "resolved after eligible responder explicitly declined"
    add_event(case, state, "COUNTER_WINDOW_DECISION", {"responder": "P", "eligible": True, "decision": "decline"},
              "P has an available Wizard2 Counterspell and perceives the cast within 60ft; P explicitly declines, so no resource or Reaction is spent.", counter_decision)

    def open_stop(s: dict[str, Any]) -> None:
        p, c = s["actors"]["P"], s["actors"]["C"]
        s["casts"][-1]["status"] = "candidate-cast-resolved-review-fixture"
        n = 3 if mode == "Universal" else 2
        anchor = s["world"]["nowMs"]
        s["effects"]["time-stop"] = {"applicationId": case_id + "-TS-APP", "sourceCastId": case_id + "-TS", "caster": "C",
            "status": "active", "mode": mode, "worldAnchorMs": anchor, "roundsGranted": n, "roundsUsed": 0,
            "d4Result": 1 if mode == "Action" else None, "actorPhasesByRound": [["C", "P"] for _ in range(n)],
            "candidateAcquisitionOnly": True}
        s["world"]["paused"] = True
        s["world"]["nowMs"] = anchor
        s["world"]["temporalInterval"] = {"source": case_id + "-TS", "mode": mode, "d4": 1 if mode == "Action" else None,
            "turnsGranted": n, "turnsUsed": 0, "worldAnchorMs": anchor,
            "ordinaryWallet": {"C": copy.deepcopy(c["budget"]), "P": copy.deepcopy(p["budget"])},
            "originalRegularMarkers": {"C": c["nextRegularStart"], "P": p["nextRegularStart"]},
            "ordinaryClockCursor": {"worldNowMs": anchor, "ordinaryRound": s["world"]["ordinaryRound"],
                "currentRegularStart": {"C": c["currentRegularStart"], "P": p["currentRegularStart"]},
                "nextRegularStart": {"C": c["nextRegularStart"], "P": p["nextRegularStart"]},
                "initiativeOrder": ["P", "C"]},
            "peerEligibility": {"P": {"timelessFormApplicationId": case_id + "-TF-APP", "operativeAtOpen": True,
                "deadlineWorldMs": 60000, "independentAgency": True}}, "personalPhaseCursor": None,
            "frozenActors": ["nonimmune-outsiders"], "worldClockFrozen": True}
        s["clockLedger"].append({"kind": "TIME_STOP_OPEN", "atWorldMs": anchor, "worldAnchorMs": anchor, "d4": 1 if mode == "Action" else None,
            "turnsGranted": n, "regularMarkersFrozen": True, "timeFormDeadline": 60000})
    add_event(case, state, "TIME_STOP_OPEN", {"worldAnchorMs": state["world"]["nowMs"], "turnsGranted": 3 if mode == "Universal" else 2,
             "immunePeer": "P"}, "Open one paused interval; retain both ordinary wallets and deadlines. Timeless Form is operative, but its world clock freezes.", open_stop)

    case["initialState"] = case["initialState"]
    case["caseStartedAfterBuild"] = True
    case["identityScopeIds"] = ["time-stop"]
    return case, state


def temporal_start(case: dict[str, Any], state: dict[str, Any], actor_id: str, round_no: int) -> None:
    def mutate(s: dict[str, Any]) -> None:
        actor = s["actors"][actor_id]
        actor["budget"] = {"Action": 1, "BonusAction": 1, "Reaction": actor["budget"]["Reaction"], "extraAction": 0,
                           "interaction": 1, "movement": actor["speed"]}
        actor["personalTurnMagicalCastFlag"] = False
        actor["personalTurnCasts"] = 0
        anchor = s["world"]["temporalInterval"]["worldAnchorMs"]
        actor["currentTemporalPhase"] = {"round": round_no, "actor": actor_id, "phaseId": f"{case['id']}-R{round_no}-{actor_id}", "worldAnchorMs": anchor}
        s["world"]["temporalInterval"]["personalPhaseCursor"] = {"round": round_no, "actor": actor_id, "phase": "START"}
        s["clockLedger"].append({"kind": "PERSONAL_PHASE_START", "round": round_no, "actor": actor_id, "phaseId": f"{case['id']}-R{round_no}-{actor_id}",
            "worldTimeMs": anchor, "separateTemporalOrdinal": len(s["clockLedger"]) + 1, "regularStartCreated": False,
            "ordinaryRechargeTick": False, "wallet": copy.deepcopy(actor["budget"])})
        if actor_id == "P":
            form = s["effects"]["timeless-form-P"]
            if form["status"] != "active" or form["originalDeadlineWorldMs"] != 60000:
                raise ValueError("immune peer is no longer operative at its scheduled personal phase")
            s["clockLedger"][-1]["peerEligibility"] = {"sourceId": "timeless-form-P", "operative": True,
                "independentAgency": True, "originalDeadlineWorldMs": form["originalDeadlineWorldMs"]}
    add_event(case, state, "PERSONAL_PHASE_START", {"round": round_no, "actor": actor_id},
              "Create one separate personal wallet without advancing world time or regular clocks.", mutate)


def move_peer(case: dict[str, Any], state: dict[str, Any], round_no: int, destination: list[int], open_door: bool = False) -> None:
    def mutate(s: dict[str, Any]) -> None:
        p = s["actors"]["P"]
        start = copy.deepcopy(p["position"])
        if open_door:
            s["items"]["door"]["open"] = True
            p["budget"]["interaction"] = 0
        p["position"] = destination
        s["items"]["focus-P"]["position"] = copy.deepcopy(destination)
        distance = sum(abs(a - b) for a, b in zip(start, destination))
        p["budget"]["movement"] -= distance
        s["clockLedger"].append({"kind": "IMMUNE_PEER_MOVEMENT", "actor": "P", "round": round_no, "from": start, "to": destination,
            "distanceFeet": distance, "speed": p["speed"], "doorOpened": open_door, "worldTimeMs": s["world"]["temporalInterval"]["worldAnchorMs"],
            "remainingMovement": p["budget"]["movement"], "independentActionSource": case["id"] + "-TF-APP"})
    add_event(case, state, "IMMUNE_PEER_INDEPENDENT_MOVEMENT", {"round": round_no, "actor": "P", "destination": destination, "openDoor": open_door},
              "The independently operative peer uses ordinary movement through finite supported geometry; no movement or world-clock event is created for frozen outsiders.", mutate)


def restore_ordinary_wallets(state: dict[str, Any], interval: dict[str, Any]) -> dict[str, Any]:
    cursor = interval["ordinaryClockCursor"]
    restored: dict[str, Any] = {}
    for actor_id in ("C", "P"):
        actor = state["actors"][actor_id]
        wallet = copy.deepcopy(interval["ordinaryWallet"][actor_id])
        # Reactions are shared across personal and ordinary turns; retain their live value.
        wallet["Reaction"] = actor["budget"]["Reaction"]
        actor["budget"] = wallet
        actor["currentTemporalPhase"] = None
        actor["currentRegularStart"] = cursor["currentRegularStart"][actor_id]
        actor["nextRegularStart"] = cursor["nextRegularStart"][actor_id]
        actor["regularSchedule"]["nextStartMs"] = cursor["nextRegularStart"][actor_id]
        restored[actor_id] = {"budget": copy.deepcopy(wallet),
            "currentRegularStart": actor["currentRegularStart"], "nextRegularStart": actor["nextRegularStart"]}
    state["world"]["nowMs"] = cursor["worldNowMs"]
    return {"worldAnchorMs": cursor["worldNowMs"], "actors": restored, "restoredExactlyOnce": True,
        "sharedReactionOverlaid": True, "unusedTemporalWalletsDiscarded": True}


def detect_time_stop_with_arcane_sight(case: dict[str, Any], state: dict[str, Any], actor_id: str,
                                       wizard_source: dict[str, Any]) -> None:
    effect_id = f"arcane-sight-{actor_id}"
    arcane = state["effects"].get(effect_id, {})
    concentration = state["actors"][actor_id].get("concentration") or {}
    if arcane.get("status") != "active" or concentration.get("id") != effect_id:
        raise ValueError(f"{actor_id} lacks active concentration-bound Arcane Sight")
    remaining = arcane.get("originalDeadlineWorldMs", -1) - state["world"]["nowMs"]
    if remaining <= 0:
        raise ValueError("Arcane Sight's source-bound duration expired before perception")
    source_position = state["actors"][actor_id]["position"]
    target_position = state["actors"]["C"]["position"]
    distance = round(sum((a - b) ** 2 for a, b in zip(source_position, target_position)) ** 0.5)
    if distance > 60 or not state["perception"].get("lineOfEffect"):
        raise ValueError("Arcane Sight cannot perceive the Time Stop aura at the recorded range/LoE")
    card_index = next(i for i, card in enumerate(wizard_source["cards"]) if card["id"] == "wizard.arch.arcane-sight")
    def mutate(s: dict[str, Any]) -> None:
        record = {"observer": actor_id, "effectId": case["id"] + "-TS-APP", "effect": "time-stop",
            "distanceFeet": distance, "lineOfEffect": True, "perceivedBeforeActionCommit": True,
            "perceptionRoute": {"sourceCardId": "wizard.arch.arcane-sight",
                "activationRecordId": f"{actor_id}-ARCANE-SIGHT-PRE-ENCOUNTER", "effectId": effect_id,
                "acquired": True, "paidRP": 2, "activeConcentration": True, "rangeFeet": 60,
                "remainingMsAtPerception": remaining, "sourceDeadlineWorldMs": arcane["originalDeadlineWorldMs"],
                "totalCoverBlocksSight": True, "sourcePath": f"wizard.json#/cards/{card_index}"},
            "atWorldMs": s["world"]["nowMs"]}
        s["perception"].setdefault("perceivedEffects", []).append(record)
        s["actors"][actor_id].setdefault("perceivedEffects", []).append(copy.deepcopy(record))
        s["clockLedger"].append({"kind": "ARCANE_SIGHT_DETECTS_TIME_STOP_AURA", "observer": actor_id,
            "effectId": case["id"] + "-TS-APP", "sourceEffectId": effect_id,
            "atWorldMs": s["world"]["nowMs"], "distanceFeet": distance, "lineOfEffect": True})
    add_event(case, state, "ARCANE_SIGHT_DETECTS_TIME_STOP", {"observer": actor_id, "sourceEffectId": effect_id,
        "atWorldMs": state["world"]["nowMs"], "distanceFeet": distance, "lineOfEffect": True},
        "Before committing Dispel Magic, active paid Arcane Sight detects Time Stop's visible aura within 60 feet and unobstructed line of effect.", mutate)


def commit_arch_dispel(case: dict[str, Any], state: dict[str, Any], actor_id: str) -> str:
    actor = state["actors"][actor_id]
    if actor["class"] != "Wizard" or not any(row["cardId"] == "wizard.arch.dispel-magic" for row in actor["selectedFeatures"]):
        raise ValueError(f"{actor_id} lacks the selected Wizard Arch Dispel card")
    if actor["budget"].get("Action", 0) < 1:
        raise ValueError(f"{actor_id} has no Action to commit Arch Dispel")
    observed = any(row.get("observer") == actor_id and row.get("effectId") == case["id"] + "-TS-APP" and row.get("perceivedBeforeActionCommit")
                   for row in state["perception"].get("perceivedEffects", []))
    if not observed:
        raise ValueError("Arch Dispel cannot commit before lawful effect-specific perception")
    def mutate(s: dict[str, Any]) -> None:
        a = s["actors"][actor_id]
        a["budget"]["Action"] = 0
        before = a["RP"]
        if before < 3:
            raise ValueError(f"{actor_id} lacks RP for Arch Dispel")
        dissonance_before = a["Dissonance"]
        refrain_before = a["Refrain"]
        first_family = "wizard.arch.dispel-magic" not in a["seenFamilies"]
        base_dissonance = 0 if first_family else 2
        a["RP"] -= 3
        a["Dissonance"] += base_dissonance
        a["lastSpell"] = "wizard.arch.dispel-magic"
        a["personalTurnMagicalCastFlag"] = True
        a["personalTurnCasts"] = a.get("personalTurnCasts", 0) + 1
        a["spellsThisTurn"] += 1
        a["regularTurnMagicalCastFlag"] = True
        a["seenFamilies"].append("wizard.arch.dispel-magic")
        round_no = a["currentTemporalPhase"]["round"]
        cast_id = f"{case['id']}-{actor_id}-DISPEL-{round_no}"
        a["recharge"]["wizard.arch.dispel-magic"] = {"roundsRemaining": 2, "roundsRequired": 2,
            "setAtTemporalRound": round_no, "ticksDuringPersonalTurns": 0, "sourcePath": "wizard.json#/cards/19"}
        cast = {"id": cast_id, "actor": actor_id, "spellId": "wizard.arch.dispel-magic", "sourceCardId": "wizard.arch.dispel-magic",
            "targetEffectId": case["id"] + "-TS-APP", "spellRank": 3, "targetEffectRank": 9, "dispelCardRank": 3,
            "actualPaid": 3, "basePaid": 3, "surcharge": 0, "RPBefore": before, "RPAfter": a["RP"],
            "DissonanceBefore": dissonance_before, "baseDissonanceApplied": base_dissonance, "DissonanceAfter": a["Dissonance"],
            "RefrainBefore": refrain_before, "RefrainAfter": a["Refrain"], "firstSameNameFamilyCast": first_family,
            "firstPreparedMatrixFamilyCast": first_family, "dissonanceRule": "wizard.json#/engine/11",
            "activation": "Action", "rangeFeet": 50, "targetPerceived": True, "perceivedBeforeActionCommit": True,
            "perceptionSourceEffectId": f"arcane-sight-{actor_id}", "lineOfEffect": True,
            "counterWindow": "pending", "status": "candidate-cast-committed-review-fixture", "check": None,
            "components": ["V", "S", "F"], "focusItemId": f"focus-{actor_id}", "candidateAcquisitionOnly": True}
        a["resourceHistory"].append(copy.deepcopy(cast))
        s["casts"].append(cast)
        s["transactions"].append({"id": cast_id + "-PAY", "actor": actor_id, "kind": "RP_COMMIT", "amount": 3,
            "before": before, "after": a["RP"], "worldTimeMs": s["world"]["nowMs"]})
        s["clockLedger"].append({"kind": "ARCH_DISPEL_CAST_COMMITMENT", "actor": actor_id, "round": round_no,
            "castId": cast_id, "worldTimeMs": s["world"]["nowMs"], "outcome": "pending", "rechargeTicks": 0})
        s.setdefault("custodyHistory", []).append({"itemId": f"focus-{actor_id}", "from": actor_id, "to": actor_id,
            "atWorldMs": s["world"]["nowMs"], "event": "used as F for Arch Dispel; remains in custody; not consumed"})
    before_count = len(state["casts"])
    add_event(case, state, "ARCH_DISPEL_CAST_COMMIT", {"actor": actor_id, "targetEffectId": case["id"] + "-TS-APP",
        "spellRank": 3, "targetEffectRank": 9, "baseRP": 3, "counterWindow": "pending"},
        f"{actor_id} commits the selected rank-3 Wizard Arch Dispel after lawful perception. Costs and Recharge2 commit before Counterspell decisions; the check and effect have not resolved.", mutate)
    if len(state["casts"]) != before_count + 1:
        raise ValueError("Arch Dispel commitment did not append exactly one cast")
    return state["casts"][-1]["id"]


def resolve_arch_dispel(case: dict[str, Any], state: dict[str, Any], cast_id: str, die: int, outcome: str) -> None:
    modifier = 5 + 6 + 1  # INT + proficiency + selected Sigil Authority.
    total = die + modifier
    success = total >= 19
    if success != (outcome == "success"):
        raise ValueError("dispel die/result mismatch")
    if not state["casts"] or state["casts"][-1]["id"] != cast_id or state["casts"][-1]["counterWindow"] == "pending":
        raise ValueError("Arch Dispel resolution must follow its completed cast-interruption window")
    def mutate(s: dict[str, Any]) -> None:
        cast = s["casts"][-1]
        actor = s["actors"][cast["actor"]]
        cast["check"] = {"die": die, "INTModifier": 5, "PB": 6, "sigilAuthorityBonus": 1,
            "total": total, "DC": 19, "outcome": outcome}
        cast["status"] = "candidate-cast-resolved-review-fixture"
        actor["resourceHistory"][-1]["check"] = copy.deepcopy(cast["check"])
        actor["resourceHistory"][-1]["status"] = cast["status"]
        s["rolls"].append({"id": cast_id + "-CHECK", "kind": "WIZARD_ARCH_DISPEL", "die": die,
            "modifier": modifier, "modifierParts": {"INT": 5, "PB": 6, "SigilAuthority": 1},
            "total": total, "dc": 19, "outcome": outcome,
            "stipulatedBeforeResolution": True, "liveRandomness": False})
        s["clockLedger"].append({"kind": "ARCH_DISPEL_RESOLUTION", "actor": cast["actor"],
            "round": actor["currentTemporalPhase"]["round"], "castId": cast_id,
            "worldTimeMs": s["world"]["nowMs"], "outcome": outcome, "rechargeTicks": 0, "afterCounterWindow": True})
        if success:
            stop = s["effects"]["time-stop"]
            stop["status"] = "ended-by-successful-arch-dispel"
            stop["endedAtWorldMs"] = s["world"]["nowMs"]
            stop["endedByCastId"] = cast_id
            interval = s["world"]["temporalInterval"]
            interval["terminatedAtTemporalPhase"] = copy.deepcopy(actor["currentTemporalPhase"])
            interval["terminationCause"] = "successful source-qualified Arch Dispel after cast-interruption window"
            interval["discardedFuturePhases"] = [["P"]] if cast["actor"] == "C" and interval["turnsGranted"] >= 2 else []
            interval["cleanupExactlyOnce"] = True
            interval["cleanupRecord"] = restore_ordinary_wallets(s, interval)
            s["auditHistory"].append({"kind": "TIME_STOP_EARLY_CLEANUP", **copy.deepcopy(interval["cleanupRecord"])})
            s["world"]["paused"] = False
            s["world"]["temporalInterval"] = None
        else:
            s["effects"]["time-stop"]["status"] = "active-after-failed-dispel"
    add_event(case, state, "ARCH_DISPEL_CHECK_AND_EFFECT_RESOLUTION", {"castId": cast_id, "die": die,
        "modifier": modifier, "dc": 19, "expected": outcome, "afterCounterWindow": True},
        f"Resolve the already-committed rank-3 Dispel after all eligible Counterspell decisions: {die}+{modifier}={total} against DC19 ({outcome}). The target is rank9; success ends the exact captured Time Stop source.", mutate)


def phase_end(case: dict[str, Any], state: dict[str, Any], actor_id: str, round_no: int) -> None:
    def mutate(s: dict[str, Any]) -> None:
        a = s["actors"][actor_id]
        prior = copy.deepcopy(a["budget"])
        a["budget"] = {"Action": 0, "BonusAction": 0, "Reaction": a["budget"]["Reaction"], "extraAction": 0, "interaction": 0, "movement": 0}
        s["clockLedger"].append({"kind": "PERSONAL_PHASE_END", "round": round_no, "actor": actor_id,
            "phaseId": a["currentTemporalPhase"]["phaseId"], "worldTimeMs": s["world"]["temporalInterval"]["worldAnchorMs"], "unusedWalletDiscarded": prior,
            "regularClockAdvanced": False, "rechargeTick": False})
        if s["world"]["temporalInterval"] is not None:
            s["world"]["temporalInterval"]["personalPhaseCursor"] = {"round": round_no, "actor": actor_id, "phase": "END"}
            if actor_id == "P":
                s["world"]["temporalInterval"]["turnsUsed"] += 1
                s["effects"]["time-stop"]["roundsUsed"] = s["world"]["temporalInterval"]["turnsUsed"]
        a["currentTemporalPhase"] = None
    add_event(case, state, "PERSONAL_PHASE_END", {"round": round_no, "actor": actor_id},
              "End this personal phase, discard unused temporal wallet, preserve shared Reaction and every ordinary deadline; no recharge or regular marker ticks.", mutate)


def close_natural(case: dict[str, Any], state: dict[str, Any]) -> None:
    def mutate(s: dict[str, Any]) -> None:
        interval = s["world"]["temporalInterval"]
        expected = interval["turnsGranted"]
        if interval["turnsUsed"] != expected:
            raise ValueError("natural closure attempted before all caster and peer rounds")
        s["effects"]["time-stop"]["status"] = "naturally-completed-after-final-peer-end"
        s["effects"]["time-stop"]["endedAtWorldMs"] = interval["worldAnchorMs"]
        s["effects"]["time-stop"]["closureEvent"] = "final-immune-peer-phase-end"
        interval["cleanupRecord"] = restore_ordinary_wallets(s, interval)
        s["auditHistory"].append({"kind": "TIME_STOP_NATURAL_CLEANUP", **copy.deepcopy(interval["cleanupRecord"])})
        s["world"]["paused"] = False
        s["world"]["temporalInterval"] = None
        s["clockLedger"].append({"kind": "TIME_STOP_NATURAL_CLOSE", "atWorldMs": s["world"]["nowMs"], "afterFinalScheduledActor": "P",
            "finalPeerPhaseCompleted": True, "worldClockResumedAtAnchor": s["world"]["nowMs"]})
        for aid in ("C", "P"):
            s["actors"][aid]["regularTurnMagicalCastFlag"] = s["actors"][aid]["spellsThisTurn"] > 0
    add_event(case, state, "TIME_STOP_NATURAL_CLOSE", {"worldTimeMs": state["world"]["nowMs"], "requiredLastActor": "P"},
              "Close only after every caster and immune-peer round; restore the original world cursor/wallet and keep Timeless Form's original deadline.", mutate)


def resume_and_expire(case: dict[str, Any], state: dict[str, Any], deadline: int) -> None:
    # Once ordinary time resumes, process two actor markers in stable initiative order
    # at each genuine 6-second round. No temporal round advances this schedule.
    for actor_id in ("P", "C"):
        if state["actors"][actor_id]["currentRegularStart"] is not None:
            def finish_open_turn(s: dict[str, Any], aid=actor_id) -> None:
                a = s["actors"][aid]
                anchor = s["world"]["nowMs"]
                a["budget"] = {"Action": 0, "BonusAction": 0, "Reaction": a["budget"]["Reaction"],
                    "extraAction": 0, "interaction": 0, "movement": 0}
                a["regularEnds"].append(anchor)
                a["regularSchedule"]["endMarkersMs"].append(anchor)
                a["currentRegularStart"] = None
                if a.get("turnScopedSpeedBonus", {}).get("status") == "active":
                    a["speed"] = 30
                    a["turnScopedSpeedBonus"]["status"] = "expired-at-regular-turn-end"
                    a["turnScopedSpeedBonus"]["expiresAt"] = anchor
                a["nextRegularStart"] = 6000
                a["regularSchedule"]["nextStartMs"] = 6000
                s["clockLedger"].append({"kind": "REGULAR_TURN_RESUMED_AND_ENDED", "actor": aid,
                    "atWorldMs": anchor, "resumedFromSameCursor": True, "unusedOrdinaryWalletDiscarded": True,
                    "sourcePath": "COMBAT_ACTION_PLAYTEST.md#L60"})
            add_event(case, state, "REGULAR_TURN_RESUMED_AND_ENDED", {"actor": actor_id, "atWorldMs": state["world"]["nowMs"]},
                "Resume the interrupted ordinary turn at its saved cursor, then close it before the next scheduled START.", finish_open_turn)
    for tick in range(6000, deadline, 6000):
        for actor_id in ("P", "C"):
            def regular_start(s: dict[str, Any], aid=actor_id, when=tick) -> None:
                a = s["actors"][aid]
                if a["regularTurnMagicalCastFlag"]:
                    a["spellsThisTurn"] = 0
                    a["regularTurnMagicalCastFlag"] = False
                reaction_before = a["budget"]["Reaction"]
                a["budget"] = {"Action": 1, "BonusAction": 1, "Reaction": 1, "extraAction": 0, "interaction": 1, "movement": a["speed"]}
                a.setdefault("reactionRefreshHistory", []).append({"atWorldMs": when, "before": reaction_before, "after": 1,
                    "rule": "refresh at each regular own-turn start", "sourcePath": "COMBAT_ACTION_PLAYTEST.md#L35"})
                a["currentRegularStart"] = when
                a["regularStarts"].append(when)
                a["regularSchedule"]["startMarkersMs"].append(when)
                a["regularSchedule"]["nextStartMs"] = when + 6000
                a["nextRegularStart"] = when + 6000
                s["world"]["nowMs"] = when
                s["world"]["ordinaryRound"] = when // 6000 + 1
                recharge_before = copy.deepcopy(a["recharge"])
                for key, record in a["recharge"].items():
                    if isinstance(record, dict) and record.get("roundsRemaining", 0) > 0:
                        record["roundsRemaining"] -= 1
                        record.setdefault("ticksAtRegularStarts", []).append(when)
                s["clockLedger"].append({"kind": "REGULAR_START", "actor": aid, "atWorldMs": when, "scheduleRound": when // 6000 + 1,
                    "rechargeTick": True, "rechargeBefore": recharge_before, "rechargeAfter": copy.deepcopy(a["recharge"]),
                    "phaseDomain": "ordinary-world", "reactionRefresh": {"before": reaction_before, "after": 1,
                        "sourcePath": "COMBAT_ACTION_PLAYTEST.md#L35"}})
            add_event(case, state, "REGULAR_START", {"actor": actor_id, "atWorldMs": tick},
                      "Process one actual regular START in stable initiative order after resumption; temporal turns did not create this tick.", regular_start)
            def regular_end(s: dict[str, Any], aid=actor_id, when=tick) -> None:
                a = s["actors"][aid]
                a["budget"] = {"Action": 0, "BonusAction": 0, "Reaction": a["budget"]["Reaction"], "extraAction": 0, "interaction": 0, "movement": 0}
                a["regularEnds"].append(when)
                a["regularSchedule"]["endMarkersMs"].append(when)
                a["currentRegularStart"] = None
                if a.get("turnScopedSpeedBonus", {}).get("status") == "active":
                    a["speed"] = 30
                    a["turnScopedSpeedBonus"]["status"] = "expired-at-regular-turn-end"
                    a["turnScopedSpeedBonus"]["expiresAt"] = when
                s["clockLedger"].append({"kind": "REGULAR_END", "actor": aid, "atWorldMs": when,
                    "scheduleRound": when // 6000 + 1, "sourcePath": "COMBAT_ACTION_PLAYTEST.md#L60"})
            add_event(case, state, "REGULAR_END", {"actor": actor_id, "atWorldMs": tick},
                      "Close this ordinary turn without altering any source deadline or replaying an action.", regular_end)
    def expire(s: dict[str, Any]) -> None:
        s["world"]["nowMs"] = deadline
        effect = s["effects"]["timeless-form-P"]
        if deadline != effect["originalDeadlineWorldMs"]:
            raise ValueError("Timeless Form did not expire at its original deadline")
        effect["status"] = "expired-before-any-later-payload"
        effect["expiredAtWorldMs"] = deadline
        s["clockLedger"].append({"kind": "SOURCE_EXPIRE", "sourceId": "timeless-form-P", "atWorldMs": deadline,
            "originalDeadlineWorldMs": effect["originalDeadlineWorldMs"], "processedBeforeLaterPayload": True})
    add_event(case, state, "TIMELESS_FORM_ORIGINAL_DEADLINE", {"deadlineWorldMs": deadline, "payloadAfterExpiry": False},
              "After world time resumes, expire Timeless Form exactly at its original stored deadline; no personal-turn extension or catch-up occurs.", expire)


def finish_case(case: dict[str, Any], state: dict[str, Any], final_status: str) -> dict[str, Any]:
    case["finalState"] = copy.deepcopy(state)
    case["status"] = final_status
    case["counts"] = {"events": len(case["events"]),
        "forwardOperations": sum(len(event["forward"]) for event in case["events"]),
        "inverseOperations": sum(len(event["inverse"]) for event in case["events"])}
    return case


def make_action_natural(catalog: dict[str, Any], wizard: dict[str, Any], cleric: dict[str, Any]) -> dict[str, Any]:
    case, state = start_case("TF318-345-ACTION-NATURAL", "time-stop", "Wizard", "Action", catalog, wizard, cleric, "natural-completion-action-mode")
    rounds = 2
    for round_no in range(1, rounds + 1):
        temporal_start(case, state, "C", round_no)
        phase_end(case, state, "C", round_no)
        temporal_start(case, state, "P", round_no)
        if round_no == 1:
            move_peer(case, state, round_no, [0, 5, 0], open_door=True)
        else:
            move_peer(case, state, round_no, [0, 15, 0], open_door=False)
        phase_end(case, state, "P", round_no)
    close_natural(case, state)
    resume_and_expire(case, state, 60000)
    return finish_case(case, state, "DEMONSTRATED_CONDITIONAL_FIXTURE")


def make_universal_natural(catalog: dict[str, Any], wizard: dict[str, Any], cleric: dict[str, Any]) -> dict[str, Any]:
    case, state = start_case("TF318-345-CLERIC-UNIVERSAL-NATURAL", "time-stop", "Cleric", "Universal", catalog, wizard, cleric, "natural-completion-cleric-universal")
    rounds = 3
    for round_no in range(1, rounds + 1):
        temporal_start(case, state, "C", round_no)
        phase_end(case, state, "C", round_no)
        temporal_start(case, state, "P", round_no)
        move_peer(case, state, round_no, [0, 5 + round_no * 5, 0], open_door=(round_no == 1))
        phase_end(case, state, "P", round_no)
    close_natural(case, state)
    resume_and_expire(case, state, 60000)
    return finish_case(case, state, "DEMONSTRATED_CONDITIONAL_FIXTURE")


def make_failed_then_interrupted(catalog: dict[str, Any], wizard: dict[str, Any], cleric: dict[str, Any]) -> dict[str, Any]:
    case, state = start_case("TF318-345-ACTION-FAILED-THEN-INTERRUPTED", "time-stop", "Wizard", "Action",
        catalog, wizard, cleric, "failed-removal-then-successful-legal-interruption")
    temporal_start(case, state, "C", 1)
    phase_end(case, state, "C", 1)
    temporal_start(case, state, "P", 1)
    detect_time_stop_with_arcane_sight(case, state, "P", wizard)
    p_cast_id = commit_arch_dispel(case, state, "P")
    def caster_declines_counterspell(s: dict[str, Any]) -> None:
        s["actors"]["C"].setdefault("decisions", []).append({"kind": "COUNTERSPELL_DECLINE", "triggeringCastId": p_cast_id,
            "sourceCardId": "wizard.base.counterspell", "eligible": True, "perceived": True, "rangeFeet": 50, "rangeLimitFeet": 60,
            "reactionBefore": 1, "decision": "decline", "RPSpent": 0, "ReactionSpent": False})
        s["casts"][-1]["counterWindow"] = "resolved after eligible responder explicitly declined"
        s["actors"]["P"]["resourceHistory"][-1]["counterWindow"] = "resolved after eligible responder explicitly declined"
        s["auditHistory"].append({"kind": "COUNTER_WINDOW_CLOSED", "castId": p_cast_id,
            "eligibleResponders": ["C"], "allDecisionsRecorded": True})
    add_event(case, state, "DISPEL_COUNTERSPELL_WINDOW_CASTER_DECLINES", {"responder": "C", "castId": p_cast_id,
        "eligible": True, "decision": "decline"},
        "After P commits the rank-3 Dispel and before its check resolves, eligible Wizard C explicitly declines Counterspell; no Reaction or RP is spent.",
        caster_declines_counterspell)
    resolve_arch_dispel(case, state, p_cast_id, 1, "failure")
    phase_end(case, state, "P", 1)
    temporal_start(case, state, "C", 2)
    detect_time_stop_with_arcane_sight(case, state, "C", wizard)
    c_cast_id = commit_arch_dispel(case, state, "C")
    def peer_declines_counterspell(s: dict[str, Any]) -> None:
        s["actors"]["P"].setdefault("decisions", []).append({"kind": "COUNTERSPELL_DECLINE", "triggeringCastId": c_cast_id,
            "sourceCardId": "wizard.base.counterspell", "eligible": True, "perceived": True, "rangeFeet": 50, "rangeLimitFeet": 60,
            "reactionBefore": 1, "decision": "decline", "RPSpent": 0, "ReactionSpent": False})
        s["casts"][-1]["counterWindow"] = "resolved after eligible responder explicitly declined"
        s["actors"]["C"]["resourceHistory"][-1]["counterWindow"] = "resolved after eligible responder explicitly declined"
        s["auditHistory"].append({"kind": "COUNTER_WINDOW_CLOSED", "castId": c_cast_id,
            "eligibleResponders": ["P"], "allDecisionsRecorded": True})
    add_event(case, state, "DISPEL_COUNTERSPELL_WINDOW_PEER_DECLINES", {"responder": "P", "castId": c_cast_id,
        "eligible": True, "decision": "decline"},
        "After C commits the rank-3 Dispel and before its check resolves, eligible Wizard P explicitly declines Counterspell; no Reaction or RP is spent.",
        peer_declines_counterspell)
    resolve_arch_dispel(case, state, c_cast_id, 8, "success")
    case["terminationRecord"] = {"phase": "C round 2", "successfulCastId": c_cast_id,
        "failedCastId": p_cast_id, "failedAttemptCostsAndRechargeRetained": True,
        "peerRound2OmittedBecauseIntervalEnded": True, "peerRechargeDidNotTick": True,
        "sourceDeadlinePreserved": 60000, "timelessFormRemainsActiveUntilOriginalDeadline": True,
        "checkTotals": {"P": {"die": 1, "modifier": 12, "total": 13, "DC": 19, "outcome": "failure"},
                        "C": {"die": 8, "modifier": 12, "total": 20, "DC": 19, "outcome": "success"}}}
    resume_and_expire(case, state, 60000)
    case["finalState"] = copy.deepcopy(state)
    case["status"] = "DEMONSTRATED_CONDITIONAL_FIXTURE"
    case["counts"] = {"events": len(case["events"]), "forwardOperations": sum(len(e["forward"]) for e in case["events"]),
        "inverseOperations": sum(len(e["inverse"]) for e in case["events"])}
    return case


def verify_case(case: dict[str, Any]) -> dict[str, Any]:
    def apply(state: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
        result = copy.deepcopy(state)
        for operation in operations:
            if operation.get("path") != "":
                raise ValueError("this packet supports exact root-state replacement only")
            if operation["op"] == "test":
                if canonical(result) != canonical(operation["value"]):
                    raise ValueError("state precondition failed")
            elif operation["op"] == "replace":
                result = copy.deepcopy(operation["value"])
            else:
                raise ValueError("unknown reversible operation")
        return result

    failures: list[str] = []
    state = copy.deepcopy(case["initialState"])
    total_forward = total_inverse = 0
    for event in case["events"]:
        before, after = event["before"], event["after"]
        if canonical(state) != canonical(before) or sha(canonical(before)) != event["beforeSHA256"] or sha(canonical(after)) != event["afterSHA256"]:
            failures.append(event["id"] + ": continuity/hash")
            break
        try:
            state = apply(state, event["forward"])
            if canonical(state) != canonical(after):
                raise ValueError("forward operations did not produce the recorded after-state")
            if canonical(apply(state, event["inverse"])) != canonical(before):
                raise ValueError("inverse operations did not restore the recorded before-state")
        except (KeyError, TypeError, ValueError) as error:
            failures.append(event["id"] + ": " + str(error))
            break
        total_forward += len(event["forward"])
        total_inverse += len(event["inverse"])
    if canonical(state) != canonical(case["finalState"]):
        failures.append("final forward replay mismatch")
    try:
        reverse = copy.deepcopy(case["finalState"])
        for event in reversed(case["events"]):
            reverse = apply(reverse, event["inverse"])
        if canonical(reverse) != canonical(case["initialState"]):
            failures.append("full reverse replay did not restore initial state")
    except (KeyError, TypeError, ValueError) as error:
        failures.append("full reverse replay: " + str(error))
    if total_forward != total_inverse:
        failures.append("forward/inverse counts differ")

    final = case["finalState"]
    source = final["effects"].get("timeless-form-P", {})
    stop = final["effects"].get("time-stop", {})
    if source.get("originalDeadlineWorldMs") != 60000 or source.get("status") != "expired-before-any-later-payload" or source.get("expiredAtWorldMs") != 60000:
        failures.append("Timeless Form did not retain and expire at its original world deadline")
    if final["world"]["paused"] or final["world"]["temporalInterval"] is not None:
        failures.append("final state retained an open Time Stop interval")
    if not stop.get("status", "").startswith(("naturally-completed", "ended-by-successful")):
        failures.append("ended Time Stop source record is missing")
    for actor_id, actor in final["actors"].items():
        if actor["class"] == "Wizard":
            book = actor.get("spellbook") or []
            book_ids = [row.get("id") for row in book]
            if len(book) != 67 or len(book_ids) != len(set(book_ids)) or any(row.get("rank", 0) < 1 for row in book):
                failures.append(f"{actor_id}: Wizard spellbook must contain 67 distinct ranked spells and no cantrips")
            if actor.get("knownRankedSpellIds") != book_ids:
                failures.append(f"{actor_id}: known ranked spells do not bind the complete spellbook")
            if len(actor.get("knownCantripIds", [])) != 5 or set(actor["knownCantripIds"]) & set(book_ids):
                failures.append(f"{actor_id}: Wizard cantrips are not represented separately")
            prepared = actor.get("preparedRankedSpellIds", [])
            if len(prepared) != 22 or len(prepared) != len(set(prepared)) or not set(prepared) <= set(book_ids):
                failures.append(f"{actor_id}: prepared matrices do not match the level+INT limit")
            auto_ids = {row.get("id") for row in actor.get("automaticFeatures", [])}
            required_auto = {"wizard.base.counterspell", "wizard.supplement.ritual-casting", "wizard.supplement.school-mastery",
                "wizard.supplement.arcane-ward", "wizard.supplement.dual-cast"}
            if not required_auto <= auto_ids:
                failures.append(f"{actor_id}: automatic Wizard progression features are incomplete")
            dual = next((row for row in actor["automaticFeatures"] if row["id"] == "wizard.supplement.dual-cast"), {})
            if dual.get("invoked") is not False:
                failures.append(f"{actor_id}: Dual Cast acquisition/invocation state is not explicit")
            if actor.get("resistances") != [actor.get("arcaneWardChoice", {}).get("damageType")]:
                failures.append(f"{actor_id}: Arcane Ward chosen resistance and effect state disagree")
        elif actor.get("HP", {}).get("max") != 105 or actor.get("hp") != 105 or actor.get("maxHP") != 105:
            failures.append(f"{actor_id}: Cleric HP calculation must resolve to 105 consistently")
    temporal_rows = [row for row in case["events"] if row["kind"] in ("PERSONAL_PHASE_START", "PERSONAL_PHASE_END", "IMMUNE_PEER_MOVEMENT")]
    opened = next((event for event in case["events"] if event["kind"] == "TIME_STOP_OPEN"), None)
    anchor = opened["after"]["world"]["temporalInterval"]["worldAnchorMs"] if opened else None
    for row in temporal_rows:
        clock = row["after"]["clockLedger"][-1]
        if clock.get("worldTimeMs") != anchor:
            failures.append(row["id"] + ": personal event advanced world time")
    if case["branch"].startswith("natural"):
        if case["events"][-1]["kind"] != "TIMELESS_FORM_ORIGINAL_DEADLINE":
            failures.append("natural branch did not process the original deadline last")
        if stop.get("status") != "naturally-completed-after-final-peer-end":
            failures.append("natural branch ended before final peer END")
        if not any(event["kind"] == "REGULAR_TURN_RESUMED_AND_ENDED" for event in case["events"]):
            failures.append("natural branch omitted saved ordinary-turn cleanup before expiry")
    else:
        failures_seen = [event for event in case["events"] if event["kind"] == "ARCH_DISPEL_CHECK_AND_EFFECT_RESOLUTION" and event["inputs"]["expected"] == "failure"]
        successes = [event for event in case["events"] if event["kind"] == "ARCH_DISPEL_CHECK_AND_EFFECT_RESOLUTION" and event["inputs"]["expected"] == "success"]
        if len(failures_seen) != 1 or len(successes) != 1:
            failures.append("interruption branch lacks the failed and successful paid Dispel attempts")
        elif failures_seen[0]["after"]["world"]["temporalInterval"] is None or failures_seen[0]["after"]["actors"]["P"]["recharge"].get("wizard.arch.dispel-magic", {}).get("roundsRemaining") != 2:
            failures.append("failed removal did not preserve Time Stop and Recharge2")
        elif failures_seen[0]["after"]["casts"][-1]["check"] != {"die": 1, "INTModifier": 5, "PB": 6, "sigilAuthorityBonus": 1,
                "total": 13, "DC": 19, "outcome": "failure"}:
            failures.append("failed Dispel does not use the actual 1d20+12 modifier")
        if successes and successes[0]["after"]["casts"][-1]["check"].get("total") != 20:
            failures.append("successful Dispel does not use the actual 8+12 total")
        for resolution in failures_seen + successes:
            cast_id = resolution["inputs"].get("castId")
            index = case["events"].index(resolution)
            if index == 0 or case["events"][index - 1]["kind"] not in ("DISPEL_COUNTERSPELL_WINDOW_CASTER_DECLINES", "DISPEL_COUNTERSPELL_WINDOW_PEER_DECLINES"):
                failures.append(f"{resolution['id']}: Dispel resolved before its Counterspell window")
            cast = resolution["after"]["casts"][-1]
            if cast.get("spellRank") != 3 or cast.get("targetEffectRank") != 9:
                failures.append(f"{resolution['id']}: Dispel cast rank and target effect rank are conflated")
        if successes and (successes[0]["after"]["world"]["temporalInterval"] is not None or successes[0]["after"]["actors"]["C"].get("currentTemporalPhase") is not None):
            failures.append("successful interruption did not close and clean up mid-phase")
    return {"caseId": case["id"], "events": len(case["events"]), "forwardOperations": total_forward,
            "inverseOperations": total_inverse, "fullReversePassed": not any("reverse" in item for item in failures),
            "passed": not failures, "failures": failures}


def write_member(path: pathlib.Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def main() -> None:
    if OUT.exists() or PUBLISH.exists():
        raise RuntimeError(f"Refusing to overwrite existing witness build/delivery output: {OUT} / {PUBLISH}")
    OUT.mkdir(parents=True)
    for p in SOURCES.values():
        if not p.is_file():
            raise FileNotFoundError(p)
    catalog = load(SOURCES["catalog"])
    wizard = load(SOURCES["wizard"])
    cleric = load(SOURCES["cleric"])
    cases = [make_action_natural(catalog, wizard, cleric), make_universal_natural(catalog, wizard, cleric),
             make_failed_then_interrupted(catalog, wizard, cleric)]

    # All fourteen prior records are retained byte-exact and are not replayed or rewritten.
    preserved_case_paths = sorted((RETURN318 / "cases").glob("*.json"))
    if len(preserved_case_paths) != 14:
        raise ValueError(f"Expected 14 exact preserved Time Stop cases, found {len(preserved_case_paths)}")
    members: dict[str, bytes] = {}
    for key, path in SOURCES.items():
        name = {
            "catalog": "evidence/sources/catalog.json", "index": "evidence/sources/authored_review_index.json",
            "core": "evidence/sources/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
            "spells": "evidence/sources/spells.js", "placements": "evidence/sources/spell-placements.json",
            "wizard": "evidence/sources/class_playtests/wizard.json", "cleric": "evidence/sources/class_playtests/cleric.json",
            "integration": "evidence/sources/SPELL_INTEGRATION_RULES.md",
            "combat": "evidence/sources/COMBAT_ACTION_PLAYTEST.md",
            "ancestry_background": "evidence/sources/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
        }[key]
        members[name] = path.read_bytes()
    members["evidence/TF318_JOINT_INTERFACE_CONTRACT.md"] = (RETURN318 / "TF318_JOINT_INTERFACE_CONTRACT.md").read_bytes()
    members["evidence/JOINT_INTERFACE_AUTHORIZATION.json"] = (RETURN318 / "JOINT_INTERFACE_AUTHORIZATION.json").read_bytes()
    members["evidence/TIME_STOP_RETURN318_RECEIPT.json"] = (AUDIT / "TIME_STOP_RETURN318_RECEIPT.json").read_bytes()
    members["evidence/TF318_DIRECTOR_SCOPE.json"] = pretty({
        "authorizationId": "TF318-JOINT-INTERFACE-01", "status": "AUTHORIZED_FOR_CONDITIONAL_WITNESS_CONSTRUCTION_ONLY",
        "scopeIds": ["time-stop"], "linkedPendingComparisonId": "timeless-form", "canonicalFilesChanged": False,
        "runtimeAuthorized": False, "applicationAuthorized": False, "preservedCasesReplayed": False,
    })
    for path in preserved_case_paths:
        members["cases/preserved/" + path.name] = path.read_bytes()
    for case in cases:
        members["cases/new/" + case["id"] + ".json"] = pretty(case)

    source_rows = []
    for key, path in SOURCES.items():
        source_rows.append(binding(path))
    preserved_rows = [{"path": path.name, "bytes": len(path.read_bytes()), "sha256": sha(path.read_bytes())} for path in preserved_case_paths]
    case_rows = [{"path": "cases/new/" + case["id"] + ".json", "bytes": len(pretty(case)), "sha256": sha(pretty(case)),
                  "events": len(case["events"]), "forwardOperations": case["counts"]["forwardOperations"],
                  "inverseOperations": case["counts"]["inverseOperations"], "status": case["status"]} for case in cases]
    archive_members = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(members.items())]
    manifest = {"id": "TF318-345-WITNESS-MEMBER-MANIFEST", "schema": "TF318-CONDITIONAL-WITNESS-1",
                "memberCount": len(archive_members) + 1, "payloadMemberCount": len(archive_members), "members": archive_members,
                "preservedCaseCount": 14, "newConditionalCaseCount": len(cases)}
    members["MEMBER_MANIFEST.json"] = pretty(manifest)
    members["ACTOR_AND_SOURCE_BINDINGS.json"] = pretty({
        "id": "TF318-345-ACTOR-SOURCE-BINDINGS", "contractId": "TF318-JOINT-INTERFACE-01",
        "sourceBindings": source_rows, "preservedCaseBindings": preserved_rows, "newCases": case_rows,
        "actors": ["C", "P"], "candidateSpellAcquisitions": ["time-stop", "timeless-form"],
        "noCampaignOrRuntimeClaim": True,
    })
    members["DIRECTOR_REQUEST_345.md"] = ("Director: review only the newly constructed conditional Time Stop witness delta under your authorization TF318-JOINT-INTERFACE-01. "
        "The 14 Return318 cases are preserved byte-exact and not replayed. Evaluate the new Wizard Action-mode natural completion, Cleric Universal Reaction-mode natural completion, and Wizard Arch Dispel failed-removal/successful-interruption branches. "
        "All characters and acquisitions are explicitly candidate review fixtures; no campaign/human play, runtime, RNG, canon change, or prior spell acquisition is claimed. "
        "Verify full actor/acquisition records, actual paid candidate casts, source route, Counterspell decisions, exact clocks, peer eligibility, costs, and inverse chains. "
        "If sufficient for a Time Stop-only ACCEPT, authorize application for Time Stop only and keep Timeless Form pending. Otherwise return the exact remaining TF192-B01 requirements and a one-identity HOLD. Preserve every unrelated hold, qualification, closure, and authority count.").encode("utf-8")

    # Rebuild exact allowlist after all payload members have been added.
    payload_rows = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}
                    for name, raw in sorted(members.items()) if name != "MEMBER_MANIFEST.json"]
    manifest = {"id": "TF318-345-WITNESS-MEMBER-MANIFEST", "schema": "TF318-CONDITIONAL-WITNESS-1",
                "memberCount": len(payload_rows) + 1, "payloadMemberCount": len(payload_rows), "members": payload_rows,
                "exactPayloadAllowlist": [row["path"] for row in payload_rows],
                "preservedCaseCount": 14, "newConditionalCaseCount": len(cases)}
    members["MEMBER_MANIFEST.json"] = pretty(manifest)

    out_cases = OUT / "cases"
    for case in cases:
        write_member(out_cases / (case["id"] + ".json"), pretty(case))
    for key, raw in members.items():
        if key.startswith("cases/"):
            continue
        write_member(OUT / "payload" / pathlib.PurePosixPath(key), raw)

    replay = [verify_case(case) for case in cases]
    all_pass = all(item["passed"] for item in replay)
    archive_path = OUT / "DD_Rank9_TimeStop_TF318_Witness345.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name, raw in sorted(members.items()):
            zf.writestr(name, raw)
    archive_raw = archive_path.read_bytes()
    delivery = {
        "id": "TIME-STOP-TF318-WITNESS345-DELIVERY", "reviewId": "Witness345",
        "scopeIds": ["time-stop"], "linkedPendingComparisonIds": ["timeless-form"],
        "acceptedIds": [], "appliedIds": [], "heldIds": [], "applicationAuthorized": False,
        "authority": {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0,
                      "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
        "authorizationId": "TF318-JOINT-INTERFACE-01", "authorizationStatus": "AUTHORIZED_FOR_CONDITIONAL_WITNESS_CONSTRUCTION_ONLY",
        "preservedTimeStopCaseCount": 14, "newConditionalCaseCount": len(cases),
        "newCaseEvents": sum(len(case["events"]) for case in cases),
        "newCaseForwardOperations": sum(case["counts"]["forwardOperations"] for case in cases),
        "newCaseInverseOperations": sum(case["counts"]["inverseOperations"] for case in cases),
        "newCasesReplayPassed": all_pass, "runtimeExecuted": False, "humanPlayExecuted": False,
        "campaignEventsClaimed": False, "canonicalFilesChanged": False,
        "archive": {"fileName": archive_path.name, "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)},
        "archiveMemberCount": len(members), "payloadMemberCount": len(members) - 1,
    }
    delivery_path = OUT / "DD_Rank9_TimeStop_TF318_Witness345_DELIVERY.json"
    delivery_path.write_bytes(pretty(delivery))
    audit = {
        "id": "TIME-STOP-TF318-WITNESS345-INDEPENDENT-AUDIT", "status": "PASS" if all_pass else "FAIL",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checks": [{"id": "new-case-replay-" + row["caseId"], "passed": row["passed"], "detail": row} for row in replay],
        "preservedCaseBytesRebound": len(preserved_rows) == 14,
        "allSourceBindingsRecorded": len(source_rows) == len(SOURCES),
        "allCasesClearlyConditional": all(case["initialState"]["fixtureMode"] == "AUTHORED_CONDITIONAL_REVIEW_FIXTURE_ONLY" for case in cases),
        "totalNewEvents": delivery["newCaseEvents"], "totalForwardOperations": delivery["newCaseForwardOperations"],
        "totalInverseOperations": delivery["newCaseInverseOperations"], "archive": delivery["archive"],
        "authorityUnchanged": delivery["authority"], "applicationPerformed": False,
    }
    replay_path = OUT / "TIME_STOP_TF318_WITNESS345_GENERATOR_REPLAY.json"
    replay_path.write_bytes(pretty(audit))
    PUBLISH.mkdir(parents=True)
    for path in (archive_path, delivery_path, replay_path):
        write_member(PUBLISH / path.name, path.read_bytes())
    (PUBLISH / "README.md").write_text(
        "# Time Stop / Timeless Form joint-interface witness 345\n\n"
        "This is a conditional authored review packet under TF318-JOINT-INTERFACE-01. "
        "The Director request and exact evidence are inside the ZIP. Both spell identities remain pending until a separate Director decision; no canon application, runtime execution, campaign event, or human-play validation is claimed.\n\n"
        "The archive contains 14 byte-exact historical cases, three new conditional branches, current source copies, source bindings, the contract, and the limited authorization. "
        "See the independent review report and delivery JSON beside the archive.\n",
        encoding="utf-8")
    print(json.dumps({"status": audit["status"], "cases": len(cases), "events": delivery["newCaseEvents"],
                      "forwardOperations": delivery["newCaseForwardOperations"], "inverseOperations": delivery["newCaseInverseOperations"],
                      "archive": delivery["archive"], "buildOutput": str(OUT), "deliveryOutput": str(PUBLISH)}, indent=2))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
