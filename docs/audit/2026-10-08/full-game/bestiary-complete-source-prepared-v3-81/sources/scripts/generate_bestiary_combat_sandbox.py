#!/usr/bin/env python3
"""
Generate draft combat columns in the canonical bestiary workbook.

Reads Bestiary.xlsx (+ final_bestiary.xlsx metadata), generates AC/HP/speed/attacks
from CR + size/type bands (DMG-style adapted for Aethel). Preserves authored
gate-guardian stats from live JSON. Writes combat columns into Bestiary.xlsx.

Provenance: all generated combat marked draft; source excel-sandbox.
Does NOT copy SRD creature attack names.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_XLSX = ROOT / "Bestiary.xlsx"
METADATA_XLSX = ROOT / "final_bestiary.xlsx"
JSON_PATH = ROOT / "src" / "bestiary_data_full.json"
BACKUP_DIR = ROOT / "backups"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from scrub_bestiary_ip import rename_value  # noqa: E402

COMBAT_COLUMNS = [
    "AC",
    "HP",
    "Speed",
    "Attack1 Name",
    "Attack1 Bonus",
    "Attack1 Damage",
    "Attack1 Type",
    "Attack2 Name",
    "Attack2 Bonus",
    "Attack2 Damage",
    "Attack2 Type",
    "Multiattack",
    "Save DC",
    "Traits",
    "Combat Provenance",
]

# DMG-style CR bands adapted for Aethel (draft). Values are baseline Medium creatures.
CR_BANDS: dict[str, dict[str, Any]] = {
    "0": {"ac": 10, "hp": 5, "bonus": 3, "dice": "1d4", "avg": 2, "mod": 0, "multi": 1, "save_dc": None},
    "1/8": {"ac": 11, "hp": 7, "bonus": 3, "dice": "1d4", "avg": 3, "mod": 1, "multi": 1, "save_dc": None},
    "1/4": {"ac": 11, "hp": 11, "bonus": 3, "dice": "1d6", "avg": 4, "mod": 1, "multi": 1, "save_dc": None},
    "1/2": {"ac": 12, "hp": 22, "bonus": 4, "dice": "1d6", "avg": 5, "mod": 2, "multi": 1, "save_dc": None},
    "1": {"ac": 13, "hp": 35, "bonus": 4, "dice": "1d8", "avg": 6, "mod": 2, "multi": 1, "save_dc": None},
    "2": {"ac": 13, "hp": 45, "bonus": 5, "dice": "1d10", "avg": 7, "mod": 2, "multi": 1, "save_dc": None},
    "3": {"ac": 14, "hp": 58, "bonus": 5, "dice": "2d6", "avg": 9, "mod": 2, "multi": 1, "save_dc": 11},
    "4": {"ac": 14, "hp": 75, "bonus": 6, "dice": "2d6", "avg": 10, "mod": 3, "multi": 1, "save_dc": 12},
    "5": {"ac": 15, "hp": 95, "bonus": 6, "dice": "2d8", "avg": 13, "mod": 4, "multi": 1, "save_dc": 13},
    "6": {"ac": 15, "hp": 112, "bonus": 6, "dice": "2d8", "avg": 13, "mod": 4, "multi": 2, "save_dc": 13},
    "7": {"ac": 15, "hp": 123, "bonus": 7, "dice": "2d8", "avg": 14, "mod": 5, "multi": 2, "save_dc": 14},
    "8": {"ac": 16, "hp": 142, "bonus": 7, "dice": "2d10", "avg": 16, "mod": 5, "multi": 2, "save_dc": 15},
    "9": {"ac": 16, "hp": 157, "bonus": 7, "dice": "2d10", "avg": 16, "mod": 5, "multi": 2, "save_dc": 15},
    "10": {"ac": 17, "hp": 172, "bonus": 8, "dice": "2d10", "avg": 17, "mod": 6, "multi": 2, "save_dc": 16},
    "11": {"ac": 17, "hp": 187, "bonus": 8, "dice": "2d10", "avg": 18, "mod": 6, "multi": 2, "save_dc": 16},
    "12": {"ac": 17, "hp": 202, "bonus": 8, "dice": "3d8", "avg": 19, "mod": 6, "multi": 2, "save_dc": 17},
    "13": {"ac": 18, "hp": 217, "bonus": 8, "dice": "3d8", "avg": 20, "mod": 6, "multi": 2, "save_dc": 17},
    "14": {"ac": 18, "hp": 232, "bonus": 9, "dice": "3d8", "avg": 21, "mod": 7, "multi": 2, "save_dc": 18},
    "15": {"ac": 18, "hp": 247, "bonus": 9, "dice": "3d10", "avg": 23, "mod": 7, "multi": 2, "save_dc": 18},
    "16": {"ac": 18, "hp": 262, "bonus": 9, "dice": "3d10", "avg": 24, "mod": 7, "multi": 3, "save_dc": 19},
    "17": {"ac": 19, "hp": 277, "bonus": 10, "dice": "3d10", "avg": 25, "mod": 7, "multi": 3, "save_dc": 19},
    "18": {"ac": 19, "hp": 292, "bonus": 10, "dice": "3d10", "avg": 26, "mod": 7, "multi": 3, "save_dc": 19},
    "19": {"ac": 19, "hp": 307, "bonus": 10, "dice": "3d12", "avg": 28, "mod": 8, "multi": 3, "save_dc": 20},
    "20": {"ac": 19, "hp": 322, "bonus": 11, "dice": "3d12", "avg": 29, "mod": 8, "multi": 3, "save_dc": 20},
    "21": {"ac": 20, "hp": 337, "bonus": 11, "dice": "3d12", "avg": 30, "mod": 8, "multi": 3, "save_dc": 21},
    "22": {"ac": 20, "hp": 352, "bonus": 11, "dice": "4d10", "avg": 31, "mod": 8, "multi": 3, "save_dc": 21},
    "23": {"ac": 20, "hp": 367, "bonus": 12, "dice": "4d10", "avg": 32, "mod": 8, "multi": 3, "save_dc": 22},
    "24": {"ac": 21, "hp": 382, "bonus": 12, "dice": "4d10", "avg": 33, "mod": 8, "multi": 3, "save_dc": 22},
    "25": {"ac": 21, "hp": 397, "bonus": 12, "dice": "4d12", "avg": 35, "mod": 9, "multi": 3, "save_dc": 23},
    "26": {"ac": 21, "hp": 412, "bonus": 13, "dice": "4d12", "avg": 36, "mod": 9, "multi": 3, "save_dc": 23},
    "27": {"ac": 22, "hp": 427, "bonus": 13, "dice": "4d12", "avg": 37, "mod": 9, "multi": 3, "save_dc": 24},
    "28": {"ac": 22, "hp": 442, "bonus": 13, "dice": "4d12", "avg": 38, "mod": 9, "multi": 3, "save_dc": 24},
    "29": {"ac": 22, "hp": 457, "bonus": 14, "dice": "5d10", "avg": 39, "mod": 9, "multi": 3, "save_dc": 25},
    "30": {"ac": 23, "hp": 472, "bonus": 14, "dice": "5d10", "avg": 40, "mod": 9, "multi": 3, "save_dc": 25},
}

SIZE_MODS: dict[str, dict[str, float | int]] = {
    "Tiny": {"ac": 1, "hp_mult": 0.25, "dmg_mult": 0.5, "multi_add": 0},
    "Small": {"ac": 0, "hp_mult": 0.5, "dmg_mult": 0.75, "multi_add": 0},
    "Medium": {"ac": 0, "hp_mult": 1.0, "dmg_mult": 1.0, "multi_add": 0},
    "Large": {"ac": -1, "hp_mult": 1.5, "dmg_mult": 1.25, "multi_add": 0},
    "Huge": {"ac": -2, "hp_mult": 2.0, "dmg_mult": 1.5, "multi_add": 1},
    "Gargantuan": {"ac": -2, "hp_mult": 2.5, "dmg_mult": 2.0, "multi_add": 1},
}

TYPE_ATTACKS: dict[str, list[tuple[str, str]]] = {
    "aberration": [("Mind Lash", "psychic"), ("Warped Tentacle", "psychic"), ("Void Rend", "psychic")],
    "beast": [("Rending Claw", "slashing"), ("Crushing Bite", "piercing"), ("Goring Horn", "piercing")],
    "celestial": [("Radiant Smite", "radiant"), ("Luminous Strike", "radiant"), ("Sanctified Blow", "radiant")],
    "construct": [("Iron Slam", "bludgeoning"), ("Stone Fist", "bludgeoning"), ("Hammer Blow", "bludgeoning")],
    "dragon": [("Scale Rend", "slashing"), ("Drake Claw", "slashing"), ("Wyrm Bite", "piercing")],
    "elemental": [("Primal Strike", "bludgeoning"), ("Elemental Slam", "thunder"), ("Core Burst", "fire")],
    "fey": [("Glamour Cut", "psychic"), ("Wild Thorn", "piercing"), ("Fey Whisper", "psychic")],
    "fiend": [("Hellfire Claw", "fire"), ("Abyssal Rend", "necrotic"), ("Infernal Strike", "fire")],
    "giant": [("Massive Club", "bludgeoning"), ("Boulder Smash", "bludgeoning"), ("Titan Fist", "bludgeoning")],
    "humanoid": [("Weapon Strike", "slashing"), ("Heavy Blow", "bludgeoning"), ("Precise Cut", "slashing")],
    "monstrosity": [("Monstrous Claw", "slashing"), ("Freak Bite", "piercing"), ("Aberrant Lash", "acid")],
    "ooze": [("Acid Pseudopod", "acid"), ("Corrosive Touch", "acid"), ("Engulfing Slam", "acid")],
    "plant": [("Thorn Lash", "piercing"), ("Root Strike", "bludgeoning"), ("Spore Touch", "poison")],
    "undead": [("Grave Touch", "necrotic"), ("Bone Rake", "slashing"), ("Death Chill", "cold")],
}

TYPE_ATTACKS_SECONDARY: dict[str, list[tuple[str, str]]] = {
    "aberration": [("Psychic Pulse", "psychic")],
    "beast": [("Tail Swipe", "bludgeoning")],
    "celestial": [("Holy Bolt", "radiant")],
    "construct": [("Grinding Gear", "bludgeoning")],
    "dragon": [("Tail Sweep", "bludgeoning")],
    "elemental": [("Surge Bolt", "lightning")],
    "fey": [("Mislead Strike", "psychic")],
    "fiend": [("Soul Burn", "fire")],
    "giant": [("Ground Stomp", "bludgeoning")],
    "humanoid": [("Off-hand Strike", "piercing")],
    "monstrosity": [("Tail Lash", "bludgeoning")],
    "ooze": [("Dissolve", "acid")],
    "plant": [("Entangle", "bludgeoning")],
    "undead": [("Life Drain", "necrotic")],
}

SPEED_BY_TYPE: dict[str, str] = {
    "aberration": "30 ft.",
    "beast": "40 ft.",
    "celestial": "30 ft., fly 60 ft.",
    "construct": "30 ft.",
    "dragon": "40 ft., fly 80 ft.",
    "elemental": "40 ft.",
    "fey": "30 ft., fly 30 ft.",
    "fiend": "30 ft., fly 60 ft.",
    "giant": "40 ft.",
    "humanoid": "30 ft.",
    "monstrosity": "40 ft.",
    "ooze": "20 ft., climb 20 ft.",
    "plant": "20 ft.",
    "undead": "30 ft.",
}

GATE_GUARDIAN_NAMES = {
    "The Bloom That Hungers",
    "Vaskor, the Stone Maw",
    "Ashthirst the Hollow",
    "Choralith, Voice Below",
    "Lumen of the Shattered Thread",
    "Threxus, the Iron Spiral",
    "Eirfax, the Dusk Crowned",
    "Xarog, the Pactbound Furnace",
    "Gor Vekk, Architect of Ends",
    "The Marquis of Silence",
}


def normalize_cr(raw: Any) -> str:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return "0"
    text = str(raw).strip()
    if not text or text.lower() == "nan":
        return "0"
    return text


def cr_to_float(cr: str) -> float:
    if "/" in cr:
        num, den = cr.split("/", 1)
        return float(num) / float(den)
    return float(cr)


def pick_from_pool(name: str, pool: list[tuple[str, str]]) -> tuple[str, str]:
    idx = int(hashlib.md5(name.encode()).hexdigest(), 16) % len(pool)
    return pool[idx]


def format_damage(dice: str, mod: int) -> str:
    if mod > 0:
        return f"{dice}+{mod}"
    if mod < 0:
        return f"{dice}{mod}"
    return dice


def scale_mod(base_mod: int, dmg_mult: float) -> tuple[str, int]:
    """Adjust modifier for size; keep dice string."""
    new_mod = max(0, round(base_mod * dmg_mult))
    return new_mod


def generate_stats(name: str, size: str, ctype: str, cr: str) -> dict[str, Any]:
    band = CR_BANDS.get(cr, CR_BANDS["0"])
    size_key = size if size in SIZE_MODS else "Medium"
    sm = SIZE_MODS[size_key]

    ac = max(8, band["ac"] + int(sm["ac"]))
    hp = max(1, round(band["hp"] * float(sm["hp_mult"])))
    bonus = band["bonus"]
    mod = scale_mod(band["mod"], float(sm["dmg_mult"]))
    multi = max(1, band["multi"] + int(sm["multi_add"]))
    if cr_to_float(cr) >= 11:
        multi = max(multi, 2)

    type_key = (ctype or "monstrosity").lower().split("(")[0].strip()
    if type_key not in TYPE_ATTACKS:
        type_key = "monstrosity"

    atk1_name, atk1_type = pick_from_pool(name, TYPE_ATTACKS[type_key])
    atk1_damage = format_damage(band["dice"], mod)

    atk2_name = ""
    atk2_type = ""
    atk2_bonus: int | str = ""
    atk2_damage = ""
    atk2_type_out = ""
    if multi >= 2 or cr_to_float(cr) >= 5:
        sec_pool = TYPE_ATTACKS_SECONDARY.get(type_key, TYPE_ATTACKS[type_key])
        atk2_name, atk2_type = pick_from_pool(name + "_2", sec_pool)
        atk2_bonus = bonus
        atk2_mod = max(0, mod - 1)
        atk2_damage = format_damage(band["dice"], atk2_mod)
        atk2_type_out = atk2_type

    speed = SPEED_BY_TYPE.get(type_key, "30 ft.")
    if size_key in ("Huge", "Gargantuan") and "fly" not in speed:
        speed = speed.replace("40 ft.", "30 ft.")

    save_dc = band.get("save_dc")
    traits = f"Draft stats from CR {cr} {size_key} {type_key} band (excel-sandbox generator)."

    return {
        "AC": ac,
        "HP": hp,
        "Speed": speed,
        "Attack1 Name": atk1_name,
        "Attack1 Bonus": bonus,
        "Attack1 Damage": atk1_damage,
        "Attack1 Type": atk1_type,
        "Attack2 Name": atk2_name if atk2_name else None,
        "Attack2 Bonus": atk2_bonus if atk2_bonus else None,
        "Attack2 Damage": atk2_damage if atk2_damage else None,
        "Attack2 Type": atk2_type_out if atk2_type_out else None,
        "Multiattack": multi if multi > 1 else None,
        "Save DC": save_dc,
        "Traits": traits,
        "Combat Provenance": "draft: excel-sandbox generator (CR band)",
    }


def load_authored_guardians() -> dict[str, dict[str, Any]]:
    if not JSON_PATH.exists():
        return {}
    with JSON_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    out: dict[str, dict[str, Any]] = {}
    for entry in data:
        if entry["name"] not in GATE_GUARDIAN_NAMES:
            continue
        combat = entry.get("combat") or {}
        attacks = combat.get("attacks") or []
        default_id = combat.get("defaultActionId")
        primary = next((a for a in attacks if a.get("id") == default_id), attacks[0] if attacks else None)
        secondary = next((a for a in attacks if a.get("id") != default_id and a.get("kind") == "attack"), None)

        row: dict[str, Any] = {
            "AC": entry.get("armorClass"),
            "HP": entry.get("hitPoints"),
            "Speed": entry.get("speed", "30 ft."),
            "Save DC": combat.get("saveDc"),
            "Traits": entry.get("description", "")[:200],
            "Combat Provenance": "draft: companion-authored (preserved)",
        }
        if primary:
            dmg = (primary.get("damage") or [{}])[0]
            row["Attack1 Name"] = primary.get("name")
            row["Attack1 Bonus"] = primary.get("attackBonus")
            row["Attack1 Damage"] = dmg.get("dice")
            row["Attack1 Type"] = dmg.get("type")
            count = primary.get("count", 1)
            row["Multiattack"] = count if count > 1 else None
        if secondary:
            dmg2 = (secondary.get("damage") or [{}])[0]
            row["Attack2 Name"] = secondary.get("name")
            row["Attack2 Bonus"] = secondary.get("attackBonus")
            row["Attack2 Damage"] = dmg2.get("dice")
            row["Attack2 Type"] = dmg2.get("type")
        out[entry["name"]] = row
    return out


def backup_workbooks() -> list[str]:
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    copied = []
    for path in (PRIMARY_XLSX, METADATA_XLSX):
        if path.exists():
            dest = BACKUP_DIR / f"{path.stem}_{stamp}{path.suffix}"
            shutil.copy2(path, dest)
            copied.append(str(dest))
    return copied


def main() -> None:
    backups = backup_workbooks()
    print(f"Backups: {backups}")

    primary_df = pd.read_excel(PRIMARY_XLSX, sheet_name="Monsters")
    meta_df = pd.read_excel(METADATA_XLSX, sheet_name="Monsters") if METADATA_XLSX.exists() else None
    meta_by_name: dict[str, pd.Series] = {}
    if meta_df is not None:
        for _, row in meta_df.iterrows():
            raw = row.get("Name")
            if pd.notna(raw):
                meta_by_name[rename_value(str(raw))] = row

    guardians = load_authored_guardians()
    generated = 0
    preserved = 0
    rows_out: list[dict[str, Any]] = []

    for _, row in primary_df.iterrows():
        name_raw = row.get("Name")
        if pd.isna(name_raw):
            continue
        name = rename_value(str(name_raw).strip())
        meta = meta_by_name.get(name)

        size = str(row.get("Size") or (meta.get("Size") if meta is not None else None) or "Medium")
        ctype = str(row.get("Type") or (meta.get("Type") if meta is not None else None) or "Monstrosity")
        cr = normalize_cr(row.get("Challenge") if pd.notna(row.get("Challenge")) else (meta.get("Challenge") if meta is not None else "0"))

        out_row = row.to_dict()
        if name in guardians:
            combat = guardians[name]
            preserved += 1
        else:
            combat = generate_stats(name, size, ctype, cr)
            generated += 1

        for col in COMBAT_COLUMNS:
            val = combat.get(col)
            out_row[col] = val

        rows_out.append(out_row)

    result_df = pd.DataFrame(rows_out)

    wb = load_workbook(PRIMARY_XLSX)
    ws = wb["Monsters"]

    # Append new column headers if missing
    existing_headers = [cell.value for cell in ws[1]]
    header_to_col = {str(h).strip(): i + 1 for i, h in enumerate(existing_headers) if h}
    start_col = len(existing_headers) + 1
    for col_name in COMBAT_COLUMNS:
        if col_name not in header_to_col:
            ws.cell(row=1, column=start_col, value=col_name)
            header_to_col[col_name] = start_col
            start_col += 1

    # Build name→row index
    name_col = header_to_col.get("Name", 1)
    name_to_row: dict[str, int] = {}
    for r in range(2, ws.max_row + 1):
        val = ws.cell(row=r, column=name_col).value
        if val:
            name_to_row[rename_value(str(val).strip())] = r

    for _, data_row in result_df.iterrows():
        name = rename_value(str(data_row["Name"]).strip())
        r = name_to_row.get(name)
        if not r:
            continue
        combat_vals = {col: data_row.get(col) for col in COMBAT_COLUMNS}
        for col_name in COMBAT_COLUMNS:
            val = combat_vals.get(col_name)
            if val is not None and (not isinstance(val, float) or not pd.isna(val)):
                ws.cell(row=r, column=header_to_col[col_name], value=val)

    wb.save(PRIMARY_XLSX)

    summary = {
        "workbook": str(PRIMARY_XLSX.name),
        "canonical_note": "Combat columns written to Bestiary.xlsx — edit there, then re-ingest",
        "rows": len(rows_out),
        "generated": generated,
        "preserved_guardians": preserved,
        "backups": backups,
        "combat_columns": COMBAT_COLUMNS,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
