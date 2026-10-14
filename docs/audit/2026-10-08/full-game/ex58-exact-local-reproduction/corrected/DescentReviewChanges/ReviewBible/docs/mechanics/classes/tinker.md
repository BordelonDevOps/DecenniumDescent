# Tinker — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/tinker.json) · [Normalized card data](../../../data/public/class_playtests/tinker.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Intelligence
- Secondary Attribute: Dexterity
- Hit Points: Medium (8 + Constitution modifier at 1st level, 1d8 per level thereafter)
- Armor Proficiency: Light armor (with Tinker-specific upgrades at higher levels)
- Weapon Proficiency: Shortbows, crossbows, and simple weapons
- Tool Proficiency: Tinker's tools, alchemist's supplies

Intelligence governs class DC/M, device attacks use PB+INT; Dexterity governs personal ranged weapons. Hit Die d8, light armor, shortbows/crossbows/simple weapons, tinkers tools and alchemist supplies. Technology is fictional equipment. Ordinary Tinker spells use RP/Dissonance; mundane bombs/devices with printed RP fuel costs are class techniques and do not separately count as spell casts.

At 1 automatically own one Anacite Drone: AC 13+INT modifier, HP 5+INT modifier+class level (minimum 1), flight 30 ft, ranged bolt 60 ft attack PB+INT for 1d6 piercing. Bonus Action commands one move and one attack or named module action; otherwise it Dodges and may follow you. On bolt hit roll d4; on 4 target CON save or cannot take Reactions through end next turn (Shock, no automatic Stun). All drones/turrets/scraplings share ONE damaging action per Bonus Action command per regular turn unless a card explicitly supplies a priced extra attack. No autonomous barrage. Drone is a construct, not immune to all conditions; poison/psychic immunity, no charm. Carry/retract it in 1 minute; no pocket extra world or passenger flight.

A destroyed drone remains 0 HP until repaired for 1 RP and 10 minutes with tools to half HP, once/short rest, or rebuilt during long rest to full. Ordinary repairing does not recharge devices, grant organic healing or trigger destruction bonuses. At 13 Dual Drone Protocols automatically chooses on each long rest either 2 basic drones each with one module, or one drone with 2 distinct modules. Still one command budget. Never more than 2 drones.

At 5 automatically gain one module slot; change module during long rest. Offensive: Burn Injector first bolt hit/turn causes 1d4 fire next 2 target turns; Poison Vents d4=4 on hit CON save or-1 attack rolls until end next turn; Concussive Bolt d4=4 on hit CON save or Stunned until end next turn, once/target/encounter shared denial guard and 1/short-rest successful Stun. Defensive: Target Taunter command action once/encounter WIS save one foe 30 ft or disadvantage attacking others until end next turn; Energy Shield command gives adjacent ally+2 AC until start next turn; Smoke Cloud command once/encounter creates 5 ft radius opaque smoke centered drone until start next turn. Support: Ammo Dispenser adjacent allies first ranged hit/turn+1 damage; Target Scanner command mark 1 visible foe 60 ft first ally attack before start next turn+1 hit; Tether Grappler command once/encounter pulls 1 willing ally 15 ft within 30 ft without opportunity attacks along open route.

Bomb stock refills during long rest with tools to 3 at 1, 4 at 5, 5 at 11; cap equals refill, class bombs have no resale or stockpiling. Encounter throw cap 1 at 1, 2 at 5, 3 at 11. Each throw uses one stock and one encounter allowance. Basic fire/cold known 1; advanced profiles known 6; Overload Core known 9. Base throw is Action, range 30 ft, 10 ft radius up to 3 creatures, DEX save S d6 element, half success. Fire failure adds 1d4 Burn next turn; cold failure Speed-10 ft until end next turn. Explosive Handling makes throw Bonus Action; still only one bomb/regular turn. At 15 Danger Close automatically allows excluding yourself/allies. Safe Detonation grants this early. Bombs cannot critically hit or inherit weapon riders.

Advanced bomb profiles replace basic rider: Thermobaric fire pushes 5 ft on failed STR save after damage; Cryo cold on failed DEX also Speed 0 until end next turn and d2=2 ignores 1 flat DR against this bomb; Shock lightning CON instead DEX, failure prevents verbal spellcasting until end next turn (construct instead loses Reactions), shared hard-denial guard; Glue no damage, 15 ft square difficult terrain 3 rounds and entering/starting DEX save or Speed-15 ft until end turn, once per creature/round. Overload Core destroys one commanded drone within 30 ft as part Action bomb, DEX save 2d6 lightning and no Reactions until end next turn on failure, half damage on success. Consumes stock/allowance; no further destruction proc.

Deployable slots start 1 at 6, 2 at 13, 3 at 17, separate from drone cap. Deploy Action 2 RP within 15 ft, fixed ground, AC 12+PB HP 2 L, duration 3 rounds, concentration not required; destroyed do not refund fuel. All share command budget. Sentry and Net require their cards. Additional engine profiles unlocked 6: Rocket Tower commanded attack 60 ft target DEX save S d6 fire/half success to up to 2 creatures within 5 ft, maximum 3 shots; Decoy Dummy one foe 30 ft WIS save when deployed or disadvantage on next attack against others, destruction S fire to one adjacent enemy no chain; Blast Wall 10-by 5 ft blocks LOS and movement, climb cost 10 ft. Net Trap one enemy entry STR save or Restrained, end turn repeat/Action escape DC, 3 round max then ends. One only fires when commanded except nonattack trap/decoy trigger; command budget limits damaging triggers too.

Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets.

**Protected source interface:** Once per short rest, route up to 2 Dissonance into an active device; that device becomes disabled until repaired or the next short rest.

## Advancement and resources

RP authority: Direct Core Systems V2 table. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 1 | 0 | Choose 4 Base; at least 2 active |
| 2 | Base | 2 | 1 | Choose 2 Base |
| 3 | Arch | 3 | 1 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 4 | 1 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 6 | 1 | Choose 1 Arch; automatic: Pet Upgrade Slot |
| 6 | Arch | 8 | 2 | Choose 1 Base/Arch |
| 7 | Arch | 10 | 2 | Choose 1 Arch |
| 8 | Arch | 12 | 2 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 14 | 2 | Choose 1 Arch |
| 10 | Hero | 16 | 3 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 18 | 3 | Choose 1 Base/Arch |
| 12 | Hero | 20 | 3 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 22 | 3 | Choose 1 Base/Arch |
| 14 | Hero | 24 | 4 | Choose 1 Hero |
| 15 | Hero | 26 | 4 | Choose 1 Base/Arch |
| 16 | Hero | 28 | 4 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 30 | 4 | Choose 1 Base/Arch |
| 18 | Hero | 32 | 5 | Choose 1 Hero |
| 19 | Hero | 34 | 5 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 36 | 5 | No ordinary selection; automatic: Mech Overdrive |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Tinker 6 INT 18 PB 3 S 2 M 4 RP 8; drone AC 17 HP 15. Bomb stock 4, encounter allowance 2, one deployable slot. Module Burn Injector.
2. Turn 1 Action deploy Sentry for 2 RP: RP 8→6. Bonus Action command drone; bolt hits 1d6, Burn 1d4 at next 2 target turns. Sentry does not fire independently.
3. Turn 2 with Explosive Handling throw fire bomb as Bonus Action: stock 4→3, allowance 2→1. DEX save 2d6 fire, half success. Action personal crossbow attack. Neither drone nor turret fires because Bonus Action already spent.
4. Turn 3 Bonus Action command Sentry for 1d6; drone Dodges. Action Field Repair 1 RP heals drone 2d8+4 up to 15, RP 6→5. No organic HP repaired.
5. Turn 4 Sentry expires after 3 turns. You cannot salvage its RP automatically. One bomb allowance and 3 stock remain until encounter ends; new encounter restores allowance 2, not stock 4.

## Base cards

#### Mechanical Aptitude

**Level 1 · selection · tinker.base.mechanical-aptitude**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Mechanical devices you examine | While using tools | Continuous |

Advantage on checks to understand, repair or disable mechanisms. Requires appropriate access and tools; no automatic control of enemy constructs.

<details><summary>Preserved source wording — book line4576</summary>

Mechanical Aptitude: Gain advantage on checks to understand, repair, or disable mechanical devices.

</details>

#### Explosive Handling

**Level 1 · selection · tinker.base.explosive-handling**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | One bomb and encounter allowance | Your bomb throw | Instant | Once/own turn |

Throw a known prepared bomb as Bonus Action instead of Action. Removes ordinary accidental misfire, not Warmachine risk or enemy defenses. Cannot command a device with the same Bonus Action.

<details><summary>Preserved source wording — book line4577</summary>

Explosive Handling: Throw bombs as a bonus action without risk of misfire.

</details>

#### Quick Fingers

**Level 1 · selection · tinker.base.quick-fingers**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | One noncombat mechanism touched | One manipulation | Once/turn |

Open unlocked latch, operate simple switch or retrieve a carried gadget. Does not activate damaging/healing devices, disarm a trap, reload every weapon or add another Bonus Action.

<details><summary>Preserved source wording — book line4578</summary>

Quick Fingers: Perform device activation and manipulation actions with increased speed.

</details>

#### Technical Knowledge

**Level 1 · selection · tinker.base.technical-knowledge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One visible nonartifact mechanical/alchemical item | Instant information | Recharge 2 |

INT+PB DC 15 identifies its ordinary purpose and operating control. Success reveals one safe use, not secret passwords or magical properties. Failure does not destroy item.

<details><summary>Preserved source wording — book line4579</summary>

Technical Knowledge: Identify the properties and functions of mechanical or alchemical items on sight.

</details>

#### Improvised Engineering

**Level 1 · selection · tinker.base.improvised-engineering**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Downtime | Tools and scrap; 10 minutes | One simple handheld tool | 1 hour | 1/short rest |

Produce lockpick, wedge, pulley, clamp or equivalent ordinary implement. No weapons, explosives, currency, rare materials or autonomous effects; collapses afterward without sale value.

<details><summary>Preserved source wording — book line4580</summary>

Improvised Engineering: Create temporary tools or simple devices from available materials.

</details>

#### Deploy Anacite Drone

**Level 1 · selection · tinker.base.deploy-anacite-drone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 if functional; repairs as engine | Your carried drone within 5 ft | Until retracted/destroyed | One deployment per drone |

Drone is automatic class engine. Selecting this card instead upgrades deployment to Bonus Action and permits 5 ft free initial placement. No free attacks, repair or extra drone.

<details><summary>Preserved source wording — book line4583</summary>

Deploy Anacite Drone: Summon a mechanical companion that attacks with ranged bolts (1d6 damage + 25% chance to shock).

</details>

#### Tinker Bomb I

**Level 1 · selection · tinker.base.tinker-bomb-i**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action or Bonus Action with Handling | One bomb; encounter allowance | 10 ft radius within 30 ft, up to 3 creatures | Instant/rider as profile | Once/turn |

Bomb recipes are automatic engine. Selecting card increases throw range to 45 ft. Use exact bomb profile, saves, stock and friendly-fire rules; no free bomb creation during combat.

<details><summary>Preserved source wording — book line4584</summary>

Tinker Bomb I: Create and throw Fire or Cold bombs that deal area effect damage.

</details>

#### Field Repair

**Level 1 · selection · tinker.base.field-repair**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | One construct/device touched | Instant | Recharge 2 |

Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses.

<details><summary>Preserved source wording — book line4585</summary>

Field Repair: Quickly fix a damaged mechanical device or construct.

</details>

#### Analyze Weakness

**Level 1 · selection · tinker.base.analyze-weakness**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Visible target within 60 ft | Until end next turn | Recharge 3 |

Identify one visibly demonstrated damage resistance. Your next bomb/device damage against it ignores 2 flat DR, not resistance/immunity. No invented weakness or automatic secret knowledge.

<details><summary>Preserved source wording — book line4586</summary>

Analyze Weakness: Study a target to identify vulnerabilities to specific damage types.

</details>

#### Jury-rig

**Level 1 · selection · tinker.base.jury-rig**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | One willing ally weapon/device touched | 3 rounds | Recharge 3 |

Choose+1 first attack roll/turn or+5 ft device movement. One modification per item, no stack. Does not change weapon category, spell function, summon limit or command budget.

<details><summary>Preserved source wording — book line4587</summary>

Jury-rig: Temporarily modify a device or weapon to perform a different function.

</details>

## Arch cards

#### Enhanced Drone Control

**Level 3 · selection · tinker.arch.enhanced-drone-control**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your drones | While active | Continuous |

Gain+1 attack roll and can follow simple move/dodge commands while within 120 ft. Attacks still require your Bonus Action and line of effect; no independent turn.

<details><summary>Preserved source wording — book line4593</summary>

Enhanced Drone Control: Your Anacite Drone gains improved targeting and responsiveness.

</details>

#### Bomb Specialization

**Level 3 · selection · tinker.arch.bomb-specialization**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your bomb damage | One target per throw | Once/turn |

Add M damage to one target that failed its initial save. No multiplying by area targets or damage ticks; Glue instead increases its slow by 5 ft maximum 20.

<details><summary>Preserved source wording — book line4594</summary>

Bomb Specialization: Your explosive devices deal additional damage or have enhanced effects.

</details>

#### Pet Upgrade Slot

**Level 5 · automatic · tinker.arch.pet-upgrade-slot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Long rest choice | 0 | One drone module slot | Until next reconfiguration | Automatic engine at 5 |

Choose one of 9 bounded modules in engine. This automatic unlock is not a selected skill. At 13 use Dual Drone Protocols, still shared command budget.

<details><summary>Preserved source wording — book line4595</summary>

Pet Upgrade Slot: Modify your drone with an Offensive, Defensive, or Support module (level 5).

</details>

#### Deployable Expertise

**Level 3 · selection · tinker.arch.deployable-expertise**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your deployables | While deployed | Continuous |

Gain M maximum/initial HP and+1 AC. Does not heal existing damage when moved or grant additional slots. Drones excluded unless another card says otherwise.

<details><summary>Preserved source wording — book line4596</summary>

Deployable Expertise: Your deployed devices have increased durability and effectiveness.

</details>

#### Remote Detonation

**Level 9 · selection · tinker.arch.remote-detonation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP; sacrifice one device | Device within 60 ft, 10 ft radius up to 3 creatures | Instant | Recharge 3 |

Destroy your device; DEX save 2 S d6 force, half success. Failed save also no Reactions until end next turn. Cannot trigger Volatile Components/Scrap Reaper or another destruction/copy chain; no resource refund.

<details><summary>Preserved source wording — book line4597</summary>

Remote Detonation: Detonate your devices remotely for area effect damage or stunning (level 9).

</details>

#### Deploy Sentry Turret

**Level 6 · selection · tinker.arch.deploy-sentry-turret**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP; one slot | Empty ground within 15 ft | 3 rounds | Recharge 2 |

Deploy Sentry engine profile: commanded attack range 25 ft PB+INT for 1d6 piercing. No auto fire, extra Bonus Action or shared budget exception. Durability AC 12+PB HP 2 L before upgrades.

<details><summary>Preserved source wording — book line4600</summary>

Deploy Sentry Turret: Place an automated turret that fires at enemies (level 6).

</details>

#### Deploy Net Trap

**Level 6 · selection · tinker.arch.deploy-net-trap**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP; one slot | One 5 ft square within 15 ft | 3 rounds or trigger | Recharge 2 |

Deploy visible Net Trap. First enemy entry STR save or Restrained, repeat end turn or Action escape against DC. Target Huge+instead speed-10 ft. No damage or continued rearming; ends after one creature escapes.

<details><summary>Preserved source wording — book line4601</summary>

Deploy Net Trap: Set a trap that roots enemies who trigger it (level 6).

</details>

#### Overcharge

**Level 3 · selection · tinker.arch.overcharge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP | One device within 30 ft | Until end next turn | Recharge 3 |

Next damaging activation adds S d6 to one target. One pending overcharge, no stacking, does not command device or grant attack. If device expires first cost lost.

<details><summary>Preserved source wording — book line4602</summary>

Overcharge: Temporarily boost the effectiveness of one of your devices.

</details>

#### Recalibrate

**Level 3 · selection · tinker.arch.recalibrate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | One drone; one visible enemy 60 ft | Until end next turn | Recharge 2 |

Drone's next attack against chosen enemy has advantage. Still needs separate command; no automatic shot, enemy type wide permanent buff or crit conversion.

<details><summary>Preserved source wording — book line4603</summary>

Recalibrate: Adjust your drone's targeting parameters to focus on a specific enemy type.

</details>

#### Emergency Protocols

**Level 3 · selection · tinker.arch.emergency-protocols**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 encounter use | Drone within 10 ft when attack hits you | One hit | 1/encounter |

Drone intercepts: reduce damage to you by S+M and takes same amount unmitigated. It must be active/conscious. Does not redirect again or trigger retaliation loops.

<details><summary>Preserved source wording — book line4604</summary>

Emergency Protocols: Your drone automatically intercepts an attack meant for you once per encounter.

</details>

## Hero cards

### Artificer

#### Calibrated Precision

**Level 10 · selection · tinker.hero.artificer.calibrated-precision**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Up to 3 allies within 15 ft | While conscious | Continuous |

Each gains+1 to first attack roll per turn. Does not stack with Target Scanner or another Calibrated Precision; no saves bonus.

<details><summary>Preserved source wording — book line4613</summary>

Calibrated Precision: Allies within 3 tiles gain +1 to hit.

</details>

#### Safe Detonation

**Level 10 · selection · tinker.hero.artificer.safe-detonation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your bomb area | Each throw | Continuous |

Exclude any allies and yourself. Grants Danger Close early; at 15 also ignore half cover for bomb save calculations. Does not make destructive sacrifices automatically safe.

<details><summary>Preserved source wording — book line4614</summary>

Safe Detonation: Your bombs deal no damage to allies.

</details>

#### Protective Programming

**Level 10 · selection · tinker.hero.artificer.protective-programming**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 RP | Drone adjacent to ally hit by attack | One hit | Once/round |

Drone grants ally S+M temporary HP before hit resolves. No heal or reversal of hit; max one protected ally, normal temporary HP nonstacking.

<details><summary>Preserved source wording — book line4615</summary>

Protective Programming: Your drone prioritizes defending vulnerable allies.

</details>

#### Efficient Power Cells

**Level 10 · selection · tinker.hero.artificer.efficient-power-cells**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your nonhealing deployables | Deployment | Continuous |

A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration.

<details><summary>Preserved source wording — book line4616</summary>

Efficient Power Cells: Your devices last 50% longer before needing recharging.

</details>

#### Nano-Aegis Drone

**Level 10 · selection · tinker.hero.artificer.nano-aegis-drone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | Your drone within 15 ft | 3 rounds | Recharge 4 |

Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode.

<details><summary>Preserved source wording — book line4619</summary>

Nano-Aegis Drone: Replace your combat drone with a healing/shield drone that protects allies.

</details>

#### Repair Pulse

**Level 10 · selection · tinker.hero.artificer.repair-pulse**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Upto 3 friendly devices within 30 ft | Instant; AC until start next turn | 1/short rest |

Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.

<details><summary>Preserved source wording — book line4620</summary>

Repair Pulse: Heal all drones, turrets, and party deployables for 50% HP and grant +1 AC to nearby allies.

</details>

#### Magnetic Wall

**Level 12 · selection · tinker.hero.artificer.magnetic-wall**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP; one slot | 10-by 5 ft wall within 15 ft | 3 rounds | Recharge 4 |

AC 12+PB HP 2 L, blocks LOS/movement. Reaction when ranged weapon hit ally within 5 ft of wall reduce its damage by S+M and wall takes reduction amount. Requires line between attack and wall; no automatic all-shot absorption.

<details><summary>Preserved source wording — book line4621</summary>

Magnetic Wall: Deploy a barrier that pulls ranged attacks into it and provides cover.

</details>

#### Restoration Field

**Level 14 · selection · tinker.hero.artificer.restoration-field**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP start; 1 RP maintenance; one slot | 10 ft radius within 30 ft | Maximum 3 pulses | Recharge 4 |

Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells.

<details><summary>Preserved source wording — book line4622</summary>

Restoration Field: Create an area that gradually repairs mechanical devices and heals organic allies.

</details>

#### Overload Suppression

**Level 16 · selection · tinker.hero.artificer.overload-suppression**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One enemy construct/device within 30 ft | Until end next target turn | 1/short rest |

CON save or fails its next Reaction and has disadvantage on attacks. On failure by 5 also Stunned, shared hard-denial guard. No automatic permanent deactivation, hacking allegiance or ignoring boss immunity.

<details><summary>Preserved source wording — book line4623</summary>

Overload Suppression: Temporarily disable enemy mechanical devices or constructs.

</details>

### Techsmith

#### Automated Field Kit

**Level 10 · selection · tinker.hero.techsmith.automated-field-kit**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Bomb stock cap/refill+1; encounter allowance unchanged. Reduce deployable card recharge by 1 minimum 1, on setting counter only. Never refresh rest uses or trigger repeated counter reductions.

<details><summary>Preserved source wording — book line4629</summary>

Automated Field Kit: Carry an extra bomb and reduce deployable cooldowns by 1 round.

</details>

#### Enhanced Targeting

**Level 10 · selection · tinker.hero.techsmith.enhanced-targeting**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your turret attacks | While active | Continuous |

Gain+1 to hit. Does not stack with Enhanced Drone Control if profile ever counts both, and does not impose save penalties.

<details><summary>Preserved source wording — book line4630</summary>

Enhanced Targeting: Your turrets gain +1 to hit.

</details>

#### Efficient Recycling

**Level 10 · selection · tinker.hero.techsmith.efficient-recycling**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | One destroyed device remains | Your destroyed device within reach | After combat 1 minute | 1/short rest |

Recover 1 RP spent on deploying it, never more than its actual paid cost. Deliberate sacrifice or copy does not qualify. Consume usable debris; no repeated salvage from same object.

<details><summary>Preserved source wording — book line4631</summary>

Efficient Recycling: Recover components from destroyed devices to create new ones.

</details>

#### Technical Mastery

**Level 10 · selection · tinker.hero.techsmith.technical-mastery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | Your damaging device activation | One target | Once/own turn |

After damage rolld 10; on 10 you may pay 1 RP to add half its unmodified damage dice total rounded down to one target. No second activation, commands, procs, resources or healing duplication.

<details><summary>Preserved source wording — book line4632</summary>

Technical Mastery: Your devices have a 10% chance to function twice when activated.

</details>

#### Advanced Turret Bay

**Level 10 · selection · tinker.hero.techsmith.advanced-turret-bay**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP; two slots | Two empty ground spaces within 15 ft | 3 rounds | Recharge 4 |

Requires 2 available slots (normally 13); if only one, deploy one for 2 RP. Sniper command attack 90 ft S d6 piercing; Burst command DEX save S d4 piercing to 2 targets within 5 ftat 30 ft. One commanded turret per Bonus Action, not both automatically.

<details><summary>Preserved source wording — book line4635</summary>

Advanced Turret Bay: Deploy two turrets simultaneously in either Sniper or Burst mode.

</details>

#### Gadget Sync Protocol

**Level 12 · selection · tinker.hero.techsmith.gadget-sync-protocol**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | One turret within 60 ft after your bomb throw | One attack | Once/own turn |

Turret makes one ordinary shot at surviving bomb target. Replaces its normal commanded damaging action for that turn; cannot combine with another device attack from Bonus Action. No chains or additional bombs.

<details><summary>Preserved source wording — book line4636</summary>

Gadget Sync Protocol: When you throw a bomb, one turret may fire instantly at the same target.

</details>

#### Snap Rebuild

**Level 14 · selection · tinker.hero.techsmith.snap-rebuild**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP; 1 encounter use | One destroyed device/drone within 15 ft | Remaining original duration | 1/encounter |

Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock.

<details><summary>Preserved source wording — book line4637</summary>

Snap Rebuild: Once per encounter, instantly redeploy any destroyed turret or pet with 50% HP.

</details>

#### Reconfiguration

**Level 10 · selection · tinker.hero.techsmith.reconfiguration**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | One deployed device within 15 ft | Remaining duration | Recharge 3 |

Change between known nonhealing profiles using same HP fraction, slot, expiry and spent uses. Cannot turn a 1 slot device into two, refill ammo, reset trap, create fresh death trigger or morph drone into free bomb.

<details><summary>Preserved source wording — book line4638</summary>

Reconfiguration: Transform one deployed device into another type.

</details>

#### Field Fabrication

**Level 16 · selection · tinker.hero.techsmith.field-fabrication**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | One ordinary tool within reach | 1 hour | 1/short rest |

Create portable ladder 10 ft, hand tool set, pulley, brace or lockable box. No autonomous damage, explosive, rare material, magic item, permanent structure or cash value. Tool must fit one 5 ft square folded.

<details><summary>Preserved source wording — book line4639</summary>

Field Fabrication: Create a temporary gadget or tool to address a specific situation.

</details>

### Warmachine

#### Malfunction Field

**Level 10 · selection · tinker.hero.warmachine.malfunction-field**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Enemy within 5 ft of your device | While device active | Once/round total |

First spell attack by one enemy has disadvantage. Multiple devices do not multiply effect; area/spell-saves unchanged. Does not create antimagic zone.

<details><summary>Preserved source wording — book line4645</summary>

Malfunction Field: Enemies near your devices must roll twice on spell attacks and take the lower result.

</details>

#### Volatile Components

**Level 10 · selection · tinker.hero.warmachine.volatile-components**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One device destroyed by enemy; one enemy within 5 ft | Instant | Once/round |

Deal S fire to that enemy. Deliberate sacrifices, copied objects, friendly damage and secondary explosions cannot trigger. No other procs/resources from damage.

<details><summary>Preserved source wording — book line4646</summary>

Volatile Components: Your devices explode when destroyed, damaging nearby enemies.

</details>

#### Unstable Enhancements

**Level 10 · selection · tinker.hero.warmachine.unstable-enhancements**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One bomb you throw | Instant | Once/turn |

Before throw opt for unstable mix; d4=4 adds S d6 to one failed-save target but bomb cannot exclude allies, including Danger Close. Other roll ordinary bomb. Never double entire damage or secondary riders.

<details><summary>Preserved source wording — book line4647</summary>

Unstable Enhancements: Your bombs have a 25% chance to deal double damage but may affect allies.

</details>

#### Scrap Salvage

**Level 10 · selection · tinker.hero.warmachine.scrap-salvage**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP; enemy-destroyed device debris | Empty space within 5 ft of debris | 3 rounds | 1/encounter |

Create one Scrapling AC 12 HP L Speed 20 ft, commanded melee attack PB+INT for 1d6 bludgeoning. Counts as deployable slot/shared command. Consumed debris cannot be salvaged again; cannot spawn its own replacement.

<details><summary>Preserved source wording — book line4648</summary>

Scrap Salvage: Create temporary minions from destroyed devices.

</details>

#### Boomcore Drone

**Level 10 · selection · tinker.hero.warmachine.boomcore-drone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | One drone within 30 ft | 3 rounds | Recharge 4 |

Commanded bolts add 1d6 fire and on hit STR save or push 5 ft. Still one command and normal attack budget; no free activation attack or unlimited stacking.

<details><summary>Preserved source wording — book line4651</summary>

Boomcore Drone: Upgrade your drone to use blast bolts that deal damage and knockback.

</details>

#### Overpressure Bombs

**Level 12 · selection · tinker.hero.warmachine.overpressure-bombs**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | One bomb throw | Instant | Once/turn |

Add on failed initial save STR save or choose push 10 ftor Prone. Also add S damage to one failed-save target. No additional blast or compounded slow; do not stack with Thermobaric push.

<details><summary>Preserved source wording — book line4652</summary>

Overpressure Bombs: Your bombs gain knockback or prone effects with enhanced elemental damage.

</details>

#### Scrap Reaper

**Level 14 · selection · tinker.hero.warmachine.scrap-reaper**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 2 RP; one destroyed enemy-hit device | Debris within 30 ft | Until end next turn | 1/short rest |

Create one Scrapling Speed 30, AC 12 HP L; next Bonus Action command moves and detonates within 5 ft one enemy for 2 S d6 fire DEX half. Uses one command budget and ends. No chain from deliberate sacrifice or its own death.

<details><summary>Preserved source wording — book line4653</summary>

Scrap Reaper: When a turret or drone dies, summon a Scrapling that chases and explodes on enemies.

</details>

#### Volatile Injection

**Level 10 · selection · tinker.hero.warmachine.volatile-injection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP; device loses MHP | One functional device within 30 ft | Until end next turn | Recharge 3 |

Must have strictly more HP than cost. Its next damaging activation adds S d6 to one target; cannot combine with Overcharge, damage cannot be refunded by same activation. No resources gained from self damage.

<details><summary>Preserved source wording — book line4654</summary>

Volatile Injection: Temporarily boost a device's power at the cost of stability.

</details>

#### Catastrophic Overload

**Level 16 · selection · tinker.hero.warmachine.catastrophic-overload**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP; sacrifice one device | 10 ft radius about device within 60 ft | Instant | 1/long rest |

All creatures including allies DEX save, 3 S d6 fire plus 3 S d6 force on failure, half success. No critical hit, additional destruction proc, salvage, automatic stun or copied damage. Device ends before blast; no Safety exclusion.

<details><summary>Preserved source wording — book line4655</summary>

Catastrophic Overload: Sacrifice a device for a massive explosion that damages all nearby creatures.

</details>

#### Mech Overdrive

**Level 20 · automatic · tinker.supplement.mech-overdrive**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered on deploying a device | 1 long-rest use plus original deployment cost | One of your newly deployed devices | Until encounter end, maximum 1 minute | 1/long rest; automatic Hero capstone |

Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment.

Prerequisite: See class engine and progression.

<details><summary>Preserved source wording — book line4715</summary>

You begin with one deployable slot and gain additional slots as you level up. At level 20, you gain Mech Overdrive, allowing one device to become permanent for the duration of a battle.

</details>

## Source appendix and open balance questions

The complete original Tinker book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/tinker.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Does the shared command budget keep multiple devices useful but manageable?
- Are bomb stock and encounter allowances too much bookkeeping?
- Can Artificer support compete with damage without infinite healing?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
