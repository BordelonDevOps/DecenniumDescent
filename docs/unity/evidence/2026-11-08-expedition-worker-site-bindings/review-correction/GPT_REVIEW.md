# Unity Rules Engine Development review

## Reviewed change

GPT reviewed the pushed worker/site-binding change at [`e0d08014`](https://github.com/BordelonDevOps/DecenniumDescent/commit/e0d08014). GPT inspected the commit and relevant handlers and codec; it did not run validation.

## Confirmed defects and corrections

1. `TestOnlyInventoryPolicy` accepted a configurable `TestOnlyCropPolicy`, but its fingerprint only contained food freshness. An empty save could therefore restore under a different crop-worker eligibility profile. `TestOnlyFillingPolicy` inherited the same omission. The inventory policy now fingerprints nondefault crop configuration; the filling policy hashes its composed custom profile. Both retain their historical default fingerprints. Regression cases reject cross-profile restores and pin the exact default inventory and filling save-byte lengths and SHA-256 hashes.
2. `CampGreens.StartWork` changed a paused task's `WorkerId` to the worker issuing resume. At zero progress, pausing removed the future booking, so a different worker could take over without any recorded labor conflict. Positive-progress takeover was already rejected later by labor-provenance validation, but only as a rollback side effect. Resume now rejects a different worker before booking and keeps the task bound to its original `CropWorkRecord.WorkerId`; `UpdateTask` no longer exposes a worker override. Tests cover zero progress, positive progress, successful original-worker continuation, and save/restore.

Initial regressions reproduced both defects: the configured inventory fingerprints collided, and zero-progress cross-worker resume committed. A first fingerprint correction then exceeded the save-header limit once composed into filling; that failed result is retained as `INTERMEDIATE_FINGERPRINT_LENGTH_FAIL.json`. Hashing the custom filling composition fixed the limit while preserving the original default bytes.

## Scope assessment and next dependency

GPT considered the Camp Greens/mining-only binding boundary sound and found no other confirmed snapshot-layout defect. Rejecting unsupported repair/trap/cache bindings when the opt-in profile is selected is an explicit composition limit, not a regression to legacy behavior. GPT noted that the mining negative case demonstrates the existing occupied-hand check; it does not prove training alone blocks extraction. That is optional follow-up coverage, not a confirmed defect.

GPT's smallest next MGT-02 dependency is to register existing tool-repair assignments through the same worker/site binding profile and delegate to the existing repair handler. Keep carpenter qualification, material settlement, labor, interruption and checks under their existing authorities. Validate the physical site against the repair location and retain the assignment, repair job, structure, physical tools/materials, actor/traversal, `WorkLedger`, clock, RNG and receipts. The suggested connected case pauses repair, saves/restores, resumes the same worker at the bench, completes the existing check, and verifies once-only material settlement and deterministic output while crop work and lead exploration continue. Do not add scheduling, recruitment, automatic travel or started-work reassignment.

## Validation after correction

- Fingerprint regression: 1/1 passed; zero-progress reassignment: 1/1 passed; positive-progress rejection/original-worker resume: 1/1 passed.
- Full C# 9 warnings-as-errors suite: 1,239/1,239 passed.
- Static package checks: 18/18 passed, 271 assets and 271 unique GUIDs.
- Fresh source-binding audit: 4 source snapshots, 17 profiles, 340 RP cells and 4 named tests passed.
- Unity Editor/import checks were not part of this C# correction.

See the preserved reports and updated source-binding manifest in this directory.
