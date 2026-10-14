"""Spot-check draft Oracle curse boon depth vs Spiral-Touched."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/data/oracle-curses.js").read_text(encoding="utf-8")

curse_blocks = re.split(r"\n  \{\n\n    id:", text)[1:]
spiral_boons: list[tuple] = []
thin: list[tuple] = []


def count_sentences(s: str) -> int:
    parts = re.split(r"(?<=[.!?])\s+", s.strip())
    return len([p for p in parts if p.strip()])


for block in curse_blocks:
    id_m = re.match(r' "([^"]+)"', block)
    if not id_m:
        continue
    cid = id_m.group(1)
    draft = "draft: true" in block
    pattern = (
        r'level: (\d+),\s*\n\s*name: "([^"]+)",\s*\n\s*description:\s*\n\s*"([^"]+)"'
    )
    for bm in re.finditer(pattern, block):
        lvl, name, desc = bm.group(1), bm.group(2), bm.group(3)
        sc = count_sentences(desc)
        entry = (cid, lvl, name, sc, len(desc), desc)
        if cid == "spiral-touched":
            spiral_boons.append(entry)
        elif draft and sc < 2:
            thin.append(entry)

print("=== Spiral-Touched reference ===")
for e in spiral_boons:
    print(f"  L{e[1]}: {e[3]} sentences, {e[4]} chars")

print(f"\n=== Draft boons under 2 sentences ({len(thin)}) ===")
for e in sorted(thin, key=lambda x: (x[3], x[4])):
    preview = e[5] if len(e[5]) <= 100 else e[5][:97] + "..."
    print(f"  {e[0]} L{e[1]} ({e[3]} sent, {e[4]} chars): {preview}")
