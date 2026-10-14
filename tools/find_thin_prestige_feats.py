"""Find prestige-referenced feats with short effect text."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    lore = json.loads((ROOT / "src/data/prestige-lorebook.json").read_text(encoding="utf-8"))
    feats_text = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")

    feat_names: set[str] = set()
    for p in lore:
        req = p.get("requirements", "")
        m = re.search(r"Feats:\s*(.+?)\s*-\s*Skills:", req)
        if m:
            for f in re.split(r",\s*", m.group(1).strip()):
                f = f.strip()
                if f:
                    feat_names.add(f)

    # Parse feats blocks (simple split on name fields)
    feats: dict[str, dict] = {}
    for block in re.split(r"\n  \{", feats_text):
        name_m = re.search(r'"name":\s*"([^"]+)"', block)
        if not name_m:
            continue
        name = name_m.group(1)
        effect_m = re.search(r'"effect":\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
        desc_m = re.search(r'"description":\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
        draft = '"draft": true' in block
        feats[name] = {
            "effect_len": len(effect_m.group(1)) if effect_m else 0,
            "effect": effect_m.group(1) if effect_m else "",
            "desc_len": len(desc_m.group(1)) if desc_m else 0,
            "draft": draft,
        }

    thin = []
    for fn in sorted(feat_names):
        if fn not in feats:
            thin.append((fn, 0, "", False, "MISSING"))
            continue
        f = feats[fn]
        if fn not in feats:
            continue
        f = feats[fn]
        if not f["draft"]:
            continue
        if f["effect_len"] < 200:
            thin.append((fn, f["effect_len"], f["effect"][:120], f["draft"], "short"))

    print(f"prestige_refs={len(feat_names)}")
    print(f"thin_candidates={len(thin)}")
    for item in thin:
        print(f"  {item[0]!r} len={item[1]} draft={item[3]} {item[4]}")
        if item[2]:
            print(f"    -> {item[2]}...")


if __name__ == "__main__":
    main()
