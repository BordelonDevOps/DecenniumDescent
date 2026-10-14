# Exact39-source damage-sharing implementation review

Codex → Calibration Review. Please reply BELOW16,000 characters. Review this exact bounded helper, tests, guide and source binding contracts against your39-source proposal and six corrections. Current88 checks/186 conservation states PASS, plus39 exact originals preserved and2 supporting Tinker engines. Please challenge defects before closure; fullgame/all-source defense order/companion lifecycle remain open.

Concrete remaining questions:
1. Mandatory offers across stages: helper accepts one already legally selected operation, forbids retransfer of retained and transferred branches. Does post-defense mandatory Aegis/Final Stand preempt a pre-mitigation optional Bloodbond offer? Need explicit ordering without a hypothetical defense preview consuming Bloom/prevention twice. Proposed phase ordering: pre-mitigation offers first, and automatic-before-optional only among SAME-STAGE eligible offers; if premitigation transfer used, root guard suppresses postphase transfers. This is a clarification of earlier broadly worded mandatory priority and must be explicit if accepted. Alternatively author a coherent cross-stage procedure.
2. Crown ledger code allows one ordinary+one Crown in either order while Crown active; two ordinary never. Text 'second must Crown' intended permission rather than chronology? If Crown first, is ordinary later legal? Code uses total2/ordinary1 and originalsource state/target legality caller. Crown nominal healing entitlement committed before blocked target healing; no refill.
3. Device helper uses ONLY damage-to0 destruction, no organic Wounds/death saves. Supporting exact Tinkerengine1/2 below. Device reconstruction/companion lifetime remains separate open package. Is that sufficient bounded interface? Emergency transferred damage does not make drone hit by enemy attack; no retaliation consumer. Do not grant unsupplied destruction-resource rewards.
4. GuardianPulse free-counter guard has explicit no-free-attack/no-Action generation and waits full incomingattack resolution; can retarget a freecounter but cannot generate a further freecounter from it. Palmforcecounter NEWroot normaldefenses/no originalattackidentity, with no-free/action/copy guards. Review source restrictions and inherited flags rather than assuming anynewdamageisacopy.

The helper caller contract deliberately leaves ownership/acquisition, source costs/actions/range/willingness, active states, per-source cadence and source-native rider legality to the stated procedure. It is not a complete combat engine. One DamageRoot is ONE original target damage packet, NOT all targets of a cast. Root totals require completed terminal recipients and source qualification filters.


## Exact source contracts and supporting engines

{
  "status": "IN_REVIEW",
  "scope": "39 exact passages: damage transfer, prevention, retargeting, new damage and non-damage exclusions.",
  "supportingSources": [
    {
      "sourcePath": "data/public/class_playtests/tinker.json",
      "engineIndex": 1,
      "text": "At 1 automatically own one Anacite Drone: AC 13+INT modifier, HP 5+INT modifier+class level (minimum 1), flight 30 ft, ranged bolt 60 ft attack PB+INT for 1d6 piercing. Bonus Action commands one move and one attack or named module action; otherwise it Dodges and may follow you. On bolt hit roll d4; on 4 target CON save or cannot take Reactions through end next turn (Shock, no automatic Stun). All drones/turrets/scraplings share ONE damaging action per Bonus Action command per regular turn unless a card explicitly supplies a priced extra attack. No autonomous barrage. Drone is a construct, not immune to all conditions; poison/psychic immunity, no charm. Carry/retract it in 1 minute; no pocket extra world or passenger flight.",
      "sha256": "58f25de4d57c94d78536bc487deabc2d878e86224dfe9f544a029d4b79e51986"
    },
    {
      "sourcePath": "data/public/class_playtests/tinker.json",
      "engineIndex": 2,
      "text": "A destroyed drone remains 0 HP until repaired for 1 RP and 10 minutes with tools to half HP, once/short rest, or rebuilt during long rest to full. Ordinary repairing does not recharge devices, grant organic healing or trigger destruction bonuses. At 13 Dual Drone Protocols automatically chooses on each long rest either 2 basic drones each with one module, or one drone with 2 distinct modules. Still one command budget. Never more than 2 drones.",
      "sha256": "fc21b2a2fbc8af0dc175d90e8d8be5d9a90480a1c8aab1ec23d7aa0d6eebd01a"
    }
  ],
  "implementationEvidence": [
    "tools/redirection_playtest_rules.py",
    "docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json"
  ],
  "bindings": [
    {
      "bindingId": "cleric.hero.priest.cosmic-equilibrium",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.priest.cosmic-equilibrium",
      "sourceSha256": "511b9a9abd80cc33649c3a30d73c03139189a2443a25ae92b7905fbdb0251787",
      "sourceProcedure": {
        "name": "Cosmic Equilibrium",
        "activation": "Action",
        "cost": "7 RP",
        "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
        "duration": "Concentration, maximum 3 rounds",
        "frequency": "1/short rest",
        "effect": "Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other.",
        "prerequisite": null
      },
      "classification": "HEALING_REDIRECTION",
      "firstProposal": "Redirects genuine excess healing into new radiant damage; reverse conversion creates healing. Existing excess ledger/no-recursion rules apply.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.blood-sacrifice",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.blood-sacrifice",
      "sourceSha256": "073e2e574467aaae7193dfd80d27b74c4b3ccc4db41a45a4d59ab3208ad335fe",
      "sourceProcedure": {
        "name": "Blood Sacrifice",
        "activation": "Bonus Action",
        "cost": "Lose S+M actual HP from yourself or one willing ally within 5 ft",
        "rangeAndTarget": "Self or one willing ally within 5 feet",
        "duration": "Empowerment lasts until end of your next regular turn",
        "frequency": "1/short rest",
        "effect": "Blood Sacrifice. Tags: cultist, sacrifice, conviction. The chosen creature loses S+M actual HP; this loss cannot be reduced, redirected or transferred and cannot reduce it below 1 HP. The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain 1 Conviction. Your next damaging or healing Rite or Invocation before the end of your next regular turn adds 1d8 to one rolled damage or healing component. A creature must be willing unless the target is you.",
        "prerequisite": null
      },
      "classification": "DIRECT_HP_LOSS_EXCLUSION",
      "firstProposal": "HP cost; never damage or redirectable.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "crimson-agent.engine[4]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": 4,
      "sourceSha256": "d0684cf6ddc12e65f87fcef501168f0a256d9bd62bb8a9d1377c978a682eadb7",
      "sourceProcedure": {
        "text": "Veinweaves are self buffs unless their card expressly allows an ally. They require concentration and one may be active. Crimson Harmony is an explicit exception permitting two Veinweaves as one linked concentration burden; a failed concentration check ends both. A non-Veinweave concentration effect replaces the whole group. BG is spent on activation; no upkeep unless printed. Damage-sharing is redirection before mitigation, not extra damage: apply each recipient's own defenses once and never redirect the redirected portion again."
      },
      "classification": "PRE_MITIGATION_TRANSFER_ENGINE",
      "firstProposal": "Veinweave sharing splits before mitigation; each recipient defends once; no retransfer.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "crimson-agent.engine[5]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": 5,
      "sourceSha256": "f0909f1cf6ccaa56c2438dd0a9dd04e6b96640047167d9f79da6298b765de52a",
      "sourceProcedure": {
        "text": "The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds."
      },
      "classification": "DIRECT_HP_LOSS_EXCLUSION",
      "firstProposal": "Sacrifice guard; no damage pipeline.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "crimson-agent.hero.bloodweaver.bloodbond",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": "crimson-agent.hero.bloodweaver.bloodbond",
      "sourceSha256": "1113d2b822287bb66bb1759c1d7e674dbcb87534005a9e65e5111bb51b5c1263",
      "sourceProcedure": {
        "name": "Bloodbond",
        "activation": "Bonus Action",
        "cost": "2 RP",
        "rangeAndTarget": "One willing ally within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 3",
        "effect": "Create Bloodbond while both remain within 30 ft. When ally takes damage, you may use Reaction to redirect floor(one-quarter of pre-mitigation damage) to yourself; each recipient applies its own defenses once. Once/round when a paid technique heals you, ally gains M temporary HP. No recursive transfers.",
        "prerequisite": null
      },
      "classification": "PRE_MITIGATION_TRANSFER + TEMP_HP_RIDER",
      "firstProposal": "Quarter pre-mitigation split; each recipient defends once. Paid actual heal to owner can grant ally temp HP under reviewed healing predicate.",
      "transferContract": {
        "phase": "raw",
        "formula": "quarter",
        "flags": [
          "noRetransfer"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "crimson-agent.hero.bloodweaver.veinlock-tether",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": "crimson-agent.hero.bloodweaver.veinlock-tether",
      "sourceSha256": "2b7d8566a5825d619cde6e1a7c9ed56616c05c75df3864153fbc830fa33f5f96",
      "sourceProcedure": {
        "name": "Veinlock Tether",
        "activation": "Reaction",
        "cost": "1 BG",
        "rangeAndTarget": "Willing linked ally within 30 ft being damaged",
        "duration": "This damage only",
        "frequency": "Once/round",
        "effect": "While your Bloodbond or Vitality Link is active, redirect up to S+M damage to yourself before mitigation. This is an alternative to Bloodbond's quarter-sharing reaction, not an additional redirection. Redirected damage cannot be redirected again.",
        "prerequisite": null
      },
      "classification": "PRE_MITIGATION_TRANSFER",
      "firstProposal": "Alternative to Bloodbond on same event; chosen amount ≤S+M and available packet.",
      "transferContract": {
        "phase": "raw",
        "formula": "scale-mod",
        "flags": [
          "noRetransfer"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "mage.hero.elementalist.elemental-absorption",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mage.json",
      "sourceId": "mage.hero.elementalist.elemental-absorption",
      "sourceSha256": "4c696eef48c76379d0a6320cbac2b23324a197d1db8d6394b249a95750f1ec56",
      "sourceProcedure": {
        "name": "Elemental Absorption",
        "activation": "Reaction",
        "cost": "3 RP",
        "rangeAndTarget": "Self",
        "duration": "Until end of your next regular turn",
        "frequency": "Recharge 3 rounds",
        "effect": "Elemental Absorption. Tags: mage-spell, elementalist, protection. Trigger when you would take fire, cold or lightning damage. Gain resistance to that triggering damage type for the triggering event and until the end of your next regular turn. Your next damaging Mage spell before then adds 1d8 of the absorbed type to one damage roll; the bonus is lost after use or expiry. This Reaction spell clears an incompatible current Nuke Chain unless the absorbed type is your current Focus.",
        "prerequisite": null
      },
      "classification": "DAMAGE_PREVENTION",
      "firstProposal": "Adds resistance during ordinary defense stage; no transfer.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "mage.hero.lich.resonance-to-flesh",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mage.json",
      "sourceId": "mage.hero.lich.resonance-to-flesh",
      "sourceSha256": "5692ac39a7de506bcf79cfcb7273630cf1f18c27e6d663ae380f764b78e3e8b2",
      "sourceProcedure": {
        "name": "Resonance to Flesh",
        "activation": "Action",
        "cost": "Variable conversion",
        "rangeAndTarget": "Self",
        "duration": "Instantaneous",
        "frequency": "1/short rest",
        "effect": "Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions.",
        "prerequisite": null
      },
      "classification": "DIRECT_HP_LOSS_EXCLUSION / HEAL",
      "firstProposal": "Flesh→RP direct HP cost; RP→Flesh ordinary healing.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "mirrorsage.arch.mirror-shell",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mirrorsage.json",
      "sourceId": "mirrorsage.arch.mirror-shell",
      "sourceSha256": "9885dead731ef2fecb13b62062346b24887c7a4ec5ae54de7089512ee3fac586",
      "sourceProcedure": {
        "name": "Mirror Shell",
        "activation": "Reaction",
        "cost": "3 RP; 1 long-rest use",
        "rangeAndTarget": "A hostile spell targeting only you within 60 ft",
        "duration": "This spell",
        "frequency": "1/long rest",
        "effect": "After a successful save against the spell or after its spell attack misses, choose its caster; it makes WIS save or takes S d8 force. Original damage/control follow normal results. No copying arbitrary spell text or redirecting an area spell.",
        "prerequisite": null
      },
      "classification": "RETALIATORY_DAMAGE",
      "firstProposal": "No redirection. Original spell already missed/saved; new force packet against caster on failed WIS save.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "monk.engine[13]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": 13,
      "sourceSha256": "f6939b2e3293635fc6a652667c81e94984b14f8dfc5b43f3b86730e5b21f3584",
      "sourceProcedure": {
        "text": "Discipline Initiate is an optional Base selection. Choosing Tank does not grant five free Base abilities: it unlocks the four non-final Tortoise Discipline cards as additional Arch-selection options at their listed Monk levels. Final Form — Bastion of Breath is never a normal selection; at Monk 9 or the first later level when eligible it is gained automatically only if you chose Tank through Discipline Initiate and know at least three of Stone Shell Discipline, Redirecting Palm, Iron Shell Pulse and Echoing Guard. Tortoise Discipline remains compatible with any Hero path chosen later."
      },
      "classification": "EXCLUSION",
      "firstProposal": "Selection/progression only.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "monk.arch.tortoise.redirecting-palm",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.arch.tortoise.redirecting-palm",
      "sourceSha256": "a849f3afc8e0ea4efe8243f4d150c8d6830c8f2e65f7681bd98b893406ac407a",
      "sourceProcedure": {
        "name": "Redirecting Palm",
        "activation": "Reaction",
        "cost": "1 Ki; requires Discipline Initiate: Tank",
        "rangeAndTarget": "Triggering melee attacker and one other enemy within 5 feet of you",
        "duration": "Instantaneous",
        "frequency": "Once per round",
        "effect": "Redirecting Palm. Tags: arch, tortoise, discipline, counter. When a melee attack damages you, spend 1 Ki. Reduce the actual damage you take by half, rounded down. Choose one enemy other than you within 5 feet; it takes force damage equal to the amount prevented, maximum Monk level. If no second enemy is present, you still receive the reduction but redirect no damage.",
        "prerequisite": null
      },
      "classification": "DAMAGE_PREVENTION + RETALIATORY_DAMAGE",
      "firstProposal": "Prevent half post-defense packet; new force event = min(prevented,L).",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "monk.hero.enlightened-master.shared-breath",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.enlightened-master.shared-breath",
      "sourceSha256": "da2757b79d797600e0823eed7b615b9165e4c9d81c88fbb6affa18018695c52e",
      "sourceProcedure": {
        "name": "Shared Breath",
        "activation": "Action",
        "cost": "3 Ki + 2 RP",
        "rangeAndTarget": "One willing ally you touch",
        "duration": "Concentration, maximum 3 rounds",
        "frequency": "Recharge 4 rounds",
        "effect": "Shared Breath. Tags: hero, enlightened, link, weave. Link yourself to one willing ally. Once per round when either linked creature takes damage, the other may use its Reaction to take up to S+M of that damage instead; transferred damage cannot be reduced or redirected again. HP healing received by either creature also grants the other S HP once per round. The link ends if you separate by more than 30 feet.",
        "prerequisite": null
      },
      "classification": "POST_DEFENSE_TRANSFER + HEALING_ECHO",
      "firstProposal": "**NEW phase:** split post-defense/pre-tempHP; recipient gets no second mitigation. Existing causal-heal rules remain.",
      "transferContract": {
        "phase": "defended",
        "formula": "scale-mod",
        "flags": [
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "oracle.engine[14]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": 14,
      "sourceSha256": "53c0ee49032421d155b7c10311016dcaf92540557980c6b9553327dc3f2f575d",
      "sourceProcedure": {
        "text": "Copied, echoed, repeated or redirected damage/healing uses only the explicitly copied numeric component. It cannot repeat RC recovery, Prophecy Triggers, action grants, conditions, passive triggers, resource restoration or another copy effect unless the copying feature explicitly says otherwise."
      },
      "classification": "ENGINE_GUARD",
      "firstProposal": "Redirected numeric component carries no RC/Prophecy/passive/copy effects unless explicit.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "oracle.engine[29]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": 29,
      "sourceSha256": "b1f27c6149ea8d930f2b1ac29e2e5a73de9991ef98d53045b5ba8b4f055fde81",
      "sourceProcedure": {
        "text": "Extra attacks and echoed damage use base weapon/spell dice before critical-hit extra dice. A redirected damage event cannot be reduced a second time, reflected again or generate RC. Charmed alone does not grant command of a creature's actions."
      },
      "classification": "ENGINE_GUARD",
      "firstProposal": "Redirected damage cannot be reduced again/reflected again/generate RC.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "oracle.supplement.bones.bones-revelation-mastery",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.bones.bones-revelation-mastery",
      "sourceSha256": "14d4537572a0e9d37eb62850c1881097ec9da711640be7b293b0ff0918640577",
      "sourceProcedure": {
        "name": "Bones Revelation Mastery",
        "activation": "Passive",
        "cost": "0 RC",
        "rangeAndTarget": "One eligible known Bones Revelation",
        "duration": "Permanent",
        "frequency": "Choose one upgrade at Oracle 15",
        "effect": "Choose one mastery for a Revelation you know. Enhanced Marrow Drain: a living target hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Ledger's Command: may target up to 3 undead, but all controlled undead still share one Bonus Action command per round. Enhanced Unfinished Chorus: when its drain resolves, you may always redirect the healing to one ally within 3 tiles of you rather than yourself; its healing cap remains S+M.",
        "prerequisite": "Oracle 15; Mystery: Bones; Revelation Mastery"
      },
      "classification": "HEALING_REDIRECTION",
      "firstProposal": "Enhanced Chorus chooses ally as recipient of same heal; not a child/second heal.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.bloom-ward",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.bloom-ward",
      "sourceSha256": "0252c7014f1020fe92cdd9c29f41c074d47a6d8c6babf5665f939529eb6a0543",
      "sourceProcedure": {
        "name": "Bloom Ward",
        "activation": "Passive and Bonus Action",
        "cost": "0 RC",
        "rangeAndTarget": "Self; allies within 2 tiles; one ally within 3 tiles for bloom",
        "duration": "Passive permanent; bloom until consumed or 1 minute",
        "frequency": "Bloom 1/long rest",
        "effect": "Once per round when a living ally within 2 tiles receives HP healing from a paid or finite-use effect, add S HP to that healing. Reduce the first necrotic or poison damage you take each round by 1. Once per long rest place a protective bloom on one ally within 3 tiles. It absorbs the next 10+Oracle level damage dealt to that ally, then ends. When it ends, the ally gains +1 on saves against Frightened until the end of its next turn.",
        "prerequisite": "Oracle 1; Mystery: Life"
      },
      "classification": "DAMAGE_PREVENTION",
      "firstProposal": "Finite `(10+L)` prevention pool across packets; no transfer.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.life-linked",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.life-linked",
      "sourceSha256": "e85dca21885aff801dd806929d567b1bfc05ea921792d259bab918337ea74c80",
      "sourceProcedure": {
        "name": "Life Linked",
        "activation": "Action",
        "cost": "2 RC",
        "rangeAndTarget": "One willing living ally within 5 tiles",
        "duration": "2 rounds",
        "frequency": "At will while RC remains; one Life Link at a time",
        "effect": "Link yourself to the ally. Once per round when it takes damage, you may use your Reaction to transfer up to half that actual damage rounded down to yourself. Transferred damage keeps its type and cannot be redirected again. The ally reduces the first necrotic damage it takes each round by S. Once per round when one of your paid or finite Oracle effects restores HP to the linked ally, it regains an additional 1d4 HP. The link ends if you are more than 5 tiles apart. Apply mitigation to the original damage once before splitting. The transferred portion cannot be mitigated again and cannot generate recovery or retaliation triggers.",
        "prerequisite": "Oracle 6; Mystery: Life; selected Tier II Revelation"
      },
      "classification": "POST_DEFENSE_TRANSFER + HEALING_INTERFACE",
      "firstProposal": "Original mitigation once, then transfer up to half; no second mitigation/recovery/retaliation from transfer.",
      "transferContract": {
        "phase": "defended",
        "formula": "half-chosen",
        "flags": [
          "noActionGeneration",
          "noConditionTriggers",
          "noCopyGeneration",
          "noPassiveTriggers",
          "noRecoveryGeneration",
          "noReflection",
          "noResourceGeneration",
          "noRetaliation",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.engine[10]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": 10,
      "sourceSha256": "240e342dd180de5c960ceeabad4c9a8302f5c4a1d0ddcb324310c42669cc4c93",
      "sourceProcedure": {
        "text": "Oath integration limits: one paid Smite total per round, including the level-7 Reaction; one Oath-aura reactive event per round. Multiple damage-redirection options share one event per round unless Crown Undying expressly allows two. Apply original-target defenses once, then split actual damage; transferred damage cannot be mitigated again, reflected, redirected again or generate resources. This explicit rule supersedes wording that permits recipient defenses again."
      },
      "classification": "POST_DEFENSE_TRANSFER_ENGINE",
      "firstProposal": "Original defenses once; one paid Smite/round; one redirection event/round; no second mitigation/resource/retaliation.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.engine[14]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": 14,
      "sourceSha256": "b38dbf499f21d489b9848610ad2d5bd91a94b22ccb0a92ca613d3fbb6fa51c0d",
      "sourceProcedure": {
        "text": "For any one damage event choose exactly one Paladin redirection feature. Using it consumes the shared redirection allowance for that round. Crown Undying permits two DIFFERENT ally-damage events per round, but still only one redirection feature may modify each event."
      },
      "classification": "REDIRECTION_LIMIT_ENGINE",
      "firstProposal": "Exactly one Paladin redirection feature/event; Crown Undying two different events exception.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.base.protective-stance",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.base.protective-stance",
      "sourceSha256": "71f0333a1fa9bee2ffd004f8327f542364d847dfd263df4bf80cb0fe324de5c7",
      "sourceProcedure": {
        "name": "Protective Stance",
        "activation": "Bonus Action",
        "cost": "One short-rest use",
        "rangeAndTarget": "Self; adjacent ally",
        "duration": "Until start next turn",
        "frequency": "1/short rest",
        "effect": "Gain+1 AC. Once before end, Reaction interpose for adjacent ally hit by weapon: reduce its damage by S+M and take that much unpreventable damage yourself. Cannot redirect again or create resource/damage triggers. You must remain conscious.",
        "prerequisite": null
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Redirect min(S+M, remaining damage); protector gets unmitigated branch.",
      "transferContract": {
        "phase": "defended",
        "formula": "scale-mod-fixed",
        "flags": [
          "noDamageTriggers",
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-shared.profane-exchange",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-shared.profane-exchange",
      "sourceSha256": "bdd5dd43a3c0724146dadcb94d4907c4b169263f843b175a7e0f949404c32542",
      "sourceProcedure": {
        "name": "Profane Exchange",
        "activation": "Action",
        "cost": "5 RP and S+M actual HP",
        "rangeAndTarget": "One creature touched",
        "duration": "Instant",
        "frequency": "Recharge 3",
        "effect": "New rank 3 Forbidden spell. You must have more current HP than the unpreventable HP cost. Target CON save, 2 S d8 necrotic on failure, half success. HP loss cannot be reduced, redirected, refunded or used for another resource trigger.",
        "prerequisite": "Paladin 9; selected Oathbreaker inversion"
      },
      "classification": "DIRECT_HP_LOSS_EXCLUSION",
      "firstProposal": "Direct HP casting cost; not damage.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
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
      "classification": "DIRECT_HP_LOSS_EXCLUSION + HEAL",
      "firstProposal": "Donor loss outside damage pipeline; recipient ordinary healing packet.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-chain.chainbound-smite",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-chain.chainbound-smite",
      "sourceSha256": "e53ece673479a5f3c060e02521f0fc3941e296d875fd5dae13c785a8823741f4",
      "sourceProcedure": {
        "name": "Chainbound Smite",
        "activation": "Triggered",
        "cost": "Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8",
        "rangeAndTarget": "Creature hit by your melee weapon attack; one bonded ally in your aura",
        "duration": "Smite instantaneous; redirection once before your next turn",
        "frequency": "One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance",
        "effect": "The Smite deals radiant damage normally. After it resolves, choose one ally in your aura as bonded until the start of your next regular turn. Once before then when that ally takes damage, you may redirect up to max(3, actual Charisma modifier) of that damage to yourself. Redirected damage retains type and cannot be redirected again; the original target’s defenses apply once before transfer, with no further mitigation.",
        "prerequisite": "Paladin 3; Oath of the Chain"
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Later bond redirect capped by actual CHA/min3 and available post-defense damage; shared Paladin allowance.",
      "transferContract": {
        "phase": "defended",
        "formula": "cha-min3",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-chain.aura-of-bonds",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-chain.aura-of-bonds",
      "sourceSha256": "e27219c1a397ba23aafd062a1d00d12b6e445eef8fd126f58dba8dadde534db1",
      "sourceProcedure": {
        "name": "Aura of Bonds",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 chosen allies in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets at start of each turn",
        "effect": "Each selected ally reduces the first damage it takes each round by S. Multiple Aura of Bonds effects do not stack. This protection does not redirect damage and therefore does not trigger effects that require you to personally absorb damage.",
        "prerequisite": "Paladin 3; Oath of the Chain"
      },
      "classification": "DAMAGE_PREVENTION",
      "firstProposal": "Flat class reduction, no transfer; participates in ordinary defense stage.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-chain.linked-ward",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-chain.linked-ward",
      "sourceSha256": "e733a4a1f12c01e46fa3b2bd23f1f24f319fbb98dd023f68575687a51eb8fba2",
      "sourceProcedure": {
        "name": "Linked Ward",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "One willing ally in your Oath aura",
        "duration": "Concentration, maximum 3 rounds",
        "frequency": "At will while RP remains",
        "effect": "Mark one willing ally. Once per round when it takes damage, use your Reaction to redirect up to 2 times your actual Charisma modifier, minimum 2, of that damage to yourself. Redirected damage keeps its type and cannot be redirected again. If this redirected damage reduces you to 0 HP, the ally gains temporary HP equal to the amount you actually absorbed, maximum Paladin level+M.",
        "prerequisite": "Paladin 3; Oath of the Chain"
      },
      "classification": "POST_DEFENSE_TRANSFER + TEMP_HP_RIDER",
      "firstProposal": "Redirect capped amount; if transfer reduces Paladin to0, ally gains temp HP from Paladin branch's actualDamageDealt, capped L+M.",
      "transferContract": {
        "phase": "defended",
        "formula": "twice-cha-min2",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-chain.martyr-s-share",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-chain.martyr-s-share",
      "sourceSha256": "a4bd7d95ebde62b625301dc9c6061ae018522e75796bd4586372f6ce0eb28851",
      "sourceProcedure": {
        "name": "Martyr's Share",
        "activation": "Reaction",
        "cost": "5 RP",
        "rangeAndTarget": "One ally in your Oath aura taking damage",
        "duration": "Instantaneous",
        "frequency": "At will while RP remains",
        "effect": "Redirect half the ally's incoming damage, rounded down, to yourself. The ally takes the remainder. Redirected damage keeps its original type and cannot be redirected again. Your portion cannot be mitigated again after the original target’s defenses have applied. Effects attached to the original hit remain on the original target unless they explicitly depend on damage being dealt.",
        "prerequisite": "Paladin 9; Oath of the Chain"
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Redirect floor(postDefenseDamage/2), ally retains remainder; hit riders remain original target.",
      "transferContract": {
        "phase": "defended",
        "formula": "half",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-chain.final-stand",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-chain.final-stand",
      "sourceSha256": "a30dfed5eb1e4a23d6db023e47c779202eb684a6a71013dd12ddf7e5cbbf77e0",
      "sourceProcedure": {
        "name": "Final Stand",
        "activation": "Action",
        "cost": "10 RP",
        "rangeAndTarget": "One willing ally in your Oath aura",
        "duration": "Until start of your next regular turn",
        "frequency": "At will while RP remains",
        "effect": "Until the start of your next turn, all damage that would be dealt to the chosen ally is redirected to you instead. The redirected damage retains type, cannot be redirected again and cannot be mitigated again after the original target’s defenses apply once. If redirected damage reduces you to 0 HP, the ally immediately gains temporary HP equal to your Paladin level and resistance to all damage until the end of its next turn. This effect ends if you die outright.",
        "prerequisite": "Paladin 17; Oath of the Chain"
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Transfers full remaining post-defense packet but constrained to one Paladin redirection event/numbered round.",
      "transferContract": {
        "phase": "defended",
        "formula": "all",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": true,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-chain.unbroken-covenant",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-chain.unbroken-covenant",
      "sourceSha256": "513944a1ffe10dd0f5c74def4fee7a4d1248ee05fa668cceba673d4e1beb9f1c",
      "sourceProcedure": {
        "name": "Unbroken Covenant",
        "activation": "Bonus Action",
        "cost": "0 RP",
        "rangeAndTarget": "Your full Oath aura; up to 3 bonded allies",
        "duration": "3 rounds",
        "frequency": "1/long rest",
        "effect": "For 3 rounds Warden's Lock fills your entire current Oath aura. Choose up to 3 allies there as bonded. Each bonded ally uses your AC if it is higher and cannot be forcibly moved against its will. Whenever you redirect damage from a bonded ally to yourself, that ally gains temporary HP equal to half the actual damage you absorb, rounded down, maximum S+M per event. Temporary HP do not stack. This Final grants no extra Reactions.",
        "prerequisite": "Paladin 20; Oath of the Chain"
      },
      "classification": "TEMP_HP_RIDER + REDIRECTION_MODIFIER",
      "firstProposal": "Does not create redirect; when one occurs, ally temp HP = floor(Paladin transfer branch actualDamageDealt/2), cap S+M.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.king-s-smite",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.king-s-smite",
      "sourceSha256": "d477840b93208eb5bca4155cbd47f455ccac24e5625dfdd29affc907abcf4b8c",
      "sourceProcedure": {
        "name": "King's Smite",
        "activation": "Triggered",
        "cost": "Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8",
        "rangeAndTarget": "Creature hit by your melee weapon attack; one ally in your aura",
        "duration": "Smite instantaneous; temporary HP until lost; redirection passive while this Oath is active",
        "frequency": "One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance",
        "effect": "The Smite deals radiant damage normally. After it resolves, choose one ally in your aura; it gains temporary HP equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Separately, once per round when an ally in your aura takes damage, you may redirect up to 5 of that damage to yourself. Apply the original target’s defenses once, then transfer up to 5 of the remaining damage. Transferred damage keeps its type and cannot be reduced again, reflected, redirected again or generate resources.",
        "prerequisite": "Paladin 3; Oath of the Martyr King"
      },
      "classification": "POST_DEFENSE_TRANSFER + TEMP_HP",
      "firstProposal": "Smite temp HP uses root Smite actualDamageDealt; separate once/round post-defense redirect ≤5.",
      "transferContract": {
        "phase": "defended",
        "formula": "five",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.aura-of-the-crown",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.aura-of-the-crown",
      "sourceSha256": "8e16b8a024ca633bd4d3be4340aed54a46e4a2618dd1a4dfd70cda0742090783",
      "sourceProcedure": {
        "name": "Aura of the Crown",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 chosen allies in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets at start of each turn; redirect once per round",
        "effect": "Selected allies gain +1 on saving throws. Once per round when one selected ally takes damage, you may use your Reaction after that target applies its defenses once to redirect up to M of its remaining damage to yourself. The transferred amount cannot be reduced, reflected, redirected again or generate resources. This consumes the shared Paladin redirection allowance.",
        "prerequisite": "Paladin 3; Oath of the Martyr King"
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Reaction after target defense; redirect ≤M; shared allowance.",
      "transferContract": {
        "phase": "defended",
        "formula": "mod",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.crown-of-embers",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.crown-of-embers",
      "sourceSha256": "0ff07991fa0838522e96deb9434534c8c584850c6203ed3b47e8eeaf4246980f",
      "sourceProcedure": {
        "name": "Crown of Embers",
        "activation": "Bonus Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 allies in your Oath aura",
        "duration": "Until start of your next regular turn",
        "frequency": "1/short rest",
        "effect": "Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself.",
        "prerequisite": "Paladin 11; Oath of the Martyr King"
      },
      "classification": "DAMAGE_PREVENTION + POST_DEFENSE_TRANSFER",
      "firstProposal": "S prevention first; then at most one eligible Crown redirect from remaining packet, shared allowance.",
      "transferContract": {
        "phase": "defended",
        "formula": "level-mod",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.burden-shared",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.burden-shared",
      "sourceSha256": "2a0ff54276d9127ac30458bae7ea5dc0f1295b5ec34ca63bb5ce22efdabb29d1",
      "sourceProcedure": {
        "name": "Burden Shared",
        "activation": "Reaction when an ally takes damage",
        "cost": "5 RP",
        "rangeAndTarget": "Triggering ally and up to two other willing allies in your aura",
        "duration": "One damage event",
        "frequency": "While RP remains",
        "effect": "After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round.",
        "prerequisite": "Paladin 9; Oath of the Martyr King"
      },
      "classification": "POST_DEFENSE_MULTI_TRANSFER",
      "firstProposal": "One redirection operation can split ≤L+M among up to two willing recipients; no second mitigation/redirect/reflection/heal/resource.",
      "transferContract": {
        "phase": "defended",
        "formula": "level-mod",
        "flags": [
          "noHealingGeneration",
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 2
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
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
      "classification": "DAMAGE_PREVENTION + POST_DEFENSE_TRANSFER + HEAL",
      "firstProposal": "Two different ally events/round, L+M transferred total. Heal each protected ally from half Paladin branch actualDamageDealt, cap S+M; blocked/capped heal never refunds entitlement.",
      "transferContract": {
        "phase": "defended",
        "formula": "level-mod",
        "flags": [
          "noReflection",
          "noResourceGeneration",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "shaman.arch.ancestral-guardian",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.ancestral-guardian",
      "sourceSha256": "2017eae94ed31d166adb032bf4a724b44206a006fbf7fc23ec6eb0e6fa5aae8e",
      "sourceProcedure": {
        "name": "Ancestral Guardian",
        "activation": "Reaction",
        "cost": "2 RP",
        "rangeAndTarget": "Ally within 30 ft being damaged",
        "duration": "One damage instance",
        "frequency": "Recharge 3",
        "effect": "A guardian prevents S d8+M damage, minimum 0. It then vanishes and creates no companion action, corpse or refund. Cannot prevent sacrifice/trauma or redirect prevented damage into another trigger.",
        "prerequisite": null
      },
      "classification": "DAMAGE_PREVENTION",
      "firstProposal": "Prevent min(Sd8+M, available damage); no transfer/corpse/refund.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "soldier.hero.champion.selfless-guardian",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/soldier.json",
      "sourceId": "soldier.hero.champion.selfless-guardian",
      "sourceSha256": "1ee9c213d3529b63f88c35415e680695e87faf9a6e5459903c12ebcf04c25c56",
      "sourceProcedure": {
        "name": "Selfless Guardian",
        "activation": "Reaction",
        "cost": "0",
        "rangeAndTarget": "One adjacent ally taking direct weapon damage",
        "duration": "One hit",
        "frequency": "Once/round",
        "effect": "Redirect up to S+M of that damage to yourself. Redirected damage cannot be reduced, redirected again or trigger retaliation. The ally takes the rest after its own mitigation.",
        "prerequisite": null
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Ally mitigates first; redirect ≤S+M from remainder; self gets no second mitigation/retaliation.",
      "transferContract": {
        "phase": "defended",
        "formula": "scale-mod",
        "flags": [
          "noRetaliation",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "tinker.arch.emergency-protocols",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.emergency-protocols",
      "sourceSha256": "ac7d27cd219c8e7e7ee81ba88425c48850dbac9861ea85a06d715ab99ad905ff",
      "sourceProcedure": {
        "name": "Emergency Protocols",
        "activation": "Reaction",
        "cost": "1 encounter use",
        "rangeAndTarget": "Drone within 10 ft when attack hits you",
        "duration": "One hit",
        "frequency": "1/encounter",
        "effect": "Drone intercepts: reduce damage to you by S+M and takes same amount unmitigated. It must be active/conscious. Does not redirect again or trigger retaliation loops.",
        "prerequisite": null
      },
      "classification": "POST_DEFENSE_TRANSFER + COMPANION_DEVICE",
      "firstProposal": "**NEW phase:** after user's defenses, before tempHP; redirect min(S+M,remaining) to drone unmitigated.",
      "transferContract": {
        "phase": "defended",
        "formula": "scale-mod-fixed",
        "flags": [
          "noRetaliation",
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "warrior.hero.wardborn.guardian-tissue",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.wardborn.guardian-tissue",
      "sourceSha256": "6758edbc7d9cf5f27f4866127fc8ef9b9df2a71a2d6f056030ca253381fdc1d6",
      "sourceProcedure": {
        "name": "Guardian Tissue",
        "activation": "Reaction",
        "cost": "0",
        "rangeAndTarget": "One adjacent ally and self",
        "duration": "Instantaneous",
        "frequency": "Once per round",
        "effect": "Guardian Tissue. When an adjacent ally would take damage, reduce that ally's incoming damage by one-third rounded down. You take the prevented amount as damage of the same type. This transferred damage cannot be redirected again and cannot trigger another Guardian Tissue. Transferred damage cannot be reduced again, redirected again or generate BT.",
        "prerequisite": null
      },
      "classification": "POST_DEFENSE_TRANSFER",
      "firstProposal": "Redirect floor(postDefenseDamage/3); no second mitigation/BT/retransfer.",
      "transferContract": {
        "phase": "defended",
        "formula": "third",
        "flags": [
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [
          "BT"
        ],
        "automatic": false,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "warrior.hero.wardborn.aegis-incarnate",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.wardborn.aegis-incarnate",
      "sourceSha256": "5e223de7f6a979dac5c81bb5b26b2c3796c41100d9cbe813da435aa9cac54c6b",
      "sourceProcedure": {
        "name": "Aegis Incarnate",
        "activation": "Bonus Action",
        "cost": "0",
        "rangeAndTarget": "Self and allies within 15 feet",
        "duration": "3 rounds",
        "frequency": "1/long rest; automatic Wardborn Final Form",
        "effect": "Final Form – Aegis Incarnate. For 3 rounds you cannot be forcibly moved or knocked Prone. Whenever an ally within 15 feet takes damage, automatically redirect half that damage rounded down to yourself after the ally's resistance but before its temporary HP; the ally takes the remainder. Redirected damage keeps its type, cannot be reduced again or generate BT, and cannot be redirected again. If taking the redirected damage would kill you outright, the redirection still occurs. This grants no extra Reaction requirement and does not stack with Guardian Tissue on the same damage event.",
        "prerequisite": null
      },
      "classification": "AUTOMATIC_POST_DEFENSE_TRANSFER",
      "firstProposal": "Automatic half after original defenses/resistance, before tempHP; no second mitigation/BT/retransfer. Survival effects still legal.",
      "transferContract": {
        "phase": "defended",
        "formula": "half",
        "flags": [
          "noRetransfer",
          "noSecondMitigation"
        ],
        "blockedResources": [
          "BT"
        ],
        "automatic": true,
        "maximumTransferredRecipients": 1
      },
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    },
    {
      "bindingId": "warrior.hero.wardborn.guardian-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.wardborn.guardian-pulse",
      "sourceSha256": "b0bb1ba7e3a0716a83932ecee97cafdc14a082891419ebdcf3299b674e6a4da9",
      "sourceProcedure": {
        "name": "Guardian Pulse",
        "activation": "Reaction",
        "cost": "0",
        "rangeAndTarget": "One adjacent ally and triggering attacker",
        "duration": "Instantaneous",
        "frequency": "1/short rest",
        "effect": "Guardian Pulse. Trigger when an adjacent ally is targeted by an attack. You become the target instead; resolve the original attack roll against your AC and defenses. After that attack fully resolves, if the attacker is within your melee reach, make one melee weapon attack against it. This counterattack is a free attack, cannot grant another free attack or Action, and occurs whether the redirected attack hit or missed.",
        "prerequisite": null
      },
      "classification": "ATTACK_RETARGET + COUNTERATTACK",
      "firstProposal": "Retarget attack before AC resolution; Guardian becomes actual attack target. One original attack roll only. Counterattack afterward is a separate attack root whether original attack hit or missed.",
      "transferContract": null,
      "status": "SOURCE-AUDITED / IN_REVIEW; bounded damage-sharing interface",
      "operationalOverrides": [
        "Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays."
      ],
      "reviewEvidence": [
        "GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md",
        "GPT_REDIRECTION_BOUNDARIES.md"
      ],
      "openIssues": [
        "Exact helper/guide review pending. Wider source lifecycle, command budgets and all-source defense/copy scheduling are outside this bounded interface."
      ]
    }
  ]
}

## Exact tools/redirection_playtest_rules.py

"""Bounded39-source damage sharing, proposed for exact notebook review.

Callers establish ownership, actions/costs, target legality, range, willingness,
active effects, printed cadence and damage type. One root is ONE original
recipient packet, not an entire multi-target cast. Each area recipient gets a
separate root under its shared cast/roll identity. No full combat scheduler.
"""
from dataclasses import dataclass,field,replace
from core_playtest_rules import attack_roll
from spell_playtest_rules import integer,SpellRuleError
from healing_playtest_rules import survival_damage_event
from control_playtest_rules import clock_marker,require_deadline

P='paladin.supplement.'
CROWN=P+'oath-of-the-martyr-king.crown-undying'
FINAL=P+'oath-of-the-chain.final-stand'
BURDEN=P+'oath-of-the-martyr-king.burden-shared'
PALADIN_BASE=frozenset({'noSecondMitigation','noRetransfer','noReflection','noResourceGeneration'})
POST=frozenset({'noSecondMitigation','noRetransfer'})

@dataclass(frozen=True)
class TransferProfile:
    phase: str
    formula: str
    flags: frozenset
    blocked_resources: frozenset=frozenset()
    automatic: bool=False
    max_recipients: int=1

PROFILES={
 'crimson-agent.hero.bloodweaver.bloodbond':TransferProfile('raw','quarter',frozenset({'noRetransfer'})),
 'crimson-agent.hero.bloodweaver.veinlock-tether':TransferProfile('raw','scale-mod',frozenset({'noRetransfer'})),
 'monk.hero.enlightened-master.shared-breath':TransferProfile('defended','scale-mod',POST),
 'oracle.supplement.life.life-linked':TransferProfile('defended','half-chosen',POST|frozenset({
     'noReflection','noResourceGeneration','noPassiveTriggers','noConditionTriggers',
     'noActionGeneration','noCopyGeneration','noRecoveryGeneration','noRetaliation'})),
 'paladin.base.protective-stance':TransferProfile('defended','scale-mod-fixed',PALADIN_BASE|{'noDamageTriggers'}),
 P+'oath-of-the-chain.chainbound-smite':TransferProfile('defended','cha-min3',PALADIN_BASE),
 P+'oath-of-the-chain.linked-ward':TransferProfile('defended','twice-cha-min2',PALADIN_BASE),
 P+'oath-of-the-chain.martyr-s-share':TransferProfile('defended','half',PALADIN_BASE),
 FINAL:TransferProfile('defended','all',PALADIN_BASE,automatic=True),
 P+'oath-of-the-martyr-king.king-s-smite':TransferProfile('defended','five',PALADIN_BASE),
 P+'oath-of-the-martyr-king.aura-of-the-crown':TransferProfile('defended','mod',PALADIN_BASE),
 P+'oath-of-the-martyr-king.crown-of-embers':TransferProfile('defended','level-mod',PALADIN_BASE),
 BURDEN:TransferProfile('defended','level-mod',PALADIN_BASE|{'noHealingGeneration'},max_recipients=2),
 CROWN:TransferProfile('defended','level-mod',PALADIN_BASE),
 'soldier.hero.champion.selfless-guardian':TransferProfile('defended','scale-mod',POST|{'noRetaliation'}),
 'tinker.arch.emergency-protocols':TransferProfile('defended','scale-mod-fixed',POST|{'noRetaliation'}),
 'warrior.hero.wardborn.guardian-tissue':TransferProfile('defended','third',POST,frozenset({'BT'})),
 'warrior.hero.wardborn.aegis-incarnate':TransferProfile('defended','half',POST,frozenset({'BT'}),automatic=True),
}

def identity(value):
    if not isinstance(value,str) or not value:raise SpellRuleError('Nonempty identity required')
    return value

def transfer_limit(source,available,*,scale=1,modifier=1,level=1,charisma=0):
    """Maximum; fixed fractions/all/fixed reductions require exactly this amount."""
    if source not in PROFILES:raise SpellRuleError('Source is not a supplied damage transfer')
    integer(available,'available damage',0);integer(scale,'S',1,4)
    integer(modifier,'M',1);integer(level,'level',1,20);integer(charisma,'actual CHA modifier',-10,20)
    f=PROFILES[source].formula
    caps={'quarter':available//4,'third':available//3,'half':available//2,
          'half-chosen':available//2,'all':available,'scale-mod':scale+modifier,
          'scale-mod-fixed':scale+modifier,'level-mod':level+modifier,
          'cha-min3':max(3,charisma),'twice-cha-min2':max(2,2*charisma),'five':5,'mod':modifier}
    return min(available,caps[f])

@dataclass(frozen=True)
class Branch:
    branch_id: str
    target: str
    amount: int
    stage: str='raw'
    transferred: bool=False
    attack_hit: bool=False
    critical: bool=False
    failed_save: bool=False
    melee_attack: bool=False
    flags: frozenset=frozenset()
    blocked_resources: frozenset=frozenset()
    prevention_ids: frozenset=frozenset()

@dataclass
class PaladinRoundLedger:
    owner: str
    round_number: int
    events: dict=field(default_factory=dict)
    crown_heal_used: dict=field(default_factory=dict)
    settled_heals: set=field(default_factory=set)

    def __post_init__(self):
        identity(self.owner);integer(self.round_number,'numbered round',1)

    def validate(self,root_id,source,amount,*,crown_active,level,modifier):
        identity(root_id);integer(amount,'positive transferred amount',1)
        integer(level,'Paladin level',1,20);integer(modifier,'M',1)
        if root_id in self.events:raise SpellRuleError('This owner already redirected that damage root')
        if len(self.events)>= (2 if crown_active else 1):
            raise SpellRuleError('Shared Paladin round allowance exhausted')
        if source==CROWN:
            if not crown_active:raise SpellRuleError('Crown is not active')
            spent=sum(x['amount'] for x in self.events.values() if x['source']==CROWN)
            if spent+amount>level+modifier:raise SpellRuleError('Crown round transferred amount exhausted')
        elif any(x['source']!=CROWN for x in self.events.values()):
            raise SpellRuleError('Only one ordinary Paladin redirection per round')

    def record(self,root_id,source,amount,ally,**options):
        self.validate(root_id,source,amount,**options)
        self.events[root_id]={'source':source,'amount':amount,'ally':identity(ally)}

    def crown_heal(self,root_id,actual_damage,*,scale,modifier):
        """Commit nominal source entitlement BEFORE target healing restrictions.

        Blocked healing spends the nominal cap. A duplicate settlement is an
        error, not another heal. Caller applies ordinary pipeline and explicit
        no-copy/no-redirection-chain flags to this source-native result.
        """
        integer(actual_damage,'final Paladin branch actual damage',0)
        integer(scale,'S',1,4);integer(modifier,'M',1)
        entry=self.events.get(root_id)
        if not entry or entry['source']!=CROWN:raise SpellRuleError('Not a Crown event')
        if root_id in self.settled_heals:raise SpellRuleError('Crown event already settled')
        if actual_damage>entry['amount']:raise SpellRuleError('Numeric damage exceeds transferred amount')
        ally=entry['ally'];used=self.crown_heal_used.get(ally,0)
        amount=min(actual_damage//2,max(0,scale+modifier-used))
        self.crown_heal_used[ally]=used+amount;self.settled_heals.add(root_id)
        return amount

class DamageRoot:
    def __init__(self,root_id,target,amount,damage_type,*,attack_hit=False,critical=False,
                 failed_save=False,melee_attack=False,inherited_flags=frozenset(),blocked_resources=frozenset()):
        self.root_id=identity(root_id);identity(target);identity(damage_type)
        integer(amount,'finalized attack/save/critical raw damage',0)
        if critical and not attack_hit:raise SpellRuleError('Critical requires an actual attack hit')
        if melee_attack and not attack_hit:raise SpellRuleError('Melee damage requires an actual hit')
        self.damage_type=damage_type;self.rolled_packet=amount
        self.original_id=root_id+'/original'
        self.branches={self.original_id:Branch(self.original_id,target,amount,
            attack_hit=attack_hit,critical=critical,failed_save=failed_save,melee_attack=melee_attack,
            flags=frozenset(inherited_flags),blocked_resources=frozenset(blocked_resources))}
        self.operation=None;self.resolved={}

    def branch(self,branch_id):
        if branch_id not in self.branches:raise SpellRuleError('Unknown branch')
        return self.branches[branch_id]

    def pending(self,branch_id):
        b=self.branch(branch_id)
        if branch_id in self.resolved:raise SpellRuleError('Branch already resolved')
        return b

    def defend(self,branch_id,*,flat_reductions=(),resistant=False,immune=False):
        b=self.pending(branch_id)
        if b.stage!='raw':raise SpellRuleError('Ordinary defenses apply once to a raw branch')
        for v in flat_reductions:integer(v,'flat class reduction',0)
        value=max(0,b.amount-max(flat_reductions,default=0))
        value=0 if immune else value//2 if resistant else value
        self.branches[branch_id]=replace(b,amount=value,stage='defended')
        return value

    def prevent(self,branch_id,amount,application_id):
        b=self.pending(branch_id);integer(amount,'eligible prevention amount',0);identity(application_id)
        if b.stage!='defended' or 'noSecondMitigation' in b.flags:
            raise SpellRuleError('Prevention requires a legally reducible defended branch')
        if application_id in b.prevention_ids:raise SpellRuleError('One prevention application per branch')
        stopped=min(amount,b.amount)
        self.branches[branch_id]=replace(b,amount=b.amount-stopped,
            prevention_ids=b.prevention_ids|{application_id})
        return stopped

    def transfer(self,source,owner,allocations,*,scale=1,modifier=1,level=1,charisma=0,
                 paladin_ledger=None,crown_active=False):
        """One selected legal operation. Entire validation precedes mutation.

        allocations maps DISTINCT willing legal recipients to positive amounts.
        Caller selects mandatory offers before optional offers at their stage.
        Zero automatic shares simply produce no operation; optional0 is illegal.
        """
        identity(owner)
        if source not in PROFILES:raise SpellRuleError('Not a supplied damage-transfer source')
        p=PROFILES[source];b=self.pending(self.original_id)
        if self.operation:raise SpellRuleError('One transfer operation per original-recipient root')
        if b.stage!=p.phase:raise SpellRuleError('Transfer at wrong defense stage')
        cap=transfer_limit(source,b.amount,scale=scale,modifier=modifier,level=level,charisma=charisma)
        if not allocations:
            if p.automatic and cap==0:return None
            raise SpellRuleError('Optional transfer requires a positive amount')
        if len(allocations)>p.max_recipients:raise SpellRuleError('Too many transferred recipients')
        for target,amount in allocations.items():
            identity(target);integer(amount,'recipient transfer',1)
            if target==b.target:raise SpellRuleError('Cannot transfer to original damage target')
        total=sum(allocations.values())
        if total>cap:raise SpellRuleError('Transfer exceeds available/source amount')
        if p.formula in ('quarter','third','half','all','scale-mod-fixed') and total!=cap:
            raise SpellRuleError('Printed fixed amount cannot be arbitrarily lowered')
        is_paladin=source.startswith('paladin.')
        if is_paladin:
            if paladin_ledger is None or paladin_ledger.owner!=owner:
                raise SpellRuleError('Use the source owner Paladin round ledger')
            paladin_ledger.validate(self.root_id,source,total,crown_active=crown_active,level=level,modifier=modifier)
        stage='raw' if p.phase=='raw' else 'sealed'
        children={self.root_id+'/transfer/'+str(i):Branch(self.root_id+'/transfer/'+str(i),
            target,amount,stage=stage,transferred=True,flags=b.flags|p.flags,
            blocked_resources=b.blocked_resources|p.blocked_resources)
            for i,(target,amount) in enumerate(allocations.items(),1)}
        # No operation below this point can fail validation.
        if is_paladin:
            paladin_ledger.record(self.root_id,source,total,b.target,crown_active=crown_active,level=level,modifier=modifier)
        self.branches[self.original_id]=replace(b,amount=b.amount-total,stage=stage)
        self.branches.update(children)
        self.operation={'source':source,'owner':owner,'amount':total,'recipientBranchIds':tuple(children)}
        return self.operation

    def resolve_living(self,branch_id,state,**life_options):
        b=self.pending(branch_id)
        if b.stage not in ('defended','sealed'):raise SpellRuleError('Resolve defenses before life state')
        if 'critical' in life_options:raise SpellRuleError('Critical identity is owned by damage branch')
        if b.transferred and any(life_options.get(k) for k in ('maiming','knockout','melee')):
            raise SpellRuleError('Original attack riders do not accompany transferred damage')
        after,event=survival_damage_event(state,b.amount,critical=b.critical,**life_options)
        event={**event,'rootDamageEventId':self.root_id,'branchId':branch_id,'targetId':b.target,
               'damageType':self.damage_type,'attackHit':b.attack_hit,'criticalHit':b.critical,
               'failedOriginalSave':b.failed_save,'transferred':b.transferred,
               'concentrationDamage':b.amount,'flags':sorted(b.flags)}
        self.resolved[branch_id]=event
        return after,event

    def resolve_device(self,branch_id,state):
        b=self.pending(branch_id)
        if b.stage not in ('defended','sealed'):raise SpellRuleError('Resolve defenses before device state')
        after,event=device_damage(state,b.amount)
        event={**event,'rootDamageEventId':self.root_id,'branchId':branch_id,'targetId':b.target,
               'damageType':self.damage_type,'attackHit':b.attack_hit,'criticalHit':b.critical,
               'failedOriginalSave':b.failed_save,'transferred':b.transferred,'flags':sorted(b.flags)}
        self.resolved[branch_id]=event
        return after,event

    def total(self,consumer='physical',*,resource=None,qualified_targets=None):
        """Caller still verifies initiating-source and target-specific predicates."""
        if set(self.resolved)!=set(self.branches):raise SpellRuleError('All terminal branches must resolve first')
        return sum(event['actualDamageDealt'] for bid,event in self.resolved.items()
                   if (qualified_targets is None or self.branches[bid].target in qualified_targets)
                   and permits_consumer(self.branches[bid],consumer,resource=resource))

def permits_consumer(branch,consumer,*,resource=None):
    flags=branch.flags
    if consumer=='physical':return True
    kinds={'damage','healing','recovery','resource','retaliation','reflection','passive','condition','action','copy','attack-hit','free-attack'}
    if consumer not in kinds:raise SpellRuleError('Unknown damage consumer')
    if 'noDamageTriggers' in flags:return False
    if consumer=='attack-hit':return branch.attack_hit
    if consumer=='resource':
        identity(resource)
        if 'noResourceGeneration' in flags or resource in branch.blocked_resources:return False
    mapping={'healing':{'noHealingGeneration','noRecoveryGeneration'},
             'recovery':{'noRecoveryGeneration'},'reflection':{'noReflection','noRetaliation'},
             'retaliation':{'noRetaliation'},'passive':{'noPassiveTriggers'},
             'condition':{'noConditionTriggers'},'action':{'noActionGeneration'},
             'copy':{'noCopyGeneration'},'free-attack':{'noFreeAttackGeneration'}}
    return not (flags & mapping.get(consumer,set()))

@dataclass(frozen=True)
class DeviceState:
    maximum_hp: int
    hp: int
    temp_hp: int=0
    destroyed: bool=False
    disabled: bool=False
    def __post_init__(self):
        integer(self.maximum_hp,'device maximum HP',1);integer(self.hp,'device HP',0,self.maximum_hp)
        integer(self.temp_hp,'legally granted device tempHP',0)
        if self.destroyed!=(self.hp==0):raise SpellRuleError('A0HP device is destroyed')

def device_damage(state,amount):
    """Tinker device damage only; no organic Wounds/death saves or repair rights."""
    integer(amount,'device resolved damage',0)
    if state.destroyed:raise SpellRuleError('Already destroyed device is not a functional damage recipient')
    absorbed=min(state.temp_hp,amount);loss=min(state.hp,amount-absorbed);hp=state.hp-loss
    return replace(state,hp=hp,temp_hp=state.temp_hp-absorbed,destroyed=hp==0),{
        'resolvedDamage':amount,'positiveDamageEvent':amount>0,'tempAbsorbed':absorbed,
        'actualHpDamage':loss,'actualDamageDealt':absorbed+loss,'destroyedNow':hp==0,
        'woundSaves':0,'deathFailuresAdded':0}

@dataclass
class BloomPool:
    application_id: str
    target: str
    remaining: int
    expires: object
    ended: bool=False
    rider_deadline: object=None
    def __post_init__(self):
        identity(self.application_id);identity(self.target);integer(self.remaining,'Bloom capacity',1)
        require_deadline(self.expires)

    def end(self,now,*,target_next_end):
        now=clock_marker(now);require_deadline(target_next_end)
        if target_next_end<=now:raise SpellRuleError('Ending rider needs a future target-next-end')
        if self.ended:return False
        self.ended=True;self.rider_deadline=target_next_end
        return True

    def absorb(self,root,branch_id,now,*,target_next_end,suppressed=False):
        b=root.pending(branch_id);now=clock_marker(now);require_deadline(target_next_end)
        if b.target!=self.target:raise SpellRuleError('Bloom belongs to a different recipient')
        if self.ended:return 0
        if now>=self.expires:
            # Caller supplies the target end AFTER actual expiry, not late polling.
            self.end(self.expires,target_next_end=target_next_end);return 0
        if target_next_end<=now:raise SpellRuleError('Ending rider needs a future target-next-end')
        if suppressed:return 0
        # prevent validates before either root/pool mutates.
        prevented=root.prevent(branch_id,self.remaining,self.application_id)
        self.remaining-=prevented
        if self.remaining==0:self.end(now,target_next_end=target_next_end)
        return prevented

@dataclass
class AttackRetarget:
    attack_id: str
    intended_target: str
    current_target: str=None
    retargeted: bool=False
    resolved: bool=False
    counter_used: bool=False
    def __post_init__(self):
        identity(self.attack_id);identity(self.intended_target)
        self.current_target=self.intended_target
    def retarget(self,guardian):
        identity(guardian)
        if self.resolved or self.retargeted:raise SpellRuleError('Attack can retarget only once before hit resolution')
        if guardian==self.current_target:raise SpellRuleError('Retarget requires a different creature')
        self.current_target=guardian;self.retargeted=True
    def resolve(self,natural,modifier,armor_class,critical_threshold=20):
        if self.resolved:raise SpellRuleError('Original attack roll resolves once')
        result=attack_roll(natural,modifier,armor_class,critical_threshold)
        self.resolved=True
        return {**result,'targetId':self.current_target,'attackId':self.attack_id}

    def guardian_counter(self,*,triggering_attack_fully_resolved,in_reach,actor_can_attack,
                         parent_flags=frozenset()):
        """Single free counter after full damage/rider resolution, on hit OR miss.

        False eligibility consumes this response opportunity, not a new attack.
        Caller attaches returned flags to the NEW counterattack and its damage.
        """
        if not self.retargeted or not self.resolved or not triggering_attack_fully_resolved:
            raise SpellRuleError('Guardian counter waits for its retargeted attack to finish')
        if self.counter_used:raise SpellRuleError('Guardian counter opportunity already settled')
        self.counter_used=True
        if not in_reach or not actor_can_attack or 'noFreeAttackGeneration' in parent_flags:return None
        return frozenset(parent_flags)|{'noFreeAttackGeneration','noActionGeneration'}

def redirecting_palm(root,branch_id,monk_level,attacker_id,*,second_enemy_id=None,new_root_id=None):
    """Caller owns Reaction/Ki/range. Distinct second enemy required for counter."""
    b=root.pending(branch_id);integer(monk_level,'Monk level',1,20);identity(attacker_id)
    if not b.attack_hit or not b.melee_attack or b.amount<=0:raise SpellRuleError('Palm requires positive melee-hit damage')
    if second_enemy_id is not None:
        identity(second_enemy_id);identity(new_root_id)
        if second_enemy_id in (b.target,attacker_id):raise SpellRuleError('Palm needs a distinct second enemy')
        if new_root_id==root.root_id:raise SpellRuleError('Counter is a NEW root')
    prevented=root.prevent(branch_id,b.amount//2,'monk.arch.tortoise.redirecting-palm')
    if not prevented or second_enemy_id is None:return None
    return DamageRoot(new_root_id,second_enemy_id,min(prevented,monk_level),'force',
                      inherited_flags=frozenset({'noActionGeneration','noFreeAttackGeneration','noCopyGeneration'}))

def native_transfer_temp_hp(root,branch_id,*,source,scale,modifier,level,reduced_to_zero=False):
    """Caller establishes actual rider ownership, bond and zero-crossing predicate."""
    integer(scale,'S',1,4);integer(modifier,'M',1);integer(level,'level',1,20)
    if not root.operation or branch_id not in root.operation['recipientBranchIds'] or branch_id not in root.resolved:
        raise SpellRuleError('Rider requires a completed transferred branch')
    value=root.resolved[branch_id]['actualDamageDealt']
    if source==P+'oath-of-the-chain.unbroken-covenant':return min(value//2,scale+modifier)
    if source==P+'oath-of-the-chain.linked-ward':
        if root.operation['source']!=source:raise SpellRuleError('Linked Ward rider belongs to its own transfer')
        return min(value,level+modifier) if reduced_to_zero else 0
    if source==FINAL:
        if root.operation['source']!=source:raise SpellRuleError('Final Stand rider belongs to its own transfer')
        return level if reduced_to_zero else 0
    raise SpellRuleError('No supplied native transfer tempHP rider')


## Exact tools/validate_redirection_playtests.py

from pathlib import Path
import json
from copy import deepcopy
from redirection_playtest_rules import *
from core_playtest_rules import LifeState
from healing_playtest_rules import healing_packet
from control_playtest_rules import absolute_deadline,turn_end_deadline
ROOT=Path(__file__).resolve().parents[1]
BB='crimson-agent.hero.bloodweaver.bloodbond'
VT='crimson-agent.hero.bloodweaver.veinlock-tether'
BREATH='monk.hero.enlightened-master.shared-breath'
TISSUE='warrior.hero.wardborn.guardian-tissue'
AEGIS='warrior.hero.wardborn.aegis-incarnate'
STANCE='paladin.base.protective-stance'
EMERGENCY='tinker.arch.emergency-protocols'

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected);checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    def raw(name,amount=20,**kw):return DamageRoot(name,'ally',amount,'fire',**kw)
    def defended(name,amount=20,**kw):
        r=raw(name,amount,**kw);r.defend(r.original_id);return r
    def living_all(r,states=None,**kw):
        states=states or {}
        for bid,b in r.branches.items():
            if b.stage=='raw':r.defend(bid)
            r.resolve_living(bid,states.get(b.target,LifeState(100,100)),**kw)
    r=raw('pre',40,attack_hit=True,critical=True)
    r.transfer(BB,'agent',{'agent':10})
    ids=list(r.branches);r.defend(ids[0],resistant=True);r.defend(ids[1],resistant=True)
    check('Quarter sharing precedes both recipients resistance',[b.amount for b in r.branches.values()],[15,5])
    check('Transferred portion loses attack-critical identity',(r.branch(ids[1]).attack_hit,r.branch(ids[1]).critical),(False,False))
    check('Original portion preserves hit and critical identity',(r.branch(ids[0]).attack_hit,r.branch(ids[0]).critical),(True,True))
    rejects('Pretransfer locks retained original against later transfer',lambda:r.transfer(BREATH,'monk',{'monk':1}))
    rejects('Quarter reaction cannot arbitrarily choose smaller share',lambda:raw('bad-quarter',40).transfer(BB,'agent',{'agent':5}))
    a=raw('pre-dr',40);a.transfer(BB,'agent',{'agent':10})
    a.defend(a.original_id,flat_reductions=(12,5),resistant=True)
    check('Strongest original flat reduction applies to retained share only',a.branch(a.original_id).amount,9)
    a.defend('pre-dr/transfer/1',flat_reductions=(2,),resistant=True)
    a.prevent('pre-dr/transfer/1',3,'guardian')
    check('Premitigation transfer accepts recipient defenses and pure prevention',a.branch('pre-dr/transfer/1').amount,1)
    r=raw('post',30);r.defend(r.original_id,flat_reductions=(5,3),resistant=True)
    check('Flat strongest then resistance floor',r.branch(r.original_id).amount,12)
    r.transfer(BREATH,'monk',{'monk':5},scale=2,modifier=3)
    check('Postdefense split conserves remaining amount',[b.amount for b in r.branches.values()],[7,5])
    child='post/transfer/1'
    rejects('Postdefense child cannot defend again',lambda:r.defend(child,immune=True))
    rejects('Postdefense child cannot use further pure prevention',lambda:r.prevent(child,5,'bloom'))
    rejects('Postsplit original cannot use late pure prevention',lambda:r.prevent(r.original_id,1,'late'))
    after,event=r.resolve_living(child,LifeState(20,20,temp_hp=5))
    check('Unmitigated transfer still consumes temporary HP',(after.hp,after.temp_hp,event['actualDamageDealt']),(20,0,5))
    check('TemporaryHP absorption does not erase concentration packet',event['concentrationDamage'],5)
    rejects('Root totals await every terminal branch',lambda:r.total())
    r.resolve_living(r.original_id,LifeState(20,20))
    check('Physical total counts final recipients only',r.total(),12)
    rejects('Final branch cannot resolve twice',lambda:r.resolve_living(child,after))
    r=defended('critical',6,attack_hit=True,critical=True)
    r.transfer(BREATH,'monk',{'monk':6},scale=3,modifier=3)
    after,event=r.resolve_living('critical/transfer/1',LifeState(20,0))
    check('Transferred critical damage causes one death failure',(after.death_failures,event['criticalHit']),(1,False))
    after,event=r.resolve_living(r.original_id,LifeState(20,20))
    check('Full transfer retains original hit without positive damage',(event['attackHit'],event['positiveDamageEvent']),(True,False))
    r=defended('aegis',50)
    r.transfer(AEGIS,'warrior',{'warrior':25})
    after,event=r.resolve_living('aegis/transfer/1',LifeState(10,2),ritual_ward=True)
    check('Aegis still transfers lethal packet but Ward can prevent death',(after.dead,after.hp,event['instantDeath'],event['wardUsed']),(False,1,True,True))
    check('Survival replacement does not overcount actualHP damage',event['actualDamageDealt'],1)
    r=defended('wounds',12);r.transfer(BREATH,'monk',{'monk':7},scale=3,modifier=4)
    after,event=r.resolve_living('wounds/transfer/1',LifeState(20,5),wound_natural=20)
    check('Ordinary transfer dropping positiveHP to0 invokes Wound save',(after.hp,event['woundSaves']),(0,1))
    rejects('A transferred branch cannot acquire original maiming rider',
            lambda:r.resolve_living(r.original_id,LifeState(20,20),critical=True))
    r=defended('no-riders',10);r.transfer(BREATH,'monk',{'monk':3},modifier=2)
    rejects('Transferred branch rejects attack maiming rider',lambda:r.resolve_living('no-riders/transfer/1',LifeState(20,20),maiming=True))
    ledger=PaladinRoundLedger('paladin',1)
    r=defended('stance-small',3,attack_hit=True)
    r.transfer(STANCE,'paladin',{'paladin':3},scale=4,modifier=4,paladin_ledger=ledger)
    check('Protective Stance cannot create nonexistent excess damage',r.operation['amount'],3)
    check('Shared Paladin ledger records one operation',len(ledger.events),1)
    r2=defended('second',5);snapshot=deepcopy(r2.branches)
    rejects('Second ordinary Paladin event rejected',lambda:r2.transfer(STANCE,'paladin',{'paladin':2},paladin_ledger=ledger))
    check('Failed shared allowance leaves root unchanged',r2.branches,snapshot)
    check('Failed shared allowance does not add ledger event',len(ledger.events),1)
    r3=defended('other-owner',5)
    r3.transfer(STANCE,'other-paladin',{'other-paladin':2},paladin_ledger=PaladinRoundLedger('other-paladin',1))
    check('Different Paladin keeps independent round allowance',r3.operation['owner'],'other-paladin')
    rejects('Different owner cannot transfer already split root',lambda:r3.transfer(BREATH,'monk',{'monk':1}))
    r=defended('zero-auto',1)
    check('Automatic rounded0 share creates no operation',r.transfer(AEGIS,'warrior',{}),None)
    check('Automatic0 leaves root unclaimed',r.operation,None)
    rejects('Optional0 transfer cannot activate',lambda:defended('zero-opt',5).transfer(BREATH,'monk',{}))
    r=defended('multi',12);ledger=PaladinRoundLedger('paladin',2)
    r.transfer(BURDEN,'paladin',{'friend-A':3,'friend-B':5},level=10,modifier=2,paladin_ledger=ledger)
    check('Burden is one multi-recipient operation',[b.amount for b in r.branches.values()],[4,3,5])
    living_all(r)
    check('Burden physical total includes all branches',r.total(),12)
    check('Burden healing consumer excludes prohibited branches',r.total('healing'),4)
    check('Burden resource consumer excludes prohibited branches',r.total('resource',resource='RP'),4)
    check('Source target predicate still filters final recipients',r.total(qualified_targets={'ally'}),4)
    r=defended('flags',9);r.transfer(TISSUE,'warrior',{'warrior':3})
    living_all(r)
    check('Warrior transfer bans BT only',r.total('resource',resource='BT'),6)
    check('Warrior transfer does not invent universal resource ban',r.total('resource',resource='Ki'),9)
    r=defended('pal-flags',8);ledger=PaladinRoundLedger('paladin',3)
    r.transfer(P+'oath-of-the-martyr-king.king-s-smite','paladin',{'paladin':5},paladin_ledger=ledger)
    living_all(r)
    check('Paladin reflection ban does not suppress all retaliation',(r.total('reflection'),r.total('retaliation')),(3,8))
    check('Paladin generic engine does not forbid healing generation',r.total('healing'),8)
    r=defended('native',8);ledger=PaladinRoundLedger('paladin',4)
    r.transfer(STANCE,'paladin',{'paladin':6},scale=2,modifier=4,paladin_ledger=ledger)
    living_all(r)
    check('Protective Stance suppresses generic damage-generated healing',r.total('healing'),2)
    check('Unbroken Covenant triggers on redirection despite noDamageTriggers',
          native_transfer_temp_hp(r,'native/transfer/1',source=P+'oath-of-the-chain.unbroken-covenant',scale=2,modifier=4,level=10),3)
    check('Unrelated later healing of recipient remains legal',healing_packet(LifeState(20,10),5)['actualHpGained'],5)
    ledger=PaladinRoundLedger('paladin',5)
    opts=dict(crown_active=True,level=10,modifier=2)
    ledger.record('c1',CROWN,6,'same-ally',**opts)
    ledger.record('c2',CROWN,6,'same-ally',**opts)
    check('Crown permits two different events for same selected ally',len(ledger.events),2)
    check('Crown healing floors per event then uses cumulative cap',
          (ledger.crown_heal('c1',5,scale=2,modifier=2),ledger.crown_heal('c2',6,scale=2,modifier=2)),(2,2))
    rejects('Crown third event rejected',lambda:ledger.record('c3',CROWN,1,'ally',**opts))
    rejects('Crown heal cannot be settled twice',lambda:ledger.crown_heal('c1',5,scale=2,modifier=2))
    ledger=PaladinRoundLedger('paladin',6)
    ledger.record('earlier',STANCE,2,'ally',crown_active=False,level=10,modifier=2)
    ledger.record('later',CROWN,8,'ally',**opts)
    check('Midround Crown activation preserves previous ordinary use',len(ledger.events),2)
    rejects('Crown activation cannot reset shared event history',lambda:ledger.record('extra',CROWN,1,'ally',**opts))
    ledger=PaladinRoundLedger('paladin',7)
    ledger.record('c-first',CROWN,2,'ally',**opts)
    ledger.record('o-second',STANCE,2,'ally',**opts)
    check('One Crown plus one ordinary allowed with Crown active in either order',len(ledger.events),2)
    ledger=PaladinRoundLedger('paladin',8)
    ledger.record('amount',CROWN,11,'ally',**opts)
    rejects('Crown amount cap independent of remaining event slot',lambda:ledger.record('too-much',CROWN,2,'ally',**opts))
    check('Failed amount cap leaves one event',len(ledger.events),1)
    ledger=PaladinRoundLedger('paladin',9)
    ledger.record('blocked',CROWN,8,'ally',**opts)
    nominal=ledger.crown_heal('blocked',8,scale=2,modifier=2)
    check('Blocked Crown heal yields0actual',healing_packet(LifeState(20,1),nominal,hp_gain_prohibited=True)['actualHpGained'],0)
    check('Blocked Crown healing consumes nominal cap',ledger.crown_heal_used['ally'],4)
    ledger=PaladinRoundLedger('paladin',10)
    r=defended('final-first',5);r.transfer(FINAL,'paladin',{'paladin':5},paladin_ledger=ledger)
    rejects('Final Stand constrained to one shared event that round',lambda:defended('final-second',4).transfer(FINAL,'paladin',{'paladin':4},paladin_ledger=ledger))
    check('Final Stand is an automatic profile',PROFILES[FINAL].automatic,True)
    r=defended('bloom-first',6);pool=BloomPool('bloom','ally',15,absolute_deadline(60))
    pool.absorb(r,r.original_id,0,target_next_end=turn_end_deadline(6))
    check('Bloom pool persists across small packet',(pool.remaining,pool.ended),(9,False))
    r=defended('bloom-second',12);pool.absorb(r,r.original_id,1,target_next_end=turn_end_deadline(6))
    check('Bloom depletion leaves remainder and starts rider',(r.branch(r.original_id).amount,pool.remaining,pool.ended,pool.rider_deadline),(3,0,True,turn_end_deadline(6)))
    pool=BloomPool('suppressed','ally',5,absolute_deadline(60));r=defended('suppressed',5)
    check('Suppression neither consumes nor ends Bloom',pool.absorb(r,r.original_id,2,target_next_end=turn_end_deadline(6),suppressed=True),0)
    check('Suppressed Bloom retains full capacity',(pool.remaining,pool.ended),(5,False))
    pool.absorb(r,r.original_id,70,target_next_end=turn_end_deadline(66),suppressed=True)
    check('Late observation preserves expiry-based rider deadline',(pool.ended,pool.rider_deadline),(True,turn_end_deadline(66)))
    pool=BloomPool('skip','monk',8,absolute_deadline(60));r=defended('skip-bloom',10)
    r.transfer(BREATH,'monk',{'monk':4},modifier=3)
    rejects('Unmitigated transfer cannot spend recipient Bloom',lambda:pool.absorb(r,'skip-bloom/transfer/1',1,target_next_end=turn_end_deadline(6)))
    check('Rejected Bloom attempt preserves finite pool',pool.remaining,8)
    attack=AttackRetarget('attack','ally');attack.retarget('guardian')
    check('Guardian uses original roll against own AC',attack.resolve(12,4,19)['hit'],False)
    rejects('Attack cannot bounce to another Guardian',lambda:attack.retarget('second-guardian'))
    rejects('Original attack cannot reroll on retarget',lambda:attack.resolve(20,4,19))
    rejects('Counter must wait for full original attack resolution',lambda:attack.guardian_counter(triggering_attack_fully_resolved=False,in_reach=True,actor_can_attack=True))
    flags=attack.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True)
    check('Missed incoming attack still permits single legal counter','noFreeAttackGeneration' in flags,True)
    rejects('Counter opportunity cannot replay',lambda:attack.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True))
    attack2=AttackRetarget('counter-parent','ally');attack2.retarget('guardian');attack2.resolve(10,5,12)
    check('A free counter cannot manufacture another free counter',
          attack2.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True,parent_flags=flags),None)
    attack=AttackRetarget('retarget-then-transfer','ally');attack.retarget('guardian')
    result=attack.resolve(20,3,20)
    r=DamageRoot('after-retarget',result['targetId'],10,'slashing',attack_hit=result['hit'],critical=result['critical'])
    r.defend(r.original_id);r.transfer(BREATH,'monk',{'monk':4},modifier=3)
    check('Attack retarget leaves later transfer opportunity intact',r.operation['amount'],4)
    r=defended('palm',9,attack_hit=True,melee_attack=True)
    counter=redirecting_palm(r,r.original_id,3,'attacker',second_enemy_id='second',new_root_id='palm-counter')
    check('Palm prevents floorhalf and caps separate force packet',(r.branch(r.original_id).amount,counter.rolled_packet),(5,3))
    counter.defend(counter.original_id,resistant=True)
    check('Palm force counter accepts new recipient defenses',counter.branch(counter.original_id).amount,1)
    check('Palm counter is not an attack hit',counter.branch(counter.original_id).attack_hit,False)
    check('Palm counter cannot create free attack or copy',(permits_consumer(counter.branch(counter.original_id),'free-attack'),permits_consumer(counter.branch(counter.original_id),'copy')),(False,False))
    r=defended('palm-no-second',9,attack_hit=True,melee_attack=True)
    check('Palm reduction remains without a second enemy',redirecting_palm(r,r.original_id,3,'attacker'),None)
    check('Palm still reduced original damage',r.branch(r.original_id).amount,5)
    r=defended('palm-bad',9,attack_hit=True,melee_attack=True)
    rejects('Palm cannot send force back to original attacker',lambda:redirecting_palm(r,r.original_id,3,'attacker',second_enemy_id='attacker',new_root_id='bad-counter'))
    check('Invalid counter target does not consume prevention',r.branch(r.original_id).amount,9)
    rejects('Ranged attack cannot activate Palm',lambda:redirecting_palm(defended('palm-ranged',9,attack_hit=True),'palm-ranged/original',3,'attacker'))
    r=defended('drone',10,attack_hit=True);r.transfer(EMERGENCY,'tinker',{'drone':6},scale=2,modifier=4)
    after,event=r.resolve_device('drone/transfer/1',DeviceState(10,3,temp_hp=1))
    check('Emergency drone destruction uses device consequences',(after.hp,after.destroyed,event['actualDamageDealt'],event['woundSaves'],event['deathFailuresAdded']),(0,True,4,0,0))
    check('Device transfer does not manufacture an enemy attack hit',event['attackHit'],False)
    check('Emergency drone transfer suppresses retaliation consumer',permits_consumer(r.branch('drone/transfer/1'),'retaliation'),False)
    rejects('Destroyed drone cannot receive another functional packet',lambda:device_damage(after,1))
    rejects('False positiveHP destroyed device rejected',lambda:DeviceState(10,1,destroyed=True))
    # Independent conservation/oracle formula coverage, including floor boundaries.
    states=0
    for amount in range(0,65):
      for source,denom in ((BB,4),(TISSUE,3),(AEGIS,2)):
       chosen=amount//denom
       check_amount=transfer_limit(source,amount)
       assert check_amount==chosen
       if not chosen:continue
       r=raw('matrix',amount) if source==BB else defended('matrix',amount)
       r.transfer(source,'protector',{'protector':chosen})
       assert sum(b.amount for b in r.branches.values())==amount
       living_all(r)
       assert r.total()==amount
       states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW; exact implementation pending',
            'scope':'Bounded39-source stage, branch flags, transfer arithmetic, per-owner Paladin/Crown budget, retarget, finite Bloom/Palm and Tinker damage interface. Not full feature execution, all-source defense order, device repair lifecycle or balance.',
            'checkCount':len(checks),'conservationStates':states,'checks':checks}
    (ROOT/'docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} redirection checks and {states} transfer conservation states; review pending.')
if __name__=='__main__':main()


## Exact docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json

{
  "status": "PASS",
  "reviewStatus": "IN_REVIEW; exact implementation pending",
  "scope": "Bounded39-source stage, branch flags, transfer arithmetic, per-owner Paladin/Crown budget, retarget, finite Bloom/Palm and Tinker damage interface. Not full feature execution, all-source defense order, device repair lifecycle or balance.",
  "checkCount": 88,
  "conservationStates": 186,
  "checks": [
    "Quarter sharing precedes both recipients resistance",
    "Transferred portion loses attack-critical identity",
    "Original portion preserves hit and critical identity",
    "Pretransfer locks retained original against later transfer",
    "Quarter reaction cannot arbitrarily choose smaller share",
    "Strongest original flat reduction applies to retained share only",
    "Premitigation transfer accepts recipient defenses and pure prevention",
    "Flat strongest then resistance floor",
    "Postdefense split conserves remaining amount",
    "Postdefense child cannot defend again",
    "Postdefense child cannot use further pure prevention",
    "Postsplit original cannot use late pure prevention",
    "Unmitigated transfer still consumes temporary HP",
    "TemporaryHP absorption does not erase concentration packet",
    "Root totals await every terminal branch",
    "Physical total counts final recipients only",
    "Final branch cannot resolve twice",
    "Transferred critical damage causes one death failure",
    "Full transfer retains original hit without positive damage",
    "Aegis still transfers lethal packet but Ward can prevent death",
    "Survival replacement does not overcount actualHP damage",
    "Ordinary transfer dropping positiveHP to0 invokes Wound save",
    "A transferred branch cannot acquire original maiming rider",
    "Transferred branch rejects attack maiming rider",
    "Protective Stance cannot create nonexistent excess damage",
    "Shared Paladin ledger records one operation",
    "Second ordinary Paladin event rejected",
    "Failed shared allowance leaves root unchanged",
    "Failed shared allowance does not add ledger event",
    "Different Paladin keeps independent round allowance",
    "Different owner cannot transfer already split root",
    "Automatic rounded0 share creates no operation",
    "Automatic0 leaves root unclaimed",
    "Optional0 transfer cannot activate",
    "Burden is one multi-recipient operation",
    "Burden physical total includes all branches",
    "Burden healing consumer excludes prohibited branches",
    "Burden resource consumer excludes prohibited branches",
    "Source target predicate still filters final recipients",
    "Warrior transfer bans BT only",
    "Warrior transfer does not invent universal resource ban",
    "Paladin reflection ban does not suppress all retaliation",
    "Paladin generic engine does not forbid healing generation",
    "Protective Stance suppresses generic damage-generated healing",
    "Unbroken Covenant triggers on redirection despite noDamageTriggers",
    "Unrelated later healing of recipient remains legal",
    "Crown permits two different events for same selected ally",
    "Crown healing floors per event then uses cumulative cap",
    "Crown third event rejected",
    "Crown heal cannot be settled twice",
    "Midround Crown activation preserves previous ordinary use",
    "Crown activation cannot reset shared event history",
    "One Crown plus one ordinary allowed with Crown active in either order",
    "Crown amount cap independent of remaining event slot",
    "Failed amount cap leaves one event",
    "Blocked Crown heal yields0actual",
    "Blocked Crown healing consumes nominal cap",
    "Final Stand constrained to one shared event that round",
    "Final Stand is an automatic profile",
    "Bloom pool persists across small packet",
    "Bloom depletion leaves remainder and starts rider",
    "Suppression neither consumes nor ends Bloom",
    "Suppressed Bloom retains full capacity",
    "Late observation preserves expiry-based rider deadline",
    "Unmitigated transfer cannot spend recipient Bloom",
    "Rejected Bloom attempt preserves finite pool",
    "Guardian uses original roll against own AC",
    "Attack cannot bounce to another Guardian",
    "Original attack cannot reroll on retarget",
    "Counter must wait for full original attack resolution",
    "Missed incoming attack still permits single legal counter",
    "Counter opportunity cannot replay",
    "A free counter cannot manufacture another free counter",
    "Attack retarget leaves later transfer opportunity intact",
    "Palm prevents floorhalf and caps separate force packet",
    "Palm force counter accepts new recipient defenses",
    "Palm counter is not an attack hit",
    "Palm counter cannot create free attack or copy",
    "Palm reduction remains without a second enemy",
    "Palm still reduced original damage",
    "Palm cannot send force back to original attacker",
    "Invalid counter target does not consume prevention",
    "Ranged attack cannot activate Palm",
    "Emergency drone destruction uses device consequences",
    "Device transfer does not manufacture an enemy attack hit",
    "Emergency drone transfer suppresses retaliation consumer",
    "Destroyed drone cannot receive another functional packet",
    "False positiveHP destroyed device rejected"
  ]
}


## Exact docs/mechanics/REDIRECTION_SOURCE_VALIDATION.json

{
  "status": "PASS",
  "exactRecords": 39,
  "supportingEnginePassages": 2,
  "scope": "Original source equality, hashes and complete individual classification; not proof of semantic completion.",
  "issues": []
}


## Exact docs/mechanics/DAMAGE_SHARING_PLAYTEST.md

# Damage sharing, prevention and interception

**IN REVIEW —39 exact source passages and two supporting Tinker engine passages.** This candidate implements the supplied damage-sharing interface. It does not establish every item/spell defense, companion lifecycle, all-source attack chain or numerical balance. Original source cards remain unchanged.

Read the [source register](REDIRECTION_SOURCE_BINDINGS.md), [source checks](REDIRECTION_SOURCE_VALIDATION.json), [reference checks](REDIRECTION_PLAYTEST_VALIDATION.json), [first notebook proposal](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md) and [complete corrections](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_BOUNDARIES.md). Later corrections supersede the retained first proposal.

## Resolve the kind of protection first

Guardian Pulse changes the target of an attack before comparing its original roll with AC. The Guardian becomes the actual hit/miss and on-hit-rider target. One attack can be retargeted once. Multiple offers are chosen by the original intended target; only the selected Guardian spends its Reaction/use. After the incoming attack fully resolves, a surviving, eligible Guardian may make the printed counterattack against an attacker in reach whether the original attack hit or missed. This free attack cannot grant another free attack or Action. Retargeting does not spend the later damage-transfer opportunity.

Bloodbond and Veinlock Tether divide the finalized raw damage before either recipient's mitigation. Attack/save success, save-halving and critical dice have already determined that amount. Bloodbond transfers one quarter, rounded down; Veinlock instead chooses up to S+M. Each recipient applies its own eligible defenses once to its own share.

Other supplied damage transfers divide damage after the original target's defenses and legal pure prevention, before temporary HP. Their transferred portions keep damage type and skip another DR/resistance/immunity/prevention stage. Temporary HP, applicable HP floors, would-die replacements, Wounds, concentration and ordinary life consequences still apply. “Unmitigated damage” does not mean “death cannot be prevented.”

Pure prevention removes damage without creating a second recipient. Elemental Absorption adds its resistance during ordinary defenses. Aura of Bonds and Crown reductions use the strongest applicable class flat reduction, then resistance/immunity. Finite/reactive prevention such as Bloom and Ancestral Guardian follows those defenses before post-defense transfer and temporary HP. Verify additional item/spell sources before treating this as universal defense ordering.

Redirecting Palm prevents half the Monk's post-defense damage, rounded down. The Monk keeps the remainder. A second enemy distinct from the triggering melee attacker, within5feet, can receive new force damage equal to the prevented amount, capped at Monk level. That new damage gets its own defenses; it is not a transferred attack or critical hit. With no second enemy, the Monk still receives the reduction.

Direct HP payments from Blood Sacrifice, Flesh-to-RP, Profane Exchange and Channel Life stay outside the damage sequence. They bypass temporary HP, obey their own legal minimum HP and do not create damage/Wound/resource triggers from paying the cost. Healing-recipient substitution and excess-healing conversion also remain distinct operations.

## One transfer operation and exact amounts

A root here means one original recipient's damage packet. A shared area cast has a separate root for each original recipient, under the same cast/roll identity.

One such root accepts one damage-sharing operation across all owners. A pre-mitigation split locks both its retained original portion and transferred portions against later transfer. Burden Shared can divide one operation among up to two other explicitly willing recipients. It does not create two redirection events. No transferred recipient may be the original damage target.

Select eligible mandatory/automatic protection before optional offers; competing mandatory claims are chosen by the original damage target. The exact arbitration between pre-mitigation optional and post-defense mandatory offers is being checked in implementation review. The helper accepts an already selected legal operation; it does not select Reactions or schedule automatic offers.

Optional transfer requires a positive chosen amount and available damage. Zero transfer cannot spend an optional Reaction/resource/use. A mandatory rounded-zero share does nothing and spends no transfer allowance. An independently legal prevention component can still occur.

| Source | Transferred amount |
|---|---|
| Bloodbond | floor(raw damage/4), fixed |
| Veinlock Tether / Shared Breath / Selfless Guardian | chosen up to S+M |
| Protective Stance / Emergency Protocols | min(S+M, available damage), fixed |
| Life Linked | chosen up to floor(available damage/2) |
| Guardian Tissue | floor(available damage/3), fixed |
| Aegis Incarnate / Martyr's Share | floor(available damage/2), fixed |
| Chainbound Smite | chosen up to max(3, actual CHA modifier) |
| Linked Ward | chosen up to max(2, twice actual CHA modifier) |
| King's Smite protection | chosen up to5 |
| Aura of the Crown | chosen up to M |
| Crown of Embers / Burden Shared | chosen up to level+M |
| Crown Undying | chosen up to remaining level+M round allowance |
| Final Stand | all available damage, subject to shared allowance |

Every amount is capped by the available packet at its source's stage. Fixed fractions/fixed protection cannot voluntarily choose a smaller amount. Original actions, range, willingness, costs, active-state requirements, cadence and source-specific use limits still apply.

## Hit identity and final damage accounting

The original damage target retains its original hit, failed-save, critical and on-hit-rider identity even if all damage is transferred. A rider that requires positive damage must recheck the actual remaining packet. A transferred recipient was not hit by that attack and did not fail its save; it receives no attached poison/control/maiming/knockout rider merely because damage moved.

Accordingly, transferred damage from a critical attack gives an already0HP recipient the ordinary one damage failure, not two critical-hit failures. Concentration still sees the transferred recipient's resolved packet even if temporary HP absorbs all of it.

Use the [reviewed life-state interface](HEALING_DEATH_PLAYTEST.md) after resolving each final recipient. Numeric actual damage is temporary HP absorbed plus actual normal HP lost, excluding overkill and damage prevented by an HP floor. Sum each terminal recipient once. Do not also count the unsplit parent or unrelated counterdamage.

Physical root totals include every recipient. A healing/resource/reflection consumer sums only branches permitted for that consumer and qualifying for its own source's target predicate. For example, a meaningful-hostile-only drain does not automatically count damage transferred onto a friendly protector. Check all applicable flags for a compound trigger, such as a passive healing proc.

## Source-specific restrictions

All transfers prohibit another transfer. All supplied post-defense transfers prohibit another mitigation/prevention stage. Further restrictions differ:

| Source family | Additional restrictions on transferred damage |
|---|---|
| Paladin engine | No reflection or resource generation; does not universally prohibit other retaliation or healing |
| Protective Stance | Also no generic damage-trigger chains |
| Burden Shared | Also no derived healing |
| Oracle Life Linked | No reflection, resource/RC, passive, condition, action or copy generation; no recovery or retaliation |
| Guardian Tissue / Aegis | No BT generation; no invented ban on every other resource |
| Shared Breath | No additional generic trigger prohibition |
| Selfless Guardian / Emergency Protocols | No retaliation chain |
| Bloodbond / Veinlock | Each recipient still has its one defense stage; no additional blanket prohibition |

A no-derived-healing flag does not prevent unrelated later healing of the recipient.

The source's explicit redirection riders remain narrowly available. Unbroken Covenant triggers on the redirection operation, even when Protective Stance prohibits generic damage triggers; use half the final protector actual damage, capped at S+M. Linked Ward's own transfer granting temporary HP on reducing the Paladin to0 uses final actual damage, capped at level+M. Final Stand's printed zero-HP protection remains its own rider. None grants a generic permission to ignore other source restrictions. Temporary HP still uses the larger remaining amount and does not stack.

## Paladin round ledger

Track each Paladin owner's numbered-round events. Ordinarily, one redirection event is available, using exactly one Paladin redirection feature. Final Stand is automatic on the first eligible positive post-defense packet while its allowance remains; the Paladin cannot save it for a later hit. Its “all damage” text does not override the explicit engine ceiling. It may redirect again in a later numbered round if still active before its source-next-start deadline.

Crown Undying can raise the owner's total to two different damage events, with at most one ordinary/non-Crown feature. The additional permission belongs to Crown Undying. A prior ordinary redirection remains recorded if Crown activates later in the same round; only one further Crown event is then possible. Reapplication does not clear history.

The two Crown events may protect the same selected ally. Sum Crown-transferred amounts against level+M per round. Its heal is floor(final Paladin branch actual damage/2) for each event, then capped by the remaining S+M per protected ally that round. Commit that nominal source entitlement before target healing restrictions; blocked or capped healing refunds no event, transfer amount or healing entitlement. The heal cannot heal the Paladin or start another redirection/heal-copy chain.

## Bloom and devices

Bloom Ward is a finite10+Oracle-level prevention pool across packets. Apply its legal prevention after ordinary defenses. Subtract only the prevented amount. The bloom ends on depletion, its1minute expiry, or actual legal removal. Suppression alone does not end it. Ending grants the printed +1 Frightened-save rider through the target's next end. A late clock observation must retain the endpoint calculated from the actual expiry, not create a fresh duration. An unmitigated transferred branch cannot consume this prevention pool.

Emergency Protocols requires an active/conscious drone within its printed range. The transfer occurs after the Tinker's defenses and before temporary HP. The drone receives the bounded transferred amount without mitigation; legally granted temporary HP can absorb it. At0HP the drone is destroyed and receives no organic Wound or death-save procedure.

Tinker engine[2] retains the destroyed drone at0 until its explicit repair/rebuild procedure. Ordinary functional repair cannot reconstruct a destroyed drone or reset ammunition, uses, duration or command budget. This package's device helper only resolves damage/destruction; it does not implement reconstruction or grant a destruction reward. The broader companion/device lifecycle remains open.

## Reference boundary

The helper validates arithmetic, stages, branch identity, replay protection and round entitlements. Callers establish legal sources, target relationships, exact source cadence, action/resource payment, clock endpoints and source-native riders. No helper imports card ownership merely from a string identifier. The source register preserves every exact original procedure alongside the overlay.

Validation currently covers88 targeted checks and186 conservation states. Full-game completion, human balance and all-source combat/device execution remain separate unfinished work.
