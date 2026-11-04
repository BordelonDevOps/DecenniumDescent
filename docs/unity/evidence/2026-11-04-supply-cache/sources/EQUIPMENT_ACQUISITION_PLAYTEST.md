# Equipment and acquisition

**REVIEWED authored operational PLAYTEST equipment/acquisition scope.** This guide applies the [equipment conference](../../../../docs/audit/2026-10-08/full-game/GPT_EQUIPMENT_ACQUISITION_CONFERENCE.md), including its twelve conference repairs, the [six exact-review repairs](../../../../docs/audit/2026-10-08/full-game/GPT_EQUIPMENT_EXACT_REVIEW.md), transaction rounding and poison clarification. Use the complete [source tables](EQUIPMENT_SOURCE_BINDINGS.md), [item procedures](EQUIPMENT_ITEM_PROCEDURES.md), [starting packages](EQUIPMENT_STARTING_PACKAGES.md) and [equipment data](../../data/playtest/equipment_acquisition_candidate.json) together. Source tables remain evidence where this guide explicitly replaces or completes a rule.

This covers mundane armor, weapons, tools, focuses, common gear, creation packages, object damage, repair and ordinary acquisition. Full crafting recipes, harvesting, vehicles, mounted combat and artifact/faction economy retain their separate unfinished work. Original books and alternate rules remain preserved. Cosmology is deferred until after a successful authorized GitHub push and verification of its remote commit.

## Record possessions and permissions

Record each physical item's identity, quantity, actual owner/custodian, location, size, equipment grade, condition, remaining contents/charges and any explicit source exception. Ownership grants no proficiency, spell access, recipe, attunement or class feature. Training grants no free item. A price is a baseline quote, not automatic shop stock or a guaranteed buyer.

The source catalog retains unknown fields as null. Its printed price or weight can apply to a bundle, such as twenty arrows, rather than one unit. The operational projection records bundle size and unit values separately. Unarmed strike is an attack option, not an inventory object. Services and living mounts are not generic mundane objects with a weapon's durability.

Use the actual equipped item and current legal class/ancestry/card permissions. A historical feature with the same name supplies no additional grant. Spells and items require their own real targets and actions. A flask cannot be thrown from inside inaccessible melded equipment.

## Armor and shields

Choose one applicable AC formula. Light armor adds the full DEX modifier to its printed base. Medium adds `min(DEX modifier, 2)`, including a negative modifier. Heavy uses its fixed AC without positive or negative DEX. Explicit separate AC bonuses apply only when their own requirements are met.

One usable equipped shield contributes its printed bonus: buckler +1, shield +2, tower shield +3. No second shield bonus. Elven weave's printed Stealth advantage uses ordinary advantage/disadvantage cancellation. Dwarven plate is AC 18; its descriptive superior protection adds nothing. Scale mail's description adds no slashing resistance. Tower shield adds no unprinted cover or additional movement penalty.

**Nonproficient worn armor.** Retain V6 disadvantage on STR/DEX ability checks, saving throws and attacks. Core replaces the older casting prohibition: spells remain permitted, but an RP-priced spell costs +1 RP once per cast and concentration checks/saves have disadvantage. Multiple nonproficient armor pieces never multiply this surcharge. A normal 0-RP spell using the RP price interface can cost 1 RP. Apply this ordinary price addition before the already reviewed eligible reductions and final Resonance Influence step.

**Nonproficient shield — new completion.** While using a shield without shield proficiency, apply the STR/DEX check/save/attack disadvantage. A shield alone adds neither Core's armor RP surcharge nor concentration disadvantage and does not prohibit casting. Core names worn armor for those casting penalties.

A charge-only ancestry spell, Oracle effect or other cast with no RP-price interface acquires no RP price or pool from nonproficient armor. Actual concentration still has disadvantage from nonproficient worn armor. Hands, spell components and other independent casting restrictions remain.

**Strength minimum — new completion.** If one or more equipped armor/shield records have a listed STR minimum you do not meet, reduce Speed by 10 feet total, minimum 0. This is not a minimum to equip; multiple deficient pieces do not stack the reduction. This penalty can coexist with Load/Burden.

The Dwarf's printed rule that Speed is not reduced by wearing heavy armor prevents this penalty when the deficient item is heavy armor. It does not waive Load/Burden, another movement penalty or a tower shield's separate STR minimum. If a table chooses V6's preserved optional encumbrance alternate, that alternate ignores the Armor Table Strength column; the active reviewed Load procedure is not that alternate.

| Equipment | Don | Doff |
|---|---|---|
| Light armor | 1 minute | 1 minute |
| Medium armor | 5 minutes | 1 minute |
| Heavy armor | 10 minutes | 5 minutes |
| Any shield | 1 Action | 1 Action |

One actual assisting creature halves doff time only; a shield still takes at least one Action. Additional helpers do not repeatedly halve it.

## Hands and focuses

A buckler straps to one forearm. Its partially available hand can carry a small nonweapon object, but supplies no free S hand, loading hand, second-weapon attack, two-handed weapon support or active focus manipulation. An ordinary shield or tower shield occupies one hand. Soldier Shield Trained is a specific selected-feature exception for its repeating-crossbow/strapped-shield use, with that feature's actual reload requirements.

A two-handed weapon requires both hands when attacking with it. Releasing one grip costs no Action; regripping is part of its next legal use. This does not free a hand already occupied by another object, restraint or incompatible anatomy.

F requires an actual focus legal for the casting source. A hand holding only that focus may manipulate it and supply S for the same cast; the focus itself is not a conflicting object. A weapon, shield, second object, loading requirement or other hand restriction can make that hand unavailable. An item independently serving as both weapon and focus can use this rule only when an actual source authorizes that item as the caster's focus.

A holy symbol may supply F while held, visibly worn or borne on a shield where that casting source permits holy symbols. A worn or shield-borne symbol does not supply a free S hand. V still requires actual audible speech, and neither a focus nor component pouch waives explicitly priced or consumed materials. The component pouch supplies its ordinary storage function; this guide does not give it a new universal F substitution.

The following focus assignments are **new class integration** for actual legal class spells requiring F. They grant no spells or resource pools. Exact class features may override their own focus rules.

| Casting class | Ordinary focus |
|---|---|
| Bard | One actual instrument |
| Cleric, Paladin | Holy symbol |
| Druid, Shaman, Ranger | Druidic focus |
| Mage, Wizard | Arcane focus |
| Mirrorsage | Steel mirror |
| Oracle | Divination token |
| Crimson Agent, Dragoon, Monk, Thief, Tinker | Token for that class |

Soldier and Warrior gain no spellcasting from focus ownership. An ancestry casting token remains ancestry-grant scoped and cannot substitute for a class focus. An explicitly granted ordinary background arcane focus or holy symbol retains its normal equipment function for a casting source already entitled to that focus category.

## Weapons and ammunition

Use the source table's exact weapon damage, type, properties, cost and weight. Proficiency follows the reviewed [character foundation](CHARACTER_FOUNDATION_TABLES.md), not the source introduction's general statement about most people using simple weapons. A normal proficient attack adds PB once. Normal ability damage follows the attack's actual rules; an item procedure saying no ability damage overrides it for that item.

- **Finesse:** choose STR or DEX for both attack and damage.
- **Thrown:** a thrown melee weapon uses its ordinary melee ability; Finesse can still supply its choice.
- **Heavy:** Small creatures attack with disadvantage. Extending this to Tiny is a new completion.
- **Light:** enables only the actual reviewed Two-Weapon Fighting procedure, not an independent free attack.
- **Reach:** add 5 feet for that weapon's attacks and its actual opportunity-attack reach.
- **Two-handed:** both hands are required for an attack, subject to an explicit feature exception.
- **Versatile:** use the printed alternate damage for an actual two-handed melee attack.
- **Ammunition:** spend one real compatible ammunition unit per attack. Drawing it is part of the attack; non-repeating loading needs an available hand. Using an ammunition weapon in melee is improvised; a sling must be loaded to deal its improvised damage.
- **Loading:** only one ammunition attack per Action, Bonus Action or Reaction, regardless of Extra Attack. This is not one attack per entire turn or round.
- **Range:** the first number is normal range, the second maximum. Beyond normal range gives disadvantage; beyond maximum is illegal. Ordinary close-range ranged-attack rules still apply.

After an encounter, one uninterrupted minute searching accessible locations recovers `floor(eligible ordinary ammunition expended in that encounter / 2)`. Resolve recovery once for that encounter's expended ammunition; another search cannot recover another half. Only physically accessible, intact ordinary ammunition qualifies. Destroyed, consumed, irretrievable or specifically nonrecoverable ammunition does not. Recovered units remain the same physical items and cannot exist in two inventories. Nets and ordinary thrown weapons do not use this half-ammunition rule.

**Ammunition retail units.** A source ammunition bundle remains the ordinary market purchase unit. `unitPriceCp` and `unitWeightLb` are derived inventory/accounting values and do not by themselves guarantee that a merchant sells fractional bundles. If an actual buyer or seller agrees to split a bundle, price the agreed quantity proportionally and apply transaction rounding once to the final transaction. Starting-kit references record one retail bundle and its twenty `grantedUnits`, not twenty bundles.

**Lance.** Attacks against a target within 5 feet have disadvantage. It requires two hands unless mounted; the item supplies no mount or general mounted-combat procedure.

**Net.** A hit restrains a Large-or-smaller creature unless formless; it deals no damage. Its range remains 5/15 feet. The target or a helper within reach can spend an Action on DC 10 STR to free it. Dealing 5 slashing damage to the net against AC 10 destroys it and frees the victim without hurting that victim. When using a net with an Action, Bonus Action or Reaction, make only one attack for that Action/BA/Reaction regardless of normal attack count. Use the reviewed Restrained condition. A missed net remains an actual object at the target location if physically accessible, not an automatically returned weapon.

**Improvised weapon.** Before rolling, the Director may agree that an actual similar object uses an existing weapon's full profile and relevant proficiency. Otherwise it deals 1d4 appropriate physical damage, with no PB absent actual improvised-weapon proficiency. Throwing an object without Thrown, or using a ranged weapon in melee, uses the improvised rule; improvised throwing range is 20/60 feet.

**Silvering.** Silver one weapon or ten ammunition units for 100 gp. This supplies actual silver eligibility only, with no automatic magic tag, attack bonus or damage bonus.

### New class equipment profiles

| Item | Price | Weight | Profile |
|---|---:|---:|---|
| Repeating heavy crossbow | 100 gp | 20 lb | Martial ranged; 1d10 piercing; 80/320 feet; Heavy, Two-handed, Ammunition, Repeating 5 |
| Kama | 2 gp | 2 lb | Simple melee; 1d4 slashing; Light |
| Nunchaku | 2 gp | 2 lb | Simple melee; 1d4 bludgeoning; Light |

**Repeating 5:** an internal magazine holds five bolts, replaces Loading, and spends one bolt per attack. An Action with an appropriate free loading hand loads up to five actually carried bolts. No spare-magazine multiplication, free refill or sixth shot. An exact feature such as Tactical Reload can change the action cost without creating ammunition. The ordinary heavy crossbow remains its separate source profile: 50 gp, 18 lb, 1d10 piercing, 100/400 feet and Loading.

The new **Sidearm** tag applies only to dagger, club, light hammer, handaxe and hand crossbow. Soldier's actual sidearm proficiency can therefore use those profiles; the tag supplies no new statistics or general Martial proficiency. Monk/Shaman staff maps to quarterstaff. Symbolic or relic weapons need an actual existing profile. Kama and nunchaku are not automatically Finesse.

## Equipment grade

An explicit V6 equipment grade changes the item's statistics and mundane baseline price as below. Structural damage does not automatically change grade. Ordinary grade does not create magical eligibility. Only one equipment grade applies.

| Grade | Worn armor | Weapon | Baseline price |
|---|---|---|---:|
| Crude | −1 AC; half normal structural HP, rounded down, minimum 1 | −1 attack; natural-1 break check | ×0.5, new price completion |
| Standard | Printed profile | Printed profile | ×1 |
| Fine | +1 AC | +1 attack | ×3 |
| Superior | +2 AC; 80% ordinary weight | +2 attack; one extra single base weapon die on a critical | ×10 |
| Exceptional | +3 AC; 70% ordinary weight | +3 attack; two extra single base weapon dice on a critical | ×25 |

Armor grade applies to worn suits, not shield AC. A future explicit crafted output may define its own shield improvements. Weapons gain no generic flat damage bonus. On a critical, double the ordinary damage dice, then add the quality dice once; a greatsword's extra quality die is one d6, not its entire 2d6 profile. A Crude weapon's natural-1 attack rolls d100: 5 or less sets structural HP to zero and breaks it. Its material remains recoverable.

Exceptional's source “minor special property” provides no additional effect until an exact property is authored. No free random enchantment is implied. Repair preserves the surviving item's recorded grade unless an exact procedure changes it.

Keep three distinct records:

| Record | What it affects |
|---|---|
| V6 equipment grade | The above combat statistics and mundane baseline price |
| Crafting outcome such as Exceptional or Masterwork | That recipe's actual yield, charges, catalyst or result procedure |
| Core artifact-market Quality | One factor inside the actual artifact valuation formula |

A successful craft does not automatically acquire a V6 grade. A recipe must explicitly specify its resulting equipment grade. Forge Dwarf's retained “exceptional quality” label remains nonnumeric until the crafting integration defines its actual result interaction. Do not multiply all three systems merely because they use similar words.

## Carrying and containers

Use the reviewed [body and equipment guide](BODY_EQUIPMENT_PLAYTEST.md) for actual pounds, Load, size, casualty transport and melded equipment. Keep known physical mass distinct from Load and Extraction Class. Known-weight-only items use pounds divided by ten as provisional Load. Every item's weight and Load count once, including containers and contents. An inclusive gross value covers only the contents it names; it does not erase unrelated quantities or supplies.

**New small-weight completion.** A genuinely small physical source unit lacking weight uses 0.02 lb, except fluid vials, full antitoxin/perfume/basic-poison vials, candles, focus sprigs/totems, holy emblems, sealing wax and soap use 0.1 lb. An ink bottle also uses the small-fluid-container 0.1-lb profile. Narrative background small tokens use the separately stated 0.1-lb accessory profile. Record these as operational estimates, keeping the original source weight null. Larger unweighed items, mounts, vehicles and services do not use this fallback. Do not round away accumulated small items. Coins of every ordinary denomination use fifty coins per pound as a new game-weight convention.

The following **new content capacities** exclude the empty container's own weight. Both weight and volume constraints apply where both are given, along with actual shape, closure and access.

| Container | Maximum contents |
|---|---|
| Backpack or sack | 30 lb and 1 cubic foot |
| Pouch | 6 lb and 0.2 cubic feet |
| Component pouch | 6 lb and 0.2 cubic feet |
| Chest | 300 lb and 12 cubic feet |
| Barrel | 500 lb and 40 gallons |
| Basket | 40 lb and 2 cubic feet |
| Bucket | 3 gallons |
| Glass bottle | 1.5 pints |
| Flask | 1 pint |
| Iron pot | 1 gallon |
| Waterskin | 4 pints |

Water uses 1 lb per pint for this game procedure. A waterskin is 1 lb empty plus up to 4 lb water, matching its source 5 lb full value. Do not add that water to the full value a second time. A printed full potion/vial weight includes contents; separately measured contents replace rather than duplicate its covered gross amount.

The component pouch retains its own source weight of 2 lb and price of 25 gp. Its capacity is mundane storage only, with no universal F substitution, automatic materials, costly-component waiver or spell access.

Preserve the source alchemical capacities: glass or crystal vial one dose; alchemist's bottle three doses; reinforced flask five doses; potion belt six actual vials; potion case twelve actual vials. The belt/case also has its printed empty weight. Extra capacity never creates doses, waives ingestion Actions or makes a multi-dose bottle into multiple physical bottles.

The seven packs expand into exactly their source contents at their source package price, not a forced sum of individual retail prices. They have no extra phantom pack-body weight beyond the named backpack/chest. A pack price does not assert that every item is inside that container or waive its capacity: record legal internal storage, external attachment or another actual custody arrangement. An external rope is still carried weight. Rations provide daily food, not full abstract Supply; Goodberry, Jungle Survival and created water retain their reviewed limited food/water effects.

## Fit and size

Equipment must fit its intended user. Small/Medium and Tiny fitted ordinary items retain the listed price, mass and profile in this candidate; fit creates no unprinted benefit. **New Large sizing:** ordinary armor, shields and weapons use twice the baseline price, twice the weight and twice generic structural HP, with the same AC, damage, reach and properties unless an exact source says otherwise.

A fixed creation package includes the necessary fitting without an added creation charge. Its sized baseline matters for replacement, resale and repair. On the wealth route, buy the fitted item at its actual sized price. Powerful Build changes only its expressly permitted carrying calculations, not item size or weapon damage. It does not resize equipment on transformation; the reviewed body/equipment rules govern that transition.

## Object damage and Sunder

These are **new mundane object procedures** completing the Core Sunder interface. A target must be one actual separately tracked object or explicitly modeled separable component. Naming an armor strap, pin, lace, hinge or seam does not create a cheaper independent target. Construct joints remain subject to the creature's actual stat block.

Sunder uses an actual legal weapon attack against one perceived reachable object/component, consuming one attack when taking the Attack Action. It grants no extra attack or free damage to a wearer. The attacker cannot target a hidden component through a creature or solid obstruction. Against worn/held gear, target AC is the higher of the material AC and wearer's current AC. Unattended gear uses material AC. Ordinary attack eligibility and printed object-target exclusions still apply.

Worn/carried inventory is never damaged merely because its creature is hit. An attack, spell or hazard damages equipment only if its actual rule expressly targets/includes objects, structures, carried gear or that item. Sunder never also damages the wearer unless another source expressly says so.

| Load-bearing material | AC |
|---|---:|
| Cloth, paper, rope | 11 |
| Glass, crystal | 13 |
| Wood, leather | 15 |
| Stone | 17 |
| Iron, steel | 19 |

For a mixed object, establish its dominant load-bearing material before damage. Do not retroactively select a material after the attack roll.

| Mundane object | Maximum structural HP |
|---|---:|
| Tiny vial or letter | 1 |
| Tool, weapon or focus | 5 |
| Ordinary shield | 10 |
| Tower shield | 15 |
| Light armor | 10 |
| Medium armor | 15 |
| Heavy armor | 20 |
| Ordinary chest or door | 20 |
| Cart | 30 |
| Targeted rope segment | 5 |
| Targeted chain segment | 10 |

Large-sized wearable/item generic HP doubles; Crude armor's half-HP rule then applies. Specific source/card durability wins, including a net's AC 10/5 slashing destruction rule and Tinker gnome devices' AC 5/HP 1. The ordinary buckler is a shield using 10 generic HP. Objects outside a listed or genuinely comparable category need an actual assigned profile before targeted durability resolution; no automatic structure or artifact certification is implied.

Objects are immune to poison and psychic damage unless an exact rule says otherwise. Establish physical damage compatibility before rolling: a sword cannot chop a liquid. Do not invent retroactive resistances. Use ordinary attack damage and applicable weapon properties; creature-only conditions and resource triggers do not become object-eligible.

At zero structural HP, the object is **Broken** and loses usable AC, weapon, focus, tool or other functional benefits. It still exists, occupies its hand/slot/container and retains mass until dropped, removed or repaired. Broken armor does not disappear. No negative HP, duplicated loot, automatic explosion, passive regeneration or repair from ordinary rest. Magic items/artifacts need their own durability; no mundane default is assigned to unresolved magical gear. True Polymorph's independently excluded-object rules still apply even when an object has HP.

A Broken item grants none of its positive usable benefits, but remains physically worn, held or strapped until removed. It continues to occupy its hand/slot and contribute weight/Load, and retains physical drawbacks from still wearing or carrying it: applicable don/doff requirements, armor Stealth disadvantage, STR-minimum movement penalty and nonproficiency consequences. A Broken shield grants no AC bonus but still occupies its actual hand/forearm until doffed. A specific source may state otherwise.

## Repair

**Self-repair — new procedure.** Use a relevant trained toolkit and workable materials. Materials cost 25% of the item's current mundane equipment-grade baseline purchase price before temporary market/standing adjustments. Include its actual size. Superior uses Standard price ×10, then 25%; Crude uses ×0.5. An item without an equipment grade uses its ordinary listed baseline.

Spend `max(1 hour, maximum structural HP / 10 hours)` active work and make the appropriate DC 10 tool task check. Success restores structural HP to maximum. Failure consumes the time and materials; another attempt requires fresh payment. No unprinted extra effect arises from a task critical result. Repair at zero HP needs the recoverable main body. It cannot recreate consumed potions, expended ammunition, burnt pages or a missing item. Preserve recorded grade; magical/artifact reconstruction requires its own rule.

**Core dungeon repair service.** Where an appropriate service is actually available, Tier I–III costs 10% and Tier IV–VI costs 15% of the item's applicable undamaged valuation immediately before structural-damage discounting. For an ordinary mundane item, use its legitimate current size and equipment-grade baseline value before damage; for an actual artifact or magic item, use its separately established applicable valuation. Do not apply a damaged-resale discount, buyer-standing sale fraction or transaction-sale penalty to the repair-price base. This percentage is the complete quoted repair service unless that service expressly lists additional costs. Do not automatically add the self-repair material price. The service cannot recreate a consumed item, missing main body, expended ammunition, burnt pages or an unresolved destroyed magical/artifact item. These source service prices do not establish full transport or Tier VI content readiness.

## Purchase and sale

Preserve the source exchange rates: 1 sp = 10 cp, 1 gp = 100 cp, 1 pp = 1,000 cp, and 1 Mithril Mark = 500 cp = 5 gp. Regional Embermark is 2 sp, Soulshard 1 gp and Tidesilver 1 sp where accepted; a Verdant Leaf has no universal GP price. Special soul-linked currency and its origin claims are outside this mundane integration.

An actual available seller/buyer and a legitimate agreed transaction are required. No infinite catalog inventory, guaranteed buyback or universal acceptance. Source trade goods retain their actual units. Ordinary undamaged mundane equipment sells at the following fraction of its actual equipment-grade baseline price, including legitimate item sizing, to that buyer:

| Qualitative standing | Sale fraction |
|---|---:|
| Honored | 75% |
| Liked | 60% |
| Neutral | 50% |
| Disliked | 40% |
| Hated | 25%, or refusal |

Use the actual qualitative relationship to that buyer. This does not choose between the competing historical numeric reputation scales. Damaged equipment needs an explicit quoted valuation; no percentage creates a minimum sale. Gems, jewelry and art can sell at full assessed value only with an actual suitable buyer. Monster-used gear may have no saleable market under the source rule. Trade goods use the source barter context and actual deal; relabeling an assembled kit or quality cannot create a guaranteed arbitrage transaction.

**New rounding:** convert the final transaction price to cp. A purchase price paid by the character rounds up to the nearest cp. Sale proceeds paid to the character round down to the nearest cp, minimum zero. Round only after all applicable modifiers, not at intermediate multiplication steps.

Recipe material/component units retain their own explicit identities and costs until reconciled. A Crafting crystal vial priced at 2 gp is not silently rewritten to the Player catalog's 5 gp retail vial, or vice versa. Existing recipe totals remain intact.

Core's actual artifact formula is `base function value × Gate tier multiplier × market Quality × provenance × demand × legality − actual stabilization, transport, tax and liability costs`. It wins conflicting historical artifact-sale formulas. It is not applied to an ordinary sword simply because recovered in the dungeon. This guide records that boundary without certifying unfinished artifact valuation, factions, tax, wages, demand, commissions or all crafting outputs.

## Evidence and remaining review

The [source evidence](../../../../docs/audit/2026-10-08/full-game/EQUIPMENT_SOURCE_EVIDENCE.json) preserves exact Player lines and Core paragraphs. The [crafting structural audit](../../../../docs/audit/2026-10-08/full-game/CRAFTING_COMPONENT_STRUCTURAL_AUDIT.json) confirms all 687 stored consumed-material value/weight calculations but does not approve their complete effects. The public recipe file exactly matches the intended 433 public source records; the 39 restricted and 215 Director entries remain segregated.

All new procedures above are authored playtest decisions. Oil prices/damage, restraints, inexpensive consumables, equipment grades, large sizing, kit burden and repair economics need human balance/economy testing. Runtime inventory execution and companion parity remain separate. No whole-game completion, final flow approval or GitHub push is implied.
