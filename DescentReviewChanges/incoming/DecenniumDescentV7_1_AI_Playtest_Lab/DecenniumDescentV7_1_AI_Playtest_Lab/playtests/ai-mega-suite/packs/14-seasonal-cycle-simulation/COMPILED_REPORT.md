# Seasonal and Decennial Campaign Simulation — Compiled Report

**Pack:** `14-seasonal-cycle-simulation`  
**Evidence:** Level A (seeded 3-Cycle × 3-Opening campaigns; public vs sealed records separated)  
**Canon:** No edits. Director sealed fields omitted from public metrics.  
**Volume:** 67 cell JSONs; matrix runs 250–500 per cell (≫1000 campaign seeds across suite)

## Primary question

Do maps, Haven districts, factions, heirs, artifacts, markets, and consequences persist enough to matter while replenishment creates a meaningfully new Opening?

**Verdict:** Yes — secured trunks raise map fidelity; unsecured chambers stay low-knowledge (nontrivialExplorationRate=1.0 across cells); failure scenarios damage districts (~99% stress) and activate heirs more often.

## Scenario coverage

| Scenario | Cells | Mean wealth | Mean heirs | Mean mapFidelity | District stress | Nontrivial explore |
|---|---:|---:|---:|---:|---:|---:|
| CYCLE-BASELINE | 12 | ~1350 | 0.46 | 0.82 | 0.39 | 1.00 |
| CYCLE-FAILURE | 12 | ~−632 | 1.24 | 0.71 | 0.99 | 1.00 |
| CYCLE-LEGACY | 6 | ~454 | 0.85 | 0.78 | 0.90 | 1.00 |
| CYCLE-MARKET | 18 | ~936 | 0.62 | 0.80 | 0.58 | 1.00 |
| CYCLE-MAP | 18 | ~913 | 0.62 | 0.80 | 0.59 | 1.00 |

## Persistence vs replenishment

- **Persistent:** secured trunks, artifacts, wealth, district state, heir depth — differ sharply Baseline vs Failure.
- **Replenished:** unsecured spurs respawn; chamberKnowledge stays ~0.1–0.4; marketDemand reshuffles — exploration remains nontrivial.
- **Canon boundary:** 0 sealed→public leaks in sims (`boundaryViolations=0`).

## Rules halts

- **OPENINGS-PER-CYCLE-COUNT** — seasonal JSON lacks hard-coded Openings/Cycle; used 3×3 per pack README.

## Confirmed findings

1. Failed extractions produce campaign-visible district stress and heir pressure.
2. Map fidelity does not collapse to zero when trunks exist — secured principles matter.
3. Replenishment prevents “solved dungeon” triviality across three Cycles.

## Suspected defects

- Heir activation rate on LEGACY (~0.85 mean) may be high/low vs intended dynasty pacing — needs human campaign feel check.
- Faction relationship deltas only lightly modeled.

## Proposed follow-up

Lock Openings-per-Cycle in seasonal JSON; publish public Cycle Record template vs sealed Director sheet.

## Evidence limitations

Abstract Opening outcomes, not full Pack 11 expedition coupling. Not proof of human fun.
