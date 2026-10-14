"""Scan class-draft-levels.js for thin non-ASI milestones."""
import re
from pathlib import Path

text = Path("src/data/class-draft-levels.js").read_text(encoding="utf-8")
ASI = re.compile(r"Ability Score Improvement", re.I)
thin = []
for m in re.finditer(r'd\("([^"]+)"\)', text):
    feat = m.group(1)
    if ASI.search(feat):
        continue
    if len(feat) < 100:
        # find class context (rough: look back for class name)
        pos = m.start()
        cls_m = list(re.finditer(r"^\s+(\w+(?:\s+\w+)?):\s*\{", text[:pos], re.M))
        cls = cls_m[-1].group(1) if cls_m else "?"
        lvl_m = list(re.finditer(r"(\d+):\s*\[d\(", text[:pos]))
        lvl = lvl_m[-1].group(1) if lvl_m else "?"
        thin.append((len(feat), cls, lvl, feat))
thin.sort()
print(f"Thin non-ASI (<100 chars): {len(thin)}")
for ln, cls, lvl, feat in thin:
    print(f"{ln:3d} | {cls} L{lvl} | {feat[:90]}")
