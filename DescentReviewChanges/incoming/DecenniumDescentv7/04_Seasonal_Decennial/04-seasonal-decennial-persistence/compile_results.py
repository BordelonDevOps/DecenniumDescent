#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent
results = sorted((ROOT / "results").rglob("*.json"))
report = ROOT / "COMPILED_REPORT.md"
rows = []
for path in results:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append((path, data))
    except Exception as exc:
        rows.append((path, {"agentId":"PARSE_ERROR","scenarioId":"unknown","observations":[str(exc)],"metrics":{},"rulesQuestions":[],"exploits":[],"recommendations":[]}))

questions = Counter()
exploits = Counter()
recommendations = Counter()
by_scenario = defaultdict(list)
for path, data in rows:
    by_scenario[data.get("scenarioId","unknown")].append(data)
    questions.update(data.get("rulesQuestions",[]))
    exploits.update(data.get("exploits",[]))
    recommendations.update(data.get("recommendations",[]))

lines = ["# Compiled Cursor Multi-Agent Playtest Report", "", f"Result files: **{len(rows)}**", ""]
for scenario, entries in sorted(by_scenario.items()):
    lines += [f"## Scenario: {scenario}", ""]
    for entry in entries:
        lines += [f"### Agent: {entry.get('agentId','unknown')}", ""]
        metrics = entry.get("metrics",{})
        if metrics:
            lines.append("**Metrics**")
            for k,v in metrics.items(): lines.append(f"- {k}: {v}")
        for title, key in [("Observations","observations"),("Rules questions","rulesQuestions"),("Exploits","exploits"),("Recommendations","recommendations")]:
            vals = entry.get(key,[])
            if vals:
                lines.append(f"**{title}**")
                lines += [f"- {v}" for v in vals]
        lines.append("")

def top(counter, title):
    lines.extend([f"## {title}", ""])
    if not counter:
        lines.append("- None reported.")
    else:
        for item,count in counter.most_common(30): lines.append(f"- ({count}) {item}")
    lines.append("")

top(questions,"Repeated rules questions")
top(exploits,"Repeated exploit findings")
top(recommendations,"Repeated recommendations")
report.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(report)
