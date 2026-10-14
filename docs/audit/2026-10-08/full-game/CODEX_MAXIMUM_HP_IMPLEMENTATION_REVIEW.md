# Exact maximumHP implementation review

Codex → Calibration Review. Please reply below15,000 characters. Review the exact helper, tests, guide and58 role bindings below against your source discussion and five boundary corrections. Current60checks/909systemicstatesPASS;58sourcehashes/liveobjects match. Challenge concrete defects before boundedclosure.

Implemented: unmodifiedbase+compatiblebonuses−GLOBALstrongestMonk then rationalfactorproduct flooronce; max/currentclamp non-damage; independent application clocks/suppression/targetrest; sameFleshAscendantengine/cardidentity; explicitNEWWizardstackexception; Conjurationcreationlevelsnapshot; dynamicotherbonusformulas; Toughacquisitionsnapshot; strictfirstfallcrossingsusingeventmax; genuinehealed-abovehalfexit; historicalRewindpredicate; percentageamountswithsourceownedminimum; priorCoreWound/HP/concentrationmetricsfrozenbeforeMonktrauma.

Caller boundary: record numericamount must be built from a legal actualsource/formula and eligibility; helper doesnotinferownership/control/equipment/acquisition, performcompanioncreation, payactions/costs, generateclockmarkers, consume firstfalluses orrefillHP. Source_amount computes documentedformulas andcallerrefreshesdynamicbonuseswhenlevelchanges. A record's suppliedearlierendpoint is allowed ONLYif anotheractualsource providesit; no invented earlierend for theseMonkcards. Preserverest-endingrecords evenwhensuppressed; do notmergeseparateapplications.

Narrow predicatecheck: HpEventSnapshot.damage_left_below_half for Rewind means realHPdamagedecrease leavingrecordedtargetbelowhalf, notnecessarilycrossingfromabove. Its source says 'if recorded damage had reduced it below half' without 'first fall'; broaderearlierhealinginterface didnotrequirefirstcrossing. Confirm orcorrectthisprecisedifference fromfourfirstfallcards.

The58recordscope includesguards,percentages andthresholds; itdoesnotpromoteentireLifeDrinker/familiar/featclass engines. Otherdomainsincludingallunsuppliedmodifiers,devicehalfmax1viability,levelupbaseHP/multiclassconstitution,companionlife/control,featretraining andrealbalance remainopen.


## Exact58 role bindings

{
  "status": "IN_PROGRESS",
  "scope": "Selected58-source maximumHP/threshold interface. Includes guards/exclusions and prior reviewed percentage healing; no complete feat/companion/character build promotion.",
  "bindings": [
    {
      "bindingId": "cleric.engine[7]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": 7,
      "sourceSha256": "bb84e1b0f1d02ca1f307edee719b2e66036799f2367b1b93511681a7f95dd455",
      "sourceProcedure": {
        "text": "Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD",
      "operationalOverrides": [
        "Healing/max-HP ceiling guard; no modifier."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.arch.anointed-guardian",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.arch.anointed-guardian",
      "sourceSha256": "27c6e65cd16abe41a61a71f92375691fce8d8a5255f3d238b1ab8d44699d1ac5",
      "sourceProcedure": {
        "name": "Anointed Guardian",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "First ally within 30 feet to fall to one-quarter maximum HP or less",
        "duration": "2 rounds",
        "frequency": "Once per encounter",
        "effect": "Anointed Guardian. Tags: protection, bishop. The first qualifying ally in an encounter gains a ward for 2 rounds. The first time during each round that ally takes damage, reduce that damage by PB + M, minimum 0. The ward does not prevent conditions attached to an attack unless the damage reduction itself invalidates them under another rule.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_CROSSING",
      "operationalOverrides": [
        "First genuine fall to ≤quarter; max-only change does not trigger."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.hero.saint.aura-of-grace",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.saint.aura-of-grace",
      "sourceSha256": "7dff7e8271aba866c1b596528fe2e7d1e3f9a1558eeec233922585461bcc9854",
      "sourceProcedure": {
        "name": "Aura of Grace",
        "activation": "Triggered and passive",
        "cost": "1 RP per healing pulse",
        "rangeAndTarget": "Living allies within 15 feet",
        "duration": "Passive during real encounters",
        "frequency": "Healing once/own regular turn; critical reduction once/ally/round",
        "effect": "Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_HEAL_ELIGIBILITY",
      "operationalOverrides": [
        "Below-half checked at pulse target selection."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.hero.saint.divine-rebirth",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.saint.divine-rebirth",
      "sourceSha256": "0911a56a90621bfce24642033cfd99929553c077fa641efacc48d90d4b94e15a",
      "sourceProcedure": {
        "name": "Divine Rebirth",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "One ally revived by your Cleric feature",
        "duration": "Instantaneous plus temporary HP for 1 minute",
        "frequency": "1/long rest",
        "effect": "Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_RESURRECTION_HP",
      "operationalOverrides": [
        "Half effective max at return; reviewed viable-return min1 applies."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.hero.saint.merciful-sacrament",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.saint.merciful-sacrament",
      "sourceSha256": "1839de6107b950771344a8a77e0c9c45ad81b114131b0969eafab0335a14c466",
      "sourceProcedure": {
        "name": "Merciful Sacrament",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your Sacrament",
        "duration": "For that activation",
        "frequency": "1/short rest",
        "effect": "Merciful Sacrament. Tags: saint, sacrament. When you start Sacrament and at least one living ally inside its initial zone is at or below one-quarter maximum HP, you may reduce that Sacrament's Conviction cost to 0. Its RP cost and all other requirements remain. Because no Conviction is spent, this waived cost does not vent Dissonance.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_COST_GATE",
      "operationalOverrides": [
        "Initial-zone ally ≤quarter snapshot when Sacrament starts."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.hero.saint.unyielding-light",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.saint.unyielding-light",
      "sourceSha256": "2b13f1c09c2c7fba28eb3ac046a34ff52f8a829eafac020aa33b762a96d4236d",
      "sourceProcedure": {
        "name": "Unyielding Light",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "Up to six living party members within 30 feet, including you",
        "duration": "Instantaneous",
        "frequency": "1/long rest",
        "effect": "Unyielding Light. Tags: saint, emergency, healing. When one damage event would leave every conscious living party member within 30 feet at 0 HP, resolve that damage, then before ordinary death-save progression each qualifying living creature at 0 HP regains floor(maximum HP/3), minimum 1. It cannot revive a creature killed outright and removes no Wounds. This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_ZERO_HP_RECOVERY",
      "operationalOverrides": [
        "`max(1,floor(max/3))`."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.hero.saint.mass-healing-light",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.saint.mass-healing-light",
      "sourceSha256": "dbb502b5ecb5d64d0973a9df82f770cdb8af28300d09a7f6f978d3fef13c2009",
      "sourceProcedure": {
        "name": "Mass Healing Light",
        "activation": "Action",
        "cost": "5 RP",
        "rangeAndTarget": "Up to six living allies within 30 feet",
        "duration": "Instantaneous",
        "frequency": "Recharge 3 rounds",
        "effect": "Mass Healing Light. Tags: saint, healing. Roll S d8 + M once. Each target regains that amount. A target below half maximum HP when chosen regains an additional 1d8 HP. Roll that bonus once and apply it to all qualifying targets. This cannot revive the dead or remove Wounds.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_HEAL_BONUS",
      "operationalOverrides": [
        "Below-half snapshot when target chosen."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.corrupt-divinity",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.corrupt-divinity",
      "sourceSha256": "b28343e6f696458ef1e0ca49d5529644e610a9603e84b09db58e597f2157e258",
      "sourceProcedure": {
        "name": "Corrupt Divinity",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "One enemy within 60 feet",
        "duration": "Maximum 2 rounds",
        "frequency": "Recharge 3 rounds",
        "effect": "Corrupt Divinity. Tags: cultist, debuff, control. The target makes a Wisdom save. On failure it takes -1 on attack rolls and saving throws. It repeats the save at the end of each turn, ending the effect on success. If a non-player NPC at or below one-quarter maximum HP fails the initial save by 10 or more, it is also Charmed by you until the end of its next turn. This never permanently converts allegiance, changes beliefs or overrides a player character's agency.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_CONTROL",
      "operationalOverrides": [
        "NPC ≤quarter checked at initial resolution."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "dragoon.hero.dragon-guardian.wyrmhide",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/dragoon.json",
      "sourceId": "dragoon.hero.dragon-guardian.wyrmhide",
      "sourceSha256": "f514ad790b1d4e61a1120eaa22c47fb6bfaab9218c5c4ef84af5c2a503898d7d",
      "sourceProcedure": {
        "name": "Wyrmhide",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self while above half maximum HP",
        "duration": "While threshold met",
        "frequency": "Continuous",
        "effect": "Reduce each damage instance by 2 and gain advantage on CON saves against Bleed, Burn and Poisoned. No blanket condition immunity; effects already present persist and ordinary nonstacking reduction applies.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "CONTINUOUS_THRESHOLD",
      "operationalOverrides": [
        "Above-half predicate recomputes with effective max."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "mage.hero.lich.flesh-to-ash",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mage.json",
      "sourceId": "mage.hero.lich.flesh-to-ash",
      "sourceSha256": "e6eb8ad0d964f777becfb64a89c2f8e3b5c3a23a72106c61afecf2386623c243",
      "sourceProcedure": {
        "name": "Flesh to Ash",
        "activation": "Action",
        "cost": "5 RP",
        "rangeAndTarget": "15-foot-radius sphere centered at a point within 60 feet",
        "duration": "Instantaneous",
        "frequency": "Recharge 3 rounds",
        "effect": "Flesh to Ash. Tags: mage-spell, lich, necrotic, damage. Creatures of your choice in the area make Constitution saves. A target at half maximum HP or more takes S d8 necrotic on failure, half on success. A target below half maximum HP instead takes 2 S d8 necrotic on failure, half on success. Determine the threshold before rolling damage.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_DAMAGE",
      "operationalOverrides": [
        "Explicit pre-damage half snapshot."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "mage.hero.lich.soulbound-ritual",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mage.json",
      "sourceId": "mage.hero.lich.soulbound-ritual",
      "sourceSha256": "402e1f7d3575a535865294094b40a0e028c23dff18e64dadc511f20340bc7b0a",
      "sourceProcedure": {
        "name": "Soulbound Ritual",
        "activation": "Action",
        "cost": "5 RP",
        "rangeAndTarget": "One of your destroyed bound elite undead companions within 30 feet or its inert binding token",
        "duration": "Instantaneous",
        "frequency": "1/long rest",
        "effect": "Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_COMPANION_RECONSTRUCTION",
      "operationalOverrides": [
        "Returns companion at half effective max; wider companion lifecycle open."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "monk.engine[9]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": 9,
      "sourceSha256": "e3923490d9849612190a0954ff0749b6e2517862bdfb1c2d7b5dbdfcff1e2eb7",
      "sourceProcedure": {
        "text": "Temporary maximum-HP reductions caused by Monk features do not stack on the same creature; use the largest reduction from your Monk features. Maximum HP cannot be reduced below 1. Unless a card specifies an earlier end, the reduction lasts until the creature completes a short or long rest. Restoring maximum HP does not restore current HP. These effects are temporary combat trauma, not unstated permanent injuries."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_REDUCTION_ENGINE",
      "operationalOverrides": [
        "Global strongest operative Monk trauma; separate records/clocks."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "monk.engine[16]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": 16,
      "sourceSha256": "35f0120ff484cecb5d18360f6532891d2de393ba4d2b5e03a9961b7e2ab07a44",
      "sourceProcedure": {
        "text": "Healing from Monk cards cannot exceed maximum HP, restore the dead or remove Wounds unless explicitly stated. Permanent HP recovery and Ki generation cannot be farmed outside encounters. Resurrection effects are explicitly limited-use. No Monk card can instantly kill a target merely because a descriptive source used language such as Death Touch; death continues to follow the game's ordinary damage and dying rules."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD",
      "operationalOverrides": [
        "Healing/death guard only."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "monk.hero.iron-fist-master.ribcrusher-strike",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.iron-fist-master.ribcrusher-strike",
      "sourceSha256": "11eb73eb0d8587fb3a965d0b24386deb32cde0270d51810eec36cd841fdcc077",
      "sourceProcedure": {
        "name": "Ribcrusher Strike",
        "activation": "Triggered",
        "cost": "2 Ki",
        "rangeAndTarget": "One creature hit by your unarmed strike",
        "duration": "Until target completes a short or long rest",
        "frequency": "Once per target per encounter",
        "effect": "Ribcrusher Strike. Tags: hero, iron-fist, attack, max-hp. After an unarmed strike hits, spend 2 Ki. The target makes a Constitution save. On failure reduce its maximum HP by S+M, minimum maximum HP 1. This reduction follows the common non-stacking maximum-HP rule and is restored after a completed short or long rest without restoring current HP.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_REDUCTION",
      "operationalOverrides": [
        "−(S+M), after attack damage, until completed rest."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "monk.hero.iron-fist-master.bone-breaking-strike",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.iron-fist-master.bone-breaking-strike",
      "sourceSha256": "be603265c88626d789efc7c940a4151d6201a7dd4548f0d8dd7b516afed85fc8",
      "sourceProcedure": {
        "name": "Bone-Breaking Strike",
        "activation": "Action",
        "cost": "2 Ki",
        "rangeAndTarget": "One creature within unarmed reach",
        "duration": "Until target completes a short or long rest",
        "frequency": "Recharge 3 rounds",
        "effect": "Bone-Breaking Strike. Tags: hero, iron-fist, attack, max-hp. Make one unarmed strike. On a hit, the target makes a Constitution save. On failure reduce its maximum HP by 2 S+M under the common non-stacking maximum-HP rule. This creates no persistent broken-limb injury; the maximum returns after a completed short or long rest without restoring current HP.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_REDUCTION",
      "operationalOverrides": [
        "−(2S+M), after attack damage."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "monk.hero.way-of-shadow.deathless-silence",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.way-of-shadow.deathless-silence",
      "sourceSha256": "a23f961c0455ab3ceeaf270e1f5493914a4d5c257841e084367c9bfc8cd7d1dd",
      "sourceProcedure": {
        "name": "Deathless Silence",
        "activation": "Action",
        "cost": "5 Ki + 5 RP",
        "rangeAndTarget": "Up to three enemies you can perceive within 60 feet",
        "duration": "Until start of your next regular turn; max-HP reduction until rest",
        "frequency": "1/long rest; automatic Hero Final",
        "effect": "Final — Deathless Silence. Tags: hero, shadow, final, teleportation, max-hp, weave. Until the start of your next regular turn you cannot be targeted by opportunity attacks or Reactions. Teleport adjacent to up to three different chosen enemies in sequence and make one unarmed strike against each. On each hit, the target makes a Constitution save. Failure reduces its maximum HP by 4 S+M under the common non-stacking rule and suppresses one non-core defensive passive it possesses until the end of its next turn; the Director identifies an applicable visible passive before the save. This does not disable core class engines, legendary rules or creature type traits.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_REDUCTION + OTHER",
      "operationalOverrides": [
        "−(4S+M); defensive-passive suppression has separate shorter clock."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "monk.hero.way-of-shadow.death-touch",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.way-of-shadow.death-touch",
      "sourceSha256": "a3a0f7f23883eb6888e379b73620f29e0f12f9945c1d6a4afd376038a342e8ea",
      "sourceProcedure": {
        "name": "Death Touch",
        "activation": "Action",
        "cost": "5 Ki",
        "rangeAndTarget": "One creature within unarmed reach",
        "duration": "Instantaneous",
        "frequency": "1/long rest",
        "effect": "Death Touch. Tags: hero, shadow, attack, finisher. Make one unarmed strike. On a hit add 3 S d8 necrotic damage. If the target began the strike at or below one-quarter maximum HP, it also makes a Constitution save; on failure add another 2 S d8 necrotic damage. This never causes automatic death, bypasses no ordinary dying rules and creates no permanent injury beyond the damage actually dealt.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_DAMAGE",
      "operationalOverrides": [
        "≤quarter snapshot at strike start."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.engine[13]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": 13,
      "sourceSha256": "915b1cf2d9327231bf75308605d2e2b72abdce2ce052fdecef493dea663af705",
      "sourceProcedure": {
        "text": "Healing from Oracle features cannot exceed maximum HP, resurrect the dead or remove Wounds unless a feature explicitly says so. Temporary HP never stack. Encounter-only regeneration and drain cannot be farmed outside meaningful combat. Corpse effects create no XP, loot, RC or repeatable corpse resources unless expressly stated."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD",
      "operationalOverrides": [
        "Healing/max ceiling only."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.spiral-touched.spiral-touched-boon-iii",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.spiral-touched.spiral-touched-boon-iii",
      "sourceSha256": "a6358be2e17db52d461c11e2df79d972481dba2c95ebd29ecd7c31a02987d377",
      "sourceProcedure": {
        "name": "Spiral-Touched — Boon III",
        "activation": "Triggered at 0 HP",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Until start of next regular turn",
        "frequency": "1/long rest",
        "effect": "1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations.",
        "prerequisite": "Oracle 10; selected Curse:Spiral-Touched"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_DIRECT_RECOVERY",
      "operationalOverrides": [
        "Quarter effective max, source min1."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.wound-eater.wound-eater-boon-iii",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.wound-eater.wound-eater-boon-iii",
      "sourceSha256": "d872f36ef75cc9ff431e85c49d7cbfe85cf4b41721c46042c12d9e8af47fea5b",
      "sourceProcedure": {
        "name": "Wound Eater — Boon III",
        "activation": "Action",
        "cost": "0",
        "rangeAndTarget": "One dying hostile living creature touched",
        "duration": "Instantaneous",
        "frequency": "1/short rest; no staged/summoned targets",
        "effect": "1/short rest as an Action touch one dying hostile living creature at 0 HP; that creature dies and you regain HP equal to one-quarter your maximum HP rounded down. It cannot trigger from summoned, trivial or staged creatures and removes no Wounds.",
        "prerequisite": "Oracle 10; selected Curse:Wound Eater"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_HEAL",
      "operationalOverrides": [
        "`floor(selfMax/4)`; no min1."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.wound-eater.wound-eater-boon-v",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.wound-eater.wound-eater-boon-v",
      "sourceSha256": "76d3f99606a9bb0c358f108d5dba7577ecaa8580e0aef97ef94b235e8dbb4811",
      "sourceProcedure": {
        "name": "Wound Eater — Boon V",
        "activation": "Action",
        "cost": "0",
        "rangeAndTarget": "Up to three living enemies within 20 feet",
        "duration": "Instantaneous",
        "frequency": "1/long rest",
        "effect": "1/long rest as an Action, up to three meaningful living enemies within 20 feet lose HP equal to the lesser of one-quarter their maximum HP or Oracle level+M; you regain half the total actual HP lost, capped at one-half your maximum HP. Allies, constructs, undead, trivial creatures and summons are unaffected.",
        "prerequisite": "Oracle 20; selected Curse:Wound Eater"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_HP_LOSS + HEAL_CAP",
      "operationalOverrides": [
        "Target quarter-max loss; self half-max recovery cap."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.burning-blood.burning-blood-boon-iv",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.burning-blood.burning-blood-boon-iv",
      "sourceSha256": "eaa7b943b6aa64f2d9052ff86f01a0ef136baa2ad2fccd5fe895fe14f29233c7",
      "sourceProcedure": {
        "name": "Burning Blood — Boon IV",
        "activation": "Triggered on first falling below half HP",
        "cost": "0",
        "rangeAndTarget": "Up to three enemies within 15 feet",
        "duration": "Instantaneous",
        "frequency": "1/short rest",
        "effect": "once per short rest when you first fall below half maximum HP, erupt in a 15-foot fire burst. Enemies make Dexterity saves, taking 2 S d6 fire on failure or half on success; you take no damage from this flare.",
        "prerequisite": "Oracle 15; selected Curse:Burning Blood"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_CROSSING",
      "operationalOverrides": [
        "Genuine first fall strictly below half."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.false-life.false-life-boon-v",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.false-life.false-life-boon-v",
      "sourceSha256": "aca1096e9676527d4009472fd552ae219dc3cf6a5196f4ac4ad30a5c7e064b0b",
      "sourceProcedure": {
        "name": "False Life — Boon V",
        "activation": "Triggered at 0 HP",
        "cost": "0",
        "rangeAndTarget": "Self; undead within 15 feet",
        "duration": "Rise next turn; immunity two rounds",
        "frequency": "1/long rest",
        "effect": "1/long rest when you are at 0 HP but not destroyed outright, appear dead until the start of your next regular turn. During that interval you are incapacitated. At the start of your next turn rise with floor(max HP/4), minimum 1, and gain necrotic immunity for 2 rounds. Undead within 15 feet treat you as non-hostile until you damage, control or overtly oppose them. Divination during the apparent-death interval returns one false but plausible state-description you choose; it cannot fabricate events outside your own condition.",
        "prerequisite": "Oracle 20; selected Curse:False Life"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_DELAYED_RECOVERY",
      "operationalOverrides": [
        "Quarter effective max at due start, min1."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.bones.death-s-threshold",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.bones.death-s-threshold",
      "sourceSha256": "7e8778eca9a8b8ee70ff366b67e6fd5f43aa3b5aae72cc6d5815df0f86e4abff",
      "sourceProcedure": {
        "name": "Death's Threshold",
        "activation": "Passive",
        "cost": "0 RC",
        "rangeAndTarget": "Self; undead enemies within 3 tiles",
        "duration": "Until healed above half maximum HP",
        "frequency": "1/short rest",
        "effect": "The first time after a short rest that you fall to one-quarter maximum HP or less, activate Death's Threshold. Until you are healed above half maximum HP, reduce the first necrotic damage and first nonmagical weapon damage you take each round by S and gain +1 to your Revelation save DC. Undead enemies within 3 tiles take -1 on their first attack roll against you each round. The effect then ends and cannot reactivate until after another short rest.",
        "prerequisite": "Oracle 6; Mystery: Bones; selected Tier II Revelation"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_CROSSING + HEALED_EXIT",
      "operationalOverrides": [
        "Trigger by genuine fall ≤quarter; exit requires actual heal to >half."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.bones.ledger-unbound",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.bones.ledger-unbound",
      "sourceSha256": "ef4172a86bb7ab4929f1689d7d0ae148634a6fc06e32b00d1d601ef71bea270f",
      "sourceProcedure": {
        "name": "Ledger Unbound",
        "activation": "Action",
        "cost": "0 RC",
        "rangeAndTarget": "Enemies and up to 3 eligible corpses within 5 tiles",
        "duration": "Damage instantaneous; bone servants 3 rounds",
        "frequency": "1/long rest",
        "effect": "Choose up to three enemies in range. Roll 4 S d8+M once; each target takes necrotic damage equal to the lesser of that roll or one-quarter its maximum HP, with a Constitution save for half. This blast cannot reduce HP below 1. Raise up to three nonsummoned corpses as 1-HP bone servants for three rounds. Once per round spend your shared companion Bonus Action to move and attack with ONE servant using your Revelation attack bonus for 1d8+S necrotic damage. Alternatively, your Reaction may sacrifice one servant to intercept a single-target attack against you; no attack is made by that servant that round. Servants grant no XP, loot, harvestable corpses or RC. For three rounds, up to three undead you already control add S damage to their one shared commanded attack and reduce the first damage they take each round by 1. No extra creature turns or command budgets are created.",
        "prerequisite": "Oracle 20; Mystery: Bones"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_DAMAGE_CAP",
      "operationalOverrides": [
        "Damage ≤floor(targetMax/4), then save; cannot reduce below1."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.flame.crown-restored",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.flame.crown-restored",
      "sourceSha256": "354e4fb2b53a1b46b121c1edc36df4e364f0dbf66931fa7bdb453e68d6f3ab8f",
      "sourceProcedure": {
        "name": "Crown Restored",
        "activation": "Bonus Action",
        "cost": "0 RC",
        "rangeAndTarget": "Self and allies within 5 tiles",
        "duration": "3 rounds",
        "frequency": "1/long rest",
        "effect": "Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap.",
        "prerequisite": "Oracle 20; Mystery: Flame"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD",
      "operationalOverrides": [
        "Healing capped by ordinary maximum; no max modifier."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.verdant-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.verdant-pulse",
      "sourceSha256": "feb0f82538549fb2d540cfa9a68b89f517d4f1138b44ade546065fc7300c24f9",
      "sourceProcedure": {
        "name": "Verdant Pulse",
        "activation": "Passive and Reaction",
        "cost": "0 RC",
        "rangeAndTarget": "Allies you heal; emergency ally within 4 tiles",
        "duration": "Buff until end of ally's next turn; emergency instantaneous",
        "frequency": "Buff once per ally per short rest; emergency 1/encounter",
        "effect": "When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it.",
        "prerequisite": "Oracle 6; Mystery: Life; selected Tier II Revelation"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_HEAL_RIDER + FLOOR",
      "operationalOverrides": [
        "“was below half” uses pre-heal state; emergency floor separate."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.time.echo-strike",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.time.echo-strike",
      "sourceSha256": "eb631339bca8a9fbada16f055ce6bb3a6ab1703132bbeef0477fd0fae77b34f0",
      "sourceProcedure": {
        "name": "Echo Strike",
        "activation": "Reaction",
        "cost": "1 RC",
        "rangeAndTarget": "Same target just hit by your weapon or touch attack",
        "duration": "Instantaneous",
        "frequency": "At most once per round",
        "effect": "Immediately after your weapon or touch attack hits, spend 1 RC. Copy half the triggering attack's unmodified rolled damage dice total, rounded down, minimum 1, as damage of the same type to the same target. The echo is not another attack, cannot critically hit and copies no flat modifiers, conditions, resource gains or proc triggers. If this copied damage leaves the target below half maximum HP, regain 1 RC after resolution, at most once per round and never above maximum.",
        "prerequisite": "Oracle 3; Mystery: Time; selected Tier I Revelation"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "POST_DAMAGE_THRESHOLD",
      "operationalOverrides": [
        "RC check after echo damage using then-effective max."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "oracle.supplement.time.rewind-wound",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.time.rewind-wound",
      "sourceSha256": "eb01bdc7533669a80e0862bf3130c342b3b8c9c3f4199f8925953086e6bc898c",
      "sourceProcedure": {
        "name": "Rewind Wound",
        "activation": "Action",
        "cost": "2 RC",
        "rangeAndTarget": "One living ally you touch",
        "duration": "Healing instantaneous; protection until start of your next turn",
        "frequency": "At will while RC remains; same damage event can be rewound once",
        "effect": "Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects.",
        "prerequisite": "Oracle 6; Mystery: Time; selected Tier II Revelation"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "HISTORICAL_THRESHOLD",
      "operationalOverrides": [
        "Uses maximum snapshot stored with referenced damage event."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-mercy.merciful-smite",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-mercy.merciful-smite",
      "sourceSha256": "bb24ea1355d04db34e882d50cc5ebadd7b6da097442a0c2813d9e39b6cc5421c",
      "sourceProcedure": {
        "name": "Merciful Smite",
        "activation": "Triggered",
        "cost": "Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8",
        "rangeAndTarget": "Creature hit by your melee weapon attack; up to 3 living allies within 10 feet of you",
        "duration": "Instantaneous",
        "frequency": "One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance",
        "effect": "Your Oath Smite deals radiant damage instead of adding a second Smite packet. After the Smite damage resolves, create a healing pool equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Divide that pool among up to 3 living allies within 10 feet. Healing cannot exceed maximum HP, remove Wounds or trigger additional Smite or healing-copy effects.",
        "prerequisite": "Paladin 3; Oath of Mercy"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "DAMAGE_DERIVED_HEAL",
      "operationalOverrides": [
        "No max modifier; healing maximum guard only."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-mercy.blessing-of-the-meek",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-mercy.blessing-of-the-meek",
      "sourceSha256": "de83f7216e4f442bf324e7e9650e69091077d79b1be79d0753257dfbce13cde4",
      "sourceProcedure": {
        "name": "Blessing of the Meek",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "One living ally within 30 feet",
        "duration": "Healing instantaneous; AC bonus until start of your next regular turn",
        "frequency": "At will while RP remains",
        "effect": "The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules.",
        "prerequisite": "Paladin 3; Oath of Mercy"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_HEAL_RIDER",
      "operationalOverrides": [
        "Below-half checked before healing."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-mercy.channel-life",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-mercy.channel-life",
      "sourceSha256": "791e5b9a6f7de5962bffa02d02d406a4eba8aedc125391595cd002581a5f6610",
      "sourceProcedure": {
        "name": "Channel Life",
        "activation": "Action",
        "cost": "5 RP",
        "rangeAndTarget": "Self and one living ally within 30 feet",
        "duration": "Instantaneous",
        "frequency": "At will while RP remains",
        "effect": "Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.",
        "prerequisite": "Paladin 9; Oath of Mercy"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD / DIRECT_HP_LOSS",
      "operationalOverrides": [
        "No max modifier; donor/current-max legality only."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-vengeance.final-verdict",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-vengeance.final-verdict",
      "sourceSha256": "588a235ef97e9f2d39ca847326623ea090b05676da713f90f447f75361e5582d",
      "sourceProcedure": {
        "name": "Final Verdict",
        "activation": "Action",
        "cost": "10 RP",
        "rangeAndTarget": "One creature marked by you within 30 feet and at or below half maximum HP",
        "duration": "Instantaneous or empowerment until end of your next regular turn",
        "frequency": "At will while RP remains",
        "effect": "The marked target makes a Constitution save, taking 4 S d8 radiant damage on failure or half on success. On failure it also cannot regain HP until the end of its next turn. If that damage reduces it to 0 HP, use ordinary Downed/death rules; there is no percentage-HP execution. On success your next Smite against it before the end of your next turn uses maximum damage dice. This bounded damage replaces the source draft’s automatic reduction to 0 HP.",
        "prerequisite": "Paladin 17; Oath of Vengeance"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_TARGET_GATE",
      "operationalOverrides": [
        "Must be ≤half at activation."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution",
      "sourceSha256": "42295f38a12b89d74114739244ddfb5ba9e19a6f750356f0cf42fbbdfaf16740",
      "sourceProcedure": {
        "name": "Death Touch — Malicious Execution",
        "activation": "Action",
        "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss",
        "rangeAndTarget": "One creature within melee reach",
        "duration": "Instantaneous",
        "frequency": "At will while Lay on Hands points remain; rider once per turn",
        "effect": "Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared Lay on Hands points. If the target was already at or below half maximum HP, it makes a Constitution save; on failure add S d6 necrotic damage. This rider never automatically executes or bypasses normal death rules.",
        "prerequisite": "Paladin 3; Oathbreaker — Oath of Vengeance"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_DAMAGE",
      "operationalOverrides": [
        "“already” ≤half before rider damage."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-vengeance.fearbrand",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-vengeance.fearbrand",
      "sourceSha256": "ecff141c9410cecd56ebbdaabcdb43dd1d6b686aa823a6b17afda3efc4307953",
      "sourceProcedure": {
        "name": "Fearbrand",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 enemies in your Oath aura",
        "duration": "Damage instantaneous; Frightened until end of next turn",
        "frequency": "1/short rest; replaces Signature Power use",
        "effect": "Each target makes a Wisdom save. On failure it takes 2 S d6 psychic damage and is Frightened until the end of its next turn; on success it takes half damage and is not Frightened. A target already below half maximum HP takes one additional d6 psychic damage. This creates no execution effect.",
        "prerequisite": "Paladin 11; Oathbreaker — Oath of Vengeance"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_DAMAGE",
      "operationalOverrides": [
        "Below-half bonus assessed before its damage."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.crown-undying",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.crown-undying",
      "sourceSha256": "f8de6f3fe586c6b30d10bbdd31c93e0976aa46dfb3631afbbcbebe8ebe1d0b1d",
      "sourceProcedure": {
        "name": "Crown Undying",
        "activation": "Bonus Action",
        "cost": "0 RP",
        "rangeAndTarget": "Up to three selected allies in your aura",
        "duration": "Three rounds; no concentration",
        "frequency": "1/long rest",
        "effect": "For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.",
        "prerequisite": "Paladin 20; Oath of the Martyr King"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD",
      "operationalOverrides": [
        "Heal cannot exceed max; no max modifier."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "shaman.hero.bloodcaller.talon-strike",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.bloodcaller.talon-strike",
      "sourceSha256": "6d8b5fb22ca3318d686cd4cb983113cde306f655db9875a58b62287826e71029",
      "sourceProcedure": {
        "name": "Talon Strike",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "One enemy in claw reach",
        "duration": "Instant; reduction until end next turn",
        "frequency": "Recharge 2",
        "effect": "Make one claw attack; hit adds S d6 necrotic and reduces the next healing it receives by M, minimum 0. Applies once and ends. No arbitrary percent stacking or permanent maximum-HP reduction.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "EXCLUSION",
      "operationalOverrides": [
        "Explicitly no permanent/max-HP reduction."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.repair-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.repair-pulse",
      "sourceSha256": "bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593",
      "sourceProcedure": {
        "name": "Repair Pulse",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "Upto 3 friendly devices within 30 ft",
        "duration": "Instant; AC until start next turn",
        "frequency": "1/short rest",
        "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_DEVICE_REPAIR",
      "operationalOverrides": [
        "Functional device restores floor(max/2)."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.snap-rebuild",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.snap-rebuild",
      "sourceSha256": "0a8d445d6a86fd84b5dc4587562eb1eab093cd81ae114f10be850ad8f512cd11",
      "sourceProcedure": {
        "name": "Snap Rebuild",
        "activation": "Bonus Action",
        "cost": "2 RP; 1 encounter use",
        "rangeAndTarget": "One destroyed device/drone within 15 ft",
        "duration": "Remaining original duration",
        "frequency": "1/encounter",
        "effect": "Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_DEVICE_RECONSTRUCTION",
      "operationalOverrides": [
        "Destroyed device restored to floor(max/2); device lifecycle handles viability."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.engine[8]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": 8,
      "sourceSha256": "99a5efcfe2e2e606bb3782c034b79441119d5183396c4bf53787d8ffc58fae4a",
      "sourceProcedure": {
        "text": "BRUTALITY PROGRESS. Begin each real encounter with Brutality Progress 0 and BT 0. Add actual damage you personally deal to meaningful hostile creatures to Brutality Progress, but a single damage event contributes no more than one-quarter of your maximum HP. Crossing cumulative thresholds equal to 25%, 50% and 75% of your maximum HP grants 1 BT each, subject to the BT cap. Crossing 100% triggers Transcendent as described below but does not create a fourth stored BT unless Stack Overflow or another feature raises the cap."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "PERCENT_THRESHOLD_RESOURCE_ENGINE",
      "operationalOverrides": [
        "Brutality contribution/thresholds use reviewed max-HP snapshots; unchanged."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.engine[15]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": 15,
      "sourceSha256": "131241182dc02a463a2ac51c44a39e0d15e63ccfa46eeb436bc8763593d8e312",
      "sourceProcedure": {
        "text": "HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "GUARD",
      "operationalOverrides": [
        "Warrior healing maximum/death guard."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.base.brutality-sense",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.base.brutality-sense",
      "sourceSha256": "1e9c30e1f682ae0ef2c634631e163656321ce1f52ce9666e01fa06e6e23b6193",
      "sourceProcedure": {
        "name": "Brutality Sense",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Hostile creatures you can perceive within 60 feet",
        "duration": "While condition remains true",
        "frequency": "Always",
        "effect": "Brutality Sense. You know when a visible hostile creature is at or below one-quarter of its maximum HP; it is Vulnerable for your Warrior features that specifically reference a marked vulnerable target. This does not reveal its exact HP or hidden resistances.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "CONTINUOUS_THRESHOLD",
      "operationalOverrides": [
        "Visible hostile ≤quarter recalculates continuously."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.hero.ironskin.regenerative-mutation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.ironskin.regenerative-mutation",
      "sourceSha256": "9dcfe6b7b149360e470c0d7940937b13c7bbdc4f696999b93710257158818fd1",
      "sourceProcedure": {
        "name": "Regenerative Mutation",
        "activation": "Passive",
        "cost": "Spend healing amount from Mutation Recovery Reserve",
        "rangeAndTarget": "Self",
        "duration": "While at least one mutation is active in a real encounter",
        "frequency": "Once at the start of each regular turn",
        "effect": "Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "CONTINUOUS_BELOW_MAX_HEAL",
      "operationalOverrides": [
        "Eligible while current HP < effective max."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.hero.dreadspawn.pain-empowerment",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.dreadspawn.pain-empowerment",
      "sourceSha256": "2b76787a8cddab4ebacdbf316a7c566f95cc8e0607dcc02cafc57f0dc09741ab",
      "sourceProcedure": {
        "name": "Pain Empowerment",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "While below maximum HP",
        "frequency": "Always",
        "effect": "Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "CONTINUOUS_PERCENT_MISSING",
      "operationalOverrides": [
        "Exact full 10% bands from current effective max."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.supplement.flesh-warden",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.flesh-warden",
      "sourceSha256": "6ebfcac9c52f7d99711196a075bf63622082e7a932f2ae4086949c4656a23886",
      "sourceProcedure": {
        "name": "Flesh Warden",
        "activation": "Passive while equipped",
        "cost": "One mutation slot",
        "rangeAndTarget": "Self",
        "duration": "While equipped",
        "frequency": "Mutation",
        "effect": "Increase maximum HP by 2 per Warrior level while equipped. Equipping raises maximum only, never current HP. Unequipping clamps current HP to the reduced maximum if necessary; it does not subtract another amount from current HP. Repeated swaps cannot heal.",
        "prerequisite": "Warrior 1; Basic Vital"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS",
      "operationalOverrides": [
        "+2×Warrior level while equipped; capacity only."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.supplement.adrenal-floodgate",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.adrenal-floodgate",
      "sourceSha256": "00458063b06700533ef4cd58b5d045311c1a0fe9b663fa20f0fa7fc7414a5c3d",
      "sourceProcedure": {
        "name": "Adrenal Floodgate",
        "activation": "Triggered while active",
        "cost": "One mutation slot; serum activation",
        "rangeAndTarget": "Self",
        "duration": "Instantaneous",
        "frequency": "1/encounter",
        "effect": "When you first fall to one-quarter maximum HP or less, regain 2d8 HP and end either Frightened, Poisoned or Staggered on yourself.",
        "prerequisite": "Warrior 6; Advanced Vital"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_CROSSING",
      "operationalOverrides": [
        "First genuine fall to ≤quarter."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.supplement.mythic-carapace",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.mythic-carapace",
      "sourceSha256": "9af81b1909628a95c3cc716c883ed8c38e2cf4b847cf8f43b43ca43e5bb67dbc",
      "sourceProcedure": {
        "name": "Mythic Carapace",
        "activation": "Passive while active",
        "cost": "One mutation slot; serum activation",
        "rangeAndTarget": "Self",
        "duration": "Until encounter ends, mutation ends or you fall below one-quarter maximum HP",
        "frequency": "Apex mutation",
        "effect": "Gain DR 3 against all damage and immunity to Bleed, Poisoned and Burn-style ongoing fire effects. Once per encounter when one hit deals more than 20 actual damage after mitigation, gain 1 BT and refresh the remaining duration of your other active mutations to 3 rounds. It grants no serum-profile refresh.",
        "prerequisite": "Warrior 15; Apex Vital; maximum one Apex equipped"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "CONTINUOUS_DURATION_THRESHOLD",
      "operationalOverrides": [
        "NEW: ends whenever state is strictly below quarter; >20 actual-damage rider separate."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "warrior.supplement.butcherform-chassis",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.butcherform-chassis",
      "sourceSha256": "623cde33b8f868af96dbfed52d286fbc5b263603e9c44ddfff41ab6b2c0efe59",
      "sourceProcedure": {
        "name": "Butcherform Chassis",
        "activation": "Passive while active",
        "cost": "One mutation slot; serum activation",
        "rangeAndTarget": "Self",
        "duration": "3 rounds or until below one-quarter maximum HP",
        "frequency": "Apex mutation",
        "effect": "When you take the ordinary Attack action, make one additional melee attack beyond other Extra Attack effects, respecting the one-additional-full-Action guard because this is part of the same Action. Your melee criticals add one extra weapon damage die beyond normal critical dice, not triple total damage. Once per round when you personally kill a meaningful hostile with a melee attack, restore one consumed prepared serum dose, never above reserve capacity.",
        "prerequisite": "Warrior 15; Apex Combat; maximum one Apex equipped"
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "CONTINUOUS_DURATION_THRESHOLD",
      "operationalOverrides": [
        "NEW: ends whenever state is strictly below quarter."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "wizard.engine[10]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/wizard.json",
      "sourceId": 10,
      "sourceSha256": "673521960e487b21772372733af6aaa0c478c7f3308b6a58607a3c5ac2d83f99",
      "sourceProcedure": {
        "text": "ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS + EXCLUSIONS",
      "operationalOverrides": [
        "Conjuration +L to Wizard-summoned creatures; other school clauses separate."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "wizard.engine[24]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/wizard.json",
      "sourceId": 24,
      "sourceSha256": "95c82d28fd1e7975539e00e8550204b4923426cf2050dd14ac56e39197f705b1",
      "sourceProcedure": {
        "text": "Flesh Ascendant's bonus applies after the listed base statistics: every undead creature you control gains +2 maximum HP per Wizard level. If at least two of your undead creatures are active, each gains +1 AC and +1 on saving throws. This does not increase the standard-minion or elite-pet caps."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS_ENGINE",
      "operationalOverrides": [
        "Flesh Ascendant +2L after listed base; same modifier identity as card."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "wizard.hero.necromancer.flesh-ascendant",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/wizard.json",
      "sourceId": "wizard.hero.necromancer.flesh-ascendant",
      "sourceSha256": "d42c2937345d5ef23acd97375f6751ada7f9ba7b83ebe12212078d603257e37b",
      "sourceProcedure": {
        "name": "Flesh Ascendant",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Undead creatures you control",
        "duration": "Permanent while active",
        "frequency": "Always",
        "effect": "Flesh Ascendant. Tags: hero, necromancer, passive, undead. Each undead creature you control gains +2 maximum HP per Wizard class level. While at least two of your undead creatures are active, each also gains +1 AC and +1 on saving throws. These bonuses apply after the common standard-minion and elite-pet statistics and do not increase companion caps or command frequency.",
        "prerequisite": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS",
      "operationalOverrides": [
        "Same Flesh Ascendant bonus as engine[24], not cumulative with it."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:exploit_weakness",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "exploit_weakness",
      "sourceSha256": "95ea910b9634b6361c12f2d3f6008aeecbc0d2e0872119df1dc0f7ed60addc76",
      "sourceProcedure": {
        "name": "Exploit Weakness",
        "description": "At level 7, a combatant seeks wounded enemies for the listed critical chance.",
        "prerequisite": "Level 7",
        "effect": "Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.",
        "legacyEffect": "+15% crit on wounded enemies",
        "status": "provisional-complete",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "THRESHOLD_ATTACK",
      "operationalOverrides": [
        "19–20 crit range only while target strictly below half."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:familiar_bond",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "familiar_bond",
      "sourceSha256": "bea9d7f867e8c31c4b4e5d07a8db262037fbfa3cdc4843d136e120322d685114",
      "sourceProcedure": {
        "name": "Familiar Bond",
        "description": "Your bond with your familiar is stronger.",
        "prerequisite": "Ability to cast find familiar",
        "effect": "Your familiar gains hit points equal to your level and can attack using your spell attack bonus.",
        "legacyEffect": null,
        "status": null,
        "source": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS_PROVISIONAL",
      "operationalOverrides": [
        "NEW: familiar +owner level max HP; creation starts with boosted max/current, later growth capacity only."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:tenacity",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "tenacity",
      "sourceSha256": "5f3e13d83dd42dca3d5fac9ba4fa2e707884921e38b07f80e230d3f013aae461",
      "sourceProcedure": {
        "name": "Tenacity",
        "description": "Level 4 supports the listed +1 HP per level.",
        "prerequisite": "Level 4",
        "effect": "Your hit point maximum increases by 1 for each character level, including levels already gained.",
        "legacyEffect": "+1 HP per level",
        "status": "provisional-complete",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS_DYNAMIC",
      "operationalOverrides": [
        "+1 per current character level."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:tough",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "tough",
      "sourceSha256": "525ce21adb774fad8a95a76be8358bf3e37fa8a2649aa2ccecb6c2009cbf45bc",
      "sourceProcedure": {
        "name": "Tough",
        "description": "Your hit point maximum increases.",
        "prerequisite": "None",
        "effect": "Your hit point maximum increases by an amount equal to twice your level when you gain this feat.",
        "legacyEffect": null,
        "status": null,
        "source": null
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS_SNAPSHOT",
      "operationalOverrides": [
        "+2×level at feat acquisition; no inferred future growth."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:tough_as_nails",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "tough_as_nails",
      "sourceSha256": "148868a5e7c860c3f3569c6f3fcade2a1f323ddca3d9cb35609511fce3ed0d86",
      "sourceProcedure": {
        "name": "Tough as Nails",
        "description": "Level 5 supports the listed +10% maximum HP.",
        "prerequisite": "Level 5",
        "effect": "Your hit point maximum increases by 2 per character level when you take this feat, and by 2 whenever you gain a level thereafter.",
        "legacyEffect": "+10% max HP",
        "status": "provisional-complete",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS_DYNAMIC",
      "operationalOverrides": [
        "+2 per current level with explicit later-level growth."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:dark_fortitude",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "dark_fortitude",
      "sourceSha256": "852eee532dee1859120104bb0d8f83f5458baa418d3a224d02d255a0e7d7890a",
      "sourceProcedure": {
        "name": "Dark Fortitude",
        "description": "Grave-cold and poison have tried to claim you. They learned your name and backed away. Prestige lineage: Gravetouched. completed from the existing development record.)",
        "prerequisite": "Constitution 15+",
        "effect": "You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest). While below half your hit point maximum, you have resistance to poison damage.",
        "legacyEffect": "You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest). While below half your hit point maximum, you have resistance to poison damage.",
        "status": "provisional-complete",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "MAX_HP_BONUS_DYNAMIC + CONTINUOUS_THRESHOLD",
      "operationalOverrides": [
        "+2/current level; poison resistance while strictly below half."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    },
    {
      "bindingId": "feat:life_drinker",
      "sourceKind": "feat",
      "sourcePath": "src/data/feats.js",
      "sourceId": "life_drinker",
      "sourceSha256": "9823f4d451eb12aa8054ad4dd9446cf99d3a7270090e9d9387906b259df516ca",
      "sourceProcedure": {
        "name": "Life Drinker",
        "description": "Every wound you open is a cup. You drink and stand taller. Prestige lineage: Bloodbound. completed from the existing development record.)",
        "prerequisite": "Dark Affinity or Hemocraft",
        "effect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
        "legacyEffect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
        "status": "provisional-complete",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required."
      },
      "status": "DISCUSSED; precise boundaries / implementation pending",
      "classification": "HEALING + CONTINUOUS_THRESHOLD",
      "operationalOverrides": [
        "Crit/kill healing plus +1d4 necrotic while strictly below half."
      ],
      "reviewEvidence": [
        "GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md"
      ],
      "openIssues": [
        "First proposal captured; exact source-clock/stacking/crossing clarification and implementation review remain open. Other card/feat components are not promoted."
      ]
    }
  ]
}

## Exact tools/maximum_hp_playtest_rules.py

"""Proposed58-source maximumHP/threshold primitives; exact review pending.

Base maximum excludes the represented ledger bonuses/reductions and systemic
factors. Caller owns legal sources, acquisition, target/control/equipment state,
level updates, real event snapshots, actions and rest completion.
"""
from dataclasses import dataclass,field,replace
from fractions import Fraction
from spell_playtest_rules import integer,SpellRuleError
from strain_playtest_rules import combined_maximum_hp,apply_effective_maximum
from control_playtest_rules import ClockMarker,clock_marker,require_deadline

MONK={
 'monk.hero.iron-fist-master.ribcrusher-strike':1,
 'monk.hero.iron-fist-master.bone-breaking-strike':2,
 'monk.hero.way-of-shadow.deathless-silence':4,
}
BONUS_GROUPS={
 'warrior.supplement.flesh-warden':'flesh-warden',
 'wizard.engine[10]':'wizard-conjuration',
 'wizard.engine[24]':'flesh-ascendant',
 'wizard.hero.necromancer.flesh-ascendant':'flesh-ascendant',
 'feat:familiar_bond':'familiar-bond',
 'feat:tenacity':'tenacity',
 'feat:tough':'tough',
 'feat:tough_as_nails':'tough-as-nails',
 'feat:dark_fortitude':'dark-fortitude',
}

def identity(value):
    if not isinstance(value,str) or not value:raise SpellRuleError('Nonempty identity required')
    return value

def source_amount(source,*,scale=1,modifier=1,character_level=1,warrior_level=1,
                  wizard_level=1,acquisition_level=None,conjuration_creation_level=None):
    """Freeze trauma/application amounts; refresh dynamic bonuses on legal level changes.

    Conjuration uses a stored creating-Wizard level; Tough uses acquisition level.
    Companion base statistics and feat acquisition/retraining are separate.
    """
    if source in MONK:
        integer(scale,'S',1,4);integer(modifier,'M',1)
        return MONK[source]*scale+modifier
    if source=='warrior.supplement.flesh-warden':
        return 2*integer(warrior_level,'Warrior level',1,20)
    if source=='wizard.engine[10]':
        return integer(conjuration_creation_level,'creating Wizard level snapshot',1,20)
    if source in ('wizard.engine[24]','wizard.hero.necromancer.flesh-ascendant'):
        return 2*integer(wizard_level,'current controlling Wizard level',1,20)
    integer(character_level,'current character level',1,20)
    if source=='feat:tough':
        return 2*integer(acquisition_level,'feat acquisition level snapshot',1,character_level)
    if source in ('feat:tenacity','feat:familiar_bond'):return character_level
    if source in ('feat:tough_as_nails','feat:dark_fortitude'):return 2*character_level
    raise SpellRuleError('Unreviewed maximumHP source')

@dataclass(frozen=True)
class MaxHpRecord:
    application_id: str
    source: str
    owner: str
    target: str
    amount: int
    starts: ClockMarker=field(default_factory=lambda:ClockMarker(0))
    expires: ClockMarker | None=None
    present: bool=True
    suppressed: bool=False
    ends_on_completed_rest: bool=False
    ended_reason: str | None=None

    def __post_init__(self):
        for x in (self.application_id,self.owner,self.target):identity(x)
        if self.source not in MONK and self.source not in BONUS_GROUPS:
            raise SpellRuleError('Unreviewed maximumHP modifier source')
        integer(self.amount,'source maximumHP modifier magnitude',0)
        require_deadline(self.starts)
        if self.expires is not None:
            require_deadline(self.expires)
            if self.expires<=self.starts:raise SpellRuleError('Expiry must follow application')
        if self.ends_on_completed_rest and self.source not in MONK:
            raise SpellRuleError('Only supplied Monk trauma uses this rest endpoint')
        if self.source in MONK and self.expires is None and not self.ends_on_completed_rest:
            raise SpellRuleError('Monk trauma needs its rest or explicit earlier endpoint')

    def operative(self,now):
        now=clock_marker(now)
        return self.present and not self.suppressed and self.starts<=now and (self.expires is None or now<self.expires)

    @property
    def group(self):
        return 'monk-trauma-global' if self.source in MONK else BONUS_GROUPS[self.source]

def effective_maximum(base,records,*,target,now=0,expedition=0,exhaustion=0):
    """Source-supported groups only; global Monk strongest, distinct bonuses additive."""
    integer(base,'base maximum excluding this ledger and systemic factors',1);identity(target)
    rows=tuple(records)
    if len({r.application_id for r in rows})!=len(rows):raise SpellRuleError('Duplicate application identity')
    active=[r for r in rows if r.target==target and r.operative(now)]
    groups={}
    for r in active:
        old=groups.get(r.group)
        if old is None or (-r.amount,r.starts,r.application_id)<(-old.amount,old.starts,old.application_id):
            groups[r.group]=r
    bonuses=sum(r.amount for r in groups.values() if r.source not in MONK)
    trauma=groups['monk-trauma-global'].amount if 'monk-trauma-global' in groups else 0
    pre=max(1,base+bonuses-trauma)
    maximum=combined_maximum_hp(pre,expedition=expedition,exhaustion=exhaustion)
    return {'effectiveMaximum':maximum,'baseMaximum':base,'additiveBonuses':bonuses,
            'monkTraumaReduction':trauma,'preSystemicMaximum':pre,
            'selectedApplications':{group:r.application_id for group,r in groups.items()}}

def update_maximum(life,base,records,**options):
    report=effective_maximum(base,records,**options)
    out=apply_effective_maximum(life,report['effectiveMaximum'])
    return out,{**report,'capacityClamp':life.hp-out.hp,'actualHpDamage':0,
                'actualHpGained':0,'woundSaves':0,'deathFailuresAdded':0}

def complete_target_rest(records,target,*,completed,rest_type):
    identity(target)
    if rest_type not in ('short','long'):raise SpellRuleError('Use a completed short or long rest')
    return tuple(replace(r,present=False,ended_reason='completed-target-'+rest_type+'-rest')
                 if completed and r.target==target and r.ends_on_completed_rest and r.present
                 else r for r in records)

def threshold(hp,maximum,*,fraction=Fraction(1,2),relation='below'):
    integer(maximum,'effective maximum',1);integer(hp,'current normalHP',0,maximum)
    if not isinstance(fraction,Fraction) or not 0<=fraction<=1:
        raise SpellRuleError('Threshold requires an exact fraction from0 through1')
    left=hp*fraction.denominator;right=maximum*fraction.numerator
    if relation=='below':return left<right
    if relation=='at-or-below':return left<=right
    if relation=='above':return left>right
    if relation=='at-or-above':return left>=right
    raise SpellRuleError('Unknown threshold relation')

@dataclass(frozen=True)
class HpEventSnapshot:
    event_id: str
    before_hp: int
    after_hp: int
    effective_maximum: int
    kind: str
    def __post_init__(self):
        identity(self.event_id);integer(self.effective_maximum,'event effective maximum',1)
        integer(self.before_hp,'before HP',0,self.effective_maximum)
        integer(self.after_hp,'after HP',0,self.effective_maximum)
        if self.kind not in ('damage','direct-hp-loss','healing','capacity-change'):
            raise SpellRuleError('Unreviewed HP transition kind')
        if self.kind in ('damage','direct-hp-loss') and self.after_hp>self.before_hp:
            raise SpellRuleError('Damage/loss snapshot cannot show net healing')
        if self.kind=='healing' and self.after_hp<self.before_hp:
            raise SpellRuleError('Healing snapshot cannot show net HP loss')

    def falls_across(self,*,fraction=Fraction(1,4),inclusive=True):
        relation='at-or-below' if inclusive else 'below'
        return (self.kind in ('damage','direct-hp-loss') and self.after_hp<self.before_hp
                and not threshold(self.before_hp,self.effective_maximum,fraction=fraction,relation=relation)
                and threshold(self.after_hp,self.effective_maximum,fraction=fraction,relation=relation))

    def healed_above_half(self):
        return self.kind=='healing' and self.after_hp>self.before_hp and threshold(self.after_hp,self.effective_maximum,relation='above')

    def damage_left_below_half(self):
        # "Had reduced it below" is a stored damage predicate, not a later stat test.
        return self.kind=='damage' and self.after_hp<self.before_hp and threshold(self.after_hp,self.effective_maximum)

def pain_empowerment(hp,maximum):
    integer(maximum,'effective maximum',1);integer(hp,'current HP',0,maximum)
    return min(5,10*(maximum-hp)//maximum)

def percentage_amount(maximum,denominator,*,source_minimum=0):
    """Pure amount only. Minimum must come from printed source/viable revival bridge."""
    integer(maximum,'effective maximum',1);integer(denominator,'percentage denominator',1)
    integer(source_minimum,'explicit source minimum',0)
    return max(source_minimum,maximum//denominator)


## Exact tools/validate_maximum_hp_playtests.py

from pathlib import Path
import json
from maximum_hp_playtest_rules import *
from core_playtest_rules import LifeState,healing_ceiling
from healing_playtest_rules import survival_damage_event
ROOT=Path(__file__).resolve().parents[1]
RIB='monk.hero.iron-fist-master.ribcrusher-strike'
BONE='monk.hero.iron-fist-master.bone-breaking-strike'
SILENCE='monk.hero.way-of-shadow.deathless-silence'
FLESH='warrior.supplement.flesh-warden'

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected);checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    def rec(name,source,amount,owner='owner',target='target',**kw):
        return MaxHpRecord(name,source,owner,target,amount,ends_on_completed_rest=source in MONK,**kw)
    rows=[rec('flesh',FLESH,20),rec('trauma',RIB,9)]
    out=effective_maximum(101,rows,target='target',expedition=4,exhaustion=4)
    check('Flat bonus and global trauma precede systemic product',out['effectiveMaximum'],42)
    check('Otherwise applicable maximum includes both flat operations',out['preSystemicMaximum'],112)
    suppressed=[rows[0],replace(rows[1],suppressed=True)]
    check('Suppressing trauma recomputes from base without drift',
          effective_maximum(101,suppressed,target='target',expedition=4,exhaustion=4)['effectiveMaximum'],45)
    monks=[rec('small',RIB,5,owner='Monk-A'),rec('large',BONE,9,owner='Monk-B')]
    check('Different Monk owners share one global strongest reduction',
          effective_maximum(30,monks,target='target')['effectiveMaximum'],21)
    check('Suppressed strongest reveals smaller owner record',
          effective_maximum(30,[monks[0],replace(monks[1],suppressed=True)],target='target')['effectiveMaximum'],25)
    duplicate=rec('another-cast',RIB,7,owner='Monk-A',starts=ClockMarker(2),expires=ClockMarker(8))
    rows=monks+[duplicate]
    check('Repeated card keeps separate record but never stacks',
          effective_maximum(30,rows,target='target',now=3)['monkTraumaReduction'],9)
    check('Future application not active yet',
          effective_maximum(30,[duplicate],target='target',now=1)['effectiveMaximum'],30)
    check('Expiry wins at exact endpoint',
          effective_maximum(30,[duplicate],target='target',now=8)['effectiveMaximum'],30)
    check('Suppressed clock still expires',
          effective_maximum(30,[replace(duplicate,suppressed=True)],target='target',now=9)['effectiveMaximum'],30)
    stopped=complete_target_rest(rows,'target',completed=True,rest_type='short')
    check('Completed target rest ends all default Monk records including other owners',
          [r.present for r in stopped],[False]*3)
    check('Interrupted rest ends none',complete_target_rest(rows,'target',completed=False,rest_type='short'),tuple(rows))
    check('Another target rest cannot end records',
          complete_target_rest(rows,'someone-else',completed=True,rest_type='long'),tuple(rows))
    bonus=rec('permanent','feat:tenacity',8)
    check('Rest does not remove unrelated bonus',complete_target_rest([bonus],'target',completed=True,rest_type='long')[0].present,True)
    different=replace(duplicate,ends_on_completed_rest=False)
    check('Explicit endpoint-only record not replaced by default rest rule',
          complete_target_rest([different],'target',completed=True,rest_type='short')[0].present,True)
    check('Same feat duplicate does not stack',effective_maximum(20,[bonus,rec('duplicate-feat','feat:tenacity',8)],target='target')['effectiveMaximum'],28)
    all_feats=[rec('tenacity','feat:tenacity',10),rec('tough','feat:tough',6),
               rec('nails','feat:tough_as_nails',20),rec('dark','feat:dark_fortitude',20)]
    check('Distinct permanent feats add under explicit integration',effective_maximum(20,all_feats,target='target')['effectiveMaximum'],76)
    check('Tough snapshots acquisition level',source_amount('feat:tough',character_level=12,acquisition_level=3),6)
    check('Tough as Nails grows by explicit source',source_amount('feat:tough_as_nails',character_level=12),24)
    check('Tenacity grows dynamically',source_amount('feat:tenacity',character_level=12),12)
    check('Dark Fortitude grows dynamically',source_amount('feat:dark_fortitude',character_level=12),24)
    check('Familiar bonus current owner level',source_amount('feat:familiar_bond',character_level=12),12)
    check('Flesh Warden uses Warrior rather than character level',source_amount(FLESH,character_level=12,warrior_level=5),10)
    check('Conjuration uses creating Wizard snapshot',source_amount('wizard.engine[10]',wizard_level=12,conjuration_creation_level=5),5)
    check('Flesh Ascendant uses current controller Wizard level',source_amount('wizard.engine[24]',wizard_level=12),24)
    wizard=[rec('school','wizard.engine[10]',10),rec('flesh-engine','wizard.engine[24]',20),
            rec('flesh-card','wizard.hero.necromancer.flesh-ascendant',20)]
    check('Conjuration stacks with Flesh but duplicate engine/card do not',
          effective_maximum(20,wizard,target='target')['effectiveMaximum'],50)
    current=LifeState(30,26,temp_hp=35)
    after,event=update_maximum(current,30,[rec('trauma',BONE,15)],target='target')
    check('Clamp lowers currentHP but does not consume temporaryHP',(after.maximum_hp,after.hp,after.temp_hp),(15,15,35))
    check('Clamp produces no damage healing Wound or failure metrics',
          tuple(event[k] for k in ('capacityClamp','actualHpDamage','actualHpGained','woundSaves','deathFailuresAdded')),(11,0,0,0,0))
    healed_capacity,event=update_maximum(after,30,[],target='target')
    check('Removing reduction restores capacity without HP',(healed_capacity.maximum_hp,healed_capacity.hp),(30,15))
    critical=LifeState(30,15,wounds=(None,None,None))
    critical,_=update_maximum(critical,30,[rec('trauma',BONE,15)],target='target')
    check('Critical ceiling recalculates after max change',(critical.maximum_hp,healing_ceiling(critical)),(15,14))
    dying=LifeState(30,0,death_failures=2)
    dying,_=update_maximum(dying,30,[rec('severe',SILENCE,100)],target='target',expedition=6,exhaustion=6)
    check('Minimum max1 and lethal-track math do not alter zero life state',
          (dying.maximum_hp,dying.hp,dying.dead,dying.death_failures),(1,0,False,2))
    dead=LifeState(30,0,dead=True,death_failures=3)
    dead,_=update_maximum(dead,30,[rec('flesh',FLESH,20)],target='target')
    check('Capacity increase does not resurrect corpse',(dead.maximum_hp,dead.hp,dead.dead,dead.death_failures),(50,0,True,3))
    stable=LifeState(30,0,stable=True,stable_until_seconds=3600)
    stable,_=update_maximum(stable,30,[rec('flesh',FLESH,20)],target='target')
    check('Capacity update preserves Stable deadline',(stable.stable,stable.stable_until_seconds),(True,3600))
    check('Exact quarter comparison uses cross multiplication',threshold(25,100,fraction=Fraction(1,4),relation='at-or-below'),True)
    check('26of101 not quarter eligible',threshold(26,101,fraction=Fraction(1,4),relation='at-or-below'),False)
    check('Odd maximum half not rounded first',threshold(50,101),True)
    check('Exact half not strictly below',threshold(50,100),False)
    check('Pain uses exact full ten-percent bands',pain_empowerment(91,101),0)
    check('Pain reaches first full ten-percent band',pain_empowerment(90,101),1)
    check('Pain caps bonus at5',pain_empowerment(1,101),5)
    loss=HpEventSnapshot('loss',26,25,100,'damage')
    check('Genuine damage crosses inclusive quarter',loss.falls_across(),True)
    check('Direct HP loss can cross quarter',replace(loss,kind='direct-hp-loss').falls_across(),True)
    check('Capacity clamp never fires fall trigger',replace(loss,kind='capacity-change').falls_across(),False)
    check('Already below quarter losingHP does not cross again',HpEventSnapshot('already-low',20,19,100,'damage').falls_across(),False)
    check('Strict half crossing excludes landing on half',HpEventSnapshot('half',51,50,100,'damage').falls_across(fraction=Fraction(1,2),inclusive=False),False)
    check('Strict half crossing includes crossing from exact half',HpEventSnapshot('half-cross',50,49,100,'damage').falls_across(fraction=Fraction(1,2),inclusive=False),True)
    check('Healed-above-half requires actual healing gain',HpEventSnapshot('heal',50,51,100,'healing').healed_above_half(),True)
    check('NoHPgain despite already above half does not end healed gate',HpEventSnapshot('none',60,60,100,'healing').healed_above_half(),False)
    check('Max-only change cannot satisfy healed exit',HpEventSnapshot('max',60,60,100,'capacity-change').healed_above_half(),False)
    history=HpEventSnapshot('old-damage',60,49,100,'damage')
    check('Historical damage uses original event maximum',history.damage_left_below_half(),True)
    check('Later max60 would differ but does not rewrite stored predicate',threshold(49,60),False)
    check('WoundEaterIII no invented minimum at tiny maximum',percentage_amount(3,4),0)
    check('Explicit Spiral/FalseLife minimum1 remains',percentage_amount(3,4,source_minimum=1),1)
    check('Viable resurrection bridge minimum1 remains',percentage_amount(1,2,source_minimum=1),1)
    damage_state,damage_event=survival_damage_event(LifeState(30,30),4)
    trauma_state,stat_event=update_maximum(damage_state,30,[rec('bone',BONE,15)],target='target')
    check('Damage precedes separate maximumHP clamp',(damage_state.hp,trauma_state.hp,damage_event['actualDamageDealt'],stat_event['capacityClamp']),(26,15,4,11))
    rejects('Duplicate application identity rejected',lambda:effective_maximum(20,[bonus,bonus],target='target'))
    rejects('Unknown modifier source rejected',lambda:rec('unknown','spell:invented',5))
    rejects('Tough requires explicit acquisition snapshot',lambda:source_amount('feat:tough',character_level=12))
    rejects('Conjuration requires explicit creation snapshot',lambda:source_amount('wizard.engine[10]',wizard_level=12))
    rejects('Trauma cannot lose all endpoints',lambda:MaxHpRecord('endless',RIB,'monk','target',3))
    rejects('Approximate floating threshold disallowed',lambda:threshold(1,10,fraction=0.25))
    states=0
    for base in range(1,102):
      for expedition in (0,4,6):
       for exhaustion in (0,4,6):
        actual=effective_maximum(base,[],target='target',expedition=expedition,exhaustion=exhaustion)['effectiveMaximum']
        expected=max(1,(Fraction(base)* (Fraction(3,4) if expedition>=4 else 1) * (Fraction(1,2) if exhaustion>=4 else 1)).__floor__())
        assert actual==expected
        states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW; exact implementation pending',
            'scope':'Selected modifier formulas/groups, capacity recomputation/clamp, rest endpoints, exact percentage thresholds and recorded HP transitions. Not full feat/class acquisition, companion creation/lifecycle or combat scheduler.',
            'checkCount':len(checks),'systemicParityStates':states,'checks':checks}
    (ROOT/'docs/mechanics/MAXIMUM_HP_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} maximumHP checks and {states} systemic parity states; review pending.')
if __name__=='__main__':main()


## Exact docs/mechanics/MAXIMUM_HP_PLAYTEST.md

# Maximum HP, stat changes and HP thresholds

**IN REVIEW —58 exact passages:51 class records and7 feats.** The [source register](MAXIMUM_HP_SOURCE_BINDINGS.md) preserves the original procedures; [source validation](MAXIMUM_HP_SOURCE_VALIDATION.json) verifies equality and hashes. The [first captured notebook reply](../../../../docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md) is incomplete and must be read with the [complete tail and boundary corrections](../../../../docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_BOUNDARIES.md).

These rules cover the maximum-HP and threshold components supplied here. They do not promote whole feats, create companion actions, decide character advancement, or certify every monster/item/spell maximum-HP modifier.

## Recompute capacity from separate records

Keep base maximum, bonuses, reductions and systemic multipliers separate. Base maximum excludes all modifiers represented separately in this ledger. Never feed a previously modified maximum back into the formula.

First calculate the otherwise-applicable maximum:

    preSystemicMaximum = max(1, baseMaximum + compatibleBonuses − strongestMonkTrauma)

Then apply the reviewed systemic factors against that same value:

    effectiveMaximum = max(1, floor(preSystemicMaximum × systemicFactors))

Expedition Strain4+ contributes3/4 and Exhaustion4+ contributes1/2. Multiply compatible rational factors before rounding once. Base101, Flesh Warden+20, Monk trauma−9 and both factors produce42. Suppressing that trauma produces45; do not subtract the trauma again afterward.

The numerical modifier calculation does not perform lethal-track transitions. Use the separate reviewed life-state procedure when a track actually changes. Merely recomputing maximum HP must not re-kill a living collapsed survivor at track6.

Each application retains its own ID, source, owner, target, magnitude, start/end markers, presence and suppression state, arbitration group and any acquisition/creation snapshot needed for its formula. Keep records even when another stronger application wins. Suppression does not stop clocks.

## Bonuses and source identities

| Source | Bonus and update rule |
|---|---|
| Flesh Warden | +2 per Warrior level while legally equipped; capacity only |
| Wizard Conjuration specialization | +Wizard level captured when that Wizard spell creates the summon |
| Flesh Ascendant | +2 per current Wizard level of the eligible controller supplying the feature |
| Familiar Bond | Provisional +current eligible owner's character level to familiar maximum HP |
| Tenacity | +current character level |
| Tough | +twice character level when the feat was acquired; retain this snapshot |
| Tough as Nails | +2 per character level at acquisition, then +2 for each later level |
| Dark Fortitude | +2 per current character level |

**New feat integration:** distinct feat identities granting maximum HP add together unless an explicit source says otherwise. Duplicate copies of the same feat do not add. Their original acquisition/prerequisite, retraining and other-effect rules still need their separate review.

**New Wizard-specific stacking exception:** Conjuration and Flesh Ascendant add when the same undead summon qualifies for both, overriding the frozen strongest same-stat class-technique bonus default for this pair only. Flesh Ascendant's engine[24] and named card describe one modifier identity; do not count both.

Conjuration's amount and caster provenance stay tied to creation. A later caster level or controller change does not recompute that snapshot. Flesh Ascendant instead follows the current eligible controller; changing control ends the old controller's eligibility and can create the new controller's eligible bonus, without healing.

**New Familiar Bond interpretation:** its ambiguous “gains hit points” wording supplies maximum capacity. Initial creation under that bonus can include it in starting HP; later level increases add capacity only. Familiar ownership/replacement and attack/command rules remain in the future companion package.

When a creature is initially created, construct its starting state from its final creation maximum unless its source expressly enters it damaged. Base20 plus Conjuration10 plus Flesh Ascendant20 gives50/50 at creation. Acquiring either bonus later does not fill missing HP. No bonus changes creature or command caps.

## Monk trauma uses one global strongest reduction

**Explicit correction of the earlier per-owner proposal:** Monk engine[9]'s categorical non-stacking clause controls. Use the largest currently operative Monk maximum-HP reduction on the target across all owners.

Ribcrusher applies S+M, Bone-Breaking Strike2S+M, and Deathless Silence4S+M. Preserve each successful application separately, including repeated applications of the same card. Do not combine the strongest magnitude with another record's longer duration. If−9 is suppressed, an operative−5 can become effective; when−5 expires, it stops contributing even while−9 remains suppressed.

Default Monk trauma ends when the target completes a short or long rest. This is effect removal, independent of how many numerical rest rewards the target already earned. Interrupted rest ends none. A genuinely explicit earlier/different endpoint controls its own record; the existence of an endpoint parameter does not grant permission to invent one.

Deathless Silence has three independent components: the Monk's protection from Reactions/opportunity attacks through source-next-regular-start; target defensive-passive suppression through that target's next-turn end; and maximum-HP trauma through the target's completed rest. Preserve the already reviewed control clocks.

## Capacity changes are not HP damage or healing

After any maximum change, clamp current normal HP down only if it exceeds the new maximum. Adding/restoring maximum HP gives no current HP. This clamp is not damage, sacrifice or healing; it creates no Wound save, death-save failure, resource trigger, redirection or first-fall event. Decay does not prevent capacity restoration.

Temporary HP is independent and remains unchanged. Maximum reduced to10 does not remove an existing25 temporary HP.

Dead, Stable and dying0 creatures retain their life state, counters and Stable deadline. A minimum maximum of1 never revives a corpse. Critical's healing ceiling recomputes afterward as max(1,effectiveMaximum−1); it is not another maximum-HP reduction.

## Exact thresholds and recorded events

Use effective maximum and integer comparison, without rounding a percentage threshold first:

| Wording | Comparison |
|---|---|
| At/below one-quarter | 4×HP ≤ maximum |
| Below one-quarter | 4×HP < maximum |
| At/below half | 2×HP ≤ maximum |
| Below half | 2×HP < maximum |
| Above half | 2×HP > maximum |

Continuous predicates update whenever HP or maximum changes: Wyrmhide, Brutality Sense, Pain Empowerment, Dark Fortitude's poison resistance, Life Drinker's conditional damage, and “below maximum” regeneration eligibility. Pain Empowerment uses full10% missing-HP bands, capped at+5, at its printed pre-roll moment.

**New first-fall interpretation:** Anointed Guardian, Burning Blood IV, Death's Threshold and Adrenal Floodgate require a genuine downward crossing. At/below-quarter triggers require HP moving from above quarter to at/below quarter. Burning Blood IV requires moving from at/above half to strictly below half. Actual damage or direct HP loss can establish a crossing unless a source specifically restricts it to damage. Capacity changes and clamps cannot.

If a rest refreshes a first-fall use while its subject is already below the threshold, neither the refresh nor another1HP loss fires it. The subject must return to the non-trigger side and cross again. Source frequency/history remains a separate eligibility gate; a crossing alone grants no new use.

Death's Threshold's exit requires actual HP restoration leaving the creature above half. A maximum reduction that makes unchanged HP above half does not end it. A later actual heal can satisfy that exit even if the creature was already above half before that heal.

**New continuous duration interpretation:** Mythic Carapace and Butcherform Chassis end when active and strictly below quarter. A maximum increase can therefore end them without damage. Exact quarter remains legal. Other duration endpoints still apply.

Record pre/post normal HP and the event-effective maximum for historical checks. Rewind Wound uses the maximum stored with its referenced damage event, never a later maximum. Freeze same-event HP crossings before a later stat clamp.

Selection/rider timing follows each card: Mass Healing Light when its target is chosen; Merciful Sacrament at initial activation; Flesh to Ash before rolling damage; Death Touch at strike start; Blessing of the Meek/ Verdant Pulse before healing; Final Verdict at legal targeting; Fearbrand/Malicious Execution before their damage/rider; Echo Strike after its copied damage. Brutality Progress's already reviewed snapshot rules remain unchanged.

## Percentage recovery and damage

Use effective maximum when the amount resolves unless the source explicitly references an earlier snapshot. Floor the percentage amount, with minimum1 only where printed or already supplied by the reviewed viable-resurrection bridge.

Wound Eater III can heal0 at maximum3. Spiral III and False Life V explicitly retain minimum1 for quarter recovery. Unyielding Light uses one third with minimum1. Divine Rebirth uses the reviewed viable-return max(1,floor(maximum/2)). Wound Eater V's quarter target-HP loss and half self-heal cap retain their direct-loss classification. Ledger Unbound caps its raw damage at a quarter of target maximum before its save-halving.

Repair Pulse and Snap Rebuild use half device maximum under their own functional/destroyed target rules. A tiny-maximum reconstruction's viability belongs to the device lifecycle and is not silently converted into a general minimum1 here.

## Attack damage before Monk trauma

**New integration for the supplied Monk trauma cards:** choose/pay an after-hit option at its legal hit window. Resolve the ordinary attack's damage, Wounds, Instant Death and any survival replacement against the pre-trauma maximum; freeze its metrics. If the target remains an eligible living creature, resolve the trauma CON save using its then-current save modifier, including applicable Wound consequences. On failure, create the trauma record and recompute capacity.

If the attack leaves the target Dead, no combat-trauma record is needed and the paid cost is not refunded. A legal same-resolution death replacement preserving life can leave the target eligible.

Example: maximum30, HP30; damage4 leaves26 and records4 actual damage. A later−15 maximum reduction gives maximum15 and clamps current HP26→15. The11-point clamp causes no second damage/Wound/threshold event and cannot rewrite the attack's Instant Death threshold or concentration packet.

## Validation and remaining scope

The current reference passes60 targeted checks and909 systemic parity states. It accepts already legal source records and event snapshots; it does not decide source acquisition, perform companion creation, pay Ki, schedule turns or consume first-fall uses.

Still open: unsupplied item/spell/monster/disease/curse maximum modifiers; non-Monk reductions; exceptions applying after systemic multipliers; full feat acquisition/retraining; familiar and summon/control lifecycle; unusual device reconstruction; human balance. The58-source discussion does not close these larger domains.


## Exact docs/mechanics/MAXIMUM_HP_PLAYTEST_VALIDATION.json

{
  "status": "PASS",
  "reviewStatus": "IN_REVIEW; exact implementation pending",
  "scope": "Selected modifier formulas/groups, capacity recomputation/clamp, rest endpoints, exact percentage thresholds and recorded HP transitions. Not full feat/class acquisition, companion creation/lifecycle or combat scheduler.",
  "checkCount": 60,
  "systemicParityStates": 909,
  "checks": [
    "Flat bonus and global trauma precede systemic product",
    "Otherwise applicable maximum includes both flat operations",
    "Suppressing trauma recomputes from base without drift",
    "Different Monk owners share one global strongest reduction",
    "Suppressed strongest reveals smaller owner record",
    "Repeated card keeps separate record but never stacks",
    "Future application not active yet",
    "Expiry wins at exact endpoint",
    "Suppressed clock still expires",
    "Completed target rest ends all default Monk records including other owners",
    "Interrupted rest ends none",
    "Another target rest cannot end records",
    "Rest does not remove unrelated bonus",
    "Explicit endpoint-only record not replaced by default rest rule",
    "Same feat duplicate does not stack",
    "Distinct permanent feats add under explicit integration",
    "Tough snapshots acquisition level",
    "Tough as Nails grows by explicit source",
    "Tenacity grows dynamically",
    "Dark Fortitude grows dynamically",
    "Familiar bonus current owner level",
    "Flesh Warden uses Warrior rather than character level",
    "Conjuration uses creating Wizard snapshot",
    "Flesh Ascendant uses current controller Wizard level",
    "Conjuration stacks with Flesh but duplicate engine/card do not",
    "Clamp lowers currentHP but does not consume temporaryHP",
    "Clamp produces no damage healing Wound or failure metrics",
    "Removing reduction restores capacity without HP",
    "Critical ceiling recalculates after max change",
    "Minimum max1 and lethal-track math do not alter zero life state",
    "Capacity increase does not resurrect corpse",
    "Capacity update preserves Stable deadline",
    "Exact quarter comparison uses cross multiplication",
    "26of101 not quarter eligible",
    "Odd maximum half not rounded first",
    "Exact half not strictly below",
    "Pain uses exact full ten-percent bands",
    "Pain reaches first full ten-percent band",
    "Pain caps bonus at5",
    "Genuine damage crosses inclusive quarter",
    "Direct HP loss can cross quarter",
    "Capacity clamp never fires fall trigger",
    "Already below quarter losingHP does not cross again",
    "Strict half crossing excludes landing on half",
    "Strict half crossing includes crossing from exact half",
    "Healed-above-half requires actual healing gain",
    "NoHPgain despite already above half does not end healed gate",
    "Max-only change cannot satisfy healed exit",
    "Historical damage uses original event maximum",
    "Later max60 would differ but does not rewrite stored predicate",
    "WoundEaterIII no invented minimum at tiny maximum",
    "Explicit Spiral/FalseLife minimum1 remains",
    "Viable resurrection bridge minimum1 remains",
    "Damage precedes separate maximumHP clamp",
    "Duplicate application identity rejected",
    "Unknown modifier source rejected",
    "Tough requires explicit acquisition snapshot",
    "Conjuration requires explicit creation snapshot",
    "Trauma cannot lose all endpoints",
    "Approximate floating threshold disallowed"
  ]
}


## Exact docs/mechanics/MAXIMUM_HP_SOURCE_VALIDATION.json

{
  "status": "PASS",
  "exactRecords": 58,
  "scope": "51 exact class passages and7 feat records: live source equality and captured hashes only. Not semantic completion of maximumHP or all listed sources.",
  "issues": []
}
