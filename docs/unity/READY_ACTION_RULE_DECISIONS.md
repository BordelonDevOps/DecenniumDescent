# Ready Action prototype policy

Status: schema58 TEST_ONLY behavior on `Engine`, implemented after review with the Unity Rules Engine Development chat. The owner authorized the Codex/GPT consensus workflow. This bounded profile is not full Ready Action support or release approval.

## Responsibilities and authoritative records

- `ReadyActionRecord` stores the declaration, actor, named target, locked ordinary weapon choice, preparation turn and revision, exact expiry marker, and lifecycle status.
- `ReadyOccurrenceRecord` stores a completed target-entry step and its queued response status. It does not change the tactical move or undo its movement.
- The shared `WorldSchedule` supplies each actor's exact six-second interval and next own-start marker. `WorldIntervals` and `TacticalActors` remain the authorities for Action and Reaction availability.
- The existing `Simulation` command transaction, deterministic attack resolver, queue for Press/Overwatch/trap choices, shared `RuleClock`, receipts, snapshot codec, save/restore and replay remain authoritative. Schema58 only appends Ready records for an opted-in profile.

## Source authority

Pinned source revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

`DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`, **Ready** section, SHA-256 `F90D039142145FBD31C37992EBECE70D7926DC4B6081E340F9A2FD9DC7237BC6`. The source says setup spends an Action, records a perceivable trigger and one legal Action-time action or movement, and expires at the actor's next regular turn start. Release uses the normal Reaction and rechecks prerequisites; decline or an invalid occurrence spends no release resource, and the declaration may wait for another trigger before expiry. The source also allows wider action types and readied movement than this implementation.

## Adopted prototype behavior

- The actor chooses one currently visible enemy and one ordinary club or unarmed attack. Target, attack form and knockout instruction are fixed at setup. One armed declaration per actor is retained; replacing it spends the new Action and records the previous declaration as replaced.
- Setup requires the actor's current regular turn and an available Action. It does not consume Reaction, roll dice, reserve ammunition, or fire immediately.
- The current trigger is a named target entering within five feet of the stationary Ready owner. It is detected only when that target completes a tactical step. A step interrupted by an earlier opportunity attack does not trigger Ready. Setup itself never creates a trigger.
- The completed step enters the shared post-step queue alongside existing Press, Overwatch and hunting-trap events. Earlier pending events resolve first by creation revision, source-applied revision and stable ID. A Ready response follows the completed movement and does not revert it.
- Acceptance rechecks actor capability, Reaction, reach, visibility and the locked ordinary attack. It spends the shared Reaction and resolves through the existing melee attack path without paying a second Action. Declining preserves the Reaction and armed declaration. A now-illegal occurrence is invalidated without spending release resources; the declaration can respond to a later entry before expiry.
- The exact expiry is captured at preparation as `WorldSchedule.Start(preparedTurnOrdinal + rosterCount)`. It is never renewed on re-entry, tactical exit, or save/restore. The shared-clock advancer splits at this marker, processes expiry at the regular-start phase, records the exact marker and the command receipt that processed it, then continues the same requested advance. Expiry does not consume or refresh Reaction. A resolved declaration is removed from future deadline selection.
- Encounter exit is not blocked only because a declaration remains armed. If its owner-start deadline follows the exit boundary, the declaration remains armed after exit and expires through ordinary shared-clock advancement.

These movement/queue details and the shared-clock behavior were adopted as prototype policy during Codex/GPT review because the engine's existing movement queue and time model do not define all Ready interactions. They do not claim that every possible Ready action is executable.

## Acceptance scenario

`ready_action_expiry_survives_tactical_exit_chunking_and_restore` uses the existing three-actor TEST_ONLY Soldier calendar. The player arms Ready against a one-hit-point authored fixture enemy; the companion moves into reach and defeats it; the real `EndFixedEncounter` exits while the Ready action remains armed until the player's later scheduled start. One trace advances past the expiry in one command. A second stops at the exact marker, saves/restores, and advances past it. Both must retain the original marker and expire exactly once. The fixture's one-hit-point maximum is test data, not a combat balance rule.

Other cases verify query purity and Action/Reaction costs, schema58 round-trip, off-turn accepted attack, duplicate response idempotency, decline and later re-entry, a later accepted occurrence retaining the prior decline, interruption ordering, stale release rejection after exact expiry, and expiry at the owner's next regular start. The combined Ready/Overwatch test accepts each earlier same-step occurrence in turn and verifies that the other is invalidated against the shared Reaction.

## Dependencies and known gaps

Implemented only in the compile-gated `Laboratory/Model` TEST_ONLY profile. Core stores and validates immutable records; Persistence encodes schema58; no Unity or presentation code participates.

The following remain unsupported: Ready spells and held concentration; readied movement or non-attack actions; class actions, Bonus Actions and Reactions; arbitrary or environmental triggers; exploration-trigger detection; selecting among multiple response targets at release; encounter roster changes; broader death/disable rules; and production content selection. Trigger detection consumes completed tactical move records (ordinary movement, Press, Command Step, Defensive Formation movement and repositioning). Other forced-displacement producers are not generalized. In the current fixed Overwatch profile, Push moves the named target away from the sole Ready owner/shooter, so it cannot create an eligible entry event. The source's complete Ready procedure is not represented by the current club/unarmed fixture.

Earlier snapshot schemas retain their original byte layouts. The profile remains opt-in and is not production-approved.
