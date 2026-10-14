# Decennium Descent V7.2 — AI Lab Evidence Review

**Source:** `DD_V7_1_AI_Lab_Reports.zip`  
**Reviewed:** 2026-08-06  
**Evidence indexed by the returned lab:** 1,941 JSON result files before the user created the report ZIP. The returned ZIP contains compiled reports and proposals, not the raw JSON corpus.

## Evidence ruling

The reports are strong enough to support procedural clarification, invariant guards, and the design of the next calibration suite. They do not support a global class rebalance by themselves.

- Deterministic rolls, frozen fixtures, Monte Carlo distributions, and property tests can support mathematical findings.
- Persona narration can identify ambiguity and lookup burden, but it cannot prove fun, comprehension, or balance.
- The returned report ZIP omitted Packs 01–04 and omitted the raw JSON used to compile the reports. Their conclusions are preserved as report evidence, but V7.2 requires raw-result retention in the next lab.

## Confirmed findings promoted in V7.2

1. **Objective difficulty was ambiguous.** Final difficulty now includes each objective, terrain, surprise, and hazard adjustment exactly once.
2. **Rest Debt conflicted with the companion.** The authoritative procedure is now a two-Watch countdown, and the tracker exposes that countdown directly.
3. **Retreat could double-count Escape.** An ordinary round now uses at most one Escape source; Critical Success remains an explicit two-success outcome.
4. **Extraction cited undefined cargo modifiers.** Highest Extraction Class now contributes +0 through +6, exposed Attention adds +1, and cargo-and-handling modifiers cap at +7.
5. **Unknown routes could deadlock.** Forced March now provides a costly, dangerous fallback without replacing Reconnaissance.
6. **Haven procedures had missing adjudication tables.** V7.2 adds a Tier I short path, counterfeit disposition, reputation access gates, insurance formulas, and Heat-at-zero clarification.
7. **Seasonal simulation used the wrong campaign premise.** Canon now explicitly records one Opening per ten-year Cycle. Multiple campaigns or expedition phases inside that Opening are not additional Openings.
8. **Windows release validation was fragile.** Public-canon and gameplay validators now use explicit UTF-8 and ASCII-safe status output.
9. **Prestige testing lacked a machine-readable registry.** V7.2 generates and validates an eighteen-path prestige snapshot.
10. **New-player lookup burden was real.** V7.2 includes a public one-page Quickstart.

## Mathematical findings retained as provisional

The V7.1 statistical proxy reported that the same encounter labels produced materially different outcomes by level:

| Example | Reported result |
|---|---:|
| Level 1, four players, Standard | 41.9% win rate |
| Level 5, four players, Standard | 100% |
| Level 10, four players, Standard | 100% |
| Level 15, four players, Standard | 100% |
| Level 20, four players, Standard | 100% in the proxy; dice-level compositions were unstable |

The report also found objective-specific instability:

- Cargo objectives were harder than neutral defeat encounters.
- Escort objectives were often too easy in the proxy.
- Hazard objectives were often nearly impossible.
- The ambush model was invalid because it granted an unrestricted enemy round.
- Retreat success was not predicted by kill budget.

V7.2 therefore defines target success bands and objective-specific construction rules but does **not** replace the 50/90/130/180/240 table without holdout validation.

## Class and action-economy findings

- The Shared Additional Action Slot held in the tested scenarios.
- The independent-actor cap held.
- Traumatic Casting self-retrigger attempts were blocked.
- Tenacity functioned as a control buffer.
- High-level results were composition sensitive.
- The static interaction scanner found risk clusters around action resets, extra actions, independent actors, and hard control, but did not prove an actual legal infinite loop.

No global class, feat, or spell nerf is promoted from those reports.

## Expedition, cargo, and economy findings

- Survival to the Haven was often too easy in the simplified attrition chassis, while financial success was meaningfully harder.
- Cargo retention declined rationally as Extraction Class increased.
- Unknown routes materially reduced successful return rates.
- The gross/net/true-profit distinction prevented false profitability claims.
- Sponsor share, provenance, taxes, and extraction loss created meaningful economic tradeoffs.

The next lab must couple real combat-resource expenditure to expedition attrition instead of using independent proxies.

## Required V7.2 holdout tests

1. Re-run the missing class, expedition, Haven, and Cycle persona packs.
2. Grid-search encounter budgets by level band, party size, and final difficulty.
3. Split tuning seeds from holdout seeds; a candidate table cannot be promoted if it only fits its training seeds.
4. Test named public bestiary fixtures as well as generic mathematical profiles.
5. Calibrate defeat, cargo, escort, hazard, ambush, and retreat objectives separately.
6. Run every class at levels 1, 3, 5, 10, 15, and 20 with frozen legal builds.
7. Couple combat losses, spell resources, Wounds, Rest Debt, Supply, cargo, and extraction into full-expedition simulations.
8. Re-run property tests with fail-closed state guards and a compiler that preserves nested failure records.
9. Preserve raw JSON, source hashes, fixture hashes, seeds, and proposed patches in the return ZIP.

## Human-table work after mathematical calibration

AI can reduce the number of obvious mathematical failures taken to a human table. It cannot establish whether the game is enjoyable, whether tactical choices feel meaningful, whether social scenes breathe, or whether a GM can adjudicate edge cases under real time pressure. The first human GM test should therefore begin only after the V7.2 calibration gate passes, then focus on pace, clarity, tension, and enjoyment rather than basic arithmetic repair.
