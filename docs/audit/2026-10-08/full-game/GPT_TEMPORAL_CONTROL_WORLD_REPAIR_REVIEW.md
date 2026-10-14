# Actual review of 44-method repair

ChatGPT said:

The five prior integration findings are repaired, and both Oracle-zone concentration corrections are now implemented correctly. In particular, the shared ConservedPulseOutputs object is genuinely canonical across the old and new resolution paths; stale child parents are projected before use; participant pre-initiative recipient claims are rejected; unknown Speed suppression no longer rewinds; concentration schema changes stale a prepared plan; and both Eternal Bloom and Crown Restored now require concentration. 
Pasted text

I still find two reproducible admission defects before I would mark this live-holder integration REVIEWED/reference-VALIDATED.

1. An active PulseSeries does not have to actually exist yet at the immutable snapshot

The code verifies the PulseSeries structure and reconstructs its schedule, but does not compare h.activation to the snapshot's current world marker. Then capture_payload() only requires non-native sources to say origin == 'outside'. 
Pasted text
 
Pasted text

Concrete reproducer:

Plain text
snapshot world time = 0

Transcendent Meditation PulseSeries:
    activation = 6
    future starts = 12, 18, 24
    origin = "outside"
    concentration ID is currently present

The series claims it will not activate until world second 6, yet capture at second 0 accepts it as preexisting snapshot state.

At second 6, an authenticated regular start can then resolve pulse 0 from a source that did not exist at the snapshot boundary. Its printed activation transaction — Action, 3 Ki, 4 RP, short-rest use — was never established by the captured world.

That conflicts directly with the agreed rule that a source created after initiative-start cannot acquire snapshot membership merely through an origin label. 
Pasted text

A related case is an outside-origin maintenance series that had already missed upkeep before capture but whose live holder has never had advance() called. Capture currently accepts that stale source as active.

Required repair: validate actual snapshot membership non-mutatively during capture_payload().

For every active PulseSeries:

Plain text
require(h.activation <= scheduler.now)

projected = plain_clone(h, payload(h))
projected.advance(scheduler.now)

require(projected.ended_at is None)

and require its current absolute deadline has not already passed. This should only validate; it should not mutate the holder at capture.

That closes both the future-activation and already-dead-at-snapshot cases.

2. BoundEffect.component is not validated for pulse, Bloom, contact, or native records

For speed, guiding, brand, rider, and reflection, the implementation correctly requires the exact (source, component) entry in CONTROL_POLICIES. 
Pasted text

But after entering the pulse branch, record.component is never checked. The code validates profile_name, source, holder, roster, schedule and concentration, but not the component metadata stored in the BoundEffect. Bloom/contact/native likewise don't validate their component identifiers. 
Pasted text

Concrete reproducer:

Plain text
record = valid Song of Mending BoundEffect
record.component = "future.unreviewed.component"

capture()

Everything else can remain canonical and capture still succeeds.

That matters because the stated contract is that BoundEffect is the selected component's source binding and unknown source state must not opt in. The mechanics currently come from profile_name, so this is primarily a provenance/admission defect, not a numerical behavior defect, but strict provenance is part of this integration's claimed scope.

Required repair: use an explicit finite component policy for these remaining families. For example:

Plain text
pulse:
    component == exact temporal pulse alias/profile binding

bloom:
    component == "installments"

contact:
    component == "first-contact"

native:
    component == "regular-heal"

or an equivalent explicit table if you want more descriptive canonical IDs. Do not infer them from class names.

What is now sound

I do consider the previously reported issues closed. The shared output guard now has one consumption history across direct-guard and world paths, and the world watches that guard's schema, registrations, events and consumption state. 
Pasted text
 
Pasted text
 
Pasted text

The repaired stale-parent check also correctly projects a PulseSeries to current time without mutating it before allowing a child operation. 
Pasted text
 The new regression addresses the exact missed-upkeep Garden case from my previous review. 
Pasted text

The Oracle correction is also supported by the supplied evidence: oracle.engine[26] requires concentration for persistent damaging/healing zones, so requiring it for Eternal Bloom and Crown Restored is the conservative source-consistent interpretation. 
Pasted text
 
Pasted text
 
Pasted text

Current disposition

LIVE CONTROL/PULSE TRANSACTION CANDIDATE — previous five findings and Oracle concentration omissions resolved; two narrow snapshot/provenance admission blockers remain.

The reported 44 integration + 76 foundation + 22 payment/output checks are useful and the validation remains correctly bounded with fullTimeLoopOperational: false. 
Pasted text

Neither remaining issue needs new source evidence; both are implementation admission checks. The larger Time Loop integrations, full nine-family/source lifecycle work, final whole-game flow review, and GitHub authorization remain open.
