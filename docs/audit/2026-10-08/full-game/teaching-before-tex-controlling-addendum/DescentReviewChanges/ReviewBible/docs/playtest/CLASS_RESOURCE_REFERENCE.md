# Class resources at the table

**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.** Use this with your acquired class cards and the linked class rules. It consolidates the current playtest configuration; it grants no feature, extra resource or access to an unfinished spell.

Choose your **Base class** first. Arch and Hero features become available only at their own class-level gates. In this sheet, `L` is the level in the named class, `S` is 1/2/3/4 at that class's levels 1/5/11/17, and `M` is the class's effect modifier, normally at least 1. Bard calls its Charisma effect modifier `C`. Use the actual ability modifier for attack rolls and save DCs. See [reading a class card](../mechanics/CLASS_PLAYTEST_RULES.md#reading-a-class-card).

## Set up your counters

Record maximum and current amounts separately. Add a row for each limited feature you actually know, including a Hero feature or Oath/Oathbreaker replacement. Copy its exact frequency, recharge, expiry and recovery rule. A larger maximum does not by itself refill the current amount.

| Resource or feature | Source card / class | Current / maximum | Spent this round or encounter | Next expiry or recovery |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

Keep one character-wide RP pool, Dissonance/Refrain history and ordinary concentration slot, with only explicit exceptions. Track each class's other resources separately. Oracle, Soldier and Warrior contribute no RP pool; a multiclass character may still have RP through another eligible class. Follow the [Resonance reference](RESONANCE_CHEATSHEET.md#multiclass-characters) for the merged pool and spellcasting recovery.

Before an activation, check the known card, level/path, targets, actions, recharge and every cost. An illegal activation spends nothing. A legal paid attempt still spends its costs when it misses or a target saves. A resource gain caused by the result cannot pay that activation's earlier cost. Record actual events; neither staged opposition nor declaring a new encounter creates recovery.

## Find your class

| Class | Main additional records |
|---|---|
| [Bard](#bard) | Crescendo, last performance, pending Echo and maintenance |
| [Cleric](#cleric) | Conviction and actual Conviction expenditure |
| [Crimson Agent](#crimson-agent) | Blood Gauge, gain allowance, Bleeds and Blood Mark |
| [Dragoon](#dragoon) | Momentum, qualifying movement/hit and round gains |
| [Druid](#druid) | Shift uses, form, Buffer Reserve and Form Surge Reserve |
| [Mage](#mage) | Focus, three-cast Nuke Chain, prime deadline and finisher recharge |
| [Mirrorsage](#mirrorsage) | Stored Echo records and the shared release allowance |
| [Monk](#monk) | Ki, own-turn/off-turn gains and stance |
| [Oracle](#oracle) | Revelation Charges and shared combat-refund allowance |
| [Paladin](#paladin) | Lay on Hands points, Smite allowance and Oath uses |
| [Ranger](#ranger) | Weapon history and, from level 11, Hit Chain and Arrow prime |
| [Shaman](#shaman) | Prepared flasks, totems and paid maintenance |
| [Soldier](#soldier) | Ammunition, Overwatch, barricade kits and deployment allowance |
| [Thief](#thief) | Prepared poison doses, coating attempts and expiry |
| [Tinker](#tinker) | Bomb stock/throw allowance, drones and deployable slots |
| [Warrior](#warrior) | Serum doses/Strain, mutations, Brutality and recovery reserve |
| [Wizard](#wizard) | Spellbook, prepared matrices, matrix-family history and limited study |

## Bard

**Crescendo: 0–5.** Begin and end a real encounter at 0, with no last performance. Starting a differently named performance gains 1, including the first performance, at most once on your regular turn. Explicit accelerators raise that turn's ceiling to 2; they do not stack beyond it. Ordinary spells, maintenance and Echo resolution do not supply a new performance or stack.

At 5, the next started performance spends all 5, vents 2 Dissonance and applies its printed rider. It gains no replacement stack; an explicit spend-all cost is paid only once. Damage resets the stacks and last performance unless Fluid Tempo prevents that reset. Silence, incapacitation and failed concentration still reset them. Track one pending Echo and each sustained performance's paid maintenance separately.

[Full rhythm and reset rules](../mechanics/BARD_PLAYTEST_v0_1.md#crescendo-and-rhythm).

## Cleric

**Conviction maximum: 3, becoming 5 at Cleric 9.** A known Conviction Pool adds 2 to the maximum without an immediate refill. A beneficial short rest restores 1 spent Conviction; a beneficial long rest restores the maximum. Conviction persists between encounters. Only explicit features generate it, within their actual limits.

Once on each regular turn, actually spending at least 2 Conviction on a Rite or Invocation vents 1 Dissonance. Waived expenditure does not qualify, and spending more does not multiply the vent. Conviction and RP remain separate costs.

[Cleric engine](../mechanics/classes/cleric.md#class-engine-and-setup).

## Crimson Agent

**Blood Gauge maximum: 3; 6 with acquired Spill Control, or automatically at Crimson Agent 9.** Spill Control can provide capacity 6 earlier but never raises it above 6. The automatic capacity increase does not itself grant Blood Gauge or refill the current amount. Begin and end encounters at 0. Once on your regular turn, a weapon attack damaging a hostile living creature grants 1 BG; Hemorrhage Slash shares that trigger. All gains, including explicit refunds or critical/kill gains, total at most 2 per round. Staged, friendly and sacrificial sources do not qualify.

Once per turn on an ordinary cast, you may spend 1 BG to prevent 1 of that cast's Dissonance gain. This is not an RP discount. Track each Bleed's remaining ticks and the one Blood Mark separately; a damage tick is not a new weapon hit or BG generator.

[Crimson Agent engine](../mechanics/classes/crimson-agent.md#class-engine-and-setup).

## Dragoon

**Momentum maximum: 5; 7 with Momentum Overflow or automatically at Dragoon 9.** Begin and end encounters at 0. On a regular turn, at least 15 feet of qualifying self-powered movement toward a tactical destination grants 1; damaging an enemy with a weapon attack grants 1 more. All gains/refunds together are capped at 2 per round. Forced movement, teleportation and movement in place do not qualify.

Pay Momentum before resolution. A later hit refund cannot finance the same technique. Separately, moving at least 20 feet this turn can reduce an ordinary cast's Dissonance gain by 1; it does not reduce RP.

[Dragoon engine](../mechanics/classes/dragoon.md#class-engine-and-setup).

## Druid

**Shift uses per long rest:** 2/3/4/5/6/7/8 at Druid levels 1/4/7/10/13/16/19. A normal shift uses a Bonus Action and one use, lasting 10 minutes. At level 20, changing form is unlimited; finite form benefits still have their own reserves. Changing forms does not refill them or once-per-rest abilities.

After a long rest, record **Buffer Reserve = 2 L + M** and **Form Surge Reserve = PB**. Pay a form's entire temporary-HP offer from the remaining buffer even if a stronger existing shield wins. A once-per-transformation special also spends 1 Form Surge. Keep your actual HP and Wounds; a form supplies no second beast HP pool. Entering a legal different form clears the remembered repeated-spell name and Refrain counter, without reducing accumulated Dissonance.

At the natural ten-minute endpoint, same-profile renewal costs another shift use below level 20 but no new Bonus Action. It preserves the instance and spent limits: no new shield, Form Surge, entry benefit or Refrain reset. An early attempt to enter the already-current identical profile is rejected without payment. A later genuine reentry still cannot refill shared reserves or per-rest uses.

[Druid engine, forms and level gates](../mechanics/classes/druid.md#class-engine-and-setup) · [Current form-entry and renewal rules](../mechanics/FORM_TEMP_HP_PLAYTEST.md#druid-one-body-throughout).

## Mage

From **Mage 2**, record the selected Fire, Cold or Lightning Focus and the last three consecutive eligible casts. Three different named, legally resolved spells of the selected element complete a Nuke Chain, vent 2 Dissonance and prime the matching finisher through the end of your next regular turn. A different-element or non-elemental spell clears the chain. Repeating a name shifts the window and follows ordinary Refrain.

The primed finisher costs a Bonus Action and 2 RP and has Recharge 3. It is not a chain-building cast. Spending or losing the prime clears the chain; a new prime does not erase a positive recharge counter. Record Resonance Surge's separate once-per-short-rest use and 2 additional RP cost when acquired, plus any selected Hero card's own limits.

[Mage engine](../mechanics/classes/mage.md#class-engine-and-setup).

## Mirrorsage

Begin with **3 empty Echo Slots**. Expansion II raises ordinary capacity to 5; restricted memory features can add a restricted slot, but total stored Echoes never exceeds 6. These are individual captured records, not spell slots. Rest can recover RP without recreating consumed Echoes.

For each record, keep the source creature and witnessed ability, bounded profile, damage type, legal rank, capture encounter and first-release history. Ordinary release pays that rank's RP cost, minimum 2, and consumes the record. First release ignores only Refrain addition, not base Dissonance. Releases, replays, fusions and reflections share one release action per round; a legal combined package still pays for every component. Follow the full rules for capture eligibility and all combined-release exceptions.

[Mirrorsage engine](../mechanics/classes/mirrorsage.md#class-engine-and-setup).

## Monk

**Ki Chain: 0–5.** Start each real encounter at 0; clear it at encounter end or after one minute without a real encounter. Incapacitation or Stunned also clears it. Normal gains are capped at 2 during your own regular turn and 1 total from reactions/defensive events between its end and your next regular turn. Keep those two allowances distinct. Staged actions cannot generate Ki.

Ki does not replace printed RP costs. A Weave-tagged technique normally adds 1 Dissonance; after validating its other costs and before resolution, an additional 1 Ki can prevent that point. Full-Ki techniques may accept the Dissonance instead. Record your one core stance and its once-per-round switch independently.

[Monk engine](../mechanics/classes/monk.md#class-engine-and-setup).

## Oracle

**RC maximum:** 3 at Oracle 1–2, 4 at 3–5, 5 at 6–8, 6 at 9–10 and 7 at 11+. A beneficial short rest restores 1 spent RC; a beneficial long rest restores the maximum. Capacity increases do not refill spent charges.

All combat-triggered RC refunds share **one recovered RC per round**, including Prophecy, damage riders and Curse Boons. At level 11+, a genuine encounter's starting floor is `min(maximum RC, max(3, Charisma modifier))`; keep a higher current amount. Rest, that floor and expressly limited Final refills have their own rules. Free/copied/refunded events cannot recursively generate recovery. Revelations pay RC and do not use ordinary spell RP or erase another class's Dissonance/Refrain history.

[Oracle engine and specific recovery exceptions](../mechanics/classes/oracle.md#class-engine-and-setup).

## Paladin

**Lay on Hands maximum = 5 L.** A beneficial long rest restores it; an encounter transition or short rest does not. The ordinary healing Action spends at most L points for that much HP, subject to healing eligibility and missing HP. The card's separate cleansing option keeps its own cost and restrictions. Smite uses RP, not healing points; Paladin grants neither Conviction nor RC.

Record one paid Smite allowance per numbered round, including any separately permitted Reaction Smite. At level 17, Full Cleansing Wave spends the entire remaining healing pool and is **once per long rest under the explicit cadence amendment**. The preserved Hero card's short-rest wording is superseded by that amendment. An Oathbreaker uses the same remaining pool for Death Touch and applicable replacement effects; changing Oath state does not refill it. Keep the chosen Oath's Signature and other uses separately.

[Paladin engine](../mechanics/classes/paladin.md#class-engine-and-setup) · [Wave and Smite amendment](../mechanics/HEALING_SOURCE_EXTENSIONS.md#paladin-cadence-amendment) · [All ten Oaths and corresponding Oathbreakers](../mechanics/PALADIN_OATHS_AND_OATHBREAKERS.md).

## Ranger

Record the last successful direct weapon hit on your own turns for Weapon Synergy; misses, damage ticks, copies and companions do not advance it. A qualifying direct weapon hit between ordinary spells clears Refrain and gives the next ordinary spell before the end of your next turn a single, nonstacking reduction of 1 Dissonance.

**Hit Chain begins at Ranger 11.** Direct successful weapon hits add 1, at most 2 per regular turn, to a cap of 3. Reaching 3 primes one Arrow until the end of your next turn; Efficient Killer changes the threshold to 2 only when acquired and eligible. Use or expiry consumes the chain, including a missed Arrow. Encounter start/end and incapacitation clear it. A primed Arrow still needs its Action, wielded bow and ammunition; at most one per round, with no self-generated chain.

[Ranger engine](../mechanics/classes/ranger.md#class-engine-and-setup).

## Shaman

After a long rest prepare **2 flasks, 3 at Shaman 5, 4 at 11**; total carried cap 4. There is no encounter refill or stockpiling, and old unused contents become inert when preparing a new batch. Base flasks use an Action. Only Theurgist/Soothsayer gain the advanced magical Bonus Action subsystem at Hero 10; Bloodcaller retains the mundane subsystem.

**Totem capacity is 1, becoming 2 at Shaman 13.** An ordinary new Totem placed at capacity replaces one chosen active Totem; an optional Echo requires its own free capacity and does not evict a Totem. Ending, replacing, destroying or expiring a parent ends its dependent Echo and releases their occupied capacities; administrative Echo ending is not another destruction reward. Track each totem's duration and the shared concentration burden. Renewal costs 2 RP to start, then 1 RP and a Bonus Action on each of the next two turns for three pulses: 4 RP total. Other totem auras have no automatic Renewal upkeep. Moving a totem competes for your Bonus Action; crossing the same creature repeatedly does not renew its once-per-round benefit. Destruction refunds nothing by default. Use the [capacity and dependent-Echo rules](../mechanics/DEVICE_LIFECYCLE_PLAYTEST.md#capacity-placement-and-dependent-totems).

[Shaman engine](../mechanics/classes/shaman.md#class-engine-and-setup).

## Soldier

Track actual ammunition and the one Overwatch zone. Designating a zone spends a Bonus Action; a qualifying shot still spends your Reaction and ammunition. A zone does not create an extra Reaction or autonomous fire.

At **Soldier 5**, Palisade uses carried barricade kits. A long rest with carpentry tools replenishes 2, carried maximum 2. Track a separate encounter deployment allowance of 1, becoming 2 at 13, and the intact-wall cap of 1, becoming 2 at 13. A deployment uses both an actual kit and an allowance. Destruction does not renew uses; replacing a wall beyond the intact cap requires its actual dismantling procedure. The Soldier class grants no RP or spellcasting engine.

[Soldier engine](../mechanics/classes/soldier.md#class-engine-and-setup).

## Thief

With a poison kit, a long rest refills class doses to **3 at Thief 1, 4 at 10, 5 at 15 and 6 at 20**. They cannot be stockpiled or sold. A missing kit prevents preparation. These are fictional class preparations; separately crafted items keep their own records.

A dose coats one melee weapon or two projectiles, lasting one minute or two attack attempts. A miss still spends an attempt. Coating normally takes an Action; the acquired Apply Poison card changes it to a Bonus Action. Record dose identity, coated equipment, attempts and deadline. More doses do not permit multiple simultaneous coatings without the explicit Double Poison exception. Track Sneak Attack's own-turn allowance separately from poison effects and magical-technique RP/Dissonance.

[Thief engine](../mechanics/classes/thief.md#class-engine-and-setup).

## Tinker

With tools, a long rest refills bomb stock to **3 at Tinker 1, 4 at 5 and 5 at 11**. Separately, the encounter throw allowance is **1/2/3** at those levels. Every throw spends one stock and one allowance; no stockpiling or resale, and at most one bomb per regular turn. The normal throw is an Action; Explosive Handling changes that only when acquired.

Track the actual Anacite drone, HP, modules and shared command allowance. Dual Drone Protocols at 13 permits the stated two-drone or two-module choice, without another command budget. Deployable slots are **1 at 6, 2 at 13 and 3 at 17**, separate from drone capacity. Device destruction does not itself refund fuel. Record a crafted automaton's paid service units separately from class RP, HP and commands; repairing one field does not refill the others. Efficient Recycling does not require enemy cause. When the feature is actually acquired, its one-minute postcombat use and once-per-short-rest allowance can refund at most min(1 RP, the RP actually paid to deploy that same owned device), consuming its qualifying usable debris once. Deliberate sacrifice, copied devices, previously consumed debris and prohibited resource-generation or no-own-destruction-chain branches remain excluded. GP construction, service, activation and repair costs are not deployment RP. Other debris consumers retain their own enemy-cause or enemy-hit requirements; use the [source-specific lifecycle predicates](../mechanics/DEVICE_LIFECYCLE_PLAYTEST.md#destruction-debris-and-source-specific-opportunities).

[Tinker engine](../mechanics/classes/tinker.md#class-engine-and-setup) · [Worked commands, repair and service](COMPANION_COMMAND_WALKTHROUGH.md).

## Warrior

**Serum reserve:** 2 prepared doses per long rest, 3 at Warrior 11, 4 at 20. No natural short-rest refill; explicit recovery cannot exceed capacity. A normal injection spends a Bonus Action and one dose, activates an equipped mutation and applies the serum profile for 3 rounds. Same-profile bonuses do not stack.

Keep **Warrior serum Strain (0–3)** separate from expedition Strain. Normal injection adds 1 unless a feature changes it. At 2, Speed is reduced by 5 feet; at 3, also apply −1 AC/−1 saves and the engine's activation restrictions. A beneficial short rest reduces serum Strain by 1; a beneficial long rest resets it to 0. No track silently converts into the other.

Track mutation slots, equipped mutations and active mutations separately: slot counts are **1/2/3/4 at Warrior 1/5/13/20**; ordinary simultaneous activity starts at one and changes only through the named features. **Brutality Progress and BT** begin/end encounters at 0. BT cap is 3, or 4 with Stack Overflow. The actual qualifying damage thresholds and damage-taken gains have separate triggers and share their stated ordinary gain ceiling; use the full engine when updating them. Spending BT can immediately remove a threshold benefit.

After a long rest, **Mutation Recovery Reserve = 3 L + M HP**. The named regenerative features draw 1 point per actual HP healed. Short rests, gauge gains and free activations do not refill it. Other finite dose/use healing keeps its own limit.

[Warrior engine and Brutality thresholds](../mechanics/classes/warrior.md#class-engine-and-setup) · [Separate Strain tracks and recovery](../mechanics/STRAIN_PLAYTEST.md#identify-the-track-first).

## Wizard

Keep the **spellbook** separate from **prepared matrices**. After a long rest, prepare `max(1, Wizard level + Intelligence modifier)` matrices from legal spells in the book. Normal study takes one hour; Matrix Efficiency changes it to 45 minutes when acquired. Duplicate preparations occupy positions but do not create extra first-cast exemptions. Track all copies of one underlying spell as one matrix family for strain/Refrain.

The first cast of each different prepared matrix family in an encounter generates zero **base** Dissonance; actual Refrain and printed strain still apply. Class cards tagged `wizard-spell` are always-prepared class matrices once acquired and do not consume daily positions. Spellbook Study permits one ten-minute substitution between long rests; specific acquired improvements keep their own rules. Preparing, scribing or losing a book does not itself restore RP. A stored spell name never bypasses its class/rank access or unfinished-catalog restriction.

[Wizard engine, study, scribing and book loss](../mechanics/classes/wizard.md#class-engine-and-setup).

## End a turn, end an encounter, finish a rest

At a regular turn boundary, resolve actual deadlines and tick round-recharge counters under the [timing rules](../mechanics/CLASS_PLAYTEST_RULES.md#action-and-timing-limits). An extra Action or extra turn does not supply another regular-turn recharge tick. A named counter can receive at most one reset/shortening per round, and a reset is neither a resource refill nor an extra activation.

At encounter end, clear only what the appropriate engine says to clear. Check pending effects and actual deadlines separately. Do not restore RP, HP, Dissonance, stock, stored Echoes or per-rest uses simply because combat ended.

For recovery, record the actual rest and completion time. The current [rest limits](../mechanics/STRAIN_PLAYTEST.md#recovery-and-actual-elapsed-time) allow at most two beneficial short rests between beneficial long rests and one beneficial long rest per 24 elapsed hours. Short rests require one hour; long rests require eight. Supplies, safety and interruptions still matter. Apply each class's own eligible recovery once, retain unrecovered histories, and record the new current amounts without replacing the old entry.
