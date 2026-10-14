# GPT form and buffer implementation findings

ChatGPT said:

I find one concrete implementation blocker. Apart from that, the submitted form/temp-HP interface tracks the agreed boundaries closely, including the 26 form profiles, buffer identity/arbitration, linked riders, form-instance rules, Necrotic Affinity staging, and Spirit Walk identity handling. The reported scope is appropriately bounded: 152 contract checks, 1,053 arbitration/damage scenarios, 26 form profiles, and 175+5 source integrity all pass without claiming full-card/runtime completion. 
Pasted text
 
Pasted text

Blocker: Recharge 2 does not mature outside regular turns

The guide correctly preserves the settled rule for Earth Warden Slam:

its Recharge 2 is owner/source scoped, survives shifting, and ticks on canonical regular starts or the protected six-second outside-initiative equivalent. 
Pasted text

The implementation, however, models the recharge entirely as a future regular_index:

Python
def regular_start(self,index,*,actual_regular_marker):
    ...
    self.regular_index=index

and:

Python
elif q['payment']=='recharge2':
    require(self.regular_index>=self.recharges.get(f.source_id,0),
            'Slam source recharge still active across shifts')
...
elif q['payment']=='recharge2':
    self.recharges[f.source_id]=self.regular_index+2

Pasted text
 
Pasted text

There is no path for actual elapsed out-of-initiative time to advance that counter.

Concrete failure
Earth Warden uses Slam at regular marker 5.
Helper records readiness at marker 7.
Encounter ends immediately.
Twenty minutes pass.
Druid later enters Earth Warden before having two more regular-turn markers.

Under the agreed rules, Recharge 2 matured roughly twelve seconds after combat ended.

Under the current helper, regular_index is still 5, so Slam remains blocked.

A completed short or long rest has the same problem. The rest functions reset source per-rest uses, but leave self.recharges untouched. 
Pasted text

So even an eight-hour long rest can leave a two-round Slam recharge artificially pending.

The current tests confirm cross-shift persistence and regular-turn ticking, but do not exercise out-of-initiative maturation or rest-spanning maturation. 
Pasted text

Required correction

Keep the owner/source-scoped recharge and cross-form persistence, but attach it to the canonical recharge clock, not exclusively to regular_index.

The corrected interface needs to accept both already-established clock paths:

in initiative: one tick at each actual owner regular start; extra turns never tick;
outside initiative: one tick per actual six seconds of elapsed canonical time.

Consequently:

12 valid out-of-initiative seconds make Recharge 2 ready;
a completed short/long rest necessarily leaves Recharge 2 ready;
shifting/reverting/reentering does not refresh it by itself;
initiative reorder/extra turns do not manufacture ticks.

I would not solve this by simply clearing recharge on rest only; that fixes the rest counterexample but still leaves ordinary 12-second downtime broken.

A regression set should include:

Slam → leave initiative → 6 seconds: still unavailable;
another 6 seconds: available;
Slam → completed short rest: available;
Slam → completed long rest: available;
no elapsed time + form reentry: still unavailable;
extra turn: no tick.
Everything else in the selected interface is acceptable

I found no additional blocker in the following reviewed machinery.

Buffer identity/arbitration: one active grant, greater replaces, equal/smaller rejected, no hidden underlying shield, zero creates no identity, fixed/dependency/default-LR lifetimes remain distinct. The implementation also correctly refuses stale recipient-rest epochs and requires scheduled expiry to settle before subsequent use. 
Pasted text

Linked versus independent riders: Bloodshield permission exists only on the accepted Bloodshield grant, while Overflowing Light's natural-expiry rider occurs only for the still-active exact grant. Replacement/depletion/dependency loss cannot later manufacture its cleanse. 
Pasted text

Core damage integration: the scalar temp-HP projection must match the grant ledger; one canonical damage identity resolves once; depletion updates the actual grant rather than creating another HP pool. 
Pasted text

Necrotic Affinity: the staged transaction matches the decision—after resistance/before old temp HP, one Reaction, half prevented, canonical packet finishes, then a new buffer is offered only to a surviving living holder. Duplicate absorption and duplicate post-packet grants are prevented. 
Pasted text

Spirit Walk: same-character area deduplication and the rule that the spirit can never be an attack target are represented correctly. No duplicate HP/resource/action ledger or fabricated transfer exists. 
Pasted text

Druid transaction identity: different-form entry spends the actual BA/shift before benefits, ends the old instance, preserves Dissonance, clears only Refrain state, spends the whole entry-buffer offer from Reserve before nonstack arbitration, and produces no zero-value grant. 
Pasted text

Renewal and forced ending: natural same-profile renewal retains the instance/local uses and extends only its own endpoint; voluntary reversion and actual 0/incapacitation/death terminate the form without a second damage resolution. 
Pasted text

Profile boundaries: original-owner PB/WIS/DC, explicit AC bridge, Elemental subtype mapping, Vermin subtype identity, no unrestricted weapon-proc permission, and no imported stat blocks are correctly represented. 
Pasted text

Surges/local uses: form-instance + special identity is correctly separate from source-wide rest/recharge clocks; Mooncursed uses one shared Howl opportunity and sequential Buffer Reserve allocation; Brood Spawn is entry-only. 
Pasted text

The source/disposition ledger also keeps the required unfinished work visible rather than silently deleting it, including Time Loop, Chef, Inspiring Leader, Soul Cage, Harmonic Bulwark, and all four polymorph-family spells. 
Pasted text
 
Pasted text
 
Pasted text

Disposition

With the submitted code:

IMPLEMENTED CANDIDATE — one exact recharge-clock correction required.

After Earth Warden Recharge 2 is moved onto the established dual-context recharge clock and the out-of-initiative/rest regressions pass, I see no other blocker to:

REVIEWED / reference-VALIDATED — selected temporary-HP grant/arbitration/lifetime interfaces, Druid same-body Shapeshift/form-instance interfaces, the 26 bounded Druid profiles, selected transformation-state bridges, Necrotic Affinity buffer staging, and Spirit Walk spatial-identity interface for this 175+5 corpus.

That closure would still leave explicitly open the equipment/anatomy matrix, global natural-weapon taxonomy, Blood Ritual target count and other unfinished feat clauses, Time Loop, Chef/Inspiring Leader/Soul Cage, Harmonic Bulwark, Shapechange/Polymorph/True Polymorph/Mass Polymorph, broader catalogs, human balance, and the complete tabletop/video-game runtime.
