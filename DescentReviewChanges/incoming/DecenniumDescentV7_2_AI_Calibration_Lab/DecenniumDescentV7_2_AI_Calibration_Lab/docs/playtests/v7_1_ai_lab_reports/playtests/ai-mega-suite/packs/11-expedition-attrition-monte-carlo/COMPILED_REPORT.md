# Expedition Attrition Monte Carlo — Compiled Report

**Pack:** `11-expedition-attrition-monte-carlo`  
**Evidence:** Level A (executable Gameplay Loop v1.1 state machine, deterministic seeds)  
**Canon:** No edits. Halts/patches only.  
**Source hash:** `data/public/Decennium_Descent_Gameplay_Loop_v1_1.json` (see suite `source-hashes.json`)  
**Volume:** 198 cell result JSONs; scenario matrix runs honored (1000–2000 per cell × policy/mapping/level/party)

## Primary question

Do Supply, Pressure, Sustenance, Rest Debt, Strain, Wounds, camps, and route mapping create survivable but meaningful long-form decisions?

**Verdict:** Partially yes under Mapped/Sketched with policy variance; Unknown mapping is a near-deadlock without Map Route success; wipe rate is near-zero in this chassis (attrition under-weighted vs Haven survival).

## Scenario coverage

| Scenario | Cells | Mean havenRate | Mean objectiveRate | Mean wipeRate | Mean trueProfit | Mean profitLossRate |
|---|---:|---:|---:|---:|---:|---:|
| EXP-SHORT | 24 | 1.00 | 0.98 | 0.00 | ~39 | 0.42 |
| EXP-HAVEN | 24 | 1.00 | 0.86 | 0.00 | ~333 | 0.19 |
| EXP-DEEP | 24 | 0.96 | 0.29 | 0.00 | ~2197 | 0.12 |
| EXP-CASUALTY | 24 | 1.00 | 0.96 | 0.00 | ~206 | 0.26 |
| EXP-REST-DEBT | 72 | 0.98 | 0.82 | 0.00 | ~206 | 0.32 |
| EXP-ABORT | 24 | 0.98 | 0.21 | 0.00 | ~364 | 0.19 |

## Statistical distributions (key)

- **Policy:** Cautious short descents often Haven-arrive yet lose money (profitLossRate ~0.72–0.77) after wages/shares — gross ≠ true profit.
- **Unknown mapping:** objectiveRate ≈ 0.0–0.01 when `progressPerWatch.Unknown=0` and Map Route fails (aggressive policy worsens this; EXP-REST-DEBT aggressive/Unknown havenRate 0.374).
- **Rest Debt:** Interrupt scenario fires `REST-DEBT-INTERRUPT-TIMING` halt; day-boundary Strain application is a chassis proxy.
- **Deep frontier:** High retained profit when objectives met, but Unknown cells never meet Progress targets.

## Rules halts (unique)

1. **EXTRACTION-CARGO-DC-MODS** — extraction test cites cargo modifiers with no numeric schedule; sim uses +EC to DC.
2. **UNKNOWN-PROGRESS-ZERO** — Unknown progress 0 without Map Route success is a soft lock.
3. **REST-DEBT-INTERRUPT-TIMING** — Rest Debt deadline vs interrupted Evening camp workers underspecified.

## Confirmed defects / design tensions

1. Haven survival too easy in chassis (wipe≈0) while economic failure remains common on short runs — survival and profitability are decoupled.
2. Unknown routes require explicit Map Route investment; aggressive “push” policy is self-defeating there.
3. Abort-objective scenarios rarely mark objective success (0.21) even when parties extract — abort success criteria need clearer charter wording.

## Suspected defects (need human table)

- Whether real tables hit wipe conditions more via combat (out of scope here) than Supply/Pressure alone.
- Camp storage tiers not fully stressed (storage used only indirectly).

## Null findings

- No evidence that Mapped vs Sketched collapses into identical outcomes; Sketched slows Progress and raises extraction cadence stress.

## Proposed follow-up

See `playtests/ai-mega-suite/proposed-patches/PACK_11_12_13_14_PROPOSED_PATCHES.md`.

## Evidence limitations

Chassis proxies Quartermaster mods, wages, and combat-lite Pressure complications. Not a substitute for Pack 02 agentic Watch play or Pack 06 dice combat.
