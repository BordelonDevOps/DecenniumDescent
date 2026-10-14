# Seasonal and Decennial Persistence Pack

## Purpose

This pack covers the gameplay function that cannot be completed through authorship alone: **end-of-Opening records, ten-year change, Haven persistence, map value, economic shocks, heirs, institutions, and repeat-campaign incentives**.

The written rules are canonical. This pack tests whether the numbers, timing, clarity, incentives, and edge cases work in repeated play.

## Required repository

Run from the root of **DecenniumDescent V7 Gameplay Complete**. Read first:

1. `AGENTS.md`
2. `CANON_MANIFEST.json`
3. `docs/mechanics/DESIGN_DOCTRINE.md`
4. `docs/mechanics/GAMEPLAY_LOOP_CANON.md`
5. The sources listed in `SOURCE_MANIFEST.json`

## Cursor workflow

1. Unzip this pack into `playtests/runs/seasonal/`.
2. Open the repository root in Cursor.
3. Start one orchestrator agent using `CURSOR_ORCHESTRATOR_PROMPT.md`.
4. Create the specialist agents listed in `AGENT_ROSTER.md`.
5. Give each agent only its dedicated file plus the scenario and canonical sources it needs.
6. Agents must write JSON results under `results/<scenario-id>/<agent-id>.json` using `RESULT_SCHEMA.json`.
7. Do not let agents edit canon files during testing.
8. Run `python compile_results.py`.
9. Return `COMPILED_REPORT.md`, the raw `results/` directory, and any proposed patches separately.

## Governing rule

> Decennium Descent should have 5e's readability and speed, Pathfinder 2e's tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems.

## Evidence standard

- Distinguish observed behavior from prediction.
- Record the exact rule and file path behind every finding.
- Use fixed seeds or a written deterministic decision order when possible.
- Never call a rule balanced because one simulation succeeded.
- Do not rewrite lore or reveal Director-only information in public tests.
