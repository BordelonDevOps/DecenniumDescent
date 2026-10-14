# Damage sharing, retargeting and prevention — source conference

Codex → Calibration Review. This is the exact39-passage redirection candidate set:32 cards and7 engine passages. It includes prohibited-transfer HP costs, reflection/reduction and non-damage healing redirection as exclusions. Classify every supplied source by exact ID; do not assume the word redirect identifies one universal operation. Preserve original source actions, costs, target willingness, range, clocks and limits.

The existing healing interface is closed only after receiving a resolvedDamage amount. It defines actualDamageDealt=tempAbsorbed+actualHpDamage for numeric drains AFTER recipient life resolution. That measure must not accidentally become the quantity being divided BEFORE tempHP. Original sources remain unchanged; proposed clarifications are review overlays.

Please author a bounded shared sequence and explicit source exceptions, and give adversarial examples for:

1. Guardian Pulse retargets an attack before AC/defenses and later counterattacks. Bloodbond/Veinlock Tether split before each recipient's own mitigation. Paladin/Oracle Life Link/Shared Breath/Soldier/Guardian Tissue/Aegis split after original defenses. Name the exact quantity/phase at each operation and the point at which original save/critical dice have already applied. Distinguish interception, damage prevention, typed transfer, retaliatory new damage, and numeric healing redirection.
2. Bloodbond pre-mitigation: does original attack/save determine raw packet before sharing? Original resistance must affect only retained portion; recipient resistance once on transferred portion. Can original-target flat DR apply before deciding share? No recursion for transferred portions. Multiple owners offering simultaneous transfers must not duplicate damage or multiply life-drain metrics.
3. Post-defense transfers: before original temporaryHP? Does recipient temporaryHP absorb a transfer described cannot-reduce/unmitigated? Aegis explicitly names before original tempHP. Are recipient HP floors/Wards and Core Wound/InstantDeath consequences preserved? Distinguish unpreventable damage from an explicit unpreventable DEATH; do not infer all survival defenses bypassed.
4. Who has actually taken damage, been hit, or become subject to an attached poison/control rider after full transfer? Does recipient suffer critical-at-zero double death failures when original attack was critical but did not hit them? Does its own concentration save use the received post-defense packet even if tempHP absorbs it? Transfer cannot manufacture an attack hit. State exact rules if sources are silent and label NEW.
5. Original-caster damage totals after split: sum actual damage across recipients once or count original only? Preserve per-target/current-turn caps and each source's no-resource/no-retaliation/no-healing flags. Paladin sources bar resource/retaliation; Crown Undying has explicit finite healing and Linked Ward/Unbroken Covenant have explicit tempHP results. Determine actual absorbed basis and priorities without counting overkill. Can blocked/capped healing restore an entitlement? (Expected no.)
6. Limits: shared Paladin1redirection event/round and exactly one Paladin redirection feature/event; Crown Undying permits2 DIFFERENT ally events with totalL+M/round, never2transfers on same event. Final Stand says all damage until next source start but shared cap says1event/round. Is Final Stand a source-specific cap exception, or constrained? Its operation would be materially different: resolve explicitly. Multiple sources owned by different characters also need per-root no-chain rules.
7. Protective Stance reduces ally byS+M and self takes that much unpreventable damage. Cap to actual available damage or can it harm protector for excess nonexistent damage? Shared Breath/Veinlock optional amounts likewise bounded by available packet. Guardian Tissue reduces one-third, Redirecting Palm 'reduce ... by half, rounded down' means preventedfloor(packet/2), retainedceil; forcecounter=min(prevented,L). Confirm source-specific rounding and no second ordinary defense on the transfer, while a NEW forcecounter is a separately defendable event.
8. Preventive Bloom absorbs next10+OracleL damage: finite buffer across packets or only one packet? Expiry/ending rider precise. Pure damage prevention (Ancestral Guardian, Elemental Absorption) isn't transfer and cannot create a corpse/resource event. Transfusion/ChannelLife/BloodSacrifice/ProfaneExchange/Flesh-to-RP costs remain direct HP loss outside the damage pipeline.

We need a procedure and exact binding of each39source, not a claim of full monster/spell/all-game semantics. Identify any additional source evidence needed before implementation.


## Preserved shared-class baseline (frozen file; quoted, not edited)


Roll once for each shared area/pulse and apply saves/defenses to each target separately; separate attacks roll separately. Halve once for a successful save and apply resistance/immunity normally. Same-named conditions/bonuses do not stack unless a printed cap allows it; same-stat flat bonuses from these class techniques use the strongest. Different resources remain separate. Damage reduction from these class features uses the strongest flat reduction, then applies resistance; it cannot create negative damage or healing. Temporary HP never stack; choose the larger remaining amount. Immunity is not reduced resistance.

Repeated permanent HP recovery must consume finite RP, a per-rest use or another finite resource; a combat-generated gauge alone never enables unlimited healing. Healing cannot exceed maximum HP or erase Wounds, death consequences, debt or Corruption unless explicit. Downed is living at 0 HP; dead is different. Resurrection requires a willing soul and sufficiently intact body, obeys its time window, cannot create a duplicate and never refunds the feature on failure to meet known prerequisites. Sacrificial HP is actual unpreventable loss, cannot be redirected or paid with temporary HP, and is not damage for resource triggers. It cannot reduce the donor below 1 unless a card expressly grants a death-triggered effect.

No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.

Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.



## cleric.hero.priest.cosmic-equilibrium

{"name": "Cosmic Equilibrium", "activation": "Action", "cost": "7 RP", "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet", "duration": "Concentration, maximum 3 rounds", "frequency": "1/short rest", "effect": "Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other.", "prerequisite": null}

## cleric.hero.cultist.blood-sacrifice

{"name": "Blood Sacrifice", "activation": "Bonus Action", "cost": "Lose S+M actual HP from yourself or one willing ally within 5 ft", "rangeAndTarget": "Self or one willing ally within 5 feet", "duration": "Empowerment lasts until end of your next regular turn", "frequency": "1/short rest", "effect": "Blood Sacrifice. Tags: cultist, sacrifice, conviction. The chosen creature loses S+M actual HP; this loss cannot be reduced, redirected or transferred and cannot reduce it below 1 HP. The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain 1 Conviction. Your next damaging or healing Rite or Invocation before the end of your next regular turn adds 1d8 to one rolled damage or healing component. A creature must be willing unless the target is you.", "prerequisite": null}

## crimson-agent.engine[4]

Veinweaves are self buffs unless their card expressly allows an ally. They require concentration and one may be active. Crimson Harmony is an explicit exception permitting two Veinweaves as one linked concentration burden; a failed concentration check ends both. A non-Veinweave concentration effect replaces the whole group. BG is spent on activation; no upkeep unless printed. Damage-sharing is redirection before mitigation, not extra damage: apply each recipient's own defenses once and never redirect the redirected portion again.

## crimson-agent.engine[5]

The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds.

## crimson-agent.hero.bloodweaver.bloodbond

{"name": "Bloodbond", "activation": "Bonus Action", "cost": "2 RP", "rangeAndTarget": "One willing ally within 30 ft", "duration": "Concentration, 3 of your turns", "frequency": "Recharge 3", "effect": "Create Bloodbond while both remain within 30 ft. When ally takes damage, you may use Reaction to redirect floor(one-quarter of pre-mitigation damage) to yourself; each recipient applies its own defenses once. Once/round when a paid technique heals you, ally gains M temporary HP. No recursive transfers.", "prerequisite": null}

## crimson-agent.hero.bloodweaver.veinlock-tether

{"name": "Veinlock Tether", "activation": "Reaction", "cost": "1 BG", "rangeAndTarget": "Willing linked ally within 30 ft being damaged", "duration": "This damage only", "frequency": "Once/round", "effect": "While your Bloodbond or Vitality Link is active, redirect up to S+M damage to yourself before mitigation. This is an alternative to Bloodbond's quarter-sharing reaction, not an additional redirection. Redirected damage cannot be redirected again.", "prerequisite": null}

## mage.hero.elementalist.elemental-absorption

{"name": "Elemental Absorption", "activation": "Reaction", "cost": "3 RP", "rangeAndTarget": "Self", "duration": "Until end of your next regular turn", "frequency": "Recharge 3 rounds", "effect": "Elemental Absorption. Tags: mage-spell, elementalist, protection. Trigger when you would take fire, cold or lightning damage. Gain resistance to that triggering damage type for the triggering event and until the end of your next regular turn. Your next damaging Mage spell before then adds 1d8 of the absorbed type to one damage roll; the bonus is lost after use or expiry. This Reaction spell clears an incompatible current Nuke Chain unless the absorbed type is your current Focus.", "prerequisite": null}

## mage.hero.lich.resonance-to-flesh

{"name": "Resonance to Flesh", "activation": "Action", "cost": "Variable conversion", "rangeAndTarget": "Self", "duration": "Instantaneous", "frequency": "1/short rest", "effect": "Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions.", "prerequisite": null}

## mirrorsage.arch.mirror-shell

{"name": "Mirror Shell", "activation": "Reaction", "cost": "3 RP; 1 long-rest use", "rangeAndTarget": "A hostile spell targeting only you within 60 ft", "duration": "This spell", "frequency": "1/long rest", "effect": "After a successful save against the spell or after its spell attack misses, choose its caster; it makes WIS save or takes S d8 force. Original damage/control follow normal results. No copying arbitrary spell text or redirecting an area spell.", "prerequisite": null}

## monk.engine[13]

Discipline Initiate is an optional Base selection. Choosing Tank does not grant five free Base abilities: it unlocks the four non-final Tortoise Discipline cards as additional Arch-selection options at their listed Monk levels. Final Form — Bastion of Breath is never a normal selection; at Monk 9 or the first later level when eligible it is gained automatically only if you chose Tank through Discipline Initiate and know at least three of Stone Shell Discipline, Redirecting Palm, Iron Shell Pulse and Echoing Guard. Tortoise Discipline remains compatible with any Hero path chosen later.

## monk.arch.tortoise.redirecting-palm

{"name": "Redirecting Palm", "activation": "Reaction", "cost": "1 Ki; requires Discipline Initiate: Tank", "rangeAndTarget": "Triggering melee attacker and one other enemy within 5 feet of you", "duration": "Instantaneous", "frequency": "Once per round", "effect": "Redirecting Palm. Tags: arch, tortoise, discipline, counter. When a melee attack damages you, spend 1 Ki. Reduce the actual damage you take by half, rounded down. Choose one enemy other than you within 5 feet; it takes force damage equal to the amount prevented, maximum Monk level. If no second enemy is present, you still receive the reduction but redirect no damage.", "prerequisite": null}

## monk.hero.enlightened-master.shared-breath

{"name": "Shared Breath", "activation": "Action", "cost": "3 Ki + 2 RP", "rangeAndTarget": "One willing ally you touch", "duration": "Concentration, maximum 3 rounds", "frequency": "Recharge 4 rounds", "effect": "Shared Breath. Tags: hero, enlightened, link, weave. Link yourself to one willing ally. Once per round when either linked creature takes damage, the other may use its Reaction to take up to S+M of that damage instead; transferred damage cannot be reduced or redirected again. HP healing received by either creature also grants the other S HP once per round. The link ends if you separate by more than 30 feet.", "prerequisite": null}

## oracle.engine[14]

Copied, echoed, repeated or redirected damage/healing uses only the explicitly copied numeric component. It cannot repeat RC recovery, Prophecy Triggers, action grants, conditions, passive triggers, resource restoration or another copy effect unless the copying feature explicitly says otherwise.

## oracle.engine[29]

Extra attacks and echoed damage use base weapon/spell dice before critical-hit extra dice. A redirected damage event cannot be reduced a second time, reflected again or generate RC. Charmed alone does not grant command of a creature's actions.

## oracle.supplement.bones.bones-revelation-mastery

{"name": "Bones Revelation Mastery", "activation": "Passive", "cost": "0 RC", "rangeAndTarget": "One eligible known Bones Revelation", "duration": "Permanent", "frequency": "Choose one upgrade at Oracle 15", "effect": "Choose one mastery for a Revelation you know. Enhanced Marrow Drain: a living target hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Ledger's Command: may target up to 3 undead, but all controlled undead still share one Bonus Action command per round. Enhanced Unfinished Chorus: when its drain resolves, you may always redirect the healing to one ally within 3 tiles of you rather than yourself; its healing cap remains S+M.", "prerequisite": "Oracle 15; Mystery: Bones; Revelation Mastery"}

## oracle.supplement.life.bloom-ward

{"name": "Bloom Ward", "activation": "Passive and Bonus Action", "cost": "0 RC", "rangeAndTarget": "Self; allies within 2 tiles; one ally within 3 tiles for bloom", "duration": "Passive permanent; bloom until consumed or 1 minute", "frequency": "Bloom 1/long rest", "effect": "Once per round when a living ally within 2 tiles receives HP healing from a paid or finite-use effect, add S HP to that healing. Reduce the first necrotic or poison damage you take each round by 1. Once per long rest place a protective bloom on one ally within 3 tiles. It absorbs the next 10+Oracle level damage dealt to that ally, then ends. When it ends, the ally gains +1 on saves against Frightened until the end of its next turn.", "prerequisite": "Oracle 1; Mystery: Life"}

## oracle.supplement.life.life-linked

{"name": "Life Linked", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "One willing living ally within 5 tiles", "duration": "2 rounds", "frequency": "At will while RC remains; one Life Link at a time", "effect": "Link yourself to the ally. Once per round when it takes damage, you may use your Reaction to transfer up to half that actual damage rounded down to yourself. Transferred damage keeps its type and cannot be redirected again. The ally reduces the first necrotic damage it takes each round by S. Once per round when one of your paid or finite Oracle effects restores HP to the linked ally, it regains an additional 1d4 HP. The link ends if you are more than 5 tiles apart. Apply mitigation to the original damage once before splitting. The transferred portion cannot be mitigated again and cannot generate recovery or retaliation triggers.", "prerequisite": "Oracle 6; Mystery: Life; selected Tier II Revelation"}

## paladin.engine[10]

Oath integration limits: one paid Smite total per round, including the level-7 Reaction; one Oath-aura reactive event per round. Multiple damage-redirection options share one event per round unless Crown Undying expressly allows two. Apply original-target defenses once, then split actual damage; transferred damage cannot be mitigated again, reflected, redirected again or generate resources. This explicit rule supersedes wording that permits recipient defenses again.

## paladin.engine[14]

For any one damage event choose exactly one Paladin redirection feature. Using it consumes the shared redirection allowance for that round. Crown Undying permits two DIFFERENT ally-damage events per round, but still only one redirection feature may modify each event.

## paladin.base.protective-stance

{"name": "Protective Stance", "activation": "Bonus Action", "cost": "One short-rest use", "rangeAndTarget": "Self; adjacent ally", "duration": "Until start next turn", "frequency": "1/short rest", "effect": "Gain+1 AC. Once before end, Reaction interpose for adjacent ally hit by weapon: reduce its damage by S+M and take that much unpreventable damage yourself. Cannot redirect again or create resource/damage triggers. You must remain conscious.", "prerequisite": null}

## paladin.supplement.oathbreaker-shared.profane-exchange

{"name": "Profane Exchange", "activation": "Action", "cost": "5 RP and S+M actual HP", "rangeAndTarget": "One creature touched", "duration": "Instant", "frequency": "Recharge 3", "effect": "New rank 3 Forbidden spell. You must have more current HP than the unpreventable HP cost. Target CON save, 2 S d8 necrotic on failure, half success. HP loss cannot be reduced, redirected, refunded or used for another resource trigger.", "prerequisite": "Paladin 9; selected Oathbreaker inversion"}

## paladin.supplement.oath-of-mercy.channel-life

{"name": "Channel Life", "activation": "Action", "cost": "5 RP", "rangeAndTarget": "Self and one living ally within 30 feet", "duration": "Instantaneous", "frequency": "At will while RP remains", "effect": "Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.", "prerequisite": "Paladin 9; Oath of Mercy"}

## paladin.supplement.oath-of-the-chain.chainbound-smite

{"name": "Chainbound Smite", "activation": "Triggered", "cost": "Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8", "rangeAndTarget": "Creature hit by your melee weapon attack; one bonded ally in your aura", "duration": "Smite instantaneous; redirection once before your next turn", "frequency": "One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance", "effect": "The Smite deals radiant damage normally. After it resolves, choose one ally in your aura as bonded until the start of your next regular turn. Once before then when that ally takes damage, you may redirect up to max(3, actual Charisma modifier) of that damage to yourself. Redirected damage retains type and cannot be redirected again; the original target’s defenses apply once before transfer, with no further mitigation.", "prerequisite": "Paladin 3; Oath of the Chain"}

## paladin.supplement.oath-of-the-chain.aura-of-bonds

{"name": "Aura of Bonds", "activation": "Passive", "cost": "0", "rangeAndTarget": "Up to 3 chosen allies in your Oath aura", "duration": "While conscious and target remains in aura", "frequency": "Choose targets at start of each turn", "effect": "Each selected ally reduces the first damage it takes each round by S. Multiple Aura of Bonds effects do not stack. This protection does not redirect damage and therefore does not trigger effects that require you to personally absorb damage.", "prerequisite": "Paladin 3; Oath of the Chain"}

## paladin.supplement.oath-of-the-chain.linked-ward

{"name": "Linked Ward", "activation": "Action", "cost": "2 RP", "rangeAndTarget": "One willing ally in your Oath aura", "duration": "Concentration, maximum 3 rounds", "frequency": "At will while RP remains", "effect": "Mark one willing ally. Once per round when it takes damage, use your Reaction to redirect up to 2 times your actual Charisma modifier, minimum 2, of that damage to yourself. Redirected damage keeps its type and cannot be redirected again. If this redirected damage reduces you to 0 HP, the ally gains temporary HP equal to the amount you actually absorbed, maximum Paladin level+M.", "prerequisite": "Paladin 3; Oath of the Chain"}

## paladin.supplement.oath-of-the-chain.martyr-s-share

{"name": "Martyr's Share", "activation": "Reaction", "cost": "5 RP", "rangeAndTarget": "One ally in your Oath aura taking damage", "duration": "Instantaneous", "frequency": "At will while RP remains", "effect": "Redirect half the ally's incoming damage, rounded down, to yourself. The ally takes the remainder. Redirected damage keeps its original type and cannot be redirected again. Your portion cannot be mitigated again after the original target’s defenses have applied. Effects attached to the original hit remain on the original target unless they explicitly depend on damage being dealt.", "prerequisite": "Paladin 9; Oath of the Chain"}

## paladin.supplement.oath-of-the-chain.final-stand

{"name": "Final Stand", "activation": "Action", "cost": "10 RP", "rangeAndTarget": "One willing ally in your Oath aura", "duration": "Until start of your next regular turn", "frequency": "At will while RP remains", "effect": "Until the start of your next turn, all damage that would be dealt to the chosen ally is redirected to you instead. The redirected damage retains type, cannot be redirected again and cannot be mitigated again after the original target’s defenses apply once. If redirected damage reduces you to 0 HP, the ally immediately gains temporary HP equal to your Paladin level and resistance to all damage until the end of its next turn. This effect ends if you die outright.", "prerequisite": "Paladin 17; Oath of the Chain"}

## paladin.supplement.oath-of-the-chain.unbroken-covenant

{"name": "Unbroken Covenant", "activation": "Bonus Action", "cost": "0 RP", "rangeAndTarget": "Your full Oath aura; up to 3 bonded allies", "duration": "3 rounds", "frequency": "1/long rest", "effect": "For 3 rounds Warden's Lock fills your entire current Oath aura. Choose up to 3 allies there as bonded. Each bonded ally uses your AC if it is higher and cannot be forcibly moved against its will. Whenever you redirect damage from a bonded ally to yourself, that ally gains temporary HP equal to half the actual damage you absorb, rounded down, maximum S+M per event. Temporary HP do not stack. This Final grants no extra Reactions.", "prerequisite": "Paladin 20; Oath of the Chain"}

## paladin.supplement.oath-of-the-martyr-king.king-s-smite

{"name": "King's Smite", "activation": "Triggered", "cost": "Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8", "rangeAndTarget": "Creature hit by your melee weapon attack; one ally in your aura", "duration": "Smite instantaneous; temporary HP until lost; redirection passive while this Oath is active", "frequency": "One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance", "effect": "The Smite deals radiant damage normally. After it resolves, choose one ally in your aura; it gains temporary HP equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Separately, once per round when an ally in your aura takes damage, you may redirect up to 5 of that damage to yourself. Apply the original target’s defenses once, then transfer up to 5 of the remaining damage. Transferred damage keeps its type and cannot be reduced again, reflected, redirected again or generate resources.", "prerequisite": "Paladin 3; Oath of the Martyr King"}

## paladin.supplement.oath-of-the-martyr-king.aura-of-the-crown

{"name": "Aura of the Crown", "activation": "Passive", "cost": "0", "rangeAndTarget": "Up to 3 chosen allies in your Oath aura", "duration": "While conscious and target remains in aura", "frequency": "Choose targets at start of each turn; redirect once per round", "effect": "Selected allies gain +1 on saving throws. Once per round when one selected ally takes damage, you may use your Reaction after that target applies its defenses once to redirect up to M of its remaining damage to yourself. The transferred amount cannot be reduced, reflected, redirected again or generate resources. This consumes the shared Paladin redirection allowance.", "prerequisite": "Paladin 3; Oath of the Martyr King"}

## paladin.supplement.oath-of-the-martyr-king.crown-of-embers

{"name": "Crown of Embers", "activation": "Bonus Action", "cost": "2 RP", "rangeAndTarget": "Up to 3 allies in your Oath aura", "duration": "Until start of your next regular turn", "frequency": "1/short rest", "effect": "Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself.", "prerequisite": "Paladin 11; Oath of the Martyr King"}

## paladin.supplement.oath-of-the-martyr-king.burden-shared

{"name": "Burden Shared", "activation": "Reaction when an ally takes damage", "cost": "5 RP", "rangeAndTarget": "Triggering ally and up to two other willing allies in your aura", "duration": "One damage event", "frequency": "While RP remains", "effect": "After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round.", "prerequisite": "Paladin 9; Oath of the Martyr King"}

## paladin.supplement.oath-of-the-martyr-king.crown-undying

{"name": "Crown Undying", "activation": "Bonus Action", "cost": "0 RP", "rangeAndTarget": "Up to three selected allies in your aura", "duration": "Three rounds; no concentration", "frequency": "1/long rest", "effect": "For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.", "prerequisite": "Paladin 20; Oath of the Martyr King"}

## shaman.arch.ancestral-guardian

{"name": "Ancestral Guardian", "activation": "Reaction", "cost": "2 RP", "rangeAndTarget": "Ally within 30 ft being damaged", "duration": "One damage instance", "frequency": "Recharge 3", "effect": "A guardian prevents S d8+M damage, minimum 0. It then vanishes and creates no companion action, corpse or refund. Cannot prevent sacrifice/trauma or redirect prevented damage into another trigger.", "prerequisite": null}

## soldier.hero.champion.selfless-guardian

{"name": "Selfless Guardian", "activation": "Reaction", "cost": "0", "rangeAndTarget": "One adjacent ally taking direct weapon damage", "duration": "One hit", "frequency": "Once/round", "effect": "Redirect up to S+M of that damage to yourself. Redirected damage cannot be reduced, redirected again or trigger retaliation. The ally takes the rest after its own mitigation.", "prerequisite": null}

## tinker.arch.emergency-protocols

{"name": "Emergency Protocols", "activation": "Reaction", "cost": "1 encounter use", "rangeAndTarget": "Drone within 10 ft when attack hits you", "duration": "One hit", "frequency": "1/encounter", "effect": "Drone intercepts: reduce damage to you by S+M and takes same amount unmitigated. It must be active/conscious. Does not redirect again or trigger retaliation loops.", "prerequisite": null}

## warrior.hero.wardborn.guardian-tissue

{"name": "Guardian Tissue", "activation": "Reaction", "cost": "0", "rangeAndTarget": "One adjacent ally and self", "duration": "Instantaneous", "frequency": "Once per round", "effect": "Guardian Tissue. When an adjacent ally would take damage, reduce that ally's incoming damage by one-third rounded down. You take the prevented amount as damage of the same type. This transferred damage cannot be redirected again and cannot trigger another Guardian Tissue. Transferred damage cannot be reduced again, redirected again or generate BT.", "prerequisite": null}

## warrior.hero.wardborn.aegis-incarnate

{"name": "Aegis Incarnate", "activation": "Bonus Action", "cost": "0", "rangeAndTarget": "Self and allies within 15 feet", "duration": "3 rounds", "frequency": "1/long rest; automatic Wardborn Final Form", "effect": "Final Form – Aegis Incarnate. For 3 rounds you cannot be forcibly moved or knocked Prone. Whenever an ally within 15 feet takes damage, automatically redirect half that damage rounded down to yourself after the ally's resistance but before its temporary HP; the ally takes the remainder. Redirected damage keeps its type, cannot be reduced again or generate BT, and cannot be redirected again. If taking the redirected damage would kill you outright, the redirection still occurs. This grants no extra Reaction requirement and does not stack with Guardian Tissue on the same damage event.", "prerequisite": null}

## warrior.hero.wardborn.guardian-pulse

{"name": "Guardian Pulse", "activation": "Reaction", "cost": "0", "rangeAndTarget": "One adjacent ally and triggering attacker", "duration": "Instantaneous", "frequency": "1/short rest", "effect": "Guardian Pulse. Trigger when an adjacent ally is targeted by an attack. You become the target instead; resolve the original attack roll against your AC and defenses. After that attack fully resolves, if the attacker is within your melee reach, make one melee weapon attack against it. This counterattack is a free attack, cannot grant another free attack or Action, and occurs whether the redirected attack hit or missed.", "prerequisite": null}