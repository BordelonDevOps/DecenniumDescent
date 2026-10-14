"""Summarize Abjuration spell class tag coverage."""
import re
from pathlib import Path

text = Path(__file__).resolve().parents[1].joinpath("src/data/spells.js").read_text(encoding="utf-8")
expected = {"Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"}
abj = []
for m in re.finditer(
    r'name:\s*"([^"]+)"[^{}]*?school:\s*"Abjuration"[^{}]*?classes:\s*\[([^\]]*)\]',
    text,
    re.S,
):
    classes = set(re.findall(r'"([^"]+)"', m.group(2)))
    missing = expected - classes
    if missing:
        abj.append((m.group(1), sorted(missing)))

print(f"abjuration_spells={len(re.findall(r'school: \"Abjuration\"', text))}")
print(f"with_missing_tags={len(abj)}")
for name, miss in abj[:10]:
    print(f"  {name}: missing {miss}")
