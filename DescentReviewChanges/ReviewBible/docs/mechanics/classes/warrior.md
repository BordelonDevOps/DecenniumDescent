# Warrior — class playtest v0.1

**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.

[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)

[Preserved book and registry evidence](../../../data/playtest/class_sources/warrior.json) · [Normalized card data](../../../data/public/class_playtests/warrior.json)

## Class engine and setup

**Book setup (provisional engine resolves any explicit conflicts below):**

- Main Attribute: Strength or Dexterity (player builds for power or agility)
- Secondary Attributes: Constitution
- Hit Points: High (12 + Constitution modifier at 1st level, 1d12 per level thereafter)
- Armor Proficiency: Medium and heavy armor
- Weapon Proficiency: All martial weapons; bonuses when wielding mutation-tagged gear
- Tool Proficiency: None

PROVISIONAL PLAYTEST CONTRACT. At Warrior level 1 choose Strength or Dexterity as your Warrior ability; this choice is permanent in this draft. S = 1/2/3/4 at Warrior levels 1/5/11/17. M = max(1, chosen Warrior ability modifier). Warrior technique attack = d20 + normal character proficiency bonus + chosen modifier. Warrior technique save DC = 8 + normal character proficiency bonus + chosen modifier. Source basis: approved Player Rulebook extract and preserved class registry.

The Warrior remains three distinct stages: Base Warrior at levels 1-2, Arch Juggernaut at levels 3-9, then one Hero path at levels 10-20: Wardborn, Ironskin or Dreadspawn. Mutation trees and serums supplement those stages rather than replacing them or functioning as parallel classes.

MUTATION SLOTS. At Warrior 1 you have one mutation slot; slot II unlocks at Warrior 5, slot III at Warrior 13 and slot IV at Warrior 20. During a completed short or long rest, equip one eligible mutation in each slot. Equipped mutations are dormant until activated unless their text explicitly says otherwise. You cannot equip the same named mutation twice.

ACTIVE MUTATIONS. Before Juggernaut Mutation Efficiency, only one equipped mutation can be active at a time. Mutation Efficiency raises the ordinary simultaneous-active limit to two. Transcendent, Apex Form and other explicit features can temporarily exceed that limit. Activating a mutation beyond the current limit ends one active mutation of your choice unless an explicit exception permits otherwise.

SERUM RESERVE. After a long rest prepare two serum doses, choosing one of the six serum profiles for each dose. At Warrior 11 the reserve becomes three prepared doses; at Warrior 20 it becomes four. Used doses do not naturally refill on a short rest. A long rest refills the reserve. Serum Recycling and explicit class features can preserve or restore doses, but no effect can increase the reserve above its current capacity.

SERUM INJECTION. Unless another feature says otherwise, injecting a prepared serum is a Bonus Action, consumes one prepared dose, activates one equipped mutation for 3 rounds and applies that dose's serum-profile benefits and side effect for the same 3 rounds. Reinjecting the same active mutation refreshes its duration rather than stacking it. Serum-profile numeric bonuses from two doses of the same profile never stack.

STRAIN. Begin after a long rest at 0 Strain; maximum Strain is 3. A normal serum injection or Mutagen Injection adds 1 Strain, Mutation Surge adds 1, and Serum Cocktail or Mutation Overload adds 2 unless modified. At Strain 2 your Speed is reduced by 5 feet. At Strain 3 you also take -1 AC and -1 on saving throws and cannot voluntarily activate another serum, Cocktail, Overclock or Surge until Strain is reduced. A completed short rest reduces Strain by 1; a long rest resets it to 0. Strain cannot exceed 3.

Mutation Adaptation and Serum Tolerance modify Strain and serum-profile side effects only as their cards state. A negative serum-profile side effect and Strain penalty are separate; preventing one does not automatically prevent the other.

BRUTALITY PROGRESS. Begin each real encounter with Brutality Progress 0 and BT 0. Add actual damage you personally deal to meaningful hostile creatures to Brutality Progress, but a single damage event contributes no more than one-quarter of your maximum HP. Crossing cumulative thresholds equal to 25%, 50% and 75% of your maximum HP grants 1 BT each, subject to the BT cap. Crossing 100% triggers Transcendent as described below but does not create a fourth stored BT unless Stack Overflow or another feature raises the cap.

TAKING DAMAGE AND BT. Once per round when one source deals you actual damage after mitigation equal to or greater than PB + M, gain 1 BT. This direct gain does not increase Brutality Progress. Normal threshold and damage-taken generation together can grant at most 2 BT per round. Explicit card gains such as Overpressure Response or Backlash Engine ignore that generation ceiling but never exceed the current BT cap.

BT CAP AND RESET. Default BT cap is 3. Stack Overflow raises it to 4. BT is not automatically spent; only features explicitly saying spend reduce it. Encounter end resets BT and Brutality Progress to 0. BT cannot be generated from friendly attacks, summoned sacrificial creatures, unattended objects, staged sparring or enemies that do not meaningfully threaten the party.

BRUTALITY STATES. At BT 1 you are Awakened; at BT 2 Primed; at BT 3 Unleashed. At Warrior 12+, reaching BT 4 or crossing 100% Brutality Progress may trigger the same once-per-encounter Transcendent pulse, even if your stored cap remains 3; it is never an indefinitely active state. State benefits are defined as operational extra Cards and vanish immediately if spending BT drops you below their thresholds.

HARD CONTROL GUARD. A creature can suffer at most one Warrior-caused effect that fully denies its normal turn, such as Stunned, Paralyzed or an equivalent full-turn denial, from your Warrior features per encounter. After the first succeeds, later Warrior effects from you that would fully deny that creature's turn instead remove its Reaction and reduce its Speed to 0 until the end of its next turn after the required save fails.

ADDITIONAL ACTION GUARD. All sources share a maximum of one additional full Action per creature per round. Additional Actions cannot generate another Action, Bonus Action or Reaction. Free attacks granted by Warrior features are explicitly bounded and never recursively grant additional free attacks.

RECHARGE GUARD. A named ability may receive at most one positive-counter reset or shortening per round. Only an ability with a positive recharge counter can be reset. Recharge never restores a spent short-rest or long-rest use unless the feature explicitly says it restores that use.

HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT.

IMMUNITY AND RESISTANCE. Warrior resistance does not stack with resistance to the same damage type; apply one resistance. Immunity supersedes resistance but multiple immunities provide no additional benefit. If a feature grants several immunities temporarily, each is still only one immunity to that specific type or condition.

MUTATION TIERS. Basic mutations require Warrior 1. Advanced mutations require Warrior 6. Apex mutations require Warrior 15. You may equip only mutations whose actual Warrior class-level gate and other prerequisites you meet. NEW explicit scope reconciliation (FEAT327-ACQ-02): across your single set of unlocked mutation slots, you may equip at most two Advanced mutations from each actual mutation tree and at most one Apex mutation in total across all trees. Basic mutations have no additional tier-count ceiling beyond the remaining unlocked slots. Count every equipped mutation, including a dormant one, toward its relevant equipment ceilings; use its actual source-defined tree and tier. These are equipped-loadout ceilings, not per-tree slot grants, limits on the number of feat identities acquired, or separate active-only tier ceilings. The completed-rest equipping procedure and prohibition on duplicate named mutations remain unchanged. Mutation Efficiency changes only the ordinary global simultaneous-active limit. Transcendent and Apex Form activate only the existing legally equipped loadout and do not waive equipment ceilings, level/prerequisite gates or duplicate restrictions. Apex Form's permanent slot IV is the single Warrior-20 slot unlock, not an additional slot each time the form activates. After a temporary activation exception ends, apply its exact ending procedure and the then-applicable active-mutation limit without refreshing durations or granting an unequipped mutation.

MUTATION FEATS. Mutation feats are not free mutation selections. They become eligible choices at an ASI/feat opportunity or other campaign feat grant once their listed level and mutation prerequisite are met. They do not consume mutation slots unless their own text says otherwise.

HERO MUTATION TREES. Bulwark Mutation Tree, Gore Mutation Tree and Aberrant Mutation Tree are Hero cards that unlock their associated Hero-specific mutation extra Cards. Those mutations still occupy normal mutation slots and obey active-mutation, serum and Strain rules.

PROPOSED ACQUISITION. Warrior 1 automatically gains Mutation Slot I and the BT tracker, then chooses 4 Base cards with at least 2 Active. Warrior 2 automatically gains Mutagen Injection, then chooses 2 additional Base cards. Warrior 3 enters Juggernaut and chooses 2 Arch cards with at least 1 Active. Warrior levels 4-9 each grant one eligible unselected Base or Arch choice. Source progression automatic features remain separate and never consume these choices.

At Warrior 10 choose Wardborn, Ironskin or Dreadspawn and choose 2 Hero cards from that path. Levels 11, 13, 15, 17 and 19 each grant one eligible unselected Base or Arch choice. Levels 12, 14, 16 and 18 each grant one Hero-path choice. The chosen Hero Final Form is automatic at Warrior 20 and cannot be selected early. ASI/feat grants remain separate.

SOURCE PROGRESSION RECONCILIATION. Book progression grants Mutation Slot II at 5, Bone Hardened at 6, Serum Overclock at 9, Mutation Slot III at 13, Brutal Adaptation at 15, Reflexive Mutation at 17 and Apex Form at 20 automatically. Registry-only Fighting Style, Second Wind, Action Surge, Extra Attack and draft level features are preserved in excluded Registry Alternatives and original source evidence. They are not acquired or stacked onto this playtest schedule.

All class gates use Warrior class level, not total character level. Proficiency bonus follows the game's ordinary total-character-level rule. No other class level unlocks Warrior mutation tiers, serum capacity, Juggernaut, Hero paths, Apex mutations or Final Forms.

Finite recovery completion: Mutation Recovery Reserve=3 L+M HP after a long rest. Bloodthick Node, Rapid Coagulation, Regenerative Mutation, Hemophage Core and their healing enhancements draw from this shared reserve, 1 point per actual HP healed. No short-rest refill; no gauge, critical hit, free activation or form change replenishes it. Other explicitly limited-use/dose healing retains its own printed limit. This new test reserve prevents indefinite regenerative healing from free mutation activations.

**Protected source interface:** No general Weave casting; mutations and serums are the Warrior's power engine.

## Advancement and resources

RP authority: No RP: protected class contract. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.

| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
|---:|---|---:|---:|---|
| 1 | Base | 0 | — | Choose 4 Base; at least 2 active; automatic: Mutation Slot I, Brutality Threshold Tracker |
| 2 | Base | 0 | — | Choose 2 Base; automatic: Mutagen Injection |
| 3 | Arch | 0 | — | Choose 2 Arch; at least 1 active |
| 4 | Arch | 0 | — | Choose 1 Base/Arch; ASI or feat |
| 5 | Arch | 0 | — | Choose 1 Base/Arch; automatic: Mutation Slot II |
| 6 | Arch | 0 | — | Choose 1 Base/Arch; automatic: Bone Hardened |
| 7 | Arch | 0 | — | Choose 1 Base/Arch |
| 8 | Arch | 0 | — | Choose 1 Base/Arch; ASI or feat |
| 9 | Arch | 0 | — | Choose 1 Arch; automatic: Serum Overclock |
| 10 | Hero | 0 | — | Choose 2 Hero; at least 1 active |
| 11 | Hero | 0 | — | Choose 1 Base/Arch |
| 12 | Hero | 0 | — | Choose 1 Hero; ASI or feat |
| 13 | Hero | 0 | — | Choose 1 Base/Arch; automatic: Mutation Slot III |
| 14 | Hero | 0 | — | Choose 1 Hero |
| 15 | Hero | 0 | — | Choose 1 Base/Arch; automatic: Brutal Adaptation |
| 16 | Hero | 0 | — | Choose 1 Hero; ASI or feat |
| 17 | Hero | 0 | — | Choose 1 Base/Arch; automatic: Reflexive Mutation |
| 18 | Hero | 0 | — | Choose 1 Hero |
| 19 | Hero | 0 | — | Choose 1 Base/Arch; ASI or feat |
| 20 | Hero | 0 | — | No ordinary selection; automatic: Aegis Incarnate (Wardborn), Adaptive Perfection (Ironskin), Abomination Ascendant (Dreadspawn), Apex Form |

Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.

See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.

## Worked encounter

1. Warrior 6 example: chosen ability Strength 18 gives M=4; assume PB=3, S=2, maximum HP 60, two mutation slots and Mutation Efficiency. The Warrior equips Ironhide Graft and Shock Muscle Weave, prepares Overdrive and Stonecore, begins a real encounter at BT 0, Brutality Progress 0 and Strain 0.
2. Turn 1: Bonus Action Serum Injection consumes the Overdrive dose, activates Ironhide Graft for 3 rounds and adds Strain 0→1. Overdrive grants +2 Strength and +10 feet Speed; its side effect gives -1 AC. Ironhide grants its own active mutation defenses. The Warrior then deals 18 actual damage; Brutality Progress becomes 18, crossing the 15-point 25% threshold and granting BT 0→1.
3. Enemy round: one attack deals 11 actual damage after mitigation. PB+M is 7, so the damage-taken rule grants BT 1→2, subject to the round generation cap. At BT 2 the Warrior is Primed. The damage itself does not add to Brutality Progress.
4. Turn 2: Serum Injection consumes Stonecore, activates Shock Muscle Weave alongside Ironhide because Mutation Efficiency permits two active mutations, and adds Strain 1→2. Stonecore grants +2 AC and knockback immunity but -10 feet Speed. Strain 2 separately applies -5 feet Speed. The Warrior deals 20 damage, Brutality Progress 18→38, crossing the 30-point 50% threshold; BT is already 2 so it becomes 3.
5. Turn 3: with BT 3 the Warrior is Unleashed and uses Brutality Unleashed, spending all 3 BT. BT 3→0. Enemies in the burst make the printed Strength save and take the area damage. Spending BT immediately ends Awakened, Primed and Unleashed state benefits, but active mutations and serum durations continue independently.
6. Turn 4: the Warrior uses Mutation Surge on Ironhide, adding 1 Strain. Strain 2→3, so the Strain 3 AC/save penalty applies after the activation. Until Strain falls below 3, another voluntary Serum Injection, Cocktail, Overclock or Surge is illegal. A later completed short rest reduces Strain 3→2 but does not refill either consumed serum dose.

## Base cards

#### Mutation Adaptation

**Level 1 · selection · warrior.base.mutation-adaptation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Mutation Adaptation. Ignore the Strain-2 Speed penalty. The first time in each encounter that activating a mutation or serum would add Strain, reduce that Strain gain by 1, minimum 0. This reduction cannot reduce Serum Cocktail or Mutation Overload below 1 Strain and cannot reduce existing Strain.

<details><summary>Preserved source wording — book line4801</summary>

Mutation Adaptation: Your body has been conditioned to accept mutations with reduced side effects.

</details>

#### Serum Tolerance

**Level 1 · selection · warrior.base.serum-tolerance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Serum Tolerance. Negative side effects printed on serum profiles do not affect you. Strain generation and Strain penalties still apply normally. This does not suppress drawbacks printed on mutation cards, Hero transformations or Mutation Overload.

<details><summary>Preserved source wording — book line4802</summary>

Serum Tolerance: You can consume serums without the normal toxicity effects that would affect others.

</details>

#### Combat Instinct

**Level 1 · selection · warrior.base.combat-instinct**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Combat Instinct. Gain +1 on initiative rolls. You cannot be Surprised while conscious unless the opposing creature's Stealth check exceeds your passive Perception by 5 or more. This does not grant extra Actions or movement before combat.

<details><summary>Preserved source wording — book line4803</summary>

Combat Instinct: +5% initiative and +10% resistance to being surprised.

</details>

#### Physical Conditioning

**Level 1 · selection · warrior.base.physical-conditioning**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Physical Conditioning. Increase carrying, pushing, dragging and lifting capacity by 25%. You have advantage on Constitution checks and saving throws made specifically against forced marching, sustained physical exertion, suffocation from exertion or environmental fatigue.

<details><summary>Preserved source wording — book line4804</summary>

Physical Conditioning: +10% carrying capacity and advantage on physical endurance checks.

</details>

#### Brutality Sense

**Level 1 · selection · warrior.base.brutality-sense**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Hostile creatures you can perceive within 60 feet | While condition remains true | Always |

Brutality Sense. You know when a visible hostile creature is at or below one-quarter of its maximum HP; it is Vulnerable for your Warrior features that specifically reference a marked vulnerable target. This does not reveal its exact HP or hidden resistances.

<details><summary>Preserved source wording — book line4805</summary>

Brutality Sense: You can sense when an opponent is below 25% health, marking them as vulnerable.

</details>

#### Serum Injection

**Level 1 · selection · warrior.base.serum-injection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | Consume 1 prepared serum dose; +1 Strain | Self | 3 rounds | At will while legal doses remain |

Serum Injection. Choose one equipped mutation and one prepared serum dose. Consume the dose, activate that mutation for 3 rounds and apply the serum profile for 3 rounds. Observe active-mutation limits, Strain legality and nonstacking same-profile bonuses.

<details><summary>Preserved source wording — book line4808</summary>

Serum Injection: Activate a prepared mutation serum as a bonus action, triggering its effects for 3 rounds.

</details>

#### Brutal Strike

**Level 1 · selection · warrior.base.brutal-strike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | One creature within your weapon reach | Instantaneous; Stagger until end of target's next turn | Recharge 1 round |

Brutal Strike. Make one melee weapon attack using its normal ability. On hit add S d6 damage of the weapon's type. The target makes a Constitution save; on failure it is Staggered, taking -1 on attack rolls and -5 feet Speed until the end of its next turn. This is not a full-turn denial.

<details><summary>Preserved source wording — book line4809</summary>

Brutal Strike: A powerful attack that deals additional damage based on your Strength and has a chance to stagger the target.

</details>

#### Mutation Surge

**Level 2 · selection · warrior.base.mutation-surge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +1 Strain | One active mutation | Until start of your next regular turn | Recharge 2 rounds |

Mutation Surge. Enhance one active mutation. If it grants AC, DR, attack, save or flat damage, increase one such bonus by 1; if it grants movement or reach, increase it by 5 feet; if it deals mutation damage, add 1d4 to one damage event. A mutation with none of those numeric effects instead grants S temporary HP. The enhancement never changes immunity, target count or duration.

<details><summary>Preserved source wording — book line4810</summary>

Mutation Surge: Temporarily enhance an active mutation, increasing its effects for 1 round but adding strain to your body.

</details>

#### Intimidating Presence

**Level 2 · selection · warrior.base.intimidating-presence**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | Up to 3 enemies of your choice within 15 feet that can see or hear you | Maximum 2 rounds | Recharge 3 rounds |

Intimidating Presence. Each target makes a Wisdom save. On failure it is Frightened of you until the end of its next turn, then repeats the save. A second failure extends the fear one final round. A creature that succeeds becomes immune to this use. This never forces surrender; NPC surrender remains a Director decision.

<details><summary>Preserved source wording — book line4811</summary>

Intimidating Presence: Use your mutated appearance to frighten enemies, potentially causing them to flee or surrender.

</details>

#### Survival Instinct

**Level 1 · selection · warrior.base.survival-instinct**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | Until start of your next regular turn | Recharge 3 rounds |

Survival Instinct. Gain +2 on Perception checks, +2 on Dexterity saving throws and one additional Reaction usable only for Dodge-like defensive reactions, opportunity-free movement granted by a feature, or Deflect-style mitigation. It cannot make an attack or trigger another additional Reaction.

<details><summary>Preserved source wording — book line4812</summary>

Survival Instinct: Enter a heightened state of awareness, gaining bonuses to perception and reaction time for a short duration.

</details>

#### Mutation Slot I

**Level 1 · automatic · warrior.supplement.mutation-slot-i**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic |

Gain one mutation slot. During a completed short or long rest, equip one eligible mutation in it. The equipped mutation remains dormant until activated unless its own text says otherwise.

Prerequisite: Warrior 1

<details><summary>Preserved source wording — book line4788</summary>

| 1 | Mutation Slot I (choose 1), Brutality Threshold (BT) tracker |

</details>

#### Brutality Threshold Tracker

**Level 1 · automatic · warrior.supplement.brutality-threshold-tracker**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Encounter | Automatic |

Track Brutality Progress and BT using the common Warrior engine. Default BT cap is 3. Encounter end resets both to 0.

Prerequisite: Warrior 1

<details><summary>Preserved source wording — book line4788</summary>

| 1 | Mutation Slot I (choose 1), Brutality Threshold (BT) tracker |

</details>

#### Mutagen Injection

**Level 2 · automatic · warrior.supplement.mutagen-injection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +1 Strain | Self | 3 rounds | 1/short rest |

Choose Power or Guard. Power grants +2 Strength, maximum 22 from this feature. Guard grants +2 AC. This emergency mutagen does not consume a prepared serum dose and does not activate a mutation.

Prerequisite: Warrior 2

<details><summary>Preserved source wording — book line4789</summary>

| 2 | Mutagen Injection (1/rest: +2 STR or +2 AC for 3 rounds) |

</details>

#### Awakened

**Level 1 · supplement · warrior.supplement.awakened**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While BT remains at least 1 | State |

Once per encounter, when a serum activation would add Strain, reduce that Strain gain by 1, minimum 0. This represents reduced activation cost; it cannot reduce Serum Cocktail or Mutation Overload below 1 Strain.

Prerequisite: BT 1+

<details><summary>Preserved source wording — book line5066</summary>

| Awakened | Deal 25% of max HP as damage | Mutations cost 10% less to activate |

</details>

#### Primed

**Level 1 · supplement · warrior.supplement.primed**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One active mutation each turn | While BT remains at least 2 | Once per turn |

Enhance one active mutation's numeric benefit for the turn: +1 to one AC, DR, attack, save or flat damage bonus; +5 feet to one movement/reach bonus; or +1 damage/healing to one mutation-generated roll. Primed never increases duration, targets, immunity or resource generation.

Prerequisite: BT 2+

<details><summary>Preserved source wording — book line5067</summary>

| Primed | Deal 50% of max HP as damage | Active mutations gain +25% effectiveness |

</details>

#### Overdrive

**Level 1 · supplement · warrior.supplement.overdrive**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Via Serum Injection | Dose consumption and normal Strain | Injected creature | 3 rounds | Per prepared dose |

Gain +2 to Strength or Dexterity, chosen on preparation, and +10 feet Speed. Side effect: -1 AC for the duration. Serum Tolerance suppresses the side effect but not Strain.

Prerequisite: Prepared serum dose

<details><summary>Preserved source wording — book line5053</summary>

| Overdrive | +2 STR/DEX | +10% Speed | 3 rounds | -10% Defense |

</details>

#### Stonecore

**Level 1 · supplement · warrior.supplement.stonecore**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Via Serum Injection | Dose consumption and normal Strain | Injected creature | 3 rounds | Per prepared dose |

Gain +2 AC and immunity to forced movement or knockback from creatures no more than one size larger. Side effect: Speed -10 feet. Serum Tolerance suppresses the Speed penalty.

Prerequisite: Prepared serum dose

<details><summary>Preserved source wording — book line5054</summary>

| Stonecore | +2 AC | Immunity to knockback | 3 rounds | -15% Speed |

</details>

#### Sanguine Surge

**Level 1 · supplement · warrior.supplement.sanguine-surge**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Via Serum Injection | Dose consumption and normal Strain | Injected living creature | 3 rounds | Per prepared dose; same creature cannot receive its healing more than once per short rest |

On injection regain 2d6 HP and gain +10 feet Speed for 3 rounds. Side effect: when the profile ends gain 1 additional Strain, maximum 3. Serum Tolerance suppresses that ending side effect. This healing removes no Wounds and cannot operate on a dead creature.

Prerequisite: Prepared serum dose

<details><summary>Preserved source wording — book line5055</summary>

| Sanguine Surge | Heal 2d6 | +10 ft speed | 3 rounds | Increased Hunger |

</details>

#### Mind Shock

**Level 1 · supplement · warrior.supplement.mind-shock**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Via Serum Injection | Dose consumption and normal Strain | Injected creature | 3 rounds | Per prepared dose |

Gain +2 on saving throws against spells. Once during the duration gain one additional Reaction usable only for movement, defense, Counterspell-like disruption already possessed or another non-attack reaction; it cannot make an attack. Side effect: -1 on Perception checks for the duration. Serum Tolerance suppresses that penalty.

Prerequisite: Prepared serum dose

<details><summary>Preserved source wording — book line5056</summary>

| Mind Shock | +2 Save vs spells | +1 reaction use this turn | 3 rounds | Minor Hallucinations |

</details>

#### Chromatic Flux

**Level 1 · supplement · warrior.supplement.chromatic-flux**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Via Serum Injection | Dose consumption and normal Strain | Injected creature | 3 rounds | Per prepared dose |

Gain advantage on Stealth checks when at least lightly obscured and choose extreme heat or extreme cold; you ignore ordinary environmental penalties from that choice during the duration. Side effect: vivid discoloration gives disadvantage on attempts to pass as physically unaltered. Serum Tolerance suppresses that social side effect.

Prerequisite: Prepared serum dose

<details><summary>Preserved source wording — book line5057</summary>

| Chromatic Flux | Adaptive Camouflage | Environmental Adaptation | 3 rounds | Skin Discoloration |

</details>

#### Berserker Brew

**Level 1 · supplement · warrior.supplement.berserker-brew**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Via Serum Injection | Dose consumption and normal Strain | Injected creature | 3 rounds | Per prepared dose |

You are immune to Frightened and once on each of your turns add 2 S damage to one melee weapon or natural-weapon hit. Side effect: -1 AC and you cannot voluntarily take Dodge or Disengage. Serum Tolerance suppresses the side effect but not the once-per-turn damage cap.

Prerequisite: Prepared serum dose

<details><summary>Preserved source wording — book line5058</summary>

| Berserker Brew | +40% Damage | Fear Immunity | 3 rounds | Temporary Madness |

</details>

#### Ironhide Graft

**Level 1 · supplement · warrior.supplement.ironhide-graft**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

Gain +2 AC against melee attack rolls and reduce the first physical weapon damage you take each round by 1.

Prerequisite: Warrior 1; Basic Vital

<details><summary>Preserved source wording — book line4937</summary>

| Ironhide Graft | +2 AC vs melee, +1 DR |

</details>

#### Bloodthick Node

**Level 1 · supplement · warrior.supplement.bloodthick-node**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active during a real encounter | Once at start of each regular turn |

Regain HP equal to current BT, maximum 3 HP per turn or 4 with Stack Overflow. No healing occurs outside a real encounter and it removes no Wounds. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

Prerequisite: Warrior 1; Basic Vital

<details><summary>Preserved source wording — book line4938</summary>

| Bloodthick Node | Heal 1 HP per BT stack each round |

</details>

#### Spinal Buffer

**Level 1 · supplement · warrior.supplement.spinal-buffer**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

Gain +1 on saving throws against being knocked Prone, Stunned or forcibly moved. If an effect uses an ability check rather than a save, add +1 to that check instead.

Prerequisite: Warrior 1; Basic Vital

<details><summary>Preserved source wording — book line4939</summary>

| Spinal Buffer | +1 Save vs knockback, stuns, and forced movement |

</details>

#### Flesh Warden

**Level 1 · supplement · warrior.supplement.flesh-warden**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while equipped | One mutation slot | Self | While equipped | Mutation |

Increase maximum HP by 2 per Warrior level while equipped. Equipping raises maximum only, never current HP. Unequipping clamps current HP to the reduced maximum if necessary; it does not subtract another amount from current HP. Repeated swaps cannot heal.

Prerequisite: Warrior 1; Basic Vital

<details><summary>Preserved source wording — book line4940</summary>

| Flesh Warden | +2 HP per level |

</details>

#### Plated Shoulder

**Level 1 · supplement · warrior.supplement.plated-shoulder**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

While adjacent to substantial terrain, a wall or a willing ally of your size or larger, you gain half cover against ranged attacks.

Prerequisite: Warrior 1; Basic Vital

<details><summary>Preserved source wording — book line4941</summary>

| Plated Shoulder | Gain half cover while standing adjacent to terrain or ally |

</details>

#### Brute Knuckles

**Level 1 · supplement · warrior.supplement.brute-knuckles**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

Your unarmed strike damage die becomes 1d10. On an unarmed critical hit, the target makes a Strength save; on failure it drops one non-attuned held item of its choice.

Prerequisite: Warrior 1; Basic Combat

<details><summary>Preserved source wording — book line4978</summary>

| Brute Knuckles | Unarmed strikes deal 1d10 and apply Disarm on crit |

</details>

#### Splinter Bone Fangs

**Level 1 · supplement · warrior.supplement.splinter-bone-fangs**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Creature critically hit by your melee attack | 2 rounds | At most once per target per turn |

A melee critical applies Bleed. The target takes 1d4 physical damage at the start of each of its next 2 turns. Reapplication refreshes rather than stacks.

Prerequisite: Warrior 1; Basic Combat

<details><summary>Preserved source wording — book line4979</summary>

| Splinter Bone Fangs | Melee crits cause 1d4 bleed for 2 rounds |

</details>

#### Lashing Ligaments

**Level 1 · supplement · warrior.supplement.lashing-ligaments**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Once per turn |

For one melee attack on your turn, increase your reach by 5 feet. Using the extended reach does not itself provoke opportunity attacks.

Prerequisite: Warrior 1; Basic Combat

<details><summary>Preserved source wording — book line4980</summary>

| Lashing Ligaments | Gain +5 ft melee reach once per turn (doesn't provoke AoO) |

</details>

#### Jaw Clench Node

**Level 1 · supplement · warrior.supplement.jaw-clench-node**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Self | Until end of your next regular turn | At most once per turn |

After you score a critical hit, gain +1 on attack rolls and +2 on Intimidation checks until the end of your next regular turn.

Prerequisite: Warrior 1; Basic Combat

<details><summary>Preserved source wording — book line4981</summary>

| Jaw Clench Node | Gain +1 to hit and +2 to Intimidation for 1 round after crit |

</details>

#### Shoulder Spike Cluster

**Level 1 · supplement · warrior.supplement.shoulder-spike-cluster**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Creature grappling you or grappled by you | Instantaneous | Once per creature per round |

When a grapple is established or maintained against you, or you successfully establish a grapple, the other creature takes 1d6 piercing damage.

Prerequisite: Warrior 1; Basic Combat

<details><summary>Preserved source wording — book line4982</summary>

| Shoulder Spike Cluster | When grappling or being grappled, attacker takes 1d6 damage |

</details>

#### Ink-Slick Glands

**Level 1 · supplement · warrior.supplement.ink-slick-glands**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action while active | One mutation slot; serum activation | 10-foot-radius cloud centered within 10 feet | 2 rounds | 1/short rest |

Create opaque black mist. Creatures outside the cloud cannot see through it; ranged attacks passing through the cloud have disadvantage. Wind or an equivalent dispersal effect may end it early.

Prerequisite: Warrior 1; Basic Aberrant

<details><summary>Preserved source wording — book line5019</summary>

| Ink-Slick Glands | Once per rest, exude a cloud of black mist (3x3, blocks LoS, causes Disadvantage on ranged attacks) |

</details>

#### Pulsing Vein Spiral

**Level 1 · supplement · warrior.supplement.pulsing-vein-spiral**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self and enemies within 5 feet | While active | Mutation |

Gain +2 on Intimidation checks. Enemies within 5 feet take -1 on morale checks or the campaign's equivalent morale roll; this does not alter attack rolls or saving throws.

Prerequisite: Warrior 1; Basic Aberrant

<details><summary>Preserved source wording — book line5020</summary>

| Pulsing Vein Spiral | Gain +2 to Intimidation and cause –1 morale on adjacent enemies |

</details>

#### Tremor Claws

**Level 1 · supplement · warrior.supplement.tremor-claws**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Creature critically hit by your melee attack | Instantaneous | At most once per target per turn |

After a melee critical, the target makes a Strength save. On failure it falls Prone.

Prerequisite: Warrior 1; Basic Aberrant

<details><summary>Preserved source wording — book line5021</summary>

| Tremor Claws | Your melee crits force target to make STR save or fall prone |

</details>

#### Rib Lash Tendrils

**Level 1 · supplement · warrior.supplement.rib-lash-tendrils**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Melee attacker within 10 feet | Instantaneous | Once per round |

When a creature damages you with a melee attack, it takes 1d4 psychic damage. This retaliation cannot trigger itself or other retaliation loops.

Prerequisite: Warrior 1; Basic Aberrant

<details><summary>Preserved source wording — book line5022</summary>

| Rib Lash Tendrils | When you are hit in melee, deal 1d4 retaliatory psychic damage |

</details>

#### Bone Lure Growth

**Level 1 · supplement · warrior.supplement.bone-lure-growth**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action while active | One mutation slot; serum activation | One enemy within 20 feet | Instantaneous | 1/encounter |

The target makes a Wisdom save. On failure it must use up to 15 feet of its available movement to move toward you by the safest path. This movement cannot force it into obviously lethal terrain and never consumes its Action.

Prerequisite: Warrior 1; Basic Aberrant

<details><summary>Preserved source wording — book line5023</summary>

| Bone Lure Growth | Once per encounter, force 1 enemy within 4 tiles to move toward you (WIS save negates) |

</details>

## Arch cards

#### Mutation Efficiency

**Level 3 · selection · warrior.arch.mutation-efficiency**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Mutation Efficiency. You may maintain up to two equipped mutations active simultaneously instead of one. Activating a third mutation while two are already active requires choosing one active mutation to become dormant unless another explicit feature temporarily raises this limit. Mutation slots, serum costs, Strain and mutation durations remain unchanged.

<details><summary>Preserved source wording — book line4818</summary>

Mutation Efficiency: May have 2 active mutations at once (Lv 3)

</details>

#### Brutal Fortitude

**Level 3 · selection · warrior.arch.brutal-fortitude**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While BT is present | Always |

Brutal Fortitude. Reduce damage you take by 1 for each current BT, to a maximum DR 3 from this feature. Stack Overflow can raise your BT cap to 4 but does not raise Brutal Fortitude above DR 3. Losing or spending BT immediately lowers this DR.

<details><summary>Preserved source wording — book line4819</summary>

Brutal Fortitude: Gain +1 DR for each BT stack (max +3)

</details>

#### Overpressure Response

**Level 5 · selection · warrior.arch.overpressure-response**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One equipped dormant mutation | 3 rounds or its shorter printed duration | Once per round |

Overpressure Response. When you take a critical hit, choose one equipped dormant non-Apex mutation and activate it without consuming a serum dose or gaining Strain. This activation must respect your normal simultaneous-active-mutation limit; if necessary, make another active mutation dormant. It grants no serum-profile benefit and cannot activate a mutation whose prerequisite you do not meet.

<details><summary>Preserved source wording — book line4820</summary>

Overpressure Response: Once per round, when struck by a critical hit, gain 1 free mutation activation

</details>

#### Crushing Advance

**Level 5 · selection · warrior.arch.crushing-advance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | Self; 20-foot straight movement path and creatures crossed or approached within 5 feet | Instantaneous | 1/long rest |

Crushing Advance. Move up to 20 feet in a straight line without provoking opportunity attacks. Each enemy no more than one size larger whose space or reach-line you pass through or adjacent to makes a Strength save. On failure it takes 2d6 bludgeoning damage, is pushed to the nearest legal space outside your path and falls Prone. On success it takes half damage and is neither pushed nor Prone. A creature is affected once per use.

<details><summary>Preserved source wording — book line4821</summary>

Crushing Advance: Once per long rest, move in a straight line up to 20 ft, knocking aside all enemies (STR save or fall prone, take 2d6)

</details>

#### Pain Conversion

**Level 7 · selection · warrior.arch.pain-conversion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Until end of your next regular turn | At most once per round |

Pain Conversion. After one damage event deals actual damage to you, gain a temporary Power bonus equal to floor(actual damage/10), minimum 1 and maximum 3. Until the end of your next regular turn, add that bonus to one Strength-based weapon damage roll or Strength check. A later trigger refreshes the duration and replaces the previous bonus rather than stacking.

<details><summary>Preserved source wording — book line4822</summary>

Pain Conversion: Convert 10% of damage taken into temporary Strength bonus.

</details>

#### Adaptive Tissue

**Level 7 · selection · warrior.arch.adaptive-tissue**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Until completion of a short or long rest | One remembered damage type at a time |

Adaptive Tissue. When a critical hit deals acid, cold, fire, lightning, necrotic, poison, psychic, radiant or thunder damage to you, gain resistance to one such damage type dealt by that hit until you complete a short or long rest. Gaining a new Adaptive Tissue resistance replaces the previous one. Immunity and duplicate resistance do not stack.

<details><summary>Preserved source wording — book line4823</summary>

Adaptive Tissue: Gain resistance to the last damage type that critically hit you until your next rest.

</details>

#### Brutality Momentum

**Level 9 · selection · warrior.arch.brutality-momentum**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Your Brutal Strike | Instantaneous | At most once per round |

Brutality Momentum. When you personally reduce a creature marked Vulnerable by Brutality Sense to 0 HP with a melee attack, set Brutal Strike's positive round-recharge counter to 0 if it has not already been reset or shortened this round. This restores no Action and cannot refresh a per-rest use. Trivial, summoned or friendly creatures cannot trigger it.

<details><summary>Preserved source wording — book line4824</summary>

Brutality Momentum: Killing a marked vulnerable target instantly readies your next Brutal Strike.

</details>

#### Mutation Overload

**Level 3 · selection · warrior.arch.mutation-overload**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +2 Strain | Your currently active mutations | 2 rounds; backlash until end of following turn | 1/short rest |

Mutation Overload. For 2 rounds, enhance each currently active mutation once: an AC, DR, attack, save or flat-damage bonus increases by 1; a movement or reach bonus increases by 5 feet; or one mutation damage/healing roll gains +1d4. Immunities, target counts, resource generation and action grants cannot be increased. When Overload ends, you suffer -1 on attack rolls and saving throws and -5 feet Speed until the end of your next regular turn. This activation is illegal if +2 Strain would exceed the Strain cap.

<details><summary>Preserved source wording — book line4827</summary>

Mutation Overload: Push your mutations beyond safe limits, gaining significantly enhanced effects for 2 rounds followed by exhaustion.

</details>

#### Serum Cocktail

**Level 5 · selection · warrior.arch.serum-cocktail**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | Consume 2 different prepared serum doses; +2 Strain | Self | 3 rounds | 1/short rest |

Serum Cocktail. Choose two different prepared serum profiles, consume both doses and apply both profiles to yourself for 3 rounds while activating one eligible equipped mutation. Same-stat bonuses use only the stronger value. Both profile side effects apply unless Serum Tolerance suppresses them. This activates only one mutation and therefore differs from Serum Overclock. It is illegal if the resulting Strain would exceed 3.

<details><summary>Preserved source wording — book line4828</summary>

Serum Cocktail: Combine two different serums for a hybrid effect, though with increased strain on your body.

</details>

#### Brutality Unleashed

**Level 7 · selection · warrior.arch.brutality-unleashed**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Spend all 3 BT; requires Unleashed state | Enemies of your choice within 15 feet | Instantaneous | At will when requirement is met |

Brutality Unleashed. Spend all 3 BT. Each chosen enemy within 15 feet makes a Strength save, taking (S+1)d8 + M bludgeoning damage and being pushed 10 feet on failure, or half damage with no push on success. Spending the BT immediately ends Awakened, Primed and Unleashed state benefits. This is one area attack and cannot generate BT or Brutality Progress from its own damage.

<details><summary>Preserved source wording — book line4829</summary>

Brutality Unleashed: Once your Brutality Threshold is crossed, unleash a devastating area attack that damages all enemies within range.

</details>

#### Survival Adaptation

**Level 7 · selection · warrior.arch.survival-adaptation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | 3 rounds | 1/short rest |

Survival Adaptation. Choose one hazard when activated: extreme heat, extreme cold, poisonous atmosphere, high altitude/low oxygen, corrosive environment or difficult natural terrain. For 3 rounds you ignore ordinary environmental penalties from that hazard; if it deals acid, cold, fire or poison damage, you instead gain resistance to that one damage type. This grants no immunity and does not protect allies.

<details><summary>Preserved source wording — book line4830</summary>

Survival Adaptation: Rapidly adapt your body to environmental hazards, gaining temporary resistance to environmental effects.

</details>

#### Intimidating Transformation

**Level 9 · selection · warrior.arch.intimidating-transformation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | +1 Strain | Up to 3 enemies of your choice within 20 feet that can see you | Maximum 2 rounds | 1/short rest |

Intimidating Transformation. Each target makes a Wisdom save. On failure it is Frightened of you until the end of its next turn and then repeats the save. On a failure by 10 or more, it would instead be Stunned until the end of its next turn, subject to the Warrior hard-control guard. A target succeeding on the initial save is immune to this use. The transformation does not force surrender or belief changes.

<details><summary>Preserved source wording — book line4831</summary>

Intimidating Transformation: Undergo a particularly terrifying mutation that can cause enemies to become frightened or even paralyzed with fear.

</details>

#### Mutation Slot II

**Level 5 · automatic · warrior.supplement.mutation-slot-ii**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic |

Gain a second mutation slot. This does not by itself raise the active-mutation concurrency limit.

Prerequisite: Warrior 5

<details><summary>Preserved source wording — book line4791</summary>

| 5 | Mutation Slot II unlocked |

</details>

#### Bone Hardened

**Level 6 · automatic · warrior.supplement.bone-hardened**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic |

While you are not Staggered, reduce physical weapon damage you take by 1 after resistance and before temporary HP.

Prerequisite: Warrior 6

<details><summary>Preserved source wording — book line4792</summary>

| 6 | Bone Hardened: DR +1 while not staggered |

</details>

#### Serum Overclock

**Level 9 · automatic · warrior.supplement.serum-overclock**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | Consume 2 prepared serum doses; +2 Strain | Self | 3 rounds | 1/short rest |

Inject two different prepared serum profiles simultaneously and activate up to two eligible equipped mutations, respecting your active-mutation limit. Resolve both profile effects; same-stat bonuses use the stronger. Overclock is illegal if the resulting Strain would exceed 3.

Prerequisite: Warrior 9, Strain 1 or lower, two prepared serum doses

<details><summary>Preserved source wording — book line4793</summary>

| 9 | Serum Overclock: Inject 2 serums at once |

</details>

#### Unleashed

**Level 3 · supplement · warrior.supplement.unleashed**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While BT remains at least 3 | State |

You satisfy the Brutality Threshold requirement for Brutality Unleashed and other features explicitly requiring the Unleashed state.

Prerequisite: BT 3+

<details><summary>Preserved source wording — book line5068</summary>

| Unleashed | Deal 75% of max HP as damage | Unlock Brutality Unleashed ability |

</details>

#### Redundant Organs

**Level 6 · supplement · warrior.supplement.redundant-organs**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Self | Instantaneous | 1/long rest |

When damage would reduce you to 0 HP without killing you outright, remain at 1 HP instead.

Prerequisite: Warrior 6; Advanced Vital

<details><summary>Preserved source wording — book line4946</summary>

| Redundant Organs | First time you'd fall to 0 HP, stay at 1 (1/long rest) |

</details>

#### Rapid Coagulation

**Level 6 · supplement · warrior.supplement.rapid-coagulation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active during a real encounter | Start of turn |

If you did not move during your previous turn, regain 2 HP at the start of your current turn. This does not function outside a real encounter. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

Prerequisite: Warrior 6; Advanced Vital

<details><summary>Preserved source wording — book line4947</summary>

| Rapid Coagulation | Gain Regeneration 2 if you haven't moved this round |

</details>

#### Ossified Core

**Level 6 · supplement · warrior.supplement.ossified-core**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

Critical hits against you do not add extra critical damage dice. Additionally reduce piercing damage you take by 2 after resistance.

Prerequisite: Warrior 6; Advanced Vital

<details><summary>Preserved source wording — book line4948</summary>

| Ossified Core | Immune to crit damage; take 2 less damage from piercing attacks |

</details>

#### Adrenal Floodgate

**Level 6 · supplement · warrior.supplement.adrenal-floodgate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Self | Instantaneous | 1/encounter |

When you first fall to one-quarter maximum HP or less, regain 2d8 HP and end either Frightened, Poisoned or Staggered on yourself.

Prerequisite: Warrior 6; Advanced Vital

<details><summary>Preserved source wording — book line4949</summary>

| Adrenal Floodgate | Once per encounter, heal 2d8 HP and remove 1 condition when you drop below 25% HP |

</details>

#### Thickened Bone Weave

**Level 6 · supplement · warrior.supplement.thickened-bone-weave**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Self | Until end of your next regular turn | At most once per round |

When you activate a serum or gain at least 1 BT, gain DR 2 against physical weapon damage until the end of your next regular turn. Reapplication refreshes but does not stack.

Prerequisite: Warrior 6; Advanced Vital

<details><summary>Preserved source wording — book line4950</summary>

| Thickened Bone Weave | +2 DR for 2 rounds after using a serum or gaining a BT stack |

</details>

#### Shock Muscle Weave

**Level 6 · supplement · warrior.supplement.shock-muscle-weave**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Once on your regular turn |

When you take the ordinary Attack action, make one additional melee weapon attack. This additional attack is not a new Action and cannot itself grant another attack. It does not apply to card techniques unless they explicitly use the ordinary Attack action.

Prerequisite: Warrior 6; Advanced Combat

<details><summary>Preserved source wording — book line4987</summary>

| Shock Muscle Weave | Gain +1 attack per turn (stacks with extra attacks, but only melee) |

</details>

#### Razorbone Growths

**Level 6 · supplement · warrior.supplement.razorbone-growths**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Your melee attacks | While active | Mutation |

Your melee attacks ignore 1 point of flat DR. Resistance and immunity are unaffected.

Prerequisite: Warrior 6; Advanced Combat

<details><summary>Preserved source wording — book line4988</summary>

| Razorbone Growths | All melee attacks ignore 1 point of DR |

</details>

#### Echo Knuckles

**Level 6 · supplement · warrior.supplement.echo-knuckles**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | One creature within unarmed reach | Instantaneous | Once per round |

After you hit with a melee attack, make one offhand slam against the same target using your Warrior technique attack. On hit deal 1d8+M bludgeoning damage. This is a free attack, cannot trigger Echo Knuckles again and cannot grant another free attack.

Prerequisite: Warrior 6; Advanced Combat

<details><summary>Preserved source wording — book line4989</summary>

| Echo Knuckles | Once per round, after hitting, make a free offhand slam (1d8) |

</details>

#### Adrenal Backlash Core

**Level 6 · supplement · warrior.supplement.adrenal-backlash-core**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Self then next melee target | Until end of your next regular turn | At most once per round |

After you take damage, empower your next melee hit before the end of your next regular turn to deal +2d6 damage of the weapon's normal type. A new trigger refreshes but does not stack.

Prerequisite: Warrior 6; Advanced Combat

<details><summary>Preserved source wording — book line4990</summary>

| Adrenal Backlash Core | When you take damage, your next melee hit deals +2d6 |

</details>

#### Warpgrip Talons

**Level 6 · supplement · warrior.supplement.warpgrip-talons**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Creature critically hit by your melee attack | 2 rounds | At most once per target per turn |

A melee critical applies Weakened for 2 rounds. While Weakened, the target deals 1 less damage with each weapon or natural-weapon hit, minimum 0. Reapplication refreshes rather than stacks.

Prerequisite: Warrior 6; Advanced Combat

<details><summary>Preserved source wording — book line4991</summary>

| Warpgrip Talons | Melee attacks apply Weakened on crit (–1 damage from target for 2 rounds) |

</details>

#### Throat Split Maw

**Level 6 · supplement · warrior.supplement.throat-split-maw**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | One creature within 5 feet | Until end of target's next turn | Once per target per round |

You gain a bite attack dealing 1d8+M piercing damage. When the bite hits a creature capable of casting spells, it makes a Constitution save; on failure it is Silenced until the end of its next turn.

Prerequisite: Warrior 6; Advanced Aberrant

<details><summary>Preserved source wording — book line5028</summary>

| Throat Split Maw | Your bite attack silences casters for 1 round on hit |

</details>

#### Viral Core Sacs

**Level 6 · supplement · warrior.supplement.viral-core-sacs**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Enemies within 10 feet | Until start of your next regular turn | Once per serum activation |

When you activate a serum, enemies within 10 feet make Constitution saves. On failure they have disadvantage on their next saving throw before the start of your next regular turn.

Prerequisite: Warrior 6; Advanced Aberrant

<details><summary>Preserved source wording — book line5029</summary>

| Viral Core Sacs | When using a serum, release a 2x2 AoE that causes Disadvantage on saves for 1 round |

</details>

#### Scythebone Spikes

**Level 6 · supplement · warrior.supplement.scythebone-spikes**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Your unarmed strike target and one different adjacent creature | Instantaneous | Once per turn |

When an unarmed strike hits, choose one different enemy within 5 feet of the original target. If the same attack roll would hit that enemy's AC, it takes damage equal to the unarmed strike's base damage die without modifiers. This cleave is not another attack and triggers no on-hit effects.

Prerequisite: Warrior 6; Advanced Aberrant

<details><summary>Preserved source wording — book line5030</summary>

| Scythebone Spikes | Your unarmed strikes gain cleave (hit 2 adjacent targets) |

</details>

#### Carrion Signal Gland

**Level 6 · supplement · warrior.supplement.carrion-signal-gland**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Creature that hits you in melee | Until end of target's next turn | Once per attacker per round |

The attacker makes a Wisdom save. On failure it becomes Shaken, taking -1 on attack rolls until the end of its next turn.

Prerequisite: Warrior 6; Advanced Aberrant

<details><summary>Preserved source wording — book line5031</summary>

| Carrion Signal Gland | Enemies who hit you in melee must make WIS save or become Shaken |

</details>

#### Wailing Eye Cluster

**Level 6 · supplement · warrior.supplement.wailing-eye-cluster**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action while active | One mutation slot; serum activation | Enemies within 15 feet | Until end of target's next turn | 1/short rest |

Enemies make Wisdom saves. On failure they become Disoriented: at the start of their next turn they cannot take Reactions and their first 5 feet of movement must be in a random legal horizontal direction determined by the Director. They otherwise keep their normal Action and movement.

Prerequisite: Warrior 6; Advanced Aberrant

<details><summary>Preserved source wording — book line5032</summary>

| Wailing Eye Cluster | As a bonus action 1/rest, emit a psychic scream: enemies within 3 tiles must save or become Disoriented (random movement) |

</details>

#### Bio-Stabilizer

**Level 4 · supplement · warrior.supplement.bio-stabilizer**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | Feat choice | Self | Permanent | Always |

While at least two mutations are active, Bloodthick Node heals 1 additional HP on each of its valid encounter-only regeneration pulses.

Prerequisite: Warrior 4; Bloodthick Node equipped; eligible feat grant

<details><summary>Preserved source wording — book line4960</summary>

| Bio-Stabilizer | Bloodthick Node | +1 regen while under the effect of 2+ mutations |

</details>

#### Juggernaut's Core

**Level 8 · supplement · warrior.supplement.juggernaut-s-core**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | Feat choice | Self | Permanent | While Ossified Core is active |

While Ossified Core is active, reduce extra damage explicitly granted by Sneak Attack or equivalent precision-damage features by half, rounded down. Ordinary weapon damage is unaffected.

Prerequisite: Warrior 8; Ossified Core equipped; eligible feat grant

<details><summary>Preserved source wording — book line4961</summary>

| Juggernaut's Core | Ossified Core | If you are immune to crits, gain resistance to sneak attack damage |

</details>

#### Living Fortress

**Level 8 · supplement · warrior.supplement.living-fortress**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | Feat choice | Self | Permanent | While at least three Vital mutations are active |

You cannot grant advantage to an enemy solely because it is flanking you. Other sources of advantage still apply.

Prerequisite: Warrior 8; three Vital mutations equipped; eligible feat grant

<details><summary>Preserved source wording — book line4962</summary>

| Living Fortress | 3 Vital Mutations active | Gain immunity to flanking |

</details>

#### Kill-Chain Adaptation

**Level 4 · supplement · warrior.supplement.kill-chain-adaptation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | Self | Until end of next regular turn | Once per round |

After you personally reduce a meaningful hostile creature to 0 HP with a melee attack, gain +10 feet Speed and +1 on your next melee attack roll before the end of your next regular turn.

Prerequisite: Warrior 4; two Combat mutations equipped; eligible feat grant

<details><summary>Preserved source wording — book line5001</summary>

| Kill-Chain Adaptation | 2 Combat Mutations | After a melee kill, gain +10 ft movement and +1 to hit |

</details>

#### Backlash Engine

**Level 8 · supplement · warrior.supplement.backlash-engine**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | Self | Instantaneous | At most once per round |

While Adrenal Backlash Core is active, the first time each round you take actual damage, gain 1 BT, never above the current cap.

Prerequisite: Warrior 8; Adrenal Backlash Core equipped; eligible feat grant

<details><summary>Preserved source wording — book line5002</summary>

| Backlash Engine | Adrenal Backlash Core | Each time you're hit while mutated, gain +1 BT |

</details>

#### Eviscerator Protocol

**Level 8 · supplement · warrior.supplement.eviscerator-protocol**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | Feat choice | Echo Knuckles target | As chosen condition | When Echo Knuckles hits, once per round |

Choose Bleed or Weakened. Bleed deals 1d4 damage at the start of the target's next 2 turns. Weakened causes -1 damage on weapon and natural-weapon hits for 2 rounds. Reapplication refreshes rather than stacks.

Prerequisite: Warrior 8; Echo Knuckles and Warpgrip Talons equipped; eligible feat grant

<details><summary>Preserved source wording — book line5003</summary>

| Eviscerator Protocol | Echo Knuckles + Talons | Free offhand hits now apply Bleed or Weakened (player choice) |

</details>

#### Distorted Dominance

**Level 4 · supplement · warrior.supplement.distorted-dominance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | Creature failing a save against your Aberrant mutation | Until end of target's next turn | Once per target per encounter |

When a creature fails a save against your Aberrant mutation, it loses its Reaction until the end of its next turn. This provisional normalization replaces the source's undefined loss of an action and does not fully deny the target's turn.

Prerequisite: Warrior 4; any Aberrant mutation equipped; eligible feat grant

<details><summary>Preserved source wording — book line5042</summary>

| Distorted Dominance | Any Aberrant Mutation | Enemies who fail saves vs your effects also lose 1 action |

</details>

#### Terror Engine

**Level 8 · supplement · warrior.supplement.terror-engine**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | Feat choice | Self | While condition is met | Always |

While at least two hostile creatures within 30 feet are currently Shaken, Frightened or Disoriented by your Warrior features, reduce the first damage you take each round by 2.

Prerequisite: Warrior 8; Carrion Signal Gland equipped; eligible feat grant

<details><summary>Preserved source wording — book line5043</summary>

| Terror Engine | Carrion Signal Gland | If 2+ enemies are Shaken or Disoriented, gain +2 DR |

</details>

#### Synaptic Rot

**Level 8 · supplement · warrior.supplement.synaptic-rot**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | Enemy within 15 feet failing a Wisdom or Intelligence save against your Warrior feature | Until end of target's next turn | Once per target per round |

When the target fails the qualifying save, it is Silenced until the end of its next turn. This does not prevent non-spell abilities.

Prerequisite: Warrior 8; Wailing Eye Cluster or Viral Core Sacs equipped; eligible feat grant

<details><summary>Preserved source wording — book line5045</summary>

| Synaptic Rot | Wailing Eye or Viral Core | If an enemy fails a WIS or INT save near you, they cannot cast spells next round |

</details>

## Hero cards

### Wardborn

#### Guardian Tissue

**Level 10 · selection · warrior.hero.wardborn.guardian-tissue**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | One adjacent ally and self | Instantaneous | Once per round |

Guardian Tissue. When an adjacent ally would take damage, reduce that ally's incoming damage by one-third rounded down. You take the prevented amount as damage of the same type. This transferred damage cannot be redirected again and cannot trigger another Guardian Tissue. Transferred damage cannot be reduced again, redirected again or generate BT.

<details><summary>Preserved source wording — book line4847</summary>

Guardian Tissue: When an adjacent ally would take damage, you can absorb 30% of it as a reaction.

</details>

#### Protective Mutations

**Level 10 · selection · warrior.hero.wardborn.protective-mutations**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Allies within 5 feet while you have at least one active mutation | While conditions are met | Always |

Protective Mutations. While at least one mutation is active, each ally other than you within 5 feet reduces the first damage it takes each round by S, minimum 0. Multiple Protective Mutations do not stack. The protection ends immediately when the ally leaves the aura or you have no active mutation.

<details><summary>Preserved source wording — book line4848</summary>

Protective Mutations: Your mutations generate a 5-foot aura that grants allies +10% damage resistance.

</details>

#### Serum Sharing

**Level 12 · selection · warrior.hero.wardborn.serum-sharing**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | Consume 1 prepared serum dose | One willing living ally you touch | 3 rounds | At most once per ally per short rest |

Serum Sharing. Inject one willing ally with a diluted prepared serum. The ally receives half of each positive numeric benefit of that serum profile, rounded down with minimum 1, for 3 rounds; nonnumeric immunities become advantage on the relevant save instead. The serum activates no mutation in the ally. The ally gains 1 Strain for this pilot and suffers the profile's printed side effect. Your Serum Tolerance does not protect the ally.

<details><summary>Preserved source wording — book line4849</summary>

Serum Sharing: You can safely inject allies with diluted versions of your serums, granting them 50% of the benefits.

</details>

#### Controlled Transformation

**Level 14 · selection · warrior.hero.wardborn.controlled-transformation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Controlled Transformation. You can suppress obvious cosmetic signs of dormant mutations and reduce visible manifestations of active mutations enough to pass as merely scarred or unusually built while fully clothed. You gain advantage on checks to conceal your Warrior mutations from casual visual inspection. This never suppresses mechanical mutation effects, defeats magical detection or conceals transformations whose cards explicitly make you Large, monstrous or otherwise impossible to hide.

<details><summary>Preserved source wording — book line4850</summary>

Controlled Transformation: Your mutations appear less monstrous and can be partially concealed when necessary.

</details>

#### Aegis Incarnate

**Level 20 · automatic · warrior.hero.wardborn.aegis-incarnate**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self and allies within 15 feet | 3 rounds | 1/long rest; automatic Wardborn Final Form |

Final Form – Aegis Incarnate. For 3 rounds you cannot be forcibly moved or knocked Prone. Whenever an ally within 15 feet takes damage, automatically redirect half that damage rounded down to yourself after the ally's resistance but before its temporary HP; the ally takes the remainder. Redirected damage keeps its type, cannot be reduced again or generate BT, and cannot be redirected again. If taking the redirected damage would kill you outright, the redirection still occurs. This grants no extra Reaction requirement and does not stack with Guardian Tissue on the same damage event.

<details><summary>Preserved source wording — book line4851</summary>

Final Form – Aegis Incarnate: Transform into a living shield for 3 rounds, becoming immovable and redirecting 50% of all damage dealt to allies within 15 feet to yourself.

</details>

#### Bulwark Mutation Tree

**Level 10 · selection · warrior.hero.wardborn.bulwark-mutation-tree**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | When selected |

Bulwark Mutation Tree. Unlock the Wardborn-specific mutations Spinal Plating, Adrenal Overwatch and Living Cover as eligible mutation choices. They occupy normal mutation slots, require serum activation unless their card says otherwise, and obey all active-mutation, tier and Strain rules. Selecting this card does not automatically equip or activate any of them.

<details><summary>Preserved source wording — book line4854</summary>

Bulwark Mutation Tree: Unlocks mutations like:

</details>

#### Mutated Guard

**Level 12 · selection · warrior.hero.wardborn.mutated-guard**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | One ally within 10 feet when your turn ends | Until start of your next regular turn | Once per turn |

Mutated Guard. If you end your turn within 10 feet of at least one ally, choose one such ally. Until the start of your next regular turn it gains +1 on saving throws and reduces the first damage it takes by 1. This benefit does not stack with another Mutated Guard.

<details><summary>Preserved source wording — book line4858</summary>

Mutated Guard: If you end your turn within 2 tiles of an ally, grant them +1 Save and DR

</details>

#### Guardian Pulse

**Level 14 · selection · warrior.hero.wardborn.guardian-pulse**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | One adjacent ally and triggering attacker | Instantaneous | 1/short rest |

Guardian Pulse. Trigger when an adjacent ally is targeted by an attack. You become the target instead; resolve the original attack roll against your AC and defenses. After that attack fully resolves, if the attacker is within your melee reach, make one melee weapon attack against it. This counterattack is a free attack, cannot grant another free attack or Action, and occurs whether the redirected attack hit or missed.

<details><summary>Preserved source wording — book line4859</summary>

Guardian Pulse: 1/rest, redirect an attack from an adjacent ally to yourself and immediately counterstrike

</details>

#### Warding Mutation

**Level 16 · selection · warrior.hero.wardborn.warding-mutation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +1 Strain | Self; protects one ally within 10 feet at a time | 3 rounds | 1/short rest |

Warding Mutation. Grow temporary protective plates for 3 rounds. At the start of each of your turns choose one ally within 10 feet. Until the start of your next turn, the first time that ally takes damage reduce it by S+M, minimum 0. The prevented damage is simply negated rather than transferred. This is a temporary transformation, not an equipped mutation, and cannot stack with itself.

<details><summary>Preserved source wording — book line4860</summary>

Warding Mutation: Develop protective growths that can absorb damage directed at allies.

</details>

#### Stabilizing Injection

**Level 16 · selection · warrior.hero.wardborn.stabilizing-injection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | Consume 1 prepared serum dose | One living creature you touch | Instantaneous | At most once per target per long rest |

Stabilizing Injection. The target regains 2d8 + M HP and may end one of Poisoned, Frightened or Staggered. If Diseased, it may immediately repeat one saving throw the disease normally permits. This removes no Wounds, cannot restore the dead and does not activate a mutation or apply the consumed serum's normal profile.

<details><summary>Preserved source wording — book line4861</summary>

Stabilizing Injection: Use your serum knowledge to create a stabilizing agent that can heal and remove negative status effects.

</details>

### Ironskin

#### Environmental Adaptation

**Level 10 · selection · warrior.hero.ironskin.environmental-adaptation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until 10 minutes after leaving the environment | One adaptation at a time |

Environmental Adaptation. After 1 uninterrupted minute exposed to extreme heat, extreme cold, high altitude/low oxygen, poisonous atmosphere or another Director-defined natural environmental hazard, adapt to it. Ignore ordinary environmental penalties from that hazard and gain advantage on saves against it. Adapting to a new environment replaces the previous adaptation. This does not grant damage immunity.

<details><summary>Preserved source wording — book line4874</summary>

Environmental Adaptation: Your body automatically begins adapting to extreme environments after 1 minute of exposure.

</details>

#### Regenerative Mutation

**Level 10 · selection · warrior.hero.ironskin.regenerative-mutation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | Spend healing amount from Mutation Recovery Reserve | Self | While at least one mutation is active in a real encounter | Once at the start of each regular turn |

Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.

<details><summary>Preserved source wording — book line4875</summary>

Regenerative Mutation: Heal 5% of your maximum health each round while at least one mutation is active.

</details>

#### Serum Recycling

**Level 12 · selection · warrior.hero.ironskin.serum-recycling**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One serum dose you are consuming | Instantaneous | At most once per turn |

Serum Recycling. Whenever you would consume a prepared serum dose, roll a d20. On 17-20, the dose is not consumed after its effects resolve. Strain and all other costs still apply. A preserved dose remains in its original prepared profile and cannot increase your serum reserve above its normal capacity.

<details><summary>Preserved source wording — book line4876</summary>

Serum Recycling: 20% chance to not consume a serum when activating a mutation.

</details>

#### Damage Memory

**Level 14 · selection · warrior.hero.ironskin.damage-memory**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until completion of a short or long rest | Tracks one damage type at a time |

Damage Memory. When you take acid, cold, fire, lightning, necrotic, poison, psychic, radiant or thunder damage, begin or continue remembering that type. The first subsequent damage event of the same type is reduced by 1, the next by 2 and later events by 3, maximum DR 3. Taking a different listed type replaces the remembered type and resets the progression. Resistance applies separately and never upgrades this feature to immunity.

<details><summary>Preserved source wording — book line4877</summary>

Damage Memory: After taking a specific damage type, gain increasing resistance to it with each subsequent hit.

</details>

#### Adaptive Perfection

**Level 20 · automatic · warrior.hero.ironskin.adaptive-perfection**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | 3 rounds | 1/long rest; automatic Ironskin Final Form |

Final Form – Adaptive Perfection. Choose up to three damage types from acid, cold, fire, lightning, necrotic, poison, psychic, radiant or thunder that have actually damaged you since your last long rest, plus one environmental hazard you personally experienced during that period. For 3 rounds you are immune to the chosen damage types and ignore ordinary penalties from the chosen hazard. You cannot choose a type or hazard you did not actually encounter, and multiple immunity sources do not stack.

<details><summary>Preserved source wording — book line4878</summary>

Final Form – Adaptive Perfection: For 3 rounds, gain immunity to the damage types and environmental effects you've been exposed to during the current day.

</details>

#### Gore Mutation Tree

**Level 10 · selection · warrior.hero.ironskin.gore-mutation-tree**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | When selected |

Gore Mutation Tree. Unlock the Ironskin-specific mutations Gore Maw, Reinforced Joints and Shard Skin as eligible mutation choices. They occupy normal mutation slots and obey serum activation, concurrency, tier and Strain rules. Selecting this card equips or activates none of them automatically.

<details><summary>Preserved source wording — book line4881</summary>

Gore Mutation Tree: Unlocks mutations like:

</details>

#### Stack Overflow

**Level 12 · selection · warrior.hero.ironskin.stack-overflow**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Always |

Stack Overflow. Increase your stored BT cap from 3 to 4. Brutal Fortitude remains capped at DR 3. At BT 4 you count as Transcendent for features that explicitly reference stored BT 4, but reaching BT 4 does not itself activate every mutation unless the common Transcendent state says so.

<details><summary>Preserved source wording — book line4885</summary>

Stack Overflow: Can hold up to 4 BT stacks instead of 3

</details>

#### Auto-Rupture

**Level 14 · selection · warrior.hero.ironskin.auto-rupture**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Enemies within 5 feet | Instantaneous | Once per round |

Auto-Rupture. When your stored BT first reaches its current maximum during a round, each enemy within 5 feet makes a Strength save. On failure it falls Prone. The shockwave deals no damage, spends no BT and cannot retrigger from remaining at maximum BT; you must fall below the cap and later reach it again.

<details><summary>Preserved source wording — book line4886</summary>

Auto-Rupture: If you reach max BT, release a shockwave: all adjacent enemies must STR save or fall prone

</details>

#### Adaptive Mutation

**Level 16 · selection · warrior.hero.ironskin.adaptive-mutation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | 0 | Self | 3 rounds | 1/short rest |

Adaptive Mutation. Trigger when you take acid, cold, fire, lightning, poison or another Director-approved environmental damage type, or when an environmental hazard forces you to make a saving throw. Gain resistance to that damage type or advantage on saves against that specific hazard for 3 rounds. Choose one if both apply. This is a temporary transformation and consumes no mutation slot or serum.

<details><summary>Preserved source wording — book line4887</summary>

Adaptive Mutation: Rapidly evolve your body to counter a specific threat or environmental hazard.

</details>

#### Cellular Reconstruction

**Level 16 · selection · warrior.hero.ironskin.cellular-reconstruction**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | 0 | Self | Until start of your next regular turn, then instantaneous recovery | 1/long rest |

Cellular Reconstruction. Enter stasis until the start of your next regular turn: your Speed becomes 0, you cannot take Actions, Bonus Actions or Reactions, and attacks against you have advantage. At the start of your next turn regain 3d8 + M HP and end Poisoned plus one mundane or magical disease that does not explicitly require a special cure. This removes no Wounds and cannot function while dead.

<details><summary>Preserved source wording — book line4888</summary>

Cellular Reconstruction: Enter a brief stasis where your body rapidly heals and purges toxins or diseases.

</details>

### Dreadspawn

#### Horrific Appearance

**Level 10 · selection · warrior.hero.dreadspawn.horrific-appearance**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Up to 3 enemies within 15 feet that can see you | Until end of target's next turn | At most once per target per round |

Horrific Appearance. Whenever you activate a mutation, each qualifying enemy within 15 feet makes a Wisdom save. On failure it is Frightened of you until the end of its next turn. A creature already Frightened by this feature is not forced to save again until that instance ends. This never forces surrender or changes beliefs.

<details><summary>Preserved source wording — book line4901</summary>

Horrific Appearance: Enemies who see you activate a mutation must make a fear save or be frightened for 1 round.

</details>

#### Infectious Mutation

**Level 10 · selection · warrior.hero.dreadspawn.infectious-mutation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | One creature hit by your weapon or natural attack | Until end of target's next turn | At most once per turn |

Infectious Mutation. After you hit a creature, roll a d10. On a 10, painful temporary growths erupt: the target takes S psychic damage and has -1 on its next attack roll or saving throw before the end of its next turn, whichever occurs first. This is not a permanent mutation, disease or body alteration and cannot spread or reproduce.

<details><summary>Preserved source wording — book line4902</summary>

Infectious Mutation: Your attacks have a 10% chance to cause minor, painful mutations in your targets.

</details>

#### Serum Toxicity

**Level 12 · selection · warrior.hero.dreadspawn.serum-toxicity**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self and creatures exposed to your serum or blood | Permanent | Always; retaliation once per round |

Serum Toxicity. A creature other than you that is directly injected with one of your prepared serum doses takes S d6 poison damage after the injection unless a feature expressly makes that serum safe; this damage does not create BT. Additionally, once per round when a creature within 5 feet deals piercing or slashing melee damage to you, it takes S acid damage from your blood. The retaliation cannot recursively trigger itself.

<details><summary>Preserved source wording — book line4903</summary>

Serum Toxicity: Your serums become poisonous to others; your blood deals acid damage to those who wound you.

</details>

#### Pain Empowerment

**Level 14 · selection · warrior.hero.dreadspawn.pain-empowerment**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | While below maximum HP | Always |

Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects.

<details><summary>Preserved source wording — book line4904</summary>

Pain Empowerment: Gain +5% damage for each 10% of health you are missing.

</details>

#### Abomination Ascendant

**Level 20 · automatic · warrior.hero.dreadspawn.abomination-ascendant**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self; fear aura 30 feet | 3 rounds | 1/long rest; automatic Dreadspawn Final Form |

Final Form – Abomination Ascendant. For 3 rounds your melee reach increases by 5 feet, your Speed increases by 10 feet and you gain a natural Claw attack dealing 2d8 + M slashing damage. At the start of each enemy's turn within 30 feet that can see you, it makes a Wisdom save; on failure it is Frightened until the end of that turn. The hard-control guard still applies to any other denial effect you use. This transformation grants no free attacks or additional Actions.

<details><summary>Preserved source wording — book line4905</summary>

Final Form – Abomination Ascendant: Transform into a nightmarish creature for 3 rounds, gaining terrifying new attacks and abilities while causing fear in a 30-foot radius.

</details>

#### Aberrant Mutation Tree

**Level 10 · selection · warrior.hero.dreadspawn.aberrant-mutation-tree**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | When selected |

Aberrant Mutation Tree. Unlock the Dreadspawn-specific mutations Whip-Tendon Limbs, Soul Spike Carapace and Hemophage Core as eligible mutation choices. They occupy normal mutation slots and obey serum activation, concurrency, tier and Strain rules. Selecting this card does not equip or activate any of them.

<details><summary>Preserved source wording — book line4908</summary>

Aberrant Mutation Tree: Unlocks:

</details>

#### Terror Radius

**Level 12 · selection · warrior.hero.dreadspawn.terror-radius**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +1 Strain | Up to 3 enemies within 15 feet | 3 rounds | 1/short rest |

Terror Radius. For 3 rounds, at the start of each enemy's turn within 15 feet it makes a Wisdom save. On failure it suffers -1 AC and -1 on morale checks until the start of its next turn. Each turn grants a new save. The effect does not stack with itself and does not reduce saving throws or attack rolls.

<details><summary>Preserved source wording — book line4912</summary>

Terror Radius: Enemies within 3 tiles at start of turn must save or suffer –1 morale and –1 AC

</details>

#### Apex Aberration (1/day)

**Level 14 · selection · warrior.hero.dreadspawn.apex-aberration-1-day**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +2 Strain | Self | 2 rounds | 1/long rest |

Apex Aberration. For 2 rounds increase Strength by 4, maximum 24 from this feature. You are immune to the effects and damage of hostile rank-3-or-lower spells, but not higher-rank spells, non-spell magical abilities or friendly spells you choose to accept. Whenever your weapon or natural attack hits, the target makes a Wisdom save; on failure it is Frightened until the end of its next turn. This activation is illegal if +2 Strain would exceed the cap.

<details><summary>Preserved source wording — book line4913</summary>

Apex Aberration (1/day): You transform for 2 rounds:

</details>

#### Horrific Mutation

**Level 16 · selection · warrior.hero.dreadspawn.horrific-mutation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Action | +1 Strain | Up to 3 enemies of your choice within 20 feet that can see or hear you | Maximum 2 rounds | 1/short rest |

Horrific Mutation. Each target makes a Wisdom save. On failure it is Frightened until the end of its next turn and then repeats the save. On a failure by 10 or more, it would be Stunned until the end of its next turn, subject to the Warrior hard-control guard. A successful initial save grants immunity to this use. This transformation does not compel surrender or obedience.

<details><summary>Preserved source wording — book line4917</summary>

Horrific Mutation: Undergo a particularly disturbing transformation designed to terrify and demoralize enemies.

</details>

#### Toxic Secretion

**Level 16 · selection · warrior.hero.dreadspawn.toxic-secretion**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | +1 Strain | Self; your melee weapon and natural attacks | 3 rounds | 1/short rest |

Toxic Secretion. For 3 rounds, once on each of your turns when a melee weapon or natural attack hits, add S d4 poison damage. The target then makes a Constitution save; on failure it is Poisoned until the end of its next turn. Repeated applications refresh rather than stack. Poison immunity prevents both the condition and poison damage as normal.

<details><summary>Preserved source wording — book line4918</summary>

Toxic Secretion: Develop glands that secrete powerful toxins, allowing you to poison enemies with your attacks.

</details>

#### Mutation Slot III

**Level 13 · automatic · warrior.supplement.mutation-slot-iii**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Permanent | Automatic |

Gain a third mutation slot. Ordinary active-mutation concurrency remains governed by Mutation Efficiency and explicit exceptions.

Prerequisite: Warrior 13

<details><summary>Preserved source wording — book line4795</summary>

| 13 | Mutation Slot III unlocked |

</details>

#### Brutal Adaptation

**Level 15 · automatic · warrior.supplement.brutal-adaptation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive | 0 | Self | Until next rest | Automatic after rest |

After each completed short or long rest choose one equipped mutation. Gain one of its passive numeric benefits at half value rounded down, minimum 1 where applicable, even while that mutation is dormant. Damage dice, control, immunity, regeneration and trigger effects cannot be selected.

Prerequisite: Warrior 15, at least one equipped mutation

<details><summary>Preserved source wording — book line4796</summary>

| 15 | Brutal Adaptation – Gain passive bonus from a mutation |

</details>

#### Reflexive Mutation

**Level 17 · automatic · warrior.supplement.reflexive-mutation**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction | Consume 1 prepared serum dose; +1 Strain | Self | 3 rounds | Once per round |

When you take damage or fail a Strength, Dexterity or Constitution save, inject one prepared serum and activate one eligible equipped mutation before subsequent effects from the triggering event resolve. It cannot retroactively undo damage or a failed save.

Prerequisite: Warrior 17, legal serum dose and Strain below 3

<details><summary>Preserved source wording — book line4797</summary>

| 17 | Reflexive Mutation – Once per round, mutate reactively |

</details>

#### Apex Form

**Level 20 · automatic · warrior.supplement.apex-form**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Bonus Action | 0 | Self | 3 rounds | 1/encounter |

Gain mutation slot IV permanently. When Apex Form activates, all equipped mutations become active for 3 rounds without consuming serum doses and ignore the normal active-mutation concurrency limit. Serum-profile effects are not granted. When the form ends, choose active mutations up to your normal limit; all others become dormant.

Prerequisite: Warrior 20

<details><summary>Preserved source wording — book line4798</summary>

| 20 | Apex Form – Gain a permanent 4th mutation & unleash once/encounter ultimate form |

</details>

#### Transcendent

**Level 12 · supplement · warrior.supplement.transcendent**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | 0 | Self | Until start of your next regular turn | 1/encounter total, regardless of trigger |

At Warrior 12+, the first time this encounter you cross 100% Brutality Progress or reach stored BT 4, activate all equipped mutations until start of your next regular turn. No serum profile or immediate healing trigger is granted. This is one total pulse, never a permanent BT 4 concurrency increase. At end choose active mutations up to normal limit, with their original remaining durations; others become dormant.

Prerequisite: Warrior 12; 100% Brutality Progress or BT 4 with raised cap; new explicit level gate

<details><summary>Preserved source wording — book line5069</summary>

| Transcendent | Deal 100% of max HP as damage | All mutations active simultaneously for 1 round |

</details>

#### Mythic Carapace

**Level 15 · supplement · warrior.supplement.mythic-carapace**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | Until encounter ends, mutation ends or you fall below one-quarter maximum HP | Apex mutation |

Gain DR 3 against all damage and immunity to Bleed, Poisoned and Burn-style ongoing fire effects. Once per encounter when one hit deals more than 20 actual damage after mitigation, gain 1 BT and refresh the remaining duration of your other active mutations to 3 rounds. It grants no serum-profile refresh.

Prerequisite: Warrior 15; Apex Vital; maximum one Apex equipped

<details><summary>Preserved source wording — book line4955</summary>

| Mythic Carapace | While this is active:<br>- +3 DR flat<br>- Immune to Bleed, Poison, and Burn<br>- Once per combat, when you're struck for more than 20 damage: immediately gain +1 BT and refresh all active mutations<br>- Lasts until the end of combat or you fall below 25% HP |

</details>

#### Butcherform Chassis

**Level 15 · supplement · warrior.supplement.butcherform-chassis**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | 3 rounds or until below one-quarter maximum HP | Apex mutation |

When you take the ordinary Attack action, make one additional melee attack beyond other Extra Attack effects, respecting the one-additional-full-Action guard because this is part of the same Action. Your melee criticals add one extra weapon damage die beyond normal critical dice, not triple total damage. Once per round when you personally kill a meaningful hostile with a melee attack, restore one consumed prepared serum dose, never above reserve capacity.

Prerequisite: Warrior 15; Apex Combat; maximum one Apex equipped

<details><summary>Preserved source wording — book line4996</summary>

| Butcherform Chassis | While active:<br>- Gain +2 attacks per round<br>- Crits deal triple damage<br>- Melee kills instantly refresh 1 serum or 1 mutation use<br>- Lasts for 3 rounds or until you're below 25% HP |

</details>

#### Voidbirth Shell

**Level 15 · supplement · warrior.supplement.voidbirth-shell**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self and enemies within 15 feet | 3 rounds | Apex mutation |

You may move through enemy spaces and nonmagical difficult terrain without extra cost but cannot end inside a creature or solid object. Enemies within 15 feet take -1 on attack rolls and morale. At the end of each of your turns create one 1-HP clone in an adjacent legal space, maximum 2 clones. A clone cannot attack or block movement; when destroyed it explodes, creatures within 5 feet make Dexterity saves taking 2d6 psychic on failure or half on success. Clones grant no resources, corpses, XP or BT.

Prerequisite: Warrior 15; Apex Aberrant; maximum one Apex equipped

<details><summary>Preserved source wording — book line5037</summary>

| Voidbirth Shell | While active:<br>- Gain Ethereal Movement (ignore terrain, move through enemies)<br>- Enemies within 3 tiles have –2 morale and suffer Weakened<br>- Each turn, summon 1 temporary clone (1 HP, explodes on death for 2d6 psychic)<br>- Lasts 3 rounds or until all clones are expended |

</details>

#### Spinal Plating

**Level 10 · supplement · warrior.supplement.spinal-plating**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

Reduce damage you take from area effects by 2 after resistance.

Prerequisite: Wardborn; Bulwark Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4855</summary>

Spinal Plating (+2 DR vs AoE)

</details>

#### Adrenal Overwatch

**Level 10 · supplement · warrior.supplement.adrenal-overwatch**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Reaction while active | One mutation slot; serum activation | Enemy within weapon reach that damages an ally within 5 feet of you | Instantaneous | Once per round |

Make one melee weapon attack against the triggering enemy. This free attack cannot grant another free attack or additional Action.

Prerequisite: Wardborn; Bulwark Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4856</summary>

Adrenal Overwatch (gain reaction attack when ally hit)

</details>

#### Living Cover

**Level 10 · supplement · warrior.supplement.living-cover**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Allies adjacent to you | While active | Mutation |

Adjacent allies gain +2 AC against ranged attacks while you are conscious and not Prone. This does not stack with another Living Cover.

Prerequisite: Wardborn; Bulwark Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4857</summary>

Living Cover (adjacent allies gain +2 AC)

</details>

#### Gore Maw

**Level 10 · supplement · warrior.supplement.gore-maw**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Creature within 5 feet | While active; Bleed 2 rounds | Mutation |

Gain a bite attack dealing 1d8+M piercing. On hit once per turn, the target takes 1d4 Bleed damage at the start of its next 2 turns. Reapplication refreshes.

Prerequisite: Ironskin; Gore Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4882</summary>

Gore Maw (bite attack, 1d8 + bleed)

</details>

#### Reinforced Joints

**Level 10 · supplement · warrior.supplement.reinforced-joints**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Self | While active | Mutation |

You are immune to being knocked Prone by creatures no more than one size larger. Effects from larger creatures instead grant advantage on your save against being knocked Prone.

Prerequisite: Ironskin; Gore Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4883</summary>

Reinforced Joints (immune to prone)

</details>

#### Shard Skin

**Level 10 · supplement · warrior.supplement.shard-skin**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Melee attacker within 5 feet | Instantaneous | Once per round |

When a creature damages you with a melee attack, it takes 1d4 piercing damage. This retaliation cannot trigger another retaliation.

Prerequisite: Ironskin; Gore Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4884</summary>

Shard Skin (1d4 damage to melee attackers)

</details>

#### Whip-Tendon Limbs

**Level 10 · supplement · warrior.supplement.whip-tendon-limbs**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Passive while active | One mutation slot; serum activation | Your melee attacks | While active | Once per turn pull |

Increase melee reach by 5 feet. Once per turn after a melee hit against a creature no more than one size larger, it makes a Strength save; on failure pull it up to 5 feet toward you.

Prerequisite: Dreadspawn; Aberrant Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4909</summary>

Whip-Tendon Limbs (reach + pull effect)

</details>

#### Soul Spike Carapace

**Level 10 · supplement · warrior.supplement.soul-spike-carapace**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Enemies within 10 feet after your melee critical | Instantaneous; fear until end next turn | At most once per round |

When you score a melee critical, gain 1 BT, then enemies of your choice within 10 feet make Wisdom saves. Failure Frightens them until the end of their next turn. The BT gain cannot exceed your cap.

Prerequisite: Dreadspawn; Aberrant Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4910</summary>

Soul Spike Carapace (crit = +1 BT and fear within 2 tiles)

</details>

#### Hemophage Core

**Level 10 · supplement · warrior.supplement.hemophage-core**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered while active | One mutation slot; serum activation | Self | Instantaneous | Once per turn |

When you personally reduce a meaningful hostile creature to 0 HP with a melee attack, regain 2d6 HP. Summoned, trivial, friendly or repeatedly revived creatures cannot trigger this healing. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

Prerequisite: Dreadspawn; Aberrant Mutation Tree; Warrior 10

<details><summary>Preserved source wording — book line4911</summary>

Hemophage Core (heal on kill; absorb 2d6 HP)

</details>

#### Evolution Under Fire

**Level 16 · supplement · warrior.supplement.evolution-under-fire**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | One Warrior ability with positive recharge | Instantaneous | At most once per round |

When one damage event deals more than 15 actual damage to you, reduce one positive Warrior round-recharge counter by 1, minimum 0, subject to the universal reset/shortening cap.

Prerequisite: Warrior 16; any Apex mutation equipped; eligible feat grant

<details><summary>Preserved source wording — book line4963</summary>

| Evolution Under Fire | Any Apex Mutation | Whenever you take >15 damage from a single hit, reduce cooldowns by 1 round |

</details>

#### Hypermutation Spike

**Level 16 · supplement · warrior.supplement.hypermutation-spike**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | Self | For one Butcherform activation | 1/long rest |

When Butcherform Chassis activates, extend its maximum duration from 3 rounds to 5. During that activation you are immune to Stunned and your Speed cannot be reduced below half its normal value.

Prerequisite: Warrior 16; Butcherform Chassis equipped; eligible feat grant

<details><summary>Preserved source wording — book line5004</summary>

| Hypermutation Spike | Butcherform Chassis (Apex) | Once per long rest, extend Butcherform to 5 rounds and become immune to stun/slow during duration |

</details>

#### Born to Horrify

**Level 16 · supplement · warrior.supplement.born-to-horrify**

| Activation | Cost | Range / targets | Duration | Frequency |
|---|---|---|---|---|
| Triggered | Feat choice | Self | Instantaneous | Once per regular turn while an Apex mutation is active |

When you fail a saving throw while an Apex mutation is active, reroll it and use the new result. This can occur at most once on each of your regular turns, not once per enemy turn.

Prerequisite: Warrior 16; any Apex mutation equipped; eligible feat grant

<details><summary>Preserved source wording — book line5044</summary>

| Born to Horrify | Any Apex Mutation | While your Apex mutation is active, you may reroll 1 save per turn |

</details>

## Source appendix and open balance questions

The complete original Warrior book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/warrior.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.

- Do BT accumulation, the three stored states and the 100%-progress Transcendent pulse create a meaningful escalating fight rhythm without making high-damage builds enter Unleashed or Transcendent too early?
- Are mutation slots, active-mutation concurrency, serum dose scarcity and Strain restrictive enough to make preparation meaningful without leaving Warrior powerless after only one or two encounters?
- Do Wardborn mitigation, Ironskin regeneration/adaptation and Dreadspawn control/damage remain comparable after all mutation-tree, Apex and serum interactions are active, especially around Extra Attack and free-attack sources?

A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.
