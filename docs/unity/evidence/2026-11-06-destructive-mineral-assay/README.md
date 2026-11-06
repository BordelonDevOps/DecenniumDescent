# Schema46 destructive mineral sample assay

This increment implements a bounded TEST_ONLY destructive assay of one already-existing prepared mineral sample portion. It does not synthesize inventory. `MiningAssaySampleRecord` identifies the real inventory lot and its source/category compatibility; `DestructiveMiningAssayProfileRecord` binds that lot and exact authored amount to one existing WIS/Mining method profile. Schema46 persists sample/profile/attempt data after schema45.

The shared WorkLedger reserves the full sample and worker interval on start. The entire portion is consumed atomically with the first positive credited second. Pause, interruption, save/restore and explicit resume retain the attempt. Pre-work cancellation releases the unused amount; cancellation after work keeps the debit and has no check, refund, finding or labor transfer. The one-minute check uses the existing shared clock, WIS/Mining resolver, deterministic RNG, snapshot transaction, receipts and replay. A successful result returns only its method profile's authored facts.

The pinned source requires a real sample and debit but does not prescribe quantity or debit timing. Codex and **Unity Rules Engine Development** agreed on the provisional prototype policy in [GPT_CONSENSUS.md](GPT_CONSENSUS.md). The exact positive quantity and compatibility are explicit authored fixture data, not source-derived defaults. This fixture accepts a prepared portion; it does not implement sample preparation or residue disposition. See [the decision record](../../MINERAL_ASSAY_RULE_DECISIONS.md) for source, provisional behavior and limits.

## Acceptance

| Check | Result |
| --- | --- |
| `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` | **PASS — 1,154/1,154**, C# 9, warnings as errors |
| `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` | **PASS — 18 checks, 225 assets, 225 unique GUIDs** |

The full result files include source hashes: [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json) and [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). The two new focused cases verify an exact prepared amount, one reservation and one debit, 20-second pause/save/40-second resume, one deterministic resolution, retry blocking after the same evidence/method result, duplicate-command idempotency, pre-work release and post-work nonrefundable cancellation.

During implementation, the first compile attempt exposed cross-assembly access to an internal content key; it was replaced with a public immutable-content comparison. Later compile attempts exposed duplicate local names in sibling command branches; those locals were given distinct names. The final test run compiled and passed all 1,154 cases. These were compile-time implementation defects; no runtime case failed.

## Source scope

The source snapshot is pinned to commit `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Its SHA-256 values and implemented/tested boundaries are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The increment remains partial TEST_ONLY coverage: no production mineral catalog, sample-preparation workflow, residue output, externally authenticated changing-evidence event, assistant work, source-specific tool benefits, general hazard invalidation or remaining MGT-07 procedures.
