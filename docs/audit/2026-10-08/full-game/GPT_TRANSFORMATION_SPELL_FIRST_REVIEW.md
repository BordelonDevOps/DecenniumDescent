# GPT five-spell first design review and clock addendum

ChatGPT said:
Clock addendum

Confirmed. The nonzero-start anchoring remains inside the previously accepted clock contract.

_anchor() establishes the six-second owner phase exactly once from the first authoritative clock observation/use. A first regular marker at time 5 therefore produces due markers at 11, 17, 23, etc.; later form changes, initiative transitions, rests, or ability uses cannot re-anchor it. The added regressions correctly demonstrate Slam blocked after the first tick at 11 and ready after the second at 17. The suite is now 165 checks + 1,053 arbitration/damage scenarios PASS. 
Pasted text
 
Pasted text

I would retain the existing form/buffer closure with this addendum.

Five-spell source conference

The following are draft operational proposals. They preserve all five existing spell identities, class access, ranks, schools and base RP costs. Where the supplied catalog/Core data are silent or contradictory, I label the rule NEW rather than treating it as recovered canon. The source batch itself explicitly calls for this distinction. 
Pasted text

1. Harmonic Bulwark

The reliable source fact is the spell's own statement:

5 temporary HP per RP spent.

It is Rank 3 for every listed class, with class-specific learn levels and base cost 5 RP. The nearby Mana Shield record is only a possible historical alias, so its Action/60-foot/V,S,F metadata cannot silently become recovered Harmonic Bulwark text. 
Pasted text

NEW operational metadata: Action, 60 feet, V/S/F, one willing creature you can perceive. These are adopted as provisional implementation choices, not as proof that Mana Shield and Harmonic Bulwark are the same source.

The RP transaction should be:

creditedRP = actualBaseRPpaid + discretionaryConversionRP

where:

normal Rank-3 base cost is 5 RP;
explicit legal discounts may reduce actualBaseRPpaid;
discretionaryConversionRP = X, chosen from 0 through PB and actually paid;
X is an additional conversion payment and cannot itself be discounted;
Dissonance/Refrain surcharges are paid normally but do not increase creditedRP;
a free/waived base cast contributes 0 credited base RP;
a copy/release that pays no Harmonic Bulwark RP does not manufacture a new RP-scaled shield unless its own copy rule explicitly copies an already-resolved buffer event.

Shield offer:

5 × creditedRP

A casting with creditedRP=0 has no legal effect and should be rejected before payment rather than producing a zero-grant cast.

Payment happens before temp-HP arbitration. A weaker/equal resulting grant can therefore lose to an existing shield while all actual RP remains spent.

The casting itself is instantaneous; because no shield lifetime is supplied, the accepted grant uses the V6 default: depleted/replaced/recipient's next completed long rest.

2. Durations and concentration for the four transformation spells

Core supplies Action/range/components but calls Polymorph, Shapechange and Mass Polymorph “Instantaneous,” which cannot operationally describe an ongoing form. True Polymorph explicitly says Until dispelled. 
Pasted text
 
Pasted text
 
Pasted text
 
Pasted text

Use these NEW reconciliations:

Spell	Operational duration
Polymorph	Concentration, up to 1 minute
Shapechange	Concentration, up to 1 minute
Mass Polymorph	Concentration, up to 1 minute
True Polymorph	Concentration during a 1-minute shaping period; if maintained for the full minute, it becomes persistent until dispelled and no longer requires concentration

True Polymorph therefore keeps meaningful permanence rather than being reduced to a short combat buff.

3. Willing/hostile targets, saves and agency
Polymorph

One willing or unwilling physical creature.

A willing creature may waive the initial save.

An unwilling creature makes a NEW Constitution save against the caster's spell DC.

On failure it transforms but retains control of its decisions. The player still chooses movement, targets and available Actions.

While the hostile transformation remains:

repeat CON save at the end of each original regular turn;
first time each numbered round the target suffers positive actual HP damage, make one additional immediate CON save after that packet;
success ends that target's transformation.

Damage does not automatically end the effect.

Mass Polymorph

Same procedure independently for each target.

Shapechange

Self only. No save.

This is a NEW narrowing of the supplied 120-foot Core range because the actual spell description is reflexive: “Transform into different creature each round.” The original 120-foot metadata stays preserved in provenance. 
Pasted text

True Polymorph

Creature → creature:

willing target can waive save;
unwilling target makes the same CON save;
while the first-minute shaping concentration continues, it receives the same end-turn and once-per-round damage-triggered repeat saves;
once the full minute completes, the form stabilizes until dispelled and no longer supplies repeat saves.

Creature → object:

willing creatures only.

This avoids creating a permanent whole-Action denial that would conflict with the reviewed hard-denial ceiling.

Object → creature/object:

no save;
object eligibility must pass the physical-object gates below.

Explicit transformation immunity, legendary defenses/resistances and other actual boss protections remain effective. None of these spells bypasses them.

All casts validate access, target, chosen profile, space and resource availability first; then Action/RP/Dissonance/Refrain costs commit; then hostile saves resolve. A successful save does not refund the spell.

None of the supplied spell-form profiles removes the target's entire Action. Losing hands/speech may make some class abilities unusable, but the subject retains movement and an ordinary form attack, so that alone is not whole-Action hard denial.

4. Finite spell-form profiles

Do not use bestiary stat blocks.

I recommend the following NEW internal spell-form profiles. They are rules records, not new named powers or creatures.

Polymorph and Mass Polymorph may use only the R4 profiles. Shapechange and True Polymorph may use both R4 and R9 profiles.

All creature-origin profiles:

retain the subject's HP/max HP/temp HP/Wounds/conditions/attributes/PB/identity;
use the original caster's spell attack bonus for the supplied natural attack;
add caster M=max(1, casting modifier) to profile damage;
have no multiattack;
grant no spellcasting, resources, legendary actions or monster abilities by themselves;
use one natural/form attack per ordinary Action;
retain ordinary senses except where stated;
treat natural/form attack identity separately from unresolved weapon-only proc taxonomy.
Profile ID	Tier	Size	Movement	Speech / hands	AC	Natural attack	Passive anatomy
spellform.humanoid	R4	Medium	walk 30	yes / yes	formNormalAC	1d6+M bludgeoning	none
spellform.predator	R4	Medium	walk 40	no / no	max(formNormalAC,13)	1d8+M slashing	none
spellform.brute	R4	Large	walk 30	no / no	max(formNormalAC,15)	2d6+M bludgeoning	none
spellform.avian	R4	Small	walk 10, fly 50	no / no	max(formNormalAC,13)	1d6+M slashing	flight
spellform.aquatic	R4	Medium	walk 20, swim 50	no / no	max(formNormalAC,14)	1d8+M piercing	water breathing
spellform.burrower	R4	Medium	walk 30, burrow 15 through loose soil	no / no	max(formNormalAC,14)	1d8+M bludgeoning	loose-soil burrow
spellform.greater-brute	R9	Large	walk 40	no / no	max(formNormalAC,17)	2d8+M bludgeoning	none
spellform.greater-winged	R9	Large	walk 20, fly 60	no / no	max(formNormalAC,16)	2d8+M slashing	flight
spellform.elemental-air	R9	Medium	fly 60, hover	no / no	16	2d8+M lightning	lightning resistance
spellform.elemental-earth	R9	Large	walk 30, burrow 20 loose soil	no / no	17	2d8+M bludgeoning	loose-soil burrow
spellform.elemental-fire	R9	Medium	walk 40	no / no	16	2d8+M fire	fire resistance
spellform.elemental-water	R9	Medium	walk 20, swim 60	no / no	16	2d8+M cold	cold resistance, water breathing

formNormalAC uses the already-reviewed anatomy bridge: melded armor/shields do not supply their normal AC calculation; only certified anatomy-compatible passive bonuses remain.

These values are NEW spell-profile design, not recovered bestiary statistics and not Druid class forms.

5. Retained state and attack provenance

Creature transformation retains:

same creature ID/body identity;
current and maximum HP;
current temp HP grant;
Wounds/injuries;
Stable/dying/death counters;
conditions;
all six actual attributes;
PB;
initiative entry;
concentration record;
class resources;
cooldown/rest-use ledgers;
buffs/debuffs not explicitly anatomy-dependent.

No second form HP exists.

The supplied spell-form natural attack uses the original caster's current spell attack bonus and M for Polymorph, Mass Polymorph and Shapechange.

That solves the NPC interoperability problem without importing an unreviewed monster attack modifier.

True Polymorph snapshots at casting:

caster spell attack;
spell DC;
PB;
casting modifier/M;
source class.

Its permanent form does not increase later because the original caster levels up.

The transformed subject's retained class abilities still use the subject's own normal statistics if it is anatomically capable of using them.

6. Equipment, spellcasting and voluntary ending

Creature-form equipment melds and is unavailable while melded.

No transformed creature silently gains access to:

melded weapon attacks;
shield use;
material components;
focus;
hand-dependent class abilities;
speech-dependent abilities.

A profile marked hands=yes can manipulate external objects acquired after transformation, but that does not unmeld the subject's original gear.

Speech/hands gates spell components normally.

Existing concentration can continue unless another rule ends it.

For Polymorph/Mass:

caster can end concentration using the canonical concentration-release timing, no added Action;
a willing transformed target may spend its Action on its regular turn to end its own target link.

Shapechange:

caster ends it by ending concentration;
no additional special Action is required.

True Polymorph during the first-minute shaping period:

caster can end concentration normally;
a willing creature target may use its Action to reject/end its own transformation.

After True Polymorph becomes permanent:

no free voluntary dismissal remains;
dispel, suppression, destruction/death consequences or a qualifying replacement True Polymorph are required.
7. Damage, zero HP and reversion

Polymorph, Mass Polymorph and Shapechange follow the accepted one-body procedure:

apply the active form's defenses to the triggering packet;
existing temp HP absorbs normally;
resolve actual HP/Wounds/Instant Death/death prevention;
only after same-packet replacement is complete, actual 0 HP, death or Incapacitated ends the transformation.

A legal instead remain at 1 HP therefore prevents forced reversion.

Reversion:

does not heal;
does not change maximum HP;
does not restore temp HP;
does not restore Wounds;
does not restore missing limbs/body matter;
does not reroll the triggering damage.

If the transformed creature actually died, the corpse returns to its natural anatomy when the temporary spell ends, but remains dead.

True Polymorph

True Polymorph does not automatically end merely because the target reaches 0 HP.

Once permanent, death/destruction occurs to the same physical identity in its transformed anatomy.

If later dispelled:

a dead transformed creature becomes the original creature's corpse, still dead and at 0;
missing/destroyed matter is not recreated;
dispelling is not resurrection or healing.

A creature permanently transformed into an object that is physically destroyed has had its same physical identity destroyed. Dispel cannot reconstruct missing vital matter.

An object-origin transformed creature that is destroyed does not create a soul, corpse-resource entitlement, XP or loot.

8. Shapechange switching

Operational target is Self, despite preserved Core range 120. This narrowing is explicitly NEW.

On initial cast choose one legal R4 or R9 profile.

Once on each of the caster's original regular turns, the caster may use a Bonus Action to switch to a different legal profile.

Switching:

is not another spell cast;
costs no additional RP;
creates no new Dissonance/Refrain event;
does not clear Refrain;
does not restore HP/temp HP/resources;
does not reset class abilities/rest uses;
does not create another body;
retains conditions and concentration;
requires legal space for the destination anatomy.

An identical-profile switch is rejected before BA expenditure.

Changing from a flying profile to a nonflying profile while unsupported begins ordinary falling immediately after the switch.

There is one Shapechange spell record and one current anatomy profile, not multiple latent forms.

9. True Polymorph modes
Creature → creature

Target must be an active physical creature.

Use one legal R4/R9 spell profile.

Agency remains with the transformed creature.

Creature → object

Target must be willing.

NEW object form bounds:

resulting size Tiny through Large;
no more than one size category away from the creature's current size;
inert mundane object;
AC 12;
no movement, actions, Reactions, speech, senses or hands;
same underlying HP/max HP/temp HP/Wounds/body identity;
no magical properties or new valuable material.
Object eligibility

True Polymorph may target only a discrete:

nonmagical;
unattended;
unworn;
uncarried;
unattuned;
Large-or-smaller object;
not a structural part of a building/terrain feature;
with a canonical structural current/max HP record.

Artifacts, active magical devices and objects lacking a resolvable durability identity are not eligible for these draft modes.

Object → creature

Choose one R4/R9 non-humanoid creature profile.

The object's structural HP/max HP become the one durability ledger for the transformed creature; no second creature HP pool is created.

It:

has no soul;
has no class levels/resources;
cannot generate XP/loot/corpse resources;
cannot reproduce;
cannot be resurrected;
receives no ordinary HP healing because that would become free object repair if dispelled;
may receive temporary HP normally.

The creature is a controlled companion of the caster.

It uses:

the reviewed owner-wide BA command;
the reviewed one offensive-companion action budget;
the attached companion phase;
uncommanded defensive behavior.

Only one active object-origin True Polymorph creature per caster is permitted in this draft. This is a NEW anti-army bound.

Object → object

Result must be an ordinary inert utility object:

same size or within one category;
no greater than Large;
approximately same or lower total mass;
common mundane material;
no magical property;
no consumable, ammunition, medicine, food, currency, gemstone, rare material, document/credential, key or precision mechanism.

Its recoverable/sale value cannot exceed the original object's documented value.

This allows meaningful barriers, ramps, containers, furniture, simple tools and similar utility without material fabrication.

Dispelling and antimagic

Dispel restores the earliest underlying physical identity/state, using its current damage/destruction condition.

Antimagic suppresses the transformed anatomy without creating a duplicate. If the permanent spell resumes afterward, the same transformation record resumes.

Destroyed/missing matter remains destroyed/missing.

10. Mass Polymorph

Preserve the explicit up to 10 creatures. 
Pasted text

Before paying:

select 1–10 distinct creatures within 120 feet;
choose one R4 form profile for each target;
validate perception/line of effect;
validate each possible form's required space.

Then pay the single casting.

Each target resolves independently:

willing target may waive save;
unwilling target makes CON save;
success means that target remains unchanged;
failure creates its own target-link under the one Mass Polymorph concentration record.

Each transformed hostile target receives its own regular-end and damage-triggered repeat saves.

One target ending does not end the others.

There is no ongoing 120-foot tether after casting.

Concentration ending ends every surviving target link simultaneously.

11. Competing transformations

Use one current anatomy record per physical identity.

NEW precedence:

Druid Shapeshift can be replaced by a successful spell transformation; doing so actually ends that Druid form and all form-dependent effects. No shift/reserve refund occurs.
A temporary transformation can replace another temporary transformation only if the new spell rank is at least the existing transformation's rank.
The new cast must fully resolve and succeed before the old anatomy ends.
Once replacement occurs, the old form is gone; it does not wait underneath.
When the new spell later ends, the target returns to its natural/base identity, not to the displaced transformation.
If a target link from Mass Polymorph is replaced, only that target link ends; the caster's concentration remains for other Mass targets.
True Polymorph, once permanent, may be replaced only by a successful new True Polymorph, dispel/suppression, or an explicit future rule naming it. Polymorph, Mass Polymorph, Shapechange and Druid Shapeshift cannot silently overwrite permanent True Polymorph.
A new True Polymorph replaces the previous True transformation record rather than nesting it. Dispel then restores the underlying original physical identity, not an intermediate hidden transformation.

All five ordinary spell casts obey normal Dissonance/Refrain. Shapechange's internal profile switch is not a cast and therefore does not.

12. Implementation boundary

These proposals should become five source-specific draft objects plus one shared finite SpellFormProfile register and a transformation identity adapter.

They should not become selectable/canonical until:

source objects are written;
adversarial state tests pass;
payment/saves/concentration/reversion/object transitions are tested;
they receive independent implementation review.

That preserves the current project's review discipline.

Proposed spell-form profile register

All rows below are NEW bounded mechanics, not bestiary imports.

ID	Allowed spells
spellform.humanoid	all four creature-transform spells
spellform.predator	all
spellform.brute	all
spellform.avian	all
spellform.aquatic	all
spellform.burrower	all
spellform.greater-brute	Shapechange, True Polymorph only
spellform.greater-winged	Shapechange, True Polymorph only
spellform.elemental-air	Shapechange, True Polymorph only
spellform.elemental-earth	Shapechange, True Polymorph only
spellform.elemental-fire	Shapechange, True Polymorph only
spellform.elemental-water	Shapechange, True Polymorph only

Polymorph and Mass Polymorph are therefore broad transformation tools without becoming access to rank-9 elemental/greater anatomy. Shapechange gets flexibility and switching; True Polymorph gets the broader list plus permanence/object modes.

Complete individual draft: Harmonic Bulwark

Preserved source: Rank 3 Universal; Bard 7, Cleric 5, Mage 5, Mirrorsage 7, Tinker 10, Wizard 5, Paladin 9; base RP 5. 
Pasted text

JSON
{
  "id": "harmonic-bulwark",
  "activation": "Action",
  "rangeFeet": 60,
  "targets": "One willing creature you can perceive within 60 feet",
  "duration": "Cast instantaneous; accepted temporary HP last until depleted, replaced, or the recipient completes a long rest",
  "concentration": false,
  "components": ["V", "S", "F"],
  "resolution": "Automatic after legal payment; temporary-HP strongest-only arbitration then applies.",
  "effect": "Pay the class-specific Rank-3 base RP cost and choose X from 0 to your proficiency bonus as additional conversion RP. Gain a temporary-HP offer equal to 5 times the credited RP. Credited RP equals the actual base RP paid after legal base-cost reductions plus the actual additional conversion RP paid. Dissonance, Refrain, or other surcharge RP does not increase the shield.",
  "scaling": "5 temporary HP per credited RP. Additional conversion RP X is capped by proficiency bonus and must actually be paid.",
  "limitations": "Additional conversion RP cannot itself be discounted. Payment occurs before nonstack arbitration and is not refunded when a stronger or equal shield remains. A cast with zero credited RP is illegal. Free casts/copies that spend no credited RP create no fresh Harmonic Bulwark shield unless their own exact copy rule expressly copies an already-resolved temporary-HP event. Temporary HP are not healing and use the canonical one-active-buffer rule.",
  "designNotes": "PRESERVED: Harmonic Bulwark identity, Universal Rank 3, class access/learn levels/base 5 RP, and 5 temporary HP per RP source wording. NEW: Action, 60-foot range, one willing target, V/S/F components, PB cap on discretionary RP, exact credited-RP accounting, and V6-default shield lifetime. Action/range/components resemble the unproven Mana Shield candidate but are adopted only as provisional Harmonic Bulwark design choices; the alias is not treated as source identity."
}
Complete individual draft: Polymorph

Preserved source: Rank 4 Transmutation, Action, 60 feet, V/S/F, base 7 RP, with its exact nine-class access table. 
Pasted text

JSON
{
  "id": "polymorph",
  "activation": "Action",
  "rangeFeet": 60,
  "targets": "One physical creature you can perceive within 60 feet",
  "duration": "Concentration, up to 1 minute",
  "concentration": true,
  "components": ["V", "S", "F"],
  "resolution": "Choose one legal R4 spell-form profile and validate its space before payment. A willing target may waive its save. An unwilling target makes a Constitution save against your spell DC. On failure it transforms. At the end of each of its original regular turns, and once per numbered round after it suffers positive actual HP damage, it may repeat the save; success ends the transformation.",
  "effect": "Replace the target's current anatomy with the chosen R4 spell-form profile while preserving one body, current/max HP, temporary HP, Wounds, conditions, attributes, proficiency, identity, resources, initiative and condition clocks. The supplied form attack uses the original caster's current spell attack bonus and M. Equipment melds and is unavailable unless a separate anatomy-compatible passive bonus is certified. The target retains control of all decisions.",
  "scaling": "No automatic profile, damage, target-count or duration scaling. Use only the bounded R4 spell-form register.",
  "limitations": "No monster stat block, multiattack, class spellcasting, legendary power, new resource pool or second HP pool is gained. Speech, hands and movement come only from the selected profile. A willing target may spend its Action on its regular turn to end its own Polymorph. Actual 0 HP, death or Incapacitated after same-packet prevention resolves ends the spell without healing. Explicit transformation immunity and legendary defenses apply normally. Natural/form attacks do not automatically qualify for unrelated weapon-only features.",
  "designNotes": "PRESERVED: Polymorph identity, Transmutation Rank 4, exact class access, Action, 60 feet, V/S/F and base 7 RP. NEW: one-minute concentration, target/save/repeat-save procedure, R4 finite profile list, same-body state retention, caster-derived form attack, equipment/anatomy rules and zero-HP reversion."
}
Complete individual draft: Shapechange

Preserved source: Rank 9; Druid/Mage Transmutation, Wizard Illusion; level 17 access; Action, source Core range 120, V/S/F, base 26 RP; description says transform into a different creature each round. 
Pasted text

JSON
{
  "id": "shapechange",
  "activation": "Action",
  "rangeFeet": 0,
  "targets": "Self",
  "duration": "Concentration, up to 1 minute",
  "concentration": true,
  "components": ["V", "S", "F"],
  "resolution": "Choose one legal R4 or R9 spell-form profile on cast. No save. Once on each of your original regular turns afterward, you may use a Bonus Action to switch to a different legal profile. The new anatomy must fit the available space.",
  "effect": "You retain your identity, current/max HP, temporary HP, Wounds, conditions, attributes, proficiency, resources, initiative and existing effects. Only your current anatomy/profile changes. Each supplied natural attack uses your current spell attack bonus and M. Profile switching does not create a new body, heal, refresh resources, restore temporary HP or reset rest/recharge uses.",
  "scaling": "No automatic scaling beyond the bounded R4+R9 profile register.",
  "limitations": "Only one Shapechange anatomy exists at a time. An identical-profile switch is rejected before Bonus Action payment. Internal switches are not spell casts and do not create new Dissonance or Refrain events. Equipment remains melded through switches. Losing flight while unsupported begins ordinary falling. Actual 0 HP, death or Incapacitated after same-packet prevention ends Shapechange without healing. The spell grants no Druid Buffer Reserve, Form Surge, Shapeshift use or Druid form features.",
  "designNotes": "PRESERVED: Shapechange identity, Rank 9, Druid/Mage/Wizard access and class-specific schools, Action, source 120-foot metadata, V/S/F, base 26 RP, and the core concept of changing creature form each round. NEW: operational target narrowed to Self, one-minute concentration, Bonus Action once-per-original-regular-turn switching, finite R4/R9 profiles and same-body state rules. The original 120-foot source field remains preserved in provenance despite the self-target operational narrowing."
}
Complete individual draft: True Polymorph

Preserved source: Rank 9, Cleric Universal and Druid/Mage/Wizard Transmutation, level 17, Action, 120 feet, V/S/F, base 26 RP, explicitly until dispelled, and creature/object transformation. 
Pasted text

JSON
{
  "id": "true-polymorph",
  "activation": "Action",
  "rangeFeet": 120,
  "targets": "One eligible physical creature or one eligible discrete nonmagical unattended object within 120 feet",
  "duration": "Concentration during a 1-minute shaping period; if maintained for the full minute, the transformation persists until dispelled without further concentration",
  "concentration": "Required during shaping; not required after permanent stabilization",
  "components": ["V", "S", "F"],
  "resolution": "Choose creature-to-creature, willing-creature-to-object, object-to-creature, or object-to-object before payment. Creature-to-creature may affect an unwilling target on a failed Constitution save; while shaping, that target repeats the save at each original regular end and once per numbered round after positive actual HP damage. Creature-to-object requires willingness. Objects make no save. If concentration survives the full shaping minute, the result becomes persistent until dispelled.",
  "effect": "Creature transformations retain one identity and one HP/durability history. Creature-to-creature uses any legal R4 or R9 spell-form profile. Creature-to-object creates one inert mundane object anatomy without healing or a new durability pool. Object-to-creature uses the object's existing structural HP as its one durability ledger and creates a controlled no-soul companion using an eligible non-humanoid R4/R9 profile and the caster's snapshotted spell statistics. Object-to-object changes only mundane form/material within the bounded utility restrictions.",
  "scaling": "No automatic scaling. Permanent attack/DC values supplied by this spell snapshot the original caster's spell attack, spell DC and M when cast.",
  "limitations": "No mode creates XP, loot, a soul, resurrection entitlement, valuable material, consumable stock, ammunition, currency, medicine, food or magical properties. Carried, worn, attuned, magical, artifact, structural-terrain and undefined-durability objects are ineligible. Object-origin creatures cannot receive ordinary HP healing as a means of repairing their source object. Only one active object-origin True Polymorph creature per caster is permitted. Such a creature shares the owner's companion Bonus Action/offensive budget and gains no independent turn/resources. Permanent True Polymorph does not end at 0 HP merely to restore the original form. Death/destruction remains real; later dispelling changes anatomy only and never heals, resurrects or recreates missing matter.",
  "designNotes": "PRESERVED: True Polymorph identity, Rank 9, exact class access/schools, Action, 120 feet, V/S/F, base 26 RP, creature/object scope and meaningful until-dispelled permanence. NEW: one-minute shaping/stabilization procedure, save/agency rules, bounded form register, object eligibility/size/value rules, object-origin companion contract, one controlled-object-creature cap, durability conservation and destruction/dispel semantics."
}
Complete individual draft: Mass Polymorph

Preserved source: Rank 9 Transmutation, Druid/Mage/Wizard level 17, Action, 120 feet, V/S/F, base 26 RP, and up to 10 creatures. 
Pasted text

JSON
{
  "id": "mass-polymorph",
  "activation": "Action",
  "rangeFeet": 120,
  "targets": "Up to 10 distinct physical creatures you can perceive within 120 feet",
  "duration": "Concentration, up to 1 minute",
  "concentration": true,
  "components": ["V", "S", "F"],
  "resolution": "Before payment choose 1-10 targets and one legal R4 spell-form profile for each, validating each possible anatomy's space. Willing targets may waive saves. Each unwilling target independently makes a Constitution save. Failure creates that target's transformation link. Each hostile transformed target repeats the save at its original regular-turn end and once per numbered round after positive actual HP damage. Success ends only that target's link.",
  "effect": "Each failed/waived target gains exactly one selected R4 anatomy while retaining its own identity, current/max HP, temporary HP, Wounds, conditions, attributes, proficiency, resources, initiative and condition clocks. Each target's supplied natural attack uses the original caster's current spell attack bonus and M. All transformed targets share one concentration record but otherwise resolve their own transformation endings independently.",
  "scaling": "Exactly up to 10 creatures. No generic three-target cap and no automatic access to the R9-only greater/elemental profiles.",
  "limitations": "Casting range and line of effect are checked only when the spell is committed; there is no ongoing range tether. One target ending does not end another. Concentration ending removes every remaining target transformation. No target gains monster stat blocks, multiattack, resources, class features or a second HP pool. Equipment/anatomy, natural-attack taxonomy, damage/reversion and agency follow the shared spell-transformation chassis.",
  "designNotes": "PRESERVED: Mass Polymorph identity, Transmutation Rank 9, Druid/Mage/Wizard level-17 access, Action, 120 feet, V/S/F, base 26 RP and explicit up-to-10-creature scope. NEW: one-minute concentration, preselected per-target R4 profiles, independent saves/endings, no ongoing tether and shared same-body transformation rules."
}
Conference disposition

The recharge-clock addendum remains accepted, so the previously closed selected 175+5 form/buffer reference interface remains REVIEWED / reference-VALIDATED.

For these five named spells, the appropriate status is now:

SOURCE-DISCUSSED / COMPLETE DRAFT PROPOSALS — implementation and independent review pending.

Harmonic Bulwark, Polymorph, Shapechange, True Polymorph and Mass Polymorph are no longer conceptually undefined in this conference, but these drafts should not yet be promoted to active operational catalog entries.

The remaining whole-game gaps are still open, including the final item/anatomy compatibility matrix, global natural-weapon interoperability, the other incomplete feat clauses/components, Time Loop/world-state conservation, broader spell/catalog review, human balance, and the full tabletop/video-game runtime.
