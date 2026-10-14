# Eight rank-2 Conjuration spells — exact manuscript review

Please review these exact cards against your source conference and current shared rules. Approve, or supply exact required repairs before promotion. Currentcatalog144/704 remains unchanged pending review. Eight original placements/Core blocks and seven actual class-access rows each are preserved. This is authored tabletop procedure approval, not effect-runtime, bestiary-CR, numerical-balance or whole-game certification. Please keep response under16,000characters.

Exact-card decisions/clarifications for attention:
- Air Pet keeps sourceAC15/HP20/TWO1d6attacks with one commandedoffensiveActionconsumingallownercompanionoffense. Ordinaryavailablemovementcanoccurbetweenattacks, noextramovement. NEW20lbbodymass forcarrying/Petrified accounting; nohands/tool/cargocapacitygranted. Attack/savesuseownerinterfacebutHP/damagefixed. Noautonomousopportunityattack/freeHelpadvantage.
- Barrage one-targetDEXhalf2d8withnoextraabilities,rank2valueversusBoltflaggedforfuturebalance.
- Shield of Sparks capturesretaliationeligibilityatattack-rollresolution:30ft+LoE,anyattackrollhitormiss,thenearnedpacketafterattackincludingconc/lifeconsequences. Latermovementdoesnoterasecapturedeligibility. Separate allcastertarget/attacker/roundguard. Noelectricgearorprocchains.
- Satchelfiniteammo quantities/masses followV6;tool<=5lb. YourAC11/HP5bag is1lbpluscontents. NEWindividualammoAC10/HP1,toolAC12/HP3 ifseparatelytargeted;destroyedcontentsdon'trefillorautomaticallydamagebag. Allconjuredcontentsdependonbag/endclock. Yourcommitted-useexceptionisboundedtoonecurrentlyresolvingattack/immediatecheck, notallfuturestagesofalongproject. No unrelateduserobjects stored/deleted.
- Minor Planar Ally explicitlyNEWuncertifiedCR1-roleprofile,notcanonbestiaryrewrite;actualextraplanarsummontag/noinferredothercreaturetype. NEWMedium100lbbody,ordinaryhands,30lbAND3Loadcarriage clarifiesbody/equipmentandnoncombattaskswithoutinventingSTR. Sourceprofile'schecks+0/savesownerPBremain. Borrowedordinarycargoisconserved/droppedwhenallyends, nofreeHelp/autonomousoffense/planehopping/loot. Confirm thisfiniteCR1-rolecompletion is acceptable asplaytestcandidatewhileactualCR/balance remainsuncertified.
- Welloncecreationuse/caster andoncereceipt/recipientbetweenactualbeneficiallongrests; reserve1d4TOTAL onceatresolution. Use/costscommittedbeforeprevention,actualmaxcaps/waste/zero-drawillegal. Castercanreceivebutuseseparatecreation/receipt. No caprefreshfromcopies/suppression/dispelorretune. Kindle/ModRodledgersstayseparate.
- GreaterEmblem NEWexactcardgeometry10ftradiussphere; surfacesfollowtheiractualmovableobjectlikeordinaryEmblem, freepointfixed. Knownordinaryfactionname/symbolnoimportedpositive/member/invocationgate. Actualdynamicmembershiponly,+1savesstrongestflat,noReport/authority/lighting. Sourceconferencesurfacevsfixedpointwasimplicit: pleaseconfirmmovementexplicitlyorrepair.
- AlignmentWeaponcurrentwielder/targetactualrecordsevenwhenhiddenfromplayers,oneopposedrecordedaxisqualifies;normalcrit4d6+STRifopposed(base+riderbothdouble),noonce-turncap. Printedgeneric-suppressiondefault confinedtothiscard:basephysicalweaponremainsunlesssuppressionactuallyremovesobjects;no magicalqualification/riderwhile suppressed, clocks/HPnotreset. No generic rewriteofothersummon/weaponcards.

After any exact required repairs, please state whether all eight may be promoted. I will add a shared companion-rule clarification for the specific Air Pet two-attacks-in-one-action exception if approved, without editing frozen CLASS_PLAYTEST_RULES.md.

## Exact candidate

Candidate byte SHA256: `68d1521d5a27fc704eb8d92f7e2249cd10471782ae4aeabbfd325af178b5f44e`

```json
{
  "status": "LOCAL CANDIDATE — SOURCE-RECONCILED; exact manuscript review pending; NOT SELECTABLE",
  "scope": "Eight rank-2 Conjuration identities, eight original placements/Core blocks; actual seven-class access retained. Provisional authored rules, not runtime, bestiary-CR or numerical-balance certification.",
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
  ],
  "spells": [
    {
      "id": "summon-air-pet",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One unoccupied space you can perceive within range.",
      "duration": "Concentration, up to 1 minute. If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual phase through initiative changes, absence or death. Outside initiative, expires 60 seconds after application; retain that absolute deadline on entering initiative. An already-passed start never counts. Ends earlier if concentration ends or the pet reaches 0 HP.",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "No initial roll. On a legal damaging command the pet takes one offensive action containing two separate melee spell attacks, using your actual casting-class spell attack bonus, reach 5 feet. Each hit deals 1d6 slashing damage with no ability damage modifier; resolve ordinary attack/critical/defense rules separately.",
      "effect": "Summon one Small air elemental with AC 15, HP 20, walking Speed 30 feet, saves equal to owner PB, other checks +0, ordinary sight/hearing, and a body mass of 20 pounds. It understands your spoken commands but has no speaking language or telepathy. It acts immediately after you. While within 60 feet and able to perceive your command, your Bonus Action commands movement plus its two-attack offensive action or one basic legal nondamaging action. Both attacks may target one creature or separate legal creatures within reach at each attack. Any movement between attacks uses its normal available movement, not extra movement.",
      "scaling": "Only the expressly printed owner PB saves and actual spell attack bonus change with the caster. AC15, HP20, two attacks and 1d6 damage remain fixed; no S-dice progression.",
      "limitations": "The printed two attacks are a specific exception to the ordinary one-attack companion profile, not two Actions or two commands. Declaring this offensive action consumes the owner-wide one damaging companion action for that numbered round, including if attacks miss or the second attack cannot occur; no other companion receives offense from the remaining portion. Without a command it may defensively move and Dodge, with no autonomous attacks. It shares the owner-wide Bonus Action companion command budget. Air grants no flight, hover, gaseous passage, resistance, immunity, special senses or borrowed monster statistics. It grants no hands/tool operation, cargo carriage, free Help advantage, independent spellcasting, corpse, loot, resource/death triggers, free resummoning or autonomous opportunity attack. One pet per caster; at 0 HP or concentration end it vanishes. Recasting pays a new cast. Carrying this pet uses its actual printed mass and the body/carrying guide; it creates no permanent material. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F/concentration 1 minute, AC15/HP20 and two 1d6 slashing attacks. NEW: Small/walking30/ordinary senses, command/profile details and the bounded two-attacks-in-one-action exception consuming all owner companion offense. Exact-card completion adds 20-pound body mass and no ungranted hands/cargo capacity. AC, HP and damage do not scale; PB/actual spell attack follow the printed owner interface.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 136,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Summon Air Pet",
            "effect": "Elemental pet: HP 20, AC 15, 2 attacks at 1d6 slashing.",
            "source_paragraph": 9148,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Concentration, up to 1 minute",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Damage",
              "Summoning"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Summon Air Pet",
          "school": "Conjuration",
          "level": 2,
          "summary": "Elemental pet: HP 20, AC 15, 2 attacks at 1d6 slashing."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "elemental-barrage",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One creature you can perceive within range.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "The target makes a Dexterity save against your spell DC. Roll 2d8 once: failure takes full damage; success takes floor(the rolled damage/2). Then apply its ordinary defenses.",
      "effect": "Choose fire, cold or lightning when casting; deal the printed 2d8 damage of that chosen type to the target under the stated save.",
      "scaling": "None.",
      "limitations": "The name grants no additional bolt, target or area. No Burn, slow, chain, terrain effect, persistent field, object damage or automatic spread. The spell supplies no attack roll, critical hit or ability modifier to damage. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F/instantaneous, 2d8 and fire/cold/lightning choices. NEW: one target and Dexterity half resolution where Core gives only generic resolution. This differentiates it from rank-1 Elemental Bolt without silently increasing source damage or adding targets. Relative rank-2 value remains an explicit balance question.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 137,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Elemental Barrage",
            "effect": "2d8 damage (choose fire, cold, lightning).",
            "source_paragraph": 9149,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Damage"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Elemental Barrage",
          "school": "Conjuration",
          "level": 2,
          "summary": "2d8 damage (choose fire, cold, lightning)."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "conjure-shield-of-sparks",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One willing creature you can perceive within range, including yourself.",
      "duration": "Concentration, up to 1 minute. If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual phase through initiative changes, absence or death. Outside initiative, expires 60 seconds after application; retain that absolute deadline on entering initiative. An already-passed start never counts. Ends earlier if concentration ends.",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic ward application. When an attack roll actually resolves against the protected creature while this ward is active, hit or miss, it can earn the printed retaliation. A canceled declaration with no resolved attack roll does not qualify.",
      "effect": "The target gains +3 AC, using the strongest applicable flat AC bonus. At the instant an attack roll resolves against the active ward, if its attacker is within 30 feet of the protected target and has line of effect to that target, queue 1d4 lightning damage to that attacker. Finish the triggering attack and its damage, interception, life and concentration consequences, then resolve the already-earned packet even if those consequences ended the ward. Range and line of effect are captured at the qualifying roll; later movement does not retroactively erase the earned packet. Both melee and ranged attack rolls can qualify. Retaliation is limited to once per protected-target/attacker/numbered-round across all Shield of Sparks applications/casters; replacement does not reset the record.",
      "scaling": "None.",
      "limitations": "Only one Shield of Sparks affects a target across all casters; a successful new application ends the displaced application and releases only its old concentration dependency. Attacks from beyond the 30-foot retaliation reach or without the required line of effect still face the +3 AC if otherwise legal but generate no retaliation. The packet is new lightning damage, not a copied original attack, an attack roll or a hit by the protected creature. Ordinary defenses, temporary HP, concentration and death consequences apply. It cannot recursively trigger another Shield of Sparks, reflection/retaliation, resource gain, copied damage, derived healing, free Action/attack or generic on-hit rider absent an exact source expressly authorizing that interaction. No physical shield, hand/equipment requirement, electric field, extra illumination or condition is created. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F, +3 AC and 1d4 lightning to an attacker. CONFLICT RULING: finite 1-minute concentration ward replaces Instantaneous metadata; no physical shield is implied. NEW: willing recipient, all attack-roll types, trigger-time 30-foot/LoE retaliation qualification, queued after-attack resolution, all-caster replacement and persistent protected-target/attacker round cap.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 138,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Conjure Shield of Sparks",
            "effect": "+3 AC and reflects 1d4 lightning to attacker.",
            "source_paragraph": 9150,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Damage",
              "Summoning",
              "Ward"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Conjure Shield of Sparks",
          "school": "Conjuration",
          "level": 2,
          "summary": "+3 AC and reflects 1d4 lightning to attacker."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "summon-weaponry-satchel",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "Your free hand, or one legal unoccupied supporting space you perceive within range, for one conjured satchel.",
      "duration": "1 hour (3,600 seconds) after application; preserve the absolute deadline through initiative changes. Ends earlier on replacement, spell ending or satchel destruction.",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic creation. Choose exactly one content mode and all its choices at creation. Actual drawing, loading, using or handing over contents uses ordinary legal object and weapon interactions; casting grants no extra use or attack.",
      "effect": "Ammo mode creates either 20 arrows (1 pound total), 20 crossbow bolts (1.5 pounds), 20 sling bullets (1.5 pounds), or 50 blowgun needles (1 pound). They function as compatible ordinary ammunition, except attacks using them count as magical weapon attacks; there is no +X or extra damage. Each piece fired is expended and vanishes after that attack resolves, hit or miss. Tool mode instead creates one ordinary simple handheld tool of at most 5 pounds, chosen with the same eligibility as Summon Tool and weighing the actual ordinary tool weight. The satchel itself weighs 1 pound, has AC 11 and 5 HP; add remaining content mass when carrying it. Each ammunition piece has AC 10/1 HP and the tool has AC 12/3 HP if separately targeted. Destroying a content item consumes that item without refilling it or automatically damaging the satchel.",
      "scaling": "None.",
      "limitations": "One satchel per caster; successful recasting ends all that caster's earlier satchel contents. Its interior accepts only its own conjured contents; unrelated user property remains outside and is never deleted by this spell. Removed conjured contents remain dependent on this casting and vanish on expiry, spell end, replacement or satchel destruction. A piece already committed to an attack currently resolving, or a tool already used in an immediate check currently resolving, finishes that atomic resolution; this does not preserve it for later attacks, later checks or an entire ongoing project. No refilling, recovery of fired ammunition, sellable/crafting material, dismantling yield, copies or permanent stock. Ammo grants no weapon, attack, proficiency or loading/reload waiver. Tool mode grants no proficiency or numeric bonus and cannot make thieves' tools, a key, a combat weapon, powered or precision device, laboratory/alchemical kit, potion, reagent, ammunition, currency, rare material or expedition Supply. All ordinary hand/carrying/access rules apply; externally carried contents count in their actual custody, not again inside the bag. These are native HP objects; no Integrity track or HP/Integrity conversion is supplied. Damage/effects must actually be able to affect the relevant object; having HP grants no creature eligibility. No unstated resistance, immunity or organic-target eligibility is supplied. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F and magical ammunition OR tools usable for one hour. NEW: fixed finite mutually exclusive modes, one-satchel cap, no concentration, exact object profiles/custody and atomic-use ending rule. Ammo quantities/masses match the cited V6 equipment rows. The 1-pound satchel and separately targeted content AC/HP are explicit provisional completions; no infinite bag, weapon grant or permanent crafting stock.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 139,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Summon Weaponry Satchel",
            "effect": "Conjures magical ammo or tools usable for 1 hour.",
            "source_paragraph": 9151,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "1 hour",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Summoning"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Summon Weaponry Satchel",
          "school": "Conjuration",
          "level": 2,
          "summary": "Conjures magical ammo or tools usable for 1 hour."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "planar-ally-minor",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One unoccupied space you can perceive within range.",
      "duration": "10 minutes (600 seconds) after application; preserve the absolute deadline through initiative changes. Ends earlier at 0 HP, replacement or spell ending.",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "No initial roll. A commanded Planar Strike makes one melee spell attack using your actual casting-class spell attack bonus, reach 5 feet. On hit deal 1d8 of bludgeoning, piercing or slashing chosen and fixed at creation, with no added ability damage modifier. The strike counts as a magical attack while retaining that physical damage type.",
      "effect": "Summon one Medium Minor Planar Ally with AC 14, HP 24, walking Speed 30 feet, saves equal to owner PB, other checks +0, ordinary sight/hearing, and body mass 100 pounds. Its explicit tags are summoned and extraplanar; this spell supplies no additional creature-type classification or world-faction identity. It understands your spoken commands but has no speaking language or telepathy. It has ordinary hands suitable for simple object manipulation. It acts immediately after you. Within 60 feet and able to perceive your command, your Bonus Action can command movement plus its one strike or one basic legal action. Without a command it may defensively move and Dodge. It shares the owner-wide Bonus Action command and one damaging companion action per numbered round.",
      "scaling": "Only the expressly printed owner PB saves and actual spell attack bonus change with the caster. AC14, HP24, 1d8 damage and all other profile capacities stay fixed; no S progression.",
      "limitations": "For noncombat assistance it may carry no more than 30 pounds AND 3 Load, manipulate simple unattended objects with its hands, or Search using its actual +0 check; source-required proficiency is not granted. Ordinary object/cargo/time/action rules still apply. It has no autonomous offense or opportunity attack, free Help advantage, planar travel, flight, special senses, resistance/immunity, supernatural knowledge, telepathy, automatic scouting report, faction/legal authority, contracts, casting, free economic labor, loot, harvestable body, corpse or resource/death triggers. One ally per caster. At 0 HP, expiry or replacement it disappears; ordinary borrowed/carried property is conserved and drops at its last location under normal support/Falling rules. This is a NEW summon-only tabletop profile for the source's intended CR-1 role, not a certified CR-1 Monster Manual creature or a grant to choose any published monster. Do not relabel Umbrin Arachnid or fractional-CR creatures to qualify. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F, an extraplanar helper for 10 minutes, source CR1 promise retained as intended design role. SOURCE GAP: the bounded 67-entry public scan established no eligible exact-CR1 extraplanar profile. NEW: this finite Medium/AC14/HP24/Speed30/1d8 summon-only profile, nonconcentration duration, command/tasks and strict capability list; exact-card completion adds 100-pound body, usable hands, 30-pound AND3-Load carriage and conservation of ordinary cargo. CR/balance certification remains open; no canonical bestiary creature is rewritten.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 140,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Planar Ally (Minor)",
            "effect": "Summon a CR 1 extraplanar creature to assist for 10 minutes.",
            "source_paragraph": 9152,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "10 minutes",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Summoning",
              "Planar"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Planar Ally (Minor)",
          "school": "Conjuration",
          "level": 2,
          "summary": "Summon a CR 1 extraplanar creature to assist for 10 minutes."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "resonance-well",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One fixed point you can perceive within range and line of effect for a nonphysical pool of resonance.",
      "duration": "If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual phase through initiative changes, absence or death. Outside initiative, expires 60 seconds after application; retain that absolute deadline on entering initiative. An already-passed start never counts. Ends earlier if the spell is ended or a later successful allowed application replaces it.",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Before activation/payment confirm the caster's unused character-wide Resonance Well creation use. Spend it at legal cast start before the Counterspell window. On successful resolution roll 1d4 exactly once to establish the total RP reserve. This amount belongs to the entire Well, not each recipient.",
      "effect": "One creation use per character across classes/copies refreshes only at that character's actual beneficial completed long rest. A countered cast spends the use and creates no Well. A creature with an actual RP pool, including the caster, can spend an Action within 5 feet and line of effect to draw. Verify its unused character-wide Resonance Well receipt use since its own last beneficial completed long rest and a positive remaining reserve. At draw start choose a positive amount no greater than that reserve, spend the recipient use and Action, and subtract that amount immediately. At resolution restore the chosen amount, capped at actual RP maximum. Over-cap recovery is wasted; a full recipient can deliberately spend a positive draw and recover 0. Zero draw is illegal. A preventing interrupt refunds nothing.",
      "scaling": "None.",
      "limitations": "One Well per caster. Receipt use is shared across all Wells/casters/classes and refreshes only at the recipient's own beneficial long rest; creation and receipt are separate records, including when caster draws from their own Well. Kindle and Mod Rod keep their separate named ledgers: Well neither resets nor shares them. At reserve 0 the Well is inert until its endpoint. Re-entry, suppression, replacement, dispelling, copying or recovery prevention never rerolls/refills the reserve or restores spent uses. Suppression prevents drawing while applicable and does not pause duration; if drawing was already committed, a subsequent actual prevention leaves its amount/use spent. This fixed nonphysical resonance cannot be carried as water, harvested, sold, used as Supply, drawn at range or treated as a pooled RP maximum. It provides no physical support, hazard or damage despite the historical Damage tag. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F and a pool from which allies draw 1d4 RP. CONFLICT RULING: finite 1-minute nonconcentration pool replaces Instantaneous metadata; Damage tag grants no unprinted damage. NEW: one rolled total reserve, explicit Action/5-foot draw, caster inclusion, positive committed withdrawals and distinct creation/receipt limits per beneficial long rest. Source supplied no daily limit; both anti-farm limits are explicitly provisional additions, not recovered canon.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 141,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Resonance Well",
            "effect": "Create a pool that allies can draw 1d4 Resonance Points from.",
            "source_paragraph": 9153,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Damage",
              "Resonance"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Resonance Well",
          "school": "Conjuration",
          "level": 2,
          "summary": "Create a pool that allies can draw 1d4 Resonance Points from."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "faction-emblem-greater",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One fixed point or nonliving surface you perceive within range and line of effect. Choose an exact canonical factionId whose ordinary name/symbol you know; no reputation, membership or Faction Seal invocation gate is added.",
      "duration": "Concentration, up to 1 minute. If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual phase through initiative changes, absence or death. Outside initiative, expires 60 seconds after application; retain that absolute deadline on entering initiative. An already-passed start never counts. Ends earlier if concentration ends.",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic display. At each saving throw, the Director evaluates actual current membership and location/line of effect for the creature making the save; no roll or magical membership report is supplied by creation.",
      "effect": "Create a visible, nonphysical emblem at most 2 feet across. Its aura is a 10-foot-radius sphere centered on the emblem. A creature with an explicit actual membership record for that faction gains +1 to saving throws while within the aura and line of effect to it. This includes the caster only if actually eligible. Leaving the area or losing membership removes eligibility; entering or gaining membership permits it. A display placed on a movable nonliving object moves with that object; a free-standing point remains fixed. It emits no light, uses ordinary visibility, and needs no separate action to maintain the aura.",
      "scaling": "None.",
      "limitations": "One Greater Emblem per caster; successful recasting replaces the old display. The strongest applicable same-stat flat bonus applies: overlapping emblems, including different factions, never add multiple +1 bonuses to one save. Neutral/positive reputation alone is not actual membership, and missing membership is not presumed. The effect does not reveal membership, identity, reputation, rank, credentials, alignment, intent or hidden faction data. Director-held actual records can establish eligibility without revealing them; observers may draw ordinary deductions from events. No authority, allegiance, persuasion, prices, RP discounts, immunity, healing, resource gain, guaranteed belief, physical token or permanent crafting symbol is supplied. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F and a faction symbol granting benefits to actual members. NEW: precisely +1 saves, 10-foot spherical aura, 2-foot display, 1-minute concentration, known ordinary symbol/name, actual membership predicate and one-caster cap. The source gives no positive-reputation gate, so none is imported. Exact-card completion follows the reviewed ordinary emblem's fixed-point versus surface-following distinction; the aura follows only the actual emblem.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 142,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Faction Emblem (Greater)",
            "effect": "Conjure a powerful symbol that grants benefits to faction members.",
            "source_paragraph": 9154,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Summoning",
              "Faction"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Faction Emblem (Greater)",
          "school": "Conjuration",
          "level": 2,
          "summary": "Conjure a powerful symbol that grants benefits to faction members."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "alignment-weapon",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One willing creature's free hand, including your own, or an unoccupied space you perceive within range.",
      "duration": "Concentration, up to 1 minute. If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual phase through initiative changes, absence or death. Outside initiative, expires 60 seconds after application; retain that absolute deadline on entering initiative. An already-passed start never counts. Ends earlier if concentration ends or the weapon reaches 0 HP.",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic creation; casting grants no attack. Later attacks use the wielder's ordinary Strength weapon attack and Strength damage modifier, adding PB only with actual simple-melee proficiency. Resolve normal hits, misses, criticals and defenses.",
      "effect": "Conjure a spectral one-handed simple melee weapon: choose and fix bludgeoning, piercing or slashing; base 1d6 plus wielder Strength modifier; reach 5 feet; weight 3 pounds; AC15/HP5. It has no unstated Light, Finesse, Thrown, Versatile, Reach or other weapon property. Its attacks count as magical weapon attacks with the chosen physical type. On each successful hit compare the current wielder's actual current canonical alignment to that target's actual current alignment. At least one recorded exact opposite axis (Lawful/Chaotic or Good/Evil) adds 1d6 of the chosen physical damage type to that hit. Neutral is not opposite. Unrecorded/unknown axes supply no opposition; one recorded opposite axis suffices when the other is unknown. Records may be known to the Director without being known to the wielder. A normal critical doubles the base 1d6 and any qualifying alignment 1d6, while Strength remains flat.",
      "scaling": "None.",
      "limitations": "The bonus applies per qualifying hit, with no invented once-turn cap. Ordinary Attack Actions, actual Extra Attack, opportunity attacks and weapon riders apply only when their own requirements accept this weapon. A change of wielder changes later alignment comparisons but refreshes no resource. No alignment announcement, personality/belief change, oath ruling, forced allegiance or magical secret report is produced; observers may make ordinary deductions from damage/events. One weapon per caster; ordinary handing, dropping, disarming, anatomy and custody apply. At 0 HP or concentration end it disappears. It is not autonomous, saleable, crafting material, ammunition or permanent inventory. For this card, if generic suppression suppresses spell effects without removing conjured objects, the weapon remains usable at its base physical 1d6 profile but loses magical-weapon qualification and alignment bonus until suppression ends; duration/concentration obligations continue. A source explicitly dismissing conjured objects overrides that default. Suppression ending restores only properties of the still-existing unexpired weapon, not lost HP, duration, spent actions or previous-hit riders. These are native HP objects; no Integrity track or HP/Integrity conversion is supplied. Damage/effects must actually be able to affect the relevant object; having HP grants no creature eligibility. No unstated resistance, immunity or organic-target eligibility is supplied. A successful new application owns its own endpoint; stale cleanup of a prior application cannot end its replacement. A countered cast creates no replacement. Starting concentration still ends the caster's incompatible prior concentration before interruption. Known/prepared access, actual class rank/level, V/S/F components, line of effect, costs, concentration transitions, Dissonance/Refrain, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Total cover blocks originating line of effect and direct targeting. No generic upcast or unstated scaling.",
      "designNotes": "PRESERVED: Action/30 feet/V/S/F, created weapon and +1d6 against opposing alignment. NEW: reviewed Minor Weapon base physical profile, finite 1-minute concentration instead of Instantaneous metadata, current-wielder/current-target two-axis comparison, exact per-hit rider/critical handling and suppression default confined to this card. A missing axis is never guessed from species, faction, appearance or player beliefs.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourceCoreEntries": [
        {
          "index": 143,
          "original": {
            "school": "Conjuration",
            "level": 2,
            "name": "Alignment Weapon",
            "effect": "Create a weapon that deals +1d6 damage to creatures of opposing alignment.",
            "source_paragraph": 9155,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Damage",
              "Alignment"
            ],
            "rp_cost": 3
          }
        }
      ],
      "sourcePlacements": [
        {
          "name": "Alignment Weapon",
          "school": "Conjuration",
          "level": 2,
          "summary": "Create a weapon that deals +1d6 damage to creatures of opposing alignment."
        }
      ],
      "classAccessEvidence": {
        "Dragoon": {
          "rank": 2,
          "minimumClassLevel": 8,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Druid": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Mage": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Ranger": {
          "rank": 2,
          "minimumClassLevel": 5,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Shaman": {
          "rank": 2,
          "minimumClassLevel": 4,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Tinker": {
          "rank": 2,
          "minimumClassLevel": 6,
          "school": "Conjuration",
          "baseRpCost": 3
        },
        "Wizard": {
          "rank": 2,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 3
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_CONJURATION_RANK2_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    }
  ]
}
```
