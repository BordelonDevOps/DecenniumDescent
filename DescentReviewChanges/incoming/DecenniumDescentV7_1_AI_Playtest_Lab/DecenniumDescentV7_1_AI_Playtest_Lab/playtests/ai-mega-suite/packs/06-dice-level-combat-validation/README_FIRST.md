# Pack 06 — Dice-Level Combat Validation

This pack exists because the first Cursor combat simulations used model-estimated DPR. Pack 06 permits no proxy arithmetic. It tests V7.1 with fixed legal builds, fixed public monster stat blocks, seeded dice, and complete round logs.

## Run order

1. Open the V7.1 repository root in Cursor.
2. Give Cursor `CURSOR_ORCHESTRATOR_PROMPT.md`.
3. Let the Build Auditor create and freeze the scenario character sheets.
4. Let the Encounter Curator copy exact enemy records into each scenario fixture.
5. Run every seed in `SCENARIO_MATRIX.csv`.
6. Do not edit canonical rules. Put rulings in `results/<scenario>/RULINGS.md`.
7. Run `python compile_results.py`.
8. Return `COMPILED_REPORT.md`, `frozen_builds/`, `fixtures/`, `results/`, and `rulings/`.
