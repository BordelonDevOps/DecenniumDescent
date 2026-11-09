# MGT-03 camp use and Pressure — schema69 evidence

**Status:** GPT reviewed implementation commit `706a129808443c028d1d063f59f1911c1c164473` and held acceptance on three integration defects. The corrections below are implemented and validated; GPT's review of the correction commit is pending. No successor module starts before that review accepts the module. This does not establish completion of all MGT-03 or the engine.

## Agreed scope and authorities

The slice connects FL-07 actual camp use to FL-08 Pressure using an authored fixed TEST_ONLY camp site at one existing route checkpoint. It uses existing route travel/spatial records and `WorldPositionResolver`, committed commands/receipts, `RuleClock`, `WorkLedger`, active cohort/exposure, typed Pressure changes/checkpoints, deterministic RNG, encounters/consequences, snapshot validation and persistence. New schema69 state is limited to camp profile/use/lying-low history and checkpoint context. Existing schema67/68 behavior and serialized layouts remain in their earlier branches.

Codex/GPT's pre-implementation contract and pinned source references are in [CAMP_USE_PRESSURE_RULE_DECISIONS.md](../../CAMP_USE_PRESSURE_RULE_DECISIONS.md). The map and architecture trace are in [IMPLEMENTATION_TRACE.md](../../IMPLEMENTATION_TRACE.md#2026-11-09--mgt-03-camp-use-and-pressure-schema69-test_only), and the current checkpoint is in [DEVELOPMENT_HANDOFF.md](../../DEVELOPMENT_HANDOFF.md).

## Connected acceptance

The full suite's seven camp-specific cases all pass. The three correction regressions directly cover the held findings:

- `expedition_camp_unrelated_companion_traversal_preserves_active_use_and_low_restore`: a valid companion traversal can start while the cohort remains at its route checkpoint with active use and lying-low; save/restore, replay and duplicate receipt remain canonical.
- `expedition_camp_severe_closure_accepts_tactical_turn_clock_receipt`: a tactical regular turn ends exactly at the Severe Watch boundary; query and execution both admit the turn, and camp use closes against that exact clock receipt and checkpoint across save/restore and duplicate replay.
- `expedition_camp_movement_encounter_entry_interrupts_low_and_replays`: a hostile world step enters tactical control; lying-low ends with the same `BeginWorldStep` receipt while camp use remains active, and save/restore replay matches.

The four original camp cases also pass:

- `expedition_camp_known_use_and_actual_combat_are_distinct_pressure_categories`: repeated camp use deduplicates within the category; actual combat is separately counted; Severe closure uses actual retreat.
- `expedition_camp_exposed_pressure_context_and_companion_farming_connect`: exposed camp creates the agreed Pressure/context; companion Camp Greens work progresses independently during obstruction.
- `expedition_camp_early_haven_uses_route_context_and_does_not_settle_twice`: an earlier Haven checkpoint retains its established context and does not reroll or settle twice.
- `expedition_camp_concealed_full_watch_lie_low_saves_replays_and_requires_unbroken_coverage`: full concealed Watch grants one shared-cap reduction; an exact closing boundary is credited to the just-completed Watch; interrupted/partial intervals grant none; mid-Watch save/restore and command replay match; one clock command crossing multiple Watches remains deterministic; lying-low grants no Rest record.

## Validation (exact correction source)

- Full C# 9 warnings-as-errors suite: **PASS, 1,289/1,289**, zero failures; 264 source hashes. The runner compiled Core, Persistence, LabModel and HeadlessTests.
- Standalone C# compilation: **PASS**, Core, Persistence and LabModel with warnings as errors; 193 source hashes.
- Static package structure validation: **PASS, 18/18** checks; 290 package assets and 290 unique GUIDs. This is not Unity import/compilation.
- Unity Editor import/compile, Edit Mode, Play Mode, standalone/player build and observed gameplay: **NOT RUN** (outside this increment and Unity integration remains deferred).

Retained before/after evidence:

- [Baseline companion traversal failure](development-attempts/gpt-review-fixes-706a129/reproduced-before-final/companion-traversal/run-20261109T150444052Z-f4e7601f/results.json): query was Available, execution rejected with `InvalidResult`.
- [Baseline tactical turn closure failure](development-attempts/gpt-review-fixes-706a129/reproduced-before-final/tactical-pressure-closure/run-20261109T150529809Z-3312e07b/results.json): `EndRegularTurn` rejected with `InvalidResult` at clock 28,798 before it could create the Severe checkpoint.
- [Baseline movement-triggered combat failure](development-attempts/gpt-review-fixes-706a129/reproduced-before-final/movement-combat/run-20261109T150609731Z-c2dbbd2a/results.json): query reported `EncounterTransition`, execution rejected with `InvalidResult`.
- [Final full suite report](development-attempts/gpt-review-fixes-706a129/final-validation/suite/run-20261109T151653653Z-0f4ce744/results.json)
- [Final standalone compile report](development-attempts/gpt-review-fixes-706a129/final-validation/compile/compile-20261109T151935633Z-baf8cb97/results.json)
- [Final static package report](development-attempts/gpt-review-fixes-706a129/final-validation/package/static-20261109T151935696Z-63bc9597/results.json)
- [Companion traversal pre-command save](development-attempts/gpt-review-fixes-706a129/final-validation/suite/run-20261109T151653653Z-0f4ce744/saves/expedition_camp_unrelated_companion_traversal_preserves_active_use_and_low_restore/camp-companion-traversal-before.ddsave)
- [Tactical closure pre-turn save](development-attempts/gpt-review-fixes-706a129/final-validation/suite/run-20261109T151653653Z-0f4ce744/saves/expedition_camp_severe_closure_accepts_tactical_turn_clock_receipt/camp-tactical-closure-before.ddsave)
- [Movement-combat pre-step save](development-attempts/gpt-review-fixes-706a129/final-validation/suite/run-20261109T151653653Z-0f4ce744/saves/expedition_camp_movement_encounter_entry_interrupts_low_and_replays/camp-world-entry-before.ddsave)
- [Concealed camp mid-Watch save](development-attempts/gpt-review-fixes-706a129/final-validation/suite/run-20261109T151653653Z-0f4ce744/saves/expedition_camp_concealed_full_watch_lie_low_saves_replays_and_requires_unbroken_coverage/pressure-concealed-camp-mid-watch.ddsave)

The runner retained compiled assemblies alongside the report in its local run directory; committed acceptance evidence is the reproducible source-hash report, test results, package report and representative save.

## Changed C# files

- `engine/com.decennium.foundation/Laboratory/Model/SharedCraftingConsequences.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedExpeditionPressure.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedExpeditionRouteTravel.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldCommandQueries.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldRangedCombat.cs`
- `engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedExpeditionCampUse.cs` and its Unity `.meta`
- `engine/com.decennium.foundation/Runtime/Core/ExpeditionPressureRecords.cs`
- `engine/com.decennium.foundation/Runtime/Core/ExpeditionCampRecords.cs` and its Unity `.meta`
- `engine/com.decennium.foundation/Runtime/Core/Simulation.cs`
- `engine/com.decennium.foundation/Runtime/Core/WorldActivityRecord.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/ExpeditionPressureCodec.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/ExpeditionCampCodec.cs` and its Unity `.meta`
- `engine/com.decennium.foundation/Runtime/Persistence/SnapshotCodec.cs`
- `engine/com.decennium.foundation/Tests/EditMode/ExpeditionPressureCases.cs`

The exact commit SHA and push URL are added to this packet after commit. The actual GPT response will be recorded separately after review; attempted contact does not count as review.

## Correction source changes

- `engine/com.decennium.foundation/Laboratory/Model/SharedExpeditionCampUse.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldRangedCombat.cs`
- `engine/com.decennium.foundation/Runtime/Core/ExpeditionCampRecords.cs`
- `engine/com.decennium.foundation/Tests/EditMode/ExpeditionPressureCases.cs`

The original GPT hold and its scope are recorded in [GPT_REVIEW.md](GPT_REVIEW.md). It reviewed source and reports but did not run compilation or tests, decode saves, or recompute source hashes. The new baseline reports above independently reproduce each reported failure against reviewed commit `706a1298` using the corrected regression scenarios. The follow-up review of the correction commit is still required.

The tactical-turn scenario also exposed that the shared combat host did not advertise or query `EndRegularTurn`, although its resolver accepted the command. The same revision adds it to the supported-command gate and evaluates it through the existing detached-copy resolver path; the regression now asserts query/execution agreement.

## Remaining limitations and unresolved capability

This is one authored `TEST_ONLY` camp profile. It does not implement general camp construction, storage, perimeter upgrades, off-route camps, dynamic concealment/discovery, production site safety or generalized party/recovery eligibility. The source-contract said guard duty interrupts lying-low, but there is currently no guard-duty C# command or authoritative record to execute that behavior. The implementation supports available interruption authorities—actual combat, route travel, and incompatible work—and leaves guard scheduling/interrupt behavior unsupported for a later mapped dependency. Remaining Pressure causes/reductions and MGT-03 capabilities are not complete.
