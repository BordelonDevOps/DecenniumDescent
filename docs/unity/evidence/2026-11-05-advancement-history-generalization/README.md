# Advancement history generalization checkpoint

**Status: partial, TEST_ONLY, source-bound, and provisional.** This checkpoint extends structural validation for the existing schema30 Soldier advancement ledger. It does not enable the level 3 advancement command or make the level 3 cards executable.

## Change

- Added stable C# IDs for Soldier `Command Step`, `Tactical Assessment`, and `Suppression Fire`.
- Generalized schema30 validation to check the level 2 result and the two source-legal level 3 pairs, fixed-average d10 HP capacity, current-HP clamp, feature-grant linkage, and chronological event sequence from the level 1 fixture.
- The advancement write path retains an existing feature runtime record when refreshing the shared Bonus Action value, so it preserves prior per-feature Recharge state. The current level-3 runtime gate means this branch is not yet exercised by an end-to-end level-up.
- Added a deterministic structural regression that constructs a valid synthetic Soldier 1→2→3 history, accepts each agreed level 3 pair independently, and rejects an invalid pair. This is not an end-to-end runtime level-up.

## Source and verification

The level 3 schedule and option identities are pinned in the [catalog source bindings](../2026-11-04-character-advancement-catalog/SOURCE_BINDINGS.json); GPT/Codex consensus completions are recorded in [SOLDIER_LEVEL3_RULE_DECISIONS.md](../../SOLDIER_LEVEL3_RULE_DECISIONS.md). The catalog projection validator passed. The headless C# 9 regression runner passed **1,069/1,069** cases and static package validation passed **14/14** checks. Exact outputs and implementation hashes are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json), [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json), [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json), and [CATALOG_VALIDATION.json](CATALOG_VALIDATION.json).

## Remaining limits

- `AdvanceCharacterLevel` still executes only Soldier 1→2. No level 3 command was committed or replayed.
- Command Step, Tactical Assessment, and Suppression Fire have no runtime handlers. Target armor/cover observations are still unavailable from authoritative generic world state.
- The synthetic two-event test covers structural chronology only; it does not prove consecutive command execution, revision-specific replay, or save/restore after a level 3 choice.
- Unity compilation, Edit Mode, Play Mode, and a standalone player build were not run. Unity integration remains deferred.
