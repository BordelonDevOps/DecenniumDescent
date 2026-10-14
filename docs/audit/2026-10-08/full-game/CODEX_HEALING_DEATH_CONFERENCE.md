# Healing, death replacement and resurrection source conference

This is the next bounded interface pass. The packet preserves 74 class cards, 5 class-engine passages and 6 ordinary spell catalog objects. Some matches are exclusions or bookkeeping. None of the six ordinary spells is operational yet. Please classify each supplied source and resolve the following questions against its exact text. Preserve original cards and distinguish recovered rules from NEW integration decisions.

1. **Separate the procedures.** Distinguish living zero-HP recovery, ordinary HP healing, direct HP-setting/state recovery, minimum-HP prevention, would-die replacement, actual resurrection and companion reconstruction. A title saying “revive” does not establish which occurs. Give a deterministic event order, including source-specific reaction windows, competing replacements and spent costs. Use the closed Core damage/Wound/death procedure below as the starting contract.

2. **HP floors versus HP gain.** Redundant Organs and Last King's Gift say to remain at 1 HP instead of dropping to zero. Does that prevent HP loss under Decay or another HP-gain prohibition? Does it work when already at zero? Phoenix Rebirth and Unyielding Light explicitly regain HP after damage. Mercy Veil and Thousand Petals impose damage floors. Resolve massive-damage Instant Death, the raw post-temp-HP Wound threshold, a fatal Wound save at three Wounds, concentration, reflection and life drain. Does a floor reduce actual damage or preserve the packet while limiting HP loss? State the snapshots used by each calculation. Separate HP-bypassing instant kills, third death-save failures, Exhaustion6 and expedition Strain6.

3. **Class Death Ward is a distinct source.** Ritual of Undeath says the first time a marked ally *would die*, it instead remains at 1 HP and temporarily counts as humanoid and undead. It does not say first drop to zero. Ordinary spell Death Ward has different wording. If a would-die replacement operates at zero while Decay forbids gaining HP, does it fail, or prevent death and leave the creature Stable at zero? The latter would require an explicit NEW bridge, with counter resets, one-use consumption and subsequent recovery defined. Resolve lethal tracks without creating an indefinitely protected six-point state. It cannot repair a destroyed vital body or resurrect someone already dead unless expressly authorized.

4. **Conscious at zero.** Mage Undying Spellform and Oracle False Life BoonIII grant different movement, speech and Action permissions. Do ordinary regular-start death saves still occur? A creature that dies cannot keep acting. Determine Mage's additional death failure at expiry, especially if it became Stable. Healing above zero ends the temporary feature but does not remove unrelated Unconscious/Prone sources. Preserve Oracle's one-choice limitation, Revelation costs and spell risk. Multiple features cannot create extra turns or duplicate Action windows.

5. **Actual resurrection and lethal tracks.** Define willing identity/soul, body sufficiency, time window, corpse location, line of effect and interruption. Preserve each source's actual costs and short windows. Core paragraph506 preserves Wounds, Corruption, debt, legal death and body claims; Oracle class Curse also persists. Three Wounds is Critical, not continuous death. Establish a playable policy for a dead creature still at Exhaustion6 or expedition Strain6, including a recovery route, without silently clearing the tracks. Distinguish an ongoing environmental hazard from a continuous lethal affliction. Does returning at1 HP count as ordinary healing, direct HP gain, or a separate life-state transition? Can a blocked HP gain yield a living Stable-zero creature, or must the resurrection fail? Decay's separate corpse-raising prohibition must remain distinct from its HP-gain prohibition.

6. **Specific revival features.** Bind Cleric Resurrection/Celestial Resurgence/Divine Rebirth, Monk Thousand Petals, Paladin Grace Reversal and other actual revival cards. Clarify Monk's “cannot revive the same creature twice” scope. Translate “since end of your previous regular turn” and other short death windows into preserved markers and out-of-initiative clocks. Divine Rebirth replaces returned HP with half maximum: specify rounding, minimum, effective maximum and interaction with Critical Wound ceiling. Keep resources spent; copying, multiple casters and reused corpses cannot create source-forbidden resource loops.

7. **Healing arithmetic and trigger order.** Order the rolled base amount, permitted bonuses, healing-source multipliers, Corrupted half, Paladin healing halves/flat reductions, current maximum, Critical ceiling, actual HP gained, reserve spending and healing-triggered riders. State how duplicate versus independent reductions stack and where to round. Separate “cannot regain HP,” “ordinary HP healing only” and “passive regeneration only.” Define whether paid pulses, life drain, Hit Dice, rest and direct state recovery are regeneration. The closed periodic rule allows a positive-potential magical heal to invoke an eligible Bleed cure even when actual gain is zero. Mutation Recovery Reserve spends only actual restored HP. Preserve the already-reviewed marks' positive-actual-damage triggers.

8. **Resurrection-blocking auras.** Dirge of Ruin says selected living creatures cannot return from death while inside its aura. Track the selected identity through death rather than making the restriction disappear because the target became a corpse. Clarify moving remains out, ending selection and no retroactive reversal. Oracle Decay's nearby corpse block, the new ordinary spell candidates, soul binding and planar eligibility need exact scopes. A generic healing prohibition does not block temporary HP or stabilization without explicit wording.

9. **Draft the six unfinished ordinary spells.** Produce individually reviewable candidates using the attached Core classes/ranks/RP, cast time, range and components unless a conflict justifies a clearly labelled change. Do not import another game's diamond cost, one-hour casting time or century limit. Ordinary Death Ward is Action/60ft/concentration1min/rank4/7RP and protects the first would-drop-to-zero event. Stitch Fate is Action/120ft/rank8/21RP; an Action cannot retroactively interrupt a completed death, and “dying” is not “dead.” Resurrection is Action/120ft/rank7/17RP; True Resurrection is Action/120ft/rank9/26RP with explicit bodyless return. Fill their actual target, time, returned-HP and consequence gaps. Mass Resurrection Denial's instantaneous metadata conflicts with an ongoing block; define duration, ending and counterplay. Soul Bind needs dying-target eligibility, resistance, the post-death record, ending/cure and player-agency safeguards. Preserve Dissonance, Refrain, Counterspell and concentration rules. All six remain inactive until their individual review and validation pass.

10. **Cures of suppressed records.** An active-effect eligibility hook differs from a cure of a still-present record. Sanctify Ground's reviewed Staggered cleanse includes suppressed records. Current periodic helpers use an active predicate that excludes suppressed/immune records for cure selection. Determine whether Medicine, fire removal and positive-potential healing can cure an existing suppressed Bleed/fire record while its clock continues. Preserve special-cure exceptions, Blood Curse's actual save procedure, family damage arbitration and exact one/all removal scopes. Do not let a supposedly cured source resume merely when temporary immunity ends.

Please give explicit operational decisions and adversarial examples, identify remaining dependencies, and avoid claiming whole-game completion from this bounded source pass.

## Closed Core interface for preservation

```markdown
# Core resolution and injury playtest rules

This is the active provisional integration for rolls, damage, zero HP, Wounds and injuries in the developing campaign candidate. It resolves specific conflicts between approved Core V2, compatible Player Rulebook V6 rules and the retained Gameplay Loop. Original books and alternate procedures remain unchanged. Full conditions, equipment, hazards and recovery integration remain separate work.

Use with [class rules](CLASS_PLAYTEST_RULES.md), [spell rules](SPELL_INTEGRATION_RULES.md) and the [complete coverage ledger](GAME_DEVELOPMENT_COVERAGE.md). The [source conference](../../../../docs/audit/2026-10-08/full-game/CODEX_CORE_RESOLUTION_CONFERENCE.json), [V6 findings](../../../../docs/audit/2026-10-08/full-game/CODEX_CORE_SOURCE_FOLLOWUP.md) and [GPT proposal](../../../../docs/audit/2026-10-08/full-game/GPT_CORE_STATE_AND_INJURY_PROPOSAL.md) preserve the reasoning.

## Which rule applies

The domain authority is [Core Systems Known Descent V2](../../../../books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx). The approved [Player Rulebook V6](../../../../books/player/Decennium_Descent_Player_Rulebook_v6.docx) supplies compatible rules that Core does not replace. This overlay states the selected interpretation or newly authored rule wherever those sources leave a gap. An explicit exception on an operative, reviewed class/spell/item card applies only within its printed scope; a historical alternate or a same-named feature is not an extra grant. This candidate does not promote an entire historical branch.

| Question | Active rule and provenance | Inactive alternate |
|---|---|---|
| Attacks | Core V2: meet AC; natural 1 misses; natural 20 hits and doubles damage dice. | Applying the general Gameplay four-degree roll to attacks. |
| Task checks | Explicitly adopted Gameplay four degrees and natural shifts. | Assuming every critical result creates an unprinted effect. |
| Ordinary saves | Binary meet-DC test; printed failure margins remain literal. Natural 1/20 do not generically shift saves in this candidate. This separation is an integration choice. | Automatic critical saves or natural-result shifts inferred from the task rule. |
| Death-save timing | Core and V6: start of turn; regular-turn-only timing is a provisional guard. | Gameplay end-of-turn saves. |
| Wounds | Core trigger/save, Constitution-save and Hit-Dice-recovery penalties, and three-Wound Critical state. | Gameplay automatic Wound triggers, Hit Dice healing penalty, half Speed and Strain lock. |
| Named Wounded condition | Core paragraph 782 expressly describes the same Wound count, Constitution penalty, Hit Dice recovery and three-Wound Critical state. Apply those records once. | V6 Appendix A paragraphs 9971–9974 give a conflicting temporary condition cleared by magic/rest with Constitution-save disadvantage; Core replaces it here. |
| Stable, instant death, knockout and temporary HP | Compatible recovered V6 rules. | Treating these recovered rules as newly invented. |
| Ordinary Wound treatment | Explicit Gameplay-derived integration below. | Claiming it is original Core wording or ordinary HP healing. |
| Injury table and unresolved thresholds | New provisional choices below, with their search limits stated. | Dropping Core's failure-by-5 consequence because its table was not located. |

## Rolls

Choose the roll type before rolling. Use the actual ability modifier, including negative values, and normal proficiency only when applicable. Existing advantage/disadvantage chooses the higher/lower of two d20s; multiple sources do not stack, and any advantage plus disadvantage cancels. Add other legal modifiers once. Fractions round down unless a rule specifies otherwise. One tile is 5 feet. Class L, S and effect M retain their definitions in the shared class rules.

**Attack:** roll d20 plus the appropriate attack modifier against AC. Meeting AC hits. Natural 1 always misses; natural 20 always hits and critically doubles damage dice, not flat modifiers. Beating AC by 10 is not a critical hit. An explicit broader critical range does not stack with another; use the broadest eligible range. In this overlay, a natural result below 20 in that range must still meet AC unless the feature expressly says it always hits.

**Task, skill or tool check against a fixed DC:** total at least DC+10 is Critical Success; at least DC is Success; at most DC-10 is Critical Failure; other totals below DC are Failure. Natural 20 then improves one degree and natural 1 worsens one, bounded at either end. A task printing only success/failure collapses the two upper degrees to success and two lower degrees to failure; no extra consequence is invented. A natural 20 can still fail an otherwise impossible check, and a natural 1 with sufficient modifiers can still succeed.

**Saving throw:** total at least DC succeeds; otherwise it fails. Natural 1 and 20 have no generic special outcome. A printed failure by 5 or 10 compares the final total with the DC; it does not add an unprinted critical-save system. Death saves are the specific exception below.

**Opposed check, new provisional tie rule:** compare final totals. Higher wins; an exact tie leaves the existing state unchanged, so the initiating creature fails to change it. Do not turn task natural shifts into hidden numeric modifiers. A maneuver explicitly printing degree outcomes must specify how those apply.

## Resolve a damage event

Resolve each genuinely separate hit or damage event once. Do not split one packet to multiply Wound saves or combine separate hits merely to cross a threshold. Feature-specific prevention that acts before damage or before reaching zero resolves at its printed timing first.

1. Resolve attack/save, damage and applicable defenses. The remaining nonnegative amount is **resolved damage**.
2. Record HP, Wounds and zero-HP state before the event. Remove temporary HP first. **Post-temp damage = resolved damage minus temporary HP absorbed.** Keep this amount even when it exceeds current HP; floor the resulting current HP at zero.
3. Check V6 Instant Death. If post-temp damage minus HP before the hit is at least maximum HP, the creature dies. For a creature already at zero, this is post-temp damage at least maximum HP. Stop: there is no Wound save, death-save failure or successful knockout from that event.
4. Otherwise, a living creature makes one Wound save if it dropped from positive HP to zero, if **2 × post-temp damage is at least maximum HP**, or if the effect actually inflicts Maiming. Overlapping triggers still cause only one save. The post-temp threshold and one-save rule are new provisional interpretations. Maiming is an independent trigger even when temporary HP absorbs all ordinary damage; immunity to Maiming itself still applies.
5. Make a Constitution save against **max(10, floor(post-temp damage / 2))**. Use pre-event Wounds for the -1-per-Wound penalty. Maiming with zero post-temp damage uses DC 10. A Wound gained now cannot penalize the roll that created it.
6. A success adds no Wound. A failure that began with zero, one or two Wounds adds exactly one; failure by 5 or more also gives that Wound one Injury. A failure that began with three Wounds kills the creature instead: no fourth Wound and no Injury roll. Stop processing later living-target consequences if dead.
7. If the creature was already at zero before this event and post-temp damage is positive, end Stable. A creature using death saves adds one failure, or two for a critical hit; three failures kill it. An ordinary creature that does not use death saves dies instead, without starting death counters. A hit from positive HP to zero does not also cause a same-packet death failure.
8. If this event newly reduces positive HP to zero, a valid melee knockout makes the surviving creature Stable. Otherwise a character/significant NPC using death saves begins dying; an ordinary monster dies. A previously Stable creature whose temporary HP absorbed all damage remains Stable unless an independent Maiming result killed it. The Director identifies significant NPCs consistently. Knockout cannot override Instant Death or a fatal Wound save.

Core's Maiming and Wound trigger rules remain subject to an actual feature's eligibility. The reference helper receives already legal events; it does not grant every attack Maiming or a damage-prevention exception.

## Zero HP and recovery

A living character at zero HP is Unconscious. Core's condition already includes Incapacitated, unawareness, dropping held items and falling Prone; an adjacent hit is critical as specified there. Healing does not silently remove other independent causes of Unconscious or Prone.

While dying, make one death save at the **start of each regular initiative turn**. Roll d20 without modifiers unless a feature specifically modifies death saves. Natural 20 restores 1 HP; natural 1 adds two failures. Other results of 10 or more add one success; 9 or less add one failure. Three successes make the creature Stable; three failures make it Dead. Extra turns and Actions add no extra death saves. Stable or Dead creatures do not roll them.

Regaining positive HP or becoming Stable resets both counters. Temporary HP does not raise normal HP, end Unconscious or reset counters. Fully absorbed damage does not end Stable or add a death failure in this provisional interpretation. Independent Maiming can still cause its Wound save.

**Stabilize:** an Action and DC 10 Wisdom (Medicine) check, or an Action using one healer's-kit use automatically, stabilizes a living dying creature at zero. It remains Unconscious and makes no death saves. Roll 1d4 once when it becomes Stable and record its absolute recovery time that many hours later. If still Stable then, it regains 1 HP. Damage reaching normal HP cancels that deadline and resumes dying with the appropriate failures. Rest and Stable recovery use the same elapsed clock, so four hours of recovery inside an eight-hour Watch do not cost twelve hours. A later rest does not separately replay the Stable healing event.

**Dead:** ordinary healing and stabilization do not restore life. Resurrection must satisfy its own willing-soul, body, time, cost and target rules. It does not automatically remove Wounds, Corruption, debts, legal death or claims upon the body. Corpses cannot supply repeated resource triggers.

## Wounds and Critical state

Each Wound imposes **-1 Constitution saves** and reduces the normal maximum number of Hit Dice recovered per long rest by one, to a minimum of zero. It does not reduce each healing die. The broader recovery rules own the normal recovery maximum and rest legality.

At three Wounds the creature is **Critically Wounded**: Speed is reduced by 10 feet, to minimum zero, and the next failed Wound save is fatal. The failure that first raises two Wounds to three is not that later failure. Core's named **Wounded** condition (paragraph 782, preserved in [the 28-condition source register](../../data/playtest/core_condition_sources.json)) explicitly summarizes these same Wounds; it does not add duplicate penalties. Its conflicting V6 predecessor is inactive in this overlay. This individual source comparison does not complete the remaining condition audit.

**New provisional healing ceiling:** while Critical, healing cannot increase HP above **max(1, maximum HP - 1)**. Maximum HP itself does not change. Gaining the third Wound does not immediately remove existing HP; a later attempted heal also cannot reduce HP. The minimum of one permits recovery when maximum HP is one and is an explicit exception to “cannot regain full HP.” Removing enough Wounds to leave Critical removes its Speed penalty and ceiling, but does not itself heal HP.

## Linked injuries

The inspected eight approved books and current text sources reference an Injury table, but no actual table was located. The full Wound/Medicine searches of both Core editions found no alternate general treatment procedure. Those are search limits, not proof about every archive. This **new provisional d6 table** supplies Core's failure-by-5 consequence until a reviewed replacement is adopted.

| d6 | Injury | Exact penalty |
|---:|---|---|
| 1 | Concussion | -1 Initiative and Perception checks. |
| 2 | Offensive Trauma | -1 attack rolls. |
| 3 | Mobility Trauma | All non-teleport Speeds reduced by 5 feet, minimum zero. |
| 4 | Fine-Motor Trauma | -1 tool checks and Dexterity checks primarily manipulating an object, mechanism, lock or device. |
| 5 | Exertion Trauma | -1 Strength and Dexterity ability checks. |
| 6 | Cognitive Trauma | -1 Intelligence, Wisdom and Charisma ability checks. |

Link each result to the one Wound just gained. An Injury never adds another Wound. Record duplicate results separately, but identical penalties apply once. Different Injury penalties affecting the same roll or stat also use only the strongest Injury penalty. V6 paragraph 7925 explicitly calls Initiative a Dexterity check, so both Concussion and Exertion Trauma can apply, with only one -1 Injury penalty. An injury affects future Initiative rolls, never an order already established. This does not change other Initiative procedures. Mobility Trauma can coexist with the separate Core Critical Speed penalty, applying both once. Other effects keep their own stacking rules.

Removing a Wound ends its linked Injury. A duplicate penalty persists while any remaining Wound carries that result. When a removal effect names no specific Wound, the patient chooses existing records. Injuries cause no extra damage, Actions lost, disadvantage, maximum-HP reduction or resource triggers. Describe equivalent trauma for unusual anatomy while retaining the printed penalty.

## Ordinary Wound treatment

This is an explicit Gameplay-derived integration. A living patient with at least one Wound receives eight elapsed hours of treatment with a medical kit and **one Supply**. **New provisional cost decision:** commit and consume that Supply once when treatment begins, on every attempt, even on success or interruption; no extra Supply is charged for failure. The retained Gameplay text requires one Supply and explicitly mentions consumption on failure but does not clearly settle success refunds. This candidate deliberately settles the ambiguity as a cost on every attempt, rather than claiming that interpretation is recovered source wording. Choose the Wound being treated before beginning. At completion roll Wisdom (Medicine) against the applicable tier DC: I 12, II 13, III 15, IV 16, V 18, VI 19. Unverified higher-tier procedures remain with the later Director/hazard pass.

Critical Success removes the chosen Wound and one other existing Wound chosen by the patient, if available. Success removes the chosen Wound. Failure removes none. Critical Failure removes none and gives the **patient** one Strain; identifying the patient is a new clarification. Associated Injuries end with removed Wounds. Treatment itself does not restore HP. Whether treatment qualifies as a legal rest is determined separately; the active healer cannot automatically claim an eight-hour Rest Watch while treating. Count the eight hours once, with any Stable recovery occurring on the same clock.

## Verification scope

`tools/core_playtest_rules.py` is a reference for roll types and the damage/Wound/death state transitions. It does not select legal Actions or targets, run all class reactions, roll damage, apply every defense, adjudicate all conditions, run medical-kit/Supply inventories or simulate a campaign clock. Its callers supply legal events and actual elapsed time. `tools/validate_core_playtests.py` reports named regression cases and sampled state invariants. Passing checks do not establish human balance or completion of the remaining game systems.

```

## Exact current class procedures

```json
[
  {
    "kind": "class-engine",
    "owner": "cleric",
    "path": "data/public/class_playtests/cleric.json",
    "engineIndex": 7,
    "text": "Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction.",
    "textSha256": "bb84e1b0f1d02ca1f307edee719b2e66036799f2367b1b93511681a7f95dd455"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.base.healing-rite",
    "name": "Healing Rite",
    "activation": "Action",
    "cost": "2 RP",
    "rangeAndTarget": "One living ally within 30 feet",
    "duration": "Instantaneous",
    "frequency": "At will while RP remains",
    "effect": "Healing Rite. Tags: rite, healing. One living ally regains S d8 + M HP. It cannot restore a dead creature or remove Wounds. Consecrated Ground and appropriate Invocation Path bonuses may modify this healing.",
    "prerequisite": null,
    "sourceObjectSha256": "20a27516ae922475d5979c529d88a5f83d4a29cff8e8ce063b46f1009be73e2f"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.saint.divine-rebirth",
    "name": "Divine Rebirth",
    "activation": "Triggered",
    "cost": "0",
    "rangeAndTarget": "One ally revived by your Cleric feature",
    "duration": "Instantaneous plus temporary HP for 1 minute",
    "frequency": "1/long rest",
    "effect": "Divine Rebirth. Tags: saint, resurrection. When one of your Cleric features returns an ally from death, you may use Divine Rebirth. That ally returns with half its maximum HP instead of the feature's normal returned HP and gains S + M temporary HP for 1 minute. It removes no Wounds and cannot affect a creature that was not actually dead.",
    "prerequisite": null,
    "sourceObjectSha256": "0911a56a90621bfce24642033cfd99929553c077fa641efacc48d90d4b94e15a"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.saint.unyielding-light",
    "name": "Unyielding Light",
    "activation": "Triggered",
    "cost": "0",
    "rangeAndTarget": "Up to six living party members within 30 feet, including you",
    "duration": "Instantaneous",
    "frequency": "1/long rest",
    "effect": "Unyielding Light. Tags: saint, emergency, healing. When one damage event would leave every conscious living party member within 30 feet at 0 HP, resolve that damage, then before ordinary death-save progression each qualifying living creature at 0 HP regains floor(maximum HP/3), minimum 1. It cannot revive a creature killed outright and removes no Wounds. This one emergency trigger may resolve even if that event incapacitates you, provided you remain alive; it grants no other actions while incapacitated.",
    "prerequisite": null,
    "sourceObjectSha256": "2b13f1c09c2c7fba28eb3ac046a34ff52f8a829eafac020aa33b762a96d4236d"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.saint.celestial-resurgence",
    "name": "Celestial Resurgence",
    "activation": "Action",
    "cost": "5 Conviction + 10 RP",
    "rangeAndTarget": "Up to six allied corpses within 30 feet that died during the previous 3 rounds",
    "duration": "Instantaneous",
    "frequency": "1/long rest",
    "effect": "Final Miracle — Celestial Resurgence. Tags: saint, finale, resurrection, rite. Each legal target returns to life at 1 HP. The body must be sufficiently present to sustain life. This removes no Wounds, curses or other death consequences. Divine Rebirth may modify one returned ally if available. The Conviction expenditure can vent Dissonance once under the common rule.",
    "prerequisite": null,
    "sourceObjectSha256": "67fbbe3e612fe1dbe47ab927928e4bb8c392086d02926c0059cf915f6d309309"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.saint.mass-healing-light",
    "name": "Mass Healing Light",
    "activation": "Action",
    "cost": "5 RP",
    "rangeAndTarget": "Up to six living allies within 30 feet",
    "duration": "Instantaneous",
    "frequency": "Recharge 3 rounds",
    "effect": "Mass Healing Light. Tags: saint, healing. Roll S d8 + M once. Each target regains that amount. A target below half maximum HP when chosen regains an additional 1d8 HP. Roll that bonus once and apply it to all qualifying targets. This cannot revive the dead or remove Wounds.",
    "prerequisite": null,
    "sourceObjectSha256": "dbb502b5ecb5d64d0973a9df82f770cdb8af28300d09a7f6f978d3fef13c2009"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.saint.resurrection",
    "name": "Resurrection",
    "activation": "Action",
    "cost": "3 Conviction + 10 RP",
    "rangeAndTarget": "One allied corpse you touch that died within the previous 1 minute",
    "duration": "Instantaneous",
    "frequency": "1/long rest",
    "effect": "Resurrection. Tags: saint, resurrection, rite. Return the target to life at 1 HP and grant it 2 S + M temporary HP for 1 minute. It gains no removed Wounds and receives no restored expended resources beyond what another rule explicitly provides. A missing vital body prevents the effect. The Conviction expenditure can vent Dissonance once.",
    "prerequisite": null,
    "sourceObjectSha256": "c30ea74832ad72360d7e3dfff95ca1b7514996ae818b04aa1b59928e93cdf67d"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.cultist.blasphemous-tongue",
    "name": "Blasphemous Tongue",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Enemies affected by your Sacrament",
    "duration": "Until the next Sacrament pulse or effect end",
    "frequency": "Once per target per pulse",
    "effect": "Blasphemous Tongue. Tags: cultist, sacrament, doomed. At each pulse of your Sacrament, each enemy affected by that pulse makes a Wisdom save. On failure it becomes Doomed until the next pulse. While Doomed, HP healing it receives is reduced by S+M, minimum 0, and each positive timed buff on it counts down one additional round at the end of its turn. Repeated failures refresh rather than stack.",
    "prerequisite": null,
    "sourceObjectSha256": "793dec5aa60dff80f8da02ed52a55b22c28c0b8975ca949d9dc9bf4374e6f1c6"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.cultist.rite-of-the-crimson-choir",
    "name": "Rite of the Crimson Choir",
    "activation": "Action",
    "cost": "5 Conviction + 8 RP",
    "rangeAndTarget": "Four unoccupied spaces within 30 feet",
    "duration": "Concentration, maximum 3 rounds",
    "frequency": "1/long rest",
    "effect": "Final Miracle — Rite of the Crimson Choir. Tags: cultist, finale, summon, rite. Summon four spectral fanatics. Each has AC 14, 10 HP, Speed 30 feet and cannot take Reactions. Spend one Bonus Action on your regular turn to command the Choir; this explicitly priced Finale permits up to four surviving fanatics to each move up to its Speed and make one melee spell-like attack using your Cleric technique attack bonus against an enemy within 5 feet; on hit it deals 1d6+S necrotic damage and you regain 1 HP, maximum 4 HP per round from the Choir. When a fanatic reaches 0 HP, when concentration ends or after the third round, it explodes; enemies within 5 feet make Dexterity saves, taking 1d6 necrotic on failure or half on success. Fanatics grant no XP, loot, corpse, resurrection target or Conviction. The Conviction expenditure can vent Dissonance once.",
    "prerequisite": null,
    "sourceObjectSha256": "8a0609352a89fd9dee65f38e363372e1dc9bc50876b68e3e90b2e7761ad553bf"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.cultist.blood-sacrifice",
    "name": "Blood Sacrifice",
    "activation": "Bonus Action",
    "cost": "Lose S+M actual HP from yourself or one willing ally within 5 ft",
    "rangeAndTarget": "Self or one willing ally within 5 feet",
    "duration": "Empowerment lasts until end of your next regular turn",
    "frequency": "1/short rest",
    "effect": "Blood Sacrifice. Tags: cultist, sacrifice, conviction. The chosen creature loses S+M actual HP; this loss cannot be reduced, redirected or transferred and cannot reduce it below 1 HP. The donor must have strictly more current HP than this cost before activation; otherwise it is illegal. You gain 1 Conviction. Your next damaging or healing Rite or Invocation before the end of your next regular turn adds 1d8 to one rolled damage or healing component. A creature must be willing unless the target is you.",
    "prerequisite": null,
    "sourceObjectSha256": "073e2e574467aaae7193dfd80d27b74c4b3ccc4db41a45a4d59ab3208ad335fe"
  },
  {
    "kind": "class-card",
    "owner": "cleric",
    "id": "cleric.hero.cultist.ritual-of-undeath",
    "name": "Ritual of Undeath",
    "activation": "Action",
    "cost": "3 Conviction + 6 RP",
    "rangeAndTarget": "One eligible corpse within 30 feet or one living ally within 30 feet",
    "duration": "Mode-dependent",
    "frequency": "1/long rest",
    "effect": "Ritual of Undeath. Tags: cultist, undead, rite. Choose one mode. Corpse Servant: one humanoid corpse dead no more than 1 minute rises for 3 rounds as a temporary thrall with AC 13, 10 HP, Speed 30 feet and one attack only when you spend your shared companion Bonus Action command using your Cleric technique attack bonus; on hit it deals S d6 necrotic. The thrall disappears at 0 HP or when duration ends and grants no XP, loot, new corpse, Conviction or resurrection target. Death Ward: one living ally is marked for 1 minute; the first time it would die during that duration, it instead remains at 1 HP and counts as both humanoid and undead until the end of its next turn. Neither mode removes Wounds. The Conviction expenditure can vent Dissonance once.",
    "prerequisite": null,
    "sourceObjectSha256": "3a49348b309930d66ab43fb15262c7062c7849daca1a4939beb6d27d22f9bea1"
  },
  {
    "kind": "class-card",
    "owner": "dragoon",
    "id": "dragoon.hero.dragon-guardian.bastion-descent",
    "name": "Bastion Descent",
    "activation": "Action",
    "cost": "5 Momentum; 1 long-rest use",
    "rangeAndTarget": "Leap within 30 ft; up to 6 allies within 15 ft of landing",
    "duration": "Instant; protection until start next turn",
    "frequency": "1/long rest",
    "effect": "Land in empty space. Chosen allies gain 4d8+M temporary HP and may end Frightened or Poisoned. They gain resistance to the next damage instance before your next turn. No healing, resurrection or removal of Wounds.",
    "prerequisite": null,
    "sourceObjectSha256": "e1005686e829ecea6d245c9627f8a22cb38f30ab26ee0c4daa97837ac5e58671"
  },
  {
    "kind": "class-card",
    "owner": "mage",
    "id": "mage.hero.archmage.harmonized-core",
    "name": "Harmonized Core",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "One ally within 30 feet",
    "duration": "Temporary HP until lost or replaced",
    "frequency": "At most once per turn",
    "effect": "Harmonized Core. Tags: archmage, support. After one of your damaging Mage spells deals damage, choose one ally within 30 feet. It gains temporary HP equal to 10% of one target's unmodified rolled damage dice total from that spell, rounded down, minimum 1 and maximum S+M. This is not HP healing and cannot trigger healing features or Echo-style repetitions.",
    "prerequisite": null,
    "sourceObjectSha256": "7d1df6cb40daec1f188736404c612c8f9a7305f874f3d21a7f335706b17fea64"
  },
  {
    "kind": "class-card",
    "owner": "mage",
    "id": "mage.hero.lich.undying-spellform",
    "name": "Undying Spellform",
    "activation": "Triggered",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Until end of your next regular turn",
    "frequency": "1/long rest",
    "effect": "Undying Spellform. Tags: lich, undead, death. When damage reduces you to 0 HP without killing you outright, remain conscious and able to take Actions until the end of your next regular turn. You remain at 0 HP, cannot benefit from voluntary movement faster than half Speed, and still suffer ordinary consequences of further damage. If still at 0 HP when the effect ends, become unconscious and suffer one failed death save. Healing above 0 ends this feature early.",
    "prerequisite": null,
    "sourceObjectSha256": "f9eb71c6354a879da6fb752283a2e78cf2330465e97605dae15c939ecf413cea"
  },
  {
    "kind": "class-card",
    "owner": "mage",
    "id": "mage.hero.lich.soul-reservoir",
    "name": "Soul Reservoir",
    "activation": "Triggered",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Instantaneous",
    "frequency": "At most once per turn and at most S times per encounter",
    "effect": "Soul Reservoir. Tags: lich, resonance, damage-over-time. During a real encounter, when a hostile creature takes damage from a damage-over-time effect created by one of your Mage spells, restore 1 RP, never above maximum. The same damage event cannot restore more than 1 RP. Damage to allies, summons, trivial creatures or your own companions does not qualify.",
    "prerequisite": null,
    "sourceObjectSha256": "ec8ad792a975cf5bef6d4b070ad1d5e9a977b33ad1f305c9a7bd6a982170ef61"
  },
  {
    "kind": "class-card",
    "owner": "mage",
    "id": "mage.hero.lich.resonance-to-flesh",
    "name": "Resonance to Flesh",
    "activation": "Action",
    "cost": "Variable conversion",
    "rangeAndTarget": "Self",
    "duration": "Instantaneous",
    "frequency": "1/short rest",
    "effect": "Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions.",
    "prerequisite": null,
    "sourceObjectSha256": "5692ac39a7de506bcf79cfcb7273630cf1f18c27e6d663ae380f764b78e3e8b2"
  },
  {
    "kind": "class-card",
    "owner": "mage",
    "id": "mage.hero.lich.soulbound-ritual",
    "name": "Soulbound Ritual",
    "activation": "Action",
    "cost": "5 RP",
    "rangeAndTarget": "One of your destroyed bound elite undead companions within 30 feet or its inert binding token",
    "duration": "Instantaneous",
    "frequency": "1/long rest",
    "effect": "Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again.",
    "prerequisite": null,
    "sourceObjectSha256": "402e1f7d3575a535865294094b40a0e028c23dff18e64dadc511f20340bc7b0a"
  },
  {
    "kind": "class-engine",
    "owner": "mirrorsage",
    "path": "data/public/class_playtests/mirrorsage.json",
    "engineIndex": 5,
    "text": "Focus Point is a separate resource: when Mimicry Focus is known, receive 1 at encounter start, maximum 1, lost at encounter end. It can modify one Echo without generating another release, recapture or resource refund. No stacking damage doublings; use the printed modest die/range boost. Healing/support copies always consume RP and cannot restore RP or duplicate limited-use features.",
    "textSha256": "5d438f2023c519d89d890af09fc094f010346755f3bb3577d94a6463558865f6"
  },
  {
    "kind": "class-card",
    "owner": "mirrorsage",
    "id": "mirrorsage.hero.light-weaver.radiant-archive",
    "name": "Radiant Archive",
    "activation": "Action",
    "cost": "RP for 3 support Echoes; consume all 3; 1 long-rest use",
    "rangeAndTarget": "Up to 3 legal allies within 30 ft",
    "duration": "Instant/shield 1 minute",
    "frequency": "1/long rest",
    "effect": "Release three stored Mend/Ward records as ONE package; assign each to one ally. No ally receives more than two components and temporary HP never stack. All costs paid; no extra release or resurrection. Missing records cannot be invented.",
    "prerequisite": null,
    "sourceObjectSha256": "bed8021f25da9ec4a1f8d3da1806e0463bdf2177c6020e641e4758474ec78be6"
  },
  {
    "kind": "class-card",
    "owner": "mirrorsage",
    "id": "mirrorsage.hero.light-weaver.divine-reflection",
    "name": "Divine Reflection",
    "activation": "Reaction",
    "cost": "2 RP; 1 long-rest use",
    "rangeAndTarget": "Willing allied caster within 30 ft just used an eligible healing/protection spell",
    "duration": "Store until spent",
    "frequency": "1/long rest",
    "effect": "Capture a Mend or Ward profile of rank at most your learnable rank into empty slot. This explicit exception permits an allied source but excludes resurrection/resource/action generation. No extra captured use for the ally and no copying a copy.",
    "prerequisite": null,
    "sourceObjectSha256": "db590cbdf89b887f256428708cbf767fcd916e2dc06e5eb5268e23f69b60816b"
  },
  {
    "kind": "class-engine",
    "owner": "monk",
    "path": "data/public/class_playtests/monk.json",
    "engineIndex": 16,
    "text": "Healing from Monk cards cannot exceed maximum HP, restore the dead or remove Wounds unless explicitly stated. Permanent HP recovery and Ki generation cannot be farmed outside encounters. Resurrection effects are explicitly limited-use. No Monk card can instantly kill a target merely because a descriptive source used language such as Death Touch; death continues to follow the game's ordinary damage and dying rules.",
    "textSha256": "35f0120ff484cecb5d18360f6532891d2de393ba4d2b5e03a9961b7e2ab07a44"
  },
  {
    "kind": "class-card",
    "owner": "monk",
    "id": "monk.base.crane-stance-support",
    "name": "Crane Stance (Support)",
    "activation": "Passive",
    "cost": "0 for stance; healing costs 1 Ki and 1 RP",
    "rangeAndTarget": "Self; one ally within 15 feet for healing rider",
    "duration": "While active",
    "frequency": "Automatic core stance",
    "effect": "Crane Stance. Tags: stance, support. While unarmored, whenever you move at least 15 feet on your turn, gain +1 AC until the start of your next turn. HP healing you receive from another creature gains +S HP once per round. When you begin an unarmed strike at exactly 5 Ki and hit, spend 1 Ki and 1 RP; you and one living ally within 15 feet each regain S+M HP, at most once per turn.",
    "prerequisite": null,
    "sourceObjectSha256": "e674e9a4ae8aa0f0d52cd371b86e9173b9ba7f00a2447db64e31c14f44b42314"
  },
  {
    "kind": "class-card",
    "owner": "monk",
    "id": "monk.hero.enlightened-master.breath-of-the-thousand-petals",
    "name": "Breath of the Thousand Petals",
    "activation": "Action",
    "cost": "5 Ki + 5 RP",
    "rangeAndTarget": "Up to six allies within 20 feet",
    "duration": "Until start of your next regular turn",
    "frequency": "1/long rest; automatic Hero Final",
    "effect": "Final — Breath of the Thousand Petals. Tags: hero, enlightened, final, resurrection, weave. Living or Downed allies in range regain 3 S d8+M HP. Up to two allied creatures that died since the end of your previous regular turn return to life at 1 HP if their bodies can sustain life. Until the start of your next turn, affected living allies cannot be reduced below 1 HP by damage, though instant-death effects still function. It removes no Wounds and cannot revive the same creature twice.",
    "prerequisite": null,
    "sourceObjectSha256": "ef8e3a96a396ed3d48f95c0e4138b0eae186fe297b746cae0c83c40004fa508e"
  },
  {
    "kind": "class-card",
    "owner": "monk",
    "id": "monk.hero.enlightened-master.healing-touch",
    "name": "Healing Touch",
    "activation": "Action",
    "cost": "2 Ki + 1 RP",
    "rangeAndTarget": "One living creature you touch",
    "duration": "Instantaneous",
    "frequency": "Recharge 2 rounds",
    "effect": "Healing Touch. Tags: hero, enlightened, healing, weave. The target regains S d8+M HP and may immediately repeat one saving throw against Poisoned or disease if that effect normally permits repeated saves. This does not resurrect, remove Wounds or automatically cure disease. It is a minor Weave technique; the common extra-Ki payment may prevent its 1 Dissonance.",
    "prerequisite": null,
    "sourceObjectSha256": "ca275c05e4d877cf61c5267324d7cc9026d4e5cce39428e9821125f72d92555b"
  },
  {
    "kind": "class-card",
    "owner": "monk",
    "id": "monk.hero.enlightened-master.circle-of-harmony",
    "name": "Circle of Harmony",
    "activation": "Action",
    "cost": "2 Ki + 3 RP to start; 1 RP maintenance",
    "rangeAndTarget": "10-foot-radius fixed zone centered within 30 feet",
    "duration": "Concentration, maximum 3 Monk turns",
    "frequency": "Recharge 4 rounds",
    "effect": "Circle of Harmony. Tags: hero, enlightened, healing, zone, weave, sustained. On start and each paid Bonus Action maintenance pulse, up to three living allies in the zone regain S d6+M HP. Maximum 3 pulses. A creature receives this named effect at most once per round. It removes no Wounds and cannot restore the dead.",
    "prerequisite": null,
    "sourceObjectSha256": "df3b3c65b152fd7b3a217eac2e551b3fc473a00b9704fcbb98bfe0dc9611c4bd"
  },
  {
    "kind": "class-card",
    "owner": "monk",
    "id": "monk.hero.enlightened-master.shared-breath",
    "name": "Shared Breath",
    "activation": "Action",
    "cost": "3 Ki + 2 RP",
    "rangeAndTarget": "One willing ally you touch",
    "duration": "Concentration, maximum 3 rounds",
    "frequency": "Recharge 4 rounds",
    "effect": "Shared Breath. Tags: hero, enlightened, link, weave. Link yourself to one willing ally. Once per round when either linked creature takes damage, the other may use its Reaction to take up to S+M of that damage instead; transferred damage cannot be reduced or redirected again. HP healing received by either creature also grants the other S HP once per round. The link ends if you separate by more than 30 feet.",
    "prerequisite": null,
    "sourceObjectSha256": "da2757b79d797600e0823eed7b615b9165e4c9d81c88fbb6affa18018695c52e"
  },
  {
    "kind": "class-card",
    "owner": "monk",
    "id": "monk.hero.way-of-shadow.veinlock-nerve-jab",
    "name": "Veinlock Nerve Jab",
    "activation": "Triggered",
    "cost": "2 Ki",
    "rangeAndTarget": "One creature hit by your unarmed strike",
    "duration": "Maximum 2 rounds",
    "frequency": "Recharge 3 rounds",
    "effect": "Veinlock Nerve Jab. Tags: hero, shadow, attack, control. After an unarmed strike hits, spend 2 Ki. The target makes a Constitution save. On failure it cannot regain HP or finite class resources until the end of its next turn and repeats the save then; failure extends the effect one final round. If you were hidden from it when the strike began, the initial failed save also Silences it until the end of its next turn.",
    "prerequisite": null,
    "sourceObjectSha256": "3bc079fb6588aa9fc7a9c545b06960c886198801a8862db231935f3b48b1247a"
  },
  {
    "kind": "class-engine",
    "owner": "oracle",
    "path": "data/public/class_playtests/oracle.json",
    "engineIndex": 3,
    "text": "Choose exactly ONE Mystery and exactly ONE Curse at Oracle level 1. They are not parallel subclasses that stack. You never gain another Mystery or Curse unless a future explicit retraining or transformation rule says otherwise. Curse limitations are permanent and cannot be removed by ordinary cleansing, curse removal, resurrection or rest.",
    "textSha256": "f6e9c61b425e06da50fb57ca05f565571fbb295f30460b42fe69cca65507121c"
  },
  {
    "kind": "class-engine",
    "owner": "oracle",
    "path": "data/public/class_playtests/oracle.json",
    "engineIndex": 13,
    "text": "Healing from Oracle features cannot exceed maximum HP, resurrect the dead or remove Wounds unless a feature explicitly says so. Temporary HP never stack. Encounter-only regeneration and drain cannot be farmed outside meaningful combat. Corpse effects create no XP, loot, RC or repeatable corpse resources unless expressly stated.",
    "textSha256": "915b1cf2d9327231bf75308605d2e2b72abdce2ce052fdecef493dea663af705"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.shared.oracle-s-burden",
    "name": "Oracle's Burden",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Permanent",
    "frequency": "Automatic at Oracle 2",
    "effect": "Your selected Curse is recognized as an intrinsic Oracle class condition rather than an ordinary removable curse. Remove Curse, cleansing, resurrection and similar generic effects cannot remove or suspend it. Only a feature that explicitly names your Oracle Curse can suppress, transform or replace one of its effects.",
    "prerequisite": "Oracle 2",
    "sourceObjectSha256": "58600e513393987a382f64e53a11dbbf7c82e705ff8afb6e40fe6645dc6f8c02"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.curse.wound-eater",
    "name": "Wound Eater",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Permanent",
    "frequency": "Chosen once at Oracle 1",
    "effect": "LIMITATIONS: HP recovery from rests and from another creature's healing is halved, rounded down; your own Wound Eater drains and your own Revelations are not halved. Before a long rest completes, you must have successfully drained HP from a meaningful hostile living creature since your previous long rest or gain one level of Exhaustion after the rest. Your corpse-like appearance imposes disadvantage on the first friendly social check with an unfamiliar mortal who can clearly see you, unless circumstances make the appearance irrelevant.",
    "prerequisite": "Selected Curse: Wound Eater",
    "sourceObjectSha256": "b0523723ce95a44326adc752ad81f0d94103918e8af87bc432ba438d7d9e9302"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.false-life.false-life-boon-i",
    "name": "False Life — Boon I",
    "activation": "Passive; triggered survival",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Permanent advantage; immediate survival",
    "frequency": "Survival 1/long rest",
    "effect": "advantage on saves against death effects and hostile necrotic/negative-energy effects. 1/long rest when you would die from failed death saves or be reduced to 0 by an effect that does not kill outright, remain at 1 HP instead.",
    "prerequisite": "Oracle 3; selected Curse:False Life",
    "sourceObjectSha256": "737564c9de90452f2445c4cf7d41e4d6ebc027a8dd490627bb8700e330692fbe"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.false-life.false-life-boon-ii",
    "name": "False Life — Boon II",
    "activation": "Action",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Until voluntarily ended or one minute",
    "frequency": "1/encounter",
    "effect": "once per encounter as an Action feign perfect death for up to 1 minute. You remain conscious but cannot move, speak, take Actions or Reactions; ordinary undead ignore you unless you attack or otherwise reveal yourself. End the effect voluntarily at the start of your turn.",
    "prerequisite": "Oracle 5; selected Curse:False Life",
    "sourceObjectSha256": "cbe8f3409a5366d074c5f40995c7f32ae95a3e81cc224d5cc0d559107c92b6ce"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.false-life.false-life-boon-iii",
    "name": "False Life — Boon III",
    "activation": "Triggered when reduced to 0 HP",
    "cost": "0",
    "rangeAndTarget": "Self",
    "duration": "Until end of next regular turn",
    "frequency": "1/long rest",
    "effect": "1/long rest when reduced to 0 HP without instant death, remain conscious until the end of your next regular turn. During that turn choose either move up to your Speed, speak normally or activate one Revelation; you cannot do more than one of those options. If still at 0 afterward, become unconscious normally.",
    "prerequisite": "Oracle 10; selected Curse:False Life",
    "sourceObjectSha256": "85d55f1cb5629d4e63245bb644d55f30fd5c23d5d0ee8fd4a38245df817fb0b5"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.ancestor.echo-armor",
    "name": "Echo Armor",
    "activation": "Passive",
    "cost": "0 RC",
    "rangeAndTarget": "Self",
    "duration": "Permanent",
    "frequency": "Damage reduction always; death prevention 1/short rest",
    "effect": "Reduce the first nonmagical weapon damage you take each round by PB, minimum 0. Once per short rest, when damage would reduce you to 0 HP without killing you outright, remain at 1 HP instead. The prevention removes no Wounds and cannot trigger if another effect has already prevented that same reduction to 0.",
    "prerequisite": "Oracle 6; Mystery: Ancestor; selected Tier II Revelation",
    "sourceObjectSha256": "32761e631f565378d31fdfc1aa9abb37e9eea99fd4864bdeb30380cf04b4864e"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.ancestor.echo-crowned",
    "name": "Echo Crowned",
    "activation": "Passive and Bonus Action",
    "cost": "0 RC to maintain spirits; Revelation costs normally unless stated",
    "rangeAndTarget": "Self; death prevention ally within 5 tiles",
    "duration": "Permanent spirits; activated effects instantaneous",
    "frequency": "Double-cast 1/long rest; each spirit may be sacrificed once per long rest",
    "effect": "Maintain three named ancestral Echoes: Offense grants +1 on your first Revelation attack each round; Defense reduces the first damage you take each round by S; Utility grants advantage on one History, Insight or Perception check per round. Once per long rest, when you activate a known Revelation, you may pay its RC cost twice and resolve it twice as part of the same action against different legal targets; copied resolution cannot duplicate resource or action triggers. You may sacrifice one currently available Echo as a Reaction when an ally within 5 tiles would be reduced to 0 HP to leave that ally at 1 HP instead, or as a Bonus Action to restore your RC to maximum. A sacrificed Echo provides no passive benefit until your next long rest.",
    "prerequisite": "Oracle 20; Mystery: Ancestor",
    "sourceObjectSha256": "7991906ef73bc0ffdfef0fa2a8d0ec79f288f9d0c8ad362042754a88c5d3bcad"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.battle.battle-prophecy-trigger",
    "name": "Battle Prophecy Trigger",
    "activation": "Triggered",
    "cost": "0 RC",
    "rangeAndTarget": "Self",
    "duration": "Instantaneous",
    "frequency": "At most once per round during a real encounter",
    "effect": "When you or an ally reduces a meaningful hostile creature to 0 HP, regain 1 RC, never above maximum. Summoned, trivial, friendly or repeatedly revived creatures do not qualify.",
    "prerequisite": "Oracle 1; Mystery: Battle",
    "sourceObjectSha256": "75d18b4ec0942414870a4519e988e3793340394c21b7f8b5cdf846538679c5d8"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.battle.avatar-of-the-war-chorus",
    "name": "Avatar of the War Chorus",
    "activation": "Bonus Action",
    "cost": "0 RC",
    "rangeAndTarget": "Self and allies within 5 tiles",
    "duration": "3 rounds",
    "frequency": "1/long rest",
    "effect": "Manifest three banners for 3 rounds. Offense Banner: once on each of your turns add 2 S damage to one weapon or Revelation damage roll. Defense Banner: gain +2 AC; allies within 5 tiles reduce first damage each round by 1. Rally Banner: once per round one ally within 5 tiles gains +1 on an attack roll made during its turn. Your known Tier I Battle Revelations cost 0 RC while all three banners remain. You may sacrifice one banner as a Reaction to leave an ally within 5 tiles at 1 HP instead of 0, or as a Bonus Action to restore your RC to maximum; that banner's benefit ends immediately. When the 3-round effect ends naturally, regain 2 RC, never above maximum. The Final grants no more than one additional full Action per creature per round.",
    "prerequisite": "Oracle 20; Mystery: Battle",
    "sourceObjectSha256": "275127469d779f546ed83820f67a70bc3aadfc67389ffbd40b07b952bf05aa47"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.bones.bones-prophecy-trigger",
    "name": "Bones Prophecy Trigger",
    "activation": "Triggered",
    "cost": "0 RC",
    "rangeAndTarget": "Self; qualifying creature within 5 tiles",
    "duration": "Instantaneous",
    "frequency": "At most once per round during a real encounter",
    "effect": "When an undead creature or meaningful hostile creature at 0 HP within 5 tiles dies, regain 1 RC, never above maximum. Summoned, friendly, trivial or repeatedly revived creatures cannot trigger this recovery.",
    "prerequisite": "Oracle 1; Mystery: Bones",
    "sourceObjectSha256": "bed997b4dca4f52173fb62c19633c42c565fa351eea1c43db2617ddc68aa55c1"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.bones.marrow-drain",
    "name": "Marrow Drain",
    "activation": "Action",
    "cost": "1 RC",
    "rangeAndTarget": "One creature you can touch",
    "duration": "Instantaneous; healing lock until end of your next turn against undead",
    "frequency": "At will while RC remains",
    "effect": "Make a Revelation attack. On hit deal 2d6 necrotic damage and regain HP equal to half the actual damage dealt, rounded down, maximum S+M HP. Against undead, deal 3d6 necrotic instead and the target cannot regain HP until the end of your next turn. Constructs are immune to the healing-drain portion. This healing removes no Wounds.",
    "prerequisite": "Oracle 3; Mystery: Bones; selected Tier I Revelation",
    "sourceObjectSha256": "107b79b9c3ad5f3e3bed99fdabc6543043cc73cd8adbe0852fbdda3c9e6deb77"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.bones.rotting-touch",
    "name": "Rotting Touch",
    "activation": "Action",
    "cost": "2 RC",
    "rangeAndTarget": "One creature you can touch",
    "duration": "Maximum 3 rounds",
    "frequency": "At will while RC remains",
    "effect": "Make a Revelation attack. On hit the target makes a Constitution save. On failure it gains Decay for up to 3 rounds: attacks against it add S damage once per attacker per turn, it takes -1 on saving throws and cannot regain HP. At the end of each turn it repeats the save, ending Decay on success. Corpses within 2 tiles of a Decayed creature cannot be raised while Decay persists. If the target is undead, it also takes 2d6 necrotic damage on the initial hit and you regain half the actual damage dealt, capped at S+M HP. At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack.",
    "prerequisite": "Oracle 6; Mystery: Bones; selected Tier II Revelation",
    "sourceObjectSha256": "2a184115c77c3e39626229f0d95c4b73218e849b6ccc078dd5ae170ccfdf3475"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.flame.undying-ember",
    "name": "Undying Ember",
    "activation": "Triggered",
    "cost": "0 RC",
    "rangeAndTarget": "Self; enemies adjacent to you; allies within 2 tiles",
    "duration": "Instantaneous; enemy penalty until end of next turn",
    "frequency": "1/long rest",
    "effect": "When damage would reduce you to 0 HP without killing you outright, remain at 1 HP. Adjacent enemies make Dexterity saves, taking 2d6 fire damage on failure or half on success; failing enemies also take -1 on attack rolls until the end of their next turn. Up to three living allies within 2 tiles each regain 1d6 HP. This removes no Wounds and cannot trigger from self-inflicted staged damage.",
    "prerequisite": "Oracle 6; Mystery: Flame; selected Tier II Revelation",
    "sourceObjectSha256": "93821a63698a0c05d1300f12c7ea95211f4c0796d8f1300e2e491384ddf5cb90"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.life.bloom-ward",
    "name": "Bloom Ward",
    "activation": "Passive and Bonus Action",
    "cost": "0 RC",
    "rangeAndTarget": "Self; allies within 2 tiles; one ally within 3 tiles for bloom",
    "duration": "Passive permanent; bloom until consumed or 1 minute",
    "frequency": "Bloom 1/long rest",
    "effect": "Once per round when a living ally within 2 tiles receives HP healing from a paid or finite-use effect, add S HP to that healing. Reduce the first necrotic or poison damage you take each round by 1. Once per long rest place a protective bloom on one ally within 3 tiles. It absorbs the next 10+Oracle level damage dealt to that ally, then ends. When it ends, the ally gains +1 on saves against Frightened until the end of its next turn.",
    "prerequisite": "Oracle 1; Mystery: Life",
    "sourceObjectSha256": "0252c7014f1020fe92cdd9c29f41c074d47a6d8c6babf5665f939529eb6a0543"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.life.overflowing-light",
    "name": "Overflowing Light",
    "activation": "Action",
    "cost": "1 RC",
    "rangeAndTarget": "One living ally within 4 tiles",
    "duration": "Healing instantaneous; temporary HP 2 rounds",
    "frequency": "At will while RC remains",
    "effect": "The target regains 2d6+M HP. Healing exceeding its maximum becomes temporary HP, maximum 10, lasting 2 rounds. When those temporary HP expire naturally, if at least 1 remains the target may end one of Frightened, Poisoned or Staggered. This cannot resurrect, remove Wounds or convert deliberately wasted healing into more than 10 temporary HP.",
    "prerequisite": "Oracle 3; Mystery: Life; selected Tier I Revelation",
    "sourceObjectSha256": "79723edccb03063801846d1d9dbb9c5b945cb4f49a797b55efb410c72042cc33"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.life.thorned-shelter",
    "name": "Thorned Shelter",
    "activation": "Action",
    "cost": "1 RC",
    "rangeAndTarget": "One living ally within 3 tiles",
    "duration": "2 rounds",
    "frequency": "At will while RC remains",
    "effect": "The target gains +2 AC and reduces the first damage it takes each round by S. Once per round when it receives HP healing from another finite effect, add 1 HP. The first melee attacker to damage it each round takes 1d4 piercing damage and must make a Strength save; on failure its Speed becomes 0 until the end of that current turn. This movement restriction is not a full-turn denial.",
    "prerequisite": "Oracle 3; Mystery: Life; selected Tier I Revelation",
    "sourceObjectSha256": "f5eae57f57896210e6d0cee18d477d87d3e99e28f33be7cbf9e1dfdd92929dda"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.life.verdant-pulse",
    "name": "Verdant Pulse",
    "activation": "Passive and Reaction",
    "cost": "0 RC",
    "rangeAndTarget": "Allies you heal; emergency ally within 4 tiles",
    "duration": "Buff until end of ally's next turn; emergency instantaneous",
    "frequency": "Buff once per ally per short rest; emergency 1/encounter",
    "effect": "When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it.",
    "prerequisite": "Oracle 6; Mystery: Life; selected Tier II Revelation",
    "sourceObjectSha256": "feb0f82538549fb2d540cfa9a68b89f517d4f1138b44ade546065fc7300c24f9"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.life.song-of-mending",
    "name": "Song of Mending",
    "activation": "Action",
    "cost": "3 RC",
    "rangeAndTarget": "Living allies within 5 tiles",
    "duration": "2 rounds",
    "frequency": "At will while RC remains",
    "effect": "On activation and at the start of your next regular turn, each living ally still within 5 tiles regains 2d6 HP, for exactly two possible pulses per use. Once during the duration for each ally, when one damage event would reduce it below 1 HP without instant death, it remains at 1 HP instead. When this prevention triggers, that ally may end Frightened or Poisoned and gains +S HP the next time a separate finite healing effect restores HP before Song ends. This removes no Wounds and cannot resurrect.",
    "prerequisite": "Oracle 9; Mystery: Life",
    "sourceObjectSha256": "ca7500f38966fc943c0398ff2fbddfe96070ca9caf15a6d0b24cee7d2fa2def1"
  },
  {
    "kind": "class-card",
    "owner": "oracle",
    "id": "oracle.supplement.life.eternal-bloom",
    "name": "Eternal Bloom",
    "activation": "Action",
    "cost": "0 RC",
    "rangeAndTarget": "5-tile-radius fixed sanctuary centered within 5 tiles",
    "duration": "3 rounds",
    "frequency": "1/long rest",
    "effect": "When Eternal Bloom appears, record each living ally's missing HP while it is inside the zone. Divide that recorded missing HP into three healing installments as evenly as possible, with any remainder assigned to earlier pulses. On activation and at the start of each of your next two regular turns, each qualifying ally still inside regains its next installment; later damage does not increase this reserve. Once per ally during the Bloom, when damage would reduce it to 0 HP without instant death, it remains at 1 HP instead. Allies in the zone have necrotic immunity for the 3 rounds. When the Bloom ends, petals create light obscurement in the zone until the start of your next turn. It removes no Wounds and does not resurrect.",
    "prerequisite": "Oracle 20; Mystery: Life",
    "sourceObjectSha256": "3d97cb828d42d1ec6f4f674e4328a37f916f47c15513a4e357cff80a706f7d02"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.base.protective-stance",
    "name": "Protective Stance",
    "activation": "Bonus Action",
    "cost": "One short-rest use",
    "rangeAndTarget": "Self; adjacent ally",
    "duration": "Until start next turn",
    "frequency": "1/short rest",
    "effect": "Gain+1 AC. Once before end, Reaction interpose for adjacent ally hit by weapon: reduce its damage by S+M and take that much unpreventable damage yourself. Cannot redirect again or create resource/damage triggers. You must remain conscious.",
    "prerequisite": null,
    "sourceObjectSha256": "71f0333a1fa9bee2ffd004f8327f542364d847dfd263df4bf80cb0fe324de5c7"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.base.sacred-touch",
    "name": "Sacred Touch",
    "activation": "Action",
    "cost": "0 for stabilize; 1 RP for inspection",
    "rangeAndTarget": "One living creature touched",
    "duration": "Instant",
    "frequency": "At will with resources",
    "effect": "Stabilize a living Downed creature at 0 HP without healing; damage/ordinary rules can end stability. Alternatively pay 1 RP and examine 1 minute to learn whether one curse/disease affects it, without revealing origin or cure. No resurrection or free healing.",
    "prerequisite": null,
    "sourceObjectSha256": "81444695d2cf9e5c54afee5721c29da4344543618244dde801758dde43744ac0"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-shared.last-reproach",
    "name": "Last Reproach",
    "activation": "Reaction after an enemy damages an ally",
    "cost": "10 RP",
    "rangeAndTarget": "That enemy 60 ft; one living ally in your aura",
    "duration": "Instant",
    "frequency": "1/short rest",
    "effect": "New rank 5 Forbidden spell. Enemy WIS save for 3 S d8 necrotic, half success; ally regains S d8 HP after triggering damage. Does not revive dead or undo conditions. Uses ordinary spell strain and your Reaction.",
    "prerequisite": "Paladin 17; selected Oathbreaker inversion",
    "sourceObjectSha256": "895f333185c3eb243fcbe76dcc36a38ed52f8b1f4994746abf250a0102f7015d"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-mercy.aura-of-mercy",
    "name": "Aura of Mercy",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Up to 3 chosen allies in your Oath aura",
    "duration": "While conscious and target remains in aura",
    "frequency": "Choose targets at start of each turn",
    "effect": "The first time each round a selected ally receives HP healing from a finite or paid effect, add S HP. Each selected ally also reduces the first necrotic damage it takes each round by S. These benefits do not stack with another Aura of Mercy from the same source.",
    "prerequisite": "Paladin 3; Oath of Mercy",
    "sourceObjectSha256": "2601db1c3ead6e19e3cda88af15a2f7525e96d2d2a1171d037fc874d9c47ae35"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-mercy.miracle-veil",
    "name": "Miracle Veil",
    "activation": "Reaction",
    "cost": "2 RP",
    "rangeAndTarget": "One living ally in your Oath aura",
    "duration": "Until start of your next regular turn",
    "frequency": "1/short rest",
    "effect": "Trigger when the ally would be reduced below 1 HP by damage. Until the start of your next regular turn, that ally cannot be reduced below 1 HP by damage. The Veil does not prevent instant-death effects that explicitly bypass HP, does not resurrect a dead creature and removes no Wounds. Damage and attached conditions still resolve normally except for the HP floor.",
    "prerequisite": "Paladin 11; Oath of Mercy",
    "sourceObjectSha256": "17846f0aa17add447d160181b21e32f4862576de60848c44818d39fdeff7a3ee"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-mercy.blessing-of-the-meek",
    "name": "Blessing of the Meek",
    "activation": "Action",
    "cost": "2 RP",
    "rangeAndTarget": "One living ally within 30 feet",
    "duration": "Healing instantaneous; AC bonus until start of your next regular turn",
    "frequency": "At will while RP remains",
    "effect": "The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules.",
    "prerequisite": "Paladin 3; Oath of Mercy",
    "sourceObjectSha256": "de83f7216e4f442bf324e7e9650e69091077d79b1be79d0753257dfbce13cde4"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-mercy.grace-reversal",
    "name": "Grace Reversal",
    "activation": "Reaction",
    "cost": "10 RP",
    "rangeAndTarget": "One allied corpse in your Oath aura that died since the end of your previous regular turn",
    "duration": "Instantaneous",
    "frequency": "At most once per creature per long rest",
    "effect": "Trigger when you are reduced to 0 HP without being killed outright. One eligible allied corpse returns to life at 1 HP. You remain at 0 HP and resolve your own dying state normally. The revived ally retains Wounds and expended resources and must have a body capable of sustaining life. Grace Reversal cannot target you.",
    "prerequisite": "Paladin 17; Oath of Mercy",
    "sourceObjectSha256": "51322e780d7ca204f39320d5cc583699a3f9a18ebc8f4e67db3feef638deec44"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-mercy.grace-eternal",
    "name": "Grace Eternal",
    "activation": "Bonus Action",
    "cost": "0 RP",
    "rangeAndTarget": "Up to 3 allies in your Oath aura",
    "duration": "Until start of your next regular turn",
    "frequency": "1/long rest",
    "effect": "Apply Miracle Veil to up to 3 allies in your aura without spending its short-rest use or RP. Once during this Veil for each affected ally, if damage would reduce it to 0 HP, it remains at 1 HP and immediately regains 2d8 HP. It also gains necrotic resistance until the end of its next turn. During Grace Eternal you may use Lay on Hands once without an Action, but must still spend points from your current Lay on Hands pool and may target only one creature.",
    "prerequisite": "Paladin 20; Oath of Mercy",
    "sourceObjectSha256": "9144f23fd7fb45d1beb6c300bb20b85cd3eb172e4a6ac53003c0260770f94a25"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression",
    "name": "Healing Suppression",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
    "duration": "While conscious and target remains in aura",
    "frequency": "Choose targets at start of each turn",
    "effect": "HP healing received by each selected creature is halved, rounded down. Temporary HP, damage prevention and resurrection are not healing for this effect. This suppression cannot reduce healing below 0 or convert prevented healing into damage.",
    "prerequisite": "Paladin 3; Oathbreaker — Oath of Mercy",
    "sourceObjectSha256": "1613079d8c08dac41dc4b7fe98b3dbbf5f4534a28a2d30282e93522bd69fdbde"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-vengeance.final-verdict",
    "name": "Final Verdict",
    "activation": "Action",
    "cost": "10 RP",
    "rangeAndTarget": "One creature marked by you within 30 feet and at or below half maximum HP",
    "duration": "Instantaneous or empowerment until end of your next regular turn",
    "frequency": "At will while RP remains",
    "effect": "The marked target makes a Constitution save, taking 4 S d8 radiant damage on failure or half on success. On failure it also cannot regain HP until the end of its next turn. If that damage reduces it to 0 HP, use ordinary Downed/death rules; there is no percentage-HP execution. On success your next Smite against it before the end of your next turn uses maximum damage dice. This bounded damage replaces the source draft’s automatic reduction to 0 HP.",
    "prerequisite": "Paladin 17; Oath of Vengeance",
    "sourceObjectSha256": "588a235ef97e9f2d39ca847326623ea090b05676da713f90f447f75361e5582d"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-flame.phoenix-rebirth",
    "name": "Phoenix Rebirth",
    "activation": "Reaction",
    "cost": "10 RP",
    "rangeAndTarget": "One living ally in your Oath aura reduced to 0 HP",
    "duration": "Revival instantaneous; fire shield until end of target's next turn",
    "frequency": "Once per combat per ally",
    "effect": "Trigger when the ally reaches 0 HP without being killed outright. It immediately regains HP equal to half its maximum, rounded down, minimum 1. Until the end of its next turn it has fire resistance. Once during that duration when a creature within melee reach damages it with a melee attack, that attacker takes 2d6 fire damage. Phoenix Rebirth removes no Wounds and cannot restore a creature destroyed beyond recovery.",
    "prerequisite": "Paladin 17; Oath of Flame",
    "sourceObjectSha256": "0a38ac2a6f534b9b6eefaa79733078371cc3169aa85ed60b825247cdfdf6ffd9"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified",
    "name": "Scorch the Sanctified",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Up to 3 enemies in your Oath aura",
    "duration": "While conscious and target remains in aura",
    "frequency": "Choose targets at start of each turn",
    "effect": "Selected enemies cannot regain HP from passive regeneration. At the start of each selected enemy's turn it makes a Charisma save. On failure, one temporary beneficial magical effect on it chosen by the Director from eligible non-innate effects is suppressed until the start of its next turn. Immunities, class engines, permanent traits and attunement are never suppressed.",
    "prerequisite": "Paladin 3; Oathbreaker — Oath of Flame",
    "sourceObjectSha256": "cbfc7808eaa7713c9e05331e24397dcbea9a3a6642ed0d08f088e4c582a950e8"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura",
    "name": "Lifeleech Bloom Aura",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Up to 3 enemies in your Oath aura",
    "duration": "While conscious and target remains in aura",
    "frequency": "Choose targets and one damage type at start of each turn",
    "effect": "Selected enemies cannot regain HP from passive regeneration. Also choose acid, cold, fire, lightning, necrotic, poison, radiant or thunder. A selected enemy's resistance to that chosen type is suppressed while it remains selected in the aura; immunity is never suppressed.",
    "prerequisite": "Paladin 3; Oathbreaker — Oath of the Ancients",
    "sourceObjectSha256": "ab791099a2d42dd7017f37b891cda2e14f4c1c3ae23f73ef652dd3f459028af2"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom",
    "name": "Lifeleech Bloom",
    "activation": "Action",
    "cost": "2 RP",
    "rangeAndTarget": "Up to 3 living creatures or plant creatures in your Oath aura",
    "duration": "Instantaneous",
    "frequency": "1/short rest; replaces Signature Power use",
    "effect": "Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. You regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. You may include willing allies among the targets, but they receive no protection and cannot be reduced below 1 HP by this Blasphemous Word. Constructs and ordinary unattended plants provide no healing.",
    "prerequisite": "Paladin 11; Oathbreaker — Oath of the Ancients",
    "sourceObjectSha256": "08c5946db93747abe8a71ed1a6aa82258108a072d3873c9f85a8ddae94fba83f"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-grief.echo-of-the-fallen",
    "name": "Echo of the Fallen",
    "activation": "Action",
    "cost": "10 RP",
    "rangeAndTarget": "One allied creature who died in your aura this encounter; one target within the former ally's normal weapon range or one ally in your aura",
    "duration": "Until start of your next regular turn",
    "frequency": "At most once per fallen ally per long rest",
    "effect": "Manifest the ally's spirit for one round. Choose one mode on cast. Strike: the spirit makes one attack using the deceased ally's last recorded ordinary weapon attack bonus and base weapon damage, with no class-resource riders, extra attacks or proc effects. Guard: one chosen ally in your aura gains +2 AC until the start of your next turn. The spirit is not resurrected, cannot be targeted and disappears afterward. The single spirit strike uses PB+CHA to hit and S d8+M damage of the original weapon type if the recorded profile would exceed either value. It consumes the shared damaging-companion-action budget for that round; no monster or high-level player stat-block duplication.",
    "prerequisite": "Paladin 17; Oath of Grief",
    "sourceObjectSha256": "27c9f765ebbd0680287b9c51689a0065caa04ddea514aafb66ba6bd88a1aa0fa"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-grief.dirge-of-passage",
    "name": "Dirge of Passage",
    "activation": "Bonus Action",
    "cost": "0 RP",
    "rangeAndTarget": "Memories of up to 2 fallen allies; creatures in your Oath aura",
    "duration": "2 rounds",
    "frequency": "1/long rest",
    "effect": "For 2 rounds maintain two Final Vigil memories simultaneously and gain both selected benefits. Up to three selected hostile undead in your aura take an additional S radiant damage from your first damaging Paladin feature each round and cannot regain HP. Living allies in your aura gain +2 on death saves. No spirit gains its own turn, resources, spellcasting or complete former statistics. This flat rider replaces blanket damage vulnerability and never doubles a whole attack.",
    "prerequisite": "Paladin 20; Oath of Grief",
    "sourceObjectSha256": "df1f6705254fc3dcbf79d5c08aae5baf78e792c21ce9e059969dfe4627c62200"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura",
    "name": "Dirge of Ruin Aura",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
    "duration": "While conscious and target remains in aura",
    "frequency": "Choose targets at start of each turn",
    "effect": "Selected living creatures cannot be returned from death while inside the aura, and HP healing they receive is reduced by S+M, minimum 0. This never converts healing into damage and cannot retroactively reverse a resurrection completed before the creature entered the aura.",
    "prerequisite": "Paladin 3; Oathbreaker — Oath of Grief",
    "sourceObjectSha256": "65f1ac74f274a2f171571f40d3ce938061c6e4c58fba8925270b949fcec183ff"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin",
    "name": "Dirge of Ruin",
    "activation": "Action",
    "cost": "2 RP",
    "rangeAndTarget": "Up to 3 creatures in your Oath aura",
    "duration": "Damage instantaneous; healing block until end of next turn",
    "frequency": "1/short rest; replaces Signature Power use",
    "effect": "Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. A failing target cannot regain HP until the end of its next turn. This does not prevent temporary HP or remove healing already received.",
    "prerequisite": "Paladin 11; Oathbreaker — Oath of Grief",
    "sourceObjectSha256": "16cc8982591672cdbad5aa34bf755e2c4b8024c032fb29dba978ec14eb4d6407"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oath-of-the-martyr-king.last-king-s-gift",
    "name": "Last King’s Gift",
    "activation": "Reaction before ally falls to 0 HP",
    "cost": "10 RP",
    "rangeAndTarget": "One living ally in your aura",
    "duration": "Instant prevention; temporary HP until lost or encounter end",
    "frequency": "Once per encounter per ally",
    "effect": "When damage would reduce the ally to 0 HP without killing it outright, it instead remains at 1 HP and gains temporary HP equal to your Paladin level after the triggering damage resolves. This does not reverse a completed death, remove Wounds or replenish any resource.",
    "prerequisite": "Paladin 17; Oath of the Martyr King",
    "sourceObjectSha256": "ef3133f57d5da376b3755b09ca86e3140362b0ae00c199b68835114019d4c693"
  },
  {
    "kind": "class-card",
    "owner": "paladin",
    "id": "paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura",
    "name": "Crownshatter Decree Aura",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Up to three selected enemies in your aura",
    "duration": "While conscious and in aura",
    "frequency": "Each incoming healing event",
    "effect": "A selected enemy receives HP healing only if it has taken actual damage from a meaningful hostile creature since the start of its previous regular turn. If it has not, that healing restores 0 HP; its source still spends its normal costs. Temporary HP, stabilization and resurrection are not HP healing for this restriction. This aura never creates damage, transfers healing or reverses recovery that already resolved.",
    "prerequisite": "Paladin 3; Oathbreaker — Oath of the Martyr King",
    "sourceObjectSha256": "e4341a3bd789ba5baa4c0bf1817a7a16ec61fc0d98d9ca79101397f9f984f203"
  },
  {
    "kind": "class-card",
    "owner": "ranger",
    "id": "ranger.hero.outrider.blight-infusion",
    "name": "Blight Infusion",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Primary target of your Arrow on blighted ground",
    "duration": "Until end target's next turn",
    "frequency": "Once/Arrow",
    "effect": "On hit target makes CON save or the next HP healing it receives is reduced by M, minimum 0. This is temporary Blight, not permanent campaign Corruption; multiple applications do not stack.",
    "prerequisite": null,
    "sourceObjectSha256": "56230dcd9d01a0ffa5627fa3b6a3dc344570f83e7eabe5ba4e241f5efd52cffe"
  },
  {
    "kind": "class-card",
    "owner": "ranger",
    "id": "ranger.hero.outrider.withering-shot",
    "name": "Withering Shot",
    "activation": "Action",
    "cost": "3 RP",
    "rangeAndTarget": "One enemy in bow range",
    "duration": "Instant; until end target's next turn",
    "frequency": "Recharge 3",
    "effect": "Bow attack; hit adds S d6 necrotic and target makes CON save. Failure halves the next HP healing it receives before expiry, rounding down. No stacking with another reduction to create negative healing.",
    "prerequisite": null,
    "sourceObjectSha256": "ba3f59599016aaaaf85726c00275367daca171477f078d3879ac916a90e41e5c"
  },
  {
    "kind": "class-card",
    "owner": "shaman",
    "id": "shaman.hero.bloodcaller.blight-totem",
    "name": "Blight Totem",
    "activation": "Action",
    "cost": "3 RP",
    "rangeAndTarget": "Totem within 30 ft; 15 ft aura affecting all creatures",
    "duration": "3 of your turns",
    "frequency": "Ordinary totem capacity/concentration",
    "effect": "HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing.",
    "prerequisite": null,
    "sourceObjectSha256": "56bd3dd7b141931dda883f3728d30221c8e34ba30347d55c87fe66dc2f338805"
  },
  {
    "kind": "class-card",
    "owner": "soldier",
    "id": "soldier.arch.fortify-zone",
    "name": "Fortify Zone",
    "activation": "Action",
    "cost": "1 short-rest use",
    "rangeAndTarget": "Visible 15 ft square within 30 ft",
    "duration": "3 rounds",
    "frequency": "1/short rest",
    "effect": "Designate fortified firing lanes. Ranged attacks against up to 3 allies inside take-2 to hit while you remain conscious within 30 ft. Does not affect saves, melee attacks or attacks from inside zone.",
    "prerequisite": null,
    "sourceObjectSha256": "0938937bdd2ad8e34bc16ade52b53b16b3dc67136d97b1a728c03f4576943f3c"
  },
  {
    "kind": "class-card",
    "owner": "soldier",
    "id": "soldier.hero.champion.rallying-cry",
    "name": "Rallying Cry",
    "activation": "Bonus Action",
    "cost": "1 long-rest use",
    "rangeAndTarget": "Up to 3 allies within 30 ft who hear you",
    "duration": "Instant; temp HP to encounter end",
    "frequency": "1/long rest",
    "effect": "End Frightened on each and grant S+M temporary HP. Cannot revive, heal real HP or repeatedly refresh from imitation/copies.",
    "prerequisite": null,
    "sourceObjectSha256": "5bfb1a71cb4b5b01c09fc3090391670394590c62f63474223b80356fa6459009"
  },
  {
    "kind": "class-card",
    "owner": "tinker",
    "id": "tinker.base.field-repair",
    "name": "Field Repair",
    "activation": "Action",
    "cost": "1 RP",
    "rangeAndTarget": "One construct/device touched",
    "duration": "Instant",
    "frequency": "Recharge 2",
    "effect": "Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses.",
    "prerequisite": null,
    "sourceObjectSha256": "612a9f00b4e33a8bfc77c3f83ff1e1d839fa1237e8d20e65b703bea1431b6d7f"
  },
  {
    "kind": "class-card",
    "owner": "tinker",
    "id": "tinker.hero.artificer.repair-pulse",
    "name": "Repair Pulse",
    "activation": "Action",
    "cost": "3 RP",
    "rangeAndTarget": "Upto 3 friendly devices within 30 ft",
    "duration": "Instant; AC until start next turn",
    "frequency": "1/short rest",
    "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets.",
    "prerequisite": null,
    "sourceObjectSha256": "bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593"
  },
  {
    "kind": "class-card",
    "owner": "warrior",
    "id": "warrior.hero.wardborn.stabilizing-injection",
    "name": "Stabilizing Injection",
    "activation": "Action",
    "cost": "Consume 1 prepared serum dose",
    "rangeAndTarget": "One living creature you touch",
    "duration": "Instantaneous",
    "frequency": "At most once per target per long rest",
    "effect": "Stabilizing Injection. The target regains 2d8 + M HP and may end one of Poisoned, Frightened or Staggered. If Diseased, it may immediately repeat one saving throw the disease normally permits. This removes no Wounds, cannot restore the dead and does not activate a mutation or apply the consumed serum's normal profile.",
    "prerequisite": null,
    "sourceObjectSha256": "b58508331c82ad5a7dad8bd3713029899b9a7c341c490220d997caf0e3aa71db"
  },
  {
    "kind": "class-card",
    "owner": "warrior",
    "id": "warrior.hero.ironskin.regenerative-mutation",
    "name": "Regenerative Mutation",
    "activation": "Passive",
    "cost": "Spend healing amount from Mutation Recovery Reserve",
    "rangeAndTarget": "Self",
    "duration": "While at least one mutation is active in a real encounter",
    "frequency": "Once at the start of each regular turn",
    "effect": "Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve.",
    "prerequisite": null,
    "sourceObjectSha256": "9dcfe6b7b149360e470c0d7940937b13c7bbdc4f696999b93710257158818fd1"
  },
  {
    "kind": "class-card",
    "owner": "warrior",
    "id": "warrior.supplement.redundant-organs",
    "name": "Redundant Organs",
    "activation": "Triggered while active",
    "cost": "One mutation slot; serum activation",
    "rangeAndTarget": "Self",
    "duration": "Instantaneous",
    "frequency": "1/long rest",
    "effect": "When damage would reduce you to 0 HP without killing you outright, remain at 1 HP instead.",
    "prerequisite": "Warrior 6; Advanced Vital",
    "sourceObjectSha256": "51fd6f5a02d4328ed7a047301865acdac992364b8c4c924da5f85315ab4efbca"
  },
  {
    "kind": "class-card",
    "owner": "warrior",
    "id": "warrior.supplement.hemophage-core",
    "name": "Hemophage Core",
    "activation": "Triggered while active",
    "cost": "One mutation slot; serum activation",
    "rangeAndTarget": "Self",
    "duration": "Instantaneous",
    "frequency": "Once per turn",
    "effect": "When you personally reduce a meaningful hostile creature to 0 HP with a melee attack, regain 2d6 HP. Summoned, trivial, friendly or repeatedly revived creatures cannot trigger this healing. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve.",
    "prerequisite": "Dreadspawn; Aberrant Mutation Tree; Warrior 10",
    "sourceObjectSha256": "e472701e8febc1973d6963d6a4d3c78ba1a4aa6d4e1740e3a484c9344b14cbda"
  }
]
```

## Exact unfinished ordinary spell records (not operational)

```json
[
  {
    "kind": "ordinary-spell-catalog",
    "spellId": "stitch-fate",
    "hasOperationalProcedure": false,
    "sourceObjectSha256": "8bd3d12e82603aadef4a255061176b3a859a6ebd496c74b71f68d8187341199f",
    "spell": {
      "id": "stitch-fate",
      "name": "Stitch Fate",
      "schools": [
        "Divination"
      ],
      "status": "blocked-pending-operational-review",
      "visibility": "public-source-review",
      "classAccess": {
        "Cleric": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Divination",
          "baseRpCost": 21
        },
        "Wizard": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Divination",
          "baseRpCost": 21
        }
      },
      "operational": null,
      "additionalRpCost": 0,
      "source": {
        "catalogPath": "src/data/spells.js",
        "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
        "catalogKey": "stitch-fate",
        "original": {
          "name": "Stitch Fate",
          "level": 8,
          "resonanceRank": 8,
          "school": "Divination",
          "schools": [
            "Divination"
          ],
          "placements": [
            {
              "name": "Stitch Fate",
              "school": "Divination",
              "level": 8,
              "summary": "Change one failed death save or auto-revive a dying target."
            }
          ],
          "classLevels": {
            "Cleric": 8,
            "Wizard": 8
          },
          "classRanks": {
            "Cleric": 8,
            "Wizard": 8
          },
          "classLearnLevels": {
            "Cleric": 15,
            "Wizard": 15
          },
          "classSchools": {
            "Cleric": "Divination",
            "Wizard": "Divination"
          },
          "castingTime": "Not specified in current rulebook",
          "range": "Not specified in current rulebook",
          "components": "Not specified in current rulebook",
          "duration": "Not specified in current rulebook",
          "description": "Change one failed death save or auto-revive a dying target.",
          "alternateSummaries": [],
          "classes": [
            "Cleric",
            "Wizard"
          ],
          "status": "canon",
          "source": "Player Rulebook — Spell Lists"
        },
        "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
        "coreEntries": [
          {
            "index": 290,
            "original": {
              "school": "Divination",
              "level": 8,
              "name": "Stitch Fate",
              "effect": "Change one failed death save or auto-revive a dying target.",
              "source_paragraph": 9339,
              "casting_time": "1 action",
              "range": "120 feet",
              "duration": "Instantaneous",
              "components": "V, S, F",
              "resolution": "Automatic or opposed as described",
              "tags": [
                "Utility"
              ],
              "rp_cost": 21
            }
          }
        ],
        "possibleHistoricalAliases": []
      },
      "reviewFlags": [
        "Core resolution requires an explicit operational interpretation",
        "Not selectable in this spell playtest packet until individual operational review"
      ]
    }
  },
  {
    "kind": "ordinary-spell-catalog",
    "spellId": "death-ward",
    "hasOperationalProcedure": false,
    "sourceObjectSha256": "163354918258ef27c93d2f829226495e221919cef574c8670224fc154bcd023e",
    "spell": {
      "id": "death-ward",
      "name": "Death Ward",
      "schools": [
        "Necromancy"
      ],
      "status": "blocked-pending-operational-review",
      "visibility": "public-source-review",
      "classAccess": {
        "Cleric": {
          "rank": 4,
          "minimumClassLevel": 7,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Crimson Agent": {
          "rank": 4,
          "minimumClassLevel": 11,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Druid": {
          "rank": 4,
          "minimumClassLevel": 7,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Shaman": {
          "rank": 4,
          "minimumClassLevel": 10,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Thief": {
          "rank": 4,
          "minimumClassLevel": 18,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Wizard": {
          "rank": 4,
          "minimumClassLevel": 7,
          "school": "Necromancy",
          "baseRpCost": 7
        }
      },
      "operational": null,
      "additionalRpCost": 0,
      "source": {
        "catalogPath": "src/data/spells.js",
        "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
        "catalogKey": "death-ward",
        "original": {
          "name": "Death Ward",
          "level": 4,
          "resonanceRank": 4,
          "school": "Necromancy",
          "schools": [
            "Necromancy"
          ],
          "placements": [
            {
              "name": "Death Ward",
              "school": "Necromancy",
              "level": 4,
              "summary": "First time target would drop to 0 HP, they drop to 1 HP instead."
            }
          ],
          "classLevels": {
            "Cleric": 4,
            "Crimson Agent": 4,
            "Druid": 4,
            "Shaman": 4,
            "Thief": 4,
            "Wizard": 4
          },
          "classRanks": {
            "Cleric": 4,
            "Crimson Agent": 4,
            "Druid": 4,
            "Shaman": 4,
            "Thief": 4,
            "Wizard": 4
          },
          "classLearnLevels": {
            "Cleric": 7,
            "Crimson Agent": 11,
            "Druid": 7,
            "Shaman": 10,
            "Thief": 18,
            "Wizard": 7
          },
          "classSchools": {
            "Cleric": "Necromancy",
            "Crimson Agent": "Necromancy",
            "Druid": "Necromancy",
            "Shaman": "Necromancy",
            "Thief": "Necromancy",
            "Wizard": "Necromancy"
          },
          "castingTime": "Not specified in current rulebook",
          "range": "Not specified in current rulebook",
          "components": "Not specified in current rulebook",
          "duration": "Not specified in current rulebook",
          "description": "First time target would drop to 0 HP, they drop to 1 HP instead.",
          "alternateSummaries": [],
          "classes": [
            "Cleric",
            "Crimson Agent",
            "Druid",
            "Shaman",
            "Thief",
            "Wizard"
          ],
          "status": "canon",
          "source": "Player Rulebook — Spell Lists"
        },
        "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
        "coreEntries": [
          {
            "index": 677,
            "original": {
              "school": "Necromancy",
              "level": 4,
              "name": "Death Ward",
              "effect": "First time target would drop to 0 HP, they drop to 1 HP instead.",
              "source_paragraph": 9818,
              "casting_time": "1 action",
              "range": "60 feet",
              "duration": "Concentration, up to 1 minute",
              "components": "V, S, M/F",
              "resolution": "Automatic or opposed as described",
              "tags": [
                "Ward"
              ],
              "rp_cost": 7
            }
          }
        ],
        "possibleHistoricalAliases": []
      },
      "reviewFlags": [
        "Core resolution requires an explicit operational interpretation",
        "Not selectable in this spell playtest packet until individual operational review"
      ]
    }
  },
  {
    "kind": "ordinary-spell-catalog",
    "spellId": "resurrection",
    "hasOperationalProcedure": false,
    "sourceObjectSha256": "7bd8e0cfd7390bd95dd2ae2637ababb87f3058c4def6cd82800346ce0a9535a8",
    "spell": {
      "id": "resurrection",
      "name": "Resurrection",
      "schools": [
        "Necromancy"
      ],
      "status": "blocked-pending-operational-review",
      "visibility": "public-source-review",
      "classAccess": {
        "Cleric": {
          "rank": 7,
          "minimumClassLevel": 13,
          "school": "Necromancy",
          "baseRpCost": 17
        },
        "Druid": {
          "rank": 7,
          "minimumClassLevel": 13,
          "school": "Necromancy",
          "baseRpCost": 17
        },
        "Shaman": {
          "rank": 7,
          "minimumClassLevel": 19,
          "school": "Necromancy",
          "baseRpCost": 17
        },
        "Wizard": {
          "rank": 7,
          "minimumClassLevel": 13,
          "school": "Necromancy",
          "baseRpCost": 17
        }
      },
      "operational": null,
      "additionalRpCost": 0,
      "source": {
        "catalogPath": "src/data/spells.js",
        "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
        "catalogKey": "resurrection",
        "original": {
          "name": "Resurrection",
          "level": 7,
          "resonanceRank": 7,
          "school": "Necromancy",
          "schools": [
            "Necromancy"
          ],
          "placements": [
            {
              "name": "Resurrection",
              "school": "Necromancy",
              "level": 7,
              "summary": "Return a dead creature to life."
            }
          ],
          "classLevels": {
            "Cleric": 7,
            "Druid": 7,
            "Shaman": 7,
            "Wizard": 7
          },
          "classRanks": {
            "Cleric": 7,
            "Druid": 7,
            "Shaman": 7,
            "Wizard": 7
          },
          "classLearnLevels": {
            "Cleric": 13,
            "Druid": 13,
            "Shaman": 19,
            "Wizard": 13
          },
          "classSchools": {
            "Cleric": "Necromancy",
            "Druid": "Necromancy",
            "Shaman": "Necromancy",
            "Wizard": "Necromancy"
          },
          "castingTime": "Not specified in current rulebook",
          "range": "Not specified in current rulebook",
          "components": "Not specified in current rulebook",
          "duration": "Not specified in current rulebook",
          "description": "Return a dead creature to life.",
          "alternateSummaries": [],
          "classes": [
            "Cleric",
            "Druid",
            "Shaman",
            "Wizard"
          ],
          "status": "canon",
          "source": "Player Rulebook — Spell Lists"
        },
        "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
        "coreEntries": [
          {
            "index": 701,
            "original": {
              "school": "Necromancy",
              "level": 7,
              "name": "Resurrection",
              "effect": "Return a dead creature to life.",
              "source_paragraph": 9848,
              "casting_time": "1 action",
              "range": "120 feet",
              "duration": "Instantaneous",
              "components": "V, S, F",
              "resolution": "Automatic or opposed as described",
              "tags": [
                "Utility"
              ],
              "rp_cost": 17
            }
          }
        ],
        "possibleHistoricalAliases": []
      },
      "reviewFlags": [
        "Core resolution requires an explicit operational interpretation",
        "Not selectable in this spell playtest packet until individual operational review"
      ]
    }
  },
  {
    "kind": "ordinary-spell-catalog",
    "spellId": "mass-resurrection-denial",
    "hasOperationalProcedure": false,
    "sourceObjectSha256": "9979b9869d187aee99435be6283154576a1639fd64d4c11790d4b22594a8fb52",
    "spell": {
      "id": "mass-resurrection-denial",
      "name": "Mass Resurrection Denial",
      "schools": [
        "Necromancy"
      ],
      "status": "blocked-pending-operational-review",
      "visibility": "public-source-review",
      "classAccess": {
        "Cleric": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Necromancy",
          "baseRpCost": 21
        },
        "Druid": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Necromancy",
          "baseRpCost": 21
        },
        "Wizard": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Necromancy",
          "baseRpCost": 21
        }
      },
      "operational": null,
      "additionalRpCost": 0,
      "source": {
        "catalogPath": "src/data/spells.js",
        "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
        "catalogKey": "mass-resurrection-denial",
        "original": {
          "name": "Mass Resurrection Denial",
          "level": 8,
          "resonanceRank": 8,
          "school": "Necromancy",
          "schools": [
            "Necromancy"
          ],
          "placements": [
            {
              "name": "Mass Resurrection Denial",
              "school": "Necromancy",
              "level": 8,
              "summary": "Prevents resurrection of all corpses in area."
            }
          ],
          "classLevels": {
            "Cleric": 8,
            "Druid": 8,
            "Wizard": 8
          },
          "classRanks": {
            "Cleric": 8,
            "Druid": 8,
            "Wizard": 8
          },
          "classLearnLevels": {
            "Cleric": 15,
            "Druid": 15,
            "Wizard": 15
          },
          "classSchools": {
            "Cleric": "Necromancy",
            "Druid": "Necromancy",
            "Wizard": "Necromancy"
          },
          "castingTime": "Not specified in current rulebook",
          "range": "Not specified in current rulebook",
          "components": "Not specified in current rulebook",
          "duration": "Not specified in current rulebook",
          "description": "Prevents resurrection of all corpses in area.",
          "alternateSummaries": [],
          "classes": [
            "Cleric",
            "Druid",
            "Wizard"
          ],
          "status": "canon",
          "source": "Player Rulebook — Spell Lists"
        },
        "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
        "coreEntries": [
          {
            "index": 705,
            "original": {
              "school": "Necromancy",
              "level": 8,
              "name": "Mass Resurrection Denial",
              "effect": "Prevents resurrection of all corpses in area.",
              "source_paragraph": 9854,
              "casting_time": "1 action",
              "range": "120 feet",
              "duration": "Instantaneous",
              "components": "V, S, M/F",
              "resolution": "Automatic or opposed as described",
              "tags": [
                "Utility"
              ],
              "rp_cost": 21
            }
          }
        ],
        "possibleHistoricalAliases": []
      },
      "reviewFlags": [
        "Core resolution requires an explicit operational interpretation",
        "Not selectable in this spell playtest packet until individual operational review"
      ]
    }
  },
  {
    "kind": "ordinary-spell-catalog",
    "spellId": "true-resurrection",
    "hasOperationalProcedure": false,
    "sourceObjectSha256": "c926a01ab227991dc144f1c3ceac2fe2b305bd755de89d2d0be6807e2215cb04",
    "spell": {
      "id": "true-resurrection",
      "name": "True Resurrection",
      "schools": [
        "Necromancy"
      ],
      "status": "blocked-pending-operational-review",
      "visibility": "public-source-review",
      "classAccess": {
        "Cleric": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Druid": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Wizard": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        }
      },
      "operational": null,
      "additionalRpCost": 0,
      "source": {
        "catalogPath": "src/data/spells.js",
        "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
        "catalogKey": "true-resurrection",
        "original": {
          "name": "True Resurrection",
          "level": 9,
          "resonanceRank": 9,
          "school": "Necromancy",
          "schools": [
            "Necromancy"
          ],
          "placements": [
            {
              "name": "True Resurrection",
              "school": "Necromancy",
              "level": 9,
              "summary": "Return a dead creature to life, even without remains."
            }
          ],
          "classLevels": {
            "Cleric": 9,
            "Druid": 9,
            "Wizard": 9
          },
          "classRanks": {
            "Cleric": 9,
            "Druid": 9,
            "Wizard": 9
          },
          "classLearnLevels": {
            "Cleric": 17,
            "Druid": 17,
            "Wizard": 17
          },
          "classSchools": {
            "Cleric": "Necromancy",
            "Druid": "Necromancy",
            "Wizard": "Necromancy"
          },
          "castingTime": "Not specified in current rulebook",
          "range": "Not specified in current rulebook",
          "components": "Not specified in current rulebook",
          "duration": "Not specified in current rulebook",
          "description": "Return a dead creature to life, even without remains.",
          "alternateSummaries": [],
          "classes": [
            "Cleric",
            "Druid",
            "Wizard"
          ],
          "status": "canon",
          "source": "Player Rulebook — Spell Lists"
        },
        "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
        "coreEntries": [
          {
            "index": 721,
            "original": {
              "school": "Necromancy",
              "level": 9,
              "name": "True Resurrection",
              "effect": "Return a dead creature to life, even without remains.",
              "source_paragraph": 9872,
              "casting_time": "1 action",
              "range": "120 feet",
              "duration": "Instantaneous",
              "components": "V, S, F",
              "resolution": "Automatic or opposed as described",
              "tags": [
                "Utility"
              ],
              "rp_cost": 26
            }
          }
        ],
        "possibleHistoricalAliases": []
      },
      "reviewFlags": [
        "Core resolution requires an explicit operational interpretation",
        "Not selectable in this spell playtest packet until individual operational review"
      ]
    }
  },
  {
    "kind": "ordinary-spell-catalog",
    "spellId": "soul-bind",
    "hasOperationalProcedure": false,
    "sourceObjectSha256": "057ba7c49d000d6819c30be8ea58c1236f94da544c2e0c557dc749116bd6c2aa",
    "spell": {
      "id": "soul-bind",
      "name": "Soul Bind",
      "schools": [
        "Necromancy"
      ],
      "status": "blocked-pending-operational-review",
      "visibility": "public-source-review",
      "classAccess": {
        "Cleric": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Druid": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Wizard": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        }
      },
      "operational": null,
      "additionalRpCost": 0,
      "source": {
        "catalogPath": "src/data/spells.js",
        "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
        "catalogKey": "soul-bind",
        "original": {
          "name": "Soul Bind",
          "level": 9,
          "resonanceRank": 9,
          "school": "Necromancy",
          "schools": [
            "Necromancy"
          ],
          "placements": [
            {
              "name": "Soul Bind",
              "school": "Necromancy",
              "level": 9,
              "summary": "Trap a dying creature's soul, preventing resurrection."
            }
          ],
          "classLevels": {
            "Cleric": 9,
            "Druid": 9,
            "Wizard": 9
          },
          "classRanks": {
            "Cleric": 9,
            "Druid": 9,
            "Wizard": 9
          },
          "classLearnLevels": {
            "Cleric": 17,
            "Druid": 17,
            "Wizard": 17
          },
          "classSchools": {
            "Cleric": "Necromancy",
            "Druid": "Necromancy",
            "Wizard": "Necromancy"
          },
          "castingTime": "Not specified in current rulebook",
          "range": "Not specified in current rulebook",
          "components": "Not specified in current rulebook",
          "duration": "Not specified in current rulebook",
          "description": "Trap a dying creature's soul, preventing resurrection.",
          "alternateSummaries": [],
          "classes": [
            "Cleric",
            "Druid",
            "Wizard"
          ],
          "status": "canon",
          "source": "Player Rulebook — Spell Lists"
        },
        "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
        "coreEntries": [
          {
            "index": 725,
            "original": {
              "school": "Necromancy",
              "level": 9,
              "name": "Soul Bind",
              "effect": "Trap a dying creature's soul, preventing resurrection.",
              "source_paragraph": 9876,
              "casting_time": "1 action",
              "range": "120 feet",
              "duration": "Instantaneous",
              "components": "V, S, F",
              "resolution": "Automatic or opposed as described",
              "tags": [
                "Utility"
              ],
              "rp_cost": 26
            }
          }
        ],
        "possibleHistoricalAliases": []
      },
      "reviewFlags": [
        "Core resolution requires an explicit operational interpretation",
        "Not selectable in this spell playtest packet until individual operational review"
      ]
    }
  }
]
```

## Previously reviewed Decay and Doomed profiles

```json
[
  {
    "mechanicalId": "oracle.decay",
    "displayName": "Decay",
    "kind": "rider",
    "status": "reviewed-proposal; final registry validation pending",
    "familyTags": [],
    "effect": "No HP recovery, -1 saves; +S flat allied attack damage once per attacker per turn and at most 3 allied hits/round; corpses within 2 tiles cannot be raised. Not doubled vulnerability.",
    "ending": "Initial failed CON save begins; repeat CON save end each regular target turn; success ends all; third such endpoint ends regardless.",
    "stacking": "No numerical stacking; independent source records retain their printed endpoints.",
    "immunityRule": "Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.",
    "applicationSources": [
      {
        "kind": "card",
        "path": "data/public/class_playtests/oracle.json",
        "cardId": "oracle.supplement.bones.rotting-touch",
        "originalDisplayName": "Rotting Touch",
        "effect": "Make a Revelation attack. On hit the target makes a Constitution save. On failure it gains Decay for up to 3 rounds: attacks against it add S damage once per attacker per turn, it takes -1 on saving throws and cannot regain HP. At the end of each turn it repeats the save, ending Decay on success. Corpses within 2 tiles of a Decayed creature cannot be raised while Decay persists. If the target is undead, it also takes 2d6 necrotic damage on the initial hit and you regain half the actual damage dealt, capped at S+M HP. At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack.",
        "duration": "Maximum 3 rounds",
        "sourceObjectSha256": "142a2e2ba3c0a79aa4e9f6b1768eeb11f3ceaffc253e636aa9c69f9907260411"
      }
    ],
    "integrationDecisions": [
      "NEW precise three-turn schedule; interaction with natural20/Stable recovery still under conference.",
      "Blocks all HP increases, including natural-20 death recovery. Blocked natural 20 clears death counters and stabilizes at zero with one ordinary d4-hour deadline.",
      "An already-due Stable recovery retains its absolute deadline while prohibited; ending prohibition resolves one HP only if still living, Stable and at zero. Damage/death cancels normally.",
      "Legal positive-potential magical healing can trigger an applicable Bleed cure even with zero actual HP regained. Separately printed condition removal remains legal."
    ],
    "reviewEvidence": [
      "docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md",
      "docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md",
      "docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md",
      "docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md"
    ]
  }
]
```

## Existing track bridge that is NOT a resurrection decision

ExpeditionStrain0–6: everypositiveunpreventedgainthatwouldreach/exceed6resolvesdeathunlessTHATsourceexplicitnonlethalexceptioncollapse. Repeatedgainat6lethalotherwise; preventedgainnone. CollapsealiveUnconsciousSpeed0noact/travel,doesnotitselfsetHP0/createStable/deathsave. Independentdying0remainsdying. Only24hHavencare/explicittreatmentcanreducecollapsed6; qualifyingremovablegateMetpointsremoved;specialgatedpointsremain. Loweringbelow6endsowncollapseonly,notdeadstate. Serum0–3differentnamespace. Exhaustion6death,differenttrack;noautomaticresurrectionfromlevelremoval. Resurrectionat6wasdeliberatelyleftOPEN. Wounddeathat3isfailedsubsequentWoundsave,notstatic3Wounddeath. Fullsourceevidencepreservedinpreviousconferences.
