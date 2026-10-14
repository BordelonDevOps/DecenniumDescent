# Dragoon — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/dragoon.json) · [Normalized card data](../../../data/public/class_playtests/dragoon.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Strength
- Secondary Attributes: Dexterity, Constitution
- Hit Points: High (10 + Constitution modifier at 1st level, 1d10 per level thereafter)
- Armor Proficiency: Light and medium armor
- Weapon Proficiency: Simple weapons, polearms (spears, glaives, tridents)
- Tool Proficiency: Leatherworker's tools

Strength is the class ability. Momentum starts/ends encounters at 0; cap 5, rising to 7 with Momentum Overflow or automatically at class 9. On each regular turn, moving at least 15 ft under your own power grants 1 Momentum, and damaging an enemy with a weapon attack grants 1 more. These are the only default gains; all gains/refunds together cap 2 per round. Forced movement, teleportation, movement in place, allies and summons cannot farm Momentum. Movement counts actual path traveled toward a tactical destination; one threshold per turn.

A leap technique moves you through an unobstructed arc to a visible unoccupied landing space within its range, adjacent to its target when attacking. Land during the same activation. It spends movement equal to horizontal distance, unless the card expressly supplies additional movement. A leap never gives flight, indefinite airborne immunity or free attacks. You cannot leap through ceilings/walls; vertical height is at most half the printed horizontal range. Safe technique landings do not cause self-fall damage; interrupted/falling travel follows ordinary falling rules. No bonus damage is earned by repeatedly dropping from a ledge.

All attack cards use a wielded polearm unless they explicitly describe a non-weapon save effect. A technique is its own Action, not an Attack Action plus free technique. At class 5 your ordinary Attack Action makes two attacks, at most two even when multiclass features overlap; each technique still gives only printed attacks. This automatic Extra Attack is a new explicit advancement specification for the pilot.

Armor bypass means the exact printed attack bonus or resistance exception, never subtracting a percentage of the target's whole AC. Critical ranges do not stack. A Dragoon can use only one free/Bonus Action leap granted by class features per round; it cannot trigger another free leap. Extra full Actions share the suite-wide cap. Reaction intercepts require a legal path and destination and do not rewind resolved damage.

Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard.

When casting an ordinary spell after moving at least 20 ft this turn, reduce that cast's Dissonance gain by 1, minimum 0; no automatic RP discount. Dragoon techniques are martial unless their card specifies elemental magic. Use Core V 2 RP and the Dragoon rank gates for separate spellcasting.

Use scheduled Base/Arch/Hero choices. Skybound Assault, Momentum Engine and related passives improve the automatic engine rather than unlock basic movement or generation. Lancer's Apex is automatic 9; at 10 choose Dragon Guardian, Drake Rider or Dragon Tyrant. The corresponding Final Flight is automatic 20. Apex Assault is an active technique despite its source passive heading.

**Protected source interface:** If the Dragoon moved at least 20 feet before a Weave cast, reduce that cast's Dissonance gain by 1 (minimum 0); Momentum carries the note through motion.

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
| 9 | Arch | 8 | 2 | Choose 1 Arch; automatic: Lancer's Apex |
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
| 20 | Hero | 20 | 4 | No ordinary selection; automatic: Bastion Descent (Dragon Guardian), Drakestorm Dive (Drake Rider), Sovereign Descent (Dragon Tyrant) |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Dragoon 5, STR 16, PB 3, S 2, M 3; start Momentum 0. Know Dragon Leap, Momentum Surge, Wyvern's Guard and Draconic Roar at 1; Momentum Engine and Draconic Discipline at 2; Dragonflight and Momentum Overflow at 3. Capacity 7.
2. Turn 1: Dragon Leap spends 0 Momentum and moves 20 ft of Speed 30. Weapon attack hits: movement+hit each gain 1, ending 2. It rolls weapon damage+2d6. Land immediately.
3. Turn 2: Bonus Action Momentum Surge spends 2, balance 0, increases movement. Move 20 ft and use ordinary Attack Action: first successful hit and movement return 2 total, even if both attacks hit. End 2.
4. Turn 3: Dragonflight costs 2, balance 0. It supplies movement up to 60 ft as part of the Action; hit and movement regain 2 within the common cap. End 2; no additional normal Attack Action.
5. Turn 4: if knocked prone, use Aerial Recovery only if known and your Reaction is available. Its 1 Momentum still counts toward the round gain cap. A second refund cannot exceed 2 total gains.
6. End encounter: Momentum 0. RP, per-rest uses and other party resources do not refill.

## Base cards

#### Skybound Assault

**Level 1 · selection · dragoon.base.skybound-assault**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One target hit by your leap | Instant | Once/own turn |

After a leap moves at least 15 ft and its attack hits, add S damage. Its hit grants ordinary Momentum, not an extra point. This benefit cannot trigger from forced movement or a leap granted by this same feature.

<details><summary>Preserved source wording — book line2277</summary>

Skybound Assault: Leap to a target and deal +25% damage. Grants 1 Momentum.

</details>

#### Draconic Discipline

**Level 1 · selection · dragoon.base.draconic-discipline**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Gain advantage on saves against being knocked Prone or forcibly moved. It does not protect against Stunned, spell damage or grappling unless the save also imposes one of those named effects.

<details><summary>Preserved source wording — book line2278</summary>

Draconic Discipline: Gain +10% resistance to knockback and crowd control.

</details>

#### Momentum Engine

**Level 1 · selection · dragoon.base.momentum-engine**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | This turn | Once/own turn |

After your first 15 ft of voluntary movement generates Momentum, ignore the next 5 ft of nonmagical difficult terrain this turn. The movement threshold itself is automatic class engine; this feature does not create another gain trigger.

<details><summary>Preserved source wording — book line2279</summary>

Momentum Engine: Movement of 3+ tiles in a turn grants 1 Momentum (Max 5).

</details>

#### Dragoon's Reach

**Level 1 · selection · dragoon.base.dragoon-s-reach**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Polearm weapon attacks | While known | Continuous |

Increase your wielded polearm's reach by 5 ft, maximum 15 ft. Once/own turn a natural 19 polearm attack that hits critically hits. It does not extend the range of other abilities or stack with another critical-range expansion.

<details><summary>Preserved source wording — book line2280</summary>

Dragoon's Reach: Polearm attacks strike 1 tile further and have +5% crit chance.

</details>

#### Aerial Poise

**Level 1 · selection · dragoon.base.aerial-poise**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | Self during an actual leap | This damage instance | Once/round |

When a ranged attack hits you during your leap movement, halve its damage. You must spend the Reaction before damage resolves. Remaining airborne between turns cannot be declared to keep this protection active.

<details><summary>Preserved source wording — book line2281</summary>

Aerial Poise: While airborne, take 25% reduced damage from ranged attacks.

</details>

#### Dragon Leap

**Level 1 · selection · dragoon.base.dragon-leap**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One polearm enemy at landing point within 30 ft | Instant | Recharge 2 |

Leap, spending normal movement, then make one polearm attack. On hit add S d6 weapon-type damage. Legal movement and a hit may each grant 1 Momentum under the common cap. Land immediately; height never adds unbounded damage.

<details><summary>Preserved source wording — book line2284</summary>

Dragon Leap: Launch yourself into the air and come crashing down on a target up to 30 feet away, dealing damage based on your Strength and height.

</details>

#### Piercing Thrust

**Level 1 · selection · dragoon.base.piercing-thrust**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 Momentum | One enemy in polearm reach | Instant | Recharge 2 |

Make one polearm attack with+2 to the attack roll. On hit add S d4 weapon damage. This is the complete armor-piercing benefit; no percentage of AC is removed and critical range is unchanged.

<details><summary>Preserved source wording — book line2285</summary>

Piercing Thrust: A powerful spear attack that partially ignores enemy armor and has increased critical hit chance.

</details>

#### Wyvern's Guard

**Level 1 · selection · dragoon.base.wyvern-s-guard**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 Momentum | Self | Until start next turn | Recharge 2 |

The next attack that damages you has damage reduced by S d6+M, minimum 0; then the guard ends. Roll the reduction only when damage occurs. This reduction cannot heal or reflect damage.

<details><summary>Preserved source wording — book line2286</summary>

Wyvern's Guard: Enter a defensive stance that increases your resistance to damage from the next attack.

</details>

#### Momentum Surge

**Level 1 · selection · dragoon.base.momentum-surge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 Momentum | Self | Until end current turn | Recharge 2 |

Gain+15 ft Speed and+1 on your next polearm attack this turn. Spend before moving; movement may then generate normal Momentum. Grants no attack, extra Action, Bonus Action or Reaction.

<details><summary>Preserved source wording — book line2287</summary>

Momentum Surge: Consume 2 Momentum to gain a burst of speed and +1 to your next attack roll.

</details>

#### Draconic Roar

**Level 1 · selection · dragoon.base.draconic-roar**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 Momentum | Up to 3 enemies and 3 allies within 15 ft that hear you | Until end your next turn | Recharge 3 |

Enemies make WIS saves; failure Frightened of you. Chosen allies gain advantage on their next save against Frightened before duration ends. A creature may repeat the WIS save at its turn end, ending fear on success.

<details><summary>Preserved source wording — book line2288</summary>

Draconic Roar: Release a intimidating battle cry that can frighten weaker enemies and rally allies.

</details>

## Arch cards

#### Crater Strike

**Level 3 · selection · dragoon.arch.crater-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 1 Momentum | Up to 2 enemies within 5 ft of your leap landing | Instant | Once/own turn |

After your leap attack hits, optionally pay 1; each selected adjacent enemy makes STR save or falls Prone. No additional weapon damage or Momentum gain. Landing on an occupied space is not permitted.

<details><summary>Preserved source wording — book line2294</summary>

Crater Strike: Leap attack that applies knockdown in a small AoE.

</details>

#### Momentum Overflow

**Level 3 · selection · dragoon.arch.momentum-overflow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Momentum cap becomes 7 early; cap becomes 7 for all Dragoons at 9. When starting a weapon technique with 6 or 7 Momentum, its first hit adds 1d6 damage before costs are deducted. Once/own turn, not per point above 5; no stored overflow beyond 7.

<details><summary>Preserved source wording — book line2295</summary>

Momentum Overflow: Exceed Momentum cap (Max 7), bonus damage scales with overflow.

</details>

#### Piercing Howl

**Level 3 · selection · dragoon.arch.piercing-howl**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 Momentum | Self; next polearm attack | Until end current turn | Recharge 3 |

Your next polearm attack gains+2 to hit and ignores resistance to its weapon damage type. Immunity remains. It does not ignore shields, natural armor, cover or arbitrary halves of AC.

<details><summary>Preserved source wording — book line2296</summary>

Piercing Howl: Next polearm strike ignores 50% armor.

</details>

#### Lance Tempo

**Level 3 · selection · dragoon.arch.lance-tempo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until start next turn | Once/own turn |

After moving 15 ft voluntarily, gain+1 AC. If you critically hit with a polearm that turn, add 1d6 weapon damage once. The added die does not double itself or create further critical triggers.

<details><summary>Preserved source wording — book line2297</summary>

Lance Tempo: If you moved this turn, gain +10% evasion and +10% crit damage.

</details>

#### Wyvern's Flow

**Level 5 · selection · dragoon.arch.wyvern-s-flow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self after a damaging leap hit | Instant | Once/round |

Regain 1 Momentum within the total 2-per-round gain cap, and shorten one OTHER positive leap cooldown by 1. Shortening uses that ability's reset allowance. No free leap or Action follows.

<details><summary>Preserved source wording — book line2298</summary>

Wyvern's Flow: Successful leaps refund 1 Momentum and reduce next cooldown by 1.

</details>

#### Apex Assault

**Level 7 · selection · dragoon.arch.apex-assault**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | All Momentum, minimum 3 | One enemy in polearm reach after leap up to 30 ft | Instant | Recharge 4 |

Spend K Momentum and leap using normal movement. Make one polearm attack; on hit add min(K, 5)d6 weapon damage. On a miss no bonus damage; expenditure remains. Gains from this activation cannot exceed the common cap.

<details><summary>Preserved source wording — book line2299</summary>

Apex Assault: Ultimate leap: high damage finisher that consumes all Momentum.

</details>

#### Lancer's Apex

**Level 9 · automatic · dragoon.arch.lancer-s-apex**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | All Momentum at current maximum; 1 short-rest use | Self; one known non-Finale leap | This activation | 1/short rest |

Before paying the leap's Momentum cost, spend all maximum Momentum instead and use that leap as a Bonus Action, still paying other costs. It cannot trigger another free leap. Damage and hit generation use ordinary caps; this grants no extra Bonus Action.

<details><summary>Preserved source wording — book line2300</summary>

Capstone – Lancer's Apex: Leap attacks now cost no action if performed at max Momentum (1/encounter).

</details>

#### Dragonflight

**Level 3 · selection · dragoon.arch.dragonflight**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 Momentum | One enemy adjacent to landing within 60 ft | Instant | Recharge 3 |

Leap up to 60 ft as additional movement supplied by this Action. Make one polearm attack on landing; on hit add(S+1)d6 weapon damage. No damage scaling from distance/height and no remaining flight.

<details><summary>Preserved source wording — book line2303</summary>

Dragonflight: An enhanced leap ability that allows you to jump twice as high and far, with increased damage based on distance traveled.

</details>

#### Spear Cyclone

**Level 3 · selection · dragoon.arch.spear-cyclone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 Momentum | Up to 3 distinct enemies in polearm reach | Instant | Recharge 3 |

Make one polearm attack against each. No target is attacked twice. Hit-based Momentum can be gained only once this turn regardless of number of hits; movement and refund caps still apply.

<details><summary>Preserved source wording — book line2304</summary>

Spear Cyclone: Spin your polearm in a wide arc, striking all enemies within range and building Momentum for each hit.

</details>

#### Momentum Burst

**Level 5 · selection · dragoon.arch.momentum-burst**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | All Momentum, minimum 2 | Self | Until end current turn | Recharge 3 |

Spend K Momentum. Next polearm hit this turn adds min(K, 4)d6 weapon damage. If the next attack misses the effect ends. It does not widen critical range or multiply another added damage package.

<details><summary>Preserved source wording — book line2305</summary>

Momentum Burst: Consume all Momentum to gain a significant boost to your next attack's damage and critical hit chance.

</details>

#### Aerial Recovery

**Level 3 · selection · dragoon.arch.aerial-recovery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | Self just knocked Prone or pushed | Instant | Recharge 2 |

After the triggering displacement resolves, stand from Prone without movement cost and move 5 ft to an unoccupied space without provoking opportunity attacks. Gain 1 Momentum within the round cap. Cannot prevent falling without a legal landing.

<details><summary>Preserved source wording — book line2306</summary>

Aerial Recovery: After being knocked down or back, instantly regain your footing and gain 1 Momentum.

</details>

#### Dragon's Eye

**Level 7 · selection · dragoon.arch.dragon-s-eye**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 Momentum | One visible enemy within 60 ft | Until end next turn | Recharge 3 |

Study it: your first polearm attack against it has advantage, and you learn one of its visible damage resistances if any. No automatic critical, secret full stat block or ability to attack through cover.

<details><summary>Preserved source wording — book line2307</summary>

Dragon's Eye: Briefly gain the keen vision of a dragon, allowing you to spot weaknesses in enemy defenses and increase your critical hit range.

</details>

## Hero cards

### Dragon Guardian

#### Aegis Leap

**Level 10 · selection · dragoon.hero.dragon-guardian.aegis-leap**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 2 Momentum | Ally within 15 ft targeted by an attack | One attack | Recharge 2 |

Before the attack roll, leap to an empty space adjacent to ally using this supplied movement. Become the target if the attack can reach you; resolve against your AC. Cannot be used if restrained or no path. Counts as your one intercept reaction.

<details><summary>Preserved source wording — book line2316</summary>

Aegis Leap: Leap to an ally and intercept the next attack made against them.

</details>

#### Wyrmhide

**Level 10 · selection · dragoon.hero.dragon-guardian.wyrmhide**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self while above half maximum HP | While threshold met | Continuous |

Reduce each damage instance by 2 and gain advantage on CON saves against Bleed, Burn and Poisoned. No blanket condition immunity; effects already present persist and ordinary nonstacking reduction applies.

<details><summary>Preserved source wording — book line2317</summary>

Wyrmhide: Gain +10% DR and immunity to Bleed/Burn/Poison while above 50% HP.

</details>

#### Momentum Shield

**Level 10 · selection · dragoon.hero.dragon-guardian.momentum-shield**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until start next turn | Once/own turn |

After spending at least 1 Momentum, gain temporary HP equal to amount spent+M, maximum 10. Later expenditure replaces with the higher remaining value; no real HP restoration.

<details><summary>Preserved source wording — book line2318</summary>

Momentum Shield: Spending Momentum grants temporary HP.

</details>

#### Spiral Defense

**Level 10 · selection · dragoon.hero.dragon-guardian.spiral-defense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 Momentum | Melee attacker in polearm reach that misses you while at maximum Momentum | Instant | Once/round |

Make one polearm attack. Pay Momentum after checking the maximum prerequisite. This counter grants no Momentum and cannot trigger another counter or leap. It consumes your ordinary Reaction.

<details><summary>Preserved source wording — book line2319</summary>

Spiral Defense: Automatically counter melee attacks with a polearm when at max Momentum.

</details>

#### Bastion Descent

**Level 20 · automatic · dragoon.hero.dragon-guardian.bastion-descent**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 Momentum; 1 long-rest use | Leap within 30 ft; up to 6 allies within 15 ft of landing | Instant; protection until start next turn | 1/long rest |

Land in empty space. Chosen allies gain 4d8+M temporary HP and may end Frightened or Poisoned. They gain resistance to the next damage instance before your next turn. No healing, resurrection or removal of Wounds.

<details><summary>Preserved source wording — book line2320</summary>

Final Flight – Bastion Descent: Slam down between allies, cleansing effects and shielding the group.

</details>

#### Guardian's Intercept

**Level 10 · selection · dragoon.hero.dragon-guardian.guardian-s-intercept**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 2 Momentum | Ally within 30 ft being hit by an attack | One attack | Recharge 3 |

Leap adjacent before damage, becoming the target of that already successful hit; halve damage to you after normal mitigation. No new roll against your AC. Requires legal path/landing. You cannot also use Aegis Leap on the same attack.

<details><summary>Preserved source wording — book line2323</summary>

Guardian's Intercept: Leap to an ally's position and take the next attack targeted at them, with reduced damage to yourself.

</details>

#### Draconic Ward

**Level 10 · selection · dragoon.hero.dragon-guardian.draconic-ward**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Momentum | Self and up to 3 allies within 10 ft | Concentration, 3 of your turns | Recharge 4 |

Project a ward: chosen creatures while within 10 ft reduce damage by S, minimum 0. The reduction does not stack with Wyrmhide or another flat class reduction. No passive healing or extra Actions.

<details><summary>Preserved source wording — book line2324</summary>

Draconic Ward: Channel draconic energy to create a protective aura around yourself and nearby allies, reducing incoming damage.

</details>

#### Wyrmscale Defense

**Level 12 · selection · dragoon.hero.dragon-guardian.wyrmscale-defense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 Momentum | Self | Until end next turn | Recharge 4 |

Gain resistance to bludgeoning, piercing and slashing and advantage on saves against Poisoned, Frightened and Stunned. This is not immunity; existing conditions still require their ordinary removal.

<details><summary>Preserved source wording — book line2325</summary>

Wyrmscale Defense: Temporarily harden your skin like dragon scales, gaining significant damage reduction and status effect resistance.

</details>

#### Momentum Barrier

**Level 14 · selection · dragoon.hero.dragon-guardian.momentum-barrier**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | All Momentum, minimum 3 | Up to 4 allies within 15 ft | Temporary HP 1 minute | Recharge 4 |

Spend K Momentum. Each gains K+S d6 temporary HP, using one shared dice roll. These HP do not stack with other shields and no unspent Momentum remains. This is not concentration.

<details><summary>Preserved source wording — book line2326</summary>

Momentum Barrier: Convert your Momentum into a protective shield that absorbs damage for you and nearby allies.

</details>

#### Dragon's Sanctuary

**Level 16 · selection · dragoon.hero.dragon-guardian.dragon-s-sanctuary**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 Momentum; 1 long-rest use | Fixed 15 ft-radius zone centered within 30 ft; up to 6 allies | Concentration, 3 of your turns | 1/long rest |

Chosen allies inside reduce damage by 5 and have advantage against Frightened/Charmed. On start and each of your next 2 turns, Bonus Action lets one ally inside repeat one save against a present Frightened, Charmed or Poisoned effect. No automatic mass cleanse each turn.

<details><summary>Preserved source wording — book line2327</summary>

Dragon's Sanctuary: Ultimate ability that creates a zone of protection, significantly reducing damage to all allies within range and cleansing negative effects.

</details>

### Drake Rider

#### Drake Mark

**Level 10 · selection · dragoon.hero.drake-rider.drake-mark**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One creature hit by your leap | Until end next turn | Once/own turn |

Mark that creature; your first subsequent direct polearm hit adds S damage. A new mark replaces old. No extra damage to the triggering leap, Do Ts or copies; it is not a spell mark.

<details><summary>Preserved source wording — book line2333</summary>

Drake Mark: Each leap attack marks enemies. Marked enemies take +10% damage from you.

</details>

#### Elemental Spearcraft

**Level 10 · selection · dragoon.hero.drake-rider.elemental-spearcraft**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 Momentum | Wielded polearm | 3 of your turns | Recharge 3 |

Choose fire, cold or lightning. Once/own turn one polearm hit adds 1d6 chosen damage. Switching requires a new activation and full cost. Does not stack with Elemental Lance's bonus; use stronger.

<details><summary>Preserved source wording — book line2334</summary>

Elemental Spearcraft: Infuse polearms with Fire, Ice, or Lightning for 3 turns (switchable).

</details>

#### Air Mastery

**Level 10 · selection · dragoon.hero.drake-rider.air-mastery**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Once/round shortening |

Increase leap range by 10 ft, not vertical ceiling penetration or flight. After a successful leap hit, shorten one OTHER positive leap cooldown by 1 using its reset allowance. Does not combine with Wyvern's Flow on the same counter in a round.

<details><summary>Preserved source wording — book line2335</summary>

Air Mastery: Gain +20% jump range and 10% reduced cooldown on leap skills.

</details>

#### Momentum Tempo

**Level 14 · selection · dragoon.hero.drake-rider.momentum-tempo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 3 additional Momentum; 1 short-rest use | Self after spending at least 3 Momentum on a technique this turn | Next regular turn only | 1/short rest |

Pay 3 additional Momentum now to gain one extra full Action on your next turn. Shared cap applies; it cannot grant another Action or another Momentum Tempo. Triggering technique must have been paid without this additional cost. No queued actions.

<details><summary>Preserved source wording — book line2336</summary>

Momentum Tempo: After spending 3+ Momentum in a round, gain an extra action next turn.

</details>

#### Drakestorm Dive

**Level 20 · automatic · dragoon.hero.drake-rider.drakestorm-dive**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 Momentum; 1 long-rest use | Leap up to 60 ft; up to 6 enemies within 15 ft of landing | Instant | 1/long rest |

Choose fire/cold/lightning. DEX save:6d8 chosen damage, half on success. On failure fire applies Burn, cold reduces Speed 10 ft until end next turn, lightning prevents Reactions until then. Land in legal empty space; no additional weapon attack.

<details><summary>Preserved source wording — book line2337</summary>

Final Flight – Drakestorm Dive: Choose an element and leap into a group, triggering a large AoE blast.

</details>

#### Elemental Lance

**Level 10 · selection · dragoon.hero.drake-rider.elemental-lance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 Momentum | Your polearm | 3 of your turns | Recharge 3 |

Choose fire/cold/lightning. Once/own turn a hit adds S d4 damage; fire adds 1 damage, cold reduces target Speed 5 ft until end next turn, lightning denies opportunity attacks until start its next turn. Nonstacking with Spearcraft; one element rider/turn.

<details><summary>Preserved source wording — book line2340</summary>

Elemental Lance: Infuse your weapon with elemental energy (fire, ice, or lightning), adding additional damage and effects to your attacks.

</details>

#### Drake's Agility

**Level 10 · selection · dragoon.hero.drake-rider.drake-s-agility**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 Momentum | Self | This turn | Recharge 3 |

Gain+20 ft Speed and may replace 10 ft of normal movement with a leap of 10 ft horizontally/5 ft vertically. This is movement only, not another leap attack or technique. No new Action or attack is granted.

<details><summary>Preserved source wording — book line2341</summary>

Drake's Agility: Channel the speed of a drake, significantly increasing your movement speed and allowing an additional leap this turn.

</details>

#### Aerial Combo

**Level 12 · selection · dragoon.hero.drake-rider.aerial-combo**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Momentum | Up to 2 enemies adjacent to legal landings within 30 ft | Instant | Recharge 3 |

Leap to first target, attack once, then leap up to 15 ft to second and attack once. All movement supplied by Action; two attacks maximum even with Extra Attack. Add 1d6 to each hit. Only one hit-generated Momentum per turn.

<details><summary>Preserved source wording — book line2342</summary>

Aerial Combo: Perform a rapid series of attacks while airborne, building and consuming Momentum with each strike.

</details>

#### Elemental Adaptation

**Level 14 · selection · dragoon.hero.drake-rider.elemental-adaptation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 Momentum | Self | Concentration, 3 of your turns | Recharge 4 |

Choose fire/cold/lightning: gain resistance to that type and may convert normal polearm weapon damage to it. This adds no damage and cannot combine with another resistance multiplicatively. Choice fixed for duration.

<details><summary>Preserved source wording — book line2343</summary>

Elemental Adaptation: Temporarily gain resistance to a chosen element and infuse your attacks with that element.

</details>

#### Drakestorm

**Level 16 · selection · dragoon.hero.drake-rider.drakestorm**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 Momentum; 1 long-rest use | Moving 10 ft aura; up to 3 enemies per pulse | Concentration, 3 of your turns | 1/long rest |

Choose element. Start and on each of next 2 turns, Bonus Action pulses S d6 damage, DEX half. During duration Speed+10 ft. No free weapon attacks or Momentum from pulse damage; maximum 3 pulses.

<details><summary>Preserved source wording — book line2344</summary>

Drakestorm: Ultimate ability that summons a swirling storm of elemental energy around you, dealing damage to nearby enemies and enhancing your mobility.

</details>

### Dragon Tyrant

#### Tyrant's Crash

**Level 10 · selection · dragoon.hero.dragon-tyrant.tyrant-s-crash**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 1 Momentum | Up to 2 enemies within 5 ft of your leap landing | Until end target's next turn | Once/own turn |

After a leap hit pay 1. Targets make WIS save; on failure Frightened and-1 AC. Save repeated at each turn end ends both. This neither stacks AC penalties nor affects enemies beyond the printed area.

<details><summary>Preserved source wording — book line2350</summary>

Tyrant's Crash: Leap attack applies Fear and Sunder Armor in an AoE.

</details>

#### Momentum Feeder

**Level 10 · selection · dragoon.hero.dragon-tyrant.momentum-feeder**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self on polearm critical or hostile kill | Instant | Once/round |

Gain 2 Momentum, still within total 2-per-round gain cap. A critical kill is one trigger, not two. Do Ts, copies, allies, summons and helpless creatures cannot trigger it.

<details><summary>Preserved source wording — book line2351</summary>

Momentum Feeder: Killing or critting grants +2 Momentum.

</details>

#### Wyrmblood Surge

**Level 10 · selection · dragoon.hero.dragon-tyrant.wyrmblood-surge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until end next turn | Once/own turn |

After spending Momentum, your next direct polearm hit adds damage equal to points spent, maximum 5. Further spending replaces rather than adds this bonus. It is flat damage and grants no resource refund.

<details><summary>Preserved source wording — book line2352</summary>

Wyrmblood Surge: Each Momentum spent grants +5% damage for the next 2 turns.

</details>

#### Skypiercer Stance

**Level 10 · selection · dragoon.hero.dragon-tyrant.skypiercer-stance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Increase leap vertical clearance allowance by 10 ft, never through solid obstacles. Once/own turn a natural 19 polearm hit critically hits; use the broadest critical range rather than stacking. It does not let you remain flying.

<details><summary>Preserved source wording — book line2353</summary>

Skypiercer Stance: Gain passive +15% crit and ignore height restrictions on leaps.

</details>

#### Sovereign Descent

**Level 20 · automatic · dragoon.hero.dragon-tyrant.sovereign-descent**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 5 Momentum; 1 long-rest use | Leap up to 60 ft; up to 6 enemies within 15 ft | Instant; conditions as stated | 1/long rest |

STR save:6d8 bludgeoning, half on success. Failure knocks Prone and applies one Bleed and Burn. Failure by 10 also Stuns until end target's next turn, subject to denial cap. Ground becomes difficult terrain for 1 minute; no destruction of structural supports.

<details><summary>Preserved source wording — book line2354</summary>

Final Flight – Sovereign Descent: Break the ground in a large radius, stunning enemies and applying Bleed and Burn. (1/rest)

</details>

#### Tyrant's Impale

**Level 10 · selection · dragoon.hero.dragon-tyrant.tyrant-s-impale**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 Momentum | One enemy in polearm reach | Instant; pin until end next turn | Recharge 3 |

Weapon attack; hit adds S d6 piercing. A hit creature no more than one size larger makes STR save or is Restrained and Bleeding. It may use Action STR(Athletics) or DEX(Acrobatics) versus class DC to end restraint. You must stay in reach to maintain pin.

<details><summary>Preserved source wording — book line2357</summary>

Tyrant's Impale: A devastating attack that can pin weaker enemies to the ground, preventing movement and causing bleeding damage.

</details>

#### Draconic Dominance

**Level 10 · selection · dragoon.hero.dragon-tyrant.draconic-dominance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 Momentum | Up to 3 enemies within 30 ft that hear you | Until end your next turn | Recharge 3 |

WIS save or Frightened; each repeats save at its turn end. On failure by 10 it must use up to 10 ft of its next normal movement away from you by a safe route, not a full Action or hazardous compulsory movement.

<details><summary>Preserved source wording — book line2358</summary>

Draconic Dominance: Channel the terrifying presence of a dragon, causing fear in nearby enemies and potentially causing them to flee.

</details>

#### Momentum Rampage

**Level 12 · selection · dragoon.hero.dragon-tyrant.momentum-rampage**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 Momentum | Self | 3 of your turns | Recharge 4 |

Once/own turn your first polearm hit adds S d6 damage. Gain+10 ft Speed but suffer-1 AC. No extra attacks, Actions, crit range or scaling from an unbounded resource count.

<details><summary>Preserved source wording — book line2359</summary>

Momentum Rampage: Enter a state of draconic fury, gaining increased damage and attack speed based on your current Momentum.

</details>

#### Terrain Shatter

**Level 14 · selection · dragoon.hero.dragon-tyrant.terrain-shatter**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 Momentum | Up to 4 enemies in 10 ft radius centered within polearm reach | Instant; terrain 1 minute | Recharge 4 |

STR save: (S+1)d6 bludgeoning, half on success; failure Prone. Ground becomes difficult terrain, excluding reinforced structures and magical floors. This creates neither a pit nor free falling damage.

<details><summary>Preserved source wording — book line2360</summary>

Terrain Shatter: A powerful ground strike that damages enemies in an area and creates difficult terrain.

</details>

#### Wyrmking's Wrath

**Level 16 · selection · dragoon.hero.dragon-tyrant.wyrmking-s-wrath**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 4 Momentum; 1 long-rest use | Self | 3 of your turns | 1/long rest |

Your first leap technique each turn costs 1 less Momentum, minimum 1, and its first hit adds 1d8 damage. Once during duration convert one non-Finale Action leap to Bonus Action, paying costs; consumes your one free/Bonus Action leap allowance and grants no extra Action.

<details><summary>Preserved source wording — book line2361</summary>

Wyrmking's Wrath: Ultimate ability that channels pure draconic power, greatly enhancing your leap attacks and allowing rapid successive jumps for a short duration.

</details>

## Source appendix and open balance questions

The complete original Dragoon book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/dragoon.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Does Momentum stay available without trivial back-and-forth movement?
- Do Guardian intercepts compete fairly for Reactions?
- Are Tyrant area attacks and Rider extra Actions bounded at high level?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
