#!/usr/bin/env python3
from pathlib import Path
import json, sys

HERE=Path(__file__).resolve()
LAB=HERE.parent.parent
errors=[]
count=0
for p in LAB.glob("results/**/*.json"):
    try:
        data=json.loads(p.read_text(encoding="utf-8"))
        count+=1
        if p.name.endswith("summary.json") or p.name=="results.json":
            continue
        if isinstance(data,dict) and "scenarioId" in data:
            for key in ["scenarioId","evidenceLevel","outcome"]:
                if key not in data: errors.append(f"{p}: missing {key}")
    except Exception as exc:
        errors.append(f"{p}: {exc}")
print(f"Validated {count} JSON files")
for e in errors: print(e,file=sys.stderr)
sys.exit(1 if errors else 0)
