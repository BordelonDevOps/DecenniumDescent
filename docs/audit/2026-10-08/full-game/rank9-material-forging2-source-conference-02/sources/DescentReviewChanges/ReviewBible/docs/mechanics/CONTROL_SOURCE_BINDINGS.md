# Control source bindings

**REVIEWED / reference-VALIDATED — supplied control scope only — 219 supplied passages.** This is not exhaustive whole-game semantic coverage.

[Operational guide](CONTROL_STATES_PLAYTEST.md) · [Coverage](CONTROL_STATE_COVERAGE.md) · [Source checks](CONTROL_STATE_SOURCE_VALIDATION.json)

Each source procedure below remains conditional on its own mode, costs, eligibility, saves, target caps, use limits and source ending. Component IDs identify pieces; they never grant simultaneous application of alternative modes. Historical conference context is preserved in the JSON and audit files, not rendered as competing operational rules.

## class-card:cleric:cleric.base.judging-light

Classification: **HOOK**. Source: `data/public/class_playtests/cleric.json` / `cleric.base.judging-light`. SHA256 `953ae6a8aba08788cc23ffb733cb683b6a230fbe6f2a385aa82546713e1623dd`.

Application components: None applied directly by this binding..

**name:** Judging Light

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Passive

**frequency:** Always

**effect:** Judging Light. Tags: smite, passive. When your Divine Smite damages a creature currently affected by a Cursed or Weakened condition, add S d4 radiant damage to that Smite. Roll these dice once as part of the Smite; they do not create a second hit or trigger.

## class-card:cleric:cleric.base.judgment.judgment

Classification: **ALREADY**. Source: `data/public/class_playtests/cleric.json` / `cleric.base.judgment.judgment`. SHA256 `3a532c5299b8e436235089cb4bd8c2be65b83544a9ce950ba8197f74b7aec26c`.

Application components: `cleric.judged`.

**name:** Judgment

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic only if Judgment was selected

**effect:** Invocation Path — Judgment. Tags: invocation, judgment, smite. When your Divine Smite deals damage to a creature, mark it Judged for 2 rounds. A Judged creature has -1 AC. Further applications refresh the duration but do not increase the AC penalty.

## class-card:cleric:cleric.hero.saint.celestial-resurgence

Classification: **DEFER**. Source: `data/public/class_playtests/cleric.json` / `cleric.hero.saint.celestial-resurgence`. SHA256 `67fbbe3e612fe1dbe47ab927928e4bb8c392086d02926c0059cf915f6d309309`.

Application components: None applied directly by this binding..

**name:** Celestial Resurgence

**activation:** Action

**cost:** 5 Conviction + 10 RP

**rangeAndTarget:** Up to six allied corpses within 30 feet that died during the previous 3 rounds

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** Final Miracle — Celestial Resurgence. Tags: saint, finale, resurrection, rite. Each legal target returns to life at 1 HP. The body must be sufficiently present to sustain life. This removes no Wounds, curses or other death consequences. Divine Rebirth may modify one returned ally if available. The Conviction expenditure can vent Dissonance once under the common rule.

## class-card:cleric:cleric.hero.priest.balanced-scales

Classification: **STATE**. Source: `data/public/class_playtests/cleric.json` / `cleric.hero.priest.balanced-scales`. SHA256 `7e7adca22a150348e1afd85fcf4ca10e7c6a2395883b66b2d889b097f8200b98`.

Application components: `cleric.balanced-scales.mark`.

**name:** Balanced Scales

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Living creatures healed by your Cleric features

**duration:** Until start of your next regular turn

**frequency:** At most once per marked ally per round

**effect:** Balanced Scales. Tags: priest, healing, retaliation. After you restore HP to a living ally, mark it until the start of your next regular turn. The first enemy to damage that ally during the mark takes S + M radiant damage. The retaliation is not an attack, cannot critically hit and cannot recursively trigger another Balanced Scales event.

**Reviewed overlay:** SUPERSESSION from healing conference: damage-event predicates require resolvedDamage>0 before tempHP, distinct from numeric actualDamageDealt=tempAbsorbed+actualHpDamage. Divine Judgment positive packet/numeric0 reflects minimum1 and consumes actual turn; fully prevented resolved0 does neither. See HEALING_DEATH_PLAYTEST.md; original costs/clocks/riders unchanged.

## class-card:cleric:cleric.hero.priest.word-of-binding

Classification: **STATE**. Source: `data/public/class_playtests/cleric.json` / `cleric.hero.priest.word-of-binding`. SHA256 `a0f422fb7033a5da53c5fe2624bbffec397603f479dc3701d9f57173a998093b`.

Application components: `cleric.word-of-binding.damage-hook`, `cleric.word-of-binding.speed-zero`, `core.silenced`.

**name:** Word of Binding

**activation:** Action

**cost:** 5 Conviction + 8 RP

**rangeAndTarget:** Up to six enemies within 30 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** 1/long rest

**effect:** Final Miracle — Word of Binding. Tags: priest, finale, control, rite. Each target makes a Wisdom save. On failure it is Silenced and its Speed becomes 0. At the end of each of its turns it repeats the save, ending both effects on success. While a target remains bound, the first instance of divine or radiant damage it takes each round gains S d6 additional radiant damage. The Conviction expenditure can vent Dissonance once.

## class-card:cleric:cleric.hero.priest.divine-judgment

Classification: **STATE**. Source: `data/public/class_playtests/cleric.json` / `cleric.hero.priest.divine-judgment`. SHA256 `45f9fa6d8a6b222522a99ef51305eb1a111e95826096cd814ee60e45d6ad94ca`.

Application components: `cleric.divine-judgment.mark`.

**name:** Divine Judgment

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One enemy within 60 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** Recharge 3 rounds

**effect:** Divine Judgment. Tags: priest, judgment. The target makes a Wisdom save; success ends the attempt. On failure it is marked. The first time on each of its turns that it deals damage to another creature, it takes radiant damage equal to half that actual damage rounded down, minimum 1, maximum your Cleric level. It repeats the Wisdom save at the end of each turn, ending the mark on success.

**Reviewed overlay:** Reflection triggers once each actual target turn, including extra turns, only first positive actual damage. Ordered victim resolution before damage, no summed victims. Off-turn damage none. Repeat saves/maximum expiry remain regular markers. SUPERSESSION from healing conference: damage-event predicates require resolvedDamage>0 before tempHP, distinct from numeric actualDamageDealt=tempAbsorbed+actualHpDamage. Divine Judgment positive packet/numeric0 reflects minimum1 and consumes actual turn; fully prevented resolved0 does neither. See HEALING_DEATH_PLAYTEST.md; original costs/clocks/riders unchanged.

## class-card:cleric:cleric.hero.cultist.ritual-of-undeath

Classification: **DEFER**. Source: `data/public/class_playtests/cleric.json` / `cleric.hero.cultist.ritual-of-undeath`. SHA256 `3a49348b309930d66ab43fb15262c7062c7849daca1a4939beb6d27d22f9bea1`.

Application components: None applied directly by this binding..

**name:** Ritual of Undeath

**activation:** Action

**cost:** 3 Conviction + 6 RP

**rangeAndTarget:** One eligible corpse within 30 feet or one living ally within 30 feet

**duration:** Mode-dependent

**frequency:** 1/long rest

**effect:** Ritual of Undeath. Tags: cultist, undead, rite. Choose one mode. Corpse Servant: one humanoid corpse dead no more than 1 minute rises for 3 rounds as a temporary thrall with AC 13, 10 HP, Speed 30 feet and one attack only when you spend your shared companion Bonus Action command using your Cleric technique attack bonus; on hit it deals S d6 necrotic. The thrall disappears at 0 HP or when duration ends and grants no XP, loot, new corpse, Conviction or resurrection target. Death Ward: one living ally is marked for 1 minute; the first time it would die during that duration, it instead remains at 1 HP and counts as both humanoid and undead until the end of its next turn. Neither mode removes Wounds. The Conviction expenditure can vent Dissonance once.

## class-engine:crimson-agent:3

Classification: **ALREADY**. Source: `data/public/class_playtests/crimson-agent.json` / `3`. SHA256 `cce77684b7ff646edb46587485d50ee3a89424262dc5711129a5baffc22e0ce6`.

Application components: `crimson-agent.blood-mark`.

**effect:** One Blood Mark at a time on a living target with your Bleed, except Phantom Strike, which explicitly may apply the mark without Bleed. It does not add a free Bleed. Marks last 5 of your regular turns, expire on encounter end or if the target dies, and never create damage by themselves. Rupture requires the target still within 60 ft and line of effect; it spends the mark. A mark does not defeat cover, planar boundaries or bloodlessness. Bloodtrail has its own tracking limits.

## class-engine:crimson-agent:6

Classification: **BOOK**. Source: `data/public/class_playtests/crimson-agent.json` / `6`. SHA256 `1cf75600b60d619ba534b8932db679f4efbf82f37a161224ccfb203ec061d3b2`.

Application components: None applied directly by this binding..

**effect:** At level 1 learn the core Blood Gauge/Bleed rules automatically. Blood Mark and Veinweaver's Core remain selections; Quickblood can be selected and used without a second unlock tax. Veinweaver's Core improves that foundation as printed. Standard scheduled acquisition applies. Bloodbound Edge is automatic 9. At 10 choose Bloodweaver, Shadow Operative or Thirstborn; its Final Cut is automatic 20. Duplicate Hemostasis names are separate Arch and Bloodweaver IDs.

## class-card:crimson-agent:crimson-agent.base.blood-mark

Classification: **ALREADY**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.base.blood-mark`. SHA256 `02b6338cd1c9e7909d4157c3d309229af687b337237fdf5da13d306bb444c3d6`.

Application components: `crimson-agent.blood-mark`.

**name:** Blood Mark

**activation:** Bonus Action

**cost:** 1 BG

**rangeAndTarget:** One living target with your Bleed within 60 ft

**duration:** 5 of your turns

**frequency:** At will, one mark

**effect:** Apply your Blood Mark. Replaces your previous mark without detonating it. The mark enables Rupture and printed mark interactions; it deals no automatic damage and does not grant vision.

## class-card:crimson-agent:crimson-agent.arch.rupture-trigger

Classification: **ALREADY**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.arch.rupture-trigger`. SHA256 `98ce8e906b0bb055a1664a0787d21d76e077aa7b9b7d38828060a643f0b72a08`.

Application components: `crimson-agent.bleed`.

**name:** Rupture Trigger

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 2 other enemies within 5 ft of ruptured mark

**duration:** Bleed 3 turns

**frequency:** Once/round

**effect:** After Rupture damages its marked target, choose up to 2 other living enemies nearby. Each makes CON save; on failure apply one Bleed. These applications do not trigger Rupture again or grant BG.

## class-card:crimson-agent:crimson-agent.arch.rupture

Classification: **HOOK**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.arch.rupture`. SHA256 `3975ef7646aea5ffc4daf17aa64deff51d025e8a74c1dd3390a802207eace4de`.

Application components: None applied directly by this binding..

**name:** Rupture

**activation:** Action

**cost:** 1 BG; consume your mark

**rangeAndTarget:** Your marked enemy within 60 ft

**duration:** Instant

**frequency:** Recharge 2

**effect:** Target makes CON save: (S+1)d8 necrotic on failure, half on success. The mark ends either way; existing Bleed remains. Damage from this technique is not a weapon hit and grants no BG.

## class-card:crimson-agent:crimson-agent.hero.bloodweaver.purify-blood

Classification: **HOOK**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.bloodweaver.purify-blood`. SHA256 `c55e2fab4332f4dfb55146f3b4766e2d71a2b40db580a5a313fe116de9ed3945`.

Application components: None applied directly by this binding..

**name:** Purify Blood

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** One willing living creature touched

**duration:** Instant

**frequency:** Recharge 3

**effect:** End Poisoned and one nonmagical disease. Magical disease needs a successful INT ability check against its stated treatment DC, or DC 15 if absent; failure spends the cost. No curse, Wound, death or Corruption removal.

## class-card:crimson-agent:crimson-agent.hero.shadow-operative.phantom-strike

Classification: **ALREADY**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.shadow-operative.phantom-strike`. SHA256 `7d3d1daa322886709b2a80a186924cc42c43121dc165988a66b5c1ece15f92f7`.

Application components: None applied directly by this binding..

**name:** Phantom Strike

**activation:** Action

**cost:** 2 BG

**rangeAndTarget:** One enemy in weapon reach; must be hidden from it

**duration:** Instant

**frequency:** Recharge 3

**effect:** Make one weapon attack with advantage. On hit add S d6 damage and apply a mark without its usual BG cost, even if not already bleeding. The mark replaces your old mark; no free Rupture occurs. Normal hit BG gain still capped.

## class-card:crimson-agent:crimson-agent.hero.thirstborn.hemorrhagic-plague

Classification: **ALREADY**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.thirstborn.hemorrhagic-plague`. SHA256 `44080ee71da09f24bd82d526545d629f47f2df467d7c5d9403b40ec8ea3255ae`.

Application components: `crimson-agent.bleed`.

**name:** Hemorrhagic Plague

**activation:** Triggered

**cost:** 1 BG

**rangeAndTarget:** One new living enemy within 5 ft of a Bleed victim

**duration:** Bleed 3 turns

**frequency:** Once every 3 of your turns

**effect:** After one of your Bleeds ticks, pay 1 BG; new target makes CON save. Failure applies one Bleed. A spread instance cannot spread again. This grants no BG and does not duplicate marks or immediate damage.

## class-card:crimson-agent:crimson-agent.hero.thirstborn.carrion-conductor

Classification: **STATE**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.thirstborn.carrion-conductor`. SHA256 `f4b09643acdf450c68fbeaf2eaa04a4dd669a090b52ffbbc756318ff79716218`.

Application components: `crimson-agent.carrion-conductor.corpse-mark`, `crimson-agent.carrion-conductor.used-corpse`.

**name:** Carrion Conductor

**activation:** Bonus Action

**cost:** 2 RP

**rangeAndTarget:** One fresh hostile living-combatant corpse within 30 ft

**duration:** Until end next turn

**frequency:** Recharge 3

**effect:** Mark the corpse once; on activation or before expiry use Reaction to burst it. Up to 3 enemies within 5 ft make DEX saves: S d6 necrotic, half on success. Corpse cannot be reused, raised by this effect or provide BG/kill triggers.

**Reviewed overlay:** Separate persistent source-specific used-corpse history survives expiration/consumption/suppression; no second Carrion use by any owner. No universal ban on unrelated corpse mechanics.

## class-card:dragoon:dragoon.base.draconic-discipline

Classification: **HOOK**. Source: `data/public/class_playtests/dragoon.json` / `dragoon.base.draconic-discipline`. SHA256 `65f98c9ee260dc50d1d6b2a0481adab398e9a9db294efe62f83172aec977ccf4`.

Application components: None applied directly by this binding..

**name:** Draconic Discipline

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** While known

**frequency:** Continuous

**effect:** Gain advantage on saves against being knocked Prone or forcibly moved. It does not protect against Stunned, spell damage or grappling unless the save also imposes one of those named effects.

## class-card:dragoon:dragoon.hero.dragon-guardian.aegis-leap

Classification: **NONSTATE**. Source: `data/public/class_playtests/dragoon.json` / `dragoon.hero.dragon-guardian.aegis-leap`. SHA256 `e223d53b9a64e7fc7afb799a361679771118188fe39cbdc07c5d51809c3cd278`.

Application components: None applied directly by this binding..

**name:** Aegis Leap

**activation:** Reaction

**cost:** 2 Momentum

**rangeAndTarget:** Ally within 15 ft targeted by an attack

**duration:** One attack

**frequency:** Recharge 2

**effect:** Before the attack roll, leap to an empty space adjacent to ally using this supplied movement. Become the target if the attack can reach you; resolve against your AC. Cannot be used if restrained or no path. Counts as your one intercept reaction.

## class-card:dragoon:dragoon.hero.drake-rider.drake-mark

Classification: **STATE**. Source: `data/public/class_playtests/dragoon.json` / `dragoon.hero.drake-rider.drake-mark`. SHA256 `9afb568a37f0fa061df1417fc822fe86304501a9ff6b748ca9b28d742c742ee9`.

Application components: `dragoon.drake-mark`.

**name:** Drake Mark

**activation:** Passive

**cost:** 0

**rangeAndTarget:** One creature hit by your leap

**duration:** Until end next turn

**frequency:** Once/own turn

**effect:** Mark that creature; your first subsequent direct polearm hit adds S damage. A new mark replaces old. No extra damage to the triggering leap, Do Ts or copies; it is not a spell mark.

## class-card:dragoon:dragoon.hero.dragon-tyrant.tyrant-s-impale

Classification: **STATE**. Source: `data/public/class_playtests/dragoon.json` / `dragoon.hero.dragon-tyrant.tyrant-s-impale`. SHA256 `1799ef7e338672002fa915d074abba2bdb4cdd74458d2c7d912b774afb59e697`.

Application components: `core.restrained`, `dragoon.bleed`, `dragoon.tyrants-impale.restraint`.

**name:** Tyrant's Impale

**activation:** Action

**cost:** 2 Momentum

**rangeAndTarget:** One enemy in polearm reach

**duration:** Instant; pin until end next turn

**frequency:** Recharge 3

**effect:** Weapon attack; hit adds S d6 piercing. A hit creature no more than one size larger makes STR save or is Restrained and Bleeding. It may use Action STR(Athletics) or DEX(Acrobatics) versus class DC to end restraint. You must stay in reach to maintain pin.

## class-engine:druid:6

Classification: **BOOK**. Source: `data/public/class_playtests/druid.json` / `6`. SHA256 `a9e0ff5d0d4f1cee036ea5216f27aba8af61b3bd02874fe3ff714a9b608e6a70`.

Application components: None applied directly by this binding..

**effect:** Circle summary: Land preserves lore and recovery; Moon improves shifting; Storm controls lightning and wind; Thorns works poison and roots; Winterfang works cold; Rotshaper uses bounded swarms; Ashen Grove works fire and regrowth. Land/Thorns duplicate Blight Elk and Tanglemaw names are kept as separate source identities. Source auto-failed hostile saves in Master of Decay/Ash become once/turn-2 on one save, not unavoidable control. Stronger supplemental flavor riders are represented explicitly below or retained as unadopted alternatives in source provenance.

## class-card:druid:druid.base.panther-form-stealth

Classification: **STATE**. Source: `data/public/class_playtests/druid.json` / `druid.base.panther-form-stealth`. SHA256 `8daa235b54a30f029be0ab4ec9285f0787742efb78cd905b848ebcb572158396`.

Application components: `core.grappled`, `druid.panther.grapple`.

**name:** Panther Form (Stealth)

**activation:** Action attack; passive form traits

**cost:** One shift

**rangeAndTarget:** Self; claw 5 ft

**duration:** While in Panther

**frequency:** One claw/Action

**effect:** Speed 40 ft, darkvision 60 ft, +4 Stealth. Claw 2d4 slashing+WIS; after 20 ft straight approach hit, STR save or Grappled. Escape Action against Druid DC; ends on separation/reversion. Only one held target, no free Restrained.

## class-card:druid:druid.hero.timeless-body

Classification: **NONSTATE**. Source: `data/public/class_playtests/druid.json` / `druid.hero.timeless-body`. SHA256 `17c46885fc461732c1e22f1af86d1a60618c22f2ba7c3880e62ae8c0fa61e52e`.

Application components: None applied directly by this binding..

**name:** Timeless Body

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic

**effect:** Age one year per ten elapsed years. Does not prevent damage, aging magic, hunger, disease or rest requirements, and grants no retroactive lifespan restoration.

## class-card:druid:druid.hero.land.nature-s-ward

Classification: **HOOK**. Source: `data/public/class_playtests/druid.json` / `druid.hero.land.nature-s-ward`. SHA256 `d07ea28918d158de8873583d8beb09dd4b6d3968910b60ef1cef63bdc227c3ed`.

Application components: None applied directly by this binding..

**name:** Nature's Ward

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Land Circle self

**duration:** Permanent

**frequency:** Automatic Circle feature

**effect:** Immune to Charmed/Frightened from fey/elementals, poison damage, Poisoned and disease. Does not suppress all creature abilities or remove an existing curse.

## class-card:druid:druid.hero.land.tanglemaw

Classification: **STATE**. Source: `data/public/class_playtests/druid.json` / `druid.hero.land.tanglemaw`. SHA256 `b916c4ba9ccc394e5cf2eb6cbc02344c0e211daec1698938f6d2403aaab415ab`.

Application components: `core.restrained`, `druid.tanglemaw.restraint`.

**name:** Tanglemaw

**activation:** Action bite; passive traits

**cost:** One shift

**rangeAndTarget:** Land Hero; bite 5 ft; sense 30 ft

**duration:** While in Tanglemaw

**frequency:** Retaliation once/round

**effect:** Bite 2d6+WIS piercing, STR save or Restrained until end next turn, escape Action against DC. Thorny Body deals 1d4 piercing to one melee attacker after hit; no reflections. Sense ground-contact locations 30 ft on same connected surface, not identities through stone walls.

## class-card:druid:druid.hero.thorns.tanglemaw

Classification: **STATE**. Source: `data/public/class_playtests/druid.json` / `druid.hero.thorns.tanglemaw`. SHA256 `daff5c2781baba250c2131a002539a6f80d7a7a2884ebaaed94b81d541d90e08`.

Application components: `core.restrained`, `druid.tanglemaw.restraint`, `druid.thorns-tanglemaw.restrained-damage`.

**name:** Tanglemaw

**activation:** Action bite; passive traits

**cost:** One shift

**rangeAndTarget:** Thorns Hero; bite 5 ft; sense 30 ft

**duration:** While in Tanglemaw

**frequency:** Retaliation once/round

**effect:** Bite 2d6+WIS piercing, STR save or Restrained through end next turn, Action escape DC. One melee attacker/round takes 1d4 piercing; one creature restrained by your bite takes 1d4 at start turn. Ground sense 30 ft same surface and advantage against Prone; no wall-penetrating identification.

## class-card:druid:druid.arch.winterfang.winter-s-embrace

Classification: **STATE**. Source: `data/public/class_playtests/druid.json` / `druid.arch.winterfang.winter-s-embrace`. SHA256 `8d621065dda6ad3f71dc015f8a3d5316dac5e64f2358607c6160547fa1c58457`.

Application components: `druid.winters-embrace.slow`.

**name:** Winter's Embrace

**activation:** Bonus Action

**cost:** One short-rest use

**rangeAndTarget:** Winterfang Circle; 10 ft radius

**duration:** Concentration, 3 rounds

**frequency:** 1/short rest

**effect:** Up to 3 enemies starting turn inside CON save or 1d6 cold and Speed-10 ft through end turn. Once/enemy/round; success no effect. Does not stack multiple slows or affect flying targets outside sphere.

**Reviewed overlay:** Slow ends at current triggering actual turn end. No turn underway:6 elapsed seconds; printed once/enemy/round cap retained.

## class-card:druid:druid.hero.winterfang.snow-leopard

Classification: **HOOK**. Source: `data/public/class_playtests/druid.json` / `druid.hero.winterfang.snow-leopard`. SHA256 `45a815d53f107787811abec352814026ffae437e83a0891e5bf3a8f21f262755`.

Application components: None applied directly by this binding..

**name:** Snow Leopard

**activation:** Action claw; passive traits

**cost:** One shift

**rangeAndTarget:** Winterfang Hero; claw 5 ft

**duration:** While in Snow Leopard

**frequency:** One claw/Action

**effect:** Claw 2d6+WIS cold, +1d4 once/turn against slowed foe. +5 Stealth on ice/snow and advantage on legal Hide there; source+10 reduced provisionally. Ignore ordinary ice/snow movement penalties, not magical restraining ice.

## class-card:druid:druid.hero.rotshaper.carrion-rat-king

Classification: **APPLY**. Source: `data/public/class_playtests/druid.json` / `druid.hero.rotshaper.carrion-rat-king`. SHA256 `66cae86b4ff384703f2aef8cc07dfd610085034b0922e02a461f86e74f20cc66`.

Application components: `core.poisoned`.

**name:** Carrion Rat King

**activation:** Action bite or summon

**cost:** One shift; summon 1 Form Surge

**rangeAndTarget:** Rotshaper Hero; bite 5 ft/swarm 30 ft

**duration:** While in Carrion Rat King

**frequency:** Summon 1/shift and finite reserve

**effect:** Bite 1d8+WIS piercing+2d6 poison; CON save or Poisoned through end next turn. Immune disease/Poisoned, not poison damage. Summon Action creates one bounded engine swarm 1 minute, same command budget; replaces previous form swarm.

## class-engine:mage:16

Classification: **DEFER**. Source: `data/public/class_playtests/mage.json` / `16`. SHA256 `990a5f4954c447d71ce057581dedcecb4bde3ad8312d4dd11841601fe573135c`.

Application components: None applied directly by this binding..

**effect:** Before the irreversible Lich roll, the Director must explicitly tell the player the historical failure stakes: permanent loss of spellcasting, transformation into a cursed melee undead NPC, hostile faction consequences, cursed-gear restriction and no further XP as that retired PC. The player must explicitly opt into that retirement risk before rolling. If the player declines, the ritual stops before the roll and the character must choose another Hero path for this playtest; no irreversible consequence is applied.

## class-card:mage:mage.hero.archmage.purifying-beam

Classification: **HOOK**. Source: `data/public/class_playtests/mage.json` / `mage.hero.archmage.purifying-beam`. SHA256 `2e585488a15f55cd62d2dfba8241864c4681ae1911eaefb365a5ac9db0f517f5`.

Application components: None applied directly by this binding..

**name:** Purifying Beam

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** 60-foot-long, 5-foot-wide line

**duration:** Instantaneous

**frequency:** Recharge 3 rounds

**effect:** Purifying Beam. Tags: mage-spell, archmage, radiant, cleansing. Enemies in the line make Dexterity saves, taking (S+1)d8 radiant damage on failure or half on success. Up to M allies in the line may each end one of Charmed, Frightened or Poisoned. Cleansing does not remove Wounds, curses or disease unless another rule expressly allows it. This non-Focus spell clears an active Nuke Chain.

## class-card:mage:mage.hero.lich.undead-immunities

Classification: **HOOK**. Source: `data/public/class_playtests/mage.json` / `mage.hero.lich.undead-immunities`. SHA256 `747624414164380afb98bb638a6d2228da28a461779d7dcafe0567228eb14f25`.

Application components: None applied directly by this binding..

**name:** Undead Immunities

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent after successful Lich transformation

**frequency:** Always

**effect:** Undead Immunities. Tags: lich, undead. You are immune to poison damage, the Poisoned condition, disease, Frightened, Charmed and magical sleep. You no longer need to breathe. You still require the normal rest schedule for mechanical recovery and can still be affected by abilities that specifically target undead unless another feature says otherwise.

## class-card:mirrorsage:mirrorsage.hero.light-weaver.light-binding

Classification: **STATE**. Source: `data/public/class_playtests/mirrorsage.json` / `mirrorsage.hero.light-weaver.light-binding`. SHA256 `bd999f909188f36b4a93e1aad1cbb9f95ce903486eff3d1d51ad2150a1e06409`.

Application components: `core.restrained`, `mirrorsage.light-binding.restraint`.

**name:** Light Binding

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** Up to 2 creatures within 30 ft

**duration:** Until end your next turn

**frequency:** Recharge 3

**effect:** Choose mode: enemies make STR save or Restrained; they repeat save at turn end. OR up to 2 allies gain S d6+M temporary HP. No mixed modes; bonds are magical and not permanent objects.

## class-card:mirrorsage:mirrorsage.hero.light-weaver.purifying-reflection

Classification: **HOOK**. Source: `data/public/class_playtests/mirrorsage.json` / `mirrorsage.hero.light-weaver.purifying-reflection`. SHA256 `2646544b5c9adf14794d43c6e1b609e99606ed3129a977dc933d4808df0f9d69`.

Application components: None applied directly by this binding..

**name:** Purifying Reflection

**activation:** Reaction

**cost:** 5 RP; 1 long-rest use

**rangeAndTarget:** Ally within 30 ft failing save against Charmed/Frightened/Poisoned

**duration:** Instant

**frequency:** 1/long rest

**effect:** Ally rerolls that save with advantage; use new result. If it succeeds, it regains S d6 HP. No arbitrary curse or death reversal; costs remain if it fails. This is not a captured Echo and creates no record.

## class-card:mirrorsage:mirrorsage.hero.mirror-mage.reflected-repertoire

Classification: **BOOK**. Source: `data/public/class_playtests/mirrorsage.json` / `mirrorsage.hero.mirror-mage.reflected-repertoire`. SHA256 `c24078e714fc565627d7069b1ac284e8981cbf909c56711d510017cf92a6403b`.

Application components: None applied directly by this binding..

**name:** Reflected Repertoire

**activation:** Bonus Action

**cost:** 8 RP; 1 long-rest use

**rangeAndTarget:** Up to 3 records currently in your archive

**duration:** Next 3 releases within 1 minute

**frequency:** 1/long rest

**effect:** Mark up to 3 distinct existing records. Each one's next release keeps its record instead of consuming it; still pay release RP and obey one release/round. No restoration of already empty slots, no invented records, no reuse-preservation after its marked use.

## class-engine:monk:8

Classification: **BOOK**. Source: `data/public/class_playtests/monk.json` / `8`. SHA256 `783093fd2be807987c3fb4c70aec16eb4ef4f4797a3a71e5af2e1f65d4be7e1c`.

Application components: None applied directly by this binding..

**effect:** STUN GUARD. A creature can be Stunned by your Monk features at most once per encounter. Mark it after the first Monk-caused Stunned condition successfully applies. If another of your Monk features would Stun that marked creature later in the same encounter, the creature still makes the required save; on failure it instead loses its Reaction until the end of its next turn. This guard is tracked separately for each Monk.

## class-engine:monk:18

Classification: **BOOK**. Source: `data/public/class_playtests/monk.json` / `18`. SHA256 `2c16b050f07ea51ea401eb66d2609be5b6b0d82f958fd9092b2c2372b6c4eb4c`.

Application components: None applied directly by this binding..

**effect:** Each technique tagged weave creates 1 D in this pilot, unless it explicitly says otherwise. Ki can prevent up to 1 D before resolution only if remaining Ki pays that additional cost. Full-Ki capstones may legally accept D. The Stun Guard shares the suite-wide once/character/target hard-denial mark; its later failed-save fallback of reaction loss is an explicit Monk exception, not a second Stun.

## class-card:monk:monk.base.stunning-strike

Classification: **APPLY**. Source: `data/public/class_playtests/monk.json` / `monk.base.stunning-strike`. SHA256 `d94b2a85b66e51f3d2735237e5716b5d31d3487fa6dd0718ba069691a8afd13a`.

Application components: `core.stunned`, `monk.stunning-strike.reaction-denial`.

**name:** Stunning Strike

**activation:** Action

**cost:** 2 Ki

**rangeAndTarget:** One creature within unarmed reach

**duration:** Until end of target's next turn

**frequency:** Once per target per encounter for Stunned

**effect:** Stunning Strike. Tags: base, active, attack, control. Make one unarmed strike. On a hit the target makes a Constitution save. On failure it is Stunned until the end of its next turn, subject to the common Monk Stun Guard. On success it suffers only the strike's normal damage. A creature already marked by your Stun Guard instead loses its Reaction on a failed save.

## class-card:monk:monk.hero.enlightened-master.serenity-breaker-palm

Classification: **HOOK**. Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.serenity-breaker-palm`. SHA256 `3a2cc91a74bba40913a2d66b6e0664a0f2becf46ebefa4f5632450377e4f9b69`.

Application components: None applied directly by this binding..

**name:** Serenity Breaker Palm

**activation:** Action

**cost:** 3 Ki

**rangeAndTarget:** One enemy within unarmed reach; allies within 10 feet

**duration:** Instantaneous

**frequency:** Recharge 3 rounds

**effect:** Serenity Breaker Palm. Tags: hero, enlightened, attack, cleanse. Make one unarmed strike. On a hit, choose up to M living allies within 10 feet of you; each may end either Charmed, Frightened or Poisoned. The cleansing occurs only if the strike hits. It removes no Wounds, curses or disease and generates no Ki beyond ordinary attack generators.

## class-card:monk:monk.hero.enlightened-master.healing-touch

Classification: **HOOK**. Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.healing-touch`. SHA256 `ca275c05e4d877cf61c5267324d7cc9026d4e5cce39428e9821125f72d92555b`.

Application components: None applied directly by this binding..

**name:** Healing Touch

**activation:** Action

**cost:** 2 Ki + 1 RP

**rangeAndTarget:** One living creature you touch

**duration:** Instantaneous

**frequency:** Recharge 2 rounds

**effect:** Healing Touch. Tags: hero, enlightened, healing, weave. The target regains S d8+M HP and may immediately repeat one saving throw against Poisoned or disease if that effect normally permits repeated saves. This does not resurrect, remove Wounds or automatically cure disease. It is a minor Weave technique; the common extra-Ki payment may prevent its 1 Dissonance.

## class-card:monk:monk.hero.enlightened-master.purifying-palm

Classification: **HOOK**. Source: `data/public/class_playtests/monk.json` / `monk.hero.enlightened-master.purifying-palm`. SHA256 `fed9683083d25c9c017a081488870fdbae034e535d36055d3b74decc896b5309`.

Application components: None applied directly by this binding..

**name:** Purifying Palm

**activation:** Action

**cost:** 2 Ki

**rangeAndTarget:** One enemy within unarmed reach; allies within 10 feet

**duration:** Instantaneous

**frequency:** Recharge 2 rounds

**effect:** Purifying Palm. Tags: hero, enlightened, attack, cleanse. Make one unarmed strike. On a hit choose up to two allies within 10 feet. Each may end Frightened or Poisoned. If you spend one additional Ki after the hit, one chosen ally may instead end Charmed. It removes no curse, disease or Wound.

## class-card:monk:monk.hero.way-of-shadow.nerve-strike

Classification: **STATE**. Source: `data/public/class_playtests/monk.json` / `monk.hero.way-of-shadow.nerve-strike`. SHA256 `2be5bf1c24ea464cc3c18a61339404a31fd6a3c5178d5b5402ecf928ad34a79b`.

Application components: `monk.nerve-strike.reaction-bonus-denial`, `monk.nerve-strike.speed-zero`.

**name:** Nerve Strike

**activation:** Action

**cost:** 2 Ki

**rangeAndTarget:** One creature within unarmed reach

**duration:** Until end of target's next turn

**frequency:** Recharge 2 rounds

**effect:** Nerve Strike. Tags: hero, shadow, attack, control. Make one unarmed strike. On a hit the target makes a Constitution save. On failure choose one: its Speed becomes 0 until the end of its next turn, or it loses its Reaction and cannot take Bonus Actions during that period. This causes no permanent nerve injury.

## class-engine:oracle:2

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `2`. SHA256 `1f8f82e024aa646d5ece8154ad59e4da0d7fd58dfe28bd187a56b85ba451ff11`.

Application components: None applied directly by this binding..

**effect:** The Oracle is an exceptional progression class rather than a 25-choice Base/Arch/Hero class. Base Oracle is levels 1-2, Revelation Tier development is the Arch-stage progression at levels 3-9, and Revelation Mastery is the Hero-stage progression at levels 10-20. Mystery and Curse are chosen at level 1 but their later Revelations, Boons and Final abilities remain class-level gated.

## class-engine:oracle:3

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `3`. SHA256 `f6e9c61b425e06da50fb57ca05f565571fbb295f30460b42fe69cca65507121c`.

Application components: None applied directly by this binding..

**effect:** Choose exactly ONE Mystery and exactly ONE Curse at Oracle level 1. They are not parallel subclasses that stack. You never gain another Mystery or Curse unless a future explicit retraining or transformation rule says otherwise. Curse limitations are permanent and cannot be removed by ordinary cleansing, curse removal, resurrection or rest.

## class-engine:oracle:15

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `15`. SHA256 `520be149d81cfcb90c9921ea7973adac1aaf86fc6ffb3f741baaf4467dd693cb`.

Application components: None applied directly by this binding..

**effect:** BASE PROGRESSION. At Oracle 1 choose Mystery and Curse; gain the RC engine, Channel Revelation, Prophetic Insight and Divine Sense. At Oracle 2 gain Curse Manifestation, Oracular Trance and Oracle's Burden. No Base feature-selection currency or Skill Points are used.

## class-engine:oracle:16

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `16`. SHA256 `d30b62db0014f6cc763e0f12cf0121cffda7444cb03651593ce856010a8b5bcf`.

Application components: None applied directly by this binding..

**effect:** ARCH-STAGE PROGRESSION. Oracle 3: choose one Tier I Revelation from your Mystery and automatically gain Curse Boon I. Oracle 4: separate ASI or eligible feat. Oracle 5: automatically gain Curse Boon II; any Mystery-specific level-5 feature recorded by the registry belongs to the Mystery module below and does not create an additional generic feature here. Oracle 6: choose one Tier II Revelation and gain Mystery Surge. Oracle 8: separate ASI or eligible feat. Oracle 9: gain your Mystery's fixed Tier III Revelation.

## class-engine:oracle:17

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `17`. SHA256 `b6370e5a552488db50746a0e8e705a8080c067d90f5a3157dca29c78322247a1`.

Application components: None applied directly by this binding..

**effect:** HERO-STAGE PROGRESSION. Oracle 10: gain Curse Boon III and Grand Revelation Foreshadow. Oracle 11: RC cap reaches 7 and the preserved encounter-start RC floor becomes active. Oracle 12: gain the Mystery-specific Mystic Insight. Oracle 13: preserved registry draft grants a second Tier II Revelation; after each completed short rest choose which of your two Tier II Revelations is Attuned for features that specifically refer to an active Tier II option, though both remain known and usable. Oracle 14: separate ASI or eligible feat. Oracle 15: gain Revelation Mastery and Curse Boon IV. Oracle 16: preserved Prophecy Trigger Mastery. Oracle 17: preserved Grand Revelation Foreshadow upgrade. Oracle 18: Prophetic Surge. Oracle 19: separate ASI or eligible feat. Oracle 20: gain the Mystery's Final Revelation and Curse Boon V.

## class-engine:oracle:20

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `20`. SHA256 `f9f65d3c11efc3bd87682befab67fc00f5c1550f3176c38961c06ef2c2d6ac25`.

Application components: `oracle.curse-manifestation.self-state`.

**effect:** CURSE MANIFESTATION provides a common operational intensification rather than ten different hidden sub-engines. When activated, your Curse becomes visibly or metaphysically dominant for 3 rounds: gain +1 on Revelation attacks and +1 to Revelation save DC, but take -1 AC and -1 on your own saving throws for the duration. Any Curse limitation that can normally be voluntarily suppressed cannot be suppressed during Manifestation.

## class-engine:oracle:21

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `21`. SHA256 `48a798dca2f2a1601ee8ca1fac4d471e8700d354030e1d3cb09b37922dbfac54`.

Application components: None applied directly by this binding..

**effect:** CURSE BOONS are automatic at Oracle levels 3, 5, 10, 15 and 20 for your ONE selected Curse. You do not choose between Curse Boons and do not gain Boons from unselected Curses. Each Curse card below operationalizes all five Boon gates and its permanent limitations.

## class-engine:oracle:22

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `22`. SHA256 `3e8f57c811ee62d8abff23449fb450bfcf0d0aaacd06d2f28755478552dd5200`.

Application components: None applied directly by this binding..

**effect:** All class gates use Oracle class level, not total character level. Normal proficiency bonus follows the game's ordinary total-character-level rule. Non-Oracle levels do not raise RC maximum, unlock Curse Boons, Revelations, Mystic Insight, Revelation Mastery, Prophetic Surge or Final Revelation.

## class-engine:oracle:24

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `24`. SHA256 `934410e19787996445cac6ff90efc57048a74242085904287e661cbdb8dd538a`.

Application components: None applied directly by this binding..

**effect:** All combat-triggered RC refunds, including Prophecy, damage riders and Curse Boons, share ONE recovered RC per round. Rest recovery, encounter-start floor and explicitly limited Final refills are separate. A free, copied or refunded use cannot recursively trigger another recovery. Apply this global cap even if an individual card says its recovery is separate.

## class-card:oracle:oracle.supplement.shared.oracle-s-curse

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.oracle-s-curse`. SHA256 `3015b66a32b769d7fa30d0f75388c59495f8edb7eafbbedf178344ebdd9e1801`.

Application components: None applied directly by this binding..

**name:** Oracle's Curse

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Choose once at Oracle 1

**effect:** Choose exactly one Curse from the ten Curse cards below. Its limitations apply immediately and cannot be removed by ordinary magic or rest. Its Boons unlock automatically at Oracle levels 3, 5, 10, 15 and 20.

**prerequisite:** Oracle 1

## class-card:oracle:oracle.supplement.shared.curse-manifestation

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.curse-manifestation`. SHA256 `702c5e9f9f9fcf0888833b580a499614bb0f1acb1cc3a548df40aad0f766083a`.

Application components: `oracle.curse-manifestation.self-state`.

**name:** Curse Manifestation

**activation:** Bonus Action

**cost:** 1 RC

**rangeAndTarget:** Self

**duration:** 3 rounds

**frequency:** 1/short rest

**effect:** Intensify your chosen Curse. For 3 rounds gain +1 on Revelation attack rolls and +1 to your Revelation save DC. For the same duration take -1 AC and -1 on your own saving throws. Any part of the selected Curse that can normally be voluntarily suppressed cannot be suppressed while Manifestation lasts.

**prerequisite:** Oracle 2 and a selected Curse

## class-card:oracle:oracle.supplement.shared.oracle-s-burden

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.oracle-s-burden`. SHA256 `58600e513393987a382f64e53a11dbbf7c82e705ff8afb6e40fe6645dc6f8c02`.

Application components: None applied directly by this binding..

**name:** Oracle's Burden

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 2

**effect:** Your selected Curse is recognized as an intrinsic Oracle class condition rather than an ordinary removable curse. Remove Curse, cleansing, resurrection and similar generic effects cannot remove or suspend it. Only a feature that explicitly names your Oracle Curse can suppress, transform or replace one of its effects.

**prerequisite:** Oracle 2

## class-card:oracle:oracle.supplement.shared.curse-boon-i

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.curse-boon-i`. SHA256 `73291ce88bb3aa8be84b5ee23f0b4fee69f091d9ce3f7bcfcfb2da75155cbf61`.

Application components: None applied directly by this binding..

**name:** Curse Boon I

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 3

**effect:** Unlock the Oracle 3 Boon printed in your selected Curse card. You gain no Boon from unselected Curses.

**prerequisite:** Oracle 3 and selected Curse

## class-card:oracle:oracle.supplement.shared.ability-score-improvement-oracle-4

Classification: **NONSTATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.ability-score-improvement-oracle-4`. SHA256 `3c645ff5b4b77b6e935aa4554ba765c64381b01ad6578578bbfa7fcd6a21d351`.

Application components: None applied directly by this binding..

**name:** Ability Score Improvement — Oracle 4

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic milestone

**effect:** Choose the campaign's normal Ability Score Improvement option or one eligible feat. This milestone is separate from Revelations, Mysteries and Curse Boons.

**prerequisite:** Oracle 4

## class-card:oracle:oracle.supplement.shared.curse-boon-ii

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.curse-boon-ii`. SHA256 `f0312dc06ac0361ae61253fc79370fdd009de2ca750723be4709e7ded885f1dc`.

Application components: None applied directly by this binding..

**name:** Curse Boon II

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 5

**effect:** Unlock the Oracle 5 Boon printed in your selected Curse card. The main registry also names a level-5 Mystery feature; that Mystery-specific feature is represented by its explicit Mystery card below and does not create an additional generic shared feature here.

**prerequisite:** Oracle 5 and selected Curse

## class-card:oracle:oracle.supplement.shared.curse-boon-iii

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.curse-boon-iii`. SHA256 `460c1864ce0396dcac7668f995d439a79801f7d53ab4078b02b2ea926925c12e`.

Application components: None applied directly by this binding..

**name:** Curse Boon III

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 10

**effect:** Unlock the Oracle 10 Boon printed in your selected Curse card.

**prerequisite:** Oracle 10 and selected Curse

## class-card:oracle:oracle.supplement.shared.curse-boon-iv

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.curse-boon-iv`. SHA256 `b16a453ee7653d8ff4b9e065cb633b8bd5be655a11dd5c4f22ebec652a4cd5aa`.

Application components: None applied directly by this binding..

**name:** Curse Boon IV

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 15

**effect:** Unlock the Oracle 15 Boon printed in your selected Curse card.

**prerequisite:** Oracle 15 and selected Curse

## class-card:oracle:oracle.supplement.shared.curse-boon-v

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shared.curse-boon-v`. SHA256 `13e92edae0db369b9d7f72c9a9c9ce44150b28b050710bb98b0b878d817133d8`.

Application components: None applied directly by this binding..

**name:** Curse Boon V

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic at Oracle 20

**effect:** Unlock the Oracle 20 Boon printed in your selected Curse card.

**prerequisite:** Oracle 20 and selected Curse

## class-card:oracle:oracle.supplement.spiral-touched.spiral-touched-boon-ii

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.spiral-touched.spiral-touched-boon-ii`. SHA256 `ace12ebc874b8d21d6debd23e6453a1387cdf5ddaa9192b37ff3e78373005e95`.

Application components: None applied directly by this binding..

**name:** Spiral-Touched — Boon II

**activation:** Passive; triggered additional Action

**cost:** 1 RC for Action

**rangeAndTarget:** Self, after another creature’s turn

**duration:** One additional Action

**frequency:** 1/encounter; global action cap

**effect:** resistance to explicitly time/aging damage and advantage on saves against aging/slow effects; once per encounter spend 1 RC after another creature finishes its turn to take one additional full Action immediately, subject to the global action cap.

**prerequisite:** Oracle 5; selected Curse:Spiral-Touched

## class-card:oracle:oracle.supplement.curse.soul-cracked

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.curse.soul-cracked`. SHA256 `aa9c4ae9f370c84be0378e15edb68faf017d4e9fabcd47d98a25beb0f7620506`.

Application components: None applied directly by this binding..

**name:** Soul-Cracked

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Chosen once at Oracle 1

**effect:** LIMITATIONS: divination that attempts to read your alignment, aura or intent returns inconsistent results unless it specifically overcomes Oracle curses. Once each encounter, before your first damaging Revelation resolves, roll d6: 1 fire, 2 cold, 3 lightning, 4 necrotic, 5 psychic, 6 radiant; that Revelation's damage becomes the rolled type. While subject to a geas, binding oath or magically enforced pact, the first time each turn you knowingly act against its terms you take S psychic damage.

**prerequisite:** Selected Curse: Soul-Cracked

## class-card:oracle:oracle.supplement.soul-cracked.soul-cracked-boon-v

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.soul-cracked.soul-cracked-boon-v`. SHA256 `d53b31de7d794605089f45ba335289017687fa2f8c52320f10e870ffc5076ae8`.

Application components: None applied directly by this binding..

**name:** Soul-Cracked — Boon V

**activation:** Action

**cost:** 0

**rangeAndTarget:** Self or willing ally within 15 feet; originator on same plane

**duration:** Instantaneous

**frequency:** 1/long rest

**effect:** 1/long rest as an Action end one curse, geas or possession on yourself or one willing ally within 15 feet if that effect is not explicitly artifact/plot-locked. If its originator is a creature on the same plane, it makes a Wisdom save, taking 3 S d6 psychic damage on failure or half on success.

**prerequisite:** Oracle 20; selected Curse:Soul-Cracked

## class-card:oracle:oracle.supplement.burning-blood.burning-blood-boon-i

Classification: **NONSTATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.burning-blood.burning-blood-boon-i`. SHA256 `9b4d064bab3ee56bee1cffd7d081cd7bf679f7e09ab11cdb01dd8acaad1b3292`.

Application components: None applied directly by this binding..

**name:** Burning Blood — Boon I

**activation:** Passive; triggered retaliation

**cost:** 0

**rangeAndTarget:** Self; melee attacker; enemies within 5 feet

**duration:** Permanent resistance; immediate damage

**frequency:** Retaliation and ignition rider once/round

**effect:** gain fire resistance. Once per round when a melee weapon attack deals damage to you, the attacker takes 1d4 fire damage. The first time each round your curse blood ignites, hostile creatures within 5 feet take 1 additional fire damage.

**prerequisite:** Oracle 3; selected Curse:Burning Blood

## class-card:oracle:oracle.supplement.burning-blood.burning-blood-boon-ii

Classification: **ALREADY**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.burning-blood.burning-blood-boon-ii`. SHA256 `9e9306cb7e2f210a1f9b8f0697bd7dbd63b7445d1dea5743d89e535cbcdbbd2e`.

Application components: None applied directly by this binding..

**name:** Burning Blood — Boon II

**activation:** Triggered before damaging Revelation

**cost:** 1 RC plus Revelation’s cost

**rangeAndTarget:** One Revelation damage roll

**duration:** Until Revelation resolves

**frequency:** Once per Revelation; no recursive riders

**effect:** before activating a damaging Revelation, spend 1 RC to ignite it. Add fire damage equal to half that Revelation's unmodified rolled damage dice total, rounded down, minimum 1; mundane extinguishing cannot remove ongoing fire riders from that use. Until the Revelation resolves, your curse blood ignition does not damage allies.

**prerequisite:** Oracle 5; selected Curse:Burning Blood

## class-card:oracle:oracle.supplement.curse.false-life

Classification: **BOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.curse.false-life`. SHA256 `2f09d387e8c4b85570bd79a1de08e4f54223e4cf1e020d66be6c0ce80a37c27d`.

Application components: None applied directly by this binding..

**name:** False Life

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Chosen once at Oracle 1

**effect:** LIMITATIONS: divination treats you as undead unless it specifically pierces Oracle curses. Before a healing spell from another creature restores HP to you, its caster may make Wisdom (Insight) against your Revelation save DC. On success healing works normally. On failure roll d2; on 1 the spell restores 0 HP to you but still expends its normal costs. Non-spell healing is unaffected. Social hesitation from life-focused clergy remains narrative unless the scene calls for an ordinary reaction check.

**prerequisite:** Selected Curse: False Life

## class-card:oracle:oracle.supplement.battle.mark-of-the-doomed

Classification: **ALREADY**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.battle.mark-of-the-doomed`. SHA256 `00102b732d31d4ea2b87c51d42ec125811e82bf970d24c6c24a1a3e36cb401d5`.

Application components: None applied directly by this binding..

**name:** Mark of the Doomed

**activation:** Bonus Action

**cost:** 1 RC

**rangeAndTarget:** One enemy you can see within 5 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains; one active mark at a time

**effect:** Mark the target. You and allies within 5 tiles gain +2 on attack rolls against it. The first critical hit against the marked creature during the mark deals +1d6 damage of the triggering attack's type. The marked creature cannot benefit from mundane concealment against you. Applying another Mark of the Doomed ends the previous mark.

**prerequisite:** Oracle 3; Mystery: Battle; selected Tier I Revelation

## class-card:oracle:oracle.supplement.bones.bone-whisper

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.bone-whisper`. SHA256 `9c6449386401097169ad50d02ee568e616d5b319d9ac3b5604a240fc1c4d82af`.

Application components: `core.incapacitated`, `oracle.bone-whisper.soft-fallback`.

**name:** Bone Whisper

**activation:** Action

**cost:** 1 RC for active suppression; corpse speech costs 0 RC

**rangeAndTarget:** One corpse touched; undead within 2 tiles for active effect

**duration:** Corpse conversation maximum 1 minute; suppression until end of your next turn

**frequency:** Corpse speech 1/corpse; active at will while RC remains

**effect:** You may ask a corpse up to three brief questions about events it personally perceived while alive; it answers from its own knowledge and cannot speculate. Separately, spend 1 RC as an Action; undead enemies within 2 tiles make Wisdom saves. On failure they would be Incapacitated until the end of your next turn, subject to the Oracle hard-control guard. On a later qualifying failure after the guard has been used, they instead lose Reactions and their Speed becomes 0 for that duration.

**prerequisite:** Oracle 3; Mystery: Bones; selected Tier I Revelation

## class-card:oracle:oracle.supplement.bones.ledger-s-memory

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.ledger-s-memory`. SHA256 `749c98cbd9fc797d2bd2dba91bf92eaf38df0e64c0e340bc4fd95717c490cec1`.

Application components: None applied directly by this binding..

**name:** Ledger's Memory

**activation:** Passive and Action

**cost:** 0 RC

**rangeAndTarget:** Self; one corpse touched

**duration:** Permanent; consultation instantaneous

**frequency:** Knowledge always; corpse reading 1/long rest

**effect:** Gain advantage on checks to identify undead, poison and disease. Once per long rest, touch one corpse and learn its identity if the Pale Ledger could reasonably know it, its approximate time of death and the direct physical or magical cause of death. This does not reveal the killer's identity unless the corpse or supernatural Ledger actually knows it.

**prerequisite:** Oracle 12; Mystery: Bones

## class-card:oracle:oracle.supplement.flame.wrathful-brand

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.flame.wrathful-brand`. SHA256 `ca22b7513003b2cd62230ab868aa357102d381871b66761712fa3e9599915dc0`.

Application components: `oracle.wrathful-brand`, `oracle.wrathful-brand.attack-penalty`.

**name:** Wrathful Brand

**activation:** Bonus Action

**cost:** 1 RC

**rangeAndTarget:** One enemy within 4 tiles

**duration:** Until end of your next regular turn

**frequency:** At will while RC remains; one Brand at a time

**effect:** Mark one enemy. The next damaging attack you hit it with before the Brand ends adds fire damage equal to half that attack's unmodified rolled base damage dice total, rounded down, minimum 1. If an ally damages the marked target before the Brand ends, that ally regains 1d6 HP once per Brand and the target makes a Wisdom save; on failure it has -1 on attack rolls until the end of its next turn.

**prerequisite:** Oracle 3; Mystery: Flame; selected Tier I Revelation

**Reviewed overlay:** Owner damage bonus needs actual positive pre-bonus attack damage. One shared ally-positive-damage entitlement for heal attempt+WIS save; no refund from prevented healing. Timed Brand can persist after riders spent. SUPERSESSION from healing conference: damage-event predicates require resolvedDamage>0 before tempHP, distinct from numeric actualDamageDealt=tempAbsorbed+actualHpDamage. Divine Judgment positive packet/numeric0 reflects minimum1 and consumes actual turn; fully prevented resolved0 does neither. See HEALING_DEATH_PLAYTEST.md; original costs/clocks/riders unchanged.

## class-card:oracle:oracle.supplement.flame.purging-flame

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.flame.purging-flame`. SHA256 `7494667c38b68d0b0ee3d514dee3b0e9abcd0794d83df4b593b5702d642487ee`.

Application components: `oracle.purging-flame.undead-attack-penalty`.

**name:** Purging Flame

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One creature you touch

**duration:** Instantaneous; attack penalty until end of undead target's next turn

**frequency:** At will while RC remains

**effect:** If the target is a living ally, it regains 1d8+M HP and may end Poisoned or immediately repeat one saving throw against a disease that normally permits saves. This removes no Wounds. If the target is undead, make a Revelation attack; on hit it takes 1d8+M fire damage and makes a Constitution save, suffering -1 on attack rolls until the end of its next turn on failure.

**prerequisite:** Oracle 3; Mystery: Flame; selected Tier I Revelation

## class-card:oracle:oracle.supplement.flame.zealot-s-renewal

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.flame.zealot-s-renewal`. SHA256 `c5be3b9f61b1d449a60c73c0d7441db0451cec2ddf56b73113e480ccb08aaf91`.

Application components: None applied directly by this binding..

**name:** Zealot's Renewal

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One living ally within 3 tiles; adjacent enemies

**duration:** Instantaneous; fire ward until start of your next turn

**frequency:** At will while RC remains

**effect:** The ally regains 2 S d8+M HP, then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it. It may end Poisoned or immediately repeat one disease save. Until the start of your next turn it reduces the first fire damage it takes by S. Hostile creatures adjacent to the healed ally take 1d4 fire damage once from scattering embers.

**prerequisite:** Oracle 6; Mystery: Flame; selected Tier II Revelation

## class-card:oracle:oracle.supplement.life.thorned-shelter

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.thorned-shelter`. SHA256 `f5eae57f57896210e6d0cee18d477d87d3e99e28f33be7cbf9e1dfdd92929dda`.

Application components: `oracle.thorned-shelter.buff`, `oracle.thorned-shelter.speed-zero`.

**name:** Thorned Shelter

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One living ally within 3 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** The target gains +2 AC and reduces the first damage it takes each round by S. Once per round when it receives HP healing from another finite effect, add 1 HP. The first melee attacker to damage it each round takes 1d4 piercing damage and must make a Strength save; on failure its Speed becomes 0 until the end of that current turn. This movement restriction is not a full-turn denial.

**prerequisite:** Oracle 3; Mystery: Life; selected Tier I Revelation

## class-card:oracle:oracle.supplement.life.garden-of-restoration

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.garden-of-restoration`. SHA256 `faaa0f647c20d847d84790b2a353bb9e9fcf3946f210c911e003d08474a7de93`.

Application components: `oracle.garden-of-restoration.undead-attack-penalty`, `oracle.garden-of-restoration.zone`.

**name:** Garden of Restoration

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** 4-tile-radius fixed zone centered within 5 tiles

**duration:** 3 rounds

**frequency:** At will while RC remains; one Garden at a time

**effect:** At the start of each living ally's turn in the Garden, it regains 1d6 HP, maximum three pulses per creature from this use, and gains +1 HP the next time another finite healing effect restores HP before its next turn. The first time each ally enters or starts in a given Garden, it may end Poisoned or immediately repeat one disease save. Undead starting in the Garden take 1d6 radiant damage and make a Wisdom save; on failure they take -1 on attack rolls until the end of that turn.

**prerequisite:** Oracle 6; Mystery: Life; selected Tier II Revelation

## class-card:oracle:oracle.supplement.life.bloom-oracle

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.bloom-oracle`. SHA256 `bf83d4b3c7854f8480f1665a98d3f73825cdb70d260d0e449d79d9d761d6b7d4`.

Application components: None applied directly by this binding..

**name:** Bloom Oracle

**activation:** Passive and Action

**cost:** 0 RC

**rangeAndTarget:** Self; one creature touched

**duration:** Permanent; diagnosis instantaneous after 1 minute

**frequency:** Skill benefit always; supernatural diagnosis 1/long rest

**effect:** Gain advantage on Medicine and Nature checks. Once per long rest, examine one willing creature for 1 minute and learn the broad nature of one disease, poison, curse-like affliction or bodily condition affecting it plus one plausible mundane, magical or quest-based countermeasure known to the Verdant Resonance. This identifies rather than automatically cures the condition.

**prerequisite:** Oracle 12; Mystery: Life

## class-card:oracle:oracle.supplement.life.life-revelation-mastery

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.life-revelation-mastery`. SHA256 `f231bdb47b3545daad32777e23dd58122092961abb95c826436a646ab5e62b44`.

Application components: None applied directly by this binding..

**name:** Life Revelation Mastery

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** One eligible known Life Revelation

**duration:** Permanent

**frequency:** Choose one upgrade at Oracle 15

**effect:** Choose one mastery for a Revelation you know. Enhanced Overflowing Light: maximum temporary HP from excess healing becomes 20. Enhanced Garden of Restoration: the first Garden pulse a creature receives may end both Poisoned and one disease that explicitly allows magical curing, rather than only one of those benefits. Enhanced Song of Mending: duration becomes 3 rounds and gains one additional 2d6 healing pulse at the start of your second later regular turn; each ally still receives only one 1-HP death prevention per use.

**prerequisite:** Oracle 15; Mystery: Life; Revelation Mastery

## class-card:oracle:oracle.supplement.shadow.marquis-s-glimpse

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.shadow.marquis-s-glimpse`. SHA256 `933829ee0beb71fa6d95b61c5f42e6f90bcd859006567a3fa0a074ae767534cb`.

Application components: `oracle.marquis-glimpse.hard-control`, `oracle.marquis-glimpse.soft-fallback`.

**name:** Marquis's Glimpse

**activation:** Bonus Action

**cost:** 0 RC

**rangeAndTarget:** Self; enemies within 4 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds, ranged attack rolls against you automatically miss unless the attacker is adjacent to you or has an effect explicitly ignoring supernatural concealment. Once on each of your turns when a psychic Revelation deals damage, add a second copy of its unmodified rolled damage dice to one target; this copied damage cannot trigger RC recovery, conditions or proc effects. At the start of each enemy's turn within 4 tiles it makes a Wisdom save; on failure it would lose its Action to nameless dread, subject to the Oracle hard-control guard. A creature already hard-denied by you this encounter instead loses its Reaction and has Speed 0 until end of that turn.

**prerequisite:** Oracle 20; Mystery: Shadow

## class-card:oracle:oracle.supplement.stars.guiding-bolt

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.stars.guiding-bolt`. SHA256 `ae5c5c10031cedd478c5fcadd9e0bb7be39483bb3aee55ad8f2f3b525c19600d`.

Application components: `oracle.guiding-bolt.enhanced-slow`, `oracle.guiding-bolt.star-mark`.

**name:** Guiding Bolt

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One enemy within 6 tiles

**duration:** Damage instantaneous; star-mark 2 rounds or until consumed

**frequency:** At will while RC remains

**effect:** Make a Revelation attack. On hit deal 2d6+M radiant damage and apply a star-mark for up to 2 rounds. The next ally other than you to make an attack against the marked target gains +2 on that attack roll. If it hits, add S radiant damage and consume the mark. A creature can carry only one of your star-marks at a time.

**prerequisite:** Oracle 3; Mystery: Stars; selected Tier I Revelation

**Reviewed overlay:** Two independent entitlements: next ally-other-than-owner attack+2 spends on roll; next qualifying ally hit addsS and ends mark, including after a prior miss. Paid reapplication resets both without stacking. Enhanced-slow component applies only if the relevant Stars Revelation Mastery enhancement is selected; no unmodified Guiding Bolt slow.

## class-card:oracle:oracle.supplement.stars.constellation-mark

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.stars.constellation-mark`. SHA256 `121e0706ad882b95a2bc1b81152cac4a3d979258275b12431ac902157fc7a7b1`.

Application components: `oracle.constellation-mark`.

**name:** Constellation Mark

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** Up to 2 enemies within 6 tiles

**duration:** 3 rounds

**frequency:** At will while RC remains

**effect:** Mark up to two enemies. Allies gain +2 on attack rolls against marked targets. The first critical hit each round against any one of your marked targets deals +1d6 radiant damage. A marked creature cannot benefit from mundane concealment against creatures that can perceive your starlight mark. Recasting ends your previous Constellation Marks.

**prerequisite:** Oracle 6; Mystery: Stars; selected Tier II Revelation

## class-card:oracle:oracle.supplement.stars.omen-reader

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.stars.omen-reader`. SHA256 `5c826ef4dd3165578d8ed69b473c9872d84e979a3cf4284ee4bfcac292fc13ea`.

Application components: `oracle.omen-reader.star-ash`.

**name:** Omen Reader

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** Self; one ally within 5 tiles; one enemy identified at initiative

**duration:** Encounter

**frequency:** Passive each encounter; imposed penalty 1/encounter

**effect:** When initiative is rolled, the Director identifies the visible hostile creature with the highest current attack bonus among creatures you can perceive. You and one ally within 5 tiles gain +2 AC against that creature's first attack each round. Once per encounter before that enemy rolls its first attack of a turn, impose -2 on the roll and mark it with star-ash until the end of its next turn; allies gain +1 on attacks against it while marked.

**prerequisite:** Oracle 6; Mystery: Stars; selected Tier II Revelation

## class-card:oracle:oracle.supplement.stars.concord-alignment

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.stars.concord-alignment`. SHA256 `39626f6a7ed4b6959aaa92296c1dba97f07ba74618b1d39d0cff4c64b2e12f63`.

Application components: `oracle.concord-alignment.aura`.

**name:** Concord Alignment

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** Allies within 5 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** For 2 rounds allies within 5 tiles gain +1 on attack rolls and advantage on saves against Charm and Fear. Once per turn when an ally within range fails an attack roll or saving throw, use your Reaction to let that ally reroll it and use the new result; only one reroll can be granted per round. During Alignment, Guiding Bolt and Constellation Mark ranges increase by 1 tile. No roll can be rerolled more than once by Oracle features.

**prerequisite:** Oracle 9; Mystery: Stars

## class-card:oracle:oracle.supplement.stars.stars-revelation-mastery

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.stars.stars-revelation-mastery`. SHA256 `b52012be3a73aff1ef2b55b708ff166e8028ec6a3e36ee694861122995654cc5`.

Application components: None applied directly by this binding..

Modifies/authorizes later application: `oracle.constellation-mark`, `oracle.guiding-bolt.enhanced-slow`, `oracle.guiding-bolt.star-mark`.

**name:** Stars Revelation Mastery

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** One eligible known Stars Revelation

**duration:** Permanent

**frequency:** Choose one upgrade at Oracle 15

**effect:** Choose one mastery for a Revelation you know. Enhanced Guiding Bolt: a creature hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Constellation Mark: may mark up to 3 enemies. Enhanced Concord Alignment: duration becomes 3 rounds and its reroll cadence remains once per round.

**prerequisite:** Oracle 15; Mystery: Stars; Revelation Mastery

**Reviewed overlay:** Passive mastery selection; only a later legal Guiding Bolt with the relevant enhancement selected applies the downstream slow. Other selected mastery upgrades retain exact source rules.

## class-card:oracle:oracle.supplement.time.rewind-wound

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.time.rewind-wound`. SHA256 `eb01bdc7533669a80e0862bf3130c342b3b8c9c3f4199f8925953086e6bc898c`.

Application components: None applied directly by this binding..

**name:** Rewind Wound

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** One living ally you touch

**duration:** Healing instantaneous; protection until start of your next turn

**frequency:** At will while RC remains; same damage event can be rewound once

**effect:** Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects.

**prerequisite:** Oracle 6; Mystery: Time; selected Tier II Revelation

## class-card:oracle:oracle.supplement.time.paradox-skin

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.time.paradox-skin`. SHA256 `a39f4a8ccbc0fdf63eb7a12ca7479dceea74f0084ff4e6953c3359c22149fdb3`.

Application components: None applied directly by this binding..

**name:** Paradox Skin

**activation:** Passive and Reaction

**cost:** 0 RC

**rangeAndTarget:** Self; one ally within 3 tiles for time-effect interception

**duration:** Permanent

**frequency:** Echo avoidance once per round; ally reroll 1/short rest

**effect:** Once per round when an attack would hit you, roll d10; on 1 the attack instead hits a temporal echo and misses. You have advantage on saves against magical aging, Slow and explicitly time-based control. Once per short rest when an ally within 3 tiles fails a save against an aging, Slow or explicitly time-based effect, use your Reaction to let it reroll with +2 and use the new result.

**prerequisite:** Oracle 6; Mystery: Time; selected Tier II Revelation

## class-engine:paladin:2

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `2`. SHA256 `a75d29d2ed079e1fcabb1a29c33f9dcd230db247285047ada790bc59b6e8e309`.

Application components: None applied directly by this binding..

**effect:** At 2 choose one Fighting Style: Defense +1 AC while armored; Dueling +2 damage to first one-handed melee hit on your own turn; Protection Reaction impose disadvantage on one attack against an adjacent ally when using a shield. At 3 Divine Health gives advantage on disease saves, not universal immunity. At 5 Extra Attack makes two attacks when taking the ordinary Attack Action; named attack techniques use their own counts. These three features reconcile preserved main-registry entries; other old level-table extras, including extra level 14 ASI and undefined free slot riders, are not stacked into this draft. ASI/feat at 4/8/12/16/19 follows general advancement once.

## class-card:paladin:paladin.base.lay-on-hands

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.base.lay-on-hands`. SHA256 `24341edafa2539d0d42b01f5821195c69dd1a3101cde176beb6809c4f4867673`.

Application components: None applied directly by this binding..

**name:** Lay on Hands

**activation:** Action

**cost:** Choose 1 or more Lay on Hands points, maximum L per Action

**rangeAndTarget:** One living creature touched

**duration:** Instant

**frequency:** While pool remains

**effect:** Restore 1 HP per point spent, maximum class level per activation. Alternatively spend 5 points to end Poisoned or allow one immediate save against an existing disease that permits saves; cannot erase special-quest diseases, Wounds or death. This is finite pool healing, no RP conversion.

## class-card:paladin:paladin.base.sacred-touch

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.base.sacred-touch`. SHA256 `81444695d2cf9e5c54afee5721c29da4344543618244dde801758dde43744ac0`.

Application components: None applied directly by this binding..

**name:** Sacred Touch

**activation:** Action

**cost:** 0 for stabilize; 1 RP for inspection

**rangeAndTarget:** One living creature touched

**duration:** Instant

**frequency:** At will with resources

**effect:** Stabilize a living Downed creature at 0 HP without healing; damage/ordinary rules can end stability. Alternatively pay 1 RP and examine 1 minute to learn whether one curse/disease affects it, without revealing origin or cure. No resurrection or free healing.

## class-card:paladin:paladin.supplement.divine-health

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.divine-health`. SHA256 `9cc0a4a5ebba7fc8504072e1ecbef0f1c0aed93a410409d12b9a192bee6b986e`.

Application components: None applied directly by this binding..

**name:** Divine Health

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Automatic

**effect:** Advantage on saving throws against disease; no automatic immunity or cure of existing disease.

**prerequisite:** See class engine and progression.

## class-card:paladin:paladin.supplement.oath-of-mercy.sanctify-ground

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-mercy.sanctify-ground`. SHA256 `b7dd4c51886cf28d428e23d61b977a3c76a8fd79a4216e29fe8d392ae736e116`.

Application components: None applied directly by this binding..

**name:** Sanctify Ground

**activation:** Action

**cost:** 7 RP to start; 1 RP maintenance after the first pulse

**rangeAndTarget:** 15-foot-radius fixed zone centered within 30 feet; up to 3 allies per pulse

**duration:** Concentration, maximum 3 pulses

**frequency:** At will while RP remains

**effect:** Resolve the first pulse on activation. On each of your next 2 regular turns you may pay 1 RP and a Bonus Action to produce another pulse. At each pulse choose up to 3 allies in the zone; each may end one of Frightened, Poisoned or Staggered, or immediately repeat one saving throw against a disease or finite-duration curse that normally allows a save. A creature receives at most one cleansing choice per pulse.

**prerequisite:** Paladin 13; Oath of Mercy

**Reviewed overlay:** Selecting Staggered ends ALL present classification.staggered records on selected creature, including suppressed records. One named cleansing choice per creature per pulse; no immunity against later applications.

## class-card:paladin:paladin.supplement.oath-of-vengeance.vengeful-smite

Classification: **ALREADY**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.vengeful-smite`. SHA256 `8e48f8eddb8ec64fb5855d44d57e497dc4aadc28059dcfeb16004b3ce540fc0b`.

Application components: `paladin.vengeance-mark.smite`.

**name:** Vengeful Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack

**duration:** Vengeance Mark until end of your next regular turn

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Choose radiant or necrotic when you Smite; the entire Smite packet uses that type. After damage, apply Vengeance Mark until the end of your next regular turn. If the creature was already marked by you when this Smite began, add S flat damage to the Smite once. Applying a new mark refreshes but never stacks it.

**prerequisite:** Paladin 3; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.aura-of-judgment

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.aura-of-judgment`. SHA256 `a6b14edcc111b986cf3520b8db4fc46f89986cccd0cca34707f0f96a43a82445`.

Application components: None applied directly by this binding..

**name:** Aura of Judgment

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 enemies in your Oath aura currently marked by you

**duration:** While conscious, marked and in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected marked enemies take -1 on saving throws and cannot Hide from you or benefit from mundane concealment against you. This does not reveal a creature behind total cover or defeat supernatural invisibility unless another feature does so.

**prerequisite:** Paladin 3; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.judgment-brand

Classification: **ALREADY**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.judgment-brand`. SHA256 `5d26e62f895602510e0ee90ef5c8e1b69d817e4849f2597938d377fe177eaee0`.

Application components: `paladin.vengeance-mark.judgment-brand`.

**name:** Judgment Brand

**activation:** Bonus Action

**cost:** 2 RP

**rangeAndTarget:** One creature you can see within 60 feet

**duration:** 3 rounds

**frequency:** 1/short rest

**effect:** Brand the target for 3 rounds. It counts as Vengeance-marked. Your melee attacks against it score critical hits on natural 19-20, but this does not widen further with another 19-20 feature. When you move directly toward the branded target, ignore nonmagical difficult terrain. Once per round when the branded target willingly moves away from you, you may move up to 10 feet toward it as a Reaction without provoking opportunity attacks.

**prerequisite:** Paladin 11; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.mark-of-retribution

Classification: **ALREADY**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.mark-of-retribution`. SHA256 `19630a366023de150d9062fc8f9b9e3cdd3cdc35e95e03de05fdef4a97ec0817`.

Application components: `paladin.vengeance-mark.retribution`.

**name:** Mark of Retribution

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One foe within 30 feet

**duration:** Until end of your next regular turn

**frequency:** At will while RP remains

**effect:** The target makes a Wisdom save. On failure it becomes Vengeance-marked. Your next Smite against it before the mark ends adds 1d8 damage of the Smite's chosen type. You have advantage on opportunity attacks against it while the mark persists.

**prerequisite:** Paladin 3; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.relentless-pursuit

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.relentless-pursuit`. SHA256 `f9e2e8a9f816ec742272f343db30e08689aec6e6200d2c33686a2490d094ebe5`.

Application components: None applied directly by this binding..

**name:** Relentless Pursuit

**activation:** Bonus Action

**cost:** 3 RP

**rangeAndTarget:** Self; one creature currently marked by you

**duration:** Concentration, maximum 3 rounds

**frequency:** At will while RP remains

**effect:** For up to 3 rounds, movement you take that directly reduces distance to the marked target ignores nonmagical difficult terrain and does not cost extra movement for climbing minor obstacles no higher than 5 feet. This does not grant teleportation, flight or movement through creatures or solid objects.

**prerequisite:** Paladin 5; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.sentence-of-doom

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.sentence-of-doom`. SHA256 `399c0bbc6433d24c7fe3f66dad1e319a8f6fac8e65c2a1ad36e31753c7d7b3cc`.

Application components: `paladin.sentence-of-doom.empowerment`.

**name:** Sentence of Doom

**activation:** Bonus Action

**cost:** 5 RP

**rangeAndTarget:** One creature currently marked by you within 30 feet

**duration:** Until end of your next regular turn or until consumed

**frequency:** At will while RP remains

**effect:** The next Smite you apply to the marked target before this spell ends treats every Smite damage die as its maximum value instead of rolling. Critical-hit doubling adds another maximized set of the same dice under ordinary critical rules. Sentence of Doom affects only one Smite and does not duplicate its damage packet.

**prerequisite:** Paladin 9; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.no-escape

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.no-escape`. SHA256 `295bd84ed4b35386fa5cd466c2a947bd7655379dea622ba133cc3cd8c9b3a904`.

Application components: None applied directly by this binding..

**name:** No Escape

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** Up to 3 creatures marked by you within 60 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** At will while RP remains

**effect:** While affected, a marked creature cannot voluntarily teleport, become invisible or enter extradimensional travel. If it willingly moves out of your Oath aura, opportunity attacks against it have advantage until the end of its next turn. This spell does not prevent ordinary movement, forced movement or planar effects explicitly stronger than the ward.

**prerequisite:** Paladin 13; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-vengeance.final-verdict

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-vengeance.final-verdict`. SHA256 `588a235ef97e9f2d39ca847326623ea090b05676da713f90f447f75361e5582d`.

Application components: `paladin.final-verdict.hp-prohibition`.

**name:** Final Verdict

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** One creature marked by you within 30 feet and at or below half maximum HP

**duration:** Instantaneous or empowerment until end of your next regular turn

**frequency:** At will while RP remains

**effect:** The marked target makes a Constitution save, taking 4 S d8 radiant damage on failure or half on success. On failure it also cannot regain HP until the end of its next turn. If that damage reduces it to 0 HP, use ordinary Downed/death rules; there is no percentage-HP execution. On success your next Smite against it before the end of your next turn uses maximum damage dice. This bounded damage replaces the source draft’s automatic reduction to 0 HP.

**prerequisite:** Paladin 17; Oath of Vengeance

## class-card:paladin:paladin.supplement.oath-of-dominion.binding-word

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-dominion.binding-word`. SHA256 `bce0da735db5d36bbfb216fa82df3f6ecb19f0155e96560478a6fe6a20c4182c`.

Application components: `core.restrained`, `paladin.binding-word.restraint`.

**name:** Binding Word

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One creature within 30 feet that can hear you

**duration:** Maximum 2 rounds

**frequency:** At will while RP remains

**effect:** The target makes a Charisma save. On failure it is Restrained until the end of its next turn. At the end of that turn it repeats the save; failure extends Restrained one final round, success ends it. A creature unable to hear the Word is unaffected.

**prerequisite:** Paladin 5; Oath of Dominion

## class-card:paladin:paladin.supplement.oath-of-flame.purifying-smite

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.purifying-smite`. SHA256 `214dd871c1ac3dfa66a8096592af0ede689de599134f3e155c89e19c6b097830`.

Application components: None applied directly by this binding..

**name:** Purifying Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack

**duration:** Instantaneous

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Choose fire or radiant when you Smite; the entire Smite packet uses that type. If the target is undead or a fiend, after damage choose one temporary magical buff, disease-like enhancement, curse-derived boon or other removable beneficial condition currently affecting it. If the effect is within ordinary dispelling scope, end it. This purge never removes innate creature traits, class engines or permanent statistics.

**prerequisite:** Paladin 3; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-flame.aura-of-purification

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.aura-of-purification`. SHA256 `154be5cdc2707838c726778a21a69ce414f8f99e2dcd62b8ea638b86765a9ce3`.

Application components: None applied directly by this binding..

**name:** Aura of Purification

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** A selected living ally has advantage on disease saving throws. A selected hostile undead creature takes S radiant damage at the start of its turn while still in the aura. This pulse occurs at most once per creature per round and cannot generate resource or damage-reflection loops.

**prerequisite:** Paladin 3; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-flame.holy-inferno

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.holy-inferno`. SHA256 `198c7c0c48fd7794a74c99917c3049cc19905125e67db9d8d9aea913439892c9`.

Application components: None applied directly by this binding..

**name:** Holy Inferno

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 creatures in your Oath aura

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** Choose each target as hostile or allied. A hostile target makes a Dexterity save, taking S d8 fire plus S d8 radiant damage on failure or half on success. An allied target takes no damage and may end one of Poisoned, Diseased if magically curable, or a finite curse that ordinary cleansing could remove. Holy Inferno is an Oath technique rather than an ordinary spell.

**prerequisite:** Paladin 11; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-flame.cleansing-brand

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.cleansing-brand`. SHA256 `5b47240c618d7a418212c14d8866004171f5eac274aa9eb67ea1ffe190896c4e`.

Application components: None applied directly by this binding..

**name:** Cleansing Brand

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One creature within 30 feet

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Make a spell attack using PB+Charisma. On hit deal 2d6 fire damage. On a natural 20, after damage you may end one curse affecting the target that an ordinary curse-removal effect of this tier could legally remove; if removing it would benefit a hostile target, you may decline. The critical cleansing removes no innate traits, Oath, class engine or artifact-level curse.

**prerequisite:** Paladin 3; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-flame.zealot-s-flame

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.zealot-s-flame`. SHA256 `ca2645fada39e6900080bb8479019012856dcdaf00908741d0297b464b9f7377`.

Application components: None applied directly by this binding..

**name:** Zealot's Flame

**activation:** Bonus Action

**cost:** 3 RP; optional 1 RP per aura pulse after the first

**rangeAndTarget:** Self; one wielded weapon; hostile undead in your aura

**duration:** Concentration; maximum three rounds

**frequency:** At will while RP remains

**effect:** Your chosen weapon deals +1d6 fire damage on the first hit you land each turn. The first time during this cast that you hit, you may end one disease affecting yourself if that disease permits magical cleansing. On activation choose up to three hostile undead in your aura; they take 1d6 radiant damage. At the start of each of your next two turns you may pay 1 RP to repeat this pulse against up to three current aura targets. Each target is affected once per round. If you decline upkeep, the aura pulses end; the weapon buff may continue for the remaining duration.

**prerequisite:** Paladin 5; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-flame.sanctified-immolation

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.sanctified-immolation`. SHA256 `820e391d39fb3c8b1fe5c187fcf5c9af665600c5aad8c358ffee225762a252d9`.

Application components: None applied directly by this binding..

**name:** Sanctified Immolation

**activation:** Bonus Action

**cost:** 7 RP

**rangeAndTarget:** Your next Smite or Holy Inferno before end of your next regular turn

**duration:** Until consumed or end of your next regular turn

**frequency:** At will while RP remains

**effect:** The empowered Smite or Holy Inferno ignores fire resistance, but not immunity. Against undead, add 1d6 radiant damage to one damage roll. If a creature damaged by the empowered effect is currently affected by a removable curse or disease, you may end one such condition on that creature after damage; this cannot remove innate traits, artifact curses or class features.

**prerequisite:** Paladin 13; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-flame.purifying-crown

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-flame.purifying-crown`. SHA256 `5d63fcc4c008fe4976ea7cdb23b06853edceed0dd5667fae74b7985793f16cc9`.

Application components: None applied directly by this binding..

**name:** Purifying Crown

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds, a selected allied creature is immune to Poisoned and ordinary disease. A selected hostile undead or fiend takes S d6 fire plus S d6 radiant damage at the start of its turn, at most once per round. When the Crown activates, restore one expended use of Holy Inferno, even if it was used since the last short rest. This restoration occurs once and cannot recurse.

**prerequisite:** Paladin 20; Oath of Flame

## class-card:paladin:paladin.supplement.oath-of-the-ancients.ancient-smite

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.ancient-smite`. SHA256 `539f25512b332e2353deb216a84346a00ca919c0f7e3dba8fdfddf89bca14b45`.

Application components: `paladin.ancients.root`.

**name:** Ancient Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack

**duration:** Root rider until end of target's next turn

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Choose force or radiant; the entire Smite packet uses that type. If the triggering weapon attack is a critical hit, the target makes a Strength save; fey and elementals have disadvantage. On failure its Speed becomes 0 until the end of its next turn. This rooting does not remove its Action or Reaction and therefore is not a full-turn denial.

**prerequisite:** Paladin 3; Oath of the Ancients

## class-card:paladin:paladin.supplement.oath-of-the-ancients.thorn-crown

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.thorn-crown`. SHA256 `fdae69088633aa52c7c8c0f4ac3870f2f6ae9660f18605317353981d442c74ea`.

Application components: None applied directly by this binding..

**name:** Thorn Crown

**activation:** Reaction

**cost:** 2 RP

**rangeAndTarget:** Creature that just imposed a condition on you within 60 feet

**duration:** Reflected condition maximum 1 round

**frequency:** 1/short rest

**effect:** Trigger after a hostile creature causes you to fail a save and gain a finite-duration condition. The source immediately makes the same type of saving throw against your Oath DC. On failure it suffers the same named condition until the end of its next turn, subject to the universal hard-denial guard. Your original condition is not removed unless another feature removes it. Thorn Crown cannot reflect damage, death, curses, Wounds, resource loss or permanent transformations.

**prerequisite:** Paladin 11; Oath of the Ancients

## class-card:paladin:paladin.supplement.oath-of-the-ancients.roots-of-memory

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.roots-of-memory`. SHA256 `b03e5bfe0a028816de205bb55c51c43e7b785d73a307bd4cc5e4850f6cb25b56`.

Application components: `core.restrained`, `paladin.roots-of-memory.restraint`.

**name:** Roots of Memory

**activation:** Reaction

**cost:** 2 RP

**rangeAndTarget:** Up to 3 enemies within 10 feet of a creature you just damaged with Smite

**duration:** Until end of each target's next turn

**frequency:** At will while RP remains; once per Smite

**effect:** Trigger after your Smite resolves. Each chosen target makes a Strength save. On failure it is Restrained until the end of its next turn. A fey, elemental or creature directly bound to an ancient magical site has disadvantage on this save. If at least one such creature fails, you learn one truthful broad fact about its origin category, such as native plane, elemental affinity, fey court or connection to the local ancient site.

**prerequisite:** Paladin 3; Oath of the Ancients

## class-card:paladin:paladin.supplement.oath-of-the-ancients.primordial-surge

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.primordial-surge`. SHA256 `14e26c2b4a4fbe85d2cdff1f84ac074955bf0280097a5717007f8af91a2fbe89`.

Application components: `paladin.ancients.root`.

**name:** Primordial Surge

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** Temporary HP until lost; root until end of target's next turn

**frequency:** At will while RP remains

**effect:** A selected ally gains temporary HP equal to 2 times your actual Charisma modifier, minimum 2. A selected hostile fey or elemental makes a Strength save; on failure roots bind it and its Speed becomes 0 until the end of its next turn. This root does not remove Actions or Reactions. You may mix allied and hostile targets but can select no more than 3 total creatures.

**prerequisite:** Paladin 17; Oath of the Ancients

## class-card:paladin:paladin.supplement.oath-of-the-ancients.primordial-crown

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.primordial-crown`. SHA256 `d8b4b6f2f19f2921aba127bc1c581b2d93005a35c0a6bb0f1be42c61442a00bd`.

Application components: `paladin.ancients.root`, `paladin.primordial-crown.attack-target-restriction`.

**name:** Primordial Crown

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Self and up to 3 chosen creatures in your Oath aura

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds Thorn Crown can trigger once per round without consuming its short-rest use or paying RP. When your Ancients Smite critical-hit root successfully affects a creature, choose one adjacent hostile creature; it makes the same Strength save and becomes rooted on failure, at most one spread target per critical. A selected allied target has advantage on saves against Charmed. A selected hostile fey or elemental makes a Wisdom save at the start of each turn; on failure it cannot attack allies other than you until the start of its next turn, though it may take other actions. The same creature remains subject to the universal denial cap.

**prerequisite:** Paladin 20; Oath of the Ancients

## class-card:paladin:paladin.supplement.oath-of-the-chain.linked-ward

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.linked-ward`. SHA256 `e733a4a1f12c01e46fa3b2bd23f1f24f319fbb98dd023f68575687a51eb8fba2`.

Application components: `paladin.linked-ward.link`.

**name:** Linked Ward

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One willing ally in your Oath aura

**duration:** Concentration, maximum 3 rounds

**frequency:** At will while RP remains

**effect:** Mark one willing ally. Once per round when it takes damage, use your Reaction to redirect up to 2 times your actual Charisma modifier, minimum 2, of that damage to yourself. Redirected damage keeps its type and cannot be redirected again. If this redirected damage reduces you to 0 HP, the ally gains temporary HP equal to the amount you actually absorbed, maximum Paladin level+M.

**prerequisite:** Paladin 3; Oath of the Chain

## class-card:paladin:paladin.supplement.oath-of-the-chain.chain-of-duty

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-chain.chain-of-duty`. SHA256 `98689aca46585afeb54021721adc7ca7afebe7efb88da76926ab7dfd3e986563`.

Application components: `paladin.chain-of-duty.link`.

**name:** Chain of Duty

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One willing ally within 30 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** At will while RP remains

**effect:** Mark the ally. If it is reduced to 0 HP while within 60 feet and on the same plane, you may use your Reaction to teleport to an unoccupied space adjacent to it. This teleport prevents no damage and does not heal either creature. The spell then ends.

**prerequisite:** Paladin 5; Oath of the Chain

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash`. SHA256 `a4c627de2157a8064d5fa971c547926d1383c60ae4412a14f4be65bdd9d5c766`.

Application components: `paladin.iron-leash.action-denial`, `paladin.iron-leash.reaction-denial`, `paladin.iron-leash.speed-zero`.

**name:** Iron Leash

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** Until end of each target's next turn

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Strength save. On failure its Speed becomes 0 and it loses its Reaction until the end of its next turn. If a target has not previously suffered a full-turn denial from you this encounter, you may choose one failing target to also lose its Action, invoking the shared hard-denial limit. You gain no stolen Action yourself.

**prerequisite:** Paladin 11; Oathbreaker — Oath of the Chain

## class-card:paladin:paladin.supplement.oath-of-grief.mourning-smite

Classification: **ALREADY**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-grief.mourning-smite`. SHA256 `05803255b710498629d804da838b3730a006ac0be46bea1371391996d98fa00a`.

Application components: `paladin.grief-mark`.

**name:** Mourning Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack

**duration:** Grief Mark until end of target's next turn

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Choose radiant or necrotic; the entire Smite packet uses that type. If the target personally reduced one of your allies to 0 HP earlier this encounter, add 1d8 damage of the chosen Smite type. Such a target also gains Grief Mark until the end of its next turn, taking -1 on attack rolls. The mark refreshes but does not stack.

**prerequisite:** Paladin 3; Oath of Grief

## class-card:paladin:paladin.supplement.oath-of-grief.sorrow-s-weight

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-grief.sorrow-s-weight`. SHA256 `f885d58ff99881b466b9525d8a183972887f48ee6ec414125643be788d9ddb39`.

Application components: `paladin.sorrows-weight.slow`.

**name:** Sorrow's Weight

**activation:** Action

**cost:** 7 RP to start; 1 RP maintenance after first pulse

**rangeAndTarget:** 20-foot-radius fixed zone centered within 30 feet; up to 3 enemies per pulse

**duration:** Concentration, maximum 3 pulses

**frequency:** At will while RP remains

**effect:** Resolve one pulse on activation, then up to two later pulses by paying 1 RP and a Bonus Action on successive turns. At each pulse choose up to 3 enemies in the zone. Living targets make Constitution saves, taking 2d6 necrotic damage and having Speed halved until the start of your next regular turn or spell end, whichever occurs first on failure, or half damage with no slow on success. Undead automatically count as failing the initial save but still make a save on later pulses, preventing passive denial locks.

**prerequisite:** Paladin 13; Oath of Grief

## class-card:paladin:paladin.supplement.oath-of-chains-broken.liberating-smite

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.liberating-smite`. SHA256 `5361fc3912db698ad29c9e7fd73a7671d8c0cfaddc6744edb50598e6a6619cc8`.

Application components: None applied directly by this binding..

**name:** Liberating Smite

**activation:** Triggered

**cost:** Use normal Divine Smite cost: 1 RP for S d6 or 2 RP for (S+1)d8

**rangeAndTarget:** Creature hit by your melee weapon attack

**duration:** Instantaneous; freedom until end of target's next turn

**frequency:** One paid Smite total per round, shared with all normal and reactive Smite uses; any redirection uses its shared allowance

**effect:** Choose force or radiant; the entire Smite packet uses that type. If the target is currently grappling or restraining another creature, one grapple or restraint it is maintaining ends after damage. If the target itself is Grappled or Restrained, those conditions are suppressed until the end of its next turn, after which a still-valid source may resume them. Against a Director-identified oppressor actively enforcing captivity or coercion in the scene, add S flat damage once.

**prerequisite:** Paladin 3; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.aura-of-liberation

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.aura-of-liberation`. SHA256 `62b39223bc7825ba7b80a3faef9793dc1bfe624c06a947544a981e6e252d0593`.

Application components: None applied directly by this binding..

**name:** Aura of Liberation

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen allies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected allies gain +1 on saves or checks made to avoid or escape Grappled or Restrained. Once on each selected ally's turn, it may use a Bonus Action to repeat one legal escape check against a grapple or restraint currently affecting it. This grants no automatic success.

**prerequisite:** Paladin 3; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.righteous-quake

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.righteous-quake`. SHA256 `359d779c646280326f98112aaa3d83e08d970147b80743d304e5403c4bf1e67c`.

Application components: None applied directly by this binding..

**name:** Righteous Quake

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 creatures in a 15-foot burst centered on you; allies in burst

**duration:** Instantaneous

**frequency:** 1/short rest

**effect:** End one ordinary Grappled or Restrained effect on each willing ally in the burst. Enemies in the burst make Strength saves, taking 2 S d6 force damage and being pushed 10 feet on failure, or half damage with no push on success. A magical restraint on an ally is suppressed until the end of your next turn unless another spell explicitly dispels it.

**prerequisite:** Paladin 11; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.break-bonds

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.break-bonds`. SHA256 `d70cd3e693e0031a9b81e8dd591177e524b989ff4cada3f832f139fe71a9b640`.

Application components: None applied directly by this binding..

**name:** Break Bonds

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** One willing ally within 30 feet

**duration:** Instantaneous; movement/escape benefit until end of next turn

**frequency:** At will while RP remains

**effect:** End one non-artifact Grappled or Restrained condition affecting the ally if its source permits magical release. If the restraint was magical, the ally also gains +10 feet Speed and advantage on its next check or save to escape another grapple/restraint before the end of its next turn. This does not dispel unrelated spell effects.

**prerequisite:** Paladin 3; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.shatter-shackles

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.shatter-shackles`. SHA256 `04313916c07073c5cf4c316622c46b0aa8e5024287a1f7a9611091c487054625`.

Application components: None applied directly by this binding..

**name:** Shatter Shackles

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** 15-foot-radius burst centered within 30 feet; up to 3 allies

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Choose up to 3 allies in the area. End each mundane Grappled or Restrained condition affecting them. For a magical restraint or binding effect of rank 3 or lower, end it automatically. For rank 4 or higher, make a Charisma check adding proficiency against DC 10+spell rank; success ends that restraint. Artifact or plot-locked bindings are unaffected unless explicitly susceptible.

**prerequisite:** Paladin 9; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.revolution-s-cry

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.revolution-s-cry`. SHA256 `a1f6ce00a6de816607df55d8cf2a092a3e0b5f72135dd33ec6aad72d2ec055d2`.

Application components: None applied directly by this binding..

**name:** Revolution's Cry

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** Up to 3 allies or Director-identified oppressors in your Oath aura

**duration:** 3 rounds

**frequency:** At will while RP remains

**effect:** Selected allies gain +10 feet Speed and advantage on saves/checks against Grappled and Restrained for 3 rounds. When a selected hostile oppressor starts its turn in the aura, it makes a Wisdom save; on failure it loses its Reaction until the end of that turn. Save again each round; no full Action denial occurs.

**prerequisite:** Paladin 13; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.unbound-host

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.unbound-host`. SHA256 `c5e145e914af7deb1f317e78058044b0f8ddf3e633056de173d6b2fc3d5344ee`.

Application components: None applied directly by this binding..

**name:** Unbound Host

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** Up to 3 chosen allies in your Oath aura

**duration:** Concentration, maximum 1 minute

**frequency:** At will while RP remains

**effect:** Selected allies cannot become Grappled or Restrained by non-artifact effects and are immune to magical effects whose sole function is binding them in place. Whenever an affected ally ends an existing grapple or restraint as the spell begins or later breaks free from one resumed after suppression, it gains +10 feet Speed until the end of its next turn.

**prerequisite:** Paladin 17; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oath-of-chains-broken.liberty-unbound

Classification: **HOOK**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-chains-broken.liberty-unbound`. SHA256 `c4bb9eb69a39b6781bf4c56c82460c08223734241dea3234327e665d4b02d62c`.

Application components: None applied directly by this binding..

**name:** Liberty Unbound

**activation:** Bonus Action

**cost:** 0 RP

**rangeAndTarget:** Allies in your Oath aura; up to 3 hostile oppressors in the aura

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** Immediately end eligible magical Grappled or Restrained effects on allies in your aura as though by Shatter Shackles. For 3 rounds allies there gain +10 feet Speed and immunity to Grappled. Chosen hostile oppressors make Strength saves on activation; on failure they are pushed 10 feet and lose Reactions until the end of their next turn. No creature loses a full Action from this Final.

**prerequisite:** Paladin 20; Oath of Chains Broken

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes-aura

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes-aura`. SHA256 `de109b3954cb25bd955bf21cc2d2056bf275dcef91cbf213e91c911e0d5846f2`.

Application components: `paladin.reign-of-ashes-aura.buff-suppression`, `paladin.reign-of-ashes-aura.slow`.

**name:** Reign of Ashes Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen enemies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** Selected enemies cannot benefit from newly applied temporary buffs that grant movement increases, advantage on escape checks or immunity to Grappled/Restrained while in the aura. Their Speed is also reduced by 5 feet. Existing unrelated buffs are unaffected and immunity from innate traits is never suppressed.

**prerequisite:** Paladin 3; Oathbreaker — Oath of Chains Broken

## class-engine:ranger:0

Classification: **STATE**. Source: `data/public/class_playtests/ranger.json` / `0`. SHA256 `0b61ea32e9c31ce8f84395a1685dd94907f3c128cd884bea4031a0aab3440ea1`.

Application components: `ranger.track-target.quarry`.

**effect:** Dexterity governs weapons; Wisdom governs primal technique DC/M. This draft uses the detailed book's d8 Hit Die; older runtime d10 remains preserved as a conflicting alternative. At 1 gain Track Target engine: Bonus Action mark one perceived enemy within 90 ft for 1 minute, no RP, one quarry at a time; new mark replaces old. Once/own turn a weapon hit against quarry adds S damage. Mark does not reveal creatures through total cover. Track Target selection is an upgrade, not a second unlock tax.

## class-engine:ranger:4

Classification: **STATE**. Source: `data/public/class_playtests/ranger.json` / `4`. SHA256 `a9162609f7a50961d25c9ac121dbfda0c81d5b533d670c747c7bbe25a4b711e1`.

Application components: `ranger.emberroot.burn`, `ranger.glacial-thorn.speed-zero`, `ranger.venomlash.damage-penalty`.

**effect:** All Rangers learn five bounded Arrows at 11. Emberroot requires the previous 3 successful weapon hits carried fire imbue: ranged attack, weapon+S d6 fire on hit; up to 2 others within 5 ft take S fire, and primary target Burns 1d4 next turn. Glacial Thorn requires 2 ranged+1 melee among those 3 hits: ranged attack weapon+S d6 cold; on hit STR save or Speed 0 until end next turn. Venomlash requires poisoned/blighted terrain at you or target: ranged attack weapon+S d6 poison; on hit CON save or-1 damage on its next attack. Spirit Fang requires quarry: ranged attack at advantage, weapon+S d6 force; ignores resistance but not immunity on the added force only. Cleansing Grove requires natural terrain at you or target: up to 3 living allies within 10 ft of a point within 60 ft each end Frightened or Poisoned; no attack or damage.

## class-card:ranger:ranger.base.track-target

Classification: **HOOK**. Source: `data/public/class_playtests/ranger.json` / `ranger.base.track-target`. SHA256 `ea15f93cfa5fad82f76cd297fde5109d1ce06e03542ede6f6402ef2694720b35`.

Application components: None applied directly by this binding..

**name:** Track Target

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your quarry

**duration:** While marked

**frequency:** Continuous

**effect:** You have advantage on Survival checks to follow its physical tracks for 1 hour after the mark ends. While it is marked, once/turn your first hit also ignores 2 points of nonmagical flat damage reduction. Does not pierce immunity or reveal through cover.

## class-card:ranger:ranger.arch.pathfinder-s-mark

Classification: **STATE**. Source: `data/public/class_playtests/ranger.json` / `ranger.arch.pathfinder-s-mark`. SHA256 `d3f68f04f123734780644f16d55330bf9f5afc8290e54986fbb5e4d2f349c186`.

Application components: `ranger.pathfinders-mark.location`.

**name:** Pathfinder's Mark

**activation:** Action

**cost:** 1 RP

**rangeAndTarget:** One fixed visible point within 30 ft

**duration:** 24 hours

**frequency:** One location mark

**effect:** Know direction and rough distance to the point within 10 miles on same plane. A new mark replaces old. It does not create teleportation, observe occupants or reveal a path through barriers.

## class-card:ranger:ranger.arch.predator-s-mark

Classification: **STATE**. Source: `data/public/class_playtests/ranger.json` / `ranger.arch.predator-s-mark`. SHA256 `f4da81cfbdb2ac7d8a2015b16210cd38de0eeff2860419d548a8cb4534d4c7ec`.

Application components: `ranger.predators-mark.upgrade`.

**name:** Predator's Mark

**activation:** Bonus Action

**cost:** 2 RP

**rangeAndTarget:** Your quarry within 90 ft

**duration:** 1 minute

**frequency:** Recharge 3

**effect:** Upgrade current mark: first direct weapon hit per turn adds 1d6 rather than the engine's flat S; choose the higher, not both. Know quarry direction while within 90 ft unless blocked by total cover. Requires concentration; ordinary mark remains if this upgrade ends.

## class-card:ranger:ranger.hero.warder.rootcall-quake

Classification: **STATE**. Source: `data/public/class_playtests/ranger.json` / `ranger.hero.warder.rootcall-quake`. SHA256 `267eb3c1e77e4b3120bd91bae46602fead72146e60f527faefd8061a85e30e04`.

Application components: `ranger.rootcall-quake.speed-zero`.

**name:** Rootcall Quake

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Up to 3 enemies in 10 ft-radius ground area within 60 ft

**duration:** Concentration, 3 of your turns

**frequency:** Recharge 3

**effect:** STR save or Speed 0. Each affected target repeats save at end of each turn and may use Action to attempt escape using STR(Athletics) against class DC. Flying creatures not touching ground are unaffected.

## class-card:ranger:ranger.hero.outrider.toxic-affinity

Classification: **HOOK**. Source: `data/public/class_playtests/ranger.json` / `ranger.hero.outrider.toxic-affinity`. SHA256 `ac530cbdc50c397925bcb85d5fab05523b45219ba18af68f37347a9cfdfabc89`.

Application components: None applied directly by this binding..

**name:** Toxic Affinity

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** While known

**frequency:** Continuous

**effect:** Immune to Poisoned and nonmagical disease; gain poison resistance. This deliberately replaces blanket immunity to every poison/disease source. Existing magical diseases require their own treatment.

## class-card:ranger:ranger.hero.outrider.venom-rain

Classification: **APPLY**. Source: `data/public/class_playtests/ranger.json` / `ranger.hero.outrider.venom-rain`. SHA256 `cb98daebe005e16e45f86461803e2e52fe4d012a86e8ccd36fadb68dc470413e`.

Application components: `core.poisoned`.

**name:** Venom Rain

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** Up to 3 enemies in 10 ft-radius area within 60 ft

**duration:** Instant; Poisoned until end next turn

**frequency:** Recharge 3

**effect:** CON save: S d8 poison, half on success; failure Poisoned until end next turn. No permanent Corruption gain, contagious disease or poison harvesting. This is a paid technique and does not build Hit Chain.

## class-card:ranger:ranger.hero.outrider.plague-bearer

Classification: **APPLY**. Source: `data/public/class_playtests/ranger.json` / `ranger.hero.outrider.plague-bearer`. SHA256 `6317ff9342ad1b414daeb16c84574895b3f15c658872648c0557b4762c45fdb2`.

Application components: `core.poisoned`.

**name:** Plague Bearer

**activation:** Bonus Action

**cost:** 5 RP; 1 long-rest use

**rangeAndTarget:** Self; direct weapon targets

**duration:** Concentration, 3 of your turns

**frequency:** 1/long rest

**effect:** Your first weapon hit each turn adds 1d6 poison; target CON save or Poisoned until end next turn. You lose M real HP on activation, cannot fall below 1. The controlled effect is not a transmissible permanent disease and creates no free toxins.

## class-engine:shaman:1

Classification: **STATE**. Source: `data/public/class_playtests/shaman.json` / `1`. SHA256 `2a2a89b4f440277a59743d2dc2936f2a625be9557882f5796fa8fb71d4b76d80`.

Application components: `shaman.flame-totem.burn`, `shaman.frost-totem.slow`.

**effect:** Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack.

**Reviewed overlay:** Frost slow current triggering actual turn end; no turn underway6sec. Printed entry/start and once/creature/round caps unchanged.

## class-engine:shaman:4

Classification: **STATE**. Source: `data/public/class_playtests/shaman.json` / `4`. SHA256 `45e8077b1ba921b793f0eb5f15592c8210b900c564edb6da35be433b37897a74`.

Application components: `core.stunned`, `shaman.flask.burn`, `shaman.flask.reaction-denial`, `shaman.flask.root`, `shaman.flask.weaken`.

**effect:** Flask tier uses S. Mundane Base modes: Burn=one enemy 30 ft DEX save S d6 fire half, failure 1d4 fire next turn; Root=one ground enemy 30 ft STR save Speed 0 until end its next turn; Weaken=one enemy 30 ft CON save or-1 attack damage until end its next turn. Advanced Hero modes additionally: Stun=one enemy 30 ft CON save or no Reactions, failure by 10 Stunned until end its next turn; Heal=one living ally 30 ft S d6+M HP; Restore=end Frightened or Poisoned on one ally 30 ft. Every thrown flask consumes one prepared unit and 2 RP for advanced magic (Base mundane flasks cost 0 RP). Changing payload requires no separate crafting action when throwing. No flask leaves harvestable poison or another flask.

## class-card:shaman:shaman.base.flask-use

Classification: **BOOK**. Source: `data/public/class_playtests/shaman.json` / `shaman.base.flask-use`. SHA256 `60530b37dcad22ac1ee2f203d6068f3c44c40b82ec72603e6c6f92496eed5bfb`.

Application components: None applied directly by this binding..

Reader/bookkeeping references: `shaman.flask.burn`, `shaman.flask.root`, `shaman.flask.weaken`.

**name:** Flask Use

**activation:** Action

**cost:** 1 prepared mundane flask

**rangeAndTarget:** One target within 30 ft

**duration:** Payload-specific

**frequency:** Prepared 2/3/4 at 1/5/11 per long rest

**effect:** Throw a Burn, Root or Weaken flask using the exact engine profile. At Hero 10 Theurgist/Soothsayer may instead throw an advanced mode as Bonus Action for 2 RP and a prepared flask. Bloodcaller does not gain that upgrade.

**Reviewed overlay:** BOOK wrapper references all three Base profiles. Actual application is source engine[4] selected mode, never duplicate wrapper+engine states.

## class-card:shaman:shaman.arch.enhanced-elemental-attunement

Classification: **HOOK**. Source: `data/public/class_playtests/shaman.json` / `shaman.arch.enhanced-elemental-attunement`. SHA256 `0f7463dafd05d59724bd3ce6d9361819f96b5c99697e94a455f9a14705a39b95`.

Application components: None applied directly by this binding..

Modifies/authorizes later application: `shaman.elemental-affinity.ice-slow`.

**name:** Enhanced Elemental Attunement

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your affinity techniques

**duration:** While known

**frequency:** Once/turn

**effect:** Fire adds 1 to first fire damage roll; Ice's slow increases to 10 ft; Air also gives+1 initiative; Earth adds+1 to CON concentration saves. These replace corresponding basic affinity quantities rather than duplicating them.

## class-card:shaman:shaman.hero.theurgist.summon-ice-wisp

Classification: **STATE**. Source: `data/public/class_playtests/shaman.json` / `shaman.hero.theurgist.summon-ice-wisp`. SHA256 `61bdd76cc7b08db81abaeb59e356d8a02a36c2492153824a7c47b05a8970baa7`.

Application components: `shaman.ice-wisp.speed-zero`.

**name:** Summon Ice Wisp

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** One spirit in empty space within 30 ft

**duration:** Concentration, 3 of your turns

**frequency:** Recharge 4

**effect:** Summon standard Ice Wisp with fly 30 ft. Commanded attack deals cold; on hit target STR save or Speed 0 until end its next turn. No whole-turn freezing, bonus independent spells or multiple companion attacks.

## class-engine:soldier:1

Classification: **STATE**. Source: `data/public/class_playtests/soldier.json` / `1`. SHA256 `6ff82608cef4523def5d2f3be83bd0c8c4e1d7e527c493f89872e11a198989a8`.

Application components: `soldier.overwatch.bleed`, `soldier.overwatch.snare`.

**effect:** Overwatch is an automatic Base engine at 1. Bonus Action designate a visible 15 ft square within weapon range until start next regular turn. Once during that interval, spend your Reaction when a perceived enemy enters, moves inside, attacks an ally from, or reveals itself inside the zone. Make one legal ranged attack with ammunition and line of fire, normally 1d8+DEX piercing. On hit choose Snare (Speed-10 ft until end next turn), Bleed (1d4 at start next turn), or Push 5 ft (STR save negates push). Concealment still applies. Only one Overwatch zone; no extra Reaction. The optional Overwatch card upgrades this engine. At 17 you may move 5 ft without opportunity attacks after its shot, once/round.

## class-card:soldier:soldier.arch.suppression-fire

Classification: **STATE**. Source: `data/public/class_playtests/soldier.json` / `soldier.arch.suppression-fire`. SHA256 `a4d07ed876df8bef5f2bf899d28be8fe49ee191b22f915a916a24189a16f49c1`.

Application components: `soldier.suppression-fire.slow`.

**name:** Suppression Fire

**activation:** Action

**cost:** Three ammunition

**rangeAndTarget:** 15 ft square within weapon range

**duration:** Until start next turn

**frequency:** Recharge 3

**effect:** Up to 3 perceived enemies in zone make DEX save. Failure: S d6 piercing and Speed-10 ft through end next turn; success half damage, no slow. Cannot shoot through full cover. No attack rolls or on-hit procs.

## class-card:soldier:soldier.arch.hold-the-line

Classification: **STATE**. Source: `data/public/class_playtests/soldier.json` / `soldier.arch.hold-the-line`. SHA256 `e0d996731d4911617d570bf3cd70a27e6865321e1d97f05a40633dfc5970b131`.

Application components: `soldier.hold-the-line.speed-zero`.

**name:** Hold the Line

**activation:** Reaction

**cost:** 1 short-rest use

**rangeAndTarget:** One enemy entering your melee reach

**duration:** Until end its turn

**frequency:** 1/short rest

**effect:** Make one melee weapon attack. On hit normal damage and STR save or Speed 0. This is soft movement control; teleportation and forced movement remain possible.

## class-card:soldier:soldier.hero.champion.guardian-s-rush

Classification: **NONSTATE**. Source: `data/public/class_playtests/soldier.json` / `soldier.hero.champion.guardian-s-rush`. SHA256 `6734bfb600cd8c8a36fd0cca17391425c06c6f40969e17e6f5eba6ba7e2226cf`.

Application components: None applied directly by this binding..

**name:** Guardian's Rush

**activation:** Reaction

**cost:** 1 short-rest use

**rangeAndTarget:** One ally within 15 ft hit by attack

**duration:** Immediate

**frequency:** 1/short rest

**effect:** Move up to 15 ft along open ground to adjacent ally without opportunity attacks; reduce that hit's damage by 2 S+M. Cannot act while restrained or incapacitated. Does not transfer target or negate unrelated riders.

## class-card:soldier:soldier.hero.champion.divine-lockdown

Classification: **STATE**. Source: `data/public/class_playtests/soldier.json` / `soldier.hero.champion.divine-lockdown`. SHA256 `c04e66591e6ea2cacd30ec6f5395cfe32bacd000fe3c0dc866650aeef3ea99ea`.

Application components: `soldier.divine-lockdown.reaction-denial`, `soldier.divine-lockdown.slow`, `soldier.divine-lockdown.speed-zero`.

**name:** Divine Lockdown

**activation:** Action

**cost:** 1 encounter use

**rangeAndTarget:** Up to 3 enemies within 15 ft

**duration:** Until end next target turn

**frequency:** 1/encounter

**effect:** STR save each; failure Speed 0 and cannot take Reactions. Success Speed-10 ft only. This is physical suppression; teleport remains possible. No damage or additional free attacks.

## class-card:soldier:soldier.hero.artillerist.net-bolt

Classification: **STATE**. Source: `data/public/class_playtests/soldier.json` / `soldier.hero.artillerist.net-bolt`. SHA256 `063410e5c79cfa76b62fa7b4d572cb0fb751bb858e7b4ab5e66c47b1d0fcadd3`.

Application components: `core.restrained`, `soldier.net-bolt.large-slow`, `soldier.net-bolt.restraint`.

**name:** Net Bolt

**activation:** Action

**cost:** One net cartridge; 1 encounter use

**rangeAndTarget:** One enemy within 30 ft

**duration:** Until escaped; at most 3 rounds

**frequency:** 1/encounter

**effect:** Ranged weapon attack; on hit S d4 bludgeoning and Restrained. Target or adjacent ally may use Action STR/Athletics against your DC to end, or destroy net AC 10 HP 5. Huge or larger targets instead lose 10 ft Speed. No automatic unsaveable imprisonment.

## class-card:soldier:soldier.hero.tyrant.marked-for-death

Classification: **STATE**. Source: `data/public/class_playtests/soldier.json` / `soldier.hero.tyrant.marked-for-death`. SHA256 `ff6565b8fa1afb6ca78485855651c12a7f8bc8bdc8652cd6dc16a5692d52e69f`.

Application components: `soldier.marked-for-death`.

**name:** Marked for Death

**activation:** Bonus Action

**cost:** 0

**rangeAndTarget:** One visible enemy within 60 ft

**duration:** Until start next turn

**frequency:** Recharge 2

**effect:** Mark foe. It takes-1 saves against your class effects and deals 1 less damage on its first hit against an ally other than you. One mark; penalty does not stack with Intimidating Presence.

## class-card:thief:thief.arch.crippling-strike

Classification: **STATE**. Source: `data/public/class_playtests/thief.json` / `thief.arch.crippling-strike`. SHA256 `fdcceacb1c8e63a7765e4c2fdfc6412bb57f7a2cdf830ff323d42e98f1851a6f`.

Application components: `thief.crippling-strike.slow`.

**name:** Crippling Strike

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One enemy hit by your Sneak Attack

**duration:** Until end next target turn

**frequency:** Once/own turn

**effect:** Target CON save; failure Speed halved. Does not stack multiple slow fractions or deny teleport. Explicit Arch minimum 15 retained.

## class-engine:tinker:3

Classification: **STATE**. Source: `data/public/class_playtests/tinker.json` / `3`. SHA256 `48ef29ba2043a595ab801397a269579864b2865bee7ef1b72353944421604669`.

Application components: `core.stunned`, `tinker.burn-injector.burn`, `tinker.poison-vents.attack-penalty`, `tinker.target-scanner.mark`, `tinker.target-taunter.attack-penalty`.

**effect:** At 5 automatically gain one module slot; change module during long rest. Offensive: Burn Injector first bolt hit/turn causes 1d4 fire next 2 target turns; Poison Vents d4=4 on hit CON save or-1 attack rolls until end next turn; Concussive Bolt d4=4 on hit CON save or Stunned until end next turn, once/target/encounter shared denial guard and 1/short-rest successful Stun. Defensive: Target Taunter command action once/encounter WIS save one foe 30 ft or disadvantage attacking others until end next turn; Energy Shield command gives adjacent ally+2 AC until start next turn; Smoke Cloud command once/encounter creates 5 ft radius opaque smoke centered drone until start next turn. Support: Ammo Dispenser adjacent allies first ranged hit/turn+1 damage; Target Scanner command mark 1 visible foe 60 ft first ally attack before start next turn+1 hit; Tether Grappler command once/encounter pulls 1 willing ally 15 ft within 30 ft without opportunity attacks along open route.

## class-engine:tinker:5

Classification: **STATE**. Source: `data/public/class_playtests/tinker.json` / `5`. SHA256 `b9ca3f83e895390256fad13f18df8d32b813c79017cc3d6c236a30444bd566b4`.

Application components: `tinker.cryo.speed-zero`, `tinker.glue.slow`, `tinker.overload-core.reaction-denial`, `tinker.shock.construct-reaction-denial`, `tinker.shock.verbal-block`.

**effect:** Advanced bomb profiles replace basic rider: Thermobaric fire pushes 5 ft on failed STR save after damage; Cryo cold on failed DEX also Speed 0 until end next turn and d2=2 ignores 1 flat DR against this bomb; Shock lightning CON instead DEX, failure prevents verbal spellcasting until end next turn (construct instead loses Reactions), shared hard-denial guard; Glue no damage, 15 ft square difficult terrain 3 rounds and entering/starting DEX save or Speed-15 ft until end turn, once per creature/round. Overload Core destroys one commanded drone within 30 ft as part Action bomb, DEX save 2d6 lightning and no Reactions until end next turn on failure, half damage on success. Consumes stock/allowance; no further destruction proc.

**Reviewed overlay:** Glue slow current triggering actual turn end, not invented next regular turn. No turn underway6sec. Other bomb components retain their own source clocks; Glue terrain lasts its independent3 rounds.

## class-engine:tinker:6

Classification: **STATE**. Source: `data/public/class_playtests/tinker.json` / `6`. SHA256 `84965457980b9a985ee4fa4022a0ad0f9b9977760f0e28b93342dc03d005a356`.

Application components: `core.restrained`, `tinker.decoy-dummy.attack-penalty`, `tinker.net-trap.restraint`.

**effect:** Deployable slots start 1 at 6, 2 at 13, 3 at 17, separate from drone cap. Deploy Action 2 RP within 15 ft, fixed ground, AC 12+PB HP 2 L, duration 3 rounds, concentration not required; destroyed do not refund fuel. All share command budget. Sentry and Net require their cards. Additional engine profiles unlocked 6: Rocket Tower commanded attack 60 ft target DEX save S d6 fire/half success to up to 2 creatures within 5 ft, maximum 3 shots; Decoy Dummy one foe 30 ft WIS save when deployed or disadvantage on next attack against others, destruction S fire to one adjacent enemy no chain; Blast Wall 10-by 5 ft blocks LOS and movement, climb cost 10 ft. Net Trap one enemy entry STR save or Restrained, end turn repeat/Action escape DC, 3 round max then ends. One only fires when commanded except nonattack trap/decoy trigger; command budget limits damaging triggers too.

## class-card:tinker:tinker.arch.bomb-specialization

Classification: **HOOK**. Source: `data/public/class_playtests/tinker.json` / `tinker.arch.bomb-specialization`. SHA256 `0ee337ec425093c282e11c0a7797356d10fade80c950b2be6a698722e811ce8c`.

Application components: None applied directly by this binding..

**name:** Bomb Specialization

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your bomb damage

**duration:** One target per throw

**frequency:** Once/turn

**effect:** Add M damage to one target that failed its initial save. No multiplying by area targets or damage ticks; Glue instead increases its slow by 5 ft maximum 20.

## class-card:tinker:tinker.arch.deploy-net-trap

Classification: **STATE**. Source: `data/public/class_playtests/tinker.json` / `tinker.arch.deploy-net-trap`. SHA256 `441a83ffad99028dd74608c352ea1e03fc65b118d636fcf0f6c474d652c7d28a`.

Application components: `core.restrained`, `tinker.net-trap.restraint`.

**name:** Deploy Net Trap

**activation:** Action

**cost:** 2 RP; one slot

**rangeAndTarget:** One 5 ft square within 15 ft

**duration:** 3 rounds or trigger

**frequency:** Recharge 2

**effect:** Deploy visible Net Trap. First enemy entry STR save or Restrained, repeat end turn or Action escape against DC. Target Huge+instead speed-10 ft. No damage or continued rearming; ends after one creature escapes.

## class-card:tinker:tinker.hero.warmachine.overpressure-bombs

Classification: **NONSTATE**. Source: `data/public/class_playtests/tinker.json` / `tinker.hero.warmachine.overpressure-bombs`. SHA256 `b9634b8bc7c8ae4b57130586ca427b5c2d7f8bb8c2a7505d1eb12511015a68f3`.

Application components: None applied directly by this binding..

**name:** Overpressure Bombs

**activation:** Triggered

**cost:** 1 RP

**rangeAndTarget:** One bomb throw

**duration:** Instant

**frequency:** Once/turn

**effect:** Add on failed initial save STR save or choose push 10 ftor Prone. Also add S damage to one failed-save target. No additional blast or compounded slow; do not stack with Thermobaric push.

## class-card:warrior:warrior.base.brutality-sense

Classification: **ALREADY**. Source: `data/public/class_playtests/warrior.json` / `warrior.base.brutality-sense`. SHA256 `1e9c30e1f682ae0ef2c634631e163656321ce1f52ce9666e01fa06e6e23b6193`.

Application components: `warrior.brutality-vulnerable`.

**name:** Brutality Sense

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Hostile creatures you can perceive within 60 feet

**duration:** While condition remains true

**frequency:** Always

**effect:** Brutality Sense. You know when a visible hostile creature is at or below one-quarter of its maximum HP; it is Vulnerable for your Warrior features that specifically reference a marked vulnerable target. This does not reveal its exact HP or hidden resistances.

## class-card:warrior:warrior.arch.brutality-momentum

Classification: **ALREADY**. Source: `data/public/class_playtests/warrior.json` / `warrior.arch.brutality-momentum`. SHA256 `4ff3b28f0910503638889962933a6677c614f1ce62c77a52dbe54134d183e8b2`.

Application components: `warrior.brutality-vulnerable`.

**name:** Brutality Momentum

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Your Brutal Strike

**duration:** Instantaneous

**frequency:** At most once per round

**effect:** Brutality Momentum. When you personally reduce a creature marked Vulnerable by Brutality Sense to 0 HP with a melee attack, set Brutal Strike's positive round-recharge counter to 0 if it has not already been reset or shortened this round. This restores no Action and cannot refresh a per-rest use. Trivial, summoned or friendly creatures cannot trigger it.

## class-card:warrior:warrior.hero.wardborn.stabilizing-injection

Classification: **HOOK**. Source: `data/public/class_playtests/warrior.json` / `warrior.hero.wardborn.stabilizing-injection`. SHA256 `b58508331c82ad5a7dad8bd3713029899b9a7c341c490220d997caf0e3aa71db`.

Application components: None applied directly by this binding..

**name:** Stabilizing Injection

**activation:** Action

**cost:** Consume 1 prepared serum dose

**rangeAndTarget:** One living creature you touch

**duration:** Instantaneous

**frequency:** At most once per target per long rest

**effect:** Stabilizing Injection. The target regains 2d8 + M HP and may end one of Poisoned, Frightened or Staggered. If Diseased, it may immediately repeat one saving throw the disease normally permits. This removes no Wounds, cannot restore the dead and does not activate a mutation or apply the consumed serum's normal profile.

## class-card:warrior:warrior.hero.ironskin.cellular-reconstruction

Classification: **ALREADY**. Source: `data/public/class_playtests/warrior.json` / `warrior.hero.ironskin.cellular-reconstruction`. SHA256 `e8bd145d4393467058e51509e15230c1bc315884f24f96ccfb509faa5186d56c`.

Application components: `warrior.cellular-reconstruction.stasis`.

**name:** Cellular Reconstruction

**activation:** Action

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until start of your next regular turn, then instantaneous recovery

**frequency:** 1/long rest

**effect:** Cellular Reconstruction. Enter stasis until the start of your next regular turn: your Speed becomes 0, you cannot take Actions, Bonus Actions or Reactions, and attacks against you have advantage. At the start of your next turn regain 3d8 + M HP and end Poisoned plus one mundane or magical disease that does not explicitly require a special cure. This removes no Wounds and cannot function while dead.

## class-card:warrior:warrior.hero.dreadspawn.infectious-mutation

Classification: **STATE**. Source: `data/public/class_playtests/warrior.json` / `warrior.hero.dreadspawn.infectious-mutation`. SHA256 `c2fc9dcc419388da637d79d4b8005eabddea2b34cca0fca32641a203dec7e02b`.

Application components: `warrior.infectious-mutation.roll-penalty`.

**name:** Infectious Mutation

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One creature hit by your weapon or natural attack

**duration:** Until end of target's next turn

**frequency:** At most once per turn

**effect:** Infectious Mutation. After you hit a creature, roll a d10. On a 10, painful temporary growths erupt: the target takes S psychic damage and has -1 on its next attack roll or saving throw before the end of its next turn, whichever occurs first. This is not a permanent mutation, disease or body alteration and cannot spread or reproduce.

## class-card:warrior:warrior.supplement.shoulder-spike-cluster

Classification: **HOOK**. Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.shoulder-spike-cluster`. SHA256 `4bd65746a241671b364a84b0fd3f0d66ec7485e6ade2b13b4a1f6f43414b9abc`.

Application components: None applied directly by this binding..

**name:** Shoulder Spike Cluster

**activation:** Triggered while active

**cost:** One mutation slot; serum activation

**rangeAndTarget:** Creature grappling you or grappled by you

**duration:** Instantaneous

**frequency:** Once per creature per round

**effect:** When a grapple is established or maintained against you, or you successfully establish a grapple, the other creature takes 1d6 piercing damage.

**prerequisite:** Warrior 1; Basic Combat

## class-engine:wizard:15

Classification: **BOOK**. Source: `data/public/class_playtests/wizard.json` / `15`. SHA256 `c2c4c1d25080e5c3fec28263df1d91aab669897ec699dfde9ee2346d4480ccc6`.

Application components: None applied directly by this binding..

**effect:** MATRIX MASTERY MODIFICATIONS. After acquiring Matrix Mastery, each prepared ordinary spell matrix may carry at most one modification chosen during preparation. QUICK SUBSTITUTION: once per short rest, replace one matrix marked Quick Substitution with another spellbook spell of exactly the same rank using a 1-minute ritual instead of the normal 10-minute midday swap; the replacement loses the modification until the next long rest. COMPONENT ENHANCEMENT: when casting a damaging or healing matrix, spend 1 additional RP to add one extra die of the spell's primary damage or healing die to one roll; if the spell has no such die this modification has no effect. MATRIX LINKING: pair two different prepared matrix families during preparation; after legally casting one, the other costs 1 less RP, minimum 1, if cast before the end of your next regular turn, at most once per pair per round. STABILITY REINFORCEMENT: gain +2 on concentration saves caused by damage while maintaining that matrix. A matrix modification never creates another spell cast or proc event.

## class-card:wizard:wizard.base.analyze-magic

Classification: **HOOK**. Source: `data/public/class_playtests/wizard.json` / `wizard.base.analyze-magic`. SHA256 `b22861d46aac71ad92b3cec729db3c03d2a1ef97ebe5aba9096cc5d8c04cd362`.

Application components: None applied directly by this binding..

**name:** Analyze Magic

**activation:** Action

**cost:** 1 RP

**rangeAndTarget:** One magical creature, object or effect within 30 feet

**duration:** Instantaneous

**frequency:** Recharge 1 round

**effect:** Analyze Magic. Tags: base, active, wizard-spell, divination, knowledge. Make an Intelligence (Arcana) check against DC 10 + the effect's spell rank, treating a non-spell effect's Director-assigned tier as rank. On success learn its school or magical category, one active mechanical property and whether it is currently sustained, cursed or bound to another effect. Failure reveals only that magic is present.

## class-card:wizard:wizard.arch.arcane-sight

Classification: **HOOK**. Source: `data/public/class_playtests/wizard.json` / `wizard.arch.arcane-sight`. SHA256 `5a2ed132c397f20afb928c0b8639f56a7137ee6c0e7b1124ecd3ad97365d35a7`.

Application components: None applied directly by this binding..

**name:** Arcane Sight

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Self; 60-foot sight

**duration:** Concentration, maximum 10 minutes

**frequency:** Recharge 2 rounds

**effect:** Arcane Sight. Tags: arch, active, wizard-spell, divination, concentration. While active you perceive magical auras within 60 feet and automatically know each visible aura's school or broad magical category. As an Action on a later turn, examine one aura to learn whether it is concentrated, summoned, cursed, warded or linked to another visible magical effect. Total cover blocks sight.

## class-card:wizard:wizard.hero.spellbinder.sigil-authority

Classification: **HOOK**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.spellbinder.sigil-authority`. SHA256 `36ed3ec717c5594ee5e1d492d4272754b49b3b3f5b22071f7f2b0d7523ab76b4`.

Application components: None applied directly by this binding..

**name:** Sigil Authority

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Permanent

**frequency:** Always

**effect:** Sigil Authority. Tags: hero, spellbinder, passive. Gain +1 on Counterspell and Dispel Magic ability checks. When a creature is Charmed, Frightened, Paralyzed, Restrained or Stunned by a source other than the spell you are currently casting, your Spellbinder spells that force it to save use a Wizard spell DC 2 higher. This increase never applies retroactively to the condition that enabled it.

## class-card:wizard:wizard.hero.spellbinder.runic-snare

Classification: **STATE**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.spellbinder.runic-snare`. SHA256 `dcb5a8d9218ad58a2aabef24157d086ca2cb1c9179a62b78e521a71f215aab3d`.

Application components: `core.restrained`, `wizard.runic-snare.restraint`.

**name:** Runic Snare

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One 10-foot square within 30 feet

**duration:** Until triggered or 1 minute

**frequency:** Recharge 3 rounds

**effect:** Runic Snare. Tags: hero, spellbinder, wizard-spell, glyph, control. Place a visible-to-you glyph. The first hostile creature entering the square makes a Dexterity save. Failure deals S d6 force damage, causes Restrained until the end of its next turn and makes it drop one non-attuned held item of its choice. Success takes half damage with no restraint or drop. A Restrained target may repeat a Strength save at the end of its turn.

## class-card:wizard:wizard.hero.necromancer.will-domination

Classification: **APPLY**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.will-domination`. SHA256 `468bd238ca1e004341fce21ce3a820393ce90d01b9e9470e0d6b03e616a1af4f`.

Application components: `core.stunned`, `wizard.will-domination.reaction-denial`.

**name:** Will Domination

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One creature that fails a save against your Wizard spell by 5 or more

**duration:** Until end of target's next turn

**frequency:** Once per target per encounter

**effect:** Will Domination. Tags: hero, necromancer, passive, control. When a creature's total on a saving throw against your Wizard spell is at least 5 below the DC, it is Stunned until the end of its next turn. After this successfully Stuns that creature once in the encounter, later qualifying failures instead remove its Reaction until the end of its next turn. This uses the shared source-character/target hard-denial mark across all your features, not a separate allowance per spell.

## class-card:wizard:wizard.hero.necromancer.binding-sigil

Classification: **STATE**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.binding-sigil`. SHA256 `9dd72d54cae678ded090d437d61a37b8f4c2da7437d53231d38aacde706fd156`.

Application components: `wizard.binding-sigil.mark`.

**name:** Binding Sigil

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** One creature directly affected by your Wizard spell

**duration:** Until end of your next regular turn

**frequency:** At most one marked creature at a time

**effect:** Binding Sigil. Tags: hero, necromancer, passive, mark. After one creature takes damage from or fails a save against your Wizard spell, you may mark it. Until the end of your next regular turn you have advantage on Wizard spell attacks against that creature. Marking another creature ends the previous mark. Echoes, companions and environmental damage cannot apply it.

## class-card:wizard:wizard.hero.necromancer.infernal-pact-quest-based-unlock

Classification: **STATE**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.infernal-pact-quest-based-unlock`. SHA256 `3ec78d206b84e52afbca7eefd488313b4aeb4371a3edb80e5f9e6e14636d053d`.

Application components: `wizard.gravebrand`.

**name:** Infernal Pact (Quest-based unlock)

**activation:** Bonus Action

**cost:** 3 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Maximum 3 rounds

**frequency:** 1/long rest; quest-gated

**effect:** Infernal Pact — Gravebrand. Tags: hero, necromancer, infernal, necrotic, dark-content. This card can be selected only after completing the campaign's Infernal Pact quest and its dark-trauma check-in. Mark one creature. At the start of each of its turns it makes a Constitution save; on failure it takes 1d6 necrotic damage and you regain HP equal to the actual damage dealt, maximum S+M; success ends Gravebrand. Gravebrand ignores necrotic resistance but not immunity. While you possess this Pact, Corpse Harvest and Auto-Raise may also treat Fiend corpses as eligible; other creature types remain ineligible.

## class-card:wizard:wizard.hero.necromancer.mental-binding

Classification: **STATE**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.mental-binding`. SHA256 `40aa26a57097f3d1611e5d21d2f7be7d9f66029454e293892076b2ce2fd560ae`.

Application components: `core.charmed`, `wizard.mental-binding.command`.

**name:** Mental Binding

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** Recharge 3 rounds

**effect:** Mental Binding. Tags: hero, necromancer, wizard-spell, enchantment, control, concentration. Target WIS save; failure becomes Charmed for at most 3 rounds, repeat save at end each turn and on damage. On its first affected turn only, choose Approach, Retreat, Drop, Kneel or Strike; target uses up to half Speed, one object interaction or one ordinary weapon attack as appropriate, consuming its normal Action only if an attack is made. This command replaces at most one normal Action/turn and uses the shared hard-denial mark. Later turns retain normal actions, but while Charmed it cannot willingly attack you. No self-harm, compelled beliefs, resource expenditure or permanent allegiance. The player chooses the safest legal interpretation for a PC.

## class-card:wizard:wizard.hero.necromancer.arcane-domination

Classification: **STATE**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.arcane-domination`. SHA256 `c41ce39b3433caf4527616c8daea043bb30055537c6c2313994a5fb0d2943ff7`.

Application components: `core.charmed`, `wizard.arcane-domination.command`, `wizard.arcane-domination.reaction-denial`.

**name:** Arcane Domination

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Concentration, up to 1 minute

**frequency:** 1/long rest

**effect:** Arcane Domination. Tags: hero, necromancer, wizard-spell, enchantment, control, concentration. Target WIS save; failure Charmed for 1 minute, repeat at end each turn and on damage. Once during this effect, spend Bonus Action to command its NEXT normal turn: Move up to Speed and either Dodge, Disengage or make one ordinary weapon attack, replacing its normal Action and using the shared hard-denial mark. It gains no extra turn or attack; later turns retain normal actions while Charmed, with no Reactions until effect ends. A PC chooses its legal attack target and reasonable route. No self-harm, forced spell/resource expenditure, belief change or permanent control.

## class-card:wizard:wizard.hero.necromancer.mind-prison

Classification: **STATE**. Source: `data/public/class_playtests/wizard.json` / `wizard.hero.necromancer.mind-prison`. SHA256 `ea4c30ad02b32512b914d94e5ce989eea0c02f72abac1b575b11ba1340267416`.

Application components: `core.incapacitated`, `wizard.mind-prison.command`, `wizard.mind-prison.reaction-denial`, `wizard.mind-prison.slow`.

**name:** Mind Prison

**activation:** Action

**cost:** 10 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Concentration, maximum 3 rounds

**frequency:** 1/week; automatic Necromancer Final Theorem

**effect:** Mind Prison. Tags: hero, necromancer, final-theorem, enchantment, illusion, control, concentration. Target WIS save; failure Incapacitated until end of its NEXT normal turn, using the shared hard-denial mark. During that one turn you may spend a Bonus Action on your turn to specify one replacement behavior: target moves up to half Speed and either Dodges or makes one ordinary weapon attack instead of its lost Action; a PC chooses its own attack target and route. After that first affected turn, no further Action denial or compelled attack occurs: while concentration continues, target Speed is halved and it cannot take Reactions. It repeats WIS save at end each turn and on damage, ending on success. Maximum 3 rounds. No forced self-harm, spell expenditure, transfer of equipment, confession, belief change or permanent allegiance.

## ordinary-spell:ordinary:dispel-minor

Classification: **HOOK**. Source: `data/public/spell_playtests/catalog.json` / `dispel-minor`. SHA256 `eaf300a9eea6b0abe4dd69eb5191a355d6333c993cb9c22c38937956d06e9bce`.

Application components: None applied directly by this binding..

**id:** dispel-minor

**activation:** Action

**rangeFeet:** 30

**targets:** One ongoing magical effect created by a rank-0 spell, or one harmless cosmetic magical effect, that you can perceive within range

**duration:** Instantaneous

**concentration:** False

**components:** V, S

**resolution:** None. If the target is eligible, the selected ongoing effect ends immediately.

**effect:** End one ongoing rank-0 spell effect or harmless cosmetic magical effect. This can end a cantrip-created light, minor illusion, temporary magical mark, minor ward, or equivalent ongoing rank-0 effect.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Cannot dispel ranked spells, permanent enchantments, magic items, curses, class engines, creature traits, instantaneous damage already resolved, or effects explicitly protected from dispelling. Cannot erase historical consequences of an ended effect. Repeated cantrip casts use shared Refrain rules.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. 

**previousDraftDesignNotes:** NEW provisional eligibility boundary. Source said to end one harmless magical effect or cantrip but supplied no timing, range, or interaction with permanent magic.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:seal-minor-wound

Classification: **ALREADY**. Source: `data/public/spell_playtests/catalog.json` / `seal-minor-wound`. SHA256 `22d3d9d11c155ae4a6a389d4ac082309f0ca10fcaea420f250ff8911c6328b15`.

Application components: None applied directly by this binding..

**id:** seal-minor-wound

**activation:** Action

**rangeFeet:** 30

**targets:** One living creature you can perceive within 30 feet

**duration:** Instantaneous

**concentration:** False

**components:** V, S

**resolution:** None.

**effect:** Choose one: stabilize a living creature at 0 HP without restoring HP, or end one ordinary Bleed/minor ongoing bleeding effect on the target.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Restores no HP, removes no Wound, disease, poison, curse, death consequence, internal injury, or non-bleeding damage-over-time effect. A stabilized creature remains at 0 HP. Repeated cantrip casts use shared Refrain rules.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. 

**previousDraftDesignNotes:** NEW provisional definition of 'minor bleeding'; healing was intentionally not added because the source specified stabilization or stopping minor bleeding only.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:earthen-grip

Classification: **APPLY**. Source: `data/public/spell_playtests/catalog.json` / `earthen-grip`. SHA256 `a6c2fdae3e80c4cc1421784daa0dd10068d470a654bf411537ba8db4e7b29a8a`.

Application components: `core.restrained`, `ordinary.earthen-grip.restraint`.

**id:** earthen-grip

**activation:** Action

**rangeFeet:** 30

**targets:** One Large-or-smaller creature touching solid ground that you can perceive within 30 feet

**duration:** Concentration, until the end of the target's next turn

**concentration:** True

**components:** V, S, F

**resolution:** Target makes a Strength save. On failure it is Restrained until the end of its next turn. On success there is no effect.

**effect:** Conjured earth grips the target in place, inflicting the CoreV2 Restrained condition until the end of its next turn on a failed Strength save; ending concentration ends the restraint sooner.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Does not affect creatures not touching a solid surface, creatures larger than Large, or targets whose anatomy or explicit immunity prevents restraint. The effect ends automatically at the stated time and does not require repeated escape checks. It is not a whole-Action denial. Ranked casting causes normal Dissonance and Refrain. An affected target may use an Action for STR(Athletics) or DEX(Acrobatics) against your spell DC to escape early.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. Catalog one-round restraint limits Core one-minute metadata; retain Core concentration. The target can use an Action for STR(Athletics) or DEX(Acrobatics) against your spell DC to end restraint early.

**previousDraftDesignNotes:** NEW provisional 60-foot range, size/ground eligibility, and CoreV2 Restrained mapping. Source specified a Strength save and one-round immobilization/restraint.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:elemental-bolt

Classification: **NONSTATE**. Source: `data/public/spell_playtests/catalog.json` / `elemental-bolt`. SHA256 `358e09a8febfa809e84c98440007edeb08234a878e23aac8beb7af35b7a68a44`.

Application components: None applied directly by this binding..

**id:** elemental-bolt

**activation:** Action

**rangeFeet:** 30

**targets:** One creature you can perceive within range

**duration:** Instantaneous

**concentration:** False

**components:** V, S, F

**resolution:** Make a spell attack. On hit deal 2d8 damage of the element chosen when cast; on miss deal no damage.

**effect:** Choose acid, cold, fire, or lightning when casting. Launch an elemental bolt dealing 2d8 damage of the chosen type on a successful spell attack.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Choice affects damage type only and grants no automatic Burn, slow, chain, corrosion, terrain, or status rider. The damage cannot be split among multiple targets. Ranked casting causes normal Dissonance and Refrain.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. 

**previousDraftDesignNotes:** NEW provisional 90-foot range and spell-attack resolution. Source 2d8 damage and four listed element choices are preserved.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:aura-glimpse

Classification: **HOOK**. Source: `data/public/spell_playtests/catalog.json` / `aura-glimpse`. SHA256 `d50180b3d48b9df2758d9e348f61d951adead6af76c7c330395dda60852013a4`.

Application components: None applied directly by this binding..

**id:** aura-glimpse

**activation:** Action

**rangeFeet:** 10

**targets:** Self; magical auras on creatures, objects, and active effects within a 10-foot radius that you can directly perceive

**duration:** Until the end of your current turn

**concentration:** False

**components:** V, S

**resolution:** None.

**effect:** Until the end of your turn, perceive the presence and outline of active magical auras within 10 feet. You can distinguish separate aura sources but learn no automatic school, rank, owner, command word, curse, or detailed property.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Total cover and effects explicitly blocking magical detection prevent perception. Does not reveal dormant magic, protected/secret properties, invisible nonmagical creatures, thoughts, traps without magical auras, or exact mechanics. Repeated cantrip casts use shared Refrain rules.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. 

**previousDraftDesignNotes:** NEW provisional one-turn duration and information ceiling. Source 10-foot magical-aura glimpse is preserved.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:identify

Classification: **HOOK**. Source: `data/public/spell_playtests/catalog.json` / `identify`. SHA256 `99b2a76f00ee7e672952214e6dc9bc6a29ef37c8a87c38eaf06285d321fb3566`.

Application components: None applied directly by this binding..

**id:** identify

**activation:** Action

**rangeFeet:** 30

**targets:** One magical object or ongoing magical effect you can see within 30 feet

**duration:** Instantaneous information

**concentration:** False

**components:** V, S, F

**resolution:** None.

**effect:** Learn the target's publicly knowable magical function: its broad school or magical category if any, ordinary activation method, numerical bonuses or penalties exposed by the effect, whether it requires attunement or equivalent bonding, and the remaining count of explicitly tracked finite charges if that information is not protected by the item's rules.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Does not automatically reveal curses, hidden sentience, passwords, historical provenance, secret Director-only functions, artifact plot conditions, concealed transformations, future consequences, protected command words, or information an effect explicitly blocks from divination. An explicit ward may register as obscured if its rules say so; hidden properties alone do not reveal their own existence. Cannot identify mundane craftsmanship beyond ordinary observation. Ranked casting causes normal Dissonance and Refrain.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. Core Action and30ft restored; no automatic secret or curse disclosure. An expressly hidden property remains hidden, without automatically revealing that a hidden property exists.

**previousDraftDesignNotes:** NEW provisional 1-minute examination procedure and public/secret information boundary. Source requirement to reveal/determine magical properties is preserved without assuming imported spell-block behavior.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:detect-magic

Classification: **HOOK**. Source: `data/public/spell_playtests/catalog.json` / `detect-magic`. SHA256 `8863fa4c2e5d7e871450dcc320ae56a78c07eca67123cc0548c3ba940cc68edf`.

Application components: None applied directly by this binding..

**id:** detect-magic

**activation:** Action

**rangeFeet:** 30

**targets:** Self; magical auras on creatures, objects, and active effects within 30 feet that you can perceive

**duration:** Concentration, up to 10 minutes

**concentration:** True

**components:** V, S, F

**resolution:** None.

**effect:** For the duration, perceive the presence and visible outline of active magical auras within 30 feet. As an Action on a later turn, you may focus on one perceived aura to learn its broad magical school/category if that information is not protected.

**scaling:** None. Damage dice, target count, range and duration do not automatically increase with character or class level.

**limitations:** Total cover and explicit anti-divination effects block detection. Does not reveal exact spell names, ranks, statistics, owners, motives, hidden curses, dormant magic, secret Director information, or mundane invisible creatures. Detecting an aura does not grant line of effect or permission to target through barriers. Ranked casting causes normal Dissonance and Refrain.

**designNotes:** Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. Core instantaneous metadata cannot sustain the described perception; this pilot uses explicit concentration for up to10minutes. The30ft range limits perception of spell-granted information.

**previousDraftDesignNotes:** NEW provisional 10-minute concentration duration and two-step information model. Source 30-foot magical detection is preserved.

**authoringFile:** data/playtest/spell_drafts/batch_1.json

## ordinary-spell:ordinary:ray-of-frost

Classification: **STATE**. Source: `data/public/spell_playtests/catalog.json` / `ray-of-frost`. SHA256 `bbbdf626b332376fc829a9bca21dea67c199a10671dcea17a77456747d153185`.

Application components: `ordinary.ray-of-frost.slow`.

**id:** ray-of-frost

**activation:** Action

**rangeFeet:** 10

**targets:** One creature you can perceive within range

**duration:** Damage instantaneous; Speed reduction until the end of the target's next regular turn

**concentration:** False

**components:** V, S

**resolution:** Make a spell attack against the target. On hit, deal 1d8 cold damage and reduce its Speed by 10 feet until the end of its next regular turn. On miss, no effect.

**effect:** Strike one creature with a freezing ray for 1d8 cold damage and a temporary 10-foot Speed reduction.

**scaling:** None; damage remains 1d8 and Speed reduction remains 10 feet.

**limitations:** Speed cannot be reduced below 0. Multiple Ray of Frost reductions do not stack; a later hit refreshes the duration. The spell does not Root, Restrict, or remove Actions. Cantrip repeats use Refrain.

**designNotes:** Core V2 Action, 10-foot range, V/S components, and source damage/Speed reduction are preserved. Core resolution is non-operational; spell attack is NEW provisional. Core lists Instantaneous duration, so the damage remains instantaneous while the source movement rider is explicitly timed through the target's next turn.

**authoringFile:** data/playtest/spell_drafts/batch_2.json

## ordinary-spell:ordinary:frost-arrow

Classification: **STATE**. Source: `data/public/spell_playtests/catalog.json` / `frost-arrow`. SHA256 `982ee5763d18a874499dee4141ff8ea86e2378a003c81384e6e4752f09b9f2aa`.

Application components: `ordinary.frost-arrow.slow`.

**id:** frost-arrow

**activation:** Action

**rangeFeet:** 10

**targets:** One creature you can perceive within range

**duration:** Damage instantaneous; Speed reduction until the end of the target's next regular turn

**concentration:** False

**components:** V, S, F

**resolution:** Make a spell attack against the target. On hit, deal 2d8 cold damage and reduce its Speed by 10 feet until the end of its next regular turn. On miss, no effect.

**effect:** Fire a freezing magical projectile that deals 2d8 cold damage and slows the target by 10 feet on a hit.

**scaling:** None; damage remains 2d8 and Speed reduction remains 10 feet.

**limitations:** Speed reduction does not stack with itself and cannot reduce Speed below 0. The spell does not Root or remove Actions. Ranked casting causes normal Dissonance and Refrain.

**designNotes:** Core V2 Action, 10-foot range, V/S/F components, and source damage/slow are preserved. The Core resolution is non-operational, so spell attack is a NEW provisional choice. Core says Instantaneous; the damage is instantaneous while the movement rider is explicitly timed through the target's next turn.

**authoringFile:** data/playtest/spell_drafts/batch_2.json

## ordinary-spell:ordinary:feather-fall

Classification: **ALREADY**. Source: `data/public/spell_playtests/catalog.json` / `feather-fall`. SHA256 `85004ad9cb188a812d46e1a60982003f2026ade68a11032238d569b5ecb9087e`.

Application components: None applied directly by this binding..

**id:** feather-fall

**activation:** Action

**rangeFeet:** 60

**targets:** Up to 5 willing falling creatures you can perceive within range

**duration:** Until each target lands, stops falling, or immediately before the caster's regular turn ten rounds after casting (1 minute), whichever occurs first

**concentration:** False

**components:** V, S, F

**resolution:** None; willing legal targets are affected automatically.

**effect:** Slow each target's downward descent to at most 60 feet at each once-per-round Fall Marker. Use the new provisional falling bridge in SPELL_INTEGRATION_RULES.md: dissipate prior uncontrolled momentum on application; if landing while this spell is active, impact is min(3, floor(total distance descended in this fall / 20))d6 bludgeoning. This impact limit is a new playtest decision, not recovered spell text.

**scaling:** None; maximum descent remains 60 feet per round and target cap remains 5.

**limitations:** Grants no flight, hovering, lateral movement or automatic safe landing. A creature ceases to be affected once it lands or is no longer Falling. Targets cannot be added after casting. Ranked casting causes normal Dissonance and Refrain. This Action requires targets still Falling when a legal Action is available; it cannot undo an impact. On expiry aloft, reset uncontrolled distance to zero and resume ordinary descent at the existing marker with no immediate extra step. Expiry resolves before a coincident Falling Step.

**designNotes:** Core V2 consistently gives Action, 60-foot range, V/S/F components and the five-creature/60-feet-per-round effect, but lists Instantaneous duration despite sustained descent. Duration, initiative marker, momentum handling and impact formula are NEW provisional decisions agreed with the GPT notebook. See SPELL_INTEGRATION_RULES.md for the full procedure and source-search limits. This does not import a Reaction casting time or automatic fall-damage immunity. F is an existing class casting focus.

**authoringFile:** data/playtest/spell_drafts/batch_2.json

## class-card:crimson-agent:crimson-agent.hero.shadow-operative.veinjammer

Classification: **STATE**. Source: `data/public/class_playtests/crimson-agent.json` / `crimson-agent.hero.shadow-operative.veinjammer`. SHA256 `7171e9629551ffbd75084dd66db7e2a149373a97e2a25cdf3fb3a493366848f2`.

Application components: `crimson-agent.veinjammer.concentration-penalty`, `crimson-agent.veinjammer.slow`.

**name:** Veinjammer

**activation:** Passive

**cost:** 0

**rangeAndTarget:** One creature damaged by your Bleed

**duration:** Until end target's next turn

**frequency:** Once/round

**effect:** After a Bleed tick, choose that victim: Speed reduced 5 ft, minimum 0, and its next concentration save takes-1. Nonstacking; does not remove an Action or prohibit spellcasting.

## class-card:dragoon:dragoon.hero.drake-rider.drakestorm-dive

Classification: **STATE**. Source: `data/public/class_playtests/dragoon.json` / `dragoon.hero.drake-rider.drakestorm-dive`. SHA256 `cb1c3322f8f5b29283e3494bc8eb4e9576f1d2ff4e2e7f03ff8d82510b3fc7fc`.

Application components: `dragoon.burn`, `dragoon.drakestorm-dive.cold-slow`, `dragoon.drakestorm-dive.reaction-denial`.

**name:** Drakestorm Dive

**activation:** Action

**cost:** 5 Momentum; 1 long-rest use

**rangeAndTarget:** Leap up to 60 ft; up to 6 enemies within 15 ft of landing

**duration:** Instant

**frequency:** 1/long rest

**effect:** Choose fire/cold/lightning. DEX save:6d8 chosen damage, half on success. On failure fire applies Burn, cold reduces Speed 10 ft until end next turn, lightning prevents Reactions until then. Land in legal empty space; no additional weapon attack.

**Reviewed overlay:** Cold slow and lightning Reaction denial: SOURCE next regular END, correcting earlier discussion. Fire uses existing independent periodic binding.

## class-card:dragoon:dragoon.hero.drake-rider.elemental-lance

Classification: **STATE**. Source: `data/public/class_playtests/dragoon.json` / `dragoon.hero.drake-rider.elemental-lance`. SHA256 `f6b2b36a079df474ab69c516158d9a6d4de327fc704a4fef0b0ad2eedc7d8cb3`.

Application components: `dragoon.elemental-lance.cold-slow`, `dragoon.elemental-lance.opportunity-denial`.

**name:** Elemental Lance

**activation:** Bonus Action

**cost:** 2 Momentum

**rangeAndTarget:** Your polearm

**duration:** 3 of your turns

**frequency:** Recharge 3

**effect:** Choose fire/cold/lightning. Once/own turn a hit adds S d4 damage; fire adds 1 damage, cold reduces target Speed 5 ft until end next turn, lightning denies opportunity attacks until start its next turn. Nonstacking with Spearcraft; one element rider/turn.

**Reviewed overlay:** Cold slow: SOURCE next regular END. Lightning opportunity-attack denial: TARGET next regular START. Preserve distinct clocks.

## class-card:mage:mage.base.elemental-bolt

Classification: **STATE**. Source: `data/public/class_playtests/mage.json` / `mage.base.elemental-bolt`. SHA256 `0aa7ebabd70565f5532458b919c7883e848a6c46091cb1b7de23e919704b71ea`.

Application components: `mage.cold-focus.flat`, `mage.elemental-bolt.burn`.

**name:** Elemental Bolt

**activation:** Action

**cost:** 1 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Instantaneous

**frequency:** At will while RP remains

**effect:** Elemental Bolt. Tags: mage-spell, elemental, focus, damage. Make a Mage spell attack. On a hit deal S d8 + M damage of your current Focus. Fire: target takes 1d4 fire at the start of its next turn. Cold: Speed -10 feet until the end of its next turn. Lightning: one different enemy within 10 feet takes S lightning damage. Secondary damage creates no new spell cast or chain credit.

## class-card:mage:mage.base.cold.cold

Classification: **STATE**. Source: `data/public/class_playtests/mage.json` / `mage.base.cold.cold`. SHA256 `bdbd2354d75ec75c65f5749dab24313e540c88d617bb80152b2859b311b182cf`.

Application components: `mage.cold-focus.flat`, `mage.cold-focus.glacier`.

**name:** Cold

**activation:** Passive

**cost:** 0; Glacier Spike costs 2 RP when primed

**rangeAndTarget:** Self; finisher uses a 15-foot cone

**duration:** Permanent Focus; finisher instantaneous plus slow

**frequency:** Choose at Mage 2; finisher recharge 3 rounds

**effect:** Elemental Focus — Cold. Tags: focus, cold. Once on each of your turns, a natural 19 that hits with a Cold Mage spell is a critical hit. When a Cold Mage spell damages a creature, its Speed is reduced by 10 feet until the end of its next turn, minimum 0. FINISHER — Glacier Spike: after a completed Cold Nuke Chain, Bonus Action, 2 RP. Creatures in a 15-foot cone make Constitution saves, taking (S+1)d8 cold on failure or half on success; failed creatures have their Speed halved until the end of their next turn.

## class-card:mage:mage.arch.elemental-mastery

Classification: **HOOK**. Source: `data/public/class_playtests/mage.json` / `mage.arch.elemental-mastery`. SHA256 `a4cd631e8a8eeba6bfed86337300867b29f50c2c047ff2816b83b53a9acf86c0`.

Application components: None applied directly by this binding..

Modifies/authorizes later application: `mage.cold-focus.flat`, `mage.cold-focus.glacier`, `mage.elemental-bolt.burn`, `mage.fire-focus.burn`, `mage.inferno-lance.burn`.

**name:** Elemental Mastery

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your current Elemental Focus spells

**duration:** Permanent

**frequency:** Always

**effect:** Elemental Mastery. Tags: arcanist, focus. Improve the secondary effect of your current Focus. Fire Burns from your Focus cards last one additional turn but never stack. Cold Focus Speed reductions increase by another 5 feet, minimum 0. Lightning Focus's once-per-turn secondary arc increases from S flat lightning damage to S d4 lightning damage. Pivoted Focus uses the corresponding upgraded rider.

## class-card:mage:mage.arch.elemental-surge

Classification: **STATE**. Source: `data/public/class_playtests/mage.json` / `mage.arch.elemental-surge`. SHA256 `a961e748135bc74d8f21cbec8fdbfed01bb7742319dfe3ef74e6b8fa3b05bdfb`.

Application components: `mage.cold-focus.flat`, `mage.fire-focus.burn`.

**name:** Elemental Surge

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Instantaneous

**frequency:** Recharge 2 rounds

**effect:** Elemental Surge. Tags: mage-spell, arcanist, elemental, focus, damage. Make a Mage spell attack. On a hit deal (S+1)d8 + M damage of your current Focus. Fire also applies the Focus Burn; Cold applies the Focus Speed reduction; Lightning applies the Focus secondary arc. This is Focus-eligible and can occupy one slot in a Nuke Chain.

## class-card:mage:mage.hero.elementalist.elemental-fusion

Classification: **STATE**. Source: `data/public/class_playtests/mage.json` / `mage.hero.elementalist.elemental-fusion`. SHA256 `4464d73abd9221a1c87048dc87a08c86effd162f3b8f1b7de9faf61dc5ea79dc`.

Application components: `mage.elemental-fusion.burn`, `mage.elemental-fusion.opportunity-denial`, `mage.elemental-fusion.reaction-denial`, `mage.elemental-fusion.slow`.

**name:** Elemental Fusion

**activation:** Action

**cost:** 4 RP

**rangeAndTarget:** One creature within 60 feet

**duration:** Instantaneous

**frequency:** Recharge 2 rounds

**effect:** Elemental Fusion. Tags: mage-spell, elementalist, elemental, damage. Choose your current Focus and one other element among Fire, Cold and Lightning. Make a Mage spell attack. On hit deal S d8 of each chosen element. Pair rider: Fire+Cold reduces Speed by 10 feet and applies 1d4 fire at start of target's next turn; Fire+Lightning removes Reaction until start of target's next turn; Cold+Lightning reduces Speed by 10 feet and prevents opportunity attacks until end of target's next turn. For Nuke Chain purposes this spell counts only as your current Focus element.

**Reviewed overlay:** NEW missing-endpoint bridge: Fire+Cold slow ends target next regular END; Cold+Lightning slow/opportunity denial same target-END; Fire+Lightning Reaction denial target next regular START. Non-Focus secondary profiles do not receive Arch Mastery.

## class-card:mage:mage.hero.elementalist.cascade-storm

Classification: **STATE**. Source: `data/public/class_playtests/mage.json` / `mage.hero.elementalist.cascade-storm`. SHA256 `ef0516869275557a7da1d913c842d50866d213df080041e29bdb3a4a889724d6`.

Application components: `mage.cascade-storm.burn`, `mage.cascade-storm.cold-slow`, `mage.cascade-storm.reaction-denial`.

**name:** Cascade Storm

**activation:** Action

**cost:** 6 RP

**rangeAndTarget:** Up to three different creatures within 60 feet

**duration:** Instantaneous

**frequency:** Recharge 3 rounds

**effect:** Cascade Storm. Tags: mage-spell, elementalist, fire, cold, lightning, damage. Choose up to three creatures. Resolve one separate Mage spell attack against each: first hit deals S d6 fire and 1d4 fire next turn; second hit deals S d6 cold and Speed -10 feet until end next turn; third hit deals S d6 lightning and removes Reaction until start next turn. If fewer than three targets are chosen, unused elements are lost. For Nuke Chain purposes choose one of the three elements before casting; Cascade Storm counts only as that element.

**Reviewed overlay:** Printed cold slow ends SOURCE next regular END; printed lightning Reaction denial SOURCE next regular START. Current-Cold passive may independently trigger on positive cold damage with its own target-END deadline.

## class-card:mage:mage.hero.elementalist.elemental-mastery

Classification: **HOOK**. Source: `data/public/class_playtests/mage.json` / `mage.hero.elementalist.elemental-mastery`. SHA256 `447852ee7d9a2ccc5b1a7e2d261b2b80f1791c5286133a8f9e62221a33b3f55d`.

Application components: None applied directly by this binding..

**name:** Elemental Mastery

**activation:** Bonus Action

**cost:** 5 RP

**rangeAndTarget:** Self

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** Elemental Mastery. Tags: elementalist, focus, mastery. For 3 rounds, Fire, Cold and Lightning Mage spells all count as matching your current Focus for Nuke Chain eligibility. After you complete one three-distinct-name chain during this duration, you may choose any one of the three Focus finishers when it becomes primed, regardless of your current Focus. Only one finisher may be generated by this use. After that finisher resolves or expires, the mastery continues defensively but cannot prime another off-focus finisher.

## class-card:mage:mage.hero.lich.undying-spellform

Classification: **STATE**. Source: `data/public/class_playtests/mage.json` / `mage.hero.lich.undying-spellform`. SHA256 `f9eb71c6354a879da6fb752283a2e78cf2330465e97605dae15c939ecf413cea`.

Application components: `mage.undying-spellform.mobility-cap`.

**name:** Undying Spellform

**activation:** Triggered

**cost:** 0

**rangeAndTarget:** Self

**duration:** Until end of your next regular turn

**frequency:** 1/long rest

**effect:** Undying Spellform. Tags: lich, undead, death. When damage reduces you to 0 HP without killing you outright, remain conscious and able to take Actions until the end of your next regular turn. You remain at 0 HP, cannot benefit from voluntary movement faster than half Speed, and still suffer ordinary consequences of further damage. If still at 0 HP when the effect ends, become unconscious and suffer one failed death save. Healing above 0 ends this feature early.

## class-card:monk:monk.arch.tortoise.echoing-guard

Classification: **STATE**. Source: `data/public/class_playtests/monk.json` / `monk.arch.tortoise.echoing-guard`. SHA256 `f8151ac23c9eddbc67c93facb73352826b6e56226fd5b118f0485db0b698d7cc`.

Application components: `monk.echoing-guard.stagger`.

**name:** Echoing Guard

**activation:** Passive

**cost:** 0; requires Discipline Initiate: Tank

**rangeAndTarget:** Creature whose attack misses you or whose attack you reduce to 0 damage

**duration:** Until end of that creature's next turn

**frequency:** At most once per attacker per round

**effect:** Echoing Guard. Tags: arch, tortoise, discipline, defense. When an attack misses you, or one of your defensive techniques reduces the triggering attack to 0 damage, the attacker becomes Staggered: -1 to attack rolls and -5 feet Speed until the end of its next turn. Reapplication refreshes but does not stack.

**Reviewed overlay:** Custom -1 attacks/-5Speed only; not Core Staggered. classification.staggered for named readers/removers. Strongest same-style attack penalty, no addition with Warrior version.

## class-card:monk:monk.arch.pressure-point-strike

Classification: **STATE**. Source: `data/public/class_playtests/monk.json` / `monk.arch.pressure-point-strike`. SHA256 `8840fdef260a38cdc2c01d2443bbb16730eb5e43022b396aa686c0c0bea4862a`.

Application components: `monk.pressure-point.arm`, `monk.pressure-point.leg`.

**name:** Pressure Point Strike

**activation:** Action

**cost:** 2 Ki

**rangeAndTarget:** One creature within unarmed reach

**duration:** Until end of target's next turn

**frequency:** Recharge 2 rounds

**effect:** Pressure Point Strike. Tags: arch, active, attack, control. Make one unarmed strike. On a hit the target makes a Constitution save. On failure choose Arm or Leg: Arm gives -1 on attack rolls; Leg reduces Speed by 10 feet, minimum 0. This represents temporary disruption only and causes no persistent limb injury.

## class-card:oracle:oracle.supplement.bones.ledger-s-command

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.ledger-s-command`. SHA256 `409a76be401ca671acce588548c0d1e35f072a339c9b370fedede28cf71b0d69`.

Application components: `oracle.ledger-command.control`, `oracle.ledger-command.soft-fallback`.

**name:** Ledger's Command

**activation:** Action

**cost:** 2 RC

**rangeAndTarget:** Up to 2 undead within 4 tiles

**duration:** 2 rounds

**frequency:** At will while RC remains

**effect:** Each target makes a Wisdom save if hostile or unwilling; willing undead may waive it. On failure you command it for 2 rounds. Once per round as a Bonus Action, command one controlled undead to move up to its Speed and make one ordinary attack, using its own statistics; this obeys the universal one-extra-action limit and all controlled undead share that single Bonus Action command. Controlled undead reduce their first damage each round by 1. Once during the command, one controlled expendable undead may intercept a single-target attack against you and be reduced to 0 HP after absorbing it. This feature creates no corpse, loot or RC farm. Eligible targets are nonlegendary undead of challenge rating no greater than half your Oracle level (round down), with Wisdom saves initially and at each turn end. Commanding uses your shared companion Bonus Action; only one commanded undead makes one attack per round, capped at S d8+M damage with no monster multiattack, recharge or spell resources. Commanding a hostile undead to spend its Action consumes its one hard-denial allowance; later control can only deny Reactions and reduce Speed to 0 on a failed save, never command another Action.

**prerequisite:** Oracle 6; Mystery: Bones; selected Tier II Revelation

## class-card:oracle:oracle.supplement.bones.bones-revelation-mastery

Classification: **HOOK**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.bones.bones-revelation-mastery`. SHA256 `14d4537572a0e9d37eb62850c1881097ec9da711640be7b293b0ff0918640577`.

Application components: None applied directly by this binding..

**name:** Bones Revelation Mastery

**activation:** Passive

**cost:** 0 RC

**rangeAndTarget:** One eligible known Bones Revelation

**duration:** Permanent

**frequency:** Choose one upgrade at Oracle 15

**effect:** Choose one mastery for a Revelation you know. Enhanced Marrow Drain: a living target hit also has Speed reduced by 1 tile until the end of its next turn. Enhanced Ledger's Command: may target up to 3 undead, but all controlled undead still share one Bonus Action command per round. Enhanced Unfinished Chorus: when its drain resolves, you may always redirect the healing to one ally within 3 tiles of you rather than yourself; its healing cap remains S+M.

**prerequisite:** Oracle 15; Mystery: Bones; Revelation Mastery

## class-card:oracle:oracle.supplement.cataclysm.tremor-sense

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.cataclysm.tremor-sense`. SHA256 `b236951ed93fecf576f4ebdb262f3feab1d22f6d5ddbdc9f589f6127b26b6db7`.

Application components: `core.prone`, `oracle.tremor-sense.slow`.

**name:** Tremor Sense

**activation:** Passive and Action

**cost:** 0 RC

**rangeAndTarget:** Self; enemies within 2 tiles for tremor

**duration:** Permanent; tremor penalties until end of your next turn

**frequency:** Passive always; tremor 1/short rest

**effect:** While touching the ground or a structure, you can identify obvious structural instability, hollow spaces and hidden passages within 3 tiles that transmit vibration, subject to ordinary concealment and construction. Reduce the first bludgeoning damage you take each round by 1. Once per short rest as an Action, enemies within 2 tiles make Strength saves; on failure they fall Prone, and on success their Speed is reduced by 1 tile until the end of your next turn.

**prerequisite:** Oracle 1; Mystery: Cataclysm

## class-card:oracle:oracle.supplement.cataclysm.shardburst

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.cataclysm.shardburst`. SHA256 `043ddecbe3dcb232027fd0ef6fc4a5605b43c047bc0bc985a98533fb6ac3d5ff`.

Application components: `core.prone`, `oracle.shardburst.slow`.

**name:** Shardburst

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** 2-tile-radius burst centered within 4 tiles

**duration:** Damage instantaneous; Speed reduction until end of target's next turn

**frequency:** At will while RC remains

**effect:** Enemies in the burst make Dexterity saves, taking 1d6+M bludgeoning damage on failure or half on success. A creature that fails also has Speed reduced by 1 tile until the end of its next turn. If a failing creature is adjacent to a wall, rubble or substantial stone terrain, it also makes a Strength save; failure knocks it Prone.

**prerequisite:** Oracle 3; Mystery: Cataclysm; selected Tier I Revelation

## class-card:oracle:oracle.supplement.cataclysm.gale-of-unmaking

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.cataclysm.gale-of-unmaking`. SHA256 `19568483244e5afbf5d0225d9fd589e8d71dd1a27e92420428dd8621f8825629`.

Application components: `oracle.gale-of-unmaking.slow`.

**name:** Gale of Unmaking

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** 4-tile line originating from you

**duration:** Damage/movement instantaneous; difficult terrain until start of your next turn

**frequency:** At will while RC remains

**effect:** Enemies in the line make Strength saves, taking 1d6+M bludgeoning damage and being pushed 1 tile on failure, or half damage with no push on success. Failed targets also have Speed reduced by 1 tile until the end of their next turn. Mundane exposed flames in the line are extinguished. Loose natural debris in the line becomes difficult terrain until the start of your next turn.

**prerequisite:** Oracle 3; Mystery: Cataclysm; selected Tier I Revelation

## class-card:oracle:oracle.supplement.cataclysm.seal-s-fracture

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.cataclysm.seal-s-fracture`. SHA256 `ff50d9552783ceff6b7703bc3b2bf958b327d7adbf220a9b89f530dc1f159e92`.

Application components: `oracle.seals-fracture.backlash`.

**name:** Seal's Fracture

**activation:** Action

**cost:** 3 RC

**rangeAndTarget:** 4-tile-radius fixed zone centered within 5 tiles

**duration:** 2 rounds; Revelation backlash 1 round

**frequency:** At will while RC remains

**effect:** Choose Earthquake, Storm or Fire. The zone becomes difficult terrain. At activation and at the start of your next regular turn, enemies in the zone make Dexterity saves, taking 2d6 damage on failure or half on success: bludgeoning for Earthquake, lightning for Storm, fire for Fire. Until the zone ends, enemies inside take -1 on saving throws against your Cataclysm Revelations; allies inside reduce first damage each round by 1 and cannot be knocked Prone by this zone. Difficult terrain expands 1 tile outward after the second pulse but deals no extra damage there. Structures may crack at Director discretion. When the effect ends you are suffering Revelation backlash until end of your next turn: -1 attacks/saves and Speed -5 feet.

**prerequisite:** Oracle 9; Mystery: Cataclysm

## class-card:oracle:oracle.supplement.dream.slumber-glimpse

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.dream.slumber-glimpse`. SHA256 `d6f622de31985a6bdb101de9ff66667ea88e40e271719e298fca3090b1037fc7`.

Application components: `oracle.slumber-glimpse.action-denial`, `oracle.slumber-glimpse.attack-bonus`, `oracle.slumber-glimpse.initiative-penalty`, `oracle.slumber-glimpse.reaction-denial`, `oracle.slumber-glimpse.soft-fallback`.

**name:** Slumber Glimpse

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One enemy within 4 tiles

**duration:** Until end of target's next turn

**frequency:** At will while RC remains

**effect:** The target makes a Wisdom save. On failure it would lose its next Action, subject to the Oracle hard-control guard; it also loses Reactions and takes -2 on its next initiative adjustment or initiative check before the end of the encounter. The next attack against it before the end of its next turn gains +2 to hit. On a target already protected by the hard-control guard, failure instead removes Reactions and reduces Speed to 0 until the end of its next turn.

**prerequisite:** Oracle 3; Mystery: Dream; selected Tier I Revelation

**Reviewed overlay:** Initiative-2 is next eligible roll/check before encounter end; no existing-slot change. Retain separate original hard/fallback and next-attack riders.

## class-card:oracle:oracle.supplement.life.resonant-seed

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.life.resonant-seed`. SHA256 `ee79b90bfc9c7117d99edebc2dc66e6b79b37bbc5f732ac6a2c4bedabab152ab`.

Application components: `oracle.resonant-seed.slow`.

**name:** Resonant Seed

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** 2-tile-radius fixed zone centered within 4 tiles

**duration:** 3 rounds

**frequency:** At will while RC remains; one Seed zone at a time

**effect:** When a living ally starts its turn in the zone, it regains 1d4 HP, at most once per round and for at most three pulses from this use, and may end Frightened or Poisoned on the first pulse it receives. Undead entering or starting their turn in the zone take 1d4 radiant damage once per round and make a Strength save; on failure their Speed is reduced by 1 tile until the end of that turn. Healing requires the paid 1 RC activation and ends after 3 rounds.

**prerequisite:** Oracle 3; Mystery: Life; selected Tier I Revelation

**Reviewed overlay:** Slow ends at end of actual triggering turn, including off-turn entry or extra turn. No turn underway:6 elapsed seconds. Printed per-creature/round pulse cap retained.

## class-card:oracle:oracle.supplement.time.moment-s-pause

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.time.moment-s-pause`. SHA256 `622b00de01c8000facb0136d67505e54872230e43acfa80b77493d514434fc3d`.

Application components: `oracle.moments-pause.action-denial`, `oracle.moments-pause.initiative-delay`, `oracle.moments-pause.reaction-denial`, `oracle.moments-pause.soft-fallback`.

**name:** Moment's Pause

**activation:** Action

**cost:** 1 RC

**rangeAndTarget:** One enemy within 4 tiles

**duration:** Until end of target's next turn

**frequency:** At will while RC remains

**effect:** The target makes a Wisdom save. On failure it would lose its next Action, subject to the Oracle hard-control guard; it also loses Reactions and is treated as acting one initiative step later for the next round only. If the target has already suffered a full-turn denial from you this encounter, failure instead removes its Reaction and reduces its Speed to 0 until the end of its next turn.

**prerequisite:** Oracle 3; Mystery: Time; selected Tier I Revelation

**Reviewed overlay:** Pending next-numbered-round canonical snapshot delay, nonstack per target. Stable application order, move after first surviving later snapshot participant, ignore new entrants. No duplicate/lost turns or changes to virtual markers. Guide procedure controls.

## class-card:oracle:oracle.supplement.time.the-spiral-opens

Classification: **STATE**. Source: `data/public/class_playtests/oracle.json` / `oracle.supplement.time.the-spiral-opens`. SHA256 `b15b7a477b14185e1510967e1d24c7e46a856a400ef1575f876d2adbaa39ee28`.

Application components: `oracle.spiral-opens.forced-echo`, `oracle.spiral-opens.player-speed-zero`.

**name:** The Spiral Opens

**activation:** Action

**cost:** 0 RC

**rangeAndTarget:** Self; one known beneficial Time Revelation or one enemy within 5 tiles

**duration:** 3 rounds

**frequency:** 1/long rest

**effect:** For 3 rounds, at the start of each of your regular turns choose ONE temporal option, each usable at most once during this Final. ECHO REVELATION: repeat only the immediate numeric damage, healing, movement or buff component of one beneficial Time Revelation you personally resolved during the previous round, paying 0 RC; this copy is not a new Revelation cast, copies no resource restoration, action grant, hard control, condition trigger, Prophecy Trigger or proc. FORCED ECHO: choose one non-player enemy within 5 tiles and one ordinary weapon attack or non-resource movement action it took during its previous turn. The enemy makes a Wisdom save. On failure, during its next turn it must repeat that action pattern if legally possible, but it chooses all legal targets and paths; it spends no limited resources and cannot be forced to harm itself. A player-controlled creature instead, on a failed save, loses its Reaction and must choose either repeat one ordinary non-resource action type from its prior turn or have Speed reduced to 0 until turn end. Allies retain memory of all temporal echoes. This Final never creates more than one additional full Action for any creature in a round. There are only two options in this Final; after using both once, remaining rounds provide only the printed temporal presence, without another echo. An echoed healing amount also pays 1 RC or consumes an unused per-rest healing use; a temporal copy cannot create an uncosted healing reserve.

**prerequisite:** Oracle 20; Mystery: Time

## class-card:paladin:paladin.supplement.oathbreaker-shared.black-manifestation

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-shared.black-manifestation`. SHA256 `fa105c2d7a52015f0d3640f7d570072e5e0a5d005d7e818da9bac58bd438247f`.

Application components: `paladin.black-manifestation.reaction-denial`, `paladin.black-manifestation.slow`.

**name:** Black Manifestation

**activation:** Bonus Action

**cost:** 1 long-rest use

**rangeAndTarget:** Self and up to 3 enemies in aura

**duration:** Until start next turn

**frequency:** 1/long rest

**effect:** New Oathbreaker Final: gain 2 S+M temporary HP; chosen enemies WIS save or lose Reactions and Speed-10 ft for duration. Refresh one expended Signature use, then pay its normal Action and other costs when used. No Death Touch pool, RP, extra Action or Final reset.

**prerequisite:** Paladin 20; selected Oathbreaker inversion

## class-card:paladin:paladin.supplement.oath-of-dominion.law-s-weight

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-dominion.law-s-weight`. SHA256 `0f0c8ee395962a463a0c25295d96ee8d4d612f1c91452dd3de3b814ad8bfabf3`.

Application components: `paladin.laws-weight.control`.

**name:** Law's Weight

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** 20-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, 3 rounds

**frequency:** At will while RP remains

**effect:** A hostile creature is considered a source-qualified law breaker only if it knowingly lied while inside your Aura of Authority earlier this encounter. When such a creature enters or starts its turn in the zone, it makes a Charisma save. On failure its Speed is halved, AC is reduced by 2 and it cannot benefit from Dash or Haste-like extra movement until the start of its next turn. It saves again each turn while affected.

**prerequisite:** Paladin 9; Oath of Dominion

## class-card:paladin:paladin.supplement.oath-of-dominion.decree-of-submission

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-dominion.decree-of-submission`. SHA256 `fcfc6b46e7347183098c1f52803b62c1d6c336b4689bf06b2d981cd754119454`.

Application components: `core.charmed`, `core.frightened`, `paladin.decree-of-submission.command`, `paladin.decree-of-submission.soft-fallback`.

**name:** Decree of Submission

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** One creature within 30 feet that can hear you

**duration:** Concentration, maximum 1 minute

**frequency:** At will while RP remains

**effect:** Choose Sub mission or Dread. The target makes a Wisdom save; a source-qualified law breaker has disadvantage on the initial save. Sub mission: on failure the target is Charmed by you and you state one simple command from Approach, Retreat, Drop, Kneel, Halt or Release. On its first affected turn it follows that command in the safest reasonable way using no more than movement and one ordinary Action, then repeats the save at turn end. Dread: on failure it is Frightened of you and cannot willingly approach you, repeating the save at the end of each turn. Either mode ends on a successful repeat save. Player-controlled targets retain target choice, may never be commanded to self-harm, and cannot be forced to change beliefs or permanent allegiance. Spending that Action uses the hard-denial allowance. On later turns the effect only imposes Charmed and, on a failed repeat save, no Reactions and half Speed until the next turn; it cannot command another Action.

**prerequisite:** Paladin 13; Oath of Dominion

## class-card:paladin:paladin.supplement.oath-of-the-ancients.echo-of-ages

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.echo-of-ages`. SHA256 `c2031fea7ded087db7fe520e096539eabab65dfdd19affdcc84858486342f8fa`.

Application components: `paladin.echo-of-ages.attack-denial`, `paladin.echo-of-ages.soft-fallback`.

**name:** Echo of Ages

**activation:** Action

**cost:** 5 RP

**rangeAndTarget:** Up to 3 chosen creatures in your Oath aura

**duration:** Concentration, maximum 1 minute

**frequency:** At will while RP remains

**effect:** Selected allies have advantage on saves against Charmed and Frightened. When a selected hostile fey or elemental first enters your aura or is selected there, it makes a Wisdom save. On failure it cannot make attacks until the end of its next turn, though it may move, Dodge, Disengage, manipulate objects or use non-attack abilities. After suffering this attack denial once from you in the encounter, later failed saves instead remove its Reaction and reduce Speed by half until the end of its next turn.

**prerequisite:** Paladin 9; Oath of the Ancients

## class-card:paladin:paladin.supplement.oath-of-the-ancients.standing-stone

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-ancients.standing-stone`. SHA256 `406bf753a69c525d79259d9127a8d883974d4cca316281ad21a93e222b5dfce4`.

Application components: `paladin.standing-stone.slow`.

**name:** Standing Stone

**activation:** Action

**cost:** 7 RP

**rangeAndTarget:** 20-foot-radius fixed zone centered within 30 feet

**duration:** Concentration, 3 rounds

**frequency:** At will while RP remains

**effect:** The zone is difficult terrain for enemies and normal terrain for allies you choose when casting. At the start of each hostile fey or elemental's turn in the zone, it makes a Strength save. On failure its Speed is halved until the start of its next turn. It saves again each turn; no creature loses Actions or Reactions solely from Standing Stone.

**prerequisite:** Paladin 13; Oath of the Ancients

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash-aura

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash-aura`. SHA256 `76b2b582b92a0079b2539592c01651b66ff8f47b82cf26241cbe4d1a279e990e`.

Application components: `paladin.iron-leash-aura.movement-limit`, `paladin.iron-leash-aura.slow`.

**name:** Iron Leash Aura

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Up to 3 chosen enemies in your Oath aura

**duration:** While conscious and target remains in aura

**frequency:** Choose targets at start of each turn

**effect:** A selected enemy has Speed reduced by 10 feet, minimum 5 feet. The first time each round it willingly moves farther from you, it makes a Strength save; on failure its movement ends after 5 feet of that movement. This does not remove Actions or prevent forced movement.

**prerequisite:** Paladin 3; Oathbreaker — Oath of the Chain

## class-card:paladin:paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes`. SHA256 `31ccd2f2ec1880c1f2a789935cdecf6c1e775b71e0c5613804dbf38ac8f26b90`.

Application components: `paladin.reign-of-ashes.ash-bound`.

**name:** Reign of Ashes

**activation:** Action

**cost:** 2 RP

**rangeAndTarget:** Up to 3 enemies in your Oath aura

**duration:** Damage instantaneous; ash bonds until end of next turn

**frequency:** 1/short rest; replaces Signature Power use

**effect:** Each target makes a Dexterity save, taking 2 S d6 fire damage on failure or half on success. A failing target becomes ash-bound until the end of its next turn: Speed is halved and it cannot benefit from Dash or teleportation. It retains its Action and Reaction unless another feature removes them.

**prerequisite:** Paladin 11; Oathbreaker — Oath of Chains Broken

**Reviewed overlay:** Operative its-next-turn wins over summary: target next regular END. Half-Speed/noDash/no willing teleport benefit, including consent to allied transport. Legal involuntary hostile teleport remains source-governed.

## class-card:paladin:paladin.supplement.oath-of-the-martyr-king.royal-decree

Classification: **STATE**. Source: `data/public/class_playtests/paladin.json` / `paladin.supplement.oath-of-the-martyr-king.royal-decree`. SHA256 `88bebd369abca88ce26556eaba7bc7b98e7eed200f438055fcfb879890713a11`.

Application components: `core.prone`, `paladin.royal-decree.choice`.

**name:** Royal Decree

**activation:** Action

**cost:** 3 RP

**rangeAndTarget:** One hearing creature within 30 feet; three selected aura allies

**duration:** Until end of target’s next turn

**frequency:** While RP remains

**effect:** Target makes a Wisdom save. On failure it chooses to kneel Prone or move toward you by the safest route using up to its normal Speed on its next turn. It retains its Action and chooses its targets. No self-harm or hazardous route is required. Three chosen allies in your aura gain +1 on morale checks and saves against Frightened until the end of your next turn.

**prerequisite:** Paladin 5; Oath of the Martyr King

## class-card:shaman:shaman.base.elemental-affinity

Classification: **STATE**. Source: `data/public/class_playtests/shaman.json` / `shaman.base.elemental-affinity`. SHA256 `3de820b6a892ea574aca2a1443f8310cf5e4e9ffa46c109d087a922b4babdfe4`.

Application components: `shaman.elemental-affinity.ice-slow`.

**name:** Elemental Affinity

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Self

**duration:** Chosen permanently at 1

**frequency:** Automatic

**effect:** Choose Fire: first fire technique hit/turn adds 1 damage; Ice: first cold damage target/turn loses 5 ft Speed until end next turn; Air:+5 ft Speed; Earth:+1 on STR/CON saves against forced movement. These are alternatives, not cumulative affinities.

**Reviewed overlay:** Ice slow: SOURCE next regular END. Enhanced Attunement replaces5 with10, not another slow.

## class-card:shaman:shaman.hero.theurgist.elemental-chorus

Classification: **STATE**. Source: `data/public/class_playtests/shaman.json` / `shaman.hero.theurgist.elemental-chorus`. SHA256 `9b3fc059fd54655db96ffe05b822859aa9b0019583161c412efeac74dc29d366`.

Application components: `shaman.elemental-chorus.slow`.

**name:** Elemental Chorus

**activation:** Action

**cost:** 8 RP; 1 long-rest use

**rangeAndTarget:** Four spirits in 10 ft-radius zone within 30 ft

**duration:** Concentration, 3 of your turns

**frequency:** 1/long rest

**effect:** Summon a single Chorus package: four visible spirits share HP 4 L, AC 12+PB, immobile. Bonus Action command pulses up to 3 enemies: DEX save S d6 chosen affinity damage half; one failed target Speed-10 ft until end next turn. Four spirits do not make four separate attacks.

**Reviewed overlay:** Slow: SOURCE next regular END, correcting earlier discussion.

## class-card:shaman:shaman.hero.soothsayer.balanced-elements

Classification: **HOOK**. Source: `data/public/class_playtests/shaman.json` / `shaman.hero.soothsayer.balanced-elements`. SHA256 `bf68f8b1d4057696f4b10d131c0c06367142432fbd60f1aeddd87f5d42b0cc24`.

Application components: None applied directly by this binding..

Modifies/authorizes later application: `dragoon.drakestorm-dive.cold-slow`, `dragoon.elemental-lance.cold-slow`, `mage.cascade-storm.cold-slow`, `mage.cold-focus.flat`, `mage.cold-focus.glacier`, `mage.elemental-fusion.slow`, `ordinary.frost-arrow.slow`, `ordinary.ray-of-frost.slow`, `shaman.elemental-affinity.ice-slow`, `shaman.elemental-chorus.slow`, `shaman.frost-totem.slow`, `shaman.ice-wisp.speed-zero`.

**name:** Balanced Elements

**activation:** Passive

**cost:** 0

**rangeAndTarget:** Your own elemental slowing/burning effect

**duration:** As modified

**frequency:** Once/turn

**effect:** Choose one application: add 1 damage to its next Burn tick OR extend a Speed reduction until end target's following turn. Never extends Stunned, silence, concentration duration or whole-Action denial.

**Reviewed overlay:** Owned explicitly classified elemental control may include legal multiclass sources. No Shaman-class-only restriction. Extend from NOW to target following regular end, max with existing endpoint, capped by governing source/concentration maximum; no recursive deadline addition. Actual elemental membership in guide/metadata.

## class-card:thief:thief.hero.shadowblade.vein-cutter

Classification: **STATE**. Source: `data/public/class_playtests/thief.json` / `thief.hero.shadowblade.vein-cutter`. SHA256 `3562354c947dcfcd84791bb543d35adf69344569ae8f62568b01c9ad49e23838`.

Application components: `thief.vein-cutter.attack-damage-penalty`, `thief.vein-cutter.bleed`, `thief.vein-cutter.slow`.

**name:** Vein Cutter

**activation:** Triggered

**cost:** One dose

**rangeAndTarget:** Enemy critically hit by your weapon

**duration:** Until end next target turn

**frequency:** Once/round

**effect:** Consume prepared poison without its normal recipe effect; target CON save or Bleed 1d4 next 2 turns, Speed-10 ft and-1 next attack damage. Reapplication refreshes; source stack 3 replaced by one bounded package.

## class-card:thief:thief.hero.blackguard.crippling-lash

Classification: **STATE**. Source: `data/public/class_playtests/thief.json` / `thief.hero.blackguard.crippling-lash`. SHA256 `93fd354186009d5cbf2632b2a203ae027fb5348d4ad409cf039fb6bbdcd63e14`.

Application components: `thief.crippling-lash.slow`, `thief.crippling-lash.weapon-hit-damage-penalty`.

**name:** Crippling Lash

**activation:** Action

**cost:** 0

**rangeAndTarget:** One enemy in melee reach

**duration:** Until end next target turn

**frequency:** Recharge 2

**effect:** Make one weapon attack. If it qualifies for Sneak, CON save or Speed-10 ft and-1 damage on next weapon hit for duration. No extra Sneak packet.

## class-card:warrior:warrior.base.brutal-strike

Classification: **STATE**. Source: `data/public/class_playtests/warrior.json` / `warrior.base.brutal-strike`. SHA256 `9d216ec96392b5308e5361954edbba36b597b28338313f50f3c10fef8023a402`.

Application components: `warrior.brutal-strike.stagger`.

**name:** Brutal Strike

**activation:** Action

**cost:** 0

**rangeAndTarget:** One creature within your weapon reach

**duration:** Instantaneous; Stagger until end of target's next turn

**frequency:** Recharge 1 round

**effect:** Brutal Strike. Make one melee weapon attack using its normal ability. On hit add S d6 damage of the weapon's type. The target makes a Constitution save; on failure it is Staggered, taking -1 on attack rolls and -5 feet Speed until the end of its next turn. This is not a full-turn denial.

**Reviewed overlay:** Custom -1 attacks/-5Speed only; not Core Staggered. classification.staggered for named readers/removers. Strongest same-style attack penalty, no addition with Monk version.

## class-card:warrior:warrior.arch.mutation-overload

Classification: **STATE**. Source: `data/public/class_playtests/warrior.json` / `warrior.arch.mutation-overload`. SHA256 `17434e4d9492799006297db7be8c411a853a0c7b5781ed727b0c457b5a2a77f9`.

Application components: `warrior.mutation-overload.backlash`.

**name:** Mutation Overload

**activation:** Bonus Action

**cost:** +2 Strain

**rangeAndTarget:** Your currently active mutations

**duration:** 2 rounds; backlash until end of following turn

**frequency:** 1/short rest

**effect:** Mutation Overload. For 2 rounds, enhance each currently active mutation once: an AC, DR, attack, save or flat-damage bonus increases by 1; a movement or reach bonus increases by 5 feet; or one mutation damage/healing roll gains +1d4. Immunities, target counts, resource generation and action grants cannot be increased. When Overload ends, you suffer -1 on attack rolls and saving throws and -5 feet Speed until the end of your next regular turn. This activation is illegal if +2 Strain would exceed the Strain cap.

## class-card:warrior:warrior.supplement.stonecore

Classification: **STATE**. Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.stonecore`. SHA256 `0861e6a1f9f25502958f016c7d0e9664b8bbfbf4ce936f5214601681eac72ad7`.

Application components: `warrior.stonecore.speed-side-effect`.

**name:** Stonecore

**activation:** Via Serum Injection

**cost:** Dose consumption and normal Strain

**rangeAndTarget:** Injected creature

**duration:** 3 rounds

**frequency:** Per prepared dose

**effect:** Gain +2 AC and immunity to forced movement or knockback from creatures no more than one size larger. Side effect: Speed -10 feet. Serum Tolerance suppresses the Speed penalty.

**prerequisite:** Prepared serum dose

## class-card:warrior:warrior.supplement.hypermutation-spike

Classification: **STATE**. Source: `data/public/class_playtests/warrior.json` / `warrior.supplement.hypermutation-spike`. SHA256 `7ddd706203f3d829ce31a8cd88b34cc00d75c197a96d85f9a471e6e0a379c169`.

Application components: `warrior.hypermutation-spike.speed-floor`.

**name:** Hypermutation Spike

**activation:** Triggered

**cost:** Feat choice

**rangeAndTarget:** Self

**duration:** For one Butcherform activation

**frequency:** 1/long rest

**effect:** When Butcherform Chassis activates, extend its maximum duration from 3 rounds to 5. During that activation you are immune to Stunned and your Speed cannot be reduced below half its normal value.

**prerequisite:** Warrior 16; Butcherform Chassis equipped; eligible feat grant

**Reviewed overlay:** Snapshot each possessed movement mode ordinary sheet Speed, including currently qualifying persistent passive modifiers. Exclude temporary/systemic changes. Half-baseline floor after numeric penalties, no explicit zero/absent-mode/movement-prohibition bypass. Incapacitated itself does not set Speed0 and floor grants no Actions.

