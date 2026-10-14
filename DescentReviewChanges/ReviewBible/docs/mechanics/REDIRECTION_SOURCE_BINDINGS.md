# Damage sharing source register

**REVIEWED / reference-VALIDATED; bounded interface —39 exact passages.** Source integrity and individual discussion do not prove complete feature execution.

[Procedure](DAMAGE_SHARING_PLAYTEST.md) · [Integrity](REDIRECTION_SOURCE_VALIDATION.json)

## cleric.hero.priest.cosmic-equilibrium

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · HEALING_REDIRECTION

Source `data/public/class_playtests/cleric.json` / `cleric.hero.priest.cosmic-equilibrium` · SHA256 `511b9a9abd80cc33649c3a30d73c03139189a2443a25ae92b7905fbdb0251787`.

**name:** Cosmic Equilibrium

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** 15-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** 1/short rest

**effect:** Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other.

**First proposal (historical; later overrides take precedence):** Redirects genuine excess healing into new radiant damage; reverse conversion creates healing. Existing excess ledger/no-recursion rules apply.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## cleric.hero.cultist.blood-sacrifice

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DIRECT_HP_LOSS_EXCLUSION

Source `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.blood-sacrifice` · SHA256 `073e2e574467aaae7193dfd80d27b74c4b3ccc4db41a45a4d59ab3208ad335fe`.

**name:** Blood Sacrifice

**activation:** Bonus Action

**cost:** Lose S+M actual HP from yourself or one willing ally within 5 ft

**rangeAndTarget:** Self or one willing ally within 5 feet

**duration:** Empowerment lasts until end of your next regular turn

**frequency:** 1/short rest

**effect:** Blood Sacrifice. Tags: cultist, sacrifice, conviction. The chosen creature loses S+M actual HP; this loss cannot be reduced, redirected or transferred and cannot reduce it below 1 HP. The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain 1 Conviction. Your next damaging or healing Rite or Invocation before the end of your next regular turn adds 1d8 to one rolled damage or healing component. A creature must be willing unless the target is you.

**First proposal (historical; later overrides take precedence):** HP cost; never damage or redirectable.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## crimson-agent.engine[4]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · PRE_MITIGATION_TRANSFER_ENGINE

Source `data/public/class_playtests/crimson-agent.json` / `4` · SHA256 `d0684cf6ddc12e65f87fcef501168f0a256d9bd62bb8a9d1377c978a682eadb7`.

**text:** Veinweaves are self buffs unless their card expressly allows an ally. They require concentration and one may be active. Crimson Harmony is an explicit exception permitting two Veinweaves as one linked concentration burden; a failed concentration check ends both. A non-Veinweave concentration effect replaces the whole group. BG is spent on activation; no upkeep unless printed. Damage-sharing is redirection before mitigation, not extra damage: apply each recipient's own defenses once and never redirect the redirected portion again.

**First proposal (historical; later overrides take precedence):** Veinweave sharing splits before mitigation; each recipient defends once; no retransfer.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## crimson-agent.engine[5]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DIRECT_HP_LOSS_EXCLUSION

Source `data/public/class_playtests/crimson-agent.json` / `5` · SHA256 `f0909f1cf6ccaa56c2438dd0a9dd04e6b96640047167d9f79da6298b765de52a`.

**text:** The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds.

**First proposal (historical; later overrides take precedence):** Sacrifice guard; no damage pipeline.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## crimson-agent.hero.bloodweaver.bloodbond

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · PRE_MITIGATION_TRANSFER + TEMP_HP_RIDER

Source `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.bloodweaver.bloodbond` · SHA256 `1113d2b822287bb66bb1759c1d7e674dbcb87534005a9e65e5111bb51b5c1263`.

**name:** Bloodbond

**activation:** Bonus Action

**cost:** 2 RP

**rangeAndTarget:** One willing ally within 30 ft

**duration:** Concentration, 3 of your turns

**frequency:** Recharge 3

**effect:** Create Bloodbond while both remain within 30 ft. When ally takes damage, you may use Reaction to redirect floor(one-quarter of pre-mitigation damage) to yourself; each recipient applies its own defenses once. Once/round when a paid technique heals you, ally gains M temporary HP. No recursive transfers.

**First proposal (historical; later overrides take precedence):** Quarter pre-mitigation split; each recipient defends once. Paid actual heal to owner can grant ally temp HP under reviewed healing predicate.

**Transfer contract:** {"phase": "raw", "formula": "quarter", "flags": ["noRetransfer"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## crimson-agent.hero.bloodweaver.veinlock-tether

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · PRE_MITIGATION_TRANSFER

Source `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.bloodweaver.veinlock-tether` · SHA256 `2b7d8566a5825d619cde6e1a7c9ed56616c05c75df3864153fbc830fa33f5f96`.

**name:** Veinlock Tether

**activation:** Reaction

**cost:** 1 BG

**rangeAndTarget:** Willing linked ally within 30 ft being damaged

**duration:** This damage only

**frequency:** Once/round

**effect:** While your Bloodbond or Vitality Link is active, redirect up to S+M damage to yourself before mitigation. This is an alternative to Bloodbond's quarter-sharing reaction, not an additional redirection. Redirected damage cannot be redirected again.

**First proposal (historical; later overrides take precedence):** Alternative to Bloodbond on same event; chosen amount ≤S+M and available packet.

**Transfer contract:** {"phase": "raw", "formula": "scale-mod", "flags": ["noRetransfer"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## mage.hero.elementalist.elemental-absorption

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION

Source `data/public/class_playtests/mage.json` / `mage.hero.elementalist.elemental-absorption` · SHA256 `4c696eef48c76379d0a6320cbac2b23324a197d1db8d6394b249a95750f1ec56`.

**name:** Elemental Absorption

**activation:** Reaction

**cost:** 3 RP

**rangeAndTarget:** Self

**duration:** Until end of your next regular turn

**frequency:** Recharge 3 rounds

**effect:** Elemental Absorption. Tags: mage-spell, elementalist, protection. Trigger when you would take fire, cold or lightning damage. Gain resistance to that triggering damage type for the triggering event and until the end of your next regular turn. Your next damaging Mage spell before then adds 1d8 of the absorbed type to one damage roll; the bonus is lost after use or expiry. This Reaction spell clears an incompatible current Nuke Chain unless the absorbed type is your current Focus.

**First proposal (historical; later overrides take precedence):** Adds resistance during ordinary defense stage; no transfer.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## mage.hero.lich.resonance-to-flesh

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DIRECT_HP_LOSS_EXCLUSION / HEAL

Source `data/public/class_playtests/mage.json` / `mage.hero.lich.resonance-to-flesh` · SHA256 `5692ac39a7de506bcf79cfcb7273630cf1f18c27e6d663ae380f764b78e3e8b2`.

**name:** Resonance to Flesh

**activation:** Action

**cost:** Variable conversion

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions.

**First proposal (historical; later overrides take precedence):** Flesh→RP direct HP cost; RP→Flesh ordinary healing.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## mirrorsage.arch.mirror-shell

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · RETALIATORY_DAMAGE

Source `data/public/class_playtests/mirrorsage.json` / `mirrorsage.arch.mirror-shell` · SHA256 `9885dead731ef2fecb13b62062346b24887c7a4ec5ae54de7089512ee3fac586`.

**name:** Mirror Shell

**activation:** Reaction

**cost:** 3 RP; 1 long-rest use

**rangeAndTarget:** A hostile spell targeting only you within 60 ft

**duration:** This spell

**frequency:** 1/long rest

**effect:** After a successful save against the spell or after its spell attack misses, choose its caster; it makes WIS save or takes S d8 force. Original damage/control follow normal results. No copying arbitrary spell text or redirecting an area spell.

**First proposal (historical; later overrides take precedence):** No redirection. Original spell already missed/saved; new force packet against caster on failed WIS save.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## monk.engine[13]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · EXCLUSION

Source `data/public/class_playtests/monk.json` / `13` · SHA256 `f6939b2e3293635fc6a652667c81e94984b14f8dfc5b43f3b86730e5b21f3584`.

**text:** Discipline Initiate is an optional Base selection. Choosing Tank does not grant five free Base abilities: it unlocks the four non-final Tortoise Discipline cards as additional Arch-selection options at their listed Monk levels. Final Form — Bastion of Breath is never a normal selection; at Monk 9 or the first later level when eligible it is gained automatically only if you chose Tank through Discipline Initiate and know at least three of Stone Shell Discipline, Redirecting Palm, Iron Shell Pulse and Echoing Guard. Tortoise Discipline remains compatible with any Hero path chosen later.

**First proposal (historical; later overrides take precedence):** Selection/progression only.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## monk.arch.tortoise.redirecting-palm

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION + RETALIATORY_DAMAGE

Source `data/public/class_playtests/monk.json` / `monk.arch.tortoise.redirecting-palm` · SHA256 `a849f3afc8e0ea4efe8243f4d150c8d6830c8f2e65f7681bd98b893406ac407a`.

**name:** Redirecting Palm

**activation:** Reaction

**cost:** 1 Ki; requires Discipline Initiate: Tank

**rangeAndTarget:** Triggering melee attacker and one other enemy within 5 feet of you

**duration:** Instantaneous

**frequency:** Once per round

**effect:** Redirecting Palm. Tags: arch, tortoise, discipline, counter. When a melee attack damages you, spend 1 Ki. Reduce the actual damage you take by half, rounded down. Choose one enemy other than you within 5 feet; it takes force damage equal to the amount prevented, maximum Monk level. If no second enemy is present, you still receive the reduction but redirect no damage.

**First proposal (historical; later overrides take precedence):** Prevent half post-defense packet; new force event = min(prevented,L).

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## monk.hero.enlightened-master.shared-breath

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER + HEALING_ECHO

Source `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.shared-breath` · SHA256 `da2757b79d797600e0823eed7b615b9165e4c9d81c88fbb6affa18018695c52e`.

**name:** Shared Breath

**activation:** Action

**cost:** 3 Ki + 2 RP

**rangeAndTarget:** One willing ally you touch

**duration:** Concentration, maximum 3 rounds

**frequency:** Recharge 4 rounds

**effect:** Shared Breath. Tags: hero, enlightened, link, weave. Link yourself to one willing ally. Once per round when either linked creature takes damage, the other may use its Reaction to take up to S+M of that damage instead; transferred damage cannot be reduced or redirected again. HP healing received by either creature also grants the other S HP once per round. The link ends if you separate by more than 30 feet.

**First proposal (historical; later overrides take precedence):** **NEW phase:** split post-defense/pre-tempHP; recipient gets no second mitigation. Existing causal-heal rules remain.

**Transfer contract:** {"phase": "defended", "formula": "scale-mod", "flags": ["noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## oracle.engine[14]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · ENGINE_GUARD

Source `data/public/class_playtests/oracle.json` / `14` · SHA256 `53c0ee49032421d155b7c10311016dcaf92540557980c6b9553327dc3f2f575d`.

**text:** Copied, echoed, repeated or redirected damage/healing uses only the explicitly copied numeric component. It cannot repeat RC recovery, Prophecy Triggers, action grants, conditions, passive triggers, resource restoration or another copy effect unless the copying feature explicitly says otherwise.

**First proposal (historical; later overrides take precedence):** Redirected numeric component carries no RC/Prophecy/passive/copy effects unless explicit.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## oracle.engine[29]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · ENGINE_GUARD

Source `data/public/class_playtests/oracle.json` / `29` · SHA256 `b1f27c6149ea8d930f2b1ac29e2e5a73de9991ef98d53045b5ba8b4f055fde81`.

**text:** Extra attacks and echoed damage use base weapon/spell dice before critical-hit extra dice. A redirected damage event cannot be reduced a second time, reflected again or generate RC. Charmed alone does not grant command of a creature's actions.

**First proposal (historical; later overrides take precedence):** Redirected damage cannot be reduced again/reflected again/generate RC.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## oracle.supplement.bones.bones-revelation-mastery

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · HEALING_REDIRECTION

Source `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.bones-revelation-mastery` · SHA256 `14d4537572a0e9d37eb62850c1881097ec9da711640be7b293b0ff0918640577`.

**name:** Bones Revelation Mastery

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** One eligible known Bones Revelation

**duration:** Permanent

**frequency:** Choose one upgrade at Oracle 15

**effect:** Choose one mastery for a Revelation you know. Enhanced Marrow Drain: a living target hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Ledger's Command: may target up to 3 undead, but all controlled undead still share one Bonus Action command per round. Enhanced Unfinished Chorus: when its drain resolves, you may always redirect the healing to one ally within 3 tiles of you rather than yourself; its healing cap remains S+M.

**prerequisite:** Oracle 15; Mystery: Bones; Revelation Mastery

**First proposal (historical; later overrides take precedence):** Enhanced Chorus chooses ally as recipient of same heal; not a child/second heal.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## oracle.supplement.life.bloom-ward

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION

Source `data/public/class_playtests/oracle.json` / `oracle.supplement.life.bloom-ward` · SHA256 `0252c7014f1020fe92cdd9c29f41c074d47a6d8c6babf5665f939529eb6a0543`.

**name:** Bloom Ward

**activation:** Passive and Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self; allies within 2 tiles; one ally within 3 tiles for bloom

**duration:** Passive permanent; bloom until consumed or 1 minute

**frequency:** Bloom 1/long rest

**effect:** Once per round when a living ally within 2 tiles receives HP healing from a paid or finite-use effect, add S HP to that healing. Reduce the first necrotic or poison damage you take each round by 1. Once per long rest place a protective bloom on one ally within 3 tiles. It absorbs the next 10+Oracle level damage dealt to that ally, then ends. When it ends, the ally gains +1 on saves against Frightened until the end of its next turn.

**prerequisite:** Oracle 1; Mystery: Life

**First proposal (historical; later overrides take precedence):** Finite `(10+L)` prevention pool across packets; no transfer.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## oracle.supplement.life.life-linked

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER + HEALING_INTERFACE

Source `data/public/class_playtests/oracle.json` / `oracle.supplement.life.life-linked` · SHA256 `e85dca21885aff801dd806929d567b1bfc05ea921792d259bab918337ea74c80`.

**name:** Life Linked

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One willing living ally within 5 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains; one Life Link at a time

**effect:** Link yourself to the ally. Once per round when it takes damage, you may use your Reaction to transfer up to half that actual damage rounded down to yourself. Transferred damage keeps its type and cannot be redirected again. The ally reduces the first necrotic damage it takes each round by S. Once per round when one of your paid or finite Oracle effects restores HP to the linked ally, it regains an additional 1d4 HP. The link ends if you are more than 5 tiles apart. Apply mitigation to the original damage once before splitting. The transferred portion cannot be mitigated again and cannot generate recovery or retaliation triggers.

**prerequisite:** Oracle 6; Mystery: Life; selected Tier II Revelation

**First proposal (historical; later overrides take precedence):** Original mitigation once, then transfer up to half; no second mitigation/recovery/retaliation from transfer.

**Transfer contract:** {"phase": "defended", "formula": "half-chosen", "flags": ["noActionGeneration", "noConditionTriggers", "noCopyGeneration", "noPassiveTriggers", "noRecoveryGeneration", "noReflection", "noResourceGeneration", "noRetaliation", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.engine[10]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER_ENGINE

Source `data/public/class_playtests/paladin.json` / `10` · SHA256 `240e342dd180de5c960ceeabad4c9a8302f5c4a1d0ddcb324310c42669cc4c93`.

**text:** Oath integration limits: one paid Smite total per round, including the level-7 Reaction; one Oath-aura reactive event per round. Multiple damage-redirection options share one event per round unless Crown Undying expressly allows two. Apply original-target defenses once, then split actual damage; transferred damage cannot be mitigated again, reflected, redirected again or generate resources. This explicit rule supersedes wording that permits recipient defenses again.

**First proposal (historical; later overrides take precedence):** Original defenses once; one paid Smite/round; one redirection event/round; no second mitigation/resource/retaliation.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.engine[14]

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · REDIRECTION_LIMIT_ENGINE

Source `data/public/class_playtests/paladin.json` / `14` · SHA256 `b38dbf499f21d489b9848610ad2d5bd91a94b22ccb0a92ca613d3fbb6fa51c0d`.

**text:** For any one damage event choose exactly one Paladin redirection feature. Using it consumes the shared redirection allowance for that round. Crown Undying permits two DIFFERENT ally-damage events per round, but still only one redirection feature may modify each event.

**First proposal (historical; later overrides take precedence):** Exactly one Paladin redirection feature/event; Crown Undying two different events exception.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.base.protective-stance

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.base.protective-stance` · SHA256 `71f0333a1fa9bee2ffd004f8327f542364d847dfd263df4bf80cb0fe324de5c7`.

**name:** Protective Stance

**activation:** Bonus Action

**cost:** One short-rest use

**rangeAndTarget:** Self; adjacent ally

**duration:** Until start next turn

**frequency:** 1/short rest

**effect:** Gain+1 AC. Once before end, Reaction interpose for adjacent ally hit by weapon: reduce its damage by S+M and take that much unpreventable damage yourself. Cannot redirect again or create resource/damage triggers. You must remain conscious.

**First proposal (historical; later overrides take precedence):** Redirect min(S+M, remaining damage); protector gets unmitigated branch.

**Transfer contract:** {"phase": "defended", "formula": "scale-mod-fixed", "flags": ["noDamageTriggers", "noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oathbreaker-shared.profane-exchange

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DIRECT_HP_LOSS_EXCLUSION

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-shared.profane-exchange` · SHA256 `bdd5dd43a3c0724146dadcb94d4907c4b169263f843b175a7e0f949404c32542`.

**name:** Profane Exchange

**activation:** Action

**cost:** 5 RP and S+M actual HP

**rangeAndTarget:** One creature touched

**duration:** Instant

**frequency:** Recharge 3

**effect:** New rank 3 Forbidden spell. You must have more current HP than the unpreventable HP cost. Target CON save, 2 S d8 necrotic on failure, half success. HP loss cannot be reduced, redirected, refunded or used for another resource trigger.

**prerequisite:** Paladin 9; selected Oathbreaker inversion

**First proposal (historical; later overrides take precedence):** Direct HP casting cost; not damage.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-mercy.channel-life

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DIRECT_HP_LOSS_EXCLUSION + HEAL

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.channel-life` · SHA256 `791e5b9a6f7de5962bffa02d02d406a4eba8aedc125391595cd002581a5f6610`.

**name:** Channel Life

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** Self and one living ally within 30 feet

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.

**prerequisite:** Paladin 9; Oath of Mercy

**First proposal (historical; later overrides take precedence):** Donor loss outside damage pipeline; recipient ordinary healing packet.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-chain.chainbound-smite

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.chainbound-smite` · SHA256 `e53ece673479a5f3c060e02521f0fc3941e296d875fd5dae13c785a8823741f4`.

**name:** Chainbound Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack; one bonded ally in your aura

**duration:** Smite instantaneous; redirection once before your next turn

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** The Smite deals radiant damage normally. After it resolves, choose one ally in your aura as bonded until the start of your next regular turn. Once before then when that ally takes damage, you may redirect up to max(3, actual Charisma modifier) of that damage to yourself. Redirected damage retains type and cannot be redirected again; the original target’s defenses apply once before transfer, with no further mitigation.

**prerequisite:** Paladin 3; Oath of the Chain

**First proposal (historical; later overrides take precedence):** Later bond redirect capped by actual CHA/min3 and available post-defense damage; shared Paladin allowance.

**Transfer contract:** {"phase": "defended", "formula": "cha-min3", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-chain.aura-of-bonds

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.aura-of-bonds` · SHA256 `e27219c1a397ba23aafd062a1d00d12b6e445eef8fd126f58dba8dadde534db1`.

**name:** Aura of Bonds

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen allies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Each selected ally reduces the first damage it takes each round by S. Multiple Aura of Bonds effects do not stack. This protection does not redirect damage and therefore does not trigger effects that require you to personally absorb damage.

**prerequisite:** Paladin 3; Oath of the Chain

**First proposal (historical; later overrides take precedence):** Flat class reduction, no transfer; participates in ordinary defense stage.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-chain.linked-ward

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER + TEMP_HP_RIDER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.linked-ward` · SHA256 `e733a4a1f12c01e46fa3b2bd23f1f24f319fbb98dd023f68575687a51eb8fba2`.

**name:** Linked Ward

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One willing ally in your Oath aura

**duration:** Concentration, maximum 3 rounds

**frequency:** At will while RP remains

**effect:** Mark one willing ally. Once per round when it takes damage, use your Reaction to redirect up to 2 times your actual Charisma modifier, minimum 2, of that damage to yourself. Redirected damage keeps its type and cannot be redirected again. If this redirected damage reduces you to 0 HP, the ally gains temporary HP equal to the amount you actually absorbed, maximum Paladin level+M.

**prerequisite:** Paladin 3; Oath of the Chain

**First proposal (historical; later overrides take precedence):** Redirect capped amount; if transfer reduces Paladin to0, ally gains temp HP from Paladin branch's actualDamageDealt, capped L+M.

**Transfer contract:** {"phase": "defended", "formula": "twice-cha-min2", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-chain.martyr-s-share

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.martyr-s-share` · SHA256 `a4bd7d95ebde62b625301dc9c6061ae018522e75796bd4586372f6ce0eb28851`.

**name:** Martyr's Share

**activation:** Reaction

**cost:** 5 RP

**rangeAndTarget:** One ally in your Oath aura taking damage

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Redirect half the ally's incoming damage, rounded down, to yourself. The ally takes the remainder. Redirected damage keeps its original type and cannot be redirected again. Your portion cannot be mitigated again after the original target’s defenses have applied. Effects attached to the original hit remain on the original target unless they explicitly depend on damage being dealt.

**prerequisite:** Paladin 9; Oath of the Chain

**First proposal (historical; later overrides take precedence):** Redirect floor(postDefenseDamage/2), ally retains remainder; hit riders remain original target.

**Transfer contract:** {"phase": "defended", "formula": "half", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-chain.final-stand

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.final-stand` · SHA256 `a30dfed5eb1e4a23d6db023e47c779202eb684a6a71013dd12ddf7e5cbbf77e0`.

**name:** Final Stand

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** One willing ally in your Oath aura

**duration:** Until start of your next regular turn

**frequency:** At will while RP remains

**effect:** Until the start of your next turn, all damage that would be dealt to the chosen ally is redirected to you instead. The redirected damage retains type, cannot be redirected again and cannot be mitigated again after the original target’s defenses apply once. If redirected damage reduces you to 0 HP, the ally immediately gains temporary HP equal to your Paladin level and resistance to all damage until the end of its next turn. This effect ends if you die outright.

**prerequisite:** Paladin 17; Oath of the Chain

**First proposal (historical; later overrides take precedence):** Transfers full remaining post-defense packet but constrained to one Paladin redirection event/numbered round.

**Transfer contract:** {"phase": "defended", "formula": "all", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": true, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-chain.unbroken-covenant

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · TEMP_HP_RIDER + REDIRECTION_MODIFIER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.unbroken-covenant` · SHA256 `513944a1ffe10dd0f5c74def4fee7a4d1248ee05fa668cceba673d4e1beb9f1c`.

**name:** Unbroken Covenant

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Your full Oath aura; up to 3 bonded allies

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds Warden's Lock fills your entire current Oath aura. Choose up to 3 allies there as bonded. Each bonded ally uses your AC if it is higher and cannot be forcibly moved against its will. Whenever you redirect damage from a bonded ally to yourself, that ally gains temporary HP equal to half the actual damage you absorb, rounded down, maximum S+M per event. Temporary HP do not stack. This Final grants no extra Reactions.

**prerequisite:** Paladin 20; Oath of the Chain

**First proposal (historical; later overrides take precedence):** Does not create redirect; when one occurs, ally temp HP = floor(Paladin transfer branch actualDamageDealt/2), cap S+M.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-martyr-king.king-s-smite

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER + TEMP_HP

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.king-s-smite` · SHA256 `d477840b93208eb5bca4155cbd47f455ccac24e5625dfdd29affc907abcf4b8c`.

**name:** King's Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack; one ally in your aura

**duration:** Smite instantaneous; temporary HP until lost; redirection passive while this Oath is active

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** The Smite deals radiant damage normally. After it resolves, choose one ally in your aura; it gains temporary HP equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Separately, once per round when an ally in your aura takes damage, you may redirect up to 5 of that damage to yourself. Apply the original target’s defenses once, then transfer up to 5 of the remaining damage. Transferred damage keeps its type and cannot be reduced again, reflected, redirected again or generate resources.

**prerequisite:** Paladin 3; Oath of the Martyr King

**First proposal (historical; later overrides take precedence):** Smite temp HP uses root Smite actualDamageDealt; separate once/round post-defense redirect ≤5.

**Transfer contract:** {"phase": "defended", "formula": "five", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-martyr-king.aura-of-the-crown

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.aura-of-the-crown` · SHA256 `8e16b8a024ca633bd4d3be4340aed54a46e4a2618dd1a4dfd70cda0742090783`.

**name:** Aura of the Crown

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen allies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn; redirect once per round

**effect:** Selected allies gain +1 on saving throws. Once per round when one selected ally takes damage, you may use your Reaction after that target applies its defenses once to redirect up to M of its remaining damage to yourself. The transferred amount cannot be reduced, reflected, redirected again or generate resources. This consumes the shared Paladin redirection allowance.

**prerequisite:** Paladin 3; Oath of the Martyr King

**First proposal (historical; later overrides take precedence):** Reaction after target defense; redirect ≤M; shared allowance.

**Transfer contract:** {"phase": "defended", "formula": "mod", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-martyr-king.crown-of-embers

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION + POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.crown-of-embers` · SHA256 `0ff07991fa0838522e96deb9434534c8c584850c6203ed3b47e8eeaf4246980f`.

**name:** Crown of Embers

**activation:** Bonus Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 allies in your Oath aura

**duration:** Until start of your next regular turn

**frequency:** 1/short rest

**effect:** Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself.

**prerequisite:** Paladin 11; Oath of the Martyr King

**First proposal (historical; later overrides take precedence):** S prevention first; then at most one eligible Crown redirect from remaining packet, shared allowance.

**Transfer contract:** {"phase": "defended", "formula": "level-mod", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-martyr-king.burden-shared

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_MULTI_TRANSFER

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.burden-shared` · SHA256 `2a0ff54276d9127ac30458bae7ea5dc0f1295b5ec34ca63bb5ce22efdabb29d1`.

**name:** Burden Shared

**activation:** Reaction when an ally takes damage

**cost:** 5 RP

**rangeAndTarget:** Triggering ally and up to two other willing allies in your aura

**duration:** One damage event

**frequency:** While RP remains

**effect:** After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round.

**prerequisite:** Paladin 9; Oath of the Martyr King

**First proposal (historical; later overrides take precedence):** One redirection operation can split ≤L+M among up to two willing recipients; no second mitigation/redirect/reflection/heal/resource.

**Transfer contract:** {"phase": "defended", "formula": "level-mod", "flags": ["noHealingGeneration", "noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 2}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## paladin.supplement.oath-of-the-martyr-king.crown-undying

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION + POST_DEFENSE_TRANSFER + HEAL

Source `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.crown-undying` · SHA256 `f8de6f3fe586c6b30d10bbdd31c93e0976aa46dfb3631afbbcbebe8ebe1d0b1d`.

**name:** Crown Undying

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to three selected allies in your aura

**duration:** Three rounds; no concentration

**frequency:** 1/long rest

**effect:** For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.

**prerequisite:** Paladin 20; Oath of the Martyr King

**First proposal (historical; later overrides take precedence):** Two different ally events/round, L+M transferred total. Heal each protected ally from half Paladin branch actualDamageDealt, cap S+M; blocked/capped heal never refunds entitlement.

**Transfer contract:** {"phase": "defended", "formula": "level-mod", "flags": ["noReflection", "noResourceGeneration", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## shaman.arch.ancestral-guardian

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · DAMAGE_PREVENTION

Source `data/public/class_playtests/shaman.json` / `shaman.arch.ancestral-guardian` · SHA256 `2017eae94ed31d166adb032bf4a724b44206a006fbf7fc23ec6eb0e6fa5aae8e`.

**name:** Ancestral Guardian

**activation:** Reaction

**cost:** 2 RP

**rangeAndTarget:** Ally within 30 ft being damaged

**duration:** One damage instance

**frequency:** Recharge 3

**effect:** A guardian prevents S d8+M damage, minimum 0. It then vanishes and creates no companion action, corpse or refund. Cannot prevent sacrifice/trauma or redirect prevented damage into another trigger.

**First proposal (historical; later overrides take precedence):** Prevent min(Sd8+M, available damage); no transfer/corpse/refund.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## soldier.hero.champion.selfless-guardian

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/soldier.json` / `soldier.hero.champion.selfless-guardian` · SHA256 `1ee9c213d3529b63f88c35415e680695e87faf9a6e5459903c12ebcf04c25c56`.

**name:** Selfless Guardian

**activation:** Reaction

**cost:** 0

**rangeAndTarget:** One adjacent ally taking direct weapon damage

**duration:** One hit

**frequency:** Once/round

**effect:** Redirect up to S+M of that damage to yourself. Redirected damage cannot be reduced, redirected again or trigger retaliation. The ally takes the rest after its own mitigation.

**First proposal (historical; later overrides take precedence):** Ally mitigates first; redirect ≤S+M from remainder; self gets no second mitigation/retaliation.

**Transfer contract:** {"phase": "defended", "formula": "scale-mod", "flags": ["noRetaliation", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## tinker.arch.emergency-protocols

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER + COMPANION_DEVICE

Source `data/public/class_playtests/tinker.json` / `tinker.arch.emergency-protocols` · SHA256 `ac7d27cd219c8e7e7ee81ba88425c48850dbac9861ea85a06d715ab99ad905ff`.

**name:** Emergency Protocols

**activation:** Reaction

**cost:** 1 encounter use

**rangeAndTarget:** Drone within 10 ft when attack hits you

**duration:** One hit

**frequency:** 1/encounter

**effect:** Drone intercepts: reduce damage to you by S+M and takes same amount unmitigated. It must be active/conscious. Does not redirect again or trigger retaliation loops.

**First proposal (historical; later overrides take precedence):** **NEW phase:** after user's defenses, before tempHP; redirect min(S+M,remaining) to drone unmitigated.

**Transfer contract:** {"phase": "defended", "formula": "scale-mod-fixed", "flags": ["noRetaliation", "noRetransfer", "noSecondMitigation"], "blockedResources": [], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## warrior.hero.wardborn.guardian-tissue

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/warrior.json` / `warrior.hero.wardborn.guardian-tissue` · SHA256 `6758edbc7d9cf5f27f4866127fc8ef9b9df2a71a2d6f056030ca253381fdc1d6`.

**name:** Guardian Tissue

**activation:** Reaction

**cost:** 0

**rangeAndTarget:** One adjacent ally and self

**duration:** Instantaneous

**frequency:** Once per round

**effect:** Guardian Tissue. When an adjacent ally would take damage, reduce that ally's incoming damage by one-third rounded down. You take the prevented amount as damage of the same type. This transferred damage cannot be redirected again and cannot trigger another Guardian Tissue. Transferred damage cannot be reduced again, redirected again or generate BT.

**First proposal (historical; later overrides take precedence):** Redirect floor(postDefenseDamage/3); no second mitigation/BT/retransfer.

**Transfer contract:** {"phase": "defended", "formula": "third", "flags": ["noRetransfer", "noSecondMitigation"], "blockedResources": ["BT"], "automatic": false, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## warrior.hero.wardborn.aegis-incarnate

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · AUTOMATIC_POST_DEFENSE_TRANSFER

Source `data/public/class_playtests/warrior.json` / `warrior.hero.wardborn.aegis-incarnate` · SHA256 `5e223de7f6a979dac5c81bb5b26b2c3796c41100d9cbe813da435aa9cac54c6b`.

**name:** Aegis Incarnate

**activation:** Bonus Action

**cost:** 0

**rangeAndTarget:** Self and allies within 15 feet

**duration:** 3 rounds

**frequency:** 1/long rest; automatic Wardborn Final Form

**effect:** Final Form – Aegis Incarnate. For 3 rounds you cannot be forcibly moved or knocked Prone. Whenever an ally within 15 feet takes damage, automatically redirect half that damage rounded down to yourself after the ally's resistance but before its temporary HP; the ally takes the remainder. Redirected damage keeps its type, cannot be reduced again or generate BT, and cannot be redirected again. If taking the redirected damage would kill you outright, the redirection still occurs. This grants no extra Reaction requirement and does not stack with Guardian Tissue on the same damage event.

**First proposal (historical; later overrides take precedence):** Automatic half after original defenses/resistance, before tempHP; no second mitigation/BT/retransfer. Survival effects still legal.

**Transfer contract:** {"phase": "defended", "formula": "half", "flags": ["noRetransfer", "noSecondMitigation"], "blockedResources": ["BT"], "automatic": true, "maximumTransferredRecipients": 1}

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.

## warrior.hero.wardborn.guardian-pulse

**REVIEWED / reference-VALIDATED: bounded damage-sharing role only** · ATTACK_RETARGET + COUNTERATTACK

Source `data/public/class_playtests/warrior.json` / `warrior.hero.wardborn.guardian-pulse` · SHA256 `b0bb1ba7e3a0716a83932ecee97cafdc14a082891419ebdcf3299b674e6a4da9`.

**name:** Guardian Pulse

**activation:** Reaction

**cost:** 0

**rangeAndTarget:** One adjacent ally and triggering attacker

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** Guardian Pulse. Trigger when an adjacent ally is targeted by an attack. You become the target instead; resolve the original attack roll against your AC and defenses. After that attack fully resolves, if the attacker is within your melee reach, make one melee weapon attack against it. This counterattack is a free attack, cannot grant another free attack or Action, and occurs whether the redirected attack hit or missed.

**First proposal (historical; later overrides take precedence):** Retarget attack before AC resolution; Guardian becomes actual attack target. One original attack roll only. Counterattack afterward is a separate attack root whether original attack hit or missed.

**Overlay:** Use DAMAGE_SHARING_PLAYTEST.md and the source-specific transfer contract where present. Complete notebook corrections supersede the first proposal. Original action/cost/target/range/duration/use fields remain authoritative except explicitly identified overlays.

**Overlay:** Final94-check/186-state guide supersedes earlier proposals: mandatory priority within each stage; pretransfer locks root; Guardian new counter inherits only its action-chain flags; Palm new force has no invented proc restrictions.

**Open:** Wider card lifecycle/ownership/cost/target scheduling remains outside this interface; no all-source defense/companion/global action-engine closure.
