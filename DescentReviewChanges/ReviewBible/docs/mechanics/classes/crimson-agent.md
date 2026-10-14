# Crimson Agent — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/crimson-agent.json) · [Normalized card data](../../../data/public/class_playtests/crimson-agent.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Dexterity
- Secondary Attributes: Intelligence, Constitution
- Hit Points: Medium (8 + Constitution modifier at 1st level, 1d8 per level thereafter)
- Armor Proficiency: Light armor
- Weapon Proficiency: Simple weapons, finesse weapons, thrown weapons
- Tool Proficiency: Poisoner's kit, thieves' tools

Blood Gauge (BG) starts and ends each encounter at 0, capacity 3; Spill Control raises capacity 6 while known. Once on your own regular turn, a weapon attack that damages a hostile living creature grants 1 BG. Hemorrhage Slash uses this same trigger, not an additional one. Explicit critical/kill/refund features can add more, but total BG gained is capped 2 per round. Self-inflicted damage, allies, summons, helpless captives and repeated damage to a corpse never generate BG. Blood is an encounter resource, not a currency carried into rest.

Dexterity governs weapon attacks; Intelligence governs hemomancy save DC and M. S scales from Crimson Agent class level. A weapon technique includes only its printed attacks, with normal weapon die plus Dexterity (or Strength when that weapon requires it). No free attack is implied by attack-speed wording. Class BG and RP are separate. Once per turn when casting an ordinary spell, optionally spend 1 BG to prevent 1 of that cast's Dissonance gain, minimum 0; never reduce RP this way.

Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation.

One Blood Mark at a time on a living target with your Bleed, except Phantom Strike, which explicitly may apply the mark without Bleed. It does not add a free Bleed. Marks last 5 of your regular turns, expire on encounter end or if the target dies, and never create damage by themselves. Rupture requires the target still within 60 ft and line of effect; it spends the mark. A mark does not defeat cover, planar boundaries or bloodlessness. Bloodtrail has its own tracking limits.

Veinweaves are self buffs unless their card expressly allows an ally. They require concentration and one may be active. Crimson Harmony is an explicit exception permitting two Veinweaves as one linked concentration burden; a failed concentration check ends both. A non-Veinweave concentration effect replaces the whole group. BG is spent on activation; no upkeep unless printed. Damage-sharing is redirection before mitigation, not extra damage: apply each recipient's own defenses once and never redirect the redirected portion again.

The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds.

At level 1 learn the core Blood Gauge/Bleed rules automatically. Blood Mark and Veinweaver's Core remain selections; Quickblood can be selected and used without a second unlock tax. Veinweaver's Core improves that foundation as printed. Standard scheduled acquisition applies. Bloodbound Edge is automatic 9. At 10 choose Bloodweaver, Shadow Operative or Thirstborn; its Final Cut is automatic 20. Duplicate Hemostasis names are separate Arch and Bloodweaver IDs.

Capacity clarification: Blood Gauge automatically reaches capacity 6 at class 9. Spill Control allows reaching 6 early but never raises the cap above 6. This new explicit gate ensures a later 5-BG Final Cut can be used without an optional capacity selection. Gain cap 2/round and encounter reset 0 still apply.

**Protected source interface:** Once per turn, spend 1 Blood Gauge while casting to prevent 1 Dissonance; the Agent routes Weave strain through blood rather than gaining free casts.

## Advancement and resources

RP authority: Explicit fallback: Cleric CoreV2 curve ×0.5, halves upward. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 2 | 0 | Choose 4 Base; at least 2 active |
| 2 | Base | 2 | 1 | Choose 2 Base |
| 3 | Arch | 4 | 1 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 5 | 1 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 6 | 2 | Choose 1 Arch |
| 6 | Arch | 8 | 2 | Choose 1 Base/Arch |
| 7 | Arch | 9 | 2 | Choose 1 Arch |
| 8 | Arch | 11 | 3 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 12 | 3 | Choose 1 Arch; automatic: Bloodbound Edge |
| 10 | Hero | 14 | 3 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 15 | 4 | Choose 1 Base/Arch |
| 12 | Hero | 17 | 4 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 18 | 4 | Choose 1 Base/Arch |
| 14 | Hero | 20 | 4 | Choose 1 Hero |
| 15 | Hero | 21 | 5 | Choose 1 Base/Arch |
| 16 | Hero | 23 | 5 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 24 | 5 | Choose 1 Base/Arch |
| 18 | Hero | 26 | 5 | Choose 1 Hero |
| 19 | Hero | 27 | 6 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 29 | 6 | No ordinary selection; automatic: Crimson Pact (Bloodweaver), Total Silence (Shadow Operative), Veinburst Requiem (Thirstborn) |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Bard-style example becomes Agent 5: DEX 16, INT 14, S 2, M 2, BG 0/cap 3, full class RP. Select Hemorrhage Slash, Quickblood, Blood Mark, Shroud at 1; Blood Tithe and Vital Targeting at 2; Rupture and Spill Control at 3. Capacity is now 6.
2. Turn 1: Hemorrhage Slash hits for ordinary weapon damage+2d6, applies Bleed, and gains 1 BG (not 2). Bonus Action Blood Mark pays 1 BG: balance 0. Target takes its first 1d4 Bleed on its next turn.
3. Turn 2: ordinary weapon attack hits and gains 1 BG. Keep the mark and save resources; Bleed ticks independently and grants no BG.
4. Turn 3: a second weapon hit gains 1 BG: balance 2. Bonus Action Quickblood spends 1 BG: balance 1. It gives movement, not another attack.
5. Turn 4: Rupture is an Action, pays 1 BG: balance 0 and consumes the mark. Target fails CON: takes(S+1)d8=3d8. Rupture is not a weapon hit, so it generates no replacement BG. Any remaining Bleed continues.
6. After the encounter BG becomes 0. Blood Tithe's used short-rest charge and spent RP do not refresh without an actual rest.

## Base cards

#### Arterial Cut

**Level 1 · selection · crimson-agent.base.arterial-cut**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your critical weapon hit | Bleed 3 turns | Once/own turn |

A critical weapon hit applies your Bleed. If it already has your Bleed, extend one instance by 2 ticks, maximum 5 ticks remaining. This damage never generates further BG.

<details><summary>Preserved source wording — book line2126</summary>

Arterial Cut: Critical hits apply Bleed for 3 turns; Bleed duration +2 turns.

</details>

#### Blood Tithe

**Level 1 · selection · crimson-agent.base.blood-tithe**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 short-rest use | Self after a hostile bleeding creature dies within 30 ft | Instant | 1/short rest |

Regain HP equal to M+class level after a creature bearing your Bleed dies. It must have been an active hostile combatant; no ally, summon, captive or corpse farming.

<details><summary>Preserved source wording — book line2127</summary>

Blood Tithe: Killing a bleeding target restores 10% of max HP.

</details>

#### Veinweaver's Core

**Level 1 · selection · crimson-agent.base.veinweaver-s-core**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

You can dismiss a Veinweave without an action and switch to another known Veinweave using its normal activation. Once/short rest reduce the BG cost of one Veinweave by 1, minimum 1. The basic one-Veinweave capacity is part of your engine, not locked behind this selection.

<details><summary>Preserved source wording — book line2128</summary>

Veinweaver's Core: Unlocks use of Veinweaves (1 active at a time).

</details>

#### Vital Targeting

**Level 1 · selection · crimson-agent.base.vital-targeting**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One weapon target | Instant | Once/own turn |

Add S damage to a weapon hit against a target that has not perceived you or is within 5 ft of another conscious hostile-to-it ally. This is flat damage, not a critical die, and requires an actual weapon hit.

<details><summary>Preserved source wording — book line2129</summary>

Vital Targeting: +15% damage to flanked or unaware enemies.

</details>

#### Shroudstep

**Level 1 · selection · crimson-agent.base.shroudstep**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until start next turn | Once/own turn |

After taking the Hide Action and moving at least 10 ft while hidden, gain+1 AC. You still need valid concealment and a successful ordinary Stealth check; this feature does not grant invisibility.

<details><summary>Preserved source wording — book line2130</summary>

Shroudstep: After using stealth movement, gain +10% dodge for 1 turn.

</details>

#### Hemorrhage Slash

**Level 1 · selection · crimson-agent.base.hemorrhage-slash**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One creature in weapon reach | Instant plus Bleed | Recharge 2 |

Make one weapon attack. On hit add S d6 damage of the weapon type and apply Bleed. The usual once/turn hit trigger grants 1 BG; this card grants no separate BG.

<details><summary>Preserved source wording — book line2133</summary>

Hemorrhage Slash: A precise strike that deals moderate damage and applies Bleed status to the target, generating 1 Blood Gauge point.

</details>

#### Veinweave: Quickblood

**Level 1 · selection · crimson-agent.base.veinweave-quickblood**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 BG | Self | 3 of your turns | Recharge 3 |

Start a Veinweave: gain+10 ft Speed and ignore nonmagical difficult terrain. Once during its duration you may draw or stow one weapon without using your object interaction. It grants no attacks or Actions.

<details><summary>Preserved source wording — book line2134</summary>

Veinweave: Quickblood: Consume 1 Blood Gauge point to increase your movement and attack speed by 15% for 3 turns.

</details>

#### Blood Mark

**Level 1 · selection · crimson-agent.base.blood-mark**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 BG | One living target with your Bleed within 60 ft | 5 of your turns | At will, one mark |

Apply your Blood Mark. Replaces your previous mark without detonating it. The mark enables Rupture and printed mark interactions; it deals no automatic damage and does not grant vision.

<details><summary>Preserved source wording — book line2135</summary>

Blood Mark: Apply a magical mark to a bleeding target that lasts for 5 turns. The mark can be detonated for additional effects.

</details>

#### Shroud

**Level 1 · selection · crimson-agent.base.shroud**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self | Until end next turn or attack/cast/bright light | 2/long rest |

Become invisible while in dim light or darkness. Attacking, casting a spell or entering bright light ends it. You must still Hide to conceal your location. Audible movement can reveal your position.

<details><summary>Preserved source wording — book line2136</summary>

Shroud: Enter stealth mode, becoming invisible to enemies until you attack or move into bright light. Limited uses per encounter.

</details>

#### Vital Sense

**Level 1 · selection · crimson-agent.base.vital-sense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | Living creatures within 60 ft, excluding total cover | 1 minute | Recharge 3 |

Sense presence and approximate direction, not identity or thoughts. Once during this minute, gain advantage on one weapon attack against a sensed creature you can otherwise legally target. This does not change critical range.

<details><summary>Preserved source wording — book line2137</summary>

Vital Sense: Heighten your senses for 1 minute, allowing you to detect the presence of living creatures within 60 feet and see their vital points more clearly (+10% critical hit chance).

</details>

## Arch cards

#### Blood Echo

**Level 3 · selection · crimson-agent.arch.blood-echo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Targets of your Bleed | As Bleed | Continuous |

Your Bleed can have two independent instances on a creature; a third application refreshes the oldest. Once on each of your turns add 1 to one Bleed instance's next tick. Never spread or detonate more instances than actually exist.

<details><summary>Preserved source wording — book line2143</summary>

Blood Echo: Bleeds now stack twice and deal +10% more damage.

</details>

#### Bio-Alchemical Flow

**Level 3 · selection · crimson-agent.arch.bio-alchemical-flow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | On activation | Continuous |

Activating a self-only Veinweave does not itself end your hidden state or Shroud. Its normal visible effects may reveal you; attacks, spells and other hostile effects still break hiding normally.

<details><summary>Preserved source wording — book line2144</summary>

Bio-Alchemical Flow: Veinweaves do not break stealth.

</details>

#### Spill Control

**Level 3 · selection · crimson-agent.arch.spill-control**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Blood Gauge capacity rises from 3 to 6. Gain rate is unchanged. This replaces, rather than adds to, the old cap. No BG is granted merely by learning it.

<details><summary>Preserved source wording — book line2145</summary>

Spill Control: Max Blood Gauge increased to 6.

</details>

#### Rupture Trigger

**Level 5 · selection · crimson-agent.arch.rupture-trigger**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Up to 2 other enemies within 5 ft of ruptured mark | Bleed 3 turns | Once/round |

After Rupture damages its marked target, choose up to 2 other living enemies nearby. Each makes CON save; on failure apply one Bleed. These applications do not trigger Rupture again or grant BG.

<details><summary>Preserved source wording — book line2146</summary>

Rupture Trigger: Detonating a Blood Mark causes AoE Bleed in a small radius.

</details>

#### Crimson Flow

**Level 3 · selection · crimson-agent.arch.crimson-flow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until end next turn | Once/own turn |

After spending BG, gain+5 ft Speed. Your next weapon damage roll before end next turn adds 1. Repeated expenditures refresh rather than stack; no attack-speed or additional-Action benefit.

<details><summary>Preserved source wording — book line2147</summary>

Crimson Flow: Using Blood Gauge grants +10% movement and attack speed for 2 turns.

</details>

#### Crimson Harmony

**Level 7 · selection · crimson-agent.arch.crimson-harmony**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self or legal linked ally | While known | Continuous |

You may sustain two Veinweaves as one concentration group. Both pay full costs and use normal activations; failing concentration ends both. Identical Veinweaves never stack, and no ordinary concentration spell can join this group.

<details><summary>Preserved source wording — book line2148</summary>

Crimson Harmony: Maintain 2 Veinweaves simultaneously.

</details>

#### Bloodbound Edge

**Level 9 · automatic · crimson-agent.arch.bloodbound-edge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 BG; 1 short-rest use | Up to 3 enemies with your Bleed within 30 ft | Instant | 1/short rest |

End up to 2 of your Bleed instances per target. Each takes 1d4 per remaining tick, maximum S d4 per creature, ignoring resistance but respecting immunity. This replaces their future ticks and grants no BG, healing or kill-trigger benefit.

<details><summary>Preserved source wording — book line2149</summary>

Capstone – Bloodbound Edge: Once per rest, convert all Bleeds on enemies to instant True Damage.

</details>

#### Veinweave: Bloodshield

**Level 3 · selection · crimson-agent.arch.veinweave-bloodshield**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 BG | Self | 3 of your turns | Recharge 3 |

Start Bloodshield Veinweave. Gain temporary HP equal to class level+M. Once while they remain, use Reaction to reduce damage to yourself by S. No self-damage refund or BG is generated.

<details><summary>Preserved source wording — book line2152</summary>

Veinweave: Bloodshield: Consume 2 Blood Gauge points to create a protective barrier that absorbs damage equal to 20% of your maximum health.

</details>

#### Rupture

**Level 3 · selection · crimson-agent.arch.rupture**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 BG; consume your mark | Your marked enemy within 60 ft | Instant | Recharge 2 |

Target makes CON save: (S+1)d8 necrotic on failure, half on success. The mark ends either way; existing Bleed remains. Damage from this technique is not a weapon hit and grants no BG.

<details><summary>Preserved source wording — book line2153</summary>

Rupture: Detonate a Blood Mark on a target, dealing significant damage and consuming the mark.

</details>

#### Bloodtrail

**Level 5 · selection · crimson-agent.arch.bloodtrail**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 BG | One living target with your Bleed within 30 ft | 1 hour | Recharge 3 |

Know the direction to the target while within 1 mile on the same plane. Total distance and a trail are not shown. Lead barriers or effects that block divination block this sense; it grants no attack advantage or targeting through cover.

<details><summary>Preserved source wording — book line2154</summary>

Bloodtrail: Mark a bleeding target, allowing you to track them perfectly for 1 hour regardless of distance or obstacles.

</details>

#### Veinweave: Sensory Theft

**Level 7 · selection · crimson-agent.arch.veinweave-sensory-theft**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 BG | One living creature with your Bleed within 60 ft | Concentration, 1 minute | Recharge 3 |

Target makes WIS save. Failure lets you see and hear through it while it remains within 1 mile on the same plane; you are blind/deaf to your own surroundings. It repeats save at the end of each of its turns and the first time each round it takes damage. No control or thought reading.

<details><summary>Preserved source wording — book line2155</summary>

Veinweave: Sensory Theft: Consume 2 Blood Gauge points to briefly experience what a bleeding target sees and hears.

</details>

#### Hemostasis

**Level 3 · selection · crimson-agent.arch.hemostasis**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | One living creature touched | Instant | Recharge 2 |

End all Bleed on the target and restore S d6+M HP, regardless of number of ticks removed. You cannot create extra healing by inflicting extra Bleed. Works even if no Bleed is present, at the same RP cost.

<details><summary>Preserved source wording — book line2156</summary>

Hemostasis: Stop all bleeding effects on yourself or an ally, converting each remaining turn of Bleed into a small amount of healing.

</details>

## Hero cards

### Bloodweaver

#### Bloodbond

**Level 10 · selection · crimson-agent.hero.bloodweaver.bloodbond**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | One willing ally within 30 ft | Concentration, 3 of your turns | Recharge 3 |

Create Bloodbond while both remain within 30 ft. When ally takes damage, you may use Reaction to redirect floor(one-quarter of pre-mitigation damage) to yourself; each recipient applies its own defenses once. Once/round when a paid technique heals you, ally gains M temporary HP. No recursive transfers.

<details><summary>Preserved source wording — book line2165</summary>

Bloodbond: Link with an ally; share 25% incoming damage and transfer 10% healing to them.

</details>

#### Hemostasis

**Level 10 · selection · crimson-agent.hero.bloodweaver.hemostasis**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 1 additional RP per application | One willing living ally in range of your Bleed application | 3 target turns | Once/own turn |

You may replace a new Bleed application on that ally with healing 1d4 at start of its next 3 turns. Pay extra RP even if original application was free. One such healing effect per target; it cannot spread, detonate, generate BG or trigger healing loops.

<details><summary>Preserved source wording — book line2166</summary>

Hemostasis: Bleeds applied to allies now heal them instead.

</details>

#### Protective Flow

**Level 10 · selection · crimson-agent.hero.bloodweaver.protective-flow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Allies actually affected by your Veinweaves | While Veinweave lasts | Continuous |

An affected ally gains+1 to saves and reduces each damage instance by 2, minimum 0. This benefit does not stack across Veinweaves or Agents. Self-only Veinweaves cannot be extended merely by this passive.

<details><summary>Preserved source wording — book line2167</summary>

Protective Flow: Allies affected by your Veinweaves gain 10% DR and +1 to all saves.

</details>

#### Veinlock Tether

**Level 10 · selection · crimson-agent.hero.bloodweaver.veinlock-tether**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 BG | Willing linked ally within 30 ft being damaged | This damage only | Once/round |

While your Bloodbond or Vitality Link is active, redirect up to S+M damage to yourself before mitigation. This is an alternative to Bloodbond's quarter-sharing reaction, not an additional redirection. Redirected damage cannot be redirected again.

<details><summary>Preserved source wording — book line2168</summary>

Veinlock Tether: Form a damage-sharing link with an ally for 3 turns.

</details>

#### Crimson Pact

**Level 20 · automatic · crimson-agent.hero.bloodweaver.crimson-pact**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 BG; 1 long-rest use | Up to 3 bleeding enemies and 6 living allies within 30 ft | Instant; shields 1 minute | 1/long rest |

End your Bleeds on chosen enemies; each makes CON save against 4d8 necrotic, half on success. Each chosen ally regains 4d8+M HP and gains 10 temporary HP. Use one shared roll per damage/healing effect; healing does not multiply by enemies or remaining ticks.

<details><summary>Preserved source wording — book line2169</summary>

Final Cut – Crimson Pact: Detonate all enemy Bleeds to heal nearby allies and grant them barriers. (1/day)

</details>

#### Transfusion

**Level 10 · selection · crimson-agent.hero.bloodweaver.transfusion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP; sacrifice up to class level HP | One willing living ally touched | Instant | 1/short rest |

Lose K real HP, at least 1, without falling below 1. Ally regains K+floor(K/2) HP. Loss bypasses defenses and cannot trigger BG, damage-sharing or healing refunds. The RP/use limit remains even if little healing is possible.

<details><summary>Preserved source wording — book line2172</summary>

Transfusion: Transfer health from yourself to an ally, healing them for 150% of the health sacrificed.

</details>

#### Veinweave: Vitality Link

**Level 10 · selection · crimson-agent.hero.bloodweaver.veinweave-vitality-link**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 BG | One willing ally within 30 ft | Concentration, 3 of your turns | Recharge 3 |

Start Vitality Link Veinweave. Once/round when you restore real HP with a paid Agent technique, linked ally regains M HP if within 30 ft. This secondary healing never triggers another link. Gain+1 AC while adjacent to that ally; no spell buffs or resources are copied.

<details><summary>Preserved source wording — book line2173</summary>

Veinweave: Vitality Link: Consume 3 Blood Gauge points to link with an ally, sharing beneficial effects and healing for 3 turns.

</details>

#### Blood Ward

**Level 12 · selection · crimson-agent.hero.bloodweaver.blood-ward**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Fixed 10 ft radius centered within 30 ft, up to 3 allies | Concentration, 3 of your turns | Recharge 4 |

Choose acid, cold, fire, lightning or necrotic. Selected allies within the zone gain resistance to that damage type. Leaving loses the benefit; reentering restores it. Identical resistance does not stack. This is not a Veinweave.

<details><summary>Preserved source wording — book line2174</summary>

Blood Ward: Create a protective circle using blood magic that shields allies within from certain types of damage or effects.

</details>

#### Purify Blood

**Level 14 · selection · crimson-agent.hero.bloodweaver.purify-blood**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | One willing living creature touched | Instant | Recharge 3 |

End Poisoned and one nonmagical disease. Magical disease needs a successful INT ability check against its stated treatment DC, or DC 15 if absent; failure spends the cost. No curse, Wound, death or Corruption removal.

<details><summary>Preserved source wording — book line2175</summary>

Purify Blood: Remove poison, disease, or other blood-borne afflictions from a target.

</details>

#### Lifewell

**Level 16 · selection · crimson-agent.hero.bloodweaver.lifewell**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP; all BG, minimum 3 | Up to 3 living allies within 15 ft | Concentration, 3 of your turns | 1/long rest |

Spend K BG. At start and on each of your next 2 turns, use Bonus Action and pay 1 RP to pulse healing: each chosen ally still within 15 ft regains 1d8+K HP. Without maintenance it ends at turn end. Total 3 pulses; no triggers create more BG.

<details><summary>Preserved source wording — book line2176</summary>

Lifewell: Ultimate ability that converts all your remaining Blood Gauge into a powerful healing aura for allies.

</details>

### Shadow Operative

#### Ghost Vein

**Level 10 · selection · crimson-agent.hero.shadow-operative.ghost-vein**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One weapon target | Instant | Once/own turn |

A weapon hit made from hidden ignores resistance to that weapon's damage type for this hit. Immunity remains. This does not bypass armor or make the attack automatically hit.

<details><summary>Preserved source wording — book line2182</summary>

Ghost Vein: Attacks from stealth ignore 25% of target resistances.

</details>

#### Blackout Agent

**Level 10 · selection · crimson-agent.hero.shadow-operative.blackout-agent**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 BG | Attacker within 30 ft that missed you | Until end attacker's next turn | Once/round |

Attacker makes CON save; failure Blinded. Requires it can see you. Each creature becomes immune to your Blackout Agent until encounter end after resolving this save, preventing repeated blind-lock.

<details><summary>Preserved source wording — book line2183</summary>

Blackout Agent: Dodging an attack blinds the attacker for 1 turn.

</details>

#### Ghostflow Reflexes

**Level 10 · selection · crimson-agent.hero.shadow-operative.ghostflow-reflexes**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self while sustaining a Veinweave | While active | Once/round reset |

Gain+1 AC. Once/round after a Veinweave starts, shorten one OTHER positive Agent cooldown by 1; this uses that ability's reset allowance. It grants no critical immunity, actions or per-rest uses.

<details><summary>Preserved source wording — book line2184</summary>

Ghostflow Reflexes: While Veinweave is active: +5% dodge, cooldowns -1, +10% crit resistance.

</details>

#### Veinjammer

**Level 10 · selection · crimson-agent.hero.shadow-operative.veinjammer**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One creature damaged by your Bleed | Until end target's next turn | Once/round |

After a Bleed tick, choose that victim: Speed reduced 5 ft, minimum 0, and its next concentration save takes-1. Nonstacking; does not remove an Action or prohibit spellcasting.

<details><summary>Preserved source wording — book line2185</summary>

Veinjammer: Bleeds reduce enemy casting and action speed by 10%.

</details>

#### Total Silence

**Level 20 · automatic · crimson-agent.hero.shadow-operative.total-silence**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 BG; 1 long-rest use | Up to 6 enemies within 30 ft | Until end your next turn | 1/long rest |

Each makes CON save. Failure prevents verbal spellcasting and Reactions, and suppresses one passive bonus to AC or attack rolls chosen from an observed effect. It never removes innate anatomy, immunities, legendary rules or class resource pools. Success prevents all effects; no whole-sheet passive disable.

<details><summary>Preserved source wording — book line2186</summary>

Final Cut – Total Silence: AoE disables all enemy passives and silences for 2 turns.

</details>

#### Phantom Strike

**Level 10 · selection · crimson-agent.hero.shadow-operative.phantom-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 BG | One enemy in weapon reach; must be hidden from it | Instant | Recharge 3 |

Make one weapon attack with advantage. On hit add S d6 damage and apply a mark without its usual BG cost, even if not already bleeding. The mark replaces your old mark; no free Rupture occurs. Normal hit BG gain still capped.

<details><summary>Preserved source wording — book line2189</summary>

Phantom Strike: Attack from stealth with increased critical chance and apply a Blood Mark automatically.

</details>

#### Veinweave: Shadow Meld

**Level 10 · selection · crimson-agent.hero.shadow-operative.veinweave-shadow-meld**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 BG | Self | Concentration, 1 minute | Recharge 4 |

Start Shadow Meld Veinweave: advantage on Stealth and invisible while motionless in dim light/darkness. Moving removes invisibility until start next turn; attacking or casting ends the Veinweave. No concealment against blindsight or effects that expressly reveal invisibility.

<details><summary>Preserved source wording — book line2190</summary>

Veinweave: Shadow Meld: Consume 3 Blood Gauge points to become nearly undetectable for 1 minute, gaining enhanced stealth capabilities.

</details>

#### Disrupt Flow

**Level 12 · selection · crimson-agent.hero.shadow-operative.disrupt-flow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 BG | One living enemy within 30 ft | Until end target's next turn | Recharge 3 |

CON save: failure prevents Reactions and gives disadvantage on its next spell attack. If concentrating, make an additional normal concentration save versus your class DC. This never disables all special abilities or guarantees a failed concentration check.

<details><summary>Preserved source wording — book line2191</summary>

Disrupt Flow: Temporarily disable a target's special abilities by disrupting their vital energies.

</details>

#### Blood Cipher

**Level 14 · selection · crimson-agent.hero.shadow-operative.blood-cipher**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Ritual | 3 RP; 10 minutes | One willing or restrained living target with your Bleed touched | One question | 1/short rest |

Target makes WIS save unless willing. On failure learn one factual sensory memory from the last 24 hours about a stated event; the target chooses a relevant memory if several exist. Success yields no information. No beliefs, absolute truth or unrelated secrets are guaranteed.

<details><summary>Preserved source wording — book line2192</summary>

Blood Cipher: Extract information directly from a bleeding target's blood, potentially learning secrets or weaknesses.

</details>

#### Blackout

**Level 16 · selection · crimson-agent.hero.shadow-operative.blackout**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP; 2 BG | Fixed 15 ft-radius sphere within 60 ft | Concentration, 3 of your turns | 1/long rest |

Create magical darkness blocking ordinary sight and darkvision. You can see within it up to 30 ft. Creatures can leave normally; no automatic damage, surprise or advantage when another sense locates you. Enemies still act and make saves normally.

<details><summary>Preserved source wording — book line2193</summary>

Blackout: Ultimate ability that creates a zone of magical darkness where only you can see clearly, granting significant advantages.

</details>

### Thirstborn

#### Blood Frenzy

**Level 10 · selection · crimson-agent.hero.thirstborn.blood-frenzy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While hostile Bleeds persist | Continuous |

Add 1 to direct weapon damage per hostile creature bearing your Bleed, maximum 3. Applies once per hit, not per Bleed instance. Secondary Bleed, copies and explosions gain no bonus.

<details><summary>Preserved source wording — book line2199</summary>

Blood Frenzy: +5% damage per enemy actively bleeding (max +25%).

</details>

#### Hemorrhagic Plague

**Level 10 · selection · crimson-agent.hero.thirstborn.hemorrhagic-plague**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 BG | One new living enemy within 5 ft of a Bleed victim | Bleed 3 turns | Once every 3 of your turns |

After one of your Bleeds ticks, pay 1 BG; new target makes CON save. Failure applies one Bleed. A spread instance cannot spread again. This grants no BG and does not duplicate marks or immediate damage.

<details><summary>Preserved source wording — book line2200</summary>

Hemorrhagic Plague: Bleeds automatically spread to nearby enemies every 3 turns.

</details>

#### Pain-to-Power Conduction

**Level 10 · selection · crimson-agent.hero.thirstborn.pain-to-power-conduction**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 BG | One enemy within 5 ft after it damages you | Instant plus Bleed | Once/round |

End one active Veinweave. Chosen enemy makes CON save: failure takes S d4 necrotic and Bleed; success takes half immediate damage only. On failure by 10 it is Frightened until end next turn. No resource refund.

<details><summary>Preserved source wording — book line2201</summary>

Pain-to-Power Conduction: Veinweaves explode when struck, dealing AoE Bleed and minor Fear.

</details>

#### Carrion Conductor

**Level 10 · selection · crimson-agent.hero.thirstborn.carrion-conductor**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | One fresh hostile living-combatant corpse within 30 ft | Until end next turn | Recharge 3 |

Mark the corpse once; on activation or before expiry use Reaction to burst it. Up to 3 enemies within 5 ft make DEX saves: S d6 necrotic, half on success. Corpse cannot be reused, raised by this effect or provide BG/kill triggers.

<details><summary>Preserved source wording — book line2202</summary>

Carrion Conductor: Corpses leave behind blood pools that explode for AoE damage.

</details>

#### Veinburst Requiem

**Level 20 · automatic · crimson-agent.hero.thirstborn.veinburst-requiem**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | All BG, minimum 3; 1 long-rest use | Up to 6 enemies with your Bleed within 30 ft | Instant | 1/long rest |

Spend K BG and end your Bleeds on targets. CON save: (S+K)d8 necrotic, half on success. A target failing by 10 with remaining HP no greater than your class level falls to 0; ordinary death rules follow. No percentage-based automatic boss execution or BG refund.

<details><summary>Preserved source wording — book line2203</summary>

Final Cut – Veinburst Requiem: Detonates all Bleeds and Blood Gauge effects in range. Enemies under 25% HP are instantly executed. (1/day)

</details>

#### Exsanguinate

**Level 10 · selection · crimson-agent.hero.thirstborn.exsanguinate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 BG | One living creature within 30 ft | Instant | Recharge 2 |

CON save: (S+1)d8 necrotic, half on success; add 1d8 if it has your Bleed. If it fails and actually takes damage, regain 1 BG within the common gain cap. The refund cannot pay activation costs retroactively.

<details><summary>Preserved source wording — book line2206</summary>

Exsanguinate: Violently extract blood from a target, dealing heavy damage to bleeding enemies and generating additional Blood Gauge.

</details>

#### Veinweave: Blood Frenzy

**Level 10 · selection · crimson-agent.hero.thirstborn.veinweave-blood-frenzy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 BG | Self | Concentration, 3 of your turns | Recharge 4 |

Start Blood Frenzy Veinweave: once on your turn add S d6 to one weapon hit; gain+10 ft Speed and suffer-2 AC. No extra attacks, Actions or critical range. Ending early removes both benefit and penalty.

<details><summary>Preserved source wording — book line2207</summary>

Veinweave: Blood Frenzy: Consume 3 Blood Gauge points to enter a frenzied state, increasing damage and attack speed but reducing defense.

</details>

#### Blood Boil

**Level 12 · selection · crimson-agent.hero.thirstborn.blood-boil**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 BG | One living enemy within 60 ft | Instant; control until end next turn | Recharge 3 |

CON save: (S+1)d6 fire, half on success. On failure target loses Reactions; on failure by 10 also Stunned until end its next turn. The Stun uses the shared hard-denial guard across all this character’s features. If this character already hard-denied that target this encounter, only damage and the non-hard-denial rider resolve.

<details><summary>Preserved source wording — book line2208</summary>

Blood Boil: Cause a target's blood to heat rapidly, dealing internal damage and potentially stunning them.

</details>

#### Crimson Harvest

**Level 14 · selection · crimson-agent.hero.thirstborn.crimson-harvest**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 BG; 1 short-rest use | One enemy in weapon reach at half HP or less | Instant | 1/short rest |

Make one weapon attack; on hit add S d8 damage. If this reduces it to 0, regain S+M HP and 1 BG within gain cap. No instant kill from a percentage threshold; summoned/allied/helpless creatures yield no recovery.

<details><summary>Preserved source wording — book line2209</summary>

Crimson Harvest: Execute a heavily wounded target, restoring health and Blood Gauge based on the target's missing health.

</details>

#### Bloodstorm

**Level 16 · selection · crimson-agent.hero.thirstborn.bloodstorm**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 RP; 3 BG | Moving 10 ft aura around self, up to 3 enemies per pulse | Concentration, 3 of your turns | 1/long rest |

On start and each later paid pulse, targets make CON saves: S d6 necrotic, half on success; failure applies one Bleed. Maintenance costs Bonus Action+1 RP. Maximum 3 pulses. Once/turn your direct weapon attack against a creature in the storm adds 1 damage; storm/bleed damage gives no BG.

<details><summary>Preserved source wording — book line2210</summary>

Bloodstorm: Ultimate ability that creates a swirling vortex of blood, dealing continuous damage to enemies and empowering your abilities.

</details>

## Source appendix and open balance questions

The complete original Crimson Agent book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/crimson-agent.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Does early setup take too many turns for one mark?
- Can Bloodweaver protect without sacrifice loops or infinite healing?
- Are denial and execution limits sufficient against bosses and multiclass dips?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
