# Healing and death first source review

Captured from the visible completed Calibration Review response. This is a proposal, not closure.

This packet supports a coherent life-state model, but it needs a strict separation between damage floors, HP recovery, death replacement, resurrection, and reconstruction. The closed Core damage/Wound/death procedure should remain authoritative; the rules below only fill the interfaces the supplied sources leave open. 
Pasted text

1. Common life-state procedure

Use these distinct mechanical operations:

Operation	Meaning
Damage floor / minimum-HP prevention	The damage packet resolves normally, but the resulting normal HP cannot cross the printed floor. No HP is “regained.”
Ordinary HP healing	A living creature increases current HP through a healing/regain-HP effect. Subject to healing modifiers and HP-recovery prohibitions.
Direct state recovery	A non-healing rule changes dying/Stable state or sets/restores a specific HP value, e.g. natural-20 death recovery or Stitch Fate. Still subject to a broad “cannot regain HP” rule unless expressly excepted.
Would-die replacement	A pending transition to Dead is replaced before Dead becomes final. Ritual of Undeath's Death Ward is this category.
Resurrection	Target is already Dead. Effect transitions it back to Living and assigns returned HP. This is not ordinary healing.
Companion reconstruction	Recreates a destroyed companion/device under that subsystem. It is not creature resurrection merely because the card says resurrection.
Temporary HP	Separate pool. Never healing and never resurrection.
Damage event order

For one damage packet:

Snapshot pre-event normal HP, temporary HP, effective maximum HP, Wounds, Stable/dying state, death counters, concentration, active floor/replacement uses and applicable defenses.
Resolve damage normally through resistance/reduction and temporary HP. Preserve the existing post-temp damage value.
Calculate the Core Instant Death result and the raw Wound trigger from that unchanged post-temp amount.
Resolve an eligible minimum-HP floor. The floor changes only the HP result; it does not reduce the damage packet.
Resolve the Core Wound save. A fatal failed Wound save at three existing Wounds creates a death event despite a 1-HP floor.
If a death outcome now exists, open the would-die replacement window.
If the creature survived and is at 0, resolve eligible post-zero recovery effects such as Phoenix Rebirth or Unyielding Light.
Establish the surviving creature's final dying/Stable/positive-HP state and death counters.
Resolve later damage/healing triggers whose source timing is after the packet.

For simultaneous beneficial floor/replacement effects, the affected creature chooses one eligible effect to resolve first. An allied Reaction must actually be offered and paid. Once one effect changes the triggering outcome, recheck the remaining effects; those whose trigger is no longer true do not spend their use.

Automatic per-rest survival uses are consumed only when they actually alter the result. Paid Reactions spend their Reaction/resource when legally declared.

2. HP floors do not reduce the damage packet

This is the key rule for Redundant Organs, Last King's Gift, Miracle Veil, Thousand Petals, Echo Armor, Song of Mending, Eternal Bloom, Undying Ember and similar sources.

NEW: A minimum-HP floor preserves the damage packet and changes only the amount of normal HP lost.

Therefore:

postTempDamage used for Instant Death and Wound thresholds stays unchanged.
Attached damage conditions still resolve.
Concentration uses its ordinary damage procedure; the floor does not reduce the triggering damage quantity.
The floor is not HP gain, so Decay or another “cannot regain HP” effect does not stop it.
A creature already at 0 cannot use a “would be reduced to 0” floor; there is no downward crossing left to prevent.
Temporary HP granted after the packet, such as Last King's Gift, remains legal because temporary HP is not HP recovery.

Define separately:

normalHpLost = preEventNormalHP - finalNormalHPAfterFloor

This is the quantity used when a source explicitly derives healing or reflection from actual damage dealt. It prevents a life-drain effect from harvesting 80 points of “damage” from someone whose floor allowed only 9 normal HP to be lost.

Generic “when this creature takes damage” still sees the positive damage event even if the floor limited HP loss.

Instant Death

A generic 1-HP floor does not override Core Instant Death unless the source explicitly says it can.

The supplied cards generally reinforce this:

Redundant Organs: only if not killed outright.
Echo Armor: only if not killed outright.
Undying Ember: only if not killed outright.
Verdant Pulse: only if no instant death.
Song/Eternal Bloom: only without instant death.
Thousand Petals expressly says instant-death effects still function. 
Pasted text

Miracle Veil likewise does not gain an unwritten massive-damage exception merely because it specifically mentions HP-bypassing instant-death effects. 
Pasted text

Example

Maximum HP 40, current HP 20, no temp HP, 25 post-temp damage, Song floor active:

raw damage remains 25;
floor leaves creature at 1 instead of 0;
2 × 25 >= 40, so Wound save still occurs;
if it already had three Wounds and fails, that failed Wound save creates a death event;
the floor itself does not stop that death.

A genuine would-die replacement could then intervene.

3. Ritual of Undeath Death Ward is a broader death replacement

The Cleric class Death Ward is not the same mechanic as the dormant ordinary spell Death Ward.

Ritual of Undeath says the marked creature's first would-die event is replaced. 
Pasted text

Bind:

cleric.ritual-of-undeath.death-ward

as a one-use death-replacement record, not a zero-HP floor.

It can replace an otherwise valid death caused by:

Core damage Instant Death, provided the body remains capable of sustaining life;
a fatal failed Wound save;
third death-save failure;
another non-body-destroying death event;
an event-based lethal track endpoint, subject to the reconciliation below.

It cannot:

resurrect an already Dead creature;
reconstruct a destroyed/missing vital body;
override a source explicitly saying its death cannot be prevented;
repair the underlying Wounds/condition/track that produced the death.
With Decay or another broad HP-gain prohibition

Normally the replacement sets the creature to 1 HP.

If the replacement prevents death but an active effect prohibits all HP increase:

NEW bridge: consume the Death Ward, prevent the death, clear death successes/failures, and leave the creature Living, Stable at 0 HP.

Record an ordinary Stable recovery deadline only if the recovery system would normally create one; Decay can keep that eventual 1 HP recovery due-but-blocked under the already-reviewed procedure.

The Ward's temporary humanoid+undead rider still applies because the death replacement succeeded.

This is not indefinite protection: the Ward is consumed.

4. Zero-HP consciousness

Zero HP does not stop death-save progression merely because a feature permits consciousness.

Mage — Undying Spellform

While active at 0:

remains conscious;
may take its normal Action;
may voluntarily move at no more than half Speed;
NEW conservative boundary: the source does not restore a Bonus Action or Reaction otherwise lost through the ordinary zero-HP state.
regular-start death saves continue normally;
further damage has all normal zero-HP consequences;
death immediately ends the feature.

If a natural 20 or other recovery raises HP above 0, the feature ends early as printed. 
Pasted text

At expiry, if still 0:

become Unconscious;
suffer one additional death-save failure.

If the creature had become Stable at 0 before expiry, the explicit expiry consequence destabilizes it: cancel the Stable recovery deadline, end Stable and record one death failure.

If that failure reaches three, it dies.

Oracle — False Life Boon III

Different permission set:

During its special turn at 0 choose exactly one:

move up to Speed;
speak normally;
activate one Revelation, paying its normal cost.

It gets no second option from an extra Action/Bonus Action feature and this does not create a second turn.

Regular-start death saves still occur.

If HP becomes positive before the special zero-HP permission is needed, ordinary positive-HP action economy resumes; the card does not continue restricting a creature that is no longer relying on its zero-HP exception. 
Pasted text

5. Resurrection is a life-state transition, not healing

A successful resurrection:

requires an actually Dead creature;
identifies one creature/soul identity;
requires that identity to be willing;
checks any source-specific body and death-time window;
checks corpse/soul/resurrection blockers;
changes Dead → Living;
assigns the source's returned HP;
clears death-save counters because the creature is no longer dying;
preserves Wounds, Corruption, debt, Oracle Curse and other death consequences unless the source explicitly removes them;
restores no spent class resources unless expressly stated.

The returned HP is not ordinary HP healing. Therefore it is not:

halved by Healing Suppression;
reduced by Doomed or Blight healing reducers;
halved by Corrupted;
blocked merely by “cannot regain HP.”

A rule must specifically prohibit resurrection/raising to stop it.

Decay therefore has two distinct interfaces:

cannot regain HP affects living HP recovery;
corpses within 2 tiles ... cannot be raised is the resurrection blocker.

Do not merge them. 
Pasted text

A successful resurrection either returns the creature at the source's valid returned HP or fails. Generic HP-gain prohibition does not turn a resurrection into Living/Stable-at-zero.

Willing soul and planar/body requirements

NEW generic bridge:

A player controls whether their character's identity/soul willingly returns.
Resurrection cannot compel belief, allegiance or return.
If willingness cannot be determined before casting, refusal at resolution causes no resurrection and does not refund an already cast spell/paid feature.
Corpse-based resurrection requires the target corpse/remains to be in range and have line of effect unless the source says touch or otherwise.
A source that requires a body fails if the remaining body is incapable of sustaining life.
Bodyless True Resurrection is the explicit exception.
Generic resurrection provides no cross-planar reach. A planar/soul barrier that actually blocks the target must be overcome by a source that says it can.
6. Lethal tracks after death prevention/resurrection

These need playable exceptions without erasing the tracks.

Expedition Strain 6

Reaching/exceeding 6 still ordinarily kills under the reviewed Strain overlay.

If an actual death replacement or resurrection prevents/reverses that death while the creature still has 6 Expedition Strain:

NEW: keep all six points and place the creature in the already-defined nonlethal expedition.collapse state.

It remains alive but collapsed until Haven care/explicit treatment legally lowers the track below 6.

This does not silently turn future positive Strain gains safe: another unprevented gain at 6 still resolves its lethal endpoint normally. 
Pasted text

Exhaustion 6

Because Exhaustion 6 is a continuing lethal level rather than an event-only endpoint:

NEW post-resurrection exception: actual resurrection can return the creature alive, but while Exhaustion remains 6 it enters exhaustion.resurrection-collapse: Unconscious, no voluntary action/travel and unable to benefit from the resurrection for adventuring purposes.

The first legal effect/rest that reduces Exhaustion to 5 ends this collapse.

This does not remove the level automatically and does not make ordinary reaching Exhaustion 6 nonlethal.

Three Wounds

Three Wounds is not a continuous death source. A resurrected character can remain at three Wounds and is Critically Wounded; the next failed Wound save remains fatal.

7. Short resurrection windows

For wording such as:

“died since the end of your previous regular turn”

record the caster/source's preserved regular-end marker.

Eligibility means:

death occurred strictly after previous source regular-end marker and no later than the current cast/trigger

Initiative changes do not rewrite that marker.

Outside initiative, use the same virtual six-second source clock, so this phrase means effectively “during the current six-second source interval.”

Specific class resurrection bindings
Cleric Resurrection: actual resurrection; corpse touched; died within 1 minute; body sufficient; returns at 1 HP + printed temp HP. 
Pasted text
Celestial Resurgence: actual resurrection; up to six allied corpses within 30 ft; body sufficient; death within previous 3 rounds = no more than 18 elapsed seconds. Returns at 1 HP. 
Pasted text
Divine Rebirth: modifies one successful Cleric resurrection. Returned normal HP becomes max(1, floor(effectiveMaximumHP/2)); then grant printed temp HP. This is returned resurrection HP, not healing, so Critical's healing ceiling does not reduce it. Wounds remain. 
Pasted text
Breath of the Thousand Petals: living/downed targets receive ordinary healing; up to two actually Dead allied creatures satisfying the source-window/body rules receive actual resurrection to 1 HP. Its damage floor then protects affected living creatures until source-next-start. 
Pasted text
Grace Reversal: actual resurrection. Its Reaction window occurs immediately after the Paladin survives the triggering reduction to 0 and before ordinary zero-HP Reaction denial finalizes, because otherwise the printed Reaction could never function. The Paladin remains 0/dying. 
Pasted text
Soulbound Ritual: companion reconstruction only. No willing soul/body/death-save procedure. The destroyed bound companion or its token is the required anchor. 
Pasted text
Thousand Petals repeat restriction

“Cannot revive the same creature twice” should not be reduced to the meaningless rule “do not target one corpse twice in one cast.”

NEW binding: source-character/creature persistent history.

Once a particular Monk has returned a creature from death using Breath of the Thousand Petals, that Monk cannot use Thousand Petals to resurrect that same creature again in the campaign.

It does not prevent:

another Monk's Thousand Petals;
another resurrection feature;
healing the creature while living.
8. Healing arithmetic

For one ordinary HP-healing event:

Stage A — construct positive potential
Roll or establish printed base healing.
Apply legal source modifiers/additional healing dice.
Apply recipient/event additive healing bonuses that modify this event.
Floor nonnegative.

Examples include Crane Stance, Aura of Mercy, Bloom Ward and Thorned Shelter when their actual trigger requirements are met. 
Pasted text
 
Pasted text

This value is the positive-potential healing used by the already-reviewed magical-healing Bleed cure interface.

Stage B — qualifying multipliers

Apply independent multiplicative healing modifiers as exact rational factors, then floor once after that multiplicative stage.

Examples:

Wound Eater qualifying healing ×1/2;
Healing Suppression ×1/2;
Withering Shot's next healing ×1/2;
Corrupted's reviewed healing ×1/2.

Same source/group does not duplicate.

If a source expressly says it is nonstacking with another healing reduction, such as Blight Totem, treat it as an exclusive reduction profile rather than multiplying it with another ordinary healing-reduction profile. Evaluate the legal competing result and use the more restrictive result; do not combine the prohibited pair.

Stage C — flat reductions

Apply independent legal flat healing reductions once each, unless their own source says nonstacking.

Examples:

Cleric Doomed -S-M;
Dirge of Ruin Aura -S-M;
Blight Infusion -M.

Floor at zero.

Repeated applications of the same source never multiply the flat reduction unless explicitly stated.

Stage D — broad prohibition

A source saying:

“cannot regain HP”

sets actual ordinary HP recovery to 0 after the potential-healing event has been established.

That includes:

paid healing;
pulses;
life drain;
Hit Dice/rest recovery;
passive regeneration;
direct positive-HP recovery,

unless the source specifically exempts a category.

It does not block:

temporary HP;
stabilization at 0;
minimum-HP floors;
actual resurrection returned HP.
Stage E — recipient caps

Cap at:

effective maximum HP;
Critical Wound's healing ceiling when applicable.

The Critical ceiling is a healing ceiling, not maximum-HP reduction.

Stage F — actual HP gained

actualHpGained = finalHP - preHealingHP

Only this value:

resets death counters through regaining positive HP;
spends Mutation Recovery Reserve;
satisfies a rider requiring the target to actually restore/regain HP.

Mutation Recovery Reserve therefore spends one point for each HP actually restored, never for rolled/potential healing lost to reductions, caps or prohibition. 
Pasted text

Overflowing Light

Its excess-to-temp-HP conversion is based on healing exceeding maximum HP, not healing prevented solely by Critical Wound's max-minus-one ceiling. It cannot transform prohibited/negated healing into temp HP. 
Pasted text

9. “Passive regeneration” is narrow

Scorch the Sanctified and Lifeleech Bloom Aura block passive regeneration, not all HP recovery. 
Pasted text

For this pass:

Passive regeneration includes

automatic/passive periodic HP restoration requiring no paid activation at that pulse, such as Regenerative Mutation.

It does not include

an Action/Bonus Action healing spell;
paid maintenance pulses;
Hit Dice;
Long Rest;
life drain based on damage;
resurrection;
direct Stable/death-save recovery.

Thus those Paladin auras block Regenerative Mutation but not Healing Rite, Marrow Drain, Circle of Harmony, or a Long Rest merely because all represent bodily recovery.

10. Living zero-HP recoveries

These are not resurrection:

Unyielding Light;
Phoenix Rebirth;
Grace Eternal's 2d8 follow-up;
Stitch Fate's proposed dying recovery;
natural-20 death save.

They apply only while the creature remains Living.

They are HP recovery and can therefore be blocked by Decay.

Example: Phoenix Rebirth is legally triggered after a surviving ally reaches 0. Under Decay its half-max HP regain becomes 0. The Reaction/RP remain spent if the Paladin chose to use it. The printed fire shield may still apply because it is a separate component; the target remains at 0 and dying. 
Pasted text

Redundant Organs is different: it never lets HP reach 0 and therefore works despite Decay. 
Pasted text

11. Resurrection blockers
Dirge of Ruin Aura

When a currently selected living creature dies, preserve the selected identity record through death.

The resurrection prohibition remains while:

the remains/identity remains inside the aura;
the Paladin remains conscious;
the aura remains active;
the selection has not been explicitly replaced.

The target becoming a corpse does not automatically delete its selection.

An existing selected corpse may continue to occupy that selected slot. A corpse cannot be newly selected by using wording that requires a selected living creature.

Moving the remains outside the aura ends this aura's denial. Bringing the remains back does not recreate the old selection automatically.

Ending the aura/selection cannot retroactively undo a resurrection that already completed. 
Pasted text

Other blockers

Keep separate:

oracle.decay: qualifying nearby corpses cannot be raised.
paladin.dirge-of-ruin-aura: selected identity/corpse inside aura.
proposed ordinary.mass-resurrection-denial: area corpse block.
proposed ordinary.soul-bind: soul-specific resurrection block.

A generic “cannot regain HP” effect is not a resurrection blocker.

12. Six dormant ordinary-spell candidates

These remain blocked/inactive until individually implemented and validated.

Stitch Fate

Source preserved: Divination rank 8; Cleric 15/Wizard 15; 21 RP; Action; 120 ft; V/S/F; Instantaneous. 
Pasted text

NEW operational candidate

Target one living dying creature at 0 HP you can perceive within 120 ft with line of effect. It cannot target Dead or Stable creatures.

Choose one:

Unravel Failure: remove one recorded failed death save.
Stitch Life: clear all death successes/failures and regain 1 HP.

If an active broad HP-gain prohibition blocks that 1 HP, Stitch Life instead makes the target Stable at 0, clears its death counters and establishes normal Stable recovery.

It is not resurrection and cannot affect completed death.

Death Ward

Source preserved: Necromancy rank 4; 7 RP; Action; 60 ft; V/S/M/F; Concentration up to 1 minute; listed class access/minimum levels unchanged. 
Pasted text

NEW operational candidate

Target one living creature you can perceive within 60 ft.

The first time during the duration an effect would reduce that creature from positive HP to 0 without Core Instant Death or another outright death result, it remains at 1 HP instead. Then the spell ends.

Damage packet/Wound calculations remain intact.
Not healing.
Works through HP-gain prohibition.
Does not trigger while target is already 0.
Does not prevent third death-save failure, fatal Wound death, Exhaustion6 or another would-die event.

This intentionally remains narrower than Cleric Ritual of Undeath's class Death Ward.

Resurrection

Source preserved: Necromancy rank 7; Cleric/Druid/Wizard 13, Shaman 19; 17 RP; Action; 120 ft; V/S/F; Instantaneous. 
Pasted text

NEW operational candidate

Target one willing Dead creature whose sufficiently intact corpse/remains is within 120 ft and line of effect and whose death occurred within the previous one Rest Watch / 8 elapsed hours.

Return it to life at 1 HP.

It:

requires a body capable of sustaining life;
restores no class resources;
removes no Wounds, Corruption, debt or Oracle Curse;
cannot overcome an active resurrection/soul blocker;
is not ordinary HP healing.

The 8-hour window is an explicit playtest choice, not recovered source wording.

Mass Resurrection Denial

Source preserved: Necromancy rank 8; Cleric/Druid/Wizard 15; 21 RP; Action; 120 ft; V/S/M/F. The source's Instantaneous metadata conflicts with its ongoing effect. 
Pasted text

NEW operational candidate

Choose a point within 120 ft. Create a 20-foot-radius fixed zone, Concentration up to 1 minute.

While active, a corpse/remains inside that zone cannot be used as the target/anchor of an effect that returns that corpse to life.

Moving the remains outside the zone ends this spell's block for that corpse.

This does not by itself prevent a bodyless resurrection such as True Resurrection when no corpse/remains is being used as the resurrection target.

Counterplay:

break caster concentration;
move remains out;
use an effect explicitly capable of ending/dispelling an ongoing rank-8 spell.

No retrospective reversal of a completed resurrection.

True Resurrection

Source preserved: Necromancy rank 9; Cleric/Druid/Wizard 17; 26 RP; Action; 120 ft; V/S/F; explicitly works without remains. 
Pasted text

NEW operational candidate

Target one willing Dead creature identity known to the caster whose death occurred within the previous 7 elapsed days.

If sufficient remains are present in range, they may be restored. If not, a viable body forms in one legal unoccupied space the caster can perceive within 120 ft.

Return target at 1 HP.

Preserve:

Wounds;
Corruption;
debts;
Oracle Curse;
spent resources and other persistent consequences.

It cannot overcome an active Soul Bind or other blocker explicitly applying to that creature's soul/identity.

The 7-day limit is a provisional game-design limit, not imported source text.

Soul Bind

Source preserved: Necromancy rank 9; Cleric/Druid/Wizard 17; 26 RP; Action; 120 ft; V/S/F; source target is a dying creature and purpose is preventing resurrection. 
Pasted text

NEW operational candidate

Target one living dying creature at 0 HP within 120 ft that you can perceive and affect.

Target makes a Charisma save.

Success: no effect.

Failure: create a soul tether for up to 1 minute while the target remains dying.

If it regains positive HP or becomes Stable, tether ends.
If it dies while tethered, convert tether into soul-bound for 24 hours.
While soul-bound, that creature cannot willingly return through resurrection.
This creates no control of its corpse, memories, personality or afterlife beyond the resurrection block.
An effect expressly capable of ending a soul binding or an eligible dispel of this rank can remove the record.
The bound player's identity/soul remains theirs; the spell grants the caster no commands, information or ownership.

No permanent player-character removal is created by an indefinite unstated duration.

13. Curing suppressed Bleed/fire records

Correct the earlier active-predicate mismatch.

For cure/removal, use:

present && cureEligible

not:

active && unsuppressed

A temporarily suppressed condition is still present and can be cured.

Therefore:

Medicine may select one present ordinary eligible Bleed record even while immunity suppresses it.
A positive-potential magical heal ends all present eligible ordinary Bleeds with autoEnd, regardless of current suppression.
Blood Curse remains its exception: each present eligible Blood Curse record gets its actual printed CON save rather than automatic removal.
Generic fire Action/full immersion ends all present ordinary-extinguishable attached-fire records, including suppressed ones.
Per-record DEX removal saves may be made for present eligible fire records that still have future periodic damage scheduled, even if currently suppressed.
Special-cure/protected records remain protected.
Successfully cured records are deleted/ended and therefore cannot resume when immunity/suppression later disappears.
Damage-family arbitration still excludes suppressed records.

This brings periodic cures into line with the already-reviewed Sanctify Ground rule without changing Bleed's one-record Medicine scope.

14. Classification of every supplied class source
Source	Disposition
cleric.engine[7]	BOOK/guard: healing/resurrection limits
cleric.base.healing-rite	HEAL ordinary
cleric.hero.saint.divine-rebirth	RESURRECTION MODIFIER
cleric.hero.saint.unyielding-light	LIVING-ZERO HP RECOVERY
cleric.hero.saint.celestial-resurgence	RESURRECTION
cleric.hero.saint.mass-healing-light	HEAL
cleric.hero.saint.resurrection	RESURRECTION
cleric.hero.cultist.blasphemous-tongue	HEALING REDUCTION / ALREADY Doomed
cleric.hero.cultist.rite-of-the-crimson-choir	COMPANION + LIFE-DRAIN HEALING, not resurrection
cleric.hero.cultist.blood-sacrifice	DIRECT HP LOSS WITH 1-HP COST FLOOR
cleric.hero.cultist.ritual-of-undeath	COMPANION REANIMATION + WOULD-DIE REPLACEMENT
dragoon.hero.dragon-guardian.bastion-descent	TEMP HP / damage protection, not healing
mage.hero.archmage.harmonized-core	TEMP HP, explicitly not healing
mage.hero.lich.undying-spellform	CONSCIOUS-AT-ZERO STATE
mage.hero.lich.soul-reservoir	RESOURCE trigger, no healing
mage.hero.lich.resonance-to-flesh	HEAL / DIRECT HP COST depending mode
mage.hero.lich.soulbound-ritual	COMPANION RECONSTRUCTION
mirrorsage.engine[5]	BOOK anti-copy/resource guard
mirrorsage.hero.light-weaver.radiant-archive	SUPPORT COPY, explicitly no resurrection
mirrorsage.hero.light-weaver.divine-reflection	COPY/BOOK hook, excludes resurrection
monk.engine[16]	BOOK healing/death guard
monk.base.crane-stance-support	HEAL modifier + paid healing
monk.hero.enlightened-master.breath-of-the-thousand-petals	HEAL + RESURRECTION + DAMAGE FLOOR
monk.hero.enlightened-master.healing-touch	HEAL
monk.hero.enlightened-master.circle-of-harmony	PAID HEALING PULSES
monk.hero.enlightened-master.shared-breath	DAMAGE REDIRECT + HEALING ECHO
monk.hero.way-of-shadow.veinlock-nerve-jab	HP/FINITE-RESOURCE RECOVERY PROHIBITION
oracle.engine[3]	BOOK: Oracle Curse persists through resurrection
oracle.engine[13]	BOOK: healing/resurrection guard
oracle.supplement.shared.oracle-s-burden	BOOK/protected class state
oracle.supplement.curse.wound-eater	HEALING MULTIPLIER / rest condition
oracle.supplement.false-life.false-life-boon-i	DAMAGE FLOOR + DEATH-SAVE DEATH REPLACEMENT
oracle.supplement.false-life.false-life-boon-ii	FEIGN-DEATH STATE, not death/revival
oracle.supplement.false-life.false-life-boon-iii	CONSCIOUS-AT-ZERO STATE
oracle.supplement.ancestor.echo-armor	DAMAGE REDUCTION + 1-HP FLOOR
oracle.supplement.ancestor.echo-crowned	ALLY 1-HP FLOOR / RC option
oracle.supplement.battle.battle-prophecy-trigger	RESOURCE trigger at hostile 0 HP
oracle.supplement.battle.avatar-of-the-war-chorus	ALLY 1-HP FLOOR / resource banners
oracle.supplement.bones.bones-prophecy-trigger	RESOURCE trigger on actual death
oracle.supplement.bones.marrow-drain	LIFE-DRAIN HEAL + HP-RECOVERY BLOCK
oracle.supplement.bones.rotting-touch	ALREADY Decay / broad HP prohibition + corpse block
oracle.supplement.flame.undying-ember	SELF 1-HP FLOOR + ordinary ally healing
oracle.supplement.life.bloom-ward	HEAL modifier + damage absorb
oracle.supplement.life.overflowing-light	HEAL + excess-to-temp-HP conversion
oracle.supplement.life.thorned-shelter	HEAL modifier
oracle.supplement.life.verdant-pulse	post-heal rider + ally 1-HP floor
oracle.supplement.life.song-of-mending	HEAL pulses + per-ally 1-HP floor
oracle.supplement.life.eternal-bloom	pre-recorded HEAL reserve + per-ally 1-HP floor
paladin.base.protective-stance	DAMAGE REDIRECTION, not healing
paladin.base.sacred-touch	STABILIZATION, explicitly not healing
paladin.supplement.oathbreaker-shared.last-reproach	ordinary ally HEAL after damage
paladin.supplement.oath-of-mercy.aura-of-mercy	HEAL modifier
paladin.supplement.oath-of-mercy.miracle-veil	persistent 1-HP DAMAGE FLOOR
paladin.supplement.oath-of-mercy.blessing-of-the-meek	HEAL
paladin.supplement.oath-of-mercy.grace-reversal	RESURRECTION Reaction
paladin.supplement.oath-of-mercy.grace-eternal	Miracle floor + post-floor HEAL
paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression	HEALING ×1/2
paladin.supplement.oath-of-vengeance.final-verdict	broad cannot-regain-HP rider
paladin.supplement.oath-of-flame.phoenix-rebirth	LIVING-ZERO HP HEAL, not resurrection
paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified	PASSIVE-REGENERATION BLOCK
paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura	PASSIVE-REGENERATION BLOCK
paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom	DAMAGE + LIFE-DRAIN HEAL + source-local target floor
paladin.supplement.oath-of-grief.echo-of-the-fallen	SPIRIT MANIFESTATION, explicitly not resurrection
paladin.supplement.oath-of-grief.dirge-of-passage	HP-recovery prohibition on selected undead + death-save bonus
paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura	RESURRECTION BLOCK + flat HEALING reduction
paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin	broad cannot-regain-HP rider
paladin.supplement.oath-of-the-martyr-king.last-king-s-gift	1-HP FLOOR + TEMP HP
paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura	conditional HP-healing gate only
ranger.hero.outrider.blight-infusion	next-healing flat reduction
ranger.hero.outrider.withering-shot	next-healing ×1/2
shaman.hero.bloodcaller.blight-totem	nonstacking HEALING ×1/2 aura
soldier.arch.fortify-zone	NON-HEAL false-positive source
soldier.hero.champion.rallying-cry	TEMP HP, not healing
tinker.base.field-repair	MACHINE REPAIR, no destroyed-object resurrection
tinker.hero.artificer.repair-pulse	MACHINE REPAIR, functional devices only
warrior.hero.wardborn.stabilizing-injection	HEAL
warrior.hero.ironskin.regenerative-mutation	PASSIVE REGENERATION / reserve-paid actual healing
warrior.supplement.redundant-organs	1-HP DAMAGE FLOOR
warrior.supplement.hemophage-core	LIFE-DRAIN HEAL / reserve-paid actual healing

These classifications follow the operative source distinctions rather than titles such as “revive,” “rebirth,” “undying,” or “resurrection.” 
Pasted text
 
Pasted text
 
Pasted text
 
Pasted text

15. Adversarial cases to implement
HP 8/max30 takes 38 post-temp with Redundant Organs → Core Instant Death; Redundant unused.
HP 20/max40 takes25 with Song floor → HP1 but Wound save still occurs from raw25.
Same creature starts at three Wounds and fails that Wound save → death despite floor; Ritual Death Ward may replace.
HP5 under Decay + Redundant Organs takes8 non-instant-death damage → remains1; Decay cannot block because no HP was regained.
HP0 under Decay + Phoenix Rebirth → reaction can occur, HP gain blocked; target remains0/dying.
Class Death Ward at 0 intercepts third death-save failure under Decay → Ward consumed; Living Stable0, counters cleared.
Mage Undying Spellform at0 rolls natural1 at regular start → two failures; if still alive it may use its permitted Action.
Mage is externally stabilized during Spellform, remains0 until expiry → expiry ends Stable and assigns one death failure.
Resurrection on corpse with Healing Suppression only → succeeds normally because resurrection is not healing.
Resurrection on corpse blocked by Dirge Aura or Soul Bind → fails; HP-reduction effects are irrelevant.
Resurrection of Expedition-Strain-6 corpse → target returns at source HP but enters expedition collapse with all six points retained.
Resurrection of Exhaustion-6 corpse → target returns but enters post-resurrection exhaustion collapse until a legal effect reduces Exhaustion below6.
Divine Rebirth on effective max101 → return at50 HP, not51; minimum1.
Thousand Petals Monk attempts to revive the same previously Thousand-Petals-revived ally on a later day → source-history rejects.
Suppressed ordinary Bleed under temporary immunity receives Medicine → Medicine may choose and permanently remove it; immunity ending cannot restore it.
Suppressed ordinary attached fire is immersed → all ordinary-extinguishable present records end permanently.
Regenerative Mutation under Scorch the Sanctified → blocked; Healing Rite under the same aura → not blocked by the passive-regeneration rule.
Wound Eater + Corrupted + Healing Suppression on a qualifying external heal → apply the legal multiplicative stages, floor once, then caps; never convert lost healing into damage.
Mutation Recovery Reserve heal rolls8 but only3 HP can actually be restored → spend3 reserve, not8.
Miracle/Last-Gift floor prevents an ordinary drop to0 but does not reduce the raw damage available to Core Wound/Instant-Death calculations.
Remaining dependencies

This is still a proposal/source-conference pass, not closure. The major remaining dependencies are the actual disease/curse catalogs, broader resurrection-counterspell/dispel spell set, precise soul/planar cosmology, object/body destruction rules, all remaining healing sources outside these 79 class procedures, and implementation/reference tests for the six ordinary spell drafts.

No original source needs modification yet, and the six ordinary spells should remain blocked-pending-operational-review until Codex returns their exact candidate objects and adversarial validation. 