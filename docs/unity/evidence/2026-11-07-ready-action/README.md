# Schema58 Ready Action evidence

This packet records a bounded TEST_ONLY Ready Action increment on the `Engine` branch. It does not claim complete Ready support or completion of the simulation.

## Behavior and source

The pinned source rule is `DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`, Ready section, at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; SHA-256: `F90D039142145FBD31C37992EBECE70D7926DC4B6081E340F9A2FD9DC7237BC6`. Source-defined setup Action, trigger, release Reaction and next-own-start expiry are represented through the existing simulation records and schedule.

The implemented trigger is one named visible enemy completing a tactical step into five-foot reach. The only response is its locked ordinary club/unarmed attack. Completed movement stays committed; Ready is ordered with the existing post-step events. Spells, held concentration, readied movement, class actions and exploration trigger detection remain unsupported.

The exact `WorldSchedule` start marker is captured at preparation and is never recalculated. Shared `AdvanceTo` visits that deadline even after tactical exit, expires the armed declaration once, records its effective deadline and initiating command receipt, and continues the requested clock advance. Existing inventory, work, conditions, RNG, command, save and replay authorities remain in use.

See the [decision record](../../READY_ACTION_RULE_DECISIONS.md) and [implementation trace](../../IMPLEMENTATION_TRACE.md#2026-11-07--ready-action-lifecycle-and-shared-clock-expiry-schema58-test_only). [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) records relevant implementation and source hashes.

## Runnable acceptance

- `ready_action_persists_declared_trigger_and_resolves_off_turn_shared_attack` checks declaration query purity/Action cost, schema58 restore, completed-step occurrence, off-turn Reaction cost, attack resolution and duplicate-command idempotency.
- `declined_ready_occurrence_keeps_reaction_and_waits_for_next_entry` checks decline, retained Reaction/declaration, no trigger on departure, a later re-entry, and retained decline history after that later occurrence is accepted.
- `ready_action_expires_at_owners_next_regular_start` checks exact own-start expiry inside the tactical calendar, then rejects a stale release without changing the refreshed Reaction, attack records or RNG.
- `ready_action_expiry_survives_tactical_exit_chunking_and_restore` uses a replay-valid three-actor encounter. After a real exit at t=4 the declaration remains armed until t=6. A t=4→8 command and a t=4→6 save/restore→8 sequence both retain the original expiry and process it once. The one-hit-point enemy maximum is explicit TEST_ONLY fixture data, not a balance rule.
- `ready_and_overwatch_compete_for_one_shared_reaction_in_application_order` causes both systems to queue from one completed step. It runs Ready-first and Overwatch-first application histories, rejects the later choice while the earlier is outstanding, accepts the earlier choice, and verifies the loser invalidates without double-spending Reaction or ammunition.

The first full-suite run reproduced four failures. Three showed that adding a default fixture maximum HP had changed historical content fingerprints; default fixture data now preserves the exact prior fingerprint. The fourth showed that an accepted Press follow, which is a deferred continuation rather than an unresolved prompt, was being treated as a live post-step choice. It is no longer added to that pending-choice ordering. The first combined Ready/Overwatch regression then exposed an initializer that did not recognize the schema58 overlay, so that existing Overwatch execution state now initializes on the layered profile. A decline-history regression also exposed that validation rejected an earlier declined occurrence once the same declaration later expired or was accepted; validation now requires chronological ordering against its terminal resolution while preserving the old occurrence. The corrected focused cases and full suite pass.

## Validation

- `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1`: **PASS, 1,217/1,217** cases, C# 9 warnings as errors. See [full results](FULL_TEST_RESULTS.json).
- `pwsh -NoProfile -File engine/tools/Validate-Package.ps1`: **PASS, 18/18** static checks, 261 package assets and 261 unique GUIDs. See [package results](PACKAGE_RESULTS.json).
- These reports attest to the local headless C# suite and static package structure. They do not imply complete Ready semantics or production approval.

## Independent review

The implementation excerpts, chronology checks, schema58 composition gate, two-order shared-Reaction acceptance and local validation totals were sent to **Unity Rules Engine Development**. GPT found no concrete blocker in the supplied material and stated that it did not inspect the checkout or run the checks. Its review receipt is [GPT_REVIEW.md](GPT_REVIEW.md).
