# Decennium Descent V7.1 — AI Playtest Lab

This workspace contains the V7.1 rules repository and one integrated multi-agent testing laboratory.

## Governing design rule

> Decennium Descent should have 5e’s readability and speed, Pathfinder 2e’s tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems.

## Open this folder in Cursor

Open the folder containing this file as the workspace root.

Then paste the complete contents of:

`playtests/ai-mega-suite/CURSOR_MASTER_ORCHESTRATOR_PROMPT.md`

into a new Cursor agent conversation.

## What the suite does

The suite separates two kinds of evidence:

1. **Deterministic and Monte Carlo tests** — useful for validating arithmetic, probabilities, resource curves, encounter budgets, cargo risk, market formulas, and regression.
2. **Agentic player simulations** — useful for finding unclear rules, dominant choices, exploit chains, role frustration, tactical dead ends, and gameplay-loop problems.

AI narration alone is not numerical evidence. All numerical recommendations must be backed by recorded dice, frozen fixtures, deterministic seeds, or executable simulation output.

## Safety and canon rules

- Do not directly edit canon while tests are running.
- Put suggested changes under `playtests/ai-mega-suite/proposed-patches/`.
- Public-player agents may not read Director-only files.
- Director-only tests must never write hidden information into public source.
- Preserve source hashes for every test run.
- A RULES_HALT must be recorded whenever the written rule cannot resolve an action.

## Recommended run order

1. Preflight and static validators.
2. Packs 07, 08, and 16 for mathematical and structural baselines.
3. Pack 06 for dice-level tactical combat.
4. Packs 09, 10, 15 for interaction and exploit stress.
5. Packs 11 and 12 for expedition and extraction.
6. Pack 13 for Haven economics.
7. Pack 14 for seasonal persistence.
8. Packs 05 and 17 for usability and GM readiness.
9. Pack 18 for final regression.
10. Compile all results.

## Key commands

Windows PowerShell:

```powershell
python playtests/ai-mega-suite/tools/preflight.py
python playtests/ai-mega-suite/tools/run_baseline_simulations.py
python playtests/ai-mega-suite/tools/compile_all_results.py
```

Cross-platform shell:

```bash
python playtests/ai-mega-suite/tools/preflight.py
python playtests/ai-mega-suite/tools/run_baseline_simulations.py
python playtests/ai-mega-suite/tools/compile_all_results.py
```

## Final output

Cursor must produce:

- `playtests/ai-mega-suite/AI_PLAYTEST_MASTER_REPORT.md`
- complete raw results under `playtests/ai-mega-suite/results/`
- a separate `playtests/ai-mega-suite/proposed-patches/` directory
- no silent canon edits
