# Haven Economy Stress — Compiled Report

**Pack:** `13-haven-economy-stress`
**Evidence:** Level A (executable Gameplay Loop v1.2 chassis)
**Canon:** No edits.

Raw JSON results: 43
Unreadable results: 0

## Scenario coverage

- **HAVEN-CHARTER:** 15 results; evidence A
- **HAVEN-COIN:** 3 results; evidence A
- **HAVEN-DEBT:** 3 results; evidence A
- **HAVEN-FACTION:** 11 results; evidence A
- **HAVEN-HEAT:** 7 results; evidence A
- **HAVEN-MARKET:** 4 results; evidence A

## Rules halts

Total instances: 15; unique codes: 3
- `COUNTERFEIT-SEIZURE-FRACTION`: coinAssay defines DCs and fees but not seizure/forfeiture fraction on detected counterfeit; sim uses 50% value loss proxy.
- `DEBT-INTEREST-OVER-CAP`: Requested rate 0.15 exceeds debtInterestCapPerOpening 0.1; clamped.
- `FACTION-ACCESS-THRESHOLDS`: reputation labels exist (-5..+5) but numeric access gates for desks/licenses are not fully tabulated in Gameplay Loop JSON; sim uses inferred thresholds.

## Findings

Total: 7
### info (7)
- long debt mean interest fraction 0.620; default rate 0.394
- medium debt mean interest fraction 0.256; default rate 0.116
- short debt mean interest fraction 0.055; default rate 0.043
- Demand 'glutted' multiplies sale value by 0.75 — glutted vs strategic spread is 2.00x
- Demand 'normal' multiplies sale value by 1.0 — glutted vs strategic spread is 2.00x
- Demand 'sought' multiplies sale value by 1.25 — glutted vs strategic spread is 2.00x
- Demand 'strategic' multiplies sale value by 1.5 — glutted vs strategic spread is 2.00x

## Metric highlights

- **HAVEN-CHARTER** (15 cells): meanTrueProfit=1048.678; lossRate=0.3953
- **HAVEN-HEAT** (7 cells): complicationRate=0.4331

## Evidence limitations

Chassis proxies party Strength capacity, Quartermaster modifiers, and some settlement wages. Numerical change proposals require holdout corroboration and owner review. No canon was edited.
