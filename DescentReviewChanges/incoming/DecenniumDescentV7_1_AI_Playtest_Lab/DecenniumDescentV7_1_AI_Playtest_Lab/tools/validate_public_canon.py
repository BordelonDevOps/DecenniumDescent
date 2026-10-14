#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'src'
PUBLIC_DATA=ROOT/'data/public'
PUBLIC_DOCS=ROOT/'docs/mechanics'
errors=[]
# Exact public leaks. Spell tiers 7-9 are not dungeon tiers and are allowed.
patterns={
 'Marquis title': re.compile(r'\bMarquis\b',re.I),
 'Floor 100': re.compile(r'\bFloor 100\b',re.I),
 'Level 97': re.compile(r'\bLevel 97\b',re.I),
 'Hidden claimant state': re.compile(r'\b(hidden|final|surviving) claimant(s| state)?\b',re.I),
 'Deep Guardian names': re.compile(r'\b(Xarog|Eirfax|Threxus)\b',re.I),
 'Focusing crystal secret': re.compile(r'\bfocusing crystal\b',re.I),
 'Global Silent One failure': re.compile(r'Silent Ones? attack|global event.*Silent',re.I),
 'Confirmed deep dungeon tier': re.compile(r'\b(?:Gate|Dungeon Tier)\s*(?:VII|VIII|IX|X|7|8|9|10)\b',re.I),
}
for scan_root in (SRC, PUBLIC_DATA, PUBLIC_DOCS):
    if not scan_root.exists():
        continue
    for p in scan_root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in {'.js','.jsx','.ts','.tsx','.json','.md','.txt'}: continue
        text=p.read_text(errors='ignore')
        for label,pat in patterns.items():
            for m in pat.finditer(text):
                line=text.count('\n',0,m.start())+1
                errors.append(f'{p.relative_to(ROOT)}:{line}: {label}: {m.group(0)}')
# Structured boundary checks
try:
    floors=json.loads((SRC/'data/floor-encounters.json').read_text())
    tiers=floors.get('tiers',floors) if isinstance(floors,dict) else floors
    vals=[]
    if isinstance(tiers,list):
        for x in tiers:
            if isinstance(x,dict): vals.append(int(x.get('tier',0)))
    elif isinstance(tiers,dict): vals=[int(k) for k in tiers if str(k).isdigit()]
    if any(t>6 for t in vals): errors.append(f'floor-encounters.json exposes tiers {sorted(set(t for t in vals if t>6))}')
except Exception as e: errors.append(f'floor-encounters.json invalid: {e}')
try:
    best=json.loads((SRC/'bestiary_data_full.json').read_text())
    if len(best)!=65: errors.append(f'Known Descent bestiary expected 65 dossiers, found {len(best)}')
except Exception as e: errors.append(f'bestiary_data_full.json invalid: {e}')
try:
    craft=json.loads((SRC/'data/crafting-recipes.json').read_text())
    rows=craft.get('recipes',craft) if isinstance(craft,dict) else craft
    bad=[r.get('id','?') for r in rows if isinstance(r,dict) and (r.get('visibility')!='public' or int(r.get('tier',r.get('recipeTier',0)) or 0)>5)]
    if bad: errors.append(f'Public crafting runtime contains {len(bad)} restricted/deep recipes; first={bad[:5]}')
except Exception as e: errors.append(f'crafting-recipes.json invalid: {e}')
if errors:
    print('FAIL public-canon-boundary')
    print('\n'.join(errors[:100]))
    sys.exit(1)
print('PASS public-canon-boundary bestiary=65 tiers<=6 crafting=public')
