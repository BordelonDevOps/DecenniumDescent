# Connected exploration, combat, and assigned mining acceptance

**Status:** TEST_ONLY cross-system acceptance; no save schema change and no rule promotion.

This run composes the existing schema14 exploration-to-tactical transition with the schema47 companion assignment and mining resolver. The companion is assigned to an authored deposit, travels to its derived site, and starts the existing finite extraction attempt. The player explores into a turn-based encounter while the companion remains outside initiative. Mining work continues on the shared clock through the encounter and resolved exit. The scenario saves and restores the active attempt, advances it to a terminal success, confirms the selected unit is extracted, replays the original assignment without a second attempt, and continues exploration.

The only runtime code adjustment is a fixture parameter that lets `WithMining` select the encounter target's HP while preserving its default value of 26. The acceptance uses 1 HP to match the existing bounded connected-combat witness. Mining and combat continue to share the existing deterministic RNG stream. No new gameplay rule, result, schedule, content profile, or persistence field was introduced.

## Validation

- Focused C# 9 warnings-as-errors run: **1/1 passed** (`connected_exploration_combat_and_assigned_mining_share_one_saved_timeline`).
- Full C# 9 warnings-as-errors suite: **1,164/1,164 passed**.
- Static package validation: **18/18 checks passed**, covering 225 package assets and 225 unique GUIDs.
- `git -c core.whitespace=cr-at-eol diff --check`: passed.
- Unity Editor import and gameplay were not run; the current work remains in the C# phase.

See [focused results](FOCUSED_RESULTS.json), [full headless results](HEADLESS_RESULTS.json), [package results](PACKAGE_RESULTS.json), and [source bindings](SOURCE_BINDINGS.json).

## Limits

The encounter and deposit remain fixed TEST_ONLY content. The companion is explicitly player-directed; this does not implement autonomous AI, a general roster, simultaneous route planning, combat loot/rewards, general world-site discovery, or production content authority. Existing separate tests cover exact mining outcome and receiver settlement. This scenario proves their shared-clock composition, not that the complete gameplay engine is finished.
