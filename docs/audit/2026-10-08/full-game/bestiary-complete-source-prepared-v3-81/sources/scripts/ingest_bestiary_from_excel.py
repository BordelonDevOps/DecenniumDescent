#!/usr/bin/env python3
"""
Re-ingest bestiary from owner workbooks → src/bestiary_data_full.json.

Primary source: Bestiary.xlsx (Monsters sheet) — identity, loot, and combat columns.
Metadata supplement: final_bestiary.xlsx — Size, Type, CR, XP, zones, tier drops when
primary cells are blank.

Combat/stat columns are mapped when present (AC, HP, Speed, abilities, attacks, etc.).
Do not fabricate stats when columns are absent.

Authored Gate Guardian records merge intelligently: Excel wins for stats and combat when
present; companion `combat` payloads are used only when Excel attack cells are empty.
Ul'nath hidden.

CLI: python scripts/ingest_bestiary_from_excel.py [--xlsx PATH]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from ast import literal_eval
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XLSX = ROOT / "Bestiary.xlsx"
METADATA_XLSX = ROOT / "final_bestiary.xlsx"
JSON_PATH = ROOT / "src" / "bestiary_data_full.json"
HIDDEN_NAMES = {"Ul'nath, the Hollow Dream", "Ul\u2019nath, the Hollow Dream"}
INGEST_SOURCE = "Bestiary.xlsx:Monsters"
SANDBOX_SOURCE = "excel-sandbox"

sys.path.insert(0, str(ROOT / "scripts"))
from scrub_bestiary_ip import rename_value  # noqa: E402

# Canonical name aliases (sheet typos / short forms → lore-pass names)
NAME_ALIASES = {
    "Xarog the Pactbound Furnace": "Xarog, the Pactbound Furnace",
    "Gor Vekk": "Gor Vekk, Architect of Ends",
    "Choralith": "Choralith, Voice Below",
}

REPEATED_NAME_PREFIXES = ("Fracture-Kin", "Order-Drone", "Hush-Broker")


def collapse_repeated_prefix(name: str) -> str:
    """Collapse scrub double-application: 'Fracture-Kin Fracture-Kin X' → 'Fracture-Kin X'."""
    out = name.strip()
    for prefix in REPEATED_NAME_PREFIXES:
        token = prefix + " "
        while out.startswith(token + prefix):
            out = out[len(token) :]
    return out


def canonicalize_name(raw: str | None) -> str | None:
    if not raw:
        return raw
    name = rename_value(str(raw).strip())
    name = collapse_repeated_prefix(name)
    return NAME_ALIASES.get(name, name)


STAT_COLUMN_MAP: dict[str, str | tuple[str, str]] = {
    "armor class": "armorClass",
    "ac": "armorClass",
    "hit points": "hitPoints",
    "hp": "hitPoints",
    "speed": "speed",
    "str": ("abilities", "strength"),
    "strength": ("abilities", "strength"),
    "dex": ("abilities", "dexterity"),
    "dexterity": ("abilities", "dexterity"),
    "con": ("abilities", "constitution"),
    "constitution": ("abilities", "constitution"),
    "int": ("abilities", "intelligence"),
    "intelligence": ("abilities", "intelligence"),
    "wis": ("abilities", "wisdom"),
    "wisdom": ("abilities", "wisdom"),
    "cha": ("abilities", "charisma"),
    "charisma": ("abilities", "charisma"),
    "skills": "skills",
    "senses": "senses",
    "languages": "languages",
    "description": "description",
    "save dc": "saveDc",
    "attacks": "attacksRaw",
    "multiattack": "multiattackRaw",
    "damage": "damageRaw",
    "resistances": "resistancesRaw",
    "immunities": "immunitiesRaw",
    "condition immunities": "conditionImmunitiesRaw",
}


def clean_cell(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    return text


def clean_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def clean_rate(value: Any) -> str | None:
    num = clean_int(value)
    if num is not None:
        return str(value) if isinstance(value, float) and not value.is_integer() else str(num)
    return clean_cell(value)


def normalize_header(header: Any) -> str:
    return re.sub(r"\s+", " ", str(header).strip().lower())


def build_column_lookup(columns: list[Any]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for col in columns:
        lookup[normalize_header(col)] = col
    return lookup


def get_row_value(row: pd.Series, lookup: dict[str, str], *header_names: str) -> Any:
    for header in header_names:
        col = lookup.get(normalize_header(header))
        if col is not None and col in row.index:
            val = row.get(col)
            if clean_cell(val) is not None:
                return val
    return None


def build_loot(row: pd.Series, lookup: dict[str, str]) -> dict[str, dict[str, str | None]]:
    loot: dict[str, dict[str, str | None]] = {}
    for tier in range(1, 7):
        drop = clean_cell(get_row_value(row, lookup, f"Tier {tier} Drop"))
        rate = clean_rate(get_row_value(row, lookup, f"Tier {tier} Rate"))
        value = clean_rate(get_row_value(row, lookup, f"Tier {tier} Value"))
        if drop or (rate and rate not in ("0", "0.0")) or (value and value not in ("0", "0.0")):
            loot[f"tier{tier}"] = {"drop": drop, "rate": rate, "value": value}
    return loot


def parse_loot_table(raw: Any) -> list[Any] | None:
    if isinstance(raw, list):
        return raw
    text = clean_cell(raw)
    if not text or text == "[]":
        return None
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, list) else None
    except (TypeError, json.JSONDecodeError):
        pass
    try:
        parsed = literal_eval(text)
        return parsed if isinstance(parsed, list) else None
    except (SyntaxError, ValueError):
        return None


def build_description(name: str, size: str | None, ctype: str | None, zone: str | None) -> str:
    if size and ctype:
        lead = f"A {size.lower()} {ctype.lower()}"
    elif ctype:
        lead = f"A {ctype.lower()}"
    else:
        lead = "A creature"
    if zone:
        return f"{lead} found in {zone}."
    return f"{lead} from the Decennium Descent bestiary."


def parse_list_field(raw: Any) -> list[str] | None:
    text = clean_cell(raw)
    if not text:
        return None
    if text.startswith("["):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except json.JSONDecodeError:
            pass
    parts = [p.strip() for p in re.split(r"[,;]", text) if p.strip()]
    return parts or None


def dice_average(dice_expr: str) -> float:
    """Compute average damage from expressions like 2d8+4."""
    text = dice_expr.replace(" ", "")
    mod = 0
    if "+" in text:
        parts = text.split("+", 1)
        text, mod = parts[0], int(parts[1])
    elif text.count("-") > 0 and "d" not in text.split("-", 1)[1]:
        parts = text.split("-", 1)
        text, mod = parts[0], -int(parts[1])
    match = re.match(r"(\d+)d(\d+)", text)
    if not match:
        return float(mod)
    count, sides = int(match.group(1)), int(match.group(2))
    return count * (sides + 1) / 2 + mod


def slugify_attack_id(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "primary"


def parse_recharge_roll(raw: Any) -> dict[str, int] | None:
    text = clean_cell(raw)
    if not text:
        return None
    if "-" in text:
        parts = text.split("-", 1)
        try:
            minimum_roll = int(parts[0].strip())
            die_sides = int(parts[1].strip())
            if die_sides < 1 or minimum_roll < 1 or minimum_roll > die_sides:
                return None
            return {"minimumRoll": minimum_roll, "dieSides": die_sides}
        except ValueError:
            return None
    try:
        minimum_roll = int(text)
        return {"minimumRoll": minimum_roll, "dieSides": 6}
    except ValueError:
        return None


def build_recharge_entry(row: pd.Series, lookup: dict[str, str]) -> dict[str, Any] | None:
    name = clean_cell(get_row_value(row, lookup, "Recharge Name"))
    damage_raw = clean_cell(get_row_value(row, lookup, "Recharge Damage"))
    if not name and not damage_raw:
        return None

    kind = (clean_cell(get_row_value(row, lookup, "Recharge Kind")) or "save").lower()
    bonus = clean_int(get_row_value(row, lookup, "Recharge Bonus"))
    damage_type = clean_cell(get_row_value(row, lookup, "Recharge Type"))
    save_dc = clean_int(get_row_value(row, lookup, "Recharge Save DC", "Recharge Save Dc"))
    save_ability = (
        clean_cell(get_row_value(row, lookup, "Recharge Save Ability")) or "constitution"
    ).lower()
    recharge = parse_recharge_roll(get_row_value(row, lookup, "Recharge Roll", "Recharge"))

    if not recharge:
        return None

    attack: dict[str, Any] = {
        "id": slugify_attack_id(name or "recharge"),
        "name": name or "Recharge",
        "kind": "save" if kind == "save" else "attack",
        "actionCost": "action",
        "usage": "recharge",
        "recharge": recharge,
        "targets": {"scope": "creatures-in-area"},
        "damage": [],
    }

    if attack["kind"] == "attack":
        attack["targets"] = {"count": 1, "scope": "creature"}
        if bonus is not None:
            attack["attackBonus"] = bonus
    else:
        if save_dc is None:
            save_dc = clean_int(get_row_value(row, lookup, "Save DC", "Save Dc"))
        if save_dc is None:
            return None
        attack["save"] = {
            "ability": save_ability,
            "dc": save_dc,
            "onSuccess": "half",
        }
        attack["range"] = {"radiusFt": 20}

    if damage_raw:
        dice = damage_raw.replace(" ", "")
        attack["damage"].append(
            {
                "dice": dice,
                "average": round(dice_average(dice), 1),
                "type": (damage_type or "bludgeoning").lower(),
            }
        )

    if not attack["damage"]:
        return None
    if attack["kind"] == "attack" and attack.get("attackBonus") is None:
        return None
    return attack


def build_attack_entry(
    name: str,
    bonus: int | None,
    damage_raw: str | None,
    damage_type: str | None,
    count: int = 1,
    is_default: bool = False,
) -> dict[str, Any] | None:
    if not name and not damage_raw:
        return None
    attack: dict[str, Any] = {
        "id": slugify_attack_id(name or "attack"),
        "name": name or "Attack",
        "kind": "attack",
        "actionCost": "action",
        "usage": "atWill",
        "count": count,
        "targets": {"count": 1, "scope": "creature"},
        "damage": [],
    }
    if bonus is not None:
        attack["attackBonus"] = bonus
    if damage_raw:
        dice = damage_raw.replace(" ", "")
        attack["damage"].append(
            {
                "dice": dice,
                "average": round(dice_average(dice), 1),
                "type": (damage_type or "bludgeoning").lower(),
            }
        )
    if not attack.get("damage") and bonus is None:
        return None
    return attack


def build_combat_from_excel(row: pd.Series, lookup: dict[str, str]) -> dict[str, Any] | None:
    save_dc = clean_int(get_row_value(row, lookup, "Save DC", "Save Dc"))
    multi_count = clean_int(get_row_value(row, lookup, "Multiattack"))
    provenance = clean_cell(get_row_value(row, lookup, "Combat Provenance"))

    # Structured Attack1/Attack2 columns (combat sandbox)
    atk1_name = clean_cell(get_row_value(row, lookup, "Attack1 Name"))
    atk1_bonus = clean_int(get_row_value(row, lookup, "Attack1 Bonus"))
    atk1_damage = clean_cell(get_row_value(row, lookup, "Attack1 Damage"))
    atk1_type = clean_cell(get_row_value(row, lookup, "Attack1 Type"))
    atk2_name = clean_cell(get_row_value(row, lookup, "Attack2 Name"))
    atk2_bonus = clean_int(get_row_value(row, lookup, "Attack2 Bonus"))
    atk2_damage = clean_cell(get_row_value(row, lookup, "Attack2 Damage"))
    atk2_type = clean_cell(get_row_value(row, lookup, "Attack2 Type"))

    attacks: list[dict[str, Any]] = []

    if atk1_name or atk1_damage:
        primary_count = multi_count if multi_count and multi_count > 1 else 1
        primary = build_attack_entry(atk1_name, atk1_bonus, atk1_damage, atk1_type, primary_count)
        if primary:
            attacks.append(primary)
        if atk2_name or atk2_damage:
            secondary = build_attack_entry(atk2_name, atk2_bonus, atk2_damage, atk2_type, 1)
            if secondary:
                secondary["id"] = slugify_attack_id(secondary["name"])
                attacks.append(secondary)

    if not attacks:
        # Legacy single-column format
        attacks_raw = clean_cell(get_row_value(row, lookup, "Attacks", "Attack"))
        damage_raw = clean_cell(get_row_value(row, lookup, "Damage"))
        multi_raw = clean_cell(get_row_value(row, lookup, "Multiattack"))
        if not attacks_raw and not damage_raw and not multi_raw:
            return None
        attack_bonus = clean_int(get_row_value(row, lookup, "Attack Bonus", "To Hit"))
        if attacks_raw or damage_raw:
            attack: dict[str, Any] = {
                "id": "primary",
                "name": multi_raw or attacks_raw or "Attack",
                "kind": "attack",
                "actionCost": "action",
                "usage": "atWill",
                "count": 1,
                "targets": {"count": 1, "scope": "creature"},
                "damage": [],
            }
            if attack_bonus is not None:
                attack["attackBonus"] = attack_bonus
            if damage_raw:
                dice_match = re.search(r"(\d+d\d+(?:\s*\+\s*\d+)?)", damage_raw, re.I)
                dice = dice_match.group(1).replace(" ", "") if dice_match else damage_raw
                attack["damage"].append(
                    {
                        "dice": dice,
                        "average": round(dice_average(dice), 1),
                        "type": "bludgeoning",
                    }
                )
            if attack.get("damage") or attack.get("attackBonus") is not None:
                attacks.append(attack)

    recharge = build_recharge_entry(row, lookup)
    if recharge:
        attacks.append(recharge)

    if not attacks:
        return None

    defenses = {
        "resistances": parse_list_field(get_row_value(row, lookup, "Resistances")) or [],
        "immunities": parse_list_field(get_row_value(row, lookup, "Immunities")) or [],
        "conditionImmunities": parse_list_field(
            get_row_value(row, lookup, "Condition Immunities")
        )
        or [],
    }

    prov_l = (provenance or "").lower()
    source = SANDBOX_SOURCE if "excel-sandbox" in prov_l else INGEST_SOURCE
    if "companion-authored" in prov_l:
        source = "companion-authored draft"
    if "gate-guardian-trusted" in prov_l:
        source = "gate-guardian-trusted"
    elif "t6-10-trusted" in prov_l:
        source = "t6-10-trusted"
    elif "t1-5-trusted" in prov_l:
        source = "t1-5-trusted"
    elif "band-trusted" in prov_l:
        source = "band-trusted"
    # Trusted provenance clears draft so Session / MonstersLibrary can ship trusted combat.
    draft = "trusted" not in prov_l

    combat: dict[str, Any] = {
        "schemaVersion": 1,
        "draft": draft,
        "source": source,
        "defaultActionId": attacks[0]["id"],
        "defenses": defenses,
        "attacks": attacks,
    }
    if save_dc is not None:
        combat["saveDc"] = save_dc
    return combat


def extract_stats(row: pd.Series, lookup: dict[str, str]) -> dict[str, Any]:
    stats: dict[str, Any] = {}
    abilities: dict[str, int] = {}

    for norm, col_name in lookup.items():
        target = STAT_COLUMN_MAP.get(norm)
        if not target:
            continue
        val = row.get(col_name)
        if clean_cell(val) is None and clean_int(val) is None:
            continue
        if isinstance(target, tuple):
            num = clean_int(val)
            if num is not None:
                abilities[target[1]] = num
        elif target in ("armorClass", "hitPoints", "saveDc"):
            num = clean_int(val)
            if num is not None:
                stats[target] = num
        elif target.endswith("Raw"):
            continue
        else:
            text = clean_cell(val)
            if text:
                stats[target] = text

    if abilities:
        stats["abilities"] = abilities
    return stats


def row_to_creature(
    primary_row: pd.Series,
    primary_lookup: dict[str, str],
    supplement_row: pd.Series | None,
    supplement_lookup: dict[str, str],
) -> dict[str, Any] | None:
    name_raw = clean_cell(get_row_value(primary_row, primary_lookup, "Name"))
    if not name_raw and supplement_row is not None:
        name_raw = clean_cell(get_row_value(supplement_row, supplement_lookup, "Name"))
    if not name_raw:
        return None

    name = canonicalize_name(name_raw) or rename_value(name_raw)
    if name in HIDDEN_NAMES or "Hollow Dream" in name:
        return None

    def pick(*headers: str, as_int: bool = False) -> Any:
        val = get_row_value(primary_row, primary_lookup, *headers)
        if clean_cell(val) is None and clean_int(val) is None and supplement_row is not None:
            val = get_row_value(supplement_row, supplement_lookup, *headers)
        if as_int:
            return clean_int(val)
        return clean_cell(val)

    size = pick("Size") or "Medium"
    ctype = pick("Type") or "Unknown"
    tags = pick("Tags")
    alignment = pick("Alignment") or ""
    cr = pick("Challenge", "Challenge Rating") or "0"
    xp = pick("XP", as_int=True) or 0
    zone = pick("Zone Found") or ""

    loot = build_loot(primary_row, primary_lookup)
    if not loot and supplement_row is not None:
        loot = build_loot(supplement_row, supplement_lookup)

    creature: dict[str, Any] = {
        "name": name,
        "type": ctype,
        "size": size,
        "challengeRating": cr,
        "xp": xp,
        "alignment": alignment,
        "zoneFound": zone,
        "description": pick("Description") or build_description(name, size, ctype, zone),
        "loot": loot,
        "ingestSource": INGEST_SOURCE,
    }
    if tags:
        creature["tags"] = tags

    loot_table = parse_loot_table(get_row_value(primary_row, primary_lookup, "Loot Table"))
    if not loot_table and supplement_row is not None:
        loot_table = parse_loot_table(
            get_row_value(supplement_row, supplement_lookup, "Loot Table")
        )
    if loot_table:
        creature["lootTable"] = loot_table

    stats = extract_stats(primary_row, primary_lookup)
    if supplement_row is not None:
        for key, val in extract_stats(supplement_row, supplement_lookup).items():
            if key not in stats or stats[key] in (None, "", {}):
                stats[key] = val
            elif key == "abilities" and isinstance(val, dict):
                merged = dict(stats.get("abilities", {}))
                for ab, score in val.items():
                    if ab not in merged:
                        merged[ab] = score
                stats["abilities"] = merged

    creature.update({k: v for k, v in stats.items() if v is not None and v != ""})

    excel_combat = build_combat_from_excel(primary_row, primary_lookup)
    if not excel_combat and supplement_row is not None:
        excel_combat = build_combat_from_excel(supplement_row, supplement_lookup)
    if excel_combat:
        creature["combat"] = excel_combat

    return creature


def is_gate_guardian(entry: dict[str, Any]) -> bool:
    tags = entry.get("tags", "")
    tag_text = tags if isinstance(tags, str) else " ".join(tags)
    return "gate guardian" in tag_text.lower()


def merge_with_override(excel_creature: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(excel_creature)
    guardian = is_gate_guardian(override)

    scalar_fields = (
        "armorClass",
        "hitPoints",
        "speed",
        "skills",
        "senses",
        "languages",
        "challengeRating",
        "xp",
        "type",
        "size",
        "alignment",
        "zoneFound",
    )

    for field in scalar_fields:
        excel_val = excel_creature.get(field)
        override_val = override.get(field)
        if excel_val is not None and excel_val != "" and excel_val != 0:
            merged[field] = excel_val
        elif override_val is not None and override_val != "":
            merged[field] = override_val

    excel_abilities = excel_creature.get("abilities") or {}
    override_abilities = override.get("abilities") or {}
    if excel_abilities or override_abilities:
        abilities = dict(override_abilities)
        for ab, score in excel_abilities.items():
            if score is not None:
                abilities[ab] = score
        merged["abilities"] = abilities

    excel_combat = excel_creature.get("combat")
    override_combat = override.get("combat")
    excel_has_attacks = bool(excel_combat and excel_combat.get("attacks"))
    override_has_attacks = bool(override_combat and override_combat.get("attacks"))

    if excel_has_attacks:
        merged["combat"] = excel_combat
    elif override_has_attacks:
        merged["combat"] = override_combat

    if guardian and override.get("description"):
        # Prefer lore-pass Excel description when present
        if not excel_creature.get("description"):
            merged["description"] = override["description"]
    if guardian and override.get("tags"):
        if not excel_creature.get("tags"):
            merged["tags"] = override["tags"]

    # Excel CR/XP win when present (lore quality pass stamped seal ladder).
    # Override fills only blanks — do not reintroduce stale sandbox CR/XP.
    if guardian:
        for field in ("challengeRating", "xp"):
            excel_val = excel_creature.get(field)
            override_val = override.get(field)
            if excel_val in (None, "", "0", 0) and override_val not in (None, "", "0", 0):
                merged[field] = override_val

    if excel_creature.get("lootTable") and not merged.get("lootTable"):
        merged["lootTable"] = excel_creature["lootTable"]

    merged["ingestSource"] = INGEST_SOURCE
    if override_has_attacks and not excel_has_attacks:
        merged["combatAuthored"] = True

    return merged


def load_authored_overrides() -> dict[str, dict[str, Any]]:
    if not JSON_PATH.exists():
        return {}
    with JSON_PATH.open(encoding="utf-8") as f:
        existing = json.load(f)
    overrides: dict[str, dict[str, Any]] = {}
    for entry in existing:
        raw_name = entry.get("name")
        canon = canonicalize_name(raw_name)
        if not canon:
            continue
        keep = False
        if entry.get("combat"):
            keep = True
        elif is_gate_guardian(entry) and entry.get("hitPoints", 0) > 1:
            keep = True
        if not keep:
            continue
        # Prefer the entry already keyed under the canonical name; otherwise
        # store under canon so IP renames / Xarog alias merge into Excel rows.
        stored = dict(entry)
        stored["name"] = canon
        if canon not in overrides:
            overrides[canon] = stored
        else:
            # If duplicate keys (Flumph + Lumen Drifter both map here), keep
            # richer combat / guardian payload.
            prev = overrides[canon]
            if not prev.get("combat") and stored.get("combat"):
                overrides[canon] = stored
            elif is_gate_guardian(stored) and not is_gate_guardian(prev):
                overrides[canon] = stored
    return overrides


def load_metadata_by_name() -> tuple[pd.DataFrame, dict[str, str]]:
    if not METADATA_XLSX.exists():
        return pd.DataFrame(), {}
    df = pd.read_excel(METADATA_XLSX, sheet_name="Monsters")
    return df, build_column_lookup(list(df.columns))


def load_primary(xlsx_path: Path | None = None) -> tuple[pd.DataFrame, dict[str, str], str]:
    path = xlsx_path or DEFAULT_XLSX
    if not path.exists():
        if METADATA_XLSX.exists():
            path = METADATA_XLSX
        else:
            raise FileNotFoundError(f"No bestiary workbook found at {xlsx_path or DEFAULT_XLSX}")
    df = pd.read_excel(path, sheet_name="Monsters")
    return df, build_column_lookup(list(df.columns)), str(path.name)


def ingest(xlsx_path: Path | None = None) -> dict[str, Any]:
    primary_df, primary_lookup, primary_label = load_primary(xlsx_path)
    meta_df, meta_lookup = load_metadata_by_name()
    overrides = load_authored_overrides()

    meta_by_scrubbed: dict[str, pd.Series] = {}
    if not meta_df.empty:
        for _, row in meta_df.iterrows():
            raw = clean_cell(row.get("Name"))
            if raw:
                meta_by_scrubbed[canonicalize_name(raw) or rename_value(raw)] = row

    creatures: list[dict[str, Any]] = []
    skipped_hidden = 0
    merged_overrides = 0
    stat_columns_found = {col for col in primary_lookup if col in STAT_COLUMN_MAP}

    for _, primary_row in primary_df.iterrows():
        name_raw = clean_cell(get_row_value(primary_row, primary_lookup, "Name"))
        if not name_raw:
            continue
        name = canonicalize_name(name_raw) or name_raw
        if name in HIDDEN_NAMES or "Hollow Dream" in name:
            skipped_hidden += 1
            continue

        supplement_row = meta_by_scrubbed.get(name)
        creature = row_to_creature(primary_row, primary_lookup, supplement_row, meta_lookup)
        if not creature:
            continue
        creature["name"] = name

        if name in overrides:
            creature = merge_with_override(creature, overrides[name])
            merged_overrides += 1

        creatures.append(creature)

    excel_names = {c["name"] for c in creatures}
    orphan_skipped = 0
    for name in sorted(overrides.keys()):
        if name in excel_names:
            continue
        # Drop JSON orphans superseded by Excel rename / prefix-collapse.
        collapsed = collapse_repeated_prefix(name)
        if collapsed in excel_names or (canonicalize_name(name) or "") in excel_names:
            orphan_skipped += 1
            continue
        extra = dict(overrides[name])
        extra["name"] = name
        extra["ingestSource"] = INGEST_SOURCE
        creatures.append(extra)

    creatures.sort(key=lambda c: c["name"].lower())

    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(creatures, f, indent=2, ensure_ascii=False)

    return {
        "primary_xlsx": primary_label,
        "metadata_supplement": str(METADATA_XLSX.name),
        "excel_rows": len(primary_df),
        "json_rows": len(creatures),
        "skipped_hidden": skipped_hidden,
        "merged_authored_overrides": merged_overrides,
        "orphan_overrides_skipped": orphan_skipped,
        "stat_columns_in_primary": sorted(stat_columns_found),
        "with_armor_class": sum(1 for c in creatures if c.get("armorClass") is not None),
        "with_hit_points": sum(1 for c in creatures if c.get("hitPoints") is not None),
        "with_loot_table": sum(1 for c in creatures if c.get("lootTable")),
        "with_combat_attacks": sum(
            1 for c in creatures if c.get("combat") and c["combat"].get("attacks")
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest bestiary Excel → JSON")
    parser.add_argument(
        "--xlsx",
        type=Path,
        default=None,
        help=f"Override primary workbook (default: {DEFAULT_XLSX.name})",
    )
    args = parser.parse_args()
    print(json.dumps(ingest(args.xlsx), indent=2))
