# Maximum HP and threshold source register

**REVIEWED / reference-VALIDATED; bounded interface —58 exact source records.**

Original sources are preserved. Each disposition applies only to the stated maximumHP/threshold role; unrelated card/feat mechanics retain their own review requirements.

[Source integrity](MAXIMUM_HP_SOURCE_VALIDATION.json)

## cleric.engine[7]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD

Source data/public/class_playtests/cleric.json / 7 · SHA256 bb84e1b0f1d02ca1f307edee719b2e66036799f2367b1b93511681a7f95dd455.

**text:** Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction.

**Overlay:** Healing/max-HP ceiling guard; no modifier.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.arch.anointed-guardian

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_CROSSING

Source data/public/class_playtests/cleric.json / cleric.arch.anointed-guardian · SHA256 27c6e65cd16abe41a61a71f92375691fce8d8a5255f3d238b1ab8d44699d1ac5.

**name:** Anointed Guardian

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** First ally within 30 feet to fall to one-quarter maximum HP or less

**duration:** 2 rounds

**frequency:** Once per encounter

**effect:** Anointed Guardian. Tags: protection, bishop. The first qualifying ally in an encounter gains a ward for 2 rounds. The first time during each round that ally takes damage, reduce that damage by PB + M, minimum 0. The ward does not prevent conditions attached to an attack unless the damage reduction itself invalidates them under another rule.

**Overlay:** First genuine fall to ≤quarter; max-only change does not trigger.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.hero.saint.aura-of-grace

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_HEAL_ELIGIBILITY

Source data/public/class_playtests/cleric.json / cleric.hero.saint.aura-of-grace · SHA256 7dff7e8271aba866c1b596528fe2e7d1e3f9a1558eeec233922585461bcc9854.

**name:** Aura of Grace

**activation:** Triggered and passive

**cost:** 1 RP per healing pulse

**rangeAndTarget:** Living allies within 15 feet

**duration:** Passive during real encounters

**frequency:** Healing once/own regular turn; critical reduction once/ally/round

**effect:** Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing.

**Overlay:** Below-half checked at pulse target selection.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.hero.saint.divine-rebirth

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_RESURRECTION_HP

Source data/public/class_playtests/cleric.json / cleric.hero.saint.divine-rebirth · SHA256 0911a56a90621bfce24642033cfd99929553c077fa641efacc48d90d4b94e15a.

**name:** Divine Rebirth

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One ally revived by your Cleric feature

**duration:** Instantaneous plus temporary HP for 1 minute

**frequency:** 1/long rest

**effect:** Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.

**Overlay:** Half effective max at return; reviewed viable-return min1 applies.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.hero.saint.merciful-sacrament

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_COST_GATE

Source data/public/class_playtests/cleric.json / cleric.hero.saint.merciful-sacrament · SHA256 1839de6107b950771344a8a77e0c9c45ad81b114131b0969eafab0335a14c466.

**name:** Merciful Sacrament

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your Sacrament

**duration:** For that activation

**frequency:** 1/short rest

**effect:** Merciful Sacrament. Tags: saint, sacrament. When you start Sacrament and at least one living ally inside its initial zone is at or below one-quarter maximum HP, you may reduce that Sacrament's Conviction cost to 0. Its RP cost and all other requirements remain. Because no Conviction is spent, this waived cost does not vent Dissonance.

**Overlay:** Initial-zone ally ≤quarter snapshot when Sacrament starts.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.hero.saint.unyielding-light

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_ZERO_HP_RECOVERY

Source data/public/class_playtests/cleric.json / cleric.hero.saint.unyielding-light · SHA256 2b13f1c09c2c7fba28eb3ac046a34ff52f8a829eafac020aa33b762a96d4236d.

**name:** Unyielding Light

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Up to six living party members within 30 feet, including you

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Unyielding Light. Tags: saint, emergency, healing. When one damage event would leave every conscious living party member within 30 feet at 0 HP, resolve that damage, then before ordinary death-save progression each qualifying living creature at 0 HP regains floor(maximum HP/3), minimum 1. It cannot revive a creature killed outright and removes no Wounds. This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.

**Overlay:** `max(1,floor(max/3))`.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.hero.saint.mass-healing-light

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_HEAL_BONUS

Source data/public/class_playtests/cleric.json / cleric.hero.saint.mass-healing-light · SHA256 dbb502b5ecb5d64d0973a9df82f770cdb8af28300d09a7f6f978d3fef13c2009.

**name:** Mass Healing Light

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** Up to six living allies within 30 feet

**duration:** Instantaneous

**frequency:** Recharge 3 rounds

**effect:** Mass Healing Light. Tags: saint, healing. Roll S d8 + M once. Each target regains that amount. A target below half maximum HP when chosen regains an additional 1d8 HP. Roll that bonus once and apply it to all qualifying targets. This cannot revive the dead or remove Wounds.

**Overlay:** Below-half snapshot when target chosen.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## cleric.hero.cultist.corrupt-divinity

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_CONTROL

Source data/public/class_playtests/cleric.json / cleric.hero.cultist.corrupt-divinity · SHA256 b28343e6f696458ef1e0ca49d5529644e610a9603e84b09db58e597f2157e258.

**name:** Corrupt Divinity

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** One enemy within 60 feet

**duration:** Maximum 2 rounds

**frequency:** Recharge 3 rounds

**effect:** Corrupt Divinity. Tags: cultist, debuff, control. The target makes a Wisdom save. On failure it takes -1 on attack rolls and saving throws. It repeats the save at the end of each turn, ending the effect on success. If a non-player NPC at or below one-quarter maximum HP fails the initial save by 10 or more, it is also Charmed by you until the end of its next turn. This never permanently converts allegiance, changes beliefs or overrides a player character's agency.

**Overlay:** NPC ≤quarter checked at initial resolution.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## dragoon.hero.dragon-guardian.wyrmhide

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · CONTINUOUS_THRESHOLD

Source data/public/class_playtests/dragoon.json / dragoon.hero.dragon-guardian.wyrmhide · SHA256 f514ad790b1d4e61a1120eaa22c47fb6bfaab9218c5c4ef84af5c2a503898d7d.

**name:** Wyrmhide

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self while above half maximum HP

**duration:** While threshold met

**frequency:** Continuous

**effect:** Reduce each damage instance by 2 and gain advantage on CON saves against Bleed, Burn and Poisoned. No blanket condition immunity; effects already present persist and ordinary nonstacking reduction applies.

**Overlay:** Above-half predicate recomputes with effective max.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## mage.hero.lich.flesh-to-ash

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_DAMAGE

Source data/public/class_playtests/mage.json / mage.hero.lich.flesh-to-ash · SHA256 e6eb8ad0d964f777becfb64a89c2f8e3b5c3a23a72106c61afecf2386623c243.

**name:** Flesh to Ash

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** 15-foot-radius sphere centered at a point within 60 feet

**duration:** Instantaneous

**frequency:** Recharge 3 rounds

**effect:** Flesh to Ash. Tags: mage-spell, lich, necrotic, damage. Creatures of your choice in the area make Constitution saves. A target at half maximum HP or more takes S d8 necrotic on failure, half on success. A target below half maximum HP instead takes 2 S d8 necrotic on failure, half on success. Determine the threshold before rolling damage.

**Overlay:** Explicit pre-damage half snapshot.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## mage.hero.lich.soulbound-ritual

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_COMPANION_RECONSTRUCTION

Source data/public/class_playtests/mage.json / mage.hero.lich.soulbound-ritual · SHA256 402e1f7d3575a535865294094b40a0e028c23dff18e64dadc511f20340bc7b0a.

**name:** Soulbound Ritual

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** One of your destroyed bound elite undead companions within 30 feet or its inert binding token

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again.

**Overlay:** Returns companion at half effective max; wider companion lifecycle open.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## monk.engine[9]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_REDUCTION_ENGINE

Source data/public/class_playtests/monk.json / 9 · SHA256 e3923490d9849612190a0954ff0749b6e2517862bdfb1c2d7b5dbdfcff1e2eb7.

**text:** Temporary maximum-HP reductions caused by Monk features do not stack on the same creature; use the largest reduction from your Monk features. Maximum HP cannot be reduced below 1. Unless a card specifies an earlier end, the reduction lasts until the creature completes a short or long rest. Restoring maximum HP does not restore current HP. These effects are temporary combat trauma, not unstated permanent injuries.

**Overlay:** Global strongest operative Monk trauma; separate records/clocks.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## monk.engine[16]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD

Source data/public/class_playtests/monk.json / 16 · SHA256 35f0120ff484cecb5d18360f6532891d2de393ba4d2b5e03a9961b7e2ab07a44.

**text:** Healing from Monk cards cannot exceed maximum HP, restore the dead or remove Wounds unless explicitly stated. Permanent HP recovery and Ki generation cannot be farmed outside encounters. Resurrection effects are explicitly limited-use. No Monk card can instantly kill a target merely because a descriptive source used language such as Death Touch; death continues to follow the game's ordinary damage and dying rules.

**Overlay:** Healing/death guard only.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## monk.hero.iron-fist-master.ribcrusher-strike

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_REDUCTION

Source data/public/class_playtests/monk.json / monk.hero.iron-fist-master.ribcrusher-strike · SHA256 11eb73eb0d8587fb3a965d0b24386deb32cde0270d51810eec36cd841fdcc077.

**name:** Ribcrusher Strike

**activation:** Triggered

**cost:** 2 Ki

**rangeAndTarget:** One creature hit by your unarmed strike

**duration:** Until target completes a short or long rest

**frequency:** Once per target per encounter

**effect:** Ribcrusher Strike. Tags: hero, iron-fist, attack, max-hp. After an unarmed strike hits, spend 2 Ki. The target makes a Constitution save. On failure reduce its maximum HP by S+M, minimum maximum HP 1. This reduction follows the common non-stacking maximum-HP rule and is restored after a completed short or long rest without restoring current HP.

**Overlay:** −(S+M), after attack damage, until completed rest.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## monk.hero.iron-fist-master.bone-breaking-strike

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_REDUCTION

Source data/public/class_playtests/monk.json / monk.hero.iron-fist-master.bone-breaking-strike · SHA256 be603265c88626d789efc7c940a4151d6201a7dd4548f0d8dd7b516afed85fc8.

**name:** Bone-Breaking Strike

**activation:** Action

**cost:** 2 Ki

**rangeAndTarget:** One creature within unarmed reach

**duration:** Until target completes a short or long rest

**frequency:** Recharge 3 rounds

**effect:** Bone-Breaking Strike. Tags: hero, iron-fist, attack, max-hp. Make one unarmed strike. On a hit, the target makes a Constitution save. On failure reduce its maximum HP by 2 S+M under the common non-stacking maximum-HP rule. This creates no persistent broken-limb injury; the maximum returns after a completed short or long rest without restoring current HP.

**Overlay:** −(2S+M), after attack damage.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## monk.hero.way-of-shadow.deathless-silence

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_REDUCTION + OTHER

Source data/public/class_playtests/monk.json / monk.hero.way-of-shadow.deathless-silence · SHA256 a23f961c0455ab3ceeaf270e1f5493914a4d5c257841e084367c9bfc8cd7d1dd.

**name:** Deathless Silence

**activation:** Action

**cost:** 5 Ki + 5 RP

**rangeAndTarget:** Up to three enemies you can perceive within 60 feet

**duration:** Until start of your next regular turn; max-HP reduction until rest

**frequency:** 1/long rest; automatic Hero Final

**effect:** Final — Deathless Silence. Tags: hero, shadow, final, teleportation, max-hp, weave. Until the start of your next regular turn you cannot be targeted by opportunity attacks or Reactions. Teleport adjacent to up to three different chosen enemies in sequence and make one unarmed strike against each. On each hit, the target makes a Constitution save. Failure reduces its maximum HP by 4 S+M under the common non-stacking rule and suppresses one non-core defensive passive it possesses until the end of its next turn; the Director identifies an applicable visible passive before the save. This does not disable core class engines, legendary rules or creature type traits.

**Overlay:** −(4S+M); defensive-passive suppression has separate shorter clock.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## monk.hero.way-of-shadow.death-touch

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_DAMAGE

Source data/public/class_playtests/monk.json / monk.hero.way-of-shadow.death-touch · SHA256 a3a0f7f23883eb6888e379b73620f29e0f12f9945c1d6a4afd376038a342e8ea.

**name:** Death Touch

**activation:** Action

**cost:** 5 Ki

**rangeAndTarget:** One creature within unarmed reach

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Death Touch. Tags: hero, shadow, attack, finisher. Make one unarmed strike. On a hit add 3 S d8 necrotic damage. If the target began the strike at or below one-quarter maximum HP, it also makes a Constitution save; on failure add another 2 S d8 necrotic damage. This never causes automatic death, bypasses no ordinary dying rules and creates no permanent injury beyond the damage actually dealt.

**Overlay:** ≤quarter snapshot at strike start.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.engine[13]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD

Source data/public/class_playtests/oracle.json / 13 · SHA256 915b1cf2d9327231bf75308605d2e2b72abdce2ce052fdecef493dea663af705.

**text:** Healing from Oracle features cannot exceed maximum HP, resurrect the dead or remove Wounds unless a feature explicitly says so. Temporary HP never stack. Encounter-only regeneration and drain cannot be farmed outside meaningful combat. Corpse effects create no XP, loot, RC or repeatable corpse resources unless expressly stated.

**Overlay:** Healing/max ceiling only.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.spiral-touched.spiral-touched-boon-iii

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_DIRECT_RECOVERY

Source data/public/class_playtests/oracle.json / oracle.supplement.spiral-touched.spiral-touched-boon-iii · SHA256 a6358be2e17db52d461c11e2df79d972481dba2c95ebd29ecd7c31a02987d377.

**name:** Spiral-Touched — Boon III

**activation:** Triggered at 0 HP

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of next regular turn

**frequency:** 1/long rest

**effect:** 1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations.

**prerequisite:** Oracle 10; selected Curse:Spiral-Touched

**Overlay:** Quarter effective max, source min1.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.wound-eater.wound-eater-boon-iii

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_HEAL

Source data/public/class_playtests/oracle.json / oracle.supplement.wound-eater.wound-eater-boon-iii · SHA256 d872f36ef75cc9ff431e85c49d7cbfe85cf4b41721c46042c12d9e8af47fea5b.

**name:** Wound Eater — Boon III

**activation:** Action

**cost:** 0

**rangeAndTarget:** One dying hostile living creature touched

**duration:** Instantaneous

**frequency:** 1/short rest; no staged/summoned targets

**effect:** 1/short rest as an Action touch one dying hostile living creature at 0 HP; that creature dies and you regain HP equal to one-quarter your maximum HP rounded down. It cannot trigger from summoned, trivial or staged creatures and removes no Wounds.

**prerequisite:** Oracle 10; selected Curse:Wound Eater

**Overlay:** `floor(selfMax/4)`; no min1.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.wound-eater.wound-eater-boon-v

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_HP_LOSS + HEAL_CAP

Source data/public/class_playtests/oracle.json / oracle.supplement.wound-eater.wound-eater-boon-v · SHA256 76d3f99606a9bb0c358f108d5dba7577ecaa8580e0aef97ef94b235e8dbb4811.

**name:** Wound Eater — Boon V

**activation:** Action

**cost:** 0

**rangeAndTarget:** Up to three living enemies within 20 feet

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** 1/long rest as an Action, up to three meaningful living enemies within 20 feet lose HP equal to the lesser of one-quarter their maximum HP or Oracle level+M; you regain half the total actual HP lost, capped at one-half your maximum HP. Allies, constructs, undead, trivial creatures and summons are unaffected.

**prerequisite:** Oracle 20; selected Curse:Wound Eater

**Overlay:** Target quarter-max loss; self half-max recovery cap.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.burning-blood.burning-blood-boon-iv

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_CROSSING

Source data/public/class_playtests/oracle.json / oracle.supplement.burning-blood.burning-blood-boon-iv · SHA256 eaa7b943b6aa64f2d9052ff86f01a0ef136baa2ad2fccd5fe895fe14f29233c7.

**name:** Burning Blood — Boon IV

**activation:** Triggered on first falling below half HP

**cost:** 0

**rangeAndTarget:** Up to three enemies within 15 feet

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** once per short rest when you first fall below half maximum HP, erupt in a 15-foot fire burst. Enemies make Dexterity saves, taking 2 S d6 fire on failure or half on success; you take no damage from this flare.

**prerequisite:** Oracle 15; selected Curse:Burning Blood

**Overlay:** Genuine first fall strictly below half.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.false-life.false-life-boon-v

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_DELAYED_RECOVERY

Source data/public/class_playtests/oracle.json / oracle.supplement.false-life.false-life-boon-v · SHA256 aca1096e9676527d4009472fd552ae219dc3cf6a5196f4ac4ad30a5c7e064b0b.

**name:** False Life — Boon V

**activation:** Triggered at 0 HP

**cost:** 0

**rangeAndTarget:** Self; undead within 15 feet

**duration:** Rise next turn; immunity two rounds

**frequency:** 1/long rest

**effect:** 1/long rest when you are at 0 HP but not destroyed outright, appear dead until the start of your next regular turn. During that interval you are incapacitated. At the start of your next turn rise with floor(max HP/4), minimum 1, and gain necrotic immunity for 2 rounds. Undead within 15 feet treat you as non-hostile until you damage, control or overtly oppose them. Divination during the apparent-death interval returns one false but plausible state-description you choose; it cannot fabricate events outside your own condition.

**prerequisite:** Oracle 20; selected Curse:False Life

**Overlay:** Quarter effective max at due start, min1.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.bones.death-s-threshold

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_CROSSING + HEALED_EXIT

Source data/public/class_playtests/oracle.json / oracle.supplement.bones.death-s-threshold · SHA256 7e8778eca9a8b8ee70ff366b67e6fd5f43aa3b5aae72cc6d5815df0f86e4abff.

**name:** Death's Threshold

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** Self; undead enemies within 3 tiles

**duration:** Until healed above half maximum HP

**frequency:** 1/short rest

**effect:** The first time after a short rest that you fall to one-quarter maximum HP or less, activate Death's Threshold. Until you are healed above half maximum HP, reduce the first necrotic damage and first nonmagical weapon damage you take each round by S and gain +1 to your Revelation save DC. Undead enemies within 3 tiles take -1 on their first attack roll against you each round. The effect then ends and cannot reactivate until after another short rest.

**prerequisite:** Oracle 6; Mystery: Bones; selected Tier II Revelation

**Overlay:** Trigger by genuine fall ≤quarter; exit requires actual heal to >half.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.bones.ledger-unbound

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_DAMAGE_CAP

Source data/public/class_playtests/oracle.json / oracle.supplement.bones.ledger-unbound · SHA256 ef4172a86bb7ab4929f1689d7d0ae148634a6fc06e32b00d1d601ef71bea270f.

**name:** Ledger Unbound

**activation:** Action

**cost:** 0 RC

**rangeAndTarget:** Enemies and up to 3 eligible corpses within 5 tiles

**duration:** Damage instantaneous; bone servants 3 rounds

**frequency:** 1/long rest

**effect:** Choose up to three enemies in range. Roll 4 S d8+M once; each target takes necrotic damage equal to the lesser of that roll or one-quarter its maximum HP, with a Constitution save for half. This blast cannot reduce HP below 1. Raise up to three nonsummoned corpses as 1-HP bone servants for three rounds. Once per round spend your shared companion Bonus Action to move and attack with ONE servant using your Revelation attack bonus for 1d8+S necrotic damage. Alternatively, your Reaction may sacrifice one servant to intercept a single-target attack against you; no attack is made by that servant that round. Servants grant no XP, loot, harvestable corpses or RC. For three rounds, up to three undead you already control add S damage to their one shared commanded attack and reduce the first damage they take each round by 1. No extra creature turns or command budgets are created.

**prerequisite:** Oracle 20; Mystery: Bones

**Overlay:** Damage ≤floor(targetMax/4), then save; cannot reduce below1.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.flame.crown-restored

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD

Source data/public/class_playtests/oracle.json / oracle.supplement.flame.crown-restored · SHA256 354e4fb2b53a1b46b121c1edc36df4e364f0dbf66931fa7bdb453e68d6f3ab8f.

**name:** Crown Restored

**activation:** Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self and allies within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap.

**prerequisite:** Oracle 20; Mystery: Flame

**Overlay:** Healing capped by ordinary maximum; no max modifier.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.life.verdant-pulse

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_HEAL_RIDER + FLOOR

Source data/public/class_playtests/oracle.json / oracle.supplement.life.verdant-pulse · SHA256 feb0f82538549fb2d540cfa9a68b89f517d4f1138b44ade546065fc7300c24f9.

**name:** Verdant Pulse

**activation:** Passive and Reaction

**cost:** 0 RC

**rangeAndTarget:** Allies you heal; emergency ally within 4 tiles

**duration:** Buff until end of ally's next turn; emergency instantaneous

**frequency:** Buff once per ally per short rest; emergency 1/encounter

**effect:** When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it.

**prerequisite:** Oracle 6; Mystery: Life; selected Tier II Revelation

**Overlay:** “was below half” uses pre-heal state; emergency floor separate.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.time.echo-strike

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · POST_DAMAGE_THRESHOLD

Source data/public/class_playtests/oracle.json / oracle.supplement.time.echo-strike · SHA256 eb631339bca8a9fbada16f055ce6bb3a6ab1703132bbeef0477fd0fae77b34f0.

**name:** Echo Strike

**activation:** Reaction

**cost:** 1 RC

**rangeAndTarget:** Same target just hit by your weapon or touch attack

**duration:** Instantaneous

**frequency:** At most once per round

**effect:** Immediately after your weapon or touch attack hits, spend 1 RC. Copy half the triggering attack's unmodified rolled damage dice total, rounded down, minimum 1, as damage of the same type to the same target. The echo is not another attack, cannot critically hit and copies no flat modifiers, conditions, resource gains or proc triggers. If this copied damage leaves the target below half maximum HP, regain 1 RC after resolution, at most once per round and never above maximum.

**prerequisite:** Oracle 3; Mystery: Time; selected Tier I Revelation

**Overlay:** RC check after echo damage using then-effective max.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## oracle.supplement.time.rewind-wound

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · HISTORICAL_THRESHOLD

Source data/public/class_playtests/oracle.json / oracle.supplement.time.rewind-wound · SHA256 eb01bdc7533669a80e0862bf3130c342b3b8c9c3f4199f8925953086e6bc898c.

**name:** Rewind Wound

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One living ally you touch

**duration:** Healing instantaneous; protection until start of your next turn

**frequency:** At will while RC remains; same damage event can be rewound once

**effect:** Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects.

**prerequisite:** Oracle 6; Mystery: Time; selected Tier II Revelation

**Overlay:** Uses maximum snapshot stored with referenced damage event.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oath-of-mercy.merciful-smite

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · DAMAGE_DERIVED_HEAL

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-mercy.merciful-smite · SHA256 bb24ea1355d04db34e882d50cc5ebadd7b6da097442a0c2813d9e39b6cc5421c.

**name:** Merciful Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack; up to 3 living allies within 10 feet of you

**duration:** Instantaneous

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Your Oath Smite deals radiant damage instead of adding a second Smite packet. After the Smite damage resolves, create a healing pool equal to half the actual radiant Smite damage dealt, rounded down, maximum S+M. Divide that pool among up to 3 living allies within 10 feet. Healing cannot exceed maximum HP, remove Wounds or trigger additional Smite or healing-copy effects.

**prerequisite:** Paladin 3; Oath of Mercy

**Overlay:** No max modifier; healing maximum guard only.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oath-of-mercy.blessing-of-the-meek

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_HEAL_RIDER

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-mercy.blessing-of-the-meek · SHA256 de83f7216e4f442bf324e7e9650e69091077d79b1be79d0753257dfbce13cde4.

**name:** Blessing of the Meek

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One living ally within 30 feet

**duration:** Healing instantaneous; AC bonus until start of your next regular turn

**frequency:** At will while RP remains

**effect:** The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules.

**prerequisite:** Paladin 3; Oath of Mercy

**Overlay:** Below-half checked before healing.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oath-of-mercy.channel-life

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD / DIRECT_HP_LOSS

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-mercy.channel-life · SHA256 791e5b9a6f7de5962bffa02d02d406a4eba8aedc125391595cd002581a5f6610.

**name:** Channel Life

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** Self and one living ally within 30 feet

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Choose X from 1 to Paladin level+M, limited so your current HP remains at least 1. Lose X HP; this loss cannot be reduced, redirected or prevented. The target regains X HP. This is a direct transfer, cannot exceed the target's maximum HP and cannot remove Wounds or create excess temporary HP.

**prerequisite:** Paladin 9; Oath of Mercy

**Overlay:** No max modifier; donor/current-max legality only.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oath-of-vengeance.final-verdict

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_TARGET_GATE

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-vengeance.final-verdict · SHA256 588a235ef97e9f2d39ca847326623ea090b05676da713f90f447f75361e5582d.

**name:** Final Verdict

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** One creature marked by you within 30 feet and at or below half maximum HP

**duration:** Instantaneous or empowerment until end of your next regular turn

**frequency:** At will while RP remains

**effect:** The marked target makes a Constitution save, taking 4 S d8 radiant damage on failure or half on success. On failure it also cannot regain HP until the end of its next turn. If that damage reduces it to 0 HP, use ordinary Downed/death rules; there is no percentage-HP execution. On success your next Smite against it before the end of your next turn uses maximum damage dice. This bounded damage replaces the source draft’s automatic reduction to 0 HP.

**prerequisite:** Paladin 17; Oath of Vengeance

**Overlay:** Must be ≤half at activation.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_DAMAGE

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution · SHA256 42295f38a12b89d74114739244ddfb5ba9e19a6f750356f0cf42fbbdfaf16740.

**name:** Death Touch — Malicious Execution

**activation:** Action

**cost:** Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss

**rangeAndTarget:** One creature within melee reach

**duration:** Instantaneous

**frequency:** At will while Lay on Hands points remain; rider once per turn

**effect:** Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared Lay on Hands points. If the target was already at or below half maximum HP, it makes a Constitution save; on failure add S d6 necrotic damage. This rider never automatically executes or bypasses normal death rules.

**prerequisite:** Paladin 3; Oathbreaker — Oath of Vengeance

**Overlay:** “already” ≤half before rider damage.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oathbreaker-oath-of-vengeance.fearbrand

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_DAMAGE

Source data/public/class_playtests/paladin.json / paladin.supplement.oathbreaker-oath-of-vengeance.fearbrand · SHA256 ecff141c9410cecd56ebbdaabcdb43dd1d6b686aa823a6b17afda3efc4307953.

**name:** Fearbrand

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** Damage instantaneous; Frightened until end of next turn

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Wisdom save. On failure it takes 2 S d6 psychic damage and is Frightened until the end of its next turn; on success it takes half damage and is not Frightened. A target already below half maximum HP takes one additional d6 psychic damage. This creates no execution effect.

**prerequisite:** Paladin 11; Oathbreaker — Oath of Vengeance

**Overlay:** Below-half bonus assessed before its damage.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## paladin.supplement.oath-of-the-martyr-king.crown-undying

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD

Source data/public/class_playtests/paladin.json / paladin.supplement.oath-of-the-martyr-king.crown-undying · SHA256 f8de6f3fe586c6b30d10bbdd31c93e0976aa46dfb3631afbbcbebe8ebe1d0b1d.

**name:** Crown Undying

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to three selected allies in your aura

**duration:** Three rounds; no concentration

**frequency:** 1/long rest

**effect:** For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool.

**prerequisite:** Paladin 20; Oath of the Martyr King

**Overlay:** Heal cannot exceed max; no max modifier.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## shaman.hero.bloodcaller.talon-strike

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · EXCLUSION

Source data/public/class_playtests/shaman.json / shaman.hero.bloodcaller.talon-strike · SHA256 6d8b5fb22ca3318d686cd4cb983113cde306f655db9875a58b62287826e71029.

**name:** Talon Strike

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One enemy in claw reach

**duration:** Instant; reduction until end next turn

**frequency:** Recharge 2

**effect:** Make one claw attack; hit adds S d6 necrotic and reduces the next healing it receives by M, minimum 0. Applies once and ends. No arbitrary percent stacking or permanent maximum-HP reduction.

**Overlay:** Explicitly no permanent/max-HP reduction.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## tinker.hero.artificer.repair-pulse

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_DEVICE_REPAIR

Source data/public/class_playtests/tinker.json / tinker.hero.artificer.repair-pulse · SHA256 bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593.

**name:** Repair Pulse

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Upto 3 friendly devices within 30 ft

**duration:** Instant; AC until start next turn

**frequency:** 1/short rest

**effect:** Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.

**Overlay:** Functional device restores floor(max/2).

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## tinker.hero.techsmith.snap-rebuild

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_DEVICE_RECONSTRUCTION

Source data/public/class_playtests/tinker.json / tinker.hero.techsmith.snap-rebuild · SHA256 0a8d445d6a86fd84b5dc4587562eb1eab093cd81ae114f10be850ad8f512cd11.

**name:** Snap Rebuild

**activation:** Bonus Action

**cost:** 2 RP; 1 encounter use

**rangeAndTarget:** One destroyed device/drone within 15 ft

**duration:** Remaining original duration

**frequency:** 1/encounter

**effect:** Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock.

**Overlay:** Destroyed device restored to floor(max/2); device lifecycle handles viability.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.engine[8]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · PERCENT_THRESHOLD_RESOURCE_ENGINE

Source data/public/class_playtests/warrior.json / 8 · SHA256 99a5efcfe2e2e606bb3782c034b79441119d5183396c4bf53787d8ffc58fae4a.

**text:** BRUTALITY PROGRESS. Begin each real encounter with Brutality Progress 0 and BT 0. Add actual damage you personally deal to meaningful hostile creatures to Brutality Progress, but a single damage event contributes no more than one-quarter of your maximum HP. Crossing cumulative thresholds equal to 25%, 50% and 75% of your maximum HP grants 1 BT each, subject to the BT cap. Crossing 100% triggers Transcendent as described below but does not create a fourth stored BT unless Stack Overflow or another feature raises the cap.

**Overlay:** Brutality contribution/thresholds use reviewed max-HP snapshots; unchanged.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.engine[15]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · GUARD

Source data/public/class_playtests/warrior.json / 15 · SHA256 131241182dc02a463a2ac51c44a39e0d15e63ccfa46eeb436bc8763593d8e312.

**text:** HEALING AND REGENERATION. Warrior healing cannot exceed maximum HP, restore the dead or remove Wounds unless a card explicitly says otherwise. Regeneration and repeated healing effects operate only during real encounters unless their card explicitly permits downtime healing. No corpse, summoned creature, trivial enemy or friendly target can be used to create infinite healing, serum doses or BT.

**Overlay:** Warrior healing maximum/death guard.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.base.brutality-sense

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · CONTINUOUS_THRESHOLD

Source data/public/class_playtests/warrior.json / warrior.base.brutality-sense · SHA256 1e9c30e1f682ae0ef2c634631e163656321ce1f52ce9666e01fa06e6e23b6193.

**name:** Brutality Sense

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Hostile creatures you can perceive within 60 feet

**duration:** While condition remains true

**frequency:** Always

**effect:** Brutality Sense. You know when a visible hostile creature is at or below one-quarter of its maximum HP; it is Vulnerable for your Warrior features that specifically reference a marked vulnerable target. This does not reveal its exact HP or hidden resistances.

**Overlay:** Visible hostile ≤quarter recalculates continuously.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.hero.ironskin.regenerative-mutation

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · CONTINUOUS_BELOW_MAX_HEAL

Source data/public/class_playtests/warrior.json / warrior.hero.ironskin.regenerative-mutation · SHA256 9dcfe6b7b149360e470c0d7940937b13c7bbdc4f696999b93710257158818fd1.

**name:** Regenerative Mutation

**activation:** Passive

**cost:** Spend healing amount from Mutation Recovery Reserve

**rangeAndTarget:** Self

**duration:** While at least one mutation is active in a real encounter

**frequency:** Once at the start of each regular turn

**effect:** Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.

**Overlay:** Eligible while current HP < effective max.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.hero.dreadspawn.pain-empowerment

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · CONTINUOUS_PERCENT_MISSING

Source data/public/class_playtests/warrior.json / warrior.hero.dreadspawn.pain-empowerment · SHA256 2b76787a8cddab4ebacdbf316a7c566f95cc8e0607dcc02cafc57f0dc09741ab.

**name:** Pain Empowerment

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** While below maximum HP

**frequency:** Always

**effect:** Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects.

**Overlay:** Exact full 10% bands from current effective max.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.supplement.flesh-warden

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS

Source data/public/class_playtests/warrior.json / warrior.supplement.flesh-warden · SHA256 6ebfcac9c52f7d99711196a075bf63622082e7a932f2ae4086949c4656a23886.

**name:** Flesh Warden

**activation:** Passive while equipped

**cost:** One mutation slot

**rangeAndTarget:** Self

**duration:** While equipped

**frequency:** Mutation

**effect:** Increase maximum HP by 2 per Warrior level while equipped. Equipping raises maximum only, never current HP. Unequipping clamps current HP to the reduced maximum if necessary; it does not subtract another amount from current HP. Repeated swaps cannot heal.

**prerequisite:** Warrior 1; Basic Vital

**Overlay:** +2×Warrior level while equipped; capacity only.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.supplement.adrenal-floodgate

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_CROSSING

Source data/public/class_playtests/warrior.json / warrior.supplement.adrenal-floodgate · SHA256 00458063b06700533ef4cd58b5d045311c1a0fe9b663fa20f0fa7fc7414a5c3d.

**name:** Adrenal Floodgate

**activation:** Triggered while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** Instantaneous

**frequency:** 1/encounter

**effect:** When you first fall to one-quarter maximum HP or less, regain 2d8 HP and end either Frightened, Poisoned or Staggered on yourself.

**prerequisite:** Warrior 6; Advanced Vital

**Overlay:** First genuine fall to ≤quarter.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.supplement.mythic-carapace

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · CONTINUOUS_DURATION_THRESHOLD

Source data/public/class_playtests/warrior.json / warrior.supplement.mythic-carapace · SHA256 9af81b1909628a95c3cc716c883ed8c38e2cf4b847cf8f43b43ca43e5bb67dbc.

**name:** Mythic Carapace

**activation:** Passive while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** Until encounter ends, mutation ends or you fall below one-quarter maximum HP

**frequency:** Apex mutation

**effect:** Gain DR 3 against all damage and immunity to Bleed, Poisoned and Burn-style ongoing fire effects. Once per encounter when one hit deals more than 20 actual damage after mitigation, gain 1 BT and refresh the remaining duration of your other active mutations to 3 rounds. It grants no serum-profile refresh.

**prerequisite:** Warrior 15; Apex Vital; maximum one Apex equipped

**Overlay:** NEW: ends whenever state is strictly below quarter; >20 actual-damage rider separate.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## warrior.supplement.butcherform-chassis

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · CONTINUOUS_DURATION_THRESHOLD

Source data/public/class_playtests/warrior.json / warrior.supplement.butcherform-chassis · SHA256 623cde33b8f868af96dbfed52d286fbc5b263603e9c44ddfff41ab6b2c0efe59.

**name:** Butcherform Chassis

**activation:** Passive while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Self

**duration:** 3 rounds or until below one-quarter maximum HP

**frequency:** Apex mutation

**effect:** When you take the ordinary Attack action, make one additional melee attack beyond other Extra Attack effects, respecting the one-additional-full-Action guard because this is part of the same Action. Your melee criticals add one extra weapon damage die beyond normal critical dice, not triple total damage. Once per round when you personally kill a meaningful hostile with a melee attack, restore one consumed prepared serum dose, never above reserve capacity.

**prerequisite:** Warrior 15; Apex Combat; maximum one Apex equipped

**Overlay:** NEW: ends whenever state is strictly below quarter.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## wizard.engine[10]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS + EXCLUSIONS

Source data/public/class_playtests/wizard.json / 10 · SHA256 673521960e487b21772372733af6aaa0c478c7f3308b6a58607a3c5ac2d83f99.

**text:** ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn.

**Overlay:** Conjuration +L to Wizard-summoned creatures; other school clauses separate.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## wizard.engine[24]

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS_ENGINE

Source data/public/class_playtests/wizard.json / 24 · SHA256 95c82d28fd1e7975539e00e8550204b4923426cf2050dd14ac56e39197f705b1.

**text:** Flesh Ascendant's bonus applies after the listed base statistics: every undead creature you control gains +2 maximum HP per Wizard level. If at least two of your undead creatures are active, each gains +1 AC and +1 on saving throws. This does not increase the standard-minion or elite-pet caps.

**Overlay:** Flesh Ascendant +2L after listed base; same modifier identity as card.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## wizard.hero.necromancer.flesh-ascendant

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS

Source data/public/class_playtests/wizard.json / wizard.hero.necromancer.flesh-ascendant · SHA256 d42c2937345d5ef23acd97375f6751ada7f9ba7b83ebe12212078d603257e37b.

**name:** Flesh Ascendant

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Undead creatures you control

**duration:** Permanent while active

**frequency:** Always

**effect:** Flesh Ascendant. Tags: hero, necromancer, passive, undead. Each undead creature you control gains +2 maximum HP per Wizard class level. While at least two of your undead creatures are active, each also gains +1 AC and +1 on saving throws. These bonuses apply after the common standard-minion and elite-pet statistics and do not increase companion caps or command frequency.

**Overlay:** Same Flesh Ascendant bonus as engine[24], not cumulative with it.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:exploit_weakness

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · THRESHOLD_ATTACK

Source src/data/feats.js / exploit_weakness · SHA256 95ea910b9634b6361c12f2d3f6008aeecbc0d2e0872119df1dc0f7ed60addc76.

**name:** Exploit Weakness

**description:** At level 7, a combatant seeks wounded enemies for the listed critical chance.

**prerequisite:** Level 7

**effect:** Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.

**legacyEffect:** +15% crit on wounded enemies

**status:** provisional-complete

**source:** Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.

**Overlay:** 19–20 crit range only while target strictly below half.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:familiar_bond

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS_PROVISIONAL

Source src/data/feats.js / familiar_bond · SHA256 bea9d7f867e8c31c4b4e5d07a8db262037fbfa3cdc4843d136e120322d685114.

**name:** Familiar Bond

**description:** Your bond with your familiar is stronger.

**prerequisite:** Ability to cast find familiar

**effect:** Your familiar gains hit points equal to your level and can attack using your spell attack bonus.

**Overlay:** NEW: familiar +owner level max HP; creation starts with boosted max/current, later growth capacity only.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:tenacity

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS_DYNAMIC

Source src/data/feats.js / tenacity · SHA256 5f3e13d83dd42dca3d5fac9ba4fa2e707884921e38b07f80e230d3f013aae461.

**name:** Tenacity

**description:** Level 4 supports the listed +1 HP per level.

**prerequisite:** Level 4

**effect:** Your hit point maximum increases by 1 for each character level, including levels already gained.

**legacyEffect:** +1 HP per level

**status:** provisional-complete

**source:** Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.

**Overlay:** +1 per current character level.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:tough

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS_SNAPSHOT

Source src/data/feats.js / tough · SHA256 525ce21adb774fad8a95a76be8358bf3e37fa8a2649aa2ccecb6c2009cbf45bc.

**name:** Tough

**description:** Your hit point maximum increases.

**prerequisite:** None

**effect:** Your hit point maximum increases by an amount equal to twice your level when you gain this feat.

**Overlay:** +2×level at feat acquisition; no inferred future growth.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:tough_as_nails

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS_DYNAMIC

Source src/data/feats.js / tough_as_nails · SHA256 148868a5e7c860c3f3569c6f3fcade2a1f323ddca3d9cb35609511fce3ed0d86.

**name:** Tough as Nails

**description:** Level 5 supports the listed +10% maximum HP.

**prerequisite:** Level 5

**effect:** Your hit point maximum increases by 2 per character level when you take this feat, and by 2 whenever you gain a level thereafter.

**legacyEffect:** +10% max HP

**status:** provisional-complete

**source:** Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.

**Overlay:** +2 per current level with explicit later-level growth.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:dark_fortitude

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · MAX_HP_BONUS_DYNAMIC + CONTINUOUS_THRESHOLD

Source src/data/feats.js / dark_fortitude · SHA256 852eee532dee1859120104bb0d8f83f5458baa418d3a224d02d255a0e7d7890a.

**name:** Dark Fortitude

**description:** Grave-cold and poison have tried to claim you. They learned your name and backed away. Prestige lineage: Gravetouched. completed from the existing development record.)

**prerequisite:** Constitution 15+

**effect:** You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest). While below half your hit point maximum, you have resistance to poison damage.

**legacyEffect:** You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest). While below half your hit point maximum, you have resistance to poison damage.

**status:** provisional-complete

**source:** Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.

**Overlay:** +2/current level; poison resistance while strictly below half.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.

## feat:life_drinker

**REVIEWED / reference-VALIDATED: supplied maximum-HP/threshold role only** · HEALING + CONTINUOUS_THRESHOLD

Source src/data/feats.js / life_drinker · SHA256 9823f4d451eb12aa8054ad4dd9446cf99d3a7270090e9d9387906b259df516ca.

**name:** Life Drinker

**description:** Every wound you open is a cup. You drink and stand taller. Prestige lineage: Bloodbound. completed from the existing development record.)

**prerequisite:** Dark Affinity or Hemocraft

**effect:** When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.

**legacyEffect:** When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.

**status:** provisional-complete

**source:** Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.

**Overlay:** Crit/kill healing plus +1d4 necrotic while strictly below half.

**Overlay:** Final MAXIMUM_HP_PLAYTEST.md controls over first proposals: global strongest Monk trauma; independent Deathless clocks; strict first-fall crossings; Rewind historical damage can begin already below half; Wizard pair adds under explicit new exception; Tough acquisition snapshot retained.

**Open:** Wider source mechanics, ownership/eligibility lifecycle, full advancement/feat system and unsupplied modifiers remain open. Engine/card Flesh Ascendant aliases must share one runtime effect identity.
