# GPT exact control candidate findings

Captured from the visible rendered Calibration Review reply.

There are four concrete issues I would fix before marking this bounded control package REVIEWED/reference-VALIDATED. The overall architecture is sound, but these are real interface/semantic defects rather than editorial preferences. The candidate itself correctly limits its claim to the supplied 219 records and selected interfaces. 
Pasted text

Material 1 — Guiding Star helper has the wrong API timing

The guide correctly says the +2 applies to the attack roll and is consumed on that roll. But GuidingStarMark.ally_attack() requires the caller to pass hit before it returns attackBonus. That makes the reference API temporally backwards: the caller needs the +2 before it can determine whether the attack hits. 
Pasted text

The comment acknowledges this, but that does not make the interface operational.

I recommend splitting it into two phases:

Plain text
begin_ally_attack(...)
    -> validates eligibility
    -> consumes the attack-bonus entitlement
    -> returns attackBonus = 0 or 2
    -> returns/records one attack token

resolve_ally_attack(token, hit)
    -> if that same qualifying attack hit and hit rider remains:
         return radiantBonus = S
         consume hit rider and end mark

Important cases:

first attack misses → +2 consumed, hit rider remains;
later ally attack begins → +0;
if later attack hits → +S and mark ends;
duplicate resolution of the same token rejected;
suppressed/illegal attack does not consume anything.

Because there is no live engine calling it yet, this is easy to correct now.

Material 2 — current-turn expiry cannot be represented by the scalar expires

The prose says an effect applied during end-turn resolution can apply and then expire at that same turn end. current_turn_endpoint(3, actual_turn_end=3) correctly returns 3. 
Pasted text

But SpeedRecord.operative() is:

Python
now < expires

So a record created at time 3 with expires=3 is immediately non-operative at time 3. 
Pasted text

That directly contradicts the intended current-turn bridge for:

Resonant Seed;
Winter's Embrace;
Frost Totem;
Glue.

The existing validation proves only that the endpoint number is 3, not that the effect can actually exist during that end-turn resolution.

Exact fix

The scheduler needs an ordered marker, not just a wall-clock integer.

For example:

Plain text
(time, phaseOrder)

with something equivalent to:

Plain text
application at:
(3, END_EFFECT_APPLICATION)

expiry at:
(3, END_EFFECT_EXPIRY)

where application precedes expiry.

A simpler implementation can use a marker object such as:

Plain text
expiresAtTime = 3
expiresAfterCurrentTurnResolution = true

but there must be some ordering dimension. Adding an epsilon to seconds would be brittle.

Also add a test that actually creates a current-turn slow at the endpoint and verifies:

it is operative for its resolution event;
it expires before events belonging to the next slot/round phase.

This is the biggest timing bug in the current helper.

Material 3 — several actual Speed components are missing eligibility.slowed-foe

The guide says explicit adverse Speed reductions/Speed0 carry the hook while suppressed records do not. 
Pasted text

The metadata index misses several printed soft fallbacks that actually contain Speed control. 
Pasted text

Add eligibility.slowed-foe to:

oracle.bone-whisper.soft-fallback — Reaction loss + Speed0.
oracle.ledger-command.soft-fallback — Reaction loss + Speed0.
oracle.marquis-glimpse.soft-fallback — Reaction loss + Speed0.
oracle.slumber-glimpse.soft-fallback — Reaction loss + Speed0.
oracle.moments-pause.soft-fallback — Reaction loss + Speed0.
paladin.decree-of-submission.soft-fallback — Reaction loss + half Speed.
paladin.echo-of-ages.soft-fallback — Reaction loss + half Speed.

This matters mechanically because Snow Leopard and future legitimate eligibility.slowed-foe readers would otherwise fail against those states.

Spiral Opens needs a split, not a blanket tag

Do not simply tag oracle.spiral-opens.forced-echo.

Its player branch contains a choice between:

repeating a non-resource action type; or
Speed0.

Its NPC branch is a different forced-pattern control.

Create a distinct component such as:

oracle.spiral-opens.player-speed-zero

and give that:

eligibility.slowed-foe

only when the player actually chooses the Speed0 branch.

Otherwise the current single component cannot accurately represent slowed eligibility.

Add binding-validator assertions for these memberships.

Material 4 — Stars Revelation Mastery is classified incorrectly

Current binding:

oracle.supplement.stars.stars-revelation-mastery → STATE

with:

oracle.guiding-bolt.enhanced-slow

But the card is a permanent passive mastery selection. It does not itself apply a slow. The Enhanced Guiding Bolt option modifies a later Guiding Bolt hit. The earlier conference correctly classified this as a HOOK. 
Pasted text

Change it to:

HOOK, with oracle.guiding-bolt.enhanced-slow as the reviewed downstream component it can authorize when that mastery option was actually selected and Guiding Bolt later hits.

This is important because STATE semantically suggests the passive card is itself a state-producing application.

Specific review points you asked about
Mage Fusion endpoint — accept the NEW bridge

Yes. For mage.hero.elementalist.elemental-fusion:

Fire+Cold -10 Speed → target next regular end.
Cold+Lightning -10 Speed → target next regular end.
Cold+Lightning opportunity-attack denial → target next regular end.
Fire+Lightning Reaction denial → target next regular start.

The first Speed endpoint is genuinely missing from the operative phrase, so the target-next-end choice is a NEW bounded gap-fill. The sibling Cold+Lightning wording is the best internal evidence for it. The guide's current choice is appropriate. 
Pasted text

I would add an explicit operationalOverrides entry to the Fusion binding because this is an authored missing-endpoint decision rather than something recoverable solely from the source.

Cascade does not require another rule decision. Its unqualified next turn wording is already deterministically handled by the closed source-clock convention:

cold → source next regular end;
lightning → source next regular start.

Adding an explicit override there would improve auditability but is not mechanically necessary.

Ray of Frost / Frost Arrow — explicitly classify these two

I approve a narrow NEW semantic classification:

ordinary.ray-of-frost.slow
ordinary.frost-arrow.slow

gain:

classification.elemental-control

for Balanced Elements.

These are audited ordinary cold spells whose operative effect directly couples cold damage to an explicit Speed reduction. This decision applies only to these reviewed records.

It does not establish:

“all cold spells are elemental control.”

Future spells still require source review.

Both already correctly carry eligibility.slowed-foe. 
Pasted text

Carrion Conductor corpse history — cross-owner scope confirmed

Yes.

The operative source says:

“Corpse cannot be reused”

rather than “cannot be reused by you.”

Therefore:

crimson-agent.carrion-conductor.used-corpse:<corpseIdentity>

should be source-family/corpse scoped, not owner-character scoped.

Once any Carrion Conductor use claims that corpse, another Crimson Agent cannot later use that same corpse for Carrion Conductor.

It remains limited to Carrion Conductor reuse. It does not prohibit:

resurrection;
harvesting;
another corpse spell;
another class feature;

unless those systems independently say so.

The candidate currently captures this correctly. 
Pasted text

Additional binding-coverage cleanup

These are not separate mechanical blockers, but they should be corrected while touching the bindings.

shaman.base.flask-use is classified BOOK but links only shaman.flask.burn, even though the source expressly invokes Burn, Root or Weaken profiles. Since your guide says component IDs are references and alternative IDs do not imply simultaneous application, either:

link all three:
shaman.flask.burn
shaman.flask.root
shaman.flask.weaken

or link none on the BOOK wrapper and leave all profile application entirely to engine[4].

The current Burn-only linkage is asymmetrical and misleading.

Likewise, mage.arch.elemental-mastery currently links its Fire components but not the Cold control components it expressly modifies. For semantic coverage, I would avoid overloading componentIds and add a dedicated field such as:

modifiesComponents

for HOOK bindings. Then Arch Elemental Mastery can explicitly reference:

mage.fire-focus.burn
mage.inferno-lance.burn
mage.cold-focus.flat
mage.cold-focus.glacier

without implying it applies those states itself.

The same structure would cleanly represent:

Enhanced Elemental Attunement → Ice-affinity slow;
Stars Revelation Mastery → Enhanced Guiding Bolt slow;
Balanced Elements → eligible elemental applications.
Things that pass this review

I found the following interfaces sound as implemented:

strongest hostile-soft Speed arbitration;
independent magnitude/deadline profiles;
Iron Leash minimum formula;
Hypermutation per-mode snapshot/floor precedence;
suppression/expiry behavior;
Root vs Restrained/Grappled separation;
physical-restraint fallback gate;
disease immunity scope helper;
curse-removal/detection boundaries;
Divine Judgment actual-turn reflection;
Wrathful Brand rider consumption;
hit-vs-attack one-shot semantics;
Balanced Elements nonrecursive deadline extension;
Reign of Ashes willing-teleport restriction;
Sanctify Ground removing all present classified Staggered records including suppressed ones;
Moment's Pause stable next-round initiative permutation. 
Pasted text

The 9,393 Speed invariant states are meaningful evidence for the arithmetic helper, but—as the guide correctly says—they do not validate all source dispatch. 
Pasted text

Disposition

Do not mark the bounded control package REVIEWED yet.

Fix:

Guiding Star's pre-roll/post-roll helper split.
Phase-aware current-turn expiry.
Missing slowed-foe memberships + Spiral Opens Speed0 subcomponent.
Stars Revelation Mastery STATE → HOOK.

Also add the two specific ordinary cold-spell elemental tags and the Fusion endpoint override.

After those changes pass targeted tests and binding validation, I would be comfortable reviewing the bounded supplied control-state interface package covering:

the 219 supplied source records;
source-qualified Speed/control arbitration;
supplied marks and rider consumption;
supplied restraint/control clocks;
Staggered classification/removal;
selected curse/disease interfaces;
selected initiative-control and Hypermutation interfaces.

That would still leave DD16/DD18, disease/curse catalogs, death/replacement/resurrection, unsupplied object/tether durability, full card execution, and the all-source semantic remainder open.