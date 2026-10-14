# Remaining131 class healing/recovery semantic matches

Codex → Calibration Review. After closing the selected interface, discuss every remaining source below. Classify each by exact source ID as HEALING_INTERFACE, TEMP_HP, RESOURCE_ONLY, COMPANION_DEVICE, CONDITION_CURE, MOVEMENT_CONTROL_ONLY, TEMPORAL_DEPENDENCY, OTHER_NAMED_DEPENDENCY or EXCLUSION (adjust role where the actual source needs more precision). Identify exact unresolved interface questions, not just keyword labels. Preserve all original source costs/actions/targets/cadences. Do not assume every lexical match heals, and do not approve a whole card because one component is reviewed.

Review potential contradictions involving actual-gain triggers, finite resource recovery, tempHP, copied healing, soul/body reconstruction, stat changes and multiple trigger chains. In particular, advise which systems we must discuss next, and name the exact subset requiring follow-up source evidence. These131 complement the68 selected supplemental passages already discussed; initial79 class sources are separate.

## Codex source-specific findings to resolve

1. Paladin engine[13] says level17 Wave once/LONG rest while the Hero Lay on Hands card reviewed in the preceding package says1/SHORT rest. Explicitly reconcile this evidence; don't leave two active use cadences. Likewise engine[10] says one paid Smite/round while engine[3] has once/own-turn: retain the narrower shared cap if that is the intended override. No original should be deleted.
2. Oracle engine[26] generic paid-zone upkeep conflicts with terse target-start zones such as Resonant Seed (1RC activation, three target-start pulses). How does a source-owned upkeep payment authorize asynchronous allied target-start pulses without paying once PER ally or inventing free rounds? Distinguish limited1/LR Finals like Crown Restored. Which actual zones need a schedule record/overlay next?
3. Lifewell says start AND later turns use BA+1RP to pulse, besides its Action+4RP+allBG activation; confirm first pulse needs that same-turn BA+1RP or identify an explicit correction. Contrast Healing Briar/Restoration Field initial pulse included in activation and later paid maintenance. Shaman Extended Totem/Echo Totem: enforce genuine paid fourth pulse and no double-heal overlap.
4. Healing-dependent riders differ by source: Divine Invocation Renewal gives5Stamina alongside healing (not base Renewal's actual-gain gate); Purging Flame/Zealot Renewal condition cure clauses independent vs conditioned? Flame Prophecy actual healing, Bloodbond paid-technique-heals trigger and Enhanced Convergence tempHP: distinguish actual gain from an attempted legal heal. Zealot Renewal blocked healing still backlash? Fire immunity vs cannot-below1 backlash and shared damage flags need an exact ruling.
5. Crown's Burn: total numeric actual fire damage (temp absorption+actualHP), divide among up to3 chosen recipients, floor when? Roll S d6+M shared or independently per ally? Zero selected recipients must not divide by0. Is min1 triggered by positive packet or positive numeric total when HP floors yield actual0? Shared-roll damage/healing abilities and explicit copy-half amounts need consistent copied quantity/dieCount provenance.
6. Monk maximum-HP reductions choose strongest among source Monk effects; state clamp and percentage thresholds must be distinct from damage/healing. Confirm applying/restoring maximum does not generate damage/healing/Wounds, and name global multi-source composition dependency. Veinburst Requiem's post-damage 'falls to0' threshold is an additional explicit state effect: does it open a new Wound save or only dying/death rules? A floor cannot be guessed to stop non-damage state loss.
7. Paladin redirection engine[10] says split 'actual damage' AFTER original defenses, then no receiving mitigation, whereas Bloodbond says pre-mitigation split and each recipient defenses. Newly reviewed actualDamageDealt is a POST-HP/temp numeric-drain measure and should not accidentally be reused before redirection. Please keep these source-specific procedures distinct and identify a dedicated redirection sequence packet if needed; don't claim it closed from healing classifications.
8. Tinker destroyed-drone reconstruction and functional-device repair are distinct; support mode/Restoration Field are explicit organic-healing exceptions. Druid temp buffer spends finite reserve but Combat Shapeshifting heals realHP. Mirrorsage copies/converted Mend and finite healing, Wizard added healing dice, Shaman flask stock and limited refunds need exact type/provenance/cadence dispositions rather than a universal 'all copies never trigger anything' beyond their actual source flags.


## cleric.base.sacred-chant

{"name": "Sacred Chant", "activation": "Action", "cost": "1 RP to start; 0 RP maintenance", "rangeAndTarget": "Self; audible 15-foot prayer aura", "duration": "Concentration, maximum 3 Cleric turns", "frequency": "At will while RP remains", "effect": "Sacred Chant. Tags: chant, sustained, conviction. Pulse on start and once when maintained on each later regular turn with a Bonus Action. Under the base feature, the third pulse generates 1 Conviction. Only a real encounter can generate Conviction this way. Maintenance itself does not otherwise heal, damage or grant Conviction.", "prerequisite": null}

## cleric.arch.miraculous-channel

{"name": "Miraculous Channel", "activation": "Bonus Action", "cost": "3 Conviction", "rangeAndTarget": "Your next ally-targeting Rite this turn", "duration": "Until end of current turn", "frequency": "At will while Conviction remains", "effect": "Miraculous Channel. Tags: rite, channel, bishop. Your next Rite this turn that normally affects one or more willing allies may affect up to six legal willing allies within the Rite's normal range instead. Roll shared healing or numeric effects once and apply normally. It does not multiply hostile targets, corpse targets or resource generation.", "prerequisite": null}

## cleric.arch.divine-invocation

{"name": "Divine Invocation", "activation": "Action", "cost": "2 Conviction + 3 RP", "rangeAndTarget": "Mode-dependent; maximum 60 feet", "duration": "Instantaneous unless mode states otherwise", "frequency": "Recharge 3 rounds", "effect": "Divine Invocation. Tags: invocation, bishop. Use only your selected Invocation Path. Radiance: up to 3 allies within 30 feet each regain S d8+M HP; one may end Frightened or Poisoned. Judgment: one enemy within 60 feet makes a Wisdom save, taking (S+1)d8 radiant on failure or half on success; failure also applies Judged for 2 rounds. Renewal: up to 2 allies within 30 feet each regain S d8+M HP and 5 Stamina. Flame: creatures in a 15-foot cone make Dexterity saves, taking (S+1)d8 fire on failure or half on success; failed targets also take 1d6 fire at the start of their next turn. Veil: up to 3 allies within 30 feet can see invisible/ethereal creatures within 30 feet and gain advantage on saves against illusions for 3 rounds. Echoes: choose one eligible Smite or Rite you resolved this turn or previous regular turn and one original target within 30 feet; repeat 50% of its immediate unmodified rolled damage or healing dice, rounded down once, minimum 1 for a positive source, with no copied conditions, resources or triggers.", "prerequisite": null}

## cleric.hero.saint.radiant-burst

{"name": "Radiant Burst", "activation": "Action", "cost": "6 RP", "rangeAndTarget": "15-foot radius centered on you; up to six allies and six Undead/Fiends", "duration": "Instantaneous", "frequency": "Recharge 4 rounds", "effect": "Radiant Burst. Tags: saint, healing, radiant. Roll S d8 once. Each chosen living ally regains that roll + M HP. Each chosen Undead or Fiend makes a Wisdom save, taking the same S d8 roll as radiant damage on failure or half on success. Healing and damage are separate applications of the shared roll.", "prerequisite": null}

## cleric.hero.priest.scriptural-echo

{"name": "Scriptural Echo", "activation": "Triggered", "cost": "0", "rangeAndTarget": "One legal original target of your previously used Divine Invocation", "duration": "Instantaneous", "frequency": "1/short rest", "effect": "Scriptural Echo. Tags: priest, rite, invocation. When you start a Rite, you may repeat 50% of the immediate rolled damage or healing dice from the most recent Divine Invocation you personally resolved since the end of your previous regular turn. Round down once, minimum 1 for a positive source. It copies no conditions, movement, resource effects, control or Invocation Path triggers.", "prerequisite": null}

## cleric.hero.priest.balanced-scales

{"name": "Balanced Scales", "activation": "Passive", "cost": "0", "rangeAndTarget": "Living creatures healed by your Cleric features", "duration": "Until start of your next regular turn", "frequency": "At most once per marked ally per round", "effect": "Balanced Scales. Tags: priest, healing, retaliation. After you restore HP to a living ally, mark it until the start of your next regular turn. The first enemy to damage that ally during the mark takes S + M radiant damage. The retaliation is not an attack, cannot critically hit and cannot recursively trigger another Balanced Scales event.", "prerequisite": null}

## cleric.hero.priest.balance-restoration

{"name": "Balance Restoration", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "15-foot-radius area centered at a point within 30 feet", "duration": "Instantaneous", "frequency": "Recharge 3 rounds", "effect": "Balance Restoration. Tags: priest, healing, radiant. Choose up to three living allies and three enemies in the area. Roll S d8 once. Each ally regains the roll + M HP. Each enemy makes a Wisdom save, taking the same S d8 roll as radiant damage on failure or half on success.", "prerequisite": null}

## cleric.hero.priest.word-of-power

{"name": "Word of Power", "activation": "Action", "cost": "4 RP", "rangeAndTarget": "One creature within 30 feet", "duration": "Instantaneous", "frequency": "Recharge 2 rounds", "effect": "Word of Power. Tags: priest, divine. Choose one mode. Mercy: one willing living creature regains S d8+M HP. Rebuke: one Undead or Fiend makes a Constitution save, taking (S+1)d8 radiant on failure or half on success; failure also removes its Reaction until the start of its next turn. Command: one other hostile creature makes a Wisdom save; failure knocks it Prone and removes its Reaction until the start of its next turn. No mode changes beliefs, loyalty or ideology.", "prerequisite": null}

## cleric.hero.cultist.zealot-s-touch

{"name": "Zealot's Touch", "activation": "Passive", "cost": "0", "rangeAndTarget": "Healing-over-time Rites you control", "duration": "Passive", "frequency": "Always", "effect": "Zealot's Touch. Tags: cultist, rite, necrotic. When starting a Rite whose printed pulse would restore HP over multiple turns, you may designate a hostile creature instead of a healing recipient. At each applicable pulse that enemy makes a Wisdom save. On failure it takes necrotic damage equal to the Rite's rolled healing dice; on success it takes half. Flat healing bonuses are not converted. The enemy receives no healing.", "prerequisite": null}

## cleric.hero.cultist.dark-sacrament

{"name": "Dark Sacrament", "activation": "Action", "cost": "3 Conviction + 5 RP to start; 1 RP maintenance", "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet", "duration": "Concentration, maximum 3 Cleric turns", "frequency": "Recharge 4 rounds", "effect": "Dark Sacrament. Tags: cultist, sacrament, rite, sustained, zone. On start and each paid maintenance pulse, roll S d6 once. Up to three enemies in the zone make Constitution saves, taking that roll as necrotic damage on failure or half on success. If at least one enemy takes damage, up to three living allies in the zone each regain floor(roll/2)+M HP. Maximum 3 pulses. The Conviction expenditure can vent Dissonance once.", "prerequisite": null}

## crimson-agent.engine[2]

Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation.

## crimson-agent.engine[5]

The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds.

## crimson-agent.arch.bloodbound-edge

{"name": "Bloodbound Edge", "activation": "Action", "cost": "3 BG; 1 short-rest use", "rangeAndTarget": "Up to 3 enemies with your Bleed within 30 ft", "duration": "Instant", "frequency": "1/short rest", "effect": "End up to 2 of your Bleed instances per target. Each takes 1d4 per remaining tick, maximum S d4 per creature, ignoring resistance but respecting immunity. This replaces their future ticks and grants no BG, healing or kill-trigger benefit.", "prerequisite": null}

## crimson-agent.hero.bloodweaver.bloodbond

{"name": "Bloodbond", "activation": "Bonus Action", "cost": "2 RP", "rangeAndTarget": "One willing ally within 30 ft", "duration": "Concentration, 3 of your turns", "frequency": "Recharge 3", "effect": "Create Bloodbond while both remain within 30 ft. When ally takes damage, you may use Reaction to redirect floor(one-quarter of pre-mitigation damage) to yourself; each recipient applies its own defenses once. Once/round when a paid technique heals you, ally gains M temporary HP. No recursive transfers.", "prerequisite": null}

## crimson-agent.hero.bloodweaver.crimson-pact

{"name": "Crimson Pact", "activation": "Action", "cost": "5 BG; 1 long-rest use", "rangeAndTarget": "Up to 3 bleeding enemies and 6 living allies within 30 ft", "duration": "Instant; shields 1 minute", "frequency": "1/long rest", "effect": "End your Bleeds on chosen enemies; each makes CON save against 4d8 necrotic, half on success. Each chosen ally regains 4d8+M HP and gains 10 temporary HP. Use one shared roll per damage/healing effect; healing does not multiply by enemies or remaining ticks.", "prerequisite": null}

## crimson-agent.hero.bloodweaver.purify-blood

{"name": "Purify Blood", "activation": "Action", "cost": "4 RP", "rangeAndTarget": "One willing living creature touched", "duration": "Instant", "frequency": "Recharge 3", "effect": "End Poisoned and one nonmagical disease. Magical disease needs a successful INT ability check against its stated treatment DC, or DC 15 if absent; failure spends the cost. No curse, Wound, death or Corruption removal.", "prerequisite": null}

## crimson-agent.hero.bloodweaver.lifewell

{"name": "Lifewell", "activation": "Action", "cost": "4 RP; all BG, minimum 3", "rangeAndTarget": "Up to 3 living allies within 15 ft", "duration": "Concentration, 3 of your turns", "frequency": "1/long rest", "effect": "Spend K BG. At start and on each of your next 2 turns, use Bonus Action and pay 1 RP to pulse healing: each chosen ally still within 15 ft regains 1d8+K HP. Without maintenance it ends at turn end. Total 3 pulses; no triggers create more BG.", "prerequisite": null}

## crimson-agent.hero.thirstborn.veinburst-requiem

{"name": "Veinburst Requiem", "activation": "Action", "cost": "All BG, minimum 3; 1 long-rest use", "rangeAndTarget": "Up to 6 enemies with your Bleed within 30 ft", "duration": "Instant", "frequency": "1/long rest", "effect": "Spend K BG and end your Bleeds on targets. CON save: (S+K)d8 necrotic, half on success. A target failing by 10 with remaining HP no greater than your class level falls to 0; ordinary death rules follow. No percentage-based automatic boss execution or BG refund.", "prerequisite": null}

## crimson-agent.hero.thirstborn.crimson-harvest

{"name": "Crimson Harvest", "activation": "Action", "cost": "2 BG; 1 short-rest use", "rangeAndTarget": "One enemy in weapon reach at half HP or less", "duration": "Instant", "frequency": "1/short rest", "effect": "Make one weapon attack; on hit add S d8 damage. If this reduces it to 0, regain S+M HP and 1 BG within gain cap. No instant kill from a percentage threshold; summoned/allied/helpless creatures yield no recovery.", "prerequisite": null}

## dragoon.engine[4]

Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard.

## dragoon.base.wyvern-s-guard

{"name": "Wyvern's Guard", "activation": "Bonus Action", "cost": "1 Momentum", "rangeAndTarget": "Self", "duration": "Until start next turn", "frequency": "Recharge 2", "effect": "The next attack that damages you has damage reduced by S d6+M, minimum 0; then the guard ends. Roll the reduction only when damage occurs. This reduction cannot heal or reflect damage.", "prerequisite": null}

## dragoon.hero.dragon-guardian.draconic-ward

{"name": "Draconic Ward", "activation": "Action", "cost": "3 Momentum", "rangeAndTarget": "Self and up to 3 allies within 10 ft", "duration": "Concentration, 3 of your turns", "frequency": "Recharge 4", "effect": "Project a ward: chosen creatures while within 10 ft reduce damage by S, minimum 0. The reduction does not stack with Wyrmhide or another flat class reduction. No passive healing or extra Actions.", "prerequisite": null}

## druid.engine[4]

Transformation reserves prevent unlimited replacement HP: at long rest record Buffer Reserve=2 L+M and Form Surge Reserve=PB. A form giving temporary HP draws that many from Buffer Reserve, up to remaining amount, with normal nonstacking; never real healing. A form special described once/transformation also spends 1 Form Surge and cannot be refreshed by resuming the form. Form Surge refills only long rest. Forms cannot grant free casts, RP or shift uses. Auras affect at most 3 enemies and once per enemy per round; retaliation once/round total; ongoing riders refresh, never stack. Entering a legal Shapeshift clears the Refrain counter and remembered repeated-spell name, as the protected source contract requires. It does not reduce accumulated Dissonance. Natural attacks do not clear Refrain.

## druid.base.moon.combat-shapeshifting

{"name": "Combat Shapeshifting", "activation": "Bonus Action", "cost": "1 to S RP", "rangeAndTarget": "Moon Circle self in form", "duration": "Instant", "frequency": "Once/own turn", "effect": "Restore 1d8 real HP per RP paid, never beyond maximum. Does not restore temporary buffer or shift uses. No Dissonance as class technique; cannot heal after form ended/incapacitated.", "prerequisite": null}

## mirrorsage.base.echo-channeling

{"name": "Echo Channeling", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your own Echo Release", "duration": "Instant", "frequency": "Once/short rest", "effect": "After releasing an Echo, add M to one target's damage or healing. No modifier to resource effects; this upgrade does not grant another release or repeat the source's rider.", "prerequisite": null}

## mirrorsage.arch.advanced-mirrorcall

{"name": "Advanced Mirrorcall", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your Mirror Beast", "duration": "While summoned", "frequency": "Once/encounter", "effect": "You may change Beast appearance to another stored source as a Bonus Action without resummoning or restoring HP. It gains either+10 ft swim or climb Speed until it ends. No new release, attack or capture.", "prerequisite": null}

## mirrorsage.arch.dual-echo-cast

{"name": "Dual Echo Cast", "activation": "Action", "cost": "RP for each of 2 Echoes; consume both", "rangeAndTarget": "One target per eligible profile", "duration": "Immediate; riders at most 1 turn", "frequency": "Recharge 3", "effect": "Release two records captured from different creatures as ONE combined release. Each deals/heals half its profile's rolled amount, round once per component. At most one Hindrance rider; no duplicated resources or additional release this round.", "prerequisite": null}

## mirrorsage.arch.mimicry-focus

{"name": "Mimicry Focus", "activation": "Passive", "cost": "0", "rangeAndTarget": "Self", "duration": "Encounter", "frequency": "Once/encounter", "effect": "At genuine encounter start gain 1 Focus Point, cap 1; any previous point is replaced. Spend on Focus Channel or pay 1 Focus during a release to add 1d6 to one damage/healing target. No point generation from staged combat.", "prerequisite": null}

## mirrorsage.arch.echo-fusion

{"name": "Echo Fusion", "activation": "Action", "cost": "RP for 2 Echoes; consume both", "rangeAndTarget": "Up to 2 profile targets within 30 ft", "duration": "Instant or 1 turn", "frequency": "Recharge 3", "effect": "Choose two stored profiles. Resolve one at full dice and the other at half dice to one target each. Only one may be healing; at most one Hindrance rider. Counts as one combined release and cannot receive Dual Echo Cast simultaneously.", "prerequisite": null}

## mirrorsage.arch.mirror-shift

{"name": "Mirror Shift", "activation": "Bonus Action", "cost": "1 RP", "rangeAndTarget": "Your Mirror Beast within 60 ft", "duration": "Remaining summon duration", "frequency": "Recharge 2", "effect": "Switch its appearance to a stored source and choose swim 30 ft or climb 30 ft until next shift. Restore no HP or attacks; no flight, incorporeality or copied creature special actions. Does not release or consume the Echo.", "prerequisite": null}

## mirrorsage.arch.focus-channel

{"name": "Focus Channel", "activation": "Bonus Action", "cost": "1 Focus", "rangeAndTarget": "Self; next release this turn", "duration": "This turn", "frequency": "Once/encounter via Focus cap", "effect": "Next Echo release adds 1d6 to one damage/healing amount OR adds 30 ft range, chosen now. Cannot multiply duration, bypass concentration, add targets or override release caps. If no release occurs this turn the point remains spent.", "prerequisite": null}

## mirrorsage.hero.light-weaver.blessed-copy

{"name": "Blessed Copy", "activation": "Passive", "cost": "1 additional RP", "rangeAndTarget": "Second living ally within 15 ft of original Mend/Ward target", "duration": "Same healing/shield duration", "frequency": "Once/round", "effect": "When releasing Mend or Ward, pay 1 extra RP to give a second ally half the rolled amount, rounded once. This is within the same release, no new source or healing proc. No duplication of concentration or resources.", "prerequisite": null}

## mirrorsage.hero.light-weaver.radiant-mirror-beast

{"name": "Radiant Mirror Beast", "activation": "Action", "cost": "4 RP", "rangeAndTarget": "Empty space within 15 ft", "duration": "Concentration, 3 of your turns", "frequency": "Recharge 4", "effect": "Summon radiant standard Beast. Bonus Action command chooses normal attack or healing S d4 to one living ally within 5 ft, paying 1 RP per heal. It may instead originate your paid Echo release under common limits. Cannot perform two options in one round.", "prerequisite": null}

## mirrorsage.hero.light-weaver.blessing-echo

{"name": "Blessing Echo", "activation": "Action", "cost": "Recorded RP cost+1; consume offensive Echo", "rangeAndTarget": "One living ally within 30 ft", "duration": "Instant or 1 minute shield", "frequency": "Recharge 3", "effect": "Convert a stored Strike/Burst record to Mend/Ward for this release, chosen on activation; heal S d6+M or grant same temporary HP. This explicit conversion cannot also deal offensive damage or copy a condition.", "prerequisite": null}

## mirrorsage.hero.light-weaver.purifying-reflection

{"name": "Purifying Reflection", "activation": "Reaction", "cost": "5 RP; 1 long-rest use", "rangeAndTarget": "Ally within 30 ft failing save against Charmed/Frightened/Poisoned", "duration": "Instant", "frequency": "1/long rest", "effect": "Ally rerolls that save with advantage; use new result. If it succeeds, it regains S d6 HP. No arbitrary curse or death reversal; costs remain if it fails. This is not a captured Echo and creates no record.", "prerequisite": null}

## mirrorsage.hero.mirror-mage.mirror-double

{"name": "Mirror Double", "activation": "Bonus Action", "cost": "2 RP", "rangeAndTarget": "One damage Echo you released this turn", "duration": "Resolves start next turn", "frequency": "Recharge 3", "effect": "Create one illusory double; it repeats half the unmodified immediate damage dice to one original enemy still within 30 ft, without roll or conditions. Declare Mirror Double before the current turn ends; its pending copy remains part of this turn’s one release package and does not consume a later release allowance. Only one pending copy; cannot copy copies/healing.", "prerequisite": null}

## mirrorsage.hero.mirror-mage.reality-fracture

{"name": "Reality Fracture", "activation": "Action", "cost": "6 RP; 1 long-rest use", "rangeAndTarget": "Fixed 10 ft-radius zone within 30 ft", "duration": "Concentration, 3 of your turns", "frequency": "1/long rest", "effect": "While you stand inside, once/turn add 1d6 to one Echo damage/healing amount or impose-1 on one target's Echo save. Choose before resolving. No free releases, random recasts, resource refunds or extra targets.", "prerequisite": null}

## mirrorsage.hero.shattered-one.fractured-dominion

{"name": "Fractured Dominion", "activation": "Bonus Action", "cost": "8 RP; 1 long-rest use", "rangeAndTarget": "Self", "duration": "2 of your turns", "frequency": "1/long rest", "effect": "Your first damage release on each of these 2 turns adds one half-dice component against a DIFFERENT enemy within 10 ft of an original target. Same package and shared copy cap; excludes healing/control. Never recursively copies a copy or adds a release action.", "prerequisite": null}

## monk.engine[1]

Ki Chain is a Monk-only resource from 0 to 5. Begin each real encounter at 0 Ki and clear Ki when the encounter ends or after 1 minute without a real encounter. Ki cannot be generated by sparring with willing creatures, attacking objects, repeatedly dodging harmless attacks, healing between encounters or other staged actions. Ki is separate from Resonance Points and Dissonance.

## monk.engine[5]

Tiger, Tortoise and Crane Ki generation obey the global Ki-gain ceilings. Tiger can generate Ki from critical unarmed strikes. Tortoise can generate Ki from specified defensive successes. Crane provides mobility and support but does not create free out-of-combat healing. A single event can satisfy more than one generator, but total gain still cannot exceed the appropriate own-turn or off-turn ceiling.

## monk.engine[9]

Temporary maximum-HP reductions caused by Monk features do not stack on the same creature; use the largest reduction from your Monk features. Maximum HP cannot be reduced below 1. Unless a card specifies an earlier end, the reduction lasts until the creature completes a short or long rest. Restoring maximum HP does not restore current HP. These effects are temporary combat trauma, not unstated permanent injuries.

## monk.arch.martial-apex-capstone

{"name": "Martial Apex (Capstone)", "activation": "Triggered", "cost": "Spend all 5 Ki", "rangeAndTarget": "One Monk Action technique you are beginning to use", "duration": "For that technique", "frequency": "1/encounter; automatic Arch capstone", "effect": "Martial Apex. Tags: arch, capstone, action. When at exactly 5 Ki, spend all 5 as you begin a Monk technique that normally requires an Action. That technique does not consume your normal Action but counts as the one additional full Action allowed to you that round. Add one additional copy of its base rolled damage dice to one damage roll. It cannot be used on healing-only techniques or a Hero Final. Spending all 5 Ki replaces only that technique's printed Ki cost; any RP, rest-use, target and recharge requirements are still paid/met. The bonus dice apply to one target only, cannot copy critical bonus dice, and cannot generate further attacks or resources.", "prerequisite": null}

## monk.hero.iron-fist-master.ribcrusher-strike

{"name": "Ribcrusher Strike", "activation": "Triggered", "cost": "2 Ki", "rangeAndTarget": "One creature hit by your unarmed strike", "duration": "Until target completes a short or long rest", "frequency": "Once per target per encounter", "effect": "Ribcrusher Strike. Tags: hero, iron-fist, attack, max-hp. After an unarmed strike hits, spend 2 Ki. The target makes a Constitution save. On failure reduce its maximum HP by S+M, minimum maximum HP 1. This reduction follows the common non-stacking maximum-HP rule and is restored after a completed short or long rest without restoring current HP.", "prerequisite": null}

## monk.hero.iron-fist-master.bone-breaking-strike

{"name": "Bone-Breaking Strike", "activation": "Action", "cost": "2 Ki", "rangeAndTarget": "One creature within unarmed reach", "duration": "Until target completes a short or long rest", "frequency": "Recharge 3 rounds", "effect": "Bone-Breaking Strike. Tags: hero, iron-fist, attack, max-hp. Make one unarmed strike. On a hit, the target makes a Constitution save. On failure reduce its maximum HP by 2 S+M under the common non-stacking maximum-HP rule. This creates no persistent broken-limb injury; the maximum returns after a completed short or long rest without restoring current HP.", "prerequisite": null}

## monk.hero.way-of-shadow.deathless-silence

{"name": "Deathless Silence", "activation": "Action", "cost": "5 Ki + 5 RP", "rangeAndTarget": "Up to three enemies you can perceive within 60 feet", "duration": "Until start of your next regular turn; max-HP reduction until rest", "frequency": "1/long rest; automatic Hero Final", "effect": "Final — Deathless Silence. Tags: hero, shadow, final, teleportation, max-hp, weave. Until the start of your next regular turn you cannot be targeted by opportunity attacks or Reactions. Teleport adjacent to up to three different chosen enemies in sequence and make one unarmed strike against each. On each hit, the target makes a Constitution save. Failure reduces its maximum HP by 4 S+M under the common non-stacking rule and suppresses one non-core defensive passive it possesses until the end of its next turn; the Director identifies an applicable visible passive before the save. This does not disable core class engines, legendary rules or creature type traits.", "prerequisite": null}

## monk.hero.way-of-shadow.death-touch

{"name": "Death Touch", "activation": "Action", "cost": "5 Ki", "rangeAndTarget": "One creature within unarmed reach", "duration": "Instantaneous", "frequency": "1/long rest", "effect": "Death Touch. Tags: hero, shadow, attack, finisher. Make one unarmed strike. On a hit add 3 S d8 necrotic damage. If the target began the strike at or below one-quarter maximum HP, it also makes a Constitution save; on failure add another 2 S d8 necrotic damage. This never causes automatic death, bypasses no ordinary dying rules and creates no permanent injury beyond the damage actually dealt.", "prerequisite": null}

## oracle.engine[6]

RC RECOVERY. A completed long rest restores RC to maximum. A completed short rest restores 1 spent RC, never above maximum. Each Mystery has exactly one Prophecy Trigger. During a real encounter, your Prophecy Trigger can restore at most 1 RC per round and never above maximum. Trivial enemies, willing staged targets, summoned sacrifices, repeated corpse abuse, copied damage, copied healing and events generated solely to trigger recovery do not qualify.

## oracle.engine[14]

Copied, echoed, repeated or redirected damage/healing uses only the explicitly copied numeric component. It cannot repeat RC recovery, Prophecy Triggers, action grants, conditions, passive triggers, resource restoration or another copy effect unless the copying feature explicitly says otherwise.

## oracle.engine[26]

Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones.

## oracle.supplement.shared.mystery-surge

{"name": "Mystery Surge", "activation": "Triggered", "cost": "0", "rangeAndTarget": "One Tier II Revelation you are activating", "duration": "For that use", "frequency": "1/short rest", "effect": "When you activate a known Tier II Revelation, choose one applicable surge: increase its Revelation attack roll or save DC by 1 for that use; add S to one rolled damage or healing result; or increase one printed non-concentration duration of 1-2 rounds by 1 round. A Surge cannot create additional Actions, targets, RC recovery or hard-control repetitions.", "prerequisite": "Oracle 6 and a known Tier II Revelation"}

## oracle.supplement.burning-blood.burning-blood-boon-v

{"name": "Burning Blood — Boon V", "activation": "Bonus Action", "cost": "0", "rangeAndTarget": "Self; up to three enemies/allies within 15 feet", "duration": "Three rounds", "frequency": "1/long rest; one pulse/target/round", "effect": "1/long rest as a Bonus Action become a living pyre for 3 rounds. At the start of each hostile creature's turn within 15 feet it takes S d6 fire damage. Once per your turn when at least one enemy takes fire damage from you, regain 1d6 HP, capped at S+M HP per turn. Allies in the aura gain fire resistance and hidden/invisible creatures within 10 feet cannot benefit from mundane darkness or visual concealment against creatures illuminated by your pyre.", "prerequisite": "Oracle 20; selected Curse:Burning Blood"}

## oracle.supplement.consumed.consumed-boon-v

{"name": "Consumed — Boon V", "activation": "Bonus Action", "cost": "0", "rangeAndTarget": "Self and up to three allies within 10 feet", "duration": "Three rounds", "frequency": "1/long rest", "effect": "1/long rest as a Bonus Action fully embody your Mystery for 3 rounds. Gain immunity to the theme damage type, +2 on Revelation attack rolls and Revelation save DC, and add S to one Revelation damage or healing roll each turn. Allies within 10 feet gain +1 AC. Visible transformation cannot be suppressed during this embodiment.", "prerequisite": "Oracle 20; selected Curse:Consumed"}

## oracle.supplement.battle.host-s-cry

{"name": "Host's Cry", "activation": "Action", "cost": "1 RC", "rangeAndTarget": "Allies within 4 tiles", "duration": "2 rounds", "frequency": "At will while RC remains", "effect": "Allies in range gain +S damage on one weapon hit per turn and reduce the first damage they take each round by 1. Once during this Cry, when a qualifying ally reduces a meaningful hostile creature to 0 HP, that ally regains 1d6 HP and you regain 1 RC, never above maximum. This special refund can occur only once per Host's Cry and still obeys the once-per-round RC recovery ceiling.", "prerequisite": "Oracle 3; Mystery: Battle; selected Tier I Revelation"}

## oracle.supplement.battle.fury-of-the-host

{"name": "Fury of the Host", "activation": "Action", "cost": "3 RC", "rangeAndTarget": "Self and allies within 5 tiles", "duration": "2 rounds; Revelation backlash 1 round", "frequency": "At will while RC remains", "effect": "For 2 rounds, each ally in range may once on its regular turn gain one additional full Action usable only for one ordinary weapon attack or Dash/Move, subject to the universal extra-Action cap. Allies also gain +1 on attack rolls and reduce the first damage they take each round by 1. You gain +2 AC and immunity to Frightened. Once per round you may activate one known Tier I Battle Revelation for 0 RC using its normal action type. The first qualifying ally each round to reduce a meaningful enemy to 0 HP regains 1d6 HP. When the effect ends, you are suffering Revelation backlash until the end of your next turn: -1 on attacks and saves and Speed -5 feet. Concentration is required; choose at most three allies for its benefits. Each granted Action may make only one ordinary weapon attack or Dash, and cannot grant another action.", "prerequisite": "Oracle 9; Mystery: Battle"}

## oracle.supplement.bones.death-s-threshold

{"name": "Death's Threshold", "activation": "Passive", "cost": "0 RC", "rangeAndTarget": "Self; undead enemies within 3 tiles", "duration": "Until healed above half maximum HP", "frequency": "1/short rest", "effect": "The first time after a short rest that you fall to one-quarter maximum HP or less, activate Death's Threshold. Until you are healed above half maximum HP, reduce the first necrotic damage and first nonmagical weapon damage you take each round by S and gain +1 to your Revelation save DC. Undead enemies within 3 tiles take -1 on their first attack roll against you each round. The effect then ends and cannot reactivate until after another short rest.", "prerequisite": "Oracle 6; Mystery: Bones; selected Tier II Revelation"}

## oracle.supplement.bones.ledger-s-memory

{"name": "Ledger's Memory", "activation": "Passive and Action", "cost": "0 RC", "rangeAndTarget": "Self; one corpse touched", "duration": "Permanent; consultation instantaneous", "frequency": "Knowledge always; corpse reading 1/long rest", "effect": "Gain advantage on checks to identify undead, poison and disease. Once per long rest, touch one corpse and learn its identity if the Pale Ledger could reasonably know it, its approximate time of death and the direct physical or magical cause of death. This does not reveal the killer's identity unless the corpse or supernatural Ledger actually knows it.", "prerequisite": "Oracle 12; Mystery: Bones"}

## oracle.supplement.bones.bones-revelation-mastery

{"name": "Bones Revelation Mastery", "activation": "Passive", "cost": "0 RC", "rangeAndTarget": "One eligible known Bones Revelation", "duration": "Permanent", "frequency": "Choose one upgrade at Oracle 15", "effect": "Choose one mastery for a Revelation you know. Enhanced Marrow Drain: a living target hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Ledger's Command: may target up to 3 undead, but all controlled undead still share one Bonus Action command per round. Enhanced Unfinished Chorus: when its drain resolves, you may always redirect the healing to one ally within 3 tiles of you rather than yourself; its healing cap remains S+M.", "prerequisite": "Oracle 15; Mystery: Bones; Revelation Mastery"}

## oracle.supplement.flame.flame-prophecy-trigger

{"name": "Flame Prophecy Trigger", "activation": "Triggered", "cost": "0 RC", "rangeAndTarget": "Self", "duration": "Instantaneous", "frequency": "At most once per round during a real encounter", "effect": "When one of your Revelations restores HP to a living ally or deals fire damage to a meaningful hostile creature, regain 1 RC, never above maximum. One Revelation use can restore at most 1 RC even if it both heals and burns or affects multiple targets.", "prerequisite": "Oracle 1; Mystery: Flame"}

## oracle.supplement.flame.wrathful-brand

{"name": "Wrathful Brand", "activation": "Bonus Action", "cost": "1 RC", "rangeAndTarget": "One enemy within 4 tiles", "duration": "Until end of your next regular turn", "frequency": "At will while RC remains; one Brand at a time", "effect": "Mark one enemy. The next damaging attack you hit it with before the Brand ends adds fire damage equal to half that attack's unmodified rolled base damage dice total, rounded down, minimum 1. If an ally damages the marked target before the Brand ends, that ally regains 1d6 HP once per Brand and the target makes a Wisdom save; on failure it has -1 on attack rolls until the end of its next turn.", "prerequisite": "Oracle 3; Mystery: Flame; selected Tier I Revelation"}

## oracle.supplement.flame.purging-flame

{"name": "Purging Flame", "activation": "Action", "cost": "1 RC", "rangeAndTarget": "One creature you touch", "duration": "Instantaneous; attack penalty until end of undead target's next turn", "frequency": "At will while RC remains", "effect": "If the target is a living ally, it regains 1d8+M HP and may end Poisoned or immediately repeat one saving throw against a disease that normally permits saves. This removes no Wounds. If the target is undead, make a Revelation attack; on hit it takes 1d8+M fire damage and makes a Constitution save, suffering -1 on attack rolls until the end of its next turn on failure.", "prerequisite": "Oracle 3; Mystery: Flame; selected Tier I Revelation"}

## oracle.supplement.flame.crown-s-burn

{"name": "Crown's Burn", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "3-tile-radius burst centered within 4 tiles", "duration": "Damage/healing instantaneous; penalties until end of next turn", "frequency": "At will while RC remains", "effect": "Enemies in the burst make Dexterity saves, taking 2d6+M fire damage on failure or half on success. A failing enemy also has -1 on attack rolls until the end of its next turn. Total the actual fire damage dealt to meaningful hostile creatures, then divide by the number of allied recipients chosen in the burst; up to three living allies in the burst each regain the lesser of that share or S d6+M HP, minimum 1 if any qualifying damage was dealt. Each healed ally reduces the first fire damage it takes before your next turn by S.", "prerequisite": "Oracle 6; Mystery: Flame; selected Tier II Revelation"}

## oracle.supplement.flame.zealot-s-renewal

{"name": "Zealot's Renewal", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "One living ally within 3 tiles; adjacent enemies", "duration": "Instantaneous; fire ward until start of your next turn", "frequency": "At will while RC remains", "effect": "The ally regains 2 S d8+M HP, then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it. It may end Poisoned or immediately repeat one disease save. Until the start of your next turn it reduces the first fire damage it takes by S. Hostile creatures adjacent to the healed ally take 1d4 fire damage once from scattering embers.", "prerequisite": "Oracle 6; Mystery: Flame; selected Tier II Revelation"}

## oracle.supplement.flame.first-flame-convergence

{"name": "First Flame Convergence", "activation": "Action", "cost": "3 RC", "rangeAndTarget": "Self and allies within 4 tiles", "duration": "2 rounds", "frequency": "At will while RC remains", "effect": "For 2 rounds, once on each of your turns when a Flame Revelation deals fire damage, add one extra die matching that Revelation's primary damage die to one damage roll. Once per turn when one of your Flame Revelations damages a meaningful hostile creature, one living ally within 4 tiles regains 1d6 HP. Allies within 4 tiles are immune to Frightened. Once per turn when this effect heals an ally, that ally reduces the first damage it takes before your next turn by 1. Zealot's Renewal deals no backlash while Convergence lasts.", "prerequisite": "Oracle 9; Mystery: Flame"}

## oracle.supplement.flame.flame-revelation-mastery

{"name": "Flame Revelation Mastery", "activation": "Passive", "cost": "0 RC", "rangeAndTarget": "One eligible known Flame Revelation", "duration": "Permanent", "frequency": "Choose one upgrade at Oracle 15", "effect": "Choose one mastery for a Revelation you know. Enhanced Wrathful Brand: its maximum duration becomes 2 rounds. Enhanced Crown's Burn: its healing may target up to three living allies within 4 tiles of the burst center rather than requiring them inside the burst. Enhanced First Flame Convergence: Zealot's Renewal backlash remains suppressed for the full Convergence duration; if already suppressed by the base effect, additionally one ally healed by Zealot's Renewal during Convergence gains S temporary HP.", "prerequisite": "Oracle 15; Mystery: Flame; Revelation Mastery"}

## oracle.supplement.flame.flame-prophecy

{"name": "Flame Prophecy", "activation": "Triggered", "cost": "0 RC for chosen Revelation", "rangeAndTarget": "One known Flame Revelation; allies within 4 tiles", "duration": "Chosen Revelation; secondary effects until end of your next turn", "frequency": "1/long rest", "effect": "Activate one known Flame Revelation for 0 RC. Until the end of your next regular turn, the next Zealot's Renewal or other Flame Revelation you use that has self-damaging healing backlash ignores that backlash, and allies within 4 tiles reduce the first fire damage they take by S. The next time you damage a creature already suffering ongoing fire damage before the effect ends, add S fire damage once.", "prerequisite": "Oracle 18; Mystery: Flame"}

## oracle.supplement.flame.crown-restored

{"name": "Crown Restored", "activation": "Bonus Action", "cost": "0 RC", "rangeAndTarget": "Self and allies within 5 tiles", "duration": "3 rounds", "frequency": "1/long rest", "effect": "Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap.", "prerequisite": "Oracle 20; Mystery: Flame"}

## oracle.supplement.life.resonant-seed

{"name": "Resonant Seed", "activation": "Action", "cost": "1 RC", "rangeAndTarget": "2-tile-radius fixed zone centered within 4 tiles", "duration": "3 rounds", "frequency": "At will while RC remains; one Seed zone at a time", "effect": "When a living ally starts its turn in the zone, it regains 1d4 HP, at most once per round and for at most three pulses from this use, and may end Frightened or Poisoned on the first pulse it receives. Undead entering or starting their turn in the zone take 1d4 radiant damage once per round and make a Strength save; on failure their Speed is reduced by 1 tile until the end of that turn. Healing requires the paid 1 RC activation and ends after 3 rounds.", "prerequisite": "Oracle 3; Mystery: Life; selected Tier I Revelation"}

## oracle.supplement.life.life-revelation-mastery

{"name": "Life Revelation Mastery", "activation": "Passive", "cost": "0 RC", "rangeAndTarget": "One eligible known Life Revelation", "duration": "Permanent", "frequency": "Choose one upgrade at Oracle 15", "effect": "Choose one mastery for a Revelation you know. Enhanced Overflowing Light: maximum temporary HP from excess healing becomes 20. Enhanced Garden of Restoration: the first Garden pulse a creature receives may end both Poisoned and one disease that explicitly allows magical curing, rather than only one of those benefits. Enhanced Song of Mending: duration becomes 3 rounds and gains one additional 2d6 healing pulse at the start of your second later regular turn; each ally still receives only one 1-HP death prevention per use.", "prerequisite": "Oracle 15; Mystery: Life; Revelation Mastery"}

## oracle.supplement.stars.radiant-path

{"name": "Radiant Path", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "5-tile line originating from you; enemies and up to 3 allies in line", "duration": "Instantaneous; star-ash until end of your next turn", "frequency": "At will while RC remains", "effect": "Enemies in the line make Dexterity saves, taking 2d6+M radiant damage on failure or half on success. Failed enemies are covered in star-ash until the end of your next turn and cannot benefit from mundane concealment. Choose up to three living allies in the line; roll 1d6 once and each regains that much HP if at least one meaningful hostile took damage, maximum healing per ally S+M if lower. After resolution, you and one chosen ally in the line may each move 1 tile along the Path without provoking opportunity attacks.", "prerequisite": "Oracle 6; Mystery: Stars; selected Tier II Revelation"}

## paladin.engine[1]

Base progression is explicit rather than the ordinary 25-card template: at 1 automatically gain Lay on Hands, Divine Sense, Martial Proficiency, Divine Strike, Protective Stance and Sacred Touch. At 2 gain Righteous Challenge, Bolstering Presence, Fighting Style and ordinary Paladin spell access. At 3 swear ONE of ten Oaths; gain only its Smite modification, Aura and first Revelation spell. This Oath is the Arch specialization. At 10 enter Hero Oath Mastery of that SAME Oath; no second Oath or additional generic Hero tree. Signature Power unlocks 11, Final Gift 20. Oath Revelations automatically unlock 3/5/9/13/17, always known in addition to the shared spell repertoire, rank 1/2/3/4/5 respectively. Exact printed RP costs replace generic cost only if the card explicitly supplies them.

## paladin.engine[2]

At 2 choose one Fighting Style: Defense +1 AC while armored; Dueling +2 damage to first one-handed melee hit on your own turn; Protection Reaction impose disadvantage on one attack against an adjacent ally when using a shield. At 3 Divine Health gives advantage on disease saves, not universal immunity. At 5 Extra Attack makes two attacks when taking the ordinary Attack Action; named attack techniques use their own counts. These three features reconcile preserved main-registry entries; other old level-table extras, including extra level 14 ASI and undefined free slot riders, are not stacked into this draft. ASI/feat at 4/8/12/16/19 follows general advancement once.

## paladin.engine[3]

Divine Strike at 1: after one melee weapon hit on your regular turn, spend 1 RP to add S d6 radiant. At 2 this becomes Divine Smite: choose 1 RP for S d6 or 2 RP for(S+1)d8 radiant, once/own turn total. Oath 3 changes type/rider as its card states, never adds another copy of the base damage. Smite is not an ordinary spell, cannot be counterspelled or generically Overcast, and causes no Dissonance. A critical hit doubles Smite damage dice under ordinary rules, but never healing, resources or percentage copies.

## paladin.engine[6]

Protected interface: Smite, Aura and Lay on Hands generate no Weave Dissonance. After a successful direct melee hit, your next Oath spell before end next turn generates 1 less Dissonance, minimum 0, consuming the benefit. No stacking, RP discount or Refrain reset. Oath Revelation spells and the five replacement Forbidden spells below are ordinary spells for strain, countering and concentration; signature powers and final gifts are Oath techniques unless expressly tagged otherwise.

## paladin.engine[7]

Oath conduct clauses remain intact in source and Oath cards. The Director identifies a relevant clause and a knowingly chosen serious breach before applying a fall. A disagreement, failed roll, coerced act or unknown fact does not silently remove a character. A fall is an explicit story transition recorded with the player: choose the corresponding Oathbreaker inversion or pursue an agreed restoration scene. Preserve class level and already spent resources. Oathbreaker replaces its Oath Aura, Smite rider, Signature and Revelation list, rather than stacking both sets. Base martial abilities remain; Lay on Hands becomes Death Touch using the same current 5 L pool, with no refill on switching.

## paladin.engine[8]

Death Touch baseline: Action melee divine attack PB+CHA; declare and spend 1 through 2 S+M points before the attack from remaining Lay on Hands pool to deal that much necrotic damage (choose amount before roll; miss still spends declared points). Each Oath inversion may alter type or add its bounded rider; never copy innate traits, confiscate class engines or automatically execute a target. A listed inverted Signature is available only at 11 and replaces the ordinary Signature use, one/short rest. An inverted aura follows the same radius, target cap and timing. Oathbreaker 20 uses the new Black Manifestation common capstone instead of its original Final Gift.

## paladin.engine[10]

Oath integration limits: one paid Smite total per round, including the level-7 Reaction; one Oath-aura reactive event per round. Multiple damage-redirection options share one event per round unless Crown Undying expressly allows two. Apply original-target defenses once, then split actual damage; transferred damage cannot be mitigated again, reflected, redirected again or generate resources. This explicit rule supersedes wording that permits recipient defenses again.

## paladin.engine[13]

The source ceiling’s half-pool-per-round Lay on Hands cap is a preserved alternative. This pilot instead uses maximum class level per ordinary Lay on Hands Action and the explicitly once-per-long-rest level-17 Wave that distributes the current remaining pool. No normal heal gains the Wave’s exception.

## paladin.engine[14]

For any one damage event choose exactly one Paladin redirection feature. Using it consumes the shared redirection allowance for that round. Crown Undying permits two DIFFERENT ally-damage events per round, but still only one redirection feature may modify each event.

## paladin.supplement.oathbreaker-shared.blighted-benediction

{"name": "Blighted Benediction", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "One creature 30 ft", "duration": "Until end target next turn", "frequency": "At will while RP remains", "effect": "New rank 1 Forbidden spell. Divine spell attack; hit S d8 necrotic and target-1 on next attack roll. No healing, command or second strike. Ordinary spell strain applies.", "prerequisite": "Paladin 3; selected Oathbreaker inversion"}

## paladin.supplement.oathbreaker-shared.dread-shelter

{"name": "Dread Shelter", "activation": "Bonus Action", "cost": "3 RP", "rangeAndTarget": "Self", "duration": "Concentration, 1 minute", "frequency": "At will while RP remains", "effect": "New rank 2 Forbidden spell. Gain 2 S+M temporary HP on casting and 1 flat DR against weapon damage for duration. No recurring temp HP pulse or healing.", "prerequisite": "Paladin 5; selected Oathbreaker inversion"}

## paladin.supplement.oathbreaker-shared.black-manifestation

{"name": "Black Manifestation", "activation": "Bonus Action", "cost": "1 long-rest use", "rangeAndTarget": "Self and up to 3 enemies in aura", "duration": "Until start next turn", "frequency": "1/long rest", "effect": "New Oathbreaker Final: gain 2 S+M temporary HP; chosen enemies WIS save or lose Reactions and Speed-10 ft for duration. Refresh one expended Signature use, then pay its normal Action and other costs when used. No Death Touch pool, RP, extra Action or Final reset.", "prerequisite": "Paladin 20; selected Oathbreaker inversion"}

## paladin.supplement.oathbreaker-oath-of-mercy.death-touch-life-drain

{"name": "Death Touch — Life Drain", "activation": "Action", "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss", "rangeAndTarget": "One creature within melee reach; up to 2 additional living creatures within 5 feet", "duration": "Instantaneous", "frequency": "At will while Lay on Hands points remain; rider once per turn", "effect": "Make a melee divine attack using PB+Charisma. On hit the primary target takes necrotic damage equal to the declared Lay on Hands points. Then up to 2 other living creatures within 5 feet make Constitution saves, taking S necrotic damage on failure or half on success. Regain HP equal to half the total actual necrotic damage dealt by the secondary drain, rounded down, maximum S+M. Constructs and undead provide no healing.", "prerequisite": "Paladin 3; Oathbreaker — Oath of Mercy"}

## paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate

{"name": "Exsanguinate", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "Up to 3 living creatures in your Oath aura", "duration": "Instantaneous", "frequency": "1/short rest; replaces Signature Power use", "effect": "Each target makes a Constitution save, taking 2 S d8 necrotic damage on failure or half on success. Regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. Undead and constructs are unaffected and cannot be used to generate healing.", "prerequisite": "Paladin 11; Oathbreaker — Oath of Mercy"}

## paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution

{"name": "Death Touch — Malicious Execution", "activation": "Action", "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss", "rangeAndTarget": "One creature within melee reach", "duration": "Instantaneous", "frequency": "At will while Lay on Hands points remain; rider once per turn", "effect": "Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared Lay on Hands points. If the target was already at or below half maximum HP, it makes a Constitution save; on failure add S d6 necrotic damage. This rider never automatically executes or bypasses normal death rules.", "prerequisite": "Paladin 3; Oathbreaker — Oath of Vengeance"}

## paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood

{"name": "Death Touch — Blighting Blood", "activation": "Action", "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss", "rangeAndTarget": "One creature within melee reach; its occupied space", "duration": "Damage instantaneous; blighted space until start of your next regular turn", "frequency": "At will while Lay on Hands points remain; terrain rider once per turn", "effect": "Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared points and blight the target's space until the start of your next turn. The first hostile creature other than the original target that enters or starts its turn in that space takes S necrotic damage. The patch creates no corpse, healing or resource trigger.", "prerequisite": "Paladin 3; Oathbreaker — Oath of Flame"}

## paladin.supplement.oath-of-the-ancients.thorn-crown

{"name": "Thorn Crown", "activation": "Reaction", "cost": "2 RP", "rangeAndTarget": "Creature that just imposed a condition on you within 60 feet", "duration": "Reflected condition maximum 1 round", "frequency": "1/short rest", "effect": "Trigger after a hostile creature causes you to fail a save and gain a finite-duration condition. The source immediately makes the same type of saving throw against your Oath DC. On failure it suffers the same named condition until the end of its next turn, subject to the universal hard-denial guard. Your original condition is not removed unless another feature removes it. Thorn Crown cannot reflect damage, death, curses, Wounds, resource loss or permanent transformations.", "prerequisite": "Paladin 11; Oath of the Ancients"}

## paladin.supplement.oath-of-the-chain.chain-of-duty

{"name": "Chain of Duty", "activation": "Action", "cost": "3 RP", "rangeAndTarget": "One willing ally within 30 feet", "duration": "Concentration, maximum 3 rounds", "frequency": "At will while RP remains", "effect": "Mark the ally. If it is reduced to 0 HP while within 60 feet and on the same plane, you may use your Reaction to teleport to an unoccupied space adjacent to it. This teleport prevents no damage and does not heal either creature. The spell then ends.", "prerequisite": "Paladin 5; Oath of the Chain"}

## paladin.supplement.oath-of-grief.memorial-flame

{"name": "Memorial Flame", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "30-foot-radius light centered on a point within 30 feet", "duration": "Concentration, maximum 1 minute", "frequency": "At will while RP remains", "effect": "The memorial light reveals hidden or invisible undead within it unless an effect explicitly defeats divine detection. Allies in the light gain +2 on death saves. Hostile undead in the light have disadvantage on attack rolls. The light does not damage undead or reveal non-undead invisible creatures.", "prerequisite": "Paladin 9; Oath of Grief"}

## paladin.supplement.oath-of-the-martyr-king.crown-of-embers

{"name": "Crown of Embers", "activation": "Bonus Action", "cost": "2 RP", "rangeAndTarget": "Up to 3 allies in your Oath aura", "duration": "Until start of your next regular turn", "frequency": "1/short rest", "effect": "Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself.", "prerequisite": "Paladin 11; Oath of the Martyr King"}

## paladin.supplement.oath-of-the-martyr-king.burden-shared

{"name": "Burden Shared", "activation": "Reaction when an ally takes damage", "cost": "5 RP", "rangeAndTarget": "Triggering ally and up to two other willing allies in your aura", "duration": "One damage event", "frequency": "While RP remains", "effect": "After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round.", "prerequisite": "Paladin 9; Oath of the Martyr King"}

## ranger.engine[5]

Chosen Hero grants a sixth Arrow at 11. Warder Nature's Wrath: ranged attack weapon+S d6 piercing; up to 2 allies within 10 ft gain M temporary HP (finite mitigation, not repeatable real healing). Stalker Phantom: two ranged attacks against different aligned targets within 60 ft, each weapon damage, no extra dice; one Arrow activation. Outrider Corruption: place 10 ft-radius zone within 60 ft, concentration until start next turn; up to 3 enemies entering/starting there take S d4 necrotic once each, CON half. Arrow copies cannot generate extra attacks, resources or permanent terrain changes.

## ranger.hero.warder.healing-briar

{"name": "Healing Briar", "activation": "Action", "cost": "4 RP", "rangeAndTarget": "Fixed 10 ft-radius natural-ground zone within 30 ft; 3 allies/pulse", "duration": "Concentration, 3 of your turns", "frequency": "Recharge 4", "effect": "On start heal 1d8+M per chosen living ally; on next 2 turns Bonus Action+1 RP repeats pulse. Maximum 3 pulses; no passive additional entry healing and no Wound removal.", "prerequisite": null}

## ranger.hero.warder.beast-companion

{"name": "Beast Companion", "activation": "Ritual", "cost": "4 RP; 1 hour with a willing/tamed eligible beast", "rangeAndTarget": "One beast touched", "duration": "Bond persists; one companion", "frequency": "1/long rest", "effect": "Bond eligible beast using standard companion stats plus Wisdom modifier HP; preserve one movement mode up to 40 ft and keen-sense advantage. Bonus Action command gives one attack, no imported boss powers. Injury persists; heal normally. Death requires a new bond after long rest, not free resummoning.", "prerequisite": null}

## shaman.engine[2]

On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction.

## shaman.engine[3]

The book places Flask Use at Base but describes advanced flask casting as Theurgist/Soothsayer-only. For this draft, Base Flask Use grants mundane prepared tactical flasks thrown with an Action; at Hero 10 only Theurgist/Soothsayer gain magical Bonus Action flasks. Bloodcaller retains mundane alchemical knowledge, not the advanced flask subsystem. At long rest prepare 2 flasks, rising to 3 at 5 and 4 at 11; no encounter refill or stockpiling, total carry cap 4, unused contents become inert when preparing a new batch. This finite-rest supply replaces encounter-based free heal farming.

## shaman.engine[4]

Flask tier uses S. Mundane Base modes: Burn=one enemy 30 ft DEX save S d6 fire half, failure 1d4 fire next turn; Root=one ground enemy 30 ft STR save Speed 0 until end its next turn; Weaken=one enemy 30 ft CON save or-1 attack damage until end its next turn. Advanced Hero modes additionally: Stun=one enemy 30 ft CON save or no Reactions, failure by 10 Stunned until end its next turn; Heal=one living ally 30 ft S d6+M HP; Restore=end Frightened or Poisoned on one ally 30 ft. Every thrown flask consumes one prepared unit and 2 RP for advanced magic (Base mundane flasks cost 0 RP). Changing payload requires no separate crafting action when throwing. No flask leaves harvestable poison or another flask.

## shaman.arch.extended-totem-duration

{"name": "Extended Totem Duration", "activation": "Passive", "cost": "0; full upkeep for extra Renewal pulse", "rangeAndTarget": "One of your totems", "duration": "Maximum 4 of your turns", "frequency": "Continuous", "effect": "Totems last 1 extra turn. Renewal may have a fourth pulse only if you pay Bonus Action+1 RP on that turn; no fifth pulse and no automatic free healing. Concentration still required.", "prerequisite": null}

## shaman.arch.spirit-cache

{"name": "Spirit Cache", "activation": "Triggered", "cost": "1 short-rest use", "rangeAndTarget": "One flask/to-tem effect you directly used", "duration": "Stored until encounter end", "frequency": "1/short rest", "effect": "Store its profile, not an active copy. On a later turn use normal Action/Bonus Action and pay all RP and a new flask unit or full totem cost to repeat it. Add 1d6 to one numerical damage/heal amount; no copy of refund/limited use.", "prerequisite": null}

## shaman.arch.totem-pulse

{"name": "Totem Pulse", "activation": "Passive", "cost": "1 RP optional", "rangeAndTarget": "Up to 3 creatures inside newly placed non-healing totem", "duration": "Instant", "frequency": "Once/turn", "effect": "On placement pay 1 RP: allies gain M temporary HP OR enemies make DEX save for S affinity damage, half on success. No immediate second Renewal healing pulse, no repeat from moving the totem.", "prerequisite": null}

## shaman.arch.spirit-saturation

{"name": "Spirit Saturation", "activation": "Triggered", "cost": "1 long-rest use", "rangeAndTarget": "One non-Renewal totem you place", "duration": "Normal duration", "frequency": "1/long rest", "effect": "Waive its 2 RP placement cost once. Still use Action, concentration, capacity and any added costs. Cannot create a healing totem or be cached/refunded to generate more free casts.", "prerequisite": null}

## shaman.hero.theurgist.echo-totem

{"name": "Echo Totem", "activation": "Triggered", "cost": "1 additional RP", "rangeAndTarget": "Adjacent empty space within 5 ft of newly placed totem", "duration": "Same remaining duration", "frequency": "Once/placement", "effect": "Create a weak echo anchor of that totem. It counts toward capacity; if no space in capacity, cannot create it. Its radius 10 ft and numerical bonuses/healing are half, rounded down. Shared concentration/upkeep and same-name nonstacking prevent double healing.", "prerequisite": null}

## shaman.hero.theurgist.elemental-harmony

{"name": "Elemental Harmony", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your summoned elemental", "duration": "Summon duration", "frequency": "Continuous", "effect": "Add class level to its maximum/current HP on creation and 1 turn duration, maximum 4 turns for class summons. Cannot extend once/day Chorus beyond 4 turns or restore an existing creature's lost HP.", "prerequisite": null}

## shaman.hero.theurgist.summon-cinderflame

{"name": "Summon Cinderflame", "activation": "Action", "cost": "4 RP", "rangeAndTarget": "One spirit within 30 ft", "duration": "Concentration, 3 of your turns", "frequency": "Recharge 4", "effect": "Summon standard Cinderflame. Commanded hit deals fire plus Burn 1d4 next target turn. On destruction only (not dismissal), up to 3 enemies within 5 ft make DEX save for S d4 fire, half. Explosion creates no further death/resource triggers.", "prerequisite": null}

## shaman.hero.soothsayer.healing-splash

{"name": "Healing Splash", "activation": "Bonus Action", "cost": "1 prepared flask; 3 RP", "rangeAndTarget": "Up to 3 living allies in 5 ft radius within 30 ft", "duration": "Instant", "frequency": "Recharge 3", "effect": "Each regains S d6+M HP, shared roll. This consumes a flask and replaces its normal payload. No damage to enemies, free conditions removed or resource refunds beyond the explicit once/day Predictive Alchemy.", "prerequisite": null}

## shaman.supplement.elder-spirit-accord-new-hero-capstone

{"name": "Elder Spirit Accord — new Hero capstone", "activation": "Triggered", "cost": "1 long-rest use", "rangeAndTarget": "Your chosen Hero ultimate", "duration": "One activation", "frequency": "1/long rest", "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast.", "prerequisite": "See class engine and progression."}

## soldier.engine[4]

Base 1–2, Commander Arch 3–9, then Champion/Artillerist/Tyrant Hero 10–20. Palisade 5 is automatic; Intercepting Shot has minimum 6 and Fortify Zone 9. Other cards require selection. There is no source automatic Arch capstone. At 20 gain the new Final Command below, clearly a playtest addition. No spell or sustained technique may be used to obtain infinite ammunition, structures, actions or permanent healing.

## soldier.hero.artillerist.precision-engineering

{"name": "Precision Engineering", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your constructed barriers and turrets", "duration": "While present", "frequency": "Continuous", "effect": "Increase maximum and initial HP by M. Does not heal existing damaged structures when learned or moved; repairing remains finite.", "prerequisite": null}

## soldier.hero.tyrant.brutal-example

{"name": "Brutal Example", "activation": "Action", "cost": "One ammunition; 1 short-rest use", "rangeAndTarget": "One enemy below half HP in weapon range", "duration": "Until end next target turn", "frequency": "1/short rest", "effect": "Weapon attack; on hit add 2 S d6 damage. Up to 2 enemies within 10 ft of victim WIS save or Frightened of you for duration. No automatic death threshold or fear through immunity.", "prerequisite": null}

## thief.engine[2]

At 1 know all four Tier I recipes, at 7 add Tier II, at 14 Tier III. Poison saving throws use Thief DC except preserved source fixed DC 12 becomes max(12, Thief DC) for Mindburn/Venombite. Unless stated damage/conditions require a failed CON save; initial weapon damage is unaffected. Critical riders also need this failed save. One ongoing instance of each recipe per target; another application refreshes rather than stacks. Maximum 2 simultaneous different poison recipes from you per target. Bleed never stops all healing by default, Poisoned uses the Core V 2 condition: disadvantage on attacks and ability checks (not saving throws), and Shaken means disadvantage on next fear save. Neither is a hidden full-turn disable.

## thief.engine[3]

Tier I: Bloodleech gives Bleed 1d4 at start next 2 target turns; critical restores 1d4 of your HP, once per dose. Crippler gives-1 on next attack before end next turn; critical also half Speed for that duration. Mindburn uses WIS save: -1 spell-attack rolls until end next turn, critical also no Reactions. Venombite gives Poisoned until end next turn; critical also-1 on next save. Tier II: Ashblood adds 2d6 poison now and 1 fire at start next 2 turns; critical prevents HP recovery through end next turn. Silencer prevents verbal spellcasting through end next turn, critical also drops one held nonbonded item into its space; it can retrieve normally. Shiver gives Shaken through end next turn; critical also no Reactions. Hexroot gives-1 saves for 2 target turns; critical lets next weapon hit ignore resistance, never immunity, before end next turn.

## tinker.engine[2]

A destroyed drone remains 0 HP until repaired for 1 RP and 10 minutes with tools to half HP, once/short rest, or rebuilt during long rest to full. Ordinary repairing does not recharge devices, grant organic healing or trigger destruction bonuses. At 13 Dual Drone Protocols automatically chooses on each long rest either 2 basic drones each with one module, or one drone with 2 distinct modules. Still one command budget. Never more than 2 drones.

## tinker.engine[7]

Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets.

## tinker.base.quick-fingers

{"name": "Quick Fingers", "activation": "Bonus Action", "cost": "0", "rangeAndTarget": "One noncombat mechanism touched", "duration": "One manipulation", "frequency": "Once/turn", "effect": "Open unlocked latch, operate simple switch or retrieve a carried gadget. Does not activate damaging/healing devices, disarm a trap, reload every weapon or add another Bonus Action.", "prerequisite": null}

## tinker.arch.deployable-expertise

{"name": "Deployable Expertise", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your deployables", "duration": "While deployed", "frequency": "Continuous", "effect": "Gain M maximum/initial HP and+1 AC. Does not heal existing damage when moved or grant additional slots. Drones excluded unless another card says otherwise.", "prerequisite": null}

## tinker.hero.artificer.protective-programming

{"name": "Protective Programming", "activation": "Reaction", "cost": "1 RP", "rangeAndTarget": "Drone adjacent to ally hit by attack", "duration": "One hit", "frequency": "Once/round", "effect": "Drone grants ally S+M temporary HP before hit resolves. No heal or reversal of hit; max one protected ally, normal temporary HP nonstacking.", "prerequisite": null}

## tinker.hero.artificer.efficient-power-cells

{"name": "Efficient Power Cells", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your nonhealing deployables", "duration": "Deployment", "frequency": "Continuous", "effect": "A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration.", "prerequisite": null}

## tinker.hero.artificer.nano-aegis-drone

{"name": "Nano-Aegis Drone", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "Your drone within 15 ft", "duration": "3 rounds", "frequency": "Recharge 4", "effect": "Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode.", "prerequisite": null}

## tinker.hero.artificer.restoration-field

{"name": "Restoration Field", "activation": "Action", "cost": "3 RP start; 1 RP maintenance; one slot", "rangeAndTarget": "10 ft radius within 30 ft", "duration": "Maximum 3 pulses", "frequency": "Recharge 4", "effect": "Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells.", "prerequisite": null}

## tinker.hero.techsmith.technical-mastery

{"name": "Technical Mastery", "activation": "Triggered", "cost": "1 RP", "rangeAndTarget": "Your damaging device activation", "duration": "One target", "frequency": "Once/own turn", "effect": "After damage rolld 10; on 10 you may pay 1 RP to add half its unmodified damage dice total rounded down to one target. No second activation, commands, procs, resources or healing duplication.", "prerequisite": null}

## tinker.hero.techsmith.reconfiguration

{"name": "Reconfiguration", "activation": "Action", "cost": "1 RP", "rangeAndTarget": "One deployed device within 15 ft", "duration": "Remaining duration", "frequency": "Recharge 3", "effect": "Change between known nonhealing profiles using same HP fraction, slot, expiry and spent uses. Cannot turn a 1 slot device into two, refill ammo, reset trap, create fresh death trigger or morph drone into free bomb.", "prerequisite": null}

## tinker.hero.warmachine.scrap-reaper

{"name": "Scrap Reaper", "activation": "Reaction", "cost": "2 RP; one destroyed enemy-hit device", "rangeAndTarget": "Debris within 30 ft", "duration": "Until end next turn", "frequency": "1/short rest", "effect": "Create one Scrapling Speed 30, AC 12 HP L; next Bonus Action command moves and detonates within 5 ft one enemy for 2 S d6 fire DEX half. Uses one command budget and ends. No chain from deliberate sacrifice or its own death.", "prerequisite": null}

## tinker.supplement.mech-overdrive

{"name": "Mech Overdrive", "activation": "Triggered on deploying a device", "cost": "1 long-rest use plus original deployment cost", "rangeAndTarget": "One of your newly deployed devices", "duration": "Until encounter end, maximum 1 minute", "frequency": "1/long rest; automatic Hero capstone", "effect": "Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment.", "prerequisite": "See class engine and progression."}

## warrior.engine[15]

HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT.

## warrior.arch.mutation-overload

{"name": "Mutation Overload", "activation": "Bonus Action", "cost": "+2 Strain", "rangeAndTarget": "Your currently active mutations", "duration": "2 rounds; backlash until end of following turn", "frequency": "1/short rest", "effect": "Mutation Overload. For 2 rounds, enhance each currently active mutation once: an AC, DR, attack, save or flat-damage bonus increases by 1; a movement or reach bonus increases by 5 feet; or one mutation damage/healing roll gains +1d4. Immunities, target counts, resource generation and action grants cannot be increased. When Overload ends, you suffer -1 on attack rolls and saving throws and -5 feet Speed until the end of your next regular turn. This activation is illegal if +2 Strain would exceed the Strain cap.", "prerequisite": null}

## warrior.hero.dreadspawn.pain-empowerment

{"name": "Pain Empowerment", "activation": "Passive", "cost": "0", "rangeAndTarget": "Self", "duration": "While below maximum HP", "frequency": "Always", "effect": "Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects.", "prerequisite": null}

## warrior.supplement.primed

{"name": "Primed", "activation": "Passive", "cost": "0", "rangeAndTarget": "One active mutation each turn", "duration": "While BT remains at least 2", "frequency": "Once per turn", "effect": "Enhance one active mutation's numeric benefit for the turn: +1 to one AC, DR, attack, save or flat damage bonus; +5 feet to one movement/reach bonus; or +1 damage/healing to one mutation-generated roll. Primed never increases duration, targets, immunity or resource generation.", "prerequisite": "BT 2+"}

## warrior.supplement.transcendent

{"name": "Transcendent", "activation": "Triggered", "cost": "0", "rangeAndTarget": "Self", "duration": "Until start of your next regular turn", "frequency": "1/encounter total, regardless of trigger", "effect": "At Warrior 12+, the first time this encounter you cross 100% Brutality Progress or reach stored BT 4, activate all equipped mutations until start of your next regular turn. No serum profile or immediate healing trigger is granted. This is one total pulse, never a permanent BT 4 concurrency increase. At end choose active mutations up to normal limit, with their original remaining durations; others become dormant.", "prerequisite": "Warrior 12; 100% Brutality Progress or BT 4 with raised cap; new explicit level gate"}

## warrior.supplement.sanguine-surge

{"name": "Sanguine Surge", "activation": "Via Serum Injection", "cost": "Dose consumption and normal Strain", "rangeAndTarget": "Injected living creature", "duration": "3 rounds", "frequency": "Per prepared dose; same creature cannot receive its healing more than once per short rest", "effect": "On injection regain 2d6 HP and gain +10 feet Speed for 3 rounds. Side effect: when the profile ends gain 1 additional Strain, maximum 3. Serum Tolerance suppresses that ending side effect. This healing removes no Wounds and cannot operate on a dead creature.", "prerequisite": "Prepared serum dose"}

## wizard.engine[10]

ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn.

## wizard.engine[15]

MATRIX MASTERY MODIFICATIONS. After acquiring Matrix Mastery, each prepared ordinary spell matrix may carry at most one modification chosen during preparation. QUICK SUBSTITUTION: once per short rest, replace one matrix marked Quick Substitution with another spellbook spell of exactly the same rank using a 1-minute ritual instead of the normal 10-minute midday swap; the replacement loses the modification until the next long rest. COMPONENT ENHANCEMENT: when casting a damaging or healing matrix, spend 1 additional RP to add one extra die of the spell's primary damage or healing die to one roll; if the spell has no such die this modification has no effect. MATRIX LINKING: pair two different prepared matrix families during preparation; after legally casting one, the other costs 1 less RP, minimum 1, if cast before the end of your next regular turn, at most once per pair per round. STABILITY REINFORCEMENT: gain +2 on concentration saves caused by damage while maintaining that matrix. A matrix modification never creates another spell cast or proc event.

## wizard.hero.spellbinder.arcane-sanctuary

{"name": "Arcane Sanctuary", "activation": "Ritual", "cost": "10 RP", "rangeAndTarget": "You and up to eight willing creatures within 15 feet", "duration": "1 hour", "frequency": "1/week; automatic Spellbinder Final Theorem", "effect": "Arcane Sanctuary. Tags: hero, spellbinder, final-theorem, demiplane. Perform a 10-minute ritual to open a temporary demiplane and transport the willing targets inside. For 1 hour creatures inside cannot cast or activate harmful magical effects and magical effects originating outside cannot enter. Nonmagical violence remains physically possible, ordinary healing and communication may function, and creatures can leave through the visible exit as an Action. When the hour ends all occupants return to the entry location or nearest legal spaces.", "prerequisite": null}
