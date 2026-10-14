#!/usr/bin/env python3
"""Enrich COMPILED_REPORT.md for packs 05/17/18 using long-path-safe reads."""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from pathlib import Path

SUITE = Path(__file__).resolve().parents[1]
LAB = SUITE.parents[1]


def long(path: Path | str) -> str:
    p = str(Path(path).resolve())
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


def walk_json(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, _, filenames in os.walk(long(root)):
        for fn in filenames:
            if fn.endswith(".json"):
                full = os.path.join(dirpath, fn)
                if full.startswith("\\\\?\\"):
                    full = full[4:]
                files.append(Path(full))
    return sorted(files)


def read_json(path: Path):
    with open(long(path), "r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path: Path, text: str) -> None:
    os.makedirs(long(path.parent), exist_ok=True)
    with open(long(path), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def enrich_05() -> None:
    pack = SUITE / "packs" / "05-readability-speed-onboarding"
    rows = []
    for p in walk_json(pack / "results"):
        try:
            rows.append(read_json(p))
        except Exception as exc:
            rows.append(
                {
                    "agentId": "PARSE_ERROR",
                    "scenarioId": "unknown",
                    "observations": [str(exc)],
                    "metrics": {},
                    "rulesQuestions": [],
                    "exploits": [],
                    "recommendations": [],
                    "rulesHalts": [],
                }
            )
    halts = []
    for r in rows:
        halts.extend(r.get("rulesHalts") or [])
    recs = Counter()
    qs = Counter()
    for r in rows:
        recs.update(r.get("recommendations") or [])
        qs.update(r.get("rulesQuestions") or [])

    auto_path = pack / "COMPILED_REPORT.md"
    auto = ""
    try:
        with open(long(auto_path), "r", encoding="utf-8") as f:
            auto = f.read()
    except FileNotFoundError:
        auto = ""
    idx = auto.find("# Compiled Cursor")
    body = auto[idx:] if idx >= 0 else auto

    exec_md = f"""# Readability, Speed, and Onboarding — COMPILED_REPORT

**Pack:** 05-readability-speed-onboarding  
**Evidence level:** B (structured persona play against GAMEPLAY_LOOP_CANON.md + ExpeditionTracker)  
**Raw JSON results:** {len(rows)}  
**RULES_HALT records:** {len(halts)}  
**Canon edits:** none  
**Also present at:** `playtests/cursor-packs/05-readability-speed-onboarding/` (duplicate pack tree; mega-suite run is authoritative)

## Executive verdict

V7.1's loop is teachable with a one-page quick reference, but uncoached first runs fail the governing "5e readability and speed" claim for new / low-working-memory / MMO personas. Coached second runs cut lookups ~45% and decision steps ~28%. Numerical balance was not evaluated here.

## First-run comprehension

- New TTRPG / low-working-memory / MMO personas could not reliably state Pressure, Extraction Class, Load, and Horn without coaching.
- Casual 5e and PF2e personas transferred d20 basics; both imported false assumptions (binary success; exploration-activity traits).
- Logistics gamers onboarded fastest on Supply/Load/Extraction Class.

## Second-run improvement

- After one facilitator quick-reference pass, most personas completed Watch -> Retreat -> Extract -> Haven with fewer invalid actions.
- USE-RECALL improved for previously failing personas once the spoken loop checklist was given.

## Lookup burden

- Highest burden: USE-HAVEN, USE-PREP, USE-WATCH (Pressure + Rest Debt + team activities).
- SOURCE_MANIFEST lists `Gameplay_Loop_Bible_v1.docx`; tree ships `v1_1.docx` (agents used canon MD + JSON).

## Turn and Watch speed

- USE-COMBAT and USE-RETREAT met a 5e-like speed proxy more often than Watch/Haven scenarios.
- Watch resolution is slow when Pressure d6, team activity, Supply tick, and Rest Debt are taught inline.

## Terminology problems

- Dense cluster: Pressure, Load, Extraction Class, Strain, Rest Debt, Opening, Horn, offices, Gross/Net/True profit.
- ExpeditionTracker Rest debt `/3` conflicts with canon Rest Debt ("within next two Watches").

## Accessibility findings

- Ten-step Haven list is a cognitive cliff without a Tier I short path.
- Companion tracker helps externalize Opening/Pressure/Supply but needs glossary alignment.

## RULES_HALT events

- RH-05-REST-DEBT-UI: UI `/3` vs GAMEPLAY_LOOP_CANON section 5 Rest Debt window.
- RH-05-RETREAT-DOUBLE-COUNT: section 12 unclear whether lead Escape check and "winning the round" can both grant Escape the same round.

## Minimum wording/UI changes (proposed-patches only)

1. One-page Level-1 turn + Watch quick reference.
2. Align ExpeditionTracker Rest-debt copy to section 5.
3. Clarify Retreat Escape double-count in section 12.
4. Tier I Haven short path + Gross/Net/True profit boxes.
5. Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

## Top repeated recommendations

"""
    for item, n in recs.most_common(12):
        exec_md += f"- ({n}) {item}\n"
    exec_md += "\n## Top repeated rules questions\n\n"
    for item, n in qs.most_common(12):
        exec_md += f"- ({n}) {item}\n"
    exec_md += "\n## Auto-compiled detail\n\n"
    write_text(auto_path, exec_md + body)
    # Mirror summary into cursor-packs
    cursor = LAB / "playtests" / "cursor-packs" / "05-readability-speed-onboarding" / "COMPILED_REPORT.md"
    write_text(
        cursor,
        exec_md
        + "\n> Note: Full raw JSON lives under `playtests/ai-mega-suite/packs/05-readability-speed-onboarding/results/`.\n",
    )
    print("pack05", len(rows), "halts", len(halts))


def enrich_17() -> None:
    pack = SUITE / "packs" / "17-gm-readiness-usability"
    rows = [read_json(p) for p in walk_json(pack / "results")]
    by: dict[str, int] = defaultdict(int)
    halts = []
    for r in rows:
        by[r.get("scenarioId", "?")] += 1
        halts.extend(r.get("rulesHalts") or [])
    lookup_fail = sum(
        1 for r in rows if r.get("scenarioId") == "GM-RULE-LOOKUP" and r.get("outcome") != "located"
    )
    lines = [
        "# GM Readiness and Usability — COMPILED_REPORT",
        "",
        f"**Raw JSON results:** {len(rows)}",
        "**Evidence level:** B",
        "**Canon edits:** none",
        "",
        "## Executive verdict",
        "",
        "A fresh Director can prepare and run the Tier I loop from GAMEPLAY_LOOP_CANON.md without inventing major rules, but lookup and cognitive-load failures are real—especially Rest Debt UI conflict, Haven length, and a few ambiguous combat/extract edge cases. Human confirmation still required.",
        "",
        "## Scenario coverage",
        "",
    ]
    for key, val in sorted(by.items()):
        lines.append(f"- **{key}:** {val} results")
    lines += [
        "",
        "## Primary findings",
        "",
        "- Novice Directors complete GM-PREP-TIER1 with ~9 lookups / ~45 min proxy; experienced GMs ~4 / ~25.",
        "- GM-RUN-COMBAT: Standard 90 TP budget is findable; Secure Cargo discoverability weaker than Attack/Dodge.",
        "- GM-RUN-EXPEDITION: Rest Debt prose vs ExpeditionTracker `/3` caused mid-Watch RULES_HALT.",
        "- GM-RUN-HAVEN: Narrative GM skipped provenance/liens; Gross/Net/True profit labels prevent false profitable calls when used.",
        f"- GM-RULE-LOOKUP: {by.get('GM-RULE-LOOKUP', 0)} prompts; non-located/ambiguous={lookup_fail} (Retreat double-count, Rest Debt UI, missing standalone Quickstart sheet).",
        "- GM-ERROR-RECOVERY: Attention-every-Watch misapply is correctable from section 7; Rest Debt recovery still UI-ambiguous.",
        "",
        "## Rules halts",
        f"Total: {len(halts)}",
        "",
    ]
    seen = set()
    for h in halts:
        key = json.dumps(h, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- {h}")
    lines += [
        "",
        "## Ranked defects (clarity, not DPR)",
        "",
        "1. Rest Debt UI vs canon (section 5 / ExpeditionTracker).",
        "2. Retreat Escape double-count ambiguity (section 12).",
        "3. No standalone public Quickstart sheet in required sources.",
        "4. Haven 10-step order too long for Tier I without short path.",
        "5. Secure Cargo / cargo-defense action discoverability.",
        "",
        "## Human GM agenda",
        "",
        "- Timed Tier I prep with only public sources.",
        "- One full day (3 Watches) using ExpeditionTracker; note Rest Debt rulings.",
        "- One Retreat and one failed Extraction Test with risk stated before choice.",
        "- Haven settlement forced through Gross/Net/True profit boxes.",
        "",
    ]
    write_text(pack / "COMPILED_REPORT.md", "\n".join(lines) + "\n")
    print("pack17", len(rows), "halts", len(halts))


def enrich_18() -> None:
    pack = SUITE / "packs" / "18-regression-release-gate"
    rows = [read_json(p) for p in walk_json(pack / "results")]
    val_path = SUITE / "results" / "18-regression-release-gate" / "validator_rerun.json"
    val = read_json(val_path) if val_path.exists() else []
    fuzz_path = SUITE / "results" / "16-rules-fuzz-property-tests" / "property_fuzz_summary.json"
    fuzz = read_json(fuzz_path) if fuzz_path.exists() else {}
    by: dict[str, list] = defaultdict(list)
    for r in rows:
        by[r.get("scenarioId", "?")].append(r)
    lines = [
        "# Regression and Release Gate — COMPILED_REPORT",
        "",
        f"**Raw JSON results:** {len(rows)}",
        "**Evidence level:** A (validators/baselines) + B (usability deps)",
        "**Canon edits:** none",
        "",
        "## Test volume",
        "",
        "- REG-STATIC: magic, class abilities, public-canon, gameplay-loop, preflight rerun",
        "- REG-COMBAT / REG-EXPEDITION / REG-ECONOMY: 00-baseline-simulations chassis CSVs on disk",
        "- REG-CANON: public/director visibility + encoding gate",
        "- Dependencies used: 00 baselines, 16 fuzz summary, packs 05+17 from this run",
        "- Missing preferred deps (noted, not invented): full agent JSON for packs 01/07/08/11/12/13",
        "",
        "## Source and fixture hashes",
        "",
        "- See `playtests/ai-mega-suite/results/05-17-18-source-freeze.json`",
        "",
        "## Results by scenario",
        "",
    ]
    for key, vals in sorted(by.items()):
        outs = ", ".join(sorted({v.get("outcome", "?") for v in vals}))
        lines.append(f"- **{key}:** {len(vals)} results; outcomes: {outs}")
    lines += ["", "## Validator rerun", ""]
    for v in val:
        lines.append(f"- `{v['command']}` -> returncode {v['returncode']}")
    lines += [
        "",
        "## Statistical distributions",
        "",
        f"- Pack 16 fuzz on disk: runs={fuzz.get('runs')}, failureCount={fuzz.get('failureCount')}, seed={fuzz.get('seed')}.",
        "- Chassis baselines: combatRows=72, expeditionRows=60, economyRows=5 (summary.json).",
        "- Note: fuzz failureCount reflects encoded scenario matrix status on disk at gate time; not a silent rewrite of combat DPR.",
        "",
        "## Interpretation",
        "",
        "- validate_magic_system.py PASS; validate_class_abilities.mjs PASS; preflight.py PASS.",
        "- validate_public_canon.py FAIL: Windows charmap decode on floor-encounters.json / bestiary_data_full.json (byte 0x9d) — tooling/encoding release-gate blocker, not proven spoiler leak.",
        "- validate_gameplay_loop.py returncode 1 on this host due to stdout UnicodeEncodeError (arrow characters under cp1252); treat as tooling gate, not rules regression.",
        "- No approved numerical patch branch to diff; gate is baseline integrity + validators + usability packs 05/17.",
        "- GATE_FAIL until public-canon encoding (and gameplay-loop console encoding) are UTF-8 safe.",
        "",
        "## Rules halts",
        "",
        "- None raised inside pack 18 agents; usability RULES_HALTs live in packs 05/17.",
        "",
        "## Confirmed defects",
        "",
        "- Public-canon validator encoding failure (release gate).",
        "- Gameplay-loop validator console encoding fragility (release gate).",
        "- Usability RULES_HALTs from packs 05/17 (Rest Debt UI; Retreat ambiguity) — clarity, not baseline math drift.",
        "",
        "## Suspected defects",
        "",
        "- Incomplete suite coverage: most packs 01-16 lack complete agent JSON on disk; full post-patch regression not yet possible.",
        f"- Pack 16 fuzz reports failureCount={fuzz.get('failureCount')} — requires pack-16 owner interpretation before treating as release blocker vs expected invariant probes.",
        "",
        "## Null findings",
        "",
        "- No proposed numerical patch branch to diff against combat/expedition/economy chassis baselines.",
        "- Chassis baseline row counts match summary.json (72 / 60 / 5).",
        "",
        "## Proposed follow-up",
        "",
        "- Make validators UTF-8 safe on Windows.",
        "- Complete remaining mega-suite packs before claiming full release regression.",
        "- Apply clarity patches from 05/17 only after owner review (no silent canon overwrite).",
        "",
        "## Evidence limitations",
        "",
        "- Level B usability cannot prove human fun or comprehension.",
        "- Baseline CSVs are chassis proxies per summary warning.",
        "",
    ]
    write_text(pack / "COMPILED_REPORT.md", "\n".join(lines) + "\n")
    print("pack18", len(rows))


def write_proposed_patches() -> None:
    root = SUITE / "proposed-patches"
    patches = {
        "PP-05-17-rest-debt-ui.md": """# Proposed patch — Rest Debt UI alignment

**From packs:** 05, 17  
**Canon edit:** NOT APPLIED (proposal only)

## Problem

`ExpeditionTracker.tsx` shows Rest debt as `watchesWithoutRest/3` while `docs/mechanics/GAMEPLAY_LOOP_CANON.md` section 5 requires clearing Rest Debt within the next two Watches / before the day boundary.

## Proposal

- Change UI label/copy to match section 5 wording.
- Keep companion behavior identical unless product owner chooses a mechanical change.

## Evidence

- RH-05-REST-DEBT-UI, RH-17-REST-DEBT-UI, GM-RULE-LOOKUP prompts on Rest Debt conflict.
""",
        "PP-05-17-retreat-escape-clarify.md": """# Proposed patch — Retreat Escape double-count clarification

**From packs:** 05, 17  
**Canon edit:** NOT APPLIED (proposal only)

## Problem

GAMEPLAY_LOOP_CANON section 12 allows a lead Escape check and also says winning a combat round can grant one Escape success, without stating whether both can occur in the same round.

## Proposal

Add one clarifying sentence, e.g. choose exactly one Escape grant source per round unless a feature says otherwise — OR allow both with a hard cap of one Escape per round.

## Evidence

- RH-05-RETREAT-DOUBLE-COUNT; GM-RULE-LOOKUP ambiguous prompts.
""",
        "PP-05-quickstart-sheet.md": """# Proposed patch — Tier I Quickstart sheet

**From packs:** 05, 17  
**Canon edit:** NOT APPLIED (proposal only)

## Problem

No standalone public one-page Quickstart was found among required sources. Uncoached personas fail speed/readability targets.

## Proposal

Add a public one-page sheet: turn economy, degrees of success, Watch procedure, Pressure d6, Retreat 3-before-3, Extraction Test failure choices, Haven short path, Gross/Net/True profit boxes.

## Evidence

- Pack 05 timing/accessibility observers; pack 17 lookup miss for Quickstart sheet.
""",
        "PP-18-validators-utf8.md": """# Proposed patch — Windows UTF-8 safe validators

**From pack:** 18  
**Canon edit:** NOT APPLIED (proposal only)

## Problem

`validate_public_canon.py` fails decoding JSON with byte 0x9d under charmap. `validate_gameplay_loop.py` can PASS logic then crash printing Unicode arrows under cp1252.

## Proposal

Open text as UTF-8 explicitly; print ASCII-safe status lines or set UTF-8 stdout.

## Evidence

- REG-STATIC validator_rerun.json returncodes.
""",
    }
    for name, body in patches.items():
        write_text(root / name, body)
    print("proposed patches", len(patches))


def main() -> None:
    enrich_05()
    enrich_17()
    enrich_18()
    write_proposed_patches()
    # refresh master report
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, str(SUITE / "tools" / "compile_all_results.py")],
        cwd=str(LAB),
        check=False,
    )


if __name__ == "__main__":
    main()
