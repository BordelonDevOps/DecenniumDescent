# Statistical Combat Calibration

## Primary question

Do hit chances, damage, healing, resource curves, and survival rates behave consistently across levels before full class complexity is added?

## Evidence required

Executable seeded Monte Carlo with frozen baseline fixtures and confidence intervals.

## Run protocol

1. Read `SOURCE_MANIFEST.json`.
2. Freeze and hash all referenced sources and fixtures.
3. Create the listed agents as separate Cursor agents.
4. Run every row in `SCENARIO_MATRIX.csv`.
5. Use deterministic seeds for executable tests.
6. Write raw results under `results/<scenario-id>/`.
7. Record unclear rules as `RULES_HALT`, not as silent assumptions.
8. Run `python compile_results.py`.
9. Return the compiled report and complete raw results.

## Canon restriction

Do not edit canon during a run. Put suggestions in the suite-level `proposed-patches/` directory.
