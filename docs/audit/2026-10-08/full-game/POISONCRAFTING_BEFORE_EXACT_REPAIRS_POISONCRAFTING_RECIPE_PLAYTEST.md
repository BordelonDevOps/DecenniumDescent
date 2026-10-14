# Poisoncrafting recipes — campaign-playtest procedures

**Draft awaiting exact manuscript review.** The source conference and Thief-interface follow-up approve the authoring direction. Completed cards still require exact review. Use the [public cards](POISONCRAFTING_PUBLIC_RECIPE_CARDS.md), [crafting framework](CRAFTING_HARVEST_PLAYTEST.md), [Core resolution](CORE_RESOLUTION_PLAYTEST.md), [conditions](CONDITIONS_PLAYTEST.md), [custom condition bindings](CUSTOM_CONDITION_BINDINGS.md) and [equipment procedures](EQUIPMENT_ITEM_PROCEDURES.md).

These are fictional game procedures. Every original source identity, current and legacy effect, component occurrence, work requirement, value and visibility boundary remains preserved. Current complete effects control older names, abbreviated fields and optional guidance. A source `developed` label is not approval. The new operational choices below are explicit playtest integration rather than quotations of recovered canon.

## Finished doses and common resolution

Each output unit is one magical nonspell **poison-effect** consumable. It requires no generic RP, RC, attunement, focus, concentration, class or proficiency to use. It creates no spell rank, spell access, Counterspell permission or Dissonance/Refrain event. All elemental varieties remain actual poison-effect applications; the printed damage type still controls damage defenses. Names and ingredient properties grant no additional effects. Only the current `mechanics.tag` supplies an operative recipe tag; preserve original tags and legacy text separately.

An actual legal exposure requires the appropriate delivery procedure. Resolve the printed **binary CON save** once: total meets DC succeeds, otherwise fails; natural 1/20 have no generic outcome shift. Success applies neither component. Failure attempts the exact printed initial damage and the printed condition independently. The initial damage is a separate save-based packet, not extra weapon damage; a critical weapon hit does not double its dice or make the poison save automatically fail. Apply the ordinary damage, temporary-HP, death and Wound procedure to each genuinely separate event without splitting or combining packets to manufacture thresholds.

Damage immunity and condition immunity operate independently. A zero-damage result does not prevent an otherwise legal condition; condition immunity does not erase damage. Explicit immunity covering the entire poison-effect/toxin application prevents both components and any new ongoing record, while the spent physical entitlement remains spent. No unnecessary die rolled for an application already prevented wholesale counts as a valid failed poison save.

All actual source-specific anatomical restrictions still apply. Creature type alone supplies no invented immunity. A living/active creature must be a legal target of the actual delivery and effect; a Dead body receives no active creature-condition record. Inhaled delivery specifically requires actual ambient-gas breathing. Injury and contact have the distinct physical eligibility below rather than a universal breathing requirement.

Every real exposure receives a unique `exposureId`, dose/deployment identity, recipe, applying DC, target, initial result and damage history. Replaying a record cannot spend another dose, roll another initial save or deal the initial damage again. Repeat saves **never repeat initial damage**. A suppressed initial effect is not banked for later unsuppression.

## Ownership, ongoing records and refresh

Assign a stable `poisonOwnerKey` when the dose is deployed:

| Delivery | Owner |
|---|---|
| Injury | Creature performing the coating Action, including for another creature's weapon or ammunition. |
| Contact | Creature coating or arming the object/surface. |
| Inhaled | Creature releasing the dose; an unattended mechanism retains the creature that committed/armed its dose. |
| No responsible character | Actual immutable deployment/source-entity key. This is a real source identity, not a new key manufactured by copying a record. |

The crafter, purchaser or later wielder is not automatically the owner. Transferring the item does not change an established deployment's key. Record the actual owner separately from any character applying an independent class rider.

The ongoing identity is **recipe ID + poison owner + target**. Each later genuinely paid exposure still receives its own initial save and damage. If its condition legally applies while the same ongoing identity remains present, refresh that one record to the later legal expiry without increasing magnitude. It does not create extra same-record ticks or duplicate penalties. A successful later initial save changes nothing about an older record. An expired/removed record cannot be resurrected by replaying its history; a new real exposure can create a new record if otherwise legal.

Different recipes/owners remain independent records with their own saves and endpoints. Actual same-name penalties and family arbitration still apply once rather than stacking unprinted magnitude. These crafted poisons do not inherit the Thief's maximum-two-class-recipes occupancy rule. **Stunned is the explicit refresh exception:** an owner that spent its hard-denial allowance cannot establish or refresh Stunned again against that target in that encounter.

For this exact-review draft, refreshing an existing Frightened record retains that record's original fixed fear locus; it extends the existing relationship rather than choosing a new source. Once that record ends, a later real application records its new actual exposure locus. This finite refresh clarification is submitted for exact review.

## Duration and ending saves

An ordinary condition has **ten future regular target-end markers**, representing one minute outside initiative. A singleton Flawed dose has five markers/30 seconds. Record the chosen virtual marker sequence once; initiative-order changes cannot shorten, extend or duplicate it. Extra turns and extra Actions never consume duration markers or add repeat saves.

- Application before the target's next regular turn begins: that upcoming regular turn's end is marker 1.
- Application during its already-in-progress regular turn: exclude that turn's end; marker 1 is the end of its next regular turn.
- Application after its regular turn ended: the next regular target-turn end is marker 1.

Outside initiative, preserve one step per complete six elapsed seconds and the already established virtual sequence across transitions. Do not reset the clock by entering/leaving initiative. All ordinary records receive the printed repeat CON save at each scheduled marker while their condition is still present. Success ends that record. The **final marker still gets its repeat CON save before expiry cleanup**; a failed final save does not extend the effect. If cure/expiry/another legal endpoint already ended the only condition, no later repeat save or initial-damage replay occurs.

Suppression and gained immunity can make a present record inactive without ending it. Its clocks and permitted ending saves continue. Applicable cures can remove a present suppressed record; active-condition hooks require actual unsuppressed eligibility. Initial immunity that prevented application creates no record to resume later. An ordinary elapsed rest does not automatically end a hostile poison unless its actual cure rule says so.

## Injury delivery

Spend one **Action**, one available hand and one accessible dose to coat **one compatible piercing/slashing weapon or up to three compatible piercing/slashing ammunition units**. All ammunition must be present during that Action. These are finite coating entitlements from one dose, not three inventory doses. An external natural-weapon profile on self or a willing creature can qualify if it actually deals piercing/slashing damage and physically retains the coating; no default mouth/bite coating. An unwilling creature's held gear or anatomy needs separately lawful control/access.

The coating lasts **one elapsed minute from application**. The weapon spends its coating on its first qualifying hit. Each ammunition unit spends its own coating on its first hit. This is **hit-gated**, not positive-damage-gated: a legal hit exposes even when weapon damage is reduced to zero, damage-immune, prevented or fully absorbed by temporary HP. A miss causes no exposure and spends no coating entitlement. A critical gives one exposure, with no doubled poison dice. A poison-immune target still spends the entitlement on a legitimate hit.

Only one coating occupies the same weapon/ammunition unit; applying another replaces and loses the old one. Thorough washing or full immersion ends an exposed coating; incidental dampness alone need not. A missed ammunition unit retains a coating only if physically intact, legally recovered, unwashed and still within its original deadline. Recovery never refreshes the clock. A hit already spent it regardless of save outcome. Carrying a coated weapon, touching a safe grip or standing nearby does not expose anyone.

Legal coating begun before the opened-dose deadline commits that dose; the deployment's one-minute clock then replaces the inventory-open clock. The ordinary surviving empty vial remains a spent container. A crafted injury dose supplies no ingested, contact or inhaled alternative just because one would be convenient.

## Contact delivery

Spend one **Action**, one available hand and an accessible dose to coat either **one accessible object no larger than a five-foot cube** or **one contiguous five-by-five-foot surface patch**. The charge lasts **one elapsed hour from deployment**, unless spent, cleaned/washed, destroyed with its carrier or replaced on the same coated region.

The first qualifying direct contact with **exposed bodily tissue/anatomy**, without an intervening object or poison-blocking barrier, spends the whole charge whether the target saves or has damage, condition or poison-effect immunity. Protective gloves or another actual impermeable/poison-blocking covering prevent contact through that covering. A separate held object touching the patch neither exposes its holder nor consumes/transfers the charge. A coated object's actual coated exterior can expose someone whose uncovered anatomy later contacts it; this does not create new active doses through incidental transfer.

There is no new touch attack, grapple rider or forced-contact Action. A coated object used as a weapon needs an independently legal attack/action and actual qualifying bodily contact; merely hitting armor is not automatic contact exposure. Legal coating with actual Protective gloves or an Applicator creates no invented proficiency check or automatic self-exposure. Actual unprotected direct contact, if it occurs, follows the same trigger as anyone else's.

Cleaning destroys the charge into inert waste. One Action and actual wiping/washing access cleans one small object. One uninterrupted active minute cleans the full patch. For this exact-review draft, a larger eligible coated object also uses that one-minute procedure: one designated cleaner, ten consecutive regular-turn Actions and at least 60 seconds, with required access through resolution and no eleventh Action. A partial/interrupted cleaning does not create recoverable active stock or complete the cleanse. This timing/large-object completion is explicitly submitted for exact review. Runoff, cloth and rinse water never become extra poison doses.

Beginning legal deployment before the one-hour opened-dose deadline commits it; the new one-hour coating clock controls afterward. A legally cleaned object or washed glove does not retain an unrecorded second charge.

## Inhaled delivery

Spend one **Action**, one available hand and an accessible dose to release it at a **visible point with line of effect**, normal range **30 feet**, long range **60 feet**. It produces one **instantaneous five-foot-radius burst** with no attack roll. At 31–60 feet, eligible creatures gain advantage on that release's **initial** poison CON save; repeat saves gain no dispersal advantage. The vial is destroyed; no spent container returns.

Every eligible creature in the burst, including allies or the releaser, receives at most one exposure from that vial. Total cover from the burst point prevents exposure. The target must actually breathe that ambient gaseous medium at resolution. A creature that does not breathe or already has a legitimate breath-holding state is not exposed. There is no generic Reaction to hold breath after seeing release; an actual feature granting that Reaction retains its own terms.

The point must be in a **nonliquid atmosphere**. An actual air/gas pocket can qualify underwater, but a point in the surrounding liquid cannot. Breaking the vial in liquid loses it without creating the gaseous effect. No later-entering targets, persistent cloud, wind drift, second area, critical or chain reaction is created. A name implying mist or miasma grants no additional area procedure. Accidentally breaking/spilling a carried vial loses the dose; it does not automatically perform its combat release Action.

## Condition profiles

Poisoned and Blinded use their reviewed Core definitions. Poisoned imposes disadvantage on attacks and ability checks, not saving throws. Blinded prevents sight, automatically fails checks requiring sight, gives disadvantage on the creature's attacks and advantage to attacks against it. Their independent condition immunities/cures retain their normal scope.

**NEW `poisoncraft.confused`:** disadvantage on attack rolls and ability checks **other than Initiative**, and cannot take Reactions. Movement, Action, Bonus Action and the creature's choices otherwise remain available. No random behavior, compelled movement, friendly fire or whole-Action denial. Multiple applications do not multiply disadvantage or remove additional resources. Its source-qualified recognition tag is `eligibility.confused`; this grants no additional mechanics.

**NEW `poisoncraft.slowed`:** halve every existing movement speed, preserving Speed 0. Multiple poisoncraft Slowed records do not quarter speed. No teleport denial. It carries `eligibility.slowed-foe`, without becoming a Thief/class Slow record. Other independently applicable movement modifiers retain their reviewed scopes; this permission does not create an additional universal modifier rule.

**NEW `poisoncraft.weakened`:** reduce weapon/natural-weapon hit damage by 1, minimum zero. Identical flat reductions use the strongest rather than adding. No reduction to spell damage, save damage, attack rolls, ability checks or saving throws. It carries `eligibility.weakened` and remains distinct from existing class records.

These three new profiles end through their printed repeat CON save, duration, or an actual cure covering that poison/profile. Explicit poison-effect immunity blocks them; a specific immunity naming Confused, Slowed or Weakened applies only when its real scope covers the profile. A different class condition's display name does not supply immunity or a new generic cure.

**Frightened:** when established, record the actual exposure's exact spatial point as a fixed fear locus. It never follows the weapon, projectile, coated carrier, applicator or crafter. Destroying/moving the carrier does not erase/move it. The visibility-dependent disadvantage on attacks and ability checks applies only with ordinary visual line of sight to that location; Blindness, obscuration or cover can prevent it. The prohibition on willingly moving closer uses that fixed locus for the record's duration even when not visible. Forced movement retains its ordinary exception. This abstraction reveals no hidden actor and creates no hallucination, false image or mind-reading. Fear immunity and actual fear cures still apply.

**Stunned:** use the reviewed Core condition and the combined hard-denial rule below. It is not the new Confused profile and is never inferred from a recipe name or damage type.

## Burning without duplicate fire

A failed initial save attempts its source initial fire packet and **one ordinary poison-created Burning record** independently. Initial fire immunity affects that packet; Burning immunity blocks the condition; explicit poison-effect immunity blocks the application. The record supplies **1d4 fire**, not the initial poison dice, to `family.ongoing-fire` at each due regular target-end marker.

Track its source group by recipe and poison owner. All applicable ordinary/custom fire groups enter the already reviewed unified family arbitration at the same marker: highest expected unmitigated damage, then earliest application, with established tie-breakers. Only the selected group's source-permitted instances damage; all due groups consume their tick. Suppressed records do not contribute damage. Do not create an extra generic record on top of this one or put the initial damage packet into periodic arbitration.

At a due end marker:

1. Resolve due ongoing-fire arbitration and its tick.
2. If this record remains present **and future scheduled fire damage remains**, make its ordinary binary DEX ending save at the recipe's applying DC.
3. If the poison-created Burning record still exists, make the printed repeat CON save.
4. Perform expiry cleanup.

At the final marker the last tick is due, **no DEX save** occurs because no future damage remains, the source-required CON save still occurs, then expiry removes a surviving record. A successful earlier DEX/CON save, ordinary extinguish Action, full immersion or actual cure ends the record, so subsequent presence-dependent steps are skipped. Present but suppressed records retain legal cures/ending saves; damage-type immunity alone does not remove or suppress the Burning record. An actual same-owner/same-recipe refresh extends one record rather than adding same-group ticks.

A Poisoned-only cure does nothing to Burning. A remover covering the actual underlying poison application can remove its dependent Burning. Ordinary extinguishing remains legal even though its original source was a poison.

## Stunned and the shared encounter allowance

Crafted Stunned joins the existing **source character / target / encounter** hard-denial allowance across class features, spells and companions. A character `poisonOwnerKey` uses that same character's allowance. An ownerless source uses its real immutable deployment/source-entity key as the equivalent item key. Duplicating records, relabeling items or changing possession cannot mint another allowance for the same source.

Claim the allowance only when a failed initial save would actually establish Stunned and no immunity/denial rule blocks it. Initial success, Stunned immunity or whole-application immunity claims nothing. If already spent, initial poison damage still resolves under its own defenses, but Stunned cannot establish **or refresh**. If an independent owner already has the target Stunned, an unused owner can establish its own record and spend its allowance; the actual penalty does not multiply.

The one allowed record lasts until its actual save/cure/expiry. Its later scheduled saves are maintenance of that record, not new applications or new allowance costs. Removing it does not refresh the spent encounter allowance. Later doses from that owner, including a different Stunned recipe, cannot extend it. This specific rule overrides ordinary same-recipe refresh.

## Immunity, suppression and cures

Keep these scopes separate:

| Effect | Scope |
|---|---|
| Poison-damage immunity/resistance | Only the actual poison-type damage packet. Other printed damage types retain their own defenses. |
| Core Poisoned immunity | Only a Poisoned component. |
| Named condition/profile immunity | The actual named applicable condition, not every poison symptom. |
| Explicit poison-effect/toxin immunity | Entire covered application: no initial damage, condition or repeat-save record. Physical expenditure still occurs. |
| Poison-save advantage | Initial and repeat CON saves of these poison effects regardless of damage type. It does not automatically cover Burning's separate DEX save. |
| Herbalism/other Poisoned-only cure | Present removable Poisoned records within its actual one/all scope. No Confused, Slowed, Weakened, Blinded, Frightened, Stunned or Burning removal by association. |
| Explicit end-one-poison-effect cure | One present removable poison application and its dependent ongoing symptoms. Independent sources and protected removal requirements remain. |

Removing an application's sole ongoing condition leaves only history; there is no hidden continuing toxin that later reapplies it without another real exposure. A lawful whole-application cure can select a present suppressed record. Damage already resolved is not undone.

A legal suppression effect covering magical nonspell poisons makes applicable established records inactive while their clocks and permitted ending saves continue. It supplies no later replay of initial damage. A finished poison suppressed at exposure spends its physical dose without banking future damage/conditions, unless the suppressing rule expressly provides another procedure. Never treat a rankless item as a rank-zero spell to create Counterspell or rank-limited dispel eligibility.

## Thief integration

Thief **prepared doses** and crafted inventory remain separate systems. Apply Poison, Double Poison, Vein Cutter and Toxic Shiv require the Thief's actual prepared doses. These crafted recipes do not inherit Thief DC, two-projectile/two-attempt delivery, Bonus Action application, Double Poison, renewable rest preparations or the two-ongoing-class-recipes limit. Exotic Toxins creates/replaces a Thief class poison profile through its own specimen/research procedure; it grants no Crafting formula or inventory output. Preserved older class wording does not override the reviewed operational cards.

**Venom Master does bridge:** the feature owner must make the qualifying critical weapon hit, and that hit must legally deliver a crafted **injury** exposure whose initial poison save actually fails. Order: critical hit, legal exposure, initial save, then the separate Venom Master -1-save rider once/round until its printed end-next-target-turn endpoint. It never modifies the triggering save. Use its existing strongest-penalty rule with Hexroot/other Venom Master.

The coating actor need not be the Venom Master wielder. The poison keeps its existing owner/group/hard-denial key; the added class rider belongs to the Venom Master. Damage-type immunity or condition immunity, even both together, does not erase a valid failed initial poison save. Blanket poison-effect immunity prevents the application and therefore the trigger. No trigger comes from misses, initial successes, repeat saves, periodic damage, contact coating, inhaled bursts or copied attacks. For exact review, the treatment of a legitimate source-mandated automatic CON failure is explicitly queried alongside the requirement that an unnecessary die for a wholly immune application cannot trigger this feature.

**Sneak Attack:** a crafted Core Poisoned record qualifies as `your Poisoned` only if active and its poison owner is the Thief. Another creature can have delivered the hit after the Thief coated it; ownership remains the coater's. **Vile Tactics** accepts any active qualifying Bleeding/Poisoned/Crippled record without ownership. Neither predicate treats other poison symptoms or poison-type damage as Poisoned. Eligibility must exist when the hit is assessed; a later condition created by that same hit cannot retroactively qualify it. Ticks, standalone poison damage, repeat saves, companions and copied attacks create no additional Sneak Attack/Vile Tactics events. All existing frequency and weapon restrictions remain.

**Toxin Sense:** exposed perceptible poison within five feet can be recognized from real sight/smell evidence. Passive recognition gives only poison presence. A sealed unseen interior is not generically scanned, and magical status alone does not make exposed poison unknowable. Actual concealment, masking, identification restrictions and sensory limitations still control. An Action with the kit and DC12 INT+PB can identify exposed/perceptible poison or a legally accessed sample as its operational game recipe. A sealed sample normally must first be legally opened/accessed. Identification gives no crafting formula/access, hidden ingredient list, donor/crafter provenance, price/discovery secrets or Director lore; restricted formula knowledge remains gated even when a character identifies an encountered combat effect.

## Work, containers and physical accounting

Use **INT + actual Poisoner's kit proficiency** under the shared framework, with an actual Poisoner's Bench, Sealed glassware, Protective gloves and all source components. The kit is **non-artisan**; Forge Dwarf artisan time/quality permissions do not apply merely because this is crafting. Owning a kit does not supply proficiency. Retain formula/trade level, field flag/station, assistance, work/rest limits and actual mishap rules.

The first **15 active minutes**, included in the printed work, bind/stabilize legal ingredients with the required station and implements. Before binding, ordinary ingredient age and interruption rules apply. Bound material remains stable only in that actual order; it is not extractable preserved raw stock. A source work year retains its original one-year/null-hours fields; the operational **1,920 active hours** overlay is labeled separately. Optional source Director guidance is retained as optional guidance, not an automatically imposed extra ritual/material gate.

Each finished dose has **0.1 lb compound + 0.1 lb vial = 0.2 lb gross**, one vial slot, **AC13/structural HP1**. A physical container remains necessary. Before the completion check, reserve enough actual source/supplementary vessels for **floor(1.5Q)** maximum output. No post-roll acquisition supplies a missing reserve.

Consumed source Glass-vial units can supply `min(source vessel units, actual finished quantity)` output vessels. Extra consumed source vessels become spent process glassware on a successful craft, not returned expensive stock. Ordinary supplementary empty vials cost **1 gp/0.1 lb** each by reference, with actual finite supplier quotes and transaction rounding. Owned ordinary suitable vials need not be bought again. Unused supplementary vessels return to inventory. Generic failed/Mishap source recovery still follows the shared framework; successful surplus-glass handling does not abolish a legal failure recovery.

Only actual consumed **non-tool/non-vessel mass**, less the selected retained catalyst, can supply compound. Exclude all tool/vessel mass even when an implement is consumed. A `consumed:false` Applicator returns unchanged with its actual identity, condition, tier/value; a `consumed:true` Applicator remains spent process equipment with zero compound credit. Same names cannot erase their different flags.

Reserve ordinary clean water only for the exact maximum compound deficit after the worst eligible one-unit catalyst return. The current nonzero maximum reserves are **recipe-368: 0.20 lb; recipe-370: 0.40 lb**. All source components still apply. After the outcome and actual catalyst selection, incorporate only the carrier needed for the resolved output before packaging; unused reserved water remains inventory. A generic outcome with no finished output incorporates no supplementary carrier. Water never replaces ingredient tiers/properties/roles or creates another dose. Excess process mass becomes waste without an automatic salvage/market identity.

## Storage, quality and value

An intact sealed finished dose has no ordinary expiry under ordinary storage. Opening starts **one elapsed hour**; resealing/transfer never resets it. Legal injury/contact deployment begun before that deadline commits the dose to its own coating clock. Inhaled release is immediate and destructive. Names grant no extra ingestion route. Partial use cannot manufacture fractional inventory doses or exceed the delivery's exact exposure entitlements.

After injury/contact deployment, a surviving vial is an ordinary spent container: **0.1 lb, AC13, actual current/max structural HP, one-dose capacity, 1-gp reference**. It retains no usable ingredient-tier properties, specialized source value or magical dose. Reuse needs an intact compatible vessel but no repurchase. Inhaled release destroys its container. Broken packaging loses containment and does not automatically perform a combat release or propagate to carried doses.

Use the framework's natural-1 Mishap and numeric six bands; natural 20 grants no independent shift. **Q≥2 Flawed:** floor(Q/2) ordinary doses. **Singleton Flawed:** one dose with unchanged initial damage, DC and delivery; only its ongoing condition limit becomes five future regular target-end markers/30 seconds. Repeat saves remain. A blocked condition gives no refund, replay or second effect. Coating clocks, opened lifetime, action cost, range/area and delivery exposure entitlements are unchanged. Burning then has at most five scheduled fire opportunities; Stunned still needs the same hard-denial allowance.

Exceptional/Masterwork choose floor(1.25Q)/floor(1.5Q) output or **Standard quantity** with improved dedicated output-vial durability. A baseline vial first improves max HP1→2 and current HP+1, preserving its existing damage deficit. Already max-2 improved vials gain nothing again; ordinary repairs remain necessary for missing HP. Broken vessels are not usable packaging before repair. Masterwork's eligible catalyst return stays independent. No quality improvement changes damage dice, DC, condition intensity, action cost, area/range, lifetime, charges or exposure entitlements per dose.

All source prices are **Standard batch references**; unit reference is batch price divided by Standard quantity. Supplemental packaging/carrier costs remain separately recorded. Actual supplier/buyer availability, ordinary quotes, resale and rounding apply. Recipe title/tier does not establish artifact status, unlimited buyers or profitable recycling. Original formula and Director visibility remain intact.

## Scope

This is an authored provisional ruleset, pending exact manuscript approval. It does not certify numerical balance, material access, complete class/spell interactions, runtime/companion parity, human playtesting or whole-game completion. No original source has been deleted. GitHub delivery remains pending; cosmology remains deferred until the authorized push succeeds and its remote commit is verified.
