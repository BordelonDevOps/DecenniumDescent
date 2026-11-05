# Schema38 fishing stock manifests and Trap lifecycle

**Branch:** `Engine` (working tree; uncommitted)  
**Pinned source revision:** `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`  
**Authority:** reviewed operational PLAYTEST source, exercised only through explicit TEST_ONLY content.

## What this increment adds

Schema38 appends two authoritative runtime record types to the schema37 physical Trap loop:

- `FishingStockManifestRecord` stores a shared-stock identity, stock version, effective interval and the sorted IDs of actual physical members.
- `FishingStockAllocationRecord` binds an opportunity to an explicit subset of those members. A whole-pool allocation must list the entire manifest.

Validation requires each candidate to belong to its allocation and version, requires overlapping versions of the same shared pool to agree on physical membership, and checks that the version applied at setup completion. The existing single-body response lock continues to prevent distinct opportunity or version labels from allocating the same creature twice.

The TEST_ONLY witness covers two overlapping allocations over the same fish and two disjoint singleton allocations over two actual fish. Save/restore retains the sorted membership records. Schemas35–37 retain their historical wire layouts. The fixture still uses one preselected candidate per opportunity and does not claim to implement multi-candidate weighting or general cross-site route reachability.

The unattended Trap loop remains covered through setup, bait/opportunity commitment, scheduled check, same-body capture, and five-minute retrieval into a supported receiver. Another capable worker can retrieve; paused work and receiver reservation persist through save/restore. Exact check/retrieval ties resolve the scheduled check first. Early retrieval avoids a roll without refunding spent inputs.

See [FISHING_TRAP_RULE_DECISIONS.md](../../FISHING_TRAP_RULE_DECISIONS.md) for source, fixture and unfinished-scope boundaries.

## Verification

- [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json): **1,100/1,100** deterministic cases passed, including 17 named fishing regressions.
- [COMPILE_RESULTS.json](COMPILE_RESULTS.json): Core, Persistence and LabModel compile under C# 9 with warnings as errors.
- [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json): **14/14** static package checks passed.
- [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) pins source snapshots and binds implementation files to named tests; the focused validator result is [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json).
- Unity import/compiler, Edit Mode, Play Mode, player build, historical-release byte comparison and gameplay qualification were **not run**.
