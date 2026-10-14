#!/usr/bin/env python3
from pathlib import Path
import json, os, sys

ROOT = Path(__file__).resolve().parent
PACK = ROOT.name
TITLE = {
  "11-expedition-attrition-monte-carlo": "Expedition Attrition Monte Carlo",
  "12-cargo-extraction-risk": "Cargo and Extraction Risk",
  "13-haven-economy-stress": "Haven Economy Stress",
  "14-seasonal-cycle-simulation": "Seasonal Cycle Simulation",
}.get(PACK, PACK)

def iter_json(root: Path):
    prefix = "\\\\?\\"
    walk_root = str(root.resolve())
    try:
        if not root.exists():
            return
    except OSError:
        pass
    for dirpath, _dirs, files in os.walk(prefix + walk_root):
        for name in files:
            if not name.endswith(".json"):
                continue
            fp = os.path.join(dirpath, name)
            yield fp

records=[]; errors=[]
for fp in iter_json(ROOT / "results"):
    try:
        with open(fp, encoding="utf-8") as f:
            records.append(json.load(f))
    except Exception as exc:
        errors.append((fp, str(exc)))

lines=[f"# {TITLE} — Compiled Report","",f"**Pack:** `{PACK}`",f"**Evidence:** Level A (executable Gameplay Loop v1.2 chassis)",f"**Canon:** No edits.", "",f"Raw JSON results: {len(records)}",f"Unreadable results: {len(errors)}",""]
by_scenario={}
for r in records:
    by_scenario.setdefault(r.get("scenarioId","UNKNOWN"),[]).append(r)
lines+=["## Scenario coverage",""]
for key,vals in sorted(by_scenario.items()):
    levels={str(v.get("evidenceLevel","?")) for v in vals}
    lines.append(f"- **{key}:** {len(vals)} results; evidence {', '.join(sorted(levels))}")

halts=[]; findings=[]
for r in records:
    halts.extend(r.get("rulesHalts") or [])
    findings.extend(r.get("findings") or [])

# unique halt codes
seen=set(); uniq_halts=[]
for h in halts:
    code=h.get("code") if isinstance(h,dict) else str(h)
    if code in seen: continue
    seen.add(code); uniq_halts.append(h)

lines+=["","## Rules halts","",f"Total instances: {len(halts)}; unique codes: {len(uniq_halts)}"]
for h in uniq_halts[:50]:
    if isinstance(h,dict):
        lines.append(f"- `{h.get('code')}`: {h.get('note',h)}")
    else:
        lines.append(f"- {h}")

# severity findings
lines+=["","## Findings","",f"Total: {len(findings)}"]
by_sev={"critical":[],"high":[],"medium":[],"info":[],"other":[]}
for item in findings:
    if not isinstance(item,dict):
        by_sev["other"].append(item); continue
    sev=str(item.get("severity","other")).lower()
    by_sev.setdefault(sev if sev in by_sev else "other", []).append(item)
for sev in ("critical","high","medium","info","other"):
    items=by_sev.get(sev) or []
    if not items: continue
    lines.append(f"### {sev} ({len(items)})")
    # unique claims
    seen_c=set()
    for item in items:
        claim=item.get("claim") if isinstance(item,dict) else str(item)
        if claim in seen_c: continue
        seen_c.add(claim)
        lines.append(f"- {claim}")

# metric rollups where present
lines+=["","## Metric highlights",""]
for key,vals in sorted(by_scenario.items()):
    mets=[v.get("metrics") or {} for v in vals if v.get("outcome")=="aggregated_monte_carlo"]
    if not mets: continue
    def avg(k):
        xs=[m[k] for m in mets if isinstance(m.get(k),(int,float))]
        return round(sum(xs)/len(xs),4) if xs else None
    bits=[]
    for k in ("havenRate","wipeRate","objectiveRate","cargoLossRate","meanRetainedLoadFrac","meanTrueProfit","lossRate","nontrivialExplorationRate","meanMapFidelity","complicationRate"):
        a=avg(k)
        if a is not None: bits.append(f"{k}={a}")
    if bits:
        lines.append(f"- **{key}** ({len(mets)} cells): " + "; ".join(bits[:8]))

if errors:
    lines+=["","## Parse errors",""]
    for p,e in errors[:20]:
        lines.append(f"- `{p}`: {e}")

lines+=["","## Evidence limitations","","Chassis proxies party Strength capacity, Quartermaster modifiers, and some settlement wages. Numerical change proposals require holdout corroboration and owner review. No canon was edited."]
(ROOT/"COMPILED_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Compiled {len(records)} results -> {ROOT/'COMPILED_REPORT.md'}")
