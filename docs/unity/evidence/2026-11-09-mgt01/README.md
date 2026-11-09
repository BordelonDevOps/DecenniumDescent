# MGT-01 physical storage and transfer — schema71

**Status:** GPT accepted corrected exact commit `bac0969ab2a376638c4cfc56e3fe3fa93953ead4` with no remaining concrete blocker. The bounded TEST_ONLY slice does not complete MGT-01 or the engine. GPT recommends MGT-04 next, beginning with source-contract review; the handoff records the verified mapped dependencies.

## Scope and authorities

The mapped increment connects an installed Temporary Camp fitting pack and one ordinary crate to the existing physical inventory model. It reuses `PortableEquipmentRecord` parent/placement links; `ResourceLot` and `InventoryLotRecord` quantity, ancestry, freshness and ownership; `VesselRecord` and `VesselContentRecord`; `WorkLedger` intervals/reservations; the completed camp installation claim; shared commands, `RuleClock`, receipts, snapshot validation and `SnapshotCodec`.

Schema71 stores immutable Core-readable storage-profile facts. One resolver serves query, execution and validation. It enforces profile fit and explicit packed volume, counts nested mass/Load once, checks pounds/Load/volume independently, and derives Temporary Camp capacity only from successful installation. Legacy `FitRuleId`/`FitMemberIds` behavior and the schema70 wire layout remain. The crate’s authored identity, owner, profile, mass and capacity remain fixed; its placement and actor custodian may change through existing portable handling. The stored profile dimensions and admissions remain TEST_ONLY, not source-derived facts.

Pinned source revision, blob identities, TEST_ONLY profile quantities and consensus boundaries are recorded in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The implementation contract is [MGT01_INVENTORY_STORAGE_RULE_DECISIONS.md](../../MGT01_INVENTORY_STORAGE_RULE_DECISIONS.md).

## Connected acceptance

`mgt01_portable_storage_connected_loop_save_restore_capacity_and_rejections` runs: route exploration → existing tactical encounter → finite cache food/water acquisition → the existing Temporary Camp construction task → filled waterskin and food management in installed storage → ordinary crate transfer → intake → continued route travel.

The case now verifies:

- Food plus a full physical skin is exactly **7 lb / 0.7 Load / 0.22 ft³**, counted once. Exact Load20 passes; weight, Load and volume overflows fail independently; unknown fit, incompatible type, cycles, pre-install storage, closed access and out-of-reach storage reject.
- An adjacent companion opens and closes the installed ground container without changing its coordinates, installation claim or synchronized lot location.
- The ordinary crate is picked up, handed over, saved/restored, and dropped through the shared resolver. Query and execution agree; contents and ownership persist; custody and burden transfer correctly; identical restored drop histories produce identical bytes.
- Deposits and retrieval preserve owner, ancestry, freshness, water source/content and synchronized vessel/lot custody/location. Duplicate commands remain idempotent.
- Active water-fill progress and reservations survive save/restore. An uninterrupted 60-second completion equals 30 seconds, disk save/restore, then 30 seconds in clock, RNG, work lots, output identity and fill semantics.
- Authentic paused schema70 bytes from the pre-storage Engine tree decode and re-encode byte-for-byte with current code, restore under schema70 policy, and resume to camp installation in two deterministic branches.

## GPT’s first implementation review

GPT reviewed initial commit `bb4832e23b26a3f71b41bc14be627e22c390ad17` and **held acceptance** for three concrete gaps: the crate validator rejected valid pickup/handover after query admission; adjacent Open/Close could relocate a ground container to the actor; and the historical test generated fresh schema70 bytes instead of testing a real pre-change save. GPT found the source-bound capacity and schema layout otherwise consistent. Its actual response, exact requests and checks it did not independently perform are in [GPT_REVIEW.md](GPT_REVIEW.md).

Corrections were committed and pushed as `bac0969ab2a376638c4cfc56e3fe3fa93953ead4`. GPT reviewed that exact commit and accepted the bounded module. Its actual verdict, inspected paths and unrun checks are recorded in [GPT_REVIEW.md](GPT_REVIEW.md).

## Historical schema70 evidence

The original paused construction save is retained at [schema70-pre-mgt01-paused-camp-construction.ddsave](fixtures/schema70-pre-mgt01-paused-camp-construction.ddsave). It is the tracked save from the pre-storage Engine tree (`37846f90e824128c4a96380dcc0969ac6edaf32d`), original source commit `ae61cd16bc1c5ec88bc1a558696f71f7245e2188`, Git blob `fd8b7d94d9061736dd40f760a4356d4828836e7e`, SHA-256 `5ef2f86460fd7af4daf8faf0d4651ec85bf6ca102e1b22081862dd748bc71214`. Its exact bytes are SHA-pinned in `PortableStorageHistoricalSchema70Cases.cs`. The current-code re-encoded file matches the source hash; the continued save contains the resolved installation.

## Validation

| Check | Result | Retained evidence |
| --- | --- | --- |
| Focused connected MGT-01 case | **PASS 1/1**, 271 source hashes; Core/Persistence/LabModel/HeadlessTests compile in the shared-source runner | `final/review-fixes-final/focused/run-20261109T223329806Z-0dae20d5/results.json` |
| Full C# 9 warnings-as-errors suite | **PASS 1,299/1,299**, zero failures, 271 source hashes | `final/review-fixes-final/full-suite/run-20261109T223711542Z-34c7ff34/results.json` |
| Standalone C# assembly compilation | **PASS** Core/Persistence/LabModel, 197 source hashes | `final/review-fixes-final/assemblies/compile-20261109T224234881Z-36564b63/results.json` |
| Static package structure/GUID checks | **PASS 18/18**, 297 assets / 297 unique GUIDs | `final/review-fixes-final/package/static-20261109T224254550Z-09ee053e/results.json` |
| `git diff --check` | **PASS** after the final documentation update, before commit | Current correction candidate |

The final full-suite run retains the connected saves:

- `mgt01_crate_handover_checkpoint.sav` (32,473 bytes)
- `mgt01_portable_storage_nested_work_checkpoint.sav` (32,294 bytes)
- `mgt01_split_fill_halfway.sav` (32,395 bytes)
- `mgt01_schema70_pre_storage_source.sav` and `mgt01_schema70_current_reencoded.sav` (13,546 bytes each; identical hashes)
- `mgt01_schema70_current_continuation.sav` (14,396 bytes)

All are under `final/review-fixes-final/full-suite/run-20261109T223711542Z-34c7ff34/saves/mgt01_portable_storage_connected_loop_save_restore_capacity_and_rejections/` and are regenerated by the runnable case.

### Failed attempts and causes

- The first correction compile failed because the new assertion passed nullable `BurdenTotals.Pounds`/`Load` values to `RuleQuantity.Sum`. The record’s nullable contract was inspected; the assertion now verifies known values and sums `.Value`. Report: `development-attempts/review-fixes/run-20261109T220929276Z-c36db10b/results.json`.
- Git’s staged whitespace check initially flagged every line in the four newly generated validation JSON reports because PowerShell wrote CRLF endings. The JSON content parsed correctly; those report files were normalized to LF and reparsed before the staged check was rerun.
- The first runtime regression attempted adjacent Open/Close in the main connected action stream; those extra one-second actions consumed the companion’s off-calendar action slot and caused a later stow query to reject with `OffCalendarActionAlreadySpent`. The interaction regression now uses an isolated restore branch so it tests stationary coordinates without perturbing the main scenario. Reports: `development-attempts/review-fixes/run-20261109T221107382Z-1682e226/results.json` and `run-20261109T221235107Z-1af195c3/results.json`.
- Before MGT-01 corrections, the schema71 full suite also reproduced two compatibility failures at `final/full-suite/run-20261109T211107164Z-d710d72b/results.json` (1,297/1,299). The legacy split-lot path and schema70 construction claim-reason ordering were corrected and pass in the final full suite.

## Limits and checks not performed

Only the selected TEST_ONLY camp pack, crate, food, waterskin and water profiles have explicit fit/volume facts. Unknown profiles and dimensions remain unsupported. Currency, purchases, general equipment catalog/acquisition, arbitrary multi-container authoring, upgrades/dismantling, autonomous hauling and production storage remain incomplete. MGT-01 and the full engine are not complete.

Unity import/compilation, Editor tests, Play Mode, standalone game build and observed game runtime were **not run**; Unity gameplay integration remains deferred. GPT did not independently compile, execute C# tests, decode/replay saves, recompute source hashes or run Unity. GPT accepted the corrected exact commit; its next-dependency recommendation is MGT-04 source-contract review, not engine completion.
