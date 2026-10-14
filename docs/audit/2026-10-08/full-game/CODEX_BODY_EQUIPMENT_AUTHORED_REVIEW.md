# Exact authored body, equipment and carrying review

Please review the attached complete tabletop guide as a whole, including its examples, and identify any concrete inconsistencies. This is an authored rules checkpoint, not full runtime closure. The user needs a complete TTRPG; reference code and automation gaps remain separately tracked and must not become an endless prerequisite to writing the remaining game.

Your completed source reconciliation is preserved locally. The guide adopts its corrected Tiny footprint, preserved base body mass, separate pound/Load/Extraction Class procedures, and melded Load exception. It labels new mechanics provisional. Source books and earlier discussions remain preserved.

Material questions to close in this review:

1. **Repeated capture loophole.** Original melded cargo is exempt from active Load, yet each new spell transformation recaptures original plus new external gear. A Humanoid can collect external cargo up to capacity, be transformed again, and repeat. Your pre-form legal-custody restriction alone does not bound this because the previous meld is exempt. Proposed completion: record a continuous chain's meld budget from the first pre-form body's legal capacity; replacements cannot increase it, and newly recaptured external gear must fit the remaining budget. Excess stays external if compatible or is legally dropped, preflighted in the source transaction. Druid-to-Druid never recaptures. A genuine final reversion restores ordinary carrying before a new chain can begin. Please settle the limit and hostile/forced replacement behavior without making overweight gear a spell-immunity trick or permitting indefinite cargo compression. Existing meld rights and actual inventory/ownership survive; no deletion.
2. **Known weight and empty inventory.** The guide treats ordinary known-pound limits as a genuine physical ceiling, retains fractional Load, exempts empty inventory from Burdened even at zero capacity, and caps overloaded push/drag movement at 5 ft without granting movement to an immobile creature. Confirm these precise completions; do not stack optional V6 encumbrance penalties.
3. **Actual custody, including borrowed gear.** Ownership and legal custody differ. An intact borrowed sword legitimately in the character's possession should meld and return to that custody while its original owner stays unchanged. Remote owned goods never join; legitimately transferred/lost items never return. Earlier wording 'externally owned items never return' was overbroad. Confirm this correction.
4. **Inclusive containers and one cargo unit.** Count each physical item once; a native bundle Load explicitly including its contents replaces that already-included sum. Secure Cargo is one physically executable operation on one real unit/bundle, not unlimited crates relabeled a bundle. It grants no capacity, hazard immunity or success. Confirm.
5. **Provenance and forced placement.** The supplied V6 excerpt explicitly states Tiny2.5ft and Medium5ft, not separately Small5ft and Large10ft; the guide labels those two completions provisional instead of claiming an exact recovered quote. Also confirm nearest-adjacent mandatory placement is truly bounded by the same region/barriers/occupancy, with unresolved conflicts recorded, and cannot be exploited as voluntary free movement.

Additional source status: the actual Gameplay Loop JSON metadata says status=playtest-staging and notes='Machine-readable companion to GAMEPLAY_LOOP_CANON.md for V7 playtest packs. Not promoted to main.' The candidate's explicit domain reconciliation does not silently promote that file. V6/Core originals are untouched.

We should close this authored scope with a final precise revision, then continue substantial remaining game content. Full Time Loop and final whole-game/GitHub flow confirmation stay open. Please do not call a manuscript or implementation reviewed unless actually supplied here.

## Complete authored draft

# Bodies equipment and carrying

**Draft for joint review.** These procedures connect the [Druid form rules](FORM_TEMP_HP_PLAYTEST.md) and [transformation spells](TRANSFORMATION_SPELL_PLAYTEST.md). They apply to the same character, HP record and physical belongings throughout a change. They grant no additional forms, spell access, actions or resources. The approved books remain preserved.

## Entering and changing forms

Before paying for a voluntary change, choose a legal form and size, check its space at your current position, and identify any equipment that must be dropped. If the destination or required drops are illegal, the change does not begin and spends nothing. Otherwise pay the source's normal costs and resolve its actual entry effects once.

Your Druid form uses your own HP, ability scores, saves, proficiency and conditions. It supplies only its printed anatomy and features. Speech does not imply hands: none of the 26 current Druid profiles grants ordinary hand-based equipment use. Of the 12 spell profiles, only Humanoid grants hands. Each profile retains its exact size and movement permissions.

| Change | Equipment procedure |
|---|---|
| Root body to first Druid form | Record and meld the equipment physically worn, held or carried by your body, including carried containers and their contents. |
| Druid form to another Druid form | Keep the same original melded equipment. End the former form's dependent effects and start the new form under its normal rules. Reconcile newly acquired external items with the new anatomy. |
| A successful spell replaces a Druid or spell form | Close the former transformation and capture the legitimate resulting gear under the new spell's meld rules in one continuous change. There is no moment when you can use the returning equipment. |
| Shapechange changes its current spell profile | Keep compatible external items. Drop incompatible external items; they do not join the original melded equipment. |
| Suppression | Follow the spell's suppression procedure. It is not an ending or a fresh capture of equipment. Original melded gear stays inaccessible. |
| Final reversion, expiry or forced ending | Return to root anatomy, end the source's dependent effects and reconcile surviving equipment as described below. |

The continuing meld record across Druid-to-Druid changes is a **new provisional integration rule**. It prevents shifting from opening an equipment-use window between forms. A spell replacement retains the already-reviewed close-and-capture procedure.

## What melds

Record where each item was before the first change: worn in a particular slot, held in a particular hand, or carried in a particular container or on the body. Ownership alone is insufficient. A sword stored in a wagon stays in the wagon when its owner becomes a Hawk.

A backpack and each of its contents remain distinct items. Count each item's own weight or Load once; a container does not erase its contents. Melded items remain in your custody but are inaccessible. You cannot withdraw or add contents, use components, consume supplies, fire ammunition or activate equipment through the meld.

Melding never repairs damage, reloads a weapon, restores charges, replenishes supplies or creates a replacement item. Destruction, consumption and legitimate transfers remain real. Keep the current condition and quantity of each actual item.

## Using equipment in a form

| Item or effect | Rule |
|---|---|
| Original armor and shield | Melded and unusable. Exclude their worn or held AC benefits from the form's normal AC. |
| Held weapon, tool, focus or material component | Requires actual access and the appropriate anatomy. A form without hands receives no general permission to use it. |
| Effect requiring an item to be worn, held or equipped | Suspended while the item is melded. |
| Effect requiring only possession or attunement | May continue only when its exact rule is independent of the lost anatomy and physical use. An unspecified magic bonus is not automatically operative. |
| Newly acquired armor, harness, collar or container | Must fit the actual size and anatomy and have a legal way to remain attached or carried. Hands are required for held items, not automatically for every wearable item. |
| Newly acquired external gear when the form changes | Remains external if compatible. Otherwise use the normal drop procedure. It does not silently join an existing meld record. |

The possession-versus-use distinction and individual compatibility checks are **new provisional defaults**. A specific item or form can supply an explicit exception. Do not infer one from a creature's name, appearance or ability to speak. Item-specific compatibility across the full equipment catalog remains to be authored.

## Returning equipment

Resolve a final reversion in this order:

1. Keep current external items that still exist and remain legally equipped or carried by the root body.
2. Return each surviving melded item that remains in the character's legitimate custody to its recorded former slot or container, if available and legal.
3. If an external item now occupies that slot, leave it there. Return the former item as carried inventory if there is a legal place and sufficient capacity.
4. Drop an item that cannot be carried or equipped at the current position or the nearest legal adjacent item position.
5. If no legal drop position exists, record that item's placement as pending. It continues to exist; it is not duplicated, destroyed or used to displace another creature.

Current external equipment taking priority over a former slot is a **new provisional integration rule**. A returned sword may go into available carried storage instead of replacing a sword you actually acquired and equipped during the transformation. Both retain their current condition and ownership.

Destroyed, consumed, transferred, lost or otherwise unavailable items never reappear. A remote item cannot return merely because you still claim ownership of it.

## Placement and involuntary endings

A transformation does not grant movement. A voluntary size change keeps the same spatial anchor and must fit before payment. Preserve the existing footprint on a same-size change when possible.

A mandatory ending still occurs if the root anatomy does not fit. First try its normal space at the same position, then a legal squeeze under the [movement rules](COMBAT_ACTION_PLAYTEST.md). If neither fits, record a placement conflict. The **new provisional placement procedure** permits only a nearest legal adjacent placement in the same unobstructed region. It cannot pass through a wall, closed barrier or occupied space. If none exists, the conflict remains until the obstruction is removed or a legal relocation effect resolves it. This normalization spends no movement and grants no movement-triggered benefit; it grants no invented crushing damage.

Track actual height and terrain. Losing flight while unsupported starts ordinary falling from the current location; reversion never moves the creature directly to the ground. Ending a burrowing form underground does not move the creature to the surface. Master of Vermin's permission to pass through Tiny gaps changes clearance, not its printed size.

Use the actual space of the expressed anatomy:

| Size | Space | On a grid of 2.5-foot subcells |
|---|---|---|
| Tiny | 2.5 by 2.5 feet | 1 subcell |
| Small | 5 by 5 feet | 2 by 2 subcells |
| Medium | 5 by 5 feet | 2 by 2 subcells |
| Large | 10 by 10 feet | 4 by 4 subcells |

V6 explicitly supplies Tiny and Medium space. Small and Large complete this bounded table provisionally; the supplied V6 passage does not separately list them. Size category still matters even when two sizes occupy the same space. Squeezing changes clearance and its penalties; it does not change size, carrying capacity or weight. Exact Tiny occupancy requires subcells or equivalent measurement, not treating Tiny as Medium.

## Body weight and conditions

**New provisional rule:** a creature-form transformation preserves the body's existing base physical weight unless an exact rule changes it. Size alone does not change weight. A 180-pound character therefore remains 180 pounds as a Tiny Hawk or Large Bear. This is a magical transformation rule, not a claim about the weight of ordinary animals. It applies equally to the current 26 Druid and 12 creature-form spell profiles.

Record base body weight separately from equipment and condition effects. Petrified multiplies current body weight by ten once; it does not rewrite the base weight or multiply repeatedly for multiple applications. Ending or changing a form does not cure that condition. Temporary Druid form ends under its existing Incapacitated rule, then Petrified continues to apply to the reverted body. An anatomy permitted to persist keeps its own base weight and the same condition overlay.

True Polymorph object anatomy uses its actual documented output weight. Its output ceiling remains the lower of current effective input weight and earliest recorded origin weight. Include a current applicable weight-changing condition in the input, but never rebase the origin ceiling upward. Equipment, casualty Load and estimated pounds do not establish material available for a transformation. Creature-origin object anatomy has no independent sale, salvage or harvest value.

For another creature, mount, floor or platform supporting you, count your effective body weight plus all actual equipment in your custody, including melded items, once. For your own inventory capacity, count what you carry, not your own body weight. Conditions change only the items or body their exact rules affect.

## Carrying and Load

Use pounds for actual weight and Load for inventory burden. Extraction Class describes cargo danger and attention. A casualty's Load describes the difficulty of transporting a body; it is not the body's weight. These quantities answer different questions and never convert automatically into each other.

The following is a **new provisional reconciliation** of V6 physical handling with the staged Gameplay Loop inventory rules. It does not promote the historical Gameplay Loop file into the approved books. V6's optional encumbrance variant remains preserved as an alternative; do not add its penalties to this Load procedure.

| Carrier size | Physical carry limit in pounds | Push, drag or lift limit in pounds | Inventory capacity in Load | Casualty Load for a body of this size |
|---|---|---|---|---|
| Tiny | Strength score × 7.5 | Strength score × 15 | Strength score ÷ 2 | 1.5 |
| Small | Strength score × 15 | Strength score × 30 | Maximum of 0 and Strength score − 2 | 3 |
| Medium | Strength score × 15 | Strength score × 30 | Strength score | 6 |
| Large | Strength score × 30 | Strength score × 60 | Strength score × 2 | 12 |

Use the character's current Strength score, not the modifier or an imported monster score. Tiny's Inventory capacity and casualty Load are new provisional additions. The pound limits come from V6; Small, Medium and Large Load values come from the Gameplay Loop. Larger unsupported transport sizes require their own completed rule before this table can handle them.

Keep fractional Loads without rounding. An item with a printed Load uses that value. If it has only a known weight, its **provisional Load is pounds divided by ten**. A Load-only item may use ten pounds per Load as a clearly labeled estimate for ordinary hauling; this is insufficient for effects requiring documented physical mass. A container's own Load and its contents count once each; an explicitly inclusive bundle total replaces the sum it already includes.

With positive carried Load at or above half capacity and no greater than capacity, you are **Burdened**: reduce Speed by 10 feet and apply disadvantage to checks to climb, swim or move silently. An empty inventory is not Burdened, including at zero capacity. Above capacity, that inventory cannot be carried routinely; drop or transfer something, or use a legal alternative such as dragging or a vehicle. These threshold and zero-Load details are provisional clarifications.

Apply actual physical limits when handling a known weight. Between physical carry capacity and twice that capacity, pushing or dragging limits Speed to 5 feet. It does not grant movement to a creature that otherwise cannot move. An exact anatomy restriction, such as Hawk's prohibition on carrying a Medium ally, still applies even if numbers would fit. Burden penalties do not create hands, harnesses, lift or access to melded gear.

Transporting a creature must pass both checks: the carrier can physically handle the body's effective weight and associated equipment, and can accommodate the casualty Load plus the equipment's Load. Petrified multiplies the body weight by ten, not its casualty Load. Removing gear can reduce equipment weight and Load; it cannot reduce the body's weight or erase its condition.

**New provisional meld exception:** original gear that legally melds is excluded from your transformed body's active Inventory Load. Record that gear and its full Load separately while it remains inaccessible. You must have legally carried it before the first entry; transformation cannot absorb an illegal pile of cargo. New external equipment still uses the expressed form's current capacity.

When someone else carries the transformed character, count its casualty Load plus both its melded and external equipment Load. Count the effective physical body weight plus all that equipment for actual weight handling. Melding therefore provides no weightless cargo for another carrier.

On final reversion, returned gear rejoins active inventory. Resolve any excess with the return-and-drop procedure; overload cannot prevent a mandatory reversion. **Joint review question:** successive spell replacements can recapture external gear, so the final procedure must bound the total melded cargo across a continuous transformation chain. The present draft does not authorize using repeated replacements to expand storage.

## Extraction Class and Secure Cargo

Extraction Class is a danger and logistics rating, not a carrying allowance:

| Class | Cargo |
|---|---|
| 0 | Ordinary trade goods |
| 1 | Common monster parts or durable salvage |
| 2 | Uncommon, fragile or regulated cargo |
| 3 | Rare artifacts, volatile substances or living captives |
| 4 | Very rare strategic cargo or dangerous curses |
| 5 | Epic cargo likely to attract sovereign or faction intervention |
| 6 | Legendary cargo requiring a dedicated extraction operation |

Retain relevant Fragile, Volatile, Cursed, Living, Contraband, Perishable and Attention tags. A light object can carry a high Extraction Class, and a heavy ordinary crate can remain Class 0.

**New provisional wording for Secure Cargo:** spend an Action on one legal attach, lift, transfer or protective operation involving one discrete cargo unit or bundle with an assigned Extraction Class. The unit must be physically handleable as declared; naming an entire convoy a bundle does not make it one operation. The action grants no extra capacity, hands, equipment, automatic success, invulnerability or reduction in Extraction Class. Apply actual restraints, harnesses, checks, hazards and source-specific handling requirements.

## Examples

**The remote sword.** A Druid wears armor, holds a staff and carries a pack containing two potions. A spare sword is in a wagon. The armor, staff, pack and both potions meld when the Druid changes. The sword remains in the wagon. Neither potion can be consumed from the melded pack.

**A compatible harness.** A transformed creature acquires a harness made for its present anatomy. A later change checks the harness against the destination form. If it does not fit, the voluntary change requires a legal drop. The harness is neither erased nor added to the old melded equipment.

**The crowded hand.** A spell Humanoid acquires and holds a new weapon. When the spell ends, root anatomy can keep that weapon if legal. The original melded weapon returns to an available legal carrying position, or is dropped if necessary. It does not replace or duplicate the new weapon.

**The loaded Hawk.** A Strength 9 Druid becomes Tiny with 3 Load of legally melded gear. It stays inaccessible and does not use the Hawk's active capacity. Tiny capacity is 4.5 Load and half capacity is 2.25; an additional 3 Load of external cargo in a genuinely compatible carrying arrangement would make the Druid Burdened. A rescuer carrying that Hawk must count 1.5 casualty Load plus all 6 Load of equipment, and separately satisfy its actual weight. The transformation preserves the Druid's base body weight.

**The stone casualty.** A Medium ally has a documented base weight of 180 pounds and becomes Petrified. The body now weighs 1,800 pounds but still contributes 6 casualty Load. A Strength 18 Medium rescuer can normally carry 270 pounds or push, drag or lift 540 pounds, so cannot move that body alone through these ordinary procedures, even with enough spare Load capacity. Additional gear is counted separately.

## Source decisions and implementation status

The [first body and equipment conference](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_BODY_EQUIPMENT_CONFERENCE.md) supplies the equipment procedures. The [additional exact evidence](../../../../docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_CARRYING_EVIDENCE.md) and [GPT's completed reconciliation](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CARRYING_RECONCILIATION.md) preserve the V6, Gameplay Loop and Core conflicts and their dispositions. The corrected candidate above replaces the first conference's full-cell Tiny footprint, factor-four mass proposal and automatic active Load from melded equipment. This exact authored draft still requires joint review, including chain cargo limits, zero-Load, inclusive-container, known-weight and cargo-unit clarifications.

The current Druid helper does not yet update the shared body, equipment custody or geometry. The spell helper's coarse hands check does not implement the full compatibility procedure. The finite ground-plane temporal helper does not model elevation, burrowing or Tiny subcells. The authored rules and these implementation gaps are separate; none of them enables full Time Loop or closes the whole-game review.
