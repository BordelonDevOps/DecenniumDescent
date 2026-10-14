# Expedition Attrition Monte Carlo — Compiled Report

**Pack:** `11-expedition-attrition-monte-carlo`
**Evidence:** Level A (executable Gameplay Loop v1.2 chassis)
**Canon:** No edits.

Raw JSON results: 198
Unreadable results: 0

## Scenario coverage

- **EXP-ABORT:** 25 results; evidence A
- **EXP-CASUALTY:** 25 results; evidence A
- **EXP-DEEP:** 25 results; evidence A
- **EXP-HAVEN:** 25 results; evidence A
- **EXP-REST-DEBT:** 73 results; evidence A
- **EXP-SHORT:** 25 results; evidence A

## Rules halts

Total instances: 284; unique codes: 3
- `EXTRACTION-HANDLING-MODS`: extraction.test cites handling modifiers beyond cargoDcModifierByHighestClass/attentionDcModifier; no numeric handling schedule in Loop JSON — sim uses 0.
- `UNKNOWN-PROGRESS-ZERO`: progressPerWatch.Unknown=0; without Map Route success, expedition cannot meet Progress targets — intentional deadlock risk.
- `REST-DEBT-INTERRUPT-TIMING`: Rest Debt deadline 'next two Watches and before next day boundary' — applied as day-boundary failure; interrupt mid-rest timing vs Evening camp workers remains underspecified in JSON.

## Findings

Total: 21
### high (1)
- EXP-REST-DEBT/aggressive/Unknown: havenRate 0.394 below 40%
### medium (14)
- EXP-DEEP/Unknown: objectiveRate 0.0 — progressPerWatch=0 without Map Route success
- EXP-REST-DEBT/Unknown: objectiveRate 0.0 — progressPerWatch=0 without Map Route success
- EXP-REST-DEBT/Unknown: objectiveRate 0.001 — progressPerWatch=0 without Map Route success
- EXP-REST-DEBT/Unknown: objectiveRate 0.008 — progressPerWatch=0 without Map Route success
- EXP-REST-DEBT/Unknown: objectiveRate 0.005 — progressPerWatch=0 without Map Route success
- EXP-REST-DEBT/cautious: haven arrivals still lose money 0.706 of the time (true profit after wages/shares)
- EXP-REST-DEBT/cautious: haven arrivals still lose money 0.702 of the time (true profit after wages/shares)
- EXP-SHORT/cautious: haven arrivals still lose money 0.728 of the time (true profit after wages/shares)
- EXP-SHORT/cautious: haven arrivals still lose money 0.785 of the time (true profit after wages/shares)
### info (6)
- EXP-ABORT rollup across 24 policy/mapping/level cells
- EXP-CASUALTY rollup across 24 policy/mapping/level cells
- EXP-DEEP rollup across 24 policy/mapping/level cells
- EXP-HAVEN rollup across 24 policy/mapping/level cells
- EXP-REST-DEBT rollup across 72 policy/mapping/level cells
- EXP-SHORT rollup across 24 policy/mapping/level cells

## Metric highlights

- **EXP-ABORT** (24 cells): havenRate=0.9798; wipeRate=0.0; objectiveRate=0.2075; meanTrueProfit=356.855
- **EXP-CASUALTY** (24 cells): havenRate=1.0; wipeRate=0.0; objectiveRate=0.9607; meanTrueProfit=205.3858
- **EXP-DEEP** (24 cells): havenRate=0.964; wipeRate=0.0; objectiveRate=0.2943; meanTrueProfit=2136.5138
- **EXP-HAVEN** (24 cells): havenRate=1.0; wipeRate=0.0; objectiveRate=0.8572; meanTrueProfit=326.7638
- **EXP-REST-DEBT** (72 cells): havenRate=0.982; wipeRate=0.0; objectiveRate=0.8234; meanTrueProfit=201.3006
- **EXP-SHORT** (24 cells): havenRate=1.0; wipeRate=0.0; objectiveRate=0.9757; meanTrueProfit=37.9312

## Evidence limitations

Chassis proxies party Strength capacity, Quartermaster modifiers, and some settlement wages. Numerical change proposals require holdout corroboration and owner review. No canon was edited.
