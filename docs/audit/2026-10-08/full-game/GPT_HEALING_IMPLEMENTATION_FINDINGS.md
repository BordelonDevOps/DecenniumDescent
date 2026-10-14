# Exact healing/death implementation findings

Captured from the completed Calibration Review reply.

There is one material contradiction and one still-open implementation choice that should now be closed before I would accept this bounded package. I do not find a separate blocker in the six dormant spell drafts.

1. Material bug: blocked natural-20 death save is wrong

The previously reviewed Decay rule is explicit: if a natural-20 death save's 1 HP recovery is blocked, the creature clears its death counters and becomes Stable at 0, with the ordinary d4-hour Stable recovery deadline. 
Pasted text

But the new death_save_with_survival() does the opposite:

natural 20 + HP prohibition → restore the original dying state, no stability. 
Pasted text

Its validation even asserts that result: HP0, not Stable, two failures retained. 
Pasted text

Worse, the same submitted package still contains death_save_with_hp_prohibition(), which does stabilize the blocked natural-20 result. 
Pasted text

So there are currently two incompatible implementations of the same reviewed rule.

Required correction

In death_save_with_survival():

natural 20 is rolled legally;
its 1 HP direct recovery is blocked;
clear successes/failures;
set Stable at 0;
roll/store the normal d4-hour Stable recovery deadline immediately;
preserve last_death_turn;
do not open a would-die replacement because the natural 20 did not produce death.

Conceptually:

Plain text
nat20 + cannotRegainHP
→ Living
→ HP 0
→ Stable
→ deathSuccesses 0
→ deathFailures 0
→ normal d4-hour Stable deadline

This should replace the existing test at lines 932–933 with the reviewed Stable-zero behavior.

That is a material blocker to bounded review because it directly contradicts an already-reviewed interface.

2. Passive Reserve regeneration and excess — accept the exclusion

I agree with the recommendation in the candidate guide. The current arithmetic can calculate genuineExcess even when passive Mutation Recovery Reserve regeneration restores 0 HP and spends 0 Reserve. 
Pasted text

Do not allow that excess to power Cosmic Equilibrium.

Add this source eligibility rule:

NEW: Unpaid passive regeneration whose healing is bounded by Mutation Recovery Reserve is ineligible to supply excess-healing conversions unless a future source expressly says otherwise.

This covers:

Bloodthick Node;
Rapid Coagulation;
Regenerative Mutation;
Bio-Stabilizer only as its modifier of Bloodthick.

So at full HP or under the Critical ceiling:

the helper may still compute a mathematical genuineExcess;
Cosmic Equilibrium receives sourceEligible = false;
no radiant damage conversion occurs;
Reserve remains unspent.

This is important because these sources are intentionally finite through the Reserve even though their activation itself is automatic. Their exact classifications are already passive Reserve-limited regeneration. 
Pasted text

I would keep this exclusion specific to the passive Reserve-regeneration family, not automatically extend it to every finite heal that happens to restore 0 HP. Cosmic Equilibrium is expressly designed to make some genuine overhealing useful.

Add at least:

full HP + Bloodthick + Reserve remaining → no Cosmic conversion;
Critical max−1 + Regenerative Mutation → no Cosmic conversion;
ordinary paid heal at full HP → may still produce eligible excess if its source/converter rules allow it.
3. Spiral III + fatal Wound + independent Ward — confirm current behavior

Yes: the phase-out survives if an independently legal would-die Ward prevents the fatal Wound death.

The submitted guide already expresses the correct distinction: fatal Wound death ends phase only on actual death; a successful Ward prevents actual death. 
Pasted text

The test is also correct:

Spiral III triggers;
quarter-HP recovery/phase occurs;
Wound save is fatal;
Ritual Ward replaces that death;
creature remains alive;
Spiral use remains spent;
phase-out remains active until its original source-next-start endpoint. 
Pasted text

The Ward does not restart, extend or refund the phase. It merely prevents the death that otherwise would have terminated it.

So retain:

spiralUsed = true
phaseOut = true
wardUsed = true
actualDeath = false

Six dormant spells: individual review

All six remain appropriately inactive. I do not see a semantic contradiction requiring redrafting before the next implementation iteration.

Stitch Fate — draft acceptable

The two-mode interpretation is coherent:

living/dying/0 only;
not Stable or Dead;
remove one recorded failure or direct 1-HP recovery;
broad HP prohibition converts Stitch Life to Stable0 with a real recovery deadline;
no retrospective interruption of completed death.

That fits the source's otherwise ambiguous “change one failed death save or auto-revive a dying target” without turning an Action into time travel. 
Pasted text

Individual draft disposition: ACCEPTABLE FOR IMPLEMENTATION/VALIDATION, still inactive.

Ordinary Death Ward — draft acceptable

Correctly distinct from Ritual of Undeath:

positive→0 prevention only;
1 HP floor;
concentration up to one minute;
no Instant Death;
no fatal Wound death;
no third death-save failure;
no lethal-track death;
no already-zero recovery.

Its raw-damage/Wound behavior is consistent with the closed damage procedure. 
Pasted text

Individual draft disposition: ACCEPTABLE FOR IMPLEMENTATION/VALIDATION, still inactive.

Resurrection — draft acceptable

The provisional 8-hour window is clearly labeled NEW, while source rank/action/range/RP structure is preserved. The life transition correctly:

requires actual death;
requires willingness;
requires viable in-range remains;
returns at 1 HP;
preserves Wounds/resources/persistent consequences;
routes retained lethal tracks into the collapse reconciliation.

Pasted text

Individual draft disposition: ACCEPTABLE AS THE PROVISIONAL PLAYTEST OBJECT, still inactive.

Mass Resurrection Denial — draft acceptable

The source's Instantaneous metadata was operationally incompatible with an ongoing resurrection block. The proposed:

fixed 20-foot sphere;
concentration up to one minute;
corpse-local anchor denial;
moving remains out as counterplay;
no automatic Soul Bind/bodyless denial

is coherent and properly labeled NEW. 
Pasted text

Individual draft disposition: ACCEPTABLE AS THE PROVISIONAL GAP-FILL, still inactive.

True Resurrection — draft acceptable

The object correctly avoids inventing unsupported soul lore:

one unambiguously identified actually Dead creature;
willing;
≤7 days as clearly NEW;
usable remains or legal perceived formation space;
no true-name requirement;
no guessed afterlife location;
one authoritative living identity;
other remains cannot create a second instance.

Pasted text

The associated identity ledger appropriately invalidates duplicate resurrection anchors after success. 
Pasted text

Individual draft disposition: ACCEPTABLE FOR IMPLEMENTATION/VALIDATION, still inactive.

Soul Bind — draft acceptable

The pending/bound split is coherent:

living dying0 target only;
CHA save;
no concentration;
60-second pending tether;
Stable/positive HP ends it;
death strictly before expiry converts;
24-hour identity block;
one family record;
failed recast refreshes rather than stacks;
caster death does not end it;
local remains only provide a removal anchor, not ownership of the soul.

Pasted text

The helper correctly treats exact expiry as winning ties and rejects post-death recasting. 
Pasted text

Individual draft disposition: ACCEPTABLE FOR IMPLEMENTATION/VALIDATION, still inactive.

Before promotion, the promotion validator should still assert the preserved catalog metadata—class access, rank, minimum level and RP cost—because these draft objects deliberately store only their operational layer rather than duplicating that authority.

Other reviewed implementation pieces

I do not find a new defect in these submitted pieces:

positive damage event vs numeric actualDamageDealt;
Ward frozen damage metrics;
no Wound replay after intercepted Instant Death;
Spiral III pre-Wound exception;
Mage/Oracle zero-HP permissions;
two-pass conditional healing;
next-heal entitlement consumption;
Blight Totem branch arbitration;
Channel Life's packet-wide no-temp-HP conversion;
shared-root secondary-heal provenance;
Grace Reversal owner/target history;
Thousand Petals six-total/two-corpse cap;
resurrection identity ledger;
Soul Bind state transition;
suppressed-present Bleed/fire cure semantics;
protected Exhaustion6/Expedition6 collapse reconciliation;
participant-only Time Loop snapshot helper with the wider temporal system explicitly deferred. 
Pasted text

The reported Core parity test is particularly useful: the new survival helper is being compared against the 120 unchanged Core damage states when none of the new exceptions is enabled. 
Pasted text

Disposition

Do not mark the bounded healing/death package REVIEWED yet.

Two implementation changes are required:

Fix blocked natural-20 death-save recovery to the already-reviewed Stable0 + cleared counters + d4 deadline behavior, eliminating the contradiction between the two helpers.
Encode/test passive Mutation-Reserve regeneration cannot feed excess-healing conversion, even when arithmetic reports excess with 0 actual HP and 0 Reserve spent.

The six ordinary spell drafts themselves pass this individual design review but should remain INACTIVE / pending operational validation and promotion.

Once those two changes are returned with targeted tests, this exact 153-source healing/death interface package should be ready for bounded closure review. DD24, the remaining 131 matches, Time Loop's world/topology layer, broader disease/curse/body/soul rules, and full-game completion remain open.