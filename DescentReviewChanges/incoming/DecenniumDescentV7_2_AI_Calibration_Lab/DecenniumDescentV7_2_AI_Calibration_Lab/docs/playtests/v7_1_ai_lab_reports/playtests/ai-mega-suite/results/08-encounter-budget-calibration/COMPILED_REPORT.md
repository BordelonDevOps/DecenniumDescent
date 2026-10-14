# Encounter Budget Calibration — Compiled Report

**Pack:** `08-encounter-budget-calibration`  
**Evidence level:** A (seeded objective simulations)  
**Seed:** `80800`  
**Source hash (Gameplay Loop v1.1):** `2f3167ff71e5c9ad99278e3d72bce48298bb71b3b9d623e430eea2851bd76ab8`  
**Outcome:** FAIL (5 confirmed band-collapse defects; 71 findings; RULES_HALT on objective step stacking)

## Test volume

| Scenario | Objective | Runs/cell | Cells (approx) |
|---|---|---:|---:|
| BUDGET-CROSS | Kill, neutral terrain | 200 | 120 |
| BUDGET-CARGO | Protect cargo fixed rounds | 200 | 18 |
| BUDGET-ESCORT | Escort to exit | 200 | 18 |
| BUDGET-HAZARD | Combat + hazard | 200 | 9 |
| BUDGET-AMBUSH | Surprise disadvantage | 200 | 9 |
| BUDGET-RETREAT | Controlled withdrawal | 200 | 12 |

**Total:** 186 cells × 200 seeds = **37,200** objective simulations.

## Source and fixture hashes

- Budgets and RTP from Gameplay Loop v1.1 `encounterMath`
- Party-size rule: ±20% budget per PC from four
- Canon note: objectives / hostile terrain / surprise / hazards each increase effective difficulty one step unless already included in creature levels

## Results by scenario

Mean objective success by labeled difficulty (averaged across levels/party sizes in matrix):

| Scenario | routine | standard | hard | severe | catastrophic |
|---|---:|---:|---:|---:|---:|
| BUDGET-CROSS | 1.00 | 0.86 | 0.54 | 0.20 | 0.00 |
| BUDGET-CARGO | — | 0.81 | 0.39 | 0.07 | — |
| BUDGET-ESCORT | — | 1.00 | 0.89 | 0.65 | — |
| BUDGET-HAZARD | — | 0.50 | 0.06 | 0.00 | — |
| BUDGET-AMBUSH | — | 0.00 | 0.00 | 0.00 | — |
| BUDGET-RETREAT | — | — | — | 1.00 | 1.00 |

## Statistical distributions

- **Kill (CROSS):** Best-behaved band ladder; catastrophic nearly unwinnable; routine automatic. Supports published 50/90/130/180/240 as a starting kill-budget scale on neutral ground.
- **Cargo / Hazard:** Steeper than kill at same labels once objective pressure is applied.
- **Escort:** Too easy; high-level 6-PC cells collapse (confirmed).
- **Ambush:** Total failure across all tested labels (confirmed collapse) — surprise free round + kill objective overwhelms chassis party.
- **Retreat:** Near-automatic even at catastrophic — withdrawal objective not stress-calibrated by creature budget alone.

## Rules halts

Total unique topics: **objective step stacking** (logged on CARGO/ESCORT/HAZARD/AMBUSH/RETREAT).

> GAMEPLAY_LOOP_CANON: objectives/terrain/surprise/hazards each increase effective difficulty by one step unless already included in creature levels. Scenario matrix labels a difficulty while sims apply objective mechanics separately — risk of double-count or under-count. **Needs owner clarification before numerical budget edits.**

## Confirmed defects

1. **BUDGET-ESCORT L10/L15 × 6 PC:** All bands within 12pp (success ≈ 0.97–1.00).
2. **BUDGET-AMBUSH L3/L5/L10 × 4 PC:** All bands at 0.00 success — labels not predictive.

## Suspected defects

- 54× adjacent-band nondistinct (&lt;5pp) pairs across scenarios.
- 12× party-size scaling unstable (&gt;25pp swing after ±20% budget adjust).
- Retreat success decoupled from threat budget.

## Null findings

- Neutral kill ladder (CROSS) shows ordered, separated bands at suite level — do **not** scrap four-character budgets based on kill-only evidence.

## Proposed follow-up

- Clarify whether matrix difficulty already includes the one-step objective modifier.
- Ambush / escort / retreat need objective-specific calibration tables (or mandatory step-up + tooling), not only kill budgets.
- Re-test party-size ±20% with full bestiary packs after Pack 06.

## Evidence limitations

- Synthetic RTP foes; objective automata are proxies for table play.
- Ambush model (free round + AC-2) may be harsher or softer than final surprise rules — treat as stress bound.
