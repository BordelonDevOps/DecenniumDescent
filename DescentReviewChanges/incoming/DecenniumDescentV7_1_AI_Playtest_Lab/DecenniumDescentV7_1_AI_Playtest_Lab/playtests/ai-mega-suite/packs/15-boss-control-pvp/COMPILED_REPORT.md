# Boss, Control, and PvP Stress — Compiled Report

Raw JSON results: 11 (aggregates + samples + sealed claimant)
Canon edits: none
Director-only claimant details: `results/sealed/` (not for public mirrors)

## Scenario coverage

| Scenario | N | Win rate | Notable |
|---|---:|---:|---|
| BOSS-TENACITY | 1000 | 0.704 | Tenacity trips 10695; post-Tenacity lockouts 9108 |
| BOSS-PHASE | 1000 | 0.976 | avg phases ≈ 2.0 |
| BOSS-ACTORS | 1000 | 0.589 | **12616** illegal actor-cap attempts blocked |
| BOSS-ACTIONS | 1000 | 0.594 | **9370** illegal AAS restacks blocked |
| PVP-POINTBUY | 1000 | imported win 0.318 | no imported runaway |
| PVP-CLAIMANT-DIRECTOR | 500 | leakRate **0.0** | sealed procedure OK |

## Key findings

1. **Tenacity works as a buffer, not immunity** — large trip counts still leave thousands of post-Tenacity lockouts; control parties can lock bosses after Tenacity is spent (aligns with Pack 06 L15 control still losing on HP).
2. **Actor cap and AAS caps hold under spam** — illegal attempts are blocked at high volume; win rates ~0.59 under actor/action stress.
3. Phase transitions fire reliably (~2.0 phases) without breaking the sim.
4. Equal-point PvP: imported optimizer parties did **not** dominate (31.8% wins).
5. Claimant procedure: **zero public leaks** across 500 sealed seeds.

## Rules / design notes

- After Tenacity exhaustion, hard control can still full-skip bosses once/source — intended by canon, but Pack 06 shows control-heavy ceilings may lack damage to finish Catastrophic HP sponges.
- Proposed (not applied): optional second Tenacity on non-Gate severe bosses only if human play confirms lockout feels cheap — do **not** silent-edit.

## Evidence level

Monte Carlo Level A for boss/PvP aggregates; Pack 06 remains the dice-log authority for individual tactical claims.
