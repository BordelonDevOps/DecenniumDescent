# Shared Bonus Action implementation decisions

**Status: Codex/GPT consensus under the owner's standing delegation; schema24 TEST_ONLY implementation policy.** This file separates source facts from the narrow data-model decisions used by the first shared Bonus Action slice. It does not approve the playtest rules for release.

## Pinned source facts

Sources are pinned to repository revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`:

| Source | Locator | Git blob | SHA-256 | Fact used |
| --- | --- | --- | --- | --- |
| `DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md` | `#action-and-timing-limits` | `5a446dd0dabae096e51f419b5e71756e0169bb3b` | `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81` | One ordinary Bonus Action between a creature's regular starts when an actual feature permits one. |
| `DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md` | `#turn` | `72bcb58af57f8bfe27596ec0b1467e4c780a6ef8` | `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6` | A turn permits a Bonus Action when an actual rule grants a use. |
| `DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json` | `/engine/1`, `/schedule/0`, `/cards/0` | `c414a1d9ba2ce37cde89d0ef73265821bb74ac2d` | `ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0` | Base Overwatch is automatically granted at Soldier 1; the optional `soldier.base.overwatch` card is a separate selected upgrade. The level-1 schedule separately selects four Base cards, with at least two active. |

## Delegated implementation decisions

On 2026-11-04 Codex and Unity Rules Engine Development agreed on this first implementation boundary:

1. Persist a shared Bonus Action ledger keyed by actor and that actor's latest regular-start ordinal. A regular start makes the actor's Bonus Action available for that interval. It cannot accumulate across intervals.
2. Tactical Reposition and Overwatch designation consult and spend the same ledger. Tactical Reposition's own Recharge and movement budget remain separate feature resources.
3. Record grant origin as either `SelectedCard` or `AutomaticClassFeature`. The automatic Soldier 1 Overwatch grant has no selection milestone and is not a selected-card choice. The same feature ID may later have both origins so the selected card can represent its upgrade.
4. The schema24 Soldier fixture contains the automatic Overwatch entitlement but no selected level-1 card choices. It is intentionally incomplete and does not claim to satisfy the four-card/two-active schedule.
5. Keep schema21-23 bytes and replay unchanged. Schema24 appends grant origins and the shared Bonus Action ledger to the character-advancement snapshot section.

The schema24 implementation connects this ledger to Tactical Reposition and refreshes it at regular starts. It does **not** implement Overwatch designation, zone geometry, triggers, reactions, shots or rider choices. Those remain the next implementation stages. The shared ledger is an engine resource model; it does not change the source's Action, Reaction, Reposition Recharge or movement costs.
