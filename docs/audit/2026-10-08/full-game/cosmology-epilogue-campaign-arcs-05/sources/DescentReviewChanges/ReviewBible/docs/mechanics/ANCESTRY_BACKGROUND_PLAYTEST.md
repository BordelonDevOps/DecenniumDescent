# Ancestries and backgrounds — playtest integration

**REVIEWED authored operational PLAYTEST integration, within the stated mechanical scope.** The source conference and exact review approved this manuscript after four repairs, now applied. It covers all 14 base ancestries, 45 variants and 20 background packages; it does not certify balance, companion implementation or the entire game. [Exact review](../../../../docs/audit/2026-10-08/full-game/GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW_BROWSER.txt) · [Review status](ANCESTRY_BACKGROUND_REVIEW_STATUS.json).

Read this with [every original mechanical trait and background package](ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md), [character creation](CHARACTER_CREATION_PLAYTEST.md), and [the ancestry spell supplement](ANCESTRY_SPELL_SUPPLEMENT_PLAYTEST.md). The [conference response](../../../../docs/audit/2026-10-08/full-game/GPT_ANCESTRY_BACKGROUND_CONFERENCE_BROWSER.txt) records the decisions. Source records and builder alternatives remain preserved.

Cosmology is deferred until the authorized GitHub push succeeds and its remote commit is verified. This guide does not review origins, gods, plane geography, afterlife identity or the truth of in-world claims. Spore Preservation's reincarnation procedure and Vengeful Tracker's cross-plane direction/distance representation remain explicitly unresolved. Their original promises remain in the source reference.

## Selecting and recording a character

Choose one base ancestry and exactly one of its printed variants. Use the full Player Rulebook mechanical traits, not the abbreviated builder record. Do not add the alternative `racial-variants.json` abilities, percentage modifiers or racial feats. Record one background and all of its actual skill/tool/language selections, possessions, feature and named starting standings.

Apply the base ancestry increases and then its one variant's increases once. **New agreed creation rule:** after these increases, an ordinary creation score cannot exceed 20. Excess is lost; it creates no alternative increase or banked point. Human's base is +1 to all six scores; Feykin's is CHA +2/DEX +1; Mycelian's is WIS +2. Drakari variants add no ASI. Nomadic Human ends with CON +2/WIS +2 and +1 to the other four. Mountain Dwarf has CON +2/STR +2. Use the complete increases table in the source reference.

Ancestry “level” and proficiency bonus use total character level. Class gates still use the actual class level. Ogre is Large; Troll is Medium. Powerful Build affects carrying capacity and push/drag/lift weight only, never size category, space, weapon damage, grappling eligibility or reach. Apply the reviewed body/equipment rules to real Large geometry and fit.

Use the foundation's duplicate-proficiency procedure. A choice remains within its actual list; a fixed ancestry/background skill uses its stated alternative list, or any of the 20 basic skills if none is printed. Tool choices stay within the permitted list/category. If every legal choice is already owned, that grant adds nothing and does not block creation or advancement. No duplicate creates Expertise, another category, a feat, or a future selection. Weapon/armor/save duplicates have no compensation.

An explicit “twice your proficiency bonus instead” trait supplies 2 × PB only for its described task, even if otherwise untrained; never PB plus another 2 × PB. Mere advantage grants no proficiency. Identical resistances do not stack. A natural armor formula is one available AC formula; it is not added to worn armor. Explicit flat AC bonuses remain bonuses subject to ordinary stacking.

The package/wealth decision in the foundation remains controlling: rolled wealth replaces both class and background physical gear and package coins, but not proficiencies, languages, features or standings. Possession grants no proficiency. An Academy spellbook/focus grants no spells; Underworld Escapee's disguise kit grants no disguise proficiency. A journal, signet, map, relic or token has no invented magical effect, price or item statistic beyond its source.

## Recharge, recovery and action clocks

Per-short-rest traits refresh after a completed beneficial short or long rest. Per-long-rest traits refresh only on a beneficial long rest. Retain the shared limits: at most two beneficial short rests between long rests, and one beneficial eight-hour long rest per 24 elapsed hours.

“Per day” remains distinct: a committed use refreshes after 24 elapsed hours. Track two independent timestamps for a twice-per-day grant. Weekly attempts similarly refresh after 168 elapsed hours. Midnight, a new calendar date, encounter entry and a rest do not reset these clocks. Spend limited uses at the source's legal activation/trigger; a failed or countered paid effect is not refunded unless an explicit rule says so.

Four-hour Elf/Umbrin Trance and Undead inactivity substitute for sleep inside the ordinary eight-hour Rest Watch; they do not create a four-hour resource reset. Undead do not eat, breathe or sleep, but their source does not remove drinking, shelter or all camp consumables. Mycelians still require food, water and sleep. No supply exemption is inferred from an ancestry's story.

Use the printed Action, Bonus Action or Reaction. A supernatural trait is not automatically a spell. One action budget, the existing Reaction rules, regular-turn deadlines and the shared limit of one extra full Action per creature per numbered round still apply. A Hide permission still requires a Hide attempt; it does not itself turn the creature invisible. Teleports require the printed visible, unoccupied destination and enough room for the actual body. Only traits that print a dim/dark origin restriction require one.

## Ancestry spellcasting

An ancestry spell is a separate explicit access source. It works for an Oracle, Soldier or Warrior without creating an RP pool, ordinary class spell access, class ranks, prepared spells, Revelation or RC conversion. Record the actual granting trait, spell identity, school/mode, rank, minimum total level, casting ability and recharge. The [grant dataset](../../data/playtest/ancestry_spell_grants_candidate.json) binds 40 fixed grants and two Wizard-cantrip choices to exact source paragraphs; it is reference data, not live companion execution.

The ancestry route casts only the named spell at its granted rank. Cantrips may be repeated. A ranked innate spell spends its stated finite use at legal cast start and has no RP price, strain surcharge, generic upcast or price adjustment from Resonance Influence. It retains the operational spell's action, components, targeting, concentration, interruption and effect rules. Being countered restores neither its use nor displaced concentration.

**New focus rule:** if a granted spell requires F, record one simple nonvaluable ancestry focus/token at creation. It satisfies F only for spells granted by that ancestry/variant unless another rule independently recognizes it. It is not a universal class focus and never substitutes for a priced or consumed material. No ancestry spell waives V/S or other actual casting requirements.

Every genuine innate cast uses the existing character-wide Dissonance and same-name Refrain history. For this cast, Limit = max(4, 2 + total PB + max(0, its printed casting modifier)). Rank 0 adds base Dissonance 0; ranks 1–5 add 1; ranks 6–9 add 2; ordinary Refrain applies. Ranked innate casting is blocked at Limit + 6 despite having no RP price. Cantrips remain available under their ordinary strain rules. Class hooks apply only when their real ownership and trigger permit them.

A character without an RP interface clears Dissonance, but not Refrain, after a beneficial short rest; long rest clears both. It receives no RP. A mixed character uses the same shared strain state and its existing recovery procedure.

The agreed ancestry-only school provenance is Dancing Lights/Evocation, Detect Magic/Divination, Feather Fall/Illusion and Charm Person/Enchantment. This does not rewrite their other school placements. Other named grants use their recorded single school or the explicitly authored supplement. High Elf and Lichborn each choose one actual catalog identity with Wizard rank 0, use its Wizard school and INT, and retain that choice. Choose an operational identity for the current executable playtest; unfinished options remain recorded for later completion. A shared name never grants the same-named class card.

Obsidian Highborn changes the separate Umbrin Faerie Fire and Darkness entitlements to two uses each per rolling 24 hours; it does not bypass their level gates. Cavern Mystic has separate once-per-long-rest Detect Magic and Speak with Plants grants, with earth/stone and fungi restrictions respectively and no invented level gate. Feykin's core Charm Person/Misty Step refresh by long rest; the variant's printed per-day grant keeps its different clock.

## Trait procedures and source-specific exceptions

All source paragraphs in the companion reference remain operative in their printed scope except where this section explicitly supplies an agreed clarification or replacement. A retained quality label or lore domain does not invent a numerical benefit or establish world truth.

### Amphibian, Umbrin and Drakari

Moisture Dependency uses a recurring 24-hour survival checkpoint selected at creation. Missing the required hour of immersion adds one Exhaustion level for that interval. One continuous hour of immersion satisfies the interval and unlocks ordinary removal of the trait's accumulated Exhaustion; immersion alone does not remove it. Never count the same elapsed interval twice.

During one ordinary Forage activity in forest/jungle, Jungle Survival requires no check for its printed food/water guarantee. Record the Amphibian and up to five other recipients as supplied with ordinary food and water through the next daily consumption checkpoint. This creates no physical Supply Units, fuel, shelter, medicine, ammunition or other camp consumables. Numerical reduction of the bundled Supply bill remains an explicit expedition-resource dependency; do not silently award six Supply Units.

Water Sense gives presence and fresh/salt distinction within its printed 60 feet, not a pinpoint map. Cavern Mystic Stone Sense gives presence of unusual stonework within 60 feet and approximate depth, not trap instructions or a floor plan. Do not impose generic line of sight on these specific buried-substance senses. Ordinary attacks, sight checks and concealment continue to use their actual rules.

Keep Umbrin Sunlight Sensitivity exactly as printed. Shadow Blade Shadow Step requires a dim/dark destination, while Twilight Elf Shadow Step requires both origin and destination to be dim/dark. Their different range, recharge and attack riders remain separate.

Drakari Breath Weapon uses one shared damage roll; every creature in its variant's printed cone/line saves independently, failure full and success half. There is no selective ally omission. Use CON DC, total-level scaling and one SR/LR entitlement. Gale Wind Step ignores difficult-terrain movement cost when it Dashes as printed, including magical difficult terrain; the builder's nonmagical-only limit is not adopted. Stone Drakari's +1 AC applies only while unarmored. Climate adaptation grants only its actual environmental benefit, not immunity to damage or suffocation.

### Dwarf, Elf and Feykin

Forge Dwarf Master Craftsman reduces actual artisan-tool creation time by 25%. “Exceptional quality” is retained as a quality label without an invented price/stat bonus; its wider crafting effect remains open. Stonecunning and other specific double-PB checks follow the task-scoped proficiency rule above. Deep Dwarf's 120-foot darkvision replaces, rather than adds to, 60 feet.

Fey Ancestry prevents magic from putting the creature to sleep. It does not grant immunity to every Unconscious effect. Twilight Fey Veil Sight requires actual line of sight within 10 feet; it does not reveal through a wall.

Summer Green Thumb is an Action touching one actual nonmagical plant that initially fits a 5-foot cube. Increase its linear dimensions up to twice normal for 24 hours, ending earlier if the trait is used again. Growth stops at the largest legal size if solid terrain, an occupied creature space or another immovable obstruction prevents it. It never pushes, restrains, crushes, damages or passes through barriers. It creates no additional nutritional value, harvest, duplicated crafting material or magic plant. These scale, action and collision details are new agreed procedures.

Vitality of Summer lets you reroll each healing die that you personally roll as a 1 once, keeping the new result. It does not affect another player's dice, flat healing or temporary HP, and cannot reroll the new 1 indefinitely.

Winter Frost Touch retains Action, touch, one object no larger than a 1-foot cube, one SR/LR use and ice lasting one hour or until fire. An unattended, self-held or willingly presented object needs no attack. To touch a hostile worn/carried object, make the agreed ancestry melee attack d20 + PB + STR against the carrier's AC. It deals no damage and adds no disarm, breakage, Slowed or frozen-creature effect.

### Gnome and Goblin

Tinker Gnome retains one hour and 10 gp of actual materials per Tiny device, AC 5, HP 1, a 24-hour operating deadline and at most three active devices. Its four source profiles remain equipment objects, not creatures, attacks or spell substitutes. Reclaim actual materials once at expiry/dismantling; they cannot produce money or duplicate material. Destroyed equipment leaves only actually recoverable remnants.

One hour maintaining a still-existing device renews its deadline from repair completion and restores its device HP to 1 without another 10 gp cost. This does not reconstruct a destroyed device. The toy moves five feet in a random legal ground direction at each regular owner turn. The sensor chirps audibly within ten feet on a creature crossing its 30-foot boundary, including invisible creatures; initialize present occupants without a chirp. It gives presence, not count, identity or location. No wall-blocking restriction is invented for this source. Multiple chirps grant no actions or interruptions. Opening/closing the music box uses an ordinary object interaction; select its song when constructed.

Arcanist Gnome Arcane Tinkering chooses one of the printed damage types when committing one genuine damaging spell. One SR/LR use changes that cast's direct damage, including later ticks, but not summoned-creature attacks, child spells, unrelated riders or class techniques. Rank, non-damage riders, tags and healing formulas are unchanged. Gnome Cunning requires an actually magical generating effect; a theme alone is insufficient.

Fury of the Small triggers after an actual attack/spell result establishes a positive raw damage packet against one larger creature, before its defenses. Choose one damage type already in that packet, spend Fury, and add total character level to that type. If defenses later reduce damage to zero, the use stays spent. It affects one packet, not every ray, target, tick or transferred recipient.

Boom Goblin creates and throws its explosive in the same Action; it is immediately expended and cannot be stockpiled, sold or retained as ammunition. No material fee is invented. Each creature in its printed area makes the source DEX save: success takes zero damage. Scavenger's Luck adds one d4 to each qualifying check before consequences, without an invented per-day cap.

Scrap Goblin uses actual suitable available materials to create one listed functional item; its HP is half ordinary item HP, minimum 1. Using the trait again ends the previous item. A healing kit requires actual medicinal consumables sufficient for its normal finite uses; reusing exhausted scraps cannot restore them. It grants no proficiency, magic item or arbitrary free consumable. Other simple tools require the printed Director agreement. Missing equipment profiles remain visible dependencies.

Shadow Blend activates in dim light or darkness, using its Action/use. Its own activation does not end it. Subsequent actual positional movement, including forced movement and teleportation, an Action or a Reaction ends it. A Bonus Action that does none of these does **not** by itself end it. There is no invented continuing dim-light requirement after activation. This corrects the proposal's overbroad Bonus Action ending.

### Human and Mycelian

Imperial Natural Leader is a new agreed Reaction to your or an ally's actual used natural-1 d20 result on an attack/check/save within 30 feet, before consequences. The ally must hear your call. Reroll once and keep the new result, spending one SR use. A discarded advantage/disadvantage die never triggers it. It creates no second attack/cast and cannot revise applied consequences. Scholarly Lore Master requires an actual studied subject, not automatic correct lore.

Spore Cloud includes its caster because it affects each creature in its area. Hallucinogenic Cloud replaces the Blindness consequence with the source Perception disadvantage; it does not add both. Bioluminescent Spores starts with the new agreed Action and ends with the printed Bonus Action, retaining bright 10 feet plus dim 10 more and no invented use cap.

Spore Preservation's sample and special container remain source features. **Its success conditions and reincarnation/identity procedure remain unresolved until after the verified push.** Do not advertise automatic resurrection, consume/duplicate a character identity or invent a cultivation recipe now.

Decomposition Touch retains its printed body/material size, one-minute corpse process and recharge. It cannot decompose living plant creatures, magic items or hostile worn/carried equipment. Actual corpse destruction may affect later source-specific resurrection eligibility. Consume Decay retains its source adjacency, temporary HP and one-hour duration; it does not expressly destroy the material or grant infection immunity. Decay Sense gives presence and general age within 30 feet, not pinpoint anatomy or identity.

Symbiotic Bond is an Action touching a distinct willing creature, lasts one minute, can end by Bonus Action and uses one LR entitlement. The other participant must remain a valid continuing creature for a damage event. When either participant takes damage, the Symbiotic Mycelian who owns this trait may use its Reaction to transfer a chosen positive amount up to floor(post-defense damage / 2) to the other participant before temporary HP. The bonded creature gains no independent Reaction permission from the bond.

Use [damage sharing](DAMAGE_SHARING_PLAYTEST.md): one transfer operation per original recipient's packet across all owners; retain type, skip a second mitigation/prevention stage; apply tempHP, HP floors, Wounds, concentration and life consequences to each final share. No recursive transfer, duplicate parent counting or transferred hit/rider identity. No extra range or same-plane restriction is added to the transfer. The printed same-plane restriction applies to Empathic Link's information only, unless another exact active rule restricts the damage operation.

Healing Spores uses its printed Action/touch, 1d8 + WIS, once LR, under ordinary healing modifiers, prohibitions and caps.

### Ogre and Orc

Ogre Natural Armor is the base AC formula 12 + CON. Mountain Ogre Stone's Endurance reduces the eligible packet by min(available damage, max(0, 1d12 + CON)) at the finite Reaction-prevention stage, before transfer/tempHP; it is not healing. Mighty Thrower adds 30 feet to both normal and long range of an independently legal thrown weapon/object attack. It grants no permission to throw a creature or building. Long-Limbed adds reach only to melee attacks on the Ogre's own turn, not out-of-turn Opportunity Attacks.

War Ogre Battle Cry gives the printed temporary HP to allies who hear it within range; self is not its own ally. Use the ordinary temporary-HP lifetime and nonstacking ledger. Stone Troll's flat +1 AC remains compatible with an otherwise legal worn-armor formula; it is not a second base formula.

Orc Aggressive spends a Bonus Action for actual movement up to Speed toward an enemy it can see/hear and must end closer. Terrain, legal movement and Opportunity Attacks still apply. It is not an extra Action or teleport. War Orc Savage Attacks adds one weapon damage die to a melee weapon critical as printed; it does not double that bonus again.

War Orc Relentless Endurance is a true positive-to-zero HP floor after the Core Instant Death check. Spend its one LR use to remain at 1. It is not healing, cannot raise an already-zero creature and cannot operate after actual death. Preventing that drop removes its drop-only Wound/zero-HP branch, while independent half-maximum/Maiming triggers still follow the shared life procedure.

Shaman Orc Healer's Intuition requires an Action that actually succeeds at stabilizing a dying living creature, then gives 1 HP direct-state recovery, subject to broad HP-gain prohibition. It does not auto-pass Medicine or turn any healing into stabilization. Already Stable, positive-HP or dead targets cannot generate the trigger. No per-rest limit is invented. This is an explicit source exception to the generic repeated-healing resource rule, not a resource conversion. Battlefield Medic instead requires an actually spent healer-kit charge and successful stabilization.

### Troll and Undead

Troll Regeneration is an explicit ancestry exception to the generic finite class-healing rule. At each regular turn start while HP is at least 1, restore PB; Blood Troll adds CON, minimum total 0. Positive acid/fire damage suppresses the next regular-start regeneration event. Outside initiative, pulse every six elapsed seconds and suppress the next pulse after acid/fire damage. Entering/leaving initiative produces no bonus pulse. It never heals from zero or removes Wounds; broad HP-gain/passive-regeneration prohibitions still apply.

Regeneration can have at most one pending acid/fire suppression. Any number of qualifying positive acid/fire packets before the next scheduled regeneration pulse still suppress only that next pulse. When that pulse is reached, consume the pending suppression and restore no HP from Regeneration. A later qualifying packet after that pulse can establish suppression for the following pulse. This applies identically to regular-start and six-second outside-initiative pulses.

Regeneration is ordinary HP restoration for current-HP state and predicates that merely ask whether HP was regained. It cannot by itself generate resources, excess-healing conversion, copied/secondary healing or repeatable proc chains unless an exact source expressly authorizes passive regeneration for that trigger. This restriction prevents resource loops; it does not certify the ancestry's balance.

Blood Troll Vitality Transfer explicitly replaces its original self-damage wording with the agreed shared sacrifice procedure. As an Action, touch a distinct willing legal creature, pay total character level in actual normal HP while remaining at least 1 HP, and attempt to heal that recipient for twice the amount paid under the ordinary healing rules. If the recipient cannot legally receive ordinary healing, the healing can be blocked while the use/payment remains spent. The ancestry feature adds no living-target prerequisite. TempHP cannot pay; loss is unpreventable, nonredirectable and not damage, and creates no damage/Wound/resource trigger. Spend its LR use even if recipient healing is blocked or capped; no refund. Preserve the original source paragraph for comparison.

An active Undead PC is alive as a life-state character while having both Humanoid and Undead creature types. An effect requiring either type may apply; an explicit exclusion of either type excludes it. The ancestry adds no unprinted monster immunities and does not make an active PC a corpse. Actual death is a separate state.

Deathless Fortitude is a positive-to-zero floor after Core Instant Death, using CON DC 5 + resolvedDamage before tempHP. It is unavailable for radiant damage or a critical hit. Spend its LR use when attempting the save, whether it succeeds or fails; no Reaction is required. It does not raise already-zero HP or replace death. Retain independent Wound triggers as in the shared life procedure.

Lichborn Soul Drain is Action/touch, CON save against 8 + PB + INT; failure deals its total-level-scaled necrotic dice + INT, success no damage/tempHP. Gain nonstacking tempHP equal to max(0, actualDamageDealt), counting eligible terminal recipient damage once, not overkill or the unsplit parent. One SR/LR use. Arcane Recovery, once per rolling 24 hours after a beneficial short rest, recovers ceil(total level / 2) RP capped at the actual merged maximum. It creates no RP pool for a character with maximum zero and no extra Dissonance reset beyond the rest.

Revenant Relentless Nature triggers only after a true reduction to zero. Attempt CON DC 10, spending its LR use; after that packet's death/Wound resolution, if the Revenant is still alive and the save succeeded, it receives the one immediate Action despite the resulting zero-HP action restriction. No movement, Bonus Action, Reaction, extra turn or extra death save. The shared extra-full-Action cap, actual source costs/components and independent incapacitation still apply. A floor that prevented zero means no trigger; actual death prevents the Action.

Vengeful Tracker retains its one-hour ritual, one designated target and replacement ritual. Same-plane general direction/distance is usable now. **The source's cross-plane awareness sentence remains preserved, but its cross-plane representation is deferred until the post-push cosmology review.** Do not invent planar coordinates or delete that permission.

Wraith Incorporeal Movement starts at the beginning of its own movement without an Action, spending one of PB rounds; that window lasts through the next regular turn start. More entries within the same window cost no extra round. It grants difficult-terrain movement through creatures/objects, not flight, vision through stone, attacks through walls or plane travel. Ending a turn inside an object deals the printed 1d10 force. At expiry inside an object, use [the reviewed mandatory placement procedure](BODY_EQUIPMENT_PLAYTEST.md): nearest legal adjacent fit in the same unobstructed region, legal squeeze first, no wall/occupied-space traversal or tactical player choice. If none fits, retain a placement conflict until a legal solution exists; no farther teleport or invented extra damage.

Chilling Touch changes a hit's normal unarmed damage to 1d4 + DEX cold. It does not grant DEX to the attack roll; that roll uses the ability the actual unarmed-strike rules permit.

## Background procedures

The full reference supplies each exact skill, tool, language, equipment package and starting standing. These source rows are authoritative over builder abbreviations. Keep Deep Cant where printed. Keep exact source feature names, including Lingering Influence, Whispers of the Past, Trailblazer, Planar Connections, Otherworldly Perspective, Relic Lore, Frontier Adaptability and Elemental Affinity.

| Background | Operational feature and limits |
|---|---|
| Aethel City Guard Veteran | Watchman's Eye gives the source city-trouble Perception advantage and navigation/location-check advantage specifically within Aethel. |
| Rift Scarred Survivor | Planar Sense gives Charmed/Frightened save advantage only from an actual listed creature type. It is not generic planar detection. |
| Disgraced Noble Scion | Lingering Influence permits one connection attempt per 168 elapsed hours for the printed audience/information/lodging purpose. It may fail or attract unwanted attention; no automatic audience or command. |
| Wildling Herbalist | Natural Remedy identifies plants as printed. During a beneficial LR with actual suitable local components, create one basic Potion of Healing OR antitoxin without gold. Record consumed components and the product. No automatic component availability, invented expiry/one-active cap or sale price. Actual products may accumulate. Complete item profiles remain an equipment dependency. |
| Guild Artisan Dropout | Insight/Persuasion and one language are retained. Trade Secret applies to actual own-trade quality, fakes, value and contacts/processes, not automatic magic identification or universal market knowledge. |
| Seeker of the Lost Pantheon | Whispers of the Past retains its specific INT knowledge advantage. Its subject scope does not establish cosmological or religious truth. |
| Marked Fugitive | Echo of the Stolen uses the detailed witness-and-access procedure below. |
| Expedition Cartographer | Trailblazer recalls actual seen/studied routes and layouts. Safest-route advice uses known terrain and visible or otherwise actually known hazards, not an omniscient guarantee. |
| Arcane Academy Dropout | Theoretical Knowledge retains its Arcana advantage domains. The physical spellbook/focus grants no spell access. |
| Cult Escapee | Dark Insights recognizes actual cult practices/signs and retains Religion advantage. Preserve all three standing relationships, including Disliked religious authorities. |
| Planar Merchant | Planar Connections allows one printed attempt per 168 elapsed hours, with actual appropriate cost and Director approval. It invents no planar market, route, stock or automatic purchase. |
| Battlefield Medic | Trauma Response requires an actual healer-kit charge and successful stabilization, then grants 1 HP direct-state recovery. No dead revival, Wound cure or HP-prohibition bypass. Identify injury nature/severity as printed. |
| Dimensional Refugee | History (original world) is a scoped proficiency: add PB only on History checks materially about that world. It is not general History or Expertise; separately gaining general History never doubles PB. Otherworldly Perspective retains its exact INT advantage without inventing facts. |
| Relic Hunter | Relic Lore requires a successful History check for approximate age, culture and significance. Contacts depend on the fiction; no automatic magical appraisal. |
| Corruption Survivor | Corruption Sense detects presence of strong sources within 60 feet without pinpointing. Retain disease-save advantage and the narrower advantage against undead/fiend corrupting effects, not universal corruption immunity. |
| Frontier Settler | Frontier Adaptability uses actual materials and real crafting, forage and shelter procedures. It does not conjure supplies or restore spent tool charges. |
| Prophecy Bearer | Establish Fated Path's direct relevance with the Director before spending its LR use and rolling. Gain advantage on one eligible attack/check/save. No forced world event or refund after failure. |
| Underworld Escapee | Criminal Network recognizes actual operations/signs and accesses existing contacts under ordinary circumstances, not automatic obedience. Kit possession does not grant proficiency. |
| Elemental Touched | Select one affinity at creation: fire/fire resistance, water/cold, air/lightning or earth/acid. Basic communication with corresponding elementals is not control. No rest-based reselection or spell pool. |
| Celestial Emissary | Divine Insight is a new agreed one-minute uninterrupted trance, one LR use spent at start, for one focused question. The Director gives truthful cryptic guidance relative to established campaign facts or honest uncertainty; it does not force disclosure/retcon of cosmology. Its reliquary emits dim light within five feet in darkness only, its sole mechanical blessing pending equipment review. |

### Echo of the Stolen

You must actually have witnessed the rank-1 spell cast with line of sight within the previous 60 minutes. For the ordinary held-class route, the same spell must have a rank-1 ordinary access entry for at least one Base class you possess. Echo itself supplies the temporary cast; ordinary known/prepared membership is not additionally required. It uses CHA and retains the witnessed actual rank/mode, activation, components, targets and concentration. Spend the one LR use at cast start with no refund. Use the innate charge-only strain interface. The source brand glows faintly afterward; this is not automatic remote tracking or an alert to every pursuer.

The Oracle Mystery route requires a separate explicit table from actual Mystery IDs to permitted ordinary rank-1 spell IDs. Only exact spells expressly named by reviewed Mystery/Revelation text, or a later owner-approved mapping, may enter it; thematic resemblance is insufficient. Until that table is reviewed, this branch is pending/ineligible. Possessing Oracle alongside another Base class does not prevent an independently legal held-class route. No RC-to-spell conversion or general Oracle Weave access is created.

### Standing and survival resources

Record Hated/Disliked/Neutral/Liked/Honored as exact qualitative labels tied to each printed named group. A specific former cult/guild/faction is not every cult/guild/faction. The code's numeric thresholds and prose endpoints require the later reputation reconciliation; do not silently invent faction IDs or normalize scores now. Standing has no automatic spell-price, RP, rank or moral-alignment effect.

Jungle Survival, Goodberry, created water, Undead food exemptions and similar effects fulfill only their actual food/water requirement. The current Supply Unit bundles food, water, fuel and camp consumables, with different Large-creature demand. Record actual supplied recipients/amounts separately until the expedition-resource pass resolves the numerical bill; never count one resource twice or claim it supplies omitted components.

## Remaining dependencies

Two branches are deliberately post-push: Spore Preservation's reincarnation procedure and Vengeful Tracker's cross-plane representation. Other unfinished work includes the Marked Fugitive Oracle mapping; potion/antitoxin/healer-kit and other equipment profiles; numerical food/water versus Supply accounting; crafting quality/procedures; standing-to-faction/score migration; remaining selectable Wizard-cantrip effects; companion parity; and human balance. None of these is silently closed by source coverage or manuscript agreement.
