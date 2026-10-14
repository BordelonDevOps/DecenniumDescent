"""Measure Oracle Tier II revelation description lengths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/data/oracle-mysteries.js").read_text(encoding="utf-8")

rows = []
for m in re.finditer(
    r'id: "(\w+)".*?tierII: \[(.*?)\],\s*tierIII:',
    text,
    re.DOTALL,
):
    mid = m.group(1)
    block = m.group(2)
    for rev in re.finditer(
        r'name: "([^"]+)".*?description:\s*"((?:[^"\\]|\\.)*)"',
        block,
        re.DOTALL,
    ):
        name, desc = rev.group(1), rev.group(2)
        rows.append((len(desc), mid, name, desc))

rows.sort()
print("ALL TIER II (shortest first):")
for length, mid, name, desc in rows:
    draft_marker = " [draft]" if mid != "ancestor" else ""
    print(f"{length:3d} | {mid:10s} | {name}{draft_marker}")

draft_rows = [r for r in rows if r[1] != "ancestor"]
print(f"\nDraft total: {len(draft_rows)}")
thin = [r for r in draft_rows if r[0] <= 130]
print(f"Draft thin (<=130): {len(thin)}")
for r in thin:
    print(f"  {r[0]:3d} | {r[1]:10s} | {r[2]}")
