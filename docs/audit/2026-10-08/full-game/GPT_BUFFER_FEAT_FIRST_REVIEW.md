# GPT eight-feat first full-clause proposals

Eight-feat source conference

All eight source objects are preserved. The existing form/buffer review already fixes several subinterfaces: Empowered Summoning's 2PB creation shield, Field Medic's post-stabilization PB shield, Blood Ritual's 2×level / level offers, and Necrotic Affinity's resistance/Reaction/post-packet shield pipeline. 
Pasted text

The following completes the remaining clauses as candidate design, not feat promotion.

1. Chef

Source guarantees only that the character can cook special food during a long rest and that it provides temporary HP to the party. 
Pasted text

I propose these NEW operational bounds:

During a long rest, spend at least 1 hour performing light cooking activity with cook's utensils and ordinary edible ingredients.
Prepare up to PB servings.
Each serving consumes one ordinary ration/meal-equivalent ingredient.
A creature spends 1 uninterrupted minute eating one serving.
A serving grants 2 × the Chef's PB temporary HP.
The temp HP use the normal default lifetime: depleted/replaced/recipient's next completed long rest.
A creature can gain the special Chef benefit once per completed long-rest epoch, regardless of how many Chefs feed it.
Prepared feat potency lasts 24 hours or until that Chef completes another long rest, whichever happens first.
Making a new batch ends the special feat potency of that Chef's earlier batch. The underlying food remains mundane food.
Food may be sold or traded only at its ordinary mundane food value; the expiring feat benefit does not create persistent magical inventory value.
No combat Action shortcut to the 1-minute eating time.

This permits portable meals without infinite stockpiling.

2. Inspiring Leader

Preserve the 10-minute speech and Charisma 13 prerequisite. 
Pasted text

NEW operational draft:

Spend 10 uninterrupted minutes speaking.
Select up to PB other willing creatures.
Each must remain within 30 ft, able to hear you and understand at least one language you use for the full speech.
Self is not a recipient; the source says companions.
On completion each receives temp HP equal to:

character level + actual CHA modifier, minimum 1.

Default temp-HP lifetime applies.
One recipient may benefit from Inspiring Leader once per completed long rest across all speakers.
Incapacitation, Silence preventing speech/hearing, or the speaker abandoning the performance interrupts it and grants nothing.
A recipient leaving range/hearing before completion simply receives nothing; it does not necessarily invalidate the speech for everyone else.

This creates a shared source-family refresh limit so serial speeches cannot refresh shields.

3. Empowered Summoning

Source: Charisma 14+, 2PB temp HP to summoned creatures, and PB added to the first damage roll each round. 
Pasted text

Retain the previously reviewed creation buffer and add:

Qualifying summon

A qualifying creature must be a new finite creature instance actually created/summoned into play by a spell or feature whose source owner is the feat holder.

Not qualifying merely by returning/reappearing:

Ranger bonded Beast;
Mage bound elite return;
persistent companion rebuild;
existing creature placed under control;
revived creature;
Tinker device;
retracted/deployed existing asset.

A genuinely new summon from a new legal paid source activation qualifies.

Creation shield

At actual creation:

2 × current total-character PB

Snapshot that amount once. It does not increase later when PB changes.

Normal default temp-HP lifetime applies, but entity ending also removes the shield.

Damage rider

For each qualifying summoned creature:

once per numbered round;
add the original summoner's current PB to that creature's first actual damage roll.

The summoned creature remains the attacker/damage owner. Empowered Summoning is a flat feat rider, not caster spell damage.

For shared/area damage:

add PB once to the shared roll;
do not add it once per target.

For separate attack rolls:

only the first damage roll of that summoned creature in the round receives PB.

An automatic fixed-damage event with no damage roll receives no bonus.

Persistent ticks can qualify only when they contain an actual damage roll and the creature has not already used its round rider.

Recreation guard

Track a summonCreationRoot.

Dismiss/redeploy/reconfigure/recreate under the same still-existing source root does not regenerate the feat's creation shield or round state. A genuinely new paid summon root does.

Existing shared companion command/offensive budgets remain unchanged.

4. Field Medic

Source has two grammatically separate clauses:

healer's kit may be used as a Bonus Action;
“When you stabilize a creature,” it gains PB temp HP. 
Pasted text

I read the second sentence broadly and source-faithfully:

the PB shield applies whenever this feat owner actually causes a creature to become Stable, not only when the Bonus Action kit method was used.

So it can apply to:

Field Medic Bonus Action healer's kit;
an ordinary Medicine stabilization by that owner;
a stabilization spell such as Spare the Dying cast by that owner.

It does not trigger from merely assisting someone else.

Kit mode
Bonus Action;
one living dying creature eligible for the canonical healer's kit procedure;
consume one actual kit use;
stabilize normally;
then grant PB temp HP.
Shield trigger

Requires a real state transition:

dying -> Stable

An already Stable target cannot be “stabilized” again.

NEW anti-replay rule: one Field Medic shield per dying episode. A new dying episode requires the creature actually to become dying again after the earlier stabilization. Replaying the same stabilization event cannot create another grant.

No healing, consciousness, Wound removal or resurrection is supplied.

Default temp-HP lifetime applies.

5. Blood Ritual

Preserve Constitution 13+, level 4+, 10 minutes, 1/LR, self 2×level, allies level, and ally 1-hour lifetime. 
Pasted text

NEW completion:

Activation: 10-minute ritual.
Use commits at ritual start after valid preflight.
Leader must remain conscious/capable and continue the ritual.
Choose up to PB willing allies at the start.
Each ally must remain within 10 ft, be able to witness the ritual, and voluntarily contribute a drop of blood for the full ritual.
No HP is lost by anyone; source prints no blood-damage/payment.
Leader receives 2 × character level temp HP with default lifetime.
Each still-eligible ally receives character level temp HP for exactly 1 hour.
Ally offers are calculated from the feat amount itself, never from whatever shield actually wins arbitration.
An ally leaving before completion simply receives no benefit.
If the leader's ritual is actually interrupted, the use remains spent and no one receives the unfinished benefits.
Save rider

Only the feat owner receives the source's advantage rider.

After successful ritual completion:

Advantage on the next saving throw actually made against an effect explicitly classified as a curse or disease, until the owner's next completed long rest.

It is consumed when that qualifying save is rolled, regardless of success.

It does not cleanse an existing curse/disease and does not remove an Oracle intrinsic Curse.

“Required for many lycanthropic oaths” establishes only a possible prerequisite relationship. Blood Ritual itself grants no oath, lycanthropy or transformation.

6. Necrotic Affinity

Preserve prerequisite:

Religion proficiency OR level 8+. 
Pasted text

The resistance/Reaction/post-packet shield remains exactly the reviewed interface. 
Pasted text

Melee-hit rider

Source says once per turn, not once on your turn.

Therefore:

once per distinct actual turn identity;
when you hit with a melee attack;
optional;
add 1d6 necrotic.

This includes a legal off-turn melee Reaction attack.

It does not refresh because of:

Extra Attack;
an extra Action during the same turn;
multiple hits in the same turn.

A genuine separate extra turn is a distinct turn and may qualify once if the general extra-turn system permits the underlying attack.

“melee attack” is broader than “melee weapon attack,” so a legally qualifying natural/form melee attack may use it. Weapon-only taxonomy is irrelevant to this clause.

Provenance:

attacker = feat owner;
source = feat:necrotic_affinity;
damage type = necrotic;
this added die is not spell damage, even when attached to a melee spell attack.

Ordinary critical rules apply to the added attack damage die.

24-hour anti-resurrection seal

When a body actually dies in a damage root where:

this owner is the attacker/source owner;
Necrotic Affinity contributed positive necrotic normal-HP damage to that fatal root;

attach to the immutable body identity:

NecroticAffinitySeal(owner, expiry = death + 24h)

It blocks resurrection effects explicitly carrying Resonance Rank 0–5.

NEW rank translation: printed “5th level or lower” is mapped to this game's Resonance Rank 5 or lower.

An unranked class/feat resurrection ability is not automatically treated as rank ≤5. It is blocked only if its exact source or future integration assigns an effective rank/level within that range.

Rank 6+ resurrection is not blocked by this feat.

The seal follows the actual body through temporary transformations and does not manufacture a corpse, soul, XP or resource entitlement.

Copies/downstream damage that no longer has this owner's Necrotic Affinity source provenance do not create the seal.

7. Lifeleech and the shared Soul Charge pool

Lifeleech source has two distinct clauses: spell-damage healing and soul sparks. 
Pasted text

Necrotic spell healing

Prerequisite remains Spellcasting ability.

Trigger when your spell causes qualifying necrotic damage to an eligible hostile target.

Use the reviewed numeric quantity:

actual necrotic damage dealt

not rolled/raw damage.

AoE/pulse bound — NEW

For each:

spellRootId + numberedRound

Lifeleech may heal at most once.

When an eligible spell event can damage multiple targets, designate one qualifying hostile target for Lifeleech before that event resolves.

Healing amount:

floor(actual necrotic damage dealt to that designated target / 2)

This prevents one area roll from multiplying healing by target count.

Separate targets, secondary arcs and repeated hits from the same spell root in that round do not produce additional Lifeleech healing.

A later numbered-round pulse from a persistent spell may qualify again.

Eligibility — NEW anti-farm integration

The designated damage target must be:

genuinely hostile;
not created/summoned by the feat owner or allies for farming;
not friendly/staged;
not an obviously trivial sacrificial target.
Healing procedure

Lifeleech heals the feat owner.

It is ordinary HP healing:

maximum HP applies;
Critical healing ceiling applies;
healing prohibitions/reductions apply;
it removes no Wounds;
it does not resurrect.

Genuine excess is calculated normally. Lifeleech itself provides no excess conversion. Another converter may use remaining excess only if its own exact interface permits it and global causal-root guards permit the chain. 
Pasted text

Shared Soul Charge pool

Lifeleech and Soul Cage use one owner-level resource:

SoulCharges: 0..3

Never two separate pools.

A qualifying death can give that owner at most one charge, even if they own both feats.

NEW anti-farm death eligibility:

actual hostile creature;
actual soul-bearing creature;
not a summon/created creature;
not a friendly/staged/trivial sacrifice;
same body may yield this owner at most one charge per completed long-rest epoch, preventing revive/kill loops.

Object-origin transformed creatures never qualify because the transformation package establishes that they have no soul.

8. Soul Cage capture, prerequisite, and world consequence

Source prerequisite:

Lifeleech or spellcasting ability, level 8+ 
Pasted text

Operational grammar:

Level 8+ AND (Lifeleech OR a spellcasting ability).

Lifeleech itself requires spellcasting ability, but preserve the printed branch.

What a charge is

This needs an explicit world ruling.

NEW decision: a Soul Charge is a soul spark/residue, not custody of the creature's complete soul.

Reason: Lifeleech explicitly calls the resource a “soul spark,” and both feats must share one charge pool. Treating the same resource as an entire imprisoned soul would silently make Lifeleech block resurrection, which its source does not say.

Therefore:

gaining a charge does not prevent resurrection;
it does not block Soul Bind or similar soul-custody magic;
the deceased soul remains available according to ordinary soul/resurrection rules.

Soul Cage's flavor text remains preserved; the operational resource is bounded residue.

Black crystal

Soul Cage requires one dedicated black crystal object in the owner's possession to:

capture via Soul Cage;
spend Soul Cage abilities.

No price or HP cost is invented.

The engine resource remains owner-level so Lifeleech and Soul Cage cannot create duplicate pools.

The crystal is a conduit, not the legal owner of the soul.

If the crystal is lost:

charges remain in the owner pool;
Soul Cage capture/spending is unavailable until the owner possesses a legal replacement black crystal.

If destroyed, same result; no trapped souls are released because whole souls were never imprisoned.

Capture

When an eligible hostile soul-bearing creature actually dies within 30 ft:

Lifeleech can generate its automatic shared-pool entitlement;
Soul Cage without Lifeleech may choose to capture the same owner entitlement if a black crystal is present.

NEW perception gate: owner must perceive the creature/death and ordinary total obstruction cannot completely isolate the death from the Soul Cage effect.

No Action or Reaction is consumed; it is an immediate death-checkpoint choice.

If pool already has 3 charges, no latent fourth charge or stored entitlement remains.

Multiple feat owners

Because the resource is residue rather than whole-soul custody, each eligible feat owner may gain their own one charge from the same genuine death.

The no-double rule is per owner:

Lifeleech + Soul Cage never gives the same owner two charges from one death.

Charge lifetime

No source duration exists, so no decay is invented.

Charges persist until:

spent;
voluntarily dissipated;
or an exact future source removes them.

The owner may dissipate any number voluntarily during 1 minute of quiet handling of the black crystal; this has no effect on the deceased soul.

9. Soul Cage shield and Agony Lance
One-charge shield

NEW operational details:

Activation: Bonus Action.
Cost: 1 Soul Charge, committed before arbitration.
Range: 30 ft.
Target: one legal ally.
Effect: 2d8 temporary HP.
Lifetime: ordinary V6 default.
Concentration: no.
Failure/refund: no refund after legal commitment merely because an existing equal/stronger shield wins.

This is temp HP only, not healing.

Agony Lance

NEW operational details:

Activation: Action.
Cost: 2 Soul Charges.
Range: 60 ft.
Target: one creature you can perceive.
Save: Constitution.
DC: ordinary feat owner's spell save DC.
If multiple spellcasting abilities exist, choose one when Soul Cage is acquired; that choice remains until an explicit retraining rule.
Damage: 3d8 necrotic, half on successful save.
Charges commit before save; no refund for success/resistance/immunity.

The damage belongs to the Soul Cage feat owner and source feat:soul_cage; it is not a spell cast.

“Disadvantage on the next healing”

There is no generic healing roll, so this requires an explicit conversion.

NEW operational conversion:

Agony Lance applies AgonyHealingSuppression until consumed or 1 minute passes.

The next incoming HP-healing event with positive pre-reduction healing potential receives an exact ×1/2 healing multiplier, rounded under the existing healing-reduction pipeline, then the suppression is consumed.

This is not because “disadvantage mathematically equals half”; it is the selected operational translation.

It applies equally to:

rolled HP healing;
fixed HP healing.

It does not affect:

temporary HP;
damage prevention;
stabilization;
resurrection;
max-HP changes.

Under the existing healing interface, if a positive healing event is later capped or blocked, the applicable next-heal reducer still consumes when that event commits. 
Pasted text

The healing suppression applies regardless of whether the Agony Lance save succeeded; the save changes only damage. Necrotic damage immunity does not by itself erase this separate rider unless an exact immunity says it negates the whole effect.

10. Complete candidate feat objects

All eight should remain candidate-design / implementation pending.

chef
Plain text
id: chef
type: General
prerequisite: None
acquisition: feat selection
repeatability: nonrepeatable
activation: during a long rest; 1 hour cooking
requirements:
  cook's utensils
  1 ordinary ration/meal-equivalent ingredient per serving
servings: PB
servingConsumption: 1 uninterrupted minute
target: creature consuming one prepared serving
effect:
  gain 2*PB temporary HP
duration:
  food potency: 24 hours or until Chef completes another long rest, whichever first
  tempHP: normal default lifetime
frequency:
  one special Chef benefit per recipient per completed long-rest epoch across all Chefs
interruption:
  incomplete cooking creates no special servings
economy:
  expired/unused food remains ordinary food
  no persistent magical/premium value is created
status: candidate
NEW:
  all quantities/times except the printed long-rest cooking role
inspiring_leader
Plain text
id: inspiring_leader
type: General
prerequisite: Charisma 13+
acquisition: feat selection
repeatability: nonrepeatable
activation: 10 uninterrupted minutes speaking
target:
  up to PB other willing creatures within 30 ft
  each must hear and understand you throughout
selfEligible: false
effect:
  each gains max(1, character level + actual CHA modifier) temporary HP
duration:
  tempHP uses normal default lifetime
frequency:
  each recipient may benefit from the Inspiring Leader source family once per completed long rest
interruption:
  speaker incapacitation/speech failure/abandonment ends performance with no effect
  individual recipient leaving range/hearing loses only that recipient's benefit
status: candidate
NEW:
  target count, range/language gate, amount, source-family refresh limit
empowered_summoning
Plain text
id: empowered_summoning
type: Magic
prerequisite: Charisma 14+
acquisition: feat selection
repeatability: nonrepeatable

qualifyingSummon:
  genuinely new finite creature created/summoned by a source activation owned by you
excluded:
  returned/revived/bound preexisting bodies
  persistent companion redeploy/rebuild
  devices

onCreation:
  offer 2*PB temporary HP
  amount snapshots PB at creation
  default lifetime plus entity-ending dependency

damageRider:
  each qualifying summoned creature
  first actual damage roll each numbered round
  add source owner's current PB once
  shared/AoE roll receives PB once total, not once per target
  fixed damage with no roll receives no bonus

provenance:
  summoned creature remains attacker/damage owner
  feat is not caster spell damage

recreationGuard:
  same summonCreationRoot cannot refresh creation shield by dismissal/recreation/reconfiguration
  genuinely new legal summon root may qualify

command:
  existing shared companion BA/offensive budget unchanged
status: candidate
field_medic
Plain text
id: field_medic
type: General
prerequisite: Trained in Medicine
acquisition: feat selection
repeatability: nonrepeatable

healersKitMode:
  activation: Bonus Action
  target: one living dying creature
  cost: one actual healer's-kit use
  effect: perform canonical automatic kit stabilization

stabilizationRider:
  trigger: this feat owner actually causes dying -> Stable by any legal method
  effect: target gains PB temporary HP
  lifetime: default

episodeGuard:
  one Field Medic grant per actual dyingEpisodeId
  already Stable target cannot be restabilized for another grant
  a genuinely new later dying episode can qualify again

limitations:
  no real HP
  no consciousness restoration
  no Wound removal
  no resurrection
status: candidate
NEW:
  broad reading of second sentence confirmed; dying-episode anti-replay identity
blood_ritual
Plain text
id: blood_ritual
type: Magic
prerequisite: Constitution 13+, character level 4+
acquisition: feat selection
repeatability: nonrepeatable
activation: 10-minute ritual
frequency: 1/long rest
useCommit: ritual start

targets:
  self
  up to PB willing allies chosen at start

allyRequirements:
  remain within 10 ft for full ritual
  witness ritual
  voluntarily share one drop of blood

cost:
  no HP loss

effect:
  self: offer 2*character level temporary HP
  each eligible ally: offer character level temporary HP

duration:
  self tempHP: default
  ally tempHP: 1 hour

selfSaveRider:
  advantage on next save against an actual curse or disease effect
  expires at next completed long rest
  consumed on qualifying save roll

interruption:
  leader interruption spends use and grants no unfinished benefit
  ally leaving only removes that ally's eligibility

limitations:
  grants no lycanthropic oath/transformation
status: candidate
NEW:
  PB ally cap, 10-ft presence rule, use timing, save-rider deadline
necrotic_affinity
Plain text
id: necrotic_affinity
type: Magic
prerequisite: Religion proficiency OR character level 8+
acquisition: feat selection
repeatability: nonrepeatable

passive:
  resistance to necrotic damage

meleeRider:
  trigger: hit with a melee attack
  frequency: once per actual turn identity
  optional: yes
  damage: +1d6 necrotic
  natural/form melee attacks may qualify
  extra Actions in same turn do not refresh
  genuine distinct extra turn may qualify once
  provenance: feat damage, not spell damage

reactionAbsorption:
  use previously REVIEWED Necrotic Affinity pipeline unchanged

antiResurrection:
  trigger:
    target actually dies in a fatal damage root
    this owner's Necrotic Affinity necrotic component contributed positive normal-HP damage
  bodyEffect:
    cannot be raised by explicit Resonance Rank 0-5 effects for 24 hours
  unranked resurrection:
    unaffected unless exact source later supplies effective rank <=5
  identity:
    follows immutable body through temporary forms

limitations:
  no corpse/soul/resource entitlement is generated
status: candidate
NEW:
  actual-turn ledger
  rank-5 translation
  fatal-root/body-identity procedure
lifeleech
Plain text
id: lifeleech
type: Magic
prerequisite: Spellcasting ability
acquisition: feat selection
repeatability: nonrepeatable

necroticHealing:
  trigger: your spell causes qualifying necrotic damage
  targetOfHealing: self
  eventCap: once per spellRootId per numbered round
  multiTarget:
    designate one qualifying hostile target before damage resolution
  amount:
    floor(actual necrotic damage dealt to designated target / 2)
  healing:
    ordinary HP healing pipeline
    maxHP/Critical/prohibitions/reductions apply
    removes no Wounds
    does not resurrect
  excess:
    feat supplies no intrinsic conversion
    outside converter requires its own legality

damageEligibility:
  genuine hostile
  not owner/ally-created or summoned farming target
  not friendly/staged/trivial sacrifice

soulResource:
  shared owner SoulCharges pool
  cap: 3

soulSpark:
  trigger: eligible hostile soul-bearing creature dies within 30 ft
  amount: +1 charge
  same owner gains at most one charge from that death across Lifeleech/Soul Cage
  same body yields that owner at most once per completed long-rest epoch

status: candidate
NEW:
  pulse/AoE bound
  anti-farm eligibility
  shared death-entitlement ledger
soul_cage
Plain text
id: soul_cage
type: Magic
prerequisite:
  character level 8+
  AND (Lifeleech OR spellcasting ability)
acquisition: feat selection
repeatability: nonrepeatable

resource:
  uses the same owner SoulCharges pool as Lifeleech
  cap: 3
  charge is soul residue/spark, not custody of whole soul
  no automatic charge decay

blackCrystal:
  one dedicated black crystal must be in owner's possession to use Soul Cage capture/abilities
  no invented HP or monetary cost
  loss of crystal prevents Soul Cage use but does not erase owner SoulCharges

capture:
  trigger: eligible hostile soul-bearing creature actually dies within 30 ft
  perception: owner must perceive the creature/death; total obstruction may block
  action: none; immediate death-checkpoint choice
  result: +1 Soul Charge if below cap
  same owner cannot also gain a second charge from Lifeleech for same death
  multiple owners may each gain their own residue entitlement
  does not prevent resurrection or Soul Bind

release:
  owner may voluntarily dissipate charges during 1 minute of quiet handling
  no effect on actual deceased soul

shield:
  activation: Bonus Action
  cost: 1 Soul Charge
  target: one legal ally within 30 ft
  effect: 2d8 temporary HP
  lifetime: default
  payment not refunded if stronger/equal shield wins

agonyLance:
  activation: Action
  cost: 2 Soul Charges
  range: 60 ft
  target: one perceived creature
  save: CON
  DC: chosen feat spellcasting ability's normal spell save DC
  damage: 3d8 necrotic, half on success
  charges spent before save

agonyHealingSuppression:
  duration: until consumed or 1 minute
  applies to next positive-potential HP-healing event
  effect: exact x1/2 healing multiplier in canonical healing-reduction pipeline
  consumed by first applicable committed heal
  does not affect tempHP, stabilization, resurrection, prevention, maxHP changes

status: candidate
NEW:
  prerequisite grammar
  residue interpretation
  crystal operational role
  capture/perception procedure
  all ability activations/ranges/DC
  healing-disadvantage conversion
Required follow-up source dependencies

Before these eight feats become implementation candidates, several external source domains should be read rather than guessed: the general feat acquisition/retraining rules; cook's utensils/rations/economy definitions; the ally/self glossary; curse/disease tagging; healer's-kit and Medicine procedures; the exact resurrection spell/ability registry for the Rank-5 seal; spellcasting-ability selection when a character has several; and the creature/soul taxonomy used to decide whether a death can produce a soul spark.

The feat conference disposition is therefore:

SOURCE-DISCUSSED / COMPLETE CANDIDATE DRAFTS — eight exact feat identities, with prior reviewed interfaces preserved and missing clauses operationally proposed. Implementation and independent validation pending; no feat promoted.
