# Actual GPT temporal control/pulse boundary conference

ChatGPT said:

The nine holder families can be given implementable temporal policies from the supplied source and reviewed guides. I would not reopen their non-temporal mechanics. The controlling principles are already explicit: source-qualified regular markers survive initiative changes, current-turn endings are distinct, and pulse schedules preserve their printed finite opportunities/costs. 
Pasted text
 
Pasted text

1. Clock descriptors

Accept the proposed descriptor, with one important distinction: Time Loop may recreate logical progress, but it never rewinds the underlying elapsed ClockMarker.

Use a wrapper such as:

Plain text
TemporalClockPolicy
    sourceId
    componentId
    origin:
        IN_INITIATIVE
        OUTSIDE_INITIATIVE
    kind:
        REGULAR_START
        REGULAR_END
        CURRENT_ACTUAL_TURN_END
        WORLD_ABSOLUTE
        PARENT_LIFETIME
    actorId?               # whose regular marker
    remainingBoundaries?   # snapshot remaining logical starts/ends
    absoluteDeadline?      # when source actually owns elapsed deadline
    parentEffectId?
    concentrationId?
A. REGULAR_START/END — restore snapshot remaining logical progress

These receive new iteration-qualified scheduler receipts after Time Loop. They receive no tick at commit.

The reviewed source table expressly puts these here:

Mage Cold passive/Bolt/Surge/Glacier → target next END.
Fusion cold/opportunity → target next END; Fire+Lightning → target next START.
Cascade → source next END / source next START.
Drakestorm Dive → source next END.
Elemental Lance → source next END / target next START.
Shaman Ice affinity and Elemental Chorus → source next END.
Ice Wisp → target next END.
Black Manifestation → source next START.
Judgment Brand → third future target END.
Sorrow's Weight → source next START or parent ends, whichever first.
Standing Stone → target next START.
Monk/Warrior custom Stagger → target next END.
Vein Cutter/Crippling Lash parent package → target next END unless its one-shot rider is consumed first. 
Pasted text

The same source-qualified procedure applies to Nerve Strike, Iron Leash, Divine Lockdown, Ray of Frost, Frost Arrow, Shardburst, Veinjammer, Slumber Glimpse, Brutal Strike and the other explicit “next regular turn” records supplied in the packet.

B. CURRENT_ACTUAL_TURN_END

Exactly:

Winter's Embrace;
Frost Totem;
Glue;
Resonant Seed slow;
Hold the Line when attached during the triggering enemy's current turn.

These are attached to the actual turn containing the application. They are not converted into “next turn.” The reviewed bridge says that when no turn exists, they instead use application + 6 seconds. 
Pasted text

Because the immutable Time Loop snapshot is at initiative start and therefore has no active actual turn, an in-progress CURRENT_ACTUAL_TURN_END attachment cannot legitimately be snapshotted there. Such a record either:

originated outside initiative and therefore already owns its absolute +6s deadline; or
indicates an invalid/incomplete snapshot.

Do not transplant it onto the first turn of the new iteration.

C. WORLD_ABSOLUTE

Any source that was using the reviewed outside-initiative elapsed deadline keeps that original deadline. Time Loop cannot extend it.

If it has expired by activation, it does not return.

D. PARENT_LIFETIME

Some control records are not independently timed:

Word of Binding;
Rootcall Quake;
later Mind Prison soft state;
Sorrow's Weight;
Standing Stone;
continuous aura selections;
Stonecore serum-side state;
physical Net Bolt state.

Their child Speed/control record cannot outlive or reconstruct its parent merely from a SpeedRecord.

Pulse schedules

For a pulse series whose source was established inside the rewound encounter, restore the snapshot's remaining regular-marker opportunities using the new iteration's authentic regular-start receipts.

For a source that was already running on an outside-initiative virtual/absolute schedule, preserve those original virtual markers; do not rebase them just because Time Loop occurred. The healing guide expressly says leaving/reentering initiative normally does not restart such clocks. 
Pasted text

That origin field is therefore mandatory.

2. SpeedRecord

Accept the basic restoration rule:

restore the same canonical application ID, source-qualified profile/magnitude, suppression state owned by the rewindable source, and snapshot remaining logical endpoint; do not call refresh_speed_record().

There is no new:

save;
cost;
application event;
slowed-foe entry hook;
immunity check;
source trigger.

Current unrelated external control/suppression records remain current and overlay the restored participant state. Unsupported overlays block.

Source-policy families

SpeedRecord may be admitted only through an explicit component policy table. The attachment supplies enough clock evidence for the selected source components; do not infer from a six-second number.

Three categories still require a parent-state adapter, though not additional rules text:

continuous relationship/aura records such as Reign of Ashes Aura and Iron Leash Aura;
physical-parent records such as Net Bolt;
form/serum/creature-parent records such as Stonecore or Ice-Wisp/Chorus state.

A naked SpeedRecord from one of those sources is insufficient.

Hypermutation Spike is not a hostile SpeedRecord; its movement floor remains systemic parent state.

The same is true of terrain movement cost.

No currently supplied Speed source needs invented clock evidence. A future component absent from the explicit source-policy registry remains unsupported.

3. GuidingStarMark and WrathfulBrand
Guiding Star

Accept with this exact split:

Rewindable snapshot state

same _identity;
owner;
target;
scaling s;
active;
attack_bonus_available;
hit_rider_available;
snapshot remaining source-qualified mark lifetime.

Conserved monotonic state

_next_token must never decrease;
historical issued/resolved attack-token identities remain reserved.

Required emptiness

_pending == empty at snapshot;
_pending == empty at Time Loop preflight.

A pending attack means the engine is not at an atomic Time Loop boundary.

After rewind:

Plain text
_next_token = max(snapshotNextToken, currentHistoricalNextToken)
_pending = empty

A later qualifying attack creates a new token, even though the mark itself has the same canonical identity.

This preserves the reviewed pre-roll +2 / later-hit-rider separation. 
Pasted text

Wrathful Brand

Restore:

same canonical parent/application identity supplied by the temporal wrapper;
timed Brand existence;
owner_rider_available;
ally_rider_available;
active state as of snapshot.

Its endpoint is source-next-regular-END. Current external suppression/eligibility is applied after restoration.

The owner rider and ally rider rewind independently. Spending either in the discarded iteration does not permanently consume the other.

Neither holder restoration is:

another RC payment;
another application;
another damage event;
another heal attempt;
another WIS save.
4. OneShotRider

The current bare dataclass is insufficient as the temporal identity by itself. Temporal integration must wrap it with:

Plain text
OneShotTemporalRecord
    applicationId
    sourceId
    componentId
    parentEffectId
    ownerId
    targetId
    triggerKind
    endpointPolicy
    snapshotAvailable

Use an explicit finite table.

Confirmed mappings
Component	Trigger
Tinker Target Scanner +1	attack — consumed on qualifying ally attack roll, hit or miss
Drake Mark bonus	hit — qualifying subsequent direct polearm hit
Soldier Marked for Death -1 damage	hit — first qualifying hit against another ally, even if final damage becomes 0
Vein Cutter -1 next attack damage	hit, with broad qualifying attack-damage predicate
Crippling Lash -1 damage	hit, weapon hit only
Balanced Scales retaliation	damage, requiring positive resolved damage
Omen Reader -2	attack, before the identified enemy rolls the qualifying attack
Slumber Glimpse +2 next attack	attack, on the qualifying attack roll
Paladin Vengeance Retribution die	hit, but only an otherwise legal Smite against its parent mark

The last two should be included if the generic adapter is intended to cover every supplied compatible holder rather than only the initially proposed subset.

Vein Cutter clarification — NEW temporal/trigger bridge

The source says “-1 next attack damage,” not “next attack roll.” A miss has no attack damage to modify. Therefore a miss does not consume this rider; the next qualifying hit does.

Crippling Lash is narrower because it expressly says “next weapon hit.”

Omen Reader clarification

The one-shot record is the once/encounter -2 before the enemy's attack roll. Its resulting star-ash mark is a separate timed parent state lasting target-next-END. Do not treat star-ash itself as the one-shot entitlement. 
Pasted text

Carrion Conductor

Correctly excluded. Its used-corpse identity is conserved physical/source history, not a temporal one-shot view. The reviewed guide expressly makes it persistent across expiry, use and suppression. 
Pasted text

5. PerTurnReflection

Confirm.

used_turn_ids becomes historical evidence, not a set that Time Loop truncates to snapshot.

Use actual temporal turn identity:

Plain text
(encounterOrigin, iteration, targetActor, actualTurnId)

A new target turn in a new Time Loop iteration therefore does not collide with an old discarded-timeline turn.

Divine Judgment can trigger once on:

a genuine regular target turn; or
a genuine separately authorized extra target turn.

It cannot trigger:

at Time Loop restoration;
from an old damage event being replayed;
from off-turn damage;
from a fabricated regular start used to emulate an extra turn.

The source clarification expressly says reflection is once each actual target turn, including extra turns, while its repeat save and duration remain regular-marker based. 
Pasted text

Until the eventual scheduler supports authenticated extra-turn receipts, extra-turn reflection should remain unavailable rather than mapped onto a normal regular turn.

6. PulseSeries

Your proposal is correct, with the following mode-specific procedure.

The series retains:

same instance_id;
exact source/profile;
fixed roster where applicable;
original activation provenance;
parent/concentration/deployment dependencies;
snapshot states;
snapshot declarations;
snapshot application view;
source-specific finite pulse count.

The reviewed source schedule is controlling. 
Pasted text

Historical versus rewindable state

Maintain two layers:

Historical

old pulse event IDs;
old resource expenditure;
old healing/damage applications;
resource-generation opportunities governed by #7;
reward/proc history.

Temporal series view

snapshot states;
declarations already present at snapshot;
recipient applications already present at snapshot;
pending/funded opportunities as they stood at snapshot.
Maintenance mode

Examples: Healing Briar, Circle, Restoration Field, Renewal, Sacrament.

If a later maintenance opportunity was pending at snapshot:

new iteration reaches its corresponding authenticated source regular turn;
pay the printed current RP/action cost again;
old discarded-timeline RP remains spent.

If that opportunity was already committed at snapshot, do not charge again.

If payment fails at its actual maintenance window, apply the ordinary source end procedure. No retry/catch-up.

Sequence mode

Examples: Song, Transcendent, Eternal Bloom.

Prepaid opportunities remain prepaid.

Song's later RC costs are not prepaid; the restored pending pulse pays current RC again when its logical due event occurs.

Delayed sequence

Hemostasis / Cellular Reconstruction / Cleric Echoes / Wound Eater:

same stored sequence identity;
same remaining opportunity count;
genuine restored due event can occur once;
source-specific later costs still apply where printed;
no catch-up at commit.
Window mode

Garden, Seed, Burning Blood:

a window that was already funded at snapshot stays funded;
a later window that was pending at snapshot must be funded again at its new due marker;
discarded-timeline payments remain spent.

No target receives a benefit merely because the window was restored.

Command mode

Nano-Aegis:

same mode/instance;
restore snapshot remaining command-count view;
every post-snapshot replayed command again requires the current 1 RP and a current legal Bonus Action;
the later device/command adapter must certify that command legality and the shared companion budget.

No second PulseWallet may own canonical resources.

Canonical wallet adapter

Use a transaction façade over the real world ledgers:

RP → current canonical character Wallet;
RC → the Time Loop-restored canonical Oracle RC state;
Bonus Action → authenticated current turn/action budget.

Never deepcopy RP/RC into PulseWallet, spend the copy and merge it back.

The attachment correctly notes that RC is specifically rewindable by Time Loop; RP is not.

RecipientLedger

The existing (domain,target,round_number) key is insufficient under Time Loop.

Use:

Plain text
(domain, target, IterationRoundId)

while retaining all old iteration claims historically.

Thus a restored Circle can affect the same target in the new iteration's round 1, while the old round-1 claim remains audit history.

named:Circle of Harmony remains global across owners within the same iteration-round, as already reviewed. 
Pasted text

Parent lifetime

If the required parent/concentration no longer exists and cannot itself legally be restored, the PulseSeries cannot be independently resurrected.

A world-expired outside-origin series does not return.

No restoration operation creates a pulse.

7. Independent outputs

The proposed conservation guard is necessary, but it must cover two supplied resource outputs, not only Transcendent Meditation:

Transcendent Meditation — pulse 2 → +1 Ki.
Sacred Chant — pulse 3 → +1 Conviction.

Both Ki and Conviction are explicitly not restored by Time Loop, so allowing the same source occurrence to generate them repeatedly would be a temporal resource exploit.

Use:

Plain text
IndependentOutputOpportunityKey
    canonicalEffectInstance
    pulseIndex
    componentId
Consumption decision

NEW conservation bridge:

The opportunity is permanently consumed when that exact independent-output occurrence is actually reached/resolved in any timeline, whether the resulting resource increase is positive or capped at maximum.

If the whole effect is suppressed at that occurrence, the source says the component is lost for that occurrence; mark the independent-output opportunity consumed. The healing guide explicitly says Transcendent's suppressed occurrence grants no Ki and that missed independent output is not banked. 
Pasted text

Therefore:

pulse occurred, +1 Ki gained → consumed forever;
pulse occurred while already at Ki cap → consumed forever;
pulse occurred while whole effect suppressed → consumed forever;
pulse was never reached before Time Loop → still eligible when the genuinely replayed due pulse occurs;
restoration itself never grants the resource.

Same policy for Sacred Chant's Conviction pulse.

This is intentionally stricter than ordinary replayable healing because these are conserved finite resources.

BG/Ki/Conviction/material costs already spent remain spent.

Eternal Bloom installments are healing effect-state, not resource pools.

8. BloomReserve and FirstContactLedger
BloomReserve

Confirm.

Immutable for the parent Bloom instance:

original selected roster;
original roster_missing;
derived installment shares.

Never recompute from restored/current HP.

Never enlarge after later damage.

Time Loop restores the snapshot installment-consumption view but retains historical consumption events under iteration-qualified audit IDs.

Example:

Plain text
snapshot consumed = {0}
discarded iteration later consumed 1
rewind -> active view consumed = {0}
history still contains iteration0/installment1

Installment 1 may then occur once in the new iteration at its authentic scheduled opportunity.

The separate 1-HP survival floor is not part of BloomReserve; its own one-shot temporal adapter owns that state. The reviewed guide already separates these. 
Pasted text

FirstContactLedger

Restore the snapshot per-instance entitlement view.

Exact event policies remain:

Garden → first legal entry or start;
Enhanced Garden → first eligible pulse, replacing the ordinary Garden contact cure;
Resonant Seed → first eligible healing pulse, not entry.

A Time Loop commit itself is never entry/start/pulse.

Post-snapshot consumed contact

Yes. If it was unconsumed at the initiative snapshot but consumed later in the discarded timeline, a genuinely new source-qualified event in the new iteration may consume it again.

That is ordinary effect-state rewind, not a finite-resource refund.

Historical record should therefore use something like:

Plain text
(instanceId, targetId, iterationId, eventId)

while active availability restores from snapshot.

If the entitlement was already consumed at snapshot, it stays consumed.

If the event was source-ineligible/suppressed and no entitlement was consumed, it remains available.

A legal contact with no useful ailment still consumes the “first contact” opportunity where the source says first entry/start/pulse; it is not banked until the player later develops a condition.

No real-rest family history is modified.

9. NativeOccurrenceLedger

Confirm the need for a new temporal key, but correct one phrase:

Native recurrence is regular-start only. Extra turns do not receive these recovery ticks.

The reviewed healing guide explicitly says extra turns provide no new periodic recovery tick. 
Pasted text

Use an authenticated scheduler receipt:

Plain text
NativeOccurrenceKey
    sourceId
    ownerId
    IterationTurnId  # genuine REGULAR start only

Do not use the bare ClockMarker as identity.

World seconds may be identical across adjacent logical events; the scheduler's actual iteration/turn receipt is the authority.

Source treatment

Aura of Grace

genuine owner regular start;
current eligibility;
optional current 1 RP payment;
no free heal on restore.

Living Pulse

same;
current natural-terrain/HP/incapacity requirements.

Thief Exsanguinate

same;
current hostile bleeding enemy check.

Regenerative Mutation / Bloodthick Node / Rapid Coagulation

genuine regular start only;
current mutation/source eligibility;
current Mutation Recovery Reserve;
spend reserve only for actual HP restored under their reviewed procedure.

Do not copy a reserve into the occurrence ledger.

One evaluation per start

The temporal wrapper should additionally record the occurrence as evaluated, not merely successful.

Thus on one authenticated regular start:

declined optional RP heal → cannot retry later that turn;
source ineligible → cannot become eligible later that turn and retry the start trigger;
payment unavailable → start opportunity is gone;
eligible and resolved → ordinary result.

A new Time Loop iteration supplies a genuinely new IterationTurnId, so there is a new source opportunity, but all current RP/Mutation Reserve expenditure remains conserved.

No outside-initiative recurrence

These exact native sources require a real encounter regular start. They receive no six-second out-of-combat healing tick.

Rapid Coagulation dependency

Its rule depends on “did not move during your previous turn.” The temporal policy is clear:

for later turns in the new iteration, use movement history from that new iteration;
discarded-timeline movement cannot satisfy it.

For the first restored turn, the adapter must use the canonical movement-history baseline that existed at the initiative snapshot.

The supplied packet does not include that movement-history holder. Until the combat/movement scheduler exposes it, Rapid Coagulation should remain unsupported in the temporal NativeOccurrence adapter, rather than guessing “didn't move.”

That is a missing state adapter, not missing card text.

Implementable disposition

I would record this conference as:

SOURCE-DISCUSSED / IMPLEMENTATION-READY — temporal policies settled for SpeedRecord, GuidingStarMark, WrathfulBrand, finite OneShotRider sources, PerTurnReflection, PulseSeries, BloomReserve, FirstContactLedger and NativeOccurrenceLedger.

Two important additions to the proposed design are:

Sacred Chant's Conviction needs the same conserved independent-output opportunity protection as Transcendent Meditation's Ki.
NativeOccurrenceLedger must use genuine regular-turn receipts only; extra turns do not produce periodic healing.
Still required before this integration itself can close

No additional card text is needed for the nine families as supplied. The outstanding dependencies are implementation/state adapters:

canonical concentration/parent-effect identity for concentration-bound control and PulseSeries;
authenticated regular/extra-turn receipts from the scheduler;
canonical RP/RC/Bonus-Action façade rather than copied PulseWallet;
historical/active generation wrappers for RecipientLedger, installment/contact consumption and one-shot riders;
actual movement-history state for Rapid Coagulation's first restored turn;
parent physical/device state for Net Bolt, Totem/Echo, Nano-Aegis and other source-dependent records.

If any of those parents is active without its adapter, the Time Loop snapshot remains unavailable. The helper class name, a component ID, or a six-second-looking deadline is never sufficient permission to admit it.

This remains only the control/healing-pulse policy conference; full Time Loop, the other six major integrations after this one, and the final whole-game/GitHub gate remain open.
