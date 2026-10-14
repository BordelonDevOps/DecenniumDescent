# GPT five-spell boundary decisions

ChatGPT said:

All 12 can be settled without changing the five spell identities, the 12 finite spell-form profiles, True Polymorph's meaningful permanence, or Mass Polymorph's ten-target scope. These are integration decisions for implementation, not catalog promotion. 
Pasted text

1. Schema and Harmonic Bulwark payment

Confirmed.

For True Polymorph use:

concentration: true
concentrationAfterStabilization: false

The changing concentration state belongs in the duration/effect procedure, not in a non-Boolean schema value.

For Harmonic Bulwark, the chosen willing recipient receives the temp-HP offer. “Gain” does not force self-targeting.

Payment is:

creditedRP = actualBaseRPpaid + X

where:

normal base = 5 RP;
exact legal base-cost discounts may reduce actualBaseRPpaid;
X is chosen 0..PB before commitment;
X is an additional payment and cannot be discounted;
Dissonance-related actual cast pricing remains whatever canonical quote_cast says;
Refrain affects post-cast Dissonance under the existing spell rules and is not a newly invented immediate RP surcharge;
surcharge RP, whatever its canonical source, never counts toward the 5 × creditedRP shield calculation.

NEW transaction timing: preflight target/access and choose X, obtain canonical quote, then commit Action + quoted casting payment + X. If the spell is subsequently countered/cancelled by a legal post-commit counter mechanism, all committed RP including X stays spent and no buffer offer is created.

A failure occurring before commitment spends neither base cost nor X. 
Pasted text

2. Concentration replacement order

Accept the proposed reconciliation.

For a caster beginning any new concentration spell:

fully preflight the prospective cast;
commit Action/resources;
immediately end that caster's currently maintained concentration;
resolve countering, saves and new effect application;
if the new spell fails/countered/saved, the old concentration does not return.

Therefore, if the caster currently maintains Mass Polymorph, beginning another concentration spell ends all Mass Polymorph links before the new saves resolve.

An anatomy maintained by another caster/source's still-active effect is different. It remains until the new transformation actually succeeds and replaces it.

A stabilized True Polymorph is no longer concentration. Starting another concentration spell does nothing to it. It remains until an allowed transformation actually succeeds, it is dispelled/suppressed, or another exact ending applies.

This supersedes my earlier overly broad “old anatomy ends only after new success” statement for same-caster concentration replacement. 
Pasted text

3. Druid Shapeshift versus spell anatomy

A Druid cannot enter Shapeshift while a spell-transformation anatomy is active.

That includes:

Polymorph;
a Mass Polymorph target link;
Shapechange;
True Polymorph during its shaping minute;
stabilized True Polymorph.

This is a NEW interoperability bridge, not an invented rank comparison.

A willing temporary spell transformation must first end through its legal procedure: target rejection Action if available, caster concentration ending, successful repeat save, dispel, etc. An unwilling Polymorph cannot simply be escaped by spending a Druid shift.

True Polymorph during shaping counts as active rank-9 spell anatomy.

Same-profile paid recasts are legal as new spell records. They still pay normal costs and undergo all saves/concentration procedures. “Must choose a different profile” applies only to Shapechange's internal Bonus Action switch, not to separate new casts.

There is always one active anatomy. No displaced Druid form, spell form or True form waits underneath. Global transformation/form instance IDs use the same world identity registry. 
Pasted text

4. Attack/damage provenance

Confirm this exact provenance model:

attacker/event owner: transformed subject;
stat provider: original caster of the transformation;
source record: the active transformation spell + spell-form profile;
attack identity: natural/form attack;
spellcast identity: false.

Therefore a Polymorphed creature's claw is not “the caster casting a spell,” and its damage is not automatically direct caster spell damage.

It does not trigger caster features requiring wording such as:

“your spell deals damage”;
“when a creature dies from your Necromancy spell”;
per-cast damage/healing riders;
spell-hit resource generation;

unless an exact future rule explicitly recognizes transformation-granted attacks.

Subject features expressly triggered by:

natural attacks;
form attacks;
melee attacks generally;

may apply if their own predicates are satisfied. Weapon-only interoperability remains unresolved.

Stat timing:

Polymorph/Mass/Shapechange supplied attacks use the current original caster spell attack and current M at attack resolution.
True Polymorph captures caster spell attack, spell DC, PB and M when cast; permanent forms use that snapshot.
Polymorph/Mass initial and repeat saves use current caster spell DC.
True Polymorph initial and shaping-period repeat saves use its captured casting-time DC.

The subject remains the causal attacker for target-side reactions, concentration damage checks, kills, etc. 
Pasted text

5. True Polymorph during shaping and creature→object
Creature-origin True Polymorph during the shaping minute

Before stabilization it is a temporary concentration-linked transformation.

For creature→creature:

actual 0 HP after same-packet prevention;
actual death;
actual Incapacitated

ends that target's shaping link.

Caster Incapacitated separately ends the caster's concentration and therefore every still-shaping target link.

Creature→object

The object anatomy does not apply the Core Incapacitated condition merely because it has no Actions.

Use a distinct state:

actionlessObjectAnatomy = true

It supplies:

Speed 0;
no Actions;
no Bonus Actions;
no Reactions;
no speech;
no ordinary senses;
no object manipulation.

It does not, by itself:

set the Incapacitated condition;
end existing concentration;
end True Polymorph's shaping concentration if the caster transformed themself.

Thus a caster can legally maintain a self-targeted creature→object True Polymorph for the full shaping minute.

A willing creature→object target cannot use the proposed rejection Action while it is actionless. Its consent was supplied before transformation. During shaping it can end only through caster concentration ending, dispel/suppression, actual external Incapacitation/death/destruction, or another applicable rule.

After stabilization, no voluntary rejection exists anyway. 
Pasted text

6. Object-origin creature durability and object anatomy

Accept the suggested object-origin creature baseline with these precise boundaries.

Object → creature

Retain exactly one structural currentHP/maxHP ledger.

The transformed object-creature has:

AC from selected spell-form profile;
saves = captured caster PB;
ordinary unproficient ability/check modifier = +0 unless the profile expressly supplies something else;
ordinary nonmagical sight/hearing under the general perception rules;
no darkvision, tremorsense, special smell, etc. unless profile explicitly supplies it;
speech/hands only if profile permits them — but object-origin creatures are barred from humanoid profile, so current permitted profiles provide no ordinary speech/hands;
no Wounds;
no death saves;
no Stable/dying state;
no soul;
no resurrection entitlement.

It uses the reviewed controlled-companion attached phase rather than its own initiative turn.

At structural 0 HP:

it is physically destroyed;
the True Polymorph creature manifestation ends;
its slot is released;
no corpse/body/soul/XP/loot resource is generated;
the original object identity remains recorded as destroyed, not magically reconstructed.
Creature → object / object → object

Use:

AC 12;
preserve same current/max durability ledger;
no new resistance/immunity from output material.

Do not import a general object-immunity package. Target-type legality of conditions remains the responsibility of the canonical condition engine; this draft grants no blanket immunity.

Corpse/significant remains are not eligible as “discrete objects” for True Polymorph unless a later exact source expressly authorizes corpse targeting. 
Pasted text

7. Immutable physical origin

Confirmed.

Every transformation record carries immutable:

earliestPhysicalOrigin = creature | object

plus the earliest origin identity.

If earliest origin is object, then through every later:

Polymorph;
Mass Polymorph;
True Polymorph recast;
control change;
suppression;
dispel/reapplication;

it remains object-origin.

Consequently it can never acquire through transformation laundering:

a soul;
ordinary creature healing eligibility;
resurrection eligibility;
reproduction;
XP/loot;
harvestable corpse;
class/rest resources.

The non-humanoid profile restriction also follows object origin through subsequent creature-form transformations.

Conversely, creature→object→creature remains the same original creature:

same character identity;
same HP/maxHP ledger;
same Wounds/conditions;
same class/resources;
not converted into a companion simply because it temporarily became an object.

Once it again has creature anatomy, its ordinary creature healing eligibility returns because its earliest origin is creature.

Source-qualified nonorganic repair for object-origin identities remains a separate future legality interface; ordinary healing does not substitute for it. 
Pasted text

8. True Polymorph object-creature slot and commands

Accept the proposed slot rule.

The slot key is:

originalCasterId → objectOriginCreatureSlot

Reserve it when an object→creature True Polymorph successfully applies its shaping transformation, before stabilization.

It remains occupied through:

shaping;
permanent stabilization;
temporary antimagic suppression;
control loss;
controller change.

A second distinct object-origin creature attempt by the same original caster is rejected before payment while the slot is occupied.

Transforming/recasting the same underlying object-origin identity does not consume a second slot.

Release only when that transformation identity actually ends through:

dispel/allowed ending;
physical destruction;
permitted replacement that no longer leaves it an object-origin creature.

There is no free post-stabilization dismissal.

Slot ownership remains with the original True Polymorph caster, even if control later changes.

Command behavior reuses the established controlled-companion contract:

source-qualified command range: 60 feet unless an exact exception says otherwise;
owner must perceive/legally command it;
one owner BA companion command;
one owner offensive-companion allowance;
attached resolution;
uncommanded move + Dodge;
no independent damaging turn.

Transforming another owner's existing summoned/companion creature does not change its existing source owner/controller/allegiance. True Polymorph only creates caster control automatically for an object-origin creature created by that caster's object→creature mode. 
Pasted text

9. Permanent object templates, mass and value

Adopt a deterministic template set.

Allowed mundane object templates
barrier/slab
ramp/wedge
open-container
static-furniture
simple-one-piece-tool

They may have ordinary fixed geometry but no actuated mechanism.

Specifically excluded:

doors with working hinges/latches;
locks;
keys;
articulated mechanisms;
gears;
clocks;
traps;
firearms/weapons requiring mechanisms;
precision instruments;
sealed pressure vessels;
documents/credentials.

An open container may be hollow. Static furniture can consist of permanently joined simple pieces but has no moving parts.

Mass

NEW exact rule: resulting object mass must be <= recorded pre-transformation physical mass.

No approximation upward.

If canonical mass is unavailable, object-producing mode is ineligible until a mass value is supplied.

Object → object value

Result's documented recoverable/sale value cannot exceed the earliest object-origin value ceiling.

Missing value data makes an economically usable object→object transformation ineligible until supplied.

Creature → object

Require actual creature/body mass.

Result mass cannot exceed that mass.

The transformed object has no independent sale, salvage or harvest value while the creature-origin transformation exists. It is the creature's transformed body, not newly manufactured inventory.

It cannot become:

consumable;
food;
medicine;
ammunition;
currency;
gemstone;
rare material;
key;
credential;
valuable crafting stock.

Chained transformations never rebase either mass or value ceiling upward. 
Pasted text

10. Equipment through profile changes

Confirm the proposal with one deterministic rule for incompatibility.

Original equipment

Equipment present on the creature when transformation begins melds into the transformation record as already specified.

It is inaccessible and contributes only certified compatible passive bonuses.

Equipment acquired afterward

A compatible humanoid/handed profile may use external equipment normally.

Actually worn compatible armor/shield can contribute to formNormalAC once, under ordinary equipment rules. “Melded gear excluded” does not forbid later external armor.

Switching to incompatible anatomy

External equipment acquired after transformation does not become newly melded.

Before the anatomy switch completes:

compatible retained items remain equipped/held;
any item the destination profile cannot wear/hold is dropped into the subject's current space;
if that exact space cannot legally contain it, place it in the nearest legal adjacent space chosen by the controller/caller under normal placement rules.

Dropped item identity remains real.

It does not reappear on later reversion.

Only equipment that belonged to the transformation's original meld set returns with the original anatomy, and even that return never reconstructs independently destroyed/lost equipment if some future effect legally altered it.

No duplication occurs. 
Pasted text

11. Mass Polymorph atomic occupancy

Confirm the stricter proposed preflight.

Before payment, for each selected target construct two possible footprints:

Oᵢ = unchanged/original footprint if it saves;
Tᵢ = transformed footprint if it fails/waives.

The casting is legal only if every possible combination of independent save outcomes can coexist.

Implementation need not enumerate all 2^N outcomes. Pairwise validate that for every two distinct targets i,j, every pair among:

Oᵢ vs Oⱼ
Oᵢ vs Tⱼ
Tᵢ vs Oⱼ
Tᵢ vs Tⱼ

is spatially legal/nonoverlapping.

A target's own Oᵢ and Tᵢ may overlap because only one will exist.

After payment and saves, all successful transformations apply simultaneously.

No sequential “target 1 grows and blocks target 10” failure is allowed.

If the preflight cannot guarantee all independent combinations, the caller must change target/profile selections before committing the cast.

Saved targets create no links.

There is no ongoing range tether.

A transformation from another caster that later replaces one Mass link ends only that target's link; the Mass caster's concentration and all other links remain. 
Pasted text

12. Exact timing and repeat-save windows

Use absolute 60-second deadlines.

Polymorph / Mass Polymorph / Shapechange

Expiry:

castTimestamp + 60 seconds

No extra-turn extension.

True Polymorph

Stabilization checkpoint:

castTimestamp + 60 seconds

provided its shaping concentration remains valid.

Shared timestamp phase order

At a timestamp where a hostile repeat save and spell expiry/stabilization are both due, order:

finish any already-started damage/event transaction;
process due hostile transformation repeat save;
apply result:
success ends target link;
failure keeps it;
then process temporary-spell expiry or True stabilization;
then ordinary administrative cleanup.

For True Polymorph, therefore, a success on the final due repeat save prevents permanent stabilization.

Damage-triggered repeat save

Trigger only on the first qualifying event per target per numbered round where:

actual normal HP damage > 0

after temporary HP absorption and all damage prevention.

Temporary-HP-only loss does not trigger it.

If the packet itself already ended the transformation through actual 0/death/Incapacitated, there is no subsequent repeat save from that ended link.

Willing recipients

A target that waived the initial save receives no hostile repeat saves merely because it later changes its mind.

For temporary creature forms it uses the previously defined rejection Action if its anatomy permits Actions.

A willing creature→object cannot do so because that anatomy is actionless.

Shapechange switching

“Afterward” means not on the casting turn.

The first internal switch may occur on the caster's next original regular turn after the cast.

Then:

maximum once on each later original regular turn;
Bonus Action;
no switching on extra turns;
no extra Action;
no free attack;
no spellcast;
no Dissonance/Refrain event.

If Shapechange was cast during a genuine extra turn, its first switch is still the next original regular turn.

The switch cadence is unrelated to companion offense budgets or numbered-round command ledgers. 
Pasted text

Resulting implementation status

These 12 decisions complete the outstanding integration boundaries for the draft implementations of:

Harmonic Bulwark
Polymorph
Shapechange
True Polymorph
Mass Polymorph

while preserving:

True Polymorph's permanent until-dispelled state after successful stabilization;
Mass Polymorph's explicit 1–10 targets;
all original class access/ranks/schools/base RP;
all 12 bounded spell-form profiles;
one-body/no-hidden-form semantics.

They should remain SOURCE-DISCUSSED / COMPLETE DRAFT — implementation and independent review pending, not active catalog entries yet. 
Pasted text
