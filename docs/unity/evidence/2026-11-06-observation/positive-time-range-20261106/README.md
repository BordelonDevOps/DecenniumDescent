# Observation boundary regression follow-up — 2026-11-06

## Scope

This is a TEST_ONLY acceptance increment after GPT reviewed pushed commit `b36d67ed87ee88038a009c8a5492f3dc4ab01924`. GPT found no blocking semantic or replay defect within the reviewed static, single-mover scope. It suggested two nonblocking coverage additions; both are implemented here. No production resolver, simulation record, command, schema field, save layout, or gameplay rule changed.

The test concerns remain owned by the existing authoritative records: `ActorState`, `WorldTraversalRecord`, `ObserverKnowledgeRecord`, condition journals and their clock, `RuleClock`, and `SnapshotCodec`. The tests call the existing `ObservationRules.ProcessWorldTraversalSegments` procedure through its established test helper and use the versioned observation fixture. Geometry, actor placement, sight range and movement traces are TEST_ONLY facts.

## Runnable acceptance

- `observation_positive_time_moving_observer_loss_survives_boundary_save_and_blocked_remainder` places a stationary target at `(4,4)`, an observer at `(1,0)`, and a sight blocker at `(3,1)`. As the observer traverses to `(2,0)` over one second, sight ends at the exact interior path boundary, parameter `3/5`, at time `3/5`. The test compares a whole traversal with a split at three feet, encodes and restores the partial traversal at the sight-loss boundary, then advances through the wholly blocked remainder. Both paths retain the same complete semantic observer-knowledge set; the target remains currently known because it did not move, and the evidence time remains earlier than the final clock.
- `observation_inclusive_range_boundary_records_sight_then_stales_after_departure` has no blockers and gives the observer an authored five-foot range. A moving target reaches the exact inclusive range boundary at time `1`, where the record is ordinary `DirectSight`. After save/restore, the target moves away from that point and is no longer visible at time `2`; its location becomes stale while the prior `DirectSight` coordinate and time remain. Two identical continuations produce identical bytes.

The geometry-only helper advances each condition journal alongside the test clock so snapshots obey the existing clock invariant. This keeps condition state synchronized in the fixture; it does not alter the production clock path.

## GPT review record

GPT reviewed commit `b36d67ed87ee88038a009c8a5492f3dc4ab01924` and concluded there was no blocking semantic/replay defect. It found the exact interval loop, stationary-target knowledge distinction, versioned fingerprint and authentic schema51 replay consistent with the stated contract. Its nonblocking recommendations were (1) test positive-time sight loss inside an unfinished edge, saved exactly at that boundary with blocked continuation, and (2) test the inclusive range endpoint as ordinary sight before subsequent unseen movement. Those exact cases are the acceptance above. GPT did not run local validation. A follow-up review of this additional test increment is pending.

## Validation

| Check | Result |
| --- | --- |
| Focused positive-time interior-loss case | PASS, 1/1 |
| Focused inclusive-range case | PASS, 1/1 |
| Full C# 9 warnings-as-errors shared-source suite | PASS, 1,184/1,184; Core, Persistence, LabModel and headless tests compiled |
| Static package structure validation | PASS, 18/18; 238 assets and 238 unique GUIDs |
| Unity Editor import/compilation, Edit Mode, Play Mode, game build | NOT RUN |
| `git diff --check` | Run after final documentation/evidence update |

`FULL_TEST_RESULTS.json` contains the full suite output and source hashes. The tested `ObservationCases.cs` SHA-256 is `34fa828a78b088b8d8e78160da388c917787e72bca43bbcf001a18ae9f2213af`. Focused command reports are retained separately.

## Reproduced fixture setup failures

The following failed attempts were reproduced and corrected before the passing runs; none indicated a production observation defect:

- `FAILED_CONDITION_CLOCK.json`: the new time-based fixture updated `RuleClock` without advancing the persisted condition journals, so `SnapshotCodec` rejected the inconsistent snapshot. The helper now appends the existing condition-history clock advance before save/restore.
- `FAILED_CONDITION_ADVANCE_ACCESS.json`: the first correction called `TestOnlyClubAttackPolicy.AdvanceConditions`, an internal LabModel member that is not visible to the separate headless test assembly. The helper now uses the public `ConditionHistory`/`ConditionOperation.Advance` records.
- `FAILED_STALE_OBSERVER_KNOWLEDGE.json`: the fixture moved actors after observation initialization, leaving current-location records for their old positions. It now reinitializes observation after final fixture placement.
