# Proposed patches — Packs 11–14 (V7.1 AI mega-suite)

**Status:** Suggestions only. Do **not** apply without owner approval. No canon edited during this run.

## P11-01 — Document Unknown Progress / Map Route gate
- **Issue:** `route.progressPerWatch.Unknown = 0` soft-locks objectives without Map Route success.
- **Evidence:** Pack 11 EXP-DEEP/REST-DEBT Unknown objectiveRate ≈ 0; Pack 12 CARGO-UNKNOWN havenRate 0.83.
- **Proposal:** Player-facing callout: Unknown routes require Recon Map Route before Progress expectations; optional Director table for “forced march” Progress at high Pressure cost.

## P11-02 — Rest Debt interrupt timing
- **Issue:** Rest Debt “next two Watches and before next day boundary” underspecified for interrupted Evening camp workers.
- **Evidence:** RULES_HALT `REST-DEBT-INTERRUPT-TIMING`.
- **Proposal:** One worked example in Gameplay Loop: interrupt mid-Long-Rest → debt clears only after full Rest Watch; camp workers on duty accrue debt if they skip owed Rest.

## P11-03 — Abort success metric
- **Issue:** EXP-ABORT objectiveRate ~0.21 despite high Haven arrival — charter abort success unclear.
- **Proposal:** Require charters to define abort success as “Haven with ≤X casualties and ≥Y reserve Supply before Pressure Z.”

## P12-01 — Numeric extraction cargo DC modifiers
- **Issue:** `extraction.test` references cargo modifiers without numbers.
- **Evidence:** RULES_HALT `EXTRACTION-CARGO-DC-MODS`; EC retention curve still rational under +EC proxy.
- **Proposal:** Table e.g. +0/+1/+2/+3/+4/+5/+6 by Extraction Class, stack caps, Attention tag +1 once.

## P13-01 — Counterfeit seizure fraction
- **Issue:** Assay DCs/fees exist; forfeiture on detect does not.
- **Proposal:** Add `coinAssay.detectedCounterfeitForfeiture` (e.g. 1.0 seized + fine).

## P13-02 — Reputation access gate table
- **Issue:** Labels −5…+5 without desk/license thresholds.
- **Proposal:** Tabulate marketDesk / licensedMaterials / strategicAuctions / sovereignContracts minima.

## P13-03 — Bribe floor vs Heat 0
- **Issue:** `bribes.floorWhileActive: 1` can create Heat if bribe applied at 0.
- **Proposal:** Floor applies only if Heat was ≥1 before bribe, or bribes illegal at Heat 0.

## P14-01 — Openings per Cycle
- **Issue:** Seasonal JSON omits Openings/Cycle count.
- **Proposal:** Add `seasonal.openingsPerCycle: 3` (or owner value) to match pack README / campaign sheets.

## Ranking by confidence
1. P12-01 / P11-01 (high — blocks adjudication)
2. P13-01 / P13-02 / P14-01 (high — missing tables)
3. P11-02 / P13-03 (medium)
4. P11-03 (medium — charter UX)
