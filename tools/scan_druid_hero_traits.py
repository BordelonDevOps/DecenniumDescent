"""Scan druid hero-form trait line lengths."""
import re
from pathlib import Path

text = Path("src/data/druid-shapeshifting.js").read_text(encoding="utf-8")
# Only HERO_FORMS block
start = text.index("export const HERO_FORMS_BY_CIRCLE")
end = text.index("export const DRUID_CIRCLES")
block = text[start:end]
traits = []
for m in re.finditer(r'traits:\s*\[(.*?)\]', block, re.S):
    for s in re.findall(r'"([^"]+)"', m.group(1)):
        traits.append(s)
traits.sort(key=len)
for t in traits:
    print(f"{len(t):3d} | {t}")
print("---")
print(f"Total: {len(traits)}")
print(f"Under 50: {sum(1 for t in traits if len(t) < 50)}")
print(f"Under 60: {sum(1 for t in traits if len(t) < 60)}")
