#!/usr/bin/env python3
from pathlib import Path
import json

HERE=Path(__file__).resolve()
LAB=HERE.parent.parent
packs=sorted((LAB/"packs").glob("[0-9][0-9]-*"))
lines=["# Decennium Descent V7.1 — AI Playtest Master Report","",
"**Status:** Automatically compiled evidence index. Cursor agents must complete interpretation sections.","",
"## Evidence policy","",
"Numerical tuning requires executable or roll-by-roll evidence. Agentic findings may support rules-clarity and usability changes but do not alone prove balance.",""]
total_json=0
suite_json=list((LAB/"results").glob("**/*.json"))
total_json+=len(suite_json)
rules_halts=[]
findings=[]
coverage=[]
for p in suite_json:
    try:
        d=json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    if isinstance(d,dict):
        rules_halts.extend(d.get("rulesHalts",[]))
        findings.extend(d.get("findings",[]))
for pack in packs:
    report=pack/"COMPILED_REPORT.md"
    json_files=list(pack.glob("results/**/*.json"))
    total_json+=len(json_files)
    coverage.append((pack.name,len(json_files),report.exists()))
    for p in json_files:
        try:
            d=json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d,dict):
            rules_halts.extend(d.get("rulesHalts",[]))
            findings.extend(d.get("findings",[]))
lines+=["## Pack coverage",""]
for name,n,has in coverage:
    lines.append(f"- **{name}:** {n} raw JSON results; compiled report {'present' if has else 'missing'}")
lines+=["","## Totals","",f"- Raw JSON result files: {total_json}",f"- Rules halts: {len(rules_halts)}",f"- Finding records: {len(findings)}",""]
baseline=LAB/"results"/"00-baseline-simulations"/"summary.json"
if baseline.exists():
    lines+=["## Baseline simulations","",f"```json\n{baseline.read_text(encoding='utf-8')}\n```",""]
lines+=["## Rules halts",""]
for item in rules_halts[:250]: lines.append(f"- {item}")
lines+=["","## Consolidated findings",""]
for item in findings[:500]: lines.append(f"- {item}")
lines+=["","## Required human follow-up","",
"- Confirm turn speed and cognitive load with real players.",
"- Confirm Director preparation burden with an experienced GM.",
"- Test emotional engagement, table communication, and fun.",
"- Treat AI-generated tactical competence as a stress condition, not a prediction of ordinary players.","",
"## Cursor completion instructions","",
"Replace this section with a ranked defect list, confidence level, source evidence, proposed patch scope, and exact human playtest agenda."]
(LAB/"AI_PLAYTEST_MASTER_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Compiled {len(packs)} packs and {total_json} JSON files")
