"""Find prestige-referenced feat names missing from feats.js."""
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

    defined = set(re.findall(r'"name":\s*"([^"]+)"', feats_text))
    missing = sorted(feat_names - defined)

    print(f"prestige_feat_refs={len(feat_names)}")
    print(f"defined_feats={len(defined)}")
    print(f"missing={len(missing)}")
    for f in missing:
        print(f"  {f}")


if __name__ == "__main__":
    main()
