#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'src/data/prestige-lorebook.json'; snap=ROOT/'docs/prestige/prestige-registry-snapshot.json'
errors=[]
if not source.exists(): errors.append('Missing prestige lorebook source')
if not snap.exists(): errors.append('Missing prestige registry snapshot')
if not errors:
    src=json.loads(source.read_text(encoding='utf-8')); out=json.loads(snap.read_text(encoding='utf-8'))
    rows=out.get('paths',[])
    if len(src)!=len(rows): errors.append(f'Prestige count mismatch source={len(src)} snapshot={len(rows)}')
    names=[x.get('name','').strip().lower() for x in rows]
    if any(not x for x in names): errors.append('Prestige snapshot contains blank names')
    if len(names)!=len(set(names)): errors.append('Prestige snapshot contains duplicate names')
    if any(not x.get('hallmarks') for x in rows): errors.append('Prestige snapshot contains path without hallmarks')
if errors:
    print('Prestige snapshot validation: FAIL'); [print(f'- {e}') for e in errors]; sys.exit(1)
print(f'Prestige snapshot validation: PASS - {len(rows)} paths')
