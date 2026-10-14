#!/usr/bin/env python3
"""Probe bestiary and class sources for pack runners."""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[3]
print("ROOT", ROOT)

mons = json.loads((ROOT / "src/bestiary_data_full.json").read_text(encoding="utf-8"))
names = [
    "Cave Bear", "Crystal Shardling", "Deep Dwarf", "Chaos-Husk Tadpole", "Deep Scion",
    "Fracture-Kin Fleshwright", "Charnel Crawler", "Ashthirst the Hollow", "Angry Grief-Bound",
    "Choralith, Voice Below", "Corrosion Grazer", "Fracture-Kin Nightreaver",
]
by = {m.get("name"): m for m in mons}
for n in names:
    m = by.get(n)
    if m:
        print(f"FOUND {n}: HP={m.get('hitPoints')} AC={m.get('armorClass')} CR={m.get('challengeRating')} acts={len(m.get('actions') or [])}")
    else:
        hits = [x["name"] for x in mons if n.lower().split(",")[0] in (x.get("name") or "").lower()]
        print(f"MISS {n} ~ {hits[:8]}")

core = (ROOT / "src/data/class-core-mechanics.js").read_text(encoding="utf-8")
print("core len", len(core))
print(core[:1200])

# class keys in class-details
cd = (ROOT / "src/data/class-details.js").read_text(encoding="utf-8")
keys = re.findall(r'^\s{2}(?:"([^"]+)"|([A-Za-z][A-Za-z ]+)):\s*\{', cd, re.M)
print("class-details keys sample", keys[:25])

# feats/spells counts
feats = (ROOT / "src/data/feats.js").read_text(encoding="utf-8")
spells = (ROOT / "src/data/spells.js").read_text(encoding="utf-8")
print("feats size", len(feats), "spells size", len(spells))
print("feat name hits", len(re.findall(r'name:\s*[\'"]', feats)))
print("spell name hits", len(re.findall(r'name:\s*[\'"]', spells)))
