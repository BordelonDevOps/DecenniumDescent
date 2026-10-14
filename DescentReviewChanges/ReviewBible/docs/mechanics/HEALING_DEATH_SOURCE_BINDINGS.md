# Healing and death source reference

**REVIEWED / reference-VALIDATED — selected153-source interface only — 153 selected source records.** An index is not a reviewed procedure.

Exact costs, actions, target limits, clocks and restrictions are retained below. Operational overrides only supersede the stated part of a procedure; original objects remain unchanged.

## class-engine:cleric:7

**REVIEWED / reference-VALIDATED — classified components only** · BOOK/guard: healing/resurrection limits

Source: `data/public/class_playtests/cleric.json` / `7`. SHA256 `bb84e1b0f1d02ca1f307edee719b2e66036799f2367b1b93511681a7f95dd455`.

**text:** Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.base.healing-rite

**REVIEWED / reference-VALIDATED — classified components only** · HEAL ordinary

Source: `data/public/class_playtests/cleric.json` / `cleric.base.healing-rite`. SHA256 `20a27516ae922475d5979c529d88a5f83d4a29cff8e8ce063b46f1009be73e2f`.

**name:** Healing Rite

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One living ally within 30 feet

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Healing Rite. Tags: rite, healing. One living ally regains S d8 + M HP. It cannot restore a dead creature or remove Wounds. Consecrated Ground and appropriate Invocation Path bonuses may modify this healing.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.saint.divine-rebirth

**REVIEWED / reference-VALIDATED — classified components only** · RESURRECTION MODIFIER

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.divine-rebirth`. SHA256 `0911a56a90621bfce24642033cfd99929553c077fa641efacc48d90d4b94e15a`.

**name:** Divine Rebirth

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One ally revived by your Cleric feature

**duration:** Instantaneous plus temporary HP for 1 minute

**frequency:** 1/long rest

**effect:** Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.saint.unyielding-light

**REVIEWED / reference-VALIDATED — classified components only** · LIVING-ZERO HP RECOVERY

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.unyielding-light`. SHA256 `2b13f1c09c2c7fba28eb3ac046a34ff52f8a829eafac020aa33b762a96d4236d`.

**name:** Unyielding Light

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Up to six living party members within 30 feet, including you

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Unyielding Light. Tags: saint, emergency, healing. When one damage event would leave every conscious living party member within 30 feet at 0 HP, resolve that damage, then before ordinary death-save progression each qualifying living creature at 0 HP regains floor(maximum HP/3), minimum 1. It cannot revive a creature killed outright and removes no Wounds. This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.saint.celestial-resurgence

**REVIEWED / reference-VALIDATED — classified components only** · RESURRECTION

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.celestial-resurgence`. SHA256 `67fbbe3e612fe1dbe47ab927928e4bb8c392086d02926c0059cf915f6d309309`.

**name:** Celestial Resurgence

**activation:** Action

**cost:** 5 Conviction + 10 RP

**rangeAndTarget:** Up to six allied corpses within 30 feet that died during the previous 3 rounds

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Final Miracle — Celestial Resurgence. Tags: saint, finale, resurrection, rite. Each legal target returns to life at 1 HP. The body must be sufficiently present to sustain life. This removes no Wounds, curses or other death consequences. Divine Rebirth may modify one returned ally if available. The Conviction expenditure can vent Dissonance once under the common rule.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.saint.mass-healing-light

**REVIEWED / reference-VALIDATED — classified components only** · HEAL

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.mass-healing-light`. SHA256 `dbb502b5ecb5d64d0973a9df82f770cdb8af28300d09a7f6f978d3fef13c2009`.

**name:** Mass Healing Light

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** Up to six living allies within 30 feet

**duration:** Instantaneous

**frequency:** Recharge 3 rounds

**effect:** Mass Healing Light. Tags: saint, healing. Roll S d8 + M once. Each target regains that amount. A target below half maximum HP when chosen regains an additional 1d8 HP. Roll that bonus once and apply it to all qualifying targets. This cannot revive the dead or remove Wounds.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.saint.resurrection

**REVIEWED / reference-VALIDATED — classified components only** · RESURRECTION

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.resurrection`. SHA256 `c30ea74832ad72360d7e3dfff95ca1b7514996ae818b04aa1b59928e93cdf67d`.

**name:** Resurrection

**activation:** Action

**cost:** 3 Conviction + 10 RP

**rangeAndTarget:** One allied corpse you touch that died within the previous 1 minute

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Resurrection. Tags: saint, resurrection, rite. Return the target to life at 1 HP and grant it 2 S + M temporary HP for 1 minute. It gains no removed Wounds and receives no restored expended resources beyond what another rule explicitly provides. A missing vital body prevents the effect. The Conviction expenditure can vent Dissonance once.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.cultist.blasphemous-tongue

**REVIEWED / reference-VALIDATED — classified components only** · HEALING REDUCTION / ALREADY Doomed

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.blasphemous-tongue`. SHA256 `793dec5aa60dff80f8da02ed52a55b22c28c0b8975ca949d9dc9bf4374e6f1c6`.

**name:** Blasphemous Tongue

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Enemies affected by your Sacrament

**duration:** Until the next Sacrament pulse or effect end

**frequency:** Once per target per pulse

**effect:** Blasphemous Tongue. Tags: cultist, sacrament, doomed. At each pulse of your Sacrament, each enemy affected by that pulse makes a Wisdom save. On failure it becomes Doomed until the next pulse. While Doomed, HP healing it receives is reduced by S+M, minimum 0, and each positive timed buff on it counts down one additional round at the end of its turn. Repeated failures refresh rather than stack.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.cultist.rite-of-the-crimson-choir

**REVIEWED / reference-VALIDATED — classified components only** · COMPANION + LIFE-DRAIN HEALING, not resurrection

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.rite-of-the-crimson-choir`. SHA256 `8a0609352a89fd9dee65f38e363372e1dc9bc50876b68e3e90b2e7761ad553bf`.

**name:** Rite of the Crimson Choir

**activation:** Action

**cost:** 5 Conviction + 8 RP

**rangeAndTarget:** Four unoccupied spaces within 30 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** 1/long rest

**effect:** Final Miracle — Rite of the Crimson Choir. Tags: cultist, finale, summon, rite. Summon four spectral fanatics. Each has AC 14, 10 HP, Speed 30 feet and cannot take Reactions. Spend one Bonus Action on your regular turn to command the Choir; this explicitly priced Finale permits up to four surviving fanatics to each move up to its Speed and make one melee spell-like attack using your Cleric technique attack bonus against an enemy within 5 feet; on hit it deals 1d6+S necrotic damage and you regain 1 HP, maximum 4 HP per round from the Choir. When a fanatic reaches 0 HP, when concentration ends or after the third round, it explodes; enemies within 5 feet make Dexterity saves, taking 1d6 necrotic on failure or half on success. Fanatics grant no XP, loot, corpse, resurrection target or Conviction. The Conviction expenditure can vent Dissonance once.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.cultist.blood-sacrifice

**REVIEWED / reference-VALIDATED — classified components only** · DIRECT HP LOSS WITH 1-HP COST FLOOR

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.blood-sacrifice`. SHA256 `073e2e574467aaae7193dfd80d27b74c4b3ccc4db41a45a4d59ab3208ad335fe`.

**name:** Blood Sacrifice

**activation:** Bonus Action

**cost:** Lose S+M actual HP from yourself or one willing ally within 5 ft

**rangeAndTarget:** Self or one willing ally within 5 feet

**duration:** Empowerment lasts until end of your next regular turn

**frequency:** 1/short rest

**effect:** Blood Sacrifice. Tags: cultist, sacrifice, conviction. The chosen creature loses S+M actual HP; this loss cannot be reduced, redirected or transferred and cannot reduce it below 1 HP. The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain 1 Conviction. Your next damaging or healing Rite or Invocation before the end of your next regular turn adds 1d8 to one rolled damage or healing component. A creature must be willing unless the target is you.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.cultist.ritual-of-undeath

**REVIEWED / reference-VALIDATED — classified components only** · COMPANION REANIMATION + WOULD-DIE REPLACEMENT

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.ritual-of-undeath`. SHA256 `3a49348b309930d66ab43fb15262c7062c7849daca1a4939beb6d27d22f9bea1`.

**name:** Ritual of Undeath

**activation:** Action

**cost:** 3 Conviction + 6 RP

**rangeAndTarget:** One eligible corpse within 30 feet or one living ally within 30 feet

**duration:** Mode-dependent

**frequency:** 1/long rest

**effect:** Ritual of Undeath. Tags: cultist, undead, rite. Choose one mode. Corpse Servant: one humanoid corpse dead no more than 1 minute rises for 3 rounds as a temporary thrall with AC 13, 10 HP, Speed 30 feet and one attack only when you spend your shared companion Bonus Action command using your Cleric technique attack bonus; on hit it deals S d6 necrotic. The thrall disappears at 0 HP or when duration ends and grants no XP, loot, new corpse, Conviction or resurrection target. Death Ward: one living ally is marked for 1 minute; the first time it would die during that duration, it instead remains at 1 HP and counts as both humanoid and undead until the end of its next turn. Neither mode removes Wounds. The Conviction expenditure can vent Dissonance once.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Would-die Ward can replace damage or non-damage death if body/explicit source eligibility permits. Positive pre-eventHP→1 is loss prevention through Decay; already0 blockedHP→Stable0 with immediate d4-hour deadline. Stop same-packet skipped death branches. Reconcile retained lethal tracks.

## class-card:dragoon:dragoon.hero.dragon-guardian.bastion-descent

**REVIEWED / reference-VALIDATED — classified components only** · TEMP HP / damage protection, not healing

Source: `data/public/class_playtests/dragoon.json` / `dragoon.hero.dragon-guardian.bastion-descent`. SHA256 `e1005686e829ecea6d245c9627f8a22cb38f30ab26ee0c4daa97837ac5e58671`.

**name:** Bastion Descent

**activation:** Action

**cost:** 5 Momentum; 1 long-rest use

**rangeAndTarget:** Leap within 30 ft; up to 6 allies within 15 ft of landing

**duration:** Instant; protection until start next turn

**frequency:** 1/long rest

**effect:** Land in empty space. Chosen allies gain 4d8+M temporary HP and may end Frightened or Poisoned. They gain resistance to the next damage instance before your next turn. No healing, resurrection or removal of Wounds.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mage:mage.hero.archmage.harmonized-core

**REVIEWED / reference-VALIDATED — classified components only** · TEMP HP, explicitly not healing

Source: `data/public/class_playtests/mage.json` / `mage.hero.archmage.harmonized-core`. SHA256 `7d1df6cb40daec1f188736404c612c8f9a7305f874f3d21a7f335706b17fea64`.

**name:** Harmonized Core

**activation:** Passive

**cost:** 0

**rangeAndTarget:** One ally within 30 feet

**duration:** Temporary HP until lost or replaced

**frequency:** At most once per turn

**effect:** Harmonized Core. Tags: archmage, support. After one of your damaging Mage spells deals damage, choose one ally within 30 feet. It gains temporary HP equal to 10% of one target's unmodified rolled damage dice total from that spell, rounded down, minimum 1 and maximum S+M. This is not HP healing and cannot trigger healing features or Echo-style repetitions.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mage:mage.hero.lich.undying-spellform

**REVIEWED / reference-VALIDATED — classified components only** · CONSCIOUS-AT-ZERO STATE

Source: `data/public/class_playtests/mage.json` / `mage.hero.lich.undying-spellform`. SHA256 `f9eb71c6354a879da6fb752283a2e78cf2330465e97605dae15c939ecf413cea`.

**name:** Undying Spellform

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until end of your next regular turn

**frequency:** 1/long rest

**effect:** Undying Spellform. Tags: lich, undead, death. When damage reduces you to 0 HP without killing you outright, remain conscious and able to take Actions until the end of your next regular turn. You remain at 0 HP, cannot benefit from voluntary movement faster than half Speed, and still suffer ordinary consequences of further damage. If still at 0 HP when the effect ends, become unconscious and suffer one failed death save. Healing above 0 ends this feature early.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Partial zero override: speech, half movement, normal Action and concentration allowed; no independent BA/Reaction. Existing concentration avoids automatic zero loss but damage save remains. Separate restrictions apply. Expiry at0 destabilizes and adds1 failure.

## class-card:mage:mage.hero.lich.soul-reservoir

**REVIEWED / reference-VALIDATED — classified components only** · RESOURCE trigger, no healing

Source: `data/public/class_playtests/mage.json` / `mage.hero.lich.soul-reservoir`. SHA256 `ec8ad792a975cf5bef6d4b070ad1d5e9a977b33ad1f305c9a7bd6a982170ef61`.

**name:** Soul Reservoir

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** At most once per turn and at most S times per encounter

**effect:** Soul Reservoir. Tags: lich, resonance, damage-over-time. During a real encounter, when a hostile creature takes damage from a damage-over-time effect created by one of your Mage spells, restore 1 RP, never above maximum. The same damage event cannot restore more than 1 RP. Damage to allies, summons, trivial creatures or your own companions does not qualify.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mage:mage.hero.lich.resonance-to-flesh

**REVIEWED / reference-VALIDATED — classified components only** · HEAL / DIRECT HP COST depending mode

Source: `data/public/class_playtests/mage.json` / `mage.hero.lich.resonance-to-flesh`. SHA256 `5692ac39a7de506bcf79cfcb7273630cf1f18c27e6d663ae380f764b78e3e8b2`.

**name:** Resonance to Flesh

**activation:** Action

**cost:** Variable conversion

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mage:mage.hero.lich.soulbound-ritual

**REVIEWED / reference-VALIDATED — classified components only** · COMPANION RECONSTRUCTION

Source: `data/public/class_playtests/mage.json` / `mage.hero.lich.soulbound-ritual`. SHA256 `402e1f7d3575a535865294094b40a0e028c23dff18e64dadc511f20340bc7b0a`.

**name:** Soulbound Ritual

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** One of your destroyed bound elite undead companions within 30 feet or its inert binding token

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:mirrorsage:5

**REVIEWED / reference-VALIDATED — classified components only** · BOOK anti-copy/resource guard

Source: `data/public/class_playtests/mirrorsage.json` / `5`. SHA256 `5d438f2023c519d89d890af09fc094f010346755f3bb3577d94a6463558865f6`.

**text:** Focus Point is a separate resource: when Mimicry Focus is known, receive 1 at encounter start, maximum 1, lost at encounter end. It can modify one Echo without generating another release, recapture or resource refund. No stacking damage doublings; use the printed modest die/range boost. Healing/support copies always consume RP and cannot restore RP or duplicate limited-use features.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mirrorsage:mirrorsage.hero.light-weaver.radiant-archive

**REVIEWED / reference-VALIDATED — classified components only** · SUPPORT COPY, explicitly no resurrection

Source: `data/public/class_playtests/mirrorsage.json` / `mirrorsage.hero.light-weaver.radiant-archive`. SHA256 `bed8021f25da9ec4a1f8d3da1806e0463bdf2177c6020e641e4758474ec78be6`.

**name:** Radiant Archive

**activation:** Action

**cost:** RP for 3 support Echoes; consume all 3; 1 long-rest use

**rangeAndTarget:** Up to 3 legal allies within 30 ft

**duration:** Instant/shield 1 minute

**frequency:** 1/long rest

**effect:** Release three stored Mend/Ward records as ONE package; assign each to one ally. No ally receives more than two components and temporary HP never stack. All costs paid; no extra release or resurrection. Missing records cannot be invented.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mirrorsage:mirrorsage.hero.light-weaver.divine-reflection

**REVIEWED / reference-VALIDATED — classified components only** · COPY/BOOK hook, excludes resurrection

Source: `data/public/class_playtests/mirrorsage.json` / `mirrorsage.hero.light-weaver.divine-reflection`. SHA256 `db590cbdf89b887f256428708cbf767fcd916e2dc06e5eb5268e23f69b60816b`.

**name:** Divine Reflection

**activation:** Reaction

**cost:** 2 RP; 1 long-rest use

**rangeAndTarget:** Willing allied caster within 30 ft just used an eligible healing/protection spell

**duration:** Store until spent

**frequency:** 1/long rest

**effect:** Capture a Mend or Ward profile of rank at most your learnable rank into empty slot. This explicit exception permits an allied source but excludes resurrection/resource/action generation. No extra captured use for the ally and no copying a copy.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:monk:16

**REVIEWED / reference-VALIDATED — classified components only** · BOOK healing/death guard

Source: `data/public/class_playtests/monk.json` / `16`. SHA256 `35f0120ff484cecb5d18360f6532891d2de393ba4d2b5e03a9961b7e2ab07a44`.

**text:** Healing from Monk cards cannot exceed maximum HP, restore the dead or remove Wounds unless explicitly stated. Permanent HP recovery and Ki generation cannot be farmed outside encounters. Resurrection effects are explicitly limited-use. No Monk card can instantly kill a target merely because a descriptive source used language such as Death Touch; death continues to follow the game's ordinary damage and dying rules.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.base.crane-stance-support

**REVIEWED / reference-VALIDATED — classified components only** · HEAL modifier + paid healing

Source: `data/public/class_playtests/monk.json` / `monk.base.crane-stance-support`. SHA256 `e674e9a4ae8aa0f0d52cd371b86e9173b9ba7f00a2447db64e31c14f44b42314`.

**name:** Crane Stance (Support)

**activation:** Passive

**cost:** 0 for stance; healing costs 1 Ki and 1 RP

**rangeAndTarget:** Self; one ally within 15 feet for healing rider

**duration:** While active

**frequency:** Automatic core stance

**effect:** Crane Stance. Tags: stance, support. While unarmored, whenever you move at least 15 feet on your turn, gain +1 AC until the start of your next turn. HP healing you receive from another creature gains +S HP once per round. When you begin an unarmed strike at exactly 5 Ki and hit, spend 1 Ki and 1 RP; you and one living ally within 15 feet each regain S+M HP, at most once per turn.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.hero.enlightened-master.breath-of-the-thousand-petals

**REVIEWED / reference-VALIDATED — classified components only** · HEAL + RESURRECTION + DAMAGE FLOOR

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.breath-of-the-thousand-petals`. SHA256 `ef8e3a96a396ed3d48f95c0e4138b0eae186fe297b746cae0c83c40004fa508e`.

**name:** Breath of the Thousand Petals

**activation:** Action

**cost:** 5 Ki + 5 RP

**rangeAndTarget:** Up to six allies within 20 feet

**duration:** Until start of your next regular turn

**frequency:** 1/long rest; automatic Hero Final

**effect:** Final — Breath of the Thousand Petals. Tags: hero, enlightened, final, resurrection, weave. Living or Downed allies in range regain 3 S d8+M HP. Up to two allied creatures that died since the end of your previous regular turn return to life at 1 HP if their bodies can sustain life. Until the start of your next turn, affected living allies cannot be reduced below 1 HP by damage, though instant-death effects still function. It removes no Wounds and cannot revive the same creature twice.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. At most6 total targets including at most2 eligible corpses. Each source Monk may resurrect each target identity once in the campaign. Living healing does not consume that history. Strict post-previous-end death marker; use/cost/floor clocks retained.

## class-card:monk:monk.hero.enlightened-master.healing-touch

**REVIEWED / reference-VALIDATED — classified components only** · HEAL

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.healing-touch`. SHA256 `ca275c05e4d877cf61c5267324d7cc9026d4e5cce39428e9821125f72d92555b`.

**name:** Healing Touch

**activation:** Action

**cost:** 2 Ki + 1 RP

**rangeAndTarget:** One living creature you touch

**duration:** Instantaneous

**frequency:** Recharge 2 rounds

**effect:** Healing Touch. Tags: hero, enlightened, healing, weave. The target regains S d8+M HP and may immediately repeat one saving throw against Poisoned or disease if that effect normally permits repeated saves. This does not resurrect, remove Wounds or automatically cure disease. It is a minor Weave technique; the common extra-Ki payment may prevent its 1 Dissonance.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.hero.enlightened-master.circle-of-harmony

**REVIEWED / reference-VALIDATED — classified components only** · PAID HEALING PULSES

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.circle-of-harmony`. SHA256 `df3b3c65b152fd7b3a217eac2e551b3fc473a00b9704fcbb98bfe0dc9611c4bd`.

**name:** Circle of Harmony

**activation:** Action

**cost:** 2 Ki + 3 RP to start; 1 RP maintenance

**rangeAndTarget:** 10-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, maximum 3 Monk turns

**frequency:** Recharge 4 rounds

**effect:** Circle of Harmony. Tags: hero, enlightened, healing, zone, weave, sustained. On start and each paid Bonus Action maintenance pulse, up to three living allies in the zone regain S d6+M HP. Maximum 3 pulses. A creature receives this named effect at most once per round. It removes no Wounds and cannot restore the dead.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.hero.enlightened-master.shared-breath

**REVIEWED / reference-VALIDATED — classified components only** · DAMAGE REDIRECT + HEALING ECHO

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.shared-breath`. SHA256 `da2757b79d797600e0823eed7b615b9165e4c9d81c88fbb6affa18018695c52e`.

**name:** Shared Breath

**activation:** Action

**cost:** 3 Ki + 2 RP

**rangeAndTarget:** One willing ally you touch

**duration:** Concentration, maximum 3 rounds

**frequency:** Recharge 4 rounds

**effect:** Shared Breath. Tags: hero, enlightened, link, weave. Link yourself to one willing ally. Once per round when either linked creature takes damage, the other may use its Reaction to take up to S+M of that damage instead; transferred damage cannot be reduced or redirected again. HP healing received by either creature also grants the other S HP once per round. The link ends if you separate by more than 30 feet.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Child healing shares root causal ledger. Every link application can fire once/root; no return path or sibling branch repeats an already visited link.

## class-card:monk:monk.hero.way-of-shadow.veinlock-nerve-jab

**REVIEWED / reference-VALIDATED — classified components only** · HP/FINITE-RESOURCE RECOVERY PROHIBITION

Source: `data/public/class_playtests/monk.json` / `monk.hero.way-of-shadow.veinlock-nerve-jab`. SHA256 `3bc079fb6588aa9fc7a9c545b06960c886198801a8862db231935f3b48b1247a`.

**name:** Veinlock Nerve Jab

**activation:** Triggered

**cost:** 2 Ki

**rangeAndTarget:** One creature hit by your unarmed strike

**duration:** Maximum 2 rounds

**frequency:** Recharge 3 rounds

**effect:** Veinlock Nerve Jab. Tags: hero, shadow, attack, control. After an unarmed strike hits, spend 2 Ki. The target makes a Constitution save. On failure it cannot regain HP or finite class resources until the end of its next turn and repeats the save then; failure extends the effect one final round. If you were hidden from it when the strike began, the initial failed save also Silences it until the end of its next turn.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:oracle:3

**REVIEWED / reference-VALIDATED — classified components only** · BOOK: Oracle Curse persists through resurrection

Source: `data/public/class_playtests/oracle.json` / `3`. SHA256 `f6e9c61b425e06da50fb57ca05f565571fbb295f30460b42fe69cca65507121c`.

**text:** Choose exactly ONE Mystery and exactly ONE Curse at Oracle level 1. They are not parallel subclasses that stack. You never gain another Mystery or Curse unless a future explicit retraining or transformation rule says otherwise. Curse limitations are permanent and cannot be removed by ordinary cleansing, curse removal, resurrection or rest.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:oracle:13

**REVIEWED / reference-VALIDATED — classified components only** · BOOK: healing/resurrection guard

Source: `data/public/class_playtests/oracle.json` / `13`. SHA256 `915b1cf2d9327231bf75308605d2e2b72abdce2ce052fdecef493dea663af705`.

**text:** Healing from Oracle features cannot exceed maximum HP, resurrect the dead or remove Wounds unless a feature explicitly says so. Temporary HP never stack. Encounter-only regeneration and drain cannot be farmed outside meaningful combat. Corpse effects create no XP, loot, RC or repeatable corpse resources unless expressly stated.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.shared.oracle-s-burden

**REVIEWED / reference-VALIDATED — classified components only** · BOOK/protected class state

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.oracle-s-burden`. SHA256 `58600e513393987a382f64e53a11dbbf7c82e705ff8afb6e40fe6645dc6f8c02`.

**name:** Oracle's Burden

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 2

**effect:** Your selected Curse is recognized as an intrinsic Oracle class condition rather than an ordinary removable curse. Remove Curse, cleansing, resurrection and similar generic effects cannot remove or suspend it. Only a feature that explicitly names your Oracle Curse can suppress, transform or replace one of its effects.

**prerequisite:** Oracle 2

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.curse.wound-eater

**REVIEWED / reference-VALIDATED — classified components only** · HEALING MULTIPLIER / rest condition

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.curse.wound-eater`. SHA256 `b0523723ce95a44326adc752ad81f0d94103918e8af87bc432ba438d7d9e9302`.

**name:** Wound Eater

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Chosen once at Oracle 1

**effect:** LIMITATIONS: HP recovery from rests and from another creature's healing is halved, rounded down; your own Wound Eater drains and your own Revelations are not halved. Before a long rest completes, you must have successfully drained HP from a meaningful hostile living creature since your previous long rest or gain one level of Exhaustion after the rest. Your corpse-like appearance imposes disadvantage on the first friendly social check with an unfamiliar mortal who can clearly see you, unless circumstances make the appearance irrelevant.

**prerequisite:** Selected Curse: Wound Eater

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.false-life.false-life-boon-i

**REVIEWED / reference-VALIDATED — classified components only** · DAMAGE FLOOR + DEATH-SAVE DEATH REPLACEMENT

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.false-life.false-life-boon-i`. SHA256 `737564c9de90452f2445c4cf7d41e4d6ebc027a8dd490627bb8700e330692fbe`.

**name:** False Life — Boon I

**activation:** Passive; triggered survival

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent advantage; immediate survival

**frequency:** Survival 1/long rest

**effect:** advantage on saves against death effects and hostile necrotic/negative-energy effects. 1/long rest when you would die from failed death saves or be reduced to 0 by an effect that does not kill outright, remain at 1 HP instead.

**prerequisite:** Oracle 3; selected Curse:False Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Distinct positive-to-zero damage-floor and failed-death-save would-die replacement modes share the printed1/LR use. Do not promote this into an all-causes Ward.

## class-card:oracle:oracle.supplement.false-life.false-life-boon-ii

**REVIEWED / reference-VALIDATED — classified components only** · FEIGN-DEATH STATE, not death/revival

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.false-life.false-life-boon-ii`. SHA256 `cbe8f3409a5366d074c5f40995c7f32ae95a3e81cc224d5cc0d559107c92b6ce`.

**name:** False Life — Boon II

**activation:** Action

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until voluntarily ended or one minute

**frequency:** 1/encounter

**effect:** once per encounter as an Action feign perfect death for up to 1 minute. You remain conscious but cannot move, speak, take Actions or Reactions; ordinary undead ignore you unless you attack or otherwise reveal yourself. End the effect voluntarily at the start of your turn.

**prerequisite:** Oracle 5; selected Curse:False Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.false-life.false-life-boon-iii

**REVIEWED / reference-VALIDATED — classified components only** · CONSCIOUS-AT-ZERO STATE

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.false-life.false-life-boon-iii`. SHA256 `85d55f1cb5629d4e63245bb644d55f30fd5c23d5d0ee8fd4a38245df817fb0b5`.

**name:** False Life — Boon III

**activation:** Triggered when reduced to 0 HP

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until end of next regular turn

**frequency:** 1/long rest

**effect:** 1/long rest when reduced to 0 HP without instant death, remain conscious until the end of your next regular turn. During that turn choose either move up to your Speed, speak normally or activate one Revelation; you cannot do more than one of those options. If still at 0 afterward, become unconscious normally.

**prerequisite:** Oracle 10; selected Curse:False Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Exactly one permitted turn choice: move, speak or Revelation using its printed activation/costs. Revelation can start concentration; prior concentration is not preserved by this feature.

## class-card:oracle:oracle.supplement.ancestor.echo-armor

**REVIEWED / reference-VALIDATED — classified components only** · DAMAGE REDUCTION + 1-HP FLOOR

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.ancestor.echo-armor`. SHA256 `32761e631f565378d31fdfc1aa9abb37e9eea99fd4864bdeb30380cf04b4864e`.

**name:** Echo Armor

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Damage reduction always; death prevention 1/short rest

**effect:** Reduce the first nonmagical weapon damage you take each round by PB, minimum 0. Once per short rest, when damage would reduce you to 0 HP without killing you outright, remain at 1 HP instead. The prevention removes no Wounds and cannot trigger if another effect has already prevented that same reduction to 0.

**prerequisite:** Oracle 6; Mystery: Ancestor; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.ancestor.echo-crowned

**REVIEWED / reference-VALIDATED — classified components only** · ALLY 1-HP FLOOR / RC option

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.ancestor.echo-crowned`. SHA256 `7991906ef73bc0ffdfef0fa2a8d0ec79f288f9d0c8ad362042754a88c5d3bcad`.

**name:** Echo Crowned

**activation:** Passive and Bonus Action

**cost:** 0 RC to maintain spirits; Revelation costs normally unless stated

**rangeAndTarget:** Self; death prevention ally within 5 tiles

**duration:** Permanent spirits; activated effects instantaneous

**frequency:** Double-cast 1/long rest; each spirit may be sacrificed once per long rest

**effect:** Maintain three named ancestral Echoes: Offense grants +1 on your first Revelation attack each round; Defense reduces the first damage you take each round by S; Utility grants advantage on one History, Insight or Perception check per round. Once per long rest, when you activate a known Revelation, you may pay its RC cost twice and resolve it twice as part of the same action against different legal targets; copied resolution cannot duplicate resource or action triggers. You may sacrifice one currently available Echo as a Reaction when an ally within 5 tiles would be reduced to 0 HP to leave that ally at 1 HP instead, or as a Bonus Action to restore your RC to maximum. A sacrificed Echo provides no passive benefit until your next long rest.

**prerequisite:** Oracle 20; Mystery: Ancestor

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.battle.battle-prophecy-trigger

**REVIEWED / reference-VALIDATED — classified components only** · RESOURCE trigger at hostile 0 HP

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.battle.battle-prophecy-trigger`. SHA256 `75d18b4ec0942414870a4519e988e3793340394c21b7f8b5cdf846538679c5d8`.

**name:** Battle Prophecy Trigger

**activation:** Triggered

**cost:** 0 RC

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** At most once per round during a real encounter

**effect:** When you or an ally reduces a meaningful hostile creature to 0 HP, regain 1 RC, never above maximum. Summoned, trivial, friendly or repeatedly revived creatures do not qualify.

**prerequisite:** Oracle 1; Mystery: Battle

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.battle.avatar-of-the-war-chorus

**REVIEWED / reference-VALIDATED — classified components only** · ALLY 1-HP FLOOR / resource banners

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.battle.avatar-of-the-war-chorus`. SHA256 `275127469d779f546ed83820f67a70bc3aadfc67389ffbd40b07b952bf05aa47`.

**name:** Avatar of the War Chorus

**activation:** Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self and allies within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** Manifest three banners for 3 rounds. Offense Banner: once on each of your turns add 2 S damage to one weapon or Revelation damage roll. Defense Banner: gain +2 AC; allies within 5 tiles reduce first damage each round by 1. Rally Banner: once per round one ally within 5 tiles gains +1 on an attack roll made during its turn. Your known Tier I Battle Revelations cost 0 RC while all three banners remain. You may sacrifice one banner as a Reaction to leave an ally within 5 tiles at 1 HP instead of 0, or as a Bonus Action to restore your RC to maximum; that banner's benefit ends immediately. When the 3-round effect ends naturally, regain 2 RC, never above maximum. The Final grants no more than one additional full Action per creature per round.

**prerequisite:** Oracle 20; Mystery: Battle

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.bones.bones-prophecy-trigger

**REVIEWED / reference-VALIDATED — classified components only** · RESOURCE trigger on actual death

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.bones-prophecy-trigger`. SHA256 `bed997b4dca4f52173fb62c19633c42c565fa351eea1c43db2617ddc68aa55c1`.

**name:** Bones Prophecy Trigger

**activation:** Triggered

**cost:** 0 RC

**rangeAndTarget:** Self; qualifying creature within 5 tiles

**duration:** Instantaneous

**frequency:** At most once per round during a real encounter

**effect:** When an undead creature or meaningful hostile creature at 0 HP within 5 tiles dies, regain 1 RC, never above maximum. Summoned, friendly, trivial or repeatedly revived creatures cannot trigger this recovery.

**prerequisite:** Oracle 1; Mystery: Bones

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.bones.marrow-drain

**REVIEWED / reference-VALIDATED — classified components only** · LIFE-DRAIN HEAL + HP-RECOVERY BLOCK

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.marrow-drain`. SHA256 `107b79b9c3ad5f3e3bed99fdabc6543043cc73cd8adbe0852fbdda3c9e6deb77`.

**name:** Marrow Drain

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One creature you can touch

**duration:** Instantaneous; healing lock until end of your next turn against undead

**frequency:** At will while RC remains

**effect:** Make a Revelation attack. On hit deal 2d6 necrotic damage and regain HP equal to half the actual damage dealt, rounded down, maximum S+M HP. Against undead, deal 3d6 necrotic instead and the target cannot regain HP until the end of your next turn. Constructs are immune to the healing-drain portion. This healing removes no Wounds.

**prerequisite:** Oracle 3; Mystery: Bones; selected Tier I Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.bones.rotting-touch

**REVIEWED / reference-VALIDATED — classified components only** · ALREADY Decay / broad HP prohibition + corpse block

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.rotting-touch`. SHA256 `2a184115c77c3e39626229f0d95c4b73218e849b6ccc078dd5ae170ccfdf3475`.

**name:** Rotting Touch

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One creature you can touch

**duration:** Maximum 3 rounds

**frequency:** At will while RC remains

**effect:** Make a Revelation attack. On hit the target makes a Constitution save. On failure it gains Decay for up to 3 rounds: attacks against it add S damage once per attacker per turn, it takes -1 on saving throws and cannot regain HP. At the end of each turn it repeats the save, ending Decay on success. Corpses within 2 tiles of a Decayed creature cannot be raised while Decay persists. If the target is undead, it also takes 2d6 necrotic damage on the initial hit and you regain half the actual damage dealt, capped at S+M HP. At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack.

**prerequisite:** Oracle 6; Mystery: Bones; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.flame.undying-ember

**REVIEWED / reference-VALIDATED — classified components only** · SELF 1-HP FLOOR + ordinary ally healing

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.flame.undying-ember`. SHA256 `93821a63698a0c05d1300f12c7ea95211f4c0796d8f1300e2e491384ddf5cb90`.

**name:** Undying Ember

**activation:** Triggered

**cost:** 0 RC

**rangeAndTarget:** Self; enemies adjacent to you; allies within 2 tiles

**duration:** Instantaneous; enemy penalty until end of next turn

**frequency:** 1/long rest

**effect:** When damage would reduce you to 0 HP without killing you outright, remain at 1 HP. Adjacent enemies make Dexterity saves, taking 2d6 fire damage on failure or half on success; failing enemies also take -1 on attack rolls until the end of their next turn. Up to three living allies within 2 tiles each regain 1d6 HP. This removes no Wounds and cannot trigger from self-inflicted staged damage.

**prerequisite:** Oracle 6; Mystery: Flame; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.bloom-ward

**REVIEWED / reference-VALIDATED — classified components only** · HEAL modifier + damage absorb

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.bloom-ward`. SHA256 `0252c7014f1020fe92cdd9c29f41c074d47a6d8c6babf5665f939529eb6a0543`.

**name:** Bloom Ward

**activation:** Passive and Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self; allies within 2 tiles; one ally within 3 tiles for bloom

**duration:** Passive permanent; bloom until consumed or 1 minute

**frequency:** Bloom 1/long rest

**effect:** Once per round when a living ally within 2 tiles receives HP healing from a paid or finite-use effect, add S HP to that healing. Reduce the first necrotic or poison damage you take each round by 1. Once per long rest place a protective bloom on one ally within 3 tiles. It absorbs the next 10+Oracle level damage dealt to that ally, then ends. When it ends, the ally gains +1 on saves against Frightened until the end of its next turn.

**prerequisite:** Oracle 1; Mystery: Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.overflowing-light

**REVIEWED / reference-VALIDATED — classified components only** · HEAL + excess-to-temp-HP conversion

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.overflowing-light`. SHA256 `79723edccb03063801846d1d9dbb9c5b945cb4f49a797b55efb410c72042cc33`.

**name:** Overflowing Light

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One living ally within 4 tiles

**duration:** Healing instantaneous; temporary HP 2 rounds

**frequency:** At will while RC remains

**effect:** The target regains 2d6+M HP. Healing exceeding its maximum becomes temporary HP, maximum 10, lasting 2 rounds. When those temporary HP expire naturally, if at least 1 remains the target may end one of Frightened, Poisoned or Staggered. This cannot resurrect, remove Wounds or convert deliberately wasted healing into more than 10 temporary HP.

**prerequisite:** Oracle 3; Mystery: Life; selected Tier I Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.thorned-shelter

**REVIEWED / reference-VALIDATED — classified components only** · HEAL modifier

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.thorned-shelter`. SHA256 `f5eae57f57896210e6d0cee18d477d87d3e99e28f33be7cbf9e1dfdd92929dda`.

**name:** Thorned Shelter

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One living ally within 3 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** The target gains +2 AC and reduces the first damage it takes each round by S. Once per round when it receives HP healing from another finite effect, add 1 HP. The first melee attacker to damage it each round takes 1d4 piercing damage and must make a Strength save; on failure its Speed becomes 0 until the end of that current turn. This movement restriction is not a full-turn denial.

**prerequisite:** Oracle 3; Mystery: Life; selected Tier I Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.verdant-pulse

**REVIEWED / reference-VALIDATED — classified components only** · post-heal rider + ally 1-HP floor

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.verdant-pulse`. SHA256 `feb0f82538549fb2d540cfa9a68b89f517d4f1138b44ade546065fc7300c24f9`.

**name:** Verdant Pulse

**activation:** Passive and Reaction

**cost:** 0 RC

**rangeAndTarget:** Allies you heal; emergency ally within 4 tiles

**duration:** Buff until end of ally's next turn; emergency instantaneous

**frequency:** Buff once per ally per short rest; emergency 1/encounter

**effect:** When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it.

**prerequisite:** Oracle 6; Mystery: Life; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.song-of-mending

**REVIEWED / reference-VALIDATED — classified components only** · HEAL pulses + per-ally 1-HP floor

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.song-of-mending`. SHA256 `ca7500f38966fc943c0398ff2fbddfe96070ca9caf15a6d0b24cee7d2fa2def1`.

**name:** Song of Mending

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** Living allies within 5 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** On activation and at the start of your next regular turn, each living ally still within 5 tiles regains 2d6 HP, for exactly two possible pulses per use. Once during the duration for each ally, when one damage event would reduce it below 1 HP without instant death, it remains at 1 HP instead. When this prevention triggers, that ally may end Frightened or Poisoned and gains +S HP the next time a separate finite healing effect restores HP before Song ends. This removes no Wounds and cannot resurrect.

**prerequisite:** Oracle 9; Mystery: Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.eternal-bloom

**REVIEWED / reference-VALIDATED — classified components only** · pre-recorded HEAL reserve + per-ally 1-HP floor

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.eternal-bloom`. SHA256 `3d97cb828d42d1ec6f4f674e4328a37f916f47c15513a4e357cff80a706f7d02`.

**name:** Eternal Bloom

**activation:** Action

**cost:** 0 RC

**rangeAndTarget:** 5-tile-radius fixed sanctuary centered within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** When Eternal Bloom appears, record each living ally's missing HP while it is inside the zone. Divide that recorded missing HP into three healing installments as evenly as possible, with any remainder assigned to earlier pulses. On activation and at the start of each of your next two regular turns, each qualifying ally still inside regains its next installment; later damage does not increase this reserve. Once per ally during the Bloom, when damage would reduce it to 0 HP without instant death, it remains at 1 HP instead. Allies in the zone have necrotic immunity for the 3 rounds. When the Bloom ends, petals create light obscurement in the zone until the start of your next turn. It removes no Wounds and does not resurrect.

**prerequisite:** Oracle 20; Mystery: Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.base.protective-stance

**REVIEWED / reference-VALIDATED — classified components only** · DAMAGE REDIRECTION, not healing

Source: `data/public/class_playtests/paladin.json` / `paladin.base.protective-stance`. SHA256 `71f0333a1fa9bee2ffd004f8327f542364d847dfd263df4bf80cb0fe324de5c7`.

**name:** Protective Stance

**activation:** Bonus Action

**cost:** One short-rest use

**rangeAndTarget:** Self; adjacent ally

**duration:** Until start next turn

**frequency:** 1/short rest

**effect:** Gain+1 AC. Once before end, Reaction interpose for adjacent ally hit by weapon: reduce its damage by S+M and take that much unpreventable damage yourself. Cannot redirect again or create resource/damage triggers. You must remain conscious.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.base.sacred-touch

**REVIEWED / reference-VALIDATED — classified components only** · STABILIZATION, explicitly not healing

Source: `data/public/class_playtests/paladin.json` / `paladin.base.sacred-touch`. SHA256 `81444695d2cf9e5c54afee5721c29da4344543618244dde801758dde43744ac0`.

**name:** Sacred Touch

**activation:** Action

**cost:** 0 for stabilize; 1 RP for inspection

**rangeAndTarget:** One living creature touched

**duration:** Instant

**frequency:** At will with resources

**effect:** Stabilize a living Downed creature at 0 HP without healing; damage/ordinary rules can end stability. Alternatively pay 1 RP and examine 1 minute to learn whether one curse/disease affects it, without revealing origin or cure. No resurrection or free healing.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-shared.last-reproach

**REVIEWED / reference-VALIDATED — classified components only** · ordinary ally HEAL after damage

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-shared.last-reproach`. SHA256 `895f333185c3eb243fcbe76dcc36a38ed52f8b1f4994746abf250a0102f7015d`.

**name:** Last Reproach

**activation:** Reaction after an enemy damages an ally

**cost:** 10 RP

**rangeAndTarget:** That enemy 60 ft; one living ally in your aura

**duration:** Instant

**frequency:** 1/short rest

**effect:** New rank 5 Forbidden spell. Enemy WIS save for 3 S d8 necrotic, half success; ally regains S d8 HP after triggering damage. Does not revive dead or undo conditions. Uses ordinary spell strain and your Reaction.

**prerequisite:** Paladin 17; selected Oathbreaker inversion

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-mercy.aura-of-mercy

**REVIEWED / reference-VALIDATED — classified components only** · HEAL modifier

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.aura-of-mercy`. SHA256 `2601db1c3ead6e19e3cda88af15a2f7525e96d2d2a1171d037fc874d9c47ae35`.

**name:** Aura of Mercy

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen allies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** The first time each round a selected ally receives HP healing from a finite or paid effect, add S HP. Each selected ally also reduces the first necrotic damage it takes each round by S. These benefits do not stack with another Aura of Mercy from the same source.

**prerequisite:** Paladin 3; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-mercy.miracle-veil

**REVIEWED / reference-VALIDATED — classified components only** · persistent 1-HP DAMAGE FLOOR

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.miracle-veil`. SHA256 `17846f0aa17add447d160181b21e32f4862576de60848c44818d39fdeff7a3ee`.

**name:** Miracle Veil

**activation:** Reaction

**cost:** 2 RP

**rangeAndTarget:** One living ally in your Oath aura

**duration:** Until start of your next regular turn

**frequency:** 1/short rest

**effect:** Trigger when the ally would be reduced below 1 HP by damage. Until the start of your next regular turn, that ally cannot be reduced below 1 HP by damage. The Veil does not prevent instant-death effects that explicitly bypass HP, does not resurrect a dead creature and removes no Wounds. Damage and attached conditions still resolve normally except for the HP floor.

**prerequisite:** Paladin 11; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-mercy.blessing-of-the-meek

**REVIEWED / reference-VALIDATED — classified components only** · HEAL

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.blessing-of-the-meek`. SHA256 `de83f7216e4f442bf324e7e9650e69091077d79b1be79d0753257dfbce13cde4`.

**name:** Blessing of the Meek

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One living ally within 30 feet

**duration:** Healing instantaneous; AC bonus until start of your next regular turn

**frequency:** At will while RP remains

**effect:** The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules.

**prerequisite:** Paladin 3; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-mercy.grace-reversal

**REVIEWED / reference-VALIDATED — classified components only** · RESURRECTION Reaction

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.grace-reversal`. SHA256 `51322e780d7ca204f39320d5cc583699a3f9a18ebc8f4e67db3feef638deec44`.

**name:** Grace Reversal

**activation:** Reaction

**cost:** 10 RP

**rangeAndTarget:** One allied corpse in your Oath aura that died since the end of your previous regular turn

**duration:** Instantaneous

**frequency:** At most once per creature per long rest

**effect:** Trigger when you are reduced to 0 HP without being killed outright. One eligible allied corpse returns to life at 1 HP. You remain at 0 HP and resolve your own dying state normally. The revived ally retains Wounds and expended resources and must have a body capable of sustaining life. Grace Reversal cannot target you.

**prerequisite:** Paladin 17; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Only source-specific post-zero Reaction window after survival/Wounds, before zero Reaction loss finalizes. No self-target. Identity history is per source Paladin/target until that Paladin Long Rest; death does not reset it.

## class-card:paladin:paladin.supplement.oath-of-mercy.grace-eternal

**REVIEWED / reference-VALIDATED — classified components only** · Miracle floor + post-floor HEAL

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.grace-eternal`. SHA256 `9144f23fd7fb45d1beb6c300bb20b85cd3eb172e4a6ac53003c0260770f94a25`.

**name:** Grace Eternal

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to 3 allies in your Oath aura

**duration:** Until start of your next regular turn

**frequency:** 1/long rest

**effect:** Apply Miracle Veil to up to 3 allies in your aura without spending its short-rest use or RP. Once during this Veil for each affected ally, if damage would reduce it to 0 HP, it remains at 1 HP and immediately regains 2d8 HP. It also gains necrotic resistance until the end of its next turn. During Grace Eternal you may use Lay on Hands once without an Action, but must still spend points from your current Lay on Hands pool and may target only one creature.

**prerequisite:** Paladin 20; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression

**REVIEWED / reference-VALIDATED — classified components only** · HEALING ×1/2

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression`. SHA256 `1613079d8c08dac41dc4b7fe98b3dbbf5f4534a28a2d30282e93522bd69fdbde`.

**name:** Healing Suppression

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** HP healing received by each selected creature is halved, rounded down. Temporary HP, damage prevention and resurrection are not healing for this effect. This suppression cannot reduce healing below 0 or convert prevented healing into damage.

**prerequisite:** Paladin 3; Oathbreaker — Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-vengeance.final-verdict

**REVIEWED / reference-VALIDATED — classified components only** · broad cannot-regain-HP rider

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.final-verdict`. SHA256 `588a235ef97e9f2d39ca847326623ea090b05676da713f90f447f75361e5582d`.

**name:** Final Verdict

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** One creature marked by you within 30 feet and at or below half maximum HP

**duration:** Instantaneous or empowerment until end of your next regular turn

**frequency:** At will while RP remains

**effect:** The marked target makes a Constitution save, taking 4 S d8 radiant damage on failure or half on success. On failure it also cannot regain HP until the end of its next turn. If that damage reduces it to 0 HP, use ordinary Downed/death rules; there is no percentage-HP execution. On success your next Smite against it before the end of your next turn uses maximum damage dice. This bounded damage replaces the source draft’s automatic reduction to 0 HP.

**prerequisite:** Paladin 17; Oath of Vengeance

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-flame.phoenix-rebirth

**REVIEWED / reference-VALIDATED — classified components only** · LIVING-ZERO HP HEAL, not resurrection

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.phoenix-rebirth`. SHA256 `0a38ac2a6f534b9b6eefaa79733078371cc3169aa85ed60b825247cdfdf6ffd9`.

**name:** Phoenix Rebirth

**activation:** Reaction

**cost:** 10 RP

**rangeAndTarget:** One living ally in your Oath aura reduced to 0 HP

**duration:** Revival instantaneous; fire shield until end of target's next turn

**frequency:** Once per combat per ally

**effect:** Trigger when the ally reaches 0 HP without being killed outright. It immediately regains HP equal to half its maximum, rounded down, minimum 1. Until the end of its next turn it has fire resistance. Once during that duration when a creature within melee reach damages it with a melee attack, that attacker takes 2d6 fire damage. Phoenix Rebirth removes no Wounds and cannot restore a creature destroyed beyond recovery.

**prerequisite:** Paladin 17; Oath of Flame

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified

**REVIEWED / reference-VALIDATED — classified components only** · PASSIVE-REGENERATION BLOCK

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified`. SHA256 `cbfc7808eaa7713c9e05331e24397dcbea9a3a6642ed0d08f088e4c582a950e8`.

**name:** Scorch the Sanctified

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected enemies cannot regain HP from passive regeneration. At the start of each selected enemy's turn it makes a Charisma save. On failure, one temporary beneficial magical effect on it chosen by the Director from eligible non-innate effects is suppressed until the start of its next turn. Immunities, class engines, permanent traits and attunement are never suppressed.

**prerequisite:** Paladin 3; Oathbreaker — Oath of Flame

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura

**REVIEWED / reference-VALIDATED — classified components only** · PASSIVE-REGENERATION BLOCK

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura`. SHA256 `ab791099a2d42dd7017f37b891cda2e14f4c1c3ae23f73ef652dd3f459028af2`.

**name:** Lifeleech Bloom Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets and one damage type at start of each turn

**effect:** Selected enemies cannot regain HP from passive regeneration. Also choose acid, cold, fire, lightning, necrotic, poison, radiant or thunder. A selected enemy's resistance to that chosen type is suppressed while it remains selected in the aura; immunity is never suppressed.

**prerequisite:** Paladin 3; Oathbreaker — Oath of the Ancients

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom

**REVIEWED / reference-VALIDATED — classified components only** · DAMAGE + LIFE-DRAIN HEAL + source-local target floor

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom`. SHA256 `08c5946db93747abe8a71ed1a6aa82258108a072d3873c9f85a8ddae94fba83f`.

**name:** Lifeleech Bloom

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 living creatures or plant creatures in your Oath aura

**duration:** Instantaneous

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. You regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. You may include willing allies among the targets, but they receive no protection and cannot be reduced below 1 HP by this Blasphemous Word. Constructs and ordinary unattended plants provide no healing.

**prerequisite:** Paladin 11; Oathbreaker — Oath of the Ancients

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-grief.echo-of-the-fallen

**REVIEWED / reference-VALIDATED — classified components only** · SPIRIT MANIFESTATION, explicitly not resurrection

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-grief.echo-of-the-fallen`. SHA256 `27c9f765ebbd0680287b9c51689a0065caa04ddea514aafb66ba6bd88a1aa0fa`.

**name:** Echo of the Fallen

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** One allied creature who died in your aura this encounter; one target within the former ally's normal weapon range or one ally in your aura

**duration:** Until start of your next regular turn

**frequency:** At most once per fallen ally per long rest

**effect:** Manifest the ally's spirit for one round. Choose one mode on cast. Strike: the spirit makes one attack using the deceased ally's last recorded ordinary weapon attack bonus and base weapon damage, with no class-resource riders, extra attacks or proc effects. Guard: one chosen ally in your aura gains +2 AC until the start of your next turn. The spirit is not resurrected, cannot be targeted and disappears afterward. The single spirit strike uses PB+CHA to hit and S d8+M damage of the original weapon type if the recorded profile would exceed either value. It consumes the shared damaging-companion-action budget for that round; no monster or high-level player stat-block duplication.

**prerequisite:** Paladin 17; Oath of Grief

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-grief.dirge-of-passage

**REVIEWED / reference-VALIDATED — classified components only** · HP-recovery prohibition on selected undead + death-save bonus

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-grief.dirge-of-passage`. SHA256 `df1f6705254fc3dcbf79d5c08aae5baf78e792c21ce9e059969dfe4627c62200`.

**name:** Dirge of Passage

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Memories of up to 2 fallen allies; creatures in your Oath aura

**duration:** 2 rounds

**frequency:** 1/long rest

**effect:** For 2 rounds maintain two Final Vigil memories simultaneously and gain both selected benefits. Up to three selected hostile undead in your aura take an additional S radiant damage from your first damaging Paladin feature each round and cannot regain HP. Living allies in your aura gain +2 on death saves. No spirit gains its own turn, resources, spellcasting or complete former statistics. This flat rider replaces blanket damage vulnerability and never doubles a whole attack.

**prerequisite:** Paladin 20; Oath of Grief

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura

**REVIEWED / reference-VALIDATED — classified components only** · RESURRECTION BLOCK + flat HEALING reduction

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura`. SHA256 `65f1ac74f274a2f171571f40d3ce938061c6e4c58fba8925270b949fcec183ff`.

**name:** Dirge of Ruin Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected living creatures cannot be returned from death while inside the aura, and HP healing they receive is reduced by S+M, minimum 0. This never converts healing into damage and cannot retroactively reverse a resurrection completed before the creature entered the aura.

**prerequisite:** Paladin 3; Oathbreaker — Oath of Grief

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin

**REVIEWED / reference-VALIDATED — classified components only** · broad cannot-regain-HP rider

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin`. SHA256 `16cc8982591672cdbad5aa34bf755e2c4b8024c032fb29dba978ec14eb4d6407`.

**name:** Dirge of Ruin

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 creatures in your Oath aura

**duration:** Damage instantaneous; healing block until end of next turn

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. A failing target cannot regain HP until the end of its next turn. This does not prevent temporary HP or remove healing already received.

**prerequisite:** Paladin 11; Oathbreaker — Oath of Grief

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-the-martyr-king.last-king-s-gift

**REVIEWED / reference-VALIDATED — classified components only** · 1-HP FLOOR + TEMP HP

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.last-king-s-gift`. SHA256 `ef3133f57d5da376b3755b09ca86e3140362b0ae00c199b68835114019d4c693`.

**name:** Last King’s Gift

**activation:** Reaction before ally falls to 0 HP

**cost:** 10 RP

**rangeAndTarget:** One living ally in your aura

**duration:** Instant prevention; temporary HP until lost or encounter end

**frequency:** Once per encounter per ally

**effect:** When damage would reduce the ally to 0 HP without killing it outright, it instead remains at 1 HP and gains temporary HP equal to your Paladin level after the triggering damage resolves. This does not reverse a completed death, remove Wounds or replenish any resource.

**prerequisite:** Paladin 17; Oath of the Martyr King

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura

**REVIEWED / reference-VALIDATED — classified components only** · conditional HP-healing gate only

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura`. SHA256 `e4341a3bd789ba5baa4c0bf1817a7a16ec61fc0d98d9ca79101397f9f984f203`.

**name:** Crownshatter Decree Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to three selected enemies in your aura

**duration:** While conscious and in aura

**frequency:** Each incoming healing event

**effect:** A selected enemy receives HP healing only if it has taken actual damage from a meaningful hostile creature since the start of its previous regular turn. If it has not, that healing restores 0 HP; its source still spends its normal costs. Temporary HP, stabilization and resurrection are not HP healing for this restriction. This aura never creates damage, transfers healing or reverses recovery that already resolved.

**prerequisite:** Paladin 3; Oathbreaker — Oath of the Martyr King

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:ranger:ranger.hero.outrider.blight-infusion

**REVIEWED / reference-VALIDATED — classified components only** · next-healing flat reduction

Source: `data/public/class_playtests/ranger.json` / `ranger.hero.outrider.blight-infusion`. SHA256 `56230dcd9d01a0ffa5627fa3b6a3dc344570f83e7eabe5ba4e241f5efd52cffe`.

**name:** Blight Infusion

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Primary target of your Arrow on blighted ground

**duration:** Until end target's next turn

**frequency:** Once/Arrow

**effect:** On hit target makes CON save or the next HP healing it receives is reduced by M, minimum 0. This is temporary Blight, not permanent campaign Corruption; multiple applications do not stack.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:ranger:ranger.hero.outrider.withering-shot

**REVIEWED / reference-VALIDATED — classified components only** · next-healing ×1/2

Source: `data/public/class_playtests/ranger.json` / `ranger.hero.outrider.withering-shot`. SHA256 `ba3f59599016aaaaf85726c00275367daca171477f078d3879ac916a90e41e5c`.

**name:** Withering Shot

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One enemy in bow range

**duration:** Instant; until end target's next turn

**frequency:** Recharge 3

**effect:** Bow attack; hit adds S d6 necrotic and target makes CON save. Failure halves the next HP healing it receives before expiry, rounding down. No stacking with another reduction to create negative healing.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:shaman:shaman.hero.bloodcaller.blight-totem

**REVIEWED / reference-VALIDATED — classified components only** · nonstacking HEALING ×1/2 aura

Source: `data/public/class_playtests/shaman.json` / `shaman.hero.bloodcaller.blight-totem`. SHA256 `56bd3dd7b141931dda883f3728d30221c8e34ba30347d55c87fe66dc2f338805`.

**name:** Blight Totem

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Totem within 30 ft; 15 ft aura affecting all creatures

**duration:** 3 of your turns

**frequency:** Ordinary totem capacity/concentration

**effect:** HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:soldier:soldier.arch.fortify-zone

**REVIEWED / reference-VALIDATED — classified components only** · NON-HEAL false-positive source

Source: `data/public/class_playtests/soldier.json` / `soldier.arch.fortify-zone`. SHA256 `0938937bdd2ad8e34bc16ade52b53b16b3dc67136d97b1a728c03f4576943f3c`.

**name:** Fortify Zone

**activation:** Action

**cost:** 1 short-rest use

**rangeAndTarget:** Visible 15 ft square within 30 ft

**duration:** 3 rounds

**frequency:** 1/short rest

**effect:** Designate fortified firing lanes. Ranged attacks against up to 3 allies inside take-2 to hit while you remain conscious within 30 ft. Does not affect saves, melee attacks or attacks from inside zone.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:soldier:soldier.hero.champion.rallying-cry

**REVIEWED / reference-VALIDATED — classified components only** · TEMP HP, not healing

Source: `data/public/class_playtests/soldier.json` / `soldier.hero.champion.rallying-cry`. SHA256 `5bfb1a71cb4b5b01c09fc3090391670394590c62f63474223b80356fa6459009`.

**name:** Rallying Cry

**activation:** Bonus Action

**cost:** 1 long-rest use

**rangeAndTarget:** Up to 3 allies within 30 ft who hear you

**duration:** Instant; temp HP to encounter end

**frequency:** 1/long rest

**effect:** End Frightened on each and grant S+M temporary HP. Cannot revive, heal real HP or repeatedly refresh from imitation/copies.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:tinker:tinker.base.field-repair

**REVIEWED / reference-VALIDATED — classified components only** · MACHINE REPAIR, no destroyed-object resurrection

Source: `data/public/class_playtests/tinker.json` / `tinker.base.field-repair`. SHA256 `612a9f00b4e33a8bfc77c3f83ff1e1d839fa1237e8d20e65b703bea1431b6d7f`.

**name:** Field Repair

**activation:** Action

**cost:** 1 RP

**rangeAndTarget:** One construct/device touched

**duration:** Instant

**frequency:** Recharge 2

**effect:** Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:tinker:tinker.hero.artificer.repair-pulse

**REVIEWED / reference-VALIDATED — classified components only** · MACHINE REPAIR, functional devices only

Source: `data/public/class_playtests/tinker.json` / `tinker.hero.artificer.repair-pulse`. SHA256 `bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593`.

**name:** Repair Pulse

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Upto 3 friendly devices within 30 ft

**duration:** Instant; AC until start next turn

**frequency:** 1/short rest

**effect:** Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:warrior:warrior.hero.wardborn.stabilizing-injection

**REVIEWED / reference-VALIDATED — classified components only** · HEAL

Source: `data/public/class_playtests/warrior.json` / `warrior.hero.wardborn.stabilizing-injection`. SHA256 `b58508331c82ad5a7dad8bd3713029899b9a7c341c490220d997caf0e3aa71db`.

**name:** Stabilizing Injection

**activation:** Action

**cost:** Consume 1 prepared serum dose

**rangeAndTarget:** One living creature you touch

**duration:** Instantaneous

**frequency:** At most once per target per long rest

**effect:** Stabilizing Injection. The target regains 2d8 + M HP and may end one of Poisoned, Frightened or Staggered. If Diseased, it may immediately repeat one saving throw the disease normally permits. This removes no Wounds, cannot restore the dead and does not activate a mutation or apply the consumed serum's normal profile.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:warrior:warrior.hero.ironskin.regenerative-mutation

**REVIEWED / reference-VALIDATED — classified components only** · PASSIVE REGENERATION / reserve-paid actual healing

Source: `data/public/class_playtests/warrior.json` / `warrior.hero.ironskin.regenerative-mutation`. SHA256 `9dcfe6b7b149360e470c0d7940937b13c7bbdc4f696999b93710257158818fd1`.

**name:** Regenerative Mutation

**activation:** Passive

**cost:** Spend healing amount from Mutation Recovery Reserve

**rangeAndTarget:** Self

**duration:** While at least one mutation is active in a real encounter

**frequency:** Once at the start of each regular turn

**effect:** Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. NEW: Unpaid passive Mutation-Reserve regeneration supplies no excess-healing conversion, including Cosmic Equilibrium, despite mathematical excess and zero Reserve spend. Future explicit source exception required.

## class-card:warrior:warrior.supplement.redundant-organs

**REVIEWED / reference-VALIDATED — classified components only** · 1-HP DAMAGE FLOOR

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.redundant-organs`. SHA256 `51fd6f5a02d4328ed7a047301865acdac992364b8c4c924da5f85315ab4efbca`.

**name:** Redundant Organs

**activation:** Triggered while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** When damage would reduce you to 0 HP without killing you outright, remain at 1 HP instead.

**prerequisite:** Warrior 6; Advanced Vital

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:warrior:warrior.supplement.hemophage-core

**REVIEWED / reference-VALIDATED — classified components only** · LIFE-DRAIN HEAL / reserve-paid actual healing

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.hemophage-core`. SHA256 `e472701e8febc1973d6963d6a4d3c78ba1a4aa6d4e1740e3a484c9344b14cbda`.

**name:** Hemophage Core

**activation:** Triggered while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** Once per turn

**effect:** When you personally reduce a meaningful hostile creature to 0 HP with a melee attack, regain 2d6 HP. Summoned, trivial, friendly or repeatedly revived creatures cannot trigger this healing. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

**prerequisite:** Dreadspawn; Aberrant Mutation Tree; Warrior 10

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.base.consecrated-ground

**REVIEWED / reference-VALIDATED — classified components only** · Restoration-conditioned flat healing add-on; same packet; once/creature/Rite pulse

Source: `data/public/class_playtests/cleric.json` / `cleric.base.consecrated-ground`. SHA256 `f4b71531332377e2ca7b3ea4b4646e46df57b264d265473b30abfbc2f86bdb55`.

**name:** Consecrated Ground

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Passive

**frequency:** Always

**effect:** Consecrated Ground. Tags: rite, healing, passive. Whenever one of your healing Rites restores HP to a living creature standing in terrain created by your Consecrate feature, that creature regains S additional HP. Apply this once per creature per Rite pulse; it is flat healing and is not itself another healing trigger.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.base.radiance.radiance

**REVIEWED / reference-VALIDATED — classified components only** · Restoration-conditioned flat add-on + cleanse; once owner turn

Source: `data/public/class_playtests/cleric.json` / `cleric.base.radiance.radiance`. SHA256 `35f3566de386bca746618537d03e3561d74b8a35e1633c073ddef7e77f507821`.

**name:** Radiance

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic only if Radiance was selected

**effect:** Invocation Path — Radiance. Tags: invocation, radiance, healing. Once on each of your turns when one of your Rites restores HP to at least one living creature, choose one creature healed by that Rite. It regains S additional HP and may immediately end either Frightened or Poisoned on itself.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.base.renewal.renewal

**REVIEWED / reference-VALIDATED — classified components only** · Post-actual-HP non-healing Stamina recovery

Source: `data/public/class_playtests/cleric.json` / `cleric.base.renewal.renewal`. SHA256 `79196d34cabcb66c4ad06b6342b8c2bf64384b64f636584b9e3ac3a942f06ecb`.

**name:** Renewal

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic only if Renewal was selected

**effect:** Invocation Path — Renewal. Tags: invocation, renewal, healing, rite. Once per use of a healing Rite, choose one creature that actually regained HP from it. That creature also restores 5 Stamina, not exceeding its Stamina maximum. A creature without a Stamina resource receives no secondary benefit.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.base.echoes.echoes

**REVIEWED / reference-VALIDATED — classified components only** · Delayed copied numeric heal/damage; no conditions/resources/triggers

Source: `data/public/class_playtests/cleric.json` / `cleric.base.echoes.echoes`. SHA256 `66a5241b20fcfd81448ba872aa1cd3fd5b59cadb5eb540467e9f5bdaf14cb155`.

**name:** Echoes

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One original target within 30 feet

**duration:** Until start of your next regular turn

**frequency:** At most one pending Echoes-path repeat

**effect:** Invocation Path — Echoes. Tags: invocation, echoes. Once on each of your turns after a Smite or Rite produces rolled immediate damage or healing, store one original target and that raw dice total. At the start of your next regular turn, if the target is legal, repeat floor(raw dice total/10), minimum 1 for a positive total, as the same damage or healing type. This repeat carries no conditions, resources or triggers.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.arch.aura-of-faith

**REVIEWED / reference-VALIDATED — classified components only** · Restoration-conditioned flat healing add-on

Source: `data/public/class_playtests/cleric.json` / `cleric.arch.aura-of-faith`. SHA256 `56acc5fb191e255889bc45374d73b2ba55798a82fe5b5ab193731ab3d57ad448`.

**name:** Aura of Faith

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Allies within 15 feet who can perceive you

**duration:** Passive while conscious

**frequency:** Always

**effect:** Aura of Faith. Tags: aura, bishop. Allies in the aura gain +1 on saving throws. Whenever your Rite restores HP to an ally in the aura, that ally also regains 1 additional HP. Multiple Aura of Faith bonuses do not stack.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.arch.sanctified-reprisal

**REVIEWED / reference-VALIDATED — classified components only** · Post-actual-heal Smite empowerment; not additional healing

Source: `data/public/class_playtests/cleric.json` / `cleric.arch.sanctified-reprisal`. SHA256 `fdcb362b242d629e172ae53e788f3ddeadf6a8a57557ee30ed31cc980b21a3fa`.

**name:** Sanctified Reprisal

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until end of your next regular turn

**frequency:** At most once per turn

**effect:** Sanctified Reprisal. Tags: healing, smite, bishop. After one of your Cleric features restores HP to a living creature, empower your next Divine Smite before the end of your next regular turn. On a hit it deals S d4 additional radiant damage. If the target is Undead, it must also make a Constitution save; failure Stuns it until the end of its next turn.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.saint.aura-of-grace

**REVIEWED / reference-VALIDATED — classified components only** · Finite paid healing pulse; not passive regeneration

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.aura-of-grace`. SHA256 `7dff7e8271aba866c1b596528fe2e7d1e3f9a1558eeec233922585461bcc9854`.

**name:** Aura of Grace

**activation:** Triggered and passive

**cost:** 1 RP per healing pulse

**rangeAndTarget:** Living allies within 15 feet

**duration:** Passive during real encounters

**frequency:** Healing once/own regular turn; critical reduction once/ally/round

**effect:** Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.priest.words-of-equilibrium

**REVIEWED / reference-VALIDATED — classified components only** · Pre-resolution formula/M modifier

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.priest.words-of-equilibrium`. SHA256 `fd8bed1334fe50bb413208e4e20d33623002d18e360548bb325f793bd5f6dab7`.

**name:** Words of Equilibrium

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Passive

**frequency:** Always

**effect:** Words of Equilibrium. Tags: priest, scaling. For numeric Cleric technique healing and damage that would add your Wisdom modifier, use the higher of your Intelligence or Wisdom modifier instead. M becomes max(1, that higher modifier) for those numeric effects. This does not change Cleric attack rolls or save DCs unless another rule explicitly says so.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.priest.cosmic-equilibrium

**REVIEWED / reference-VALIDATED — classified components only** · Excess-heal→damage converter + radiant-damage→heal converter; separate once/round entitlements; no mutual recursion

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.priest.cosmic-equilibrium`. SHA256 `511b9a9abd80cc33649c3a30d73c03139189a2443a25ae92b7905fbdb0251787`.

**name:** Cosmic Equilibrium

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** 15-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** 1/short rest

**effect:** Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.cultist.sanguine-rite

**REVIEWED / reference-VALIDATED — classified components only** · Damage-driven finite healing based on actualDamageDealt

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.sanguine-rite`. SHA256 `b043e78dd641a9e31b86b49c238105f2b4ee4138c21f4e2ae9e194fee44169f9`.

**name:** Sanguine Rite

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self and one ally within 30 feet

**duration:** Instantaneous

**frequency:** At most once on each of your turns

**effect:** Sanguine Rite. Tags: cultist, rite, healing. When one of your Rites deals damage to at least one enemy, choose one living ally within 30 feet. That ally regains HP equal to half the actual damage dealt to one chosen damaged enemy, rounded down, maximum S+M HP. This healing cannot trigger Sanguine Rite again.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:cleric:cleric.hero.cultist.zealot-s-fervor

**REVIEWED / reference-VALIDATED — classified components only** · Pre-resolution flat healing-roll modifier; strongest-flat rules

Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.zealot-s-fervor`. SHA256 `c54199ee73ebfbe5c2c47cd5771fc43fd4f7609dfef775292d0798b409d44e4f`.

**name:** Zealot's Fervor

**activation:** Bonus Action

**cost:** 2 Conviction

**rangeAndTarget:** Self

**duration:** 3 rounds

**frequency:** 1/short rest

**effect:** Zealot's Fervor. Tags: cultist, stance. For 3 rounds, once on each of your turns add S to one damage roll from a Cleric feature and S to one HP-healing roll from a Cleric feature. While the Fervor lasts, your AC is reduced by 1. The Conviction expenditure is not a Rite or Invocation and therefore does not vent Dissonance by itself.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:crimson-agent:crimson-agent.base.blood-tithe

**REVIEWED / reference-VALIDATED — classified components only** · Limited triggered healing after qualifying death; anti-farm

Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.base.blood-tithe`. SHA256 `1db4f0777a524fb57e9b007e92e46aa430ba568b20c1720ec02fea8d56338cab`.

**name:** Blood Tithe

**activation:** Triggered

**cost:** 1 short-rest use

**rangeAndTarget:** Self after a hostile bleeding creature dies within 30 ft

**duration:** Instant

**frequency:** 1/short rest

**effect:** Regain HP equal to M+class level after a creature bearing your Bleed dies. It must have been an active hostile combatant; no ally, summon, captive or corpse farming.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:crimson-agent:crimson-agent.arch.hemostasis

**REVIEWED / reference-VALIDATED — classified components only** · Bleed cure + ordinary finite healing; cure remains legal even when healing is later blocked

Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.arch.hemostasis`. SHA256 `f8563c88b8499416fffe590c35b46f369197b04790121696b180a7bed083129e`.

**name:** Hemostasis

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One living creature touched

**duration:** Instant

**frequency:** Recharge 2

**effect:** End all Bleed on the target and restore S d6+M HP, regardless of number of ticks removed. You cannot create extra healing by inflicting extra Bleed. Works even if no Bleed is present, at the same RP cost.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:crimson-agent:crimson-agent.hero.bloodweaver.hemostasis

**REVIEWED / reference-VALIDATED — classified components only** · Paid finite delayed healing pulses; explicit no healing-loop behavior

Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.bloodweaver.hemostasis`. SHA256 `fd035eba7d0e2ed5547d745a6e3e52207bfa499b87cd0c693f1f00bb932b87f0`.

**name:** Hemostasis

**activation:** Passive

**cost:** 1 additional RP per application

**rangeAndTarget:** One willing living ally in range of your Bleed application

**duration:** 3 target turns

**frequency:** Once/own turn

**effect:** You may replace a new Bleed application on that ally with healing 1d4 at start of its next 3 turns. Pay extra RP even if original application was free. One such healing effect per target; it cannot spread, detonate, generate BG or trigger healing loops.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:crimson-agent:crimson-agent.hero.bloodweaver.transfusion

**REVIEWED / reference-VALIDATED — classified components only** · Non-damage donor HP cost + finite recipient healing

Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.bloodweaver.transfusion`. SHA256 `d7ac6dec9bb7ad1c0b940322906967a9aa1d366608896d8b9ef9a2f8c7342ce2`.

**name:** Transfusion

**activation:** Action

**cost:** 2 RP; sacrifice up to class level HP

**rangeAndTarget:** One willing living ally touched

**duration:** Instant

**frequency:** 1/short rest

**effect:** Lose K real HP, at least 1, without falling below 1. Ally regains K+floor(K/2) HP. Loss bypasses defenses and cannot trigger BG, damage-sharing or healing refunds. The RP/use limit remains even if little healing is possible.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Donor pays K normalHP before recipient baseK+floor(K/2) ordinary healing. No damage/redirection/temp payment/refund; donor remains1. Recipient legal modifiers/restrictions apply.

## class-card:crimson-agent:crimson-agent.hero.bloodweaver.veinweave-vitality-link

**REVIEWED / reference-VALIDATED — classified components only** · Separate triggered M-HP secondary heal; requires actual paid-Agent restoration; cannot retrigger link

Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.bloodweaver.veinweave-vitality-link`. SHA256 `352537575776482f39b276b924579af24fc920b770aaf87f289c10f58e840333`.

**name:** Veinweave: Vitality Link

**activation:** Bonus Action

**cost:** 3 BG

**rangeAndTarget:** One willing ally within 30 ft

**duration:** Concentration, 3 of your turns

**frequency:** Recharge 3

**effect:** Start Vitality Link Veinweave. Once/round when you restore real HP with a paid Agent technique, linked ally regains M HP if within 30 ft. This secondary healing never triggers another link. Gain+1 AC while adjacent to that ally; no spell buffs or resources are copied.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Separate child heal requires actual restoration by paid Agent source; child carries blockLinkTriggers for every downstream link, shared root/provenance retained.

## class-engine:mirrorsage:2

**REVIEWED / reference-VALIDATED — classified components only** · BOOK/profile engine: Mend is copied finite healing; Ward temp HP; no role conversion

Source: `data/public/class_playtests/mirrorsage.json` / `2`. SHA256 `756a34d737a53cf7042e866780a2ad66491d356dc21c07305883302ccc27702b`.

**text:** Record source creature/name, witnessed ability, category, damage type, allowed rank, capture encounter and whether first release has occurred. For this pilot, capture copies the observed role into ONE bounded profile: Strike=one target 60 ft class spell attack S d8 observed damage type; Burst=up to 3 enemies in 10 ft radius within 30 ft DEX save S d6, half on success; Mend=one living ally 30 ft S d6+M HP; Ward=one ally 30 ft S d6+M temporary HP for 1 minute; Hindrance=one enemy 30 ft WIS save or Speed-10 ft and no Reactions until end its next turn. Choose only a profile actually expressed by the observed source; physical attack cannot become healing. Rank is max(1, ceil(source challenge rating/2)); if source lacks a rating the Director assigns a rank before the encounter, not after seeing a desirable ability. Rank cannot exceed your Mirrorsage learnable rank; no copying character levels from a creature. Damage/targets/control are capped by these profiles, not source boss dice.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:mirrorsage:mirrorsage.hero.shattered-one.echo-leech

**REVIEWED / reference-VALIDATED — classified components only** · Paid damage-drain healing using actualDamageDealt; no secondary healing/resource procs

Source: `data/public/class_playtests/mirrorsage.json` / `mirrorsage.hero.shattered-one.echo-leech`. SHA256 `8cef2175f25fc74493af814999948b1abec88c5b707326dc86a7b82646eeb60c`.

**name:** Echo Leech

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** Self after direct Echo damages a hostile creature

**duration:** Instant

**frequency:** Once/round

**effect:** Pay 1 RP to regain HP equal to min(M, actual damage dealt to one target). Copies, Do Ts and companion attacks do not trigger it. Healing has no secondary healing/resource procs; no damage means no heal.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.base.stance-shift

**REVIEWED / reference-VALIDATED — classified components only** · Pre-heal Reaction state switch; can establish applicable stance before healing resolves

Source: `data/public/class_playtests/monk.json` / `monk.base.stance-shift`. SHA256 `c5e6f771d4dd5845d4fb51419cfad69c28e17cbb5ebf1be55e6f154c2674e499`.

**name:** Stance Shift

**activation:** Reaction

**cost:** 0

**rangeAndTarget:** Self

**duration:** Instantaneous stance change

**frequency:** Uses the same once-per-round stance switch

**effect:** Stance Shift. Tags: base, passive-upgrade, stance. Your automatic core stance change may be used as a Reaction when you are targeted by an attack, forced to make a saving throw, or immediately before an ally within 15 feet receives healing. The new stance applies before the triggering roll or healing resolves. This consumes your one stance switch for that round and never grants a second switch.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.arch.meditative-healing

**REVIEWED / reference-VALIDATED — classified components only** · Finite self-healing + independent post-resolution Ki restoration

Source: `data/public/class_playtests/monk.json` / `monk.arch.meditative-healing`. SHA256 `8bec2f739147f5da0c8f8a956b03d20d49fc1497ff717e1b9d312edbc0ec164f`.

**name:** Meditative Healing

**activation:** Action

**cost:** 2 Ki + 2 RP

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** Meditative Healing. Tags: arch, active, healing, weave. Regain S d8 + M HP, then regain 1 Ki after resolution, never above 5. The restored Ki does not count as a normal generator but cannot be used if this feature was activated outside a real encounter merely to farm Ki. It removes no Wounds. As a minor Weave technique, you may spend 1 additional Ki before resolution to prevent its 1 Dissonance.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.hero.enlightened-master.tranquil-lotus-step

**REVIEWED / reference-VALIDATED — classified components only** · Stored restoration-conditioned flat add-on to next heal

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.tranquil-lotus-step`. SHA256 `a57127e0ff0f86cb40bd7268a2b4b1e331711d676a07715cea307eb179c87e92`.

**name:** Tranquil Lotus Step

**activation:** Bonus Action

**cost:** 2 Ki

**rangeAndTarget:** One willing ally within your walking Speed

**duration:** Until end of your next regular turn

**frequency:** Recharge 3 rounds

**effect:** Tranquil Lotus Step. Tags: hero, enlightened, support, cleanse. Move up to your Speed toward a willing ally without provoking opportunity attacks. If you finish within 5 feet, choose Charmed, Frightened or Poisoned currently affecting that ally; end it on the ally and apply that same condition to yourself until the end of your next regular turn if you are not immune. The ally gains +S HP the next time it receives healing before then.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.hero.enlightened-master.balance-beyond-flesh

**REVIEWED / reference-VALIDATED — classified components only** · Paid finite triggered healing from qualifying resource expenditure

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.balance-beyond-flesh`. SHA256 `d77dbde6e81663010aa15bd970c6497220a16d444b6e2c89de78e41b59e423f9`.

**name:** Balance Beyond Flesh

**activation:** Passive

**cost:** 1 RP for each healing trigger

**rangeAndTarget:** Allies within 15 feet while you are in Crane Stance

**duration:** Passive during real encounters

**frequency:** Once per ally per round

**effect:** Balance Beyond Flesh. Tags: hero, enlightened, support, healing. During a real encounter, when an ally within 15 feet spends at least 1 point from a finite class resource such as Ki, RP or Conviction, you may pay 1 RP for that ally to regain S HP, at most once per round. It cannot trigger from free abilities, staged spending outside combat or resources immediately refunded by the same event.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:monk:monk.hero.enlightened-master.transcendent-meditation

**REVIEWED / reference-VALIDATED — classified components only** · Finite paid healing pulses + independent second-pulse Ki restoration

Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.transcendent-meditation`. SHA256 `ef26fc5933a98d0d06c511e4ecddeda4ea9dab8ee064bc4f2eec65d028589803`.

**name:** Transcendent Meditation

**activation:** Action

**cost:** 3 Ki + 4 RP

**rangeAndTarget:** Self and up to three allies within 15 feet

**duration:** Concentration, maximum 3 Monk turns

**frequency:** 1/short rest

**effect:** Transcendent Meditation. Tags: hero, enlightened, healing, weave, sustained. On start and at the start of each of your next two regular turns while concentration holds, each target regains S d6 HP. You regain 1 Ki on the second pulse only, never above 5. Targets must remain within 15 feet. This finite healing cannot be restarted until the short-rest use refreshes.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.spiral-touched.spiral-touched-boon-iii

**REVIEWED / reference-VALIDATED — classified components only** · Zero-HP direct recovery + phase-out; not floor/resurrection

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.spiral-touched.spiral-touched-boon-iii`. SHA256 `a6358be2e17db52d461c11e2df79d972481dba2c95ebd29ecd7c31a02987d377`.

**name:** Spiral-Touched — Boon III

**activation:** Triggered at 0 HP

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of next regular turn

**frequency:** 1/long rest

**effect:** 1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations.

**prerequisite:** Oracle 10; selected Curse:Spiral-Touched

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Specific pre-Wound recovery after Instant Death fails and no true floor prevents crossing. Preserve original drop Wound trigger; spend use, attempt quarter-maximum direct recovery, phase out, then Wound. Fatal Wound ends phase unless independently replaced.

## class-card:oracle:oracle.supplement.spiral-touched.spiral-touched-boon-v

**REVIEWED / reference-VALIDATED — classified components only** · DEFER temporal snapshot restoration, explicitly not generic resurrection

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.spiral-touched.spiral-touched-boon-v`. SHA256 `f3eee6bab3405acd7905b87c42e3c6bf6539da20cc12dd0b74ad34d2c1fa68f6`.

**name:** Spiral-Touched — Boon V

**activation:** Reaction before round 4

**cost:** 0

**rangeAndTarget:** Recorded encounter participants

**duration:** Restore recorded encounter-start state

**frequency:** 1/long rest

**effect:** 1/long rest as a Reaction before the fourth round of the encounter begins, rewind the current encounter to its initiative-start snapshot: restore combatant positions, HP, temporary HP, conditions, RC and per-encounter uses to that snapshot. Short-/long-rest uses, physical consumables and this Time Loop use remain spent. Slain encounter participants return to their snapshot state and no duplicate XP, treasure or consumables are created. Allies retain memory of the previous timeline. Time Loop does not restore RP, Ki, Conviction, Blood Gauge, device stock, healing reserves or any other daily/rest resource; only the named RC and per-encounter states rewind. No loot changes ownership through rewinding. Record the snapshot at initiative; if no complete snapshot exists, this option is unavailable and unspent. It cannot undo a previous encounter or duplicate a per-rest use.

**prerequisite:** Oracle 20; selected Curse:Spiral-Touched

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. DEFER: snapshot participant contract is discussed/tested, including Wounds, RC, per-encounter use and Soul Bind restoration. Full clocks/environment/equipment/body duplication semantics require temporal package; no complete execution claim.

## class-card:oracle:oracle.supplement.wound-eater.wound-eater-boon-iii

**REVIEWED / reference-VALIDATED — classified components only** · Direct death effect + heal only if target actually dies

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.wound-eater.wound-eater-boon-iii`. SHA256 `d872f36ef75cc9ff431e85c49d7cbfe85cf4b41721c46042c12d9e8af47fea5b`.

**name:** Wound Eater — Boon III

**activation:** Action

**cost:** 0

**rangeAndTarget:** One dying hostile living creature touched

**duration:** Instantaneous

**frequency:** 1/short rest; no staged/summoned targets

**effect:** 1/short rest as an Action touch one dying hostile living creature at 0 HP; that creature dies and you regain HP equal to one-quarter your maximum HP rounded down. It cannot trigger from summoned, trivial or staged creatures and removes no Wounds.

**prerequisite:** Oracle 10; selected Curse:Wound Eater

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Direct pending death of a legal living dying hostile0 target emits no damage/Wound event. Legal Ward may intercept. Healing requires actual death; paid use/action remains spent.

## class-card:oracle:oracle.supplement.wound-eater.wound-eater-boon-iv

**REVIEWED / reference-VALIDATED — classified components only** · Paid finite damage/drain pulses; self heal from actualDamageDealt

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.wound-eater.wound-eater-boon-iv`. SHA256 `9028f42b10e75ba44b130f18695a0ef9411d99df43b4929f1b89d1e4ead2d127`.

**name:** Wound Eater — Boon IV

**activation:** Bonus Action; start-of-turn pulses

**cost:** 2 RC start; 1 RC per later pulse

**rangeAndTarget:** Up to three living enemies within 10 feet

**duration:** Concentration; at most three pulses

**frequency:** One aura; once/target/round

**effect:** pay 2 RC as a Bonus Action to activate a 10-foot drain aura, requiring concentration for at most three pulses; pay 1 RC before each pulse after the first or end it. You may suppress it freely. During a real encounter, at the start of your turn up to three meaningful living enemies in the aura takes S necrotic damage; regain HP equal to the total actually dealt, capped at S+M per turn.

**prerequisite:** Oracle 15; selected Curse:Wound Eater

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.wound-eater.wound-eater-boon-v

**REVIEWED / reference-VALIDATED — classified components only** · Direct non-damage HP loss + heal from actual HP lost

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.wound-eater.wound-eater-boon-v`. SHA256 `76d3f99606a9bb0c358f108d5dba7577ecaa8580e0aef97ef94b235e8dbb4811`.

**name:** Wound Eater — Boon V

**activation:** Action

**cost:** 0

**rangeAndTarget:** Up to three living enemies within 20 feet

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** 1/long rest as an Action, up to three meaningful living enemies within 20 feet lose HP equal to the lesser of one-quarter their maximum HP or Oracle level+M; you regain half the total actual HP lost, capped at one-half your maximum HP. Allies, constructs, undead, trivial creatures and summons are unaffected.

**prerequisite:** Oracle 20; selected Curse:Wound Eater

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.curse.burning-blood

**REVIEWED / reference-VALIDATED — classified components only** · Cold-tagged HP-healing gate + actual-HP-damage ignition

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.curse.burning-blood`. SHA256 `30fbed4192491488d5ac68d036dd6d9d4f97e85392d1f732b11b6bf331b9c208`.

**name:** Burning Blood

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Chosen once at Oracle 1

**effect:** LIMITATIONS: once per round when slashing or piercing damage deals actual HP damage to you, your blood ignites: you and hostile creatures within 5 feet each take 1d4 fire damage. You cannot gain cold resistance from a beneficial spell, item or class feature and cold-tagged healing restores 0 HP to you. After slashing or piercing damage wounds you, take -2 on Stealth until a creature spends an Action succeeding on DC 10 Medicine to bind the wound or you complete a short/long rest.

**prerequisite:** Selected Curse: Burning Blood

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.curse.false-life

**REVIEWED / reference-VALIDATED — classified components only** · Other-creature healing-spell gate with Insight/d2 procedure

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.curse.false-life`. SHA256 `2f09d387e8c4b85570bd79a1de08e4f54223e4cf1e020d66be6c0ce80a37c27d`.

**name:** False Life

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Chosen once at Oracle 1

**effect:** LIMITATIONS: divination treats you as undead unless it specifically pierces Oracle curses. Before a healing spell from another creature restores HP to you, its caster may make Wisdom (Insight) against your Revelation save DC. On success healing works normally. On failure roll d2; on 1 the spell restores 0 HP to you but still expends its normal costs. Non-spell healing is unaffected. Social hesitation from life-focused clergy remains narrative unless the scene calls for an ordinary reaction check.

**prerequisite:** Selected Curse: False Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.false-life.false-life-boon-v

**REVIEWED / reference-VALIDATED — classified components only** · Delayed start-turn direct HP recovery at 0; not resurrection

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.false-life.false-life-boon-v`. SHA256 `aca1096e9676527d4009472fd552ae219dc3cf6a5196f4ac4ad30a5c7e064b0b`.

**name:** False Life — Boon V

**activation:** Triggered at 0 HP

**cost:** 0

**rangeAndTarget:** Self; undead within 15 feet

**duration:** Rise next turn; immunity two rounds

**frequency:** 1/long rest

**effect:** 1/long rest when you are at 0 HP but not destroyed outright, appear dead until the start of your next regular turn. During that interval you are incapacitated. At the start of your next turn rise with floor(max HP/4), minimum 1, and gain necrotic immunity for 2 rounds. Undead within 15 feet treat you as non-hostile until you damage, control or overtly oppose them. Divination during the apparent-death interval returns one false but plausible state-description you choose; it cannot fabricate events outside your own condition.

**prerequisite:** Oracle 20; selected Curse:False Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Delayed quarter-maximum direct recovery at next regular start before death save. Extra turn does not advance it. Dead target is not revived; broad gain prohibition leaves0 without invented stability.

## class-card:oracle:oracle.supplement.fate-bound.fate-bound-boon-iv

**REVIEWED / reference-VALIDATED — classified components only** · Death-effect save bonus + pre-commit failed-death-save reroll

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.fate-bound.fate-bound-boon-iv`. SHA256 `e1d7c3772757a656f312cd8d57d129f5254d1f9bb220c38793963ac7e81246d8`.

**name:** Fate-Bound — Boon IV

**activation:** Passive; triggered death-save reroll

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent save bonus; immediate reroll

**frequency:** Reroll 1/long rest

**effect:** +2 on saves against death effects, banishment, forced temporal/fate displacement and effects explicitly severing a destiny bond. 1/long rest reroll one failed death save.

**prerequisite:** Oracle 15; selected Curse:Fate-Bound

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Reroll failed death save before committing natural1/failure counters, then use new result. Generic death-effect save bonus does not apply to ordinary death saves.

## class-card:oracle:oracle.supplement.bones.unfinished-chorus

**REVIEWED / reference-VALIDATED — classified components only** · Zone corpse-raising block + finite damage/drain healing

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.unfinished-chorus`. SHA256 `d0c65305f314bb6bbb3b9245ec88c655a5d4b815b553e84d3cddcca489dfe535`.

**name:** Unfinished Chorus

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** Enemies, controlled undead and corpses within 4 tiles

**duration:** 2 rounds; Revelation backlash 1 round

**frequency:** At will while RC remains

**effect:** For 2 rounds, enemies within 4 tiles suffer Dread: -1 on attack rolls and saving throws. Once on each of your turns choose one living enemy in range; it takes 1d6 necrotic damage and you either regain half the actual damage dealt, rounded down, or one living ally within 3 tiles of you regains that amount, maximum S+M HP. Undead you control add S damage to one attack each turn and reduce first damage each round by 1. Corpses in the area cannot be raised while the Chorus lasts. Afterward you are suffering Revelation backlash until end of your next turn: -1 attacks/saves and Speed -5 feet. Choose up to three enemies and three allies. Enemies make Wisdom saves on entry and at the end of each turn, ending their debuff on success. The drain allows a Constitution save for half damage; healing is capped at S+M total per pulse. Concentration and pulse upkeep apply.

**prerequisite:** Oracle 9; Mystery: Bones

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.flame.ember-mantle

**REVIEWED / reference-VALIDATED — classified components only** · Restoration-conditioned external-healing flat add-on

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.flame.ember-mantle`. SHA256 `f2005c31d91f94a76fcd8844d701eacf8e27e3040db4c86f17c424a2278c9f29`.

**name:** Ember Mantle

**activation:** Passive and Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self; allies within 2 tiles during ignition

**duration:** Passive permanent; ignition 2 rounds

**frequency:** Ignition 1/long rest

**effect:** Gain fire resistance and add S HP to the first external healing effect that restores HP to you each round. Once per long rest ignite the Mantle for 2 rounds. Once per round when a creature within melee reach damages you with a melee attack, it takes 1d4 fire damage. You shed bright light in 2 tiles, and allies there gain +1 on saves against Frightened.

**prerequisite:** Oracle 1; Mystery: Flame

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.life-prophecy-trigger

**REVIEWED / reference-VALIDATED — classified components only** · Resource trigger requiring ≥1 actual HP; copies/reflections/staged excluded

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.life-prophecy-trigger`. SHA256 `a38f2ccd5df773cb51b309cb218f9ca6324e698e665a9fc367eb4f39b98e0b7f`.

**name:** Life Prophecy Trigger

**activation:** Triggered

**cost:** 0 RC

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** At most once per round during a real encounter

**effect:** When you restore at least 1 actual HP to a living ally other than through a copied, reflected or staged healing event, regain 1 RC, never above maximum. Healing multiple allies from one effect still restores only 1 RC that round.

**prerequisite:** Oracle 1; Mystery: Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.garden-of-restoration

**REVIEWED / reference-VALIDATED — classified components only** · Finite paid-zone healing pulses + stored restoration-conditioned +1 add-on

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.garden-of-restoration`. SHA256 `faaa0f647c20d847d84790b2a353bb9e9fcf3946f210c911e003d08474a7de93`.

**name:** Garden of Restoration

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** 4-tile-radius fixed zone centered within 5 tiles

**duration:** 3 rounds

**frequency:** At will while RC remains; one Garden at a time

**effect:** At the start of each living ally's turn in the Garden, it regains 1d6 HP, maximum three pulses per creature from this use, and gains +1 HP the next time another finite healing effect restores HP before its next turn. The first time each ally enters or starts in a given Garden, it may end Poisoned or immediately repeat one disease save. Undead starting in the Garden take 1d6 radiant damage and make a Wisdom save; on failure they take -1 on attack rolls until the end of that turn.

**prerequisite:** Oracle 6; Mystery: Life; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.life-linked

**REVIEWED / reference-VALIDATED — classified components only** · Damage-transfer link + rolled restoration-conditioned 1d4 add-on

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.life-linked`. SHA256 `e85dca21885aff801dd806929d567b1bfc05ea921792d259bab918337ea74c80`.

**name:** Life Linked

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One willing living ally within 5 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains; one Life Link at a time

**effect:** Link yourself to the ally. Once per round when it takes damage, you may use your Reaction to transfer up to half that actual damage rounded down to yourself. Transferred damage keeps its type and cannot be redirected again. The ally reduces the first necrotic damage it takes each round by S. Once per round when one of your paid or finite Oracle effects restores HP to the linked ally, it regains an additional 1d4 HP. The link ends if you are more than 5 tiles apart. Apply mitigation to the original damage once before splitting. The transferred portion cannot be mitigated again and cannot generate recovery or retaliation triggers.

**prerequisite:** Oracle 6; Mystery: Life; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.life.life-prophecy

**REVIEWED / reference-VALIDATED — classified components only** · Free Revelation activation + pre-resolution maximize-dice modifier + stored future flat healing add-on + nonrecursive radiant rider

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.life-prophecy`. SHA256 `279c910bb43d91ce02d504f21677dd60ca95cd4c6f6321567e210baeac41a258`.

**name:** Life Prophecy

**activation:** Triggered

**cost:** 0 RC for chosen Revelation

**rangeAndTarget:** One known Life Revelation; allies you heal

**duration:** Chosen Revelation; empowerment until end of your next regular turn

**frequency:** 1/long rest

**effect:** Activate one known Life Revelation for 0 RC. Until the end of your next regular turn, when one of your paid, finite or Prophetic-Surge Life effects rolls healing dice, treat each healing die as its maximum value. Each ally you heal during this period gains +S HP from the next separate finite healing effect it receives before the end of its next turn. Once per round when you heal an ally, undead within 3 tiles of that ally take 1d4 radiant damage. This radiant damage cannot trigger healing or RC recursively.

**prerequisite:** Oracle 18; Mystery: Life

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.time.rewind-wound

**REVIEWED / reference-VALIDATED — classified components only** · Finite HP healing based specifically on actualHpDamage + bounded event-condition removal

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.time.rewind-wound`. SHA256 `eb01bdc7533669a80e0862bf3130c342b3b8c9c3f4199f8925953086e6bc898c`.

**name:** Rewind Wound

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One living ally you touch

**duration:** Healing instantaneous; protection until start of your next turn

**frequency:** At will while RC remains; same damage event can be rewound once

**effect:** Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects.

**prerequisite:** Oracle 6; Mystery: Time; selected Tier II Revelation

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:oracle:oracle.supplement.time.the-spiral-opens

**REVIEWED / reference-VALIDATED — classified components only** · Copied healing interface; explicit no triggers/procs and must still pay printed copied-healing cost/use

Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.time.the-spiral-opens`. SHA256 `b15b7a477b14185e1510967e1d24c7e46a856a400ef1575f876d2adbaa39ee28`.

**name:** The Spiral Opens

**activation:** Action

**cost:** 0 RC

**rangeAndTarget:** Self; one known beneficial Time Revelation or one enemy within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds, at the start of each of your regular turns choose ONE temporal option, each usable at most once during this Final. ECHO REVELATION: repeat only the immediate numeric damage, healing, movement or buff component of one beneficial Time Revelation you personally resolved during the previous round, paying 0 RC; this copy is not a new Revelation cast, copies no resource restoration, action grant, hard control, condition trigger, Prophecy Trigger or proc. FORCED ECHO: choose one non-player enemy within 5 tiles and one ordinary weapon attack or non-resource movement action it took during its previous turn. The enemy makes a Wisdom save. On failure, during its next turn it must repeat that action pattern if legally possible, but it chooses all legal targets and paths; it spends no limited resources and cannot be forced to harm itself. A player-controlled creature instead, on a failed save, loses its Reaction and must choose either repeat one ordinary non-resource action type from its prior turn or have Speed reduced to 0 until turn end. Allies retain memory of all temporal echoes. This Final never creates more than one additional full Action for any creature in a round. There are only two options in this Final; after using both once, remaining rounds provide only the printed temporal presence, without another echo. An echoed healing amount also pays 1 RC or consumes an unused per-rest healing use; a temporal copy cannot create an uncosted healing reserve.

**prerequisite:** Oracle 20; Mystery: Time

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:paladin:0

**REVIEWED / reference-VALIDATED — classified components only** · BOOK finite Lay-on-Hands pool; Long Rest default refill

Source: `data/public/class_playtests/paladin.json` / `0`. SHA256 `3a192da0a97fc8b1f53cc6931be84771eedf432c0fac5567d6b4116284ea441e`.

**text:** Charisma governs Oath DC/M and divine technique attacks. Weapon attacks use their ordinary Strength/Dexterity ability. Hit Die d10; all armor, shields, simple and martial weapons. Paladin has no Conviction or Oracle Revelation Charges. Lay on Hands is its own pool, 5×Paladin level, fully restored only by long rest. Ordinary spells and printed Smite fuel use the same Paladin Core V 2 RP pool; healing points never convert to RP.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:paladin:11

**REVIEWED / reference-VALIDATED — classified components only** · BOOK sustained Oath healing-zone cadence

Source: `data/public/class_playtests/paladin.json` / `11`. SHA256 `965790fb859474dc7264c2a1afe1c947eb45153cea27d16eb10fe47c027ad779`.

**text:** Sustained Oath spell damage/healing zones use concentration, at most three pulses, and 1 RP upkeep after the first pulse unless a priced card expressly supplies a different finite cadence. Native Oath auras retain their printed passive cadence and target cap. Final auras last their stated finite duration and include their pulses. All hard-denial effects, including compelled Actions, share the common once/source/target/encounter guard; later failures only remove Reactions and reduce Speed by half for one turn.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.base.lay-on-hands

**REVIEWED / reference-VALIDATED — classified components only** · Finite pool healing/cleanse

Source: `data/public/class_playtests/paladin.json` / `paladin.base.lay-on-hands`. SHA256 `24341edafa2539d0d42b01f5821195c69dd1a3101cde176beb6809c4f4867673`.

**name:** Lay on Hands

**activation:** Action

**cost:** Choose 1 or more Lay on Hands points, maximum L per Action

**rangeAndTarget:** One living creature touched

**duration:** Instant

**frequency:** While pool remains

**effect:** Restore 1 HP per point spent, maximum class level per activation. Alternatively spend 5 points to end Poisoned or allow one immediate save against an existing disease that permits saves; cannot erase special-quest diseases, Wounds or death. This is finite pool healing, no RP conversion.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.hero.lay-on-hands

**REVIEWED / reference-VALIDATED — classified components only** · Finite pool mass allocation; entire remaining pool, 1/SR

Source: `data/public/class_playtests/paladin.json` / `paladin.hero.lay-on-hands`. SHA256 `4c5b19d2b558ca46e38f1d530683c19801b878d8bdf7027cb796e856c5ebcc75`.

**name:** Lay on Hands

**activation:** Action

**cost:** All remaining Lay on Hands points; minimum 1

**rangeAndTarget:** Up to 3 living allies in aura

**duration:** Instant

**frequency:** 1/short rest and pool cost

**effect:** Allocate remaining points among targets, at least 1 each; restore 1 HP per point. You may instead allocate 5 points per target to end Poisoned or Frightened. Spend entire pool, cannot multiply it by recipient count, raise the dead or remove Wounds. Oathbreakers instead deal allocated necrotic damage to 3 enemies, CON half, same pool cost.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oathbreaker-shared.desecrated-ground

**REVIEWED / reference-VALIDATED — classified components only** · Per-healing-die reduction; same-stat nonstacking

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-shared.desecrated-ground`. SHA256 `5bcc361442663e6799678be29cff54b4a1d6ebd29793db87ec39edc2845513e9`.

**name:** Desecrated Ground

**activation:** Action; Bonus Action maintenance

**cost:** 7 RP start; 1 RP per later pulse

**rangeAndTarget:** 10 ft radius fixed point 30 ft, up to 3 enemies

**duration:** Concentration, maximum 3 pulses

**frequency:** Recharge 4

**effect:** New rank 4 Forbidden spell. Initial and each paid pulse CON save for S d6 necrotic, half success. A failed target receives 1 less HP per healing die until start of your next turn. Penalty cannot make healing negative or stack with another same-stat reduction.

**prerequisite:** Paladin 13; selected Oathbreaker inversion

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-mercy.merciful-smite

**REVIEWED / reference-VALIDATED — classified components only** · Damage-derived finite healing pool using actualDamageDealt; no Smite/heal-copy chain

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.merciful-smite`. SHA256 `bb24ea1355d04db34e882d50cc5ebadd7b6da097442a0c2813d9e39b6cc5421c`.

**name:** Merciful Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack; up to 3 living allies within 10 feet of you

**duration:** Instantaneous

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Your Oath Smite deals radiant damage instead of adding a second Smite packet. After the Smite damage resolves, create a healing pool equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Divide that pool among up to 3 living allies within 10 feet. Healing cannot exceed maximum HP, remove Wounds or trigger additional Smite or healing-copy effects.

**prerequisite:** Paladin 3; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-mercy.channel-life

**REVIEWED / reference-VALIDATED — classified components only** · Non-damage donor HP cost + finite recipient healing

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.channel-life`. SHA256 `791e5b9a6f7de5962bffa02d02d406a4eba8aedc125391595cd002581a5f6610`.

**name:** Channel Life

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** Self and one living ally within 30 feet

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.

**prerequisite:** Paladin 9; Oath of Mercy

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Donor non-damage HP cost first, cannot be prevented/refunded, must remain1. Recipient ordinary heal accepts legal modifiers. Packet forbids ALL excess-to-tempHP conversion across owners; eligible excess-to-damage conversion remains possible.

## class-card:paladin:paladin.supplement.oath-of-vengeance.verdict-absolute

**REVIEWED / reference-VALIDATED — classified components only** · Explicit source-specific Lay-on-Hands full refill

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.verdict-absolute`. SHA256 `d0a6a7c1d230009b7b4c04c3c7304c7718ba39a097973dd6bf2b40fb849210b9`.

**name:** Verdict Absolute

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** One Judgment Brand target; witnesses in your aura

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds, your current Judgment Brand cannot be removed by an ordinary save or concealment effect. Smites against the branded target use maximum Smite dice, and it cannot voluntarily teleport or become invisible. If the branded target reaches 0 HP during the effect, restore your Lay on Hands pool to its normal maximum once, then up to three hostile creatures in your aura that witnessed the defeat make Wisdom saves; on failure they are Frightened until the end of their next turn. The Lay on Hands refill requires a meaningful nonsummoned hostile defeated in a real encounter; staged or willing sacrifices do not qualify.

**prerequisite:** Paladin 20; Oath of Vengeance

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-grief.last-rites

**REVIEWED / reference-VALIDATED — classified components only** · Stabilization + death-save/necrotic protection; not healing

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-grief.last-rites`. SHA256 `01538f718fe38198992f024db12296602b37d844d141dab99cd723a6c9516b1d`.

**name:** Last Rites

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One dying living creature within 30 feet; hostile undead within 10 feet of it

**duration:** Protection 1 hour; turning until end of undead target's next turn

**frequency:** At will while RP remains

**effect:** Stabilize the living target if at 0 HP. For 1 hour it gains +2 on death saves and necrotic resistance. Each hostile undead within 10 feet makes a Wisdom save; on failure it is Turned until the end of its next turn, meaning it must use its movement to move away by the safest route and cannot willingly move closer. This does not destroy or permanently repel undead.

**prerequisite:** Paladin 5; Oath of Grief

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-the-martyr-king.throne-s-grace

**REVIEWED / reference-VALIDATED — classified components only** · Range bridge + pre-resolution +1 per healing die; no pool-point bonus

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.throne-s-grace`. SHA256 `084a132d73f1f54d9155a932605eb82e4da34e8e1f61e69ca51c5031b3c502ad`.

**name:** Throne’s Grace

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** Self and up to three allies in your aura

**duration:** Concentration; three rounds

**frequency:** While RP remains

**effect:** Your Lay on Hands and touch-range Paladin healing can target selected allies anywhere in your current aura with clear line of effect. Normal activation, pool/RP costs, rank gates and use limits remain. Rolled healing you grant them adds 1 HP per die, maximum S+M additional HP per effect; pool-point healing adds no dice bonus. Selected allies gain +1 on death saves. The spell itself restores no HP.

**prerequisite:** Paladin 13; Oath of the Martyr King

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:paladin:paladin.supplement.oath-of-the-martyr-king.crown-undying

**REVIEWED / reference-VALIDATED — classified components only** · Damage redirect + finite secondary healing based on actually absorbed damage; no redirection/heal-copy chain

Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.crown-undying`. SHA256 `f8de6f3fe586c6b30d10bbdd31c93e0976aa46dfb3631afbbcbebe8ebe1d0b1d`.

**name:** Crown Undying

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to three selected allies in your aura

**duration:** Three rounds; no concentration

**frequency:** 1/long rest

**effect:** For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.

**prerequisite:** Paladin 20; Oath of the Martyr King

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:ranger:ranger.hero.warder.living-pulse

**REVIEWED / reference-VALIDATED — classified components only** · Paid finite self-healing; explicitly unavailable Downed/Incapacitated; not passive regen

Source: `data/public/class_playtests/ranger.json` / `ranger.hero.warder.living-pulse`. SHA256 `e1b7bfa045b543de315480c9e783e4da0cc13ea5adad64a79ca535d32af375bd`.

**name:** Living Pulse

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** Self in natural terrain

**duration:** Start of your regular turn

**frequency:** Once/turn

**effect:** You may pay 1 RP to regain 2 HP. Does not trigger when Downed or incapacitated, cannot exceed maximum and never counts as another healing spell. Replaces unlimited passive regeneration with a finite cost.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:ranger:ranger.hero.warder.healing-touch

**REVIEWED / reference-VALIDATED — classified components only** · Restoration-conditioned flat add-on to own paid spell/item healing

Source: `data/public/class_playtests/ranger.json` / `ranger.hero.warder.healing-touch`. SHA256 `172cd48e6cd74926574cbab5ab787d4d13becf500c21089e3a5868c55be64849`.

**name:** Healing Touch

**activation:** Passive

**cost:** 0

**rangeAndTarget:** One other ally healed by your paid spell/item

**duration:** Instant

**frequency:** Once/turn

**effect:** Add M HP to actual healing. Do not multiply potion dice or duplicate consumed items; cannot apply to regeneration, companions' healing, copies or another Ranger's same bonus.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:shaman:1

**REVIEWED / reference-VALIDATED — classified components only** · BOOK Renewal Totem finite paid three-pulse healing package

Source: `data/public/class_playtests/shaman.json` / `1`. SHA256 `2a2a89b4f440277a59743d2dc2936f2a625be9557882f5796fa8fb71d4b76d80`.

**text:** Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:shaman:shaman.hero.theurgist.benevolent-spirits

**REVIEWED / reference-VALIDATED — classified components only** · Pre-resolution flat modifier to one qualifying paid technique; excludes copies/triggered heals

Source: `data/public/class_playtests/shaman.json` / `shaman.hero.theurgist.benevolent-spirits`. SHA256 `58058070a3b6002909a01fb47d851e0b9e68efcb16429202a79369fde2b1ab3a`.

**name:** Benevolent Spirits

**activation:** Passive

**cost:** 0

**rangeAndTarget:** One ally below half HP healed by your paid technique

**duration:** Instant

**frequency:** Once/turn

**effect:** Add M HP to that healing. It does not improve multiple targets, copies or triggered heals, and cannot itself trigger Benevolent Spirits again.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:shaman:shaman.hero.bloodcaller.blood-feast

**REVIEWED / reference-VALIDATED — classified components only** · Paid finite self-heal; unavailable Downed; no damage/resource proc

Source: `data/public/class_playtests/shaman.json` / `shaman.hero.bloodcaller.blood-feast`. SHA256 `30b3df4c4300374344e5639bdbe04d81fb1a631d5b5c2a5722c0f016a4bb13b3`.

**name:** Blood Feast

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** Self at start regular turn; hostile bleeding creature within 10 ft

**duration:** Instant

**frequency:** Once/turn

**effect:** Pay 1 RP to regain M HP. Bleeding allies, summons or staged captives cannot qualify. No healing while Downed; secondary heal creates no damage/resource triggers.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:shaman:shaman.hero.bloodcaller.blood-curse

**REVIEWED / reference-VALIDATED — classified components only** · Bleed cure interface; positive-potential magical healing grants its printed CON save, not auto-cure

Source: `data/public/class_playtests/shaman.json` / `shaman.hero.bloodcaller.blood-curse`. SHA256 `34064d553a32ec2626c5cf9fd9dffdfc4c7a53c5027914e0b3a927be699b9319`.

**name:** Blood Curse

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One living enemy within 60 ft

**duration:** 3 target turns

**frequency:** Recharge 3

**effect:** CON save or Bleed 1d4 necrotic at start of each of next 3 turns. Action plus successful Medicine check against class DC ends it; magical healing also permits an immediate CON save to end. Never permanently unhealable; no repeated stacking.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:shaman:shaman.hero.bloodcaller.talon-strike

**REVIEWED / reference-VALIDATED — classified components only** · One-shot next-healing flat reduction

Source: `data/public/class_playtests/shaman.json` / `shaman.hero.bloodcaller.talon-strike`. SHA256 `6d8b5fb22ca3318d686cd4cb983113cde306f655db9875a58b62287826e71029`.

**name:** Talon Strike

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One enemy in claw reach

**duration:** Instant; reduction until end next turn

**frequency:** Recharge 2

**effect:** Make one claw attack; hit adds S d6 necrotic and reduces the next healing it receives by M, minimum 0. Applies once and ends. No arbitrary percent stacking or permanent maximum-HP reduction.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:thief:thief.hero.blackguard.exsanguinate

**REVIEWED / reference-VALIDATED — classified components only** · Paid finite self-heal; unavailable Incapacitated

Source: `data/public/class_playtests/thief.json` / `thief.hero.blackguard.exsanguinate`. SHA256 `37e182dce2daee77d1a02e8e10618f449d263f1fd06d4a1ea9a7db6937821a2f`.

**name:** Exsanguinate

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** Self; bleeding enemy within 15 ft

**duration:** Instant

**frequency:** Once/own turn

**effect:** At start of your regular turn with a hostile bleeding enemy nearby you may pay 1 RP to regain S HP. No multiplying by enemy count or healing while incapacitated; not an ordinary spell or Dissonance-generating technique.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:tinker:tinker.hero.techsmith.snap-rebuild

**REVIEWED / reference-VALIDATED — classified components only** · Device reconstruction, not living healing/resurrection; original slot/expiry retained

Source: `data/public/class_playtests/tinker.json` / `tinker.hero.techsmith.snap-rebuild`. SHA256 `0a8d445d6a86fd84b5dc4587562eb1eab093cd81ae114f10be850ad8f512cd11`.

**name:** Snap Rebuild

**activation:** Bonus Action

**cost:** 2 RP; 1 encounter use

**rangeAndTarget:** One destroyed device/drone within 15 ft

**duration:** Remaining original duration

**frequency:** 1/encounter

**effect:** Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-engine:warrior:24

**REVIEWED / reference-VALIDATED — classified components only** · BOOK Mutation Recovery Reserve; spends only actual HP restored

Source: `data/public/class_playtests/warrior.json` / `24`. SHA256 `8d9be8ad7bbd69c27fc5c86a56943772f63026390522e512a2ec38b145a7eaf6`.

**text:** Finite recovery completion: Mutation Recovery Reserve=3 L+M HP after a long rest. Bloodthick Node, Rapid Coagulation, Regenerative Mutation, Hemophage Core and their healing enhancements draw from this shared reserve, 1 point per actual HP healed. No short-rest refill; no gauge, critical hit, free activation or form change replenishes it. Other explicitly limited-use/dose healing retains its own printed limit. This new test reserve prevents indefinite regenerative healing from free mutation activations.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. Reserve spends only actualHP gained; unchanged reserve does not itself grant permission for excess conversion. Passive Reserve regeneration is explicitly ineligible for excess conversion without a future source exception.

## class-card:warrior:warrior.hero.ironskin.cellular-reconstruction

**REVIEWED / reference-VALIDATED — classified components only** · Finite delayed self-healing after stasis; not passive regeneration

Source: `data/public/class_playtests/warrior.json` / `warrior.hero.ironskin.cellular-reconstruction`. SHA256 `e8bd145d4393467058e51509e15230c1bc315884f24f96ccfb509faa5186d56c`.

**name:** Cellular Reconstruction

**activation:** Action

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of your next regular turn, then instantaneous recovery

**frequency:** 1/long rest

**effect:** Cellular Reconstruction. Enter stasis until the start of your next regular turn: your Speed becomes 0, you cannot take Actions, Bonus Actions or Reactions, and attacks against you have advantage. At the start of your next turn regain 3d8 + M HP and end Poisoned plus one mundane or magical disease that does not explicitly require a special cure. This removes no Wounds and cannot function while dead.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:warrior:warrior.supplement.bloodthick-node

**REVIEWED / reference-VALIDATED — classified components only** · Passive regeneration, Reserve-limited

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.bloodthick-node`. SHA256 `d0a5ce3e76d61b789bfa1ab1daebf96399f56187b8fc796a0e44a1697007618b`.

**name:** Bloodthick Node

**activation:** Passive while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** While active during a real encounter

**frequency:** Once at start of each regular turn

**effect:** Regain HP equal to current BT, maximum 3 HP per turn or 4 with Stack Overflow. No healing occurs outside a real encounter and it removes no Wounds. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

**prerequisite:** Warrior 1; Basic Vital

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. NEW: Unpaid passive Mutation-Reserve regeneration supplies no excess-healing conversion, including Cosmic Equilibrium, despite mathematical excess and zero Reserve spend. Future explicit source exception required.

## class-card:warrior:warrior.supplement.flesh-warden

**REVIEWED / reference-VALIDATED — classified components only** · Maximum-HP stat modifier; never healing

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.flesh-warden`. SHA256 `6ebfcac9c52f7d99711196a075bf63622082e7a932f2ae4086949c4656a23886`.

**name:** Flesh Warden

**activation:** Passive while equipped

**cost:** One mutation slot

**rangeAndTarget:** Self

**duration:** While equipped

**frequency:** Mutation

**effect:** Increase maximum HP by 2 per Warrior level while equipped. Equipping raises maximum only, never current HP. Unequipping clamps current HP to the reduced maximum if necessary; it does not subtract another amount from current HP. Repeated swaps cannot heal.

**prerequisite:** Warrior 1; Basic Vital

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:warrior:warrior.supplement.rapid-coagulation

**REVIEWED / reference-VALIDATED — classified components only** · Passive regeneration, Reserve-limited

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.rapid-coagulation`. SHA256 `8f6169026b8720168ba76650964f555e611eb7cc5c65f24be359a3561fbaa8ad`.

**name:** Rapid Coagulation

**activation:** Passive while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** While active during a real encounter

**frequency:** Start of turn

**effect:** If you did not move during your previous turn, regain 2 HP at the start of your current turn. This does not function outside a real encounter. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.

**prerequisite:** Warrior 6; Advanced Vital

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. NEW: Unpaid passive Mutation-Reserve regeneration supplies no excess-healing conversion, including Cosmic Equilibrium, despite mathematical excess and zero Reserve spend. Future explicit source exception required.

## class-card:warrior:warrior.supplement.adrenal-floodgate

**REVIEWED / reference-VALIDATED — classified components only** · Finite 1/encounter triggered healing, not passive regeneration

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.adrenal-floodgate`. SHA256 `00458063b06700533ef4cd58b5d045311c1a0fe9b663fa20f0fa7fc7414a5c3d`.

**name:** Adrenal Floodgate

**activation:** Triggered while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** 1/encounter

**effect:** When you first fall to one-quarter maximum HP or less, regain 2d8 HP and end either Frightened, Poisoned or Staggered on yourself.

**prerequisite:** Warrior 6; Advanced Vital

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## class-card:warrior:warrior.supplement.bio-stabilizer

**REVIEWED / reference-VALIDATED — classified components only** · Modifier to Bloodthick passive regeneration

Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.bio-stabilizer`. SHA256 `1bc1a0dd29cac0774f73c5c357f1c81ade4efca327bf104ce4004eaad84de7b7`.

**name:** Bio-Stabilizer

**activation:** Passive

**cost:** Feat choice

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Always

**effect:** While at least two mutations are active, Bloodthick Node heals 1 additional HP on each of its valid encounter-only regeneration pulses.

**prerequisite:** Warrior 4; Bloodthick Node equipped; eligible feat grant

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences. NEW: Unpaid passive Mutation-Reserve regeneration supplies no excess-healing conversion, including Cosmic Equilibrium, despite mathematical excess and zero Reserve spend. Future explicit source exception required.

## class-card:wizard:wizard.hero.necromancer.infernal-pact-quest-based-unlock

**REVIEWED / reference-VALIDATED — classified components only** · Gravebrand periodic damage + finite damage-drain healing based on actualDamageDealt

Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.infernal-pact-quest-based-unlock`. SHA256 `3ec78d206b84e52afbca7eefd488313b4aeb4371a3edb80e5f9e6e14636d053d`.

**name:** Infernal Pact (Quest-based unlock)

**activation:** Bonus Action

**cost:** 3 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Maximum 3 rounds

**frequency:** 1/long rest; quest-gated

**effect:** Infernal Pact — Gravebrand. Tags: hero, necromancer, infernal, necrotic, dark-content. This card can be selected only after completing the campaign's Infernal Pact quest and its dark-trauma check-in. Mark one creature. At the start of each of its turns it makes a Constitution save; on failure it takes 1d6 necrotic damage and you regain HP equal to the actual damage dealt, maximum S+M; success ends Gravebrand. Gravebrand ignores necrotic resistance but not immunity. While you possess this Pact, Corpse Harvest and Auto-Raise may also treat Fiend corpses as eligible; other creature types remain ineligible.

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## ordinary-spell:stitch-fate

**REVIEWED / reference-VALIDATED; promoted operational-playtest draft** · INDIVIDUAL DRAFT: stitch-fate; exact object pending review/promotion

Source: `data/public/spell_playtests/catalog.json` / `stitch-fate`. SHA256 `8bd3d12e82603aadef4a255061176b3a859a6ebd496c74b71f68d8187341199f`.

**name:** Stitch Fate

**classAccess:** {"Cleric": {"rank": 8, "minimumClassLevel": 15, "school": "Divination", "baseRpCost": 21}, "Wizard": {"rank": 8, "minimumClassLevel": 15, "school": "Divination", "baseRpCost": 21}}

**coreEntries:** [{"index": 290, "original": {"school": "Divination", "level": 8, "name": "Stitch Fate", "effect": "Change one failed death save or auto-revive a dying target.", "source_paragraph": 9339, "casting_time": "1 action", "range": "120 feet", "duration": "Instantaneous", "components": "V, S, F", "resolution": "Automatic or opposed as described", "tags": ["Utility"], "rp_cost": 21}}]

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## ordinary-spell:death-ward

**REVIEWED / reference-VALIDATED; promoted operational-playtest draft** · INDIVIDUAL DRAFT: death-ward; exact object pending review/promotion

Source: `data/public/spell_playtests/catalog.json` / `death-ward`. SHA256 `163354918258ef27c93d2f829226495e221919cef574c8670224fc154bcd023e`.

**name:** Death Ward

**classAccess:** {"Cleric": {"rank": 4, "minimumClassLevel": 7, "school": "Necromancy", "baseRpCost": 7}, "Crimson Agent": {"rank": 4, "minimumClassLevel": 11, "school": "Necromancy", "baseRpCost": 7}, "Druid": {"rank": 4, "minimumClassLevel": 7, "school": "Necromancy", "baseRpCost": 7}, "Shaman": {"rank": 4, "minimumClassLevel": 10, "school": "Necromancy", "baseRpCost": 7}, "Thief": {"rank": 4, "minimumClassLevel": 18, "school": "Necromancy", "baseRpCost": 7}, "Wizard": {"rank": 4, "minimumClassLevel": 7, "school": "Necromancy", "baseRpCost": 7}}

**coreEntries:** [{"index": 677, "original": {"school": "Necromancy", "level": 4, "name": "Death Ward", "effect": "First time target would drop to 0 HP, they drop to 1 HP instead.", "source_paragraph": 9818, "casting_time": "1 action", "range": "60 feet", "duration": "Concentration, up to 1 minute", "components": "V, S, M/F", "resolution": "Automatic or opposed as described", "tags": ["Ward"], "rp_cost": 7}}]

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## ordinary-spell:resurrection

**REVIEWED / reference-VALIDATED; promoted operational-playtest draft** · INDIVIDUAL DRAFT: resurrection; exact object pending review/promotion

Source: `data/public/spell_playtests/catalog.json` / `resurrection`. SHA256 `7bd8e0cfd7390bd95dd2ae2637ababb87f3058c4def6cd82800346ce0a9535a8`.

**name:** Resurrection

**classAccess:** {"Cleric": {"rank": 7, "minimumClassLevel": 13, "school": "Necromancy", "baseRpCost": 17}, "Druid": {"rank": 7, "minimumClassLevel": 13, "school": "Necromancy", "baseRpCost": 17}, "Shaman": {"rank": 7, "minimumClassLevel": 19, "school": "Necromancy", "baseRpCost": 17}, "Wizard": {"rank": 7, "minimumClassLevel": 13, "school": "Necromancy", "baseRpCost": 17}}

**coreEntries:** [{"index": 701, "original": {"school": "Necromancy", "level": 7, "name": "Resurrection", "effect": "Return a dead creature to life.", "source_paragraph": 9848, "casting_time": "1 action", "range": "120 feet", "duration": "Instantaneous", "components": "V, S, F", "resolution": "Automatic or opposed as described", "tags": ["Utility"], "rp_cost": 17}}]

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## ordinary-spell:mass-resurrection-denial

**REVIEWED / reference-VALIDATED; promoted operational-playtest draft** · INDIVIDUAL DRAFT: mass-resurrection-denial; exact object pending review/promotion

Source: `data/public/spell_playtests/catalog.json` / `mass-resurrection-denial`. SHA256 `9979b9869d187aee99435be6283154576a1639fd64d4c11790d4b22594a8fb52`.

**name:** Mass Resurrection Denial

**classAccess:** {"Cleric": {"rank": 8, "minimumClassLevel": 15, "school": "Necromancy", "baseRpCost": 21}, "Druid": {"rank": 8, "minimumClassLevel": 15, "school": "Necromancy", "baseRpCost": 21}, "Wizard": {"rank": 8, "minimumClassLevel": 15, "school": "Necromancy", "baseRpCost": 21}}

**coreEntries:** [{"index": 705, "original": {"school": "Necromancy", "level": 8, "name": "Mass Resurrection Denial", "effect": "Prevents resurrection of all corpses in area.", "source_paragraph": 9854, "casting_time": "1 action", "range": "120 feet", "duration": "Instantaneous", "components": "V, S, M/F", "resolution": "Automatic or opposed as described", "tags": ["Utility"], "rp_cost": 21}}]

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## ordinary-spell:true-resurrection

**REVIEWED / reference-VALIDATED; promoted operational-playtest draft** · INDIVIDUAL DRAFT: true-resurrection; exact object pending review/promotion

Source: `data/public/spell_playtests/catalog.json` / `true-resurrection`. SHA256 `c926a01ab227991dc144f1c3ceac2fe2b305bd755de89d2d0be6807e2215cb04`.

**name:** True Resurrection

**classAccess:** {"Cleric": {"rank": 9, "minimumClassLevel": 17, "school": "Necromancy", "baseRpCost": 26}, "Druid": {"rank": 9, "minimumClassLevel": 17, "school": "Necromancy", "baseRpCost": 26}, "Wizard": {"rank": 9, "minimumClassLevel": 17, "school": "Necromancy", "baseRpCost": 26}}

**coreEntries:** [{"index": 721, "original": {"school": "Necromancy", "level": 9, "name": "True Resurrection", "effect": "Return a dead creature to life, even without remains.", "source_paragraph": 9872, "casting_time": "1 action", "range": "120 feet", "duration": "Instantaneous", "components": "V, S, F", "resolution": "Automatic or opposed as described", "tags": ["Utility"], "rp_cost": 26}}]

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

## ordinary-spell:soul-bind

**REVIEWED / reference-VALIDATED; promoted operational-playtest draft** · INDIVIDUAL DRAFT: soul-bind; exact object pending review/promotion

Source: `data/public/spell_playtests/catalog.json` / `soul-bind`. SHA256 `057ba7c49d000d6819c30be8ea58c1236f94da544c2e0c557dc749116bd6c2aa`.

**name:** Soul Bind

**classAccess:** {"Cleric": {"rank": 9, "minimumClassLevel": 17, "school": "Necromancy", "baseRpCost": 26}, "Druid": {"rank": 9, "minimumClassLevel": 17, "school": "Necromancy", "baseRpCost": 26}, "Wizard": {"rank": 9, "minimumClassLevel": 17, "school": "Necromancy", "baseRpCost": 26}}

**coreEntries:** [{"index": 725, "original": {"school": "Necromancy", "level": 9, "name": "Soul Bind", "effect": "Trap a dying creature's soul, preventing resurrection.", "source_paragraph": 9876, "casting_time": "1 action", "range": "120 feet", "duration": "Instantaneous", "components": "V, S, F", "resolution": "Automatic or opposed as described", "tags": ["Utility"], "rp_cost": 26}}]

**Operational overlay:** Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.

