# Remaining lifecycle exact implementation review

Codex → Calibration Review. Review the actual bounded implementation below against all three saved conference decisions.124 targeted checks pass. Shared CreatureWorld change is additive known-created-object identity guarding; prior creature121/2800 regressions pass.80 original source records+5 frozen supports retain their hashes. Please identify concrete semantic defects, not claim the entire card/family complete. If no blockers, explicitly dispose only of selected lifecycle/command/object/guard roles; all exclusions remain.

Questions to scrutinize: canonical owner/target budgets and cross-round reservations; one post-hit interception per actual incoming attack and native zero assignment (caller executes existing creature lifecycle); Choir end snapshots and sealed-trigger/no-heal bursts; on-hit healing at zero damage; true corpse consumption; Palisade inventory/caps/repair; per-use turret quantity without a global2 cap; no Tinker permissions; Echo profile cap; narrative scout return deadline. First-damage DR opportunities are consumed before strongest-only arbitration. ExistingUndeadBuff.attack_bonus is a profile eligibility query; caller certifies the one source-authorized commanded attack, not every hit. No complete attack/condition runtime is asserted.

All source IDs and classifications (exact originals follow):

cleric.engine[2] — GUARD resource/corpse/agency/acquisition
{"text":"Only explicit features generate Conviction. Sacred Chant, Sermon of Purpose, Doctrine Shield, Dark Conviction and other printed cards are valid generators. A feature cannot generate more Conviction than its text permits, and Conviction can never exceed the current maximum. Summoned creatures, friendly creatures, trivial creatures, repeated corpse manipulation and staged out-of-combat actions cannot be used to farm Conviction."}

cleric.engine[7] — GUARD resource/corpse/agency/acquisition
{"text":"Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction."}

cleric.hero.saint.divine-rebirth — PREV resurrection/death; THP details remain later corpus
{"name":"Divine Rebirth","activation":"Triggered","cost":"0","rangeAndTarget":"One ally revived by your Cleric feature","duration":"Instantaneous plus temporary HP for 1 minute","frequency":"1/long rest","effect":"Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.","prerequisite":null}

cleric.hero.saint.resurrection — PREV resurrection/death; THP details remain later corpus
{"name":"Resurrection","activation":"Action","cost":"3 Conviction + 10 RP","rangeAndTarget":"One allied corpse you touch that died within the previous 1 minute","duration":"Instantaneous","frequency":"1/long rest","effect":"Resurrection. Tags: saint, resurrection, rite. Return the target to life at 1 HP and grant it 2 S + M temporary HP for 1 minute. It gains no removed Wounds and receives no restored expended resources beyond what another rule explicitly provides. A missing vital body prevents the effect. The Conviction expenditure can vent Dissonance once.","prerequisite":null}

cleric.hero.cultist.dark-conviction — GUARD resource/corpse/agency/acquisition
{"name":"Dark Conviction","activation":"Triggered","cost":"0","rangeAndTarget":"Self","duration":"Instantaneous","frequency":"At most once on each of your turns","effect":"Dark Conviction. Tags: cultist, conviction. During a real encounter, when a hostile non-summoned creature that meaningfully threatened the party dies after taking damage from one of your Cleric features since the start of your current turn, gain 1 Conviction. Friendly creatures, summoned creatures, trivial staged creatures and repeated corpse destruction never qualify.","prerequisite":null}

cleric.hero.cultist.rite-of-the-crimson-choir — LC + PREV companion/reanimation; retain reviewed healing/death components
{"name":"Rite of the Crimson Choir","activation":"Action","cost":"5 Conviction + 8 RP","rangeAndTarget":"Four unoccupied spaces within 30 feet","duration":"Concentration, maximum 3 rounds","frequency":"1/long rest","effect":"Final Miracle — Rite of the Crimson Choir. Tags: cultist, finale, summon, rite. Summon four spectral fanatics. Each has AC 14, 10 HP, Speed 30 feet and cannot take Reactions. Spend one Bonus Action on your regular turn to command the Choir; this explicitly priced Finale permits up to four surviving fanatics to each move up to its Speed and make one melee spell-like attack using your Cleric technique attack bonus against an enemy within 5 feet; on hit it deals 1d6+S necrotic damage and you regain 1 HP, maximum 4 HP per round from the Choir. When a fanatic reaches 0 HP, when concentration ends or after the third round, it explodes; enemies within 5 feet make Dexterity saves, taking 1d6 necrotic on failure or half on success. Fanatics grant no XP, loot, corpse, resurrection target or Conviction. The Conviction expenditure can vent Dissonance once.","prerequisite":null}

cleric.hero.cultist.ritual-of-undeath — LC + PREV companion/reanimation; retain reviewed healing/death components
{"name":"Ritual of Undeath","activation":"Action","cost":"3 Conviction + 6 RP","rangeAndTarget":"One eligible corpse within 30 feet or one living ally within 30 feet","duration":"Mode-dependent","frequency":"1/long rest","effect":"Ritual of Undeath. Tags: cultist, undead, rite. Choose one mode. Corpse Servant: one humanoid corpse dead no more than 1 minute rises for 3 rounds as a temporary thrall with AC 13, 10 HP, Speed 30 feet and one attack only when you spend your shared companion Bonus Action command using your Cleric technique attack bonus; on hit it deals S d6 necrotic. The thrall disappears at 0 HP or when duration ends and grants no XP, loot, new corpse, Conviction or resurrection target. Death Ward: one living ally is marked for 1 minute; the first time it would die during that duration, it instead remains at 1 HP and counts as both humanoid and undead until the end of its next turn. Neither mode removes Wounds. The Conviction expenditure can vent Dissonance once.","prerequisite":null}

crimson-agent.engine[0] — GUARD BG gain/anti-farm
{"text":"Blood Gauge (BG) starts and ends each encounter at 0, capacity 3; Spill Control raises capacity 6 while known. Once on your own regular turn, a weapon attack that damages a hostile living creature grants 1 BG. Hemorrhage Slash uses this same trigger, not an additional one. Explicit critical/kill/refund features can add more, but total BG gained is capped 2 per round. Self-inflicted damage, allies, summons, helpless captives and repeated damage to a corpse never generate BG. Blood is an encounter resource, not a currency carried into rest."}

crimson-agent.engine[5] — PREV healing/direct-HP/redirection + anti-farm
{"text":"The healing, execution and denial text below deliberately bounds the source's vague percentage/instant-kill claims. HP sacrificed is direct loss, bypasses temporary HP and defenses, cannot be redirected, and cannot reduce the donor below 1. Only a willing ally can donate. HP sacrifice is never damage for class triggers. No class feature here restores the dead or removes Wounds."}

crimson-agent.base.blood-tithe — PREV healing/direct-HP/redirection + anti-farm
{"name":"Blood Tithe","activation":"Triggered","cost":"1 short-rest use","rangeAndTarget":"Self after a hostile bleeding creature dies within 30 ft","duration":"Instant","frequency":"1/short rest","effect":"Regain HP equal to M+class level after a creature bearing your Bleed dies. It must have been an active hostile combatant; no ally, summon, captive or corpse farming.","prerequisite":null}

crimson-agent.arch.veinweave-bloodshield — DEFER THP/defense
{"name":"Veinweave: Bloodshield","activation":"Bonus Action","cost":"2 BG","rangeAndTarget":"Self","duration":"3 of your turns","frequency":"Recharge 3","effect":"Start Bloodshield Veinweave. Gain temporary HP equal to class level+M. Once while they remain, use Reaction to reduce damage to yourself by S. No self-damage refund or BG is generated.","prerequisite":null}

crimson-agent.hero.bloodweaver.bloodbond — PREV healing/direct-HP/redirection + anti-farm
{"name":"Bloodbond","activation":"Bonus Action","cost":"2 RP","rangeAndTarget":"One willing ally within 30 ft","duration":"Concentration, 3 of your turns","frequency":"Recharge 3","effect":"Create Bloodbond while both remain within 30 ft. When ally takes damage, you may use Reaction to redirect floor(one-quarter of pre-mitigation damage) to yourself; each recipient applies its own defenses once. Once/round when a paid technique heals you, ally gains M temporary HP. No recursive transfers.","prerequisite":null}

crimson-agent.hero.bloodweaver.crimson-pact — PREV healing/direct-HP/redirection + anti-farm
{"name":"Crimson Pact","activation":"Action","cost":"5 BG; 1 long-rest use","rangeAndTarget":"Up to 3 bleeding enemies and 6 living allies within 30 ft","duration":"Instant; shields 1 minute","frequency":"1/long rest","effect":"End your Bleeds on chosen enemies; each makes CON save against 4d8 necrotic, half on success. Each chosen ally regains 4d8+M HP and gains 10 temporary HP. Use one shared roll per damage/healing effect; healing does not multiply by enemies or remaining ticks.","prerequisite":null}

crimson-agent.hero.thirstborn.crimson-harvest — PREV healing/direct-HP/redirection + anti-farm
{"name":"Crimson Harvest","activation":"Action","cost":"2 BG; 1 short-rest use","rangeAndTarget":"One enemy in weapon reach at half HP or less","duration":"Instant","frequency":"1/short rest","effect":"Make one weapon attack; on hit add S d8 damage. If this reduces it to 0, regain S+M HP and 1 BG within gain cap. No instant kill from a percentage threshold; summoned/allied/helpless creatures yield no recovery.","prerequisite":null}

dragoon.engine[0] — GUARD Momentum/kill farming
{"text":"Strength is the class ability. Momentum starts/ends encounters at 0; cap 5, rising to 7 with Momentum Overflow or automatically at class 9. On each regular turn, moving at least 15 ft under your own power grants 1 Momentum, and damaging an enemy with a weapon attack grants 1 more. These are the only default gains; all gains/refunds together cap 2 per round. Forced movement, teleportation, movement in place, allies and summons cannot farm Momentum. Movement counts actual path traveled toward a tactical destination; one threshold per turn."}

dragoon.hero.dragon-guardian.momentum-shield — DEFER THP/full effect
{"name":"Momentum Shield","activation":"Passive","cost":"0","rangeAndTarget":"Self","duration":"Until start next turn","frequency":"Once/own turn","effect":"After spending at least 1 Momentum, gain temporary HP equal to amount spent+M, maximum 10. Later expenditure replaces with the higher remaining value; no real HP restoration.","prerequisite":null}

dragoon.hero.dragon-guardian.bastion-descent — DEFER THP/full effect
{"name":"Bastion Descent","activation":"Action","cost":"5 Momentum; 1 long-rest use","rangeAndTarget":"Leap within 30 ft; up to 6 allies within 15 ft of landing","duration":"Instant; protection until start next turn","frequency":"1/long rest","effect":"Land in empty space. Chosen allies gain 4d8+M temporary HP and may end Frightened or Poisoned. They gain resistance to the next damage instance before your next turn. No healing, resurrection or removal of Wounds.","prerequisite":null}

dragoon.hero.dragon-guardian.momentum-barrier — DEFER THP/full effect
{"name":"Momentum Barrier","activation":"Action","cost":"All Momentum, minimum 3","rangeAndTarget":"Up to 4 allies within 15 ft","duration":"Temporary HP 1 minute","frequency":"Recharge 4","effect":"Spend K Momentum. Each gains K+S d6 temporary HP, using one shared dice roll. These HP do not stack with other shields and no unspent Momentum remains. This is not concentration.","prerequisite":null}

dragoon.hero.dragon-tyrant.momentum-feeder — GUARD Momentum/kill farming
{"name":"Momentum Feeder","activation":"Triggered","cost":"0","rangeAndTarget":"Self on polearm critical or hostile kill","duration":"Instant","frequency":"Once/round","effect":"Gain 2 Momentum, still within total 2-per-round gain cap. A critical kill is one trigger, not two. Do Ts, copies, allies, summons and helpless creatures cannot trigger it.","prerequisite":null}

monk.base.discipline-initiate — DEFER incidental THP/discipline choice
{"name":"Discipline Initiate","activation":"Passive","cost":"0","rangeAndTarget":"Self","duration":"Permanent","frequency":"Choose once when acquired","effect":"Discipline Initiate. Tags: base, discipline. Choose Offense, Tank or Support. Offense technique: once per turn in Tiger after an unarmed hit, spend 1 Ki to deal +S damage and push the target 5 feet if it is no more than one size larger. Tank: unlock the Tortoise Discipline Arch cards under the common gate. Support technique: once per turn in Crane after an unarmed hit, spend 1 Ki to grant one ally within 15 feet S+M temporary HP. The chosen discipline cannot be changed without a future retraining rule.","prerequisite":null}

oracle.engine[6] — GUARD resources/agency/copy/redirection
{"text":"RC RECOVERY. A completed long rest restores RC to maximum. A completed short rest restores 1 spent RC, never above maximum. Each Mystery has exactly one Prophecy Trigger. During a real encounter, your Prophecy Trigger can restore at most 1 RC per round and never above maximum. Trivial enemies, willing staged targets, summoned sacrifices, repeated corpse abuse, copied damage, copied healing and events generated solely to trigger recovery do not qualify."}

oracle.engine[13] — GUARD resources/agency/copy/redirection
{"text":"Healing from Oracle features cannot exceed maximum HP, resurrect the dead or remove Wounds unless a feature explicitly says so. Temporary HP never stack. Encounter-only regeneration and drain cannot be farmed outside meaningful combat. Corpse effects create no XP, loot, RC or repeatable corpse resources unless expressly stated."}

oracle.supplement.spiral-touched.spiral-touched-boon-v — DEFER Time Loop snapshot interface
{"name":"Spiral-Touched — Boon V","activation":"Reaction before round 4","cost":"0","rangeAndTarget":"Recorded encounter participants","duration":"Restore recorded encounter-start state","frequency":"1/long rest","effect":"1/long rest as a Reaction before the fourth round of the encounter begins, rewind the current encounter to its initiative-start snapshot: restore combatant positions, HP, temporary HP, conditions, RC and per-encounter uses to that snapshot. Short-/long-rest uses, physical consumables and this Time Loop use remain spent. Slain encounter participants return to their snapshot state and no duplicate XP, treasure or consumables are created. Allies retain memory of the previous timeline. Time Loop does not restore RP, Ki, Conviction, Blood Gauge, device stock, healing reserves or any other daily/rest resource; only the named RC and per-encounter states rewind. No loot changes ownership through rewinding. Record the snapshot at initiative; if no complete snapshot exists, this option is unavailable and unspent. It cannot undo a previous encounter or duplicate a per-rest use.","prerequisite":"Oracle 20; selected Curse:Spiral-Touched"}

oracle.supplement.wound-eater.wound-eater-boon-iii — PREV death/direct-HP/healing
{"name":"Wound Eater — Boon III","activation":"Action","cost":"0","rangeAndTarget":"One dying hostile living creature touched","duration":"Instantaneous","frequency":"1/short rest; no staged/summoned targets","effect":"1/short rest as an Action touch one dying hostile living creature at 0 HP; that creature dies and you regain HP equal to one-quarter your maximum HP rounded down. It cannot trigger from summoned, trivial or staged creatures and removes no Wounds.","prerequisite":"Oracle 10; selected Curse:Wound Eater"}

oracle.supplement.wound-eater.wound-eater-boon-v — PREV death/direct-HP/healing
{"name":"Wound Eater — Boon V","activation":"Action","cost":"0","rangeAndTarget":"Up to three living enemies within 20 feet","duration":"Instantaneous","frequency":"1/long rest","effect":"1/long rest as an Action, up to three meaningful living enemies within 20 feet lose HP equal to the lesser of one-quarter their maximum HP or Oracle level+M; you regain half the total actual HP lost, capped at one-half your maximum HP. Allies, constructs, undead, trivial creatures and summons are unaffected.","prerequisite":"Oracle 20; selected Curse:Wound Eater"}

oracle.supplement.haunted.haunted-boon-v — LC scout/control/servants
{"name":"Haunted — Boon V","activation":"Action to summon","cost":"0","rangeAndTarget":"One spirit scout; one-mile same-plane route limit","duration":"10 minutes","frequency":"1/long rest","effect":"1/long rest summon one spirit scout for 10 minutes. It can travel along a route you have personally traveled on the same plane, up to 1 mile from you, observe with ordinary sight/hearing, speak with willing dead spirits it encounters and deliver one short prophetic message. On return it truthfully reports what it directly observed and may identify one unexpected creature or person's name it actually encountered. It cannot pass sealed planar barriers, read minds or reveal unknowable facts.","prerequisite":"Oracle 20; selected Curse:Haunted"}

oracle.supplement.battle.battle-prophecy-trigger — GUARD resources/agency/copy/redirection
{"name":"Battle Prophecy Trigger","activation":"Triggered","cost":"0 RC","rangeAndTarget":"Self","duration":"Instantaneous","frequency":"At most once per round during a real encounter","effect":"When you or an ally reduces a meaningful hostile creature to 0 HP, regain 1 RC, never above maximum. Summoned, trivial, friendly or repeatedly revived creatures do not qualify.","prerequisite":"Oracle 1; Mystery: Battle"}

oracle.supplement.bones.bones-prophecy-trigger — GUARD resources/agency/copy/redirection
{"name":"Bones Prophecy Trigger","activation":"Triggered","cost":"0 RC","rangeAndTarget":"Self; qualifying creature within 5 tiles","duration":"Instantaneous","frequency":"At most once per round during a real encounter","effect":"When an undead creature or meaningful hostile creature at 0 HP within 5 tiles dies, regain 1 RC, never above maximum. Summoned, friendly, trivial or repeatedly revived creatures cannot trigger this recovery.","prerequisite":"Oracle 1; Mystery: Bones"}

oracle.supplement.bones.ledger-s-command — LC scout/control/servants
{"name":"Ledger's Command","activation":"Action","cost":"2 RC","rangeAndTarget":"Up to 2 undead within 4 tiles","duration":"2 rounds","frequency":"At will while RC remains","effect":"Each target makes a Wisdom save if hostile or unwilling; willing undead may waive it. On failure you command it for 2 rounds. Once per round as a Bonus Action, command one controlled undead to move up to its Speed and make one ordinary attack, using its own statistics; this obeys the universal one-extra-action limit and all controlled undead share that single Bonus Action command. Controlled undead reduce their first damage each round by 1. Once during the command, one controlled expendable undead may intercept a single-target attack against you and be reduced to 0 HP after absorbing it. This feature creates no corpse, loot or RC farm. Eligible targets are nonlegendary undead of challenge rating no greater than half your Oracle level (round down), with Wisdom saves initially and at each turn end. Commanding uses your shared companion Bonus Action; only one commanded undead makes one attack per round, capped at S d8+M damage with no monster multiattack, recharge or spell resources. Commanding a hostile undead to spend its Action consumes its one hard-denial allowance; later control can only deny Reactions and reduce Speed to 0 on a failed save, never command another Action.","prerequisite":"Oracle 6; Mystery: Bones; selected Tier II Revelation"}

oracle.supplement.bones.unfinished-chorus — MOD/PREV periodic/control/healing; not lifecycle-complete cards
{"name":"Unfinished Chorus","activation":"Action","cost":"3 RC","rangeAndTarget":"Enemies, controlled undead and corpses within 4 tiles","duration":"2 rounds; Revelation backlash 1 round","frequency":"At will while RC remains","effect":"For 2 rounds, enemies within 4 tiles suffer Dread: -1 on attack rolls and saving throws. Once on each of your turns choose one living enemy in range; it takes 1d6 necrotic damage and you either regain half the actual damage dealt, rounded down, or one living ally within 3 tiles of you regains that amount, maximum S+M HP. Undead you control add S damage to one attack each turn and reduce first damage each round by 1. Corpses in the area cannot be raised while the Chorus lasts. Afterward you are suffering Revelation backlash until end of your next turn: -1 attacks/saves and Speed -5 feet. Choose up to three enemies and three allies. Enemies make Wisdom saves on entry and at the end of each turn, ending their debuff on success. The drain allows a Constitution save for half damage; healing is capped at S+M total per pulse. Concentration and pulse upkeep apply.","prerequisite":"Oracle 9; Mystery: Bones"}

oracle.supplement.bones.bones-revelation-mastery — MOD/PREV periodic/control/healing; not lifecycle-complete cards
{"name":"Bones Revelation Mastery","activation":"Passive","cost":"0 RC","rangeAndTarget":"One eligible known Bones Revelation","duration":"Permanent","frequency":"Choose one upgrade at Oracle 15","effect":"Choose one mastery for a Revelation you know. Enhanced Marrow Drain: a living target hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Ledger's Command: may target up to 3 undead, but all controlled undead still share one Bonus Action command per round. Enhanced Unfinished Chorus: when its drain resolves, you may always redirect the healing to one ally within 3 tiles of you rather than yourself; its healing cap remains S+M.","prerequisite":"Oracle 15; Mystery: Bones; Revelation Mastery"}

oracle.supplement.bones.ledger-unbound — LC scout/control/servants
{"name":"Ledger Unbound","activation":"Action","cost":"0 RC","rangeAndTarget":"Enemies and up to 3 eligible corpses within 5 tiles","duration":"Damage instantaneous; bone servants 3 rounds","frequency":"1/long rest","effect":"Choose up to three enemies in range. Roll 4 S d8+M once; each target takes necrotic damage equal to the lesser of that roll or one-quarter its maximum HP, with a Constitution save for half. This blast cannot reduce HP below 1. Raise up to three nonsummoned corpses as 1-HP bone servants for three rounds. Once per round spend your shared companion Bonus Action to move and attack with ONE servant using your Revelation attack bonus for 1d8+S necrotic damage. Alternatively, your Reaction may sacrifice one servant to intercept a single-target attack against you; no attack is made by that servant that round. Servants grant no XP, loot, harvestable corpses or RC. For three rounds, up to three undead you already control add S damage to their one shared commanded attack and reduce the first damage they take each round by 1. No extra creature turns or command budgets are created.","prerequisite":"Oracle 20; Mystery: Bones"}

oracle.supplement.flame.flame-revelation-mastery — MOD/PREV periodic/control/healing; not lifecycle-complete cards
{"name":"Flame Revelation Mastery","activation":"Passive","cost":"0 RC","rangeAndTarget":"One eligible known Flame Revelation","duration":"Permanent","frequency":"Choose one upgrade at Oracle 15","effect":"Choose one mastery for a Revelation you know. Enhanced Wrathful Brand: its maximum duration becomes 2 rounds. Enhanced Crown's Burn: its healing may target up to three living allies within 4 tiles of the burst center rather than requiring them inside the burst. Enhanced First Flame Convergence: Zealot's Renewal backlash remains suppressed for the full Convergence duration; if already suppressed by the base effect, additionally one ally healed by Zealot's Renewal during Convergence gains S temporary HP.","prerequisite":"Oracle 15; Mystery: Flame; Revelation Mastery"}

oracle.supplement.life.overflowing-light — PREV death/direct-HP/healing
{"name":"Overflowing Light","activation":"Action","cost":"1 RC","rangeAndTarget":"One living ally within 4 tiles","duration":"Healing instantaneous; temporary HP 2 rounds","frequency":"At will while RC remains","effect":"The target regains 2d6+M HP. Healing exceeding its maximum becomes temporary HP, maximum 10, lasting 2 rounds. When those temporary HP expire naturally, if at least 1 remains the target may end one of Frightened, Poisoned or Staggered. This cannot resurrect, remove Wounds or convert deliberately wasted healing into more than 10 temporary HP.","prerequisite":"Oracle 3; Mystery: Life; selected Tier I Revelation"}

oracle.supplement.life.life-revelation-mastery — MOD/PREV periodic/control/healing; not lifecycle-complete cards
{"name":"Life Revelation Mastery","activation":"Passive","cost":"0 RC","rangeAndTarget":"One eligible known Life Revelation","duration":"Permanent","frequency":"Choose one upgrade at Oracle 15","effect":"Choose one mastery for a Revelation you know. Enhanced Overflowing Light: maximum temporary HP from excess healing becomes 20. Enhanced Garden of Restoration: the first Garden pulse a creature receives may end both Poisoned and one disease that explicitly allows magical curing, rather than only one of those benefits. Enhanced Song of Mending: duration becomes 3 rounds and gains one additional 2d6 healing pulse at the start of your second later regular turn; each ally still receives only one 1-HP death prevention per use.","prerequisite":"Oracle 15; Mystery: Life; Revelation Mastery"}

oracle.supplement.stars.clarity — MOD/PREV periodic/control/healing; not lifecycle-complete cards
{"name":"Clarity","activation":"Action","cost":"1 RC","rangeAndTarget":"One willing ally within 4 tiles; 2-tile reveal radius around target","duration":"Cleanse instantaneous; save bonus 2 rounds; reveal 1 round","frequency":"At will while RC remains","effect":"End one Charmed, Frightened or illusion-based condition on the target. For 2 rounds it gains +1 on saving throws. Until the end of your next regular turn, shapeshifted, invisible and ethereal creatures within 2 tiles of the target are revealed to it unless protected by an effect explicitly defeating supernatural revelation.","prerequisite":"Oracle 3; Mystery: Stars; selected Tier I Revelation"}

paladin.engine[5] — DEFER THP/full aura/control details
{"text":"At 17 Aura Surge once/short rest Bonus Action: until start next turn choose up to 3 allies in aura to gain S+M temporary HP and+1 saves. This bounded surge replaces vague doubling of every aura number. At 20 Divine Manifestation makes the aura active upon initiative without an action, radius 30 ft; it ignores ordinary Silence and terrain obstruction between allies but not antimagic explicitly suppressing divine powers, planar barriers or the consciousness rule. Source cannot-be-suppressed language is bounded explicitly. It grants no free Signature, Smite or Revelation spell."}

paladin.base.divine-strike — GUARD/MOD no companion proc / perception / resource-trigger
{"name":"Divine Strike","activation":"Triggered after melee hit","cost":"1 RP; upgraded option 2 RP from 2","rangeAndTarget":"One creature you hit","duration":"Instant","frequency":"Once/own turn","effect":"Use engine Divine Strike/Smite dice and later Oath modification. Declare after hit, then pay; normal critical dice rules. Not a spell and produces no Dissonance. Cannot trigger from reflected/copy/companion damage.","prerequisite":null}

paladin.base.bolstering-presence — DEFER THP/full aura/control details
{"name":"Bolstering Presence","activation":"Bonus Action","cost":"One short-rest use","rangeAndTarget":"Up to 3 allies 15 ft who can perceive you","duration":"Until start next turn","frequency":"1/short rest","effect":"Each gains+2 on its next save against Charmed or Frightened and M temporary HP. Use strongest save bonus from same class; does not end existing conditions automatically.","prerequisite":null}

paladin.hero.divine-sense — GUARD/MOD no companion proc / perception / resource-trigger
{"name":"Divine Sense","activation":"Passive upgrade","cost":"Normal Divine Sense use","rangeAndTarget":"Divine Sense targets 60 ft","duration":"Normal sense duration","frequency":"Automatic at 18","effect":"Divine Sense identifies celestial/fiend/undead nature despite ordinary disguise or shapeshift. Still requires clear line of effect; cannot reveal through walls or defeat artifact-specific concealment without its rule.","prerequisite":null}

paladin.supplement.oathbreaker-shared.dread-shelter — DEFER THP/full aura/control details
{"name":"Dread Shelter","activation":"Bonus Action","cost":"3 RP","rangeAndTarget":"Self","duration":"Concentration, 1 minute","frequency":"At will while RP remains","effect":"New rank 2 Forbidden spell. Gain 2 S+M temporary HP on casting and 1 flat DR against weapon damage for duration. No recurring temp HP pulse or healing.","prerequisite":"Paladin 5; selected Oathbreaker inversion"}

paladin.supplement.oathbreaker-shared.black-manifestation — DEFER THP/full aura/control details
{"name":"Black Manifestation","activation":"Bonus Action","cost":"1 long-rest use","rangeAndTarget":"Self and up to 3 enemies in aura","duration":"Until start next turn","frequency":"1/long rest","effect":"New Oathbreaker Final: gain 2 S+M temporary HP; chosen enemies WIS save or lose Reactions and Speed-10 ft for duration. Refresh one expended Signature use, then pay its normal Action and other costs when used. No Death Touch pool, RP, extra Action or Final reset.","prerequisite":"Paladin 20; selected Oathbreaker inversion"}

paladin.supplement.oath-of-mercy.channel-life — PREV healing/redirection/death
{"name":"Channel Life","activation":"Action","cost":"5 RP","rangeAndTarget":"Self and one living ally within 30 feet","duration":"Instantaneous","frequency":"At will while RP remains","effect":"Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.","prerequisite":"Paladin 9; Oath of Mercy"}

paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression — PREV healing/redirection/death
{"name":"Healing Suppression","activation":"Passive","cost":"0","rangeAndTarget":"Up to 3 chosen creatures in your Oath aura","duration":"While conscious and target remains in aura","frequency":"Choose targets at start of each turn","effect":"HP healing received by each selected creature is halved, rounded down. Temporary HP, damage prevention and resurrection are not healing for this effect. This suppression cannot reduce healing below 0 or convert prevented healing into damage.","prerequisite":"Paladin 3; Oathbreaker — Oath of Mercy"}

paladin.supplement.oath-of-vengeance.verdict-absolute — GUARD/MOD no companion proc / perception / resource-trigger
{"name":"Verdict Absolute","activation":"Bonus Action","cost":"0 RP","rangeAndTarget":"One Judgment Brand target; witnesses in your aura","duration":"3 rounds","frequency":"1/long rest","effect":"For 3 rounds, your current Judgment Brand cannot be removed by an ordinary save or concealment effect. Smites against the branded target use maximum Smite dice, and it cannot voluntarily teleport or become invisible. If the branded target reaches 0 HP during the effect, restore your Lay on Hands pool to its normal maximum once, then up to three hostile creatures in your aura that witnessed the defeat make Wisdom saves; on failure they are Frightened until the end of their next turn. The Lay on Hands refill requires a meaningful nonsummoned hostile defeated in a real encounter; staged or willing sacrifices do not qualify.","prerequisite":"Paladin 20; Oath of Vengeance"}

paladin.supplement.oath-of-the-ancients.primordial-surge — DEFER THP/full aura/control details
{"name":"Primordial Surge","activation":"Action","cost":"10 RP","rangeAndTarget":"Up to 3 chosen creatures in your Oath aura","duration":"Temporary HP until lost; root until end of target's next turn","frequency":"At will while RP remains","effect":"A selected ally gains temporary HP equal to 2 times your actual Charisma modifier, minimum 2. A selected hostile fey or elemental makes a Strength save; on failure roots bind it and its Speed becomes 0 until the end of its next turn. This root does not remove Actions or Reactions. You may mix allied and hostile targets but can select no more than 3 total creatures.","prerequisite":"Paladin 17; Oath of the Ancients"}

paladin.supplement.oath-of-the-chain.linked-ward — PREV healing/redirection/death
{"name":"Linked Ward","activation":"Action","cost":"2 RP","rangeAndTarget":"One willing ally in your Oath aura","duration":"Concentration, maximum 3 rounds","frequency":"At will while RP remains","effect":"Mark one willing ally. Once per round when it takes damage, use your Reaction to redirect up to 2 times your actual Charisma modifier, minimum 2, of that damage to yourself. Redirected damage keeps its type and cannot be redirected again. If this redirected damage reduces you to 0 HP, the ally gains temporary HP equal to the amount you actually absorbed, maximum Paladin level+M.","prerequisite":"Paladin 3; Oath of the Chain"}

paladin.supplement.oath-of-the-chain.final-stand — PREV healing/redirection/death
{"name":"Final Stand","activation":"Action","cost":"10 RP","rangeAndTarget":"One willing ally in your Oath aura","duration":"Until start of your next regular turn","frequency":"At will while RP remains","effect":"Until the start of your next turn, all damage that would be dealt to the chosen ally is redirected to you instead. The redirected damage retains type, cannot be redirected again and cannot be mitigated again after the original target’s defenses apply once. If redirected damage reduces you to 0 HP, the ally immediately gains temporary HP equal to your Paladin level and resistance to all damage until the end of its next turn. This effect ends if you die outright.","prerequisite":"Paladin 17; Oath of the Chain"}

paladin.supplement.oath-of-the-chain.unbroken-covenant — PREV healing/redirection/death
{"name":"Unbroken Covenant","activation":"Bonus Action","cost":"0 RP","rangeAndTarget":"Your full Oath aura; up to 3 bonded allies","duration":"3 rounds","frequency":"1/long rest","effect":"For 3 rounds Warden's Lock fills your entire current Oath aura. Choose up to 3 allies there as bonded. Each bonded ally uses your AC if it is higher and cannot be forcibly moved against its will. Whenever you redirect damage from a bonded ally to yourself, that ally gains temporary HP equal to half the actual damage you absorb, rounded down, maximum S+M per event. Temporary HP do not stack. This Final grants no extra Reactions.","prerequisite":"Paladin 20; Oath of the Chain"}

paladin.supplement.oath-of-grief.echo-of-the-fallen — LC source-native spirit manifestation, explicitly not resurrection
{"name":"Echo of the Fallen","activation":"Action","cost":"10 RP","rangeAndTarget":"One allied creature who died in your aura this encounter; one target within the former ally's normal weapon range or one ally in your aura","duration":"Until start of your next regular turn","frequency":"At most once per fallen ally per long rest","effect":"Manifest the ally's spirit for one round. Choose one mode on cast. Strike: the spirit makes one attack using the deceased ally's last recorded ordinary weapon attack bonus and base weapon damage, with no class-resource riders, extra attacks or proc effects. Guard: one chosen ally in your aura gains +2 AC until the start of your next turn. The spirit is not resurrected, cannot be targeted and disappears afterward. The single spirit strike uses PB+CHA to hit and S d8+M damage of the original weapon type if the recorded profile would exceed either value. It consumes the shared damaging-companion-action budget for that round; no monster or high-level player stat-block duplication.","prerequisite":"Paladin 17; Oath of Grief"}

paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin — PREV healing/redirection/death
{"name":"Dirge of Ruin","activation":"Action","cost":"2 RP","rangeAndTarget":"Up to 3 creatures in your Oath aura","duration":"Damage instantaneous; healing block until end of next turn","frequency":"1/short rest; replaces Signature Power use","effect":"Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. A failing target cannot regain HP until the end of its next turn. This does not prevent temporary HP or remove healing already received.","prerequisite":"Paladin 11; Oathbreaker — Oath of Grief"}

paladin.supplement.oath-of-the-martyr-king.king-s-smite — PREV healing/redirection/death
{"name":"King's Smite","activation":"Triggered","cost":"Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8","rangeAndTarget":"Creature hit by your melee weapon attack; one ally in your aura","duration":"Smite instantaneous; temporary HP until lost; redirection passive while this Oath is active","frequency":"One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance","effect":"The Smite deals radiant damage normally. After it resolves, choose one ally in your aura; it gains temporary HP equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Separately, once per round when an ally in your aura takes damage, you may redirect up to 5 of that damage to yourself. Apply the original target’s defenses once, then transfer up to 5 of the remaining damage. Transferred damage keeps its type and cannot be reduced again, reflected, redirected again or generate resources.","prerequisite":"Paladin 3; Oath of the Martyr King"}

paladin.supplement.oath-of-the-martyr-king.noble-bearing — DEFER THP/full aura/control details
{"name":"Noble Bearing","activation":"Action","cost":"2 RP","rangeAndTarget":"Up to three allies in your aura","duration":"Concentration; three rounds","frequency":"While RP remains","effect":"Selected allies gain +1 on morale checks and saves against Frightened. Once on each of your turns after a paid Smite deals radiant damage, one selected ally gains temporary HP equal to half the actual Smite damage, rounded down, capped at S+M. This replaces, rather than stacks with, the identical King’s Smite temporary HP. Temporary HP never stack.","prerequisite":"Paladin 3; Oath of the Martyr King"}

paladin.supplement.oath-of-the-martyr-king.last-king-s-gift — PREV healing/redirection/death
{"name":"Last King’s Gift","activation":"Reaction before ally falls to 0 HP","cost":"10 RP","rangeAndTarget":"One living ally in your aura","duration":"Instant prevention; temporary HP until lost or encounter end","frequency":"Once per encounter per ally","effect":"When damage would reduce the ally to 0 HP without killing it outright, it instead remains at 1 HP and gains temporary HP equal to your Paladin level after the triggering damage resolves. This does not reverse a completed death, remove Wounds or replenish any resource.","prerequisite":"Paladin 17; Oath of the Martyr King"}

paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura — PREV healing/redirection/death
{"name":"Crownshatter Decree Aura","activation":"Passive","cost":"0","rangeAndTarget":"Up to three selected enemies in your aura","duration":"While conscious and in aura","frequency":"Each incoming healing event","effect":"A selected enemy receives HP healing only if it has taken actual damage from a meaningful hostile creature since the start of its previous regular turn. If it has not, that healing restores 0 HP; its source still spends its normal costs. Temporary HP, stabilization and resurrection are not HP healing for this restriction. This aura never creates damage, transfers healing or reverses recovery that already resolved.","prerequisite":"Paladin 3; Oathbreaker — Oath of the Martyr King"}

soldier.engine[2] — OBJ/LC structures and finite turrets
{"text":"At 5 automatically gain Palisade Deployment. Spend one carried barricade kit and an Action to erect a 2-by 1-tile wall in contiguous unoccupied ground within 5 ft. Height 5 ft, AC 12, HP 5+CON modifier minimum 1, immunity psychic/poison; blocks movement and line of sight across its full height but can be climbed using 10 ft movement. One kit/use per encounter, two at 13; a long rest with carpentry tools replenishes 2 kits (carried maximum 2, reusable parts have no resale value). Material is required; no conjuring. At most one intact wall, two at 13. Old wall must be dismantled in 1 minute before replacement beyond cap. Once per encounter an Action repairs a wall for M HP using spare parts; destruction does not refresh uses."}

soldier.base.quick-deploy — OBJ/LC structures and finite turrets
{"name":"Quick Deploy","activation":"Action","cost":"1 encounter use","rangeAndTarget":"One 5 ft square within 5 ft","duration":"3 rounds or destroyed","frequency":"1/encounter","effect":"Place low cover from carried field supplies: AC 12, HP 5, grants half cover and is difficult terrain. It is not a full palisade and does not grant its bonuses. One at a time; no transferable saleable material.","prerequisite":null}

soldier.base.rally-point — DEFER/GUARD THP/resource refresh
{"name":"Rally Point","activation":"Bonus Action","cost":"1 short-rest use","rangeAndTarget":"Up to 3 allies within 15 ft who hear you","duration":"Until start next turn","frequency":"1/short rest","effect":"Each gains M temporary HP and+1 on the next saving throw before duration ends. Temporary HP follows strongest-only rule and is lost at encounter end.","prerequisite":null}

soldier.arch.palisade-deployment — OBJ/LC structures and finite turrets
{"name":"Palisade Deployment","activation":"Action","cost":"One kit; one encounter deployment","rangeAndTarget":"Adjacent 10-by 5 ft ground","duration":"Until destroyed/dismantled","frequency":"1/encounter; 2 at 13","effect":"Automatic engine, not a selected skill. Build the palisade with the exact statistics, kit and repair rules in the class engine. Source minimum 5 retained.","prerequisite":null}

soldier.hero.champion.rallying-cry — DEFER/GUARD THP/resource refresh
{"name":"Rallying Cry","activation":"Bonus Action","cost":"1 long-rest use","rangeAndTarget":"Up to 3 allies within 30 ft who hear you","duration":"Instant; temp HP to encounter end","frequency":"1/long rest","effect":"End Frightened on each and grant S+M temporary HP. Cannot revive, heal real HP or repeatedly refresh from imitation/copies.","prerequisite":null}

soldier.hero.artillerist.palisade-synergy — MOD actual Palisade modifiers
{"name":"Palisade Synergy","activation":"Passive","cost":"0","rangeAndTarget":"Your ranged weapon attack while adjacent to palisade","duration":"One hit","frequency":"Once/own turn","effect":"Add S damage. Does not apply to every shot, area save or turret hit, and requires an intact wall you deployed.","prerequisite":null}

soldier.hero.artillerist.turret-deployment — OBJ/LC structures and finite turrets
{"name":"Turret Deployment","activation":"Action","cost":"1 short-rest use","rangeAndTarget":"Up to 2 empty squares within 10 ft","duration":"3 rounds","frequency":"1/short rest","effect":"Deploy 2 turrets, each AC 12+PB and HP 2 L, immobile, range 60 ft. On your Bonus Action command ONE turret to attack using PB+DEX for 1d6+M piercing. Both share that single command/attack budget with other companions; no autonomous shots. Reclaimed after use, no resale.","prerequisite":null}

soldier.hero.artillerist.bubble-of-discipline — ZONE/effect, not HP objects
{"name":"Bubble of Discipline","activation":"Action","cost":"1 long-rest use","rangeAndTarget":"15 ft square centered within 15 ft","duration":"Until start of your second next turn","frequency":"1/long rest","effect":"Deploy dense layered cover. Up to 3 allies inside gain+2 AC against spell attacks and advantage on DEX saves against spells from outside. Once total, Reaction reduce spell damage to one protected ally by 2 S+M. Does not negate a spell, block internal casting or protect each ally independently.","prerequisite":null}

soldier.supplement.final-command — DEFER/GUARD THP/resource refresh
{"name":"Final Command","activation":"Bonus Action","cost":"1 long-rest use","rangeAndTarget":"Self and up to 3 willing allies within 30 ft who hear you","duration":"Until start next turn","frequency":"1/long rest","effect":"New Hero capstone. Allies may each move 10 ft without opportunity attacks and gain S+M temporary HP. You refresh one expended short-rest Soldier card, excluding Final Command and long-rest features. A refreshed card still costs its activation and ammunition; no extra turn or recursive resets.","prerequisite":"See class engine and progression."}

thief.engine[0] — GUARD/check; no lifecycle creation rights
{"text":"Dexterity governs weapons and class DC/M. Choose Intelligence or Wisdom for noncombat class tool/sense checks at 1. Hit Die d8; light armor, daggers, shortswords, thrown weapons and hand crossbows; thieves tools and poison kit. Sneak Attack is automatic at 1: once on your regular turn, add ceil(class level/2)d6 to one finesse/ranged weapon hit if you had advantage, an active ally threatens target within 5 ft, or target is suffering your Bleed/Poisoned/Crippled. Disadvantage prevents Sneak Attack even if canceled into a straight roll. A feature can explicitly grant Sneak Attack on a different qualifying hit but never more than once/regular turn. Copies, poison ticks and companions cannot Sneak Attack."}

thief.base.disable-device — GUARD/check; no lifecycle creation rights
{"name":"Disable Device","activation":"Action","cost":"Thieves tools","rangeAndTarget":"One accessible device within reach","duration":"One attempt","frequency":"At will; retries need changed approach","effect":"Make DEX+PB against its stated disarm DC; unknown DC defaults 15 for ordinary trap, 20 complex. Success disarms one accessible mechanism, failure by 5 triggers it. Does not automatically dispel magic.","prerequisite":null}

thief.hero.arcane-trickster.arcane-theft — GUARD/check; no lifecycle creation rights
{"name":"Arcane Theft","activation":"Action","cost":"3 RP","rangeAndTarget":"One enemy within 30 ft with observed spell buff","duration":"Concentration, at most 3 rounds","frequency":"1/short rest","effect":"Target WIS save. Failure suppress one eligible temporary rank 1–3 buff for duration and gain only its printed AC bonus (max 2), Speed bonus(max 10 ft), or resistance to one damage type; choose before save. Does not copy actions, spells, resources, summons or capstones. Magical technique 1 D.","prerequisite":null}

warrior.engine[10] — GUARD/PREV resource/healing/redirection/DR
{"text":"BT CAP AND RESET. Default BT cap is 3. Stack Overflow raises it to 4. BT is not automatically spent; only features explicitly saying spend reduce it. Encounter end resets BT and Brutality Progress to 0. BT cannot be generated from friendly attacks, summoned sacrificial creatures, unattended objects, staged sparring or enemies that do not meaningfully threaten the party."}

warrior.engine[15] — GUARD/PREV resource/healing/redirection/DR
{"text":"HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT."}

warrior.base.mutation-surge — DEFER incidental THP
{"name":"Mutation Surge","activation":"Bonus Action","cost":"+1 Strain","rangeAndTarget":"One active mutation","duration":"Until start of your next regular turn","frequency":"Recharge 2 rounds","effect":"Mutation Surge. Enhance one active mutation. If it grants AC, DR, attack, save or flat damage, increase one such bonus by 1; if it grants movement or reach, increase it by 5 feet; if it deals mutation damage, add 1d4 to one damage event. A mutation with none of those numeric effects instead grants S temporary HP. The enhancement never changes immunity, target count or duration.","prerequisite":null}

warrior.arch.brutality-momentum — GUARD/PREV resource/healing/redirection/DR
{"name":"Brutality Momentum","activation":"Triggered","cost":"0","rangeAndTarget":"Your Brutal Strike","duration":"Instantaneous","frequency":"At most once per round","effect":"Brutality Momentum. When you personally reduce a creature marked Vulnerable by Brutality Sense to 0 HP with a melee attack, set Brutal Strike's positive round-recharge counter to 0 if it has not already been reset or shortened this round. This restores no Action and cannot refresh a per-rest use. Trivial, summoned or friendly creatures cannot trigger it.","prerequisite":null}

warrior.hero.wardborn.aegis-incarnate — GUARD/PREV resource/healing/redirection/DR
{"name":"Aegis Incarnate","activation":"Bonus Action","cost":"0","rangeAndTarget":"Self and allies within 15 feet","duration":"3 rounds","frequency":"1/long rest; automatic Wardborn Final Form","effect":"Final Form – Aegis Incarnate. For 3 rounds you cannot be forcibly moved or knocked Prone. Whenever an ally within 15 feet takes damage, automatically redirect half that damage rounded down to yourself after the ally's resistance but before its temporary HP; the ally takes the remainder. Redirected damage keeps its type, cannot be reduced again or generate BT, and cannot be redirected again. If taking the redirected damage would kill you outright, the redirection still occurs. This grants no extra Reaction requirement and does not stack with Guardian Tissue on the same damage event.","prerequisite":null}

warrior.supplement.bone-hardened — GUARD/PREV resource/healing/redirection/DR
{"name":"Bone Hardened","activation":"Passive","cost":"0","rangeAndTarget":"Self","duration":"Permanent","frequency":"Automatic","effect":"While you are not Staggered, reduce physical weapon damage you take by 1 after resistance and before temporary HP.","prerequisite":"Warrior 6"}

warrior.supplement.hemophage-core — GUARD/PREV resource/healing/redirection/DR
{"name":"Hemophage Core","activation":"Triggered while active","cost":"One mutation slot; serum activation","rangeAndTarget":"Self","duration":"Instantaneous","frequency":"Once per turn","effect":"When you personally reduce a meaningful hostile creature to 0 HP with a melee attack, regain 2d6 HP. Summoned, trivial, friendly or repeatedly revived creatures cannot trigger this healing. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.","prerequisite":"Dreadspawn; Aberrant Mutation Tree; Warrior 10"}

cleric.engine[10] — GUARD resource/corpse/agency/acquisition
{"text":"All acquisition gates use Cleric class level, not total character level. Proficiency bonus still follows normal total-character-level rules. A multiclass character cannot use non-Cleric levels to unlock Bishop, Hero, Invocation or Finale features. Divine commands, visions and social abilities can influence actions only to the extent their exact mechanical text states; no Cleric feature can force a player character to adopt, abandon or profess a belief."}

oracle.engine[19] — GUARD resources/agency/copy/redirection
{"text":"PROPHECY AND DIVINATION never force player beliefs, future choices or confessions. Information features can provide truthful clues, likely outcomes, symbolic visions or current facts, but the Director is not required to reveal unknowable future player decisions. Effects that command or compel a player-controlled character preserve the player's choice of targets and prohibit self-harm, permanent allegiance changes and belief alteration."}

oracle.engine[29] — GUARD resources/agency/copy/redirection
{"text":"Extra attacks and echoed damage use base weapon/spell dice before critical-hit extra dice. A redirected damage event cannot be reduced a second time, reflected again or generate RC. Charmed alone does not grant command of a creature's actions."}

soldier.engine[3] — MOD actual Palisade modifiers
{"text":"Palisade Tier II at 13 doubles wall HP and grants resistance to damage from area effects. Hold Position: while adjacent to your intact wall gain+1 AC and+1 saves. Brace Line: an ally immediately behind you relative to a ranged attacker, with your wall adjacent to both of you, has 2 flat DR against that attacker. These bonuses do not stack with another Soldier wall; strongest flat DR applies. Full cover prevents attacks rather than granting an additional AC bonus."}

soldier.arch.fortify-zone — ZONE/effect, not HP objects
{"name":"Fortify Zone","activation":"Action","cost":"1 short-rest use","rangeAndTarget":"Visible 15 ft square within 30 ft","duration":"3 rounds","frequency":"1/short rest","effect":"Designate fortified firing lanes. Ranged attacks against up to 3 allies inside take-2 to hit while you remain conscious within 30 ft. Does not affect saves, melee attacks or attacks from inside zone.","prerequisite":null}

soldier.hero.champion.wall-of-aegis — ZONE/effect, not HP objects
{"name":"Wall of Aegis","activation":"Bonus Action","cost":"1 short-rest use","rangeAndTarget":"Self and up to 3 adjacent allies","duration":"Until start of your second next turn","frequency":"1/short rest","effect":"Gain 2 flat DR against all damage except psychic. Use strongest reduction once per damage packet; does not stack with other flat DR.","prerequisite":null}

## Exact frozen supporting paragraphs
{"scope": "Two additional frozen targeting/hard-denial paragraphs; original three supports remain in the100-source inventory.", "supportingSources": [{"sourcePath": "docs/mechanics/CLASS_PLAYTEST_RULES.md", "paragraphPrefix": "Unless expressly stated,", "text": "Unless expressly stated, perceive the target, remain within range and have line of effect; total cover blocks targeting. “Ally” includes self unless it says OTHER. A list cannot contain a creature twice. Select up to the printed limit; an empty target list is not a valid way to farm activation benefits. Zones remain at their chosen point unless described as an aura; allies can leave and lose their benefits. An aura requires its owner conscious unless the card supplies a bounded exception. An effect ending at “end next turn” means the affected creature's next turn only when the card says target's; otherwise the user's.", "fullFileSha256": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81"}, {"sourcePath": "docs/mechanics/CLASS_PLAYTEST_RULES.md", "paragraphPrefix": "No repeated hard denial", "text": "No repeated hard denial without a new save and cost. For this class suite, a creature can suffer **Stunned, compelled loss of its whole Action/turn, or equivalent hard denial from a given character at most once per encounter**, across that character's class features; later such riders fail while damage and soft riders resolve normally. Record source and target. This draft guard is broader than the older Oracle-only ceiling and is an explicit balance proposal. Reaction denial, Speed reduction, penalties and Frightened do not count as whole-turn loss. Do not silently waive boss immunities, legendary defenses or anatomy.", "fullFileSha256": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81"}]}

## docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md
SHA256 82d6be0bb9d161903ed5c3c0d05ce58d53a3c12314e4f31e1e2388f6601a2a90
```
# Remaining companion and structure lifecycles

**IMPLEMENTED CANDIDATE — GPT implementation review pending.** The selected interfaces pass 124 targeted checks. This guide implements decisions from the source conference, boundary reconciliation and final profile discussion. It does not replace original cards or promote all 80 passages to complete abilities.

The [source register](REMAINING_LIFECYCLE_SOURCE_BINDINGS.md) preserves all 80 exact class passages, their hashes, individual roles and open work. Five frozen shared paragraphs support the targeting, command and hard-denial rules. [Source validation](REMAINING_LIFECYCLE_SOURCE_VALIDATION.json) and [transaction validation](REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json) are separate evidence. The earlier [creature](CREATURE_LIFECYCLE_PLAYTEST.md) and [device](DEVICE_LIFECYCLE_PLAYTEST.md) packages remain applicable only to their specified sources.

## Shared operation

One owner has one numbered-round companion Bonus Action command allowance and one offensive companion allowance across classes. The ordinary commands below require the owner's **original regular turn** and resolve once in its attached companion phase. This scheduling is **NEW integration** where a card says only once per round. Extra turns do not supply another ordinary issuance window or refresh commands, target extra Actions, regular markers, duration or recharge. Costs and current-round allowances commit on issuance; inability to execute later provides no refund. A future forced native Action instead reserves the resolution round's offense and releases that reservation if cancelled, retaining its already spent issuance Bonus Action.

Keep original source owner, current controller and creature identity separate. Current source-class attack statistics belong to the original source owner. Control does not substitute the controller's statistics or manufacture another body or independent turn. Use the same physical-body registry, owner command ledger, action/resource wallet, encounter hard-denial set and target extra-Action clock across all sources. A real rest/encounter/recharge transition supplies a canonical scope; choosing a different key in code never authorizes another use.

Created finite creatures and turrets use the HP-only layer: apply legal defenses and existing temporary HP, then ordinary HP; at 0 they end. They gain no player Wounds, Stable state, death saves, XP, loot, corpse, resurrection target or resource-farming rights. No repair, resurrection or autonomous damaging turn follows from the word companion. Soldier structures have their own states below. The existing body registry also records known created-object identities, so later relabeling cannot turn a wall into corpse fuel.

The reference helper is a bounded transaction model. The caller supplies source access, target and placement legality, player agency, active control, native capability, actual dice results, defenses, class-resource side effects, exact virtual deadlines and canonical recharge scopes. These assertions are mandatory inputs, not permissions created by the helper. Ordinary attacks, complete condition/rider execution, native-monster damage and the live scheduler are not implemented here. Use `RemainingWorld.damage/expire/end_choir` for these selected bodies; routing Choir through the generic finite-creature cleanup would omit its source-specific bursts.

## Cleric: Rite of the Crimson Choir

Spend an Action, 5 Conviction and 8 RP, once per long rest, to place four fanatics in legal unoccupied spaces within 30 feet. Concentrate for at most three rounds. Each has AC14, HP10, Speed30 and no Reactions. Conviction expenditure can vent Dissonance once under the established class rule; the helper does not invent a second vent.

The Finale explicitly permits one regular-turn Bonus Action/offensive command to authorize up to four surviving fanatics. Each can move up to its Speed and independently make one melee attack at reach5 using the current Cleric technique attack bonus, dealing 1d6+S necrotic on a hit. This is one shared command with up to four actual attack rolls.

A legal hit also heals the Cleric exactly 1 HP, at most 4 HP per numbered round, within maximum HP and all applicable healing restrictions. **The hit predicate is literal:** fully resisted or immune damage does not by itself cancel this 1 HP. A miss gives none. The earlier healing classification must not be read as `min(actualDamage,1)`. The caller applies ordinary healing eligibility, Critical limits and explicit healing-generation prohibitions; this is not resurrection or Wound removal. A hit result is settled once, and a cancelled attack cannot claim it.

**NEW event identity:** every fanatic has one explosion opportunity. It explodes when it reaches 0, when concentration actually ends, or at the third-round deadline. Each burst affects legal enemies within5, DEX save, 1d6 necrotic on failure/half on success. All four bursts can affect the same enemy when geometry permits; there is no invented shared per-target burst cap.

If an applicable `noDeathTriggers`, `noRetaliation` or `noDamageTriggers` restriction suppresses the zero-triggered burst, permanently settle that fanatic's opportunity and end it. It cannot wait for expiry to explode again. At a true source-wide ending, snapshot all surviving fanatics and their positions, prepare bursts in stable creation order, then remove them as that ending resolves. A prior zero-ended fanatic is absent. Mere suppression of output while concentration remains active is not concentration ending. No individual voluntary dismissal is granted.

Bursts are source-native damage, not another command; they produce no Choir healing, corpse, XP, loot, Conviction or recursive death/retaliation/resource/copy chain. Already snapshotted source-wide bursts still resolve independently. There is no repair or return of ended fanatics.

## Cleric: Ritual of Undeath

One Action, 3 Conviction, 6 RP and one long-rest use choose **Corpse Servant or Death Ward**. They are not both granted. Death Ward retains its already reviewed would-die replacement: one living ally within30, one minute, first actual would-die event leaves1 HP and the specified temporary creature typing; no Wound removal.

For Corpse Servant, choose a real available humanoid corpse within30 that died no more than60 seconds ago. **NEW body integration:** successful creation consumes the physical corpse into the servant; it is unavailable for other corpse targeting, anchors and resurrection. Ending the servant never recreates that body as available corpse fuel.

The thrall lasts three rounds, AC13, HP10, Speed30, finite HP-only. One shared regular-turn Bonus Action/offensive command permits one Cleric technique attack dealing S d6 necrotic. **NEW missing-profile completion confirmed by GPT:** melee, reach5 only. No ranged mode, multiattack or imported undead abilities. It disappears at0 or expiry without XP, loot, new corpse, Conviction or resurrection target.

## Oracle: Ledger's Command

Spend an Action and2 RC to target one or two eligible undead within4 tiles (20 feet); Bones mastery may raise that target maximum to3. Each must be nonlegendary with CR no greater than floor(Oracle level/2). Resolve initial and actual regular-end Wisdom saves; willing undead may waive each required save. A failed/waived initial save establishes control for at most two rounds. A successful initial save still spends the cast resources. Preserve native HP, AC, original stat provenance, body and initiative.

**Willing order:** a regular-turn Bonus Action commits the Oracle's shared command/offense and that target's canonical one-extra-full-Action allowance for the same numbered round. This allowance is shared with every other extra-Action source and cannot recurse. In the attached phase, recheck control, consent, capability and target legality. Resolve one consensual extra move/ordinary attack. The original creature retains its normal regular Action; a created standard companion still gains no autonomous damaging turn. Withdrawn willingness cancels without a forced substitute, hard denial or any refund.

**Hostile/unwilling order:** after the failed save, issue one future order replacing the target's next real regular Action. Spend issuance-round Bonus Action and reserve the offense in the actual resolution round. Do not grant an attached extra attack. Revalidate control, capability, legality and the canonical (encounter, Oracle, target) hard-denial allowance. Spend that hard denial only if the native Action is actually replaced. Cancellation releases unused future offense, retaining the spent Bonus Action. At most one pending order for a target exists in an application; all applications also share the canonical budgets.

After that Oracle-to-target hard-denial allowance is spent, later failed regular-end saves can only deny Reactions and set Speed0 until the next original regular end or earlier Ledger ending. No repeated forced attack, Dodge or movement is allowed. A successful save ends control and pending orders. Extra/replayed markers do not tick this process. Ended control cannot retain the soft effect. The caller must cancel/revalidate pending orders promptly when source/control/legality changes, including expiry.

Each ordinary commanded attack uses the native permitted attack bonus, damage type and reach/range, without multiattack, recharge/spell/resource powers or extra riders. **NEW deterministic damage cap:** compare its maximum possible noncritical ordinary damage (dice maxima plus flat modifier) to `8 × S + M`. Keep a profile at or below that maximum; otherwise substitute S d8+M for its damage formula only. Then use ordinary attack/critical rules. Do not roll a second competing cap packet or clamp actual rolled damage.

Controlled undead offer flat DR1 on their first qualifying positive incoming damage event each numbered round, at the ordinary flat-reduction stage. An active qualifying source consumes its opportunity even if an equal or stronger DR wins strongest-only arbitration. Two DR1 sources do not add to2. Losing/regaining control does not reset an already used opportunity. A source inactive at an earlier event may use its first eligible event after becoming active.

**NEW source-native interception:** once per entire application, after a successful single-target attack against the Oracle hits but before damage/on-hit consequences, choose an active controlled expendable undead. No Reaction cost is added. No ongoing distance tether is invented from the acquisition range. Resolve the common interception transaction below. Ledger has no per-creature attack-versus-interception round exclusion; do not import the Unbound restriction.

## Oracle: Ledger Unbound

The Action costs0 RC and uses its once-per-long-rest entitlement. Its enemy blast retains the already reviewed shared-roll, maximum-HP comparison and minimum1-HP floor: up to3 enemies within5 tiles, roll4 S d8+M once, cap each target at one-quarter maximum HP, CON half, never reduce below1. This lifecycle helper does not roll or replay that damage.

Raise up to3 selected real nonsummoned available corpse bodies in range as bone servants. Each distinct body is consumed and never reappears when its servant ends. Each servant has HP1, AC12+floor(PB/2), Speed30 and owner-PB saves; duration three rounds. These defensive creation statistics are the standard bounded chassis. Attacks use current original Oracle Revelation bonus for1d8+S necrotic. **NEW gap-fill:** melee reach5 only, no ranged mode or imported monster profile.

One shared regular-turn Bonus Action/offensive command allows only one servant to move/attack. At issuance, reserve that servant's numbered-round local mode as `ATTACK_RESERVED`; cancelled execution does not refund it. A servant without a reserved attack may instead be sacrificed using the Oracle's actual Reaction to intercept a qualifying incoming attack. Its local mode becomes `SACRIFICED`. The same servant cannot attack and sacrifice in one numbered round, but servantA can attack while servantB is sacrificed. Sacrifice has no additional offensive-companion debit. The original Oracle must still control its own servant. No XP, loot, harvestable corpse or RC is created.

**NEW buff membership:** snapshot up to3 undead already controlled before the new servants are created. Only those identities can benefit for the original three-round duration. While each is actually controlled, it adds currentS to the one shared commanded attack and offers first-damage DR1 as above. Lost control suspends; regained control restores the same identity during the original duration, without replacing recipients or resetting used reduction. New servants are excluded. The helper's attack-bonus query is a profile eligibility calculation: the caller certifies the one qualifying commanded attack and applies existing shared command/rider limits, never every hit or arbitrary attack.

### Common Oracle interception transaction

Use one real incoming attack ID and a canonical window shared by both variants. It must be an actual successful single-target attack **against this Oracle**, after the hit and before consequences. The first committed interception closes that attack's window. No second attack roll, damage transfer branch or replay occurs. The Oracle receives no damage or on-hit consequences from it. The interceptor receives the source's zero-HP assignment/sacrifice, which is not damage, Wound-producing damage, retaliation or resource generation. Then resolve its native legal0-HP lifecycle.

For existing native creatures, the helper returns the zero-assignment instruction to the caller; it does not rewrite arbitrary monster/PC state. The caller must certify control, source expendability, agency and native prevention rights, then apply that native lifecycle once. This cannot silently sacrifice a PC or bypass a legal death replacement. A preexisting ordinary body retains whatever same-body remains its native lifecycle allows. No new or duplicate corpse entitlement follows. Created Unbound servants simply end and supply no body fuel.

## Oracle: Haunted Boon V

Action,0 cost, once per long rest. This manifestation has no invented HP, AC, combat targetability, attack or companion command. It has ordinary sight/hearing and can follow only a personally traveled same-plane route within one mile, without crossing sealed planar barriers. Speaking requires willing dead spirits encountered. It cannot read minds or supply unknowable facts, remote real-time senses or the Oracle's senses.

**NEW task integration:** choose one mode: scout/observe, one assigned inquiry of willing dead spirits, or deliver one prophetic message. The one task includes outbound travel, its performance, attempted return and printed report. It ends after that return/report or ten minutes, whichever first. A delivered message remains delivered even if the scout expires during return. No remote report or telepathic final upload occurs if it expires before returning. The returned account/name must derive from actual observations/encounters. No numerical Speed exists in the supplied source; the Director/caller certifies a real timed route within the deadline. General travel timing remains later work.

## Paladin: Echo of the Fallen

Record an actual allied death inside this Paladin's aura during the current encounter. A finite summon merely disappearing does not qualify. No corpse is required, and “who died” does not impose a new requirement that the ally remain dead. Track use by **Paladin + ally identity + actual long-rest epoch**, preventing repeated deaths from making extra uses.

Spend an Action and10 RP and immediately resolve one mode, including on a genuine extra own turn if the Action and source budgets exist. The spirit is untargetable with no HP, AC, native turn, Bonus Action command, corpse or follow-on action. It is not resurrection.

**Strike:** require an actual recorded ordinary weapon attack bonus, base damage formula, type and normal range. Without a recorded weapon profile, Strike is unavailable. Attack bonus is the lesser of that recorded bonus and current PB+actual CHA. **NEW deterministic cap:** compare maximum noncritical ordinary base damage to8×S+M; use S d8+M if the recorded profile exceeds it, otherwise retain that profile. Preserve original damage type/range and apply ordinary critical rules after selecting the profile. No Smite, Sneak Attack, resource riders, procs, extra attacks or stat-block duplication. Commit the shared offensive companion allowance, but not its Bonus Action command.

**Guard:** choose a legal ally in the aura, granting+2 AC until the Paladin's next original regular start. No recorded weapon or offensive-companion debit is required. Both modes spend the same ally's long-rest use.

## Soldier: Palisade and materials

At Soldier5 the automatic Palisade engine grants construction; it is not a selected skill. Spend an Action, one actual carried kit and an encounter deployment to erect contiguous unoccupied10×5-foot ground within5, height5, AC12. It blocks movement and line of sight across its height; climbing uses10 feet movement, with actual geometry/cover adjudicated normally. Psychic/poison immunity applies.

**NEW construction snapshot:** maximumHP=max(1,5+actual CON at deployment). At creation with Soldier13+, double that value and grant area-damage resistance. Later statistics do not recalculate or heal existing construction. The intact-wall cap and encounter deployments are1 below13,2 at13+. A later cap decrease preserves existing walls but prevents further construction at or above the current cap.

States are intact, destroyed or dismantled. Only positive-HP intact walls count against the cap and grant the printed benefits. Deployment consumes one kit into the wall. **NEW material integration:** completed one-minute dismantling returns at most one reusable carried kit, with hard carried cap2. At2, no third kit, hidden cache, deferred credit or sale value is created. Dismantling does not refund the encounter deployment. Destruction releases intact capacity without a kit, use, salvage or reconstruction refund. A completed long rest with carpentry tools replenishes carried kits to2; it does not restore walls or reset encounter counters without an actual encounter transition.

Once per encounter, an Action plus actual spare parts restores currentM HP to an eligible positive-HP damaged wall, capped at creation maximum. No repair payment at full HP, no0-HP reconstruction, no kit/deployment reset. Material accounting uses actual inventory; reference supply units represent one real source-qualified kit, field-supply use or spare-part use, not a newly invented economy price.

Hold Position grants+1 AC/+1 saves while adjacent to your intact wall. Brace Line grants the specified ally2 flatDR only with the printed wall/ally/attacker geometry. Bonuses do not stack across Soldier walls; strongest flatDR applies. Full cover prevents targeting instead of adding another cover AC bonus. Palisade Synergy addsS once per own turn to an actual own ranged weapon hit while adjacent to your deployed intact wall; it does not apply to every shot, area save or turret hit.

## Soldier: turrets, Quick Deploy and named protections

**Turret Deployment:** Action, one short-rest use, choose **one or two** legal empty squares within10. This reconciles “up to2” targets with “deploy2.” A chosen single turret spends the full use; no later second placement. Validate a two-turret placement atomically. Each snapshots AC12+PB, HP2×Soldier level, immobile, duration three rounds. One shared regular-turn Bonus Action/offensive command fires one turret: range60, current original Soldier PB+actual DEX,1d6+currentM piercing. There is no autonomous fire.

There is no printed global2-turret cap. Another independently legal refreshed use can create another1–2 while the old set remains; all share one owner offense/command. Expiry/reclamation is administrative bookkeeping with no sale, salvage, inventory surplus, extra deployment or recharge reset.

**Quick Deploy:** Action, one encounter use and actual carried field supplies; one legal5-foot square within5; AC12/HP5, three rounds or destroyed, half cover and difficult terrain. One at a time. **NEW replacement:** a successful independent legal use administratively ends old cover immediately before placing the new. Invalid replacement leaves the old object untouched. No refund or salvage. It is not Palisade and receives no Palisade TierII, repair, Hold Position, Brace Line or Synergy.

Neither Soldier turrets nor these structures inherit Tinker Field Repair, Snap, protected Dissonance routing, Volatile Components, Recycling, Salvage or Tinker deployable slots by analogy. An exact future source must grant a cross-class right individually.

**Bubble of Discipline** is a non-HP protective zone with only its printed spell-attack AC, spell-save and once-total Reaction reduction. **Fortify Zone** is a non-HP firing-lane effect dependent on the conscious Soldier and printed range/attack geometry. **Wall of Aegis** is a creature flat-DR effect, not another physical wall. None grants an attackable/repairable/dismantlable anchor or Palisade Synergy. Real cover and an independently applicable DR effect can both operate, but flatDR still uses strongest-only arbitration. Complete zone targeting, duration and defense execution remain with the appropriate combat/defense interfaces.

## Classified guards and deferred work

All 80 source IDs are individually discussed. Anti-farm and agency passages constrain their own Conviction, BG, Momentum, RC, Blood Tithe, healing, kill and copy systems; they never create corpse or companion permissions. Prior healing, death, control, maximum-HP and damage-sharing component reviews remain component reviews. Incidental temporary-HP effects, the complete Time Loop snapshot, full forms, all unimplemented portions of these cards and full source-family integration remain open.

The bounded guide adds no named abilities. All NEW procedures above are explicit completions of already existing sources, with original text preserved. Global corpse decay/cleanup, natural creature rest/Hit Dice, complete scout travel procedures, balance, human playtesting and the full tabletop/video-game runtime are not closed by these checks.

```

## tools/remaining_lifecycle_playtest_rules.py
SHA256 4f2d26e482206adeb5aa1e5ca5b9d107327a22f698f1acdc27fe184c8933d4ff
```
"""Bounded Cleric/Oracle/Paladin/Soldier lifecycle reference, not a runtime.

Share CreatureWorld (physical bodies), Wallet, CommandLedger, HardDenialLedger,
ExtraActionClock and IncomingAttacks across all abilities. The caller certifies
source access, placement/targets/agency, exact deadlines, recharge/reset scopes,
ordinary rolls/defenses and native creature zero-HP handling. A true legality
flag is an assertion of those checks, never an authorization invented here.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from creature_lifecycle_playtest_rules import Creature, CreatureWorld, Corpse, require, HardDenialLedger
from device_lifecycle_playtest_rules import Wallet, CommandLedger
from combat_playtest_rules import ExtraActionClock
from control_playtest_rules import ClockMarker, clock_marker, require_deadline
from spell_playtest_rules import SpellRuleError, integer
from redirection_playtest_rules import identity

CHOIR='cleric.hero.cultist.rite-of-the-crimson-choir'
RITUAL='cleric.hero.cultist.ritual-of-undeath'
UNBOUND='oracle.supplement.bones.ledger-unbound'
LEDGER='oracle.supplement.bones.ledger-s-command'
TURRET='soldier.hero.artillerist.turret-deployment'
PALISADE='soldier.arch.palisade-deployment'
QUICK='soldier.base.quick-deploy'
ZONES=frozenset(('soldier.hero.artillerist.bubble-of-discipline',
                'soldier.arch.fortify-zone','soldier.hero.champion.wall-of-aegis'))


@dataclass(frozen=True)
class Stats:
    owner: str
    source_class: str
    level: int
    pb: int
    scale: int
    modifier: int
    attack: int
    dc: int
    constitution: int=0
    dexterity: int=0
    charisma: int=0

    def __post_init__(self):
        identity(self.owner)
        require(self.source_class in ('cleric','oracle','paladin','soldier'),'Wrong source class')
        integer(self.level,'class level',1,20);integer(self.pb,'PB',1)
        integer(self.scale,'S',1,4);integer(self.modifier,'M',1)
        for v in (self.attack,self.dc,self.constitution,self.dexterity,self.charisma):
            require(type(v) is int,'Actual modifier must be an integer')


def deadline(now,expiry,seconds):
    now=clock_marker(now);require_deadline(expiry)
    require(now<expiry and expiry.seconds-now.seconds<=seconds,'Invalid printed deadline')


@dataclass
class Points:
    """Adapter to the canonical class resource balance (Conviction or RC)."""
    owner: str
    resource: str
    value: int

    def validate(self,owner,resource,cost):
        require((self.owner,self.resource)==(owner,resource),'Wrong resource ledger')
        integer(self.value,'class resource',0);integer(cost,'class resource cost',0)
        require(self.value>=cost,'Insufficient class resource')


@dataclass
class RemainingCreature(Creature):
    position: object=None
    explosion_settled: bool=False
    local_modes: dict=field(default_factory=dict)

    def attack_profile(self,stats):
        self.verify_stats(stats)
        out={'sourceOwner':self.source_owner,'sourceClass':self.source_class,
             'attack':stats.attack,'saves':stats.pb,'saveDC':stats.dc,
             'range':5,'mode':'melee','damageType':'necrotic','resourceEligible':False}
        if self.profile=='choir':out['damage']=(1,6,stats.scale)
        elif self.profile=='thrall':out['damage']=(stats.scale,6,0)
        elif self.profile=='bone-servant':out['damage']=(1,8,stats.scale)
        elif self.profile=='soldier-turret':
            out.update(attack=stats.pb+stats.dexterity,range=60,mode='ranged',
                       damage=(1,6,stats.modifier),damageType='piercing')
        else:raise SpellRuleError('Unregistered remaining companion profile')
        return out


@dataclass
class Structure:
    instance_id: str
    owner: str
    kind: str
    maximum_hp: int
    hp: int
    expiry: ClockMarker | None=None
    area_resistance: bool=False
    state: str='intact'
    ac: int=12

    def active(self,now):
        return self.state=='intact' and self.hp>0 and (self.expiry is None or clock_marker(now)<self.expiry)


@dataclass
class Supplies:
    owner: str
    kits: int=2
    field_supplies: int=0
    spare_parts: int=0
    deployments: dict=field(default_factory=dict)
    repaired: set=field(default_factory=set)

    def validate(self,owner):
        require(self.owner==owner,'Wrong material inventory')
        integer(self.kits,'carried kits',0,2)
        integer(self.field_supplies,'actual field supply uses',0)
        integer(self.spare_parts,'actual spare-part uses',0)

    def completed_rest(self,*,completed,carpentry):
        self.validate(self.owner)
        require(completed and carpentry,'Actual completed long rest and carpentry tools required')
        self.kits=2


@dataclass
class IncomingAttacks:
    """Canonical post-hit/pre-consequence windows, keyed by real attack identity."""
    closed: set=field(default_factory=set)

    def validate(self,attack_id,*,successful_single_target_hit,pre_consequences,legal):
        identity(attack_id)
        require(successful_single_target_hit and pre_consequences and legal,'No legal interception window')
        require(attack_id not in self.closed,'Attack already intercepted/resolved')

    def commit(self,attack_id,target):
        self.closed.add(attack_id)
        return {'attackId':attack_id,'zeroAssignmentTarget':target,'oracleDamage':0,
                'oracleOnHit':False,'newAttackRoll':False,'transferredDamage':False,
                'damageEvent':False,'resourceEvent':False,'duplicateBody':False,
                'nativeZeroLifecycleRequired':True}


@dataclass
class ExistingUndeadBuff:
    owner: str
    members: frozenset
    expiry: ClockMarker
    first_damage: set=field(default_factory=set)

    def operative(self,target,now,*,controlled):
        return controlled and target in self.members and clock_marker(now)<self.expiry

    def attack_bonus(self,target,now,scale,*,controlled,commanded):
        integer(scale,'S',1,4)
        return scale if commanded and self.operative(target,now,controlled=controlled) else 0

    def first_damage_offer(self,target,now,round_number,*,controlled,qualifying):
        integer(round_number,'numbered round',1)
        key=(target,round_number)
        if not qualifying or not self.operative(target,now,controlled=controlled) or key in self.first_damage:return 0
        self.first_damage.add(key)
        return 1  # Consume before strongest-only arbitration, even if another DR wins.


class RemainingWorld:
    def __init__(self,physical_world):
        self.physical=physical_world
        self.structures={};self.orders={};self.choirs={};self.choir_healing={}
        self.hit_events=set();self.unbound_buffs={};self.synergy_turns=set()

    def fresh(self,ident):
        self.physical.fresh(ident)
        require(ident not in self.structures,'Object identity already exists')

    def create(self,ident,stats,source,profile,hp,ac,speed,expiry,**kwargs):
        return RemainingCreature(ident,stats.owner,stats.owner,stats.source_class,source,profile,
                                 'finite',hp,hp,hp,ac,speed,expiry=expiry,**kwargs)

    def choir(self,application,ids,positions,stats,now,expiry,wallet,conviction,*,use_key,legal,concentration):
        identity(application);require(application not in self.choirs,'Application reused')
        require(stats.source_class=='cleric' and legal and concentration,'Choir source/placement/concentration required')
        require(len(ids)==len(set(ids))==len(positions)==4,'Exactly four unique legal bodies required')
        deadline(now,expiry,18)
        for ident in ids:self.fresh(ident)
        identity(use_key);wallet.validate(8,'action',use_key);conviction.validate(stats.owner,'Conviction',5)
        cs=[self.create(i,stats,CHOIR,'choir',10,14,30,expiry,concentration=concentration,
                        command_group=application,position=deepcopy(p)) for i,p in zip(ids,positions)]
        wallet.pay(8,'action',use_key);conviction.value-=5
        self.choirs[application]=tuple(ids)
        for c in cs:self.physical.creatures[c.instance_id]=c
        return tuple(cs)

    def thrall(self,ident,body_id,stats,now,expiry,wallet,conviction,*,use_key,legal,death_age_seconds):
        require(stats.source_class=='cleric' and legal,'Corpse Servant exact source gates required')
        integer(death_age_seconds,'actual corpse age seconds',0,60)
        self.fresh(ident);deadline(now,expiry,18);identity(use_key)
        body=self.physical.corpses[body_id]
        require(body.real_original and body.available and body.creature_type=='humanoid','Real available humanoid body required')
        wallet.validate(6,'action',use_key);conviction.validate(stats.owner,'Conviction',3)
        c=self.create(ident,stats,RITUAL,'thrall',10,13,30,expiry)
        wallet.pay(6,'action',use_key);conviction.value-=3
        self.physical.consume_body(body_id,ident);self.physical.creatures[ident]=c
        return c

    def unbound(self,application,ids,body_ids,existing_ids,stats,now,expiry,wallet,*,use_key,legal,existing_control_certified):
        identity(application);require(application not in self.unbound_buffs,'Application reused')
        require(stats.source_class=='oracle' and legal and existing_control_certified,'Exact Unbound/body/control gates required')
        require(len(ids)==len(body_ids)<=3 and len(set(ids))==len(ids) and len(set(body_ids))==len(body_ids),'Unique bodies/instances, up to three')
        require(len(existing_ids)<=3 and len(set(existing_ids))==len(existing_ids) and not set(ids)&set(existing_ids),'Snapshot existing undead before creation')
        for ident in existing_ids:identity(ident)
        for ident in ids:self.fresh(ident)
        for ident in body_ids:
            body=self.physical.corpses[ident]
            require(body.real_original and body.available,'Real available nonsummoned body required')
        deadline(now,expiry,18);identity(use_key);wallet.validate(0,'action',use_key)
        cs=[self.create(i,stats,UNBOUND,'bone-servant',1,12+stats.pb//2,30,expiry) for i in ids]
        buff=ExistingUndeadBuff(stats.owner,frozenset(existing_ids),expiry)
        wallet.pay(0,'action',use_key)
        for body_id,c in zip(body_ids,cs):
            self.physical.consume_body(body_id,c.instance_id);self.physical.creatures[c.instance_id]=c
        self.unbound_buffs[application]=buff
        return tuple(cs),buff

    def turrets(self,ids,stats,now,expiry,wallet,*,use_key,legal):
        require(stats.source_class=='soldier' and legal,'Exact Turret source/placement gates required')
        require(1<=len(ids)<=2 and len(set(ids))==len(ids),'Choose one or two legal turrets for this use')
        for ident in ids:self.fresh(ident)
        deadline(now,expiry,18);identity(use_key);wallet.validate(0,'action',use_key)
        cs=[self.create(i,stats,TURRET,'soldier-turret',2*stats.level,12+stats.pb,0,expiry) for i in ids]
        wallet.pay(0,'action',use_key)
        for c in cs:self.physical.creatures[c.instance_id]=c
        return tuple(cs)

    def command(self,order_id,ids,round_number,now,wallet,ledger,*,regular,legal,capable):
        identity(order_id);require(order_id not in self.orders,'Order identity reused')
        require(regular and legal and capable,'Original regular-turn issuance and legal capable actors required')
        require(ids and len(set(ids))==len(ids),'Unique commanded identities required')
        cs=[self.physical.creatures[i] for i in ids]
        require(all(isinstance(c,RemainingCreature) and c.controller==ledger.owner and c.can_act(now,round_number) for c in cs),'Own active selected creatures required')
        if len(cs)>1:
            require(len(cs)<=4 and all(c.profile=='choir' and c.command_group==cs[0].command_group for c in cs),'Only one Choir permits grouped attacks')
        for c in cs:
            require(c.profile!='bone-servant' or round_number not in c.local_modes,'Servant local attack/sacrifice choice spent')
        ledger.activate(round_number,'attack',wallet)
        for c in cs:
            if c.profile=='bone-servant':c.local_modes[round_number]='ATTACK_RESERVED'
        self.orders[order_id]={'owner':ledger.owner,'ids':tuple(ids),'round':round_number,'settled':False}

    def resolve_command(self,order_id,round_number,now,*,attached_phase,valid_ids):
        o=self.orders[order_id]
        require(attached_phase and round_number==o['round'] and not o['settled'],'Exactly once in designated attached phase')
        require(set(valid_ids)<=set(o['ids']),'Only commanded actors may execute')
        o['settled']=True
        live=[i for i in o['ids'] if i in valid_ids and self.physical.creatures[i].controller==o['owner']
              and self.physical.creatures[i].can_act(now,round_number)]
        o['executed']=tuple(live)
        return {'attackers':live,'attackRolls':len(live),'extraTurns':0,'refund':False}

    def choir_hit(self,event_id,order_id,fanatic_id,round_number,*,hit,healing_permitted,current_hp,maximum_hp):
        identity(event_id);o=self.orders[order_id]
        require(o['settled'] and round_number==o['round'] and fanatic_id in o.get('executed',()),'Must follow the actual commanded attack')
        c=self.physical.creatures[fanatic_id];require(c.profile=='choir','Choir only')
        key=(order_id,fanatic_id)
        require(event_id not in self.hit_events and key not in self.hit_events,'Attack result already settled')
        integer(maximum_hp,'maximum HP',1);integer(current_hp,'current HP',0,maximum_hp)
        self.hit_events.update((event_id,key))
        cap_key=(o['owner'],round_number);used=self.choir_healing.get(cap_key,0)
        gained=int(bool(hit and healing_permitted and used<4 and current_hp<maximum_hp))
        self.choir_healing[cap_key]=used+gained
        return {'hp':current_hp+gained,'healed':gained,'woundsRemoved':0}

    def burst(self,c,*,suppressed=False):
        require(c.profile=='choir','Only Choir explodes')
        if c.explosion_settled:return None
        c.explosion_settled=True
        if suppressed:return None
        return {'fanatic':c.instance_id,'position':deepcopy(c.position),'radius':5,'targets':'legal enemies',
                'damage':'1d6 necrotic','save':'DEX half','healing':False,'commandDebit':False,
                'noDeathTriggers':True,'noRetaliation':True,'noDamageTriggers':True,
                'noResourceGeneration':True,'noCopyChain':True,'corpse':False}

    def damage(self,ident,amount,now,*,suppress_zero_explosion=False):
        """Actual damage after defenses, before this body's existing temp HP."""
        c=self.physical.creatures[ident]
        require(isinstance(c,RemainingCreature) and c.active(now),'Active selected finite body required')
        integer(amount,'post-defense damage',0)
        absorbed=min(amount,c.temp_hp);c.temp_hp-=absorbed;c.hp=max(0,c.hp-(amount-absorbed))
        burst=None
        if c.hp==0:
            c.state='ended'
            if c.profile=='choir':burst=self.burst(c,suppressed=suppress_zero_explosion)
        return {'burst':burst,'corpse':False,'woundRoll':False}

    def end_choir(self,application,now,*,concentration_ended=False):
        cs=[self.physical.creatures[i] for i in self.choirs[application]]
        require(concentration_ended or all(clock_marker(now)>=c.expiry for c in cs),'Actual concentration or deadline ending required')
        # Snapshot descriptors before effects can alter positions or end another body.
        survivors=[c for c in cs if c.state=='active' and c.hp>0]
        events=[self.burst(c) for c in survivors]
        for c in survivors:c.state='ended'
        return [e for e in events if e is not None]

    def expire(self,now):
        events=[]
        for application,ids in self.choirs.items():
            if clock_marker(now)>=self.physical.creatures[ids[0]].expiry:
                events+=self.end_choir(application,now)
        for c in self.physical.creatures.values():
            if isinstance(c,RemainingCreature) and c.profile!='choir' and c.state=='active' and clock_marker(now)>=c.expiry:c.state='ended'
        for s in self.structures.values():
            if s.expiry and clock_marker(now)>=s.expiry and s.state=='intact':s.state='expired'
        return events

    def sacrifice(self,ident,round_number,now,wallet,windows,attack_id,*,owner,legal,successful_single_target_hit,pre_consequences):
        c=self.physical.creatures[ident]
        require(isinstance(c,RemainingCreature) and c.profile=='bone-servant' and c.active(now),'Living Unbound servant required')
        require(c.controller==c.source_owner==owner,'Original Oracle must currently control its own servant')
        integer(round_number,'numbered round',1)
        require(round_number not in c.local_modes,'This servant already reserved attack/sacrifice')
        windows.validate(attack_id,successful_single_target_hit=successful_single_target_hit,pre_consequences=pre_consequences,legal=legal)
        wallet.validate(0,'reaction')
        wallet.pay(action='reaction');c.local_modes[round_number]='SACRIFICED';c.hp=0;c.state='ended'
        return windows.commit(attack_id,ident)

    def palisade(self,ident,stats,supplies,wallet,encounter,*,legal):
        require(stats.source_class=='soldier' and stats.level>=5 and legal,'Palisade access/material/ground requirements')
        self.fresh(ident);identity(encounter);supplies.validate(stats.owner)
        cap=2 if stats.level>=13 else 1
        count=sum(s.owner==stats.owner and s.kind=='palisade' and s.state=='intact' for s in self.structures.values())
        require(count<cap and supplies.deployments.get(encounter,0)<cap and supplies.kits>0,'Intact cap, encounter allowance or kit exhausted')
        wallet.validate(0,'action');maximum=max(1,5+stats.constitution)*(2 if stats.level>=13 else 1)
        s=Structure(ident,stats.owner,'palisade',maximum,maximum,area_resistance=stats.level>=13)
        wallet.pay(action='action');supplies.kits-=1;supplies.deployments[encounter]=supplies.deployments.get(encounter,0)+1
        self.structures[ident]=s
        self.physical.noncorpse_identities.add(ident)
        return s

    def quick_deploy(self,ident,stats,supplies,now,expiry,wallet,*,use_key,legal):
        require(stats.source_class=='soldier' and legal,'Legal Quick Deploy required')
        self.fresh(ident);supplies.validate(stats.owner);require(supplies.field_supplies>0,'Actual carried field supplies required')
        deadline(now,expiry,18);identity(use_key);wallet.validate(0,'action',use_key)
        s=Structure(ident,stats.owner,'quick',5,5,expiry)
        wallet.pay(0,'action',use_key);supplies.field_supplies-=1
        for old in self.structures.values():
            if old.owner==stats.owner and old.kind=='quick' and old.state=='intact':old.state='replaced'
        self.structures[ident]=s
        self.physical.noncorpse_identities.add(ident)
        return s

    def structure_damage(self,ident,amount,now):
        """Caller already applied actual object defenses, including area resistance."""
        s=self.structures[ident];require(s.active(now),'Intact object required');integer(amount,'post-defense damage',0)
        s.hp=max(0,s.hp-amount)
        if s.hp==0:s.state='destroyed'
        return {'hp':s.hp,'state':s.state,'salvage':0,'kitRefund':0}

    def repair(self,ident,stats,supplies,wallet,encounter,now,*,legal):
        s=self.structures[ident];supplies.validate(stats.owner)
        require(stats.source_class=='soldier' and s.owner==stats.owner and s.kind=='palisade' and s.active(now) and legal,'Own legal positive-HP Palisade required')
        require(s.hp<s.maximum_hp and encounter not in supplies.repaired and supplies.spare_parts>0,'Repair requires damage, unused encounter use and actual spare parts')
        wallet.validate(0,'action');gain=min(stats.modifier,s.maximum_hp-s.hp)
        wallet.pay(action='action');supplies.spare_parts-=1;supplies.repaired.add(encounter);s.hp+=gain
        return gain

    def dismantle(self,ident,supplies,now,*,completed_seconds,legal):
        s=self.structures[ident];supplies.validate(s.owner)
        require(legal and completed_seconds>=60 and s.kind=='palisade' and s.active(now),'Actual one-minute dismantling of intact Palisade required')
        s.state='dismantled';before=supplies.kits;supplies.kits=min(2,before+1)
        return supplies.kits-before

    def palisade_benefits(self,ident,owner,now,*,adjacent,brace_geometry):
        s=self.structures[ident]
        valid=s.owner==owner and s.kind=='palisade' and s.active(now) and adjacent
        return {'holdAC':int(valid),'holdSaves':int(valid),'braceFlatDR':2 if valid and brace_geometry else 0}

    def synergy(self,ident,stats,now,turn_id,*,adjacent,own_ranged_weapon_hit):
        identity(turn_id);s=self.structures[ident];key=(stats.owner,turn_id)
        require(stats.source_class=='soldier' and s.owner==stats.owner and s.kind=='palisade' and s.active(now) and adjacent and own_ranged_weapon_hit,'Actual own ranged weapon hit beside own intact Palisade required')
        require(key not in self.synergy_turns,'Palisade Synergy already used this own turn')
        self.synergy_turns.add(key);return stats.scale


@dataclass
class LedgerControl:
    owner: str
    application_id: str
    expiry: ClockMarker
    targets: dict
    interception_used: bool=False
    pending: dict=field(default_factory=dict)
    order_ids: set=field(default_factory=set)
    first_damage: set=field(default_factory=set)

    @classmethod
    def apply(cls,application,stats,now,expiry,target_results,wallet,rc,*,legal,mastery=False):
        """target_results maps eligible target ID to actual failed/waived initial save.
        Caller checks nonlegendary undead, CR<=floor(L/2), range20, agency.
        Successful saves still consume the cast's Action and2 RC.
        """
        identity(application);require(stats.source_class=='oracle' and legal,'Exact Ledger source/target gates')
        require(1<=len(target_results)<=(3 if mastery else 2),'One to printed target maximum')
        for t,result in target_results.items():identity(t);require(type(result) is bool,'Resolved save result required')
        deadline(now,expiry,12);wallet.validate(0,'action');rc.validate(stats.owner,'RC',2)
        wallet.pay(action='action');rc.value-=2
        return cls(stats.owner,application,expiry,{t:{'active':True,'last_end':0,'soft_until':None} for t,v in target_results.items() if v})

    def operative(self,target,now,controlled):
        return controlled and target in self.targets and self.targets[target]['active'] and clock_marker(now)<self.expiry

    def issue(self,target,order_id,now,round_number,wallet,commands,hard,encounter,*,regular,willing,controlled,capable,legal,extra_clock=None,granted_by_extra_action=False,target_turn_upcoming=True):
        identity(order_id);require(order_id not in self.order_ids and target not in self.pending,'Duplicate order or pending target')
        require(commands.owner==self.owner,'Wrong canonical command ledger')
        require(regular and capable and legal and self.operative(target,now,controlled),'Legal original regular-turn order required')
        if willing:
            require(isinstance(extra_clock,ExtraActionClock) and not granted_by_extra_action and round_number not in extra_clock.spent_rounds,'Canonical target extra-Action allowance required')
            commands.validate(round_number,'attack',wallet)
            extra_clock.spend(round_number);commands.activate(round_number,'attack',wallet);resolution=round_number
        else:
            require(hard.available(encounter,self.owner,target),'Shared hard denial spent')
            resolution=round_number if target_turn_upcoming else round_number+1
            commands.reserve(round_number,resolution,order_id,wallet)
        self.order_ids.add(order_id)
        self.pending[target]={'id':order_id,'round':resolution,'willing':willing,'encounter':encounter}
        return resolution

    def cancel(self,target,commands):
        require(commands.owner==self.owner,'Wrong command ledger')
        o=self.pending.pop(target,None)
        if o and not o['willing']:commands.settle(o['round'],o['id'],executed=False)

    def resolve(self,target,now,round_number,commands,hard,*,attached_phase=False,actual_regular_action_slot=False,willing,controlled,capable,legal):
        require(commands.owner==self.owner and target in self.pending,'Matching pending order required')
        o=self.pending[target];require(round_number==o['round'],'Wrong resolution round')
        require(attached_phase if o['willing'] else actual_regular_action_slot,'Wrong action checkpoint')
        valid=self.operative(target,now,controlled) and capable and legal
        if o['willing']:valid=valid and willing
        else:valid=valid and hard.available(o['encounter'],self.owner,target)
        if not o['willing']:
            commands.settle(round_number,o['id'],executed=bool(valid))
            if valid:hard.spend(o['encounter'],self.owner,target)
        del self.pending[target]
        return {'attackRolls':int(bool(valid)),'replacesNormalAction':bool(valid and not o['willing']),
                'extraAction':bool(valid and o['willing']),'extraTurn':False,'sourceStats':'original creature',
                'damageCap':'S d8+M','monsterMultiattack':False,'resourceRiders':False}

    def revalidate(self,target,now,commands,hard,*,willing,controlled,capable,legal):
        o=self.pending.get(target)
        if not o:return False
        valid=self.operative(target,now,controlled) and capable and legal
        valid=valid and (willing if o['willing'] else hard.available(o['encounter'],self.owner,target))
        if not valid:self.cancel(target,commands)
        return bool(valid)

    def regular_end(self,target,now,marker,commands,hard,encounter,*,failed_save,regular,controlled):
        t=self.targets[target];integer(marker,'target original regular-end index',1)
        require(regular and marker>t['last_end'],'Extra/repeated end cannot tick target')
        t['last_end']=marker;t['soft_until']=None
        if not self.operative(target,now,controlled) or not failed_save:
            t['active']=False;self.cancel(target,commands);return None
        if not hard.available(encounter,self.owner,target):
            t['soft_until']=marker+1
            return {'noReactions':True,'speed':0,'untilRegularEnd':marker+1,'orEarlier':self.expiry}
        return None

    def first_damage_offer(self,target,now,round_number,*,controlled,qualifying):
        integer(round_number,'numbered round',1);key=(target,round_number)
        if not qualifying or not self.operative(target,now,controlled) or key in self.first_damage:return 0
        self.first_damage.add(key);return 1

    def intercept(self,target,now,windows,attack_id,*,controlled,expendable,native_zero_legal,successful_single_target_hit,pre_consequences):
        require(self.operative(target,now,controlled) and expendable and native_zero_legal and not self.interception_used,'Legal expendable controlled undead and unused application required')
        windows.validate(attack_id,successful_single_target_hit=successful_single_target_hit,pre_consequences=pre_consequences,legal=True)
        self.interception_used=True
        # Return a zero-assignment instruction; caller executes native death prevention/lifecycle.
        return windows.commit(attack_id,target)


@dataclass(frozen=True)
class WeaponProfile:
    attack: int
    dice: tuple  # tuple of (count,sides), ordinary base only
    flat: int
    damage_type: str
    range_feet: int

    def __post_init__(self):
        require(type(self.attack) is int and type(self.flat) is int,'Recorded numeric attack/base modifier required')
        identity(self.damage_type);integer(self.range_feet,'actual ordinary weapon range',1)
        for count,sides in self.dice:integer(count,'dice count',1);integer(sides,'die sides',2)

    def capped_damage(self,scale,modifier):
        integer(scale,'S',1,4);integer(modifier,'M',1)
        if sum(n*s for n,s in self.dice)+self.flat>8*scale+modifier:return (((scale,8),),modifier)
        return self.dice,self.flat


def ledger_attack_profile(profile,stats):
    require(isinstance(profile,WeaponProfile) and stats.source_class=='oracle','Actual permitted native ordinary attack and Oracle stats required')
    dice,flat=profile.capped_damage(stats.scale,stats.modifier)
    return {'attack':profile.attack,'dice':dice,'flat':flat,'damageType':profile.damage_type,
            'range':profile.range_feet,'ordinaryCrit':True,'multiattack':False,'resourceRiders':False}


@dataclass
class FallenEchoes:
    deaths: set=field(default_factory=set)
    uses: set=field(default_factory=set)

    def record_death(self,owner,ally,encounter,*,actual_allied_death_in_aura):
        for v in (owner,ally,encounter):identity(v)
        require(actual_allied_death_in_aura,'Must be actual allied death in aura, not finite disappearance')
        self.deaths.add((owner,ally,encounter))

    def invoke(self,ally,encounter,rest_epoch,mode,stats,round_number,wallet,commands,*,legal,own_turn,profile=None,guard_expiry=None):
        require(stats.source_class=='paladin' and commands.owner==stats.owner and legal and own_turn,'Actual own Action and exact legal Echo target/source required')
        identity(rest_epoch);require((stats.owner,ally,encounter) in self.deaths,'Recorded qualifying death required')
        key=(stats.owner,ally,rest_epoch);require(key not in self.uses,'Same fallen ally already used this long rest')
        require(mode in ('strike','guard'),'Choose exactly one Echo mode')
        wallet.validate(10,'action')
        if mode=='strike':
            require(isinstance(profile,WeaponProfile),'Recorded ordinary weapon profile required')
            commands.validate(round_number,'decoy',wallet)
            dice,flat=profile.capped_damage(stats.scale,stats.modifier)
            result={'attack':min(profile.attack,stats.pb+stats.charisma),'dice':dice,'flat':flat,
                    'damageType':profile.damage_type,'range':profile.range_feet,'ordinaryCrit':True}
        else:
            require_deadline(guard_expiry)
            result={'acBonus':2,'expires':guard_expiry}
        wallet.pay(10,'action');self.uses.add(key)
        if mode=='strike':commands.activate(round_number,'decoy',wallet)
        result.update(targetable=False,corpse=False,resurrection=False,extraTurn=False,resourceRiders=False)
        return result


@dataclass
class SpiritScout:
    owner: str
    mode: str
    expiry: ClockMarker
    state: str='outbound'
    delivered_message: bool=False
    observations: list=field(default_factory=list)

    @classmethod
    def summon(cls,stats,mode,now,expiry,wallet,*,use_key,legal_timed_route):
        require(stats.source_class=='oracle' and legal_timed_route,'Source/route/plane/barrier/timing certification required')
        require(mode in ('observe','inquiry','message'),'One assigned task required')
        deadline(now,expiry,600);identity(use_key);wallet.validate(0,'action',use_key)
        wallet.pay(0,'action',use_key);return cls(stats.owner,mode,expiry)

    def arrive_and_perform(self,now,observations,*,legal_direct_observations,willing_spirits=True):
        require(self.state=='outbound' and clock_marker(now)<self.expiry,'Live outbound task required')
        require(legal_direct_observations and (self.mode!='inquiry' or willing_spirits),'Ordinary direct observations or willing spirit inquiry only')
        self.observations=list(observations);self.delivered_message=self.mode=='message';self.state='returning'

    def return_report(self,now,*,actually_returned):
        require(self.state=='returning' and actually_returned,'Actual return required; no remote report')
        if clock_marker(now)>=self.expiry:
            self.state='expired';return []
        self.state='ended';return list(self.observations)

    def expire(self,now):
        if clock_marker(now)>=self.expiry and self.state in ('outbound','returning'):self.state='expired'
        return {'state':self.state,'remoteReport':None,'messageAlreadyDelivered':self.delivered_message}

```

## tools/validate_remaining_lifecycle_playtests.py
SHA256 9245c5282b038343dd5aeaf6c6710646b10c3898cea941a789bef8562e78771e
```
"""Adversarial transactions for remaining lifecycle interfaces."""
from pathlib import Path
from dataclasses import replace
from copy import deepcopy
import json
from remaining_lifecycle_playtest_rules import *
ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    def check(name,got,want):
        assert got==want,(name,got,want)
        checks.append({'name':name,'result':'PASS'})
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append({'name':name,'result':'PASS'})
        else:raise AssertionError(name)
    def stats(cls='cleric',**kw):
        return replace(Stats('owner',cls,10,4,2,3,7,15,constitution=3,dexterity=2,charisma=3),**kw)
    def world():return RemainingWorld(CreatureWorld())
    def corpse(w,body='body',kind='humanoid'):
        c=Corpse(body,'original:'+body,kind);w.physical.register_corpse(c);return c
    def choir(w,application='choir'):
        return w.choir(application,tuple(application+str(n) for n in range(4)),((0,0),(1,0),(2,0),(3,0)),
                       stats(),0,ClockMarker(18),Wallet(20),Points('owner','Conviction',5),
                       use_key=application,legal=True,concentration=application)
    def unbound(w,application='unbound',n=3):
        ids=tuple(application+str(i) for i in range(n));bodies=tuple('body:'+i for i in ids)
        for body in bodies:corpse(w,body)
        return w.unbound(application,ids,bodies,('native',),stats('oracle'),0,ClockMarker(18),Wallet(),
                         use_key=application,legal=True,existing_control_certified=True)
    def control(targets=None):
        return LedgerControl.apply('control',stats('oracle'),0,ClockMarker(12),targets or {'native':True},Wallet(),Points('owner','RC',2),legal=True)
    def issue(b,commands,hard,*,willing=True,round_number=1,extra=None,target='native',order='order',**kw):
        return b.issue(target,order,1,round_number,Wallet(),commands,hard,'enc',regular=True,willing=willing,
                       controlled=True,capable=True,legal=True,extra_clock=extra,**kw)
    def resolve(b,commands,hard,*,willing=True,controlled=True,round_number=1):
        return b.resolve('native',2,round_number,commands,hard,attached_phase=True,actual_regular_action_slot=True,
                         willing=willing,controlled=controlled,capable=True,legal=True)
    def sacrifice(w,c,round_number,windows,attack='hit',**kw):
        args=dict(owner='owner',legal=True,successful_single_target_hit=True,pre_consequences=True);args.update(kw)
        return w.sacrifice(c.instance_id,round_number,2,Wallet(),windows,attack,**args)

    w=world();wallet=Wallet(7);points=Points('owner','Conviction',5)
    rejects('Choir insufficient RP is atomic',lambda:w.choir('fail',('a','b','c','d'),(1,2,3,4),stats(),0,ClockMarker(18),wallet,points,use_key='c',legal=True,concentration='c'))
    check('Failed Choir leaves all resources and bodies',(wallet.rp,wallet.actions,points.value,w.physical.creatures),(7,1,5,{}))
    cs=choir(w);commands=CommandLedger('owner')
    w.command('choir-attack',tuple(c.instance_id for c in cs),1,1,Wallet(),commands,regular=True,legal=True,capable=True)
    check('Four Choir rolls consume one shared command',w.resolve_command('choir-attack',1,2,attached_phase=True,valid_ids=tuple(c.instance_id for c in cs))['attackRolls'],4)
    check('Choir shared command/offense committed',commands.rounds[1],{'command':True,'damage':True})
    check('Fanatic exact attack profile',cs[0].attack_profile(stats())['damage'],(1,6,2))
    hp=5
    for i,c in enumerate(cs):hp=w.choir_hit('hit'+str(i),'choir-attack',c.instance_id,1,hit=True,healing_permitted=True,current_hp=hp,maximum_hp=20)['hp']
    check('Four legal hits heal four even zero actual damage',hp,9)
    rejects('Fanatic hit cannot replay with new event ID',lambda:w.choir_hit('new','choir-attack',cs[0].instance_id,1,hit=True,healing_permitted=True,current_hp=9,maximum_hp=20))
    rejects('No second same-round offensive command',lambda:commands.activate(1,'attack',Wallet()))
    suppressed=w.damage(cs[0].instance_id,10,3,suppress_zero_explosion=True)
    check('Sealed zero settles explosion permanently',(suppressed['burst'],cs[0].state,cs[0].explosion_settled),(None,'ended',True))
    burst=w.damage(cs[1].instance_id,10,3)['burst']
    check('Normal zero makes one gated independent burst',(burst['fanatic'],burst['radius'],burst['healing'],burst['noDeathTriggers']),(cs[1].instance_id,5,False,True))
    events=w.end_choir('choir',4,concentration_ended=True)
    check('Ending snapshots survivors in creation order',[e['fanatic'] for e in events],[cs[2].instance_id,cs[3].instance_id])
    cs[2].position=(99,99)
    check('Burst position does not drift',events[0]['position'],(2,0))
    check('Repeated expiry never repeats burst',w.expire(18),[])
    check('No finite corpses',w.physical.corpses,{})
    rejects('Known Choir cannot be relabeled real corpse',lambda:w.physical.register_corpse(Corpse('fake',cs[0].instance_id,'humanoid')))
    w=world();cs=choir(w)
    rejects('Output suppression alone cannot end Choir',lambda:w.end_choir('choir',2))
    check('All four ending bursts can exist independently',len(w.end_choir('choir',18)),4)
    w=world();cs=choir(w);commands=CommandLedger('owner')
    rejects('Extra turn cannot issue ordinary command',lambda:w.command('extra',(cs[0].instance_id,),1,1,Wallet(),commands,regular=False,legal=True,capable=True))
    w.command('a',(cs[0].instance_id,),1,1,Wallet(),commands,regular=True,legal=True,capable=True)
    w.resolve_command('a',1,2,attached_phase=True,valid_ids=())
    rejects('Invalid attached attack cannot generate healing',lambda:w.choir_hit('h','a',cs[0].instance_id,1,hit=True,healing_permitted=True,current_hp=2,maximum_hp=20))
    check('Invalid attached order loses offense',commands.rounds[1]['damage'],True)
    rejects('Attached order cannot replay',lambda:w.resolve_command('a',1,3,attached_phase=True,valid_ids=()))

    w=world();body=corpse(w);points=Points('owner','Conviction',3);wallet=Wallet(6)
    rejects('Too-old corpse rejected before payment',lambda:w.thrall('t','body',stats(),0,ClockMarker(18),wallet,points,use_key='r',legal=True,death_age_seconds=61))
    check('Rejected corpse mode leaves body',(body.available,wallet.rp,points.value),(True,6,3))
    c=w.thrall('t','body',stats(),0,ClockMarker(18),wallet,points,use_key='r',legal=True,death_age_seconds=60)
    check('Thrall consumes single physical body',(body.body_state,body.consumed_by,c.hp,c.ac,c.speed),('consumed','t',10,13,30))
    check('Thrall NEW melee-only profile',(c.attack_profile(stats())['mode'],c.attack_profile(stats())['range'],c.attack_profile(stats())['damage']),('melee',5,(2,6,0)))
    w.damage('t',10,1)
    check('Ended thrall never returns corpse',(body.available,c.state),(False,'ended'))
    rejects('Spent Ritual cannot also buy another mode',lambda:wallet.validate(0,'action','r'))
    rejects('Finite thrall cannot become corpse fuel',lambda:w.physical.register_corpse(Corpse('fake','t','humanoid')))

    w=world();cs,buff=unbound(w);commands=CommandLedger('owner');windows=IncomingAttacks()
    check('Bone servant profile',(cs[0].hp,cs[0].ac,cs[0].speed,cs[0].attack_profile(stats('oracle'))['damage']),(1,14,30,(1,8,2)))
    check('Unbound consumes each distinct corpse',all(not b.available for b in w.physical.corpses.values()),True)
    w.command('bone',(cs[0].instance_id,),1,1,Wallet(),commands,regular=True,legal=True,capable=True)
    rejects('Reserved attacker cannot sacrifice before attack',lambda:sacrifice(w,cs[0],1,windows))
    w.resolve_command('bone',1,2,attached_phase=True,valid_ids=())
    rejects('Failed attack does not refund local mode',lambda:sacrifice(w,cs[0],1,windows))
    result=sacrifice(w,cs[1],1,windows)
    check('Another servant may intercept without offense debit',(cs[1].state,result['damageEvent'],commands.rounds[1]['damage']),('ended',False,True))
    rejects('One attack cannot consume second interceptor',lambda:sacrifice(w,cs[2],1,windows))
    check('Second interception refusal preserves servant',cs[2].hp,1)
    rejects('Other controller cannot source-sacrifice servant',lambda:sacrifice(w,cs[2],1,windows,'hit2',owner='other'))
    rejects('Miss has no interception window',lambda:sacrifice(w,cs[2],1,windows,'miss',successful_single_target_hit=False))
    check('Created servants excluded from existing-undead snapshot',buff.operative(cs[0].instance_id,1,controlled=True),False)
    check('Existing member gets current S',buff.attack_bonus('native',1,3,controlled=True,commanded=True),3)
    check('Lost control suspends existing buff',buff.attack_bonus('native',2,3,controlled=False,commanded=True),0)
    check('Regained control restores same member only',buff.attack_bonus('native',3,3,controlled=True,commanded=True),3)
    check('No replacement member',buff.attack_bonus('replacement',3,3,controlled=True,commanded=True),0)
    check('First damage offers one flat DR',buff.first_damage_offer('native',2,1,controlled=True,qualifying=True),1)
    check('Losing flat DR arbitration still consumes opportunity',buff.first_damage_offer('native',3,1,controlled=True,qualifying=True),0)
    check('Numbered round permits next DR opportunity',buff.first_damage_offer('native',7,2,controlled=True,qualifying=True),1)
    check('Buff expires on original deadline',buff.attack_bonus('native',18,3,controlled=True,commanded=True),0)
    w.expire(18);check('Bone expiry grants no usable corpses',any(b.available for b in w.physical.corpses.values()),False)

    b=control();commands=CommandLedger('owner');hard=HardDenialLedger();extra=ExtraActionClock()
    extra.spend(1)
    rejects('Other source extra Action blocks willing Ledger atomically',lambda:issue(b,commands,hard,extra=extra))
    check('Failed extra-Action request leaves Oracle budget',commands.rounds,{})
    extra=ExtraActionClock();issue(b,commands,hard,extra=extra)
    check('Willing command spends canonical target cap',extra.spent_rounds,{1})
    result=resolve(b,commands,hard,willing=False)
    check('Withdrawn consent cancels with no forced substitute',(result['attackRolls'],result['replacesNormalAction'],hard.used,commands.rounds[1]['damage']),(0,False,set(),True))
    b=control();commands=CommandLedger('owner');extra=ExtraActionClock();issue(b,commands,hard,extra=extra)
    result=resolve(b,commands,hard)
    check('Willing attack retains native regular Action',(result['extraAction'],result['replacesNormalAction'],result['extraTurn']),(True,False,False))
    b=control();commands=CommandLedger('owner');hard=HardDenialLedger()
    issue(b,commands,hard,willing=False,target_turn_upcoming=False)
    check('Hostile order reserves next-round offense',(commands.rounds[1],commands.reservations),({'command':True,'damage':False},{2:'order'}))
    rejects('Reserved future offense blocks other source',lambda:commands.activate(2,'attack',Wallet()))
    rejects('Hostile order cannot resolve in issuance round',lambda:resolve(b,commands,hard,willing=False,round_number=1))
    check('Control loss cancels pending future reservation',b.revalidate('native',2,commands,hard,willing=False,controlled=False,capable=True,legal=True),False)
    check('Cancelled reservation releases only offense',(commands.reservations,commands.rounds[1]['command'],hard.used),({},True,set()))
    b=control();commands=CommandLedger('owner');hard=HardDenialLedger();issue(b,commands,hard,willing=False)
    result=resolve(b,commands,hard,willing=False)
    check('First hostile attack replaces actual regular Action',(result['replacesNormalAction'],result['extraAction'],hard.used),(True,False,{('enc','owner','native')}))
    rejects('Hard denial shared across later applications',lambda:issue(control(),CommandLedger('owner'),hard,willing=False,round_number=2))
    soft=b.regular_end('native',3,1,commands,hard,'enc',failed_save=True,regular=True,controlled=True)
    check('Later failed save gives only soft fallback',(soft['noReactions'],soft['speed'],soft['untilRegularEnd']),(True,0,2))
    rejects('Extra end cannot tick Ledger',lambda:b.regular_end('native',4,2,commands,hard,'enc',failed_save=True,regular=False,controlled=True))
    check('Successful subsequent save ends control',b.regular_end('native',9,2,commands,hard,'enc',failed_save=False,regular=True,controlled=True),None)
    check('Ended Ledger has no soft fallback',b.targets['native']['soft_until'],None)
    b=control();windows=IncomingAttacks()
    result=b.intercept('native',1,windows,'attack',controlled=True,expendable=True,native_zero_legal=True,successful_single_target_hit=True,pre_consequences=True)
    check('Ledger interception is assignment not replay',(result['newAttackRoll'],result['transferredDamage'],result['nativeZeroLifecycleRequired'],result['duplicateBody']),(False,False,True,False))
    rejects('Application-wide interception cannot repeat',lambda:b.intercept('native',2,windows,'otherattack',controlled=True,expendable=True,native_zero_legal=True,successful_single_target_hit=True,pre_consequences=True))
    b=control();rejects('Native agency/death prevention cannot be bypassed',lambda:b.intercept('native',1,IncomingAttacks(),'hit',controlled=True,expendable=True,native_zero_legal=False,successful_single_target_hit=True,pre_consequences=True))
    check('Inactive source does not consume first-damage chance',b.first_damage_offer('native',1,1,controlled=False,qualifying=True),0)
    check('Reactivated source may take first eligible event',b.first_damage_offer('native',2,1,controlled=True,qualifying=True),1)
    check('Control change never resets consumed opportunity',b.first_damage_offer('native',3,1,controlled=True,qualifying=True),0)
    p=WeaponProfile(15,((4,12),),9,'slashing',10)
    check('Ledger cap replaces only native damage',ledger_attack_profile(p,stats('oracle')),{'attack':15,'dice':((2,8),),'flat':3,'damageType':'slashing','range':10,'ordinaryCrit':True,'multiattack':False,'resourceRiders':False})
    psmall=WeaponProfile(2,((1,4),),-1,'piercing',5)
    check('Weaker native profile remains weaker',ledger_attack_profile(psmall,stats('oracle'))['flat'],-1)

    e=FallenEchoes();commands=CommandLedger('owner');wallet=Wallet(30,actions=3)
    rejects('Disappeared finite summon is not actual death',lambda:e.record_death('owner','ghost','enc',actual_allied_death_in_aura=False))
    e.record_death('owner','ally','enc',actual_allied_death_in_aura=True)
    rejects('Missing weapon profile leaves Strike unpaid',lambda:e.invoke('ally','enc','rest0','strike',stats('paladin'),1,wallet,commands,legal=True,own_turn=True))
    check('Failed Strike does not consume Action/RP',(wallet.rp,wallet.actions,e.uses),(30,3,set()))
    result=e.invoke('ally','enc','rest0','strike',stats('paladin'),1,wallet,commands,legal=True,own_turn=True,profile=p)
    check('Echo cap uses native type/range but bounded attack',(result['attack'],result['dice'],result['flat'],result['damageType'],result['range']),(7,((2,8),),3,'slashing',10))
    check('Immediate Echo leaves BA command available',commands.rounds[1],{'command':False,'damage':True})
    e.record_death('owner','ally','enc',actual_allied_death_in_aura=True)
    rejects('Repeated death does not replenish Echo use',lambda:e.invoke('ally','enc','rest0','guard',stats('paladin'),2,wallet,commands,legal=True,own_turn=True,guard_expiry=ClockMarker(12)))
    result=e.invoke('ally','enc','rest1','guard',stats('paladin'),2,wallet,commands,legal=True,own_turn=True,guard_expiry=ClockMarker(12))
    check('Guard needs no weapon and no offensive debit',(result['acBonus'],2 in commands.rounds),(2,False))
    check('Equal cap keeps original distribution',WeaponProfile(7,((1,16),),3,'cold',30).capped_damage(2,3),(((1,16),),3))

    w=world();s=stats('soldier');sup=Supplies('owner',field_supplies=3,spare_parts=2)
    wall=w.palisade('wall',s,sup,Wallet(),'enc',legal=True)
    check('Base wall snapshots actual CON',(wall.hp,wall.maximum_hp,wall.area_resistance,sup.kits),(8,8,False,1))
    rejects('Intact cap prevents new wall even new encounter',lambda:w.palisade('extra',s,sup,Wallet(),'next',legal=True))
    w.structure_damage('wall',3,1)
    check('Repair uses current M and caps HP',w.repair('wall',replace(s,modifier=8),sup,Wallet(),'enc',2,legal=True),3)
    rejects('Full-HP wall cannot spend repair',lambda:w.repair('wall',s,sup,Wallet(),'new',2,legal=True))
    rejects('Dismantle requires a full minute',lambda:w.dismantle('wall',sup,3,completed_seconds=59,legal=True))
    check('Dismantle returns one kit',w.dismantle('wall',sup,61,completed_seconds=60,legal=True),1)
    rejects('Dismantle does not refund encounter use',lambda:w.palisade('wall2',s,sup,Wallet(),'enc',legal=True))
    wall=w.palisade('wall2',s,sup,Wallet(),'next',legal=True)
    sup.completed_rest(completed=True,carpentry=True)
    check('Rest sets kits2 without resetting walls/counters',(sup.kits,wall.hp,sup.deployments['next']),(2,8,1))
    check('Dismantle at kit cap produces no surplus',w.dismantle('wall2',sup,62,completed_seconds=60,legal=True),0)
    rejects('Destroyed/dismantled structure cannot become real body',lambda:w.physical.register_corpse(Corpse('fake','wall2','humanoid')))
    rejects('Object IDs cannot be reused as summons',lambda:w.physical.fresh('wall2'))
    tier=stats('soldier',level=13,constitution=-7);sup=Supplies('owner');w=world()
    a=w.palisade('a',tier,sup,Wallet(),'enc',legal=True);bwall=w.palisade('b',tier,sup,Wallet(),'enc',legal=True)
    check('TierII minimum applied before double',(a.hp,a.area_resistance),(2,True))
    sup.completed_rest(completed=True,carpentry=True)
    rejects('Level down preserves walls but blocks overcap build',lambda:w.palisade('c',replace(tier,level=12),sup,Wallet(),'next',legal=True))
    check('Existing walls remain intact after cap rejection',(a.state,bwall.state),('intact','intact'))
    w.structure_damage('a',2,1)
    check('Destroyed wall grants no kit refund',sup.kits,2)
    rejects('Zero HP cannot be repaired',lambda:w.repair('a',tier,Supplies('owner',spare_parts=1),Wallet(),'repair',1,legal=True))
    check('Destroyed wall grants no Palisade benefit',w.palisade_benefits('a','owner',1,adjacent=True,brace_geometry=True),{'holdAC':0,'holdSaves':0,'braceFlatDR':0})
    check('Intact wall grants geometry-certified benefits',w.palisade_benefits('b','owner',1,adjacent=True,brace_geometry=True),{'holdAC':1,'holdSaves':1,'braceFlatDR':2})
    rejects('Turret hit does not receive Palisade Synergy',lambda:w.synergy('b',tier,1,'turn',adjacent=True,own_ranged_weapon_hit=False))
    check('Own actual ranged hit receives one S',w.synergy('b',tier,1,'turn',adjacent=True,own_ranged_weapon_hit=True),2)
    rejects('Second shot same own turn cannot repeat Synergy',lambda:w.synergy('b',tier,1,'turn',adjacent=True,own_ranged_weapon_hit=True))
    w=world();sup=Supplies('owner',field_supplies=2);q=w.quick_deploy('q',s,sup,0,ClockMarker(18),Wallet(),use_key='quick1',legal=True)
    rejects('Illegal replacement does not remove previous cover',lambda:w.quick_deploy('q2',s,sup,1,ClockMarker(19),Wallet(),use_key='quick2',legal=False))
    check('Old cover remains on invalid replacement',q.state,'intact')
    q2=w.quick_deploy('q2',s,sup,1,ClockMarker(19),Wallet(),use_key='quick2',legal=True)
    check('Real refreshed use replaces cover without supply refund',(q.state,q2.state,sup.field_supplies),('replaced','intact',0))
    check('Quick cover is no Palisade',w.palisade_benefits('q2','owner',2,adjacent=True,brace_geometry=True)['holdAC'],0)
    rejects('Quick cover cannot receive Palisade repair',lambda:w.repair('q2',s,Supplies('owner',spare_parts=1),Wallet(),'enc',2,legal=True))
    w=world();ts=w.turrets(('one',),s,0,ClockMarker(18),Wallet(),use_key='turret1',legal=True)
    more=w.turrets(('two','three'),s,0,ClockMarker(18),Wallet(),use_key='real-refresh',legal=True)
    check('Per-use one/two is not a global turret cap',len(w.physical.creatures),3)
    check('Turret defense snapshot',(ts[0].hp,ts[0].ac,ts[0].speed),(20,16,0))
    check('Turret attack follows current original Soldier',ts[0].attack_profile(stats('soldier',pb=6,dexterity=5,modifier=5))['attack'],11)
    check('Turret defense does not follow later attack stats',(ts[0].hp,ts[0].ac),(20,16))
    rejects('Turret cannot borrow controller stats',lambda:ts[0].attack_profile(stats('soldier',owner='other')))
    rejects('Turrets do not gain Choir group command',lambda:w.command('two',('one','two'),1,1,Wallet(),CommandLedger('owner'),regular=True,legal=True,capable=True))
    rejects('Empty deployment cannot spend use',lambda:w.turrets((),s,0,ClockMarker(18),Wallet(),use_key='empty',legal=True))
    w.expire(18);check('Turret expiry is administrative, no corpse',(ts[0].state,w.physical.corpses),('ended',{}))
    check('Named protections are three non-HP effects',len(ZONES),3)

    scout=SpiritScout.summon(stats('oracle'),'message',0,ClockMarker(600),Wallet(),use_key='scout',legal_timed_route=True)
    scout.arrive_and_perform(300,['observed name'],legal_direct_observations=True)
    check('Message delivery continues only for return',(scout.state,scout.delivered_message),('returning',True))
    rejects('No remote scout report',lambda:scout.return_report(400,actually_returned=False))
    check('Expiry cannot telepathically upload report',scout.return_report(600,actually_returned=True),[])
    check('Already delivered message survives scout expiry',scout.expire(600)['messageAlreadyDelivered'],True)
    scout=SpiritScout.summon(stats('oracle'),'observe',0,ClockMarker(600),Wallet(),use_key='scout',legal_timed_route=True)
    scout.arrive_and_perform(30,['real sight'],legal_direct_observations=True)
    check('Actual return reports once and ends task',(scout.return_report(60,actually_returned=True),scout.state),(['real sight'],'ended'))
    rejects('Ended scout cannot report twice',lambda:scout.return_report(61,actually_returned=True))
    rejects('Uncertified instantaneous route not invented',lambda:SpiritScout.summon(stats('oracle'),'observe',0,ClockMarker(600),Wallet(),use_key='x',legal_timed_route=False))
    rejects('Scout duration cannot exceed ten minutes',lambda:SpiritScout.summon(stats('oracle'),'observe',0,ClockMarker(601),Wallet(),use_key='x',legal_timed_route=True))
    rejects('Canonical S cannot exceed four',lambda:stats(scale=5))
    rejects('Canonical M cannot be zero',lambda:stats(modifier=0))

    report={'status':'PASS','checks':len(checks),'scope':'Selected remaining80+5 lifecycle/command/object/guard interfaces; not full cards or runtime','results':checks}
    (ROOT/'docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"PASS {len(checks)} targeted remaining lifecycle checks")


if __name__=='__main__':main()

```

## docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json
SHA256 a2326638dc555bba6a85005a6e2afa9fc44db1ef69b136639f8db09012a82f10
```
{
  "status": "PASS",
  "checks": 124,
  "scope": "Selected remaining80+5 lifecycle/command/object/guard interfaces; not full cards or runtime",
  "results": [
    {
      "name": "Choir insufficient RP is atomic",
      "result": "PASS"
    },
    {
      "name": "Failed Choir leaves all resources and bodies",
      "result": "PASS"
    },
    {
      "name": "Four Choir rolls consume one shared command",
      "result": "PASS"
    },
    {
      "name": "Choir shared command/offense committed",
      "result": "PASS"
    },
    {
      "name": "Fanatic exact attack profile",
      "result": "PASS"
    },
    {
      "name": "Four legal hits heal four even zero actual damage",
      "result": "PASS"
    },
    {
      "name": "Fanatic hit cannot replay with new event ID",
      "result": "PASS"
    },
    {
      "name": "No second same-round offensive command",
      "result": "PASS"
    },
    {
      "name": "Sealed zero settles explosion permanently",
      "result": "PASS"
    },
    {
      "name": "Normal zero makes one gated independent burst",
      "result": "PASS"
    },
    {
      "name": "Ending snapshots survivors in creation order",
      "result": "PASS"
    },
    {
      "name": "Burst position does not drift",
      "result": "PASS"
    },
    {
      "name": "Repeated expiry never repeats burst",
      "result": "PASS"
    },
    {
      "name": "No finite corpses",
      "result": "PASS"
    },
    {
      "name": "Known Choir cannot be relabeled real corpse",
      "result": "PASS"
    },
    {
      "name": "Output suppression alone cannot end Choir",
      "result": "PASS"
    },
    {
      "name": "All four ending bursts can exist independently",
      "result": "PASS"
    },
    {
      "name": "Extra turn cannot issue ordinary command",
      "result": "PASS"
    },
    {
      "name": "Invalid attached attack cannot generate healing",
      "result": "PASS"
    },
    {
      "name": "Invalid attached order loses offense",
      "result": "PASS"
    },
    {
      "name": "Attached order cannot replay",
      "result": "PASS"
    },
    {
      "name": "Too-old corpse rejected before payment",
      "result": "PASS"
    },
    {
      "name": "Rejected corpse mode leaves body",
      "result": "PASS"
    },
    {
      "name": "Thrall consumes single physical body",
      "result": "PASS"
    },
    {
      "name": "Thrall NEW melee-only profile",
      "result": "PASS"
    },
    {
      "name": "Ended thrall never returns corpse",
      "result": "PASS"
    },
    {
      "name": "Spent Ritual cannot also buy another mode",
      "result": "PASS"
    },
    {
      "name": "Finite thrall cannot become corpse fuel",
      "result": "PASS"
    },
    {
      "name": "Bone servant profile",
      "result": "PASS"
    },
    {
      "name": "Unbound consumes each distinct corpse",
      "result": "PASS"
    },
    {
      "name": "Reserved attacker cannot sacrifice before attack",
      "result": "PASS"
    },
    {
      "name": "Failed attack does not refund local mode",
      "result": "PASS"
    },
    {
      "name": "Another servant may intercept without offense debit",
      "result": "PASS"
    },
    {
      "name": "One attack cannot consume second interceptor",
      "result": "PASS"
    },
    {
      "name": "Second interception refusal preserves servant",
      "result": "PASS"
    },
    {
      "name": "Other controller cannot source-sacrifice servant",
      "result": "PASS"
    },
    {
      "name": "Miss has no interception window",
      "result": "PASS"
    },
    {
      "name": "Created servants excluded from existing-undead snapshot",
      "result": "PASS"
    },
    {
      "name": "Existing member gets current S",
      "result": "PASS"
    },
    {
      "name": "Lost control suspends existing buff",
      "result": "PASS"
    },
    {
      "name": "Regained control restores same member only",
      "result": "PASS"
    },
    {
      "name": "No replacement member",
      "result": "PASS"
    },
    {
      "name": "First damage offers one flat DR",
      "result": "PASS"
    },
    {
      "name": "Losing flat DR arbitration still consumes opportunity",
      "result": "PASS"
    },
    {
      "name": "Numbered round permits next DR opportunity",
      "result": "PASS"
    },
    {
      "name": "Buff expires on original deadline",
      "result": "PASS"
    },
    {
      "name": "Bone expiry grants no usable corpses",
      "result": "PASS"
    },
    {
      "name": "Other source extra Action blocks willing Ledger atomically",
      "result": "PASS"
    },
    {
      "name": "Failed extra-Action request leaves Oracle budget",
      "result": "PASS"
    },
    {
      "name": "Willing command spends canonical target cap",
      "result": "PASS"
    },
    {
      "name": "Withdrawn consent cancels with no forced substitute",
      "result": "PASS"
    },
    {
      "name": "Willing attack retains native regular Action",
      "result": "PASS"
    },
    {
      "name": "Hostile order reserves next-round offense",
      "result": "PASS"
    },
    {
      "name": "Reserved future offense blocks other source",
      "result": "PASS"
    },
    {
      "name": "Hostile order cannot resolve in issuance round",
      "result": "PASS"
    },
    {
      "name": "Control loss cancels pending future reservation",
      "result": "PASS"
    },
    {
      "name": "Cancelled reservation releases only offense",
      "result": "PASS"
    },
    {
      "name": "First hostile attack replaces actual regular Action",
      "result": "PASS"
    },
    {
      "name": "Hard denial shared across later applications",
      "result": "PASS"
    },
    {
      "name": "Later failed save gives only soft fallback",
      "result": "PASS"
    },
    {
      "name": "Extra end cannot tick Ledger",
      "result": "PASS"
    },
    {
      "name": "Successful subsequent save ends control",
      "result": "PASS"
    },
    {
      "name": "Ended Ledger has no soft fallback",
      "result": "PASS"
    },
    {
      "name": "Ledger interception is assignment not replay",
      "result": "PASS"
    },
    {
      "name": "Application-wide interception cannot repeat",
      "result": "PASS"
    },
    {
      "name": "Native agency/death prevention cannot be bypassed",
      "result": "PASS"
    },
    {
      "name": "Inactive source does not consume first-damage chance",
      "result": "PASS"
    },
    {
      "name": "Reactivated source may take first eligible event",
      "result": "PASS"
    },
    {
      "name": "Control change never resets consumed opportunity",
      "result": "PASS"
    },
    {
      "name": "Ledger cap replaces only native damage",
      "result": "PASS"
    },
    {
      "name": "Weaker native profile remains weaker",
      "result": "PASS"
    },
    {
      "name": "Disappeared finite summon is not actual death",
      "result": "PASS"
    },
    {
      "name": "Missing weapon profile leaves Strike unpaid",
      "result": "PASS"
    },
    {
      "name": "Failed Strike does not consume Action/RP",
      "result": "PASS"
    },
    {
      "name": "Echo cap uses native type/range but bounded attack",
      "result": "PASS"
    },
    {
      "name": "Immediate Echo leaves BA command available",
      "result": "PASS"
    },
    {
      "name": "Repeated death does not replenish Echo use",
      "result": "PASS"
    },
    {
      "name": "Guard needs no weapon and no offensive debit",
      "result": "PASS"
    },
    {
      "name": "Equal cap keeps original distribution",
      "result": "PASS"
    },
    {
      "name": "Base wall snapshots actual CON",
      "result": "PASS"
    },
    {
      "name": "Intact cap prevents new wall even new encounter",
      "result": "PASS"
    },
    {
      "name": "Repair uses current M and caps HP",
      "result": "PASS"
    },
    {
      "name": "Full-HP wall cannot spend repair",
      "result": "PASS"
    },
    {
      "name": "Dismantle requires a full minute",
      "result": "PASS"
    },
    {
      "name": "Dismantle returns one kit",
      "result": "PASS"
    },
    {
      "name": "Dismantle does not refund encounter use",
      "result": "PASS"
    },
    {
      "name": "Rest sets kits2 without resetting walls/counters",
      "result": "PASS"
    },
    {
      "name": "Dismantle at kit cap produces no surplus",
      "result": "PASS"
    },
    {
      "name": "Destroyed/dismantled structure cannot become real body",
      "result": "PASS"
    },
    {
      "name": "Object IDs cannot be reused as summons",
      "result": "PASS"
    },
    {
      "name": "TierII minimum applied before double",
      "result": "PASS"
    },
    {
      "name": "Level down preserves walls but blocks overcap build",
      "result": "PASS"
    },
    {
      "name": "Existing walls remain intact after cap rejection",
      "result": "PASS"
    },
    {
      "name": "Destroyed wall grants no kit refund",
      "result": "PASS"
    },
    {
      "name": "Zero HP cannot be repaired",
      "result": "PASS"
    },
    {
      "name": "Destroyed wall grants no Palisade benefit",
      "result": "PASS"
    },
    {
      "name": "Intact wall grants geometry-certified benefits",
      "result": "PASS"
    },
    {
      "name": "Turret hit does not receive Palisade Synergy",
      "result": "PASS"
    },
    {
      "name": "Own actual ranged hit receives one S",
      "result": "PASS"
    },
    {
      "name": "Second shot same own turn cannot repeat Synergy",
      "result": "PASS"
    },
    {
      "name": "Illegal replacement does not remove previous cover",
      "result": "PASS"
    },
    {
      "name": "Old cover remains on invalid replacement",
      "result": "PASS"
    },
    {
      "name": "Real refreshed use replaces cover without supply refund",
      "result": "PASS"
    },
    {
      "name": "Quick cover is no Palisade",
      "result": "PASS"
    },
    {
      "name": "Quick cover cannot receive Palisade repair",
      "result": "PASS"
    },
    {
      "name": "Per-use one/two is not a global turret cap",
      "result": "PASS"
    },
    {
      "name": "Turret defense snapshot",
      "result": "PASS"
    },
    {
      "name": "Turret attack follows current original Soldier",
      "result": "PASS"
    },
    {
      "name": "Turret defense does not follow later attack stats",
      "result": "PASS"
    },
    {
      "name": "Turret cannot borrow controller stats",
      "result": "PASS"
    },
    {
      "name": "Turrets do not gain Choir group command",
      "result": "PASS"
    },
    {
      "name": "Empty deployment cannot spend use",
      "result": "PASS"
    },
    {
      "name": "Turret expiry is administrative, no corpse",
      "result": "PASS"
    },
    {
      "name": "Named protections are three non-HP effects",
      "result": "PASS"
    },
    {
      "name": "Message delivery continues only for return",
      "result": "PASS"
    },
    {
      "name": "No remote scout report",
      "result": "PASS"
    },
    {
      "name": "Expiry cannot telepathically upload report",
      "result": "PASS"
    },
    {
      "name": "Already delivered message survives scout expiry",
      "result": "PASS"
    },
    {
      "name": "Actual return reports once and ends task",
      "result": "PASS"
    },
    {
      "name": "Ended scout cannot report twice",
      "result": "PASS"
    },
    {
      "name": "Uncertified instantaneous route not invented",
      "result": "PASS"
    },
    {
      "name": "Scout duration cannot exceed ten minutes",
      "result": "PASS"
    },
    {
      "name": "Canonical S cannot exceed four",
      "result": "PASS"
    },
    {
      "name": "Canonical M cannot be zero",
      "result": "PASS"
    }
  ]
}

```

## docs/mechanics/REMAINING_LIFECYCLE_SOURCE_VALIDATION.json
SHA256 2722a48835f45f7aed4911e413f503ad7c249da70af01a698d80dc17d265a8f2
```
{
  "result": "PASS",
  "status": "UNREVIEWED_SOURCE_INTEGRITY_ONLY",
  "exactClassRecords": 80,
  "originalCandidates": 74,
  "semanticSupplements": 6,
  "frozenSharedParagraphs": 5,
  "scope": "Exact preserved source equality/hash; no interpretation/implementation approval.",
  "issues": []
}

```

## Shared exact Wallet/CommandLedger
@dataclass
class Wallet:
    rp: int=0
    actions: int=1
    bonus_action: bool=True
    reaction: bool=True
    used: set=field(default_factory=set)

    def validate(self,rp=0,action=None,use_key=None):
        integer(rp,'RP cost',0)
        integer(self.rp,'available RP',0)
        if action not in (None,'action','bonus','reaction'):
            raise SpellRuleError('Unknown action payment')
        if self.rp<rp:raise SpellRuleError('Insufficient RP')
        if action=='action' and self.actions<1:raise SpellRuleError('No Action')
        if action=='bonus' and not self.bonus_action:raise SpellRuleError('No Bonus Action')
        if action=='reaction' and not self.reaction:raise SpellRuleError('No Reaction')
        if use_key is not None:
            identity(use_key)
            if use_key in self.used:raise SpellRuleError('Source use already spent in this scope')

    def pay(self,rp=0,action=None,use_key=None):
        self.validate(rp,action,use_key)
        self.rp-=rp
        if action=='action':self.actions-=1
        if action=='bonus':self.bonus_action=False
        if action=='reaction':self.reaction=False
        if use_key is not None:self.used.add(use_key)


@dataclass
class CommandLedger:
    """Owner-wide numbered-round ledger, including multiclass companions."""
    owner: str
    rounds: dict=field(default_factory=dict)
    reservations: dict=field(default_factory=dict)

    def validate(self,round_number,mode,wallet,*,rp=0,tinker=False,regular=True):
        integer(round_number,'numbered round',1)
        if mode not in ('support','attack','control','gadget-sync','decoy'):
            raise SpellRuleError('Not a shared command mode')
        command=mode in ('support','attack','control')
        offensive=mode!='support'
        if tinker and command and not regular:
            raise SpellRuleError('Tinker command requires a regular turn')
        entry=self.rounds.get(round_number,{'command':False,'damage':False})
        if command and entry['command']:raise SpellRuleError('Round companion command spent')
        if offensive and (entry['damage'] or round_number in self.reservations):
            raise SpellRuleError('Round companion offense spent or reserved')
        if mode=='gadget-sync' and rp!=1:raise SpellRuleError('Gadget Sync costs 1 RP')
        if mode=='decoy' and rp!=0:raise SpellRuleError('Decoy trigger has no RP cost')
        wallet.validate(rp,'bonus' if command else None)
        return command,offensive,entry

    def reserve(self,issuance_round,resolution_round,order_id,wallet):
        """Reflective order pays current BA, reserves future offense atomically."""
        identity(order_id)
        integer(resolution_round,'resolution round',issuance_round)
        command,_,entry=self.validate(issuance_round,'support',wallet)
        future=self.rounds.get(resolution_round,{'command':False,'damage':False})
        if future['damage'] or resolution_round in self.reservations or order_id in self.reservations.values():
            raise SpellRuleError('Future offense already committed or duplicate order')
        wallet.pay(action='bonus')
        self.rounds[issuance_round]={'command':True,'damage':entry['damage']}
        self.reservations[resolution_round]=order_id

    def settle(self,resolution_round,order_id,*,executed):
        if self.reservations.get(resolution_round)!=order_id:
            raise SpellRuleError('No matching offensive reservation')
        del self.reservations[resolution_round]
        if executed:
            entry=self.rounds.setdefault(resolution_round,{'command':False,'damage':False})
            entry['damage']=True

    def activate(self,round_number,mode,wallet,*,rp=0,tinker=False,regular=True):
        command,damaging,entry=self.validate(round_number,mode,wallet,rp=rp,tinker=tinker,regular=regular)
        wallet.pay(rp,'bonus' if command else None)
        self.rounds[round_number]={
            'command':entry['command'] or command,
            'damage':entry['damage'] or damaging}
        return {'commandSpent':command,'damagingActivationSpent':damaging}




## Shared exact dependency class Corpse:
class Corpse:
    """One physical body identity, with current corpse eligibility kept separate."""
    body_id: str
    creature_id: str
    creature_type: str
    goblinoid: bool=False
    real_original: bool=True
    body_state: str='corpse'
    consumed_by: str | None=None

    def __post_init__(self):
        identity(self.body_id);identity(self.creature_id)
        require(self.body_state in ('living','corpse','consumed','removed'),'Unknown physical body state')

    @property
    def available(self):return self.body_state=='corpse'

    def eligible(self,profile,*,pact=False):
        return self.available and self.real_original and (
            self.creature_type=='humanoid' or (pact and self.creature_type=='fiend')) and (
            profile!='goblin-thrall' or self.goblinoid)




## Shared exact dependency class HardDenialLedger:
class HardDenialLedger:
    """Adapter over the canonical ALL-feature (encounter, character, target) set."""
    used: set=field(default_factory=set)

    def available(self,encounter,owner,target):
        for v in (encounter,owner,target):identity(v)
        return (encounter,owner,target) not in self.used

    def spend(self,encounter,owner,target):
        require(self.available(encounter,owner,target),'Shared hard-denial allowance spent')
        self.used.add((encounter,owner,target))




## Shared exact dependency class CreatureWorld:
class CreatureWorld:
    def __init__(self):
        self.creatures={};self.corpses={};self.reflective={}
        self.reservations={};self.auto_used=set();self.closed_checkpoints=set()
        self.orders={};self.completed_rests={};self.ranger_deaths={}
        self.noncorpse_identities=set()  # Exact external created-object integrations.

    def fresh(self,ident):
        identity(ident)
        require(ident not in self.creatures and ident not in self.noncorpse_identities,'Creature/object identity already exists')

    def register_corpse(self,corpse):
        require(corpse.body_id not in self.corpses,'Body identity already registered')
        require(not any(c.creature_id==corpse.creature_id for c in self.corpses.values()),'Fragments/repeated death are not new bodies')
        require(corpse.real_original,'Summoned/copied/raised remains are not corpse fuel')
        require(corpse.creature_id not in self.noncorpse_identities,'Known created object cannot become real body fuel')
        known=self.creatures.get(corpse.creature_id)
        require(known is None or known.life_kind=='ranger','Known created companion cannot become real body fuel')
        self.corpses[corpse.body_id]=corpse

    def consume_body(self,body_id,consumer):
        identity(consumer);corpse=self.corpses[body_id]
        require(corpse.available,'Body already consumed')
        corpse.body_state='consumed';corpse.consumed_by=consumer



## Shared exact ExtraActionClock
class ExtraActionClock:
    spent_rounds: set = field(default_factory=set)

    def spend(self, round_number, *, granted_by_extra_action=False):
        integer(round_number, 'numbered round', 1)
        if granted_by_extra_action or round_number in self.spent_rounds:
            raise SpellRuleError('Extra full Action cap or recursive grant')
        self.spent_rounds.add(round_number)



