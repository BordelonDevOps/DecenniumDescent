# MGT-01 physical storage and transfer — schema71

**Status:** implemented on `Engine`; Codex validation is complete. GPT’s post-implementation review of the exact commit is pending. This is bounded TEST_ONLY content and does not complete MGT-01 or the engine.

## Scope and authoritative records

This increment connects an installed Temporary Camp fitting pack and one ordinary crate to the shared physical inventory model. It reuses `PortableEquipmentRecord` parent/placement links; `ResourceLot` and `InventoryLotRecord` quantities, ancestry, freshness and ownership; `VesselRecord` and `VesselContentRecord`; `WorkLedger` worker intervals and reservations; the completed camp installation claim; shared commands, `RuleClock`, idempotent receipts, snapshot validation and `SnapshotCodec`.

Schema71 adds immutable Core-readable, explicitly fingerprinted `PortableStorageProfileRecord` facts. One resolver supplies compatibility and packed-volume checks to Core validation and LabModel command assessment. It totals nested mass and Load once, checks each physical container's pounds and cubic feet, and requires the fitting-pack root's actual successful installation before deriving the Camp's 20 Load / 200 lb / 20 ft³ storage. The old `FitRuleId`/`FitMemberIds` path remains active for legacy profiles. No item-volume inference, mutable capacity ledger, second inventory ledger, currency, purchase system or production authority was added.

The selected profile volumes and admitted types are TEST_ONLY authored facts, not source-derived dimensions. The exact source revision, blobs, authored profile bounds and agreement limits are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and [the MGT-01 contract](../../MGT01_INVENTORY_STORAGE_RULE_DECISIONS.md).

## Connected acceptance

`mgt01_portable_storage_connected_loop_save_restore_capacity_and_rejections` runs a single coherent route: exploration reaches the existing tactical encounter; the encounter resolves through the current pressure/combat authorities; actual finite cache food and water are acquired; the existing trained crew completes a Temporary Camp; the installed pack is opened and accepts a real full waterskin and food portions; a compatible ordinary crate receives a retrieved portion; restored branches hand over and consume the same provisions; then route travel continues after the companion clears the next mapped route cell.

The case verifies:

- The filled skin stays 1 lb tare plus four pints; together with two pounds of food, the stored subtree is exactly **7 lb / 0.7 Load / 0.22 ft³**, each item counted once.
- Exact Load20 is accepted; Load overflow rejects while weight/volume fit; pounds and volume overflow are checked independently; a cycle is rejected.
- Pre-install, closed, out-of-reach, incompatible, and duplicate-command paths preserve the applicable shared state and receipts.
- Depositing updates subtree custody and linked vessel/lot locations while preserving original owner, food freshness and water provenance.
- Schema71 profiles, nested inventory, active water-fill work and reservations roundtrip; the registered schema70 profile roundtrips with its historical layout.
- Two identical restored management histories produce identical canonical bytes and continue through intake and travel with identical results.
- A separate clock branch completes the same active fill as one 60-second advance or as 30 seconds, disk save/restore, then 30 seconds. Midpoint progress and remaining reservation match; final `RuleClock`, RNG, work lots, output identity and fill state match semantically.

## Changed implementation areas

- Core: immutable storage-profile record, profile fit/volume/capacity validation, Load fallback helper, snapshot field/copy/validation and schema71 gate.
- Persistence: appended schema71 profile-table read/write with schema70 and earlier branches preserved.
- LabModel: TEST_ONLY profile initialization/fingerprint validation; shared destination storage and nested custody/link synchronization; installation movement and exact anchor-claim handling; schema71 composition with route, camp, pressure, combat, repair and query authorities.
- Regression suite: one connected storage case plus registration and optional storage/food-quantity controls in the existing camp-construction fixture.
- Architecture map, MGT-01 contract, handoff and this evidence index.

The exact changed-file list is available in the implementation commit’s Git diff and will be copied into [GPT_REVIEW.md](GPT_REVIEW.md) with the final verdict.

## Validation

| Check | Result | Retained evidence |
| --- | --- | --- |
| Focused connected MGT-01 case | **PASS 1/1** | `development-attempts/run-20261109T213245969Z-2a989213/results.json` |
| Full C# 9 warnings-as-errors suite | **PASS 1,299/1,299**, 270 source hashes; Core, Persistence, LabModel and HeadlessTests compile in the shared-source runner | `final/full-suite-final/run-20261109T213447756Z-bbfbab53/results.json` |
| Standalone C# assembly compilation | **PASS** Core/Persistence/LabModel, 197 source hashes | `final/assemblies/compile-20261109T212235953Z-5879cba0/results.json` and adjacent DLLs |
| Static package structure and GUID checks | **PASS 18/18**, 296 assets / 296 unique GUIDs | `final/package-final/static-20261109T214302316Z-eba6bbb2/results.json` |
| `git diff --check` | **PASS** | No output; rerun before commit |

The full suite first reproduced two schema-compatibility regressions at `final/full-suite/run-20261109T211107164Z-d710d72b/results.json` (1,297/1,299). The legacy split-lot test showed the new profile-only destination assessment intercepted the established exact-member fit path; the schema70 construction test showed the new movement rejection masked its existing durable claim result. The resolver now takes the profile path only for selected profile containers, and the new immovability result applies to the installed MGT fitting-pack root after other live claims are checked. Both tests and the MGT case pass in the final suite. Failed focused compile/runtime attempts remain in `development-attempts/`.

The connected save files from the final full-suite run are:

- `final/full-suite-final/run-20261109T213447756Z-bbfbab53/saves/mgt01_portable_storage_connected_loop_save_restore_capacity_and_rejections/mgt01_portable_storage_nested_work_checkpoint.sav` (32,294 bytes)
- `final/full-suite-final/run-20261109T213447756Z-bbfbab53/saves/mgt01_portable_storage_connected_loop_save_restore_capacity_and_rejections/mgt01_split_fill_halfway.sav` (32,395 bytes)

Each is also recreated by the runnable test. Result files contain the exact source hashes used for each check.

## Limits and checks not performed

Only the selected TEST_ONLY pack, crate, food, waterskin and water profiles have explicit fit/volume facts. Unknown profiles and dimensions remain unsupported. Currency, purchases, general equipment catalog/acquisition, arbitrary multi-container authoring, upgrades/dismantling, autonomous hauling and production storage are not implemented. MGT-01 and the full C# engine remain partial.

Unity import/compilation, Editor tests, Play Mode, standalone game build and observed game runtime were **not run**; Unity gameplay integration remains deferred. GPT’s implementation review has not yet occurred; no successor module is authorized before that actual review resolves concrete blockers and agrees acceptance.
