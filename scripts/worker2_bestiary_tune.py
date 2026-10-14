#!/usr/bin/env python3
"""Worker 2 — fix Size/Type/CR garbage, tune low-CR HP, add NeedsReview flags."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "Bestiary.xlsx"
BACKUP_DIR = ROOT / "backups"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from scrub_bestiary_ip import rename_value  # noqa: E402

GATE_GUARDIANS = {
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

VALID_SIZES = ("Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan")
VALID_TYPES = {
    "aberration", "beast", "celestial", "construct", "dragon", "elemental",
    "fey", "fiend", "giant", "humanoid", "monstrosity", "ooze", "plant", "undead",
}

SIZE_RANK = {s: i for i, s in enumerate(VALID_SIZES)}

# Draft minimum size for a CR band (Worker 2 heuristic — not SRD canon).
CR_SIZE_FLOOR = [
    (20, "Gargantuan"),
    (11, "Huge"),
    (5, "Large"),
    (1, "Medium"),
    (0.25, "Small"),
    (0, "Tiny"),
]


def cr_float(raw) -> float:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return 0.0
    text = str(raw).strip()
    if not text or text.lower() == "nan":
        return 0.0
    if "/" in text:
        num, den = text.split("/", 1)
        try:
            return float(num) / float(den)
        except ValueError:
            return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def normalize_cr(raw) -> str:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return "0"
    text = str(raw).strip()
    return text if text and text.lower() != "nan" else "0"


def expected_size_for_cr(cr: float) -> str:
    for threshold, size in CR_SIZE_FLOOR:
        if cr >= threshold:
            return size
    return "Tiny"


def clean_type(raw) -> str | None:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return None
    text = str(raw).strip()
    if not text or text.lower() in ("nan", "none"):
        return None
    base = text.split("(")[0].strip().lower()
    return base if base in VALID_TYPES else None


def size_mismatch_flags(size: str, cr: float) -> list[str]:
    flags: list[str] = []
    if size not in VALID_SIZES:
        flags.append("invalid-size")
        return flags
    expected = expected_size_for_cr(cr)
    delta = SIZE_RANK[size] - SIZE_RANK[expected]
    if delta >= 2:
        flags.append(f"oversized-for-cr{cr:g}")
    if delta <= -2:
        flags.append(f"undersized-for-cr{cr:g}")
    if size in ("Huge", "Gargantuan") and cr <= 0.25:
        flags.append("huge-at-low-cr")
    if size == "Tiny" and cr >= 10:
        flags.append("tiny-at-high-cr")
    if size == "Small" and cr >= 15:
        flags.append("small-at-legendary-cr")
    return flags


def draft_size_fix(size: str, cr: float) -> tuple[str, bool]:
    if size not in VALID_SIZES:
        return expected_size_for_cr(cr), True
    expected = expected_size_for_cr(cr)
    if abs(SIZE_RANK[size] - SIZE_RANK[expected]) >= 2:
        return expected, True
    if size in ("Huge", "Gargantuan") and cr <= 0.25:
        return expected, True
    if size == "Tiny" and cr >= 10:
        return expected, True
    if size == "Small" and cr >= 15:
        return expected, True
    return size, False


def hp_bump(cr: float, hp) -> tuple[int | None, bool]:
    if hp is None or (isinstance(hp, float) and pd.isna(hp)):
        return None, False
    old = int(hp)
    if cr <= 0:
        new = max(old, round(old * 1.35), 8)
    elif cr <= 0.125:
        new = max(old, round(old * 1.30), 10)
    elif cr <= 0.25:
        new = max(old, round(old * 1.25), 14)
    elif cr <= 0.5:
        new = max(old, round(old * 1.20), 26)
    elif cr <= 1:
        new = max(old, round(old * 1.15), 52)
    elif cr <= 2:
        new = max(old, round(old * 1.10), 68)
    elif cr <= 3:
        new = max(old, round(old * 1.08), 88)
    else:
        return old, False
    return new, new != old


def main() -> None:
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIR / f"Bestiary_worker2_{stamp}.xlsx"
    shutil.copy2(PRIMARY, backup_path)

    df = pd.read_excel(PRIMARY, sheet_name="Monsters")
    if "NeedsReview" not in df.columns:
        df["NeedsReview"] = ""

    stats = {
        "backup": str(backup_path),
        "rows_scanned": 0,
        "size_fixed": 0,
        "type_fixed": 0,
        "hp_tuned": 0,
        "needs_review_flagged": 0,
        "guardians_skipped": 0,
        "touched_rows": 0,
    }
    samples: list[str] = []

    for idx, row in df.iterrows():
        name_raw = row.get("Name")
        if pd.isna(name_raw):
            continue
        name = str(name_raw).strip()
        scrubbed = rename_value(name)
        stats["rows_scanned"] += 1

        if scrubbed in GATE_GUARDIANS:
            stats["guardians_skipped"] += 1
            continue

        touched = False
        notes: list[str] = []

        size = str(row.get("Size") or "").strip()
        ctype_raw = row.get("Type")
        cr_raw = normalize_cr(row.get("Challenge"))
        cr = cr_float(cr_raw)

        flags = size_mismatch_flags(size, cr)
        new_size, size_changed = draft_size_fix(size, cr)
        if size_changed:
            df.at[idx, "Size"] = new_size
            stats["size_fixed"] += 1
            touched = True
            notes.append(f"size:{size}->{new_size}")

        if clean_type(ctype_raw) is None:
            df.at[idx, "Type"] = "Monstrosity"
            stats["type_fixed"] += 1
            touched = True
            notes.append("type->Monstrosity")

        # CR suspect when size was huge at low CR but CR unchanged — author must confirm
        if flags and "huge-at-low-cr" in flags and not size_changed:
            notes.append("cr-suspect-low")
        if flags and any("undersized" in f for f in flags):
            notes.append("cr-suspect-high")

        final_size = str(df.at[idx, "Size"]).strip()
        final_cr = cr_float(df.at[idx, "Challenge"])
        residual = size_mismatch_flags(final_size, final_cr)
        if residual:
            stats["needs_review_flagged"] += 1
            notes.extend(residual)

        if "HP" in df.columns:
            old_hp = df.at[idx, "HP"]
            new_hp, hp_changed = hp_bump(final_cr, old_hp)
            if hp_changed and new_hp is not None:
                df.at[idx, "HP"] = new_hp
                stats["hp_tuned"] += 1
                touched = True
                notes.append(f"hp:{int(old_hp)}->{new_hp}")

        if notes:
            df.at[idx, "NeedsReview"] = "; ".join(dict.fromkeys(notes))
            if touched:
                stats["touched_rows"] += 1
                if len(samples) < 12:
                    samples.append(f"{name}: {df.at[idx, 'NeedsReview']}")

    wb = load_workbook(PRIMARY)
    ws = wb["Monsters"]
    headers = [cell.value for cell in ws[1]]
    header_to_col = {str(h).strip(): i + 1 for i, h in enumerate(headers) if h}
    if "NeedsReview" not in header_to_col:
        col = len(headers) + 1
        ws.cell(row=1, column=col, value="NeedsReview")
        header_to_col["NeedsReview"] = col

    name_col = header_to_col.get("Name", 1)
    name_to_row = {
        str(ws.cell(row=r, column=name_col).value).strip(): r
        for r in range(2, ws.max_row + 1)
        if ws.cell(row=r, column=name_col).value
    }

    for col_name in ("Size", "Type", "HP", "NeedsReview"):
        if col_name not in header_to_col:
            continue
        for _, data_row in df.iterrows():
            name = data_row.get("Name")
            if pd.isna(name):
                continue
            r = name_to_row.get(str(name).strip())
            if not r:
                continue
            val = data_row.get(col_name)
            if val is not None and not (isinstance(val, float) and pd.isna(val)):
                ws.cell(row=r, column=header_to_col[col_name], value=val)

    wb.save(PRIMARY)
    stats["samples"] = samples
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
