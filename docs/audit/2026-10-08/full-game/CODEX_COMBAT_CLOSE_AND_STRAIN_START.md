# Combat exact findings: implemented disposition

Both material fixes and the requested clarifications are implemented. Validation now PASS112 bounded checks plus285 movement-cost invariant states.

1. `marker_deadline(..., excluded_current_marker=None)` computes the first strictly future scheduled marker, compares that exact marker to the excluded current-end marker, and advances6 only if equal. Tests cover application1/end3→9; application4/excluded3→9; applicationexactly3/excluded3→9; two future ends with current end excluded→15. No blind Boolean skip remains.
2. Added `ManeuverAttempts`: separate Pin and Silence tokens, refreshed only by increasing regular-start ordinals. Legal declare-and-roll consumes on hit/miss; rejected illegal declaration consumes nothing. Extra turn and round boundary do not reset. Tests cover all your listed cases plus repeated-marker rejection and optional-maneuver conflict.
3. Ally-targeted bare N-round buffs explicitly use source-start convention; explicit target/pulse/absolute clock wins. Guide cites your exact review.
4. Ready effect duration explicitly begins at release; setup casting/cost/hold/Ready clocks stay at preparation. Separate helper tests prepared0/released4/3 elapsed rounds→22, and prepared1/released4/target end phase3/3 target markers→21. Release-before-prepare rejected. Caller still validates unexpired legal Ready state.
5. Added exact HP-helper scope sentence and Boolean-only Hide helper scope. Simultaneous arbitration remains outside HP helper, as documented. Secure Cargo/Load terminology remains open.

One specific-source exception found while collecting the next Strain sources needs your explicit acknowledgement so the generic Reaction rule does not erase it:

`data/public/class_playtests/warrior.json`, card `warrior.supplement.mind-shock`, serumProfile, Via Serum Injection, cost Dose consumption and normal Strain, duration3rounds, frequency Per prepared dose:

> Gain +2 on saving throws against spells. Once during the duration gain one additional Reaction usable only for movement, defense, Counterspell-like disruption already possessed or another non-attack reaction; it cannot make an attack. Side effect: -1 on Perception checks for the duration. Serum Tolerance suppresses that penalty.

Original source preserved on card: `| Mind Shock | +2 Save vs spells | +1 reaction use this turn | 3 rounds | Minor Hallucinations |`.

Proposed boundary: our interval model governs the ORDINARY Reaction. A reviewed explicit extra-Reaction card is a separate limited source grant, not a refresh of the ordinary resource and not a general permission for extra reactions. Mind Shock cannot make attacks or bypass Focused/Surprise/Incapacitated restrictions, and cannot teach Counterspell. Exact per-dose refresh/reapplication and all other class resource-grant interactions remain part of the all-source semantic pass; do not claim the ordinary `ReactionClock` helper models these. The guide now explicitly states this helper exclusion; source-card text is unchanged. Please confirm that source preservation and generic boundary, or identify a needed correction.

After the above bounded combat disposition, please proceed to the attached Strain namespace conference. This is continuing the whole-game work; the six broad combat ledger rows stay open. No original source has been deleted.


# Strain identities and recovery conference

Next remaining condition dependency: the same display name means two distinct systems. No original source is being rewritten. I propose explicit IDs `warrior.serum-strain` and `expedition.strain`; global `core.exhaustion`, Oracle Revelation backlash and spell Dissonance remain separate. Please review the exact evidence below and resolve the operational gaps. This is a fictional game-design decision, not medical advice.

Known evidence:
- Warrior normalized class engine[6], already class-reviewed: personal serum Strain0–3, serum/Mutagen/Surge +1, Cocktail/Overload +2 unless modified; level2 Speed−5; level3 additionally−1AC/saves and cannot voluntarily activate another serum/Cocktail/Overclock/Surge; short rest−1, long rest0, cap3.
- Gameplay Loop Strain0–6, exact table below; separate Expedition Load/campaign subsystem, not a class resource. Original core mentions unqualified Strain for Quickglass crash and morale rest but does not define that track in these passages.
- Core recovery/Wound treatment candidate critical failure adds1Strain to the patient, not healer. This needs an explicit namespace.
- Global Exhaustion six cumulative levels is already reviewed from Core+V6. Exhaustion immunity/removal should not silently affect either Strain track; a serum-rest reduction does not heal expedition attrition.
- Current generic condition guide says simply 'Strain is the expedition track'; that needs correcting to name both identities.

Please settle:

1. Agree separate IDs with no automatic conversion or pooled cap. Contextual references inside Warrior engine/cards mean serum Strain; Quickglass crash, morale rest, ordinary Wound-treatment critical failure and campaign survival references mean expedition Strain. Unknown unqualified future sources remain unbound until reviewed rather than guessed.
2. Are expedition table consequences cumulative? Propose yes, label NEW interpretation if not explicit. Level6 'death or permanent collapse, as appropriate to cause' is not executable. Choose a concrete default and any narrowly defined cause exception, with an honest NEW label. Avoid irreversible character removal merely from undefined Director whim. Serum3 never becomes expedition6/death by name match.
3. Penalties across independent tracks: can expedition−10 Speed and serum−5 coexist, and global Exhaustion half-Speed apply afterward? How combine expedition maxHP−25% with Exhaustion half-maxHP and existing Wound/critical healing ceiling? Propose combine applicable rational multipliers then floor once, min1, clamp currentHP downward only; removal restores maxHP capacity but never heals. Sources of same typed track do not stack numerical copies; increments change its level.
4. Expedition 'cannot Dash twice consecutively' at3: means two sequential turns of Dash, two Dashes in one turn, any consecutive Actions including separated by ordinary movement, or an interval cooldown? Give an explicit finite tracking rule covering BA Dash, extra turns, intervening non-Dash Actions and entering/leaving initiative. This must not silently contradict our legal multiple-Dash general rule; it is a track-specific restriction.
5. Expedition5 'Incapacitated except for slow travel and Rest': Core Incapacitated denies A/BA/R/concentration but not movement. Define slow travel and voluntary combat movement. Can the victim voluntarily drink, be fed, communicate and receive treatment? No arbitrary resurrection/free turns. Specify allowed assistance without inventing universal capture rules.
6. Rest: serum short/long recovery stays class-specific. Expedition secure long rest−1; Haven care 'one full day' removes all ordinary Strain. Existing expedition rest debt/food-water rules can block Strain reduction. Define secure/Haven time and ordinary vs source-blocked levels; avoid duplicate rewards from interrupt/restart or repeatedly declaring the same period. Core morale rest says safe evening chosen recreation removes1Strain; propose a finite 4h safe recreation, at most once per24h, cannot overlap work or sleep, no forced substance use. Can one genuinely separate evening + long rest legitimately remove2 expedition Strain? Source says two separate benefits, so don't erase one without marking NEW cap.
7. Can a single actual event add both Strain and Exhaustion? Only if source explicitly imposes both; never infer double attrition because both represent fatigue. Quickglass1Strain is expedition only, with its independent1h DEX-check disadvantage. Wound treatment failure1 is expedition only; no additional Wound beyond specified outcomes.
8. Immunities/removal: exact named immunity unless a reviewed source explicitly covers broader fatigue; don't import poison immunity into serum resource management, nor Exhaustion immunity into expedition Strain. Does gaining immunity suppress penalties while track clocks/recovery persist, or block only further gains? Need source-specific binding rather than universal guessed semantics.

Please identify any sources needed before resolving a point, and distinguish preserved rules from NEW defaults. We will retain the0–6 table as an explicit provisional expedition overlay, not silently promote it into Core. I will validate concrete recovery/maximumHP/namespace cases and return exact decisions before closure.

Additional source gate: the Gameplay reference caps beneficial short rests at2 between Long Rests and beneficial Long Rests at1 per24h. The shared class reference states completed1h/8h durations without repeating those caps. Please explicitly retain those campaign rest limits if compatible; do not let this pass silently waive them. Full HP/RP/RC rest rewards remain their later system review.

EXACT SOURCES

{
  "warriorPath": "data/public/class_playtests/warrior.json",
  "engine": [
    {
      "index": 2,
      "text": "MUTATION SLOTS. At Warrior 1 you have one mutation slot; slot II unlocks at Warrior 5, slot III at Warrior 13 and slot IV at Warrior 20. During a completed short or long rest, equip one eligible mutation in each slot. Equipped mutations are dormant until activated unless their text explicitly says otherwise. You cannot equip the same named mutation twice.",
      "textSha256": "46e631d227cb350f7e60ffc4e7b41d9a7587a3898c6a31399482749e4e3ca747"
    },
    {
      "index": 4,
      "text": "SERUM RESERVE. After a long rest prepare two serum doses, choosing one of the six serum profiles for each dose. At Warrior 11 the reserve becomes three prepared doses; at Warrior 20 it becomes four. Used doses do not naturally refill on a short rest. A long rest refills the reserve. Serum Recycling and explicit class features can preserve or restore doses, but no effect can increase the reserve above its current capacity.",
      "textSha256": "11e97b3da341ca4fcc22ba9e4b899d24d9fac85c485a6fce09e1dad882b7a657"
    },
    {
      "index": 6,
      "text": "STRAIN. Begin after a long rest at 0 Strain; maximum Strain is 3. A normal serum injection or Mutagen Injection adds 1 Strain, Mutation Surge adds 1, and Serum Cocktail or Mutation Overload adds 2 unless modified. At Strain 2 your Speed is reduced by 5 feet. At Strain 3 you also take -1 AC and -1 on saving throws and cannot voluntarily activate another serum, Cocktail, Overclock or Surge until Strain is reduced. A completed short rest reduces Strain by 1; a long rest resets it to 0. Strain cannot exceed 3.",
      "textSha256": "9c7678cb575181c076420262bcfcbeb61ef386d481f824e01e75cb860ce2c0e5"
    },
    {
      "index": 7,
      "text": "Mutation Adaptation and Serum Tolerance modify Strain and serum-profile side effects only as their cards state. A negative serum-profile side effect and Strain penalty are separate; preventing one does not automatically prevent the other.",
      "textSha256": "05c151592082a1142e732a25bbc761ef26c6e1bf74b33c61bc82d774fb49df4d"
    },
    {
      "index": 14,
      "text": "RECHARGE GUARD. A named ability may receive at most one positive-counter reset or shortening per round. Only an ability with a positive recharge counter can be reset. Recharge never restores a spent short-rest or long-rest use unless the feature explicitly says it restores that use.",
      "textSha256": "ab27d17725c41dbe4e0366e9a53c97ef7f5fadaa36cd129d576c9087445c1c71"
    },
    {
      "index": 15,
      "text": "HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT.",
      "textSha256": "131241182dc02a463a2ac51c44a39e0d15e63ccfa46eeb436bc8763593d8e312"
    },
    {
      "index": 19,
      "text": "HERO MUTATION TREES. Bulwark Mutation Tree, Gore Mutation Tree and Aberrant Mutation Tree are Hero cards that unlock their associated Hero-specific mutation extra Cards. Those mutations still occupy normal mutation slots and obey active-mutation, serum and Strain rules.",
      "textSha256": "621367b0999764bf09f44086dc0cb9ba127245e3759154d12328cfdea3555818"
    },
    {
      "index": 24,
      "text": "Finite recovery completion: Mutation Recovery Reserve=3 L+M HP after a long rest. Bloodthick Node, Rapid Coagulation, Regenerative Mutation, Hemophage Core and their healing enhancements draw from this shared reserve, 1 point per actual HP healed. No short-rest refill; no gauge, critical hit, free activation or form change replenishes it. Other explicitly limited-use/dose healing retains its own printed limit. This new test reserve prevents indefinite regenerative healing from free mutation activations.",
      "textSha256": "8d9be8ad7bbd69c27fc5c86a56943772f63026390522e512a2ec38b145a7eaf6"
    }
  ],
  "cards": [
    {
      "card": {
        "id": "warrior.base.mutation-adaptation",
        "name": "Mutation Adaptation",
        "className": "Warrior",
        "band": "Base",
        "path": null,
        "sourceKind": "passive",
        "minimumClassLevel": 1,
        "acquisition": "selection",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "Always",
        "effect": "Mutation Adaptation. Ignore the Strain-2 Speed penalty. The first time in each encounter that activating a mutation or serum would add Strain, reduce that Strain gain by 1, minimum 0. This reduction cannot reduce Serum Cocktail or Mutation Overload below 1 Strain and cannot reduce existing Strain.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4801,
          "originalText": "Mutation Adaptation: Your body has been conditioned to accept mutations with reduced side effects."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "e2f1a4625af779917a1abae78741c4445c3a24a7188f3a32ab67eb6a07f2602d"
    },
    {
      "card": {
        "id": "warrior.base.serum-tolerance",
        "name": "Serum Tolerance",
        "className": "Warrior",
        "band": "Base",
        "path": null,
        "sourceKind": "passive",
        "minimumClassLevel": 1,
        "acquisition": "selection",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "Always",
        "effect": "Serum Tolerance. Negative side effects printed on serum profiles do not affect you. Strain generation and Strain penalties still apply normally. This does not suppress drawbacks printed on mutation cards, Hero transformations or Mutation Overload.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4802,
          "originalText": "Serum Tolerance: You can consume serums without the normal toxicity effects that would affect others."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "fa39611615df3f6588a057acb603826b033f89dbe1a4703bdb7e7a6e08ca875e"
    },
    {
      "card": {
        "id": "warrior.base.serum-injection",
        "name": "Serum Injection",
        "className": "Warrior",
        "band": "Base",
        "path": null,
        "sourceKind": "active",
        "minimumClassLevel": 1,
        "acquisition": "selection",
        "activation": "Bonus Action",
        "cost": "Consume 1 prepared serum dose; +1 Strain",
        "rangeAndTarget": "Self",
        "duration": "3 rounds",
        "frequency": "At will while legal doses remain",
        "effect": "Serum Injection. Choose one equipped mutation and one prepared serum dose. Consume the dose, activate that mutation for 3 rounds and apply the serum profile for 3 rounds. Observe active-mutation limits, Strain legality and nonstacking same-profile bonuses.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4808,
          "originalText": "Serum Injection: Activate a prepared mutation serum as a bonus action, triggering its effects for 3 rounds."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "3ab2bfe1ad5c1d295ae2a7a868308ad9baf407f94684964d81edb492683dc507"
    },
    {
      "card": {
        "id": "warrior.arch.mutation-efficiency",
        "name": "Mutation Efficiency",
        "className": "Warrior",
        "band": "Arch",
        "path": null,
        "sourceKind": "passive",
        "minimumClassLevel": 3,
        "acquisition": "selection",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "Always",
        "effect": "Mutation Efficiency. You may maintain up to two equipped mutations active simultaneously instead of one. Activating a third mutation while two are already active requires choosing one active mutation to become dormant unless another explicit feature temporarily raises this limit. Mutation slots, serum costs, Strain and mutation durations remain unchanged.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4818,
          "originalText": "Mutation Efficiency: May have 2 active mutations at once (Lv 3)"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "d3452ae5d2a8040786772ea76f913adda7124e2c1440b697921b2ee3c4102c21"
    },
    {
      "card": {
        "id": "warrior.arch.overpressure-response",
        "name": "Overpressure Response",
        "className": "Warrior",
        "band": "Arch",
        "path": null,
        "sourceKind": "passive",
        "minimumClassLevel": 5,
        "acquisition": "selection",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "One equipped dormant mutation",
        "duration": "3 rounds or its shorter printed duration",
        "frequency": "Once per round",
        "effect": "Overpressure Response. When you take a critical hit, choose one equipped dormant non-Apex mutation and activate it without consuming a serum dose or gaining Strain. This activation must respect your normal simultaneous-active-mutation limit; if necessary, make another active mutation dormant. It grants no serum-profile benefit and cannot activate a mutation whose prerequisite you do not meet.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4820,
          "originalText": "Overpressure Response: Once per round, when struck by a critical hit, gain 1 free mutation activation"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "01f78bcb49a1cf5e0ce5c2bcaae49f136774afe835ad4779757224ea53395a57"
    },
    {
      "card": {
        "id": "warrior.arch.mutation-overload",
        "name": "Mutation Overload",
        "className": "Warrior",
        "band": "Arch",
        "path": null,
        "sourceKind": "active",
        "minimumClassLevel": 3,
        "acquisition": "selection",
        "activation": "Bonus Action",
        "cost": "+2 Strain",
        "rangeAndTarget": "Your currently active mutations",
        "duration": "2 rounds; backlash until end of following turn",
        "frequency": "1/short rest",
        "effect": "Mutation Overload. For 2 rounds, enhance each currently active mutation once: an AC, DR, attack, save or flat-damage bonus increases by 1; a movement or reach bonus increases by 5 feet; or one mutation damage/healing roll gains +1d4. Immunities, target counts, resource generation and action grants cannot be increased. When Overload ends, you suffer -1 on attack rolls and saving throws and -5 feet Speed until the end of your next regular turn. This activation is illegal if +2 Strain would exceed the Strain cap.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4827,
          "originalText": "Mutation Overload: Push your mutations beyond safe limits, gaining significantly enhanced effects for 2 rounds followed by exhaustion."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "17434e4d9492799006297db7be8c411a853a0c7b5781ed727b0c457b5a2a77f9"
    },
    {
      "card": {
        "id": "warrior.arch.serum-cocktail",
        "name": "Serum Cocktail",
        "className": "Warrior",
        "band": "Arch",
        "path": null,
        "sourceKind": "active",
        "minimumClassLevel": 5,
        "acquisition": "selection",
        "activation": "Bonus Action",
        "cost": "Consume 2 different prepared serum doses; +2 Strain",
        "rangeAndTarget": "Self",
        "duration": "3 rounds",
        "frequency": "1/short rest",
        "effect": "Serum Cocktail. Choose two different prepared serum profiles, consume both doses and apply both profiles to yourself for 3 rounds while activating one eligible equipped mutation. Same-stat bonuses use only the stronger value. Both profile side effects apply unless Serum Tolerance suppresses them. This activates only one mutation and therefore differs from Serum Overclock. It is illegal if the resulting Strain would exceed 3.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4828,
          "originalText": "Serum Cocktail: Combine two different serums for a hybrid effect, though with increased strain on your body."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "647e7cf03d689985ee3b9a3a1adecd15bd52b8ae3582e481cb431526d89c9147"
    },
    {
      "card": {
        "id": "warrior.hero.wardborn.serum-sharing",
        "name": "Serum Sharing",
        "className": "Warrior",
        "band": "Hero",
        "path": "Wardborn",
        "sourceKind": "passive",
        "minimumClassLevel": 12,
        "acquisition": "selection",
        "activation": "Bonus Action",
        "cost": "Consume 1 prepared serum dose",
        "rangeAndTarget": "One willing living ally you touch",
        "duration": "3 rounds",
        "frequency": "At most once per ally per short rest",
        "effect": "Serum Sharing. Inject one willing ally with a diluted prepared serum. The ally receives half of each positive numeric benefit of that serum profile, rounded down with minimum 1, for 3 rounds; nonnumeric immunities become advantage on the relevant save instead. The serum activates no mutation in the ally. The ally gains 1 Strain for this pilot and suffers the profile's printed side effect. Your Serum Tolerance does not protect the ally.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4849,
          "originalText": "Serum Sharing: You can safely inject allies with diluted versions of your serums, granting them 50% of the benefits."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "0c90a4ae67736741bf6cadee0d5a43311b2c879976a87f008704cfba026cac17"
    },
    {
      "card": {
        "id": "warrior.hero.wardborn.bulwark-mutation-tree",
        "name": "Bulwark Mutation Tree",
        "className": "Warrior",
        "band": "Hero",
        "path": "Wardborn",
        "sourceKind": "active",
        "minimumClassLevel": 10,
        "acquisition": "selection",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "When selected",
        "effect": "Bulwark Mutation Tree. Unlock the Wardborn-specific mutations Spinal Plating, Adrenal Overwatch and Living Cover as eligible mutation choices. They occupy normal mutation slots, require serum activation unless their card says otherwise, and obey all active-mutation, tier and Strain rules. Selecting this card does not automatically equip or activate any of them.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4854,
          "originalText": "Bulwark Mutation Tree: Unlocks mutations like:"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "913525b5872727368eb0a555f35713b4f1d4b5e8697440648f93f971c09fdedb"
    },
    {
      "card": {
        "id": "warrior.hero.ironskin.serum-recycling",
        "name": "Serum Recycling",
        "className": "Warrior",
        "band": "Hero",
        "path": "Ironskin",
        "sourceKind": "passive",
        "minimumClassLevel": 12,
        "acquisition": "selection",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "One serum dose you are consuming",
        "duration": "Instantaneous",
        "frequency": "At most once per turn",
        "effect": "Serum Recycling. Whenever you would consume a prepared serum dose, roll a d20. On 17-20, the dose is not consumed after its effects resolve. Strain and all other costs still apply. A preserved dose remains in its original prepared profile and cannot increase your serum reserve above its normal capacity.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4876,
          "originalText": "Serum Recycling: 20% chance to not consume a serum when activating a mutation."
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "df2e9fe9ee501e480e834329bc224970504e027e479589b8875657de045ad74f"
    },
    {
      "card": {
        "id": "warrior.hero.ironskin.gore-mutation-tree",
        "name": "Gore Mutation Tree",
        "className": "Warrior",
        "band": "Hero",
        "path": "Ironskin",
        "sourceKind": "active",
        "minimumClassLevel": 10,
        "acquisition": "selection",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "When selected",
        "effect": "Gore Mutation Tree. Unlock the Ironskin-specific mutations Gore Maw, Reinforced Joints and Shard Skin as eligible mutation choices. They occupy normal mutation slots and obey serum activation, concurrency, tier and Strain rules. Selecting this card equips or activates none of them automatically.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4881,
          "originalText": "Gore Mutation Tree: Unlocks mutations like:"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "8a23a00140dd203deb82f019b4b969ab90185bff7def6a5680fc95dda12c6943"
    },
    {
      "card": {
        "id": "warrior.hero.dreadspawn.aberrant-mutation-tree",
        "name": "Aberrant Mutation Tree",
        "className": "Warrior",
        "band": "Hero",
        "path": "Dreadspawn",
        "sourceKind": "active",
        "minimumClassLevel": 10,
        "acquisition": "selection",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "When selected",
        "effect": "Aberrant Mutation Tree. Unlock the Dreadspawn-specific mutations Whip-Tendon Limbs, Soul Spike Carapace and Hemophage Core as eligible mutation choices. They occupy normal mutation slots and obey serum activation, concurrency, tier and Strain rules. Selecting this card does not equip or activate any of them.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4908,
          "originalText": "Aberrant Mutation Tree: Unlocks:"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "750619db361277a3df1fb6db8b671533e3dcb60fb6ae783b8199bb04e853d31d"
    },
    {
      "card": {
        "id": "warrior.hero.dreadspawn.apex-aberration-1-day",
        "name": "Apex Aberration (1/day)",
        "className": "Warrior",
        "band": "Hero",
        "path": "Dreadspawn",
        "sourceKind": "active",
        "minimumClassLevel": 14,
        "acquisition": "selection",
        "activation": "Bonus Action",
        "cost": "+2 Strain",
        "rangeAndTarget": "Self",
        "duration": "2 rounds",
        "frequency": "1/long rest",
        "effect": "Apex Aberration. For 2 rounds increase Strength by 4, maximum 24 from this feature. You are immune to the effects and damage of hostile rank-3-or-lower spells, but not higher-rank spells, non-spell magical abilities or friendly spells you choose to accept. Whenever your weapon or natural attack hits, the target makes a Wisdom save; on failure it is Frightened until the end of its next turn. This activation is illegal if +2 Strain would exceed the cap.",
        "source": {
          "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
          "line": 4913,
          "originalText": "Apex Aberration (1/day): You transform for 2 rounds:"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "8df19876a2c5a23fd3bd0f68330ff5376b31cd7e783d0bf271905a9193a34d09"
    },
    {
      "card": {
        "id": "warrior.supplement.serum-overclock",
        "name": "Serum Overclock",
        "className": "Warrior",
        "band": "Arch",
        "path": null,
        "sourceKind": "progression",
        "minimumClassLevel": 9,
        "acquisition": "automatic",
        "activation": "Bonus Action",
        "cost": "Consume 2 prepared serum doses; +2 Strain",
        "rangeAndTarget": "Self",
        "duration": "3 rounds",
        "frequency": "1/short rest",
        "effect": "Inject two different prepared serum profiles simultaneously and activate up to two eligible equipped mutations, respecting your active-mutation limit. Resolve both profile effects; same-stat bonuses use the stronger. Overclock is illegal if the resulting Strain would exceed 3.",
        "prerequisite": "Warrior 9, Strain 1 or lower, two prepared serum doses",
        "source": {
          "line": 4793,
          "reference": null,
          "originalText": "| 9 | Serum Overclock: Inject 2 serums at once |",
          "status": "source-derived"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "59adf9c7d711f635dc195da40a827238d67976b45c49a7a85d861d3b13296c17"
    },
    {
      "card": {
        "id": "warrior.supplement.awakened",
        "name": "Awakened",
        "className": "Warrior",
        "band": "Base",
        "path": null,
        "sourceKind": "brutalityState",
        "minimumClassLevel": 1,
        "acquisition": "supplement",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "While BT remains at least 1",
        "frequency": "State",
        "effect": "Once per encounter, when a serum activation would add Strain, reduce that Strain gain by 1, minimum 0. This represents reduced activation cost; it cannot reduce Serum Cocktail or Mutation Overload below 1 Strain.",
        "prerequisite": "BT 1+",
        "source": {
          "line": 5066,
          "reference": null,
          "originalText": "| Awakened | Deal 25% of max HP as damage | Mutations cost 10% less to activate |",
          "status": "source-derived"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "a444e43049f5644a0dd260f7af13170fba99d4bf75e43cb6df30f1e6cf3928b6"
    },
    {
      "card": {
        "id": "warrior.supplement.overdrive",
        "name": "Overdrive",
        "className": "Warrior",
        "band": "Base",
        "path": null,
        "sourceKind": "serumProfile",
        "minimumClassLevel": 1,
        "acquisition": "supplement",
        "activation": "Via Serum Injection",
        "cost": "Dose consumption and normal Strain",
        "rangeAndTarget": "Injected creature",
        "duration": "3 rounds",
        "frequency": "Per prepared dose",
        "effect": "Gain +2 to Strength or Dexterity, chosen on preparation, and +10 feet Speed. Side effect: -1 AC for the duration. Serum Tolerance suppresses the side effect but not Strain.",
        "prerequisite": "Prepared serum dose",
        "source": {
          "line": 5053,
          "reference": null,
          "originalText": "| Overdrive | +2 STR/DEX | +10% Speed | 3 rounds | -10% Defense |",
          "status": "source-derived"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "72201696e91df756500bcc810d652abd2a97932234cb774b2ce6acbaeb9e6dfa"
    },
    {
      "card": {
        "id": "warrior.supplement.sanguine-surge",
        "name": "Sanguine Surge",
        "className": "Warrior",
        "band": "Base",
        "path": null,
        "sourceKind": "serumProfile",
        "minimumClassLevel": 1,
        "acquisition": "supplement",
        "activation": "Via Serum Injection",
        "cost": "Dose consumption and normal Strain",
        "rangeAndTarget": "Injected living creature",
        "duration": "3 rounds",
        "frequency": "Per prepared dose; same creature cannot receive its healing more than once per short rest",
        "effect": "On injection regain 2d6 HP and gain +10 feet Speed for 3 rounds. Side effect: when the profile ends gain 1 additional Strain, maximum 3. Serum Tolerance suppresses that ending side effect. This healing removes no Wounds and cannot operate on a dead creature.",
        "prerequisite": "Prepared serum dose",
        "source": {
          "line": 5055,
          "reference": null,
          "originalText": "| Sanguine Surge | Heal 2d6 | +10 ft speed | 3 rounds | Increased Hunger |",
          "status": "source-derived"
        },
        "designStatus": "provisional-playtest",
        "spellRank": null
      },
      "sourceObjectSha256": "8f4cb446c0ec4b28716532e2f3decc1918c85c4e803f41ec03d44fa427b27d5b"
    }
  ],
  "gameplayPath": "docs/mechanics/GAMEPLAY_LOOP_CANON.md",
  "gameplaySha256": "ba5ebcbdb77a27cb8fde88ba13fd05216d6808b10f7b58b64e6cba54eed62066",
  "gameplaySections": [
    {
      "heading": "## 5. Opening clock and Watches",
      "exactText": "## 5. Opening clock and Watches\n\nThe Opening lasts 2,400 hours. At hour 1,200, the Horn announces the point of no return. Expeditions still inside must withdraw or accept the risk of being sealed below for ten years.\n\nA Watch advances the Opening clock by eight hours. A normal day contains:\n\n- Two active Watches.\n- One Rest Watch for each character.\n\nA character assigned to work during their scheduled Rest Watch gains **Rest Debt**. An attempted Rest Watch interrupted before completion also creates Rest Debt after the emergency scene ends.\n\nRecord a two-Watch countdown. The character must complete one full Rest Watch before the end of the second following Watch. At the end of that second Watch, an unpaid debt causes 1 Strain and remains owed until a full Rest Watch is completed. A character can owe only one Rest Debt at a time; missing another scheduled Rest while already indebted immediately causes 1 Strain and resets the countdown to two Watches. Completing the owed Rest clears the debt. A character cannot remove Strain until completing a safe Rest Watch.\n\n### Short Rest\n\nA Short Rest takes one hour. A character can benefit from no more than two Short Rests between Long Rests.\n\n- Spend Hit Dice as permitted by class rules.\n- Recover one-quarter of maximum RP, rounded down, minimum 1 for a character with an RP pool.\n- An Oracle regains 1 Revelation Charge, up to maximum.\n- End effects that specify a Short Rest.\n\n### Long Rest\n\nA Long Rest occupies one full Watch and can benefit a character only once per twenty-four hours.\n\n- Restore HP according to the Player Rulebook.\n- Restore RP and Revelation Charges.\n- Recover half expended Hit Dice, rounded up.\n- Remove 1 Strain in a secure camp or Haven.\n- Wounds require treatment; a Long Rest alone does not remove them.\n\n"
    },
    {
      "heading": "### Supply",
      "exactText": "### Supply Units\n\nOne Supply Unit sustains one Medium character for one day and includes food, water, fuel, and ordinary camp consumables. Small characters still consume one unit; Large characters consume two.\n\nAt the end of each twenty-four hours, consume Supply equal to the Expedition's daily requirement.\n\nIf the Expedition cannot pay the full requirement, every unsupported character gains 1 Strain and cannot remove Strain that day.\n\n"
    },
    {
      "heading": "### Strain",
      "exactText": "### Strain\n\nStrain represents exhaustion, sleep debt, hunger, exposure, and sustained magical stress.\n\n| Strain | Effect |\n|---:|---|\n| 0 | No penalty |\n| 1 | -1 initiative and expedition checks |\n| 2 | Speed -10 ft.; -1 attacks and saves |\n| 3 | Disadvantage on expedition checks; cannot Dash twice consecutively |\n| 4 | Maximum HP reduced by 25% |\n| 5 | Incapacitated except for slow travel and Rest |\n| 6 | Death or permanent collapse, as appropriate to the cause |\n\nA secure Long Rest removes 1 Strain. Haven care removes all ordinary Strain after one full day. Specific conditions may require treatment.\n\n"
    }
  ],
  "core": {
    "path": "books\\player\\Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
    "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
    "paragraphIndex": "zero-based all w:p descendants",
    "paragraphs": [
      {
        "paragraph": 8512,
        "text": "Gain access to a patron, criminal, noble, or expedition contact."
      },
      {
        "paragraph": 8513,
        "text": "Morale rest"
      },
      {
        "paragraph": 8514,
        "text": "A safe evening of chosen recreation removes 1 Strain, never a Wound."
      },
      {
        "paragraph": 8515,
        "text": "Protection contract"
      },
      {
        "paragraph": 8516,
        "text": "Workers or house hire security, healers, and legal advocates."
      },
      {
        "paragraph": 8517,
        "text": "Blackmail file"
      },
      {
        "paragraph": 8527,
        "text": "Quickglass"
      },
      {
        "paragraph": 8528,
        "text": "Gain +10 ft. speed and advantage on initiative for 10 minutes."
      },
      {
        "paragraph": 8529,
        "text": "Afterward, suffer 1 Strain and disadvantage on Dexterity checks for 1 hour."
      },
      {
        "paragraph": 8530,
        "text": "13"
      },
      {
        "paragraph": 8531,
        "text": "Restricted"
      },
      {
        "paragraph": 8532,
        "text": "25 gp"
      }
    ]
  }
}
