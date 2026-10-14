"""List prestige draft feats sorted by effect length."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
lore = json.loads((ROOT / "src/data/prestige-lorebook.json").read_text(encoding="utf-8"))
feats_text = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")
feat_names = set()
for p in lore:
    req = p.get("requirements", "")
    m = re.search(r"Feats:\s*(.+?)\s*-\s*Skills:", req)
    if m:
        for f in re.split(r",\s*", m.group(1).strip()):
            if f.strip():
                feat_names.add(f.strip())
feats = {}
for block in re.split(r"\n  \{", feats_text):
    name_m = re.search(r'"name":\s*"([^"]+)"', block)
    if not name_m:
        continue
    name = name_m.group(1)
    effect_m = re.search(r'"effect":\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
    draft = '"draft": true' in block
    if name in feat_names:
        eff = effect_m.group(1) if effect_m else ""
        feats[name] = (len(eff), draft, eff)
print("draft prestige feats under 320 chars:")
for n in sorted(feats, key=lambda x: feats[x][0]):
    l, d, e = feats[n]
    if d and l < 320:
        print(f"  {l:3d}  {n}")
        print(f"       {e[:140]}...")
