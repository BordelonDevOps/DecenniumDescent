# Schema57 buried-cache excavation evidence

This packet records one bounded TEST_ONLY procedure on the `Engine` branch. It does not mark the complete gameplay simulation finished or promote this fixture to release content.

## Source and implementation

The shovel is the reviewed PLAYTEST candidate at pinned revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, path `DescentReviewChanges/ReviewBible/data/playtest/equipment_acquisition_candidate.json`, blob `afd06198e19409385408ac258be7dc1d0b2600fb`, pointer `/items/146`. The extracted item binds the `adventuring-gear.shovel` identity and its five-pound source and operational weight. See [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and the [pinned item snapshot](sources/equipment-acquisition-shovel-item-146.json).

The 300 active-second safe-site procedure and one-time exposure are provisional prototype decisions, not rules recovered from the source. `BuriedCacheSiteRecord` binds the existing cache, site and shovel. `CacheExcavationRecord` preserves its assignment, worker, timestamps, exact earned work and status. Shared `RuleClock`, `WorkLedger`, activity projection, portable-equipment claim, command transaction, snapshot codec and supply-cache/inventory handlers remain the authorities. Schema57 appends opt-in records and preserves earlier snapshot layouts.

## Runnable acceptance

- `cache_excavation_assignment_resumes_exact_work_and_exposes_cache_once`: travel, hidden-cache gating, 100 seconds of work, rejection of forged paused progress by canonical command replay, pause/save/restore, no paused progress, exact 199+1 completion, one-time exposure, and ordinary unlock/open/retrieve with finite stock lineage preserved.
- `cache_excavation_requires_assignment_site_and_can_only_be_started_once`: target/site readiness and duplicate-start rejection.
- `content_manifest_buried_cache_profile_pins_actual_shovel_without_rebinding_legacy`: shovel source binding and legacy content-manifest selection.

The three individual reports are retained in [focused](focused/).

An adversarial progress edit first surfaced `InvalidSharedWorldReplay`. The shared-world validator replays persisted command receipts and compares the canonical snapshot for every subsystem, so changing saved work without matching command history is already rejected. The final regression asserts that existing integrity boundary; no duplicate progress ledger or alternate credit authority was added. The investigation is documented in [INVARIANT_INVESTIGATION.md](INVARIANT_INVESTIGATION.md), with the two diagnostic reports in [investigation](investigation/).

## Validation

- **C# 9 warnings-as-errors headless suite: PASS, 1,208/1,208.** It compiled the shared C# sources with Roslyn and ran the headless cases. See [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json).
- **Static package validation: PASS, 18/18 checks, 257 package assets and 257 unique GUIDs.** This validates package structure and dependency rules; it is not Unity import, Editor compilation, player-build or gameplay qualification. See [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- `git diff --check` passed after the code, documentation and evidence updates.

## Review and limits

[GPT's review receipt](GPT_REVIEW.md) records its agreement on pause/resume invariants and its limits. The optional competing-worker regression was not added because the current cache-only fixture has no second worker-consuming procedure; the implementation checks active worker intervals/projected jobs and shared command execution is candidate-copy/validate/commit atomic.

The fixture supports one authored buried cache, one shovel and one open excavation. It does not provide variable geology, hazards, structural support, arbitrary terrain changes, generated stock, multi-worker labor, cancellation or production content selection. Unity integration was not performed.
