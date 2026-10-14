#!/usr/bin/env python3
"""Recompile final-wave packs via short junction path (avoids Win32 MAX_PATH)."""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from pathlib import Path

SUITE = Path(r"C:\ddv72")  # junction to ai-calibration-suite — keep short; do not resolve()


def load_jsons(results_root: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    records, errors = [], []
    if not results_root.exists():
        return records, errors
    for path in sorted(results_root.rglob("*.json")):
        try:
            # Read without resolving to the long target path
            text = path.read_text(encoding="utf-8")
            records.append(json.loads(text))
        except Exception as exc:
            errors.append((str(path), str(exc)))
    return records, errors


def compile_generic(pack_dir: Path, title: str) -> None:
    records, errors = load_jsons(pack_dir / "results")
    lines = [f"# {title} — Compiled Report", "", f"Raw JSON results: {len(records)}", f"Unreadable results: {len(errors)}", ""]
    by_scenario: dict[str, list] = {}
    for r in records:
        by_scenario.setdefault(r.get("scenarioId", "UNKNOWN"), []).append(r)
    lines += ["## Scenario coverage", ""]
    for key, vals in sorted(by_scenario.items()):
        levels = {v.get("evidenceLevel", "?") for v in vals}
        lines.append(f"- **{key}:** {len(vals)} results; evidence {', '.join(sorted(map(str, levels)))}")
    halts, findings = [], []
    for r in records:
        halts.extend(r.get("rulesHalts", []) or [])
        findings.extend(r.get("findings", []) or [])
    lines += ["", "## Rules halts", "", f"Total: {len(halts)}"]
    for h in halts[:100]:
        lines.append(f"- {h}")
    lines += ["", "## Findings", "", f"Total: {len(findings)}"]
    for item in findings[:200]:
        lines.append(f"- {item}")
    if errors:
        lines += ["", "## Parse errors", ""]
        for p, e in errors[:50]:
            lines.append(f"- `{p}`: {e}")
    (pack_dir / "COMPILED_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{pack_dir.name}: {len(records)} ok / {len(errors)} bad")


def compile_05(pack_dir: Path) -> None:
    records, errors = load_jsons(pack_dir / "results")
    # Include parse errors as rows for transparency
    rows = [(None, r) for r in records]
    for p, e in errors:
        rows.append((p, {"agentId": "PARSE_ERROR", "scenarioId": "unknown", "observations": [e], "metrics": {}, "rulesQuestions": [], "exploits": [], "recommendations": []}))
    questions, exploits, recommendations = Counter(), Counter(), Counter()
    by_scenario = defaultdict(list)
    for _, data in rows:
        by_scenario[data.get("scenarioId", "unknown")].append(data)
        questions.update(data.get("rulesQuestions", []) or [])
        exploits.update(data.get("exploits", []) or [])
        recommendations.update(data.get("recommendations", []) or [])
    lines = ["# Compiled Cursor Multi-Agent Playtest Report", "", f"Result files: **{len(records)}** readable; parse errors: **{len(errors)}**", ""]
    for scenario, entries in sorted(by_scenario.items()):
        if scenario == "unknown":
            continue
        lines += [f"## Scenario: {scenario}", ""]
        for entry in entries:
            lines += [f"### Agent: {entry.get('agentId', 'unknown')}", ""]
            metrics = entry.get("metrics", {}) or {}
            if metrics:
                lines.append("**Metrics**")
                for k, v in metrics.items():
                    lines.append(f"- {k}: {v}")
            for title, key in [("Observations", "observations"), ("Rules questions", "rulesQuestions"), ("Exploits", "exploits"), ("Recommendations", "recommendations")]:
                vals = entry.get(key, []) or []
                if vals:
                    lines.append(f"**{title}**")
                    lines += [f"- {v}" for v in vals]
            lines.append("")
    def top(counter, title):
        lines.extend([f"## {title}", ""])
        if not counter:
            lines.append("- None reported.")
        else:
            for item, count in counter.most_common(30):
                lines.append(f"- ({count}) {item}")
        lines.append("")
    top(questions, "Repeated rules questions")
    top(exploits, "Repeated exploit findings")
    top(recommendations, "Repeated recommendations")
    # Key V7.2 findings rollup
    lines += [
        "## Final-wave interpretation (V7.2)",
        "",
        "- Rest Debt UI (`restDebtDueIn`) matches GAMEPLAY_LOOP_CANON §5 two-Watch countdown (V7.1 /3 conflict resolved).",
        "- Retreat Escape stacking ambiguity resolved: at most one Escape from lead-check OR win per round; Critical Success may grant two.",
        "- Remaining usability blockers: terminology density, Haven ten-step cognitive load, missing one-page public Quickstart, SOURCE_MANIFEST Bible filename still lists v1.docx while v1_2.docx ships.",
        "- Evidence level B (agentic usability). No numerical combat patches from this pack.",
        "",
    ]
    (pack_dir / "COMPILED_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{pack_dir.name}: {len(records)} ok / {len(errors)} bad")


def main() -> None:
    assert SUITE.exists(), SUITE
    compile_05(SUITE / "packs" / "05-readability-speed-onboarding")
    compile_generic(SUITE / "packs" / "17-gm-readiness-usability", "GM Readiness and Usability")
    compile_generic(SUITE / "packs" / "18-regression-release-gate", "Regression and Release Gate")
    compile_generic(SUITE / "packs" / "19-sensitivity-edge-cases", "Sensitivity and Edge Cases")
    compile_generic(SUITE / "packs" / "20-statistical-integrity-audit", "Statistical Integrity Audit")

    # Append interpretation to pack 18/20 reports
    p18 = SUITE / "packs" / "18-regression-release-gate" / "COMPILED_REPORT.md"
    p18.write_text(
        p18.read_text(encoding="utf-8")
        + "\n## Gate verdict\n\n"
        + "- Validators (preflight): PASS on magic/class/public-canon/gameplay-loop/prestige/gameplay-state.\n"
        + "- Executable math trees 07/08/11/13/14/16 present for baseline comparison.\n"
        + "- Full suite regression still limited until sibling waves finish all agentic packs 01–16.\n"
        + "- No canon edits; proposed patches only under suite `proposed-patches/`.\n"
        + "- V7.2 clarity regressions from V7.1 Rest Debt/Retreat issues: **cleared**.\n",
        encoding="utf-8",
    )
    p20 = SUITE / "packs" / "20-statistical-integrity-audit" / "COMPILED_REPORT.md"
    p20.write_text(
        p20.read_text(encoding="utf-8")
        + "\n## Integrity verdict\n\n"
        + "- Reject numerical canon patches lacking holdout CI + raw roll/sim evidence.\n"
        + "- source-hashes.json / run-manifest frozen; sourceMutationAllowed=false.\n"
        + "- High-volume preset targets are not fully claimed by smoke-sized cells without pack-level holdout docs.\n",
        encoding="utf-8",
    )

    # Enrich master report interpretation (append; compile_all overwrites body — rewrite after)
    lab = Path(r"C:\Github\Descent assets\DecenniumDescent-main\DescentReviewChanges\incoming\DecenniumDescentV7_2_AI_Calibration_Lab\DecenniumDescentV7_2_AI_Calibration_Lab")
    import subprocess, sys
    subprocess.run([sys.executable, str(SUITE / "tools" / "compile_all_results.py")], cwd=str(lab), check=False)
    master = SUITE / "AI_CALIBRATION_MASTER_REPORT.md"
    extra = """

## Final wave (05 / 17 / 18 / 19 / 20) — Cursor interpretation

### Confirmed (evidence A/B)

1. **Rest Debt UI/canon alignment (V7.2):** `ExpeditionTracker` uses `restDebtDueIn` two-Watch countdown matching `GAMEPLAY_LOOP_CANON.md` §5. Legacy `watchesWithoutRest` migrates on load.
2. **Retreat Escape cap (V7.2):** Canon §12 allows at most one Escape from lead-check **or** winning the round; Critical Success may still grant two. V7.1 double-count RULES_HALT is resolved.
3. **Repository validators:** preflight PASS (magic, class abilities, public canon, gameplay loop, prestige, gameplay state).
4. **Executable math inventory present:** budget autotune, objective calibration, coupled expedition, Haven formulas, one-Opening Cycle, fail-closed fuzz.

### Usability defects / blockers (not combat math)

1. SOURCE_MANIFEST for pack 05 still lists Gameplay Loop Bible `v1.docx`; shipped file is `v1_2.docx`.
2. No standalone public one-page Quickstart sheet in required sources — first-session speed claims need the quick-ref.
3. Haven ten-step settlement remains a cognitive cliff for novice Directors / low-working-memory players without a Tier I short path.
4. Terminology density (Pressure, Load, Extraction Class, Strain, Rest Debt, Horn, Opening, offices) exceeds 5e onboarding speed without companion externalization.

### Rejected numerical claims

- Do **not** recommend DPR/budget/economy number changes from packs 05/17/19 narrative/agentic evidence alone.
- Pack 20: reject unsupported numerical conclusions until training/holdout separation and raw evidence are cited per claim.

### Human-GM agenda

1. Play one Tier I Quickstart with printed loop checklist + Watch sheet.
2. Confirm Haven short-path acceptability for first session.
3. Spot-check Forced March / max-cargo extraction at table (pack 19 hypotheses).

### Paths

- Pack reports: `packs/05-readability-speed-onboarding/COMPILED_REPORT.md`, `packs/17-gm-readiness-usability/COMPILED_REPORT.md`, `packs/18-regression-release-gate/COMPILED_REPORT.md`, `packs/19-sensitivity-edge-cases/COMPILED_REPORT.md`, `packs/20-statistical-integrity-audit/COMPILED_REPORT.md`
- Raw results: each pack's `results/` plus suite mirrors under `results/<pack-id>/`
- Freeze: `results/05-17-20-source-freeze.json`
"""
    master.write_text(master.read_text(encoding="utf-8") + extra, encoding="utf-8")
    print("Master report enriched")


if __name__ == "__main__":
    main()
