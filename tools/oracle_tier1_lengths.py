"""Measure Oracle Tier I revelation description lengths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/data/oracle-mysteries.js").read_text(encoding="utf-8")

rows = []
for m in re.finditer(
    r'id: "(\w+)".*?tierI: \[(.*?)\],\s*tierII:',
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
for length, mid, name, desc in rows:
    print(f"{length:3d} | {mid:10s} | {name}")
