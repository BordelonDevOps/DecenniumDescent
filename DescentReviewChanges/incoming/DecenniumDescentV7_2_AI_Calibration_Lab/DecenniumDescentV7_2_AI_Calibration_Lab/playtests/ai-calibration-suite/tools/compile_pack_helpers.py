#!/usr/bin/env python3
"""Compile pack results with Windows MAX_PATH-safe reads; prefer short suite paths."""
from __future__ import annotations

import json
import os
from pathlib import Path


def win_long(path: Path) -> str:
    p = os.path.abspath(str(path))
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


def load_json(path: Path):
    try:
        with open(win_long(path), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def gather(search_roots):
    records = []
    errors = []
    seen = set()
    for base in search_roots:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.json")):
            key = path.name + "|" + path.parent.name
            if key in seen:
                continue
            data = load_json(path)
            if data is None:
                errors.append((str(path), "unreadable"))
                continue
            if not (isinstance(data, dict) and data.get("scenarioId")):
                continue
            seen.add(key)
            records.append(data)
    return records, errors


def write_report(root: Path, lab: Path, title: str, pack_slug: str, records, errors, extra_lines=None):
    lines = [f"# {title}", "", f"Raw JSON results: {len(records)}", f"Unreadable skipped: {len(errors)}", ""]
    by_scenario = {}
    for r in records:
        by_scenario.setdefault(r.get("scenarioId", "UNKNOWN"), []).append(r)
    lines += ["## Scenario coverage", ""]
    for key, vals in sorted(by_scenario.items()):
        levels = {v.get("evidenceLevel", "?") for v in vals}
        outcome = vals[0].get("outcome", "?") if vals else "?"
        lines.append(f"- **{key}:** {len(vals)} results; evidence {', '.join(sorted(levels))}; outcome {outcome}")
    halts = []
    findings = []
    for r in records:
        halts.extend(r.get("rulesHalts", []) or [])
        findings.extend(r.get("findings", []) or [])
    lines += ["", "## Rules halts", "", f"Total: {len(halts)}"]
    for h in halts[:100]:
        lines.append(f"- {h}")
    lines += ["", "## Findings", "", f"Total: {len(findings)}"]
    for item in findings[:200]:
        if isinstance(item, dict):
            lines.append(f"- [{item.get('severity','?')}] {item.get('type', item.get('summary', item))}")
        else:
            lines.append(f"- {item}")
    if extra_lines:
        lines += ["", "## Wave summary", ""] + extra_lines
    if errors:
        lines += ["", "## Unreadable paths (skipped; short-path twins used when available)", ""]
        for p, e in errors[:20]:
            lines.append(f"- `{p}`: {e}")
    body = "\n".join(lines) + "\n"
    (root / "COMPILED_REPORT.md").write_text(body, encoding="utf-8")
    mirror = lab / "results" / pack_slug / "COMPILED_REPORT.md"
    os.makedirs(win_long(mirror.parent), exist_ok=True)
    with open(win_long(mirror), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"Compiled {len(records)} results -> {root / 'COMPILED_REPORT.md'}")


if __name__ == "__main__":
    raise SystemExit("import helpers only")
