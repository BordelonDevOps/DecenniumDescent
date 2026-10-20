# Actual GPT parent policy conference

Captured from Calibration Review on 2026-10-09. Source/policy decisions only; no parent runtime implementation approval. The wording about historical Action expenditures is being clarified separately against the already-reviewed snapshot action-budget rule.

ChatGPT said:

The ten cases can be settled from the current helpers plus the twelve Time Loop conservation decisions. I would treat the result as a source/policy conference only: implementation and adversarial review still follow separately. The parent integration must continue sharing the one Core life ledger, BufferLedger, ConcentrationLedger, physical identities and persistent slots rather than inventing parallel form state. 
Pasted text

Participant concentration restoration — CONFIRMED, with one NEW PROVISIONAL implementation invariant.
Yes: a participant's snapshot Polymorph/Shapechange/Mass/True shaping concentration can be restored after a post-snapshot concentration failure when the original absolute deadline is still valid. Restore the exact original Cast, Link, anatomy relationship and concentration parent; do not call cast(), reroll a save, repay RP, fire a cast hook, or manufacture a new link identity. The existing helper shows that starting concentration owns a callback which ends the original cast's shaping links, so this must be restored as one source closure, not by merely changing Link.state. 
Pasted text
 
Pasted text
 
Pasted text

If the participant now concentrates on a different post-snapshot source, that later participant-owned concentration may be retired as part of the rewind, while all RP/uses/actions already spent on it remain conserved. Preflight must project every consequence of invoking/retiring its source closure before mutation. NEW PROVISIONAL implementation invariant: snapshot the original participant concentration slot/callback identity just as the control bridge now pins concentration identities; restoration rebinds that original source closure rather than constructing an equivalent-looking synthetic slot.

Outsider concentration remains different: the twelve decisions explicitly say a nonparticipant's concentration slot is current external state and cannot be recreated or rewritten. 
Pasted text

Mixed-roster concentration — CONFIRMED, but use the conservative boundary.
Do not implement a synthetic half-Mass-Polymorph.

For the first complete parent adapter, permit mixed-roster restoration only when the exact original shared cast/concentration slot is still current and every nonparticipant link remains current and unchanged. Then the participant-facing rewind may restore compatible participant state without touching the outsider.

If that shared slot ended/replaced after snapshot, or restoring its callback would revive/end/change the nonparticipant's link, reject Time Loop. This follows directly from the external-dependency rule: dependency closure does not turn the outsider into a rewind participant. 
Pasted text

So for the concrete Mass Polymorph example: if concentration failure ended both links after snapshot, you cannot restore only the participant. That activation is unavailable. No save replay, no half-cast.

True Polymorph stabilization — stabilization is CONFIRMED; later dispel/replacement needs a NEW PROVISIONAL ruling.
Once the original 60-second shaping checkpoint legitimately resolves to permanent, Time Loop cannot turn it back into shaping, recreate concentration, or rerun the checkpoint. The helper itself changes the same link to permanent and detaches concentration at that checkpoint. 
Pasted text
 The twelve-decision table already classifies True shaping as world-absolute and permanent True as a permanent record. 
Pasted text

NEW PROVISIONAL: a later post-snapshot dispel does not automatically make restoration impossible merely because the dispel event is historical. Event history can remain conserved while participant state rewinds, just as damage-event history survives while HP rewinds. Therefore the same original link may be restored as permanent, never shaping, if:

the ending was a rewindable post-snapshot effect on that participant;
the original link/lineage still has a unique identity;
current physical inventory, sponsor slot, geometry and external suppression reconcile; and
no protected outsider/persistent state must be rewritten.

A later replacement is treated similarly but is harder: the replacement source closure must be legally retireable. If the current replacement depends on an outsider, a conserved persistent slot, transferred gear, or another nonrewindable enrollment, reject instead. A successful dispel/replacement event remains historical and its cost remains spent.

Druid paid same-instance renewal — CONFIRMED; historical receipt requirement is NEW PROVISIONAL.
Your example resolves exactly as proposed. F at 600 is legally renewed by natural_endpoint() to 1200, with the shift consumed. At t=601, the actual world-valid endpoint is 1200. Time Loop must not restore 600 and must not turn it into 601+600. The helper explicitly mutates the same FormInstance.expiry; it does not create a new form. 
Pasted text

If F subsequently ended before the rewind, F may be reactivated from snapshot encounter state only when the reason it ended is itself rewindable and current time is still strictly before 1200. It comes back with endpoint 1200. If current world time is 1200+, it cannot return. If its later end reflects conserved external state, restoration rejects.

NEW PROVISIONAL: require a conserved renewal receipt such as (formInstanceId, oldExpiry=600, newExpiry=1200, renewalEventId/paymentIdentity). Merely observing that expiry changed is insufficient proof that a real shift was legally spent. A new form ID can never inherit this receipt or extension.

Druid local permissions versus global expenditures — CONFIRMED.
FormInstance.spent is a form-local one-shot view. If a special was unspent at snapshot but spent only in the discarded iteration, the restored same form may regain that local permission. If it was already spent at snapshot, it remains spent. This follows the general temporal one-shot rule. 
Pasted text

But all global finite state stays current: shifts, reserve, surges, rest_uses, recharges, long/short epochs and OwnerRechargeClock. The helper requires both the local permission and the global currency; restoring f.spent therefore cannot bypass surges == 0, a used short/long-rest special, or a still-running recharge. 
Pasted text

Broodmother is especially clear: entry_open exists only during the actual shift() entry transaction and closes immediately afterward. Temporal restoration is not an entry, so it never reopens the spawn window. 
Pasted text
 The source itself says the spawn is on entry. 
Pasted text

Current rest/attunement/progression wins. If an Arch form is no longer currently attuned after a real conserved rest, do not manufacture old attunement to make the snapshot legal; absent an exact adapter, reject.

Druid entry buffers and independent Mooncursed shields — CONFIRMED.
For an entry-buffer form, restore the same form instance and the same original grant identity with its snapshot remaining amount, subject to the current dependency still being valid. Do not call shift(), offer() a new grant, or debit reserve again.

So Bear:

paid entry created F:entry;
snapshot THP = 12;
later damage/reversion ended the dependency;
Time Loop can restore that same grant to 12 if F itself is valid;
current Buffer Reserve stays at its actual spent value.

This matches both the helper's form-dependent entry grant and _end() dependency termination. 
Pasted text
 An expired/invalid F cannot carry the shield back with it.

Mooncursed Howl is intentionally different. Its grants use the recipient's rest_epoch, not the form instance as a dependency. Ending Mooncursed therefore does not inherently end an already legal Howl shield. 
Pasted text
 Its source confirms Howl is a separately paid Form-Surge effect drawing from Buffer Reserve. 
Pasted text
 Apply the ordinary rest-bound buffer temporal policy to that grant. Other shield families still require their own source policy.

Recharge bridge/authentic markers — CONFIRMED, with one wording correction.
Keep exactly one canonical OwnerRechargeClock and the current DruidState.recharges. Time Loop does not restore their snapshot values and calls no recharge method during the restore. The twelve decisions already state this clock spans initiative and downtime and is conserved. 
Pasted text

At each genuine owner regular start, pass the scheduler's monotonic global regular marker exactly once into DruidState.regular_start(). It is fine that the values might be 1, 4, 7 rather than 1, 2, 3; the helper needs a monotonic actual marker, not a consecutive owner-local integer. 
Pasted text
 
Pasted text

Correction: a first post-loop start at unchanged world seconds does not tick merely because it has a new regular-marker identity. But if the preserved next_tick is actually due at that same world timestamp, the genuine regular-start call may legitimately tick. The rewind itself never ticks.

A prepared temporal plan must watch the entire recharge clock plus recharges, rest epochs and other finite Druid state; an actual tick/rest between preflight and commit makes it stale.

Shapechange switches and hostile repeat-save windows — CONFIRMED, with a NEW wrapper representation.
Replace raw regular_index/round_number temporal identity with authenticated:
IterationTurnId for actual regular-turn windows and IterationRoundId for first-damage-per-round windows. Keep global event IDs historical. The current numeric fields are adequate for the non-temporal helper but not across a rewind. 
Pasted text

For an outside-origin Shapechange already active at the initiative snapshot, the owner's first genuine regular turn in new iteration round 1 counts as “later than the original casting turn.” The cast occurred before the current encounter's turn sequence. It does not get a free switch at restore; the switch still consumes its Bonus Action and must choose a different legal profile. The current helper's once/later-turn rule remains the semantic source. 
Pasted text

NEW PROVISIONAL representation: give outside-origin casts a stable OUTSIDE_CAST origin token plus original cast timestamp/identity instead of pretending they were cast on iteration-0 turn 0.

For a hostile link whose first positive-HP-damage repeat save was consumed only after snapshot: that old save/event remains historical, but the restored snapshot's active round-consumption view is unspent. The first qualifying positive normal-HP damage in a genuine new IterationRoundId may therefore trigger the repeat save again. No save occurs during restoration. 
Pasted text

If that discarded save succeeded and ended the link/concentration, restoration is then subject to case 1: participant-owned parent concentration may be restored; an outsider's ended concentration cannot be recreated.

Druid cadence — NEW PROVISIONAL temporal classification, but source evidence is sufficient now.
Do not restore snapshot refrain, rememberedSpell, or dissonance. Preserve the current canonical cadence dictionary across Time Loop.

The reason is source-grounded:

an actual Druid shift() explicitly clears Refrain and rememberedSpell;
it explicitly leaves accumulated Dissonance alone;
temporal restoration is not shift(). 
Pasted text

These values are spellcasting-history/economy state, not a form-local permission. Conserving them also prevents a cast in the discarded timeline from having its RP expenditure conserved while its Refrain/Dissonance consequence disappears.

Therefore the first parent implementation does not need to reject merely because cadence changed after snapshot. It should:

alias the one real cadence dict;
watch it for preflight staleness;
leave its current values untouched at restore;
never clear it merely because a Druid form is being restored.

A real post-snapshot paid shift that cleared Refrain keeps that clear even if Time Loop later restores an earlier form state. That is a conserved consequence of a real paid class transaction, not a free Time Loop reset.

Expired forms and current external effects — CONFIRMED: reject; no generic base-anatomy normalization is authorized.
The twelve decisions already classify ordinary Druid form duration and temporary transformation spell duration as world-absolute. A same-instance Druid extension such as case 4 or True's permanent stabilization is an explicit exception because it changes the actual valid endpoint/state. Otherwise, an expired form cannot simply be resurrected. 
Pasted text

There is also no existing authorization to say “restore everything except anatomy, normalize to base, and keep whichever snapshot movement/gear/shields still make sense.” That would invent a hybrid state and could leave dependent movement, melded gear, buffers or other children detached from their parent.

So if current world time has passed the exact form/anatomy endpoint and there is no valid same-instance extension/permanent state, snapshot restoration requiring that anatomy is unavailable. Do not call the endpoint again, grant a fresh duration, or selectively preserve dependent children.

External suppression is different only while the underlying link remains legally alive: restore the valid source record, overlay the current conserved suppression, express root anatomy as required, and preflight the resulting geometry. The current transformation helper already keeps suppression on the same link without resetting its clock or recapturing gear. 
Pasted text
 The twelve decisions likewise require current external suppression and current item ownership to overlay the rewind. 
Pasted text

The resulting parent policy is coherent enough for implementation. The main genuinely new rulings here are: participant concentration can be reconstructed as the exact original source closure; permanent True may survive a rewound post-snapshot dispel/replacement when no conserved external state conflicts; Druid paid renewals require conserved renewal receipts; outside-origin Shapechange needs an explicit cast-origin token; and Druid spell cadence is conserved current state rather than snapshot-restored state.

I would record this conference as:

SOURCE-DISCUSSED / IMPLEMENTATION-READY — concentration, transformation-anatomy, Druid form, recharge, buffer-dependency and cadence boundaries settled for the supplied parent integration; code and adversarial validation still pending.

Full Time Loop, the remaining parent/lifecycle domains, and the final joint whole-game flow/GitHub gate remain open.
