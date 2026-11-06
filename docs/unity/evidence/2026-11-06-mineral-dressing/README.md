# Schema48 mundane mineral dressing

Schema48 adds the source-defined ten-minute no-roll dressing operation for one already-extracted ordinary mineral unit up to 1 lb. It uses the shared `RuleClock`, worker intervals, WorkLedger reservation, inventory ancestry, portable-item identity, command query/discovery, snapshot codec and replay path. No independent clock, inventory, scheduler or RNG was added.

## Responsibilities and authoritative state

- `MineralPreparationProfileRecord` is explicit TEST_ONLY content binding a unit to measured gangue waste and retained mass plus the two physical presentation profiles. No mass-loss rate is inferred.
- `MineralPreparationAttemptRecord` owns the worker, input, profile, exact active work, status and output lot identities. The `WorkLedger` owns active labor and the whole-input claim.
- The original `MiningMaterialUnitRecord` remains the ingredient identity and retains its original mass, value, category and condition. Inventory lineage records the original lot as the parent, the dressed retained mineral as a child, and any measured gangue as another child.
- The retained item remains in the existing authored receiver; gangue is represented as a physical ground lot at the worksite. The source lot is reduced to zero only after the reservation is released and the children are created atomically.

## Source application and fixture boundary

The pinned mining guide supplies ten active minutes, no roll, compatible Miner's tools, two hands, a capable worker, a stable accessible surface, and an ordinary unit or predeclared portion no heavier than 1 lb. It requires the actual removed waste and retained mass to be recorded. This schema supports whole extracted units only. Profiles carry an explicit measured waste amount; retained mass is the exact conserved remainder. There is no value, tier, grade, condition, freshness or ingredient-identity transformation.

The TEST_ONLY fixture locates the open receiver, selected extracted unit and stable authored surface at the same worksite. It does not model lifting the unit onto a surface or general surface placement. General item-on-surface geometry, portions, exceptional/incompatible material, and recipe-integrated dressing during extraction remain unsupported. The schema does not add a cancellation command; a worker may pause and resume while the claim remains reserved.

## Acceptance

| Check | Result |
| --- | --- |
| Focused `mineral_preparation_conserves_measured_mass_and_resumes_after_save` | **PASS — 1/1** |
| `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` | **PASS — 1,160/1,160**, C# 9 warnings as errors |
| `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` | **PASS — 18 checks, 225 assets, 225 unique GUIDs** |
| `git -c core.whitespace=cr-at-eol diff --check` | **PASS** |

The scenario first extracts one unit, verifies rejection before extraction and for an unprofiled unit, starts the operation, saves and restores at 200 seconds, pauses and resumes with the full input still reserved, and finishes the remaining 400 seconds. It verifies the exact 1.0 = 0.9 retained + 0.1 gangue split, physical receiver/ground custody, unchanged source facts and RNG, complete save/restore and duplicate-command idempotency. Reports and tested source hashes are [focused](FOCUSED_RESULTS.json), [full suite](HEADLESS_RESULTS.json), and [static package](PACKAGE_RESULTS.json).

The first focused run exposed that `SupportsCommand` filtered out the new preparation options despite the resolver being present. The query policy now recognizes all three start/pause/resume command kinds; the focused case and complete suite pass after that fix.

## Source scope and limits

The rule snapshots are pinned to `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Git blob IDs, SHA-256 values, implementation paths and the named acceptance case are in [source bindings](SOURCE_BINDINGS.json) and [binding validation](SOURCE_BINDINGS_VALIDATION.json). This remains TEST_ONLY work and does not imply production content or release approval.
