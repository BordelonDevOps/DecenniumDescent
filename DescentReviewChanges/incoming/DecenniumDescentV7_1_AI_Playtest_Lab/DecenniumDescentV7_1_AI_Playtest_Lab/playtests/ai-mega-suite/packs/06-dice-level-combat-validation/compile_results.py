#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,statistics
ROOT=Path(__file__).resolve().parent
files=list((ROOT/'results').rglob('*.json'))
valid=[]; invalid=[]
for p in files:
    try:
        d=json.loads(p.read_text())
        if 'roundLog' in d and 'scenarioId' in d and 'seed' in d: valid.append((p,d))
    except Exception as e: invalid.append((p,str(e)))
by={}
for p,d in valid: by.setdefault(d['scenarioId'],[]).append(d)
lines=['# Pack 06 Dice-Level Combat Report','',f'Valid complete result files: {len(valid)}',f'Invalid JSON files: {len(invalid)}','']
for sid,rows in sorted(by.items()):
    outcomes={k:sum(r.get('outcome')==k for r in rows) for k in ['victory','retreat','defeat','timeout']}
    rounds=[int(r.get('rounds',0)) for r in rows]
    logs=sum(len(r.get('roundLog',[])) for r in rows)
    lookups=sum(int(r.get('rulesLookups',0)) for r in rows)
    illegal=sum(len(r.get('illegalAttempts',[])) for r in rows)
    lines += [f'## {sid}',f'- Seeds: {len(rows)}',f'- Outcomes: {outcomes}',f'- Median rounds: {statistics.median(rounds) if rounds else 0}',f'- Logged rounds: {logs}',f'- Rules lookups: {lookups}',f'- Illegal attempts: {illegal}','']
lines += ['## Evidence ruling','','Only results with frozen build hashes, fixture hashes, individual dice, and complete round logs may support numerical changes. Missing evidence must be listed rather than estimated.','']
(ROOT/'COMPILED_REPORT.md').write_text('\n'.join(lines))
print(ROOT/'COMPILED_REPORT.md')
