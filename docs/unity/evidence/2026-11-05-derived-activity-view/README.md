# Derived active-work view — 2026-11-05

## Scope

This increment extends the existing, transient `WorldActivityProjection` over active procedure records. It reports the record's status, progress values that are explicitly stored, worker intervals and resource reservations linked by the procedure ID, the nearest future linked interval boundary, and admissible procedure controls supplied by same-revision command discovery.

The identity-only `CurrentWork(snapshot)` path remains the path used for labor-conflict checks and retains its domain ordering. The enriched overload does not mutate simulation state or add a save field/schema. Procedure handlers remain responsible for actual pause, resume, cancel and settlement behavior.

Fishing-trap setup and retrieval controls are represented by existing `Interact` commands whose target is the physical Trap ID. The TEST_ONLY query path now discovers and purely assesses their existing Pause/Resume/Cancel operations; the read model links them to the procedure row using the Trap ID stored in that procedure record. Query and execution both report a spent off-calendar Dash before the exploration-only restriction. Execution still uses the existing Trap resolver. No gameplay rule was added.

## Limits

The richer projection currently includes working procedure records only. Paused and awaiting-choice rows, passive intervals, and traversal have not been added. It exposes only claims present in `WorkLedger` and progress/boundaries represented by the source records; it does not create universal status, progress-total, claim, or cancellation models. The fishing-trap query extension is limited to the existing TEST_ONLY fixture handlers.

## Validation

- `shared_world_data_defined_handlers_run_two_distinct_configurations`: **1/1 passed**.
- `fishing_trap_setup_pause_resume_and_save_replay`: **1/1 passed**.
- `fishing_trap_retrieval_moves_the_same_catch_after_saved_partial_work`: **1/1 passed**.
- `fishing_trap_resume_query_matches_off_calendar_action_gate`: **1/1 passed**.
- Full deterministic suite: **1,118/1,126**; C# 9 warnings-as-errors compilation **passed**. The eight failures have the same names and `HarvestValidation` exception as the earlier **1,115/1,123** baseline in [the Prowl/OpenRA checkpoint](../2026-11-05-prowl-openra-extraction/BASELINE_RESULTS.json). The changed shared-world and Trap cases pass.
- Static package checks: **14/14 passed**.

The result JSON files contain source hashes, individual case outcomes, and package-check details. The full-suite failures remain visible in the receipt; this increment did not change them.
