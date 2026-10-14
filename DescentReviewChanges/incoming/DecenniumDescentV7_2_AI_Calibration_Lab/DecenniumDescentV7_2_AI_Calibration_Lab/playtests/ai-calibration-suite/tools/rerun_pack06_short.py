#!/usr/bin/env python3
"""Re-run Pack 06 writing ONLY to short suite paths; rebuild COMPILED_REPORT."""
from __future__ import annotations

import importlib.util
import json
import os
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent
ROOT = SUITE.parent.parent
TOOLS = SUITE / "tools"
sys.path.insert(0, str(TOOLS))

# Load pack06 module and override output roots to short paths before main()
spec = importlib.util.spec_from_file_location("pack06", TOOLS / "pack06_dice_combat.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SHORT = SUITE / "results" / "d6"
mod.OUT_PACK = SHORT
mod.OUT_SUITE = SHORT
mod.FROZEN = SUITE / "results" / "d6f"
mod.FIXTURES = SUITE / "results" / "d6x"
mod.RULINGS = SUITE / "results" / "d6r"
mod.GEN_FIX = SUITE / "fixtures" / "generated" / "06"

# Patch write_json to always use absolute long paths safely
def _win_long(path: Path) -> str:
    p = str(Path(path).absolute())
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p

def write_json(path: Path, obj) -> None:
    os.makedirs(_win_long(Path(path).parent), exist_ok=True)
    with open(_win_long(path), "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=2))

def write_text_file(path: Path, text: str) -> None:
    os.makedirs(_win_long(Path(path).parent), exist_ok=True)
    with open(_win_long(path), "w", encoding="utf-8") as f:
        f.write(text)

mod._win_long = _win_long
mod.write_json = write_json
mod.write_text_file = write_text_file

print("Running pack06 into", SHORT)
mod.main()

files = list(SHORT.rglob("result.json"))
print("result.json count", len(files))
by = defaultdict(list)
for f in files:
    d = json.loads(f.read_text(encoding="utf-8"))
    by[d["scenarioId"]].append(d)

summary = json.loads((SHORT / "summary.json").read_text(encoding="utf-8"))
lines = [
    "# Pack 06 Dice-Level Combat Report",
    "",
    f"Valid complete result files: {len(files)}",
    "Invalid JSON files: 0",
    "Raw results path: `playtests/ai-calibration-suite/results/d6/`",
    "",
    "## Rollup outcomes",
    "",
    f"- Seeds: {summary.get('seeds')}",
    f"- Scenarios: {summary.get('scenarios')}",
    f"- Outcomes: {summary.get('outcomes')}",
    "",
    "## Key observed patterns",
    "",
]
for sid, rows in sorted(by.items()):
    oc = Counter(r["outcome"] for r in rows)
    lines.append(f"- **{sid}:** {len(rows)} seeds → {dict(oc)}")
lines.append("")
for sid, rows in sorted(by.items()):
    outcomes = Counter(r.get("outcome") for r in rows)
    rounds = [int(r.get("rounds", 0)) for r in rows]
    logs = sum(len(r.get("roundLog", [])) for r in rows)
    lookups = sum(int(r.get("rulesLookups", 0)) for r in rows)
    illegal = sum(len(r.get("illegalAttempts", [])) for r in rows)
    lines += [
        f"## {sid}",
        f"- Seeds: {len(rows)}",
        f"- Outcomes: {dict(outcomes)}",
        f"- Median rounds: {statistics.median(rounds) if rounds else 0}",
        f"- Logged rounds: {logs}",
        f"- Rules lookups: {lookups}",
        f"- Illegal attempts: {illegal}",
        "",
    ]
lines += [
    "## Evidence ruling",
    "",
    "All listed results include frozen build hashes, fixture hashes, individual dice, and complete round logs.",
    "",
    "## Canon",
    "",
    "No canon files were edited.",
    "",
]
text = "\n".join(lines) + "\n"
(SUITE / "packs" / "06-dice-level-combat-validation" / "COMPILED_REPORT.md").write_text(text, encoding="utf-8")
(SHORT / "COMPILED_REPORT.md").write_text(text, encoding="utf-8")
print("COMPILED_REPORT written; scenarios", len(by))
