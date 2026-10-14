# Thief — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/thief.json) · [Normalized card data](../../../data/public/class_playtests/thief.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Dexterity
- Secondary Attribute: Intelligence or Wisdom (player choice for traps/senses)
- Hit Points: Medium (8 + Constitution modifier at 1st level, 1d8 per level thereafter)
- Armor Proficiency: Light armor
- Weapon Proficiency: Daggers, short swords, thrown weapons, hand crossbows
- Tool Proficiency: Thieves' tools, poisoner's kit

Dexterity governs weapons and class DC/M. Choose Intelligence or Wisdom for noncombat class tool/sense checks at 1. Hit Die d8; light armor, daggers, shortswords, thrown weapons and hand crossbows; thieves tools and poison kit. Sneak Attack is automatic at 1: once on your regular turn, add ceil(class level/2)d6 to one finesse/ranged weapon hit if you had advantage, an active ally threatens target within 5 ft, or target is suffering your Bleed/Poisoned/Crippled. Disadvantage prevents Sneak Attack even if canceled into a straight roll. A feature can explicitly grant Sneak Attack on a different qualifying hit but never more than once/regular turn. Copies, poison ticks and companions cannot Sneak Attack.

Prepare fictional poison doses with poison kit during a long rest: maximum 3 carried at 1, 4 at 10, 5 at 15, 6 at 20; refill to this cap, never stockpile or sell these class preparations. A destroyed/confiscated kit prevents preparation until replaced. One dose coats one melee weapon or 2 projectiles, lasts 1 minute or until 2 attack attempts; hit applies its effect, miss still spends an attempt. Apply Poison card improves Action coating to Bonus Action; baseline coating is Action. Do not coat the same weapon with multiple doses except Double Poison. Fictional reagents come from ordinary adventuring supplies; no real-world recipes. Creating an exotic source-approved recipe requires an adventure specimen and one successful INT+PB poison-kit check DC 15, one attempt per specimen. It replaces a known recipe, not unlimited extra doses.

At 1 know all four Tier I recipes, at 7 add Tier II, at 14 Tier III. Poison saving throws use Thief DC except preserved source fixed DC 12 becomes max(12, Thief DC) for Mindburn/Venombite. Unless stated damage/conditions require a failed CON save; initial weapon damage is unaffected. Critical riders also need this failed save. One ongoing instance of each recipe per target; another application refreshes rather than stacks. Maximum 2 simultaneous different poison recipes from you per target. Bleed never stops all healing by default, Poisoned uses the Core V 2 condition: disadvantage on attacks and ability checks (not saving throws), and Shaken means disadvantage on next fear save. Neither is a hidden full-turn disable.

Tier I: Bloodleech gives Bleed 1d4 at start next 2 target turns; critical restores 1d4 of your HP, once per dose. Crippler gives-1 on next attack before end next turn; critical also half Speed for that duration. Mindburn uses WIS save: -1 spell-attack rolls until end next turn, critical also no Reactions. Venombite gives Poisoned until end next turn; critical also-1 on next save. Tier II: Ashblood adds 2d6 poison now and 1 fire at start next 2 turns; critical prevents HP recovery through end next turn. Silencer prevents verbal spellcasting through end next turn, critical also drops one held nonbonded item into its space; it can retrieve normally. Shiver gives Shaken through end next turn; critical also no Reactions. Hexroot gives-1 saves for 2 target turns; critical lets next weapon hit ignore resistance, never immunity, before end next turn.

Tier III: Voidspine deals 1d6 necrotic at start next 3 turns; critical adds-1 CON saves until end next turn, never changes ability scores/derived HP. Gravepetal makes target Unconscious until damage or end next turn, subject to shared hard-denial guard; critical also Prone and 3d6 poison immediate (resolve damage before unconsciousness). Neuroshock gives disadvantage on next DEX or WIS save before end next turn; critical also no Reactions. Wraithbane suppresses one observed bonus to AC (maximum 2) or damage resistance chosen before save until end next turn; critical prevents voluntary ethereal movement for duration. No core-engine, legendary action or creature-type removal; unsupported traits cannot be targeted.

Ordinary magical Thief techniques use the provisional minor-Weave RP pool and incur 1 D on use unless an ordinary spell says otherwise. Once per round, a Weave trick cast while hidden ignores its first point of Refrain Dissonance, as the protected source contract requires. It does not reduce base Dissonance or refund RP; a technique producing only its fixed 1 D receives no Refrain reduction unless it actually incurred Refrain. Arcane Trickster is still a Thief Hero, not an unrestricted full caster. Base 1–2, Rake Arch 3–9, chosen Arcane Trickster/Shadowblade/Blackguard Hero 10–20. Preserve advanced Arch gates: Distraction Tactics 13 and Crippling Strike 15 remain Arch selections obtainable after entering Hero. There is no automatic source Arch capstone; level 9 has its normal selection. Unseen Hand is Blackguard 20 automatic; the other paths receive the new level 20 finale below.

**Protected source interface:** Once per round, a Weave trick cast while hidden ignores its first point of Refrain Dissonance; stealth changes delivery, not RP cost.

## Advancement and resources

RP authority: Explicit fallback: Cleric CoreV2 curve ×0.35, halves upward. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 1 | 0 | Choose 4 Base; at least 2 active |
| 2 | Base | 1 | 0 | Choose 2 Base |
| 3 | Arch | 2 | 1 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 3 | 1 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 4 | 1 | Choose 1 Arch |
| 6 | Arch | 5 | 1 | Choose 1 Base/Arch |
| 7 | Arch | 6 | 1 | Choose 1 Arch |
| 8 | Arch | 7 | 2 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 8 | 2 | Choose 1 Arch |
| 10 | Hero | 9 | 2 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 11 | 2 | Choose 1 Base/Arch |
| 12 | Hero | 12 | 2 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 13 | 3 | Choose 1 Base/Arch |
| 14 | Hero | 14 | 3 | Choose 1 Hero |
| 15 | Hero | 15 | 3 | Choose 1 Base/Arch |
| 16 | Hero | 16 | 3 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 17 | 3 | Choose 1 Base/Arch |
| 18 | Hero | 18 | 4 | Choose 1 Hero |
| 19 | Hero | 19 | 4 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 20 | 4 | No ordinary selection; automatic: Unseen Hand (Blackguard), Master of the Unseen (Arcane Trickster), Master of the Unseen (Shadowblade) |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Thief 7, DEX 18, PB 3, S 2, M 4, Sneak 4d6, three doses prepared. Choose Bloodleech, Ashblood and Silencer. RP does not fuel mundane poison.
2. Turn 1 Bonus Action Apply Poison Bloodleech: doses 3→2 and coated attempts 2. Action weapon attack with adjacent ally qualifies Sneak. Hit deals weapon+4d6, CON save failure applies Bleed; coating attempts 2→1.
3. Target starts turn: takes 1d4 Bleed. No extra Sneak Attack, poison proc or RP recovery. It can still receive healing.
4. Turn 2 Feint uses Bonus Action; weapon hit at advantage can Sneak once. Final coating attempt 1→0; failed save refreshes Bloodleech duration instead of adding a second instance.
5. Turn 3 apply Ashblood, doses 2→1; miss spends first coated attempt without poison or Sneak damage. Tier II does not let this level 7 Thief select Hero abilities.
6. A long rest with kit refills to 3 total, rather than adding 3. No encounter transition refills doses.

## Base cards

#### Sneak Attack

**Level 1 · selection · thief.base.sneak-attack**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Sneak Attack | One hit | Once/own turn |

Upgrade automatic Sneak Attack: ignore 1 flat DR on the qualifying hit. Does not add another Sneak Attack or change its dice progression.

<details><summary>Preserved source wording — book line4371</summary>

Sneak Attack: Deal 1d6 extra damage when attacking from stealth, against flanked targets, or targets suffering from Bleed, Poison, or Disable.

</details>

#### Lockpick Mastery

**Level 1 · selection · thief.base.lockpick-mastery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Nonmagical locks using thieves tools | One check | Continuous |

Gain+5 on checks to pick nonmagical locks. Requires tools, access and ordinary time; success does not disable associated traps. Magic locks need their own permission.

<details><summary>Preserved source wording — book line4372</summary>

Lockpick Mastery: Gain +5 to open non-magical locks.

</details>

#### Stealth Chain

**Level 1 · selection · thief.base.stealth-chain**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self after Sneak Attack | Until end next turn | Once/turn |

Gain+2 on next Stealth check. You still need cover/concealment and an action to Hide; the bonus does not automatically hide an observed attacker.

<details><summary>Preserved source wording — book line4373</summary>

Stealth Chain: Gain +2 to your next stealth check after landing a Sneak Attack.

</details>

#### Toxin Sense

**Level 1 · selection · thief.base.toxin-sense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Exposed fictional poison within 5 ft | While examining | Continuous |

Recognize presence of poison on sight or smell if perceptible. Action with kit identifies its game recipe on DC 12 INT+PB; sealed or magical substances may evade detection. Never grants immunity.

<details><summary>Preserved source wording — book line4374</summary>

Toxin Sense: Identify resistances, immunities, or ideal poisons against enemies.

</details>

#### Trap Intuition

**Level 1 · selection · thief.base.trap-intuition**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While searching for traps | Continuous |

Advantage on Perception/Investigation to notice physical traps and their triggers. Does not reveal every trap automatically or defeat concealed magic.

<details><summary>Preserved source wording — book line4375</summary>

Trap Intuition: Gain advantage on checks to spot hidden traps and mechanisms.

</details>

#### Apply Poison

**Level 1 · selection · thief.base.apply-poison**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | One prepared dose | One weapon or 2 projectiles touched | 1 minute or 2 attack attempts | At will while doses remain |

Coat using engine rules. Replaces ordinary Action coating. Damage or critical riders use the dose profile and required save; it is not a free weapon attack.

<details><summary>Preserved source wording — book line4378</summary>

Apply Poison: Use a bonus action to apply poison to your weapon, lasting for 2 attacks.

</details>

#### Cunning Movement

**Level 1 · selection · thief.base.cunning-movement**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | Current turn | Recharge 2 |

Move up to half Speed without opportunity attacks; may pass through hostile occupied squares but not end there. Cannot cross impassable terrain or escape restraints.

<details><summary>Preserved source wording — book line4379</summary>

Cunning Movement: Move through hostile-occupied tiles without provoking opportunity attacks.

</details>

#### Disable Device

**Level 1 · selection · thief.base.disable-device**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Thieves tools | One accessible device within reach | One attempt | At will; retries need changed approach |

Make DEX+PB against its stated disarm DC; unknown DC defaults 15 for ordinary trap, 20 complex. Success disarms one accessible mechanism, failure by 5 triggers it. Does not automatically dispel magic.

<details><summary>Preserved source wording — book line4380</summary>

Disable Device: Disarm non-magical traps, pressure plates, or poison glyphs.

</details>

#### Feint

**Level 1 · selection · thief.base.feint**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | One enemy within 10 ft that perceives you | Until end current turn | Recharge 2 |

CHA or DEX+PB deception check against target passive Insight. Success grants advantage on your next weapon attack against it. Failure gives no bonus; no mind-control or guaranteed critical.

<details><summary>Preserved source wording — book line4381</summary>

Feint: Distract an opponent, giving you advantage on your next attack against them.

</details>

#### Shadow Step

**Level 1 · selection · thief.base.shadow-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self in cover/concealment | Immediate movement | Recharge 2 |

Move half Speed and attempt Hide if the destination can conceal you. Movement produces no deliberate footfall noise but normal senses still apply. This Base feature is not teleportation.

<details><summary>Preserved source wording — book line4382</summary>

Shadow Step: Move half your speed without making sound or leaving tracks.

</details>

## Arch cards

#### Combat Opener

**Level 3 · selection · thief.arch.combat-opener**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Combat initiative | Continuous |

Gain+5 initiative. Does not grant a surprise round, extra Action or automatic advantage against later actors.

<details><summary>Preserved source wording — book line4388</summary>

Combat Opener: Gain +5 to initiative rolls.

</details>

#### Ambush Focus

**Level 3 · selection · thief.arch.ambush-focus**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One creature unaware of you before your attack | One hit | Once/own turn |

Add 2 damage to first weapon hit against it. Becoming unaware again requires legitimate hiding; invisible but detected is not automatically unaware.

<details><summary>Preserved source wording — book line4389</summary>

Ambush Focus: Deal +2 damage against unaware or distracted targets.

</details>

#### Evasion

**Level 5 · selection · thief.arch.evasion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Against DEX save effects dealing half on success | Continuous |

Take no damage on success and half on failure, unless incapacitated. Applies only to such DEX damage saves; cannot halve every spell or condition.

<details><summary>Preserved source wording — book line4390</summary>

Evasion: Take half damage on successful saves against area effects (level 5).

</details>

#### Trap Sense

**Level 6 · selection · thief.arch.trap-sense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Against physical traps | Continuous |

Gain+2 AC against trap attacks and+2 saves against traps. These bonuses do not detect or disable them and do not apply to ordinary monster attacks in a corridor.

<details><summary>Preserved source wording — book line4391</summary>

Trap Sense: Gain passive trap detection and disarm bonuses (level 6).

</details>

#### Shadow Stab

**Level 9 · selection · thief.arch.shadow-stab**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 encounter use | One enemy critically hit by your melee weapon | Instant movement; Bleed 2 turns | 1/encounter |

After crit, move through target to adjacent empty space within 10 ft without opportunity attacks; apply Bleed 1d4 next 2 target turns. Movement requires open route, is not teleport and does not add another attack.

<details><summary>Preserved source wording — book line4392</summary>

Shadow Stab: On critical hit, teleport through target and apply Bleed (level 9).

</details>

#### Precision Feint

**Level 3 · selection · thief.arch.precision-feint**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 encounter use | One enemy within 10 ft | Until start next turn | 1/encounter |

DEX+PB versus passive Insight; success target-2 AC against your next attack and cannot take Reactions until start your next turn. Failure no effect; cannot stack AC penalties from copies.

<details><summary>Preserved source wording — book line4395</summary>

Precision Feint: Once per encounter, feint an enemy to impose -2 AC and remove their reactions until next round.

</details>

#### Vanish

**Level 3 · selection · thief.arch.vanish**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 short-rest use | Self | Until end next turn or attack | 1/short rest |

Become Invisible even while observed. Ends immediately after you attack, deal damage or force a save. Does not erase sound/tracks, allow passage through walls or grant full untargetability.

<details><summary>Preserved source wording — book line4396</summary>

Vanish: Become hidden even when observed, lasting until you attack or end your next turn.

</details>

#### Analyze Weakness

**Level 3 · selection · thief.arch.analyze-weakness**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | One perceived enemy within 30 ft | Until end next turn | Recharge 3 |

Identify one of its visible defenses: armor, cover or exhibited damage resistance. Next weapon hit ignores 2 flat DR; does not invent vulnerabilities or reveal undisplayed secrets.

<details><summary>Preserved source wording — book line4397</summary>

Analyze Weakness: Study a target to identify vulnerabilities and gain advantage on your next attack.

</details>

#### Distraction Tactics

**Level 13 · selection · thief.arch.distraction-tactics**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 encounter use | One enemy within 30 ft that perceives you | Until start next turn | 1/encounter |

Target WIS save; failure loses Reactions and next ally attack against it has advantage. Explicit Arch minimum 13 retained; no full Action theft.

<details><summary>Preserved source wording — book line4398</summary>

Distraction Tactics: Create a diversion that allows you to disengage freely once per turn (level 13).

</details>

#### Crippling Strike

**Level 15 · selection · thief.arch.crippling-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One enemy hit by your Sneak Attack | Until end next target turn | Once/own turn |

Target CON save; failure Speed halved. Does not stack multiple slow fractions or deny teleport. Explicit Arch minimum 15 retained.

<details><summary>Preserved source wording — book line4399</summary>

Crippling Strike: Your Sneak Attack applies Slow effect to the target (level 15).

</details>

## Hero cards

### Arcane Trickster

#### Mage Sense

**Level 10 · selection · thief.hero.arcane-trickster.mage-sense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | Visible magical phenomenon within 25 ft | Instant information | Recharge 2 |

Detect whether it is active spell magic and its broad school if observable. Does not penetrate total cover, read spell descriptions or identify hidden casters automatically.

<details><summary>Preserved source wording — book line4408</summary>

Mage Sense: Detect all magical effects and passives within 5 tiles.

</details>

#### Arcane Resistance

**Level 10 · selection · thief.hero.arcane-trickster.arcane-resistance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Against spells | Continuous |

Gain+2 saves against spells. Not all supernatural monster abilities are spells; no resistance to damage unless separately granted.

<details><summary>Preserved source wording — book line4409</summary>

Arcane Resistance: Gain +2 to saves against magic.

</details>

#### Illusory Stealth

**Level 10 · selection · thief.hero.arcane-trickster.illusory-stealth**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self while hidden | One casting | Once/own turn |

A nonhostile illusion or concealment technique does not automatically break hiding. Components may still reveal your location and normal perception applies. Any attack, damage or forced save ends this exception.

<details><summary>Preserved source wording — book line4410</summary>

Illusory Stealth: Casting illusion or utility spells does not break stealth.

</details>

#### Spell Disruptor

**Level 10 · selection · thief.hero.arcane-trickster.spell-disruptor**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | One enemy critically hit by your poisoned weapon | Until end next target turn | Once/round |

WIS save or suppress one observed temporary magical+AC bonus, maximum 2. No core class engine, innate trait, item destruction or blanket magic shutdown. Magical technique incurs 1 D unless cadence prevents it.

<details><summary>Preserved source wording — book line4411</summary>

Spell Disruptor: Your poisons also suppress passive magical abilities for 1 round on critical hits.

</details>

#### Magebane Blade

**Level 10 · selection · thief.hero.arcane-trickster.magebane-blade**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | One enemy in weapon reach/range | Instant | Recharge 3 |

Make one weapon attack with normal Sneak eligibility. On hit suppress one temporary spell buff of rank no greater than your spell-rank access through end next turn; higher rank remains. If none eligible, add 1d6 psychic. Magical technique 1 D.

<details><summary>Preserved source wording — book line4414</summary>

Magebane Blade: Your Sneak Attack removes 1 magical buff or deals 1d6 psychic damage if no buff is present.

</details>

#### Pocket Illusion

**Level 10 · selection · thief.hero.arcane-trickster.pocket-illusion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 RP | One attacker within 15 ft that you perceive | Triggering attack | Recharge 3 |

Before attack roll flash distracting illusion; WIS save or attack has disadvantage. No automatic miss or sustained Blindness. Magical technique 1 D, one Reaction.

<details><summary>Preserved source wording — book line4415</summary>

Pocket Illusion: Create a clone that absorbs 1 hit, then explodes in a blinding flash.

</details>

#### Flash Shift

**Level 12 · selection · thief.hero.arcane-trickster.flash-shift**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self | Until start next turn | Recharge 3 |

Teleport 15 ft to perceived unoccupied space; gain+2 AC and+2 saves until duration ends. Full solid barrier blocks destination sight. Magical technique 1 D.

<details><summary>Preserved source wording — book line4416</summary>

Flash Shift: Blink 3 tiles, avoid opportunity attacks, and gain +2 AC/Saves for 1 round.

</details>

#### Arcane Theft

**Level 14 · selection · thief.hero.arcane-trickster.arcane-theft**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One enemy within 30 ft with observed spell buff | Concentration, at most 3 rounds | 1/short rest |

Target WIS save. Failure suppress one eligible temporary rank 1–3 buff for duration and gain only its printed AC bonus (max 2), Speed bonus(max 10 ft), or resistance to one damage type; choose before save. Does not copy actions, spells, resources, summons or capstones. Magical technique 1 D.

<details><summary>Preserved source wording — book line4417</summary>

Arcane Theft: Steal a beneficial spell effect from a target and apply it to yourself.

</details>

#### Spell Snare

**Level 16 · selection · thief.hero.arcane-trickster.spell-snare**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One 5 ft square within 15 ft | Concentration, 1 minute | 1/short rest |

Place visible magical trap. First creature casting rank 1–3 spell while on/adjacent makes WIS save; failure spell fizzles after cost is paid. Trap ends either way. Higher spells unaffected and do not trigger; cannot counter legendary powers. Magical technique 1 D, maximum one trap.

<details><summary>Preserved source wording — book line4418</summary>

Spell Snare: Set a trap that triggers when a spell is cast within range, countering the spell.

</details>

### Shadowblade

#### Ambusher's Grace

**Level 10 · selection · thief.hero.shadowblade.ambusher-s-grace**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 encounter use | Self after crit or defeating hostile enemy | Until start next turn | 1/encounter |

Become Invisible; ends after your next attack, damage or forced save. You remain targetable if perceived and area effects work. No chain of unlimited untargetability from minions.

<details><summary>Preserved source wording — book line4424</summary>

Ambusher's Grace: After killing a target or critically hitting one affected by Bleed or Poison, become untargetable until your next turn.

</details>

#### Double Poison

**Level 10 · selection · thief.hero.shadowblade.double-poison**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | One additional prepared dose | One weapon coating | Until coating ends | Once per coating |

You may apply two different doses using the same coating action. First critical hit may apply both with independent saves; noncritical hit applies your chosen one. Both doses consumed, total coated attack attempts remains 2.

<details><summary>Preserved source wording — book line4425</summary>

Double Poison: Apply two poisons instead of one on critical hits.

</details>

#### Persistent Bleed

**Level 10 · selection · thief.hero.shadowblade.persistent-bleed**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One enemy hit by your weapon | Bleed extension | Once/own turn |

Refresh one of your existing Bleed effects to 2 target turns. Cannot increase its dice, duplicate instances or extend a capped poison effect beyond its poison rules.

<details><summary>Preserved source wording — book line4426</summary>

Persistent Bleed: Bleeds you cause refresh on hit instead of expiring.

</details>

#### Shadow Affinity

**Level 10 · selection · thief.hero.shadowblade.shadow-affinity**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self in dim light or darkness | While concealed | Continuous |

Advantage on Stealth. Requires a legal Hide opportunity; darkvision and other senses can still perceive you.

<details><summary>Preserved source wording — book line4427</summary>

Shadow Affinity: Gain advantage on Stealth checks in dim light or darkness.

</details>

#### Dark Step

**Level 10 · selection · thief.hero.shadowblade.dark-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self in dim light/darkness | Instant; one attack this turn | Recharge 3 |

Teleport 25 ft to visible dim/dark unoccupied space. Next weapon attack this turn has advantage. Magical technique 1 D; no travel through unseen closed rooms.

<details><summary>Preserved source wording — book line4430</summary>

Dark Step: Teleport behind any enemy within 5 tiles and gain advantage on your next attack.

</details>

#### Shadow Dive

**Level 10 · selection · thief.hero.shadowblade.shadow-dive**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self | Until end next turn or first attack | Recharge 3 |

Become Invisible. First qualifying Sneak Attack before invisibility ends adds 1d6; attacking ends invisibility after resolution. Does not grant additional Sneak uses. Magical technique 1 D.

<details><summary>Preserved source wording — book line4431</summary>

Shadow Dive: Become invisible for 1 round, gaining +1d6 Sneak Attack if used on the next turn.

</details>

#### Vein Cutter

**Level 12 · selection · thief.hero.shadowblade.vein-cutter**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | One dose | Enemy critically hit by your weapon | Until end next target turn | Once/round |

Consume prepared poison without its normal recipe effect; target CON save or Bleed 1d4 next 2 turns, Speed-10 ft and-1 next attack damage. Reapplication refreshes; source stack 3 replaced by one bounded package.

<details><summary>Preserved source wording — book line4432</summary>

Vein Cutter: On critical hit, apply Bleed, Slow, and Weakened effects that can stack up to 3 times.

</details>

#### Smoke Bomb

**Level 14 · selection · thief.hero.shadowblade.smoke-bomb**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest smoke charge | 10 ft radius centered within 30 ft | Until start of your second next turn | 1/short rest |

Opaque smoke blocks sight for all creatures; wind of 20 mph or greater disperses it. Does not Blind creatures outside or prevent area effects. No damage, poisoning or additional attack.

<details><summary>Preserved source wording — book line4433</summary>

Smoke Bomb: Create a cloud of smoke that obscures vision and grants you advantage on Stealth checks.

</details>

#### Death Blossom

**Level 17 · selection · thief.hero.shadowblade.death-blossom**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest use | Up to 3 enemies within melee reach | Instant | 1/short rest |

Make one weapon attack against each; apply Sneak Attack only to ONE qualifying hit. Source minimum 17 retained. Other per-turn damage riders retain caps; no extra Attack Action.

<details><summary>Preserved source wording — book line4434</summary>

Death Blossom: Strike all adjacent enemies, applying Sneak Attack damage to one of them (level 17).

</details>

### Blackguard

#### Exsanguinate

**Level 10 · selection · thief.hero.blackguard.exsanguinate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | Self; bleeding enemy within 15 ft | Instant | Once/own turn |

At start of your regular turn with a hostile bleeding enemy nearby you may pay 1 RP to regain S HP. No multiplying by enemy count or healing while incapacitated; not an ordinary spell or Dissonance-generating technique.

<details><summary>Preserved source wording — book line4440</summary>

Exsanguinate: Gain 1 HP per round for each bleeding target within 3 tiles.

</details>

#### Prolonged Suffering

**Level 10 · selection · thief.hero.blackguard.prolonged-suffering**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Bleed application | Up to 4 target turns | Continuous |

When you apply Bleed with base 2-turn duration it lasts 4 turns instead. Never doubles dice or stacks with another extension; subsequent refresh sets to 4, not adds 4.

<details><summary>Preserved source wording — book line4441</summary>

Prolonged Suffering: Bleeds you cause last twice as long.

</details>

#### Venom Master

**Level 10 · selection · thief.hero.blackguard.venom-master**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Enemy critically hit by poisoned weapon | Until end next target turn | Once/round |

If poison save fails target also takes-1 saves. Does not stack with Hexroot or another Venom Master; use strongest penalty.

<details><summary>Preserved source wording — book line4442</summary>

Venom Master: On critical hits, your poisons also apply -1 to all saves.

</details>

#### Exotic Toxins

**Level 10 · selection · thief.hero.blackguard.exotic-toxins**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Downtime | One adventure specimen; poison kit | One known exotic recipe | Permanent knowledge | One attempt/specimen |

Use engine DC 15 INT+PB research. Director assigns it an existing Tier-appropriate poison profile with fictional name/type, no stronger numbers. No harvesting captives or arbitrary monster abilities for unlimited doses.

<details><summary>Preserved source wording — book line4443</summary>

Exotic Toxins: You can use monster-only venoms if harvested from bestiary bosses.

</details>

#### Crippling Lash

**Level 10 · selection · thief.hero.blackguard.crippling-lash**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One enemy in melee reach | Until end next target turn | Recharge 2 |

Make one weapon attack. If it qualifies for Sneak, CON save or Speed-10 ft and-1 damage on next weapon hit for duration. No extra Sneak packet.

<details><summary>Preserved source wording — book line4446</summary>

Crippling Lash: Your Sneak Attack slows the target and reduces their damage by -1 for 2 rounds.

</details>

#### Toxic Shiv

**Level 10 · selection · thief.hero.blackguard.toxic-shiv**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | One prepared dose | One weapon touched | 1 minute or 2 attempts | At will while doses remain |

Apply any known prepared poison, including exotic profile, using normal coating rules. You may change an existing coating by discarding it. This is not an extra attack and refunds no discarded dose.

<details><summary>Preserved source wording — book line4447</summary>

Toxic Shiv: As a bonus action, apply any poison from your inventory with no check or delay.

</details>

#### Vile Tactics

**Level 12 · selection · thief.hero.blackguard.vile-tactics**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One weapon hit against Bleeding/Poisoned/Crippled enemy | Instant | Once/own turn |

Add 1d6 weapon damage. Separate from Sneak but neither repeats on poison ticks nor copied attacks; multiple conditions do not multiply the bonus.

<details><summary>Preserved source wording — book line4448</summary>

Vile Tactics: Deal +1d6 damage against Bleeding, Poisoned, or Frightened enemies.

</details>

#### Terror Strike

**Level 14 · selection · thief.hero.blackguard.terror-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest use | One enemy in weapon reach; up to 2 enemies within 10 ft of it | Until end next target turn | 1/short rest |

Weapon attack; hit normal damage and secondary enemies WIS save or Frightened of you for duration. Sneak eligibility normal. Immune creatures remain immune; no automatic fleeing Action.

<details><summary>Preserved source wording — book line4449</summary>

Terror Strike: Cause nearby enemies to become frightened, imposing disadvantage on their attacks.

</details>

#### Unseen Hand

**Level 20 · automatic · thief.hero.blackguard.unseen-hand**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 long-rest use | Self while Invisible | Current turn | 1/long rest; automatic Blackguard Final |

After taking an Action while Invisible gain one extra Action to make one weapon attack or use a nonmagical Thief skill. Attacking ends invisibility normally. No second Sneak Attack, second extra Action, Bonus Action, Reaction or self-reset.

<details><summary>Preserved source wording — book line4450</summary>

Unseen Hand: Once per round, take an action while invisible (attack or move) (level 20).

</details>

### Arcane Trickster

#### Master of the Unseen

**Level 20 · automatic · thief.supplement.arcane-trickster.master-of-the-unseen**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 long-rest use | Self; Arcane Trickster only | Until end current turn | 1/long rest; automatic Hero Final |

New playtest finale for paths without a source Final. Become Invisible until after your next attack and move up to half Speed without opportunity attacks. Your next qualifying Sneak Attack this turn adds S d6 force (Arcane Trickster) or piercing (Shadowblade), and ignores resistance to those added dice only. It grants no second Sneak Attack or free Action.

Prerequisite: Thief 20; Arcane Trickster

Source status: **new playtest completion**, not recovered historical wording.

### Shadowblade

#### Master of the Unseen

**Level 20 · automatic · thief.supplement.shadowblade.master-of-the-unseen**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 long-rest use | Self; Shadowblade only | Until end current turn | 1/long rest; automatic Hero Final |

New playtest finale for paths without a source Final. Become Invisible until after your next attack and move up to half Speed without opportunity attacks. Your next qualifying Sneak Attack this turn adds S d6 force (Arcane Trickster) or piercing (Shadowblade), and ignores resistance to those added dice only. It grants no second Sneak Attack or free Action.

Prerequisite: Thief 20; Shadowblade

Source status: **new playtest completion**, not recovered historical wording.

## Source appendix and open balance questions

The complete original Thief book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/thief.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Is the broad Sneak qualification too reliable compared with maneuvering?
- Can players track two coated attempts and poison durations easily?
- Do TierIII control poisons remain useful under the shared denial limit?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
