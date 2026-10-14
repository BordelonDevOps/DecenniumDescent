#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_excel(ROOT / "bestiary_metadata_source.xlsx", sheet_name="Monsters")
row = df[df["Name"] == "Aarakocra"].iloc[0]
print("Excel Aarakocra:", {k: row[k] for k in ["Name", "Size", "Type", "Challenge", "XP", "Zone Found"]})

with (ROOT / "src" / "bestiary_data_full.json").open(encoding="utf-8") as f:
    data = json.load(f)

gate = [c for c in data if c.get("hitPoints", 1) > 1 or c.get("combat")]
print(f"\nGate/authored entries: {len(gate)}")
for c in gate:
    print(
        f"  {c['name']}: AC={c.get('armorClass')} HP={c.get('hitPoints')} "
        f"CR={c.get('challengeRating')} combat={bool(c.get('combat'))}"
    )

names = Counter(c["name"] for c in data)
dups = {n: c for n, c in names.items() if c > 1}
print(f"\nDuplicate names: {len(dups)}")
for n, c in sorted(dups.items())[:20]:
    print(f"  {n}: {c}x")
