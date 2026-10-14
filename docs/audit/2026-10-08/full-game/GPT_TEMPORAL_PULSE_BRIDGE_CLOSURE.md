# Actual GPT bounded pulse bridge review

ChatGPT said:

I find no reproducible blocker inside this explicitly limited payment/resolved-output scope. The 22-test bridge is consistent with the nine-policy conference, and the guide correctly avoids claiming clock restoration or active control/pulse admission. 
Pasted text

1. Maintenance-payment wording — confirmed

Your interpretation is correct and should control implementation.

For an ordinary maintenance window such as Healing Briar, Circle of Harmony, Renewal, Sacrament, etc., an early failed attempt does not immediately destroy the opportunity. The opportunity remains pending until its actual source-turn maintenance deadline. If payment/action becomes legal before that deadline, it may still be completed. Only reaching the deadline without successful maintenance ends the source.

That is exactly how the existing reviewed PulseSeries.resolve() behaves: maintenance uses a window, while exact-due paid sequence opportunities have different failure semantics. 
Pasted text

So preserve this distinction:

ordinary maintenance window: early payment/BA failure → no mutation, still pending; unresolved at turn-end → source ends;
exact-due paid sequence/delayed-sequence: failure at the exact due marker → source/opportunity ends immediately;
funded window: failure to fund at its exact registered marker → window/source ends immediately;
prepaid sequence: no new payment is invented.

The new canonical payment façade supports that correctly because it validates balance and Bonus Action before mutating either RP/RC or the Action budget. 
Pasted text

The corrected test is also right: a later prepaid opportunity is not invalid merely because an earlier opportunity was missed where the ordinary source permits that schedule. 
Pasted text

2. Immutable snapshot membership — confirmed

Also correct.

The Time Loop snapshot exists at original initiative start, before the first turn or combat event. Therefore:

A source instance created after that immutable boundary is not snapshot state and cannot be reconstructed by Time Loop.

No temporal descriptor, origin flag or logical-clock conversion can retroactively make it a snapshot member.

So there are three different cases:

Source existed at snapshot and originated outside initiative.
It is eligible for snapshot admission if its exact source adapter supports it, but keeps its original outside-initiative virtual markers/absolute deadlines. Time Loop does not rebase those markers.

Source existed at snapshot and already had a legitimate in-initiative logical-marker identity.
Its remaining logical progress may be restored only if such a source can actually exist at that boundary according to its exact provenance.

Source was first created after snapshot.
It disappears with the discarded timeline; its activation payment/use remains conserved where applicable. It is not restored.

For the currently supplied PulseSeries profiles, I do not see an authentic source that needs a special “created at the initiative snapshot itself” exception. Their actual series creation is driven by an Action, Bonus Action, trigger or other event; the snapshot explicitly precedes such encounter events. The legitimate pulse series present at capture will therefore normally be effects that were already running before initiative and carry their preserved outside-origin schedule.

Permanent/passive abilities such as Aura of Grace or Regenerative Mutation are different: the ability exists at the boundary, but a healing occurrence does not. Their next recovery opportunity arises only from a future authenticated regular start. They should not be materialized as a PulseSeries at capture.

Likewise, an initiative-specific source such as Omen Reader may eventually need its own initiative/setup ordering, but that is not a reason to fabricate a PulseSeries instance. If a future exact source explicitly says that an effect is created when initiative begins, that source will need a dedicated ordering rule specifying whether creation occurs before or after the immutable Time Loop snapshot.

Your guide wording at lines 451–453 is therefore correct. 
Pasted text

Limited code review

CanonicalPulseWallet is acceptable for this stage. It owns no duplicate RP/RC pool, resolves RP and Bonus Action against the canonical actor Wallet, resolves RC against the canonical Scheduler, checks alias/binding changes before payment, and performs all affordability checks before mutation. 
Pasted text

ConservedPulseOutputs also correctly implements the two currently settled independent outputs:

Transcendent Meditation pulse index 1 → Ki;
Sacred Chant pulse index 2 → Conviction.

The guard only creates an allowance after an actual successful PulseSeries.resolve(), permanently reserves the instance/index/resource opportunity once reached, consumes it under whole-effect suppression, prevents event replay, and removes the old unguarded independentKi authorization from the returned result by replacing it with the guarded value. 
Pasted text

The test cases cover the important conservation cases: normal Ki/Conviction, replayed snapshot views, suppression, resource cap, never-reached opportunities, non-encounter Chant, duplicate events, payment failure, and healing-independent Ki. 
Pasted text

One implementation requirement remains exactly as your guide states and is not a blocker in this limited checkpoint: the returned allowance and actual Ki/Conviction mutation must eventually participate in the same atomic source transaction. Until that host mutation exists, this helper is an authorization guard, not the resource application itself. 
Pasted text

Bounded disposition

Record this portion as:

REVIEWED / reference-VALIDATED — canonical PulseSeries RP/RC/Bonus-Action payment bridge and resolved Transcendent-Meditation-Ki / Sacred-Chant-Conviction conservation guard only.

The validation reports 22 passing methods, zero failures/errors and correctly states that timing/source restoration remains unimplemented. 
Pasted text

This does not approve source-clock restoration, snapshot serialization of the nine families, concentration/parent reconciliation, native-start receipts, missed-output reconciliation, or final Ki/Conviction mutation. Full control/pulse restoration and all seven larger Time Loop integrations remain open, as do the final whole-game flow and GitHub gates.
