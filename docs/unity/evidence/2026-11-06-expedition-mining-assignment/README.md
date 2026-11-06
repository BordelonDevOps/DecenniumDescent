# Schema47 expedition assignment to mining extraction

This increment composes the existing persisted expedition assignment flow with the existing exposed mineral extraction procedure. A companion receives an assignment to a versioned deposit and an explicit extraction selection, travels through the shared exploration movement commands, and starts extraction only after reaching the deposit's derived work site. The start operation delegates to the existing mining resolver; it adds no second mining scheduler or settlement path.

## Responsibilities and authoritative state

- `ExpeditionWorkAssignmentRecord` owns the assigned worker, procedure, target, derived site, travel/readiness state, selected mining choices, and the link to the started job.
- `MiningAttemptRecord`, the selected `MiningMaterialUnitRecord` records, `WorkLedger`, and resulting inventory records remain authoritative for extraction access, work, claims, check, and output.
- Existing traversal, `RuleClock`, deterministic RNG, command receipts, replay protection, and snapshot codecs provide execution and persistence.

The selected deposit supplies the site and version. The assignment request cannot override them. Mining qualification, tools, hands, stock, receiver fit, and other procedure checks are revalidated by the existing mining handler at start.

## Acceptance

| Check | Result |
| --- | --- |
| Focused `expedition_assignment_travels_to_mine_and_dispatches_shared_extraction` | **PASS — 1/1** |
| `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` | **PASS — 1,159/1,159**, C# 9 warnings as errors |
| `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` | **PASS — 18 checks, 225 package assets, 225 unique GUIDs** |

The scenario assigns a companion two cardinal steps from a fixture deposit, saves and restores partial travel, reaches the deposit, starts extraction, saves and restores the in-progress attempt, completes the deterministic successful extraction into the existing receiver, and replays the original assignment without changing settled state. Full result files include the exact tested source hashes: [headless results](HEADLESS_RESULTS.json) and [package results](PACKAGE_RESULTS.json). The focused source-binding check verifies all three pinned Git blob IDs and SHA-256 values, 11 implementation paths and the named passing test: [binding validation](SOURCE_BINDINGS_VALIDATION.json).

The initial focused run failed at assignment start because `AssessMiningCommand` accepted schema43 only. Schema47 carries the same mining records, so the resolver now accepts schema43 and later schemas. The focused run and full suite pass after that correction.

## Source scope and limits

The source snapshots are pinned to `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; exact Git blob IDs and SHA-256 hashes are listed in [source bindings](SOURCE_BINDINGS.json). No new gameplay timing or balance rule is introduced here. The assignment integration reuses the existing FL-01–03 site-aware assignment policy and the selected exposed-mineral extraction profile.

This is bounded TEST_ONLY composition with one authored deposit and one assigned worker. Travel remains player-directed. The increment does not add automatic route planning, general site discovery, assistant bonuses, concurrent multiworker mining, production site authority, or general assignment command discovery. It does not validate engine completeness or gameplay balance.
