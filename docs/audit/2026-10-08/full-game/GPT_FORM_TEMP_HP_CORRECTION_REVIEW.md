# GPT form and buffer correction review

ChatGPT said:

I find no remaining concrete blocker in the corrected selected form/temp-HP interface.

The recharge correction resolves the only blocker from the prior review, and the form-instance identity change closes a real cross-owner dependency hazard without expanding source permissions. The corrected suite reports 163 contract checks + 1,053 arbitration/damage scenarios PASS, while keeping the scope explicitly limited to the selected interface. 
Pasted text

Recharge timeline — accepted

OwnerRechargeClock now provides the required single owner timeline rather than separate combat and downtime clocks:

one monotonically increasing tick ordinal;
one six-second phase;
actual regular starts can consume a due tick;
actual elapsed time can consume the same due sequence only while outside initiative;
entering initiative first advances that same outside timeline;
a boundary consumed outside cannot be consumed again by the first regular turn;
backward time and parallel elapsed-time advancement during initiative are rejected. 
Pasted text

That matches the settled Recharge rule.

Earth Warden Slam now records readiness as:

source recharge ready at ownerTick + 2

rather than regularTurnIndex + 2, so its readiness survives form changes while being able to mature through either two legitimate regular-start ticks or twelve seconds of legitimate downtime. 
Pasted text

The new regressions cover the counterexamples I requested:

6 seconds outside: still blocked;
12 seconds: ready;
initiative reentry cannot double-count the boundary;
reordered/too-early starts cannot manufacture a tick;
an elapsed outside clock cannot run in parallel while initiative is active;
time cannot reverse;
actual short-rest elapsed time matures Recharge;
actual long-rest elapsed time matures Recharge. 
Pasted text

Importantly, this does not turn a rest into a magical “clear Recharge” operation. The actual elapsed rest time advances the same timeline, which is the right model.

Rest integration — accepted

The short- and long-rest methods now advance the recharge clock using their actual completion time before performing their own resource resets. 
Pasted text

That preserves the distinctions we wanted:

Recharge matures because time passed;
SR abilities reset because an actual SR completed;
LR abilities/reserves reset because an actual LR completed;
shifting itself does none of those things.

The caller still has to put the recharge clock outside initiative before processing downtime/rest, which is appropriate for this bounded adapter rather than silently inventing scheduler transitions.

Global form-instance identity — accepted

This is also the correct correction.

Previously, each DruidState had only local knowledge of its form IDs. Now the shared BufferLedger owns a world-wide form_instances registry. 
Pasted text

Before any shift payment or old-form teardown, entry verifies:

instance_id not in self.buffers.form_instances

Only after successful commit is the new identity permanently reserved. 
Pasted text

This gives the desired properties:

two Druids sharing the same world cannot have the same parent-form identity;
collision rejection happens before BA/shift expenditure;
collision does not end the actor's existing form;
ended form IDs remain reserved and cannot later ambiguously refer to a different form instance;
CreatureWorld.end_dependency(form=...) therefore cannot accidentally terminate another owner's dependent creatures because of reused form IDs.

The new cross-owner regression demonstrates both unpaid rejection and successful coexistence with distinct IDs. 
Pasted text

No regression found in previously accepted interfaces

I rechecked the corrected helper around the changed pieces and find no new semantic conflict with the prior decisions.

The implementation still preserves:

one active temp-HP grant with greater-only replacement and equal-value retention;
no zero-value grant identity;
recipient-LR versus explicit-expiry versus dependency lifetimes;
grant-linked Bloodshield permissions;
Overflowing Light cleanse only on the exact active grant's natural expiry;
exact Core temp-HP projection and one canonical damage event;
Necrotic Affinity's after-resistance/before-old-buffer prevention and post-packet grant;
Spirit Walk's one-character spatial deduplication and unattackable spirit representation;
finite Druid Buffer/Surge reserves;
same-instance natural renewal;
genuine new instance on form change/reentry;
Elemental/Vermin subtype identity;
source-local Surge uses versus owner-wide Recharge/rest uses;
Broodmother's entry-only spawn window;
independent Mooncursed ally shields;
no global authorization of unrelated weapon procs. 
Pasted text
 
Pasted text
Final disposition

The selected package can now be promoted to:

REVIEWED / reference-VALIDATED — selected temporary-HP grant identity, arbitration, payment/lifetime/dependency, linked-rider and Core-damage interfaces; Druid same-body Shapeshift lifecycle, reserve, renewal, form-instance, special-use and owner-recharge interfaces; the 26 bounded Druid form profiles; selected Necrotic Affinity and Spirit Walk integration boundaries for the reviewed 175 exact source roles + 5 supporting passages.

Validation evidence accepted:

163 targeted contract checks: PASS
1,053 buffer arbitration/damage scenarios: PASS
26 bounded Druid profiles
175 + 5 source integrity: PASS
global form-instance collision regression: PASS
combat/downtime/rest Recharge regressions: PASS. 
Pasted text

This closure remains deliberately bounded. It does not close or silently remove the nine named deferred components: Time Loop; Chef; Inspiring Leader; Soul Cage; Harmonic Bulwark; Shapechange; Polymorph; True Polymorph; or Mass Polymorph. It also does not close Blood Ritual's target count, other unfinished feat clauses, the item/anatomy compatibility matrix, global natural-weapon interoperability, broader ancestry/spell catalogs, human balance, the complete combat scheduler/runtime, or the whole game. 
Pasted text
