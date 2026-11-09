# Expedition Pressure and Watch-end consequences (schema67, TEST_ONLY)

**Status:** Implementation candidate complete; GPT review of the exact commit is pending. This is a bounded slice of MGT-03, not completion of the engine or MGT-03. Unity remains deferred.

## Scope and authorities

This increment implements source-bound FL-08/FL-09 pressure processing for one fixed `TEST_ONLY` traveler/cohort on selected existing route profiles. It persists the cohort seed, route exposure interval, source-linked Pressure changes and immutable Watch checkpoints. Each checkpoint records the before/stored/effective values, actual causes and reduction IDs, route and profile fingerprints, route quality/Risk floor, die/RNG state, classification, finite consequence, route position, deadline, and the command receipt/revision that settled it.

The implementation reuses `ExpeditionRouteTravelRecord` and its route fixture for route identity, Progress, geometry, Mapping, quality, Risk and Capacity; committed `MeleeAttackRecord`/`RangedAttackRecord` entries and canonical receipts for actual combat evidence; the shared `RuleClock`, `DiceStream`, WorkLedger, Camp Greens work, SnapshotCodec and command history for time, randomness, work, save/restore and replay. It adds no independently mutable Pressure counter. Route completion records remain historical rows, while only Moving/Paused rows block a new route command. Schema67 may resume an existing route after resolved tactical control while older route-only profiles retain their historical conflict behavior.

Exact schema records, consumer files, source rows and deliberately unsupported producers are listed in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The pre-implementation agreement is in [GPT_CONSENSUS.md](GPT_CONSENSUS.md). Source scope is the pinned player-book FL-08, FL-09, FL-10 and TR-13 text at ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

## Acceptance scenario and actual results

The scenarios run with C# 9 Roslyn compilation and warnings-as-errors. Full results preserve source hashes.

| Acceptance | Result |
| --- | --- |
| Pressure arithmetic, shared two-credit cap, Risk floor, TR-13 and FL-09 classification | [1/1 PASS](results/focused/PRESSURE_ARITHMETIC.json) |
| Actual hostile attacks during active route exposure; pre-Watch `FileSaveStore` save; restore/replay; whole/split shared-clock equivalence; Standard obstruction; companion Camp Greens work; route continuation; byte-identical restored command continuation | [1/1 PASS](results/focused/ACTUAL_COMBAT_STANDARD_SAVE_REPLAY.json) |
| Pressure 6 automatic Severe without RNG draw; closes the route; saves/restores; retreats on the existing physical path | [1/1 PASS](results/focused/SEVERE_CLOSURE_RETREAT.json) |
| Pressure 0 and Watch settlement consume no die; one-second portable handling that would cross the Watch boundary is rejected without changing bytes | [1/1 PASS after correction](results/focused/PRESSURE_ZERO_BOUNDARY_FIXED.json) |
| Early safe-Haven arrival settles once, retains Pressure, and rejects same-Watch route re-entry | [1/1 PASS](results/focused/EARLY_HAVEN.json) |
| Safe-Haven arrival exactly at 28,800 seconds produces one boundary settlement; schema67 save/restore followed by advancing to the next Watch remains byte-identical with no duplicate checkpoint/reset | [1/1 PASS](results/focused/EXACT_HAVEN_WATCH_END.json) |
| Full C# regression suite | [1,273/1,273 PASS; 261 source hashes](results/FULL_SUITE_RESULTS.json) |
| Separate Core, Persistence and LabModel compile | [PASS; 190 source hashes](results/COMPILE_RESULTS.json) |
| Static Unity package validation | [18/18 PASS; 563 package hashes](results/PACKAGE_RESULTS.json) |
| Supported historical save compatibility | [Schema66, 4,929 bytes, byte-identical decode/encode](results/HISTORICAL_SCHEMA66_ROUNDTRIP.json) |

### Reproduced validation defect and correction

The first pressure-zero boundary test failed concretely: `HandlePortableEquipment` committed a one-second drop from `28,799.5` to `28,800.5` seconds, crossing a pressure Watch boundary. The shared management preflight already checked this deadline, but portable equipment dispatches through its own resolver, whose timed-handling checks omitted Expedition Pressure. The before-fix failure is retained in [BOUNDARY_BEFORE_FIX.json](results/diagnostics/BOUNDARY_BEFORE_FIX.json). The correction adds the same `NextExpeditionPressureBoundary` guard in that resolver; the regression then passed as shown above. No other gameplay result was changed for this fix.

## Remaining limits and gates

- The only pressure increase currently produced is one open-combat category derived from committed attacks involving the cohort. Several attacks remain one category. The only reduction currently produced is a qualifying secured-route entry, capped at two credits in a Watch. Capacity, missing/captured members, pursuit, abort, exposed camps, Attention cargo, Counter-Ambush, concealed camps, pursuit ending, and reconnaissance remain unsupported; they are not treated as inferred facts.
- The selected TEST_ONLY route fixture supplies the route, Risk, quality and geometry. The pressure fixture marks `TestOnlyCropPolicy.PlotId` as a safe-Haven endpoint only for timing tests; this does not create a canonical Haven or its services.
- Runtime complications are limited to a 60-minute obstruction and closure/physical retreat on that same existing route. No new enemy, damage, loot, evacuation, cargo or casualty result is created. Minor is gated by a source-applied modifier/reroll, which this profile does not have.
- This does not implement the complete travelling group, camps, extraction, generalized routes, production pressure content, or the other FL-08 causes/reductions. MGT-03 and the overall engine remain partial.
- Unity Editor import, Unity Edit Mode/Play Mode tests and game builds were **not run**.

## GPT review gate

GPT must review the exact commit and evidence files above, verify the agreed scope and source requirements, identify any concrete blocker, and confirm whether the acceptance criteria pass and the next mapped dependency is aligned. An attempted message does not complete this gate. The review result will be recorded in [GPT_REVIEW.md](GPT_REVIEW.md); no next module will begin before actual GPT agreement.

**Implementation commit:** pending.
**GPT implementation review:** pending.
