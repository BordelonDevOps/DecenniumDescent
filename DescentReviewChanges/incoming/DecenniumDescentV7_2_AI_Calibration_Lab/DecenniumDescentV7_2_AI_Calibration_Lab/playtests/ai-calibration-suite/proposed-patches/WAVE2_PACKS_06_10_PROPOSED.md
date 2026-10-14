# Proposed patches — V7.2 Wave 2 (Packs 06–10)

**Date:** 2026-08-06  
**Status:** proposals only — **no canon edits applied**  
**Evidence:** raw JSON under `playtests/ai-calibration-suite/results/` (`06-…`, `p07`/`07-…`, `p08`/`08-…`, `p09`/`09-…`, `p10`/`10-…`)

## Pack 06 — dice-level combat

1. **L1 Standard retune (candidate):** Cave Bear + Crystal Shardling at Standard / protect-cargo produced **0/10** party victories. Consider −1 relative threat step or Explicit cargo-timer teaching encounter before claiming class-balance at L1.
2. **L10 Dark / L15 Control:** Weave/control parties **0/10** vs named threats. Candidate: encounter budget step-down for Traumatic Casting parties **or** clearer Tenacity/save pacing — hold for Pack 07/15 corroboration.
3. **Sheet reminder:** Independent actor cap (≤2 per controller) and Traumatic Casting retrigger blocks held in logs; add companion UI guards, not rulebook rewrite.

## Pack 07 — statistical chassis

1. **Level-scaled budgets:** Multiple `level_curve_instability` WARN cells — L1 too deadly / L5+ standard soft. Candidate scales only after holdout corroboration (disjoint seeds already used in runner).
2. Treat all Pack 07 rates as **proxy chassis** until Pack 06 frozen builds agree.

## Pack 08 — encounter budgets / objectives

1. **BUDGET-AMBUSH / BUDGET-ESCORT = FAIL:** Ambush success collapsed; escort objective progress model too brittle. Candidate: explicit ambush surprise table + escort checkpoint rules in companion — **RULES_HALT** until Director text names the clock.
2. **Objective one-step stacking HALT:** Do not silently invent multi-objective stacking; propose companion validator only.

## Pack 09 — interactions

1. Flag top pairwise/triple tags (`extra_action`, `actor`, `reset`, `unbounded`, `control`) for Designer review.
2. **RULES_HALT:** Data resets cannot reset the same ability more than once per round — sheet reminder.

## Pack 10 — progression / multiclass

1. Pure-class viability OK across 17×4×6.
2. Multiclass dip / AAS stacking watch — **RULES_HALT** for prestige/AAS double-fill confirmation.
3. Dark-path actor-cap / Traumatic retrigger blocks observed; keep as runtime guards.

## Explicit non-actions

- No Player Rulebook / DM-01 / ReviewBible text changes.
- No auto-promotion from `incoming/`.
