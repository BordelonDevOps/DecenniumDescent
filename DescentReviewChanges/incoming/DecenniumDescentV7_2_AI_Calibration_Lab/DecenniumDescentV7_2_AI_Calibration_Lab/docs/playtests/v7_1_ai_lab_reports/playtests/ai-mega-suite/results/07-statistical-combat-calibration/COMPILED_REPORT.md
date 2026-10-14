# Statistical Combat Calibration — Compiled Report

**Pack:** `07-statistical-combat-calibration`  
**Evidence level:** A (seeded Monte Carlo chassis; not full class builds)  
**Seed:** `70700`  
**Source hash (Gameplay Loop v1.1):** `2f3167ff71e5c9ad99278e3d72bce48298bb71b3b9d623e430eea2851bd76ab8`  
**Outcome:** WARN (15 suspected defects; 0 confirmed inversions; 0 RULES_HALT)

## Test volume

| Scenario | Cells | Runs/cell | Evidence |
|---|---:|---:|---|
| MC-L1 | 4 | 1000 | A |
| MC-L3 | 4 | 1000 | A |
| MC-L5 | 4 | 1000 | A |
| MC-L10 | 10 | 1000 | A |
| MC-L15 | 8 | 1000 | A |
| MC-L20 | 8 | 1000 | A |

**Total:** 38 cells × 1000 seeds = **38,000** combat simulations. Raw JSON: 7 files under pack `results/` (+ suite mirror).

## Source and fixture hashes

- `data/public/Decennium_Descent_Gameplay_Loop_v1_1.json` = `src/data/gameplay-loop.json` (identical SHA-256)
- Budgets used: routine 50 / standard 90 / hard 130 / severe 180 / catastrophic 240 with ±20% per PC from four
- Opposition packed via `encounterMath.relativeThreatPoints` against party level

## Results by scenario

Mean win rates across all cells by labeled difficulty:

| Difficulty | Mean win rate | n cells |
|---|---:|---:|
| routine | 1.000 | 5 |
| standard | 0.924 | 9 |
| hard | 0.742 | 9 |
| severe | 0.235 | 9 |
| catastrophic | 0.028 | 6 |

Difficulty order is globally respected (no confirmed inversions). Separation fails locally between some adjacent bands and across levels.

## Statistical distributions

Representative 4-PC standard vs hard:

| Level | Standard WR | Hard WR | Notes |
|---:|---:|---:|---|
| 1 | 0.419 | 0.074 | Early game far deadlier than later |
| 3 | 0.897 | 0.343 | Hard still punishing |
| 5 | 1.000 | 0.936 | Standard trivial; hard soft |
| 10 | 1.000 | 0.958 | Soft mid-tier |
| 15 | 1.000 | 0.915 | Soft |
| 20 | 1.000 | 0.497 | Hard re-tightens at ceiling |

Hit rates stayed ~0.50–0.63 across levels (readable d20 chassis). Healing/RP proxies fired when support present; catastrophic wipe rates dominate severe+.

## Rules halts

Total: **0**

## Confirmed defects

None (no harder-budget win-rate inversions).

## Suspected defects

1. **Level-curve instability (high confidence for chassis):** Same budget labels produce L1 standard ~42% WR vs L5–20 standard ~100% WR. Relative threat packing alone does not keep “standard” meaning stable by level.
2. **Standard vs routine collapse at L5+:** Routine and standard both near-automatic wins for 4–6 PCs after early levels.
3. **Band collapse hard↔standard at several mid levels:** Adjacent bands often within ~5pp (see findings in scenario `summary.json`).
4. **Catastrophic remains appropriately rare** (~3% mean WR) — null finding for “too easy ceiling.”

## Null findings

- No RULES_HALT on published RTP table placement for tested budgets.
- Natural attack bonus / AC chassis yields mid-50s to low-60s hit rates (acceptable readability target).

## Proposed follow-up

- Human/Director playtest at L1 and L5 with published bestiary (not only synthetic RTP packs) before any global HP/damage edit.
- Consider level-banded budget multipliers or CR mix guidance (proposed patch only).
- Pack 06 dice-level should target L1 standard/hard and L10 standard soft spots.

## Evidence limitations

- Chassis roles (front/support/striker/caster), not full V7.1 class/feat/spell loadouts.
- Synthetic foes from threat points, not named bestiary entries.
- Average DPR proxies ≠ Pack 06 roll-by-roll proof.
