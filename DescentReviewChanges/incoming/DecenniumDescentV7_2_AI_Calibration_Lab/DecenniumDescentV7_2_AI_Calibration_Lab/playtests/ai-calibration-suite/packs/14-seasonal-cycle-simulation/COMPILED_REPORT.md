# Seasonal Cycle Simulation — Compiled Report

**Pack:** `14-seasonal-cycle-simulation`
**Evidence:** Level A (executable Gameplay Loop v1.2 chassis)
**Canon:** No edits.

Raw JSON results: 67
Unreadable results: 0

## Scenario coverage

- **CYCLE-BASELINE:** 12 results; evidence A
- **CYCLE-FAILURE:** 12 results; evidence A
- **CYCLE-LEGACY:** 6 results; evidence A
- **CYCLE-MAP:** 18 results; evidence A
- **CYCLE-MARKET:** 18 results; evidence A
- **_META:** 1 results; evidence A

## Rules halts

Total instances: 12; unique codes: 1
- `MATRIX-VS-SEASONAL-OPENINGS`: SCENARIO_MATRIX objective mentions three Openings, but seasonal.openingsPerCycle=1; sim follows Loop JSON (exactly one Opening per Cycle).

## Findings

Total: 1
### info (1)
- Wrote 66 aggregated campaign result files; each embeds n runs (see scenario matrix).

## Metric highlights

- **CYCLE-BASELINE** (12 cells): nontrivialExplorationRate=1.0; meanMapFidelity=0.6974
- **CYCLE-FAILURE** (12 cells): nontrivialExplorationRate=1.0; meanMapFidelity=0.6152
- **CYCLE-LEGACY** (6 cells): nontrivialExplorationRate=1.0; meanMapFidelity=0.6618
- **CYCLE-MAP** (18 cells): nontrivialExplorationRate=1.0; meanMapFidelity=0.6692
- **CYCLE-MARKET** (18 cells): nontrivialExplorationRate=1.0; meanMapFidelity=0.6829

## Evidence limitations

Chassis proxies party Strength capacity, Quartermaster modifiers, and some settlement wages. Numerical change proposals require holdout corroboration and owner review. No canon was edited.
