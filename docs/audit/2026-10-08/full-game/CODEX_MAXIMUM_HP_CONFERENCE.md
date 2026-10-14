# Maximum HP, thresholds and composition — exact source conference

Codex → Calibration Review. Please reply below18,000 characters. Preserve every source. Classify ALL supplied51 class passages plus7 feat records by exact source ID, separating actual maximum-HP modifiers, thresholds, percentage healing/damage, guards and exclusions. Lexical matches are not semantic completeness. No ordinary spell source object matched this wording; this is not proof of no hidden maxHP behavior in unfinished spells/items/monsters. This is a bounded composition proposal, not promotion of all feats.

Existing closed bridge: multiply rational systemic maximumHP factors against the same otherwise-applicable maximum, floor ONCE, minimum1. Expedition4+ contributes3/4; Exhaustion4+ contributes1/2; base100 gives37. CurrentHP clamps down to effective maximum without damage/Wounds/resource/death-failure triggers. Removal raises capacity without healing or resetting counters. Critical's max(1,effectiveMaximum−1) is HEALING ceiling, not another maxHP multiplier. At lethal track6, actual life transitions remain handled by the already reviewed lethal-track module; numerical recomputation alone must not re-kill a collapsed survivor.

We need explicit source-backed or labeled NEW decisions:

1. Complete stage equation: base character/creature maximum + compatible permanent bonuses + active temporary bonuses − reductions, then systemic factors once? Or do temporary flat drains apply AFTER multipliers? Choose and justify with examplesbase101,FleshWarden+20,Monk−9,Exhaustion×1/2,Expedition×3/4. Track modifiers separately to avoid repeated multiplication and recast/suppression drift. Does flatstrongest rule apply across distinct permanent FEATS or only class technique bonuses?
2. Monkengine9 'largest reduction from your Monk features': previous131discussion treated perowner. Do reductions from different Monkowners stack, or does firstsentence 'do not stack on samecreature' require globalstrongest? Source is internallyambiguous. We need explicit resolution, not silently change earlierperownerdecision. Different sourceIDs sameowner max only; suppressedlargest revealsnexteligible while clocksstilltick. Repeatedsamecard applications fromsameowner? strongestamount/longestremainingendpoint or separateeffects withseparateexpiry? Unless earlierend, anycompletedshortorlongrest ofTARGETclearsallMonktrauma, regardlessrestrewardcaps? Ifrestinterruptednone. Parent DeathlessSilence target-end passive suppression mustnotshorten separatemaximumHPreduction.
3. FleshWardenequipped+2WarriorL capacityonly, noheal. SummoncreationwithWizardConjuration+L orFleshAscendant+2L initialHPdoesitstartatfinalboostedmaximum? Latergainingcontrol/equippingbonus onlycapacitywithoutheal. Conjuration+FleshAscendantsameundead summon: compatibleadditive vsstrongestclassflat? FleshAscendant engine24 explicitly 'afterlistedbase' but no explicitstack. Changingcontroller vsfixedcaster schoolbonus trackownerandeligibility. Do not inventcompanioncap/newheal oncontroller swaps.
4. Feats: Tenacity+1percharacterlevel grows; Tough exacttext says+twicelevelWHENgained but nofuturelevel clause; ToughasNailsexplicitgrows+2perlaterlevel. KeepTough acquisition-levelsnapshot vsinferfuturegrowth? Source-specific and preserve source; don't useanothergame'smemory. DarkFortitude+2percharacterlevel dynamic. Same-name duplicates no stack; distinctfeatbenefits stack or strongest? Constitutionbasegrowth/advancementprocedures stillseparate. FamiliarBond 'gains hitpoints equaltolevel' maximumvsimmediatehealingambiguous; proposedcapacitybonus, initialcreationfullboostedHP; latercapacitygainnoheal. Its attackcommandlifecycle remainsopen.
5. CurrentHPclampnotdamage norHPpayment; doesDecaypreventcapacityrestoration? Expectedno. AddingmaxHPwithoutHPgain changespercentthresholds; dynamicpassivesrecomputebut event 'firstfallbelow/atquarter' mustnottriggermerelymaximumchanges. Distinguish actualdamage/loss/healing transitions. Becomingabovehalfsolelymaximumdecrease doesn'tsatisfy 'untilHEALEDabovehalf'. MythicCarapace/Butcherformendswhenbelowquarter: continuousendconditionvsdamagecrossing? Theirdurationwordingneedsindividualdisposition.
6. Fractioncomparison: avoidroundedthresholderrors useexactcrossmultiply (at/belowquarter 4HP<=max, strictlybelowhalf2HP<max). Percentagehealing floorformula atresolutioneffectiveMaxunlesssourceexplicitprevalue; preserve min1onlywheresourcegrantsit. WoundEaterIII no min1 atsmallmax; DivineRebirthhalf nofreeinventedfloor unlessexistingrevivalbridgeapplies. Thresholdsnapshotatselection/beforeattack vsafterevent percard. RewindWound stored HP snapshot maximum atthatdamageevent, no retroactivequalify aftermaxchange. Brutalityprogress threshold state alreadyreviewed snapshot rules; don'treopenunchangedcode.
7. Stat update on dead/stable/0HP creatures leaves life/death counters untouched; minimummax1neverresurrects. ReducingmaxbelowcurrentTempHPdoesnotclampTempHP (independentbuffer), unlesssourceexplicit. Removingdebuff nothealing so doesn't trigger ordinarycure/HPgainprocs. HealingceilingCritical recomputesaftermaximumchanges.
8. Source-order with damaging attack that ALSO lowersmaxHP: resolve attack damage+Wounds/InstantDeath againstpretrauma maximum, thenapply successfuldrainclamp tosurvivingtarget? Existinghit-rider ordering sourceexactneeddecide. MaxHPincreasewithin sameevent mustnotrewrite alreadyfrozen actualDamage metrics. Offer adversarial examplesbeforecoding.

Return a bounded sharedprocedure, all58individualclassifications and openevidencedependencies. No whole-game completion.


## cleric.engine[7]

Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction.

## cleric.arch.anointed-guardian

{"name": "Anointed Guardian", "activation": "Triggered", "cost": "0", "rangeAndTarget": "First ally within 30 feet to fall to one-quarter maximum HP or less", "duration": "2 rounds", "frequency": "Once per encounter", "effect": "Anointed Guardian. Tags: protection, bishop. The first qualifying ally in an encounter gains a ward for 2 rounds. The first time during each round that ally takes damage, reduce that damage by PB + M, minimum 0. The ward does not prevent conditions attached to an attack unless the damage reduction itself invalidates them under another rule.", "prerequisite": null}

## cleric.hero.saint.aura-of-grace

{"name": "Aura of Grace", "activation": "Triggered and passive", "cost": "1 RP per healing pulse", "rangeAndTarget": "Living allies within 15 feet", "duration": "Passive during real encounters", "frequency": "Healing once/own regular turn; critical reduction once/ally/round", "effect": "Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing.", "prerequisite": null}

## cleric.hero.saint.divine-rebirth

{"name": "Divine Rebirth", "activation": "Triggered", "cost": "0", "rangeAndTarget": "One ally revived by your Cleric feature", "duration": "Instantaneous plus temporary HP for 1 minute", "frequency": "1/long rest", "effect": "Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.", "prerequisite": null}

## cleric.hero.saint.merciful-sacrament

{"name": "Merciful Sacrament", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your Sacrament", "duration": "For that activation", "frequency": "1/short rest", "effect": "Merciful Sacrament. Tags: saint, sacrament. When you start Sacrament and at least one living ally inside its initial zone is at or below one-quarter maximum HP, you may reduce that Sacrament's Conviction cost to 0. Its RP cost and all other requirements remain. Because no Conviction is spent, this waived cost does not vent Dissonance.", "prerequisite": null}

## cleric.hero.saint.unyielding-light

{"name": "Unyielding Light", "activation": "Triggered", "cost": "0", "rangeAndTarget": "Up to six living party members within 30 feet, including you", "duration": "Instantaneous", "frequency": "1/long rest", "effect": "Unyielding Light. Tags: saint, emergency, healing. When one damage event would leave every conscious living party member within 30 feet at 0 HP, resolve that damage, then before ordinary death-save progression each qualifying living creature at 0 HP regains floor(maximum HP/3), minimum 1. It cannot revive a creature killed outright and removes no Wounds. This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.", "prerequisite": null}

## cleric.hero.saint.mass-healing-light

{"name": "Mass Healing Light", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "Up to six living allies within 30 feet", "duration": "Instantaneous", "frequency": "Recharge 3 rounds", "effect": "Mass Healing Light. Tags: saint, healing. Roll S d8 + M once. Each target regains that amount. A target below half maximum HP when chosen regains an additional 1d8 HP. Roll that bonus once and apply it to all qualifying targets. This cannot revive the dead or remove Wounds.", "prerequisite": null}

## cleric.hero.cultist.corrupt-divinity

{"name": "Corrupt Divinity", "activation": "Action", "cost": "4 RP", "rangeAndTarget": "One enemy within 60 feet", "duration": "Maximum 2 rounds", "frequency": "Recharge 3 rounds", "effect": "Corrupt Divinity. Tags: cultist, debuff, control. The target makes a Wisdom save. On failure it takes -1 on attack rolls and saving throws. It repeats the save at the end of each turn, ending the effect on success. If a non-player NPC at or below one-quarter maximum HP fails the initial save by 10 or more, it is also Charmed by you until the end of its next turn. This never permanently converts allegiance, changes beliefs or overrides a player character's agency.", "prerequisite": null}

## dragoon.hero.dragon-guardian.wyrmhide

{"name": "Wyrmhide", "activation": "Passive", "cost": "0", "rangeAndTarget": "Self while above half maximum HP", "duration": "While threshold met", "frequency": "Continuous", "effect": "Reduce each damage instance by 2 and gain advantage on CON saves against Bleed, Burn and Poisoned. No blanket condition immunity; effects already present persist and ordinary nonstacking reduction applies.", "prerequisite": null}

## mage.hero.lich.flesh-to-ash

{"name": "Flesh to Ash", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "15-foot-radius sphere centered at a point within 60 feet", "duration": "Instantaneous", "frequency": "Recharge 3 rounds", "effect": "Flesh to Ash. Tags: mage-spell, lich, necrotic, damage. Creatures of your choice in the area make Constitution saves. A target at half maximum HP or more takes S d8 necrotic on failure, half on success. A target below half maximum HP instead takes 2 S d8 necrotic on failure, half on success. Determine the threshold before rolling damage.", "prerequisite": null}

## mage.hero.lich.soulbound-ritual

{"name": "Soulbound Ritual", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "One of your destroyed bound elite undead companions within 30 feet or its inert binding token", "duration": "Instantaneous", "frequency": "1/long rest", "effect": "Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again.", "prerequisite": null}

## monk.engine[9]

Temporary maximum-HP reductions caused by Monk features do not stack on the same creature; use the largest reduction from your Monk features. Maximum HP cannot be reduced below 1. Unless a card specifies an earlier end, the reduction lasts until the creature completes a short or long rest. Restoring maximum HP does not restore current HP. These effects are temporary combat trauma, not unstated permanent injuries.

## monk.engine[16]

Healing from Monk cards cannot exceed maximum HP, restore the dead or remove Wounds unless explicitly stated. Permanent HP recovery and Ki generation cannot be farmed outside encounters. Resurrection effects are explicitly limited-use. No Monk card can instantly kill a target merely because a descriptive source used language such as Death Touch; death continues to follow the game's ordinary damage and dying rules.

## monk.hero.iron-fist-master.ribcrusher-strike

{"name": "Ribcrusher Strike", "activation": "Triggered", "cost": "2 Ki", "rangeAndTarget": "One creature hit by your unarmed strike", "duration": "Until target completes a short or long rest", "frequency": "Once per target per encounter", "effect": "Ribcrusher Strike. Tags: hero, iron-fist, attack, max-hp. After an unarmed strike hits, spend 2 Ki. The target makes a Constitution save. On failure reduce its maximum HP by S+M, minimum maximum HP 1. This reduction follows the common non-stacking maximum-HP rule and is restored after a completed short or long rest without restoring current HP.", "prerequisite": null}

## monk.hero.iron-fist-master.bone-breaking-strike

{"name": "Bone-Breaking Strike", "activation": "Action", "cost": "2 Ki", "rangeAndTarget": "One creature within unarmed reach", "duration": "Until target completes a short or long rest", "frequency": "Recharge 3 rounds", "effect": "Bone-Breaking Strike. Tags: hero, iron-fist, attack, max-hp. Make one unarmed strike. On a hit, the target makes a Constitution save. On failure reduce its maximum HP by 2 S+M under the common non-stacking maximum-HP rule. This creates no persistent broken-limb injury; the maximum returns after a completed short or long rest without restoring current HP.", "prerequisite": null}

## monk.hero.way-of-shadow.deathless-silence

{"name": "Deathless Silence", "activation": "Action", "cost": "5 Ki + 5 RP", "rangeAndTarget": "Up to three enemies you can perceive within 60 feet", "duration": "Until start of your next regular turn; max-HP reduction until rest", "frequency": "1/long rest; automatic Hero Final", "effect": "Final — Deathless Silence. Tags: hero, shadow, final, teleportation, max-hp, weave. Until the start of your next regular turn you cannot be targeted by opportunity attacks or Reactions. Teleport adjacent to up to three different chosen enemies in sequence and make one unarmed strike against each. On each hit, the target makes a Constitution save. Failure reduces its maximum HP by 4 S+M under the common non-stacking rule and suppresses one non-core defensive passive it possesses until the end of its next turn; the Director identifies an applicable visible passive before the save. This does not disable core class engines, legendary rules or creature type traits.", "prerequisite": null}

## monk.hero.way-of-shadow.death-touch

{"name": "Death Touch", "activation": "Action", "cost": "5 Ki", "rangeAndTarget": "One creature within unarmed reach", "duration": "Instantaneous", "frequency": "1/long rest", "effect": "Death Touch. Tags: hero, shadow, attack, finisher. Make one unarmed strike. On a hit add 3 S d8 necrotic damage. If the target began the strike at or below one-quarter maximum HP, it also makes a Constitution save; on failure add another 2 S d8 necrotic damage. This never causes automatic death, bypasses no ordinary dying rules and creates no permanent injury beyond the damage actually dealt.", "prerequisite": null}

## oracle.engine[13]

Healing from Oracle features cannot exceed maximum HP, resurrect the dead or remove Wounds unless a feature explicitly says so. Temporary HP never stack. Encounter-only regeneration and drain cannot be farmed outside meaningful combat. Corpse effects create no XP, loot, RC or repeatable corpse resources unless expressly stated.

## oracle.supplement.spiral-touched.spiral-touched-boon-iii

{"name": "Spiral-Touched — Boon III", "activation": "Triggered at 0 HP", "cost": "0", "rangeAndTarget": "Self", "duration": "Until start of next regular turn", "frequency": "1/long rest", "effect": "1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations.", "prerequisite": "Oracle 10; selected Curse:Spiral-Touched"}

## oracle.supplement.wound-eater.wound-eater-boon-iii

{"name": "Wound Eater — Boon III", "activation": "Action", "cost": "0", "rangeAndTarget": "One dying hostile living creature touched", "duration": "Instantaneous", "frequency": "1/short rest; no staged/summoned targets", "effect": "1/short rest as an Action touch one dying hostile living creature at 0 HP; that creature dies and you regain HP equal to one-quarter your maximum HP rounded down. It cannot trigger from summoned, trivial or staged creatures and removes no Wounds.", "prerequisite": "Oracle 10; selected Curse:Wound Eater"}

## oracle.supplement.wound-eater.wound-eater-boon-v

{"name": "Wound Eater — Boon V", "activation": "Action", "cost": "0", "rangeAndTarget": "Up to three living enemies within 20 feet", "duration": "Instantaneous", "frequency": "1/long rest", "effect": "1/long rest as an Action, up to three meaningful living enemies within 20 feet lose HP equal to the lesser of one-quarter their maximum HP or Oracle level+M; you regain half the total actual HP lost, capped at one-half your maximum HP. Allies, constructs, undead, trivial creatures and summons are unaffected.", "prerequisite": "Oracle 20; selected Curse:Wound Eater"}

## oracle.supplement.burning-blood.burning-blood-boon-iv

{"name": "Burning Blood — Boon IV", "activation": "Triggered on first falling below half HP", "cost": "0", "rangeAndTarget": "Up to three enemies within 15 feet", "duration": "Instantaneous", "frequency": "1/short rest", "effect": "once per short rest when you first fall below half maximum HP, erupt in a 15-foot fire burst. Enemies make Dexterity saves, taking 2 S d6 fire on failure or half on success; you take no damage from this flare.", "prerequisite": "Oracle 15; selected Curse:Burning Blood"}

## oracle.supplement.false-life.false-life-boon-v

{"name": "False Life — Boon V", "activation": "Triggered at 0 HP", "cost": "0", "rangeAndTarget": "Self; undead within 15 feet", "duration": "Rise next turn; immunity two rounds", "frequency": "1/long rest", "effect": "1/long rest when you are at 0 HP but not destroyed outright, appear dead until the start of your next regular turn. During that interval you are incapacitated. At the start of your next turn rise with floor(max HP/4), minimum 1, and gain necrotic immunity for 2 rounds. Undead within 15 feet treat you as non-hostile until you damage, control or overtly oppose them. Divination during the apparent-death interval returns one false but plausible state-description you choose; it cannot fabricate events outside your own condition.", "prerequisite": "Oracle 20; selected Curse:False Life"}

## oracle.supplement.bones.death-s-threshold

{"name": "Death's Threshold", "activation": "Passive", "cost": "0 RC", "rangeAndTarget": "Self; undead enemies within 3 tiles", "duration": "Until healed above half maximum HP", "frequency": "1/short rest", "effect": "The first time after a short rest that you fall to one-quarter maximum HP or less, activate Death's Threshold. Until you are healed above half maximum HP, reduce the first necrotic damage and first nonmagical weapon damage you take each round by S and gain +1 to your Revelation save DC. Undead enemies within 3 tiles take -1 on their first attack roll against you each round. The effect then ends and cannot reactivate until after another short rest.", "prerequisite": "Oracle 6; Mystery: Bones; selected Tier II Revelation"}

## oracle.supplement.bones.ledger-unbound

{"name": "Ledger Unbound", "activation": "Action", "cost": "0 RC", "rangeAndTarget": "Enemies and up to 3 eligible corpses within 5 tiles", "duration": "Damage instantaneous; bone servants 3 rounds", "frequency": "1/long rest", "effect": "Choose up to three enemies in range. Roll 4 S d8+M once; each target takes necrotic damage equal to the lesser of that roll or one-quarter its maximum HP, with a Constitution save for half. This blast cannot reduce HP below 1. Raise up to three nonsummoned corpses as 1-HP bone servants for three rounds. Once per round spend your shared companion Bonus Action to move and attack with ONE servant using your Revelation attack bonus for 1d8+S necrotic damage. Alternatively, your Reaction may sacrifice one servant to intercept a single-target attack against you; no attack is made by that servant that round. Servants grant no XP, loot, harvestable corpses or RC. For three rounds, up to three undead you already control add S damage to their one shared commanded attack and reduce the first damage they take each round by 1. No extra creature turns or command budgets are created.", "prerequisite": "Oracle 20; Mystery: Bones"}

## oracle.supplement.flame.crown-restored

{"name": "Crown Restored", "activation": "Bonus Action", "cost": "0 RC", "rangeAndTarget": "Self and allies within 5 tiles", "duration": "3 rounds", "frequency": "1/long rest", "effect": "Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap.", "prerequisite": "Oracle 20; Mystery: Flame"}

## oracle.supplement.life.verdant-pulse

{"name": "Verdant Pulse", "activation": "Passive and Reaction", "cost": "0 RC", "rangeAndTarget": "Allies you heal; emergency ally within 4 tiles", "duration": "Buff until end of ally's next turn; emergency instantaneous", "frequency": "Buff once per ally per short rest; emergency 1/encounter", "effect": "When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it.", "prerequisite": "Oracle 6; Mystery: Life; selected Tier II Revelation"}

## oracle.supplement.time.echo-strike

{"name": "Echo Strike", "activation": "Reaction", "cost": "1 RC", "rangeAndTarget": "Same target just hit by your weapon or touch attack", "duration": "Instantaneous", "frequency": "At most once per round", "effect": "Immediately after your weapon or touch attack hits, spend 1 RC. Copy half the triggering attack's unmodified rolled damage dice total, rounded down, minimum 1, as damage of the same type to the same target. The echo is not another attack, cannot critically hit and copies no flat modifiers, conditions, resource gains or proc triggers. If this copied damage leaves the target below half maximum HP, regain 1 RC after resolution, at most once per round and never above maximum.", "prerequisite": "Oracle 3; Mystery: Time; selected Tier I Revelation"}

## oracle.supplement.time.rewind-wound

{"name": "Rewind Wound", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "One living ally you touch", "duration": "Healing instantaneous; protection until start of your next turn", "frequency": "At will while RC remains; same damage event can be rewound once", "effect": "Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects.", "prerequisite": "Oracle 6; Mystery: Time; selected Tier II Revelation"}

## paladin.supplement.oath-of-mercy.merciful-smite

{"name": "Merciful Smite", "activation": "Triggered", "cost": "Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8", "rangeAndTarget": "Creature hit by your melee weapon attack; up to 3 living allies within 10 feet of you", "duration": "Instantaneous", "frequency": "One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance", "effect": "Your Oath Smite deals radiant damage instead of adding a second Smite packet. After the Smite damage resolves, create a healing pool equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Divide that pool among up to 3 living allies within 10 feet. Healing cannot exceed maximum HP, remove Wounds or trigger additional Smite or healing-copy effects.", "prerequisite": "Paladin 3; Oath of Mercy"}

## paladin.supplement.oath-of-mercy.blessing-of-the-meek

{"name": "Blessing of the Meek", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "One living ally within 30 feet", "duration": "Healing instantaneous; AC bonus until start of your next regular turn", "frequency": "At will while RP remains", "effect": "The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules.", "prerequisite": "Paladin 3; Oath of Mercy"}

## paladin.supplement.oath-of-mercy.channel-life

{"name": "Channel Life", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "Self and one living ally within 30 feet", "duration": "Instantaneous", "frequency": "At will while RP remains", "effect": "Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.", "prerequisite": "Paladin 9; Oath of Mercy"}

## paladin.supplement.oath-of-vengeance.final-verdict

{"name": "Final Verdict", "activation": "Action", "cost": "10 RP", "rangeAndTarget": "One creature marked by you within 30 feet and at or below half maximum HP", "duration": "Instantaneous or empowerment until end of your next regular turn", "frequency": "At will while RP remains", "effect": "The marked target makes a Constitution save, taking 4 S d8 radiant damage on failure or half on success. On failure it also cannot regain HP until the end of its next turn. If that damage reduces it to 0 HP, use ordinary Downed/death rules; there is no percentage-HP execution. On success your next Smite against it before the end of your next turn uses maximum damage dice. This bounded damage replaces the source draft’s automatic reduction to 0 HP.", "prerequisite": "Paladin 17; Oath of Vengeance"}

## paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution

{"name": "Death Touch — Malicious Execution", "activation": "Action", "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss", "rangeAndTarget": "One creature within melee reach", "duration": "Instantaneous", "frequency": "At will while Lay on Hands points remain; rider once per turn", "effect": "Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared Lay on Hands points. If the target was already at or below half maximum HP, it makes a Constitution save; on failure add S d6 necrotic damage. This rider never automatically executes or bypasses normal death rules.", "prerequisite": "Paladin 3; Oathbreaker — Oath of Vengeance"}

## paladin.supplement.oathbreaker-oath-of-vengeance.fearbrand

{"name": "Fearbrand", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "Up to 3 enemies in your Oath aura", "duration": "Damage instantaneous; Frightened until end of next turn", "frequency": "1/short rest; replaces Signature Power use", "effect": "Each target makes a Wisdom save. On failure it takes 2 S d6 psychic damage and is Frightened until the end of its next turn; on success it takes half damage and is not Frightened. A target already below half maximum HP takes one additional d6 psychic damage. This creates no execution effect.", "prerequisite": "Paladin 11; Oathbreaker — Oath of Vengeance"}

## paladin.supplement.oath-of-the-martyr-king.crown-undying

{"name": "Crown Undying", "activation": "Bonus Action", "cost": "0 RP", "rangeAndTarget": "Up to three selected allies in your aura", "duration": "Three rounds; no concentration", "frequency": "1/long rest", "effect": "For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.", "prerequisite": "Paladin 20; Oath of the Martyr King"}

## shaman.hero.bloodcaller.talon-strike

{"name": "Talon Strike", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "One enemy in claw reach", "duration": "Instant; reduction until end next turn", "frequency": "Recharge 2", "effect": "Make one claw attack; hit adds S d6 necrotic and reduces the next healing it receives by M, minimum 0. Applies once and ends. No arbitrary percent stacking or permanent maximum-HP reduction.", "prerequisite": null}

## tinker.hero.artificer.repair-pulse

{"name": "Repair Pulse", "activation": "Action", "cost": "3 RP", "rangeAndTarget": "Upto 3 friendly devices within 30 ft", "duration": "Instant; AC until start next turn", "frequency": "1/short rest", "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.", "prerequisite": null}

## tinker.hero.techsmith.snap-rebuild

{"name": "Snap Rebuild", "activation": "Bonus Action", "cost": "2 RP; 1 encounter use", "rangeAndTarget": "One destroyed device/drone within 15 ft", "duration": "Remaining original duration", "frequency": "1/encounter", "effect": "Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock.", "prerequisite": null}

## warrior.engine[8]

BRUTALITY PROGRESS. Begin each real encounter with Brutality Progress 0 and BT 0. Add actual damage you personally deal to meaningful hostile creatures to Brutality Progress, but a single damage event contributes no more than one-quarter of your maximum HP. Crossing cumulative thresholds equal to 25%, 50% and 75% of your maximum HP grants 1 BT each, subject to the BT cap. Crossing 100% triggers Transcendent as described below but does not create a fourth stored BT unless Stack Overflow or another feature raises the cap.

## warrior.engine[15]

HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT.

## warrior.base.brutality-sense

{"name": "Brutality Sense", "activation": "Passive", "cost": "0", "rangeAndTarget": "Hostile creatures you can perceive within 60 feet", "duration": "While condition remains true", "frequency": "Always", "effect": "Brutality Sense. You know when a visible hostile creature is at or below one-quarter of its maximum HP; it is Vulnerable for your Warrior features that specifically reference a marked vulnerable target. This does not reveal its exact HP or hidden resistances.", "prerequisite": null}

## warrior.hero.ironskin.regenerative-mutation

{"name": "Regenerative Mutation", "activation": "Passive", "cost": "Spend healing amount from Mutation Recovery Reserve", "rangeAndTarget": "Self", "duration": "While at least one mutation is active in a real encounter", "frequency": "Once at the start of each regular turn", "effect": "Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.", "prerequisite": null}

## warrior.hero.dreadspawn.pain-empowerment

{"name": "Pain Empowerment", "activation": "Passive", "cost": "0", "rangeAndTarget": "Self", "duration": "While below maximum HP", "frequency": "Always", "effect": "Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects.", "prerequisite": null}

## warrior.supplement.flesh-warden

{"name": "Flesh Warden", "activation": "Passive while equipped", "cost": "One mutation slot", "rangeAndTarget": "Self", "duration": "While equipped", "frequency": "Mutation", "effect": "Increase maximum HP by 2 per Warrior level while equipped. Equipping raises maximum only, never current HP. Unequipping clamps current HP to the reduced maximum if necessary; it does not subtract another amount from current HP. Repeated swaps cannot heal.", "prerequisite": "Warrior 1; Basic Vital"}

## warrior.supplement.adrenal-floodgate

{"name": "Adrenal Floodgate", "activation": "Triggered while active", "cost": "One mutation slot; serum activation", "rangeAndTarget": "Self", "duration": "Instantaneous", "frequency": "1/encounter", "effect": "When you first fall to one-quarter maximum HP or less, regain 2d8 HP and end either Frightened, Poisoned or Staggered on yourself.", "prerequisite": "Warrior 6; Advanced Vital"}

## warrior.supplement.mythic-carapace

{"name": "Mythic Carapace", "activation": "Passive while active", "cost": "One mutation slot; serum activation", "rangeAndTarget": "Self", "duration": "Until encounter ends, mutation ends or you fall below one-quarter maximum HP", "frequency": "Apex mutation", "effect": "Gain DR 3 against all damage and immunity to Bleed, Poisoned and Burn-style ongoing fire effects. Once per encounter when one hit deals more than 20 actual damage after mitigation, gain 1 BT and refresh the remaining duration of your other active mutations to 3 rounds. It grants no serum-profile refresh.", "prerequisite": "Warrior 15; Apex Vital; maximum one Apex equipped"}

## warrior.supplement.butcherform-chassis

{"name": "Butcherform Chassis", "activation": "Passive while active", "cost": "One mutation slot; serum activation", "rangeAndTarget": "Self", "duration": "3 rounds or until below one-quarter maximum HP", "frequency": "Apex mutation", "effect": "When you take the ordinary Attack action, make one additional melee attack beyond other Extra Attack effects, respecting the one-additional-full-Action guard because this is part of the same Action. Your melee criticals add one extra weapon damage die beyond normal critical dice, not triple total damage. Once per round when you personally kill a meaningful hostile with a melee attack, restore one consumed prepared serum dose, never above reserve capacity.", "prerequisite": "Warrior 15; Apex Combat; maximum one Apex equipped"}

## wizard.engine[10]

ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn.

## wizard.engine[24]

Flesh Ascendant's bonus applies after the listed base statistics: every undead creature you control gains +2 maximum HP per Wizard level. If at least two of your undead creatures are active, each gains +1 AC and +1 on saving throws. This does not increase the standard-minion or elite-pet caps.

## wizard.hero.necromancer.flesh-ascendant

{"name": "Flesh Ascendant", "activation": "Passive", "cost": "0", "rangeAndTarget": "Undead creatures you control", "duration": "Permanent while active", "frequency": "Always", "effect": "Flesh Ascendant. Tags: hero, necromancer, passive, undead. Each undead creature you control gains +2 maximum HP per Wizard class level. While at least two of your undead creatures are active, each also gains +1 AC and +1 on saving throws. These bonuses apply after the common standard-minion and elite-pet statistics and do not increase companion caps or command frequency.", "prerequisite": null}

## feat:exploit_weakness

{"id": "exploit_weakness", "name": "Exploit Weakness", "description": "At level 7, a combatant seeks wounded enemies for the listed critical chance.", "prerequisite": "Level 7", "effect": "Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.", "type": "Combat", "legacyEffect": "+15% crit on wounded enemies", "status": "provisional-complete", "balanceReview": true, "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.", "draft": false, "deprecated": false, "needsReview": true}

## feat:familiar_bond

{"id": "familiar_bond", "name": "Familiar Bond", "description": "Your bond with your familiar is stronger.", "prerequisite": "Ability to cast find familiar", "effect": "Your familiar gains hit points equal to your level and can attack using your spell attack bonus.", "type": "Magic", "draft": false, "deprecated": false, "needsReview": false}

## feat:tenacity

{"id": "tenacity", "name": "Tenacity", "description": "Level 4 supports the listed +1 HP per level.", "prerequisite": "Level 4", "effect": "Your hit point maximum increases by 1 for each character level, including levels already gained.", "type": "General", "legacyEffect": "+1 HP per level", "status": "provisional-complete", "balanceReview": true, "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.", "draft": false, "deprecated": false, "needsReview": true}

## feat:tough

{"id": "tough", "name": "Tough", "description": "Your hit point maximum increases.", "prerequisite": "None", "effect": "Your hit point maximum increases by an amount equal to twice your level when you gain this feat.", "type": "General", "draft": false, "deprecated": false, "needsReview": false}

## feat:tough_as_nails

{"id": "tough_as_nails", "name": "Tough as Nails", "description": "Level 5 supports the listed +10% maximum HP.", "prerequisite": "Level 5", "effect": "Your hit point maximum increases by 2 per character level when you take this feat, and by 2 whenever you gain a level thereafter.", "type": "General", "legacyEffect": "+10% max HP", "status": "provisional-complete", "balanceReview": true, "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.", "draft": false, "deprecated": false, "needsReview": true}

## feat:dark_fortitude

{"id": "dark_fortitude", "name": "Dark Fortitude", "description": "Grave-cold and poison have tried to claim you. They learned your name and backed away. Prestige lineage: Gravetouched. completed from the existing development record.)", "prerequisite": "Constitution 15+", "effect": "You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest). While below half your hit point maximum, you have resistance to poison damage.", "type": "General", "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.", "legacyEffect": "You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest). While below half your hit point maximum, you have resistance to poison damage.", "status": "provisional-complete", "balanceReview": true, "draft": false, "deprecated": false, "needsReview": true}

## feat:life_drinker

{"id": "life_drinker", "name": "Life Drinker", "description": "Every wound you open is a cup. You drink and stand taller. Prestige lineage: Bloodbound. completed from the existing development record.)", "prerequisite": "Dark Affinity or Hemocraft", "effect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.", "type": "Combat", "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.", "legacyEffect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.", "status": "provisional-complete", "balanceReview": true, "draft": false, "deprecated": false, "needsReview": true}

## Already reviewed tools/strain_playtest_rules.py

def combined_maximum_hp(base_maximum, *, expedition, exhaustion, other_factors=()):
    integer(base_maximum,'otherwise applicable maximumHP',1)
    integer(expedition,'Expedition Strain',0,6)
    integer(exhaustion,'Exhaustion',0,6)
    value=Fraction(base_maximum)
    for factor in other_factors:
        factor=Fraction(factor)
        if factor<=0:
            raise SpellRuleError('MaximumHP multiplier must be positive')
        value*=factor
    if expedition>=4:
        value*=Fraction(3,4)
    if exhaustion>=4:
        value*=Fraction(1,2)
    return max(1,value.numerator//value.denominator)


def apply_effective_maximum(life, maximum):
    integer(maximum,'effective maximumHP',1)
    return replace(life,maximum_hp=maximum,hp=min(life.hp,maximum))




## Already reviewed docs/mechanics/STRAIN_PLAYTEST.md

| 4 | Effective maximum HP×3/4 |
Represent each point with `pointId`, `sourceId`, `ordinaryRemovable` and `removalGateMet`. Level is the active count, maximum6. Keep source history and attempted overflow even when no additional point can be stored. A generic recovery can select only points that are ordinary-removable **and** whose gate is met. A specific treatment can override only the source it expressly covers. Clearing a gate updates metadata; it does not silently delete a point.
## Independent penalties and maximum HP
NEW maximum-HP composition: multiply applicable rational factors against the same otherwise-applicable maximum, floor **once**, minimum1. Expedition4×3/4 and Exhaustion4×1/2 produce37 from base100. Clamp currentHP down if necessary; that clamp is not damage and triggers no Wound, death-save failure or damage resource. Removing a modifier raises capacity without healing/resetting death counters. Critical Wounds' healing ceiling then uses `max(1, effectiveMaximumHP−1)`; it is not another maxHP multiplier.
The [validation report](STRAIN_PLAYTEST_VALIDATION.json) records71 transition checks,30 exact source checks and4,949 maximum-HP invariant states. Broader rest rewards, travel, all-source class semantics, future Strain references, resurrection and human balance remain open.