"""Measure Oracle mysticInsight / propheticSurge / finalRevelation description lengths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/data/oracle-mysteries.js").read_text(encoding="utf-8")

DRAFT_IDS = [
    "battle",
    "bones",
    "cataclysm",
    "dream",
    "flame",
    "life",
    "shadow",
    "stars",
    "time",
]
FIELDS = ["mysticInsight", "propheticSurge", "finalRevelation"]


def get_field(mid: str, field: str) -> tuple[str, str] | None:
    pat = rf'id: "{mid}".*?(?=^\s{{2}}\{{\s*$|\Z)'
    m = re.search(pat, text, re.DOTALL | re.MULTILINE)
    if not m:
        return None
    block = m.group(0)
    fp = rf'{field}: \{{\s*name: "([^"]+)".*?description:\s*"((?:[^"\\]|\\.)*)"'
    fm = re.search(fp, block, re.DOTALL)
    if fm:
        return fm.group(1), fm.group(2)
    return None


ancestor = {f: get_field("ancestor", f) for f in FIELDS}
print("ANCESTOR baselines:")
for f in FIELDS:
    name, desc = ancestor[f]  # type: ignore[misc]
    print(f"  {f}: {len(desc)} chars | {name}")

for f in FIELDS:
    anc_len = len(ancestor[f][1])  # type: ignore[index]
    print(f"\n=== {f} (draft mysteries, shortest first; ancestor={anc_len}) ===")
    rows = []
    for mid in DRAFT_IDS:
        r = get_field(mid, f)
        if r:
            name, desc = r
            rows.append((len(desc), mid, name, desc))
    rows.sort()
    thin = sum(1 for length, *_ in rows if length < anc_len * 0.85)
    for length, mid, name, _desc in rows:
        flag = " THIN" if length < anc_len * 0.85 else ""
        print(f"{length:3d} | {mid:10s} | {name}{flag}")
    print(f"thin (<85% ancestor): {thin}/{len(rows)}")
