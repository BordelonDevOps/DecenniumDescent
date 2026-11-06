# Legal tactical Hide through exploration — 2026-11-06

## Scope

This schema51 increment adds exact visibility-loss boundary semantics to the TEST_ONLY moving-target observation path, plus a connected acceptance trace. The `ObserverKnowledgeRecord` layout and schema51 serialization are unchanged; `DirectSightLimit=4` is appended to the existing evidence enum and stored in its existing integer field. Existing evidence values remain stable. The observation implementation is in the TEST_ONLY LabModel; no production game resolver or new snapshot field was added.

- Responsibilities exercised: tactical Hide, per-observer Hidden state, shared encounter resolution/exit, exact moving-target visibility intervals and loss boundary, world traversal, save/restore, deterministic replay.
- Authoritative records: `ActorState` and `WorldTraversalRecord` for position/progress; `ConditionJournal` for the explicitly authored Blinded event; `ObservationActionRecord`, `ObservationHideResultRecord`, and `ObserverKnowledgeRecord` for Hide and observer-specific information; existing encounter, initiative, Action/Reaction, command receipt, clock and RNG records for combat/time/execution.
- Dependencies: the shared `Simulation` command path; `ObservationRules.Refresh` on successful commands and world advancement; `ProcessWorldTraversalSegments`; `EndFixedEncounter`; `SnapshotCodec`; existing connected-combat and world-movement fixtures.
- Rule boundary: the exact excluded sight-loss representation is a Codex/GPT consensus completion of the prototype observation contract. Interval midpoints classify visibility only. An exposed interval clears Hidden for its observer; when sight ends at a closed blocker boundary, that exact limit coordinate/time is recorded with `DirectSightLimit`, current-location knowledge false, and no claim that the blocked boundary itself was seen. The planar map, sight profiles, seed, opponent's Blinded condition, perimeter route, and combat statistics are named TEST_ONLY facts. Fixed-target sight updates while the observer moves still use the old sample path. Attack-evidence semantics, hearing, other Invisible episode edges, and reaction-specific observation remain open.

## Runnable acceptance

Case: `observation_tactical_hide_survives_exit_then_legal_exploration_sighting_is_observer_specific` in `engine/com.decennium.foundation/Tests/EditMode/ObservationCases.cs`.

The trace legally moves the hero to a covered world anchor, begins a fixed encounter, performs Hide against two observers, and saves/restores. A blinded fixture opponent takes legal tactical steps around the authored blockers until it is adjacent; the hero resolves the encounter, and `EndFixedEncounter` returns control to shared exploration. The hider begins a legal world step, and three branches exercise a single uninterrupted one-second advance, a quarter/three-quarter split with save/restore at 1.25 feet, and a split/save exactly at the visibility-entry boundary. All finish with the same excluded sight-loss position/time and `DirectSightLimit`, despite different command partitions. The partial branch verifies the companion's exact direct-sight position while currently visible; the boundary branch confirms the boundary itself fails sight and an interior point on its visible side passes. Only the companion clears Hidden; the second observer's knowledge remains byte-for-byte unchanged. Each saved trace round-trips, and repeated execution from identical encounter bytes produces identical final snapshot bytes.

The assertion does not use a direct call to `ProcessWorldTraversalSegments`: all movement is submitted through `BeginWorldStep` and `AdvanceClock`. The prior processor-seam regression remains to isolate its two-observer transition behavior.

## Validation

| Check | Result |
| --- | --- |
| Legal Hide/exit acceptance | PASS, 1/1 (`run-20261106T213638427Z-8405fa03`) |
| Existing traversal boundary acceptance | PASS, 1/1 (`run-20261106T213638400Z-7c58b360`) |
| Full C# 9 warnings-as-errors suite | PASS, 1,179/1,179; Core, Persistence, LabModel and headless test sources compiled |
| Static package validation | PASS, 18/18 checks; 237 assets and 237 unique GUIDs |
| Unity import, Editor tests, player build, runtime or gameplay qualification | NOT RUN; C#-first phase remains active |
| `git diff --check` | PASS after the final documentation/evidence updates |

Final runner reports are retained in `FOCUSED_RESULTS.json`, `BOUNDARY_TRAVERSAL_RESULTS.json`, `FULL_TEST_RESULTS.json`, and `PACKAGE_RESULTS.json`. Source hash inventories are embedded in the C# runner reports. Changed source SHA-256:

```text
FEE16DBE1C9C1C5EA7E2743DD4FAD7B7695FA6E8AF16FAF964B31A21ED162EFA  engine/com.decennium.foundation/Runtime/Core/ObservationRecords.cs
7E93A6928917886954EB8133FB4FC3CB516B51EC2FE42974FE9F09D0062ADEF7  engine/com.decennium.foundation/Laboratory/Model/ObservationRules.cs
2BF1EA4CA33A1AE72CAC9BD51DA40EB763E50A34BF8DA93AF19591D3D47AE6A1  engine/com.decennium.foundation/Tests/EditMode/ObservationCases.cs
```

## Diagnosed test-fixture failure

The initial Hide/exit focused runs failed with `UnknownConditionEvent`. The condition handler requires both the event ID and command actor to match the authored `ConditionFixtureEvent.Target`; the test had used the helper's default hero actor while the event targeted the opponent. An unchanged rerun reproduced it. The command now dispatches as `AdditionalTacticalActor.Id`; this was fixture construction, not a simulation defect. Reports remain in `FAILED_UNKNOWN_CONDITION_EVENT.json` and `FAILED_REPRODUCTION.json`.

After exact sight-loss semantics were added, the full suite first failed **1,178/1,179** in the earlier traversal acceptance. An unchanged full rerun reproduced the same assertion. It expected a fractional interior sample (`DirectSight`), while the new agreed semantics correctly returned the excluded endpoint boundary `(2,0)` at time `2` as `DirectSightLimit`; the test was updated to assert that exact fixture boundary. Its subsequent focused run confirmed those values, and both changed cases plus the final full suite passed. The failed suite, unchanged reproduction and boundary diagnostic are retained as `FAILED_PARTITION_EXPECTATION.json`, `FAILED_PARTITION_REPRODUCTION.json`, and `FAILED_BOUNDARY_DIAGNOSTIC.json`.

## GPT review

The initial review packet was sent to **Unity Rules Engine Development** with the exact algorithm excerpt, test scenarios, and local result identifiers. GPT identified two gaps: the fixed-target observer-motion path still sampled sight, and a newer algorithm could fail authentic schema51 receipt replay. GPT did not run local checks. Both findings are addressed by the versioned, bidirectional follow-up in [exact-path evidence](../exact-partition-20261106/README.md); its independent review is tracked there.
