# MGT-03 camp use and Pressure — schema69 evidence

**Status:** implementation is complete for the agreed bounded TEST_ONLY slice. This packet is awaiting GPT's post-implementation review. Do not treat it as acceptance of all MGT-03 or engine completion.

## Agreed scope and authorities

The slice connects FL-07 actual camp use to FL-08 Pressure using an authored fixed TEST_ONLY camp site at one existing route checkpoint. It uses existing route travel/spatial records and `WorldPositionResolver`, committed commands/receipts, `RuleClock`, `WorkLedger`, active cohort/exposure, typed Pressure changes/checkpoints, deterministic RNG, encounters/consequences, snapshot validation and persistence. New schema69 state is limited to camp profile/use/lying-low history and checkpoint context. Existing schema67/68 behavior and serialized layouts remain in their earlier branches.

Codex/GPT's pre-implementation contract and pinned source references are in [CAMP_USE_PRESSURE_RULE_DECISIONS.md](../../CAMP_USE_PRESSURE_RULE_DECISIONS.md). The map and architecture trace are in [IMPLEMENTATION_TRACE.md](../../IMPLEMENTATION_TRACE.md#2026-11-09--mgt-03-camp-use-and-pressure-schema69-test_only), and the current checkpoint is in [DEVELOPMENT_HANDOFF.md](../../DEVELOPMENT_HANDOFF.md).

## Connected acceptance

The full suite's four camp-specific cases all pass:

- `expedition_camp_known_use_and_actual_combat_are_distinct_pressure_categories`: repeated camp use deduplicates within the category; actual combat is separately counted; Severe closure uses actual retreat.
- `expedition_camp_exposed_pressure_context_and_companion_farming_connect`: exposed camp creates the agreed Pressure/context; companion Camp Greens work progresses independently during obstruction.
- `expedition_camp_early_haven_uses_route_context_and_does_not_settle_twice`: an earlier Haven checkpoint retains its established context and does not reroll or settle twice.
- `expedition_camp_concealed_full_watch_lie_low_saves_replays_and_requires_unbroken_coverage`: full concealed Watch grants one shared-cap reduction; an exact closing boundary is credited to the just-completed Watch; interrupted/partial intervals grant none; mid-Watch save/restore and command replay match; one clock command crossing multiple Watches remains deterministic; lying-low grants no Rest record.

## Validation (exact candidate source)

- Full C# 9 warnings-as-errors suite: **PASS, 1,286/1,286**, zero failures; 264 source hashes; `coreCompilation=PASS`.
- Standalone C# compilation: **PASS**, Core, Persistence and LabModel, warnings as errors.
- Static package structure validation: **PASS, 18/18** checks. This is not Unity import/compilation.
- Unity Editor import/compile, Edit Mode, Play Mode, standalone/player build and observed gameplay: **NOT RUN** (outside this increment and Unity integration remains deferred).

Retained reports and the scenario save:

- [Full suite report](development-attempts/commit-candidate/full-suite/run-20261109T135821463Z-f573c206/results.json)
- [Standalone compile report](development-attempts/commit-candidate/compile/compile-20261109T135821582Z-419c6af1/results.json)
- [Static package report](development-attempts/commit-candidate/package-validation/static-20261109T140441540Z-d66b9cff/results.json)
- [Concealed camp mid-Watch save](development-attempts/commit-candidate/full-suite/run-20261109T135821463Z-f573c206/saves/expedition_camp_concealed_full_watch_lie_low_saves_replays_and_requires_unbroken_coverage/pressure-concealed-camp-mid-watch.ddsave)

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

## Remaining limitations and unresolved capability

This is one authored `TEST_ONLY` camp profile. It does not implement general camp construction, storage, perimeter upgrades, off-route camps, dynamic concealment/discovery, production site safety or generalized party/recovery eligibility. The source-contract said guard duty interrupts lying-low, but there is currently no guard-duty C# command or authoritative record to execute that behavior. The implementation supports available interruption authorities—actual combat, route travel, and incompatible work—and leaves guard scheduling/interrupt behavior unsupported for a later mapped dependency. Remaining Pressure causes/reductions and MGT-03 capabilities are not complete.
