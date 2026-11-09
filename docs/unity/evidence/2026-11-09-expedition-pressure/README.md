# Expedition Pressure and Watch-end consequences (schema68 lifecycle and causal-history correction, TEST_ONLY)

**Status:** GPT reviewed `3d00c97457682f7fdac9eaef7bf82a83c24845a1` and `3a8db64bf37a51e94b4af90cd6b2bb1219adcfac`. It confirmed the three earlier findings were corrected and held the latter commit on a fourth defect: a long `AdvanceClock` could cross multiple Watches while `Current` excluded an earlier checkpoint assigned to that same in-flight command revision. GPT asked for an explicit cutoff and schema67/schema68 partition/save-restore regression. Codex reproduced `InvalidResult` on the reviewed runtime and implemented the explicit revision/time cutoff. The focused regression, full suite, dedicated assemblies and package checks now pass; GPT accepted the exact correction commit 11eda010b1c8e7fd74bede7221813e9971daa114 with no remaining concrete acceptance blocker for this bounded Pressure slice. This remains the same bounded TEST_ONLY MGT-03 slice, not a new module or completion of MGT-03/the engine. Unity remains deferred.

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

The earlier schema67 acceptance and arithmetic/source results below remain the module's original baseline; the table above is the prior schema68 lifecycle validation. The latest GPT review additionally found: (1) schema67 exact-Watch Haven arrival must retain its original `HavenArrivalAtWatchEnd` replay reason; (2) checkpoint cause validation must use the causal source set available at checkpoint application, so later same-Watch attacks can remain in history; and (3) attack exposure membership must respect receipt revision when attack and retreat share a RuleTime, including departure reactions. GPT confirmed the original three blockers were addressed and agreed that a late, previously uncounted category is carried through a derived once-only adjustment at Watch end or earlier safe-Haven admission, with the earlier checkpoint unchanged and no second roll. This source-silent reconciliation is explicitly TEST_ONLY. The focused correction and full validation now pass; see the next section. GPT accepted correction commit 11eda010b1c8e7fd74bede7221813e9971daa114; no concrete blocker remains. The mapped MGT-03 camps work under FL-07 is next for source-contract review and connection to camp-related Pressure. No successor implementation has started, and no unwritten mechanics are approved.

## Causal-history follow-up (same schema68 layout, TEST_ONLY; GPT accepted)

The correction preserves schema67's exact-boundary Haven-arrival reason. Checkpoint validation now compares each immutable checkpoint with the source changes available by its applied revision and RuleTime, while retaining later same-Watch evidence. Pressure after an early checkpoint is derived once from its original `PressureBefore`, the union of actual category evidence available by the due point, already-counted reduction credits and the captured Risk floor. The adjustment becomes visible at the Watch close or an actual safe-Haven admission after that checkpoint; it creates no second checkpoint, roll or mutable counter. A later checkpoint receives that derived value as its `PressureBefore`. The connected late-cause regression compares whole and split RuleClock advancement with save/restore, verifies the earlier checkpoint and RNG outcome remain unchanged, checks exact admission timing, and confirms one-time carry-forward into the next checkpoint.

Attack membership uses the exposure's start/end receipts. Earlier attacks at the same RuleTime as retreat remain valid when their receipt precedes the end receipt. A same-receipt opportunity attack is accepted only when a completed tactical move names the cohort member as mover and the attacker as a captured reactor. The producer records such attacks even when the movement ends exposure in that receipt. No serialized record or codec layout changed.

| Acceptance or reproduced finding | Result |
| --- | --- |
| Schema67 exact-Watch Haven reason and restore/continuation | [Baseline failure](development-attempts/gpt-review-fixes-3d00c974/reproduction/schema67-exact-watch/results.json); [1/1 focused PASS](development-attempts/gpt-review-fixes-3d00c974/validation/focused/schema67-exact-watch/results.json) |
| Later same-Watch attacks after an immutable early Haven checkpoint; duplicate category; actual admission; save/restore; next-checkpoint carry-forward | [Baseline `InvalidResult`](development-attempts/gpt-review-fixes-3d00c974/reproduction/late-watch-cause/results.json); [1/1 focused PASS](development-attempts/gpt-review-fixes-3d00c974/validation/focused/late-watch-cause/results.json) |
| Earlier attack and departure opportunity attack at the same RuleTime; completed tactical retreat; canonical save/restore | [Baseline `InvalidResult`](development-attempts/gpt-review-fixes-3d00c974/reproduction/same-time-retreat/results.json); [1/1 focused PASS](development-attempts/gpt-review-fixes-3d00c974/validation/focused/same-time-retreat/results.json) |
| Full C# 9 warnings-as-errors regression suite, Core/Persistence/LabModel/headless test assemblies | [1,281/1,281 PASS; 261 source hashes](development-attempts/gpt-review-fixes-3d00c974/validation/full-suite/results.json); retained assemblies and pressure saves are beside the report |
| Dedicated Core, Persistence and LabModel C# 9 warnings-as-errors compilation | [PASS; source hashes and all three assemblies](development-attempts/gpt-review-fixes-3d00c974/validation/assembly-compile/results.json) |
| Static Unity package structure validation | [18/18 PASS; 287 assets / 287 unique GUIDs](development-attempts/gpt-review-fixes-3d00c974/validation/package/results.json) |

Baseline results reproduce all three findings on the reviewed `3d00c974` runtime. Full and focused reports retain source hashes. The dedicated compile report records Core, Persistence and LabModel separately; the full suite additionally emits the headless test assembly. Existing schema66 historical evidence remains a 4,929-byte byte-identical decode/encode result. Unity Editor compilation, Edit/Play Mode, player builds and observed runtime gameplay were not run.

The scoped runnable scenario uses the selected TEST_ONLY route and combat fixture. It does not add production Haven authority, new enemy/content rules or other FL-08 causes/reductions. The source-silent late-cause timing remains TEST_ONLY per the actual Codex/GPT ruling. The complete engine, MGT-03 and Unity gameplay integration remain unfinished.

## In-flight checkpoint revision follow-up (schema67 and schema68; GPT accepted)

GPT's review of `3a8db64bf37a51e94b4af90cd6b2bb1219adcfac` confirmed the previous three fixes and found that a single clock command spanning two Watch boundaries omitted its first, in-flight checkpoint from the next Pressure calculation. The committed-state `Current` query filtered with `snapshot.Revision`, while the same resolving command assigned `AppliedRevision = s.Revision + 1`; final validation therefore rejected the computed later checkpoint as `InvalidResult`. This applied to schema67 too because the revision filter ran before the schema-specific projection.

Codex added a source-bound reproduction against the reviewed runtime: Pressure 5, one secured-route reduction, no combat, open exposure, and one command advancing across 28,800 and 57,600 seconds. The first checkpoint stored 4, but resolution of the next Watch returned `InvalidResult`. The failure report is [retained here](development-attempts/gpt-review-fixes-3a8db64/reproduction/inflight-multiwatch/results.json). The correction adds `ExpeditionPressureRules.CurrentAt(snapshot, cohortId, causalRevision, at)`; checkpoint resolution includes the current command revision and exact boundary time. Committed-state queries continue to use committed revision, and validation keeps checkpoint-specific causal cutoffs. No schema, payload, or early revision mutation was added.

| Acceptance | Result |
| --- | --- |
| Same secured-entry history, one command across two Watches, schema67 and schema68; split branch saves at Watch one and restores; compare both checkpoint results, RNG, consequences and final RuleClock; canonical save replay | [Focused 1/1 PASS](development-attempts/gpt-review-fixes-3a8db64/validation/focused/inflight-multiwatch/results.json) |
| Full C# 9 warnings-as-errors suite and Core/Persistence/LabModel/headless test compilation | [1,282/1,282 PASS; 261 source hashes](development-attempts/gpt-review-fixes-3a8db64/validation/full-suite/results.json) |
| Dedicated Core/Persistence/LabModel C# 9 warnings-as-errors compilation | [PASS; 190 source hashes and three assemblies](development-attempts/gpt-review-fixes-3a8db64/validation/assembly-compile/results.json) |
| Static package validation | [18/18 PASS; 287 assets / 287 unique GUIDs](development-attempts/gpt-review-fixes-3a8db64/validation/package/results.json) |

The focused regression's `ExpeditionPressureCases.cs` hash matches the full-suite report. Eleven pressure/in-flight save files plus compiled assemblies and all reports are retained in the evidence folder. GPT accepted the exact correction commit; the recorded optional authentic pre-correction schema67 archived-continuation check is not an acceptance requirement. Unity Editor import/compile, Edit/Play Mode, standalone/game builds and observed runtime play were not run; MGT-03, the full engine and Unity gameplay integration remain incomplete.

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
