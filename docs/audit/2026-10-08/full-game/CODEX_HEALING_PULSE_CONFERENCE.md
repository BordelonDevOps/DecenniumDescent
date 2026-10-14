# Healing pulses, zones and upkeep conference

Codex → Calibration Review. Maximum-HP exact review closure is recorded (58 sources;60 checks/909 states); Rewind historical damage predicate and Flesh Ascendant runtime alias caveat retained. No original sources changed.

Next bounded discussion:100 lexical class candidates below. Many are guards, earlier-reviewed regeneration/flat bonuses, or non-healing zones. Please classify EVERY supplied ID in a compact table, distinguish native passive recurrence, action-paid pulses, target-start funded windows, finite installments, already-reviewed guards and excluded single-use/repair effects. Do not invent a uniform three-pulse limit for passives. This is source discussion before implementation. Keep reply under18,000 characters; concise per-ID table plus shared rulings is best.

Resolve these source-sensitive questions with explicit NEW labels where needed:

1. Exact initial and later payments/actions: Lifewell's FIRST pulse already costs BA+1RP beyond activation; Renewal/Briar/Harmony/Restoration first included then BA+1RP. Oracle engine26 vs Garden/Song/Finals and Paladin engine11 need precise distinct schedules.
2. Funded window versus per-target cost: Garden target-start healing uses activation window1, source-next-regular-start1RC for windows2/3? Crown Restored target-start maximum3 and Final included payments? Song exactlyactivation+nextregularstart, nottargetstart? Eternal Bloom fixed3 reserve installments.
3. Define source regular-turn/target-start windows, missed upkeep endpoint (Lifewell source-end explicit), extra turns, source incapacity/unconsciousness/concentration loss, suppression, and clocks outside initiative. Do paid BA zones end immediately if skipped, or at own end and cannot resume? Does max3 count scheduled opportunities regardless actual gain?
4. Target identities: fixed at activation for Oracleengine26/Lifewell explicitchosenallies; other pulses repick≤3 when no fixed wording? How do chosen targets leaving/re-entering, death, enemy classification, zone movement and per-creature/round ledgers work? A blocked heal/zero actualgain still spends its paid opportunity; no replacement after dice/blocked outcome?
5. Renewal upgrade4thpulse, Echo Totem half arithmetic/shared parent upkeep/lifetime and same-name nonstack. Are parent and Echo same pulse for once/round and target cap, how choose strongest coverage without double healing, and what happens if parent destroyed? Totem movement/other BAs compete; cannot create entry healing. Keep non-Renewal Totem Pulse distinct.
6. Eternal Bloom reserve snapshot: three integer installments/remainders, missing/outside/dead targets lose scheduled share rather than bank? Suppression does not extend clocks; source-independent target clocks? One floor perally distinct from installments. Garden first-entry/start cure is independent of HP gain and differs from healing pulses.
7. Cleric passive Aura of Grace and Mutation regen retain source cadence/cost rather than genericthreecap. EfficientPowerCells/MechOverdrive extend duration only where allowed, never RestorationField3pulses or free recharges; disabled devices do not pause clocks.
8. Propose coherent per-instance record and eligibility/budget commit ordering for source/target/round/pulse IDs; retain previous healing graph, strongest flat modifiers, blocked-gain cure independence and exact clocks. No broad copy/companion/control runtime closure.

Please expose missing supporting source evidence rather than guessing; candidate extraction is lexical, not proof every zone in all game catalogs was supplied.

## Exact source procedures

### cleric.base.consecrated-ground

data/public/class_playtests/cleric.json

{
  "name": "Consecrated Ground",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Passive",
  "frequency": "Always",
  "effect": "Consecrated Ground. Tags: rite, healing, passive. Whenever one of your healing Rites restores HP to a living creature standing in terrain created by your Consecrate feature, that creature regains S additional HP. Apply this once per creature per Rite pulse; it is flat healing and is not itself another healing trigger."
}

### cleric.base.radiance.radiance

data/public/class_playtests/cleric.json

{
  "name": "Radiance",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Permanent",
  "frequency": "Automatic only if Radiance was selected",
  "effect": "Invocation Path — Radiance. Tags: invocation, radiance, healing. Once on each of your turns when one of your Rites restores HP to at least one living creature, choose one creature healed by that Rite. It regains S additional HP and may immediately end either Frightened or Poisoned on itself."
}

### cleric.base.echoes.echoes

data/public/class_playtests/cleric.json

{
  "name": "Echoes",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "One original target within 30 feet",
  "duration": "Until start of your next regular turn",
  "frequency": "At most one pending Echoes-path repeat",
  "effect": "Invocation Path — Echoes. Tags: invocation, echoes. Once on each of your turns after a Smite or Rite produces rolled immediate damage or healing, store one original target and that raw dice total. At the start of your next regular turn, if the target is legal, repeat floor(raw dice total/10), minimum 1 for a positive total, as the same damage or healing type. This repeat carries no conditions, resources or triggers."
}

### cleric.base.sacred-chant

data/public/class_playtests/cleric.json

{
  "name": "Sacred Chant",
  "activation": "Action",
  "cost": "1 RP to start; 0 RP maintenance",
  "rangeAndTarget": "Self; audible 15-foot prayer aura",
  "duration": "Concentration, maximum 3 Cleric turns",
  "frequency": "At will while RP remains",
  "effect": "Sacred Chant. Tags: chant, sustained, conviction. Pulse on start and once when maintained on each later regular turn with a Bonus Action. Under the base feature, the third pulse generates 1 Conviction. Only a real encounter can generate Conviction this way. Maintenance itself does not otherwise heal, damage or grant Conviction."
}

### cleric.arch.aura-of-faith

data/public/class_playtests/cleric.json

{
  "name": "Aura of Faith",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Allies within 15 feet who can perceive you",
  "duration": "Passive while conscious",
  "frequency": "Always",
  "effect": "Aura of Faith. Tags: aura, bishop. Allies in the aura gain +1 on saving throws. Whenever your Rite restores HP to an ally in the aura, that ally also regains 1 additional HP. Multiple Aura of Faith bonuses do not stack."
}

### cleric.arch.divine-invocation

data/public/class_playtests/cleric.json

{
  "name": "Divine Invocation",
  "activation": "Action",
  "cost": "2 Conviction + 3 RP",
  "rangeAndTarget": "Mode-dependent; maximum 60 feet",
  "duration": "Instantaneous unless mode states otherwise",
  "frequency": "Recharge 3 rounds",
  "effect": "Divine Invocation. Tags: invocation, bishop. Use only your selected Invocation Path. Radiance: up to 3 allies within 30 feet each regain S d8+M HP; one may end Frightened or Poisoned. Judgment: one enemy within 60 feet makes a Wisdom save, taking (S+1)d8 radiant on failure or half on success; failure also applies Judged for 2 rounds. Renewal: up to 2 allies within 30 feet each regain S d8+M HP and 5 Stamina. Flame: creatures in a 15-foot cone make Dexterity saves, taking (S+1)d8 fire on failure or half on success; failed targets also take 1d6 fire at the start of their next turn. Veil: up to 3 allies within 30 feet can see invisible/ethereal creatures within 30 feet and gain advantage on saves against illusions for 3 rounds. Echoes: choose one eligible Smite or Rite you resolved this turn or previous regular turn and one original target within 30 feet; repeat 50% of its immediate unmodified rolled damage or healing dice, rounded down once, minimum 1 for a positive source, with no copied conditions, resources or triggers."
}

### cleric.hero.saint.aura-of-grace

data/public/class_playtests/cleric.json

{
  "name": "Aura of Grace",
  "activation": "Triggered and passive",
  "cost": "1 RP per healing pulse",
  "rangeAndTarget": "Living allies within 15 feet",
  "duration": "Passive during real encounters",
  "frequency": "Healing once/own regular turn; critical reduction once/ally/round",
  "effect": "Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing."
}

### cleric.hero.priest.balanced-scales

data/public/class_playtests/cleric.json

{
  "name": "Balanced Scales",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Living creatures healed by your Cleric features",
  "duration": "Until start of your next regular turn",
  "frequency": "At most once per marked ally per round",
  "effect": "Balanced Scales. Tags: priest, healing, retaliation. After you restore HP to a living ally, mark it until the start of your next regular turn. The first enemy to damage that ally during the mark takes S + M radiant damage. The retaliation is not an attack, cannot critically hit and cannot recursively trigger another Balanced Scales event."
}

### cleric.hero.priest.word-of-power

data/public/class_playtests/cleric.json

{
  "name": "Word of Power",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One creature within 30 feet",
  "duration": "Instantaneous",
  "frequency": "Recharge 2 rounds",
  "effect": "Word of Power. Tags: priest, divine. Choose one mode. Mercy: one willing living creature regains S d8+M HP. Rebuke: one Undead or Fiend makes a Constitution save, taking (S+1)d8 radiant on failure or half on success; failure also removes its Reaction until the start of its next turn. Command: one other hostile creature makes a Wisdom save; failure knocks it Prone and removes its Reaction until the start of its next turn. No mode changes beliefs, loyalty or ideology."
}

### cleric.hero.priest.cosmic-equilibrium

data/public/class_playtests/cleric.json

{
  "name": "Cosmic Equilibrium",
  "activation": "Action",
  "cost": "7 RP",
  "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
  "duration": "Concentration, maximum 3 rounds",
  "frequency": "1/short rest",
  "effect": "Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other."
}

### cleric.hero.cultist.sanguine-rite

data/public/class_playtests/cleric.json

{
  "name": "Sanguine Rite",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self and one ally within 30 feet",
  "duration": "Instantaneous",
  "frequency": "At most once on each of your turns",
  "effect": "Sanguine Rite. Tags: cultist, rite, healing. When one of your Rites deals damage to at least one enemy, choose one living ally within 30 feet. That ally regains HP equal to half the actual damage dealt to one chosen damaged enemy, rounded down, maximum S+M HP. This healing cannot trigger Sanguine Rite again."
}

### cleric.hero.cultist.blasphemous-tongue

data/public/class_playtests/cleric.json

{
  "name": "Blasphemous Tongue",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Enemies affected by your Sacrament",
  "duration": "Until the next Sacrament pulse or effect end",
  "frequency": "Once per target per pulse",
  "effect": "Blasphemous Tongue. Tags: cultist, sacrament, doomed. At each pulse of your Sacrament, each enemy affected by that pulse makes a Wisdom save. On failure it becomes Doomed until the next pulse. While Doomed, HP healing it receives is reduced by S+M, minimum 0, and each positive timed buff on it counts down one additional round at the end of its turn. Repeated failures refresh rather than stack."
}

### cleric.hero.cultist.zealot-s-touch

data/public/class_playtests/cleric.json

{
  "name": "Zealot's Touch",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Healing-over-time Rites you control",
  "duration": "Passive",
  "frequency": "Always",
  "effect": "Zealot's Touch. Tags: cultist, rite, necrotic. When starting a Rite whose printed pulse would restore HP over multiple turns, you may designate a hostile creature instead of a healing recipient. At each applicable pulse that enemy makes a Wisdom save. On failure it takes necrotic damage equal to the Rite's rolled healing dice; on success it takes half. Flat healing bonuses are not converted. The enemy receives no healing."
}

### cleric.hero.cultist.dark-sacrament

data/public/class_playtests/cleric.json

{
  "name": "Dark Sacrament",
  "activation": "Action",
  "cost": "3 Conviction + 5 RP to start; 1 RP maintenance",
  "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
  "duration": "Concentration, maximum 3 Cleric turns",
  "frequency": "Recharge 4 rounds",
  "effect": "Dark Sacrament. Tags: cultist, sacrament, rite, sustained, zone. On start and each paid maintenance pulse, roll S d6 once. Up to three enemies in the zone make Constitution saves, taking that roll as necrotic damage on failure or half on success. If at least one enemy takes damage, up to three living allies in the zone each regain floor(roll/2)+M HP. Maximum 3 pulses. The Conviction expenditure can vent Dissonance once."
}

### cleric.hero.cultist.zealot-s-fervor

data/public/class_playtests/cleric.json

{
  "name": "Zealot's Fervor",
  "activation": "Bonus Action",
  "cost": "2 Conviction",
  "rangeAndTarget": "Self",
  "duration": "3 rounds",
  "frequency": "1/short rest",
  "effect": "Zealot's Fervor. Tags: cultist, stance. For 3 rounds, once on each of your turns add S to one damage roll from a Cleric feature and S to one HP-healing roll from a Cleric feature. While the Fervor lasts, your AC is reduced by 1. The Conviction expenditure is not a Rite or Invocation and therefore does not vent Dissonance by itself."
}

### crimson-agent.engine[2]

data/public/class_playtests/crimson-agent.json

{
  "text": "Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation."
}

### crimson-agent.hero.bloodweaver.hemostasis

data/public/class_playtests/crimson-agent.json

{
  "name": "Hemostasis",
  "activation": "Passive",
  "cost": "1 additional RP per application",
  "rangeAndTarget": "One willing living ally in range of your Bleed application",
  "duration": "3 target turns",
  "frequency": "Once/own turn",
  "effect": "You may replace a new Bleed application on that ally with healing 1d4 at start of its next 3 turns. Pay extra RP even if original application was free. One such healing effect per target; it cannot spread, detonate, generate BG or trigger healing loops."
}

### crimson-agent.hero.bloodweaver.lifewell

data/public/class_playtests/crimson-agent.json

{
  "name": "Lifewell",
  "activation": "Action",
  "cost": "4 RP; all BG, minimum 3",
  "rangeAndTarget": "Up to 3 living allies within 15 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "1/long rest",
  "effect": "Spend K BG. At start and on each of your next 2 turns, use Bonus Action and pay 1 RP to pulse healing: each chosen ally still within 15 ft regains 1d8+K HP. Without maintenance it ends at turn end. Total 3 pulses; no triggers create more BG."
}

### dragoon.engine[4]

data/public/class_playtests/dragoon.json

{
  "text": "Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard."
}

### druid.engine[4]

data/public/class_playtests/druid.json

{
  "text": "Transformation reserves prevent unlimited replacement HP: at long rest record Buffer Reserve=2 L+M and Form Surge Reserve=PB. A form giving temporary HP draws that many from Buffer Reserve, up to remaining amount, with normal nonstacking; never real healing. A form special described once/transformation also spends 1 Form Surge and cannot be refreshed by resuming the form. Form Surge refills only long rest. Forms cannot grant free casts, RP or shift uses. Auras affect at most 3 enemies and once per enemy per round; retaliation once/round total; ongoing riders refresh, never stack. Entering a legal Shapeshift clears the Refrain counter and remembered repeated-spell name, as the protected source contract requires. It does not reduce accumulated Dissonance. Natural attacks do not clear Refrain."
}

### mirrorsage.hero.mirror-mage.reality-fracture

data/public/class_playtests/mirrorsage.json

{
  "name": "Reality Fracture",
  "activation": "Action",
  "cost": "6 RP; 1 long-rest use",
  "rangeAndTarget": "Fixed 10 ft-radius zone within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "1/long rest",
  "effect": "While you stand inside, once/turn add 1d6 to one Echo damage/healing amount or impose-1 on one target's Echo save. Choose before resolving. No free releases, random recasts, resource refunds or extra targets."
}

### mirrorsage.hero.shattered-one.fractured-dominion

data/public/class_playtests/mirrorsage.json

{
  "name": "Fractured Dominion",
  "activation": "Bonus Action",
  "cost": "8 RP; 1 long-rest use",
  "rangeAndTarget": "Self",
  "duration": "2 of your turns",
  "frequency": "1/long rest",
  "effect": "Your first damage release on each of these 2 turns adds one half-dice component against a DIFFERENT enemy within 10 ft of an original target. Same package and shared copy cap; excludes healing/control. Never recursively copies a copy or adds a release action."
}

### monk.base.crane-stance-support

data/public/class_playtests/monk.json

{
  "name": "Crane Stance (Support)",
  "activation": "Passive",
  "cost": "0 for stance; healing costs 1 Ki and 1 RP",
  "rangeAndTarget": "Self; one ally within 15 feet for healing rider",
  "duration": "While active",
  "frequency": "Automatic core stance",
  "effect": "Crane Stance. Tags: stance, support. While unarmored, whenever you move at least 15 feet on your turn, gain +1 AC until the start of your next turn. HP healing you receive from another creature gains +S HP once per round. When you begin an unarmed strike at exactly 5 Ki and hit, spend 1 Ki and 1 RP; you and one living ally within 15 feet each regain S+M HP, at most once per turn."
}

### monk.hero.enlightened-master.breath-of-the-thousand-petals

data/public/class_playtests/monk.json

{
  "name": "Breath of the Thousand Petals",
  "activation": "Action",
  "cost": "5 Ki + 5 RP",
  "rangeAndTarget": "Up to six allies within 20 feet",
  "duration": "Until start of your next regular turn",
  "frequency": "1/long rest; automatic Hero Final",
  "effect": "Final — Breath of the Thousand Petals. Tags: hero, enlightened, final, resurrection, weave. Living or Downed allies in range regain 3 S d8+M HP. Up to two allied creatures that died since the end of your previous regular turn return to life at 1 HP if their bodies can sustain life. Until the start of your next turn, affected living allies cannot be reduced below 1 HP by damage, though instant-death effects still function. It removes no Wounds and cannot revive the same creature twice."
}

### monk.hero.enlightened-master.circle-of-harmony

data/public/class_playtests/monk.json

{
  "name": "Circle of Harmony",
  "activation": "Action",
  "cost": "2 Ki + 3 RP to start; 1 RP maintenance",
  "rangeAndTarget": "10-foot-radius fixed zone centered within 30 feet",
  "duration": "Concentration, maximum 3 Monk turns",
  "frequency": "Recharge 4 rounds",
  "effect": "Circle of Harmony. Tags: hero, enlightened, healing, zone, weave, sustained. On start and each paid Bonus Action maintenance pulse, up to three living allies in the zone regain S d6+M HP. Maximum 3 pulses. A creature receives this named effect at most once per round. It removes no Wounds and cannot restore the dead."
}

### monk.hero.enlightened-master.transcendent-meditation

data/public/class_playtests/monk.json

{
  "name": "Transcendent Meditation",
  "activation": "Action",
  "cost": "3 Ki + 4 RP",
  "rangeAndTarget": "Self and up to three allies within 15 feet",
  "duration": "Concentration, maximum 3 Monk turns",
  "frequency": "1/short rest",
  "effect": "Transcendent Meditation. Tags: hero, enlightened, healing, weave, sustained. On start and at the start of each of your next two regular turns while concentration holds, each target regains S d6 HP. You regain 1 Ki on the second pulse only, never above 5. Targets must remain within 15 feet. This finite healing cannot be restarted until the short-rest use refreshes."
}

### oracle.engine[26]

data/public/class_playtests/oracle.json

{
  "text": "Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones."
}

### oracle.supplement.spiral-touched.spiral-touched-boon-iii

data/public/class_playtests/oracle.json

{
  "name": "Spiral-Touched — Boon III",
  "activation": "Triggered at 0 HP",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Until start of next regular turn",
  "frequency": "1/long rest",
  "effect": "1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations."
}

### oracle.supplement.wound-eater.wound-eater-boon-iv

data/public/class_playtests/oracle.json

{
  "name": "Wound Eater — Boon IV",
  "activation": "Bonus Action; start-of-turn pulses",
  "cost": "2 RC start; 1 RC per later pulse",
  "rangeAndTarget": "Up to three living enemies within 10 feet",
  "duration": "Concentration; at most three pulses",
  "frequency": "One aura; once/target/round",
  "effect": "pay 2 RC as a Bonus Action to activate a 10-foot drain aura, requiring concentration for at most three pulses; pay 1 RC before each pulse after the first or end it. You may suppress it freely. During a real encounter, at the start of your turn up to three meaningful living enemies in the aura takes S necrotic damage; regain HP equal to the total actually dealt, capped at S+M per turn."
}

### oracle.supplement.burning-blood.burning-blood-boon-v

data/public/class_playtests/oracle.json

{
  "name": "Burning Blood — Boon V",
  "activation": "Bonus Action",
  "cost": "0",
  "rangeAndTarget": "Self; up to three enemies/allies within 15 feet",
  "duration": "Three rounds",
  "frequency": "1/long rest; one pulse/target/round",
  "effect": "1/long rest as a Bonus Action become a living pyre for 3 rounds. At the start of each hostile creature's turn within 15 feet it takes S d6 fire damage. Once per your turn when at least one enemy takes fire damage from you, regain 1d6 HP, capped at S+M HP per turn. Allies in the aura gain fire resistance and hidden/invisible creatures within 10 feet cannot benefit from mundane darkness or visual concealment against creatures illuminated by your pyre."
}

### oracle.supplement.consumed.consumed-boon-v

data/public/class_playtests/oracle.json

{
  "name": "Consumed — Boon V",
  "activation": "Bonus Action",
  "cost": "0",
  "rangeAndTarget": "Self and up to three allies within 10 feet",
  "duration": "Three rounds",
  "frequency": "1/long rest",
  "effect": "1/long rest as a Bonus Action fully embody your Mystery for 3 rounds. Gain immunity to the theme damage type, +2 on Revelation attack rolls and Revelation save DC, and add S to one Revelation damage or healing roll each turn. Allies within 10 feet gain +1 AC. Visible transformation cannot be suppressed during this embodiment."
}

### oracle.supplement.bones.rotting-touch

data/public/class_playtests/oracle.json

{
  "name": "Rotting Touch",
  "activation": "Action",
  "cost": "2 RC",
  "rangeAndTarget": "One creature you can touch",
  "duration": "Maximum 3 rounds",
  "frequency": "At will while RC remains",
  "effect": "Make a Revelation attack. On hit the target makes a Constitution save. On failure it gains Decay for up to 3 rounds: attacks against it add S damage once per attacker per turn, it takes -1 on saving throws and cannot regain HP. At the end of each turn it repeats the save, ending Decay on success. Corpses within 2 tiles of a Decayed creature cannot be raised while Decay persists. If the target is undead, it also takes 2d6 necrotic damage on the initial hit and you regain half the actual damage dealt, capped at S+M HP. At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack."
}

### oracle.supplement.bones.unfinished-chorus

data/public/class_playtests/oracle.json

{
  "name": "Unfinished Chorus",
  "activation": "Action",
  "cost": "3 RC",
  "rangeAndTarget": "Enemies, controlled undead and corpses within 4 tiles",
  "duration": "2 rounds; Revelation backlash 1 round",
  "frequency": "At will while RC remains",
  "effect": "For 2 rounds, enemies within 4 tiles suffer Dread: -1 on attack rolls and saving throws. Once on each of your turns choose one living enemy in range; it takes 1d6 necrotic damage and you either regain half the actual damage dealt, rounded down, or one living ally within 3 tiles of you regains that amount, maximum S+M HP. Undead you control add S damage to one attack each turn and reduce first damage each round by 1. Corpses in the area cannot be raised while the Chorus lasts. Afterward you are suffering Revelation backlash until end of your next turn: -1 attacks/saves and Speed -5 feet. Choose up to three enemies and three allies. Enemies make Wisdom saves on entry and at the end of each turn, ending their debuff on success. The drain allows a Constitution save for half damage; healing is capped at S+M total per pulse. Concentration and pulse upkeep apply."
}

### oracle.supplement.flame.zealot-s-renewal

data/public/class_playtests/oracle.json

{
  "name": "Zealot's Renewal",
  "activation": "Action",
  "cost": "2 RC",
  "rangeAndTarget": "One living ally within 3 tiles; adjacent enemies",
  "duration": "Instantaneous; fire ward until start of your next turn",
  "frequency": "At will while RC remains",
  "effect": "The ally regains 2 S d8+M HP, then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it. It may end Poisoned or immediately repeat one disease save. Until the start of your next turn it reduces the first fire damage it takes by S. Hostile creatures adjacent to the healed ally take 1d4 fire damage once from scattering embers."
}

### oracle.supplement.flame.first-flame-convergence

data/public/class_playtests/oracle.json

{
  "name": "First Flame Convergence",
  "activation": "Action",
  "cost": "3 RC",
  "rangeAndTarget": "Self and allies within 4 tiles",
  "duration": "2 rounds",
  "frequency": "At will while RC remains",
  "effect": "For 2 rounds, once on each of your turns when a Flame Revelation deals fire damage, add one extra die matching that Revelation's primary damage die to one damage roll. Once per turn when one of your Flame Revelations damages a meaningful hostile creature, one living ally within 4 tiles regains 1d6 HP. Allies within 4 tiles are immune to Frightened. Once per turn when this effect heals an ally, that ally reduces the first damage it takes before your next turn by 1. Zealot's Renewal deals no backlash while Convergence lasts."
}

### oracle.supplement.flame.crown-restored

data/public/class_playtests/oracle.json

{
  "name": "Crown Restored",
  "activation": "Bonus Action",
  "cost": "0 RC",
  "rangeAndTarget": "Self and allies within 5 tiles",
  "duration": "3 rounds",
  "frequency": "1/long rest",
  "effect": "Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap."
}

### oracle.supplement.life.resonant-seed

data/public/class_playtests/oracle.json

{
  "name": "Resonant Seed",
  "activation": "Action",
  "cost": "1 RC",
  "rangeAndTarget": "2-tile-radius fixed zone centered within 4 tiles",
  "duration": "3 rounds",
  "frequency": "At will while RC remains; one Seed zone at a time",
  "effect": "When a living ally starts its turn in the zone, it regains 1d4 HP, at most once per round and for at most three pulses from this use, and may end Frightened or Poisoned on the first pulse it receives. Undead entering or starting their turn in the zone take 1d4 radiant damage once per round and make a Strength save; on failure their Speed is reduced by 1 tile until the end of that turn. Healing requires the paid 1 RC activation and ends after 3 rounds."
}

### oracle.supplement.life.garden-of-restoration

data/public/class_playtests/oracle.json

{
  "name": "Garden of Restoration",
  "activation": "Action",
  "cost": "2 RC",
  "rangeAndTarget": "4-tile-radius fixed zone centered within 5 tiles",
  "duration": "3 rounds",
  "frequency": "At will while RC remains; one Garden at a time",
  "effect": "At the start of each living ally's turn in the Garden, it regains 1d6 HP, maximum three pulses per creature from this use, and gains +1 HP the next time another finite healing effect restores HP before its next turn. The first time each ally enters or starts in a given Garden, it may end Poisoned or immediately repeat one disease save. Undead starting in the Garden take 1d6 radiant damage and make a Wisdom save; on failure they take -1 on attack rolls until the end of that turn."
}

### oracle.supplement.life.verdant-pulse

data/public/class_playtests/oracle.json

{
  "name": "Verdant Pulse",
  "activation": "Passive and Reaction",
  "cost": "0 RC",
  "rangeAndTarget": "Allies you heal; emergency ally within 4 tiles",
  "duration": "Buff until end of ally's next turn; emergency instantaneous",
  "frequency": "Buff once per ally per short rest; emergency 1/encounter",
  "effect": "When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it."
}

### oracle.supplement.life.song-of-mending

data/public/class_playtests/oracle.json

{
  "name": "Song of Mending",
  "activation": "Action",
  "cost": "3 RC",
  "rangeAndTarget": "Living allies within 5 tiles",
  "duration": "2 rounds",
  "frequency": "At will while RC remains",
  "effect": "On activation and at the start of your next regular turn, each living ally still within 5 tiles regains 2d6 HP, for exactly two possible pulses per use. Once during the duration for each ally, when one damage event would reduce it below 1 HP without instant death, it remains at 1 HP instead. When this prevention triggers, that ally may end Frightened or Poisoned and gains +S HP the next time a separate finite healing effect restores HP before Song ends. This removes no Wounds and cannot resurrect."
}

### oracle.supplement.life.life-revelation-mastery

data/public/class_playtests/oracle.json

{
  "name": "Life Revelation Mastery",
  "activation": "Passive",
  "cost": "0 RC",
  "rangeAndTarget": "One eligible known Life Revelation",
  "duration": "Permanent",
  "frequency": "Choose one upgrade at Oracle 15",
  "effect": "Choose one mastery for a Revelation you know. Enhanced Overflowing Light: maximum temporary HP from excess healing becomes 20. Enhanced Garden of Restoration: the first Garden pulse a creature receives may end both Poisoned and one disease that explicitly allows magical curing, rather than only one of those benefits. Enhanced Song of Mending: duration becomes 3 rounds and gains one additional 2d6 healing pulse at the start of your second later regular turn; each ally still receives only one 1-HP death prevention per use."
}

### oracle.supplement.life.eternal-bloom

data/public/class_playtests/oracle.json

{
  "name": "Eternal Bloom",
  "activation": "Action",
  "cost": "0 RC",
  "rangeAndTarget": "5-tile-radius fixed sanctuary centered within 5 tiles",
  "duration": "3 rounds",
  "frequency": "1/long rest",
  "effect": "When Eternal Bloom appears, record each living ally's missing HP while it is inside the zone. Divide that recorded missing HP into three healing installments as evenly as possible, with any remainder assigned to earlier pulses. On activation and at the start of each of your next two regular turns, each qualifying ally still inside regains its next installment; later damage does not increase this reserve. Once per ally during the Bloom, when damage would reduce it to 0 HP without instant death, it remains at 1 HP instead. Allies in the zone have necrotic immunity for the 3 rounds. When the Bloom ends, petals create light obscurement in the zone until the start of your next turn. It removes no Wounds and does not resurrect."
}

### oracle.supplement.time.rewind-wound

data/public/class_playtests/oracle.json

{
  "name": "Rewind Wound",
  "activation": "Action",
  "cost": "2 RC",
  "rangeAndTarget": "One living ally you touch",
  "duration": "Healing instantaneous; protection until start of your next turn",
  "frequency": "At will while RC remains; same damage event can be rewound once",
  "effect": "Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects."
}

### oracle.supplement.time.the-spiral-opens

data/public/class_playtests/oracle.json

{
  "name": "The Spiral Opens",
  "activation": "Action",
  "cost": "0 RC",
  "rangeAndTarget": "Self; one known beneficial Time Revelation or one enemy within 5 tiles",
  "duration": "3 rounds",
  "frequency": "1/long rest",
  "effect": "For 3 rounds, at the start of each of your regular turns choose ONE temporal option, each usable at most once during this Final. ECHO REVELATION: repeat only the immediate numeric damage, healing, movement or buff component of one beneficial Time Revelation you personally resolved during the previous round, paying 0 RC; this copy is not a new Revelation cast, copies no resource restoration, action grant, hard control, condition trigger, Prophecy Trigger or proc. FORCED ECHO: choose one non-player enemy within 5 tiles and one ordinary weapon attack or non-resource movement action it took during its previous turn. The enemy makes a Wisdom save. On failure, during its next turn it must repeat that action pattern if legally possible, but it chooses all legal targets and paths; it spends no limited resources and cannot be forced to harm itself. A player-controlled creature instead, on a failed save, loses its Reaction and must choose either repeat one ordinary non-resource action type from its prior turn or have Speed reduced to 0 until turn end. Allies retain memory of all temporal echoes. This Final never creates more than one additional full Action for any creature in a round. There are only two options in this Final; after using both once, remaining rounds provide only the printed temporal presence, without another echo. An echoed healing amount also pays 1 RC or consumes an unused per-rest healing use; a temporal copy cannot create an uncosted healing reserve."
}

### paladin.engine[11]

data/public/class_playtests/paladin.json

{
  "text": "Sustained Oath spell damage/healing zones use concentration, at most three pulses, and 1 RP upkeep after the first pulse unless a priced card expressly supplies a different finite cadence. Native Oath auras retain their printed passive cadence and target cap. Final auras last their stated finite duration and include their pulses. All hard-denial effects, including compelled Actions, share the common once/source/target/encounter guard; later failures only remove Reactions and reduce Speed by half for one turn."
}

### paladin.hero.lay-on-hands

data/public/class_playtests/paladin.json

{
  "name": "Lay on Hands",
  "activation": "Action",
  "cost": "All remaining Lay on Hands points; minimum 1",
  "rangeAndTarget": "Up to 3 living allies in aura",
  "duration": "Instant",
  "frequency": "1/short rest and pool cost",
  "effect": "Allocate remaining points among targets, at least 1 each; restore 1 HP per point. You may instead allocate 5 points per target to end Poisoned or Frightened. Spend entire pool, cannot multiply it by recipient count, raise the dead or remove Wounds. Oathbreakers instead deal allocated necrotic damage to 3 enemies, CON half, same pool cost."
}

### paladin.supplement.oathbreaker-shared.dread-shelter

data/public/class_playtests/paladin.json

{
  "name": "Dread Shelter",
  "activation": "Bonus Action",
  "cost": "3 RP",
  "rangeAndTarget": "Self",
  "duration": "Concentration, 1 minute",
  "frequency": "At will while RP remains",
  "effect": "New rank 2 Forbidden spell. Gain 2 S+M temporary HP on casting and 1 flat DR against weapon damage for duration. No recurring temp HP pulse or healing."
}

### paladin.supplement.oathbreaker-shared.desecrated-ground

data/public/class_playtests/paladin.json

{
  "name": "Desecrated Ground",
  "activation": "Action; Bonus Action maintenance",
  "cost": "7 RP start; 1 RP per later pulse",
  "rangeAndTarget": "10 ft radius fixed point 30 ft, up to 3 enemies",
  "duration": "Concentration, maximum 3 pulses",
  "frequency": "Recharge 4",
  "effect": "New rank 4 Forbidden spell. Initial and each paid pulse CON save for S d6 necrotic, half success. A failed target receives 1 less HP per healing die until start of your next turn. Penalty cannot make healing negative or stack with another same-stat reduction."
}

### paladin.supplement.oathbreaker-shared.last-reproach

data/public/class_playtests/paladin.json

{
  "name": "Last Reproach",
  "activation": "Reaction after an enemy damages an ally",
  "cost": "10 RP",
  "rangeAndTarget": "That enemy 60 ft; one living ally in your aura",
  "duration": "Instant",
  "frequency": "1/short rest",
  "effect": "New rank 5 Forbidden spell. Enemy WIS save for 3 S d8 necrotic, half success; ally regains S d8 HP after triggering damage. Does not revive dead or undo conditions. Uses ordinary spell strain and your Reaction."
}

### paladin.supplement.oath-of-mercy.aura-of-mercy

data/public/class_playtests/paladin.json

{
  "name": "Aura of Mercy",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to 3 chosen allies in your Oath aura",
  "duration": "While conscious and target remains in aura",
  "frequency": "Choose targets at start of each turn",
  "effect": "The first time each round a selected ally receives HP healing from a finite or paid effect, add S HP. Each selected ally also reduces the first necrotic damage it takes each round by S. These benefits do not stack with another Aura of Mercy from the same source."
}

### paladin.supplement.oath-of-mercy.blessing-of-the-meek

data/public/class_playtests/paladin.json

{
  "name": "Blessing of the Meek",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "One living ally within 30 feet",
  "duration": "Healing instantaneous; AC bonus until start of your next regular turn",
  "frequency": "At will while RP remains",
  "effect": "The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules."
}

### paladin.supplement.oath-of-mercy.grace-eternal

data/public/class_playtests/paladin.json

{
  "name": "Grace Eternal",
  "activation": "Bonus Action",
  "cost": "0 RP",
  "rangeAndTarget": "Up to 3 allies in your Oath aura",
  "duration": "Until start of your next regular turn",
  "frequency": "1/long rest",
  "effect": "Apply Miracle Veil to up to 3 allies in your aura without spending its short-rest use or RP. Once during this Veil for each affected ally, if damage would reduce it to 0 HP, it remains at 1 HP and immediately regains 2d8 HP. It also gains necrotic resistance until the end of its next turn. During Grace Eternal you may use Lay on Hands once without an Action, but must still spend points from your current Lay on Hands pool and may target only one creature."
}

### paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression

data/public/class_playtests/paladin.json

{
  "name": "Healing Suppression",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
  "duration": "While conscious and target remains in aura",
  "frequency": "Choose targets at start of each turn",
  "effect": "HP healing received by each selected creature is halved, rounded down. Temporary HP, damage prevention and resurrection are not healing for this effect. This suppression cannot reduce healing below 0 or convert prevented healing into damage."
}

### paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate

data/public/class_playtests/paladin.json

{
  "name": "Exsanguinate",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Up to 3 living creatures in your Oath aura",
  "duration": "Instantaneous",
  "frequency": "1/short rest; replaces Signature Power use",
  "effect": "Each target makes a Constitution save, taking 2 S d8 necrotic damage on failure or half on success. Regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. Undead and constructs are unaffected and cannot be used to generate healing."
}

### paladin.supplement.oath-of-flame.phoenix-rebirth

data/public/class_playtests/paladin.json

{
  "name": "Phoenix Rebirth",
  "activation": "Reaction",
  "cost": "10 RP",
  "rangeAndTarget": "One living ally in your Oath aura reduced to 0 HP",
  "duration": "Revival instantaneous; fire shield until end of target's next turn",
  "frequency": "Once per combat per ally",
  "effect": "Trigger when the ally reaches 0 HP without being killed outright. It immediately regains HP equal to half its maximum, rounded down, minimum 1. Until the end of its next turn it has fire resistance. Once during that duration when a creature within melee reach damages it with a melee attack, that attacker takes 2d6 fire damage. Phoenix Rebirth removes no Wounds and cannot restore a creature destroyed beyond recovery."
}

### paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood

data/public/class_playtests/paladin.json

{
  "name": "Death Touch — Blighting Blood",
  "activation": "Action",
  "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss",
  "rangeAndTarget": "One creature within melee reach; its occupied space",
  "duration": "Damage instantaneous; blighted space until start of your next regular turn",
  "frequency": "At will while Lay on Hands points remain; terrain rider once per turn",
  "effect": "Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared points and blight the target's space until the start of your next turn. The first hostile creature other than the original target that enters or starts its turn in that space takes S necrotic damage. The patch creates no corpse, healing or resource trigger."
}

### paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified

data/public/class_playtests/paladin.json

{
  "name": "Scorch the Sanctified",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to 3 enemies in your Oath aura",
  "duration": "While conscious and target remains in aura",
  "frequency": "Choose targets at start of each turn",
  "effect": "Selected enemies cannot regain HP from passive regeneration. At the start of each selected enemy's turn it makes a Charisma save. On failure, one temporary beneficial magical effect on it chosen by the Director from eligible non-innate effects is suppressed until the start of its next turn. Immunities, class engines, permanent traits and attunement are never suppressed."
}

### paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word

data/public/class_playtests/paladin.json

{
  "name": "Scorch the Sanctified — Blasphemous Word",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Up to 3 creatures in your Oath aura",
  "duration": "Instantaneous; suppressed effect until end of next turn",
  "frequency": "1/short rest; replaces Signature Power use",
  "effect": "Each target makes a Constitution save, taking S d6 fire plus S d6 necrotic damage on failure or half on success. A failing target also has one eligible temporary beneficial spell or regeneration effect suppressed until the end of its next turn. You may knowingly include allies among the targets; the effect offers them no protection."
}

### paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura

data/public/class_playtests/paladin.json

{
  "name": "Lifeleech Bloom Aura",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to 3 enemies in your Oath aura",
  "duration": "While conscious and target remains in aura",
  "frequency": "Choose targets and one damage type at start of each turn",
  "effect": "Selected enemies cannot regain HP from passive regeneration. Also choose acid, cold, fire, lightning, necrotic, poison, radiant or thunder. A selected enemy's resistance to that chosen type is suppressed while it remains selected in the aura; immunity is never suppressed."
}

### paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom

data/public/class_playtests/paladin.json

{
  "name": "Lifeleech Bloom",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Up to 3 living creatures or plant creatures in your Oath aura",
  "duration": "Instantaneous",
  "frequency": "1/short rest; replaces Signature Power use",
  "effect": "Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. You regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. You may include willing allies among the targets, but they receive no protection and cannot be reduced below 1 HP by this Blasphemous Word. Constructs and ordinary unattended plants provide no healing."
}

### paladin.supplement.oath-of-grief.dirge-of-passage

data/public/class_playtests/paladin.json

{
  "name": "Dirge of Passage",
  "activation": "Bonus Action",
  "cost": "0 RP",
  "rangeAndTarget": "Memories of up to 2 fallen allies; creatures in your Oath aura",
  "duration": "2 rounds",
  "frequency": "1/long rest",
  "effect": "For 2 rounds maintain two Final Vigil memories simultaneously and gain both selected benefits. Up to three selected hostile undead in your aura take an additional S radiant damage from your first damaging Paladin feature each round and cannot regain HP. Living allies in your aura gain +2 on death saves. No spirit gains its own turn, resources, spellcasting or complete former statistics. This flat rider replaces blanket damage vulnerability and never doubles a whole attack."
}

### paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura

data/public/class_playtests/paladin.json

{
  "name": "Dirge of Ruin Aura",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
  "duration": "While conscious and target remains in aura",
  "frequency": "Choose targets at start of each turn",
  "effect": "Selected living creatures cannot be returned from death while inside the aura, and HP healing they receive is reduced by S+M, minimum 0. This never converts healing into damage and cannot retroactively reverse a resurrection completed before the creature entered the aura."
}

### paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin

data/public/class_playtests/paladin.json

{
  "name": "Dirge of Ruin",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Up to 3 creatures in your Oath aura",
  "duration": "Damage instantaneous; healing block until end of next turn",
  "frequency": "1/short rest; replaces Signature Power use",
  "effect": "Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. A failing target cannot regain HP until the end of its next turn. This does not prevent temporary HP or remove healing already received."
}

### paladin.supplement.oath-of-the-martyr-king.crown-of-embers

data/public/class_playtests/paladin.json

{
  "name": "Crown of Embers",
  "activation": "Bonus Action",
  "cost": "2 RP",
  "rangeAndTarget": "Up to 3 allies in your Oath aura",
  "duration": "Until start of your next regular turn",
  "frequency": "1/short rest",
  "effect": "Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself."
}

### paladin.supplement.oath-of-the-martyr-king.burden-shared

data/public/class_playtests/paladin.json

{
  "name": "Burden Shared",
  "activation": "Reaction when an ally takes damage",
  "cost": "5 RP",
  "rangeAndTarget": "Triggering ally and up to two other willing allies in your aura",
  "duration": "One damage event",
  "frequency": "While RP remains",
  "effect": "After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round."
}

### paladin.supplement.oath-of-the-martyr-king.throne-s-grace

data/public/class_playtests/paladin.json

{
  "name": "Throne’s Grace",
  "activation": "Action",
  "cost": "7 RP",
  "rangeAndTarget": "Self and up to three allies in your aura",
  "duration": "Concentration; three rounds",
  "frequency": "While RP remains",
  "effect": "Your Lay on Hands and touch-range Paladin healing can target selected allies anywhere in your current aura with clear line of effect. Normal activation, pool/RP costs, rank gates and use limits remain. Rolled healing you grant them adds 1 HP per die, maximum S+M additional HP per effect; pool-point healing adds no dice bonus. Selected allies gain +1 on death saves. The spell itself restores no HP."
}

### paladin.supplement.oath-of-the-martyr-king.crown-undying

data/public/class_playtests/paladin.json

{
  "name": "Crown Undying",
  "activation": "Bonus Action",
  "cost": "0 RP",
  "rangeAndTarget": "Up to three selected allies in your aura",
  "duration": "Three rounds; no concentration",
  "frequency": "1/long rest",
  "effect": "For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool."
}

### paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura

data/public/class_playtests/paladin.json

{
  "name": "Crownshatter Decree Aura",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to three selected enemies in your aura",
  "duration": "While conscious and in aura",
  "frequency": "Each incoming healing event",
  "effect": "A selected enemy receives HP healing only if it has taken actual damage from a meaningful hostile creature since the start of its previous regular turn. If it has not, that healing restores 0 HP; its source still spends its normal costs. Temporary HP, stabilization and resurrection are not HP healing for this restriction. This aura never creates damage, transfers healing or reverses recovery that already resolved."
}

### ranger.engine[5]

data/public/class_playtests/ranger.json

{
  "text": "Chosen Hero grants a sixth Arrow at 11. Warder Nature's Wrath: ranged attack weapon+S d6 piercing; up to 2 allies within 10 ft gain M temporary HP (finite mitigation, not repeatable real healing). Stalker Phantom: two ranged attacks against different aligned targets within 60 ft, each weapon damage, no extra dice; one Arrow activation. Outrider Corruption: place 10 ft-radius zone within 60 ft, concentration until start next turn; up to 3 enemies entering/starting there take S d4 necrotic once each, CON half. Arrow copies cannot generate extra attacks, resources or permanent terrain changes."
}

### ranger.hero.warder.living-pulse

data/public/class_playtests/ranger.json

{
  "name": "Living Pulse",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "Self in natural terrain",
  "duration": "Start of your regular turn",
  "frequency": "Once/turn",
  "effect": "You may pay 1 RP to regain 2 HP. Does not trigger when Downed or incapacitated, cannot exceed maximum and never counts as another healing spell. Replaces unlimited passive regeneration with a finite cost."
}

### ranger.hero.warder.healing-briar

data/public/class_playtests/ranger.json

{
  "name": "Healing Briar",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "Fixed 10 ft-radius natural-ground zone within 30 ft; 3 allies/pulse",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "On start heal 1d8+M per chosen living ally; on next 2 turns Bonus Action+1 RP repeats pulse. Maximum 3 pulses; no passive additional entry healing and no Wound removal."
}

### shaman.engine[1]

data/public/class_playtests/shaman.json

{
  "text": "Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack."
}

### shaman.engine[2]

data/public/class_playtests/shaman.json

{
  "text": "On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction."
}

### shaman.arch.extended-totem-duration

data/public/class_playtests/shaman.json

{
  "name": "Extended Totem Duration",
  "activation": "Passive",
  "cost": "0; full upkeep for extra Renewal pulse",
  "rangeAndTarget": "One of your totems",
  "duration": "Maximum 4 of your turns",
  "frequency": "Continuous",
  "effect": "Totems last 1 extra turn. Renewal may have a fourth pulse only if you pay Bonus Action+1 RP on that turn; no fifth pulse and no automatic free healing. Concentration still required."
}

### shaman.arch.spirit-cache

data/public/class_playtests/shaman.json

{
  "name": "Spirit Cache",
  "activation": "Triggered",
  "cost": "1 short-rest use",
  "rangeAndTarget": "One flask/to-tem effect you directly used",
  "duration": "Stored until encounter end",
  "frequency": "1/short rest",
  "effect": "Store its profile, not an active copy. On a later turn use normal Action/Bonus Action and pay all RP and a new flask unit or full totem cost to repeat it. Add 1d6 to one numerical damage/heal amount; no copy of refund/limited use."
}

### shaman.arch.totem-pulse

data/public/class_playtests/shaman.json

{
  "name": "Totem Pulse",
  "activation": "Passive",
  "cost": "1 RP optional",
  "rangeAndTarget": "Up to 3 creatures inside newly placed non-healing totem",
  "duration": "Instant",
  "frequency": "Once/turn",
  "effect": "On placement pay 1 RP: allies gain M temporary HP OR enemies make DEX save for S affinity damage, half on success. No immediate second Renewal healing pulse, no repeat from moving the totem."
}

### shaman.arch.spirit-saturation

data/public/class_playtests/shaman.json

{
  "name": "Spirit Saturation",
  "activation": "Triggered",
  "cost": "1 long-rest use",
  "rangeAndTarget": "One non-Renewal totem you place",
  "duration": "Normal duration",
  "frequency": "1/long rest",
  "effect": "Waive its 2 RP placement cost once. Still use Action, concentration, capacity and any added costs. Cannot create a healing totem or be cached/refunded to generate more free casts."
}

### shaman.hero.theurgist.echo-totem

data/public/class_playtests/shaman.json

{
  "name": "Echo Totem",
  "activation": "Triggered",
  "cost": "1 additional RP",
  "rangeAndTarget": "Adjacent empty space within 5 ft of newly placed totem",
  "duration": "Same remaining duration",
  "frequency": "Once/placement",
  "effect": "Create a weak echo anchor of that totem. It counts toward capacity; if no space in capacity, cannot create it. Its radius 10 ft and numerical bonuses/healing are half, rounded down. Shared concentration/upkeep and same-name nonstacking prevent double healing."
}

### shaman.hero.bloodcaller.blight-totem

data/public/class_playtests/shaman.json

{
  "name": "Blight Totem",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "Totem within 30 ft; 15 ft aura affecting all creatures",
  "duration": "3 of your turns",
  "frequency": "Ordinary totem capacity/concentration",
  "effect": "HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing."
}

### shaman.hero.bloodcaller.blood-curse

data/public/class_playtests/shaman.json

{
  "name": "Blood Curse",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "One living enemy within 60 ft",
  "duration": "3 target turns",
  "frequency": "Recharge 3",
  "effect": "CON save or Bleed 1d4 necrotic at start of each of next 3 turns. Action plus successful Medicine check against class DC ends it; magical healing also permits an immediate CON save to end. Never permanently unhealable; no repeated stacking."
}

### shaman.supplement.elder-spirit-accord-new-hero-capstone

data/public/class_playtests/shaman.json

{
  "name": "Elder Spirit Accord — new Hero capstone",
  "activation": "Triggered",
  "cost": "1 long-rest use",
  "rangeAndTarget": "Your chosen Hero ultimate",
  "duration": "One activation",
  "frequency": "1/long rest",
  "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast."
}

### soldier.engine[4]

data/public/class_playtests/soldier.json

{
  "text": "Base 1–2, Commander Arch 3–9, then Champion/Artillerist/Tyrant Hero 10–20. Palisade 5 is automatic; Intercepting Shot has minimum 6 and Fortify Zone 9. Other cards require selection. There is no source automatic Arch capstone. At 20 gain the new Final Command below, clearly a playtest addition. No spell or sustained technique may be used to obtain infinite ammunition, structures, actions or permanent healing."
}

### thief.hero.blackguard.exsanguinate

data/public/class_playtests/thief.json

{
  "name": "Exsanguinate",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "Self; bleeding enemy within 15 ft",
  "duration": "Instant",
  "frequency": "Once/own turn",
  "effect": "At start of your regular turn with a hostile bleeding enemy nearby you may pay 1 RP to regain S HP. No multiplying by enemy count or healing while incapacitated; not an ordinary spell or Dissonance-generating technique."
}

### tinker.engine[7]

data/public/class_playtests/tinker.json

{
  "text": "Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets."
}

### tinker.base.field-repair

data/public/class_playtests/tinker.json

{
  "name": "Field Repair",
  "activation": "Action",
  "cost": "1 RP",
  "rangeAndTarget": "One construct/device touched",
  "duration": "Instant",
  "frequency": "Recharge 2",
  "effect": "Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses."
}

### tinker.hero.artificer.efficient-power-cells

data/public/class_playtests/tinker.json

{
  "name": "Efficient Power Cells",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your nonhealing deployables",
  "duration": "Deployment",
  "frequency": "Continuous",
  "effect": "A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration."
}

### tinker.hero.artificer.nano-aegis-drone

data/public/class_playtests/tinker.json

{
  "name": "Nano-Aegis Drone",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Your drone within 15 ft",
  "duration": "3 rounds",
  "frequency": "Recharge 4",
  "effect": "Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode."
}

### tinker.hero.artificer.repair-pulse

data/public/class_playtests/tinker.json

{
  "name": "Repair Pulse",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "Upto 3 friendly devices within 30 ft",
  "duration": "Instant; AC until start next turn",
  "frequency": "1/short rest",
  "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets."
}

### tinker.hero.artificer.restoration-field

data/public/class_playtests/tinker.json

{
  "name": "Restoration Field",
  "activation": "Action",
  "cost": "3 RP start; 1 RP maintenance; one slot",
  "rangeAndTarget": "10 ft radius within 30 ft",
  "duration": "Maximum 3 pulses",
  "frequency": "Recharge 4",
  "effect": "Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells."
}

### tinker.supplement.mech-overdrive

data/public/class_playtests/tinker.json

{
  "name": "Mech Overdrive",
  "activation": "Triggered on deploying a device",
  "cost": "1 long-rest use plus original deployment cost",
  "rangeAndTarget": "One of your newly deployed devices",
  "duration": "Until encounter end, maximum 1 minute",
  "frequency": "1/long rest; automatic Hero capstone",
  "effect": "Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment."
}

### warrior.hero.ironskin.regenerative-mutation

data/public/class_playtests/warrior.json

{
  "name": "Regenerative Mutation",
  "activation": "Passive",
  "cost": "Spend healing amount from Mutation Recovery Reserve",
  "rangeAndTarget": "Self",
  "duration": "While at least one mutation is active in a real encounter",
  "frequency": "Once at the start of each regular turn",
  "effect": "Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve."
}

### warrior.hero.ironskin.cellular-reconstruction

data/public/class_playtests/warrior.json

{
  "name": "Cellular Reconstruction",
  "activation": "Action",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Until start of your next regular turn, then instantaneous recovery",
  "frequency": "1/long rest",
  "effect": "Cellular Reconstruction. Enter stasis until the start of your next regular turn: your Speed becomes 0, you cannot take Actions, Bonus Actions or Reactions, and attacks against you have advantage. At the start of your next turn regain 3d8 + M HP and end Poisoned plus one mundane or magical disease that does not explicitly require a special cure. This removes no Wounds and cannot function while dead."
}

### warrior.hero.dreadspawn.pain-empowerment

data/public/class_playtests/warrior.json

{
  "name": "Pain Empowerment",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "While below maximum HP",
  "frequency": "Always",
  "effect": "Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects."
}

### warrior.supplement.primed

data/public/class_playtests/warrior.json

{
  "name": "Primed",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "One active mutation each turn",
  "duration": "While BT remains at least 2",
  "frequency": "Once per turn",
  "effect": "Enhance one active mutation's numeric benefit for the turn: +1 to one AC, DR, attack, save or flat damage bonus; +5 feet to one movement/reach bonus; or +1 damage/healing to one mutation-generated roll. Primed never increases duration, targets, immunity or resource generation."
}

### warrior.supplement.transcendent

data/public/class_playtests/warrior.json

{
  "name": "Transcendent",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Until start of your next regular turn",
  "frequency": "1/encounter total, regardless of trigger",
  "effect": "At Warrior 12+, the first time this encounter you cross 100% Brutality Progress or reach stored BT 4, activate all equipped mutations until start of your next regular turn. No serum profile or immediate healing trigger is granted. This is one total pulse, never a permanent BT 4 concurrency increase. At end choose active mutations up to normal limit, with their original remaining durations; others become dormant."
}

### warrior.supplement.bloodthick-node

data/public/class_playtests/warrior.json

{
  "name": "Bloodthick Node",
  "activation": "Passive while active",
  "cost": "One mutation slot; serum activation",
  "rangeAndTarget": "Self",
  "duration": "While active during a real encounter",
  "frequency": "Once at start of each regular turn",
  "effect": "Regain HP equal to current BT, maximum 3 HP per turn or 4 with Stack Overflow. No healing occurs outside a real encounter and it removes no Wounds. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve."
}

### warrior.supplement.rapid-coagulation

data/public/class_playtests/warrior.json

{
  "name": "Rapid Coagulation",
  "activation": "Passive while active",
  "cost": "One mutation slot; serum activation",
  "rangeAndTarget": "Self",
  "duration": "While active during a real encounter",
  "frequency": "Start of turn",
  "effect": "If you did not move during your previous turn, regain 2 HP at the start of your current turn. This does not function outside a real encounter. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve."
}

### warrior.supplement.bio-stabilizer

data/public/class_playtests/warrior.json

{
  "name": "Bio-Stabilizer",
  "activation": "Passive",
  "cost": "Feat choice",
  "rangeAndTarget": "Self",
  "duration": "Permanent",
  "frequency": "Always",
  "effect": "While at least two mutations are active, Bloodthick Node heals 1 additional HP on each of its valid encounter-only regeneration pulses."
}

### wizard.engine[10]

data/public/class_playtests/wizard.json

{
  "text": "ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn."
}

### wizard.hero.necromancer.infernal-pact-quest-based-unlock

data/public/class_playtests/wizard.json

{
  "name": "Infernal Pact (Quest-based unlock)",
  "activation": "Bonus Action",
  "cost": "3 RP",
  "rangeAndTarget": "One creature within 60 feet",
  "duration": "Maximum 3 rounds",
  "frequency": "1/long rest; quest-gated",
  "effect": "Infernal Pact — Gravebrand. Tags: hero, necromancer, infernal, necrotic, dark-content. This card can be selected only after completing the campaign's Infernal Pact quest and its dark-trauma check-in. Mark one creature. At the start of each of its turns it makes a Constitution save; on failure it takes 1d6 necrotic damage and you regain HP equal to the actual damage dealt, maximum S+M; success ends Gravebrand. Gravebrand ignores necrotic resistance but not immunity. While you possess this Pact, Corpse Harvest and Auto-Raise may also treat Fiend corpses as eligible; other creature types remain ineligible."
}
