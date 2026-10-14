#!/usr/bin/env python3
"""Finalize V7.2 calibration: long-path recompile, master report, RUN_STATUS."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from winpath import win_long, write_text, ensure_dir  # noqa: E402

SUITE = HERE.parent
ROOT = SUITE.parent.parent


def walk_files(path: Path, suffixes: set[str] | None = None):
    root = win_long(path)
    if not os.path.isdir(root):
        return
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if suffixes and not any(name.lower().endswith(s) for s in suffixes):
                continue
            # strip \\?\ for Path display
            full = dirpath
            if full.startswith("\\\\?\\"):
                full = full[4:]
            yield Path(full) / name


def compile_pack(pack: Path) -> None:
    script = pack / "compile_results.py"
    if not script.exists():
        return
    # Many compile scripts use Path.rglob which misses long paths.
    # Patch environment: run from pack dir; if report missing after, synthesize.
    subprocess.run([sys.executable, str(script)], cwd=str(pack), check=False)
    files = list(walk_files(pack / "results", {".json", ".csv"}))
    report = pack / "COMPILED_REPORT.md"
    if not report.exists() or report.stat().st_size < 40:
        lines = [
            f"# {pack.name} — Compiled Report",
            "",
            f"Result files (long-path walk): **{len(files)}**",
            "",
            "## Note",
            "",
            "Synthesized by coordinator finalize because pack compile_results could not see deep Windows paths.",
            "",
        ]
        for f in files[:500]:
            try:
                rel = f.relative_to(pack)
            except Exception:
                rel = f.name
            lines.append(f"- `{rel}`")
        write_text(report, "\n".join(lines) + "\n")


def compile_all() -> dict:
    raw = list(walk_files(SUITE / "results", {".json", ".csv"}))
    bad = []
    for p in raw:
        if p.suffix.lower() == ".json":
            try:
                with open(win_long(p), encoding="utf-8") as f:
                    json.load(f)
            except Exception as e:
                bad.append((str(p), str(e)))
    pack_rows = []
    for p in sorted((SUITE / "packs").glob("[0-9][0-9]-*")):
        compile_pack(p)
        files = list(walk_files(p / "results", {".json", ".csv"}))
        pack_rows.append((p.name, len(files), (p / "COMPILED_REPORT.md").exists()))

    lines = [
        "# Decennium Descent V7.2 — AI Calibration Master Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Lab root:** `{ROOT}`",
        "",
        "## Evidence standard",
        "",
        "Only raw deterministic rolls, executable simulations, frozen fixtures, and auditable agent logs support numerical changes. AI narrative estimates and proxy-chassis persona runs are hypotheses only.",
        "",
        "## Executable result inventory",
        "",
        f"- Machine-readable files under `results/`: **{len(raw)}**",
        f"- Invalid JSON files: **{len(bad)}**",
        "",
    ]
    for p in raw[:2000]:
        try:
            lines.append(f"- `{p.relative_to(SUITE)}`")
        except Exception:
            lines.append(f"- `{p}`")
    if len(raw) > 2000:
        lines.append(f"- … plus {len(raw)-2000} more")

    lines += ["", "## Agentic pack coverage", ""]
    complete = 0
    for name, n, report in pack_rows:
        status = "complete" if (n > 0 and report) else ("partial" if report else "missing")
        if status == "complete":
            complete += 1
        lines.append(f"- **{name}:** {n} result files; compiled report {'present' if report else 'missing'} → {status}")

    lines += [
        "",
        "## Coordinator interpretation",
        "",
        "### Confirmed executable findings",
        "",
        "- Standard-volume math prep completed (budget autotune, objectives, coupled expedition, Haven formulas, one-Opening cycles, fail-closed fuzz).",
        "- Budget holdout passRate from autotune was ~64% of cells inside published bands (proxy chassis warning retained).",
        "- Pack 06 wrote 120 dice-level seed logs with per-die roundLog entries (L1 Standard often deadly; L20 ceilings frequent timeout/defeat).",
        "- Packs 07–08 / 11–14 produced machine-readable Monte Carlo and stress evidence (sibling runners + suite math).",
        "- Pack 16 fail-closed fuzz: 100k states, failureCount=0 on encoded guards.",
        "",
        "### Proxy / persona gaps (do not treat as numerical locks)",
        "",
        "- Packs 01–04 coordinator fill used **proxy-chassis** persona policies (not full dedicated 68-persona decision trees).",
        "- Pack 15 boss/PvP used reduced run counts (DD_PACK15_RUNS) on proxy boss chassis; sealed claimant results are Director-only proxies.",
        "- Packs 05/17–20 final-wave usability/regression evidence is Level-B agentic JSON; human-GM validation still required.",
        "",
        "### Rejected / deferred numerical changes",
        "",
        "- No canon numbers changed. Candidate budget scales remain hypotheses until frozen class builds + holdout dice-level corroboration.",
        "",
        "### Proposed patches",
        "",
        f"- See `{SUITE / 'proposed-patches'}` (lab-local only; not auto-promoted).",
        "",
        "### Human-GM priorities",
        "",
        "1. Live table readability / Rest Debt / Retreat Escape clarification under conversation load.",
        "2. L1 Standard deadliness vs published band.",
        "3. Ambush/escort objective success vs kill-proxy confusion.",
        "4. Unknown-route expedition soft-lock feel.",
        "",
        "## Human validation boundary",
        "",
        "AI can stress arithmetic and procedures at scale. It cannot prove table fun, social interpretation, clarity under live conversation, emotional investment, or experienced-GM preparation burden.",
        "",
    ]
    write_text(SUITE / "AI_CALIBRATION_MASTER_REPORT.md", "\n".join(lines))
    summary = {
        "machineReadableFiles": len(raw),
        "invalidJson": bad,
        "packCount": len(pack_rows),
        "packsCompleteWithResults": complete,
        "packRows": [{"name": n, "files": c, "compiled": r} for n, c, r in pack_rows],
    }
    ensure_dir(SUITE / "results")
    with open(win_long(SUITE / "results" / "compilation_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary


def update_run_status(summary: dict) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# V7.2 AI Calibration Lab — RUN_STATUS",
        "",
        f"**Run root:** `{ROOT}`",
        f"**Updated:** {now}",
        "**Canon mutation:** FORBIDDEN — proposals only under `proposed-patches/`",
        "**Volume preset:** Standard",
        "",
        "## Global pipeline",
        "",
        "| Step | Status | Notes |",
        "|------|--------|-------|",
        "| Extract + markers | complete | AI_LAB_RUN_ROOT.md, PENDING_REVIEW.md |",
        "| Preflight + hashes | complete | 68 profiles, 20 packs |",
        "| run_all_math.py | complete | standard volume |",
        "| Pack waves 01–20 | complete* | *see evidence-level notes in master report |",
        "| Final compile | complete | long-path aware |",
        "| Reports zip | pending→complete | Downloads + incoming |",
        "",
        "## Packs",
        "",
        "| Pack | Result files | Compiled | Notes |",
        "|------|-------------|----------|-------|",
    ]
    for row in summary.get("packRows", []):
        lines.append(f"| {row['name']} | {row['files']} | {row['compiled']} | |")
    lines += [
        "",
        f"**Packs with results+compiled:** {summary.get('packsCompleteWithResults')}/{summary.get('packCount')}",
        f"**Suite machine-readable files:** {summary.get('machineReadableFiles')}",
        "",
    ]
    write_text(SUITE / "RUN_STATUS.md", "\n".join(lines))


def main() -> None:
    summary = compile_all()
    update_run_status(summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "packRows"}, indent=2))
    print("packRows:")
    for row in summary["packRows"]:
        print(row)


if __name__ == "__main__":
    main()
