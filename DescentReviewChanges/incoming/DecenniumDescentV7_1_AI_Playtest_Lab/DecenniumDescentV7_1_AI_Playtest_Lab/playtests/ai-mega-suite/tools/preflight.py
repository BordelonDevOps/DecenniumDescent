#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, hashlib, os

HERE=Path(__file__).resolve()
LAB=HERE.parent.parent
ROOT=LAB.parent.parent
errors=[]
required=[
    ROOT/"AGENTS.md",
    ROOT/"CANON_MANIFEST.json",
    ROOT/"data/public/Decennium_Descent_Gameplay_Loop_v1_1.json",
    ROOT/"src/data/gameplay-loop.json",
    ROOT/"src/data/class-core-mechanics.js",
    ROOT/"src/data/feats.js",
    ROOT/"src/data/spells.js",
    ROOT/"src/bestiary_data_full.json",
]
for p in required:
    if not p.exists():
        errors.append(f"Missing: {p.relative_to(ROOT)}")
for p in [ROOT/"data/public/Decennium_Descent_Gameplay_Loop_v1_1.json",ROOT/"src/bestiary_data_full.json"]:
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Invalid JSON {p}: {exc}")

packs=sorted((LAB/"packs").glob("[0-9][0-9]-*"))
profiles=sorted((LAB/"player-profiles").glob("*/*.md"))
if len(packs)<18:
    errors.append(f"Expected 18 packs, found {len(packs)}")
if len(profiles)!=68:
    errors.append(f"Expected 68 player profiles, found {len(profiles)}")

hashes={}
for p in required:
    if p.exists():
        hashes[str(p.relative_to(ROOT)).replace("\\","/")]=hashlib.sha256(p.read_bytes()).hexdigest()
(LAB/"source-hashes.json").write_text(json.dumps(hashes,indent=2),encoding="utf-8")

manifest={
    "suite":"Decennium Descent V7.1 AI Playtest Lab",
    "packs":[p.name for p in packs],
    "playerProfiles":len(profiles),
    "sourceHashes":"source-hashes.json",
    "status":"FAIL" if errors else "PASS",
    "errors":errors,
}
(LAB/"run-manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
sys.exit(1 if errors else 0)
