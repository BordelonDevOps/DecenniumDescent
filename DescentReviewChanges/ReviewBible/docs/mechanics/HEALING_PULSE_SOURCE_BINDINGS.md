# Recurring healing and zone source register

**REVIEWED / reference-VALIDATED; bounded100+6-source interface —100 supplied records.**

Original sources remain unchanged. Inclusion can mean a guard or exclusion; review status applies only to the stated role.

[Source integrity](HEALING_PULSE_SOURCE_VALIDATION.json)

## cleric.base.consecrated-ground

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/cleric.json / cleric.base.consecrated-ground · SHA256 f4b71531332377e2ca7b3ea4b4646e46df57b264d265473b30abfbc2f86bdb55.

**name:** Consecrated Ground

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Passive

**frequency:** Always

**effect:** Consecrated Ground. Tags: rite, healing, passive. Whenever one of your healing Rites restores HP to a living creature standing in terrain created by your Consecrate feature, that creature regains S additional HP. Apply this once per creature per Rite pulse; it is flat healing and is not itself another healing trigger.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: +S once/creature/Rite pulse after actual restoration; not child heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.base.radiance.radiance

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/cleric.json / cleric.base.radiance.radiance · SHA256 35f3566de386bca746618537d03e3561d74b8a35e1633c073ddef7e77f507821.

**name:** Radiance

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic only if Radiance was selected

**effect:** Invocation Path — Radiance. Tags: invocation, radiance, healing. Once on each of your turns when one of your Rites restores HP to at least one living creature, choose one creature healed by that Rite. It regains S additional HP and may immediately end either Frightened or Poisoned on itself.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Once/own turn after Rite actually restores HP.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.base.echoes.echoes

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI/COPY

Source data/public/class_playtests/cleric.json / cleric.base.echoes.echoes · SHA256 66a5241b20fcfd81448ba872aa1cd3fd5b59cadb5eb540467e9f5bdaf14cb155.

**name:** Echoes

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One original target within 30 feet

**duration:** Until start of your next regular turn

**frequency:** At most one pending Echoes-path repeat

**effect:** Invocation Path — Echoes. Tags: invocation, echoes. Once on each of your turns after a Smite or Rite produces rolled immediate damage or healing, store one original target and that raw dice total. At the start of your next regular turn, if the target is legal, repeat floor(raw dice total/10), minimum 1 for a positive total, as the same damage or healing type. This repeat carries no conditions, resources or triggers.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One delayed source-next-start numeric repeat; no triggers/resources.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.base.sacred-chant

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X/MP

Source data/public/class_playtests/cleric.json / cleric.base.sacred-chant · SHA256 4053fdc1a1a48cc3fdb2accfef3abad95e23fce696a30321c714a2934e4a66b2.

**name:** Sacred Chant

**activation:** Action

**cost:** 1 RP to start; 0 RP maintenance

**rangeAndTarget:** Self; audible 15-foot prayer aura

**duration:** Concentration, maximum 3 Cleric turns

**frequency:** At will while RP remains

**effect:** Sacred Chant. Tags: chant, sustained, conviction. Pulse on start and once when maintained on each later regular turn with a Bonus Action. Under the base feature, the third pulse generates 1 Conviction. Only a real encounter can generate Conviction this way. Maintenance itself does not otherwise heal, damage or grant Conviction.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Nonhealing sustained 3-pulse chant; start + later BA maintenance.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.arch.aura-of-faith

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/cleric.json / cleric.arch.aura-of-faith · SHA256 56acc5fb191e255889bc45374d73b2ba55798a82fe5b5ab193731ab3d57ad448.

**name:** Aura of Faith

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Allies within 15 feet who can perceive you

**duration:** Passive while conscious

**frequency:** Always

**effect:** Aura of Faith. Tags: aura, bishop. Allies in the aura gain +1 on saving throws. Whenever your Rite restores HP to an ally in the aura, that ally also regains 1 additional HP. Multiple Aura of Faith bonuses do not stack.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: +1 after actual Rite HP restoration in aura.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.arch.divine-invocation

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I/COPY

Source data/public/class_playtests/cleric.json / cleric.arch.divine-invocation · SHA256 7dae262ad987193dc14e8ce21c6d45c5a2ad7d0f2008377d0217f5959e2848c2.

**name:** Divine Invocation

**activation:** Action

**cost:** 2 Conviction + 3 RP

**rangeAndTarget:** Mode-dependent; maximum 60 feet

**duration:** Instantaneous unless mode states otherwise

**frequency:** Recharge 3 rounds

**effect:** Divine Invocation. Tags: invocation, bishop. Use only your selected Invocation Path. Radiance: up to 3 allies within 30 feet each regain S d8+M HP; one may end Frightened or Poisoned. Judgment: one enemy within 60 feet makes a Wisdom save, taking (S+1)d8 radiant on failure or half on success; failure also applies Judged for 2 rounds. Renewal: up to 2 allies within 30 feet each regain S d8+M HP and 5 Stamina. Flame: creatures in a 15-foot cone make Dexterity saves, taking (S+1)d8 fire on failure or half on success; failed targets also take 1d6 fire at the start of their next turn. Veil: up to 3 allies within 30 feet can see invisible/ethereal creatures within 30 feet and gain advantage on saves against illusions for 3 rounds. Echoes: choose one eligible Smite or Rite you resolved this turn or previous regular turn and one original target within 30 feet; repeat 50% of its immediate unmodified rolled damage or healing dice, rounded down once, minimum 1 for a positive source, with no copied conditions, resources or triggers.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Instant modes; Renewal/Radiance heal, Echoes numeric repeat; no sustained schedule.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.saint.aura-of-grace

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · NR

Source data/public/class_playtests/cleric.json / cleric.hero.saint.aura-of-grace · SHA256 7dff7e8271aba866c1b596528fe2e7d1e3f9a1558eeec233922585461bcc9854.

**name:** Aura of Grace

**activation:** Triggered and passive

**cost:** 1 RP per healing pulse

**rangeAndTarget:** Living allies within 15 feet

**duration:** Passive during real encounters

**frequency:** Healing once/own regular turn; critical reduction once/ally/round

**effect:** Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Source regular-start; optional 1 RP; once/own regular turn, no 3-cap.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.priest.balanced-scales

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/cleric.json / cleric.hero.priest.balanced-scales · SHA256 7e7adca22a150348e1afd85fcf4ca10e7c6a2395883b66b2d889b097f8200b98.

**name:** Balanced Scales

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Living creatures healed by your Cleric features

**duration:** Until start of your next regular turn

**frequency:** At most once per marked ally per round

**effect:** Balanced Scales. Tags: priest, healing, retaliation. After you restore HP to a living ally, mark it until the start of your next regular turn. The first enemy to damage that ally during the mark takes S + M radiant damage. The retaliation is not an attack, cannot critically hit and cannot recursively trigger another Balanced Scales event.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Actual-gain mark; no healing pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.priest.word-of-power

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/cleric.json / cleric.hero.priest.word-of-power · SHA256 b238551c3ab4549273d2ad295301aba312d27d3cc75f8768e800cc67fb23c175.

**name:** Word of Power

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** One creature within 30 feet

**duration:** Instantaneous

**frequency:** Recharge 2 rounds

**effect:** Word of Power. Tags: priest, divine. Choose one mode. Mercy: one willing living creature regains S d8+M HP. Rebuke: one Undead or Fiend makes a Constitution save, taking (S+1)d8 radiant on failure or half on success; failure also removes its Reaction until the start of its next turn. Command: one other hostile creature makes a Wisdom save; failure knocks it Prone and removes its Reaction until the start of its next turn. No mode changes beliefs, loyalty or ideology.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Mercy single heal only.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.priest.cosmic-equilibrium

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH/G

Source data/public/class_playtests/cleric.json / cleric.hero.priest.cosmic-equilibrium · SHA256 511b9a9abd80cc33649c3a30d73c03139189a2443a25ae92b7905fbdb0251787.

**name:** Cosmic Equilibrium

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** 15-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** 1/short rest

**effect:** Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Trigger conversions once/round; no autonomous pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.cultist.sanguine-rite

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH

Source data/public/class_playtests/cleric.json / cleric.hero.cultist.sanguine-rite · SHA256 b043e78dd641a9e31b86b49c238105f2b4ee4138c21f4e2ae9e194fee44169f9.

**name:** Sanguine Rite

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self and one ally within 30 feet

**duration:** Instantaneous

**frequency:** At most once on each of your turns

**effect:** Sanguine Rite. Tags: cultist, rite, healing. When one of your Rites deals damage to at least one enemy, choose one living ally within 30 feet. That ally regains HP equal to half the actual damage dealt to one chosen damaged enemy, rounded down, maximum S+M HP. This healing cannot trigger Sanguine Rite again.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Once/own turn damage-derived finite heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.cultist.blasphemous-tongue

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/cleric.json / cleric.hero.cultist.blasphemous-tongue · SHA256 793dec5aa60dff80f8da02ed52a55b22c28c0b8975ca949d9dc9bf4374e6f1c6.

**name:** Blasphemous Tongue

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Enemies affected by your Sacrament

**duration:** Until the next Sacrament pulse or effect end

**frequency:** Once per target per pulse

**effect:** Blasphemous Tongue. Tags: cultist, sacrament, doomed. At each pulse of your Sacrament, each enemy affected by that pulse makes a Wisdom save. On failure it becomes Doomed until the next pulse. While Doomed, HP healing it receives is reduced by S+M, minimum 0, and each positive timed buff on it counts down one additional round at the end of its turn. Repeated failures refresh rather than stack.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Healing reduction applied by Sacrament pulses.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.cultist.zealot-s-touch

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/cleric.json / cleric.hero.cultist.zealot-s-touch · SHA256 d419c667240c84d69d12a5f639b9466ef00ed47af9eb2a0eea3e9c3d924649e6.

**name:** Zealot's Touch

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Healing-over-time Rites you control

**duration:** Passive

**frequency:** Always

**effect:** Zealot's Touch. Tags: cultist, rite, necrotic. When starting a Rite whose printed pulse would restore HP over multiple turns, you may designate a hostile creature instead of a healing recipient. At each applicable pulse that enemy makes a Wisdom save. On failure it takes necrotic damage equal to the Rite's rolled healing dice; on success it takes half. Flat healing bonuses are not converted. The enemy receives no healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Converts qualifying HoT pulse dice to damage; inherits source pulse cadence.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.cultist.dark-sacrament

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP

Source data/public/class_playtests/cleric.json / cleric.hero.cultist.dark-sacrament · SHA256 86c14c628a3b9ee335e2c7316844416ed1cd61e83f60f83d5af04d2e216071f4.

**name:** Dark Sacrament

**activation:** Action

**cost:** 3 Conviction + 5 RP to start; 1 RP maintenance

**rangeAndTarget:** 15-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, maximum 3 Cleric turns

**frequency:** Recharge 4 rounds

**effect:** Dark Sacrament. Tags: cultist, sacrament, rite, sustained, zone. On start and each paid maintenance pulse, roll S d6 once. Up to three enemies in the zone make Constitution saves, taking that roll as necrotic damage on failure or half on success. If at least one enemy takes damage, up to three living allies in the zone each regain floor(roll/2)+M HP. Maximum 3 pulses. The Conviction expenditure can vent Dissonance once.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start pulse included; later 1 RP maintenance; max3. Maintenance action unspecified here.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## cleric.hero.cultist.zealot-s-fervor

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/cleric.json / cleric.hero.cultist.zealot-s-fervor · SHA256 c54199ee73ebfbe5c2c47cd5771fc43fd4f7609dfef775292d0798b409d44e4f.

**name:** Zealot's Fervor

**activation:** Bonus Action

**cost:** 2 Conviction

**rangeAndTarget:** Self

**duration:** 3 rounds

**frequency:** 1/short rest

**effect:** Zealot's Fervor. Tags: cultist, stance. For 3 rounds, once on each of your turns add S to one damage roll from a Cleric feature and S to one HP-healing roll from a Cleric feature. While the Fervor lasts, your AC is reduced by 1. The Conviction expenditure is not a Rite or Invocation and therefore does not vent Dissonance by itself.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: +S to one healing roll/own turn for 3 rounds.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## crimson-agent.engine[2]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/crimson-agent.json / 2 · SHA256 44a38acbffca3c994c2444d9f9183f7d8013ddda451f37182a4c2c25150755ea.

**text:** Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Bleed/healing-version distinction; no healing scheduler.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## crimson-agent.hero.bloodweaver.hemostasis

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI

Source data/public/class_playtests/crimson-agent.json / crimson-agent.hero.bloodweaver.hemostasis · SHA256 fd035eba7d0e2ed5547d745a6e3e52207bfa499b87cd0c693f1f00bb932b87f0.

**name:** Hemostasis

**activation:** Passive

**cost:** 1 additional RP per application

**rangeAndTarget:** One willing living ally in range of your Bleed application

**duration:** 3 target turns

**frequency:** Once/own turn

**effect:** You may replace a new Bleed application on that ally with healing 1d4 at start of its next 3 turns. Pay extra RP even if original application was free. One such healing effect per target; it cannot spread, detonate, generate BG or trigger healing loops.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Prepaid 1d4 at target-next 3 regular starts; no upkeep.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## crimson-agent.hero.bloodweaver.lifewell

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP

Source data/public/class_playtests/crimson-agent.json / crimson-agent.hero.bloodweaver.lifewell · SHA256 df6aec7b14a71408fb30b0e66b2051a09d3570829b228e4e04c55b7cb0ae2568.

**name:** Lifewell

**activation:** Action

**cost:** 4 RP; all BG, minimum 3

**rangeAndTarget:** Up to 3 living allies within 15 ft

**duration:** Concentration, 3 of your turns

**frequency:** 1/long rest

**effect:** Spend K BG. At start and on each of your next 2 turns, use Bonus Action and pay 1 RP to pulse healing: each chosen ally still within 15 ft regains 1d8+K HP. Without maintenance it ends at turn end. Total 3 pulses; no triggers create more BG.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: First same-turn BA+1RP; next2 BA+1RP; fixed targets; missed maintenance ends.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## dragoon.engine[4]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/dragoon.json / 4 · SHA256 250848ddbb6f7e2f67c7ae07765b704f2c2dfcee59e1acb21e1b1c32c622a8cd.

**text:** Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Burn/Bleed periodic damage only.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## druid.engine[4]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X/G

Source data/public/class_playtests/druid.json / 4 · SHA256 7befb5eef095e247cb6cab325a66a0e3b84d24b9ea7771ba28fa9a13c2afa976.

**text:** Transformation reserves prevent unlimited replacement HP: at long rest record Buffer Reserve=2 L+M and Form Surge Reserve=PB. A form giving temporary HP draws that many from Buffer Reserve, up to remaining amount, with normal nonstacking; never real healing. A form special described once/transformation also spends 1 Form Surge and cannot be refreshed by resuming the form. Form Surge refills only long rest. Forms cannot grant free casts, RP or shift uses. Auras affect at most 3 enemies and once per enemy per round; retaliation once/round total; ongoing riders refresh, never stack. Entering a legal Shapeshift clears the Refrain counter and remembered repeated-spell name, as the protected source contract requires. It does not reduce accumulated Dissonance. Natural attacks do not clear Refrain.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Temp-HP reserve and aura guards; not real recurring healing.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## mirrorsage.hero.mirror-mage.reality-fracture

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/mirrorsage.json / mirrorsage.hero.mirror-mage.reality-fracture · SHA256 01db39e48e6febb6fea905259253d2c146292352ba0876f75fc6101b79c195cd.

**name:** Reality Fracture

**activation:** Action

**cost:** 6 RP; 1 long-rest use

**rangeAndTarget:** Fixed 10 ft-radius zone within 30 ft

**duration:** Concentration, 3 of your turns

**frequency:** 1/long rest

**effect:** While you stand inside, once/turn add 1d6 to one Echo damage/healing amount or impose-1 on one target's Echo save. Choose before resolving. No free releases, random recasts, resource refunds or extra targets.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Once/turn optional +1d6 to existing Echo heal; no pulse creation.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## mirrorsage.hero.shattered-one.fractured-dominion

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/mirrorsage.json / mirrorsage.hero.shattered-one.fractured-dominion · SHA256 7eb5063a016220234c5eca407a3ccd2eb580379e56ac90b5fb8dc4ade2315150.

**name:** Fractured Dominion

**activation:** Bonus Action

**cost:** 8 RP; 1 long-rest use

**rangeAndTarget:** Self

**duration:** 2 of your turns

**frequency:** 1/long rest

**effect:** Your first damage release on each of these 2 turns adds one half-dice component against a DIFFERENT enemy within 10 ft of an original target. Same package and shared copy cap; excludes healing/control. Never recursively copies a copy or adds a release action.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Damage copy only; healing excluded.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## monk.base.crane-stance-support

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD/TH

Source data/public/class_playtests/monk.json / monk.base.crane-stance-support · SHA256 e674e9a4ae8aa0f0d52cd371b86e9173b9ba7f00a2447db64e31c14f44b42314.

**name:** Crane Stance (Support)

**activation:** Passive

**cost:** 0 for stance; healing costs 1 Ki and 1 RP

**rangeAndTarget:** Self; one ally within 15 feet for healing rider

**duration:** While active

**frequency:** Automatic core stance

**effect:** Crane Stance. Tags: stance, support. While unarmored, whenever you move at least 15 feet on your turn, gain +1 AC until the start of your next turn. HP healing you receive from another creature gains +S HP once per round. When you begin an unarmed strike at exactly 5 Ki and hit, spend 1 Ki and 1 RP; you and one living ally within 15 feet each regain S+M HP, at most once per turn.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Incoming-heal +S once/round; paid hit rider heal once/turn.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## monk.hero.enlightened-master.breath-of-the-thousand-petals

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/monk.json / monk.hero.enlightened-master.breath-of-the-thousand-petals · SHA256 ef8e3a96a396ed3d48f95c0e4138b0eae186fe297b746cae0c83c40004fa508e.

**name:** Breath of the Thousand Petals

**activation:** Action

**cost:** 5 Ki + 5 RP

**rangeAndTarget:** Up to six allies within 20 feet

**duration:** Until start of your next regular turn

**frequency:** 1/long rest; automatic Hero Final

**effect:** Final — Breath of the Thousand Petals. Tags: hero, enlightened, final, resurrection, weave. Living or Downed allies in range regain 3 S d8+M HP. Up to two allied creatures that died since the end of your previous regular turn return to life at 1 HP if their bodies can sustain life. Until the start of your next turn, affected living allies cannot be reduced below 1 HP by damage, though instant-death effects still function. It removes no Wounds and cannot revive the same creature twice.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One Final heal/resurrection event; no recurring pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## monk.hero.enlightened-master.circle-of-harmony

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP

Source data/public/class_playtests/monk.json / monk.hero.enlightened-master.circle-of-harmony · SHA256 df3b3c65b152fd7b3a217eac2e551b3fc473a00b9704fcbb98bfe0dc9611c4bd.

**name:** Circle of Harmony

**activation:** Action

**cost:** 2 Ki + 3 RP to start; 1 RP maintenance

**rangeAndTarget:** 10-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, maximum 3 Monk turns

**frequency:** Recharge 4 rounds

**effect:** Circle of Harmony. Tags: hero, enlightened, healing, zone, weave, sustained. On start and each paid Bonus Action maintenance pulse, up to three living allies in the zone regain S d6+M HP. Maximum 3 pulses. A creature receives this named effect at most once per round. It removes no Wounds and cannot restore the dead.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start included; later BA+1RP; max3; repick≤3/pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## monk.hero.enlightened-master.transcendent-meditation

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI

Source data/public/class_playtests/monk.json / monk.hero.enlightened-master.transcendent-meditation · SHA256 ef26fc5933a98d0d06c511e4ecddeda4ea9dab8ee064bc4f2eec65d028589803.

**name:** Transcendent Meditation

**activation:** Action

**cost:** 3 Ki + 4 RP

**rangeAndTarget:** Self and up to three allies within 15 feet

**duration:** Concentration, maximum 3 Monk turns

**frequency:** 1/short rest

**effect:** Transcendent Meditation. Tags: hero, enlightened, healing, weave, sustained. On start and at the start of each of your next two regular turns while concentration holds, each target regains S d6 HP. You regain 1 Ki on the second pulse only, never above 5. Targets must remain within 15 feet. This finite healing cannot be restarted until the short-rest use refreshes.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start + next2 source regular-start automatic pulses; fixed targets; concentration.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.engine[26]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G/TW

Source data/public/class_playtests/oracle.json / 26 · SHA256 dd6003b655e77deb78cbdc17b83837c51b1f4798eb77d546cbd9b865cdf725b2.

**text:** Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Generic Oracle persistent-zone schedule: fixed sets, concentration, ≤3 funded windows.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.spiral-touched.spiral-touched-boon-iii

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/oracle.json / oracle.supplement.spiral-touched.spiral-touched-boon-iii · SHA256 a6358be2e17db52d461c11e2df79d972481dba2c95ebd29ecd7c31a02987d377.

**name:** Spiral-Touched — Boon III

**activation:** Triggered at 0 HP

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of next regular turn

**frequency:** 1/long rest

**effect:** 1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One direct recovery; not pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.wound-eater.wound-eater-boon-iv

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP

Source data/public/class_playtests/oracle.json / oracle.supplement.wound-eater.wound-eater-boon-iv · SHA256 9028f42b10e75ba44b130f18695a0ef9411d99df43b4929f1b89d1e4ead2d127.

**name:** Wound Eater — Boon IV

**activation:** Bonus Action; start-of-turn pulses

**cost:** 2 RC start; 1 RC per later pulse

**rangeAndTarget:** Up to three living enemies within 10 feet

**duration:** Concentration; at most three pulses

**frequency:** One aura; once/target/round

**effect:** pay 2 RC as a Bonus Action to activate a 10-foot drain aura, requiring concentration for at most three pulses; pay 1 RC before each pulse after the first or end it. You may suppress it freely. During a real encounter, at the start of your turn up to three meaningful living enemies in the aura takes S necrotic damage; regain HP equal to the total actually dealt, capped at S+M per turn.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: First drain next source start; two later 1RC source-start pulses.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.burning-blood.burning-blood-boon-v

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TW/TH

Source data/public/class_playtests/oracle.json / oracle.supplement.burning-blood.burning-blood-boon-v · SHA256 2632f2e1356764183fce28146213368f6ddea68646318394a679610edc8c2d83.

**name:** Burning Blood — Boon V

**activation:** Bonus Action

**cost:** 0

**rangeAndTarget:** Self; up to three enemies/allies within 15 feet

**duration:** Three rounds

**frequency:** 1/long rest; one pulse/target/round

**effect:** 1/long rest as a Bonus Action become a living pyre for 3 rounds. At the start of each hostile creature's turn within 15 feet it takes S d6 fire damage. Once per your turn when at least one enemy takes fire damage from you, regain 1d6 HP, capped at S+M HP per turn. Allies in the aura gain fire resistance and hidden/invisible creatures within 10 feet cannot benefit from mundane darkness or visual concealment against creatures illuminated by your pyre.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Target-start damaging aura + once/own-turn heal trigger; engine26 applies unless later source marks Final exception.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.consumed.consumed-boon-v

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/oracle.json / oracle.supplement.consumed.consumed-boon-v · SHA256 50d2ca5f682a506377c7b843b7ce6a077296b98aa74cd95085384509ac42ccd0.

**name:** Consumed — Boon V

**activation:** Bonus Action

**cost:** 0

**rangeAndTarget:** Self and up to three allies within 10 feet

**duration:** Three rounds

**frequency:** 1/long rest

**effect:** 1/long rest as a Bonus Action fully embody your Mystery for 3 rounds. Gain immunity to the theme damage type, +2 on Revelation attack rolls and Revelation save DC, and add S to one Revelation damage or healing roll each turn. Allies within 10 feet gain +1 AC. Visible transformation cannot be suppressed during this embodiment.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: +S to one Revelation heal/turn; no pulse itself.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.bones.rotting-touch

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH/G

Source data/public/class_playtests/oracle.json / oracle.supplement.bones.rotting-touch · SHA256 2a184115c77c3e39626229f0d95c4b73218e849b6ccc078dd5ae170ccfdf3475.

**name:** Rotting Touch

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One creature you can touch

**duration:** Maximum 3 rounds

**frequency:** At will while RC remains

**effect:** Make a Revelation attack. On hit the target makes a Constitution save. On failure it gains Decay for up to 3 rounds: attacks against it add S damage once per attacker per turn, it takes -1 on saving throws and cannot regain HP. At the end of each turn it repeats the save, ending Decay on success. Corpses within 2 tiles of a Decayed creature cannot be raised while Decay persists. If the target is undead, it also takes 2d6 necrotic damage on the initial hit and you regain half the actual damage dealt, capped at S+M HP. At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Initial undead damage-derived heal; Decay blocks healing; no healing pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.bones.unfinished-chorus

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP/TH

Source data/public/class_playtests/oracle.json / oracle.supplement.bones.unfinished-chorus · SHA256 d0c65305f314bb6bbb3b9245ec88c655a5d4b815b553e84d3cddcca489dfe535.

**name:** Unfinished Chorus

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** Enemies, controlled undead and corpses within 4 tiles

**duration:** 2 rounds; Revelation backlash 1 round

**frequency:** At will while RC remains

**effect:** For 2 rounds, enemies within 4 tiles suffer Dread: -1 on attack rolls and saving throws. Once on each of your turns choose one living enemy in range; it takes 1d6 necrotic damage and you either regain half the actual damage dealt, rounded down, or one living ally within 3 tiles of you regains that amount, maximum S+M HP. Undead you control add S damage to one attack each turn and reduce first damage each round by 1. Corpses in the area cannot be raised while the Chorus lasts. Afterward you are suffering Revelation backlash until end of your next turn: -1 attacks/saves and Speed -5 feet. Choose up to three enemies and three allies. Enemies make Wisdom saves on entry and at the end of each turn, ending their debuff on success. The drain allows a Constitution save for half damage; healing is capped at S+M total per pulse. Concentration and pulse upkeep apply.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: First source-turn drain included; later engine26 upkeep; 2-round cadence, fixed candidate sets.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.flame.zealot-s-renewal

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/oracle.json / oracle.supplement.flame.zealot-s-renewal · SHA256 c5be3b9f61b1d449a60c73c0d7441db0451cec2ddf56b73113e480ccb08aaf91.

**name:** Zealot's Renewal

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One living ally within 3 tiles; adjacent enemies

**duration:** Instantaneous; fire ward until start of your next turn

**frequency:** At will while RC remains

**effect:** The ally regains 2 S d8+M HP, then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it. It may end Poisoned or immediately repeat one disease save. Until the start of your next turn it reduces the first fire damage it takes by S. Hostile creatures adjacent to the healed ally take 1d4 fire damage once from scattering embers.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Single healing event + independent cure/backlash.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.flame.first-flame-convergence

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH

Source data/public/class_playtests/oracle.json / oracle.supplement.flame.first-flame-convergence · SHA256 25282e2ec8de9b5017e44ff952f9082abcada88b6d5990dbb595d67b44540b76.

**name:** First Flame Convergence

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** Self and allies within 4 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** For 2 rounds, once on each of your turns when a Flame Revelation deals fire damage, add one extra die matching that Revelation's primary damage die to one damage roll. Once per turn when one of your Flame Revelations damages a meaningful hostile creature, one living ally within 4 tiles regains 1d6 HP. Allies within 4 tiles are immune to Frightened. Once per turn when this effect heals an ally, that ally reduces the first damage it takes before your next turn by 1. Zealot's Renewal deals no backlash while Convergence lasts.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Once/turn damage-triggered heal; no generic zone pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.flame.crown-restored

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI/TW

Source data/public/class_playtests/oracle.json / oracle.supplement.flame.crown-restored · SHA256 354e4fb2b53a1b46b121c1edc36df4e364f0dbf66931fa7bdb453e68d6f3ab8f.

**name:** Crown Restored

**activation:** Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self and allies within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Limited Final target-start pulses, max3/creature; no generic upkeep.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.life.resonant-seed

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TW

Source data/public/class_playtests/oracle.json / oracle.supplement.life.resonant-seed · SHA256 ee79b90bfc9c7117d99edebc2dc66e6b79b37bbc5f732ac6a2c4bedabab152ab.

**name:** Resonant Seed

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** 2-tile-radius fixed zone centered within 4 tiles

**duration:** 3 rounds

**frequency:** At will while RC remains; one Seed zone at a time

**effect:** When a living ally starts its turn in the zone, it regains 1d4 HP, at most once per round and for at most three pulses from this use, and may end Frightened or Poisoned on the first pulse it receives. Undead entering or starting their turn in the zone take 1d4 radiant damage once per round and make a Strength save; on failure their Speed is reduced by 1 tile until the end of that turn. Healing requires the paid 1 RC activation and ends after 3 rounds.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Activation-funded window1; later engine26 1RC windows2/3; fixed Oracle set.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.life.garden-of-restoration

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TW

Source data/public/class_playtests/oracle.json / oracle.supplement.life.garden-of-restoration · SHA256 faaa0f647c20d847d84790b2a353bb9e9fcf3946f210c911e003d08474a7de93.

**name:** Garden of Restoration

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** 4-tile-radius fixed zone centered within 5 tiles

**duration:** 3 rounds

**frequency:** At will while RC remains; one Garden at a time

**effect:** At the start of each living ally's turn in the Garden, it regains 1d6 HP, maximum three pulses per creature from this use, and gains +1 HP the next time another finite healing effect restores HP before its next turn. The first time each ally enters or starts in a given Garden, it may end Poisoned or immediately repeat one disease save. Undead starting in the Garden take 1d6 radiant damage and make a Wisdom save; on failure they take -1 on attack rolls until the end of that turn.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Same funded-window model; first-contact cure independent of HP gain.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.life.verdant-pulse

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/oracle.json / oracle.supplement.life.verdant-pulse · SHA256 feb0f82538549fb2d540cfa9a68b89f517d4f1138b44ade546065fc7300c24f9.

**name:** Verdant Pulse

**activation:** Passive and Reaction

**cost:** 0 RC

**rangeAndTarget:** Allies you heal; emergency ally within 4 tiles

**duration:** Buff until end of ally's next turn; emergency instantaneous

**frequency:** Buff once per ally per short rest; emergency 1/encounter

**effect:** When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Triggered after actual finite HP restoration; emergency floor separate.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.life.song-of-mending

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI

Source data/public/class_playtests/oracle.json / oracle.supplement.life.song-of-mending · SHA256 ca7500f38966fc943c0398ff2fbddfe96070ca9caf15a6d0b24cee7d2fa2def1.

**name:** Song of Mending

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** Living allies within 5 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** On activation and at the start of your next regular turn, each living ally still within 5 tiles regains 2d6 HP, for exactly two possible pulses per use. Once during the duration for each ally, when one damage event would reduce it below 1 HP without instant death, it remains at 1 HP instead. When this prevention triggers, that ally may end Frightened or Poisoned and gains +S HP the next time a separate finite healing effect restores HP before Song ends. This removes no Wounds and cannot resurrect.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Activation + next source regular-start; Enhanced adds second-later start; no target-start upkeep.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.life.life-revelation-mastery

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/oracle.json / oracle.supplement.life.life-revelation-mastery · SHA256 f231bdb47b3545daad32777e23dd58122092961abb95c826436a646ab5e62b44.

**name:** Life Revelation Mastery

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** One eligible known Life Revelation

**duration:** Permanent

**frequency:** Choose one upgrade at Oracle 15

**effect:** Choose one mastery for a Revelation you know. Enhanced Overflowing Light: maximum temporary HP from excess healing becomes 20. Enhanced Garden of Restoration: the first Garden pulse a creature receives may end both Poisoned and one disease that explicitly allows magical curing, rather than only one of those benefits. Enhanced Song of Mending: duration becomes 3 rounds and gains one additional 2d6 healing pulse at the start of your second later regular turn; each ally still receives only one 1-HP death prevention per use.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Modifies Garden/Song; creates no pulse alone.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.life.eternal-bloom

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI

Source data/public/class_playtests/oracle.json / oracle.supplement.life.eternal-bloom · SHA256 3d97cb828d42d1ec6f4f674e4328a37f916f47c15513a4e357cff80a706f7d02.

**name:** Eternal Bloom

**activation:** Action

**cost:** 0 RC

**rangeAndTarget:** 5-tile-radius fixed sanctuary centered within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** When Eternal Bloom appears, record each living ally's missing HP while it is inside the zone. Divide that recorded missing HP into three healing installments as evenly as possible, with any remainder assigned to earlier pulses. On activation and at the start of each of your next two regular turns, each qualifying ally still inside regains its next installment; later damage does not increase this reserve. Once per ally during the Bloom, when damage would reduce it to 0 HP without instant death, it remains at 1 HP instead. Allies in the zone have necrotic immunity for the 3 rounds. When the Bloom ends, petals create light obscurement in the zone until the start of your next turn. It removes no Wounds and does not resurrect.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Three fixed reserve installments; activation + next2 source starts; no upkeep.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.time.rewind-wound

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/oracle.json / oracle.supplement.time.rewind-wound · SHA256 eb01bdc7533669a80e0862bf3130c342b3b8c9c3f4199f8925953086e6bc898c.

**name:** Rewind Wound

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One living ally you touch

**duration:** Healing instantaneous; protection until start of your next turn

**frequency:** At will while RC remains; same damage event can be rewound once

**effect:** Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One historical-damage heal; no recurring pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## oracle.supplement.time.the-spiral-opens

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · COPY/FI

Source data/public/class_playtests/oracle.json / oracle.supplement.time.the-spiral-opens · SHA256 b15b7a477b14185e1510967e1d24c7e46a856a400ef1575f876d2adbaa39ee28.

**name:** The Spiral Opens

**activation:** Action

**cost:** 0 RC

**rangeAndTarget:** Self; one known beneficial Time Revelation or one enemy within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds, at the start of each of your regular turns choose ONE temporal option, each usable at most once during this Final. ECHO REVELATION: repeat only the immediate numeric damage, healing, movement or buff component of one beneficial Time Revelation you personally resolved during the previous round, paying 0 RC; this copy is not a new Revelation cast, copies no resource restoration, action grant, hard control, condition trigger, Prophecy Trigger or proc. FORCED ECHO: choose one non-player enemy within 5 tiles and one ordinary weapon attack or non-resource movement action it took during its previous turn. The enemy makes a Wisdom save. On failure, during its next turn it must repeat that action pattern if legally possible, but it chooses all legal targets and paths; it spends no limited resources and cannot be forced to harm itself. A player-controlled creature instead, on a failed save, loses its Reaction and must choose either repeat one ordinary non-resource action type from its prior turn or have Speed reduced to 0 until turn end. Allies retain memory of all temporal echoes. This Final never creates more than one additional full Action for any creature in a round. There are only two options in this Final; after using both once, remaining rounds provide only the printed temporal presence, without another echo. An echoed healing amount also pays 1 RC or consumes an unused per-rest healing use; a temporal copy cannot create an uncosted healing reserve.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Up to one healing echo option; requires 1RC or unused healing use; no free reserve.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.engine[11]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G/MP

Source data/public/class_playtests/paladin.json / 11 · SHA256 965790fb859474dc7264c2a1afe1c947eb45153cea27d16eb10fe47c027ad779.

**text:** Sustained Oath spell damage/healing zones use concentration, at most three pulses, and 1 RP upkeep after the first pulse unless a priced card expressly supplies a different finite cadence. Native Oath auras retain their printed passive cadence and target cap. Final auras last their stated finite duration and include their pulses. All hard-denial effects, including compelled Actions, share the common once/source/target/encounter guard; later failures only remove Reactions and reduce Speed by half for one turn.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Sustained Oath zones: first included, later1RP upkeep, ≤3; Finals/native auras exempt.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.hero.lay-on-hands

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/paladin.json / paladin.hero.lay-on-hands · SHA256 4c5b19d2b558ca46e38f1d530683c19801b878d8bdf7027cb796e856c5ebcc75.

**name:** Lay on Hands

**activation:** Action

**cost:** All remaining Lay on Hands points; minimum 1

**rangeAndTarget:** Up to 3 living allies in aura

**duration:** Instant

**frequency:** 1/short rest and pool cost

**effect:** Allocate remaining points among targets, at least 1 each; restore 1 HP per point. You may instead allocate 5 points per target to end Poisoned or Frightened. Spend entire pool, cannot multiply it by recipient count, raise the dead or remove Wounds. Oathbreakers instead deal allocated necrotic damage to 3 enemies, CON half, same pool cost.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Single pool-spend heal; corrected Wave cadence belongs elsewhere.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-shared.dread-shelter

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-shared.dread-shelter · SHA256 21aacaa2a10867f745124fcb7d6c76eb33b0c79c19178726cd324df4b92df562.

**name:** Dread Shelter

**activation:** Bonus Action

**cost:** 3 RP

**rangeAndTarget:** Self

**duration:** Concentration, 1 minute

**frequency:** At will while RP remains

**effect:** New rank 2 Forbidden spell. Gain 2 S+M temporary HP on casting and 1 flat DR against weapon damage for duration. No recurring temp HP pulse or healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One temp-HP grant; explicitly no recurring heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-shared.desecrated-ground

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X/MP

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-shared.desecrated-ground · SHA256 5bcc361442663e6799678be29cff54b4a1d6ebd29793db87ec39edc2845513e9.

**name:** Desecrated Ground

**activation:** Action; Bonus Action maintenance

**cost:** 7 RP start; 1 RP per later pulse

**rangeAndTarget:** 10 ft radius fixed point 30 ft, up to 3 enemies

**duration:** Concentration, maximum 3 pulses

**frequency:** Recharge 4

**effect:** New rank 4 Forbidden spell. Initial and each paid pulse CON save for S d6 necrotic, half success. A failed target receives 1 less HP per healing die until start of your next turn. Penalty cannot make healing negative or stack with another same-stat reduction.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Nonhealing damage zone; initial + paid BA pulses under engine11.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-shared.last-reproach

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I/TH

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-shared.last-reproach · SHA256 895f333185c3eb243fcbe76dcc36a38ed52f8b1f4994746abf250a0102f7015d.

**name:** Last Reproach

**activation:** Reaction after an enemy damages an ally

**cost:** 10 RP

**rangeAndTarget:** That enemy 60 ft; one living ally in your aura

**duration:** Instant

**frequency:** 1/short rest

**effect:** New rank 5 Forbidden spell. Enemy WIS save for 3 S d8 necrotic, half success; ally regains S d8 HP after triggering damage. Does not revive dead or undo conditions. Uses ordinary spell strain and your Reaction.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One reaction heal after damage; no pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-mercy.aura-of-mercy

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-mercy.aura-of-mercy · SHA256 2601db1c3ead6e19e3cda88af15a2f7525e96d2d2a1171d037fc874d9c47ae35.

**name:** Aura of Mercy

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen allies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** The first time each round a selected ally receives HP healing from a finite or paid effect, add S HP. Each selected ally also reduces the first necrotic damage it takes each round by S. These benefits do not stack with another Aura of Mercy from the same source.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: First finite/paid heal per selected ally/round gets +S.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-mercy.blessing-of-the-meek

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-mercy.blessing-of-the-meek · SHA256 de83f7216e4f442bf324e7e9650e69091077d79b1be79d0753257dfbce13cde4.

**name:** Blessing of the Meek

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One living ally within 30 feet

**duration:** Healing instantaneous; AC bonus until start of your next regular turn

**frequency:** At will while RP remains

**effect:** The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Single heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-mercy.grace-eternal

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I/MOD

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-mercy.grace-eternal · SHA256 9144f23fd7fb45d1beb6c300bb20b85cd3eb172e4a6ac53003c0260770f94a25.

**name:** Grace Eternal

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to 3 allies in your Oath aura

**duration:** Until start of your next regular turn

**frequency:** 1/long rest

**effect:** Apply Miracle Veil to up to 3 allies in your aura without spending its short-rest use or RP. Once during this Veil for each affected ally, if damage would reduce it to 0 HP, it remains at 1 HP and immediately regains 2d8 HP. It also gains necrotic resistance until the end of its next turn. During Grace Eternal you may use Lay on Hands once without an Action, but must still spend points from your current Lay on Hands pool and may target only one creature.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Finite floor+heal per ally; one actionless LoH permission; no pulse schedule.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression · SHA256 1613079d8c08dac41dc4b7fe98b3dbbf5f4534a28a2d30282e93522bd69fdbde.

**name:** Healing Suppression

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** HP healing received by each selected creature is halved, rounded down. Temporary HP, damage prevention and resurrection are not healing for this effect. This suppression cannot reduce healing below 0 or convert prevented healing into damage.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Incoming HP healing halved; no pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate · SHA256 7fdfc30a56a5fbfec418c11a859f48cc7636e45998913a574f3b8dd80d7d14f5.

**name:** Exsanguinate

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 living creatures in your Oath aura

**duration:** Instantaneous

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Constitution save, taking 2 S d8 necrotic damage on failure or half on success. Regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. Undead and constructs are unaffected and cannot be used to generate healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Single damage-derived heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-flame.phoenix-rebirth

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · I

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-flame.phoenix-rebirth · SHA256 0a38ac2a6f534b9b6eefaa79733078371cc3169aa85ed60b825247cdfdf6ffd9.

**name:** Phoenix Rebirth

**activation:** Reaction

**cost:** 10 RP

**rangeAndTarget:** One living ally in your Oath aura reduced to 0 HP

**duration:** Revival instantaneous; fire shield until end of target's next turn

**frequency:** Once per combat per ally

**effect:** Trigger when the ally reaches 0 HP without being killed outright. It immediately regains HP equal to half its maximum, rounded down, minimum 1. Until the end of its next turn it has fire resistance. Once during that duration when a creature within melee reach damages it with a melee attack, that attacker takes 2d6 fire damage. Phoenix Rebirth removes no Wounds and cannot restore a creature destroyed beyond recovery.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Single zero-HP recovery; no recurring heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood · SHA256 d622135b269bb89a3f32d0f6ef20481b4d3b7a70ffe4601e14e0212048d385b5.

**name:** Death Touch — Blighting Blood

**activation:** Action

**cost:** Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss

**rangeAndTarget:** One creature within melee reach; its occupied space

**duration:** Damage instantaneous; blighted space until start of your next regular turn

**frequency:** At will while Lay on Hands points remain; terrain rider once per turn

**effect:** Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared points and blight the target's space until the start of your next turn. The first hostile creature other than the original target that enters or starts its turn in that space takes S necrotic damage. The patch creates no corpse, healing or resource trigger.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Damage/terrain only; explicitly no healing trigger.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified · SHA256 cbfc7808eaa7713c9e05331e24397dcbea9a3a6642ed0d08f088e4c582a950e8.

**name:** Scorch the Sanctified

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected enemies cannot regain HP from passive regeneration. At the start of each selected enemy's turn it makes a Charisma save. On failure, one temporary beneficial magical effect on it chosen by the Director from eligible non-innate effects is suppressed until the start of its next turn. Immunities, class engines, permanent traits and attunement are never suppressed.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Blocks passive regeneration only.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G/X

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word · SHA256 792ec5718045963e10d1e82e7880f66c22de6fa172a81242389edb31ea7c38f6.

**name:** Scorch the Sanctified — Blasphemous Word

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 creatures in your Oath aura

**duration:** Instantaneous; suppressed effect until end of next turn

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Constitution save, taking S d6 fire plus S d6 necrotic damage on failure or half on success. A failing target also has one eligible temporary beneficial spell or regeneration effect suppressed until the end of its next turn. You may knowingly include allies among the targets; the effect offers them no protection.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Damage + temporary regeneration-effect suppression.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura · SHA256 ab791099a2d42dd7017f37b891cda2e14f4c1c3ae23f73ef652dd3f459028af2.

**name:** Lifeleech Bloom Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets and one damage type at start of each turn

**effect:** Selected enemies cannot regain HP from passive regeneration. Also choose acid, cold, fire, lightning, necrotic, poison, radiant or thunder. A selected enemy's resistance to that chosen type is suppressed while it remains selected in the aura; immunity is never suppressed.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Blocks passive regeneration; not all finite healing.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom · SHA256 08c5946db93747abe8a71ed1a6aa82258108a072d3873c9f85a8ddae94fba83f.

**name:** Lifeleech Bloom

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 living creatures or plant creatures in your Oath aura

**duration:** Instantaneous

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. You regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. You may include willing allies among the targets, but they receive no protection and cannot be reduced below 1 HP by this Blasphemous Word. Constructs and ordinary unattended plants provide no healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Single damage-derived heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-grief.dirge-of-passage

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G/X

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-grief.dirge-of-passage · SHA256 df1f6705254fc3dcbf79d5c08aae5baf78e792c21ce9e059969dfe4627c62200.

**name:** Dirge of Passage

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Memories of up to 2 fallen allies; creatures in your Oath aura

**duration:** 2 rounds

**frequency:** 1/long rest

**effect:** For 2 rounds maintain two Final Vigil memories simultaneously and gain both selected benefits. Up to three selected hostile undead in your aura take an additional S radiant damage from your first damaging Paladin feature each round and cannot regain HP. Living allies in your aura gain +2 on death saves. No spirit gains its own turn, resources, spellcasting or complete former statistics. This flat rider replaces blanket damage vulnerability and never doubles a whole attack.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Prevents hostile-undead HP regain; no healing pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura · SHA256 65f1ac74f274a2f171571f40d3ce938061c6e4c58fba8925270b949fcec183ff.

**name:** Dirge of Ruin Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected living creatures cannot be returned from death while inside the aura, and HP healing they receive is reduced by S+M, minimum 0. This never converts healing into damage and cannot retroactively reverse a resurrection completed before the creature entered the aura.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Flat healing reduction + resurrection denial.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G/X

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin · SHA256 16cc8982591672cdbad5aa34bf755e2c4b8024c032fb29dba978ec14eb4d6407.

**name:** Dirge of Ruin

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 creatures in your Oath aura

**duration:** Damage instantaneous; healing block until end of next turn

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. A failing target cannot regain HP until the end of its next turn. This does not prevent temporary HP or remove healing already received.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Damage plus temporary no-HP-regain.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-the-martyr-king.crown-of-embers

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-the-martyr-king.crown-of-embers · SHA256 0ff07991fa0838522e96deb9434534c8c584850c6203ed3b47e8eeaf4246980f.

**name:** Crown of Embers

**activation:** Bonus Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 allies in your Oath aura

**duration:** Until start of your next regular turn

**frequency:** 1/short rest

**effect:** Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Prevention/redirection only; expressly no healing.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-the-martyr-king.burden-shared

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-the-martyr-king.burden-shared · SHA256 2a0ff54276d9127ac30458bae7ea5dc0f1295b5ec34ca63bb5ce22efdabb29d1.

**name:** Burden Shared

**activation:** Reaction when an ally takes damage

**cost:** 5 RP

**rangeAndTarget:** Triggering ally and up to two other willing allies in your aura

**duration:** One damage event

**frequency:** While RP remains

**effect:** After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Redirection only; transferred branch cannot trigger healing.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-the-martyr-king.throne-s-grace

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-the-martyr-king.throne-s-grace · SHA256 084a132d73f1f54d9155a932605eb82e4da34e8e1f61e69ca51c5031b3c502ad.

**name:** Throne’s Grace

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** Self and up to three allies in your aura

**duration:** Concentration; three rounds

**frequency:** While RP remains

**effect:** Your Lay on Hands and touch-range Paladin healing can target selected allies anywhere in your current aura with clear line of effect. Normal activation, pool/RP costs, rank gates and use limits remain. Rolled healing you grant them adds 1 HP per die, maximum S+M additional HP per effect; pool-point healing adds no dice bonus. Selected allies gain +1 on death saves. The spell itself restores no HP.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Modifies other Paladin heals; itself restores none.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oath-of-the-martyr-king.crown-undying

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-the-martyr-king.crown-undying · SHA256 f8de6f3fe586c6b30d10bbdd31c93e0976aa46dfb3631afbbcbebe8ebe1d0b1d.

**name:** Crown Undying

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to three selected allies in your aura

**duration:** Three rounds; no concentration

**frequency:** 1/long rest

**effect:** For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Finite redirection-derived healing; redirection ledger governs cadence.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura · SHA256 e4341a3bd789ba5baa4c0bf1817a7a16ec61fc0d98d9ca79101397f9f984f203.

**name:** Crownshatter Decree Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to three selected enemies in your aura

**duration:** While conscious and in aura

**frequency:** Each incoming healing event

**effect:** A selected enemy receives HP healing only if it has taken actual damage from a meaningful hostile creature since the start of its previous regular turn. If it has not, that healing restores 0 HP; its source still spends its normal costs. Temporary HP, stabilization and resurrection are not HP healing for this restriction. This aura never creates damage, transfers healing or reverses recovery that already resolved.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Conditional incoming-heal permission; source costs still spent when blocked.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## ranger.engine[5]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/ranger.json / 5 · SHA256 f45c0cef68da878ce0d7921f372222c3698711b0f412f432597bbc20445859da.

**text:** Chosen Hero grants a sixth Arrow at 11. Warder Nature's Wrath: ranged attack weapon+S d6 piercing; up to 2 allies within 10 ft gain M temporary HP (finite mitigation, not repeatable real healing). Stalker Phantom: two ranged attacks against different aligned targets within 60 ft, each weapon damage, no extra dice; one Arrow activation. Outrider Corruption: place 10 ft-radius zone within 60 ft, concentration until start next turn; up to 3 enemies entering/starting there take S d4 necrotic once each, CON half. Arrow copies cannot generate extra attacks, resources or permanent terrain changes.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Temp HP / damage-zone interfaces; no recurring real heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## ranger.hero.warder.living-pulse

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · NR

Source data/public/class_playtests/ranger.json / ranger.hero.warder.living-pulse · SHA256 e1b7bfa045b543de315480c9e783e4da0cc13ea5adad64a79ca535d32af375bd.

**name:** Living Pulse

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** Self in natural terrain

**duration:** Start of your regular turn

**frequency:** Once/turn

**effect:** You may pay 1 RP to regain 2 HP. Does not trigger when Downed or incapacitated, cannot exceed maximum and never counts as another healing spell. Replaces unlimited passive regeneration with a finite cost.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Once source regular-start/turn, optional1RP, self2HP.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## ranger.hero.warder.healing-briar

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI/paid

Source data/public/class_playtests/ranger.json / ranger.hero.warder.healing-briar · SHA256 d1ca2d633ca412393953afab0065f0439a3ad3a7f95d50500385078c999e1f6f.

**name:** Healing Briar

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** Fixed 10 ft-radius natural-ground zone within 30 ft; 3 allies/pulse

**duration:** Concentration, 3 of your turns

**frequency:** Recharge 4

**effect:** On start heal 1d8+M per chosen living ally; on next 2 turns Bonus Action+1 RP repeats pulse. Maximum 3 pulses; no passive additional entry healing and no Wound removal.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start included; next2 source turns BA+1RP; max3; repick≤3.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.engine[1]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP

Source data/public/class_playtests/shaman.json / 1 · SHA256 2a2a89b4f440277a59743d2dc2936f2a625be9557882f5796fa8fb71d4b76d80.

**text:** Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Renewal start included; next2 BA+1RP; ≤3 beneficiaries/pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.engine[2]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/shaman.json / 2 · SHA256 673d1b3887e874041180d1c813ee02efa51962dbc07a33844853a708b1468a5a.

**text:** On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Movement competes with upkeep; movement creates no extra pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.arch.extended-totem-duration

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD/MP

Source data/public/class_playtests/shaman.json / shaman.arch.extended-totem-duration · SHA256 d3e1a07ab47f089ce66a98f3ef5083eb604f55174892955836175df7c94724bb.

**name:** Extended Totem Duration

**activation:** Passive

**cost:** 0; full upkeep for extra Renewal pulse

**rangeAndTarget:** One of your totems

**duration:** Maximum 4 of your turns

**frequency:** Continuous

**effect:** Totems last 1 extra turn. Renewal may have a fourth pulse only if you pay Bonus Action+1 RP on that turn; no fifth pulse and no automatic free healing. Concentration still required.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: One fourth Renewal opportunity only with BA+1RP.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.arch.spirit-cache

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · COPY

Source data/public/class_playtests/shaman.json / shaman.arch.spirit-cache · SHA256 9a84d6cf21f387bfc7fc32c7e9e7344aa7449da4abd8e24b96e76710e18249ce.

**name:** Spirit Cache

**activation:** Triggered

**cost:** 1 short-rest use

**rangeAndTarget:** One flask/to-tem effect you directly used

**duration:** Stored until encounter end

**frequency:** 1/short rest

**effect:** Store its profile, not an active copy. On a later turn use normal Action/Bonus Action and pay all RP and a new flask unit or full totem cost to repeat it. Add 1d6 to one numerical damage/heal amount; no copy of refund/limited use.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Recast profile later with full costs/new stock; not active pulse copy.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.arch.totem-pulse

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/shaman.json / shaman.arch.totem-pulse · SHA256 da88a2c237b85efcd2b52a63b65f8a2decafbdc6671d11820ab72f859f0c0ce6.

**name:** Totem Pulse

**activation:** Passive

**cost:** 1 RP optional

**rangeAndTarget:** Up to 3 creatures inside newly placed non-healing totem

**duration:** Instant

**frequency:** Once/turn

**effect:** On placement pay 1 RP: allies gain M temporary HP OR enemies make DEX save for S affinity damage, half on success. No immediate second Renewal healing pulse, no repeat from moving the totem.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Nonhealing placement pulse; no extra Renewal heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.arch.spirit-saturation

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X/G

Source data/public/class_playtests/shaman.json / shaman.arch.spirit-saturation · SHA256 e25c049b60111d478b8844f935bfdf3b1f6068d80100de6a8c2d702a9723f543.

**name:** Spirit Saturation

**activation:** Triggered

**cost:** 1 long-rest use

**rangeAndTarget:** One non-Renewal totem you place

**duration:** Normal duration

**frequency:** 1/long rest

**effect:** Waive its 2 RP placement cost once. Still use Action, concentration, capacity and any added costs. Cannot create a healing totem or be cached/refunded to generate more free casts.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Cannot waive/create Renewal healing totem.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.hero.theurgist.echo-totem

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD/MP

Source data/public/class_playtests/shaman.json / shaman.hero.theurgist.echo-totem · SHA256 20874e77366801074f6dc417c26450a1957dab6d55ca77ba083e370fec3fa92b.

**name:** Echo Totem

**activation:** Triggered

**cost:** 1 additional RP

**rangeAndTarget:** Adjacent empty space within 5 ft of newly placed totem

**duration:** Same remaining duration

**frequency:** Once/placement

**effect:** Create a weak echo anchor of that totem. It counts toward capacity; if no space in capacity, cannot create it. Its radius 10 ft and numerical bonuses/healing are half, rounded down. Shared concentration/upkeep and same-name nonstacking prevent double healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Shares parent pulse/upkeep; half amount; NEW shared target budget/no double heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.hero.bloodcaller.blight-totem

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/shaman.json / shaman.hero.bloodcaller.blight-totem · SHA256 56bd3dd7b141931dda883f3728d30221c8e34ba30347d55c87fe66dc2f338805.

**name:** Blight Totem

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Totem within 30 ft; 15 ft aura affecting all creatures

**duration:** 3 of your turns

**frequency:** Ordinary totem capacity/concentration

**effect:** HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Healing-halving aura only.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.hero.bloodcaller.blood-curse

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/shaman.json / shaman.hero.bloodcaller.blood-curse · SHA256 34064d553a32ec2626c5cf9fd9dffdfc4c7a53c5027914e0b3a927be699b9319.

**name:** Blood Curse

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One living enemy within 60 ft

**duration:** 3 target turns

**frequency:** Recharge 3

**effect:** CON save or Bleed 1d4 necrotic at start of each of next 3 turns. Action plus successful Medicine check against class DC ends it; magical healing also permits an immediate CON save to end. Never permanently unhealable; no repeated stacking.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Magical healing permits cure save; healing itself not scheduled.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## shaman.supplement.elder-spirit-accord-new-hero-capstone

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/shaman.json / shaman.supplement.elder-spirit-accord-new-hero-capstone · SHA256 14135567a903c049f854953b8feb74893959b5f92c58123af008a3d8e67eac70.

**name:** Elder Spirit Accord — new Hero capstone

**activation:** Triggered

**cost:** 1 long-rest use

**rangeAndTarget:** Your chosen Hero ultimate

**duration:** One activation

**frequency:** 1/long rest

**effect:** When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Adds M to one healing roll/use; no duration/pulse increase.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## soldier.engine[4]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/soldier.json / 4 · SHA256 f4f11a1404b15b950d423edee89296a42130ca4ca686b322d4259ecda7e1b6ed.

**text:** Base 1–2, Commander Arch 3–9, then Champion/Artillerist/Tyrant Hero 10–20. Palisade 5 is automatic; Intercepting Shot has minimum 6 and Fortify Zone 9. Other cards require selection. There is no source automatic Arch capstone. At 20 gain the new Final Command below, clearly a playtest addition. No spell or sustained technique may be used to obtain infinite ammunition, structures, actions or permanent healing.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Anti-infinite-healing guard only.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## thief.hero.blackguard.exsanguinate

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · NR

Source data/public/class_playtests/thief.json / thief.hero.blackguard.exsanguinate · SHA256 37e182dce2daee77d1a02e8e10618f449d263f1fd06d4a1ea9a7db6937821a2f.

**name:** Exsanguinate

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** Self; bleeding enemy within 15 ft

**duration:** Instant

**frequency:** Once/own turn

**effect:** At start of your regular turn with a hostile bleeding enemy nearby you may pay 1 RP to regain S HP. No multiplying by enemy count or healing while incapacitated; not an ordinary spell or Dissonance-generating technique.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Source regular-start/turn, optional1RP, once/own turn.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.engine[7]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/tinker.json / 7 · SHA256 9429949777c5be914254699b4403f903a1e617504b801672deaff80b2f0ae0d4.

**text:** Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Healing pulse caps/costs remain; disabled duration continues.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.base.field-repair

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · DEV/X

Source data/public/class_playtests/tinker.json / tinker.base.field-repair · SHA256 612a9f00b4e33a8bfc77c3f83ff1e1d839fa1237e8d20e65b703bea1431b6d7f.

**name:** Field Repair

**activation:** Action

**cost:** 1 RP

**rangeAndTarget:** One construct/device touched

**duration:** Instant

**frequency:** Recharge 2

**effect:** Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Instant functional-device repair; not organic healing pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.hero.artificer.efficient-power-cells

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X/G

Source data/public/class_playtests/tinker.json / tinker.hero.artificer.efficient-power-cells · SHA256 c9738585ed8fae504de1ec5a0603fbea55a31fbcc5c4711838d7c7a252736c44.

**name:** Efficient Power Cells

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your nonhealing deployables

**duration:** Deployment

**frequency:** Continuous

**effect:** A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Nonhealing duration extension only; healing pulse count unchanged.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.hero.artificer.nano-aegis-drone

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI/command

Source data/public/class_playtests/tinker.json / tinker.hero.artificer.nano-aegis-drone · SHA256 a3117289c319bbe6ef18ae9437975f46db8da26795fd3f271cb54b443b93ee01.

**name:** Nano-Aegis Drone

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Your drone within 15 ft

**duration:** 3 rounds

**frequency:** Recharge 4

**effect:** Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Up to3 paid BA-command healing/tempHP pulses during3 rounds.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.hero.artificer.repair-pulse

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · DEV/X

Source data/public/class_playtests/tinker.json / tinker.hero.artificer.repair-pulse · SHA256 bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593.

**name:** Repair Pulse

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Upto 3 friendly devices within 30 ft

**duration:** Instant; AC until start next turn

**frequency:** 1/short rest

**effect:** Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Instant device repair; no organic healing.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.hero.artificer.restoration-field

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MP

Source data/public/class_playtests/tinker.json / tinker.hero.artificer.restoration-field · SHA256 a791259766db2192f9effe98f8946304ee8ef85d4ff243faa87c04665bf96ffa.

**name:** Restoration Field

**activation:** Action

**cost:** 3 RP start; 1 RP maintenance; one slot

**rangeAndTarget:** 10 ft radius within 30 ft

**duration:** Maximum 3 pulses

**frequency:** Recharge 4

**effect:** Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Initial pulse + later BA+1RP maintenance; max3; organic/device applications distinct.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## tinker.supplement.mech-overdrive

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · G

Source data/public/class_playtests/tinker.json / tinker.supplement.mech-overdrive · SHA256 0a3d5549a68c395cdfa364bac06f334436af7ac848ca5fed71a0a9bc141aec73.

**name:** Mech Overdrive

**activation:** Triggered on deploying a device

**cost:** 1 long-rest use plus original deployment cost

**rangeAndTarget:** One of your newly deployed devices

**duration:** Until encounter end, maximum 1 minute

**frequency:** 1/long rest; automatic Hero capstone

**effect:** Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Duration extension only; never increases healing pulses.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.hero.ironskin.regenerative-mutation

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · NR

Source data/public/class_playtests/warrior.json / warrior.hero.ironskin.regenerative-mutation · SHA256 9dcfe6b7b149360e470c0d7940937b13c7bbdc4f696999b93710257158818fd1.

**name:** Regenerative Mutation

**activation:** Passive

**cost:** Spend healing amount from Mutation Recovery Reserve

**rangeAndTarget:** Self

**duration:** While at least one mutation is active in a real encounter

**frequency:** Once at the start of each regular turn

**effect:** Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start each source regular turn; reserve-paid actual restoration; no3-cap.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.hero.ironskin.cellular-reconstruction

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · FI

Source data/public/class_playtests/warrior.json / warrior.hero.ironskin.cellular-reconstruction · SHA256 e8bd145d4393467058e51509e15230c1bc315884f24f96ccfb509faa5186d56c.

**name:** Cellular Reconstruction

**activation:** Action

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of your next regular turn, then instantaneous recovery

**frequency:** 1/long rest

**effect:** Cellular Reconstruction. Enter stasis until the start of your next regular turn: your Speed becomes 0, you cannot take Actions, Bonus Actions or Reactions, and attacks against you have advantage. At the start of your next turn regain 3d8 + M HP and end Poisoned plus one mundane or magical disease that does not explicitly require a special cure. This removes no Wounds and cannot function while dead.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Delayed one-time source-next-start recovery after stasis.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.hero.dreadspawn.pain-empowerment

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/warrior.json / warrior.hero.dreadspawn.pain-empowerment · SHA256 2b76787a8cddab4ebacdbf316a7c566f95cc8e0607dcc02cafc57f0dc09741ab.

**name:** Pain Empowerment

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** While below maximum HP

**frequency:** Always

**effect:** Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Threshold damage passive, not healing recurrence.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.supplement.primed

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/warrior.json / warrior.supplement.primed · SHA256 4ed45f7e4cbd2ee61dab2a5126f7d5494750257f17b5699d5ff4bb5fcffbc324.

**name:** Primed

**activation:** Passive

**cost:** 0

**rangeAndTarget:** One active mutation each turn

**duration:** While BT remains at least 2

**frequency:** Once per turn

**effect:** Enhance one active mutation's numeric benefit for the turn: +1 to one AC, DR, attack, save or flat damage bonus; +5 feet to one movement/reach bonus; or +1 damage/healing to one mutation-generated roll. Primed never increases duration, targets, immunity or resource generation.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: +1 to one mutation heal roll/turn; no new pulse.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.supplement.transcendent

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/warrior.json / warrior.supplement.transcendent · SHA256 473a344f361727b78897d649edbcc5fa6ad32f5edee5a0a6e9c943f027272f3c.

**name:** Transcendent

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of your next regular turn

**frequency:** 1/encounter total, regardless of trigger

**effect:** At Warrior 12+, the first time this encounter you cross 100% Brutality Progress or reach stored BT 4, activate all equipped mutations until start of your next regular turn. No serum profile or immediate healing trigger is granted. This is one total pulse, never a permanent BT 4 concurrency increase. At end choose active mutations up to normal limit, with their original remaining durations; others become dormant.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Explicitly no immediate healing trigger.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.supplement.bloodthick-node

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · NR

Source data/public/class_playtests/warrior.json / warrior.supplement.bloodthick-node · SHA256 d0a5ce3e76d61b789bfa1ab1daebf96399f56187b8fc796a0e44a1697007618b.

**name:** Bloodthick Node

**activation:** Passive while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** While active during a real encounter

**frequency:** Once at start of each regular turn

**effect:** Regain HP equal to current BT, maximum 3 HP per turn or 4 with Stack Overflow. No healing occurs outside a real encounter and it removes no Wounds. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start each regular turn, reserve-limited; no3-cap.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.supplement.rapid-coagulation

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · NR

Source data/public/class_playtests/warrior.json / warrior.supplement.rapid-coagulation · SHA256 8f6169026b8720168ba76650964f555e611eb7cc5c65f24be359a3561fbaa8ad.

**name:** Rapid Coagulation

**activation:** Passive while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** While active during a real encounter

**frequency:** Start of turn

**effect:** If you did not move during your previous turn, regain 2 HP at the start of your current turn. This does not function outside a real encounter. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Start each regular turn if prior-turn no movement; reserve-limited.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## warrior.supplement.bio-stabilizer

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · MOD

Source data/public/class_playtests/warrior.json / warrior.supplement.bio-stabilizer · SHA256 1bc1a0dd29cac0774f73c5c357f1c81ade4efca327bf104ce4004eaad84de7b7.

**name:** Bio-Stabilizer

**activation:** Passive

**cost:** Feat choice

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Always

**effect:** While at least two mutations are active, Bloodthick Node heals 1 additional HP on each of its valid encounter-only regeneration pulses.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: +1 to valid Bloodthick pulse; no independent heal.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## wizard.engine[10]

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · X

Source data/public/class_playtests/wizard.json / 10 · SHA256 673521960e487b21772372733af6aaa0c478c7f3308b6a58607a3c5ac2d83f99.

**text:** ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Temp HP/max-HP school effects; Necromancy tempHP is not healing.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.

## wizard.hero.necromancer.infernal-pact-quest-based-unlock

**REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only** · TH/FI

Source data/public/class_playtests/wizard.json / wizard.hero.necromancer.infernal-pact-quest-based-unlock · SHA256 3ec78d206b84e52afbca7eefd488313b4aeb4371a3edb80e5f9e6e14636d053d.

**name:** Infernal Pact (Quest-based unlock)

**activation:** Bonus Action

**cost:** 3 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Maximum 3 rounds

**frequency:** 1/long rest; quest-gated

**effect:** Infernal Pact — Gravebrand. Tags: hero, necromancer, infernal, necrotic, dark-content. This card can be selected only after completing the campaign's Infernal Pact quest and its dark-trauma check-in. Mark one creature. At the start of each of its turns it makes a Constitution save; on failure it takes 1d6 necrotic damage and you regain HP equal to the actual damage dealt, maximum S+M; success ends Gravebrand. Gravebrand ignores necrotic resistance but not immunity. While you possess this Pact, Corpse Harvest and Auto-Raise may also treat Fiend corpses as eligible; other creature types remain ineligible.

**Overlay:** FIRST PROPOSAL; read later source corrections before implementing: Target-start damage; heal from actual damage, max3-round source; not a healing pulse itself.

**Overlay:** BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.

**Overlay:** Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities.

**Open:** Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target.
