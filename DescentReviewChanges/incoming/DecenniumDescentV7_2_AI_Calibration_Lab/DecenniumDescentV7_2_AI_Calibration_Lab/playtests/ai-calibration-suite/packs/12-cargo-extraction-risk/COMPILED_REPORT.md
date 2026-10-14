# Cargo and Extraction Risk — Compiled Report

**Pack:** `12-cargo-extraction-risk`
**Evidence:** Level A (executable Gameplay Loop v1.2 chassis)
**Canon:** No edits.

Raw JSON results: 150
Unreadable results: 0

## Scenario coverage

- **CARGO-ATTENTION:** 36 results; evidence A
- **CARGO-CASUALTY:** 36 results; evidence A
- **CARGO-LIGHT:** 36 results; evidence A
- **CARGO-RARE:** 24 results; evidence A
- **CARGO-UNKNOWN:** 18 results; evidence A

## Rules halts

Total instances: 168; unique codes: 2
- `EXTRACTION-HANDLING-MODS`: extraction.test cites handling modifiers beyond cargoDcModifierByHighestClass/attentionDcModifier; no numeric handling schedule in Loop JSON — sim uses 0.
- `UNKNOWN-PROGRESS-ZERO`: progressPerWatch.Unknown=0; without Map Route success, expedition cannot meet Progress targets — intentional deadlock risk.

## Findings

Total: 0

## Metric highlights

- **CARGO-ATTENTION** (36 cells): havenRate=1.0; cargoLossRate=0.5033; meanRetainedLoadFrac=0.4967; meanTrueProfit=389.4217
- **CARGO-CASUALTY** (36 cells): havenRate=1.0; cargoLossRate=0.3194; meanRetainedLoadFrac=0.6806; meanTrueProfit=84.7631
- **CARGO-LIGHT** (36 cells): havenRate=1.0; cargoLossRate=0.1908; meanRetainedLoadFrac=0.8092; meanTrueProfit=20.3897
- **CARGO-RARE** (24 cells): havenRate=1.0; cargoLossRate=0.3356; meanRetainedLoadFrac=0.6644; meanTrueProfit=146.0417
- **CARGO-UNKNOWN** (18 cells): havenRate=0.8335; cargoLossRate=0.4009; meanRetainedLoadFrac=0.5991; meanTrueProfit=401.5278

## Evidence limitations

Chassis proxies party Strength capacity, Quartermaster modifiers, and some settlement wages. Numerical change proposals require holdout corroboration and owner review. No canon was edited.
