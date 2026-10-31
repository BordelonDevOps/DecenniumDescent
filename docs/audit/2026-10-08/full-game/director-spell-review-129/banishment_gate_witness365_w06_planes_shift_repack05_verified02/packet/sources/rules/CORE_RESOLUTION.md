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
