# -*- coding: utf-8 -*-
"""Extract NeedsReview / Traits / Combat Provenance / Tags from Bestiary.xlsx
into scripts/_excel_extra.json, keyed by monster Name.

This is a read-only export used by generate_codex_of_heartcell.js to cross-check
src/bestiary_data_full.json against the workbook's own data-quality flags.
Re-run this after any Bestiary.xlsx edit, then re-run generate_codex_of_heartcell.js.
"""
from __future__ import annotations

import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]


def cell(row, idx, key, default=None):
    i = idx.get(key)
    if i is None or i >= len(row):
        return default
    return row[i] if row[i] is not None else default


def main() -> None:
    wb = openpyxl.load_workbook(ROOT / "Bestiary.xlsx", read_only=True, data_only=True)
    ws = wb["Monsters"]
    rows = ws.iter_rows(values_only=True)
    header = [str(h) if h else f"c{i}" for i, h in enumerate(next(rows))]
    idx = {h: i for i, h in enumerate(header)}

    extra: dict[str, dict] = {}
    for row in rows:
        name = cell(row, idx, "Name")
        if not name:
            continue
        name = str(name).strip()
        extra[name] = {
            "needsReview": cell(row, idx, "NeedsReview"),
            "traits": cell(row, idx, "Traits"),
            "combatProvenance": cell(row, idx, "Combat Provenance"),
            "tags": cell(row, idx, "Tags"),
        }
    wb.close()

    out_path = Path(__file__).resolve().parent / "_excel_extra.json"
    out_path.write_text(json.dumps(extra, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out_path} ({len(extra)} rows)")


if __name__ == "__main__":
    main()
