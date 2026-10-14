# Actual live control/pulse integration findings

ChatGPT said:

I do not close the live-holder candidate yet. The foundation extension is generally coherent, and most of the 36 new checks exercise the right boundaries, but I find five concrete blockers in the admitted integration scope, plus one source-policy item that should be settled before implementation continues.

The existing limits are stated correctly: the candidate is not full Time Loop, later parent/device/form/mutation integrations remain unavailable, and a BoundEffect is not evidence that the entire source card executed. 
Pasted text

1. A missed-upkeep Garden can still fire its child contact

This is the clearest live-path defect.

_event() verifies that a pulse parent has ended_at is None, but it does not advance the parent to current world time before making that determination. contact(... event='start') then checks the target's authentic start and directly consumes the contact entitlement. 
Pasted text
 
Pasted text

Reproducer:

Garden exists before initiative.
Its initial window is funded.
The source reaches the later funding marker and does not pay.
No call to fund_window()/target_start()/advance() happens at that moment, so the raw PulseSeries.ended_at is still None.
At a later ally regular start, call the Garden first-contact cure.

contact() sees an apparently live parent and permits the cure, even though PulseSeries.advance(now) would have ended Garden at the missed funding marker.

Your current regression manually calls parent.end(...), which tests an already-reconciled parent, not this stale missed-upkeep state. 
Pasted text

Repair: every child operation must first establish the parent is currently live according to its clock. For a pulse parent, clone/advance it to now; if that projection says the parent should already have ended and the real parent has not been lifecycle-reconciled, reject with the existing missing-parent-lifecycle dependency. Do not grant the child benefit.

This is not asking you to implement parent retirement yet. Blocking the stale parent is sufficient for this candidate.

2. Snapshot RecipientLedger.claimed can silently import an unsupported outside-initiative round

The code correctly adds iteration-qualified historical tokens, but the active claimed view remains the old (domain, target, numericRound) structure. 
Pasted text

Capture simply serializes that active set, and restoration puts snapshot claims for roster members directly back into it. 
Pasted text
 
Pasted text

That is unsafe while outside-initiative round-ledger import is explicitly unimplemented.

Reproducer:

Plain text
before capture:
claimed = {("named:Circle of Harmony", "b", 1)}

Because the immutable snapshot is before the encounter's first turn, that claim cannot have originated from this encounter's actual numbered round 1; it must be an outside/previous virtual-round claim requiring the missing import policy.

Capture currently accepts it.

After rewind, scheduler round becomes 1 and the same raw claim is restored. A genuine new-iteration round-1 Circle attempt against B is then rejected by the active ledger even though its conserved history has no new-iteration claim.

The opposite interpretation could also be wrong—which is exactly why the missing outside-round mapping must not silently opt in.

Repair: until the outside-initiative round-ledger adapter exists, reject capture if an active RecipientLedger.claimed entry involving a snapshot participant already exists. Outsider-only current claims can remain conserved. Once the import adapter exists, convert each legitimate outside domain to an explicit qualified baseline instead of pretending its numeric round is encounter round 1.

3. The approved independent-output guard and the new world use two different conservation ledgers

The approved payment/output bridge has its own canonical:

ConservedPulseOutputs.consumed
ConservedPulseOutputs.events. 
Pasted text

The new live world separately creates:

TemporalControlWorld.independent_consumed
TemporalControlWorld.events. 
Pasted text

And resolve_pulse() reimplements the Ki/Conviction guard instead of delegating to the previously approved one. 
Pasted text

That makes the two independently passing test suites non-compositional.

Concrete counterexample:

Register Transcendent Meditation's PulseSeries with the previously approved ConservedPulseOutputs.
Resolve pulse 2 through that approved bridge; it grants the one Ki and records the opportunity in guard.consumed.
TemporalControlWorld.independent_consumed remains empty.
Restore a snapshot view where pulse 2 was pending.
Resolve it through TemporalControlWorld.resolve_pulse().

The new world sees its own empty set and can authorize the same Ki again.

Repair: there must be exactly one canonical independent-output conservation ledger. Either make TemporalControlWorld own/use ConservedPulseOutputs, or migrate that approved state into a shared ledger both APIs reference. Do not leave two valid resolution paths with separate conservation histories.

This is separate from the acknowledged missing final Ki/Conviction pool mutation. The defect is in the already-implemented once-per-effect authorization itself.

4. Speed suppression can be rewound even though its provenance is unknown

Your settled policy says current external suppression remains authoritative. The live adapter cannot currently prove that.

IMMUTABLE_FIELDS['speed'] deliberately excludes suppressed. 
Pasted text

During restore, the full snapshot SpeedRecord payload—including its old suppressed Boolean—is reconstructed and replaces the current value. 
Pasted text

Reproducer:

Snapshot SpeedRecord: suppressed=False.
After snapshot, a conserved/external source begins suppressing that control record: suppressed=True.
No suppression provenance adapter exists.
Time Loop restores the old record with suppressed=False.

The current external suppression has silently disappeared.

The reverse ambiguity also exists: a suppression caused only by the discarded timeline may need to disappear. A bare Boolean cannot distinguish them.

Repair: until suppression provenance is supplied, do not rewind a changed SpeedRecord.suppressed value. Safest bounded rule:

unchanged suppression → admit;
changed suppression with no classified provenance adapter → Time Loop unavailable;
later source adapter → explicitly decides rewind versus conserved overlay.

If an active snapshot record is already suppressed and you cannot identify why, I would likewise require a suppression dependency rather than treating the Boolean as self-authorizing.

5. Prepared Time Loop plans do not watch ConcentrationLedger schema

The adapter validates at preflight that the concentration object contains exactly {'current'}. 
Pasted text

But watch() only watches:

the concentration binding;
its current binding;
the identities of entries inside current.

It does not call tx.watch_shape(self.concentration). 
Pasted text

Reproducer:

Plain text
plan = kernel.kernel_plan("a")
control.concentration.new_temporal_state = ...
plan.commit()

The plan can still commit because the object identity and current registry are unchanged.

That breaks the foundation's established invariant that dynamically added/unclassified live state after preflight makes a prepared temporal plan stale.

Repair: add:

Plain text
tx.watch_shape(self.concentration)

and, if future concentration fields become legitimate, classify/watch them explicitly.

This is a small repair but belongs in this checkpoint because it changes the previously approved foundation's stale-plan guarantees.

Source-policy defect: Eternal Bloom concentration is currently omitted

This one is not merely a missing future parent adapter; the supplied source evidence already answers it.

The source alias for Eternal Bloom includes oracle.engine[26]. 
Pasted text

That engine explicitly says persistent damaging/healing zones require concentration. 
Pasted text
 Eternal Bloom is a fixed 5-tile sanctuary delivering three scheduled healing installments. 
Pasted text

But the candidate's CONCENTRATION_PROFILES omits eternal-bloom, so your current Bloom tests legally construct and capture it without any concentration identity. 
Pasted text

Required repair: eternal-bloom must require concentration and the same exact-current-concentration validation as the other Oracle persistent healing zones.

There is a closely related Crown Restored question. Its alias also includes oracle.engine[26], and it is a three-round ally-healing aura. 
Pasted text
 
Pasted text
 I find no supplied exemption saying Finals ignore the engine's concentration clause. Unless you have an exact reviewed exemption elsewhere, I would add crown-restored to the concentration-required set as well. If an exemption exists, that exact evidence should be attached rather than inferred from “Final.”

What looks good

The small foundation extension itself has the right architecture: adapter payloads are part of the immutable snapshot, the adapter set is watched, adapter state is staged into the same core transaction, and the scheduler's start/body phase prevents ordinary body events from masquerading as authenticated regular-start triggers. 
Pasted text

I also find the following bounded pieces sound:

post-snapshot control records retire instead of acquiring snapshot membership;
Guiding Star preserves same-object entitlements while keeping the token sequence monotonic;
Divine Judgment preserves actual-turn consumption across iterations;
Hemostasis correctly keys off the target's regular start;
Bloom/contact require same-iteration parent receipts where implemented;
expired outside-origin pulse opportunities are advanced/lost without catch-up healing;
current concentration replacement/disappearance is caught for profiles that are actually marked concentration-dependent;
RP/RC/Bonus Action payments still use the canonical bridge rather than a copied PulseWallet;
post-snapshot RP stays spent;
external participant overlays conservatively block;
Rapid Coagulation, device/stasis/copy parents, entry receipts and mutation-reserve recurrence remain explicitly unavailable rather than guessed. 
Pasted text
Disposition

I would currently record this as:

LIVE CONTROL/PULSE TRANSACTION CANDIDATE — substantial bounded implementation, but five code blockers plus the Eternal-Bloom concentration-policy correction remain before this integration receives REVIEWED/reference-VALIDATED status.

The 36 + 76 + 22 passing checks remain useful engineering evidence, but they do not yet compose into a safe control/pulse checkpoint because of the split independent-output ledger and the uncovered stale-parent/snapshot-admission cases.

None of this closes full Time Loop. The remaining transformation, Druid, creature, device, remaining-lifecycle, full FeatWorld and broader parent/source integrations remain open, as do the final joint whole-game flow and GitHub authorization gates.
