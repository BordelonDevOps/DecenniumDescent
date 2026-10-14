# Proposed patch notes — Wave 3 (packs 11–14)

**Status:** candidate only — no canon edited  
**Source:** V7.2 AI Calibration Lab executable chassis (Gameplay Loop v1.2)

## Rules gaps (halts)

1. **EXTRACTION-HANDLING-MODS** — `extraction.test` mentions handling modifiers; Loop JSON has `cargoDcModifierByHighestClass`, `attentionDcModifier`, `cargoModifierCap` but no numeric handling schedule.
2. **UNKNOWN-PROGRESS-ZERO** — `progressPerWatch.Unknown=0` creates near-deadlock without Map Route; confirm intentional vs needs Forced March / scout escape valve in public JSON.
3. **REST-DEBT-INTERRUPT-TIMING** — Rest Debt interrupt mid-rest vs Evening camp workers underspecified.
4. **COUNTERFEIT-SEIZURE-FRACTION** — coinAssay DCs/fees present; seizure/forfeiture fraction on detected counterfeit missing.
5. **FACTION-ACCESS-THRESHOLDS** — reputation labels −5..+5 exist; desk/license numeric gates not tabulated.
6. **MATRIX-VS-SEASONAL-OPENINGS** — Pack 14 matrix text says “three Openings”; `seasonal.openingsPerCycle=1` (sim follows JSON / master orchestrator).

## Balance hypotheses (need holdout + owner)

- Pack 11 wipeRate ≈ 0 across cells — attrition may be under-weighted vs Haven survival.
- Cautious short descents often lose money after wages/shares despite haven arrival.
- Unknown mapping objectiveRate ≈ 0 without Map Route success.
- Pack 12 EC ladder shows graded cargoLossRate (light ~0.19 → attention ~0.50) — tradeoff present; no high-severity defects auto-flagged.
