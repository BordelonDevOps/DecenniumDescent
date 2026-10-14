#!/usr/bin/env python3
from pathlib import Path
import json, statistics, csv

ROOT = Path(__file__).resolve().parent
files = sorted(ROOT.glob("results/**/*.json"))
records=[]
errors=[]
for path in files:
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    records.append(item)
                else:
                    errors.append((str(path), f"non-object list item: {type(item).__name__}"))
        elif isinstance(data, dict):
            records.append(data)
        else:
            errors.append((str(path), f"unsupported JSON root: {type(data).__name__}"))
    except Exception as exc:
        errors.append((str(path),str(exc)))

lines=["# Rules Fuzz and Property Tests — Compiled Report","",f"Raw JSON results: {len(records)}",f"Unreadable results: {len(errors)}",""]
by_scenario={}
for r in records:
    by_scenario.setdefault(r.get("scenarioId","UNKNOWN"),[]).append(r)
lines+=["## Scenario coverage",""]
for key,vals in sorted(by_scenario.items()):
    levels={v.get("evidenceLevel","?") for v in vals}
    lines.append(f"- **{key}:** {len(vals)} results; evidence {', '.join(sorted(levels))}")
halts=[]
findings=[]
for r in records:
    halts.extend(r.get("rulesHalts",[]))
    findings.extend(r.get("findings",[]))
lines+=["","## Rules halts","",f"Total: {len(halts)}"]
for h in halts[:100]:
    lines.append(f"- {h}")
lines+=["","## Findings","",f"Total: {len(findings)}"]
for item in findings[:200]:
    lines.append(f"- {item}")
if errors:
    lines+=["","## Parse errors",""]
    for p,e in errors:
        lines.append(f"- `{p}`: {e}")
(ROOT/"COMPILED_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Compiled {len(records)} results")
