# Multi-recipe manufacturing — 2026-11-05

## Implementation

The existing manufacturing and formula-research fixtures now accept an explicit one- or two-recipe profile. Recipe 4 and Recipe 14 are the only admitted definitions. Their selector IDs remain stable: `0` is Recipe 4, `1` is Recipe 14. Source-manifest validation requires the selected profile to support both formula research/copy and manufacturing/output operations. Multi-recipe worlds without that manifest are rejected.

Initial component stock and supplementary vials are created as independent finite lots per recipe. Orders select by source recipe ID and preserve recipe-specific material set, package reservation, difficulty, yield, catalyst, output, and formula requirement. Only one order may remain open at a time; sequential orders share the existing clock, worker, apparatus, ledger, and deterministic RNG. Single-profile Recipe 4 and Recipe 14 key material remains unchanged; the combined profile gets a new fingerprint.

Authoritative state remains `FormulaWorkRecord`, `ManufacturingOrderRecord`, `WorkLedger`, `TradeProgressRecord`, `AlchemyDoseRecord`, and `Snapshot` content fingerprint, RNG, and receipts. No new simulation, inventory, clock, save mechanism, or schema fields were introduced.

## Runnable scenario and results

`manufacturing_two_source_recipes_coexist_with_recipe_keyed_knowledge_stock_and_replay` is the connected acceptance. It verifies independent formula knowledge, rejection of a not-yet-known formula, source-manifest gating, Recipe 4 completion and save/restore, Recipe 14 work across the eight-hour boundary, the existing incomplete-phase reset, paused restore and resume, separate outputs/materials/packaging, and exact duplicate replay.

- Multi-recipe acceptance: **1/1 PASS**. See [focused results](FOCUSED_MULTI_RECIPE_RESULTS.json).
- C# 9 warnings-as-errors compile: **PASS**.
- Full deterministic suite: **1,125/1,133 passed**. The eight failures have the same case names and exact exception text as the prior **1,124/1,132** baseline; each fails during schema42 harvest-manifest validation before manufacturing code runs. See [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json) and [the prior baseline](../2026-11-05-manufacturing-recipe14/HEADLESS_RESULTS.json).
- Static package validation: **18/18 PASS**, 213 package assets and 213 unique metadata GUIDs. See [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- Independent read-only code review found no concrete defect in the multi-recipe changes. The reviewer did not run tests; test results above are from the headless runner.

The exact source snapshots, manifest digest, code hashes, and named test are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The known eight harvest failures remain the next regression issue to resolve; they are not waived by this multi-recipe acceptance.
