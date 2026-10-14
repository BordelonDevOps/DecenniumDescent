# Time Loop: forms and concentration

**Source policies discussed; parent implementation and adversarial review pending. Full Time Loop remains unavailable.**

The [actual parent conference](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_BOUNDARIES.md) applies the [twelve conservation decisions](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_WORLD_BOUNDARIES.md) to the current Druid and transformation helpers. The [form rules](FORM_TEMP_HP_PLAYTEST.md) and [transformation spell rules](TRANSFORMATION_SPELL_PLAYTEST.md) retain authority over ordinary play. This is a temporal overlay, not a new form, spell, class benefit or release of the full Oracle ability.

## Decisions for play

| Situation | Proposed restoration under the discussed policy |
|---|---|
| A participant's snapshot Polymorph ended after concentration failed; its original deadline is still future | Restore the same cast, link and original concentration callback together, if every source dependency is legal. No new cast, payment, save or entry event. |
| The participant now concentrates on a different post-snapshot source | Retire that later source only after projecting its complete consequences. Its RP and finite uses stay spent. Unsupported effects or protected outsider consequences make the rewind unavailable. |
| An outsider supplied the snapshot concentration | The exact original slot must still be current. The outsider's slot, resources and body do not rewind. |
| Mass Polymorph affects a participant and a nonparticipant | The first parent implementation may accept only the still-current exact shared cast/slot with every outsider link unchanged. If concentration ended or replacement would change an outsider, reject; do not reconstruct a partial cast. |
| The same True Polymorph reached its original stabilization checkpoint after initiative | Retain permanent status and the absence of concentration. Do not turn it back into shaping or replay the checkpoint. |
| That stabilized True Polymorph was later dispelled or replaced | It may return as the same permanent link only when the later ending is rewindable, physical lineage remains unique, and current gear, enrollment, suppression and geometry all reconcile. A protected current replacement prevents restoration. |
| Druid form F was legally renewed at second 600 to second 1200; rewind occurs at second 601 | Preserve the paid renewal and deadline 1200. The shift stays spent. Never set the deadline back to 600 or forward to 1201. The extension belongs only to F. |
| F ended after that renewal | Restore F with deadline 1200 only if the ending is rewindable and current time is still strictly before 1200. A conserved external ending or expired endpoint blocks it. |
| A form special was unused at snapshot but used afterward | Its same-instance local permission may return. Current Surges, rest uses, recharge state and other required costs still govern actual use. An exhausted global resource cannot be bypassed. |
| Broodmother is restored | Its entry-only spawn window stays closed. Restore creates no entry event. |
| Bear's entry shield had 12 points at snapshot and was later lost | Restore the same grant to 12 only if the original form dependency is valid. Current Buffer Reserve stays spent; no new shield offer occurs. |
| Mooncursed ended after giving an ally its Howl shield | That shield follows its original recipient long-rest endpoint, independently of the form. Restore uses the same grant and no new Surge or reserve allocation. |
| A new iteration gives the Druid a genuine regular start | Feed the next real global regular marker to the existing owner recharge clock once. A tick occurs only if its conserved due marker is actually due. Rewind itself calls no clock method. |
| An outside-origin Shapechange exists at snapshot | The first genuine owner regular turn in the new iteration is later than the original cast. A switch still costs its Bonus Action, requires a different legal profile, and occurs at most once in that authenticated turn. |
| A hostile transformation's damage-triggered repeat save was used only after snapshot | Preserve the old event history. The first qualifying positive normal-HP damage in the new iteration-round may allow its ordinary repeat save. Restore itself rolls nothing. |
| Druid Refrain, remembered spell or Dissonance changed after snapshot | Keep the current shared cadence values. Restoring a form neither clears them nor restores older values. A real paid shift's earlier Refrain clear stays recorded. |
| A required snapshot form expired with no valid renewal or permanent stabilization | Reject restoration requiring that anatomy. There is no generic permission to substitute base anatomy while keeping selected old movement, gear or shield benefits. |
| An otherwise live spell form is currently suppressed | Preserve the actual external suppression, express the required operative anatomy and preflight geometry together. Suppression does not grant a new duration or recapture equipment. |

The notebook [confirmed the Action-budget clarification](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_CADENCE_CLARIFICATION.md): snapshot turn allowances return with outstanding Time Loop Reaction debts overlaid; past event history and finite RP/rest expenditures remain conserved. No parent implementation may introduce an additional Action refund or charge while retiring a cast.

## Newly specified temporal rules

These are explicit provisional design additions rather than recovered historical rules:

- Participant concentration restoration reuses the exact retained original slot/callback and the whole original source relationship. Equivalent text IDs or freshly built callbacks are insufficient.
- A post-snapshot dispel or replacement can be undone for a uniquely preserved permanent True Polymorph when the ending and its dependencies are rewindable. Its permanent world checkpoint never becomes a shaping phase again.
- Same-instance Druid renewal needs historical evidence of the legal renewal and payment. A changed expiry field alone does not prove a paid extension.
- Outside-origin Shapechange has an explicit cast-origin record with its real cast identity and time, distinct from an invented encounter turn zero.
- Druid's current Refrain, remembered spell and Dissonance are conserved casting economy/history. They are not form-local permissions restored from the snapshot.

Future genuine events modify that current cadence only under their existing rules. There is no new generic short-rest Dissonance reset here. The frozen common rules identify Retune, long rest, the limited meditation option, qualified idle turns and Grounding; class-specific vents retain their exact source requirements. The temporal bridge does not broaden those recovery permissions or implement every class's cadence hooks.

## Required source history

A complete parent adapter must retain the original cast/form ID, actual creation marker, exact owner/targets, original source procedure, original concentration slot/callback where applicable, and original physical lineage. It must also record renewal, stabilization and ending events with their real markers and causes. A current `state` or `expiry` field cannot establish that history by itself.

A renewal record identifies F, the prior endpoint, the new endpoint, the actual event and its source-qualified payment. A level-20 zero-shift renewal remains a real authorized renewal event. A new form cannot borrow another instance's extension. A stabilization record identifies the original True link and its resolved checkpoint even if that link was subsequently dispelled. An ending record must distinguish a rewindable participant event from a protected external or persistent change.

Retained past events never become new payment, reward, entry, cast, healing or save events. Local permission views use iteration-qualified keys while their original event histories remain intact.

## Implementation order and acceptance cases

The first implementation layer is now `tools/temporal_parent_history.py`: an observational journal over the existing Druid and transformation objects. It binds the host's actual actor wallets, retains original source/callback identities, and records creation, paid renewal, stabilization and ending evidence from native operations. Its [38-method validation](TEMPORAL_PARENT_HISTORY_VALIDATION.json) includes forged expiry/permanence flags, equal-looking replacement objects, duplicate wallets, lost gear, genuine recharge starts, and failures after a native operation already changed state. The [exact implementation submission](../../../../docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_PARENT_HISTORY_REVIEW.md) is under notebook review.

This layer begins observing before source creation; it cannot reconstruct old history from current state. `valid_form_deadline()` establishes a recorded endpoint, not permission to reactivate the form. `permanent_link()` establishes a historical True checkpoint, not permission to override a later protected ending. Ordinary source access, geometry and authoritative save results still come from the host and existing helpers. A failed native operation that already changed observed state blocks further temporal admission pending host reconciliation. The journal does not roll back a committed cast or replay its save.

No parent restore transaction is implemented by this layer. Reference-safe callback staging, full dependency reconciliation, temporal turn wrappers and integration with the existing kernel remain required below.

The [field inventory](../../../../docs/audit/2026-10-08/full-game/TEMPORAL_PARENT_STATE_INVENTORY.json) accounts for 85 actual fields across nine holder types and links all 26 Druid profiles. It is an engineering checklist, not runtime validation. In particular, Druid reserves created by `_refill()` are included, not just constructor fields.

1. Bind canonical Core life, BufferLedger, concentration, Druid, physical inventory and persistent enrollment references. Prove every active source and child is disclosed.
2. Preserve source creation/renewal/stabilization/ending receipts and the original concentration references. Validate their history before taking a snapshot or charging a rewind.
3. Produce one complete proposed anatomy/concentration state for participants and protected outsider dependencies. Reject incompatible, unknown or expired sources before writes.
4. Reconcile current inventory and enrollment. Restore meld membership only for still-existing items still held/owned by the participant. Preserve compatible later external gear; plan legal drops for incompatible gear.
5. Validate all participant geometry and item drops together. Preserve protected outsider space and physical state.
6. Stage classified field writes in the existing atomic transaction. Preserve all finite economy, cadence and clock state. Install the original callback references without invoking cast/start/end procedures during temporal commit.
7. Exercise real later concentration endings, due recharge starts, form specials, repeat saves and paid switches against those same restored objects. A later ordinary event must reach the intended source exactly once.

Required adverse cases include replaced canonical objects; same-ID callback replacement; ended mixed-roster concentration; transferred or destroyed melded equipment; competing persistent sponsor slots; fabricated renewal/stabilization receipts; expired form children; exhausted Surge with restored local permission; Broodmother spawn replay; a due versus not-yet-due recharge at unchanged world time; duplicate regular markers; malformed collections; and a source mutation between preflight and commit. Every rejected plan must leave costs and live state unchanged.

The approved control/pulse adapter currently requires its original concentration to remain current. Parent restoration will require a separately reviewed shared proposed-concentration interface; this guide does not relax that restriction in existing code. Creature children, devices, full class cadence hooks and other missing source adapters still block unsupported scenes.

All seven major temporal integration domains remain open. This conference does not enable Time Loop, close any whole-game coverage area, or satisfy the final joint flow review required for GitHub delivery.
