# Soldier — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/soldier.json) · [Normalized card data](../../../data/public/class_playtests/soldier.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Constitution (for DR, resistances, control effects)
- Secondary Attribute: Dexterity (for ranged accuracy, overwatch utility)
- Hit Points: High (10 + Constitution modifier at 1st level, 1d10 per level thereafter)
- Armor Proficiency: All armor types, including heavy armor
- Weapon Proficiency: Repeating heavy crossbows, tower shields, and compatible sidearms
- Tool Proficiency: Carpenter's tools, siege engineer's kit

A martial class with d10 Hit Die, all armor and shields, repeating crossbows, sidearms and siege tools. Dexterity governs ranged attacks; Constitution governs class DC/M and defensive techniques. No RP, ordinary spellcasting, Refrain or Dissonance engine. Names such as Divine Lockdown describe disciplined suppression; they do not grant divine magic.

Overwatch is an automatic Base engine at 1. Bonus Action designate a visible 15 ft square within weapon range until start next regular turn. Once during that interval, spend your Reaction when a perceived enemy enters, moves inside, attacks an ally from, or reveals itself inside the zone. Make one legal ranged attack with ammunition and line of fire, normally 1d8+DEX piercing. On hit choose Snare (Speed-10 ft until end next turn), Bleed (1d4 at start next turn), or Push 5 ft (STR save negates push). Concealment still applies. Only one Overwatch zone; no extra Reaction. The optional Overwatch card upgrades this engine. At 17 you may move 5 ft without opportunity attacks after its shot, once/round.

At 5 automatically gain Palisade Deployment. Spend one carried barricade kit and an Action to erect a 2-by 1-tile wall in contiguous unoccupied ground within 5 ft. Height 5 ft, AC 12, HP 5+CON modifier minimum 1, immunity psychic/poison; blocks movement and line of sight across its full height but can be climbed using 10 ft movement. One kit/use per encounter, two at 13; a long rest with carpentry tools replenishes 2 kits (carried maximum 2, reusable parts have no resale value). Material is required; no conjuring. At most one intact wall, two at 13. Old wall must be dismantled in 1 minute before replacement beyond cap. Once per encounter an Action repairs a wall for M HP using spare parts; destruction does not refresh uses.

Palisade Tier II at 13 doubles wall HP and grants resistance to damage from area effects. Hold Position: while adjacent to your intact wall gain+1 AC and+1 saves. Brace Line: an ally immediately behind you relative to a ranged attacker, with your wall adjacent to both of you, has 2 flat DR against that attacker. These bonuses do not stack with another Soldier wall; strongest flat DR applies. Full cover prevents attacks rather than granting an additional AC bonus.

Base 1–2, Commander Arch 3–9, then Champion/Artillerist/Tyrant Hero 10–20. Palisade 5 is automatic; Intercepting Shot has minimum 6 and Fortify Zone 9. Other cards require selection. There is no source automatic Arch capstone. At 20 gain the new Final Command below, clearly a playtest addition. No spell or sustained technique may be used to obtain infinite ammunition, structures, actions or permanent healing.

**Protected source interface:** No general Weave casting; class power is entirely positional and martial.

## Advancement and resources

RP authority: No RP: protected class contract. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 0 | — | Choose 4 Base; at least 2 active |
| 2 | Base | 0 | — | Choose 2 Base |
| 3 | Arch | 0 | — | Choose 2 Arch; at least 1 active |
| 4 | Arch | 0 | — | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 0 | — | Choose 1 Arch; automatic: Palisade Deployment |
| 6 | Arch | 0 | — | Choose 1 Base/Arch |
| 7 | Arch | 0 | — | Choose 1 Arch |
| 8 | Arch | 0 | — | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 0 | — | Choose 1 Arch |
| 10 | Hero | 0 | — | Choose 2 Hero; at least 1 active |
| 11 | Hero | 0 | — | Choose 1 Base/Arch |
| 12 | Hero | 0 | — | Choose 1 Hero; ASI or feat |
| 13 | Hero | 0 | — | Choose 1 Base/Arch |
| 14 | Hero | 0 | — | Choose 1 Hero |
| 15 | Hero | 0 | — | Choose 1 Base/Arch |
| 16 | Hero | 0 | — | Choose 1 Hero; ASI or feat |
| 17 | Hero | 0 | — | Choose 1 Base/Arch |
| 18 | Hero | 0 | — | Choose 1 Hero |
| 19 | Hero | 0 | — | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 0 | — | No ordinary selection; automatic: Final Command |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Soldier 6, DEX 16, CON 16, PB 3, S 2, M 3. Carry 2 barricade kits and begin with one encounter deployment available.
2. Turn 1 Action deploy a 10-by 5 ft wall: kits 2→1, encounter uses 1→0, wall HP 8. Bonus Action designate Overwatch. Standing adjacent grants+1 AC/+1 saves.
3. Enemy moves inside zone; Reaction attack hits for 1d8+3. Choose Snare: Speed-10 ft through end of its next turn. You cannot also use Intercepting Shot before your Reaction refreshes.
4. Turn 2 use Covering Fire: one ranged attack with its printed rider. You cannot add an ordinary Attack Action. Renew Overwatch with Bonus Action; its next shot still needs your Reaction.
5. If the wall is destroyed, encounter deployment stays 0. An intact wall could receive its once/encounter repair for 3 HP. After combat a new encounter still requires a carried kit; long rest restores at most 2 kits.

## Base cards

#### Overwatch

**Level 1 · selection · soldier.base.overwatch**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Overwatch zone | While known | Once/round |

Increase zone to 20 ft square. After a qualifying enemy triggers it you may decline the shot and keep waiting until zone expires. Still only one Reaction shot and normal sight requirements.

<details><summary>Preserved source wording — book line4191</summary>

Overwatch: Set up a reaction shot against movement in your designated zone.

</details>

#### Shield Trained

**Level 1 · selection · soldier.base.shield-trained**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While stationary | Continuous |

Wield a repeating crossbow with a strapped shield; reloading still needs an available hand or the repeating mechanism. If you have moved 0 ft since start last turn gain 1 flat DR. Forced movement ends the benefit.

<details><summary>Preserved source wording — book line4192</summary>

Shield Trained: Wield a shield alongside your crossbow and gain +1 Damage Reduction when stationary.

</details>

#### Tactical Awareness

**Level 1 · selection · soldier.base.tactical-awareness**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | During combat | Continuous |

Gain+2 Perception and initiative. Does not reveal unseen creatures automatically or allow attacks without line of fire.

<details><summary>Preserved source wording — book line4193</summary>

Tactical Awareness: Gain advantage on perception checks related to battlefield threats.

</details>

#### Defensive Positioning

**Level 1 · selection · soldier.base.defensive-positioning**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self adjacent to solid terrain or your cover | While positioned | Continuous |

Gain+1 AC. Does not stack with Hold Position or another copy of this feature; full cover follows ordinary rules.

<details><summary>Preserved source wording — book line4194</summary>

Defensive Positioning: Gain +1 AC when adjacent to terrain or structures.

</details>

#### Steady Aim

**Level 1 · selection · soldier.base.steady-aim**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your ranged attacks | While known | Continuous |

Ignore the AC bonus from half cover. Three-quarter and full cover still apply; this is not permission to shoot through allies or walls.

<details><summary>Preserved source wording — book line4195</summary>

Steady Aim: Ignore partial cover when making ranged attacks.

</details>

#### Covering Fire

**Level 1 · selection · soldier.base.covering-fire**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | One ammunition | One enemy within weapon range | Until start next turn | Recharge 2 |

Make one ranged weapon attack. On hit normal damage and target has-2 on its next attack against an ally other than you. Further Covering Fire replaces rather than stacks this penalty.

<details><summary>Preserved source wording — book line4198</summary>

Covering Fire: Fire a volley that forces enemies in a line to take cover or suffer damage.

</details>

#### Quick Deploy

**Level 1 · selection · soldier.base.quick-deploy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 encounter use | One 5 ft square within 5 ft | 3 rounds or destroyed | 1/encounter |

Place low cover from carried field supplies: AC 12, HP 5, grants half cover and is difficult terrain. It is not a full palisade and does not grant its bonuses. One at a time; no transferable saleable material.

<details><summary>Preserved source wording — book line4199</summary>

Quick Deploy: Set up a temporary barricade that provides partial cover.

</details>

#### Warning Shot

**Level 1 · selection · soldier.base.warning-shot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | One ammunition | One visible enemy within 60 ft | Until end next target turn | Recharge 2 |

Make a ranged attack; on hit deal weapon die only and impose disadvantage on its next attack. Does not force it to attack or expend an action.

<details><summary>Preserved source wording — book line4200</summary>

Warning Shot: Fire a deterrent shot that imposes disadvantage on an enemy's next attack.

</details>

#### Tactical Reposition

**Level 1 · selection · soldier.base.tactical-reposition**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | Immediate movement | Recharge 2 |

Move up to half Speed without opportunity attacks. Requires an open route; no teleporting, escaping restraints or attacks.

<details><summary>Preserved source wording — book line4201</summary>

Tactical Reposition: Move half your speed without provoking opportunity attacks.

</details>

#### Rally Point

**Level 1 · selection · soldier.base.rally-point**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 short-rest use | Up to 3 allies within 15 ft who hear you | Until start next turn | 1/short rest |

Each gains M temporary HP and+1 on the next saving throw before duration ends. Temporary HP follows strongest-only rule and is lost at encounter end.

<details><summary>Preserved source wording — book line4202</summary>

Rally Point: Designate a location that grants allies who move there a small defensive bonus.

</details>

## Arch cards

#### Command Step

**Level 3 · selection · soldier.arch.command-step**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One willing ally adjacent | Immediate movement | Once/round on your turn |

After you take an Action, ally may move 5 ft without opportunity attacks. No extra action, attack, teleport or movement through blocked spaces.

<details><summary>Preserved source wording — book line4208</summary>

Command Step: Once per round, shift one adjacent ally 1 tile in any direction.

</details>

#### Formation Lock

**Level 3 · selection · soldier.arch.formation-lock**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self and adjacent allies | While conscious and adjacent | Continuous |

Enemies gain no flanking bonus from surrounding protected creatures. Other sources of advantage and cover remain; allies need not spend reactions.

<details><summary>Preserved source wording — book line4209</summary>

Formation Lock: Allies adjacent to you cannot be flanked.

</details>

#### Iron Orders

**Level 3 · selection · soldier.arch.iron-orders**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Up to 3 allies within 15 ft who hear you | While conscious | Continuous |

Gain+1 AC and+1 saves against Frightened. This AC bonus does not stack with other Soldier formation/aura AC bonuses; use highest.

<details><summary>Preserved source wording — book line4210</summary>

Iron Orders: All allies within 3 tiles gain +1 Save vs Fear and +1 AC.

</details>

#### Palisade Deployment

**Level 5 · automatic · soldier.arch.palisade-deployment**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | One kit; one encounter deployment | Adjacent 10-by 5 ft ground | Until destroyed/dismantled | 1/encounter; 2 at 13 |

Automatic engine, not a selected skill. Build the palisade with the exact statistics, kit and repair rules in the class engine. Source minimum 5 retained.

<details><summary>Preserved source wording — book line4211</summary>

Palisade Deployment: Deploy a 2x1 barrier that blocks movement and line of sight (level 5).

</details>

#### Intercepting Shot

**Level 6 · selection · soldier.arch.intercepting-shot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | One ammunition | Attacker within 25 ft that you perceive | One attack | Once/round |

When it hits an ally within 25 ft, attack it before damage. On your hit reduce triggering damage by S+M, minimum 0. Your shot deals weapon die only. Does not undo a hit or block an area effect against everyone.

<details><summary>Preserved source wording — book line4212</summary>

Intercepting Shot: Use your reaction to fire at an enemy about to hit an ally within 5 tiles (level 6).

</details>

#### Fortify Zone

**Level 9 · selection · soldier.arch.fortify-zone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest use | Visible 15 ft square within 30 ft | 3 rounds | 1/short rest |

Designate fortified firing lanes. Ranged attacks against up to 3 allies inside take-2 to hit while you remain conscious within 30 ft. Does not affect saves, melee attacks or attacks from inside zone.

<details><summary>Preserved source wording — book line4213</summary>

Fortify Zone: Enemies in a 3x3 area take –2 to ranged attacks against your allies (level 9).

</details>

#### Tactical Assessment

**Level 3 · selection · soldier.arch.tactical-assessment**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | One visible enemy within 60 ft | Until end next turn | Recharge 3 |

Learn its current armor category and whether it has cover. Choose one ally: their next attack against it gains+1 to hit. No hidden statistics, mind-reading or vulnerability invention.

<details><summary>Preserved source wording — book line4216</summary>

Tactical Assessment: Analyze the battlefield to gain information about enemy weaknesses.

</details>

#### Coordinated Maneuver

**Level 3 · selection · soldier.arch.coordinated-maneuver**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest use | One willing ally within 30 ft who hears you | Immediate | 1/short rest |

Ally spends Reaction to move up to half Speed and make one weapon attack. This is one granted attack, not a full Attack Action; no Extra Attack. For cap purposes this granted move plus one weapon attack counts as the ally’s one additional full Action for the round; it still permits only one weapon attack and never Extra Attack.

<details><summary>Preserved source wording — book line4217</summary>

Coordinated Maneuver: Direct an ally to move and take an action out of turn.

</details>

#### Suppression Fire

**Level 3 · selection · soldier.arch.suppression-fire**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Three ammunition | 15 ft square within weapon range | Until start next turn | Recharge 3 |

Up to 3 perceived enemies in zone make DEX save. Failure: S d6 piercing and Speed-10 ft through end next turn; success half damage, no slow. Cannot shoot through full cover. No attack rolls or on-hit procs.

<details><summary>Preserved source wording — book line4218</summary>

Suppression Fire: Create a zone that enemies must save against or take damage when entering.

</details>

#### Defensive Formation

**Level 3 · selection · soldier.arch.defensive-formation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 encounter use | Up to 3 willing allies within 15 ft | Until start next turn | 1/encounter |

Each may shift 5 ft without opportunity attacks and gains 1 flat DR while adjacent to another affected ally. Uses strongest DR, not an additive stack.

<details><summary>Preserved source wording — book line4219</summary>

Defensive Formation: Arrange allies in an optimal pattern, granting defensive bonuses.

</details>

#### Hold the Line

**Level 3 · selection · soldier.arch.hold-the-line**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 short-rest use | One enemy entering your melee reach | Until end its turn | 1/short rest |

Make one melee weapon attack. On hit normal damage and STR save or Speed 0. This is soft movement control; teleportation and forced movement remain possible.

<details><summary>Preserved source wording — book line4220</summary>

Hold the Line: Establish a defensive position that grants bonuses to allies behind you.

</details>

## Hero cards

### Champion

#### Protective Aura

**Level 10 · selection · soldier.hero.champion.protective-aura**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Allies within 10 ft | While conscious | Continuous |

Advantage on saves against Frightened or Charmed. Does not end existing effects automatically or grant immunity to all mental effects.

<details><summary>Preserved source wording — book line4229</summary>

Protective Aura: Nearby allies ignore fear and charm effects while you stand.

</details>

#### Selfless Guardian

**Level 10 · selection · soldier.hero.champion.selfless-guardian**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | One adjacent ally taking direct weapon damage | One hit | Once/round |

Redirect up to S+M of that damage to yourself. Redirected damage cannot be reduced, redirected again or trigger retaliation. The ally takes the rest after its own mitigation.

<details><summary>Preserved source wording — book line4230</summary>

Selfless Guardian: Take reduced damage when intercepting attacks meant for allies.

</details>

#### Inspiring Presence

**Level 10 · selection · soldier.hero.champion.inspiring-presence**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Allies within 15 ft who hear you | While conscious | Continuous |

Gain+2 on saves against fear and checks to rally a routed formation. No generic bonus to all saves or attacks; does not stack with Iron Orders fear bonus.

<details><summary>Preserved source wording — book line4231</summary>

Inspiring Presence: Allies within sight gain a bonus to morale saves.

</details>

#### Defensive Expertise

**Level 10 · selection · soldier.hero.champion.defensive-expertise**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self using a shield | While conscious | Continuous |

Gain 2 flat DR against weapon damage. Use strongest DR; does not stack with Shield Trained, wall protection or Wall of Aegis.

<details><summary>Preserved source wording — book line4232</summary>

Defensive Expertise: Gain additional damage reduction when using defensive abilities.

</details>

#### Guardian's Rush

**Level 10 · selection · soldier.hero.champion.guardian-s-rush**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 short-rest use | One ally within 15 ft hit by attack | Immediate | 1/short rest |

Move up to 15 ft along open ground to adjacent ally without opportunity attacks; reduce that hit's damage by 2 S+M. Cannot act while restrained or incapacitated. Does not transfer target or negate unrelated riders.

<details><summary>Preserved source wording — book line4235</summary>

Guardian's Rush: Move adjacent to an ally being attacked, potentially intercepting the blow.

</details>

#### Divine Lockdown

**Level 12 · selection · soldier.hero.champion.divine-lockdown**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 encounter use | Up to 3 enemies within 15 ft | Until end next target turn | 1/encounter |

STR save each; failure Speed 0 and cannot take Reactions. Success Speed-10 ft only. This is physical suppression; teleport remains possible. No damage or additional free attacks.

<details><summary>Preserved source wording — book line4236</summary>

Divine Lockdown: Prevent enemy movement in a small area (once per encounter).

</details>

#### Wall of Aegis

**Level 14 · selection · soldier.hero.champion.wall-of-aegis**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 short-rest use | Self and up to 3 adjacent allies | Until start of your second next turn | 1/short rest |

Gain 2 flat DR against all damage except psychic. Use strongest reduction once per damage packet; does not stack with other flat DR.

<details><summary>Preserved source wording — book line4237</summary>

Wall of Aegis: Grant all adjacent allies +2 Damage Reduction for 2 rounds.

</details>

#### Rallying Cry

**Level 10 · selection · soldier.hero.champion.rallying-cry**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 long-rest use | Up to 3 allies within 30 ft who hear you | Instant; temp HP to encounter end | 1/long rest |

End Frightened on each and grant S+M temporary HP. Cannot revive, heal real HP or repeatedly refresh from imitation/copies.

<details><summary>Preserved source wording — book line4238</summary>

Rallying Cry: Remove fear effects from nearby allies and grant temporary hit points.

</details>

#### Sacrificial Defense

**Level 16 · selection · soldier.hero.champion.sacrificial-defense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 1 long-rest use | One adjacent ally that would reach 0 HP from damage | One hit | 1/long rest |

Reduce damage by up to your current HP minus 1, taking that amount as unmitigable damage yourself. Ally takes remainder. Cannot make either creature's HP negative, erase massive-damage rules or transfer the cost again.

<details><summary>Preserved source wording — book line4239</summary>

Sacrificial Defense: Take damage in place of an ally, converting a portion to non-lethal damage.

</details>

### Artillerist

#### Enhanced Overwatch

**Level 10 · selection · soldier.hero.artillerist.enhanced-overwatch**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your Overwatch zone | While known | Continuous |

A hidden enemy that attacks or moves inside must roll Stealth against your passive Perception; failure reveals its space until turn end. Invisibility still imposes its normal attack penalty. Total cover blocks detection and firing.

<details><summary>Preserved source wording — book line4245</summary>

Enhanced Overwatch: Your Overwatch can reveal and fire on stealthed or invisible enemies.

</details>

#### Tactical Reload

**Level 10 · selection · soldier.hero.artillerist.tactical-reload**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One wielded crossbow | Own turn | Once/turn |

Reload its ordinary magazine without an action, consuming carried ammunition. No infinite ammunition or additional shots; incompatible with ammunition you cannot physically load.

<details><summary>Preserved source wording — book line4246</summary>

Tactical Reload: Reload your crossbow as a free action once per round.

</details>

#### Palisade Synergy

**Level 10 · selection · soldier.hero.artillerist.palisade-synergy**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your ranged weapon attack while adjacent to palisade | One hit | Once/own turn |

Add S damage. Does not apply to every shot, area save or turret hit, and requires an intact wall you deployed.

<details><summary>Preserved source wording — book line4247</summary>

Palisade Synergy: Your attacks deal additional damage to enemies adjacent to your palisades.

</details>

#### Precision Engineering

**Level 10 · selection · soldier.hero.artillerist.precision-engineering**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your constructed barriers and turrets | While present | Continuous |

Increase maximum and initial HP by M. Does not heal existing damaged structures when learned or moved; repairing remains finite.

<details><summary>Preserved source wording — book line4248</summary>

Precision Engineering: Your deployed structures have increased durability and effectiveness.

</details>

#### Net Bolt

**Level 10 · selection · soldier.hero.artillerist.net-bolt**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | One net cartridge; 1 encounter use | One enemy within 30 ft | Until escaped; at most 3 rounds | 1/encounter |

Ranged weapon attack; on hit S d4 bludgeoning and Restrained. Target or adjacent ally may use Action STR/Athletics against your DC to end, or destroy net AC 10 HP 5. Huge or larger targets instead lose 10 ft Speed. No automatic unsaveable imprisonment.

<details><summary>Preserved source wording — book line4251</summary>

Net Bolt: Fire a specialized bolt that snares the target on hit (no save).

</details>

#### Shatterburst

**Level 10 · selection · soldier.hero.artillerist.shatterburst**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Three ammunition | 15 ft cone | Until end next target turn | Recharge 3 |

Up to 3 enemies DEX save, S d6 piercing on failure, half success. Failure also-1 attack rolls for duration. This save technique has no critical hits or weapon-hit riders.

<details><summary>Preserved source wording — book line4252</summary>

Shatterburst: Fire a cone volley that imposes a -1 attack penalty on enemies for 1 round.

</details>

#### Repel Shot

**Level 12 · selection · soldier.hero.artillerist.repel-shot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | One ammunition; one charge | Enemy within 30 ft moving toward you | Immediate | 2/short rest |

Ranged attack; on hit weapon die damage and STR save or pushed 10 ft away. No pushing through walls or into occupied squares; it can continue remaining movement afterward.

<details><summary>Preserved source wording — book line4253</summary>

Repel Shot: Use your reaction to knock back a melee attacker (2 charges).

</details>

#### Turret Deployment

**Level 14 · selection · soldier.hero.artillerist.turret-deployment**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest use | Up to 2 empty squares within 10 ft | 3 rounds | 1/short rest |

Deploy 2 turrets, each AC 12+PB and HP 2 L, immobile, range 60 ft. On your Bonus Action command ONE turret to attack using PB+DEX for 1d6+M piercing. Both share that single command/attack budget with other companions; no autonomous shots. Reclaimed after use, no resale.

<details><summary>Preserved source wording — book line4254</summary>

Turret Deployment: Deploy up to 2 automated turrets that last 3 rounds, firing for 1d6+WIS damage and applying Snare or Disrupt effects.

</details>

#### Bubble of Discipline

**Level 16 · selection · soldier.hero.artillerist.bubble-of-discipline**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 long-rest use | 15 ft square centered within 15 ft | Until start of your second next turn | 1/long rest |

Deploy dense layered cover. Up to 3 allies inside gain+2 AC against spell attacks and advantage on DEX saves against spells from outside. Once total, Reaction reduce spell damage to one protected ally by 2 S+M. Does not negate a spell, block internal casting or protect each ally independently.

<details><summary>Preserved source wording — book line4255</summary>

Bubble of Discipline: Create a 3x3 area effect that blocks 1 spell per ally for 2 rounds (once per rest).

</details>

### Tyrant

#### Intimidating Presence

**Level 10 · selection · soldier.hero.tyrant.intimidating-presence**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Enemies within 10 ft that perceive you | While conscious | Continuous |

They take-1 on saves against your Frightened effects. Never alters immunity or stacks multiple Tyrant penalties.

<details><summary>Preserved source wording — book line4261</summary>

Intimidating Presence: Enemies that can see you have disadvantage on morale checks.

</details>

#### Cruel Efficiency

**Level 10 · selection · soldier.hero.tyrant.cruel-efficiency**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One enemy you hit with a weapon on successive regular turns | One hit | Once/own turn |

Second and later consecutive-turn hits against same enemy add S damage. Missing all attacks or changing target ends chain. Bonus never grows beyond S and excludes Overwatch/turrets/copies.

<details><summary>Preserved source wording — book line4262</summary>

Cruel Efficiency: Gain a stacking damage bonus when hitting the same target consecutively.

</details>

#### Marked for Death

**Level 10 · selection · soldier.hero.tyrant.marked-for-death**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | One visible enemy within 60 ft | Until start next turn | Recharge 2 |

Mark foe. It takes-1 saves against your class effects and deals 1 less damage on its first hit against an ally other than you. One mark; penalty does not stack with Intimidating Presence.

<details><summary>Preserved source wording — book line4263</summary>

Marked for Death: Enemies you designate take –1 to saves and deal –1 damage vs allies other than you.

</details>

#### Ruthless Tactician

**Level 10 · selection · soldier.hero.tyrant.ruthless-tactician**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Your weapon attacks | Own turn | Once/turn |

Gain advantage on one attack against a flanked enemy or enemy in difficult terrain. Terrain must actually impede it; creating harmless decoration does not qualify.

<details><summary>Preserved source wording — book line4264</summary>

Ruthless Tactician: Gain advantage on attacks against enemies that are flanked or hindered by terrain.

</details>

#### Crushing Decree

**Level 10 · selection · soldier.hero.tyrant.crushing-decree**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 encounter use | Up to 3 enemies within 30 ft that hear you | Until end next target turn | 1/encounter |

WIS save; failure has disadvantage on attacks against allies other than you while it can perceive you. It may move, cast nonattack spells or decline attacks; no compelled suicide or removed Action.

<details><summary>Preserved source wording — book line4267</summary>

Crushing Decree: Taunt enemies in range, forcing them to target you.

</details>

#### Impale Line

**Level 10 · selection · soldier.hero.tyrant.impale-line**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Two ammunition | 20 ft line, up to 2 enemies | Until end next target turn | Recharge 3 |

Make one ranged attack against each, normal weapon damage. If both hit, both lose Reactions for duration. If only one target exists, no double attack against it and no reaction rider.

<details><summary>Preserved source wording — book line4268</summary>

Impale Line: Fire a shot that travels in a 4-tile line; if it hits 2+ targets, all enemies lose their reactions.

</details>

#### Execution Zone

**Level 14 · selection · soldier.hero.tyrant.execution-zone**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 1 short-rest use | 15 ft square within 60 ft | 3 rounds | 1/short rest |

Designate zone. First time each round one enemy tries to leave, Reaction weapon attack; on hit normal damage and STR save or movement ends at boundary for current turn. Teleport/forced movement works. One shot across all targets, no impassable magical wall.

<details><summary>Preserved source wording — book line4269</summary>

Execution Zone: Create an area where enemies take –1 to morale and cannot escape.

</details>

#### Demoralizing Shot

**Level 12 · selection · soldier.hero.tyrant.demoralizing-shot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | One ammunition; 1 encounter use | Visible enemy within range; up to 2 allies of it within 10 ft | Until end next target turn | 1/encounter |

Weapon attack normal damage. On hit secondary enemies WIS save or disadvantage on next attack. Director need not designate a privileged leader; source leadership fiction represented by visible example.

<details><summary>Preserved source wording — book line4270</summary>

Demoralizing Shot: Hit an enemy leader to impose disadvantage on all nearby enemy attacks.

</details>

#### Brutal Example

**Level 16 · selection · soldier.hero.tyrant.brutal-example**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | One ammunition; 1 short-rest use | One enemy below half HP in weapon range | Until end next target turn | 1/short rest |

Weapon attack; on hit add 2 S d6 damage. Up to 2 enemies within 10 ft of victim WIS save or Frightened of you for duration. No automatic death threshold or fear through immunity.

<details><summary>Preserved source wording — book line4271</summary>

Brutal Example: Deal massive damage to a weakened target, causing nearby enemies to become frightened.

</details>

#### Final Command

**Level 20 · automatic · soldier.supplement.final-command**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 1 long-rest use | Self and up to 3 willing allies within 30 ft who hear you | Until start next turn | 1/long rest |

New Hero capstone. Allies may each move 10 ft without opportunity attacks and gain S+M temporary HP. You refresh one expended short-rest Soldier card, excluding Final Command and long-rest features. A refreshed card still costs its activation and ammunition; no extra turn or recursive resets.

Prerequisite: See class engine and progression.

Source status: **new playtest completion**, not recovered historical wording.

## Source appendix and open balance questions

The complete original Soldier book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/soldier.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Does Overwatch meaningfully influence enemy movement without deciding every turn?
- Are finite barricade kits practical to track?
- Do support actions compete fairly with attacking?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
