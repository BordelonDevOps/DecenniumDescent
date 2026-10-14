#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,hashlib
HERE=Path(__file__).resolve();LAB=HERE.parent.parent;ROOT=LAB.parent.parent
checks=[['python','tools/validate_magic_system.py'],['node','--no-warnings','tools/validate_class_abilities.mjs'],['python','tools/validate_public_canon.py'],['python','tools/validate_gameplay_loop.py'],['python','tools/validate_prestige_snapshot.py'],['python','tools/validate_gameplay_state.py']]
for c in checks:
 r=subprocess.run(c,cwd=ROOT)
 if r.returncode:raise SystemExit(r.returncode)
profiles=list((LAB/'player-profiles').glob('*/*.md'));packs=list((LAB/'packs').glob('[0-9][0-9]-*'))
if len(profiles)!=68:raise SystemExit(f'Expected 68 player profiles, found {len(profiles)}')
if len(packs)<20:raise SystemExit(f'Expected at least 20 packs, found {len(packs)}')
paths=[ROOT/'CANON_MANIFEST.json',ROOT/'data/public/Decennium_Descent_Gameplay_Loop_v1_2.json',ROOT/'src/data/gameplay-loop.json',ROOT/'src/bestiary_data_full.json']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(LAB/'source-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
manifest={'release':'V7.2','profiles':len(profiles),'packs':len(packs),'sourceHashes':'source-hashes.json','sourceMutationAllowed':False}
(LAB/'run-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
