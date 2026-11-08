# Expedition worker and site binding evidence

## Increment

This schema61-layout-unchanged TEST_ONLY increment adds an immutable content profile that binds controlled workers to existing procedures and their physical sites. It composes two existing procedures: Camp Greens crop work at its prepared plot and mineral extraction at the selected deposit. Assignment creation and start both check the same worker/procedure/site binding; physical target identity and coordinates are revalidated from the crop and deposit records.

`ExpeditionWorkAssignmentRecord` remains authoritative for worker, procedure, target, resolved site, status, and linked `WorkId`. `CropPlotRecord`, `CropBatchRecord`, and `CropWorkRecord` remain the crop authorities. `MiningDepositRecord`, `MiningAttemptRecord`, and the mineral unit/lot records remain the mining authorities. Existing actor/traversal state, `SkillTrainingRecord`, hand/equipment checks, `WorkLedger`, inventory custody, `RuleClock`, RNG, command receipts, and procedure resolvers continue to settle work and outcomes. Assignment registration grants no skill, tool, ownership, access, or free hands.

## Connected acceptance

`registered_workers_and_physical_sites_compose_crop_mining_exploration_and_replay` uses a distinct planter and miner at the existing plot and deposit. The lead continues exploring while crop labor and mining are active. A registered worker with no mining-tools training is rejected by the actual mining handler because its existing equipment occupies a hand; the rejection creates no attempt and consumes no mineral. The configured miner retains explicit training and completes extraction through the existing handler. Crop planting pauses after exact input settlement, then two restored simulations resume crop and mining to identical snapshot bytes, RNG state, output custody, and linked work IDs. Forged assignment work, worker, and procedure links fail snapshot validation.

No saved fields, codec branches, or schema migration were added. Existing schemas and the default fixture fingerprints remain unchanged; the opt-in profile changes only that fixture's content fingerprint. Existing supported historical saves remain covered by the full suite.

## Validation

- Focused connected scenario: **1/1 passed** — [FOCUSED_RESULTS.json](FOCUSED_RESULTS.json).
- Full headless C# 9 warnings-as-errors suite: **1,236/1,236 passed** — [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).
- Static package checks: **18/18 passed**, **271 assets / 271 unique GUIDs** — [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- Fresh source-binding audit: **4 exact source snapshots, 17 class profiles, 340 RP cells, 1 named acceptance passed** — [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json).
- `git diff --check`: passed.
- Source and changed-code hashes: [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json), [CHANGED_SOURCE_HASHES.json](CHANGED_SOURCE_HASHES.json).

The initial no-argument source-binding run used the validator's historical schema39 manifest and its archived headless receipt. It stopped on the unchanged `ActorConditionRecord.cs` hash before reaching tests; [RULE_BINDINGS_STALE_DEFAULT.json](RULE_BINDINGS_STALE_DEFAULT.json) preserves that result. The validator was rerun with this increment's fresh manifest and the current full-suite receipt, and passed. No unrelated source pin was refreshed.

## GPT review correction

GPT reviewed commit `e0d08014` and found two concrete issues: standalone inventory/filling fingerprints omitted custom crop-worker configuration, and a zero-progress paused crop task could be resumed by another worker. Both are fixed without a schema or codec change. Default inventory and filling saves retain their historical fingerprints and exact byte hashes; custom inventory/filling configurations now have distinct bounded fingerprints. Crop tasks retain their original worker across pause/resume, and different-worker resume rejects before new labor is booked. The full reports, pre-fix reproductions, and fresh four-test binding audit are preserved in [review-correction](review-correction/README.md). GPT found the crop/mining-only binding boundary sound; its next recommendation is registered tool-repair assignments through the existing handler.

## Limits

The profile currently binds the existing Camp Greens and mining procedures only. The crop handler still requires the prepared plot at `(3,3)`; the mining site comes from the deposit record. Movement remains player-directed. There is no roster acquisition, autonomous route planning, started-work reassignment, general scheduler, or production worker/site authority. Registration does not grant mining qualification or equipment, and the current profile does not generalize binding validation to repair, trap, or cache assignments.
