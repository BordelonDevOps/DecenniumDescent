# Soldier level-four source-row advancement and permanent ASI

**Status:** implemented as a bounded TEST_ONLY increment on snapshot schema61. It extends the existing Soldier advancement fixture through class level four; it does not complete the character engine.

## Responsibilities and authoritative records

The resolver reads the pinned Soldier class-level-4 schedule row (`/schedule/3`): one Base-or-Arch selection, no required active selection, and a separate ASI-or-feat opportunity. It implements the ASI branch as one score +2 or two scores +1, capped at 20, and permits only Defensive Formation as a level-four selected-card grant because its existing tactical handler accepts that level and grant origin. Feats and other level-four card handlers remain unbound and fail closed.

- `ActorCharacterRecord.Abilities` and ordered `Levels` remain the current score and level authorities.
- `ActorLifeRecord` remains current and maximum HP authority; existing chronological base-HP and clamp formulas remain in use.
- `CharacterAdvancementRecord` records row choice, ASI increments, scores before/after, and causal HP values for history validation.
- Existing milestone, selected-grant, Hit Die, feature-runtime, command receipt, tactical, Map Route, condition, inventory, clock, and persistence records keep their roles.
- Schema61 appends advancement score history and Map Route check-time linked injuries. Schema60 and earlier keep their historical codec branches.

Historical validation binds each advancement event to its command receipt and source-row assessment, reconstructs score progression, recomputes each chronological HP capacity change, and checks the final character/life facts. The check-time Map Route facts prevent a later ASI or injury change from rewriting a resolved check.

## Connected scenarios

`soldier_level_four_asi_is_source_row_driven_and_reuses_historical_character_facts` resolves a trained WIS (Survival) Map Route check at Wisdom 10, saves/restores, advances the same Soldier with Defensive Formation and Wisdom +2, then verifies the original check remains unchanged and a later Map Route check uses the new Wisdom. It executes Defensive Formation in tactical combat, saves/restores and replays both pending recipient choices, and resolves a deterministic hostile hit through the actual damage pipeline. The test checks that an adjacent ally and spent shield stationarity produce the feature's one-point reduction in both the combat record and HP loss. It also rejects unsupported feature/feat branches.

`soldier_level_four_constitution_asi_recomputes_all_level_hp_without_healing_or_spending_dice` applies Constitution +2, verifies the four-level maximum HP recalculates from 22 to 32, preserves current HP, preserves spent Hit Dice, and verifies save/restore replay.

## Validation

- Full C# 9 warnings-as-errors suite: **PASS, 1,234/1,234**. See [headless results](HEADLESS_RESULTS.json).
- Focused advancement scenarios: **PASS, 2/2**. See [focused results](FOCUSED_RESULTS.json).
- Class advancement source projection: **PASS, 17 class files, 340 schedule rows, 1,223 option records**. See [schedule results](SCHEDULE_RESULTS.json).
- Static package validation: **PASS, 18/18 checks, 271 assets, 271 unique GUIDs**. See [package results](PACKAGE_RESULTS.json).
- `git diff --check`: **PASS**.
- Independent review and current changed-source hashes are recorded in [review notes](INDEPENDENT_REVIEW.md) and [source bindings](SOURCE_BINDINGS.json).

These are headless C# compilation/regression and static package checks. They do not establish editor import, in-editor tests, a player build, production content or release qualification.

## Remaining limits

Only the Soldier advancement path through level four is covered. The feat branch, other level-four handlers, automatic level-five Palisade operation, later class rows, other class advancement, prerequisites, multiclassing, retraining, general resource updates and production character content remain incomplete. The pinned class material is provisional playtest source, not release approval.
