# Next temporal parent integrations: actual holder dependencies

Preparation from the current reference code, not a new rules decision or completion certificate. The twelve decisions in `GPT_TEMPORAL_WORLD_BOUNDARIES.md` remain controlling. The bounded control/pulse revision is independently reviewed in its own trail.

## Concentration and transformation

`TransformationWorld` in `tools/transformation_spell_playtest_rules.py` owns canonical `bodies`, `casts`, `links`, `slots`, `druids`, damage/regular-end history and commands. Its `buffers` and `concentration` references must remain the same shared ledgers used by the other adapters. Each `Body.life` points to actual life state; there is no separate transformation HP pool to copy.

The actual concentration entry is `(cast_id, on_end_callback)`. `_end_cast` reaches the existing world and each existing Link. `_end_link` updates Body anatomy/size/mass, shared `BufferLedger.spell_anatomies`, linked shields, melded equipment, persistent slots and placement requirements. Replaying this ordinary end procedure during temporal commit would also emit ordinary lifecycle events. The temporal adapter therefore needs a complete proposed state and deliberate callback rebinding to restored canonical identities, without ordinary entry/end triggers at commit.

Required joint checks include same life/buffer/concentration aliases; replacement or ended concentration; unchanged physical origin; still-owned melded equipment; current lost/transferred items; one persistent enrollment slot; current geometry after all participant forms are restored; no new cast/save/payment/shield offer; and a later real concentration ending that reaches exactly the intended restored links. The full geometry/provenance decisions already require unsupported cases to reject atomically.

## Druid

`DruidState` is in `tools/form_temphp_playtest_rules.py`. It shares the same BufferLedger and optionally the same CreatureWorld. Its state includes current FormInstance and instance registry; rest epochs and uses; shifts, reserve, surges and capacities; attunement; cadence; recharges and OwnerRechargeClock. `_refill` initializes several finite fields outside `__init__`, so a constructor-only inventory is incomplete.

`OwnerRechargeClock` keeps `mode`, `now`, `next_tick`, `ticks`, `last_regular` and `anchored`. It conserves one real owner schedule across initiative transitions. A temporal iteration/turn token cannot replace its real regular-marker index or create a second recharge clock. The host scheduler's monotonic actual marker must feed the existing clock only at real regular starts, with no call at restore.

Current form state must be reconciled jointly with transformation ownership and `BufferLedger.form_instances`, not restored through a fresh `shift()`. That ordinary method charges resources and opens entry effects; temporal restoration must do neither. Current finite reserves/rest history remain governed by the settled conservation decisions.

## Current control/pulse dependency

The repaired control world takes the host's existing `ConservedPulseOutputs` explicitly. Its exact current concentration checks are a bounded dependency check, not a full parent restoration/replacement adapter. Outside-initiative recipient-round import, complete source sibling lifecycles and final capped HP/Ki/Conviction application remain unfinished. These must be composed with the real host rather than implemented as independent copies of balances, recipient budgets or callback worlds.

No source has been deleted or promoted by this preparation. All seven major integration domains remain open.

## Parent source conference completed

The [actual ten-case conference](GPT_TEMPORAL_PARENT_BOUNDARIES.md) and [Action-budget/cadence clarification](GPT_TEMPORAL_PARENT_CADENCE_CLARIFICATION.md) settle source policies for participant concentration, protected mixed-roster spells, permanent True Polymorph, paid Druid renewals, local/global spending, entry shields, authentic recharge, new-iteration windows, conserved cadence and expired anatomy. Five temporal rules are explicitly labeled new/provisional in the [authored parent guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md).

The Action clarification preserves the approved kernel: current turn allowances restore from the snapshot with all outstanding Time Loop Reaction debts; historical activation events and finite resource spending remain recorded. No new generic short-rest Dissonance reset was adopted from loose wording in the reply; actual source-authorized recovery still governs.

`TEMPORAL_PARENT_STATE_INVENTORY.json` accounts for85 actual fields across9 holder types, including Druid fields initialized outside the constructor, and links all26 exact form profiles. This is source/implementation preparation, not runtime validation. The new review-status manifest explicitly leaves parent code, all seven larger integrations, full Time Loop and whole-game approval unfinished. All exact previously reviewed helper hashes remain unchanged. No original content was deleted or pushed.

## Parent operation history: four-finding repair under review

The notebook's [actual initial review](GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md) found four evidence gaps in the 38-method candidate. Canonical stats/ordinary prices, persistent Druid finite-state checking, operation-qualified transition evidence and outside-event classification are addressed in the [exact 55-method repair](CODEX_TEMPORAL_PARENT_HISTORY_REPAIR.md), now submitted in Calibration Review. This is recorded as a candidate pending the actual response, not a joint closure. The first authority probes and original exact packet remain preserved.

The current guide and coverage ledger now distinguish source discussion, authored rules and executed validation evidence. Repeated temporal progress notes were consolidated; the entire earlier ledger is retained in COVERAGE_BEFORE_PARENT_HISTORY_REPAIR.json. No original game source was deleted. All seven major temporal integrations and final whole-game/GitHub gates remain open.

## Parent operation-history checkpoint closed

The notebook [confirmed the exact 59-method journal](GPT_TEMPORAL_PARENT_HISTORY_CLOSURE.md), closing all four initial findings and the two follow-up findings. The [current manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json) binds the actual closure to the helper, tests and validation report. Earlier packets and actual reviews remain preserved. Ordinary source helpers, the reviewed control/pulse files and frozen class rules are unchanged by hash comparison.

Next work is the actual parent transaction: capture the reviewed identities/history, propose complete forms/concentration and dependent state, reconcile current inventory/enrollment/geometry, stage the exact original references atomically, and exercise subsequent genuine events. The present Transaction intentionally accepts only data values, so reference staging requires its own reviewed extension. The kernel still rejects active form identities and admits only its existing control/pulse adapter. Do not remove either gate based on history-only approval.

All seven larger integration domains remain open. Full Time Loop, the remaining game content, final whole-game flow review and GitHub delivery remain unfinished. Nothing was deleted or pushed.

## Original-reference transaction transport closed

The notebook [confirmed exact-reference staging](GPT_TEMPORAL_REFERENCE_TRANSACTION_CLOSURE.md) after 15 targeted checks and the existing207 checks passed. The same Transaction now transports exact Druid.current and concentration slot/callback references, detects stale bindings and rolls back exact original references on a later failure. No callbacks run at commit or rollback. The [manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json) binds this extension to the current foundation hash; the former reviewed foundation is preserved intact in temporal_playtest_rules_control_checkpoint.py.

This completes the transport prerequisite, not parent source planning. Full mutable source/dependency/gear/geometry watches and an integrated legal restore remain required. Seven major integrations remain open; no game content was deleted or pushed.
