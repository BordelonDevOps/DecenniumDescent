# Ranger — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/ranger.json) · [Normalized card data](../../../data/public/class_playtests/ranger.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Dexterity
- Secondary Attribute: Wisdom
- Hit Points: Medium (8 + Constitution modifier at 1st level, 1d8 per level thereafter)
- Armor Proficiency: Light and medium armor (no plate)
- Weapon Proficiency: Longbows, shortbows, spears, dual-wielded blades
- Tool Proficiency: Survival tools, herbalism kit

Dexterity governs weapons; Wisdom governs primal technique DC/M. This draft uses the detailed book's d8 Hit Die; older runtime d10 remains preserved as a conflicting alternative. At 1 gain Track Target engine: Bonus Action mark one perceived enemy within 90 ft for 1 minute, no RP, one quarry at a time; new mark replaces old. Once/own turn a weapon hit against quarry adds S damage. Mark does not reveal creatures through total cover. Track Target selection is an upgrade, not a second unlock tax.

Weapon Synergy tracks last successful direct weapon hit on your own turns. Changing melee→ranged grants+1 to that ranged attack roll if it is your first attack of the turn; changing ranged→melee makes the hit apply Bleed 1d4 on target's next 2 turns. Once/turn synergy; Do Ts, copies, companions, forced attacks and misses do not advance it. At 5 ordinary Attack Action makes two attacks; techniques use only printed counts. You may draw/stow one weapon as normal object interaction; Dual Style later improves this.

Elemental Attunement is defensive; Elemental Imbue is the separate Pathfinder feature gated 6. Imbue Bonus Action 2 RP, one element for 3 of your turns; once/turn a weapon hit adds 1d4 of chosen element plus fire:Burn 1d4 next target turn, cold:Speed-10 ft until end next turn, poison:CON save or-1 attack rolls until end next turn. Nonstacking; Do Ts never build Hit Chain. Switching element pays again.

Druidic Arrow Combo starts at Ranger 11, not at Base 1. Each direct successful weapon hit adds 1 Hit Chain, maximum 2 gained per regular turn and cap 3. Completing 3 primes one Arrow until end next turn; using it consumes the chain, even on miss. Efficient Killer lowers threshold 2. Chain starts/ends encounters 0, cannot be stocked against allies/captives/summons and is cleared by incapacitation. The Arrow is one Action with a ranged weapon attack or the stated save, costs 0 RP when primed, and is a magical class technique rather than an ordinary spell cast. At most one Arrow per round; it cannot advance its own chain. It requires a wielded bow and ammunition. Ordinary attack/damage riders apply once as printed, never another free arrow.

All Rangers learn five bounded Arrows at 11. Emberroot requires the previous 3 successful weapon hits carried fire imbue: ranged attack, weapon+S d6 fire on hit; up to 2 others within 5 ft take S fire, and primary target Burns 1d4 next turn. Glacial Thorn requires 2 ranged+1 melee among those 3 hits: ranged attack weapon+S d6 cold; on hit STR save or Speed 0 until end next turn. Venomlash requires poisoned/blighted terrain at you or target: ranged attack weapon+S d6 poison; on hit CON save or-1 damage on its next attack. Spirit Fang requires quarry: ranged attack at advantage, weapon+S d6 force; ignores resistance but not immunity on the added force only. Cleansing Grove requires natural terrain at you or target: up to 3 living allies within 10 ft of a point within 60 ft each end Frightened or Poisoned; no attack or damage.

Chosen Hero grants a sixth Arrow at 11. Warder Nature's Wrath: ranged attack weapon+S d6 piercing; up to 2 allies within 10 ft gain M temporary HP (finite mitigation, not repeatable real healing). Stalker Phantom: two ranged attacks against different aligned targets within 60 ft, each weapon damage, no extra dice; one Arrow activation. Outrider Corruption: place 10 ft-radius zone within 60 ft, concentration until start next turn; up to 3 enemies entering/starting there take S d4 necrotic once each, CON half. Arrow copies cannot generate extra attacks, resources or permanent terrain changes.

A successful direct weapon hit between ordinary spell casts clears Refrain and gives the next ordinary spell before end next turn 1 less Dissonance, minimum 0. The benefit is single-use/nonstacking; it reduces neither RP nor both base and repeat separately. Ordinary spells use Ranger rank gates and the shared test magic configuration.

Base choices 1–2, Pathfinder Arch 3–9, and chosen Warder/Stalker/Outrider Hero 10–20 are distinct stages. No source Arch capstone/Finale exists: level 9 receives its normal eligible choice, while 20 automatically improves your Hero Arrow once/long rest (new capstone below). Do not acquire a Hero by spending Base choices. Beast Companion is one permanent bond; it must be a willing/tamed noncorrupted beast with INT<7 and CR no greater than your class level. Its combat profile uses the bounded companion below rather than importing a full CR 20 monster.

If a primed Arrow expires unused, the prime ends and Hit Chain resets to 0. This applies equally to Efficient Killer’s threshold of two. Efficient Killer itself requires Ranger 11, when Hit Chain exists.

**Protected source interface:** A successful weapon hit between spell casts clears Refrain and reduces the next spell's Dissonance gain by 1 (minimum 0), rewarding the Ranger's martial/primal cadence.

## Advancement and resources

RP authority: Direct Core Systems V2 table. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 1 | 0 | Choose 4 Base; at least 2 active |
| 2 | Base | 2 | 1 | Choose 2 Base |
| 3 | Arch | 3 | 1 | Choose 2 Arch; at least 1 active |
| 4 | Arch | 4 | 1 | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 6 | 2 | Choose 1 Arch |
| 6 | Arch | 8 | 2 | Choose 1 Base/Arch |
| 7 | Arch | 10 | 2 | Choose 1 Arch |
| 8 | Arch | 12 | 2 | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 14 | 3 | Choose 1 Arch |
| 10 | Hero | 16 | 3 | Choose 2 Hero; at least 1 active |
| 11 | Hero | 18 | 3 | Choose 1 Base/Arch |
| 12 | Hero | 20 | 3 | Choose 1 Hero; ASI or feat |
| 13 | Hero | 22 | 4 | Choose 1 Base/Arch |
| 14 | Hero | 24 | 4 | Choose 1 Hero |
| 15 | Hero | 26 | 4 | Choose 1 Base/Arch |
| 16 | Hero | 28 | 4 | Choose 1 Hero; ASI or feat |
| 17 | Hero | 30 | 5 | Choose 1 Base/Arch |
| 18 | Hero | 32 | 5 | Choose 1 Hero |
| 19 | Hero | 34 | 5 | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 36 | 5 | No ordinary selection; automatic: Master of the Hunt — new Hero capstone |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Ranger 11, DEX 18, WIS 16, PB 4, S 3, M 3, RP 18. Track quarry with Bonus Action; no RP spent. Start Hit Chain 0.
2. Turn 1 normal Attack Action has 2 attacks; both hit quarry, chain 0→2. Apply quarry bonus 3 once, not twice. No Arrow until next qualifying hit.
3. Turn 2 first weapon attack hits, chain 2→3 and primes Arrow. You already spent your Action on Attack, so cannot freely add an Arrow. An extra Action from an ally would use the shared cap, but none is assumed.
4. Turn 3 use Spirit Fang Arrow as Action, consume chain 3→0, pay 0 RP. On hit weapon+3d6 force; advantage does not double damage. The Arrow cannot rebuild its own chain.
5. Turn 4 cast an ordinary rank 1 spell after the previous direct weapon hit between casts. Pay 2 RP, RP 18→16 plus any pre-existing strain surcharge. Its base 1 D is reduced by 1 to 0; the one-use cadence benefit ends.
6. On encounter end unused chain and mark expire. RP does not refill. Natural-terrain healing and companions still need their printed finite costs.

## Base cards

#### Weapon Bond

**Level 1 · selection · ranger.base.weapon-bond**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Ritual | 0; 1 hour during rest | One bow or pair of blades touched | Until rebonded | One bond |

Bond weapons. Bonus Action summons one bonded weapon to your hand from within 30 ft if not held by another creature and no total cover. Cannot disarm someone or cross planar boundaries; bond no additional items.

<details><summary>Preserved source wording — book line3841</summary>

Weapon Bond: Form a special connection with either a bow or a pair of blades, allowing you to summon them to your hand.

</details>

#### Track Target

**Level 1 · selection · ranger.base.track-target**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your quarry | While marked | Continuous |

You have advantage on Survival checks to follow its physical tracks for 1 hour after the mark ends. While it is marked, once/turn your first hit also ignores 2 points of nonmagical flat damage reduction. Does not pierce immunity or reveal through cover.

<details><summary>Preserved source wording — book line3842</summary>

Track Target: Mark an enemy to deal +10% damage and enable special abilities against them.

</details>

#### Natural Explorer

**Level 1 · selection · ranger.base.natural-explorer**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Advantage on Survival checks in natural terrain; ignore nonmagical difficult terrain caused by vegetation, loose earth, mud or snow. Magical terrain, climbing and hazards still require their own rules.

<details><summary>Preserved source wording — book line3843</summary>

Natural Explorer: Gain advantage on Survival checks and move normally through difficult natural terrain.

</details>

#### Keen Senses

**Level 1 · selection · ranger.base.keen-senses**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self in natural terrain | While known | Continuous |

Gain+2 Perception and passive Perception. You still need a sense that can detect the target; this does not reveal invisible creatures automatically or read tracks through solid stone.

<details><summary>Preserved source wording — book line3844</summary>

Keen Senses: Gain enhanced perception in natural environments, making it harder for creatures to hide from you.

</details>

#### Combat Focus

**Level 1 · selection · ranger.base.combat-focus**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Choice on learning | Continuous |

Choose one: Precision adds 1 to first ranged attack each turn against quarry; Momentum gives+5 ft Speed after switching weapon mode; Wild Hunt gives advantage on Survival to follow injured creatures and+1 initiative. Choices do not stack; no general retraining.

<details><summary>Preserved source wording — book line3845</summary>

Combat Focus: Choose one combat style (Precision, Momentum, or Wild Hunt) that enhances your fighting abilities.

</details>

#### Quick Shot

**Level 1 · selection · ranger.base.quick-shot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 short-rest use | One enemy in bow range | Instant | 1/short rest |

Make one ranged weapon attack, dealing weapon die only without ability damage modifier. Does not trigger Extra Attack or another Quick Shot; may gain one Hit Chain point at 11 within the turn cap.

<details><summary>Preserved source wording — book line3848</summary>

Quick Shot: Fire a rapid arrow that deals less damage but can be used as part of another action.

</details>

#### Twin Strike

**Level 1 · selection · ranger.base.twin-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One or 2 enemies in melee reach; two light weapons wielded | Instant | Recharge 2 |

Make one attack with each weapon. Add ability modifier to first hit only. These are the full attacks for this Action; do not add ordinary Extra Attack. Hit Chain gains at 11 cap 2 per turn.

<details><summary>Preserved source wording — book line3849</summary>

Twin Strike: Make a swift attack with both melee weapons when dual wielding.

</details>

#### Nature's Whisper

**Level 1 · selection · ranger.base.nature-s-whisper**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | Natural terrain within 15 ft | 1 minute | Recharge 3 |

Gain advantage on one Perception/Survival check to find tracks, hidden natural creatures or signs of passage. It reveals evidence on success, not automatically creatures through total cover, incorporeal beings or thoughts.

<details><summary>Preserved source wording — book line3850</summary>

Nature's Whisper: Cast a minor nature spell that reveals hidden creatures or tracks within a small area.

</details>

#### Skirmisher's Step

**Level 1 · selection · ranger.base.skirmisher-s-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | Immediate movement | Recharge 2 |

Move up to half Speed without provoking opportunity attacks. Supplied movement does not increase remaining normal movement. Requires an unblocked route; no teleport or escape from restraints.

<details><summary>Preserved source wording — book line3851</summary>

Skirmisher's Step: Move half your speed without provoking opportunity attacks.

</details>

#### Elemental Attunement

**Level 1 · selection · ranger.base.elemental-attunement**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP | Self | Concentration, 1 minute | Recharge 3 |

Choose fire/cold/poison. Gain resistance to that damage and sense an exposed source of it within 15 ft. Does not infuse weapons, detect through total cover or identify exact poison recipes.

<details><summary>Preserved source wording — book line3852</summary>

Elemental Attunement: Temporarily attune yourself to an element (fire, cold, or poison), gaining minor resistance and the ability to detect that element.

</details>

## Arch cards

#### Ignore Difficult Terrain

**Level 3 · selection · ranger.arch.ignore-difficult-terrain**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Ignore movement cost increases from difficult terrain, including magical terrain. You still suffer its separate damage, restraints and hazards, and cannot cross impassable walls or surfaces without movement capability.

<details><summary>Preserved source wording — book line3858</summary>

Ignore Difficult Terrain: Move normally through any type of difficult terrain.

</details>

#### Enhanced Stealth and Perception

**Level 3 · selection · ranger.arch.enhanced-stealth-and-perception**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Gain+2 Stealth and Perception. It does not stack with Keen Senses on Perception; use+2 total from these class features. Advantage from another feature is separate.

<details><summary>Preserved source wording — book line3859</summary>

Enhanced Stealth and Perception: Gain +2 to Stealth and Perception checks.

</details>

#### Tactical Draw

**Level 3 · selection · ranger.arch.tactical-draw**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self after switching melee/ranged weapon mode | Until start next turn | Once/own turn |

Gain+1 AC after making an attack with the new mode. Drawing/stowing alone is insufficient. Further switches refresh neither extra AC nor actions.

<details><summary>Preserved source wording — book line3860</summary>

Tactical Draw: Gain +1 AC after switching from bow to blade or vice versa.

</details>

#### Vigilant Heart

**Level 7 · selection · ranger.arch.vigilant-heart**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While conscious | Continuous |

You cannot be surprised by a creature you can perceive. Gain advantage on saves against scrying; on success learn someone attempted it but not identity/location. No blanket immunity to divination.

<details><summary>Preserved source wording — book line3861</summary>

Vigilant Heart: Become immune to surprise and scrying attempts.

</details>

#### Dual Style

**Level 5 · selection · ranger.arch.dual-style**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Own turn | Once/turn |

Draw/stow a bow and up to 2 light melee weapons as one free exchange on your turn. This replaces normal object interaction for those weapons and cannot manipulate unrelated items or grant attacks.

<details><summary>Preserved source wording — book line3862</summary>

Dual Style: Gain the ability to swap weapons as a free action (level 5).

</details>

#### Elemental Imbue

**Level 6 · selection · ranger.arch.elemental-imbue**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Wielded weapons | 3 of your turns | Recharge 3 |

Use the engine's fire/cold/poison Imbue: once/turn add 1d4 and its bounded elemental rider to a weapon hit. Switching element pays again. It does not stack multiple imbues or multiply Do Ts.

<details><summary>Preserved source wording — book line3863</summary>

Elemental Imbue: Infuse your weapons with fire, cold, or poison to deal additional effects (level 6).

</details>

#### Pathfinder's Mark

**Level 3 · selection · ranger.arch.pathfinder-s-mark**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 RP | One fixed visible point within 30 ft | 24 hours | One location mark |

Know direction and rough distance to the point within 10 miles on same plane. A new mark replaces old. It does not create teleportation, observe occupants or reveal a path through barriers.

<details><summary>Preserved source wording — book line3866</summary>

Pathfinder's Mark: Place a magical mark on a location that you can sense the direction and distance to for 24 hours.

</details>

#### Natural Camouflage

**Level 3 · selection · ranger.arch.natural-camouflage**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self in natural cover | Until you move or attack | Recharge 2 |

Take Hide with advantage if foliage, rock or other natural cover can conceal you. Being stationary in open view does not qualify. Does not grant invisibility or hide your allies.

<details><summary>Preserved source wording — book line3867</summary>

Natural Camouflage: Blend into natural surroundings, gaining advantage on Stealth checks while stationary.

</details>

#### Terrain Analysis

**Level 3 · selection · ranger.arch.terrain-analysis**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | Visible terrain within 60 ft | Instant information | Recharge 2 |

Learn up to 2 observable tactical facts: difficult ground, unstable footing, tracks or usable cover. Director states facts supported by senses; hidden magical traps still need normal checks. Next ally following your identified safe route gains+5 ft movement once.

<details><summary>Preserved source wording — book line3868</summary>

Terrain Analysis: Quickly survey an area to gain tactical information about the environment.

</details>

#### Swift Traverse

**Level 5 · selection · ranger.arch.swift-traverse**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 RP | Self in natural terrain | This turn | Recharge 3 |

Take Dash, gaining movement equal to Speed; ignore opportunity attacks from your quarry during this movement only. No free attacks, flight, wall traversal or doubled daily travel rate.

<details><summary>Preserved source wording — book line3869</summary>

Swift Traverse: Move at double speed for a short time when in natural terrain.

</details>

#### Predator's Mark

**Level 9 · selection · ranger.arch.predator-s-mark**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Your quarry within 90 ft | 1 minute | Recharge 3 |

Upgrade current mark: first direct weapon hit per turn adds 1d6 rather than the engine's flat S; choose the higher, not both. Know quarry direction while within 90 ft unless blocked by total cover. Requires concentration; ordinary mark remains if this upgrade ends.

<details><summary>Preserved source wording — book line3870</summary>

Predator's Mark: Mark a tracked target for bonus damage and enhanced awareness of their movements (level 9).

</details>

## Hero cards

### Warder

#### Living Pulse

**Level 10 · selection · ranger.hero.warder.living-pulse**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 RP | Self in natural terrain | Start of your regular turn | Once/turn |

You may pay 1 RP to regain 2 HP. Does not trigger when Downed or incapacitated, cannot exceed maximum and never counts as another healing spell. Replaces unlimited passive regeneration with a finite cost.

<details><summary>Preserved source wording — book line3879</summary>

Living Pulse: Regenerate 2 HP per round while in natural terrain.

</details>

#### Beast Empathy

**Level 10 · selection · ranger.hero.warder.beast-empathy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Natural beasts within 30 ft that hear you | While communicating | Continuous |

Communicate simple emotions/directions. They are not automatically friendly or controlled, cannot answer beyond their experience, and may need normal Animal Handling. No language-based compulsion or extra companion slot.

<details><summary>Preserved source wording — book line3880</summary>

Beast Empathy: Communicate basic concepts with natural beasts.

</details>

#### Warden's Vigilance

**Level 10 · selection · ranger.hero.warder.warden-s-vigilance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Ritual | 1 RP; 10 minutes | Natural area within 300 ft | Instant information | 1/short rest |

Learn direction of one substantial recent fire, poisoning or unnatural blight in the area. Does not locate arbitrary enemies or identify culprits. A protected or planar-hidden effect may remain undetected.

<details><summary>Preserved source wording — book line3881</summary>

Warden's Vigilance: Detect threats to natural areas within a large radius.

</details>

#### Healing Touch

**Level 10 · selection · ranger.hero.warder.healing-touch**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One other ally healed by your paid spell/item | Instant | Once/turn |

Add M HP to actual healing. Do not multiply potion dice or duplicate consumed items; cannot apply to regeneration, companions' healing, copies or another Ranger's same bonus.

<details><summary>Preserved source wording — book line3882</summary>

Healing Touch: Your healing spells and items are 25% more effective on allies.

</details>

#### Rootcall Quake

**Level 10 · selection · ranger.hero.warder.rootcall-quake**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Up to 3 enemies in 10 ft-radius ground area within 60 ft | Concentration, 3 of your turns | Recharge 3 |

STR save or Speed 0. Each affected target repeats save at end of each turn and may use Action to attempt escape using STR(Athletics) against class DC. Flying creatures not touching ground are unaffected.

<details><summary>Preserved source wording — book line3885</summary>

Rootcall Quake: Create an area effect that roots enemies in place.

</details>

#### Healing Briar

**Level 10 · selection · ranger.hero.warder.healing-briar**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Fixed 10 ft-radius natural-ground zone within 30 ft; 3 allies/pulse | Concentration, 3 of your turns | Recharge 4 |

On start heal 1d8+M per chosen living ally; on next 2 turns Bonus Action+1 RP repeats pulse. Maximum 3 pulses; no passive additional entry healing and no Wound removal.

<details><summary>Preserved source wording — book line3886</summary>

Healing Briar: Establish a healing zone that restores health to allies within it.

</details>

#### Warden's Step

**Level 12 · selection · ranger.hero.warder.warden-s-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 3 RP | Empty space adjacent to injured ally within 30 ft | Instant; pressure until start next turn | Recharge 3 |

Teleport to visible legal space. Up to 2 adjacent enemies make WIS save; failure gives disadvantage on next attack against someone other than you. No forced targeting, movement or whole-Action loss.

<details><summary>Preserved source wording — book line3887</summary>

Warden's Step: Teleport to an injured ally and taunt nearby foes.

</details>

#### Nature's Blessing

**Level 14 · selection · ranger.hero.warder.nature-s-blessing**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One willing ally within 30 ft | Concentration, 3 of your turns | Recharge 3 |

Ally gains+10 ft Speed and S d6+M temporary HP on start. While effect lasts it has advantage on saves against forced movement. Temporary HP are not refreshed each turn.

<details><summary>Preserved source wording — book line3888</summary>

Nature's Blessing: Grant an ally temporary bonuses to speed and resilience.

</details>

#### Beast Companion

**Level 16 · selection · ranger.hero.warder.beast-companion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Ritual | 4 RP; 1 hour with a willing/tamed eligible beast | One beast touched | Bond persists; one companion | 1/long rest |

Bond eligible beast using standard companion stats plus Wisdom modifier HP; preserve one movement mode up to 40 ft and keen-sense advantage. Bonus Action command gives one attack, no imported boss powers. Injury persists; heal normally. Death requires a new bond after long rest, not free resummoning.

<details><summary>Preserved source wording — book line3889</summary>

Beast Companion: Tame one beast from the bestiary (CR ≤ your level, INT < 7, not corrupted) as a permanent companion that scales with your Wisdom and level.

</details>

### Stalker

#### Hunter's Reflex

**Level 10 · selection · ranger.hero.stalker.hunter-s-reflex**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self after ranged attack | Until start next turn | Once/turn |

Gain+1 AC against the next ranged attack targeting you. Benefit ends after that attack, hit or miss. Multiple shots do not create multiple dodge charges.

<details><summary>Preserved source wording — book line3895</summary>

Hunter's Reflex: Gain +10% Dodge chance after making a ranged attack.

</details>

#### Shadow Step

**Level 10 · selection · ranger.hero.stalker.shadow-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self at normal walking speed | While moving | Continuous |

Leave no mundane footprints and make no ordinary footstep sound. You still need cover and Stealth to hide; speech, equipment noise, scent, tremorsense and magical tracking remain possible.

<details><summary>Preserved source wording — book line3896</summary>

Shadow Step: Leave no tracks and make no sound when moving at normal speed.

</details>

#### Keen Hunter

**Level 10 · selection · ranger.hero.stalker.keen-hunter**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your quarry within normal sight | While marked | Continuous |

If quarry attempts to Hide while visible to you, you know its position until it gains total cover or leaves your sight. Does not negate invisibility, darkness or planar travel without an appropriate sense.

<details><summary>Preserved source wording — book line3897</summary>

Keen Hunter: Tracked targets cannot hide from you within your line of sight.

</details>

#### Efficient Killer

**Level 11 · selection · ranger.hero.stalker.efficient-killer**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Hit Chain after class 11 unlock | While known | Continuous |

Arrow threshold becomes 2 successful direct weapon hits instead of 3; gain cap remains 2/turn. The source of an Arrow's combo prerequisite still needs its stated history; Emberroot/Glacial may require 3 hits even though chain is primed at 2.

<details><summary>Preserved source wording — book line3898</summary>

Efficient Killer: Reduce the Hit Chain requirement for Druidic Arrow to 2 hits instead of 3.

</details>

#### Camouflage Step

**Level 10 · selection · ranger.hero.stalker.camouflage-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 2 RP | Self in natural cover or dim light | Until end next turn or attack/cast | Recharge 3 |

Become invisible; ends immediately after your first attack roll or spell cast, hit or miss. No automatic surprise. Taking damage does not itself end it, but ordinary senses can locate you.

<details><summary>Preserved source wording — book line3901</summary>

Camouflage Step: Become invisible until you make your first attack.

</details>

#### Silent Volley

**Level 10 · selection · ranger.hero.stalker.silent-volley**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Up to 3 distinct enemies in bow range | Instant | Recharge 3 |

Make 3 bow attacks, each weapon die without ability damage modifier. Ignore half cover, not armor or total cover. Quarry/riders once per their limits; chain gains at most 2. This is not three full Attack Actions.

<details><summary>Preserved source wording — book line3902</summary>

Silent Volley: Fire three arrows in rapid succession, ignoring armor bonuses.

</details>

#### Shattershot

**Level 12 · selection · ranger.hero.stalker.shattershot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One enemy in bow range | Instant; shield suppression until end next turn | Recharge 3 |

One bow attack; hit adds S d6 piercing. Target makes STR save or loses its shield's AC bonus until end next turn. One visible rank 1–3 magical defense can instead be suppressed after a WIS save failure; never permanently destroys gear or dispels everything.

<details><summary>Preserved source wording — book line3903</summary>

Shattershot: Fire a specialized arrow that breaks shields and removes magical buffs.

</details>

#### Ghost Strike

**Level 14 · selection · ranger.hero.stalker.ghost-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 2 RP | One enemy in melee reach | Instant | Recharge 3 |

One melee weapon attack with+2 to hit; on hit add S d6 force. Only added force ignores resistance, not immunity. Does not remove natural armor, all AC or legendary defenses.

<details><summary>Preserved source wording — book line3904</summary>

Ghost Strike: Make a melee attack that bypasses physical armor.

</details>

#### Vanishing Act

**Level 16 · selection · ranger.hero.stalker.vanishing-act**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 4 RP; 1 short-rest use | Self; visible destination within 30 ft | Until start next turn or attack/cast | 1/short rest |

Teleport to unoccupied visible space and become invisible until the stated end. Cannot pass a ward that blocks teleportation, escape a dimensional prison or retain invisibility after attacking.

<details><summary>Preserved source wording — book line3905</summary>

Vanishing Act: Disappear from sight and reposition to any point within 30 feet.

</details>

### Outrider

#### Predator's Grin

**Level 10 · selection · ranger.hero.outrider.predator-s-grin**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 short-rest use | Self after directly reducing quarry to 0 | Your next regular turn | 1/short rest |

Gain one extra full Action next turn within the shared cap. It cannot grant another Action or trigger another Predator's Grin. Allies, summons, helpless creatures and ongoing copied damage do not qualify.

<details><summary>Preserved source wording — book line3911</summary>

Predator's Grin: Killing a tracked target grants you an extra action once per rest.

</details>

#### Toxic Affinity

**Level 10 · selection · ranger.hero.outrider.toxic-affinity**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While known | Continuous |

Immune to Poisoned and nonmagical disease; gain poison resistance. This deliberately replaces blanket immunity to every poison/disease source. Existing magical diseases require their own treatment.

<details><summary>Preserved source wording — book line3912</summary>

Toxic Affinity: Gain immunity to poison and disease.

</details>

#### Corruption Touch

**Level 10 · selection · ranger.hero.outrider.corruption-touch**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Elemental Imbue | Up to 6 of your turns | Once/turn spread |

Imbue lasts 6 turns instead of 3. On a weapon critical, one other enemy within 5 ft takes 1d4 of imbue type. No additional condition, Hit Chain or recursive critical effects on that secondary damage.

<details><summary>Preserved source wording — book line3913</summary>

Corruption Touch: Your elemental imbues last twice as long and spread to adjacent targets on critical hits.

</details>

#### Blight Infusion

**Level 10 · selection · ranger.hero.outrider.blight-infusion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Primary target of your Arrow on blighted ground | Until end target's next turn | Once/Arrow |

On hit target makes CON save or the next HP healing it receives is reduced by M, minimum 0. This is temporary Blight, not permanent campaign Corruption; multiple applications do not stack.

<details><summary>Preserved source wording — book line3914</summary>

Blight Infusion: Your Druidic Arrows inflict Blight on hit if the terrain is corrupted.

</details>

#### Venom Rain

**Level 10 · selection · ranger.hero.outrider.venom-rain**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | Up to 3 enemies in 10 ft-radius area within 60 ft | Instant; Poisoned until end next turn | Recharge 3 |

CON save: S d8 poison, half on success; failure Poisoned until end next turn. No permanent Corruption gain, contagious disease or poison harvesting. This is a paid technique and does not build Hit Chain.

<details><summary>Preserved source wording — book line3917</summary>

Venom Rain: Create an area effect that deals poison damage and applies Corruption.

</details>

#### Rotting Tether

**Level 10 · selection · ranger.hero.outrider.rotting-tether**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One enemy standing on ground within 60 ft | Concentration, 3 of your turns | Recharge 3 |

CON save or tethered: first time it voluntarily moves at least 5 ft each turn, takes S d4 necrotic. Repeat save at turn end ends tether. Forced movement causes no damage; maximum 1 tick/turn, no whole-turn loss.

<details><summary>Preserved source wording — book line3918</summary>

Rotting Tether: Link an enemy to corrupted terrain, causing damage when they move.

</details>

#### Entropic March

**Level 12 · selection · ranger.hero.outrider.entropic-march**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 4 RP | Fixed 15 ft-radius ground area within 60 ft | Concentration, 3 of your turns | Recharge 4 |

Create temporary blighted difficult terrain. On start and first entry/start of turn, up to 3 enemies take S d4 necrotic, CON half, maximum once/creature/round. Ground returns unchanged afterward; no permanent ecological corruption or resource farming.

<details><summary>Preserved source wording — book line3919</summary>

Entropic March: Convert natural terrain into Blighted terrain in a large area.

</details>

#### Withering Shot

**Level 14 · selection · ranger.hero.outrider.withering-shot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 3 RP | One enemy in bow range | Instant; until end target's next turn | Recharge 3 |

Bow attack; hit adds S d6 necrotic and target makes CON save. Failure halves the next HP healing it receives before expiry, rounding down. No stacking with another reduction to create negative healing.

<details><summary>Preserved source wording — book line3920</summary>

Withering Shot: Fire an arrow that drastically reduces the target's healing received.

</details>

#### Plague Bearer

**Level 16 · selection · ranger.hero.outrider.plague-bearer**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 5 RP; 1 long-rest use | Self; direct weapon targets | Concentration, 3 of your turns | 1/long rest |

Your first weapon hit each turn adds 1d6 poison; target CON save or Poisoned until end next turn. You lose M real HP on activation, cannot fall below 1. The controlled effect is not a transmissible permanent disease and creates no free toxins.

<details><summary>Preserved source wording — book line3921</summary>

Plague Bearer: Infect yourself with a controlled disease that spreads to enemies you damage.

</details>

#### Master of the Hunt — new Hero capstone

**Level 20 · automatic · ranger.supplement.master-of-the-hunt-new-hero-capstone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 1 long-rest use | One legal chosen Hero Arrow | That Arrow | 1/long rest |

New playtest Hero capstone. Once per long rest when using your Hero Arrow, pay its normal Hit Chain/action requirements, then enhance only that activation: Warder grants 2 M temporary HP instead of M; Stalker adds S d6 piercing to one of its two hits; Outrider adds S d4 necrotic to one target on its single pulse. No extra Arrow, Hit Chain, action or copied proc.

Prerequisite: See class engine and progression.

Source status: **new playtest completion**, not recovered historical wording.

## Source appendix and open balance questions

The complete original Ranger book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/ranger.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Can switching weapons remain worthwhile without eclipsing focused styles?
- Does the level11 Arrow timing feel rewarding without free attacks?
- Are permanent companions useful while respecting a shared command budget?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
