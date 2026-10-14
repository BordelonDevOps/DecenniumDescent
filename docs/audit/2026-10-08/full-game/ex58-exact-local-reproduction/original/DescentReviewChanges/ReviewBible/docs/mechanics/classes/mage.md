# Mage — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/mage.json) · [Normalized card data](../../../data/public/class_playtests/mage.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Intelligence
- Secondary Attributes: Wisdom, Dexterity
- Hit Points: Low (6 + Constitution modifier at 1st level, 1d6 per level thereafter)
- Armor Proficiency: None (cloth only)
- Weapon Proficiency: Wands, staves, spell foci
- Tool Proficiency: Arcana tools, scribe's supplies

PROVISIONAL PLAYTEST CONTRACT. Intelligence is the Mage class ability. S = 1/2/3/4 at Mage levels 1/5/11/17. M = max(1, Intelligence modifier) unless a feature explicitly says otherwise. Mage spell attack = d20 + normal character proficiency bonus + Intelligence modifier. Mage spell save DC = 8 + normal character proficiency bonus + Intelligence modifier.

Spellcasting and Resonance Pool are automatic class features, never selection taxes. Use the Mage maximum Resonance Point pool and ordinary spell-rank costs from authoritative Core Systems Known Descent V 2. All Mage card RP costs and ordinary spell RP costs come from that same pool. There are no spell slots. A long rest restores RP according to Core V 2; other existing recovery rules remain separate unless this pilot explicitly overrides them.

Named Mage cards tagged mage-spell, and the three Focus finishers are spells for Focus, Nuke Chain, Refrain, concentration, Counterspell and other spell-referencing mechanics. Their printed RP cost replaces an ordinary rank cost; do not charge both. Generic Overcast is disabled for these class-card spells during this pilot unless a card expressly enables it. They receive no extra class-level Burn or Dissonance simply for being card spells; ordinary Core V 2 spell-risk rules still apply where applicable.

Elemental Focus is gained automatically at Mage level 2. Choose Fire, Cold or Lightning and automatically gain the corresponding Focus card. Your selected Focus determines the element used by Elemental Bolt, Elemental Surge, your Focus finisher and other effects that refer to your chosen element. Unless Elemental Pivot or another explicit effect changes it, the choice is permanent in this draft.

NUKE CHAIN. Track your last three consecutive Focus-eligible spell casts. A Focus-eligible cast is a Mage or ordinary spell that deals your currently chosen Fire, Cold or Lightning damage type and is identified by a distinct spell or card name. A spell of another element or a non-elemental spell clears the chain. The last three eligible casts must have three different names. Repeating one chosen-element spell remains a legal cast but shifts the three-cast window and follows ordinary Refrain rules; repetition does not receive special protection from Dissonance.

When the third different named chosen-element spell in the current three-cast window resolves, complete the Nuke Chain, reduce Dissonance by 2 to a minimum of 0, and prime your selected Focus finisher until the end of your next regular Mage turn. Chain completion occurs whether targets hit or save, provided all three spells were legally cast and resolved. A finisher is not itself a chain-building spell. Using the finisher or allowing it to expire clears the chain and the primed state.

FOCUS FINISHERS. A primed Focus finisher is a Bonus Action Mage spell costing 2 RP and is usable once per completed Nuke Chain. Each finisher also has a 3-round recharge. A completed chain can prime a finisher whose recharge is still positive, but the primed use expires normally if the recharge does not become ready in time. Finisher recharge is subject to the universal positive-counter reset limit of once per ability per round.

RESONANCE SURGE. Once per short rest, when you begin casting a damaging Mage spell, you may spend 2 additional RP after validating the spell's normal cost. Add S d8 damage of one damage type already dealt by that spell to one of its damage rolls. Resonance Surge does not count as Overcast, does not independently alter Dissonance or Burn, does not create another spell cast, and does not advance the Nuke Chain separately.

Only one concentration effect may be maintained at a time. Starting another concentration effect ends the first. Damage prompts the current Core Systems concentration save; for this pilot any required half-damage rounding is down. Round recharge counters tick once at the start of your regular initiative turn even if incapacitated, and every uninterrupted 6 seconds outside initiative. Only positive counters may be shortened or reset and each named ability can receive at most one reset or shortening per round.

All sources share a maximum of one additional full Action per creature per round. Additional Actions cannot grant additional Actions, Bonus Actions or Reactions. Mage summons and companions do not receive independent damaging turns: all Mage-controlled conjured companions share one Companion Command per Mage regular turn. Spend one Bonus Action to command exactly one companion to move up to its Speed and use one damaging or control action from its stat block. Uncommanded companions may move to remain near you and take Dodge but cannot deal damage or impose control.

ELEMENTAL FAMILIAR. Conjure Elemental Familiar creates one familiar matching your current Focus; you may have only one elemental familiar. AC = 12 + PB; HP = 5 + Mage level + M; Speed 30 feet; Lightning familiar additionally has Fly 30 feet, Fire has resistance to fire, Cold has resistance to cold. It uses your saves and PB where required. Elemental Dart: ranged spell attack using your Mage spell attack, range 30 feet, hit S d4 damage of its element. It cannot generate RP, Dissonance, Focus casts, corpses, XP, loot or kill-trigger resources.

LICH COMPANION SYSTEM. A successful Lich transformation unlocks three unique bound elite companions: Boneflayer, Dreadblade and Wraithbound. You can maintain at most one of each, maximum three total. They return at full HP after a completed long rest unless a campaign consequence expressly prevents it. A destroyed elite leaves no usable corpse and cannot generate XP, loot, RP, Nuke Chain credit, Soul Reservoir or kill-based resources. Soulbound Ritual can return one before a long rest.

BONEFLAYER. Medium undead; AC 14; HP = 12 + 2 × Mage level; Speed 30 feet. Bone Shards: range 60 feet, your Mage spell attack, hit 2d6 + S necrotic. Fear Pulse: instead of Bone Shards, enemies of your choice within 10 feet make Wisdom saves against your Mage DC; failure causes Frightened until the end of their next turn; recharge 3 rounds. Grave Miasma: instead of Bone Shards, one 10-foot-radius point within 30 feet persists until the start of your next turn; enemies entering or starting there take 1d6 necrotic once; recharge 3 rounds.

DREADBLADE. Medium undead; AC 16; HP = 16 + 3 × Mage level; Speed 30 feet. Disrupting Blade: melee spell attack using your Mage attack bonus, reach 5 feet, hit 1d8 + S necrotic. If the target is concentrating it immediately makes its concentration save with disadvantage. On a natural 20, the target is Weakened until the end of its next turn, taking -1 to attack rolls. Dreadblade has advantage on saves against forced movement.

WRAITHBOUND. Medium undead; AC 14; HP = 10 + 2 × Mage level; Fly 40 feet and can hover. While it has not attacked or imposed control since the end of its previous turn, it is Invisible; attacking ends that state until the end of its next turn. Wraith Strike: melee spell attack using your Mage attack bonus, reach 5 feet, hit 1d8 + S necrotic. On a natural 20, the target makes a Constitution save against your Mage DC; failure Stuns it until the end of its next turn.

LICH TRANSFORMATION READINESS. At Mage level 10 a character may select Lich only after obtaining either one Soul Coin or two ritual participants, binding at least two named mini-bosses as guardians, securing a planar nexus and surviving the Director's divine-echo encounter. A third bound guardian grants +2 to the final ritual check. If both ritual participants are willing, the final ritual check has advantage.

Before the irreversible Lich roll, the Director must explicitly tell the player the historical failure stakes: permanent loss of spellcasting, transformation into a cursed melee undead NPC, hostile faction consequences, cursed-gear restriction and no further XP as that retired PC. The player must explicitly opt into that retirement risk before rolling. If the player declines, the ritual stops before the roll and the character must choose another Hero path for this playtest; no irreversible consequence is applied.

LICH RITUAL CHECK. After all readiness gates and the divine-echo encounter are completed, roll d20 + Intelligence modifier + Constitution modifier against DC 20, applying the third-guardian +2 and willing-participant advantage where applicable. Success completes the Lich transformation and unlocks its cards and elite companions. Failure after explicit consent applies the historical failure state and the Director pauses for the agreed player-to-NPC handoff before continuing play. No silent PC deletion is permitted.

PROPOSED ACQUISITION. Mage 1 automatically gains Spellcasting, Resonance Pool and Resonance Surge, then chooses 4 eligible selectable Base cards, at least 2 Active. Mage 2 automatically chooses and gains one Elemental Focus card, then chooses 2 additional Base cards. Mage 3 enters Arcanist and chooses 2 Arch cards, at least 1 Active. Levels 4 through 9 each grant one eligible unselected Base or Arch card; level 9 is an ordinary choice because the historical source has no Arch capstone.

At Mage 10 choose Archmage, Elementalist or, if its ritual succeeds, Lich; choose 2 cards from that Hero path. Levels 11, 13, 15, 17 and 19 each grant one eligible unselected Base or Arch choice. Levels 12, 14, 16 and 18 each grant one Hero-path choice. Mage 20 grants one additional Hero-path choice plus the NEW playtest level-20 class capstone in extra Cards. No historical Hero Finale is implied. ASI/feat milestones remain separate.

All acquisition gates use Mage class level, not total character level. Proficiency bonus remains the normal total-character proficiency bonus. Non-Mage levels do not unlock Elemental Focus, Arcanist, Hero cards, Nuke Chain upgrades, Lich ritual access or the level-20 Mage capstone.

Class-spell ranks are printed in the normalized card data: use the legal maximum Mage rank at that card's minimum class level, capped 9; the three Focus finishers are rank 1. Rank determines Dissonance, Counterspell and rank-limited interactions, not a second RP cost. A shared spell uses the ally's normal Action and caster-side Dissonance at the moment it is cast; it never builds the Mage's Nuke Chain remotely. Spellcasting through Fracture as Lich uses the shared direct-trauma rule.

**Protected source interface:** A Nuke Chain requires different named spells of the chosen element; completing a three-spell chain vents 2 Dissonance. Repeating one nuke builds Refrain normally.

## Advancement and resources

RP authority: Direct Core Systems V2 table. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 3 | 1 | Choose 4 Base; at least 2 active; automatic: Spellcasting, Resonance Pool |
| 2 | Base | 5 | 1 | Choose 2 Base; automatic: Fire (Fire), Cold (Cold), Lightning (Lightning) |
| 3 | Arch | 8 | 2 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 10 | 2 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 14 | 3 | Choose 1 Base/Arch |
| 6 | Arch | 17 | 3 | Choose 1 Base/Arch |
| 7 | Arch | 20 | 4 | Choose 1 Base/Arch |
| 8 | Arch | 23 | 4 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 26 | 5 | Choose 1 Base/Arch |
| 10 | Hero | 29 | 5 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 32 | 6 | Choose 1 Base/Arch |
| 12 | Hero | 35 | 6 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 38 | 7 | Choose 1 Base/Arch |
| 14 | Hero | 41 | 7 | Choose 1 Hero |
| 15 | Hero | 44 | 8 | Choose 1 Base/Arch |
| 16 | Hero | 47 | 8 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 50 | 9 | Choose 1 Base/Arch |
| 18 | Hero | 53 | 9 | Choose 1 Hero |
| 19 | Hero | 56 | 9 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 60 | 9 | Choose 1 Hero; automatic: Resonance Apex — NEW Playtest Capstone |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Mage 5 Fire example: Intelligence 16 gives M=3, PB=3 and S=2. For arithmetic illustration, assume the current Core V 2 character sheet gives this Mage 14 RP. Dissonance begins at 4, Fire Focus is selected, the Nuke Chain is empty and all targets are legal.
2. Turn 1: Elemental Bolt costs 1 RP, so RP 14→13. It is named Elemental Bolt and deals Fire because Fire is the current Focus, so the chain is [Elemental Bolt]. Its attack hits for 2d8+3 fire; Fire Focus adds its printed Burn rider.
3. Turn 2: the Mage casts a distinct ordinary Fire spell whose Core V 2 cost is 2 RP, so RP 13→11. Because it is a different named Fire spell, the chain becomes [Elemental Bolt, ordinary Fire spell]. Ordinary Core V 2 Refrain/Dissonance rules still apply to that spell independently.
4. Turn 3: Elemental Surge costs 3 RP, so RP 11→8. It is a third different named Fire spell, completing the exact three-spell Nuke Chain. After it resolves, Dissonance vents 4→2 and Inferno Lance becomes primed through the end of the Mage's next regular turn.
5. Turn 3 Bonus Action: Inferno Lance is ready and costs 2 RP, so RP 8→6. The Mage fires its 20-foot line. Inferno Lance is a finisher, not another chain-building spell; after it resolves the chain and primed state clear and Inferno Lance receives its printed 3-round recharge.
6. Turn 4: the Mage uses Resonance Surge with Arcane Barrage. Arcane Barrage costs 3 RP plus 2 additional RP for Surge, so RP 6→1. Surge adds S d8 = 2d8 force damage to one Barrage damage roll. Because Arcane Barrage is non-elemental, it clears any partial Fire chain and Resonance Surge itself does not count as another spell.

## Base cards

#### Spellcasting

**Level 1 · automatic · mage.base.spellcasting**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic at Mage 1 |

Spellcasting. Tags: core, spellcasting. You automatically gain Mage spellcasting and access to the Mage repertoire permitted by your separately reconciled spell progression, including Evocation Tier I at the level specified by Core Systems. Use Intelligence for Mage spell attacks and save DCs. This feature is never purchased with a class-feature choice.

<details><summary>Preserved source wording — book line2890</summary>

Spellcasting: Access to Evocation Tier I spells, focusing on direct damage.

</details>

#### Resonance Pool

**Level 1 · automatic · mage.base.resonance-pool**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic at Mage 1 |

Resonance Pool. Tags: core, resonance. Your Mage spells and Mage class-spell cards draw from the same Core Systems V 2 Resonance Point pool. Use the authoritative Mage RP maximum by Mage level. This card creates no second pool, no spell slots and no additional recovery method. It is never purchased with a class-feature choice.

<details><summary>Preserved source wording — book line2891</summary>

Resonance Pool: A reservoir of arcane energy that powers your spells and recovers during rest.

</details>

#### Arcane Insight

**Level 1 · selection · mage.base.arcane-insight**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Arcane Insight. Tags: passive, knowledge. Gain proficiency in Arcana, or expertise if already proficient. After examining a magical item, spell residue, ward or active magical effect for 1 minute, you may make an Intelligence (Arcana) check to identify its school, broad function or elemental signature. The Director sets the normal knowledge DC; failure supplies no fabricated information.

<details><summary>Preserved source wording — book line2892</summary>

Arcane Insight: Identify magical effects and items with greater accuracy than non-mages.

</details>

#### Elemental Affinity

**Level 2 · selection · mage.base.elemental-affinity**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always after Elemental Focus is chosen |

Elemental Affinity. Tags: passive, elemental. Gain resistance to the damage type of your current Elemental Focus: fire for Fire, cold for Cold or lightning for Lightning. If Elemental Pivot temporarily changes your Focus, this resistance changes with it and returns to your original element when the Pivot ends.

<details><summary>Preserved source wording — book line2893</summary>

Elemental Affinity: Gain a minor resistance to your chosen element once selected.

</details>

#### Spell Precision

**Level 1 · selection · mage.base.spell-precision**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your area Mage spells | Instantaneous modification | Once per Mage spell |

Spell Precision. Tags: passive, spell. When you cast a Mage spell that forces creatures in an area to make a saving throw, choose up to M creatures you can perceive in that area. Those creatures automatically succeed on that spell's initial save and take no damage if a normal successful save would deal half damage. This does not protect them from later independent hazards or pulses.

<details><summary>Preserved source wording — book line2894</summary>

Spell Precision: Reduce the chance of friendly fire damage from your area effect spells.

</details>

#### Arcane Missile

**Level 1 · selection · mage.base.arcane-missile**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | One creature within 60 feet | Instantaneous | At will while RP remains |

Arcane Missile. Tags: mage-spell, arcane, damage. The missile automatically hits one creature you can perceive within range and deals S d4 + M force damage. No attack roll or saving throw is made. It is non-elemental, so casting it clears an Elemental Focus Nuke Chain. Multiple missiles are represented by the scaling dice, not separate hits or triggers.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2897</summary>

Arcane Missile: Launch bolts of pure arcane energy that unerringly strike your target.

</details>

#### Elemental Bolt

**Level 2 · selection · mage.base.elemental-bolt**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | One creature within 60 feet | Instantaneous | At will while RP remains |

Elemental Bolt. Tags: mage-spell, elemental, focus, damage. Make a Mage spell attack. On a hit deal S d8 + M damage of your current Focus. Fire: target takes 1d4 fire at the start of its next turn. Cold: Speed -10 feet until the end of its next turn. Lightning: one different enemy within 10 feet takes S lightning damage. Secondary damage creates no new spell cast or chain credit.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2898</summary>

Elemental Bolt: Cast a bolt of your chosen element (once selected) that deals additional effects based on the element.

</details>

#### Resonance Shield

**Level 1 · selection · mage.base.resonance-shield**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | Spend X RP, where X is 1, 2 or 3 | Self | 1 minute or until temporary HP are lost | Recharge 2 rounds |

Resonance Shield. Tags: mage-spell, abjuration, protection. Spend 1-3 RP and gain temporary HP equal to X × (S + M). Temporary HP do not stack. This spell is non-elemental and therefore clears an active Elemental Nuke Chain. Its RP payment cannot be reduced below 1 by Spell Efficiency.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2899</summary>

Resonance Shield: Convert a portion of your Resonance Points into a temporary protective barrier.

</details>

#### Blink

**Level 1 · selection · mage.base.blink**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self | Instantaneous | Recharge 2 rounds |

Blink. Tags: mage-spell, teleportation. Teleport to an unoccupied space you can perceive within 30 feet. This movement does not provoke opportunity attacks and cannot pass through planar wards that prohibit teleportation. Blink deals no damage and is non-elemental, so using it clears an active Elemental Nuke Chain.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2900</summary>

Blink: Teleport a short distance to avoid danger or reposition.

</details>

#### Detect Magic

**Level 1 · selection · mage.base.detect-magic**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | Self; 30-foot magical sense | Concentration, up to 10 minutes | At will while RP remains |

Detect Magic. Tags: mage-spell, divination, concentration. While concentrating, sense the presence and approximate location of active magical auras within 30 feet that are not completely blocked by an effect specifically preventing magical detection. Spending an Action examining one sensed aura reveals its broad school or elemental character. It is non-elemental and clears an active Nuke Chain.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2901</summary>

Detect Magic: Sense and identify magical auras and effects in your vicinity.

</details>

### Fire

#### Fire

**Level 2 · automatic · mage.base.fire.fire**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0; Inferno Lance costs 2 RP when primed | Self; finisher uses a 20-foot-long, 5-foot-wide line originating from you | Permanent Focus; finisher instantaneous plus Burn | Choose at Mage 2; finisher recharge 3 rounds |

Elemental Focus — Fire. Tags: focus, fire. Once on each of your turns when a Fire Mage spell deals damage, add S fire damage to one damaged target. That target also takes 1d4 fire at the start of its next turn; repeated Burns refresh rather than stack. FINISHER — Inferno Lance: after a completed Fire Nuke Chain, Bonus Action, 2 RP. Creatures in the 20-foot line make Dexterity saves, taking (S+1)d8 fire on failure or half on success. Failed targets also take 1d6 fire at the start of each of their next 2 turns.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2907</summary>

Fire: +10% damage, adds Burn DoT effect. Finisher: Inferno Lance – 4-tile line, DoT over time

</details>

### Cold

#### Cold

**Level 2 · automatic · mage.base.cold.cold**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0; Glacier Spike costs 2 RP when primed | Self; finisher uses a 15-foot cone | Permanent Focus; finisher instantaneous plus slow | Choose at Mage 2; finisher recharge 3 rounds |

Elemental Focus — Cold. Tags: focus, cold. Once on each of your turns, a natural 19 that hits with a Cold Mage spell is a critical hit. When a Cold Mage spell damages a creature, its Speed is reduced by 10 feet until the end of its next turn, minimum 0. FINISHER — Glacier Spike: after a completed Cold Nuke Chain, Bonus Action, 2 RP. Creatures in a 15-foot cone make Constitution saves, taking (S+1)d8 cold on failure or half on success; failed creatures have their Speed halved until the end of their next turn.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2908</summary>

Cold: +5% crit chance, slows targets. Finisher: Glacier Spike – Cone AoE, 50% slow

</details>

### Lightning

#### Lightning

**Level 2 · automatic · mage.base.lightning.lightning**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0; Storm Arc costs 2 RP when primed | Self; finisher starts on one enemy within 60 feet and may jump twice within 15 feet | Permanent Focus; finisher instantaneous | Choose at Mage 2; finisher recharge 3 rounds |

Elemental Focus — Lightning. Tags: focus, lightning. Once on each of your turns after a Lightning Mage spell damages a creature, arc S lightning damage to one different enemy within 10 feet. FINISHER — Storm Arc: after a completed Lightning Nuke Chain, Bonus Action, 2 RP. Make separate Mage spell attacks against one enemy within 60 feet and up to two additional different enemies, each within 15 feet of the previous target. Each hit deals S d6 lightning. A target critically hit by Storm Arc makes a Constitution save; failure Stuns it until the end of its next turn.

Class-spell rank: **1** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2909</summary>

Lightning: +15% jump chance, arc disruption. Finisher: Storm Arc – Jumps to 3 enemies, stuns on crit

</details>

## Arch cards

#### Arcane Stability

**Level 3 · selection · mage.arch.arcane-stability**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Arcane Stability. Tags: arcanist, passive. When damage causes you to make a concentration save for a Mage spell, add +2 to that save. This bonus does not stack with another feature named Arcane Stability and does not change the concentration DC. It does not prevent Silence, incapacitation or effects that end concentration without a save.

<details><summary>Preserved source wording — book line2912</summary>

Arcane Stability: Reduce spell fizzle chance by 25%.

</details>

#### Overload Crits

**Level 3 · selection · mage.arch.overload-crits**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One enemy within 10 feet of a creature critically hit by your damaging Mage spell | Instantaneous | At most once per turn |

Overload Crits. Tags: arcanist, critical. When a damaging Mage spell scores a critical hit, choose one different enemy within 10 feet of the critically hit target. It takes damage of the same type equal to 50% of the spell's base unmodified damage dice total before critical extra dice, rounded down once, minimum 1. Flat bonuses, riders and critical extra dice are not copied again.

<details><summary>Preserved source wording — book line2913</summary>

Overload Crits: Critical strikes deal +50% splash damage to nearby enemies.

</details>

#### Arcane Bypass

**Level 5 · selection · mage.arch.arcane-bypass**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One Mage spell you are beginning to cast | For that spell | 1/long rest |

Arcane Bypass. Tags: arcanist, penetration. Before paying costs for a damaging Mage spell, declare Arcane Bypass. Damage from that spell ignores resistance to its printed damage types. Immunity remains immunity. The declaration is spent once the spell is legally cast even if all attacks miss or all targets succeed on saves.

<details><summary>Preserved source wording — book line2914</summary>

Arcane Bypass: Once per rest, ignore all enemy resistances for one spell.

</details>

#### Metaspell Access

**Level 5 · selection · mage.arch.metaspell-access**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One Mage spell you are beginning to cast | For that spell | 1/long rest; choose one metamagic mode when this feature is acquired |

Metaspell Access. Tags: arcanist, metamagic. Choose one mode permanently: Reach increases one spell's range by 30 feet; Widen increases one circular radius or cone length by 5 feet; Sculpt lets up to M creatures automatically succeed on that spell's initial area save and take no damage if success normally halves damage. Apply the chosen mode once per long rest before casting; it does not alter RP cost or create another cast.

<details><summary>Preserved source wording — book line2915</summary>

Metaspell Access: Choose one Universal Metamagic effect to apply to a spell once per day.

</details>

#### Elemental Mastery

**Level 7 · selection · mage.arch.elemental-mastery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your current Elemental Focus spells | Permanent | Always |

Elemental Mastery. Tags: arcanist, focus. Improve the secondary effect of your current Focus. Fire Burns from your Focus cards last one additional turn but never stack. Cold Focus Speed reductions increase by another 5 feet, minimum 0. Lightning Focus's once-per-turn secondary arc increases from S flat lightning damage to S d4 lightning damage. Pivoted Focus uses the corresponding upgraded rider.

<details><summary>Preserved source wording — book line2916</summary>

Elemental Mastery: Increase the effectiveness of your chosen element's secondary effects.

</details>

#### Spell Efficiency

**Level 9 · selection · mage.arch.spell-efficiency**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until end of your next regular turn | At most once per turn |

Spell Efficiency. Tags: arcanist, resonance, focus. After you legally cast a Focus-eligible spell, your next differently named Focus-eligible spell of the same current element before the end of your next regular turn costs 1 less RP, minimum 1 RP. This reduction cannot apply to Focus finishers, Resonance Surge's additional cost or a spell already reduced to 0 by another explicit feature.

<details><summary>Preserved source wording — book line2917</summary>

Spell Efficiency: Reduce the Resonance Point cost of spells cast in sequence with the same element.

</details>

#### Elemental Surge

**Level 3 · selection · mage.arch.elemental-surge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One creature within 60 feet | Instantaneous | Recharge 2 rounds |

Elemental Surge. Tags: mage-spell, arcanist, elemental, focus, damage. Make a Mage spell attack. On a hit deal (S+1)d8 + M damage of your current Focus. Fire also applies the Focus Burn; Cold applies the Focus Speed reduction; Lightning applies the Focus secondary arc. This is Focus-eligible and can occupy one slot in a Nuke Chain.

Class-spell rank: **2** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2920</summary>

Elemental Surge: Channel a concentrated burst of your chosen element, dealing high damage to a single target.

</details>

#### Arcane Barrage

**Level 3 · selection · mage.arch.arcane-barrage**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Creatures within 60 feet | Instantaneous | Recharge 2 rounds |

Arcane Barrage. Tags: mage-spell, arcanist, arcane, damage. Create S+2 force bolts. Each bolt automatically hits one creature you can perceive within 60 feet for 1d4 force damage. Distribute bolts among any number of legal targets, but all bolts together are one spell cast. This spell is non-elemental and clears an active Nuke Chain.

Class-spell rank: **2** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2921</summary>

Arcane Barrage: Launch multiple arcane projectiles that seek out different targets.

</details>

#### Conjure Elemental Familiar

**Level 5 · selection · mage.arch.conjure-elemental-familiar**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | One unoccupied space within 30 feet | 10 minutes | 1/long rest |

Conjure Elemental Familiar. Tags: mage-spell, arcanist, summon, elemental. Summon one elemental familiar matching your current Focus using the common familiar stat block. Only one elemental familiar from this feature may exist at once; summoning another dismisses the first. It obeys the shared Companion Command rule. It disappears at 0 HP or when duration ends and leaves no corpse, XP, loot or resource trigger.

Class-spell rank: **3** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2922</summary>

Conjure Elemental Familiar: Summon a minor elemental of your chosen type to assist you in combat.

</details>

#### Displacement

**Level 7 · selection · mage.arch.displacement**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 RP | Self | Until start of your next regular turn | Recharge 3 rounds |

Displacement. Tags: mage-spell, arcanist, illusion, teleportation. Teleport up to 20 feet to an unoccupied space you perceive and create two illusory duplicates. Until the start of your next regular turn, the next two attack rolls made against you have disadvantage; each attack roll consumes one duplicate whether it hits or misses. Area effects ignore the duplicates. This non-elemental spell clears an active Nuke Chain.

Class-spell rank: **4** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2923</summary>

Displacement: Create illusory duplicates of yourself while teleporting to safety.

</details>

#### Counterspell

**Level 9 · selection · mage.arch.counterspell**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 4 RP | One creature you perceive casting a spell within 60 feet | Instantaneous | Recharge 3 rounds |

Counterspell. Tags: mage-spell, arcanist, disruption. Trigger when a creature begins casting a spell. Make an Intelligence check adding your proficiency bonus against DC 10 + twice the spell's rank, treating rank 0 as 0. On success the triggering spell is negated after its costs are paid. On failure it proceeds normally. Counterspell is non-elemental and, because it is itself a spell, clears an active Nuke Chain.

Class-spell rank: **5** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2924</summary>

Counterspell: Disrupt an enemy's spellcasting, potentially negating their spell entirely.

</details>

## Hero cards

### Archmage

#### Ward of Purity

**Level 10 · selection · mage.hero.archmage.ward-of-purity**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 3 RP | You and allies within 15 feet | Until triggering spell finishes resolving | 1/short rest |

Ward of Purity. Tags: archmage, abjuration, ward. Trigger when you or an ally within 15 feet would take damage from a spell. Create a ward over all chosen allies in range; reduce spell damage to each by S+M, minimum 0. If at least one point is prevented, the original caster takes S force damage once. Reflection cannot trigger another reflection or proc chain.

<details><summary>Preserved source wording — book line2933</summary>

Ward of Purity: Create an AoE shield that reflects 25% of incoming spells.

</details>

#### Celestial Comet

**Level 12 · selection · mage.hero.archmage.celestial-comet**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 6 RP | 20-foot-radius sphere centered at a point within 60 feet | Instantaneous plus Blind rider | Recharge 4 rounds |

Celestial Comet. Tags: mage-spell, archmage, radiant, arcane, damage. Creatures of your choice in the area make Dexterity saves, taking (S+2)d8 radiant damage on failure or half on success. A creature that fails by 10 or more is Blinded until the end of its next turn. Celestial Comet is non-Focus elemental magic and clears an active Nuke Chain.

Class-spell rank: **6** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2934</summary>

Celestial Comet: Cast a Radiant/Arcane AoE that blinds enemies.

</details>

#### Empowered Link

**Level 14 · selection · mage.hero.archmage.empowered-link**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Up to M allies within 25 feet | Matches the shared benefit, maximum until end of your next regular turn | At most once per turn |

Empowered Link. Tags: archmage, buff. When one of your Mage cards grants you temporary HP, a Speed bonus or a numeric attack/save bonus, choose up to M allies within 25 feet. They gain the same non-resource benefit at half its numeric amount rounded down, minimum 1 where applicable. It never shares Actions, RP, Focus, concentration, invisibility, summons or class resources. Resistance is not a numeric bonus and is not shared by this card.

<details><summary>Preserved source wording — book line2935</summary>

Empowered Link: Share buffs with allies in a 5-tile radius.

</details>

#### Harmonized Core

**Level 16 · selection · mage.hero.archmage.harmonized-core**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One ally within 30 feet | Temporary HP until lost or replaced | At most once per turn |

Harmonized Core. Tags: archmage, support. After one of your damaging Mage spells deals damage, choose one ally within 30 feet. It gains temporary HP equal to 10% of one target's unmodified rolled damage dice total from that spell, rounded down, minimum 1 and maximum S+M. This is not HP healing and cannot trigger healing features or Echo-style repetitions.

<details><summary>Preserved source wording — book line2936</summary>

Harmonized Core: Spells heal allies for 10% of base damage as temporary HP.

</details>

#### Arcane Sanctuary

**Level 10 · selection · mage.hero.archmage.arcane-sanctuary**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 6 RP to start; 1 RP maintenance | 15-foot-radius fixed zone centered within 30 feet | Concentration, maximum 3 Mage turns | Recharge 4 rounds |

Arcane Sanctuary. Tags: mage-spell, archmage, zone, concentration. On start and each paid Bonus Action maintenance pulse, allies in the zone gain S+M temporary HP until the start of your next regular turn or effect end, whichever is first and +1 to Mage or spell attack rolls while inside. The zone grants no save-DC increase and no additional Actions. Maximum 3 pulses.

Class-spell rank: **5** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2939</summary>

Arcane Sanctuary: Create a zone of protection that shields allies and enhances their magical abilities.

</details>

#### Purifying Beam

**Level 10 · selection · mage.hero.archmage.purifying-beam**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | 60-foot-long, 5-foot-wide line | Instantaneous | Recharge 3 rounds |

Purifying Beam. Tags: mage-spell, archmage, radiant, cleansing. Enemies in the line make Dexterity saves, taking (S+1)d8 radiant damage on failure or half on success. Up to M allies in the line may each end one of Charmed, Frightened or Poisoned. Cleansing does not remove Wounds, curses or disease unless another rule expressly allows it. This non-Focus spell clears an active Nuke Chain.

Class-spell rank: **5** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2940</summary>

Purifying Beam: Channel a beam of radiant arcane energy that damages enemies and cleanses negative effects from allies.

</details>

#### Spell Sharing

**Level 12 · selection · mage.hero.archmage.spell-sharing**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP plus the shared card's printed RP cost | One willing ally within 30 feet | Until end of ally's next regular turn | 1/short rest |

Spell Sharing. Tags: archmage, spell-sharing. Choose one Base or Arch Mage spell card you know with an Action activation and printed base RP cost 4 or less. Pay both costs now. The ally may cast that card once before the end of its next turn without paying RP, using your Mage spell attack and DC. It cannot share summons, Counterspell, Hero cards, finishers, Resonance Surge or another Spell Sharing.

<details><summary>Preserved source wording — book line2941</summary>

Spell Sharing: Temporarily grant an ally access to one of your spells.

</details>

#### Resonance Transfusion

**Level 14 · selection · mage.hero.archmage.resonance-transfusion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Transfer 1 to S+M of your current RP | One willing creature within 30 feet with an RP pool | Instantaneous | 1/short rest |

Resonance Transfusion. Tags: archmage, resonance. Choose X from 1 to S+M, limited by your current RP. Lose X RP and the target restores X RP, never above its own maximum. This is a transfer, not generation. It cannot target yourself, cannot be amplified, Echoed or converted into HP, and neither side gains Dissonance from the transfer itself. The recipient is another creature; same-pool transfers and circular refund chains cannot increase total RP.

<details><summary>Preserved source wording — book line2942</summary>

Resonance Transfusion: Transfer a portion of your Resonance Points to restore an ally's magical reserves.

</details>

#### Arcane Convergence

**Level 16 · selection · mage.hero.archmage.arcane-convergence**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | You and up to two willing allied spellcasters within 30 feet | Until start of your next regular turn | Recharge 4 rounds |

Arcane Convergence. Tags: archmage, coordination. Choose up to two allied spellcasters. Before the start of your next regular turn, the next damaging spell cast by each chosen creature, including you, adds 1d6 damage of one type that spell already deals. A creature receives this bonus only once, and the added die cannot trigger another Convergence, Resonance Surge or action grant.

<details><summary>Preserved source wording — book line2943</summary>

Arcane Convergence: Combine your magic with nearby allies for a coordinated, enhanced spell effect.

</details>

### Elementalist

#### Elemental Pivot

**Level 10 · selection · mage.hero.elementalist.elemental-pivot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self | Until encounter ends or you dismiss it | 1/short rest |

Elemental Pivot. Tags: elementalist, focus. Switch your current Elemental Focus to one of the other two Focuses. Your Elemental Affinity, Focus passive, Elemental Mastery rider and available finisher change to that element. Clear the current Nuke Chain and any primed finisher when Pivot occurs. At encounter end your original level-2 Focus automatically returns.

<details><summary>Preserved source wording — book line2949</summary>

Elemental Pivot: Switch focus element mid-combat as a bonus action.

</details>

#### Voltaic Pulse

**Level 10 · selection · mage.hero.elementalist.voltaic-pulse**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | One different enemy within 15 feet of a creature damaged by your Lightning spell | Instantaneous | At most once per round |

Voltaic Pulse. Tags: elementalist, lightning, control. After your Lightning Mage spell damages a creature, spend 1 RP to arc S d4 lightning damage to one different enemy within 15 feet. That enemy makes a Constitution save; on failure it also loses its Reaction until the start of its next turn. This is not another spell cast and grants no Nuke Chain credit.

<details><summary>Preserved source wording — book line2950</summary>

Voltaic Pulse: Create an AoE jump-stun effect.

</details>

#### Elemental Overload

**Level 12 · selection · mage.hero.elementalist.elemental-overload**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 2 RP | 15-foot square centered on a point within 30 feet of a target damaged by your elemental spell | Instantaneous | 1/short rest |

Elemental Overload. Tags: elementalist, elemental, area. After a Fire, Cold or Lightning Mage spell deals damage, spend 2 RP and choose one different element from those three. Creatures of your choice in the square make Dexterity saves, taking S d6 damage of the triggering type plus S d6 of the chosen second type on failure, half on success. This is one triggered effect, not another spell cast.

<details><summary>Preserved source wording — book line2951</summary>

Elemental Overload: Deal dual-element damage in a 3x3 blast.

</details>

#### Elemental Supremacy

**Level 14 · selection · mage.hero.elementalist.elemental-supremacy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self and current Focus finisher | Permanent | Always; reset at most once per round |

Elemental Supremacy. Tags: elementalist, focus, vulnerability. Once on each of your turns when a Mage spell deals a damage type to which its target is vulnerable, add S damage of that type after vulnerability is applied. Additionally, when a hostile non-summoned creature that meaningfully threatened the party dies from one of your Focus-eligible spells, you may reset your current Focus finisher's positive recharge counter to 0, subject to the universal reset limit.

<details><summary>Preserved source wording — book line2952</summary>

Elemental Supremacy: Deal +10% damage against elemental vulnerabilities; reset chain cooldown on kill.

</details>

#### Elemental Fusion

**Level 10 · selection · mage.hero.elementalist.elemental-fusion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | One creature within 60 feet | Instantaneous | Recharge 2 rounds |

Elemental Fusion. Tags: mage-spell, elementalist, elemental, damage. Choose your current Focus and one other element among Fire, Cold and Lightning. Make a Mage spell attack. On hit deal S d8 of each chosen element. Pair rider: Fire+Cold reduces Speed by 10 feet and applies 1d4 fire at start of target's next turn; Fire+Lightning removes Reaction until start of target's next turn; Cold+Lightning reduces Speed by 10 feet and prevents opportunity attacks until end of target's next turn. For Nuke Chain purposes this spell counts only as your current Focus element.

Class-spell rank: **5** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2955</summary>

Elemental Fusion: Combine two elements to create a hybrid spell with unique effects.

</details>

#### Cascade Storm

**Level 12 · selection · mage.hero.elementalist.cascade-storm**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 6 RP | Up to three different creatures within 60 feet | Instantaneous | Recharge 3 rounds |

Cascade Storm. Tags: mage-spell, elementalist, fire, cold, lightning, damage. Choose up to three creatures. Resolve one separate Mage spell attack against each: first hit deals S d6 fire and 1d4 fire next turn; second hit deals S d6 cold and Speed -10 feet until end next turn; third hit deals S d6 lightning and removes Reaction until start next turn. If fewer than three targets are chosen, unused elements are lost. For Nuke Chain purposes choose one of the three elements before casting; Cascade Storm counts only as that element.

Class-spell rank: **6** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2956</summary>

Cascade Storm: Trigger a sequence of elemental effects that build upon each other.

</details>

#### Elemental Absorption

**Level 14 · selection · mage.hero.elementalist.elemental-absorption**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 3 RP | Self | Until end of your next regular turn | Recharge 3 rounds |

Elemental Absorption. Tags: mage-spell, elementalist, protection. Trigger when you would take fire, cold or lightning damage. Gain resistance to that triggering damage type for the triggering event and until the end of your next regular turn. Your next damaging Mage spell before then adds 1d8 of the absorbed type to one damage roll; the bonus is lost after use or expiry. This Reaction spell clears an incompatible current Nuke Chain unless the absorbed type is your current Focus.

Class-spell rank: **7** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2957</summary>

Elemental Absorption: Temporarily absorb incoming elemental damage to enhance your next spell.

</details>

#### Primal Channeling

**Level 16 · selection · mage.hero.elementalist.primal-channeling**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | Instantaneous | 1/short rest |

Primal Channeling. Tags: elementalist, resonance. During a real encounter, draw ambient elemental energy and restore 2 RP, never above your maximum. You cannot use Primal Channeling outside a real encounter, during a rest, through a summoned proxy or more than once per short rest. It does not count as a spell cast, does not advance Nuke Chain and does not alter Dissonance.

<details><summary>Preserved source wording — book line2958</summary>

Primal Channeling: Draw raw elemental energy from the environment to empower your spells.

</details>

#### Elemental Mastery

**Level 16 · selection · mage.hero.elementalist.elemental-mastery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 5 RP | Self | 3 rounds | 1/long rest |

Elemental Mastery. Tags: elementalist, focus, mastery. For 3 rounds, Fire, Cold and Lightning Mage spells all count as matching your current Focus for Nuke Chain eligibility. After you complete one three-distinct-name chain during this duration, you may choose any one of the three Focus finishers when it becomes primed, regardless of your current Focus. Only one finisher may be generated by this use. After that finisher resolves or expires, the mastery continues defensively but cannot prime another off-focus finisher.

<details><summary>Preserved source wording — book line2959</summary>

Elemental Mastery: Temporarily gain mastery over all elements, allowing you to use any elemental finisher regardless of your focus.

</details>

### Lich

#### Undying Spellform

**Level 10 · selection · mage.hero.lich.undying-spellform**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Until end of your next regular turn | 1/long rest |

Undying Spellform. Tags: lich, undead, death. When damage reduces you to 0 HP without killing you outright, remain conscious and able to take Actions until the end of your next regular turn. You remain at 0 HP, cannot benefit from voluntary movement faster than half Speed, and still suffer ordinary consequences of further damage. If still at 0 HP when the effect ends, become unconscious and suffer one failed death save. Healing above 0 ends this feature early.

<details><summary>Preserved source wording — book line2979</summary>

Undying Spellform: When reduced to 0 HP, continue casting for 1 full round before death.

</details>

#### Soul Reservoir

**Level 12 · selection · mage.hero.lich.soul-reservoir**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Instantaneous | At most once per turn and at most S times per encounter |

Soul Reservoir. Tags: lich, resonance, damage-over-time. During a real encounter, when a hostile creature takes damage from a damage-over-time effect created by one of your Mage spells, restore 1 RP, never above maximum. The same damage event cannot restore more than 1 RP. Damage to allies, summons, trivial creatures or your own companions does not qualify.

<details><summary>Preserved source wording — book line2980</summary>

Soul Reservoir: All DoT damage you deal feeds Resonance recovery.

</details>

#### Necromantic Mastery

**Level 14 · selection · mage.hero.lich.necromantic-mastery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your necrotic Mage spells | Permanent | Always |

Necromantic Mastery. Tags: lich, necromancy. Once on each of your turns when a Mage spell deals necrotic damage, add S necrotic damage to one damaged target. Your necrotic Mage spells also ignore resistance to necrotic damage; immunity remains immunity. This feature does not convert another spell's damage type and cannot apply to companion attacks unless a card explicitly identifies them as your spell.

<details><summary>Preserved source wording — book line2981</summary>

Necromantic Mastery: Gain access to enhanced necromancy spells and abilities.

</details>

#### Undead Immunities

**Level 16 · selection · mage.hero.lich.undead-immunities**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent after successful Lich transformation | Always |

Undead Immunities. Tags: lich, undead. You are immune to poison damage, the Poisoned condition, disease, Frightened, Charmed and magical sleep. You no longer need to breathe. You still require the normal rest schedule for mechanical recovery and can still be affected by abilities that specifically target undead unless another feature says otherwise.

<details><summary>Preserved source wording — book line2982</summary>

Undead Immunities: Become immune to poison, disease, fear, sleep, and mind control.

</details>

#### Lingering Malice

**Level 10 · selection · mage.hero.lich.lingering-malice**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP to start; 1 RP maintenance | 15-foot-radius fixed zone centered within 60 feet | Concentration, maximum 3 Mage turns | Recharge 4 rounds |

Lingering Malice. Tags: mage-spell, lich, necrotic, zone, concentration. Choose Fear or Drain when cast. On start and each paid Bonus Action maintenance pulse, enemies in the zone make Wisdom saves. Failure takes S d6 necrotic. Fear mode also Frightens until the start of your next turn. Drain mode lets you gain temporary HP equal to M once per pulse if at least one enemy fails. Maximum 3 pulses; each pulse grants a new save.

Class-spell rank: **5** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2985</summary>

Lingering Malice: Create a necrotic zone for 3 rounds that applies Fear or Drain effects.

</details>

#### Resonance to Flesh

**Level 10 · selection · mage.hero.lich.resonance-to-flesh**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Variable conversion | Self | Instantaneous | 1/short rest |

Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions.

<details><summary>Preserved source wording — book line2986</summary>

Resonance to Flesh: Convert Resonance into HP (or vice versa) once per rest.

</details>

#### Flesh to Ash

**Level 12 · selection · mage.hero.lich.flesh-to-ash**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | 15-foot-radius sphere centered at a point within 60 feet | Instantaneous | Recharge 3 rounds |

Flesh to Ash. Tags: mage-spell, lich, necrotic, damage. Creatures of your choice in the area make Constitution saves. A target at half maximum HP or more takes S d8 necrotic on failure, half on success. A target below half maximum HP instead takes 2 S d8 necrotic on failure, half on success. Determine the threshold before rolling damage.

Class-spell rank: **6** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2987</summary>

Flesh to Ash: Create an AoE burst that doubles damage if target is below 50% HP.

</details>

#### Corpse Gateway

**Level 14 · selection · mage.hero.lich.corpse-gateway**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | One visible corpse within 60 feet and one unoccupied space within 5 feet of it | Instantaneous | Recharge 2 rounds |

Corpse Gateway. Tags: mage-spell, lich, teleportation, corpse. Teleport to the chosen unoccupied space adjacent to a visible corpse. The corpse is not consumed or altered. Summoned-companion remains, repeated fragments of the same destroyed creature and illusory corpses are not legal anchors. This non-elemental spell clears an active Nuke Chain.

Class-spell rank: **7** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2988</summary>

Corpse Gateway: Teleport to a corpse within line of sight.

</details>

#### Soulbound Ritual

**Level 16 · selection · mage.hero.lich.soulbound-ritual**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | One of your destroyed bound elite undead companions within 30 feet or its inert binding token | Instantaneous | 1/long rest |

Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again.

Class-spell rank: **8** for Dissonance, countering and rank restrictions; pay printed RP only.

<details><summary>Preserved source wording — book line2989</summary>

Soulbound Ritual: Revive a fallen undead pet with bonus stats.

</details>

#### Resonance Apex — NEW Playtest Capstone

**Level 20 · automatic · mage.supplement.resonance-apex-new-playtest-capstone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 additional RP | One Mage spell you are beginning to cast | For that cast | 1/long rest |

Before paying for one Mage spell, reduce that spell's printed RP cost by up to 10 RP, minimum final cost 0. This capstone is new playtest design and is not claimed as a recovered historical feature. The cast cannot also use Resonance Surge or generic Overcast. It remains one spell cast, follows ordinary Focus/Nuke Chain rules, and alters Dissonance only through rules that would already apply to that cast.

Prerequisite: See class engine and progression.

Source status: **new playtest completion**, not recovered historical wording.

## Source appendix and open balance questions

The complete original Mage book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/mage.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Does requiring three different named Focus spells make Nuke Chains achievable at the intended cadence without forcing every Mage into the same ordinary-spell repertoire, and are the 2 RP Bonus Action finishers appropriately rewarding for the setup?
- Do Resonance Surge, Spell Efficiency, Primal Channeling, Soul Reservoir and Resonance to Flesh keep the shared Core V2 RP economy bounded across multiple encounters rather than creating a sustainable positive-RP loop?
- With the one-shared-damaging-command rule, do the elemental familiar and Lich's three elite companions provide meaningful identity without overwhelming the Mage's own Action economy or creating corpse, kill, control or resource farms?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
