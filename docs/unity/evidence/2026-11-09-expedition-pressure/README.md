# Expedition Pressure and Watch-end consequences (schema68 lifecycle correction, TEST_ONLY)

**Status:** GPT reviewed the schema67 implementation commit and held acceptance on three concrete lifecycle blockers. The corrections below implement schema68 behavior and await GPT's review of the exact correction commit. This remains the same bounded MGT-03 slice, not a new module or completion of MGT-03/the engine. Unity remains deferred.

## Scope and authorities

This increment implements source-bound FL-08/FL-09 pressure processing for one fixed `TEST_ONLY` traveler/cohort on selected existing route profiles. It persists the cohort seed, route exposure interval, source-linked Pressure changes and immutable Watch checkpoints. Each checkpoint records the before/stored/effective values, actual causes and reduction IDs, route and profile fingerprints, route quality/Risk floor, die/RNG state, classification, finite consequence, route position, deadline, and the command receipt/revision that settled it.

The implementation reuses `ExpeditionRouteTravelRecord` and its route fixture for route identity, Progress, geometry, Mapping, quality, Risk and Capacity; committed `MeleeAttackRecord`/`RangedAttackRecord` entries and canonical receipts for actual combat evidence; the shared `RuleClock`, `DiceStream`, WorkLedger, Camp Greens work, SnapshotCodec and command history for time, randomness, work, save/restore and replay. It adds no independently mutable Pressure counter. Route completion records remain historical rows, while only Moving/Paused rows block a new route command. Schema67 may resume an existing route after resolved tactical control while older route-only profiles retain their historical conflict behavior.

Exact schema records, consumer files, source rows and deliberately unsupported producers are listed in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The pre-implementation agreement is in [GPT_CONSENSUS.md](GPT_CONSENSUS.md). Source scope is the pinned player-book FL-08, FL-09, FL-10 and TR-13 text at ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

## Schema68 correction responding to GPT's first review

GPT's review of schema67 identified three blockers: a Standard timed Haven obstruction did not delay physical Haven admission; tactical steps could bypass a Severe route closure; and Severe closure ended the Pressure exposure before the traveler physically withdrew, so retreating through a later Watch lost a checkpoint. Each finding was reproduced against the earlier code: [Standard admission](results/schema68-gpt-follow-up/BASELINE_FAIL_STANDARD_ADMISSION.json), [tactical closure](results/schema68-gpt-follow-up/BASELINE_FAIL_TACTICAL_CLOSURE.json), and [retreat exposure](results/schema68-gpt-follow-up/BASELINE_FAIL_RETREAT_EXPOSURE.json).

The lifecycle correction uses the existing checkpoint, exposure, route-position, movement receipt, shared RuleClock, and command-history authorities. It does not add a second mutable pending-arrival ledger or serialized fields. The existing timed Haven checkpoint plus the active exposure and gate-side position derive pending admission. A Standard obstruction therefore holds the traveler at the route gate until its deadline; save/restore reconstructs the same pending state. A Severe checkpoint leaves the traveler at the gate, keeps exposure active, and routes both exploration and tactical movement through the same closure/retreat assessment. The traveler can retreat only along the existing route path; Watch boundaries still process during retreat, and exposure ends only on a completed physical step off the route. The accepted-clock target remains the shared command target. Schema67 save continuation deliberately keeps the historical admission/closure behavior; no serializer layout change was made.

| Correction acceptance | Result |
| --- | --- |
| Standard Haven obstruction resolves before admission; companion Camp Greens work advances the same clock; pending save/restore and byte-identical continuation | [1/1 PASS](results/schema68-gpt-follow-up/HAVEN_STANDARD_SAVE_RESTORE.json) |
| Severe Haven checkpoint keeps the traveler gate-side and permits physical route retreat | [1/1 PASS](results/schema68-gpt-follow-up/HAVEN_SEVERE_RETREAT.json) |
| Shared query and execution reject a tactical forward step through a Severe closure without changing snapshot bytes | [1/1 PASS](results/schema68-gpt-follow-up/TACTICAL_CLOSURE_GATE.json) |
| Severe retreat crosses a Watch, retains exposure/checkpoints, ends exposure after off-route departure, then permits normal movement | [1/1 PASS](results/schema68-gpt-follow-up/RETREAT_WATCH_RELEASE.json) |
| Generated schema67 save restores and continues with its legacy semantics and byte-identical branch state | [1/1 PASS](results/schema68-gpt-follow-up/SCHEMA67_COMPATIBILITY.json) |
| Full C# 9 warnings-as-errors regression run; Core, Persistence, LabModel and headless test compilation | [1,278/1,278 PASS; 261 source hashes](results/schema68-gpt-follow-up/FULL_SUITE_RESULTS.json) |
| Static Unity package structure validation | [18/18 PASS; 287 assets / 287 unique GUIDs](results/schema68-gpt-follow-up/PACKAGE_RESULTS.json) |

The full-run report records Unity Editor compilation, Edit Mode, Play Mode, standalone build and runtime gameplay as **NOT RUN**. One earlier run during correction returned 1,277/1,278 because a new retreat regression used the second Watch timestamp while asserting the first. The fixture timestamp was corrected, the affected case passed focused rerun, and the final full run passed 1,278/1,278. The validation attempt and final reports remain under `development-attempts/`.

The earlier schema67 acceptance and arithmetic/source results below remain the module's original baseline; the table above is the final schema68 correction validation. GPT has not yet reviewed this correction commit. No successor module may start before GPT confirms blocker closure, module acceptance, and alignment of the next dependency.

## Original schema67 module acceptance and baseline results

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
