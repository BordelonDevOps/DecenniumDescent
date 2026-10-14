#!/usr/bin/env python3
from pathlib import Path
import json,csv,hashlib
HERE=Path(__file__).resolve();LAB=HERE.parent.parent
raw=[];bad=[]
for p in (LAB/'results').rglob('*'):
 if p.is_file() and p.suffix.lower() in {'.json','.csv'}:
  raw.append(p)
  if p.suffix.lower()=='.json':
   try:json.loads(p.read_text(encoding='utf-8'))
   except Exception as e:bad.append((str(p.relative_to(LAB)),str(e)))
pack_rows=[]
for p in sorted((LAB/'packs').glob('[0-9][0-9]-*')):
 files=list((p/'results').rglob('*')) if (p/'results').exists() else []
 pack_rows.append((p.name,len([x for x in files if x.is_file()]),(p/'COMPILED_REPORT.md').exists()))
lines=['# Decennium Descent V7.2 — AI Calibration Master Report','','## Evidence standard','','Only raw deterministic rolls, executable simulations, frozen fixtures, and auditable agent logs support numerical changes. AI narrative estimates are hypotheses only.','','## Executable result inventory','',f'- Machine-readable files: {len(raw)}',f'- Invalid JSON files: {len(bad)}','']
for p in raw: lines.append(f'- `{p.relative_to(LAB)}`')
lines+=['','## Agentic pack coverage','']
for name,n,report in pack_rows:lines.append(f'- **{name}:** {n} result files; compiled report {"present" if report else "missing"}')
lines+=['','## Required interpretation','','Cursor must add: confidence intervals, training/holdout comparison, class and persona findings, confirmed rules defects, suspected balance defects, proposed patches, rejected hypotheses, and a human-GM agenda.','','## Human validation boundary','','AI can stress arithmetic and procedures at scale. It cannot prove table fun, social interpretation, clarity under live conversation, emotional investment, or experienced-GM preparation burden.']
(LAB/'AI_CALIBRATION_MASTER_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
summary={'machineReadableFiles':len(raw),'invalidJson':bad,'packCount':len(pack_rows)};(LAB/'results'/'compilation_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2));raise SystemExit(1 if bad else 0)
