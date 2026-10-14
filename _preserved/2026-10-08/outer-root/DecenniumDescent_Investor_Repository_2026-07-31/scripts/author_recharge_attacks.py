#!/usr/bin/env python3
"""
Author draft recharge/trait rows into Bestiary.xlsx (Excel-first).

Adds optional recharge columns when missing and fills:
- All 10 gate guardians
- ~15 diverse CR-band creatures (Aethel names; no FR)

Does not overwrite existing Recharge Name cells unless --force.
Backs up Bestiary.xlsx to backups/ before writing.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_XLSX = ROOT / "Bestiary.xlsx"
BACKUP_DIR = ROOT / "backups"

RECHARGE_COLUMNS = [
    "Recharge Name",
    "Recharge Kind",
    "Recharge Bonus",
    "Recharge Damage",
    "Recharge Type",
    "Recharge Save DC",
    "Recharge Save Ability",
    "Recharge Roll",
]

# Gate guardians — companion-themed draft recharges (save unless noted).
GUARDIAN_RECHARGES: dict[str, dict[str, str | int]] = {
    "The Bloom That Hungers": {
        "Recharge Name": "Spore Burst",
        "Recharge Kind": "save",
        "Recharge Damage": "1d8",
        "Recharge Type": "poison",
        "Recharge Save DC": 14,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "6",
    },
    "Vaskor, the Stone Maw": {
        "Recharge Name": "Seismic Roar",
        "Recharge Kind": "save",
        "Recharge Damage": "4d8",
        "Recharge Type": "bludgeoning",
        "Recharge Save DC": 15,
        "Recharge Save Ability": "strength",
        "Recharge Roll": "5-6",
    },
    "Ashthirst the Hollow": {
        "Recharge Name": "Hollow Wail",
        "Recharge Kind": "save",
        "Recharge Damage": "5d8",
        "Recharge Type": "psychic",
        "Recharge Save DC": 16,
        "Recharge Save Ability": "wisdom",
        "Recharge Roll": "5-6",
    },
    "Choralith, Voice Below": {
        "Recharge Name": "Subsonic Chord",
        "Recharge Kind": "save",
        "Recharge Damage": "6d8",
        "Recharge Type": "thunder",
        "Recharge Save DC": 17,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "5-6",
    },
    "Lumen of the Shattered Thread": {
        "Recharge Name": "Thread Shatter",
        "Recharge Kind": "save",
        "Recharge Damage": "6d10",
        "Recharge Type": "force",
        "Recharge Save DC": 18,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Threxus, the Iron Spiral": {
        "Recharge Name": "Iron Vortex",
        "Recharge Kind": "save",
        "Recharge Damage": "7d10",
        "Recharge Type": "bludgeoning",
        "Recharge Save DC": 19,
        "Recharge Save Ability": "strength",
        "Recharge Roll": "5-6",
    },
    "Eirfax, the Dusk Crowned": {
        "Recharge Name": "Crown of Dusk",
        "Recharge Kind": "save",
        "Recharge Damage": "8d8",
        "Recharge Type": "necrotic",
        "Recharge Save DC": 20,
        "Recharge Save Ability": "wisdom",
        "Recharge Roll": "5-6",
    },
    "Xarog the Pactbound Furnace": {
        "Recharge Name": "Inferno Pact",
        "Recharge Kind": "save",
        "Recharge Damage": "8d10",
        "Recharge Type": "fire",
        "Recharge Save DC": 21,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Xarog, the Pactbound Furnace": {
        "Recharge Name": "Inferno Pact",
        "Recharge Kind": "save",
        "Recharge Damage": "8d10",
        "Recharge Type": "fire",
        "Recharge Save DC": 21,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Gor Vekk, Architect of Ends": {
        "Recharge Name": "End Architecture",
        "Recharge Kind": "save",
        "Recharge Damage": "9d8",
        "Recharge Type": "force",
        "Recharge Save DC": 22,
        "Recharge Save Ability": "intelligence",
        "Recharge Roll": "5-6",
    },
    "The Marquis of Silence": {
        "Recharge Name": "Zone of Silence",
        "Recharge Kind": "save",
        "Recharge Damage": "10d10",
        "Recharge Type": "psychic",
        "Recharge Save DC": 23,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "5-6",
    },
}

# Diverse CR-band samples — draft Aethel-flavored names.
SANDBOX_RECHARGES: dict[str, dict[str, str | int]] = {
    "Aarakocra": {
        "Recharge Name": "Grave Shriek",
        "Recharge Kind": "save",
        "Recharge Damage": "1d6",
        "Recharge Type": "necrotic",
        "Recharge Save DC": 10,
        "Recharge Save Ability": "wisdom",
        "Recharge Roll": "6",
    },
    "Androsphinx": {
        "Recharge Name": "Caustic Surge",
        "Recharge Kind": "save",
        "Recharge Damage": "2d6",
        "Recharge Type": "acid",
        "Recharge Save DC": 11,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "6",
    },
    "Bandit": {
        "Recharge Name": "Desperate Lunge",
        "Recharge Kind": "attack",
        "Recharge Bonus": 4,
        "Recharge Damage": "1d8+2",
        "Recharge Type": "piercing",
        "Recharge Roll": "6",
    },
    "Allosaurus": {
        "Recharge Name": "Caustic Spit",
        "Recharge Kind": "save",
        "Recharge Damage": "2d8",
        "Recharge Type": "acid",
        "Recharge Save DC": 12,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Blood Hawk": {
        "Recharge Name": "Blood Dive",
        "Recharge Kind": "attack",
        "Recharge Bonus": 5,
        "Recharge Damage": "2d6+2",
        "Recharge Type": "slashing",
        "Recharge Roll": "6",
    },
    "Gloom Weaver": {
        "Recharge Name": "Shadow Weave",
        "Recharge Kind": "save",
        "Recharge Damage": "3d6",
        "Recharge Type": "necrotic",
        "Recharge Save DC": 13,
        "Recharge Save Ability": "wisdom",
        "Recharge Roll": "5-6",
    },
    "Babau": {
        "Recharge Name": "Abyssal Leak",
        "Recharge Kind": "save",
        "Recharge Damage": "3d8",
        "Recharge Type": "acid",
        "Recharge Save DC": 13,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "5-6",
    },
    "Deep Scion": {
        "Recharge Name": "Pressure Wave",
        "Recharge Kind": "save",
        "Recharge Damage": "4d6",
        "Recharge Type": "bludgeoning",
        "Recharge Save DC": 14,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "5-6",
    },
    "Acolyte": {
        "Recharge Name": "Warp Pulse",
        "Recharge Kind": "save",
        "Recharge Damage": "4d8",
        "Recharge Type": "psychic",
        "Recharge Save DC": 15,
        "Recharge Save Ability": "wisdom",
        "Recharge Roll": "5-6",
    },
    "Bard": {
        "Recharge Name": "Dissonant Verse",
        "Recharge Kind": "save",
        "Recharge Damage": "4d8",
        "Recharge Type": "thunder",
        "Recharge Save DC": 15,
        "Recharge Save Ability": "constitution",
        "Recharge Roll": "5-6",
    },
    "Aboleth": {
        "Recharge Name": "Mind Lash",
        "Recharge Kind": "save",
        "Recharge Damage": "5d6",
        "Recharge Type": "psychic",
        "Recharge Save DC": 16,
        "Recharge Save Ability": "intelligence",
        "Recharge Roll": "5-6",
    },
    "Amnizu": {
        "Recharge Name": "Hellfire Cone",
        "Recharge Kind": "save",
        "Recharge Damage": "5d8",
        "Recharge Type": "fire",
        "Recharge Save DC": 16,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Air Elemental Myrmidon": {
        "Recharge Name": "Gale Burst",
        "Recharge Kind": "save",
        "Recharge Damage": "5d10",
        "Recharge Type": "lightning",
        "Recharge Save DC": 17,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Abyssal Wretch": {
        "Recharge Name": "Soul Scream",
        "Recharge Kind": "save",
        "Recharge Damage": "6d8",
        "Recharge Type": "necrotic",
        "Recharge Save DC": 17,
        "Recharge Save Ability": "wisdom",
        "Recharge Roll": "5-6",
    },
    "Adult Blue Dracolich": {
        "Recharge Name": "Lightning Breath",
        "Recharge Kind": "save",
        "Recharge Damage": "8d10",
        "Recharge Type": "lightning",
        "Recharge Save DC": 19,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
    "Ancient Bronze Dragon": {
        "Recharge Name": "Repulsion Breath",
        "Recharge Kind": "save",
        "Recharge Damage": "9d10",
        "Recharge Type": "lightning",
        "Recharge Save DC": 21,
        "Recharge Save Ability": "dexterity",
        "Recharge Roll": "5-6",
    },
}

ALL_RECHARGES = {**GUARDIAN_RECHARGES, **SANDBOX_RECHARGES}


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in RECHARGE_COLUMNS:
        if col not in df.columns:
            df[col] = None
    return df


def backup_workbook() -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = BACKUP_DIR / f"Bestiary_before_recharge_{stamp}.xlsx"
    shutil.copy2(PRIMARY_XLSX, dest)
    return dest


def apply_recharges(force: bool = False) -> dict[str, int]:
    backup = backup_workbook()
    df = pd.read_excel(PRIMARY_XLSX, sheet_name="Monsters")
    df = ensure_columns(df)

    written = 0
    skipped = 0
    missing = 0

    for idx, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        if not name or name.lower() == "nan":
            continue
        payload = ALL_RECHARGES.get(name)
        if not payload:
            continue
        if not force and clean_cell(row.get("Recharge Name")):
            skipped += 1
            continue
        for col, val in payload.items():
            df.at[idx, col] = val
        written += 1

    for name in ALL_RECHARGES:
        if name not in df["Name"].astype(str).values:
            missing += 1

    # Preserve column order: append new cols after Combat Provenance
    base_cols = [c for c in df.columns if c not in RECHARGE_COLUMNS]
    prov_idx = base_cols.index("Combat Provenance") if "Combat Provenance" in base_cols else len(base_cols)
    ordered = base_cols[: prov_idx + 1] + RECHARGE_COLUMNS + base_cols[prov_idx + 1 :]
    ordered = list(dict.fromkeys(ordered))
    df = df[ordered]

    with pd.ExcelWriter(PRIMARY_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="Monsters", index=False)

    return {
        "backup": str(backup),
        "written": written,
        "skipped_existing": skipped,
        "names_not_in_sheet": missing,
        "total_recharge_defs": len(ALL_RECHARGES),
    }


def clean_cell(value: object) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    return text if text and text.lower() != "nan" else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Author recharge rows into Bestiary.xlsx")
    parser.add_argument("--force", action="store_true", help="Overwrite existing Recharge Name cells")
    args = parser.parse_args()
    import json

    print(json.dumps(apply_recharges(force=args.force), indent=2))
