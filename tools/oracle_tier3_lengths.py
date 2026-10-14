"""Measure Oracle Tier III revelation description lengths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/data/oracle-mysteries.js").read_text(encoding="utf-8")

rows = []
for m in re.finditer(
    r'id: "(\w+)".*?tierIII: \{.*?name: "([^"]+)".*?description:\s*"((?:[^"\\]|\\.)*)"',
    text,
    re.DOTALL,
):
    mid, name, desc = m.group(1), m.group(2), m.group(3)
    if mid == "ancestor":
        continue
    rows.append((len(desc), mid, name, desc))

rows.sort()
print("Draft Tier III (shortest first):")
for length, mid, name, desc in rows:
    flag = " THIN" if length <= 130 else ""
    print(f"{length:3d} | {mid:10s} | {name}{flag}")
print(f"\nTotal: {len(rows)}, thin (<=130): {sum(1 for r in rows if r[0] <= 130)}")
