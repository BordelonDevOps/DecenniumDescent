#!/usr/bin/env python3
"""Phase C: retune Bloom Spore Burst in Bestiary.xlsx (Excel-first)."""
from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "Bestiary.xlsx"
BACKUP_DIR = ROOT / "backups"


def main() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    BACKUP_DIR.mkdir(exist_ok=True)
    backup = BACKUP_DIR / f"Bestiary_phaseC_{stamp}.xlsx"
    shutil.copy2(XLSX, backup)

    df = pd.read_excel(XLSX, sheet_name="Monsters")
    mask = df["Name"] == "The Bloom That Hungers"
    if not mask.any():
        raise SystemExit("Bloom row not found")

    idx = df[mask].index[0]
    print("Before:", df.loc[idx, ["Recharge Damage", "Recharge Roll"]].to_dict())
    df.at[idx, "Recharge Damage"] = "1d8"
    df.at[idx, "Recharge Roll"] = "6"
    print("After:", df.loc[idx, ["Recharge Damage", "Recharge Roll"]].to_dict())

    with pd.ExcelWriter(XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="Monsters", index=False)
    print("Backup:", backup)


if __name__ == "__main__":
    main()
