# MGT-05B bounded implementation corrections

**Status:** GPT accepted the corrected implementation at code commit `9c0a4e92b7f2af8c62c07326934fad7524f64f9c`, with evidence/docs at `6573b7882ee2f9c6323a2de96d95100820e80629`: “No concrete acceptance blocker remains within the agreed bounded schema75 TEST_ONLY contract.” The MGT-05B implementation-review gate is closed. GPT did not select or start a successor module; its separate next-step response is pending. The earlier MGT-05A acceptance remains intact.

## Scope and authority

This is a correction to the already approved schema75 `TEST_ONLY` closed-container preservation slice. It uses the same pinned preservation/spoilage rules from `CRAFTING_HARVEST_PLAYTEST.md` at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `b8adb3ac6eb51f333fdb8f2d68ecc7e9c6511e7ee3aded1bfe54cd4728c93479`, together with the approved [MGT-05B contract](../../../HARVEST_PRESERVATION_TREATMENT_DECISIONS.md). The correction adds no gameplay rule, schema field, inventory authority, clock, mutable cache, or random source.

The exact correction diff from the GPT-reviewed implementation is [MGT05B_CORRECTIONS.patch](MGT05B_CORRECTIONS.patch). The code commit changes three files:

- `HarvestPreservationRules.UnprotectedAgeAt` follows the actual inventory ancestry and stops inheriting a treatment interval at the recorded `CreatedAt` of the first child below the treated lot. A later split of that older branch therefore does not regain protection. A descendant separated from the treated material after protection expires still inherits the interval that material actually experienced.
- Snapshot validation rejects a direct split only when its `CreatedAt` falls inside `[CompletedAt, CompletedAt + 24 hours)`. A split created before treatment no longer invalidates successful completion; the exact expiry instant remains outside the protected interval.
- The treatment fixture now validates supply custody against its physical inventory item and vessel placement. A whole closed-vessel handover may update custodian throughout the contents while preserving inventory ownership, the original worker, and immutable treatment history. Loose fixture supply remains bound to the worker.

## Acceptance evidence

The two new runnable headless regressions cover the returned findings:

- `mgt05b_lineage_cutoff_save_restore_and_replay` harvests and subdivides actual fish material before treatment, saves/restores partial and completed work, and replays the same commands. It verifies that the pre-treatment branch keeps aging, a later child from that branch has the same age/state, and a portion split from the treated lot after expiry inherits the protection interval that lot actually experienced. Inventory quantities are conserved.
- `mgt05b_closed_vessel_handover_preserves_treatment_and_ownership` completes treatment in the sealed vessel, hands the whole vessel to the companion during protection, then verifies synchronized physical custody, unchanged ownership and worker/treatment evidence, unchanged protected age, save/restore and replay. The recipient still cannot open the protected vessel or retrieve its contents.

Both defects were first reproduced against the reviewed commit and retained under `reproduction-lineage/` and `reproduction-handover/`; each returned `InvalidResult`. The corrected focused results are retained under `after-fix-lineage-2/` and `after-fix-handover-3/` and pass **1/1** each.

The complete current C# 9 warnings-as-errors run passes **1,326/1,326** cases, with **282 source hashes** and all four compiled assemblies retained in `final-full/`. It includes all five MGT-05B cases. Static package validation passes **18/18**, with **308 assets**, **308 unique GUIDs**, and **605 file hashes** in `final-package/`. The fresh package report hashes the actual `.meta` sidecars in this checkout: `SharedHarvestPreservationTreatment.cs.meta` (`ffcdf42b…`), `HarvestPreservationTreatmentCodec.cs.meta` (`50c20b47…`), and `HarvestPreservationTreatmentCases.cs.meta` (`22258d8a…`). This replaces the superseded report whose three metadata hashes GPT found mismatched.

Exact report digests, changed source hashes, assembly digests, reproduction results and sidecar hashes are collected in [MGT05B_CORRECTION_BINDINGS.json](MGT05B_CORRECTION_BINDINGS.json). All retained reports are tied to the exact source hashes recorded by the runners.

## Acceptance boundary and remaining limits

This remains a bounded `TEST_ONLY` fish-material and vessel profile. Other materials, general exposure handling, re-treatment, active-protection content splitting, cancellation settlement, recipes and production authority remain unsupported. No Unity import or compilation, Editor tests, Play Mode, player build, or observed game runtime was performed.

This acceptance covers only the bounded schema75 TEST_ONLY slice. GPT's next-dependency recommendation must be reconciled with the implementation map before another module starts. The engine remains incomplete.
