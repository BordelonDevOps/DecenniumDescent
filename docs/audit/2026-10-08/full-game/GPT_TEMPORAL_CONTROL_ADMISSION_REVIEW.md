# Actual review of 49-method admission repair

ChatGPT said:

The two follow-up admission findings are repaired correctly, and the missed Eternal Bloom installment correction is consistent with the reviewed clock policy. The new component admission checks and non-mutating snapshot-membership projection close the exact defects from the 44-method review. 
Pasted text

I find one remaining reproducible blocker in the admitted concentration integration before I would close this bounded live-holder checkpoint.

Confirmed repairs

Pulse snapshot membership is fixed. An active pulse now has to exist by the actual snapshot marker, remain before its absolute deadline, and survive a non-mutating advance(snapshotTime) projection. A future activation, stale missed-upkeep series, or already-expired series therefore cannot acquire snapshot membership merely by claiming origin='outside'. 
Pasted text

Component provenance is fixed. Pulse records now require their exact admitted profile/component identity, while Bloom, contact and native records require the finite installments, first-contact, and regular-heal component identities. 
Pasted text
 
Pasted text

The added collection validation also closes the four demonstrated partial-mutation cases. The guard, recipient ledger, pulse holder and native holder can no longer proceed far enough to spend resources or consume opportunities after those canonical collections have been replaced with malformed list state. 
Pasted text

Eternal Bloom correction — confirmed

The new rule:

Plain text
consume every installment whose original open marker < current world time

is the right temporal reconciliation.

It correctly means:

snapshot at installment 0;
rewind at second 7, after installment 1's original second-6 opportunity;
installment 1 is now lost/consumed without healing;
installment 2 at second 12 remains legally scheduled;
restoration does not recompute missing HP or create any recovery;
an opportunity exactly at now remains available because the comparison is strict <, not <=.

That matches the previously reviewed rule that a missed prepaid Bloom share is lost while later shares remain on their original schedule. The implementation applies the same projection both during restore and immediately before an actual consume_bloom() call. 
Pasted text
 The regression demonstrates the intended {0} → {0,1} reconciliation at second 7 followed by the legitimate third share at second 12. 
Pasted text

Remaining blocker: concentration callback identity can change after snapshot

The current concentration checks establish that the concentration ID is still present, but the immutable snapshot does not bind the actual concentration slot/callback identity.

The unchanged live-world code validates a slot as a tuple (concentrationId, callback) and, for an active source, tests only:

Plain text
current[0] == record.concentration_id

Pasted text

At snapshot, capture_payload() does not record the current concentration tuple or callback identity. 
Pasted text

The transaction does watch the concentration registry, so replacing the callback after preflight is correctly detected as stale. 
Pasted text
 But replacement between snapshot and preflight is still accepted.

Reproducer

At snapshot:

Plain text
concentration.current["a"] =
    ("pulse", callback_that_ends_pulse)

After snapshot but before Time Loop preflight:

Plain text
concentration.current["a"] =
    ("pulse", some_other_callback)

The concentration ID is still "pulse".

validate() accepts the tuple because it is structurally valid. The source's concentration_id still matches current[0]. stage_restore() therefore accepts the concentration as the exact parent and can restore the pulse.

Later:

Plain text
concentration.end("a", "failure")

invokes some_other_callback, which may fail to retire this restored source.

That leaves the restored source alive after its supposed concentration parent ends.

This is exactly the sort of same-ID/replaced-identity case the temporal kernel has consistently treated as unsupported rather than equivalent.

Required repair

Capture a stable concentration-binding fingerprint for every active concentration-dependent snapshot record. For example:

Plain text
concentrationBindings[effectId] = {
    ownerId,
    concentrationId,
    slotIdentity,
    callbackIdentity
}

The actual snapshot payload can store deterministic/reference tokens rather than the callable itself. In this reference implementation, object-identity tokens are sufficient.

At preflight require:

Plain text
current concentration ID == snapshot ID
AND
current slot/callback identity == snapshot binding

If the same textual concentration ID has been detached/reconstructed/rebound since capture, reject until the future full concentration/restoration adapter explicitly authorizes that transition.

Also add the inverse regression to the existing after-preflight stale test:

create concentration;
capture;
replace tuple with same cast ID but different callback;
complete an event;
kernel_plan() must reject with no mutation/cost.

This needs no new source ruling. It is a canonical identity/admission requirement.

Disposition

So I would record the 49-method revision as:

LIVE CONTROL/PULSE TRANSACTION CANDIDATE — both prior admission findings, malformed-collection partial writes, and missed-Bloom reconciliation resolved; one concentration binding-identity blocker remains.

The reported validation remains properly bounded: 49 integration methods pass, with fullTimeLoopOperational: false, while the unchanged 76 foundation and 22 payment/output suites remain passing. 
Pasted text

Once the same-ID/different-callback concentration case is rejected, I do not currently see another blocker in this admitted control/pulse transaction scope. Full nine-family completion, final HP/Ki/Conviction mutation, the seven broader integrations, whole-game flow confirmation, and GitHub authorization all remain open.
