# Seasonal and Decennial Campaign Simulation

## Primary question

Do maps, Haven districts, factions, heirs, artifacts, markets, and consequences persist enough to matter while replenishment creates a meaningfully new Opening?

## Evidence required

At least one thousand seeded three-Cycle campaigns with public and sealed records separated.

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
