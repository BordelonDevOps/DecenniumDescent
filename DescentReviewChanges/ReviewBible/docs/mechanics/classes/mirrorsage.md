# Mirrorsage — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/mirrorsage.json) · [Normalized card data](../../../data/public/class_playtests/mirrorsage.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Intelligence
- Secondary Attributes: Wisdom, Charisma
- Hit Points: Medium (8 + Constitution modifier at 1st level, 1d8 per level thereafter)
- Armor Proficiency: Light armor
- Weapon Proficiency: Simple weapons, short swords, hand crossbows
- Tool Proficiency: Calligrapher's supplies

Intelligence is the class ability; use d8 Hit Die from the detailed book, recording the older runtime d6 as superseded for this draft. You begin with 3 empty Echo Slots. Expansion II raises ordinary capacity 5; Sacred/Floating memory features may add one restricted slot, but total concurrent stored Echoes never exceeds 6. Slots are storage, not spell slots. Releasing normally empties that record. Rest restores RP, not spent Echoes. Starting a new encounter does not duplicate the archive.

Mirrorbind is an Action, once per encounter, against a creature within 60 ft whose eligible ability you saw resolve since the start of your previous turn. Target must have INT 6 or lower, not be a boss or possess unique/legendary status unless an encounter script explicitly permits copying. It makes WIS save versus class DC; failure captures one witnessed ability into an empty slot. No copying from allies, your companions, another copy, a corpse, a recharge-limited legendary power or an at-will source that itself restores resources. You can voluntarily erase a slot without an action on your turn, permanently losing its record.

Record source creature/name, witnessed ability, category, damage type, allowed rank, capture encounter and whether first release has occurred. For this pilot, capture copies the observed role into ONE bounded profile: Strike=one target 60 ft class spell attack S d8 observed damage type; Burst=up to 3 enemies in 10 ft radius within 30 ft DEX save S d6, half on success; Mend=one living ally 30 ft S d6+M HP; Ward=one ally 30 ft S d6+M temporary HP for 1 minute; Hindrance=one enemy 30 ft WIS save or Speed-10 ft and no Reactions until end its next turn. Choose only a profile actually expressed by the observed source; physical attack cannot become healing. Rank is max(1, ceil(source challenge rating/2)); if source lacks a rating the Director assigns a rank before the encounter, not after seeing a desirable ability. Rank cannot exceed your Mirrorsage learnable rank; no copying character levels from a creature. Damage/targets/control are capped by these profiles, not source boss dice.

Echo Release costs the Core V 2 RP cost of the recorded rank, minimum 2, consumes its record and counts as a spell for Dissonance and Refrain. Spell attack/DC use your own stats. First release of a newly captured record ignores Refrain addition only; base strain remains. Any preserved subsequent release uses ordinary repeated-spell strain. All released Echoes, pet replays, fusions and reflections share ONE release action per round; a specifically combined package counts once but pays for every component and has its printed damage cap. Copies cannot create resources or recursive Echoes.

One Mirror Beast OR Reflective Companion, never both. Mirror Beast uses standard companion stats, initially copies appearance only, and costs a Bonus Action to command. You may command it to make its normal attack OR originate your round's Echo Release from its position, paying RP and consuming the record normally; not both. You still supply an Action for release unless a feature specifically changes that action cost. A shifted appearance grants no extra actions/stats. Destroying/dismissing it grants no capture, corpse, XP or recovery. Charm Bind is 1/long rest, 3 rounds, concentration, INT 6-or-lower target WIS save and repeat at each turn end/when harmed by your side; never a player character or boss without explicit encounter permission. A charmed companion uses its own ordinary attack with damage capped at standard companion S d6; unique spells/powers remain unavailable.

Focus Point is a separate resource: when Mimicry Focus is known, receive 1 at encounter start, maximum 1, lost at encounter end. It can modify one Echo without generating another release, recapture or resource refund. No stacking damage doublings; use the printed modest die/range boost. Healing/support copies always consume RP and cannot restore RP or duplicate limited-use features.

Standard acquisition applies; baseline Mirrorbind, Echo Release and summon procedure become usable by selecting their cards. Echo Channeling and Mirrorcall are upgrades, not duplicate mandatory unlocks. The contradiction between source initial 3 slots and Expansion I 2→3 is reconciled as an archive-safety upgrade below. Perfect Reflection automatic 9, Hero choice 10, corresponding Final 20. The finale does not override copy eligibility or the shared release cap.

**Protected source interface:** The first replay of a newly Mirrorbound Echo ignores Refrain Dissonance; repeating the same stored Echo builds Refrain normally.

## Advancement and resources

RP authority: Direct Core Systems V2 table. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 2 | 1 | Choose 4 Base; at least 2 active |
| 2 | Base | 3 | 1 | Choose 2 Base |
| 3 | Arch | 5 | 1 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 7 | 2 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 9 | 2 | Choose 1 Arch |
| 6 | Arch | 11 | 2 | Choose 1 Base/Arch |
| 7 | Arch | 14 | 3 | Choose 1 Arch |
| 8 | Arch | 17 | 3 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 20 | 3 | Choose 1 Arch; automatic: Perfect Reflection |
| 10 | Hero | 23 | 4 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 26 | 4 | Choose 1 Base/Arch |
| 12 | Hero | 29 | 4 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 32 | 5 | Choose 1 Base/Arch |
| 14 | Hero | 35 | 5 | Choose 1 Hero |
| 15 | Hero | 38 | 5 | Choose 1 Base/Arch |
| 16 | Hero | 41 | 6 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 44 | 6 | Choose 1 Base/Arch |
| 18 | Hero | 47 | 6 | Choose 1 Hero |
| 19 | Hero | 50 | 7 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 54 | 7 | No ordinary selection; automatic: Radiant Archive (Light Weaver), Reflected Repertoire (Mirror Mage), Fractured Dominion (Shattered One) |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Mirrorsage 5, INT 16, PB 3, S 2, M 3, RP 9, three slots; know Mirrorbind, Echo Release, Mirror Beast Summon, Reflective Shield at 1, Beast Instinct and Reflective Pulse at 2; Mimicry Focus and Reflective Analysis at 3. Begin with Focus 1.
2. Turn 1: witness an eligible serpent's rank 1 poison cone, then Mirrorbind on your turn. It fails WIS save; store Burst/poison/rank 1. RP stays 9; one encounter capture spent.
3. Turn 2: Echo Release is Action and 2 RP, RP 9→7; empty the stored slot. Up to 3 enemies roll DEX against 14 for 2d6 poison, half on success. First release ignores Refrain but still adds 1 base Dissonance.
4. Turn 3: without another stored Echo you cannot simply release again. Use a weapon or ordinary legal spell. A short rest restores RP but not the consumed record.
5. Alternative turn 2: summon Mirror Beast for 2 RP, leaving RP 7 and the Echo stored. On turn 3 use Action Echo Release plus Bonus Action command to originate it from the Beast, pay 2 RP, ending 5; the Beast cannot also attack that round.
6. A failed Mirrorbind capture still expends its encounter attempt. Beast Instinct's limited retry may help if known; a boss excluded by eligibility cannot be made eligible with a high roll.

## Base cards

#### Echo Channeling

**Level 1 · selection · mirrorsage.base.echo-channeling**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your own Echo Release | Instant | Once/short rest |

After releasing an Echo, add M to one target's damage or healing. No modifier to resource effects; this upgrade does not grant another release or repeat the source's rider.

<details><summary>Preserved source wording — book line3067</summary>

Echo Channeling: Cast a stored Echo ability. Consumes a slot.

</details>

#### Mirrorcall

**Level 1 · selection · mirrorsage.base.mirrorcall**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Mirror Beast | While it exists | Continuous |

Beast gains+M maximum/current HP when summoned and+5 ft Speed. Echo Release or Mirror Beast Summon already provides its base procedure; this is an optional enhancement, not a second required unlock.

<details><summary>Preserved source wording — book line3068</summary>

Mirrorcall: Summon a Mirror Beast that mimics one stored Echo ability.

</details>

#### Echo Slot Expansion I

**Level 1 · selection · mirrorsage.base.echo-slot-expansion-i**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One newly bound record | Until your next long rest | 1/long rest |

If an ordinary slot is full, replace one record while preserving its name/profile in an inert backup. Once before next long rest, after a slot empties, restore that backup without an Action. Total usable records remain at your capacity; backup cannot be cast directly or backed up again. An inert backup counts toward the absolute six-record archive ceiling. A backup cannot be created if usable records plus inert backups would exceed six.

<details><summary>Preserved source wording — book line3069</summary>

Echo Slot Expansion I: Increase slots from 2 → 3.

</details>

#### Reflective Pulse

**Level 1 · selection · mirrorsage.base.reflective-pulse**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | Attacker within 30 ft after its first hit this round damages you | Instant | Once/round |

Deal psychic damage equal to min(M, damage actually taken). This cannot critically hit, trigger another reflection, generate resources or prevent the original damage. No effect if you take 0.

<details><summary>Preserved source wording — book line3070</summary>

Reflective Pulse: First hit you take each round returns 10% damage.

</details>

#### Beast Instinct

**Level 1 · selection · mirrorsage.base.beast-instinct**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 short-rest use | A failed Mirrorbind against eligible INT 6-or-lower source | Immediate retry | 1/short rest |

Force that target to reroll its successful save; use the second result. Eligibility, line of effect and an empty slot still required. Does not create a second captured record or a new encounter attempt.

<details><summary>Preserved source wording — book line3071</summary>

Beast Instinct: +10% chance to capture Echoes from INT ≤ 6 creatures.

</details>

#### Mirrorbind

**Level 1 · selection · mirrorsage.base.mirrorbind**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0; encounter attempt | One eligible witnessed creature within 60 ft | Stored until released/erased | 1/encounter |

Apply the engine's exact capture procedure: WIS save or store a bounded profile for the witnessed ability. State category/rank before save. Success prevents capture but consumes attempt; no target can be mirrored outside eligibility restrictions.

<details><summary>Preserved source wording — book line3074</summary>

Mirrorbind: Attempt to capture an ability you've just witnessed, storing it in an Echo Slot if successful.

</details>

#### Echo Release

**Level 1 · selection · mirrorsage.base.echo-release**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Recorded rank RP cost; consume 1 Echo | Profile target/range | Profile duration | One release action/round |

Resolve the stored Strike/Burst/Mend/Ward/Hindrance profile, using current S and INT. Pay before release; empty slot even if resisted. First release ignores only Refrain addition. No original source extra actions/resources/procs.

<details><summary>Preserved source wording — book line3075</summary>

Echo Release: Cast a stored Echo ability, consuming the slot.

</details>

#### Mirror Beast Summon

**Level 1 · selection · mirrorsage.base.mirror-beast-summon**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | One empty space within 15 ft | 1 minute | Recharge 3 |

Summon one standard Mirror Beast; replaces any prior Beast/Reflective Companion. Choose appearance of a stored source. It attacks only on Bonus Action command or originates your paid release with Action+command, never both. No copied anatomy, regeneration or immortality.

<details><summary>Preserved source wording — book line3076</summary>

Mirror Beast Summon: Call forth a Mirror Beast that can use one of your stored Echo abilities.

</details>

#### Charm Creature

**Level 1 · selection · mirrorsage.base.charm-creature**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP; 1 long-rest use | One eligible INT 6-or-lower creature within 30 ft | Concentration, at most 3 rounds | 1/long rest |

WIS save or become Reflective Companion under engine restrictions. It repeats save at turn end and when harmed by your side. Replaces Mirror Beast; on end original disposition returns. Requires no suicidal orders; cannot force beliefs or permanently enslave.

<details><summary>Preserved source wording — book line3077</summary>

Charm Creature: Attempt to temporarily charm a low-intelligence creature to fight alongside you.

</details>

#### Reflective Shield

**Level 1 · selection · mirrorsage.base.reflective-shield**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 RP | Self when hit by an attack from within 60 ft | This attack | Recharge 2 |

Gain+2 AC against triggering attack, potentially making it miss. If it misses, attacker takes M force damage. This is bounded retaliation, not copying the original attack; cannot trigger another reflection or capture.

<details><summary>Preserved source wording — book line3078</summary>

Reflective Shield: Create a brief defensive barrier that has a chance to reflect the next attack back at the attacker.

</details>

## Arch cards

#### Advanced Mirrorcall

**Level 3 · selection · mirrorsage.arch.advanced-mirrorcall**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Mirror Beast | While summoned | Once/encounter |

You may change Beast appearance to another stored source as a Bonus Action without resummoning or restoring HP. It gains either+10 ft swim or climb Speed until it ends. No new release, attack or capture.

<details><summary>Preserved source wording — book line3084</summary>

Advanced Mirrorcall: Mirror Beast can now shift once per fight into a new form based on a second Echo.

</details>

#### Echo Slot Expansion II

**Level 3 · selection · mirrorsage.arch.echo-slot-expansion-ii**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your archive | While known | Continuous |

Ordinary Echo storage capacity becomes 5, replacing 3. Restricted extra slots still obey total 6. New slots are empty; the feature creates no Echo records or spell access.

<details><summary>Preserved source wording — book line3085</summary>

Echo Slot Expansion II: Max Echo Slots: 5

</details>

#### Dual Echo Cast

**Level 5 · selection · mirrorsage.arch.dual-echo-cast**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | RP for each of 2 Echoes; consume both | One target per eligible profile | Immediate; riders at most 1 turn | Recharge 3 |

Release two records captured from different creatures as ONE combined release. Each deals/heals half its profile's rolled amount, round once per component. At most one Hindrance rider; no duplicated resources or additional release this round.

<details><summary>Preserved source wording — book line3086</summary>

Dual Echo Cast: Spend 2 Echoes in one turn; must be from different creatures.

</details>

#### Mimicry Focus

**Level 3 · selection · mirrorsage.arch.mimicry-focus**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Encounter | Once/encounter |

At genuine encounter start gain 1 Focus Point, cap 1; any previous point is replaced. Spend on Focus Channel or pay 1 Focus during a release to add 1d6 to one damage/healing target. No point generation from staged combat.

<details><summary>Preserved source wording — book line3087</summary>

Mimicry Focus: Gain +1 Focus Point per battle. Can spend Focus to empower Echoes (double duration/damage).

</details>

#### Mirror Shell

**Level 7 · selection · mirrorsage.arch.mirror-shell**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 3 RP; 1 long-rest use | A hostile spell targeting only you within 60 ft | This spell | 1/long rest |

After a successful save against the spell or after its spell attack misses, choose its caster; it makes WIS save or takes S d8 force. Original damage/control follow normal results. No copying arbitrary spell text or redirecting an area spell.

<details><summary>Preserved source wording — book line3088</summary>

Mirror Shell: Once per long rest, reflect the first ability cast at you.

</details>

#### Perfect Reflection

**Level 9 · automatic · mirrorsage.arch.perfect-reflection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 4 RP; 1 long-rest use | Creature within 60 ft whose observed ability targets you | This ability | 1/long rest |

Reduce triggering damage to you by(S+1)d8+M, minimum 0. If any is prevented, source makes WIS save or takes that prevented amount as force, maximum 30. This is your release action for the round; no reflected conditions or legendary powers. Cannot recursively reflect.

<details><summary>Preserved source wording — book line3089</summary>

Capstone – Perfect Reflection: Reflect any observed ability (spell, breath, strike) back at the caster for full effect (1/day).

</details>

#### Echo Fusion

**Level 3 · selection · mirrorsage.arch.echo-fusion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | RP for 2 Echoes; consume both | Up to 2 profile targets within 30 ft | Instant or 1 turn | Recharge 3 |

Choose two stored profiles. Resolve one at full dice and the other at half dice to one target each. Only one may be healing; at most one Hindrance rider. Counts as one combined release and cannot receive Dual Echo Cast simultaneously.

<details><summary>Preserved source wording — book line3092</summary>

Echo Fusion: Temporarily combine two stored Echoes to create a hybrid ability with properties of both.

</details>

#### Mirror Shift

**Level 3 · selection · mirrorsage.arch.mirror-shift**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP | Your Mirror Beast within 60 ft | Remaining summon duration | Recharge 2 |

Switch its appearance to a stored source and choose swim 30 ft or climb 30 ft until next shift. Restore no HP or attacks; no flight, incorporeality or copied creature special actions. Does not release or consume the Echo.

<details><summary>Preserved source wording — book line3093</summary>

Mirror Shift: Command your Mirror Beast to change form, adopting a different stored Echo ability.

</details>

#### Focus Channel

**Level 3 · selection · mirrorsage.arch.focus-channel**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 Focus | Self; next release this turn | This turn | Once/encounter via Focus cap |

Next Echo release adds 1d6 to one damage/healing amount OR adds 30 ft range, chosen now. Cannot multiply duration, bypass concentration, add targets or override release caps. If no release occurs this turn the point remains spent.

<details><summary>Preserved source wording — book line3094</summary>

Focus Channel: Spend a Focus Point to significantly enhance your next Echo cast or Mirror Beast ability.

</details>

#### Reflective Analysis

**Level 3 · selection · mirrorsage.arch.reflective-analysis**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One observed creature within 60 ft | Until end next turn | Recharge 2 |

Learn whether it is capture-eligible and one visible ability's bounded profile/rank before attempting. The next Mirrorbind save it makes against you has-1. Nonstacking; does not reveal private thoughts or permit boss copying.

<details><summary>Preserved source wording — book line3095</summary>

Reflective Analysis: Study a creature to gain insight into its abilities and weaknesses, increasing your chance to successfully bind its Echoes.

</details>

#### Mirror Dimension

**Level 7 · selection · mirrorsage.arch.mirror-dimension**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Fixed 10 ft-radius zone within 30 ft; up to 3 enemies | Concentration, 3 of your turns | Recharge 4 |

On entry activation and each of next 2 turns with Bonus Action maintenance, selected enemies make WIS save; failure gives disadvantage on next attack before your next turn. Inside, your Mirrorbind range extends 30 ft. No additional capture attempts/releases or pocket escape route.

<details><summary>Preserved source wording — book line3096</summary>

Mirror Dimension: Create a small pocket dimension of reflective surfaces that confuses enemies and enhances your mimicry abilities.

</details>

## Hero cards

### Light Weaver

#### Blessed Copy

**Level 10 · selection · mirrorsage.hero.light-weaver.blessed-copy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 1 additional RP | Second living ally within 15 ft of original Mend/Ward target | Same healing/shield duration | Once/round |

When releasing Mend or Ward, pay 1 extra RP to give a second ally half the rolled amount, rounded once. This is within the same release, no new source or healing proc. No duplication of concentration or resources.

<details><summary>Preserved source wording — book line3105</summary>

Blessed Copy: Echoed heals or buffs also affect a second ally.

</details>

#### Luminant Bond

**Level 10 · selection · mirrorsage.hero.light-weaver.luminant-bond**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Allies/enemies within 10 ft of your Beast/Companion | While companion exists | Continuous |

Allies gain+1 to WIS saves. Invisible enemies in aura shed faint outlines and cannot gain advantage solely from invisibility, but concealment/cover still apply. This grants neither full True Sight nor targeting through walls.

<details><summary>Preserved source wording — book line3106</summary>

Luminant Bond: Charmed/Beast emits aura that reveals invisible and grants +5% saves.

</details>

#### Sacred Echo Slot

**Level 10 · selection · mirrorsage.hero.light-weaver.sacred-echo-slot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One restricted archive slot | While known | Continuous |

Add one slot usable only for Mend or Ward, total storage cap 6. If already at 6, designate one existing slot sacred instead; once/short rest its release costs 1 less RP, minimum 1. No duplicate slot or free record.

<details><summary>Preserved source wording — book line3107</summary>

Sacred Echo Slot: +1 additional slot for healing/support abilities.

</details>

#### Radiant Archive

**Level 20 · automatic · mirrorsage.hero.light-weaver.radiant-archive**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | RP for 3 support Echoes; consume all 3; 1 long-rest use | Up to 3 legal allies within 30 ft | Instant/shield 1 minute | 1/long rest |

Release three stored Mend/Ward records as ONE package; assign each to one ally. No ally receives more than two components and temporary HP never stack. All costs paid; no extra release or resurrection. Missing records cannot be invented.

<details><summary>Preserved source wording — book line3108</summary>

Final – Radiant Archive: Cast 3 stored divine Echoes at once (once/day).

</details>

#### Divine Reflection

**Level 10 · selection · mirrorsage.hero.light-weaver.divine-reflection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 2 RP; 1 long-rest use | Willing allied caster within 30 ft just used an eligible healing/protection spell | Store until spent | 1/long rest |

Capture a Mend or Ward profile of rank at most your learnable rank into empty slot. This explicit exception permits an allied source but excludes resurrection/resource/action generation. No extra captured use for the ally and no copying a copy.

<details><summary>Preserved source wording — book line3111</summary>

Divine Reflection: Capture and enhance beneficial abilities, increasing their healing or protective power.

</details>

#### Radiant Mirror Beast

**Level 10 · selection · mirrorsage.hero.light-weaver.radiant-mirror-beast**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Empty space within 15 ft | Concentration, 3 of your turns | Recharge 4 |

Summon radiant standard Beast. Bonus Action command chooses normal attack or healing S d4 to one living ally within 5 ft, paying 1 RP per heal. It may instead originate your paid Echo release under common limits. Cannot perform two options in one round.

<details><summary>Preserved source wording — book line3112</summary>

Radiant Mirror Beast: Summon a Mirror Beast infused with divine energy, capable of healing allies and revealing hidden threats.

</details>

#### Blessing Echo

**Level 12 · selection · mirrorsage.hero.light-weaver.blessing-echo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Recorded RP cost+1; consume offensive Echo | One living ally within 30 ft | Instant or 1 minute shield | Recharge 3 |

Convert a stored Strike/Burst record to Mend/Ward for this release, chosen on activation; heal S d6+M or grant same temporary HP. This explicit conversion cannot also deal offensive damage or copy a condition.

<details><summary>Preserved source wording — book line3113</summary>

Blessing Echo: Transform a captured offensive Echo into a beneficial effect that can heal or protect allies.

</details>

#### Light Binding

**Level 14 · selection · mirrorsage.hero.light-weaver.light-binding**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Up to 2 creatures within 30 ft | Until end your next turn | Recharge 3 |

Choose mode: enemies make STR save or Restrained; they repeat save at turn end. OR up to 2 allies gain S d6+M temporary HP. No mixed modes; bonds are magical and not permanent objects.

<details><summary>Preserved source wording — book line3114</summary>

Light Binding: Create bonds of radiant energy that can restrain enemies or create protective barriers for allies.

</details>

#### Purifying Reflection

**Level 16 · selection · mirrorsage.hero.light-weaver.purifying-reflection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 5 RP; 1 long-rest use | Ally within 30 ft failing save against Charmed/Frightened/Poisoned | Instant | 1/long rest |

Ally rerolls that save with advantage; use new result. If it succeeds, it regains S d6 HP. No arbitrary curse or death reversal; costs remain if it fails. This is not a captured Echo and creates no record.

<details><summary>Preserved source wording — book line3115</summary>

Purifying Reflection: Reflect and purify harmful effects, potentially converting them into healing or beneficial effects.

</details>

### Mirror Mage

#### Mirror Double

**Level 10 · selection · mirrorsage.hero.mirror-mage.mirror-double**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | One damage Echo you released this turn | Resolves start next turn | Recharge 3 |

Create one illusory double; it repeats half the unmodified immediate damage dice to one original enemy still within 30 ft, without roll or conditions. Declare Mirror Double before the current turn ends; its pending copy remains part of this turn’s one release package and does not consume a later release allowance. Only one pending copy; cannot copy copies/healing.

<details><summary>Preserved source wording — book line3121</summary>

Mirror Double: Create a copy of yourself for 1 turn. It casts your last Echo at 50% power.

</details>

#### Fused Echo

**Level 10 · selection · mirrorsage.hero.mirror-mage.fused-echo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 1 long-rest use | One use of Echo Fusion | This release | 1/long rest |

Increase Fusion's half-strength component to full dice. Still two sources, full RP, one combined release and normal target limits. This never adds a third component or doubles resources, control duration or already copied damage.

<details><summary>Preserved source wording — book line3122</summary>

Fused Echo: Combine two Echoes to create a custom hybrid. Once per long rest.

</details>

#### Floating Memory Slot

**Level 10 · selection · mirrorsage.hero.mirror-mage.floating-memory-slot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One temporary archive slot | Until encounter end | Continuous during encounter |

Capacity becomes 6 if below 6; temporary slot is erased at encounter end. If already 6, choose one existing slot instead and its release gains+5 ft range. Never exceed 6 or preserve a seventh via a backup.

<details><summary>Preserved source wording — book line3123</summary>

Floating Memory Slot: Temporarily store a 6th Echo. Auto-erases after combat.

</details>

#### Reflected Repertoire

**Level 20 · automatic · mirrorsage.hero.mirror-mage.reflected-repertoire**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 8 RP; 1 long-rest use | Up to 3 records currently in your archive | Next 3 releases within 1 minute | 1/long rest |

Mark up to 3 distinct existing records. Each one's next release keeps its record instead of consuming it; still pay release RP and obey one release/round. No restoration of already empty slots, no invented records, no reuse-preservation after its marked use.

<details><summary>Preserved source wording — book line3124</summary>

Final – Reflected Repertoire: Reset all Echo slots. Next 3 Echoes cast without consuming slots.

</details>

#### Echo Manipulation

**Level 10 · selection · mirrorsage.hero.mirror-mage.echo-manipulation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP | One stored Echo | Next release before end next turn | Recharge 2 |

Choose +30 ft range OR change damage to acid/cold/fire/lightning/thunder. No change to category, rank, targets, save ability, copied conditions or eligibility. Nonstacking modifications; record reverts after release/expiry.

<details><summary>Preserved source wording — book line3127</summary>

Echo Manipulation: Modify a stored Echo, changing its element, range, or effect.

</details>

#### Mirror Image

**Level 10 · selection · mirrorsage.hero.mirror-mage.mirror-image**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Self | Concentration, 3 of your turns | Recharge 3 |

Create two decoys. When an attack hits you, use Reaction to erase one and impose disadvantage on that attack's reroll. Decoys do not cast, attack, intercept area damage or create Echo records. At most one decoy erased per round.

<details><summary>Preserved source wording — book line3128</summary>

Mirror Image: Create multiple illusory duplicates of yourself that can confuse enemies and potentially cast Echo abilities.

</details>

#### Prismatic Reflection

**Level 12 · selection · mirrorsage.hero.mirror-mage.prismatic-reflection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Recorded RP cost+2; consume Strike Echo | Up to 3 enemies within 30 ft | Instant | Recharge 3 |

Replace Strike's attack with separate spell attacks; divide its S d8 dice among targets with at least 1 die each. At S 2 only 2 targets. Total dice do not increase. One combined release; no full-damage copy per target.

<details><summary>Preserved source wording — book line3129</summary>

Prismatic Reflection: Split a single-target Echo into multiple weaker versions that can affect several targets.

</details>

#### Echo Preservation

**Level 14 · selection · mirrorsage.hero.mirror-mage.echo-preservation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 2 RP; 1 short-rest use | One Echo you are about to release | This use | 1/short rest |

Preserve that record after release instead of consuming it. Pay normal RP plus 2 and obey all limits. Does not stack with Repertoire or preserve more records in Fusion; choose one. Its next release is no longer a first replay.

<details><summary>Preserved source wording — book line3130</summary>

Echo Preservation: Prevent an Echo from being consumed when cast, allowing it to be used again.

</details>

#### Reality Fracture

**Level 16 · selection · mirrorsage.hero.mirror-mage.reality-fracture**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 6 RP; 1 long-rest use | Fixed 10 ft-radius zone within 30 ft | Concentration, 3 of your turns | 1/long rest |

While you stand inside, once/turn add 1d6 to one Echo damage/healing amount or impose-1 on one target's Echo save. Choose before resolving. No free releases, random recasts, resource refunds or extra targets.

<details><summary>Preserved source wording — book line3131</summary>

Reality Fracture: Create a zone where Echo abilities are enhanced and have a chance to trigger additional effects.

</details>

### Shattered One

#### Corrupted Mirrorcall

**Level 10 · selection · mirrorsage.hero.shattered-one.corrupted-mirrorcall**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Beast on summoning | Summon duration | Once/summon |

Roll d2:1 Ember grants its one commanded attack+1d4 fire; 2 Barbs grants+1d4 piercing. Extra dice apply once/round only. Mutation grants no aura damage, poison supply, resource gain or separate creature.

<details><summary>Preserved source wording — book line3137</summary>

Corrupted Mirrorcall: Mirror Beast gains a random mutation (e.g., Burn Aura, Bleed Burst).

</details>

#### Shatterbind

**Level 10 · selection · mirrorsage.hero.shattered-one.shatterbind**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Record captured from undead/demon/aberration | That release | Once/round |

You may change its damage type to necrotic or psychic on release. Category/eligibility/rank stay unchanged; high-INT undead and bosses remain excluded unless an encounter explicitly permits them.

<details><summary>Preserved source wording — book line3138</summary>

Shatterbind: Echoes from undead/demons/aberrations gain necrotic or psychic damage tags.

</details>

#### Fractured Echo

**Level 10 · selection · mirrorsage.hero.shattered-one.fractured-echo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 2 RP; 1 short-rest use | One damage Echo just released | Start next turn | 1/short rest |

Create one pending half-dice repeat against one original target still within 30 ft. No conditions, procs, crits, resource changes or additional capture. Replaces any pending Mirror Double/Fractured copy. Deterministic limited use replaces the old random 25% trigger.

<details><summary>Preserved source wording — book line3139</summary>

Fractured Echo: 25% chance each Echo triggers again randomly the next round.

</details>

#### Fractured Dominion

**Level 20 · automatic · mirrorsage.hero.shattered-one.fractured-dominion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 8 RP; 1 long-rest use | Self | 2 of your turns | 1/long rest |

Your first damage release on each of these 2 turns adds one half-dice component against a DIFFERENT enemy within 10 ft of an original target. Same package and shared copy cap; excludes healing/control. Never recursively copies a copy or adds a release action.

<details><summary>Preserved source wording — book line3140</summary>

Final – Fractured Dominion: For 2 turns, every Echo cast also generates a Glitched Clone Echo that strikes a nearby enemy.

</details>

#### Corrupt Echo

**Level 10 · selection · mirrorsage.hero.shattered-one.corrupt-echo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Your next damage Echo | Before end current turn | Recharge 3 |

Add 1d6 necrotic to one target on release OR force one damaged target to make WIS save or lose Reactions until end its next turn. No double rider or additional release. Added die is excluded from later copies.

<details><summary>Preserved source wording — book line3143</summary>

Corrupt Echo: Twist a captured ability into a more destructive or debilitating version.

</details>

#### Shattered Mirror Beast

**Level 10 · selection · mirrorsage.hero.shattered-one.shattered-mirror-beast**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Empty space within 15 ft | Concentration, 3 of your turns | Recharge 4 |

Summon standard corrupted Beast. On commanded hit add 1d6 necrotic once/round; after that hit, each other creature within 5 ft of Beast, including allies, takes 1 psychic damage. This splash has no procs and cannot trigger another splash. Normal companion cap applies.

<details><summary>Preserved source wording — book line3144</summary>

Shattered Mirror Beast: Summon a corrupted Mirror Beast with unstable, mutated abilities that can harm both enemies and allies.

</details>

#### Echo Leech

**Level 12 · selection · mirrorsage.hero.shattered-one.echo-leech**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | Self after direct Echo damages a hostile creature | Instant | Once/round |

Pay 1 RP to regain HP equal to min(M, actual damage dealt to one target). Copies, Do Ts and companion attacks do not trigger it. Healing has no secondary healing/resource procs; no damage means no heal.

<details><summary>Preserved source wording — book line3145</summary>

Echo Leech: Drain life force from a target when casting certain Echo abilities, healing yourself.

</details>

#### Fractured Reality

**Level 14 · selection · mirrorsage.hero.shattered-one.fractured-reality**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP | Fixed 10 ft-radius zone within 30 ft; up to 3 enemies/pulse | Concentration, 3 of your turns | Recharge 4 |

On start and each later Bonus Action+1 RP pulse, WIS save: S d6 psychic, half on success. Failure also loses Reactions until start your next turn. At most 3 pulses. Zone is not an Echo source or resource generator.

<details><summary>Preserved source wording — book line3146</summary>

Fractured Reality: Create a zone of broken reflections that confuses and damages creatures within it.

</details>

#### Mind Shatter

**Level 16 · selection · mirrorsage.hero.shattered-one.mind-shatter**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 6 RP; consume 1 offensive Echo; 1 long-rest use | One enemy within 60 ft | Instant; control until end next turn | 1/long rest |

WIS save: (S+2)d8 psychic, half on success. Failure imposes disadvantage on next attack; failure by 10 also Stunned until end its next turn within denial cap. No permanent mental illness or control of the player's beliefs.

<details><summary>Preserved source wording — book line3147</summary>

Mind Shatter: Use corrupted Echo energy to attack a creature's mind, potentially causing confusion or temporary insanity.

</details>

## Source appendix and open balance questions

The complete original Mirrorsage book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/mirrorsage.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Is the initial capture dependency enjoyable with an empty archive?
- Are bounded profiles diverse enough without importing boss actions?
- Does the shared release/companion budget keep fusions and clones manageable?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
