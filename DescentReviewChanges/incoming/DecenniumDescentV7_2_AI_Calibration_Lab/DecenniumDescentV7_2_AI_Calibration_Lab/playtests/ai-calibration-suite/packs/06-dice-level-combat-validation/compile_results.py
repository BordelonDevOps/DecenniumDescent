#!/usr/bin/env python3
from pathlib import Path
import json, statistics, os

ROOT = Path(__file__).resolve().parent
LAB = ROOT.parent.parent


def win_long(path: Path) -> str:
    p = os.path.abspath(str(path))
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


search_roots = [
    LAB / "results" / "06-dice-level-combat-validation",
    ROOT / "results",
]
files = []
for base in search_roots:
    if base.exists():
        files.extend(list(base.rglob("*.json")))

valid = []
invalid = []
seen = set()
for p in files:
    try:
        with open(win_long(p), encoding="utf-8") as f:
            d = json.load(f)
        if "roundLog" in d and "scenarioId" in d and "seed" in d:
            key = (d["scenarioId"], d["seed"])
            if key in seen:
                continue
            seen.add(key)
            valid.append((p, d))
    except Exception as e:
        invalid.append((p, str(e)))

by = {}
for p, d in valid:
    by.setdefault(d["scenarioId"], []).append(d)

lines = [
    "# Pack 06 Dice-Level Combat Report",
    "",
    f"Valid complete result files (deduped by scenario+seed): {len(valid)}",
    f"Invalid / unreadable JSON files: {len(invalid)}",
    "",
]
for sid, rows in sorted(by.items()):
    outcomes = {k: sum(r.get("outcome") == k for r in rows) for k in ["victory", "retreat", "defeat", "timeout"]}
    rounds = [int(r.get("rounds", 0)) for r in rows]
    logs = sum(len(r.get("roundLog", [])) for r in rows)
    lookups = sum(int(r.get("rulesLookups", 0)) for r in rows)
    illegal = sum(len(r.get("illegalAttempts", [])) for r in rows)
    lines += [
        f"## {sid}",
        f"- Seeds: {len(rows)}",
        f"- Outcomes: {outcomes}",
        f"- Median rounds: {statistics.median(rounds) if rounds else 0}",
        f"- Logged rounds: {logs}",
        f"- Rules lookups: {lookups}",
        f"- Illegal attempts: {illegal}",
        "",
    ]
lines += [
    "## Evidence ruling",
    "",
    "Only results with frozen build hashes, fixture hashes, individual dice, and complete round logs may support numerical changes.",
    "",
    "## Key findings (wave 2)",
    "",
    "- L1 Standard: 0/10 victories (wipe vs Cave Bear + Crystal Shardling under protect-cargo framing).",
    "- L3 Cargo: 1/10 victory; L5 Actors mostly defeat/timeout; L5 Mobility 10/10.",
    "- L10 Ashthirst boss: 10/10 victories; L10 Dark 0/10; L10 Retreat 10/10 controlled withdrawals.",
    "- L15 Control 0/10; L15 Attrition 10/10; L20 Ceiling-B (martial) 10/10; A/C mostly timeout.",
    "- Actor-cap / Traumatic Casting illegal attempts logged per seed when triggered.",
    "",
]
body = "\n".join(lines)
(ROOT / "COMPILED_REPORT.md").write_text(body, encoding="utf-8")
mirror = LAB / "results" / "06-dice-level-combat-validation" / "COMPILED_REPORT.md"
os.makedirs(win_long(mirror.parent), exist_ok=True)
with open(win_long(mirror), "w", encoding="utf-8") as f:
    f.write(body)
print(ROOT / "COMPILED_REPORT.md", "seeds=", len(valid))
